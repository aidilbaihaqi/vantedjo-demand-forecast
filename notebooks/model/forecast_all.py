import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ==========================================
# CONFIG
# ==========================================

DATASETS = {
    "Ayam Potong": "../processed_for_model/sarimax_ap_clean.csv",
    "Ayam Kampung": "../processed_for_model/sarimax_ak_clean.csv",
    "Ayam Tua": "../processed_for_model/sarimax_at_clean.csv",
}

N_TEST_DAYS = 7  # jumlah hari terakhir untuk evaluasi


# ==========================================
# UTILS
# ==========================================

def build_features(df, clip_quantile=0.95):
    """
    - Clip outlier di atas quantile tertentu
    - Log transform (log1p)
    - Buat lag1, lag3, lag7, ma3, ma7
    """
    # smoothing outlier
    q_high = df['sales'].quantile(clip_quantile)
    df['sales_smooth'] = df['sales'].clip(upper=q_high)

    # log transform
    df['sales_log'] = np.log1p(df['sales_smooth'])

    # lag features
    for lag in [1, 3, 7]:
        df[f'lag{lag}'] = df['sales_smooth'].shift(lag)

    # moving averages
    df['ma3'] = df['sales_smooth'].rolling(3, min_periods=1).mean()
    df['ma7'] = df['sales_smooth'].rolling(7, min_periods=1).mean()

    # drop baris yang kena NaN karena lag/MA awal
    df_model = df.dropna().copy()

    return df_model, q_high


def evaluate_forecast(y_true, y_pred):
    """
    Hitung MAE, RMSE, MAPE (dengan handling nilai 0)
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))

    y_true_safe = np.where(y_true == 0, 0.1, y_true)
    mape = np.mean(np.abs((y_true_safe - y_pred) / y_true_safe)) * 100

    return mae, rmse, mape


def forecast_one_series(name, csv_path, n_test=N_TEST_DAYS, clip_quantile=0.95):
    print(f"\n==============================")
    print(f"  FORECAST SERIES: {name}")
    print(f"  File: {csv_path}")
    print(f"==============================")

    # --------------------------------------
    # 1. Load data
    # --------------------------------------
    df = pd.read_csv(csv_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date').sort_index()

    print("Shape awal:", df.shape)

    # --------------------------------------
    # 2. Feature engineering (smoothing + log + lag + MA)
    # --------------------------------------
    df_model, q_high = build_features(df, clip_quantile=clip_quantile)
    print(f"Quantile {int(clip_quantile*100)}% (upper clip): {q_high}")
    print("Shape setelah feature engineering + dropna:", df_model.shape)

    # --------------------------------------
    # 3. Train-test split
    # --------------------------------------
    train = df_model.iloc[:-n_test]
    test = df_model.iloc[-n_test:]

    exog_cols = [
        'is_closed', 'dow', 'is_weekend', 'is_event',
        'pre_event_peak', 'restock_flag',
        'lag1', 'lag3', 'lag7', 'ma3', 'ma7'
    ]

    print("Periode train:", train.index.min(), "→", train.index.max())
    print("Periode test :", test.index.min(), "→", test.index.max())

    # --------------------------------------
    # 4. Fit SARIMAX di domain log
    # --------------------------------------
    model = SARIMAX(
        train['sales_log'],
        exog=train[exog_cols],
        order=(0, 1, 1),
        seasonal_order=(0, 1, 1, 7),
        enforce_stationarity=False,
        enforce_invertibility=False
    ).fit(disp=False)

    print("\nRingkasan model (short):")
    print(model.summary().tables[1])  # hanya tabel koefisien biar singkat

    # --------------------------------------
    # 5. Forecast (domain log → balik ke skala asli)
    # --------------------------------------
    log_forecast = model.predict(
        start=test.index[0],
        end=test.index[-1],
        exog=test[exog_cols]
    )

    forecast = np.expm1(log_forecast)

    # --------------------------------------
    # 6. Evaluation
    # --------------------------------------
    y_true = test['sales']
    y_pred = forecast

    mae, rmse, mape = evaluate_forecast(y_true, y_pred)

    print("\n=== Evaluation Results:", name, "===")
    print("MAE  :", mae)
    print("RMSE :", rmse)
    print("MAPE :", mape)

    # --------------------------------------
    # 7. Simpan forecast ke CSV
    # --------------------------------------
    result_df = pd.DataFrame({
        "date": test.index,
        "actual_sales": y_true.values,
        "pred_sales": y_pred.values
    })
    out_csv = f"forecast_{name.replace(' ', '_').lower()}.csv"
    result_df.to_csv(out_csv, index=False)
    print(f"Hasil forecast disimpan ke: {out_csv}")

    # --------------------------------------
    # 8. Plot
    # --------------------------------------
    plt.figure(figsize=(10, 5))
    plt.plot(train['sales'][-21:], label="Recent Actual (Train)")
    plt.plot(test['sales'], label="Actual (Test)", marker='o')
    plt.plot(forecast, label="Forecast", marker='x')
    plt.title(f"SARIMAX Improved - {name} (Last {n_test} days)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return {
        "name": name,
        "mae": mae,
        "rmse": rmse,
        "mape": mape,
        "q_high": q_high,
        "n_obs": df.shape[0]
    }


def main():
    summary = []

    for name, path in DATASETS.items():
        try:
            metrics = forecast_one_series(name, path, n_test=N_TEST_DAYS)
            summary.append(metrics)
        except FileNotFoundError:
            print(f"[WARNING] File tidak ditemukan: {path}")

    # Ringkasan akhir
    if summary:
        print("\n\n========== RINGKASAN AKHIR ==========")
        for m in summary:
            print(f"\n{m['name']}")
            print(f"- Observasi       : {m['n_obs']}")
            print(f"- Upper clip q95  : {m['q_high']:.3f}")
            print(f"- MAE             : {m['mae']:.3f}")
            print(f"- RMSE            : {m['rmse']:.3f}")
            print(f"- MAPE            : {m['mape']:.3f} %")
        print("=====================================")


if __name__ == "__main__":
    main()
