import time
import requests
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from loguru import logger


templates = Jinja2Templates(directory="static/templates")

router = APIRouter()


@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/{route}")
def route_by_param(route: str, request: Request):
    return templates.TemplateResponse(f"{route}.html", {"request": request})

@router.post("/login")
def login(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/signup")
def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})