from pydantic import BaseModel


class RecommendationItem(BaseModel):
    reference: str
    reason: str


class RecommendationsResponse(BaseModel):
    items: list[RecommendationItem]
