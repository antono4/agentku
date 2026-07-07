# 🪟 File Batch untuk Windows

File-file batch (.bat) ini memudahkan Anda menginstall dan menjalankan agent di PC Windows tanpa perlu mengetik command di Command Prompt.

## 📋 Daftar File Batch

### 🚀 File Utama (Yang Paling Sering Dipakai)

#### 1. `setup.bat` ⭐ (Paling Penting!)
**Fungsi**: Setup pertama kali - install semua dependencies dan konfigurasi

**Cara Pakai**:
```batch
Klik 2x setup.bat
```

**Yang dilakukan**:
- ✅ Install Python dependencies
- ✅ Buat virtual environment
- ✅ Minta API Key
- ✅ Buat file konfigurasi
- ✅ Test apakah semua bekerja

**Kapan dipakai**: Hanya sekali saat pertama kali install

---

#### 2. `START.bat` ⚡ (Jalankan Cepat)
**Fungsi**: Langsung jalankan agent tanpa menu

**Cara Pakai**:
```batch
Klik 2x START.bat
```

**Yang dilakukan**:
- ✅ Aktifkan virtual environment
- ✅ Load konfigurasi
- ✅ Jalankan agent di mode interaktif

**Kapan dipakai**: Setiap kali mau jalankan agent dengan cepat

---

#### 3. `run.bat` 📋 (Dengan Menu)
**Fungsi**: Jalankan agent dengan pilihan menu

**Cara Pakai**:
```batch
Klik 2x run.bat
```

**Menu yang muncul**:
```
[1] Mode Interaktif     - CLI interaktif
[2] Contoh Usage         - Tampilkan contoh
[3] Test                - Jalankan test
[4] Status              - Cek status
[5] Custom Command       - Command kustom
[6] Keluar
```

**Kapan dipakai**: Kalau mau pilih-pilih mode

---

### 📦 File Pendukung

#### 4. `install.bat`
**Fungsi**: Install dependencies saja (tanpa setup lengkap)

**Cara Pakai**:
```batch
Klik 2x install.bat
```

**Yang dilakukan**:
- ✅ Cek Python
- ✅ Buat virtual environment
- ✅ Install openhands-sdk
- ✅ Install dependencies

**Kapan dipakai**: Kalau mau install ulang dependencies

---

#### 5. `test.bat` 🧪
**Fungsi**: Jalankan test suite

**Cara Pakai**:
```batch
Klik 2x test.bat
```

**Yang dilakukan**:
- ✅ Aktifkan virtual environment
- ✅ Jalankan `test_agent.py`
- ✅ Tampilkan hasil test

**Kapan dipakai**: Untuk memastikan agent bekerja dengan benar

---

#### 6. `quick_schedule.bat` ⏰
**Fungsi**: Tambahkan scheduled task dengan cepat

**Cara Pakai**:
```batch
Klik 2x quick_schedule.bat
```

**Yang dilakukan**:
- ✅ Tampilkan menu pilihan schedule type
- ✅ Minta input task name & instruction
- ✅ Buat scheduled task

**Kapan dipakai**: Untuk cepat-cepat add scheduled task

---

#### 7. `update.bat` 🔄
**Fungsi**: Update agent ke versi terbaru

**Cara Pakai**:
```batch
Klik 2x update.bat
```

**Yang dilakukan**:
- ✅ Update pip
- ✅ Update openhands-sdk
- ✅ Update dependencies

**Kapan dipakai**: Untuk update ke versi terbaru

---

#### 8. `uninstall.bat` 🗑️
**Fungsi**: Hapus semua file instalasi

**Cara Pakai**:
```batch
Klik 2x uninstall.bat
```

**Yang dilakukan**:
- ✅ Hapus virtual environment
- ✅ Hapus .env
- ✅ Hapus agent.log
- ✅ Hapus agent_workspace
- ✅ Hapus desktop shortcut

**Kapan dipakai**: Kalau mau uninstall agent

---

## 📖 Panduan Pemula

### Langkah 1: Pertama Kali Install

```
1. Klik 2x → setup.bat
2. Masukkan API Key saat diminta
3. Tunggu sampai selesai
4. Selesai!
```

### Langkah 2: Jalankan Agent

```
Pilih salah satu:
• Klik 2x → START.bat          (Tercepat!)
• Klik 2x → run.bat            (Ada menu)
• Klik 2x → setup.bat          (Setup ulang)
```

### Langkah 3: Pakai Mode Interaktif

```
agent> add "Buat file hello.txt"
✓ Task added!

agent> schedule backup "Backup data"
✓ Schedule added!

agent> status
📊 Running: True...

agent> exit
```

---

## 🎯 Use Case Specific

### Ingin...?
#### ...Jalankan agent dengan cepat?
→ `START.bat`

#### ...Tambah scheduled task?
→ `quick_schedule.bat`

#### ...Test apakah agent works?
→ `test.bat`

#### ...Update ke versi terbaru?
→ `update.bat`

#### ...Setup ulang dari awal?
→ `setup.bat`

#### ...Hapus agent?
→ `uninstall.bat`

---

## 💡 Tips

1. **Simpan di tempat mudah**
   - Desktop atau Documents
   - Jangan di folder yang dalam/rumit

2. **Buat Shortcut**
   - Klik kanan `START.bat`
   - Pilih "Create shortcut"
   - Taruh di Desktop

3. **API Key**
   - Disimpan di file `.env`
   - Jangan share ke orang lain

4. **Error?**
   - Buka `agent.log`
   - Jalankan `test.bat`
   - Atau jalankan `setup.bat` lagi

---

## 🔧 Troubleshooting

### Error: "Python tidak ditemukan"
```batch
→ Install Python dari python.org
→ Centang "Add to PATH" saat install
→ Jalankan setup.bat lagi
```

### Error: "Module not found"
```batch
→ Jalankan install.bat
→ Atau: setup.bat
```

### Error: "API Key invalid"
```batch
→ Edit file .env
→ Pastikan API key benar
```

### Batch file tidak bisa diklik 2x?
```batch
→ Klik kanan file .bat
→ Pilih "Open with" → "Command Prompt"
→ Atau drag file ke Command Prompt
```

---

## 📂 Struktur Folder Setelah Install

```
ScheduledAgent/
│
├── 🟢 File Batch (Klik untuk jalan)
│   ├── setup.bat              ← Setup pertama kali
│   ├── START.bat              ← Jalankan cepat
│   ├── run.bat                ← Menu interaktif
│   ├── quick_schedule.bat     ← Tambah schedule
│   ├── test.bat               ← Test agent
│   ├── install.bat            ← Install ulang
│   ├── update.bat             ← Update agent
│   └── uninstall.bat          ← Hapus agent
│
├── 🔵 Python Files
│   ├── scheduled_concurrent_agent.py
│   └── test_agent.py
│
├── 📄 Dokumentasi
│   ├── README.md
│   ├── INSTALL_WINDOWS.md
│   ├── QUICKSTART.md
│   ├── BATCH_FILES_GUIDE.md   ← (file ini)
│   └── WINDOWS_GUIDE.txt
│
├── 🟡 Config & Logs
│   ├── .env                   ← Konfigurasi (setelah install)
│   ├── agent.log              ← Log file
│   └── requirements.txt
│
└── 🟠 Lainnya
    ├── Dockerfile
    ├── docker-compose.yml
    └── venv/                  ← Virtual environment
```

---

## 🎓 Contoh Penggunaan

### Contoh 1: Setup dari Nol

```batch
1. Klik setup.bat
2. Masukkan API Key: sk-xxxxx
3. Tunggu sampai selesai
4. Klik START.bat
5. Done!
```

### Contoh 2: Tambah Scheduled Task

```batch
1. Klik quick_schedule.bat
2. Pilih [1] Daily
3. Nama: Daily Backup
4. Instruction: Backup semua file
5. Jam: 2, Menit: 0
6. Selesai!
```

### Contoh 3: Test Agent

```batch
1. Klik test.bat
2. Lihat hasil
3. Semua ✅ = agent work!
```

---

## 🔐 Keamanan

- ✅ API key di file `.env` (tidak di batch file)
- ✅ Virtual environment terisolasi
- ✅ Tidak install system-wide
- ✅ Mudah di-uninstall

---

## 📞 Butuh Bantuan?

1. **Error Installation** → `setup.bat` lagi
2. **Error Runtime** → Cek `agent.log`
3. **Tidak jalan** → `test.bat`
4. **Update** → `update.bat`

---

💡 **Tip**: Baca `WINDOWS_GUIDE.txt` untuk panduan super singkat!

🎉 Happy automating!
