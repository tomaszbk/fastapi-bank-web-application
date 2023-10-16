import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")


def get_postgres_uri() -> str:
    uri = os.getenv("POSTGRES_URI")
    if not uri:
        raise Exception("POSTGRES_URI not set")
    return uri


def get_redis_uri() -> tuple[str, int]:
    if ENVIRONMENT != "LOCAL":
        host = "redis"
    else:
        host = "localhost"
    return host, 6379
