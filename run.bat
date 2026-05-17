@echo off
echo Starting Code Analysis Demo Tool...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
echo.

REM Start the server
echo Starting FastAPI server...
echo.
echo Web UI will be available at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn app.main:app --reload --port 8000

@REM Made with Bob
