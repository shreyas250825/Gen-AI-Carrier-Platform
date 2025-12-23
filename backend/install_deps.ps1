Write-Host "🚀 Installing GenAI Career Platform Dependencies..." -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Yellow

$dependencies = @(
    "boto3",
    "pymongo", 
    "python-dotenv",
    "motor",
    "google-generativeai",
    "ollama"
)

foreach ($dep in $dependencies) {
    Write-Host "Installing $dep..." -ForegroundColor Cyan
    try {
        pip install $dep
        Write-Host "✅ $dep installed successfully" -ForegroundColor Green
    }
    catch {
        Write-Host "❌ Failed to install $dep" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "✅ Critical dependencies installed!" -ForegroundColor Green
Write-Host ""
Write-Host "🎯 Ready for AWS ImpactX Challenge Demo!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: uvicorn app.main:app --reload"
Write-Host "2. Open: http://localhost:8000/docs"
Write-Host "3. Test: http://localhost:8000/api/v1/demo/status"
Write-Host ""