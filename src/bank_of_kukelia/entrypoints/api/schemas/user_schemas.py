from pydantic import BaseModel


class UserLoginForm(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    dni: int
    age: int
    email: str
