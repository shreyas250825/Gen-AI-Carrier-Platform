#!/usr/bin/env python3
"""
Test the API endpoints to verify functionality
"""

import requests
import json

def test_aptitude_endpoint():
    """Test aptitude question generation"""
    print("🧠 Testing Aptitude Endpoint...")
    
    response = requests.post('http://localhost:8000/api/aptitude/generate', json={
        'difficulty': 'medium',
        'count': 3
    })
    
    if response.status_code == 200:
        questions = response.json()
        print(f"✅ Generated {len(questions)} aptitude questions")
        for i, q in enumerate(questions[:2]):
            print(f"   Q{i+1}: {q.get('question', 'N/A')[:60]}...")
            print(f"        Type: {q.get('type')}, Difficulty: {q.get('difficulty')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

def test_job_fit_endpoint():
    """Test job fit analysis"""
    print("\n💼 Testing Job Fit Endpoint...")
    
    # Use the correct schema format
    request_data = {
        "resume_data": {
            "role": "Software Engineer",
            "skills": ["Python", "JavaScript", "React", "Node.js"],
            "experience_years": 3,
            "experience_level": "Mid-Level"
        },
        "job_description": {
            "title": "Senior Software Engineer",
            "required_skills": ["Python", "JavaScript", "React", "AWS"],
            "preferred_skills": ["Docker", "Kubernetes"],
            "required_experience_years": 3,
            "company": "TechCorp"
        }
    }
    
    response = requests.post('http://localhost:8000/api/job-fit/analyze', json=request_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Job fit analysis completed")
        print(f"   Overall Fit Score: {result.get('overall_fit_score')}/100")
        print(f"   Skill Match: {result.get('skill_match_percentage')}%")
        print(f"   Role Suitability: {result.get('role_suitability')}")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        test_aptitude_endpoint()
        test_job_fit_endpoint()
        print("\n✅ All endpoint tests completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")