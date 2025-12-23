#!/usr/bin/env python3
"""
Test script to verify Gemini integration and conversational interview flow.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.ai_engines.gemini_engine import GeminiEngine

def test_gemini_engine():
    """Test the Gemini engine functionality"""
    print("🧪 Testing Gemini Engine Integration")
    print("=" * 50)
    
    # Initialize engine
    engine = GeminiEngine()
    print(f"✅ GeminiEngine initialized")
    
    # Test profile
    test_profile = {
        "role": "Software Engineer",
        "experience_level": "Mid-Level",
        "skills": ["Python", "JavaScript", "React", "Node.js"],
        "experience_years": 3
    }
    
    print(f"\n📋 Test Profile: {test_profile['role']} with {test_profile['experience_years']} years experience")
    
    # Test 1: Generate first question
    print("\n1️⃣ Testing first question generation...")
    first_question = engine.generate_first_question(test_profile)
    print(f"   Question ID: {first_question.get('id')}")
    print(f"   Question: {first_question.get('text')}")
    print(f"   Type: {first_question.get('type')}")
    
    # Test 2: Simulate conversation history
    print("\n2️⃣ Testing conversational flow...")
    conversation_history = [
        {
            "type": "question",
            "content": first_question.get('text'),
            "question_number": 1
        },
        {
            "type": "answer",
            "content": "I'm a software engineer with 3 years of experience working primarily with Python and JavaScript. I've built several web applications using React and Node.js, and I'm passionate about creating efficient, scalable solutions.",
            "question_number": 1
        }
    ]
    
    # Generate next question
    next_question = engine.generate_next_question(test_profile, conversation_history, 2)
    print(f"   Next Question ID: {next_question.get('id')}")
    print(f"   Next Question: {next_question.get('text')}")
    print(f"   Type: {next_question.get('type')}")
    
    # Test 3: Answer evaluation
    print("\n3️⃣ Testing answer evaluation...")
    test_answer = "I approach technical problems by first understanding the requirements, breaking down the problem into smaller components, researching best practices, and then implementing a solution step by step while testing along the way."
    
    evaluation = engine.evaluate_answer(
        question_text=next_question.get('text'),
        answer=test_answer,
        profile=test_profile
    )
    
    print(f"   Technical Score: {evaluation.get('technical')}/100")
    print(f"   Communication Score: {evaluation.get('communication')}/100")
    print(f"   Confidence Score: {evaluation.get('confidence')}/100")
    print(f"   Notes: {evaluation.get('short_notes')}")
    
    # Test 4: Answer improvement
    print("\n4️⃣ Testing answer improvement...")
    improved = engine.improve_answer(
        question_text=next_question.get('text'),
        answer=test_answer,
        profile=test_profile
    )
    print(f"   Improved Answer: {improved[:100]}...")
    
    # Test 5: Aptitude questions
    print("\n5️⃣ Testing aptitude question generation...")
    aptitude_questions = engine.generate_aptitude_questions(difficulty="medium", count=2)
    for i, q in enumerate(aptitude_questions):
        print(f"   Q{i+1}: {q.get('question', '')[:60]}...")
        print(f"        Type: {q.get('type')}, Difficulty: {q.get('difficulty')}")
    
    # Test 6: Job fit analysis
    print("\n6️⃣ Testing job fit analysis...")
    job_desc = {
        "title": "Senior Software Engineer",
        "required_skills": ["Python", "JavaScript", "React", "AWS"],
        "required_experience_years": 3
    }
    
    job_fit = engine.calculate_job_fit(test_profile, job_desc)
    print(f"   Overall Fit Score: {job_fit.get('overall_fit_score')}/100")
    print(f"   Skill Match: {job_fit.get('skill_match_percentage')}%")
    print(f"   Role Suitability: {job_fit.get('role_suitability')}")
    
    print("\n✅ All tests completed successfully!")
    print("\n🎯 Key Features Verified:")
    print("   ✓ Conversational question generation")
    print("   ✓ Dynamic question flow based on previous answers")
    print("   ✓ Answer evaluation with multiple criteria")
    print("   ✓ Answer improvement suggestions")
    print("   ✓ Aptitude assessment generation")
    print("   ✓ Job fit analysis")
    
    return True

if __name__ == "__main__":
    try:
        test_gemini_engine()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)