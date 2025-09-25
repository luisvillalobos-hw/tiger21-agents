import json
import functions_framework
from google.cloud import logging
import sys
import os

# Add the local path for imports
sys.path.append(os.path.dirname(__file__))

# Set up logging
logging_client = logging.Client()
logging_client.setup_logging()

@functions_framework.http
def deal_coordinator_agent(request):
    """HTTP Cloud Function for Deal Coordinator Agent"""

    # Handle CORS
    if request.method == 'OPTIONS':
        headers = {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST',
            'Access-Control-Allow-Headers': 'Content-Type',
            'Access-Control-Max-Age': '3600'
        }
        return ('', 204, headers)

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'application/json'
    }

    try:
        # Get the request data
        request_json = request.get_json(silent=True)
        if not request_json or 'query' not in request_json:
            return json.dumps({'error': 'Missing query parameter'}), 400, headers

        query = request_json['query']

        # Import and use the deal coordinator agent
        from agents.sub_agents.agent import deal_coordinator_agent

        # Run the agent using the correct method
        import asyncio
        async def run_agent():
            async for event in deal_coordinator_agent.run_live(query):
                if hasattr(event, 'content') and event.content:
                    return event.content
                elif hasattr(event, 'text') and event.text:
                    return event.text
                elif hasattr(event, 'message') and event.message:
                    return event.message
                elif isinstance(event, str):
                    return event
            return "I can help you coordinate and analyze deal opportunities across different markets."

        result = asyncio.run(run_agent())

        response = {
            'agent': 'deal_coordinator_agent',
            'query': query,
            'result': result or 'I can help you coordinate and analyze deal opportunities across different markets. What deals would you like me to evaluate?',
            'status': 'success'
        }

        return json.dumps(response), 200, headers

    except Exception as e:
        print(f"Error in deal coordinator agent: {str(e)}")
        error_response = {
            'agent': 'deal_coordinator_agent',
            'error': str(e),
            'status': 'error'
        }
        return json.dumps(error_response), 500, headers