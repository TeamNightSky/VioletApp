"""Module classes defined for data validation and stucture using Pydantic."""
import os
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import jwt  # type: ignore[import]
from fastapi import HTTPException
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class Asset(BaseModel):
    """Discussion or User Asset JSON Model"""

    base64: str
    mimetype: str
    snowflake: int


class User(BaseModel):
    """User JSON Model"""

    snowflake: int
    date_joined: datetime = datetime.utcnow()
    name: Optional[str] = None
    is_superuser: bool = False
    is_staff: bool = False
    image: Optional[Asset] = None
    projects: List[int] = []


class Entry(BaseModel):
    """Discussion Entry JSON Model"""

    user: int
    snowflake: int
    content: str
    timestamp: datetime
    assets: List[Asset] = []
    refs: Dict[int, Tuple[str, int, str]] = {}
    # Used for referencing stuff (code snippets, sections of pages, issues, etc.)
    # {ref id: (type of ref, id of referred object, selector)}
    # Selector may be line and col numbers, or css selectors, or other


class Discussion(BaseModel):
    """Discussion JSON Model"""

    name: str
    snowflake: int
    tags: List[str] = []
    entries: List[Entry] = []


class ProjectBase(BaseModel):
    """Project JSON Model for client to send."""

    name: str
    public: bool = True
    tags: List[str] = []
    icon: Optional[str] = None
    owners: List[int] = []  # Snowflakes
    collaborators: List[int] = []  # Snowflakes
    assets: List[int] = []  # Snowflakes


class Project(BaseModel):
    """Project JSON Model"""

    name: str
    snowflake: Optional[int] = None
    created_at: datetime = datetime.utcnow()
    public: bool = True
    tags: List[str] = []
    icon: Optional[str] = None
    owners: List[int] = []  # Snowflakes
    collaborators: List[int] = []  # Snowflakes
    assets: List[int] = []  # Snowflakes
    discussions: List[int] = []  # Snowflakes


def cached(method):
    """Caching function to save processing power when accessing JWT payload"""
    prev_token = None
    payload = None

    def decode(self, fail_response=None):
        nonlocal prev_token
        nonlocal payload
        if self.token != prev_token:
            prev_token = self.token
            payload = method(self, fail_response)
        return payload

    return decode


class Auth(BaseModel):
    """Authorization JSON model."""

    token: str

    # @cached
    def decode(self, fail_response=None) -> Dict[str, Any]:
        """Returns the payload of the token."""
        if (jwt_secret := os.getenv("JWT_SECRET")) is None:
            raise ValueError("Expected JWT_SECRET")
        try:
            return jwt.decode(  # pylint: disable=no-member
                self.token, jwt_secret, algorithms=["HS256"], audience=["authenticated"]
            )
        except jwt.PyJWTError as err:  # pylint: disable=no-member
            if fail_response:
                return fail_response
            raise HTTPException(status_code=401, detail=str(err)) from err

    @property
    def snowflake(self):
        """Returns the snowflake of the Auth object"""
        return uuid.UUID(self.decode()["sub"]).int >> 64

    @property
    def expire_at(self):
        """Returns the expire_at attribute from its payload."""
        return self.decode().get("exp")

    @staticmethod
    def from_payload(**payload) -> "Auth":
        """Creates an Auth model from JSON keyword arguments."""
        if (jwt_secret := os.getenv("JWT_SECRET")) is None:
            raise ValueError("Expected JWT_SECRET")
        token = jwt.encode(  # pylint: disable=no-member
            payload, jwt_secret, algorithm="HS256"
        )  # pylint: disable=no-member
        return Auth(token=token, payload=payload)


def snowflake() -> int:
    """Returns a universally unique 64-bit snowflake. 5.4e-20 chance of collision."""
    return uuid.uuid4().int >> 64  # Small enough so that int8 can hold it
