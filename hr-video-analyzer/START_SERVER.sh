#!/bin/bash

# Script to start the HR Interview Analytics Platform backend server

echo "Starting HR Interview Analytics Platform Backend..."
echo ""

# Check if we're in the right directory
if [ ! -f "app.py" ]; then
    echo "Error: app.py not found. Please run this script from the hr-video-analyzer directory."
    exit 1
fi

# Find the correct Python interpreter
# Try anaconda3 first, then venv, then system python3
if [ -f "/Users/mahi/anaconda3/bin/python3" ]; then
    PYTHON="/Users/mahi/anaconda3/bin/python3"
    PIP="/Users/mahi/anaconda3/bin/pip"
elif [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    PYTHON="python3"
    PIP="pip"
else
    PYTHON="python3"
    PIP="pip3"
fi

echo "Using Python: $PYTHON"
echo "Python version: $($PYTHON --version 2>&1)"
echo ""

# Check if required packages are installed
echo "Checking dependencies..."
$PYTHON -c "import fastapi" 2>/dev/null || {
    echo "Warning: FastAPI not found. Installing dependencies..."
    $PIP install -r requirements.txt
}

# Check if uvicorn is available
if ! $PYTHON -c "import uvicorn" 2>/dev/null; then
    echo "Installing uvicorn..."
    $PIP install uvicorn[standard]
fi

# Start the server
echo ""
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop the server"
echo ""
$PYTHON -m uvicorn app:app --reload --host 0.0.0.0 --port 8000

