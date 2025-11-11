from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class NoteCreate(BaseModel):
    verse_ref: str
    stage: Literal["observation", "interpretation", "application"]
    content_md: str = Field(alias="content_md")

    class Config:
        populate_by_name = True


class Note(BaseModel):
    id: str
    verse_ref: str
    stage: Literal["observation", "interpretation", "application"]
    content_md: str = Field(alias="content_md")
    created_at: datetime

    class Config:
        populate_by_name = True


class NotesResponse(BaseModel):
    verse_ref: str
    notes: list[Note]
