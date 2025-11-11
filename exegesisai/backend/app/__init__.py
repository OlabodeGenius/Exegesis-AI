"""
ExegesisAI backend application package.

This module exposes the ASGI application instance so that external
servers (e.g., gunicorn/uvicorn) can import it directly via
`backend.app:app`.
"""

from .main import app

__all__ = ["app"]
