"""
ARIMA Predictor Module
Modul untuk generate prediksi 14 hari menggunakan model ARIMA
Updated: Menggunakan parameter ARIMA yang lebih baik untuk variasi prediksi
"""

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Optional: Install pmdarima untuk auto ARIMA
# pip install pmdarima
try:
    from pmdarima import auto_arima
    AUTO_ARIMA_AVAILABLE = True
except ImportError:
    AUTO_ARIMA_AVAILABLE = False
    print("Note: pmdarima tidak terinstall. Menggunakan parameter manual.")


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
    
    def find_best_order(self, series):
        """
        Cari parameter ARIMA terbaik menggunakan auto_arima atau grid search
        
        Args:
            series: pandas Series dengan data time series
            
        Returns:
            tuple (p, d, q) terbaik
        """
        if AUTO_ARIMA_AVAILABLE:
            try:
                # Gunakan auto_arima untuk mencari parameter terbaik
                model = auto_arima(
                    series,
                    start_p=0, max_p=3,
                    start_q=0, max_q=3,
                    d=1,  # differencing order
                    seasonal=False,
                    trace=False,
                    error_action='ignore',
                    suppress_warnings=True,
                    stepwise=True
                )
                return model.order
            except:
                pass
        
        # Fallback: Gunakan parameter yang lebih baik dari (1,1,1)
        # Berdasarkan analisis data penjualan yang bervariasi
        return (2, 1, 2)  # ARIMA(2,1,2) lebih baik untuk data dengan variasi
    
    def train_and_forecast(self, series, order=None, steps=14):
        """
        Train model ARIMA dan generate forecast
        
        Args:
            series: pandas Series dengan data time series
            order: tuple (p, d, q) untuk ARIMA (None = auto detect)
            steps: jumlah hari untuk forecast
            
        Returns:
            pandas Series dengan forecast values
        """
        try:
            # Jika order tidak diberikan, cari yang terbaik
            if order is None:
                order = self.find_best_order(series)
                print(f"  Using ARIMA{order}")
            
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
    
    def predict_all_categories(self, start_date=None, days=14, skip_dates=None):
        """
        Generate prediksi untuk semua kategori ayam
        
        Args:
            start_date: tanggal mulai prediksi (default: 2 Jan 2025, skip tgl 1)
            days: jumlah hari prediksi (default: 14)
            skip_dates: list tanggal yang harus di-skip (toko tutup)
            
        Returns:
            dict dengan prediksi untuk setiap kategori
        """
        if start_date is None:
            # Mulai dari tanggal 2 Januari karena tgl 1 toko tutup
            start_date = datetime(2025, 1, 2)
        
        if skip_dates is None:
            # Default: skip tanggal 1 Januari setiap tahun
            skip_dates = []
        
        # Load data untuk setiap kategori
        # order=None akan auto-detect parameter terbaik
        data_configs = [
            {
                'filename': 'ts_ayam_potong_clean.csv',
                'column': 'Ayam_Potong',
                'key': 'ayam_potong',
                'order': None  # Auto-detect atau gunakan (2,1,2)
            },
            {
                'filename': 'ts_ayam_kampung_clean.csv',
                'column': 'Ayam_Kampung',
                'key': 'ayam_kampung',
                'order': None  # Auto-detect atau gunakan (2,1,2)
            },
            {
                'filename': 'ts_ayam_tua_clean.csv',
                'column': 'Ayam_Tua',
                'key': 'ayam_tua',
                'order': None  # Auto-detect atau gunakan (2,1,2)
            }
        ]
        
        predictions = {
            'dates': [],
            'ayam_potong': [],
            'ayam_kampung': [],
            'ayam_tua': [],
            'notes': []  # Catatan untuk tanggal tertentu (misal: toko tutup)
        }
        
        # Generate tanggal prediksi
        prediction_dates = []
        current_date = start_date
        days_added = 0
        
        while days_added < days:
            # Skip tanggal 1 Januari
            if current_date.month == 1 and current_date.day == 1:
                current_date += timedelta(days=1)
                continue
            
            # Skip tanggal yang ada di skip_dates
            if current_date.strftime('%Y-%m-%d') in skip_dates:
                current_date += timedelta(days=1)
                continue
            
            prediction_dates.append(current_date)
            days_added += 1
            current_date += timedelta(days=1)
        
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
                    
                    # Tambahkan catatan untuk setiap tanggal
                    for date in prediction_dates:
                        if date.month == 1 and date.day == 1:
                            predictions['notes'].append('Toko tutup')
                        else:
                            predictions['notes'].append('')
                else:
                    # Fallback ke rata-rata jika gagal
                    avg = series.tail(14).mean()
                    predictions[config['key']] = [float(avg)] * len(prediction_dates)
            else:
                # Fallback jika data tidak bisa diload
                predictions[config['key']] = [0.0] * len(prediction_dates)
        
        return predictions


def get_predictions(start_date=None, days=14, skip_dates=None):
    """
    Helper function untuk mendapatkan prediksi
    
    Args:
        start_date: tanggal mulai prediksi (default: 2 Jan 2025)
        days: jumlah hari prediksi
        skip_dates: list tanggal yang harus di-skip
        
    Returns:
        dict dengan prediksi
    """
    predictor = ARIMAPredictor()
    return predictor.predict_all_categories(start_date, days, skip_dates)


if __name__ == "__main__":
    # Test predictor
    print("Testing ARIMA Predictor...")
    print("Note: Tanggal 1 Januari di-skip karena toko tutup\n")
    predictions = get_predictions()
    
    print(f"Prediksi untuk {len(predictions['dates'])} hari:")
    print(f"Tanggal: {predictions['dates'][0]} - {predictions['dates'][-1]}")
    print(f"\nAyam Potong (rata-rata): {sum(predictions['ayam_potong'])/len(predictions['ayam_potong']):.2f} kg/hari")
    print(f"Ayam Kampung (rata-rata): {sum(predictions['ayam_kampung'])/len(predictions['ayam_kampung']):.2f} kg/hari")
    print(f"Ayam Tua (rata-rata): {sum(predictions['ayam_tua'])/len(predictions['ayam_tua']):.2f} kg/hari")
    
    print(f"\nDetail prediksi:")
    for i, date in enumerate(predictions['dates']):
        print(f"{date}: AP={predictions['ayam_potong'][i]:.2f}, AK={predictions['ayam_kampung'][i]:.2f}, AT={predictions['ayam_tua'][i]:.2f}")
