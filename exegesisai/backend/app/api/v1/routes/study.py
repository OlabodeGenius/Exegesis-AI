from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from ....schemas import (
    ObservationSection,
    StudyJobStatus,
    StudyRunRequest,
    StudyRunResponse,
)
from ....services.orchestrator import StudyOrchestrator

router = APIRouter()
orchestrator = StudyOrchestrator()

_demo_request = StudyRunRequest(reference="Romans 12:2")
_demo_result = orchestrator.run(_demo_request)
JOB_STORE: dict[str, StudyJobStatus] = {
    "demo-job": StudyJobStatus(job_id="demo-job", status="completed", result=_demo_result)
}


@router.post("/run", response_model=StudyRunResponse, summary="Execute the full OIA study pipeline")
async def run_study(payload: StudyRunRequest) -> StudyRunResponse:
    return orchestrator.run(payload)


@router.post("/observation", response_model=ObservationSection, summary="Run only the Observation step")
async def observation(payload: StudyRunRequest) -> ObservationSection:
    result = orchestrator.run(payload.model_copy(update={"include": ["observation"]}))
    assert result.observation is not None
    return result.observation


@router.post("/interpretation", summary="Run only the Interpretation step")
async def interpretation(payload: StudyRunRequest) -> dict:
    result = orchestrator.run(payload.model_copy(update={"include": ["interpretation"]}))
    if not result.interpretation:
        return {"historical_context": "", "crossrefs": []}
    return result.interpretation.model_dump(by_alias=True)


@router.post("/application", summary="Run only the Application step")
async def application(payload: StudyRunRequest) -> dict:
    result = orchestrator.run(payload.model_copy(update={"include": ["application"]}))
    if not result.application:
        return {"prompts": []}
    return result.application.model_dump()


@router.get("/jobs/{job_id}", response_model=StudyJobStatus, summary="Check status of an async study job")
async def job_status(job_id: str) -> StudyJobStatus:
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return job
