# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Deal Sourcing Coordinator: discover investment opportunities"""

import os
from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

import prompt
from agents.sub_agents.real_estate_agent import real_estate_agent
from agents.sub_agents.financial_news_agent import financial_news_agent
from agents.sub_agents.deal_coordinator_agent import deal_coordinator_agent
from agents.sub_agents.risk_analyst import risk_analyst_agent

MODEL = "gemini-2.5-pro"


deal_sourcing_coordinator = LlmAgent(
    name="deal_sourcing_coordinator",
    model=MODEL,
    description=(
        "guide users through a structured process to discover investment "
        "opportunities by orchestrating specialized search agents. help them "
        "find real estate deals, business opportunities, and financial news, "
        "then coordinate and analyze the results."
    ),
    instruction=prompt.DEAL_SOURCING_COORDINATOR_PROMPT,
    output_key="deal_sourcing_coordinator_output",
    tools=[
        AgentTool(agent=real_estate_agent),
        AgentTool(agent=financial_news_agent),
        AgentTool(agent=deal_coordinator_agent),
        AgentTool(agent=risk_analyst_agent),
    ],
)

# Check optimization settings
PARALLEL_EXECUTION = os.getenv('ENABLE_PARALLEL_EXECUTION', 'true').lower() == 'true'
PDF_ENABLED = os.getenv('ENABLE_PDF_GENERATION', 'true').lower() == 'true'
ULTRA_FAST = os.getenv('ULTRA_FAST_MODE', 'true').lower() == 'true'

# Use ultra-fast mode if enabled (combines all optimizations)
if ULTRA_FAST:
    try:
        from ultra_fast_agent import get_ultra_fast_agent
        root_agent = get_ultra_fast_agent()
    except ImportError:
        PARALLEL_EXECUTION = True  # Fallback to parallel mode

if PARALLEL_EXECUTION and 'root_agent' not in locals():
    try:
        from parallel_agent import optimized_root_agent
        root_agent = optimized_root_agent
        print("PARALLEL EXECUTION enabled - 30-50% faster deal sourcing")
    except ImportError:
        print("Parallel agent not available, falling back to standard agent")
        if PDF_ENABLED:
            try:
                from pdf_agent import deal_sourcing_coordinator_with_pdf
                root_agent = deal_sourcing_coordinator_with_pdf
                print("PDF generation enabled for deal sourcing reports")
            except ImportError:
                print("PDF dependencies not installed, using standard agent")
                root_agent = deal_sourcing_coordinator
        else:
            root_agent = deal_sourcing_coordinator
else:
    if PDF_ENABLED:
        try:
            from pdf_agent import deal_sourcing_coordinator_with_pdf
            root_agent = deal_sourcing_coordinator_with_pdf
            print("PDF generation enabled for deal sourcing reports")
        except ImportError:
            print("PDF dependencies not installed, using standard agent")
            root_agent = deal_sourcing_coordinator
    else:
        root_agent = deal_sourcing_coordinator
