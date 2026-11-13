
from typing import TypedDict


class EmailState(TypedDict, total=False):
    email: str
    tone: str
    length: str
    analysis: dict
    reply: str


