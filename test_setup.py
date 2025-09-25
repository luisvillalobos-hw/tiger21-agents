#!/usr/bin/env python3
"""
Test script to verify the CrewAI setup is working correctly.

This script performs basic import tests and configuration checks.
"""

import os
import sys

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")

    try:
        import crewai
        print("✅ CrewAI imported successfully")
    except ImportError as e:
        print(f"❌ CrewAI import failed: {e}")
        return False

    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        print("✅ LangChain Google GenAI imported successfully")
    except ImportError as e:
        print(f"❌ LangChain Google GenAI import failed: {e}")
        return False

    try:
        from src.agents import (
            create_real_estate_agent,
            create_financial_news_agent,
            create_deal_coordinator_agent,
            create_risk_analyst
        )
        print("✅ Custom agents imported successfully")
    except ImportError as e:
        print(f"❌ Custom agents import failed: {e}")
        return False

    try:
        from src.crew import InvestmentOpportunityCrew
        print("✅ Investment crew imported successfully")
    except ImportError as e:
        print(f"❌ Investment crew import failed: {e}")
        return False

    return True

def test_config():
    """Test configuration and environment variables."""
    print("\n⚙️ Testing configuration...")

    try:
        from config import GOOGLE_API_KEY, MODELS, LLM_CONFIG
        print("✅ Config module imported successfully")
    except ImportError as e:
        print(f"❌ Config import failed: {e}")
        return False

    # Check if API key is set
    if not GOOGLE_API_KEY:
        print("⚠️ GOOGLE_API_KEY not set in environment")
        return False
    else:
        print("✅ GOOGLE_API_KEY is configured")

    print(f"📊 Models configured: {MODELS}")
    return True

def test_agent_creation():
    """Test that agents can be created without errors."""
    print("\n🤖 Testing agent creation...")

    # Skip this test if no API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ Skipping agent creation test (no API key)")
        return True

    try:
        from src.agents import create_real_estate_agent
        agent = create_real_estate_agent()
        print("✅ Real estate agent created successfully")
    except Exception as e:
        print(f"❌ Real estate agent creation failed: {e}")
        return False

    try:
        from src.agents import create_financial_news_agent
        agent = create_financial_news_agent()
        print("✅ Financial news agent created successfully")
    except Exception as e:
        print(f"❌ Financial news agent creation failed: {e}")
        return False

    return True

def test_crew_creation():
    """Test that the crew can be initialized."""
    print("\n👥 Testing crew creation...")

    # Skip this test if no API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("⚠️ Skipping crew creation test (no API key)")
        return True

    try:
        from src.crew import InvestmentOpportunityCrew
        crew = InvestmentOpportunityCrew()
        print("✅ Investment opportunity crew created successfully")
    except Exception as e:
        print(f"❌ Crew creation failed: {e}")
        return False

    return True

def main():
    """Run all tests."""
    print("🚀 CrewAI Tiger21 Setup Test")
    print("=" * 40)

    tests = [
        test_imports,
        test_config,
        test_agent_creation,
        test_crew_creation
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1

    print(f"\n📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Your CrewAI setup is ready.")
        print("\n💡 Next steps:")
        print("1. Set your GOOGLE_API_KEY in .env file")
        print("2. Optionally set SERPER_API_KEY for better search")
        print("3. Run 'uv run python main.py' to start analysis")
    else:
        print("❌ Some tests failed. Please check your setup.")
        sys.exit(1)

if __name__ == "__main__":
    main()