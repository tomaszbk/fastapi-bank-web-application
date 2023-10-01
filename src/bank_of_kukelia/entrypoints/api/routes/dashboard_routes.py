from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger

from services.auth_service import auth

from datetime import timedelta


templates = Jinja2Templates(directory="entrypoints/api/templates")

router = APIRouter()


@router.get("/")
def dashboard_view(request: Request, user=Depends(auth.get_current_user)):
    """Template includes chart of user's balance over time,
    and a table of user's recent transactions."""
    return templates.TemplateResponse("dashboard.html", {"request": request})
