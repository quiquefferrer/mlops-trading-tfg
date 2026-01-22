import os
import ssl
import time
from datetime import datetime
import pandas as pd

# ======================================================
# CONFIGURACIÓN
# ======================================================
START_YEAR = 1990
END_YEAR = datetime.now().year

SERIES = {
    "SPY": {"yf": "SPY"},
    "QQQ": {"yf": "QQQ"},
    "VIX": {"yf": "^VIX"},
}

BASE_PATH = "data/raw"
os.makedirs(BASE_PATH, exist_ok=True)

# ======================================================
# UTILIDADES
# ======================================================
def clean_yfinance_df(df: pd.DataFrame) -> pd.DataFrame:
    """Arregla MultiIndex / tuples de yfinance"""
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]

    df = df.reset_index()
    df.columns = [str(c).lower().replace(" ", "_") for c in df.columns]

    if "adj_close" in df.columns and "close" not in df.columns:
        df["close"] = df["adj_close"]

    return df[["date", "open", "high", "low", "close", "volume"]]


def download_year_yfinance(symbol: str, year: int) -> pd.DataFrame | None:
    try:
        import yfinance as yf
    except ImportError:
        raise RuntimeError("yfinance no está instalado. pip install yfinance")

    start = f"{year}-01-01"
    end = f"{year+1}-01-01"

    try:
        df = yf.download(
            symbol,
            start=start,
            end=end,
            progress=False,
            auto_adjust=False,
            threads=False
        )
        if df is None or df.empty:
            return None

        df = clean_yfinance_df(df)
        df["date"] = pd.to_datetime(df["date"])
        return df.dropna().reset_index(drop=True)

    except Exception as e:
        print(f"   ❌ Error yfinance {symbol} {year}: {e}")
        return None


# ======================================================
# MAIN
# ======================================================
def main():
    print("=" * 70)
    print("⬇️ DESCARGA RAW DIARIA (SPY / QQQ / VIX)")
    print("=" * 70)

    for name, cfg in SERIES.items():
        symbol = cfg["yf"]
        out_dir = os.path.join(BASE_PATH, name)
        os.makedirs(out_dir, exist_ok=True)

        print(f"\n📈 {name} ({symbol})")

        for year in range(START_YEAR, END_YEAR + 1):
            out_file = os.path.join(out_dir, f"{name}_{year}.csv")

            if os.path.exists(out_file):
                print(f"   ⏭️  {year} ya existe, salto")
                continue

            print(f"   ⬇️  Descargando {year}...")
            df = download_year_yfinance(symbol, year)

            if df is None or df.empty:
                print(f"   ⚠️  Sin datos para {year}")
                continue

            df.to_csv(out_file, index=False)
            print(f"   ✅ Guardado {out_file} ({len(df)} filas)")
            time.sleep(0.8)  # amable con la API

    print("\n✅ DESCARGA RAW COMPLETADA")


if __name__ == "__main__":
    main()
