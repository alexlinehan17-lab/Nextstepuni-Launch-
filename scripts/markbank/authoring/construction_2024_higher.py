"""Source-pinned validator for the 2024 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

Checks the reviewed authoring file against the original SEC paper and marking scheme: pinned hashes
and page text, lifted wording (narrowing only deletes printed words; a Q10(b) item, named by reference
to the printed list, carries the scheme's own heading after ' — '), scheme-traceable rows, the
published tariffs and steps, the printed choice Q10(a) as ONE card with an anyN group over all three
items (choice is not a route), Q4(b) as one task marked alike for either site, the separate alternative
Q10, pixel-exact figure crops (single rects and multi-page composites), the selection ledger and exact
topic/Atlas bindings. The 22 pre-audit 2024 Higher cards keep their IDs and concept IDs and are
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
REVIEW = R / 'scripts/markbank/authored/construction-studies-2024-higher-reviewed.json'
DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts/construction-2024-higher'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2024/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2024/LC029ALP000EV.pdf'
HASHES = {P: 'a236712dcac010ce50b394d73de5ebe0683267809ab53bca86e8678987966aeb',
          S: 'e3359c9c16e5e5e3fa55e04f64df714d982d4872cda62bcefd667250b0a89887'}
PREFIX = 'cons-2024-hl-'
FP = 'construction-studies-2024-HL-'
CROSS = 'construction-studies-higher-'
BAND8 = [0, 4, 6, 8]
LIGATURES = {'Ɵ': 'ti', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q3-b', 'q3-c', 'q4-a', 'q4-b', 'q5-c-advantages', 'q5-c-disadvantages', 'q6-a', 'q6-b', 'q6-c',
          'q7-a', 'q7-b', 'q8-a', 'q8-b', 'q8-c', 'q9-c', 'q10-a', 'q10-b-indoor-air-quality', 'q10-b-space-heating', 'q10-c'}
CHOICES = {'q10-a': ('items', 2, 12, ['Airtightness', 'Windows', 'Building fabric'])}


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('external-wall', 16, r(16)), ('roof', 16, r(16)), ('front-wall', 16, r(16)), ('presentation', 8, BAND8)],
    'q1-b': [('ventilation', 4, r(4))],
    'q2-a': [(k, 6, r(6)) for k in ['kitchen-1', 'kitchen-2', 'bedroom-1', 'bedroom-2']],
    'q2-b': [('line-diagram', 4, r(4)), ('items', 15, r(15)), ('dimensions', 2, r(2))],
    'q2-c': [(k, 3, r(3)) for k in ['access', 'shower', 'wc', 'basin', 'grab-rails']],
    'q3-a': [('layout', 14, r(14)), ('linking', 3, r(3)), ('daylight', 3, r(3)), ('views', 3, r(3)), ('justification', 3, r(3))],
    'q3-b': [('notes', 12, r(12)), ('sketch', 12, r(12))],
    'q3-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q4-a': [(f'reason-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q4-b': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q4-c': [('sketch', 6, r(6)), ('house', 5, r(5)), ('outdoor', 5, r(5)), ('road', 5, r(5)), ('justification', 3, r(3))],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 24, list(range(0, 25, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'pellets', 'cost']],
    'q5-c-advantages': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q5-c-disadvantages': [('disadvantage-1', 3, r(3)), ('disadvantage-2', 3, r(3))],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2)],
    'q6-c': [(f'advantage-{i}', 5, r(5)) for i in (1, 2)],
    'q7-a': [('external-wall', 20, r(20)), ('window-head', 16, r(16)), ('first-floor', 12, r(12)), ('presentation', 8, BAND8)],
    'q7-b': [('detail', 4, r(4))],
    'q8-a': [('layout', 28, r(28)), ('sizes', 4, [0, 2, 4])],
    'q8-b': [('notes', 6, r(6)), ('sketches', 6, r(6))],
    'q8-c': [(k, 4, r(4)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q9-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2)],
    'q9-b': [(k, 8, r(8)) for k in ['floor-notes', 'floor-sketches', 'wall-notes', 'wall-sketches']],
    'q9-c': [('approach-1', 4, r(4)), ('principle-1', 2, r(2)), ('approach-2', 4, r(4)), ('principle-2', 2, r(2))],
    'q10-a': [('items', 24, None)],
    'q10-b-indoor-air-quality': [('notes', 6, r(6)), ('sketches', 6, r(6))],
    'q10-b-space-heating': [('notes', 6, r(6)), ('sketches', 6, r(6))],
    'q10-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-c': ['q5-c-advantages', 'q5-c-disadvantages'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-b': ['q10-b-indoor-air-quality', 'q10-b-space-heating'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
PART_TOTALS = {'q1-a': 56, 'q1-b': 4, 'q2-a': 24, 'q2-b': 21, 'q2-c': 15, 'q3-a': 26, 'q3-b': 24, 'q3-c': 10, 'q4-a': 18, 'q4-b': 18,
               'q4-c': 24, 'q5-a': 33, 'q5-b': 15, 'q5-c-advantages': 6, 'q5-c-disadvantages': 6, 'q5-c': 12, 'q6-a': 30, 'q6-b': 20,
               'q6-c': 10, 'q7-a': 56, 'q7-b': 4, 'q8-a': 32, 'q8-b': 12, 'q8-c': 16, 'q9-a': 16, 'q9-b': 32, 'q9-c': 12, 'q10-a': 24,
               'q10-b-indoor-air-quality': 12, 'q10-b-space-heating': 12, 'q10-b': 24, 'q10-c': 12, 'q10-alt-a': 30, 'q10-alt-b': 30,
               **{k: 60 for k in COMPOSITE if '-complete' in k}}
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-10', 'cons-3-9', 'cons-3-3', 'cons-3-4'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q1-b': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q2-a': (['cons-1-2'], ['planning-sustainability-environment']),
    'q2-b': (['cons-1-2', 'cons-5-6'], ['planning-sustainability-environment', 'drainage']),
    'q2-c': (['cons-1-2', 'cons-5-6'], ['planning-sustainability-environment', 'drainage']),
    'q3-a': (['cons-1-1', 'cons-1-2', 'cons-7-4'], ['conservation-restoration', 'windows-light']),
    'q3-b': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q3-c': (['cons-1-1'], ['conservation-restoration']),
    'q4-a': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q4-b': (['cons-1-3'], ['planning-sustainability-environment']),
    'q4-c': (['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']),
    'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c-advantages': (['cons-5-3'], ['hot-water-space-heating']),
    'q5-c-disadvantages': (['cons-5-3'], ['hot-water-space-heating']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-6-3', 'cons-6-4', 'cons-6-2'], ['heat-loss-insulation', 'sustainability-the-environment']),
    'q6-c': (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-3', 'cons-3-6', 'cons-4-3'], ['question-1-drawing-questions', 'walls', 'windows-light', 'floors']),
    'q7-b': (['cons-6-5', 'cons-4-3'], ['condensation-air-tightness', 'floors']),
    'q8-a': (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating']),
    'q8-b': (['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment']),
    'q8-c': (['cons-5-3'], ['hot-water-space-heating']),
    'q9-a': (['cons-1-2', 'cons-7-4', 'cons-6-5'], ['planning-sustainability-environment', 'windows-light', 'condensation-air-tightness']),
    'q9-b': (['cons-8-3', 'cons-4-3', 'cons-4-1'], ['sound', 'floors', 'walls']),
    'q9-c': (['cons-8-3'], ['sound']),
    'q10-a': (['cons-6-5', 'cons-3-5', 'cons-6-2', 'cons-6-4'], ['passive-design', 'condensation-air-tightness', 'windows-light', 'heat-loss-insulation']),
    'q10-b-indoor-air-quality': (['cons-6-5'], ['passive-design', 'condensation-air-tightness']),
    'q10-b-space-heating': (['cons-5-3', 'cons-6-2'], ['hot-water-space-heating', 'passive-design']),
    'q10-c': (['cons-6-5', 'cons-6-2'], ['passive-design']),
    'q10-alt-a': (['cons-1-2'], ['sustainability-the-environment']),
    'q10-alt-b': (['cons-1-2'], ['sustainability-the-environment']),
}


def composite(*panels):
    return construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 375], False), 'q1-section': (S, 4, [50, 51, 552, 760], True),
    'q1-ventilation': (S, 5, [51, 506, 531, 796], True), 'q2-original': (P, 2, [45, 390, 580, 762], False),
    'q2-guidelines': composite((6, [51, 51, 546, 778]), (7, [51, 50, 539, 593])),
    'q2-layouts': (S, 8, [51, 50, 543, 792], True), 'q2-justify': (S, 9, [51, 50, 545, 794], True),
    'q3-original': (P, 3, [45, 53, 580, 411], False),
    'q3-layout': composite((10, [51, 51, 545, 591]), (11, [51, 60, 545, 587])),
    'q3-external': composite((11, [51, 591, 545, 761]), (12, [51, 50, 547, 590])),
    'q4-original': (P, 3, [45, 431, 580, 731], False), 'q4-sites': (S, 14, [51, 50, 539, 800], True),
    'q4-site-plans': (S, 15, [51, 50, 535, 715], True), 'q5-original': (P, 4, [45, 48, 580, 735], False),
    'q5-calculation': (S, 16, [51, 51, 540, 791], True), 'q6-original': (P, 5, [45, 51, 580, 423], False),
    'q6-low-impact': (S, 18, [51, 51, 549, 725], True), 'q6-features': (S, 19, [51, 50, 546, 739], True),
    'q7-original': (P, 5, [45, 430, 580, 740], False), 'q7-section': (S, 21, [51, 51, 527, 801], True),
    'q7-airtightness': (S, 22, [51, 71, 509, 381], True), 'q8-original': (P, 6, [45, 53, 580, 402], False),
    'q8-system': (S, 23, [51, 51, 545, 743], True), 'q8-renewables': (S, 24, [51, 50, 544, 789], True),
    'q9-original': (P, 6, [45, 434, 580, 722], False), 'q9-requirements': (S, 26, [51, 51, 545, 644], True),
    'q9-sound': (S, 27, [51, 50, 543, 789], True), 'q10-original': (P, 7, [45, 53, 580, 399], False),
    'q10-items': composite((29, [51, 51, 544, 789]), (30, [51, 50, 543, 728])),
    'q10-upgrade': (S, 31, [51, 50, 543, 791], True),
    'q10-scheme': composite((29, [51, 51, 544, 789]), (30, [51, 50, 543, 728]), (31, [51, 50, 543, 791])),
    'q10-alt-original': (P, 7, [45, 465, 580, 702], False),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-ventilation', 'q1-complete': 'q1-section', 'q2-a': 'q2-guidelines', 'q2-b': 'q2-layouts',
            'q2-c': 'q2-justify', 'q2-complete': 'q2-layouts', 'q3-a': 'q3-layout', 'q3-b': 'q3-external', 'q3-complete': 'q3-layout',
            'q4-b': 'q4-sites', 'q4-c': 'q4-site-plans', 'q4-complete': 'q4-site-plans', 'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation',
            'q5-complete': 'q5-calculation', 'q6-a': 'q6-low-impact', 'q6-b': 'q6-features', 'q6-complete': 'q6-low-impact',
            'q7-a': 'q7-section', 'q7-b': 'q7-airtightness', 'q7-complete': 'q7-section', 'q8-a': 'q8-system', 'q8-b': 'q8-renewables',
            'q8-complete': 'q8-system', 'q9-a': 'q9-requirements', 'q9-b': 'q9-sound', 'q9-complete': 'q9-sound', 'q10-a': 'q10-items',
            'q10-b-indoor-air-quality': 'q10-upgrade', 'q10-b-space-heating': 'q10-upgrade', 'q10-b': 'q10-upgrade', 'q10-complete': 'q10-scheme'}
# A Q10(b) item, named only by reference to the printed list, carries the scheme's own heading after ' — '.
LABELLED = {'q10-b-indoor-air-quality', 'q10-b-space-heating'}
SCHEME_PAGES = {'1': [4, 5, 36], '2': [6, 7, 8, 9, 37], '3': [10, 11, 12, 13, 38], '4': [13, 14, 15, 39], '5': [16, 17, 40],
                '6': [18, 19, 20, 41], '7': [21, 22, 42], '8': [23, 24, 25, 43], '9': [26, 27, 28, 44], '10': [29, 30, 31, 32, 45],
                '10-alt': [33, 34, 46]}
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
        'construction-studies', 2024, 'higher', 'ev', 'main', 'single', 'LC029ALP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    assert set(cards) == set(LEAF) | set(COMPOSITE) and len(d['tasks']) == len(cards) == 45
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) not in LEGACY]
    assert len(d['addedIds']) == 23 and all(t['correction'] == (k in LEGACY) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == 45
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == set(cards) and len(d['bindings']) == 45
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 47)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 32

    for key, c in cards.items():
        qk = qkey_of(key)
        q = '10' if qk == '10-alt' else qk
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q and t['alternative'] == (qk == '10-alt')
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2024, 'higher', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f'2024 HL Q{qk}')
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
    for key, page, values in [('q5-a', 16, ['0.018', '5.000', '0.117', '1.667', '0.050', '0.022', '7.044', '0.142']),
                              ('q5-b', 16, ['218.6269', '4,838,400', '1,057,804', '60.96', '31.71'])]:
        notes = ' '.join(row['contextNote'] for row in cards[key]['rows'])
        text = page_text(S, page)
        assert all(x in notes and x in text for x in values), (key, [x for x in values if x not in notes or x not in text])
    # The alternative Question 10 never combines with the EnerPHit question.
    for key, c in cards.items():
        for g in c.get('taskGroups', []):
            assert key.startswith('q10-alt') == g['sourceCardId'].startswith(PREFIX + 'q10-alt')
    # Choice is not a route: the printed choice is ONE card holding one anyN group over every printed item.
    for key, (rid, n, each, options) in CHOICES.items():
        assert [row['id'] for row in cards[key]['rows']] == [rid] and cards[key]['rows'][0]['group'] == dict(claimMax=n, perOption=each, options=options), key
    assert [k for k in cards if any(row['kind'] == 'anyN' for row in cards[k]['rows']) and k not in COMPOSITE] == list(CHOICES)
    assert not [k for k in cards if re.match(r'q(4-b|10-a)-.', k)], 'per-item, per-site or per-combination route cards'
    # One complete card per question, each worth 60.
    ledgers = d['questionRouteLedgers']
    for qk in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '10-alt']:
        whole = sorted(k for k in cards if k.startswith(f'q{qk}-complete') and qkey_of(k) == qk)
        assert len(whole) == 1 and [w['id'] for w in ledgers[qk]['wholeRoutes']] == [PREFIX + k for k in whole]
        assert all(cards[k]['totalMarks'] == 60 for k in whole)
    sel = d['selectionLedger']
    assert {k: v['cardId'] for k, v in sel['finiteQuestionChoices'].items()} == {'10a': PREFIX + 'q10-a'}
    assert sel['optionSelectionsMarkedAlike'] == {'4b': dict(options=['site A', 'site B'], cardId=PREFIX + 'q4-b')}
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 6

    for key, f in figures.items():  # pixel-exact: a single crop, or a composite of exact page crops
        construction_figures.check(f, FIGURES[key], figure_dir, images)
    assert len({f['sha256'] for f in d['questionFigures']}) == 32

    # In-place corrections: same ID and concept ID, hash-linked to the pre-audit card they replace.
    legacy = {c['id']: c for c in json.loads((DRAFTS / 'prior-2024-higher-cards.json').read_text())}
    assert set(legacy) == {PREFIX + k for k in LEGACY}
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == {PREFIX + k for k in LEGACY} and len(d['corrections']) == 22
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
        assert prior['count'] == len(prior['cards']) == 710
        for cid in fixes:
            assert prior['cards'][cid] == fixes[cid]['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        assert sorted(c for c in by_id if c.startswith(PREFIX)) == sorted(t['card']['id'] for t in d['tasks'])
        # No build-time override may replace reviewed content.
        for name in ['card-source-bindings.json', 'card-corrections.json']:
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
        assert [x['cardId'] for x in d.get('retiredBuildOverrides', [])] == [PREFIX + 'q8-a']
    elif integrated is False:  # before integration (None skips authored checks)
        assert all(construction_corrections.card_hash(by_id[cid]) == fixes[cid]['priorSha256'] for cid in fixes)
    assert d['questionsReviewed'] == [str(n) for n in range(1, 11)] and d['unreviewedQuestions'] == [] and d['alternativeQuestions'] == ['10']
    return dict(tasks=45, addedTasks=23, correctedTasks=22, leafTasks=len(LEAF),
                wholeQuestions=sum(1 for k in cards if '-complete' in k), anyNChoiceCards=len(CHOICES), sourceFigures=32, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
