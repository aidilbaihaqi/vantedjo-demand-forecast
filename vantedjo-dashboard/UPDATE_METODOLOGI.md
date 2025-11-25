# Update Informasi Metodologi

## ✅ **Perubahan yang Dilakukan**

### **1. Karakteristik Data Mentah**

#### **Sebelum:**
```
• Missing Values: X hari (dihitung otomatis)
• Hari Tutup: X hari (dihitung otomatis)
```

#### **Sesudah:**
```
• Missing Values: 0 hari (data lengkap, tidak ada missing)
• Hari Tutup: 10 hari (toko benar-benar tutup)
```

**Penjelasan:**
- Data mentah sudah lengkap, tidak ada missing values
- Yang ada adalah 10 hari dimana toko tutup (tidak beroperasi)

---

### **2. Proses Cleaning Data**

#### **Sebelum:**
```
Step 1: Handling Missing Values
Step 2: Format Tanggal
Step 3: Agregasi Harian
Step 4: Outlier Detection
Step 5: Time Series Preparation
```

#### **Sesudah:**
```
Step 1: Identifikasi Hari Tutup & Wawancara Ulang
        → Wawancara ulang dengan owner
        → Konfirmasi alasan toko tutup
        → Buat atribut is_closed

Step 2: Marking Hari Tutup
        → Tandai 10 hari yang toko tutup
        → Set is_closed = True

Step 3: Handling Data Hari Tutup
        → Isi quantity = 0 untuk hari tutup
        → Karena memang tidak ada penjualan

Step 4: Outlier Detection & Handling
        → IQR method untuk data valid
        → Exclude hari tutup dari perhitungan

Step 5: Time Series Preparation
        → Set date sebagai index
        → Sort chronologically
```

---

## 📊 **Detail 10 Hari Tutup**

Berdasarkan wawancara ulang dengan owner:

| Tanggal | Alasan |
|---------|--------|
| 1 Januari | Tahun Baru (Libur) |
| 15 Juli | Sakit |
| 16 Juli | Sakit |
| 17 Agustus | Hari Kemerdekaan |
| 27 Agustus | Antar Stok |
| 3 September | Sakit |
| 4 September | Sakit |
| 5 September | Sakit |
| 29 Oktober | Antar Stok |
| 22 November | Sakit |

**Total: 10 hari**

---

## 🔍 **Proses Wawancara Ulang**

### **Tujuan:**
Mengidentifikasi dan mengkonfirmasi alasan toko tutup pada hari-hari tertentu.

### **Pertanyaan yang Diajukan:**
1. Apakah toko benar-benar tutup (tidak beroperasi)?
2. Atau toko buka tapi tidak ada transaksi?
3. Apa alasan toko tutup?

### **Hasil:**
- **10 hari** toko benar-benar tutup (tidak beroperasi)
- **0 hari** toko buka tapi tidak ada transaksi
- Alasan: Sakit (6 hari), Libur (1 hari), Antar Stok (2 hari), Tahun Baru (1 hari)

---

## 💻 **Implementasi Kode**

### **Membuat Atribut is_closed:**

```python
import pandas as pd

# Load data
df = pd.read_excel('data_mentah.xlsx')

# Buat atribut is_closed (default False)
df['is_closed'] = False

# Daftar 10 hari tutup (dari wawancara)
closed_dates = [
    '2024-01-01',  # Tahun Baru
    '2024-07-15',  # Sakit
    '2024-07-16',  # Sakit
    '2024-08-17',  # Hari Kemerdekaan
    '2024-08-27',  # Antar Stok
    '2024-09-03',  # Sakit
    '2024-09-04',  # Sakit
    '2024-09-05',  # Sakit
    '2024-10-29',  # Antar Stok
    '2024-11-22'   # Sakit
]

# Tandai hari tutup
df.loc[df['date'].isin(closed_dates), 'is_closed'] = True

# Isi quantity = 0 untuk hari tutup
df.loc[df['is_closed'], 'quantity'] = 0

# Outlier detection hanya untuk hari buka
df_open = df[~df['is_closed']]
Q1 = df_open['quantity'].quantile(0.25)
Q3 = df_open['quantity'].quantile(0.75)
IQR = Q3 - Q1

# Handle outliers...
```

---

## 📈 **Impact pada Model**

### **Sebelum (Tanpa is_closed):**
- Model memperlakukan hari tutup sebagai hari dengan penjualan 0
- Bisa mempengaruhi akurasi prediksi
- Outlier detection tidak akurat

### **Sesudah (Dengan is_closed):**
- Model tahu bahwa hari tersebut memang tutup
- Outlier detection lebih akurat (exclude hari tutup)
- Prediksi lebih reliable untuk hari operasional

---

## ✅ **Validasi Data**

### **Checklist:**
- [x] Total records: 366 hari (2024 adalah tahun kabisat)
- [x] Missing values: 0 hari (data lengkap)
- [x] Hari tutup: 10 hari (sudah dikonfirmasi)
- [x] Atribut is_closed: Sudah dibuat
- [x] Data hari tutup: Sudah diisi 0
- [x] Outlier detection: Exclude hari tutup

---

## 🎯 **Untuk Presentasi**

### **Highlight Points:**

1. **Data Quality:**
   - "Data mentah sudah lengkap, tidak ada missing values"
   - "Yang ada adalah 10 hari dimana toko tutup"

2. **Metodologi:**
   - "Kami melakukan wawancara ulang untuk konfirmasi"
   - "Membuat atribut is_closed untuk membedakan hari tutup"

3. **Data Cleaning:**
   - "Proses cleaning dimulai dengan identifikasi hari tutup"
   - "Outlier detection hanya untuk hari operasional"

4. **Kredibilitas:**
   - "Proses validasi data yang ketat"
   - "Wawancara ulang untuk memastikan akurasi"

---

## 📝 **File yang Diupdate:**

1. ✅ `templates/methodology.html`
   - Stats: Missing Values = 0, Hari Tutup = 10
   - Process cleaning: 5 steps baru

2. ✅ `static/methodology.js`
   - Remove auto-calculation
   - Stats hardcoded

3. ✅ `HALAMAN_METODOLOGI.md`
   - Update dokumentasi
   - Update Q&A

---

**Kesimpulan**: Informasi metodologi sudah diupdate untuk mencerminkan proses yang sebenarnya dilakukan, dengan emphasis pada wawancara ulang dan pembuatan atribut is_closed! 🎯
