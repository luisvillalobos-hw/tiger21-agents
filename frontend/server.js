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

    // Use REST API with correct format for Reasoning Engine
    const resourceName = `projects/766839068481/locations/${LOCATION}/reasoningEngines/${AGENT_ENGINE_ID}`;
    const agentEndpoint = `https://${LOCATION}-aiplatform.googleapis.com/v1/${resourceName}:query`;

    console.log(`Making request to: ${agentEndpoint}`);

    // Use the correct Agent Engine API format
    const payload = {
      "class_method": "query",
      "input": {
        "message": message
      }
    };

    console.log('Using correct payload format:', JSON.stringify(payload));

    const response = await fetch(agentEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(payload),
    });

    const agentResponse = await response.json();
    console.log('Agent Engine response:', agentResponse);

    if (!response.ok) {
      console.error('Agent Engine error:', agentResponse);
      throw new Error(agentResponse.error?.message || `Agent Engine request failed: ${response.status}`);
    }

    // Return the response
    res.json({
      output: agentResponse.output || agentResponse.result || agentResponse.response || agentResponse.predictions?.[0] || 'Response received from Agent Engine',
      metadata: {
        projectId: PROJECT_ID,
        location: LOCATION,
        agentEngineId: AGENT_ENGINE_ID,
      },
      rawResponse: agentResponse
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