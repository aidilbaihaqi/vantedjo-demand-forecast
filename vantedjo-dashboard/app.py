from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import os
from arima_predictor import get_predictions as get_arima_predictions

app = Flask(__name__)
CORS(app)

# Load data yang sudah diproses
DATA_PATH = 'data'

# Flag untuk menggunakan ARIMA atau baseline
USE_ARIMA = True  # Set False untuk menggunakan baseline sederhana

def load_data():
    """Load semua data time series yang sudah diproses"""
    try:
        df_ap = pd.read_csv(f'{DATA_PATH}/ts_ayam_potong_clean.csv', parse_dates=['date'])
        df_ak = pd.read_csv(f'{DATA_PATH}/ts_ayam_kampung_clean.csv', parse_dates=['date'])
        df_at = pd.read_csv(f'{DATA_PATH}/ts_ayam_tua_clean.csv', parse_dates=['date'])
        
        # Rename kolom untuk konsistensi
        df_ap.rename(columns={'Ayam_Potong': 'quantity'}, inplace=True)
        df_ak.rename(columns={'Ayam_Kampung': 'quantity'}, inplace=True)
        df_at.rename(columns={'Ayam_Tua': 'quantity'}, inplace=True)
        
        return {
            'ayam_potong': df_ap,
            'ayam_kampung': df_ak,
            'ayam_tua': df_at
        }
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def generate_predictions():
    """Generate prediksi 14 hari untuk semua kategori ayam"""
    
    # Jika USE_ARIMA = True, gunakan model ARIMA
    if USE_ARIMA:
        try:
            print("Generating predictions using ARIMA model...")
            # Mulai dari 2 Januari karena tgl 1 toko tutup
            start_date = datetime(2025, 1, 2)
            predictions = get_arima_predictions(start_date=start_date, days=14)
            
            # Round values untuk display yang lebih baik
            for key in ['ayam_potong', 'ayam_kampung', 'ayam_tua']:
                predictions[key] = [round(v, 2) for v in predictions[key]]
            
            print("ARIMA predictions generated successfully!")
            return predictions
            
        except Exception as e:
            print(f"Error using ARIMA model: {e}")
            print("Falling back to baseline method...")
            # Fallback ke baseline jika ARIMA gagal
    
    # Baseline method (rata-rata 14 hari terakhir)
    data = load_data()
    if not data:
        return None
    
    # Tanggal prediksi: 2-15 Januari 2025 (skip tgl 1 karena toko tutup)
    start_date = datetime(2025, 1, 2)
    prediction_dates = [start_date + timedelta(days=i) for i in range(14)]
    
    predictions = {
        'dates': [d.strftime('%Y-%m-%d') for d in prediction_dates],
        'ayam_potong': [],
        'ayam_kampung': [],
        'ayam_tua': []
    }
    
    # Untuk setiap kategori, ambil rata-rata 14 hari terakhir sebagai baseline
    for category, df in data.items():
        df_sorted = df.sort_values('date')
        last_14_days = df_sorted.tail(14)['quantity'].values
        
        # Simple forecast: gunakan rata-rata dengan sedikit variasi
        avg = last_14_days.mean()
        std = last_14_days.std()
        
        # Generate prediksi dengan pola yang mirip
        for i in range(14):
            # Tambahkan sedikit variasi berdasarkan pola historis
            variation = (last_14_days[i % len(last_14_days)] - avg) * 0.3
            pred_value = round(avg + variation, 2)
            predictions[category].append(max(0, pred_value))
    
    return predictions

@app.route('/')
def index():
    """Render halaman dashboard"""
    return render_template('index.html')

@app.route('/api/predictions')
def get_predictions():
    """API endpoint untuk mendapatkan prediksi 14 hari"""
    predictions = generate_predictions()
    
    if predictions:
        return jsonify({
            'success': True,
            'data': predictions,
            'period': '2 Januari 2025 - 15 Januari 2025',
            'message': 'Prediksi berlaku untuk 14 hari ke depan (tanggal 1 Januari di-skip karena toko tutup)'
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Gagal memuat data'
        }), 500

@app.route('/api/historical')
def get_historical():
    """API endpoint untuk data historis (30 hari terakhir)"""
    data = load_data()
    if not data:
        return jsonify({'success': False, 'message': 'Gagal memuat data'}), 500
    
    historical = {
        'dates': [],
        'ayam_potong': [],
        'ayam_kampung': [],
        'ayam_tua': []
    }
    
    # Ambil 30 hari terakhir dari setiap kategori
    for category, df in data.items():
        df_sorted = df.sort_values('date').tail(30)
        if len(historical['dates']) == 0:
            historical['dates'] = df_sorted['date'].dt.strftime('%Y-%m-%d').tolist()
        historical[category] = df_sorted['quantity'].tolist()
    
    return jsonify({
        'success': True,
        'data': historical
    })

@app.route('/api/stats')
def get_stats():
    """API endpoint untuk statistik ringkasan"""
    data = load_data()
    if not data:
        return jsonify({'success': False, 'message': 'Gagal memuat data'}), 500
    
    stats = {}
    for category, df in data.items():
        stats[category] = {
            'total': int(df['quantity'].sum()),
            'average': round(df['quantity'].mean(), 2),
            'max': int(df['quantity'].max()),
            'min': int(df['quantity'].min())
        }
    
    return jsonify({
        'success': True,
        'data': stats
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
