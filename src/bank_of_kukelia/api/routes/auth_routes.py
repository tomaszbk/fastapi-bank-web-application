from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from loguru import logger
from api.schemas.user_schemas import User
from bank_of_kukelia.domain.auth import auth
from fastapi import Form
from typing import Annotated
from domain import user_repository
from api.schemas.auth_schemas import Token
from datetime import timedelta
from services.user_service import user_already_exists
from

router = APIRouter()

@router.post("/register")
def register(form_data : User):
    #TODO get user from real db
    logger.info('starting user registration')

    # if db.get(form_data.username) is not None:
    if user_already_exists(form_data.username):
        logger.warning('User with this email already exist')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
            )
    user = {
        'email': form_data.email,
        'hashed_password': auth.get_hashed_password(form_data.password)
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
