"""Module for interacting with Supabase DB"""
import os
import typing as t

from fastapi import HTTPException
from postgrest_py import AsyncPostgrestClient  # type: ignore[import]

from violet.models import Discussion, Project, User


class VioletDB(AsyncPostgrestClient):
    """A customized class to intereact with our Supabase Postgrest Servers"""

    key: t.Optional[str] = os.getenv("SUPA_KEY")
    url: t.Optional[str] = os.getenv("SUPA_URL")

    def __init__(self):
        super().__init__(
            self.url + "rest/v1",
            headers={"Authorization": f"Bearer {self.key}", "apiKey": self.key},
        )

    async def get_user(self, payload: dict, select_args: t.Tuple[str] = ("*",)) -> User:
        """Get user by snowflake"""
        user = (
            await self.from_("userdata")
            .select(*select_args)
            .eq("snowflake", payload["snowflake"])
            .execute()
        )
        if not user[0]:
            user = await self.create_user(payload)
        userobj = User(**{k: v for k, v in user[0][0].items() if v is not None})
        return userobj

    async def create_user(self, payload: dict):
        """Creates a user in the db."""
        query = self.from_("userdata").insert(
            {
                k: v
                for k, v in {**payload["user_metadata"], **payload}.items()
                if k in User.__fields__
            }
        )
        return await query.execute()

    async def get_discussion(self, snowflake: int) -> Discussion:
        """Get discussion from snowflake."""
        query = self.from_("discussion").select("*").eq("snowflake", snowflake)
        discussion = await query.execute()
        if isinstance(discussion[0], dict) and not discussion[0].get(
            "message", True
        ):  # Not sure how to properly check if it was not found
            raise HTTPException(status_code=403, detail="Missing permissions")
        return Discussion(**discussion[0][0])

    async def get_project(self, snowflake: int) -> Project:
        """Get project from snoflake."""
        query = self.from_("projects").select("*").eq("snowflake", snowflake)
        proj = await query.execute()

        if isinstance(proj[0], dict) and not proj[0].get("message", True):
            raise HTTPException(status_code=403, detail="Missing permissions")

        return Project(**{k: v for k, v in proj[0][0].items() if v is not None})

    async def create_project(self, proj: Project) -> Project:
        """Create project"""
        query = self.from_("projects").insert(proj.dict())
        data = await query.execute()
        return Project(**data)


app_db = VioletDB()
