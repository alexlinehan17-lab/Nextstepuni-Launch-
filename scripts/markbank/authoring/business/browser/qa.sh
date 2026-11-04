#!/bin/bash
# Browser QA for reviewed Business cards: start Vite on the Business port (5705),
# run one scenario script, stop Vite. Run through the shared heavy-check lock.
#   bash scripts/markbank/authoring/business/browser/qa.sh scripts/markbank/authoring/business/browser/browser-2020ol.mjs
cd "$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
H=scripts/markbank/authoring/business/browser/harness
SCRIPT=${1:?scenario script}
mkdir -p tmp/business-review
LOG=tmp/business-review/vite-5705.log
npx vite --config $H/vite.config.ts --host 127.0.0.1 --port 5705 --strictPort > "$LOG" 2>&1 &
VITE=$!
trap 'kill $VITE 2>/dev/null; wait $VITE 2>/dev/null' EXIT
for i in $(seq 1 60); do curl -s -o /dev/null http://127.0.0.1:5705/$H/index.html && break; sleep 1; done
node "$SCRIPT"
echo "browser exit $?"
