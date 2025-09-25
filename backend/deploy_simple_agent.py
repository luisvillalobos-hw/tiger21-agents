#!/usr/bin/env python3
"""
Deploy a simple test agent to Reasoning Engine first
"""

import os
import json
from google.cloud import aiplatform
from vertexai.preview import reasoning_engines

def deploy_simple_agent():
    """Deploy a simple agent to test Reasoning Engine setup"""

    print("🚀 Deploying Simple Test Agent to Vertex AI Agent Engine...")

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
        # Import the simple agent
        from simple_agent import agent
        print("✅ Imported simple agent successfully")

        # Minimal requirements - only what's absolutely necessary
        requirements = [
            "google-cloud-aiplatform==1.116.0",
            "cloudpickle==3.1.1"
        ]

        # Create the reasoning engine instance with minimal config
        print("📡 Creating Reasoning Engine instance...")
        remote_agent = reasoning_engines.ReasoningEngine.create(
            reasoning_engine=agent,
            requirements=requirements,
            display_name="HW Deal Sourcing Test Agent",
            description="Simple test agent for deployment validation"
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
            "deployment_method": "simple_test_agent"
        }

        with open("agent_engine_config.json", "w") as f:
            json.dump(config, f, indent=2)

        print("✅ Configuration saved to agent_engine_config.json")

        # Test the deployment
        print("\n🧪 Testing deployed agent...")
        test_query = "Hello! I'm looking for multifamily investment opportunities in Denver under $5M. Can you help?"

        response = remote_agent.query(input=test_query)
        print("✅ Test query successful!")
        print(f"Response: {response}")

        return agent_engine_id

    except Exception as e:
        print(f"❌ Deployment failed: {str(e)}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    agent_id = deploy_simple_agent()
    if agent_id:
        print(f"\n🎉 Deployment complete! Agent Engine ID: {agent_id}")
    else:
        print("\n❌ Deployment failed")
        exit(1)