"""Module classes defined for data validation and stucture using Pydantic."""
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

import jwt  # type: ignore[import]
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Asset(BaseModel):
    """Discussion or User Asset JSON Model"""

    base64: str
    mimetype: str
    snowflake: int


class User(BaseModel):
    """User JSON Model"""

    name: str
    username: str
    snowflake: int
    image: Optional[Asset] = None


class Entry(BaseModel):
    """Discussion Entry JSON Model"""

    user: User
    snowflake: int
    content: str
    timestamp: datetime
    assets: List[Asset]


class Discussion(BaseModel):
    """Discussion JSON Model"""

    name: str
    snowflake: int
    tags: List[str] = []
    entries: List[Entry] = []


class Auth(BaseModel):
    """Authorization JSON model."""

    token: str
    payload: Dict[str, Any]

    def decode(self) -> bool:
        """Returns whether the token is valid, sets self.payload to the payload if valid."""
        try:
            self.payload = jwt.decode(  # pylint: disable=no-member
                self.token, os.getenv("JWT_SECRET"), algorithms=["HS256"]
            )
        except jwt.PyJWTError:  # pylint: disable=no-member
            return False
        return True

    @property
    def expire_at(self):
        """Returns the expire_at attribute from its payload."""
        return self.payload.get("expire_at")

    @staticmethod
    def from_payload(**payload) -> "Auth":
        """Creates an Auth model from JSON keyword arguments."""
        token = jwt.encode(  # pylint: disable=no-member
            payload, os.getenv("JWT_SECRET"), algorithms=["HS256"]
        )  # pylint: disable=no-member
        return Auth(token=token, payload=payload)


def snowflake() -> int:
    """Returns a universally unique snowflake aka a uuid."""
    return uuid.uuid4().int
