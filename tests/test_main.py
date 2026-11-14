import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_info():
    response = client.get("/info")
    assert response.status_code == 200
    data = response.json()
    assert data["model_type"] == "Logistic Regression"
    assert "features" in data
    assert len(data["features"]) == 13
    assert "age" in data["features"]
    assert "thal" in data["features"]


def test_predict_positive():
    payload = {
        "age": 63,
        "sex": 1,
        "cp": 3,
        "trestbps": 145,
        "chol": 233,
        "fbs": 1,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.3,
        "slope": 0,
        "ca": 0,
        "thal": 1,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "heart_disease" in data
    assert isinstance(data["heart_disease"], bool)


def test_predict_negative():
    payload = {
        "age": 55,
        "sex": 1,
        "cp": 0,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.5,
        "slope": 0,
        "ca": 0,
        "thal": 3,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "heart_disease" in data
    assert isinstance(data["heart_disease"], bool)


def test_predict_missing_field():
    payload = {
        "age": 55,
        "sex": 1,
        "cp": 0,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.5,
        "slope": 0,
        "ca": 0,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_invalid_type():
    payload = {
        "age": "not_a_number",
        "sex": 1,
        "cp": 0,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 0,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 2.5,
        "slope": 0,
        "ca": 0,
        "thal": 3,
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422