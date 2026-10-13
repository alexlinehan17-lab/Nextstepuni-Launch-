#!/bin/bash
# The per-paper gate for Chemistry: every Mark Bank suite and the Chemistry
# Topic Atlas suite, the typecheck, then the mobile cases of one case file
# (see qa.sh). Run it under heavy.sh. Logs and a status file go to
# tmp/chemistry-audit/.
#   bash scripts/markbank/authoring/chemistry/browser/verify.sh 2026-hl
set -u
NAME="$1"
cd "$(dirname "$0")/../../../../.."
OUT=tmp/chemistry-audit
mkdir -p "$OUT"
npx vitest run test/markBank test/chemistryExamTopics.test.ts > "$OUT/vitest-$NAME.log" 2>&1
echo "vitest $?" > "$OUT/verify-$NAME.status"
npm run typecheck > "$OUT/typecheck-$NAME.log" 2>&1
echo "typecheck $?" >> "$OUT/verify-$NAME.status"
bash scripts/markbank/authoring/chemistry/browser/qa.sh "$NAME"
echo "browser $?" >> "$OUT/verify-$NAME.status"
cat "$OUT/verify-$NAME.status"
