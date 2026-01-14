#!/bin/bash

# Bitcoin Market Analysis Dashboard Launch Script

echo "======================================"
echo "  Bitcoin Market Analysis Dashboard"
echo "======================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3.8 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "Python version: $PYTHON_VERSION"

# Check if Streamlit is installed
if ! python3 -c "import streamlit" &> /dev/null
then
    echo ""
    echo "Streamlit not found. Installing dependencies..."
    pip install -r requirements.txt
    echo ""
fi

# Launch the dashboard
echo ""
echo "Launching dashboard..."
echo "The dashboard will open in your default browser."
echo "If it doesn't open automatically, navigate to: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the dashboard."
echo ""

streamlit run dashboard.py
