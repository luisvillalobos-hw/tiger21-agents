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

// Configure static file serving with proper MIME types
app.use(express.static(path.join(__dirname, 'dist'), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.js')) {
      res.setHeader('Content-Type', 'application/javascript');
    } else if (filePath.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css');
    } else if (filePath.endsWith('.svg')) {
      res.setHeader('Content-Type', 'image/svg+xml');
    }
  }
}));

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
    const AGENT_ENGINE_ID = config?.agentEngineId || process.env.AGENT_ENGINE_ID || '7562269452029394944';

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

    // Step 1: Create a session first
    console.log('Step 1: Creating session...');
    const createSessionPayload = {
      "class_method": "async_create_session",
      "input": {
        "user_id": "web_user"
      }
    };

    console.log('Creating session with payload:', JSON.stringify(createSessionPayload));

    const sessionResponse = await fetch(agentEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(createSessionPayload),
    });

    const sessionData = await sessionResponse.json();
    console.log('Session creation response:', sessionData);

    if (!sessionResponse.ok) {
      console.error('Session creation error:', sessionData);
      throw new Error(sessionData.error?.message || `Session creation failed: ${sessionResponse.status}`);
    }

    // Extract session ID from response
    const sessionId = sessionData.output?.id || sessionData.output || sessionData.result?.id;
    console.log('Created session ID:', sessionId);

    if (!sessionId) {
      throw new Error('Failed to get session ID from response');
    }

    // Step 2: Query using streaming method (since our Agent Engine has async methods)
    console.log('Step 2: Querying with session...');
    const streamEndpoint = `https://${LOCATION}-aiplatform.googleapis.com/v1/${resourceName}:streamQuery?alt=sse`;

    const queryPayload = {
      "class_method": "async_stream_query",
      "input": {
        "user_id": "web_user",
        "session_id": sessionId,
        "message": message
      }
    };

    console.log('Querying with payload:', JSON.stringify(queryPayload));

    const queryResponse = await fetch(streamEndpoint, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(queryPayload),
    });

    console.log('Query response status:', queryResponse.status);

    if (!queryResponse.ok) {
      const errorData = await queryResponse.json();
      console.error('Query error:', errorData);
      throw new Error(errorData.error?.message || `Query failed: ${queryResponse.status}`);
    }

    // Handle the streaming response
    const responseText = await queryResponse.text();
    console.log('Raw streaming response:', responseText);

    // Parse the streaming response and extract clean text
    let finalResponse = 'Processing your request...';

    // Helper function to extract clean text from complex response objects
    const extractCleanText = (data) => {
      // If it's a string, return as is
      if (typeof data === 'string') {
        return data;
      }

      // If it's an object, look for common text fields
      if (typeof data === 'object' && data !== null) {
        // Look for text field
        if (data.text && typeof data.text === 'string') {
          return data.text;
        }

        // Look for content field
        if (data.content && typeof data.content === 'string') {
          return data.content;
        }

        // Look for message field
        if (data.message && typeof data.message === 'string') {
          return data.message;
        }

        // Look for output field
        if (data.output && typeof data.output === 'string') {
          return data.output;
        }

        // If it has parts array (common in streaming responses)
        if (data.parts && Array.isArray(data.parts)) {
          const textParts = data.parts
            .map(part => {
              if (typeof part === 'string') return part;
              if (part.text) return part.text;
              if (part.content) return part.content;
              return '';
            })
            .filter(text => text.trim() !== '');
          if (textParts.length > 0) {
            return textParts.join('\n');
          }
        }

        // Convert object to string as fallback
        return JSON.stringify(data, null, 2);
      }

      return String(data);
    };

    // Parse the streaming response (Server-Sent Events format)
    if (responseText.includes('data: ')) {
      const lines = responseText.split('\n');
      const dataLines = lines.filter(line => line.startsWith('data: '));

      let allResponses = [];

      // Process all data lines to collect streaming responses
      dataLines.forEach(line => {
        const dataContent = line.replace('data: ', '').trim();
        if (dataContent && dataContent !== '[DONE]') {
          try {
            const parsed = JSON.parse(dataContent);
            const cleanText = extractCleanText(parsed);
            if (cleanText && cleanText !== 'Processing your request...') {
              allResponses.push(cleanText);
            }
          } catch {
            // If it's not JSON, treat as plain text
            if (dataContent.length > 0) {
              allResponses.push(dataContent);
            }
          }
        }
      });

      // Join all responses or use the last one
      if (allResponses.length > 0) {
        finalResponse = allResponses.join('\n').trim();
      }
    } else {
      // If not SSE format, try to parse as JSON
      try {
        const parsed = JSON.parse(responseText);
        finalResponse = extractCleanText(parsed);
      } catch {
        // Plain text response
        finalResponse = responseText.trim();
      }
    }

    // Final cleanup - remove any JSON artifacts that might have slipped through
    if (finalResponse.includes('"content":') || finalResponse.includes('"parts":')) {
      try {
        const cleanupPattern = /.*"text":\s*"([^"]+)".*/;
        const match = finalResponse.match(cleanupPattern);
        if (match && match[1]) {
          finalResponse = match[1];
        }
      } catch {
        // Keep original if cleanup fails
      }
    }

    const agentResponse = { output: finalResponse };

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