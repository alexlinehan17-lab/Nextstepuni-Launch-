"""Source-pinned validator for the 2020 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure, checked by the shared engine construction_paper.validate against
the pinned SEC paper and scheme. Run: python3 scripts/markbank/authoring/construction_2020_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2020, 'higher'
HASHES = ('22c84780da2ac7b0b034506068b6b35804d9b522dfffc51a340b0c80b5c006c5', '74eaba480cdb9437c28084ac9707fc46bda4ba0fa321d275ce98fe9f8523ac8d')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 806
BAND8 = [0, 4, 6, 8]
Q4A = ['materials-and-finishes', 'shape-and-form', 'streetscape']
Q9A = ['completeness', 'flexibility', 'isolation']
LEGACY = ({'q1-b', 'q2-a', 'q2-b', 'q3-a', 'q3-c-advantages', 'q3-c-disadvantages', 'q4-b', 'q4-c', 'q5-a', 'q5-b', 'q6-a-advantages',
           'q6-a-disadvantages', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q8-a', 'q8-c', 'q9-b', 'q9-c', 'q10-a', 'q10-c'}
          | {f'q4-a-{k}' for k in Q4A} | {f'q9-a-{k}' for k in Q9A})
FINITE = {}
LABELLED = {f'q4-a-{k}' for k in Q4A} | {f'q9-a-{k}' for k in Q9A}
LEDGER = [(1, 'Answer Question'), (7, 'OR')]
LEAF = {
    'q1-a': [('details', 44, r(44)), ('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q1-b': [('ventilation', 4, r(4))],
    'q2-a': [(k, 14, r(14)) for k in ['erecting', 'accessing', 'platforms']],
    'q2-b': [(f'responsibility-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-b': [('layout', 15, r(15)), ('considerations', 9, r(9)), ('open-plan', 3, r(3)), ('justification', 3, r(3))],
    'q3-c-advantages': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q3-c-disadvantages': [('disadvantage-1', 3, r(3)), ('disadvantage-2', 3, r(3))],
    **{f'q4-a-{k}': [('characteristic', 8, r(8))] for k in Q4A},
    'q4-b': [('notes', 6, r(6)), ('sketches', 14, r(14)), ('justification', 4, r(4))],
    'q4-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q5-a': [('resistances', 27, list(range(0, 28, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [('notes', 4, r(4)), ('sketch', 8, r(8))],
    'q6-a-advantages': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q6-a-disadvantages': [('disadvantage-1', 3, r(3)), ('disadvantage-2', 3, r(3))],
    'q6-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-c': [('modification-1', 6, r(6)), ('modification-2', 6, r(6)), ('justification-1', 3, r(3)), ('justification-2', 3, r(3))],
    'q7-a': [('details', 45, r(45)), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q7-b': [('air-supply', 4, r(4))],
    'q8-a': [(f'consideration-{i}', 10, r(10)) for i in (1, 2)],
    'q8-b': [('notes', 12, r(12)), ('sketch', 12, r(12)), ('dimensions', 4, r(4))],
    'q8-c': [(f'consideration-{i}', 6, r(6)) for i in (1, 2)],
    **{f'q9-a-{k}': [('principle', 8, r(8))] for k in Q9A},
    'q9-b': [('partition', 10, r(10)), ('floor', 10, r(10)), ('materials', 4, r(4)), ('dimension', 4, r(4))],
    'q9-c': [(f'benefit-{i}', 4, r(4)) for i in (1, 2)],
    'q10-a': [(f'consideration-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q10-b': [('diagram', 4, r(4)), ('unit', 4, r(4)), ('ducting', 4, r(4)), ('airflow', 4, r(4)), ('description', 8, r(8))],
    'q10-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-complete': ['q2-a', 'q2-b'], 'q3-c': ['q3-c-advantages', 'q3-c-disadvantages'],
    'q3-complete': ['q3-a', 'q3-b', 'q3-c'], 'q4-a': [f'q4-a-{k}' for k in Q4A], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'],
    'q5-complete': ['q5-a', 'q5-b', 'q5-c'], 'q6-a': ['q6-a-advantages', 'q6-a-disadvantages'], 'q6-complete': ['q6-a', 'q6-b', 'q6-c'],
    'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-a': [f'q9-a-{k}' for k in Q9A],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q3-c': 12, 'q4-a': 24, 'q6-a': 12, 'q9-a': 24, **{k: 60 for k in COMPOSITE if k.endswith('-complete')}})
SAFE = (['cons-1-8'], ['site-safety'])
ACCESS = (['cons-1-2'], ['planning-sustainability-environment'])
URBAN = (['cons-1-2', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration'])
RETRO = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
DRAIN = (['cons-5-6'], ['drainage'])
SOUND = (['cons-8-3'], ['sound'])
MVHR = (['cons-6-5'], ['condensation-air-tightness', 'passive-design'])
ENERGY = (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q1-b': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q2-a': SAFE, 'q2-b': SAFE, 'q3-a': ACCESS, 'q3-b': ACCESS, 'q3-c-advantages': ACCESS, 'q3-c-disadvantages': ACCESS,
    **{f'q4-a-{k}': URBAN for k in Q4A}, 'q4-b': URBAN, 'q4-c': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'floors']),
    'q6-a-advantages': RETRO, 'q6-a-disadvantages': RETRO,
    'q6-b': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-c': (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-5-7', 'cons-4-2'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'floors']),
    'q7-b': (['cons-5-7', 'cons-6-5'], ['fireplaces-fire-prevention', 'condensation-air-tightness']),
    'q8-a': (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']), 'q8-b': DRAIN, 'q8-c': DRAIN,
    **{f'q9-a-{k}': SOUND for k in Q9A}, 'q9-b': (['cons-8-3', 'cons-4-3', 'cons-4-5'], ['sound', 'floors', 'doors']), 'q9-c': SOUND,
    'q10-a': MVHR, 'q10-b': MVHR, 'q10-c': MVHR, 'q10-alt-a': ENERGY, 'q10-alt-b': ENERGY,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 455], False), 'q2-original': (P, 2, [45, 455, 580, 695], False),
    'q3-original': (P, 3, [45, 53, 580, 422], False), 'q4-original': (P, 3, [45, 422, 580, 760], False),
    'q5-original': (P, 4, [45, 53, 580, 712], False), 'q6-original': (P, 5, [45, 53, 580, 431], False),
    'q7-original': (P, 5, [45, 431, 580, 745], False), 'q8-original': (P, 6, [45, 53, 580, 395], False),
    'q9-original': (P, 6, [45, 395, 580, 760], False), 'q10-original': (P, 7, [45, 53, 580, 417], False),
    'q10-alt-original': (P, 7, [45, 478, 580, 722], False),
    'q1-section': composite((4, [51, 51, 550, 745]), (5, [51, 383, 550, 775])),
    'q1-ventilation': (S, 5, [51, 51, 550, 383], True),
    'q2-scaffolding': composite((6, [51, 51, 550, 790]), (7, [51, 51, 550, 775]), (8, [51, 51, 550, 585])),
    'q3-layout': composite((9, [51, 455, 550, 762]), (10, [51, 51, 550, 690])),
    'q4-materials': (S, 12, [51, 51, 550, 455], True), 'q4-shape': (S, 12, [51, 455, 550, 775], True),
    'q4-streetscape': (S, 13, [51, 51, 550, 465], True),
    'q4-characteristics': composite((12, [51, 51, 550, 775]), (13, [51, 51, 550, 465])),
    'q4-design': composite((13, [51, 470, 550, 765]), (14, [51, 51, 550, 605])),
    'q5-calculation': composite((15, [51, 51, 550, 735]), (16, [51, 51, 550, 240])),
    'q5-thermal-bridge': (S, 16, [51, 240, 550, 565], True),
    'q6-low-impact': (S, 18, [51, 51, 550, 725], True),
    'q6-modifications': composite((19, [51, 51, 550, 750]), (20, [51, 51, 550, 530])),
    'q7-section': (S, 21, [51, 51, 550, 765], True),
    'q8-location': (S, 22, [51, 51, 550, 735], True), 'q8-pipework': (S, 23, [51, 51, 550, 615], True),
    'q9-completeness': (S, 24, [51, 51, 550, 350], True), 'q9-flexibility': (S, 24, [51, 350, 550, 532], True),
    'q9-isolation': (S, 24, [51, 532, 550, 750], True), 'q9-principles': (S, 24, [51, 51, 550, 750], True),
    'q9-upgrades': composite((25, [51, 51, 550, 790]), (26, [51, 51, 550, 262])),
    'q10-mvhr': (S, 28, [51, 51, 550, 640], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-ventilation', 'q1-complete': 'q1-section',
            'q2-a': 'q2-scaffolding', 'q2-complete': 'q2-scaffolding', 'q3-b': 'q3-layout', 'q3-complete': 'q3-layout',
            'q4-a-materials-and-finishes': 'q4-materials', 'q4-a-shape-and-form': 'q4-shape', 'q4-a-streetscape': 'q4-streetscape',
            'q4-a': 'q4-characteristics', 'q4-b': 'q4-design', 'q4-complete': 'q4-design',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-thermal-bridge', 'q5-complete': 'q5-calculation',
            'q6-b': 'q6-low-impact', 'q6-c': 'q6-modifications', 'q6-complete': 'q6-low-impact',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-location', 'q8-b': 'q8-pipework', 'q8-complete': 'q8-pipework',
            'q9-a-completeness': 'q9-completeness', 'q9-a-flexibility': 'q9-flexibility', 'q9-a-isolation': 'q9-isolation',
            'q9-a': 'q9-principles', 'q9-b': 'q9-upgrades', 'q9-complete': 'q9-upgrades',
            'q10-b': 'q10-mvhr', 'q10-complete': 'q10-mvhr'}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}
SCHEME_PAGES = {'1': [4, 5, 32], '2': [6, 7, 8, 33], '3': [9, 10, 11, 34], '4': [12, 13, 14, 35], '5': [15, 16, 36], '6': [17, 18, 19, 20, 37],
                '7': [21, 38], '8': [22, 23, 39], '9': [24, 25, 26, 40], '10': [27, 28, 41], '10-alt': [29, 30, 42]}
WORKED = [('q5-a', [15], ['0.003', '0.092', '9.091', '0.117', '0.001', '0.148', '0.188', '9.993']),
          ('q5-b', [15], ['81.9', '8,845,200', '724,421.88', '19.39', '18.62'])]
RUBRIC = 'Question 1 and any four of the other nine questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
