import sys
import os
sys.path.append("/tmp/sports_libs")

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_squared_error, mean_absolute_error
from model import ElectricityPredictor

def evaluate():
    predictor = ElectricityPredictor()
    X, y = predictor.prepare_data('backend/sports_facility_usage.csv')
    
    # Load model
    predictor.build_model()
    if os.path.exists('backend/model.h5'):
        predictor.model.load_weights('backend/model.h5')
    else:
        print("Model file not found!")
        return

    # Predictions
    y_pred = predictor.model.predict(X)
    
    # Inverse transform to get real values
    y_true_inv = predictor.scaler.inverse_transform(y.reshape(-1, 1))
    y_pred_inv = predictor.scaler.inverse_transform(y_pred)
    
    mse = mean_squared_error(y_true_inv, y_pred_inv)
    mae = mean_absolute_error(y_true_inv, y_pred_inv)
    
    print(f"Mean Squared Error: {mse:.4f}")
    print(f"Mean Absolute Error: {mae:.4f}")
    
    with open('backend/evaluation_results.txt', 'w') as f:
        f.write(f"Model Evaluation Results\n")
        f.write(f"========================\n")
        f.write(f"MSE: {mse:.4f}\n")
        f.write(f"MAE: {mae:.4f}\n")

if __name__ == "__main__":
    evaluate()
