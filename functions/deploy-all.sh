#!/bin/bash

# Deploy all cloud functions for the deal sourcing agents

set -e

PROJECT_ID=${GOOGLE_CLOUD_PROJECT:-$(gcloud config get-value project)}
REGION=${REGION:-"us-central1"}

echo "Deploying all deal sourcing cloud functions to project: $PROJECT_ID"
echo "Region: $REGION"
echo "=================================="

# Function to deploy a cloud function
deploy_function() {
    local function_dir=$1
    local function_name=$2
    local entry_point=$3

    echo "Deploying $function_name..."

    cd "$function_dir"

    gcloud functions deploy "$function_name" \
        --gen2 \
        --runtime=python311 \
        --region="$REGION" \
        --source=. \
        --entry-point="$entry_point" \
        --trigger-http \
        --allow-unauthenticated \
        --memory=1024MB \
        --timeout=540s \
        --set-env-vars="GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

    cd - > /dev/null

    echo "✅ $function_name deployed successfully"
    echo "URL: https://$REGION-$PROJECT_ID.cloudfunctions.net/$function_name"
    echo ""
}

# Deploy all functions
deploy_function "financial-news-agent" "financial-news-agent" "financial_news_agent"
deploy_function "real-estate-agent" "real-estate-agent" "real_estate_agent"
deploy_function "deal-coordinator-agent" "deal-coordinator-agent" "deal_coordinator_agent"
deploy_function "risk-analyst-agent" "risk-analyst-agent" "risk_analyst_agent"
deploy_function "main-coordinator" "main-coordinator" "main_coordinator"

echo "🎉 All cloud functions deployed successfully!"
echo ""
echo "Function URLs:"
echo "- Financial News Agent: https://$REGION-$PROJECT_ID.cloudfunctions.net/financial-news-agent"
echo "- Real Estate Agent: https://$REGION-$PROJECT_ID.cloudfunctions.net/real-estate-agent"
echo "- Deal Coordinator Agent: https://$REGION-$PROJECT_ID.cloudfunctions.net/deal-coordinator-agent"
echo "- Risk Analyst Agent: https://$REGION-$PROJECT_ID.cloudfunctions.net/risk-analyst-agent"
echo "- Main Coordinator: https://$REGION-$PROJECT_ID.cloudfunctions.net/main-coordinator"