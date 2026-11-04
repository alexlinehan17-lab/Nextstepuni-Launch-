#!/usr/bin/env python3
"""Fail closed on unreviewed choice wording in the original French papers.

The review ledger is independent of card generation. It pins the source
document and every detected phrase, including non-task uses and MCQ distractors.
Run --list to inspect candidates; this never writes or approves a review.
"""
from pathlib import Path
import argparse
import hashlib
import json
import math
import re
import fitz

ROOT = Path(__file__).resolve().parents[3]
LEDGER = Path(__file__).with_name('french-selection-review.json')
NUMBER = r'(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)'
DIRECTIVE = re.compile(
    rf'\b(?:choos\w*|chois\w*|select(?:ion|ing|ed)?|either|any\s+{NUMBER}'
    rf'|{NUMBER}\s+of\b|answer\s+(?:any\s+)?{NUMBER}'
    r'|répondez\s+à\s+(?:une|deux|trois|\([a-z]\))'
    r'|(?:une|deux|trois)\s+des\s+questions|choix\s+multiple'
    r'|réel\s+ou\s+imaginaire)(?!\w)|(?m:^\s*(?:OU|OR)\s*$)', re.I)
POLICIES = {
    'independent-tasks', 'finite-pool', 'required-response',
    'open-scope', 'mcq-answer', 'source-content', 'exam-administration',
}


def scan_paper(path):
    rows = []
    with fitz.open(path) as doc:
        for page, pdf_page in enumerate(doc, 1):
            # Preserve standalone OU and join wrapped prose for "three of".
            raw = '\n'.join(' '.join(line.split()) for line in pdf_page.get_text().splitlines())
            for index, match in enumerate(DIRECTIVE.finditer(raw), 1):
                phrase = ' '.join(match.group().split())
                context = ' '.join(raw[max(0, match.start()-90):match.end()+180].split())
                digest = hashlib.sha256(context.encode()).hexdigest()[:12]
                rows.append(dict(key=f'{page}:{index}:{digest}', page=page,
                                 phrase=phrase, context=context))
    return rows


def verify_paper(path, ledger=None, *, pages=None):
    ledger = ledger if ledger is not None else json.loads(LEDGER.read_text())
    record = ledger['papers'].get(path.name)
    if not record and pages:
        record = ledger['papers'].get(path.name + '#pages=' + ','.join(map(str, sorted(pages))))
    if not record:
        raise ValueError(f'Unreviewed French selection source: {path.name}')
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if record['sha256'] != digest:
        raise ValueError(f'French selection source changed: {path.name}')
    actual = scan_paper(path)
    if record.get('pages'):
        if sorted(pages or []) != record['pages']:
            raise ValueError(f'French selection review does not cover the requested pages: {path.name}')
        actual = [row for row in actual if row['page'] in pages]
    reviewed = record['directives']
    if len({row['key'] for row in reviewed}) != len(reviewed):
        raise ValueError(f'Duplicate French selection review: {path.name}')
    if {row['key'] for row in actual} != {row['key'] for row in reviewed}:
        raise ValueError(f'Unclassified or stale French choice directive: {path.name}')
    for source in actual:
        row = next(row for row in reviewed if row['key'] == source['key'])
        if any(row.get(key) != value for key, value in source.items()):
            raise ValueError(f'French selection text mismatch: {path.name}/{source["key"]}')
        if row.get('policy') not in POLICIES or not row.get('reason'):
            raise ValueError(f'French selection decision missing: {path.name}/{source["key"]}')
        if row['policy'] == 'finite-pool' and not row.get('task'):
            raise ValueError(f'French selection has no expansion task: {path.name}/{source["key"]}')
        if row['policy'] == 'finite-pool' and row.get('routes') != math.comb(row['poolSize'], row['choose']):
            raise ValueError(f'French selection route count is wrong: {path.name}/{source["key"]}')
    return actual


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('papers', nargs='+', type=Path)
    parser.add_argument('--list', action='store_true')
    args = parser.parse_args()
    for path in args.papers:
        rows = scan_paper(path) if args.list else verify_paper(path)
        print(json.dumps(dict(paper=path.name, directives=rows), ensure_ascii=False, indent=2))
