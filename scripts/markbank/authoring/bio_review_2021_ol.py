"""Biology 2021 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-13), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 40 pages: p1 cover
    (with the note that the 2021 papers were adjusted for disruption to
    learning), p2 instructions, p3-p7 Section A Questions 1-7, p8-p10
    Section B Questions 8-10, p11 Section C answerbook instructions,
    p12-p15 graph paper, p16-p39 ruled answer pages, p40 back cover. No
    acknowledgements page.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "Do not hand this question paper up", p12 back cover.
  * LC025GLP000EV (marking scheme), 28 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7-p26 Questions
    1-17, p27 "BLANK PAGE", p28 back cover.

The 2021 papers set fewer questions to answer: any four of Section A, any one
of Section B and any three of Section C. Every printed question is carded.

The sitting was already carded (168 authored cards, 164 shipped). As for the
later sittings, every task is re-derived from the PDFs at the scheme's own
mark boundaries and the existing cards are corrected in place: every shipped
id is kept, mapped (`id=`) to the task it was carding, verified or corrected
with its old fields recorded; tasks the old cards bundled or missed are
added. Four authored figure twins that never shipped are withdrawn.

Tariffs as printed. Section A is laddered: Q1 and Q3 "2(8) + 2 + 2(1)" over
five responses, Q2 and Q4-Q7 "2(6) + 3(2) + 2(1)" over seven; Section B
(a) "5 + 1" and (b) "2(9) + 6(1)". Every response is carded at its ladder's
first rate and the ladder, not the cards, makes the printed total. Section C
prints a mark per row.

Printed choices the scheme marks differently per option are split into
routes: Q7(f)(i) and (ii) arthritis or osteoporosis, Q16(b)(vi) the carbon
dioxide test or the ethanol test. Q11(c)(ii) and (v), Q16(a)(vi) and
Q13(c)/Q16(a)'s other either-or asks are marked on shared rows and are one
card each ("choice is not a route").

The degree sign and the tally printed at the end of a menu's last line
("Any three") are read as the page shows them: the tally is the row's note,
not an option.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2021, 'ol'
REVIEWED_AT = '2026-10-13'
BASELINE_COMMIT = '85935123c'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2021-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': 'd4ad67d49220aa4902fb08d3852ab3bef6be9778e7a1de4d6d7cfa2c16c42354',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2021-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': 'a8c1c7b25b3cc337f2f6711d49d5c0d987e469c29025ef37f2316f05dfa86ae7',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2021-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '7bbe606661c393fbc8f663b60f434550a4c30df1b633f6af6ad7cc07cddae602',
               'pages': 28},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 11)},
            11: 'answerbook-instructions', **{p: 'graph-paper' for p in range(12, 16)},
            **{p: 'answer-pages' for p in range(16, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', **{p: 'marking' for p in range(7, 27)},
               27: 'blank', 28: 'back-cover'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 8)}, **{n: 30 for n in range(8, 11)},
    **{n: 60 for n in range(11, 16)}, 16: 120, 17: 120,
}
PART_TOTALS = {
    **{(n, 'a'): 9 for n in range(11, 16)}, **{(n, 'b'): 27 for n in range(11, 16)},
    **{(n, 'c'): 24 for n in range(11, 16)},
    **{(n, x): 30 for n in (16, 17) for x in 'abcd'},
}


def _ladder(notation):
    steps = []
    for term in notation.split(' + '):
        n, _, m = term.partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation}


LADDERS = {
    1: _ladder('2(8) + 2 + 2(1)'), 3: _ladder('2(8) + 2 + 2(1)'),
    **{q: _ladder('2(6) + 3(2) + 2(1)') for q in (2, 4, 5, 6, 7)},
    **{(n, 'a'): _ladder('5 + 1') for n in (8, 9, 10)},
    **{(n, 'b'): _ladder('2(9) + 6(1)') for n in (8, 9, 10)},
}

CHECKSUMS = {
    1: {8: 5}, 3: {8: 5}, **{q: {6: 7} for q in (2, 4, 5, 6, 7)},
    **{(n, 'a'): {5: 2} for n in (8, 9, 10)}, **{(n, 'b'): {9: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in range(11, 16)}, **{(n, 'b'): {3: 9} for n in range(11, 16)},
    **{(n, 'c'): {3: 8} for n in range(11, 16)},
    **{(n, x): {3: 10} for n in (16, 17) for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 11), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any four', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any one', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any three', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any four', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: every part asked.'),
    ('038', 3, 'the following', 'Q2 lead-in: every part asked.'),
    ('038', 4, 'choose', 'Q3 "Choose each structure": a matching list, every structure placed; one card per lettered '
                         'location.'),
    ('038', 4, 'the following', 'Q3 structure list.'),
    ('038', 6, 'the following', 'Q6 lead-in: every statement asked.'),
    ('038', 6, 'or', 'Q6 "true or false": the answer options.'),
    ('038', 6, 'or', 'Q6(e) "tall grass or water": statement text.'),
    ('038', 7, 'or', 'Q7(b) "free moving or synovial joint": one joint type, two names.'),
    ('038', 7, 'any one', 'Q7(e) "any one function": open single answer; one card.'),
    ('038', 7, 'the following', 'Q7(f) lead-in: every part asked.'),
    ('038', 7, 'either', 'Q7(f) "either of the above disorders": separate causes and treatments per option: ROUTES.'),
    ('038', 8, 'any one', 'Section B rubric repeated.'),
    ('038', 8, 'or', 'Q8(a)(ii) "stage or platform": one part, two names.'),
    ('038', 8, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('038', 9, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 10, 'or', 'Q10(b)(v) "reagent or chemical": either form; one answer.'),
    ('040', 2, 'any three', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q11(a): every term asked, one card per roman.'),
    ('040', 2, 'or', 'Q11(c)(ii) "agriculture or industry or the home": marked on the same rows; one card.'),
    ('040', 2, 'or', 'Q11(c)(ii), same choice.'),
    ('040', 2, 'or', 'Q11(c)(v) "agriculture or fisheries or forestry": one 3-mark row for every area; one card.'),
    ('040', 2, 'or', 'Q11(c)(v), same choice.'),
    ('040', 2, 'any two', 'Q11(c)(vi) "any two sets of factors": bounded menu; one card.'),
    ('040', 3, 'the following', 'Q12(a): every term asked, one card per roman.'),
    ('040', 3, 'both', 'Q12(c)(iv) "both stages of the cell cycle": both required; one card.'),
    ('040', 4, 'the following', 'Q13(b)(i): each part asked, one card per item.'),
    ('040', 4, 'the following', 'Q13(c)(ii): each heading asked, one card per item.'),
    ('040', 5, 'any two', 'Q14(b)(iv) "any two functions": bounded menu; one card.'),
    ('040', 5, 'any three', 'Q14(c)(ii) "any three of the following endocrine glands": bounded menu; one card.'),
    ('040', 5, 'the following', 'Q14(c)(ii) gland list.'),
    ('040', 5, 'both', 'Q14(c)(iv) "both an endocrine and an exocrine gland": description.'),
    ('040', 6, 'any two', 'Q15(c)(vii) "any two ways": bounded menu; one card.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'or', 'Q16(a)(vi) "the ear or the eye": marked on the same two rows; one card.'),
    ('040', 7, 'either', 'Q16(b)(vi) "either one of the products": separate test and result per product: ROUTES.'),
    ('040', 8, 'the following', 'Q16(d)(v): each process asked, one card per item.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 10, 'any two', 'Q17(c)(v) "any two factors": bounded menu; one card.'),
    ('040', 10, 'or', 'Q17(d)(iii) "gap or region": one answer, two names.'),
]

ROUTES = {
    'Q7(f)(i)': ['arthritis', 'osteoporosis'],
    'Q7(f)(ii)': ['arthritis', 'osteoporosis'],
    'Q16(b)(vi)': ['carbon-dioxide', 'ethanol'],
}

LAYOUT_CHECKS = [
    ('scheme', 23, 'Milky appearance if CO2 is present', ['Limewater test', 'Iodoform test'], 'Limewater test'),
    ('scheme', 23, 'Yellow colour appears if ethanol is present', ['Limewater test', 'Iodoform test'],
     'Iodoform test'),
]

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2021-ol-q14-b-iv-fig': 'Never shipped: a figure twin of bio-2021-ol-q14-b-iv, which carries the reviewed '
                                'task and its figure.',
    'bio-2021-ol-q15-b-v-fig': 'Never shipped: a figure twin of bio-2021-ol-q15-b-v, which carries the reviewed '
                               'task and its figure.',
    'bio-2021-ol-q15-b-vi-fig': 'Never shipped: a figure twin of bio-2021-ol-q15-b-vi, which carries the reviewed '
                                'task and its figure.',
    'bio-2021-ol-q16d-iv-fig': 'Never shipped: a figure twin of bio-2021-ol-q16d-iv, which carries the reviewed '
                               'task and its figure.',
}
WITHDRAW = {k: (k.replace('-fig', ''), v) for k, v in RETAINED.items()}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list ("1." on its own line, its item on the next)."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


def tick(clip, answer):
    return G('tick-col', page=9, clip=clip, headers=['True', 'False'], expect=answer, marks=6)


def bundled(parts, keep):
    return f'The old card bundled {parts}; it keeps its id for {keep}.'


EACH_ITEM = 'Numbered items are separately counted: one card each.'
SECTION_A_RATE = 'Carded at its ladder\'s first rate; the old card carried the whole question\'s 20.'

Q1 = _A(3, 'Use your knowledge of nutrition to answer the following questions:')
Q2 = _A(3, 'Answer the following in relation to tissues and organs.')
Q3LEAD = _A(4, 'Choose each structure from the following list', 'Column A.')
Q3 = [_A(4, 'Ureter'), _A(4, 'Retina'), _A(4, 'Bronchus'), _A(4, 'Grey matter'), _A(4, 'Villi')]
Q4 = _A(4, 'In squirrels, the allele for black coat colour (B) is dominant', 'phenotypes of the cross.')
Q5 = _A(5, 'The diagram shows the structure of a virus such as COVID')
Q6 = _A(6, 'State whether each of the following statements is true or false', 'appropriate box in each case.')
Q7 = _A(7, 'The diagram shows the structure of a human skeleton.')
Q7F = [_A(7, 'Arthritis and osteoporosis are two disorders', 'the above disorders.'), _A(7, 'Name of disorder:')]
Q8B = _A(8, 'Answer the following questions in relation to the', 'using a light microscope.')
Q9A = _A(9, 'Enzymes play an important role in the body’s metabolism.')
Q9B = _A(9, 'Answer the following in relation to an investigation you carried out', 'rate of enzyme activity.')
Q10B = _A(10, 'The diagram shows the results of an investigation into the digestive activity of', 'germinating seeds.')
Q11A = _C(2, 'Explain the following terms used in ecology:')
Q11B = [_C(2, 'Read the passage below and answer the questions that follow.'),
        _C(2, 'Game of cones: how the red squirrel is making a big comeback'),
        _C(2, 'The mammal fauna found in Ireland', 'certain midland counties.'),
        _C(2, 'Research conducted in 2019', 'hunt for squirrel.'),
        _C(2, 'The new study shows', 'came to the pine marten.'),
        _C(2, '(Adapted from RTE Brainstorm 2020)')]
Q11CII = [M('(ii)', 2), _C(2, 'Name one pollutant from agriculture or industry or the home', 'affects the ecosystem.')]
Q12A = _C(3, 'Explain the following terms used in genetics:')
Q12B = [_C(3, 'The photograph shows Watson and Crick in 1953', 'discovered DNA structure.'),
        _C(3, '(DNA model in 1953. BBC News)')]
Q13B = _C(4, 'The diagram shows the structure of the human heart.')
Q13BI = _C(4, 'In your answer book, state', 'of the following parts:')
Q13C = _C(4, 'The human circulatory system is described as a closed system.')
Q13CII = _C(4, 'Distinguish between an artery and a vein under the following headings:')
Q13CIV = [M('(iv)', 4), _C(4, 'Name another system that carries fluid in the body.')]
Q14B = _C(5, 'The diagram shows the human digestive system.')
Q14C = _C(5, 'The human endocrine system produces hormones.')
Q14CII = [_C(5, 'Draw an outline diagram of the human body and on it indicate the location of',
             'endocrine glands listed below:'),
          _C(5, 'Pituitary', br=True), _C(5, 'Thyroid'), _C(5, 'Pancreas'), _C(5, 'Adrenals'), _C(5, 'Ovaries'),
          _C(5, 'Testes')]
Q15B = _C(6, 'The diagram shows the path that water takes as it is absorbed into the roots of a plant.')
Q15C2 = _C(6, 'The diagram below shows the under surface of a leaf.')
Q16A = _C(7, 'The diagram shows the human ear.')
Q16BIII = _C(7, 'Aerobic respiration is a two', 'stage process.')
Q16BV = [M('(v)', 7), _C(7, 'In bread making yeast is used to', 'fermentation produced by yeast.')]
Q16CIV = _C(8, 'Seeds contain an embryo plant, a food store and a testa.')
Q16D = _C(8, 'The diagram shows the human urinary system.')
Q16DV = _C(8, 'Name the region of part A in which each of the following takes place:')
Q17A = _C(9, 'The diagram shows a foetus in the womb before birth.')
Q17BIV = _C(9, 'During photosynthesis water is split to release three components.')
Q17C = _C(10, 'The diagram shows the structure of a typical bacteria cell.')
Q17D = _C(10, 'The diagram shows a neuron.')

L_VIRUS = [L('A', S('Protein or capsid', page=9), True), L('B', S('DNA or RNA or nucleic acid', page=9), True)]
L_X = [L('X', S('X located on the shoulder or the elbow or the hip or the knee', page=10), False)]
L_GUT = [L(x, S(m, page=20), True) for x, m in [('A', 'Duodenum (or small intestine)'), ('B', 'Liver'),
                                                  ('C', 'Stomach'), ('D', 'Pancreas'),
                                                  ('E', 'Colon (or large intestine)')]]
L_ROOT = [L('A', S('Root hair', page=22), True), L('B', S('Xylem', page=22), True), L('C', S('Phloem', page=22), True)]
L_LEAF = [L('X', S('Stomata', page=22), True), L('Y', S('Guard (cells)', page=22), True)]
L_EAR = [L('A', S('Semi-circular canals', page=23), True), L('B', S('Cochlea', page=23), True),
         L('C', S('Eardrum', page=23), True)]
L_URINARY = [L('A', S('Kidney', page=24), True), L('B', S('Ureter', page=24), True), L('C', S('Bladder', page=24), True)]
L_FOETUS = [L('A', S('Fallopian tube (or oviduct)', page=25), True), L('B', S('Ovary', page=25), True),
            L('C', S('Cervix', page=25), True)]
L_BACTERIUM = [L('A', S('Capsule (allow cell wall) (allow slime layer)', page=26), True),
               L('B', S('DNA (or nucleoid) or chromosome', page=26), True),
               L('C', S('Cytosol (or cytoplasm)', page=26), True)]
L_NEURON = [L('A', S('Cell body (not nucleus)', page=26), True), L('B', S('Dendrites', page=26), True),
            L('C', S('Schwann cell (allow myelin)', page=26), True), L('D', S('Axon (allow node of Ranvier)', page=26),
                                                                       True)]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


def only(keys, *letters):
    return [k for k in keys if k['letter'] in letters]


TASKS = [
    # ------------------------------------------------------------ Section A --
] + [
    T(f'1{x}', f'Q1({x})', 'A', _A(3, ask), rows, 'bio-1-2', concept, SQ(7, sq), 8, stem=[Q1],
      id=f'bio-2021-ol-q1-{x}', decision=SECTION_A_RATE)
    for x, ask, rows, concept, sq in [
        ('a', 'Which food biomolecule contains glycerol?', [pt(S('Fat or lipid'), 8)], 'glycerol-in-fats',
         'Which food biomolecule contains glycerol?'),
        ('b', 'Name a reagent used to test for the presence of a reducing sugar.',
         [pt(S('Benedict’s or Fehling’s or Clinistix'), 8)], 'test-for-reducing-sugar',
         'Name a reagent used to test for the presence of a reducing sugar:'),
        ('c', 'Identify one other element, contained in protein, in addition to C, H, O.',
         [pt(S('Nitrogen (or N) or Sulphur (or S)'), 8, note_sel=S('allow Phosphorus (P)'))], 'elements-in-protein',
         'Identify one other element contained in protein:'),
        ('d', 'Name one fibrous protein found in the body.', [pt(S('Keratin or collagen or elastin or myosin'), 8)],
         'fibrous-proteins', 'Name one fibrous protein found in the body:'),
        ('e', 'Give one example of a water', [pt(S('Vitamin C or Vitamin B'), 8)], 'water-soluble-vitamins',
         'Give one example of a water-soluble vitamin:')]
] + [
    T('2a', 'Q2(a)', 'A', _A(3, 'A tissue is a group of'), [pt(S('(Similar) cells (working together)'), 6)],
      'bio-1-3', 'tissue', SQ(7, 'A tissue is a group of:'), 6, stem=[Q2], id='bio-2021-ol-q2-a',
      decision=SECTION_A_RATE),
    T('2b', 'Q2(b)', 'A', _A(3, 'Name one animal tissue type and one plant tissue type.'),
      [pt(S('Muscle or epithelial or connective or nervous'), 6, label=S('Animal:')),
       pt(S('Dermal or ground or vascular or meristem'), 6, label=S('Plant:'), note_sel=S('(allow xylem or phloem)'))],
      'bio-1-3', 'tissue-types', SQ(7, 'Name one animal tissue and one plant tissue:'), 12, stem=[Q2],
      id='bio-2021-ol-q2-b', decision=SECTION_A_RATE),
    T('2c', 'Q2(c)', 'A', _A(3, 'An organ is a group of'), [pt(S('Tissues (working together to carry out a function)'), 6)],
      'bio-1-3', 'organ', SQ(7, 'An organ is a group of:'), 6, stem=[Q2], id='bio-2021-ol-q2-c',
      decision=SECTION_A_RATE),
    T('2d', 'Q2(d)', 'A', _A(3, 'Name one animal organ and one plant organ.'),
      [pt(S('Any correct animal organ, e.g. heart or lung or brain, etc.'), 6, kind='criterion', label=S('Animal:')),
       pt(S('Any correct plant organ, e.g. leaf or root or flower or stem'), 6, kind='criterion', label=S('Plant:'))],
      'bio-1-3', 'organs', SQ(7, 'Name one animal organ and one plant organ:'), 12, stem=[Q2], id='bio-2021-ol-q2-d',
      decision=SECTION_A_RATE),
    T('2e', 'Q2(e)', 'A', _A(3, 'What is tissue culture?'), [pt(S('Growing cells outside the body (or in a lab)'), 6)],
      'bio-1-3', 'tissue-culture', SQ(7, 'What is tissue culture?'), 6, stem=[Q2], id='bio-2021-ol-q2-e',
      decision=SECTION_A_RATE),
] + [
    T(f'3{x}', f'Q3({x})', 'A', [Q3LEAD, _A(4, location, br=True)], [pt(S(answer, after=location), 8)], topic,
      concept,
      SQ(8, location, after='Question 3'), 8, stem=Q3, id=old,
      decision='Lettered parts are separate printed addresses; each card asks the printed instruction for its own '
               'location, and the completed example (Rib cage, struck through in the list) is left out of the stem.'
      + (f' {dec}' if dec else ''))
    for x, location, answer, topic, concept, old, dec in [
        ('a', 'Spinal cord', 'Grey matter', 'bio-2-4', 'grey-matter', 'bio-2021-ol-q3-ab',
         bundled('(a) and (b)', '(a)')),
        ('b', 'Eye', 'Retina', 'bio-2-4', 'retina', None, ''),
        ('c', 'Lungs', 'Bronchus', 'bio-2-6', 'bronchus', 'bio-2021-ol-q3-cde', bundled('(c)-(e)', '(c)')),
        ('d', 'Small intestine', 'Villi', 'bio-2-6', 'villi', None, ''),
        ('e', 'Kidney', 'Ureter', 'bio-2-6', 'ureter', None, '')]
] + [
    T('4a', 'Q4(a)', 'A', _A(4, 'Possible gametes'),
      [pt(S('B'), 6, note='The scheme\'s completed table is shown after reveal.'), pt(S('b'), 6), pt(S('b', nth=2), 6)],
      'bio-1-4', 'gametes-of-the-cross', SQ(8, 'Possible gametes'), 18, stem=[Q4], qfig='q4-table',
      fig='q4-scheme', id='bio-2021-ol-q4-abc',
      decision='A table to complete: one card per lettered row, a response per box. ' + bundled('(a)-(c)', '(a)')),
    T('4b', 'Q4(b)', 'A', _A(4, 'Genotype of offspring'), [pt(S('Bb'), 6), pt(S('bb'), 6)], 'bio-1-4',
      'offspring-genotypes', SQ(8, 'Genotype of offspring'), 12, stem=[Q4], qfig='q4-table', fig='q4-scheme'),
    T('4c', 'Q4(c)', 'A', _A(4, 'Phenotype of offspring'), [pt(S('Black'), 6), pt(S('Grey'), 6)], 'bio-1-4',
      'offspring-phenotypes', SQ(8, 'Phenotype of offspring'), 12, stem=[Q4], qfig='q4-table', fig='q4-scheme'),
    T('5a', 'Q5(a)', 'A', _A(5, 'Why are viruses not considered to be living organisms?'),
      [pt(S('Not cells or only have one type of nucleic acid or no organelles'), 6)], 'bio-1-1', 'viruses-not-living',
      SQ(9, 'Why are viruses not considered to be living organisms?'), 6, stem=[Q5], fig='q5-virus',
      id='bio-2021-ol-q5-a', decision=SECTION_A_RATE),
    T('5b', 'Q5(b)', 'A', _A(5, 'Identify the two parts labelled A and B that are found in all viruses.'),
      [pt(S('Protein or capsid'), 6, label=S('A:')), pt(S('DNA or RNA or nucleic acid'), 6, label=S('B:'))],
      'bio-1-1', 'parts-of-a-virus', SQ(9, 'Identify the two parts labelled A and B'), 12, stem=[Q5], fig='q5-virus',
      labels=L_VIRUS, id='bio-2021-ol-q5-b-fig', decision=SECTION_A_RATE),
    T('5c', 'Q5(c)', 'A', _A(5, 'Describe one way viruses may be spread from person to person.'),
      [pt(S('Coughing or sneezing', 'any valid answer'), 6)], 'bio-1-1', 'spread-of-viruses',
      SQ(9, 'Describe one way viruses may be spread'), 6, stem=[Q5], fig='q5-virus', id='bio-2021-ol-q5-c',
      decision=SECTION_A_RATE),
    T('5d', 'Q5(d)', 'A', _A(5, 'State one way the body can defend itself against viruses.'),
      [pt(S('Barrier (system) or skin', 'antibodies'), 6)], 'bio-2-4', 'defence-against-viruses',
      SQ(9, 'State one way the body can defend itself against viruses:'), 6, stem=[Q5], fig='q5-virus',
      id='bio-2021-ol-q5-d', decision=SECTION_A_RATE),
    T('5e', 'Q5(e)', 'A', _A(5, 'Give one way in which viruses are beneficial.'),
      [pt(S('(Used in) vaccine production', 'population control'), 6)], 'bio-1-1', 'beneficial-viruses',
      SQ(9, 'Give one way in which viruses are beneficial:'), 6, stem=[Q5], fig='q5-virus', id='bio-2021-ol-q5-e',
      decision=SECTION_A_RATE),
    T('5f', 'Q5(f)', 'A', _A(5, 'Explain why viruses are described as obligate parasites.'),
      [pt(S('Can only replicate in living cells (or host)'), 6)], 'bio-1-1', 'obligate-parasites',
      SQ(9, 'Explain why viruses are described as obligate parasites:'), 6, stem=[Q5], fig='q5-virus',
      id='bio-2021-ol-q5-f', decision=SECTION_A_RATE),
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(6, start), [tick(clip, answer)], 'bio-3-1', concept, SQ(9, start), 6,
      stem=[Q6], id=old, decision=dec)
    for x, start, clip, answer, concept, old, dec in [
        ('a', 'A pooter can be used to collect small insects from leaves.', (60, 430, 560, 456), 'True', 'pooter',
         'bio-2021-ol-q6-abc', bundled('(a)-(c)', '(a)')),
        ('b', 'A mammal trap is used to identify plants.', (60, 456, 560, 480), 'False', 'mammal-trap', None, ''),
        ('c', 'A cryptozoic trap can capture large animals.', (60, 480, 560, 505), 'False', 'cryptozoic-trap', None,
         ''),
        ('d', 'A pitfall trap is used to capture insects in flight.', (60, 505, 560, 530), 'False', 'pitfall-trap',
         'bio-2021-ol-q6-def', bundled('(d)-(f)', '(d)')),
        ('e', 'A net is used to capture small organisms from tall grass or water.', (60, 530, 560, 554), 'True',
         'sweep-net', None, ''),
        ('f', 'A Tullgren funnel is used to extract small organisms from leaf litter.', (60, 554, 560, 578), 'True',
         'tullgren-funnel', None, ''),
        ('g', 'Abiotic factors are living factors that affect organisms.', (60, 578, 560, 604), 'False',
         'abiotic-factors', 'bio-2021-ol-q6-g', '')]
] + [
    T('7a', 'Q7(a)', 'A', _A(7, 'What type of joint is found in the skull?'),
      [pt(S('Immovable (or fused) or fixed or sutures'), 6)], 'bio-2-4', 'skull-joints',
      SQ(10, 'What type of joint is found in the skull?'), 6, stem=[Q7], fig='q7-skeleton', id='bio-2021-ol-q7-a',
      decision=SECTION_A_RATE),
    T('7b', 'Q7(b)', 'A', _A(7, 'Place an X on the diagram in a position to', 'synovial joint.'),
      [pt(S('X located on the shoulder or the elbow or the hip or the knee'), 6, kind='criterion')], 'bio-2-4',
      'synovial-joints', SQ(10, 'Place an X on the diagram'), 6, stem=[Q7], fig='q7-skeleton',
      id='bio-2021-ol-q7-b', decision=SECTION_A_RATE),
    T('7c', 'Q7(c)', 'A', _A(7, 'Name the type of synovial joint you have', 'labelled X on the diagram.'),
      [pt(S('Ball and socket (if X is located at the shoulder or hip) or hinge', 'knee or elbow)'), 6)], 'bio-2-4',
      'types-of-synovial-joint', SQ(10, 'Name the type of synovial joint'), 6,
      stem=[Q7, M('(b)', 7), _A(7, 'Place an X on the diagram in a position to', 'synovial joint.')],
      fig='q7-skeleton', labels=L_X,
      decision='The X is the student\'s own mark from (b): the label key gives where the scheme accepts it.'),
    T('7d', 'Q7(d)', 'A', _A(7, 'Place an F on the diagram to show the femur.'),
      [pt(S('F located on either long bone in the upper leg (thigh)'), 6, kind='criterion')], 'bio-2-4', 'femur',
      SQ(10, 'Place an F on the diagram to show the femur:'), 6, stem=[Q7], fig='q7-skeleton',
      id='bio-2021-ol-q7-d-fig', decision=SECTION_A_RATE),
    T('7e', 'Q7(e)', 'A', _A(7, 'Give any one function of the skeleton.'),
      [pt(S('Protection or make blood cells or support (or shape or structure) or movement'), 6)], 'bio-2-4',
      'functions-of-the-skeleton', SQ(10, 'Give any one function of the skeleton:'), 6, stem=[Q7],
      fig='q7-skeleton', id='bio-2021-ol-q7-e', decision=SECTION_A_RATE),
    T('7fi-arthritis', 'Q7(f)(i)', 'A', _A(7, 'One possible cause of the named disorder.'),
      [pt(S('inflammation or wear and tear (or old age) or injury or autoimmune'), 6, label=S('Arthritis:'),
          note_sel=S('Disorder must be named to get this point'))], 'bio-2-4', 'causes-of-arthritis',
      SQ(10, 'One possible cause of the named musculoskeletal disorder:'), 6, stem=[Q7] + Q7F, fig='q7-skeleton', route='arthritis',
      id='bio-2021-ol-q7-f',
      decision='Closed choose-one pool of two printed disorders, each with its own scheme rows: one card per '
               'disorder. The old card carried (f) whole; it keeps its id for (f)(i), arthritis.'),
    T('7fi-osteoporosis', 'Q7(f)(i)', 'A', _A(7, 'One possible cause of the named disorder.'),
      [pt(S('Osteoporosis: low calcium', 'sex hormone'), 6, note_sel=S('Disorder must be named to get this point'))],
      'bio-2-4', 'causes-of-osteoporosis', SQ(10, 'One possible cause of the named musculoskeletal disorder:'), 6,
      stem=[Q7] + Q7F, fig='q7-skeleton', route='osteoporosis',
      decision='Closed choose-one pool of two printed disorders, each with its own scheme rows: one card per '
               'disorder.'),
    T('7fii-arthritis', 'Q7(f)(ii)', 'A', _A(7, 'One treatment for the named disorder.'),
      [pt(S('(anti-inflammatory) medication or rest or exercise or surgery'), 6, label=S('Arthritis:'),
          note_sel=S('Treatment must match cause'))], 'bio-2-4', 'treating-arthritis',
      SQ(10, 'One treatment for the named musculoskeletal disorder.'), 6, stem=[Q7] + Q7F, fig='q7-skeleton', route='arthritis',
      decision='Closed choose-one pool of two printed disorders, each with its own scheme rows: one card per '
               'disorder.'),
    T('7fii-osteoporosis', 'Q7(f)(ii)', 'A', _A(7, 'One treatment for the named disorder.'),
      [pt(S('Osteoporosis: healthy diet', 'surgery (allow vitamin D)'), 6, note_sel=S('Treatment must match cause'))],
      'bio-2-4', 'treating-osteoporosis', SQ(10, 'One treatment for the named musculoskeletal disorder.'), 6,
      stem=[Q7] + Q7F, fig='q7-skeleton', route='osteoporosis',
      decision='Closed choose-one pool of two printed disorders, each with its own scheme rows: one card per '
               'disorder.'),
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(8, 'Identify with a label X, the eyepiece on the', 'light microscope.'),
      [pt(S('X correctly positioned'), 5, kind='criterion')], 'bio-1-3', 'microscope-eyepiece',
      SQ(11, 'Identify with a label X, the eyepiece'), 5, fig='q8-microscope'),
    T('8aii', 'Q8(a)(ii)', 'B', _A(8, 'Identify with a label Y, the stage or platform on', 'light microscope.'),
      [pt(S('Y correctly positioned'), 5, kind='criterion')], 'bio-1-3', 'microscope-stage',
      SQ(11, 'Identify with a label Y, the stage or platform'), 5, fig='q8-microscope'),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', _A(8, ask, aend), rows, 'bio-1-3', concept, SQ(11, sq), total, stem=[Q8B],
      id=f'bio-2021-ol-q8-b-{r}')
    for r, ask, aend, rows, concept, sq, total in [
        ('i', 'Name a plant you used to obtain the sample of', 'cells.', [pt(S('Onion (or another correct example)'), 9)],
         'plant-for-cells', 'Name a plant you used to obtain the sample of cells:', 9),
        ('ii', 'How did you prepare an unstained plant cell', 'microscope?',
         [anyn(S('Cut or peel or place / a (thin) slice', 'lowered a cover slip Any three'), 3, 9)],
         'preparing-a-slide', 'How did you prepare an unstained plant cell sample?', 27),
        ('iii', 'What stain did you add to the cells?', None, [pt(S('Iodine'), 9)], 'iodine-stain',
         'What stain did you add to the cells?', 9),
        ('iv', 'What was the purpose of the stain?', None, [pt(S('Makes cells stand out or cells more easily seen'), 9)],
         'why-stain', 'What was the purpose of the stain?', 9),
        ('v', 'How did the objective lens help you to see your stained cell sample?', None,
         [pt(S('Magnifies image or enlarges image or see more detail'), 9)], 'objective-lens',
         'How did the objective lens help you', 9),
        ('vi', 'Give one cell structure that showed you were looking at plant cells.', None,
         [pt(S('Cell wall or (large) vacuole or chloroplast'), 9)], 'plant-cell-features',
         'Give one cell structure that showed you were looking at plant cells:', 9)]
] + [
    T('9ai', 'Q9(a)(i)', 'B', _A(9, 'What is an enzyme?'), [pt(S('Protein catalyst'), 5)], 'bio-2-1', 'enzyme',
      SQ(12, 'What is an enzyme?'), 5, stem=[Q9A], id='bio-2021-ol-q9-a-i'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(9, 'Explain the underlined word.'),
      [pt(S('(All) chemical reactions that occur in the body (or a cell)'), 5)], 'bio-1-1', 'metabolism',
      SQ(12, 'Explain metabolism:'), 5, stem=[Q9A], qfig='q9a-ii-question', id='bio-2021-ol-q9-a-ii',
      decision='The paper marks the word to explain by underlining it: the question is shown as printed.'),
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', _A(9, ask, aend), rows, 'bio-2-1', concept, SQ(12, sq), total, stem=[Q9B],
      id=f'bio-2021-ol-q9-b-{r}', qfig='q9b-vii-question' if r == 'vii' else None,
      decision='The ask points at axes printed below it: the question is shown as printed, with the axes.'
      if r == 'vii' else '')
    for r, ask, aend, rows, concept, sq, total in [
        ('i', 'Name the enzyme you used in the investigation.', None,
         [pt(S('Correctly named enzyme (e.g. catalase or pepsin or amylase)'), 9, kind='criterion')], 'enzyme-for-ph',
         'Name the enzyme you used in the investigation:', 9),
        ('ii', 'Name the substrate for the enzyme named at part (i) above.', None,
         [pt(S('Catalase: hydrogen peroxide', 'Amylase: starch'), 9, whole=True, kind='criterion')], 'substrates',
         'Name the substrate for the enzyme named at part (i) above:', 9),
        ('iii', 'How did you vary the pH?', None, [pt(S('Using different (pH) buffers'), 9)], 'buffers',
         'How did you vary the pH?', 9),
        ('iv', 'Name the factor that you kept constant.', None, [pt(S('Temperature'), 9)], 'constant-factor',
         'Name the factor that you kept constant:', 9),
        ('v', 'How was this factor kept constant?', None, [pt(S('Waterbath'), 9)], 'water-bath',
         'How was this factor kept constant?', 9),
        ('vi', 'How did you measure the rate of enzyme activity?', None,
         [pt(S('Catalase: (height of) foam or bubbles', 'Amylase: disappearance of blue-black colour'), 9, whole=True,
             kind='criterion'),
          pt(S('per unit time'), 9)], 'measuring-enzyme-rate', 'How did you measure the rate of enzyme activity?', 18),
        ('vii', 'Sketch a graph to show the results of your investigation using the axis provided.', None,
         [pt(S('Increasing line, peak, and decreasing line'), 9, kind='criterion')], 'rate-against-ph',
         'Sketch a graph on effect of pH on the rate of enzyme activity:', 9)]
] + [
    T('10ai', 'Q10(a)(i)', 'B', _A(10, 'What is digestion?'), [pt(S('Breakdown of food'), 5)], 'bio-2-6', 'digestion',
      SQ(13, 'What is digestion?'), 5, id='bio-2021-ol-q10-a-i'),
    T('10aii', 'Q10(a)(ii)', 'B', _A(10, 'Name the product of starch digestion in plants.'),
      [pt(S('Maltose or glucose'), 5)], 'bio-2-6', 'starch-digestion', SQ(13, 'Name the product of starch digestion'),
      5, id='bio-2021-ol-q10-a-ii'),
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'B', _A(10, ask, aend), rows, topic, concept, SQ(13, sq), total, stem=[Q10B],
      fig='q10-dishes', id=f'bio-2021-ol-q10-b-{r}')
    for r, ask, aend, rows, topic, concept, sq, total in [
        ('i', 'Name a seed you could use in the investigation.', None,
         [pt(S('Broad bean (or another correctly named seed)'), 9)], 'bio-2-5', 'seed-for-digestion',
         'Name a seed you could use:', 9),
        ('ii', 'Name a type of agar you could use in this investigation.', None,
         [pt(S('Starch (agar) or milk (agar)'), 9)], 'bio-2-5', 'agar-for-digestion', 'Name a type of agar', 9),
        ('iii', 'Describe one step taken to minimise contamination during the investigation.', None,
         [pt(S('Clean bench with disinfectant', 'petri dish)'), 9)], 'bio-2-5', 'avoiding-contamination',
         'Describe one step taken to minimise contamination', 9),
        ('iv', 'Why are there multiple seeds used in each dish?', None,
         [pt(S('In case some seeds are dead or for a fair test'), 9)], 'bio-2-5', 'replicate-seeds',
         'Why are there multiple seeds used in each dish?', 9),
        ('v', 'What test reagent or chemical was added to determine if digestive activity had', 'occurred?',
         [pt(S('Iodine (if starch agar was used) or Biuret (reagent) (if milk agar was used)'), 9)], 'bio-2-5',
         'test-reagent', 'What test reagent or chemical was added', 9),
        ('vi', 'Why are there no clear patches in dish B?', None,
         [anyn(S('(Boiled) seeds are dead /', 'dish is fully stained by iodine (or Biuret reagent)'), 2, 9)],
         'bio-2-5', 'boiled-seeds', 'Why are there no clear patches in dish B?', 18),
        ('vii', 'What is the purpose of a control in a scientific investigation?', None,
         [pt(S('(Act) as a comparison (to the test)'), 9)], 'bio-u2', 'control',
         'What is the purpose of a control', 9)]
] + [
    # ------------------------------------------------------------ Section C --
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, _C(2, term, br=True)], rows, 'bio-3-1', concept,
      SQ(14, 'Explain the following terms used in ecology:'), 3, id='bio-2021-ol-q11-a' if r == 'i' else None,
      decision=bundled('(a)(i)-(iii)', '(i), and (ii), (iii) are added') if r == 'i' else '')
    for r, term, rows, concept in [
        ('i', 'Biosphere', [pt(S('place (on Earth) where life can exist'), 3, label=S('Biosphere:'))], 'biosphere'),
        ('ii', 'Edaphic factors', [pt(S('Edaphic factors: (relating to the) soil'), 3)], 'edaphic-factors'),
        ('iii', 'Food web.', [pt(S('interconnected food chains'), 3, label=S('Food web:'))], 'food-web')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', _C(2, ask, aend), rows, 'bio-3-1', concept, SQ(14, sq), total, stem=Q11B,
      id=f'bio-2021-ol-q11-b-{r}',
      notes='Nothing in this part depends on the photograph of a squirrel printed beside the passage; the '
            'passage\'s "has shown" is its own wording.')
    for r, ask, aend, rows, concept, sq, total in [
        ('i', 'What is meant by the term fauna?', None, [pt(S('Animals'), 3)], 'fauna',
         'What is meant by the term fauna?', 3),
        ('ii', 'Give two reasons why the population of red squirrels declined after 1911.', None,
         [anyn(S('Arrival of larger grey squirrels /', 'squirrel pox virus'), 2, 3)], 'red-squirrel-decline',
         'Give two reasons why the population of red squirrels declined', 6),
        ('iii', 'Name an ecological technique used to calculate the population of an animal species.', None,
         [pt(S('Capture-recapture (technique)'), 3)], 'capture-recapture',
         'Name an ecological technique used to calculate the population', 3),
        ('iv', 'Name a predator mentioned in the passage above.', None, [pt(S('Pine marten'), 3)], 'pine-marten',
         'Name a predator mentioned in the passage:', 3),
        ('v', 'Give two activities that affected the population of the named predator', 'above.',
         [pt(S('Hunting'), 3), pt(S('Habitat loss (accept Wildlife Act)'), 3)], 'pine-marten-decline',
         'Give two activities that affected the population', 6),
        ('vi', 'Why has the population of grey squirrels declined in recent years?', None,
         [pt(S('Prey for the pine marten or showed a'), 3)], 'grey-squirrel-decline',
         'Why has the population of grey squirrels declined', 3),
        ('vii', 'Draw a food chain using the information from the above passage.', None,
         [pt(S('Pine nuts → Squirrel → Pine marten'), 3)], 'food-chain-from-passage',
         'Draw a food chain using the information', 3)]
] + [
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Explain the term pollution.'), [pt(S('Harmful addition to the environment'), 3)],
      'bio-3-1', 'pollution', SQ(15, 'Explain the term pollution:'), 3, id='bio-2021-ol-q11-c-i'),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Name one pollutant from agriculture or industry or the home', 'ecosystem.'),
      [pt(S('Correctly named pollutant'), 3, kind='criterion'), pt(S('Matching effect'), 3, kind='criterion')],
      'bio-3-1', 'pollutants', SQ(15, 'Name one pollutant from and describe how it affects the ecosystem:'), 6,
      decision='"Agriculture or industry or the home": marked on the same two rows; one card.'),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'How could the pollutant named at part (ii) above be controlled?'),
      [pt(S('Matching control method'), 3, kind='criterion')], 'bio-3-1', 'controlling-pollution',
      SQ(15, 'How could the pollutant named at part (ii) above be controlled?'), 3, stem=Q11CII),
    T('11civ', 'Q11(c)(iv)', 'C', _C(2, 'Give one reason why waste management is important.'),
      [pt(S('Prevent pollution or protects the environment', 'improves health'), 3)], 'bio-3-1',
      'why-manage-waste', SQ(15, 'Give one reason why waste management is important:'), 3, id='bio-2021-ol-q11-c-iv'),
    T('11cv', 'Q11(c)(v)', 'C', _C(2, 'Give one example of a good waste management practice from agriculture or',
                                   'fisheries or forestry.'),
      [pt(S('Agriculture: Storing slurry', 'chipboard or any valid example'), 3, whole=True)], 'bio-3-1',
      'waste-management-practice', SQ(15, 'Give one example of a good waste management practice'), 3,
      id='bio-2021-ol-q11-c-v',
      decision='"Agriculture or fisheries or forestry": one 3-mark row listing an example for each area; one card.'),
    T('11cvi', 'Q11(c)(vi)', 'C', _C(2, 'Name any two sets of factors that affect the distribution of organisms in a',
                                     'habitat.'),
      [anyn(S('Environmental / climatic / edaphic / aquatic / or any correct example'), 2, 3)], 'bio-3-1',
      'distribution-factors', SQ(15, 'Name any two sets of factors'), 6, id='bio-2021-ol-q11-c-vi'),
] + [
    T(f'12a{r}', f'Q12(a)({r})', 'C', [Q12A, _C(3, term, br=True)], rows, 'bio-1-4', concept,
      SQ(16, 'Explain the following terms used in genetics:'), 3, id='bio-2021-ol-q12-a' if r == 'i' else None,
      decision=bundled('(a)(i)-(iii)', '(i), and (ii), (iii) are added') if r == 'i' else '')
    for r, term, rows, concept in [
        ('i', 'Heredity', [pt(S('passing on of features from parents to offspring (or by means of', 'genes)'), 3,
                              label=S('Heredity:'))], 'heredity'),
        ('ii', 'Gene', [pt(S('section of DNA (that codes for a protein) or unit of inheritance or',
                             'part of DNA or part of chromosome'), 3, label=S('Gene:'))], 'gene'),
        ('iii', 'Chromosome.', [pt(S('Chromosome: (coiled thread of) DNA and protein'), 3)], 'chromosome')]
] + [
    T(f'12b{r}', f'Q12(b)({r})', 'C', _C(3, ask, aend), rows, topic, concept, SQ(16, sq), 3, stem=Q12B,
      fig='q12-watson-crick', id=f'bio-2021-ol-q12-b-{r}')
    for r, ask, aend, rows, topic, concept, sq in [
        ('i', 'How many strands are there in a molecule of DNA?', None, [pt(S('Two'), 3)], 'bio-1-2', 'dna-strands',
         'How many strands are there in a molecule of DNA?'),
        ('ii', 'Explain why some parts of DNA may be described as ‘junk DNA’.', None,
         [pt(S('They do not code for any proteins (or they are non-coding) or they have no use'), 3)], 'bio-1-2',
         'junk-dna', 'Explain why some parts of DNA may be described'),
        ('iii', 'Name a complementary base pair found in DNA.', None,
         [pt(S('Adenine and thymine (or A and T) or Guanine and cytosine (or G and C)'), 3)], 'bio-1-2', 'base-pairs',
         'Name a complementary base pair found in DNA:'),
        ('iv', 'What happens structurally, to the DNA molecule, before replication begins?', None,
         [pt(S('The two strands of DNA separate or it unzips or uncoils or it separates'), 3)], 'bio-2-3',
         'dna-replication', 'What happens structurally, to the DNA molecule'),
        ('v', 'Name the complementary structure to DNA that is involved in protein synthesis.', None,
         [pt(S('RNA'), 3)], 'bio-2-3', 'rna', 'Name the complementary structure to DNA'),
        ('vi', 'Describe one way this molecule differs from DNA.', None,
         [pt(S('It is single stranded or it has uracil', 'ribosome or cytoplasm'), 3)], 'bio-1-2', 'rna-and-dna',
         'Describe one way this molecule differs from DNA:'),
        ('vii', 'What is a codon?', None,
         [pt(S('A sequence of three bases in DNA (or RNA) or codes for an amino acid'), 3)], 'bio-2-3', 'codon',
         'What is a codon?'),
        ('viii', 'Name the smaller molecules that are put together to form a protein molecule.', None,
         [pt(S('Amino acids or peptides'), 3)], 'bio-1-2', 'amino-acids', 'Name the smaller molecules'),
        ('ix', 'What further step must be taken before these chains of molecules become', 'functional proteins?',
         [pt(S('Folding'), 3)], 'bio-2-3', 'protein-folding', 'What further step must be taken')]
] + [
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'What is cancer?'), [pt(S('Uncontrolled cell division'), 3)], 'bio-2-3',
      'cancer', SQ(17, 'What is cancer?'), 3, id='bio-2021-ol-q12-c-i'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Give two causes of cancer.'),
      [anyn(S('Cigarette smoke or smoking / asbestos', 'other correct'), 2, 3)], 'bio-2-3', 'causes-of-cancer',
      SQ(17, 'Give two causes of cancer:'), 6, id='bio-2021-ol-q12-c-ii'),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Name the two types of cell division and give one difference between them.'),
      [pt(S('Mitosis'), 3), pt(S('Meiosis'), 3),
       pt(S('Mitosis:', 'used in sexual reproduction'), 3, whole=True,
          note_sel=S('(Must have mitosis or meiosis in answer in correct context)'))], 'bio-2-3',
      'mitosis-and-meiosis', SQ(17, 'Name the two types of cell division'), 9, id='bio-2021-ol-q12-c-iii'),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Draw one simple labelled diagram which represents both stages of the cell cycle.'),
      [pt(S('Chart correct:'), 3, kind='criterion', whole=True,
          note='The scheme\'s chart is shown after reveal.'),
       pt(S('Both labels correct:'), 3, kind='criterion', whole=True)], 'bio-2-3', 'cell-cycle-diagram',
      SQ(17, 'Draw one simple labelled diagram'), 6, fig='q12c-iv-scheme',
      decision='The scheme draws its chart (interphase and mitosis) and marks the chart and both labels: its '
               'drawing is the solution figure.'),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'What is the liquid part of the blood called?'), [pt(S('Plasma'), 3)], 'bio-2-6',
      'plasma', SQ(18, 'What is the liquid part of the blood called?'), 3, id='bio-2021-ol-q13-a-i'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Name one cell type found in the blood and give one function', 'type.'),
      [pt(S('Correct blood cell type'), 3, kind='criterion'), pt(S('Matching function'), 3, kind='criterion')],
      'bio-2-6', 'blood-cells', SQ(18, 'Name one cell type found in the blood'), 6),
] + [
    T(f'13bi{n}', f'Q13(b)(i){n}', 'C', [Q13BI, item(4, n, part, 'In your answer book, state')],
      [pt(S(letter, after=after), 3)], 'bio-2-6', concept, SQ(18, 'Which letter represents each of the following parts:'),
      3, stem=[Q13B], fig='q13-heart', id='bio-2021-ol-q13-b-i-fig' if n == 1 else None,
      decision=('The old card bundled items 1-4; it keeps its id for 1., and 2.-4. are added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, part, letter, after, concept in [
        (1, 'Septum', 'E', '1. Septum:', 'septum'), (2, 'Vena cava', 'A', '2. Vena cava:', 'vena-cava'),
        (3, 'Aorta', 'C', '3. Aorta:', 'aorta'), (4, 'Bicuspid valve.', 'D', '3. Aorta:', 'bicuspid-valve')]
] + [
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Describe two ways the blood', 'right atrium.'),
      [pt(S('Higher in oxygen'), 3), pt(S('Lower in CO2'), 3)], 'bio-2-6', 'left-ventricle-blood',
      SQ(18, 'Describe two ways the blood in the left ventricle differs'), 6, stem=[Q13B], fig='q13-heart',
      id='bio-2021-ol-q13-b-ii'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Where does the blood in structure B', 'flow to next?'),
      [pt(S('Lungs'), 3)], 'bio-2-6', 'pulmonary-artery', SQ(18, 'Where does the blood in structure B flow to next?'), 3,
      stem=[Q13B], fig='q13-heart', id='bio-2021-ol-q13-b-iii-fig'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'What is the purpose of structure D?'), [pt(S('Prevent backflow of blood'), 3)],
      'bio-2-6', 'heart-valves', SQ(18, 'What is the purpose of structure D?'), 3, stem=[Q13B], fig='q13-heart',
      id='bio-2021-ol-q13-b-iv'),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'Name one factor that causes the pulse rate to increase.'),
      [pt(S('Exercise or smoking', 'any stimulant'), 3)], 'bio-2-6', 'pulse-rate',
      SQ(18, 'Name one factor that causes the pulse rate to increase:'), 3, stem=[Q13B], fig='q13-heart', id='bio-2021-ol-q13-b-v'),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'What is meant by a closed circulatory system?'),
      [pt(S('Blood remains in vessels'), 3)], 'bio-2-6', 'closed-circulation',
      SQ(19, 'What is meant by a closed circulatory system?'), 3, stem=[Q13C], id='bio-2021-ol-q13-c-i'),
] + [
    T(f'13cii{n}', f'Q13(c)(ii){n}', 'C', item(4, n, head, 'Distinguish between an artery and a vein'),
      [pt(S(ans), 3)], 'bio-2-6', concept, SQ(19, 'Distinguish between an artery and a vein'), 3, stem=[Q13C, Q13CII],
      id='bio-2021-ol-q13-c-ii' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, head, ans, concept in [
        (1, 'Size of lumen (cavity)', 'Artery lumen is smaller or vein lumen is larger', 'lumen-size'),
        (2, 'Thickness of wall.', 'Artery wall is thicker or vein wall is thinner', 'wall-thickness')]
] + [
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Give one feature of capillaries which is related to their function.'),
      [pt(S('Thin walls (allow diffusion) or narrow or numerous or porous'), 3)], 'bio-2-6', 'capillaries',
      SQ(19, 'Give one feature of capillaries'), 3, stem=[Q13C], id='bio-2021-ol-q13-c-iii'),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'Name another system that carries fluid in the body.'),
      [pt(S('Lymphatic system'), 3)], 'bio-2-6', 'lymphatic-system', SQ(19, 'Name another system that carries fluid'), 3,
      stem=[Q13C], id='bio-2021-ol-q13-c-iv'),
    T('13cv', 'Q13(c)(v)', 'C', _C(4, 'Name the fluid carried by the system named at part (iv) above.'),
      [pt(S('Lymph'), 3)], 'bio-2-6', 'lymph', SQ(19, 'Name the fluid carried by the system'), 3,
      stem=[Q13C] + Q13CIV, id='bio-2021-ol-q13-c-v'),
    T('13cvi', 'Q13(c)(vi)', 'C', _C(4, 'Give two functions of the system named at part (iv) above.'),
      [anyn(S('Returns excess tissue fluid to blood /', 'maturation (or storage) of white blood cells'), 2, 3)],
      'bio-2-6', 'lymphatic-functions', SQ(19, 'Give two functions of the system'), 6, stem=[Q13C] + Q13CIV,
      id='bio-2021-ol-q13-c-vi'),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'Name two types of digestion that take place in the human body.'),
      [pt(S('Chemical'), 3), pt(S('Mechanical (or physical)'), 3)], 'bio-2-6', 'types-of-digestion',
      SQ(20, 'Name two types of digestion'), 6, id='bio-2021-ol-q14-a-i'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Food is moved along the digestive system by muscular contractions.',
                                     'What is this process called?'),
      [pt(S('Peristalsis'), 3)], 'bio-2-6', 'peristalsis', SQ(20, 'Food is moved along the digestive system'), 3,
      id='bio-2021-ol-q14-a-ii'),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Name the parts labelled A, B, C, D, E.'),
      [pt(S(f'{x}: {m}'), 3) for x, m in [('A', 'Duodenum (or small intestine)'), ('B', 'Liver'), ('C', 'Stomach'),
                                          ('D', 'Pancreas'), ('E', 'Colon (or large intestine)')]],
      'bio-2-6', 'parts-of-the-gut', SQ(20, 'Name the parts labelled A, B, C, D, E:'), 15, stem=[Q14B],
      fig='q14-digestive', labels=L_GUT, id='bio-2021-ol-q14-b-i-fig'),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Name the acid released by part C.'), [pt(S('Hydrochloric (acid)'), 3)],
      'bio-2-6', 'hydrochloric-acid', SQ(20, 'Name the acid released by part C:'), 3, stem=[Q14B], fig='q14-digestive',
      labels=only(asked(L_GUT), 'C'), id='bio-2021-ol-q14-b-ii'),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'What liquid is stored in the gall bladder?'), [pt(S('Bile'), 3)], 'bio-2-6',
      'bile', SQ(20, 'What liquid is stored in the gall bladder?'), 3, stem=[Q14B], fig='q14-digestive',
      id='bio-2021-ol-q14-b-iii'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Give any two functions of the part labelled B.'),
      [anyn(S('Breakdown red blood cells / make bile', 'make blood proteins'), 2, 3)], 'bio-2-6',
      'functions-of-the-liver', SQ(20, 'Give any two functions of the part labelled B:'), 6, stem=[Q14B],
      fig='q14-digestive', labels=only(asked(L_GUT), 'B'), id='bio-2021-ol-q14-b-iv'),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'Explain the underlined term.'), [pt(S('Chemical messenger'), 3)], 'bio-2-4',
      'hormones', SQ(21, 'Explain the term hormones:'), 3, stem=[Q14C], qfig='q14c-i-question',
      id='bio-2021-ol-q14-c-i',
      decision='The paper marks the term to explain by underlining it: the question is shown as printed.'),
    T('14cii', 'Q14(c)(ii)', 'C', Q14CII,
      [anyn(None, 3, 3, options=[S(g, after='Q14 (c) (i - iv)') for g in
                                 ('Pituitary', 'Thyroid', 'Pancreas', 'Adrenals', 'Ovaries', 'Testes')],
            note='The scheme\'s labelled outline is shown after reveal.')], 'bio-2-4', 'locating-endocrine-glands',
      SQ(21, 'Outline diagram of the human body and locations of three endocrine glands:'), 9, stem=[Q14C],
      fig='q14c-ii-scheme', id='bio-2021-ol-q14-c-ii',
      decision='"Any three 3(3)": the scheme marks each gland it labels on its outline; its labels are the menu and '
               'its drawing is the solution figure.'),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Name a hormone produced by each of the three glands referred to in your',
                                       'diagram at part (ii) above.'),
      [anyn(None, 3, 3, options=[S('Pituitary: Growth hormone (or other correct)'), S('Thyroid:', 'Thyroxine'),
                                 S('Pancreas: Insulin'), S('Adrenals: Adrenaline'),
                                 S('Ovaries:', 'Oestrogen or progesterone'), S('Testes:', 'Testosterone')],
            note_sel=S('The three glands and hormones must', 'match answers to part (ii) above'))], 'bio-2-4',
      'hormones-of-endocrine-glands', SQ(21, 'Name a hormone produced by each of the three glands:'), 9,
      stem=[Q14C, M('(ii)', 5)] + Q14CII, id='bio-2021-ol-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'Name one gland from the above list that is both an endocrine and an exocrine',
                                     'gland.'),
      [pt(S('Pancreas or ovaries or testes'), 3)], 'bio-2-4', 'endocrine-and-exocrine',
      SQ(21, 'Name one gland from the list'), 3, stem=[Q14C], id='bio-2021-ol-q14-c-iv'),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'What is phototropism?'), [pt(S('Growth response (of plants) to light'), 3)],
      'bio-2-4', 'phototropism', SQ(22, 'What is phototropism?'), 3, id='bio-2021-ol-q15-a-i'),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Name a part of a plant that responds positively to phototropism.'),
      [pt(S('Stem or leaf or meristem or flower'), 3)], 'bio-2-4', 'positively-phototropic',
      SQ(22, 'Name a part of a plant that responds positively'), 3, id='bio-2021-ol-q15-a-ii'),
    T('15aiii', 'Q15(a)(iii)', 'C', _C(6, 'What benefit does phototropism give to a plant?'),
      [pt(S('Increased photosynthesis (or food production) or increased growth'), 3)], 'bio-2-4',
      'benefit-of-phototropism', SQ(22, 'What benefit does phototropism give to a plant?'), 3,
      id='bio-2021-ol-q15-a-iii'),
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', _C(6, ask, aend), rows, 'bio-2-6', concept, SQ(22, sq), total, stem=[Q15B],
      fig='q15-root', labels=labels, id=old)
    for r, ask, aend, rows, concept, sq, total, labels, old in [
        ('i', 'Name the method by which water moves from the soil into the roots.', None, [pt(S('Osmosis'), 3)],
         'osmosis-into-roots', 'Name the method which water moves', 3, None, 'bio-2021-ol-q15-b-i'),
        ('ii', 'Name the structure labelled A that absorbs water from the soil.', None, [pt(S('Root hair'), 3)],
         'root-hair', 'Name the structure labelled A', 3, only(L_ROOT, 'A'), 'bio-2021-ol-q15-b-ii-fig'),
        ('iii', 'What else could be absorbed through structure A into the root in addition to', 'water?',
         [pt(S('Minerals (or named mineral)'), 3)], 'mineral-uptake', 'What else could be absorbed', 3, None,
         'bio-2021-ol-q15-b-iii'),
        ('iv', 'Name the vessels labelled B that transport water within the roots of a plant.', None,
         [pt(S('Xylem'), 3)], 'xylem', 'Name the vessels labelled B', 3, only(L_ROOT, 'B'), 'bio-2021-ol-q15-b-iv-fig'),
        ('v', 'Describe two ways the vessels labelled B are adapted to their function.', None,
         [anyn(S('Narrow / hollow / tubes / lignin / pits'), 2, 3)], 'adaptations-of-xylem',
         'Describe two ways the vessels labelled B', 6, only(asked(L_ROOT), 'B'), 'bio-2021-ol-q15-b-v'),
        ('vi', 'Name the process responsible for the upward movement of water through the', 'vessels labelled B.',
         [pt(S('Transpiration or root pressure'), 3)], 'transpiration-pull', 'Name the process responsible', 3,
         only(asked(L_ROOT), 'B'), 'bio-2021-ol-q15-b-vi'),
        ('vii', 'Food is transported throughout the plant by C.', 'Name structure C.', [pt(S('Phloem'), 3)], 'phloem',
         'Name structure C:', 3, None, 'bio-2021-ol-q15-b-vii-fig'),
        ('viii', 'Give one way structure C is adapted to carry out its function.', None,
         [pt(S('Living or sieve plates or tubes or companion cells'), 3)], 'adaptations-of-phloem',
         'Give one way structure C is adapted', 3, None, 'bio-2021-ol-q15-b-viii')]
] + [
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'What is meant by the term homeostasis?'),
      [pt(S('Maintaining a constant (or balanced) internal environment'), 3)], 'bio-2-4', 'homeostasis',
      SQ(22, 'What is meant by the term homeostasis?'), 3, id='bio-2021-ol-q15-c-i'),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Give one reason why homeostasis is essential in living organisms.'),
      [pt(S('Maintain metabolism or for enzymes to work'), 3)], 'bio-2-4', 'why-homeostasis',
      SQ(22, 'Give one reason why homeostasis is essential'), 3, id='bio-2021-ol-q15-c-ii'),
] + [
    T(f'15c{r}', f'Q15(c)({r})', 'C', _C(6, ask, aend), rows, topic, concept, SQ(22, sq), total, stem=[Q15C2],
      fig='q15-leaf', labels=labels, id=old)
    for r, ask, aend, rows, topic, concept, sq, total, labels, old in [
        ('iii', 'Name the small openings labelled X', 'through which gas exchange occurs.', [pt(S('Stomata'), 3)],
         'bio-2-6', 'stomata', 'Name the small openings labelled X', 3, only(L_LEAF, 'X'), 'bio-2021-ol-q15-c-iii-fig'),
        ('iv', 'Name one gas excreted through these', 'during respiration.',
         [pt(S('Carbon dioxide or water (vapour)'), 3)], 'bio-2-6', 'gases-through-stomata',
         'Name one gas excreted through these small openings', 3, None, 'bio-2021-ol-q15-c-iv'),
        ('v', 'Name the cells labelled Y that', 'openings.', [pt(S('Guard (cells)'), 3)], 'bio-2-6', 'guard-cells',
         'Name the cells labelled Y', 3, only(L_LEAF, 'Y'), 'bio-2021-ol-q15-c-v-fig'),
        ('vi', 'Name the openings in stems through', 'which gas exchange occurs.', [pt(S('Lenticels'), 3)], 'bio-2-6',
         'lenticels', 'Name the openings in stems', 3, None, 'bio-2021-ol-q15-c-vi'),
        ('vii', 'State any two ways in which plants', 'have adapted to protect themselves.',
         [anyn(S('Thorns / cuticles / heat shock proteins / stings / bark / other correct answer'), 2, 3)], 'bio-2-4',
         'plant-defences', 'State any two ways in which plants have adapted', 6, None, 'bio-2021-ol-q15-c-vii')]
] + [
    # Q16 -------------------------------------------------------------------
    T(f'16a{r}', f'Q16(a)({r})', 'C', _C(7, f'Name the part labelled {x} and give its function.'),
      [pt(S(name, after=f'Name the part labelled {x}'), 3, label=S('Name:', after=f'Name the part labelled {x}')),
       pt(S(func, after=f'Name the part labelled {x}'), 3)], 'bio-2-4', concept,
      SQ(23, f'Name the part labelled {x} and give its function:'), 6, stem=[Q16A], fig='q16-ear',
      labels=only(L_EAR, x), id=f'bio-2021-ol-q16a-{r}-fig')
    for r, x, name, func, concept in [
        ('i', 'A', 'Semi-circular canals', 'Function: Balance', 'semicircular-canals'),
        ('ii', 'B', 'Cochlea', 'Function: Hearing or convert vibrations to nerve impulses', 'cochlea'),
        ('iii', 'C', 'Eardrum', 'Function: Detect sound or pass sound vibrations onto the middle ear', 'eardrum')]
] + [
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'What is connected to the middle ear by the Eustachian tube?'),
      [pt(S('Throat (or pharynx)'), 3)], 'bio-2-4', 'eustachian-tube',
      SQ(23, 'What is connected to the middle ear'), 3, stem=[Q16A], fig='q16-ear', id='bio-2021-ol-q16a-iv'),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'The auditory nerve connects the ear to which organ?'), [pt(S('Brain'), 3)],
      'bio-2-4', 'auditory-nerve', SQ(23, 'The auditory nerve connects the ear to which organ?'), 3, stem=[Q16A],
      fig='q16-ear', id='bio-2021-ol-q16a-v'),
    T('16avi', 'Q16(a)(vi)', 'C', _C(7, 'State how any named disorder of the ear or the eye can be corrected.'),
      [pt(S('Named disorder'), 3, kind='criterion'), pt(S('Method of correction'), 3, kind='criterion')], 'bio-2-4',
      'correcting-ear-and-eye-disorders', SQ(23, 'State how any named disorder'), 6,
      decision='"The ear or the eye": marked on the same two rows; one card.'),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'What is meant by the term respiration?'),
      [pt(S('Obtaining energy from food'), 3)], 'bio-2-2', 'respiration', SQ(23, 'What is meant by the term respiration?'),
      3, id='bio-2021-ol-q16b-i'),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Write a word equation to represent aerobic respiration.'),
      [pt(S('Glucose +', 'Water (+ Energy)'), 6, kind='criterion', units=[3, 3],
          note_sel=S('(only 3m if one part incorrect)', '2(3)'))], 'bio-2-2', 'respiration-word-equation',
      SQ(23, 'Write a word equation to represent aerobic respiration:'), 6, id='bio-2021-ol-q16b-ii'),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'State clearly where stage one and stage two occur within the cell.'),
      [pt(S('Cytosol (or cytoplasm)'), 3, label=S('Stage 1:')), pt(S('Mitochondrion'), 3, label=S('Stage 2:'))],
      'bio-2-2', 'where-respiration-happens', SQ(23, 'State clearly where stage one and stage two'), 6,
      stem=[Q16BIII], id='bio-2021-ol-q16b-iii'),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'What is meant by fermentation?'), [pt(S('Anaerobic respiration'), 3)],
      'bio-2-2', 'fermentation', SQ(23, 'What is meant by fermentation?'), 3, id='bio-2021-ol-q16b-iv'),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'In bread making yeast is used to', 'fermentation produced by yeast.'),
      [pt(S('Alcohol'), 3), pt(S('Carbon dioxide'), 3)], 'bio-2-2', 'products-of-fermentation',
      SQ(23, 'Name the two products of fermentation produced by yeast:'), 6, id='bio-2021-ol-q16b-v'),
] + [
    T(f'16bvi-{route}', 'Q16(b)(vi)', 'C', _C(7, 'Describe a laboratory test for either', 'above.'),
      [pt(S(test), 3), pt(S(result), 3)], 'bio-2-2', f'test-for-{route}',
      SQ(23, 'Describe a laboratory test for either one of the products'), 6, stem=Q16BV, route=route,
      id='bio-2021-ol-q16b-vi' if route == 'carbon-dioxide' else None,
      decision='Closed choose-one pool of the two products, each with its own scheme column: one card each.'
      + (' The old card keeps its id for the carbon dioxide test.' if route == 'carbon-dioxide' else ''))
    for route, test, result in [('carbon-dioxide', 'Limewater test', 'Milky appearance if CO2 is present'),
                                ('ethanol', 'Iodoform test', 'Yellow colour appears if ethanol is present')]
] + [
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'Name the part of the flower which forms the fruit.'),
      [pt(S('Ovary (accept receptacle)'), 3)], 'bio-2-5', 'fruit-formation',
      SQ(24, 'Name the part of the flower which forms the fruit:'), 3, id='bio-2021-ol-q16c-i'),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Why is seed dispersal important?'),
      [pt(S('Reduces competition or colonise new habitats', 'unsuitable conditions'), 3)], 'bio-2-5',
      'why-disperse-seeds', SQ(24, 'Why is seed dispersal important?'), 3, id='bio-2021-ol-q16c-ii'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Give three examples of how seeds are dispersed.'),
      [anyn(S('Wind / water / animal / self'), 3, 3)], 'bio-2-5', 'seed-dispersal',
      SQ(24, 'Give three examples of how seeds are dispersed:'), 9, id='bio-2021-ol-q16c-iii'),
    T('16civ1', 'Q16(c)(iv)1', 'C', item(8, 1, 'What is the function of the testa?', 'Seeds contain an embryo plant'),
      [pt(S('Protection'), 3)], 'bio-2-5', 'testa', SQ(24, 'What is the function of the testa?'), 3,
      stem=[Q16CIV], id='bio-2021-ol-q16c-iv-1'),
    T('16civ2', 'Q16(c)(iv)2', 'C', item(8, 2, 'Name a structure in seeds that stores food.',
                                       'Seeds contain an embryo plant'),
      [pt(S('Cotyledon or endosperm'), 3)], 'bio-2-5', 'food-store-in-seeds',
      SQ(24, 'Name a structure in seeds that stores food:'), 3, stem=[Q16CIV], id='bio-2021-ol-q16c-iv-2'),
    T('16civ3', 'Q16(c)(iv)3', 'C', [item(8, 3, 'Name the structures in the embryo plant that form:',
                                         'Seeds contain an embryo plant'),
                                    _C(8, 'a.', 'The root', br=True), _C(8, 'b.', 'The shoot.', br=True)],
      [pt(S('Radicle'), 3, label=S('a. The root:')), pt(S('b. The shoot: Plumule'), 3)], 'bio-2-5',
      'radicle-and-plumule', SQ(24, 'Name the structures in the embryo plant that form:'), 6, stem=[Q16CIV],
      id='bio-2021-ol-q16c-iv-3'),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Before germination, seeds undergo a period of dormancy.', 'What is dormancy?'),
      [pt(S('Period of no growth or period of inactivity', 'low metabolism'), 3)], 'bio-2-5', 'dormancy',
      SQ(24, 'What is dormancy?'), 3, id='bio-2021-ol-q16c-v'),
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'Explain the term excretion.'),
      [pt(S('Release of waste products of metabolism'), 3)], 'bio-2-6', 'excretion',
      SQ(24, 'Explain the term excretion:'), 3, id='bio-2021-ol-q16d-i'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Name the parts labelled A, B, C.'),
      [pt(S('Kidney'), 3, label=S('A:')), pt(S('Ureter'), 3, label=S('B:')), pt(S('Bladder'), 3, label=S('C:'))],
      'bio-2-6', 'urinary-system', SQ(24, 'Name the parts of the human urinary system labelled A, B, C:'), 9,
      stem=[Q16D], fig='q16-urinary', labels=L_URINARY, id='bio-2021-ol-q16d-ii-fig'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Name two substances excreted by part A.'),
      [anyn(S('(Excess) water / (excess) salts / urea / other correct answer'), 2, 3)], 'bio-2-6', 'excreted-by-kidney',
      SQ(24, 'Name two substances excreted by part A:'), 6, stem=[Q16D], fig='q16-urinary',
      labels=only(asked(L_URINARY), 'A'), id='bio-2021-ol-q16d-iii'),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Give the function of the part labelled C.'), [pt(S('Store urine'), 3)],
      'bio-2-6', 'bladder', SQ(24, 'Give the function of the part labelled C:'), 3, stem=[Q16D], fig='q16-urinary',
      labels=only(asked(L_URINARY), 'C'), id='bio-2021-ol-q16d-iv'),
] + [
    T(f'16dv{n}', f'Q16(d)(v){n}', 'C', item(8, n, head, 'Name the region of part A'),
      [pt(S(*ans), 3)], 'bio-2-6', concept, SQ(24, 'Name the region of part A'), 3, stem=[Q16D, Q16DV],
      fig='q16-urinary', labels=only(asked(L_URINARY), 'A'), id='bio-2021-ol-q16d-v' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, head, ans, concept in [(1, 'Filtration', ('Cortex',), 'site-of-filtration'),
                                  (2, 'Reabsorption.', ('Cortex or medulla',), 'site-of-reabsorption')]
] + [
    T('16dvi', 'Q16(d)(vi)', 'C', _C(8, 'Give the function of the urethra.'),
      [pt(S('Transport urine out of the bladder', 'semen out of body'), 3)], 'bio-2-6', 'urethra',
      SQ(24, 'Give the function of the urethra:'), 3, stem=[Q16D], fig='q16-urinary', id='bio-2021-ol-q16d-vi'),
    # Q17 -------------------------------------------------------------------
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'Identify the structures labelled A, B, C on the diagram.'),
      [pt(S('Fallopian tube (or oviduct)'), 3, label=S('A:')), pt(S('Ovary'), 3, label=S('B:')),
       pt(S('Cervix'), 3, label=S('C:'))], 'bio-2-5', 'female-reproductive-structures',
      SQ(25, 'Identify the structures labelled A, B, C on the diagram:'), 9, stem=[Q17A], fig='q17-foetus',
      labels=L_FOETUS, id='bio-2021-ol-q17a-i-fig'),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Give two functions of the placenta.'),
      [anyn(S('Allows food (or nutrients or named nutrient) to pass to foetus / allows waste',
              'blood and mother’s blood separate'), 2, 3)], 'bio-2-5', 'placenta',
      SQ(25, 'Give two functions of the placenta:'), 6, stem=[Q17A], fig='q17-foetus', id='bio-2021-ol-q17a-ii'),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'Describe two stages that occur during childbirth.'),
      [anyn(S('Waters break / labour', 'placenta delivered'), 2, 3)], 'bio-2-5', 'childbirth',
      SQ(25, 'Describe two stages that occur during childbirth:'), 6, stem=[Q17A], fig='q17-foetus', id='bio-2021-ol-q17a-iii'),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Name the hormone that stimulates the production of breast milk.'),
      [pt(S('Prolactin'), 3)], 'bio-2-5', 'prolactin', SQ(25, 'Name the hormone that stimulates the production'), 3,
      stem=[Q17A], fig='q17-foetus', id='bio-2021-ol-q17a-iv'),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'Give two benefits of breastfeeding.'),
      [anyn(S('(Breast milk) contains antibodies /', 'reduces risk of breast cancer'), 2, 3)], 'bio-2-5',
      'breastfeeding', SQ(25, 'Give two benefits of breastfeeding:'), 6, stem=[Q17A], fig='q17-foetus', id='bio-2021-ol-q17a-v'),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'What is meant by the term photosynthesis?'),
      [pt(S('Making food using (sun)light'), 3)], 'bio-2-2', 'photosynthesis',
      SQ(25, 'What is meant by the term photosynthesis?'), 3, id='bio-2021-ol-q17b-i'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Name the gas in the air that is needed for photosynthesis.'),
      [pt(S('Carbon dioxide'), 3)], 'bio-2-2', 'carbon-dioxide-for-photosynthesis',
      SQ(25, 'Name the gas in the air that is needed for photosynthesis:'), 3, id='bio-2021-ol-q17b-ii'),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'Name the cell organelle in which photosynthesis occurs.'),
      [pt(S('Chloroplast'), 3)], 'bio-2-2', 'chloroplast', SQ(25, 'Name the cell organelle in which photosynthesis'), 3,
      id='bio-2021-ol-q17b-iii'),
] + [
    T(f'17biv{n}', f'Q17(b)(iv){n}', 'C', item(9, n, ask, 'During photosynthesis water is split'),
      [pt(S(ans), 3)], 'bio-2-2', concept, SQ(25, sq), 3, stem=[Q17BIV],
      id='bio-2021-ol-q17b-iv' if n == 1 else None,
      decision=('The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, ask, ans, concept, sq in [
        (1, 'Name the product that is released to the atmosphere.', 'Oxygen', 'oxygen-released',
         '1. Name the product from the splitting of water that is released'),
        (2, 'Name the product that is used to form carbohydrates.', 'Hydrogen ions (or protons) or H+',
         'hydrogen-for-carbohydrates', '2. Name the product from the splitting of water that is used'),
        (3, 'Name the product that passes to chlorophyll.', 'Electrons', 'electrons-to-chlorophyll',
         '3. Name the product that passes to chlorophyll:')]
] + [
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'What is the carbohydrate called that is formed by plants in photosynthesis?'),
      [pt(S('Glucose'), 3)], 'bio-2-2', 'glucose', SQ(25, 'What is the carbohydrate called'), 3, id='bio-2021-ol-q17b-v'),
    T('17bvi', 'Q17(b)(vi)', 'C', _C(9, 'What is the role of chlorophyll in photosynthesis?'),
      [pt(S('Trap energy in (sun)light'), 3)], 'bio-2-2', 'role-of-chlorophyll',
      SQ(25, 'What is the role of chlorophyll in photosynthesis?'), 3, id='bio-2021-ol-q17b-vi'),
    T('17bvii', 'Q17(b)(vii)', 'C', _C(9, 'Give two environmental factors that affect the rate of photosynthesis.'),
      [anyn(S('Temperature / carbon dioxide (concentration) / pH / water (availability) / mineral',
              'light (intensity)'), 2, 3)], 'bio-2-2', 'rate-of-photosynthesis',
      SQ(25, 'Give two environmental factors'), 6, id='bio-2021-ol-q17b-vii'),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'Identify the bacterial structures labelled A, B, C on the diagram.'),
      [pt(S('A: Capsule (allow cell wall) (allow slime layer)'), 3), pt(S('B: DNA (or nucleoid) or chromosome'), 3),
       pt(S('C: Cytosol (or cytoplasm)'), 3)], 'bio-3-2', 'parts-of-a-bacterium',
      SQ(26, 'Identify the bacterial structures labelled A, B, C:'), 9, stem=[Q17C], fig='q17-bacterium',
      labels=L_BACTERIUM, id='bio-2021-ol-q17c-i-fig'),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'What is the function of C?'),
      [pt(S('(Allows for) metabolism or maintains the shape of the cell', 'stores water'), 3)], 'bio-3-2',
      'role-of-cytosol', SQ(26, 'What is the function of C?'), 3, stem=[Q17C], fig='q17-bacterium',
      labels=only(asked(L_BACTERIUM), 'C'), id='bio-2021-ol-q17c-ii-fig'),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'What is meant by the term asexual reproduction?'),
      [pt(S('New organism comes from one parent', 'are involved'), 3)], 'bio-3-2', 'asexual-reproduction',
      SQ(26, 'What is meant by the term asexual reproduction?'), 3, stem=[Q17C], fig='q17-bacterium', id='bio-2021-ol-q17c-iii'),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Name the type of asexual reproduction used by bacteria.'),
      [pt(S('Binary fission'), 3)], 'bio-3-2', 'binary-fission', SQ(26, 'Name the type of asexual reproduction'), 3,
      stem=[Q17C], fig='q17-bacterium', id='bio-2021-ol-q17c-iv'),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'State any two factors that affect the growth of bacteria.'),
      [anyn(S('Temperature / pH / oxygen levels / food / waste levels'), 2, 3)], 'bio-3-2', 'bacterial-growth',
      SQ(26, 'State any two factors that affect the growth of bacteria:'), 6, stem=[Q17C], fig='q17-bacterium', id='bio-2021-ol-q17c-v'),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'Describe two examples of the economic importance of bacteria.'),
      [anyn(S('Dairy products (or named) / silage', 'waste disposal'), 2, 3)], 'bio-3-2', 'useful-bacteria',
      SQ(26, 'Describe two examples of the economic importance of bacteria:'), 6, stem=[Q17C],
      fig='q17-bacterium', id='bio-2021-ol-q17c-vi'),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'Name the parts A, B, C, D.'),
      [pt(S(m), 3, label=S(f'{x}:', after='Question 17 (d)')) for x, m in
       [('A', 'Cell body (not nucleus)'), ('B', 'Dendrites'), ('C', 'Schwann cell (allow myelin)'),
        ('D', 'Axon (allow node of Ranvier)')]], 'bio-2-4', 'parts-of-a-neuron',
      SQ(26, 'Name the parts A, B, C, D:'), 12, stem=[Q17D], fig='q17-neuron', labels=L_NEURON,
      id='bio-2021-ol-q17d-i-fig'),
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'What type of neuron is shown in the diagram?'),
      [pt(S('Motor or interneuron'), 3)], 'bio-2-4', 'type-of-neuron', SQ(26, 'What type of neuron is shown'), 3,
      stem=[Q17D], fig='q17-neuron', id='bio-2021-ol-q17d-ii-fig'),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'Name the gap or region between two neurons.'), [pt(S('Synapse'), 3)],
      'bio-2-4', 'synapse', SQ(26, 'Name the gap or region between two neurons:'), 3, stem=[Q17D],
      fig='q17-neuron', id='bio-2021-ol-q17d-iii'),
    T('17div', 'Q17(d)(iv)', 'C', _C(10, 'What helps the nerve impulse travel across the gap named at part (iii) above?'),
      [pt(S('Neurotransmitters'), 3)], 'bio-2-4', 'neurotransmitters', SQ(26, 'What helps the nerve impulse travel'), 3,
      stem=[Q17D], fig='q17-neuron', id='bio-2021-ol-q17d-iv'),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Name one disorder of the nervous system.'),
      [pt(S('Parkinson’s disease or paralysis or other correct'), 3)], 'bio-2-4', 'nervous-disorders',
      SQ(26, 'Name one disorder of the nervous system:'), 3, stem=[Q17D], fig='q17-neuron', id='bio-2021-ol-q17d-v'),
    T('17dvi', 'Q17(d)(vi)', 'C', _C(10, 'Give a cause and a possible treatment of the disorder named at part (v) above.'),
      [pt(S('Lack of dopamine (Parkinson’s) or injury (paralysis) or other correct'), 3, label=S('Cause:')),
       pt(S('Physiotherapy or medication', 'other correct'), 3, label=S('Possible treatment:'))], 'bio-2-4',
      'treating-nervous-disorders', SQ(26, 'Give a cause and a possible treatment'), 6,
      stem=[Q17D, M('(v)', 10), _C(10, 'Name one disorder of the nervous system.')], fig='q17-neuron', id='bio-2021-ol-q17d-vi'),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q4-table': ('038', 4, (80, 438, 482, 596), SEC, [],
                 'The printed table to complete: Genotypes of parents Bb x bb, then rows (a) Possible gametes, (b) '
                 'Genotype of offspring and (c) Phenotype of offspring, each with empty boxes under each parent.',
                 False),
    'q4-scheme': ('scheme', 8, (105, 448, 502, 600), SEC, [],
                  "The marking scheme's completed table: parents Bb x bb; possible gametes B and b, and b; genotypes "
                  'of offspring Bb and bb; phenotypes Black and Grey.', True),
    'q5-virus': ('038', 5, (188, 78, 495, 282), SEC, ['A', 'B'],
                 'Drawing of a virus: a round outer coat studded with spikes, arrow A pointing to the coat and arrow B '
                 'to the coiled strand inside it.', False),
    'q7-skeleton': ('038', 7, (357, 58, 545, 410), SEC, [],
                    'Photograph of a human skeleton, front view, with a label pointing to the Skull.', False),
    'q8-microscope': ('038', 8, (382, 120, 545, 378), SEC, [],
                      'Drawing of a light microscope seen from the side.', False),
    'q9a-ii-question': ('038', 9, (80, 58, 545, 148), SEC, [],
                        'The printed question: 9. (a) Enzymes play an important role in the body\'s metabolism. The '
                        'word metabolism is underlined. (ii) Explain the underlined word.',
                        False, [(82, 76, 545, 131)]),
    'q9b-vii-question': ('038', 9, (108, 540, 545, 742), SEC, [],
                         'The printed question: (vii) Sketch a graph to show the results of your investigation using '
                         'the axis provided. Below it, a blank pair of axes: Rate of enzyme activity up the side, pH '
                         'along the bottom.', False),
    'q10-dishes': ('038', 10, (116, 188, 538, 375), SEC, [],
                   'Two dishes of agar and test reagent. Dish A, untreated seeds: each seed sits in a clear patch. '
                   'Dish B, treated seeds: labelled Boiled seeds, with no clear patches.', False),
    'q12-watson-crick': ('040', 3, (198, 186, 398, 398), SEC, [],
                         'Black-and-white photograph of two men beside a tall model of DNA, captioned DNA model in '
                         '1953, BBC News.', False),
    'q12c-iv-scheme': ('scheme', 17, (138, 344, 270, 462), SEC, [],
                       "The marking scheme's diagram: a circle divided into a small slice labelled Mitosis and the "
                       'large remainder labelled Interphase.', True),
    'q13-heart': ('040', 4, (305, 147, 548, 367), SEC, ['A', 'B', 'C', 'D', 'E'],
                  'Drawing of a section through the heart: labels point to the Right atrium and the Left ventricle; '
                  'arrow A points to the large vessel entering at the top left, arrow B to a vessel leaving at the '
                  'top, arrow C to the vessel arching at the top right, arrow D to a valve on the left side, and '
                  'arrow E to the wall dividing the two sides.', False, [(305, 324, 329, 367)]),
    'q14-digestive': ('040', 5, (140, 155, 440, 404), SEC, ['A', 'B', 'C', 'D', 'E'],
                      'Drawing of the human digestive system: arrow B points to the large organ at the top left, a '
                      'label Gall bladder to the small sac beneath it, arrow A to the tube leading from below it, '
                      'arrow C to the bag-shaped organ at the top right, arrow D to the organ beneath it, and arrow E '
                      'to the wide tube around the coiled intestine.', False),
    'q14c-i-question': ('040', 5, (80, 509, 545, 545), SEC, [],
                        'The printed question: (c) The human endocrine system produces hormones. The word hormones '
                        'is underlined. (i) Explain the underlined term.', False),
    'q14c-ii-scheme': ('scheme', 21, (180, 155, 410, 400), SEC, [],
                       "The marking scheme's outline of the human body with the glands labelled: Pituitary in the "
                       'head, Thyroid in the neck, Adrenals and Pancreas in the abdomen, Ovaries low in the abdomen '
                       'and Testes below.', True),
    'q15-root': ('040', 6, (62, 110, 502, 300), SEC, ['A', 'B', 'C'],
                 'Drawing of water moving from the soil into a root: labels point to Soil particles, arrow A to a '
                 'long thin outgrowth reaching between them, and arrows show water passing through the cells to a '
                 'bracketed group of tubes B at the right, beside a narrower bracketed group C.', False),
    'q15-leaf': ('040', 6, (334, 546, 535, 708), SEC, ['X', 'Y'],
                 'Drawing of the under surface of a leaf: a sheet of cells labelled Dermal cells, with small oval '
                 'openings; arrow X points to an opening and arrow Y to one of the two cells around it.', False),
    'q16-ear': ('040', 7, (110, 118, 485, 340), SEC, ['A', 'B', 'C'],
                'Drawing of the human ear: arrow A points to the looped canals at the top of the inner ear, arrow B '
                'to the coiled structure below them, and arrow C to the thin membrane at the end of the ear canal; '
                'labels point to the Auditory nerve, the Eustachian tube and the Middle ear.', False),
    'q16-urinary': ('040', 8, (196, 322, 450, 575), SEC, ['A', 'B', 'C'],
                    'Drawing of the human urinary system: arrow A points to one of the two bean-shaped organs, arrow B '
                    'to the tube running down from it, arrow C to the sac at the bottom, and a label Urethra to the '
                    'tube leaving the sac.', False),
    'q17-foetus': ('040', 9, (138, 120, 462, 364), SEC, ['A', 'B', 'C'],
                   'Drawing of a foetus in the womb: arrow A points to one of the tubes at the top, arrow B to the '
                   'oval body at the end of a tube, arrow C to the narrow opening at the bottom of the womb; labels '
                   'point to the Placenta, the Umbilical cord and the Womb wall.', False),
    'q17-bacterium': ('040', 10, (157, 74, 432, 218), SEC, ['A', 'B', 'C'],
                      'Drawing of a rod-shaped bacterium: arrow A points to the outer layer, arrow B to the tangled '
                      'strand in the middle, and arrow C to the dotted fluid filling the cell.', False),
    'q17-neuron': ('040', 10, (128, 372, 466, 520), SEC, ['A', 'B', 'C', 'D'],
                   'Drawing of a neuron: arrow A points to the cell body, arrows B to its branching extensions, arrow '
                   'C to one of the sheath segments along the fibre, and arrow D to the fibre between two segments.',
                   False),
}
