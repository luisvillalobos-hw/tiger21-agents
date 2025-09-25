#!/usr/bin/env python3
"""
Deploy Deal Sourcing Agent to Vertex AI Agent Engine
"""

import os
import sys
import json
import vertexai
from vertexai.preview import reasoning_engines


def deploy_agent_via_adk():
    """Deploy using proper ADK/ReasoningEngine SDK approach"""
    print("🚀 Deploying agent using ADK/ReasoningEngine SDK...")

    # Set up project and location
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "tiger21-demo")
    location = os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1")
    staging_bucket = os.getenv("STAGING_BUCKET", f"gs://{project_id}-adk-staging")

    print(f"Deploying to project: {project_id}")
    print(f"Location: {location}")
    print(f"Staging bucket: {staging_bucket}")

    try:
        # IMPORTANT: init with regional endpoint + staging bucket
        vertexai.init(project=project_id, location=location, staging_bucket=staging_bucket)

        # Import the wrapped agent AFTER init so dependencies are set up
        from reasoning_engine_wrapper import reasoning_engine
        from deal_sourcing_agent import root_agent

        print("✅ ADK agent loaded successfully")
        print(f"Agent name: {getattr(root_agent, 'name', 'N/A')}")
        print(f"Agent description: {getattr(root_agent, 'description', 'N/A')}")

        # Minimal requirements; add your deps and pin them
        requirements = [
            "google-cloud-aiplatform[agent_engines,adk]",
            "google-adk>=1.0.0",
            "cloudpickle==3.0",
            "pydantic>=2.10.6",
            "aiohttp>=3.10.0",
            "requests>=2.32.0",
            "reportlab>=4.2.0",
            "markdown>=3.7.0",
            "beautifulsoup4>=4.12.0",
        ]

        # If you need to ship local modules, list folders/files here; else None
        extra_packages = None  # e.g., ["agents", "utils/helpers.py"]

        print("📡 Creating Reasoning Engine (this builds & deploys)...")
        print("⏳ This may take several minutes...")

        remote = reasoning_engines.ReasoningEngine.create(
            reasoning_engine,
            display_name="Deal Sourcing Agent",
            description="AI-powered investment opportunity discovery agent with real estate and financial analysis",
            requirements=requirements,
            extra_packages=extra_packages,
            # Optional: env_vars={}, encryption_spec=..., agent_service_account_email="..."
        )

        resource_name = remote.resource_name  # projects/123.../locations/us-central1/reasoningEngines/ID
        agent_id = resource_name.split("/")[-1]
        print("✅ Agent deployed successfully!")
        print(f"Resource Name: {resource_name}")
        print(f"Agent Engine ID: {agent_id}")

        # Save the configuration for the backend
        config = {
            "agent_engine_id": agent_id,
            "project_id": project_id,
            "location": location,
            "resource_name": resource_name,
            "status": "deployed",
            "deployment_method": "sdk_reasoning_engine"
        }

        with open("agent_engine_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print("✅ Configuration saved to agent_engine_config.json")

        # Test the deployed agent
        print("\n🧪 Testing deployed agent...")
        try:
            response = remote.query(
                input="Hello! I'm looking for multifamily investment opportunities in Denver under $5M. Can you help?"
            )
            print("✅ Test successful!")
            print(f"Response preview: {str(response)[:200]}...")
        except Exception as test_e:
            print(f"⚠️  Agent deployed but test failed: {test_e}")

        return agent_id

    except Exception as e:
        print(f"❌ ADK deployment failed: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main deployment function with fallback strategies"""

    print("🎯 Starting Agent Engine deployment process...")

    # Try ADK-based deployment first
    agent_id = deploy_agent_via_adk()

    if not agent_id:
        print("❌ All deployment methods failed")
        sys.exit(1)

    print(f"\n🎉 Deployment complete! Agent Engine ID: {agent_id}")
    return agent_id


if __name__ == "__main__":
    main()