// Configuration for the React application

interface Config {
  projectId: string;
  location: string;
  agentEngineId: string;
}

export const config: Config = {
  projectId: import.meta.env.VITE_GOOGLE_CLOUD_PROJECT || 'your-project-id',
  location: import.meta.env.VITE_GOOGLE_CLOUD_LOCATION || 'us-central1',
  agentEngineId: import.meta.env.VITE_AGENT_ENGINE_ID || 'your-agent-engine-id',
};

// Helper function to construct Agent Engine API endpoint
export const getAgentEngineEndpoint = (): string => {
  const { projectId, location, agentEngineId } = config;
  return `https://${location}-aiplatform.googleapis.com/v1/projects/${projectId}/locations/${location}/reasoningEngines/${agentEngineId}:query`;
};

export default config;