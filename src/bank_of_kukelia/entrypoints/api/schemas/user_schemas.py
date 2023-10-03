from pydantic import BaseModel


class UserLoginForm(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    dni: int
    age: int
    email: str

class UserRead(BaseModel):
    name: str
    surname: str
    username: str
    dni: int
    age: int
    email: str

    class Config:
        from_attributes = True
