from datetime import datetime, timedelta

import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.infrastructure.external import get_jwt_from_code
from app.infrastructure.models import User


class Auth:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = "e64b1149d445998de645136b902ebfc5e84411f58cfa1e1e0859258b514e4910"
        self.ALGORITHM = "HS256"
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
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    async def get_current_active_user(self, session: Session, token: str) -> User:
        payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

        username = payload.get("sub")
        user = session.query(User).filter(User.username == username).one_or_none()
        if user is None:
            raise Exception("User not found")
        return user

    def handle_external_login(self, code: str) -> tuple[str, dict]:
        token = get_jwt_from_code(code)
        if not token:
            raise Exception("Error getting token from Renaper")

        with open("key.pem", "rb") as f:
            public_key = f.read()
        data = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            options={
                "verify_exp": False,  # Skipping expiration date check
                "verify_aud": False,
            },
        )
        return token, data


auth: Auth = Auth()
