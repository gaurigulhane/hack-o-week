import pandas as pd
import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import timedelta

def train_and_forecast():
    # Load data
    df = pd.read_csv('library_energy.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    
    # Fill any missing values
    df = df.resample('h').mean().fillna(method='ffill')
    
    # Split into train and test
    # We'll use the last 30 days as a dummy test set for validation
    train_end = df.index.max() - timedelta(days=30)
    train = df[:train_end]
    test = df[train_end:]
    
    print(f"Training model on data from {train.index.min()} to {train.index.max()}")
    
    # Holt-Winters Exponential Smoothing
    # Seasonal period for hourly data is 24 (daily)
    model = ExponentialSmoothing(
        train['energy_kw'],
        seasonal_periods=24,
        trend='add',
        seasonal='add',
    ).fit()
    
    # Forecast
    forecast_steps = len(test)
    forecast = model.forecast(forecast_steps)
    
    # Calculate simple confidence intervals (naive approach for demo)
    # Using residual standard deviation
    residuals = train['energy_kw'] - model.fittedvalues
    sigma = residuals.std()
    
    forecast_df = pd.DataFrame({
        'forecast': forecast.values,
        'lower_ci': forecast.values - 1.96 * sigma,
        'upper_ci': forecast.values + 1.96 * sigma
    }, index=test.index)
    
    print("Forecasting complete.")
    return model, forecast_df

if __name__ == "__main__":
    train_and_forecast()
