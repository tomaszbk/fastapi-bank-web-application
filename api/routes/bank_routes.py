import time
import requests
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from loguru import logger
from api.models.user_models import SignupModel
from libs.security import security
from fastapi import Form

db = {}
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
    return templates.TemplateResponse("index.html", {"request": request})

@router.post("/signup")
def signup(request: Request, username = Form(...), password = Form(...), email = Form(...)):
    user = db.get(username, None) #TODO get user
    if user is not None:
        #     raise HTTPException(
        #     status_code=status.HTTP_400_BAD_REQUEST,
        #     detail="User with this email already exist"
        # )
        return {'response': 'User with this email already exist'}
    user = {
        'email': email,
        'password': security.get_password_hash(password)
    }
    db[username] = user
    # TODO saving user to database
    return templates.TemplateResponse("login.html", {"request": request})