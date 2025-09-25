# HW Deal Sourcing UI

A React frontend for the Deal Sourcing ADK Agent, providing a modern chat interface for finding investment opportunities.

## Features

- **Modern UI**: Clean, professional interface built with React and Tailwind CSS
- **Real-time Chat**: Interactive chat interface for communicating with the ADK agent
- **Quick Actions**: Pre-built buttons for common deal sourcing queries
- **Responsive Design**: Works on desktop and mobile devices
- **ADK Integration**: Direct connection to the Deal Sourcing ADK agent backend

## Prerequisites

- Node.js 18+
- Python 3.9+ (for ADK agent)
- uv (Python package manager)
- Google Cloud credentials configured

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

Copy the `.env` file and update with your Google Cloud settings:

```bash
# Update the values in .env file
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=your-project-location
```

### 3. Ensure ADK Agent is Working

From the parent directory (`../`), test that the ADK agent works:

```bash
cd ../
uv run adk run deal_sourcing
```

## Development

### Run Frontend Only
```bash
npm run dev
```
The UI will be available at `http://localhost:5173`

### Run Backend Only
```bash
npm run server:dev
```
The API will be available at `http://localhost:3001`

### Run Full Stack (Recommended)
```bash
npm run full-dev
```
This runs both frontend and backend concurrently.

## API Endpoints

- `POST /api/chat` - Send messages to the ADK agent
- `GET /api/health` - Health check endpoint

## Usage

1. Start the full development environment:
   ```bash
   npm run full-dev
   ```

2. Open your browser to `http://localhost:5173`

3. Use the chat interface to interact with the deal sourcing agent:
   - Type messages in the input field
   - Use the quick action buttons for common queries
   - Get real-time responses from the ADK agent

## Quick Action Examples

- **Real Estate Deals**: "Find multifamily properties under $5M in Denver"
- **M&A Opportunities**: "Search for M&A opportunities in the technology sector"
- **Investment Report**: "Generate a comprehensive investment report on all opportunities"

## Architecture

```
Frontend (React/Vite) → Backend (Express) → ADK Agent (Python/uv)
     ↓                      ↓                    ↓
Port 5173              Port 3001           CLI Interface
```

The React frontend sends HTTP requests to the Express backend, which spawns the ADK agent process and returns responses.

## Troubleshooting

### Backend Connection Issues
- Ensure port 3001 is available
- Check that the ADK agent path is correct in `server/server.js`
- Verify Google Cloud credentials are configured

### ADK Agent Issues
- Test the agent independently: `cd .. && uv run adk run deal_sourcing`
- Check environment variables in `.env`
- Ensure all dependencies are installed in the parent project

### Build Issues
- Clear node_modules and reinstall: `rm -rf node_modules && npm install`
- Check TypeScript configuration in `tsconfig.*.json`
