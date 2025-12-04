"""
SARIMAX Predictor Module
Modul untuk generate prediksi 7 hari menggunakan model SARIMAX
Model: SARIMAX(1,1,1)(1,1,1,7) dengan exogenous variables
"""

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')


# ========================
# CONFIG
# ========================
FORECAST_DAYS = 7

CALENDAR_BASE_COLS = [
    "is_closed",
    "dow",
    "is_weekend",
    "is_event",
    "pre_event_peak",
    "restock_flag",
]


class SARIMAXPredictor:
    """Class untuk prediksi menggunakan SARIMAX"""
    
    def __init__(self, data_path='data'):
        self.data_path = data_path
        self.models = {}
        self.model_params = {
            'ayam_potong': {
                'filename': 'sarimax_ap_clean.csv',
                'column': 'sales',
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 7)
            },
            'ayam_kampung': {
                'filename': 'sarimax_ak_clean.csv',
                'column': 'sales',
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 7)
            },
            'ayam_tua': {
                'filename': 'sarimax_at_clean.csv',
                'column': 'sales',
                'order': (1, 1, 1),
                'seasonal_order': (1, 1, 1, 7)
            }
        }
        
    def load_data(self, filename, column_name):
        """Load data dari CSV"""
        try:
            df = pd.read_csv(f'{self.data_path}/{filename}')
            # Parse date dengan format M/D/YYYY
            df['date'] = pd.to_datetime(df['date'], format='%m/%d/%Y')
            df = df.set_index('date').sort_index()
            df = df.asfreq('D')
            # Kolom sales sudah ada di file SARIMAX baru
            df['sales'] = df[column_name].fillna(0)
            return df
        except Exception as e:
            print(f"Error loading {filename}: {e}")
            return None
    
    def prepare_features(self, df):
        """Build lag, MA, smoothing, log transform"""
        q_high = df['sales'].quantile(0.98)
        df['sales_smooth'] = df['sales'].clip(lower=0, upper=q_high)
        df['sales_log'] = np.log1p(df['sales_smooth'])
        
        for lag in [1, 3, 7]:
            df[f'lag{lag}'] = df['sales_smooth'].shift(lag)
        
        df['ma3'] = df['sales_smooth'].rolling(3, min_periods=1).mean()
        df['ma7'] = df['sales_smooth'].rolling(7, min_periods=1).mean()
        
        # Ensure calendar columns exist
        for col in CALENDAR_BASE_COLS:
            if col not in df.columns:
                df[col] = 0
        
        df_model = df.dropna().copy()
        return df_model, q_high
    
    def generate_future_calendar(self, last_date, days=7):
        """Generate calendar features untuk future dates"""
        future_dates = pd.date_range(
            start=last_date + timedelta(days=1),
            periods=days,
            freq='D'
        )
        
        calendar_data = []
        for date in future_dates:
            dow = date.dayofweek
            is_weekend = 1 if dow >= 4 else 0  # Jumat=4, Sabtu=5
            
            # Simple heuristic untuk event/closed
            is_closed = 0
            is_event = 0
            pre_event_peak = 0
            restock_flag = 0
            
            calendar_data.append({
                'date': date,
                'is_closed': is_closed,
                'dow': dow,
                'is_weekend': is_weekend,
                'is_event': is_event,
                'pre_event_peak': pre_event_peak,
                'restock_flag': restock_flag
            })
        
        return pd.DataFrame(calendar_data).set_index('date')
    
    def train_and_forecast(self, df, order, seasonal_order, steps=7):
        """Train SARIMAX model dan generate forecast"""
        try:
            df_model, q_high = self.prepare_features(df)
            exog_cols = CALENDAR_BASE_COLS + ['lag1', 'lag3', 'lag7', 'ma3', 'ma7']
            
            y_train = df_model['sales_log']
            X_train = df_model[exog_cols]
            
            # Build dan fit model SARIMAX
            model = SARIMAX(
                endog=y_train,
                exog=X_train,
                order=order,
                seasonal_order=seasonal_order,
                enforce_stationarity=False,
                enforce_invertibility=False,
            )
            
            res = model.fit(disp=False, maxiter=300)
            
            # Generate future calendar
            last_date = df_model.index.max()
            cal_future = self.generate_future_calendar(last_date, steps)
            
            # Dynamic forecasting
            results = []
            last_df = df_model.copy()
            
            for current_date, row in cal_future.iterrows():
                cal_vals = {col: int(row[col]) for col in CALENDAR_BASE_COLS}
                
                lag1 = last_df['sales_smooth'].iloc[-1]
                lag3 = last_df['sales_smooth'].iloc[-3]
                lag7 = last_df['sales_smooth'].iloc[-7]
                ma3 = last_df['sales_smooth'].rolling(3).mean().iloc[-1]
                ma7 = last_df['sales_smooth'].rolling(7).mean().iloc[-1]
                
                exog_row = pd.DataFrame(
                    {
                        **cal_vals,
                        'lag1': [lag1],
                        'lag3': [lag3],
                        'lag7': [lag7],
                        'ma3': [ma3],
                        'ma7': [ma7],
                    },
                    index=[current_date],
                )
                
                # Forecast
                log_pred = res.forecast(steps=1, exog=exog_row[exog_cols])
                y_hat = np.expm1(log_pred.iloc[0])
                y_hat = max(0, y_hat)
                y_hat = min(y_hat, q_high * 1.8)
                
                results.append((current_date, y_hat))
                
                # Update last_df untuk iterasi berikutnya
                last_df.loc[current_date] = {
                    'sales': y_hat,
                    'sales_smooth': min(y_hat, q_high),
                    'sales_log': np.log1p(min(y_hat, q_high)),
                    **cal_vals,
                    'lag1': lag1,
                    'lag3': lag3,
                    'lag7': lag7,
                    'ma3': ma3,
                    'ma7': ma7,
                }
            
            # Convert to Series
            forecast_dates = [r[0] for r in results]
            forecast_values = [r[1] for r in results]
            
            return pd.Series(forecast_values, index=forecast_dates)
            
        except Exception as e:
            print(f"Error in train_and_forecast: {e}")
            return None
    
    def predict_all_categories(self, start_date=None, days=7):
        """
        Generate prediksi untuk semua kategori ayam
        
        Args:
            start_date: tanggal mulai prediksi (default: hari ini + 1)
            days: jumlah hari prediksi (default: 7)
            
        Returns:
            dict dengan prediksi untuk setiap kategori
        """
        if start_date is None:
            start_date = datetime.now() + timedelta(days=1)
        
        predictions = {
            'dates': [],
            'ayam_potong': [],
            'ayam_kampung': [],
            'ayam_tua': [],
        }
        
        # Generate prediksi untuk setiap kategori
        for key, params in self.model_params.items():
            df = self.load_data(params['filename'], params['column'])
            
            if df is not None:
                forecast = self.train_and_forecast(
                    df,
                    order=params['order'],
                    seasonal_order=params['seasonal_order'],
                    steps=days
                )
                
                if forecast is not None:
                    if len(predictions['dates']) == 0:
                        predictions['dates'] = [d.strftime('%Y-%m-%d') for d in forecast.index]
                    
                    values = [max(0, float(v)) for v in forecast.values]
                    predictions[key] = values
                else:
                    # Fallback ke rata-rata jika gagal
                    avg = df['sales'].tail(14).mean()
                    predictions[key] = [float(avg)] * days
            else:
                # Fallback jika data tidak bisa diload
                predictions[key] = [0.0] * days
        
        # Ensure dates are populated
        if len(predictions['dates']) == 0:
            prediction_dates = [start_date + timedelta(days=i) for i in range(days)]
            predictions['dates'] = [d.strftime('%Y-%m-%d') for d in prediction_dates]
        
        return predictions


def get_predictions(start_date=None, days=7):
    """
    Helper function untuk mendapatkan prediksi
    
    Args:
        start_date: tanggal mulai prediksi (default: besok)
        days: jumlah hari prediksi (default: 7)
        
    Returns:
        dict dengan prediksi
    """
    predictor = SARIMAXPredictor()
    return predictor.predict_all_categories(start_date, days)


if __name__ == "__main__":
    # Test predictor
    print("Testing SARIMAX Predictor...")
    print("Model: SARIMAX(1,1,1)(1,1,1,7) dengan exogenous variables\n")
    predictions = get_predictions()
    
    print(f"Prediksi untuk {len(predictions['dates'])} hari:")
    print(f"Tanggal: {predictions['dates'][0]} - {predictions['dates'][-1]}")
    print(f"\nAyam Potong (rata-rata): {sum(predictions['ayam_potong'])/len(predictions['ayam_potong']):.2f} kg/hari")
    print(f"Ayam Kampung (rata-rata): {sum(predictions['ayam_kampung'])/len(predictions['ayam_kampung']):.2f} kg/hari")
    print(f"Ayam Tua (rata-rata): {sum(predictions['ayam_tua'])/len(predictions['ayam_tua']):.2f} kg/hari")
    
    print(f"\nDetail prediksi:")
    for i, date in enumerate(predictions['dates']):
        print(f"{date}: AP={predictions['ayam_potong'][i]:.2f}, AK={predictions['ayam_kampung'][i]:.2f}, AT={predictions['ayam_tua'][i]:.2f}")
