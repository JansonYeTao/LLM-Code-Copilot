#!/usr/bin/env bash
set -euo pipefail

export LLM_BASE_URL="${LLM_BASE_URL:-http://127.0.0.1:8080}"
exec uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --reload
