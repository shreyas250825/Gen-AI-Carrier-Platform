# API Documentation 📚

## 📋 Overview

Complete API documentation for the GenAI Career Intelligence Platform, including all endpoints, request/response formats, and integration examples.

## 🔗 Base URL

```
Development: http://localhost:8000
Production: https://your-domain.com
```

## 🔐 Authentication

Currently, the API uses simple session-based authentication. Future versions will include JWT tokens and API keys.

```bash
# No authentication required for current version
curl -X GET "http://localhost:8000/api/health"
```

## 📊 Core API Endpoints

### 1. Health & Status

#### System Health Check
```http
GET /api/health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-23T10:30:00Z",
  "version": "2.1.0",
  "services": {
    "database": "connected",
    "ai_engine": "available",
    "storage": "accessible"
  }
}
```

#### Intelligence Status
```http
GET /api/intelligence-status
```

**Response:**
```json
{
  "status": "operational",
  "ai_engines": {
    "ollama": {
      "available": true,
      "model": "llama3.1:8b",
      "response_time": 1.2
    },
    "gemini": {
      "available": true,
      "model": "gemini-pro",
      "response_time": 0.8
    }
  },
  "current_engine": "ollama",
  "fallback_enabled": true
}
```

### 2. Resume Processing

#### Upload Resume
```http
POST /api/v1/resume/upload
Content-Type: multipart/form-data
```

**Request:**
```bash
curl -X POST "http://localhost:8000/api/v1/resume/upload" \
  -F "file=@resume.pdf" \
  -F "candidate_name=John Doe"
```

**Response:**
```json
{
  "success": true,
  "file_id": "resume_123456",
  "candidate_name": "John Doe",
  "file_size": 245760,
  "upload_time": "2025-12-23T10:30:00Z",
  "s3_url": "s3://bucket/resumes/123456/resume.pdf"
}
```

#### Parse Resume
```http
POST /api/v1/resume/parse
Content-Type: application/json
```

**Request:**
```json
{
  "file_id": "resume_123456",
  "candidate_name": "John Doe"
}
```

**Response:**
```json
{
  "success": true,
  "extracted_data": {
    "skills": ["Python", "JavaScript", "React", "AWS"],
    "experience_years": 4.5,
    "experience_level": "Mid-Level",
    "education": ["Bachelor of Technology in Computer Science"],
    "companies": ["TechCorp", "StartupXYZ"],
    "projects": [
      "E-commerce platform with React and Node.js",
      "Machine learning model for price prediction"
    ]
  },
  "validation_results": {
    "is_valid": true,
    "completeness_score": 95,
    "missing_fields": []
  }
}
```

### 3. Interview Management

#### Start Interview Session
```http
POST /api/v1/interview/start
Content-Type: application/json
```

**Request:**
```json
{
  "candidate_name": "John Doe",
  "role": "Software Engineer",
  "interview_type": "Technical",
  "persona": "Senior Engineer",
  "resume_data": {
    "skills": ["Python", "JavaScript"],
    "experience_years": 4.5
  }
}
```

**Response:**
```json
{
  "success": true,
  "session_id": "interview_789012",
  "first_question": {
    "id": "q1",
    "text": "Can you explain the difference between REST and GraphQL APIs?",
    "type": "technical",
    "difficulty": "medium",
    "expected_keywords": ["endpoints", "queries", "flexibility"],
    "expected_length": "2-3 minutes"
  },
  "session_info": {
    "total_questions": 7,
    "estimated_duration": 45,
    "current_question": 1
  }
}
```

#### Submit Answer
```http
POST /api/v1/interview/{session_id}/answer
Content-Type: application/json
```

**Request:**
```json
{
  "question_id": "q1",
  "answer": "REST uses multiple endpoints while GraphQL uses a single endpoint with flexible queries...",
  "duration": 120
}
```

**Response:**
```json
{
  "success": true,
  "evaluation": {
    "score": 8.5,
    "feedback": "Excellent understanding of API architectures",
    "strengths": ["Clear explanation", "Good examples"],
    "improvements": ["Could mention caching differences"],
    "expected_answer": "A strong answer should cover: multiple endpoints vs single endpoint, query flexibility, over-fetching prevention, and type safety."
  },
  "next_question": {
    "id": "q2",
    "text": "How do you handle state management in React applications?",
    "type": "technical",
    "difficulty": "medium"
  }
}
```

#### Get Interview Status
```http
GET /api/v1/interview/{session_id}/status
```

**Response:**
```json
{
  "session_id": "interview_789012",
  "status": "in_progress",
  "progress": {
    "current_question": 3,
    "total_questions": 7,
    "completion_percentage": 43
  },
  "timing": {
    "start_time": "2025-12-23T10:00:00Z",
    "elapsed_time": 1200,
    "estimated_remaining": 1500
  },
  "scores": {
    "current_average": 8.2,
    "question_scores": [8.5, 7.8, 8.3]
  }
}
```

#### Complete Interview
```http
POST /api/v1/interview/{session_id}/complete
```

**Response:**
```json
{
  "success": true,
  "session_id": "interview_789012",
  "final_report": {
    "overall_score": 85,
    "duration": 42,
    "questions_answered": 7,
    "detailed_scores": {
      "technical": 88,
      "communication": 82,
      "problem_solving": 85,
      "confidence": 87
    },
    "recommendations": [
      "Practice system design concepts",
      "Work on explaining complex topics simply"
    ],
    "report_url": "s3://bucket/reports/789012/report.json"
  }
}
```

### 4. Job Fit Analysis

#### Get Available Roles
```http
GET /api/v1/job-fit/available-roles
```

**Response:**
```json
{
  "success": true,
  "roles": [
    {
      "id": "software-engineer",
      "title": "Software Engineer",
      "category": "Engineering",
      "required_skills": ["Programming", "Problem Solving"],
      "preferred_skills": ["JavaScript", "Python", "React"]
    },
    {
      "id": "data-scientist",
      "title": "Data Scientist",
      "category": "Data & Analytics",
      "required_skills": ["Python", "Statistics", "Machine Learning"],
      "preferred_skills": ["TensorFlow", "SQL", "Visualization"]
    }
  ],
  "total_roles": 50
}
```

#### Analyze Job Fit
```http
POST /api/v1/job-fit/analyze-with-role
Content-Type: application/json
```

**Request:**
```json
{
  "candidate_name": "John Doe",
  "target_role": "Senior Software Engineer",
  "resume_data": {
    "skills": ["Python", "JavaScript", "React", "AWS"],
    "experience_years": 4.5,
    "projects": ["E-commerce platform", "ML model"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "overall_fit_score": 85,
    "skill_match_percentage": 80,
    "experience_match_percentage": 90,
    "recommendation": "Excellent Fit",
    "confidence_score": 92,
    "matched_skills": ["Python", "JavaScript", "React", "AWS"],
    "missing_skills": ["System Design", "Microservices", "Kubernetes"],
    "next_steps": [
      "Study system design patterns",
      "Gain experience with microservices architecture",
      "Learn container orchestration"
    ],
    "salary_estimate": {
      "min": 95000,
      "max": 125000,
      "currency": "USD"
    }
  }
}
```

### 5. Aptitude Assessment

#### Start Aptitude Test
```http
POST /api/v1/aptitude/start
Content-Type: application/json
```

**Request:**
```json
{
  "candidate_name": "John Doe",
  "assessment_type": "Logical Reasoning",
  "difficulty": "Medium"
}
```

**Response:**
```json
{
  "success": true,
  "assessment_id": "apt_345678",
  "questions": [
    {
      "id": "q1",
      "type": "pattern_recognition",
      "question": "What comes next in the sequence: 2, 4, 8, 16, ?",
      "options": ["24", "32", "30", "20"],
      "time_limit": 60
    }
  ],
  "total_questions": 20,
  "time_limit": 1800
}
```

#### Submit Aptitude Answers
```http
POST /api/v1/aptitude/{assessment_id}/submit
Content-Type: application/json
```

**Request:**
```json
{
  "answers": [
    {"question_id": "q1", "answer": "32", "time_taken": 45},
    {"question_id": "q2", "answer": "B", "time_taken": 52}
  ]
}
```

**Response:**
```json
{
  "success": true,
  "results": {
    "overall_score": 85,
    "correct_answers": 17,
    "total_questions": 20,
    "time_spent": 1425,
    "categories": {
      "pattern_recognition": {"score": 90, "correct": 4, "total": 5},
      "logical_sequence": {"score": 80, "correct": 4, "total": 5},
      "analytical_reasoning": {"score": 85, "correct": 4, "total": 5},
      "quantitative_aptitude": {"score": 85, "correct": 5, "total": 5}
    },
    "strengths": ["Pattern Recognition", "Quantitative Analysis"],
    "improvements": ["Logical Sequence", "Time Management"]
  }
}
```

### 6. AI Engine Management

#### Get Engine Status
```http
GET /api/v1/ai-engine/status
```

**Response:**
```json
{
  "current_engine": "ollama",
  "engines": {
    "ollama": {
      "available": true,
      "model": "llama3.1:8b",
      "requests": 1156,
      "avg_response_time": 1.2,
      "last_used": "2025-12-23T10:25:00Z"
    },
    "gemini": {
      "available": true,
      "model": "gemini-pro",
      "requests": 91,
      "avg_response_time": 0.8,
      "last_used": "2025-12-23T09:15:00Z"
    }
  },
  "statistics": {
    "total_requests": 1247,
    "fallback_count": 12,
    "success_rate": 99.2
  }
}
```

#### Force Engine Selection
```http
POST /api/v1/ai-engine/select
Content-Type: application/json
```

**Request:**
```json
{
  "engine": "gemini",
  "reason": "Testing cloud processing"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Engine switched to gemini",
  "previous_engine": "ollama",
  "current_engine": "gemini"
}
```

## 📝 Request/Response Formats

### Standard Success Response
```json
{
  "success": true,
  "data": { /* response data */ },
  "timestamp": "2025-12-23T10:30:00Z",
  "request_id": "req_123456"
}
```

### Standard Error Response
```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "candidate_name",
      "issue": "Required field missing"
    }
  },
  "timestamp": "2025-12-23T10:30:00Z",
  "request_id": "req_123456"
}
```

### Common Error Codes

| Code | Description | HTTP Status |
|------|-------------|-------------|
| `VALIDATION_ERROR` | Invalid input parameters | 400 |
| `NOT_FOUND` | Resource not found | 404 |
| `AI_ENGINE_ERROR` | AI processing failed | 500 |
| `STORAGE_ERROR` | File storage issue | 500 |
| `RATE_LIMIT_EXCEEDED` | Too many requests | 429 |

## 🔧 Integration Examples

### Python Client
```python
import requests
import json

class GenAIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
    
    def start_interview(self, candidate_name, role, interview_type):
        """Start a new interview session"""
        url = f"{self.base_url}/api/v1/interview/start"
        data = {
            "candidate_name": candidate_name,
            "role": role,
            "interview_type": interview_type
        }
        response = self.session.post(url, json=data)
        return response.json()
    
    def submit_answer(self, session_id, question_id, answer):
        """Submit an answer to interview question"""
        url = f"{self.base_url}/api/v1/interview/{session_id}/answer"
        data = {
            "question_id": question_id,
            "answer": answer
        }
        response = self.session.post(url, json=data)
        return response.json()

# Usage example
client = GenAIClient()
interview = client.start_interview("John Doe", "Software Engineer", "Technical")
session_id = interview["session_id"]
first_question = interview["first_question"]

# Submit answer
result = client.submit_answer(
    session_id, 
    first_question["id"], 
    "REST uses multiple endpoints..."
)
```

### JavaScript Client
```javascript
class GenAIClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }
    
    async startInterview(candidateName, role, interviewType) {
        const response = await fetch(`${this.baseUrl}/api/v1/interview/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                candidate_name: candidateName,
                role: role,
                interview_type: interviewType
            })
        });
        return await response.json();
    }
    
    async submitAnswer(sessionId, questionId, answer) {
        const response = await fetch(`${this.baseUrl}/api/v1/interview/${sessionId}/answer`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question_id: questionId,
                answer: answer
            })
        });
        return await response.json();
    }
}

// Usage example
const client = new GenAIClient();

async function runInterview() {
    const interview = await client.startInterview("John Doe", "Software Engineer", "Technical");
    const sessionId = interview.session_id;
    const firstQuestion = interview.first_question;
    
    // Submit answer
    const result = await client.submitAnswer(
        sessionId,
        firstQuestion.id,
        "REST uses multiple endpoints..."
    );
    console.log(result);
}
```

### cURL Examples
```bash
# Start interview
curl -X POST "http://localhost:8000/api/v1/interview/start" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "role": "Software Engineer",
    "interview_type": "Technical"
  }'

# Submit answer
curl -X POST "http://localhost:8000/api/v1/interview/session_123/answer" \
  -H "Content-Type: application/json" \
  -d '{
    "question_id": "q1",
    "answer": "REST uses multiple endpoints while GraphQL uses a single endpoint..."
  }'

# Get job fit analysis
curl -X POST "http://localhost:8000/api/v1/job-fit/analyze-with-role" \
  -H "Content-Type: application/json" \
  -d '{
    "candidate_name": "John Doe",
    "target_role": "Senior Software Engineer",
    "resume_data": {
      "skills": ["Python", "JavaScript", "React"],
      "experience_years": 4.5
    }
  }'
```

## 📊 Rate Limits

| Endpoint Category | Limit | Window |
|------------------|-------|--------|
| Interview APIs | 100 requests | 1 hour |
| Resume Processing | 50 uploads | 1 hour |
| Job Fit Analysis | 200 requests | 1 hour |
| AI Engine Management | 1000 requests | 1 hour |

## 🔐 Security Headers

All API responses include security headers:
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

## 📚 Additional Resources

- **OpenAPI Spec**: Available at `/docs` (Swagger UI)
- **Postman Collection**: `postman_collection.json` in project root
- **SDK Libraries**: Python and JavaScript clients available
- **Webhooks**: Coming in v2.2.0 for real-time notifications

---

**🎯 Complete API documentation for seamless integration!**