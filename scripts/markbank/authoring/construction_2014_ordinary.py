"""Source-pinned validator for the 2014 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card and selection
words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2014_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2014, 'ordinary'
HASHES = ('c333950b806be0bf31dc1c1ef365236fabf05f83e5c38eeb306e4cf9a4e69d7b', '96b23fa46e5860d21c3a83f2c29f56e4e7f228bd6a1acbe799aec65d3c9ac47f')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 966
BAND8 = [0, 4, 6, 8]
Q8 = 'q8-terms'
TERMS = ['Strip Foundation', 'Housing joint', 'Laser beam', 'Thermostatic Valve', 'Collar tie', 'Radon sump', 'Roof-light window', 'Smart meter', 'External ramp']
LEGACY = set()
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
CHOICES.update({'q1-a': ('details', 9, 4, ["External render – 19 mm", "150 cavity full fill insulation", "Cavity ties", "Internal leaf solid block – 100 mm", "Internal plaster – 15 mm", "Skirting board", "Floating tongued and grooved hardwood floor", "Acoustic layer or adhesive layer for fixing floor boards", "Plywood deck – 20 mm", "Adhesive tape to wall and plywood", "Floor joists 225 × 40 mm", "Plaster skim"]), 'q3-a': ('details', 9, 4, ["Rising main", "Cold water storage tank and ball valve", "Overflow", "Cold feed from storage to indirect hot water cylinder", "Indirect hot water cylinder", "Expansion pipe from cylinder", "Supply to sink", "Supply to expansion tank", "Expansion tank and ball valve", "Overflow", "Cold water feed and primary return", "Wood burning stove / back boiler", "Expansion pipe and primary flow", "Valves", "Insulation to water storage tank and pipework", "Labelling"]), 'q5-a': ('details', 6, 6, ["Ridge tile", "Ridge vent", "Ridge board – 300 mm × 32 mm", "Tiles", "Battens – 50 mm × 30 mm", "Vapour barrier/vapour diffusion membrane", "Rafters – 200 mm × 50 mm", "Collar tie – 150 - 200 mm × 50 mm", "Insulation", "Plasterboard", "Labelling"])})  # drawing details as option groups (construction_choices.py)
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
LEDGER = [(1, 'Answer Question'), (3, 'any five'), (3, 'one of')]
GAPS = {'q4-c': {'cons-4-1'}, Q8: {'cons-10-1', 'cons-10-4'}}
LEAF = {
    'q1-a': [('details', 36, None), ('dimensions', 4, r(4))],
    'q1-b': [('bridging', 2, [0, 2]), ('presentation', 8, BAND8)],
    'q2-a': [('description-1', 4, r(4)), ('description-2', 4, r(4)), ('insulation', 4, r(4)), ('presentation', 8, BAND8)],
    'q2-b': [('step-1', 4, r(4)), ('step-2', 4, r(4)), ('finish', 4, r(4)), ('presentation', 8, BAND8)],
    'q2-c': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q3-a': [('details', 36, None), ('presentation', 8, BAND8)],
    'q3-b': [('advantage-1', 3, r(3)), ('advantage-2', 3, r(3))],
    'q4-a': [(f'detail-{i}', 4, r(4)) for i in (1, 2, 3)] + [('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q4-b': [('detail', 6, r(6))],
    'q4-c': [(f'detail-{i}', 4, r(4)) for i in (1, 2, 3)] + [('presentation', 8, BAND8)],
    'q5-a': [('details', 36, None), ('dimensions', 3, r(3))],
    'q5-b': [('ventilation', 3, r(3)), ('presentation', 8, BAND8)],
    'q6-a': [(k, 8, BAND8) for k in ['helmet', 'vest', 'boots']],
    'q6-b': [(k, 4, r(4)) for k in ['helmet', 'vest', 'boots']],
    'q6-c': [('reason-1', 7, r(7)), ('reason-2', 7, r(7))],
    'q7-a': [(f'detail-{i}', 6, r(6)) for i in (1, 2, 3)] + [('presentation', 8, BAND8)],
    'q7-b': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4)), ('use-1', 4, r(4)), ('use-2', 4, r(4))],
    'q7-c': [('advantage', 4, r(4)), ('disadvantage', 4, r(4))],
    Q8: [('terms', 50, None)],
    'q9-a': [('presentation', 8, BAND8), ('sink', 4, r(4)), ('cooker', 4, r(4)), ('fridge', 4, r(4))],
    'q9-b': [('detail-1', 4, r(4)), ('detail-2', 4, r(4)), ('presentation', 8, BAND8)],
    'q9-c': [('granite', 4, r(4)), ('wood', 4, r(4)), ('preferred', 2, r(2)), ('reason-1', 2, r(2)), ('reason-2', 2, r(2))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'abc'), ('3', 'ab'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
SITE = (['cons-1-8'], ['site-safety'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-3', 'cons-4-3'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q1-b': (['cons-4-3'], ['foundations-floors-walls']),
    'q2-a': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-2', 'cons-3-2'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-c': (['cons-6-3', 'cons-6-2'], ['heat-loss-insulation']),
    'q3-a': (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating']),
    'q3-b': (['cons-6-4', 'cons-6-3'], ['planning-sustainability-environment', 'heat-loss-insulation']),
    'q4-a': (['cons-4-5'], ['windows-doors']),
    'q4-b': (['cons-5-8', 'cons-4-5'], ['services-water-gas-electrical', 'windows-doors']),
    'q4-c': (['cons-4-1'], ['foundations-floors-walls']),
    'q5-a': (['cons-1-5', 'cons-3-8', 'cons-3-9'], ['question-one-drawing-questions', 'roofs']),
    'q5-b': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q6-a': SITE, 'q6-b': SITE, 'q6-c': SITE,
    'q7-a': (['cons-5-4', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']),
    'q7-b': (['cons-1-2', 'cons-5-2'], ['planning-sustainability-environment', 'services-water-gas-electrical']),
    'q7-c': (['cons-5-1', 'cons-5-2'], ['services-water-gas-electrical']),
    Q8: (['cons-2-4', 'cons-10-1', 'cons-10-4', 'cons-10-7', 'cons-5-3', 'cons-3-8', 'cons-4-2', 'cons-3-4', 'cons-3-5', 'cons-3-6', 'cons-5-8', 'cons-1-2'],
         ['foundations-floors-walls', 'wood-rot-ventilation', 'hot-water-space-heating', 'roofs', 'windows-doors', 'services-water-gas-electrical', 'planning-sustainability-environment']),
    'q9-a': (['cons-1-2'], ['planning-sustainability-environment']),
    'q9-b': (['cons-10-7'], ['wood-rot-ventilation']),
    'q9-c': (['cons-10-7', 'cons-1-2'], ['wood-rot-ventilation', 'planning-sustainability-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 228], False), 'q2-original': (P, 2, [30, 230, 580, 422], False),
    'q3-original': (P, 2, [30, 424, 580, 627], False), 'q4-original': (P, 2, [30, 629, 580, 790], False),
    'q5-original': (P, 3, [30, 39, 580, 190], False), 'q6-original': (P, 3, [30, 192, 580, 337], False),
    'q7-original': (P, 3, [30, 339, 580, 508], False), 'q8-original': (P, 3, [30, 510, 580, 590], False),
    'q9-original': (P, 3, [30, 592, 580, 790], False),
    'q1-scheme': composite((4, [25, 45, 580, 722]), (5, [25, 45, 580, 775])),
    'q2-fixing': (S, 6, [25, 45, 580, 296], True), 'q2-finish': (S, 6, [25, 296, 580, 616], True), 'q2-advantages': (S, 6, [25, 616, 580, 775], True),
    'q3-system': (S, 7, [25, 45, 580, 513], True), 'q3-solar': (S, 7, [25, 513, 580, 690], True),
    'q4-partition': (S, 8, [25, 45, 580, 280], True), 'q4-socket': (S, 8, [25, 280, 580, 543], True),
    'q4-skim': composite((8, [25, 543, 580, 785]), (9, [25, 45, 580, 240])),
    'q5-scheme': composite((9, [25, 258, 580, 760]), (10, [25, 45, 580, 376])), 'q5-vent': (S, 10, [25, 376, 580, 440], True),
    'q6-signs': (S, 10, [25, 455, 580, 630], True), 'q6-reasons': composite((10, [25, 630, 580, 775]), (11, [25, 45, 580, 250])),
    'q6-visitors': (S, 11, [25, 252, 580, 490], True),
    'q7-collection': composite((11, [25, 500, 580, 775]), (12, [25, 45, 450, 196]), (12, [450, 100, 580, 297])), 'q7-uses': composite((12, [25, 196, 450, 297]), (12, [25, 297, 580, 515])),
    'q7-meter': (S, 12, [25, 515, 580, 775], True),
    'q8-terms': composite((13, [25, 45, 580, 775]), (14, [25, 45, 580, 775]), (15, [25, 45, 580, 340])),
    'q9-layout': (S, 15, [25, 352, 580, 790], True), 'q9-paint': composite((16, [25, 45, 580, 360]), (16, [25, 360, 450, 460]), (16, [450, 360, 580, 522])),
    'q9-worktop': composite((16, [25, 460, 450, 533]), (16, [25, 533, 580, 775]), (17, [25, 45, 580, 350])),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-fixing', 'q2-b': 'q2-finish', 'q2-c': 'q2-advantages', 'q2-complete': 'q2-fixing',
            'q3-a': 'q3-system', 'q3-b': 'q3-solar', 'q3-complete': 'q3-system',
            'q4-a': 'q4-partition', 'q4-b': 'q4-socket', 'q4-c': 'q4-skim', 'q4-complete': 'q4-partition',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-vent', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-reasons', 'q6-c': 'q6-visitors', 'q6-complete': 'q6-signs',
            'q7-a': 'q7-collection', 'q7-b': 'q7-uses', 'q7-c': 'q7-meter', 'q7-complete': 'q7-collection', Q8: 'q8-terms',
            'q9-a': 'q9-layout', 'q9-b': 'q9-paint', 'q9-c': 'q9-worktop', 'q9-complete': 'q9-layout'}
CHOICE_FIGURE_PAGES = {Q8: {13, 14, 15}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 2, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
SCHEME_PAGES = {'1': [4, 5, 18], '2': [6, 19], '3': [7, 20], '4': [8, 9, 21], '5': [9, 10, 22], '6': [10, 11, 23], '7': [11, 12, 24], '8': [13, 14, 15, 25], '9': [15, 16, 17, 26]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
