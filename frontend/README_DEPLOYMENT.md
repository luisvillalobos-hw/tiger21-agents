# Frontend Deployment Instructions

## Prerequisites
1. Google Cloud SDK installed and configured
2. Project `tiger21-demo` created and configured
3. Agent Engine deployed (ID: 2163579398719012864)

## Deployment Steps

### 1. Initialize App Engine (if needed)
```bash
# First, make sure you're in the correct project
gcloud config set project tiger21-demo

# Create App Engine application (only needed once)
gcloud app create --region=us-central1
```

### 2. Build the Frontend
```bash
cd frontend
npm install
npm run build
```

### 3. Deploy to App Engine
```bash
# From the frontend directory
gcloud app deploy app.yaml --project=tiger21-demo
```

### 4. View Your Application
After deployment, your app will be available at:
- https://tiger21-demo.appspot.com

### 5. Monitor Logs
```bash
gcloud app logs tail --project=tiger21-demo
```

## Configuration Details

### Environment Variables
The following are configured in `app.yaml`:
- `GOOGLE_CLOUD_PROJECT`: tiger21-demo
- `GOOGLE_CLOUD_LOCATION`: us-central1
- `AGENT_ENGINE_ID`: 2163579398719012864

### Files Structure
```
frontend/
├── app.yaml           # App Engine configuration
├── server.js          # Express server for API proxy
├── package.json       # Node.js dependencies
├── dist/             # Built React app
├── src/              # React source code
└── .env              # Local environment variables
```

### API Integration
The frontend connects to Agent Engine through a server-side proxy (`server.js`) that handles:
1. Authentication with Google Cloud
2. Forwarding requests to Agent Engine
3. Returning responses to the React app

### Testing the Integration
1. Visit your deployed app
2. Try sample queries like:
   - "Find multifamily properties under $5M in Denver"
   - "Search for M&A opportunities in the technology sector"
   - "Generate a comprehensive investment report"

## Troubleshooting

### If App Engine creation fails:
1. Ensure you have the necessary permissions
2. Check if App Engine API is enabled:
   ```bash
   gcloud services enable appengine.googleapis.com
   ```

### If deployment fails:
1. Check the build output for errors
2. Verify all dependencies are installed
3. Ensure `app.yaml` is correctly configured

### If Agent Engine connection fails:
1. Verify the Agent Engine ID is correct
2. Check service account permissions
3. Review server logs for authentication issues

## Manual Deployment Alternative

If the automated deployment fails, you can also deploy manually:

1. Build locally:
   ```bash
   npm run build
   ```

2. Deploy with verbose output:
   ```bash
   gcloud app deploy app.yaml --project=tiger21-demo --verbosity=debug
   ```

3. Check deployment status:
   ```bash
   gcloud app versions list --project=tiger21-demo
   ```