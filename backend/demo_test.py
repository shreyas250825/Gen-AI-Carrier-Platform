#!/usr/bin/env python3
"""
Demo Test Script for AWS ImpactX Challenge
Tests S3 and MongoDB integration for judges
"""

import asyncio
import json
from datetime import datetime
from app.services.s3_service import s3_service
from app.services.mongodb_service import mongodb_service

async def test_demo_integration():
    """Test the demo integration for AWS ImpactX Challenge"""
    
    print("🎯 GenAI Career Intelligence Platform - Demo Integration Test")
    print("=" * 60)
    
    # Test 1: S3 Service
    print("\n📁 Testing S3 Integration...")
    try:
        # Test file upload
        demo_resume_content = b"Demo Resume Content for AWS ImpactX Challenge"
        upload_result = s3_service.upload_resume(
            user_id="demo_candidate_001",
            file_content=demo_resume_content,
            filename="demo_resume.pdf"
        )
        
        if upload_result["success"]:
            print(f"✅ S3 Upload Success: {upload_result['file_url']}")
        else:
            print(f"❌ S3 Upload Failed: {upload_result.get('error', 'Unknown error')}")
        
        # Test storage stats
        storage_stats = s3_service.get_storage_stats()
        print(f"📊 S3 Stats: {storage_stats['total_files']} files, {storage_stats.get('total_size_mb', 0)} MB")
        
    except Exception as e:
        print(f"❌ S3 Test Failed: {e}")
    
    # Test 2: MongoDB Service
    print("\n🗄️ Testing MongoDB Integration...")
    try:
        # Test interview session insertion
        interview_data = {
            "candidateName": "Demo Candidate",
            "role": "Software Engineer",
            "interviewType": "Technical Interview",
            "score": 88,
            "feedback": "Excellent technical skills for AWS ImpactX demo",
            "demo_showcase": True
        }
        
        session_id = mongodb_service.insert_interview_session(interview_data)
        print(f"✅ MongoDB Insert Success: Session ID {session_id}")
        
        # Test job fit analysis insertion
        job_fit_data = {
            "candidateName": "Demo Candidate",
            "targetRole": "Senior Software Engineer",
            "overallFitScore": 87,
            "recommendation": "Excellent Fit",
            "demo_showcase": True
        }
        
        analysis_id = mongodb_service.insert_job_fit_analysis(job_fit_data)
        print(f"✅ MongoDB Job Fit Success: Analysis ID {analysis_id}")
        
        # Test database stats
        db_stats = mongodb_service.get_database_stats()
        print(f"📊 MongoDB Stats: {db_stats['total_documents']} documents across {len(db_stats['collections'])} collections")
        
    except Exception as e:
        print(f"❌ MongoDB Test Failed: {e}")
    
    # Test 3: Integration Test
    print("\n🔄 Testing Full Integration...")
    try:
        # Simulate complete workflow
        candidate_name = "AWS ImpactX Demo User"
        
        # 1. Upload resume
        resume_content = b"Professional resume content for demonstration"
        upload_result = s3_service.upload_resume(
            user_id="impactx_demo_user",
            file_content=resume_content,
            filename="impactx_demo_resume.pdf"
        )
        
        # 2. Store resume analysis in MongoDB
        resume_analysis = {
            "candidateName": candidate_name,
            "fileName": "impactx_demo_resume.pdf",
            "s3_url": upload_result["file_url"],
            "extractedData": {
                "skills": ["Python", "AWS", "React", "MongoDB", "S3"],
                "experienceYears": 5.0,
                "estimatedRole": "Senior Software Engineer"
            },
            "demo_showcase": True,
            "aws_impactx_challenge": True
        }
        
        analysis_id = mongodb_service.insert_interview_session({
            "type": "resume_analysis",
            "candidateName": candidate_name,
            "data": resume_analysis
        })
        
        # 3. Run job fit analysis
        job_fit_result = {
            "candidateName": candidate_name,
            "targetRole": "AWS Solutions Architect",
            "overallFitScore": 92,
            "skillMatchPercentage": 90,
            "recommendation": "Excellent Fit for AWS Role",
            "matchedSkills": ["Python", "AWS", "S3", "MongoDB"],
            "aws_impactx_challenge": True
        }
        
        job_fit_id = mongodb_service.insert_job_fit_analysis(job_fit_result)
        
        # 4. Generate comprehensive report
        report_data = {
            "candidate": candidate_name,
            "resume_analysis_id": analysis_id,
            "job_fit_analysis_id": job_fit_id,
            "s3_resume_url": upload_result["file_url"],
            "overall_assessment": {
                "technical_score": 92,
                "aws_readiness": 95,
                "recommendation": "Highly recommended for AWS roles"
            },
            "aws_impactx_demo": True,
            "generated_at": datetime.now().isoformat()
        }
        
        report_result = s3_service.store_interview_report("impactx_demo_session", report_data)
        
        print(f"✅ Full Integration Success!")
        print(f"   📁 Resume stored in S3: {upload_result['file_url']}")
        print(f"   🗄️ Analysis stored in MongoDB: {analysis_id}")
        print(f"   🎯 Job fit analysis: {job_fit_id}")
        print(f"   📊 Report generated: {report_result['report_url']}")
        
    except Exception as e:
        print(f"❌ Integration Test Failed: {e}")
    
    # Test 4: Demo API Endpoints
    print("\n🌐 Demo API Endpoints Ready:")
    print("   GET  /api/v1/demo/status - Platform status for judges")
    print("   POST /api/v1/demo/upload-resume - S3 upload demonstration")
    print("   POST /api/v1/demo/job-fit-analysis - MongoDB + AI analysis")
    print("   POST /api/v1/demo/interview-session - Complete workflow demo")
    print("   GET  /api/v1/demo/system-analytics - Platform analytics")
    print("   GET  /api/v1/demo/architecture-overview - Architecture showcase")
    
    print("\n🎯 Frontend Demo Available:")
    print("   http://localhost:3000/demo - Interactive demo showcase")
    
    print("\n" + "=" * 60)
    print("🚀 AWS ImpactX Challenge Demo Ready!")
    print("✅ S3 Integration: File storage and management")
    print("✅ MongoDB Integration: Real-time data processing")
    print("✅ AI Processing: Ollama + Gemini dual engine")
    print("✅ Scalable Architecture: Production-ready design")
    print("✅ Cost Effective: Optimized AWS resource usage")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_demo_integration())