"""Source-pinned validator for the 2018 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the added Q8 any-five card, the
Q9(c) advantage and disadvantage cards composed into (c), selection words, the 19 pre-audit cards corrected
in place and the three retired build overrides), checked by the shared engine construction_paper.validate
against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2018_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2018, 'ordinary'
HASHES = ('ed26d3fbdb863826bd485e22ece6b7aeabc53e70ff7dce447d623b75c98352c3', '7344fc028e7e7588c55886d87002958a42fe5b79a47980256560228d44000f9c')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 873
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
Q8 = 'q8-terms'
TERMS = ['Smart meter', 'Biscuit joint', 'Earth rod', 'Airtightness tape', 'Evacuated tube', 'Magnetic catch', 'Roof light window', 'Aerated shower', 'LED lighting']
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q4-a', 'q5-a', 'q5-b', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q7-c', 'q9-a', 'q9-b',
          'q9-c-advantage', 'q9-c-disadvantage'}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
CHOICES.update({'q1-a': ('details', 7, 5, ["15 mm internal plaster with skim coat", "120 × 50 mm doorframe", "60 mm flush panel door", "65 × 15 mm architrave and 100 × 15 mm skirting board", "20 mm tongue and groove floating hardwood floor", "100 mm smooth concrete floor", "250 mm floor insulation with thermal blocks", "200 mm concrete sub-floor", "Radon barrier", "30 mm sand blinding", "200 mm hardcore", "Reinforced concrete foundation", "215 mm concrete block wall"]), 'q3-a': ('items', 7, 5, ["15 mm rising main", "Water storage tank and overflow 22 mm min", "22 mm cold feed from water storage tank to hot water cylinder", "Hot water cylinder", "22 mm expansion pipe from hot water cylinder", "22 mm hot water supply to shower", "Wood-burning stove", "28 mm primary flow and return to and from wood-burning stove and hot", "22 mm cold feed from expansion tank and 22 mm expansion pipe", "Expansion tank and overflow 22 mm min"]), 'q5-a': ('details', 7, 5, ["Weather proofing three layers of bituminous felt", "Marine plywood decking 18 to 25 mm", "Battens/counter battens 50 mm × 50 mm and firring piece", "Roof/ceiling joists 200 mm × 50 mm", "Roof insulation min 200 mm", "12.5 mm insulated plasterboard with skim coat", "100 × 75 mm wallplate and wallplate straps", "Concrete block inner leaf 100 mm", "Full-fill cavity insulation and cavity closer with fire stopping insulation", "Concrete block outer leaf 100 mm", "15 mm internal plaster and 19 mm external render", "Fascia 25 mm, soffit 12 mm and eaves gutter 100 mm"])})  # drawing details as option groups (construction_choices.py)
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
TAILS = {'8': 'between the sitting room and the dining room.'}
LEDGER = [(1, 'Answer Question'), (4, 'any five')]
GAPS = {'q4-b': {'cons-2-1'}, Q8: {'cons-10-1', 'cons-10-4', 'cons-10-2'}}
RETIRED = [('card-source-bindings.json', 'q3-a'), ('card-corrections.json', 'q6-c'), ('card-corrections.json', 'q9-c-advantage')]
LEAF = {
    'q1-a': [('details', 35, None), ('dimensions', 3, r(3))],
    'q1-b': [('radon', 4, [0, 4]), ('presentation', 8, BAND8)],
    'q2-a': [('description-1', 4, r(4)), ('description-2', 4, r(4)), ('thickness', 4, r(4)), ('presentation', 8, BAND8)],
    'q2-b': [('step-1', 4, r(4)), ('step-2', 4, r(4)), ('finish', 4, r(4)), ('presentation', 8, BAND8)],
    'q2-c': [('advantage', 5, r(5)), ('disadvantage', 5, r(5))],
    'q3-a': [('items', 35, None), ('presentation', 8, BAND8)],
    'q3-b': [('advantage', 7, r(7))],
    'q4-a': [('detail-1', 5, r(5)), ('detail-2', 5, r(5))],
    'q4-b': [(k, 10, r(10)) for k in ['profiles', 'width-depth', 'wall-position']],
    'q4-c': [('level', 10, r(10))],
    'q5-a': [('details', 35, None), ('dimensions', 3, r(3))],
    'q5-b': [('ventilation', 4, [0, 4]), ('presentation', 8, BAND8)],
    'q6-a': [(k, 8, BAND8) for k in ['vest', 'footwear', 'helmet']],
    'q6-b': [(k, 3, r(3)) for k in ['vest', 'footwear', 'helmet']] + [('presentation', 8, BAND8)],
    'q6-c': [('item', 4, r(4)), ('reason', 5, r(5))],
    'q7-a': [('sketch', 4, r(4)), ('pipework', 4, r(4)), ('labels', 4, r(4)), ('presentation', 8, BAND8)],
    'q7-b': [('detail-1', 4, r(4)), ('detail-2', 4, r(4)), ('pump', 4, r(4)), ('valves', 4, r(4)), ('presentation', 8, BAND8)],
    'q7-c': [('advantage', 6, r(6))],
    Q8: [('terms', 50, None)],
    'q9-a': [('detail-1', 4, r(4)), ('detail-2', 4, r(4)), ('presentation', 6, BAND6)],
    'q9-b': [('square', 8, r(8)), ('square-presentation', 6, BAND6), ('fixing', 8, r(8)), ('fixing-presentation', 6, BAND6)],
    'q9-c-advantage': [('advantage', 4, r(4))],
    'q9-c-disadvantage': [('disadvantage', 4, r(4))],
}
COMPOSITE = {'q9-c': ['q9-c-advantage', 'q9-c-disadvantage']}
COMPOSITE.update({f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
                  [('1', 'ab'), ('2', 'abc'), ('3', 'ab'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]})
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q9-c': 8, **{k: 50 for k in COMPOSITE if k.endswith('-complete')}})
WALL = (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls'])
HEAT = (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating'])
SAFE = (['cons-1-8'], ['site-safety'])
DOORS = (['cons-3-7', 'cons-4-5'], ['windows-doors'])
GLAZED = (['cons-3-7', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-4-2', 'cons-3-7'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors']),
    'q1-b': (['cons-3-4', 'cons-4-2'], ['foundations-floors-walls']),
    'q2-a': WALL, 'q2-b': WALL, 'q2-c': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q3-a': HEAT, 'q3-b': (['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'planning-sustainability-environment']),
    'q4-a': (['cons-2-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment']),
    'q4-b': (['cons-2-4', 'cons-2-1'], ['foundations-floors-walls']), 'q4-c': (['cons-2-4'], ['foundations-floors-walls']),
    'q5-a': (['cons-1-5', 'cons-3-10', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls']),
    'q5-b': (['cons-3-10', 'cons-6-5'], ['roofs', 'wood-rot-ventilation']),
    'q6-a': SAFE, 'q6-b': SAFE, 'q6-c': SAFE,
    'q7-a': (['cons-5-4'], ['drainage']), 'q7-b': (['cons-5-2', 'cons-5-6'], ['services-water-gas-electrical', 'drainage']),
    'q7-c': (['cons-5-4', 'cons-1-2'], ['drainage', 'planning-sustainability-environment']),
    Q8: (['cons-5-8', 'cons-10-1', 'cons-10-4', 'cons-6-5', 'cons-5-2', 'cons-10-2', 'cons-3-5', 'cons-3-9'],
         ['services-water-gas-electrical', 'wood-rot-ventilation', 'air-tightness-condensation', 'hot-water-space-heating', 'windows-doors', 'roofs']),
    'q9-a': (['cons-3-4'], ['foundations-floors-walls']), 'q9-b': DOORS, 'q9-c-advantage': GLAZED, 'q9-c-disadvantage': GLAZED,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [35, 39, 580, 300], False), 'q2-original': (P, 2, [35, 305, 580, 556], False),
    'q3-original': (P, 2, [35, 565, 580, 775], False), 'q4-original': (P, 3, [35, 39, 580, 278], False),
    'q5-original': (P, 3, [35, 280, 580, 563], False), 'q6-original': (P, 3, [35, 570, 580, 783], False),
    'q7-original': (P, 4, [35, 39, 580, 336], False), 'q8-original': (P, 4, [35, 345, 580, 482], False),
    'q9-original': (P, 4, [35, 490, 580, 760], False),
    'q1-scheme': (S, 4, [25, 50, 580, 692], True),
    'q2-method': (S, 5, [25, 50, 580, 430], True), 'q2-finish': (S, 5, [25, 430, 580, 710], True), 'q2-advantages': (S, 6, [25, 50, 580, 390], True),
    'q3-system': composite((6, [25, 390, 580, 765]), (7, [25, 50, 580, 313])), 'q3-stove': (S, 7, [25, 313, 580, 517], True),
    'q4-environment': (S, 7, [25, 517, 580, 770], True), 'q4-setting-out': (S, 8, [25, 50, 580, 677], True), 'q4-level': (S, 9, [25, 50, 580, 230], True),
    'q5-scheme': composite((9, [25, 230, 580, 765]), (10, [25, 30, 580, 517])),
    'q6-signs': (S, 10, [25, 517, 580, 750], True), 'q6-features': (S, 11, [25, 50, 580, 730], True), 'q6-other': (S, 12, [25, 50, 580, 450], True),
    'q7-collection': (S, 12, [25, 450, 580, 730], True), 'q7-pumping': (S, 13, [25, 50, 580, 420], True), 'q7-advantage': (S, 13, [25, 420, 580, 577], True),
    'q8-terms': composite((13, [25, 577, 580, 780]), (14, [25, 50, 580, 745]), (15, [25, 50, 580, 783])),
    'q9-support': (S, 16, [25, 50, 580, 297], True), 'q9-frame': (S, 16, [25, 297, 580, 703], True), 'q9-glazed': (S, 17, [25, 50, 580, 386], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-method', 'q2-b': 'q2-finish', 'q2-c': 'q2-advantages', 'q2-complete': 'q2-method',
            'q3-a': 'q3-system', 'q3-b': 'q3-stove', 'q3-complete': 'q3-system',
            'q4-a': 'q4-environment', 'q4-b': 'q4-setting-out', 'q4-c': 'q4-level', 'q4-complete': 'q4-setting-out',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-features', 'q6-c': 'q6-other', 'q6-complete': 'q6-signs',
            'q7-a': 'q7-collection', 'q7-b': 'q7-pumping', 'q7-c': 'q7-advantage', 'q7-complete': 'q7-collection', Q8: 'q8-terms',
            'q9-a': 'q9-support', 'q9-b': 'q9-frame', 'q9-c-advantage': 'q9-glazed', 'q9-c-disadvantage': 'q9-glazed', 'q9-c': 'q9-glazed',
            'q9-complete': 'q9-frame'}
CHOICE_FIGURE_PAGES = {Q8: {13, 14, 15}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
SCHEME_PAGES = {'1': [4, 18], '2': [5, 6, 19], '3': [6, 7, 20], '4': [7, 8, 9, 21], '5': [9, 10, 22], '6': [10, 11, 12, 23], '7': [12, 13, 24], '8': [13, 14, 15, 25], '9': [16, 17, 26]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
