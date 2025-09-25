#!/usr/bin/env python3
"""
Reasoning Engine Application wrapper for Deal Sourcing Agent
"""

from deal_sourcing_agent import root_agent

class DealSourcingApp:
    """Simple wrapper class that provides query method for Reasoning Engine"""

    def __init__(self):
        self.agent = root_agent
        self.name = "deal_sourcing_app"
        self.description = "AI-powered investment opportunity discovery agent"

    def query(self, input_text: str) -> str:
        """Query method for Reasoning Engine compatibility"""
        try:
            # ADK agents are called with the input text
            response = self.agent(input_text)

            # Handle different response types
            if hasattr(response, 'content'):
                return response.content
            elif isinstance(response, dict):
                return response.get('content', str(response))
            else:
                return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Create the app instance
app = DealSourcingApp()