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
    'agsci-2022-ol-q13bi': ([0, .066, 1, .383], [0, .085, 1, .149]),
    'agsci-2025-ol-q8b': ([0, .529, 1, .808], [0, .370, 1, .419]),
}
# Explicit assignments survive reordering the authored deck or adding cards.
NUMBERS = {
    'agsci-2022-ol-q2bii': '1001',
    'agsci-2022-ol-q13bi': '1003',
    'agsci-2025-ol-q8b': '1001',
}


def new_answer_map(year, fileid, scheme_fileid):
    """A sitting with no Paper Trail answer map yet gets one in the sidecar contract: the
    single-component scheme band spans every scheme page, as in the corpus's other maps."""
    import fitz
    # A deferred sitting's edition ("LC024ALP000EV-deferred.pdf") reads the deferred scheme, filed under June's id.
    path = (ROOT / f'paper-trail-corpus/deferredmarkingschemes/{year}/{scheme_fileid.replace("-deferred.pdf", ".pdf")}'
            if scheme_fileid.endswith('-deferred.pdf') else ROOT / f'paper-trail-corpus/markingschemes/{year}/{scheme_fileid}')
    with fitz.open(path) as scheme:
        pages = len(scheme)
    return {'v': 1, 'paperFileid': fileid, 'schemeFileid': scheme_fileid, 'component': '000',
            'band': [1, pages + 1], 'copyright': '© State Examinations Commission', 'q': []}


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
            # A deferred sitting's card (agricultural_science_2023_hl_deferred.py) maps onto its own index entry.
            deferred = card['questionRef'].endswith(' — Deferred sitting')
            entry = next(e for e in index if e['year'] == card['year'] and e['level'] == card['level'] and e['lang'] == 'ev'
                         and (e.get('sitting') == 'deferred') == deferred)
            assert len(entry['papers']) == 1
            fileid = entry['papers'][0]['doc']['f']
            key = (card['year'], fileid)
            if key not in maps:
                path = ROOT / f'scripts/paper-trail/answers/{card["year"]}/{fileid}.json'
                maps[key] = json.loads(path.read_text()) if path.exists() else new_answer_map(card['year'], fileid, entry['papers'][0]['scheme']['f'])
            if 'paperRegions' in task:
                paper_regions, scheme_regions = task['paperRegions'], task['schemeRegions']
                n = task['atlasNumbers'][cid]
            else:
                paper_rect, scheme_rect = REGIONS[cid]
                paper_regions = [{'p': task['paperPage'], 'r': paper_rect}]
                scheme_regions = [{'p': task['schemePage'], 'r': scheme_rect}]
                n = NUMBERS[cid]
            label = card['questionRef'].split(' Q', 1)[1].removesuffix(' — Deferred sitting')
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
    # A deferred edition's new map has no Paper Trail whole-question anchors to preserve; the Atlas still lists its
    # printed questions 1-18, so each gets one, built from its own reviewed tasks: the paper from its first task's
    # head, the scheme over every page its tasks' answers use (June's whole-question form).
    for (year, fileid), answer_map in maps.items():
        if not fileid.endswith('-deferred.pdf') or any(not q['n'].isdigit() or int(q['n']) < 1000 for q in answer_map['q']):
            continue
        parents = {}
        for q in answer_map['q']:
            parents.setdefault(q['parentN'], []).append(q)
        whole = []
        for n, tasks in sorted(parents.items(), key=lambda kv: int(kv[0])):
            first = min(tasks, key=lambda q: (q['pP'], q['pY'][0]))
            spans = {}
            for q in tasks:
                for r in q['region']:
                    lo, hi = spans.get(r['p'], (1, 0))
                    spans[r['p']] = (min(lo, r['r'][1]), max(hi, r['r'][3]))
            whole.append({'conf': 1.0, 'mode': 'crop', 'n': n, 'pP': first['pP'], 'pY': [first['pY'][0], 1.0],
                          'region': [{'p': p, 'r': [0.0, lo, 1.0, hi]} for p, (lo, hi) in sorted(spans.items())]})
        answer_map['q'] = whole + answer_map['q']
    # Edition-specific source notes also accompany the preserved whole-question
    # readers. A translation does not create a duplicate English Mark Bank card.
    for paper in review['paperReviews']:
        # A deferred sitting's map holds only its reviewed tasks (no whole-question anchors): its source notes ride
        # on those tasks' own anchors (schemeNote, above).
        if not paper.get('sourceNotes') or paper.get('sitting') == 'deferred':
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


def flag_deferred_answers(path, year, fileid):
    """The Paper Trail index item of a reviewed deferred edition carries "answers": 1, as June's reviewed editions do;
    its map is hosted (public/paper-answers, HOSTED_ANSWER_OVERRIDES in components/PaperTrail/vaultResolve.ts).
    Returns the index text, flagged."""
    index = path.read_text()
    item = re.compile(r'(\{"year": %d, "level": "higher", "lang": "ev", "sitting": "deferred", "papers": \[\{"label": '
                      r'"Deferred · Exam Paper", "doc": \{"f": "%s", "b": \d+\}, "sitting": "deferred", "scheme": '
                      r'\{"f": "%s", "b": \d+\})(, "answers": 1)?(\}\]\})' % (year, re.escape(fileid), re.escape(fileid)))
    assert len(item.findall(index)) == 1, f'{year} {fileid}: deferred index item'
    return item.sub(r'\1, "answers": 1\3', index)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    # The reviewed deferred editions (agricultural_science_2023_hl_deferred.py), each flagged in the index.
    index_path = ROOT / 'paperTrailData.ts'
    flagged = flag_deferred_answers(index_path, 2023, 'LC024ALP000EV-deferred.pdf')
    if args.write and flagged != index_path.read_text():
        index_path.write_text(flagged)
    elif args.check:
        assert flagged == index_path.read_text(), 'Deferred index answers flag stale'
    for path, data in outputs().items():
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(data, ensure_ascii=False, separators=(',', ':'))+'\n')
        elif args.check:
            assert path.exists() and json.loads(path.read_text()) == data, f'Stale: {path}'
    print('Reviewed practice tasks mapped to Topic Atlas; prior whole-question identities retained')


if __name__ == '__main__':
    main()
