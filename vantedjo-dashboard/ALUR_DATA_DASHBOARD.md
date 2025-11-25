# Alur Data Prediksi di Dashboard Vantedjo

## 📊 **Dari Mana Data Prediksi Berasal?**

Berdasarkan screenshot dashboard Anda yang menampilkan tabel prediksi harian, berikut alur lengkapnya:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ALUR DATA PREDIKSI                           │
└─────────────────────────────────────────────────────────────────┘

1. DATA TRAINING
   ├── notebooks/processed_for_model/ts_ayam_potong_clean.csv
   ├── notebooks/processed_for_model/ts_ayam_kampung_clean.csv
   └── notebooks/processed_for_model/ts_ayam_tua_clean.csv
   
2. MODEL ARIMA
   ├── arima_predictor.py
   │   ├── Load data dari CSV
   │   ├── Build model ARIMA(2,1,2) untuk setiap jenis ayam
   │   ├── Fit model dengan data historis
   │   └── Generate forecast 14 hari (skip tgl 1 Jan)
   │
   └── Output: Dictionary dengan prediksi
       {
         'dates': ['2025-01-02', '2025-01-03', ...],
         'ayam_potong': [25.2, 25.8, 25.3, ...],
         'ayam_kampung': [12.7, 10.1, 12.6, ...],
         'ayam_tua': [7.0, 5.0, 5.3, ...]
       }

3. BACKEND (Flask)
   ├── app.py
   │   ├── Route: /api/predictions
   │   ├── Call: get_predictions() dari arima_predictor.py
   │   ├── Round values ke 1 desimal
   │   └── Return JSON response
   │
   └── JSON Response:
       {
         "success": true,
         "data": {
           "dates": [...],
           "ayam_potong": [...],
           "ayam_kampung": [...],
           "ayam_tua": [...]
         },
         "period": "2 Januari 2025 - 15 Januari 2025",
         "message": "..."
       }

4. FRONTEND (JavaScript)
   ├── static/script.js
   │   ├── Fetch data dari /api/predictions
   │   ├── Parse JSON response
   │   └── Update UI:
   │       ├── updateStats() → Card statistik rata-rata
   │       ├── updateChart() → Grafik Chart.js
   │       └── updateTable() → Tabel detail harian
   │
   └── templates/index.html
       └── Tampilkan tabel dengan data prediksi

5. TAMPILAN DASHBOARD (Yang Anda Lihat)
   ┌─────────────────────────────────────────────────────┐
   │ Tanggal       │ Ayam Potong │ Ayam Kampung │ Ayam Tua │
   ├─────────────────────────────────────────────────────┤
   │ 2 Jan 2025    │    25.2     │     12.7     │   7.0    │
   │ 3 Jan 2025    │    25.8     │     10.1     │   5.0    │
   │ 4 Jan 2025    │    25.3     │     12.6     │   5.3    │
   │ ...           │    ...      │     ...      │   ...    │
   └─────────────────────────────────────────────────────┘
```

## 🔍 **Detail Setiap Langkah:**

### **1. Data Training (CSV Files)**

Data historis dari Januari - Desember 2024:
- `ts_ayam_potong_clean.csv` - 366 baris data harian
- `ts_ayam_kampung_clean.csv` - 366 baris data harian
- `ts_ayam_tua_clean.csv` - 366 baris data harian

### **2. Model ARIMA (arima_predictor.py)**

```python
# Proses di arima_predictor.py:

1. Load data CSV
   df = pd.read_csv('ts_ayam_potong_clean.csv')

2. Build model ARIMA(2,1,2)
   model = ARIMA(series, order=(2, 1, 2))
   model_fit = model.fit()

3. Generate forecast 14 hari
   forecast = model_fit.forecast(steps=14)

4. Skip tanggal 1 Januari
   # Mulai dari 2 Januari
   start_date = datetime(2025, 1, 2)

5. Return hasil
   return {
     'dates': ['2025-01-02', ...],
     'ayam_potong': [25.2, 25.8, ...],
     ...
   }
```

### **3. Backend Flask (app.py)**

```python
# Route API:

@app.route('/api/predictions')
def get_predictions():
    # 1. Call arima_predictor
    predictions = generate_predictions()
    
    # 2. Round values
    for key in ['ayam_potong', 'ayam_kampung', 'ayam_tua']:
        predictions[key] = [round(v, 1) for v in predictions[key]]
    
    # 3. Return JSON
    return jsonify({
        'success': True,
        'data': predictions
    })
```

### **4. Frontend JavaScript (script.js)**

```javascript
// Fetch dan tampilkan data:

async function loadPredictions() {
    // 1. Fetch dari API
    const response = await fetch('/api/predictions');
    const result = await response.json();
    
    // 2. Update tabel
    updateTable(result.data);
}

function updateTable(data) {
    // Loop setiap tanggal
    for (let i = 0; i < data.dates.length; i++) {
        // Buat row tabel
        row.innerHTML = `
            <td>${formatDate(data.dates[i])}</td>
            <td>${data.ayam_potong[i].toFixed(1)}</td>
            <td>${data.ayam_kampung[i].toFixed(1)}</td>
            <td>${data.ayam_tua[i].toFixed(1)}</td>
            <td>${total.toFixed(1)}</td>
        `;
    }
}
```

### **5. HTML Template (index.html)**

```html
<!-- Tabel di dashboard -->
<table id="predictionTable">
    <thead>
        <tr>
            <th>Tanggal</th>
            <th>Ayam Potong</th>
            <th>Ayam Kampung</th>
            <th>Ayam Tua</th>
            <th>Total</th>
        </tr>
    </thead>
    <tbody id="tableBody">
        <!-- Diisi oleh JavaScript -->
    </tbody>
</table>
```

## 📈 **Contoh Data Flow:**

```
CSV Data (2024-12-31):
  Ayam_Potong = 22.5 kg

↓ (ARIMA Model Training)

Model ARIMA(2,1,2):
  - Menganalisis pola 366 hari
  - Menangkap trend, seasonality
  - Fit dengan data historis

↓ (Forecast)

Prediksi 2025-01-02:
  Ayam_Potong = 25.2 kg  ← Hasil model ARIMA

↓ (Backend Processing)

JSON Response:
  {
    "dates": ["2025-01-02"],
    "ayam_potong": [25.2]
  }

↓ (Frontend Rendering)

Tabel Dashboard:
  | 2 Januari 2025 | 25.2 | ... |
```

## 🎯 **Kenapa Nilai Bervariasi?**

Dari screenshot Anda, terlihat nilai **sudah bervariasi dengan baik**:

```
2 Jan: AP=25.2, AK=12.7, AT=7.0
3 Jan: AP=25.8, AK=10.1, AT=5.0  ← Naik-turun
4 Jan: AP=25.3, AK=12.6, AT=5.3  ← Ada variasi
```

Ini karena:
1. ✅ Model ARIMA(2,1,2) menangkap pola variasi data
2. ✅ Parameter (p=2, q=2) lebih kompleks dari (1,1,1)
3. ✅ Model memprediksi berdasarkan pola historis

## 🔧 **Cara Verifikasi:**

### Test Backend:
```bash
# Test arima_predictor langsung
python vantedjo-dashboard/arima_predictor.py
```

### Test API:
```bash
# Jalankan server
python vantedjo-dashboard/app.py

# Di browser lain atau curl:
curl http://localhost:5000/api/predictions
```

### Test Frontend:
```
Buka browser: http://localhost:5000
Lihat tabel prediksi harian
```

## 📊 **Struktur Data JSON:**

```json
{
  "success": true,
  "data": {
    "dates": [
      "2025-01-02",
      "2025-01-03",
      "2025-01-04",
      ...
    ],
    "ayam_potong": [25.2, 25.8, 25.3, ...],
    "ayam_kampung": [12.7, 10.1, 12.6, ...],
    "ayam_tua": [7.0, 5.0, 5.3, ...],
    "notes": ["", "", "", ...]
  },
  "period": "2 Januari 2025 - 15 Januari 2025",
  "message": "Prediksi berlaku untuk 14 hari ke depan..."
}
```

## ✅ **Kesimpulan:**

Data prediksi harian di dashboard Anda berasal dari:

1. **Model ARIMA(2,1,2)** yang di-train dengan data historis 2024
2. **Diproses oleh** `arima_predictor.py`
3. **Dikirim via API** `/api/predictions` oleh Flask
4. **Ditampilkan oleh** JavaScript di frontend
5. **Hasil:** Tabel prediksi harian yang bervariasi dan realistis

Variasi yang Anda lihat (25.2 → 25.8 → 25.3) adalah **hasil natural dari model ARIMA** yang menangkap pola data historis! 🎉

---

**Note:** Jika ingin variasi lebih natural lagi, install `pmdarima` untuk auto-tuning parameter ARIMA optimal.
