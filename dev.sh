#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "🌱 Starting digital garden sync..."
python3 sync.py

# Start watcher in the background
python3 sync.py --watch &
WATCHER_PID=$!

# Cleanup on exit
cleanup() {
    echo -e "\n🧹 Stopping background file watcher..."
    kill $WATCHER_PID 2>/dev/null
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

echo "🚀 Starting Hugo preview server..."
../bin/hugo server -D --port 1313 --bind 127.0.0.1
