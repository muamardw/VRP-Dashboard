@echo off
echo 🔧 TESTING DEPOT MARKER FINAL
echo ===============================
echo.
echo 🔍 Memeriksa depot marker:
echo    1. Marker default Leaflet (pin merah)
echo    2. Circle marker backup (lingkaran merah)
echo    3. 4 garis rute dari depot ke destinasi
echo    4. Map terpusat di Jakarta Pusat
echo.
echo 📋 Langkah-langkah test:
echo    1. Frontend akan terbuka di browser
echo    2. Map akan otomatis terpusat di Jakarta Pusat
echo    3. Cari 2 marker depot (pin + lingkaran merah)
echo    4. Pastikan ada 4 garis rute dari depot
echo    5. Klik marker untuk popup info depot
echo    6. Cek console browser untuk debugging info
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
echo 📍 Map akan terpusat di Jakarta Pusat
echo 🏢 Cari 2 marker depot (pin + lingkaran merah)
echo 🛣️ Pastikan ada 4 garis rute dari depot
echo 🔍 Cek console browser untuk debugging
echo.

REM Start the development server
npm start

echo.
echo ✅ Test selesai!
echo 💡 Jika depot masih tidak muncul, cek console browser
echo 📍 Koordinat depot: -6.2088, 106.8456 (Jakarta Pusat)
pause 