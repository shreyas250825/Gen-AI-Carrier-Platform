# 🧪 Testing Suite

This directory contains all testing files for the Gen AI Career Intelligence Platform.

## 📋 Test Categories

### 🚀 **System Integration Tests**
- **`test_complete_system.py`** - Comprehensive end-to-end system test
- **`test_system.py`** - Core system functionality tests
- **`test_endpoints.py`** - API endpoint testing

### 🤖 **AI Engine Tests**
- **`test_gemini_integration.py`** - Gemini AI engine integration tests
- **`test_gemini_api.py`** - Direct Gemini API testing with model discovery
- **`test_single_gemini_call.py`** - Single API call testing
- **`test_updated_gemini.py`** - Updated Gemini engine testing
- **`test_intelligence_engine.py`** - Three-level intelligence system tests

### 💼 **Feature-Specific Tests**
- **`test_job_fit_debug.py`** - Job fit analysis debugging
- **`test_job_fit_direct.py`** - Direct job fit functionality testing
- **`test_resume_upload.py`** - Resume upload and parsing tests

### 🔧 **Infrastructure Tests**
- **`test_env_loading.py`** - Environment variable loading tests
- **`test_imports.py`** - Module import verification

### 📜 **Legacy Tests**
- **`test_openrouter.py`** - OpenRouter tests (deprecated, kept for reference)

### ⚙️ **Setup & Configuration**
- **`setup_intelligence_engine.py`** - Intelligence engine setup script

## 🏃‍♂️ **How to Run Tests**

### **Prerequisites**
```bash
# Ensure you're in the project root
cd gen-ai-carrier-platform

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
cp backend/.env.example backend/.env
# Add your GEMINI_API_KEY to the .env file
```

### **Run Individual Tests**
```bash
# Complete system test (recommended first test)
python tests/test_complete_system.py

# Test Gemini API integration
python tests/test_gemini_integration.py

# Test specific endpoints
python tests/test_endpoints.py

# Debug environment setup
python tests/test_env_loading.py
```

### **Run All Tests**
```bash
# Run all Python test files
for file in tests/test_*.py; do echo "Running $file"; python "$file"; echo ""; done
```

## 📊 **Test Results Interpretation**

### **✅ Success Indicators**
- `✅` - Test passed successfully
- `🎉` - Major milestone completed
- `📝` - Information/status message

### **❌ Error Indicators**
- `❌` - Test failed
- `⚠️` - Warning (may still work with fallbacks)
- `🔍` - Debug information

### **🧠 Intelligence Levels**
- **Level 1**: Deterministic fallbacks (always works)
- **Level 2**: Local AI (Ollama, if available)
- **Level 3**: Cloud AI (Gemini API)

## 🔑 **Environment Setup**

### **Required Environment Variables**
```bash
# In backend/.env
GEMINI_API_KEY=your-gemini-api-key-here
DATABASE_URL=sqlite:///./interview.db
FRONTEND_URL=http://localhost:3000
```

### **Optional Environment Variables**
```bash
HF_API_TOKEN=your-huggingface-token  # For legacy compatibility
DEBUG=True
SECRET_KEY=your-secret-key
```

## 🎯 **Key Test Scenarios**

### **1. Basic Functionality**
```bash
python tests/test_complete_system.py
```
Tests: Health check, interview flow, aptitude, job fit, intelligence status

### **2. AI Integration**
```bash
python tests/test_gemini_integration.py
```
Tests: Question generation, answer evaluation, job fit analysis

### **3. API Endpoints**
```bash
python tests/test_endpoints.py
```
Tests: Aptitude generation, job fit analysis endpoints

### **4. Environment Debugging**
```bash
python tests/test_env_loading.py
```
Tests: Environment variable loading, API key detection

## 🚨 **Common Issues & Solutions**

### **Issue: "GEMINI_API_KEY not found"**
**Solution**: 
1. Check if `.env` file exists in `backend/` directory
2. Verify the API key is correctly set
3. Run `python tests/test_env_loading.py` to debug

### **Issue: "429 Too Many Requests"**
**Solution**: 
- Wait a few minutes between API calls
- The system will use intelligent fallbacks
- All functionality still works with fallback responses

### **Issue: "404 Model Not Found"**
**Solution**: 
- Run `python tests/test_gemini_api.py` to check available models
- The system automatically uses the correct model (`gemini-2.0-flash`)

### **Issue: Import Errors**
**Solution**: 
1. Ensure you're running from project root
2. Check Python path: `python tests/test_imports.py`
3. Install missing dependencies: `pip install -r backend/requirements.txt`

## 📈 **Test Coverage**

- ✅ **Interview System**: Conversational flow, question generation, answer evaluation
- ✅ **Aptitude Assessment**: Question generation, answer evaluation, scoring
- ✅ **Job Fit Analysis**: Resume parsing, skill matching, recommendations
- ✅ **AI Integration**: Gemini API, fallback systems, error handling
- ✅ **API Endpoints**: All major endpoints tested
- ✅ **Environment**: Configuration loading, API key validation

## 🔄 **Continuous Testing**

For development, you can set up a simple test runner:

```bash
# Create a simple test runner script
echo '#!/bin/bash
echo "🧪 Running Core Tests..."
python tests/test_complete_system.py
echo ""
echo "🤖 Testing AI Integration..."
python tests/test_gemini_integration.py
echo ""
echo "📡 Testing API Endpoints..."
python tests/test_endpoints.py
echo ""
echo "✅ Testing Complete!"' > run_tests.sh

chmod +x run_tests.sh
./run_tests.sh
```

## 📝 **Adding New Tests**

When adding new tests, follow this naming convention:
- `test_[feature]_[specific_aspect].py`
- Include comprehensive docstrings
- Use the established emoji system for output
- Include both success and failure scenarios
- Test with and without API keys (fallback scenarios)

---

**Last Updated**: December 2025  
**Test Suite Version**: 2.0 (Post-Gemini Migration)  
**Total Tests**: 15 test files covering all major functionality