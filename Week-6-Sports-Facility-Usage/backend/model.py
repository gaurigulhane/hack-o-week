import sys
import os
# Add libs to path before other imports
sys.path.append("/tmp/sports_libs")

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler

class ElectricityPredictor:
    """
    A Simple LSTM based RNN for predicting hourly electricity usage patterns.
    Uses historical data (24-hour windows) to forecast the next hour's usage.
    """
    def __init__(self):
        self.scaler = MinMaxScaler()
        self.model = None
        self.window_size = 24 # Use last 24 hours to predict next hour

    def prepare_data(self, csv_path):
        """
        Loads CSV data, scales it using MinMaxScaler, and generates 
        windowed samples (X) and targets (y) for RNN training.
        """
        df = pd.read_csv(csv_path)
        data = df['electricity_usage'].values.reshape(-1, 1)
        scaled_data = self.scaler.fit_transform(data)
        
        X, y = [], []
        for i in range(len(scaled_data) - self.window_size):
            X.append(scaled_data[i:i+self.window_size])
            y.append(scaled_data[i+self.window_size])
            
        return np.array(X), np.array(y)

    def build_model(self):
        model = Sequential([
            LSTM(50, activation='relu', input_shape=(self.window_size, 1), return_sequences=True),
            Dropout(0.2),
            LSTM(50, activation='relu'),
            Dropout(0.2),
            Dense(1)
        ])
        model.compile(optimizer='adam', loss='mse')
        self.model = model
        return model

    def train(self, X, y, epochs=10):
        if self.model is None:
            self.build_model()
        self.model.fit(X, y, epochs=epochs, batch_size=32, validation_split=0.1)
        
    def save_model(self, path='backend/model.h5'):
        if self.model:
            self.model.save(path)
            
    def predict(self, last_24_hours):
        scaled_input = self.scaler.transform(np.array(last_24_hours).reshape(-1, 1))
        prediction = self.model.predict(scaled_input.reshape(1, self.window_size, 1))
        return self.scaler.inverse_transform(prediction)[0][0]

if __name__ == "__main__":
    predictor = ElectricityPredictor()
    X, y = predictor.prepare_data('backend/sports_facility_usage.csv')
    predictor.build_model()
    predictor.train(X, y, epochs=5)
    predictor.save_model()
    print("Model trained and saved.")
