"""Source-pinned validator for the 2016 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card with its
seven pre-audit per-term IDs withdrawn into it, selection words, the 20 pre-audit cards corrected in place and
the retired build override), checked by the shared engine construction_paper.validate against the pinned SEC
paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2016_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2016, 'ordinary'
HASHES = ('1dae550c6c6e5a3dbb497bb66e319afd086086453929cfe829ba581c79f6b312', '167fd55b676b7b104721282db92dff78cedb79654ada944e5ea16a41dfc6f135')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 925
BAND8 = [0, 4, 6, 8]
Q8 = 'q8-None-lever-valve'
TERMS = ['Lever valve', 'Mortice and tenon joint', 'Cob wall', 'Thermal bridge', 'Dual flush toilet', 'Smart meter', 'Solar gain', 'Low-e glazing', 'Access ramp']
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-b', 'q3-a', 'q3-b', 'q3-c', 'q4-a', 'q4-b', 'q4-c', 'q5-a', 'q5-b', 'q6-a', 'q6-b', 'q7-a', 'q7-b', 'q7-c', 'q9-a', 'q9-c', Q8}
CONSOLIDATED = {f'q8-None-{t}': Q8 for t in ['mortice-and-tenon-joint', 'thermal-bridge', 'dual-flush-toilet', 'smart-meter', 'solar-gain', 'low-e-glazing', 'access-ramp']}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
LEDGER = [(1, 'Answer Question'), (3, 'any five')]
GAPS = {'q5-a': {'cons-4-4'}, 'q5-b': {'cons-4-4', 'cons-10-1'}, 'q7-c': {'cons-4-1'}, Q8: {'cons-10-1', 'cons-10-4'}}
RETIRED = [('card-source-bindings.json', 'q3-a')]
LEAF = {
    'q1-a': [('details', 36, list(range(0, 37, 4))), ('dimensions', 4, r(4))],
    'q1-b': [('thermal-bridge', 2, [0, 2]), ('presentation', 8, BAND8)],
    'q2-a': [('attic', 12, r(12)), ('tank', 12, r(12)), ('pipes', 8, r(8)), ('presentation', 8, BAND8)],
    'q2-b': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q3-a': [('items', 32, list(range(0, 33, 4))), ('presentation', 8, BAND8)],
    'q3-b': [('solar', 4, r(4))],
    'q3-c': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q4-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q4-b': [('site-layout-map', 15, r(15)), ('newspaper-notice', 15, r(15))],
    'q4-c': [('reason', 8, r(8))],
    'q5-a': [('details', 40, list(range(0, 41, 5)))],
    'q5-b': [('baluster', 2, [0, 2]), ('presentation', 8, BAND8)],
    'q6-a': [(k, 8, r(8)) for k in ['scalpel', 'chisel', 'adhesive']],
    'q6-b': [(f'precaution-{i}', 6, r(6)) for i in (1, 2, 3)] + [('presentation', 8, BAND8)],
    'q7-a': [('sketch', 12, r(12)), ('presentation', 8, BAND8), ('notes', 8, r(8))],
    'q7-b': [('detail', 4, r(4)), ('presentation', 8, BAND8)],
    'q7-c': [('detail-1', 5, r(5)), ('detail-2', 5, r(5))],
    Q8: [('terms', 50, None)],
    'q9-a': [('wood', 5, r(5)), ('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q9-b': [('finish', 4, r(4)), ('steps', 15, r(15)), ('presentation', 8, BAND8)],
    'q9-c': [('feature-1', 4, r(4)), ('feature-2', 4, r(4))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'ab'), ('3', 'abc'), ('4', 'abc'), ('5', 'ab'), ('6', 'ab'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
HEAT = (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'])
PLAN = (['cons-1-3'], ['planning-sustainability-environment'])
WORKSHOP = (['cons-9-4'], ['site-safety'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q1-b': (['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-a': (['cons-3-9', 'cons-6-2', 'cons-5-2'], ['roofs', 'heat-loss-insulation', 'hot-water-space-heating']),
    'q2-b': (['cons-6-3', 'cons-6-2'], ['heat-loss-insulation']),
    'q3-a': HEAT, 'q3-b': (['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'planning-sustainability-environment']),
    'q3-c': (['cons-6-4', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation']),
    'q4-a': PLAN, 'q4-b': PLAN, 'q4-c': PLAN,
    'q5-a': (['cons-1-5', 'cons-4-4'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q5-b': (['cons-4-4', 'cons-10-1'], ['foundations-floors-walls', 'wood-rot-ventilation']),
    'q6-a': WORKSHOP, 'q6-b': WORKSHOP,
    'q7-a': (['cons-4-5'], ['windows-doors']), 'q7-b': (['cons-8-3', 'cons-4-5'], ['sound', 'windows-doors']), 'q7-c': (['cons-4-1'], ['foundations-floors-walls']),
    Q8: (['cons-5-2', 'cons-10-1', 'cons-10-4', 'cons-3-3', 'cons-6-2', 'cons-5-8', 'cons-6-4', 'cons-3-6', 'cons-1-2'],
         ['services-water-gas-electrical', 'wood-rot-ventilation', 'foundations-floors-walls', 'heat-loss-insulation', 'planning-sustainability-environment', 'windows-doors']),
    'q9-a': (['cons-3-2', 'cons-10-7'], ['foundations-floors-walls', 'wood-rot-ventilation']), 'q9-b': (['cons-10-7'], ['wood-rot-ventilation']),
    'q9-c': (['cons-1-2', 'cons-6-4'], ['planning-sustainability-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 207], False), 'q2-original': (P, 2, [30, 210, 580, 370], False),
    'q3-original': (P, 2, [30, 375, 580, 610], False), 'q4-original': (P, 2, [30, 615, 580, 790], False),
    'q5-original': (P, 3, [30, 39, 580, 170], False), 'q6-original': (P, 3, [30, 172, 580, 328], False),
    'q7-original': (P, 3, [30, 330, 580, 528], False), 'q8-original': (P, 3, [30, 532, 580, 620], False),
    'q9-original': (P, 3, [30, 625, 580, 790], False),
    'q1-scheme': (S, 4, [25, 50, 580, 685], True),
    'q2-attic': (S, 5, [25, 50, 580, 484], True), 'q2-reasons': (S, 5, [25, 484, 580, 750], True),
    'q3-system': (S, 6, [25, 50, 580, 478], True), 'q3-solar': (S, 6, [25, 478, 580, 607], True), 'q3-advantages': (S, 6, [25, 607, 580, 770], True),
    'q4-reasons': (S, 7, [25, 50, 580, 320], True), 'q4-documents': (S, 7, [25, 320, 580, 652], True), 'q4-public': (S, 8, [25, 50, 580, 257], True),
    'q5-scheme': (S, 8, [25, 260, 580, 710], True),
    'q6-precautions': (S, 9, [25, 50, 580, 677], True), 'q6-lathe': (S, 10, [25, 50, 580, 560], True),
    'q7-partition': (S, 11, [25, 50, 580, 387], True), 'q7-sound': composite((11, [25, 387, 580, 710]), (12, [25, 30, 580, 288])),
    'q7-finish': (S, 12, [25, 288, 580, 497], True),
    'q8-terms': composite((12, [25, 497, 580, 710]), (13, [25, 50, 580, 776]), (14, [25, 50, 580, 710]), (15, [25, 50, 580, 509])),
    'q9-wood': composite((15, [25, 509, 580, 776]), (16, [25, 50, 580, 212])), 'q9-finish': (S, 16, [25, 212, 580, 547], True),
    'q9-eco': (S, 16, [25, 547, 580, 745], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-attic', 'q2-b': 'q2-reasons', 'q2-complete': 'q2-attic',
            'q3-a': 'q3-system', 'q3-b': 'q3-solar', 'q3-c': 'q3-advantages', 'q3-complete': 'q3-system',
            'q4-a': 'q4-reasons', 'q4-b': 'q4-documents', 'q4-c': 'q4-public', 'q4-complete': 'q4-documents',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-precautions', 'q6-b': 'q6-lathe', 'q6-complete': 'q6-lathe',
            'q7-a': 'q7-partition', 'q7-b': 'q7-sound', 'q7-c': 'q7-finish', 'q7-complete': 'q7-partition', Q8: 'q8-terms',
            'q9-a': 'q9-wood', 'q9-b': 'q9-finish', 'q9-c': 'q9-eco', 'q9-complete': 'q9-finish'}
CHOICE_FIGURE_PAGES = {Q8: {12, 13, 14, 15}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 2, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 8, 20], '5': [8, 21], '6': [9, 10, 22], '7': [11, 12, 23], '8': [12, 13, 14, 15, 24], '9': [15, 16, 25]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
