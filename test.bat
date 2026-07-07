@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║        SCHEDULED CONCURRENT AGENT - Test Suite               ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment tidak ditemukan!
    echo.
    echo Jalankan setup.bat atau install.bat terlebih dahulu
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

echo 🚀 Menjalankan test suite...
echo.

REM Run tests
python test_agent.py

echo.
echo ════════════════════════════════════════════════════════════════
echo.

if errorlevel 1 (
    echo ❌ Ada test yang gagal!
    echo.
    echo 💡 Tips troubleshooting:
    echo    - Pastikan semua dependencies terinstall
    echo    - Cek file agent.log untuk error details
    echo    - Pastikan LLM_API_KEY sudah diset
    echo.
) else (
    echo ✅ Semua test berhasil!
    echo.
    echo 🎉 Agent siap digunakan!
)

echo.
pause
