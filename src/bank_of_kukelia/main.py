from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from loguru import logger
from jinja2 import TemplateNotFound
from entrypoints.api.routes.home_routes import router as home_router
from entrypoints.api.routes.auth_routes import router as security_router
# from api.routes.operation_routes import router as operation_router


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

app.include_router(home_router)
app.include_router(security_router, prefix='/auth')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
