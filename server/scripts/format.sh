#!/bin/bash
# Code formatting script

echo "Formatting code..."

# Sort imports
isort src tests # Changed path to src tests

# Format with black
#black src tests # Changed path to src tests

echo "Code formatted!"
