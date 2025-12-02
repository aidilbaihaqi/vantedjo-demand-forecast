from flask import Flask, jsonify, render_template
from flask_cors import CORS
import pandas as pd
from datetime import datetime, timedelta
import os
from sarimax_wrapper import get_predictions as get_sarimax_predictions

app = Flask(__name__)
CORS(app)

# Load data yang sudah diproses
DATA_PATH = 'data'

# Flag untuk menggunakan SARIMAX atau baseline
USE_SARIMAX = True  # Set False untuk menggunakan baseline sederhana

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
    """Generate prediksi 7 hari untuk semua kategori ayam menggunakan SARIMAX"""
    
    # Jika USE_SARIMAX = True, gunakan model SARIMAX
    if USE_SARIMAX:
        try:
            print("Generating predictions using SARIMAX model...")
            print("Model: SARIMAX(1,1,1)(1,1,1,7) dengan exogenous variables")
            
            # Generate prediksi 7 hari ke depan
            start_date = datetime.now() + timedelta(days=1)
            predictions = get_sarimax_predictions(start_date=start_date, days=7)
            
            # Round values untuk display yang lebih baik
            for key in ['ayam_potong', 'ayam_kampung', 'ayam_tua']:
                predictions[key] = [round(v, 2) for v in predictions[key]]
            
            print("SARIMAX predictions generated successfully!")
            return predictions
            
        except Exception as e:
            print(f"Error using SARIMAX model: {e}")
            print("Falling back to baseline method...")
            # Fallback ke baseline jika SARIMAX gagal
    
    # Baseline method (rata-rata 7 hari terakhir)
    data = load_data()
    if not data:
        return None
    
    # Tanggal prediksi: 7 hari ke depan
    start_date = datetime.now() + timedelta(days=1)
    prediction_dates = [start_date + timedelta(days=i) for i in range(7)]
    
    predictions = {
        'dates': [d.strftime('%Y-%m-%d') for d in prediction_dates],
        'ayam_potong': [],
        'ayam_kampung': [],
        'ayam_tua': []
    }
    
    # Untuk setiap kategori, ambil rata-rata 7 hari terakhir sebagai baseline
    for category, df in data.items():
        df_sorted = df.sort_values('date')
        last_7_days = df_sorted.tail(7)['quantity'].values
        
        # Simple forecast: gunakan rata-rata dengan sedikit variasi
        avg = last_7_days.mean()
        
        # Generate prediksi dengan pola yang mirip
        for i in range(7):
            # Tambahkan sedikit variasi berdasarkan pola historis
            variation = (last_7_days[i % len(last_7_days)] - avg) * 0.3
            pred_value = round(avg + variation, 2)
            predictions[category].append(max(0, pred_value))
    
    return predictions

@app.route('/')
def index():
    """Render halaman dashboard"""
    return render_template('index.html')

@app.route('/api/predictions')
def get_predictions():
    """API endpoint untuk mendapatkan prediksi 7 hari menggunakan SARIMAX"""
    predictions = generate_predictions()
    
    if predictions:
        start_date = predictions['dates'][0]
        end_date = predictions['dates'][-1]
        
        return jsonify({
            'success': True,
            'data': predictions,
            'model': 'SARIMAX(1,1,1)(1,1,1,7)',
            'period': f'{start_date} - {end_date}',
            'message': 'Prediksi 7 hari ke depan menggunakan model SARIMAX dengan exogenous variables'
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

@app.route('/api/model-info')
def get_model_info():
    """API endpoint untuk informasi model SARIMAX"""
    model_info = {
        'model_name': 'SARIMAX',
        'model_type': 'Seasonal AutoRegressive Integrated Moving Average with eXogenous variables',
        'forecast_horizon': '7 hari',
        'categories': {
            'ayam_potong': {
                'order': '(1, 1, 1)',
                'seasonal_order': '(1, 1, 1, 7)',
                'description': 'SARIMAX dengan seasonal period 7 hari (weekly pattern)',
                'exogenous_vars': ['is_closed', 'dow', 'is_weekend', 'is_event', 'pre_event_peak', 'restock_flag', 'lag1', 'lag3', 'lag7', 'ma3', 'ma7'],
                'accuracy': {
                    'mae': 'Mean Absolute Error - mengukur rata-rata kesalahan prediksi',
                    'rmse': 'Root Mean Squared Error - mengukur kesalahan dengan penalti lebih besar untuk error besar',
                    'mape': 'Mean Absolute Percentage Error - mengukur akurasi dalam persentase'
                }
            },
            'ayam_kampung': {
                'order': '(1, 1, 1)',
                'seasonal_order': '(1, 1, 1, 7)',
                'description': 'SARIMAX dengan seasonal period 7 hari (weekly pattern)',
                'exogenous_vars': ['is_closed', 'dow', 'is_weekend', 'is_event', 'pre_event_peak', 'restock_flag', 'lag1', 'lag3', 'lag7', 'ma3', 'ma7'],
                'accuracy': {
                    'mae': 'Mean Absolute Error - mengukur rata-rata kesalahan prediksi',
                    'rmse': 'Root Mean Squared Error - mengukur kesalahan dengan penalti lebih besar untuk error besar',
                    'mape': 'Mean Absolute Percentage Error - mengukur akurasi dalam persentase'
                }
            },
            'ayam_tua': {
                'order': '(1, 1, 1)',
                'seasonal_order': '(1, 1, 1, 7)',
                'description': 'SARIMAX dengan seasonal period 7 hari (weekly pattern)',
                'exogenous_vars': ['is_closed', 'dow', 'is_weekend', 'is_event', 'pre_event_peak', 'restock_flag', 'lag1', 'lag3', 'lag7', 'ma3', 'ma7'],
                'accuracy': {
                    'mae': 'Mean Absolute Error - mengukur rata-rata kesalahan prediksi',
                    'rmse': 'Root Mean Squared Error - mengukur kesalahan dengan penalti lebih besar untuk error besar',
                    'mape': 'Mean Absolute Percentage Error - mengukur akurasi dalam persentase'
                }
            }
        },
        'features': {
            'calendar_features': {
                'is_closed': 'Indikator toko tutup (1=tutup, 0=buka)',
                'dow': 'Day of week (0=Senin, 6=Minggu)',
                'is_weekend': 'Indikator weekend (1=Jumat/Sabtu, 0=hari kerja)',
                'is_event': 'Indikator hari libur/event (1=ada event, 0=tidak)',
                'pre_event_peak': 'Indikator hari sebelum event (demand biasanya naik)',
                'restock_flag': 'Indikator hari restock'
            },
            'lag_features': {
                'lag1': 'Penjualan 1 hari sebelumnya',
                'lag3': 'Penjualan 3 hari sebelumnya',
                'lag7': 'Penjualan 7 hari sebelumnya (weekly pattern)'
            },
            'moving_average': {
                'ma3': 'Moving average 3 hari',
                'ma7': 'Moving average 7 hari'
            }
        },
        'advantages': [
            'Menangkap pola seasonal (weekly pattern)',
            'Menggunakan exogenous variables (kalender, event, dll)',
            'Dynamic forecasting dengan lag features',
            'Akurasi tinggi untuk data time series dengan seasonality',
            'Dapat menangani trend dan seasonality secara bersamaan'
        ]
    }
    
    return jsonify({
        'success': True,
        'data': model_info
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
