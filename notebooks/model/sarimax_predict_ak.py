import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# ============================
# 1. Load dataset
# ============================
df = pd.read_csv("../processed_for_model/sarimax_ak_clean.csv")

# pastikan kolom date jadi datetime dan jadi index
df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

print("Shape awal:", df.shape)
print(df.head())

# ============================
# 2. Smoothing outlier (upper clip)
# ============================
# kita clip hanya sisi atas (biar zero / nilai kecil tetap apa adanya)
q_high = df['sales'].quantile(0.95)
df['sales_smooth'] = np.where(df['sales'] > q_high, q_high, df['sales'])

print("\nQuantile 95%:", q_high)
print("Contoh sebelum/sesudah smoothing:")
print(df[['sales', 'sales_smooth']].head(15))

# ============================
# 3. Log transform
# ============================
# log1p aman untuk nilai 0 (log(1 + x))
df['sales_log'] = np.log1p(df['sales_smooth'])

# ============================
# 4. Buat lag & moving average features
# ============================
for lag in [1, 3, 7]:
    df[f'lag{lag}'] = df['sales_smooth'].shift(lag)

df['ma3'] = df['sales_smooth'].rolling(window=3, min_periods=1).mean()
df['ma7'] = df['sales_smooth'].rolling(window=7, min_periods=1).mean()

# Buang baris awal yang masih ada NaN karena lag
df_model = df.dropna().copy()
print("\nShape setelah dropna (karena lag/MA):", df_model.shape)

# ============================
# 5. Train-test split (7 hari terakhir)
# ============================
# kita pakai 7 hari terakhir dari df_model sebagai test
train = df_model.iloc[:-7]
test = df_model.iloc[-7:]

exog_cols = [
    'is_closed',
    'dow',
    'is_weekend',
    'is_event',
    'pre_event_peak',
    'restock_flag',
    'lag1',
    'lag3',
    'lag7',
    'ma3',
    'ma7'
]

print("\nPeriode train:", train.index.min(), "→", train.index.max())
print("Periode test :", test.index.min(), "→", test.index.max())

# ============================
# 6. Build & fit SARIMAX di domain log
#    Model lebih sederhana: (0,1,1)x(0,1,1,7)
# ============================
model = SARIMAX(
    train['sales_log'],
    exog=train[exog_cols],
    order=(0, 1, 1),
    seasonal_order=(0, 1, 1, 7),
    enforce_stationarity=False,
    enforce_invertibility=False
).fit(disp=False)

print("\n===== SARIMAX Ayam Kampung (Improved) =====")
print(model.summary())

# ============================
# 7. Forecast 7 hari (di domain log, lalu balik ke skala asli)
# ============================
log_forecast = model.predict(
    start=test.index[0],
    end=test.index[-1],
    exog=test[exog_cols]
)

# balik dari log1p ke skala aslinya
forecast = np.expm1(log_forecast)

# ============================
# 8. Evaluation di skala asli (kg)
# ============================
y_true = test['sales']          # pakai original sales, bukan smoothed
y_pred = forecast

MAE = mean_absolute_error(y_true, y_pred)
RMSE = np.sqrt(mean_squared_error(y_true, y_pred))

# untuk MAPE, hati-hati dengan nilai 0 → kita ganti 0 dengan 0.1 agar tidak divide-by-zero
y_true_safe = np.where(y_true == 0, 0.1, y_true)
MAPE = np.mean(np.abs((y_true_safe - y_pred) / y_true_safe)) * 100

print("\n=== Evaluation Results (Ayam Kampung - Improved) ===")
print("MAE  :", MAE)
print("RMSE :", RMSE)
print("MAPE :", MAPE)

# ============================
# 9. Plot Actual vs Forecast
# ============================
plt.figure(figsize=(10, 5))
plt.plot(train['sales'][-21:], label="Recent Actual (Train)")
plt.plot(test['sales'], label="Actual (Test)", marker='o')
plt.plot(forecast, label="Forecast (7 days, improved)", marker='x')
plt.title("SARIMAX Improved - Ayam Kampung (7 hari)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
