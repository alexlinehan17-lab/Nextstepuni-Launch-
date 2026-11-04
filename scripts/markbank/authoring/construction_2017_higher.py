"""Source-pinned validator for the 2017 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q4(b) and Q10(a) any-two
cards, selection words, the 25 pre-audit cards corrected in place and the thirteen retired build overrides),
checked by the shared engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2017_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2017, 'higher'
HASHES = ('3751ae5b7139751f60b07b1c367487cabe10aa77c7953d60b762787498cf8804', '822396a75a761c0401757fdb5b6a7334fd49f049525c844b7b9437d8df9e299c')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 886
BAND8 = [0, 4, 6, 8]
LEGACY = {'q1-b', 'q2-a', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q3-c', 'q4-a', 'q4-b', 'q4-c', 'q5-b', 'q5-c', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b',
          'q8-a', 'q8-b', 'q8-c', 'q9-a', 'q9-c', 'q10-a', 'q10-b', 'q10-c'}
CHOICES = {'q4-b': ('walls', 2, 12, ['Concrete block construction', 'Timber frame construction', 'Timber frame and hemp-lime construction']),
           'q10-a': ('items', 2, 12, ['Airtightness', 'Indoor air quality', 'Solar shading'])}
FINITE = {'4b': 'q4-b', '10a': 'q10-a'}
RETIRED = [('card-source-bindings.json', k) for k in ['q4-b', 'q2-c', 'q4-c', 'q6-b', 'q6-c', 'q9-a']] + \
          [('card-corrections.json', k) for k in ['q2-c', 'q4-a', 'q4-b', 'q4-c', 'q6-b', 'q6-c', 'q9-a']]
LEDGER = [(1, 'Answer Question'), (2, 'or'), (3, 'or'), (3, 'or'), (3, 'Select'), (3, 'any two'), (4, 'one of'), (4, 'or'), (4, 'any other'),
          (5, 'any two'), (5, 'OR'), (5, 'or')]
GAPS = {'q9-b': {'cons-2-7'}, 'q9-c': {'cons-2-7'}}
LEAF = {
    'q1-a': [('wall', 32, list(range(0, 33, 4))), ('timber-floor', 16, list(range(0, 17, 4))), ('presentation', 8, BAND8)],
    'q1-b': [('ventilation', 4, r(4))],
    'q2-a': [(f'requirement-{i}', 12, r(12)) for i in (1, 2)],
    'q2-b': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q2-c': [('fittings', 12, r(12)), ('grab-rails', 4, r(4)), ('dimensions', 4, r(4)), ('sewer-gas', 4, r(4))],
    'q3-a': [('daylight', 16, r(16)), ('open-plan', 16, r(16))],
    'q3-b': [(f'reason-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-c': [(f'advantage-{i}', 5, r(5)) for i in (1, 2)],
    'q4-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q4-b': [('walls', 24, None)],
    'q4-c': [('wall-1', 6, r(6)), ('wall-2', 6, r(6))],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 18, list(range(0, 19, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, r(3))],
    'q5-b': [('required-resistance', 6, r(6))] + [(k, 3, r(3)) for k in ['existing-resistance', 'difference', 'formula', 'thickness']],
    'q5-c': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q6-a': [(f'advantage-{i}', 5, r(5)) for i in (1, 2)],
    'q6-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-c': [(f'feature-{i}', 10, r(10)) for i in (1, 2)],
    'q7-a': [('roof', 24, list(range(0, 25, 4))), ('wall', 20, list(range(0, 21, 4))), ('both-walls', 4, r(4)), ('presentation', 8, BAND8)],
    'q7-b': [('dimensions', 4, r(4))],
    'q8-a': [('natural', 8, r(8)), ('artificial', 8, r(8))],
    'q8-b': [('formula', 6, r(6)), ('floor-area', 3, r(3)), ('product', 3, r(3)), ('solve', 6, r(6)), ('area', 2, r(2))],
    'q8-c': [(f'advancement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q9-a': [(k, 4, r(4)) for k in ['sketch', 'note', 'reinforcement', 'dimensions', 'reasons']],
    'q9-b': [(k, 6, r(6)) for k in ['mixing', 'placing', 'compacting', 'curing']],
    'q9-c': [('note', 8, r(8)), ('sketch', 8, r(8))],
    'q10-a': [('items', 24, None)],
    'q10-b': [(k, 6, r(6)) for k in ['diagram', 'ducting', 'airflow', 'description']],
    'q10-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 60 for k in COMPOSITE})
ACCESS = (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment'])
LIGHT = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
WALLS = (['cons-3-3', 'cons-3-2'], ['walls'])
MHRV = (['cons-6-5'], ['condensation-air-tightness', 'passive-design'])
HERITAGE = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-4-2', 'cons-3-3'], ['question-1-drawing-questions', 'foundations', 'floors', 'walls']),
    'q1-b': (['cons-4-2', 'cons-6-5'], ['floors', 'wood-rot-ventilation']),
    'q2-a': ACCESS, 'q2-b': (['cons-1-2'], ['planning-sustainability-environment']), 'q2-c': ACCESS,
    'q3-a': LIGHT, 'q3-b': LIGHT, 'q3-c': (['cons-1-1', 'cons-1-2'], ['conservation-restoration']),
    'q4-a': WALLS, 'q4-b': (['cons-3-3', 'cons-3-2', 'cons-6-2'], ['walls', 'heat-loss-insulation']),
    'q4-c': (['cons-3-3', 'cons-1-2'], ['walls', 'sustainability-the-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q5-c': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q6-a': (['cons-1-2'], ['sustainability-the-environment']), 'q6-b': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-c': (['cons-6-3', 'cons-6-4'], ['heat-loss-insulation', 'sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-8', 'cons-3-9', 'cons-3-10', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q7-b': (['cons-3-8'], ['roofs']),
    'q8-a': (['cons-7-4', 'cons-7-2'], ['windows-light']), 'q8-b': (['cons-7-2', 'cons-3-5'], ['windows-light']), 'q8-c': (['cons-3-6'], ['windows-light']),
    'q9-a': (['cons-2-4', 'cons-2-5'], ['foundations']), 'q9-b': (['cons-2-7', 'cons-2-4'], ['foundations']), 'q9-c': (['cons-2-7', 'cons-2-4'], ['foundations']),
    'q10-a': (['cons-6-5', 'cons-6-4'], ['passive-design', 'condensation-air-tightness']), 'q10-b': MHRV, 'q10-c': MHRV,
    'q10-alt-discussion': HERITAGE, 'q10-alt-guidelines': HERITAGE,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 282], False), 'q2-original': (P, 2, [30, 282, 580, 545], False),
    'q3-original': (P, 2, [30, 545, 580, 800], False), 'q4-original': (P, 3, [30, 39, 580, 315], False),
    'q5-original': (P, 3, [30, 315, 580, 800], False), 'q6-original': (P, 4, [30, 39, 580, 300], False),
    'q7-original': (P, 4, [30, 300, 580, 520], False), 'q8-original': (P, 4, [30, 520, 580, 800], False),
    'q9-original': (P, 5, [30, 39, 580, 302], False), 'q10-original': (P, 5, [30, 302, 580, 565], False),
    'q10-alt-original': (P, 5, [30, 590, 580, 800], False),
    'q1-section': composite((4, [45, 56, 575, 800]), (5, [45, 56, 575, 509])),
    'q2-requirements': (S, 5, [45, 509, 575, 790], True), 'q2-advantages': (S, 6, [45, 56, 575, 270], True), 'q2-layout': (S, 6, [28, 270, 575, 790], True),
    'q3-layout': (S, 7, [45, 56, 575, 390], True), 'q3-reasons': composite((7, [45, 390, 575, 760]), (8, [45, 56, 575, 212])),
    'q3-advantages': composite((8, [45, 212, 575, 765]), (9, [45, 56, 575, 176])),
    'q4-requirements': composite((9, [45, 174, 415, 200]), (9, [45, 200, 575, 420]), (9, [45, 420, 455, 446])),
    'q4-walls': composite((9, [45, 433, 575, 785]), (10, [45, 56, 575, 240])),
    'q4-discussion': composite((10, [45, 240, 575, 790]), (11, [45, 56, 575, 755])),
    'q5-calculation': (S, 12, [45, 56, 575, 340], True), 'q5-thickness': (S, 12, [45, 342, 575, 505], True),
    'q5-cost': composite((12, [45, 505, 575, 790]), (13, [45, 56, 575, 205])),
    'q6-advantages': (S, 13, [45, 215, 575, 475], True), 'q6-features': composite((13, [45, 477, 575, 785]), (14, [45, 56, 575, 326])),
    'q6-operating': composite((14, [45, 326, 575, 790]), (15, [45, 56, 575, 495])),
    'q7-section': composite((16, [45, 56, 575, 700]), (17, [30, 56, 575, 370])),
    'q8-light': (S, 17, [45, 370, 575, 790], True), 'q8-window': composite((18, [45, 56, 575, 415]), (18, [45, 415, 400, 437])),
    'q8-glazing': composite((18, [45, 412, 575, 790]), (19, [45, 56, 575, 205])),
    'q9-foundation': (S, 19, [45, 207, 575, 590], True),
    'q9-concrete': composite((19, [45, 460, 385, 620]), (19, [45, 620, 575, 785]), (20, [45, 56, 575, 415])),
    'q9-test': composite((20, [30, 415, 430, 430]), (20, [30, 430, 575, 775]), (21, [45, 56, 575, 440])),
    'q10-principles': composite((21, [45, 441, 575, 790]), (22, [45, 56, 575, 816])),
    'q10-mhrv': composite((23, [45, 56, 575, 285]), (23, [45, 430, 575, 800])), 'q10-advantages': (S, 23, [45, 288, 575, 428], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-requirements', 'q2-b': 'q2-advantages', 'q2-c': 'q2-layout', 'q2-complete': 'q2-layout',
            'q3-a': 'q3-layout', 'q3-b': 'q3-reasons', 'q3-c': 'q3-advantages', 'q3-complete': 'q3-layout',
            'q4-a': 'q4-requirements', 'q4-b': 'q4-walls', 'q4-c': 'q4-discussion', 'q4-complete': 'q4-walls',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-thickness', 'q5-c': 'q5-cost', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-advantages', 'q6-b': 'q6-features', 'q6-c': 'q6-operating', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-light', 'q8-b': 'q8-window', 'q8-c': 'q8-glazing', 'q8-complete': 'q8-window',
            'q9-a': 'q9-foundation', 'q9-b': 'q9-concrete', 'q9-c': 'q9-test', 'q9-complete': 'q9-concrete',
            'q10-a': 'q10-principles', 'q10-b': 'q10-mhrv', 'q10-c': 'q10-advantages', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q4-b': {9, 10}, 'q4-complete': {9, 10}, 'q10-a': {21, 22}, 'q10-complete': {21, 22}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 5, 27], '2': [5, 6, 28], '3': [7, 8, 9, 29], '4': [9, 10, 11, 30], '5': [12, 13, 31], '6': [13, 14, 15, 32],
                '7': [16, 17, 33], '8': [17, 18, 19, 34], '9': [19, 20, 21, 35], '10': [21, 22, 23, 36], '10-alt': [24, 25, 37]}
WORKED = [('q5-a', [12], ['0.03472', '0.67568', '0.078125', '1.151', '0.869']),
          ('q5-b', [12], ['6.6666', '5.5156', '0.20408']),
          ('q5-c', [12], ['252', '7,257,600', '1,828,915.2', '48.9669', '47.99']),
          ('q8-b', [18], ['16.8', '8400', '8.4'])]
RUBRIC = 'Question 1 and any four of the other nine questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
