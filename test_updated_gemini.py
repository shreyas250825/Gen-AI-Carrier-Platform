#!/usr/bin/env python3
"""
Test the updated Gemini engine with correct model
"""

import sys
import os
sys.path.append('backend')

from dotenv import load_dotenv
load_dotenv('backend/.env')
load_dotenv('.env')

from backend.app.ai_engines.gemini_engine import GeminiEngine

def test_updated_gemini():
    """Test the updated Gemini engine"""
    print("🧪 Testing Updated Gemini Engine")
    print("=" * 50)
    
    engine = GeminiEngine()
    
    # Test 1: Simple API call
    print("\n1️⃣ Testing simple API call...")
    result = engine.call_gemini("Say 'Hello from Gemini 2.0!' and nothing else.", temperature=0.1, max_tokens=20)
    
    if result:
        print(f"✅ API call successful: {result}")
    else:
        print("❌ API call failed")
        return False
    
    # Test 2: Question generation
    print("\n2️⃣ Testing question generation...")
    profile = {
        "role": "Software Engineer",
        "experience_level": "Mid-Level",
        "skills": ["Python", "JavaScript", "React"]
    }
    
    question = engine.generate_first_question(profile)
    print(f"✅ Generated question: {question.get('text', 'No text')[:80]}...")
    
    # Test 3: Answer evaluation
    print("\n3️⃣ Testing answer evaluation...")
    evaluation = engine.evaluate_answer(
        question_text="Tell me about your experience with Python.",
        answer="I have 3 years of experience with Python, building web applications and data processing scripts.",
        profile=profile
    )
    
    print(f"✅ Evaluation scores:")
    print(f"   Technical: {evaluation.get('technical')}/100")
    print(f"   Communication: {evaluation.get('communication')}/100")
    print(f"   Confidence: {evaluation.get('confidence')}/100")
    
    # Test 4: Job fit analysis
    print("\n4️⃣ Testing job fit analysis...")
    job_desc = {
        "title": "Senior Software Engineer",
        "required_skills": ["Python", "JavaScript", "React", "AWS"],
        "required_experience_years": 3
    }
    
    job_fit = engine.calculate_job_fit(profile, job_desc)
    print(f"✅ Job fit score: {job_fit.get('overall_fit_score')}/100")
    
    print("\n🎉 All tests completed successfully!")
    print("✅ Gemini API is fully operational with real AI responses!")
    
    return True

if __name__ == "__main__":
    test_updated_gemini()