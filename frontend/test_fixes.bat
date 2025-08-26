@echo off
echo 🔧 TESTING FIXES
echo ================
echo.
echo 🔍 Memeriksa 2 perbaikan:
echo    1. Ikon depot muncul di peta (marker merah)
echo    2. Format ETA: di bawah 1 jam = menit, di atas 1 jam = jam
echo.
echo 📋 Langkah-langkah test:
echo    1. Frontend akan terbuka di browser
echo    2. Cari marker depot merah di peta Jakarta Pusat
echo    3. Klik marker depot untuk popup detail
echo    4. Klik marker destinasi untuk melihat ETA
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
echo ⏱️ Cek format ETA: 0.5 jam = 30 menit, 1.2 jam = 1.2 jam
echo.

REM Start the development server
npm start

echo.
echo ✅ Test selesai!
echo 💡 Jika ada masalah, cek console browser untuk error
pause 