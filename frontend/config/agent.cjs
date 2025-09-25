/**
 * Centralized Agent Engine Configuration (CommonJS version)
 * Single source of truth for all Agent Engine settings
 */

// Load configuration from environment with fallbacks
const PROJECT_ID = process.env.GOOGLE_CLOUD_PROJECT || process.env.VITE_GOOGLE_CLOUD_PROJECT || 'tiger21-demo';
const LOCATION = process.env.GOOGLE_CLOUD_LOCATION || process.env.VITE_GOOGLE_CLOUD_LOCATION || 'us-central1';
const AGENT_ENGINE_ID = process.env.AGENT_ENGINE_ID || process.env.VITE_AGENT_ENGINE_ID || '7562269452029394944';

// Combined config object
const AGENT_CONFIG = {
  PROJECT_ID,
  LOCATION,
  AGENT_ENGINE_ID,
  RESOURCE_NAME: `projects/766839068481/locations/${LOCATION}/reasoningEngines/${AGENT_ENGINE_ID}`
};

module.exports = {
  PROJECT_ID,
  LOCATION,
  AGENT_ENGINE_ID,
  AGENT_CONFIG
};