from pydantic import BaseModel


class TransactionCreate(BaseModel):
    amount: float
    destiny_username: str
    description: str | None = None

    class Config:
        from_attributes = True
