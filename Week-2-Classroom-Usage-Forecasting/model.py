import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from pmdarima import auto_arima
import warnings

warnings.filterwarnings("ignore")

class ElectricityForecaster:
    def __init__(self, data):
        self.data = data.copy()
        self.data['timestamp'] = pd.to_datetime(self.data['timestamp'])
        self.data.set_index('timestamp', inplace=True)
        self.data = self.data.asfreq('H')
        
    def train_arima(self, target_col='electricity_draw', exog_col='occupancy'):
        """
        Trains an ARIMAX model using occupancy as an exogenous variable.
        """
        # Prepare data
        y = self.data[target_col]
        exog = self.data[[exog_col]]
        
        # Use auto_arima to find best parameters (p, d, q)
        # For simplicity and speed in a "simple ARIMA" request, we can also hardcode or use a fast search
        # Best to use a simple (1,1,1) or (2,1,1) if data is seasonal
        
        # In a real scenario, occupancy for the next hour is unknown.
        # But here we can assume we have historical data to train.
        
        # Using a fixed order for speed in this demo, or auto_arima
        # Best practice: auto_arima(y, exogenous=exog, seasonal=True, m=24)
        
        # Let's use a standard ARIMA(2,1,2) for illustration
        model = ARIMA(y, exog=exog, order=(2, 1, 2))
        self.model_fit = model.fit()
        return self.model_fit

    def forecast_next_hour(self, next_occupancy, steps=1):
        """
        Forecasts the next step(s).
        next_occupancy: The expected occupancy for the next hour(s).
        """
        exog_next = np.array([[next_occupancy]])
        forecast_res = self.model_fit.get_forecast(steps=steps, exog=exog_next)
        
        forecast_mean = forecast_res.summary_frame()['mean']
        forecast_ci = forecast_res.summary_frame()[['mean_ci_lower', 'mean_ci_upper']]
        
        return forecast_mean, forecast_ci

if __name__ == "__main__":
    from data_generator import generate_classroom_data
    df = generate_classroom_data(days=7)
    forecaster = ElectricityForecaster(df)
    forecaster.train_arima()
    
    # Forecast for next hour assuming 25 people
    mean, ci = forecaster.forecast_next_hour(next_occupancy=25)
    print(f"Forecasted Electricity Draw: {mean.values[0]:.2f} kW")
    print(f"95% Confidence Interval: [{ci.iloc[0, 0]:.2f}, {ci.iloc[0, 1]:.2f}] kW")
