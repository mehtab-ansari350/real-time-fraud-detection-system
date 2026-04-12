from pydantic import BaseModel
from typing import List

class Transaction(BaseModel):
    features: List[float]
    