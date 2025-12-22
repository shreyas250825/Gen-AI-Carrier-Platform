"""
Google Gemini Engine - Clean AI service layer for all LLM tasks.

Handles:
- Conversational interview question generation
- Answer evaluation and scoring
- Job fit analysis
- Aptitude assessment generation
- Final report generation

Uses Google Gemini API (text-only) for all AI operations.
"""

import os
import json
import logging
import requests
from typing import Dict, List, Any, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

# Gemini Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

if not GEMINI_API_KEY:
    logger.warning("⚠️ GEMINI_API_KEY not found in environment")
else:
    logger.info("✅ Gemini API key loaded")


class GeminiEngine:
    """
    Google Gemini Engine for all AI operations in the interview platform.
    """
    
    def __init__(self):
        self.api_key = GEMINI_API_KEY
        self.base_url = GEMINI_BASE_URL
        
    def call_gemini(self, prompt: str, temperature: float = 0.7, max_tokens: int = 1000) -> str:
        """
        Call Google Gemini API and return response text.
        
        Args:
            prompt: The input prompt for Gemini
            temperature: Creativity level (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated text response
        """
        if not self.api_key:
            logger.error("Gemini API key not configured")
            return ""
        
        try:
            headers = {
                "Content-Type": "application/json",
            }
            
            payload = {
                "contents": [{
                    "parts": [{
                        "text": prompt
                    }]
                }],
                "generationConfig": {
                    "temperature": temperature,
                    "maxOutputTokens": max_tokens,
                    "topP": 0.8,
                    "topK": 10
                }
            }
            
            url = f"{self.base_url}?key={self.api_key}"
            
            logger.info(f"🔄 Gemini request: {len(prompt)} chars")
            
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if "candidates" in data and len(data["candidates"]) > 0:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                logger.info(f"✅ Gemini response: {len(content)} chars")
                return content.strip()
            else:
                logger.error("No candidates in Gemini response")
                return ""
                
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Gemini API request failed: {e}")
            return ""
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            logger.error(f"❌ Gemini response parsing failed: {e}")
            return ""
        except Exception as e:
            logger.error(f"❌ Unexpected Gemini error: {e}")
            return ""

    def generate_first_question(self, profile: Dict[str, Any], persona: str = "professional", interview_type: str = "mixed") -> Dict[str, Any]:
        """
        Generate the first introductory interview question based on candidate profile.
        
        Args:
            profile: Candidate profile with role, experience, skills, etc.
            persona: Interview persona (professional, friendly, etc.)
            interview_type: Type of interview (technical, behavioral, mixed)
            
        Returns:
            Question object with text, type, and metadata
        """
        role = profile.get("role", "Software Engineer")
        experience_level = profile.get("experience_level", "Mid-Level")
        skills = profile.get("skills", [])
        
        prompt = f"""You are conducting a professional interview for a {role} position.

Candidate Profile:
- Role: {role}
- Experience Level: {experience_level}
- Key Skills: {', '.join(skills[:5]) if skills else 'Not specified'}

Generate the first introductory question that:
1. Is warm and welcoming
2. Asks about their background and experience
3. Sets a conversational tone
4. Is relevant to the {role} role

Return ONLY a JSON object with this exact structure:
{{
    "id": "q1",
    "text": "Your question here",
    "type": "introductory",
    "expected_keywords": ["topic1", "topic2"],
    "difficulty": "easy"
}}"""

        response = self.call_gemini(prompt, temperature=0.3)
        
        try:
            question_data = json.loads(response)
            question_data["timestamp"] = datetime.now().isoformat()
            return question_data
        except json.JSONDecodeError:
            # Fallback question
            return {
                "id": "q1",
                "text": f"Thank you for joining us today! Could you start by telling me about your background and experience as a {role}?",
                "type": "introductory",
                "expected_keywords": ["background", "experience", "career"],
                "difficulty": "easy",
                "timestamp": datetime.now().isoformat()
            }

    def generate_next_question(self, profile: Dict[str, Any], conversation_history: List[Dict[str, Any]], question_number: int) -> Dict[str, Any]:
        """
        Generate the next conversational question based on previous Q&A and profile.
        
        Args:
            profile: Candidate profile
            conversation_history: List of previous questions and answers
            question_number: Current question number (2-8)
            
        Returns:
            Next question object
        """
        role = profile.get("role", "Software Engineer")
        
        # Build conversation context
        context = ""
        for item in conversation_history:
            if item.get("type") == "question":
                context += f"Q{item.get('question_number', '')}: {item.get('content', '')}\n"
            elif item.get("type") == "answer":
                context += f"A{item.get('question_number', '')}: {item.get('content', '')}\n\n"
        
        # Determine question focus based on number
        if question_number <= 3:
            focus = "technical skills and experience"
        elif question_number <= 5:
            focus = "problem-solving and analytical thinking"
        elif question_number <= 7:
            focus = "behavioral and situational scenarios"
        else:
            focus = "role fit and career goals"
        
        prompt = f"""You are conducting a professional interview for a {role} position.

Previous Conversation:
{context}

Candidate Profile:
- Role: {role}
- Experience Level: {profile.get('experience_level', 'Mid-Level')}

This is question #{question_number} of 8. Focus on: {focus}

Generate the next question that:
1. Builds naturally on the previous conversation
2. Explores {focus} relevant to {role}
3. Feels conversational, not scripted
4. Provides insight into the candidate's capabilities

Return ONLY a JSON object with this exact structure:
{{
    "id": "q{question_number}",
    "text": "Your question here",
    "type": "technical|behavioral|situational|role_fit",
    "expected_keywords": ["topic1", "topic2"],
    "difficulty": "easy|medium|hard"
}}"""

        response = self.call_gemini(prompt, temperature=0.5)
        
        try:
            question_data = json.loads(response)
            question_data["timestamp"] = datetime.now().isoformat()
            return question_data
        except json.JSONDecodeError:
            # Fallback question based on question number
            fallback_questions = {
                2: f"What specific technologies or tools do you use most in your {role} work?",
                3: "Can you walk me through how you approach solving complex technical problems?",
                4: "Tell me about a challenging project you've worked on recently.",
                5: "How do you handle working with tight deadlines and changing requirements?",
                6: "Describe a time when you had to collaborate with a difficult team member.",
                7: "What interests you most about this role and our company?",
                8: "Where do you see your career heading in the next few years?"
            }
            
            return {
                "id": f"q{question_number}",
                "text": fallback_questions.get(question_number, "Tell me more about your experience."),
                "type": "general",
                "expected_keywords": ["experience", "skills"],
                "difficulty": "medium",
                "timestamp": datetime.now().isoformat()
            }

    def evaluate_answer(self, question_text: str, answer: str, profile: Dict[str, Any], conversation_history: List[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Evaluate candidate's answer using Gemini AI.
        
        Args:
            question_text: The interview question
            answer: Candidate's response
            profile: Candidate profile
            conversation_history: Previous conversation context
            
        Returns:
            Evaluation results with scores and feedback
        """
        if not answer or len(answer.strip()) < 10:
            return {
                "technical": 20,
                "communication": 20,
                "confidence": 20,
                "relevance": 20,
                "short_notes": "Answer was too brief. Please provide more detailed responses.",
                "timestamp": datetime.now().isoformat()
            }
        
        role = profile.get("role", "Software Engineer")
        
        prompt = f"""Evaluate this interview answer professionally and objectively.

Question: {question_text}
Candidate Role: {role}

Candidate's Answer: {answer}

Provide a comprehensive evaluation with scores (0-100) for:
- Technical competency
- Communication clarity
- Confidence level
- Relevance to question

Return ONLY a JSON object with this exact structure:
{{
    "technical": 85,
    "communication": 90,
    "confidence": 80,
    "relevance": 85,
    "short_notes": "Brief feedback about the answer quality (max 100 chars)"
}}"""

        response = self.call_gemini(prompt, temperature=0.2)
        
        try:
            evaluation = json.loads(response)
            evaluation["timestamp"] = datetime.now().isoformat()
            return evaluation
        except json.JSONDecodeError:
            # Fallback evaluation
            score = min(80, max(40, len(answer.split()) * 2))  # Basic length-based scoring
            return {
                "technical": score,
                "communication": score,
                "confidence": score,
                "relevance": score,
                "short_notes": "Your answer shows understanding. Consider adding more specific examples.",
                "timestamp": datetime.now().isoformat()
            }

    def improve_answer(self, question_text: str, answer: str, profile: Dict[str, Any]) -> str:
        """
        Generate an improved version of the candidate's answer.
        
        Args:
            question_text: The interview question
            answer: Candidate's original response
            profile: Candidate profile
            
        Returns:
            Improved answer text
        """
        role = profile.get("role", "Software Engineer")
        
        prompt = f"""Improve this interview answer to be more professional and comprehensive.

Question: {question_text}
Role: {role}
Original Answer: {answer}

Provide an improved version that:
1. Is more structured and clear
2. Includes specific examples
3. Demonstrates technical competency
4. Shows professional communication

Return ONLY the improved answer text (no JSON, no quotes)."""

        response = self.call_gemini(prompt, temperature=0.3, max_tokens=200)
        
        if response and len(response.strip()) > 20:
            return response.strip()
        else:
            return f"As a {role}, I would approach this by leveraging my experience with relevant technologies and following best practices to ensure quality results."

    def generate_final_report(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive interview report using Gemini AI.
        
        Args:
            session_data: Complete interview session with questions, answers, evaluations
            
        Returns:
            Final report with scores, analysis, and recommendations
        """
        profile = session_data.get("profile", {})
        evaluations = session_data.get("evaluations", [])
        conversation_history = session_data.get("conversation_history", [])
        
        if not evaluations:
            return {
                "overall_summary": "No evaluation data available for this session.",
                "technical_strengths": [],
                "technical_gaps": [],
                "communication_score": 0,
                "behavioral_score": 0,
                "improved_answers": [],
                "recommendations": []
            }
        
        # Calculate average scores
        avg_technical = sum(e.get("technical", 0) for e in evaluations) / len(evaluations)
        avg_communication = sum(e.get("communication", 0) for e in evaluations) / len(evaluations)
        avg_confidence = sum(e.get("confidence", 0) for e in evaluations) / len(evaluations)
        
        role = profile.get("role", "Software Engineer")
        
        prompt = f"""Generate a comprehensive interview report for a {role} candidate.

Interview Performance:
- Average Technical Score: {avg_technical:.1f}/100
- Average Communication Score: {avg_communication:.1f}/100
- Average Confidence Score: {avg_confidence:.1f}/100
- Total Questions: {len(evaluations)}

Create a professional summary with strengths, gaps, and recommendations.

Return ONLY a JSON object with this exact structure:
{{
    "overall_summary": "Comprehensive summary of performance",
    "technical_strengths": ["strength1", "strength2"],
    "technical_gaps": ["gap1", "gap2"],
    "communication_score": 85,
    "behavioral_score": 80,
    "improved_answers": [],
    "recommendations": ["recommendation1", "recommendation2"]
}}"""

        response = self.call_gemini(prompt, temperature=0.3)
        
        try:
            report = json.loads(response)
            return report
        except json.JSONDecodeError:
            # Fallback report
            return {
                "overall_summary": f"Completed interview with average scores: Technical {avg_technical:.1f}%, Communication {avg_communication:.1f}%, Confidence {avg_confidence:.1f}%.",
                "technical_strengths": ["Demonstrated technical knowledge"] if avg_technical >= 70 else [],
                "technical_gaps": ["Continue developing technical skills"] if avg_technical < 70 else [],
                "communication_score": int(avg_communication),
                "behavioral_score": int(avg_confidence),
                "improved_answers": [],
                "recommendations": ["Practice more interview scenarios", "Focus on providing specific examples"]
            }

    def generate_aptitude_questions(self, difficulty: str = "medium", count: int = 10) -> List[Dict[str, Any]]:
        """
        Generate aptitude and logical reasoning questions using Gemini.
        
        Args:
            difficulty: easy, medium, hard
            count: Number of questions to generate
            
        Returns:
            List of aptitude questions with answers and explanations
        """
        prompt = f"""Generate {count} aptitude and logical reasoning questions for technical interview assessment.

Requirements:
- Difficulty: {difficulty}
- Focus on: problem-solving, analytical thinking, decision making
- Include: quantitative reasoning, logical puzzles, pattern recognition
- Each question should have 4 multiple choice options
- Provide correct answer and reasoning steps

Return ONLY a JSON array with this exact structure:
[
    {{
        "id": "apt_1",
        "question": "Question text here",
        "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
        "correct_answer": "A) Option 1",
        "explanation": "Step-by-step reasoning",
        "type": "quantitative|logical|pattern",
        "difficulty": "{difficulty}"
    }}
]"""

        response = self.call_gemini(prompt, temperature=0.4, max_tokens=2000)
        
        try:
            questions = json.loads(response)
            for i, q in enumerate(questions):
                q["id"] = f"apt_{i+1}"
                q["timestamp"] = datetime.now().isoformat()
            return questions
        except json.JSONDecodeError:
            # Return fallback questions
            return [{
                "id": "apt_1",
                "question": "If a team of 4 developers can complete a project in 6 days, how many days will it take for 6 developers?",
                "options": ["A) 4 days", "B) 3 days", "C) 5 days", "D) 2 days"],
                "correct_answer": "A) 4 days",
                "explanation": "Work = People × Days. 4×6 = 24 person-days. For 6 people: 24÷6 = 4 days",
                "type": "quantitative",
                "difficulty": difficulty,
                "timestamp": datetime.now().isoformat()
            }]

    def evaluate_aptitude_answer(self, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """
        Evaluate aptitude question answer.
        
        Args:
            question: Question object with correct answer
            user_answer: User's selected answer
            
        Returns:
            Evaluation result
        """
        correct_answer = question.get("correct_answer", "")
        explanation = question.get("explanation", "")
        
        # Simple exact match for now
        is_correct = user_answer.strip().lower() == correct_answer.lower()
        
        score = 100 if is_correct else 0
        
        return {
            "correct": is_correct,
            "score": score,
            "correct_answer": correct_answer,
            "explanation": explanation,
            "user_answer": user_answer
        }

    def calculate_job_fit(self, resume_data: Dict[str, Any], job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze job fit between candidate resume and job requirements using Gemini.
        
        Args:
            resume_data: Parsed resume information
            job_description: Job requirements and description
            
        Returns:
            Job fit analysis with scores and recommendations
        """
        skills = resume_data.get("skills", [])
        experience = resume_data.get("experience_years", 0)
        role = resume_data.get("role", "")
        
        required_skills = job_description.get("required_skills", [])
        job_title = job_description.get("title", "")
        required_experience = job_description.get("required_experience_years", 0)
        
        prompt = f"""Analyze job fit between candidate and position requirements.

Candidate Profile:
- Current Role: {role}
- Experience: {experience} years
- Skills: {', '.join(skills)}

Job Requirements:
- Position: {job_title}
- Required Experience: {required_experience} years
- Required Skills: {', '.join(required_skills)}

Provide comprehensive job fit analysis with specific scores and actionable recommendations.

Return ONLY a JSON object with this exact structure:
{{
    "overall_fit_score": 85,
    "skill_match_percentage": 80,
    "experience_match_percentage": 90,
    "missing_required_skills": ["skill1", "skill2"],
    "missing_preferred_skills": [],
    "matched_skills": ["skill1", "skill2"],
    "role_suitability": "Excellent fit - highly recommended",
    "recommendations": ["recommendation1", "recommendation2"]
}}"""

        response = self.call_gemini(prompt, temperature=0.2)
        
        try:
            analysis = json.loads(response)
            analysis["timestamp"] = datetime.now().isoformat()
            return analysis
        except json.JSONDecodeError:
            # Fallback analysis
            skill_overlap = len(set(skills) & set(required_skills))
            skill_match = (skill_overlap / len(required_skills) * 100) if required_skills else 50
            exp_match = min(100, (experience / required_experience * 100)) if required_experience > 0 else 75
            
            return {
                "overall_fit_score": round((skill_match + exp_match) / 2),
                "skill_match_percentage": round(skill_match),
                "experience_match_percentage": round(exp_match),
                "missing_required_skills": list(set(required_skills) - set(skills)),
                "missing_preferred_skills": [],
                "matched_skills": list(set(skills) & set(required_skills)),
                "role_suitability": "Good fit with some skill development needed",
                "recommendations": ["Develop missing technical skills", "Gain more relevant experience"],
                "timestamp": datetime.now().isoformat()
            }
