
import json

from datetime import datetime, timezone
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, Session

from app.database import Base


class EmailHistory(Base):

    __tablename__ = "email_history"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    email: Mapped[str] = mapped_column(Text)

    analysis: Mapped[str] = mapped_column(Text)

    reply: Mapped[str] = mapped_column(Text)

    tone: Mapped[str] = mapped_column(String(30))

    length: Mapped[str] = mapped_column(String(30))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )


def save_history(
    db: Session,
    email: str,
    analysis: dict,
    reply: str,
    tone: str,
    length: str
):

    record = EmailHistory(
        email=email,
        analysis=json.dumps(analysis),
        reply=reply,
        tone=tone,
        length=length
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_history(db: Session):

    return (
        db.query(EmailHistory)
        .order_by(EmailHistory.id.desc())
        .all()
    )


def get_history_by_id(db: Session, record_id: int):

    return db.query(EmailHistory).filter(
        EmailHistory.id == record_id
    ).first()


def delete_history(db: Session, record_id: int):

    record = get_history_by_id(db, record_id)

    if not record:
        return False

    db.delete(record)
    db.commit()

    return True


