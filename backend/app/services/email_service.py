
from app.agents.graph import run_email_graph


def process_email(email: str, tone: str, length: str):

    result = run_email_graph(
        email=email,
        tone=tone,
        length=length
    )

    return {
        "analysis": result["analysis"],
        "reply": result["reply"]
    }

