from fastapi import APIRouter, Query
from pydantic import BaseModel
from typing import Literal

router = APIRouter()


class NoteCreate(BaseModel):
	verse_ref: str
	stage: Literal["observation", "interpretation", "application"]
	content_md: str


@router.post("")
def add_note(payload: NoteCreate):
	return {"ok": True, "note": payload.model_dump()}


@router.get("")
def list_notes(verse_ref: str = Query(...)):
	return {"verse_ref": verse_ref, "notes": []}
*** End Patch

