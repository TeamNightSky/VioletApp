from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class Asset(BaseModel):
    base64: str
    mimetype: str
    snowflake: int


class User(BaseModel):
    name: str
    snowflake: int
    image: Optional[Asset] = None


class Entry(BaseModel):
    user: User
    snowflake: int
    content: str
    timestamp: datetime
    assets: List[Asset]


class Discussion(BaseModel):
    name: str
    snowflake: int
    tags: List[str] = []
    entries: List[Entry] = []
