@echo off
REM Django Development Server Runner
REM Appointment360 Project

echo ========================================
echo Appointment360 - Django Development
echo ========================================
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found.
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Starting Django development server...
echo Access at: http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python manage.py runserver

