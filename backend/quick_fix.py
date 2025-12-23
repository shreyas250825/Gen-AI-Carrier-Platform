#!/usr/bin/env python3
"""
Quick Fix for Missing Dependencies
Run this to install boto3 and pymongo immediately
"""

import subprocess
import sys

def quick_install():
    """Install critical missing dependencies"""
    critical_deps = [
        "boto3",
        "pymongo", 
        "python-dotenv"
    ]
    
    print("🔧 Quick Fix: Installing critical dependencies...")
    
    for dep in critical_deps:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dep])
            print(f"✅ Installed {dep}")
        except Exception as e:
            print(f"❌ Failed to install {dep}: {e}")
    
    print("\n✅ Quick fix complete! Try starting the server again.")

if __name__ == "__main__":
    quick_install()