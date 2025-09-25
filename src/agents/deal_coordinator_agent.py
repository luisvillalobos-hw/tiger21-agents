from crewai import Agent, LLM
# Removed langchain import
from config import LLM_CONFIG

def create_deal_coordinator_agent():
    """Create a CrewAI deal coordinator agent for synthesizing and coordinating all investment opportunities."""

    llm = LLM(
        model=f"gemini/{LLM_CONFIG['thinking']['model']}",
        api_key=LLM_CONFIG["thinking"]["api_key"],
        temperature=LLM_CONFIG["thinking"]["temperature"]
    )

    return Agent(
        role="Investment Strategy Coordinator",
        goal="Synthesize and coordinate results from real estate and financial agents to provide comprehensive investment analysis",
        backstory="""You are a strategic investment coordinator with extensive experience in portfolio management
        and cross-asset investment analysis. Your expertise lies in combining diverse investment opportunities from
        real estate and financial markets to identify the most promising deals. You excel at prioritizing opportunities,
        identifying cross-sector themes, resolving conflicts between different opportunity types, and creating
        comprehensive investment strategies that maximize portfolio diversification and return potential.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=5,
        memory=False  # Disabled to avoid OpenAI embedding dependency
    )