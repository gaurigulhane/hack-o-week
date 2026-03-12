import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_data():
    # Set seed for reproducibility
    np.random.seed(42)
    
    # 2 years of hourly data
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 12, 31, 23, 0)
    dates = pd.date_range(start=start_date, end=end_date, freq='h')
    
    # Base energy usage (kW)
    base_usage = 50
    
    # Seasonality components
    hourly_seasonality = 10 * np.sin(2 * np.pi * dates.hour / 24)
    daily_seasonality = 5 * np.sin(2 * np.pi * dates.dayofweek / 7)
    
    # Noise
    noise = np.random.normal(0, 2, len(dates))
    
    energy_usage = base_usage + hourly_seasonality + daily_seasonality + noise
    
    # Academic Calendar (Exam Periods)
    # Mid-May (Finals), Mid-December (Finals), Mid-March (Midterms), Mid-October (Midterms)
    exam_periods = [
        ('2024-03-10', '2024-03-20', 'Midterms'),
        ('2024-05-10', '2024-05-25', 'Finals'),
        ('2024-10-10', '2024-10-20', 'Midterms'),
        ('2024-12-10', '2024-12-23', 'Finals'),
        ('2025-03-10', '2025-03-20', 'Midterms'),
        ('2025-05-10', '2025-05-25', 'Finals'),
        ('2025-10-10', '2025-10-20', 'Midterms'),
        ('2025-12-10', '2025-12-23', 'Finals'),
    ]
    
    calendar_df = pd.DataFrame(exam_periods, columns=['start', 'end', 'event'])
    calendar_df['start'] = pd.to_datetime(calendar_df['start'])
    calendar_df['end'] = pd.to_datetime(calendar_df['end'])
    
    # Apply exam energy surges
    energy_df = pd.DataFrame({'timestamp': dates, 'energy_kw': energy_usage})
    
    for _, row in calendar_df.iterrows():
        mask = (energy_df['timestamp'] >= row['start']) & (energy_df['timestamp'] <= row['end'])
        # Finals have higher surge than Midterms
        surge_factor = 2.0 if row['event'] == 'Finals' else 1.5
        energy_df.loc[mask, 'energy_kw'] *= surge_factor
        # Add some extra variation during exams
        energy_df.loc[mask, 'energy_kw'] += np.random.normal(5, 2, mask.sum())

    # Save to files
    energy_df.to_csv('library_energy.csv', index=False)
    calendar_df.to_csv('academic_calendar.csv', index=False)
    print("Data generation complete: library_energy.csv and academic_calendar.csv created.")

if __name__ == "__main__":
    generate_data()
