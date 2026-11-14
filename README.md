# Heart Disease Prediction API

A FastAPI-based REST API that predicts heart disease (`heart_disease: true/false`) using a trained Logistic Regression model.

## Tech Stack

- **Python 3.11**
- **FastAPI** - Web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Request validation / schemas
- **scikit-learn** - Model loading & prediction (Pipeline with preprocessing + Logistic Regression classifier)
- **joblib** - Model serialization
- **pandas** - DataFrame handling for prediction
- **uv** - Fast Python package manager (used inside Docker container)
- **Docker** / **Docker Compose** - Containerization

## Project Structure

```
heart-desease-prediction-api/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, endpoints (/health, /info, /predict)
│   └── schemas.py       # Pydantic model for input features
├── model/
│   ├── heart_model.joblib   # Trained model
│   └── model_metadata.json  # Model info (type, features, metrics)
├── tests/
│   ├── __init__.py
│   └── test_main.py     # Pytest test cases
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml       # uv project config
├── requirements.txt
└── README.md
```

## Getting Started (Local)

### Prerequisites

- Docker installed
- Docker Compose installed

### Run the App

```bash
# Build the Docker image
docker-compose build

# Start the container
docker-compose up
```

The API will be available at:

- **Base URL:** `http://localhost:8000`
- **Swagger UI / Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`
- **Info:** `http://localhost:8000/info`
- **Predict:** `http://localhost:8000/predict`

## API Endpoints

### GET /health

Returns the health status of the service.

```bash
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "ok"
}
```

### GET /info

Returns model type, feature list, and metadata.

```bash
curl http://localhost:8000/info
```

### POST /predict

Accepts clinical features and returns heart disease prediction.

**Request Body (JSON):**

```json
{
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
  "thal": 3
}
```

**Using curl:**

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "thal": 3
  }'
```

**Response:**

```json
{
  "heart_disease": false
}
```

## Manual Test Instructions

### 1. Health Check

```bash
curl http://localhost:8000/health
```

### 2. Info

```bash
curl http://localhost:8000/info
```

### 3. Predict (Heart Disease = true)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "thal": 1
  }'
```

### 4. Predict (Heart Disease = false)

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
    "thal": 3
  }'
```

### 5. Swagger UI

Open in browser:

```
http://localhost:8000/docs
```

## Running Tests

### Run Tests Inside Container

```bash
docker exec heart-disease-api uv run pytest tests/ -v
```

### Run Tests Locally (if uv is installed)

```bash
uv run pytest tests/ -v
```

### Run Tests with Docker Compose

```bash
docker compose exec heart-disease-api uv run pytest tests/ -v
```

## Docker Commands

### Build the Image

```bash
docker-compose build
```

### Start the Container

```bash
docker-compose up
```

### Stop the Container

```bash
docker-compose down
```

### Rebuild & Restart (After Code / Model Changes)

```bash
docker-compose up -d --build
```

### Incremental Change Reflecting to Same Container

If you change the app code or model and want the same running container to pick up changes:

```bash
# Rebuild the image and recreate the container
docker-compose up -d --build

# Or rebuild only the image and restart the service
docker-compose build
docker-compose up -d
```

## uv Usage (Inside Container)

The project uses `uv` as the package manager. `uv` is installed inside the Docker container (not on the host).

### Install Dependencies

```bash
docker exec heart-disease-api uv pip install -r requirements.txt
```

### Run Tests

```bash
docker exec heart-disease-api uv run pytest tests/ -v
```

### Check Installed Packages

```bash
docker exec heart-disease-api uv pip list
```

## Deploy on Render

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

### 2. Create a New Web Service on Render

1. Go to [Render](https://render.com) and sign in.
2. Click **New +** → **Web Service**.
3. **Repository:** Select your GitHub repo.
4. **Environment:** Select **Docker**.
5. **Build Command:** Leave empty (Render auto-detects Dockerfile).
6. **Start Command:** Leave empty (Render auto-detects from Dockerfile CMD).
7. **Build Context:** Set to `/` (root) since the Dockerfile is at the project root.
8. **Port:** Set to `8000` (Render sets this automatically from EXPOSE).
9. Click **Create Web Service**.

### 3. Wait for Build

Render will build the Docker image and deploy. Wait for the service to become live.

### 4. Test the Deployed Endpoints

```bash
curl https://<your-render-app-name>.onrender.com/health
curl https://<your-render-app-name>.onrender.com/info
curl -X POST https://<your-render-app-name>.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{ ... }'
```

Swagger UI will be available at:

```
https://<your-render-app-name>.onrender.com/docs
```

## Submission Requirements

The GitHub repository must contain:

- `app/` - FastAPI application code
- `model/` - Trained model artifacts (`heart_model.joblib`, `model_metadata.json`)
- `tests/` - Test cases
- `Dockerfile`
- `docker-compose.yml`
- `requirements.txt`
- `pyproject.toml` - uv project config
- `README.md`

Live Render deployment URL:

```
https://<your-render-app-name>.onrender.com
