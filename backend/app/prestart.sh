#! /usr/bin/env bash
set -e

# Let the DB start
python /app/app/backend_pre_start.py

if [ "${RUN_DB_MIGRATIONS_ON_STARTUP:-false}" = "true" ]; then
  alembic upgrade head
fi

if [ "${RUN_INIT_DATA_ON_STARTUP:-false}" = "true" ]; then
  python /app/app/initial_data.py
fi
