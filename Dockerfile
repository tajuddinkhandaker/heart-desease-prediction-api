FROM python:3.11-slim

WORKDIR /app

# Install uv inside the container (not on host)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy dependency files first for better layer caching
COPY pyproject.toml requirements.txt ./

# Install dependencies with uv
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application code and model
COPY app/ ./app/
COPY model/ ./model/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
