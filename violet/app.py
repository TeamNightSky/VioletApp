from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from violet.api import api
from violet.frontend import frontend


app = FastAPI()
app.mount("/static", StaticFiles(directory="violet/static"))
app.mount("/api", api)
app.mount("/", frontend)
