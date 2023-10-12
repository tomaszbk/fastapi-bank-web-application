from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates

from api.routes.auth_routes import (
    get_current_user_from_header,
    get_current_user_from_url,
)
from api.schemas.user_schemas import UserRead
from api.schemas.transaction_schemas import TransactionCreate

from services.transaction_service import create_transaction
from services.user_service import get_by_username as get_user_by_username

from infrastructure.engine import postgres_session_factory
from infrastructure.models import User

templates = Jinja2Templates(directory="entrypoints/api/templates")

router = APIRouter()


@router.get("")
async def dashboard_view(request: Request, user: User = Depends(get_current_user_from_url)):
    """Template includes chart of user's balance over time,
    and a table of user's recent transactions."""
    transactions = user.bank_account.origin_transactions + user.bank_account.destiny_transactions
    transactions.sort(key=lambda transaction: transaction.transaction_date, reverse=True)

    return templates.TemplateResponse(
        "dashboard.html", {"request": request, "user": user, "transactions": transactions}
    )


@router.get("/profile")
async def profile_view(request: Request, user: UserRead = Depends(get_current_user_from_url)):
    """Template shows User data."""
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/transaction")
async def transaction_view(request: Request, user: UserRead = Depends(get_current_user_from_url)):
    """Template allows to create a new transaction."""
    return templates.TemplateResponse("transaction.html", {"request": request, "user": user})


@router.post("/transaction")
async def transaction(
    transaction: TransactionCreate,
    session=Depends(postgres_session_factory.get_session),
    user=Depends(get_current_user_from_header),
):
    """Creates a new transaction."""
    destiny_user = get_user_by_username(session, transaction.destiny_username)
    if destiny_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No user found with provided username"
        )
    create_transaction(session, user, transaction.amount, destiny_user)
    return {"message": "Transaction created successfully"}
