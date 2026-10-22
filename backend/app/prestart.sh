#! /usr/bin/env bash
set -e

# Sourced by the base image's /start.sh before gunicorn starts.
# Migrations and seed data run in the numerbay-job-bootstrap-db Cloud Run job.

# Let the DB start
python -m app.backend_pre_start
