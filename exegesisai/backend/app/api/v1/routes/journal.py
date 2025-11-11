from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class JournalCreate(BaseModel):
	title: str
	content: str


@router.post("")
def create_journal(payload: JournalCreate):
	return {"id": "jr_001", "title": payload.title, "content": payload.content}


@router.get("")
def list_journal():
	return {"items": []}
*** End Patch

