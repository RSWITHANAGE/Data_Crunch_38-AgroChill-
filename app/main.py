from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
import pandas as pd
from datetime import datetime, timedelta

from app.models.schemas import (
    PredictionRequest, 
    PredictionResponse, 
    WeatherDataRequest,
    PriceDataRequest,
    WeatherEntry,
    PredictionEntry
)
from app.models.predictor import AgroChillPredictor
from app.data.storage import DataStorage

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AgroChill Price Forecasting API",
    description="API for the AgroChill system that predicts crop prices for Magnus Greenvale's freezer gambit",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize data storage and predictor
storage = DataStorage()
predictor = AgroChillPredictor(model_path="models/agrochill_model.pkl")

@app.on_event("startup")
async def startup_event():
    """Initialize data and model on startup"""
    logger.info("Loading data and initializing model...")
    # Load existing data if available
    storage.load_data()
    # Initialize predictor with data
    predictor.initialize(storage.get_weather_data(), storage.get_price_data())
    logger.info("Initialization complete")

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to AgroChill Price Forecasting API", "status": "operational"}

@app.post("/api/predict", response_model=PredictionResponse)
def predict_prices(request: PredictionRequest):
    """Predict prices for the next 4 weeks for a specific crop and region"""
    logger.info(f"Prediction request received for {request.crop} in {request.region}")
    
    try:
        # Get predictions for the next 4 weeks
        predictions = predictor.predict(request.crop, request.region)
        
        # Format predictions for response
        prediction_entries = []
        current_date = datetime.now().date()
        
        for i, price in enumerate(predictions):
            prediction_date = current_date + timedelta(days=(i+1)*7)  # Weekly predictions
            prediction_entries.append(
                PredictionEntry(
                    prediction_index=i,
                    date=prediction_date.strftime("%Y-%m-%d"),
                    price=float(price)
                )
            )
        
        return PredictionResponse(
            crop=request.crop,
            region=request.region,
            predictions=prediction_entries
        )
    
    except KeyError:
        logger.error(f"Invalid crop or region: {request.crop}, {request.region}")
        raise HTTPException(
            status_code=400, 
            detail=f"No data available for crop '{request.crop}' in region '{request.region}'"
        )
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.post("/api/data/weather")
def add_weather_data(request: WeatherDataRequest):
    """Add new weather data"""
    logger.info(f"Weather data received for {request.region} on {request.date}")
    
    try:
        # Store weather data
        weather_entry = WeatherEntry(
            date=request.date,
            region=request.region,
            temperature=request.weatherData.temp,
            rainfall=request.weatherData.rainfall,
            humidity=request.weatherData.humidity,
            # Calculate crop yield impact score based on weather data
            # This is a placeholder - actual calculation would depend on specific requirements
            crop_yield_impact_score=calculate_yield_impact(
                request.weatherData.temp, 
                request.weatherData.rainfall, 
                request.weatherData.humidity
            )
        )
        
        storage.add_weather_data(weather_entry)
        
        # Update model with new data
        predictor.update_weather_data(storage.get_weather_data())
        
        return {"status": "success", "message": "Weather data stored successfully"}
    
    except Exception as e:
        logger.error(f"Error storing weather data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error storing weather data: {str(e)}")

@app.post("/api/data/prices")
def add_price_data(request: PriceDataRequest):
    """Add new price data"""
    logger.info(f"Price data received for {request.crop} in {request.region} on {request.date}")
    
    try:
        # Store price data
        storage.add_price_data({
            "date": request.date,
            "region": request.region,
            "commodity": request.crop,
            "price": request.priceData.price,
            # Type is required in the dataset but not in the API request
            # This could be determined from existing data or require modification of the API
            "type": determine_commodity_type(request.crop)
        })
        
        # Update model with new data
        predictor.update_price_data(storage.get_price_data())
        
        return {"status": "success", "message": "Price data stored successfully"}
    
    except Exception as e:
        logger.error(f"Error storing price data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error storing price data: {str(e)}")

def calculate_yield_impact(temperature, rainfall, humidity):
    """
    Calculate crop yield impact score based on weather parameters
    This is a simplified placeholder - actual calculation would be more complex
    """
    # Simple weighted average as an example
    if None in (temperature, rainfall, humidity):
        return None
    
    # Normalize values (assuming typical ranges)
    norm_temp = min(max((temperature - 273.15) / 30, 0), 1)  # Convert K to C, normalize around 0-30C
    norm_rain = min(max(rainfall / 50, 0), 1)  # Normalize around 0-50mm
    norm_humid = min(max(humidity / 100, 0), 1)  # Normalize 0-100%
    
    # Simple weighted score
    return (0.4 * norm_temp + 0.4 * norm_rain + 0.2 * norm_humid) * 10  # 0-10 scale

def determine_commodity_type(crop):
    """
    Determine if a commodity is a fruit or vegetable
    This could be based on a predefined mapping or existing data
    """
    # This is a simplified version - a real implementation would have a complete mapping
    fruits = ["Apple", "Banana", "Cantaloupe", "Cherry", "Grape", "Mango", "Orange", 
              "Peach", "Pear", "Plum", "Strawberry", "Watermelon"]
    
    if crop in fruits:
        return "Fruit"
    return "Vegetable"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)