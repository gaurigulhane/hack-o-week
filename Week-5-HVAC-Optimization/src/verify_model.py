import joblib
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score

def verify_model():
    print("--- HVAC Model Verification ---")
    try:
        model = joblib.load('models/hvac_model.joblib')
        features = joblib.load('models/features.joblib')
        data = pd.read_csv('data/hvac_data.csv')
        
        # Prepare test data (same preprocessing as trainer)
        df = data.copy()
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df = pd.get_dummies(df, columns=['zone'], prefix='zone')
        
        # Ensure all feature columns exist (might be missing if some zones didn't appear in small samples)
        for col in features:
            if col not in df.columns:
                df[col] = 0
                
        X = df[features]
        y_true = df['cooling_need']
        
        y_pred = model.predict(X)
        mae = mean_absolute_error(y_true, y_pred)
        r2 = r2_score(y_true, y_pred)
        
        print(f"Mean Absolute Error: {mae:.4f} kW")
        print(f"R2 Score: {r2:.4f}")
        
        if r2 > 0.8:
            print("Status: ✅ Model performing well.")
        else:
            print("Status: ⚠️ Model accuracy below threshold.")
            
    except Exception as e:
        print(f"Verification failed: {e}")

if __name__ == "__main__":
    verify_model()
