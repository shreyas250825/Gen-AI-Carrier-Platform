# AWS Architecture for GenAI Career Intelligence Platform

## Overview

This document outlines the AWS services integration for the GenAI Career Intelligence Platform, designed for scalability, security, and cost-effectiveness in production deployment.

## Architecture Diagram

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────────┐
│   Frontend      │    │   API Gateway    │    │   Lambda Functions  │
│   (React/Vite)  │───▶│   (REST API)     │───▶│   (FastAPI/Python)  │
│   CloudFront    │    │   Rate Limiting  │    │   Auto Scaling      │
└─────────────────┘    └──────────────────┘    └─────────────────────┘
                                                           │
                       ┌─────────────────────────────────────┼─────────────────────────────────────┐
                       │                                     ▼                                     │
                       │                        ┌─────────────────────┐                          │
                       │                        │   AWS Bedrock       │                          │
                       │                        │   (LLM Inference)   │                          │
                       │                        │   - Claude 3 Haiku  │                          │
                       │                        │   - Question Gen     │                          │
                       │                        │   - Answer Eval      │                          │
                       │                        └─────────────────────┘                          │
                       │                                                                         │
┌─────────────────┐    │    ┌──────────────────┐    ┌─────────────────────┐    ┌──────────────┐ │
│   Amazon S3     │◀───┼────│   DynamoDB       │    │   Amazon Rekognition│    │  CloudWatch  │ │
│   - Resumes     │    │    │   - Sessions     │    │   - Facial Analysis │    │  - Logs      │ │
│   - Videos      │    │    │   - User Data    │    │   - Emotion Detect  │    │  - Metrics   │ │
│   - Reports     │    │    │   - Interviews   │    └─────────────────────┘    │  - Alerts    │ │
│   - Transcripts │    │    │   - Reports      │                               └──────────────┘ │
└─────────────────┘    │    └──────────────────┘                                                │
                       │                                                                         │
                       │    ┌──────────────────┐    ┌─────────────────────┐                    │
                       │    │   Amazon Polly   │    │   Amazon Transcribe │                    │
                       │    │   - Text-to-Speech│    │   - Speech-to-Text  │                    │
                       │    │   - AI Interviewer│    │   - Answer Capture  │                    │
                       │    └──────────────────┘    └─────────────────────┘                    │
                       │                                                                         │
                       └─────────────────────────────────────────────────────────────────────────┘
```

## Core AWS Services Integration

### 1. API Gateway → Frontend → Backend
- **Amazon API Gateway**: RESTful API endpoints with built-in rate limiting, authentication, and monitoring
- **AWS Lambda**: Serverless compute for FastAPI application with automatic scaling
- **Amazon CloudFront**: Global CDN for React frontend with edge caching

### 2. Lambda → AI Inference Wrapper
```python
# Example Lambda function structure
import json
import boto3
from app.ai_engines.intelligence_engine import intelligence_engine

def lambda_handler(event, context):
    """
    AWS Lambda wrapper for AI inference calls
    Routes requests to appropriate intelligence level
    """
    try:
        # Extract request data
        body = json.loads(event['body'])
        action = body.get('action')
        
        if action == 'generate_questions':
            result = intelligence_engine.generate_questions(
                profile=body['profile'],
                interview_type=body['interview_type']
            )
        elif action == 'evaluate_answer':
            result = intelligence_engine.evaluate_answer(
                question=body['question'],
                answer=body['answer'],
                expected_keywords=body['keywords'],
                profile=body['profile']
            )
        
        return {
            'statusCode': 200,
            'body': json.dumps(result),
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### 3. S3 → Reports, Transcripts, Resume Storage
```python
# S3 integration for file storage
import boto3

s3_client = boto3.client('s3')
BUCKET_NAME = 'genai-career-platform-storage'

def store_interview_session(session_id: str, session_data: dict):
    """Store complete interview session in S3"""
    key = f"interviews/{session_id}/session_data.json"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=json.dumps(session_data),
        ContentType='application/json'
    )

def store_resume(user_id: str, resume_file: bytes):
    """Store uploaded resume in S3"""
    key = f"resumes/{user_id}/resume.pdf"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=resume_file,
        ContentType='application/pdf'
    )

def store_video_recording(session_id: str, video_data: bytes):
    """Store interview video recording"""
    key = f"videos/{session_id}/recording.webm"
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=video_data,
        ContentType='video/webm'
    )
```

### 4. DynamoDB → Interview Sessions
```python
# DynamoDB schema and operations
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')

# Table schemas
TABLES = {
    'Interviews': {
        'TableName': 'genai-interviews',
        'KeySchema': [
            {'AttributeName': 'session_id', 'KeyType': 'HASH'}
        ],
        'AttributeDefinitions': [
            {'AttributeName': 'session_id', 'AttributeType': 'S'}
        ]
    },
    'Users': {
        'TableName': 'genai-users',
        'KeySchema': [
            {'AttributeName': 'user_id', 'KeyType': 'HASH'}
        ]
    },
    'Reports': {
        'TableName': 'genai-reports',
        'KeySchema': [
            {'AttributeName': 'session_id', 'KeyType': 'HASH'}
        ]
    }
}

def create_interview_session(session_data: dict):
    """Create new interview session in DynamoDB"""
    table = dynamodb.Table('genai-interviews')
    table.put_item(Item=session_data)

def get_interview_session(session_id: str):
    """Retrieve interview session from DynamoDB"""
    table = dynamodb.Table('genai-interviews')
    response = table.get_item(Key={'session_id': session_id})
    return response.get('Item')
```

### 5. Bedrock (Optional) → Cloud LLM Inference
```python
# AWS Bedrock integration for Level 3 intelligence
import boto3
import json

bedrock_client = boto3.client('bedrock-runtime', region_name='us-east-1')

def call_bedrock_claude(prompt: str, max_tokens: int = 1000) -> str:
    """
    Call AWS Bedrock with Claude 3 Haiku for cost-effective inference
    """
    try:
        body = {
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.3,
            "anthropic_version": "bedrock-2023-05-31"
        }
        
        response = bedrock_client.invoke_model(
            modelId='anthropic.claude-3-haiku-20240307-v1:0',
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']
        
    except Exception as e:
        print(f"Bedrock call failed: {e}")
        return None

# Integration with intelligence engine
def _level3_generate_questions_bedrock(profile: dict, interview_type: str, count: int = 7):
    """Level 3 implementation using AWS Bedrock"""
    prompt = f"""Generate {count} {interview_type} interview questions for:
Role: {profile.get('role', 'Software Engineer')}
Skills: {', '.join(profile.get('skills', [])[:5])}
Experience: {profile.get('experience_level', 'Mid-Level')}

Return JSON array with: id, text, followups, type, difficulty, expected_keywords, expected_length"""
    
    response = call_bedrock_claude(prompt, max_tokens=1200)
    if response:
        return parse_json_from_text(response)
    return None
```

### 6. CloudWatch → Logs & Monitoring
```python
# CloudWatch integration for monitoring and logging
import boto3
import json
from datetime import datetime

cloudwatch = boto3.client('cloudwatch')
logs_client = boto3.client('logs')

def log_interview_metrics(session_id: str, metrics: dict):
    """Send custom metrics to CloudWatch"""
    cloudwatch.put_metric_data(
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
                'MetricName': 'AverageScore',
                'Value': metrics.get('average_score', 0),
                'Unit': 'Percent'
            }
        ]
    )

def log_ai_engine_usage(level_used: int, operation: str):
    """Track which AI level was used for operations"""
    cloudwatch.put_metric_data(
        Namespace='GenAI/AIEngine',
        MetricData=[
            {
                'MetricName': f'Level{level_used}Usage',
                'Value': 1,
                'Unit': 'Count',
                'Dimensions': [
                    {'Name': 'Operation', 'Value': operation}
                ]
            }
        ]
    )
```

## Speech and Vision Services

### Amazon Transcribe Integration
```python
# Real-time speech-to-text for interview answers
import boto3

transcribe_client = boto3.client('transcribe')

def start_transcription_job(audio_file_uri: str, job_name: str):
    """Start transcription job for interview audio"""
    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': audio_file_uri},
        MediaFormat='webm',
        LanguageCode='en-US',
        Settings={
            'ShowSpeakerLabels': True,
            'MaxSpeakerLabels': 2
        }
    )
    return response
```

### Amazon Polly Integration
```python
# Text-to-speech for AI interviewer responses
import boto3

polly_client = boto3.client('polly')

def generate_interviewer_speech(text: str, voice_id: str = 'Joanna'):
    """Convert interviewer response to speech"""
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId=voice_id,
        Engine='neural'
    )
    return response['AudioStream'].read()
```

### Amazon Rekognition Integration
```python
# Facial expression and emotion analysis
import boto3

rekognition_client = boto3.client('rekognition')

def analyze_interview_video(video_bytes: bytes):
    """Analyze facial expressions during interview"""
    response = rekognition_client.detect_faces(
        Image={'Bytes': video_bytes},
        Attributes=['ALL']
    )
    
    emotions = []
    for face in response['FaceDetails']:
        emotions.append({
            'confidence': face['Confidence'],
            'emotions': face['Emotions'],
            'age_range': face['AgeRange'],
            'smile': face['Smile']
        })
    
    return emotions
```

## Security and IAM

### IAM Roles and Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream"
      ],
      "Resource": "arn:aws:bedrock:*:*:model/anthropic.claude-3-haiku-*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::genai-career-platform-storage/*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:Query"
      ],
      "Resource": [
        "arn:aws:dynamodb:*:*:table/genai-interviews",
        "arn:aws:dynamodb:*:*:table/genai-users",
        "arn:aws:dynamodb:*:*:table/genai-reports"
      ]
    }
  ]
}
```

## Cost Optimization

### Service Tier Selection
- **AWS Bedrock**: Claude 3 Haiku (most cost-effective)
- **Lambda**: ARM-based Graviton2 processors for better price/performance
- **DynamoDB**: On-demand billing for variable workloads
- **S3**: Intelligent Tiering for automatic cost optimization

### Usage Monitoring
```python
# Cost monitoring and alerts
def monitor_bedrock_usage():
    """Monitor Bedrock token usage and costs"""
    cloudwatch.put_metric_data(
        Namespace='GenAI/Costs',
        MetricData=[
            {
                'MetricName': 'BedrockTokensUsed',
                'Value': token_count,
                'Unit': 'Count'
            }
        ]
    )
```

## Deployment Strategy

### Infrastructure as Code (CloudFormation/CDK)
```yaml
# CloudFormation template excerpt
Resources:
  GenAILambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: genai-career-platform
      Runtime: python3.11
      Handler: lambda_function.lambda_handler
      Role: !GetAtt LambdaExecutionRole.Arn
      Environment:
        Variables:
          DYNAMODB_TABLE: !Ref InterviewsTable
          S3_BUCKET: !Ref StorageBucket
```

### CI/CD Pipeline
1. **GitHub Actions** → Build and test
2. **AWS CodeBuild** → Package Lambda functions
3. **AWS CodeDeploy** → Deploy to staging/production
4. **CloudWatch** → Monitor deployment health

## Scalability Considerations

### Auto Scaling
- **Lambda**: Automatic scaling up to 10,000 concurrent executions
- **DynamoDB**: Auto-scaling based on read/write capacity
- **API Gateway**: Built-in throttling and caching

### Performance Optimization
- **CloudFront**: Edge caching for static assets
- **ElastiCache**: Redis for session caching
- **Connection pooling**: For database connections

## Monitoring and Alerting

### Key Metrics
- Interview completion rate
- AI engine fallback frequency
- Response latency
- Error rates
- Cost per interview session

### Alerts
- High error rates (>5%)
- Bedrock quota approaching
- Unusual cost spikes
- Lambda timeout issues

## Future Enhancements

### Planned AWS Integrations
- **Amazon SageMaker**: Custom model training
- **AWS Comprehend**: Advanced text analysis
- **Amazon Connect**: Voice-based interviews
- **AWS Personalize**: Personalized question recommendations

This architecture provides a robust, scalable foundation for the GenAI Career Intelligence Platform while maintaining cost-effectiveness and reliability through the three-level intelligence system.