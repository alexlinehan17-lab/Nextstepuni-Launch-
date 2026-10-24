"""Source-pinned validator for the 2018 Higher Level Construction Studies theory paper (Q1-Q10 and the Q10 alternative).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q10(a) any-two card, the
Q4(b) site choice marked alike, selection words, the 27 pre-audit cards corrected in place and the retired
build override), checked by the shared engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2018_higher.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2018, 'higher'
HASHES = ('c719ee9d731d6897511c1f159d266a6a1323190112f29d9c12083b8c63685725', 'e511515f52851ffc803fd68b5f7e7b87709fc0523acf0149c684282bbd9f72a1')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 11)]
ALT = True
PRIOR_COUNT = 859
PRES = [0, 2, 3, 4, 5, 6, 7, 8]
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q3-c', 'q4-a', 'q4-b', 'q4-c', 'q5-a', 'q5-b', 'q5-c', 'q6-a', 'q6-b', 'q6-c',
          'q7-a', 'q7-b', 'q8-a', 'q8-b', 'q8-c', 'q9-a', 'q9-b', 'q9-c', 'q10-a', 'q10-c'}
CHOICES = {'q10-a': ('items', 2, 8, ['Space heating energy demand', 'Building form', 'Thermal bridging'])}
FINITE = {'10a': 'q10-a'}
MARKED_ALIKE = {'4b': dict(options=['site A', 'site B'], cardId='cons-2018-hl-q4-b')}
RETIRED = [('card-source-bindings.json', 'q9-b')]
LEDGER = [(1, 'Answer Question'), (2, 'or'), (2, 'answer fits'), (3, 'Select'), (7, 'any two'), (7, 'OR')]
LEAF = {
    'q1-a': [(k, 16, r(16)) for k in ['house-wall', 'roof', 'porch-wall']] + [('presentation', 8, PRES)],
    'q1-b': [('abutment', 4, r(4))],
    'q2-a': [(k, 4, r(4)) for k in ['cables', 'trench', 'roof']],
    'q2-b': [(k, 12, r(12)) for k in ['cables', 'trench', 'roof']],
    'q2-c': [(f'strategy-{i}', 4, r(4)) for i in (1, 2, 3)],
    'q3-a': [(f'consideration-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q3-b': [(k, 6, r(6)) for k in ['extension-note', 'extension-sketch', 'modification-note', 'modification-sketch']],
    'q3-c': [(f'discussion-{i}', 6, r(6)) for i in (1, 2, 3)],
    'q4-a': [('dwellings', 12, r(12)), ('site', 12, r(12))],
    'q4-b': [(f'consideration-{i}', 5, r(5)) for i in (1, 2, 3)],
    'q4-c': [('sketch', 15, r(15)), ('justification', 6, r(6))],
    'q5-a': [('tabulation', 3, r(3)), ('resistances', 21, list(range(0, 22, 3))), ('total-resistance', 3, [0, 3]), ('u-value', 3, [0, 3])],
    'q5-b': [(k, 3, r(3)) for k in ['heat-loss', 'duration', 'energy', 'oil', 'cost']],
    'q5-c': [(k, 3, r(3)) for k in ['required-resistance', 'existing-resistance', 'difference', 'formula', 'thickness']],
    'q6-a': [(k, 3, r(3)) for k in ['advantage-1', 'advantage-2', 'disadvantage-1', 'disadvantage-2']],
    'q6-b': [(f'feature-{i}', 10, r(10)) for i in (1, 2, 3)],
    'q6-c': [('modification-1', 6, r(6)), ('modification-2', 6, r(6)), ('justification-1', 3, r(3)), ('justification-2', 3, r(3))],
    'q7-a': [(k, 16, r(16)) for k in ['wall', 'door', 'floor']] + [('presentation', 8, PRES)],
    'q7-b': [('airtightness', 4, r(4))],
    'q8-a': [('items', 24, list(range(0, 25, 3))), ('sizes', 4, r(4))],
    'q8-b': [('feature-1', 8, r(8)), ('feature-2', 8, r(8)), ('discussion', 4, r(4))],
    'q8-c': [('consideration-1', 6, r(6)), ('consideration-2', 6, r(6))],
    'q9-a': [(f'requirement-{i}', 12, r(12)) for i in (1, 2, 3)],
    'q9-b': [('stability', 6, r(6)), ('stud-wall', 6, r(6)), ('labels', 6, r(6))],
    'q9-c': [('air-leakage', 6, r(6))],
    'q10-a': [('items', 16, None)],
    'q10-b': [(f'modification-{i}', 8, r(8)) for i in (1, 2, 3)] + [('justification', 4, r(4))],
    'q10-c': [(k, 4, r(4)) for k in ['sketch', 'orientation', 'sun-path', 'thermal-performance']],
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
SAFE = (['cons-1-8'], ['site-safety'])
WELL = (['cons-1-2', 'cons-7-4'], ['planning-sustainability-environment', 'windows-light'])
SITE = (['cons-1-3'], ['planning-sustainability-environment'])
HEAT = (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating'])
PASSIVE = (['cons-6-2', 'cons-6-4', 'cons-6-5'], ['passive-design'])
SUST = (['cons-1-2', 'cons-6-4'], ['sustainability-the-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-10', 'cons-3-9', 'cons-3-3', 'cons-3-2'], ['question-1-drawing-questions', 'roofs', 'walls']),
    'q1-b': (['cons-3-10', 'cons-3-4'], ['roofs', 'walls']),
    'q2-a': SAFE, 'q2-b': SAFE, 'q2-c': SAFE,
    'q3-a': WELL, 'q3-b': (['cons-1-2', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration']), 'q3-c': WELL,
    'q4-a': (['cons-1-3', 'cons-1-1'], ['planning-sustainability-environment', 'conservation-restoration']), 'q4-b': SITE,
    'q4-c': (['cons-1-3', 'cons-6-4'], ['planning-sustainability-environment']),
    'q5-a': (['cons-6-1'], ['heat-u-value-calculations']), 'q5-b': (['cons-6-3', 'cons-6-1'], ['heat-u-value-calculations']),
    'q5-c': (['cons-6-1', 'cons-6-2', 'cons-4-2'], ['heat-u-value-calculations', 'heat-loss-insulation', 'floors']),
    'q6-a': (['cons-1-2'], ['planning-sustainability-environment']), 'q6-b': (['cons-1-2', 'cons-3-3'], ['sustainability-the-environment', 'walls']),
    'q6-c': (['cons-1-2', 'cons-6-4', 'cons-6-2'], ['sustainability-the-environment']),
    'q7-a': (['cons-1-5', 'cons-3-7', 'cons-3-3', 'cons-4-3'], ['question-1-drawing-questions', 'doors', 'walls', 'floors']),
    'q7-b': (['cons-6-5', 'cons-4-3'], ['condensation-air-tightness', 'floors']),
    'q8-a': HEAT, 'q8-b': HEAT, 'q8-c': (['cons-5-7'], ['fireplaces-fire-prevention']),
    'q9-a': (['cons-3-9', 'cons-1-9'], ['roofs', 'fireplaces-fire-prevention']), 'q9-b': (['cons-3-8', 'cons-3-9', 'cons-4-5'], ['roofs', 'doors']),
    'q9-c': (['cons-6-5', 'cons-3-9'], ['condensation-air-tightness', 'roofs']),
    'q10-a': (['cons-6-2', 'cons-6-3', 'cons-6-4'], ['passive-design', 'heat-loss-insulation']), 'q10-b': PASSIVE,
    'q10-c': (['cons-6-4'], ['passive-design', 'planning-sustainability-environment']),
    'q10-alt-discussion': SUST, 'q10-alt-guidelines': SUST,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 53, 580, 395], False), 'q2-original': (P, 2, [30, 510, 580, 730], False),
    'q3-original': (P, 3, [30, 65, 580, 415], False), 'q4-original': (P, 3, [30, 460, 580, 790], False),
    'q5-original': (P, 4, [30, 39, 580, 700], False), 'q6-original': (P, 5, [30, 39, 580, 495], False),
    'q7-original': (P, 5, [30, 530, 580, 775], False), 'q8-original': (P, 6, [30, 39, 580, 285], False),
    'q9-original': (P, 6, [30, 390, 580, 650], False), 'q10-original': (P, 7, [30, 39, 580, 420], False),
    'q10-alt-original': (P, 7, [30, 515, 580, 720], False),
    'q1-section': composite((4, [45, 56, 575, 790]), (5, [45, 56, 575, 555])),
    'q2-guidelines': composite((6, [45, 265, 575, 805]), (7, [45, 56, 575, 795])),
    'q3-considerations': (S, 8, [45, 450, 575, 780], True), 'q3-layout': (S, 9, [45, 56, 575, 795], True), 'q3-meets': (S, 10, [45, 56, 575, 410], True),
    'q4-characteristics': composite((10, [45, 420, 575, 795]), (11, [45, 56, 575, 280])),
    'q4-sites': composite((11, [45, 305, 575, 740]), (12, [45, 56, 575, 170])), 'q4-layout': (S, 12, [45, 180, 575, 625], True),
    'q5-calculation': (S, 13, [45, 56, 575, 760], True), 'q5-thickness': (S, 14, [45, 56, 575, 280], True),
    'q6-self-build': (S, 14, [45, 300, 575, 640], True), 'q6-features': composite((14, [45, 645, 575, 805]), (15, [45, 56, 575, 270])),
    'q6-modifications': composite((15, [45, 280, 575, 790]), (16, [45, 56, 575, 595])),
    'q7-section': (S, 17, [45, 56, 575, 795], True),
    'q8-layout': (S, 18, [45, 56, 575, 400], True), 'q8-safety': composite((18, [45, 405, 575, 800]), (19, [45, 56, 575, 180])),
    'q8-chimney': (S, 19, [45, 190, 575, 485], True),
    'q9-requirements': composite((19, [45, 530, 575, 790]), (20, [45, 56, 575, 480])),
    'q9-structure': composite((20, [45, 495, 575, 795]), (21, [45, 56, 575, 140])), 'q9-air-leakage': (S, 21, [45, 148, 575, 255], True),
    'q10-principles': composite((21, [45, 265, 575, 800]), (22, [45, 56, 575, 775])),
    'q10-modifications': (S, 23, [45, 56, 575, 603], True), 'q10-orientation': composite((23, [45, 603, 575, 790]), (24, [45, 56, 575, 400])),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-b': 'q2-guidelines', 'q2-complete': 'q2-guidelines',
            'q3-a': 'q3-considerations', 'q3-b': 'q3-layout', 'q3-c': 'q3-meets', 'q3-complete': 'q3-layout',
            'q4-a': 'q4-characteristics', 'q4-b': 'q4-sites', 'q4-c': 'q4-layout', 'q4-complete': 'q4-layout',
            'q5-a': 'q5-calculation', 'q5-b': 'q5-calculation', 'q5-c': 'q5-thickness', 'q5-complete': 'q5-calculation',
            'q6-a': 'q6-self-build', 'q6-b': 'q6-features', 'q6-c': 'q6-modifications', 'q6-complete': 'q6-features',
            'q7-a': 'q7-section', 'q7-b': 'q7-section', 'q7-complete': 'q7-section',
            'q8-a': 'q8-layout', 'q8-b': 'q8-safety', 'q8-c': 'q8-chimney', 'q8-complete': 'q8-layout',
            'q9-a': 'q9-requirements', 'q9-b': 'q9-structure', 'q9-c': 'q9-air-leakage', 'q9-complete': 'q9-structure',
            'q10-a': 'q10-principles', 'q10-b': 'q10-modifications', 'q10-c': 'q10-orientation', 'q10-complete': 'q10-principles'}
CHOICE_FIGURE_PAGES = {'q10-a': {21, 22}, 'q10-complete': {21, 22}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 3, '4': 3, '5': 4, '6': 5, '7': 5, '8': 6, '9': 6, '10': 7, '10-alt': 7}
SCHEME_PAGES = {'1': [4, 5, 28], '2': [5, 6, 7, 8, 29], '3': [8, 9, 10, 30], '4': [10, 11, 12, 31], '5': [13, 14, 32], '6': [14, 15, 16, 33],
                '7': [17, 34], '8': [18, 19, 35], '9': [19, 20, 21, 36], '10': [21, 22, 23, 24, 37], '10-alt': [24, 25, 26, 38]}
WORKED = [('q5-a', [13], ['0.0355', '0.0781', '0.2500', '0.1481', '0.1875', '0.8042', '1.2434']),
          ('q5-b', [13], ['1432.3968', '9,576,000', '367.24', '352.5']),
          ('q5-c', [14], ['6.6666', '5.8624', '0.2169088'])]
RUBRIC = 'Question 1 and any four of the other nine questions, 60 marks each, 300 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
