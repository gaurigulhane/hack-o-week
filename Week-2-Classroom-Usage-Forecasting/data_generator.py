import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_classroom_data(days=30):
    """
    Generates synthetic hourly data for classroom occupancy (Wi-Fi logs) 
    and electricity draw.
    """
    np.random.seed(42)
    start_date = datetime.now() - timedelta(days=days)
    date_rng = pd.date_range(start=start_date, periods=days*24, freq='H')
    
    df = pd.DataFrame(date_rng, columns=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    
    # Occupancy model (Wi-Fi logs)
    # Higher occupancy during weekdays (0-4) and working hours (8-18)
    def get_occupancy(row):
        if row['day_of_week'] < 5: # Weekday
            if 8 <= row['hour'] <= 18:
                return np.random.randint(10, 50)
            elif 18 < row['hour'] <= 22 or 6 <= row['hour'] < 8:
                return np.random.randint(0, 10)
            else:
                return 0
        else: # Weekend
            if 10 <= row['hour'] <= 16:
                return np.random.randint(0, 5)
            else:
                return 0
                
    df['occupancy'] = df.apply(get_occupancy, axis=1)
    
    # Electricity draw model (kW)
    # Base load + (occupancy * per_person_load) + noise
    # Also affected by time of day (AC/Heating, lighting)
    base_load = 2.0
    per_person_load = 0.05
    
    df['electricity_draw'] = base_load + (df['occupancy'] * per_person_load)
    
    # Add seasonal peak (morning/afternoon)
    df.loc[(df['hour'] >= 9) & (df['hour'] <= 16), 'electricity_draw'] += 1.5
    
    # Add some random noise
    df['electricity_draw'] += np.random.normal(0, 0.2, len(df))
    
    # Ensure no negative values
    df['electricity_draw'] = df['electricity_draw'].clip(lower=0.5)
    
    return df

if __name__ == "__main__":
    df = generate_classroom_data()
    df.to_csv('classroom_data.csv', index=False)
    print("Generated synthetic data and saved to classroom_data.csv")
    print(df.head())
