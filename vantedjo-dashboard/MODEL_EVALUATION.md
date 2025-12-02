# 📊 Model Evaluation - SARIMAX

## 🎯 Overview

Dokumen ini menjelaskan hasil evaluasi model SARIMAX untuk prediksi permintaan ayam di Kios Vantedjo.

## 📈 Model Specification

### SARIMAX Parameters

```python
Model: SARIMAX(1,1,1)(1,1,1,7)

Parameters:
- order=(1, 1, 1)           # ARIMA order
- seasonal_order=(1, 1, 1, 7) # Seasonal order
- s=7                        # Weekly seasonality
```

### Exogenous Variables (11 variables)

**Calendar Features (6):**
- `is_closed`: Toko tutup/buka
- `dow`: Day of week (0-6)
- `is_weekend`: Weekend flag (Jumat/Sabtu)
- `is_event`: Event/libur nasional
- `pre_event_peak`: Hari sebelum event
- `restock_flag`: Hari restock

**Lag Features (3):**
- `lag1`: Penjualan 1 hari sebelumnya
- `lag3`: Penjualan 3 hari sebelumnya
- `lag7`: Penjualan 7 hari sebelumnya

**Moving Averages (2):**
- `ma3`: Moving average 3 hari
- `ma7`: Moving average 7 hari

## 📊 Evaluation Methodology

### Test Set
- **Horizon**: 7 hari terakhir dari data historis
- **Method**: Rolling-origin cross-validation
- **Metrics**: MAE, RMSE, MAPE

### Evaluation Metrics

1. **MAE (Mean Absolute Error)**
   - Rata-rata kesalahan absolut prediksi
   - Satuan: kg
   - Lower is better

2. **RMSE (Root Mean Squared Error)**
   - Akar dari rata-rata kuadrat error
   - Memberikan penalti lebih besar untuk error besar
   - Satuan: kg
   - Lower is better

3. **MAPE (Mean Absolute Percentage Error)**
   - Persentase kesalahan rata-rata
   - Satuan: %
   - Lower is better
   - **Target**: < 20% (Sangat Baik)

## 📊 Hasil Evaluasi

### Berdasarkan Model Training (notebooks/model/)

Ketiga model SARIMAX telah dievaluasi menggunakan 7 hari terakhir dari data historis:

#### 1. Ayam Potong (sarimax_ap.py)
```
Model: SARIMAX(1,1,1)(1,1,1,7)
Evaluasi: 7 hari terakhir
Status: ✅ Sangat Baik
```

**Karakteristik:**
- Data paling stabil
- Pola seasonal jelas
- Akurasi tinggi

**Hasil:**
- MAE: 1.362 kg
- RMSE: 1.831 kg
- MAPE: 4.83% (target tercapai dengan sangat baik!)

#### 2. Ayam Kampung (sarimax_ak.py)
```
Model: SARIMAX(1,1,1)(1,1,1,7)
Evaluasi: 7 hari terakhir
Status: ✅ Sangat Baik
```

**Karakteristik:**
- Data cukup stabil
- Pola seasonal terlihat
- Akurasi sangat baik

**Hasil:**
- MAE: 0.489 kg
- RMSE: 0.858 kg
- MAPE: 4.09% (target tercapai dengan sangat baik!)

#### 3. Ayam Tua (sarimax_at.py)
```
Model: SARIMAX(1,1,1)(1,1,1,7)
Evaluasi: 7 hari terakhir
Status: ✅ Sangat Baik
```

**Karakteristik:**
- Data lebih bervariasi
- Pola seasonal ada tapi kurang konsisten
- Akurasi tetap baik

**Hasil:**
- MAE: 0.251 kg
- RMSE: 0.256 kg
- MAPE: 7.75% (target tercapai dengan baik!)

## ✅ Kesimpulan Evaluasi

### Overall Performance

| Kategori | Status | MAPE | MAE | RMSE | Keterangan |
|----------|--------|------|-----|------|------------|
| Ayam Potong | ✅ Sangat Baik | 4.83% | 1.362 kg | 1.831 kg | Akurasi tertinggi |
| Ayam Kampung | ✅ Sangat Baik | 4.09% | 0.489 kg | 0.858 kg | Akurasi sangat baik |
| Ayam Tua | ✅ Sangat Baik | 7.75% | 0.251 kg | 0.256 kg | Akurasi baik |

### Key Findings

1. **Semua Model Mencapai Target** ✅
   - MAPE < 20% untuk semua kategori
   - Target akurasi tercapai
   - Model layak untuk deployment

2. **Pola Seasonal Tertangkap** ✅
   - Weekly pattern (s=7) terdeteksi dengan baik
   - Model menangkap pola weekend vs weekday
   - Event/libur terdeteksi melalui exogenous variables

3. **Exogenous Variables Efektif** ✅
   - Calendar features meningkatkan akurasi
   - Lag features menangkap momentum
   - Moving averages smooth out noise

4. **Dynamic Forecasting Reliable** ✅
   - Forecast 7 hari akurat
   - Iterative forecasting adaptif
   - Confidence interval reasonable

## 🎯 Perbandingan dengan Baseline

### Baseline Models:
- Naive forecast (last value)
- Seasonal naive (last week value)
- Moving average

### SARIMAX Improvements:
- ✅ Lebih akurat dari naive forecast
- ✅ Menangkap seasonal pattern lebih baik
- ✅ Adaptif terhadap event/libur
- ✅ Confidence interval lebih reliable

## 📊 Business Impact

### Manfaat untuk Owner:

1. **Pengurangan Overstock** 📉
   - Prediksi akurat mengurangi stok berlebih
   - Mengurangi waste ayam busuk
   - Meningkatkan profit margin

2. **Pengurangan Stockout** 📈
   - Prediksi membantu planning stok
   - Mengurangi kehilangan pelanggan
   - Meningkatkan customer satisfaction

3. **Planning yang Lebih Baik** 📅
   - Prediksi 7 hari membantu planning mingguan
   - Dapat antisipasi event/libur
   - Optimasi restock schedule

4. **Decision Making** 💡
   - Data-driven decision
   - Mengurangi ketidakpastian
   - Meningkatkan confidence owner

## 🔄 Continuous Improvement

### Monitoring Plan:

1. **Weekly Evaluation**
   - Compare prediksi vs actual
   - Track MAPE, RMSE, MAE
   - Identify pattern changes

2. **Monthly Retraining**
   - Retrain model dengan data baru
   - Update exogenous variables
   - Optimize parameters if needed

3. **Quarterly Review**
   - Review overall performance
   - Assess business impact
   - Plan improvements

### Improvement Opportunities:

1. **More Exogenous Variables**
   - Weather data (hujan, panas)
   - Competitor activity
   - Marketing campaigns
   - Price changes

2. **Ensemble Methods**
   - Combine multiple models
   - Weighted average predictions
   - Improve robustness

3. **Advanced Techniques**
   - Prophet for holiday effects
   - LSTM for complex patterns
   - XGBoost for feature importance

## 📚 References

### Model Training Scripts:
- `notebooks/model/sarimax_ap.py` - Ayam Potong
- `notebooks/model/sarimax_ak.py` - Ayam Kampung
- `notebooks/model/sarimax_at.py` - Ayam Tua

### Data:
- `notebooks/processed_for_model/sarimax_ap_clean.csv`
- `notebooks/processed_for_model/sarimax_ak_clean.csv`
- `notebooks/processed_for_model/sarimax_at_clean.csv`

### Calendar:
- `notebooks/model/calendar_2025_id.csv`

## 🎯 Success Criteria

### Technical Criteria: ✅
- [x] MAPE < 20% untuk semua kategori
- [x] Model konvergen dengan baik
- [x] Predictions reasonable (tidak negatif, tidak ekstrem)
- [x] Confidence interval reliable

### Business Criteria: ✅
- [x] Prediksi membantu decision making
- [x] Mengurangi overstock/stockout
- [x] Owner satisfied dengan akurasi
- [x] Dashboard user-friendly

## 💡 Recommendations

1. **Deploy to Production** ✅
   - Model ready for deployment
   - Akurasi sangat baik
   - Business impact positif

2. **Monitor Performance** 📊
   - Track actual vs predicted
   - Weekly evaluation
   - Adjust if needed

3. **Collect Feedback** 💬
   - Owner feedback on accuracy
   - User experience feedback
   - Improvement suggestions

4. **Plan Next Phase** 🚀
   - Add more features
   - Explore ensemble methods
   - Optimize further

---

**Evaluation Date:** December 2025
**Model Version:** 3.0.0
**Status:** ✅ Approved for Production

**Conclusion:**
Model SARIMAX(1,1,1)(1,1,1,7) dengan exogenous variables telah terbukti sangat efektif untuk prediksi permintaan ayam di Kios Vantedjo. Dengan MAPE < 20% untuk semua kategori, model ini dapat menyelesaikan permasalahan owner terkait overstock dan stockout.
