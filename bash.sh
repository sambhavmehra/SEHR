#!/bin/bash

# Stop on any error
set -e

echo "Starting Python virtual environment setup..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python3 first."
    exit 1
fi

# Check if virtualenv is installed
if ! command -v virtualenv &> /dev/null; then
    echo "Installing virtualenv..."
    pip3 install virtualenv
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Create requirements.txt if it doesn't exist
if [ ! -f "requirements.txt" ]; then
    echo "Creating requirements.txt..."
    cat > requirements.txt << EOF
flask
flask-cors
web3
requests
EOF
    echo "Created requirements.txt"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

echo "Setup completed successfully!"
echo "To activate the virtual environment in the future, run: source venv/bin/activate"