from fastapi import FastAPI
from datetime import datetime

app = FastAPI()


@app.get("/zodiac/{date}")
async def get_zodiac_sign(date: str):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        month = date_obj.month
        day = date_obj.day
        if month == 12:
            astro_sign = "Sagittarius" if (day < 22) else "Capricorn"
        elif month == 1:
            astro_sign = "Capricorn" if (day < 20) else "Aquarius"
        elif month == 2:
            astro_sign = "Aquarius" if (day < 19) else "Pisces"
        elif month == 3:
            astro_sign = "Pisces" if (day < 21) else "Aries"
        elif month == 4:
            astro_sign = "Aries" if (day < 20) else "Taurus"
        elif month == 5:
            astro_sign = "Taurus" if (day < 21) else "Gemini"
        elif month == 6:
            astro_sign = "Gemini" if (day < 21) else "Cancer"
        elif month == 7:
            astro_sign = "Cancer" if (day < 23) else "Leo"
        elif month == 8:
            astro_sign = "Leo" if (day < 23) else "Virgo"
        elif month == 9:
            astro_sign = "Virgo" if (day < 23) else "Libra"
        elif month == 10:
            astro_sign = "Libra" if (day < 23) else "Scorpio"
        elif month == 11:
            astro_sign = "Scorpio" if (day < 22) else "Sagittarius"
        return astro_sign
    except ValueError:
        return {"error": "Invalid date format. Please use YYYY-MM-DD."}
