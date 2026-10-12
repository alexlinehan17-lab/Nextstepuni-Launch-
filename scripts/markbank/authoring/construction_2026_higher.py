"""Source-pinned validator for the 2026 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

Checks the reviewed authoring file against the original SEC paper and marking scheme: pinned
hashes and page text, lifted wording (narrowing only deletes printed words; a circled Q9 location
is named after ' — ' with the scheme's own heading), scheme-traceable rows, the published tariffs
and steps, every finite route (Q4 3 x 3 = 9, Q9 C(4,3) = 4), the separate alternative Q10,
pixel-exact figure crops, the selection ledger and exact topic/Atlas bindings.
"""
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path

import fitz
from PIL import Image, ImageChops

import construction_corrections

R = Path(__file__).resolve().parents[3]
REVIEW = R / 'scripts/markbank/authored/construction-studies-2026-higher-reviewed.json'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2026/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2026/LC029ALP000EV.pdf'
HASHES = {P: 'c470bc9009af7f39b2f4bd6c5e1182dd9ccf3190daa15ea8e3c4b75c3cebe0a4',
          S: 'e78fab89d53f74c61721efaee0e3371312bc52080ecfa45e5008e98c6905cd0d'}
PREFIX = 'cons-2026-hl-'
FP = 'construction-studies-2026-HL-'
CROSS = 'construction-studies-higher-'
BAND8 = [0, 4, 6, 8]
AREAS = ['stone-wall', 'cut-roof', 'sash-windows']
PRINCIPLES = ['conservation-original-materials', 'breathable-structure', 'respect-built-heritage']
LOCATIONS = ['wall-roof', 'window-head', 'window-cill', 'wall-floor']


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('external-wall', 12, r(12)), ('roof-structure', 16, r(16)), ('eaves', 16, r(16)), ('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q1-b': [('airtightness', 4, r(4))],
    'q2-a-entrance-access': [('guideline-1', 8, r(8)), ('guideline-2', 8, r(8))],
    'q2-a-bathroom': [('guideline-1', 8, r(8)), ('guideline-2', 8, r(8))],
    'q2-b': [('consideration-1', 6, r(6)), ('consideration-2', 6, r(6)), ('consideration-3', 6, r(6)), ('dimensions', 2, r(2))],
    'q2-c': [('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q3-a': [('layout', 18, r(18)), ('open-plan', 3, r(3)), ('daylight', 3, r(3)), ('bedroom-bathroom', 3, r(3))],
    'q3-b': [(f'reason-{i}', 7, r(7)) for i in (1, 2, 3)],
    'q3-c': [(f'benefit-{i}', 6, r(6)) for i in (1, 2)],
    **{f'q4-a-{a}': [('notes', 8, r(8)), ('sketches', 12, r(12))] for a in AREAS},
    **{f'q4-b-{p}': [('discussion', 10, r(10))] for p in PRINCIPLES},
    'q5-a': [('tabulation', 3, r(3)), ('surfaces', 6, r(6)), ('layers', 21, r(21)), ('total-resistance', 3, r(3)), ('u-value', 3, r(3))],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'pellets', 'cost']],
    'q5-c': [('notes', 3, r(3)), ('sketch', 6, r(6))],
    'q6-a': [(f'feature-{i}', 12, r(12)) for i in (1, 2, 3)],
    'q6-b': [(f'feature-{i}', 8, r(8)) for i in (1, 2)],
    'q6-c': [(f'advantage-{i}', 4, r(4)) for i in (1, 2)],
    'q7-a': [('construction', 40, r(40)), ('dimensions', 6, r(6)), ('presentation', 8, BAND8)],
    'q7-b': [('detail-1', 3, r(3)), ('detail-2', 3, r(3))],
    'q8-a': [(f'consideration-{i}', 8, r(8)) for i in (1, 2)],
    'q8-b': [('notes', 12, r(12)), ('sketch', 16, r(16)), ('dimensions', 4, r(4))],
    'q8-c': [('notes', 6, r(6)), ('sketches', 6, r(6))],
    **{f'q9-a-{loc}': [('note', 8, r(8)), ('sketches', 8, r(8))] for loc in LOCATIONS},
    'q9-b': [(f'benefit-{i}', 6, r(6)) for i in (1, 2)],
    'q10-a': [(f'selection-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q10-b': [(f'retrofit-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-c': [('notes', 6, r(6)), ('sketches', 6, r(6))],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
A_PAIRS = {f'q4-a-{x}-and-{y}': [f'q4-a-{x}', f'q4-a-{y}'] for x, y in itertools.combinations(AREAS, 2)}
B_PAIRS = {f'q4-b-{x}-and-{y}': [f'q4-b-{x}', f'q4-b-{y}'] for x, y in itertools.combinations(PRINCIPLES, 2)}
TRIPLES = {'q9-a-' + '-'.join(c): [f'q9-a-{x}' for x in c] for c in itertools.combinations(LOCATIONS, 3)}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'],
    'q2-a': ['q2-a-entrance-access', 'q2-a-bathroom'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'],
    'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    **A_PAIRS, **B_PAIRS,
    **{f"q4-complete-{a.removeprefix('q4-a-')}--{b.removeprefix('q4-b-')}": [a, b] for a in A_PAIRS for b in B_PAIRS},
    'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'],
    'q8-complete': ['q8-a', 'q8-b', 'q8-c'],
    **TRIPLES, **{'q9-complete-' + k.removeprefix('q9-a-'): [*v, 'q9-b'] for k, v in TRIPLES.items()},
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
PART_TOTALS = {'q1-a': 56, 'q1-b': 4, 'q2-a': 32, 'q2-a-entrance-access': 16, 'q2-a-bathroom': 16, 'q2-b': 20, 'q2-c': 8,
               'q3-a': 27, 'q3-b': 21, 'q3-c': 12, 'q5-a': 36, 'q5-b': 15, 'q5-c': 9, 'q6-a': 36, 'q6-b': 16, 'q6-c': 8,
               'q7-a': 54, 'q7-b': 6, 'q8-a': 16, 'q8-b': 32, 'q8-c': 12, 'q9-b': 12, 'q10-a': 18, 'q10-b': 30, 'q10-c': 12,
               'q10-alt-a': 30, 'q10-alt-b': 30, **{k: 40 for k in A_PAIRS}, **{k: 20 for k in B_PAIRS}, **{k: 48 for k in TRIPLES},
               **{f'q4-a-{a}': 20 for a in AREAS}, **{f'q4-b-{p}': 10 for p in PRINCIPLES}, **{f'q9-a-{loc}': 16 for loc in LOCATIONS},
               **{k: 60 for k in COMPOSITE if '-complete' in k}}
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-10', 'cons-3-3', 'cons-6-2'], ['question-1-drawing-questions', 'roofs', 'walls', 'heat-loss-insulation']),
    'q1-b': (['cons-6-6', 'cons-6-5'], ['condensation-air-tightness']),
    'q2-a-entrance-access': (['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'doors']),
    'q2-a-bathroom': (['cons-1-2'], ['planning-sustainability-environment']),
    'q2-b': (['cons-1-2'], ['planning-sustainability-environment']), 'q2-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q3-a': (['cons-1-2', 'cons-7-4', 'cons-6-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-b': (['cons-1-2', 'cons-6-4', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q4-a-stone-wall': (['cons-1-1', 'cons-3-3', 'cons-6-2'], ['conservation-restoration', 'walls', 'heat-loss-insulation']),
    'q4-a-cut-roof': (['cons-1-1', 'cons-3-9', 'cons-6-2'], ['conservation-restoration', 'roofs', 'heat-loss-insulation']),
    'q4-a-sash-windows': (['cons-1-1', 'cons-3-5', 'cons-3-6'], ['conservation-restoration', 'windows-light']),
    'q4-b-conservation-original-materials': (['cons-1-1'], ['conservation-restoration']),
    'q4-b-breathable-structure': (['cons-1-1', 'cons-6-6'], ['conservation-restoration', 'condensation-air-tightness']),
    'q4-b-respect-built-heritage': (['cons-1-1'], ['conservation-restoration']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-6', 'cons-3-3'], ['condensation-air-tightness', 'walls']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-7-4'], ['sustainability-the-environment', 'windows-light']),
    'q6-c': (['cons-1-2'], ['sustainability-the-environment']),
    'q7-a': (['cons-4-4', 'cons-10-1'], ['stairs']), 'q7-b': (['cons-4-4'], ['stairs']),
    'q8-a': (['cons-5-6'], ['drainage']), 'q8-b': (['cons-5-6'], ['drainage']), 'q8-c': (['cons-5-6'], ['drainage']),
    'q9-a-wall-roof': (['cons-6-2', 'cons-3-10', 'cons-3-3'], ['heat-loss-insulation', 'roofs', 'walls']),
    'q9-a-window-head': (['cons-6-2', 'cons-3-6', 'cons-3-4'], ['heat-loss-insulation', 'windows-light', 'walls']),
    'q9-a-window-cill': (['cons-6-2', 'cons-3-6'], ['heat-loss-insulation', 'windows-light']),
    'q9-a-wall-floor': (['cons-6-2', 'cons-4-2', 'cons-3-3'], ['heat-loss-insulation', 'floors', 'walls']),
    'q9-b': (['cons-6-2', 'cons-6-6'], ['heat-loss-insulation', 'condensation-air-tightness']),
    'q10-a': (['cons-6-2', 'cons-6-5'], ['passive-design']), 'q10-b': (['cons-6-2', 'cons-6-5'], ['passive-design']),
    'q10-c': (['cons-6-5'], ['condensation-air-tightness', 'passive-design']),
    'q10-alt-a': (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness', 'wood-rot-ventilation']),
    'q10-alt-b': (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness', 'wood-rot-ventilation']),
}
FIGURES = {
    'q1-original': (P, 2, [45, 50, 575, 362], False), 'q1-roof-section': (S, 4, [48, 52, 568, 803], True),
    'q1-airtightness': (S, 5, [48, 482, 540, 722], True), 'q2-original': (P, 2, [45, 362, 580, 765], False),
    'q2-entrance-access': (S, 6, [48, 52, 568, 803], True), 'q2-bathroom': (S, 7, [48, 52, 568, 803], True),
    'q2-kitchen-plan': (S, 9, [176, 124, 450, 667], True), 'q3-original': (P, 3, [45, 50, 580, 420], False),
    'q3-option-1': (S, 11, [48, 52, 568, 803], True), 'q3-option-2': (S, 12, [48, 52, 568, 803], True),
    'q4-original': (P, 3, [45, 420, 580, 765], False), 'q4-stone-wall': (S, 16, [48, 52, 568, 803], True),
    'q4-cut-roof': (S, 18, [48, 52, 568, 803], True), 'q4-sash-windows': (S, 19, [48, 52, 568, 792], True),
    'q5-original': (P, 4, [45, 50, 575, 720], False), 'q5-calculation': (S, 21, [48, 52, 568, 803], True),
    'q5-moisture': (S, 22, [48, 52, 568, 803], True), 'q6-original': (P, 5, [45, 40, 580, 526], False),
    'q6-low-impact': (S, 23, [48, 52, 568, 803], True), 'q6-nature': (S, 25, [48, 52, 568, 803], True),
    'q7-original': (P, 5, [45, 526, 580, 760], False), 'q7-stairs': (S, 28, [48, 52, 568, 803], True),
    'q8-original': (P, 6, [45, 50, 575, 395], False), 'q8-stack': (S, 30, [250, 320, 568, 778], True),
    'q8-traps': (S, 31, [284, 296, 586, 708], True), 'q9-original': (P, 6, [45, 395, 575, 770], False),
    'q9-wall-roof': (S, 33, [140, 115, 470, 300], True), 'q9-window-head': (S, 33, [140, 302, 470, 402], True),
    'q9-window-cill': (S, 33, [140, 405, 470, 512], True), 'q9-wall-floor': (S, 33, [140, 530, 470, 740], True),
    'q9-details': (S, 33, [140, 100, 470, 752], True), 'q10-original': (P, 7, [45, 50, 575, 400], False),
    'q10-areas': (S, 35, [48, 52, 568, 803], True), 'q10-retrofit': (S, 36, [48, 52, 568, 803], True),
    'q10-blower-door': (S, 38, [240, 480, 552, 690], True), 'q10-alt-original': (P, 7, [45, 440, 575, 705], False),
}
SOLUTION = {'q1-a': 'q1-roof-section', 'q1-b': 'q1-airtightness', 'q1-complete': 'q1-roof-section',
            'q2-a-entrance-access': 'q2-entrance-access', 'q2-a-bathroom': 'q2-bathroom', 'q2-a': 'q2-entrance-access',
            'q2-b': 'q2-kitchen-plan', 'q2-complete': 'q2-kitchen-plan', 'q3-a': 'q3-option-1', 'q3-b': 'q3-option-2',
            'q3-complete': 'q3-option-1', 'q4-a-stone-wall': 'q4-stone-wall', 'q4-a-cut-roof': 'q4-cut-roof',
            'q4-a-sash-windows': 'q4-sash-windows', 'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-moisture',
            'q5-complete': 'q5-calculation', 'q6-a': 'q6-low-impact', 'q6-b': 'q6-nature', 'q6-complete': 'q6-low-impact',
            'q7-a': 'q7-stairs', 'q7-b': 'q7-stairs', 'q7-complete': 'q7-stairs', 'q8-b': 'q8-stack', 'q8-c': 'q8-traps',
            'q8-complete': 'q8-stack', **{f'q9-a-{loc}': f'q9-{loc}' for loc in LOCATIONS}, **{k: 'q9-details' for k in TRIPLES},
            **{'q9-complete-' + k.removeprefix('q9-a-'): 'q9-details' for k in TRIPLES},
            'q10-a': 'q10-areas', 'q10-b': 'q10-retrofit', 'q10-c': 'q10-blower-door', 'q10-complete': 'q10-retrofit',
            **{k: 'q4-' + v[0].removeprefix('q4-a-') for k, v in A_PAIRS.items()},
            **{f"q4-complete-{a.removeprefix('q4-a-')}--{b.removeprefix('q4-b-')}": 'q4-' + A_PAIRS[a][0].removeprefix('q4-a-') for a in A_PAIRS for b in B_PAIRS}}
SCHEME_PAGES = {'1': [4, 5, 43], '2': [6, 7, 8, 9, 10, 44], '3': [11, 12, 13, 14, 15, 45], '4': [16, 17, 18, 19, 20, 46],
                '5': [21, 22, 47], '6': [23, 24, 25, 26, 27, 48], '7': [28, 49], '8': [29, 30, 31, 32, 50],
                '9': [33, 34, 51], '10': [35, 36, 37, 38, 39, 52], '10-alt': [40, 41, 53]}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.lower())


def is_subsequence(needle, haystack):
    it = iter(haystack)
    return all(word in it for word in needle)


def normalise(text):
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', text.lower())


def page_text(f, page):
    with fitz.open(R / f) as pdf:
        return ' '.join(pdf[page - 1].get_text().split())


def region(qkey):
    text = page_text(P, PAPER_PAGE[qkey])
    if qkey == '10':
        return text[text.index(' 10. '):text.index(' OR ')]
    if qkey == '10-alt':
        return text[text.index(' OR ') + 4:]
    start = text.index(f' {qkey}. ')
    nxt = [text.index(f' {n}. ') for n in map(str, range(int(qkey) + 1, 11)) if f' {n}. ' in text]
    return text[start:min(nxt) if nxt else len(text)]


def qkey_of(key):
    return '10-alt' if key.startswith('q10-alt') else key[1:].split('-')[0]


def validate(d, images=True, figure_dir=FIGURE_DIR, integrated=True):
    assert d['sourceHashes'] == HASHES
    for f, h in HASHES.items():
        assert hashlib.sha256((R / f).read_bytes()).hexdigest() == h, f
    assert (d['subjectId'], d['year'], d['level'], d['lang'], d['sitting'], d['paperKey'], d['fileid']) == (
        'construction-studies', 2026, 'higher', 'ev', 'main', 'single', 'LC029ALP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    assert set(cards) == set(LEAF) | set(COMPOSITE) and len(d['tasks']) == len(cards) == 69
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks']]
    assert len({c['questionRef'] for c in cards.values()}) == 69
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == set(cards) and len(d['bindings']) == 69
    scheme_pages = ' '.join(page_text(S, p) for p in range(1, 54))
    scheme = normalise(scheme_pages)
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 36

    for key, c in cards.items():
        qk = qkey_of(key)
        q = '10' if qk == '10-alt' else qk
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q and t['alternative'] == (qk == '10-alt')
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2026, 'higher', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f"2026 HL Q{qk}")
        assert c['questionFigureKey'] == f'{FP}q{qk}-original' and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[qk]] and t['requiredQuestionFigures'] == [c['questionFigureKey']]
        assert c.get('figureKey') == (FP + SOLUTION[key] if key in SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + SOLUTION[key]] if key in SOLUTION else [])
        if key in SOLUTION:
            assert figures[SOLUTION[key]]['solution'] is True
        assert figures[f'q{qk}-original']['solution'] is False
        # Lift, never write: printed wording only; a circled location is named by the scheme heading.
        words = tokens(region(qk))
        heads, labels = [], []
        for para in c['questionText'].split('\n\n'):
            head, _, tail = para.partition(' — ')
            heads.append(head)
            labels += tail.split('; ') if tail else []
        assert is_subsequence(tokens(' '.join(heads)), words), (key, 'questionText not lifted')
        assert all(normalise(x) in scheme for x in labels), (key, 'location label not printed in the scheme')
        assert not labels or q == '9', key
        assert is_subsequence(tokens(c['stem']), words), (key, 'stem not lifted')
        for row in c['rows']:
            assert row['kind'] == 'criterion' and row['contextNote'].strip()
            assert normalise(row['verbatim']) in scheme, (key, row['verbatim'])
            steps = row['permittedMarks']
            assert steps[0] == 0 and steps[-1] == row['marks'] and steps == sorted(set(steps)), (key, row['id'])
        assert 'questionBonus' not in c and c['totalMarks'] == sum(row['marks'] for row in c['rows'])
        assert c['totalMarks'] == PART_TOTALS[key], key
        if key in LEAF:
            assert [(row['id'], row['marks'], row['permittedMarks']) for row in c['rows']] == LEAF[key], key
            assert 'taskGroups' not in c
            nodes, topics = TOPICS[key]
            assert b['canonicalTopicIds'] == nodes and b['atlasTopicIds'] == [CROSS + x for x in topics], key
            covered = {n for x in b['atlasTopicIds'] for n in crosswalk[x]}
            assert set(nodes) <= covered, (key, 'canonical topics outside Atlas crosswalk')
        else:
            kids = COMPOSITE[key]
            assert [g['sourceCardId'] for g in c['taskGroups']] == [PREFIX + k for k in kids] and len(kids) >= 2
            rows = []
            for kid, g in zip(kids, c['taskGroups']):
                rs = copy.deepcopy(cards[kid]['rows'])
                for row in rs:
                    row['id'] = kid.removeprefix(f'q{qk}-') + '-' + row['id']
                assert g['rowIds'] == [row['id'] for row in rs] and g['marks'] == cards[kid]['totalMarks'] and len(rs) <= 5 and g['label'].strip()
                rows += rs
            assert c['rows'] == rows, key
            assert b['canonicalTopicIds'] == list(dict.fromkeys(n for k in kids for n in bindings[k]['canonicalTopicIds']))
            assert b['atlasTopicIds'] == list(dict.fromkeys(x for k in kids for x in bindings[k]['atlasTopicIds']))
        assert b['markBankTopicId'] == c['topicId'] == b['canonicalTopicIds'][0]
        assert set(b['canonicalTopicIds']) <= library_nodes and len(set(b['canonicalTopicIds'])) == len(b['canonicalTopicIds'])
        assert all(x.startswith(CROSS) and x in crosswalk for x in b['atlasTopicIds']) and b['atlasTopicIds']
        assert len(b['canonicalTopicIds']) == 1 or b['canonicalTopicReview'].strip()
        assert [(x['file'], x['page']) for x in t['sourceChecks']] == [(P, 1), (P, PAPER_PAGE[qk])] + [(S, p) for p in [2, 3, *SCHEME_PAGES[qk]]], key
        for x in t['sourceChecks']:
            assert hashlib.sha256(page_text(x['file'], x['page']).encode()).hexdigest() == x['textSha256'], (key, x)

    # Worked answers quoted in the calculation cards are the scheme's own figures.
    p21 = page_text(S, 21)
    for key, values in {'q5-a': ['0.035', '0.069', '0.092', '6.410', '0.050', '7.367', '0.136'],
                        'q5-b': ['254.592', '4,989,600', '1,270,312.243', '73.2168', '€40.27']}.items():
        notes = ' '.join(row['contextNote'] for row in cards[key]['rows'])
        assert all(x in notes and x in p21 for x in values), (key, [x for x in values if x not in notes or x not in p21])
    # The alternative Question 10 never combines with the EnerPHit question.
    for key, c in cards.items():
        for g in c.get('taskGroups', []):
            assert key.startswith('q10-alt') == g['sourceCardId'].startswith(PREFIX + 'q10-alt')
    # Finite routes, each exactly once: Q4 3 x 3 = 9 and Q9 C(4,3) = 4; every complete route is worth 60.
    ledgers = d['questionRouteLedgers']
    for qk in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '10-alt']:
        whole = sorted(k for k in cards if k.startswith(f'q{qk}-complete') and qkey_of(k) == qk)
        assert whole and {w['id'] for w in ledgers[qk]['wholeRoutes']} == {PREFIX + k for k in whole}
        assert all(cards[k]['totalMarks'] == 60 for k in whole)
    assert len(ledgers['4']['wholeRoutes']) == 9 and len(ledgers['9']['wholeRoutes']) == 4
    sel = d['selectionLedger']
    assert sel['finiteQuestionChoices']['4a']['routes'] == [list(c) for c in itertools.combinations(AREAS, 2)]
    assert sel['finiteQuestionChoices']['4b']['routes'] == [list(c) for c in itertools.combinations(PRINCIPLES, 2)]
    assert sel['finiteQuestionChoices']['9a']['routes'] == [list(c) for c in itertools.combinations(LOCATIONS, 3)]
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 9

    for key, f in figures.items():
        assert (f['source'], f['page'], f['rect'], f['solution']) == FIGURES[key] and f['visuallyInspected'] and f['renderScale'] == 2
        path = Path(figure_dir) / f"{f['key']}.png"
        assert hashlib.sha256(path.read_bytes()).hexdigest() == f['sha256'], key
        if images:
            with fitz.open(R / f['source']) as pdf:
                px = pdf[f['page'] - 1].get_pixmap(matrix=fitz.Matrix(2, 2), clip=fitz.Rect(f['rect']), alpha=False)
            a = Image.frombytes('RGB', (px.width, px.height), px.samples)
            saved = Image.open(path).convert('RGB')
            assert a.size == saved.size and ImageChops.difference(a, saved).getbbox() is None, key
    assert len({f['sha256'] for f in d['questionFigures']}) == 36

    if integrated:
        prior = json.loads((R / 'docs/markbank-audit/2026-09-28/drafts/construction-2026-higher/prior-authored-card-hashes.json').read_text())
        authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
        by_id = {c['id']: c for c in authored}
        assert prior['count'] == len(prior['cards']) == 783 and len(by_id) == len(authored)
        # Byte-identical, or replaced in place through a later review's recorded, hash-linked correction.
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
    assert d['questionsReviewed'] == [str(n) for n in range(1, 11)] and d['unreviewedQuestions'] == [] and d['alternativeQuestions'] == ['10']
    return dict(tasks=69, leafTasks=len(LEAF), wholeQuestionRoutes=sum(1 for k in cards if '-complete' in k),
                q4Routes=9, q9Routes=4, sourceFigures=36, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
