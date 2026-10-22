"""Source-pinned validator for the 2019 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q4(b) any-two card, selection
words, the 21 pre-audit cards corrected in place and the four retired build overrides), checked by the shared
engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2019_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2019, 'higher'
HASHES = ('45bad0b8a8a9d02b29f856805aa37e3385709cbfe458661f79a3104fbe769ea0', '8b5abe8e2e0ba5d4d19c280bbdce76fde932a941cd07205edd9bb0a8c71c3edc')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 829
BAND8 = [0, 4, 6, 8]
LEGACY = {'q1-b', 'q2-a', 'q2-c', 'q3-a', 'q3-b', 'q4-a', 'q5-a', 'q5-b', 'q5-c', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q8-a', 'q8-b', 'q8-c',
          'q9-b', 'q10-a', 'q10-b', 'q10-c'}
AREAS = ['Traditional cut roof with natural slates', 'Softwood sliding sash windows with single - glazing',
         'Solid external walls of brick construction, uninsulated and with internal lime render']
CHOICES = {'q4-b': ('areas', 2, 18, AREAS)}
FINITE = {'4b': 'q4-b'}
RETIRED = [('card-source-bindings.json', 'q2-c'), ('card-source-bindings.json', 'q8-b'), ('card-corrections.json', 'q8-c'), ('card-corrections.json', 'q10-b')]
LEDGER = [(1, 'Answer Question'), (2, 'Select'), (3, 'one of'), (3, 'one of'), (3, 'Select'), (3, 'any two'), (7, 'OR'), (7, 'One of'), (7, 'or')]
LEAF = {
    'q1-a': [('details', 48, r(48)), ('presentation', 8, BAND8)],
    'q1-b': [('cill', 4, r(4))],
    'q2-a': [(f'requirement-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q2-b': [(f'profile-{i}', 8, r(8)) for i in (1, 2, 3)] + [('recommendation', 3, r(3)), ('justification', 3, r(3))],
    'q2-c': [(f'material-{i}', 4, r(4)) for i in (1, 2, 3)],
    'q3-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-b': [('layout', 14, r(14))] + [(f'consideration-{i}', 3, r(3)) for i in (1, 2, 3)] + [('justification', 3, r(3))],
    'q3-c': [('notes', 4, r(4)), ('sketches', 12, r(12))],
    'q4-a': [(f'benefit-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q4-b': [('areas', 36, None)],
    'q5-a': [('resistances', 24, list(range(0, 25, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [(k, 3, r(3)) for k in ['required-resistance', 'existing-resistance', 'difference', 'formula', 'thickness']],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(k, 6, r(6)) for k in ['evacuated-tubes', 'wind-turbines', 'photovoltaic-panels']],
    'q6-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q7-a': [('details', 40, r(40)), ('dimensions', 6, r(6)), ('presentation', 8, BAND8)],
    'q7-b': [('safety', 6, r(6))],
    'q8-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q8-b': [('notes', 10, r(10)), ('sketch', 10, r(10)), ('dimensions', 6, r(6))],
    'q8-c': [('notes', 8, r(8)), ('sketch', 8, r(8))],
    'q9-a': [(k, 16, r(16)) for k in ['wallplate', 'door-head', 'threshold']],
    'q9-b': [(f'impact-{i}', 6, r(6)) for i in (1, 2)],
    'q10-a': [(f'consideration-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q10-b': [(f'upgrade-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q10-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    'q4-complete': ['q4-a', 'q4-b'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 60 for k in COMPOSITE})
ROOF = (['cons-3-8', 'cons-3-9'], ['roofs'])
EXT = (['cons-1-2', 'cons-5-6'], ['planning-sustainability-environment', 'drainage'])
CALC = (['cons-6-1'], ['heat-u-value-calculations'])
STAIRS = (['cons-4-4'], ['stairs'])
DRAIN = (['cons-5-5'], ['drainage'])
ENERPHIT = (['cons-6-2', 'cons-6-5', 'cons-6-4'], ['passive-design'])
GREEN = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-2'], ['question-1-drawing-questions', 'windows-light', 'walls']),
    'q1-b': (['cons-3-6', 'cons-3-4'], ['windows-light', 'walls']),
    'q2-a': ROOF, 'q2-b': (['cons-3-8', 'cons-1-2'], ['roofs', 'planning-sustainability-environment']), 'q2-c': (['cons-3-9'], ['roofs']),
    'q3-a': EXT, 'q3-b': EXT, 'q3-c': (['cons-1-2', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration']),
    'q4-a': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q4-b': (['cons-1-1', 'cons-3-9', 'cons-3-5', 'cons-3-3', 'cons-6-2'], ['conservation-restoration', 'roofs', 'windows-light', 'walls', 'heat-loss-insulation']),
    'q5-a': CALC, 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-5-3', 'cons-5-8', 'cons-6-4'], ['services-water-gas-electricity', 'sustainability-the-environment']),
    'q6-c': (['cons-1-1', 'cons-1-2'], ['conservation-restoration', 'sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-4-4', 'cons-10-1'], ['question-1-drawing-questions', 'stairs']), 'q7-b': STAIRS,
    'q8-a': (['cons-5-5', 'cons-1-3'], ['drainage', 'planning-sustainability-environment']), 'q8-b': DRAIN, 'q8-c': DRAIN,
    'q9-a': (['cons-6-2', 'cons-3-10', 'cons-3-7', 'cons-4-2'], ['heat-loss-insulation', 'roofs', 'doors', 'floors']),
    'q9-b': (['cons-6-2', 'cons-6-6'], ['heat-loss-insulation', 'condensation-air-tightness']),
    'q10-a': ENERPHIT, 'q10-b': ENERPHIT, 'q10-c': (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment']),
    'q10-alt-discussion': GREEN, 'q10-alt-guidelines': GREEN,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 430], False), 'q2-original': (P, 2, [45, 430, 580, 750], False),
    'q3-original': (P, 3, [45, 53, 580, 440], False), 'q4-original': (P, 3, [45, 440, 580, 760], False),
    'q5-original': (P, 4, [45, 53, 580, 760], False), 'q6-original': (P, 5, [45, 53, 580, 470], False),
    'q7-original': (P, 5, [45, 475, 580, 730], False), 'q8-original': (P, 6, [45, 53, 580, 415], False),
    'q9-original': (P, 6, [45, 415, 580, 760], False), 'q10-original': (P, 7, [45, 53, 580, 425], False),
    'q10-alt-original': (P, 7, [45, 495, 580, 715], False),
    'q1-section': composite((4, [45, 50, 575, 790]), (5, [45, 50, 575, 310])),
    'q1-cill': (S, 5, [45, 50, 575, 310], True),
    'q2-profiles': (S, 6, [45, 50, 575, 530], True),
    'q3-layout': composite((8, [45, 235, 575, 770]), (9, [45, 50, 575, 330])),
    'q3-external': composite((9, [45, 360, 575, 745]), (10, [45, 50, 575, 790])),
    'q4-upgrades': composite((11, [45, 250, 575, 770]), (12, [45, 50, 575, 790]), (13, [45, 50, 575, 790]), (14, [45, 50, 575, 790]), (15, [45, 50, 575, 475])),
    'q5-calculation': (S, 16, [45, 50, 575, 780], True), 'q5-thickness': (S, 17, [45, 50, 575, 285], True),
    'q6-features': (S, 17, [45, 290, 575, 790], True),
    'q6-renewables': composite((18, [45, 50, 575, 740]), (19, [45, 50, 575, 670]), (20, [45, 50, 575, 395])),
    'q7-section': (S, 21, [45, 50, 575, 770], True),
    'q8-layout': (S, 22, [45, 345, 575, 775], True), 'q8-alternative': (S, 23, [45, 75, 575, 790], True),
    'q9-details': (S, 24, [45, 50, 575, 790], True),
    'q10-retrofit': composite((26, [45, 50, 575, 780]), (27, [45, 50, 575, 510])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-cill', 'q1-complete': 'q1-section',
            'q2-b': 'q2-profiles', 'q2-complete': 'q2-profiles', 'q3-b': 'q3-layout', 'q3-c': 'q3-external', 'q3-complete': 'q3-layout',
            'q4-b': 'q4-upgrades', 'q4-complete': 'q4-upgrades',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-thickness', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-renewables', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-b': 'q8-layout', 'q8-c': 'q8-alternative', 'q8-complete': 'q8-layout',
            'q9-a': 'q9-details', 'q9-complete': 'q9-details', 'q10-b': 'q10-retrofit', 'q10-complete': 'q10-retrofit'}
CHOICE_FIGURE_PAGES = {'q4-b': {11, 12, 13, 14, 15}, 'q4-complete': {11, 12, 13, 14, 15}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}
SCHEME_PAGES = {'1': [4, 5, 32], '2': [5, 6, 33], '3': [7, 8, 9, 10, 34], '4': [11, 12, 13, 14, 15, 35], '5': [16, 17, 36], '6': [17, 18, 19, 20, 37],
                '7': [21, 38], '8': [22, 23, 39], '9': [24, 25, 40], '10': [25, 26, 27, 41], '10-alt': [28, 29, 42]}
WORKED = [('q5-a', [16], ['0.035', '0.069', '1.351', '0.075', '1.939', '0.516']),
          ('q5-b', [16], ['975.24', '8,164,800', '212.34', '199.60']),
          ('q5-c', [17], ['6.666', '4.727', '0.146537'])]
RUBRIC = 'Question 1 and any four of the other nine questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
