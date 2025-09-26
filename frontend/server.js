/**
 * Express server for App Engine deployment
 * Serves the React app and provides API proxy for CrewAI analysis
 */

const express = require('express');
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = process.env.PORT || 8080;

// Middleware
app.use(cors());
app.use(express.json());

// Configure static file serving with proper MIME types
app.use(express.static(path.join(__dirname, 'dist'), {
  setHeaders: (res, filePath) => {
    if (filePath.endsWith('.js')) {
      res.setHeader('Content-Type', 'application/javascript');
    } else if (filePath.endsWith('.css')) {
      res.setHeader('Content-Type', 'text/css');
    } else if (filePath.endsWith('.svg')) {
      res.setHeader('Content-Type', 'image/svg+xml');
    }
  }
}));

// API endpoint for streaming analysis
app.post('/api/analysis', async (req, res) => {
  try {
    const { search_criteria, deal_interests, industry_focus } = req.body;

    if (!search_criteria) {
      return res.status(400).json({ error: 'search_criteria is required' });
    }

    console.log('Starting analysis...');

    // Set up Server-Sent Events
    res.writeHead(200, {
      'Content-Type': 'text/event-stream',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Cache-Control'
    });

    // Import child_process to run the analysis system
    const { spawn } = require('child_process');

    // Path to the analysis system
    const analysisPath = '/Volumes/ExternalSSD2/hw/crewai-tiger21';

    const analysisProcess = spawn('uv', ['run', 'python', 'main.py'], {
      cwd: analysisPath,
      env: {
        ...process.env,
        SEARCH_CRITERIA: search_criteria,
        DEAL_INTERESTS: deal_interests || 'M&A deals in technology and real estate sectors',
        INDUSTRY_FOCUS: industry_focus || 'technology and real estate'
      }
    });

    let fullOutput = '';
    let currentThinking = '';
    let currentStep = '';

    // Function to send stream updates
    const sendUpdate = (type, data) => {
      res.write(`data: ${JSON.stringify({ type, data })}\n\n`);
    };

    // Send initial status
    sendUpdate('status', 'Starting analysis...');

    analysisProcess.stdout.on('data', (data) => {
      const output = data.toString();
      fullOutput += output;

      // Parse and extract meaningful updates for the user
      const lines = output.split('\n');

      for (const line of lines) {
        if (line.trim()) {
          // Extract agent activities
          if (line.includes('Agent: ')) {
            const agent = line.split('Agent: ')[1]?.split(' │')[0] || 'Agent';
            currentStep = `${agent} is analyzing...`;
            sendUpdate('thinking', currentStep);
          }

          // Extract search activities
          if (line.includes('Using Tool: Search')) {
            sendUpdate('thinking', 'Searching for opportunities...');
          }

          if (line.includes('search_query')) {
            try {
              const searchMatch = line.match(/"search_query":\s*"([^"]+)"/);
              if (searchMatch) {
                sendUpdate('thinking', `Searching: ${searchMatch[1]}`);
              }
            } catch (e) {
              // Ignore parsing errors
            }
          }

          // Extract task completion
          if (line.includes('✅ Completed')) {
            sendUpdate('thinking', 'Task completed, moving to next agent...');
          }

          // Extract final analysis
          if (line.includes('Final Answer:') || line.includes('INVESTMENT OPPORTUNITIES')) {
            sendUpdate('thinking', 'Generating final report...');
          }
        }
      }
    });

    analysisProcess.stderr.on('data', (data) => {
      console.error('Analysis error:', data.toString());
    });

    analysisProcess.on('close', (code) => {
      if (code === 0) {
        // Clean and format the final output
        const cleanedOutput = cleanOutput(fullOutput);
        sendUpdate('complete', cleanedOutput);
      } else {
        sendUpdate('error', 'Analysis failed. Please try again.');
      }
      res.end();
    });

    // Set a timeout for the process (10 minutes)
    setTimeout(() => {
      analysisProcess.kill();
      sendUpdate('error', 'Analysis timed out. Please try with a more specific query.');
      res.end();
    }, 10 * 60 * 1000);

  } catch (error) {
    console.error('Analysis API error:', error);
    res.write(`data: ${JSON.stringify({ type: 'error', data: 'Failed to start analysis' })}\n\n`);
    res.end();
  }
});

// Function to clean and format the output
function cleanOutput(rawOutput) {
  let cleaned = rawOutput;

  // Remove all debug UI elements and unwanted content
  cleaned = cleaned.replace(/╭[─┐┘└╯╮│]*╯/g, '');
  cleaned = cleaned.replace(/│[^│]*│/g, '');
  cleaned = cleaned.replace(/└[─┐┘└╯╮]*╯/g, '');
  cleaned = cleaned.replace(/🚀 Crew: crew[\s\S]*?(?=\n)/g, '');
  cleaned = cleaned.replace(/📋 Task: [a-f0-9-]+[\s\S]*?(?=\n)/g, '');
  cleaned = cleaned.replace(/Status: [^\n]*/g, '');
  cleaned = cleaned.replace(/🔧 Used Search[^\n]*/g, '');
  cleaned = cleaned.replace(/Assigned to: [^\n]*/g, '');
  cleaned = cleaned.replace(/├──[^\n]*/g, '');
  cleaned = cleaned.replace(/└──[^\n]*/g, '');
  cleaned = cleaned.replace(/nternet with Serper[^\n]*/g, '');

  // Remove any M&A or financial news content
  cleaned = cleaned.replace(/Financial News and Business Opportunities Report[\s\S]*?(?=\n\n|$)/g, '');
  cleaned = cleaned.replace(/Deal Interests: M&A deals[^\n]*/g, '');
  cleaned = cleaned.replace(/Industry Focus: technology and real estate[^\n]*/g, '');
  cleaned = cleaned.replace(/M&A[\s\S]*?(?=\n\n|$)/g, '');
  cleaned = cleaned.replace(/merger[^\n]*/gi, '');
  cleaned = cleaned.replace(/acquisition[^\n]*/gi, '');
  cleaned = cleaned.replace(/private equity[^\n]*/gi, '');
  cleaned = cleaned.replace(/venture capital[^\n]*/gi, '');

  // Remove additional debug elements
  cleaned = cleaned.replace(/\[.*?\]/g, ''); // Remove bracketed debug info
  cleaned = cleaned.replace(/Agent: [^\n]*/g, ''); // Remove agent debug lines
  cleaned = cleaned.replace(/Using Tool: [^\n]*/g, ''); // Remove tool usage lines
  cleaned = cleaned.replace(/Thought: [^\n]*/g, ''); // Remove thought lines
  cleaned = cleaned.replace(/Action: [^\n]*/g, ''); // Remove action lines
  cleaned = cleaned.replace(/Observation: [^\n]*/g, ''); // Remove observation lines

  // Extract the final answer/report
  let finalContent = '';

  // Look for the coordinator's final answer first
  const coordinatorMatch = cleaned.match(/Final Answer:\s*([\s\S]*?)(?=\n\n✅|$)/);
  if (coordinatorMatch) {
    finalContent = coordinatorMatch[1].trim();
  } else {
    // Look for multifamily content specifically
    const multifamilyMatch = cleaned.match(/Multifamily[\s\S]*?(?=\n\n\n|$)/);
    if (multifamilyMatch) {
      finalContent = multifamilyMatch[0].trim();
    } else {
      // Fallback: get meaningful content from the end
      const lines = cleaned.split('\n').filter(line => {
        const lower = line.toLowerCase();
        return line.trim() &&
          !line.includes('═') &&
          !line.includes('─') &&
          !line.includes('🚀') &&
          !line.includes('📋') &&
          !line.includes('╭') &&
          !line.includes('│') &&
          !line.includes('└') &&
          !line.includes('nternet') &&
          !line.includes('Assigned to') &&
          !line.includes('Status:') &&
          !lower.includes('debug') &&
          !lower.includes('error') &&
          !lower.includes('warning');
      });
      finalContent = lines.slice(-50).join('\n');
    }
  }

  // Clean up any remaining artifacts
  finalContent = finalContent.replace(/\*\*\s*\n\s*/g, '**');
  finalContent = finalContent.replace(/\n\s*\n\s*\n/g, '\n\n');
  finalContent = finalContent.replace(/^\s*\n+/, ''); // Remove leading whitespace and newlines
  finalContent = finalContent.trim();

  // If the content is still not clean or too short, provide a fallback
  if (finalContent.length < 100 || finalContent.includes('╭') || finalContent.includes('│')) {
    finalContent = 'Analysis completed. The multifamily investment opportunities search has finished. Please check the thinking process above for detailed findings.';
  }

  return formatMarkdown(finalContent);
}

// Function to format markdown for display with professional memo formatting
function formatMarkdown(text) {
  let formatted = text;

  // Remove markdown artifacts and clean up
  formatted = formatted.replace(/\*\*/g, ''); // Remove ** markers
  formatted = formatted.replace(/\*/g, ''); // Remove * markers
  formatted = formatted.replace(/###?\s*/g, ''); // Remove ### and ## markers
  formatted = formatted.replace(/^\s*\*\s*/gm, ''); // Remove bullet asterisks
  formatted = formatted.replace(/^\s*•\s*/gm, ''); // Remove existing bullet points
  formatted = formatted.replace(/^\s*-\s*/gm, ''); // Remove dash bullets

  // Add memo header
  const currentDate = new Date().toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  formatted = `
    <div class="memo-header">
      <div class="memo-title">INVESTMENT ANALYSIS MEMORANDUM</div>
      <div class="memo-meta">
        <div class="memo-date">Date: ${currentDate}</div>
        <div class="memo-from">From: HW Deal Sourcing Intelligence</div>
        <div class="memo-subject">Subject: Multifamily Investment Opportunities Analysis</div>
      </div>
    </div>
    <div class="memo-body">
      ${formatted}
    </div>
  `;

  // Handle URLs and property links (do this before other formatting)
  formatted = formatted.replace(
    /(https?:\/\/[^\s\)>,]+)/gi,
    '<a href="$1" target="_blank" class="property-link">🔗 View Property Details</a>'
  );

  // Format section headers professionally
  formatted = formatted.replace(
    /^([A-Z][A-Za-z\s&\-:()]{10,}):\s*$/gm,
    '<div class="memo-section-header">$1</div><br>'
  );

  // Format subsection headers
  formatted = formatted.replace(
    /^([A-Z][A-Za-z\s\-]{5,15}):\s*$/gm,
    '<div class="memo-subsection">$1:</div><br>'
  );

  // Format property headers
  formatted = formatted.replace(
    /Property \d+:\s*(.+)/gi,
    '<div class="property-entry"><div class="property-title">🏢 Property: $1</div>'
  );

  // Format numbered recommendations
  formatted = formatted.replace(
    /^(\d+)\.\s*(.+)$/gm,
    '<div class="recommendation-item"><span class="recommendation-number">$1.</span> $2</div>'
  );

  // Remove this general bullet formatting to avoid extra bullets

  // Format key property details with specific styling
  formatted = formatted.replace(
    /(Investment Rationale|Strategic Value Proposition|Risk-Return Profile|Due Diligence Roadmap):\s*(.+)/gi,
    '<div class="property-detail"><span class="detail-type">$1:</span> $2</div>'
  );

  // Format other property details without bullets
  formatted = formatted.replace(
    /(Timeline|Recommended Investment Approach|Portfolio Fit|Competitive Market Position|Property|Location|Unit Count):\s*(.+)/gi,
    '<div class="simple-detail"><span class="detail-label">$1:</span> $2</div>'
  );

  // Handle line breaks and spacing
  formatted = formatted.replace(/\n\n+/g, '</div><div class="memo-paragraph">');
  formatted = formatted.replace(/\n/g, '<br>');

  // Wrap content in memo paragraphs
  formatted = '<div class="memo-paragraph">' + formatted + '</div>';

  // Add professional memo styling
  return `
    <div class="professional-memo">
      <style>
        .professional-memo {
          max-width: 900px;
          margin: 0 auto;
          font-family: 'Times New Roman', Times, serif;
          font-size: 14px;
          line-height: 1.4;
          color: #000;
          background: #fff;
          padding: 40px;
          border: 1px solid #ccc;
        }

        .memo-header {
          text-align: center;
          border-bottom: 3px double #000;
          padding-bottom: 20px;
          margin-bottom: 30px;
        }

        .memo-title {
          font-size: 20px;
          font-weight: bold;
          letter-spacing: 2px;
          margin-bottom: 15px;
          text-transform: uppercase;
        }

        .memo-meta {
          text-align: left;
          border: 1px solid #000;
          padding: 15px;
          background: #f9f9f9;
        }

        .memo-date, .memo-from, .memo-subject {
          margin: 5px 0;
          font-weight: bold;
        }

        .memo-body {
          margin-top: 30px;
        }

        .memo-section-header {
          font-size: 16px;
          font-weight: bold;
          text-transform: uppercase;
          margin: 25px 0 15px 0;
          padding: 10px;
          background: #2c5aa0;
          color: white;
          text-align: center;
          letter-spacing: 1px;
          display: block;
        }

        .memo-subsection {
          font-size: 15px;
          font-weight: bold;
          margin: 20px 0 10px 0;
          text-decoration: underline;
          color: #2c5aa0;
          display: block;
        }

        .property-entry {
          border: 1px solid #ddd;
          margin: 15px 0;
          padding: 15px;
          background: #fafafa;
        }

        .property-title {
          font-size: 15px;
          font-weight: bold;
          color: #1a472a;
          margin-bottom: 10px;
          border-bottom: 1px solid #1a472a;
          padding-bottom: 5px;
        }

        .recommendation-item {
          margin: 10px 0;
          padding: 10px;
          background: #f0f8ff;
          border-left: 4px solid #2c5aa0;
        }

        .recommendation-number {
          font-weight: bold;
          color: #2c5aa0;
          margin-right: 8px;
        }

        .memo-bullet {
          margin: 8px 0 8px 20px;
          position: relative;
        }

        .property-detail {
          margin: 8px 0;
          padding: 8px;
          background: #f5f5f5;
          border-left: 2px solid #666;
        }

        .detail-type {
          font-weight: bold;
          color: #2c5aa0;
        }

        .simple-detail {
          margin: 5px 0;
          padding: 3px 0;
        }

        .detail-label {
          font-weight: bold;
          color: #1f2937;
        }

        .property-link {
          display: inline-block;
          background: #2c5aa0;
          color: white !important;
          padding: 6px 12px;
          border-radius: 4px;
          text-decoration: none;
          font-weight: bold;
          margin: 5px 5px 5px 0;
          font-size: 12px;
          transition: background-color 0.3s;
        }

        .property-link:hover {
          background: #1e3d72;
          text-decoration: none;
        }

        .memo-paragraph {
          margin: 15px 0;
          text-align: justify;
        }

        @media print {
          .professional-memo {
            border: none;
            padding: 20px;
            font-size: 12px;
          }
          .property-link {
            background: none;
            color: #2c5aa0 !important;
            border: 1px solid #2c5aa0;
          }
        }
      </style>
      ${formatted}
    </div>
  `;
}

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    service: 'CrewAI Investment Analysis'
  });
});

// Serve React app for all other routes
app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
  console.log(`HW DealSourcing Service Ready`);
});