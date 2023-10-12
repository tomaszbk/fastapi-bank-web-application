from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from loguru import logger


templates = Jinja2Templates(directory="api/templates")

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/not_found")
def not_found_view(request: Request):
    logger.info("returning 404 page")
    return templates.TemplateResponse("404_not_found.html", {"request": request})


@router.get("/about")
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


@router.get("/contact")
async def contact(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})


@router.get("/login")
async def login_view(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.get("/register")
async def register_view(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.get("/logout")
async def logout_view(request: Request):
    return templates.TemplateResponse("logout.html", {"request": request})
