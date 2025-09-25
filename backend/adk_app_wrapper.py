#!/usr/bin/env python3
"""
Proper ADK App wrapper for Agent Engine deployment
"""

from vertexai import agent_engines
from deal_sourcing_agent import root_agent

# Wrap the agent in AdkApp for Agent Engine deployment
app = agent_engines.AdkApp(
    agent=root_agent,
    enable_tracing=True,
)