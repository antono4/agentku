# 🕐 Scheduled Concurrent Agent

Agent AI yang dapat berjalan di komputer lokal, mengerjakan berbagai pekerjaan secara bersamaan (concurrent execution), dan dapat dijadwalkan (scheduled execution).

Dibangun menggunakan **OpenHands SDK** - framework untuk membangun AI agent yang dapat menulis software.

## ✨ Fitur

- **Concurrent Task Execution** - Menjalankan multiple tugas secara bersamaan
- **Scheduled Execution** - Menjadwalkan tugas dengan berbagai pola (sekali, interval, harian, mingguan)
- **Priority Queue** - Tugas dengan prioritas lebih tinggi dikerjakan lebih dulu
- **Real-time Logging** - Logging ke console dan file
- **Workspace Isolation** - Setiap task memiliki workspace sendiri
- **CLI Interface** - Antarmuka command-line interaktif
- **API-ready** - Mudah diintegrasikan dengan sistem lain

## 📋 Prerequisites

- Python 3.9+
- LLM API Key (OpenAI, Anthropic, atau provider lain yang kompatibel)

## 🚀 Instalasi

```bash
# Clone atau download agent ini
cd scheduled_concurrent_agent

# Install dependencies
pip install -r requirements.txt

# Set API key
export LLM_API_KEY="your-api-key-here"

# Atau gunakan model lain
export LLM_MODEL="claude-sonnet-4-5-20250929"
export LLM_BASE_URL="https://api.openhands.ai/v1"  # Optional
```

## 💻 Usage

### 1. Interactive CLI Mode

```bash
python scheduled_concurrent_agent.py --interactive
```

```
agent> add Buat file hello.txt berisi 'Hello World'
✓ Task added: abc123

agent> schedule daily_backup "Backup semua file penting"
✓ Schedule added: def456

agent> status
📊 Agent Status:
  Running: True
  Active tasks: 1
  Queued tasks: 0
  Completed tasks: 2
  Schedules: 1

agent> exit
```

### 2. Programmatic Usage

```python
from scheduled_concurrent_agent import ScheduledConcurrentAgent
from datetime import datetime, timedelta

# Initialize agent
agent = ScheduledConcurrentAgent(
    llm_api_key="your-api-key",
    max_concurrent=3  # Max 3 tasks concurrently
)

# Start agent
agent.start()

# Add immediate tasks with priority (1-10, higher = more important)
agent.add_task("Buat file hello.txt", priority=8)
agent.add_task("Download data dari API", priority=5)

# Schedule tasks
# 1. Run once at specific time
agent.schedule_once(
    task_name="Meeting reminder",
    instruction="Kirim email reminder meeting",
    run_at=datetime.now() + timedelta(hours=1)
)

# 2. Run at intervals (every hour)
agent.schedule_interval(
    task_name="Health check",
    instruction="Cek status server",
    interval_seconds=3600
)

# 3. Run daily at specific time (2:00 AM)
agent.schedule_daily(
    task_name="Daily backup",
    instruction="Backup database dan file",
    hour=2,
    minute=0
)

# 4. Run weekly on specific day (Friday at 5 PM)
agent.schedule_weekly(
    task_name="Weekly report",
    instruction="Generate laporan mingguan",
    weekday=4,  # 0=Monday, 4=Friday
    hour=17,
    minute=0
)

# Wait for completion
agent.wait_for_completion(timeout=300)

# Get status
print(agent.get_status())

# Stop when done
agent.stop()
```

### 3. Example with Different Task Types

```python
agent = ScheduledConcurrentAgent()
agent.start()

# File operations
agent.add_task("Buat file konfigurasi config.json dengan struktur yang sesuai")
agent.add_task("Edit file .env dan tambahkan DATABASE_URL")

# Data processing
agent.add_task("Proses file CSV dan generate laporan summary")

# Research tasks
agent.add_task("Cari informasi terbaru tentang topic X dan simpan ke research.md")

# Code tasks
agent.add_task("Generate unit tests untuk fungsi calculate_total di app.py")

# Monitoring tasks
agent.add_task("Cek apakah semua services berjalan dengan normal")

agent.stop()
```

## 📅 Scheduling Options

### Schedule Types

| Type | Description | Use Case |
|------|-------------|----------|
| `schedule_once` | Jalankan sekali di waktu tertentu | One-time reminders, immediate tasks |
| `schedule_interval` | Jalankan setiap X detik | Health checks, periodic syncs |
| `schedule_daily` | Jalankan setiap hari di jam tertentu | Daily backups, daily reports |
| `schedule_weekly` | Jalankan setiap minggu di hari & jam tertentu | Weekly summaries, maintenance |

### Cron Expression Format (Simplified)

Untuk `schedule_daily` dan `schedule_weekly`:

```
HH:MM              # Daily at specific time (e.g., "02:00" = 2 AM)
HH:MM WD           # Weekly on specific day and time (e.g., "17:00 4" = Friday 5 PM)
                   # WD: 0=Monday, 1=Tuesday, ..., 6=Sunday
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_API_KEY` | API key untuk LLM | Required |
| `LLM_MODEL` | Model yang digunakan | `claude-sonnet-4-5-20250929` |
| `LLM_BASE_URL` | Base URL untuk API (optional) | None |

### Constructor Options

```python
ScheduledConcurrentAgent(
    llm_api_key="your-key",      # Optional if LLM_API_KEY env var set
    llm_model="anthropic/claude-sonnet-4-5-20250929",
    llm_base_url=None,            # For custom API endpoints
    max_concurrent=3,             # Max parallel tasks
    workspace_base="./workspace"  # Base directory for task workspaces
)
```

## 📊 Monitoring

### Status Output

```python
status = agent.get_status()
# {
#     "running": True,
#     "max_concurrent": 3,
#     "active_tasks": 2,
#     "queued_tasks": 5,
#     "completed_tasks": 10,
#     "schedules": 3,
#     "active_task_details": [
#         {"id": "abc", "instruction": "Task...", "status": "running"},
#         ...
#     ]
# }
```

### Log File

Semua aktivitas di-log ke `agent.log`:

```
2024-01-15 10:30:00 - ScheduledConcurrentAgent - INFO - Agent started with 3 workers
2024-01-15 10:30:05 - ScheduledConcurrentAgent - INFO - Task added: abc123 - Buat file...
2024-01-15 10:30:06 - ScheduledConcurrentAgent - INFO - [abc123] Starting task...
2024-01-15 10:31:00 - ScheduledConcurrentAgent - INFO - [abc123] Task completed successfully
```

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   ScheduledConcurrentAgent                  │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────┐  │
│  │   Task      │    │  Scheduler │    │  Concurrent     │  │
│  │   Queue     │───▶│   Thread   │───▶│  Engine         │  │
│  │  (Priority) │    │  (Cron)    │    │  (Workers)      │  │
│  └─────────────┘    └─────────────┘    └────────┬────────┘  │
│                                                │           │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              OpenHands SDK                         │  │
│  │  ┌───────────┐  ┌───────────┐  ┌────────────────┐   │  │
│  │  │    LLM    │  │   Agent   │  │  Conversation  │   │  │
│  │  └───────────┘  └───────────┘  └────────────────┘   │  │
│  │  ┌─────────────────────────────────────────────┐   │  │
│  │  │              Tools                          │   │  │
│  │  │  TerminalTool │ FileEditorTool │ TaskTracker │   │  │
│  │  └─────────────────────────────────────────────┘   │  │
│  └─────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 🔧 Advanced Usage

### Custom LLM Provider

```python
# Using custom API endpoint
agent = ScheduledConcurrentAgent(
    llm_api_key="your-key",
    llm_model="gpt-4",
    llm_base_url="https://api.your-provider.com/v1"
)
```

### High Concurrency

```python
# Handle many tasks concurrently
agent = ScheduledConcurrentAgent(
    max_concurrent=10  # 10 parallel tasks
)
```

### Isolated Workspaces

Setiap task mendapatkan workspace sendiri di `./agent_workspace/task_{task_id}/`

## 📝 CLI Commands

| Command | Description |
|---------|-------------|
| `add <instruction>` | Add new task |
| `schedule <name> <instruction>` | Add daily scheduled task |
| `status` | Show agent status |
| `list` | List active tasks |
| `help` | Show help |
| `exit` | Stop and exit |

## 🎯 Best Practices

1. **Set appropriate concurrency** - Jangan terlalu tinggi untuk menghindari rate limits
2. **Use priorities** - Task penting harus punya priority lebih tinggi
3. **Set timeouts** - Gunakan `wait_for_completion(timeout=...)` untuk evitar hanging
4. **Monitor logs** - Check `agent.log` untuk debugging
5. **Cleanup workspaces** - Hapus `./agent_workspace` secara periodik

## 🐛 Troubleshooting

### "LLM_API_KEY not set"
```bash
export LLM_API_KEY="your-key"
python scheduled_concurrent_agent.py --interactive
```

### "OpenHands SDK not available"
```bash
pip install openhands-sdk openhands-tools
```

### Tasks not running
- Check if agent is started (`agent.start()`)
- Check status (`agent.get_status()`)
- Check logs (`tail -f agent.log`)

### Rate limit errors
- Kurangi `max_concurrent`
- Tambah delay antar tasks
- Gunakan exponential backoff

## 📄 License

MIT License

## 🤝 Contributing

Silakan buat issue atau pull request jika menemukan bugs atau ingin menambahkan fitur.

## 📚 Resources

- [OpenHands SDK Documentation](https://docs.openhands.dev/sdk)
- [OpenHands GitHub](https://github.com/OpenHands/software-agent-sdk)
- [Model Context Protocol](https://docs.openhands.dev/overview/model-context-protocol)
