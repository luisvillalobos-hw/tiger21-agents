from crewai import Agent, LLM
# Removed langchain import
from config import LLM_CONFIG

def create_risk_analyst():
    """Create a CrewAI risk analyst for comprehensive risk evaluation and final reporting."""

    llm = LLM(
        model=f"gemini/{LLM_CONFIG['thinking']['model']}",
        api_key=LLM_CONFIG["thinking"]["api_key"],
        temperature=LLM_CONFIG["thinking"]["temperature"]
    )

    return Agent(
        role="Senior Risk Analysis and Reporting Specialist",
        goal="Provide comprehensive risk analysis of discovered investment opportunities and generate professional stakeholder-ready reports",
        backstory="""You are a senior risk analyst with deep expertise in investment risk assessment, portfolio analysis,
        and stakeholder reporting. You have extensive experience evaluating both real estate and financial market risks,
        including market timing, valuation, operational, and regulatory risks. Your strength is in synthesizing complex
        investment data into clear, actionable insights and professional reports that enable informed decision-making.
        You excel at identifying risk mitigation strategies and creating comprehensive due diligence frameworks.""",
        verbose=True,
        allow_delegation=False,
        llm=llm,
        max_iter=5,
        memory=False  # Disabled to avoid OpenAI embedding dependency
    )