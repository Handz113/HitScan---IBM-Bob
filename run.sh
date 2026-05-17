#!/bin/bash
echo "Starting Code Analysis Demo Tool..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo ""
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo ""

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt
echo ""

# Start the server
echo "Starting FastAPI server..."
echo ""
echo "Web UI will be available at: http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
uvicorn app.main:app --reload --port 8000

# Made with Bob