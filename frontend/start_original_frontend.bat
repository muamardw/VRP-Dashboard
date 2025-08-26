@echo off
echo 🚚 FRONTEND VRP DQN - VERSI ORIGINAL
echo ======================================
echo.
echo ✅ Frontend sudah dikembalikan ke versi semula:
echo    • Map container dengan peta interaktif
echo    • Detail rute panel
echo    • Control button "📋 Detail Rute"
echo    • Legend peta
echo    • Tanpa fitur faktor dinamis
echo.
echo 🚀 Menjalankan frontend original...
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
echo 🗺️ FITUR YANG TERSEDIA:
echo    • Peta interaktif dengan marker destinasi
echo    • Panel detail rute (klik "📋 Detail Rute")
echo    • Info traffic dan cuaca per destinasi
echo    • Update otomatis setiap 30 detik
echo.
echo 🗺️ Peta akan terbuka di browser...
echo.

REM Start the development server
npm start

pause 