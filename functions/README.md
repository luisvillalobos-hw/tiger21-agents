# Deal Sourcing Cloud Functions

This directory contains Google Cloud Functions for the Deal Sourcing application. Each agent is deployed as a separate cloud function for scalable, serverless execution.

## Functions

### 1. Financial News Agent (`financial-news-agent/`)
- **Purpose**: Analyze financial news and market trends
- **Endpoint**: `/financial-news-agent`
- **Entry Point**: `financial_news_agent`

### 2. Real Estate Agent (`real-estate-agent/`)
- **Purpose**: Find and analyze real estate investment opportunities
- **Endpoint**: `/real-estate-agent`
- **Entry Point**: `real_estate_agent`

### 3. Deal Coordinator Agent (`deal-coordinator-agent/`)
- **Purpose**: Coordinate and analyze deal opportunities across markets
- **Endpoint**: `/deal-coordinator-agent`
- **Entry Point**: `deal_coordinator_agent`

### 4. Risk Analyst Agent (`risk-analyst-agent/`)
- **Purpose**: Analyze risks and evaluate investment downsides
- **Endpoint**: `/risk-analyst-agent`
- **Entry Point**: `risk_analyst_agent`

### 5. Main Coordinator (`main-coordinator/`)
- **Purpose**: Main orchestration agent that coordinates all sub-agents
- **Endpoint**: `/main-coordinator`
- **Entry Point**: `main_coordinator`

## Deployment

### Prerequisites
- Google Cloud SDK installed and configured
- Project set up with Cloud Functions API enabled
- Appropriate IAM permissions

### Environment Variables
```bash
export GOOGLE_CLOUD_PROJECT="your-project-id"
export REGION="us-central1"  # Optional, defaults to us-central1
```

### Deploy All Functions
```bash
./deploy-all.sh
```

### Deploy Individual Function
```bash
cd <function-directory>
gcloud functions deploy <function-name> \
    --gen2 \
    --runtime=python311 \
    --region=us-central1 \
    --source=. \
    --entry-point=<entry_point> \
    --trigger=http \
    --allow-unauthenticated \
    --memory=1024MB \
    --timeout=540s
```

## API Usage

All functions expect POST requests with JSON payload:

```json
{
  "query": "Your query or request here"
}
```

Response format:
```json
{
  "agent": "agent_name",
  "query": "original_query",
  "result": "agent_response",
  "status": "success|error"
}
```

## CORS Support

All functions include CORS headers to support web frontend integration:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: POST`
- `Access-Control-Allow-Headers: Content-Type`

## Error Handling

Functions return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing query parameter)
- `500`: Internal server error

## Dependencies

Each function includes a `requirements.txt` file with:
- `functions-framework==3.*` - Google Cloud Functions framework
- `google-cloud-logging==3.*` - Cloud logging support
- `google-adk` - Google Agent Development Kit