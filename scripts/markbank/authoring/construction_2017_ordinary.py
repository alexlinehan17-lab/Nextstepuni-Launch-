"""Source-pinned validator for the 2017 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card with its
eight per-term IDs withdrawn into it, selection words, the 19 pre-audit cards corrected in place and the
three retired build overrides), checked by the shared engine construction_paper.validate against the pinned
SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2017_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2017, 'ordinary'
HASHES = ('d3b27427c7d7cb63b783c6d94cefde26f5f5f692b8ff26a5d9d5b677b766a0e0', '0bd3312f2540c026eccd6a33c2b4a18eaaa690e9a5f305ed4762f2674ba8dda9')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 902
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
Q8 = 'q8-None-hand-rail'
TERMS = ['Hand rail', 'Box dovetail joint', 'Purlin', 'Damp-proof course', 'Ball valve', 'Energy rating', 'Wind turbine', 'Joist hanger', 'Service cavity']
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-b', 'q3-a', 'q3-b', 'q4-b', 'q5-a', 'q5-b', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q7-c', 'q9-a', 'q9-b', 'q9-c', Q8}
CONSOLIDATED = {f'q8-None-{t}': Q8 for t in ['box-dovetail-joint', 'purlin', 'damp-proof-course', 'ball-valve', 'energy-rating', 'wind-turbine',
                                            'joist-hanger', 'service-cavity']}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
LEDGER = [(1, 'Answer Question'), (4, 'any five'), (4, 'or')]
GAPS = {'q2-c': {'cons-4-1'}, Q8: {'cons-4-4', 'cons-10-1', 'cons-10-4'}}
RETIRED = [('card-source-bindings.json', 'q3-a'), ('card-corrections.json', 'q6-b'), ('card-corrections.json', 'q9-c')]
LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3))],
    'q1-b': [('dpc', 4, [0, 4]), ('presentation', 8, BAND8)],
    'q2-a': [('sketch', 10, r(10)), ('presentation', 8, BAND8), ('notes', 8, r(8)), ('type-thickness', 4, r(4))],
    'q2-b': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
    'q2-c': [('presentation', 8, BAND8)],
    'q3-a': [('items', 28, list(range(0, 29, 4))), ('presentation', 8, BAND8)],
    'q3-b': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q3-c': [('presentation', 6, BAND6)],
    'q4-a': [('sketch', 4, r(4)), ('presentation', 8, BAND8), ('detail-1', 6, r(6)), ('detail-2', 6, r(6))],
    'q4-b': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q4-c': [('use-1', 5, r(5)), ('use-2', 5, r(5)), ('reason-1', 3, r(3)), ('reason-2', 3, r(3))],
    'q5-a': [('details', 36, list(range(0, 37, 4))), ('dimensions', 3, r(3))],
    'q5-b': [('cold-bridge', 3, [0, 3]), ('presentation', 8, BAND8)],
    'q6-a': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q6-b': [(f'item-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-c': [('precaution-1', 5, r(5)), ('precaution-2', 5, r(5))],
    'q7-a': [('sketch', 4, r(4)), ('presentation', 8, BAND8), ('detail-1', 4, r(4)), ('detail-2', 4, r(4))],
    'q7-b': [('sketch', 4, r(4)), ('presentation', 8, BAND8), ('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q7-c': [('advantage', 4, r(4)), ('disadvantage', 4, r(4))],
    Q8: [('terms', 50, None)],
    'q9-a': [('sketch', 4, r(4)), ('presentation', 8, BAND8), ('detail-1', 4, r(4)), ('detail-2', 4, r(4))],
    'q9-b': [('finish', 4, r(4)), ('step-1', 4, r(4)), ('step-2', 4, r(4)), ('presentation', 8, BAND8)],
    'q9-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'abc'), ('3', 'abc'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
WASTE = (['cons-1-2', 'cons-1-8'], ['planning-sustainability-environment', 'site-safety'])
SAFE = (['cons-1-8'], ['site-safety'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-7', 'cons-3-4', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q1-b': (['cons-3-4', 'cons-3-7'], ['foundations-floors-walls', 'windows-doors']),
    'q2-a': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']), 'q2-c': (['cons-4-1'], ['foundations-floors-walls']),
    'q3-a': (['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'planning-sustainability-environment']),
    'q3-b': (['cons-6-4', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation']),
    'q3-c': (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']),
    'q4-a': WASTE, 'q4-b': WASTE, 'q4-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q5-a': (['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-4'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q5-b': (['cons-6-2', 'cons-3-6'], ['heat-loss-insulation', 'windows-doors']),
    'q6-a': SAFE, 'q6-b': SAFE, 'q6-c': (['cons-1-8', 'cons-9-4'], ['site-safety']),
    'q7-a': (['cons-4-3'], ['foundations-floors-walls']), 'q7-b': (['cons-4-3', 'cons-10-3'], ['foundations-floors-walls', 'wood-rot-ventilation']),
    'q7-c': (['cons-3-9', 'cons-1-2'], ['roofs', 'planning-sustainability-environment']),
    Q8: (['cons-4-4', 'cons-10-1', 'cons-10-4', 'cons-3-8', 'cons-3-4', 'cons-5-2', 'cons-6-3', 'cons-5-8', 'cons-1-2', 'cons-4-3', 'cons-3-3'],
         ['wood-rot-ventilation', 'roofs', 'foundations-floors-walls', 'services-water-gas-electrical', 'heat-loss-insulation', 'planning-sustainability-environment']),
    'q9-a': (['cons-10-3', 'cons-10-7'], ['wood-rot-ventilation']), 'q9-b': (['cons-10-7'], ['wood-rot-ventilation']),
    'q9-c': (['cons-1-2'], ['planning-sustainability-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 262], False), 'q2-original': (P, 2, [30, 268, 580, 470], False),
    'q3-original': (P, 2, [30, 488, 580, 770], False), 'q4-original': (P, 3, [30, 39, 580, 240], False),
    'q5-original': (P, 3, [30, 258, 580, 485], False), 'q6-original': (P, 3, [30, 505, 580, 700], False),
    'q7-original': (P, 4, [30, 39, 580, 255], False), 'q8-original': (P, 4, [30, 272, 580, 395], False),
    'q9-original': (P, 4, [30, 413, 580, 660], False),
    'q1-scheme': (S, 4, [25, 50, 580, 775], True),
    'q2-method': (S, 5, [25, 50, 580, 410], True), 'q2-advantages': (S, 5, [25, 410, 580, 608], True), 'q2-finish': (S, 5, [25, 608, 580, 775], True),
    'q3-system': (S, 6, [25, 50, 580, 440], True), 'q3-solar': (S, 6, [25, 440, 580, 606], True), 'q3-tap': (S, 6, [25, 606, 580, 775], True),
    'q4-sorting': (S, 7, [25, 50, 580, 436], True), 'q4-reasons': (S, 7, [25, 436, 580, 649], True),
    'q4-uses': composite((7, [25, 649, 580, 790]), (8, [25, 50, 580, 260])),
    'q5-scheme': (S, 8, [25, 270, 580, 775], True),
    'q6-signs': (S, 9, [25, 50, 580, 230], True), 'q6-ppe': (S, 9, [25, 230, 580, 785], True), 'q6-power-tools': (S, 10, [25, 50, 580, 265], True),
    'q7-joists': (S, 10, [25, 270, 580, 770], True), 'q7-joint': (S, 11, [25, 50, 580, 275], True), 'q7-attic': (S, 11, [25, 275, 580, 590], True),
    'q8-terms': composite((11, [25, 590, 580, 785]), (12, [25, 50, 580, 670]), (13, [25, 50, 580, 640]), (14, [25, 50, 580, 392])),
    'q9-decking': (S, 14, [25, 392, 580, 785], True), 'q9-finish': (S, 15, [25, 50, 580, 336], True), 'q9-patio': (S, 15, [25, 336, 580, 500], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-method', 'q2-b': 'q2-advantages', 'q2-c': 'q2-finish', 'q2-complete': 'q2-method',
            'q3-a': 'q3-system', 'q3-b': 'q3-solar', 'q3-c': 'q3-tap', 'q3-complete': 'q3-system',
            'q4-a': 'q4-sorting', 'q4-b': 'q4-reasons', 'q4-c': 'q4-uses', 'q4-complete': 'q4-sorting',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-ppe', 'q6-c': 'q6-power-tools', 'q6-complete': 'q6-ppe',
            'q7-a': 'q7-joists', 'q7-b': 'q7-joint', 'q7-c': 'q7-attic', 'q7-complete': 'q7-joists', Q8: 'q8-terms',
            'q9-a': 'q9-decking', 'q9-b': 'q9-finish', 'q9-c': 'q9-patio', 'q9-complete': 'q9-decking'}
CHOICE_FIGURE_PAGES = {Q8: {11, 12, 13, 14}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 17], '3': [6, 18], '4': [7, 8, 19], '5': [8, 20], '6': [9, 10, 21], '7': [10, 11, 22], '8': [11, 12, 13, 14, 23], '9': [14, 15, 24]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
