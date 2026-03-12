import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib
import os

def generate_synthetic_data(samples=1000):
    np.random.seed(42)
    
    # Features: Temperature (C), Humidity (%), Hour (0-23)
    temp = np.random.uniform(15, 35, samples)
    humidity = np.random.uniform(30, 90, samples)
    hour = np.random.uniform(10, 15, samples) # Focusing on lunch hours
    
    # Lunch peak factor: higher load between 12:00 and 13:30
    lunch_peak = np.where((hour >= 11.5) & (hour <= 13.5), 50, 0)
    
    # Base load + temperature effect + humidity effect + lunch surge + noise
    load = 20 + 0.5 * temp - 0.1 * humidity + lunch_peak + np.random.normal(0, 5, samples)
    
    df = pd.DataFrame({
        'temperature': temp,
        'humidity': humidity,
        'hour': hour,
        'load': load
    })
    
    return df

def train_model():
    print("Generating synthetic data...")
    df = generate_synthetic_data()
    
    X = df[['temperature', 'humidity', 'hour']]
    y = df['load']
    
    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X, y)
    
    # Save the model
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/cafeteria_model.joblib')
    print("Model saved to models/cafeteria_model.joblib")
    
    # Example prediction
    test_data = np.array([[25, 50, 12.5]]) # 25C, 50% hum, 12:30 PM
    prediction = model.predict(test_data)
    print(f"Test Prediction (25C, 50% humidity, 12:30 PM): {prediction[0]:.2f}")

if __name__ == "__main__":
    train_model()
