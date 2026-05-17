# Activate virtual environment for PowerShell
Write-Host "Activating virtual environment..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "Virtual environment activated!" -ForegroundColor Green
Write-Host ""
Write-Host "Quick commands:" -ForegroundColor Yellow
Write-Host "  Start server: uvicorn app.main:app --reload" -ForegroundColor Cyan
Write-Host "  Run test:     python test_analysis.py" -ForegroundColor Cyan
Write-Host "  Open browser: http://localhost:8000" -ForegroundColor Cyan
Write-Host ""

# Made with Bob
