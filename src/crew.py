from crewai import Crew, Process
from src.agents import (
    create_real_estate_agent,
    create_financial_news_agent,
    create_deal_coordinator_agent,
    create_risk_analyst
)
from src.tasks import (
    create_real_estate_task,
    create_financial_news_task,
    create_deal_coordination_task,
    create_risk_analysis_task
)

class InvestmentOpportunityCrew:
    """CrewAI crew for finding and analyzing investment opportunities."""

    def __init__(self):
        # Create agents
        self.real_estate_agent = create_real_estate_agent()
        self.financial_news_agent = create_financial_news_agent()
        self.deal_coordinator_agent = create_deal_coordinator_agent()
        self.risk_analyst = create_risk_analyst()

    def create_crew(self, search_criteria, deal_interests, industry_focus="",
                   max_data_age_days_re=30, target_results_count_re=15,
                   max_data_age_days_fn=14, target_results_count_fn=20):
        """Create and configure the CrewAI crew with tasks."""

        # Create tasks
        real_estate_task = create_real_estate_task(
            agent=self.real_estate_agent,
            search_criteria=search_criteria,
            max_data_age_days=max_data_age_days_re,
            target_results_count=target_results_count_re
        )

        financial_news_task = create_financial_news_task(
            agent=self.financial_news_agent,
            deal_interests=deal_interests,
            industry_focus=industry_focus,
            max_data_age_days=max_data_age_days_fn,
            target_results_count=target_results_count_fn
        )

        deal_coordination_task = create_deal_coordination_task(
            agent=self.deal_coordinator_agent,
            deal_interests=deal_interests,
            industry_focus=industry_focus
        )

        risk_analysis_task = create_risk_analysis_task(
            agent=self.risk_analyst,
            deal_interests=deal_interests,
            industry_focus=industry_focus
        )

        # Set up task dependencies
        deal_coordination_task.context = [real_estate_task, financial_news_task]
        risk_analysis_task.context = [real_estate_task, financial_news_task, deal_coordination_task]

        # Create and return the crew
        crew = Crew(
            agents=[
                self.real_estate_agent,
                self.financial_news_agent,
                self.deal_coordinator_agent,
                self.risk_analyst
            ],
            tasks=[
                real_estate_task,
                financial_news_task,
                deal_coordination_task,
                risk_analysis_task
            ],
            process=Process.sequential,
            verbose=True,
            memory=False  # Disabled to avoid OpenAI embedding dependency
        )

        return crew

    def run_analysis(self, search_criteria, deal_interests, industry_focus="",
                    max_data_age_days_re=30, target_results_count_re=15,
                    max_data_age_days_fn=14, target_results_count_fn=20):
        """Run the complete investment opportunity analysis."""

        print("🚀 Starting Investment Opportunity Analysis...")
        print(f"📍 Real Estate Search: {search_criteria}")
        print(f"💼 Deal Interests: {deal_interests}")
        print(f"🏭 Industry Focus: {industry_focus or 'Broad coverage'}")
        print("-" * 50)

        # Create the crew
        crew = self.create_crew(
            search_criteria=search_criteria,
            deal_interests=deal_interests,
            industry_focus=industry_focus,
            max_data_age_days_re=max_data_age_days_re,
            target_results_count_re=target_results_count_re,
            max_data_age_days_fn=max_data_age_days_fn,
            target_results_count_fn=target_results_count_fn
        )

        # Execute the crew
        try:
            result = crew.kickoff()
            print("\n✅ Analysis Complete!")
            print("📋 Final Risk Analysis and Report:")
            print("-" * 50)
            print(result)
            return result
        except Exception as e:
            print(f"❌ Error during analysis: {str(e)}")
            raise e