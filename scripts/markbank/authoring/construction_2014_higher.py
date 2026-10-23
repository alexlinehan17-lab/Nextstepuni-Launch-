"""Source-pinned validator for the 2014 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q4(b), Q9(a) and Q10(a) any-two
cards and selection words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2014_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2014, 'higher'
HASHES = ('fa69de01573c5b7504ed8b2cc76ae930be5d815c85febcb1a7c2e7d03d68e2d1', '9673985bd87e5867668828d4f03244185b7cb75d0dbe70fa4f55ad819214608c')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 927
LEGACY = set()
UNNUMBERED = {'5'}  # printed "5 (a)" without a full stop
CHOICES = {'q4-b': ('areas', 2, 12, ['External random rubble wall', 'Traditional cut roof', 'Suspended timber ground floor']),
           'q9-a': ('items', 2, 12, ['Sound absorption', 'Sound reflection', 'Reverberation time']),
           'q10-a': ('items', 2, 10, ['Building form', 'Indoor air quality', 'Foundation Design'])}
FINITE = {'4b': 'q4-b', '9a': 'q9-a', '10a': 'q10-a'}
LEDGER = [(1, 'Answer Question'), (3, 'Select'), (3, 'any two'), (5, 'any two'), (5, 'any two'), (5, 'OR'), (5, 'or')]
LEAF = {
    'q1-a': [('details', 40, list(range(0, 41, 4))), ('presentation', 8, r(8)), ('dimensions', 3, r(3)), ('slates', 3, r(3)), ('ventilation', 3, r(3))],
    'q1-b': [('airtightness', 3, r(3))],
    'q2-a': [(k, 14, r(14)) for k in ['threshold', 'weather', 'lighting']] + [('dimensions', 6, r(6))],
    'q2-b': [(f'reason-{i}', 6, r(6)) for i in (1, 2)],
    'q3-a': [(f'requirement-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-b': [(f'requirement-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q3-c': [('design', 12, r(12))],
    'q4-a': [(k, 6, r(6)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q4-b': [('areas', 24, None), ('character', 6, r(6)), ('reuse', 6, r(6))],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 18, list(range(0, 19, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, r(3))],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [('note', 9, r(9)), ('sketch', 9, r(9))],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2)],
    'q6-c': [('discussion', 10, r(10))],
    'q7-a': [('details', 40, list(range(0, 41, 5))), ('dimensions', 3, r(3)), ('presentation', 9, r(9))],
    'q7-b': [('head', 4, r(4)), ('cill', 4, r(4))],
    'q8-a': [('sketch', 8, r(8)), ('items', 20, r(20))],
    'q8-b': [(k, 4, r(4)) for k in ['shower', 'basin', 'wc', 'svp', 'sizes']],
    'q8-c': [('consideration-1', 6, r(6)), ('consideration-2', 6, r(6))],
    'q9-a': [('items', 24, None)],
    'q9-b': [('floor', 8, r(8)), ('partition', 8, r(8)), ('materials', 4, r(4)), ('dimensions', 4, r(4))],
    'q9-c': [('principle-1', 6, r(6)), ('principle-2', 6, r(6))],
    'q10-a': [('items', 20, None)],
    'q10-b': [('notes', 7, r(7)), ('sketches', 7, r(7)), ('sun-path', 6, r(6))],
    'q10-c': [('reason-1', 4, r(4)), ('reason-2', 4, r(4)), ('detail-1', 6, r(6)), ('detail-2', 6, r(6))],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b'], 'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    'q4-complete': ['q4-a', 'q4-b'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 60 for k in COMPOSITE})
STUDY = (['cons-1-2'], ['planning-sustainability-environment'])
DRAIN = (['cons-5-6'], ['drainage'])
NEIGH = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-10', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q1-b': (['cons-6-5', 'cons-3-10'], ['condensation-air-tightness', 'roofs']),
    'q2-a': (['cons-1-2', 'cons-3-7'], ['planning-sustainability-environment', 'doors']), 'q2-b': STUDY,
    'q3-a': STUDY, 'q3-b': (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']), 'q3-c': STUDY,
    'q4-a': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q4-b': (['cons-1-1', 'cons-3-3', 'cons-3-9', 'cons-4-3', 'cons-6-2'], ['conservation-restoration', 'walls', 'roofs', 'floors', 'heat-loss-insulation']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'floors']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-6-4', 'cons-5-8'], ['sustainability-the-environment', 'services-water-gas-electricity']),
    'q6-c': (['cons-1-2'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-4'], ['question-1-drawing-questions', 'windows-light', 'walls']),
    'q7-b': (['cons-3-6', 'cons-3-4'], ['windows-light', 'walls']),
    'q8-a': (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']), 'q8-b': DRAIN,
    'q8-c': (['cons-5-6', 'cons-5-2'], ['drainage', 'services-water-gas-electricity']),
    'q9-a': (['cons-8-1', 'cons-8-2'], ['sound']), 'q9-b': (['cons-8-3', 'cons-4-3', 'cons-4-5'], ['sound', 'floors', 'doors']), 'q9-c': (['cons-8-3'], ['sound']),
    'q10-a': (['cons-6-2', 'cons-6-5', 'cons-2-4'], ['passive-design', 'foundations']), 'q10-b': (['cons-6-4'], ['passive-design']),
    'q10-c': (['cons-6-4', 'cons-6-5'], ['passive-design']),
    'q10-alt-discussion': NEIGH, 'q10-alt-guidelines': NEIGH,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 45, 580, 275], False), 'q2-original': (P, 2, [30, 277, 580, 505], False),
    'q3-original': (P, 2, [30, 505, 580, 790], False), 'q4-original': (P, 3, [30, 45, 580, 318], False),
    'q5-original': (P, 3, [30, 318, 580, 790], False), 'q6-original': (P, 4, [30, 45, 580, 310], False),
    'q7-original': (P, 4, [30, 310, 580, 545], False), 'q8-original': (P, 4, [30, 545, 580, 790], False),
    'q9-original': (P, 5, [30, 45, 580, 360], False), 'q10-original': (P, 5, [30, 360, 580, 575], False),
    'q10-alt-original': (P, 5, [30, 595, 580, 790], False),
    'q1-section': composite((4, [45, 50, 575, 800]), (5, [45, 50, 575, 462])),
    'q2-entrance': composite((5, [45, 462, 575, 795]), (6, [45, 50, 575, 222]), (6, [320, 222, 575, 298])),
    'q2-reasons': composite((6, [45, 222, 320, 307]), (6, [45, 307, 575, 405])),
    'q3-requirements': (S, 6, [45, 405, 575, 800], True), 'q3-layout': (S, 7, [45, 50, 575, 805], True), 'q3-external': (S, 8, [45, 50, 575, 478], True),
    'q4-step': (S, 8, [45, 478, 575, 800], True),
    'q4-upgrades': composite((9, [45, 50, 575, 800]), (10, [45, 50, 575, 800]), (11, [45, 50, 575, 800]), (12, [45, 50, 575, 800]), (13, [45, 50, 575, 790])),
    'q5-calculation': (S, 14, [45, 60, 575, 576], True), 'q5-cold-bridge': (S, 14, [45, 576, 575, 800], True),
    'q6-features': composite((15, [45, 50, 575, 800]), (16, [45, 50, 575, 535])),
    'q6-other': composite((16, [45, 535, 575, 800]), (17, [45, 50, 575, 560]), (18, [45, 50, 575, 612])),
    'q6-importance': (S, 18, [45, 612, 575, 790], True),
    'q7-section': (S, 19, [45, 50, 575, 790], True),
    'q8-layout': (S, 20, [45, 50, 575, 790], True),
    'q8-pipework': composite((21, [45, 50, 575, 330]), (21, [345, 330, 575, 450])),
    'q8-water': composite((21, [45, 330, 345, 470]), (21, [45, 470, 575, 795])),
    'q9-principles': composite((22, [45, 50, 575, 563]), (22, [45, 563, 360, 598])),
    'q9-upgrades': composite((22, [360, 563, 575, 598]), (22, [45, 598, 575, 790]), (23, [45, 50, 575, 334])),
    'q9-insulating': (S, 23, [45, 334, 575, 790], True),
    'q10-principles': composite((24, [45, 50, 575, 800]), (25, [45, 50, 575, 790])),
    'q10-orientation': (S, 26, [45, 50, 575, 286], True),
    'q10-overheating': composite((26, [45, 286, 575, 810]), (27, [45, 50, 575, 800])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-entrance', 'q2-b': 'q2-reasons', 'q2-complete': 'q2-entrance',
            'q3-a': 'q3-requirements', 'q3-b': 'q3-layout', 'q3-c': 'q3-external', 'q3-complete': 'q3-layout',
            'q4-a': 'q4-step', 'q4-b': 'q4-upgrades', 'q4-complete': 'q4-upgrades',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-cold-bridge', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-other', 'q6-c': 'q6-importance', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-layout', 'q8-b': 'q8-pipework', 'q8-c': 'q8-water', 'q8-complete': 'q8-pipework',
            'q9-a': 'q9-principles', 'q9-b': 'q9-upgrades', 'q9-c': 'q9-insulating', 'q9-complete': 'q9-upgrades',
            'q10-a': 'q10-principles', 'q10-b': 'q10-orientation', 'q10-c': 'q10-overheating', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q4-b': {9, 10, 11, 12, 13}, 'q4-complete': {9, 10, 11, 12, 13}, 'q9-a': {22}, 'q10-a': {24, 25}, 'q10-complete': {24, 25}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 5, 32], '2': [5, 6, 33], '3': [6, 7, 8, 34], '4': [8, 9, 10, 11, 12, 13, 35], '5': [14, 36], '6': [15, 16, 17, 18, 37],
                '7': [19, 38], '8': [20, 21, 39], '9': [22, 23, 40], '10': [24, 25, 26, 27, 41], '10-alt': [28, 29, 42]}
WORKED = [('q5-a', [14], ['0.7813', '6.4516', '0.0006', '0.1875', '0.1786', '7.70', '0.1298']),
          ('q5-b', [14], ['165.36', '3,276', '52.2', '49.59'])]
RUBRIC = 'Question 1 and any four of the other nine questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
