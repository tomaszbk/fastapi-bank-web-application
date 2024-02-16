from pydantic import BaseModel, ConfigDict, field_validator


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    cuit: int
    age: int
    email: str

    @field_validator("age")
    def age_must_be_greater_than_18(cls, age):
        if age < 18 or age > 100:
            raise ValueError("Age must be greater than 18 or less than 100")
        return age

    @field_validator("cuit")
    def cuit_must_be_valid(cls, cuit):
        if len(str(cuit)) != 11:
            raise ValueError("cuit must be 8 digits long")
        return cuit

    @field_validator("email")
    def email_must_be_valid(cls, email):
        if "@" not in email:
            raise ValueError("Email must be valid")
        return email


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    surname: str
    username: str
    dni: int
    age: int
    email: str
