@echo off
echo 🏢 FRONTEND VRP DQN - DEPOT PUSAT
echo ====================================
echo.
echo ✅ Depot marker sudah diperbaiki:
echo    • Ikon depot yang lebih besar dan menonjol
echo    • Animasi pulse untuk menarik perhatian
echo    • Info koneksi ke 4 destinasi
echo    • Popup detail dengan semua informasi
echo    • Garis koneksi yang lebih jelas
echo    • Header dengan info depot pusat
echo.
echo 🚀 Menjalankan frontend dengan depot...
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
echo 🏢 FITUR DEPOT YANG TERSEDIA:
echo    • Ikon depot merah dengan animasi pulse
echo    • Info "4 Destinasi" di dalam marker
echo    • Popup detail dengan semua koneksi
echo    • Garis koneksi putus-putus ke setiap destinasi
echo    • Header dengan info depot pusat
echo    • Klik depot untuk melihat detail lengkap
echo.
echo 🗺️ Peta akan terbuka di browser...
echo.

REM Start the development server
npm start

pause 