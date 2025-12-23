#!/usr/bin/env python3
"""
Debug the job fit API endpoint
"""

import requests
import json
import traceback

def test_job_fit_debug():
    """Test job fit with detailed error reporting"""
    print("🔍 Debugging Job Fit Endpoint...")
    
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
    
    try:
        response = requests.post('http://localhost:8000/api/job-fit/analyze', json=request_data)
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Success!")
            print(json.dumps(result, indent=2))
        else:
            print(f"❌ Error Response:")
            print(f"   Status: {response.status_code}")
            print(f"   Text: {response.text}")
            
            # Try to parse as JSON for more details
            try:
                error_json = response.json()
                print(f"   JSON: {json.dumps(error_json, indent=2)}")
            except:
                pass
                
    except Exception as e:
        print(f"❌ Request failed: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    test_job_fit_debug()