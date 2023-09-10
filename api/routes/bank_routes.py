from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from loguru import logger
import time
import requests

templates = Jinja2Templates(directory="static/templates")

router = APIRouter()

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@router.post("/register")
def register(request: Request):
    return templates.TemplateResponse("questionnaire.html", {"request": request})
