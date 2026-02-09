## AgroChill – Agricultural Price Forecasting System

AgroChill is a data-driven forecasting system designed to predict weekly market prices of fruits and vegetables across multiple regions. The system supports strategic decision-making by recommending whether to sell produce immediately or store it for future profit, based on predicted price trends, weather conditions, and forecast confidence.

The model generates rolling four-week-ahead price forecasts using historical market price data and environmental factors. It continuously adapts as new data becomes available, ensuring predictions remain aligned with real-world market dynamics.

### Key Features
- Weekly price forecasting for multiple commodity–region pairs
- Rolling four-week-ahead predictions
- Hybrid modeling approach combining time series analysis and machine learning
- Advanced feature engineering using lagged and rolling window features
- Confidence-aware decision logic for selling or freezing produce
- Interpretable outputs with clear business recommendations

### Model Architecture
- **Facebook Prophet** for capturing trend and seasonal patterns in agricultural markets
- **LightGBM** for modeling complex nonlinear relationships between weather variables and prices

### Technologies Used
- Python
- Facebook Prophet
- LightGBM
- Pandas
- Scikit-learn

### Application
AgroChill transforms complex forecasting outputs into actionable business decisions, helping optimize cold storage usage and maximize profitability in agricultural markets.
