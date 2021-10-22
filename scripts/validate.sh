#!/bin/bash
set -e

bandit -r animelister/ -l -x tests.py
isort --check-only animelister/**/*.py
black --check --diff --exclude=/migrations/ animelister/
prospector -I "animelister/settings/*"
