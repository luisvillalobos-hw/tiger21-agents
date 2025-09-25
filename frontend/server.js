/**
 * Express server for App Engine deployment
 * Serves the React app and provides API proxy for Agent Engine
 */

const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8080;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'dist')));

// API endpoint for Agent Engine proxy
app.post('/api/agent', async (req, res) => {
  try {
    const { message, config } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Get configuration from environment or request
    const PROJECT_ID = config?.projectId || process.env.GOOGLE_CLOUD_PROJECT || 'tiger21-demo';
    const LOCATION = config?.location || process.env.GOOGLE_CLOUD_LOCATION || 'us-central1';
    const AGENT_ENGINE_ID = config?.agentEngineId || process.env.AGENT_ENGINE_ID || '2163579398719012864';

    // Import Google Auth Library
    const { GoogleAuth } = require('google-auth-library');
    const auth = new GoogleAuth({
      scopes: ['https://www.googleapis.com/auth/cloud-platform'],
    });

    // Get access token
    const client = await auth.getClient();
    const accessToken = await client.getAccessToken();

    console.log(`Calling Agent Engine: ${AGENT_ENGINE_ID}`);

    // Use the Vertex AI SDK to properly communicate with Agent Engine
    const vertexai = require('@google-cloud/vertexai');
    const { agent_engines } = vertexai;

    // Initialize Vertex AI
    vertexai.init({
      project: PROJECT_ID,
      location: LOCATION,
    });

    // Get the deployed agent engine using the resource name from our config
    const resourceName = `projects/766839068481/locations/${LOCATION}/reasoningEngines/${AGENT_ENGINE_ID}`;

    // Get the agent engine
    const remoteAgent = agent_engines.get(resourceName);

    // Create a simple session (non-async version)
    let sessionId;
    try {
      const session = await remoteAgent.create_session({ user_id: "web_user" });
      sessionId = session.id || session.get("id");
      console.log(`Created session: ${sessionId}`);
    } catch (sessionError) {
      console.error('Session creation error:', sessionError);
      // Try without session
      sessionId = null;
    }

    // Query the agent
    let agentResponse;
    if (sessionId) {
      agentResponse = await remoteAgent.query({
        user_id: "web_user",
        session_id: sessionId,
        message: message
      });
    } else {
      // Try direct query without session
      agentResponse = await remoteAgent.query({
        input: message
      });
    }

    console.log('Agent response received:', agentResponse);

    // Return the response
    res.json({
      output: agentResponse.output || agentResponse.result || agentResponse.response || agentResponse || 'Response received from Agent Engine',
      metadata: {
        projectId: PROJECT_ID,
        location: LOCATION,
        agentEngineId: AGENT_ENGINE_ID,
        sessionId: sessionId
      }
    });

  } catch (error) {
    console.error('API error:', error);
    res.status(500).json({
      error: 'Failed to query Agent Engine',
      details: error.message,
    });
  }
});

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    environment: {
      project: process.env.GOOGLE_CLOUD_PROJECT,
      location: process.env.GOOGLE_CLOUD_LOCATION,
      agentEngineId: process.env.AGENT_ENGINE_ID,
    }
  });
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`Agent Engine ID: ${process.env.AGENT_ENGINE_ID}`);
  console.log(`Project: ${process.env.GOOGLE_CLOUD_PROJECT}`);
  console.log(`Location: ${process.env.GOOGLE_CLOUD_LOCATION}`);
});