"""Source-pinned validator for the 2021 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure, checked by the shared engine construction_paper.validate against
the pinned SEC paper and scheme. Run: python3 scripts/markbank/authoring/construction_2021_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2021, 'higher'
HASHES = ('4c6644e20702d03fbfedaffe0e97f0e48edc2868ca8c937300cb204de4ce273e', '6753b7de9d8ecb13faaf35f0c954d5b69bb31c1671aae77db7300594419840ca')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 783
BAND8 = [0, 4, 6, 8]
Q2A = ['safety-training', 'personal-protective-equipment-ppe', 'vigilance']
Q2B = ['repairing-a-chimney-stack', 'overhead-electrical-cables', 'on-site-health-hygiene']
Q4A = ['availability-of-services', 'existing-trees-and-hedgerows', 'site-topography']
LEGACY = ({'q1-a', 'q1-b', 'q2-c', 'q3-a', 'q3-b', 'q3-c-advantages', 'q3-c-disadvantages', 'q4-b', 'q4-c', 'q5-b', 'q6-a', 'q6-b', 'q6-c',
           'q7-a', 'q7-b', 'q8-a', 'q8-b', 'q8-c', 'q9-a', 'q9-b', 'q9-c', 'q10-a', 'q10-b', 'q10-c'}
          | {f'q2-a-{k}' for k in Q2A} | {f'q2-b-{k}' for k in Q2B} | {f'q4-a-{k}' for k in Q4A})
FINITE = {}
MARKED_ALIKE = {'4b': dict(options=['site A', 'site B'], cardId='cons-2021-hl-q4-b')}
LABELLED = {f'q2-a-{k}' for k in Q2A} | {f'q2-b-{k}' for k in Q2B} | {f'q4-a-{k}' for k in Q4A}
LEDGER = [(1, 'Answer any'), (3, 'Select'), (3, 'or'), (7, 'OR'), (7, 'or')]
LEAF = {
    'q1-a': [('foundation', 16, r(16)), ('floor', 16, r(16)), ('threshold', 16, r(16)), ('presentation', 8, BAND8)],
    'q1-b': [('thermal-bridge', 4, r(4))],
    **{f'q2-a-{k}': [('duty', 6, r(6))] for k in Q2A},
    **{f'q2-b-{k}': [('risk', 6, r(6))] for k in Q2B},
    'q2-c': [(k, 8, r(8)) for k in ['chimney', 'cables', 'hygiene']],
    'q3-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-b': [('layout', 15, r(15))] + [(f'consideration-{i}', 4, r(4)) for i in (1, 2, 3)] + [('justification', 3, r(3))],
    'q3-c-advantages': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q3-c-disadvantages': [('disadvantage-1', 3, r(3)), ('disadvantage-2', 3, r(3))],
    **{f'q4-a-{k}': [('factor', 8, r(8))] for k in Q4A},
    'q4-b': [(f'consideration-{i}', 4, r(4)) for i in (1, 2, 3)],
    'q4-c': [('sketch', 4, r(4)), ('items', 16, r(16)), ('justification', 4, r(4))],
    'q5-a': [('resistances', 24, list(range(0, 25, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['required-resistance', 'existing-resistance', 'difference', 'formula', 'thickness']],
    'q5-c': [('notes', 8, r(8)), ('sketch', 7, r(7))],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2)],
    'q6-c': [(f'advantage-{i}', 5, r(5)) for i in (1, 2)],
    'q7-a': [('chimney', 20, r(20)), ('roofing', 20, r(20)), ('slates', 6, r(6)), ('presentation', 8, BAND8)],
    'q7-b': [('detail-1', 3, r(3)), ('detail-2', 3, r(3))],
    'q8-a': [('layout', 28, r(28)), ('sizes', 4, r(4))],
    'q8-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2)],
    'q8-c': [(f'advantage-{i}', 4, r(4)) for i in (1, 2)],
    'q9-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q9-b': [('board', 5, r(5)), ('sockets', 5, r(5)), ('cabling', 15, r(15)), ('size-colour', 5, r(5))],
    'q9-c': [(f'benefit-{i}', 6, r(6)) for i in (1, 2)],
    'q10-a': [(k, 6, r(6)) for k in ['reason-1', 'reason-2', 'effect-1', 'effect-2']],
    'q10-b': [(f'method-{i}', 12, r(12)) for i in (1, 2)],
    'q10-c': [(f'feature-{i}', 6, r(6)) for i in (1, 2)],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-a': [f'q2-a-{k}' for k in Q2A], 'q2-b': [f'q2-b-{k}' for k in Q2B],
    'q2-complete': ['q2-a', 'q2-b', 'q2-c'], 'q3-c': ['q3-c-advantages', 'q3-c-disadvantages'], 'q3-complete': ['q3-a', 'q3-b', 'q3-c'],
    'q4-a': [f'q4-a-{k}' for k in Q4A], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'], 'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q2-a': 18, 'q2-b': 18, 'q3-c': 12, 'q4-a': 24, **{k: 60 for k in COMPOSITE if k.endswith('-complete')}})
SAFE = (['cons-1-8'], ['site-safety'])
OFFICE = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
SITE = (['cons-1-3'], ['planning-sustainability-environment'])
REUSE = (['cons-1-1', 'cons-1-2'], ['conservation-restoration'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-7', 'cons-4-2', 'cons-2-4'], ['question-1-drawing-questions', 'doors', 'floors', 'foundations']),
    'q1-b': (['cons-6-2', 'cons-3-7'], ['heat-loss-insulation', 'doors']),
    **{f'q2-a-{k}': SAFE for k in Q2A}, **{f'q2-b-{k}': SAFE for k in Q2B}, 'q2-c': SAFE,
    'q3-a': OFFICE, 'q3-b': OFFICE,
    'q3-c-advantages': (['cons-1-2'], ['planning-sustainability-environment']), 'q3-c-disadvantages': (['cons-1-2'], ['planning-sustainability-environment']),
    **{f'q4-a-{k}': SITE for k in Q4A}, 'q4-b': SITE,
    'q4-c': (['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']),
    'q5-b': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q5-c': (['cons-6-6', 'cons-3-3'], ['condensation-air-tightness', 'walls']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-6-3', 'cons-5-8', 'cons-5-3'], ['heat-loss-insulation', 'services-water-gas-electricity', 'hot-water-space-heating']),
    'q6-c': (['cons-6-3', 'cons-1-2'], ['heat-loss-insulation', 'sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-5-7', 'cons-3-9', 'cons-3-8'], ['question-1-drawing-questions', 'fireplaces-fire-prevention', 'roofs']),
    'q7-b': (['cons-3-4', 'cons-5-7'], ['walls', 'fireplaces-fire-prevention']),
    'q8-a': (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating']),
    'q8-b': (['cons-5-3'], ['hot-water-space-heating']),
    'q8-c': (['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'sustainability-the-environment']),
    'q9-a': (['cons-5-8'], ['services-water-gas-electricity']), 'q9-b': (['cons-5-8'], ['services-water-gas-electricity']),
    'q9-c': (['cons-5-8', 'cons-1-2'], ['services-water-gas-electricity', 'sustainability-the-environment']),
    'q10-a': (['cons-6-4', 'cons-6-5'], ['passive-design']), 'q10-b': (['cons-6-4'], ['passive-design']),
    'q10-c': REUSE, 'q10-alt-a': REUSE, 'q10-alt-b': REUSE,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 455], False), 'q2-original': (P, 2, [45, 455, 580, 720], False),
    'q3-original': (P, 3, [45, 53, 580, 419], False), 'q4-original': (P, 3, [45, 419, 580, 762], False),
    'q5-original': (P, 4, [45, 53, 580, 615], False), 'q6-original': (P, 5, [45, 53, 580, 469], False),
    'q7-original': (P, 5, [45, 469, 580, 746], False), 'q8-original': (P, 6, [45, 53, 580, 455], False),
    'q9-original': (P, 6, [45, 455, 580, 714], False), 'q10-original': (P, 7, [45, 53, 580, 390], False),
    'q10-alt-original': (P, 7, [45, 465, 580, 683], False),
    'q1-section': composite((4, [51, 51, 550, 600]), (5, [51, 51, 550, 386])),
    'q1-thermal-bridge': (S, 5, [51, 415, 550, 760], True),
    'q2-procedures': composite((7, [51, 460, 550, 790]), (8, [51, 51, 550, 790])),
    'q3-layout': composite((10, [51, 51, 550, 740]), (11, [51, 51, 550, 320])),
    'q4-services': (S, 12, [51, 51, 550, 331], True), 'q4-trees': composite((12, [51, 312, 372, 331]), (12, [51, 331, 550, 510])),
    'q4-topography': (S, 12, [51, 510, 550, 770], True), 'q4-factors': (S, 12, [51, 51, 550, 770], True),
    'q4-sites': (S, 13, [51, 51, 550, 585], True), 'q4-site-plans': (S, 14, [51, 51, 550, 760], True),
    'q5-calculation': (S, 15, [51, 51, 550, 670], True), 'q5-layers': (S, 16, [51, 51, 550, 465], True),
    'q6-low-impact': (S, 17, [51, 51, 550, 598], True),
    'q6-features': composite((17, [51, 598, 550, 782]), (18, [51, 51, 550, 778]), (19, [51, 51, 550, 190])),
    'q7-section': (S, 20, [51, 51, 550, 785], True),
    'q8-system': (S, 21, [51, 51, 550, 591], True),
    'q8-features': composite((21, [51, 591, 550, 790]), (22, [51, 51, 550, 400])),
    'q8-heat-pump': (S, 22, [51, 415, 550, 787], True),
    'q9-ring-main': (S, 24, [51, 51, 550, 575], True),
    'q10-shading': (S, 26, [51, 51, 550, 782], True), 'q10-setting': (S, 27, [51, 51, 550, 640], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-thermal-bridge', 'q1-complete': 'q1-section',
            'q2-c': 'q2-procedures', 'q2-complete': 'q2-procedures', 'q3-b': 'q3-layout', 'q3-complete': 'q3-layout',
            'q4-a-availability-of-services': 'q4-services', 'q4-a-existing-trees-and-hedgerows': 'q4-trees', 'q4-a-site-topography': 'q4-topography',
            'q4-a': 'q4-factors', 'q4-b': 'q4-sites', 'q4-c': 'q4-site-plans', 'q4-complete': 'q4-site-plans',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-layers', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-low-impact', 'q6-b': 'q6-features', 'q6-complete': 'q6-low-impact',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-system', 'q8-b': 'q8-features', 'q8-c': 'q8-heat-pump', 'q8-complete': 'q8-system',
            'q9-b': 'q9-ring-main', 'q9-complete': 'q9-ring-main',
            'q10-b': 'q10-shading', 'q10-c': 'q10-setting', 'q10-complete': 'q10-shading'}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}
SCHEME_PAGES = {'1': [4, 5, 31], '2': [6, 7, 8, 32], '3': [9, 10, 11, 33], '4': [12, 13, 14, 34], '5': [15, 16, 35], '6': [17, 18, 19, 36],
                '7': [20, 37], '8': [21, 22, 38], '9': [23, 24, 39], '10': [25, 26, 27, 40], '10-alt': [28, 29, 41]}
WORKED = [('q5-a', [15], ['0.130', '0.069', '4.487', '0.050', '5.424', '0.184']), ('q5-b', [15], ['6.666', '1.243', '0.04226'])]
RUBRIC = 'Any four of ten questions, 60 marks each, 240 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
