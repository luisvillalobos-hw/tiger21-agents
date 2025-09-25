# CrewAI Tiger21 Investment Opportunity Analysis

A sophisticated multi-agent system built with CrewAI that analyzes both real estate and financial investment opportunities using Google's Gemini AI models.

## 🚀 Features

- **Real Estate Agent**: Searches for commercial properties (multifamily, office, retail, industrial)
- **Financial News Agent**: Finds M&A deals, funding rounds, partnerships, and business opportunities
- **Deal Coordinator**: Synthesizes and prioritizes opportunities across both sectors
- **Risk Analyst**: Provides comprehensive risk analysis and professional reporting

## 🛠️ Setup

### Prerequisites

- Python 3.8+
- UV (for dependency management)
- Google Cloud Platform API access

### Installation

1. **Clone and navigate to the project**:
   ```bash
   cd /path/to/crewai-tiger21
   ```

2. **Install dependencies with UV**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

4. **Configure API keys in `.env`**:
   ```
   GOOGLE_API_KEY=your_google_gemini_api_key
   SERPER_API_KEY=your_serper_search_api_key  # Optional but recommended
   ```

### Getting API Keys

1. **Google Gemini API Key**:
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Add it to your `.env` file

2. **Serper API Key** (optional but recommended for better search):
   - Go to [Serper.dev](https://serper.dev)
   - Sign up and get your API key
   - Add it to your `.env` file

## 🏃‍♂️ Usage

### Basic Usage

Run the analysis with default parameters:

```bash
uv run python main.py
```

### Custom Analysis

Edit the parameters in `main.py` to customize your search:

```python
# Example search parameters
search_criteria = "multifamily properties in Austin Texas under $10M"
deal_interests = "M&A deals in technology and real estate sectors"
industry_focus = "technology and real estate"

# Run with custom parameters
result = crew.run_analysis(
    search_criteria=search_criteria,
    deal_interests=deal_interests,
    industry_focus=industry_focus,
    max_data_age_days_re=30,      # Real estate data freshness (days)
    target_results_count_re=15,    # Target real estate opportunities
    max_data_age_days_fn=14,      # Financial news data freshness (days)
    target_results_count_fn=20     # Target financial opportunities
)
```

### Using the InvestmentOpportunityCrew Class

```python
from src.crew import InvestmentOpportunityCrew

# Initialize the crew
crew = InvestmentOpportunityCrew()

# Run analysis
result = crew.run_analysis(
    search_criteria="office buildings in Denver under $20M",
    deal_interests="private equity acquisitions in commercial real estate",
    industry_focus="real estate and finance"
)

print(result)
```

## 🏗️ Architecture

### Agents

1. **Real Estate Agent** (`gemini-1.5-flash`)
   - Searches commercial real estate platforms
   - Analyzes property metrics (cap rates, NOI, square footage)
   - Categorizes by property type

2. **Financial News Agent** (`gemini-1.5-flash`)
   - Searches financial news sources
   - Finds M&A deals, funding rounds, partnerships
   - Analyzes deal terms and valuations

3. **Deal Coordinator** (`gemini-2.5-pro`)
   - Synthesizes results from both agents
   - Identifies cross-sector opportunities
   - Prioritizes all opportunities by attractiveness

4. **Risk Analyst** (`gemini-2.5-pro`)
   - Comprehensive risk assessment
   - Professional stakeholder reporting
   - Implementation recommendations

### Process Flow

1. **Parallel Search Phase**: Real estate and financial agents search simultaneously
2. **Coordination Phase**: Deal coordinator synthesizes and prioritizes all opportunities
3. **Risk Analysis Phase**: Risk analyst generates comprehensive final report

## 📊 Output

The system generates a comprehensive report including:

- **Executive Summary**: Key findings and recommendations
- **Top Priority Opportunities**: Ranked by investment attractiveness
- **Cross-Sector Analysis**: Geographic and industry insights
- **Risk Assessment**: Comprehensive risk analysis across all opportunities
- **Implementation Strategy**: Immediate and long-term action items
- **Due Diligence Priorities**: Research gaps and validation needs

## 🔧 Configuration

### Model Configuration

The system uses different Gemini models optimized for each task:

- **Simple tasks** (search agents): `gemini-1.5-flash` for speed and efficiency
- **Complex tasks** (coordination, risk analysis): `gemini-2.5-pro` for advanced reasoning

Edit `config.py` to modify model settings:

```python
MODELS = {
    "thinking": "gemini-2.5-pro",    # Complex analysis
    "simple": "gemini-1.5-flash",    # Search and simple tasks
}
```

### Search Tools

The system supports multiple search backends:

1. **Serper API** (recommended): Fast, reliable search results
2. **Google Custom Search**: Fallback option
3. **Basic search**: Default if no API keys provided

## 🔍 Troubleshooting

### Common Issues

1. **Missing API Keys**:
   ```
   ❌ Error: GOOGLE_API_KEY environment variable is required.
   ```
   - Ensure your `.env` file contains valid API keys

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'src'
   ```
   - Run from the project root directory
   - Ensure virtual environment is activated: `uv run python main.py`

3. **Search Limitations**:
   - Without Serper API key, search capabilities are limited
   - Consider getting a Serper API key for better results

### Performance Tips

- Use Serper API for better search results
- Adjust `target_results_count` based on your needs
- Modify `max_data_age_days` to focus on recent opportunities

## 📈 Advanced Usage

### Custom Agent Creation

```python
from src.agents import create_real_estate_agent
from src.tasks import create_real_estate_task

# Create custom agent
agent = create_real_estate_agent()

# Create custom task
task = create_real_estate_task(
    agent=agent,
    search_criteria="industrial properties in Phoenix",
    max_data_age_days=60,
    target_results_count=25
)
```

### Integration with Other Systems

The crew can be integrated into larger systems:

```python
class MyInvestmentSystem:
    def __init__(self):
        self.crew = InvestmentOpportunityCrew()

    def analyze_opportunities(self, criteria):
        return self.crew.run_analysis(**criteria)
```

## 📝 License

This project maintains the original Apache 2.0 license from the base agents.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

**Disclaimer**: This system generates AI-powered analysis for educational and informational purposes only. Always consult with qualified professionals before making investment decisions.