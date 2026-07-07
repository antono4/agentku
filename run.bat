@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║           SCHEDULED CONCURRENT AGENT - Runner                  ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment tidak ditemukan!
    echo.
    echo Jalankan install.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Load .env file if exists
if exist ".env" (
    echo 📄 Memuat konfigurasi dari .env...
    for /f "usebackq tokens=1,* delims==" %%a in (`findstr /v "^#" .env`) do (
        set "%%a=%%b"
    )
    echo ✅ Konfigurasi dimuat
)

REM Check if LLM_API_KEY is set
if "%LLM_API_KEY%"=="" (
    echo.
    echo ⚠️  Warning: LLM_API_KEY belum diset!
    echo.
    echo Pastikan Anda sudah:
    echo   1. Mengisi API key di file .env, atau
    echo   2. Set variabel environment:
    echo      set LLM_API_KEY=your-api-key-here
    echo.
    echo ℹ️  Tanpa API key, agent akan berjalan dalam simulation mode
    echo.
    powershell -Command "$result = Read-Host 'Lanjutkan tanpa API key? (y/n)'; if($result -ne 'y') { exit 1 }"
)

echo.
echo 🚀 Menjalankan Scheduled Concurrent Agent...
echo.

REM Show configuration
echo 📋 Konfigurasi:
echo    Max Concurrent: %MAX_CONCURRENT%=3
echo    LLM Model: %LLM_MODEL%=claude-sonnet-4-5-20250929
echo.

REM Parse command line arguments
if "%~1"=="" (
    REM No arguments - show menu
    goto :menu
) else if "%~1"=="--interactive" (
    python scheduled_concurrent_agent.py --interactive
) else if "%~1"=="--example" (
    python scheduled_concurrent_agent.py --example
) else (
    python scheduled_concurrent_agent.py %*
)

goto :end

:menu
echo ════════════════════════════════════════════════════════════════
echo.
echo    Pilih mode运行:
echo.
echo    [1] Mode Interaktif     - Jalankan dengan antarmuka CLI
echo    [2] Contoh Usage         - Tampilkan contoh penggunaan
echo    [3] Test                 - Jalankan test suite
echo    [4] Status               - Cek status agent
echo    [5] Custom Command       - Jalankan dengan argumen kustom
echo    [6] Keluar
echo.
echo ════════════════════════════════════════════════════════════════
echo.

set /p choice="Pilih menu (1-6): "

if "%choice%"=="1" goto :interactive
if "%choice%"=="2" goto :example
if "%choice%"=="3" goto :test
if "%choice%"=="4" goto :status
if "%choice%"=="5" goto :custom
if "%choice%"=="6" goto :end

echo.
echo ❌ Pilihan tidak valid!
goto :menu

:interactive
echo.
echo 🚀 Memulai mode interaktif...
echo.
python scheduled_concurrent_agent.py --interactive
goto :end

:example
echo.
echo 📚 Menampilkan contoh penggunaan...
echo.
python scheduled_concurrent_agent.py --example
goto :end

:test
echo.
echo 🧪 Menjalankan test suite...
echo.
python test_agent.py
goto :end

:status
echo.
echo 📊 Status Agent...
echo.
echo ℹ️  Jalankan agent dulu untuk melihat status akt
echo    python scheduled_concurrent_agent.py --interactive
echo.
echo Tekan tombol apa saja untuk kembali...
pause >nul
goto :end

:custom
echo.
set /p args="Masukkan argumen: "
echo.
python scheduled_concurrent_agent.py %args%
goto :end

:end
echo.
pause
