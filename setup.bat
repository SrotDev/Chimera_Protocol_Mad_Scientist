@echo off
REM Chimera Protocol Backend Setup Script for Windows

echo.
echo ========================================
echo Chimera Protocol - Backend Setup
echo ========================================
echo.

REM Create virtual environment
echo [1/6] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    echo Make sure Python 3.9+ is installed
    pause
    exit /b 1
)

REM Activate virtual environment
echo [2/6] Activating virtual environment...
call .venv\Scripts\activate.bat

REM Upgrade pip
echo [3/6] Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo [4/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Copy environment file
echo [5/6] Setting up environment file...
if not exist .env (
    copy .env.example .env
    echo Created .env file - please update with your database credentials
) else (
    echo .env file already exists
)

REM Run migrations
echo [6/6] Running database migrations...
python manage.py makemigrations
python manage.py migrate
if errorlevel 1 (
    echo.
    echo WARNING: Database migrations failed
    echo Make sure PostgreSQL is running and credentials in .env are correct
    echo Or edit chimera/settings.py to use SQLite for quick testing
    echo.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo   1. Update .env with your database credentials (if using PostgreSQL)
echo   2. Create a superuser: python manage.py createsuperuser
echo   3. Start the server: python manage.py runserver
echo.
echo API will be available at: http://localhost:8000/api/
echo Admin panel: http://localhost:8000/admin/
echo API docs: http://localhost:8000/swagger/
echo.
pause
