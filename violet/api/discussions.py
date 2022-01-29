"""Registers discussion CRUD endpoints."""
from fastapi import APIRouter

# from violet.db import app_db
from violet.models import Auth, Discussion

dis = APIRouter()


@dis.get("/{snowflake}")
async def get_discussion(snowflake: int, auth: Auth):
    """Gets a discussion."""
    del snowflake
    del auth


@dis.put("/{snowflake}")
async def put_discussion(snowflake: int, discussion: Discussion, auth: Auth):
    """Creates a discussion."""
    del snowflake
    del discussion
    del auth


@dis.post("/{snowflake}")
async def post_discussion(snowflake: int, discussion: Discussion, auth: Auth):
    """Updates a discussion."""
    del snowflake
    del discussion
    del auth


@dis.delete("/{snowflake}")
async def delete_discussion(snowflake: int, auth: Auth):
    """Deletes a discussion model."""
    del snowflake
    del auth
