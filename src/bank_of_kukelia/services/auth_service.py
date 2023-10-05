from passlib.context import CryptContext
from jose import jwt, ExpiredSignatureError
from datetime import datetime, timedelta
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from sqlalchemy.orm import Session

from infrastructure.models import User
from infrastructure.engine import postgres_session_factory


class Auth():

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = 'e64b1149d445998de645136b902ebfc5e84411f58cfa1e1e0859258b514e4910'
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30

    def hash_password(self, password: str) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def authenticate_user(self, session: Session, username, password: str):
        # get user from database
        user = session.query(User).filter(User.username == username).one_or_none()
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt


    # Depends(oauth2_scheme): look in the request for the Authorization header,
    # check if value is Bearer plus some token, and returns the token as str
    # Otherwise, 401 status code error (UNAUTHORIZED)
    async def get_current_user_from_header(self, token: Annotated[str, Depends(oauth2_scheme)],):
        return await self.get_current_active_user(token)

    async def get_current_user_from_url(self, token: str):
        return await self.get_current_active_user(token)

    async def get_current_active_user(self, token: str, session = postgres_session_factory.get_session()):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
        except ExpiredSignatureError as ex:
            raise ExpiredSignatureError('Signature has expired') from ex
        username = payload.get("sub")
        user = session.query(User).filter(User.username == username).one_or_none()
        if user is None:
            raise Exception('User not found')
        return user

auth: Auth = Auth()
