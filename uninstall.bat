@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║        SCHEDULED CONCURRENT AGENT - Uninstaller              ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo ⚠️  Peringatan: Proses ini akan menghapus:
echo.
echo    - Virtual environment (venv)
echo    - File konfigurasi (.env)
echo    - Log files (agent.log)
echo    - Workspace files (agent_workspace)
echo.
echo    File source code akan tetap ada
echo.

set /p confirm="Apakah Anda yakin ingin uninstall? (y/n): "

if /i not "%confirm%"=="y" (
    echo.
    echo Uninstall dibatalkan.
    pause
    exit /b 0
)

echo.
echo 🗑️  Menghapus files...
echo.

REM Remove virtual environment
if exist "venv" (
    rmdir /s /q venv
    echo ✅ Virtual environment dihapus
)

REM Remove config files
if exist ".env" (
    del /q ".env"
    echo ✅ Konfigurasi dihapus
)

REM Remove log files
if exist "agent.log" (
    del /q "agent.log"
    echo ✅ Log files dihapus
)

REM Remove workspace
if exist "agent_workspace" (
    rmdir /s /q agent_workspace
    echo ✅ Workspace dihapus
)

REM Remove desktop shortcut if exists
if exist "%USERPROFILE%\Desktop\Scheduled Agent.lnk" (
    del /q "%USERPROFILE%\Desktop\Scheduled Agent.lnk"
    echo ✅ Desktop shortcut dihapus
)

REM Remove pycache
if exist "__pycache__" (
    rmdir /s /q __pycache__
    echo ✅ Cache dihapus
)

REM Remove egg-info
for /d %%i in (*.egg-info) do (
    rmdir /s /q "%%i"
    echo ✅ %%i dihapus
)

echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║                    ✅ UNINSTALL COMPLETE                      ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.
echo 📝 Catatan:
echo    - File source code masih ada
echo    - Untuk instalasi ulang, jalankan setup.bat
echo.
pause
