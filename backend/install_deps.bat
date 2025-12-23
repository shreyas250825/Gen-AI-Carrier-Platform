@echo off
echo 🚀 Installing GenAI Career Platform Dependencies...
echo ================================================

echo Installing boto3 (AWS SDK)...
pip install boto3

echo Installing pymongo (MongoDB driver)...
pip install pymongo

echo Installing python-dotenv (Environment variables)...
pip install python-dotenv

echo Installing motor (Async MongoDB driver)...
pip install motor

echo Installing google-generativeai (Gemini AI)...
pip install google-generativeai

echo Installing ollama (Local LLM)...
pip install ollama

echo.
echo ✅ Critical dependencies installed!
echo.
echo 🎯 Ready for AWS ImpactX Challenge Demo!
echo.
echo Next steps:
echo 1. Run: uvicorn app.main:app --reload
echo 2. Open: http://localhost:8000/docs
echo 3. Test: http://localhost:8000/api/v1/demo/status
echo.
pause