from pydantic import BaseModel, field_validator


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    dni: int
    age: int
    email: str

    @field_validator("age")
    def age_must_be_greater_than_18(cls, age):
        if age < 18 or age > 100:
            raise ValueError("Age must be greater than 18 or less than 100")
        return age

    @field_validator("dni")
    def dni_must_be_valid(cls, dni):
        if len(str(dni)) != 8:
            raise ValueError("DNI must be 8 digits long")
        return dni

    @field_validator("email")
    def email_must_be_valid(cls, email):
        if "@" not in email:
            raise ValueError("Email must be valid")
        return email


class UserRead(BaseModel):
    name: str
    surname: str
    username: str
    dni: int
    age: int
    email: str

    class Config:
        from_attributes = True
