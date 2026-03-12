from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import joblib
import numpy as np
import asyncio
from datetime import datetime
import json
import os

app = FastAPI()

# Load the trained model
MODEL_PATH = "models/cafeteria_model.joblib"
model = None
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)

# Serve static files
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/predict")
async def predict(temp: float, humidity: float, hour: float):
    if model is None:
        return {"error": "Model not found"}
    
    features = np.array([[temp, humidity, hour]])
    prediction = model.predict(features)[0]
    return {"predicted_load": round(float(prediction), 2)}

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

async def simulate_occupancy():
    """Simulates real-time occupancy changes and broadcasts them."""
    while True:
        now = datetime.now()
        hour = now.hour + now.minute / 60.0
        
        # Simulate current weather
        temp = 25 + np.sin(hour / 24 * 2 * np.pi) * 5
        humidity = 50 + np.cos(hour / 24 * 2 * np.pi) * 10
        
        if model:
            features = np.array([[temp, humidity, hour]])
            prediction = model.predict(features)[0]
            # Add some randomness to actual load
            actual_load = max(0, prediction + np.random.normal(0, 2))
        else:
            actual_load = 0
            prediction = 0

        data = {
            "time": now.strftime("%H:%M:%S"),
            "actual_load": round(float(actual_load), 1),
            "predicted_load": round(float(prediction), 1),
            "temperature": round(temp, 1),
            "humidity": round(humidity, 1)
        }
        
        await manager.broadcast(json.dumps(data))
        await asyncio.sleep(2) # Update every 2 seconds for demo

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(simulate_occupancy())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
