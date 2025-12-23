#!/usr/bin/env python3
"""
Test a single Gemini API call to verify it's working
"""

import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')
load_dotenv('.env')

from backend.app.ai_engines.gemini_engine import GeminiEngine

def test_single_call():
    """Test a single API call"""
    print("🧪 Testing Single Gemini API Call")
    print("=" * 40)
    
    engine = GeminiEngine()
    
    print("Making API call...")
    result = engine.call_gemini(
        "Generate a professional interview question for a Software Engineer. Keep it under 20 words.", 
        temperature=0.3, 
        max_tokens=50
    )
    
    if result and len(result) > 10:
        print(f"✅ SUCCESS! Real Gemini response:")
        print(f"   '{result}'")
        print("\n🎉 Gemini API is working with real AI responses!")
        return True
    else:
        print(f"❌ No response or fallback used: '{result}'")
        print("   (This might be due to rate limiting)")
        return False

if __name__ == "__main__":
    test_single_call()