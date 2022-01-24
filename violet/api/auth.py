"""Registers endpoints for the api sub-mounted app."""
from datetime import datetime, timedelta

from fastapi import Depends, Form, HTTPException

from violet.models import Auth

from .app import api


async def verify_auth(auth: Auth) -> Auth:
    """Verifies integrity of the oauth token."""
    if not auth.decode():
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return auth


@api.post("/auth/token/refresh")
async def refresh_token(auth: Auth = Depends(verify_auth)) -> Auth:
    """Invalidates the current token and returns a new one with newer expiration date."""
    # -TODO: invalidate previous auth
    del auth.payload["expire_at"]
    return Auth.from_payload(
        **auth.payload, expire_at=datetime.utcnow() + timedelta(hours=24)
    )


@api.get("/auth/token")
async def get_token_info(auth: Auth = Depends(verify_auth)) -> Auth:
    """Returns currently used oauth token details."""
    return auth


@api.post("/auth/token")
async def create_token(username: str = Form(...), password: str = Form(...)):
    """Creates a temporary oauth token."""
    if username == "Admin" and password == "HelloWorld":
        return Auth.from_payload(
            expire_at=datetime.utcnow() + timedelta(hours=24), user=username, token_id=1
        )
    raise HTTPException(status_code=404, detail="Invalid username or password")


@api.delete("/auth/token")
async def delete_token(auth: Auth = Depends(verify_auth)) -> None:
    """Deletes a registered oauth token."""
    del auth
