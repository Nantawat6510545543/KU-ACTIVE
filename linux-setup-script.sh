#!/bin/bash
echo "Setting up the project environment..."

# Check if py is available, if not, check if python3 is available,
# if not, fall back to python
if command -v py &>/dev/null; then
    PYTHON_CMD="py"
elif command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

# Create and activate virtual environment
$PYTHON_CMD -m venv venv
source ./venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env file
cp sample.env .env

# Run migrations
$PYTHON_CMD manage.py migrate

# Run setup oauth
$PYTHON_CMD manage.py setup_oauth

# Load initial data
#$PYTHON_CMD manage.py loaddata data/action.json

# Run tests
$PYTHON_CMD manage.py test

# Start the server
echo "Starting the server..."
$PYTHON_CMD manage.py runserver --insecure
