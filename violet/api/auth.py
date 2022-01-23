from .app import api
from fastapi import Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials


security = HTTPBasic()


@api.get("/auth/token")
async def basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username in ["Admin"]:
        if credentials.password == "123":
            return "a-refresh-token"


@api.get("/auth/token/refresh")
async def refresh_token(violet_token: str = Header()):
    pass


@api.get("/auth/info")
async def token_details(violet_token: str = Header()):
    pass
