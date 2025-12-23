# AI Integration Guide 🤖

## 📋 Overview

The GenAI Career Intelligence Platform features a sophisticated AI engine system with local and cloud processing capabilities, providing privacy, performance, and reliability.

## 🏗️ AI Architecture

### Dual Engine System
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Application   │    │   AI Engine     │    │   Ollama        │
│   Layer         │───▶│   Router         │───▶│   (Primary)     │
└─────────────────┘    │                  │    │   Local LLM     │
                       │                  │    └─────────────────┘
                       │                  │    ┌─────────────────┐
                       │                  │───▶│   Gemini        │
                       └──────────────────┘    │   (Fallback)    │
                                               │   Cloud API     │
                                               └─────────────────┘
```

### Intelligence Layers
1. **Context Intelligence** - Profile analysis and context extraction
2. **Interview Intelligence** - Question generation and flow management
3. **Evaluation Intelligence** - Answer assessment and scoring

## 🔧 Ollama Integration (Local AI)

### Installation & Setup

#### 1. Install Ollama
```bash
# Windows: Download from https://ollama.ai
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

#### 2. Pull Recommended Model
```bash
# Recommended for production (8B parameters)
ollama pull llama3.1:8b

# Alternative models
ollama pull llama3.1:7b    # Faster, less memory
ollama pull llama3.1:13b   # Better quality, more memory
```

#### 3. Configuration
```env
# backend/.env
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TIMEOUT=30
PREFER_OLLAMA=true
```

### Benefits of Local Processing
- **🔒 Privacy**: Data never leaves your server
- **💰 Cost**: No per-request API charges
- **⚡ Speed**: Often faster than cloud APIs
- **🌐 Offline**: Works without internet connection

### Model Recommendations

| Model | Size | Memory | Speed | Quality | Use Case |
|-------|------|--------|-------|---------|----------|
| llama3.1:7b | 4GB | 8GB RAM | Fast | Good | Development |
| llama3.1:8b | 4.7GB | 8GB RAM | Medium | Better | Production ⭐ |
| llama3.1:13b | 7.3GB | 16GB RAM | Slow | Best | High-quality |

## ☁️ Gemini Integration (Cloud AI)

### Setup
```env
# backend/.env
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
FALLBACK_TO_GEMINI=true
```

### Benefits of Cloud Processing
- **🌍 Reliability**: Always available
- **🚀 Performance**: Consistent response times
- **📈 Scalability**: Handles high loads
- **🔄 Updates**: Latest model improvements

## 🎯 Intelligent Router System

### Automatic Fallback Logic
1. **Primary**: Attempt Ollama (local processing)
2. **Health Check**: Verify Ollama availability
3. **Fallback**: Switch to Gemini if Ollama fails
4. **Recovery**: Monitor and return to Ollama when available
5. **Statistics**: Track usage and performance

### Configuration Options
```env
# AI Engine Preferences
PREFER_OLLAMA=true              # Use Ollama as primary
FALLBACK_TO_GEMINI=true         # Enable automatic fallback
OLLAMA_TIMEOUT=30               # Timeout for Ollama requests
GEMINI_TIMEOUT=30               # Timeout for Gemini requests
```

## 📊 Monitoring & Management

### API Endpoints

#### System Status
```bash
# Overall intelligence status
GET /api/intelligence-status

# Detailed engine health
GET /api/v1/ai-engine/health

# Usage statistics
GET /api/v1/ai-engine/status
```

#### Engine Control
```bash
# Force engine selection
POST /api/v1/ai-engine/select
{
  "engine": "ollama" | "gemini"
}

# Reset to default preferences
POST /api/v1/ai-engine/reset
```

### Health Check Response
```json
{
  "status": "healthy",
  "engines": {
    "ollama": {
      "available": true,
      "model": "llama3.1:8b",
      "response_time": 1.2,
      "last_used": "2025-12-23T10:30:00Z"
    },
    "gemini": {
      "available": true,
      "model": "gemini-pro",
      "response_time": 0.8,
      "last_used": "2025-12-23T09:15:00Z"
    }
  },
  "statistics": {
    "total_requests": 1247,
    "ollama_requests": 1156,
    "gemini_requests": 91,
    "fallback_count": 12
  }
}
```

## 🔧 Implementation Details

### AI Engine Interface
```python
class AIEngine:
    """Base interface for AI engines"""
    
    def extract_candidate_context(self, resume_text: str) -> dict:
        """Extract candidate information from resume"""
        pass
    
    def generate_first_question(self, profile: dict, interview_type: str) -> dict:
        """Generate opening interview question"""
        pass
    
    def generate_next_question(self, context: dict) -> dict:
        """Generate follow-up questions"""
        pass
    
    def evaluate_answer(self, question: str, answer: str, profile: dict) -> dict:
        """Evaluate candidate's answer"""
        pass
    
    def generate_final_report(self, session_data: dict) -> dict:
        """Generate comprehensive interview report"""
        pass
```

### Router Implementation
```python
class AIEngineRouter:
    """Intelligent routing between AI engines"""
    
    def __init__(self):
        self.ollama_engine = OllamaEngine()
        self.gemini_engine = GeminiEngine()
        self.prefer_ollama = True
        self.fallback_enabled = True
    
    def route_request(self, method: str, *args, **kwargs):
        """Route request to appropriate engine with fallback"""
        if self.prefer_ollama and self.ollama_engine.is_available():
            try:
                return self.ollama_engine.__getattribute__(method)(*args, **kwargs)
            except Exception as e:
                if self.fallback_enabled:
                    return self.gemini_engine.__getattribute__(method)(*args, **kwargs)
                raise e
        else:
            return self.gemini_engine.__getattribute__(method)(*args, **kwargs)
```

## 🚀 Production Deployment

### Resource Requirements

#### Ollama Server
- **Minimum**: 8GB RAM, 4 CPU cores
- **Recommended**: 16GB RAM, 8 CPU cores
- **Storage**: 10GB+ for models

#### Application Server
- **CPU**: 2-4 cores
- **Memory**: 4-8GB RAM
- **Storage**: 5GB for application

### Docker Configuration
```dockerfile
# Ollama service
FROM ollama/ollama:latest
EXPOSE 11434
CMD ["ollama", "serve"]

# Application service
FROM python:3.11-slim
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    depends_on:
      - ollama

volumes:
  ollama_data:
```

## 🔍 Troubleshooting

### Common Issues

#### Ollama Connection Failed
```bash
# Check if Ollama is running
ollama list

# Start Ollama service
ollama serve

# Test connection
curl http://localhost:11434/api/tags
```

#### Model Not Found
```bash
# List available models
ollama list

# Pull required model
ollama pull llama3.1:8b
```

#### High Memory Usage
```bash
# Check model size
ollama show llama3.1:8b

# Use smaller model
ollama pull llama3.1:7b
```

#### Gemini API Errors
```bash
# Test API key
curl -H "Authorization: Bearer $GEMINI_API_KEY" \
  https://generativelanguage.googleapis.com/v1/models

# Check quota limits
# Visit Google Cloud Console
```

### Performance Optimization

#### Ollama Optimization
```bash
# Use GPU acceleration (if available)
ollama run llama3.1:8b --gpu

# Adjust context window
ollama run llama3.1:8b --ctx-size 4096
```

#### Application Optimization
```python
# Connection pooling
OLLAMA_POOL_SIZE = 5
GEMINI_POOL_SIZE = 10

# Request caching
CACHE_RESPONSES = True
CACHE_TTL = 300  # 5 minutes
```

## 📈 Performance Metrics

### Typical Response Times
- **Ollama (local)**: 1-3 seconds
- **Gemini (cloud)**: 0.5-2 seconds
- **Router overhead**: <50ms

### Throughput
- **Ollama**: 10-30 requests/minute (depends on hardware)
- **Gemini**: 60+ requests/minute (API limits apply)

### Accuracy Comparison
- **Question Generation**: Both engines perform similarly
- **Answer Evaluation**: Gemini slightly more consistent
- **Report Generation**: Ollama more detailed, Gemini more structured

## 🔐 Security Considerations

### Local Processing (Ollama)
- ✅ Data never leaves your infrastructure
- ✅ No external API calls for sensitive data
- ✅ Complete control over processing

### Cloud Processing (Gemini)
- ⚠️ Data sent to Google's servers
- ✅ Enterprise-grade security
- ✅ Compliance with major standards

### Best Practices
1. **Sensitive Data**: Use Ollama for resume processing
2. **General Queries**: Gemini for non-sensitive operations
3. **Hybrid Approach**: Route based on data sensitivity
4. **Monitoring**: Track which engine processes what data

## 📚 Additional Resources

- **Ollama Documentation**: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Gemini API Docs**: [https://ai.google.dev/docs](https://ai.google.dev/docs)
- **Model Comparison**: [Ollama Model Library](https://ollama.ai/library)
- **Performance Tuning**: See deployment documentation

---

**🎯 The AI integration provides enterprise-grade intelligence with privacy, performance, and reliability!**