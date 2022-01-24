"""Sub-Mounted App for frontend page templates."""
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

frontend = FastAPI()


templates = Jinja2Templates(directory="violet/templates")


@frontend.get("/", response_class=HTMLResponse)
async def view_index(request: Request):
    """Returns the home page template"""
    return templates.TemplateResponse("index.html", {"request": request})


@frontend.get("/register", response_class=HTMLResponse)
async def view_register(request: Request):
    """Returns the registration page template"""
    return templates.TemplateResponse("register.html", {"request": request})


@frontend.post("/register", response_class=HTMLResponse)
async def register_user(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    email: str = Form(...),
):
    """Registers a user in the db and returns a redirect template."""
    print(username, password, email)
    return templates.TemplateResponse("register_success.html", {"request": request})


@frontend.get("/about", response_class=HTMLResponse)
async def view_about(request: Request):
    """Returns the about page template"""
    return templates.TemplateResponse("about.html", {"request": request})


@frontend.get("/conversations", response_class=HTMLResponse)
async def view_conversations(request: Request):
    """Returns conversations page template"""
    return templates.TemplateResponse("conversations.html", {"request": request})


@frontend.get("/conversation", response_class=HTMLResponse)
async def view_conversation(request: Request):
    """Returns a conversation page template"""
    return templates.TemplateResponse("conversation.html", {"request": request})


@frontend.get("/login", response_class=HTMLResponse)
async def view_login(request: Request):
    """Returns the login page template."""
    return templates.TemplateResponse("login.html", {"request": request})
