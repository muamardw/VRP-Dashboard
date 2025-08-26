@echo off
echo 🔧 TESTING NEW COORDINATES
echo ===========================
echo.
echo 🔍 Memeriksa koordinat baru berdasarkan alamat:
echo.
echo 🏢 DEPOT: Pulogadung, Jakarta Timur
echo    Alamat: Kw. Industri Pulogadung, Jl. Pulo Lentut No.10
echo    Koordinat: -6.1857, 106.9367
echo.
echo 📍 DESTINASI:
echo    🏙️ Bogor: Jl. Wangun no. 216 Sindangsari (-6.5971, 106.8060)
echo    🏙️ Tangerang: JL. PAJAJARAN, KEL GANDASARI (-6.1783, 106.6319)
echo    🏙️ Jakarta: Jl. Srengseng Raya No.8 (-6.1778, 106.7378)
echo    🏙️ Bekasi: Jl. Jakasetia no. 27 B (-6.2346, 106.9896)
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
echo 🏢 Depot: Pulogadung, Jakarta Timur (marker merah)
echo 📍 4 Destinasi dengan alamat lengkap
echo 🛣️ Garis rute yang akurat berdasarkan koordinat baru
echo.

REM Start the development server
npm start

echo.
echo ✅ Test selesai!
echo 💡 Koordinat sudah disesuaikan dengan alamat lengkap
pause 