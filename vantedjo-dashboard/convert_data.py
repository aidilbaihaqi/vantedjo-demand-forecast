"""
Script untuk convert data SARIMAX clean ke format yang dibutuhkan dashboard
"""
import pandas as pd

# Convert Ayam Potong
df_ap = pd.read_csv('data/ts_ayam_potong_clean.csv')
df_ap = df_ap.rename(columns={'sales': 'Ayam_Potong'})
df_ap.to_csv('data/ts_ayam_potong_clean.csv', index=False)
print("✓ Converted Ayam Potong")

# Convert Ayam Kampung
df_ak = pd.read_csv('data/ts_ayam_kampung_clean.csv')
df_ak = df_ak.rename(columns={'sales': 'Ayam_Kampung'})
df_ak.to_csv('data/ts_ayam_kampung_clean.csv', index=False)
print("✓ Converted Ayam Kampung")

# Convert Ayam Tua
df_at = pd.read_csv('data/ts_ayam_tua_clean.csv')
df_at = df_at.rename(columns={'sales': 'Ayam_Tua'})
df_at.to_csv('data/ts_ayam_tua_clean.csv', index=False)
print("✓ Converted Ayam Tua")

print("\n✅ All data converted successfully!")
