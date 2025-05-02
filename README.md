# AgroChill Price Forecasting System

This is the AgroChill Price Forecasting System, built for Magnus Greenvale's Freezer Gambit in Agrovia. The system predicts crop prices for the next 4 weeks to support strategic storage and sales decisions.

## Overview

The AgroChill system provides:

- Price predictions for 37 commodities across 25 regions
- APIs for retrieving predictions and submitting new data
- Data storage and model updating capabilities
- Dockerized deployment for easy installation

## Technical Architecture

The system consists of the following components:

1. **FastAPI Backend**: REST API endpoints for predictions and data submission
2. **Forecasting Model**: Time series model for predicting crop prices
3. **Data Storage**: Storage and management of weather and price data
4. **Docker Deployment**: Containerized for easy deployment

## API Endpoints

The system exposes the following API endpoints:

1. `/api/predict`: Get price predictions for a specific crop in a specific region
2. `/api/data/weather`: Submit new weather data
3. `/api/data/prices`: Submit new price data

## Installation and Running

### Prerequisites

- Docker
- Docker Compose (optional)

### Building and Running the Docker Container

1. Clone this repository
2. Navigate to the repository root
3. Build the Docker image:

```bash
docker build -t agrochill:latest .
```

4. Run the container:

```bash
docker run -p 8000:8000 agrochill:latest
```

The API will be available at: http://localhost:8000

### API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Example API Usage

### Get Price Predictions

```bash
curl -X POST "http://localhost:8000/api/predict" \
     -H "Content-Type: application/json" \
     -d '{"crop": "Cantaloupe", "region": "Valhalla"}'
```

### Submit Weather Data

```bash
curl -X POST "http://localhost:8000/api/data/weather" \
     -H "Content-Type: application/json" \
     -d '{
           "date": "2025-04-16",
           "region": "Valhalla",
           "weatherData": {
             "temp": 29.4,
             "rainfall": 5.2,
             "humidity": 78.3
           }
         }'
```

### Submit Price Data

```bash
curl -X POST "http://localhost:8000/api/data/prices" \
     -H "Content-Type: application/json" \
     -d '{
           "date": "2025-04-16",
           "crop": "Cantaloupe",
           "region": "Valhalla",
           "priceData": {
             "price": 86.4
           }
         }'
```

## Project Structure

```
agrochill/
├── app/
│   ├── __init__.py
│   ├── main.py               # FastAPI application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   ├── predictor.py      # Model prediction logic
│   │   └── schemas.py        # Pydantic schemas for API
│   ├── data/
│   │   ├── __init__.py
│   │   ├── database.py       # Database connection and operations
│   │   └── storage.py        # Data storage utilities
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Helper functions
├── models/
│   └── agrochill_model.pkl   # Serialized forecast model
├── data/
│   ├── weather.csv           # Storage for weather data
│   └── prices.csv            # Storage for price data
├── Dockerfile                # Docker configuration
├── requirements.txt          # Python dependencies
└── README.md                 # Documentation
```