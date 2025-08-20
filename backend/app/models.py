from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class Attachment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    entry_id: int = Field(foreign_key="journalentry.id")
    filename: str
    sha256: str
    path: str

class JournalEntry(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    tags: str = ""
    timestamp: datetime
    prev_hash: str
    content_hash: str
    current_hash: str
    attachments: List[Attachment] = Relationship(back_populates=None)
