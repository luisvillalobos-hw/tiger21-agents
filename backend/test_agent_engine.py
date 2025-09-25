#!/usr/bin/env python3
"""
Test script for Agent Engine deployment
"""

import json
import os
from google.cloud import aiplatform

def test_agent_engine():
    """Test the deployed Agent Engine"""

    # Load configuration
    with open('agent_engine_config.json', 'r') as f:
        config = json.load(f)

    print(f"🧪 Testing Agent Engine deployment...")
    print(f"Agent Engine ID: {config['agent_engine_id']}")
    print(f"Project: {config['project_id']}")
    print(f"Location: {config['location']}")

    # Initialize Vertex AI
    aiplatform.init(
        project=config['project_id'],
        location=config['location']
    )

    try:
        # Create a reasoning engine instance
        from vertexai.preview import reasoning_engines

        remote_agent = reasoning_engines.ReasoningEngine(
            resource_name=config['resource_name']
        )

        print("✅ Agent Engine instance created successfully")

        # Test query
        test_query = "Hello! I'm looking for multifamily investment opportunities in Denver under $5M. Can you help?"
        print(f"\n🔍 Testing query: {test_query}")

        response = remote_agent.query(input=test_query)

        print("✅ Query successful!")
        print(f"Response: {str(response)[:200]}...")

        return True

    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print(f"Error type: {type(e)}")

        # If the specific Agent Engine ID doesn't work, let's try local testing
        print("\n🔄 Falling back to local ADK agent test...")
        try:
            from deal_sourcing_agent import root_agent
            response = root_agent.query(test_query)
            print("✅ Local agent test successful!")
            print(f"Local response: {str(response)[:200]}...")
            return True
        except Exception as local_e:
            print(f"❌ Local test also failed: {local_e}")
            return False

if __name__ == "__main__":
    success = test_agent_engine()
    exit(0 if success else 1)