"""Source-pinned validator for the 2010 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the Q8 any-five card and selection
words; the paper was never carded, so every task is added), checked by the shared engine
construction_paper.validate against the pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2010_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2010, 'ordinary'
HASHES = ('e3dc8aa0f218165fb0a4c9e834df5d1aedfb899f064773d95a3f0456f8f2e7d2', '6601a161493382099d7cd0e7e43e2a5ac7fd6a014cc4b680c51dacbee436297e')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 1232
Q8 = 'q8-terms'
TERMS = ['Concrete lintel', 'Mortice and tenon joint', 'Energy rating', 'Door saddle', 'Quarter sawing', 'Ridge board', 'Triple glazing', 'Window cill', 'Vapour barrier']
LEGACY = set()
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
CHOICES.update({'q1-a': ('details', 7, 5, ["19 mm external render and 13 mm internal plaster", "100 mm concrete block outer leaf", "D.P.C", "50 mm residual cavity", "Wall tie", "100 mm thermal insulation", "100mm concrete block inner leaf", "Skirting board 120 x 20 mm", "20 mm quarry tiles with seal between wall and floor", "150 mm concrete floor", "150 mm floor insulation", "D.P.M. /radon barrier", "Hardcore and sand blinding", "Concrete fill / foundation blocks", "Reinforced concrete foundation"]), 'q3-a': ('details', 9, 4, ["15 mm rising main with stop valve", "Insulated storage tank and ballvalve", "22 mm overflow", "22 mm cold feed with insulation from storage tank to hot water cylinder", "Insulated indirect hot water cylinder", "22 mm hot water supply", "Insulated expansion tank with ballvalve", "22 mm cold feed with insulation from expansion tank", "28 mm primary return", "Wood burning stove / back boiler", "28 mm primary flow", "22 mm expansion pipe with insulation", "Valves"]), 'q5-a': ('details', 9, 4, ["Plasterboard ceiling", "225 x 50 mm ceiling joists", "Tongued and grooved floor", "Door saddle", "120 x 20 mm skirting board", "70 x 20 mm architrave", "Internal door", "110 x 44 mm door frame", "70 x 20 mm architrave", "120 x 20 mm skirting board"])})  # drawing details as option groups (construction_choices.py)
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
LEDGER = [(1, 'Answer Question'), (3, 'any five'), (3, 'one of'), (3, 'one of')]
TAILS = {'8': ('repainting a window frame in one of the houses.', 'any five of the following:')}  # Q8's bullets follow Q9 in the text layer
GAPS = {Q8: {'cons-10-1', 'cons-10-4'}}
LEAF = {
    'q1-a': [('details', 35, None), ('dimensions', 4, r(4)), ('presentation', 8, r(8))],
    'q1-b': [('cold-bridge', 3, r(3))],
    'q2-a': [('description-1', 4, r(4)), ('description-2', 4, r(4)), ('insulation', 4, r(4)), ('detail', 4, r(4)), ('presentation', 5, r(5))],
    'q2-b': [('advantage', 4, r(4)), ('disadvantage', 4, r(4))],
    'q2-c': [('detail-1', 4, r(4)), ('detail-2', 4, r(4)), ('insulation', 4, r(4)), ('thickness', 4, r(4)), ('presentation', 5, r(5))],
    'q3-a': [('details', 36, None), ('presentation', 6, r(6))],
    'q3-b': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q4-a': [('description-1', 3, r(3)), ('description-2', 3, r(3)), ('sketch', 4, r(4)), ('presentation', 5, r(5))],
    'q4-b': [('description-1', 3, r(3)), ('description-2', 3, r(3)), ('sketch', 4, r(4)), ('presentation', 5, r(5))],
    'q4-c': [('hinge', 5, r(5)), ('detail-1', 3, r(3)), ('detail-2', 3, r(3)), ('sketch', 4, r(4)), ('presentation', 5, r(5))],
    'q5-a': [('details', 36, None), ('presentation', 8, r(8))],
    'q5-b': [('sound', 6, r(6))],
    'q6-a': [(k, 14, r(14)) for k in ['ladder', 'veneer', 'jigsaw']],
    'q6-b': [('precaution-1', 2, r(2)), ('precaution-2', 2, r(2)), ('presentation', 4, r(4))],
    'q7-a': [('gutter', 4, r(4)), ('downpipe', 4, r(4)), ('presentation', 5, r(5)), ('description-1', 4, r(4)), ('description-2', 4, r(4))],
    'q7-b': [('tank', 4, r(4)), ('filter', 4, r(4)), ('presentation', 5, r(5)), ('description-1', 4, r(4)), ('description-2', 4, r(4))],
    'q7-c': [('use-1', 4, r(4)), ('use-2', 4, r(4))],
    Q8: [('terms', 50, None)],
    'q9-a': [('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q9-b': [('cleaning', 4, r(4)), ('pins', 4, r(4)), ('glazing', 4, r(4)), ('details', 4, r(4)), ('presentation', 5, r(5))],
    'q9-c': [('removal', 4, r(4)), ('preparation', 4, r(4)), ('painting', 4, r(4)), ('details', 4, r(4)), ('presentation', 5, r(5))],
}
COMPOSITE = {f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
             [('1', 'ab'), ('2', 'abc'), ('3', 'ab'), ('4', 'abc'), ('5', 'ab'), ('6', 'ab'), ('7', 'abc'), ('9', 'abc')]}
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({k: 50 for k in COMPOSITE})
DOOR = (['cons-4-5'], ['windows-doors'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-2-4', 'cons-3-3', 'cons-4-2'], ['question-one-drawing-questions', 'foundations-floors-walls']),
    'q1-b': (['cons-6-2', 'cons-4-2'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-a': (['cons-6-2', 'cons-3-3'], ['heat-loss-insulation', 'foundations-floors-walls']),
    'q2-b': (['cons-6-2', 'cons-6-3'], ['heat-loss-insulation']),
    'q2-c': (['cons-3-9', 'cons-6-2', 'cons-5-2'], ['roofs', 'heat-loss-insulation', 'hot-water-space-heating']),
    'q3-a': (['cons-5-2', 'cons-5-3'], ['hot-water-space-heating']),
    'q3-b': (['cons-5-3', 'cons-1-2'], ['hot-water-space-heating', 'planning-sustainability-environment']),
    'q4-a': (['cons-4-5', 'cons-10-7'], ['windows-doors', 'wood-rot-ventilation']), 'q4-b': DOOR,
    'q4-c': (['cons-4-5', 'cons-3-7'], ['windows-doors']),
    'q5-a': (['cons-1-5', 'cons-4-5', 'cons-4-3'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q5-b': (['cons-8-3', 'cons-4-5'], ['sound', 'windows-doors']),
    'q6-a': (['cons-1-8', 'cons-9-4'], ['site-safety']), 'q6-b': (['cons-9-4'], ['site-safety']),
    'q7-a': (['cons-5-4', 'cons-3-10'], ['drainage', 'roofs']), 'q7-b': (['cons-5-4', 'cons-5-5'], ['drainage']),
    'q7-c': (['cons-1-2', 'cons-5-2'], ['planning-sustainability-environment', 'services-water-gas-electrical']),
    Q8: (['cons-3-4', 'cons-2-6', 'cons-10-1', 'cons-10-4', 'cons-6-3', 'cons-3-7', 'cons-10-3', 'cons-3-8', 'cons-3-6', 'cons-6-2', 'cons-6-6'],
         ['foundations-floors-walls', 'concrete', 'wood-rot-ventilation', 'heat-loss-insulation', 'windows-doors', 'roofs', 'air-tightness-condensation']),
    'q9-a': (['cons-1-2', 'cons-3-5'], ['planning-sustainability-environment', 'windows-doors']),
    'q9-b': (['cons-3-6'], ['windows-doors']),
    'q9-c': (['cons-10-7', 'cons-3-5'], ['wood-rot-ventilation', 'windows-doors']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [30, 39, 580, 201], False), 'q2-original': (P, 2, [30, 201, 580, 414], False),
    'q3-original': (P, 2, [30, 414, 580, 610], False), 'q4-original': (P, 2, [30, 610, 580, 790], False),
    'q5-original': (P, 3, [30, 39, 580, 207], False), 'q6-original': (P, 3, [30, 207, 580, 336], False),
    'q7-original': (P, 3, [30, 336, 580, 510], False), 'q8-original': (P, 3, [30, 510, 580, 606], False),
    'q9-original': (P, 3, [30, 606, 580, 790], False),
    'q1-section': (S, 4, [25, 45, 580, 778], True),
    'q2-injecting': (S, 5, [25, 45, 580, 270], True), 'q2-pros-cons': (S, 5, [25, 270, 580, 513], True),
    'q2-attic': composite((5, [25, 513, 580, 778]), (6, [25, 45, 580, 249])),
    'q3-system': (S, 6, [25, 249, 580, 604], True), 'q3-advantages': (S, 6, [25, 604, 580, 778], True),
    'q4-scheme': (S, 7, [25, 45, 580, 563], True),
    'q5-scheme': (S, 8, [25, 45, 580, 470], True),
    'q6-precautions': composite((8, [25, 470, 580, 778]), (9, [25, 45, 580, 413])), 'q6-outdoors': (S, 9, [25, 413, 580, 778], True),
    'q7-scheme': (S, 10, [25, 45, 580, 520], True), 'q7-uses': (S, 10, [25, 520, 580, 778], True),
    'q8-terms': composite((11, [25, 45, 580, 778]), (12, [25, 45, 580, 778])),
    'q9-reasons': (S, 13, [25, 45, 580, 193], True), 'q9-glass': (S, 13, [25, 193, 580, 453], True), 'q9-paint': (S, 13, [25, 453, 580, 778], True),
}
SOLUTION = {'q1-a': 'q1-section', 'q1-b': 'q1-section', 'q1-complete': 'q1-section',
            'q2-a': 'q2-injecting', 'q2-b': 'q2-pros-cons', 'q2-c': 'q2-attic', 'q2-complete': 'q2-injecting',
            'q3-a': 'q3-system', 'q3-b': 'q3-advantages', 'q3-complete': 'q3-system',
            'q4-a': 'q4-scheme', 'q4-b': 'q4-scheme', 'q4-c': 'q4-scheme', 'q4-complete': 'q4-scheme',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a': 'q6-precautions', 'q6-b': 'q6-outdoors', 'q6-complete': 'q6-precautions',
            'q7-a': 'q7-scheme', 'q7-b': 'q7-scheme', 'q7-c': 'q7-uses', 'q7-complete': 'q7-scheme', Q8: 'q8-terms',
            'q9-a': 'q9-reasons', 'q9-b': 'q9-glass', 'q9-c': 'q9-paint', 'q9-complete': 'q9-glass'}
CHOICE_FIGURE_PAGES = {Q8: {11, 12}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 2, '5': 3, '6': 3, '7': 3, '8': 3, '9': 3}
SCHEME_PAGES = {'1': [4, 14], '2': [5, 6, 15], '3': [6, 16], '4': [7, 17], '5': [8, 18], '6': [8, 9, 19], '7': [10, 20], '8': [11, 12, 21], '9': [13, 22]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
