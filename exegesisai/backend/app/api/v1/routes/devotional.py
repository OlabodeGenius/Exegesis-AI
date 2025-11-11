from datetime import date

from fastapi import APIRouter

from ....schemas import DevotionalResponse

router = APIRouter()

_ROTATING_DEVOTIONALS = [
    (
        "Psalm 23:1",
        "The LORD is my shepherd; I shall not want.",
        "Rest in the Shepherd who provides and guides.",
    ),
    (
        "Romans 12:2",
        "Do not be conformed to this world, but be transformed by the renewal of your mind...",
        "Invite the Spirit to renew your thoughts today.",
    ),
    (
        "Joshua 1:9",
        "Be strong and courageous. Do not be frightened, and do not be dismayed...",
        "Bold obedience grows from God’s faithful presence.",
    ),
]


@router.get("/today", response_model=DevotionalResponse, summary="Daily devotional verse and reflection")
async def today() -> DevotionalResponse:
    index = date.today().toordinal() % len(_ROTATING_DEVOTIONALS)
    reference, text, reflection = _ROTATING_DEVOTIONALS[index]
    return DevotionalResponse(reference=reference, text=text, reflection=reflection, date=date.today())
