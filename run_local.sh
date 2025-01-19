#!/bin/bash
set -e

PYTHON="python3"
$PYTHON -m venv venv
source venv/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Requirements installed"
echo

echo "Setting environment variables..."
# Export variables from the .env file
set -a # Automatically export all variables
source .env
set +a # Stop exporting

echo "Running Rebate System..."
PYTHON main.py
deactivate
