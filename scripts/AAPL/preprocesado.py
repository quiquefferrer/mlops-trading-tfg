import pandas as pd
import os


RAW_PATH = "data/raw/AAPL.csv"
PROCESSED_PATH = "data/processed/AAPL_processed.csv"


def preprocess_aapl():
    # Crear carpeta processed si no existe
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)

    # Leer CSV sin asumir estructura
    df = pd.read_csv(RAW_PATH)

    # Detectar columna de fecha
    possible_date_cols = [c for c in df.columns if c.lower() in ["date", "datetime", "timestamp"]]
    if possible_date_cols:
        date_col = possible_date_cols[0]
    else:
        # Caso típico yfinance: primera columna es la fecha
        date_col = df.columns[0]

    # Parsear fechas correctamente
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])

    # Normalizar nombres de columnas
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
    date_col = date_col.lower().strip().replace(" ", "_")

    # Renombrar fecha a 'date'
    df = df.rename(columns={date_col: "date"})

    # Seleccionar columnas estándar OHLCV si existen
    expected_cols = ["date", "open", "high", "low", "close", "volume"]
    df = df[[c for c in expected_cols if c in df.columns]]

    # Limpiar y ordenar
    df = df.drop_duplicates("date").sort_values("date").reset_index(drop=True)

    # Guardar CSV procesado
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"✅ Datos preprocesados guardados en {PROCESSED_PATH}")
    print(f"📅 Rango temporal: {df['date'].min().date()} → {df['date'].max().date()}")
    print(f"📈 Filas totales: {len(df)}")


if __name__ == "__main__":
    preprocess_aapl()
