from pydantic import BaseModel, ConfigDict, field_validator


class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    password: str
    cuil: int
    age: int
    email: str

    @field_validator("age")
    def age_must_be_greater_than_18(cls, age):
        if age < 18 or age > 100:
            raise ValueError("Age must be greater than 18 or less than 100")
        return age

    @field_validator("cuil")
    def cuil_must_be_valid(cls, cuil):
        if len(str(cuil)) != 11:
            raise ValueError("cuil must be 8 digits long")
        return cuil

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
