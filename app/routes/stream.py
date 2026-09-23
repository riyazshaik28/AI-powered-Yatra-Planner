import json
from typing import Any, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from ..models import travelRequestModel
from ..services.currency import fetch_currency_rates
from ..services.places import fetch_places
from ..services.weather import fetch_weather

router = APIRouter(
    prefix="/stream",
    tags=["stream"],
    responses={404: {"description": "Not found"}},
)


def format_sse(data: dict[str, Any], event: Optional[str] = None) -> str:
    json_data = json.dumps(data, default=str, separators=(",", ":"))

    if event:
        return f"event: {event}\ndata: {json_data}\n\n"

    return f"data: {json_data}\n\n"


async def stream_generator(travel_request: travelRequestModel):
    try:
        yield format_sse(
            {"message": "Starting travel plan aggregation..."},
            event="start",
        )

        yield format_sse(
            {"message": "Fetching weather information..."},
            event="weather",
        )

        weather_data = await fetch_weather(
            destination=travel_request.destination,
            start_date=travel_request.start_date,
            end_date=travel_request.end_date,
        )

        yield format_sse(
            {
                "message": "Weather information fetched successfully",
                "data": [
                    item.model_dump() if hasattr(item, "model_dump") else item
                    for item in weather_data
                ],
            },
            event="weather_complete",
        )

        places_data = await fetch_places(
            destination=travel_request.destination
        )

        yield format_sse(
            {
                "message": "Places fetched successfully",
                "data": [
                    item.model_dump() if hasattr(item, "model_dump") else item
                    for item in places_data
                ],
            },
            event="places_complete",
        )

        currency_rates = await fetch_currency_rates(
            base_currency=travel_request.base_currency
        )

        yield format_sse(
            {
                "message": "Currency rates fetched successfully",
                "data": currency_rates,
            },
            event="currency_complete",
        )

        yield format_sse(
            {"message": "Travel plan generated successfully"},
            event="complete",
        )

    except Exception as exc:
        yield format_sse(
            {"error": str(exc)},
            event="error",
        )


@router.post("")
async def stream_travel_plan(
    travel_request: travelRequestModel,
):
    if travel_request.start_date > travel_request.end_date:
        raise HTTPException(
            status_code=400,
            detail="Start date must be before end date.",
        )

    trip_days = (
        travel_request.end_date - travel_request.start_date
    ).days

    if trip_days < 1:
        raise HTTPException(
            status_code=400,
            detail="Trip duration must be at least 1 day.",
        )

    if trip_days > 30:
        raise HTTPException(
            status_code=400,
            detail="Trip duration must not exceed 30 days.",
        )

    return StreamingResponse(
        stream_generator(travel_request),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        },
    )