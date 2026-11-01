#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt fastapi 'uvicorn[standard]' -q
python3 -m uvicorn api:app --host 127.0.0.1 --port 8000
