#!/usr/bin/env python3
"""Publish reviewed practice tasks in Topic Atlas, preserving whole-question IDs.

Each reviewed crop was inspected against the PDF pages. The rest of the corpus
is intentionally not labelled complete. IDs 1001+ are additive, stable practice
identities; the existing 1–18 question cards and their saved progress survive.
"""
import argparse
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNTIME = ROOT / 'data/examTopics/agricultural-science-question-runtime.json'

# Prefix, exact paper range, exact scheme range. Include the source artwork in
# each question crop and stop before the next independently marked part.
REGIONS = {
    'agsci-2022-ol-q2bii': ([0, .089, 1, .596], [0, .618, 1, .732]),
    'agsci-2023-hl-q18ai': ([0, .066, 1, .386], [0, .317, 1, .559]),
    'agsci-2022-ol-q13bi': ([0, .066, 1, .383], [0, .085, 1, .149]),
    'agsci-2025-ol-q8b': ([0, .529, 1, .808], [0, .370, 1, .419]),
}
# Explicit assignments survive reordering the authored deck or adding cards.
NUMBERS = {
    'agsci-2022-ol-q2bii': '1001',
    'agsci-2022-ol-q13bi': '1003',
    'agsci-2023-hl-q18ai': '1001',
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
               'questionMappings': [], 'markBankCards': [], 'translatedMarkBankCards': []}
    maps = {}
    for task in review['tasks']:
        for cid in task['cardIds']:
            card = cards[cid]
            entry = next(e for e in index if e['year'] == card['year'] and e['level'] == card['level'] and e['lang'] == 'ev')
            assert len(entry['papers']) == 1
            fileid = entry['papers'][0]['doc']['f']
            key = (card['year'], fileid)
            if key not in maps:
                path = ROOT / f'scripts/paper-trail/answers/{card["year"]}/{fileid}.json'
                maps[key] = json.loads(path.read_text()) if path.exists() else {
                    'v': 1, 'paperFileid': fileid, 'schemeFileid': entry['papers'][0]['scheme']['f'],
                    'component': '', 'copyright': '© State Examinations Commission', 'q': [],
                }
            if 'paperRegions' in task:
                paper_regions, scheme_regions = task['paperRegions'], task['schemeRegions']
                n = task['atlasNumbers'][cid]
            else:
                paper_rect, scheme_rect = REGIONS[cid]
                paper_regions = [{'p': task['paperPage'], 'r': paper_rect}]
                scheme_regions = [{'p': task['schemePage'], 'r': scheme_rect}]
                n = NUMBERS[cid]
            label = card['questionRef'].split(' Q', 1)[1]
            anchor = {
                'n': n, 'label': f'Question {label}', 'conf': 1.0, 'mode': 'crop',
                'parentN': re.search(r'Q(\d+)', card['questionRef']).group(1),
                'pP': paper_regions[0]['p'], 'pY': [paper_regions[0]['r'][1], paper_regions[-1]['r'][3]],
                'paperRegion': paper_regions,
                'endP': paper_regions[-1]['p'], 'endY': paper_regions[-1]['r'][3],
                'region': scheme_regions,
            }
            if task.get('schemeNote'):
                anchor['schemeNote'] = task['schemeNote']
            old = next((q for q in maps[key]['q'] if q['n'] == n), None)
            assert old is None or old == anchor, f'Review changed for {key} {n}; inspect before replacing'
            if old is None:
                maps[key]['q'].append(anchor)
            runtime['questionMappings'].append([
                'h' if card['level'] == 'higher' else 'o', 'e', card['year'], 'single', fileid, n,
                [topics.index(tid) for tid in task['examTopicIds']],
            ])
            runtime['markBankCards'].append({'cardId': cid, 'year': card['year'], 'fileid': fileid, 'n': n})
            for source in task.get('translatedSources', []):
                translated_fileid = source['paperFileid']
                translated_key = (card['year'], translated_fileid)
                translated_entry = next(e for e in index if e['year']==card['year'] and e['level']==card['level'] and e['lang']==source['lang'])
                assert translated_entry['papers'][0]['doc']['f'] == translated_fileid
                if translated_key not in maps:
                    path = ROOT / f'scripts/paper-trail/answers/{card["year"]}/{translated_fileid}.json'
                    maps[translated_key] = json.loads(path.read_text())
                translated_paper, translated_scheme = source['paperRegions'], source['schemeRegions']
                translated_anchor = {
                    'n': n, 'label': source['label'], 'conf': 1.0, 'mode': 'crop',
                    'parentN': anchor['parentN'],
                    'pP': translated_paper[0]['p'],
                    'pY': [translated_paper[0]['r'][1], translated_paper[-1]['r'][3]],
                    'paperRegion': translated_paper,
                    'endP': translated_paper[-1]['p'], 'endY': translated_paper[-1]['r'][3],
                    'region': translated_scheme,
                }
                if source.get('schemeNote'):
                    translated_anchor['schemeNote'] = source['schemeNote']
                old = next((q for q in maps[translated_key]['q'] if q['n']==n), None)
                assert old is None or old==translated_anchor, f'Review changed for {translated_key} {n}; inspect before replacing'
                if old is None:
                    maps[translated_key]['q'].append(translated_anchor)
                runtime['questionMappings'].append([
                    'h' if card['level']=='higher' else 'o', 'i', card['year'], 'single', translated_fileid, n,
                    [topics.index(tid) for tid in task['examTopicIds']],
                ])
                runtime['translatedMarkBankCards'].append({
                    'cardId':cid,'year':card['year'],'lang':source['lang'],'fileid':translated_fileid,
                    'n':n,'marksPerRoute':source['marksPerRoute'],
                })
    # Edition-specific source notes also accompany the preserved whole-question
    # readers. A translation does not create a duplicate English Mark Bank card.
    for paper in review['paperReviews']:
        if not paper.get('sourceNotes'):
            continue
        key = (paper['year'], paper['paperFileid'])
        if key not in maps:
            path = ROOT / f'scripts/paper-trail/answers/{key[0]}/{key[1]}.json'
            maps[key] = json.loads(path.read_text())
        notes = {}
        for note in paper['sourceNotes']:
            notes.setdefault(note['questionN'], []).append(note['note'])
        for n, values in notes.items():
            anchor = next(q for q in maps[key]['q'] if q['n'] == n)
            anchor['schemeNote'] = '\n\n'.join(values)
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
    print('Reviewed practice tasks mapped to Topic Atlas; prior whole-question identities retained')


if __name__ == '__main__':
    main()
