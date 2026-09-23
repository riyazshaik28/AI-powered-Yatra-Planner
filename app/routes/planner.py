import asyncio

from fastapi import APIRouter, HTTPException

from ..models import travelRequestModel
from ..services.weather import fetch_weather
from ..services.places import fetch_places
from ..models import placeModel
from ..services.currency import fetch_currency_rates

router = APIRouter(
    prefix="/plan",
    tags=["travel_plan"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def create_travel_plan(
    travel_request: travelRequestModel,
):
    """
    Create a new travel plan by aggregating data from the user and providing a travel plan.
    """

    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(status_code=400, detail="Start date must be before end date.")

    trip_days = (travel_request.end_date - travel_request.start_date).days
    if trip_days < 1:
        raise HTTPException(status_code=400, detail="trip duration must be at least 1 day.")

    if trip_days > 30:
        raise HTTPException(
            status_code=400, detail="trip duration must not exceed 30 days."
        )
    # Logic to create a new travel plan goes here
    #make them to parallel to reduce the response time
    weather_data,places_data,currency_rates= await asyncio.gather(
        fetch_weather(
            destination=travel_request.destination,
            start_date=travel_request.start_date,
            end_date=travel_request.end_date,
        ),
        fetch_places(destination=travel_request.destination),
        fetch_currency_rates(base_currency=travel_request.base_currency)
    )
    
    return {
        "message": "Travel plan created successfully.",
        "weather_data": weather_data,
        "places_data": places_data,
        "currency_rates": currency_rates
    }
    
