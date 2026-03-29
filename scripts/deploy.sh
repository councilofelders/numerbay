#! /usr/bin/env sh

# Exit in case of error
set -e

STACK_COMPOSE_FILE=${STACK_COMPOSE_FILE:-docker-compose.yml}
BOOTSTRAP_DB_BEFORE_DEPLOY=${BOOTSTRAP_DB_BEFORE_DEPLOY:-true}

DOMAIN=${DOMAIN?Variable not set} \
TRAEFIK_TAG=${TRAEFIK_TAG?Variable not set} \
STACK_NAME=${STACK_NAME?Variable not set} \
TAG=${TAG?Variable not set} \
docker compose \
-f "${STACK_COMPOSE_FILE}" \
config | sed '/^name:*/d' > docker-stack.yml

docker-auto-labels docker-stack.yml

sed -r "s/^(\s*SECRET_KEY\s*:\s*).*/\1${SECRET_KEY?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*FIRST_SUPERUSER_PASSWORD\s*:\s*).*/\1${FIRST_SUPERUSER_PASSWORD?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*FLOWER_BASIC_AUTH\s*:\s*).*/\1${FLOWER_BASIC_AUTH?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*POSTGRES_PASSWORD\s*:\s*).*/\1${POSTGRES_PASSWORD?Variable not set}/" -i docker-stack.yml
if [ -n "${POSTGRES_SERVER:-}" ]; then
  sed -r "s/^(\s*POSTGRES_SERVER\s*:\s*).*/\1${POSTGRES_SERVER}/" -i docker-stack.yml
fi

if [ -n "${POSTGRES_USER:-}" ]; then
  sed -r "s/^(\s*POSTGRES_USER\s*:\s*).*/\1${POSTGRES_USER}/" -i docker-stack.yml
fi

if [ -n "${POSTGRES_DB:-}" ]; then
  sed -r "s/^(\s*POSTGRES_DB\s*:\s*).*/\1${POSTGRES_DB}/" -i docker-stack.yml
fi

if [ "${BOOTSTRAP_DB_BEFORE_DEPLOY}" = "true" ]; then
  sh ./scripts/bootstrap-db.sh
fi

docker stack deploy -c docker-stack.yml --with-registry-auth --prune "${STACK_NAME?Variable not set}"
