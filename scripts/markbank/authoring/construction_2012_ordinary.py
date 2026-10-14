"""Source-pinned validator for the 2012 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card and selection
words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2012_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2012, 'ordinary'
HASHES = ('d529d6c698018dc5277c9263c92682f5c6294239f37f59ac891caea7056238e3', '6e9157b363ec4060b91166a6ce6a623e211cf5e81847a41cd4cdcf5918f0bebe')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 1100
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
BAND4 = [0, 2, 3, 4]
Q8 = 'q8-terms'
TERMS = ['Rainwater butt', 'Box Dovetail Joint', 'Compression joint', 'Wall tie', 'Gully trap', 'Angle bead', 'Newel Post', 'Through and through sawing', 'Biscuit joint']
LEGACY = set()
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
LEDGER = [(1, 'Answer Question'), (3, 'any five')]
GAPS = {'q4-a': {'cons-2-5'}, Q8: {'cons-10-1', 'cons-10-4', 'cons-4-1', 'cons-4-4'}, 'q9-a': {'cons-10-1', 'cons-10-4'}}
LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 5, r(5))],
    'q1-b': [('closer', 4, r(4)), ('presentation', 6, BAND6)],
    'q2-a': [('description-1', 6, r(6)), ('description-2', 6, r(6)), ('finish', 6, r(6)), ('insulation', 6, r(6)), ('sketch', 16, r(16))],
    'q2-b': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q3-a': [('details', 30, list(range(0, 31, 5))), ('presentation', 8, BAND8)],
    'q3-b': [('frost', 6, r(6))],
    'q3-c': [('ways', 6, r(6))],
    'q4-a': [(k, 10, r(10)) for k in ['trench', 'level', 'reinforcement', 'position']],
    'q4-b': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 5, r(5))],
    'q5-b': [('cold-bridge', 4, r(4)), ('presentation', 6, BAND6)],
    'q6-a': [('lifting', 10, r(10)), ('concrete', 10, r(10))],
    'q6-b': [('item-1', 15, r(15)), ('item-2', 15, r(15))],
    'q7-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q7-b': [('map', 15, r(15)), ('notice', 15, r(15))],
    'q7-c': [('refusal', 8, r(8))],
    Q8: [('terms', 50, None)],
    'q9-a': [('name', 4, r(4)), ('suitability', 4, r(4)), ('presentation', 6, BAND6)],
    'q9-b': [('detail-1', 6, r(6)), ('detail-2', 6, r(6)), ('presentation', 4, BAND4)],
    'q9-c': [('finish', 4, r(4)), ('detail-1', 6, r(6)), ('detail-2', 6, r(6)), ('presentation', 4, BAND4)],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'ab'), ('3', 'abc'), ('4', 'ab'), ('5', 'ab'), ('6', 'ab'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
WATER = (['cons-5-1', 'cons-5-2'], ['services-water-gas-electrical'])
SITE = (['cons-1-8'], ['site-safety'])
PLAN = (['cons-1-3'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-9', 'cons-3-10', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls']),
    'q1-b': (['cons-3-10', 'cons-3-3'], ['roofs', 'foundations-floors-walls']),
    'q2-a': (['cons-6-2', 'cons-3-2'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-3', 'cons-6-2'], ['heat-loss-insulation']),
    'q3-a': WATER, 'q3-b': WATER, 'q3-c': (['cons-5-2', 'cons-1-2'], ['services-water-gas-electrical', 'planning-sustainability-environment']),
    'q4-a': (['cons-2-4', 'cons-2-5'], ['foundations-floors-walls']), 'q4-b': (['cons-2-4', 'cons-2-2'], ['foundations-floors-walls']),
    'q5-a': (['cons-1-5', 'cons-3-6', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q5-b': (['cons-6-2', 'cons-3-6'], ['heat-loss-insulation', 'windows-doors']),
    'q6-a': SITE, 'q6-b': SITE,
    'q7-a': PLAN, 'q7-b': PLAN, 'q7-c': PLAN,
    Q8: (['cons-5-4', 'cons-10-1', 'cons-10-4', 'cons-5-2', 'cons-3-3', 'cons-5-5', 'cons-4-1', 'cons-4-4', 'cons-10-3'],
         ['drainage', 'wood-rot-ventilation', 'services-water-gas-electrical', 'foundations-floors-walls']),
    'q9-a': (['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation']), 'q9-b': (['cons-10-7'], ['wood-rot-ventilation']),
    'q9-c': (['cons-10-7'], ['wood-rot-ventilation']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 197], False), 'q2-original': (P, 2, [30, 197, 580, 372], False),
    'q3-original': (P, 2, [30, 372, 580, 580], False), 'q4-original': (P, 2, [30, 580, 580, 790], False),
    'q5-original': (P, 3, [30, 39, 580, 191], False), 'q6-original': (P, 3, [30, 191, 580, 313], False),
    'q7-original': (P, 3, [30, 313, 580, 509], False), 'q8-original': (P, 3, [30, 509, 580, 601], False),
    'q9-original': (P, 3, [30, 601, 580, 790], False),
    'q1-section': (S, 4, [18, 50, 580, 622], True), 'q1-closer': (S, 4, [18, 622, 580, 777], True),
    'q2-method': (S, 5, [25, 50, 580, 564], True), 'q2-advantages': (S, 5, [25, 564, 580, 777], True),
    'q3-system': (S, 6, [25, 50, 580, 322], True), 'q3-frost': (S, 6, [25, 322, 580, 408], True), 'q3-saving': (S, 6, [25, 408, 580, 563], True),
    'q4-design': composite((6, [25, 563, 580, 777]), (7, [25, 60, 580, 540])), 'q4-reasons': (S, 7, [25, 540, 580, 777], True),
    'q5-scheme': (S, 8, [25, 46, 580, 436], True),
    'q6-precautions': composite((8, [25, 436, 580, 777]), (9, [25, 50, 580, 252])), 'q6-ppe': (S, 9, [25, 252, 580, 777], True),
    'q7-reasons': (S, 10, [25, 50, 580, 207], True), 'q7-documents': (S, 10, [25, 207, 580, 565], True), 'q7-refusal': (S, 10, [25, 565, 580, 777], True),
    'q8-terms': composite((11, [25, 50, 580, 777]), (12, [25, 50, 580, 777]), (13, [25, 50, 580, 120])),
    'q9-joint': (S, 13, [25, 120, 580, 505], True), 'q9-restore': (S, 13, [25, 505, 580, 777], True), 'q9-finish': (S, 14, [25, 50, 580, 560], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-closer', 'q1-complete': 'q1-section',
            'q2-a': 'q2-method', 'q2-b': 'q2-advantages', 'q2-complete': 'q2-method',
            'q3-a': 'q3-system', 'q3-b': 'q3-frost', 'q3-c': 'q3-saving', 'q3-complete': 'q3-system',
            'q4-a': 'q4-design', 'q4-b': 'q4-reasons', 'q4-complete': 'q4-design',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-precautions', 'q6-b': 'q6-ppe', 'q6-complete': 'q6-precautions',
            'q7-a': 'q7-reasons', 'q7-b': 'q7-documents', 'q7-c': 'q7-refusal', 'q7-complete': 'q7-documents', Q8: 'q8-terms',
            'q9-a': 'q9-joint', 'q9-b': 'q9-restore', 'q9-c': 'q9-finish', 'q9-complete': 'q9-restore'}
CHOICE_FIGURE_PAGES = {Q8: {11, 12, 13}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 2, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
SCHEME_PAGES = {'1': [4, 15], '2': [5, 16], '3': [6, 17], '4': [6, 7, 18], '5': [8, 19], '6': [8, 9, 20], '7': [10, 21], '8': [11, 12, 13, 22], '9': [13, 14, 23]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
