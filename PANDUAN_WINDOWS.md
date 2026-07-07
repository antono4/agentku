# 🪟 File Batch untuk Windows - Panduan Lengkap

File-file `.bat` ini memudahkan Anda menginstall dan menjalankan **Scheduled Concurrent Agent** di Windows tanpa perlu mengetik command di Command Prompt.

---

## 🚀 CARA PAKAI (3 Langkah Super Mudah)

### Langkah 1: Download & Extract
```
1. Download project ini
2. Extract ke folder yang Anda mau
   Contoh: C:\Users\NamaAnda\ScheduledAgent
```

### Langkah 2: Setup
```
→ Klik 2x file: setup.bat
→ Masukkan API Key Anda saat diminta
→ Tunggu sampai selesai
```

### Langkah 3: Jalankan
```
→ Klik 2x file: START.bat
→ Agent langsung jalan!
```

---

## 📁 Daftar File Batch

| File | Fungsi | Kapan Dipakai |
|------|--------|---------------|
| `setup.bat` | ⚡ Setup lengkap | Pertama kali install |
| `START.bat` | 🚀 Jalankan cepat | Setiap mau jalanin agent |
| `run.bat` | 📋 Menu interaktif | Mau pilih-pilih mode |
| `quick_schedule.bat` | ⏰ Tambah schedule cepat | Tambah scheduled task |
| `test.bat` | 🧪 Test agent | Testing agent works |
| `install.bat` | 📦 Install ulang | Install dependencies |
| `update.bat` | 🔄 Update agent | Update ke versi terbaru |
| `uninstall.bat` | 🗑️ Hapus agent | Uninstall semuanya |

---

## 💻 Panduan Pemula

### Ingin Install dari Nol?
```
Klik: setup.bat
```

### Ingin Jalankan Agent?
```
Klik: START.bat
```

### Ingin Tambah Scheduled Task?
```
Klik: quick_schedule.bat
```

### Ingin Test Agent?
```
Klik: test.bat
```

---

## ⚡ Quick Reference

### Command di Mode Interaktif

```bash
agent> add "Task baru"
✓ Task added!

agent> schedule daily_backup "Backup data"
✓ Schedule added!

agent> status
📊 Running: True...

agent> exit
```

### Schedule Types

```
quick_schedule.bat akan tanya:

[1] Daily      - Setiap hari jam tertentu
[2] Interval   - Setiap X detik
[3] Weekly     - Setiap minggu di hari tertentu
[4] Once       - Jalankan sekali
```

---

## 🔧 Troubleshooting

### Error: "Python tidak ditemukan"
```
1. Install Python dari: https://www.python.org/downloads/
2. Centang "Add Python to PATH" saat install
3. Jalankan setup.bat lagi
```

### Error: "Module not found"
```
→ Jalankan: install.bat
→ Atau: setup.bat
```

### Ingin Ganti API Key?
```
1. Edit file: .env
2. Ganti baris: LLM_API_KEY=key-baru-anda
3. Save
```

### Ingin Cek Log?
```
→ Buka file: agent.log
```

---

## 📚 Dokumentasi Lainnya

| File | Isi |
|------|-----|
| `INSTALL_WINDOWS.md` | Panduan instalasi lengkap |
| `WINDOWS_GUIDE.txt` | Panduan super singkat |
| `README.md` | Dokumentasi utama |
| `QUICKSTART.md` | Panduan cepat 5 menit |
| `BATCH_FILES_GUIDE.md` | Guide lengkap untuk semua batch file |

---

## 💡 Tips

1. **Simpan di tempat mudah**
   - Desktop atau Documents
   - Jangan di folder yang dalam

2. **Buat Shortcut**
   - Klik kanan `START.bat`
   - Pilih "Create shortcut"
   - Taruh di Desktop

3. **Backup API Key**
   - API key ada di file `.env`
   - Jangan share ke orang lain

4. **Regular Testing**
   - Jalankan `test.bat` secara berkala
   - Pastikan agent masih work

---

## 🎯 Use Cases

### Data Processing
```batch
setup.bat → jalankan
→ add "Proses data sales"
→ add "Generate laporan"
→ schedule daily "Process data", jam 3 pagi
```

### Automation
```batch
quick_schedule.bat
→ [1] Daily
→ Backup Database
→ Backup semua data penting
→ Jam: 2, Menit: 0
```

### Monitoring
```batch
quick_schedule.bat
→ [2] Interval
→ Health Check
→ Cek status server
→ Interval: 1800 (30 menit)
```

---

## 🔐 Keamanan

- ✅ API key tersimpan di file `.env`
- ✅ Virtual environment terisolasi
- ✅ Tidak install ke system
- ✅ Mudah di-uninstall

---

## 📞 Help

### Butuh Bantuan?
1. Buka `INSTALL_WINDOWS.md` untuk panduan lengkap
2. Cek `agent.log` untuk error details
3. Jalankan `test.bat` untuk troubleshooting

### Error Report?
- Buka file `agent.log`
- Cari baris yang mengandung "ERROR"
- Screenshoot atau copy error message-nya

---

## 🎉 Selesai!

Sekarang Anda sudah punya:
- ✅ Agent yang bisa jalan concurrent
- ✅ Scheduling system
- ✅ 8 file batch untuk kemudahan
- ✅ Dokumentasi lengkap

**Selamat mengautomasi! 🚀**

---

*💡 Tip: Baca file WINDOWS_GUIDE.txt untuk panduan super singkat!*
