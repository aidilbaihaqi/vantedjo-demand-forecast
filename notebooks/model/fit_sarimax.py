# sarimax_forecast_eval_per_ayam.py

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error

# ====================
# CONFIG
# ====================
FILES = {
    "Ayam Potong": "../processed_for_model/sarimax_ap_clean.csv",
    "Ayam Kampung": "../processed_for_model/sarimax_ak_clean.csv",
    "Ayam Tua": "../processed_for_model/sarimax_at_clean.csv",
}

CALENDAR_FILE = "calendar_2025_id.csv"
FORECAST_DAYS = 7

EXOG_COLS = [
    "is_closed",
    "dow",
    "is_weekend",
    "is_event",
    "pre_event_peak",
    "restock_flag",
]

# ====================
# LOAD CALENDAR
# ====================
def load_calendar():
    cal = pd.read_csv(CALENDAR_FILE)
    cal["date"] = pd.to_datetime(cal["date"])
    cal = cal.set_index("date")
    return cal

# ====================
# EVALUATION FUNCTION
# ====================
def evaluate(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(((y_true - y_pred) ** 2).mean())
    mape = (np.abs((y_true - y_pred) / y_true.replace(0, np.nan))).mean() * 100
    return mae, rmse, mape

# ====================
# MAIN FORECAST LOGIC
# ====================
def run_sarimax(name, file_path, calendar_df):
    print(f"\n====================")
    print(f" SARIMAX — {name}")
    print(f"====================")

    # 1. LOAD DATA HISTORIS
    df = pd.read_csv(file_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()

    # Pastikan kolom exogenous ada di df historis,
    # kalau belum ada, isi 0 saja
    for col in EXOG_COLS:
        if col not in df.columns:
            df[col] = 0

    # 2. SPLIT TRAIN / TEST (7 hari terakhir untuk evaluasi)
    if len(df) <= FORECAST_DAYS + 5:
        raise ValueError(f"Data {name} terlalu pendek untuk split train/test.")

    train = df.iloc[:-FORECAST_DAYS]
    test = df.iloc[-FORECAST_DAYS:]

    y_train = train["sales"]
    y_test = test["sales"]

    X_train = train[EXOG_COLS]
    X_test = test[EXOG_COLS]

    # 3. FIT SARIMAX
    model = SARIMAX(
        y_train,
        exog=X_train,
        order=(0, 1, 1),
        seasonal_order=(0, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    result = model.fit(disp=False)

    # 4. FORECAST 7 HARI UNTUK EVALUASI (pakai X_test)
    forecast_test = result.get_forecast(steps=FORECAST_DAYS, exog=X_test)
    pred_test = forecast_test.predicted_mean

    mae, rmse, mape = evaluate(y_test, pred_test)

    print(f"\n=== EVALUASI (7 hari terakhir) — {name} ===")
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"MAPE : {mape:.2f}%")

    # 5. FORECAST 7 HARI KE DEPAN (future 2025)
    last_date = df.index.max()

    # ambil tanggal future > last_date dari calendar_2025_id.csv
    cal_future = calendar_df.loc[calendar_df.index > last_date].copy()
    cal_future = cal_future.iloc[:FORECAST_DAYS]

    if cal_future.empty:
        print("Tidak ada tanggal future setelah last_date di calendar_2025_id.csv")
        return None, mae, rmse, mape

    # pastikan exog future lengkap
    for col in EXOG_COLS:
        if col not in cal_future.columns:
            cal_future[col] = 0

    future_forecast = result.get_forecast(
        steps=len(cal_future),
        exog=cal_future[EXOG_COLS]
    )
    y_future = future_forecast.predicted_mean

    out = pd.DataFrame({
        "date": cal_future.index,
        "forecast_sales": y_future.values
    })

    print(f"\n=== FUTURE FORECAST 7 HARI — {name} ===")
    print(out)

    # simpan ke CSV (optional)
    out_csv = f"future_forecast_7hari_{name.replace(' ', '_').lower()}.csv"
    out.to_csv(out_csv, index=False)
    print(f"Hasil forecast 7 hari ({name}) disimpan ke: {out_csv}")

    return out, mae, rmse, mape

# ====================
# RUN ALL MODELS
# ====================
def main():
    calendar_df = load_calendar()

    results = {}

    for name, file in FILES.items():
        forecast, mae, rmse, mape = run_sarimax(name, file, calendar_df)
        results[name] = {
            "forecast": forecast,
            "MAE": mae,
            "RMSE": rmse,
            "MAPE": mape,
        }

    print("\n=========================")
    print("  SUMMARY ALL MODELS")
    print("=========================")
    for name, r in results.items():
        print(f"\n{name}:")
        print(f"MAE  = {r['MAE']:.3f}")
        print(f"RMSE = {r['RMSE']:.3f}")
        print(f"MAPE = {r['MAPE']:.2f}%")

if __name__ == "__main__":
    main()
