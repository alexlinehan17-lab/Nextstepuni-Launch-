"""Source-pinned validator for the 2020 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card with its
eight per-term IDs withdrawn into it, selection words, the 21 pre-audit cards corrected in place and the
retired card-source-bindings override), checked by the shared engine construction_paper.validate against
the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2020_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2020, 'ordinary'
HASHES = ('a35744b1da7e9a1108d6d061ebb37756af8904d0bb132e54612d729c05ec4202', '774f5fc6fc917e7f1e6c0e24ba6c896faf5b0327d224b1fe2cad7af9bb6c23fa')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 828
BAND8 = [0, 4, 6, 8]
Q8 = 'q8-None-stud-partition'
TERMS = ['Stud partition', 'Domino joint', 'Slump test', 'Dynamic glass', 'Pyrite', 'Pile foundation', 'Trimmer', 'Butt hinge', 'Solar Panel']
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q4-a', 'q4-c', 'q5-a', 'q5-b', 'q6-a', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q7-c',
          'q9-a', 'q9-b', 'q9-c', Q8}
CONSOLIDATED = {f'q8-None-{t}': Q8 for t in ['domino-joint', 'slump-test', 'dynamic-glass', 'pyrite', 'pile-foundation', 'trimmer', 'butt-hinge', 'solar-panel']}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
CHOICES.update({'q1-a': ('details', 7, 5, ["Reinforced strip foundation 1200 mm x 400 mm", "Concrete fill / foundation blocks", "Hardcore and sand blinding", "1200-gauge damp proof course/radon barrier", "200 - 300 mm Floor insulation", "Floor tiles 20 mm", "Skirting board", "Concrete block inner leaf with 13 mm internal plaster", "200 mm Full fill cavity insulation", "Wall ties", "Concrete block outer leaf with 19 mm render"]), 'q3-a': ('items', 8, 5, ["15 mm cold feed to burner", "22 mm flow to radiators", "22 mm return from radiators", "Radiators", "22 mm primary flow to cylinder", "22 mm primary return to burner", "22 mm overflow pipe", "22 mm expansion pipe from cylinder", "Valves / pumps"]), 'q5-a': ('details', 7, 5, ["Ridge tile", "Ridge vent", "Roofing slates", "Battens 50 mm x 35 mm", "Breather membrane", "Ridge board 275 mm x 32 mm", "Rafter 200 mm x 50 mm", "Collar tie 200 mm x 50 mm", "Insulation between rafters", "Airtight membrane", "Insulated plasterboard", "Plaster skim"])})  # drawing details as option groups (construction_choices.py)
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
TAILS = {'8': 'entering the dwelling.'}
LEDGER = [(1, 'Answer Question'), (4, 'any five')]
GAPS = {'q9-b': {'cons-7-4'}, 'q9-c': {'cons-7-4'}}
RETIRED = [('card-source-bindings.json', 'q7-b')]
LEAF = {
    'q1-a': [('details', 35, None), ('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q1-b': [('membrane', 3, [0, 3])],
    'q2-a': [('method', 16, r(16)), ('type', 5, r(5)), ('thickness', 5, r(5))],
    'q2-b': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q2-c': [('additional', 16, r(16))],
    'q3-a': [('items', 40, None), ('presentation', 6, [0, 2, 4, 6])],
    'q3-b': [('advantage', 4, r(4))],
    'q4-a': [('reason-1', 8, r(8)), ('reason-2', 8, r(8))],
    'q4-b': [('material-1', 4, r(4)), ('material-2', 4, r(4)), ('reuse-1', 5, r(5)), ('reuse-2', 5, r(5))],
    'q4-c': [('method', 16, r(16))],
    'q5-a': [('details', 35, None), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q5-b': [('ventilation', 4, [0, 4])],
    'q6-a': [(k, 8, r(8)) for k in ['sign-1', 'sign-2', 'sign-3']],
    'q6-b': [('precaution-1', 9, r(9)), ('precaution-2', 9, r(9))],
    'q6-c': [('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q7-a': [('sketch', 6, r(6))] + [(k, 6, r(6)) for k in ['toilet', 'wash-basin', 'shower']],
    'q7-b': [('location-1', 6, r(6)), ('reason-1', 4, r(4)), ('location-2', 6, r(6)), ('reason-2', 4, r(4))],
    'q7-c': [('advantage', 6, r(6))],
    Q8: [('terms', 50, None)],
    'q9-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q9-b': [('modification-1', 13, r(13)), ('modification-2', 13, r(13))],
    'q9-c': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'abc'), ('3', 'ab'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
WASTE = (['cons-1-2', 'cons-1-8'], ['planning-sustainability-environment', 'site-safety'])
SAFE = (['cons-1-8'], ['site-safety'])
ACCESS = (['cons-1-2'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q1-b': (['cons-3-4', 'cons-4-2'], ['foundations-floors-walls']),
    'q2-a': (['cons-3-3', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation']),
    'q2-b': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q2-c': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q3-a': (['cons-5-3', 'cons-5-2'], ['hot-water-space-heating']),
    'q3-b': (['cons-5-3'], ['hot-water-space-heating']),
    'q4-a': WASTE, 'q4-b': (['cons-1-2'], ['planning-sustainability-environment']), 'q4-c': WASTE,
    'q5-a': (['cons-1-5', 'cons-3-8', 'cons-3-9'], ['question-one-drawing-questions', 'roofs']),
    'q5-b': (['cons-3-9', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q6-a': SAFE, 'q6-b': SAFE, 'q6-c': SAFE,
    'q7-a': (['cons-5-6', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']), 'q7-b': ACCESS, 'q7-c': ACCESS,
    Q8: (['cons-4-5', 'cons-10-3', 'cons-2-7', 'cons-3-6', 'cons-4-2', 'cons-2-4', 'cons-4-3', 'cons-3-7', 'cons-3-5', 'cons-6-4', 'cons-5-3', 'cons-5-8'],
         ['foundations-floors-walls', 'windows-doors', 'wood-rot-ventilation', 'concrete', 'services-water-gas-electrical', 'planning-sustainability-environment']),
    'q9-a': (['cons-1-2'], ['planning-sustainability-environment']),
    'q9-b': (['cons-7-4', 'cons-3-5'], ['planning-sustainability-environment', 'windows-doors']),
    'q9-c': (['cons-7-4', 'cons-6-4'], ['planning-sustainability-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 280], False), 'q2-original': (P, 2, [45, 280, 580, 497], False),
    'q3-original': (P, 2, [45, 497, 580, 765], False), 'q4-original': (P, 3, [45, 39, 580, 276], False),
    'q5-original': (P, 3, [45, 276, 580, 532], False), 'q6-original': (P, 3, [45, 532, 580, 765], False),
    'q7-original': (P, 4, [45, 39, 580, 375], False), 'q8-original': (P, 4, [45, 375, 580, 500], False),
    'q9-original': (P, 4, [45, 515, 580, 765], False),
    'q1-scheme': (S, 4, [25, 58, 580, 760], True),
    'q2-method': (S, 5, [25, 58, 580, 478], True), 'q2-advantages': (S, 5, [25, 357, 465, 478], True), 'q2-additional': (S, 5, [25, 478, 580, 795], True),
    'q3-system': (S, 6, [25, 58, 580, 660], True), 'q3-underfloor': (S, 6, [25, 660, 580, 785], True),
    'q4-reasons': (S, 7, [25, 58, 580, 234], True), 'q4-materials': (S, 7, [25, 234, 580, 520], True), 'q4-storage': (S, 7, [25, 520, 580, 795], True),
    'q5-scheme': (S, 8, [25, 58, 580, 735], True),
    'q6-signs': (S, 9, [25, 58, 580, 755], True), 'q6-heights': (S, 10, [25, 58, 580, 592], True), 'q6-training': (S, 10, [25, 592, 580, 770], True),
    'q7-layout': (S, 11, [25, 58, 580, 780], True), 'q7-grab-rails': (S, 12, [25, 58, 580, 535], True), 'q7-advantage': (S, 12, [25, 535, 580, 705], True),
    'q8-terms': composite((13, [25, 58, 580, 768]), (14, [25, 58, 580, 718]), (15, [25, 58, 580, 750])),
    'q9-reasons': (S, 16, [25, 58, 580, 236], True), 'q9-light': (S, 16, [25, 236, 580, 636], True), 'q9-advantages': (S, 16, [25, 636, 580, 780], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-method', 'q2-b': 'q2-advantages', 'q2-c': 'q2-additional', 'q2-complete': 'q2-method',
            'q3-a': 'q3-system', 'q3-b': 'q3-underfloor', 'q3-complete': 'q3-system',
            'q4-a': 'q4-reasons', 'q4-b': 'q4-materials', 'q4-c': 'q4-storage', 'q4-complete': 'q4-storage',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-heights', 'q6-c': 'q6-training', 'q6-complete': 'q6-signs',
            'q7-a': 'q7-layout', 'q7-b': 'q7-grab-rails', 'q7-c': 'q7-advantage', 'q7-complete': 'q7-layout', Q8: 'q8-terms',
            'q9-a': 'q9-reasons', 'q9-b': 'q9-light', 'q9-c': 'q9-advantages', 'q9-complete': 'q9-light'}
CHOICE_FIGURE_PAGES = {Q8: {13, 14, 15}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
SCHEME_PAGES = {'1': [4, 18], '2': [5, 19], '3': [6, 20], '4': [7, 21], '5': [8, 22], '6': [9, 10, 23], '7': [11, 12, 24], '8': [13, 14, 15, 25], '9': [16, 26]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
