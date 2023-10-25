from fastapi import FastAPI
import redis
import requests


app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/zodiac_sign/{date}")
async def get_from_redis(date: int):
    if redis_client.exists(date):
        return {"zodiac_sign": redis_client.hget(date)}
    zodiac_sign = requests.get(f"http://localhost:5000/zodiac/{date}")
    redis_client.hset(date, zodiac_sign)
    return {"message": f"Your zodiac sign is {zodiac_sign}"}
