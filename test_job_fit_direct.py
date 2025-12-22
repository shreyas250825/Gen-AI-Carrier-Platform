#!/usr/bin/env python3
"""
Direct test of job fit functionality without API endpoints
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.ai_engines.gemini_engine import GeminiEngine

def test_job_fit_direct():
    """Test job fit analysis directly"""
    print("💼 Testing Job Fit Analysis Directly...")
    
    # Initialize engine
    engine = GeminiEngine()
    
    # Test data
    resume_data = {
        "role": "Software Engineer",
        "skills": ["Python", "JavaScript", "React", "Node.js"],
        "experience_years": 3
    }
    
    job_description = {
        "title": "Senior Software Engineer",
        "required_skills": ["Python", "JavaScript", "React", "AWS"],
        "preferred_skills": ["Docker", "Kubernetes"],
        "required_experience_years": 3
    }
    
    # Test the method directly
    try:
        result = engine.calculate_job_fit(resume_data, job_description)
        
        print("✅ Job fit analysis completed successfully!")
        print(f"   Overall Fit Score: {result.get('overall_fit_score')}/100")
        print(f"   Skill Match: {result.get('skill_match_percentage')}%")
        print(f"   Experience Match: {result.get('experience_match_percentage')}%")
        print(f"   Role Suitability: {result.get('role_suitability')}")
        print(f"   Missing Required Skills: {result.get('missing_required_skills')}")
        print(f"   Missing Preferred Skills: {result.get('missing_preferred_skills')}")
        print(f"   Matched Skills: {result.get('matched_skills')}")
        print(f"   Recommendations: {result.get('recommendations')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Direct test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_job_fit_direct()