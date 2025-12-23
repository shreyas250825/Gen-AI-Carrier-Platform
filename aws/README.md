# AWS Integration 🚀

## 📋 Overview

This directory contains AWS-specific configuration and deployment files for the GenAI Career Intelligence Platform, focusing on **S3** and **MongoDB Atlas** integration.

## 📁 Files

- **`architecture.md`** - Detailed AWS architecture documentation
- **`deployment.md`** - Step-by-step deployment guide
- **`README.md`** - This overview file

## 🏗️ Architecture Summary

### Core Services
- **Amazon S3** - File storage (resumes, reports, static files)
- **MongoDB Atlas** - Database (interviews, users, analytics)
- **CloudWatch** - Monitoring and logging

### Deployment Options
1. **ECS Fargate** (Recommended) - Serverless containers
2. **EC2 Auto Scaling** - Traditional instances
3. **Lambda Functions** - Serverless API endpoints

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS credentials
aws configure
```

### 2. Environment Setup
```bash
# Set required environment variables
export AWS_REGION="us-east-1"
export AWS_S3_BUCKET="genai-career-platform-storage"
export MONGODB_URI="mongodb+srv://username:password@cluster.mongodb.net/genai_career"
```

### 3. Deploy Infrastructure
```bash
# Create S3 bucket
aws s3 mb s3://genai-career-platform-storage

# Deploy using CloudFormation (optional)
aws cloudformation deploy \
  --template-file infrastructure.yaml \
  --stack-name genai-career-infrastructure \
  --capabilities CAPABILITY_IAM
```

## 📊 Cost Estimation

### Monthly Costs (Estimated)
- **S3 Storage**: $5-15 (depending on usage)
- **MongoDB Atlas M10**: $57/month
- **ECS Fargate**: $20-50 (2 tasks, t3.medium equivalent)
- **CloudWatch**: $5-10
- **Data Transfer**: $5-15

**Total Estimated**: $92-147/month for production workload

### Development Environment
- **S3**: $1-3/month
- **MongoDB Atlas M2**: $9/month
- **ECS Fargate**: $10-20/month
- **CloudWatch**: $2-5/month

**Total Development**: $22-37/month

## 🔐 Security Features

### S3 Security
- Bucket policies with least privilege access
- Server-side encryption (AES-256)
- Versioning enabled for data protection
- Lifecycle policies for cost optimization

### Network Security
- VPC with private subnets
- Security groups with minimal required ports
- Application Load Balancer with SSL termination
- WAF protection (optional)

### Access Control
- IAM roles with minimal required permissions
- No hardcoded credentials
- Environment-based configuration
- CloudTrail logging for audit

## 📈 Monitoring & Alerts

### CloudWatch Metrics
- Interview completion rates
- AI engine usage (Ollama vs Gemini)
- Application performance metrics
- Cost monitoring and alerts

### Custom Dashboards
- Real-time platform usage
- Error rates and response times
- Resource utilization
- Business metrics (interviews/day, user growth)

### Alerting
- High error rates (>5%)
- Cost thresholds exceeded
- Resource utilization alerts
- Security incidents

## 🔄 CI/CD Integration

### GitHub Actions
- Automated testing on pull requests
- Docker image building and pushing
- Infrastructure deployment
- Application deployment to ECS

### Deployment Strategies
- Blue/green deployments for zero downtime
- Canary releases for gradual rollouts
- Automatic rollback on health check failures
- Database migration handling

## 📋 Deployment Checklist

### Infrastructure Setup
- [ ] AWS account with appropriate permissions
- [ ] S3 bucket created and configured
- [ ] MongoDB Atlas cluster provisioned
- [ ] VPC and networking configured
- [ ] Security groups and IAM roles created

### Application Deployment
- [ ] Docker images built and pushed to ECR
- [ ] ECS service deployed and running
- [ ] Load balancer configured with health checks
- [ ] Domain name and SSL certificate configured
- [ ] Environment variables set

### Monitoring & Security
- [ ] CloudWatch dashboards created
- [ ] Alerts configured for critical metrics
- [ ] Backup procedures tested
- [ ] Security scanning completed
- [ ] Performance testing passed

## 🛠️ Troubleshooting

### Common Issues

**S3 Access Denied**
```bash
# Check bucket policy and IAM permissions
aws s3api get-bucket-policy --bucket genai-career-platform-storage
aws iam simulate-principal-policy --policy-source-arn ROLE_ARN --action-names s3:GetObject
```

**ECS Task Failures**
```bash
# Check task logs
aws logs get-log-events --log-group-name /ecs/genai-career-task
```

**High Costs**
```bash
# Analyze cost breakdown
aws ce get-cost-and-usage --time-period Start=2025-12-01,End=2025-12-31 --granularity MONTHLY
```

### Support Resources
- [AWS Documentation](https://docs.aws.amazon.com/)
- [MongoDB Atlas Documentation](https://docs.atlas.mongodb.com/)
- [ECS Best Practices](https://docs.aws.amazon.com/AmazonECS/latest/bestpracticesguide/)
- [S3 Security Best Practices](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

## 🔗 Related Documentation

- **Architecture Details**: See `architecture.md`
- **Deployment Guide**: See `deployment.md`
- **MongoDB Setup**: See `../mongodb/README.md`
- **Application Docs**: See `../docs/README.md`

---

**🎯 Ready for AWS deployment with S3 and MongoDB Atlas!**