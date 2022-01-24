"""Registers discussion CRUD endpoints."""
from violet.api.app import api
from violet.models import Discussion


@api.get("/discussions/{snowflake}")
async def get_discussion(snowflake: int):
    """Gets a discussion."""
    del snowflake


@api.put("/discussions/{snowflake}")
async def put_discussion(snowflake: int, discussion: Discussion):
    """Creates a discussion."""
    del snowflake
    del discussion


@api.post("/discussions/{snowflake}")
async def post_discussion(snowflake: int, discussion: Discussion):
    """Updates a discussion."""
    del snowflake
    del discussion


@api.delete("/discussions/{snowflake}")
async def delete_discussion(snowflake: int):
    """Deletes a discussion model."""
    del snowflake
