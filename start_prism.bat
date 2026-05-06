@echo off
title PRISM IoT Engine
echo [SYSTEM] Starting PRISM Real-Time System...

:: Check for Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.
    pause
    exit /b 1
)

:: Install Dependencies
echo [SYSTEM] Checking dependencies...
pip install flask flask-cors >nul 2>&1

:: Get Local IP
for /f "tokens=4" %%a in ('route print ^| find " 0.0.0.0"') do set IP=%%a

echo ======================================================
echo  PRISM DASHBOARD IS GOING LIVE
echo  1. Dashboard: http://localhost:5000
echo  2. Sensor IP: %IP%:5000
echo ======================================================
echo.

:: Open Browser
start http://localhost:5000

:: Start Server
python app.py
pause
