from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger

from services.auth_service import auth

from datetime import timedelta


templates = Jinja2Templates(directory="entrypoints/api/templates")

router = APIRouter()


@router.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/{route}")
async def route_by_param(route: str, request: Request):
    return templates.TemplateResponse(f"{route}.html", {"request": request})


@router.get('/{route}/x')
def restricted(route: str, request: Request, current_user= Depends(auth.get_current_user)):
    return templates.TemplateResponse("restricted.html", {"request": request})
