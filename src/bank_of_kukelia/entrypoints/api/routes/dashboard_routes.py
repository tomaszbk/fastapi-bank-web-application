from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger

from services.auth_service import auth
from entrypoints.api.schemas.user_schemas import UserRead

from decorators import auth_exception_handler

templates = Jinja2Templates(directory="entrypoints/api/templates")

router = APIRouter()


@router.get("")
@auth_exception_handler
def dashboard_view(request: Request, user: UserRead = Depends(auth.get_current_user_from_url)):
    """Template includes chart of user's balance over time,
    and a table of user's recent transactions."""
    return templates.TemplateResponse("dashboard.html", {"request": request, "user": user})


@router.get("/profile")
@auth_exception_handler
def profile_view(request: Request, user: UserRead = Depends(auth.get_current_user_from_url)):
    """Template shows User data."""
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/transaction")
@auth_exception_handler
def transaction_view(request: Request, user: UserRead = Depends(auth.get_current_user_from_url)):
    """Template allows to create a new transaction."""
    return templates.TemplateResponse("transaction.html", {"request": request, "user": user})
