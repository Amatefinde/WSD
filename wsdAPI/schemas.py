from pydantic import BaseModel
from typing import List


class BaseInput(BaseModel):
    word: str
    context: str
    meanings: List[str]