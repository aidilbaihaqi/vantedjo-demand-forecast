import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error
import matplotlib.pyplot as plt

# ============================
# 1. Load dataset ayam potong
# ============================
df = pd.read_csv("../processed_for_model/sarimax_ap_clean.csv")

df['date'] = pd.to_datetime(df['date'])
df = df.set_index('date')

print("Shape awal:", df.shape)

# ============================
# 2. Smoothing Outlier
# ============================
q_high = df['sales'].quantile(0.95)
df['sales_smooth'] = df['sales'].clip(upper=q_high)

print("Quantile 95%:", q_high)

# ============================
# 3. Log transform
# ============================
df['sales_log'] = np.log1p(df['sales_smooth'])

# ============================
# 4. Lag features
# ============================
for lag in [1, 3, 7]:
    df[f'lag{lag}'] = df['sales_smooth'].shift(lag)

df['ma3'] = df['sales_smooth'].rolling(3, min_periods=1).mean()
df['ma7'] = df['sales_smooth'].rolling(7, min_periods=1).mean()

# Drop NA
df_model = df.dropna()

# ============================
# 5. Train-test split (7 hari)
# ============================
train = df_model.iloc[:-7]
test = df_model.iloc[-7:]

exog_cols = [
    'is_closed','dow','is_weekend','is_event','pre_event_peak','restock_flag',
    'lag1','lag3','lag7','ma3','ma7'
]

# ============================
# 6. Fit SARIMAX
# ============================
model = SARIMAX(
    train['sales_log'],
    exog=train[exog_cols],
    order=(0,1,1),
    seasonal_order=(0,1,1,7),
    enforce_stationarity=False,
    enforce_invertibility=False
).fit()

print(model.summary())

# ============================
# 7. Forecast
# ============================
log_pred = model.predict(
    start=test.index[0],
    end=test.index[-1],
    exog=test[exog_cols]
)

pred = np.expm1(log_pred)

# ============================
# 8. Evaluation
# ============================
y_true = test['sales']
y_pred = pred

MAE = mean_absolute_error(y_true, y_pred)
RMSE = np.sqrt(mean_squared_error(y_true, y_pred))

y_true_safe = np.where(y_true==0, 0.1, y_true)
MAPE = np.mean(np.abs((y_true_safe - y_pred) / y_true_safe)) * 100

print("\n=== Evaluation Ayam Potong (Improved) ===")
print("MAE :", MAE)
print("RMSE:", RMSE)
print("MAPE:", MAPE)

# ============================
# 9. Plot
# ============================
plt.figure(figsize=(10,5))
plt.plot(train['sales'][-21:], label="Recent Actual (Train)")
plt.plot(test['sales'], label="Actual Test", marker='o')
plt.plot(pred, label="Forecast (Improved)", marker='x')
plt.title("SARIMAX Improved - Ayam Potong")
plt.grid(True)
plt.legend()
plt.show()
