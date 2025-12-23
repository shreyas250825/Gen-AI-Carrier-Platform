# Docker Configuration Guide 🐳

## 📋 Overview

Complete Docker setup for the GenAI Career Intelligence Platform with support for development, testing, and production environments. All Docker configurations are consolidated into a single `docker-compose.yml` file with profile-based service management.

## 🏗️ Architecture

### Service Stack
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   Frontend       │    │   Backend       │
│   Load Balancer │───▶│   React App      │───▶│   FastAPI       │
│   (Port 80/443) │    │   (Port 3000)    │    │   (Port 8000)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                         │
                       ┌─────────────────────────────────────┼─────────────────────────────────────┐
                       │                                     ▼                                     │
                       │                        ┌─────────────────────┐                          │
                       │                        │   Ollama AI         │                          │
                       │                        │   Local LLM         │                          │
                       │                        │   (Port 11434)      │                          │
                       │                        └─────────────────────┘                          │
                       │                                                                         │
┌─────────────────┐    │    ┌──────────────────┐    ┌─────────────────────┐    ┌──────────────┐ │
│   MongoDB       │◀───┼────│   Redis Cache    │    │   Monitoring        │    │  LocalStack  │ │
│   Database      │    │    │   Session Store  │    │   Prometheus        │    │  AWS Mock    │ │
│   (Port 27017)  │    │    │   (Port 6379)    │    │   Grafana           │    │  (Port 4566) │ │
└─────────────────┘    │    └──────────────────┘    └─────────────────────┘    └──────────────┘ │
                       └─────────────────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### 1. Prerequisites
```bash
# Install Docker and Docker Compose
# Docker Desktop (Windows/Mac) or Docker Engine (Linux)
docker --version
docker-compose --version
```

### 2. Environment Setup
```bash
# Copy environment template
cp .env.docker .env

# Edit configuration (optional)
nano .env
```

### 3. Start Services

#### Full Development Environment
```bash
# Start all services (recommended for development)
docker-compose --profile full up -d

# View logs
docker-compose logs -f

# Check status
docker-compose ps
```

#### Minimal Backend Development
```bash
# Start only backend services
docker-compose --profile backend --profile database --profile ai up -d
```

#### Frontend Development Only
```bash
# Start frontend with backend dependencies
docker-compose --profile frontend --profile backend --profile database up -d
```

## 📊 Service Profiles

### Available Profiles

| Profile | Services | Use Case |
|---------|----------|----------|
| `full` | All core services | Complete development environment |
| `backend` | Backend API | Backend development |
| `frontend` | React app | Frontend development |
| `database` | MongoDB | Database development |
| `ai` | Ollama | AI engine development |
| `cache` | Redis | Caching development |
| `monitoring` | Prometheus, Grafana | Performance monitoring |
| `proxy` | Nginx | Production deployment |
| `testing` | Test services | Automated testing |
| `development` | LocalStack | AWS development |

### Profile Usage Examples

#### Development Scenarios
```bash
# Full development stack
docker-compose --profile full up -d

# Backend + Database + AI only
docker-compose --profile backend --profile database --profile ai up -d

# Frontend development (with backend running separately)
docker-compose --profile frontend up -d

# Database development
docker-compose --profile database up -d
```

#### Production Scenarios
```bash
# Production deployment with monitoring
docker-compose --profile full --profile monitoring --profile proxy up -d

# Production without monitoring
docker-compose --profile full --profile proxy up -d
```

#### Testing Scenarios
```bash
# Run tests
docker-compose --profile testing up --abort-on-container-exit

# Testing with AWS services
docker-compose --profile testing --profile development up --abort-on-container-exit
```

## 🔧 Service Configuration

### Core Services

#### Frontend (React)
```yaml
# Ports: 3000
# Profiles: frontend, full
# Dependencies: backend
# Volumes: ./frontend/src (development)
```

#### Backend (FastAPI)
```yaml
# Ports: 8000
# Profiles: backend, full
# Dependencies: mongodb, ollama, redis
# Volumes: ./backend (development)
# Health Check: /api/health
```

#### MongoDB Database
```yaml
# Ports: 27017
# Profiles: database, full
# Authentication: admin/password (configurable)
# Volumes: mongodb_data, mongodb_config
# Health Check: mongosh ping
```

#### Ollama AI Engine
```yaml
# Ports: 11434
# Profiles: ai, full
# Memory: 4G (configurable)
# Volumes: ollama_data
# Health Check: /api/tags
```

#### Redis Cache
```yaml
# Ports: 6379
# Profiles: cache, full
# Password: configurable
# Volumes: redis_data
# Health Check: redis-cli ping
```

### Additional Services

#### Nginx Proxy
```yaml
# Ports: 80, 443
# Profiles: proxy, production
# Dependencies: frontend, backend
# Volumes: nginx config, SSL certificates
```

#### Monitoring Stack
```yaml
# Prometheus: Port 9090
# Grafana: Port 3001
# Profiles: monitoring
# Volumes: monitoring data
```

#### Development Tools
```yaml
# LocalStack: Port 4566 (AWS emulation)
# Test Runner: Automated testing
# Profiles: development, testing
```

## 🔧 Environment Configuration

### Environment Files

#### Development (.env)
```env
ENVIRONMENT=development
DEBUG=true
MONGODB_URI=mongodb://admin:password@mongodb:27017/genai_career
OLLAMA_MODEL=llama3.1:8b
GEMINI_API_KEY=your_key_here
```

#### Production (.env.prod)
```env
ENVIRONMENT=production
DEBUG=false
RESTART_POLICY=always
MONGODB_URI=mongodb+srv://user:pass@cluster.mongodb.net/genai_career
OLLAMA_MEMORY=8G
```

#### Testing (.env.test)
```env
ENVIRONMENT=testing
MONGODB_DATABASE=genai_career_test
USE_LOCALSTACK=true
CACHE_TTL=0
```

### Key Configuration Options

#### Service Versions
```env
MONGODB_VERSION=7.0
REDIS_VERSION=7.2-alpine
OLLAMA_VERSION=latest
NGINX_VERSION=alpine
```

#### Resource Limits
```env
OLLAMA_MEMORY=4G
OLLAMA_MEMORY_LIMIT=8G
MAX_CONCURRENT_REQUESTS=10
```

#### Security Settings
```env
MONGODB_ROOT_PASSWORD=secure_password
REDIS_PASSWORD=secure_password
SECRET_KEY=secure_secret_key
GRAFANA_PASSWORD=secure_password
```

## 📋 Common Commands

### Service Management
```bash
# Start services
docker-compose --profile full up -d

# Stop services
docker-compose down

# Restart specific service
docker-compose restart backend

# View logs
docker-compose logs -f backend

# Execute commands in container
docker-compose exec backend bash
docker-compose exec mongodb mongosh
```

### Development Workflow
```bash
# Start development environment
docker-compose --profile full up -d

# Watch logs during development
docker-compose logs -f backend frontend

# Rebuild after code changes
docker-compose build backend
docker-compose up -d backend

# Reset database
docker-compose down -v
docker-compose --profile database up -d
```

### Data Management
```bash
# Backup MongoDB data
docker-compose exec mongodb mongodump --out /backup

# Restore MongoDB data
docker-compose exec mongodb mongorestore /backup

# Clear all data (destructive)
docker-compose down -v
```

### AI Model Management
```bash
# Pull Ollama model
docker-compose exec ollama ollama pull llama3.1:8b

# List available models
docker-compose exec ollama ollama list

# Test AI engine
curl http://localhost:11434/api/tags
```

## 🔍 Troubleshooting

### Common Issues

#### Services Won't Start
```bash
# Check Docker daemon
docker info

# Check port conflicts
netstat -tulpn | grep :8000

# Check logs for errors
docker-compose logs backend
```

#### Database Connection Issues
```bash
# Test MongoDB connection
docker-compose exec mongodb mongosh --eval "db.adminCommand('ping')"

# Check MongoDB logs
docker-compose logs mongodb

# Reset MongoDB
docker-compose stop mongodb
docker volume rm genai-career-platform_mongodb_data
docker-compose up -d mongodb
```

#### AI Engine Problems
```bash
# Check Ollama status
docker-compose exec ollama ollama list

# Pull model manually
docker-compose exec ollama ollama pull llama3.1:8b

# Check Ollama logs
docker-compose logs ollama
```

#### Memory Issues
```bash
# Check container resource usage
docker stats

# Increase Ollama memory limit
# Edit .env: OLLAMA_MEMORY_LIMIT=16G
docker-compose up -d ollama
```

### Performance Optimization

#### Resource Allocation
```env
# Increase memory for AI processing
OLLAMA_MEMORY=8G
OLLAMA_MEMORY_LIMIT=16G

# Optimize backend performance
MAX_CONCURRENT_REQUESTS=20
CACHE_TTL=600
```

#### Network Optimization
```yaml
# Use custom network for better performance
networks:
  genai-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.20.0.0/16
```

## 🚀 Production Deployment

### Production Configuration
```bash
# Use production environment
cp .env.docker .env.prod

# Edit production settings
nano .env.prod

# Deploy with production profile
docker-compose --env-file .env.prod --profile full --profile proxy --profile monitoring up -d
```

### Security Hardening
```env
# Strong passwords
MONGODB_ROOT_PASSWORD=complex_secure_password_2025
REDIS_PASSWORD=complex_secure_password_2025
SECRET_KEY=complex_secure_secret_key_2025

# Restrict access
ALLOWED_HOSTS=["your-domain.com"]
CORS_ORIGINS=["https://your-domain.com"]
```

### SSL Configuration
```bash
# Add SSL certificates
mkdir -p nginx/ssl
cp your-cert.pem nginx/ssl/
cp your-key.pem nginx/ssl/

# Update nginx configuration
# Edit nginx/nginx.conf for SSL
```

### Monitoring Setup
```bash
# Start with monitoring
docker-compose --profile full --profile monitoring up -d

# Access monitoring
# Prometheus: http://localhost:9090
# Grafana: http://localhost:3001 (admin/password)
```

## 📊 Health Checks

### Service Health Monitoring
```bash
# Check all service health
docker-compose ps

# Individual service health
curl http://localhost:8000/api/health
curl http://localhost:11434/api/tags
```

### Automated Health Checks
All services include built-in health checks:
- **Backend**: HTTP health endpoint
- **MongoDB**: Database ping
- **Redis**: Redis ping
- **Ollama**: API availability
- **Nginx**: Configuration validation

## 🔄 CI/CD Integration

### GitHub Actions Example
```yaml
name: Docker Build and Test
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          cp .env.docker .env
          docker-compose --profile testing up --abort-on-container-exit
```

### Automated Deployment
```bash
# Build and push images
docker-compose build
docker-compose push

# Deploy to production
docker-compose --env-file .env.prod --profile full --profile proxy up -d
```

---

## 📚 Additional Resources

- **Docker Documentation**: [https://docs.docker.com/](https://docs.docker.com/)
- **Docker Compose Reference**: [https://docs.docker.com/compose/](https://docs.docker.com/compose/)
- **Production Best Practices**: See AWS deployment guide
- **Monitoring Setup**: See monitoring documentation

**🎯 Complete Docker solution for all environments!**