import pandas as pd
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class DataStorage:
    """
    DataStorage class manages the storage and retrieval of weather and price data
    """
    def __init__(self, weather_file='data/weather.csv', price_file='data/prices.csv'):
        """
        Initialize data storage with file paths
        
        Args:
            weather_file: Path to the weather data CSV file
            price_file: Path to the price data CSV file
        """
        self.weather_file = weather_file
        self.price_file = price_file
        self.weather_data = None
        self.price_data = None
        
        # Ensure data directories exist
        os.makedirs(os.path.dirname(weather_file), exist_ok=True)
        os.makedirs(os.path.dirname(price_file), exist_ok=True)
    
    def load_data(self):
        """Load weather and price data from CSV files"""
        try:
            if os.path.exists(self.weather_file):
                self.weather_data = pd.read_csv(self.weather_file)
                logger.info(f"Weather data loaded: {len(self.weather_data)} records")
            else:
                # Create empty DataFrame with expected columns
                self.weather_data = pd.DataFrame(columns=[
                    'date', 'region', 'temperature', 'rainfall', 
                    'humidity', 'crop_yield_impact_score'
                ])
                logger.info("Created empty weather data DataFrame")
            
            if os.path.exists(self.price_file):
                self.price_data = pd.read_csv(self.price_file)
                logger.info(f"Price data loaded: {len(self.price_data)} records")
            else:
                # Create empty DataFrame with expected columns
                self.price_data = pd.DataFrame(columns=[
                    'date', 'region', 'commodity', 'price', 'type'
                ])
                logger.info("Created empty price data DataFrame")
        except Exception as e:
            logger.error(f"Error loading data: {str(e)}")
            # Initialize empty DataFrames if loading fails
            self.weather_data = pd.DataFrame(columns=[
                'date', 'region', 'temperature', 'rainfall', 
                'humidity', 'crop_yield_impact_score'
            ])
            self.price_data = pd.DataFrame(columns=[
                'date', 'region', 'commodity', 'price', 'type'
            ])
    
    def save_data(self):
        """Save weather and price data to CSV files"""
        try:
            if self.weather_data is not None:
                self.weather_data.to_csv(self.weather_file, index=False)
                logger.info(f"Weather data saved to {self.weather_file}")
            
            if self.price_data is not None:
                self.price_data.to_csv(self.price_file, index=False)
                logger.info(f"Price data saved to {self.price_file}")
        except Exception as e:
            logger.error(f"Error saving data: {str(e)}")
    
    def get_weather_data(self):
        """
        Get weather data
        
        Returns:
            DataFrame containing weather data
        """
        if self.weather_data is None:
            self.load_data()
        return self.weather_data
    
    def get_price_data(self):
        """
        Get price data
        
        Returns:
            DataFrame containing price data
        """
        if self.price_data is None:
            self.load_data()
        return self.price_data
    
    def add_weather_data(self, weather_entry):
        """
        Add a weather data entry
        
        Args:
            weather_entry: Dictionary or Pydantic model containing weather data
        """
        if self.weather_data is None:
            self.load_data()
        
        # Convert Pydantic model to dict if needed
        if hasattr(weather_entry, 'dict'):
            weather_entry = weather_entry.dict()
        
        # Add entry to DataFrame
        self.weather_data = pd.concat([
            self.weather_data, 
            pd.DataFrame([weather_entry])
        ], ignore_index=True)
        
        # Remove duplicates if any
        self.weather_data = self.weather_data.drop_duplicates(
            subset=['date', 'region'], 
            keep='last'
        )
        
        # Save data
        self.save_data()
        logger.info(f"Weather data added for {weather_entry['region']} on {weather_entry['date']}")
    
    def add_price_data(self, price_entry):
        """
        Add a price data entry
        
        Args:
            price_entry: Dictionary or Pydantic model containing price data
        """
        if self.price_data is None:
            self.load_data()
        
        # Convert Pydantic model to dict if needed
        if hasattr(price_entry, 'dict'):
            price_entry = price_entry.dict()
        
        # Add entry to DataFrame
        self.price_data = pd.concat([
            self.price_data, 
            pd.DataFrame([price_entry])
        ], ignore_index=True)
        
        # Remove duplicates if any
        self.price_data = self.price_data.drop_duplicates(
            subset=['date', 'region', 'commodity'], 
            keep='last'
        )
        
        # Save data
        self.save_data()
        logger.info(f"Price data added for {price_entry['commodity']} in {price_entry['region']} on {price_entry['date']}")
    
    def get_regions(self):
        """
        Get list of unique regions
        
        Returns:
            List of region names
        """
        if self.weather_data is None:
            self.load_data()
        
        return sorted(self.weather_data['region'].unique().tolist())
    
    def get_commodities(self):
        """
        Get list of unique commodities
        
        Returns:
            List of commodity names
        """
        if self.price_data is None:
            self.load_data()
        
        return sorted(self.price_data['commodity'].unique().tolist())