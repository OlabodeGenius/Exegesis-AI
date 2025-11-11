from datetime import datetime
from typing import List, Literal, Optional

from pydantic import BaseModel, Field


class ObservationSection(BaseModel):
    keywords: List[str]
    clauses: List[str]


class InterpretationSection(BaseModel):
    historical_context: str
    theological_themes: List[str] = Field(default_factory=list)
    cross_references: List[str] = Field(alias="crossrefs", default_factory=list)

    class Config:
        populate_by_name = True


class ApplicationPrompt(BaseModel):
    question: str
    action_step: Optional[str] = None


class ApplicationSection(BaseModel):
    prompts: List[ApplicationPrompt]


class StudyRunRequest(BaseModel):
    reference: str
    translation: str = "ESV"
    depth: Literal["light", "standard", "deep"] = "standard"
    include: List[Literal["observation", "interpretation", "application"]] = Field(
        default_factory=lambda: ["observation", "interpretation", "application"]
    )
    return_sources: bool | None = Field(default=False, alias="return_sources")

    class Config:
        populate_by_name = True


class StudyRunResponse(BaseModel):
    reference: str
    translation: str
    observation: ObservationSection | None = None
    interpretation: InterpretationSection | None = None
    application: ApplicationSection | None = None
    generated_at: datetime


class StudyJobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "running", "completed", "failed"]
    result: StudyRunResponse | None = None
