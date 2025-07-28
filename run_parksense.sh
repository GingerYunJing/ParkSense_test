#!/bin/bash

# ParkSense Project Runner Script

echo "=== ParkSense Project Setup & Runner ==="

# Check for .env
if [ ! -f .env ]; then
  echo "WARNING: .env file not found in project root. Please create one for backend configuration."
fi

# # Start FastAPI backend
# echo "Starting FastAPI backend (http://localhost:8000)..."
# uvicorn app.main:app --host 0.0.0.0 --port 8000
echo "Starting FastAPI backend (http://localhost:8080)..."
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8080}
