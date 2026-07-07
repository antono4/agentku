@echo off
chcp 65001 >nul
echo.
echo ╔═══════════════════════════════════════════════════════════════╗
echo ║     QUICK SCHEDULE - Tambahkan Task dengan Cepat              ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

REM Activate virtual environment
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Load .env if exists
if exist ".env" (
    for /f "usebackq tokens=1,* delims==" %%a in (`findstr /v "^#" .env`) do (
        set "%%a=%%b"
    )
)

echo ℹ️  Pilihan Schedule Type:
echo.
echo   [1] Daily      - Setiap hari jam tertentu
echo   [2] Interval   - Setiap X detik
echo   [3] Weekly     - Setiap minggu di hari tertentu
echo   [4] Once       - Jalankan sekali di waktu tertentu
echo.
echo.

set /p sched_type="Pilih tipe schedule (1-4): "

if "%sched_type%"=="1" goto :daily
if "%sched_type%"=="2" goto :interval
if "%sched_type%"=="3" goto :weekly
if "%sched_type%"=="4" goto :once

echo.
echo ❌ Pilihan tidak valid!
goto :end

:daily
echo.
set /p task_name="Nama task: "
set /p task_instr="Instruction: "
set /p hour="Jam (0-23): "
set /p minute="Menit (0-59): "

echo.
echo 📝 Membuat scheduled task...
echo.

python -c "
from scheduled_concurrent_agent import ScheduledConcurrentAgent
from datetime import datetime

agent = ScheduledConcurrentAgent()
agent.start()

agent.schedule_daily(
    task_name='%task_name%',
    instruction='%task_instr%',
    hour=int('%hour%'),
    minute=int('%minute%')
)

print('✅ Task scheduled!')
agent.stop()
"
goto :end

:interval
echo.
set /p task_name="Nama task: "
set /p task_instr="Instruction: "
set /p seconds="Interval (detik): "

echo.
echo 📝 Membuat interval task...
echo.

python -c "
from scheduled_concurrent_agent import ScheduledConcurrentAgent

agent = ScheduledConcurrentAgent()
agent.start()

agent.schedule_interval(
    task_name='%task_name%',
    instruction='%task_instr%',
    interval_seconds=int('%seconds%')
)

print('✅ Task scheduled!')
agent.stop()
"
goto :end

:weekly
echo.
set /p task_name="Nama task: "
set /p task_instr="Instruction: "
echo.
echo 📅 Hari: 0=Senin, 1=Selasa, 2=Rabu, 3=Kamis, 4=Jumat, 5=Sabtu, 6=Minggu
set /p weekday="Hari (0-6): "
set /p hour="Jam (0-23): "
set /p minute="Menit (0-59): "

echo.
echo 📝 Membuat weekly task...
echo.

python -c "
from scheduled_concurrent_agent import ScheduledConcurrentAgent

agent = ScheduledConcurrentAgent()
agent.start()

agent.schedule_weekly(
    task_name='%task_name%',
    instruction='%task_instr%',
    weekday=int('%weekday%'),
    hour=int('%hour%'),
    minute=int('%minute%')
)

print('✅ Task scheduled!')
agent.stop()
"
goto :end

:once
echo.
set /p task_name="Nama task: "
set /p task_instr="Instruction: "
set /p hour="Jam (0-23): "
set /p minute="Menit (0-59): "

echo.
echo 📝 Membuat one-time task...
echo.

python -c "
from scheduled_concurrent_agent import ScheduledConcurrentAgent
from datetime import datetime, timedelta

run_time = datetime.now() + timedelta(hours=int('%hour%'), minutes=int('%minute%'))

agent = ScheduledConcurrentAgent()
agent.start()

agent.schedule_once(
    task_name='%task_name%',
    instruction='%task_instr%',
    run_at=run_time,
    max_runs=1
)

print('✅ Task scheduled!')
agent.stop()
"

:end
echo.
echo.
echo Tekan tombol apa saja untuk keluar...
pause >nul
