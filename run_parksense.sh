#!/bin/bash

# ParkSense Project Runner Script

echo "=== ParkSense Project Setup & Runner ==="

# # Check Python
# if ! command -v python3 &>/dev/null; then
#   echo "Python3 is not installed. Please install Python 3.10+."
#   exit 1
# fi

# # Check pip
# if ! command -v pip3 &>/dev/null; then
#   echo "pip3 is not installed. Please install pip for Python 3."
#   exit 1
# fi

# # Check Node.js
# if ! command -v node &>/dev/null; then
#   echo "Node.js is not installed. Please install Node.js (v18+ recommended)."
#   exit 1
# fi

# # Check npm
# if ! command -v npm &>/dev/null; then
#   echo "npm is not installed. Please install npm."
#   exit 1
# fi

# # Backend setup
# echo "Setting up Python backend..."
# python3 -m venv .venv
# source .venv/bin/activate
# pip install --upgrade pip
# pip install -r requirements.txt

# Check for .env
if [ ! -f .env ]; then
  echo "WARNING: .env file not found in project root. Please create one for backend configuration."
fi

# Start FastAPI backend
echo "Starting FastAPI backend (http://localhost:8000)..."
uvicorn app.main:app --host 0.0.0.0 --port 8000

# # Frontend setup
# echo "Setting up Next.js frontend..."
# cd parksense-frontend || { echo "Frontend directory 'parksense-frontend' not found!"; exit 1; }
# npm install

# # Check for .env
# if [ ! -f .env ]; then
#   echo "WARNING: .env file not found in parksense-frontend. Please create one for frontend configuration."
# fi

# # Start Next.js frontend
# echo "Starting Next.js frontend (http://localhost:3000)..."
# npm run dev &

# cd ..

# echo "=== ParkSense is running! ==="
# echo "- Backend:   http://localhost:8000"
# echo "- Frontend:  http://localhost:3000"
# echo ""
# echo "To stop the backend, run: kill $BACKEND_PID"
# echo "To stop the frontend, press Ctrl+C in the frontend terminal." 