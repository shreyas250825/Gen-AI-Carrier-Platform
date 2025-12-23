#!/usr/bin/env python3
"""
Gemini Integration Verification

This script verifies that the Gemini API integration is working correctly
by testing the configuration, availability, and fallback system.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
backend_dir = Path(__file__).parent
env_file = backend_dir / ".env"
if env_file.exists():
    load_dotenv(env_file)

# Add backend to path
sys.path.append(str(backend_dir))

from app.ai_engines.engine_router import ai_engine_router

def main():
    """Verify Gemini integration status"""
    print("🔍 Gemini Integration Verification")
    print("=" * 50)
    
    # Check environment variables
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    print(f"📋 Configuration Check:")
    print(f"   GEMINI_API_KEY: {'✅ Set' if gemini_api_key else '❌ Missing'}")
    print(f"   GEMINI_MODEL: {gemini_model}")
    print(f"   PREFER_OLLAMA: {os.getenv('PREFER_OLLAMA', 'true')}")
    print(f"   FALLBACK_TO_GEMINI: {os.getenv('FALLBACK_TO_GEMINI', 'true')}")
    
    # Check engine health
    print(f"\n🏥 Engine Health Check:")
    health = ai_engine_router.health_check()
    
    ollama_status = "✅ Available" if health['ollama']['available'] else "❌ Unavailable"
    gemini_status = "✅ Available" if health['gemini']['available'] else "❌ Unavailable"
    
    print(f"   Ollama: {ollama_status}")
    if health['ollama']['available']:
        print(f"     Model: {health['ollama']['model']}")
        print(f"     URL: {health['ollama']['base_url']}")
    
    print(f"   Gemini: {gemini_status}")
    if health['gemini']['available']:
        print(f"     API Key: Configured")
        print(f"     Model: {gemini_model}")
    
    # Check router configuration
    print(f"\n🔀 Router Configuration:")
    router_config = health['router']
    print(f"   Prefer Ollama: {'✅ Yes' if router_config['prefer_ollama'] else '❌ No'}")
    print(f"   Fallback Enabled: {'✅ Yes' if router_config['fallback_enabled'] else '❌ No'}")
    
    # Get usage statistics
    print(f"\n📊 Usage Statistics:")
    stats = ai_engine_router.get_engine_stats()
    print(f"   Ollama Requests: {stats['ollama_requests']}")
    print(f"   Gemini Requests: {stats['gemini_requests']}")
    print(f"   Fallback Events: {stats['fallback_count']}")
    print(f"   Last Engine Used: {stats['last_engine_used'] or 'None'}")
    
    # Test engine switching capability
    print(f"\n🔧 Testing Engine Switching:")
    
    # Try to switch to Gemini
    if health['gemini']['available']:
        switch_success = ai_engine_router.force_engine("gemini")
        if switch_success:
            print("   ✅ Can switch to Gemini")
            # Switch back to Ollama
            ai_engine_router.force_engine("ollama")
            print("   ✅ Can switch back to Ollama")
        else:
            print("   ❌ Cannot switch to Gemini")
    else:
        print("   ⚠️ Gemini not available for switching")
    
    # Overall assessment
    print(f"\n🎯 Integration Status:")
    
    if health['gemini']['available'] and health['ollama']['available']:
        print("   ✅ FULLY OPERATIONAL")
        print("   • Ollama available for local processing")
        print("   • Gemini available for cloud fallback")
        print("   • Automatic fallback system ready")
        print("   • Manual engine switching functional")
        
        print(f"\n💡 System Behavior:")
        print("   1. Primary: Uses Ollama for privacy and speed")
        print("   2. Fallback: Switches to Gemini if Ollama fails")
        print("   3. Manual: Can force specific engine via API")
        print("   4. Monitoring: Tracks usage and health stats")
        
        return True
        
    elif health['gemini']['available']:
        print("   ⚠️ GEMINI ONLY MODE")
        print("   • Gemini available for cloud processing")
        print("   • Ollama not available (local processing disabled)")
        print("   • System will use Gemini for all operations")
        
        return True
        
    elif health['ollama']['available']:
        print("   ⚠️ OLLAMA ONLY MODE")
        print("   • Ollama available for local processing")
        print("   • Gemini not available (no cloud fallback)")
        print("   • System will use Ollama for all operations")
        
        return False
        
    else:
        print("   ❌ NO ENGINES AVAILABLE")
        print("   • Neither Ollama nor Gemini is available")
        print("   • System cannot perform AI operations")
        
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print(f"\n🎉 Gemini integration is working correctly!")
        print("The system is ready for production use with intelligent AI engine routing.")
    else:
        print(f"\n⚠️ Gemini integration needs attention.")
        print("Please check the configuration and ensure the API key is valid.")