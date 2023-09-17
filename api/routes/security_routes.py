import time
import requests
from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.templating import Jinja2Templates
from loguru import logger
from api.models.user_models import SignupModel
from libs.security import security
from fastapi import Form
from typing import Annotated