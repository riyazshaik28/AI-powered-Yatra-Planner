from datetime import date
import os

import httpx
from dotenv import load_dotenv
from ..models import weatherResponseModel
from .cache import get_cache, set_cache

load_dotenv()

WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")

async def fetch_weather(
    destination: str,
    start_date: date,
    end_date: date,
) -> list[weatherResponseModel]:
    cache_key = f"{destination}_{start_date}_{end_date}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data


    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.weatherapi.com/v1/forecast.json",
            params={
                "key": WEATHERAPI_API_KEY,
                "q": destination,
                "dt": start_date.isoformat(),
            },
        )

        response.raise_for_status()
        data = response.json()

        forecasts = []

        for day in data["forecast"]["forecastday"]:
            forecast = weatherResponseModel(
                date=day["date"],
                condition=day["day"]["condition"]["text"],
                temperature_high=day["day"]["maxtemp_c"],
                temperature_low=day["day"]["mintemp_c"],
                humidity=day["day"]["avghumidity"],
                rain_chance=day["day"]["daily_chance_of_rain"],
            )
            forecasts.append(forecast)
        set_cache(cache_key, forecasts, ttl=3600)  # Cache for 1 hour
        return forecasts