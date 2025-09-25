from crewai import Agent, LLM
from config import LLM_CONFIG

def create_real_estate_agent():
    """Create a CrewAI real estate agent for finding investment opportunities."""

    # Use CrewAI's LLM class for proper LiteLLM integration
    llm = LLM(
        model=f"gemini/{LLM_CONFIG['simple']['model']}",  # Use gemini/ prefix for LiteLLM
        api_key=LLM_CONFIG["simple"]["api_key"],
        temperature=LLM_CONFIG["simple"]["temperature"]
    )

    return Agent(
        role="Real Estate Investment Specialist",
        goal="Find and analyze real estate investment opportunities across multifamily, office, retail, and industrial properties",
        backstory="""You are an experienced real estate investment analyst specializing in commercial property acquisition.
        You have deep expertise in evaluating multifamily properties, office buildings, retail spaces, and industrial properties.
        Your strength lies in identifying undervalued properties, analyzing cap rates, NOI, and market trends. You exclusively
        use search tools to find current listings on platforms like LoopNet, CREXi, and other commercial real estate platforms.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=False  # Disabled to avoid OpenAI embedding dependency
    )