#!/bin/bash
# Test runner script

echo "Running tests..."

# Run linting
echo "Running flake8..."
flake8 src tests # Changed path to src tests

echo "Running mypy..."
mypy src # Changed path to src

# Run tests
echo "Running pytest..."
pytest

echo "Tests completed!"
