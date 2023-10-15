import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")


def get_postgres_uri() -> str:
    uri = os.getenv("POSTGRES_URI")
    return uri if ENVIRONMENT != "LOCAL" else uri.replace("desarrollo-postgres-1", "localhost")  # type: ignore


def get_redis_uri() -> tuple[str, int]:
    if ENVIRONMENT != "LOCAL":
        host = "redis"
    else:
        host = "localhost"
    return host, 6379
