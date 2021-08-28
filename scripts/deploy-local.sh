#! /usr/bin/env sh

# Exit in case of error
set -e

docker network create --driver=overlay traefik-public || true
export NODE_ID=$(docker info -f '{{.Swarm.NodeID}}')
docker node update --label-add traefik-public.traefik-public-certificates-live=true $NODE_ID
DOMAIN=traefik.localhost.tiangolo.com EMAIL=admin@numerbay.ai USERNAME=admin PASSWORD=changethis \
  HASHED_PASSWORD=$(openssl passwd -apr1 changethis) docker stack deploy -c docker-compose.traefik.yml traefik

export TRAEFIK_TAG=numerbay.ai STACK_NAME=numerbay-ai TAG=prod DOMAIN=localhost.tiangolo.com
export SECRET_KEY=bc595a8c7d1634c18d6d72b41912b270314383c7289c7358591174a33d4e0517
export FIRST_SUPERUSER_PASSWORD=d8264886c4b3c1c87838cfbb962e804c2d3b5e835303867d8a108644e03c772b
export FLOWER_BASIC_AUTH=admin:d8264886c4b3c1c87838cfbb962e804c2d3b5e835303867d8a108644e03c772b
export POSTGRES_PASSWORD=ad5a3cdcd8e85220cd9364453d6f809a6e3189cccc6583c3392fac0e102c77e6
export PGADMIN_DEFAULT_PASSWORD=cbd572a062fa8cdc3a2192816235882b78154ce140be51d490780a26def9560c
bash ./scripts/deploy.sh