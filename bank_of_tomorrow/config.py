import os
from dotenv import load_dotenv

load_dotenv()

LOCAL = True


def get_postgres_uri() -> str:
    uri = os.getenv("POSTGRES_URI")
    return uri if not LOCAL else uri.replace("desarrollo-postgres-1", "localhost")  # type: ignore
