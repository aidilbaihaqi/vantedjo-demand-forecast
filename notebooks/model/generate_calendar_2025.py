# generate_calendar_2025.py

import pandas as pd
import holidays

YEAR = 2025
COUNTRY = "ID"  # Indonesia

def main():
    # 1. Buat range tanggal 1 Jan - 31 Des 2025
    dates = pd.date_range(start=f"{YEAR}-01-01", end=f"{YEAR}-12-31", freq="D")
    cal = pd.DataFrame({"date": dates})
    
    # 2. Info dasar kalender
    cal["dow"] = cal["date"].dt.weekday          # 0=Mon, 6=Sun
    cal["is_weekend"] = (cal["dow"] >= 5).astype(int)
    
    # 3. Libur nasional Indonesia via library 'holidays'
    id_holidays = holidays.Indonesia(years=[YEAR])
    
    cal["is_national_holiday"] = cal["date"].isin(id_holidays).astype(int)
    cal["holiday_name"] = cal["date"].map(lambda d: id_holidays.get(d, ""))

    # 4. Event & pre_event_peak
    cal["is_event"] = cal["is_national_holiday"]
    cal["pre_event_peak"] = 0
    
    for idx, row in cal.iterrows():
        if row["is_event"] == 1:
            prev_date = row["date"] - pd.Timedelta(days=1)
            if prev_date.year == YEAR:
                mask_prev = cal["date"] == prev_date
                # pre_event_peak = 1 kalau hari sebelumnya bukan libur nasional (boleh kamu ubah rules)
                if not cal.loc[mask_prev, "is_national_holiday"].any():
                    cal.loc[mask_prev, "pre_event_peak"] = 1

    # 5. is_closed default: libur nasional (boleh tambahkan weekend kalau kamu mau)
    cal["is_closed"] = cal["is_national_holiday"]  # + weekend bisa pakai: | cal["is_weekend"]

    # 6. restock_flag default 0 (bisa kamu update manual/by rule)
    cal["restock_flag"] = 0

    # 7. Simpan ke CSV
    cal.to_csv("calendar_2025_id.csv", index=False)
    print("Kalender 2025 Indonesia berhasil dibuat: calendar_2025_id.csv")
    print(cal.head(15))


if __name__ == "__main__":
    main()
