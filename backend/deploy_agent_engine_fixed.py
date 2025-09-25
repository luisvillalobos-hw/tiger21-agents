#!/usr/bin/env python3
"""
Deploy Deal Sourcing Agent to Vertex AI Agent Engine - Fixed Version
"""

import os
import json
import vertexai
from vertexai import agent_engines

def deploy_to_agent_engine():
    """Deploy using correct Vertex AI Agent Engine API"""

    print("🚀 Deploying to Vertex AI Agent Engine (Fixed Version)...")

    # Configuration
    project_id = "tiger21-demo"
    location = "us-central1"
    staging_bucket = "gs://tiger21-demo-adk-staging"

    # Initialize Vertex AI
    vertexai.init(
        project=project_id,
        location=location,
        staging_bucket=staging_bucket
    )

    print(f"✅ Initialized Vertex AI for project: {project_id}")

    try:
        # Import your ADK app
        from adk_app_wrapper import app
        print("✅ Imported ADK app wrapper successfully")

        # Updated requirements with proper versions
        requirements = [
            "google-cloud-aiplatform[agent_engines,adk]>=1.111",
            "google-genai",
            "pydantic>=2.6.4",
            "python-dotenv",
            "aiohttp",
            "requests",
            "reportlab",
            "markdown",
            "beautifulsoup4"
        ]

        # Deploy using agent_engines (not reasoning_engines)
        print("📡 Creating Agent Engine instance...")
        remote_agent = agent_engines.create(
            agent_engine=app,
            requirements=requirements,
            display_name="HW Deal Sourcing Agent",
            description="AI-powered investment opportunity discovery agent with real estate and financial analysis capabilities",
            min_instances=1,
            max_instances=10,
            resource_limits={"cpu": "4", "memory": "8Gi"},
            container_concurrency=9
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
        try:
            # Simple query test without async for now
            print("Agent Engine deployed successfully - testing will be done separately")
        except Exception as test_e:
            print(f"⚠️ Agent deployed but test failed: {test_e}")

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