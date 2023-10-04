from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.requests import Request
from loguru import logger
from jinja2 import TemplateNotFound

from entrypoints.api.routes.home_routes import router as home_router
from entrypoints.api.routes.auth_routes import router as security_router
from entrypoints.api.routes.dashboard_routes import router as dashboard_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="entrypoints/api/static"), name="static")

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

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return RedirectResponse('/not_found')


app.include_router(home_router)
app.include_router(security_router, prefix='/auth')
app.include_router(dashboard_router, prefix='/dashboard')

# @app.middleware("http")
# async def redirect_on_not_found(request: Request, call_next):
#     response = await call_next(request)
#     if response.status_code == 404:
#         return RedirectResponse("https://fastapi.tiangolo.com")
#     else:
#         return response
