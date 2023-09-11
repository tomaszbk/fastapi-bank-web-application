from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from loguru import logger
import time
import requests
from jinja2 import TemplateNotFound

templates = Jinja2Templates(directory="static/templates")

router = APIRouter()

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.get("/contact")
def register(request: Request):
    return templates.TemplateResponse("contact.html", {"request": request})

@router.get("/{route}")
def route_by_param(route: str, request: Request):
    return templates.TemplateResponse(f"{route}.html", {"request": request})

