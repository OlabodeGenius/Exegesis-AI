from fastapi import APIRouter, HTTPException, status

from ....schemas import ExportRequest, ExportResponse
from ....services.datastore import store

router = APIRouter()


@router.post("", response_model=ExportResponse, summary="Create a study or journal export bundle")
async def create_export(payload: ExportRequest) -> ExportResponse:
    return store.create_export(payload)


@router.get("/{export_id}", response_model=ExportResponse, summary="Download an export bundle")
async def get_export(export_id: str) -> ExportResponse:
    export = store.get_export(export_id)
    if not export:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Export not found")
    return export
