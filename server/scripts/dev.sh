#!/bin/bash
# Development server startup script

echo "Starting development environment..."

# Start services with docker-compose
# docker-compose up -d db
# Env
source /home/mohrazium/Projects/WorkSpaces/zen_task_manager/server/.venv/bin/activate

# Wait for services to be ready
# echo "Waiting for services to be ready..."
# sleep 5

# # Run database migrations
# echo "Setting up database..."
# python scripts/db/init.py

# Start the development server
echo "Starting FastAPI development server..."
uvicorn src.app.main:app --reload --host 0.0.0.0 --port 8001 # Changed path to src.app.main
