from fastapi import APIRouter, Query

from ....core.config import settings
from ....schemas import (
    CrossReferencesResponse,
    VerseContextResponse,
    VerseLookupResponse,
    VerseSearchResponse,
)
from ....services.bible.provider import BibleProvider

router = APIRouter()
provider = BibleProvider(api_key=settings.bible_api_key, provider=settings.bible_api_provider)


@router.get("/lookup", response_model=VerseLookupResponse, summary="Retrieve a single verse")
async def lookup(
    ref: str = Query(..., description="Canonical reference, e.g. Romans 12:2"),
    translation: str = Query("ESV", description="Translation code (ESV, NIV, KJV, etc.)"),
) -> VerseLookupResponse:
    verse = await provider.lookup(ref, translation)
    return VerseLookupResponse(reference=verse.reference, translation=verse.translation, text=verse.text)


@router.get("/context", response_model=VerseContextResponse, summary="Read verse with its immediate context")
async def context(
    ref: str,
    translation: str = "ESV",
    window: int = Query(1, ge=1, le=3, description="Number of verses to include before and after"),
) -> VerseContextResponse:
    verses = await provider.context(ref, translation, window)
    before = [verses[0].text] if len(verses) > 1 else []
    after = [verses[-1].text] if len(verses) > 1 else []
    return VerseContextResponse(
        reference=ref,
        translation=translation,
        window=window,
        before=before,
        after=after,
    )


@router.get("/crossrefs", response_model=CrossReferencesResponse, summary="Retrieve semantic cross references")
async def crossrefs(ref: str) -> CrossReferencesResponse:
    related = await provider.cross_references(ref)
    return CrossReferencesResponse(reference=ref, crossrefs=related)


@router.get("/search", response_model=VerseSearchResponse, summary="Search verses by keyword or semantics")
async def search(q: str, mode: str = Query("keyword", pattern="^(keyword|semantic)$")) -> VerseSearchResponse:
    results = await provider.search(q, mode=mode)
    return VerseSearchResponse(mode=mode, query=q, results=results)
