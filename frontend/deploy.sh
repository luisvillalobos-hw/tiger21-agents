#!/bin/bash

# Frontend deployment script for App Engine

# Exit on error
set -e

echo "🚀 Starting frontend deployment to App Engine..."

# Get the Cloud Run backend URL
BACKEND_URL=$(gcloud run services describe deal-sourcing-backend --region=us-central1 --format='value(status.url)')

if [ -z "$BACKEND_URL" ]; then
    echo "❌ Could not get Cloud Run backend URL. Make sure the backend is deployed first."
    exit 1
fi

echo "✅ Backend URL: $BACKEND_URL"

# Build the frontend with the production API URL
echo "📦 Building frontend for production..."
VITE_API_URL=$BACKEND_URL npm run build

# Deploy to App Engine
echo "☁️ Deploying to App Engine..."
gcloud app deploy app.yaml --quiet

# Get the App Engine URL
APP_URL=$(gcloud app browse --no-launch-browser 2>&1 | grep -o 'https://[^ ]*')

echo "✅ Frontend deployed successfully!"
echo "🌐 Frontend URL: $APP_URL"
echo "🔗 Backend URL: $BACKEND_URL"

# Update the backend CORS settings
echo "🔄 Updating backend CORS settings..."
gcloud run services update deal-sourcing-backend \
    --region=us-central1 \
    --update-env-vars="FRONTEND_URL=$APP_URL" \
    --quiet

echo "🎉 Deployment complete!"
echo "Frontend: $APP_URL"
echo "Backend: $BACKEND_URL"