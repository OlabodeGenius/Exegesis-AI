from fastapi import APIRouter, Query

router = APIRouter()


@router.get("/lookup")
def lookup(ref: str = Query(..., description="e.g., Romans 12:2"), translation: str = "ESV"):
	# Stubbed response
	return {"ref": ref, "translation": translation, "text": "Do not be conformed to this world... (stub)"
	}


@router.get("/context")
def context(ref: str, window: int = 1):
	return {"ref": ref, "window": window, "before": [], "after": []}


@router.get("/crossrefs")
def crossrefs(ref: str):
	return {"ref": ref, "crossrefs": ["2 Corinthians 3:18"]}


@router.get("/search")
def search(q: str, mode: str = "keyword"):
	return {"mode": mode, "results": []}
*** End Patch

