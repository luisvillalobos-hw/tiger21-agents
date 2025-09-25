#!/bin/bash

# Frontend deployment script for App Engine with Agent Engine integration

# Exit on error
set -e

echo "🚀 Starting frontend deployment to App Engine..."
echo "📋 Using Agent Engine for backend processing"

# Configuration
PROJECT_ID="tiger21-demo"
LOCATION="us-central1"
AGENT_ENGINE_ID="7562269452029394944"

echo "🔧 Configuration:"
echo "  - Project: $PROJECT_ID"
echo "  - Location: $LOCATION"
echo "  - Agent Engine ID: $AGENT_ENGINE_ID"

# Build the frontend
echo "📦 Building frontend for production..."
npm run build

# Check if build succeeded
if [ $? -ne 0 ]; then
    echo "❌ Build failed!"
    exit 1
fi

echo "✅ Build successful!"

# Deploy to App Engine
echo "☁️ Deploying to App Engine..."
gcloud app deploy app.yaml --project=$PROJECT_ID --quiet

# Get the App Engine URL
APP_URL="https://${PROJECT_ID}.appspot.com"

echo "✅ Frontend deployed successfully!"
echo ""
echo "🎉 Deployment complete!"
echo "🌐 Frontend URL: $APP_URL"
echo "🤖 Agent Engine ID: $AGENT_ENGINE_ID"
echo ""
echo "📊 To view logs:"
echo "  gcloud app logs tail --project=$PROJECT_ID"
echo ""
echo "🧪 To test the Agent Engine integration:"
echo "  1. Visit $APP_URL"
echo "  2. Try asking about investment opportunities"
echo "  3. The Agent Engine will process your requests"