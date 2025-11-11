import secrets

from fastapi import APIRouter, HTTPException, status

from ....core.config import settings
from ....schemas import AuthResponse, LoginRequest, SignupRequest

router = APIRouter()


def _issue_tokens() -> AuthResponse:
    return AuthResponse(
        access_token=secrets.token_urlsafe(32),
        refresh_token=secrets.token_urlsafe(48),
    )


@router.post("/signup", response_model=AuthResponse, summary="Register a new user")
async def signup(payload: SignupRequest) -> AuthResponse:
    if settings.env != "dev":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Signups are disabled in this environment.",
        )
    return _issue_tokens()


@router.post("/login", response_model=AuthResponse, summary="Login and receive JWT tokens")
async def login(payload: LoginRequest) -> AuthResponse:
    # Stubbed login flow – replace with real authentication provider
    if payload.password == "invalid":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return _issue_tokens()


@router.post("/logout", summary="Invalidate the current session")
async def logout() -> dict[str, bool]:
    return {"ok": True}
