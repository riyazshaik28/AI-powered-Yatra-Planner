from datetime import date
import os
import httpx


from ..models import  weatherResponseModel

from dotenv import load_dotenv
import os

load_dotenv()

WEATHERAPI_API_KEY = os.getenv("WEATHERAPI_API_KEY")

print("WEATHERAPI_API_KEY:", WEATHERAPI_API_KEY)

async def fetch_weather(
    destination: str,
    start_date: date,
    end_date: date,
) -> list[weatherResponseModel]:

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

        return forecasts