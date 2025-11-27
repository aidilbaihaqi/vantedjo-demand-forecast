# Penjelasan Metrik Evaluasi Model ARIMA(2,1,2)

## 📚 Daftar Isi
1. [Pengenalan Metrik Evaluasi](#pengenalan-metrik-evaluasi)
2. [MAE (Mean Absolute Error)](#mae-mean-absolute-error)
3. [RMSE (Root Mean Squared Error)](#rmse-root-mean-squared-error)
4. [MAPE (Mean Absolute Percentage Error)](#mape-mean-absolute-percentage-error)
5. [Perbandingan Metrik](#perbandingan-metrik)
6. [Interpretasi Hasil](#interpretasi-hasil)
7. [Cara Menjalankan Evaluasi](#cara-menjalankan-evaluasi)

---

## 1. Pengenalan Metrik Evaluasi

Metrik evaluasi digunakan untuk mengukur **seberapa baik model ARIMA** dalam memprediksi data. Semakin kecil nilai error, semakin baik model.

### Mengapa Perlu Evaluasi?

- ✅ Mengukur **akurasi** model
- ✅ Membandingkan **performa** antar model
- ✅ Menentukan apakah model **layak digunakan**
- ✅ Mengidentifikasi **area perbaikan**

### Metode Evaluasi: Train-Test Split

```
Total Data (366 hari)
    ↓
┌─────────────────────────────────────┐
│  Training (80%)  │  Testing (20%)   │
│   293 hari       │   73 hari        │
└─────────────────────────────────────┘
         ↓                  ↓
    Train Model      Evaluasi Prediksi
```

**Proses:**
1. **Training (80%)**: Model belajar dari data ini
2. **Testing (20%)**: Model diprediksi, lalu dibandingkan dengan data aktual
3. **Hitung Error**: Bandingkan prediksi vs aktual

---

## 2. MAE (Mean Absolute Error)

### Definisi
**MAE** mengukur rata-rata **selisih absolut** antara nilai prediksi dan nilai aktual.

### Formula
```
MAE = (1/n) × Σ|y_actual - y_predicted|
```

Dimana:
- `n` = jumlah observasi
- `y_actual` = nilai aktual
- `y_predicted` = nilai prediksi
- `|...|` = nilai absolut (selalu positif)

### Contoh Perhitungan

**Data Testing (5 hari):**
```
Tanggal     Aktual (kg)   Prediksi (kg)   Error Absolut
2024-11-01      25.5          23.2         |25.5 - 23.2| = 2.3
2024-11-02      28.3          27.1         |28.3 - 27.1| = 1.2
2024-11-03      22.8          24.5         |22.8 - 24.5| = 1.7
2024-11-04      30.2          29.8         |30.2 - 29.8| = 0.4
2024-11-05      26.7          25.9         |26.7 - 25.9| = 0.8
```

**Perhitungan MAE:**
```
MAE = (2.3 + 1.2 + 1.7 + 0.4 + 0.8) / 5
MAE = 6.4 / 5
MAE = 1.28 kg
```

### Interpretasi MAE

| MAE (kg) | Interpretasi | Keterangan |
|----------|--------------|------------|
| 0 - 2    | Sangat Baik  | Error sangat kecil |
| 2 - 5    | Baik         | Error masih dapat diterima |
| 5 - 10   | Cukup        | Perlu monitoring |
| > 10     | Kurang       | Model perlu perbaikan |

**Contoh Interpretasi:**
- MAE = 1.28 kg → Model rata-rata meleset **1.28 kg** per hari
- Jika prediksi 25 kg, aktual bisa 23.72 kg atau 26.28 kg

### Kelebihan MAE
- ✅ Mudah dipahami (dalam satuan asli: kg)
- ✅ Tidak sensitif terhadap outlier
- ✅ Semua error diperlakukan sama

### Kekurangan MAE
- ❌ Tidak membedakan error besar dan kecil
- ❌ Tidak dalam bentuk persentase

---

## 3. RMSE (Root Mean Squared Error)

### Definisi
**RMSE** mengukur rata-rata **akar kuadrat dari error kuadrat**. Lebih sensitif terhadap error besar.

### Formula
```
RMSE = √[(1/n) × Σ(y_actual - y_predicted)²]
```

### Contoh Perhitungan

Menggunakan data yang sama:
```
Tanggal     Aktual   Prediksi   Error    Error²
2024-11-01   25.5     23.2      2.3      5.29
2024-11-02   28.3     27.1      1.2      1.44
2024-11-03   22.8     24.5     -1.7      2.89
2024-11-04   30.2     29.8      0.4      0.16
2024-11-05   26.7     25.9      0.8      0.64
```

**Perhitungan RMSE:**
```
MSE = (5.29 + 1.44 + 2.89 + 0.16 + 0.64) / 5
MSE = 10.42 / 5
MSE = 2.084

RMSE = √2.084
RMSE = 1.44 kg
```

### Interpretasi RMSE

**Perbandingan RMSE vs MAE:**
- Jika **RMSE ≈ MAE** → Error konsisten, tidak ada outlier besar
- Jika **RMSE >> MAE** → Ada beberapa error besar (outlier)

**Contoh:**
- MAE = 1.28 kg
- RMSE = 1.44 kg
- RMSE/MAE = 1.44/1.28 = 1.125

**Interpretasi:**
- Rasio 1.125 (dekat dengan 1) → Error relatif konsisten
- Tidak ada outlier yang signifikan

### Kelebihan RMSE
- ✅ Lebih sensitif terhadap error besar
- ✅ Menghukum prediksi yang sangat meleset
- ✅ Berguna untuk deteksi outlier

### Kekurangan RMSE
- ❌ Lebih sulit dipahami dibanding MAE
- ❌ Sangat dipengaruhi outlier
- ❌ Tidak dalam bentuk persentase

---

## 4. MAPE (Mean Absolute Percentage Error)

### Definisi
**MAPE** mengukur rata-rata **persentase error absolut**. Metrik paling mudah dipahami karena dalam bentuk persentase.

### Formula
```
MAPE = (1/n) × Σ|(y_actual - y_predicted) / y_actual| × 100%
```

### Contoh Perhitungan

```
Tanggal     Aktual   Prediksi   Error    % Error
2024-11-01   25.5     23.2      2.3      |2.3/25.5| × 100 = 9.02%
2024-11-02   28.3     27.1      1.2      |1.2/28.3| × 100 = 4.24%
2024-11-03   22.8     24.5     -1.7      |1.7/22.8| × 100 = 7.46%
2024-11-04   30.2     29.8      0.4      |0.4/30.2| × 100 = 1.32%
2024-11-05   26.7     25.9      0.8      |0.8/26.7| × 100 = 3.00%
```

**Perhitungan MAPE:**
```
MAPE = (9.02 + 4.24 + 7.46 + 1.32 + 3.00) / 5
MAPE = 25.04 / 5
MAPE = 5.01%
```

### Interpretasi MAPE

| MAPE (%) | Akurasi Model | Interpretasi |
|----------|---------------|--------------|
| < 10%    | Sangat Baik   | Excellent forecasting |
| 10-20%   | Baik          | Good forecasting |
| 20-30%   | Cukup         | Acceptable forecasting |
| 30-50%   | Kurang        | Inaccurate forecasting |
| > 50%    | Buruk         | Poor forecasting |

**Contoh Interpretasi:**
- MAPE = 5.01% → Model **SANGAT BAIK**
- Artinya: Prediksi rata-rata meleset **5.01%** dari nilai aktual
- Jika prediksi 100 kg, aktual bisa 95 kg - 105 kg

### Kelebihan MAPE
- ✅ Mudah dipahami (dalam persentase)
- ✅ Dapat dibandingkan antar dataset berbeda
- ✅ Standar industri untuk forecasting
- ✅ Tidak bergantung pada skala data

### Kekurangan MAPE
- ❌ Tidak bisa digunakan jika ada nilai aktual = 0
- ❌ Asimetris (lebih menghukum under-prediction)
- ❌ Bias terhadap nilai kecil

---

## 5. Perbandingan Metrik

### Tabel Perbandingan

| Aspek | MAE | RMSE | MAPE |
|-------|-----|------|------|
| **Satuan** | Sama dengan data (kg) | Sama dengan data (kg) | Persentase (%) |
| **Interpretasi** | Mudah | Sedang | Sangat Mudah |
| **Sensitivitas Outlier** | Rendah | Tinggi | Sedang |
| **Penggunaan** | Error absolut | Deteksi outlier | Akurasi relatif |
| **Standar Industri** | Ya | Ya | Ya (paling populer) |

### Kapan Menggunakan Metrik Apa?

**Gunakan MAE jika:**
- ✅ Ingin metrik yang mudah dipahami
- ✅ Semua error sama pentingnya
- ✅ Tidak ingin dipengaruhi outlier

**Gunakan RMSE jika:**
- ✅ Error besar harus dihukum lebih berat
- ✅ Ingin deteksi outlier
- ✅ Perlu metrik yang sensitif

**Gunakan MAPE jika:**
- ✅ Ingin metrik dalam persentase
- ✅ Membandingkan model untuk dataset berbeda
- ✅ Komunikasi dengan non-teknis
- ✅ Standar industri forecasting

---

## 6. Interpretasi Hasil

### Contoh Hasil Evaluasi

```
HASIL EVALUASI MODEL ARIMA(2,1,2) - AYAM POTONG

📊 METRIK EVALUASI:
   MAE  : 3.45 kg
   RMSE : 4.23 kg
   MAPE : 12.34%

📈 STATISTIK DATA:
   Rata-rata Aktual   : 28.50 kg/hari
   Rata-rata Prediksi : 27.80 kg/hari
   Selisih Rata-rata  : 0.70 kg
```

### Analisis Lengkap

#### 1. Analisis MAE (3.45 kg)
```
✅ INTERPRETASI:
   • Model rata-rata meleset 3.45 kg per hari
   • Untuk prediksi 28.5 kg, range error: 25.05 - 31.95 kg
   • Error relatif kecil untuk bisnis ayam

💡 IMPLIKASI BISNIS:
   • Jika prediksi 100 kg, siapkan buffer ±3.45 kg
   • Total buffer untuk 14 hari: ±48.3 kg
   • Masih dalam toleransi operasional
```

#### 2. Analisis RMSE (4.23 kg)
```
✅ INTERPRETASI:
   • RMSE/MAE = 4.23/3.45 = 1.23
   • Rasio > 1.2 menunjukkan ada beberapa error besar
   • Model kadang meleset cukup jauh

💡 IMPLIKASI BISNIS:
   • Perlu monitoring harian untuk deteksi anomali
   • Siapkan stok cadangan untuk hari-hari tertentu
   • Identifikasi pola hari dengan error besar
```

#### 3. Analisis MAPE (12.34%)
```
✅ INTERPRETASI:
   • MAPE 12.34% → Akurasi Model: BAIK
   • Prediksi rata-rata meleset 12.34% dari aktual
   • Masih dalam kategori "Good Forecasting"

💡 IMPLIKASI BISNIS:
   • Model layak digunakan untuk perencanaan stok
   • Akurasi 87.66% cukup untuk operasional
   • Dapat mengurangi overstock dan understock
```

### Kesimpulan Evaluasi

```
✅ MODEL LAYAK DIGUNAKAN

Alasan:
1. MAPE < 20% (kategori BAIK)
2. MAE relatif kecil (3.45 kg dari rata-rata 28.5 kg)
3. RMSE tidak terlalu jauh dari MAE (ada outlier tapi terkontrol)

Rekomendasi:
• Gunakan untuk forecasting 14 hari ke depan
• Monitor dan update model setiap bulan
• Pertimbangkan faktor eksternal (libur, event)
• Siapkan buffer stok ±5 kg per hari
```

---

## 7. Cara Menjalankan Evaluasi

### Langkah 1: Persiapan

Pastikan file data ada di lokasi yang benar:
```
notebooks/processed_for_model/
├── ts_ayam_potong_clean.csv
├── ts_ayam_kampung_clean.csv
└── ts_ayam_tua_clean.csv
```

### Langkah 2: Install Dependencies

```bash
pip install pandas numpy statsmodels scikit-learn matplotlib
```

### Langkah 3: Jalankan Script

```bash
python evaluate_arima_model.py
```

### Langkah 4: Output yang Dihasilkan

**1. Output Console:**
```
====================================================================================
                         EVALUASI MODEL ARIMA(2,1,2)
                      FORECASTING KIOS VANTEDJO
====================================================================================

======================================================================
EVALUASI MODEL ARIMA(2,1,2) - AYAM POTONG
======================================================================

Total data: 366 hari
Periode: 2024-01-01 s/d 2024-12-31

Data Training: 293 hari (80.0%)
Data Testing: 73 hari (20.0%)

[INFO] Training model ARIMA(2,1,2)...
[INFO] Model berhasil di-training!
[INFO] Melakukan prediksi untuk 73 hari...

======================================================================
HASIL EVALUASI MODEL
======================================================================

📊 METRIK EVALUASI:
   MAE (Mean Absolute Error)      : 3.4523 kg
   RMSE (Root Mean Squared Error) : 4.2341 kg
   MAPE (Mean Absolute % Error)   : 12.34%

📈 STATISTIK DATA:
   Rata-rata Aktual               : 28.50 kg/hari
   Rata-rata Prediksi             : 27.80 kg/hari
   Selisih Rata-rata              : 0.70 kg

💡 INTERPRETASI:
   ...
```

**2. File yang Dihasilkan:**
- `evaluasi_ayam_potong.png` - Grafik perbandingan
- `evaluasi_ayam_kampung.png` - Grafik perbandingan
- `evaluasi_ayam_tua.png` - Grafik perbandingan
- `hasil_evaluasi_arima.csv` - Tabel hasil evaluasi

**3. Tabel Ringkasan:**
```
==========================================================================================
RINGKASAN EVALUASI SEMUA KATEGORI AYAM
==========================================================================================

Kategori             MAE (kg)        RMSE (kg)       MAPE (%)        Akurasi        
------------------------------------------------------------------------------------------
Ayam Potong          3.4523          4.2341          12.34           BAIK           
Ayam Kampung         2.1234          2.8765          15.67           BAIK           
Ayam Tua             1.8901          2.3456          18.23           BAIK           
------------------------------------------------------------------------------------------
RATA-RATA            2.4886          3.1521          15.41           

==========================================================================================
```

---

## 📊 Visualisasi Hasil

Grafik yang dihasilkan menampilkan:
- **Garis Biru**: Data aktual (ground truth)
- **Garis Merah Putus-putus**: Prediksi model
- **Judul**: Menampilkan MAE, RMSE, dan MAPE

Contoh interpretasi grafik:
- Jika garis merah dekat dengan biru → Model akurat
- Jika ada gap besar → Model kurang akurat di periode tersebut
- Pola yang sama → Model menangkap trend dengan baik

---

## 🎯 Kesimpulan

### Metrik Terbaik untuk Forecasting Kios Vantedjo

**Prioritas 1: MAPE**
- Paling mudah dipahami (persentase)
- Standar industri forecasting
- Dapat dikomunikasikan ke stakeholder non-teknis

**Prioritas 2: MAE**
- Dalam satuan kg (mudah dipahami)
- Langsung menunjukkan buffer stok yang dibutuhkan
- Tidak terlalu sensitif terhadap outlier

**Prioritas 3: RMSE**
- Untuk deteksi outlier
- Monitoring kualitas model
- Identifikasi hari-hari dengan error besar

### Target Metrik yang Baik

Untuk bisnis forecasting ayam:
- **MAPE < 20%** → Model BAIK
- **MAE < 5 kg** → Error dapat diterima
- **RMSE/MAE < 1.5** → Tidak banyak outlier

---

## 📚 Referensi

1. Hyndman, R. J., & Koehler, A. B. (2006). Another look at measures of forecast accuracy
2. Makridakis, S., Wheelwright, S. C., & Hyndman, R. J. (1998). Forecasting: Methods and Applications
3. Scikit-learn Documentation: https://scikit-learn.org/stable/modules/model_evaluation.html

---

**Dibuat untuk:** Project Akhir Penambangan Data - Forecasting Kios Vantedjo  
**Tanggal:** 27 November 2025  
**Model:** ARIMA(2,1,2) dengan evaluasi MAE, RMSE, dan MAPE
