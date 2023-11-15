import os
from dotenv import load_dotenv
from fastapi.templating import Jinja2Templates

load_dotenv()

LOCAL = True

templates = Jinja2Templates(directory="bank_of_tomorrow/api/templates")


def get_postgres_uri() -> str:
    uri = os.getenv("POSTGRES_URI")
    return uri if not LOCAL else uri.replace("desarrollo-postgres-1", "localhost")  # type: ignore
