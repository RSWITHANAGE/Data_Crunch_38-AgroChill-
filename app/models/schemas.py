from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# Weather Data Models
class WeatherDataContent(BaseModel):
    temp: Optional[float] = None
    rainfall: Optional[float] = None
    humidity: Optional[float] = None

class WeatherDataRequest(BaseModel):
    date: str
    region: str
    weatherData: WeatherDataContent

class WeatherEntry(BaseModel):
    date: str
    region: str
    temperature: Optional[float] = None
    rainfall: Optional[float] = None
    humidity: Optional[float] = None
    crop_yield_impact_score: Optional[float] = None

# Price Data Models
class PriceDataContent(BaseModel):
    price: float

class PriceDataRequest(BaseModel):
    date: str
    crop: str
    region: str
    priceData: PriceDataContent

class PriceEntry(BaseModel):
    date: str
    region: str
    commodity: str
    price: float
    type: str

# Prediction Models
class PredictionRequest(BaseModel):
    crop: str
    region: str

class PredictionEntry(BaseModel):
    prediction_index: int
    date: str
    price: float

class PredictionResponse(BaseModel):
    crop: str
    region: str
    predictions: List[PredictionEntry]