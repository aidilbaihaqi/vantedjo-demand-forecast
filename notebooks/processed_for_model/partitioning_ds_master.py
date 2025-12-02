import pandas as pd

# ================================
# 1. Load master dataset
# ================================
df = pd.read_csv("df_daily_master.csv")

# ================================
# 2. Buat dataset SARIMAX per ayam
# ================================

# Ayam Potong
sarimax_ap = df[[
    "date",
    "Ayam Potong (A.P)",
    "is_closed",
    "dow",
    "is_weekend",
    "is_event",
    "pre_event_peak",
    "restock_flag"
]].rename(columns={"Ayam Potong (A.P)": "sales"})

# Ayam Kampung
sarimax_ak = df[[
    "date",
    "Ayam Kampung (A.K)",
    "is_closed",
    "dow",
    "is_weekend",
    "is_event",
    "pre_event_peak",
    "restock_flag"
]].rename(columns={"Ayam Kampung (A.K)": "sales"})

# Ayam Tua
sarimax_at = df[[
    "date",
    "Ayam Tua (A.T)",
    "is_closed",
    "dow",
    "is_weekend",
    "is_event",
    "pre_event_peak",
    "restock_flag"
]].rename(columns={"Ayam Tua (A.T)": "sales"})


# ================================
# 3. Simpan sebagai CSV final
# ================================
sarimax_ap.to_csv("sarimax_ap.csv", index=False)
sarimax_ak.to_csv("sarimax_ak.csv", index=False)
sarimax_at.to_csv("sarimax_at.csv", index=False)

print("✅ Dataset SARIMAX berhasil dibuat:")
print("- sarimax_ap.csv")
print("- sarimax_ak.csv")
print("- sarimax_at.csv")
