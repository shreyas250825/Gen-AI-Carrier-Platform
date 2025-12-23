#!/usr/bin/env python3
"""
Check AI engine status after interview test
"""

import requests
import json

def check_engine_status():
    """Check which AI engine is being used"""
    
    try:
        response = requests.get('http://localhost:8000/api/v1/ai-engine/status')
        
        if response.status_code == 200:
            data = response.json()['data']
            stats = data['stats']
            
            print("🔍 AI Engine Status:")
            print(f"  Last Engine Used: {stats['last_engine_used']}")
            print(f"  Ollama Requests: {stats['ollama_requests']}")
            print(f"  Gemini Requests: {stats['gemini_requests']}")
            print(f"  Fallback Count: {stats['fallback_count']}")
            
            if stats['last_engine_used'] == 'ollama':
                print("✅ Ollama is being used for AI operations!")
            elif stats['last_engine_used'] == 'gemini':
                print("⚠️ Gemini is being used (fallback)")
            else:
                print("❓ No engine used yet")
                
        else:
            print(f"❌ Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    check_engine_status()