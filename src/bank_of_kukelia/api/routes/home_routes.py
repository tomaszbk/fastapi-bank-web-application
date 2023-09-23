db = {}
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger

from api.schemas.user_schemas import User
from libs.security import security

from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm 


templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/{route}")
def route_by_param(route: str, request: Request):
    return templates.TemplateResponse(f"{route}.html", {"request": request})


@router.get('/{route}/x')
def restricted(route: str, request: Request, current_user = Depends(security.get_current_user)):
    return templates.TemplateResponse("restricted.html", {"request": request})
