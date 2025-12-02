import pandas as pd

# Load datasets
ap = pd.read_csv("sarimax_ap.csv")
ak = pd.read_csv("sarimax_ak.csv")
at = pd.read_csv("sarimax_at.csv")

# Remove duplicates
ap_clean = ap.drop_duplicates(subset='date', keep='first')
ak_clean = ak.drop_duplicates(subset='date', keep='first')
at_clean = at.drop_duplicates(subset='date', keep='first')

# Check new shape
print("Ayam Potong:", ap_clean.shape)
print("Ayam Kampung:", ak_clean.shape)
print("Ayam Tua:", at_clean.shape)

# Save cleaned versions
ap_clean.to_csv("sarimax_ap_clean.csv", index=False)
ak_clean.to_csv("sarimax_ak_clean.csv", index=False)
at_clean.to_csv("sarimax_at_clean.csv", index=False)

print("Selesai! Dataset SARIMAX clean berhasil dibuat.")
