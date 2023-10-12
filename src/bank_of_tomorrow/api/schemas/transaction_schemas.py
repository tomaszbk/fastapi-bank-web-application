from pydantic import BaseModel, ConfigDict


class TransactionCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    amount: float
    destiny_username: str
    description: str | None = None
