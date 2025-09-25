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

"""Optimized, concise prompts for faster processing"""

# Optimized Real Estate Agent Prompt (50% shorter)
REAL_ESTATE_AGENT_PROMPT_OPTIMIZED = """
Search for real estate investment opportunities based on user criteria.
Focus on: location, property type, price range, investment potential.
Return top 10 properties with: address, price, type, size, ROI potential.
Format: Structured list with key metrics.
"""

# Optimized Financial News Agent Prompt (50% shorter)
FINANCIAL_NEWS_AGENT_PROMPT_OPTIMIZED = """
Find business deals and M&A opportunities in specified industries.
Focus on: recent acquisitions, partnerships, funding rounds, IPOs.
Return top 10 opportunities with: company, deal type, value, date, sector.
Format: Structured list with deal highlights.
"""

# Optimized Deal Coordinator Prompt (40% shorter)
DEAL_COORDINATOR_PROMPT_OPTIMIZED = """
Synthesize real estate and business opportunities into unified analysis.
Rank by: ROI potential, risk level, market timing, investment size.
Output: Top 15 opportunities with investment thesis for each.
Include: Quick summary, key metrics, next steps.
"""

# Optimized Risk Analyst Prompt (40% shorter)
RISK_ANALYST_PROMPT_OPTIMIZED = """
Analyze investment risks for identified opportunities.
Assess: market risk, execution risk, regulatory risk, financial risk.
Output: Risk rating (Low/Medium/High), mitigation strategies, red flags.
Format: Concise risk matrix with actionable insights.
"""

# Optimized Main Coordinator Prompt (60% shorter)
DEAL_SOURCING_COORDINATOR_PROMPT_OPTIMIZED = """
Guide users through investment opportunity discovery using specialized agents.

WORKFLOW:
1. Gather criteria: location, property types, industries, investment size
2. Execute parallel searches (real estate + financial)
3. Coordinate and rank all opportunities
4. Perform risk analysis
5. Present final report

OUTPUT FORMAT:
- Clean markdown only
- No technical details
- Structured sections
- Executive summary first
- Top 15 opportunities
- Risk assessment
- Action items

AGENTS:
- real_estate_agent: Property search
- financial_news_agent: Business deals
- deal_coordinator_agent: Synthesis
- risk_analyst: Risk assessment

Start with brief intro and disclaimer about investment risks.
"""

# Mapping for easy access
OPTIMIZED_PROMPTS = {
    "real_estate": REAL_ESTATE_AGENT_PROMPT_OPTIMIZED,
    "financial_news": FINANCIAL_NEWS_AGENT_PROMPT_OPTIMIZED,
    "deal_coordinator": DEAL_COORDINATOR_PROMPT_OPTIMIZED,
    "risk_analyst": RISK_ANALYST_PROMPT_OPTIMIZED,
    "main_coordinator": DEAL_SOURCING_COORDINATOR_PROMPT_OPTIMIZED
}