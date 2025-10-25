#! /usr/bin/env bash

# Let the DB start
echo "running backend_pre_start.py"
python /app/app/backend_pre_start.py

# Run migrations
echo "running migrations"
alembic upgrade head

# Create initial data in DB
echo "initial data"
python /app/app/initial_data.py
echo "all done"
