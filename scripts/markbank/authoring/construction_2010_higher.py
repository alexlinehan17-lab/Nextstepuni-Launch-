"""Source-pinned validator for the 2010 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q10(a) any-two card and selection
words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2010_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2010, 'higher'
HASHES = ('c4651a6996cf20f3efda5b3c754337f4c57bd4d9155a49d79a3cb6176fd51ccb', '43dbe433ff008b0ebea913028b365e78e93bf3eaaff3eee5858bc089190070e0')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 1194
LEGACY = set()
CHOICES = {'q10-a': ('items', 2, 8, ['Shape and Form', 'Continuity of Insulation', 'Reduced cold bridge'])}
FINITE = {'10a': 'q10-a'}
LEDGER = [(1, 'Answer Question'), (2, 'select'), (2, 'any two'), (2, 'either'), (2, 'or'), (4, 'or'), (4, 'any other'), (5, 'any two'), (5, 'OR')]
LEAF = {
    'q1-a': [('details', 48, list(range(0, 49, 4))), ('dimensions', 4, r(4)), ('presentation', 4, r(4))],
    'q1-b': [('closure', 4, r(4))],
    'q2-a': [('detail-1', 16, r(16)), ('detail-2', 16, r(16))],
    'q2-b': [('area-1', 14, r(14)), ('area-2', 14, r(14))],
    'q3-a': [('internal', 24, r(24)), ('external', 24, r(24))],
    'q3-b': [('internal-advantages', 4, r(4)), ('external-advantages', 4, r(4)), ('recommendation', 4, r(4))],
    'q4-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q4-b': [('note', 8, r(8)), ('sketch', 8, r(8)), ('dimensions', 8, r(8))],
    'q4-c': [('test', 12, r(12))],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 15, list(range(0, 16, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 6, r(6)), ('units', 3, r(3))],
    'q5-b': [('formula', 3, r(3)), ('existing', 3, r(3)), ('required', 3, r(3)), ('difference', 3, r(3)), ('thickness', 9, r(9))],
    'q5-c': [('mass', 9, r(9))],
    'q6-a': [(f'feature-{i}', 16, r(16)) for i in (1, 2, 3)],
    'q6-b': [(k, 4, r(4)) for k in ['renewable', 'durable', 'local']],
    'q7-a': [('details', 30, list(range(0, 31, 5))), ('presentation', 4, r(4)), ('stairs-handrail', 2, r(2)), ('landing-handrail', 2, r(2)), ('balusters', 2, r(2))],
    'q7-b': [('feature-1', 10, r(10)), ('feature-2', 10, r(10))],
    'q8-a': [('formula', 4, r(4)), ('floor-area', 2, r(2)), ('product', 2, r(2)), ('solve', 4, r(4)), ('window-area', 2, r(2))],
    'q8-b': [(k, 8, r(8)) for k in ['frame-1', 'frame-2', 'glazing-1', 'glazing-2']],
    'q8-c': [('consideration-1', 7, r(7)), ('consideration-2', 7, r(7))],
    'q9-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q9-b': [('leakage-1', 5, r(5)), ('detail-1', 4, r(4)), ('leakage-2', 5, r(5)), ('detail-2', 4, r(4)), ('materials', 2, r(2))],
    'q9-c': [('advantage-1', 8, r(8)), ('advantage-2', 8, r(8))],
    'q10-a': [('items', 16, None)],
    'q10-b': [('principle-1', 8, r(8)), ('principle-2', 8, r(8)), ('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q10-c': [('detail-1', 10, r(10)), ('detail-2', 10, r(10))],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b'], 'q3-complete': ['q3-a', 'q3-b'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 60 for k in COMPOSITE})
ACCESS = (['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'doors'])
INSUL = (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'walls'])
DRAIN = (['cons-5-5'], ['drainage'])
AIR = (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness'])
URBAN = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-6', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'windows-light', 'walls']),
    'q1-b': (['cons-3-3', 'cons-3-10'], ['walls', 'roofs']),
    'q2-a': ACCESS, 'q2-b': ACCESS, 'q3-a': INSUL, 'q3-b': INSUL,
    'q4-a': DRAIN, 'q4-b': DRAIN, 'q4-c': DRAIN,
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q5-c': (['cons-6-4', 'cons-6-2'], ['passive-design', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-4-4', 'cons-4-3'], ['question-1-drawing-questions', 'stairs', 'floors']),
    'q7-b': (['cons-4-4'], ['stairs']),
    'q8-a': (['cons-7-2', 'cons-3-5'], ['windows-light']),
    'q8-b': (['cons-3-6', 'cons-6-2'], ['windows-light', 'heat-loss-insulation']),
    'q8-c': (['cons-3-5', 'cons-1-2'], ['windows-light', 'sustainability-the-environment']),
    'q9-a': (['cons-3-8', 'cons-1-9', 'cons-6-2'], ['roofs', 'fireplaces-fire-prevention', 'heat-loss-insulation']),
    'q9-b': AIR, 'q9-c': AIR,
    'q10-a': (['cons-6-2', 'cons-6-4'], ['passive-design', 'heat-loss-insulation']),
    'q10-b': (['cons-6-5'], ['passive-design', 'condensation-air-tightness']),
    'q10-c': (['cons-6-4', 'cons-6-5'], ['passive-design']),
    'q10-alt-discussion': URBAN, 'q10-alt-guidelines': URBAN,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 50, 580, 304], False), 'q2-original': (P, 2, [30, 304, 580, 537], False),
    'q3-original': (P, 2, [30, 537, 580, 790], False), 'q4-original': (P, 3, [30, 50, 580, 251], False),
    'q5-original': (P, 3, [30, 251, 580, 534], False), 'q6-original': (P, 3, [30, 534, 580, 790], False),
    'q7-original': (P, 4, [30, 50, 580, 266], False), 'q8-original': (P, 4, [30, 266, 580, 479], False),
    'q9-original': (P, 4, [30, 479, 580, 790], False), 'q10-original': (P, 5, [30, 50, 580, 311], False),
    'q10-alt-original': (P, 5, [30, 330, 580, 790], False),
    'q1-section': (S, 4, [40, 60, 585, 784], True),
    'q2-entrance': (S, 5, [40, 60, 585, 324], True),
    'q2-areas': composite((5, [40, 324, 585, 784]), (6, [40, 60, 585, 130])),
    'q3-systems': composite((6, [40, 130, 585, 786]), (7, [40, 60, 585, 784]), (8, [40, 60, 585, 209.5])),
    'q3-advantages': (S, 8, [40, 209.5, 585, 784], True),
    'q4-requirements': (S, 9, [40, 60, 585, 438], True), 'q4-manhole': (S, 9, [40, 438, 585, 725], True),
    'q4-test': composite((9, [40, 725, 585, 786]), (10, [40, 60, 585, 310])),
    'q5-calculation': composite((10, [40, 310, 585, 784]), (11, [40, 60, 585, 320])),
    'q5-mass': composite((11, [40, 320, 585, 784]), (12, [40, 60, 585, 452])),
    'q6-features': composite((12, [40, 452, 585, 784]), (13, [40, 60, 585, 228])), 'q6-materials': (S, 13, [40, 228, 585, 784], True),
    'q7-scheme': composite((14, [40, 60, 585, 784]), (15, [40, 60, 585, 290])),
    'q8-calculation': (S, 15, [40, 300, 585, 784], True), 'q8-window': (S, 16, [40, 60, 585, 554], True),
    'q8-environment': (S, 16, [40, 554, 585, 784], True),
    'q9-requirements': (S, 17, [40, 60, 585, 524], True), 'q9-leakage': composite((17, [40, 524, 585, 784]), (18, [40, 60, 585, 158])),
    'q9-advantages': (S, 18, [40, 158, 585, 431], True),
    'q10-principles': composite((18, [40, 431, 585, 784]), (19, [40, 60, 585, 187])),
    'q10-mhrv': (S, 19, [40, 187, 585, 784], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-entrance', 'q2-b': 'q2-areas', 'q2-complete': 'q2-entrance',
            'q3-a': 'q3-systems', 'q3-b': 'q3-advantages', 'q3-complete': 'q3-systems',
            'q4-a': 'q4-requirements', 'q4-b': 'q4-manhole', 'q4-c': 'q4-test', 'q4-complete': 'q4-manhole',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-mass', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-materials', 'q6-complete': 'q6-features',
            'q7-a': 'q7-scheme', 'q7-b': 'q7-scheme', 'q7-complete': 'q7-scheme',
            'q8-a': 'q8-calculation', 'q8-b': 'q8-window', 'q8-c': 'q8-environment', 'q8-complete': 'q8-window',
            'q9-a': 'q9-requirements', 'q9-b': 'q9-leakage', 'q9-c': 'q9-advantages', 'q9-complete': 'q9-leakage',
            'q10-a': 'q10-principles', 'q10-b': 'q10-mhrv', 'q10-c': 'q10-mhrv', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q10-a': {18, 19}, 'q10-complete': {18, 19}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 24], '2': [5, 6, 25], '3': [6, 7, 8, 26], '4': [9, 10, 27], '5': [10, 11, 12, 28], '6': [12, 13, 29],
                '7': [14, 15, 30], '8': [15, 16, 31], '9': [17, 18, 32], '10': [18, 19, 33], '10-alt': [20, 21, 34]}
WORKED = [('q5-a', [10], ['0.03472', '0.26775', '0.08125', '0.55372', '1.805']),
          ('q5-b', [10, 11], ['3.703', '3.15', '0.07875', '78.75']),
          ('q8-a', [15], ['19.0', '1,000', '2850', '2.85'])]
RUBRIC = 'Question 1 and four other questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
