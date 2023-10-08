from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger

from entrypoints.api.schemas.user_schemas import UserRead

from services.auth_service import auth
from services.transaction_service import create_transaction
from services.user_service import get_by_username as get_user_by_username

from infrastructure.engine import postgres_session_factory
from infrastructure.models import User

templates = Jinja2Templates(directory="entrypoints/api/templates")

router = APIRouter()


@router.get("")
async def dashboard_view(request: Request, user: User = Depends(auth.get_current_user_from_url)):
    """Template includes chart of user's balance over time,
    and a table of user's recent transactions."""
    transactions = user.bank_account.origin_transactions + user.bank_account.destiny_transactions
    transactions.sort(key=lambda transaction: transaction.transaction_date, reverse=True)
    transactions_len = len(transactions)
    return templates.TemplateResponse("dashboard.html", {"request": request,
                                                        "user": user,
                                                        "transactions": transactions,
                                                        "transactions_len": transactions_len})


@router.get("/profile")
def profile_view(request: Request, user: UserRead = Depends(auth.get_current_user_from_url)):
    """Template shows User data."""
    return templates.TemplateResponse("profile.html", {"request": request, "user": user})


@router.get("/transaction")
def transaction_view(request: Request, user: UserRead = Depends(auth.get_current_user_from_url)):
    """Template allows to create a new transaction."""
    return templates.TemplateResponse("transaction.html", {"request": request, "user": user})


@router.post("/transaction")
def transaction(request: Request, amount: float, destiny_username: str,
                 user = Depends(auth.get_current_user_from_header),
                 session = Depends(postgres_session_factory.get_session)):
    """Creates a new transaction."""
    destiny_user = get_user_by_username(session, destiny_username)
    if destiny_username is None:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user found with provided username"
                )
    create_transaction(session, user, amount, destiny_user) #type: ignore
