from fastapi import APIRouter, Request
from loguru import logger

from app.config import templates
from app.infrastructure.engine import postgres_session_factory
from app.schemas.user import UserCreate
from app.services.auth import auth
from app.services.user import create_user

router = APIRouter()


@router.get("/")
async def index(request: Request, queryParametro: str | None = None):
    logger.info(queryParametro)
    code = queryParametro
    if code:
        jwt, data = await auth.handle_external_login(code)
        session = postgres_session_factory.get_session_no_yield()
        user_data = UserCreate(
            name=data["Nombre"],
            surname=data["Apellido"],
            email=data["Email"],
            cuil=data["Cuil"],
            username=data["Nombre"] + data["Apellido"],
            password="RENAPER",
            age=18,
        )
        create_user(session=session, form_data=user_data)
        session.close()
    else:
        jwt = None

    return templates.TemplateResponse("index.html", {"request": request, "jwt": jwt})


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
