from __future__ import annotations

from datetime import datetime, timezone
from typing import Iterable

from ..schemas import (
    ApplicationPrompt,
    ApplicationSection,
    InterpretationSection,
    ObservationSection,
    StudyRunRequest,
    StudyRunResponse,
)


class StudyOrchestrator:
    """
    Lightweight orchestrator that mimics the Observation → Interpretation → Application pipeline.

    This class is intentionally deterministic and fast so that the onboarding experience
    works even without external ML dependencies. Swap its internals with real model
    calls or task queues when integrating production services.
    """

    @staticmethod
    def _extract_keywords(reference: str) -> list[str]:
        tokens = [token.strip(",.;:").lower() for token in reference.split()]
        return sorted({token for token in tokens if len(token) > 3})

    @staticmethod
    def _clauses(reference: str) -> list[str]:
        parts = reference.split(";")
        if len(parts) == 1:
            return [reference]
        return [part.strip() for part in parts if part.strip()]

    @staticmethod
    def _crossrefs(reference: str) -> list[str]:
        book = reference.split()[0]
        mapping: dict[str, Iterable[str]] = {
            "Genesis": ["John 1:1", "Romans 5:12"],
            "Psalms": ["John 10:11", "Philippians 4:6"],
            "Romans": ["Ephesians 4:23", "2 Corinthians 3:18"],
        }
        return list(mapping.get(book, []))

    def run(self, request: StudyRunRequest) -> StudyRunResponse:
        observation = None
        if "observation" in request.include:
            observation = ObservationSection(
                keywords=self._extract_keywords(request.reference),
                clauses=self._clauses("Do not be conformed; be transformed by the renewal of your mind."),
            )

        interpretation = None
        if "interpretation" in request.include:
            interpretation = InterpretationSection(
                historical_context=(
                    "Paul contrasts the prevailing cultural pressures with the Spirit-led renewal "
                    "available to believers."
                ),
                theological_themes=["Sanctification", "Renewal", "Holy Spirit"],
                crossrefs=list(self._crossrefs(request.reference)),
            )

        application = None
        if "application" in request.include:
            prompts = [
                ApplicationPrompt(
                    question="Where are you tempted to conform to surrounding cultural norms?",
                    action_step="List one habit that needs renewal this week.",
                ),
                ApplicationPrompt(
                    question="How can Scripture reshape your thinking today?",
                    action_step="Memorize the key clause from this verse.",
                ),
            ]
            application = ApplicationSection(prompts=prompts)

        return StudyRunResponse(
            reference=request.reference,
            translation=request.translation,
            observation=observation,
            interpretation=interpretation,
            application=application,
            generated_at=datetime.now(tz=timezone.utc),
        )
