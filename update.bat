@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║        SCHEDULED CONCURRENT AGENT - Update                    ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment diaktifkan
) else (
    echo ❌ Virtual environment tidak ditemukan!
    echo Jalankan setup.bat terlebih dahulu
    pause
    exit /b 1
)

echo.
echo 📦 Mengecek updates...
echo.

REM Update pip
echo 🔄 Updating pip...
python -m pip install --upgrade pip

REM Update packages
echo.
echo 🔄 Updating packages...
pip install --upgrade openhands-sdk openhands-tools pydantic

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    ✅ UPDATE COMPLETE                         ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 💡 Jalankan agent dengan: run.bat
echo.

pause
