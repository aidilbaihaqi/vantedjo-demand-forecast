# sarimax_ap.py
# SARIMAX untuk Ayam Potong (stabil version)
# - Evaluasi 7 hari terakhir (MAE, RMSE, MAPE)
# - Future forecast 7 hari ke depan (setelah last_date) pakai kalender 2025

import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ========================
# CONFIG
# ========================
DATA_CSV = "../processed_for_model/sarimax_ap_clean.csv"
CALENDAR_CSV = "calendar_2025_id.csv"
FORECAST_DAYS = 7

CALENDAR_BASE_COLS = [
    "is_closed",
    "dow",
    "is_weekend",
    "is_event",
    "pre_event_peak",
    "restock_flag",
]


# ========================
# HELPER FUNCTIONS
# ========================
def prepare_features(df: pd.DataFrame):
    """Build lag and MA features + smooth + log-transform."""
    q_high = df["sales"].quantile(0.98)  # gunakan q98 agar model lebih fleksibel
    df["sales_smooth"] = df["sales"].clip(lower=0, upper=q_high)
    df["sales_log"] = np.log1p(df["sales_smooth"])

    for lag in [1, 3, 7]:
        df[f"lag{lag}"] = df["sales_smooth"].shift(lag)

    df["ma3"] = df["sales_smooth"].rolling(3, min_periods=1).mean()
    df["ma7"] = df["sales_smooth"].rolling(7, min_periods=1).mean()

    df_model = df.dropna().copy()
    return df_model, q_high


def evaluate_metrics(y_true, y_pred):
    y_true = pd.Series(y_true).astype(float)
    y_pred = pd.Series(y_pred).astype(float)

    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = np.sqrt(mse)
    mape = (np.abs((y_true - y_pred) / y_true.replace(0, np.nan))).mean() * 100

    return mae, rmse, mape


def load_calendar_2025():
    cal = pd.read_csv(CALENDAR_CSV)
    cal["date"] = pd.to_datetime(cal["date"])
    cal = cal.set_index("date").sort_index()
    return cal


# ========================
# MAIN
# ========================
def main():
    print("\n====================")
    print(" SARIMAX — Ayam Potong (Stable Model)")
    print("====================")

    # 1. Load data historis
    df = pd.read_csv(DATA_CSV)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()

    df = df.asfreq("D")
    df["sales"] = df["sales"].fillna(0)

    for col in CALENDAR_BASE_COLS:
        if col not in df.columns:
            df[col] = 0

    df_model, q_high = prepare_features(df)
    exog_cols = CALENDAR_BASE_COLS + ["lag1", "lag3", "lag7", "ma3", "ma7"]

    # 2. Train-test split
    test_horizon = FORECAST_DAYS
    train = df_model.iloc[:-test_horizon]
    test = df_model.iloc[-test_horizon:]

    y_train = train["sales_log"]
    X_train = train[exog_cols]

    y_test = test["sales"]
    X_test = test[exog_cols]

    # ===============================
    # ⚡ STABLE SARIMAX ORDER
    # ===============================
    model = SARIMAX(
        endog=y_train,
        exog=X_train,
        order=(1, 1, 1),
        seasonal_order=(1, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )

    print("\nFitting stable SARIMAX model...")
    res = model.fit(disp=False, maxiter=300)

    # 3. Evaluasi
    fc_test = res.get_forecast(steps=test_horizon, exog=X_test)
    pred_log = fc_test.predicted_mean
    y_pred = np.expm1(pred_log).clip(lower=0)

    mae, rmse, mape = evaluate_metrics(y_test, y_pred)

    print("\n=== EVALUASI (7 hari terakhir) — Ayam Potong ===")
    print(f"MAE  : {mae:.3f}")
    print(f"RMSE : {rmse:.3f}")
    print(f"MAPE : {mape:.2f}%")

    # 4. Future forecast 7 hari
    cal2025 = load_calendar_2025()
    last_date = df_model.index.max()

    cal_future = cal2025.loc[cal2025.index > last_date].copy()
    cal_future = cal_future.iloc[:FORECAST_DAYS]

    for col in CALENDAR_BASE_COLS:
        if col not in cal_future.columns:
            cal_future[col] = 0

    results = []
    last_df = df_model.copy()

    print("\nForecasting 7 hari ke depan...")

    for current_date, row in cal_future.iterrows():
        # Calendar exog
        cal_vals = {col: int(row[col]) for col in CALENDAR_BASE_COLS}

        # Dynamic lag/MA
        lag1 = last_df["sales_smooth"].iloc[-1]
        lag3 = last_df["sales_smooth"].iloc[-3]
        lag7 = last_df["sales_smooth"].iloc[-7]
        ma3 = last_df["sales_smooth"].rolling(3).mean().iloc[-1]
        ma7 = last_df["sales_smooth"].rolling(7).mean().iloc[-1]

        exog_row = pd.DataFrame(
            {
                **cal_vals,
                "lag1": [lag1],
                "lag3": [lag3],
                "lag7": [lag7],
                "ma3": [ma3],
                "ma7": [ma7],
            },
            index=[current_date],
        )

        # Forecast log → exp
        log_pred = res.forecast(steps=1, exog=exog_row[exog_cols])
        y_hat = np.expm1(log_pred.iloc[0])
        y_hat = max(0, y_hat)
        y_hat = min(y_hat, q_high * 1.8)  # beri lebih fleksibel supaya weekend naik

        results.append((current_date, y_hat))

        last_df.loc[current_date] = {
            "sales": y_hat,
            "sales_smooth": min(y_hat, q_high),
            "sales_log": np.log1p(min(y_hat, q_high)),
            **cal_vals,
        }

    print("\n=== FUTURE FORECAST 7 HARI (STABLE MODEL) — Ayam Potong ===")
    for date, value in results:
        print(f"{date.strftime('%Y-%m-%d')}: {value:.2f} kg")
    
    print(f"\nRata-rata prediksi: {sum([v for _, v in results])/len(results):.2f} kg/hari")
    
    return results


if __name__ == "__main__":
    main()
