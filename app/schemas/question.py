from typing import List

from pydantic import BaseModel


class Question(BaseModel):
    id: int
    text: str
    answers: List[str]
    correct_answer: str

