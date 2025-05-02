import datetime
import pandas as pd
import numpy as np
from typing import List, Dict, Any, Union
import logging

logger = logging.getLogger(__name__)

def parse_date(date_str: str) -> datetime.date:
    """
    Parse date string into datetime.date object
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        datetime.date object
    """
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        logger.warning(f"Invalid date format: {date_str}, using current date")
        return datetime.date.today()

def format_date(date_obj: datetime.date) -> str:
    """
    Format date object as string
    
    Args:
        date_obj: datetime.date object
        
    Returns:
        Date string in YYYY-MM-DD format
    """
    return date_obj.strftime('%Y-%m-%d')

def get_week_number(date_str: str) -> int:
    """
    Get ISO week number from date string
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        
    Returns:
        ISO week number (1-53)
    """
    date_obj = parse_date(date_str)
    return date_obj.isocalendar()[1]

def calculate_weekly_stats(data: pd.DataFrame, group_cols: List[str], value_col: str) -> pd.DataFrame:
    """
    Calculate weekly statistics for a value column
    
    Args:
        data: DataFrame containing data
        group_cols: Columns to group by
        value_col: Column to calculate statistics for
        
    Returns:
        DataFrame with weekly statistics
    """
    # Add week number column
    data = data.copy()
    data['week'] = data['date'].apply(get_week_number)
    
    # Group by specified columns and week
    grouped = data.groupby(group_cols + ['week'])
    
    # Calculate statistics
    stats = pd.DataFrame({
        'min': grouped[value_col].min(),
        'max': grouped[value_col].max(),
        'mean': grouped[value_col].mean(),
        'median': grouped[value_col].median(),
        'std': grouped[value_col].std(),
        'count': grouped[value_col].count()
    }).reset_index()
    
    return stats

def get_next_n_weeks(n: int = 4) -> List[str]:
    """
    Get dates for the next N weeks
    
    Args:
        n: Number of weeks
        
    Returns:
        List of date strings for the next N weeks
    """
    today = datetime.date.today()
    
    # Find the next weeks
    weeks = []
    for i in range(1, n+1):
        next_week = today + datetime.timedelta(days=i*7)
        weeks.append(format_date(next_week))
    
    return weeks

def add_feature_lags(df: pd.DataFrame, feature_col: str, lag_periods: List[int]) -> pd.DataFrame:
    """
    Add lagged features to DataFrame
    
    Args:
        df: Input DataFrame
        feature_col: Column to create lags for
        lag_periods: List of lag periods
        
    Returns:
        DataFrame with added lag columns
    """
    result = df.copy()
    
    for lag in lag_periods:
        result[f'{feature_col}_lag_{lag}'] = result[feature_col].shift(lag)
    
    return result

def add_rolling_stats(df: pd.DataFrame, feature_col: str, windows: List[int]) -> pd.DataFrame:
    """
    Add rolling statistics to DataFrame
    
    Args:
        df: Input DataFrame
        feature_col: Column to calculate rolling statistics for
        windows: List of window sizes
        
    Returns:
        DataFrame with added rolling statistics columns
    """
    result = df.copy()
    
    for window in windows:
        result[f'{feature_col}_rolling_mean_{window}'] = result[feature_col].rolling(window=window, min_periods=1).mean()
        result[f'{feature_col}_rolling_std_{window}'] = result[feature_col].rolling(window=window, min_periods=1).std()
        result[f'{feature_col}_rolling_min_{window}'] = result[feature_col].rolling(window=window, min_periods=1).min()
        result[f'{feature_col}_rolling_max_{window}'] = result[feature_col].rolling(window=window, min_periods=1).max()
    
    return result

def filter_by_date_range(df: pd.DataFrame, start_date: str = None, end_date: str = None) -> pd.DataFrame:
    """
    Filter DataFrame by date range
    
    Args:
        df: Input DataFrame with a 'date' column
        start_date: Start date (inclusive)
        end_date: End date (inclusive)
        
    Returns:
        Filtered DataFrame
    """
    result = df.copy()
    
    if start_date:
        result = result[result['date'] >= start_date]
    
    if end_date:
        result = result[result['date'] <= end_date]
    
    return result

def merge_weather_price_data(weather_df: pd.DataFrame, price_df: pd.DataFrame) -> pd.DataFrame:
    """
    Merge weather and price data
    
    Args:
        weather_df: Weather DataFrame
        price_df: Price DataFrame
        
    Returns:
        Merged DataFrame
    """
    # Ensure date columns are of the same type
    weather_df = weather_df.copy()
    price_df = price_df.copy()
    
    # Merge on date and region
    merged_df = pd.merge(
        price_df,
        weather_df,
        on=['date', 'region'],
        how='left'
    )
    
    return merged_df

def normalize_data(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Normalize specified columns to 0-1 range
    
    Args:
        df: Input DataFrame
        columns: Columns to normalize
        
    Returns:
        DataFrame with normalized columns
    """
    result = df.copy()
    
    for col in columns:
        if col in result.columns:
            min_val = result[col].min()
            max_val = result[col].max()
            
            if max_val > min_val:
                result[col] = (result[col] - min_val) / (max_val - min_val)
            else:
                # If all values are the same, set to 0.5
                result[col] = 0.5
    
    return result

def detect_outliers(df: pd.DataFrame, column: str, z_threshold: float = 3.0) -> pd.DataFrame:
    """
    Detect outliers in a column using z-score
    
    Args:
        df: Input DataFrame
        column: Column to check for outliers
        z_threshold: Z-score threshold for outliers
        
    Returns:
        DataFrame with outlier flag column
    """
    result = df.copy()
    
    # Calculate z-score
    mean = result[column].mean()
    std = result[column].std()
    
    if std > 0:
        result[f'{column}_zscore'] = (result[column] - mean) / std
        result[f'{column}_is_outlier'] = abs(result[f'{column}_zscore']) > z_threshold
    else:
        result[f'{column}_zscore'] = 0
        result[f'{column}_is_outlier'] = False
    
    return result