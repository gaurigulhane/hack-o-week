import unittest
import os
import sys
sys.path.append("/tmp/sports_libs")
sys.path.append(os.getcwd())
from fastapi.testclient import TestClient
from backend.main import app

class TestAPIFallback(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_predict_fallback(self):
        # Even if the model isn't loaded/found, the API should return a fallback
        response = self.client.get("/predict?day_type=Weekday")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("predicted", data)
        self.assertEqual(len(data["predicted"]), 24)

if __name__ == "__main__":
    unittest.main()
