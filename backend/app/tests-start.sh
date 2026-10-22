#! /usr/bin/env bash
set -e

cd "$(dirname "$0")"

bash ./scripts/lint.sh

python -m app.tests_pre_start

bash ./scripts/test.sh "$@"
