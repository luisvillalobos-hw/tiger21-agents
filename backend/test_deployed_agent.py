#!/usr/bin/env python3
"""
Test the deployed Agent Engine
"""

import json
import asyncio
import vertexai
from vertexai import agent_engines

async def test_deployed_agent():
    """Test the deployed Agent Engine"""

    # Load configuration
    with open('agent_engine_config.json', 'r') as f:
        config = json.load(f)

    print(f"🧪 Testing deployed Agent Engine...")
    print(f"Agent Engine ID: {config['agent_engine_id']}")
    print(f"Project: {config['project_id']}")
    print(f"Location: {config['location']}")
    print(f"Status: {config['status']}")

    # Initialize Vertex AI
    vertexai.init(
        project=config['project_id'],
        location=config['location']
    )

    try:
        # Get the deployed agent engine
        remote_agent = agent_engines.get(config['resource_name'])
        print("✅ Successfully connected to deployed Agent Engine")

        # Test query
        test_queries = [
            "Hello! I'm looking for multifamily investment opportunities in Denver under $5M. Can you help?",
            "What types of real estate deals can you help me find?",
            "Can you search for M&A opportunities in the technology sector?"
        ]

        for i, query in enumerate(test_queries, 1):
            print(f"\n🔍 Test Query {i}: {query}")

            try:
                # Create a test session
                session = await remote_agent.async_create_session(user_id="test_user")
                session_id = session.get("id") if isinstance(session, dict) else session.id
                print(f"✅ Created session: {session_id}")

                # Query the agent using streaming
                print("🔄 Streaming response...")
                response_parts = []

                async for event in remote_agent.async_stream_query(
                    user_id="test_user",
                    session_id=session_id,
                    message=query
                ):
                    print(f"📝 Event: {event}")
                    response_parts.append(str(event))

                full_response = " ".join(response_parts)
                print("✅ Query successful!")
                print(f"Full Response: {full_response}")

                break  # Just test one query for now

            except Exception as query_error:
                print(f"❌ Query {i} failed: {query_error}")
                import traceback
                traceback.print_exc()
                continue

        return True

    except Exception as e:
        print(f"❌ Connection failed: {str(e)}")
        print(f"Error type: {type(e)}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_deployed_agent())
    if success:
        print("\n🎉 Agent Engine test completed!")
    else:
        print("\n❌ Agent Engine test failed")
        exit(1)