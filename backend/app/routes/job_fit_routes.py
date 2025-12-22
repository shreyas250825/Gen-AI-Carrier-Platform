"""
Job Fit & Role Matching Routes

NEW FEATURE: AI-based job fit analysis and role matching.
Analyzes resume against job descriptions to provide fit scores and recommendations.
"""

from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from typing import Dict, Any, List
import logging
import json

from app.database import get_db
from app.ai_engines.gemini_engine import GeminiEngine
from app.services.resume_service import ResumeService
from app.schemas.analysis_schema import JobFitRequest, JobFitResult, RoleMatchingRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/job-fit", tags=["job-fit"])

# Initialize Gemini engine
gemini_engine = GeminiEngine()


@router.post("/analyze", response_model=JobFitResult)
async def analyze_job_fit(
    request: JobFitRequest
    # Removed db dependency for now since we don't actually use it in this endpoint
):
    """
    Analyze job fit between candidate profile and job description.
    
    Features:
    - Overall fit score (0-100)
    - Skill match percentage
    - Experience alignment
    - Missing skills identification
    - Role suitability assessment
    - Personalized recommendations
    """
    try:
        logger.info(f"Analyzing job fit for role: {request.job_description.title}")
        
        # Calculate job fit using intelligence engine
        fit_analysis = gemini_engine.calculate_job_fit(
            resume_data=request.resume_data.dict(),
            job_description=request.job_description.dict()
        )
        
        return JobFitResult(
            overall_fit_score=fit_analysis['overall_fit_score'],
            skill_match_percentage=fit_analysis['skill_match_percentage'],
            experience_match_percentage=fit_analysis['experience_match_percentage'],
            missing_required_skills=fit_analysis['missing_required_skills'],
            missing_preferred_skills=fit_analysis['missing_preferred_skills'],
            matched_skills=fit_analysis['matched_skills'],
            role_suitability=fit_analysis['role_suitability'],
            recommendations=fit_analysis['recommendations'],
            detailed_analysis={
                'skill_breakdown': _analyze_skill_categories(
                    request.resume_data.skills,
                    request.job_description.required_skills,
                    request.job_description.preferred_skills or []
                ),
                'experience_analysis': _analyze_experience_fit(
                    request.resume_data.experience_years,
                    request.job_description.required_experience_years,
                    request.resume_data.projects or []
                ),
                'education_match': _analyze_education_fit(
                    request.resume_data.education or {},
                    request.job_description.education_requirements or {}
                )
            }
        )
        
    except Exception as e:
        logger.error(f"Error analyzing job fit: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze job fit")


@router.post("/upload-resume-analyze")
async def analyze_job_fit_from_resume(
    resume_file: UploadFile = File(...),
    job_description: str = None
):
    """
    Upload resume file and analyze job fit against provided job description.
    
    Supports PDF, DOC, DOCX resume formats.
    """
    try:
        if not job_description:
            raise HTTPException(status_code=400, detail="Job description is required")
        
        # Parse job description JSON
        try:
            job_desc_data = json.loads(job_description)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid job description JSON format")
        
        # Read and parse resume
        resume_content = await resume_file.read()
        resume_service = ResumeService(db)
        
        # Parse resume (this would use your existing resume parsing logic)
        parsed_resume = await resume_service.parse_resume_content(
            resume_content, 
            resume_file.filename
        )
        
        # Analyze job fit
        fit_analysis = gemini_engine.calculate_job_fit(
            resume_data=parsed_resume,
            job_description=job_desc_data
        )
        
        return {
            "resume_analysis": parsed_resume,
            "job_fit_analysis": fit_analysis,
            "filename": resume_file.filename
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing resume job fit: {e}")
        raise HTTPException(status_code=500, detail="Failed to analyze resume job fit")


@router.post("/role-matching", response_model=List[Dict[str, Any]])
async def find_matching_roles(
    request: RoleMatchingRequest
):
    """
    Find best matching roles for a candidate based on their profile.
    
    Returns ranked list of roles with fit scores and explanations.
    """
    try:
        logger.info("Finding matching roles for candidate profile")
        
        # Sample job roles database (in production, this would come from a real database)
        sample_roles = [
            {
                "title": "Frontend Developer",
                "required_skills": ["JavaScript", "React", "HTML", "CSS"],
                "preferred_skills": ["TypeScript", "Vue.js", "SASS"],
                "required_experience_years": 2,
                "company": "TechCorp",
                "location": "Remote"
            },
            {
                "title": "Full Stack Developer", 
                "required_skills": ["JavaScript", "Node.js", "React", "MongoDB"],
                "preferred_skills": ["Python", "AWS", "Docker"],
                "required_experience_years": 3,
                "company": "StartupXYZ",
                "location": "San Francisco"
            },
            {
                "title": "Backend Developer",
                "required_skills": ["Python", "Django", "PostgreSQL", "REST API"],
                "preferred_skills": ["Redis", "Celery", "AWS"],
                "required_experience_years": 3,
                "company": "DataCorp",
                "location": "New York"
            },
            {
                "title": "DevOps Engineer",
                "required_skills": ["AWS", "Docker", "Kubernetes", "CI/CD"],
                "preferred_skills": ["Terraform", "Ansible", "Monitoring"],
                "required_experience_years": 4,
                "company": "CloudTech",
                "location": "Austin"
            }
        ]
        
        # Analyze fit for each role
        role_matches = []
        for role in sample_roles:
            fit_analysis = gemini_engine.calculate_job_fit(
                resume_data=request.candidate_profile,
                job_description=role
            )
            
            role_matches.append({
                "role": role,
                "fit_score": fit_analysis['overall_fit_score'],
                "skill_match": fit_analysis['skill_match_percentage'],
                "experience_match": fit_analysis['experience_match_percentage'],
                "suitability": fit_analysis['role_suitability'],
                "missing_skills": fit_analysis['missing_required_skills'][:3],  # Top 3
                "recommendations": fit_analysis['recommendations'][:2]  # Top 2
            })
        
        # Sort by fit score (descending)
        role_matches.sort(key=lambda x: x['fit_score'], reverse=True)
        
        return role_matches
        
    except Exception as e:
        logger.error(f"Error finding matching roles: {e}")
        raise HTTPException(status_code=500, detail="Failed to find matching roles")


@router.get("/sample-job-descriptions")
async def get_sample_job_descriptions():
    """
    Get sample job descriptions for testing job fit analysis.
    """
    return {
        "sample_jobs": [
            {
                "title": "Senior Software Engineer",
                "company": "TechCorp",
                "required_skills": ["Python", "JavaScript", "React", "Node.js", "PostgreSQL"],
                "preferred_skills": ["AWS", "Docker", "TypeScript", "GraphQL"],
                "required_experience_years": 5,
                "education_requirements": {
                    "degree": "Bachelor's",
                    "field": "Computer Science or related"
                },
                "description": "We're looking for a senior software engineer to join our growing team..."
            },
            {
                "title": "Frontend Developer",
                "company": "StartupXYZ", 
                "required_skills": ["JavaScript", "React", "HTML", "CSS"],
                "preferred_skills": ["TypeScript", "Next.js", "Tailwind CSS"],
                "required_experience_years": 3,
                "education_requirements": {
                    "degree": "Bachelor's or equivalent experience"
                },
                "description": "Join our frontend team to build amazing user experiences..."
            },
            {
                "title": "Data Scientist",
                "company": "DataCorp",
                "required_skills": ["Python", "Machine Learning", "SQL", "Statistics"],
                "preferred_skills": ["TensorFlow", "PyTorch", "AWS", "Spark"],
                "required_experience_years": 4,
                "education_requirements": {
                    "degree": "Master's preferred",
                    "field": "Data Science, Statistics, or related"
                },
                "description": "We're seeking a data scientist to drive insights from our data..."
            }
        ]
    }


# Helper functions for detailed analysis

def _analyze_skill_categories(candidate_skills: List[str], required_skills: List[str], preferred_skills: List[str]) -> Dict[str, Any]:
    """Analyze skills by category (programming languages, frameworks, tools, etc.)"""
    
    categories = {
        "programming_languages": ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
        "frameworks": ["React", "Angular", "Vue.js", "Django", "Flask", "Express", "Spring"],
        "databases": ["PostgreSQL", "MySQL", "MongoDB", "Redis", "Elasticsearch"],
        "cloud_platforms": ["AWS", "Azure", "GCP", "Docker", "Kubernetes"],
        "tools": ["Git", "Jenkins", "Terraform", "Ansible", "Webpack"]
    }
    
    candidate_lower = [skill.lower() for skill in candidate_skills]
    required_lower = [skill.lower() for skill in required_skills]
    preferred_lower = [skill.lower() for skill in preferred_skills]
    
    analysis = {}
    
    for category, skills in categories.items():
        skills_lower = [skill.lower() for skill in skills]
        
        candidate_in_category = [skill for skill in candidate_lower if skill in skills_lower]
        required_in_category = [skill for skill in required_lower if skill in skills_lower]
        preferred_in_category = [skill for skill in preferred_lower if skill in skills_lower]
        
        matches = set(candidate_in_category).intersection(set(required_in_category + preferred_in_category))
        
        analysis[category] = {
            "candidate_skills": candidate_in_category,
            "required_matches": list(set(candidate_in_category).intersection(set(required_in_category))),
            "preferred_matches": list(set(candidate_in_category).intersection(set(preferred_in_category))),
            "total_matches": len(matches)
        }
    
    return analysis


def _analyze_experience_fit(candidate_years: int, required_years: int, projects: List[Dict]) -> Dict[str, Any]:
    """Analyze experience fit including years and project relevance"""
    
    experience_gap = required_years - candidate_years
    experience_ratio = candidate_years / max(required_years, 1)
    
    # Analyze project complexity and relevance
    project_score = 0
    if projects:
        # Simple scoring based on project descriptions
        for project in projects[:5]:  # Top 5 projects
            description = project.get('description', '').lower()
            if any(word in description for word in ['led', 'managed', 'architected', 'designed']):
                project_score += 2
            if any(word in description for word in ['team', 'collaboration', 'cross-functional']):
                project_score += 1
            if any(word in description for word in ['scale', 'performance', 'optimization']):
                project_score += 1
    
    return {
        "years_experience": candidate_years,
        "required_years": required_years,
        "experience_gap": experience_gap,
        "experience_ratio": round(experience_ratio, 2),
        "project_leadership_score": project_score,
        "assessment": "Exceeds requirements" if experience_gap <= -2 else
                    "Meets requirements" if experience_gap <= 0 else
                    "Below requirements" if experience_gap <= 2 else
                    "Significantly below requirements"
    }


def _analyze_education_fit(candidate_education: Dict, required_education: Dict) -> Dict[str, Any]:
    """Analyze education requirements fit"""
    
    if not required_education:
        return {"match": True, "notes": "No specific education requirements"}
    
    candidate_degree = candidate_education.get('degree', '').lower()
    required_degree = required_education.get('degree', '').lower()
    
    degree_hierarchy = {
        'phd': 4, 'doctorate': 4,
        'master': 3, 'masters': 3, 'msc': 3, 'mba': 3,
        'bachelor': 2, 'bachelors': 2, 'bsc': 2, 'ba': 2,
        'associate': 1, 'diploma': 1
    }
    
    candidate_level = 0
    required_level = 0
    
    for degree, level in degree_hierarchy.items():
        if degree in candidate_degree:
            candidate_level = max(candidate_level, level)
        if degree in required_degree:
            required_level = max(required_level, level)
    
    meets_requirement = candidate_level >= required_level
    
    return {
        "candidate_degree": candidate_education.get('degree', 'Not specified'),
        "required_degree": required_education.get('degree', 'Not specified'),
        "meets_requirement": meets_requirement,
        "education_level_match": candidate_level >= required_level,
        "field_match": _check_field_match(
            candidate_education.get('field', ''),
            required_education.get('field', '')
        )
    }


def _check_field_match(candidate_field: str, required_field: str) -> bool:
    """Check if education field matches requirements"""
    if not required_field or not candidate_field:
        return True  # No specific requirement
    
    candidate_lower = candidate_field.lower()
    required_lower = required_field.lower()
    
    # Simple keyword matching - could be enhanced with more sophisticated matching
    related_fields = {
        'computer science': ['software', 'programming', 'computing', 'informatics'],
        'engineering': ['technical', 'technology', 'science'],
        'business': ['management', 'administration', 'commerce'],
        'data science': ['statistics', 'mathematics', 'analytics', 'data']
    }
    
    # Direct match
    if any(word in candidate_lower for word in required_lower.split()):
        return True
    
    # Related field match
    for field, related in related_fields.items():
        if field in required_lower and any(word in candidate_lower for word in related):
            return True
    
    return False