"""Source-pinned validator for the 2023 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

Checks the reviewed authoring file against the original SEC paper and marking scheme: pinned hashes
and page text, lifted wording (narrowing only deletes printed words; a Q2 item, named by reference to
the printed list, carries the scheme's own heading after ' — '), scheme-traceable rows, the published
tariffs and steps, the printed choices Q4(b) and Q10(a) as ONE card each with an anyN group over all
three items (choice is not a route), the separate alternative Q10, pixel-exact figure crops (single
rects and multi-page composites, every choice item's drawings carried), the selection ledger and exact
topic/Atlas bindings. The 29 pre-audit 2023 Higher cards keep their IDs and concept IDs and are
corrected in place, each hash-linked to the card it replaced; every other prior card stays
byte-identical.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import fitz

import construction_corrections
import construction_figures

R = Path(__file__).resolve().parents[3]
REVIEW = R / 'scripts/markbank/authored/construction-studies-2023-higher-reviewed.json'
DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts/construction-2023-higher'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2023/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2023/LC029ALP000EV.pdf'
HASHES = {P: '194c14229122c30285677e2133d08f4855a6798893add82f3bc50e94b5ca38f5',
          S: 'fd7a1e74988a4af90cbb10c455f2cbe2c9ec8c724f9d690093e1b822db4fc0b4'}
PREFIX = 'cons-2023-hl-'
FP = 'construction-studies-2023-HL-'
CROSS = 'construction-studies-higher-'
LIGATURES = {'Ɵ': 'ti', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
LEGACY = {'q1-a', 'q1-b', 'q2-a-communication', 'q2-a-supervision', 'q2-a-training', 'q2-b-site-access', 'q2-b-using-a-ladder', 'q2-c',
          'q3-a', 'q3-b', 'q3-c-advantages', 'q3-c-disadvantages', 'q4-a', 'q4-b', 'q4-c', 'q5-b', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b',
          'q8-a', 'q8-c', 'q9-a', 'q9-b', 'q9-c-advantages', 'q9-c-disadvantages', 'q10-a', 'q10-c'}
CHOICES = {'q4-b': ('items', 2, 7, ['Choice of material', 'Craft skills', 'Respect for local character']),
           'q10-a': ('items', 2, 10, ['Foundation design', 'Solar shading', 'Thermally efficient building envelope'])}


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('wall', 20, r(20)), ('roof', 12, r(12)), ('eaves', 16, r(16)), ('presentation', 8, r(8))],
    'q1-b': [('ventilation', 4, r(4))],
    **{f'q2-a-{k}': [('importance', 6, r(6))] for k in ['communication', 'supervision', 'training']},
    **{f'q2-b-{k}': [('guideline-1', 8, r(8)), ('guideline-2', 8, r(8))] for k in ['site-access', 'using-a-ladder']},
    'q2-c': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q3-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-b': [('layout', 14, r(14))] + [(f'consideration-{i}', 2, r(2)) for i in (1, 2, 3)] + [('justification', 2, r(2))],
    'q3-c-advantages': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q3-c-disadvantages': [('disadvantage-1', 5, r(5)), ('disadvantage-2', 5, r(5))],
    'q4-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q4-b': [('items', 14, None)],
    'q4-c': [('reason-1', 8, r(8)), ('reason-2', 8, r(8))],
    'q5-a': [('resistances', 24, list(range(0, 25, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [('notes', 5, r(5)), ('sketch', 10, r(10))],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(k, 6, r(6)) for k in ['photovoltaic', 'heat-pump', 'evacuated-tubes']],
    'q6-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q7-a': [('door-head', 16, r(16)), ('external-door', 16, r(16)), ('threshold', 16, r(16)), ('presentation', 8, r(8))],
    'q7-b': [('threshold-moisture', 4, r(4))],
    'q8-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q8-b': [('notes', 6, r(6)), ('sketch', 10, r(10)), ('description', 6, r(6)), ('dimensions', 4, r(4))],
    'q8-c': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q9-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2)],
    'q9-b': [('formula', 4, r(4)), ('entry', 4, r(4)), ('floor-area', 4, r(4)), ('lux', 4, r(4)), ('window-area', 12, r(12))],
    'q9-c-advantages': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q9-c-disadvantages': [('disadvantage-1', 4, r(4)), ('disadvantage-2', 4, r(4))],
    'q10-a': [('items', 20, None)],
    'q10-b': [('diagram', 5, r(5)), ('unit', 5, r(5)), ('ducting', 5, r(5)), ('airflow', 5, r(5)), ('description', 6, r(6))],
    'q10-c': [(f'consideration-{i}', 7, r(7)) for i in (1, 2)],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-a': ['q2-a-communication', 'q2-a-supervision', 'q2-a-training'],
    'q2-b': ['q2-b-site-access', 'q2-b-using-a-ladder'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'],
    'q3-c': ['q3-c-advantages', 'q3-c-disadvantages'], 'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-c': ['q9-c-advantages', 'q9-c-disadvantages'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
PART_TOTALS = {'q1-a': 56, 'q1-b': 4, 'q2-a-communication': 6, 'q2-a-supervision': 6, 'q2-a-training': 6, 'q2-a': 18,
               'q2-b-site-access': 16, 'q2-b-using-a-ladder': 16, 'q2-b': 32, 'q2-c': 10, 'q3-a': 18, 'q3-b': 22, 'q3-c-advantages': 10,
               'q3-c-disadvantages': 10, 'q3-c': 20, 'q4-a': 30, 'q4-b': 14, 'q4-c': 16, 'q5-a': 30, 'q5-b': 15, 'q5-c': 15, 'q6-a': 30,
               'q6-b': 18, 'q6-c': 12, 'q7-a': 56, 'q7-b': 4, 'q8-a': 24, 'q8-b': 26, 'q8-c': 10, 'q9-a': 16, 'q9-b': 28,
               'q9-c-advantages': 8, 'q9-c-disadvantages': 8, 'q9-c': 16, 'q10-a': 20, 'q10-b': 26, 'q10-c': 14, 'q10-alt-a': 30,
               'q10-alt-b': 30, **{k: 60 for k in COMPOSITE if '-complete' in k}}
SAFETY = (['cons-1-8'], ['site-safety'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q1-b': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q2-a-communication': SAFETY, 'q2-a-supervision': SAFETY, 'q2-a-training': SAFETY,
    'q2-b-site-access': SAFETY, 'q2-b-using-a-ladder': SAFETY, 'q2-c': SAFETY,
    'q3-a': (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-b': (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-c-advantages': (['cons-1-2'], ['planning-sustainability-environment']),
    'q3-c-disadvantages': (['cons-1-2'], ['planning-sustainability-environment']),
    'q4-a': (['cons-1-1'], ['conservation-restoration']),
    'q4-b': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q4-c': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']),
    'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-2', 'cons-3-10'], ['heat-loss-insulation', 'roofs']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-6-3', 'cons-5-8', 'cons-5-3', 'cons-5-2'], ['heat-loss-insulation', 'services-water-gas-electricity', 'hot-water-space-heating']),
    'q6-c': (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-3-4', 'cons-4-2'], ['question-1-drawing-questions', 'doors', 'walls', 'floors']),
    'q7-b': (['cons-3-7', 'cons-3-4'], ['doors', 'walls']),
    'q8-a': (['cons-5-5'], ['drainage']), 'q8-b': (['cons-5-5'], ['drainage']), 'q8-c': (['cons-5-5'], ['drainage']),
    'q9-a': (['cons-3-6', 'cons-7-4'], ['windows-light']),
    'q9-b': (['cons-7-2', 'cons-7-4'], ['windows-light']),
    'q9-c-advantages': (['cons-3-6'], ['windows-light']),
    'q9-c-disadvantages': (['cons-3-6'], ['windows-light']),
    'q10-a': (['cons-6-4', 'cons-2-4', 'cons-6-2'], ['passive-design', 'foundations', 'heat-loss-insulation']),
    'q10-b': (['cons-6-5'], ['condensation-air-tightness', 'passive-design']),
    'q10-c': (['cons-6-5'], ['condensation-air-tightness', 'passive-design']),
    'q10-alt-a': (['cons-1-2'], ['planning-sustainability-environment']),
    'q10-alt-b': (['cons-1-2'], ['planning-sustainability-environment']),
}


def composite(*panels):
    return construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 342], False), 'q2-original': (P, 2, [45, 430, 580, 688], False),
    'q3-original': (P, 3, [45, 53, 580, 410], False), 'q4-original': (P, 3, [45, 462, 580, 752], False),
    'q5-original': (P, 4, [45, 50, 580, 702], False), 'q6-original': (P, 5, [45, 53, 580, 432], False),
    'q7-original': (P, 5, [45, 481, 580, 757], False), 'q8-original': (P, 6, [45, 53, 580, 318], False),
    'q9-original': (P, 6, [45, 401, 580, 723], False), 'q10-original': (P, 7, [45, 53, 580, 466], False),
    'q10-alt-original': (P, 7, [45, 533, 580, 756], False),
    'q1-section': (S, 4, [51, 51, 550, 806], True), 'q1-ventilation': (S, 5, [51, 498, 520, 809], True),
    'q2-site-access': (S, 7, [51, 113, 540, 721], True), 'q2-ladder': (S, 8, [51, 50, 542, 484], True),
    'q2-guidelines': composite((7, [51, 113, 540, 721]), (8, [51, 50, 542, 484])),
    'q3-considerations': composite((9, [51, 51, 554, 796]), (10, [51, 50, 543, 232])),
    'q3-layout': composite((10, [51, 236, 539, 800]), (11, [51, 48, 542, 712])),
    'q4-features': composite((12, [51, 412, 544, 773]), (13, [51, 48, 554, 603])),
    'q4-refurbishment': composite((13, [51, 603, 545, 779]), (14, [51, 48, 546, 733])),
    'q4-scheme': composite((12, [51, 412, 544, 773]), (13, [51, 48, 554, 779]), (14, [51, 48, 546, 733])),
    'q5-calculation': composite((15, [51, 476, 540, 802]), (16, [51, 70, 471, 485])),
    'q5-thermal-bridge': (S, 16, [53, 485, 524, 791], True),
    'q6-low-impact': composite((17, [51, 51, 540, 709]), (18, [51, 48, 530, 361])),
    'q6-technologies': composite((18, [51, 367, 545, 767]), (19, [51, 50, 546, 803])),
    'q7-section': (S, 21, [51, 51, 531, 788], True), 'q7-threshold': (S, 22, [51, 315, 545, 741], True),
    'q8-system': composite((23, [51, 333, 532, 766]), (24, [51, 50, 526, 221])),
    'q9-requirements': composite((24, [51, 465, 552, 761]), (25, [51, 48, 537, 663])),
    'q9-calculation': (S, 26, [51, 50, 502, 438], True),
    'q10-features': composite((27, [51, 370, 549, 719]), (28, [51, 49, 563, 784]), (29, [46, 48, 543, 334])),
    'q10-mvhr': (S, 29, [46, 336, 543, 804], True),
    'q10-scheme': composite((27, [51, 370, 549, 719]), (28, [51, 49, 563, 784]), (29, [46, 48, 543, 804])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-ventilation', 'q1-complete': 'q1-section',
            'q2-b-site-access': 'q2-site-access', 'q2-b-using-a-ladder': 'q2-ladder', 'q2-b': 'q2-guidelines', 'q2-complete': 'q2-guidelines',
            'q3-a': 'q3-considerations', 'q3-b': 'q3-layout', 'q3-complete': 'q3-layout',
            'q4-a': 'q4-features', 'q4-b': 'q4-refurbishment', 'q4-complete': 'q4-scheme',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-thermal-bridge', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-low-impact', 'q6-b': 'q6-technologies', 'q6-complete': 'q6-low-impact',
            'q7-a': 'q7-section', 'q7-b': 'q7-threshold', 'q7-complete': 'q7-section', 'q8-b': 'q8-system', 'q8-complete': 'q8-system',
            'q9-a': 'q9-requirements', 'q9-b': 'q9-calculation', 'q9-complete': 'q9-calculation',
            'q10-a': 'q10-features', 'q10-b': 'q10-mvhr', 'q10-complete': 'q10-scheme'}
# A Q2 item, named only by reference to the printed list, carries the scheme's own heading after ' — '.
LABELLED = {'q2-a-communication', 'q2-a-supervision', 'q2-a-training', 'q2-b-site-access', 'q2-b-using-a-ladder'}
# Every printed item of a one-card choice keeps its scheme drawings, on the card and on its complete route.
CHOICE_FIGURE_PAGES = {'q4-b': {13, 14}, 'q4-complete': {12, 13, 14}, 'q10-a': {27, 28, 29}, 'q10-complete': {27, 28, 29}}
SCHEME_PAGES = {'1': [4, 5, 33], '2': [6, 7, 8, 34], '3': [9, 10, 11, 12, 35], '4': [12, 13, 14, 15, 36], '5': [15, 16, 37],
                '6': [17, 18, 19, 20, 38], '7': [21, 22, 39], '8': [23, 24, 40], '9': [24, 25, 26, 27, 41], '10': [27, 28, 29, 30, 42],
                '10-alt': [30, 31, 43]}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}


def tokens(text):
    return re.findall(r'[a-z0-9]+', text.replace('²', '2').lower())


def is_subsequence(needle, haystack):
    it = iter(haystack)
    return all(word in it for word in needle)


def normalise(text):
    return re.sub(r'[^a-z0-9Ā-ſ]+', '', text.lower())


def page_text(f, page):
    with fitz.open(R / f) as pdf:
        return ' '.join(pdf[page - 1].get_text().split())


def printed(text):
    for glyph, letters in LIGATURES.items():
        text = text.replace(glyph, letters)
    return text


def region(qkey):
    text = printed(page_text(P, PAPER_PAGE[qkey]))
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
        'construction-studies', 2023, 'higher', 'ev', 'main', 'single', 'LC029ALP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    assert set(cards) == set(LEAF) | set(COMPOSITE) and len(d['tasks']) == len(cards) == 50
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) not in LEGACY]
    assert len(d['addedIds']) == 21 and all(t['correction'] == (k in LEGACY) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == 50
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == set(cards) and len(d['bindings']) == 50
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 44)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 33

    for key, c in cards.items():
        qk = qkey_of(key)
        q = '10' if qk == '10-alt' else qk
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q and t['alternative'] == (qk == '10-alt')
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2023, 'higher', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2023 HL Q{qk}')
        assert c['questionFigureKey'] == f'{FP}q{qk}-original' and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[qk]] and t['requiredQuestionFigures'] == [c['questionFigureKey']]
        assert c.get('figureKey') == (FP + SOLUTION[key] if key in SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + SOLUTION[key]] if key in SOLUTION else [])
        assert figures[f'q{qk}-original']['solution'] is False and (key not in SOLUTION or figures[SOLUTION[key]]['solution'] is True)
        # Lift, never write: printed wording only; an item named by reference uses the scheme heading.
        words = tokens(printed(region(qk)))
        heads, labels = [], []
        for para in c['questionText'].split('\n\n'):
            head, _, tail = para.partition(' — ')
            heads.append(head)
            labels += tail.split('; ') if tail else []
        assert is_subsequence(tokens(' '.join(heads)), words), (key, 'questionText not lifted')
        assert all(normalise(x) in scheme for x in labels), (key, 'item label not printed in the scheme')
        assert bool(labels) == (key in LABELLED), (key, labels)
        assert is_subsequence(tokens(c['stem']), words), (key, 'stem not lifted')
        for row in c['rows']:
            assert row['contextNote'].strip()
            if row['kind'] == 'anyN':  # a closed choice: every printed option, in the scheme's own headings
                assert 'permittedMarks' not in row and row['marks'] == row['group']['claimMax'] * row['group']['perOption'], (key, row['id'])
                assert normalise(row['verbatim']) in scheme and all(normalise(o) in scheme for o in row['group']['options']), key
                continue
            assert row['kind'] == 'criterion'
            assert normalise(row['verbatim']) in scheme, (key, row['verbatim'])
            steps = row['permittedMarks']
            assert steps[0] == 0 and steps[-1] == row['marks'] and steps == sorted(set(steps)), (key, row['id'])
        assert 'questionBonus' not in c and c['totalMarks'] == sum(row['marks'] for row in c['rows'])
        assert c['totalMarks'] == PART_TOTALS[key], key
        if key in LEAF:
            assert [(row['id'], row['marks'], row.get('permittedMarks')) for row in c['rows']] == LEAF[key], key
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
    for key, pages, values in [('q5-a', [15, 16], ['0.013', '6.818', '0.154', '2.273', '0.050', '9.647', '0.104']),
                               ('q5-b', [16], ['51.714', '7,257,600', '375,319', '10.04', '12.53']),
                               ('q9-b', [26], ['18.9', '9450', '9.45'])]:
        notes = ' '.join(row['contextNote'] for row in cards[key]['rows'])
        text = ' '.join(page_text(S, p) for p in pages)
        assert all(x in notes and x in text for x in values), (key, [x for x in values if x not in notes or x not in text])
    # The alternative Question 10 never combines with the Passive House question.
    for key, c in cards.items():
        for g in c.get('taskGroups', []):
            assert key.startswith('q10-alt') == g['sourceCardId'].startswith(PREFIX + 'q10-alt')
    # Choice is not a route: the printed choice is ONE card holding one anyN group over every printed item.
    for key, (rid, n, each, options) in CHOICES.items():
        assert [row['id'] for row in cards[key]['rows']] == [rid] and cards[key]['rows'][0]['group'] == dict(claimMax=n, perOption=each, options=options), key
    assert [k for k in cards if any(row['kind'] == 'anyN' for row in cards[k]['rows']) and k not in COMPOSITE] == list(CHOICES)
    assert not [k for k in cards if re.match(r'q(4-b|10-a)-.', k)], 'per-item or per-combination route cards'
    for key, pages in CHOICE_FIGURE_PAGES.items():
        spec = FIGURES[SOLUTION[key]]
        assert pages <= {p for _, p, _ in construction_figures.panels_of(spec)}, (key, 'a choice item lost its scheme drawings')
    # One complete card per question, each worth 60.
    ledgers = d['questionRouteLedgers']
    for qk in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '10-alt']:
        whole = sorted(k for k in cards if k.startswith(f'q{qk}-complete') and qkey_of(k) == qk)
        assert len(whole) == 1 and [w['id'] for w in ledgers[qk]['wholeRoutes']] == [PREFIX + k for k in whole]
        assert all(cards[k]['totalMarks'] == 60 for k in whole)
    sel = d['selectionLedger']
    assert {k: v['cardId'] for k, v in sel['finiteQuestionChoices'].items()} == {'4b': PREFIX + 'q4-b', '10a': PREFIX + 'q10-a'}
    assert all(v['choose'] == 2 and v['options'] == CHOICES[v['cardId'].removeprefix(PREFIX)][3] for v in sel['finiteQuestionChoices'].values())
    assert 'optionSelectionsMarkedAlike' not in sel
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 9

    for key, f in figures.items():  # pixel-exact: a single crop, or a composite of exact page crops
        construction_figures.check(f, FIGURES[key], figure_dir, images)
    assert len({f['sha256'] for f in d['questionFigures']}) == 33

    # In-place corrections: same ID and concept ID, hash-linked to the pre-audit card they replace.
    legacy = {c['id']: c for c in json.loads((DRAFTS / 'prior-2023-higher-cards.json').read_text())}
    assert set(legacy) == {PREFIX + k for k in LEGACY}
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == {PREFIX + k for k in LEGACY} and len(d['corrections']) == 29
    for cid, old in legacy.items():
        new = cards[cid.removeprefix(PREFIX)]
        fix = fixes[cid]
        assert fix['priorSha256'] == construction_corrections.card_hash(old) and fix['correctedSha256'] == construction_corrections.card_hash(new), cid
        assert new['conceptId'] == old['conceptId'] and fix['reason'].strip(), cid
        assert (fix['priorTotalMarks'], fix['correctedTotalMarks'], fix['priorTopicId'], fix['correctedTopicId']) == (
            old['totalMarks'], new['totalMarks'], old['topicId'], new['topicId']), cid

    authored = json.loads((R / 'scripts/markbank/authored/construction-studies.json').read_text())
    by_id = {c['id']: c for c in authored}
    assert len(by_id) == len(authored)
    if integrated:
        prior = json.loads((DRAFTS / 'prior-authored-card-hashes.json').read_text())
        assert prior['count'] == len(prior['cards']) == 738
        for cid in fixes:
            assert prior['cards'][cid] == fixes[cid]['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        assert sorted(c for c in by_id if c.startswith(PREFIX)) == sorted(t['card']['id'] for t in d['tasks'])
        # No build-time override may replace reviewed content.
        for name in ['card-source-bindings.json', 'card-corrections.json']:
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
        assert 'retiredBuildOverrides' not in d
    elif integrated is False:  # before integration (None skips authored checks)
        assert all(construction_corrections.card_hash(by_id[cid]) == fixes[cid]['priorSha256'] for cid in fixes)
    assert d['questionsReviewed'] == [str(n) for n in range(1, 11)] and d['unreviewedQuestions'] == [] and d['alternativeQuestions'] == ['10']
    return dict(tasks=50, addedTasks=21, correctedTasks=29, leafTasks=len(LEAF),
                wholeQuestions=sum(1 for k in cards if '-complete' in k), anyNChoiceCards=len(CHOICES), sourceFigures=33, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
