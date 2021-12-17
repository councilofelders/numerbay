#!/usr/bin/env bash

set -x

mypy app
black app
isort --recursive app
flake8
