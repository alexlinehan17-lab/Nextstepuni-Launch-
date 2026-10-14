#!/bin/bash
# Construction vitests one file at a time, sequentially (the Atlas test needs a larger heap):
#   bash scripts/markbank/authoring/construction_tools/vitests.sh OUTDIR
ROOT=$(git rev-parse --show-toplevel) || exit 1
cd "$ROOT" || exit 1
OUT=${1:-$(mktemp -d)}; mkdir -p "$OUT"
for f in markBankConstructionReviewedPapers constructionStudiesExamTopics markBankCardPreservation markBankDeck markBankTopicAtlas; do
  NODE_OPTIONS=--max-old-space-size=6144 npx vitest run test/$f.test.ts --maxWorkers=1 --testTimeout=900000 > "$OUT/$f.log" 2>&1; code=$?
  echo "$f exit $code $(grep -E 'Tests ' "$OUT/$f.log" | tr -s ' ')"
  grep -E "FAIL|×|heap" "$OUT/$f.log" | head -5
done
echo DONE
