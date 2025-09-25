import { getAgentEngineEndpoint, config } from '../config';

export interface ChatMessage {
  content: string;
  timestamp: Date;
  sender: 'user' | 'agent';
}

export interface AgentEngineRequest {
  input: string;
}

export interface AgentEngineResponse {
  output?: string;
  error?: string;
}

/**
 * Call the deployed Agent Engine with proper authentication
 * Note: This implementation uses a simplified approach.
 * In production, you should implement proper OAuth2 flow or service account authentication.
 */
export async function queryAgentEngine(message: string): Promise<AgentEngineResponse> {
  try {
    // For development/demo purposes, we'll use a simplified approach
    // In production, implement proper Google Auth with OAuth2 or service accounts

    const requestBody: AgentEngineRequest = {
      input: message,
    };

    // Note: Direct calls from browser to Agent Engine require proper CORS setup
    // and authentication. Consider using a minimal backend proxy for production.

    const response = await fetch('/api/agent', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: message,
        config: {
          projectId: config.projectId,
          location: config.location,
          agentEngineId: config.agentEngineId,
        }
      }),
    });

    if (!response.ok) {
      throw new Error(`Agent Engine request failed: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();

    return {
      output: data.output || data.result || data.message || 'No response from agent',
    };

  } catch (error) {
    console.error('Agent Engine error:', error);

    // Provide helpful error messages based on the error type
    let errorMessage = 'Unknown error occurred';

    if (error instanceof TypeError && error.message.includes('fetch')) {
      errorMessage = 'Unable to connect to Agent Engine. Make sure the backend proxy is running or Agent Engine is properly deployed.';
    } else if (error instanceof Error) {
      errorMessage = error.message;
    }

    return {
      error: errorMessage,
    };
  }
}

/**
 * Format a message for display in the chat interface
 */
export function formatChatMessage(content: string, sender: 'user' | 'agent'): ChatMessage {
  return {
    content,
    timestamp: new Date(),
    sender,
  };
}