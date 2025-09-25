#!/usr/bin/env python3
"""
Deploy Deal Sourcing Agent to Vertex AI Agent Engine using official documentation approach
"""

import os
import json
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines

def deploy_to_agent_engine():
    """Deploy using the official Vertex AI Agent Engine approach"""

    print("🚀 Deploying to Vertex AI Agent Engine...")

    # Initialize Vertex AI
    project_id = "tiger21-demo"
    location = "us-central1"
    staging_bucket = "gs://tiger21-demo-adk-staging"

    aiplatform.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket
    )

    print(f"✅ Initialized Vertex AI for project: {project_id}")

    try:
        # Import the ADK app wrapper
        from reasoning_engine_app import app
        print("✅ Imported ADK app wrapper successfully")

        # Define requirements
        requirements = [
            "google-cloud-aiplatform[agent_engines,adk]",
            "google-genai>=1.9.0",
            "google-auth>=2.0.0",
            "google-adk>=1.0.0",
            "pydantic>=2.10.6",
            "python-dotenv>=1.0.1",
            "aiohttp>=3.10.0",
            "requests>=2.32.0",
            "reportlab>=4.2.0",
            "markdown>=3.7.0",
            "beautifulsoup4>=4.12.0"
        ]

        # Create the reasoning engine instance
        print("📡 Creating Reasoning Engine instance...")
        remote_agent = reasoning_engines.ReasoningEngine.create(
            reasoning_engine=app,
            requirements=requirements,
            display_name="HW Deal Sourcing Agent",
            description="AI-powered investment opportunity discovery agent with real estate and financial analysis capabilities"
        )

        # Get resource information
        resource_name = remote_agent.resource_name
        agent_engine_id = resource_name.split("/")[-1]

        print("✅ Agent Engine deployed successfully!")
        print(f"Resource Name: {resource_name}")
        print(f"Agent Engine ID: {agent_engine_id}")

        # Save configuration
        config = {
            "agent_engine_id": agent_engine_id,
            "project_id": project_id,
            "location": location,
            "resource_name": resource_name,
            "status": "deployed",
            "deployment_method": "vertex_ai_agent_engines"
        }

        with open("agent_engine_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print("✅ Configuration saved to agent_engine_config.json")

        # Test the deployment
        print("\n🧪 Testing deployed agent...")
        test_query = "Hello! I'm looking for multifamily investment opportunities in Denver under $5M. Can you help?"

        response = remote_agent.query(input=test_query)
        print("✅ Test query successful!")
        print(f"Response preview: {str(response)[:200]}...")

        return agent_engine_id

    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    agent_id = deploy_to_agent_engine()
    if agent_id:
        print(f"\n🎉 Deployment complete! Agent Engine ID: {agent_id}")
    else:
        print("\n❌ Deployment failed")
        exit(1)