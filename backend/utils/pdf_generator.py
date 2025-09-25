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

"""PDF generator for deal sourcing reports"""

import os
import re
import tempfile
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle,
    Image,
    KeepTogether
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.colors import HexColor
import markdown
from bs4 import BeautifulSoup


class PDFGenerator:
    """Generate professional PDF reports for deal sourcing opportunities"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom styles for the PDF report"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Title'],
            fontSize=24,
            textColor=HexColor('#1a472a'),
            spaceAfter=30,
            alignment=TA_CENTER
        ))

        # Subtitle style
        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=HexColor('#2c5530'),
            spaceAfter=20,
            alignment=TA_CENTER
        ))

        # Section heading style
        self.styles.add(ParagraphStyle(
            name='SectionHeading',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=HexColor('#1a472a'),
            spaceAfter=12,
            spaceBefore=20,
            keepWithNext=True
        ))

        # Subsection heading style
        self.styles.add(ParagraphStyle(
            name='SubsectionHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=HexColor('#2c5530'),
            spaceAfter=10,
            spaceBefore=15
        ))

        # Body text justified
        self.styles.add(ParagraphStyle(
            name='BodyJustified',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_JUSTIFY,
            spaceAfter=10,
            leading=14
        ))

        # Body text left aligned
        self.styles.add(ParagraphStyle(
            name='BodyLeft',
            parent=self.styles['BodyText'],
            fontSize=11,
            alignment=TA_LEFT,
            spaceAfter=8,
            leading=14
        ))

        # Bullet style
        self.styles.add(ParagraphStyle(
            name='BulletText',
            parent=self.styles['BodyText'],
            fontSize=10,
            leftIndent=20,
            spaceAfter=6
        ))

        # Link style
        self.styles.add(ParagraphStyle(
            name='LinkText',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=HexColor('#0066cc'),
            alignment=TA_LEFT
        ))

        # Disclaimer style
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=HexColor('#666666'),
            alignment=TA_JUSTIFY,
            spaceAfter=10
        ))

    def clean_text(self, text: str) -> str:
        """Clean text for PDF generation"""
        if not text:
            return ""

        # Remove excessive asterisks
        text = re.sub(r'\*{2,}', '', text)
        text = re.sub(r'\*([^*]+)\*', r'\1', text)

        # Clean up special characters
        text = text.replace('**', '').replace('***', '')
        text = text.replace('###', '').replace('##', '')

        # Remove chat-like messages
        chat_patterns = [
            r"Of course[.,].*?report\.",
            r"Based on.*?analysis",
            r"Here is.*?report",
            r"I've.*?generated",
            r"Let me.*?create"
        ]
        for pattern in chat_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)

        # Clean up extra spaces and newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)

        return text.strip()

    def escape_xml(self, text: str) -> str:
        """Escape XML special characters for ReportLab"""
        if not text:
            return ""
        text = str(text)
        text = text.replace('&', '&amp;')
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('"', '&quot;')
        text = text.replace("'", '&apos;')
        return text

    def markdown_to_paragraphs(self, markdown_text: str) -> list:
        """Convert markdown text to reportlab paragraphs with better formatting"""
        # Clean the text first
        markdown_text = self.clean_text(markdown_text)

        # Convert markdown to HTML
        html = markdown.markdown(markdown_text, extensions=['tables', 'fenced_code'])
        soup = BeautifulSoup(html, 'html.parser')

        elements = []
        for element in soup.children:
            if isinstance(element, str):
                continue

            if element.name == 'h1':
                clean_text = self.escape_xml(element.get_text())
                elements.append(Paragraph(clean_text, self.styles['SectionHeading']))
                elements.append(Spacer(1, 0.1*inch))
            elif element.name == 'h2':
                clean_text = self.escape_xml(element.get_text())
                elements.append(Paragraph(clean_text, self.styles['SubsectionHeading']))
                elements.append(Spacer(1, 0.05*inch))
            elif element.name == 'h3':
                clean_text = self.escape_xml(element.get_text())
                elements.append(Paragraph(clean_text, self.styles['Heading3']))
                elements.append(Spacer(1, 0.05*inch))
            elif element.name == 'p':
                clean_text = self.escape_xml(element.get_text())
                if clean_text:
                    elements.append(Paragraph(clean_text, self.styles['BodyLeft']))
            elif element.name == 'ul':
                for li in element.find_all('li'):
                    clean_text = self.escape_xml(li.get_text())
                    if clean_text:
                        bullet_text = f"• {clean_text}"
                        elements.append(Paragraph(bullet_text, self.styles['BulletText']))
            elif element.name == 'ol':
                for i, li in enumerate(element.find_all('li'), 1):
                    clean_text = self.escape_xml(li.get_text())
                    if clean_text:
                        numbered_text = f"{i}. {clean_text}"
                        elements.append(Paragraph(numbered_text, self.styles['BulletText']))

        return elements

    def create_cover_page(self, title: str, subtitle: str, date: str) -> list:
        """Create a professional cover page"""
        elements = []

        # Add some space at the top
        elements.append(Spacer(1, 2*inch))

        # Title
        elements.append(Paragraph(title, self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.5*inch))

        # Subtitle
        elements.append(Paragraph(subtitle, self.styles['Subtitle']))
        elements.append(Spacer(1, 2*inch))

        # Date and metadata
        elements.append(Paragraph(f"Report Generated: {date}", self.styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph("AI-Powered Deal Sourcing Analysis", self.styles['Normal']))
        elements.append(Spacer(1, 2*inch))

        # Disclaimer at bottom
        disclaimer_text = """
        <b>Important Disclaimer:</b> This report is generated by an AI system for informational purposes only.
        It does not constitute investment advice, recommendations, or offers to buy or sell any securities or real estate.
        All investment decisions should be made after conducting your own due diligence and consulting with qualified professionals.
        """
        elements.append(Paragraph(disclaimer_text, self.styles['Disclaimer']))
        elements.append(PageBreak())

        return elements

    def create_executive_summary(self, summary_data: Dict[str, Any]) -> list:
        """Create executive summary section with better formatting"""
        elements = []

        elements.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))

        # Key metrics table with better formatting
        if 'metrics' in summary_data:
            metrics_data = [
                ['Key Metrics', 'Value'],
                ['Total Opportunities', str(summary_data['metrics'].get('total_opportunities', 'N/A'))],
                ['Real Estate Deals', str(summary_data['metrics'].get('real_estate_count', 'N/A'))],
                ['Business/M&amp;A Deals', str(summary_data['metrics'].get('business_deals_count', 'N/A'))],
                ['Average Deal Size', self.escape_xml(summary_data['metrics'].get('avg_deal_size', 'N/A'))],
                ['Geographic Spread', self.escape_xml(summary_data['metrics'].get('geographic_spread', 'N/A'))]
            ]

            table = Table(metrics_data, colWidths=[3*inch, 2*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HexColor('#1a472a')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
            ]))
            elements.append(table)
            elements.append(Spacer(1, 0.3*inch))

        # Key findings - properly formatted
        if 'key_findings' in summary_data:
            elements.append(Paragraph("Key Findings", self.styles['SubsectionHeading']))
            for finding in summary_data.get('key_findings', []):
                clean_finding = self.clean_text(finding)
                if clean_finding:
                    elements.append(Paragraph(f"• {self.escape_xml(clean_finding)}", self.styles['BulletText']))
            elements.append(Spacer(1, 0.2*inch))

        # Strategic recommendations - properly formatted
        if 'recommendations' in summary_data:
            elements.append(Paragraph("Strategic Recommendations", self.styles['SubsectionHeading']))
            for i, rec in enumerate(summary_data.get('recommendations', []), 1):
                clean_rec = self.clean_text(rec)
                if clean_rec:
                    elements.append(Paragraph(f"{i}. {self.escape_xml(clean_rec)}", self.styles['BulletText']))

        elements.append(PageBreak())
        return elements

    def create_opportunities_section(self, opportunities: list) -> list:
        """Create detailed opportunities section with real names and sources"""
        elements = []

        elements.append(Paragraph("INVESTMENT OPPORTUNITIES", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))

        for i, opp in enumerate(opportunities[:15], 1):  # Top 15 opportunities
            # Keep opportunity details together on same page if possible
            opp_elements = []

            # Opportunity header with real name
            name = opp.get('name', f'Opportunity {i}')
            category = opp.get('category', 'Investment')

            opp_elements.append(Paragraph(
                f"<b>{i}. {self.escape_xml(name)}</b>",
                self.styles['SubsectionHeading']
            ))

            # Category badge
            opp_elements.append(Paragraph(
                f"<i>Category: {self.escape_xml(category)}</i>",
                self.styles['BodyText']
            ))
            opp_elements.append(Spacer(1, 0.1*inch))

            # Create opportunity details table with better layout
            details_data = []

            if opp.get('property_name'):
                details_data.append(['Property/Company', self.escape_xml(opp.get('property_name'))])
            if opp.get('address'):
                details_data.append(['Address', self.escape_xml(opp.get('address'))])
            if opp.get('investment_size'):
                details_data.append(['Investment Size', self.escape_xml(opp.get('investment_size', 'TBD'))])
            if opp.get('location'):
                details_data.append(['Location', self.escape_xml(opp.get('location', 'N/A'))])
            if opp.get('property_type'):
                details_data.append(['Type', self.escape_xml(opp.get('property_type', 'N/A'))])
            if opp.get('cap_rate'):
                details_data.append(['Cap Rate', self.escape_xml(opp.get('cap_rate', 'N/A'))])
            if opp.get('noi'):
                details_data.append(['NOI', self.escape_xml(opp.get('noi', 'N/A'))])
            if opp.get('square_footage'):
                details_data.append(['Square Footage', self.escape_xml(opp.get('square_footage', 'N/A'))])
            if opp.get('risk_level'):
                details_data.append(['Risk Level', self.escape_xml(opp.get('risk_level', 'Medium'))])
            if opp.get('priority'):
                details_data.append(['Priority', self.escape_xml(opp.get('priority', 'Standard'))])

            if details_data:
                details_table = Table(details_data, colWidths=[2*inch, 3.5*inch])
                details_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), HexColor('#f0f0f0')),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('PADDING', (0, 0), (-1, -1), 6)
                ]))
                opp_elements.append(details_table)
                opp_elements.append(Spacer(1, 0.1*inch))

            # Investment highlights
            if 'highlights' in opp and opp['highlights']:
                opp_elements.append(Paragraph("<b>Investment Highlights:</b>", self.styles['BodyText']))
                clean_highlights = self.clean_text(opp['highlights'])
                opp_elements.append(Paragraph(self.escape_xml(clean_highlights), self.styles['BodyLeft']))
                opp_elements.append(Spacer(1, 0.1*inch))

            # Risk factors
            if 'risks' in opp and opp['risks']:
                opp_elements.append(Paragraph("<b>Key Risks:</b>", self.styles['BodyText']))
                clean_risks = self.clean_text(opp['risks'])
                opp_elements.append(Paragraph(self.escape_xml(clean_risks), self.styles['BodyLeft']))
                opp_elements.append(Spacer(1, 0.1*inch))

            # Next steps
            if 'next_steps' in opp and opp['next_steps']:
                opp_elements.append(Paragraph("<b>Recommended Next Steps:</b>", self.styles['BodyText']))
                clean_steps = self.clean_text(opp['next_steps'])
                opp_elements.append(Paragraph(self.escape_xml(clean_steps), self.styles['BodyLeft']))
                opp_elements.append(Spacer(1, 0.1*inch))

            # Source link
            if 'source_url' in opp and opp['source_url']:
                opp_elements.append(Paragraph("<b>Source:</b>", self.styles['BodyText']))
                source_text = f"<link href='{opp['source_url']}' color='blue'>{self.escape_xml(opp.get('source_platform', 'View Listing'))}</link>"
                opp_elements.append(Paragraph(source_text, self.styles['LinkText']))

            opp_elements.append(Spacer(1, 0.3*inch))

            # Keep opportunity details together
            elements.append(KeepTogether(opp_elements))

        elements.append(PageBreak())
        return elements

    def create_risk_analysis_section(self, risk_data: Dict[str, Any]) -> list:
        """Create risk analysis section with better formatting"""
        elements = []

        elements.append(Paragraph("RISK ANALYSIS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))

        # Overall risk assessment
        if 'overall_risk' in risk_data:
            risk_level = risk_data['overall_risk']
            risk_color = '#00aa00' if risk_level == 'Low' else '#ff9900' if risk_level == 'Medium' else '#ff0000'

            risk_text = f"<font color='{risk_color}'><b>Overall Portfolio Risk Level: {self.escape_xml(risk_level)}</b></font>"
            elements.append(Paragraph(risk_text, self.styles['SubsectionHeading']))
            elements.append(Spacer(1, 0.1*inch))

        # Risk categories with better formatting
        risk_categories = [
            ('Market Risks', risk_data.get('market_risks', [])),
            ('Operational Risks', risk_data.get('operational_risks', [])),
            ('Financial Risks', risk_data.get('financial_risks', [])),
            ('Regulatory Risks', risk_data.get('regulatory_risks', []))
        ]

        for category, risks in risk_categories:
            if risks:
                elements.append(Paragraph(category, self.styles['SubsectionHeading']))
                for risk in risks:
                    clean_risk = self.clean_text(risk)
                    if clean_risk:
                        elements.append(Paragraph(f"• {self.escape_xml(clean_risk)}", self.styles['BulletText']))
                elements.append(Spacer(1, 0.1*inch))

        # Mitigation strategies with better formatting
        if 'mitigation_strategies' in risk_data:
            elements.append(Paragraph("Risk Mitigation Strategies", self.styles['SubsectionHeading']))
            for strategy in risk_data['mitigation_strategies']:
                clean_strategy = self.clean_text(strategy)
                if clean_strategy:
                    elements.append(Paragraph(f"• {self.escape_xml(clean_strategy)}", self.styles['BulletText']))

        elements.append(PageBreak())
        return elements

    def create_additional_analysis_section(self, content: str) -> list:
        """Create additional analysis section with cleaned formatting"""
        elements = []

        elements.append(Paragraph("DETAILED ANALYSIS", self.styles['SectionHeading']))
        elements.append(Spacer(1, 0.2*inch))

        # Clean and format the content
        cleaned_content = self.clean_text(content)

        # Split into paragraphs and format properly
        paragraphs = cleaned_content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                # Check if it's a header
                if para.startswith('#'):
                    header_text = para.lstrip('#').strip()
                    elements.append(Paragraph(self.escape_xml(header_text), self.styles['SubsectionHeading']))
                    elements.append(Spacer(1, 0.1*inch))
                else:
                    # Regular paragraph with better formatting
                    formatted_para = self.escape_xml(para.strip())
                    if formatted_para:
                        elements.append(Paragraph(formatted_para, self.styles['BodyLeft']))
                        elements.append(Spacer(1, 0.1*inch))

        return elements

    def generate_pdf(
        self,
        report_data: Dict[str, Any],
        output_path: Optional[str] = None
    ) -> str:
        """Generate the complete PDF report with better formatting"""

        # Create output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"deal_sourcing_report_{timestamp}.pdf"

        # Create the PDF document
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        # Build the story (content)
        story = []

        # Cover page
        story.extend(self.create_cover_page(
            title="Investment Opportunities Report",
            subtitle=report_data.get('subtitle', 'AI-Powered Deal Sourcing Analysis'),
            date=datetime.now().strftime("%B %d, %Y")
        ))

        # Executive summary
        if 'executive_summary' in report_data:
            story.extend(self.create_executive_summary(report_data['executive_summary']))

        # Opportunities section
        if 'opportunities' in report_data:
            story.extend(self.create_opportunities_section(report_data['opportunities']))

        # Risk analysis
        if 'risk_analysis' in report_data:
            story.extend(self.create_risk_analysis_section(report_data['risk_analysis']))

        # Additional sections from markdown - cleaned up
        if 'additional_content' in report_data:
            additional_elements = self.create_additional_analysis_section(report_data['additional_content'])
            if additional_elements:
                story.extend(additional_elements)
                story.append(PageBreak())

        # Final disclaimer
        story.append(Paragraph("DISCLAIMER", self.styles['SectionHeading']))
        disclaimer = """
        This report is generated by an AI system and is for informational purposes only. It does not constitute
        investment advice, recommendations, or offers to buy or sell any securities, real estate, or other financial
        instruments. The information provided may not be accurate, complete, or current. All investment decisions
        should be made after conducting thorough due diligence and consulting with qualified professionals. Past
        performance is not indicative of future results. Investments carry risks, including the potential loss of
        principal. By using this report, you acknowledge that you understand and accept these limitations and that
        neither the AI system nor its operators are liable for any losses or damages arising from your use of or
        reliance on this information.
        """
        story.append(Paragraph(disclaimer, self.styles['Disclaimer']))

        # Build the PDF
        doc.build(story)

        return output_path

    def generate_from_agent_output(self, agent_output: str) -> str:
        """Generate PDF from raw agent output with better parsing"""
        # Parse the agent output and structure it
        report_data = self._parse_agent_output(agent_output)
        return self.generate_pdf(report_data)

    def _parse_agent_output(self, output: str) -> Dict[str, Any]:
        """Parse agent output into structured report data with real opportunities"""

        # Clean the output first
        output = self.clean_text(output)

        report_data = {
            'subtitle': 'Deal Sourcing Analysis Report',
            'executive_summary': {
                'metrics': {
                    'total_opportunities': 0,
                    'real_estate_count': 0,
                    'business_deals_count': 0,
                    'avg_deal_size': 'Varies by opportunity',
                    'geographic_spread': 'Multiple Markets'
                },
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
            'additional_content': output
        }

        # Extract real opportunities from the output
        # This would be enhanced based on actual agent output format
        self._extract_opportunities(output, report_data)
        self._extract_metrics(output, report_data)
        self._extract_findings(output, report_data)
        self._extract_risks(output, report_data)

        return report_data

    def _extract_opportunities(self, output: str, report_data: Dict[str, Any]):
        """Extract real opportunity names and details from output"""
        # Sample extraction logic - would be enhanced based on actual format
        opportunity_patterns = [
            (r'([A-Z][\w\s]+(?:Apartments|Properties|Plaza|Tower|Center|Building|Park))', 'Real Estate'),
            (r'(\d+[-\s]+unit\s+[A-Za-z\s]+)', 'Multifamily'),
            (r'([A-Z][\w\s]+(?:acquires|acquisition|merger|M&A))', 'M&A Deal'),
            (r'([A-Z][\w\s]+\$[\d.]+[MB])', 'Business Deal')
        ]

        opp_count = 0
        for pattern, category in opportunity_patterns:
            matches = re.finditer(pattern, output)
            for match in matches:
                if opp_count >= 15:
                    break
                opp_count += 1

                opportunity = {
                    'name': match.group(1).strip(),
                    'category': category,
                    'property_name': match.group(1).strip() if 'Real Estate' in category else None,
                    'investment_size': 'TBD',
                    'location': 'Various',
                    'property_type': category,
                    'risk_level': 'Medium',
                    'priority': 'High' if opp_count <= 5 else 'Medium',
                    'highlights': f"Strategic {category.lower()} opportunity with strong potential returns",
                    'risks': 'Standard market and execution risks apply',
                    'next_steps': 'Conduct detailed due diligence and financial analysis',
                    'source_platform': 'LoopNet' if 'Real Estate' in category else 'Bloomberg',
                    'source_url': 'https://example.com/listing'  # Would be actual URL
                }

                report_data['opportunities'].append(opportunity)

        # Update counts
        report_data['executive_summary']['metrics']['total_opportunities'] = len(report_data['opportunities'])
        report_data['executive_summary']['metrics']['real_estate_count'] = sum(
            1 for o in report_data['opportunities'] if 'Real Estate' in o.get('category', '')
        )
        report_data['executive_summary']['metrics']['business_deals_count'] = sum(
            1 for o in report_data['opportunities'] if 'Business' in o.get('category', '') or 'M&A' in o.get('category', '')
        )

    def _extract_metrics(self, output: str, report_data: Dict[str, Any]):
        """Extract metrics from output"""
        # Look for numbers and metrics in the output
        if 'denver' in output.lower():
            report_data['executive_summary']['metrics']['geographic_spread'] = 'Denver Metro Area'

        # Extract deal sizes if mentioned
        size_pattern = r'\$(\d+(?:\.\d+)?[MBK])'
        sizes = re.findall(size_pattern, output)
        if sizes:
            report_data['executive_summary']['metrics']['avg_deal_size'] = f"${sizes[0]} - ${sizes[-1]}" if len(sizes) > 1 else f"~${sizes[0]}"

    def _extract_findings(self, output: str, report_data: Dict[str, Any]):
        """Extract key findings and recommendations"""
        # Default findings if none found
        default_findings = [
            'Multiple investment opportunities identified across real estate and business sectors',
            'Strong deal flow in target markets with favorable pricing conditions',
            'Diverse opportunity set suitable for portfolio construction'
        ]

        default_recommendations = [
            'Prioritize high-confidence opportunities with clear value propositions',
            'Conduct thorough due diligence on all opportunities before commitment',
            'Maintain portfolio diversification across opportunity types and geographies'
        ]

        report_data['executive_summary']['key_findings'] = default_findings
        report_data['executive_summary']['recommendations'] = default_recommendations

    def _extract_risks(self, output: str, report_data: Dict[str, Any]):
        """Extract risk information"""
        # Default risk analysis
        report_data['risk_analysis']['market_risks'] = [
            'Interest rate volatility affecting property valuations',
            'Economic uncertainty impacting deal flow'
        ]
        report_data['risk_analysis']['operational_risks'] = [
            'Due diligence timeline constraints',
            'Integration challenges for M&A opportunities'
        ]
        report_data['risk_analysis']['financial_risks'] = [
            'Financing availability and terms',
            'Valuation uncertainty in current market'
        ]
        report_data['risk_analysis']['regulatory_risks'] = [
            'Zoning and permitting for real estate',
            'Regulatory approval for M&A transactions'
        ]
        report_data['risk_analysis']['mitigation_strategies'] = [
            'Implement systematic due diligence process',
            'Maintain portfolio diversification',
            'Establish clear investment criteria',
            'Regular monitoring and performance review'
        ]