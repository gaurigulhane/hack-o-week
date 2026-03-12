from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import json
import os
import sys

# Add libs to path
sys.path.append("/tmp/sports_libs")

# Import our model class
from model import ElectricityPredictor

app = FastAPI(
    title="Sports Facility Usage API",
    description="API for predicting and retrieving hourly electricity usage data."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = ElectricityPredictor()
DATA_PATH = 'backend/sports_facility_usage.csv'
MODEL_PATH = 'backend/model.h5'

@app.get("/")
def read_root():
    """Health check endpoint."""
    return {"message": "Sports Facility API is running"}

@app.get("/data")
def get_data(day_type: str = "All"):
    """
    Retrieves historical/synthetic electricity usage data.
    Allows filtering by day_type (Weekday, Weekend, Event).
    """
    df = pd.read_csv(DATA_PATH)
    if day_type != "All":
        df = df[df['day_type'] == day_type]
    
    # Take a sample of 24 hours for the dashboard
    sample = df.head(24)
    return {
        "labels": sample['hour'].tolist(),
        "actual": sample['electricity_usage'].tolist(),
        "day_type": day_type
    }

@app.get("/predict")
def predict_usage(day_type: str = "All"):
    df = pd.read_csv(DATA_PATH)
    if day_type != "All":
        df = df[df['day_type'] == day_type]
    
    # Take a sample for the dashboard
    sample = df.head(48) # Get 48 hours to have 24 for context and 24 to predict
    
    if os.path.exists(MODEL_PATH):
        try:
            # Load model if not loaded
            if predictor.model is None:
                predictor.prepare_data(DATA_PATH) # This fits the scaler
                predictor.build_model()
                predictor.model.load_weights(MODEL_PATH)
            
            # Predict for the next 24 hours based on the first 24 hours of the sample
            context = sample['electricity_usage'].values[:24]
            predictions = []
            curr_context = list(context)
            
            for _ in range(24):
                pred = predictor.predict(curr_context[-24:])
                predictions.append(float(pred))
                curr_context.append(pred)
                
            return {
                "labels": [f"{i}:00" for i in range(24)],
                "actual": sample['electricity_usage'].values[24:48].tolist(),
                "predicted": predictions,
                "day_type": day_type
            }
        except Exception as e:
            return {"error": str(e), "fallback": True}
            
    # Fallback to dummy
    return {
        "labels": [f"{i}:00" for i in range(24)],
        "actual": sample['electricity_usage'].values[24:48].tolist(),
        "predicted": [v * 1.1 for v in sample['electricity_usage'].values[24:48].tolist()]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
# Final backend cleanup
