FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

WORKDIR /app/

# Install uv
RUN python -m pip install --no-cache-dir "uv==0.10.10"

# Copy dependency metadata before the app for better layer caching
COPY ./app/pyproject.toml ./app/uv.lock* /app/

ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN uv sync --locked --no-install-project --no-dev
ENV PATH="/opt/venv/bin:${PATH}"

COPY ./app /app
ENV PYTHONPATH=/app
