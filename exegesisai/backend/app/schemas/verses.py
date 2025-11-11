from pydantic import BaseModel, Field
from typing import List


class VerseLookupResponse(BaseModel):
    reference: str = Field(alias="ref")
    translation: str
    text: str

    class Config:
        populate_by_name = True


class VerseContextResponse(BaseModel):
    reference: str = Field(alias="ref")
    translation: str
    window: int
    before: List[str]
    after: List[str]

    class Config:
        populate_by_name = True


class CrossReferencesResponse(BaseModel):
    reference: str = Field(alias="ref")
    cross_references: List[str] = Field(alias="crossrefs")

    class Config:
        populate_by_name = True


class VerseSearchResponse(BaseModel):
    mode: str
    query: str
    results: list[dict]  # stubbed result payload
