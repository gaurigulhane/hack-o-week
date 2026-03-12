import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_lab_data(num_days=30, zones=['Lab A', 'Lab B', 'Clean Room', 'Office 1']):
    np.random.seed(42)
    start_date = datetime(2025, 1, 1)
    
    data = []
    
    for day in range(num_days):
        current_date = start_date + timedelta(days=day)
        
        for hour in range(24):
            timestamp = current_date + timedelta(hours=hour)
            
            for zone in zones:
                # Basic seasonal/diurnal temperature variation
                ambient_temp = 20 + 5 * np.sin(2 * np.pi * (hour - 6) / 24) + np.random.normal(0, 1)
                
                # Occupancy pattern (higher during day)
                if 9 <= hour <= 18:
                    occupancy = np.random.randint(5, 20) if 'Office' not in zone else np.random.randint(2, 10)
                else:
                    occupancy = np.random.randint(0, 3)
                
                # Equipment power depends on occupancy and zone type
                base_power = 2.0 if 'Clean Room' in zone else 0.5
                equipment_power = base_power + (occupancy * 0.1) + np.random.normal(0, 0.2)
                
                # Formula for Cooling Need (Target temp 22°C)
                # Cooling = Heat from people + Heat from equipment + Heat from ambient
                heat_per_person = 0.12  # kW
                cooling_need = (occupancy * heat_per_person) + equipment_power + max(0, (ambient_temp - 22) * 0.5)
                
                data.append({
                    'timestamp': timestamp,
                    'zone': zone,
                    'occupancy': occupancy,
                    'ambient_temp': round(ambient_temp, 2),
                    'equipment_power': round(max(0, equipment_power), 2),
                    'cooling_need': round(max(0, cooling_need), 2)
                })
                
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    df = generate_lab_data()
    df.to_csv('data/hvac_data.csv', index=False)
    print(f"Generated {len(df)} records in data/hvac_data.csv")
