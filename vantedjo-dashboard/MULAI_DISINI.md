# 🚀 MULAI DI SINI - Dashboard Prediksi Ayam Kios Vantedjo

## 👋 Selamat Datang!

Dashboard ini menampilkan **prediksi penjualan ayam untuk 14 hari ke depan** (1-14 Januari 2025) untuk Kios Vantedjo.

---

## ⚡ Quick Start (3 Langkah)

### 1️⃣ Install Dependencies
Buka Command Prompt atau PowerShell, lalu jalankan:
```bash
pip install flask flask-cors pandas
```

### 2️⃣ Jalankan Dashboard
**Cara 1 - Double click:**
```
Klik 2x file: run_dashboard.bat
```

**Cara 2 - Manual:**
```bash
python app.py
```

### 3️⃣ Buka Browser
```
http://localhost:5000
```

**SELESAI!** Dashboard sudah bisa digunakan! 🎉

---

## 📱 Akses dari HP/Tablet

1. Pastikan HP/Tablet terhubung ke WiFi yang sama dengan komputer
2. Cari IP komputer:
   ```bash
   ipconfig
   ```
3. Buka browser di HP/Tablet:
   ```
   http://[IP_KOMPUTER]:5000
   ```
   Contoh: `http://192.168.1.100:5000`

---

## 🎯 Apa yang Bisa Dilakukan?

### ✅ Lihat Prediksi 14 Hari
- Prediksi untuk Ayam Potong, Kampung, dan Tua
- Periode: 1-14 Januari 2025

### ✅ Lihat Grafik Interaktif
- Hover mouse untuk lihat detail
- Klik legend untuk hide/show kategori

### ✅ Lihat Tabel Detail
- Prediksi harian lengkap
- Total per hari

### ✅ Gunakan API
- Integrasi dengan sistem lain
- Format JSON

---

## 📚 Dokumentasi Lengkap

Butuh info lebih detail? Baca dokumentasi berikut:

| Dokumen | Untuk Apa? |
|---------|-----------|
| **[QUICK_START.md](QUICK_START.md)** | Setup cepat & troubleshooting |
| **[DASHBOARD_README.md](DASHBOARD_README.md)** | Dokumentasi lengkap |
| **[FITUR_DASHBOARD.md](FITUR_DASHBOARD.md)** | Fitur-fitur dashboard |
| **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** | Deploy ke production |
| **[DOKUMENTASI_INDEX.md](DOKUMENTASI_INDEX.md)** | Index semua dokumentasi |

---

## ❓ Troubleshooting

### Dashboard tidak bisa dibuka?
1. Pastikan Python sudah terinstall
2. Pastikan dependencies sudah terinstall
3. Pastikan port 5000 tidak digunakan aplikasi lain

### Data tidak muncul?
1. Pastikan file CSV ada di folder `notebooks/processed_for_model/`
2. Cek console browser (tekan F12) untuk error
3. Cek terminal untuk error message

### Port 5000 sudah digunakan?
Edit file `app.py` baris terakhir:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Ganti 5000 ke 8000
```

---

## 🛑 Stop Dashboard

Tekan `Ctrl + C` di terminal/command prompt

---

## 📊 Preview Dashboard

```
╔══════════════════════════════════════════════════════╗
║     🐔 Dashboard Prediksi Penjualan Ayam            ║
║              Kios Vantedjo                           ║
╚══════════════════════════════════════════════════════╝

┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│ Ayam Potong │  │ Ayam Kampung│  │  Ayam Tua   │
│    45.2     │  │    32.5     │  │    28.3     │
└─────────────┘  └─────────────┘  └─────────────┘

📈 Grafik Prediksi 14 Hari
[Interactive Line Chart]

📋 Detail Prediksi Harian
[Table dengan 14 hari prediksi]
```

Lihat preview lengkap di: [PREVIEW_DASHBOARD.txt](PREVIEW_DASHBOARD.txt)

---

## 🎓 Teknologi yang Digunakan

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Chart**: Chart.js
- **Data**: CSV Files

---

## 👥 Tim Proyek

**Proyek Data Mining - Kios Vantedjo**

- Product Manager: Cahyadi
- Data Engineer: Sabriyah
- Data Analyst: Elfa
- Modeler: Aidil
- Delivery & Ops: Rusydi

---

## 📞 Butuh Bantuan?

1. Baca [QUICK_START.md](QUICK_START.md) untuk troubleshooting
2. Baca [DOKUMENTASI_INDEX.md](DOKUMENTASI_INDEX.md) untuk navigasi
3. Lihat [SUMMARY_PROJECT.md](SUMMARY_PROJECT.md) untuk overview

---

## ✅ Checklist

Sebelum mulai, pastikan:

- [ ] Python 3.8+ terinstall
- [ ] Dependencies terinstall (`pip install flask flask-cors pandas`)
- [ ] File CSV ada di `notebooks/processed_for_model/`
- [ ] Port 5000 tidak digunakan
- [ ] Browser modern (Chrome, Firefox, Edge)

---

## 🎉 Selamat Menggunakan!

Dashboard siap digunakan untuk menampilkan prediksi penjualan ayam 14 hari ke depan!

**Jika ada pertanyaan, silakan baca dokumentasi lengkap di folder ini.**

---

**🐔 Happy Forecasting! 📈**
