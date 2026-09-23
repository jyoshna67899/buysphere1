@echo off
setlocal
cd /d "%~dp0"

echo ========================================
echo        BuySphere AI - Launcher
echo ========================================
where python >nul 2>nul || (echo Python is not installed. Install Python 3.11+ and run again.&pause&exit /b 1)
where npm >nul 2>nul || (echo Node.js/npm is not installed. Install Node.js LTS and run again.&pause&exit /b 1)

if not exist "backend\.venv\Scripts\python.exe" (
  echo Creating backend virtual environment...
  python -m venv backend\.venv
)
call backend\.venv\Scripts\activate.bat
if not exist "backend\.venv\Lib\site-packages\fastapi" (
  echo Installing backend packages...
  python -m pip install -r backend\requirements.txt
)
if not exist "backend\.env" copy /Y backend\.env.example backend\.env >nul
if not exist "frontend\node_modules" (
  echo Installing frontend packages (first run only)...
  cd frontend
  call npm install
  cd ..
)

echo Starting BuySphere backend...
start "BuySphere Backend" cmd /k "cd /d %~dp0backend && call .venv\Scripts\activate.bat && python -m uvicorn app.main:app --reload --port 8000"
timeout /t 3 >nul
echo Starting BuySphere frontend...
start "BuySphere Frontend" cmd /k "cd /d %~dp0frontend && npm run dev"
timeout /t 5 >nul
start "" http://localhost:5173

echo.
echo BuySphere is starting at http://localhost:5173
pause
