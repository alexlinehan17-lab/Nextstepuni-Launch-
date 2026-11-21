"""Source-pinned validator for the 2022 Higher Level Construction Studies DEFERRED theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, choices and selection words),
checked by the shared engine construction_paper.validate against the pinned SEC deferred paper and
scheme (deferredexams/ and deferredmarkingschemes/). No pre-audit cards exist for this sitting, so every
task is an addition. Run: python3 scripts/markbank/authoring/construction_2022_higher_deferred.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2022, 'higher'
SITTING = 'deferred'
HASHES = ('11b605087a6ee3d40ab3668af3003b8b97c740fe50ae3d188cdf984becb99356', 'e2d8850b5be78760d43044a95dee137e3b8250fd8fecd411c67355bbc5aa1ec3')
P, S = cp.sources(YEAR, LEVEL, SITTING)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 1261
BAND8 = [0, 4, 6, 8]
LEGACY = set()
ITEMS2A = ['safety-signage', 'personal-protective-equipment', 'awareness']
ACTIVITIES = ['use-of-vehicles', 'use-of-a-ladder', 'demolition-work']
CHOICES = {'q6-b': ('items', 2, 10, ['Flexibility of design', 'Use of recycled materials', 'Thermal efficiency']),
           'q9-b': ('locations', 2, 14, ['Back of chimney', 'Front of chimney', 'Head of Window']),
           'q10-a': ('items', 2, 10, ['Building form', 'Continuity of insulation', 'Windows and glazing'])}
FINITE = {'6b': 'q6-b', '9b': 'q9-b', '10a': 'q10-a'}
# A Q2(c) activity, named only by reference to 2(b), carries the scheme's own heading after ' — '.
LABELLED = {f'q2-c-{a}' for a in ACTIVITIES}
LEDGER = [(1, 'Answer any'), (5, 'any two'), (6, 'any two'), (7, 'any two'), (7, 'OR'), (7, 'or')]
LEAF = {
    'q1-a': [('foundation-wall', 12, r(12)), ('floor', 20, r(20)), ('window', 12, r(12)), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q1-b': [('ventilation', 5, r(5))],
    **{f'q2-a-{k}': [('importance', 5, r(5))] for k in ITEMS2A},
    **{f'q2-b-{a}': [('risk', 3, r(3))] for a in ACTIVITIES},
    **{f'q2-c-{a}': [('procedure-1', 6, r(6)), ('procedure-2', 6, r(6))] for a in ACTIVITIES},
    'q3-a': [('external', 18, r(18)), ('internal', 18, r(18))],
    'q3-b': [('daylight', 8, r(8)), ('connection', 8, r(8)), ('garden', 8, r(8))],
    'q4-a': [('layout', 32, r(32)), ('sizes', 4, r(4))],
    'q4-b': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q4-c': [(f'consideration-{i}', 6, r(6)) for i in (1, 2)],
    'q5-a': [('resistances', 24, list(range(0, 25, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['required-resistance', 'existing-resistance', 'difference', 'formula', 'thickness']],
    'q5-c': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [('items', 20, None)],
    'q6-c': [(f'advantage-{i}', 5, r(5)) for i in (1, 2)],
    'q7-a': [('external-wall', 15, r(15)), ('door', 15, r(15)), ('eaves', 15, r(15)), ('tiles', 3, r(3)), ('presentation', 8, BAND8)],
    'q7-b': [('thermal-bridge', 4, r(4))],
    'q8-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q8-b': [(f'wall-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q8-c': [('recommendation', 2, r(2)), ('justification', 4, r(4))],
    'q9-a': [(f'reason-{i}', 8, r(8)) for i in (1, 2)],
    'q9-b': [('locations', 28, None)],
    'q9-c': [(f'material-{i}', 8, r(8)) for i in (1, 2)],
    'q10-a': [('items', 20, None)],
    'q10-b': [('orientation', 10, r(10)), ('sun-path', 5, r(5)), ('justification', 5, r(5))],
    'q10-c': [('reason-1', 5, r(5)), ('reason-2', 5, r(5)), ('modification', 10, r(10))],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'],
    'q2-a': [f'q2-a-{k}' for k in ITEMS2A], 'q2-b': [f'q2-b-{a}' for a in ACTIVITIES], 'q2-c': [f'q2-c-{a}' for a in ACTIVITIES],
    'q2-complete': ['q2-a', 'q2-b', *[f'q2-c-{a}' for a in ACTIVITIES]],
    'q3-complete': ['q3-a', 'q3-b'], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'], 'q8-complete': ['q8-a', 'q8-b', 'q8-c'],
    'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'],
    'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q2-a': 15, 'q2-b': 9, 'q2-c': 36, **{k: 60 for k in COMPOSITE if k.endswith('-complete')}})
SAFETY = (['cons-1-8'], ['site-safety'])
GARDEN_ROOM = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
EMBODIED = (['cons-1-2'], ['sustainability-the-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-4-3', 'cons-3-3', 'cons-3-6'], ['question-1-drawing-questions', 'foundations', 'floors', 'walls', 'windows-light']),
    'q1-b': (['cons-4-3', 'cons-6-5'], ['floors', 'wood-rot-ventilation']),
    **{f'q2-a-{k}': SAFETY for k in ITEMS2A}, **{f'q2-{p}-{a}': SAFETY for p in 'bc' for a in ACTIVITIES},
    'q3-a': GARDEN_ROOM, 'q3-b': GARDEN_ROOM,
    'q4-a': (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating']),
    'q4-b': (['cons-5-7', 'cons-5-3'], ['fireplaces-fire-prevention', 'hot-water-space-heating']),
    'q4-c': (['cons-5-3', 'cons-5-7'], ['hot-water-space-heating', 'fireplaces-fire-prevention']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']),
    'q5-b': (['cons-6-1', 'cons-6-2', 'cons-4-2'], ['heat-u-value-calculations', 'heat-loss-insulation', 'floors']),
    'q5-c': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-1-2', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-c': (['cons-1-2'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-3-4', 'cons-3-10', 'cons-3-8'], ['question-1-drawing-questions', 'doors', 'walls', 'roofs']),
    'q7-b': (['cons-6-2', 'cons-3-7', 'cons-3-4'], ['heat-loss-insulation', 'doors', 'walls']),
    'q8-a': (['cons-3-2', 'cons-3-3'], ['walls']),
    'q8-b': (['cons-3-3', 'cons-6-2'], ['walls', 'heat-loss-insulation']),
    'q8-c': (['cons-3-3', 'cons-1-2'], ['walls', 'sustainability-the-environment']),
    'q9-a': (['cons-3-4', 'cons-3-3'], ['walls']),
    'q9-b': (['cons-3-4', 'cons-5-7', 'cons-3-10', 'cons-3-6'], ['walls', 'fireplaces-fire-prevention', 'roofs', 'windows-light']),
    'q9-c': (['cons-3-4', 'cons-3-9'], ['walls', 'roofs']),
    'q10-a': (['cons-6-4', 'cons-6-2', 'cons-3-6'], ['passive-design', 'heat-loss-insulation', 'windows-light']),
    'q10-b': (['cons-6-4'], ['passive-design']),
    'q10-c': (['cons-6-4', 'cons-6-5'], ['passive-design']),
    'q10-alt-a': EMBODIED, 'q10-alt-b': EMBODIED,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


Q10_PAGES = ((23, [51, 51, 545, 778]), (24, [51, 51, 545, 784]))
FIGURES = {
    'q1-original': (P, 2, [45, 50, 580, 372], False), 'q2-original': (P, 2, [45, 440, 580, 730], False),
    'q3-original': (P, 3, [45, 50, 580, 386], False), 'q4-original': (P, 3, [45, 440, 580, 750], False),
    'q5-original': (P, 4, [45, 50, 580, 722], False), 'q6-original': (P, 5, [45, 50, 580, 405], False),
    'q7-original': (P, 5, [45, 470, 580, 760], False), 'q8-original': (P, 6, [45, 50, 580, 322], False),
    'q9-original': (P, 6, [45, 412, 580, 736], False), 'q10-original': (P, 7, [45, 50, 580, 388], False),
    'q10-alt-original': (P, 7, [45, 500, 580, 710], False),
    'q1-section': composite((4, [51, 51, 545, 792]), (5, [51, 51, 545, 518])),
    'q1-ventilation': (S, 5, [51, 520, 545, 792], True),
    'q2-procedures': (S, 8, [51, 51, 545, 768], True),
    'q3-design': composite((9, [51, 51, 562, 768]), (10, [51, 51, 545, 290])),
    'q4-system': (S, 11, [51, 51, 553, 392], True),
    'q5-u-value': (S, 12, [51, 51, 545, 380], True), 'q5-thickness': (S, 12, [51, 404, 545, 645], True),
    'q5-cost': (S, 13, [51, 51, 545, 606], True),
    'q5-scheme': composite((12, [51, 51, 545, 645]), (13, [51, 51, 545, 606])),
    'q6-low-impact': (S, 14, [51, 51, 545, 566], True),
    'q7-section': composite((16, [26, 51, 545, 732]), (17, [51, 51, 545, 284])),
    'q7-thermal-bridge': (S, 17, [51, 333, 545, 642], True),
    'q8-requirements': (S, 18, [51, 51, 545, 780], True),
    'q8-walls': composite((19, [51, 51, 545, 708]), (20, [51, 51, 545, 232])),
    'q9-locations': (S, 21, [51, 268, 560, 766], True), 'q9-materials': (S, 22, [51, 51, 545, 656], True),
    'q10-items': composite(*Q10_PAGES),
    'q10-orientation': (S, 25, [51, 51, 545, 400], True),
    'q10-overheating': composite((25, [51, 422, 545, 672]), (26, [51, 51, 545, 426])),
    'q10-scheme': composite(*Q10_PAGES, (25, [51, 51, 545, 672]), (26, [51, 51, 545, 426])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-ventilation', 'q1-complete': 'q1-section',
            **{f'q2-c-{a}': 'q2-procedures' for a in ACTIVITIES}, 'q2-c': 'q2-procedures', 'q2-complete': 'q2-procedures',
            'q3-a': 'q3-design', 'q3-complete': 'q3-design', 'q4-a': 'q4-system', 'q4-complete': 'q4-system',
            'q5-a': 'q5-u-value', 'q5-b': 'q5-thickness', 'q5-c': 'q5-cost', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-low-impact', 'q6-complete': 'q6-low-impact',
            'q7-a': 'q7-section', 'q7-b': 'q7-thermal-bridge', 'q7-complete': 'q7-section',
            'q8-a': 'q8-requirements', 'q8-b': 'q8-walls', 'q8-complete': 'q8-walls',
            'q9-b': 'q9-locations', 'q9-c': 'q9-materials', 'q9-complete': 'q9-locations',
            'q10-a': 'q10-items', 'q10-b': 'q10-orientation', 'q10-c': 'q10-overheating', 'q10-complete': 'q10-scheme'}
# Every printed item of a one-card choice keeps its scheme drawings, on the card and on its complete route.
# Q6(b)'s three items are answered in text alone in the scheme (pages 14-15), so that card carries no figure.
CHOICE_FIGURE_PAGES = {'q9-b': {21}, 'q9-complete': {21}, 'q10-a': {23, 24}, 'q10-complete': {23, 24}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}
SCHEME_PAGES = {'1': [4, 5, 29], '2': [6, 7, 8, 30], '3': [9, 10, 31], '4': [11, 32], '5': [12, 13, 33], '6': [14, 15, 34],
                '7': [16, 17, 35], '8': [18, 19, 20, 36], '9': [21, 22, 37], '10': [23, 24, 25, 26, 38], '10-alt': [26, 27, 39]}
WORKED = [('q5-a', [12], ['0.104', '0.009', '0.127', '2.273', '0.001', '0.313', '0.130', '0.188', '3.145', '0.318']),
          ('q5-b', [12], ['8.333', '3.144', '5.190', '0.114', '114/115']),
          ('q5-c', [13], ['132.3', '7,459,200', '986,852', '26.422', '25.63'])]
RUBRIC = 'Any four of ten questions, 60 marks each, 240 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
