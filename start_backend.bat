@echo off
echo ========================================
echo    VRP Dashboard Backend Server
echo ========================================
echo.
echo Starting backend server...
echo.
cd vrp_rl_project
echo Installing dependencies...
pip install fastapi uvicorn pydantic requests openrouteservice python-dotenv python-multipart
echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
uvicorn backend_api:app --host 0.0.0.0 --port 8000
pause 