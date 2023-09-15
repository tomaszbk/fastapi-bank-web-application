from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt

from api.routes.bank_routes import router as bank_router
from loguru import logger
from jinja2 import TemplateNotFound


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(TemplateNotFound)
def template_not_found_exception(request: Request, exc: Exception):
    logger.error(f"template not found in {request.__dict__['scope']['route']}: {exc}")
    return JSONResponse(
        status_code=404,
        content={"message": "No such template"},
    )

@app.exception_handler(Exception)
async def exception_handler(request: Request, exc: Exception):
    logger.error(f'{exc}')
    return JSONResponse(
        status_code=500,
        content={"message": "Internal Server Error"},
    )

app.include_router(bank_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)