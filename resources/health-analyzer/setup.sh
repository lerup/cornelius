#!/bin/bash
# Setup script for Health Data Analyzer
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Setting up Health Data Analyzer..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Installing dependencies..."
./venv/bin/pip install --upgrade pip -q
./venv/bin/pip install -r requirements.txt -q

mkdir -p data output

echo ""
echo "Setup complete."
echo "Place your health data exports in: $SCRIPT_DIR/data/"
echo "  - Apple Health ZIP or ECG CSV files"
echo "  - Oura Ring JSON or CSV export"
echo ""
echo "Run analysis with: ./run_analyze.sh run"
