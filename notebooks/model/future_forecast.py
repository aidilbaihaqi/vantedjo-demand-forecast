# future_forecast_2025.py

import pandas as pd
import numpy as np
from datetime import timedelta
from statsmodels.tsa.statespace.sarimax import SARIMAX

# ========================
# CONFIG
# ========================
DATASETS = {
    "Ayam Potong": "../processed_for_model/sarimax_ap_clean.csv",
    "Ayam Kampung": "../processed_for_model/sarimax_ak_clean.csv",
    "Ayam Tua": "../processed_for_model/sarimax_at_clean.csv",
}

CALENDAR_CSV = "calendar_2025_id.csv"
FORECAST_END = "2025-01-07"   # bisa kamu ganti, misal "2025-01-31"

FORECAST_START_AFTER_HISTORY = True
# Kalau True → mulai forecast H+1 setelah last_date di histori
# Kalau False → pakai dari 2025-01-01 langsung (pastikan > last_date)


# ========================
# FEATURE ENGINEERING
# ========================
def prepare_features(df):
    """
    - Clip outlier q95
    - Log transform
    - lag1, lag3, lag7
    - ma3, ma7
    """
    q_high = df["sales"].quantile(0.95)
    df["sales_smooth"] = df["sales"].clip(upper=q_high)
    df["sales_log"] = np.log1p(df["sales_smooth"])

    for lag in [1, 3, 7]:
        df[f"lag{lag}"] = df["sales_smooth"].shift(lag)

    df["ma3"] = df["sales_smooth"].rolling(3, min_periods=1).mean()
    df["ma7"] = df["sales_smooth"].rolling(7, min_periods=1).mean()

    df_model = df.dropna().copy()
    return df_model, q_high


def load_calendar():
    cal = pd.read_csv(CALENDAR_CSV)
    cal["date"] = pd.to_datetime(cal["date"])
    cal = cal.set_index("date").sort_index()
    return cal


def forecast_future_2025(name, csv_path, calendar_df):
    print(f"\n=== FUTURE FORECAST 2025 (ITERATIVE): {name} ===\n")

    # 1. Load data historis
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date").sort_index()

    # 2. Build fitur improved
    df_model, q_high = prepare_features(df)

    exog_cols = [
        "is_closed",
        "dow",
        "is_weekend",
        "is_event",
        "pre_event_peak",
        "restock_flag",
        "lag1",
        "lag3",
        "lag7",
        "ma3",
        "ma7",
    ]

    # 3. Fit SARIMAX ke seluruh histori
    model = SARIMAX(
        df_model["sales_log"],
        exog=df_model[exog_cols],
        order=(0, 1, 1),
        seasonal_order=(0, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False,
    ).fit(disp=False)

    last_df = df_model.copy()
    last_date = last_df.index.max()

    # 4. Tentukan tanggal future yang mau diprediksi
    cal = calendar_df.copy()
    cal = cal.loc[(cal.index > last_date) & (cal.index <= FORECAST_END)]

    if cal.empty:
        print("Tidak ada tanggal future dalam range setelah last_date.")
        return None

    print(f"Last historical date  : {last_date.date()}")
    print(f"Forecast date range   : {cal.index.min().date()} → {cal.index.max().date()}")
    print(f"Total days to predict : {len(cal)}")

    results = []

    # 5. Iterasi per tanggal future
    for current_date, row in cal.iterrows():
        # Exog kalender (sudah ada dari CSV)
        is_closed = int(row["is_closed"])
        is_event = int(row["is_event"])
        pre_event_peak = int(row["pre_event_peak"])
        restock_flag = int(row.get("restock_flag", 0))
        dow = int(row["dow"])
        is_weekend = int(row["is_weekend"])

        # Lag & MA dari last_df (sudah termasuk prediksi sebelumnya)
        lag1 = last_df["sales_smooth"].iloc[-1]
        lag3 = last_df["sales_smooth"].iloc[-3]
        lag7 = last_df["sales_smooth"].iloc[-7]
        ma3 = last_df["sales_smooth"].rolling(3).mean().iloc[-1]
        ma7 = last_df["sales_smooth"].rolling(7).mean().iloc[-1]

        exog_row = pd.DataFrame(
            {
                "is_closed": [is_closed],
                "dow": [dow],
                "is_weekend": [is_weekend],
                "is_event": [is_event],
                "pre_event_peak": [pre_event_peak],
                "restock_flag": [restock_flag],
                "lag1": [lag1],
                "lag3": [lag3],
                "lag7": [lag7],
                "ma3": [ma3],
                "ma7": [ma7],
            },
            index=[current_date],
        )

        # 1-step forecast di domain log
        log_pred = model.forecast(steps=1, exog=exog_row[exog_cols])
        y_hat = np.expm1(log_pred.iloc[0])  # balik ke kg

        results.append((current_date, y_hat))

        # Update last_df untuk tanggal ini (supaya lag/MA untuk hari berikutnya benar)
        sales_smooth_new = min(y_hat, q_high)
        sales_log_new = np.log1p(sales_smooth_new)

        new_row = {
            "sales": y_hat,
            "sales_smooth": sales_smooth_new,
            "sales_log": sales_log_new,
            "is_closed": is_closed,
            "dow": dow,
            "is_weekend": is_weekend,
            "is_event": is_event,
            "pre_event_peak": pre_event_peak,
            "restock_flag": restock_flag,
            # lag & MA akan dihitung ulang lewat prepare_features di iterasi berikutnya?
            # Di sini kita biarkan sales_smooth terisi, dan rolling diambil dari last_df
        }
        last_df.loc[current_date] = new_row
        last_df = last_df.sort_index()

    # 6. Simpan hasil
    out = pd.DataFrame(results, columns=["date", "forecast_sales"])
    out_csv = f"future_forecast_2025_{name.replace(' ', '_').lower()}.csv"
    out.to_csv(out_csv, index=False)

    print(out.head(15))
    print(f"Hasil forecast masa depan 2025 disimpan ke: {out_csv}\n")

    return out


def main():
    calendar_df = load_calendar()

    for name, path in DATASETS.items():
        forecast_future_2025(name, path, calendar_df)


if __name__ == "__main__":
    main()
