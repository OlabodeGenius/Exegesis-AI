from fastapi import APIRouter, Query

from ....schemas import Note, NoteCreate, NotesResponse
from ....services.datastore import store

router = APIRouter()


@router.post("", response_model=Note, summary="Persist a personal study note")
async def add_note(payload: NoteCreate) -> Note:
    return store.add_note(payload)


@router.get("", response_model=NotesResponse, summary="Retrieve notes for a verse")
async def list_notes(verse_ref: str = Query(..., description="Canonical verse reference")) -> NotesResponse:
    return store.list_notes(verse_ref)
