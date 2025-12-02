# 🤖 Integrasi Model SARIMAX

## 📋 Overview

Dashboard Kios Vantedjo kini menggunakan **SARIMAX (Seasonal AutoRegressive Integrated Moving Average with eXogenous variables)** untuk prediksi permintaan ayam 7 hari ke depan.

## 🎯 Mengapa SARIMAX?

### Keunggulan SARIMAX vs ARIMA:

1. **Menangkap Pola Seasonal** 🔄
   - SARIMAX secara eksplisit menangkap pola seasonal (weekly pattern)
   - Parameter seasonal: (P, D, Q, s) = (1, 1, 1, 7)
   - Cocok untuk data dengan pola mingguan yang kuat

2. **Exogenous Variables** 📊
   - Menggunakan variabel eksternal untuk meningkatkan akurasi
   - Calendar features: dow, is_weekend, is_event, is_closed
   - Lag features: lag1, lag3, lag7
   - Moving averages: ma3, ma7

3. **Dynamic Forecasting** 🔄
   - Forecast dilakukan secara iteratif
   - Setiap prediksi menggunakan hasil prediksi sebelumnya
   - Lebih adaptif terhadap perubahan pola

4. **Akurasi Tinggi** ✅
   - MAPE < 20% untuk semua kategori ayam
   - Menangkap dampak event/libur terhadap permintaan
   - Hasil evaluasi menunjukkan akurasi sangat baik

## 📊 Parameter Model

### Model Configuration

```python
SARIMAX(
    order=(1, 1, 1),           # (p, d, q) - ARIMA order
    seasonal_order=(1, 1, 1, 7), # (P, D, Q, s) - Seasonal order
    enforce_stationarity=False,
    enforce_invertibility=False
)
```

### Parameter Explanation:

- **order=(1, 1, 1)**
  - p=1: Autoregressive order (menggunakan 1 lag)
  - d=1: Differencing order (untuk stationarity)
  - q=1: Moving average order

- **seasonal_order=(1, 1, 1, 7)**
  - P=1: Seasonal autoregressive order
  - D=1: Seasonal differencing order
  - Q=1: Seasonal moving average order
  - s=7: Seasonal period (weekly pattern)

## 🔧 Exogenous Variables

### 1. Calendar Features

```python
CALENDAR_BASE_COLS = [
    "is_closed",      # Toko tutup (1) atau buka (0)
    "dow",            # Day of week (0=Senin, 6=Minggu)
    "is_weekend",     # Weekend (1=Jumat/Sabtu, 0=hari kerja)
    "is_event",       # Hari libur/event (1=ada, 0=tidak)
    "pre_event_peak", # Hari sebelum event (demand naik)
    "restock_flag",   # Hari restock
]
```

### 2. Lag Features

```python
# Penjualan hari sebelumnya
lag1 = sales_smooth.shift(1)  # 1 hari sebelumnya
lag3 = sales_smooth.shift(3)  # 3 hari sebelumnya
lag7 = sales_smooth.shift(7)  # 7 hari sebelumnya (weekly)
```

### 3. Moving Averages

```python
# Rata-rata bergerak
ma3 = sales_smooth.rolling(3).mean()  # MA 3 hari
ma7 = sales_smooth.rolling(7).mean()  # MA 7 hari
```

## 📈 Proses Forecasting

### 1. Data Preparation

```python
# Load data historis
df = pd.read_csv('data/ts_ayam_potong_clean.csv')

# Prepare features
q_high = df['sales'].quantile(0.98)
df['sales_smooth'] = df['sales'].clip(lower=0, upper=q_high)
df['sales_log'] = np.log1p(df['sales_smooth'])

# Create lag and MA features
for lag in [1, 3, 7]:
    df[f'lag{lag}'] = df['sales_smooth'].shift(lag)

df['ma3'] = df['sales_smooth'].rolling(3).mean()
df['ma7'] = df['sales_smooth'].rolling(7).mean()
```

### 2. Model Training

```python
# Build SARIMAX model
model = SARIMAX(
    endog=y_train,
    exog=X_train,
    order=(1, 1, 1),
    seasonal_order=(1, 1, 1, 7),
    enforce_stationarity=False,
    enforce_invertibility=False,
)

# Fit model
res = model.fit(disp=False, maxiter=300)
```

### 3. Dynamic Forecasting

```python
# Forecast 7 hari secara iteratif
for current_date in future_dates:
    # Update lag features dengan prediksi sebelumnya
    lag1 = last_df['sales_smooth'].iloc[-1]
    lag3 = last_df['sales_smooth'].iloc[-3]
    lag7 = last_df['sales_smooth'].iloc[-7]
    
    # Update MA features
    ma3 = last_df['sales_smooth'].rolling(3).mean().iloc[-1]
    ma7 = last_df['sales_smooth'].rolling(7).mean().iloc[-1]
    
    # Forecast 1 hari
    log_pred = res.forecast(steps=1, exog=exog_row)
    y_hat = np.expm1(log_pred.iloc[0])
    
    # Clip prediction
    y_hat = max(0, y_hat)
    y_hat = min(y_hat, q_high * 1.8)
    
    # Update last_df untuk iterasi berikutnya
    last_df.loc[current_date] = {...}
```

## 📊 Evaluasi Model

### Metrik Evaluasi (7 hari terakhir):

Semua model SARIMAX mencapai akurasi sangat baik:

- **MAE (Mean Absolute Error)**: Rata-rata kesalahan prediksi
- **RMSE (Root Mean Squared Error)**: Kesalahan dengan penalti untuk error besar
- **MAPE (Mean Absolute Percentage Error)**: < 20% untuk semua kategori

### Hasil Evaluasi:

✅ **Ayam Potong**: MAPE < 20%, akurasi sangat baik
✅ **Ayam Kampung**: MAPE < 20%, akurasi sangat baik
✅ **Ayam Tua**: MAPE < 20%, akurasi sangat baik

## 🚀 Cara Menggunakan

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Jalankan Dashboard

```bash
python app.py
```

### 3. Akses Dashboard

Buka browser dan akses: `http://localhost:5000`

## 📁 File Structure

```
vantedjo-dashboard/
├── app.py                      # Flask backend
├── sarimax_predictor.py        # SARIMAX model implementation
├── data/
│   ├── ts_ayam_potong_clean.csv   # Data Ayam Potong
│   ├── ts_ayam_kampung_clean.csv  # Data Ayam Kampung
│   └── ts_ayam_tua_clean.csv      # Data Ayam Tua
├── templates/
│   └── index.html              # Frontend dashboard
└── static/
    ├── script.js               # JavaScript logic
    └── style.css               # Styling
```

## 🔄 API Endpoints

### 1. Get Predictions

```
GET /api/predictions
```

Response:
```json
{
  "success": true,
  "model": "SARIMAX(1,1,1)(1,1,1,7)",
  "period": "2025-12-03 - 2025-12-09",
  "data": {
    "dates": ["2025-12-03", "2025-12-04", ...],
    "ayam_potong": [22.5, 23.1, ...],
    "ayam_kampung": [9.8, 10.2, ...],
    "ayam_tua": [5.5, 5.7, ...]
  }
}
```

### 2. Get Model Info

```
GET /api/model-info
```

Response: Informasi lengkap tentang model SARIMAX, parameter, dan exogenous variables.

### 3. Get Historical Data

```
GET /api/historical
```

Response: Data historis 30 hari terakhir untuk visualisasi.

## 💡 Tips & Best Practices

1. **Data Quality**: Pastikan data historis lengkap dan akurat
2. **Calendar Features**: Update calendar features untuk event/libur baru
3. **Model Retraining**: Retrain model secara berkala dengan data terbaru
4. **Monitoring**: Monitor akurasi prediksi vs actual untuk evaluasi berkelanjutan

## 🐛 Troubleshooting

### Model tidak konvergen?
- Coba increase `maxiter` parameter
- Check data quality dan missing values
- Adjust parameter order jika perlu

### Prediksi tidak masuk akal?
- Check exogenous variables
- Verify lag features calculation
- Review data preprocessing steps

### Error saat load data?
- Pastikan file CSV ada di folder `data/`
- Check format tanggal (YYYY-MM-DD)
- Verify column names

## 📚 Referensi

- [Statsmodels SARIMAX Documentation](https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html)
- [Time Series Analysis with Python](https://www.statsmodels.org/stable/tsa.html)
- [SARIMAX Tutorial](https://www.statsmodels.org/stable/examples/notebooks/generated/statespace_sarimax_stata.html)

## 📞 Support

Untuk pertanyaan atau issue, silakan hubungi tim development atau buat issue di repository.

---

**Version:** 3.0.0
**Last Updated:** December 2025
**Model:** SARIMAX(1,1,1)(1,1,1,7)
