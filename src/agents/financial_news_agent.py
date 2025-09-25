from crewai import Agent, LLM
# Removed langchain import
from config import LLM_CONFIG

def create_financial_news_agent():
    """Create a CrewAI financial news agent for finding business deals and M&A opportunities."""

    # Use CrewAI's LLM class for proper LiteLLM integration
    llm = LLM(
        model=f"gemini/{LLM_CONFIG['simple']['model']}",  # Use gemini/ prefix for LiteLLM
        api_key=LLM_CONFIG["simple"]["api_key"],
        temperature=LLM_CONFIG["simple"]["temperature"]
    )

    return Agent(
        role="Financial News and M&A Analyst",
        goal="Discover and analyze business deals, M&A opportunities, funding rounds, and strategic partnerships",
        backstory="""You are a seasoned financial analyst with expertise in mergers & acquisitions, private equity,
        venture capital, and strategic partnerships. You have a keen eye for identifying investment opportunities
        from financial news sources including Bloomberg, Reuters, Financial Times, Wall Street Journal, and TechCrunch.
        You excel at analyzing deal terms, valuations, strategic rationales, and market trends across various industries.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=3,
        memory=False  # Disabled to avoid OpenAI embedding dependency
    )