from fastapi import APIRouter

from .routes import auth, verses, study, notes, exports, journal, devotional, recommendations


api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(verses.router, prefix="/verses", tags=["verses"])
api_router.include_router(study.router, prefix="/study", tags=["study"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(journal.router, prefix="/journal", tags=["journal"])
api_router.include_router(devotional.router, prefix="/devotional", tags=["devotional"])
api_router.include_router(recommendations.router, prefix="/recommendations", tags=["recommendations"])
api_router.include_router(exports.router, prefix="/exports", tags=["exports"])
*** End Patch``` } ***!

