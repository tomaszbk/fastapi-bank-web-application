import os
from dotenv import load_dotenv
import json
from fastapi.templating import Jinja2Templates

load_dotenv()

LOCAL = False

templates = Jinja2Templates(directory="app/api/templates")

with open("app/config.json") as f:
    config = json.loads(f.read())


def get_postgres_uri() -> str:
    uri = os.getenv("POSTGRES_URI")
    return uri if not LOCAL else uri.replace("desarrollo-postgres-1", "localhost")  # type: ignore
