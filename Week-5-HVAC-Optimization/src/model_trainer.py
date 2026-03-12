import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
import os

# Using joblib instead of pickle for scikit-learn
import joblib

def train_model(data_path='data/hvac_data.csv'):
    df = pd.read_csv(data_path)
    
    # Feature engineering
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    
    # One-hot encode zones
    df = pd.get_dummies(df, columns=['zone'], prefix='zone')
    
    features = ['occupancy', 'ambient_temp', 'equipment_power', 'hour'] + [c for c in df.columns if c.startswith('zone_')]
    X = df[features]
    y = df['cooling_need']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = DecisionTreeRegressor(max_depth=5, random_state=42)
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    
    print(f"Model trained. MSE: {mse:.4f}")
    
    # Save model and features
    if not os.path.exists('models'):
        os.makedirs('models')
        
    joblib.dump(model, 'models/hvac_model.joblib')
    joblib.dump(features, 'models/features.joblib')
    
    return model, mse

if __name__ == "__main__":
    train_model()
