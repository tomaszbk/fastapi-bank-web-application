db = {}
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger
from api.schemas.auth_schemas import Token
from api.schemas.user_schemas import User
from libs.security import security
from fastapi.responses import JSONResponse
from typing import Annotated
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm 


templates = Jinja2Templates(directory="static/templates")

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

@router.post("/register")
def register(form_data : User):
    #TODO get user from real db
    logger.info('starting user registration')
    if db.get(form_data.username) is not None:
        logger.warning('User with this email already exist')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
            )
    user = {
        'email': form_data.email,
        'hashed_password': security.get_hashed_password(form_data.password)
    }
    db[form_data.username] = user # TODO saving user to real database
    logger.info(f'new user {form_data.username} created')
    return JSONResponse(content={"message": "Registration successful"})

@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = security.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    #TODO access user attr
    access_token = security.create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires
                    )
    return {"access_token": access_token, "token_type": "bearer"}