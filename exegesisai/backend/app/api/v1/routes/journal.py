from fastapi import APIRouter

from ....schemas import JournalCreate, JournalEntry, JournalListResponse
from ....services.datastore import store

router = APIRouter()


@router.post("", response_model=JournalEntry, summary="Create a journal entry")
async def create_journal(payload: JournalCreate) -> JournalEntry:
    return store.create_journal(payload)


@router.get("", response_model=JournalListResponse, summary="List journal entries")
async def list_journal() -> JournalListResponse:
    return store.list_journal()
