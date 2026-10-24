"""Source-pinned validator for the 2019 Ordinary Level Construction Studies theory paper (Q1-Q9).

The paper's own expected structure (rows, tariffs, steps, topics, figures, the added Q8 any-five card, the
two Q6(a) situation cards composed into (a), selection words, the 21 pre-audit cards corrected in place and
the three retired build overrides), checked by the shared engine construction_paper.validate against the
pinned SEC paper and scheme.
Run: python3 scripts/markbank/authoring/construction_2019_ordinary.py
"""
import construction_paper as cp
from construction_paper import r

YEAR, LEVEL = 2019, 'ordinary'
HASHES = ('2b3c07cfadcfded21bfd0a773f877a9d648f7c05cf990be01c0f44e981ec78d2', '7545b54efb409c3f339f58869873772e0dad225735af6d1733d213571529455d')
P, S = cp.sources(YEAR, LEVEL)
QUESTIONS = [str(i) for i in range(1, 10)]
PRIOR_COUNT = 847
BAND8 = [0, 4, 6, 8]
BAND6 = [0, 2, 4, 6]
Q8 = 'q8-terms'
Q6A = ['using-a-contact-adhesive-to-glue-veneers', 'using-a-battery-powered-screwdriver']
TERMS = ['Carbon monoxide alarm', 'Grab rail', 'Furniture castor', 'Laminated safety glass', 'Eaves gutter', 'Balusters', 'Sapwood', 'Bridle joint',
         'Fluorescent lighting']
LEGACY = {'q1-a', 'q1-b', 'q2-b', 'q2-c', 'q3-a', 'q3-b', 'q3-c', 'q4-b', 'q4-c', 'q5-a', 'q5-b', 'q6-b', 'q6-c', 'q7-a', 'q7-b', 'q7-c', 'q9-a', 'q9-b',
          'q9-c'} | {f'q6-a-{k}' for k in Q6A}
CHOICES = {Q8: ('terms', 5, 10, TERMS)}
FINITE = {'8': Q8}
WHOLE_CHOICES = {Q8}
LABELLED = {f'q6-a-{k}' for k in Q6A}
TAILS = {'8': 'with the surrounding garden.'}
LEDGER = [(1, 'Answer Question'), (4, 'Select'), (4, 'any five')]
GAPS = {'q4-a': {'cons-2-5'}, Q8: {'cons-10-2', 'cons-4-4', 'cons-10-1', 'cons-10-4'}}
RETIRED = [('card-source-bindings.json', 'q3-a'), ('card-source-bindings.json', 'q3-b'), ('card-corrections.json', 'q3-b')]
LEAF = {
    'q1-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 4, r(4))],
    'q1-b': [('closer', 3, [0, 3]), ('presentation', 8, BAND8)],
    'q2-a': [('sketch', 8, r(8)), ('type', 5, r(5)), ('thickness', 5, r(5)), ('presentation', 8, BAND8)],
    'q2-b': [('insulating', 5, r(5)), ('sealing', 5, r(5)), ('presentation', 8, BAND8)],
    'q2-c': [('reason-1', 3, r(3)), ('reason-2', 3, r(3))],
    'q3-a': [('items', 28, list(range(0, 29, 4))), ('presentation', 6, BAND6)],
    'q3-b': [('location', 3, r(3)), ('reason', 3, r(3)), ('presentation', 6, BAND6)],
    'q3-c': [('advantage', 4, r(4))],
    'q4-a': [('sketch', 11, r(11)), ('wall-position', 6, r(6)), ('reinforcement', 6, r(6)), ('dimensions', 3, r(3)), ('presentation', 6, BAND6)],
    'q4-b': [('method', 4, r(4)), ('presentation', 6, BAND6)],
    'q4-c': [('advantage-1', 4, r(4)), ('advantage-2', 4, r(4))],
    'q5-a': [('details', 35, list(range(0, 36, 5))), ('dimensions', 3, r(3))],
    'q5-b': [('insulation', 4, [0, 4]), ('presentation', 8, BAND8)],
    **{f'q6-a-{k}': [('precaution-1', 4, r(4)), ('precaution-2', 4, r(4))] for k in Q6A},
    'q6-b': [(f'precaution-{i}', 6, r(6)) for i in (1, 2, 3)] + [('presentation', 8, BAND8)],
    'q6-c': [('reason-1', 4, r(4)), ('reason-2', 4, r(4))],
    'q7-a': [('sketch', 4, r(4))] + [(k, 4, r(4)) for k in ['cooker', 'fridge', 'sink']] + [('presentation', 8, BAND8)],
    'q7-b': [(k, 3, r(3)) for k in ['kitchen-floor', 'kitchen-reason', 'dining-floor', 'dining-reason']],
    'q7-c': [('island', 4, r(4)), ('advantage', 4, r(4)), ('presentation', 6, BAND6)],
    Q8: [('terms', 50, None)],
    'q9-a': [('wood', 6, r(6)), ('reason-1', 6, r(6)), ('reason-2', 6, r(6))],
    'q9-b': [('modification', 12, r(12)), ('presentation', 8, BAND8)],
    'q9-c': [('advantage-1', 6, r(6)), ('advantage-2', 6, r(6))],
}
COMPOSITE = {'q6-a': [f'q6-a-{k}' for k in Q6A]}
COMPOSITE.update({f'q{q}-complete': [f'q{q}-{p}' for p in parts] for q, parts in
                  [('1', 'ab'), ('2', 'abc'), ('3', 'abc'), ('4', 'abc'), ('5', 'ab'), ('6', 'abc'), ('7', 'abc'), ('9', 'abc')]})
TOTALS = {k: sum(x[1] for x in v) for k, v in LEAF.items()}
TOTALS.update({'q6-a': 16, **{k: 50 for k in COMPOSITE if k.endswith('-complete')}})
WORKSHOP = (['cons-9-4'], ['site-safety'])
KITCHEN = (['cons-1-2'], ['planning-sustainability-environment'])
TOPICS = {
    'q1-a': (['cons-1-5', 'cons-3-6', 'cons-3-3', 'cons-3-4'], ['question-one-drawing-questions', 'windows-doors', 'foundations-floors-walls']),
    'q1-b': (['cons-3-6', 'cons-3-3'], ['windows-doors', 'foundations-floors-walls']),
    'q2-a': (['cons-3-9', 'cons-6-2'], ['roofs', 'heat-loss-insulation']),
    'q2-b': (['cons-6-2', 'cons-6-5'], ['heat-loss-insulation', 'air-tightness-condensation']),
    'q2-c': (['cons-6-3', 'cons-6-2'], ['heat-loss-insulation']),
    'q3-a': (['cons-5-2', 'cons-5-1'], ['hot-water-space-heating', 'services-water-gas-electrical']),
    'q3-b': (['cons-5-2', 'cons-5-6'], ['services-water-gas-electrical', 'drainage']),
    'q3-c': (['cons-5-6'], ['drainage']),
    'q4-a': (['cons-2-4', 'cons-2-5'], ['foundations-floors-walls']), 'q4-b': (['cons-3-3'], ['foundations-floors-walls']), 'q4-c': (['cons-2-7'], ['concrete']),
    'q5-a': (['cons-1-5', 'cons-4-3', 'cons-4-5'], ['question-one-drawing-questions', 'foundations-floors-walls', 'windows-doors']),
    'q5-b': (['cons-4-5', 'cons-8-3'], ['windows-doors', 'sound']),
    **{f'q6-a-{k}': WORKSHOP for k in Q6A}, 'q6-b': WORKSHOP, 'q6-c': WORKSHOP,
    'q7-a': KITCHEN, 'q7-b': (['cons-4-2', 'cons-1-2'], ['foundations-floors-walls', 'planning-sustainability-environment']), 'q7-c': KITCHEN,
    Q8: (['cons-1-9', 'cons-5-7', 'cons-1-2', 'cons-10-2', 'cons-3-6', 'cons-5-4', 'cons-3-10', 'cons-4-4', 'cons-10-7', 'cons-10-1', 'cons-10-4', 'cons-5-8'],
         ['fire-places-fire-prevention', 'planning-sustainability-environment', 'wood-rot-ventilation', 'windows-doors', 'drainage', 'roofs',
          'services-water-gas-electrical']),
    'q9-a': (['cons-3-2', 'cons-10-7'], ['foundations-floors-walls', 'wood-rot-ventilation']),
    'q9-b': (['cons-3-5', 'cons-1-2'], ['windows-doors', 'planning-sustainability-environment']),
    'q9-c': (['cons-1-2', 'cons-6-4'], ['planning-sustainability-environment']),
}


def composite(*panels):
    return cp.construction_figures.composite([(S, p, rc) for p, rc in panels])


FIGURES = {
    'q1-original': (P, 2, [45, 39, 580, 235], False), 'q2-original': (P, 2, [45, 240, 580, 465], False),
    'q3-original': (P, 2, [45, 475, 580, 765], False), 'q4-original': (P, 3, [45, 39, 580, 285], False),
    'q5-original': (P, 3, [45, 295, 580, 535], False), 'q6-original': (P, 3, [45, 545, 580, 765], False),
    'q7-original': (P, 4, [45, 39, 580, 340], False), 'q8-original': (P, 4, [45, 365, 580, 470], False),
    'q9-original': (P, 4, [45, 490, 580, 765], False),
    'q1-scheme': (S, 4, [25, 58, 580, 745], True),
    'q2-attic': (S, 5, [25, 58, 580, 382], True), 'q2-trapdoor': (S, 5, [25, 382, 580, 580], True), 'q2-reasons': composite((5, [25, 562, 372, 580]), (5, [25, 580, 580, 770])),
    'q3-system': (S, 6, [25, 58, 580, 450], True), 'q3-valve': (S, 6, [25, 450, 580, 615], True), 'q3-dual-flush': (S, 6, [25, 620, 580, 775], True),
    'q4-foundation': (S, 7, [25, 58, 580, 570], True), 'q4-ties': (S, 7, [25, 580, 580, 760], True), 'q4-ready-mix': (S, 8, [25, 70, 580, 255], True),
    'q5-scheme': (S, 9, [25, 58, 580, 740], True),
    'q6-adhesive': (S, 10, [25, 140, 580, 290], True), 'q6-screwdriver': (S, 10, [25, 295, 580, 480], True), 'q6-precautions': (S, 10, [25, 58, 580, 480], True),
    'q6-bandsaw': composite((11, [25, 58, 580, 760]), (12, [25, 58, 580, 390])), 'q6-instruction': (S, 12, [25, 455, 580, 630], True),
    'q7-layout': (S, 13, [25, 58, 580, 615], True), 'q7-floors': composite((13, [25, 635, 580, 790]), (14, [25, 58, 580, 430])),
    'q7-island': (S, 14, [25, 465, 580, 770], True),
    'q8-terms': composite((15, [25, 58, 580, 765]), (16, [25, 58, 580, 710])),
    'q9-cladding': (S, 17, [25, 58, 580, 485], True), 'q9-modification': (S, 17, [25, 490, 580, 795], True), 'q9-advantages': (S, 18, [25, 70, 580, 250], True),
}
SOLUTION = {'q1-a': 'q1-scheme', 'q1-b': 'q1-scheme', 'q1-complete': 'q1-scheme',
            'q2-a': 'q2-attic', 'q2-b': 'q2-trapdoor', 'q2-c': 'q2-reasons', 'q2-complete': 'q2-attic',
            'q3-a': 'q3-system', 'q3-b': 'q3-valve', 'q3-c': 'q3-dual-flush', 'q3-complete': 'q3-system',
            'q4-a': 'q4-foundation', 'q4-b': 'q4-ties', 'q4-c': 'q4-ready-mix', 'q4-complete': 'q4-foundation',
            'q5-a': 'q5-scheme', 'q5-b': 'q5-scheme', 'q5-complete': 'q5-scheme',
            'q6-a-using-a-contact-adhesive-to-glue-veneers': 'q6-adhesive', 'q6-a-using-a-battery-powered-screwdriver': 'q6-screwdriver',
            'q6-a': 'q6-precautions', 'q6-b': 'q6-bandsaw', 'q6-c': 'q6-instruction', 'q6-complete': 'q6-bandsaw',
            'q7-a': 'q7-layout', 'q7-b': 'q7-floors', 'q7-c': 'q7-island', 'q7-complete': 'q7-layout', Q8: 'q8-terms',
            'q9-a': 'q9-cladding', 'q9-b': 'q9-modification', 'q9-c': 'q9-advantages', 'q9-complete': 'q9-modification'}
CHOICE_FIGURE_PAGES = {Q8: {15, 16}}
PAPER_PAGE = {'1': 2, '2': 2, '3': 2, '4': 3, '5': 3, '6': 3, '7': 4, '8': 4, '9': 4}
SCHEME_PAGES = {'1': [4, 19], '2': [5, 20], '3': [6, 21], '4': [7, 8, 22], '5': [9, 23], '6': [10, 11, 12, 24], '7': [13, 14, 25], '8': [15, 16, 26], '9': [17, 18, 27]}
RUBRIC = 'Question 1 and three other questions, 50 marks each, 200 total'


def validate(d, images=True, figure_dir=cp.FIGURE_DIR, integrated=True):
    import sys
    return cp.validate(d, sys.modules[__name__], images, figure_dir, integrated)


if __name__ == '__main__':
    import sys
    cp.main(sys.modules[__name__])
