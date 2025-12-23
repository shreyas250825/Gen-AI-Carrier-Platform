# AWS Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: ECS Fargate (Recommended)
**Best for**: Production workloads with auto-scaling needs

```bash
# 1. Build and push Docker image
docker build -t genai-career-platform .
docker tag genai-career-platform:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/genai-career-platform:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/genai-career-platform:latest

# 2. Deploy using ECS CLI
ecs-cli compose --project-name genai-career service up --cluster genai-cluster
```

### Option 2: EC2 with Auto Scaling
**Best for**: Full control over infrastructure

```bash
# 1. Launch EC2 instances
aws ec2 run-instances \
  --image-id ami-0abcdef1234567890 \
  --count 2 \
  --instance-type t3.medium \
  --key-name genai-keypair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678

# 2. Deploy application
ssh -i genai-keypair.pem ec2-user@instance-ip
git clone https://github.com/your-repo/genai-career-platform.git
cd genai-career-platform
./deploy.sh
```

### Option 3: Lambda Functions
**Best for**: Serverless, event-driven workloads

```bash
# 1. Package Lambda function
zip -r genai-lambda.zip app/ requirements.txt

# 2. Deploy Lambda
aws lambda create-function \
  --function-name genai-career-api \
  --runtime python3.11 \
  --role arn:aws:iam::123456789012:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://genai-lambda.zip
```

## 📋 Environment Setup

### 1. S3 Bucket Configuration
```bash
# Create S3 bucket
aws s3 mb s3://genai-career-platform-storage --region us-east-1

# Set bucket policy
aws s3api put-bucket-policy \
  --bucket genai-career-platform-storage \
  --policy file://s3-bucket-policy.json

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket genai-career-platform-storage \
  --versioning-configuration Status=Enabled
```

### 2. MongoDB Atlas Setup
```bash
# Set environment variables
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/genai_career"
export AWS_S3_BUCKET="genai-career-platform-storage"
export AWS_REGION="us-east-1"

# Test connection
python -c "from mongodb.config import MongoDBConfig; print('✅ MongoDB connected!' if MongoDBConfig().get_database() else '❌ Connection failed')"
```

### 3. CloudWatch Configuration
```bash
# Create log group
aws logs create-log-group --log-group-name /aws/genai-career-platform

# Create custom metrics
aws cloudwatch put-metric-data \
  --namespace "GenAI/Health" \
  --metric-data MetricName=DeploymentStatus,Value=1,Unit=Count
```

## 🔧 Infrastructure as Code

### CloudFormation Template
```yaml
# infrastructure.yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'GenAI Career Platform Infrastructure'

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues: [development, staging, production]

Resources:
  # S3 Bucket
  StorageBucket:
    Type: AWS::S3::Bucket
    Properties:
      BucketName: !Sub 'genai-career-${Environment}-storage'
      VersioningConfiguration:
        Status: Enabled
      LifecycleConfiguration:
        Rules:
          - Id: ArchiveOldFiles
            Status: Enabled
            Transitions:
              - TransitionInDays: 30
                StorageClass: STANDARD_IA
              - TransitionInDays: 90
                StorageClass: GLACIER

  # ECS Cluster
  ECSCluster:
    Type: AWS::ECS::Cluster
    Properties:
      ClusterName: !Sub 'genai-career-${Environment}'
      CapacityProviders:
        - FARGATE
        - FARGATE_SPOT

  # Application Load Balancer
  LoadBalancer:
    Type: AWS::ElasticLoadBalancingV2::LoadBalancer
    Properties:
      Name: !Sub 'genai-career-${Environment}-alb'
      Scheme: internet-facing
      Type: application
      Subnets:
        - !Ref PublicSubnet1
        - !Ref PublicSubnet2

Outputs:
  BucketName:
    Description: 'S3 Bucket Name'
    Value: !Ref StorageBucket
    Export:
      Name: !Sub '${AWS::StackName}-BucketName'
```

### Deploy Infrastructure
```bash
# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file infrastructure.yaml \
  --stack-name genai-career-infrastructure \
  --parameter-overrides Environment=production \
  --capabilities CAPABILITY_IAM
```

## 🐳 Docker Configuration

### Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose for Local Development
```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MONGODB_URI=${MONGODB_URI}
      - AWS_S3_BUCKET=${AWS_S3_BUCKET}
      - AWS_REGION=${AWS_REGION}
    volumes:
      - ./app:/app/app
    depends_on:
      - localstack

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    environment:
      - REACT_APP_API_URL=http://localhost:8000
    volumes:
      - ./frontend/src:/app/src

  localstack:
    image: localstack/localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,cloudwatch
      - DEBUG=1
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
```

## 🔐 Security Configuration

### IAM Policies
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "S3Access",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::genai-career-*-storage",
        "arn:aws:s3:::genai-career-*-storage/*"
      ]
    },
    {
      "Sid": "CloudWatchAccess",
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

### Security Groups
```bash
# Create security group for application
aws ec2 create-security-group \
  --group-name genai-career-app-sg \
  --description "Security group for GenAI Career Platform"

# Allow HTTP/HTTPS traffic
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

## 📊 Monitoring Setup

### CloudWatch Dashboards
```python
# create_dashboard.py
import boto3
import json

cloudwatch = boto3.client('cloudwatch')

dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "x": 0, "y": 0,
            "width": 12, "height": 6,
            "properties": {
                "metrics": [
                    ["GenAI/Interviews", "InterviewCompleted"],
                    ["GenAI/AIEngine", "EngineUsage", "Engine", "ollama"],
                    ["GenAI/AIEngine", "EngineUsage", "Engine", "gemini"]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "Platform Usage Metrics"
            }
        },
        {
            "type": "log",
            "x": 0, "y": 6,
            "width": 24, "height": 6,
            "properties": {
                "query": "SOURCE '/aws/genai-career-platform'\n| fields @timestamp, @message\n| filter @message like /ERROR/\n| sort @timestamp desc\n| limit 100",
                "region": "us-east-1",
                "title": "Recent Errors"
            }
        }
    ]
}

cloudwatch.put_dashboard(
    DashboardName='GenAI-Career-Platform',
    DashboardBody=json.dumps(dashboard_body)
)
```

### Alerts Configuration
```bash
# Create billing alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "GenAI-High-Costs" \
  --alarm-description "Alert when monthly costs exceed $100" \
  --metric-name EstimatedCharges \
  --namespace AWS/Billing \
  --statistic Maximum \
  --period 86400 \
  --evaluation-periods 1 \
  --threshold 100 \
  --comparison-operator GreaterThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:123456789012:billing-alerts

# Create error rate alarm
aws cloudwatch put-metric-alarm \
  --alarm-name "GenAI-High-Error-Rate" \
  --alarm-description "Alert when error rate exceeds 5%" \
  --metric-name ErrorRate \
  --namespace GenAI/Application \
  --statistic Average \
  --period 300 \
  --evaluation-periods 2 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold
```

## 🚀 CI/CD Pipeline

### GitHub Actions Workflow
```yaml
# .github/workflows/deploy.yml
name: Deploy to AWS

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v2
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Build and push Docker image
      run: |
        docker build -t genai-career-platform .
        docker tag genai-career-platform:latest $ECR_REGISTRY/genai-career-platform:latest
        docker push $ECR_REGISTRY/genai-career-platform:latest
    
    - name: Deploy to ECS
      run: |
        aws ecs update-service \
          --cluster genai-career-production \
          --service genai-career-service \
          --force-new-deployment
```

## 📋 Deployment Checklist

### Pre-deployment
- [ ] AWS account configured with proper permissions
- [ ] S3 bucket created and configured
- [ ] MongoDB Atlas cluster set up
- [ ] Domain name and SSL certificate ready
- [ ] Environment variables configured
- [ ] Docker images built and tested

### Deployment
- [ ] Infrastructure deployed via CloudFormation
- [ ] Application deployed to chosen compute service
- [ ] Load balancer configured with health checks
- [ ] DNS records updated
- [ ] SSL certificate attached
- [ ] Security groups configured

### Post-deployment
- [ ] Health checks passing
- [ ] Monitoring dashboards created
- [ ] Alerts configured
- [ ] Backup procedures tested
- [ ] Performance testing completed
- [ ] Documentation updated

### Rollback Plan
- [ ] Previous version tagged and available
- [ ] Rollback procedure documented
- [ ] Database migration rollback tested
- [ ] Monitoring for rollback triggers

## 🔧 Troubleshooting

### Common Issues

**Connection Timeouts**
```bash
# Check security groups
aws ec2 describe-security-groups --group-ids sg-12345678

# Test connectivity
telnet your-domain.com 80
```

**High Memory Usage**
```bash
# Check ECS task definition
aws ecs describe-task-definition --task-definition genai-career-task

# Update memory limits
aws ecs register-task-definition --cli-input-json file://updated-task-def.json
```

**S3 Access Issues**
```bash
# Test S3 access
aws s3 ls s3://genai-career-platform-storage/

# Check IAM permissions
aws iam simulate-principal-policy \
  --policy-source-arn arn:aws:iam::123456789012:role/genai-app-role \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::genai-career-platform-storage/*
```

## 💰 Cost Optimization

### Reserved Instances
```bash
# Purchase reserved instances for predictable workloads
aws ec2 purchase-reserved-instances-offering \
  --reserved-instances-offering-id 12345678-1234-1234-1234-123456789012 \
  --instance-count 2
```

### Spot Instances for Development
```bash
# Use spot instances for development environments
aws ec2 request-spot-instances \
  --spot-price "0.05" \
  --instance-count 1 \
  --type "one-time" \
  --launch-specification file://spot-launch-spec.json
```

### S3 Lifecycle Policies
```json
{
  "Rules": [
    {
      "Id": "CostOptimization",
      "Status": "Enabled",
      "Filter": {"Prefix": ""},
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
    }
  ]
}
```

This deployment guide provides comprehensive instructions for deploying the GenAI Career Intelligence Platform on AWS with proper security, monitoring, and cost optimization.