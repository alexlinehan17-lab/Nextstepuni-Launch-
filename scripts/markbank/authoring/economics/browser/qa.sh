#!/bin/bash
# Mobile browser QA for the Economics Mark Bank cards: one isolated preview on
# :5706, one case file, then the preview is stopped.
#   bash scripts/markbank/authoring/economics/browser/qa.sh 2023-hl-rereview
#   bash scripts/markbank/authoring/economics/browser/qa.sh iv-checks
# Runs browser-<name>.mjs. Screenshots, logs and results go to tmp/economics-audit/.
# Needs Google Chrome and playwright-core; set PLAYWRIGHT_CORE to its index.mjs
# (default: the Codex runtime copy) and CHROME_PATH if Chrome lives elsewhere.
set -u
NAME="$1"
cd "$(dirname "$0")/../../../../.."
HERE=scripts/markbank/authoring/economics/browser
OUT=tmp/economics-audit
mkdir -p "$OUT"
export PLAYWRIGHT_CORE="${PLAYWRIGHT_CORE:-$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.mjs}"
PAGE="http://127.0.0.1:5706/$HERE/review.html"
npm run dev -- --host 127.0.0.1 --port 5706 --strictPort --config "$HERE/vite.config.mjs" > "$OUT/preview-$NAME.log" 2>&1 &
VITE=$!
for i in $(seq 1 60); do curl -s -o /dev/null "$PAGE" && break; sleep 1; done
# Warm the dependency optimiser once so the first case is not racing it.
curl -s -o /dev/null "$PAGE?card=econ-2026-hl-sa-q1-a"; sleep 5
node "$HERE/browser-$NAME.mjs" > "$OUT/browser-$NAME.log" 2>&1
STATUS=$?
kill $VITE 2>/dev/null; pkill -P $VITE 2>/dev/null; wait $VITE 2>/dev/null
exit $STATUS
