#!/bin/bash

# Build frontend, move to backend, and deploy to Heroku
echo "Building frontend..."
cd frontend
npm run build

echo "Copying build to backend..."
cd ..
rm -rf backend/build
cp -r frontend/build backend/build

echo "Deploying to Heroku..."
cd backend
git add .
git commit -m "Automated deploy: update frontend build"
git push heroku master
echo "Deployment complete!"
