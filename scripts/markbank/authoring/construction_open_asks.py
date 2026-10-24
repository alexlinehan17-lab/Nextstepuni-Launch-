#!/usr/bin/env python3
"""Re-measure Construction Studies coverage and write the declared open asks.

    python3 scripts/markbank/authoring/construction_open_asks.py            # write the asks file only
    python3 scripts/markbank/authoring/construction_open_asks.py --baseline # also rewrite the coverage baseline

Runs reconcile.py for construction-studies and writes
docs/markbank-audit/2026-09-28/construction-open-asks.json: the baseline entry, every paper with its
leaves, covered count and open asks, and a note naming the papers whose theory component is fully
source-reviewed (read from the reviewed files, never typed). Open asks are declared, never hidden.
"""
import argparse
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

R = Path(__file__).resolve().parents[3]
OUT = R / 'docs/markbank-audit/2026-09-28/construction-open-asks.json'
RECONCILE = R / 'scripts/markbank/authoring/reconcile.py'
COMMAND = 'python3 scripts/markbank/authoring/reconcile.py construction-studies --baseline write'


def reviewed_papers():
    papers = []
    for f in sorted((R / 'scripts/markbank/authored').glob('construction-studies-*-reviewed.json')):
        d = json.loads(f.read_text())
        if d.get('paperComplete') and d.get('component') == 'theory':
            papers.append((d['year'], d['level']))
    return [f'{y} {lvl.capitalize()}' for y, lvl in sorted(papers)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--baseline', action='store_true', help='rewrite the construction-studies coverage baseline first')
    args = ap.parse_args()
    if args.baseline:
        subprocess.run([sys.executable, str(RECONCILE), 'construction-studies', '--baseline', 'write'], cwd=R, check=False)
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / 'reconcile.json'
        subprocess.run([sys.executable, str(RECONCILE), 'construction-studies', '--json', str(out)], cwd=R,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
        d = json.loads(out.read_text())
    b = json.loads((R / 'scripts/markbank/coverage-baseline.json').read_text())['construction-studies']
    papers = [dict(year=p['year'], level=p['level'], leaves=p['leaves'], covered=p['covered'], open=p['open']) for p in d['papers'] if p['leaves']]
    note = ('Legacy census denominator (2010–2026 written papers, English editions). Open asks are declared here, never hidden: '
            'they are papers not yet source-reviewed. Fully source-reviewed and reconciled: ' + ', '.join(reviewed_papers()) +
            ' theory. Practical components and Irish editions are outside this census.')
    result = dict(subjectId='construction-studies', measuredAt=datetime.now(timezone.utc).isoformat(), command=COMMAND, baseline=b,
                  note=note, openTotal=sum(len(p['open']) for p in papers), papers=papers)
    assert result['openTotal'] == b['open'] == d['open'], (result['openTotal'], b['open'], d['open'])
    assert b['orphans'] == 0 == len(d['orphans']), 'orphan cards'
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(f"{OUT.relative_to(R)}: {result['openTotal']} open asks; baseline {b['covered']}/{b['leaves']}, {b['cards']} cards")


if __name__ == '__main__':
    main()
