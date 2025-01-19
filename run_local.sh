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
echo "Database name: $DB_NAME"

# Checking for DB connection
if ! nc -z $DB_HOST $DB_PORT; then
    echo "Error: Unable to connect to the database at $DB_HOST:$DB_PORT."
    echo "Ensure the database pod is up and accessible before running this script."
    deactivate
    exit 1
fi
echo "Database connection successful."

echo "Running alembic migration..."
alembic -c src/config/alembic.ini upgrade head

echo "Running Rebate System..."
PYTHON main.py
deactivate
