from fastapi import APIRouter, Query

from ....schemas import RecommendationItem, RecommendationsResponse

router = APIRouter()


@router.get(
    "/verses",
    response_model=RecommendationsResponse,
    summary="Suggest related verses based on semantic themes",
)
async def recommended_verses(theme: str = Query("renewal", description="Theme or keyword to explore")) -> RecommendationsResponse:
    themes = {
        "renewal": [
            RecommendationItem(reference="Ephesians 4:23", reason="Shared theme of mind renewal"),
            RecommendationItem(reference="Colossians 3:2", reason="Set minds on things above"),
        ],
        "shepherd": [
            RecommendationItem(reference="John 10:11", reason="Jesus fulfils the shepherd promise"),
            RecommendationItem(reference="Isaiah 40:11", reason="Prophetic shepherd imagery"),
        ],
    }
    items = themes.get(theme.lower(), themes["renewal"])
    return RecommendationsResponse(items=items)
