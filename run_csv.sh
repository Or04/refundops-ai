#!/usr/bin/env bash
set -euo pipefail
if [ "$#" -ne 2 ]; then echo 'Usage: ./run_csv.sh input.csv output.csv' >&2; exit 2; fi
INPUT="$(python3 -c 'import os,sys;print(os.path.abspath(sys.argv[1]))' "$1")"
OUTPUT="$(python3 -c 'import os,sys;print(os.path.abspath(sys.argv[1]))' "$2")"
cd "$(dirname "$0")/product"
python3 cli.py --input "$INPUT" --output "$OUTPUT"
