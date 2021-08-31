#! /usr/bin/env bash
set -e

bash ./scripts/lint.sh

python /app/app/tests_pre_start.py

bash ./scripts/test.sh "$@"
