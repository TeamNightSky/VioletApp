"""Registers endpoints for the api sub-mounted app."""
from datetime import datetime, timedelta
from typing import Any, Dict

from fastapi import APIRouter

from violet.models import Auth

auth_router = APIRouter()


@auth_router.post("/token/refresh")
async def refresh_token(auth: Auth) -> Auth:
    """Invalidates the current token and returns a new one with newer expiration date."""
    payload = auth.decode()
    if "exp" in payload:
        del payload["exp"]

    return Auth.from_payload(**payload, exp=datetime.utcnow() + timedelta(hours=24))


@auth_router.get("/token")
async def get_token_info(auth: Auth) -> Dict[str, Any]:
    """Returns currently used JWT details."""
    return auth.decode()
