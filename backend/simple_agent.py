#!/usr/bin/env python3
"""
Simplified Agent for Reasoning Engine deployment
"""

class SimpleDealSourcingAgent:
    """A simple agent class that can be deployed to Reasoning Engine"""

    def __init__(self):
        self.name = "HW Deal Sourcing Agent"
        self.description = "AI-powered investment opportunity discovery"

    def query(self, input_text: str) -> str:
        """Main query method for the agent"""
        try:
            # For now, return a simple response to test deployment
            return f"Hello! I'm the HW Deal Sourcing Agent. You asked: '{input_text}'. I'm ready to help you find investment opportunities in real estate and financial markets. The full agent functionality will be integrated once deployment is successful."

        except Exception as e:
            return f"Error processing query: {str(e)}"

# Create the agent instance
agent = SimpleDealSourcingAgent()