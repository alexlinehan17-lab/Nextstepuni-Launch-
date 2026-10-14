"""Source-pinned validator for the 2011 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q9(a) any-three and Q10(a) any-two
cards and selection words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2011_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2011, 'higher'
HASHES = ('d02fe420b8c4aabdf284fc4551d08af11e98fc0b3447a29f8b98ecf78e7f2be8', 'd71697473ec9446fc95f06bb2c855e31c25047b741324af6f7a2c8b6f5ea8bef')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 1128
LEGACY = set()
CHOICES = {'q9-a': ('locations', 3, 16, ['Wall plate and eaves', 'Insulated steel lintel', 'Sill', 'Floor insulation']),
           'q10-a': ('items', 2, 12, ['Foundations suitable for passive house', 'Airtight building envelope', 'Windows and Glazing'])}
FINITE = {'9a': 'q9-a', '10a': 'q10-a'}
LEDGER = [(1, 'Answer Question'), (3, 'one of'), (5, 'Select'), (5, 'any three'), (5, 'any two'), (5, 'OR'), (5, 'or'), (5, 'any stage'), (5, 'or'), (5, 'or')]
LEAF = {
    'q1-a': [('details', 44, list(range(0, 45, 4))), ('presentation', 8, r(8))],
    'q1-b': [('drainage', 8, r(8))],
    'q2-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q2-b': [('roof-1', 12, r(12)), ('roof-2', 12, r(12))],
    'q2-c': [('recommendation', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q3-a': [('envelope', 20, r(20)), ('layout', 20, r(20))],
    'q3-b': [('envelope-reasons', 10, r(10)), ('layout-reasons', 10, r(10))],
    'q4-a': [(k, 8, r(8)) for k in ['mass', 'completeness', 'isolation']],
    'q4-b': [(k, 4, r(4)) for k in ['reason-1', 'reason-2', 'note', 'sketch']],
    'q4-c': [(k, 4, r(4)) for k in ['note', 'sketch', 'principles', 'materials', 'dimensions']],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 18, list(range(0, 19, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, r(3))],
    'q5-b': [(k, 3, r(3)) for k in ['target', 'existing', 'difference', 'formula', 'thickness']],
    'q5-c': [('disadvantage-1', 6, r(6)), ('disadvantage-2', 6, r(6)), ('recommendation', 6, r(6))],
    'q6-a': [(f'feature-{i}', 14, r(14)) for i in (1, 2, 3)],
    'q6-b': [(k, 6, r(6)) for k in ['form', 'materials', 'lifetime']],
    'q7-a': [('chimney', 16, list(range(0, 17, 4))), ('flashing', 12, list(range(0, 13, 4))), ('roof', 16, list(range(0, 17, 4))), ('presentation', 8, r(8))],
    'q7-b': [('detail-1', 4, r(4)), ('detail-2', 4, r(4))],
    'q8-a': [('items', 28, list(range(0, 29, 4))), ('sizes', 4, r(4))],
    'q8-b': [('solar', 16, list(range(0, 17, 4)))],
    'q8-c': [('location', 6, r(6)), ('factor-1', 3, r(3)), ('factor-2', 3, r(3))],
    'q9-a': [('locations', 48, None)],
    'q9-b': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
    'q10-a': [('items', 24, None)],
    'q10-b': [('description', 20, r(20))],
    'q10-c': [(k, 4, r(4)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q10-alt-discussion': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-guidelines': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-complete': ['q3-a', 'q3-b'],
    'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-complete': ['q6-a', 'q6-b'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b'],
    'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-discussion', 'q10-alt-guidelines'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 60 for k in COMPOSITE})
ROOF = (['cons-3-8'], ['roofs'])
SUN = (['cons-6-4', 'cons-3-6', 'cons-6-2'], ['passive-design', 'windows-light', 'heat-loss-insulation'])
SOUND = (['cons-8-3'], ['sound'])
HEAT = (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'])
NEIGH = (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-7', 'cons-4-2', 'cons-3-4'], ['question-1-drawing-questions', 'doors', 'floors', 'walls']),
    'q1-b': (['cons-3-7', 'cons-1-2'], ['doors', 'planning-sustainability-environment']),
    'q2-a': (['cons-3-8', 'cons-3-9'], ['roofs']), 'q2-b': ROOF, 'q2-c': ROOF,
    'q3-a': SUN, 'q3-b': SUN,
    'q4-a': SOUND, 'q4-b': (['cons-8-3', 'cons-3-3'], ['sound', 'walls']), 'q4-c': (['cons-8-3', 'cons-4-5'], ['sound', 'doors']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q5-c': (['cons-3-3', 'cons-6-2'], ['walls', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-5-7', 'cons-3-9', 'cons-3-10'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs']),
    'q7-b': (['cons-5-7'], ['fireplaces-fire-prevention']),
    'q8-a': HEAT, 'q8-b': (['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment']),
    'q8-c': (['cons-6-4'], ['sustainability-the-environment']),
    'q9-a': (['cons-6-2', 'cons-3-10', 'cons-3-6', 'cons-4-2'], ['heat-loss-insulation', 'roofs', 'windows-light', 'floors']),
    'q9-b': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q10-a': (['cons-2-4', 'cons-6-5', 'cons-3-6', 'cons-6-2'], ['passive-design', 'foundations', 'condensation-air-tightness', 'windows-light']),
    'q10-b': (['cons-6-5'], ['passive-design', 'condensation-air-tightness']),
    'q10-c': (['cons-6-5'], ['passive-design', 'condensation-air-tightness']),
    'q10-alt-discussion': NEIGH, 'q10-alt-guidelines': NEIGH,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 50, 580, 276], False), 'q2-original': (P, 2, [30, 276, 580, 429], False),
    'q3-original': (P, 2, [30, 429, 580, 790], False), 'q4-original': (P, 3, [30, 50, 580, 321], False),
    'q5-original': (P, 3, [30, 321, 580, 790], False), 'q6-original': (P, 4, [30, 50, 580, 305], False),
    'q7-original': (P, 4, [30, 305, 580, 527], False), 'q8-original': (P, 4, [30, 527, 580, 790], False),
    'q9-original': (P, 5, [30, 50, 580, 262], False), 'q10-original': (P, 5, [30, 262, 580, 526], False),
    'q10-alt-original': (P, 5, [30, 550, 580, 790], False),
    'q1-section': composite((4, [40, 60, 585, 575]), (5, [40, 60, 585, 762])),
    'q2-requirements': (S, 6, [40, 60, 585, 345], True),
    'q2-roofs': composite((6, [40, 345, 585, 780]), (7, [40, 60, 585, 425])), 'q2-recommendation': (S, 7, [40, 425, 585, 780], True),
    'q3-design': composite((8, [40, 60, 585, 780]), (9, [40, 60, 585, 780]), (10, [40, 60, 585, 578])),
    'q3-reasons': composite((10, [40, 578, 585, 780]), (11, [40, 60, 585, 220])),
    'q4-principles': composite((11, [40, 220, 585, 780]), (12, [40, 60, 585, 214])),
    'q4-party-wall': (S, 12, [40, 214, 585, 680], True), 'q4-partition': (S, 13, [40, 60, 585, 780], True),
    'q5-calculation': (S, 14, [40, 60, 585, 607], True),
    'q5-walls': composite((14, [40, 607, 585, 780]), (15, [40, 60, 585, 780])),
    'q6-features': composite((16, [40, 60, 585, 780]), (17, [40, 60, 585, 204])),
    'q6-importance': composite((17, [40, 204, 585, 780]), (18, [40, 60, 585, 780]), (19, [40, 60, 585, 232])),
    'q7-section': (S, 20, [40, 60, 585, 780], True),
    'q8-system': (S, 21, [40, 60, 585, 780], True), 'q8-siting': (S, 22, [40, 60, 585, 435], True),
    'q9-scheme': composite((22, [40, 435, 585, 780]), (23, [40, 60, 585, 659])),
    'q10-principles': composite((24, [40, 60, 585, 780]), (25, [40, 60, 585, 282]), (25, [40, 282, 405, 366]), (25, [405, 280, 585, 392])),
    'q10-mhrv': composite((25, [40, 366, 405, 389.5]), (25, [40, 389.5, 585, 633])),
    'q10-advantages': composite((25, [40, 633, 585, 780]), (26, [40, 60, 585, 345])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-requirements', 'q2-b': 'q2-roofs', 'q2-c': 'q2-recommendation', 'q2-complete': 'q2-roofs',
            'q3-a': 'q3-design', 'q3-b': 'q3-reasons', 'q3-complete': 'q3-design',
            'q4-a': 'q4-principles', 'q4-b': 'q4-party-wall', 'q4-c': 'q4-partition', 'q4-complete': 'q4-party-wall',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-walls', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-features', 'q6-b': 'q6-importance', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-system', 'q8-b': 'q8-system', 'q8-c': 'q8-siting', 'q8-complete': 'q8-system',
            'q9-a': 'q9-scheme', 'q9-b': 'q9-scheme', 'q9-complete': 'q9-scheme',
            'q10-a': 'q10-principles', 'q10-b': 'q10-mhrv', 'q10-c': 'q10-advantages', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q9-a': {22, 23}, 'q9-complete': {22, 23}, 'q10-a': {24, 25}, 'q10-complete': {24, 25}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 4, '7': 4, '8': 4, '9': 5, '10': 5, '10-alt': 5}
SCHEME_PAGES = {'1': [4, 5, 30], '2': [6, 7, 31], '3': [8, 9, 10, 11, 32], '4': [11, 12, 13, 33], '5': [14, 15, 34], '6': [16, 17, 18, 19, 35],
                '7': [20, 36], '8': [21, 22, 37], '9': [22, 23, 38], '10': [24, 25, 26, 39], '10-alt': [26, 27, 28, 40]}
WORKED = [('q5-a', [14], ['0.03255', '0.075', '0.63955', '1.563599']),
          ('q5-b', [14], ['3.703', '3.06345', '0.1133476', '113'])]
RUBRIC = 'Question 1 and four other questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
