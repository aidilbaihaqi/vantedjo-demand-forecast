# Proyek Prediksi Musiman Penjualan Ayam – Kios Vantedjo

## 📋 Ringkasan Proyek

Proyek ini bertujuan untuk membangun sistem peramalan permintaan untuk Kios Vantedjo menggunakan teknik time series forecasting. Fokus utama adalah memprediksi penjualan harian untuk 3 kategori ayam (kampung, tua, potong) untuk mengurangi risiko overstock dan stockout.

## 🎯 Tujuan Bisnis

- **Masalah:** Kesulitan memprediksi permintaan musiman → risiko overstock/stockout
- **Solusi:** Time series forecasting dengan ARIMA/SARIMA
- **Target:** Penurunan MAPE 15-25% dan RMSE 20% dibanding baseline

## 📊 Data & Scope

- **Periode:** Januari - Desember 2024 (12 bulan)
- **Granularitas:** Harian per kategori ayam
- **Kategori:** Ayam kampung, ayam tua, ayam potong

## 🏗️ Struktur Proyek

```
vandtejo-demand-forecast/
├── data/
│   ├── raw/                 # Data mentah dari sumber (buku catatan, Excel)
│   ├── interim/             # Data dalam proses cleaning
│   └── processed/           # Data siap untuk modeling
├── notebooks/
│   ├── 01_eda.ipynb        # Exploratory Data Analysis
│   ├── 02_prep.ipynb       # Data Preparation & Feature Engineering
│   └── 03_modeling.ipynb   # Model Development & Evaluation
├── src/
│   ├── models/
│   │   └── arima.py        # ARIMA/SARIMA model implementations
│   └── eval/
│       └── tscv.py         # Time series cross-validation utilities
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Git ignore rules
```

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Start Jupyter Notebook
jupyter notebook
```

### 2. Data Pipeline

1. **Data Collection:** Place raw data in `data/raw/`
2. **EDA:** Run `notebooks/01_eda.ipynb`
3. **Preprocessing:** Run `notebooks/02_prep.ipynb`
4. **Modeling:** Run `notebooks/03_modeling.ipynb`

## 📈 Metodologi

### CRISP-DM Framework

1. **Business Understanding** - KPI definition, stakeholder alignment
2. **Data Understanding** - EDA, data quality assessment
3. **Data Preparation** - Cleaning, feature engineering
4. **Modeling** - ARIMA/SARIMA, baseline comparison
5. **Evaluation** - Time series CV, business metrics
6. **Deployment** - Dashboard, SOP documentation

### Model Approach

- **Baseline:** Naive & Seasonal Naive forecasts
- **Primary:** SARIMA with seasonal patterns (s=7)
- **Enhancement:** ARIMAX with calendar features
- **Validation:** Rolling-origin cross-validation

## 📊 Key Performance Indicators

### Technical Metrics
- **MAPE:** < 25% (target: 15-25% improvement vs baseline)
- **RMSE:** 20% reduction vs baseline
- **sMAPE:** Symmetric accuracy measure

### Business Metrics
- **Stockout Rate:** Frequency of zero inventory
- **Overstock Rate:** Excess inventory percentage
- **Forecast Accuracy:** Weekly forecast vs actual

## 👥 Tim & Peran

| Peran | Nama | Tanggung Jawab |
|-------|------|----------------|
| Product Manager | Cahyadi | Business requirements, KPI, stakeholder communication |
| Data Engineer | Sabriyah | Data pipeline, cleaning, feature engineering |
| Data Analyst | Elfa | EDA, data insights, baseline models |
| Modeler | Aidil | ARIMA development, model tuning |
| Delivery & Ops | Rusydi | Dashboard, SOP, operationalization |

## 📅 Timeline (6 Minggu)

- **Week 1:** Business understanding, data digitization
- **Week 2:** EDA, data quality assessment
- **Week 3:** Data preparation, baseline models
- **Week 4:** ARIMA/SARIMA development
- **Week 5:** Model evaluation, error analysis
- **Week 6:** Dashboard, SOP, final presentation

## 🔧 Dependencies

Key libraries dalam `requirements.txt`:
- `pandas`, `numpy` - Data manipulation
- `statsmodels` - Time series modeling
- `scikit-learn` - Model evaluation
- `plotly`, `matplotlib` - Visualization
- `arima` - ARIMA

## 📝 Komponen Utama

### Notebooks
- **01_eda.ipynb:** Analisis eksploratori data, identifikasi pola musiman
- **02_prep.ipynb:** Data cleaning, feature engineering, calendar features
- **03_modeling.ipynb:** Model development, tuning, dan evaluasi

### Source Code
- **src/models/arima.py:** Implementasi model ARIMA/SARIMA
- **src/eval/tscv.py:** Time series cross-validation framework

## 📋 Status Proyek

**Current Phase:** Week 6 - Dashboard, SOP, final presentation
**Last Updated:** November 2025
**Version:** 2.0.0 (with ARIMA Integration)

## 🌐 Dashboard Web

Dashboard interaktif untuk visualisasi prediksi 14 hari dengan **Model ARIMA** telah tersedia!

### ⚡ Quick Start Dashboard:
```bash
# Install dependencies
pip install -r requirements.txt

# Jalankan dashboard
python app.py
```

Akses di: `http://localhost:5000`

### 🤖 Model ARIMA
Dashboard menggunakan **ARIMA(1,1,1)** untuk prediksi yang lebih akurat:
- ✅ Training otomatis dengan data historis 2024
- ✅ Forecast 14 hari ke depan (1-14 Januari 2025)
- ✅ Mempertimbangkan trend dan pola historis

### 📚 Dokumentasi Lengkap
- **[CARA_MENJALANKAN.md](CARA_MENJALANKAN.md)** - Panduan lengkap (Bahasa Indonesia)
- **[DASHBOARD_README.md](DASHBOARD_README.md)** - Dokumentasi dashboard
- **[ARIMA_INTEGRATION.md](ARIMA_INTEGRATION.md)** - Detail integrasi ARIMA
- **[DOKUMENTASI_INDEX.md](DOKUMENTASI_INDEX.md)** - Index semua dokumentasi

---

### 🔄 Development Workflow

1. **Branch Strategy:** Feature branches untuk setiap milestone
2. **Code Review:** Peer review untuk semua notebook dan script
3. **Documentation:** Update README untuk setiap perubahan major
4. **Testing:** Validasi data quality dan model performance

### 📈 Success Criteria

**Technical:**
- Model mengalahkan Seasonal Naive di semua kategori
- MAPE & RMSE mencapai target improvement

**Business:**
- Simulasi menunjukkan penurunan stockout/overstock ≥15%
- Stakeholder approval untuk implementasi