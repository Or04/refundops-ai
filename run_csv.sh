#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo 'Usage: ./run_csv.sh input.csv output.csv' >&2; exit 2; fi
cd "$(dirname "$0")/product"
python3 cli.py --input "$1" --output "$2"
