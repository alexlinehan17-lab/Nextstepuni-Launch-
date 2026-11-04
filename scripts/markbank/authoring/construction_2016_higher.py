"""Source-pinned validator for the 2016 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8(b) and Q10(a) any-two
cards, the Q2(b) item cards composed into (b), selection words, the 22 pre-audit cards corrected in place and
the five retired build overrides), checked by the shared engine construction_paper.validate against the
pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2016_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2016, 'higher'
HASHES = ('a5bd5ecc2755e771f98bb2e6b13e3a95af33521592d128d05e676be556be5de9', 'c6e563e2a60a0c2c660cc215179795443b2c8ae93a15f5ad410bfd2f7e448f81')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 906
PRES = [0, 2, 3, 4, 5, 6, 7, 8]
Q2B = ['level-of-risk', 'duration-of-task']
LEGACY = ({'q2-a', 'q2-c', 'q3-a', 'q3-b', 'q4-a', 'q4-b', 'q4-c', 'q5-b', 'q5-c', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q8-a', 'q9-a', 'q9-c',
           'q10-a', 'q10-b', 'q10-c'} | {f'q2-b-{k}' for k in Q2B})
CHOICES = {'q8-b': ('areas', 2, 16, ['Upgrading walls', 'Upgrading roof', 'Upgrading floor']),
           'q10-a': ('items', 2, 12, ['Foundations', 'Ground Floor', 'Walls'])}
FINITE = {'8b': 'q8-b', '10a': 'q10-a'}
LABELLED = {f'q2-b-{k}' for k in Q2B}
RETIRED = [('card-source-bindings.json', k) for k in ['q6-a', 'q10-b', 'q7-b']] + [('card-corrections.json', k) for k in ['q6-a', 'q10-b']]
LEDGER = [(1, 'Answer Question'), (2, 'or'), (4, 'Select'), (4, 'any two'), (5, 'any two'), (5, 'OR'), (5, 'One of')]
LEAF = {
    'q1-a': [('details', 44, list(range(0, 45, 4))), ('dimensions', 4, r(4)), ('presentation', 8, PRES)],
    'q1-b': [('abutment', 4, r(4))],
    'q2-a': [('training', 6, r(6)), ('responsibility', 6, r(6))],
    **{f'q2-b-{k}': [('item', 6, r(6))] for k in Q2B},
    'q2-c': [(f'guideline-{i}', 12, r(12)) for i in (1, 2, 3)],
    'q3-a': [('envelope', 20, r(20)), ('layout', 20, r(20))],
    'q3-b': [(f'redesign-{i}', 10, r(10)) for i in (1, 2)],
    'q4-a': [(f'reason-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q4-b': [(k, 6, r(6)) for k in ['sketches', 'location', 'entrance', 'justification-1', 'justification-2']],
    'q4-c': [(k, 3, r(3)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q5-a': [('resistances', 24, list(range(0, 25, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, r(3))],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [(k, 3, r(3)) for k in ['required-resistance', 'existing-resistance', 'difference', 'formula', 'thickness']],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [('notes', 10, r(10)), ('sketches', 10, r(10))],
    'q6-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q7-a': [('details', 44, list(range(0, 45, 4))), ('presentation', 8, PRES)],
    'q7-b': [('detail-1', 2, r(2)), ('detail-2', 2, r(2)), ('dimensions', 4, r(4))],
    'q8-a': [(k, 5, r(5)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q8-b': [('areas', 32, None), ('justification-1', 4, r(4)), ('justification-2', 4, r(4))],
    'q9-a': [('ring', 4, r(4)), ('radial', 4, r(4))],
    'q9-b': [('sketch', 12, r(12)), ('sizes', 6, r(6)), ('colours', 6, r(6)), ('safety-1', 6, r(6)), ('safety-2', 6, r(6))],
    'q9-c': [('feature-1', 8, r(8)), ('feature-2', 8, r(8))],
    'q10-a': [('items', 24, None)],
    'q10-b': [(k, 6, r(6)) for k in ['reason-1', 'reason-2', 'detail-1', 'detail-2']],
    'q10-c': [(k, 3, r(3)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-b': [f'q2-b-{k}' for k in Q2B], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'],
    'q3-complete': ['q3-a', 'q3-b'], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q2-b': 12, **{k: 60 for k in COMPOSITE if k.endswith('-complete')}})
SAFE = (['cons-1-8'], ['site-safety'])
LIGHT = (['cons-7-4', 'cons-1-2'], ['windows-light', 'planning-sustainability-environment'])
ELEC = (['cons-5-8'], ['services-water-gas-electricity'])
REUSE = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-10', 'cons-3-3', 'cons-3-6'], ['question-1-drawing-questions', 'roofs', 'walls', 'windows-light']),
    'q1-b': (['cons-3-10', 'cons-3-4'], ['roofs', 'walls']),
    'q2-a': SAFE, **{f'q2-b-{k}': SAFE for k in Q2B}, 'q2-c': SAFE,
    'q3-a': LIGHT, 'q3-b': LIGHT,
    'q4-a': (['cons-1-3'], ['planning-sustainability-environment']), 'q4-b': (['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment']),
    'q4-c': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-5-8', 'cons-6-4'], ['services-water-gas-electricity', 'sustainability-the-environment']),
    'q6-c': (['cons-1-2', 'cons-5-8'], ['sustainability-the-environment', 'services-water-gas-electricity']),
    'q7-a': (['cons-1-5', 'cons-5-7', 'cons-3-9', 'cons-3-10'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs']),
    'q7-b': (['cons-5-7'], ['fireplaces-fire-prevention']),
    'q8-a': REUSE,
    'q8-b': (['cons-1-1', 'cons-3-3', 'cons-3-9', 'cons-4-2', 'cons-6-2'], ['conservation-restoration', 'walls', 'roofs', 'floors', 'heat-loss-insulation']),
    'q9-a': ELEC, 'q9-b': ELEC, 'q9-c': (['cons-5-8', 'cons-7-4'], ['services-water-gas-electricity', 'windows-light']),
    'q10-a': (['cons-6-2', 'cons-2-4', 'cons-4-2', 'cons-3-3'], ['passive-design', 'foundations', 'floors', 'walls']),
    'q10-b': (['cons-6-4', 'cons-6-5'], ['passive-design']),
    'q10-c': (['cons-1-3', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation']),
    'q10-alt-discussion': REUSE, 'q10-alt-guidelines': REUSE,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 290], False), 'q2-original': (P, 2, [30, 290, 580, 490], False),
    'q3-original': (P, 2, [30, 490, 580, 790], False), 'q4-original': (P, 3, [30, 39, 580, 270], False),
    'q5-original': (P, 3, [30, 272, 580, 760], False), 'q6-original': (P, 4, [30, 39, 580, 315], False),
    'q7-original': (P, 4, [30, 315, 580, 540], False), 'q8-original': (P, 4, [30, 543, 580, 785], False),
    'q9-original': (P, 5, [30, 39, 580, 250], False), 'q10-original': (P, 5, [30, 252, 580, 490], False),
    'q10-alt-original': (P, 5, [30, 555, 580, 670], False),
    'q1-section': composite((4, [45, 50, 575, 790]), (5, [45, 60, 575, 790]), (6, [45, 50, 575, 625])),
    'q2-culture': composite((6, [45, 625, 575, 790]), (7, [45, 50, 575, 750])),
    'q2-level-of-risk': (S, 8, [45, 50, 575, 348], True), 'q2-duration-of-task': (S, 8, [45, 348, 575, 589], True),
    'q2-ladder': (S, 8, [45, 50, 575, 589], True), 'q2-guidelines': (S, 8, [45, 589, 575, 795], True),
    'q3-redesign': (S, 9, [45, 50, 575, 418], True), 'q3-reasons': composite((9, [45, 418, 575, 790]), (10, [45, 50, 575, 245])),
    'q4-reasons': (S, 10, [45, 260, 575, 458], True), 'q4-layout': (S, 10, [45, 458, 575, 790], True), 'q4-one-off': (S, 11, [45, 50, 575, 425], True),
    'q5-calculation': composite((12, [45, 50, 575, 770]), (13, [45, 50, 575, 205])), 'q5-thickness': (S, 13, [45, 208, 575, 470], True),
    'q6-features': composite((13, [45, 485, 575, 790]), (14, [45, 50, 575, 334])),
    'q6-renewable': composite((14, [45, 334, 575, 790]), (15, [45, 50, 575, 355])), 'q6-advantages': (S, 15, [45, 355, 575, 765], True),
    'q7-section': (S, 16, [45, 50, 575, 785], True),
    'q8-advantages': (S, 17, [45, 50, 575, 640], True),
    'q8-upgrades': composite((17, [45, 640, 575, 790]), (18, [45, 50, 575, 790]), (19, [45, 50, 575, 790]), (20, [45, 50, 575, 292])),
    'q9-circuits': (S, 20, [45, 455, 575, 765], True), 'q9-lighting': (S, 21, [45, 50, 575, 445], True), 'q9-economy': (S, 21, [45, 445, 575, 775], True),
    'q10-principles': (S, 22, [45, 50, 575, 785], True),
    'q10-overheating': composite((23, [45, 50, 575, 790]), (24, [45, 50, 575, 165])), 'q10-planning': (S, 24, [45, 168, 575, 500], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-culture', 'q2-b-level-of-risk': 'q2-level-of-risk', 'q2-b-duration-of-task': 'q2-duration-of-task', 'q2-b': 'q2-ladder',
            'q2-c': 'q2-guidelines', 'q2-complete': 'q2-guidelines',
            'q3-a': 'q3-redesign', 'q3-b': 'q3-reasons', 'q3-complete': 'q3-redesign',
            'q4-a': 'q4-reasons', 'q4-b': 'q4-layout', 'q4-c': 'q4-one-off', 'q4-complete': 'q4-layout',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-thickness', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-renewable', 'q6-c': 'q6-advantages', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-advantages', 'q8-b': 'q8-upgrades', 'q8-complete': 'q8-upgrades',
            'q9-a': 'q9-circuits', 'q9-b': 'q9-lighting', 'q9-c': 'q9-economy', 'q9-complete': 'q9-lighting',
            'q10-a': 'q10-principles', 'q10-b': 'q10-overheating', 'q10-c': 'q10-planning', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q8-b': {17, 18, 19, 20}, 'q8-complete': {17, 18, 19, 20}, 'q10-a': {22}, 'q10-complete': {22}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 5, 6, 28], '2': [6, 7, 8, 29], '3': [9, 10, 30], '4': [10, 11, 31], '5': [12, 13, 32], '6': [13, 14, 15, 33],
                '7': [16, 34], '8': [17, 18, 19, 20, 35], '9': [20, 21, 36], '10': [22, 23, 24, 37], '10-alt': [25, 26, 38]}
WORKED = [('q5-a', [12], ['0.04123', '0.07575', '0.13846', '3.00000', '0.078125', '3.655565', '0.273555']),
          ('q5-b', [12], ['492.39994', '3772168.08', '100.99', '96.96']),
          ('q5-c', [13], ['6.6666', '3.6555', '3.0111', '0.1114107'])]
RUBRIC = 'Question 1 and any four of the other nine questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
