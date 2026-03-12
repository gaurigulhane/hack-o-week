import unittest
import sys
import os
sys.path.append("/tmp/sports_libs")
sys.path.append(os.getcwd()) # Add project root for backend package
import pandas as pd
from backend.data_gen import generate_data

class TestDataGen(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate small sample data for testing
        if not os.path.exists('backend'):
            os.makedirs('backend')
        generate_data(days=10)
        cls.df = pd.read_csv('backend/sports_facility_usage.csv')

    def test_schema_columns(self):
        expected_columns = ['timestamp', 'hour', 'day_of_week', 'is_weekend', 'electricity_usage', 'is_event', 'day_type']
        for col in expected_columns:
            self.assertIn(col, self.df.columns)

    def test_negative_values(self):
        self.assertTrue((self.df['electricity_usage'] >= 0).all())

    def test_day_types(self):
        valid_types = ['Weekday', 'Weekend', 'Event']
        self.assertTrue(self.df['day_type'].isin(valid_types).all())

if __name__ == "__main__":
    unittest.main()
