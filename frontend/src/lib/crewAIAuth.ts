export interface ChatMessage {
  content: string;
  timestamp: Date;
  sender: 'user' | 'agent';
}

export interface CrewAIRequest {
  search_criteria: string;
  deal_interests?: string;
  industry_focus?: string;
}

export interface AnalysisResponse {
  status?: string;
  analysis?: string;
  error?: string;
  metadata?: {
    search_criteria: string;
    deal_interests: string;
    industry_focus: string;
    timestamp: string;
  };
}

export interface StreamUpdate {
  type: 'thinking' | 'status' | 'complete' | 'error';
  data: string;
}

/**
 * Call the analysis system with streaming
 */
export async function queryAnalysis(
  message: string,
  onUpdate: (update: StreamUpdate) => void
): Promise<AnalysisResponse> {
  try {
    // Parse the message to extract search criteria
    const requestBody: AnalysisRequest = {
      search_criteria: message,
      deal_interests: "M&A deals in technology and real estate sectors",
      industry_focus: "technology and real estate"
    };

    const response = await fetch('/api/analysis', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.status} ${response.statusText}`);
    }

    const reader = response.body?.getReader();
    if (!reader) {
      throw new Error('Stream not available');
    }

    let finalResult = '';

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = new TextDecoder().decode(value);
      const lines = chunk.split('\n');

      for (const line of lines) {
        if (line.startsWith('data: ')) {
          try {
            const data = JSON.parse(line.slice(6));
            onUpdate(data);

            if (data.type === 'complete') {
              finalResult = data.data;
            }
          } catch (e) {
            // Ignore parsing errors
          }
        }
      }
    }

    return {
      status: 'success',
      analysis: finalResult,
    };

  } catch (error) {
    console.error('Analysis error:', error);

    // Provide helpful error messages based on the error type
    let errorMessage = 'Unknown error occurred';

    if (error instanceof TypeError && error.message.includes('fetch')) {
      errorMessage = 'Unable to connect to analysis service. Make sure the backend is running.';
    } else if (error instanceof Error) {
      errorMessage = error.message;
    }

    return {
      error: errorMessage,
    };
  }
}

// Legacy interface for compatibility
export interface CrewAIRequest {
  search_criteria: string;
  deal_interests?: string;
  industry_focus?: string;
}

// New interface name
export interface AnalysisRequest {
  search_criteria: string;
  deal_interests?: string;
  industry_focus?: string;
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