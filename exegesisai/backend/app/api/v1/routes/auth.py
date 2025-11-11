from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

router = APIRouter()


class SignupRequest(BaseModel):
	email: EmailStr
	password: str
	displayName: str | None = None


class AuthResponse(BaseModel):
	accessToken: str
	refreshToken: str | None = None


@router.post("/signup", response_model=AuthResponse)
def signup(payload: SignupRequest):
	# Stubbed signup
	return AuthResponse(accessToken="stub.jwt.token", refreshToken="stub.refresh.token")


class LoginRequest(BaseModel):
	email: EmailStr
	password: str


@router.post("/login", response_model=AuthResponse)
def login(payload: LoginRequest):
	# Stubbed login
	return AuthResponse(accessToken="stub.jwt.token", refreshToken="stub.refresh.token")


@router.post("/logout")
def logout():
	return {"ok": True}
*** End Patch  \n```} ***!

