#!/usr/bin/env python3
"""
Test different Gemini API endpoints and models
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('backend/.env')
load_dotenv('.env')

API_KEY = os.getenv('GEMINI_API_KEY')

def test_gemini_models():
    """Test different Gemini model endpoints"""
    print("🧪 Testing Gemini API with different models...")
    print(f"API Key: {API_KEY[:15]}..." if API_KEY else "No API key found")
    
    if not API_KEY:
        print("❌ No API key available")
        return
    
    # Different model names to try
    models_to_test = [
        "gemini-1.5-flash-latest",
        "gemini-1.5-flash",
        "gemini-1.5-pro-latest", 
        "gemini-1.5-pro",
        "gemini-pro",
        "gemini-1.0-pro"
    ]
    
    base_url = "https://generativelanguage.googleapis.com/v1beta/models"
    
    for model in models_to_test:
        print(f"\n🔍 Testing model: {model}")
        
        url = f"{base_url}/{model}:generateContent?key={API_KEY}"
        
        payload = {
            "contents": [{
                "parts": [{
                    "text": "Hello! Please respond with 'API test successful'"
                }]
            }],
            "generationConfig": {
                "temperature": 0.1,
                "maxOutputTokens": 50
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                if "candidates" in data and data["candidates"]:
                    content = data["candidates"][0]["content"]["parts"][0]["text"]
                    print(f"   ✅ SUCCESS: {content}")
                    return model  # Return the working model
                else:
                    print(f"   ❌ No content in response: {data}")
            else:
                print(f"   ❌ Error: {response.text}")
                
        except Exception as e:
            print(f"   ❌ Exception: {e}")
    
    print("\n❌ No working models found")
    return None

def test_api_key_validity():
    """Test if the API key is valid by listing available models"""
    print("\n🔑 Testing API key validity...")
    
    if not API_KEY:
        print("❌ No API key available")
        return False
    
    # Try to list available models
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Models list status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "models" in data:
                print(f"✅ API key is valid! Found {len(data['models'])} models:")
                for model in data["models"][:5]:  # Show first 5 models
                    print(f"   - {model.get('name', 'Unknown')}")
                return True
            else:
                print(f"❌ Unexpected response format: {data}")
        else:
            print(f"❌ Error response: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return False

if __name__ == "__main__":
    print("🚀 GEMINI API TESTING")
    print("=" * 50)
    
    # Test API key validity first
    if test_api_key_validity():
        # Test different models
        working_model = test_gemini_models()
        
        if working_model:
            print(f"\n🎉 Found working model: {working_model}")
            print("✅ Gemini API is fully functional!")
        else:
            print("\n❌ No working models found, but API key seems valid")
    else:
        print("\n❌ API key appears to be invalid or inactive")
        print("\n💡 To get a valid API key:")
        print("   1. Go to https://makersuite.google.com/app/apikey")
        print("   2. Create a new API key")
        print("   3. Replace the key in your .env files")