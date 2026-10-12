"""Biology 2025 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover, p2
    instructions, p3-p9 Section A Questions 1-7, p10-p12 Section B Questions
    8-10, p13 Section C answerbook instructions, p14-p15 graph paper, p16-p38
    ruled answer pages, p39 acknowledgements, p40 back cover.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 acknowledgements, p12 back cover.
  * LC025ALP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7 Irish-medium
    bonus, p8-p35 Questions 1-17, p36 blank.

This sitting was already carded (119 authored cards, 106 shipped) before the
review. The review re-derives every task from the PDFs at the scheme's own
mark boundaries, then corrects the existing cards IN PLACE: every existing id
is kept, mapped to the task it was carding (`id=`), and either verified as
already correct or corrected, with the fields it showed before recorded in
the audit (review.corrected[].fieldsBefore). Tasks the old cards bundled
together or left out are added as new cards. BASELINE_COMMIT pins the bank
the corrections are measured against.

Boundary rules, as for 2026: one card per printed address the scheme prices;
an address whose items are separately priced and separately asked (Q14(b)(i)
1.-4., Q15(c)(i) 1.-4., Q17(a)(i) 1.-4.) is carded per item; a list of
required headings (Q13(c)(i)) or one instruction over lettered parts of one
figure (Q4(a), Q11(b)(iv)) stays one card; a long list of separately priced
procedure points (Q9(b)(ii), Q10(b)(i)) is one all-of-N group, since its
points have no printed boundary between them.

Finite printed routes (one card each): Q14(b)(iv) long sightedness or short
sightedness or a hearing defect; Q14(c)(iv) Parkinson's disease or paralysis;
Q15(c)(iii) agriculture or industry or domestic; Q16(b)(vi) bronchitis or
asthma.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2025, 'hl'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = '6bb860204'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2025-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': '23983f696580948ae097280069cd4bc7977fcefaadd3f17dc8c50c016960ee9c',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2025-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': 'd56e7550c86a92f8d9285d7265fd6b0c316f266d1a5d74e75cae425684d9044b',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2025-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'f3417b27f2446080891b3f05444eaeccc06a7b820992a2d371662f2e6ec93843',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 13)},
            13: 'answerbook-instructions', 14: 'graph-paper', 15: 'graph-paper',
            **{p: 'answer-pages' for p in range(16, 39)}, 39: 'acknowledgements',
            40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'acknowledgements',
            12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 36)}, 36: 'blank'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 8)}, **{n: 30 for n in range(8, 11)},
    **{n: 60 for n in range(11, 16)},
}
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (8, 9, 10)}, **{(n, 'b'): 24 for n in (8, 9, 10)},
    **{(n, 'a'): 9 for n in range(11, 16)}, **{(n, 'b'): 27 for n in range(11, 16)},
    **{(n, 'c'): 24 for n in range(11, 16)},
    **{(n, x): 30 for n in (16, 17) for x in 'abcd'},
}
# Q1: "Best five answers from (a) - (f)": six parts at 4, the best five count.
BEST_OF = {1: (5, 4)}

# The examiner tick summary under each scheme block: {mark value: count}.
CHECKSUMS = {
    1: {4: 6},   # printed "5 x4": the best five of the six 4-mark parts carded here
    2: {3: 6, 1: 2}, 3: {2: 1, 3: 6}, 4: {2: 3, 3: 4, 1: 2}, 5: {3: 6, 2: 1},
    6: {2: 3, 3: 4, 1: 2}, 7: {2: 1, 3: 6},
    (8, 'a'): {2: 1, 4: 1}, (8, 'b'): {3: 8}, (9, 'a'): {2: 1, 4: 1}, (9, 'b'): {3: 8},
    (10, 'a'): {4: 1, 2: 1}, (10, 'b'): {3: 8},
    **{(n, 'a'): {3: 3} for n in range(11, 16)},
    (11, 'b'): {3: 9}, (11, 'c'): {3: 8}, (12, 'b'): {3: 9}, (12, 'c'): {3: 8},
    (13, 'b'): {3: 9}, (13, 'c'): {3: 8},
    (14, 'b'): {3: 8, 1: 1, 2: 1}, (14, 'c'): {1: 2, 2: 2, 3: 6},
    (15, 'b'): {3: 7, 2: 3}, (15, 'c'): {3: 8},
    (16, 'a'): {1: 3, 3: 9}, (16, 'b'): {1: 3, 3: 9}, (16, 'c'): {3: 9, 1: 3}, (16, 'd'): {3: 10},
    (17, 'a'): {3: 10}, (17, 'b'): {2: 6, 3: 5, 1: 3}, (17, 'c'): {3: 10},
    (17, 'd'): {3: 6, 1: 8, 2: 2},
}

SCAN_PAGES = {'038': range(2, 13), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card at 4 marks.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 7, 'or', 'Q5 stem "enzymes and/or microorganisms": description, not a choice.'),
    ('038', 9, 'the following', 'Q7 lead-in: every part asked.'),
    ('038', 10, 'any two', 'Section B rubric repeated.'),
    ('038', 10, 'the following', 'Q8(b) lead-in: both parts asked.'),
    ('038', 10, 'any two', 'Q8(b)(ii) "any two abiotic factors": open, priced per factor; one card.'),
    ('038', 11, 'the following', 'Q9(b) lead-in: both parts asked.'),
    ('038', 11, 'or', 'Q9(b)(i) "tissue or membrane": open, one card.'),
    ('038', 12, 'the following', 'Q10(b) lead-in: both parts asked.'),
    ('040', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('040', 3, 'both', 'Q12(b)(ii)1 "heterozygous for both characteristics", not a choice.'),
    ('040', 3, 'both', 'Q12(c)(iii) stem "contain both DNA and RNA", not a choice.'),
    ('040', 3, 'any one', 'Q12(c)(iii) "any one structural difference": scheme alternatives; one card.'),
    ('040', 4, 'or', 'Q13(a) stem "anabolic or catabolic": classification, not a choice.'),
    ('040', 4, 'the following', 'Q13(c)(i) required headings: one card with a row per heading.'),
    ('040', 5, 'both', 'Q14(b) stem "both sense organs", not a choice.'),
    ('040', 5, 'the following', 'Q14(b)(i) four structures, each priced: one card per item.'),
    ('040', 5, 'or', 'Q14(b)(ii) "(A or B)": the answer options.'),
    ('040', 5, 'the following', 'Q14(b)(iii) three structures, each priced: one card per item.'),
    ('040', 5, 'one of the following', 'Q14(b)(iv) closed pool of three disorders: route cards.'),
    ('040', 5, 'or', 'Q14(b)(iv) pool: long sightedness or short sightedness.'),
    ('040', 5, 'or', 'Q14(b)(iv) pool: short sightedness or a hearing defect.'),
    ('040', 5, 'or', 'Q14(c)(i)1 "(X or Y)": the answer options.'),
    ('040', 5, 'or', 'Q14(c)(i)2 "(X or Y)": the answer options.'),
    ('040', 5, 'both', 'Q14(c)(iii) stem "associated with both neurons", not a choice.'),
    ('040', 5, 'or', 'Q14(c)(iv) closed pool (Parkinson\'s disease or paralysis): route cards.'),
    ('040', 6, 'the following', 'Q15(a) three terms, each its own roman part.'),
    ('040', 6, 'any one', 'Q15(b)(iv)1 "any one of its prey": open, one card.'),
    ('040', 6, 'the following', 'Q15(c)(i) four processes, each priced: one card per item.'),
    ('040', 6, 'one of the following', 'Q15(c)(iii) closed pool of three areas: route cards.'),
    ('040', 6, 'or', 'Q15(c)(iii) pool: agriculture or industry.'),
    ('040', 6, 'or', 'Q15(c)(iii) pool: industry or domestic.'),
    ('040', 7, 'any two', 'Q16 any two of (a)-(d): every part carded.'),
    ('040', 7, 'one of the following', 'Q16(b)(vi) closed pool (bronchitis or asthma): route cards.'),
    ('040', 7, 'or', 'Q16(b)(vi) pool: bronchitis or asthma.'),
    ('040', 9, 'any two', 'Q17 any two of (a)-(d): every part carded.'),
    ('040', 9, 'the following', 'Q17(a)(i) four numbered asks, each priced: one card per item.'),
    ('040', 9, 'both', 'Q17(a)(i)1 "Name both circuits": both required in one ask.'),
    ('040', 9, 'the following', 'Q17(a)(ii) two structures, each priced: one card per item.'),
    ('040', 9, 'any three', 'Q17(b)(i) "any three types of joint": open, priced 3(2) + 3(2); one card.'),
    ('040', 9, 'any one', 'Q17(b)(ii) "any one antagonistic muscle pair": open, one card.'),
    ('040', 10, 'the following', 'Q17(c)(v) three numbered asks, each priced: one card per item.'),
    ('040', 10, 'the following', 'Q17(d)(i) X, Y and Z marked on the one drawing: one card.'),
]

ROUTES = {
    'Q14(b)(iv)': ['long-sightedness', 'short-sightedness', 'hearing-defect'],
    'Q14(c)(iv)': ['parkinsons-disease', 'paralysis'],
    'Q15(c)(iii)': ['agriculture', 'industry', 'domestic'],
    'Q16(b)(vi)': ['bronchitis', 'asthma'],
}

# The Topic Atlas files Unit 1 (Scientific knowledge) with the investigating-
# in-science heading: no separate reference topic exists for it.
ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

# Pre-existing cards no task maps to. Each is a figure twin the build never
# shipped (superseded by its base card), or a card whose task is carded under
# its base id; withdrawn explicitly below so a corrected base cannot expose it.
_TWIN = ('Never shipped: a figure twin superseded by its base card {b}, which now '
         'carries the reviewed task and its figure. Withdrawn so the corrected base\'s '
         'questionRef cannot expose it as a duplicate.')
_TWINS = {
    'bio-2025-hl-q3-a-fig': 'bio-2025-hl-q3-a', 'bio-2025-hl-q4-ab-fig': 'bio-2025-hl-q4-ab',
    'bio-2025-hl-q5-a-fig': 'bio-2025-hl-q5-a', 'bio-2025-hl-q5-b-fig': 'bio-2025-hl-q5-b',
    'bio-2025-hl-q6-a-fig': 'bio-2025-hl-q6-a', 'bio-2025-hl-q6-b-fig': 'bio-2025-hl-q6-b',
    'bio-2025-hl-q6-c-fig': 'bio-2025-hl-q6-c',
    'bio-2025-hl-q11-b-iv-vi-fig': 'bio-2025-hl-q11-b-iv-vi',
    'bio-2025-hl-q14-c-i-fig': 'bio-2025-hl-q14-c-neuron-id',
    'bio-2025-hl-q16-a-iv-1-fig': 'bio-2025-hl-q16-a-iv-1',
    'bio-2025-hl-q16-c-iii-fig': 'bio-2025-hl-q16-c-iii',
    'bio-2025-hl-q17-a-i-fig': 'bio-2025-hl-q17-a-i',
}
RETAINED = {k: _TWIN.format(b=v) for k, v in _TWINS.items()}
WITHDRAW = {k: (v, _TWIN.format(b=v)) for k, v in _TWINS.items()}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def listed(page, anchor, ends, doc='040'):
    """A printed numbered list ("1." on its own line, its item on the next)."""
    return [Q(page, f'{i}.', end, doc=doc, after=anchor, br=True)
            for i, end in enumerate(ends, 1)]


Q1 = _A(3, 'Answer any five of the following parts (a) to (f):')
Q2 = _A(4, 'The diagram shows a longitudinal section through the', 'root of a plant.')
Q3 = _A(5, 'Aerobic respiration is a two-stage process.', 'cell organelle shown.')
Q4 = _A(6, 'The diagram below shows part of the ultrastructure of a cell membrane.')
Q4D = _A(6, 'Plant cells have a cell wall in addition to a cell', 'membrane.')
Q5 = _A(7, 'The image shows a piece of equipment', 'equipment shown.')
Q6 = _A(8, 'The diagram shows the human digestive system.')
Q7 = _A(9, 'Answer the following questions in relation to the scientific method.')
Q8B = _A(10, 'Answer the following questions based on your study', 'ecosystem.')
Q9B = _A(11, 'Answer the following questions in relation to a laboratory', 'demonstrate osmosis.')
Q10B = _A(12, 'Answer the following questions in relation to an investigation', 'leaf yeast.')
Q11A = _C(2, 'Tropisms are important for plants.')
Q11B = _C(2, 'The diagram shows the arrangement of the cells', 'a flowering plant.')
Q11C = _C(2, 'Sexual reproduction results in seed formation', 'dormancy.')
Q11CIV = _C(2, 'Some plants reproduce asexually by means of vegetative propagation.')
Q12B = _C(3, 'In fruit flies, the genes for body', 'for curly wing (n).')
Q13A = _C(4, 'Metabolic reactions can be classified as anabolic or catabolic.')
Q13B = _C(4, 'During photosynthesis chlorophyll absorbs', 'light energy.')
Q13C = _C(4, 'Enzymes control metabolic reactions', 'photosynthesis.')
Q14A = _C(5, 'The nervous system is composed of', 'nervous system (PNS).')
Q14B = _C(5, 'The eye and the ear are both sense organs', 'external stimuli.')
Q14C = _C(5, 'Neurons are the functional unit of the nervous system.')
Q14CI = _C(5, 'The diagrams show two neurons', '(X and Y).')
Q15B = [_C(6, 'White-tailed sea eagles were once widespread', 'other small mammals.'),
        _C(6, 'Adapted from White-tailed eagles breed')]
Q15C = _C(6, 'The following processes occur in the nitrogen cycle.')
Q16A = _C(7, 'The diagram shows Rhizopus.')
Q16B = _C(7, 'The diagram shows gases X and Y and their main', 'exchange in the lungs.')
Q16C = _C(8, 'The cell cycle involves interphase and mitosis.')
Q16D = _C(8, 'Lymphocytes, such as the one shown in the', 'part of the human defence system.')
Q17A = _C(9, 'Using the diagram as an aid, answer the', 'following questions:')
Q17B = _C(9, 'The diagrams show some types of joints of the human skeleton.')
Q17C = _C(10, 'Homeostasis is an important process in living organisms.')
Q17CV = [_C(10, 'The graphs (X and Y) show the relationship', 'exercising vigourously.'),
         _C(10, 'Using the information given in the description above', 'following questions.')]

EACH_EYE = _C(5, 'Describe the role of each of the following in the eye:')
EACH_EAR = _C(5, 'Describe the role of each of the', 'following in the ear:', nth=2)
NITROGEN = _C(6, 'Outline what is occurring during each process.')


def item(page, n, ends, doc='040', after=None):
    """Printed item n of a numbered list (number on its own line)."""
    return Q(page, f'{n}.', ends, doc=doc, after=after)


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Write the general formula for carbohydrates.'),
      [pt(S('Cx(H2O)y'), 4)], 'bio-1-2', 'carbohydrate-general-formula',
      SQ(8, 'Write the general formula'), 4, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Give the four chemical elements found in all proteins.'),
      [pt(S('Carbon (or C) and hydrogen'), 4, kind='allOf')], 'bio-1-2', 'elements-in-protein',
      SQ(8, 'Give the four chemical elements'), 4, stem=[Q1],
      decision='One 4-mark line naming all four elements: one all-of row.'),
    T('1c', 'Q1(c)', 'A', _A(3, 'State one structural role of proteins in the body.'),
      [pt(S('(To form) muscles'), 4)], 'bio-1-2', 'structural-role-of-protein',
      SQ(8, 'State one structural role'), 4, stem=[Q1]),
    T('1d', 'Q1(d)', 'A', _A(3, 'Name the small subunits that make protein.'),
      [pt(S('Amino acids'), 4)], 'bio-1-2', 'amino-acids', SQ(8, 'Name the small subunits'), 4,
      stem=[Q1]),
    T('1e', 'Q1(e)', 'A', _A(3, 'Name one water-soluble vitamin.'),
      [pt(S('B (or named B vitamin)'), 4)], 'bio-1-2', 'water-soluble-vitamins',
      SQ(8, 'Name one water-soluble vitamin.'), 4, stem=[Q1]),
    T('1f', 'Q1(f)', 'A', _A(3, 'Give one example of a trace element found in food.'),
      [pt(S('Copper (or Cu)'), 4)], 'bio-1-2', 'trace-elements',
      SQ(8, 'Give one example of a trace element'), 4, stem=[Q1]),
    T('2a', 'Q2(a)', 'A', _A(4, 'Name the structure indicated by the letter X and', 'give its function.'),
      [pt(S('Root hair'), 3, label=S('Name:')),
       pt(S('Absorption of water or minerals'), 3, label=S('Function:'))],
      'bio-2-6', 'root-hair', SQ(9, 'Name structure indicated by the letter X'), 6,
      stem=[Q2], fig='q2-root', id='bio-2025-hl-q2-abc-fig',
      decision='The old card bundled (a)-(c); it keeps its id for (a), and (b) and (c) are added.'),
    T('2b', 'Q2(b)', 'A', _A(4, 'Name the tissue type indicated by the letter Y and', 'give its function.'),
      [pt(S('Vascular (tissue)'), 3, label=S('Name:')),
       pt(S('Transport of a correct named substance'), 3, kind='criterion', label=S('Function:'))],
      'bio-2-6', 'vascular-tissue', SQ(9, 'Name the tissue type indicated'), 6,
      stem=[Q2], fig='q2-root'),
    T('2c', 'Q2(c)', 'A', _A(4, 'Name the tissue indicated by the letter Z where', 'rapid mitosis is occurring.'),
      [pt(S('Meristematic'), 3)], 'bio-2-6', 'meristematic-tissue',
      SQ(9, 'Name the tissue indicated by the letter Z'), 3, stem=[Q2], fig='q2-root'),
    T('2d', 'Q2(d)', 'A', _A(4, 'In the space below, draw and label a transverse section', 'in the diagram above.'),
      [pt(S('circle with vascular tissue clearly visible'), 3, kind='criterion', label=S('Drawing:')),
       anyn(S('dermal (tissue) / vascular', 'examples'), 2, 1)],
      'bio-2-6', 'root-transverse-section', SQ(9, 'In the space below, draw and label'), 5,
      stem=[Q2], fig='q2-root'),
    T('3a', 'Q3(a)', 'A', _A(5, 'Name the cell organelle shown.'),
      [pt(S('Mitochondrion'), 2)], 'bio-1-3', 'mitochondrion', SQ(10, 'Name the cell organelle shown.'), 2,
      stem=[Q3], fig='q3-mitochondrion'),
    T('3b', 'Q3(b)', 'A', _A(5, 'Name the cycle of reactions that occurs in', 'aerobic respiration.'),
      [pt(S('Krebs'), 3)], 'bio-2-2', 'krebs-cycle', SQ(10, 'Name the cycle of reactions'), 3,
      stem=[Q3], fig='q3-mitochondrion'),
    T('3c', 'Q3(c)', 'A', _A(5, 'ATP is produced in large quantities', 'What does ATP stand for?'),
      [pt(S('Adenosine triphosphate'), 3)], 'bio-2-2', 'atp', SQ(10, 'What does ATP stand for?'), 3),
    T('3d', 'Q3(d)', 'A', _A(5, 'NAD+ is an important molecule in respiration.', 'Give the function of NAD+.'),
      [pt(S('Carries (high energy) electrons'), 3)], 'bio-2-2', 'nad-coenzyme',
      SQ(10, 'Give the function of NAD+.'), 3),
    T('3e', 'Q3(e)', 'A', _A(5, 'Suggest a condition under which anaerobic'),
      [pt(S('Lack of oxygen or described'), 3)], 'bio-2-2', 'anaerobic-respiration-conditions',
      SQ(10, 'Suggest a condition under which'), 3,
      stem=[_A(5, 'Anaerobic respiration may occur under certain conditions.')]),
    T('3f', 'Q3(f)', 'A', _A(5, 'State where anaerobic respiration occurs in a cell.'),
      [pt(S('Cytosol'), 3)], 'bio-2-2', 'anaerobic-respiration-site',
      SQ(10, 'State where anaerobic respiration'), 3,
      stem=[_A(5, 'Anaerobic respiration may occur under certain conditions.')]),
    T('3g', 'Q3(g)', 'A', _A(5, 'Name one main product of anaerobic respiration.'),
      [pt(S('Lactic acid or ethanol'), 3)], 'bio-2-2', 'anaerobic-respiration-products',
      SQ(10, 'Name one main product'), 3,
      stem=[_A(5, 'Anaerobic respiration may occur under certain conditions.')]),
    T('4a', 'Q4(a)', 'A', _A(6, 'Name the parts labelled X and Y.'),
      [pt(S('Phospholipid'), 2, label=S('X:')), pt(S('Protein'), 2, label=S('Y:'))],
      'bio-1-3', 'cell-membrane-structure', SQ(11, 'Name the parts labelled X and Y.'), 4,
      stem=[Q4], fig='q4-membrane', id='bio-2025-hl-q4-ab',
      labels=[L('X', S('Phospholipid', page=11), True), L('Y', S('Protein', page=11), True)],
      decision='The old card bundled (a) and (b), and (b) also had a card of its own; it keeps '
               'its id for (a).'),
    T('4b', 'Q4(b)', 'A', _A(6, 'Give a function of the cell membrane.'),
      [pt(S('Controls what substances pass through'), 3)], 'bio-1-3', 'cell-membrane-function',
      SQ(11, 'Give a function of the cell membrane.'), 3),
    T('4ci', 'Q4(c)(i)', 'A', _A(6, 'What term describes cells without membrane-bound organelles?'),
      [pt(S('Prokaryotic'), 3)], 'bio-1-3', 'prokaryotic-cells',
      SQ(11, 'What term describes cells without'), 3, id='bio-2025-hl-q4-c',
      decision='The old card bundled (c)(i) and (ii); it keeps its id for (i).'),
    T('4cii', 'Q4(c)(ii)', 'A', _A(6, 'What term describes cells with membrane-bound organelles?'),
      [pt(S('Eukaryotic'), 3)], 'bio-1-3', 'eukaryotic-cells',
      SQ(11, 'What term describes cells with membrane-bound'), 3),
    T('4di', 'Q4(d)(i)', 'A', _A(6, 'Sketch the basic structure of a plant cell', 'the cell wall.'),
      [pt(S('showing cell membrane and cell wall'), 3, kind='criterion', label=S('Correct sketch:')),
       pt(S('Cell membrane', after='Labels:'), 1, label=S('Labels:')),
       pt(S('Cell wall', after='Labels:'), 1, label=S('Labels:'))],
      'bio-1-3', 'plant-cell-sketch', SQ(11, 'Sketch the basic structure'), 5, stem=[Q4D]),
    T('4dii', 'Q4(d)(ii)', 'A', _A(6, 'Give one function of a plant cell wall.'),
      [pt(S('Gives shape (to the cell)'), 2)], 'bio-1-3', 'plant-cell-wall-function',
      SQ(11, 'Give one function of a plant cell wall.'), 2, stem=[Q4D]),
    T('5a', 'Q5(a)', 'A', _A(7, 'What is the common name given to this piece of equipment?'),
      [pt(S('Bioreactor'), 3)], 'bio-3-2', 'bioreactor', SQ(12, 'What is the common name'), 3,
      stem=[Q5], fig='q5-bioreactor'),
    T('5b', 'Q5(b)', 'A', _A(7, 'Name two factors controlled by the piece of equipment', 'nutrient availability.'),
      [anyn(S('pH / temperature / pressure / oxygen'), 2, 3)], 'bio-3-2', 'bioreactor-growth-factors',
      SQ(12, 'Name two factors controlled'), 6, stem=[Q5], fig='q5-bioreactor'),
    T('5c', 'Q5(c)', 'A', _A(7, 'Name the two stages X and Y on the population growth curve.'),
      [pt(S('Log'), 3, label=S('Stage X:')), pt(S('Stationary'), 3, label=S('Stage Y:'))],
      'bio-3-2', 'bacterial-growth-curve', SQ(12, 'Name the two stages X and Y'), 6,
      stem=[Q5], fig='q5-bioreactor', id='bio-2025-hl-q5-c-fig'),
    T('5d', 'Q5(d)', 'A', _A(7, 'The piece of equipment is keeping the population', 'growth curve shown?'),
      [pt(S('Continuous'), 3)], 'bio-3-2', 'continuous-flow-processing',
      SQ(12, 'Which type of food processing technique'), 3, stem=[Q5], fig='q5-bioreactor',
      id='bio-2025-hl-q5-d-fig'),
    T('5e', 'Q5(e)', 'A', _A(7, 'If the population of bacteria in the piece of equipment', 'how the line would continue.'),
      [pt(S('Line drops'), 2)], 'bio-3-2', 'decline-phase', SQ(12, 'If the population of bacteria'), 2,
      stem=[Q5], fig='q5-bioreactor'),
    T('6a', 'Q6(a)', 'A', _A(8, 'Name the parts labelled A and B.'),
      [pt(S('Oesophagus'), 2, label=S('A:')), pt(S('Stomach'), 2, label=S('B:'))],
      'bio-2-6', 'digestive-system-parts', SQ(13, 'Name the parts labelled A and B.'), 4,
      stem=[Q6], fig='q6-digestive',
      labels=[L('A', S('Oesophagus', page=13), True), L('B', S('Stomach', page=13), True)]),
    T('6b', 'Q6(b)', 'A', _A(8, 'Name and describe briefly the method by which', 'through structure A.'),
      [pt(S('Peristalsis'), 3, label=S('Name:')), pt(S('Description:'), 3)],
      'bio-2-6', 'peristalsis', SQ(13, 'Name and describe briefly'), 6, stem=[Q6], fig='q6-digestive'),
    T('6c', 'Q6(c)', 'A', _A(8, 'How does the pH of the food material change as', 'from A to B?'),
      [pt(S('Lowers'), 2)], 'bio-2-6', 'stomach-ph', SQ(13, 'How does the pH'), 2, stem=[Q6],
      fig='q6-digestive'),
    T('6d', 'Q6(d)', 'A', _A(8, 'Name the enzyme produced in the pancreas which digests lipids.'),
      [pt(S('Lipase'), 3)], 'bio-2-6', 'pancreatic-lipase', SQ(13, 'Name the enzyme produced'), 3,
      stem=[Q6], fig='q6-digestive'),
    T('6e', 'Q6(e)', 'A', _A(8, 'In the space below, draw and label the internal structure of a villus.'),
      [pt(S('Drawing: villus / lacteal / blood vessels'), 3, kind='criterion',
          note_sel=S('Any two', after='blood vessels')),
       anyn(S('villus / lacteal / capillary'), 2, 1)],
      'bio-2-6', 'villus-structure', SQ(13, 'Draw and label the internal structure'), 5,
      stem=[_A(8, 'The villus is present in the small intestine.')]),
    T('7a', 'Q7(a)', 'A', _A(9, 'In the scientific method, a testable statement', 'in the box below.'),
      [pt(S('Hypothesis'), 2)], 'bio-u2', 'hypothesis', SQ(14, 'In the scientific method, a testable'), 2,
      stem=[Q7], id='bio-2025-hl-q7-ab',
      decision='The old card bundled (a) and (b); it keeps its id for (a), and (b) is added.'),
    T('7b', 'Q7(b)', 'A', _A(9, 'How can this statement be tested?'),
      [pt(S('Conducting an experiment'), 3)], 'bio-u2', 'testing-a-hypothesis',
      SQ(14, 'How can this statement be tested?'), 3,
      stem=[Q7, M('(a)', 9), _A(9, 'In the scientific method, a testable statement', 'in the box below.')]),
    T('7c', 'Q7(c)', 'A', _A(9, 'What is the function of a scientific control?'),
      [pt(S('A comparison to the experiment'), 3)], 'bio-u2', 'scientific-control',
      SQ(14, 'What is the function of a scientific control?'), 3, stem=[Q7]),
    T('7d', 'Q7(d)', 'A', _A(9, 'Give two limitations of the scientific method.'),
      [anyn(S('Accidental discovery /', 'experimental design……….'), 2, 3)], 'bio-u1',
      'limitations-of-science', SQ(14, 'Give two limitations'), 6, stem=[Q7]),
    T('7e', 'Q7(e)', 'A', _A(9, 'Where does a biologist normally publish their results?'),
      [pt(S('Scientific journal'), 3)], 'bio-u1', 'scientific-publication',
      SQ(14, 'Where does a biologist normally publish'), 3, stem=[Q7]),
    T('7f', 'Q7(f)', 'A', _A(9, 'What is meant by the term theory?'),
      [pt(S('Supported (or tested) hypothesis'), 3)], 'bio-u1', 'scientific-theory',
      SQ(14, 'What is meant by the term theory?'), 3, stem=[Q7]),
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(10, 'What is meant by the term ecosystem?'),
      [pt(S('Organisms and their environment'), 2)], 'bio-3-1', 'ecosystem',
      SQ(15, 'What is meant by the term ecosystem?'), 2),
    T('8aii', 'Q8(a)(ii)', 'B', _A(10, 'What could aid ecologists in identifying organisms'),
      [pt(S('Key'), 4)], 'bio-3-1', 'identification-key', SQ(15, 'What could aid ecologists'), 4),
    T('8bi', 'Q8(b)(i)', 'B', _A(10, 'Describe how you carried out a quantitative study'),
      [pt(S('Named plant species'), 3, kind='criterion'),
       pt(S('Used a quadrat or line transect'), 3),
       pt(S('Counted and repeated'), 3, kind='allOf'),
       pt(S('Calculation described'), 3, kind='criterion')],
      'bio-3-1', 'quantitative-plant-study', SQ(15, 'Describe how you carried out a quantitative'), 12,
      stem=[Q8B]),
    T('8bii', 'Q8(b)(ii)', 'B', _A(10, 'Name any two abiotic factors you have investigated', 'measured each factor.'),
      [pt(S('Correctly named abiotic factor 1'), 3, kind='criterion'),
       pt(S('Matching method of measurement of factor 1'), 3, kind='criterion'),
       pt(S('Correctly named abiotic factor 2'), 3, kind='criterion'),
       pt(S('Matching method of measurement of factor 2'), 3, kind='criterion')],
      'bio-3-1', 'abiotic-factors-measured', SQ(15, 'Name any two abiotic factors'), 12, stem=[Q8B]),
    T('9a', 'Q9(a)', 'B', _A(11, 'Explain the term osmosis.'),
      [pt(S('Movement of water'), 2), pt(S('from a region of higher water concentration', 'membrane'), 4)],
      'bio-2-6', 'osmosis', SQ(16, 'Explain the term osmosis.'), 6),
    T('9bi', 'Q9(b)(i)', 'B', _A(11, 'Name the tissue or membrane that you used in the activity.'),
      [pt(S('Correctly named tissue or membrane'), 3, kind='criterion')], 'bio-2-6',
      'osmosis-tissue-or-membrane', SQ(16, 'Name the tissue or membrane'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', _A(11, 'Describe how you carried out this activity', 'if you wish.'),
      [anyn(None, 7, 3, options=[
          S('Description how tissue or membrane'), S('Correct use of salt or sugar'),
          S('Control named and setup described'), S('Left for a time'),
          S('Matching result for test'), S('Matching result for control'),
          S('Named piece of apparatus used')], note_sel=S('Points may be obtained'))],
      'bio-2-6', 'osmosis-demonstration', SQ(16, 'Describe how you carried out this activity'), 21,
      stem=[Q9B],
      decision='Seven separately priced procedure points with no printed boundary between them: '
               'one all-of-seven group.'),
    T('10ai', 'Q10(a)(i)', 'B', _A(12, 'To which kingdom of living organisms do yeast belong?'),
      [pt(S('*Fungi'), 4)], 'bio-3-2', 'yeast-kingdom', SQ(17, 'To which kingdom'), 4),
    T('10aii', 'Q10(a)(ii)', 'B', _A(12, 'Working with microorganisms often involves sterility.', 'the term sterility.'),
      [pt(S('Absence of all (micro)organisms'), 2)], 'bio-3-2', 'sterility',
      SQ(17, 'Explain the term sterility.'), 2),
    T('10bi', 'Q10(b)(i)', 'B', _A(12, 'Describe how you set up the investigation.', 'if you wish.'),
      [anyn(None, 6, 3, options=[
          S('Named piece of apparatus used'), S('Correct position of leaf'),
          S('Left at a suitable temperature'), S('Left for a suitable time'),
          S('Control named and setup described'), S('Safety precaution described')],
          note_sel=S('Points may be obtained'))],
      'bio-3-2', 'leaf-yeast-isolation', SQ(17, 'Describe how you set up the investigation.'), 18,
      stem=[Q10B],
      decision='Six separately priced procedure points with no printed boundary between them: '
               'one all-of-six group.'),
    T('10bii', 'Q10(b)(ii)', 'B', _A(12, 'Describe the result of the investigation', 'successfully.'),
      [pt(S('Pink colonies (in test)'), 3), pt(S('No growth (in control)'), 3)],
      'bio-3-2', 'leaf-yeast-result', SQ(17, 'Describe the result of the investigation'), 6, stem=[Q10B]),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'What is geotropism?'),
      [pt(S('Growth response (of a plant) to gravity.'), 3)], 'bio-2-4', 'geotropism',
      SQ(18, 'What is geotropism?'), 3, stem=[Q11A], id='bio-2025-hl-q11-a',
      decision='The old card bundled (a)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Name a part of a plant that responds positively to geotropism.'),
      [pt(S('*Root'), 3)], 'bio-2-4', 'positive-geotropism', SQ(18, 'Name a part of a plant'), 3,
      stem=[Q11A]),
    T('11aiii', 'Q11(a)(iii)', 'C', _C(2, 'How does this growth response benefit plants?'),
      [pt(S('Obtain (more) water or minerals or anchorage'), 3)], 'bio-2-4', 'benefit-of-geotropism',
      SQ(18, 'How does this growth response'), 3,
      stem=[Q11A, M('(ii)', 2), _C(2, 'Name a part of a plant that responds positively to geotropism.')]),
    T('11bi1', 'Q11(b)(i)1', 'C', _C(2, 'The male reproductive parts of the flower.'),
      [pt(S('*Stamen'), 3)], 'bio-2-5', 'stamen', SQ(18, '1. The male reproductive parts'), 3,
      stem=[Q11B, _C(2, 'Give the collective name for:')], fig='q11-embryo-sac', id='bio-2025-hl-q11-b-i',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('11bi2', 'Q11(b)(i)2', 'C', _C(2, 'The female reproductive parts of the flower.'),
      [pt(S('*Carpel'), 3)], 'bio-2-5', 'carpel', SQ(18, '2. The female reproductive parts'), 3,
      stem=[Q11B, _C(2, 'Give the collective name for:')], fig='q11-embryo-sac'),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Name the specific part of the flower that holds the embryo sac.'),
      [pt(S('*Ovule (accept ovary)'), 3)], 'bio-2-5', 'ovule', SQ(18, 'Name the specific part of the flower'), 3,
      stem=[Q11B], fig='q11-embryo-sac', id='bio-2025-hl-q11-b-ii-iii',
      decision='The old card bundled (ii) and (iii); it keeps its id for (ii), and (iii) is added.'),
    T('11biii', 'Q11(b)(iii)', 'C', _C(2, 'The embryo sac develops from a single diploid cell.', 'Name this cell.'),
      [pt(S('*Megaspore mother (cell)'), 3)], 'bio-2-5', 'megaspore-mother-cell',
      SQ(18, 'The embryo sac develops from'), 3, stem=[Q11B], fig='q11-embryo-sac'),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'Name the parts labelled P and Q in the embryo sac', 'fertilisation.'),
      [pt(S('*Polar nucleus'), 3, label=S('P:')), pt(S('*Egg (cell)'), 3, label=S('Q:'))],
      'bio-2-5', 'polar-nucleus-and-egg', SQ(18, 'Name the parts labelled P and Q'), 6,
      stem=[Q11B], fig='q11-embryo-sac', id='bio-2025-hl-q11-b-iv-vi',
      labels=[L('P', S('*Polar nucleus', page=18), True), L('Q', S('*Egg (cell)', page=18), True)],
      decision='The old card bundled (iv)-(vi); it keeps its id for (iv), and (v), (vi) are added.'),
    T('11bv', 'Q11(b)(v)', 'C', _C(2, 'Explain why parts P and Q are genetically identical.'),
      [pt(S('They were produced by mitosis'), 3)], 'bio-2-5', 'p-and-q-identical',
      SQ(18, 'Explain why parts P and Q'), 3, stem=[Q11B], fig='q11-embryo-sac',
      labels=[L('P', S('*Polar nucleus', page=18), True), L('Q', S('*Egg (cell)', page=18), True)]),
    T('11bvi', 'Q11(b)(vi)', 'C', _C(2, 'State what each of the parts P and Q develop into', 'double fertilisation.'),
      [pt(S('Endosperm'), 3, label=S('P:', after='(vi)')), pt(S('Diploid zygote'), 3, label=S('Q:', after='(vi)'))],
      'bio-2-5', 'double-fertilisation-products', SQ(18, 'State what each of the parts P and Q'), 6,
      stem=[Q11B], fig='q11-embryo-sac',
      labels=[L('P', S('*Polar nucleus', page=18), True), L('Q', S('*Egg (cell)', page=18), True)]),
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Name two methods by which seeds are dispersed.'),
      [anyn(S('Wind / animal / water / self'), 2, 3)], 'bio-2-5', 'seed-dispersal-methods',
      SQ(19, 'Name two methods by which seeds'), 6, stem=[Q11C], id='bio-2025-hl-q11-c-i-ii',
      decision='The old card bundled (c)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Give two advantages of seed dispersal to a plant species.'),
      [anyn(S('Reduce competition /', 'survival ……….'), 2, 3)], 'bio-2-5',
      'seed-dispersal-advantages', SQ(19, 'Give two advantages of seed dispersal'), 6, stem=[Q11C]),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'Give two advantages of dormancy to a plant species.'),
      [anyn(S('Allows time for development of embryo /', 'unfavourable conditions……….'), 2, 3)],
      'bio-2-5', 'dormancy-advantages', SQ(19, 'Give two advantages of dormancy'), 6, stem=[Q11C]),
    T('11civ1', 'Q11(c)(iv)1', 'C', _C(2, 'Give one example of a plant that reproduces asexually using leaves.'),
      [pt(S('Correct example given'), 3, kind='criterion')], 'bio-2-5', 'vegetative-propagation-leaves',
      SQ(19, 'Give one example of a plant that reproduces asexually using leaves.'), 3, stem=[Q11CIV]),
    T('11civ2', 'Q11(c)(iv)2', 'C', _C(2, 'Give one example of a plant that reproduces asexually using buds.'),
      [pt(S('Correct example given'), 3, kind='criterion')], 'bio-2-5', 'vegetative-propagation-buds',
      SQ(19, 'Give one example of a plant that reproduces asexually using buds.'), 3, stem=[Q11CIV]),
    T('12ai', 'Q12(a)(i)', 'C', _C(3, 'Explain the term mutation.'),
      [pt(S('Change in the structure (or sequence)'), 3)], 'bio-2-3', 'mutation',
      SQ(20, 'Explain the term mutation.'), 3, id='bio-2025-hl-q12-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('12aii', 'Q12(a)(ii)', 'C', _C(3, 'Give two causes of mutations.'),
      [anyn(S('Radiation / chemicals / viruses'), 2, 3)], 'bio-2-3', 'causes-of-mutation',
      SQ(20, 'Give two causes of mutations.'), 6),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'Distinguish between the', 'gene and allele.'),
      [pt(S('Gene:', 'a protein.'), 3), pt(S('Allele:'), 3)], 'bio-1-4', 'gene-vs-allele',
      SQ(20, 'Distinguish between the terms, gene and allele.'), 6),
    T('12bii1', 'Q12(b)(ii)1', 'C', _C(3, 'Using the letters', 'for both characteristics.'),
      [pt(S('*EeNn'), 3)], 'bio-1-4', 'dihybrid-genotype-heterozygous',
      SQ(20, '1. Using the letters mentioned above'), 3, stem=[Q12B], fig='q12-flies',
      id='bio-2025-hl-q12-b-ii-1-2',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('12bii2', 'Q12(b)(ii)2', 'C', _C(3, 'Give the genotype of a fruit fly with a black body and curly wings.'),
      [pt(S('*eenn'), 3)], 'bio-1-4', 'dihybrid-genotype-recessive',
      SQ(20, '2. Give the genotype for a fruit fly'), 3, stem=[Q12B], fig='q12-flies'),
    T('12bii3', 'Q12(b)(ii)3', 'C', _C(3, 'Give all the possible genotypes and matching phenotypes', '1. and 2. above.'),
      [pt(S(row), 3, note_sel=S('If phenotype not matched', 'correct genotype', after='black, curly'))
       for row in ('*EeNn and ebony, normal', '*Eenn and ebony, curly', '*eeNn and black, normal',
                   '*eenn and black, curly')],
      'bio-1-4', 'dihybrid-cross-offspring', SQ(20, '3. Give all the possible genotypes'), 12,
      stem=[Q12B, M('1.', 3), _C(3, 'Using the letters', 'for both characteristics.'),
            M('2.', 3), _C(3, 'Give the genotype of a fruit fly with a black body and curly wings.')],
      fig='q12-flies'),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'What term is used for genes found on the same chromosome?'),
      [pt(S('*Linked'), 3)], 'bio-1-4', 'linked-genes', SQ(20, 'What term is used for genes'), 3),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'DNA contains a pattern of bases', 'What do the letters DNA stand for?'),
      [pt(S('*Deoxyribonucleic acid'), 3)], 'bio-1-2', 'dna-name', SQ(21, 'What do the letters DNA stand for?'), 3,
      id='bio-2025-hl-q12-c-i-iii',
      decision='The old card bundled (c)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Adenine, thymine, cytosine and guanine', 'which two are pyrimidines.'),
      [pt(S('*Adenine (or A) and *guanine (or G)'), 3, label=S('Purines:')),
       pt(S('*Cytosine (or C) and *thymine (or T)'), 3, label=S('Pyrimidines:'))],
      'bio-1-2', 'purines-and-pyrimidines', SQ(21, 'State which two are purines'), 6, fig='q12-bases'),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Human cells contain both DNA and RNA.', 'between DNA and RNA.'),
      [anyn(None, 1, 3, options=[S('DNA is double stranded and RNA'),
                                 S('DNA has the sugar, deoxyribose'), S('DNA has thymine and RNA')])],
      'bio-1-2', 'dna-and-rna', SQ(21, 'State any one structural difference'), 3),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'DNA profiling can be used to identify DNA', 'creating a DNA profile.'),
      [pt(S('Cells are broken down to release DNA'), 3), pt(S('DNA is cut into fragments'), 3),
       pt(S('The (DNA) fragments are separated'), 3), pt(S('A pattern of fragments is analysed'), 3)],
      'bio-3-3', 'dna-profiling-steps', SQ(21, 'Describe the four main steps'), 12),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Explain why photosynthesis is an example of an anabolic reaction.'),
      [pt(S('It involves the building up', 'energy'), 3)], 'bio-2-2', 'photosynthesis-anabolic',
      SQ(22, 'Explain why photosynthesis is an example'), 3, stem=[Q13A], id='bio-2025-hl-q13-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Write a balanced chemical equation to represent photosynthesis.'),
      [pt(S('First point: formulae; second point: balancing'), 6, kind='criterion', units=[3, 3], whole=True,
          note='The scheme\'s equation, with its subscripts and arrow, is shown after reveal.')],
      'bio-2-2', 'photosynthesis-equation', SQ(22, 'Write a balanced chemical equation'), 6,
      stem=[Q13A], fig='q13a-ii-scheme',
      decision='The scheme prints the equation with subscripts and an arrow the text layer '
               'drops; its row lifts the scheme\'s pricing line, and the equation is the '
               'scheme crop shown after reveal.'),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Name the cell organelle shown in the', 'chlorophyll is located.'),
      [pt(S('*Chloroplast'), 3)], 'bio-2-2', 'chloroplast', SQ(22, 'Name the cell organelle shown in the diagram'), 3,
      stem=[Q13B], fig='q13-chloroplast', id='bio-2025-hl-q13-b-i-ii',
      decision='The old card bundled (b)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Name the energised particles released', 'by chlorophyll.'),
      [pt(S('*Electrons'), 3)], 'bio-2-2', 'energised-electrons', SQ(22, 'Name the energised particles'), 3,
      stem=[Q13B]),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'These particles can enter one of two', 'particle movement only.'),
      [pt(S('In pathway 1 electron returns', 'returns to chlorophyll'), 3)], 'bio-2-2',
      'pathways-1-and-2', SQ(22, 'State the difference between each'), 3, stem=[Q13B]),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'Two products of the light-dependent stage', 'each of their roles.'),
      [pt(S('*ATP or adenosine triphosphate'), 3, label=S('Name 1:')),
       pt(S('Supplies energy'), 3, label=S('Role:')),
       pt(S('*NADPH'), 3, label=S('Name 2:')),
       pt(S('Supplies electrons and protons'), 3, label=S('Role:', after='Name 2:'))],
      'bio-2-2', 'light-dependent-products', SQ(22, 'Two products of the light-dependent stage'), 12,
      stem=[Q13B]),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'Name the two products of the light-independent stage', 'light-dependent stage.'),
      [pt(S('*ADP (+P) or adenosine diphosphate'), 3), pt(S('*NADP+'), 3)], 'bio-2-2',
      'regenerated-products', SQ(22, 'Name the two products of the light-independent'), 6, stem=[Q13B]),
    T('13ci', 'Q13(c)(i)', 'C',
      [_C(4, 'Briefly describe enzymes under the following headings:')]
      + listed(4, 'Briefly describe enzymes', ['Biochemical nature', 'Shape.']),
      [pt(S('*Protein'), 3, label=S('1. Biochemical nature')), pt(S('Folded or described'), 3, label=S('2. Shape'))],
      'bio-2-1', 'enzyme-nature-and-shape', SQ(23, 'Briefly describe enzymes'), 6, stem=[Q13C],
      id='bio-2025-hl-q13-c-i-ii',
      decision='Required headings stay one card. The old card bundled (c)(i) and (ii); it keeps '
               'its id for (i), and (ii) is added.'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Based on the biochemical nature of enzymes, name the cell', 'enzymes are made.'),
      [pt(S('*Ribosome'), 3)], 'bio-2-1', 'site-of-enzyme-synthesis',
      SQ(23, 'Based on the biochemical nature'), 3, stem=[Q13C]),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Enzymes can be denatured.', 'enzyme can be denatured.'),
      [pt(S('(An enzyme) that has lost its shape'), 3), pt(S('By pH changes or extreme heat'), 3)],
      'bio-2-1', 'denaturation', SQ(23, 'Explain the underlined term and state one way'), 6, stem=[Q13C]),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'Enzymes can be immobilised, an example of which is shown', 'enzyme immobilisation.'),
      [pt(S('Two correct and relevant named chemicals'), 3, kind='criterion'),
       pt(S('First correct physical procedural step described'), 3, kind='criterion'),
       pt(S('Second correct physical procedural step described'), 3, kind='criterion')],
      'bio-2-1', 'enzyme-immobilisation-method', SQ(23, 'Describe a method of enzyme immobilisation.'), 9,
      stem=[Q13C], fig='q13-beads'),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'Distinguish between the central nervous system and peripheral nervous system.'),
      [pt(S('brain and spinal cord'), 3, label=S('Central:')),
       pt(S('nerves throughout body (and ganglia)'), 3, label=S('Peripheral:'))],
      'bio-2-4', 'cns-and-pns', SQ(24, 'Distinguish between the central nervous system'), 6, stem=[Q14A],
      id='bio-2025-hl-q14-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Name one way in which the human central nervous system is protected.'),
      [pt(S('Skull or spine or vertebrae or meninges'), 3)], 'bio-2-4', 'protection-of-the-cns',
      SQ(24, 'Name one way in which the human nervous system'), 3, stem=[Q14A]),
] + [
    T(f'14bi{n}', f'Q14(b)(i){n}', 'C', item(5, n, part, after='in the eye:'),
      [pt(S(row), 3)], 'bio-2-4', f'role-of-the-{slug}', SQ(24, f'{n}. {part.rstrip(".")}'), 3,
      stem=[Q14B, EACH_EYE], id=old,
      decision='Four structures, each priced: one card each.' + (
          ' The old card bundled all four; it keeps its id for 1.' if old else ''))
    for n, part, row, slug, old in [
        (1, 'Cornea', 'Allows light in or refracts light', 'cornea', 'bio-2025-hl-q14-b-eye'),
        (2, 'Retina', 'Convert light into nerve impulse', 'retina', None),
        (3, 'Optic nerve', 'Carry (nerve) impulses to the brain', 'optic-nerve', None),
        (4, 'Lens.', 'Focus the light onto the retina', 'lens', None)]
] + [
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Which eye (A or B) is exposed to', 'Justify your answer.'),
      [pt(S('*B'), 1), pt(S('The pupil is larger (dilated)'), 2, label=S('Justify:'))], 'bio-2-4',
      'pupil-in-low-light', SQ(24, 'Which eye (A or B), is exposed'), 3,
      stem=[Q14B, _C(5, 'The diagram shows two eyes.')], fig='q14-eyes', id='bio-2025-hl-q14-b-ii-fig'),
] + [
    T(f'14biii{n}', f'Q14(b)(iii){n}', 'C', item(5, n, part, after='following in the ear:'),
      [pt(S(row), 3)], 'bio-2-4', f'role-of-the-{slug}', SQ(24, f'{n}. {part.rstrip(".")}', after='in the ear'), 3,
      stem=[Q14B, EACH_EAR], id=old,
      decision='Three structures, each priced: one card each.' + (
          ' The old card bundled all three; it keeps its id for 1.' if old else ''))
    for n, part, row, slug, old in [
        (1, 'Ossicles', 'Transfer sound (vibrations)', 'ossicles', 'bio-2025-hl-q14-b-ear'),
        (2, 'Cochlea', 'Convert the sound (stimulus)', 'cochlea', None),
        (3, 'Eustachian tube.', 'Equalise pressure', 'eustachian-tube', None)]
] + [
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Describe one corrective measure for one of the following', 'you are referring.'),
      [pt(S('Matching corrective measure described.'), 3, kind='criterion')], 'bio-2-4',
      f'correcting-{route}', SQ(24, 'Describe one corrective measure'), 3, stem=[Q14B], route=route,
      decision='Closed choose-one pool of three printed disorders: one card each.')
    for route in ROUTES['Q14(b)(iv)']
] + [
    T('14ci1', 'Q14(c)(i)1', 'C', [_C(5, 'Which neuron (X or Y) is a', 'motor neuron?'), _C(5, 'Justify your answer.')],
      [pt(S('*X'), 1), pt(S('Justify:'), 2)], 'bio-2-4',
      'motor-neuron', SQ(25, '1. Which neuron (X or Y) is a motor neuron.'), 3, stem=[Q14C, Q14CI],
      fig='q14-neurons', id='bio-2025-hl-q14-c-neuron-id',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('14ci2', 'Q14(c)(i)2', 'C', [_C(5, 'Which neuron (X or Y) is a', 'sensory neuron?', nth=2),
                                   _C(5, 'Justify your answer.', nth=2)],
      [pt(S('*Y'), 1), pt(S('Justify:', 'described', after='*Y'), 2)],
      'bio-2-4', 'sensory-neuron', SQ(25, '2. Which neuron (X or Y) is a sensory neuron.'), 3,
      stem=[Q14C, Q14CI], fig='q14-neurons'),
    T('14cii', 'Q14(c)(ii)', 'C', [_C(5, 'Neurotransmitters are found at', 'position Z.'),
                                   _C(5, 'Describe how neurotransmitters', 'work.')],
      [anyn(S('Impulse arrives at synaptic terminal /', 'inactivated or described'), 3, 3)], 'bio-2-4',
      'how-neurotransmitters-work', SQ(25, 'Describe how neurotransmitters work.'), 9, stem=[Q14C],
      fig='q14-neurons', id='bio-2025-hl-q14-c-neurotransmitters'),
    T('14ciii', 'Q14(c)(iii)', 'C', [_C(5, 'Schwann cells are associated with', 'both neurons.'),
                                     _C(5, 'What is the function of a Schwann', 'cell?')],
      [pt(S('Produce myelin (sheath)'), 3)], 'bio-2-4', 'schwann-cells',
      SQ(25, 'What is the function of a Schwann cell?'), 3, stem=[Q14C], fig='q14-neurons',
      id='bio-2025-hl-q14-c-schwann'),
] + [
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'In relation to Parkinson’s disease or', 'you are referring.'),
      [pt(S('Correct matching cause'), 3, kind='criterion'),
       pt(S('Correct matching treatment'), 3, kind='criterion')], 'bio-2-4', f'{route}-cause-and-treatment',
      SQ(25, 'In relation to Parkinson’s disease'), 6, stem=[Q14C], route=route,
      decision='Closed choose-one pool (Parkinson\'s disease or paralysis): one card each.')
    for route in ROUTES['Q14(c)(iv)']
] + [
    T(f'15a{r}', f'Q15(a)({r})', 'C',
      [_C(6, 'Explain the following three ecological terms:'), _C(6, term, br=True)],
      [pt(S(row), 3)], 'bio-3-1', slug, SQ(26, term), 3, id=old,
      decision='Three terms, each its own roman part.' + (
          ' The old card bundled all three; it keeps its id for (i).' if old else ''))
    for r, term, row, slug, old in [
        ('i', 'Biosphere', 'Part of the Earth where life exists', 'biosphere', 'bio-2025-hl-q15-a'),
        ('ii', 'Niche', '(Functional) role of an organism', 'niche', None),
        ('iii', 'Competition', 'Struggle between organisms', 'competition', None)]
] + [
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'Distinguish between the terms, predator and prey.'),
      [pt(S('an organism that kills and eats'), 3, label=S('Predator:')),
       pt(S('an organism that is killed and eaten'), 3, label=S('Prey:'))], 'bio-3-1',
      'predator-and-prey', SQ(26, 'Distinguish between the terms, predator'), 6, stem=Q15B,
      id='bio-2025-hl-q15-b-predator-prey',
      decision='The old card bundled (b)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'Name an adaptation useful for the survival'),
      [pt(S('Powerful (or flexor) muscles'), 3)], 'bio-3-1', 'eagle-adaptation',
      SQ(26, 'Name an adaptation useful'), 3, stem=Q15B),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Name one human activity that impacts on the population', 'eagles.'),
      [pt(S('Poisoning or wind turbine'), 3)], 'bio-3-1', 'human-impact-on-eagles',
      SQ(26, 'Name one human activity'), 3, stem=Q15B),
    T('15biv1', 'Q15(b)(iv)1', 'C', _C(6, 'The graph shows the periodic changes in the', 'same time period.'),
      [pt(S('Dashed line higher peaks than predator'), 3, kind='criterion'),
       pt(S('Dashed line out of sync with predator'), 3, kind='criterion')], 'bio-3-1',
      'predator-prey-graph', SQ(26, '1. Then, using a dashed line'), 6, stem=Q15B, fig='q15-graph'),
    T('15biv2', 'Q15(b)(iv)2', 'C', _C(6, 'Give a detailed explanation of the graph that', 'prey species.'),
      [pt(S('Increases due to lower predator numbers', 'higher predator numbers'), 2, label=S('Line:')),
       pt(S('Number:', 'smaller in size)'), 2),
       pt(S('Delay in increase'), 2, label=S('Time:'))], 'bio-3-1', 'predator-prey-explanation',
      SQ(26, '2. Give a detailed explanation'), 6,
      stem=Q15B + [M('1.', 6), _C(6, 'The graph shows the periodic changes in the', 'same time period.')],
      fig='q15-graph', id='bio-2025-hl-q15-b-prey-graph'),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'Explain why food chains, such as the those', 'are limited in length.'),
      [pt(S('Large loss in energy between trophic levels'), 3)], 'bio-3-1', 'food-chain-length',
      SQ(26, 'Explain why food chains'), 3, stem=Q15B, id='bio-2025-hl-q15-b-food-chain'),
] + [
    T(f'15ci{n}', f'Q15(c)(i){n}', 'C', item(6, n, part, after='during each process.'),
      [pt(S(row, end), 3)], 'bio-3-2', slug, SQ(27, f'{n}. {part}'), 3, stem=[Q15C, NITROGEN], id=old,
      decision='Four processes, each priced: one card each.' + (
          ' The old card bundled all four; it keeps its id for 1.' if old else ''))
    for n, part, row, end, slug, old in [
        (1, 'Nitrogen fixation', 'Nitrogen gas or atmospheric nitrogen', 'nitrite or nitrate', 'nitrogen-fixation',
         'bio-2025-hl-q15-c-nitrogen-cycle'),
        (2, 'Decomposition', 'Breakdown of (dead) organic matter', None, 'decomposition', None),
        (3, 'Nitrification', 'Conversion of ammonium (or ammonia', None, 'nitrification', None),
        (4, 'Denitrification', 'Conversion of ammonia or ammonium', 'atmospheric nitrogen', 'denitrification', None)]
] + [
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Pollution can affect the nitrogen cycle.', 'What is pollution?'),
      [pt(S('Harmful addition to the environment'), 3)], 'bio-3-1', 'pollution',
      SQ(27, 'What is pollution?'), 3, id='bio-2025-hl-q15-c-pollution'),
] + [
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Name and state the effect of one pollutant', 'industry or domestic.'),
      [pt(S('correctly named pollutant'), 3, kind='criterion', label=S('Name:')),
       pt(S('correct matching effect'), 3, kind='criterion', label=S('Effect:'))], 'bio-3-1',
      f'{route}-pollutant', SQ(27, 'Name and state the effect'), 6, route=route,
      decision='Closed choose-one pool of three printed areas: one card each.')
    for route in ROUTES['Q15(c)(iii)']
] + [
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Describe how the pollutant you have named in part (iii)'),
      [pt(S('Correct matching control measure described'), 3, kind='criterion')], 'bio-3-1',
      'pollution-control', SQ(27, 'Describe how the pollutant'), 3,
      stem=[M('(iii)', 6), _C(6, 'Name and state the effect of one pollutant', 'industry or domestic.')],
      decision='"The pollutant you have named in part (iii)" is the candidate\'s own answer, not a '
               'printed pool: one card.'),
    # Q16: any two of (a)-(d), each 30.
    T('16ai', 'Q16(a)(i)', 'C', _C(7, 'Name the structures A, B and C.'),
      [pt(S('*Sporangium'), 1, label=S('A:')), pt(S('*Spore'), 1, label=S('B:')),
       pt(S('*Stolon'), 1, label=S('C:'))], 'bio-3-2', 'rhizopus-structures',
      SQ(28, 'Name the structures A, B and C.'), 3, stem=[Q16A], fig='q16-rhizopus',
      id='bio-2025-hl-q16-a-i-ii-fig',
      labels=[L('A', S('*Sporangium', page=28), True), L('B', S('*Spore', page=28), True),
              L('C', S('*Stolon', page=28), True)],
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'Give one function of structure C.'),
      [pt(S('Spread the fungus'), 3)], 'bio-3-2', 'stolon-function', SQ(28, 'Give one function of structure C.'), 3,
      stem=[Q16A], fig='q16-rhizopus'),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'Name the method of nutrition used by', 'Rhizopus.'),
      [pt(S('Saprophytic or heterotrophic'), 3)], 'bio-3-2', 'rhizopus-nutrition',
      SQ(28, 'Name the method of nutrition'), 3, stem=[Q16A], fig='q16-rhizopus'),
    T('16aiv1', 'Q16(a)(iv)1', 'C', _C(7, 'The Rhizopus shown in the diagram is', 'to support this statement?'),
      [pt(S('Spores (are being released)'), 3)], 'bio-3-2', 'evidence-of-asexual-reproduction',
      SQ(28, 'The Rhizopus shown in the diagram'), 3,
      stem=[Q16A, _C(7, 'Rhizopus can reproduce sexually and', 'asexually.')], fig='q16-rhizopus'),
    T('16aiv2', 'Q16(a)(iv)2', 'C', _C(7, 'Describe the process of sexual', 'reproduction in Rhizopus.'),
      [anyn(S('+ and – strains grow close together /', 'suitable conditions are present'), 4, 3)],
      'bio-3-2', 'sexual-reproduction-in-rhizopus', SQ(28, 'Describe the process of sexual'), 12,
      stem=[Q16A, _C(7, 'Rhizopus can reproduce sexually and', 'asexually.')], fig='q16-rhizopus'),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'Name a beneficial use and a harmful effect of', 'fungi.'),
      [pt(S('Correct beneficial effect named'), 3, kind='criterion'),
       pt(S('Correct harmful effect named'), 3, kind='criterion')], 'bio-3-2', 'fungi-uses-and-harms',
      SQ(28, 'Name a beneficial use and a harmful'), 6),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'Name the structures A and B, and the type', 'around the body.'),
      [pt(S('A: *Capillary'), 1), pt(S('B: *Alveolus'), 1), pt(S('C: *Red (blood cell)'), 1)],
      'bio-2-6', 'gas-exchange-structures', SQ(29, 'Name the structures A and B, and the type'), 3,
      stem=[Q16B], fig='q16-alveolus', id='bio-2025-hl-q16-b-i-ii-fig',
      labels=[L('A', S('*Capillary', page=29), True), L('B', S('*Alveolus', page=29), True),
              L('C', S('*Red (blood cell)', page=29), True)],
      decision='The old card bundled (b)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Give one way structure B is adapted for its', 'function in gas exchange.'),
      [pt(S('Moist (internal) surface'), 3)], 'bio-2-6', 'alveolus-adaptations',
      SQ(29, 'Give one way structure B is adapted'), 3, stem=[Q16B], fig='q16-alveolus'),
    T('16biii1', 'Q16(b)(iii)1', 'C', _C(7, 'Oxygen and carbon dioxide are two', 'main directions of movement.'),
      [pt(S('X: *Carbon dioxide (or CO2) and Y'), 3, whole=True)], 'bio-2-6', 'gases-x-and-y',
      SQ(29, 'Match each gas to the letters X and Y'), 3, stem=[Q16B], fig='q16-alveolus',
      id='bio-2025-hl-q16-b-iii-fig',
      labels=[L('A', S('*Capillary', page=29), True), L('B', S('*Alveolus', page=29), True)],
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('16biii2', 'Q16(b)(iii)2', 'C', _C(7, 'What term describes the movement', 'of these gases?'),
      [pt(S('*Diffusion'), 3)], 'bio-2-6', 'diffusion-of-gases', SQ(29, 'What term describes the movement'), 3,
      stem=[Q16B, M('1.', 7), _C(7, 'Oxygen and carbon dioxide are two', 'main directions of movement.')],
      fig='q16-alveolus'),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'Name two muscles that are directly', 'involved in inhalation.'),
      [pt(S('*Intercostals'), 3), pt(S('*Diaphragm'), 3)], 'bio-2-6', 'muscles-of-inhalation',
      SQ(29, 'Name two muscles that are directly'), 6),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'Describe the changes that occur in the chest during exhalation.'),
      [anyn(S('Muscles or named relax /', 'air moves out (of the lungs)'), 3, 3)], 'bio-2-6', 'exhalation',
      SQ(29, 'Describe the changes that occur'), 9),
] + [
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'Give one treatment for one of the following breathing disorders:', 'you are referring.'),
      [pt(S('Correct matching treatment'), 3, kind='criterion')], 'bio-2-6', f'{route}-treatment',
      SQ(29, 'Give one treatment for one of the following'), 3, route=route,
      decision='Closed choose-one pool (bronchitis or asthma): one card each.')
    for route in ROUTES['Q16(b)(vi)']
] + [
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'What is interphase?'),
      [pt(S('State of non-division in a cell'), 3)], 'bio-2-3', 'interphase', SQ(30, 'What is interphase?'), 3,
      stem=[Q16C]),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Name a cell activity that occurs during interphase.'),
      [pt(S('Respiration or photosynthesis'), 3)], 'bio-2-3', 'interphase-activity',
      SQ(30, 'Name a cell activity'), 3, stem=[Q16C]),
    T('16ciii1', 'Q16(c)(iii)1', 'C', _C(8, 'Name the stage shown.'),
      [pt(S('*Telophase'), 3)], 'bio-2-3', 'telophase', SQ(30, '1. Name the stage shown.'), 3,
      stem=[Q16C, _C(8, 'The diagram shows a stage of mitosis.')], fig='q16-mitosis',
      id='bio-2025-hl-q16-c-iii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2., 3. are added.'),
    T('16ciii2', 'Q16(c)(iii)2', 'C', _C(8, 'What is the diploid number of this', 'cell?'),
      [pt(S('*4'), 3)], 'bio-2-3', 'diploid-number', SQ(30, '2. What is the diploid number'), 3,
      stem=[Q16C, _C(8, 'The diagram shows a stage of mitosis.')], fig='q16-mitosis'),
    T('16ciii3', 'Q16(c)(iii)3', 'C', _C(8, 'Draw a series of labelled diagrams of', 'stages of mitosis.'),
      [pt(S('Nuclear membrane disappearing', 'visible'), 3, kind='criterion', label=S('Diagram of prophase:')),
       pt(S('Diagram of metaphase:', 'spindle fibres are shown'), 3, kind='criterion'),
       pt(S('Four chromosomes pulled to each pole'), 3, kind='criterion', label=S('Diagram of anaphase:')),
       pt(S('Any three correct labels'), 3, kind='criterion', units=[1, 1, 1])],
      'bio-2-3', 'stages-of-mitosis', SQ(30, '3. Draw a series of labelled diagrams'), 12,
      stem=[Q16C, _C(8, 'The diagram shows a stage of mitosis.')], fig='q16-mitosis'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Give two ways in which meiosis is different to mitosis.'),
      [anyn(S('Meiosis halves the chromosome number', 'genetically identical'), 2, 3,
            note_sel=None)],
      'bio-2-3', 'meiosis-versus-mitosis', SQ(30, 'Give two ways in which meiosis'), 6,
      stem=[_C(8, 'Meiosis is another type of cell division.')]),
    T('16di1', 'Q16(d)(i)1', 'C', _C(8, 'Name two organs of the lymphatic system.'),
      [anyn(S('Lymph vessel / lymph node'), 2, 3)], 'bio-2-6', 'lymphatic-organs',
      SQ(31, '1. Name two organs of the lymphatic system.'), 6, stem=[Q16D], fig='q16-lymphocyte'),
    T('16di2', 'Q16(d)(i)2', 'C', _C(8, 'Other than maturation of lymphocytes, give', 'lymphatic system.'),
      [anyn(S('Return (excess tissue) fluid to the blood /', 'fight infection……….'), 2, 3)], 'bio-2-6',
      'lymphatic-functions', SQ(31, '2. Other than maturation'), 6, stem=[Q16D], fig='q16-lymphocyte'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Lymphocytes play a role in the specific defence', 'lymphocytes are produced.'),
      [pt(S('*Bone marrow'), 3)], 'bio-2-4', 'where-lymphocytes-are-made',
      SQ(31, 'State the precise location'), 3),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Name two types of lymphocyte and describe the', 'role of each.'),
      [pt(S('Name of lymphocyte 1'), 3, kind='criterion'),
       pt(S('Correct matching role of lymphocyte 1'), 3, kind='criterion'),
       pt(S('Name of lymphocyte 2'), 3, kind='criterion'),
       pt(S('Correct matching role of lymphocyte 2'), 3, kind='criterion')], 'bio-2-4',
      'types-of-lymphocyte', SQ(31, 'Name two types of lymphocyte'), 12),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Explain the term vaccination.'),
      [pt(S('Administration of an attenuated pathogen', 'immunity)'), 3)], 'bio-2-4', 'vaccination',
      SQ(31, 'Explain the term vaccination.'), 3),
    # Q17: any two of (a)-(d), each 30.
    T('17ai1', 'Q17(a)(i)1', 'C', _C(9, 'The human circulatory system has two', 'Name both circuits.'),
      [pt(S('*Pulmonary'), 3), pt(S('*Systemic'), 3)], 'bio-2-6', 'two-circuits',
      SQ(32, '1. Name both circuits.'), 6, stem=[Q17A], fig='q17-circulation', id='bio-2025-hl-q17-a-i',
      decision='Four numbered asks, each priced. The old card bundled all four; it keeps its id '
               'for 1., and 2.-4. are added.'),
    T('17ai2', 'Q17(a)(i)2', 'C', _C(9, 'Which of these circuits receives blood', 'from the left ventricle?'),
      [pt(S('*Systemic', after='left ventricle'), 3)], 'bio-2-6', 'systemic-circuit',
      SQ(32, '2. Which of these circuits'), 3,
      stem=[Q17A, M('1.', 9), _C(9, 'The human circulatory system has two', 'Name both circuits.')],
      fig='q17-circulation'),
    T('17ai3', 'Q17(a)(i)3', 'C', _C(9, 'Name the blood vessel that is carrying', 'highest in oxygen.'),
      [pt(S('*Pulmonary vein'), 3)], 'bio-2-6', 'vessel-highest-in-oxygen',
      SQ(32, '3. Name the blood vessel'), 3, stem=[Q17A], fig='q17-circulation'),
    T('17ai4', 'Q17(a)(i)4', 'C', _C(9, 'Name the blood vessel that is carrying', 'highest in nutrients.', nth=2),
      [pt(S('*Hepatic portal vein'), 3)], 'bio-2-6', 'vessel-highest-in-nutrients',
      SQ(32, '4. Name the blood vessel'), 3, stem=[Q17A], fig='q17-circulation'),
    T('17aii1', 'Q17(a)(ii)1', 'C', [_C(9, 'State the precise function of the following in', 'the heart:'),
                                     _C(9, 'Sino-atrial (SA) node', br=True)],
      [pt(S('Sends impulse to the atria', 'or pacemaker'), 3)], 'bio-2-6', 'sa-node',
      SQ(32, '1. Sino-atrial (SA) node'), 3, id='bio-2025-hl-q17-a-ii',
      decision='Two structures, each priced. The old card bundled both; it keeps its id for 1.'),
    T('17aii2', 'Q17(a)(ii)2', 'C', [_C(9, 'State the precise function of the following in', 'the heart:'),
                                     _C(9, 'Septum', br=True)],
      [pt(S('Separates oxygenated and deoxygenated', 'from the right side'), 3)], 'bio-2-6', 'septum',
      SQ(32, 'Septum', after='Sino-atrial'), 3),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'What term is used to describe the period of', 'contracting?'),
      [pt(S('*Systole'), 3)], 'bio-2-6', 'systole', SQ(32, 'What term is used to describe the period'), 3),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Give two structural differences between', 'arteries and veins.'),
      [anyn(S('Arteries have thick walls and veins', 'veins have a wide lumen'), 2, 3)], 'bio-2-6',
      'arteries-and-veins', SQ(32, 'Give two structural differences'), 6),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'Name any three types of joint found in the human skeleton', 'precise location for each type.'),
      [pt(S('Three correctly named joint types'), 6, kind='criterion', units=[2, 2, 2]),
       pt(S('Matching locations stated correctly'), 6, kind='criterion', units=[2, 2, 2])],
      'bio-2-4', 'types-of-joint', SQ(33, 'Name any three types of joint'), 12, stem=[Q17B], fig='q17-joints'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Name any one antagonistic muscle pair', 'movement.'),
      [pt(S('Correctly named antagonistic muscle pair'), 3, kind='criterion'),
       pt(S('when one (named) muscle contracts', 'particular direction'), 3, label=S('First movement:')),
       pt(S('Second movement:', 'first movement'), 3)],
      'bio-2-4', 'antagonistic-pairs', SQ(33, 'Name any one antagonistic muscle pair'), 9,
      stem=[_C(9, 'Antagonistic muscle pairs are associated with the skeleton.')]),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'Sketch the internal structure of a long bone and label at least three parts.'),
      [pt(S('Diagram: Epiphysis and diaphysis'), 6, kind='criterion', units=[3, 3],
          note_sel=S('[Any one missing = 3]')),
       anyn(S('Medullary cavity / cartilage', 'diaphysis……….'), 3, 1)],
      'bio-2-4', 'long-bone-structure', SQ(33, 'Sketch the internal structure of a long bone'), 9),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'Explain the underlined term.'),
      [pt(S('(Homeostasis is) the maintenance'), 3)], 'bio-2-4', 'homeostasis',
      SQ(34, 'Explain the underlined term.'), 3, stem=[Q17C]),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'ADH (anti-diuretic hormone) is an important', 'secretes ADH.'),
      [pt(S('*Pituitary'), 3)], 'bio-2-4', 'adh-gland', SQ(34, 'Name the endocrine gland'), 3, stem=[Q17C],
      id='bio-2025-hl-q17-c-adh',
      decision='The old card bundled (c)(ii)-(iv); it keeps its id for (ii), and (iii), (iv) are added.'),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Name one specific part of the nephron', 'affects.'),
      [pt(S('Distal convoluted tubule or collecting duct'), 3)], 'bio-2-6', 'adh-target',
      SQ(34, 'Name one specific part of the nephron'), 3, stem=[Q17C]),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'What effect does increased ADH have', 'kidneys?'),
      [pt(S('Lowers (the volume)'), 3)], 'bio-2-6', 'adh-and-urine-volume',
      SQ(34, 'What effect does increased ADH'), 3, stem=[Q17C]),
    T('17cv1', 'Q17(c)(v)1', 'C', _C(10, 'State the relationship between blood volume and ADH levels in this case.'),
      [pt(S('Blood volume decreases and ADH levels increases.'), 3)], 'bio-2-4', 'blood-volume-and-adh',
      SQ(34, 'State the relationship between blood volume'), 3, stem=[Q17C] + Q17CV, fig='q17-graphs',
      id='bio-2025-hl-q17-c-v',
      decision='Three numbered asks, each priced. The old card bundled 1. and 2.; it keeps its id '
               'for 1., and 2., 3. are added.'),
    T('17cv2', 'Q17(c)(v)2', 'C', _C(10, 'Suggest how the athlete might increase their blood volume back to normal.'),
      [pt(S('Intake fluids'), 3)], 'bio-2-4', 'restoring-blood-volume',
      SQ(34, 'Suggest how the athlete might'), 3, stem=[Q17C] + Q17CV, fig='q17-graphs'),
    T('17cv3', 'Q17(c)(v)3', 'C', _C(10, 'Copy graph Y into your answerbook and continue the line', 'normal after exercising.'),
      [pt(S('Line reducing'), 3, kind='criterion'),
       pt(S('Line levels off at the same level as the start'), 3, kind='criterion')], 'bio-2-4',
      'adh-graph-continued', SQ(34, 'Copy graph Y into your answerbook'), 6, stem=[Q17C] + Q17CV,
      fig='q17-graphs'),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'State two ways the skin can help the athlete’s homeostasis.'),
      [anyn(S('Sweating / vasodilation'), 2, 3)], 'bio-2-4', 'skin-and-homeostasis',
      SQ(34, 'State two ways the skin'), 6,
      stem=[Q17C, _C(10, 'The skin of the athlete is also involved', 'vigourous exercise.')]),
    T('17di', 'Q17(d)(i)', 'C',
      [_C(10, 'Draw the structure of the human male reproductive system', 'of the following occurs:')]
      + listed(10, 'Draw the structure of the human male', ['Sperm production (X)', 'Sperm storage (Y)',
                                                             'Seminal fluid production (Z)']),
      [pt(S('Diagram: Penis and testes'), 6, kind='criterion', units=[3, 3],
          note_sel=S('[Any one missing = 3]')),
       anyn(S('Penis / testes / urethra', 'vesicles / scrotum……….'), 3, 1),
       pt(S('X located in the testes'), 1), pt(S('Y located in the epididymis'), 1),
       pt(S('Z located on the prostate'), 1)],
      'bio-2-5', 'male-reproductive-system', SQ(35, 'Draw the structure of the male reproductive'), 12),
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'The image shows an electron micrograph of a', 'role for each part.'),
      [pt(S('Head'), 1, label=S('A:')), pt(S('Holds the nucleus'), 2, label=S('Function of A:')),
       pt(S('Tail'), 1, label=S('B:')), pt(S('Movement'), 2, label=S('Function of B:'))],
      'bio-2-5', 'sperm-structure', SQ(35, 'Name parts A and B and give one role'), 6, fig='q17-sperm',
      labels=[L('A', S('Head', page=35), True), L('B', S('Tail', page=35), True)]),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'What is the approximate survival time for sperm', 'copulation?'),
      [pt(S('Up to 7 days'), 3)], 'bio-2-5', 'sperm-survival', SQ(35, 'What is the approximate survival'), 3),
    T('17div', 'Q17(d)(iv)', 'C', _C(10, 'Where does fertilisation usually occur in the', 'female?'),
      [pt(S('*Fallopian tube'), 3)], 'bio-2-5', 'site-of-fertilisation',
      SQ(35, 'Where does fertilisation usually occur'), 3),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Give one cause of infertility and describe a', 'corrective measure.'),
      [pt(S('Correct cause given'), 3, kind='criterion'), pt(S('Corrective measure given'), 3, kind='criterion')],
      'bio-2-5', 'infertility', SQ(35, 'Give one cause of infertility'), 6),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2-root': ('038', 4, (378, 56, 545, 365), 'Adapted from Taiz L, Zeiger E (1998), Plant physiology, 2nd Ed., Sinauer Associates, Sunderland, MA.', ['X', 'Y', 'Z'], 'Diagram of a longitudinal section through a plant root, its tip at the bottom. A bracket labelled Y spans the central core of long, narrow cells running the length of the root; an arrow labelled X points to one of the fine outgrowths on the outside of the root; a line labelled Z points to a small circled patch of tightly packed cells just behind the tip. A thick dashed line crosses the root near the top.', False),
    'q3-mitochondrion': ('038', 5, (340, 88, 542, 197), SEC, [], 'Drawing of a rounded, elongated organelle with a smooth outer membrane and an inner membrane folded into many finger-like inward folds, with small dots scattered in the interior.', False),
    'q4-membrane': ('038', 6, (128, 80, 472, 216), 'alamy.com', ['X', 'Y'], 'Diagram of part of a cell membrane: a curved double row of round heads, each with two wavy tails, with larger blocks embedded in or across it and small branched chains on its outer surface. A bracket labelled X spans the double row; an arrow labelled Y points to a large block that crosses the whole membrane.', False),
    'q5-bioreactor': ('038', 7, (95, 122, 502, 326), 'dciinc.com; State Examinations Commission', ['X', 'Y'], 'Left: photograph of a large stainless-steel vessel with pipes, valves and gauges on a wheeled frame. Right: a graph of Population against Time: the curve starts flat, rises steeply through a section labelled X, then levels off into a flat plateau labelled Y.', False),
    'q6-digestive': ('038', 8, (380, 54, 545, 337), 'shutterstock.com', ['A', 'B'], 'Diagram of the human digestive system inside an outline of the head and upper body. An arrow labelled A points to the tube running down the neck; B labels the bag-shaped organ below the liver; a label Pancreas points to the gland beneath it; the coiled tube in the middle of the abdomen is labelled Small intestine.', False),
    'q11-embryo-sac': ('040', 2, (220, 262, 452, 430), 'dreamstime.com', ['P', 'Q'], "Diagram of a flower's ovary (left) with an arrow to an enlarged ovule (right). Inside the ovule, the embryo sac holds three cells at the top, two small nuclei in the centre and three cells at the bottom. An arrow labelled P points to the two small central nuclei; an arrow labelled Q points to the middle cell of the bottom group.", False),
    'q12-flies': ('040', 3, (300, 113, 541, 280), 'alamy.com', [], 'Two black-and-white photographs of fruit flies, captioned Fruit fly with ebony body and normal wing, and Fruit fly with black body and curly wing.', False),
    'q12-bases': ('040', 3, (145, 486, 500, 600), 'alamy.com', [], 'Structural formulae, rings of carbon and nitrogen atoms, of the four DNA bases side by side, captioned Adenine (A), Thymine (T), Cytosine (C) and Guanine (G).', False),
    'q13a-ii-scheme': ('scheme', 22, (106, 154, 276, 174), SEC, [], "The marking scheme's balanced equation: 6CO2 + 6H2O, an arrow, then C6H12O6 + 6O2, with the number after each element printed as a subscript.", True),
    'q13-chloroplast': ('040', 4, (340, 128, 541, 235), SEC, [], 'Drawing of an oval organelle with a double outer membrane; inside, stacks of flat discs are joined by long membranes, with small dots between them.', False),
    'q13-beads': ('040', 4, (450, 432, 542, 543), 'Tess Watson, flickr.com', [], 'Photograph of a glass beaker filled with small, pale, round beads.', False),
    'q14-eyes': ('040', 5, (318, 215, 541, 297), 'Adapted from nei.nih.gov', ['A', 'B'], 'Two drawings of an eye side by side, labelled A and B. In eye A the black pupil is a small dot in the middle of the grey iris; in eye B the black pupil is much larger, leaving only a thin ring of iris.', False),
    'q14-neurons': ('040', 5, (330, 445, 545, 680), 'alamy.com', ['X', 'Y', 'Z'], 'Diagrams of two neurons. Neuron X has a large cell body covered in branching extensions and a long fibre running down to end among muscle cells, labelled Muscle cells. Neuron Y has its cell body set to one side of its fibre, branched endings at the top marked Z by a bracket, and its other end in a patch of skin, labelled Skin. Arrows from the words Schwann cells point to the segments wrapping each fibre.', False),
    'q15-graph': ('040', 6, (408, 388, 540, 505), SEC, [], 'Graph of Number of organisms against Time: a wavy line rising and falling in regular peaks and troughs.', False),
    'q16-rhizopus': ('040', 7, (370, 88, 542, 290), 'shutterstock.com', ['A', 'B', 'C'], 'Diagram of the bread mould Rhizopus growing on a surface: upright stalks topped by round heads, root-like threads below, and a horizontal thread joining the groups. Arrow A points to one of the round heads; arrow B to small round bodies scattering from a burst head; arrow C to the horizontal thread.', False),
    'q16-alveolus': ('040', 7, (362, 378, 545, 615), 'alamy.com', ['A', 'B', 'C', 'X', 'Y'], 'Diagram of a rounded air sac, labelled B, open at the top to an airway and wrapped by a narrow blood vessel. Arrow A points to the vessel; arrow C points to one of the disc-shaped cells inside it. Curved arrows show two gases crossing between the vessel and the sac: X moves out of the vessel into the sac, and Y moves out of the sac into the vessel.', False),
    'q16-mitosis': ('040', 8, (362, 117, 542, 239), 'britannica.com', [], 'Drawing of a cell pinching into two, with a rounded nucleus forming in each half; each new nucleus holds four chromosomes, and short fibres radiate from a small structure at each end of the cell.', False),
    'q16-lymphocyte': ('040', 8, (395, 360, 545, 558), 'dreamstime.com', [], 'Drawing of a round cell with a large nucleus and Y-shaped molecules projecting from its surface, labelled Lymphocyte; more Y-shaped molecules are released from it towards the lower left.', False),
    'q17-circulation': ('040', 9, (372, 86, 542, 372), 'shutterstock.com', [], 'Diagram of the human circulatory system: the heart in the centre, with vessels looping up through the lungs and down through networks in the liver, the gut, the kidneys and the lower body, and back to the heart.', False),
    'q17-joints': ('040', 9, (115, 418, 530, 597), 'dreamstime.com; alamy.com', [], 'Four images of parts of the human skeleton side by side: a knee, a shoulder (the upper arm bone meeting the shoulder blade and collar bone), a skull, and a spine.', False),
    'q17-graphs': ('040', 10, (140, 205, 480, 330), SEC, [], 'Two graphs over the same time. Graph X, Blood volume against Time, is a dashed line falling steadily. Graph Y, ADH levels against Time, is a solid line that starts low and flat, then rises more and more steeply.', False),
    'q17-sperm': ('040', 10, (390, 590, 542, 696), 'Zhu, WJ. (2020). Atlas of Human Sperm Ultrastructural Morphology. Springer, Singapore. https://doi.org/10.1007/978-981-15-5325-7_2', ['A', 'B'], 'Electron micrograph of a sperm cell with a 2 µm scale bar. Arrow A points to its oval end; arrow B points to the long, thin part trailing from it.', False),
}
