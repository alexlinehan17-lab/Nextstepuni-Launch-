#!/usr/bin/env python3
"""Re-read every committed Japanese review selector from its pinned source PDF.

This independent check does not execute the authoring modules. It also runs the
physical-page census validation. Use --year to limit a checkpoint's sources.
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import fitz
from ja_paper import JaPaper
from ja_text import page_rows
from ja_review_census import reviewed_census

ROOT = Path(__file__).resolve().parents[3]


def verify(path):
    review = json.loads(path.read_text())
    year, level = review['sitting'].split('-')
    if recovery := review.get('glyphRecovery'):
        assert hashlib.sha256((ROOT / recovery['path']).read_bytes()).hexdigest() == recovery['sha256'], 'Glyph recovery proof changed'
        assert '\ufffd' not in json.dumps([review['cards'], review['selectors']], ensure_ascii=False), 'Unresolved glyph in published text'
    assert reviewed_census(int(year), level), f'{path}: no independent census'
    rows = {}
    for source in review['sources']:
        original = ROOT / source['path']
        assert hashlib.sha256(original.read_bytes()).hexdigest() == source['sha256'], original
        with fitz.open(original) as doc:
            assert source['pagesReviewed'] == list(range(1, len(doc) + 1))
            rows[source['document']] = [page_rows(page) for page in doc]
    asks = None
    for selector in review['selectors']:
        if 'parts' in selector:
            parts = []
            for part in selector['parts']:
                groups = rows[selector['document']][selector['page'] - 1][part['row']]
                parts.append(' '.join(group[2] for group in groups) if part['group'] is None else groups[part['group']][2])
            actual = ' '.join(parts)
        elif 'row' in selector:
            groups = rows[selector['document']][selector['page'] - 1][selector['row']]
            actual = ' '.join(group[2] for group in groups) if selector['group'] is None else groups[selector['group']][2]
        else:
            if asks is None:
                asks = {ask.key: ask for ask in JaPaper(int(year), level).asks()}
            actual = asks[tuple(selector['ask'])].text
        assert actual == selector['text'], f'{path}: source selector changed: {selector}'
    print(f'{review["sitting"]}: {len(review["selectors"])} original selectors and every physical source page verified')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int)
    args = parser.parse_args()
    for path in sorted((ROOT / 'scripts/markbank/authoring/reviews').glob('japanese-*.json')):
        match = re.fullmatch(r'japanese-(\d{4})-(hl|ol)\.json', path.name)
        if match and (args.year is None or int(match[1]) == args.year):
            verify(path)
