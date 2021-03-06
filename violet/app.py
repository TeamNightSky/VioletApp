"""Mounts all apps for full-stack app."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from violet.api import api
from violet.frontend import frontend

app = FastAPI()
app.mount("/assets", StaticFiles(directory="violet/static"))
app.include_router(api, prefix="/api")
app.mount("/", frontend)
