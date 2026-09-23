from datetime import datetime, timedelta
import os
import httpx
from dotenv import load_dotenv
from ..services.cache import get_cache, set_cache
load_dotenv()
EXCHANGERATE_API_KEY = os.getenv("EXCHANGERATE_API_KEY")

async def fetch_currency_rates(base_currency: str) -> dict:
    """
    Fetch currency exchange rates for a given base currency.
    """
    cache_key = f"currency_rates_{base_currency}"
    cached_data = get_cache(cache_key)
    if cached_data:
        return cached_data

    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/latest/{base_currency}"
        )
        response.raise_for_status()
        data = response.json()

        rates=data.get("conversion_rates", {})
        set_cache(cache_key, rates, ttl=3600)  # Cache for 1 hour
        return rates