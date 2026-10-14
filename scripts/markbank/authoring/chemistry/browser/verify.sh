#!/bin/bash
# The per-paper gate for Chemistry: every Mark Bank suite and the Chemistry
# Topic Atlas suite, the typecheck, then the mobile cases of one case file
# (see qa.sh). Run it under heavy.sh. Logs and a status file go to
# tmp/chemistry-audit/.
#   bash scripts/markbank/authoring/chemistry/browser/verify.sh 2026-hl [2026-ol ...]
#
# Each step has its own time limit, so a stuck step fails and frees the shared
# lock instead of holding it: on 2026-10-14 vitest workers that never started
# held it for 4.5 hours. Limits (seconds) can be overridden with VITEST_TIMEOUT,
# TSC_TIMEOUT and QA_TIMEOUT; 142 in the status file means a step was stopped.
set -u
cd "$(dirname "$0")/../../../../.."
OUT=tmp/chemistry-audit
mkdir -p "$OUT"
TAG="$(IFS=+; echo "$*")"
STATUS="$OUT/verify-$TAG.status"
: > "$STATUS"
limit() { perl -e 'alarm shift @ARGV; exec @ARGV or die "exec: $!"' "$@"; }
limit "${VITEST_TIMEOUT:-1200}" npx vitest run test/markBank test/chemistryExamTopics.test.ts \
  --maxWorkers 2 --testTimeout 120000 > "$OUT/vitest-$TAG.log" 2>&1
echo "vitest $?" >> "$STATUS"
limit "${TSC_TIMEOUT:-900}" npm run typecheck > "$OUT/typecheck-$TAG.log" 2>&1
echo "typecheck $?" >> "$STATUS"
for NAME in "$@"; do
  QA_TIMEOUT="${QA_TIMEOUT:-900}" bash scripts/markbank/authoring/chemistry/browser/qa.sh "$NAME"
  echo "browser-$NAME $?" >> "$STATUS"
done
cat "$STATUS"
