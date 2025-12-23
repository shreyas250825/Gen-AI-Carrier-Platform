# Documentation 📚

## 📋 Overview

Comprehensive documentation for the GenAI Career Intelligence Platform, covering all aspects from setup to advanced usage.

## 📁 Documentation Structure

### Core Documentation
- **`README.md`** - This overview file
- **`ai-integration.md`** - AI engine setup and configuration
- **`api-documentation.md`** - Complete API reference

### Related Documentation
- **`../mongodb/README.md`** - MongoDB Atlas setup and configuration
- **`../aws/README.md`** - AWS deployment and architecture
- **`../frontend/src/styles/DESIGN_SYSTEM.md`** - Frontend design system

## 🚀 Quick Start Guide

### 1. System Requirements
- **Python**: 3.11+
- **Node.js**: 18+
- **Memory**: 8GB+ RAM (for Ollama)
- **Storage**: 20GB+ available space

### 2. Installation Steps

#### Backend Setup
```bash
# Clone repository
git clone https://github.com/your-repo/genai-career-platform.git
cd genai-career-platform

# Setup Python environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your configuration
```

#### Frontend Setup
```bash
# Setup React application
cd frontend
npm install
npm start
```

#### AI Engine Setup
```bash
# Install Ollama (see ai-integration.md for details)
# Download from https://ollama.ai
ollama pull llama3.1:8b

# Configure Gemini API (optional)
# Add GEMINI_API_KEY to .env file
```

#### Database Setup
```bash
# Setup MongoDB Atlas (see ../mongodb/README.md)
cd mongodb
python setup_script.py
```

### 3. Start the Platform
```bash
# Start backend (Terminal 1)
cd backend
uvicorn app.main:app --reload

# Start frontend (Terminal 2)
cd frontend
npm start

# Access the platform
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## 🏗️ Architecture Overview

### System Components
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   React         │    │   FastAPI        │    │   AI Engines    │
│   Frontend      │───▶│   Backend        │───▶│   Ollama/Gemini │
│   (Port 3000)   │    │   (Port 8000)    │    │   Local/Cloud   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Data Storage   │
                       │   MongoDB Atlas  │
                       │   Amazon S3      │
                       └──────────────────┘
```

### Key Features
- **🤖 Dual AI Processing**: Local (Ollama) + Cloud (Gemini) with intelligent routing
- **📝 Smart Interviews**: Dynamic question generation and real-time evaluation
- **🎯 Job Fit Analysis**: AI-powered role matching with comprehensive scoring
- **🧠 Aptitude Testing**: Multi-category assessments with detailed analytics
- **📊 Analytics Dashboard**: Real-time performance tracking and insights
- **🔒 Privacy-First**: Local AI processing for sensitive data

## 📖 Feature Documentation

### Interview System
The platform provides comprehensive interview capabilities:

#### Interview Types
- **Technical Interviews**: Programming, system design, algorithms
- **Behavioral Interviews**: Leadership, teamwork, problem-solving
- **Domain-Specific**: Role-tailored questions for specific positions

#### AI-Powered Features
- **Dynamic Question Generation**: Context-aware questions based on resume
- **Real-time Evaluation**: Instant feedback with scoring and suggestions
- **Adaptive Difficulty**: Questions adjust based on candidate performance
- **Comprehensive Reports**: Detailed analysis with improvement recommendations

### Job Fit Analysis
Advanced matching system for role compatibility:

#### Analysis Components
- **Skill Matching**: Technical and soft skill alignment
- **Experience Assessment**: Years and quality of relevant experience
- **Project Relevance**: Portfolio and project alignment
- **Growth Potential**: Learning trajectory and adaptability

#### Supported Roles (50+)
- Software Engineering (Frontend, Backend, Full-Stack, DevOps)
- Data & Analytics (Data Scientist, Analyst, Engineer)
- AI/ML (ML Engineer, AI Researcher, Data Engineer)
- Leadership (Tech Lead, Engineering Manager, CTO)
- Specialized (Security, Mobile, Game Development)

### Resume Processing
Intelligent document analysis and extraction:

#### Supported Formats
- **PDF**: Advanced text extraction with layout preservation
- **DOCX**: Microsoft Word document processing
- **TXT**: Plain text resume parsing

#### Extraction Capabilities
- **Skills**: 500+ technical keywords across all domains
- **Experience**: Accurate parsing of work history and duration
- **Education**: Degree, institution, and graduation year extraction
- **Projects**: Project descriptions and technology stack identification

## 🔧 Configuration Guide

### Environment Variables

#### Core Configuration
```env
# Application Settings
DEBUG=false
PORT=8000
CORS_ORIGINS=["http://localhost:3000"]

# Database Configuration
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/genai_career

# AI Engine Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
GEMINI_API_KEY=your_gemini_api_key
PREFER_OLLAMA=true
FALLBACK_TO_GEMINI=true

# Storage Configuration
AWS_S3_BUCKET=genai-career-platform-storage
AWS_REGION=us-east-1
```

#### Advanced Settings
```env
# Performance Tuning
OLLAMA_TIMEOUT=30
GEMINI_TIMEOUT=30
MAX_CONCURRENT_REQUESTS=10
CACHE_TTL=300

# Security Settings
SECRET_KEY=your_secret_key_here
ALLOWED_HOSTS=["localhost", "your-domain.com"]
RATE_LIMIT_PER_MINUTE=100

# Logging Configuration
LOG_LEVEL=INFO
LOG_FORMAT=json
ENABLE_REQUEST_LOGGING=true
```

### Feature Flags
```env
# Feature Toggles
ENABLE_VOICE_INTERVIEWS=false
ENABLE_VIDEO_ANALYSIS=false
ENABLE_REAL_TIME_COLLABORATION=false
ENABLE_ADVANCED_ANALYTICS=true
```

## 🔍 Troubleshooting Guide

### Common Issues

#### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Verify dependencies
pip list | grep fastapi

# Check port availability
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows
```

#### Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check Node.js version
node --version  # Should be 18+

# Verify environment variables
cat .env.local
```

#### AI Engine Issues
```bash
# Test Ollama connection
curl http://localhost:11434/api/tags

# Check model availability
ollama list

# Test Gemini API
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models
```

#### Database Connection Problems
```bash
# Test MongoDB connection
python -c "from mongodb.config import MongoDBConfig; print('✅ Connected!' if MongoDBConfig().get_database() else '❌ Failed')"

# Check network connectivity
ping cluster.mongodb.net

# Verify credentials
echo $MONGODB_URI
```

### Performance Optimization

#### Backend Optimization
```python
# Increase worker processes
uvicorn app.main:app --workers 4 --host 0.0.0.0 --port 8000

# Enable caching
REDIS_URL=redis://localhost:6379
CACHE_BACKEND=redis

# Database connection pooling
MONGODB_MAX_POOL_SIZE=100
MONGODB_MIN_POOL_SIZE=10
```

#### Frontend Optimization
```bash
# Build for production
npm run build

# Analyze bundle size
npm install -g webpack-bundle-analyzer
npx webpack-bundle-analyzer build/static/js/*.js
```

#### AI Engine Optimization
```bash
# Use GPU acceleration (if available)
ollama run llama3.1:8b --gpu

# Optimize model parameters
ollama run llama3.1:8b --ctx-size 4096 --batch-size 512
```

## 📊 Monitoring & Analytics

### Health Monitoring
```bash
# System health check
curl http://localhost:8000/api/health

# AI engine status
curl http://localhost:8000/api/v1/ai-engine/status

# Database connectivity
curl http://localhost:8000/api/v1/health/database
```

### Performance Metrics
- **Response Times**: API endpoint latency tracking
- **AI Engine Usage**: Ollama vs Gemini request distribution
- **Success Rates**: Interview completion and error rates
- **Resource Usage**: CPU, memory, and storage utilization

### Business Metrics
- **Interview Volume**: Daily/weekly interview counts
- **User Engagement**: Session duration and completion rates
- **Job Fit Success**: Placement and satisfaction rates
- **Platform Growth**: User acquisition and retention

## 🔐 Security Best Practices

### Data Protection
- **Encryption**: All data encrypted in transit and at rest
- **Access Control**: Role-based permissions and authentication
- **Privacy**: Local AI processing for sensitive data
- **Compliance**: GDPR and SOC 2 compliance ready

### API Security
- **Rate Limiting**: Prevent abuse and ensure fair usage
- **Input Validation**: Comprehensive request sanitization
- **CORS Configuration**: Proper cross-origin resource sharing
- **Security Headers**: Standard security header implementation

### Infrastructure Security
- **Network Security**: VPC and security group configuration
- **Secrets Management**: Environment variable encryption
- **Audit Logging**: Comprehensive activity tracking
- **Backup Strategy**: Regular data backup and recovery testing

## 📚 Additional Resources

### Development Resources
- **API Documentation**: Complete endpoint reference with examples
- **SDK Libraries**: Python and JavaScript client libraries
- **Postman Collection**: Ready-to-use API testing collection
- **Docker Compose**: Local development environment setup

### Deployment Resources
- **AWS Guide**: Production deployment on AWS infrastructure
- **Docker Images**: Containerized deployment options
- **CI/CD Pipelines**: Automated testing and deployment
- **Monitoring Setup**: CloudWatch and custom metrics

### Community Resources
- **GitHub Repository**: Source code and issue tracking
- **Documentation Site**: Comprehensive online documentation
- **Community Forum**: Developer discussions and support
- **Video Tutorials**: Step-by-step setup and usage guides

## 🎯 Getting Help

### Support Channels
1. **Documentation**: Check this comprehensive guide first
2. **API Reference**: Detailed endpoint documentation
3. **GitHub Issues**: Bug reports and feature requests
4. **Community Forum**: Developer discussions and Q&A

### Reporting Issues
When reporting issues, please include:
- **Environment**: OS, Python/Node versions, dependencies
- **Configuration**: Relevant environment variables (redacted)
- **Error Messages**: Complete error logs and stack traces
- **Steps to Reproduce**: Detailed reproduction steps
- **Expected Behavior**: What should happen vs what actually happens

---

**🎯 Complete documentation for the GenAI Career Intelligence Platform!**