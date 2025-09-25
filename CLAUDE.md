# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the HW Deal Sourcing application, an AI-powered investment opportunity discovery system built using Google ADK (Agent Development Kit). The system consists of:

- **Frontend**: React/TypeScript application deployed to Google App Engine
- **Backend**: ADK agents deployed directly to Vertex AI Agent Engine
- **Functions**: Individual Google Cloud Functions serving as specialized agents (NOT used for Agent Engine deployment)

## Architecture

The project uses a simplified two-tier architecture without Docker:

```
Frontend (React + Vite) → Vertex AI Agent Engine
     ↓ App Engine              ↓ ADK Agents
   Port 8080              (Deployed via SDK)
```

**Key Components:**
- `/frontend/` - React UI with Tailwind CSS, calls Agent Engine directly
- `/backend/` - ADK agent definitions and deployment scripts
- `/functions/` - Legacy Cloud Functions (individual agents, not used for Agent Engine)

## Development Commands

### Frontend Development
```bash
cd frontend/
npm install                    # Install dependencies
npm run dev                   # Start development server (port 5173)
npm run build                 # Build for production
npm run preview               # Preview production build (port 8080)
```

### Backend/Agent Development
```bash
cd backend/
python -m venv venv           # Create virtual environment
source venv/bin/activate      # Activate venv (Linux/Mac)
# OR: venv\Scripts\activate   # Activate venv (Windows)
poetry install                # Install Python dependencies
adk run deal_sourcing        # Test ADK agent locally
adk web                      # Launch ADK web interface
```

### Testing
```bash
cd backend/
source venv/bin/activate     # Activate venv
poetry install --with dev    # Install test dependencies
python -m pytest tests      # Run unit tests
python -m pytest eval       # Run evaluation tests
```

## Deployment Strategy

**IMPORTANT**: This project deploys WITHOUT Docker to avoid deployment errors.

### 1. Deploy Agents to Agent Engine
```bash
cd backend/
source venv/bin/activate
python deploy_agent.py  # Deploy ADK agent to Vertex AI Agent Engine
```
This creates `agent_engine_config.json` with the deployed agent configuration.

### 2. Update Frontend with Agent Engine Configuration
```bash
cd frontend/
# Update .env with Agent Engine endpoint from agent_engine_config.json
npm run build                 # Build React app with Agent Engine integration
gcloud app deploy app.yaml   # Deploy to App Engine
```

### 3. Legacy Cloud Functions (Optional)
```bash
cd functions/
./deploy-all.sh              # Deploy individual agent functions (not used for main app)
```

## Key Configuration Files

- `frontend/app.yaml` - App Engine deployment configuration
- `frontend/vite.config.ts` - Vite build configuration
- `backend/pyproject.toml` - Python dependencies and project metadata
- `backend/agent_engine_config.json` - Agent Engine deployment settings (generated)
- `functions/deploy-all.sh` - Cloud Functions deployment script

## Agent Architecture

The system implements a multi-agent pattern using ADK:

1. **Real Estate Agent** - Searches for commercial property investments
2. **Financial News Agent** - Finds M&A and business opportunities
3. **Deal Coordinator Agent** - Synthesizes and prioritizes results
4. **Risk Analyst Agent** - Generates risk assessments and PDF reports

These agents are coordinated through the ADK framework and deployed as a single Agent Engine instance.

## Environment Variables

### Frontend (.env)
```bash
VITE_GOOGLE_CLOUD_PROJECT=your-project-id
VITE_GOOGLE_CLOUD_LOCATION=your-location
VITE_AGENT_ENGINE_ID=your-agent-engine-id
```

### Backend (.env) - For Development/Deployment Only
```bash
GOOGLE_GENAI_USE_VERTEXAI=true
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
GOOGLE_CLOUD_STORAGE_BUCKET=your-staging-bucket
STAGING_BUCKET=gs://your-project-adk-staging
```

## Common Tasks

### Full Development Setup
```bash
# Test agents locally
cd backend/ && source venv/bin/activate && poetry install && adk web &

# Frontend development
cd frontend/ && npm install && npm run dev
```

### Production Deployment
```bash
# 1. Deploy agents to Agent Engine
cd backend/ && source venv/bin/activate && python deploy_agent.py

# 2. Update frontend config and deploy
cd frontend/ &&
# Copy agent_engine_id from ../backend/agent_engine_config.json to .env
npm run build && gcloud app deploy app.yaml
```

### Testing Agent Deployment
```bash
cd backend/
# Load config and test
python -c "
import json
with open('agent_engine_config.json') as f:
    config = json.load(f)
    print(f'Agent ID: {config[\"agent_engine_id\"]}')
"
```

## Important Notes

- **NO Docker** - All deployments use native cloud services (App Engine, Agent Engine)
- **Agent Engine** - Agents are deployed as a single reasoning engine, not individual functions
- **Direct Integration** - Frontend calls Agent Engine directly via Vertex AI SDK
- **Python Environment** - Uses standard Python venv and Poetry for dependency management
- **ADK Integration** - Uses Google ADK SDK for agent deployment and management