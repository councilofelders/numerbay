#! /usr/bin/env sh

set -e

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
REPO_ROOT=$(dirname "$SCRIPT_DIR")

if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  . "$REPO_ROOT/.env"
  set +a
fi

IMAGE="${DOCKER_IMAGE_BACKEND?Variable not set}:${TAG-latest}"
SERVER_NAME="${SERVER_NAME:-${DOMAIN?Variable not set}}"
SERVER_HOST="${SERVER_HOST:-https://${DOMAIN?Variable not set}}"
PROJECT_NAME="${PROJECT_NAME:-NumerBay}"
FIRST_SUPERUSER="${FIRST_SUPERUSER:-admin@numerbay.ai}"
POSTGRES_SERVER="${POSTGRES_SERVER:-db}"
POSTGRES_USER="${POSTGRES_USER:-postgres}"
POSTGRES_DB="${POSTGRES_DB:-app}"

docker run --rm \
  -e SERVER_NAME="${SERVER_NAME}" \
  -e SERVER_HOST="${SERVER_HOST}" \
  -e PROJECT_NAME="${PROJECT_NAME}" \
  -e FIRST_SUPERUSER="${FIRST_SUPERUSER}" \
  -e FIRST_SUPERUSER_PASSWORD="${FIRST_SUPERUSER_PASSWORD?Variable not set}" \
  -e POSTGRES_SERVER="${POSTGRES_SERVER}" \
  -e POSTGRES_USER="${POSTGRES_USER}" \
  -e POSTGRES_PASSWORD="${POSTGRES_PASSWORD?Variable not set}" \
  -e POSTGRES_DB="${POSTGRES_DB}" \
  "${IMAGE}" \
  bash /app/bootstrap-db.sh
