#!/usr/bin/env python3
"""Inventory the FULL Irish Paper Trail scope, independently of the card builder.

This is a gap report, never a question census or proof of completeness. A paper
with cards still requires a complete visual paper/scheme and selection review.
Source hashes make later review records refer to an exact document version.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import fitz

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'scripts/markbank/authored/irish-archive-inventory.json'


def document(corpus: Path, kind: str, year: int, fileid: str | None) -> dict | None:
    if not fileid:
        return None
    path = corpus / kind / str(year) / fileid
    if not path.exists():
        return {'fileid': fileid, 'availableLocally': False}
    data = path.read_bytes()
    with fitz.open(stream=data, filetype='pdf') as pdf:
        pages = len(pdf)
    return {
        'fileid': fileid, 'availableLocally': True, 'pages': pages,
        'sha256': hashlib.sha256(data).hexdigest(),
    }


def inventory(corpus: Path) -> dict:
    result = subprocess.run([
        'node', '--input-type=module', '-e',
        "import {paperIndex} from './scripts/markbank/paperIndex.mjs';"
        'process.stdout.write(JSON.stringify(paperIndex.irish));',
    ], cwd=ROOT, capture_output=True, text=True, check=True)
    entries = json.loads(result.stdout)
    cards = json.loads((ROOT / 'components/MarkBank/cards/irish/authored.json').read_text())['cards']
    tags = json.loads((ROOT / 'scripts/paper-trail/topic-tags/tags/irish.json').read_text())
    rows = []
    seen_cards = set()
    for entry in entries:
        for paper in entry['papers']:
            fileid = paper['doc']['f']
            subset = [c for c in cards if c['year'] == entry['year']
                      and c['level'] == entry['level']
                      and c['paperFileid'] + '.pdf' == fileid]
            atlas = [t for t in tags if t['year'] == entry['year']
                     and t['level'] == entry['level'] and t['fileid'] == fileid]
            seen_cards.update(c['id'] for c in subset)
            rows.append({
                'key': f"{entry['year']}|{entry['level']}|{fileid}",
                'year': entry['year'], 'level': entry['level'],
                'label': paper['label'],
                'paper': document(corpus, 'exampapers', entry['year'], fileid),
                'scheme': document(corpus, 'markingschemes', entry['year'],
                                   paper.get('scheme', {}).get('f')),
                'markBankCardIds': [c['id'] for c in subset],
                'atlasQuestionIds': [q['n'] for t in atlas for q in t['q']],
                'questionCoverage': 'unverified' if subset else 'missing-from-mark-bank',
                'fullVisualReview': 'pending',
                'partAndSelectionReconciliation': 'pending',
                'bankAtlasTaskParity': 'pending',
            })
    return {
        'subject': 'irish',
        'scope': 'Every Irish paper component in PAPER_TRAIL_INDEX, all years and levels',
        'warning': 'Presence of cards or Atlas section anchors does not establish question-level completeness.',
        'summary': {
            'papers': len(rows),
            'years': sorted({r['year'] for r in rows}),
            'levels': sorted({r['level'] for r in rows}),
            'papersWithCards': sum(bool(r['markBankCardIds']) for r in rows),
            'papersWithoutCards': sum(not r['markBankCardIds'] for r in rows),
            'indexedCards': len(seen_cards),
            'orphanCardIds': sorted(c['id'] for c in cards if c['id'] not in seen_cards),
            'missingLocalPapers': [r['key'] for r in rows if not r['paper']['availableLocally']],
            'papersWithoutIndexedScheme': [r['key'] for r in rows if r['scheme'] is None],
            'missingLocalSchemes': [r['key'] for r in rows
                                    if r['scheme'] and not r['scheme']['availableLocally']],
            'papersPendingFullReview': len(rows),
        },
        'papers': rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus', type=Path, default=ROOT / 'paper-trail-corpus')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = inventory(args.corpus)
    content = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if not OUT.exists() or OUT.read_text() != content:
            raise SystemExit('Irish archive inventory is stale; run irish_inventory.py')
    else:
        OUT.write_text(content)
    print(json.dumps(data['summary'], ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
