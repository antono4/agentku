# 🪟 Panduan Instalasi untuk Windows

## 📋 Persyaratan Sistem

- **OS**: Windows 10 atau Windows 11
- **Python**: Version 3.9 atau lebih baru
- **Internet**: Koneksi internet untuk install dependencies
- **API Key**: LLM API key (OpenAI, Anthropic, dll)

## 🚀 Cara Instalasi (3 Langkah Mudah)

### Langkah 1: Download & Extract

1. Download project ini
2. Extract ke folder yang Anda inginkan, contoh:
   ```
   C:\Users\NamaAnda\ScheduledAgent
   ```

### Langkah 2: Jalankan Setup

1. Buka folder yang sudah diextract
2. **Klik dua kali** file `setup.bat`
3. Ikuti instruksi di layar

```
📁 ScheduledAgent/
├── setup.bat          ← Klik dua kali ini!
├── install.bat
├── run.bat
├── test.bat
└── ...
```

### Langkah 3: Masukkan API Key

Saat instalasi, Anda akan diminta memasukkan API Key:

```
Masukkan LLM API Key Anda: sk-xxxxxxxxxxxxx
```

## 🎯 Cara Menjalankan

### Metode 1: Setup Wizard (Recommended)
```
Klik dua kali: setup.bat
```

### Metode 2: Langsung Jalankan
```
Klik dua kali: run.bat
```

### Metode 3: Command Prompt
```
1. Buka Command Prompt (CMD)
2. cd C:\Users\NamaAnda\ScheduledAgent
3. run.bat
```

## 📖 Cara Penggunaan

### Mode Interaktif

Setelah menjalankan agent, Anda bisa menggunakan commands:

```
agent> add "Buat file hello.txt"
✓ Task added: abc123

agent> add "Download data dari web"
✓ Task added: def456

agent> schedule daily_backup "Backup semua file"
✓ Schedule added: ghi789

agent> status
📊 Running: True
   Active tasks: 2
   Queued tasks: 0
   Completed tasks: 1

agent> exit
```

### Commands yang Tersedia

| Command | Fungsi |
|---------|--------|
| `add <task>` | Tambahkan task baru |
| `schedule <name> <task>` | Schedule task harian |
| `status` | Lihat status agent |
| `list` | Lihat semua task aktif |
| `help` | Tampilkan bantuan |
| `exit` | Keluar dari agent |

## ⚙️ Konfigurasi

### Mengubah API Key

Edit file `.env`:

```
LLM_API_KEY=sk-xxxxxxxxxxxxx
```

### Mengubah Model

Edit file `.env`:

```
LLM_MODEL=gpt-4
```

### Mengubah Max Concurrent

Edit file `.env`:

```
MAX_CONCURRENT=5
```

## 🔧 Troubleshooting

### Error: "Python tidak ditemukan"

1. Install Python dari https://www.python.org/downloads/
2. Pastikan centang "Add Python to PATH" saat instalasi
3. Restart Command Prompt
4. Jalankan ulang `setup.bat`

### Error: "Module not found"

1. Jalankan `install.bat`
2. Atau ketik di Command Prompt:
   ```
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

### Error: "API Key tidak valid"

1. Cek file `.env`
2. Pastikan API key sesuai dengan provider
3. Periksa apakah key masih aktif

### Agent tidak berjalan

1. Buka `agent.log` untuk melihat error
2. Pastikan virtual environment aktif
3. Jalankan `test.bat` untuk troubleshooting

## 📁 Struktur Folder

```
ScheduledAgent/
├── scheduled_concurrent_agent.py   ← Main program
├── test_agent.py                  ← Test suite
├── requirements.txt               ← Python dependencies
├── setup.bat                      ← Setup wizard ⭐
├── install.bat                    ← Install dependencies
├── run.bat                        ← Jalankan agent ⭐
├── test.bat                       ← Jalankan test ⭐
├── .env                          ← Konfigurasi
├── README.md                      ← Dokumentasi
├── agent.log                      ← Log file
└── agent_workspace/              ← Workspace untuk tasks
```

## 🎓 Contoh Penggunaan

### Contoh 1: Backup Otomatis Harian

```python
from scheduled_concurrent_agent import ScheduledConcurrentAgent

agent = ScheduledConcurrentAgent()
agent.start()

# Schedule backup daily jam 2 pagi
agent.schedule_daily(
    task_name="Daily Backup",
    instruction="Backup semua file ke folder backup",
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

# Queue banyak tasks
tasks = [
    "Proses file sales_q1.csv",
    "Generate laporan keuangan",
    "Update database produk",
    "Kirim email report",
    "Backup sistem",
]

for task in tasks:
    agent.add_task(task, priority=8)

agent.wait_for_completion(timeout=600)
print("Semua task selesai!")
agent.stop()
```

### Contoh 3: Health Check Periodik

```python
from scheduled_concurrent_agent import ScheduledConcurrentAgent

agent = ScheduledConcurrentAgent()
agent.start()

# Cek server setiap 30 menit
agent.schedule_interval(
    task_name="Health Check",
    instruction="Cek apakah server berjalan normal",
    interval_seconds=1800  # 30 menit
)

agent.stop()
```

## 📊 Monitoring

### Cek Status

```bash
# Buka Command Prompt
cd C:\Users\NamaAnda\ScheduledAgent
run.bat

# Di mode interaktif:
agent> status
```

### Lihat Log

Buka file `agent.log` di folder yang sama

### Lihat Workspace

Semua file hasil task ada di folder `agent_workspace/`

## 🆘 Butuh Bantuan?

1. **Dokumentasi Lengkap**: `README.md`
2. **Panduan Cepat**: `QUICKSTART.md`
3. **Contoh**: `test_agent.py`
4. **Log Error**: `agent.log`

## 🔒 Keamanan

- ✅ API key disimpan di file `.env`
- ✅ Workspace terisolasi per task
- ✅ Log tidak mengandung data sensitif
- ✅ Virtual environment terisolasi

## ✅ Checklist Instalasi

- [ ] Python 3.9+ terinstall
- [ ] `setup.bat` sudah dijalankan
- [ ] API key sudah dimasukkan
- [ ] `run.bat` bisa dibuka
- [ ] Test sudah dijalankan
- [ ] Agent bisa menambah task

---

💡 **Tips**: Simpan folder ini di lokasi yang mudah diakses, contoh Desktop atau Documents

🎉 Selamat menggunakan Scheduled Concurrent Agent!
