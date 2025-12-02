import pandas as pd

# ============================
# 1. Load all SARIMAX datasets
# ============================
ap = pd.read_csv("sarimax_ap.csv")
ak = pd.read_csv("sarimax_ak.csv")
at = pd.read_csv("sarimax_at.csv")

datasets = {"Ayam Potong": ap, "Ayam Kampung": ak, "Ayam Tua": at}

# ============================
# 2. Validation Function
# ============================

def validate_dataset(name, df):
    print(f"\n==============================")
    print(f"VALIDASI DATASET: {name}")
    print("==============================")

    # ---- Shape ----
    print(f"Jumlah baris: {df.shape[0]} (expected: 366)")
    print(f"Jumlah kolom: {df.shape[1]} (expected: 8)\n")

    # ---- Check columns ----
    print("Kolom yang ada:", df.columns.tolist())

    # ---- Missing values ----
    print("\nJumlah missing values per kolom:")
    print(df.isna().sum())

    # ---- Check duplicates ----
    print("\nJumlah data duplikat:", df.duplicated().sum())

    # ---- Check negative values ----
    if (df['sales'] < 0).any():
        print("\n⚠️ Ada nilai penjualan negatif!")
    else:
        print("\n✔ Tidak ada nilai penjualan negatif.")

    # ---- Check date order ----
    df['date'] = pd.to_datetime(df['date'])
    if df['date'].is_monotonic_increasing:
        print("✔ Tanggal berurutan naik.")
    else:
        print("⚠️ Tanggal TIDAK berurutan!")

    # ---- Check date range ----
    print(f"Range tanggal: {df['date'].min()} → {df['date'].max()}")

    # ---- Check exog variable anomalies ----
    print("\nUnique values per fitur exog:")
    print({
        'is_closed': df['is_closed'].unique().tolist(),
        'is_weekend': df['is_weekend'].unique().tolist(),
        'is_event': df['is_event'].unique().tolist(),
        'pre_event_peak': df['pre_event_peak'].unique().tolist(),
        'restock_flag': df['restock_flag'].unique().tolist(),
    })

    ap[ap.duplicated(subset='date', keep=False)]


# ============================
# 3. Run validation for each dataset
# ============================

for name, df in datasets.items():
    validate_dataset(name, df)
