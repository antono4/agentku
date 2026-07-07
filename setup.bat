@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║        SCHEDULED CONCURRENT AGENT - Setup Wizard              ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Get current directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

REM Step 1: Install dependencies
echo [STEP 1] Install Dependencies
echo ════════════════════════════════════════════════════════════════
echo.

call install.bat
if errorlevel 1 (
    echo.
    echo ❌ Installation gagal!
    pause
    exit /b 1
)

REM Step 2: Configure API Key
echo.
echo [STEP 2] Konfigurasi API Key
echo ════════════════════════════════════════════════════════════════
echo.

set API_KEY=
set /p API_KEY="Masukkan LLM API Key Anda: "

if "%API_KEY%"=="" (
    echo.
    echo ⚠️  Anda tidak memasukkan API Key
    echo.
    echo Anda bisa:
    echo   1. Edit file .env manualmente
    echo   2. Set variabel environment nanti
    echo.
) else (
    REM Update .env file
    (
        echo # Scheduled Concurrent Agent Configuration
        echo # ===========================================
        echo LLM_API_KEY=%API_KEY%
        echo LLM_MODEL=claude-sonnet-4-5-20250929
        echo MAX_CONCURRENT=3
        echo # LLM_BASE_URL=https://api.example.com/v1
    ) > .env
    
    echo ✅ API Key berhasil disimpan ke .env
)

REM Step 3: Create shortcuts
echo.
echo [STEP 3] Membuat Shortcuts
echo ════════════════════════════════════════════════════════════════
echo.

REM Create desktop shortcut (PowerShell)
powershell -Command "
$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut('Desktop\Scheduled Agent.lnk')
$Shortcut.TargetPath = '%USERPROFILE%\AppData\Local\Programs\Python\Python*\python.exe'
$Shortcut.Arguments = 'scheduled_concurrent_agent.py --interactive'
$Shortcut.WorkingDirectory = '%SCRIPT_DIR%'
$Shortcut.Description = 'Scheduled Concurrent Agent'
$Shortcut.Save()
"

if errorlevel 1 (
    echo ⚠️  Gagal membuat desktop shortcut
    echo    Anda bisa menjalankan manual dengan: run.bat
)

REM Step 4: Test run
echo.
echo [STEP 4] Test Run
echo ════════════════════════════════════════════════════════════════
echo.

echo ℹ️  Apakah Anda ingin menjalankan test untuk memastikan semua bekerja?
echo.

set /p test_choice="Jalankan test? (y/n): "

if /i "%test_choice%"=="y" (
    call venv\Scripts\activate.bat
    python test_agent.py
)

REM Final message
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                      ✅ SETUP COMPLETE                       ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 🎉 Scheduled Concurrent Agent siap digunakan!
echo.
echo 📋 Cara penggunaan:
echo.
echo   1. Jalankan agent:
echo      run.bat
echo.
echo   2. Mode interaktif:
echo      python scheduled_concurrent_agent.py --interactive
echo.
echo   3. Lihat dokumentasi:
echo      README.md
echo.
echo   4. Panduan cepat:
echo      QUICKSTART.md
echo.
echo.

REM Ask to start agent
set /p start_choice="Mulai jalankan agent sekarang? (y/n): "

if /i "%start_choice%"=="y" (
    call run.bat --interactive
)

endlocal
