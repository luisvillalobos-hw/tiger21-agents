# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""PDF-enabled Deal Sourcing Coordinator"""

import os
import json
import tempfile
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from google.adk.agents import LlmAgent
from google.adk.tools.agent_tool import AgentTool

from . import prompt
from .sub_agents.real_estate_agent import real_estate_agent
from .sub_agents.financial_news_agent import financial_news_agent
from .sub_agents.deal_coordinator_agent import deal_coordinator_agent
from .sub_agents.risk_analyst import risk_analyst_agent
from .utils.pdf_generator import PDFGenerator

MODEL = "gemini-2.5-pro"


def generate_pdf_report(analysis_results: str) -> Dict[str, Any]:
    """Generate PDF from analysis results"""
    try:
        # Parse the analysis results
        pdf_generator = PDFGenerator()
        report_data = _structure_report_data(analysis_results)

        # Generate PDF
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("generated_reports")
        output_dir.mkdir(exist_ok=True)

        output_path = output_dir / f"deal_sourcing_report_{timestamp}.pdf"
        pdf_path = pdf_generator.generate_pdf(report_data, str(output_path))

        # Also create a downloadable link for web interface
        download_url = f"/download/{output_path.name}"

        return {
            "success": True,
            "pdf_path": str(pdf_path),
            "download_url": download_url,
            "message": f"PDF report generated successfully: {pdf_path}",
            "report_name": output_path.name
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to generate PDF: {str(e)}"
        }

def _structure_report_data(analysis_results: str) -> Dict[str, Any]:
        """Structure the analysis results for PDF generation"""

        # Try to extract structured data from the analysis
        report_data = {
            'subtitle': 'AI-Powered Investment Opportunity Analysis',
            'executive_summary': {
                'metrics': {},
                'key_findings': [],
                'recommendations': []
            },
            'opportunities': [],
            'risk_analysis': {
                'overall_risk': 'Medium',
                'market_risks': [],
                'operational_risks': [],
                'financial_risks': [],
                'regulatory_risks': [],
                'mitigation_strategies': []
            },
            'additional_content': analysis_results
        }

        # Parse the analysis results to extract key information
        lines = analysis_results.split('\n')
        current_section = None
        opportunity_count = 0

        for line in lines:
            line = line.strip()

            # Detect sections
            if 'EXECUTIVE SUMMARY' in line.upper():
                current_section = 'executive_summary'
            elif 'OPPORTUNITY' in line.upper() or 'OPPORTUNITIES' in line.upper():
                current_section = 'opportunities'
            elif 'RISK' in line.upper() and 'ANALYSIS' in line.upper():
                current_section = 'risk_analysis'

            # Extract metrics
            if 'Total' in line and 'opportunities' in line.lower():
                try:
                    count = int(''.join(filter(str.isdigit, line)))
                    report_data['executive_summary']['metrics']['total_opportunities'] = count
                except:
                    pass

            # Extract opportunities
            if current_section == 'opportunities' and any(x in line.lower() for x in ['property', 'deal', 'acquisition', 'm&a']):
                opportunity_count += 1
                if opportunity_count <= 15:  # Limit to top 15
                    report_data['opportunities'].append({
                        'name': f'Opportunity {opportunity_count}',
                        'category': 'Real Estate' if 'property' in line.lower() else 'Business Deal',
                        'investment_size': 'TBD',
                        'location': 'Various',
                        'type': 'Investment Opportunity',
                        'risk_level': 'Medium',
                        'priority': 'High' if opportunity_count <= 5 else 'Medium',
                        'highlights': line[:200] if len(line) > 200 else line,
                        'risks': 'Standard market and execution risks',
                        'next_steps': 'Conduct detailed due diligence'
                    })

            # Extract key findings
            if current_section == 'executive_summary' and line and len(line) > 20:
                if len(report_data['executive_summary']['key_findings']) < 5:
                    report_data['executive_summary']['key_findings'].append(line[:150])

            # Extract recommendations
            if 'recommend' in line.lower() and line:
                if len(report_data['executive_summary']['recommendations']) < 5:
                    report_data['executive_summary']['recommendations'].append(line[:150])

            # Extract risks
            if current_section == 'risk_analysis' and 'risk' in line.lower():
                if 'market' in line.lower():
                    report_data['risk_analysis']['market_risks'].append(line[:100])
                elif 'operational' in line.lower():
                    report_data['risk_analysis']['operational_risks'].append(line[:100])
                elif 'financial' in line.lower():
                    report_data['risk_analysis']['financial_risks'].append(line[:100])
                elif 'regulatory' in line.lower():
                    report_data['risk_analysis']['regulatory_risks'].append(line[:100])

        # Set default metrics if not found
        if not report_data['executive_summary']['metrics']:
            report_data['executive_summary']['metrics'] = {
                'total_opportunities': opportunity_count,
                'real_estate_count': sum(1 for o in report_data['opportunities'] if o['category'] == 'Real Estate'),
                'business_deals_count': sum(1 for o in report_data['opportunities'] if o['category'] == 'Business Deal'),
                'avg_deal_size': 'Varies by opportunity',
                'geographic_spread': 'Multiple Markets'
            }

        # Add default content if empty
        if not report_data['executive_summary']['key_findings']:
            report_data['executive_summary']['key_findings'] = [
                'Multiple investment opportunities identified across real estate and business sectors',
                'Opportunities span various risk-return profiles suitable for different investor types',
                'Market conditions favorable for selective investment deployment'
            ]

        if not report_data['executive_summary']['recommendations']:
            report_data['executive_summary']['recommendations'] = [
                'Prioritize high-confidence opportunities with clear value propositions',
                'Conduct thorough due diligence on all opportunities before commitment',
                'Diversify across opportunity types to manage portfolio risk'
            ]

        if not report_data['risk_analysis']['mitigation_strategies']:
            report_data['risk_analysis']['mitigation_strategies'] = [
                'Implement systematic due diligence process for all opportunities',
                'Maintain portfolio diversification across sectors and geographies',
                'Establish clear investment criteria and exit strategies',
                'Regular monitoring and performance review of investments'
            ]

        return report_data


# Create PDF-enabled coordinator with custom prompt
PDF_COORDINATOR_PROMPT = prompt.DEAL_SOURCING_COORDINATOR_PROMPT + """

CRITICAL OUTPUT FORMATTING RULES:

1. NEVER show raw function call outputs or error messages to the user
2. ALWAYS format agent results as clean, readable markdown text
3. Process all subagent responses and present them in a professional manner
4. Hide technical implementation details from the user

IMPORTANT WORKFLOW FOR PDF GENERATION:

After completing the risk analysis and generating the final report, you MUST follow this two-step process:

STEP 1: Display the complete analysis report in the chat interface
- Present the full analysis results to the user in a well-formatted, readable manner using clean markdown
- Process and format all subagent outputs into a cohesive, professional report
- Include all sections: Executive Summary, Investment Opportunities, Risk Analysis, and Additional Analysis
- Make sure the report is comprehensive and easy to read in the chat
- Do NOT show any raw function calls, JSON data, or technical errors

STEP 2: Ask for PDF confirmation
- After displaying the complete formatted report, ask the user: "Would you like me to generate a downloadable PDF version of this report?"
- Wait for the user's response
- ONLY if the user confirms (says "yes", "sure", "please do", etc.), then use the generate_pdf_report tool

FORMATTING GUIDELINES:
- Use proper markdown headers (# ## ###)
- Format lists with bullet points or numbers
- Use tables for structured data
- Bold important information
- Keep text clean and professional
- Remove any technical jargon or raw data dumps

The PDF should include:
1. Executive Summary with key metrics and findings
2. Detailed analysis of top 15 opportunities
3. Risk assessment and mitigation strategies
4. Professional formatting and visualization
5. Complete disclaimer and legal notices

When the PDF is generated, provide the user with:
- Confirmation that the PDF was created successfully
- The download link or path to access the PDF
- Brief summary of what's included in the report

This ensures users can review the report first and only generate the PDF if they actually want it.
"""

deal_sourcing_coordinator_with_pdf = LlmAgent(
    name="deal_sourcing_coordinator_pdf",
    model=MODEL,
    description=(
        "guide users through a structured process to discover investment "
        "opportunities by orchestrating specialized search agents. help them "
        "find real estate deals, business opportunities, and financial news, "
        "then coordinate and analyze the results, finally generating a downloadable PDF report."
    ),
    instruction=PDF_COORDINATOR_PROMPT,
    output_key="deal_sourcing_coordinator_output",
    tools=[
        AgentTool(agent=real_estate_agent),
        AgentTool(agent=financial_news_agent),
        AgentTool(agent=deal_coordinator_agent),
        AgentTool(agent=risk_analyst_agent),
        generate_pdf_report
    ],
)

# Make this the root agent for PDF-enabled version
root_agent = deal_sourcing_coordinator_with_pdf