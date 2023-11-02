from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import redis
import requests
import json

# port 8000
app = FastAPI()
redis_client = redis.Redis(host="localhost", port=6379)


@app.get("/", response_class=HTMLResponse)
async def index():
    if redis_client.exists("weather"):
        weather = redis_client.get("weather").decode("utf-8")
    else:
        response = requests.get("http://localhost:5000/get_weather")
        response.raise_for_status()
        weather = json.loads(response.text)
        redis_client.set("weather", weather)
    return f"""
        <html>
            <head><title>Weather</title></head>
            <body>
                <h1>Weather is {weather}</h1>
            </body>
        </html>"""


@app.post("/validate_user/{username}")
async def validate_user(username: str):
    if redis_client.exists(f"user:{username}", "validated"):
        if redis_client.hget(f"user:{username}", "validated") is True:
            return "user is validated"
        return "user not validated"
    else:
        response = requests.get(f"http://localhost:5000/validate_user/{username}")
        response.raise_for_status()
        state = response.text
        redis_client.hset(f"user:{username}", "validated", state)
        redis_client.expire(f"user:{username}", 60)
        if state == "true":
            return "user is validated"
        return "user not validated"
