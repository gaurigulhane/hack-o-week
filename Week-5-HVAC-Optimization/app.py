import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Set page config
st.set_page_config(page_title="HVAC Lab Optimizer", layout="wide", initial_sidebar_state="expanded")

# Load model and features
@st.cache_resource
def load_assets():
    model = joblib.load('models/hvac_model.joblib')
    features = joblib.load('models/features.joblib')
    return model, features

try:
    model, features = load_assets()
    data = pd.read_csv('data/hvac_data.csv')
except Exception as e:
    st.error(f"Error loading assets: {e}. Please ensure model training is complete.")
    st.stop()

# Title and Header
st.title("🌡️ HVAC Optimization - Lab Zone Forecast")
st.markdown("""
Monitor and forecast cooling needs across laboratory zones using Decision Tree AI.
Adjust occupancy and ambient conditions to see real-time forecasts.
""")

# Sidebar Controls
st.sidebar.header("Control Panel")
hour = st.sidebar.slider("Current Hour", 0, 23, datetime.now().hour)
ambient_temp = st.sidebar.slider("Ambient Temperature (°C)", 15.0, 40.0, 25.0)

zones = ['Lab A', 'Lab B', 'Clean Room', 'Office 1']
zone_occupancy = {}

st.sidebar.subheader("Zone Occupancy")
for zone in zones:
    zone_occupancy[zone] = st.sidebar.number_input(f"{zone} People", 0, 50, 5)

# Prediction Logic
def get_prediction(zone, occupancy, temp, hour):
    # Prepare feature vector
    input_data = pd.DataFrame(columns=features)
    input_data.loc[0] = 0
    
    input_data['occupancy'] = occupancy
    input_data['ambient_temp'] = temp
    input_data['hour'] = hour
    
    zone_col = f'zone_{zone}'
    if zone_col in input_data.columns:
        input_data[zone_col] = 1
        
    prediction = model.predict(input_data)[0]
    return max(0, prediction)

# Calculate Forecasts
forecasts = {}
for zone in zones:
    forecasts[zone] = get_prediction(zone, zone_occupancy[zone], ambient_temp, hour)

# Display Metrics
cols = st.columns(len(zones))
for i, zone in enumerate(zones):
    cols[i].metric(label=f"{zone} Cooling", value=f"{forecasts[zone]:.2f} kW", delta=None)

# Heatmap Visualization
st.subheader("🔥 Zone-wise Cooling Need Heatmap")

# Create a grid for the heatmap
# For simplicity, we'll map 4 zones to a 2x2 grid
heatmap_data = np.array([
    [forecasts['Lab A'], forecasts['Lab B']],
    [forecasts['Clean Room'], forecasts['Office 1']]
])

fig = px.imshow(
    heatmap_data,
    labels=dict(x="Zone X", y="Zone Y", color="Cooling (kW)"),
    x=['A/Lab', 'B/Lab'],
    y=['Clean', 'Office'],
    color_continuous_scale='YlOrRd',
    text_auto=".2f",
    aspect="auto"
)

fig.update_layout(height=400)
st.plotly_chart(fig, use_container_width=True)

# Historical Analysis
st.subheader("📊 Historical Cooling Load (Last 24h)")
# Get latest 24 samples from data
latest_data = data.tail(4 * 24) # 4 zones * 24 hours
fig_line = px.line(
    latest_data, 
    x='timestamp', 
    y='cooling_need', 
    color='zone',
    title="Cooling Demand Trends",
    template="plotly_dark"
)
st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.info("Decision Tree Model version: 1.0.0 | MSE: 0.0952")
