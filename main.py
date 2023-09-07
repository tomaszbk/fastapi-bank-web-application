from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.routes.bank_routes import router as bank_router


app = FastAPI()
app.mount("/static", StaticFiles(directory="api/static"), name="static")
app.include_router(bank_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)