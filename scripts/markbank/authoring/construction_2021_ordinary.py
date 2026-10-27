"""Source-pinned validator for the 2021 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card with its
eight per-term IDs withdrawn into it, selection words and the 18 pre-audit cards corrected in place),
checked by the shared engine construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2021_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2021, 'ordinary'
HASHES = ('58d741d2e4ac4bbbe000a5d8e056d8908291a8488fd9191010eb170fa96672b0', '88bb726b606474103cf4c1d04ef58cb78c1d4508f68a5bd766681cf40bc4c258')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 802
BAND8 = [0, 4, 6, 8]
Q8 = 'q8-None-joist-bridging'
TERMS = ['Joist bridging', 'Steel reinforcement', 'Biscuit joint', 'Working drawing', 'Heat pump', 'Room thermostat', 'Roof light', 'Ridge board', 'Building Energy Rating']
LEGACY = {'q1-a', 'q1-b', 'q2-a', 'q3-a', 'q3-b', 'q4-a', 'q4-b', 'q5-a', 'q5-b', 'q6-a', 'q6-b', 'q6-c', 'q7-b', 'q7-c', 'q9-a', 'q9-b', 'q9-c', Q8}
CONSOLIDATED = {f'q8-None-{t}': Q8 for t in ['steel-reinforcement', 'biscuit-joint', 'working-drawing', 'heat-pump', 'room-thermostat', 'roof-light',
                                            'ridge-board', 'building-energy-rating']}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
CHOICES.update({'q1-a': ('details', 7, 5, ["Breather membrane", "Rafters 200 mm × 50 mm", "Ceiling joist with insulation between joists", "Insulated plasterboard with skim coat", "Wallplate 100 mm × 75 mm", "Airtight membrane and tape", "Ventilation", "Tilting fillet, fascia, soffit and eaves gutter", "Concrete block inner leaf", "Concrete block outer leaf", "13 mm internal plaster and 19 mm render"]), 'q3-a': ('items', 8, 4, ["Mains water supply", "Water meter", "15 mm rising main", "Kitchen sink", "Connection to kitchen sink", "Ball-valve", "Cold water storage tank", "Insulation around storage tank", "28 mm overflow", "Pipe insulation", "Valves / pumps", "Annotation"]), 'q5-a': ('details', 7, 5, ["Concrete block outer leaf", "Full filled insulated cavity", "Wall ties", "Concrete block inner leaf", "13 mm internal plaster and 19 mm external render", "Cavity closer", "DPC", "Precast concrete window cill with throating / drip", "Window board", "Airtight tape", "Window frame 120 mm × 80 mm", "Triple glazing"])})  # drawing details as option groups (construction_choices.py)
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
TAILS = {'8': 'creating an outdoor living space.'}
LEDGER = [(1, 'Answer any'), (4, 'any five')]
GAPS = {Q8: {'cons-2-5', 'cons-10-1', 'cons-10-4'}}
LEAF = {
    'q1-a': [('details', 35, None), ('dimensions', 4, r(4)), ('presentation', 8, BAND8)],
    'q1-b': [('gutter', 3, [0, 3])],
    'q2-a': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q2-b': [('method', 16, r(16)), ('type', 5, r(5)), ('thickness', 5, r(5))],
    'q2-c': [('floor', 6, r(6)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q3-a': [('items', 32, None), ('presentation', 8, BAND8)],
    'q3-b': [('advantage-1', 5, r(5)), ('advantage-2', 5, r(5))],
    'q4-a': [('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q4-b': [('site-notice', 13, r(13)), ('location-map', 13, r(13))],
    'q4-c': [('advantage', 6, r(6)), ('disadvantage', 6, r(6))],
    'q5-a': [('details', 35, None), ('dimensions', 3, r(3)), ('presentation', 8, BAND8)],
    'q5-b': [('cill', 4, [0, 4])],
    'q6-a': [(k, 9, r(9)) for k in ['vest', 'boots', 'helmet']],
    'q6-b': [('risk-1', 5, r(5)), ('risk-2', 5, r(5))],
    'q6-c': [('precaution', 13, r(13))],
    'q7-a': [('sketch', 8, r(8)), ('access', 6, r(6)), ('advantage', 6, r(6))],
    'q7-b': [(k, 6, r(6)) for k in ['sofa-3', 'sofa-2', 'stove', 'television']],
    'q7-c': [('advantage', 6, r(6))],
    Q8: [('terms', 50, None)],
    'q9-a': [('finish', 4, r(4)), ('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q9-b': [('modification-1', 13, r(13)), ('modification-2', 13, r(13))],
    'q9-c': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'abc'), ('3', 'ab'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
PLAN = (['cons-1-3'], ['planning-sustainability-environment'])
LIVING = (['cons-1-2'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-8', 'cons-3-10', 'cons-3-9', 'cons-3-3'], ['question-one-drawing-questions', 'roofs', 'foundations-floors-walls']),
    'q1-b': (['cons-5-4'], ['drainage']),
    'q2-a': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q2-b': (['cons-4-2', 'cons-6-2'], ['foundations-floors-walls', 'heat-loss-insulation']),
    'q2-c': (['cons-4-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment']),
    'q3-a': (['cons-5-2', 'cons-5-1'], ['hot-water-space-heating', 'services-water-gas-electrical']),
    'q3-b': (['cons-5-1'], ['services-water-gas-electrical']),
    'q4-a': PLAN, 'q4-b': PLAN, 'q4-c': (['cons-1-2', 'cons-1-3'], ['planning-sustainability-environment']),
    'q5-a': (['cons-1-5', 'cons-3-3', 'cons-3-6', 'cons-3-4'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors']),
    'q5-b': (['cons-3-6', 'cons-3-4'], ['windows-doors', 'foundations-floors-walls']),
    'q6-a': (['cons-1-8'], ['site-safety']), 'q6-b': (['cons-1-8'], ['site-safety']), 'q6-c': (['cons-1-8'], ['site-safety']),
    'q7-a': LIVING, 'q7-b': LIVING, 'q7-c': (['cons-5-3', 'cons-5-7'], ['hot-water-space-heating', 'fire-places-fire-prevention']),
    Q8: (['cons-4-3', 'cons-2-5', 'cons-10-1', 'cons-10-4', 'cons-1-5', 'cons-5-3', 'cons-3-5', 'cons-3-9', 'cons-3-8', 'cons-6-3'],
         ['foundations-floors-walls', 'wood-rot-ventilation', 'question-one-drawing-questions', 'hot-water-space-heating', 'services-water-gas-electrical',
          'windows-doors', 'roofs', 'heat-loss-insulation']),
    'q9-a': (['cons-10-7'], ['wood-rot-ventilation']),
    'q9-b': LIVING, 'q9-c': LIVING,
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 297], False), 'q2-original': (P, 2, [45, 297, 580, 517], False),
    'q3-original': (P, 2, [45, 517, 580, 765], False), 'q4-original': (P, 3, [45, 39, 580, 295], False),
    'q5-original': (P, 3, [45, 295, 580, 536], False), 'q6-original': (P, 3, [45, 536, 580, 765], False),
    'q7-original': (P, 4, [45, 39, 580, 377], False), 'q8-original': (P, 4, [45, 377, 580, 475], False),
    'q9-original': (P, 4, [45, 511, 580, 765], False),
    'q1-scheme': (S, 4, [25, 58, 580, 760], True),
    'q2-advantages': (S, 5, [25, 58, 580, 222], True), 'q2-method': (S, 5, [25, 222, 580, 478], True), 'q2-floor': (S, 5, [25, 478, 580, 792], True),
    'q3-system': (S, 6, [25, 58, 580, 563], True), 'q3-meter': (S, 6, [25, 563, 580, 680], True),
    'q4-reasons': composite((7, [25, 58, 580, 116]), (7, [25, 116, 445, 236])), 'q4-documents': (S, 7, [25, 240, 580, 575], True), 'q4-town': (S, 7, [25, 575, 580, 790], True),
    'q5-scheme': (S, 8, [25, 58, 580, 645], True),
    'q6-signs': (S, 9, [25, 58, 580, 386], True), 'q6-risks': (S, 9, [25, 386, 580, 545], True), 'q6-trench': (S, 9, [25, 545, 580, 792], True),
    'q7-access': (S, 10, [25, 58, 580, 265], True),
    'q7-layout': composite((10, [25, 265, 580, 775]), (11, [25, 51, 580, 395])),
    'q7-stove': (S, 11, [25, 420, 580, 550], True),
    'q8-terms': composite((12, [25, 58, 580, 768]), (13, [25, 51, 580, 792])),
    'q9-finish': (S, 14, [25, 58, 580, 345], True), 'q9-winter': (S, 14, [25, 345, 580, 632], True), 'q9-advantages': (S, 14, [25, 606, 580, 760], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-advantages', 'q2-b': 'q2-method', 'q2-c': 'q2-floor', 'q2-complete': 'q2-method',
            'q3-a': 'q3-system', 'q3-b': 'q3-meter', 'q3-complete': 'q3-system',
            'q4-a': 'q4-reasons', 'q4-b': 'q4-documents', 'q4-c': 'q4-town', 'q4-complete': 'q4-documents',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-signs', 'q6-b': 'q6-risks', 'q6-c': 'q6-trench', 'q6-complete': 'q6-signs',
            'q7-a': 'q7-access', 'q7-b': 'q7-layout', 'q7-c': 'q7-stove', 'q7-complete': 'q7-layout', Q8: 'q8-terms',
            'q9-a': 'q9-finish', 'q9-b': 'q9-winter', 'q9-c': 'q9-advantages', 'q9-complete': 'q9-winter'}
CHOICE_FIGURE_PAGES = {Q8: {12, 13}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
SCHEME_PAGES = {'1': [4, 15], '2': [5, 16], '3': [6, 17], '4': [7, 18], '5': [8, 19], '6': [9, 20], '7': [10, 11, 21], '8': [12, 13, 22], '9': [14, 23]}
RUBRIC = 'Any three of nine questions, 50 marks each, 150 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
