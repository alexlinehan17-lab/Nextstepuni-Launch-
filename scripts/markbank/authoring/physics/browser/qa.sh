#!/bin/bash
# Mobile browser QA for Physics Mark Bank cards: one isolated preview on
# :5707, one case file, then the preview is stopped. Run it under heavy.sh.
#   bash scripts/markbank/authoring/physics/browser/qa.sh 2026-hl
# Runs browser-cases.mjs over browser-<name>.json; screenshots, logs and
# results go to tmp/physics-audit/. Needs Google Chrome and playwright-core:
# set PLAYWRIGHT_CORE to its index.mjs and CHROME_PATH if Chrome lives elsewhere.
#
# Every wait is bounded. On 2026-10-14 a verify run held the shared lock for
# hours; this script now fails fast: the preview must answer within 120 s, the
# case run is killed after QA_TIMEOUT seconds (default 900), and the preview
# is stopped on every exit path.
set -u
NAME="$1"
cd "$(dirname "$0")/../../../../.."
HERE=scripts/markbank/authoring/physics/browser
OUT=tmp/physics-audit
mkdir -p "$OUT"
export PLAYWRIGHT_CORE="${PLAYWRIGHT_CORE:-$HOME/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright-core/index.mjs}"
PAGE="http://127.0.0.1:5707/$HERE/review.html"
limit() { perl -e 'alarm shift @ARGV; exec @ARGV or die "exec: $!"' "$@"; }

npm run dev -- --host 127.0.0.1 --port 5707 --strictPort --config "$HERE/vite.config.mjs" > "$OUT/preview-$NAME.log" 2>&1 &
VITE=$!
stop() { kill $VITE 2>/dev/null; pkill -P $VITE 2>/dev/null; wait $VITE 2>/dev/null; }
trap stop EXIT INT TERM

up=0
for i in $(seq 1 120); do
  if curl -s -m 5 -o /dev/null "$PAGE"; then up=1; break; fi
  kill -0 $VITE 2>/dev/null || break
  sleep 1
done
if [ $up -ne 1 ]; then
  echo "qa.sh: the preview on :5707 did not answer within 120 s (see $OUT/preview-$NAME.log)" | tee "$OUT/browser-$NAME.log"
  exit 1
fi
limit "${QA_TIMEOUT:-900}" node "$HERE/browser-cases.mjs" "$HERE/browser-$NAME.json" "$NAME" > "$OUT/browser-$NAME.log" 2>&1
STATUS=$?
[ $STATUS -eq 142 ] && echo "qa.sh: case run exceeded ${QA_TIMEOUT:-900} s and was stopped" >> "$OUT/browser-$NAME.log"
tail -5 "$OUT/browser-$NAME.log"
exit $STATUS
