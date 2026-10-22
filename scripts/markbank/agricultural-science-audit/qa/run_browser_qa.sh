#!/bin/bash
# usage: bash scripts/markbank/agricultural-science-audit/qa/run_browser_qa.sh <outdir> [script.mjs]
# One session: start the QA server on port 5707, run the browser script, stop the server.
set -u
cd "$(dirname "$0")/../../../.."
OUT="$1"; SCRIPT="${2:-browser_qa.mjs}"; mkdir -p "$OUT"
QA=scripts/markbank/agricultural-science-audit/qa
node_modules/.bin/vite --config $QA/vite.qa.config.ts --host 127.0.0.1 --port 5707 --strictPort > "$OUT/server.log" 2>&1 &
SERVER=$!
for i in $(seq 1 60); do curl -s -o /dev/null http://127.0.0.1:5707/$QA/reader_qa.html && break; sleep 1; done
node $QA/$SCRIPT "$OUT" "${@:3}" > "$OUT/browser.log" 2>&1
STATUS=$?
kill $SERVER; wait $SERVER 2>/dev/null
echo "browser exit $STATUS"; tail -3 "$OUT/browser.log"
exit $STATUS
