#!/bin/bash
# One heavy session: start the Irish preview on port 5703, run browser_qa.mjs for SPEC, stop only this server.
# usage: qa.sh SPEC.json OUT_DIR
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$ROOT"
SPEC=$1; OUT=$2; mkdir -p "$OUT"
node node_modules/vite/bin/vite.js --config scripts/markbank/authoring/irish_tools/preview/vite.config.ts --host 127.0.0.1 --port 5703 --strictPort > "$OUT/dev.log" 2>&1 &
DEV=$!
trap 'kill $DEV 2>/dev/null; pkill -P $DEV 2>/dev/null; wait $DEV 2>/dev/null' EXIT
for i in $(seq 1 60); do curl -s -o /dev/null http://127.0.0.1:5703/scripts/markbank/authoring/irish_tools/preview/preview.html && break; sleep 1; done
node scripts/markbank/authoring/irish_tools/browser_qa.mjs "$SPEC" "$OUT" > "$OUT/browser.log" 2>&1
status=$?; echo "browser exit $status"; exit $status
