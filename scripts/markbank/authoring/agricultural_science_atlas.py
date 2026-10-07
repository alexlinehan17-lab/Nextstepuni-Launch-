#!/usr/bin/env python3
"""Publish reviewed practice tasks in Topic Atlas, preserving whole-question IDs.

These eight crops were inspected against the PDF pages. The rest of the corpus
is intentionally not labelled complete. IDs 1001+ are additive, stable practice
identities; the existing 1–18 question cards and their saved progress survive.
"""
import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / 'data/examTopics/agricultural-science-question-runtime.json'

# Prefix, exact paper range, exact scheme range. Include the source artwork in
# each question crop and stop before the next independently marked part.
REGIONS = {
    'agsci-2022-ol-q2bii-route-': ([0, .089, 1, .596], [0, .618, 1, .732]),
    'agsci-2023-hl-q18ai-route-': ([0, .066, 1, .386], [0, .317, 1, .559]),
    'agsci-2022-ol-q13bi': ([0, .066, 1, .383], [0, .085, 1, .149]),
    'agsci-2025-ol-q8b': ([0, .529, 1, .808], [0, .370, 1, .419]),
}
# Explicit assignments survive reordering the authored deck or adding cards.
NUMBERS = {
    'agsci-2022-ol-q2bii-route-e': '1001',
    'agsci-2022-ol-q2bii-route-f': '1002',
    'agsci-2022-ol-q13bi': '1003',
    'agsci-2023-hl-q18ai-route-abc': '1001',
    'agsci-2023-hl-q18ai-route-abd': '1002',
    'agsci-2023-hl-q18ai-route-acd': '1003',
    'agsci-2023-hl-q18ai-route-bcd': '1004',
    'agsci-2025-ol-q8b': '1001',
}


def outputs():
    review = json.loads((ROOT / 'scripts/markbank/authored/agricultural-science-reviewed-tasks.json').read_text())
    cards = {c['id']: c for c in json.loads((ROOT / 'scripts/markbank/authored/agricultural-science.json').read_text())}
    index = json.loads(subprocess.check_output([
        'node', '--input-type=module', '-e',
        'import {paperIndex} from "./scripts/markbank/paperIndex.mjs"; console.log(JSON.stringify(paperIndex["agricultural-science"]));',
    ], cwd=ROOT, text=True))
    topics = sorted({tid for task in review['tasks'] for tid in task['examTopicIds']})
    runtime = {'schemaVersion': 1, 'subjectId': 'agricultural-science', 'topicIds': topics,
               'questionMappings': [], 'markBankCards': []}
    maps = {}
    for task in review['tasks']:
        for cid in task['cardIds']:
            card = cards[cid]
            entry = next(e for e in index if e['year'] == card['year'] and e['level'] == card['level'] and e['lang'] == 'ev')
            assert len(entry['papers']) == 1
            fileid = entry['papers'][0]['doc']['f']
            key = (card['year'], fileid)
            if key not in maps:
                maps[key] = json.loads((ROOT / f'scripts/paper-trail/answers/{card["year"]}/{fileid}.json').read_text())
            paper_rect, scheme_rect = next(regions for prefix, regions in REGIONS.items() if cid.startswith(prefix))
            n = NUMBERS[cid]
            label = card['questionRef'].split(' Q', 1)[1]
            anchor = {
                'n': n, 'label': f'Question {label}', 'conf': 1.0, 'mode': 'crop',
                'parentN': card['questionRef'].split('Q', 1)[1].split('(', 1)[0],
                'pP': task['paperPage'], 'pY': [paper_rect[1], paper_rect[3]],
                'paperRegion': [{'p': task['paperPage'], 'r': paper_rect}],
                'endP': task['paperPage'], 'endY': paper_rect[3],
                'region': [{'p': task['schemePage'], 'r': scheme_rect}],
            }
            old = next((q for q in maps[key]['q'] if q['n'] == n), None)
            assert old is None or old == anchor, f'Review changed for {key} {n}; inspect before replacing'
            if old is None:
                maps[key]['q'].append(anchor)
            runtime['questionMappings'].append([
                'h' if card['level'] == 'higher' else 'o', 'e', card['year'], 'single', fileid, n,
                [topics.index(tid) for tid in task['examTopicIds']],
            ])
            runtime['markBankCards'].append({'cardId': cid, 'year': card['year'], 'fileid': fileid, 'n': n})
    result = {RUNTIME: runtime}
    for (year, fileid), answer_map in maps.items():
        for directory in ['scripts/paper-trail/answers', 'public/paper-answers']:
            result[ROOT / f'{directory}/{year}/{fileid}.json'] = answer_map
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    for path, data in outputs().items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n')
        elif args.check:
            assert path.exists() and json.loads(path.read_text()) == data, f'Stale: {path}'
    print('8 reviewed practice tasks mapped to Topic Atlas; prior whole-question identities retained')


if __name__ == '__main__':
    main()
