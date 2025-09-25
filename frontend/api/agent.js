/**
 * API proxy for Agent Engine communication
 * This runs server-side on App Engine to handle authentication
 */

import { VertexAI } from '@google-cloud/vertexai';

const PROJECT_ID = process.env.VITE_GOOGLE_CLOUD_PROJECT || 'tiger21-demo';
const LOCATION = process.env.VITE_GOOGLE_CLOUD_LOCATION || 'us-central1';
const AGENT_ENGINE_ID = process.env.VITE_AGENT_ENGINE_ID || '2163579398719012864';

// Initialize Vertex AI client
const vertexAI = new VertexAI({
  project: PROJECT_ID,
  location: LOCATION,
});

export default async function handler(req, res) {
  // Enable CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Call Agent Engine using the Vertex AI SDK
    const agentEndpoint = `projects/${PROJECT_ID}/locations/${LOCATION}/reasoningEngines/${AGENT_ENGINE_ID}`;

    // For now, we'll use a simple REST API call
    // In production, use the proper Vertex AI SDK methods
    const response = await fetch(
      `https://${LOCATION}-aiplatform.googleapis.com/v1/${agentEndpoint}:query`,
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${await getAccessToken()}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          input: message,
        }),
      }
    );

    if (!response.ok) {
      throw new Error(`Agent Engine request failed: ${response.status}`);
    }

    const data = await response.json();

    return res.status(200).json({
      output: data.output || data.result || 'Response received from Agent Engine',
    });

  } catch (error) {
    console.error('Agent Engine error:', error);
    return res.status(500).json({
      error: 'Failed to query Agent Engine',
      details: error.message,
    });
  }
}

// Helper function to get access token for authentication
async function getAccessToken() {
  // In App Engine, this will use the default service account
  try {
    const { GoogleAuth } = require('google-auth-library');
    const auth = new GoogleAuth({
      scopes: ['https://www.googleapis.com/auth/cloud-platform'],
    });
    const client = await auth.getClient();
    const tokenResponse = await client.getAccessToken();
    return tokenResponse.token;
  } catch (error) {
    console.error('Failed to get access token:', error);
    throw error;
  }
}