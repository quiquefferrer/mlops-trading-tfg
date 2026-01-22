import os
import glob
import pandas as pd

RAW_PATH = "data/raw"
OUT_PATH = "data/processed"
SERIES = ["SPY", "QQQ", "VIX"]

os.makedirs(OUT_PATH, exist_ok=True)

for name in SERIES:
    files = sorted(glob.glob(os.path.join(RAW_PATH, name, f"{name}_*.csv")))
    if not files:
        raise FileNotFoundError(f"No files found for {name}")

    dfs = []
    for f in files:
        df = pd.read_csv(f)
        df.columns = [c.lower().strip() for c in df.columns]
        df = df[["date", "open", "high", "low", "close", "volume"]]
        df["date"] = pd.to_datetime(df["date"])
        dfs.append(df)

    combined = (
        pd.concat(dfs, ignore_index=True)
        .drop_duplicates(subset="date")
        .sort_values("date")
        .reset_index(drop=True)
    )

    out_file = os.path.join(OUT_PATH, f"{name}_daily.csv")
    combined.to_csv(out_file, index=False)
    print(f"Saved {out_file} ({len(combined)} rows)")
