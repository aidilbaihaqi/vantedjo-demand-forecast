# Catatan Hari Libur / Toko Tutup

## Konfigurasi Saat Ini

Sistem prediksi sudah dikonfigurasi untuk **melewati tanggal 1 Januari** karena toko tutup pada hari tersebut.

### Perubahan yang Dilakukan:

1. **Tanggal Mulai Prediksi**: Diubah dari 1 Januari menjadi **2 Januari 2025**
2. **Periode Prediksi**: 2 Januari - 15 Januari 2025 (14 hari kerja)
3. **Tanggal yang Di-skip**: Otomatis melewati tanggal 1 Januari setiap tahun

## Cara Menambah Hari Libur Lainnya

Jika ada hari libur lain yang perlu di-skip, edit file `arima_predictor.py`:

### Contoh 1: Skip Tanggal Tertentu

```python
# Di function get_predictions()
skip_dates = ['2025-01-01', '2025-12-25', '2025-12-31']  # Tahun Baru, Natal, dll
predictions = get_predictions(skip_dates=skip_dates)
```

### Contoh 2: Skip Hari Minggu

Tambahkan logika di `predict_all_categories()`:

```python
while days_added < days:
    # Skip tanggal 1 Januari
    if current_date.month == 1 and current_date.day == 1:
        current_date += timedelta(days=1)
        continue
    
    # Skip hari Minggu (weekday() == 6)
    if current_date.weekday() == 6:
        current_date += timedelta(days=1)
        continue
    
    prediction_dates.append(current_date)
    days_added += 1
    current_date += timedelta(days=1)
```

### Contoh 3: Skip Hari Libur Nasional

```python
# Definisikan hari libur nasional
HARI_LIBUR = [
    '2025-01-01',  # Tahun Baru
    '2025-03-29',  # Idul Fitri (contoh)
    '2025-03-30',  # Idul Fitri (contoh)
    '2025-08-17',  # HUT RI
    '2025-12-25',  # Natal
]

# Di loop prediksi
if current_date.strftime('%Y-%m-%d') in HARI_LIBUR:
    current_date += timedelta(days=1)
    continue
```

## Testing

Untuk memverifikasi bahwa tanggal sudah benar:

```bash
python vantedjo-dashboard/arima_predictor.py
```

Output akan menampilkan:
- Tanggal mulai dan akhir prediksi
- Detail prediksi per tanggal
- Konfirmasi bahwa tanggal 1 Januari di-skip

## Catatan Penting

1. **Jumlah Hari**: Sistem tetap menghasilkan 14 prediksi, tapi tanggalnya disesuaikan dengan hari kerja
2. **Fleksibilitas**: Mudah ditambahkan hari libur lain sesuai kebutuhan
3. **Konsistensi**: Perubahan ini berlaku untuk semua jenis ayam (Potong, Kampung, Tua)
