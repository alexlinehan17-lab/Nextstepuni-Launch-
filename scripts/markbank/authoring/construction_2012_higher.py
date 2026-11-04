"""Source-pinned validator for the 2012 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q9(b) any-three and Q10(a) any-two
cards and selection words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2012_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2012, 'higher'
HASHES = ('2a13b942b63a681f24f3a0a146afdd78e3020e620a3c63dac93a1c822d5bef20', '1d92d18557cfb807abeb7d938cf5baac82f061135cb8a6f755e2c1d607c93995')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 1061
LEGACY = set()
CHOICES = {'q9-b': ('locations', 3, 10, ['Ground Floor', 'Window Cill', 'Light Fittings', 'Trapdoor']),
           'q10-a': ('items', 2, 10, ['Building form', 'Indoor environment', 'Energy performance'])}
FINITE = {'9b': 'q9-b', '10a': 'q10-a'}
LEDGER = [(1, 'Answer Question'), (5, 'one of'), (5, 'Select'), (5, 'any three'), (5, 'any two'), (5, 'OR')]
LEAF = {
    'q1-a': [('details', 48, list(range(0, 49, 4))), ('presentation', 8, r(8))],
    'q1-b': [('abutment', 4, r(4))],
    'q2-a': [('requirement-1', 11, r(11)), ('requirement-2', 11, r(11))],
    'q2-b': [('items', 20, r(20)), ('dimensions', 3, r(3))],
    'q2-c': [(k, 3, r(3)) for k in ['window', 'shower', 'toilet', 'basin', 'rails']],
    'q3-a': [('layout', 20, r(20)), ('thermal', 20, r(20))],
    'q3-b': [('layout-reasons', 10, r(10)), ('wall-reasons', 10, r(10))],
    'q4-a': [('principle-1', 14, r(14)), ('principle-2', 14, r(14))],
    'q4-b': [('details', 16, list(range(0, 17, 2))), ('dimensions', 4, r(4))],
    'q4-c': [(f'reason-{i}', 4, r(4)) for i in (1, 2, 3)],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 21, list(range(0, 22, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, r(3))],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [('notes', 5, r(5)), ('sketches', 10, r(10))],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(k, 10, r(10)) for k in ['orientation', 'flexibility', 'materials']],
    'q7-a': [('details', 45, list(range(0, 46, 5))), ('dimensions', 4, r(4)), ('presentation', 8, r(8))],
    'q7-b': [('vapour', 3, r(3))],
    'q8-a': [('wiring', 4, r(4)), ('sockets', 4, r(4)), ('cables', 4, r(4)), ('colours', 12, [0, 4, 8, 12])],
    'q8-b': [('feature-1', 12, r(12)), ('feature-2', 12, r(12))],
    'q8-c': [('strategy-1', 6, r(6)), ('strategy-2', 6, r(6))],
    'q9-a': [('point-1', 10, r(10)), ('point-2', 10, r(10))],
    'q9-b': [('locations', 30, None)],
    'q9-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q10-a': [('items', 20, None)],
    'q10-b': [('ducting', 10, r(10)), ('airflow', 5, r(5)), ('explanation', 5, r(5))],
    'q10-c': [(k, 5, r(5)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b', 'q9-c'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 60 for k in COMPOSITE})
LIFE = (['cons-1-2'], ['planning-sustainability-environment'])
SEPTIC = (['cons-5-5'], ['drainage'])
ELEC = (['cons-5-8'], ['services-water-gas-electricity'])
AIR = (['cons-6-5', 'cons-6-6'], ['condensation-air-tightness'])
HOUSING = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-6', 'cons-3-9', 'cons-3-10'], ['question-1-drawing-questions', 'windows-light', 'roofs']),
    'q1-b': (['cons-3-10', 'cons-3-4'], ['roofs', 'walls']),
    'q2-a': LIFE, 'q2-b': LIFE, 'q2-c': LIFE,
    'q3-a': (['cons-1-2', 'cons-3-6', 'cons-6-2'], ['planning-sustainability-environment', 'windows-light', 'heat-loss-insulation']),
    'q3-b': (['cons-6-4', 'cons-6-2'], ['passive-design', 'heat-loss-insulation']),
    'q4-a': SEPTIC, 'q4-b': SEPTIC, 'q4-c': (['cons-5-5', 'cons-1-3'], ['drainage', 'planning-sustainability-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-4-2', 'cons-6-2', 'cons-3-4'], ['floors', 'heat-loss-insulation', 'walls']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-4-3'], ['question-1-drawing-questions', 'doors', 'walls', 'floors']),
    'q7-b': (['cons-6-6', 'cons-6-5'], ['condensation-air-tightness']),
    'q8-a': ELEC, 'q8-b': ELEC, 'q8-c': (['cons-5-8', 'cons-5-3'], ['services-water-gas-electricity']),
    'q9-a': AIR,
    'q9-b': (['cons-6-5', 'cons-4-2', 'cons-3-6', 'cons-5-8'], ['condensation-air-tightness', 'floors', 'windows-light', 'services-water-gas-electricity']),
    'q9-c': (['cons-3-3', 'cons-6-5'], ['walls', 'condensation-air-tightness']),
    'q10-a': (['cons-6-2', 'cons-6-5', 'cons-6-3'], ['passive-design', 'heat-loss-insulation']),
    'q10-b': (['cons-6-5'], ['passive-design', 'condensation-air-tightness']),
    'q10-c': (['cons-6-3', 'cons-6-2'], ['passive-design', 'heat-loss-insulation']),
    'q10-alt-discussion': HOUSING, 'q10-alt-guidelines': HOUSING,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 50, 580, 256], False), 'q2-original': (P, 2, [30, 256, 580, 517], False),
    'q3-original': (P, 2, [30, 517, 580, 775], False), 'q4-original': (P, 3, [30, 50, 580, 327], False),
    'q5-original': (P, 3, [30, 327, 580, 790], False), 'q6-original': (P, 4, [30, 50, 580, 403], False),
    'q7-original': (P, 4, [30, 403, 580, 623], False), 'q8-original': (P, 4, [30, 623, 580, 790], False),
    'q9-original': (P, 5, [30, 50, 580, 331], False), 'q10-original': (P, 5, [30, 331, 580, 620], False),
    'q10-alt-original': (P, 5, [30, 640, 580, 790], False),
    'q1-section': (S, 4, [40, 57, 585, 784], True),
    'q2-requirements': (S, 5, [40, 60, 585, 515], True),
    'q2-layout': composite((5, [40, 476, 300, 515]), (5, [40, 515, 585, 783])),
    'q2-locations': (S, 6, [40, 60, 585, 450], True),
    'q3-design': composite((6, [40, 450, 585, 784]), (7, [40, 60, 585, 558])), 'q3-reasons': (S, 7, [40, 558, 585, 784], True),
    'q4-scheme': (S, 8, [40, 60, 585, 784], True),
    'q5-calculation': (S, 9, [40, 60, 585, 612], True), 'q5-floor': (S, 9, [40, 612, 585, 784], True),
    'q6-features': composite((10, [40, 60, 585, 784]), (11, [40, 60, 585, 275])),
    'q6-importance': composite((11, [40, 275, 585, 784]), (12, [40, 60, 585, 560])),
    'q7-section': (S, 13, [40, 60, 585, 784], True),
    'q8-wiring': composite((14, [40, 60, 205, 178]), (14, [205, 60, 585, 337])),
    'q8-safety': composite((14, [40, 176, 205, 337]), (14, [40, 337, 585, 536]), (14, [460, 220, 560, 334])),
    'q8-economy': composite((14, [40, 536, 585, 784]), (15, [40, 60, 585, 160])),
    'q9-airtightness': (S, 15, [40, 160, 585, 784], True),
    'q9-locations': (S, 16, [40, 60, 585, 645], True), 'q9-service': (S, 16, [40, 645, 585, 784], True),
    'q10-principles': composite((17, [40, 60, 585, 784]), (18, [40, 60, 585, 273.5]), (20, [40, 60, 585, 240])),
    'q10-mhrv': composite((18, [40, 273.5, 585, 784]), (19, [40, 60, 585, 462])),
    'q10-passive': (S, 19, [40, 462, 585, 784], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-requirements', 'q2-b': 'q2-layout', 'q2-c': 'q2-locations', 'q2-complete': 'q2-layout',
            'q3-a': 'q3-design', 'q3-b': 'q3-reasons', 'q3-complete': 'q3-design',
            'q4-a': 'q4-scheme', 'q4-b': 'q4-scheme', 'q4-c': 'q4-scheme', 'q4-complete': 'q4-scheme',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-floor', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-importance', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-wiring', 'q8-b': 'q8-safety', 'q8-c': 'q8-economy', 'q8-complete': 'q8-wiring',
            'q9-a': 'q9-airtightness', 'q9-b': 'q9-locations', 'q9-c': 'q9-service', 'q9-complete': 'q9-locations',
            'q10-a': 'q10-principles', 'q10-b': 'q10-mhrv', 'q10-c': 'q10-passive', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q9-b': {16}, 'q9-complete': {16}, 'q10-a': {17, 18}, 'q10-complete': {17, 18}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 24], '2': [5, 6, 25], '3': [6, 7, 26], '4': [8, 27], '5': [9, 28], '6': [10, 11, 12, 29],
                '7': [13, 30], '8': [14, 15, 31], '9': [15, 16, 32], '10': [17, 18, 19, 20, 33], '10-alt': [20, 21, 34]}
WORKED = [('q5-a', [9], ['0.0426', '0.625', '0.001', '0.3125', '0.1692', '0.1667', '1.421', '0.704']),
          ('q5-b', [9], ['665.28', '3,360', '12,096,000', '8,047,226', '215.45', '183.13'])]
RUBRIC = 'Question 1 and four other questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
