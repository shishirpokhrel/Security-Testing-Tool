#!/bin/bash

# Get directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check for venv
if [ -f "$DIR/venv/bin/activate" ]; then
    source "$DIR/venv/bin/activate"
else
    echo "Virtual environment not found. Please run ./run.sh first."
    exit 1
fi

echo "==================================================="
echo "Starting Security Scanner Web UI"
echo "==================================================="

# Start Backend in background
echo "Starting Backend Server..."
python "$DIR/api.py" &
BACKEND_PID=$!

# Function to kill backend on exit
cleanup() {
    echo "Stopping Backend Server (PID: $BACKEND_PID)..."
    kill $BACKEND_PID
}
trap cleanup EXIT

# Start Frontend
echo "Starting Frontend..."
cd "$DIR/frontend"

if [ ! -d "node_modules" ]; then
    echo "Node modules not found. Installing dependencies..."
    npm install
fi

echo "Starting Vite Dev Server..."
npm run dev
