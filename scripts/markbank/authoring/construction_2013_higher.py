"""Source-pinned validator for the 2013 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q9(a) any-three and Q10(a) any-two
cards and selection words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2013_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2013, 'higher'
HASHES = ('ae15d2922194ca980c0f2cd89d011a1f8f54b26f2c9ef75a75538d84808b5693', '1c269d4c127339d06f4efe11b0d4cfcd0126230fde3aab345f89839aaf1abba3')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 996
LEGACY = set()
CHOICES = {'q9-a': ('locations', 3, 12, ['Location 1', 'Location 2', 'Location 3', 'Location 4']),
           'q10-a': ('items', 2, 12, ['Building orientation', 'Thermal mass', 'Primary energy demand'])}
FINITE = {'9a': 'q9-a', '10a': 'q10-a'}
LEDGER = [(1, 'Answer Question'), (4, 'either'), (4, 'or'), (5, 'Select'), (5, 'any three'), (5, 'Select'), (5, 'any two'), (5, 'any two'),
          (5, 'OR'), (5, 'or'), (5, 'or')]
GAPS = {'q8-c': {'cons-2-7'}}
LEAF = {
    'q1-a': [('details', 40, list(range(0, 41, 4))), ('dimensions', 6, r(6)), ('handrails', 4, r(4)), ('presentation', 6, r(6))],
    'q1-b': [('feature-1', 2, r(2)), ('feature-2', 2, r(2))],
    'q2-a': [(k, 9, r(9)) for k in ['training', 'vigilance', 'teamwork']],
    'q2-b': [(k, 6, r(6)) for k in ['ladder-risks', 'window-risks', 'ladder-procedures', 'window-procedures']],
    'q2-c': [(f'guideline-{i}', 3, r(3)) for i in (1, 2, 3)],
    'q3-a': [('extension', 20, r(20)), ('layout', 20, r(20))],
    'q3-b': [('sunlight', 10, r(10)), ('view', 10, r(10))],
    'q4-a': [('items', 36, list(range(0, 37, 4))), ('sizes', 4, r(4))],
    'q4-b': [('consideration-1', 6, r(6)), ('consideration-2', 6, r(6))],
    'q4-c': [(k, 2, r(2)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q5-a': [('frame', 15, r(15)), ('glazing', 15, r(15))],
    'q5-b': [('thermal', 7, r(7)), ('environmental', 7, r(7))],
    'q5-c': [('notes', 8, r(8)), ('sketch', 8, r(8))],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(k, 10, r(10)) for k in ['scale', 'modify', 'services']],
    'q7-a': [('details', 45, list(range(0, 46, 5))), ('dimensions', 6, r(6)), ('presentation', 6, r(6))],
    'q7-b': [('liners', 3, r(3))],
    'q8-a': [(f'requirement-{i}', 10, r(10)) for i in (1, 2)],
    'q8-b': [('strip', 10, r(10)), ('raft', 10, r(10)), ('recommendation', 3, r(3)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q8-c': [(f'guideline-{i}', 3, r(3)) for i in (1, 2, 3)],
    'q9-a': [('locations', 36, None)],
    'q9-b': [('material-1', 6, r(6)), ('material-2', 6, r(6))],
    'q9-c': [('discussion-1', 6, r(6)), ('discussion-2', 6, r(6))],
    'q10-a': [('items', 24, None)],
    'q10-b': [(k, 6, r(6)) for k in ['layout', 'location', 'ducting', 'explanation']],
    'q10-c': [('consideration-1', 6, r(6)), ('consideration-2', 6, r(6))],
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
SAFE = (['cons-1-8'], ['site-safety'])
LIGHT = (['cons-1-2', 'cons-6-4', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
PASSIVE = (['cons-6-5'], ['passive-design', 'condensation-air-tightness'])
HOUSING = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-4-4', 'cons-4-3'], ['question-1-drawing-questions', 'stairs', 'floors']),
    'q1-b': (['cons-4-4'], ['stairs']),
    'q2-a': SAFE, 'q2-b': SAFE, 'q2-c': (['cons-9-4', 'cons-1-8'], ['site-safety']),
    'q3-a': LIGHT, 'q3-b': LIGHT,
    'q4-a': (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating']),
    'q4-b': (['cons-6-4', 'cons-5-2'], ['sustainability-the-environment', 'hot-water-space-heating']),
    'q4-c': (['cons-5-3', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment']),
    'q5-a': (['cons-6-1', 'cons-3-6'], ['heat-u-value-calculations', 'windows-light']),
    'q5-b': (['cons-6-3', 'cons-3-6', 'cons-1-2'], ['heat-u-value-calculations', 'windows-light', 'sustainability-the-environment']),
    'q5-c': (['cons-3-6', 'cons-3-4', 'cons-6-2'], ['windows-light', 'walls', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q7-a': (['cons-1-5', 'cons-5-7', 'cons-4-2'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'floors']),
    'q7-b': (['cons-5-7'], ['fireplaces-fire-prevention']),
    'q8-a': (['cons-2-2'], ['foundations']), 'q8-b': (['cons-2-4', 'cons-2-3', 'cons-2-5'], ['foundations']),
    'q8-c': (['cons-2-7', 'cons-2-5'], ['foundations']),
    'q9-a': (['cons-3-4', 'cons-3-10', 'cons-3-6'], ['walls', 'roofs', 'windows-light']), 'q9-b': (['cons-3-4'], ['walls']),
    'q9-c': (['cons-3-3', 'cons-6-6'], ['walls', 'condensation-air-tightness']),
    'q10-a': (['cons-6-4', 'cons-6-2', 'cons-6-3'], ['passive-design', 'heat-loss-insulation']), 'q10-b': PASSIVE,
    'q10-c': (['cons-6-5'], ['passive-design']),
    'q10-alt-discussion': HOUSING, 'q10-alt-guidelines': HOUSING,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 50, 580, 280], False), 'q2-original': (P, 2, [30, 280, 580, 510], False),
    'q3-original': (P, 2, [30, 510, 580, 796], False), 'q4-original': (P, 3, [30, 50, 580, 236], False),
    'q5-original': (P, 3, [30, 236, 580, 790], False), 'q6-original': (P, 4, [30, 50, 580, 328], False),
    'q7-original': (P, 4, [30, 328, 580, 577], False), 'q8-original': (P, 4, [30, 577, 580, 790], False),
    'q9-original': (P, 5, [30, 50, 580, 294], False), 'q10-original': (P, 5, [30, 294, 580, 580], False),
    'q10-alt-original': (P, 5, [30, 605, 580, 790], False),
    'q1-section': (S, 4, [45, 50, 575, 800], True),
    'q2-culture': composite((5, [45, 50, 575, 536]), (5, [45, 536, 440, 585])),
    'q2-risks': composite((5, [45, 585, 440, 790]), (5, [440, 540, 575, 760]), (6, [45, 50, 575, 258])),
    'q2-tools': (S, 6, [45, 258, 575, 480], True),
    'q3-design': composite((6, [45, 483, 575, 800]), (7, [45, 50, 575, 310]), (7, [45, 310, 430, 462]), (7, [430, 312, 575, 488])),
    'q3-reasons': composite((7, [45, 462, 430, 800]), (7, [430, 525, 575, 720]), (8, [45, 50, 575, 150])),
    'q4-system': (S, 8, [45, 148, 575, 800], True),
    'q4-siting': (S, 9, [45, 50, 575, 452], True), 'q4-advantages': (S, 9, [45, 452, 575, 790], True),
    'q5-calculation': (S, 10, [45, 50, 575, 790], True),
    'q5-comparison': (S, 11, [45, 60, 575, 556], True), 'q5-head': (S, 11, [45, 556, 575, 800], True),
    'q6-features': composite((12, [45, 50, 575, 800]), (13, [45, 60, 575, 800]), (14, [45, 50, 575, 262])),
    'q6-buyers': composite((14, [45, 262, 575, 800]), (15, [45, 60, 575, 300])),
    'q7-section': (S, 15, [25, 300, 575, 800], True),
    'q8-requirements': composite((16, [45, 60, 575, 255]), (16, [45, 255, 390, 278])),
    'q8-foundations': composite((16, [45, 276, 390, 371]), (16, [390, 252, 575, 371]), (16, [45, 371, 575, 800])), 'q8-concrete': (S, 17, [45, 50, 575, 305], True),
    'q9-locations': composite((17, [45, 305, 575, 800]), (18, [45, 60, 370, 172]), (18, [370, 80, 575, 263])),
    'q9-materials': composite((18, [45, 170, 370, 263]), (18, [45, 263, 575, 420])),
    'q9-moisture': (S, 18, [45, 420, 575, 800], True),
    'q10-principles': composite((19, [45, 60, 575, 800]), (20, [45, 50, 575, 800])),
    'q10-mhrv': composite((21, [45, 50, 575, 800]), (22, [45, 50, 575, 175])),
    'q10-location': (S, 22, [45, 175, 575, 480], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-culture', 'q2-b': 'q2-risks', 'q2-c': 'q2-tools', 'q2-complete': 'q2-risks',
            'q3-a': 'q3-design', 'q3-b': 'q3-reasons', 'q3-complete': 'q3-design',
            'q4-a': 'q4-system', 'q4-b': 'q4-siting', 'q4-c': 'q4-advantages', 'q4-complete': 'q4-system',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-comparison', 'q5-c': 'q5-head', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-buyers', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-requirements', 'q8-b': 'q8-foundations', 'q8-c': 'q8-concrete', 'q8-complete': 'q8-foundations',
            'q9-a': 'q9-locations', 'q9-b': 'q9-materials', 'q9-c': 'q9-moisture', 'q9-complete': 'q9-locations',
            'q10-a': 'q10-principles', 'q10-b': 'q10-mhrv', 'q10-c': 'q10-location', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q9-a': {17, 18}, 'q9-complete': {17, 18}, 'q10-a': {19, 20}, 'q10-complete': {19, 20}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 26], '2': [5, 6, 27], '3': [6, 7, 8, 28], '4': [8, 9, 29], '5': [10, 11, 30], '6': [12, 13, 14, 15, 31],
                '7': [15, 32], '8': [16, 17, 33], '9': [17, 18, 34], '10': [19, 20, 21, 22, 35], '10-alt': [23, 24, 36]}
WORKED = [('q5-a', [10], ['0.400', '2.857', '5.607', '0.178', '0.0038095', '0.25', '3.8388', '0.260495'])]
RUBRIC = 'Question 1 and four other questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
