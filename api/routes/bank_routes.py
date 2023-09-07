from fastapi import APIRouter, Request

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="api/static/templates")

router = APIRouter()

@router.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/register")
def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(request: Request):
    return templates.TemplateResponse("questionnaire.html", {"request": request})
