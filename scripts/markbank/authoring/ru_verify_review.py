#!/usr/bin/env python3
"""Fail if reviewed Russian claimable content does not occur on its source pages."""
import json
import re
from pathlib import Path
import fitz

ROOT = Path(__file__).resolve().parents[3]


def normal(text):
    return re.sub(r'[^\w]+', '', text.casefold())


def claims(card):
    if card['kind'] == 'question':
        for row in card['rows']:
            if row.get('group'):
                for option in row['group']['options']:
                    yield from option.split(' — ')
            else:
                yield row['verbatim']
        return
    rubric = card['rubric']
    for group in rubric.get('groups', []):
        for row in group['rows']:
            yield from row['text'].split(' — ')
    yield from rubric['taskRequirements']
    for criterion in rubric.get('criteria', []):
        yield from criterion['guidance']
        for band in criterion.get('bands', []):
            yield from band['guidance']
        for limit in criterion.get('limits', []):
            yield from limit['guidance']
            for band in limit.get('bands', []):
                yield from band['guidance']


def verify():
    cards = json.loads((ROOT / 'scripts/markbank/authored/russian-reviewed.json').read_text())
    failures = []
    count = 0
    for card in cards:
        level = 'hl' if card['level'] == 'higher' else 'ol'
        with fitz.open(ROOT / f"examiner-reports/russian/schemes/{card['year']}-{level}.pdf") as document:
            pages = sorted(set(card['review']['schemePages'] + card['review'].get('guidancePages', [])))
            versions = ['\n'.join(document[p-1].get_text(sort=sort) for p in pages) for sort in (False,True)]
            sources = [normal(version) for version in versions]
        for claim in claims(card):
            count += 1
            if not any(normal(claim) in source for source in sources):
                failures.append((card['id'], claim))
    assert not failures, '\n'.join(f'{cid}: {claim}' for cid,claim in failures)
    print(f'{len(cards)} Russian cards: {count} answer/guidance slices verified against their original scheme pages.')


if __name__ == '__main__':
    verify()
