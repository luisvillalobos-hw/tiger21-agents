# Agent Engine Configuration Management

## Overview

This project now uses a centralized configuration system for Agent Engine settings. Instead of manually updating multiple files when the Agent Engine ID changes, the configuration is managed automatically.

## How It Works

### 1. Single Source of Truth
The backend `agent_engine_config.json` is the single source of truth for Agent Engine configuration.

### 2. Automatic Sync
The frontend automatically syncs configuration from the backend using a sync script.

### 3. Environment Variables
Configuration is exposed through environment variables that work in both development and production.

## Configuration Files

### Backend (Source of Truth)
- `backend/agent_engine_config.json` - Contains the deployed Agent Engine details

### Frontend (Auto-Generated)
- `frontend/.env` - Auto-synced from backend config
- `frontend/config/agent.js` - ES modules configuration
- `frontend/config/agent.cjs` - CommonJS configuration

## Usage

### Automatic Sync (Recommended)
The configuration is automatically synced before every build:

```bash
npm run build  # Automatically runs sync-config first
```

### Manual Sync
If you need to sync manually:

```bash
npm run sync-config
```

### Getting Config in Code

**Server-side (CommonJS):**
```javascript
const { AGENT_CONFIG } = require('./config/agent.cjs');
console.log('Agent ID:', AGENT_CONFIG.AGENT_ENGINE_ID);
```

**Client-side (ES Modules):**
```javascript
import { AGENT_CONFIG } from './config/agent.js';
console.log('Agent ID:', AGENT_CONFIG.AGENT_ENGINE_ID);
```

## When Agent Engine ID Changes

1. Deploy new agent to backend (updates `backend/agent_engine_config.json`)
2. Run `npm run build` in frontend (auto-syncs and rebuilds)
3. Deploy frontend

**That's it!** No need to manually update multiple files.

## Environment Variables

The system uses these environment variables:

- `VITE_GOOGLE_CLOUD_PROJECT` - GCP Project ID
- `VITE_GOOGLE_CLOUD_LOCATION` - GCP Region
- `VITE_AGENT_ENGINE_ID` - Agent Engine ID
- `GOOGLE_CLOUD_PROJECT` - Server-side project ID
- `GOOGLE_CLOUD_LOCATION` - Server-side location
- `AGENT_ENGINE_ID` - Server-side agent ID

## Benefits

✅ **Single Source of Truth** - Backend config is the authoritative source
✅ **Automatic Sync** - No manual updates needed
✅ **Build Integration** - Syncs before every build
✅ **Environment Flexibility** - Works in dev and production
✅ **Error Reduction** - No more forgetting to update files