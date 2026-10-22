#! /usr/bin/env bash
set -e

cd "$(dirname "$0")"

python -m app.backend_pre_start
alembic upgrade head
python -m app.initial_data
