@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║     SCHEDULED CONCURRENT AGENT - Installation Wizard          ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo [1/4] Memeriksa instalasi Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python tidak ditemukan!
    echo.
    echo Silakan install Python terlebih dahulu:
    echo    https://www.python.org/downloads/
    echo.
    echo Pastikan Python添加到 PATH saat instalasi
    echo.
    pause
    exit /b 1
)
echo ✅ Python ditemukan

REM Check pip
echo.
echo [2/4] Memeriksa pip...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip tidak ditemukan
    echo.
    echo Coba install dengan: python -m ensurepip
    echo.
    pause
    exit /b 1
)
echo ✅ pip ditemukan

REM Check/create virtual environment
echo.
echo [3/4] Membuat virtual environment...
if exist "venv" (
    echo ✅ Virtual environment sudah ada
) else (
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Gagal membuat virtual environment
        pause
        exit /b 1
    )
    echo ✅ Virtual environment dibuat
)

REM Activate virtual environment
echo.
echo Mengaktifkan virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo [4/4] Menginstall dependencies...
echo.

pip install --upgrade pip
if errorlevel 1 (
    echo ⚠️ Gagal upgrade pip, melanjutkan...
)

pip install openhands-sdk openhands-tools pydantic
if errorlevel 1 (
    echo.
    echo ❌ Gagal menginstall dependencies!
    echo.
    echo Pastikan koneksi internet aktif
    echo.
    pause
    exit /b 1
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    ✅ INSTALLATION COMPLETE                     ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📋 Langkah selanjutnya:
echo.
echo   1. Set API Key:
echo      set LLM_API_KEY=your-api-key-here
echo.
echo   2. Jalankan agent:
echo      run.bat
echo.
echo   Atau gunakan mode interaktif:
echo      python scheduled_concurrent_agent.py --interactive
echo.
echo.

REM Create .env file template
if not exist ".env" (
    echo # Scheduled Concurrent Agent Configuration > .env
    echo # =========================================== >> .env
    echo LLM_API_KEY=your-api-key-here >> .env
    echo LLM_MODEL=claude-sonnet-4-5-20250929 >> .env
    echo # LLM_BASE_URL=https://api.example.com/v1 >> .env
    echo. >> .env
    echo # Edit .env file dan masukkan API key Anda >> .env
    echo.
    echo 📝 File .env telah dibuat!
    echo    Buka file .env dan masukkan API key Anda
    echo.
)

pause
