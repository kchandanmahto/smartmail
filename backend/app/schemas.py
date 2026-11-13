
from typing import Literal
from pydantic import BaseModel, Field


class EmailRequest(BaseModel):
    email: str = Field(min_length=10, max_length=15000)
    tone: Literal[
        "professional",
        "friendly",
        "formal"
    ] = "professional"

    length: Literal[
        "short",
        "medium",
        "detailed"
    ] = "medium"


class EmailAnalysis(BaseModel):
    intent: str
    category: str
    sentiment: Literal[
        "positive",
        "neutral",
        "negative"
    ]
    priority: Literal[
        "low",
        "medium",
        "high"
    ]
    summary: str
    key_points: list[str]
    requires_response: bool


class EmailResponse(BaseModel):
    id: int
    analysis: EmailAnalysis
    reply: str
    tone: str
    length: str
    created_at: str


class HistoryItem(BaseModel):
    id: int
    email: str
    category: str
    priority: str
    sentiment: str
    tone: str
    created_at: str


