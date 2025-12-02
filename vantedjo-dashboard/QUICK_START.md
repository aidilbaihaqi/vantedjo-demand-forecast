# 🚀 Quick Start Guide - Dashboard Kios Vantedjo

## 📋 Prerequisites

- Python 3.8 atau lebih tinggi
- pip (Python package manager)

## ⚡ Langkah Cepat

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```bash
python app.py
```

### 3. Akses Dashboard

Buka browser dan akses:
```
http://localhost:5000
```

## 🎯 Apa yang Akan Anda Lihat?

### Dashboard Features:

1. **📊 Statistik Cards**
   - Rata-rata prediksi untuk setiap kategori ayam
   - Ayam Potong, Ayam Kampung, Ayam Tua

2. **🤖 Model Info Card**
   - Parameter model SARIMAX(1,1,1)(1,1,1,7)
   - Exogenous variables yang digunakan
   - Keunggulan model

3. **📈 Grafik Prediksi**
   - Visualisasi prediksi 7 hari ke depan
   - Line chart interaktif untuk 3 kategori ayam

4. **📋 Tabel Detail**
   - Prediksi harian untuk setiap kategori
   - Total prediksi per hari

5. **📚 Metodologi**
   - Penjelasan lengkap CRISP-DM framework
   - Detail model SARIMAX
   - Evaluasi dan hasil

## 🔧 Troubleshooting

### Port 5000 sudah digunakan?

Ubah port di `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=8080)
```

### Module tidak ditemukan?

Install ulang dependencies:
```bash
pip install -r requirements.txt --upgrade
```

### Data tidak muncul?

1. Pastikan file data ada di folder `data/`:
   - `ts_ayam_potong_clean.csv`
   - `ts_ayam_kampung_clean.csv`
   - `ts_ayam_tua_clean.csv`

2. Check console untuk error messages

## 📊 Test Model

Untuk test model SARIMAX secara standalone:

```bash
python sarimax_predictor.py
```

Output akan menampilkan:
- Prediksi 7 hari untuk semua kategori
- Rata-rata prediksi per kategori
- Detail prediksi harian

## 🎨 Customize Dashboard

### Ubah Forecast Horizon

Edit `sarimax_predictor.py`:
```python
FORECAST_DAYS = 7  # Ubah ke jumlah hari yang diinginkan
```

### Ubah Model Parameters

Edit `sarimax_predictor.py`:
```python
self.model_params = {
    'ayam_potong': {
        'order': (1, 1, 1),           # Ubah parameter ARIMA
        'seasonal_order': (1, 1, 1, 7) # Ubah parameter seasonal
    },
    ...
}
```

## 📚 Dokumentasi Lengkap

- **[README.md](README.md)** - Overview proyek
- **[SARIMAX_INTEGRATION.md](SARIMAX_INTEGRATION.md)** - Detail model SARIMAX
- **[CHANGELOG.md](CHANGELOG.md)** - Riwayat perubahan

## 💡 Tips

1. **Refresh Data**: Model akan retrain setiap kali API dipanggil
2. **Browser Cache**: Clear cache jika UI tidak update
3. **Console Logs**: Check browser console untuk debugging

## 🐛 Report Issues

Jika menemukan bug atau issue:
1. Check console logs (browser & terminal)
2. Verify data files exist
3. Check Python version compatibility

## 🎯 Next Steps

Setelah dashboard berjalan:
1. Explore metodologi section
2. Review model parameters
3. Analyze prediksi vs actual (jika ada data actual)
4. Customize sesuai kebutuhan

---

**Happy Forecasting! 🚀**

Model: SARIMAX(1,1,1)(1,1,1,7)
Version: 3.0.0
