from passlib.context import CryptContext

class Security():
    def __init__(self) -> None:
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.SECRET_KEY = 'e64b1149d445998de645136b902ebfc5e84411f58cfa1e1e0859258b514e4910'
        self.ALGORITHM = 'HS256'
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30
        
    def get_password_hash(self, password :str) -> str:
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password :str, hashed_password :str) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def authenticate_user(self, user, password :str):
        if not user:
            return False
        if not self.verify_password(password, user.hashed_password):
            return False
        return user
    
security : Security = Security()