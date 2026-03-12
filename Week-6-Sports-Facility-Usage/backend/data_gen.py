import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data(days=365):
    start_date = datetime(2024, 1, 1)
    date_rng = pd.date_range(start=start_date, periods=days*24, freq='h')
    
    df = pd.DataFrame(date_rng, columns=['timestamp'])
    df['hour'] = df['timestamp'].dt.hour
    df['day_of_week'] = df['timestamp'].dt.dayofweek
    df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Generate base electricity usage pattern
    # lower at night (0-6), peak in evening (17-22)
    def base_usage(hour):
        if 0 <= hour <= 6:
            return 5 + np.random.normal(0, 0.5)
        elif 7 <= hour <= 16:
            return 15 + np.random.normal(0, 1.5)
        elif 17 <= hour <= 22:
            return 40 + np.random.normal(0, 5)
        else:
            return 10 + np.random.normal(0, 1)

    df['electricity_usage'] = df['hour'].apply(base_usage)
    
    # Add weekend effect (higher usage during day)
    df.loc[df['is_weekend'] == 1, 'electricity_usage'] *= 1.5
    
    # Add Event Day effect (Randomly assign 10% days as event days)
    event_days = np.random.choice(df['timestamp'].dt.date.unique(), size=int(days * 0.1), replace=False)
    df['is_event'] = df['timestamp'].dt.date.isin(event_days).astype(int)
    
    # Event days have high usage specifically in evening/night
    df.loc[(df['is_event'] == 1) & (df['hour'] >= 18), 'electricity_usage'] += 50 + np.random.normal(0, 10)
    
    # Ensure no negative values
    df['electricity_usage'] = df['electricity_usage'].clip(lower=0)
    
    # Define day_type for filtering
    def get_day_type(row):
        if row['is_event']:
            return 'Event'
        if row['is_weekend']:
            return 'Weekend'
        return 'Weekday'
    
    df['day_type'] = df.apply(get_day_type, axis=1)
    
    df.to_csv('backend/sports_facility_usage.csv', index=False)
    print("Data generated and saved to backend/sports_facility_usage.csv")

if __name__ == "__main__":
    generate_data()
