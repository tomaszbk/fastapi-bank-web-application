from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float
    destiny_cbu: str
    motive: str | None = None
