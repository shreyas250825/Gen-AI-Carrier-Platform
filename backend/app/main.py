# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.routes import health_check, interview_routes, resume_routes, report_routes, auth_routes
# Import new routes for enhanced features
from app.routes import aptitude_routes, job_fit_routes
from app.middleware.cors import setup_cors
from app.config import get_settings

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
  title="GenAI Career Intelligence Platform API",
  description="AWS-powered career intelligence platform with three-level AI architecture",
  version="2.0.0",
  docs_url="/docs",
  redoc_url="/redoc",
)

# Setup CORS middleware
setup_cors(app)

# Include existing routers
app.include_router(health_check.router, tags=["Health"])
# New simplified interview API lives under /api
app.include_router(interview_routes.router, prefix="/api", tags=["Interview"])
app.include_router(resume_routes.router, prefix="/api/v1/resume", tags=["Resume"])
# Also include resume routes under /api/resume for the new parse endpoint
app.include_router(resume_routes.router, prefix="/api/resume", tags=["Resume"])
app.include_router(report_routes.router, prefix="/api/v1/reports", tags=["Reports"])
app.include_router(auth_routes.router, tags=["Auth"])

# Include NEW FEATURE routers
app.include_router(aptitude_routes.router, tags=["Aptitude Assessment"])
app.include_router(job_fit_routes.router, tags=["Job Fit Analysis"])


@app.get("/")
async def root():
  return {
    "message": "GenAI Career Intelligence Platform API",
    "status": "running",
    "version": "2.0.0",
    "features": [
      "Three-Level Intelligence Architecture",
      "Aptitude & Logical Reasoning Assessment", 
      "AI-Based Job Fit & Role Matching",
      "AWS-Aligned Cloud AI Integration",
      "Offline AI Capability (Ollama)",
      "Deterministic Fallback System"
    ],
    "intelligence_levels": {
      "level_1": "Deterministic Intelligence (Always Available)",
      "level_2": "Local AI Intelligence (Ollama)",
      "level_3": "Cloud AI Intelligence (AWS Bedrock)"
    }
  }


@app.get("/health")
@app.head("/health")
async def health():
  return {"status": "ok"}


@app.get("/api/intelligence-status")
async def intelligence_status():
  """
  Check the status of all three intelligence levels.
  Useful for monitoring and debugging the AI system.
  """
  from app.ai_engines.intelligence_engine import intelligence_engine
  
  return {
    "level_1_deterministic": {
      "status": "available" if intelligence_engine.level_1_enabled else "unavailable",
      "description": "Rule-based fallback system"
    },
    "level_2_local_ai": {
      "status": "available" if intelligence_engine.level_2_enabled else "unavailable", 
      "description": "Ollama local LLM"
    },
    "level_3_cloud_ai": {
      "status": "available" if intelligence_engine.level_3_enabled else "unavailable",
      "description": "AWS Bedrock (pluggable)"
    },
    "current_primary": "level_3" if intelligence_engine.level_3_enabled else 
                     "level_2" if intelligence_engine.level_2_enabled else "level_1"
  }


if __name__ == "__main__":
  import uvicorn

  uvicorn.run(
    "app.main:app",
    host="0.0.0.0",
    port=8000,
    reload=settings.DEBUG,
  )

