from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from api.routes.bank_routes import router as bank_router
from loguru import logger

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

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