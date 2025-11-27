"""
Evaluasi Model ARIMA(2,1,2) untuk Forecasting Kios Vantedjo
Menghitung MAE, RMSE, dan MAPE untuk ketiga jenis ayam
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def calculate_mape(y_true, y_pred):
    """
    Menghitung Mean Absolute Percentage Error (MAPE)
    
    MAPE = (1/n) * Σ|((y_true - y_pred) / y_true)| * 100
    
    Args:
        y_true: Nilai aktual
        y_pred: Nilai prediksi
    
    Returns:
        MAPE dalam persentase
    """
    # Hindari pembagian dengan nol
    mask = y_true != 0
    return np.mean(np.abs((y_true[mask] - y_pred[mask]) / y_true[mask])) * 100


def evaluate_arima_model(data_path, column_name, category_name):
    """
    Evaluasi model ARIMA(2,1,2) dengan train-test split
    
    Args:
        data_path: Path ke file CSV
        column_name: Nama kolom data
        category_name: Nama kategori (untuk display)
    
    Returns:
        Dictionary berisi metrik evaluasi
    """
    print(f"\n{'='*70}")
    print(f"EVALUASI MODEL ARIMA(2,1,2) - {category_name.upper()}")
    print(f"{'='*70}\n")
    
    # 1. Load data
    df = pd.read_csv(data_path, parse_dates=['date'])
    df = df.set_index('date').sort_index()
    series = df[column_name]
    
    print(f"Total data: {len(series)} hari")
    print(f"Periode: {series.index[0].strftime('%Y-%m-%d')} s/d {series.index[-1].strftime('%Y-%m-%d')}")
    
    # 2. Split data: 80% training, 20% testing
    train_size = int(len(series) * 0.8)
    train_data = series[:train_size]
    test_data = series[train_size:]
    
    print(f"\nData Training: {len(train_data)} hari ({train_size/len(series)*100:.1f}%)")
    print(f"Data Testing: {len(test_data)} hari ({len(test_data)/len(series)*100:.1f}%)")
    
    # 3. Build dan fit model ARIMA(2,1,2)
    print("\n[INFO] Training model ARIMA(2,1,2)...")
    model = ARIMA(train_data, order=(2, 1, 2))
    model_fit = model.fit()
    
    print("[INFO] Model berhasil di-training!")
    
    # 4. Prediksi untuk periode testing
    print(f"[INFO] Melakukan prediksi untuk {len(test_data)} hari...")
    predictions = model_fit.forecast(steps=len(test_data))
    
    # 5. Hitung metrik evaluasi
    y_true = test_data.values
    y_pred = predictions.values
    
    # MAE (Mean Absolute Error)
    mae = mean_absolute_error(y_true, y_pred)
    
    # RMSE (Root Mean Squared Error)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    
    # MAPE (Mean Absolute Percentage Error)
    mape = calculate_mape(y_true, y_pred)
    
    # Statistik tambahan
    mean_actual = np.mean(y_true)
    mean_predicted = np.mean(y_pred)
    
    # 6. Tampilkan hasil
    print(f"\n{'='*70}")
    print("HASIL EVALUASI MODEL")
    print(f"{'='*70}")
    print(f"\n📊 METRIK EVALUASI:")
    print(f"   MAE (Mean Absolute Error)      : {mae:.4f} kg")
    print(f"   RMSE (Root Mean Squared Error) : {rmse:.4f} kg")
    print(f"   MAPE (Mean Absolute % Error)   : {mape:.2f}%")
    
    print(f"\n📈 STATISTIK DATA:")
    print(f"   Rata-rata Aktual               : {mean_actual:.2f} kg/hari")
    print(f"   Rata-rata Prediksi             : {mean_predicted:.2f} kg/hari")
    print(f"   Selisih Rata-rata              : {abs(mean_actual - mean_predicted):.2f} kg")
    
    # 7. Interpretasi hasil
    print(f"\n💡 INTERPRETASI:")
    
    # Interpretasi MAE
    print(f"\n   MAE = {mae:.2f} kg")
    print(f"   → Rata-rata error prediksi adalah {mae:.2f} kg per hari")
    print(f"   → Model meleset sekitar {mae:.2f} kg dari nilai aktual")
    
    # Interpretasi RMSE
    print(f"\n   RMSE = {rmse:.2f} kg")
    print(f"   → RMSE lebih besar dari MAE, menunjukkan ada beberapa error besar")
    print(f"   → Model lebih sensitif terhadap outlier")
    
    # Interpretasi MAPE
    print(f"\n   MAPE = {mape:.2f}%")
    if mape < 10:
        akurasi = "SANGAT BAIK"
        keterangan = "Model sangat akurat"
    elif mape < 20:
        akurasi = "BAIK"
        keterangan = "Model cukup akurat untuk forecasting"
    elif mape < 30:
        akurasi = "CUKUP"
        keterangan = "Model masih dapat diterima"
    else:
        akurasi = "KURANG"
        keterangan = "Model perlu perbaikan"
    
    print(f"   → Akurasi Model: {akurasi}")
    print(f"   → {keterangan}")
    print(f"   → Error rata-rata {mape:.2f}% dari nilai aktual")
    
    # 8. Visualisasi
    plt.figure(figsize=(14, 6))
    
    # Plot data aktual vs prediksi
    plt.plot(test_data.index, y_true, label='Aktual', marker='o', markersize=4, linewidth=2)
    plt.plot(test_data.index, y_pred, label='Prediksi ARIMA(2,1,2)', 
             marker='s', markersize=4, linewidth=2, linestyle='--', alpha=0.8)
    
    plt.title(f'Perbandingan Aktual vs Prediksi - {category_name}\n'
              f'MAE={mae:.2f} kg | RMSE={rmse:.2f} kg | MAPE={mape:.2f}%',
              fontsize=14, fontweight='bold')
    plt.xlabel('Tanggal', fontsize=12)
    plt.ylabel('Jumlah (kg)', fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Simpan plot
    output_file = f'evaluasi_{category_name.lower().replace(" ", "_")}.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n📁 Grafik disimpan: {output_file}")
    plt.close()
    
    # 9. Return hasil
    return {
        'category': category_name,
        'mae': mae,
        'rmse': rmse,
        'mape': mape,
        'mean_actual': mean_actual,
        'mean_predicted': mean_predicted,
        'train_size': len(train_data),
        'test_size': len(test_data),
        'accuracy': akurasi
    }


def create_comparison_table(results):
    """
    Membuat tabel perbandingan hasil evaluasi semua kategori
    
    Args:
        results: List of dictionaries berisi hasil evaluasi
    """
    print(f"\n\n{'='*90}")
    print("RINGKASAN EVALUASI SEMUA KATEGORI AYAM")
    print(f"{'='*90}\n")
    
    # Header tabel
    print(f"{'Kategori':<20} {'MAE (kg)':<15} {'RMSE (kg)':<15} {'MAPE (%)':<15} {'Akurasi':<15}")
    print(f"{'-'*90}")
    
    # Data tabel
    for result in results:
        print(f"{result['category']:<20} "
              f"{result['mae']:<15.4f} "
              f"{result['rmse']:<15.4f} "
              f"{result['mape']:<15.2f} "
              f"{result['accuracy']:<15}")
    
    print(f"{'-'*90}")
    
    # Rata-rata
    avg_mae = np.mean([r['mae'] for r in results])
    avg_rmse = np.mean([r['rmse'] for r in results])
    avg_mape = np.mean([r['mape'] for r in results])
    
    print(f"{'RATA-RATA':<20} "
          f"{avg_mae:<15.4f} "
          f"{avg_rmse:<15.4f} "
          f"{avg_mape:<15.2f}")
    
    print(f"\n{'='*90}\n")
    
    # Kesimpulan
    print("📋 KESIMPULAN EVALUASI MODEL ARIMA(2,1,2):\n")
    
    if avg_mape < 10:
        print("✅ Model SANGAT BAIK untuk semua kategori ayam")
        print("   → Dapat digunakan untuk forecasting dengan confidence tinggi")
    elif avg_mape < 20:
        print("✅ Model BAIK untuk forecasting")
        print("   → Akurasi cukup tinggi untuk perencanaan stok")
    elif avg_mape < 30:
        print("⚠️  Model CUKUP untuk forecasting")
        print("   → Perlu monitoring dan adjustment berkala")
    else:
        print("❌ Model KURANG AKURAT")
        print("   → Perlu perbaikan atau pertimbangkan model lain")
    
    print(f"\n💡 REKOMENDASI:")
    print(f"   • Gunakan model ini untuk perencanaan stok 14 hari ke depan")
    print(f"   • Monitor actual vs predicted secara berkala")
    print(f"   • Update model setiap bulan dengan data terbaru")
    print(f"   • Pertimbangkan faktor eksternal (hari libur, event khusus)")


def main():
    """
    Main function untuk menjalankan evaluasi semua kategori ayam
    """
    print("\n" + "="*90)
    print(" "*25 + "EVALUASI MODEL ARIMA(2,1,2)")
    print(" "*20 + "FORECASTING KIOS VANTEDJO")
    print("="*90)
    
    # Konfigurasi data
    data_configs = [
        {
            'path': 'notebooks/processed_for_model/ts_ayam_potong_clean.csv',
            'column': 'Ayam_Potong',
            'name': 'Ayam Potong'
        },
        {
            'path': 'notebooks/processed_for_model/ts_ayam_kampung_clean.csv',
            'column': 'Ayam_Kampung',
            'name': 'Ayam Kampung'
        },
        {
            'path': 'notebooks/processed_for_model/ts_ayam_tua_clean.csv',
            'column': 'Ayam_Tua',
            'name': 'Ayam Tua'
        }
    ]
    
    # Evaluasi setiap kategori
    results = []
    for config in data_configs:
        try:
            result = evaluate_arima_model(
                config['path'],
                config['column'],
                config['name']
            )
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error evaluasi {config['name']}: {str(e)}")
    
    # Tampilkan tabel perbandingan
    if results:
        create_comparison_table(results)
        
        # Simpan hasil ke CSV
        df_results = pd.DataFrame(results)
        df_results.to_csv('hasil_evaluasi_arima.csv', index=False)
        print(f"\n📁 Hasil evaluasi disimpan: hasil_evaluasi_arima.csv")
    
    print("\n" + "="*90)
    print("EVALUASI SELESAI!")
    print("="*90 + "\n")


if __name__ == "__main__":
    main()
