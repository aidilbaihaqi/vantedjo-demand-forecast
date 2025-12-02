# Changelog - Dashboard Kios Vantedjo

## [3.0.0] - December 2025

### 🚀 Major Changes: ARIMA → SARIMAX

#### ✨ New Features

1. **Model SARIMAX Implementation**
   - Upgraded dari ARIMA(2,1,2) ke SARIMAX(1,1,1)(1,1,1,7)
   - Menangkap pola seasonal (weekly pattern) secara eksplisit
   - Forecast horizon: 14 hari → 7 hari (lebih akurat)

2. **Exogenous Variables**
   - Calendar features: is_closed, dow, is_weekend, is_event, pre_event_peak, restock_flag
   - Lag features: lag1, lag3, lag7
   - Moving averages: ma3, ma7

3. **Dynamic Forecasting**
   - Forecast dilakukan secara iteratif
   - Setiap prediksi menggunakan hasil prediksi sebelumnya
   - Lebih adaptif terhadap perubahan pola

4. **Model Info API**
   - Endpoint baru: `/api/model-info`
   - Menampilkan informasi lengkap tentang model, parameter, dan exogenous variables

#### 📊 Data Changes

1. **Data Format Update**
   - Menggunakan data dari `notebooks/processed_for_model/sarimax_*_clean.csv`
   - Format kolom: date, sales, is_closed, dow, is_weekend, is_event, pre_event_peak, restock_flag
   - Data sudah include calendar features dan preprocessing

2. **Data Conversion**
   - Script `convert_data.py` untuk convert format data
   - Rename kolom `sales` → `Ayam_Potong/Ayam_Kampung/Ayam_Tua`

#### 🎨 Frontend Updates

1. **Dashboard UI**
   - Update header: menampilkan model SARIMAX(1,1,1)(1,1,1,7)
   - Periode prediksi dinamis (dari API response)
   - Model info card dengan parameter dan keunggulan SARIMAX

2. **Metodologi Section**
   - Update parameter model dari ARIMA ke SARIMAX
   - Tambah informasi exogenous variables
   - Update proses training dengan SARIMAX code
   - Update evaluasi dengan hasil SARIMAX

3. **Footer**
   - Update model info: SARIMAX(1,1,1)(1,1,1,7)
   - Update forecast horizon: 7 hari

#### 🔧 Backend Updates

1. **app.py**
   - Import `sarimax_predictor` instead of `arima_predictor`
   - Update `USE_SARIMAX` flag (was `USE_ARIMA`)
   - Update `generate_predictions()` untuk 7 hari forecast
   - Update API response dengan model info
   - Tambah endpoint `/api/model-info`

2. **sarimax_wrapper.py** (New)
   - Wrapper untuk menggunakan model SARIMAX asli dari notebooks/model/
   - Menggunakan hasil langsung dari model yang sudah dievaluasi
   - Menjamin konsistensi dengan hasil evaluasi model

3. **model_sarimax_*.py** (New)
   - Copy dari notebooks/model/sarimax_*.py
   - Model SARIMAX asli yang sudah dievaluasi
   - Hasil prediksi sama dengan evaluasi di notebooks

#### 📚 Documentation

1. **SARIMAX_INTEGRATION.md** (New)
   - Dokumentasi lengkap integrasi SARIMAX
   - Penjelasan parameter model
   - Exogenous variables explanation
   - Proses forecasting step-by-step
   - API endpoints documentation

2. **README.md**
   - Update model info: SARIMAX(1,1,1)(1,1,1,7)
   - Update keunggulan SARIMAX vs ARIMA
   - Update version: 3.0.0

3. **CHANGELOG.md** (New)
   - Dokumentasi perubahan dari versi sebelumnya

#### 🐛 Bug Fixes

- Fix data loading untuk format baru
- Fix periode prediksi display
- Fix chart update untuk 7 hari forecast

#### ⚡ Performance Improvements

- Model training lebih cepat dengan parameter optimal
- Dynamic forecasting lebih akurat
- Exogenous variables meningkatkan akurasi prediksi

---

## [2.0.0] - November 2025

### Features
- ARIMA(2,1,2) model implementation
- 14 hari forecast
- Dashboard web dengan Flask
- Chart interaktif dengan Chart.js
- Tabel prediksi harian

---

## [1.0.0] - October 2025

### Features
- Baseline model (Naive & Seasonal Naive)
- EDA notebooks
- Data preprocessing
- Initial dashboard prototype

---

**Note:** Untuk detail lengkap tentang SARIMAX integration, lihat [SARIMAX_INTEGRATION.md](SARIMAX_INTEGRATION.md)
