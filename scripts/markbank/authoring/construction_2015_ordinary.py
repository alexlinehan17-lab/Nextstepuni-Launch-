"""Source-pinned validator for the 2015 Ordinary Level Construction Studies theory paper (Q1-Q9).

Checks the reviewed authoring file against the original SEC paper and marking scheme:
pinned hashes and page text, lifted question wording (a narrowed task may only delete
printed words), scheme-traceable marking rows, published tariffs and mark steps, the
single shared drawing allowance on Q1 and Q5, every finite route (all C(9,5) = 126 for
Q8 as ONE any-five card over all nine printed terms: choice is not a route), pixel-exact figure crops, the selection ledger, and exact topic/Atlas bindings.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import fitz
from PIL import Image, ImageChops

import construction_corrections
import construction_figures

R = Path(__file__).resolve().parents[3]
REVIEW = R / 'scripts/markbank/authored/construction-studies-2015-ordinary-reviewed.json'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2015/LC029GLP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2015/LC029GLP000EV.pdf'
HASHES = {P: '6a5e6c2c39fcfc5d7d3d4eebae139ed927eaaaa16fb429d0eab333c3f0d7e99f',
          S: 'ca21a4dccfd47aea12de99758ce82058a9b33138a0ab9742dba1197b47364e07'}
PREFIX = 'cons-2015-ol-'
FP = 'construction-studies-2015-OL-'
CROSS = 'construction-studies-ordinary-'
BAND8 = [0, 4, 6, 8]
TERMS = ['box-dovetail-joint', 'triple-glazing', 'solar-panel', 'cordless-drill', 'skirting-board',
         'compression-fitting', 'natural-seasoning', 'concrete-lintel', 'radon-barrier']
TERM_NAMES = [t.replace('-', ' ') for t in TERMS]
TERM_HEADINGS = ['Box dovetail joint', 'Triple glazing', 'Solar panel', 'Cordless drill', 'Skirting board', 'Compression fitting',
                 'Natural seasoning', 'Concrete lintel', 'Radon barrier']

# Leaf tasks: id -> [(row id, marks, permitted steps)] exactly as the scheme mark tables print them.
LEAF = {
    'q1-a': [('details', 36, list(range(0, 37, 4))), ('dimensions', 4, [0, 4])],
    'q1-b': [('fixing', 2, [0, 2])],
    'q2-a-cavity-fill': [('notes', 12, [0, 4, 8, 12]), ('sketches', 8, BAND8)],
    'q2-a-external-insulation': [('notes', 12, [0, 4, 8, 12]), ('sketches', 8, BAND8)],
    'q2-b': [('advantages', 10, [0, 5, 10])],
    'q3-a': [('details', 32, list(range(0, 33, 4))), ('sketch', 8, BAND8)],
    'q3-b': [('methods', 10, [0, 5, 10])],
    'q4-a': [('site', 3, [0, 3]), ('entrance', 3, [0, 3]), ('driveway', 3, [0, 3]), ('septic', 3, [0, 3]), ('sketch', 8, BAND8)],
    'q4-b-entrance': [('reason', 4, [0, 4])],
    'q4-b-driveway': [('reason', 4, [0, 4])],
    'q4-b-septic-tank': [('reason', 4, [0, 4])],
    'q4-c': [('types', 4, [0, 2, 4]), ('sketch', 8, BAND8), ('advantages', 6, [0, 3, 6])],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 4, [0, 4])],
    'q5-b': [('insulation', 3, [0, 3])],
    'q6-a-hand': [('sign', 8, BAND8)], 'q6-a-ear': [('sign', 8, BAND8)], 'q6-a-eye': [('sign', 8, BAND8)],
    'q6-b-hand': [('activity', 4, [0, 4])], 'q6-b-ear': [('activity', 4, [0, 4])], 'q6-b-eye': [('activity', 4, [0, 4])],
    'q6-c': [('activities', 14, [0, 7, 14])],
    'q7-a': [('notes', 12, [0, 6, 12]), ('sketch', 8, BAND8)],
    'q7-b-advantages': [('advantages', 10, [0, 5, 10])],
    'q7-b-disadvantages': [('disadvantages', 10, [0, 5, 10])],
    'q7-c': [('reasons', 10, [0, 5, 10])],
    'q8': [('terms', 50, None)],
    'q9-a': [('joint', 4, [0, 4]), ('reason', 4, [0, 4]), ('sketch', 8, BAND8)],
    'q9-b': [('features', 8, [0, 4, 8]), ('sketch', 8, BAND8)],
    'q9-c': [('finish', 4, [0, 4]), ('steps', 10, [0, 5, 10]), ('sketch', 4, [0, 2, 3, 4])],
}
# Composite cards: id -> ordered children. Complete routes total 50; parts total their printed part marks.
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'],
    'q2-a': ['q2-a-cavity-fill', 'q2-a-external-insulation'], 'q2-complete': ['q2-a', 'q2-b'],
    'q3-complete': ['q3-a', 'q3-b'],
    'q4-b': ['q4-b-entrance', 'q4-b-driveway', 'q4-b-septic-tank'], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'],
    'q5-complete': ['q5-a', 'q5-b'],
    'q6-a': ['q6-a-hand', 'q6-a-ear', 'q6-a-eye'], 'q6-b': ['q6-b-hand', 'q6-b-ear', 'q6-b-eye'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-b': ['q7-b-advantages', 'q7-b-disadvantages'], 'q7-complete': ['q7-a', 'q7-b', 'q7-c'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
}
TOTALS = {'q1-a': 40, 'q1-b': 2, 'q2-a': 40, 'q2-a-cavity-fill': 20, 'q2-a-external-insulation': 20, 'q2-b': 10,
          'q3-a': 40, 'q3-b': 10, 'q4-a': 20, 'q4-b': 12, 'q4-c': 18, 'q5-a': 39, 'q5-b': 3, 'q6-a': 24, 'q6-b': 12,
          'q6-c': 14, 'q7-a': 20, 'q7-b': 20, 'q7-c': 10, 'q9-a': 16, 'q9-b': 16, 'q9-c': 18,
          **{k: 50 for k in COMPOSITE if '-complete' in k}}
BONUS = {'q1-complete', 'q5-complete'}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 8, 20], '5': [9, 21], '6': [10, 11, 22],
                '7': [11, 12, 23], '9': [15, 16, 25]}
PAPER_PAGE = {q: (2 if q in '1234' else 3) for q in '123456789'}
FIGURES = {
    'q1-original': (P, 2, [38, 34, 580, 221], False), 'q1-roof-section': (S, 4, [54, 54, 568, 752], True),
    'q2-original': (P, 2, [38, 236, 580, 398], False), 'q2-cavity-fill': (S, 5, [408, 56, 544, 343], True),
    'q2-external-insulation': (S, 5, [382, 343, 556, 495], True), 'q2-insulated-wall': (S, 5, [315, 540, 565, 699], True),
    'q2-scheme': (S, 5, [50, 52, 566, 765], True),
    'q3-original': (P, 2, [38, 398, 580, 588], False), 'q3-system': (S, 6, [333, 97, 547, 350], True),
    'q3-scheme': (S, 6, [50, 52, 566, 765], True),
    'q4-original': (P, 2, [38, 588, 580, 790], False), 'q4-site-plans': (S, 7, [43, 124, 549, 359], True),
    'q5-original': (P, 3, [38, 34, 580, 220], False), 'q5-section': (S, 9, [50, 52, 566, 716], True),
    'q6-original': (P, 3, [38, 220, 580, 381], False), 'q6-hand-sign': (S, 10, [52, 76, 169, 212], True),
    'q6-ear-sign': (S, 10, [222, 76, 340, 212], True), 'q6-eye-sign': (S, 10, [408, 76, 523, 212], True),
    'q6-signs': (S, 10, [52, 76, 523, 212], True),
    'q7-original': (P, 3, [38, 381, 580, 528], False), 'q7-water-butt': (S, 11, [397, 457, 548, 654], True),
    'q8-original': (P, 3, [38, 528, 580, 622], False),
    'q9-original': (P, 3, [38, 622, 580, 790], False), 'q9-joint': (S, 15, [50, 388, 560, 779], True),
    'q9-table-features': (S, 16, [375, 89, 538, 214], True), 'q9-finish': (S, 16, [408, 400, 546, 745], True),
}
FIGURES['q8-terms'] = construction_figures.composite([(S, 12, [51, 351, 544, 705]), (S, 13, [51, 44, 558, 701]), (S, 14, [51, 49, 572, 748]), (S, 15, [51, 49, 543, 350])])
SOLUTION_FIGURE = {
    'q1-a': 'q1-roof-section', 'q1-b': 'q1-roof-section', 'q1-complete': 'q1-roof-section',
    'q2-a-cavity-fill': 'q2-cavity-fill', 'q2-a-external-insulation': 'q2-external-insulation', 'q2-a': 'q2-scheme',
    'q2-b': 'q2-insulated-wall', 'q2-complete': 'q2-scheme',
    'q3-a': 'q3-system', 'q3-b': 'q3-scheme', 'q3-complete': 'q3-scheme',
    **{k: 'q4-site-plans' for k in ['q4-a', 'q4-b-entrance', 'q4-b-driveway', 'q4-b-septic-tank', 'q4-b', 'q4-c', 'q4-complete']},
    'q5-a': 'q5-section', 'q5-b': 'q5-section', 'q5-complete': 'q5-section',
    'q6-a-hand': 'q6-hand-sign', 'q6-a-ear': 'q6-ear-sign', 'q6-a-eye': 'q6-eye-sign', 'q6-a': 'q6-signs', 'q6-complete': 'q6-signs',
    'q7-a': 'q7-water-butt', 'q7-complete': 'q7-water-butt',
    'q9-a': 'q9-joint', 'q9-b': 'q9-table-features', 'q9-c': 'q9-finish', 'q9-complete': 'q9-joint',
    'q8': 'q8-terms',
}
# Pinned leaf topic decisions (composites inherit the ordered union).
TOPICS = {
    'q1-a': (['cons-3-8', 'cons-3-9', 'cons-3-3', 'cons-6-2', 'cons-1-5'], ['roofs', 'foundations-floors-walls', 'heat-loss-insulation', 'question-one-drawing-questions']),
    'q1-b': (['cons-3-8', 'cons-3-3'], ['roofs', 'foundations-floors-walls']),
    'q2-a-cavity-fill': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-a-external-insulation': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q3-a': (['cons-5-2', 'cons-5-1'], ['services-water-gas-electrical', 'hot-water-space-heating']),
    'q3-b': (['cons-5-6', 'cons-5-2'], ['drainage', 'services-water-gas-electrical']),
    'q4-a': (['cons-1-3', 'cons-5-5'], ['planning-sustainability-environment', 'drainage']),
    'q4-b-entrance': (['cons-1-3'], ['planning-sustainability-environment']),
    'q4-b-driveway': (['cons-1-3'], ['planning-sustainability-environment']),
    'q4-b-septic-tank': (['cons-5-5', 'cons-1-3'], ['drainage', 'planning-sustainability-environment']),
    'q4-c': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q5-a': (['cons-2-4', 'cons-3-3', 'cons-4-2', 'cons-3-4', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation']),
    'q5-b': (['cons-6-2', 'cons-3-3', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q6-a-hand': (['cons-1-8'], ['site-safety']), 'q6-a-ear': (['cons-1-8', 'cons-8-4'], ['site-safety', 'sound']),
    'q6-a-eye': (['cons-1-8'], ['site-safety']), 'q6-b-hand': (['cons-1-8'], ['site-safety']),
    'q6-b-ear': (['cons-1-8', 'cons-8-4'], ['site-safety', 'sound']), 'q6-b-eye': (['cons-1-8'], ['site-safety']),
    'q6-c': (['cons-9-4'], ['site-safety']),
    'q7-a': (['cons-5-4'], ['drainage']), 'q7-b-advantages': (['cons-5-4'], ['drainage']),
    'q7-b-disadvantages': (['cons-5-4'], ['drainage']), 'q7-c': (['cons-5-4'], ['drainage']),
    'q8': (['cons-10-2', 'cons-10-4', 'cons-3-6', 'cons-6-2', 'cons-6-6', 'cons-6-4', 'cons-5-3', 'cons-9-2', 'cons-9-4', 'cons-4-5', 'cons-5-2', 'cons-5-1', 'cons-10-3', 'cons-3-4', 'cons-4-2'],
           ['wood-rot-ventilation', 'windows-doors', 'heat-loss-insulation', 'air-tightness-condensation', 'planning-sustainability-environment', 'hot-water-space-heating', 'site-safety', 'services-water-gas-electrical', 'foundations-floors-walls']),
    'q9-a': (['cons-10-4', 'cons-10-6'], ['wood-rot-ventilation']),
    'q9-b': (['cons-10-3'], ['wood-rot-ventilation']),
    'q9-c': (['cons-10-7'], ['wood-rot-ventilation']),
}
GAPS = {'q8': {'cons-10-2', 'cons-10-4', 'cons-9-2'}, 'q9-a': {'cons-10-4', 'cons-10-6'}}


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def is_subsequence(needle, haystack):
    it = iter(haystack)
    return all(word in it for word in needle)


def normalise(text):
    # Mirrors scripts/markbank/schemeText.mjs normalise() for Latin text.
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', text.lower().replace('‐', '-'))


def page_text(f, page):
    with fitz.open(R / f) as pdf:
        return ' '.join(pdf[page - 1].get_text().split())


def question_region(q):
    text = page_text(P, PAPER_PAGE[q])
    start = text.index(f' {q}. ')
    following = [text.index(f' {n}. ') for n in '123456789' if int(n) > int(q) and f' {n}. ' in text]
    return text[start:min(following) if following else len(text)]


def children_of(key):
    return COMPOSITE.get(key, [])


def leaves_of(key):
    return [leaf for child in children_of(key) for leaf in leaves_of(child)] if key in COMPOSITE else [key]


def validate(d, images=True, figure_dir=FIGURE_DIR, integrated=True):
    assert d['sourceHashes'] == HASHES
    for f, h in HASHES.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid']) == (
        'construction-studies', 2015, 'ordinary', 'ev', 'main', 'single', 'LC029GLP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    expected = set(LEAF) | set(COMPOSITE)
    assert len(d['tasks']) == len(cards) == len(expected) == 42 and set(cards) == expected
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks']]
    assert len({c['questionRef'] for c in cards.values()}) == 42, 'questionRef must be unique per card'
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert len(d['bindings']) == 42 and set(bindings) == expected

    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 26)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    registry = set(re.findall(r"id: '(cons-\d+-\d+)'", (R / 'curriculumRegistry.ts').read_text()))
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 27

    for key, c in cards.items():
        q = key[1]
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2015, 'ordinary', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2015 OL Q{q}')
        assert c['questionFigureKey'] == f'{FP}q{q}-original' and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[q]] and c['sourceMaterial']['kind'] == 'source-illustration'
        assert t['requiredQuestionFigures'] == [c['questionFigureKey']]
        solution = SOLUTION_FIGURE.get(key)
        assert c.get('figureKey') == (FP + solution if solution else None), key
        assert t['requiredSolutionFigures'] == ([FP + solution] if solution else [])
        if solution:
            assert figures[solution]['solution'] is True
        assert figures[f'q{q}-original']['solution'] is False
        # Lift, never write: wording comes from the printed question, narrowed only by deletion.
        region = tokens(question_region(q))
        assert is_subsequence(tokens(c['questionText']), region), (key, 'questionText not lifted')
        assert is_subsequence(tokens(c['stem']), region), (key, 'stem not lifted')
        # Every marking row is printed in the scheme and has published steps.
        rows = c['rows'] + ([c['questionBonus']] if c.get('questionBonus') else [])
        for r in rows:
            assert r['contextNote'].strip()
            if r['kind'] == 'anyN':  # a closed choice: every printed option, in the scheme's own headings
                assert 'permittedMarks' not in r and r['marks'] == r['group']['claimMax'] * r['group']['perOption'], (key, r['id'])
                assert all(normalise(o) in scheme for o in r['group']['options']), (key, 'option not printed in the scheme')
                continue
            assert r['kind'] == 'criterion'
            assert normalise(r['verbatim']) in scheme, (key, r['verbatim'])
            steps = r['permittedMarks']
            assert steps[0] == 0 and steps[-1] == r['marks'] and steps == sorted(set(steps)), (key, r['id'])
        bonus = c['questionBonus']['marks'] if c.get('questionBonus') else 0
        assert c['totalMarks'] == sum(r['marks'] for r in c['rows']) + bonus
        if key in LEAF:
            assert [(r['id'], r['marks'], r.get('permittedMarks')) for r in c['rows']] == LEAF[key], key
            assert 'taskGroups' not in c and 'questionBonus' not in c
            nodes, topics = TOPICS[key]
            assert b['canonicalTopicIds'] == nodes and b['atlasTopicIds'] == [CROSS + x for x in topics], key
            covered = {n for x in b['atlasTopicIds'] for n in crosswalk[x]}
            assert set(nodes) - covered == GAPS.get(key, set()), (key, 'canonical topics outside Atlas crosswalk')
        else:
            kids = children_of(key)
            assert [g['sourceCardId'] for g in c['taskGroups']] == [PREFIX + k for k in kids]
            assert len(c['taskGroups']) >= 2
            rows_expected = []
            for kid, g in zip(kids, c['taskGroups']):
                child = cards[kid]
                rs = copy.deepcopy(child['rows'])
                for r in rs:
                    r['id'] = kid.removeprefix(f'q{q}-') + '-' + r['id']
                assert g['rowIds'] == [r['id'] for r in rs] and g['marks'] == child['totalMarks'] and len(rs) <= 5
                assert g['label'].strip()
                rows_expected += rs
            assert c['rows'] == rows_expected, key
            union_nodes = list(dict.fromkeys(n for k in kids for n in bindings[k]['canonicalTopicIds']))
            union_topics = list(dict.fromkeys(x for k in kids for x in bindings[k]['atlasTopicIds']))
            assert b['canonicalTopicIds'] == union_nodes and b['atlasTopicIds'] == union_topics, key
        assert (key in BONUS) == ('questionBonus' in c), key
        assert c['totalMarks'] == TOTALS.get(key, c['totalMarks']), key
        assert b['markBankTopicId'] == c['topicId'] == b['canonicalTopicIds'][0]
        assert set(b['canonicalTopicIds']) <= registry and len(set(b['canonicalTopicIds'])) == len(b['canonicalTopicIds'])
        assert set(b['canonicalTopicIds']) <= library_nodes, (key, 'canonical topic outside the reviewed library crosswalk')
        assert all(x.startswith(CROSS) and x in crosswalk for x in b['atlasTopicIds']) and b['atlasTopicIds']
        assert len(b['canonicalTopicIds']) == 1 or b['canonicalTopicReview'].strip()
        # Original pages behind every task, pinned by text hash.
        pages = [12, 13, 14, 15, 24] if q == '8' else SCHEME_PAGES[q]
        assert [(x['file'], x['page']) for x in t['sourceChecks']] == [(P, 1), (P, PAPER_PAGE[q])] + [(S, p) for p in [2, *pages]], key
        for x in t['sourceChecks']:
            assert hashlib.sha256(page_text(x['file'], x['page']).encode()).hexdigest() == x['textSha256'], (key, x)

    # The shared drawing allowance is applied exactly once per drawing question, never inside a part.
    for key in BONUS:
        bonus = cards[key]['questionBonus']
        assert (bonus['id'], bonus['verbatim'], bonus['marks'], bonus['permittedMarks']) == (
            'drawing-quality', 'Draughting, accuracy and scale', 8, BAND8)
    for key, c in cards.items():
        assert all(r['verbatim'] != 'Draughting, accuracy and scale' for r in c['rows']), key
    # Q1 preserves the validated checkpoint-589 draft rows and allowance.
    q1 = json.loads((R / 'docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-draft/q1-draft.json').read_text())
    q1 = {x['card']['id'].removeprefix(PREFIX): x['card'] for x in q1['tasks']}
    for key in ['q1-a', 'q1-b', 'q1-complete']:
        assert cards[key]['rows'] == q1[key]['rows'] and cards[key]['totalMarks'] == q1[key]['totalMarks']
    assert cards['q1-complete']['questionBonus'] == q1['q1-complete']['questionBonus']

    # Q8: choice is not a route. ONE card prints all nine terms and carries one any-five group over them.
    ledger = d['questionRouteLedgers']['8']
    assert ledger['choose'] == 5 and ledger['options'] == TERM_NAMES and [w['id'] for w in ledger['wholeRoutes']] == [PREFIX + 'q8']
    q8 = cards['q8']
    assert [k for k in cards if k.startswith('q8')] == ['q8'] and 'taskGroups' not in q8 and q8['totalMarks'] == 50
    assert q8['questionText'].endswith('any five of the following: ' + '; '.join(TERM_NAMES) + '.')
    assert q8['rows'][0]['kind'] == 'anyN' and q8['rows'][0]['group'] == dict(claimMax=5, perOption=10, options=TERM_HEADINGS)
    sel = d['selectionLedger']
    assert sel['finiteQuestionChoices']['8']['cardId'] == PREFIX + 'q8' and 'routes' not in sel['finiteQuestionChoices']['8']
    assert sel['unclassified'] == 0 and all(r['classification'] for r in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(r['page'], r['start'], r['match']) for r in sel['rows']] and len(observed) == 3

    # Whole-paper reconciliation: every question has complete routes at 50 marks; 200 = Q1 + three others.
    for q in '123456789':
        whole = ['q8'] if q == '8' else [k for k in cards if k.startswith(f'q{q}-complete')]
        assert whole and all(cards[k]['totalMarks'] == 50 for k in whole)
        assert {r['id'] for r in d['questionRouteLedgers'][q]['wholeRoutes']} == {PREFIX + k for k in whole}

    for key, f in figures.items():  # pixel-exact: a single crop, or a composite of every choice item's scheme panel
        construction_figures.check(f, FIGURES[key], figure_dir, images)
    assert len({f['sha256'] for f in d['questionFigures']}) == 27

    if integrated:
        # Runtime input carries exactly these cards after the 607 prior cards, which are byte-for-byte unchanged.
        prior = json.loads((R / 'docs/markbank-audit/2026-09-28/drafts/construction-2015-ordinary-q1-q9/prior-authored-card-hashes.json').read_text())
        authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
        by_id = {c['id']: c for c in authored}
        assert prior['count'] == len(prior['cards']) == 607 and len(by_id) == len(authored)
        # Byte-identical, or replaced in place through a later review's recorded, hash-linked correction.
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
    gaps = {g['cardId'].removeprefix(PREFIX): set(g['canonicalTopicIds']) for g in d['taxonomyGaps']}
    assert gaps == GAPS
    assert d['questionsReviewed'] == list('123456789') and d['unreviewedQuestions'] == []
    return dict(tasks=42, leafTasks=len(LEAF), wholeQuestions=sum(1 for k in cards if '-complete' in k or k == 'q8'),
                q8AnyFiveOfNine=True, sourceFigures=27, sharedDrawingAllowances=2, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
