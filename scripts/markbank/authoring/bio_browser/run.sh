#!/bin/bash
# Phone-width browser check of Biology Mark Bank cards: start the dev server on
# the review port, open each card (light, or ":dark"), screenshot it before and
# after the reveal, report its images and any horizontal overflow, stop the server.
#   bash scripts/markbank/authoring/bio_browser/run.sh "bio-2023-hl-q1-a,bio-2023-ol-q2-a:dark"
# Screenshots go to $BIO_REVIEW_OUT/shots (default <tmpdir>/bio-review/shots).
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../../../.." && pwd)"
PORT="${BIO_REVIEW_PORT:-5709}"
OUT="${BIO_REVIEW_OUT:-${TMPDIR:-/tmp}/bio-review}"
mkdir -p "$OUT"
cd "$ROOT"
npx vite --host 127.0.0.1 --port "$PORT" --strictPort --config "$HERE/vite.config.ts" > "$OUT/vite.log" 2>&1 &
VITE=$!
trap 'kill $VITE 2>/dev/null; wait $VITE 2>/dev/null' EXIT
for i in $(seq 1 60); do curl -s -o /dev/null "http://127.0.0.1:$PORT/scripts/markbank/authoring/bio_browser/preview.html" && break; sleep 1; done
BIO_REVIEW_PORT="$PORT" BIO_REVIEW_OUT="$OUT" node "$HERE/browser.mjs" "$1"
