#!/bin/bash

# Exit on error
set -e

echo "Installing test dependencies..."
pip install -r dev-requirements.txt

echo "Running tests..."
# Set PYTHONPATH to include the project root directory
export PYTHONPATH=$PYTHONPATH:$(pwd)
pytest

echo "Tests completed successfully!"