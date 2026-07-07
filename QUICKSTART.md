# 🚀 Quick Start Guide

## 5 Menit Pertama dengan Scheduled Concurrent Agent

### Langkah 1: Install

```bash
cd /workspace/output
pip install -r requirements.txt
```

### Langkah 2: Set API Key

```bash
export LLM_API_KEY="your-api-key-here"
```

### Langkah 3: Jalankan (Mode Interaktif)

```bash
python scheduled_concurrent_agent.py --interactive
```

Atau gunakan script yang sudah siap:

```bash
./run.sh
```

### Langkah 4: Coba Commands Dasar

```
agent> add Buat file hello.txt berisi 'Hello World'
✓ Task added: abc12345

agent> add Download data dari internet
✓ Task added: def67890

agent> status
📊 Agent Status:
  Running: True
  Active tasks: 1
  Queued tasks: 1
  Completed tasks: 0
  Schedules: 0

agent> exit
```

## 📝 Contoh Penggunaan Cepat

### Contoh 1: Backup Otomatis Harian

```python
from scheduled_concurrent_agent import ScheduledConcurrentAgent

agent = ScheduledConcurrentAgent()
agent.start()

# Schedule backup daily at 2 AM
agent.schedule_daily(
    task_name="Daily Backup",
    instruction="Backup semua file database ke folder backup",
    hour=2,
    minute=0
)

print("Backup scheduler aktif!")
agent.stop()
```

### Contoh 2: Multi-Task Processing

```python
from scheduled_concurrent_agent import ScheduledConcurrentAgent

agent = ScheduledConcurrentAgent(max_concurrent=5)
agent.start()

# Queue many tasks
tasks = [
    "Proses file sales_q1.csv",
    "Generate laporan keuangan",
    "Update database produk",
    "Kirim email report",
    "Backup sistem",
]

for task in tasks:
    agent.add_task(task, priority=8 if "report" in task else 5)

# Wait for all to complete
agent.wait_for_completion(timeout=600)
print(f"✅ {len(tasks)} tasks completed!")

agent.stop()
```

### Contoh 3: Scheduled Report

```python
from scheduled_concurrent_agent import ScheduledConcurrentAgent
from datetime import datetime, timedelta

agent = ScheduledConcurrentAgent()
agent.start()

# Schedule one-time task for tomorrow
tomorrow = datetime.now() + timedelta(days=1)
tomorrow = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)

agent.schedule_once(
    task_name="Weekly Report",
    instruction="Generate dan kirim weekly report ke email team",
    run_at=tomorrow,
    max_runs=1
)

print("Report scheduled untuk besok jam 9!")
agent.stop()
```

## 🎯 Tips Cepat

### 1. Priority Jobs
Tugas dengan priority lebih tinggi (1-10) dikerjakan lebih dulu:

```python
agent.add_task("URGENT: Fix bug", priority=10)  # Dikerjakan duluan
agent.add_task("Regular task", priority=5)
```

### 2. Monitor Status
Cek status kapan saja:

```python
status = agent.get_status()
print(f"Active: {status['active_tasks']}, "
      f"Queued: {status['queued_tasks']}, "
      f"Done: {status['completed_tasks']}")
```

### 3. Handle Errors
Gunakan try-except untuk graceful shutdown:

```python
try:
    agent.start()
    # ... your logic
except KeyboardInterrupt:
    print("Shutting down...")
finally:
    agent.stop()
```

## 🔧 Troubleshooting Cepat

### Error: "LLM_API_KEY not set"
```bash
export LLM_API_KEY="your-key"
```

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Agent tidak merespond
- Cek apakah `agent.start()` sudah dipanggil
- Cek logs: `tail -f agent.log`

## 📊 Default Configuration

- **Max Concurrent Tasks**: 3
- **LLM Model**: claude-sonnet-4-5-20250929
- **Workspace**: ./agent_workspace
- **Log File**: agent.log

## 🐳 Docker Quick Start

```bash
# Build
docker build -t scheduled-agent .

# Run
docker-compose up
```

## ✅ Checklist

- [ ] Install dependencies (`pip install -r requirements.txt`)
- [ ] Set API key (`export LLM_API_KEY=...`)
- [ ] Run interactive mode (`python scheduled_concurrent_agent.py --interactive`)
- [ ] Add a task (`add "Buat file test.txt"`)
- [ ] Check status (`status`)
- [ ] Schedule a task (`schedule daily_task "Task harian"`)
- [ ] Stop agent (`exit`)

---

💡 **Need help?** Cek README.md untuk dokumentasi lengkap atau buat issue di GitHub.
