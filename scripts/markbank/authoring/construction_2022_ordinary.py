"""Source-pinned validator for the 2022 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card with its
eight per-term IDs withdrawn into it, selection words and the 20 pre-audit cards corrected in place),
checked by the shared engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2022_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2022, 'ordinary'
HASHES = ('69e29520c0fbe774c560c2cd91363cc5cf125b168ec3266f5ea31021f4617b0d', '196311e890e14bc99d31a4de3318fd97ec5a2850908c00379a6d2ec108282e3b')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 780
BAND8, BAND6 = [0, 4, 6, 8], [0, 2, 4, 6]
Q8 = 'q8-None-strip-foundation'
TERMS = ['Strip foundation', 'Fascia board', 'Airtight tape', 'Wind turbine', 'Septic tank', 'Dovetail joint', 'Wall tie', 'Cordless jigsaw', 'Underfloor heating']
LEGACY = {'q1-a', 'q1-b', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q3-c', 'q4-a', 'q4-c', 'q5-a', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q7-c',
          'q9-a', 'q9-b', 'q9-c', Q8}
CONSOLIDATED = {f'q8-None-{t}': Q8 for t in ['fascia-board', 'airtight-tape', 'wind-turbine', 'septic-tank', 'dovetail-joint', 'wall-tie',
                                            'cordless-jigsaw', 'underfloor-heating']}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
TAILS = {'8': 'front porch to their house.'}
LEDGER = [(1, 'Answer any'), (4, 'any five')]
GAPS = {Q8: {'cons-10-1', 'cons-10-4', 'cons-9-2'}}
LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q1-b': [('closer', 3, [0, 3])],
    'q2-a': [('method', 14, r(14)), ('type', 4, r(4)), ('thickness', 4, r(4))],
    'q2-b': [('tank', 9, r(9)), ('pipework', 9, r(9))],
    'q2-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q3-a': [(k, 4, r(4)) for k in ['sketch', 'collection', 'to-tank', 'filters']],
    'q3-b': [('items', 24, list(range(0, 25, 4))), ('sketch', 4, r(4))],
    'q3-c': [('advantage', 6, r(6))],
    'q4-a': [('items', 20, r(20)), ('note', 4, r(4)), ('presentation', 6, BAND6)],
    'q4-b': [('advantage', 5, r(5)), ('disadvantage', 5, r(5))],
    'q4-c': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q5-b': [('creaking', 4, [0, 4])],
    'q6-a': [(f'sign-{i}', 9, r(9)) for i in (1, 2, 3)],
    'q6-b': [('risk-1', 5, r(5)), ('risk-2', 5, r(5))],
    'q6-c': [('precaution', 13, r(13))],
    'q7-a': [('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    'q7-b': [('sketch', 6, r(6))] + [(k, 6, r(6)) for k in ['outdoor', 'storage', 'flower-beds', 'lawn']],
    'q7-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    Q8: [('terms', 50, None)],
    'q9-a': [('wood', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q9-b': [('modification-1', 13, r(13)), ('modification-2', 13, r(13))],
    'q9-c': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'abc'), ('3', 'abc'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-7', 'cons-3-4', 'cons-3-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q1-b': (['cons-3-3', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation']),
    'q2-a': (['cons-3-9', 'cons-6-2'], ['roofs', 'heat-loss-insulation']),
    'q2-b': (['cons-5-2', 'cons-6-2'], ['hot-water-space-heating', 'heat-loss-insulation']),
    'q2-c': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q3-a': (['cons-5-4'], ['drainage']),
    'q3-b': (['cons-5-2', 'cons-5-6'], ['hot-water-space-heating', 'drainage']),
    'q3-c': (['cons-5-4', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']),
    'q4-a': (['cons-4-5'], ['windows-doors']),
    'q4-b': (['cons-4-5', 'cons-8-3'], ['windows-doors', 'sound']),
    'q4-c': (['cons-1-2'], ['planning-sustainability-environment']),
    'q5-a': (['cons-1-5', 'cons-4-4'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q5-b': (['cons-4-4', 'cons-10-1'], ['foundations-floors-walls', 'wood-rot-ventilation']),
    'q6-a': (['cons-1-8'], ['site-safety']), 'q6-b': (['cons-1-8', 'cons-9-4'], ['site-safety']), 'q6-c': (['cons-1-8'], ['site-safety']),
    'q7-a': (['cons-1-2'], ['planning-sustainability-environment']), 'q7-b': (['cons-1-2'], ['planning-sustainability-environment']),
    'q7-c': (['cons-1-2'], ['planning-sustainability-environment']),
    Q8: (['cons-2-4', 'cons-3-10', 'cons-6-5', 'cons-5-8', 'cons-1-2', 'cons-5-5', 'cons-10-1', 'cons-10-4', 'cons-3-3', 'cons-9-2', 'cons-5-3'],
         ['foundations-floors-walls', 'roofs', 'air-tightness-condensation', 'services-water-gas-electrical', 'planning-sustainability-environment',
          'drainage', 'wood-rot-ventilation', 'hot-water-space-heating']),
    'q9-a': (['cons-3-2', 'cons-10-3'], ['foundations-floors-walls', 'wood-rot-ventilation']),
    'q9-b': (['cons-3-5'], ['windows-doors']),
    'q9-c': (['cons-1-2'], ['planning-sustainability-environment']),
}
GAPS.update({'q5-a': {'cons-4-4'}, 'q5-b': {'cons-4-4', 'cons-10-1'}})


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 284], False), 'q2-original': (P, 2, [45, 284, 580, 530], False),
    'q3-original': (P, 2, [45, 530, 580, 768], False), 'q4-original': (P, 3, [45, 39, 580, 325], False),
    'q5-original': (P, 3, [45, 325, 580, 522], False), 'q6-original': (P, 3, [45, 522, 580, 770], False),
    'q7-original': (P, 4, [45, 52, 580, 394], False), 'q8-original': (P, 4, [45, 394, 580, 494], False),
    'q9-original': (P, 4, [45, 530, 580, 765], False),
    'q1-scheme': (S, 4, [25, 58, 580, 790], True),
    'q2-method': (S, 5, [25, 58, 580, 365], True), 'q2-tank': (S, 5, [25, 365, 580, 655], True), 'q2-advantages': (S, 5, [25, 655, 580, 790], True),
    'q3-collection': (S, 6, [25, 58, 580, 384], True), 'q3-supply': (S, 6, [25, 384, 580, 714], True), 'q3-advantage': (S, 6, [51, 698, 410, 790], True),
    'q4-partition': (S, 7, [25, 58, 580, 520], True), 'q4-pros-cons': (S, 7, [25, 520, 580, 650], True), 'q4-reasons': (S, 7, [25, 650, 580, 790], True),
    'q5-scheme': (S, 8, [25, 58, 580, 790], True),
    'q6-signs': (S, 9, [25, 58, 580, 625], True), 'q6-risks': (S, 9, [25, 625, 580, 775], True), 'q6-public': (S, 10, [25, 51, 580, 770], True),
    'q7-reasons': (S, 11, [25, 58, 580, 255], True),
    'q7-layout': composite((11, [25, 255, 580, 790]), (12, [25, 51, 580, 580])),
    'q7-advantages': (S, 12, [25, 585, 580, 745], True),
    'q8-terms': composite((13, [25, 51, 580, 790]), (14, [25, 51, 580, 690]), (15, [25, 51, 580, 780])),
    'q9-wood': (S, 16, [25, 51, 580, 320], True), 'q9-light': (S, 16, [25, 325, 580, 590], True), 'q9-porch': (S, 16, [25, 590, 580, 775], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-method', 'q2-b': 'q2-tank', 'q2-c': 'q2-advantages', 'q2-complete': 'q2-method',
            'q3-a': 'q3-collection', 'q3-b': 'q3-supply', 'q3-c': 'q3-advantage', 'q3-complete': 'q3-supply',
            'q4-a': 'q4-partition', 'q4-b': 'q4-pros-cons', 'q4-c': 'q4-reasons', 'q4-complete': 'q4-partition',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-risks', 'q6-c': 'q6-public', 'q6-complete': 'q6-signs',
            'q7-a': 'q7-reasons', 'q7-b': 'q7-layout', 'q7-c': 'q7-advantages', 'q7-complete': 'q7-layout', Q8: 'q8-terms',
            'q9-a': 'q9-wood', 'q9-b': 'q9-light', 'q9-c': 'q9-porch', 'q9-complete': 'q9-light'}
CHOICE_FIGURE_PAGES = {Q8: {13, 14, 15}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
SCHEME_PAGES = {'1': [4, 17], '2': [5, 18], '3': [6, 19], '4': [7, 20], '5': [8, 21], '6': [9, 10, 22], '7': [11, 12, 23], '8': [13, 14, 15, 24], '9': [16, 25]}
RUBRIC = 'Any three of nine questions, 50 marks each, 150 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
