"""Source-pinned validator for the 2022 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, choices, selection words and
the 27 pre-audit cards corrected in place), checked by the shared engine construction_paper.validate
against the pinned SEC paper and scheme. Run: python3 scripts/markbank/authoring/construction_2022_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2022, 'higher'
HASHES = ('2e74b08fa90a1063dda36fc6d33cf08d67f2d83f63cc663bffb0cb598dde6bb9', 'cc608ae4393ae400dcf2d2ce36bca603e0e542e2a5c937bb22fc0bea65cc0e82')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 762
BAND8 = [0, 4, 6, 8]
LEGACY = {'q1-a', 'q1-b', 'q2-a-entrance-access', 'q2-a-internal-corridor', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q3-c', 'q4-a', 'q4-b', 'q4-c',
          'q5-b', 'q5-c', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q8-a', 'q8-b', 'q8-c-advantages', 'q8-c-disadvantages', 'q9-a', 'q9-b',
          'q9-c', 'q10-a'}
RETIRED = [('card-source-bindings.json', 'q4-b'), ('card-source-bindings.json', 'q4-c')]
CHOICES = {'q6-b': ('items', 2, 10, ['Internal air quality', 'Thermal environment', 'Social interaction']),
           'q9-b': ('items', 2, 18, ['Head of window detail', 'Wallplate position detail', 'Light fitting detail'])}
FINITE = {'6b': 'q6-b', '9b': 'q9-b'}
LABELLED = {'q2-a-entrance-access', 'q2-a-internal-corridor'}
LEDGER = [(1, 'Answer any'), (5, 'any two'), (6, 'any two'), (7, 'OR')]
LEAF = {
    'q1-a': [('external-wall', 16, r(16)), ('flat-roof', 16, r(16)), ('rear-wall', 16, r(16)), ('presentation', 8, BAND8)],
    'q1-b': [('thermal-bridge', 4, r(4))],
    'q2-a-entrance-access': [('detail-1', 6, r(6)), ('detail-2', 6, r(6))],
    'q2-a-internal-corridor': [('detail-1', 6, r(6)), ('detail-2', 6, r(6))],
    'q2-b': [('area-1', 10, r(10)), ('area-2', 10, r(10)), ('dimensions', 4, r(4))],
    'q2-c': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q3-a': [('layout', 15, r(15)), ('living-space', 5, r(5)), ('daylight', 5, r(5)), ('courtyard', 5, r(5))],
    'q3-b': [(f'reason-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-c': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q4-a': [(f'requirement-{i}', 8, r(8)) for i in (1, 2, 3)],
    'q4-b': [('foundation-1', 8, r(8)), ('details-1', 4, r(4)), ('foundation-2', 8, r(8)), ('details-2', 4, r(4))],
    'q4-c': [(k, 3, r(3)) for k in ['advantage-1', 'disadvantage-1', 'advantage-2', 'disadvantage-2']],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 21, list(range(0, 22, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [(k, 3, r(3)) for k in ['required-resistance', 'existing-resistance', 'difference', 'formula', 'thickness']],
    'q6-a': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-b': [('items', 20, None)],
    'q6-c': [(f'advantage-{i}', 5, r(5)) for i in (1, 2)],
    'q7-a': [('details', 45, r(45)), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q7-b': [('detail-1', 2, r(2)), ('detail-2', 2, r(2))],
    'q8-a': [(f'consideration-{i}', 5, r(5)) for i in (1, 2, 3)],
    'q8-b': [('components', 20, r(20)), ('valves', 4, r(4)), ('description', 5, r(5))],
    'q8-c-advantages': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q8-c-disadvantages': [('disadvantage-1', 4, r(4)), ('disadvantage-2', 4, r(4))],
    'q9-a': [(f'advantage-{i}', 6, r(6)) for i in (1, 2)],
    'q9-b': [('items', 36, None)],
    'q9-c': [('notes', 6, r(6)), ('sketches', 6, r(6))],
    'q10-a': [(f'benefit-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q10-b': [('sketch', 12, r(12)), ('orientation', 4, r(4)), ('sun-path', 4, r(4)), ('thermal-performance', 4, r(4))],
    'q10-c': [('thermal-mass', 10, r(10)), ('feature-1', 4, r(4)), ('feature-2', 4, r(4))],
    'q10-alt-a': [(f'point-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q10-alt-b': [(f'guideline-{i}', 10, r(10)) for i in (1, 2, 3)],
}
COMPOSITE = {
    'q1-complete': ['q1-a', 'q1-b'], 'q2-a': ['q2-a-entrance-access', 'q2-a-internal-corridor'], 'q2-complete': ['q2-a', 'q2-b', 'q2-c'],
    'q3-complete': ['q3-a', 'q3-b', 'q3-c'], 'q4-complete': ['q4-a', 'q4-b', 'q4-c'], 'q5-complete': ['q5-a', 'q5-b', 'q5-c'],
    'q6-complete': ['q6-a', 'q6-b', 'q6-c'], 'q7-complete': ['q7-a', 'q7-b'], 'q8-c': ['q8-c-advantages', 'q8-c-disadvantages'],
    'q8-complete': ['q8-a', 'q8-b', 'q8-c'], 'q9-complete': ['q9-a', 'q9-b', 'q9-c'], 'q10-complete': ['q10-a', 'q10-b', 'q10-c'],
    'q10-alt-complete': ['q10-alt-a', 'q10-alt-b'],
}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q2-a': 24, 'q8-c': 16, **{k: 60 for k in COMPOSITE if k.endswith('-complete')}})
LIFETIME = (['cons-1-2'], ['planning-sustainability-environment'])
SOLAR = (['cons-5-2', 'cons-6-4'], ['hot-water-space-heating', 'sustainability-the-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-10', 'cons-3-3', 'cons-3-4'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q1-b': (['cons-6-2', 'cons-3-10'], ['heat-loss-insulation', 'roofs']),
    'q2-a-entrance-access': LIFETIME, 'q2-a-internal-corridor': LIFETIME, 'q2-b': LIFETIME, 'q2-c': LIFETIME,
    'q3-a': (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-b': (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light']),
    'q3-c': (['cons-1-1', 'cons-1-2'], ['conservation-restoration', 'planning-sustainability-environment']),
    'q4-a': (['cons-2-2'], ['foundations']),
    'q4-b': (['cons-2-4', 'cons-2-5', 'cons-2-2'], ['foundations']),
    'q4-c': (['cons-2-4', 'cons-2-2'], ['foundations']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']),
    'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-1', 'cons-6-2'], ['heat-u-value-calculations', 'heat-loss-insulation']),
    'q6-a': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q6-b': (['cons-6-5', 'cons-6-2', 'cons-1-2'], ['condensation-air-tightness', 'heat-loss-insulation', 'planning-sustainability-environment']),
    'q6-c': (['cons-1-2', 'cons-6-5'], ['planning-sustainability-environment', 'condensation-air-tightness']),
    'q7-a': (['cons-1-5', 'cons-4-4', 'cons-4-3'], ['question-1-drawing-questions', 'stairs', 'floors']),
    'q7-b': (['cons-4-4'], ['stairs']),
    'q8-a': SOLAR, 'q8-b': SOLAR, 'q8-c-advantages': SOLAR, 'q8-c-disadvantages': SOLAR,
    'q9-a': (['cons-6-5'], ['condensation-air-tightness']),
    'q9-b': (['cons-6-5', 'cons-3-6', 'cons-3-9'], ['condensation-air-tightness', 'windows-light', 'roofs']),
    'q9-c': (['cons-6-5'], ['condensation-air-tightness']),
    'q10-a': (['cons-6-4'], ['passive-design']), 'q10-b': (['cons-6-4'], ['passive-design']),
    'q10-c': (['cons-6-4', 'cons-6-2'], ['passive-design', 'heat-loss-insulation']),
    'q10-alt-a': (['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'sustainability-the-environment']),
    'q10-alt-b': (['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'sustainability-the-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 53, 580, 410], False), 'q2-original': (P, 2, [45, 410, 580, 760], False),
    'q3-original': (P, 3, [45, 53, 580, 466], False), 'q4-original': (P, 3, [45, 466, 580, 765], False),
    'q5-original': (P, 4, [45, 53, 580, 720], False), 'q6-original': (P, 5, [45, 53, 580, 447], False),
    'q7-original': (P, 5, [45, 447, 580, 765], False), 'q8-original': (P, 6, [45, 53, 580, 413], False),
    'q9-original': (P, 6, [45, 413, 580, 760], False), 'q10-original': (P, 7, [45, 53, 580, 421], False),
    'q10-alt-original': (P, 7, [45, 495, 580, 715], False),
    'q1-section': composite((4, [51, 51, 545, 790]), (5, [51, 51, 545, 440])),
    'q1-thermal-bridge': (S, 5, [51, 465, 545, 775], True),
    'q2-entrance': (S, 6, [51, 51, 545, 470], True), 'q2-corridor': (S, 6, [51, 470, 545, 780], True),
    'q2-guidelines': (S, 6, [51, 51, 545, 780], True),
    'q2-areas': composite((7, [51, 51, 545, 790]), (8, [51, 51, 545, 330])),
    'q3-layout': (S, 9, [51, 51, 545, 780], True), 'q3-reasons': (S, 10, [51, 51, 545, 470], True),
    'q4-requirements': (S, 11, [51, 51, 545, 445], True),
    'q4-foundations': composite((11, [51, 445, 545, 731]), (12, [51, 51, 545, 580])),
    'q5-calculation': (S, 14, [51, 51, 545, 792], True), 'q5-insulation': (S, 15, [51, 51, 570, 300], True),
    'q6-low-impact': (S, 16, [51, 51, 545, 790], True),
    'q6-wellbeing': composite((17, [51, 51, 545, 790]), (18, [51, 51, 545, 450])),
    'q6-scheme': composite((16, [51, 51, 545, 790]), (17, [51, 51, 545, 790]), (18, [51, 51, 545, 450])),
    'q7-section': (S, 19, [51, 51, 545, 786], True),
    'q8-system': (S, 21, [51, 51, 545, 565], True),
    'q9-locations': composite((22, [51, 252, 545, 790]), (23, [51, 51, 545, 325])),
    'q9-test': (S, 23, [51, 330, 545, 770], True),
    'q10-orientation': (S, 24, [51, 280, 545, 704], True), 'q10-thermal-mass': (S, 25, [51, 51, 550, 795], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-thermal-bridge', 'q1-complete': 'q1-section',
            'q2-a-entrance-access': 'q2-entrance', 'q2-a-internal-corridor': 'q2-corridor', 'q2-a': 'q2-guidelines', 'q2-b': 'q2-areas',
            'q2-complete': 'q2-areas', 'q3-a': 'q3-layout', 'q3-b': 'q3-reasons', 'q3-complete': 'q3-layout',
            'q4-a': 'q4-requirements', 'q4-b': 'q4-foundations', 'q4-complete': 'q4-foundations',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-insulation', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-low-impact', 'q6-b': 'q6-wellbeing', 'q6-complete': 'q6-scheme',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section', 'q8-b': 'q8-system', 'q8-complete': 'q8-system',
            'q9-b': 'q9-locations', 'q9-c': 'q9-test', 'q9-complete': 'q9-locations',
            'q10-b': 'q10-orientation', 'q10-c': 'q10-thermal-mass', 'q10-complete': 'q10-orientation'}
CHOICE_FIGURE_PAGES = {'q6-b': {17, 18}, 'q6-complete': {16, 17, 18}, 'q9-b': {22, 23}, 'q9-complete': {22, 23}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}
SCHEME_PAGES = {'1': [4, 5, 29], '2': [6, 7, 8, 30], '3': [9, 10, 31], '4': [11, 12, 13, 32], '5': [14, 15, 33], '6': [16, 17, 18, 34],
                '7': [19, 35], '8': [20, 21, 36], '9': [22, 23, 37], '10': [24, 25, 38], '10-alt': [26, 27, 39]}
WORKED = [('q5-a', [14], ['0.012', '4.839', '0.005', '0.149', '0.055', '5.229', '0.191']),
          ('q5-b', [14], ['413.068', '9,324,000', '3,851,446.032', '103.118', '100.02']),
          ('q5-c', [15], ['8.333', '3.104', '0.096'])]
RUBRIC = 'Any four of ten questions, 60 marks each, 240 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
