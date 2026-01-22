# src/features.py
import pandas as pd

FEATURE_COLS = [
    "spy_ret_1d", "qqq_ret_1d", "vix_chg_1d",
    "spy_rv_5d", "spy_rv_10d", "spy_rv_20d",
    "qqq_rv_5d", "qqq_rv_10d", "qqq_rv_20d",
    "ratio_qqq_spy"
]

def make_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["ratio_qqq_spy"] = df["qqq_close"] / df["spy_close"]

    missing = [c for c in FEATURE_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required feature columns: {missing}")

    return df[FEATURE_COLS]
