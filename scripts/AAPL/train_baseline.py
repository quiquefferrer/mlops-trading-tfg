import os
import joblib
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error

RAW_PROCESSED = "data/processed/AAPL_processed.csv"
MODEL_PATH = "models/model.joblib"

def make_supervised(df: pd.DataFrame, n_lags: int = 5):
    df = df.copy()
    df = df.sort_values("date")
    # Target: close del día siguiente
    df["y"] = df["close"].shift(-1)

    # Lags
    for i in range(1, n_lags + 1):
        df[f"lag_{i}"] = df["close"].shift(i)

    df = df.dropna().reset_index(drop=True)
    X = df[[f"lag_{i}" for i in range(1, n_lags + 1)]]
    y = df["y"]
    return X, y, df

def time_split(X, y, train_ratio=0.8):
    n = len(X)
    cut = int(n * train_ratio)
    return X.iloc[:cut], X.iloc[cut:], y.iloc[:cut], y.iloc[cut:]

def main():
    df = pd.read_csv(RAW_PROCESSED)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"]).sort_values("date")

    X, y, _ = make_supervised(df, n_lags=5)
    X_train, X_test, y_train, y_test = time_split(X, y, train_ratio=0.8)

    model = LinearRegression()
    model.fit(X_train, y_train)

    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    rmse = mean_squared_error(y_test, preds) ** 0.5

    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "n_lags": 5,
            "feature_names": list(X.columns),
            "metrics": {"mae": float(mae), "rmse": float(rmse)},
        },
        MODEL_PATH
    )

    print(f"✅ Modelo guardado en {MODEL_PATH}")
    print(f"MAE={mae:.4f} | RMSE={rmse:.4f}")

if __name__ == "__main__":
    main()
