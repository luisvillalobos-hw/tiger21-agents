from crewai_tools import SerperDevTool
from langchain_community.tools import GoogleSearchRun
from langchain_community.utilities import GoogleSearchAPIWrapper
import os

def create_google_search_tool():
    """Create a Google search tool for CrewAI agents."""
    # Try SerperDevTool first (if API key is available)
    if os.getenv("SERPER_API_KEY"):
        return SerperDevTool()

    # Fallback to Google Search API (requires GOOGLE_API_KEY and GOOGLE_CSE_ID)
    if os.getenv("GOOGLE_API_KEY") and os.getenv("GOOGLE_CSE_ID"):
        search = GoogleSearchAPIWrapper(
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            google_cse_id=os.getenv("GOOGLE_CSE_ID")
        )
        return GoogleSearchRun(api_wrapper=search)

    # If no search API keys are available, return SerperDevTool anyway
    # (user will need to configure API keys)
    return SerperDevTool()