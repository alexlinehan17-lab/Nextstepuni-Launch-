"""Source-pinned validator for the 2013 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the whole-question Q5 drawing, the
Q8 any-five card and selection words; the paper was never carded, so every task is added), checked by the
shared engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2013_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2013, 'ordinary'
HASHES = ('c339448bf1d0e305695e8e4c6671facec2416b13b03c5617cfd632e28f77c34b', 'bbb47b80dd5a3770ac1af97855fbee9264beca1dac16d7c3749ba43acf83541b')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 1035
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
Q8 = 'q8-terms'
TERMS = ['Solar panel', 'Dovetail halving joint', 'Sash cramp', 'Flue liner', 'Purlin', 'Water table', 'Wind turbine', 'Low-e coating', 'Vapour barrier']
LEGACY = set()
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8, 'q5-section'}  # Q8's any-five card and the unlettered Q5 drawing are each a whole question
LEDGER = [(1, 'Answer Question'), (3, 'any five')]
TAILS = {'6': ('the kitchen in a dwelling house.', 'must be worn on a construction site:')}  # Q6(a)'s bullets follow Q9 in the text layer
GAPS = {'q4-a': {'cons-2-1'}, 'q4-b': {'cons-2-5'}, Q8: {'cons-10-1', 'cons-10-4', 'cons-10-6', 'cons-2-1'}, 'q9-a': {'cons-10-1'}}
LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 4, r(4))],
    'q1-b': [('rainwater', 3, r(3)), ('presentation', 8, BAND8)],
    'q2-a': [('cavity-notes', 12, r(12)), ('cavity-sketch', 8, BAND8), ('internal-notes', 12, r(12)), ('internal-sketch', 8, BAND8)],
    'q2-b': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q3-a': [('details', 35, list(range(0, 36, 5))), ('presentation', 8, BAND8)],
    'q3-b': [('primary', 4, r(4)), ('other', 3, r(3))],
    'q4-a': [(k, 9, r(9)) for k in ['profiles', 'trench', 'square', 'level']],
    'q4-b': [('reinforcement', 3, r(3)), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q5-section': [('details', 36, list(range(0, 37, 6))), ('dimensions', 6, r(6)), ('presentation', 8, BAND8)],
    'q6-a': [(k, 6, BAND6) for k in ['eye-sign', 'ear-sign', 'gloves-sign']],
    'q6-b': [(k, 6, r(6)) for k in ['eye', 'ear', 'gloves']],
    'q6-c': [('item', 6, r(6)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q7-a': [('detail-1', 4, r(4)), ('detail-2', 4, r(4)), ('dimensions', 6, r(6)), ('labelling', 8, r(8)), ('presentation', 8, BAND8)],
    'q7-b': [('cold-bridge', 5, r(5))],
    'q7-c': [('covering', 5, r(5)), ('reason-1', 5, r(5)), ('reason-2', 5, r(5))],
    Q8: [('terms', 50, None)],
    'q9-a': [('detail-1', 6, r(6)), ('detail-2', 6, r(6)), ('presentation', 8, BAND8)],
    'q9-b': [('detail-1', 6, r(6)), ('detail-2', 6, r(6)), ('presentation', 8, BAND8)],
    'q9-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'ab'), ('3', 'ab'), ('4', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
SITE = (['cons-1-8'], ['site-safety'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-10', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls']),
    'q1-b': (['cons-3-10', 'cons-5-4'], ['roofs', 'drainage']),
    'q2-a': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-3', 'cons-6-2'], ['heat-loss-insulation']),
    'q3-a': (['cons-5-2'], ['hot-water-space-heating', 'services-water-gas-electrical']),
    'q3-b': (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']),
    'q4-a': (['cons-2-1', 'cons-2-4'], ['foundations-floors-walls']), 'q4-b': (['cons-2-4', 'cons-2-5'], ['foundations-floors-walls']),
    'q5-section': (['cons-1-5', 'cons-4-5', 'cons-4-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q6-a': SITE, 'q6-b': SITE, 'q6-c': SITE,
    'q7-a': (['cons-4-2', 'cons-3-3'], ['foundations-floors-walls']),
    'q7-b': (['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q7-c': (['cons-4-2'], ['foundations-floors-walls']),
    Q8: (['cons-6-4', 'cons-10-1', 'cons-10-4', 'cons-10-6', 'cons-5-7', 'cons-3-8', 'cons-2-1', 'cons-5-8', 'cons-3-6', 'cons-6-2', 'cons-6-6'],
         ['planning-sustainability-environment', 'wood-rot-ventilation', 'fire-places-fire-prevention', 'roofs', 'foundations-floors-walls',
          'services-water-gas-electrical', 'windows-doors', 'heat-loss-insulation', 'air-tightness-condensation']),
    'q9-a': (['cons-3-7', 'cons-10-1'], ['windows-doors', 'wood-rot-ventilation']),
    'q9-b': (['cons-3-6', 'cons-3-7'], ['windows-doors']),
    'q9-c': (['cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 228], False), 'q2-original': (P, 2, [30, 228, 580, 430], False),
    'q3-original': (P, 2, [30, 430, 580, 621], False), 'q4-original': (P, 2, [30, 621, 580, 790], False),
    'q5-original': (P, 3, [30, 39, 580, 208], False), 'q6-original': (P, 3, [30, 208, 580, 378], False),
    'q7-original': (P, 3, [30, 378, 580, 551], False), 'q8-original': (P, 3, [30, 551, 580, 650], False),
    'q9-original': (P, 3, [30, 650, 580, 797], False),
    'q1-section': (S, 4, [25, 45, 580, 778], True), 'q1-rainwater': (S, 5, [25, 45, 580, 206], True),
    'q2-systems': (S, 5, [25, 206, 580, 778], True),
    'q2-advantages': (S, 6, [25, 45, 580, 195], True),
    'q3-system': (S, 6, [25, 195, 580, 578], True), 'q3-tap': (S, 6, [25, 578, 580, 778], True),
    'q4-setting-out': (S, 7, [25, 45, 580, 779], True), 'q4-strip': (S, 8, [25, 45, 580, 340], True),
    'q5-scheme': (S, 8, [25, 340, 580, 778], True),
    'q6-signs': (S, 9, [25, 45, 580, 216], True), 'q6-tasks': (S, 9, [25, 216, 580, 560], True),
    'q6-other': composite((9, [25, 560, 580, 778]), (10, [25, 45, 580, 293])),
    'q7-floor': (S, 10, [25, 293, 580, 576], True), 'q7-cold-bridge': (S, 10, [25, 576, 580, 778], True),
    'q7-covering': (S, 11, [25, 45, 580, 500], True),
    'q8-terms': composite((11, [25, 500, 580, 778]), (12, [25, 45, 580, 778]), (13, [25, 45, 580, 778])),
    'q9-joint': (S, 14, [25, 45, 580, 312], True), 'q9-glass': (S, 14, [25, 312, 580, 613], True),
    'q9-advantages': (S, 14, [25, 613, 580, 778], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-rainwater', 'q1-complete': 'q1-section',
            'q2-a': 'q2-systems', 'q2-b': 'q2-advantages', 'q2-complete': 'q2-systems',
            'q3-a': 'q3-system', 'q3-b': 'q3-tap', 'q3-complete': 'q3-system',
            'q4-a': 'q4-setting-out', 'q4-b': 'q4-strip', 'q4-complete': 'q4-setting-out',
            'q5-section': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-tasks', 'q6-c': 'q6-other', 'q6-complete': 'q6-signs',
            'q7-a': 'q7-floor', 'q7-b': 'q7-cold-bridge', 'q7-c': 'q7-covering', 'q7-complete': 'q7-floor', Q8: 'q8-terms',
            'q9-a': 'q9-joint', 'q9-b': 'q9-glass', 'q9-c': 'q9-advantages', 'q9-complete': 'q9-joint'}
CHOICE_FIGURE_PAGES = {Q8: {11, 12, 13}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 2, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
SCHEME_PAGES = {'1': [4, 5, 15], '2': [5, 6, 16], '3': [6, 17], '4': [7, 8, 18], '5': [8, 19], '6': [9, 10, 20], '7': [10, 11, 21], '8': [11, 12, 13, 22], '9': [14, 23]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
