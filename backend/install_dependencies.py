#!/usr/bin/env python3
"""
Dependency Installation Script for GenAI Career Platform
Installs all required packages for S3 and MongoDB integration
"""

import subprocess
import sys
import os

def install_package(package):
    """Install a package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ Successfully installed {package}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install {package}: {e}")
        return False

def main():
    """Install all required dependencies"""
    print("🚀 Installing GenAI Career Platform Dependencies...")
    print("=" * 60)
    
    # Core dependencies for S3 and MongoDB integration
    dependencies = [
        "boto3==1.34.0",
        "botocore==1.34.0", 
        "pymongo==4.6.0",
        "motor==3.3.2",
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "python-multipart==0.0.6",
        "pydantic==1.10.24",
        "python-dotenv==1.0.0",
        "aiofiles==23.2.1",
        "pdfplumber==0.10.3",
        "python-docx==1.1.0",
        "google-generativeai==0.3.2",
        "ollama==0.1.7",
        "requests>=2.31.0",
        "numpy>=2.0.0"
    ]
    
    failed_packages = []
    
    for package in dependencies:
        if not install_package(package):
            failed_packages.append(package)
    
    print("\n" + "=" * 60)
    
    if failed_packages:
        print(f"❌ Failed to install {len(failed_packages)} packages:")
        for package in failed_packages:
            print(f"   - {package}")
        print("\n💡 Try running: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies installed successfully!")
        print("\n🎯 Ready for AWS ImpactX Challenge Demo!")
        print("\nNext steps:")
        print("1. Start backend: uvicorn app.main:app --reload")
        print("2. Navigate to: http://localhost:8000/docs")
        print("3. Test demo endpoints: http://localhost:8000/api/v1/demo/status")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)