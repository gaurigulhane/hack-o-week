import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from datetime import datetime, timedelta

st.set_page_config(page_title="Library Energy Forecast", layout="wide")

st.title("⚡ Library Energy Usage Forecast: Exam Periods")
st.markdown("---")

# Data Loading
@st.cache_data
def load_data():
    df = pd.read_csv('library_energy.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    cal = pd.read_csv('academic_calendar.csv')
    cal['start'] = pd.to_datetime(cal['start'])
    cal['end'] = pd.to_datetime(cal['end'])
    return df, cal

df, cal = load_data()

# Sidebar - Selection
st.sidebar.header("Forecast Settings")
selected_event = st.sidebar.selectbox("Select Exam Period to Forecast", cal['event'].unique())
event_info = cal[cal['event'] == selected_event].iloc[-1] # Get latest one

# Forecasting Logic
def get_forecast(target_start, target_end):
    # Train on everything before target_start
    train_data = df[df['timestamp'] < target_start].copy()
    train_data.set_index('timestamp', inplace=True)
    train_data = train_data.resample('h').mean().fillna(method='ffill')
    
    model = ExponentialSmoothing(
        train_data['energy_kw'],
        seasonal_periods=24,
        trend='add',
        seasonal='add',
    ).fit()
    
    # Forecast range
    forecast_dates = pd.date_range(start=target_start, end=target_end, freq='h')
    forecast = model.forecast(len(forecast_dates))
    
    # Simple CI
    residuals = train_data['energy_kw'] - model.fittedvalues
    sigma = residuals.std()
    
    return pd.DataFrame({
        'timestamp': forecast_dates,
        'forecast': forecast.values,
        'lower_ci': forecast.values - 1.96 * sigma,
        'upper_ci': forecast.values + 1.96 * sigma
    })

forecast_df = get_forecast(event_info['start'], event_info['end'])
peak_usage = forecast_df['forecast'].max()
peak_time = forecast_df.loc[forecast_df['forecast'].idxmax(), 'timestamp']

# Dashboard Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Forecasted Peak: {selected_event}")
    
    # Gauge Chart
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = peak_usage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Peak Power Consumption (kW)"},
        gauge = {
            'axis': {'range': [None, 150]},
            'steps': [
                {'range': [0, 60], 'color': "lightgray"},
                {'range': [60, 100], 'color': "yellow"},
                {'range': [100, 150], 'color': "red"}],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': peak_usage}
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    st.metric("Estimated Peak Time", peak_time.strftime('%Y-%m-%d %H:00'))
    st.info(f"The energy consumption is expected to be **{peak_usage/50:.1f}x** higher than average during this period.")

with col2:
    st.subheader("Historical vs. Forecast Trend")
    
    # Combine historical (last 14 days) and forecast
    hist_start = event_info['start'] - timedelta(days=14)
    hist_data = df[(df['timestamp'] >= hist_start) & (df['timestamp'] < event_info['start'])]
    
    fig_trend = go.Figure()
    
    # Historical
    fig_trend.add_trace(go.Scatter(
        x=hist_data['timestamp'], y=hist_data['energy_kw'],
        name='Historical', line=dict(color='blue')
    ))
    
    # Forecast
    fig_trend.add_trace(go.Scatter(
        x=forecast_df['timestamp'], y=forecast_df['forecast'],
        name='Forecast', line=dict(color='orange', dash='dash')
    ))
    
    # Confidence Interval
    fig_trend.add_trace(go.Scatter(
        x=list(forecast_df['timestamp']) + list(forecast_df['timestamp'])[::-1],
        y=list(forecast_df['upper_ci']) + list(forecast_df['lower_ci'])[::-1],
        fill='toself',
        fillcolor='rgba(255, 165, 0, 0.2)',
        line=dict(color='rgba(255, 255, 255, 0)'),
        hoverinfo="skip",
        showlegend=False
    ))
    
    fig_trend.update_layout(
        xaxis_title="Date",
        yaxis_title="Power (kW)",
        hovermode="x unified",
        template="plotly_white"
    )
    st.plotly_chart(fig_trend, use_container_width=True)

st.markdown("---")
st.subheader("Academic Calendar Overview")
st.dataframe(cal, use_container_width=True)
