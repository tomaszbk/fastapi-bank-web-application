from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from loguru import logger
from typing import Annotated
from datetime import timedelta

from entrypoints.api.schemas.user_schemas import UserLoginForm

from services.auth_service import auth
from services.user_service import user_already_exists, create_user
from entrypoints.api.schemas.auth_schemas import Token

from infrastructure.engine import postgres_session_factory



router = APIRouter()

credentials_exception = HTTPException(
                            status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"},
                        )

@router.post("/register")
async def register(form_data : UserLoginForm,
                   session = postgres_session_factory.get_session()):
    logger.info('starting user registration')

    if user_already_exists(session, form_data.username):
        logger.warning('User with this email already exist')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
            )
    user = create_user(session, form_data)

    session.commit()
    logger.info(f'new user {user.username} created')
    return JSONResponse(content={"message": "Registration successful"})


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session = Depends(postgres_session_factory.get_session)
    ):
    try:
        user = auth.authenticate_user(session, form_data.username, form_data.password)
    except Exception as ex:
        logger.error(f'Error authenticating user: {ex}')
        raise credentials_exception from ex
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires
                    )
    return {"access_token": access_token, "token_type": "bearer"}
