from pydantic import BaseModel, field_validator


class User(BaseModel):
    email : str
    username: str
    password: str

