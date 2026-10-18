#!/usr/bin/env python3
"""Inventory every French document in Paper Trail; never infer completeness.

Usage: python3 scripts/markbank/authoring/fr_inventory.py --corpus /path/to/paper-trail-corpus
All source paths in the output are relative to that corpus, so the record is portable.
"""
from pathlib import Path
import argparse
import collections
import hashlib
import json
import fitz

ROOT = Path(__file__).resolve().parents[3]


def build(corpus):
    text = (ROOT / 'paperTrailData.ts').read_text()
    block = text.split('  "french": [', 1)[1].split('\n  ],', 1)[0]
    entries = [json.loads(line.strip().rstrip(',')) for line in block.splitlines() if line.strip()]
    # Reviewed window only: June sittings from 2010.
    entries = [entry for entry in entries if not entry.get('sitting') and entry['year'] >= 2010]
    sources = {}
    papers = []
    for entry in entries:
        for item in entry['papers']:
            source_keys = {}
            for kind, folder, doc in [('paper', 'exampapers', item['doc']),
                                      ('scheme', 'markingschemes', item.get('scheme'))]:
                if not doc:
                    source_keys[kind] = None
                    continue
                key = f'{folder}/{entry["year"]}/{doc["f"]}'
                source_keys[kind] = key
                if key in sources:
                    continue
                source = corpus / key
                if not source.exists():
                    raise FileNotFoundError(key)
                data = source.read_bytes()
                if len(data) != doc['b']:
                    raise ValueError(f'{key}: local bytes {len(data)} differ from Paper Trail {doc["b"]}')
                with fitz.open(source) as pdf:
                    page_count = len(pdf)
                sources[key] = dict(bytes=len(data), pages=page_count, sha256=hashlib.sha256(data).hexdigest())
            papers.append(dict(year=entry['year'], level=entry['level'], lang=entry['lang'],
                               label=item['label'], **source_keys))
    result = dict(subject='french', status='inventory-verified-review-in-progress',
                  scope='Every French Higher and Ordinary Level paper currently in Paper Trail, including translated editions.',
                  years=sorted(set(p['year'] for p in papers)), paperVariants=len(papers),
                  sourceDocuments=len(sources), sources=sources, papers=papers,
                  completionRequirements=[
                      'Visual sweep of every paper and corresponding scheme.',
                      'Every independently practicable tariff boundary and finite answer route carded.',
                      'All original Mark Bank card IDs and content retained unless independently corrected.',
                      'Exact task/topic parity in Mark Bank and Topic Atlas.',
                      'Required passages, illustrations, forms and recordings available before reveal.',
                      'No unresolved tasks or orphaned cards; no parser count used as independent proof.',
                  ])
    output = ROOT / 'scripts/markbank/authoring/french-corpus-inventory.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(dict(paperVariants=len(papers), sourceDocuments=len(sources),
                          paperVariantsByYear=dict(sorted(collections.Counter(p['year'] for p in papers).items())))))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=Path, required=True)
    build(parser.parse_args().corpus)
