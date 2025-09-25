from crewai import Task
from src.tools import create_google_search_tool

def create_real_estate_task(agent, search_criteria, max_data_age_days=30, target_results_count=15):
    """Create a task for the real estate agent to find investment opportunities."""

    search_tool = create_google_search_tool()

    description = f"""
    Find comprehensive real estate investment opportunities based on the following criteria:

    Search Criteria: {search_criteria}
    Data Freshness: Focus on listings within the last {max_data_age_days} days
    Target Count: Aim for {target_results_count} distinct, high-quality property listings

    Your task is to:
    1. Perform iterative searches across commercial real estate platforms (LoopNet, CREXi, Ten-X, etc.)
    2. Focus on multifamily, office, retail, and industrial properties
    3. Gather key metrics: cap rates, NOI, square footage, occupancy rates, price per sq ft
    4. Prioritize fresh listings and investment-grade properties
    5. Analyze market trends and identify value-add opportunities

    Provide a structured report with:
    - Executive summary of market observations
    - Properties categorized by type (multifamily, office, retail, industrial)
    - Investment analysis with key metrics for each property
    - Source platforms and contact information
    - Top opportunities ranked by investment attractiveness
    """

    expected_output = """
    A comprehensive real estate investment opportunities report containing:

    **Real Estate Investment Opportunities Report**

    **Report Date:** [Current Date]
    **Search Criteria:** [Provided criteria]
    **Properties Found:** [Count] distinct properties

    **1. Executive Summary:**
    - Key market observations and trends
    - Most promising investment opportunities identified
    - Overall market conditions and timing considerations

    **2. Property Categories:**

    **Multifamily Properties:**
    - Property details with prices, cap rates, unit counts
    - NOI and investment highlights
    - Contact information and source platforms

    **Office Buildings:**
    - Property details with prices, occupancy rates
    - Square footage and tenant information
    - Investment highlights and market position

    **Retail Properties:**
    - Property details with cap rates and anchor tenants
    - Leasable square footage and market position
    - Investment potential and location advantages

    **Industrial Properties:**
    - Property details with price per square foot
    - Total square footage and key features
    - Location advantages and investment highlights

    **3. Investment Analysis:**
    - Top 10 opportunities ranked by attractiveness
    - Market insights and pricing trends
    - Value-add potential and renovation opportunities

    **4. Source Documentation:**
    - Platform listings with URLs and dates
    - Contact information for key opportunities
    - Relevance assessment for each major listing
    """

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        tools=[search_tool]
    )

def create_financial_news_task(agent, deal_interests, industry_focus="", max_data_age_days=14, target_results_count=20):
    """Create a task for the financial news agent to find business deals and M&A opportunities."""

    search_tool = create_google_search_tool()

    description = f"""
    Find comprehensive business deals and financial opportunities based on the following criteria:

    Deal Interests: {deal_interests}
    Industry Focus: {industry_focus if industry_focus else "Broad industry coverage"}
    Data Freshness: Focus on deals within the last {max_data_age_days} days
    Target Count: Aim for {target_results_count} distinct, high-quality opportunities

    Your task is to:
    1. Search financial news sources (Bloomberg, Reuters, Financial Times, WSJ, TechCrunch)
    2. Find M&A deals, private equity acquisitions, VC funding rounds, partnerships
    3. Look for IPO activity and public market transactions
    4. Gather deal terms, valuations, strategic rationales when available
    5. Identify SEC filings and material agreements
    6. Analyze market trends and transaction patterns

    Provide a structured report with:
    - Executive summary of significant deals and trends
    - Opportunities categorized by deal type
    - Financial analysis with valuations and terms
    - Market intelligence and industry insights
    - Top opportunities ranked by strategic value
    """

    expected_output = """
    A comprehensive financial news and business opportunities report containing:

    **Financial News and Business Opportunities Report**

    **Report Date:** [Current Date]
    **Deal Interests:** [Provided interests]
    **Industry Focus:** [Specified focus]
    **Opportunities Found:** [Count] distinct opportunities

    **1. Executive Summary:**
    - Most significant deals and market trends
    - Key insights about transaction activity
    - Overall market conditions and timing

    **2. Deal Categories:**

    **M&A and Acquisition Opportunities:**
    - Target and acquirer company names
    - Deal values and transaction structures
    - Strategic rationales and synergies
    - Timeline and closing conditions

    **Private Equity and Venture Capital:**
    - Company names and business descriptions
    - Funding amounts and round types
    - Lead investors and valuations
    - Use of proceeds and growth strategies

    **Strategic Partnerships:**
    - Partner company names and scope
    - Partnership objectives and terms
    - Strategic benefits and market impact

    **Public Market Opportunities:**
    - IPO and offering details
    - Company descriptions and offering sizes
    - Use of proceeds and growth plans

    **3. Market Analysis:**
    - Deal activity trends by type and sector
    - Valuation insights and pricing multiples
    - Industry hotspots and strategic themes

    **4. Investment Opportunities:**
    - Top deals ranked by strategic value
    - Market timing observations
    - Due diligence priorities

    **5. Source Documentation:**
    - News sources with URLs and dates
    - Deal announcements and SEC filings
    - Relevance assessment for each opportunity
    """

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        tools=[search_tool]
    )

def create_deal_coordination_task(agent, deal_interests="", industry_focus=""):
    """Create a task for the deal coordinator to synthesize all opportunities."""

    description = f"""
    Coordinate and synthesize results from both real estate and financial news agents to provide
    comprehensive investment analysis.

    Deal Interests: {deal_interests if deal_interests else "Broad investment focus"}
    Industry Focus: {industry_focus if industry_focus else "Multi-industry coverage"}

    Your task is to:
    1. Thoroughly analyze both real estate and financial opportunity datasets
    2. Identify overlaps and complementary opportunities between sectors
    3. Look for cross-sector investment themes and geographic concentrations
    4. Rank all opportunities by investment attractiveness
    5. Assess portfolio diversification potential
    6. Evaluate data quality and identify research gaps
    7. Provide strategic investment recommendations

    Critical Prerequisites:
    - Both real estate and financial news results must be available
    - If either dataset is missing, halt and request completion of prior steps

    Focus on:
    - Integration of real estate and business opportunities
    - Strategic analysis across asset classes
    - Risk-return optimization across opportunity types
    - Market timing and geographic considerations
    """

    expected_output = """
    A comprehensive coordinated investment opportunities analysis containing:

    **Coordinated Investment Opportunities Analysis**

    **Report Date:** [Current Date]
    **Deal Interests Scope:** [Specified or broad focus]
    **Industry Focus:** [Specified or multi-industry]
    **Total Opportunities:** [Combined count from both agents]

    **1. Executive Summary:**
    - Most compelling coordinated findings
    - Key insights about market conditions
    - Cross-sector investment themes

    **2. Top Priority Opportunities:**

    **Rank 1-5: Highest Priority**
    - Opportunity names and categories
    - Investment highlights and strategic value
    - Investment size requirements
    - Risk factors and mitigation strategies
    - Recommended next steps

    **Rank 6-10: High Priority**
    - [Same detailed structure]

    **Rank 11-15: Moderate Priority**
    - [Same detailed structure]

    **3. Cross-Sector Investment Themes:**
    - Geographic hotspots with activity in both sectors
    - Industry convergence opportunities
    - Market timing insights
    - Diversification opportunities

    **4. Investment Strategy Recommendations:**
    - Immediate action items
    - Medium-term pipeline development
    - Strategic positioning for long-term value
    - Risk management approach

    **5. Due Diligence Priorities:**
    - Critical research gaps
    - Market validation needs
    - Financial analysis requirements
    - Legal/regulatory review needs

    **6. Resource Allocation:**
    - High-impact opportunity focus
    - Quick wins identification
    - Long-term investment planning
    - Portfolio balance recommendations

    **7. Market Intelligence:**
    - Real estate market insights
    - Financial market trends
    - Competitive landscape assessment
    - Economic indicators impact

    **8. Quality Assessment:**
    - Data completeness evaluation
    - Analysis confidence levels
    - Follow-up research recommendations
    - Reporting readiness assessment
    """

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=[]  # Will be populated with outputs from previous tasks
    )

def create_risk_analysis_task(agent, deal_interests, industry_focus):
    """Create a task for the risk analyst to generate comprehensive risk analysis and final report."""

    description = f"""
    Generate a comprehensive risk analysis and professional stakeholder report for all discovered
    investment opportunities.

    Deal Interests: {deal_interests}
    Industry Focus: {industry_focus}

    Your task is to:
    1. Evaluate overall portfolio risk profile across all opportunity types
    2. Assess individual deal risks for top priority opportunities
    3. Analyze market, economic, and operational risk factors
    4. Develop risk mitigation strategies and frameworks
    5. Create actionable implementation recommendations
    6. Generate professional stakeholder-ready deliverable

    Critical Prerequisites:
    - Real estate opportunities analysis must be complete
    - Financial news opportunities analysis must be complete
    - Coordinated analysis results must be available
    - If any prerequisite is missing, halt and request completion

    Focus on:
    - Comprehensive risk assessment across asset classes
    - Portfolio optimization and diversification strategies
    - Professional reporting suitable for stakeholders
    - Actionable insights and implementation guidance
    """

    expected_output = """
    A comprehensive investment opportunities risk analysis and PDF-ready report containing:

    **INVESTMENT OPPORTUNITIES RISK ANALYSIS AND REPORT**

    **EXECUTIVE SUMMARY**
    - Investment opportunity overview by category and priority
    - Risk assessment summary with overall portfolio risk profile
    - Top 3-5 strategic recommendations for immediate consideration
    - Report confidence level and data quality assessment

    **OPPORTUNITY PORTFOLIO ANALYSIS**
    - Portfolio composition across real estate vs financial opportunities
    - Geographic and sector distribution analysis
    - Deal size distribution and investment requirements
    - Timeline urgency and market timing considerations

    **Top Priority Opportunities (Detailed Analysis):**
    - **Tier 1 (Top 5 Highest Priority):**
      - Opportunity names, categories, investment sizes
      - Strategic value propositions and competitive advantages
      - Risk-return profiles and key success factors
      - Due diligence requirements and timelines
      - Recommended portfolio allocation

    **COMPREHENSIVE RISK ANALYSIS**
    - **Market and Economic Risks:**
      - Interest rate sensitivity and economic cycle risks
      - Industry concentration and geographic risks
      - Liquidity risks and exit strategy considerations

    - **Opportunity-Specific Risks:**
      - **Real Estate Investment Risks:** Valuation, occupancy, CapEx, regulatory
      - **Financial/Business Deal Risks:** Valuation, integration, competitive, regulatory

    - **Operational and Execution Risks:**
      - Due diligence scope and timeline risks
      - Capital availability and financing risks
      - Management bandwidth and expertise requirements

    - **Risk Mitigation Strategies:**
      - Portfolio diversification recommendations
      - Due diligence protocols and checklists
      - Contingency planning and exit strategies
      - Monitoring and early warning systems

    **INVESTMENT STRATEGY AND IMPLEMENTATION**
    - **Immediate Action Items (Next 30 Days):**
      - Priority opportunities requiring immediate follow-up
      - Critical due diligence tasks and timelines
      - Key stakeholder meetings and resource allocation

    - **Medium-Term Pipeline (30-180 Days):**
      - Systematic evaluation and development opportunities
      - Market monitoring and competitive intelligence
      - Partnership development and capital preparation

    - **Long-Term Strategic Positioning (6+ Months):**
      - Portfolio optimization strategies
      - Market trend monitoring and adaptation
      - Capability building and performance measurement

    **QUALITY ASSURANCE AND DATA CONFIDENCE**
    - Source quality assessment and reliability analysis
    - Analysis confidence levels by opportunity category
    - Data gaps and limitations requiring additional research
    - Recommendations for improving analysis quality

    **PROFESSIONAL DISCLAIMER**
    "Important Disclaimer: For Educational and Informational Purposes Only.
    [Complete professional disclaimer regarding AI-generated analysis,
    investment risks, and recommendation for professional consultation]"
    """

    return Task(
        description=description,
        expected_output=expected_output,
        agent=agent,
        context=[]  # Will be populated with outputs from previous tasks
    )