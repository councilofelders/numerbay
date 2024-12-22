#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=${DOMAIN?Variable not set} \
TRAEFIK_TAG=${TRAEFIK_TAG?Variable not set} \
STACK_NAME=${STACK_NAME?Variable not set} \
TAG=${TAG?Variable not set} \
docker compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml

sed -r "s/^(\s*SECRET_KEY\s*:\s*).*/\1${SECRET_KEY?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*FIRST_SUPERUSER_PASSWORD\s*:\s*).*/\1${FIRST_SUPERUSER_PASSWORD?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*FLOWER_BASIC_AUTH\s*:\s*).*/\1${FLOWER_BASIC_AUTH?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*POSTGRES_PASSWORD\s*:\s*).*/\1${POSTGRES_PASSWORD?Variable not set}/" -i docker-stack.yml
sed -r "s/^(\s*PGADMIN_DEFAULT_PASSWORD\s*:\s*).*/\1${PGADMIN_DEFAULT_PASSWORD?Variable not set}/" -i docker-stack.yml
cat docker-stack.yml

docker stack deploy -c docker-stack.yml --with-registry-auth "${STACK_NAME?Variable not set}"
