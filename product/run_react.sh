#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
python3 -m pip install -r requirements.txt fastapi 'uvicorn[standard]' >/dev/null
if [ ! -d web/node_modules ]; then (cd web && npm install); fi
python3 -m uvicorn api:app --host 127.0.0.1 --port 8000 &
API_PID=$!
trap 'kill "$API_PID" 2>/dev/null || true' EXIT
cd web
npm run dev
