#!/bin/bash
# Wrapper script for health data analysis
# Usage: ./run_analyze.sh scan
#        ./run_analyze.sh run [--ecg-only] [--oura-only] [--date YYYY-MM-DD] [--last N]
#        ./run_analyze.sh ecg /path/to/file.csv
#        ./run_analyze.sh oura /path/to/file.json

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ ! -d "$SCRIPT_DIR/venv" ]; then
    echo "Error: Virtual environment not found. Run setup first:"
    echo "  cd $SCRIPT_DIR && bash setup.sh"
    exit 1
fi

"$SCRIPT_DIR/venv/bin/python" "$SCRIPT_DIR/analyze.py" "$@"
