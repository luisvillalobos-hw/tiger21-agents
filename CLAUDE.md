# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Backend (Python/CrewAI)
- **Install dependencies**: `uv sync`
- **Run main analysis**: `uv run python main.py`
- **Test setup**: `uv run python test_setup.py`
- **Python version**: 3.12+ (using uv for dependency management)

### Root Frontend (Create React App)
- **Install**: `npm install`
- **Run development**: `npm start`
- **Build production**: `npm run build`
- **Run tests**: `npm test`

### Frontend (Vite/Express in /frontend)
- **Install**: `cd frontend && npm install`
- **Run frontend only**: `cd frontend && npm run dev`
- **Build**: `cd frontend && npm run build`
- **Deploy to Google Cloud**: `cd frontend && npm run deploy`

## Architecture

### Core System
This is a **CrewAI multi-agent investment analysis system** that combines real estate and financial opportunity sourcing. The system uses Google's Gemini AI models with different tiers for different complexity tasks:

- **Search Agents** (gemini-1.5-flash): Fast, efficient for data gathering
- **Analysis Agents** (gemini-2.5-pro): Advanced reasoning for synthesis and risk assessment

### Agent Hierarchy
1. **Real Estate Agent** (`src/agents/real_estate_agent.py`): Searches commercial properties
2. **Financial News Agent** (`src/agents/financial_news_agent.py`): Finds M&A deals, funding rounds
3. **Deal Coordinator** (`src/agents/deal_coordinator_agent.py`): Synthesizes and prioritizes all opportunities
4. **Risk Analyst** (`src/agents/risk_analyst.py`): Generates comprehensive risk reports

### Process Flow
The crew operates in **sequential mode** with context passing:
1. Real Estate and Financial agents search in parallel
2. Deal Coordinator receives context from both search agents
3. Risk Analyst receives context from all three previous agents

### Key Integration Points
- **CrewAI Framework**: Orchestrates agent collaboration via `src/crew.py:InvestmentOpportunityCrew`
- **Search Tools**: `src/tools/search_tools.py` provides Google/Serper API integration
- **Task Definitions**: `src/tasks/tasks.py` defines structured outputs for each agent
- **Model Configuration**: `config.py` manages Gemini model selection

## Environment Setup

Required environment variables in `.env`:
```
GOOGLE_API_KEY=your_google_gemini_api_key  # Required
SERPER_API_KEY=your_serper_api_key        # Optional but recommended for better search
```

## Frontend Architecture

Two separate frontend implementations:
1. **Root**: Basic Create React App (port 3000)
2. **frontend/**: Production Vite + Express app with Google Cloud deployment (port 5173)

The production frontend in `/frontend` includes:
- Express backend server for ADK agent integration
- Vite-based React UI with Tailwind CSS
- Google Cloud App Engine deployment configuration