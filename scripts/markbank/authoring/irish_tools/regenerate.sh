#!/bin/bash
# Regenerate every committed Irish ledger, card file and Atlas output, or verify them byte-for-byte.
#
#   regenerate.sh            rebuild everything in dependency order (ledgers, legacy cards, reviewed
#                            components, then the Atlas chain twice)
#   regenerate.sh --check    verify: every ledger maker and generator reproduces its committed file,
#                            and re-running the Atlas chain leaves the working tree unchanged
#
# Needs the local paper-trail-corpus PDFs (gitignored). Run from any directory.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$ROOT"
A=scripts/markbank/authoring
MODE=${1:-}
LEDGERS=$(ls $A/irish_ledgers/*.py | grep -v '/_ledger.py$')
GENERATORS="irish_foundation_2010.py irish_foundation_2011.py irish_foundation_2012.py irish_foundation_2013.py irish_foundation_2014.py
 irish_foundation_2015.py irish_foundation_2016.py irish_foundation_2017.py irish_foundation_2018.py irish_foundation_2019.py
 irish_foundation_2020.py irish_foundation_2021.py irish_foundation_2022.py irish_foundation_2023.py irish_foundation_2024.py
 irish_foundation.py irish_foundation_2026.py irish_higher_2026_p1.py irish_higher_2026_p2.py irish_ordinary_2026_p1.py
 irish_ordinary_2026_p2.py irish_higher_2025_p1.py irish_higher_2025_p2.py irish_ordinary_2025_p1.py irish_ordinary_2025_p2.py
 irish_higher_2024_p1.py irish_ordinary_2024_p1.py irish_ordinary_2024_p2.py"
OUTPUTS="components/MarkBank/cards/irish data/examTopics data/paperTrail public/paper-anchors public/paper-answers
 scripts/paper-trail/answers scripts/paper-trail/topic-tags/tags/irish.json scripts/markbank/authored"

if [ "$MODE" = "--check" ]; then
  # Compares the working tree with the index: stage (or commit) intended changes before checking.
  if ! git diff --quiet -- $OUTPUTS; then echo "Unstaged Irish output changes; stage or commit them before --check." >&2; exit 2; fi
  for m in $LEDGERS; do python3 "$m" --check; done
  python3 $A/irish_cards.py --check
  for g in $GENERATORS; do
    if ! python3 "$A/$g" --check >/dev/null; then echo "STALE: $g does not reproduce its committed output" >&2; exit 1; fi
    echo "OK $g"
  done
fi
if [ "$MODE" != "--check" ]; then
  for m in $LEDGERS; do python3 "$m"; done
  python3 $A/irish_cards.py
  for g in $GENERATORS; do python3 "$A/$g"; done
fi
# The Atlas chain reads the card files and its own previous sidecars, so it runs twice: the
# second pass must change nothing (idempotence), and in --check mode nothing may change at all.
for pass in 1 2; do
  node scripts/paper-trail/build-irish-exam-topic-crosswalk.mjs > /dev/null
  node scripts/paper-trail/topic-tags/build-tags.mjs > /dev/null
  python3 $A/irish_inventory.py > /dev/null
done
if [ "$MODE" = "--check" ]; then
  git diff --exit-code --stat -- $OUTPUTS && echo "IRISH OUTPUTS REPRODUCE BYTE-IDENTICALLY"
fi
