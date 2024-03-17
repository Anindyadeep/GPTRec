import uuid
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    id: str = Field(default=str(uuid.uuid4()))
    query: str


class RecommendationResponse(BaseModel):
    search_id: str
    response_id: str
    search_query: str 
    search_results: dict 


class ErrorResponse(BaseModel):
    id: str
    error_id: int
    error_msg: str


class ChatRequest(BaseModel):
    id: str = Field(default=str(uuid.uuid4()))
    query: str
    temperature: float = Field(default=0.1)
    max_length: int = Field(default=200)
