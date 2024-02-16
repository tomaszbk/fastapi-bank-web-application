from pydantic import BaseModel, ConfigDict, field_validator


class TransactionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    origin_cbu: str
    amount: float
    destiny_cbu: str
    motive: str | None = None
    number: str | None = None

    @field_validator("cbu")
    def cbu_len_must_be_valid(cls, cuit):
        if len(str(cuit)) != 22:
            raise ValueError("cbu must be 22 digits long")
        return cuit


class TransactionCreateFront(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    amount: float
    destiny_cbu: str
    motive: str | None = None
    number: str | None = None
