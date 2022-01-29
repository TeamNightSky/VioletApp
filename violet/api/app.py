"""Initializes api sub-mounted app"""
from fastapi import APIRouter

from .auth import auth_router
from .discussions import dis
from .projects import proj_router

api = APIRouter()
api.include_router(auth_router, prefix="/auth")
api.include_router(proj_router, prefix="/projects")
api.include_router(dis, prefix="/discussions")
