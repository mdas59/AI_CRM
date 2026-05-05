from pydantic import BaseModel
from typing import Optional


class InteractionCreate(BaseModel):
    hcp_name: str
    interaction_type: str
    interaction_date:  str
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_action: Optional[str] = None
    summary: Optional[str] = None

class InteractionUpdate(BaseModel):
    hcp_name: Optional[str] = None
    interaction_type: Optional[str] = None
    interaction_date: Optional[str] = None
    topics_discussed: Optional[str] = None
    materials_shared: Optional[str] = None
    samples_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcome: Optional[str] = None
    follow_up_action: Optional[str] = None
    summary: Optional[str] = None


class InteractionResponse(InteractionCreate):
    id: int

    class Config:
        from_attributes = True