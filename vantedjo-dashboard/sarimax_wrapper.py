"""
SARIMAX Wrapper
Wrapper untuk menggunakan model SARIMAX asli dari notebooks/model/
"""

import sys
import os

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

# Import model functions
from model_sarimax_ap import main as forecast_ayam_potong
from model_sarimax_ak import main as forecast_ayam_kampung
from model_sarimax_at import main as forecast_ayam_tua


def get_predictions(start_date=None, days=7):
    """
    Get predictions dari model SARIMAX asli
    
    Returns:
        dict dengan prediksi untuk setiap kategori
    """
    print("🔄 Running SARIMAX models...")
    
    # Run model untuk setiap kategori
    print("\n📊 Ayam Potong...")
    results_ap = forecast_ayam_potong()
    
    print("\n📊 Ayam Kampung...")
    results_ak = forecast_ayam_kampung()
    
    print("\n📊 Ayam Tua...")
    results_at = forecast_ayam_tua()
    
    # Format results
    predictions = {
        'dates': [],
        'ayam_potong': [],
        'ayam_kampung': [],
        'ayam_tua': []
    }
    
    # Extract dates and values
    for (date_ap, val_ap), (date_ak, val_ak), (date_at, val_at) in zip(results_ap, results_ak, results_at):
        predictions['dates'].append(date_ap.strftime('%Y-%m-%d'))
        predictions['ayam_potong'].append(round(val_ap, 2))
        predictions['ayam_kampung'].append(round(val_ak, 2))
        predictions['ayam_tua'].append(round(val_at, 2))
    
    print("\n✅ Predictions generated successfully!")
    return predictions


if __name__ == "__main__":
    # Test wrapper
    print("Testing SARIMAX Wrapper...")
    predictions = get_predictions()
    
    print(f"\n📊 Prediksi untuk {len(predictions['dates'])} hari:")
    print(f"Tanggal: {predictions['dates'][0]} - {predictions['dates'][-1]}")
    print(f"\nAyam Potong (rata-rata): {sum(predictions['ayam_potong'])/len(predictions['ayam_potong']):.2f} kg/hari")
    print(f"Ayam Kampung (rata-rata): {sum(predictions['ayam_kampung'])/len(predictions['ayam_kampung']):.2f} kg/hari")
    print(f"Ayam Tua (rata-rata): {sum(predictions['ayam_tua'])/len(predictions['ayam_tua']):.2f} kg/hari")
    
    print(f"\nDetail prediksi:")
    for i, date in enumerate(predictions['dates']):
        print(f"{date}: AP={predictions['ayam_potong'][i]:.2f}, AK={predictions['ayam_kampung'][i]:.2f}, AT={predictions['ayam_tua'][i]:.2f}")
