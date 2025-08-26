@echo off
echo ========================================
echo    Ngrok Tunnel for VRP Dashboard
echo ========================================
echo.
echo Starting Ngrok tunnel...
echo.
echo Make sure you have:
echo 1. Downloaded ngrok from ngrok.com
echo 2. Added your authtoken with: ngrok config add-authtoken YOUR_TOKEN
echo.
echo Exposing port 8000 to internet...
echo.
ngrok http 8000
pause 