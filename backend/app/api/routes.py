
import json
import logging

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import EmailRequest
from app.services.email_service import process_email
from app.services.history_service import (
    save_history,
    get_history,
    get_history_by_id,
    delete_history
)


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["SmartMail AI"])


@router.post("/generate")
def generate_email_reply(
    request: EmailRequest,
    db: Session = Depends(get_db)
):
    try:
        logger.info("Email generation request received")

        result = process_email(
            email=request.email,
            tone=request.tone,
            length=request.length
        )

        if not isinstance(result, dict):
            raise ValueError("Invalid response from email processing service")

        if "analysis" not in result or "reply" not in result:
            raise ValueError("Email processing response is missing analysis or reply")

        record = save_history(
            db=db,
            email=request.email,
            analysis=result["analysis"],
            reply=result["reply"],
            tone=request.tone,
            length=request.length
        )

        logger.info("Email reply generated successfully. History ID: %s", record.id)

        return {
            "success": True,
            "data": {
                "id": record.id,
                "analysis": result["analysis"],
                "reply": result["reply"],
                "tone": record.tone,
                "length": record.length,
                "created_at": record.created_at.isoformat()
            }
        }

    except Exception as error:
        logger.exception("Email generation failed")

        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Email processing failed: {str(error)}"
        ) from error


@router.get("/history")
def email_history(
    db: Session = Depends(get_db)
):
    try:
        records = get_history(db)

        return {
            "success": True,
            "data": [
                {
                    "id": item.id,
                    "email": item.email,
                    "analysis": json.loads(item.analysis),
                    "reply": item.reply,
                    "tone": item.tone,
                    "length": item.length,
                    "created_at": item.created_at.isoformat()
                }
                for item in records
            ]
        }

    except Exception as error:
        logger.exception("Failed to retrieve email history")

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve email history"
        ) from error


@router.get("/history/{record_id}")
def email_history_detail(
    record_id: int,
    db: Session = Depends(get_db)
):
    try:
        item = get_history_by_id(db, record_id)

        if not item:
            raise HTTPException(
                status_code=404,
                detail="History record not found"
            )

        return {
            "success": True,
            "data": {
                "id": item.id,
                "email": item.email,
                "analysis": json.loads(item.analysis),
                "reply": item.reply,
                "tone": item.tone,
                "length": item.length,
                "created_at": item.created_at.isoformat()
            }
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Failed to retrieve history record: %s", record_id)

        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve history record"
        ) from error


@router.delete("/history/{record_id}")
def remove_history(
    record_id: int,
    db: Session = Depends(get_db)
):
    try:
        deleted = delete_history(db, record_id)

        if not deleted:
            raise HTTPException(
                status_code=404,
                detail="History record not found"
            )

        return {
            "success": True,
            "message": "History deleted successfully"
        }

    except HTTPException:
        raise

    except Exception as error:
        logger.exception("Failed to delete history record: %s", record_id)

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Failed to delete history record"
        ) from error

