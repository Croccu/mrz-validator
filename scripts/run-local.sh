#!/bin/bash

# Run React frontend and Flask backend concurrently from root

# Launch backend (with venv)
echo "Starting backend..."
cd backend
source venv/bin/activate
export FLASK_APP=app.py
export FLASK_ENV=development
flask run &

# Launch frontend
echo "Starting frontend..."
cd ../frontend
npm start
