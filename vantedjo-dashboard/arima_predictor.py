"""
ARIMA Predictor Module
Modul untuk generate prediksi 14 hari menggunakan model ARIMA
"""

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


class ARIMAPredictor:
    """Class untuk prediksi menggunakan ARIMA"""
    
    def __init__(self, data_path='notebooks/processed_for_model'):
        self.data_path = data_path
        self.models = {}
        
    def load_data(self, filename, column_name):
        """Load data dari CSV"""
        try:
            df = pd.read_csv(f'{self.data_path}/{filename}', parse_dates=['date'])
            df = df.set_index('date').sort_index()
            return df[column_name]
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def train_and_forecast(self, series, order=(1, 1, 1), steps=14):
        """
        Train model ARIMA dan generate forecast
        
        Args:
            series: pandas Series dengan data time series
            order: tuple (p, d, q) untuk ARIMA
            steps: jumlah hari untuk forecast
            
        Returns:
            pandas Series dengan forecast values
        """
        try:
            # Build dan fit model ARIMA
            model = ARIMA(series, order=order)
            model_fit = model.fit()
            
            # Forecast
            forecast_values = model_fit.forecast(steps=steps)
            
            # Buat index tanggal untuk forecast
            last_date = series.index.max()
            future_dates = pd.date_range(
                start=last_date + pd.Timedelta(days=1),
                periods=steps,
                freq='D'
            )
            
            # Return sebagai Series
            forecast_series = pd.Series(
                forecast_values.values,
                index=future_dates
            )
            
            return forecast_series
            
        except Exception as e:
            print(f"Error in train_and_forecast: {e}")
            return None
    
    def predict_all_categories(self, start_date=None, days=14):
        """
        Generate prediksi untuk semua kategori ayam
        
        Args:
            start_date: tanggal mulai prediksi (default: 1 Jan 2025)
            days: jumlah hari prediksi (default: 14)
            
        Returns:
            dict dengan prediksi untuk setiap kategori
        """
        if start_date is None:
            start_date = datetime(2025, 1, 1)
        
        # Load data untuk setiap kategori
        data_configs = [
            {
                'filename': 'ts_ayam_potong_clean.csv',
                'column': 'Ayam_Potong',
                'key': 'ayam_potong',
                'order': (1, 1, 1)  # ARIMA order untuk Ayam Potong
            },
            {
                'filename': 'ts_ayam_kampung_clean.csv',
                'column': 'Ayam_Kampung',
                'key': 'ayam_kampung',
                'order': (1, 1, 1)  # ARIMA order untuk Ayam Kampung
            },
            {
                'filename': 'ts_ayam_tua_clean.csv',
                'column': 'Ayam_Tua',
                'key': 'ayam_tua',
                'order': (1, 1, 1)  # ARIMA order untuk Ayam Tua
            }
        ]
        
        predictions = {
            'dates': [],
            'ayam_potong': [],
            'ayam_kampung': [],
            'ayam_tua': []
        }
        
        # Generate tanggal prediksi
        prediction_dates = [start_date + timedelta(days=i) for i in range(days)]
        predictions['dates'] = [d.strftime('%Y-%m-%d') for d in prediction_dates]
        
        # Generate prediksi untuk setiap kategori
        for config in data_configs:
            series = self.load_data(config['filename'], config['column'])
            
            if series is not None:
                forecast = self.train_and_forecast(
                    series, 
                    order=config['order'], 
                    steps=days
                )
                
                if forecast is not None:
                    # Ambil nilai prediksi dan pastikan tidak negatif
                    values = [max(0, float(v)) for v in forecast.values]
                    predictions[config['key']] = values
                else:
                    # Fallback ke rata-rata jika gagal
                    avg = series.tail(14).mean()
                    predictions[config['key']] = [float(avg)] * days
            else:
                # Fallback jika data tidak bisa diload
                predictions[config['key']] = [0.0] * days
        
        return predictions


def get_predictions(start_date=None, days=14):
    """
    Helper function untuk mendapatkan prediksi
    
    Args:
        start_date: tanggal mulai prediksi
        days: jumlah hari prediksi
        
    Returns:
        dict dengan prediksi
    """
    predictor = ARIMAPredictor()
    return predictor.predict_all_categories(start_date, days)


if __name__ == "__main__":
    # Test predictor
    print("Testing ARIMA Predictor...")
    predictions = get_predictions()
    
    print(f"\nPrediksi untuk {len(predictions['dates'])} hari:")
    print(f"Tanggal: {predictions['dates'][0]} - {predictions['dates'][-1]}")
    print(f"\nAyam Potong (rata-rata): {sum(predictions['ayam_potong'])/len(predictions['ayam_potong']):.2f} kg/hari")
    print(f"Ayam Kampung (rata-rata): {sum(predictions['ayam_kampung'])/len(predictions['ayam_kampung']):.2f} kg/hari")
    print(f"Ayam Tua (rata-rata): {sum(predictions['ayam_tua'])/len(predictions['ayam_tua']):.2f} kg/hari")
