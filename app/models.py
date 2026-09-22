from pydantic import BaseModel
from datetime import date
class travelRequestModel(BaseModel):
    destination: str
    start_date: date
    end_date: date
    base_currency: str="INR"

class weatherResponseModel(BaseModel):
    date:str
    condition:str
    temperature_high: float
    temperature_low:float
    humidity:float
    rain_chance:float
