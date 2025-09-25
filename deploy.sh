#!/bin/bash

# HW Deal Sourcing - Simplified Deployment Script
# Deploys agents to Agent Engine and frontend to App Engine

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}
REGION=${REGION:-"us-central1"}

echo "🚀 HW Deal Sourcing Deployment"
echo "Project: $PROJECT_ID"
echo "Region: $REGION"
echo "=================================="

# Step 1: Deploy agents to Agent Engine
echo "📡 Deploying agents to Vertex AI Agent Engine..."
cd backend/

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies with Poetry
echo "Installing Python dependencies..."
pip install poetry
poetry install --with deployment

# Deploy to Agent Engine
echo "Deploying to Agent Engine..."
python deploy_agent.py

# Check if deployment was successful
if [ ! -f "agent_engine_config.json" ]; then
    echo "❌ Agent Engine deployment failed - config file not found"
    exit 1
fi

AGENT_ENGINE_ID=$(python -c "import json; config=json.load(open('agent_engine_config.json')); print(config['agent_engine_id'])")
echo "✅ Agent Engine deployed with ID: $AGENT_ENGINE_ID"

cd ..

# Step 2: Update frontend configuration
echo "🔧 Updating frontend configuration..."
cd frontend/

# Update .env file with the deployed Agent Engine configuration
cat > .env << EOF
VITE_GOOGLE_CLOUD_PROJECT=$PROJECT_ID
VITE_GOOGLE_CLOUD_LOCATION=$REGION
VITE_AGENT_ENGINE_ID=$AGENT_ENGINE_ID
EOF

echo "✅ Frontend configuration updated"

# Step 3: Build and deploy frontend to App Engine
echo "🏗️  Building frontend..."
npm install
npm run build

echo "📤 Deploying frontend to App Engine..."
gcloud app deploy app.yaml --quiet

cd ..

echo ""
echo "🎉 Deployment completed successfully!"
echo ""
echo "📋 Summary:"
echo "- Agent Engine ID: $AGENT_ENGINE_ID"
echo "- Frontend URL: https://$PROJECT_ID.appspot.com"
echo ""
echo "🔗 Your deal sourcing application is now live!"