# 🚀 Quick Start Guide - AWS ImpactX Challenge Demo

## ❌ Current Issue: Missing Dependencies

The error you're seeing is because the AWS and MongoDB dependencies are not installed in your Python environment.

## 🔧 Quick Fix (Choose One Method)

### Method 1: Install All Dependencies
```bash
cd gen-ai-carrier-platform/backend
pip install -r requirements.txt
```

### Method 2: Install Critical Dependencies Only
```bash
cd gen-ai-carrier-platform/backend
pip install boto3 pymongo python-dotenv
```

### Method 3: Use Quick Fix Script
```bash
cd gen-ai-carrier-platform/backend
python quick_fix.py
```

## 🎯 Complete Setup Process

### 1. Install Dependencies
```bash
cd gen-ai-carrier-platform/backend
pip install -r requirements.txt
```

### 2. Set Environment Variables
Create or update `.env` file in backend directory:
```env
# Demo Mode (works without real AWS credentials)
DEMO_MODE=true

# AI Engine Configuration
OLLAMA_BASE_URL=http://localhost:11434
GEMINI_API_KEY=your_gemini_key_here

# Optional: Real AWS credentials (not needed for demo)
AWS_S3_BUCKET=genai-career-demo-bucket
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key

# Optional: Real MongoDB (not needed for demo)
MONGODB_URI=mongodb://localhost:27017/genai_career
```

### 3. Start Backend Server
```bash
cd gen-ai-carrier-platform/backend
uvicorn app.main:app --reload
```

### 4. Start Frontend (New Terminal)
```bash
cd gen-ai-carrier-platform/frontend
npm install
npm start
```

## 🎭 Demo Mode Features

The system works in **DEMO MODE** by default, which means:

- ✅ **No AWS credentials required** - uses local file storage
- ✅ **No MongoDB required** - uses local JSON storage  
- ✅ **Pre-loaded sample data** - ready for immediate demonstration
- ✅ **All features work** - S3 and MongoDB integration simulated

## 🌐 Access Points

Once running, access these URLs:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Demo Dashboard**: http://localhost:3000/demo
- **Demo API Status**: http://localhost:8000/api/v1/demo/status

## 🎯 AWS ImpactX Challenge Demo

Navigate to the **Demo** section in the frontend to showcase:

1. **Platform Overview** - Real-time system status
2. **S3 Integration** - File upload demonstration  
3. **MongoDB Demo** - Job fit analysis with data storage
4. **Architecture** - Technical overview for judges

## 🔍 Troubleshooting

### Issue: ModuleNotFoundError: No module named 'boto3'
**Solution**: Run `pip install boto3 pymongo`

### Issue: MongoDB connection failed
**Solution**: This is expected in demo mode - the system automatically falls back to local storage

### Issue: Ollama not available
**Solution**: The system automatically falls back to Gemini or demo responses

### Issue: Frontend not connecting to backend
**Solution**: Ensure backend is running on port 8000 and frontend on port 3000

## 🚀 Production Deployment

For production deployment with real AWS services:

1. Set `DEMO_MODE=false` in environment
2. Provide real AWS credentials
3. Configure MongoDB Atlas connection
4. Use Docker deployment: `docker-compose --profile full up -d`

## 📞 Support

If you encounter any issues:

1. Check that all dependencies are installed: `pip list | grep -E "(boto3|pymongo|fastapi)"`
2. Verify environment variables are set correctly
3. Check logs for specific error messages
4. Ensure ports 3000 and 8000 are available

---

**🎯 Ready for AWS ImpactX Challenge presentation!**