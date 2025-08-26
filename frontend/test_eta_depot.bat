@echo off
echo 🔧 TESTING ETA FORMAT & DEPOT MARKER
echo ======================================
echo.
echo 🔍 Memeriksa 2 perbaikan:
echo    1. Format ETA: 1.5 jam = 1 jam 30 menit
echo    2. Depot marker muncul di peta (4 garis rute)
echo.
echo 📋 Langkah-langkah test:
echo    1. Frontend akan terbuka di browser
echo    2. Cari marker depot merah di peta Jakarta Pusat
echo    3. Pastikan ada 4 garis rute dari depot ke destinasi
echo    4. Klik marker destinasi untuk melihat format ETA baru
echo    5. Cek format ETA di popup dan detail panel
echo.
echo 🚀 Menjalankan test...
echo.

cd /d "%~dp0"

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js tidak ditemukan!
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm tidak ditemukan!
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

echo.
echo 🌐 Membuka browser...
echo 📍 Cari marker depot merah di peta Jakarta Pusat
echo 🛣️ Pastikan ada 4 garis rute dari depot
echo ⏱️ Cek format ETA: 1.5 jam = 1 jam 30 menit
echo.

REM Start the development server
npm start

echo.
echo ✅ Test selesai!
echo 💡 Jika ada masalah, cek console browser untuk error
pause 