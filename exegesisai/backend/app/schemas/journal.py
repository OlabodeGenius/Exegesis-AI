from datetime import datetime

from pydantic import BaseModel, Field


class JournalCreate(BaseModel):
    title: str
    content: str


class JournalEntry(BaseModel):
    id: str
    title: str
    content: str
    created_at: datetime = Field(alias="created_at")

    class Config:
        populate_by_name = True


class JournalListResponse(BaseModel):
    items: list[JournalEntry]
