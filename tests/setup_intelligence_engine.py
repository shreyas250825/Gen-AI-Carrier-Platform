#!/usr/bin/env python3
"""
Setup script for GenAI Career Intelligence Platform

This script helps set up the three-level intelligence architecture:
1. Checks system requirements
2. Installs dependencies
3. Sets up Ollama (optional)
4. Tests the intelligence engine
5. Provides next steps for AWS integration

Run this before demonstrating the platform to judges.
"""

import os
import sys
import subprocess
import json
import requests
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is compatible")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    print("\n📦 Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'sqlalchemy', 'pydantic', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} is installed")
        except ImportError:
            print(f"❌ {package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📥 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', 
                '-r', 'backend/requirements.txt'
            ])
            print("✅ Dependencies installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies")
            return False
    
    return True

def check_ollama():
    """Check if Ollama is available for Level 2 intelligence"""
    print("\n🤖 Checking Ollama (Level 2 Intelligence)...")
    
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            # Check for recommended model
            model_names = [m.get('name', '') for m in models]
            if any('llama3.2' in name for name in model_names):
                print("✅ Recommended model (llama3.2) is available")
                return True
            else:
                print("⚠️ Recommended model not found. Installing llama3.2:1b...")
                try:
                    subprocess.run(['ollama', 'pull', 'llama3.2:1b'], check=True)
                    print("✅ Model installed successfully")
                    return True
                except subprocess.CalledProcessError:
                    print("⚠️ Could not install model automatically")
                    return False
        else:
            print("❌ Ollama is not responding correctly")
            return False
            
    except requests.exceptions.RequestException:
        print("⚠️ Ollama is not running")
        print("   Level 2 intelligence will be disabled (fallback to Level 1)")
        print("   To enable Ollama:")
        print("   1. Install: https://ollama.ai/")
        print("   2. Run: ollama pull llama3.2:1b")
        print("   3. Start Ollama service")
        return False

def setup_directories():
    """Create necessary directories"""
    print("\n📁 Setting up directories...")
    
    directories = [
        'backend/data/demos',
        'backend/logs',
        'backend/static',
        'docs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created/verified: {directory}")

def test_intelligence_engine():
    """Test the intelligence engine"""
    print("\n🧠 Testing Intelligence Engine...")
    
    try:
        # Add backend to path
        sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
        
        from app.ai_engines.intelligence_engine import intelligence_engine
        
        # Test basic functionality
        test_profile = {
            "role": "Software Engineer",
            "skills": ["Python", "JavaScript"],
            "experience_level": "Mid-Level",
            "experience_years": 3
        }
        
        # Test question generation
        questions = intelligence_engine.generate_questions(
            profile=test_profile,
            interview_type="mixed",
            count=2
        )
        
        if len(questions) >= 2:
            print("✅ Question generation working")
        else:
            print("❌ Question generation failed")
            return False
        
        # Test answer evaluation
        evaluation = intelligence_engine.evaluate_answer(
            question="Tell me about yourself",
            answer="I am a software engineer with 3 years of experience",
            expected_keywords=["experience", "engineer"],
            profile=test_profile
        )
        
        if evaluation and 'technical' in evaluation:
            print("✅ Answer evaluation working")
        else:
            print("❌ Answer evaluation failed")
            return False
        
        # Test aptitude questions
        aptitude = intelligence_engine.generate_aptitude_questions(count=1)
        if len(aptitude) >= 1:
            print("✅ Aptitude questions working")
        else:
            print("❌ Aptitude questions failed")
            return False
        
        # Test job fit
        job_desc = {
            "title": "Developer",
            "required_skills": ["Python"],
            "required_experience_years": 2
        }
        
        job_fit = intelligence_engine.calculate_job_fit(test_profile, job_desc)
        if job_fit and 'overall_fit_score' in job_fit:
            print("✅ Job fit analysis working")
        else:
            print("❌ Job fit analysis failed")
            return False
        
        print("✅ All intelligence engine tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Intelligence engine test failed: {e}")
        return False

def create_demo_data():
    """Create demo data for testing"""
    print("\n📊 Creating demo data...")
    
    # Sample job descriptions for testing
    sample_jobs = [
        {
            "title": "Senior Software Engineer",
            "company": "TechCorp",
            "required_skills": ["Python", "JavaScript", "React", "AWS"],
            "preferred_skills": ["Docker", "Kubernetes", "TypeScript"],
            "required_experience_years": 5,
            "description": "We're looking for a senior software engineer..."
        },
        {
            "title": "Frontend Developer", 
            "company": "StartupXYZ",
            "required_skills": ["JavaScript", "React", "HTML", "CSS"],
            "preferred_skills": ["TypeScript", "Next.js", "Tailwind"],
            "required_experience_years": 3,
            "description": "Join our frontend team..."
        }
    ]
    
    demo_dir = Path('backend/data/demos')
    demo_dir.mkdir(parents=True, exist_ok=True)
    
    with open(demo_dir / 'sample_jobs.json', 'w') as f:
        json.dump(sample_jobs, f, indent=2)
    
    print("✅ Demo data created")

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎯 Setup Complete! Next Steps:")
    print("=" * 50)
    
    print("\n1. 🚀 Start the API server:")
    print("   cd backend")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    
    print("\n2. 📖 View API documentation:")
    print("   http://localhost:8000/docs")
    
    print("\n3. 🧪 Test the intelligence system:")
    print("   python test_intelligence_engine.py")
    
    print("\n4. 🔍 Check intelligence status:")
    print("   GET http://localhost:8000/api/intelligence-status")
    
    print("\n5. 🎮 Try new features:")
    print("   • Aptitude Assessment: POST /api/aptitude/generate")
    print("   • Job Fit Analysis: POST /api/job-fit/analyze")
    print("   • Role Matching: POST /api/job-fit/role-matching")
    
    print("\n6. ☁️ For AWS integration:")
    print("   • Review docs/aws-architecture.md")
    print("   • Configure AWS credentials")
    print("   • Enable Level 3 intelligence in intelligence_engine.py")
    
    print("\n🏆 Ready for AWS ImpactX Challenge demonstration!")

def main():
    """Main setup function"""
    print("🚀 GenAI Career Intelligence Platform Setup")
    print("=" * 50)
    print("Setting up three-level intelligence architecture...")
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Setup directories
    setup_directories()
    
    # Check Ollama (optional)
    ollama_available = check_ollama()
    
    # Create demo data
    create_demo_data()
    
    # Test intelligence engine
    if not test_intelligence_engine():
        print("\n⚠️ Intelligence engine tests failed, but basic setup is complete.")
        print("The system will work with Level 1 (Deterministic) intelligence.")
    
    # Print next steps
    print_next_steps()
    
    print(f"\n📊 Setup Summary:")
    print(f"  ✅ Level 1 (Deterministic): Always available")
    print(f"  {'✅' if ollama_available else '⚠️'} Level 2 (Local AI): {'Available' if ollama_available else 'Not available'}")
    print(f"  🔧 Level 3 (Cloud AI): Ready for AWS integration")

if __name__ == "__main__":
    main()