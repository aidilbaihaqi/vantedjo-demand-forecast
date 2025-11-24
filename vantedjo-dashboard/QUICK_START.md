# 🚀 Quick Start - Dashboard Prediksi Ayam

## Langkah Cepat (3 Menit)

### 1️⃣ Install Dependencies
```bash
pip install flask flask-cors pandas
```

### 2️⃣ Jalankan Dashboard
**Windows:**
```bash
run_dashboard.bat
```

**Manual:**
```bash
python app.py
```

### 3️⃣ Buka Browser
```
http://localhost:5000
```

---

## 🧪 Testing API

```bash
python test_api.py
```

---

## 📱 Akses dari Device Lain

1. Cek IP komputer:
```bash
ipconfig
```

2. Akses dari device lain:
```
http://[IP_KOMPUTER]:5000
```

Contoh: `http://192.168.1.100:5000`

---

## 🛑 Stop Server

Tekan `Ctrl + C` di terminal

---

## 📋 Checklist

- [ ] Python terinstall (3.8+)
- [ ] Dependencies terinstall
- [ ] File CSV ada di `notebooks/processed_for_model/`
- [ ] Port 5000 tidak digunakan aplikasi lain
- [ ] Browser modern (Chrome, Firefox, Edge)

---

## ❓ Troubleshooting

### Port sudah digunakan
```bash
# Ubah port di app.py (line terakhir)
app.run(debug=True, host='0.0.0.0', port=8000)
```

### Module tidak ditemukan
```bash
pip install -r requirements.txt
```

### Data tidak muncul
- Pastikan file CSV ada di `notebooks/processed_for_model/`
- Cek console browser (F12) untuk error
- Cek terminal server untuk error log

---

## 📚 Dokumentasi Lengkap

- [DASHBOARD_README.md](DASHBOARD_README.md) - Dokumentasi lengkap
- [STRUKTUR_DASHBOARD.md](STRUKTUR_DASHBOARD.md) - Arsitektur & struktur
- [README.md](README.md) - Project overview

---

**Happy Forecasting! 🐔📈**
