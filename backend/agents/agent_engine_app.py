#!/usr/bin/env python3
"""
Agent Engine Application Entry Point for HW Deal Sourcing Agent
"""

import sys
import os

# Add parent directory to path to import from root level
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import the root agent from deal_sourcing_agent
from deal_sourcing_agent import root_agent

# Export the root_agent for Agent Engine
app = root_agent