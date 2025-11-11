from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class ExportRequest(BaseModel):
    study_id: str | None = Field(default=None, alias="study_id")
    journal_id: str | None = Field(default=None, alias="journal_id")
    format: Literal["pdf", "markdown", "json"] = "pdf"

    class Config:
        populate_by_name = True


class ExportResponse(BaseModel):
    id: str
    status: Literal["processing", "ready", "failed"]
    format: Literal["pdf", "markdown", "json"]
    url: str | None = None
    created_at: datetime
