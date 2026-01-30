from typing import List

from pydantic import BaseModel


class Citation(BaseModel):
    text: str
    url: str = None
    section: str = None


class AgentAnswer(BaseModel):
    answer: str
    citations: List[Citation]
