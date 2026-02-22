#!/bin/bash
export BRAIN_PATH="/Users/alexanderruppert/Desktop/Claude/OBSIDIAN VAULT"
SCRIPT_DIR="/Users/alexanderruppert/Desktop/Claude/cornelius/resources/local-brain-search"
PYTHON="$SCRIPT_DIR/venv/bin/python"
SEARCH="$SCRIPT_DIR/search.py"

echo "=== SEARCH 1: European Defense ==="
$PYTHON $SEARCH "European defense sovereignty military startups venture capital defense technology drones Ukraine" --limit 8 --json

echo ""
echo "=== SEARCH 2: Europe Trillion Dollar Startup ==="
$PYTHON $SEARCH "Europe trillion dollar startup innovation technology founders venture capital tech companies economic growth" --limit 8 --json

echo ""
echo "=== SEARCH 3: Chinese Century ==="
$PYTHON $SEARCH "China century manufacturing dominance state capacity technology innovation geopolitical power economic rise" --limit 8 --json

echo ""
echo "=== SEARCH 4: Death of the West ==="
$PYTHON $SEARCH "Europe NATO Trump Russia Ukraine alliance defense spending geopolitical order collapse Western world" --limit 8 --json

echo ""
echo "=== SEARCH 5: We're All Soviets Now ==="
$PYTHON $SEARCH "America Soviet Union decline institutional decay deaths of despair healthcare deficit military spending Cold War" --limit 8 --json

echo ""
echo "=== SEARCH 6: Authoritarian Europe ==="
$PYTHON $SEARCH "European Union civil liberties surveillance privacy regulation crypto authoritarian government overreach" --limit 8 --json

echo ""
echo "=== SEARCH 7: Sociopolitical Collapse ==="
$PYTHON $SEARCH "sociopolitical collapse complexity diminishing returns Rome civilization decline abundance agenda energy" --limit 8 --json
