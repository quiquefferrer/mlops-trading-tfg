from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

MODEL_PATH = "models/model.joblib"

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
feature_names = bundle["feature_names"]
n_lags = bundle["n_lags"]

app = FastAPI(title="AAPL Baseline Predictor", version="0.1")


class PredictRequest(BaseModel):
    # Lista con al menos n_lags cierres, en este orden:
    # [close_t, close_t-1, close_t-2, ...]
    closes: list[float]


@app.get("/health")
def health():
    return {"status": "ok", "n_lags": n_lags, "metrics": bundle.get("metrics", {})}


@app.post("/predict")
def predict(req: PredictRequest):
    if len(req.closes) < n_lags:
        return {"error": f"Necesito al menos {n_lags} valores en closes."}

    row = {f"lag_{i}": float(req.closes[i - 1]) for i in range(1, n_lags + 1)}
    X = pd.DataFrame([row], columns=feature_names)
    y_hat = float(model.predict(X)[0])
    return {"prediction_next_close": y_hat}
