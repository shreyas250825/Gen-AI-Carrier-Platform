"""
Three-Level Intelligence Architecture for GenAI Career Intelligence Platform

Level 1: Deterministic Intelligence (Fallback Layer) - Always works, 100% uptime
Level 2: Local AI Intelligence (Ollama) - Optional offline AI capability  
Level 3: Cloud AI Intelligence (AWS-Aligned) - Pluggable cloud AI interface

This engine ensures reliability by falling back through levels when higher levels fail.
"""

import json
import logging
import random
import time
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime

# Import existing engines for backward compatibility
from app.ai_engines.local_llm_engine import call_local_llm
from app.ai_engines.openrouter_engine import call_openrouter

logger = logging.getLogger(__name__)

class IntelligenceEngine:
    """
    Three-level intelligence system with automatic fallback.
    
    Architecture:
    Level 3 (Cloud AI) -> Level 2 (Local AI) -> Level 1 (Deterministic)
    """
    
    def __init__(self):
        self.level_1_enabled = True  # Always enabled
        self.level_2_enabled = self._check_ollama_availability()
        self.level_3_enabled = self._check_aws_availability()
        
        logger.info(f"Intelligence Engine initialized:")
        logger.info(f"  Level 1 (Deterministic): {'✅' if self.level_1_enabled else '❌'}")
        logger.info(f"  Level 2 (Local AI): {'✅' if self.level_2_enabled else '❌'}")
        logger.info(f"  Level 3 (Cloud AI): {'✅' if self.level_3_enabled else '❌'}")

    def _check_ollama_availability(self) -> bool:
        """Check if Ollama is running locally"""
        try:
            import requests
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def _check_aws_availability(self) -> bool:
        """Check if AWS services are configured (mock for now)"""
        # TODO: Replace with actual AWS Bedrock availability check
        # For now, return False to demonstrate fallback behavior
        return False

    # ============================================================================
    # LEVEL 1: DETERMINISTIC INTELLIGENCE (FALLBACK LAYER)
    # ============================================================================

    def _level1_generate_questions(self, profile: Dict[str, Any], interview_type: str, count: int = 7) -> List[Dict[str, Any]]:
        """
        Level 1: Rule-based question generation that looks AI-like but is deterministic.
        Uses role, skills, and experience level to create contextual questions.
        """
        logger.info("🔧 Using Level 1 (Deterministic) for question generation")
        
        role = profile.get("role", "Software Engineer")
        skills = profile.get("skills", [])
        experience_level = profile.get("experience_level", "Mid-Level")
        experience_years = profile.get("experience_years", 3)
        
        # Question templates with dynamic insertion
        templates = {
            "behavioral": [
                {
                    "template": "Tell me about a time when you had to {challenge} in your {role} role.",
                    "challenges": ["work under tight deadlines", "resolve a conflict with a team member", "learn a new technology quickly", "lead a difficult project"],
                    "followups": "What was the outcome?",
                    "keywords": ["leadership", "problem-solving", "communication", "teamwork"]
                },
                {
                    "template": "Describe how you would handle {situation} as a {role}.",
                    "situations": ["a disagreement with your manager", "a project falling behind schedule", "a team member not meeting expectations", "changing requirements mid-project"],
                    "followups": "How would you prevent this in the future?",
                    "keywords": ["conflict resolution", "time management", "leadership", "adaptability"]
                },
                {
                    "template": "Give me an example of when you {action} in your previous {role} experience.",
                    "actions": ["improved a process", "mentored a junior colleague", "solved a complex problem", "took initiative on a project"],
                    "followups": "What impact did this have?",
                    "keywords": ["initiative", "mentoring", "process improvement", "impact"]
                }
            ],
            "technical": [
                {
                    "template": "How would you approach {technical_challenge} in {domain}?",
                    "technical_challenges": ["optimizing database performance", "designing a scalable system", "implementing security measures", "debugging a production issue"],
                    "domains": self._get_technical_domain(skills),
                    "followups": "What tools would you use?",
                    "keywords": ["architecture", "performance", "security", "debugging"]
                },
                {
                    "template": "Explain how you would implement {feature} using {technology}.",
                    "features": ["user authentication", "real-time notifications", "data caching", "API rate limiting"],
                    "technologies": skills[:3] if skills else ["modern web technologies"],
                    "followups": "What challenges might you face?",
                    "keywords": ["implementation", "best practices", "scalability", "security"]
                },
                {
                    "template": "Walk me through your process for {task} in a {role} position.",
                    "tasks": ["code review", "system design", "performance optimization", "testing strategy"],
                    "followups": "How do you ensure quality?",
                    "keywords": ["process", "quality", "best practices", "methodology"]
                }
            ],
            "aptitude": [
                {
                    "template": "If you have {scenario}, how would you prioritize and solve this?",
                    "scenarios": ["multiple urgent tasks with the same deadline", "limited resources for a critical project", "conflicting requirements from different stakeholders"],
                    "followups": "What factors would you consider?",
                    "keywords": ["prioritization", "resource management", "decision making", "analysis"]
                }
            ]
        }
        
        questions = []
        question_types = self._determine_question_mix(interview_type, count)
        
        for i, q_type in enumerate(question_types):
            template_group = templates.get(q_type, templates["behavioral"])
            template_data = random.choice(template_group)
            
            # Generate question text with dynamic content
            question_text = self._fill_template(template_data, role, skills, experience_level)
            
            questions.append({
                "id": f"q{i+1}",
                "text": question_text,
                "followups": template_data["followups"],
                "type": q_type,
                "difficulty": self._determine_difficulty(experience_years),
                "expected_keywords": template_data["keywords"],
                "expected_length": "medium" if q_type == "behavioral" else "long",
                "ideal_answer": self._generate_ideal_answer(question_text, q_type, role)
            })
        
        return questions

    def _level1_evaluate_answer(self, question: str, answer: str, expected_keywords: List[str], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Level 1: Rule-based answer evaluation using keyword matching and heuristics.
        """
        logger.info("🔧 Using Level 1 (Deterministic) for answer evaluation")
        
        answer_lower = answer.lower()
        question_lower = question.lower()
        
        # Keyword matching score
        keyword_matches = sum(1 for keyword in expected_keywords if keyword.lower() in answer_lower)
        keyword_score = min(100, (keyword_matches / max(len(expected_keywords), 1)) * 100)
        
        # Length and structure analysis
        word_count = len(answer.split())
        structure_score = self._analyze_answer_structure(answer)
        
        # Technical content detection
        technical_indicators = ["implement", "design", "architecture", "algorithm", "database", "api", "framework", "library", "performance", "security"]
        technical_matches = sum(1 for indicator in technical_indicators if indicator in answer_lower)
        technical_score = min(100, 60 + (technical_matches * 8))
        
        # Communication quality heuristics
        communication_score = self._analyze_communication_quality(answer)
        
        # Confidence indicators
        confidence_indicators = ["I", "my experience", "I've worked", "I implemented", "I designed", "I led"]
        confidence_matches = sum(1 for indicator in confidence_indicators if indicator.lower() in answer_lower)
        confidence_score = min(100, 50 + (confidence_matches * 10))
        
        # Relevance to question
        relevance_score = self._calculate_relevance(question_lower, answer_lower)
        
        return {
            "technical": int(technical_score),
            "communication": int(communication_score),
            "confidence": int(confidence_score),
            "relevance": int(relevance_score),
            "short_notes": f"Keyword matches: {keyword_matches}/{len(expected_keywords)}. Word count: {word_count}. Structure score: {structure_score}."
        }

    def _level1_improve_answer(self, question: str, answer: str, profile: Dict[str, Any]) -> str:
        """
        Level 1: Template-based answer improvement using best practices.
        """
        logger.info("🔧 Using Level 1 (Deterministic) for answer improvement")
        
        role = profile.get("role", "professional")
        
        # Analyze current answer
        word_count = len(answer.split())
        has_example = any(word in answer.lower() for word in ["example", "instance", "time when", "project", "experience"])
        has_metrics = any(char.isdigit() for char in answer)
        
        improvements = []
        
        if word_count < 30:
            improvements.append("provide more detailed explanation")
        if not has_example:
            improvements.append("include a specific example from your experience")
        if not has_metrics:
            improvements.append("add quantifiable results or metrics")
        
        # Generate improved version using templates
        if "tell me about yourself" in question.lower():
            return f"I'm a {role} with {profile.get('experience_years', 3)} years of experience. In my most recent role, I specialized in {', '.join(profile.get('skills', ['various technologies'])[:3])}. For example, I led a project that improved system performance by 30% through optimization techniques. I'm passionate about continuous learning and am excited about opportunities to contribute to innovative projects."
        
        elif "challenging project" in question.lower():
            return f"I worked on a complex {role.lower()} project where we needed to integrate multiple systems under a tight deadline. The main challenge was ensuring data consistency across different platforms. I approached this by first analyzing the data flow, then implementing a robust synchronization mechanism. The result was a 40% improvement in data accuracy and reduced processing time by 25%."
        
        else:
            # Generic improvement
            base_answer = answer[:100] + "..." if len(answer) > 100 else answer
            return f"Building on that, {base_answer} Specifically, in my experience as a {role}, I've found that the key is to focus on measurable outcomes. For instance, when I implemented similar solutions, we achieved significant improvements in both efficiency and user satisfaction."

    def _level1_generate_final_report(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Level 1: Rule-based final report generation using score analysis.
        """
        logger.info("🔧 Using Level 1 (Deterministic) for final report generation")
        
        evaluations = session_data.get("evaluations", [])
        questions = session_data.get("questions", [])
        
        if not evaluations:
            return self._empty_report()
        
        # Calculate averages
        avg_technical = sum(e.get("technical", 0) for e in evaluations) / len(evaluations)
        avg_communication = sum(e.get("communication", 0) for e in evaluations) / len(evaluations)
        avg_confidence = sum(e.get("confidence", 0) for e in evaluations) / len(evaluations)
        avg_relevance = sum(e.get("relevance", 0) for e in evaluations) / len(evaluations)
        
        # Generate insights based on scores
        strengths = []
        gaps = []
        recommendations = []
        
        if avg_technical >= 80:
            strengths.append("Strong technical knowledge and problem-solving skills")
        elif avg_technical < 60:
            gaps.append("Technical concepts need strengthening")
            recommendations.append("Review fundamental concepts in your field")
        
        if avg_communication >= 80:
            strengths.append("Clear and effective communication")
        elif avg_communication < 60:
            gaps.append("Communication clarity could be improved")
            recommendations.append("Practice structuring answers using the STAR method")
        
        if avg_confidence >= 80:
            strengths.append("Confident and professional demeanor")
        elif avg_confidence < 60:
            gaps.append("Could demonstrate more confidence in responses")
            recommendations.append("Practice speaking about your achievements with confidence")
        
        # Generate overall summary
        overall_performance = "excellent" if (avg_technical + avg_communication + avg_confidence) / 3 >= 80 else \
                            "good" if (avg_technical + avg_communication + avg_confidence) / 3 >= 70 else \
                            "satisfactory" if (avg_technical + avg_communication + avg_confidence) / 3 >= 60 else "needs improvement"
        
        summary = f"Overall performance was {overall_performance}. Technical competency averaged {avg_technical:.1f}%, communication skills {avg_communication:.1f}%, and confidence level {avg_confidence:.1f}%."
        
        return {
            "overall_summary": summary,
            "technical_strengths": strengths,
            "technical_gaps": gaps,
            "communication_score": int(avg_communication),
            "behavioral_score": int(avg_confidence),
            "improved_answers": [],
            "recommendations": recommendations
        }

    # ============================================================================
    # LEVEL 2: LOCAL AI INTELLIGENCE (OLLAMA)
    # ============================================================================

    def _level2_generate_questions(self, profile: Dict[str, Any], interview_type: str, count: int = 7) -> Optional[List[Dict[str, Any]]]:
        """
        Level 2: Use Ollama for question generation with short, deterministic prompts.
        """
        if not self.level_2_enabled:
            return None
            
        logger.info("🤖 Using Level 2 (Local AI/Ollama) for question generation")
        
        try:
            import requests
            
            role = profile.get("role", "Software Engineer")
            skills = ", ".join(profile.get("skills", [])[:5])
            experience = profile.get("experience_level", "Mid-Level")
            
            prompt = f"""Generate {count} {interview_type} interview questions for a {experience} {role}.
Skills: {skills}

Return JSON array with objects containing: id, text, followups, type, difficulty, expected_keywords, expected_length.
Keep questions concise and relevant."""

            payload = {
                "model": "llama3.2:1b",  # Use lightweight model
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,
                    "num_predict": 800
                }
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                
                # Try to parse JSON from response
                questions = self._parse_json_from_text(text)
                if isinstance(questions, list) and len(questions) >= count:
                    return questions[:count]
            
        except Exception as e:
            logger.warning(f"Level 2 (Ollama) failed: {e}")
            self.level_2_enabled = False  # Disable for this session
        
        return None

    def _level2_evaluate_answer(self, question: str, answer: str, expected_keywords: List[str], profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Level 2: Use Ollama for answer evaluation.
        """
        if not self.level_2_enabled:
            return None
            
        logger.info("🤖 Using Level 2 (Local AI/Ollama) for answer evaluation")
        
        try:
            import requests
            
            prompt = f"""Evaluate this interview answer on a scale of 0-100:

Question: {question}
Answer: {answer}
Expected keywords: {', '.join(expected_keywords)}

Return JSON with: technical, communication, confidence, relevance, short_notes.
Be concise and objective."""

            payload = {
                "model": "llama3.2:1b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 200
                }
            }
            
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=15)
            
            if response.status_code == 200:
                result = response.json()
                text = result.get("response", "")
                
                evaluation = self._parse_json_from_text(text)
                if isinstance(evaluation, dict) and "technical" in evaluation:
                    return evaluation
            
        except Exception as e:
            logger.warning(f"Level 2 (Ollama) evaluation failed: {e}")
            self.level_2_enabled = False
        
        return None

    # ============================================================================
    # LEVEL 3: CLOUD AI INTELLIGENCE (AWS-ALIGNED)
    # ============================================================================

    def _level3_generate_questions(self, profile: Dict[str, Any], interview_type: str, count: int = 7) -> Optional[List[Dict[str, Any]]]:
        """
        Level 3: AWS Bedrock interface for question generation.
        
        NOTE: This is a pluggable interface for AWS services.
        Currently mocked for demonstration - replace with actual AWS Bedrock calls.
        """
        if not self.level_3_enabled:
            return None
            
        logger.info("☁️ Using Level 3 (AWS Cloud AI) for question generation")
        
        # TODO: Replace with actual AWS Bedrock implementation
        # Example of how this would work:
        """
        import boto3
        
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps({
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 1000,
                'temperature': 0.3
            })
        )
        """
        
        # For now, return None to demonstrate fallback behavior
        logger.info("☁️ AWS Bedrock not configured - falling back to lower level")
        return None

    def _level3_evaluate_answer(self, question: str, answer: str, expected_keywords: List[str], profile: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Level 3: AWS Bedrock interface for answer evaluation.
        
        NOTE: This would integrate with AWS Bedrock for production use.
        """
        if not self.level_3_enabled:
            return None
            
        logger.info("☁️ Using Level 3 (AWS Cloud AI) for answer evaluation")
        
        # TODO: Implement AWS Bedrock evaluation
        # This would call AWS Bedrock with the evaluation prompt
        
        return None

    # ============================================================================
    # PUBLIC API - AUTOMATIC FALLBACK THROUGH LEVELS
    # ============================================================================

    def generate_questions(self, profile: Dict[str, Any], interview_type: str, count: int = 7) -> List[Dict[str, Any]]:
        """
        Generate questions with automatic fallback through intelligence levels.
        """
        # Try Level 3 (Cloud AI) first
        result = self._level3_generate_questions(profile, interview_type, count)
        if result:
            return result
        
        # Try Level 2 (Local AI) second
        result = self._level2_generate_questions(profile, interview_type, count)
        if result:
            return result
        
        # Fall back to Level 1 (Deterministic) - always works
        return self._level1_generate_questions(profile, interview_type, count)

    def evaluate_answer(self, question: str, answer: str, expected_keywords: List[str], profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate answer with automatic fallback through intelligence levels.
        """
        # Try Level 3 (Cloud AI) first
        result = self._level3_evaluate_answer(question, answer, expected_keywords, profile)
        if result:
            return result
        
        # Try Level 2 (Local AI) second
        result = self._level2_evaluate_answer(question, answer, expected_keywords, profile)
        if result:
            return result
        
        # Fall back to Level 1 (Deterministic) - always works
        return self._level1_evaluate_answer(question, answer, expected_keywords, profile)

    def improve_answer(self, question: str, answer: str, profile: Dict[str, Any]) -> str:
        """
        Improve answer with automatic fallback through intelligence levels.
        """
        # For now, use Level 1 deterministic improvement
        # TODO: Add Level 2 and Level 3 implementations
        return self._level1_improve_answer(question, answer, profile)

    def generate_final_report(self, session_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate final report with automatic fallback through intelligence levels.
        """
        # For now, use Level 1 deterministic report generation
        # TODO: Add Level 2 and Level 3 implementations
        return self._level1_generate_final_report(session_data)

    # ============================================================================
    # APTITUDE & LOGICAL REASONING ASSESSMENT
    # ============================================================================

    def generate_aptitude_questions(self, difficulty: str = "medium", count: int = 5) -> List[Dict[str, Any]]:
        """
        Generate aptitude and logical reasoning questions.
        """
        logger.info(f"🧠 Generating {count} aptitude questions (difficulty: {difficulty})")
        
        question_types = ["quantitative", "logical", "analytical", "pattern", "verbal"]
        questions = []
        
        for i in range(count):
            q_type = random.choice(question_types)
            question = self._generate_aptitude_question(q_type, difficulty, i+1)
            questions.append(question)
        
        return questions

    def evaluate_aptitude_answer(self, question: Dict[str, Any], user_answer: str) -> Dict[str, Any]:
        """
        Evaluate aptitude question answer.
        """
        correct_answer = question.get("correct_answer", "")
        explanation = question.get("explanation", "")
        
        # Simple exact match for now - could be enhanced with fuzzy matching
        is_correct = user_answer.strip().lower() == correct_answer.lower()
        
        score = 100 if is_correct else 0
        
        return {
            "correct": is_correct,
            "score": score,
            "correct_answer": correct_answer,
            "explanation": explanation,
            "user_answer": user_answer
        }

    # ============================================================================
    # JOB FIT & ROLE MATCHING
    # ============================================================================

    def calculate_job_fit(self, resume_data: Dict[str, Any], job_description: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculate job fit score and role matching analysis.
        """
        logger.info("🎯 Calculating job fit and role matching")
        
        candidate_skills = set(skill.lower() for skill in resume_data.get("skills", []))
        required_skills = set(skill.lower() for skill in job_description.get("required_skills", []))
        preferred_skills = set(skill.lower() for skill in job_description.get("preferred_skills", []))
        
        # Calculate skill matches
        required_matches = candidate_skills.intersection(required_skills)
        preferred_matches = candidate_skills.intersection(preferred_skills)
        
        # Calculate scores
        required_score = (len(required_matches) / max(len(required_skills), 1)) * 100
        preferred_score = (len(preferred_matches) / max(len(preferred_skills), 1)) * 100
        
        # Experience matching
        candidate_years = resume_data.get("experience_years", 0)
        required_years = job_description.get("required_experience_years", 0)
        experience_score = min(100, (candidate_years / max(required_years, 1)) * 100)
        
        # Overall job fit calculation
        overall_fit = (required_score * 0.5) + (preferred_score * 0.3) + (experience_score * 0.2)
        
        # Generate missing skills
        missing_required = required_skills - candidate_skills
        missing_preferred = preferred_skills - candidate_skills
        
        # Role suitability assessment
        suitability = self._assess_role_suitability(overall_fit, required_score, experience_score)
        
        return {
            "overall_fit_score": round(overall_fit, 1),
            "skill_match_percentage": round(required_score, 1),
            "experience_match_percentage": round(experience_score, 1),
            "missing_required_skills": list(missing_required),
            "missing_preferred_skills": list(missing_preferred),
            "matched_skills": list(required_matches.union(preferred_matches)),
            "role_suitability": suitability,
            "recommendations": self._generate_job_fit_recommendations(overall_fit, missing_required, missing_preferred)
        }

    # ============================================================================
    # HELPER METHODS
    # ============================================================================

    def _get_technical_domain(self, skills: List[str]) -> List[str]:
        """Map skills to technical domains"""
        domains = []
        skill_lower = [s.lower() for s in skills]
        
        if any(s in skill_lower for s in ["python", "java", "javascript", "c++", "go"]):
            domains.append("software development")
        if any(s in skill_lower for s in ["react", "angular", "vue", "html", "css"]):
            domains.append("frontend development")
        if any(s in skill_lower for s in ["node.js", "django", "flask", "spring", "express"]):
            domains.append("backend development")
        if any(s in skill_lower for s in ["aws", "azure", "docker", "kubernetes", "terraform"]):
            domains.append("cloud infrastructure")
        if any(s in skill_lower for s in ["mysql", "postgresql", "mongodb", "redis"]):
            domains.append("database management")
        
        return domains if domains else ["software engineering"]

    def _determine_question_mix(self, interview_type: str, count: int) -> List[str]:
        """Determine the mix of question types based on interview type"""
        if interview_type.lower() == "technical":
            return ["technical"] * (count - 1) + ["behavioral"]
        elif interview_type.lower() == "behavioral":
            return ["behavioral"] * (count - 1) + ["technical"]
        else:  # mixed
            mix = []
            for i in range(count):
                if i % 3 == 0:
                    mix.append("aptitude")
                elif i % 2 == 0:
                    mix.append("technical")
                else:
                    mix.append("behavioral")
            return mix

    def _fill_template(self, template_data: Dict, role: str, skills: List[str], experience_level: str) -> str:
        """Fill question template with dynamic content"""
        template = template_data["template"]
        
        # Replace placeholders
        if "{challenge}" in template:
            template = template.replace("{challenge}", random.choice(template_data["challenges"]))
        if "{situation}" in template:
            template = template.replace("{situation}", random.choice(template_data["situations"]))
        if "{action}" in template:
            template = template.replace("{action}", random.choice(template_data["actions"]))
        if "{technical_challenge}" in template:
            template = template.replace("{technical_challenge}", random.choice(template_data["technical_challenges"]))
        if "{domain}" in template:
            domains = template_data.get("domains", ["software development"])
            template = template.replace("{domain}", random.choice(domains))
        if "{feature}" in template:
            template = template.replace("{feature}", random.choice(template_data["features"]))
        if "{technology}" in template:
            technologies = template_data.get("technologies", skills[:3] if skills else ["modern technologies"])
            template = template.replace("{technology}", random.choice(technologies))
        if "{task}" in template:
            template = template.replace("{task}", random.choice(template_data["tasks"]))
        if "{scenario}" in template:
            template = template.replace("{scenario}", random.choice(template_data["scenarios"]))
        if "{role}" in template:
            template = template.replace("{role}", role)
        
        return template

    def _determine_difficulty(self, experience_years: int) -> str:
        """Determine question difficulty based on experience"""
        if experience_years < 2:
            return "easy"
        elif experience_years < 5:
            return "medium"
        else:
            return "hard"

    def _generate_ideal_answer(self, question: str, q_type: str, role: str) -> str:
        """Generate ideal answer template for the question"""
        if "tell me about yourself" in question.lower():
            return f"Briefly introduce your background, highlight key skills relevant to {role}, mention 1-2 significant achievements, and express enthusiasm for the role."
        elif "challenging project" in question.lower():
            return "Use STAR method: Situation (context), Task (your responsibility), Action (what you did), Result (measurable outcome)."
        elif "technical" in q_type:
            return "Explain the technical approach, mention relevant technologies, discuss trade-offs, and provide a concrete example if possible."
        else:
            return "Provide a specific example, explain your thought process, describe the actions you took, and highlight the positive outcome."

    def _analyze_answer_structure(self, answer: str) -> int:
        """Analyze the structure quality of an answer"""
        sentences = answer.split('.')
        has_intro = len(sentences) > 0 and len(sentences[0].split()) > 5
        has_body = len(sentences) > 2
        has_conclusion = len(sentences) > 1 and any(word in sentences[-1].lower() for word in ["result", "outcome", "learned", "conclusion"])
        
        structure_score = 40  # Base score
        if has_intro:
            structure_score += 20
        if has_body:
            structure_score += 20
        if has_conclusion:
            structure_score += 20
        
        return min(100, structure_score)

    def _analyze_communication_quality(self, answer: str) -> int:
        """Analyze communication quality using heuristics"""
        word_count = len(answer.split())
        sentence_count = len([s for s in answer.split('.') if s.strip()])
        
        # Base score
        comm_score = 60
        
        # Length appropriateness
        if 50 <= word_count <= 200:
            comm_score += 15
        elif word_count < 20:
            comm_score -= 20
        
        # Sentence variety
        if sentence_count > 1:
            avg_sentence_length = word_count / sentence_count
            if 8 <= avg_sentence_length <= 20:
                comm_score += 10
        
        # Professional language indicators
        professional_words = ["experience", "implemented", "developed", "managed", "achieved", "collaborated"]
        professional_count = sum(1 for word in professional_words if word in answer.lower())
        comm_score += min(15, professional_count * 3)
        
        return min(100, comm_score)

    def _calculate_relevance(self, question: str, answer: str) -> int:
        """Calculate how relevant the answer is to the question"""
        question_words = set(question.lower().split())
        answer_words = set(answer.lower().split())
        
        # Remove common words
        common_words = {"the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "how", "what", "when", "where", "why", "you", "your", "me", "my", "i", "is", "are", "was", "were"}
        question_words -= common_words
        answer_words -= common_words
        
        if not question_words:
            return 70  # Default if no meaningful words in question
        
        overlap = question_words.intersection(answer_words)
        relevance_score = (len(overlap) / len(question_words)) * 100
        
        return min(100, max(30, relevance_score))  # Minimum 30, maximum 100

    def _parse_json_from_text(self, text: str) -> Optional[Any]:
        """Parse JSON from text, handling markdown code blocks"""
        if not text:
            return None
        
        cleaned = text.strip()
        
        # Remove markdown code blocks
        if "```json" in cleaned:
            start = cleaned.find("```json") + 7
            end = cleaned.find("```", start)
            if end > start:
                cleaned = cleaned[start:end].strip()
        elif "```" in cleaned:
            start = cleaned.find("```") + 3
            end = cleaned.find("```", start)
            if end > start:
                cleaned = cleaned[start:end].strip()
        
        # Try to find JSON object/array
        for start_char, end_char in [("[", "]"), ("{", "}")]:
            start_idx = cleaned.find(start_char)
            if start_idx != -1:
                end_idx = cleaned.rfind(end_char)
                if end_idx > start_idx:
                    try:
                        json_str = cleaned[start_idx:end_idx + 1]
                        return json.loads(json_str)
                    except json.JSONDecodeError:
                        continue
        
        # Direct JSON parse attempt
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            return None

    def _empty_report(self) -> Dict[str, Any]:
        """Return empty report structure"""
        return {
            "overall_summary": "No evaluation data available.",
            "technical_strengths": [],
            "technical_gaps": [],
            "communication_score": 0,
            "behavioral_score": 0,
            "improved_answers": [],
            "recommendations": []
        }

    def _generate_aptitude_question(self, q_type: str, difficulty: str, question_id: int) -> Dict[str, Any]:
        """Generate a single aptitude question based on type and difficulty"""
        
        if q_type == "quantitative":
            if difficulty == "easy":
                a, b = random.randint(10, 50), random.randint(10, 50)
                return {
                    "id": f"apt_{question_id}",
                    "type": "quantitative",
                    "difficulty": difficulty,
                    "text": f"If a product costs ${a} and is discounted by 20%, what is the final price?",
                    "options": [f"${a*0.8:.2f}", f"${a*0.75:.2f}", f"${a*0.85:.2f}", f"${a*0.9:.2f}"],
                    "correct_answer": f"${a*0.8:.2f}",
                    "explanation": f"20% discount means paying 80% of original price: ${a} × 0.8 = ${a*0.8:.2f}"
                }
            else:
                return {
                    "id": f"apt_{question_id}",
                    "type": "quantitative",
                    "difficulty": difficulty,
                    "text": "A train travels 120 km in 2 hours. If it increases speed by 25%, how long will it take to travel 180 km?",
                    "options": ["2.4 hours", "2.8 hours", "3.0 hours", "3.2 hours"],
                    "correct_answer": "2.4 hours",
                    "explanation": "Original speed: 60 km/h. New speed: 75 km/h. Time = 180/75 = 2.4 hours"
                }
        
        elif q_type == "logical":
            return {
                "id": f"apt_{question_id}",
                "type": "logical",
                "difficulty": difficulty,
                "text": "All roses are flowers. Some flowers are red. Therefore:",
                "options": [
                    "All roses are red",
                    "Some roses are red", 
                    "No roses are red",
                    "Cannot be determined"
                ],
                "correct_answer": "Cannot be determined",
                "explanation": "We know all roses are flowers and some flowers are red, but we cannot determine if any roses are among the red flowers."
            }
        
        elif q_type == "pattern":
            sequence = [2, 4, 8, 16, 32]
            next_val = sequence[-1] * 2
            return {
                "id": f"apt_{question_id}",
                "type": "pattern",
                "difficulty": difficulty,
                "text": f"What comes next in the sequence: {', '.join(map(str, sequence))}?",
                "options": [str(next_val), str(next_val + 4), str(next_val - 8), str(next_val + 16)],
                "correct_answer": str(next_val),
                "explanation": "Each number is double the previous number: 2×2=4, 4×2=8, 8×2=16, 16×2=32, 32×2=64"
            }
        
        else:  # analytical
            return {
                "id": f"apt_{question_id}",
                "type": "analytical",
                "difficulty": difficulty,
                "text": "In a team of 8 developers, if 3 are frontend specialists, 4 are backend specialists, and 1 is full-stack, how many developers work on backend technologies?",
                "options": ["4", "5", "6", "7"],
                "correct_answer": "5",
                "explanation": "Backend specialists (4) + Full-stack developer (1) = 5 developers working on backend technologies"
            }

    def _assess_role_suitability(self, overall_fit: float, required_score: float, experience_score: float) -> str:
        """Assess overall role suitability based on scores"""
        if overall_fit >= 85 and required_score >= 80:
            return "Excellent fit - highly recommended"
        elif overall_fit >= 70 and required_score >= 60:
            return "Good fit - recommended with minor skill development"
        elif overall_fit >= 55:
            return "Moderate fit - requires significant skill development"
        else:
            return "Poor fit - consider alternative roles or extensive training"

    def _generate_job_fit_recommendations(self, overall_fit: float, missing_required: set, missing_preferred: set) -> List[str]:
        """Generate recommendations based on job fit analysis"""
        recommendations = []
        
        if overall_fit < 70:
            recommendations.append("Focus on developing core skills required for this role")
        
        if missing_required:
            recommendations.append(f"Priority: Learn {', '.join(list(missing_required)[:3])} to meet basic requirements")
        
        if missing_preferred:
            recommendations.append(f"Consider learning {', '.join(list(missing_preferred)[:3])} to strengthen your candidacy")
        
        if overall_fit >= 70:
            recommendations.append("You're a strong candidate - highlight your matching skills in your application")
        
        recommendations.append("Prepare specific examples demonstrating your experience with the matched skills")
        
        return recommendations


# Global instance
intelligence_engine = IntelligenceEngine()