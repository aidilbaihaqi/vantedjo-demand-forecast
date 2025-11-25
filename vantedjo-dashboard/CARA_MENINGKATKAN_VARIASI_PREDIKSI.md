# Cara Meningkatkan Variasi Prediksi ARIMA

## 🔍 Masalah: Prediksi Terlalu Flat/Sama

Jika prediksi ARIMA Anda hampir sama setiap hari (misalnya: 22.65, 22.65, 22.65...), ini karena:

1. **Parameter ARIMA terlalu sederhana** - ARIMA(1,1,1) cenderung konvergen ke mean
2. **Model tidak menangkap pola variasi** - Data penjualan sebenarnya bervariasi setiap hari
3. **Forecast horizon terlalu panjang** - Semakin jauh prediksi, semakin mendekati mean

## ✅ Solusi yang Sudah Diterapkan

### 1. **Upgrade ke ARIMA(2,1,2)**

Parameter yang lebih kompleks untuk menangkap variasi:
- **p=2**: Menggunakan 2 lag sebelumnya (bukan 1)
- **d=1**: Differencing order tetap 1
- **q=2**: Moving average order 2 (bukan 1)

Hasil: **Variasi lebih baik!**

```
Sebelum (1,1,1):
2025-01-04: AP=22.65
2025-01-05: AP=22.65
2025-01-06: AP=22.65

Sesudah (2,1,2):
2025-01-04: AP=22.68
2025-01-05: AP=22.66
2025-01-06: AP=22.68
```

### 2. **Auto ARIMA (Optional - Lebih Baik)**

Install library `pmdarima` untuk auto-detect parameter terbaik:

```bash
pip install pmdarima
```

Setelah install, sistem akan otomatis mencari parameter ARIMA terbaik untuk setiap jenis ayam.

## 🚀 Cara Install pmdarima

### Windows:
```bash
pip install pmdarima
```

### Linux/Mac:
```bash
pip3 install pmdarima
```

### Jika ada error:
```bash
# Install dependencies dulu
pip install numpy scipy scikit-learn statsmodels

# Kemudian install pmdarima
pip install pmdarima
```

## 📊 Hasil yang Diharapkan

### Dengan ARIMA(2,1,2):
- ✅ Variasi lebih baik dari (1,1,1)
- ✅ Masih ada pola naik-turun
- ⚠️ Pola mungkin masih terlihat repetitif

### Dengan Auto ARIMA (pmdarima):
- ✅ Parameter optimal untuk setiap jenis ayam
- ✅ Variasi lebih natural
- ✅ Akurasi lebih baik
- ✅ Contoh: Ayam Potong mungkin (3,1,2), Ayam Kampung (2,1,1), dll

## 🔧 Opsi Lain untuk Variasi Lebih Baik

### Opsi 1: SARIMA (Seasonal ARIMA)

Jika data punya pola musiman (mingguan/bulanan):

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX

model = SARIMAX(series, 
                order=(2, 1, 2),
                seasonal_order=(1, 1, 1, 7))  # 7 = weekly pattern
```

### Opsi 2: Prophet (Facebook)

Model yang lebih advanced untuk time series:

```bash
pip install prophet
```

```python
from prophet import Prophet

df_prophet = pd.DataFrame({
    'ds': series.index,
    'y': series.values
})

model = Prophet()
model.fit(df_prophet)
future = model.make_future_dataframe(periods=14)
forecast = model.predict(future)
```

### Opsi 3: LSTM (Deep Learning)

Untuk pola yang sangat kompleks:

```python
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Build LSTM model
# (Lebih kompleks, butuh lebih banyak data)
```

## 📝 Rekomendasi

Untuk kasus Anda (Kios Vantedjo):

1. **Mulai dengan ARIMA(2,1,2)** ✅ (Sudah diterapkan)
2. **Install pmdarima** untuk auto-tuning
3. **Jika masih kurang variasi**, coba SARIMA dengan seasonal pattern
4. **Jika butuh akurasi tinggi**, pertimbangkan Prophet

## 🎯 Trade-off

| Model | Variasi | Akurasi | Kompleksitas | Speed |
|-------|---------|---------|--------------|-------|
| ARIMA(1,1,1) | ⭐ | ⭐⭐ | ⭐ | ⭐⭐⭐ |
| ARIMA(2,1,2) | ⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ |
| Auto ARIMA | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐ | ⭐⭐ |
| SARIMA | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |
| Prophet | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐ |
| LSTM | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐ |

## ⚠️ Catatan Penting

1. **Variasi ≠ Akurasi**: Prediksi yang bervariasi belum tentu lebih akurat
2. **Validasi Penting**: Selalu validasi dengan data test
3. **Business Context**: Untuk stok planning, prediksi yang stabil mungkin lebih baik
4. **Uncertainty**: Pertimbangkan confidence interval, bukan hanya point forecast

## 🧪 Testing

Setelah perubahan, test dengan:

```bash
python vantedjo-dashboard/arima_predictor.py
```

Bandingkan:
- Variasi prediksi (apakah ada naik-turun?)
- Rata-rata prediksi (apakah masuk akal?)
- Pola prediksi (apakah natural?)

---

**Current Status**: ✅ Menggunakan ARIMA(2,1,2) - Variasi lebih baik!
**Next Step**: Install pmdarima untuk hasil optimal
