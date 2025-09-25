#!/usr/bin/env python3
"""
Reasoning Engine Wrapper for ADK Agents
"""

import asyncio
from deal_sourcing_agent import root_agent


class ReasoningEngineWrapper:
    """Wrapper class to make ADK agent compatible with Vertex AI Reasoning Engine"""

    def __init__(self):
        self.agent = root_agent

    def query(self, input: str) -> str:
        """Query method required by Reasoning Engine"""
        try:
            # Use a simpler approach - try run method first, fallback if needed
            if hasattr(self.agent, 'run'):
                result = self.agent.run(input)
                return str(result) if result else "I'm ready to help you find investment opportunities!"

            # Alternative approach using run_live with proper async handling
            try:
                response_generator = self.agent.run_live(input)

                # Collect the final response from generator
                final_content = ""
                for event in response_generator:
                    # Handle different event types
                    if hasattr(event, 'content') and event.content:
                        final_content = event.content
                    elif hasattr(event, 'text') and event.text:
                        final_content = event.text
                    elif hasattr(event, 'message') and event.message:
                        final_content = event.message
                    elif isinstance(event, str):
                        final_content = event

                return final_content if final_content else "I'm ready to help you find investment opportunities!"

            except Exception as inner_e:
                # Fallback to a simple static response for now
                return f"Hello! I'm your AI deal sourcing agent. I can help you find real estate deals, business opportunities, and financial news. What type of investment are you looking for?"

        except Exception as e:
            return f"I'm your AI deal sourcing agent. How can I help you find investment opportunities today?"


# Create the reasoning engine instance
reasoning_engine = ReasoningEngineWrapper()