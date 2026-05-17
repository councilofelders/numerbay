FROM python:3.11-slim

WORKDIR /app/

# Install uv
RUN python -m pip install --no-cache-dir "uv==0.10.10"

# Copy dependency metadata before the app for better layer caching
COPY ./app/pyproject.toml ./app/uv.lock* /app/

# Allow installing dev dependencies to run tests
ARG INSTALL_DEV=false
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT=/opt/venv
RUN bash -c "if [ \"$INSTALL_DEV\" = 'true' ] ; then uv sync --locked --no-install-project ; else uv sync --locked --no-install-project --no-dev ; fi"
ENV PATH="/opt/venv/bin:${PATH}"

# For development, Jupyter remote kernel, Hydrogen
# Using inside the container:
# jupyter lab --ip=0.0.0.0 --allow-root --NotebookApp.custom_display_url=http://127.0.0.1:8888
ARG INSTALL_JUPYTER=false
RUN bash -c "if [ $INSTALL_JUPYTER == 'true' ] ; then uv pip install --python /opt/venv/bin/python jupyterlab ; fi"

ENV C_FORCE_ROOT=1

COPY ./app /app
WORKDIR /app

ENV PYTHONPATH=/app

COPY ./app/worker-start.sh /worker-start.sh

RUN chmod +x /worker-start.sh

#CMD ["bash", "/worker-start.sh"]
