from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from loguru import logger
from api.schemas.user_schemas import UserLoginForm
from services.auth_service import auth
from typing import Annotated
from api.schemas.auth_schemas import Token
from datetime import timedelta

from adapters.db.orm import get_session
from adapters.repositories.user_repo import UserSqlAlchemyRepo
from services.user_service import user_already_exists, create_user



router = APIRouter()

@router.post("/register")
def register(form_data : UserLoginForm, session = Depends(get_session)):
    logger.info('starting user registration')
    user_repo = UserSqlAlchemyRepo(session)

    if user_already_exists(user_repo, form_data.username):
        logger.warning('User with this email already exist')
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
            )
    user = create_user(user_repo, form_data)

    session.commit()
    logger.info(f'new user {user.username} created')
    return JSONResponse(content={"message": "Registration successful"})


@router.post("/login", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session = Depends(get_session)
    ):
    user_repo = UserSqlAlchemyRepo(session)
    user = auth.authenticate_user(user_repo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    #TODO access user attr
    access_token = auth.create_access_token(
                    data={"sub": user.username}, expires_delta=access_token_expires
                    )
    return {"access_token": access_token, "token_type": "bearer"}
