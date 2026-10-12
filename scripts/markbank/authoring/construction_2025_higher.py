"""Source-pinned validator for the 2025 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

Checks the reviewed authoring file against the original SEC paper and marking scheme: pinned
hashes and page text, lifted wording (narrowing only deletes printed words; a Q2(c) activity, named by
reference to 2(b), carries the scheme's own heading after ' — '), scheme-traceable rows, the
published tariffs and steps, every printed choice as ONE card with an anyN group over all its items
(Q2(a) any two of three, Q8(b) any three of four, Q10(a) any two of three: choice is not a route),
the separate alternative Q10, pixel-exact figure crops, the selection ledger and exact topic/Atlas
bindings. The pre-audit 2025 Higher cards keep their IDs and concept IDs: 18 are corrected in place
(hash-linked to the card each replaced) and three per-item cards of a choice are consolidated into
the surviving card for that part through a progress alias; every other prior card stays byte-identical.
"""
import copy
import hashlib
import json
import re
from pathlib import Path

import fitz
from PIL import Image, ImageChops

import construction_corrections

R = Path(__file__).resolve().parents[3]
REVIEW = R / 'scripts/markbank/authored/construction-studies-2025-higher-reviewed.json'
DRAFTS = R / 'docs/markbank-audit/2026-09-28/drafts/construction-2025-higher'
FIGURE_DIR = R / 'public/exam-figures/construction-studies/markbank'
P = 'paper-trail-corpus/exampapers/2025/LC029ALP000EV.pdf'
S = 'paper-trail-corpus/markingschemes/2025/LC029ALP000EV.pdf'
HASHES = {P: 'b0779f335d38e88afcae39af2e5aa9124a53e3472aa3a9f535c7d9989ebb8dec',
          S: 'c9ca8dee72bc663d239244d9cde736b284de65540f48bb7aa9763d0baed1189b'}
PREFIX = 'cons-2025-hl-'
FP = 'construction-studies-2025-HL-'
CROSS = 'construction-studies-higher-'
BAND8 = [0, 4, 6, 8]
PAGE = [48, 46, 591, 803]
ACTIVITIES = ['deep-trench', 'attic-insulation', 'chimney-capping']
ITEMS6 = ['indoor-air-quality', 'natural-light', 'materials-and-finishes']
# Printed ligature glyphs in the paper's text layer (page 6 prints "airƟght", "beneﬁts").
LIGATURES = {'Ɵ': 'ti', 'ﬁ': 'fi', 'ﬂ': 'fl', 'ﬀ': 'ff', 'ﬃ': 'ffi', 'ﬄ': 'ffl'}
LEGACY = {'q1-a', 'q1-b', 'q2-a-safety-training', 'q2-c',
          'q3-b', 'q3-c', 'q4-a', 'q5-c', 'q6-b-indoor-air-quality', 'q6-b-natural-light', 'q6-b-materials-and-finishes',
          'q6-c', 'q7-b', 'q8-a', 'q9-a', 'q9-c', 'q10-a-building-form', 'q10-b'}
CONSOLIDATED = {'q2-a-health-and-safety-officer': 'q2-a-safety-training', 'q2-a-risk-assessment-audit': 'q2-a-safety-training',
                'q10-a-foundation-design': 'q10-a-building-form'}
CHOICES = {'q2-a-safety-training': ('importance', 2, 6, ['Safety training', 'Health and safety officer', 'Risk assessment audit']),
           'q8-b': ('locations', 3, 16, ['Head of external door', 'First floor junction with external wall', 'Wallplate level',
                                         'MVHR duct protruding through the ceiling']),
           'q10-a-building-form': ('items', 2, 10, ['Building form', 'Foundation design', 'Space heating energy demand'])}


def r(n):
    return list(range(n + 1))


LEAF = {
    'q1-a': [('foundation-floor', 20, r(20)), ('external-wall', 16, r(16)), ('window', 12, r(12)), ('presentation', 8, BAND8)],
    'q1-b': [('radon', 4, r(4))],
    'q2-a-safety-training': [('importance', 12, None)],
    **{f'q2-b-{a}': [('risk', 4, r(4))] for a in ACTIVITIES},
    **{f'q2-c-{a}': [('guideline-1', 6, r(6)), ('guideline-2', 6, r(6))] for a in ACTIVITIES},
    'q3-a': [('layout', 16, r(16)), ('bathroom', 2, r(2)), ('open-plan', 2, r(2)), ('daylight', 2, r(2))],
    'q3-b': [(f'reason-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-c': [('notes', 10, r(10)), ('sketch', 10, r(10))],
    'q4-a': [(f'requirement-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q4-b': [('construction-1', 15, r(15)), ('construction-2', 15, r(15))],
    'q4-c': [('construction-1', 6, r(6)), ('construction-2', 6, r(6))],
    'q5-a': [('external-surface', 3, r(3)), ('internal-surface', 3, r(3)), ('layers', 21, r(21)), ('total-resistance', 3, r(3)), ('u-value', 3, r(3))],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'pellets', 'cost']],
    'q5-c': [(k, 3, r(3)) for k in ['required-resistance', 'difference', 'formula', 'thickness']],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    **{f'q6-b-{i}': [('contribution', 6, r(6))] for i in ITEMS6},
    'q6-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q7-a': [('construction', 40, r(40)), ('slate-courses', 6, r(6)), ('presentation', 8, BAND8)],
    'q7-b': [('detail', 6, r(6))],
    'q8-a': [(f'benefit-{i}', 6, r(6)) for i in (1, 2)],
    'q8-b': [('locations', 48, None)],
    'q9-a': [('distribution-board', 5, r(5)), ('single-switch', 5, r(5)), ('light-points', 5, r(5)), ('cabling', 15, r(15)), ('cable-size-colour', 4, r(4))],
    'q9-b': [(f'feature-{i}', 8, r(8)) for i in (1, 2)],
    'q9-c': [(f'approach-{i}', 5, r(5)) for i in (1, 2)],
    'q10-a-building-form': [('items', 20, None)],
    'q10-b': [('sketch', 8, r(8)), ('orientation', 4, r(4)), ('sunpath', 4, r(4)), ('benefit-1', 6, r(6)), ('benefit-2', 6, r(6))],
    'q10-c': [('method-1', 6, r(6)), ('method-2', 6, r(6))],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'],
    'q2-b': [f'q2-b-{a}' for a in ACTIVITIES], 'q2-c': [f'q2-c-{a}' for a in ACTIVITIES],
    'q2-complete': ['q2-a-safety-training', 'q2-b', *[f'q2-c-{a}' for a in ACTIVITIES]],
    'q3-complete': ['q3-a', 'q3-b', 'q3-c'], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'],
    'q6-b': [f'q6-b-{i}' for i in ITEMS6], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'],
    'q8-complete': ['q8-a', 'q8-b'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
    'q10-complete': ['q10-a-building-form', 'q10-b', 'q10-c'],
    'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
PART_TOTALS = {'q1-a': 56, 'q1-b': 4, 'q2-b': 12, 'q2-c': 36, 'q3-a': 22, 'q3-b': 18, 'q3-c': 20, 'q4-a': 18, 'q4-b': 30, 'q4-c': 12,
               'q5-a': 33, 'q5-b': 15, 'q5-c': 12, 'q6-a': 30, 'q6-b': 18, 'q6-c': 12, 'q7-a': 54, 'q7-b': 6, 'q8-a': 12,
               'q9-a': 34, 'q9-b': 16, 'q9-c': 10, 'q10-b': 28, 'q10-c': 12, 'q10-alt-a': 30, 'q10-alt-b': 30,
               'q2-a-safety-training': 12, **{f'q2-b-{a}': 4 for a in ACTIVITIES},
               **{f'q2-c-{a}': 12 for a in ACTIVITIES}, **{f'q6-b-{i}': 6 for i in ITEMS6}, 'q8-b': 48, 'q10-a-building-form': 20,
               **{k: 60 for k in COMPOSITE if '-complete' in k}}
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-4-2', 'cons-3-3', 'cons-3-6'], ['question-1-drawing-questions', 'foundations', 'floors', 'walls', 'windows-light']),
    'q1-b': (['cons-3-4', 'cons-4-2'], ['walls', 'floors']),
    'q2-a-safety-training': (['cons-1-8'], ['site-safety']),
    **{f'q2-{p}-{x}': (['cons-1-8'], ['site-safety']) for p, xs in [('b', ACTIVITIES), ('c', ACTIVITIES)] for x in xs},
    'q3-a': (['cons-1-2', 'cons-7-4', 'cons-6-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-b': (['cons-1-2', 'cons-6-4', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q4-a': (['cons-3-2', 'cons-3-3'], ['walls']), 'q4-b': (['cons-3-3', 'cons-6-2'], ['walls', 'heat-loss-insulation']),
    'q4-c': (['cons-3-3'], ['walls']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b-indoor-air-quality': (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness']),
    'q6-b-natural-light': (['cons-7-4'], ['windows-light']),
    'q6-b-materials-and-finishes': (['cons-6-5', 'cons-1-2'], ['condensation-air-tightness', 'sustainability-the-environment']),
    'q6-c': (['cons-1-2'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-5-7', 'cons-3-10', 'cons-3-9'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs']),
    'q7-b': (['cons-3-10', 'cons-5-7'], ['roofs', 'fireplaces-fire-prevention']),
    'q8-a': (['cons-6-5', 'cons-6-2'], ['condensation-air-tightness', 'heat-loss-insulation']),
    'q8-b': (['cons-6-5', 'cons-6-6', 'cons-3-7', 'cons-4-3', 'cons-3-10'], ['condensation-air-tightness', 'doors', 'floors', 'roofs']),
    **{f'q9-{p}': (['cons-5-8'], ['services-water-gas-electricity']) for p in 'abc'},
    'q10-a-building-form': (['cons-6-4', 'cons-6-2', 'cons-2-4', 'cons-6-3'], ['passive-design', 'foundations', 'heat-loss-insulation']),
    'q10-b': (['cons-6-4'], ['passive-design']), 'q10-c': (['cons-6-4'], ['passive-design']),
    'q10-alt-a': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q10-alt-b': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
}
FIGURES = {
    'q1-original': (P, 2, [45, 50, 575, 380], False), 'q1-section': (S, 4, PAGE, True), 'q1-radon': (S, 5, [48, 580, 568, 760], True),
    'q2-original': (P, 2, [45, 440, 580, 750], False), 'q2-trench': (S, 8, PAGE, True), 'q2-attic': (S, 9, [48, 46, 582, 384], True),
    'q2-chimney': (S, 9, [48, 384, 582, 790], True), 'q3-original': (P, 3, [45, 50, 580, 455], False),
    'q3-layout-1': (S, 10, PAGE, True), 'q3-layout-2': (S, 11, PAGE, True), 'q3-garage': (S, 13, PAGE, True),
    'q4-original': (P, 3, [45, 470, 580, 745], False), 'q4-requirements': (S, 14, PAGE, True), 'q4-walls': (S, 15, PAGE, True),
    'q5-original': (P, 4, [45, 50, 575, 750], False), 'q5-calculation': (S, 20, PAGE, True), 'q5-thickness': (S, 21, [48, 46, 568, 380], True),
    'q6-original': (P, 5, [45, 50, 580, 470], False), 'q6-low-impact': (S, 22, PAGE, True),
    'q7-original': (P, 5, [45, 500, 580, 760], False), 'q7-section': (S, 25, PAGE, True), 'q7-flashing': (S, 26, [48, 45, 568, 622], True),
    'q8-original': (P, 6, [45, 50, 575, 395], False),
   
    'q9-original': (P, 6, [45, 455, 575, 740], False),
    'q9-wiring': (S, 29, PAGE, True), 'q9-safety': (S, 30, [48, 46, 568, 446], True), 'q10-original': (P, 7, [45, 50, 580, 410], False),
   
    'q10-orientation': (S, 32, [48, 314, 568, 790], True),
    'q10-overheating': (S, 33, PAGE, True), 'q10-alt-original': (P, 7, [45, 490, 580, 725], False),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-radon', 'q1-complete': 'q1-section',
            'q2-c-deep-trench': 'q2-trench', 'q2-c-attic-insulation': 'q2-attic', 'q2-c-chimney-capping': 'q2-chimney', 'q2-c': 'q2-trench',
            'q2-complete': 'q2-trench',
            'q3-a': 'q3-layout-1', 'q3-c': 'q3-garage', 'q3-complete': 'q3-layout-1',
            'q4-a': 'q4-requirements', 'q4-b': 'q4-walls', 'q4-complete': 'q4-walls',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-thickness', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-low-impact', 'q6-complete': 'q6-low-impact', 'q7-a': 'q7-section', 'q7-b': 'q7-flashing', 'q7-complete': 'q7-section',
            'q9-a': 'q9-wiring', 'q9-b': 'q9-safety', 'q9-complete': 'q9-wiring',
            'q10-b': 'q10-orientation', 'q10-c': 'q10-overheating', 'q10-complete': 'q10-orientation'}
# A Q2(c) activity, named only by reference to 2(b), carries the scheme's own heading after ' — '.
LABELLED = {f'q2-c-{a}' for a in ACTIVITIES}
SCHEME_PAGES = {'1': [4, 5, 37], '2': [6, 7, 8, 9, 38], '3': [10, 11, 12, 13, 39], '4': [14, 15, 16, 17, 18, 19, 40],
                '5': [20, 21, 41], '6': [22, 23, 24, 42], '7': [25, 26, 43], '8': [27, 28, 44],
                '9': [29, 30, 45], '10': [31, 32, 33, 46], '10-alt': [34, 35, 47]}
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
        'construction-studies', 2025, 'higher', 'ev', 'main', 'single', 'LC029ALP000EV.pdf')
    cards = {t['card']['id'].removeprefix(PREFIX): t['card'] for t in d['tasks']}
    tasks = {t['card']['id'].removeprefix(PREFIX): t for t in d['tasks']}
    assert set(cards) == set(LEAF) | set(COMPOSITE) and len(d['tasks']) == len(cards) == 49
    assert d['addedIds'] == [t['card']['id'] for t in d['tasks'] if t['card']['id'].removeprefix(PREFIX) not in LEGACY]
    assert len(d['addedIds']) == 31 and all(t['correction'] == (k in LEGACY) for k, t in tasks.items())
    assert len({c['questionRef'] for c in cards.values()}) == 49
    bindings = {b['cardId'].removeprefix(PREFIX): b for b in d['bindings']}
    assert set(bindings) == set(cards) and len(d['bindings']) == 49
    scheme = normalise(' '.join(page_text(S, p) for p in range(1, 48)))
    crosswalk = json.loads((R / 'data/examTopics/construction-studies-curriculum-crosswalk.json').read_text())
    library_nodes = {n for nodes in crosswalk.values() for n in nodes}
    figures = {f['key'].removeprefix(FP): f for f in d['questionFigures']}
    assert set(figures) == set(FIGURES) and len(d['questionFigures']) == 30

    for key, c in cards.items():
        qk = qkey_of(key)
        q = '10' if qk == '10-alt' else qk
        t, b = tasks[key], bindings[key]
        assert t['questionNumber'] == b['questionNumber'] == q and t['alternative'] == (qk == '10-alt')
        assert (c['subjectId'], c['year'], c['level'], c['section']) == ('construction-studies', 2025, 'higher', 'B')
        assert c['tariffModel'] == {'kind': 'fixed'} and c['questionRef'].startswith(f"2025 HL Q{qk}")
        assert c['questionFigureKey'] == f'{FP}q{qk}-original' and c['questionFigureIncludesPrompt'] is True
        assert c['sourceMaterial']['pages'] == [1, PAPER_PAGE[qk]] and t['requiredQuestionFigures'] == [c['questionFigureKey']]
        assert c.get('figureKey') == (FP + SOLUTION[key] if key in SOLUTION else None), key
        assert t['requiredSolutionFigures'] == ([FP + SOLUTION[key]] if key in SOLUTION else [])
        if key in SOLUTION:
            assert figures[SOLUTION[key]]['solution'] is True
        assert figures[f'q{qk}-original']['solution'] is False
        # Lift, never write: printed wording only; an item named by reference uses the scheme heading.
        words = tokens(region(qk))
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
                assert all(normalise(o) in scheme for o in row['group']['options']), (key, 'option not printed in the scheme')
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
    for key, page, values in [('q5-a', 20, ['0.012', '3.333', '0.035', '0.210', '0.676', '0.078', '0.017', '4.531', '0.221']),
                              ('q5-b', 20, ['413.712', '5,821,200', '2,408,300.29', '138.810', '€76.34']),
                              ('q5-c', 21, ['9.091', '4.525', '4.566', '0.137', '137 mm'])]:
        notes = ' '.join(row['contextNote'] for row in cards[key]['rows'])
        text = page_text(S, page)
        assert all(x in notes and x in text for x in values), (key, [x for x in values if x not in notes or x not in text])
    # The alternative Question 10 never combines with the Passive House question.
    for key, c in cards.items():
        for g in c.get('taskGroups', []):
            assert key.startswith('q10-alt') == g['sourceCardId'].startswith(PREFIX + 'q10-alt')
    # Choice is not a route: each printed choice is ONE card holding one anyN group over every printed item.
    for key, (rid, n, each, options) in CHOICES.items():
        assert cards[key]['rows'][0]['id'] == rid and cards[key]['rows'][0]['group'] == dict(claimMax=n, perOption=each, options=options), key
    assert not [k for k in cards if re.match(r'q(2-a|8-b|10-a)-.', k) and k not in CHOICES], 'per-item or per-combination route cards'
    # One complete card per question, each worth 60.
    ledgers = d['questionRouteLedgers']
    for qk in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '10-alt']:
        whole = sorted(k for k in cards if k.startswith(f'q{qk}-complete') and qkey_of(k) == qk)
        assert whole and {w['id'] for w in ledgers[qk]['wholeRoutes']} == {PREFIX + k for k in whole}
        assert all(cards[k]['totalMarks'] == 60 for k in whole)
    assert [len(ledgers[q]['wholeRoutes']) for q in ['2', '8', '10']] == [1, 1, 1]
    sel = d['selectionLedger']
    assert {k: v['cardId'] for k, v in sel['finiteQuestionChoices'].items()} == {
        '2a': PREFIX + 'q2-a-safety-training', '8b': PREFIX + 'q8-b', '10a': PREFIX + 'q10-a-building-form'}
    assert sel['unclassified'] == 0 and all(x['classification'] for x in sel['rows'])
    observed = []
    with fitz.open(R / P) as pdf:
        for i, p in enumerate(pdf):
            observed.extend((i + 1, m.start(), m.group()) for m in re.finditer(sel['pattern'], ' '.join(p.get_text().split()), re.I))
    assert observed == [(x['page'], x['start'], x['match']) for x in sel['rows']] and len(observed) == 5

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
    assert len({f['sha256'] for f in d['questionFigures']}) == 30

    # In-place corrections: same ID and concept ID, hash-linked to the pre-audit card they replace.
    legacy = {c['id']: c for c in json.loads((DRAFTS / 'prior-2025-higher-cards.json').read_text())}
    assert set(legacy) == {PREFIX + k for k in LEGACY | set(CONSOLIDATED)}
    fixes = {x['cardId']: x for x in d['corrections']}
    assert set(fixes) == {PREFIX + k for k in LEGACY} and len(d['corrections']) == 18
    merged = {x['cardId']: x for x in d['consolidatedLegacy']}
    assert merged == {PREFIX + k: dict(cardId=PREFIX + k, aliasOf=PREFIX + v, preCorrectionSha256=construction_corrections.card_hash(legacy[PREFIX + k]))
                      for k, v in CONSOLIDATED.items()}
    for cid, old in legacy.items():
        if cid in merged:
            continue
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
        assert prior['count'] == len(prior['cards']) == 1018
        for cid in fixes:
            assert prior['cards'][cid] == fixes[cid]['priorSha256'], cid
        construction_corrections.assert_prior_cards_preserved(prior['cards'], by_id)
        assert all(by_id[t['card']['id']] == t['card'] for t in d['tasks'])
        # The consolidated per-item cards are withdrawn through a recorded progress alias to their surviving card.
        gone = {w['cardId']: w for w in d.get('withdrawn', [])}
        aliases = construction_corrections.card_aliases()
        for cid, m in merged.items():
            assert cid not in by_id and gone[cid]['aliasOf'] == m['aliasOf'] == aliases[cid], cid
            assert gone[cid]['preCorrectionSha256'] == m['preCorrectionSha256'] == prior['cards'][cid], cid
        # No build-time override may replace reviewed content.
        for name in ['card-source-bindings.json', 'card-corrections.json']:
            overrides = json.loads((R / 'scripts/markbank' / name).read_text()).get('construction-studies', {})
            assert not [k for k in overrides if k.startswith(PREFIX)], name
        assert [x['cardId'] for x in d.get('retiredBuildOverrides', [])] == [PREFIX + 'q10-b']
    elif integrated is False:  # before integration (None skips authored checks, for a consolidation)
        assert all(construction_corrections.card_hash(by_id[cid]) == fixes[cid]['priorSha256'] for cid in fixes)
    assert d['questionsReviewed'] == [str(n) for n in range(1, 11)] and d['unreviewedQuestions'] == [] and d['alternativeQuestions'] == ['10']
    return dict(tasks=49, addedTasks=31, correctedTasks=18, consolidatedLegacy=3, leafTasks=len(LEAF),
                wholeQuestions=sum(1 for k in cards if '-complete' in k), anyNChoiceCards=len(CHOICES), sourceFigures=30, paperComplete=True)


if __name__ == '__main__':
    print(json.dumps(validate(json.loads(REVIEW.read_text()))))
