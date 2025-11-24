# 📖 Cara Menjalankan Dashboard Prediksi Penjualan Ayam

## 🎯 Ringkasan Singkat

Dashboard ini menampilkan **prediksi penjualan ayam untuk 14 hari ke depan** (1-14 Januari 2025) untuk 3 kategori: Ayam Potong, Ayam Kampung, dan Ayam Tua.

---

## ⚡ Langkah Cepat (Quick Start)

### 1. Install Dependencies
Buka Command Prompt atau PowerShell, lalu jalankan:
```bash
pip install flask flask-cors pandas statsmodels
```

Atau install semua dependencies sekaligus:
```bash
pip install -r requirements.txt
```

### 2. Jalankan Server
Ada 2 cara:

**Cara 1 - Double Click (Termudah):**
```
Klik 2x file: run_dashboard.bat
```

**Cara 2 - Manual:**
```bash
python app.py
```

### 3. Buka Dashboard
Buka browser (Chrome/Firefox/Edge) dan akses:
```
http://localhost:5000
```

**SELESAI!** Dashboard sudah bisa digunakan! 🎉

---

## 📁 File-File Penting

### File Aplikasi
- **`app.py`** - Backend server (Flask API)
- **`templates/index.html`** - Halaman dashboard
- **`static/style.css`** - Styling dashboard
- **`static/script.js`** - Logic JavaScript

### File Data
- **`notebooks/processed_for_model/ts_ayam_potong_clean.csv`** - Data Ayam Potong
- **`notebooks/processed_for_model/ts_ayam_kampung_clean.csv`** - Data Ayam Kampung
- **`notebooks/processed_for_model/ts_ayam_tua_clean.csv`** - Data Ayam Tua

### File Helper
- **`run_dashboard.bat`** - Script untuk menjalankan server (Windows)
- **`test_api.py`** - Script untuk testing API

---

## 🌐 Akses Dashboard

### Dari Komputer yang Sama
```
http://localhost:5000
atau
http://127.0.0.1:5000
```

### Dari HP/Tablet/Komputer Lain (WiFi yang Sama)

1. **Cari IP komputer:**
   ```bash
   ipconfig
   ```
   Cari bagian "IPv4 Address", contoh: `192.168.1.5`

2. **Akses dari device lain:**
   ```
   http://192.168.1.5:5000
   ```
   (Ganti `192.168.1.5` dengan IP komputer Anda)

---

## 🎨 Fitur Dashboard

### ✅ Yang Bisa Dilakukan:

1. **Lihat Prediksi 14 Hari**
   - Periode: 1-14 Januari 2025
   - 3 kategori: Ayam Potong, Kampung, Tua
   - Satuan: kilogram (kg)

2. **Statistik Ringkasan**
   - Card untuk setiap kategori
   - Menampilkan rata-rata prediksi per hari

3. **Grafik Interaktif**
   - Line chart dengan Chart.js
   - Hover mouse untuk lihat detail
   - Klik legend untuk hide/show kategori

4. **Tabel Detail**
   - Prediksi harian lengkap
   - Total per hari
   - 14 baris data

5. **REST API**
   - `/api/predictions` - Prediksi 14 hari
   - `/api/historical` - Data historis
   - `/api/stats` - Statistik ringkasan

---

## 🛑 Cara Menghentikan Server

Tekan **`Ctrl + C`** di terminal/command prompt

---

## 🧪 Testing API

Untuk test apakah API berjalan dengan baik:

```bash
python test_api.py
```

Script ini akan test 3 endpoint:
- `/api/predictions`
- `/api/historical`
- `/api/stats`

---

## ❓ Troubleshooting

### 1. Dashboard tidak bisa dibuka?

**Cek:**
- ✅ Python sudah terinstall? Coba: `python --version`
- ✅ Dependencies sudah terinstall? Jalankan: `pip install flask flask-cors pandas`
- ✅ Server sudah jalan? Lihat terminal, harus ada tulisan "Running on http://127.0.0.1:5000"
- ✅ Port 5000 tidak digunakan aplikasi lain?

**Solusi:**
Jika port 5000 sudah digunakan, edit `app.py` baris terakhir:
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Ganti 5000 ke 8000
```

### 2. Data tidak muncul di dashboard?

**Cek:**
- ✅ File CSV ada di folder `notebooks/processed_for_model/`?
- ✅ Ada 3 file: `ts_ayam_potong_clean.csv`, `ts_ayam_kampung_clean.csv`, `ts_ayam_tua_clean.csv`?

**Solusi:**
- Pastikan file CSV ada dan tidak corrupt
- Cek console browser (tekan F12) untuk error
- Cek terminal server untuk error message

### 3. Error "Module not found"?

**Solusi:**
```bash
pip install -r requirements.txt
```

### 4. Browser menampilkan error 404?

**Cek:**
- ✅ URL benar? Harus: `http://localhost:5000` (bukan `http://localhost:5000/index.html`)
- ✅ Server masih jalan?

### 5. Grafik tidak muncul?

**Cek:**
- ✅ Koneksi internet? (Chart.js dimuat dari CDN)
- ✅ Browser modern? (Chrome, Firefox, Edge terbaru)

---

## 📊 Struktur Project

```
vantedjo-web/
│
├── app.py                          # Backend Flask API
├── templates/
│   └── index.html                  # Frontend Dashboard
├── static/
│   ├── style.css                   # Styling
│   └── script.js                   # JavaScript Logic
├── notebooks/processed_for_model/  # Data CSV
│   ├── ts_ayam_potong_clean.csv
│   ├── ts_ayam_kampung_clean.csv
│   └── ts_ayam_tua_clean.csv
├── run_dashboard.bat               # Script run (Windows)
├── test_api.py                     # Testing script
└── CARA_MENJALANKAN.md            # File ini
```

---

## 🔧 Konfigurasi

### Mengubah Port
Edit `app.py` baris terakhir:
```python
app.run(debug=True, host='0.0.0.0', port=XXXX)  # Ganti XXXX
```

### Mengubah Periode Prediksi
Edit `app.py` fungsi `generate_predictions()`:
```python
start_date = datetime(2025, 1, 1)  # Ubah tanggal mulai
prediction_dates = [start_date + timedelta(days=i) for i in range(14)]  # Ubah 14
```

---

## 📚 Dokumentasi Lengkap

Untuk informasi lebih detail, baca:

| File | Isi |
|------|-----|
| **MULAI_DISINI.md** | Panduan mulai cepat (Bahasa Indonesia) |
| **QUICK_START.md** | Setup 3 menit |
| **DASHBOARD_README.md** | Dokumentasi lengkap |
| **FITUR_DASHBOARD.md** | Penjelasan fitur-fitur |
| **STRUKTUR_DASHBOARD.md** | Arsitektur sistem |
| **DEPLOYMENT_GUIDE.md** | Panduan deployment |
| **DOKUMENTASI_INDEX.md** | Index semua dokumentasi |

---

## 💻 Teknologi yang Digunakan

- **Backend:** Flask (Python)
- **Frontend:** HTML5, CSS3, JavaScript
- **Chart:** Chart.js
- **Data:** Pandas, CSV
- **API:** REST JSON
- **Prediction:** ARIMA Model (statsmodels)

---

## 👥 Tim Proyek

**Proyek Data Mining - Kios Vantedjo**

- Product Manager: Cahyadi
- Data Engineer: Sabriyah
- Data Analyst: Elfa
- Modeler: Aidil
- Delivery & Ops: Rusydi

---

## ✅ Checklist Sebelum Mulai

- [ ] Python 3.8+ terinstall
- [ ] Dependencies terinstall (`pip install -r requirements.txt`)
- [ ] File CSV ada di `notebooks/processed_for_model/`
- [ ] Port 5000 tidak digunakan aplikasi lain
- [ ] Browser modern (Chrome, Firefox, Edge)

## 🤖 Model ARIMA

Dashboard menggunakan **model ARIMA** untuk prediksi yang lebih akurat!

- Model: ARIMA(1,1,1) untuk setiap kategori
- Training: Otomatis menggunakan data historis 2024
- Akurasi: Lebih baik dari metode baseline

Lihat **ARIMA_INTEGRATION.md** untuk detail teknis.

---

## 📞 Butuh Bantuan?

1. Baca file **MULAI_DISINI.md** untuk panduan cepat
2. Baca file **QUICK_START.md** untuk troubleshooting
3. Lihat **DOKUMENTASI_INDEX.md** untuk navigasi lengkap

---

## 🎉 Selamat Menggunakan!

Dashboard siap digunakan untuk menampilkan prediksi penjualan ayam 14 hari ke depan!

**Jika ada pertanyaan, silakan baca dokumentasi lengkap yang tersedia.**

---

**🐔 Happy Forecasting! 📈**

*Dashboard Prediksi Penjualan Ayam - Kios Vantedjo*
*Data Mining Project - 2025*
