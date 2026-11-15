
#!/usr/bin/env bash

set -Eeuo pipefail

# Move to the project root directory
ROOT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"

# Configuration
PYTHON="${PYTHON:-python}"
REQUESTS="${1:-1000}"
LOG_FILE="${2:-data/generated.log}"

echo "===================================="
echo "       LOG-LENS AUTOMATION"
echo "===================================="

# Check Python
if ! command -v "$PYTHON" >/dev/null 2>&1; then
    echo "ERROR: Python not found."
    echo "Try: PYTHON=python3 bash run_project.sh"
    exit 1
fi

# Validate request count
if ! [[ "$REQUESTS" =~ ^[0-9]+$ ]]; then
    echo "ERROR: Request count must be a non-negative integer."
    exit 1
fi

# Check GNU Awk compatibility
if ! awk 'BEGIN { a[1]=1; asort(a) }' >/dev/null 2>&1; then
    echo "ERROR: GNU Awk is required."
    echo "Ensure that the awk command uses GNU Awk (gawk)."
    exit 1
fi

mkdir -p "$(dirname "$LOG_FILE")"

# Step 1: Generate logs
echo ""
echo "[1/5] Generating synthetic logs..."

"$PYTHON" python/generate_logs.py "$REQUESTS" "$LOG_FILE"

# Step 2: Python analysis
echo ""
echo "[2/5] Running Python analyzer..."

"$PYTHON" python/analyzer.py "$LOG_FILE"

# Step 3: Unix/AWK analysis
echo ""
echo "[3/5] Running Unix/AWK analyzer..."

bash unix/analyze.sh "$LOG_FILE"

# Step 4: Functional tests
echo ""
echo "[4/5] Running functional tests..."

"$PYTHON" -m unittest discover -s tests -v

# Step 5: Generate visualization
echo ""
echo "[5/5] Generating Gnuplot visualization..."

if command -v gnuplot >/dev/null 2>&1; then
    gnuplot gnuplot/status_categories.gp
    echo "Chart generated successfully."
else
    echo "WARNING: Gnuplot not found. Skipping visualization."
fi

echo ""
echo "===================================="
echo "      LOG-LENS COMPLETED"
echo "===================================="
echo "Input log: $LOG_FILE"
