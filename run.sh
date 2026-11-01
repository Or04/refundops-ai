#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/product"
exec bash ./run.sh
