#!/bin/bash
cd "$(dirname "$0")"
poetry run pytest tests/ -v --tb=short --cov=src --cov-report=term-missing
