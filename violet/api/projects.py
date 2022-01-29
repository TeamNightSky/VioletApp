"""Projects API"""
from fastapi import APIRouter, HTTPException

from violet.db import app_db
from violet.models import Auth, Project

proj_router = APIRouter()


@proj_router.get("/{snowflake}")
async def get_project(snowflake: int, auth: Auth = None) -> Project:
    """Gets a project model from the database."""
    project = await app_db.get_project(snowflake)
    if project.public:
        return project
    if auth is not None:
        payload = auth.decode()
        if payload["snowflake"] in project.collaborators:
            return project
    raise HTTPException(status_code=401)


@proj_router.post("/create")
async def create_project(auth: Auth, proj: Project) -> Project:
    """Creates a project model in the database."""
    # Auth is decoded in auth.snowflake
    proj.owners = list({*proj.owners, auth.snowflake})  # clever
    proj.collaborators = list({*proj.owners, *proj.collaborators})
    project = await app_db.create_project(proj)
    return project
