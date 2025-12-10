@echo off
echo Starting GitHub Analysis Service...
echo.

REM Set Python path
set PYTHONPATH=%PYTHONPATH%;%CD%

REM Start the service
cd services\github_analysis
python main.py
