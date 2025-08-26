@echo off
echo 🏢 FRONTEND VRP DQN - IKON DEPOT DI PETA
echo ==========================================
echo.
echo ✅ Ikon depot di peta sudah diperbaiki:
echo    • Ikon depot yang lebih besar (100x100 pixel)
echo    • Animasi pulse yang lebih menonjol
echo    • Hub indicator dengan ikon ⚡
echo    • Circle hub yang berputar di background
echo    • Z-index tinggi agar selalu di atas
echo    • Shadow dan border yang lebih tebal
echo    • Info "4 Destinasi" yang jelas
echo.
echo 🚀 Menjalankan frontend dengan ikon depot...
echo.

cd /d "%~dp0"

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js tidak ditemukan!
    echo 💡 Silakan install Node.js dari https://nodejs.org/
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm tidak ditemukan!
    echo 💡 Silakan install npm
    pause
    exit /b 1
)

REM Check if package.json exists
if not exist "package.json" (
    echo ❌ Tidak berada di direktori frontend!
    echo 💡 Jalankan script ini dari folder frontend/
    pause
    exit /b 1
)

REM Install dependencies if node_modules doesn't exist
if not exist "node_modules" (
    echo 📦 Menginstall dependencies...
    npm install
    if %errorlevel% neq 0 (
        echo ❌ Gagal menginstall dependencies!
        pause
        exit /b 1
    )
    echo ✅ Dependencies berhasil diinstall!
)

echo.
echo 🏢 FITUR IKON DEPOT DI PETA:
echo    • Ikon 🏢 yang besar dan menonjol
echo    • Animasi pulse untuk menarik perhatian
echo    • Hub indicator ⚡ di pojok kanan atas
echo    • Circle hub yang berputar di background
echo    • Info "4 Destinasi" di dalam ikon
echo    • Klik ikon untuk melihat detail lengkap
echo    • Popup dengan semua informasi koneksi
echo.
echo 🗺️ Peta akan terbuka di browser...
echo.

REM Start the development server
npm start

pause 