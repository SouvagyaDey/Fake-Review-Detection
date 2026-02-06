from pydantic import BaseModel
from typing import List

class TextRequest(BaseModel):
    review: str

class BatchRequest(BaseModel):
    reviews: List[str]

class PredictionResponse(BaseModel):
    label: str
    confidence: float

class ExplainResponse(BaseModel):
    label: str
    confidence: float
    important_tokens: List[str]

class ModerateResponse(BaseModel):
    label: str
    confidence: float
    action: str
