#!/bin/bash

# Check if py is available, if not, check if python3 is available,
# if not, fall back to python
if command -v py &>/dev/null; then
    PYTHON_CMD="py"
elif command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

echo "Setting up the project environment..."
$PYTHON_CMD -m venv venv
source ./venv/bin/activate

echo "Install requirements.."
pip install -r requirements.txt

# Create .env file
cp sample.env .env

echo "Run migrations..."
$PYTHON_CMD manage.py migrate

echo "Run setup oauth..."
$PYTHON_CMD manage.py setup_oauth

echo "Run tests..."
$PYTHON_CMD manage.py test