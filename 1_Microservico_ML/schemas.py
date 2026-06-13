from pydantic import BaseModel, Field

class TicketRequest(BaseModel):
    # Garante que ninguém envie um texto vazio ou gigantesco para travar a IA
    text: str = Field(..., min_length=5, max_length=1000)

class TicketResponse(BaseModel):
    id: int
    text: str
    sentiment: str
    confidence_score: float
    insight: str
    priority: str
    routed_to_llm: bool
    processing_time_ms: float

    class Config:
        from_attributes = True