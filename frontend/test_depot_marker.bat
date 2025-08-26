@echo off
echo 🧪 TESTING DEPOT MARKER
echo =======================
echo.
echo 🔍 Memeriksa apakah ikon depot muncul di peta...
echo.
echo 📋 Langkah-langkah test:
echo    1. Frontend akan terbuka di browser
echo    2. Cari ikon depot merah di peta
echo    3. Ikon seharusnya berada di Jakarta Pusat
echo    4. Klik ikon untuk melihat popup detail
echo    5. Pastikan ada 4 garis koneksi ke destinasi
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
echo 📍 Cari ikon depot merah di peta Jakarta Pusat
echo 🏢 Ikon seharusnya menampilkan "DEPOT" dan "4 Destinasi"
echo.

REM Start the development server
npm start

echo.
echo ✅ Test selesai!
echo 💡 Jika ikon depot tidak muncul, cek console browser untuk error
pause 