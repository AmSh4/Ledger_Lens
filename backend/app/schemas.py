from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class EntryCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)

class EntryOut(BaseModel):
    id: int
    title: str
    content: str
    tags: List[str]
    timestamp: datetime
    prev_hash: str
    content_hash: str
    current_hash: str
    attachments: List[dict]
    class Config:
        from_attributes = True
