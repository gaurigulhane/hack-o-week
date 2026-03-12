import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from data_generator import generate_classroom_data
from model import ElectricityForecaster
import datetime

# Page config
st.set_page_config(page_title="Classroom Electricity Forecast", layout="wide")

# Custom CSS for rich aesthetics
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stMetric {
        background-color: #1e2227;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #00d4ff;
    }
    .stPlotlyChart {
        border-radius: 15px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("⚡ Classroom Electricity & Usage Forecasting")
st.markdown("Monitor real-time occupancy and predict future electricity demand using ARIMAX modeling.")

# Sidebar for controls
with st.sidebar:
    st.header("Simulation Settings")
    history_days = st.slider("Historical Data Scope (Days)", 3, 30, 7)
    next_hour_occ = st.slider("Expected Occupancy for Next Hour", 0, 100, 30)
    
    if st.button("Regenerate Data & Retrain Model"):
        st.cache_data.clear()
        st.experimental_rerun()

@st.cache_data
def get_data(days):
    return generate_classroom_data(days)

df = get_data(history_days)

# Model Training
forecaster = ElectricityForecaster(df)
with st.spinner("Training ARIMA Forecast Grid..."):
    forecaster.train_arima()

# Forecast
mean, ci = forecaster.forecast_next_hour(next_occupancy=next_hour_occ)

# Layout
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Current Occupancy", f"{df['occupancy'].iloc[-1]} Persons")
with col2:
    st.metric("Current Draw", f"{df['electricity_draw'].iloc[-1]:.2f} kW")
with col3:
    st.metric("Predicted Next Hour Draw", f"{mean.values[0]:.2f} kW", 
              delta=f"{mean.values[0] - df['electricity_draw'].iloc[-1]:.2f} kW")

# Visualizations
st.subheader("📊 Electricity Usage & Forecast")

# Create figure
fig = go.Figure()

# Historical Data
fig.add_trace(go.Scatter(
    x=df['timestamp'], y=df['electricity_draw'],
    name="Historical Usage",
    line=dict(color='#00d4ff', width=2)
))

# Forecast Mean
forecast_time = df['timestamp'].iloc[-1] + pd.Timedelta(hours=1)
fig.add_trace(go.Scatter(
    x=[df['timestamp'].iloc[-1], forecast_time],
    y=[df['electricity_draw'].iloc[-1], mean.values[0]],
    name="Forecast",
    line=dict(color='#ffaa00', width=3, dash='dash')
))

# Confidence Intervals
fig.add_trace(go.Scatter(
    x=[forecast_time, forecast_time],
    y=[ci.iloc[0, 0], ci.iloc[0, 1]],
    mode='lines+markers',
    name="95% CI",
    line=dict(color='#ffaa00', width=10, dash='solid'),
    opacity=0.5
))

# Fill between (for a better looking CI if we had more steps)
# But with 1 step, we just show the range bar

fig.update_layout(
    template="plotly_dark",
    xaxis_title="Time",
    yaxis_title="Electricity Draw (kW)",
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(l=20, r=20, t=50, b=20),
    height=400
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("👥 Occupancy Trends (Wi-Fi Logs)")
fig_occ = go.Figure()
fig_occ.add_trace(go.Bar(
    x=df['timestamp'], y=df['occupancy'],
    marker_color='#7c4dff',
    name="Occupancy"
))
fig_occ.update_layout(
    template="plotly_dark",
    xaxis_title="Time",
    yaxis_title="Number of People",
    margin=dict(l=20, r=20, t=20, b=20),
    height=300
)
st.plotly_chart(fig_occ, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("This dashboard uses an ARIMA model with exogenous occupancy data to provide accurate energy demand predictions.")
