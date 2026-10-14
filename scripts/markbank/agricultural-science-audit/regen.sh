#!/bin/bash
# Regenerate every Agricultural Science derived artefact and run the checks. Run from the worktree root.
# usage: bash scripts/markbank/agricultural-science-audit/regen.sh <year>-<hl|ol>   (the paper whose cards to lint and claim-check)
set -e
T=tmp/agricultural-science-audit; mkdir -p $T
cd scripts/markbank/authoring
python3 agricultural_science_completion.py --write | tail -1
python3 agricultural_science_atlas.py --write 2>&1 | tail -1
cd ../../..
node scripts/markbank/build-deck.mjs scripts/markbank/authored/agricultural-science.json 2>&1 | grep -i "LEDGER\|built\|DROP\|error\|stale\|untrace" | head
cd scripts/markbank/authoring
python3 agricultural_science_inventory.py --write | tail -1
python3 agricultural_science_census.py --write | tail -c 80; echo
python3 agricultural_science_reconcile.py --write --check-reviewed | tail -1
for m in completion atlas inventory census; do python3 agricultural_science_$m.py --check 2>&1 | tail -1 | cut -c1-70; done
cd ../../..
python3 scripts/markbank/authoring/cardlint.py agricultural-science 2>&1 | grep "agsci-$1" || echo "cardlint: no $1 hits"
# The ledger reads the census written above, and the atlas reads the built deck: build again, then re-map.
node scripts/markbank/build-deck.mjs scripts/markbank/authored/agricultural-science.json 2>&1 | grep -i "LEDGER\|built"
(cd scripts/markbank/authoring && python3 agricultural_science_atlas.py --write >/dev/null && python3 agricultural_science_atlas.py --check 2>&1 | tail -1 | cut -c1-60)
python3 scripts/markbank/authoring/reconcile.py agricultural-science --baseline write 2>&1 | tail -1
python3 -c "
import json,sys; d=[c for c in json.load(open('scripts/markbank/authored/agricultural-science.json')) if c['id'].startswith('agsci-$1')]
json.dump(d,open('$T/claim.json','w'))"
node scripts/markbank/agricultural-science-audit/claimcheck.mjs $PWD $T/claim.json | tail -3
