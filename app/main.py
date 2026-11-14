import json
from pathlib import Path

import joblib
from fastapi import FastAPI
from pydantic import BaseModel

from app.schemas import HeartDiseaseFeatures

app = FastAPI(
    title="Heart Disease Prediction API",
    description="API for predicting heart disease risk based on clinical features.",
    version="1.0.0",
)

MODEL_PATH = Path(__file__).resolve().parent.parent / "model" / "heart_model.joblib"
MODEL = joblib.load(MODEL_PATH)

METADATA_PATH = Path(__file__).resolve().parent.parent / "model" / "model_metadata.json"
with open(METADATA_PATH, "r") as f:
    METADATA = json.load(f)

FEATURE_COLUMNS = METADATA.get("feature_columns", [
    "age", "sex", "cp", "trestbps", "chol", "fbs", "restecg",
    "thalach", "exang", "oldpeak", "slope", "ca", "thal"
])


class PredictionResponse(BaseModel):
    heart_disease: bool


@app.get("/")
def root():
    return {
        "message": "Heart Disease Prediction API",
        "docs": "/docs",
        "health": "/health",
        "info": "/info",
        "predict": "/predict",
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/info")
def info():
    return {
        "model_type": METADATA.get("selected_model", "Logistic Regression"),
        "features": FEATURE_COLUMNS,
        "target_column": METADATA.get("target_column", "target"),
        "assumed_target_mapping": METADATA.get("assumed_target_mapping", {"0": "absence", "1": "presence"}),
        "test_metrics": METADATA.get("test_metrics", {}),
        "random_state": METADATA.get("random_state", 42),
    }


@app.post("/predict")
def predict(features: HeartDiseaseFeatures):
    import pandas as pd
    data = features.model_dump()
    df = pd.DataFrame([data], columns=FEATURE_COLUMNS)
    prediction = MODEL.predict(df)[0]
    heart_disease = bool(prediction)
    return {"heart_disease": heart_disease}