#!/bin/bash
# The per-paper gate: the seven Economics-related suites, the typecheck, then
# the mobile cases of one case file (see qa.sh). Logs and a status file go to
# tmp/economics-audit/.
#   bash scripts/markbank/authoring/economics/browser/verify.sh 2022-ol-rereview
set -u
NAME="$1"
cd "$(dirname "$0")/../../../../.."
OUT=tmp/economics-audit
mkdir -p "$OUT"
npx vitest run test/economicsCorpusReview.test.ts test/markBankSession.test.tsx test/markBankCardPreservation.test.ts \
  test/curriculumRegistry.test.ts test/markBankDeck.test.ts test/economicsExamTopics.test.ts test/markBankCoverage.test.ts \
  --maxWorkers 1 --no-file-parallelism --testTimeout 120000 > "$OUT/vitest7-$NAME.log" 2>&1
echo "vitest $?" > "$OUT/verify-$NAME.status"
npm run typecheck > "$OUT/typecheck-$NAME.log" 2>&1
echo "typecheck $?" >> "$OUT/verify-$NAME.status"
bash scripts/markbank/authoring/economics/browser/qa.sh "$NAME"
echo "browser $?" >> "$OUT/verify-$NAME.status"
cat "$OUT/verify-$NAME.status"
