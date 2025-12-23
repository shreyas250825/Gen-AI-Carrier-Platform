# Ollama Setup Guide

This guide explains how to set up Ollama for local AI processing in the GenAI Career Intelligence Platform.

## What is Ollama?

Ollama is an open-source tool that allows you to run large language models locally on your machine. This provides:

- **Privacy**: All AI processing happens locally
- **Cost Savings**: No API costs for AI operations
- **Offline Capability**: Works without internet connection
- **Performance**: Often faster than cloud APIs

## Installation

### Windows

1. Download Ollama from [https://ollama.ai](https://ollama.ai)
2. Run the installer
3. Ollama will start automatically as a service

### macOS

```bash
# Using Homebrew
brew install ollama

# Or download from https://ollama.ai
```

### Linux

```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

## Model Setup

After installing Ollama, you need to pull a model:

```bash
# Recommended model for interview platform (8B parameters, good balance of speed/quality)
ollama pull llama3.1:8b

# Alternative models:
ollama pull llama3.1:7b    # Faster, less memory
ollama pull llama3.1:13b   # Better quality, more memory
ollama pull codellama:7b   # Specialized for code
```

## Configuration

The platform is configured via environment variables in `backend/.env`:

```env
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b
OLLAMA_TIMEOUT=30
PREFER_OLLAMA=true
FALLBACK_TO_GEMINI=true
```

### Configuration Options

- `OLLAMA_BASE_URL`: Ollama server URL (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: llama3.1:8b)
- `OLLAMA_TIMEOUT`: Request timeout in seconds (default: 30)
- `PREFER_OLLAMA`: Use Ollama as primary engine (default: true)
- `FALLBACK_TO_GEMINI`: Fall back to Gemini if Ollama fails (default: true)

## Verification

### Check Ollama Status

```bash
# Check if Ollama is running
ollama list

# Test a simple prompt
ollama run llama3.1:8b "Hello, how are you?"
```

### Check Platform Integration

1. Start the backend server
2. Visit `http://localhost:8000/api/intelligence-status`
3. Check that Ollama shows as "available"

### API Endpoints

The platform provides several endpoints to monitor AI engine status:

- `GET /api/intelligence-status` - Overall AI system status
- `GET /api/v1/ai-engine/status` - Detailed engine statistics
- `GET /api/v1/ai-engine/health` - Health check with recommendations
- `POST /api/v1/ai-engine/select` - Force engine selection

## Troubleshooting

### Ollama Not Starting

```bash
# Check if Ollama service is running
ps aux | grep ollama

# Start Ollama manually
ollama serve
```

### Model Not Found

```bash
# List available models
ollama list

# Pull the required model
ollama pull llama3.1:8b
```

### Connection Issues

1. Check that Ollama is running on port 11434
2. Verify `OLLAMA_BASE_URL` in `.env` file
3. Check firewall settings

### Performance Issues

1. **Memory**: Ensure you have enough RAM (8GB+ recommended for 8B models)
2. **CPU**: Models run faster on modern CPUs with more cores
3. **GPU**: Ollama can use GPU acceleration if available

### Model Selection

| Model | Size | Memory | Speed | Quality | Use Case |
|-------|------|--------|-------|---------|----------|
| llama3.1:7b | 4GB | 8GB RAM | Fast | Good | Development/Testing |
| llama3.1:8b | 4.7GB | 8GB RAM | Medium | Better | Production (Recommended) |
| llama3.1:13b | 7.3GB | 16GB RAM | Slow | Best | High-quality interviews |

## Fallback System

The platform includes an intelligent fallback system:

1. **Primary**: Ollama (local processing)
2. **Fallback**: Google Gemini (cloud API)
3. **Automatic**: Switches to Gemini if Ollama is unavailable
4. **Recovery**: Switches back to Ollama when it becomes available

## Benefits of Local Processing

### Privacy
- Resume data never leaves your server
- Interview transcripts processed locally
- Complete data sovereignty

### Cost
- No per-request API costs
- Unlimited usage
- Predictable infrastructure costs

### Performance
- No network latency
- Consistent response times
- No rate limiting

### Reliability
- Works offline
- No dependency on external services
- Reduced points of failure

## Production Deployment

### Docker Setup

```dockerfile
# Add to your Dockerfile
FROM ollama/ollama:latest as ollama

# In your main container
COPY --from=ollama /usr/bin/ollama /usr/bin/ollama
```

### Resource Requirements

- **Minimum**: 8GB RAM, 4 CPU cores
- **Recommended**: 16GB RAM, 8 CPU cores
- **Storage**: 10GB+ for models

### Monitoring

Monitor Ollama performance:

```bash
# Check resource usage
ollama ps

# Monitor logs
ollama logs
```

## Security Considerations

1. **Network**: Ollama runs on localhost by default
2. **Access**: No authentication required for local access
3. **Models**: Models are downloaded from Ollama's registry
4. **Data**: All processing happens locally

## Getting Help

- **Ollama Documentation**: [https://github.com/ollama/ollama](https://github.com/ollama/ollama)
- **Platform Issues**: Check `/api/v1/ai-engine/health` endpoint
- **Model Issues**: Try `ollama pull <model>` to re-download

## Next Steps

1. Install Ollama and pull a model
2. Update your `.env` configuration
3. Restart the backend server
4. Test with `/api/intelligence-status`
5. Run an interview to verify everything works

The platform will automatically use Ollama for all AI operations while maintaining the same API interface and functionality.