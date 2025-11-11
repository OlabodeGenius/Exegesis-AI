from __future__ import annotations

from datetime import datetime, timezone
from threading import Lock
import uuid

from ..schemas import (
    ExportRequest,
    ExportResponse,
    JournalCreate,
    JournalEntry,
    JournalListResponse,
    Note,
    NoteCreate,
    NotesResponse,
)


class InMemoryStore:
    """
    Demo-grade persistence layer.

    Replaces a proper database so the API behaves realistically during local exploration.
    """

    def __init__(self) -> None:
        self._lock = Lock()
        self._notes: list[Note] = []
        self._journals: list[JournalEntry] = []
        self._exports: dict[str, ExportResponse] = {}

    def add_note(self, payload: NoteCreate) -> Note:
        with self._lock:
            note = Note(
                id=str(uuid.uuid4()),
                verse_ref=payload.verse_ref,
                stage=payload.stage,
                content_md=payload.content_md,
                created_at=datetime.now(tz=timezone.utc),
            )
            self._notes.append(note)
        return note

    def list_notes(self, verse_ref: str) -> NotesResponse:
        with self._lock:
            notes = [note for note in self._notes if note.verse_ref == verse_ref]
        return NotesResponse(verse_ref=verse_ref, notes=notes)

    def create_journal(self, payload: JournalCreate) -> JournalEntry:
        with self._lock:
            entry = JournalEntry(
                id=str(uuid.uuid4()),
                title=payload.title,
                content=payload.content,
                created_at=datetime.now(tz=timezone.utc),
            )
            self._journals.append(entry)
        return entry

    def list_journal(self) -> JournalListResponse:
        with self._lock:
            items = list(self._journals)
        return JournalListResponse(items=items)

    def create_export(self, payload: ExportRequest) -> ExportResponse:
        with self._lock:
            export_id = str(uuid.uuid4())
            export = ExportResponse(
                id=export_id,
                status="ready" if payload.format != "pdf" else "processing",
                format=payload.format,
                url=None,
                created_at=datetime.now(tz=timezone.utc),
            )
            if export.status == "ready":
                export.url = f"https://example.com/exports/{export_id}.{payload.format}"
            self._exports[export_id] = export
        return export

    def get_export(self, export_id: str) -> ExportResponse | None:
        with self._lock:
            return self._exports.get(export_id)


store = InMemoryStore()
