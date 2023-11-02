from fastapi import FastAPI
import asyncio

# port 5000
app = FastAPI()


@app.get("/get_weather")
async def get_zodiac_sign():
    await asyncio.sleep(5)
    return "16°C"


@app.get("/validate_user/{username}")
async def validate_user(username: str):
    await asyncio.sleep(5)
    return True
