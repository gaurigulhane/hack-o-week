import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
import joblib
import os

def train_models():
    if not os.path.exists('admin_usage.csv'):
        from data_generator import generate_admin_data
        df = generate_admin_data()
    else:
        df = pd.read_csv('admin_usage.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Prepare features for clustering (daily profiles)
    daily_usage = df.pivot_table(index=df['timestamp'].dt.date, columns='hour', values='usage')
    
    # 1. K-Means Clustering
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(daily_usage)
    
    # Identify which cluster is which
    cluster_means = daily_usage.mean(axis=1)
    business_cluster = cluster_means.idxmax() # Placeholder logic
    # More robust: cluster with higher average usage is business day
    business_label = np.argmax(kmeans.cluster_centers_.mean(axis=1))
    
    joblib.dump(kmeans, 'kmeans_model.joblib')
    
    # 2. Linear Regression for each cluster
    models = {}
    for cluster_id in range(2):
        cluster_days = daily_usage.index[clusters == cluster_id]
        cluster_data = df[df['timestamp'].dt.date.isin(cluster_days)]
        
        X = cluster_data[['hour', 'day_of_week']]
        y = cluster_data['usage']
        
        lr = LinearRegression()
        lr.fit(X, y)
        models[cluster_id] = lr
        
    joblib.dump(models, 'regression_models.joblib')
    print("Trained and saved models.")

if __name__ == "__main__":
    train_models()
