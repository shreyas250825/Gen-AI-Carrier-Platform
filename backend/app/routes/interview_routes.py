# backend/app/routes/interview_routes.py
from typing import Any, Dict, List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import uuid

from app.ai_engines.gemini_engine import GeminiEngine

router = APIRouter()


class StartReq(BaseModel):
  profile: Dict[str, Any]
  role: Optional[str] = None
  interview_type: Optional[str] = "mixed"
  persona: Optional[str] = "male"


class StartRes(BaseModel):
  session_id: str
  question: Dict[str, Any]


class AnswerReq(BaseModel):
  session_id: str
  question_id: str
  transcript: str
  metrics: Dict[str, Any]


class AnswerRes(BaseModel):
  evaluation: Dict[str, Any]
  improved: str
  next_question: Optional[Dict[str, Any]] = None


class MetricsReq(BaseModel):
  session_id: Optional[str] = None
  question_id: Optional[str] = None
  metrics: Dict[str, Any]


class ReportRes(BaseModel):
  session_id: str
  questions: List[Dict[str, Any]]
  evaluations: List[Dict[str, Any]]
  answers: List[Dict[str, Any]]
  summary: str
  interview_type: Optional[str] = None
  created_at: Optional[str] = None
  role: Optional[str] = None


class ReportListItem(BaseModel):
  session_id: str
  role: str
  interview_type: str
  created_at: str
  overall_score: float
  technical_score: float
  communication_score: float
  confidence_score: float
  questions_count: int


class ReportListRes(BaseModel):
  reports: List[ReportListItem]


SESSIONS: Dict[str, Dict[str, Any]] = {}

# Initialize Gemini engine
gemini_engine = GeminiEngine()


@router.post("/interview/start", response_model=StartRes)
def start(req: StartReq) -> StartRes:
  session_id = str(uuid.uuid4())

  # Use role from request or profile
  role = req.role or req.profile.get("role") or req.profile.get("estimated_role") or "Software Engineer"
  interview_type = req.interview_type or "mixed"
  persona = req.persona or "male"
  
  # Update profile with role
  profile = req.profile.copy()
  profile["role"] = role
  profile["interview_type"] = interview_type
  profile["persona"] = persona

  # Generate first question using Gemini engine
  first_question = gemini_engine.generate_first_question(
      profile=profile,
      persona=persona,
      interview_type=interview_type
  )

  SESSIONS[session_id] = {
    "profile": profile,
    "interview_type": interview_type,
    "persona": persona,
    "conversation_history": [],
    "current_question_number": 1,
    "answers": [],
    "evaluations": [],
    "created_at": datetime.utcnow().isoformat(),
    "role": role,
    "started_at": datetime.utcnow().isoformat(),
  }

  return StartRes(session_id=session_id, question=first_question)


@router.post("/interview/answer", response_model=AnswerRes)
def answer(req: AnswerReq) -> AnswerRes:
  session = SESSIONS.get(req.session_id)
  if not session:
    raise HTTPException(status_code=404, detail="Session not found")

  # Get current question text from conversation history or generate it
  question_text = ""
  if session["conversation_history"]:
    # Find the last question in conversation history
    for entry in reversed(session["conversation_history"]):
      if entry["type"] == "question":
        question_text = entry["content"]
        break
  
  if not question_text:
    # This shouldn't happen, but fallback to a generic question
    question_text = "Please tell me about your experience."

  # Evaluate answer using Gemini
  eval_res = gemini_engine.evaluate_answer(
      question_text=question_text,
      answer=req.transcript,
      profile=session.get("profile", {}),
      conversation_history=session.get("conversation_history", [])
  )
  
  # Generate improved answer using Gemini
  improved = gemini_engine.improve_answer(
      question_text=question_text,
      answer=req.transcript,
      profile=session.get("profile", {})
  )

  # Add question and answer to conversation history
  session["conversation_history"].extend([
    {
      "type": "question",
      "content": question_text,
      "question_number": session["current_question_number"]
    },
    {
      "type": "answer", 
      "content": req.transcript,
      "question_number": session["current_question_number"],
      "evaluation": eval_res,
      "improved": improved
    }
  ])

  session["answers"].append({
    "question_id": req.question_id,
    "question": question_text,
    "transcript": req.transcript,
    "metrics": req.metrics,
    "evaluation": eval_res,
    "improved": improved,
  })
  session["evaluations"].append(eval_res)

  # Generate next question if we haven't reached 8 questions yet
  next_q: Optional[Dict[str, Any]] = None
  if session["current_question_number"] < 8:
    session["current_question_number"] += 1
    next_q = gemini_engine.generate_next_question(
        profile=session.get("profile", {}),
        conversation_history=session["conversation_history"],
        question_number=session["current_question_number"]
    )

  return AnswerRes(evaluation=eval_res, improved=improved, next_question=next_q)


@router.post("/metrics")
def store_metrics(req: MetricsReq) -> Dict[str, str]:
  # Optional endpoint; we also store metrics in /answer.
  session = SESSIONS.get(req.session_id) if req.session_id else None
  if session:
    session.setdefault("extra_metrics", []).append(
      {"question_id": req.question_id, "metrics": req.metrics}
    )
  return {"status": "ok"}


@router.get("/interview/report/{session_id}", response_model=ReportRes)
def report(session_id: str) -> ReportRes:
  session = SESSIONS.get(session_id)
  if not session:
    raise HTTPException(status_code=404, detail="Session not found")

  evals: List[Dict[str, Any]] = session.get("evaluations", [])
  
  # Generate final report using Gemini
  try:
    report_data = gemini_engine.generate_final_report(session)
    summary = report_data.get("overall_summary", "")
    if not summary:
      # Fallback to simple summary
      if evals:
        tech = sum(e.get("technical", 0) for e in evals) / len(evals)
        comm = sum(e.get("communication", 0) for e in evals) / len(evals)
        conf = sum(e.get("confidence", 0) for e in evals) / len(evals)
        summary = (
          f"Average technical score: {tech:.1f}. "
          f"Average communication score: {comm:.1f}. "
          f"Average confidence score: {conf:.1f}."
        )
      else:
        summary = "No answers recorded for this session."
  except Exception as e:
    print(f"Error generating final report: {e}")
    # Fallback to simple summary
    if evals:
      tech = sum(e.get("technical", 0) for e in evals) / len(evals)
      comm = sum(e.get("communication", 0) for e in evals) / len(evals)
      conf = sum(e.get("confidence", 0) for e in evals) / len(evals)
      summary = (
        f"Average technical score: {tech:.1f}. "
        f"Average communication score: {comm:.1f}. "
        f"Average confidence score: {conf:.1f}."
      )
    else:
      summary = "No answers recorded for this session."

  # Convert conversation history to questions format for compatibility
  questions = []
  for entry in session.get("conversation_history", []):
    if entry["type"] == "question":
      questions.append({
        "id": f"q{entry['question_number']}",
        "text": entry["content"],
        "type": "conversational",
        "difficulty": "medium"
      })

  return ReportRes(
    session_id=session_id,
    questions=questions,
    evaluations=evals,
    answers=session.get("answers", []),
    summary=summary,
    interview_type=session.get("interview_type"),
    created_at=session.get("created_at"),
    role=session.get("role"),
  )


@router.get("/interview/reports", response_model=ReportListRes)
def list_reports() -> ReportListRes:
  """List all interview sessions with metadata"""
  reports = []
  
  for session_id, session in SESSIONS.items():
    evals = session.get("evaluations", [])
    
    if evals:
      tech = sum(e.get("technical", 0) for e in evals) / len(evals)
      comm = sum(e.get("communication", 0) for e in evals) / len(evals)
      conf = sum(e.get("confidence", 0) for e in evals) / len(evals)
      overall = (tech + comm + conf) / 3
    else:
      tech = comm = conf = overall = 0.0
    
    # Count questions from conversation history
    question_count = len([entry for entry in session.get("conversation_history", []) if entry["type"] == "question"])
    
    reports.append(ReportListItem(
      session_id=session_id,
      role=session.get("role", "Software Engineer"),
      interview_type=session.get("interview_type", "mixed"),
      created_at=session.get("created_at", datetime.utcnow().isoformat()),
      overall_score=overall,
      technical_score=tech,
      communication_score=comm,
      confidence_score=conf,
      questions_count=question_count
    ))
  
  # Sort by created_at descending (most recent first)
  reports.sort(key=lambda x: x.created_at, reverse=True)
  
  return ReportListRes(reports=reports)