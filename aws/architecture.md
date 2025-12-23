# AWS Architecture for GenAI Career Intelligence Platform

## Overview

This document outlines the simplified AWS services integration for the GenAI Career Intelligence Platform, focusing on **S3** and **MongoDB Atlas** for cost-effective, scalable deployment.

## Simplified Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │    │   Load Balancer  │    │   Backend Server    │
│   (React/Vite)  │───▶│   (ALB/CloudFront│───▶│   (FastAPI/Python)  │
│   S3 Static     │    │   Rate Limiting) │    │   EC2/ECS/Lambda    │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                           │
                       ┌─────────────────────────────────────┼─────────────────────────────────────┐
                       │                                     ▼                                     │
                       │                        ┌─────────────────────┐                          │
                       │                        │   AI Engine Router  │                          │
                       │                        │   - Ollama (Local)  │                          │
                       │                        │   - Gemini (Cloud)  │                          │
                       │                        │   - Auto Fallback   │                          │
                       │                        └─────────────────────┘                          │
                       │                                                                         │
┌─────────────────┐    │    ┌──────────────────┐                               ┌──────────────┐ │
│   Amazon S3     │◀───┼────│   MongoDB Atlas  │                               │  CloudWatch  │ │
│   - Resumes     │    │    │   - Sessions     │                               │  - Logs      │ │
│   - Reports     │    │    │   - User Data    │                               │  - Metrics   │ │
│   - Static Files│    │    │   - Interviews   │                               │  - Alerts    │ │
│   - Backups     │    │    │   - Job Fits     │                               └──────────────┘ │
└─────────────────┘    │    │   - Analytics    │                                                │
                       │    └──────────────────┘                                                │
                       └─────────────────────────────────────────────────────────────────────────┘
```

## Core AWS Services Integration

### 1. Amazon S3 - File Storage
Primary storage for all file-based content with intelligent tiering for cost optimization.

```python
# S3 integration for file storage
import boto3
from botocore.exceptions import ClientError

class S3Manager:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        self.bucket_name = 'genai-career-platform-storage'
    
    def upload_resume(self, user_id: str, resume_file: bytes, filename: str):
        """Upload resume to S3 with organized structure"""
        key = f"resumes/{user_id}/{filename}"
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=resume_file,
                ContentType='application/pdf',
                Metadata={
                    'user_id': user_id,
                    'upload_date': datetime.now().isoformat()
                }
            )
            return f"s3://{self.bucket_name}/{key}"
        except ClientError as e:
            print(f"Error uploading resume: {e}")
            return None
    
    def store_interview_report(self, session_id: str, report_data: dict):
        """Store generated interview report"""
        key = f"reports/{session_id}/report.json"
        try:
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=json.dumps(report_data, indent=2),
                ContentType='application/json'
            )
            return f"s3://{self.bucket_name}/{key}"
        except ClientError as e:
            print(f"Error storing report: {e}")
            return None
    
    def get_resume_url(self, user_id: str, filename: str, expiration: int = 3600):
        """Generate presigned URL for resume access"""
        key = f"resumes/{user_id}/{filename}"
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            print(f"Error generating URL: {e}")
            return None
```

### 2. MongoDB Atlas - Database
Managed MongoDB service for all application data with automatic scaling and backup.

```python
# MongoDB Atlas integration
import os
from pymongo import MongoClient
from datetime import datetime

class MongoDBManager:
    def __init__(self):
        self.mongodb_uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(self.mongodb_uri)
        self.db = self.client.genai_career
    
    def store_interview_session(self, session_data: dict):
        """Store complete interview session"""
        collection = self.db.interview_sessions
        session_data['createdAt'] = datetime.now()
        result = collection.insert_one(session_data)
        return str(result.inserted_id)
    
    def store_job_fit_analysis(self, analysis_data: dict):
        """Store job fit analysis results"""
        collection = self.db.job_fit_analyses
        analysis_data['createdAt'] = datetime.now()
        result = collection.insert_one(analysis_data)
        return str(result.inserted_id)
    
    def get_user_profile(self, user_id: str):
        """Retrieve user profile"""
        collection = self.db.user_profiles
        return collection.find_one({"user_id": user_id})
    
    def update_user_statistics(self, user_id: str, stats_update: dict):
        """Update user statistics"""
        collection = self.db.user_profiles
        collection.update_one(
            {"user_id": user_id},
            {"$set": stats_update, "$currentDate": {"updatedAt": True}}
        )
```

### 3. CloudWatch - Monitoring
Essential monitoring and logging for production deployment.

```python
# CloudWatch integration for monitoring
import boto3
from datetime import datetime

class CloudWatchManager:
    def __init__(self):
        self.cloudwatch = boto3.client('cloudwatch')
        self.logs_client = boto3.client('logs')
    
    def log_interview_completion(self, session_id: str, score: float, duration: int):
        """Log interview completion metrics"""
        self.cloudwatch.put_metric_data(
            Namespace='GenAI/Interviews',
            MetricData=[
                {
                    'MetricName': 'InterviewCompleted',
                    'Value': 1,
                    'Unit': 'Count',
                    'Dimensions': [
                        {'Name': 'SessionId', 'Value': session_id}
                    ]
                },
                {
                    'MetricName': 'InterviewScore',
                    'Value': score,
                    'Unit': 'Percent'
                },
                {
                    'MetricName': 'InterviewDuration',
                    'Value': duration,
                    'Unit': 'Seconds'
                }
            ]
        )
    
    def log_ai_engine_usage(self, engine_used: str, operation: str):
        """Track AI engine usage"""
        self.cloudwatch.put_metric_data(
            Namespace='GenAI/AIEngine',
            MetricData=[
                {
                    'MetricName': 'EngineUsage',
                    'Value': 1,
                    'Unit': 'Count',
                    'Dimensions': [
                        {'Name': 'Engine', 'Value': engine_used},
                        {'Name': 'Operation', 'Value': operation}
                    ]
                }
            ]
        )
```

## Deployment Options

### Option 1: EC2 with Auto Scaling
```yaml
# CloudFormation template for EC2 deployment
Resources:
  GenAIAutoScalingGroup:
    Type: AWS::AutoScaling::AutoScalingGroup
    Properties:
      MinSize: 1
      MaxSize: 5
      DesiredCapacity: 2
      LaunchTemplate:
        LaunchTemplateId: !Ref GenAILaunchTemplate
        Version: !GetAtt GenAILaunchTemplate.LatestVersionNumber
      VPCZoneIdentifier:
        - !Ref PrivateSubnet1
        - !Ref PrivateSubnet2
      TargetGroupARNs:
        - !Ref GenAITargetGroup
```

### Option 2: ECS Fargate (Recommended)
```yaml
# ECS Fargate service definition
Resources:
  GenAIService:
    Type: AWS::ECS::Service
    Properties:
      Cluster: !Ref GenAICluster
      TaskDefinition: !Ref GenAITaskDefinition
      DesiredCount: 2
      LaunchType: FARGATE
      NetworkConfiguration:
        AwsvpcConfiguration:
          SecurityGroups:
            - !Ref GenAISecurityGroup
          Subnets:
            - !Ref PrivateSubnet1
            - !Ref PrivateSubnet2
```

### Option 3: Lambda (For API endpoints)
```python
# Lambda function for specific API endpoints
import json
from app.routes.interview_routes import router as interview_router
from app.routes.job_fit_routes import router as job_fit_router

def lambda_handler(event, context):
    """AWS Lambda handler for API endpoints"""
    try:
        # Route based on path
        path = event.get('path', '')
        method = event.get('httpMethod', 'GET')
        
        if path.startswith('/api/interview'):
            return handle_interview_request(event, context)
        elif path.startswith('/api/job-fit'):
            return handle_job_fit_request(event, context)
        
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not found'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

## S3 Bucket Structure

```
genai-career-platform-storage/
├── resumes/
│   ├── user_123/
│   │   ├── resume_v1.pdf
│   │   └── resume_v2.pdf
│   └── user_456/
│       └── resume.pdf
├── reports/
│   ├── session_abc123/
│   │   ├── report.json
│   │   └── detailed_analysis.pdf
│   └── session_def456/
│       └── report.json
├── static/
│   ├── frontend/
│   │   ├── index.html
│   │   ├── assets/
│   │   └── css/
│   └── templates/
│       └── report_template.html
└── backups/
    ├── mongodb/
    │   └── daily_backup_2025-12-23.json
    └── logs/
        └── application_logs_2025-12-23.log
```

## MongoDB Atlas Collections

```javascript
// Database: genai_career
{
  // Collections
  "interview_sessions": {
    "_id": ObjectId,
    "candidateName": String,
    "role": String,
    "interviewType": String,
    "score": Number,
    "questions": Array,
    "createdAt": Date,
    "s3_report_url": String
  },
  
  "job_fit_analyses": {
    "_id": ObjectId,
    "candidateName": String,
    "targetRole": String,
    "overallFitScore": Number,
    "matchedSkills": Array,
    "missingSkills": Array,
    "s3_resume_url": String,
    "createdAt": Date
  },
  
  "user_profiles": {
    "_id": ObjectId,
    "name": String,
    "email": String,
    "currentRole": String,
    "skills": Array,
    "statistics": Object,
    "preferences": Object,
    "createdAt": Date,
    "updatedAt": Date
  }
}
```

## Security Configuration

### S3 Bucket Policy
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowApplicationAccess",
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::ACCOUNT-ID:role/GenAI-Application-Role"
      },
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::genai-career-platform-storage/*"
    }
  ]
}
```

### IAM Role for Application
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::genai-career-platform-storage",
        "arn:aws:s3:::genai-career-platform-storage/*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData",
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "*"
    }
  ]
}
```

## Cost Optimization

### S3 Lifecycle Policies
```json
{
  "Rules": [
    {
      "Id": "ResumeArchiving",
      "Status": "Enabled",
      "Filter": {"Prefix": "resumes/"},
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    },
    {
      "Id": "ReportRetention",
      "Status": "Enabled",
      "Filter": {"Prefix": "reports/"},
      "Expiration": {"Days": 365}
    }
  ]
}
```

### MongoDB Atlas Optimization
- Use M2 cluster for development
- M10 cluster for production (with auto-scaling)
- Enable data compression
- Set up automated backups with 7-day retention

## Monitoring and Alerts

### CloudWatch Dashboards
```python
# Custom dashboard for monitoring
dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["GenAI/Interviews", "InterviewCompleted"],
                    ["GenAI/AIEngine", "EngineUsage", "Engine", "ollama"],
                    ["GenAI/AIEngine", "EngineUsage", "Engine", "gemini"]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "Platform Usage"
            }
        }
    ]
}
```

### Cost Alerts
```yaml
# CloudWatch billing alarm
BillingAlarm:
  Type: AWS::CloudWatch::Alarm
  Properties:
    AlarmName: GenAI-Monthly-Cost-Alert
    AlarmDescription: Alert when monthly costs exceed $50
    MetricName: EstimatedCharges
    Namespace: AWS/Billing
    Statistic: Maximum
    Period: 86400
    EvaluationPeriods: 1
    Threshold: 50
    ComparisonOperator: GreaterThanThreshold
```

## Deployment Checklist

### Pre-deployment
- [ ] S3 bucket created with proper permissions
- [ ] MongoDB Atlas cluster configured
- [ ] IAM roles and policies set up
- [ ] Environment variables configured
- [ ] SSL certificates obtained

### Deployment
- [ ] Application deployed to chosen compute service
- [ ] Load balancer configured
- [ ] CloudWatch monitoring enabled
- [ ] Backup procedures tested
- [ ] Security groups configured

### Post-deployment
- [ ] Health checks passing
- [ ] Monitoring dashboards created
- [ ] Cost alerts configured
- [ ] Performance testing completed
- [ ] Documentation updated

This simplified AWS architecture provides a robust, cost-effective foundation using only S3 and MongoDB Atlas while maintaining scalability and reliability for the GenAI Career Intelligence Platform.