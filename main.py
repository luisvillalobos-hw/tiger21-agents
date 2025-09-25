#!/usr/bin/env python3
"""
Main execution script for the Investment Opportunity Analysis CrewAI system.

This script runs a comprehensive analysis combining real estate and financial opportunities
using multiple specialized AI agents powered by Google's Gemini models.
"""

import os
from src.crew import InvestmentOpportunityCrew

def main():
    """Main execution function."""

    # Check for required environment variables
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY environment variable is required.")
        print("📝 Please set your Google API key in the .env file or environment.")
        return

    # Example search parameters - customize these based on your needs
    search_criteria = "multifamily properties in Austin Texas under $10M"
    deal_interests = "M&A deals in technology and real estate sectors"
    industry_focus = "technology and real estate"

    print("🏢 Investment Opportunity Analysis System")
    print("=" * 50)

    # Create and run the crew
    crew = InvestmentOpportunityCrew()

    try:
        result = crew.run_analysis(
            search_criteria=search_criteria,
            deal_interests=deal_interests,
            industry_focus=industry_focus,
            max_data_age_days_re=30,
            target_results_count_re=15,
            max_data_age_days_fn=14,
            target_results_count_fn=20
        )

        print("\n🎯 Analysis completed successfully!")
        print("📄 Check the output above for the comprehensive investment analysis report.")

    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        print("💡 Please check your API keys and network connection.")

if __name__ == "__main__":
    main()
