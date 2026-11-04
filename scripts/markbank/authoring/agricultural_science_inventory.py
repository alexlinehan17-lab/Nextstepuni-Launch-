#!/usr/bin/env python3
"""Inventory EVERY Agricultural Science Paper Trail document for manual review.

The output is a work queue, never a completeness certificate. Question-parser
counts cannot prove coverage. Source changes invalidate the recorded hashes;
selection directives stay pending until classified against paper and scheme.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'scripts/markbank/authored/agricultural-science-inventory.json'
DIRECTIVE = re.compile(
    r'\b(?:choose|select|either|any\s+(?:one|two|three|four|five|six|seven|eight|nine|ten|\d+)|'
    r'one\s+of|two\s+of|answer\s+(?:all|one|two|three|four|five|six|seven|eight|nine|ten|\d+)|'
    r'roghnaigh|roghnaítear|freagair|ceachtar|dhá cheann|trí cinn)\b', re.I)


def inventory():
    entries = json.loads(subprocess.check_output([
        'node', '--input-type=module', '-e',
        'import {paperIndex} from "./scripts/markbank/paperIndex.mjs"; console.log(JSON.stringify(paperIndex["agricultural-science"]));',
    ], cwd=ROOT, text=True))
    authored = json.loads((ROOT / 'scripts/markbank/authored/agricultural-science.json').read_text())
    reviews = json.loads((ROOT / 'scripts/markbank/authored/agricultural-science-reviewed-tasks.json').read_text()).get('paperReviews', [])
    papers = []
    for entry in sorted(entries, key=lambda e: (e['year'], e['level'], e['lang'])):
        for booklet in entry['papers']:
            files = {}
            directives = []
            for kind, prop in [('exampapers', 'doc'), ('markingschemes', 'scheme')]:
                assert prop in booklet, f'Missing {prop}: {entry}'
                path = ROOT / 'paper-trail-corpus' / kind / str(entry['year']) / booklet[prop]['f']
                assert path.is_file(), f'Missing source: {path}'
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                with fitz.open(path) as pdf:
                    files[prop] = {'fileid': path.name, 'sha256': digest, 'pages': len(pdf)}
                    if prop == 'doc':
                        for index, page in enumerate(pdf):
                            text = ' '.join(page.get_text().split())
                            for match in DIRECTIVE.finditer(text):
                                context = text[max(0, match.start()-90):match.end()+230]
                                key = hashlib.sha256(f'{digest}|{index+1}|{match.start()}|{context}'.encode()).hexdigest()[:16]
                                directives.append({'id': key, 'page': index+1, 'cue': match.group(),
                                                   'context': context, 'classification': 'pending'})
            papers.append({
                'year': entry['year'], 'level': entry['level'], 'lang': entry['lang'],
                'label': booklet['label'], **files,
                'authoredEnglishCardsForSitting': sum(c['year'] == entry['year'] and c['level'] == entry['level'] for c in authored),
                'wholePaperVisualReview': 'pending', 'schemeBoundaryReview': 'pending',
                'selectionDirectives': directives,
            })
            reviewed = next((r for r in reviews if (r['year'],r['level'],r['lang'],r['paperFileid']) ==
                             (entry['year'],entry['level'],entry['lang'],files['doc']['fileid'])), None)
            if reviewed:
                assert reviewed['hashes'] == {kind:files[prop]['sha256'] for kind,prop in [('exampapers','doc'),('markingschemes','scheme')]}, 'Reviewed source changed'
                classified = {cue['id']:cue for cue in reviewed['selectionDirectives']}
                assert set(classified) == {cue['id'] for cue in directives}, 'Stale/unclassified raw selection'
                papers[-1].update({key:reviewed[key] for key in ['wholePaperVisualReview','schemeBoundaryReview']})
                papers[-1]['selectionDirectives'] = [classified[cue['id']] for cue in directives]
    return {'subjectId': 'agricultural-science', 'status': 'in-progress',
            'source': 'paperTrailData.ts PAPER_TRAIL_INDEX', 'booklets': len(papers),
            'warning': 'This is an inventory and review queue. It does not prove complete question coverage.',
            'papers': papers}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    data = inventory()
    if args.write:
        OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n')
    elif args.check:
        assert json.loads(OUT.read_text()) == data, 'Inventory stale: source corpus or authored cards changed'
    print(f'{data["booklets"]} indexed booklets and matching schemes; '
          f'{sum(c["classification"] == "pending" for p in data["papers"] for c in p["selectionDirectives"])} selection cues pending classification')


if __name__ == '__main__':
    main()
