#!/bin/bash
set -e

poetry run bandit -r animelister/ -l -x tests.py
poetry run isort --check-only animelister/**/*.py
poetry run black --check --diff --exclude=/migrations/ animelister/
poetry run prospector -I "animelister/settings/*"
