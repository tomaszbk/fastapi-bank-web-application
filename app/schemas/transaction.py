from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    origin_cbu: str
    amount: float
    destiny_cbu: str
    motive: str | None = None
    number: str | None = None
