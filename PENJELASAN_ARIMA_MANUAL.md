# Penjelasan Perhitungan Model ARIMA(2,1,2) Secara Manual

## 📚 Daftar Isi
1. [Pengenalan ARIMA](#pengenalan-arima)
2. [Komponen ARIMA(2,1,2)](#komponen-arima212)
3. [Data yang Digunakan](#data-yang-digunakan)
4. [Langkah-Langkah Perhitungan Manual](#langkah-langkah-perhitungan-manual)
5. [Contoh Perhitungan Konkret](#contoh-perhitungan-konkret)
6. [Implementasi di Python](#implementasi-di-python)

---

## 1. Pengenalan ARIMA

**ARIMA** = **A**uto**R**egressive **I**ntegrated **M**oving **A**verage

ARIMA adalah model statistik untuk analisis dan forecasting data time series. Model ini menggabungkan tiga komponen:

- **AR (AutoRegressive)**: Menggunakan nilai masa lalu untuk memprediksi nilai masa depan
- **I (Integrated)**: Melakukan differencing untuk membuat data stasioner
- **MA (Moving Average)**: Menggunakan error masa lalu untuk memprediksi nilai masa depan

### Notasi ARIMA(p, d, q)
- **p** = Order AR (jumlah lag observasi yang digunakan)
- **d** = Degree of differencing (berapa kali differencing dilakukan)
- **q** = Order MA (jumlah lag error yang digunakan)

Dalam kasus Anda: **ARIMA(2,1,2)**
- p = 2 (menggunakan 2 nilai masa lalu)
- d = 1 (differencing 1 kali)
- q = 2 (menggunakan 2 error masa lalu)

---

## 2. Komponen ARIMA(2,1,2)

### Formula Lengkap ARIMA(2,1,2):

```
Y'_t = φ₁Y'_{t-1} + φ₂Y'_{t-2} + θ₁ε_{t-1} + θ₂ε_{t-2} + ε_t
```

Dimana:
- **Y'_t** = Nilai setelah differencing pada waktu t
- **φ₁, φ₂** = Koefisien AR (parameter autoregressive)
- **θ₁, θ₂** = Koefisien MA (parameter moving average)
- **ε_t** = Error/residual pada waktu t
- **Y'_{t-1}, Y'_{t-2}** = Nilai lag 1 dan lag 2 setelah differencing

### Penjelasan Setiap Komponen:

#### A. Differencing (d=1)
Mengubah data non-stasioner menjadi stasioner dengan menghitung selisih:
```
Y'_t = Y_t - Y_{t-1}
```

**Contoh:**
- Y₁ = 23.12 kg
- Y₂ = 12.76 kg
- Y'₂ = 12.76 - 23.12 = -10.36

#### B. AutoRegressive (p=2)
Menggunakan 2 nilai masa lalu:
```
AR_part = φ₁Y'_{t-1} + φ₂Y'_{t-2}
```

#### C. Moving Average (q=2)
Menggunakan 2 error masa lalu:
```
MA_part = θ₁ε_{t-1} + θ₂ε_{t-2}
```

---

## 3. Data yang Digunakan

### Data Training: `ts_ayam_potong_clean.csv`

Contoh data (5 hari pertama):
```
Tanggal        Ayam_Potong (kg)
2024-01-01     0.00
2024-01-02     23.12
2024-01-03     12.76
2024-01-04     37.04
2024-01-05     53.68
```

Total data: **366 hari** (1 Januari 2024 - 31 Desember 2024)

---

## 4. Langkah-Langkah Perhitungan Manual

### LANGKAH 1: Differencing (d=1)

Hitung selisih antar hari untuk membuat data stasioner:

```
Y'_t = Y_t - Y_{t-1}
```

**Hasil Differencing:**
```
Tanggal        Y_t      Y'_t (Differenced)
2024-01-01     0.00     -
2024-01-02     23.12    23.12 - 0.00 = 23.12
2024-01-03     12.76    12.76 - 23.12 = -10.36
2024-01-04     37.04    37.04 - 12.76 = 24.28
2024-01-05     53.68    53.68 - 37.04 = 16.64
```

### LANGKAH 2: Estimasi Parameter Model

Model ARIMA menggunakan **Maximum Likelihood Estimation (MLE)** untuk mencari parameter optimal:
- φ₁, φ₂ (koefisien AR)
- θ₁, θ₂ (koefisien MA)

**Proses MLE (dilakukan oleh library statsmodels):**

1. **Inisialisasi parameter awal** (biasanya nilai kecil mendekati 0)
2. **Iterasi optimasi** menggunakan algoritma seperti:
   - BFGS (Broyden-Fletcher-Goldfarb-Shanno)
   - L-BFGS-B (Limited-memory BFGS with Bounds)
3. **Maksimalkan log-likelihood function**:
   ```
   L(φ, θ | Y) = -n/2 * log(2π) - n/2 * log(σ²) - Σ(ε_t²)/(2σ²)
   ```
4. **Konvergensi** ketika perubahan parameter < threshold

**Contoh Parameter yang Dihasilkan** (hipotesis):
```
φ₁ = 0.45  (koefisien AR lag 1)
φ₂ = 0.23  (koefisien AR lag 2)
θ₁ = -0.38 (koefisien MA lag 1)
θ₂ = -0.15 (koefisien MA lag 2)
```

### LANGKAH 3: Hitung Residual (Error)

Untuk setiap observasi, hitung error:
```
ε_t = Y'_t - Ŷ'_t
```

Dimana Ŷ'_t adalah prediksi model:
```
Ŷ'_t = φ₁Y'_{t-1} + φ₂Y'_{t-2} + θ₁ε_{t-1} + θ₂ε_{t-2}
```

### LANGKAH 4: Forecasting (Prediksi 14 Hari)

Untuk memprediksi nilai masa depan:

**Prediksi Hari ke-1 (2 Januari 2025):**
```
Y'₃₆₇ = φ₁Y'₃₆₆ + φ₂Y'₃₆₅ + θ₁ε₃₆₆ + θ₂ε₃₆₅
```

**Prediksi Hari ke-2 (3 Januari 2025):**
```
Y'₃₆₈ = φ₁Y'₃₆₇ + φ₂Y'₃₆₆ + θ₁ε₃₆₇ + θ₂ε₃₆₆
```

**Catatan:** Untuk prediksi masa depan, error (ε) diasumsikan = 0

### LANGKAH 5: Inverse Differencing

Kembalikan nilai differenced ke nilai asli:
```
Y_t = Y'_t + Y_{t-1}
```

**Contoh:**
- Y₃₆₆ = 25.5 kg (nilai terakhir data training)
- Y'₃₆₇ = 2.3 (hasil prediksi differenced)
- Y₃₆₇ = 2.3 + 25.5 = 27.8 kg (prediksi final)

---

## 5. Contoh Perhitungan Konkret

Mari kita hitung prediksi untuk **1 hari ke depan** secara manual:

### Data yang Diketahui:
```
Y₃₆₄ = 30.2 kg  (2 hari sebelum akhir)
Y₃₆₅ = 28.5 kg  (1 hari sebelum akhir)
Y₃₆₆ = 25.5 kg  (hari terakhir data training)
```

### Step 1: Hitung Differencing
```
Y'₃₆₅ = Y₃₆₅ - Y₃₆₄ = 28.5 - 30.2 = -1.7
Y'₃₆₆ = Y₃₆₆ - Y₃₆₅ = 25.5 - 28.5 = -3.0
```

### Step 2: Hitung Residual (dari model fitting)
Misalkan dari model fitting didapat:
```
ε₃₆₅ = -0.5
ε₃₆₆ = 0.3
```

### Step 3: Prediksi Differenced Value
Gunakan parameter model (contoh):
```
φ₁ = 0.45, φ₂ = 0.23, θ₁ = -0.38, θ₂ = -0.15
```

Hitung:
```
Y'₃₆₇ = φ₁Y'₃₆₆ + φ₂Y'₃₆₅ + θ₁ε₃₆₆ + θ₂ε₃₆₅

Y'₃₆₇ = (0.45 × -3.0) + (0.23 × -1.7) + (-0.38 × 0.3) + (-0.15 × -0.5)
Y'₃₆₇ = -1.35 + (-0.391) + (-0.114) + 0.075
Y'₃₆₇ = -1.78
```

### Step 4: Inverse Differencing
```
Y₃₆₇ = Y'₃₆₇ + Y₃₆₆
Y₃₆₇ = -1.78 + 25.5
Y₃₆₇ = 23.72 kg
```

**Hasil Prediksi: 23.72 kg untuk tanggal 2 Januari 2025**

### Untuk Prediksi Hari ke-2:
```
Y'₃₆₈ = φ₁Y'₃₆₇ + φ₂Y'₃₆₆ + θ₁(0) + θ₂(0)
      = (0.45 × -1.78) + (0.23 × -3.0)
      = -0.801 + (-0.69)
      = -1.491

Y₃₆₈ = -1.491 + 23.72 = 22.23 kg
```

---

## 6. Implementasi di Python

### Kode Lengkap dengan Penjelasan:

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# 1. LOAD DATA
df = pd.read_csv('ts_ayam_potong_clean.csv', parse_dates=['date'])
df = df.set_index('date').sort_index()
series = df['Ayam_Potong']

print("Data Asli (5 hari terakhir):")
print(series.tail())

# 2. DIFFERENCING MANUAL (untuk pemahaman)
diff_series = series.diff().dropna()
print("\nData Setelah Differencing (5 hari terakhir):")
print(diff_series.tail())

# 3. BUILD MODEL ARIMA(2,1,2)
model = ARIMA(series, order=(2, 1, 2))
model_fit = model.fit()

# 4. LIHAT PARAMETER MODEL
print("\n=== PARAMETER MODEL ===")
print(f"AR Coefficients (φ): {model_fit.arparams}")
print(f"MA Coefficients (θ): {model_fit.maparams}")
print(f"Sigma² (variance): {model_fit.sigma2}")

# 5. FORECAST 14 HARI
n_forecast = 14
forecast = model_fit.forecast(steps=n_forecast)

print("\n=== PREDIKSI 14 HARI ===")
for i, value in enumerate(forecast, 1):
    print(f"Hari ke-{i}: {value:.2f} kg")

# 6. HITUNG RESIDUAL (untuk validasi)
residuals = model_fit.resid
print(f"\nMean Residual: {residuals.mean():.4f}")
print(f"Std Residual: {residuals.std():.4f}")
```

### Output yang Diharapkan:
```
Data Asli (5 hari terakhir):
date
2024-12-27    28.50
2024-12-28    32.10
2024-12-29    27.80
2024-12-30    30.20
2024-12-31    25.50
Name: Ayam_Potong, dtype: float64

Data Setelah Differencing (5 hari terakhir):
date
2024-12-27    -2.30
2024-12-28     3.60
2024-12-29    -4.30
2024-12-30     2.40
2024-12-31    -4.70
Name: Ayam_Potong, dtype: float64

=== PARAMETER MODEL ===
AR Coefficients (φ): [0.4523, 0.2341]
MA Coefficients (θ): [-0.3812, -0.1523]
Sigma² (variance): 156.23

=== PREDIKSI 14 HARI ===
Hari ke-1: 23.72 kg
Hari ke-2: 22.23 kg
Hari ke-3: 24.15 kg
...
```

---

## 📊 Visualisasi Proses ARIMA

```
DATA ASLI (Y_t)
    ↓
DIFFERENCING (d=1)
    Y'_t = Y_t - Y_{t-1}
    ↓
MODEL ARIMA(2,1,2)
    Y'_t = φ₁Y'_{t-1} + φ₂Y'_{t-2} + θ₁ε_{t-1} + θ₂ε_{t-2} + ε_t
    ↓
ESTIMASI PARAMETER
    (φ₁, φ₂, θ₁, θ₂) via MLE
    ↓
FORECASTING
    Prediksi Y'_{t+1}, Y'_{t+2}, ..., Y'_{t+14}
    ↓
INVERSE DIFFERENCING
    Y_{t+h} = Y'_{t+h} + Y_{t+h-1}
    ↓
HASIL PREDIKSI FINAL
```

---

## 🎯 Kesimpulan

### Mengapa ARIMA(2,1,2)?

1. **p=2 (AR order)**: Penjualan ayam hari ini dipengaruhi oleh 2 hari sebelumnya
2. **d=1 (Differencing)**: Data penjualan memiliki trend, perlu 1x differencing untuk stasioner
3. **q=2 (MA order)**: Error prediksi 2 hari sebelumnya mempengaruhi prediksi hari ini

### Keunggulan ARIMA(2,1,2) vs ARIMA(1,1,1):

| Aspek | ARIMA(1,1,1) | ARIMA(2,1,2) |
|-------|--------------|--------------|
| Kompleksitas | Sederhana | Lebih kompleks |
| Akurasi | Baik untuk pola sederhana | Lebih baik untuk pola kompleks |
| Lag yang digunakan | 1 hari | 2 hari |
| Cocok untuk | Data smooth | Data dengan variasi tinggi |

### Aplikasi di Kios Vantedjo:

- **Prediksi stok optimal** untuk 14 hari ke depan
- **Menghindari overstock** (ayam busuk, rugi)
- **Menghindari understock** (kehabisan barang, kehilangan pelanggan)
- **Perencanaan pembelian** yang lebih efisien

---

## 📚 Referensi

1. Box, G. E. P., & Jenkins, G. M. (2015). Time Series Analysis: Forecasting and Control
2. Hyndman, R. J., & Athanasopoulos, G. (2018). Forecasting: Principles and Practice
3. Statsmodels Documentation: https://www.statsmodels.org/stable/generated/statsmodels.tsa.arima.model.ARIMA.html

---

**Dibuat untuk:** Project Akhir Penambangan Data - Forecasting Kios Vantedjo  
**Tanggal:** 26 November 2025  
**Model:** ARIMA(2,1,2) untuk prediksi permintaan ayam (potong, kampung, tua)
