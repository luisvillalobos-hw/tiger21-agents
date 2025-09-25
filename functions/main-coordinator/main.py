import json
import functions_framework
from google.cloud import logging
import requests
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Set up logging
logging_client = logging.Client()
logging_client.setup_logging()

# Configuration for agent function URLs
AGENT_FUNCTIONS = {
    'real_estate_agent': os.getenv('REAL_ESTATE_FUNCTION_URL', 'https://us-central1-tiger21-demo.cloudfunctions.net/real-estate-agent'),
    'financial_news_agent': os.getenv('FINANCIAL_NEWS_FUNCTION_URL', 'https://us-central1-tiger21-demo.cloudfunctions.net/financial-news-agent'),
    'deal_coordinator_agent': os.getenv('DEAL_COORDINATOR_FUNCTION_URL', 'https://us-central1-tiger21-demo.cloudfunctions.net/deal-coordinator-agent'),
    'risk_analyst_agent': os.getenv('RISK_ANALYST_FUNCTION_URL', 'https://us-central1-tiger21-demo.cloudfunctions.net/risk-analyst-agent')
}

def call_agent_function(agent_name, function_url, query, timeout=60):
    """Call an individual agent function"""
    try:
        headers = {'Content-Type': 'application/json'}
        payload = {'query': query}

        response = requests.post(
            function_url,
            json=payload,
            headers=headers,
            timeout=timeout
        )

        if response.status_code == 200:
            return {
                'agent': agent_name,
                'success': True,
                'data': response.json()
            }
        else:
            return {
                'agent': agent_name,
                'success': False,
                'error': f"HTTP {response.status_code}: {response.text}"
            }
    except Exception as e:
        return {
            'agent': agent_name,
            'success': False,
            'error': str(e)
        }

@functions_framework.http
def main_coordinator(request):
    """HTTP Cloud Function for Main Deal Sourcing Coordinator"""

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
        if not request_json or 'message' not in request_json:
            return json.dumps({'error': 'Missing message parameter'}), 400, headers

        user_message = request_json['message']
        session_id = request_json.get('session_id', 'default')

        print(f"Processing message: {user_message}")

        # Determine which agents to call based on the message content
        message_lower = user_message.lower()
        agents_to_call = []

        # Simple keyword-based routing
        if any(keyword in message_lower for keyword in ['real estate', 'property', 'house', 'building', 'rent']):
            agents_to_call.append('real_estate_agent')

        if any(keyword in message_lower for keyword in ['news', 'market', 'financial', 'stock', 'economy']):
            agents_to_call.append('financial_news_agent')

        if any(keyword in message_lower for keyword in ['deal', 'investment', 'opportunity', 'analyze']):
            agents_to_call.append('deal_coordinator_agent')

        if any(keyword in message_lower for keyword in ['risk', 'safe', 'secure', 'danger', 'assess']):
            agents_to_call.append('risk_analyst_agent')

        # If no specific agents identified, use real estate as default
        if not agents_to_call:
            agents_to_call = ['real_estate_agent']

        print(f"Calling agents: {agents_to_call}")

        # Call the relevant agent functions in parallel
        results = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {}

            for agent_name in agents_to_call:
                function_url = AGENT_FUNCTIONS.get(agent_name)
                if function_url:
                    future = executor.submit(call_agent_function, agent_name, function_url, user_message)
                    futures[future] = agent_name
                else:
                    results.append({
                        'agent': agent_name,
                        'success': False,
                        'error': f'Function URL not configured for {agent_name}'
                    })

            # Collect results
            for future in as_completed(futures, timeout=120):
                result = future.result()
                results.append(result)

        # Process and combine results
        successful_results = [r for r in results if r['success']]
        failed_results = [r for r in results if not r['success']]

        if successful_results:
            # Combine the agent responses
            combined_response = "Based on my analysis:\n\n"
            for result in successful_results:
                agent_name = result['agent'].replace('_', ' ').title()
                agent_response = result['data'].get('result', '')
                combined_response += f"**{agent_name}:** {agent_response}\n\n"
        else:
            combined_response = "I'm your AI deal sourcing agent. I can help you find real estate deals, analyze financial opportunities, and assess investment risks. How can I assist you today?"

        response = {
            'message': combined_response,
            'session_id': session_id,
            'agents_called': agents_to_call,
            'successful_agents': len(successful_results),
            'failed_agents': len(failed_results),
            'timestamp': int(time.time()),
            'status': 'success'
        }

        if failed_results:
            response['errors'] = [{'agent': r['agent'], 'error': r['error']} for r in failed_results]

        return json.dumps(response), 200, headers

    except Exception as e:
        print(f"Error in main coordinator: {str(e)}")
        error_response = {
            'message': 'I encountered an error processing your request. Please try again.',
            'error': str(e),
            'status': 'error'
        }
        return json.dumps(error_response), 500, headers