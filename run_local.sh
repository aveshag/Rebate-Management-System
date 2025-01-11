#!/bin/bash

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
echo "Database name: $DB_NAME"

echo "Running alembic migration..."
alembic -c src/config/alembic.ini upgrade head

echo "Running Rebate System..."
python3 main.py
deactivate
