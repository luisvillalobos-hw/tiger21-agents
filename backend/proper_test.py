#!/usr/bin/env python3
"""
Proper test using ADK InMemoryRunner pattern
"""

import os
import asyncio
from dotenv import load_dotenv
from google.adk.runners import InMemoryRunner
from google.genai.types import Part, UserContent

# Load environment variables
load_dotenv()

async def test_agent():
    """Test the deal sourcing agent using proper ADK pattern"""
    print("🧪 Testing Deal Sourcing Agent with ADK InMemoryRunner...")
    
    try:
        # Import the agent
        from deal_sourcing_agent import root_agent
        print("✅ Agent imported successfully")
        
        # Create runner
        runner = InMemoryRunner(agent=root_agent)
        print("✅ InMemoryRunner created")
        
        # Create session
        session = await runner.session_service.create_session(
            app_name=runner.app_name, 
            user_id="test_user"
        )
        print("✅ Session created")
        
        # Test query
        test_query = "Search for multifamily properties in Denver under $5M"
        print(f"🔍 Testing with: {test_query}")
        
        # Create content
        content = UserContent(parts=[Part(text=test_query)])
        
        # Run the agent
        response = ""
        print("🤖 Agent response:")
        print("-" * 50)
        
        async for event in runner.run_async(
            user_id=session.user_id,
            session_id=session.id,
            new_message=content,
        ):
            if hasattr(event, 'content') and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, 'text') and part.text:
                        print(part.text, end='', flush=True)
                        response += part.text
            else:
                print(f"[Event: {type(event).__name__}]")
        
        print("\n" + "-" * 50)
        print(f"✅ Test completed! Response length: {len(response)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function"""
    print(f"Environment variables:")
    print(f"  GOOGLE_GENAI_USE_VERTEXAI: {os.getenv('GOOGLE_GENAI_USE_VERTEXAI')}")
    print(f"  GOOGLE_CLOUD_PROJECT: {os.getenv('GOOGLE_CLOUD_PROJECT')}")
    print(f"  GOOGLE_CLOUD_LOCATION: {os.getenv('GOOGLE_CLOUD_LOCATION')}")
    print()
    
    success = asyncio.run(test_agent())
    exit(0 if success else 1)

if __name__ == "__main__":
    main()
