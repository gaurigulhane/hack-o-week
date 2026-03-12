# Getting Started with SportsFacility AI

Welcome to the SportsFacility AI project! This guide will help you set up the development environment and understand the codebase.

## Project Overview
This project predicts hourly electricity usage for a sports facility using an LSTM RNN. It features a FastAPI backend and a Vanilla JS frontend.

## Prerequisites
- Python 3.8+
- Basic knowledge of FastAPI and TensorFlow/Keras

## Directory Structure
- `backend/`: Python code for data generation, model training, and API.
- `frontend/`: HTML, CSS, and JS for the interactive dashboard.
- `task.md`: Project task tracking and milestones.

## Rapid Setup
1. **Data & Model**:
   ```bash
   python3 backend/data_gen.py
   python3 backend/model.py
   ```
2. **Launch API**:
   ```bash
   uvicorn backend.main:app --port 8000
   ```
3. **Open Dashboard**:
   Simply open `frontend/index.html` in any modern web browser.

## Contributing
Please ensure all unit tests pass before submitting a pull request:
```bash
python3 backend/test_data.py
python3 backend/test_api.py
```
