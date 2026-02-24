#!/bin/bash

# Function to kill background processes on exit
cleanup() {
    echo ""
    echo "--- Stopping servers ---"
    # Kill the entire process group to ensure subshells and pipes are cleaned up
    kill $(jobs -p) 2>/dev/null
    echo "Servers stopped."
    exit
}

# Trap Ctrl+C (SIGINT) and call cleanup
trap cleanup SIGINT

# Absolute path to project root
PROJECT_ROOT=$(pwd)

echo "--- Starting Project Development Servers with Prefixed Logging ---"

# Start Backend
echo "1. Starting Backend (Port 5001)..."
(
    cd "$PROJECT_ROOT/backend"
    if [ -d ".venv" ]; then
        source .venv/bin/activate
    fi
    # -u for unbuffered output
    python -u main.py 2>&1 | while read -r line; do echo -e "\033[0;34m[BACKEND]\033[0m $line"; done
) &

# Start Frontend
echo "2. Starting Frontend (Vite)..."
(
    cd "$PROJECT_ROOT"
    npm run dev 2>&1 | while read -r line; do echo -e "\033[0;32m[FRONTEND]\033[0m $line"; done
) &

echo "--- Both servers are running! ---"
echo "--- Press Ctrl+C at any time to stop both. ---"

# Wait for background jobs
wait
