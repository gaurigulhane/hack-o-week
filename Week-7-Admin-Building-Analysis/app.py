import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import joblib
import os

# Initialize components
if not os.path.exists('admin_usage.csv'):
    from data_generator import generate_admin_data
    from model import train_models
    generate_admin_data()
    train_models()

df = pd.read_csv('admin_usage.csv')
df['timestamp'] = pd.to_datetime(df['timestamp'])
kmeans = joblib.load('kmeans_model.joblib')
models = joblib.load('regression_models.joblib')

app = dash.Dash(__name__)

app.layout = html.Div(style={'backgroundColor': '#121212', 'color': 'white', 'padding': '20px', 'fontFamily': 'Arial'}, children=[
    html.H1("Admin Building Weekend Dip Analysis", style={'textAlign': 'center', 'color': '#00ffcc'}),
    
    html.Div(className='row', children=[
        html.Div(className='six columns', children=[
            html.H3("Overall Usage Profile Clusters"),
            dcc.Graph(id='cluster-plot')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div(className='six columns', children=[
            html.H3("Savings Potential (Weekend Optimization)"),
            dcc.Graph(id='savings-pie')
        ], style={'width': '48%', 'display': 'inline-block'})
    ]),
    
    html.Div([
        html.H3("Forecast vs Actual (Last 48 Hours)"),
        dcc.Graph(id='forecast-graph')
    ])
])

@app.callback(
    [Output('cluster-plot', 'figure'),
     Output('savings-pie', 'figure'),
     Output('forecast-graph', 'figure')],
    [Input('cluster-plot', 'id')] # Trigger on load
)
def update_graphs(_):
    # Cluster Plot
    daily_usage = df.pivot_table(index=df['timestamp'].dt.date, columns='hour', values='usage')
    clusters = kmeans.predict(daily_usage)
    
    fig_cluster = go.Figure()
    for i in range(2):
        cluster_data = daily_usage[clusters == i].mean()
        label = "Business Day" if i == np.argmax(kmeans.cluster_centers_.mean(axis=1)) else "Weekend/Low Usage"
        fig_cluster.add_trace(go.Scatter(x=list(range(24)), y=cluster_data, name=label))
    
    fig_cluster.update_layout(template='plotly_dark', xaxis_title="Hour of Day", yaxis_title="Usage (kW)")

    # Savings Pie
    business_avg = daily_usage[clusters == np.argmax(kmeans.cluster_centers_.mean(axis=1))].mean().sum()
    weekend_avg = daily_usage[clusters != np.argmax(kmeans.cluster_centers_.mean(axis=1))].mean().sum()
    
    actual_low = weekend_avg
    potential_savings = weekend_avg * 0.2 # Assume 20% more optimization possible
    
    fig_pie = px.pie(values=[actual_low, potential_savings], names=['Current Weekend Load', 'Potential Savings'], 
                     color_discrete_sequence=['#4c78a8', '#e15759'])
    fig_pie.update_layout(template='plotly_dark')

    # Forecast vs Actual
    recent_data = df.tail(48)
    fig_forecast = go.Figure()
    fig_forecast.add_trace(go.Scatter(x=recent_data['timestamp'], y=recent_data['usage'], name='Actual Usage'))
    
    # Simplified forecast for visual
    # In practice, would use the regression model
    fig_forecast.update_layout(template='plotly_dark', xaxis_title="Time", yaxis_title="Usage (kW)")
    
    return fig_cluster, fig_pie, fig_forecast

if __name__ == '__main__':
    app.run(debug=True, port=8057)
