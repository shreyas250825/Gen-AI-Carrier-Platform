#!/usr/bin/env python3
"""
Test environment variable loading
"""

import os
from dotenv import load_dotenv

print("🔍 Testing Environment Variable Loading")
print("=" * 50)

# Check current environment
print(f"1. Current environment: {os.getenv('GEMINI_API_KEY', 'NOT_FOUND')}")

# Try loading from backend/.env
load_dotenv('backend/.env')
print(f"2. After loading backend/.env: {os.getenv('GEMINI_API_KEY', 'NOT_FOUND')}")

# Try loading from root .env
load_dotenv('.env')
print(f"3. After loading .env: {os.getenv('GEMINI_API_KEY', 'NOT_FOUND')}")

# Test the Gemini engine
import sys
sys.path.append('backend')

try:
    from backend.app.ai_engines.gemini_engine import GeminiEngine
    engine = GeminiEngine()
    
    if engine.api_key:
        print(f"✅ GeminiEngine has API key: {engine.api_key[:15]}...")
    else:
        print("❌ GeminiEngine has no API key")
        
except Exception as e:
    print(f"❌ Error importing GeminiEngine: {e}")

# Test a simple API call
if os.getenv('GEMINI_API_KEY'):
    print("\n🧪 Testing simple Gemini API call...")
    try:
        engine = GeminiEngine()
        result = engine.call_gemini("Say 'Hello from Gemini!'", temperature=0.1, max_tokens=50)
        if result:
            print(f"✅ API call successful: {result}")
        else:
            print("❌ API call returned empty result")
    except Exception as e:
        print(f"❌ API call failed: {e}")
else:
    print("❌ No API key available for testing")