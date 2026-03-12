import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_admin_data(days=60):
    np.random.seed(42)
    start_date = datetime(2026, 1, 1)
    data = []
    
    for day in range(days):
        current_day = start_date + timedelta(days=day)
        is_weekend = current_day.weekday() >= 5
        
        # Base load
        base_load = 50 if not is_weekend else 20
        
        for hour in range(24):
            # Daily profile
            time_factor = np.sin(np.pi * (hour - 6) / 12) if 6 <= hour <= 20 else 0
            if time_factor < 0: time_factor = 0
            
            activity_load = 100 * time_factor if not is_weekend else 10 * time_factor
            noise = np.random.normal(0, 5)
            
            total_usage = base_load + activity_load + noise
            data.append({
                'timestamp': current_day.replace(hour=hour),
                'usage': max(5, total_usage),
                'hour': hour,
                'day_of_week': current_day.weekday(),
                'is_weekend': int(is_weekend)
            })
            
    df = pd.DataFrame(data)
    df.to_csv('admin_usage.csv', index=False)
    print("Generated admin_usage.csv")
    return df

if __name__ == "__main__":
    generate_admin_data()
