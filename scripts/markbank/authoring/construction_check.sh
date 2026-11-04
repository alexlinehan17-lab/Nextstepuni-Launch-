#!/bin/bash
# Construction Studies source checks, run from the repository root of a checkout:
#   bash scripts/markbank/authoring/construction_check.sh [outdir]
# Every paper validator, every mutation suite, every committed draft generator (which must regenerate
# without changing a tracked Construction file), the crosswalk, library and deck builds, and the
# coverage ratchet. Exit status is the number of failing steps; per-step logs go to outdir.
# The vitest suites (test/markBankConstruction*Reviewed.test.ts, constructionStudiesExamTopics,
# markBankCardPreservation, markBankCoverage, markBankDeck, markBankTopicAtlas) run separately.
ROOT=$(git rev-parse --show-toplevel) || exit 1
cd "$ROOT" || exit 1
OUT=${1:-$(mktemp -d)}; mkdir -p "$OUT"; : > "$OUT/codes.txt"
fails=0
step() { name=$1; shift; "$@" > "$OUT/$name.log" 2>&1; code=$?; echo "$name $code" >> "$OUT/codes.txt"; [ $code -ne 0 ] && fails=$((fails+1)); return 0; }
TRACKED="scripts/markbank/authored components/MarkBank/cards/construction-studies components/MarkBank/figures-construction-studies.json data/markBank/construction-studies-library-topics.json data/examTopics/construction-studies-runtime.json scripts/markbank/atlas-reviews"
snapshot() { git diff HEAD -- $TRACKED | git hash-object --stdin; git status --porcelain -- $TRACKED | grep -c '^??'; }
before=$(snapshot)
for v in $(ls scripts/markbank/authoring/construction_20*.py | sort); do
  n=$(basename "$v" .py); step "$n" python3 "$v"
done
for t in $(ls scripts/markbank/authoring/test_construction_*.py | sort); do
  n=$(basename "$t" .py); step "$n" bash -c "cd scripts/markbank/authoring && python3 -m unittest $n"
done
for g in $(git ls-files 'docs/markbank-audit/2026-09-28/drafts/construction-*/*-draft.py'); do
  step "regen-$(basename "$g" .py)" python3 "$g"
done
step crosswalk node scripts/paper-trail/build-construction-studies-exam-topic-crosswalk.mjs
step library node scripts/markbank/build-library-topic-index.mjs
step deck node scripts/markbank/build-deck.mjs scripts/markbank/authored/construction-studies.json
after=$(snapshot)
if [ "$before" = "$after" ]; then echo "no-tracked-drift 0" >> "$OUT/codes.txt"; else echo "no-tracked-drift 1" >> "$OUT/codes.txt"; fails=$((fails+1)); fi
python3 scripts/markbank/authoring/reconcile.py construction-studies --baseline check > "$OUT/reconcile.log" 2>&1
if grep -q "RATCHET:" "$OUT/reconcile.log"; then echo "reconcile-ratchet 1" >> "$OUT/codes.txt"; fails=$((fails+1)); else echo "reconcile-ratchet 0" >> "$OUT/codes.txt"; fi
cat "$OUT/codes.txt"; echo "logs: $OUT; failing steps: $fails"
exit $fails
