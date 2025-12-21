"""
Cloud LLM Engine - Updated to use Three-Level Intelligence Architecture
Maintains backward compatibility while leveraging the new intelligence system.
"""
from typing import Any, Dict, List

# Import the new intelligence engine
from app.ai_engines.intelligence_engine import intelligence_engine

def generate_questions(profile: Dict[str, Any], interview_type: str, persona: str = "professional", round_name: str = "round1") -> List[Dict[str, Any]]:
    """
    Generate 6-7 interview questions using the three-level intelligence system.
    
    This function now uses the IntelligenceEngine which automatically falls back through:
    Level 3 (AWS Cloud AI) -> Level 2 (Local AI/Ollama) -> Level 1 (Deterministic)
    """
    questions = intelligence_engine.generate_questions(profile, interview_type, count=7)
    
    # Ensure backward compatibility - add missing fields if needed
    for q in questions:
        if "followups" not in q:
            q["followups"] = ""
        if "type" not in q:
            q["type"] = interview_type
        if "expected_keywords" not in q:
            q["expected_keywords"] = []
        if "expected_length" not in q:
            q["expected_length"] = "medium"
        if "ideal_answer" not in q:
            q["ideal_answer"] = ""
    
    return questions


def evaluate_answer(question: str, answer: str, profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Evaluate answer using the three-level intelligence system.
    
    Automatically falls back through intelligence levels for reliability.
    """
    # Extract expected_keywords from question if available
    expected_keywords = []
    question_text = ""
    
    if isinstance(question, dict):
        expected_keywords = question.get("expected_keywords", [])
        question_text = question.get("text", question.get("question", str(question)))
    else:
        question_text = str(question)
    
    result = intelligence_engine.evaluate_answer(question_text, answer, expected_keywords, profile)
    
    # Ensure backward compatibility - map fields
    if "notes" not in result and "short_notes" in result:
        result["notes"] = result["short_notes"]
    # Add relevance as notes if not present (for backward compatibility)
    if "relevance" in result and "notes" not in result:
        result["notes"] = result.get("short_notes", f"Relevance score: {result['relevance']}")
    
    return result


def improve_answer(question: str, answer: str, profile: Dict[str, Any]) -> str:
    """
    Improve answer using the three-level intelligence system.
    """
    if isinstance(question, dict):
        question_text = question.get("text", question.get("question", str(question)))
    else:
        question_text = str(question)
    
    return intelligence_engine.improve_answer(question_text, answer, profile)


def generate_final_report(session_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate final report using the three-level intelligence system.
    """
    return intelligence_engine.generate_final_report(session_data)


def generate_interviewer_response(question: str, candidate_answer: str, conversation_history: list = None) -> str:
    """
    Generate interviewer response - currently uses Level 1 deterministic responses.
    TODO: Enhance with Level 2 and Level 3 implementations.
    """
    # For now, use simple responses - can be enhanced with intelligence engine
    responses = [
        "Thank you for sharing that. Can you elaborate on the specific challenges you faced?",
        "That's interesting. How did you measure the success of that approach?",
        "Good point. What would you do differently if you encountered a similar situation again?",
        "I appreciate that example. Can you walk me through your decision-making process?",
        "That sounds like valuable experience. How did that project impact your team or organization?"
    ]
    
    import random
    return random.choice(responses)


# ============================================================================
# NEW FEATURES: APTITUDE & JOB FIT ASSESSMENT
# ============================================================================

def generate_aptitude_questions(difficulty: str = "medium", count: int = 5) -> List[Dict[str, Any]]:
    """
    Generate aptitude and logical reasoning questions.
    
    NEW FEATURE: Supports quantitative, logical, analytical, and pattern recognition questions.
    """
    return intelligence_engine.generate_aptitude_questions(difficulty, count)


def evaluate_aptitude_answer(question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
    """
    Evaluate aptitude question answer.
    
    NEW FEATURE: Provides correct/incorrect feedback with explanations.
    """
    return intelligence_engine.evaluate_aptitude_answer(question, user_answer)


def calculate_job_fit(resume_data: Dict[str, Any], job_description: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate job fit score and role matching analysis.
    
    NEW FEATURE: AI-based job fit analysis with skill matching and recommendations.
    
    Args:
        resume_data: Parsed resume data with skills, experience, etc.
        job_description: Job requirements with required/preferred skills
        
    Returns:
        Dict with overall_fit_score, skill_match_percentage, missing_skills, recommendations
    """
    return intelligence_engine.calculate_job_fit(resume_data, job_description)


