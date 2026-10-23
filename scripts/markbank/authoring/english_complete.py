#!/usr/bin/env python3
"""Audit English against every paper in the application's Paper Trail index.

This ledger is an inventory, not a completeness certificate. In particular,
existing answer-map blocks and legacy Mark Bank cards are not task counts.
Paper/scheme review and finite-choice reconciliation remain separate gates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess

import fitz

ROOT = Path(__file__).resolve().parents[3]
CORPUS = ROOT / 'paper-trail-corpus'
OUTPUT = ROOT / 'scripts/markbank/authored/english-paper-inventory.json'


def paper_index():
    return json.loads(subprocess.check_output([
        'node', '--input-type=module', '-e',
        'import {paperIndex} from "./scripts/markbank/paperIndex.mjs";'
        'process.stdout.write(JSON.stringify(paperIndex.english));',
    ], cwd=ROOT, text=True))


def document_record(path):
    if not path.is_file():
        raise FileNotFoundError(f'Paper Trail source missing: {path}')
    with fitz.open(path) as doc:
        return {
            'path': str(path.relative_to(ROOT)),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'pages': len(doc),
        }


def inventory():
    authored = json.loads((ROOT / 'components/MarkBank/cards/english/authored.json').read_text())
    papers = []
    for entry in sorted(paper_index(), key=lambda e: (e['year'], e['level'])):
        if entry['lang'] != 'ev':
            raise ValueError('Unclassified English paper language: ' + entry['lang'])
        for item in entry['papers']:
            number = {'Paper One': 1, 'Paper Two': 2}[item['label']]
            paper_file = item['doc']['f']
            scheme_file = item['scheme']['f']
            sidecar_path = ROOT / 'scripts/paper-trail/answers' / str(entry['year']) / (paper_file + '.json')
            sidecar = json.loads(sidecar_path.read_text()) if sidecar_path.is_file() else None
            if sidecar and (sidecar['paperFileid'] != paper_file or sidecar['schemeFileid'] != scheme_file):
                raise ValueError(f'{sidecar_path}: document identity disagrees with Paper Trail')
            cards = [c for c in authored['cards'] if c['year'] == entry['year']
                     and c['level'] == entry['level'] and c['paper'] == number]
            papers.append({
                'id': f"english-{entry['year']}-{'hl' if entry['level'] == 'higher' else 'ol'}-p{number}",
                'year': entry['year'], 'level': entry['level'], 'paper': number,
                'paperFileid': paper_file, 'schemeFileid': scheme_file,
                'questionPaper': document_record(CORPUS / 'exampapers' / str(entry['year']) / paper_file),
                'markingScheme': document_record(CORPUS / 'markingschemes' / str(entry['year']) / scheme_file),
                'answerMapPresent': sidecar is not None,
                'answerMapBlocks': len(sidecar['q']) if sidecar else 0,
                'markBankCards': len(cards),
            })
    return {
        'subject': 'english',
        'scope': 'Every English question paper in PAPER_TRAIL_INDEX, both levels and both papers.',
        'evidenceRule': 'Inventory and parser counts do not prove task, choice, source-material or topic completeness.',
        'paperCount': len(papers),
        'papers': papers,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    payload = inventory()
    rendered = json.dumps(payload, ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text() != rendered:
            raise SystemExit('English paper inventory is stale; run english_complete.py')
    else:
        OUTPUT.write_text(rendered)
    print(f"English: {payload['paperCount']} indexed papers; "
          f"{sum(p['markBankCards'] == 0 for p in payload['papers'])} have no Mark Bank cards; "
          f"{sum(not p['answerMapPresent'] for p in payload['papers'])} lack an answer map.")


if __name__ == '__main__':
    main()
