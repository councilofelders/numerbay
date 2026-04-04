#! /usr/bin/env sh

set -e

PROJECT_ID=${PROJECT_ID:-numerbay}
REGION=${REGION:-us-central1}
SERVICE_NAME=${SERVICE_NAME:-numerbay-api}
IMAGE=${IMAGE:-gcr.io/${PROJECT_ID}/backend:prod}
NETWORK=${NETWORK:-numerbay}
SUBNET=${SUBNET:-numerbay}
ENV_FILE=${ENV_FILE:-ops/gcp/env/backend-api-prod.env}
MIN_INSTANCES=${MIN_INSTANCES:-1}
MAX_INSTANCES=${MAX_INSTANCES:-2}
CONCURRENCY=${CONCURRENCY:-20}
MEMORY=${MEMORY:-1Gi}
CPU=${CPU:-1}
TIMEOUT=${TIMEOUT:-900s}

gcloud run deploy "${SERVICE_NAME}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --image "${IMAGE}" \
  --network "${NETWORK}" \
  --subnet "${SUBNET}" \
  --vpc-egress private-ranges-only \
  --ingress all \
  --allow-unauthenticated \
  --min-instances "${MIN_INSTANCES}" \
  --max-instances "${MAX_INSTANCES}" \
  --concurrency "${CONCURRENCY}" \
  --memory "${MEMORY}" \
  --cpu "${CPU}" \
  --timeout "${TIMEOUT}" \
  --env-vars-file "${ENV_FILE}"
