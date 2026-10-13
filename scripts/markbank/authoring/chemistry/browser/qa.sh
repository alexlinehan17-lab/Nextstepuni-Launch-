#!/bin/bash
# Mobile browser QA for Chemistry Mark Bank cards: one isolated preview on
# :5706, one case file, then the preview is stopped. Run it under heavy.sh.
#   bash scripts/markbank/authoring/chemistry/browser/qa.sh 2026-hl
# Runs browser-<name>.mjs with the shared cases runner; screenshots, logs and
# results go to tmp/chemistry-audit/. Needs Google Chrome and playwright-core:
# set PLAYWRIGHT_CORE to its index.mjs and CHROME_PATH if Chrome lives elsewhere.
set -u
NAME="$1"
cd "$(dirname "$0")/../../../../.."
HERE=scripts/markbank/authoring/chemistry/browser
OUT=tmp/chemistry-audit
mkdir -p "$OUT"
export PLAYWRIGHT_CORE="${PLAYWRIGHT_CORE:-$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.mjs}"
PAGE="http://127.0.0.1:5706/$HERE/review.html"
npm run dev -- --host 127.0.0.1 --port 5706 --strictPort --config "$HERE/vite.config.mjs" > "$OUT/preview-$NAME.log" 2>&1 &
VITE=$!
for i in $(seq 1 90); do curl -s -o /dev/null "$PAGE" && break; sleep 1; done
# Warm the dependency optimiser once so the first case is not racing it.
curl -s -o /dev/null "$PAGE?card=chem-2026-hl-q1-a-i"; sleep 5
node "$HERE/browser-cases.mjs" "$HERE/browser-$NAME.json" "$NAME" > "$OUT/browser-$NAME.log" 2>&1
STATUS=$?
kill $VITE 2>/dev/null; pkill -P $VITE 2>/dev/null; wait $VITE 2>/dev/null
cat "$OUT/browser-$NAME.log" | tail -5
exit $STATUS
