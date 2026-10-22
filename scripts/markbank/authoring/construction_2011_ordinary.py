"""Source-pinned validator for the 2011 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card, Q7(b) marked
alike for either appliance, and selection words; the paper was never carded, so every task is added), checked by
the shared engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2011_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2011, 'ordinary'
HASHES = ('d02ee1cffc9d9c404ca6299e98001f373fba97977988b9b1b0f46150bc81d304', '2ab53d9280c298352ee2d11cce327a37d5b1c9e08ddd0f33cd3243d29fd2fd7b')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 1166
BAND4 = [0, 2, 3, 4]
BAND5 = [0, 3, 4, 5]
BAND3 = [0, 1, 2, 3]
Q8 = 'q8-terms'
TERMS = ['Fascia', 'Strip foundation', 'Thermostatic valve', 'Window board', 'Butt hinge', 'Rafter', 'Solar panel', 'Wall tie', 'Radon barrier']
LEGACY = set()
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
MARKED_ALIKE = {'7b': dict(options=['toilet', 'washing machine'], cardId='cons-2011-ol-q7-b')}
LEDGER = [(1, 'Answer Question'), (3, 'one of'), (3, 'any five')]
GAPS = {'q4-a': {'cons-10-2'}, 'q5-a': {'cons-4-4', 'cons-10-1'}, 'q5-b': {'cons-4-4', 'cons-10-1'}, 'q9-b': {'cons-10-1', 'cons-10-4'}}
LEAF = {
    'q1-a': [('details', 42, list(range(0, 43, 6)))],
    'q1-b': [('flashing', 4, r(4)), ('presentation', 4, BAND4)],
    'q2-a': [(k, 10, r(10)) for k in ['cavity-notes', 'cavity-sketch', 'internal-notes', 'internal-sketch']],
    'q2-b': [('cavity', 5, r(5)), ('internal', 5, r(5))],
    'q3-a': [('details', 35, list(range(0, 36, 5))), ('presentation', 6, r(6))],
    'q3-b': [('advantage-1', 5, r(5)), ('advantage-2', 4, r(4))],
    'q4-a': [('description-1', 4, r(4)), ('description-2', 4, r(4)), ('presentation', 6, r(6)), ('detail', 4, r(4))],
    'q4-b': [('description-1', 4, r(4)), ('description-2', 4, r(4)), ('sketch', 10, r(10)), ('wood', 2, r(2)), ('reasons', 4, r(4))],
    'q4-c': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('sizes', 5, r(5))],
    'q5-b': [('detail', 4, r(4)), ('presentation', 6, r(6))],
    'q6-a': [('cill', 15, r(15)), ('height', 15, r(15))],
    'q6-b': [('precaution-1', 5, r(5)), ('precaution-2', 5, r(5)), ('reasons', 5, r(5)), ('presentation', 5, BAND5)],
    'q7-a': [('detail-1', 5, r(5)), ('detail-2', 5, r(5)), ('sketch', 15, list(range(0, 16, 5))), ('presentation', 6, r(6))],
    'q7-b': [('note', 5, r(5)), ('presentation', 6, r(6)), ('annotation', 4, r(4))],
    'q7-c': [('reason', 4, r(4))],
    Q8: [('terms', 50, None)],
    'q9-a': [('feature', 5, r(5)), ('presentation', 6, r(6)), ('details', 4, r(4))],
    'q9-b': [('joint', 5, r(5)), ('presentation', 6, r(6)), ('details', 4, r(4))],
    'q9-c': [('finish', 5, r(5)), ('detail-1', 6, r(6)), ('detail-2', 6, r(6)), ('presentation', 3, BAND3)],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'ab'), ('3', 'ab'), ('4', 'abc'), ('5', 'ab'), ('6', 'ab'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
WATER = (['cons-5-2'], ['hot-water-space-heating', 'services-water-gas-electrical'])
STAIRS = (['cons-4-4', 'cons-10-1'], ['foundations-floors-walls', 'wood-rot-ventilation'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-6', 'cons-3-4', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q1-b': (['cons-3-4', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation']),
    'q2-a': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q3-a': WATER, 'q3-b': (['cons-5-2', 'cons-5-8'], ['hot-water-space-heating', 'services-water-gas-electrical']),
    'q4-a': (['cons-10-2'], ['wood-rot-ventilation']),
    'q4-b': (['cons-4-2', 'cons-10-7'], ['foundations-floors-walls', 'wood-rot-ventilation']),
    'q4-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q5-a': STAIRS, 'q5-b': STAIRS,
    'q6-a': (['cons-1-8'], ['site-safety']), 'q6-b': (['cons-9-4'], ['site-safety']),
    'q7-a': (['cons-5-4', 'cons-5-2'], ['drainage', 'services-water-gas-electrical']),
    'q7-b': (['cons-5-2', 'cons-5-6'], ['services-water-gas-electrical', 'drainage']),
    'q7-c': (['cons-5-2', 'cons-1-2'], ['services-water-gas-electrical', 'planning-sustainability-environment']),
    Q8: (['cons-3-10', 'cons-2-4', 'cons-5-3', 'cons-3-6', 'cons-3-7', 'cons-3-8', 'cons-6-4', 'cons-3-3', 'cons-3-4', 'cons-4-2'],
         ['roofs', 'foundations-floors-walls', 'hot-water-space-heating', 'services-water-gas-electrical', 'windows-doors', 'planning-sustainability-environment']),
    'q9-a': (['cons-10-7'], ['wood-rot-ventilation']), 'q9-b': (['cons-10-1', 'cons-10-4'], ['wood-rot-ventilation']),
    'q9-c': (['cons-10-7'], ['wood-rot-ventilation']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 208], False), 'q2-original': (P, 2, [30, 208, 580, 407], False),
    'q3-original': (P, 2, [30, 407, 580, 592], False), 'q4-original': (P, 2, [30, 592, 580, 790], False),
    'q5-original': (P, 3, [30, 39, 580, 170], False), 'q6-original': (P, 3, [30, 170, 580, 284], False),
    'q7-original': (P, 3, [30, 284, 580, 498], False), 'q8-original': (P, 3, [30, 498, 580, 593], False),
    'q9-original': (P, 3, [30, 593, 580, 790], False),
    'q1-section': (S, 4, [25, 45, 580, 778], True),
    'q2-systems': (S, 5, [25, 45, 580, 575], True), 'q2-pros-cons': composite((5, [25, 575, 580, 778]), (6, [25, 45, 580, 384])),
    'q3-system': (S, 6, [25, 384, 580, 778], True), 'q3-shower': (S, 7, [25, 45, 580, 252], True),
    'q4-cabinets': (S, 7, [25, 252, 580, 778], True), 'q4-floor': (S, 8, [25, 45, 580, 710], True), 'q4-layout': (S, 9, [25, 45, 580, 194], True),
    'q5-scheme': (S, 9, [25, 194, 580, 778], True),
    'q6-precautions': (S, 10, [25, 45, 580, 435], True), 'q6-lathe': (S, 10, [25, 435, 580, 778], True),
    'q7-pump': (S, 11, [25, 45, 580, 441.5], True), 'q7-appliance': (S, 11, [25, 441.5, 580, 640], True), 'q7-reason': (S, 11, [25, 640, 580, 778], True),
    'q8-terms': composite((12, [25, 60, 580, 778]), (13, [25, 45, 580, 778])),
    'q9-feature': (S, 14, [25, 45, 580, 265], True), 'q9-joint': (S, 14, [25, 265, 580, 410], True),
    'q9-finish': composite((14, [25, 410, 580, 778]), (15, [25, 60, 580, 250])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-systems', 'q2-b': 'q2-pros-cons', 'q2-complete': 'q2-systems',
            'q3-a': 'q3-system', 'q3-b': 'q3-shower', 'q3-complete': 'q3-system',
            'q4-a': 'q4-cabinets', 'q4-b': 'q4-floor', 'q4-c': 'q4-layout', 'q4-complete': 'q4-floor',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-precautions', 'q6-b': 'q6-lathe', 'q6-complete': 'q6-precautions',
            'q7-a': 'q7-pump', 'q7-b': 'q7-appliance', 'q7-c': 'q7-reason', 'q7-complete': 'q7-pump', Q8: 'q8-terms',
            'q9-a': 'q9-feature', 'q9-b': 'q9-joint', 'q9-c': 'q9-finish', 'q9-complete': 'q9-joint'}
CHOICE_FIGURE_PAGES = {Q8: {12, 13}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 2, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
SCHEME_PAGES = {'1': [4, 16], '2': [5, 6, 17], '3': [6, 7, 18], '4': [7, 8, 9, 19], '5': [9, 20], '6': [10, 21], '7': [11, 22], '8': [12, 13, 23], '9': [14, 15, 24]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
