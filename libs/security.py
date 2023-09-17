from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status 
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm 
from typing import Annotated

db = {}
class Security():

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = 'e64b1149d445998de645136b902ebfc5e84411f58cfa1e1e0859258b514e4910'
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        
    def get_hashed_password(self, password :str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password :str, hashed_password :str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, username, password :str):
        # get user from database
        user = db.get(username, None)
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
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt
    
    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
            )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = db.get(username)
        if user is None:
            raise credentials_exception
        return user
    

    # async def get_current_active_user(self,
    #     current_user: Annotated[User, Depends(get_current_user)]
    # ):
    #     if current_user.disabled:
    #         raise HTTPException(status_code=400, detail="Inactive user")
    #     return current_user
    
security : Security = Security()