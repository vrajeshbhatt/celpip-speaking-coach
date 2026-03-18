@echo off
echo ===================================================
echo     CELPIP Speaking Coach
echo ===================================================

if not exist venv\Scripts\python.exe (
    echo [ERROR] Virtual environment not found.
    echo Please run setup first:
    echo python -m venv venv
    echo .\venv\Scripts\pip install -r requirements.txt
    pause
    exit /b 1
)

echo Starting application server...
.\venv\Scripts\python.exe app.py
pause
