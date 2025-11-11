from fastapi import APIRouter

router = APIRouter()


@router.get("/today")
def today():
	return {
		"reference": "Psalm 23:1",
		"text": "The LORD is my shepherd; I shall not want. (stub)",
		"reflection": "Trust God’s provision today.",
	}
*** End Patch

