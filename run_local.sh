#!/bin/bash

PYTHON="python3"
$PYTHON -m venv venv
source venv/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Requirements installed"
echo

echo "Running Rebate System..."
python3 main.py
deactivate
