# src/model.py
import json
import lightgbm as lgb
import pandas as pd
from pathlib import Path

class RiskModel:
    def __init__(self, models_dir="models"):
        self.models_dir = Path(models_dir)
        meta = json.loads((self.models_dir / "metadata.json").read_text())

        self.threshold = float(meta["threshold"])
        self.exposure_low = float(meta["exposure_low_risk"])
        self.exposure_high = float(meta["exposure_high_risk"])

        self.booster = lgb.Booster(model_file=str(self.models_dir / meta["model_file"]))

    def predict_proba(self, X: pd.DataFrame) -> float:
        # X debe venir ya con columnas en orden correcto
        return float(self.booster.predict(X)[0])

    def recommend_exposure(self, prob_high_risk: float) -> float:
        return self.exposure_high if prob_high_risk > self.threshold else self.exposure_low
