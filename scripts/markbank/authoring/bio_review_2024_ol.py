"""Biology 2024 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 36 pages: p1 cover, p2
    instructions, p3-p8 Section A Questions 1-7, p9-p11 Section B Questions
    8-10, p12 Section C answerbook instructions, p13-p14 graph paper, p15-p35
    ruled answer pages, p36 back cover. No acknowledgements page.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "There is no examination material on this page", p12 back cover.
  * LC025GLP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7 Irish-medium
    bonus, p8-p32 Questions 1-17, p33-p34 "BLANK PAGE", p35 blank, p36 back
    cover.

The sitting was already carded (124 cards, all shipped). As for 2025 and
2024 Higher, every task is re-derived from the PDFs at the scheme's own mark
boundaries and the existing cards are corrected in place: every id is kept,
mapped (`id=`) to the task it was carding, verified or corrected with its old
fields recorded; tasks the old cards bundled or missed are added.
bio-2024-ol-q7 bundled Q7(a)-(e) while (a)-(d) also had cards of their own:
it keeps its id for (e), the one part no card carried.

Tariffs as printed: Q1, Q4 and Q7 5(4); Q2, Q5 and Q6 one ladder each,
6(3) + 2 (seven responses carded at 3); Q3 prices each part (3, 3, 4, 4, 3,
3). Sections B and C print n(3) per part.

No choice here is marked differently per option, so none is split into
routes ("choice is not a route"): Q9(b)(i) enzyme from a printed list of
three, Q10(b)(i)/(ii) pulse or breathing rate, Q11(c)(iii)2 agriculture,
fisheries or forestry, and Q13(a)(ii) Darwin or Wallace are one card each,
the scheme's own alternatives on its rows.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2024, 'ol'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = '89843f7fc'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2024-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': 'e43ae547650731087183ecf4db9973b152ab9748d0138311434d57e305b683a3',
            'pages': 36},
    '040': {'path': 'examiner-reports/biology/papers/2024-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': '0650c443e91a40dd9834992584569e2ae98bdd076465136a7f2f4302b073ea56',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2024-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '65393273ec12042cf99d3b8f2876bfd798fc7b03af5d8d1e0f57579d12171c19',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 12)},
            12: 'answerbook-instructions', 13: 'graph-paper', 14: 'graph-paper',
            **{p: 'answer-pages' for p in range(15, 36)}, 36: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 33)}, 33: 'blank', 34: 'blank', 35: 'blank',
               36: 'back-cover'},
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
# "6(3) + 2": seven responses, six at 3 and the seventh at 2.
LADDERS = {q: [3, 3, 3, 3, 3, 3, 2] for q in (2, 5, 6)}

CHECKSUMS = {
    1: {4: 5}, 2: {3: 7}, 3: {3: 4, 4: 2}, 4: {4: 5}, 5: {3: 7}, 6: {3: 7}, 7: {4: 5},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in range(11, 16)}, **{(n, 'b'): {3: 9} for n in range(11, 16)},
    **{(n, 'c'): {3: 8} for n in range(11, 16)},
    **{(n, x): {3: 10} for n in (16, 17) for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 12), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: every part asked.'),
    ('038', 3, 'the following', 'Q1(d): one of two printed roles; one answer.'),
    ('038', 3, 'one of the following', 'Q1(e): one of three printed terms; one answer.'),
    ('038', 4, 'or', 'Q2(a) "unicellular or multicellular": the answer options.'),
    ('038', 4, 'or', 'Q2(c) "(X or Y)": the answer options.'),
    ('038', 6, 'the following', 'Q4(d): one of two printed sentences; one answer.'),
    ('038', 7, 'the following', 'Q5(c): one of three printed joint types; one answer.'),
    ('038', 7, 'or', 'Q5(c) option "Free moving or synovial": one option.'),
    ('038', 7, 'the following', 'Q5(d): one of three printed joint types; one answer.'),
    ('038', 7, 'or', 'Q5(d) "a hinge or ball and socket joint": description.'),
    ('038', 7, 'or', 'Q5(d) option "Free moving or synovial": one option.'),
    ('038', 8, 'the following', 'Q6 lead-in: every statement asked.'),
    ('038', 8, 'or', 'Q6 "true or false": the answer options.'),
    ('038', 8, 'choose', 'Q7 "Choose each term": a matching list, every term placed; one card per lettered description.'),
    ('038', 8, 'the following', 'Q7 term list.'),
    ('038', 9, 'any two', 'Section B rubric repeated.'),
    ('038', 9, 'or', 'Q8(b)(ii) "apparatus or ... methods": one list; one card.'),
    ('038', 10, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 11, 'or', 'Q10(b)(i) "resting PR or resting BR": the scheme marks both on one row; one card.'),
    ('038', 11, 'either', 'Q10(b)(ii) "either pulse or breathing rate": one set of rows for both; one card.'),
    ('038', 11, 'or', 'Q10(b)(ii), same choice.'),
    ('038', 11, 'either', 'Q10(b)(ii) "either pulse rate (PR) or breathing rate (BR)": same choice.'),
    ('038', 11, 'or', 'Q10(b)(ii), same choice.'),
    ('038', 11, 'or', 'Q10(b)(iii) "PR or BR": one row for both; one card.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q11(a)(ii): both terms asked, one card each.'),
    ('040', 2, 'any one', 'Q11(b)(v)1 "any one food chain": open single answer; one card.'),
    ('040', 2, 'any one', 'Q11(c)(ii)1 "Give any one": open single answer; one card.'),
    ('040', 2, 'one of the following', 'Q11(c)(iii)2 "from one of the following areas": the scheme marks every area on '
                                       'the same two rows; one card.'),
    ('040', 3, 'the following', 'Q12(a) lead-in: both parts asked.'),
    ('040', 3, 'the following', 'Q12(a)(ii): both processes classified; one card.'),
    ('040', 3, 'or', 'Q12(a)(ii) "anabolic or catabolic": the answer options.'),
    ('040', 3, 'the following', 'Q12(b)(i): the equation to complete.'),
    ('040', 3, 'the following', 'Q12(b)(v): every heading asked; one card.'),
    ('040', 4, 'either', 'Q13(a)(ii) "either one of the ... biologists": one row "Darwin or Wallace"; one card.'),
    ('040', 4, 'the following', 'Q13(b) lead-in: every part asked.'),
    ('040', 4, 'both', 'Q13(b)(i) "Both parents": description.'),
    ('040', 4, 'both', 'Q13(b)(ii) "both parents": both required; one card.'),
    ('040', 4, 'or', 'Q13(b)(iv) "fraction or percentage": either form; one answer.'),
    ('040', 4, 'or', 'Q13(c)(i) "(mitosis or meiosis)": the answer options.'),
    ('040', 4, 'or', 'Q13(c)(ii) "agents or substances": one list; one card.'),
    ('040', 4, 'or', 'Q13(c)(iv) "(or uses)": rewording.'),
    ('040', 4, 'or', 'Q13(c)(v) "(or use)": rewording.'),
    ('040', 5, 'the following', 'Q14(a): every organism matched; one card.'),
    ('040', 5, 'the following', 'Q14(b)(i): every label required; one card.'),
    ('040', 5, 'any one', 'Q14(b)(vi) "any one factor": open single answer; one card.'),
    ('040', 5, 'the following', 'Q14(c)(i) matching: all three parts.'),
    ('040', 6, 'the following', 'Q15(b)(i) matching: all three parts.'),
    ('040', 6, 'or', 'Q15(b)(iv) "a sperm cell or an egg cell": the answer options.'),
    ('040', 6, 'the following', 'Q15(c) lead-in: every part asked.'),
    ('040', 6, 'any two', 'Q15(c)(v) "any two biological benefits": bounded menu; one card.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q16(a)(i) matching: both tissues.'),
    ('040', 7, 'the following', 'Q16(a)(iii): one of two printed terms; one answer.'),
    ('040', 7, 'or', 'Q16(a)(v) "a parallel pattern or a net pattern": description.'),
    ('040', 7, 'the following', 'Q16(a)(v) matching: both leaves.'),
    ('040', 7, 'or', 'Q16(a)(vi) "(monocot) or ... (dicot)": description.'),
    ('040', 7, 'the following', 'Q16(a)(vi) matching: both venation types.'),
    ('040', 7, 'the following', 'Q16(b)(i) matching: all four parts.'),
    ('040', 7, 'the following', 'Q16(b)(ii): both terms explained, one card each.'),
    ('040', 7, 'any one', 'Q16(b)(iv) "Give any one": open single answer; one card.'),
    ('040', 7, 'any one', 'Q16(b)(v) "any one function": open single answer; one card.'),
    ('040', 8, 'the following', 'Q16(c)(i) matching: all three parts.'),
    ('040', 8, 'the following', 'Q16(c)(ii) matching: all three functions.'),
    ('040', 8, 'or', 'Q16(c)(v) "female or male": the answer options.'),
    ('040', 8, 'the following', 'Q16(d)(i) matching: all three parts.'),
    ('040', 8, 'or', 'Q16(d)(iv) "Using information in the diagram, or otherwise": method, not a choice of task.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'the following', 'Q17(a) lead-in: every part asked.'),
    ('040', 9, 'the following', 'Q17(b)(ii) matching: all three parts.'),
    ('040', 9, 'the following', 'Q17(b)(iii) matching: all three functions.'),
    ('040', 10, 'the following', 'Q17(c) lead-in: every part asked.'),
    ('040', 10, 'or', 'Q17(c)(ii) "(stem, root, leaf or bud)": the answer options for each plant.'),
    ('040', 10, 'any three', 'Q17(c)(iv) "any three of these methods": bounded menu; one card.'),
    ('040', 10, 'the following', 'Q17(d)(ii) matching: all three glands.'),
    ('040', 10, 'the following', 'Q17(d)(iii) matching: all three hormones.'),
    ('040', 10, 'both', 'Q17(d)(iv) "both endocrine and exocrine": description.'),
]

ROUTES = {}

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def items(page, anchor, ends, doc='040'):
    """A printed numbered list ("1." on its own line, its item on the next)."""
    return [Q(page, f'{i}.', end, doc=doc, after=anchor, br=True) for i, end in enumerate(ends, 1)]


def tick(clip, answer):
    return G('tick-col', page=10, clip=clip, headers=['True', 'False'], expect=answer, marks=3)


Q1 = _A(3, 'Use your knowledge of nutrition to answer the following questions.')
Q2 = _A(4, 'The diagram shows a yeast cell budding.')
Q3 = _A(5, 'The diagram shows DNA replication followed by mitosis.')
Q4 = _A(6, 'The diagram shows the basic structure of a virus.')
Q5 = _A(7, 'The diagram shows the human skeleton.')
Q6 = _A(8, 'State whether each of the following statements is true or false', 'appropriate box in each case.')
Q7 = [_A(8, 'Choose each term from the following list', 'Column A.'), _A(8, 'Hypothesis'), _A(8, 'Data'),
      _A(8, 'Control'), _A(8, 'Theory'), _A(8, 'Experiment')]
Q8B = _A(9, 'As part of your habitat study, you will have investigated three abiotic factors.')
Q9B = _A(10, 'Answer the following questions based on an activity', 'of an enzyme.')
Q10B = _A(11, 'A student investigated the effect of three minutes', 'average data for PR and BR.')
Q11B = _C(2, 'The diagram shows a food web.')
Q11C = _C(2, 'Pollution, waste management and conservation', 'ecosystems.')
Q12A = _C(3, 'Answer the following questions in relation to metabolism.')
Q12B = _C(3, 'Aerobic respiration is a two-stage process', 'balanced equation.')
Q12C = _C(3, 'Photosynthesis is a process that occurs in the', 'shown in the diagram.')
Q13B = _C(4, 'Study the diagram of a cross between', 'following questions.')
Q13F2 = _C(4, 'Two of the F1 offspring were then', 'purple-flowered.')
Q13C = _C(4, 'Variation in offspring can result from', 'mutations.')
Q14B = _C(5, 'Bacteria are very small cells and are found in all habitats.')
Q14C = _C(5, 'Amoeba is a single-celled micro-organism', 'in the diagram.')
Q14CI = [_C(5, 'In your answerbook, match each of the', 'terms:')] + items(
    5, 'In your answerbook, match each of the', ['Pseudopod', 'Nucleus', 'Contractile vacuole'])
Q15B = _C(6, 'The diagram shows the human female reproductive system.')
Q15C = _C(6, 'Answer the following questions in relation to human reproduction.')
Q16A = _C(7, 'The diagram shows a transverse section through a leaf.')
Q16AII = _C(7, 'Xylem and phloem are shown in', 'the diagram.')
Q16B = _C(7, 'The diagram shows the human digestive system.')
Q16C = _C(8, 'The diagram shows the structure of a flower.')
Q16D = _C(8, 'The diagram shows a section through', 'the human skin.')
Q17A = _C(9, 'Answer the following questions in relation to', 'seeds and germination.')
Q17AI = _C(9, 'The diagram shows the internal', 'structure of a seed.')
Q17AII = _C(9, 'The testa is also part of the seed', 'on the diagram.')
Q17AIII = _C(9, 'Seeds usually go through a period of dormancy before germinating.')
Q17B = _C(9, 'The diagram shows the structure', 'of the human ear.')
Q17C = _C(10, 'Answer the following questions in relation to vegetative propagation.')
Q17D = _C(10, 'The diagram shows some parts of the human male', 'The endocrine system produces hormones.')

def SEED_LABELS(food):
    """The seed diagram labels its parts by name; the key repeats each printed name."""
    return [L('Cotyledon', Q(9, 'Cotyledon', doc='040'), food), L('Embryo', Q(9, 'Embryo', doc='040'), not food),
            L('Endosperm', Q(9, 'Endosperm', doc='040'), food)]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Why is food required by all living organisms?'),
      [pt(S('Energy or growth or repair'), 4)], 'bio-1-2', 'why-food-is-required',
      SQ(8, 'Why is food required by all living organisms?'), 4, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Carbon, hydrogen, oxygen and one other element', 'Name the other element.'),
      [pt(S('Nitrogen (or N)'), 4)], 'bio-1-2', 'nitrogen-in-protein', SQ(8, 'Name the other element.'), 4,
      stem=[Q1]),
    T('1c', 'Q1(c)', 'A', _A(3, 'Give one source of protein in the diet.'),
      [pt(S('Correct source named'), 4, kind='criterion')], 'bio-1-2', 'protein-in-the-diet',
      SQ(8, 'Give one source of protein in the diet.'), 4, stem=[Q1]),
    T('1d', 'Q1(d)', 'A', [_A(3, 'Which of the following is a structural role', 'correct box.'),
                           _A(3, 'Component of hair and nails', br=True),
                           _A(3, 'Takes part in enzyme reactions', br=True)],
      [pt(S('Component of hair and nails'), 4)], 'bio-1-2', 'structural-role-of-protein',
      SQ(8, 'Which of the following is a structural role'), 4, stem=[Q1]),
    T('1e', 'Q1(e)', 'A', [_A(3, 'Which one of the following terms is the smallest', 'correct box.'),
                           _A(3, 'Monosaccharide', br=True), _A(3, 'Amino acid', br=True),
                           _A(3, 'Triglyceride', br=True)],
      [pt(S('Amino acid'), 4)], 'bio-1-2', 'amino-acids', SQ(8, 'Which of the following is the smallest unit'), 4,
      stem=[Q1]),
    T('2a', 'Q2(a)', 'A', [_A(4, 'Is yeast a unicellular or multicellular', 'correct box.'),
                           _A(4, 'Unicellular', br=True), _A(4, 'Multicellular', br=True)],
      [pt(S('Unicellular'), 3)], 'bio-3-2', 'yeast-is-unicellular', SQ(8, 'Is yeast a unicellular'), 3,
      stem=[Q2], fig='q2-yeast'),
    T('2b', 'Q2(b)', 'A', [_A(4, 'What is the reason for budding in yeast?', 'correct box.'),
                           _A(4, 'Respiration', br=True), _A(4, 'Excretion', br=True), _A(4, 'Reproduction', br=True)],
      [pt(S('Reproduction'), 3)], 'bio-3-2', 'why-yeast-buds', SQ(8, 'What is the reason for budding'), 3,
      stem=[Q2], fig='q2-yeast'),
    T('2c', 'Q2(c)', 'A', [_A(4, 'Which part of the yeast cell (X or Y) is the bud?', 'correct box.'),
                           _A(4, 'X', br=True, after='Which part of the yeast cell'),
                           _A(4, 'Y', br=True, after='Which part of the yeast cell')],
      [pt(S('X'), 3)], 'bio-3-2', 'the-bud', SQ(8, 'Which part of the yeast cell (X or Y)'), 3, stem=[Q2],
      fig='q2-yeast', id='bio-2024-ol-q2-c-fig'),
    T('2d', 'Q2(d)', 'A', _A(4, 'Briefly describe what happens to the bud.'),
      [pt(S('Remains attached or detaches from parent cell'), 3)], 'bio-3-2', 'fate-of-the-bud',
      SQ(8, 'Briefly describe what happens to the bud.'), 3, stem=[Q2], fig='q2-yeast'),
    T('2e', 'Q2(e)', 'A', _A(4, 'What is the name of the organelle labelled Z?'),
      [pt(S('Nucleus'), 3)], 'bio-3-2', 'yeast-nucleus', SQ(8, 'What is the name of the organelle labelled Z?'), 3,
      stem=[Q2], fig='q2-yeast', id='bio-2024-ol-q2-e-fig', labels=[L('Z', S('Nucleus', page=8), True)]),
    T('2f', 'Q2(f)', 'A', _A(4, 'On the diagram above, draw an arrow', 'cell wall in the yeast cell.'),
      [pt(S('Label correctly pointing at cell wall'), 3, kind='criterion')], 'bio-3-2', 'yeast-cell-wall',
      SQ(8, 'On the diagram above, draw an arrow'), 3, stem=[Q2], fig='q2-yeast'),
    T('2g', 'Q2(g)', 'A', _A(4, 'Yeast is a member of which kingdom?'),
      [pt(S('Fungi'), 3)], 'bio-3-2', 'kingdom-fungi', SQ(8, 'Yeast is a member of which kingdom?'), 3,
      stem=[Q2], fig='q2-yeast'),
    T('3a', 'Q3(a)', 'A', _A(5, 'Structure A is made of DNA and protein. Name structure A.'),
      [pt(S('Chromosome'), 3)], 'bio-2-3', 'chromosome', SQ(9, 'Name structure A.'), 3, stem=[Q3],
      fig='q3-mitosis', labels=[L('A', S('Chromosome', page=9), True)]),
    T('3b', 'Q3(b)', 'A', _A(5, 'Structure B is shown during Stage 2 and Stage 3 of mitosis. Name structure B.'),
      [pt(S('(Spindle) fibre'), 3)], 'bio-2-3', 'spindle-fibres', SQ(9, 'Name structure B.'), 3, stem=[Q3],
      fig='q3-mitosis', labels=[L('B', S('(Spindle) fibre', page=9), True)]),
    T('3c', 'Q3(c)', 'A', _A(5, 'Briefly describe what is happening during Stage 2 of mitosis.'),
      [pt(S('(Duplicated chromosomes) line up on the equator of the cell'), 4)], 'bio-2-3', 'metaphase-events',
      SQ(9, 'Briefly describe what is happening during Stage 2'), 4, stem=[Q3], fig='q3-mitosis'),
    T('3d', 'Q3(d)', 'A', _A(5, 'Briefly describe what is happening during Stage 3 of mitosis.'),
      [pt(S('(Chromosomes) are pulled to the ends', 'separate'), 4)], 'bio-2-3', 'anaphase-events',
      SQ(9, 'Briefly describe what is happening during Stage 3'), 4, stem=[Q3], fig='q3-mitosis'),
    T('3e', 'Q3(e)', 'A', _A(5, 'How many daughter cells result from mitosis?'),
      [pt(S('2'), 3)], 'bio-2-3', 'daughter-cells-of-mitosis', SQ(9, 'How many daughter cells result'), 3,
      stem=[Q3], fig='q3-mitosis'),
    T('3f', 'Q3(f)', 'A', _A(5, 'What is the function of mitosis in multicellular organisms?'),
      [pt(S('Growth'), 3)], 'bio-2-3', 'function-of-mitosis', SQ(9, 'What is the function of mitosis'), 3,
      stem=[Q3], fig='q3-mitosis'),
    T('4a', 'Q4(a)', 'A', _A(6, 'Name the two main components (A and B) of a virus.'),
      [pt(S('A: Protein (or capsid)'), 4), pt(S('B: Nucleic acid (or DNA or RNA)'), 4)], 'bio-1-1',
      'components-of-a-virus', SQ(9, 'Name the two main components'), 8, stem=[Q4], fig='q4-virus',
      id='bio-2024-ol-q4-a-fig',
      labels=[L('A', S('Protein (or capsid)', page=9), True), L('B', S('Nucleic acid (or DNA or RNA)', page=9), True)]),
    T('4b', 'Q4(b)', 'A', _A(6, 'Give one example of a harmful virus.'),
      [pt(S('One harmful virus named'), 4, kind='criterion')], 'bio-1-1', 'harmful-virus',
      SQ(9, 'Give one examples of harmful virus.'), 4, stem=[Q4], fig='q4-virus'),
    T('4c', 'Q4(c)', 'A', _A(6, 'Give an example of how viruses might be beneficial.'),
      [pt(S('Used in genetic engineering', 'other correct'), 4)], 'bio-1-1', 'beneficial-viruses',
      SQ(9, 'Give an example of how viruses might be beneficial.'), 4, stem=[Q4], fig='q4-virus'),
    T('4d', 'Q4(d)', 'A', [_A(6, 'Which of the following sentences describes how viruses replicate?', 'correct box.'),
                           _A(6, 'Viruses replicate outside of living cells.', br=True),
                           _A(6, 'Viruses replicate within living cells.', br=True)],
      [pt(S('Viruses replicate within living cells.'), 4)], 'bio-1-1', 'viral-replication',
      SQ(9, 'Which of the following sentences describe'), 4, stem=[Q4], fig='q4-virus'),
    T('5a', 'Q5(a)', 'A', _A(7, 'Give two functions of the skeleton.'),
      [anyn(S('Structure / support', 'other correct'), 2, 3)], 'bio-2-4', 'functions-of-the-skeleton',
      SQ(10, 'Give two functions of the skeleton.'), 6, stem=[Q5], fig='q5-skeleton'),
    T('5b', 'Q5(b)', 'A', _A(7, 'Name the parts of the skeleton labelled', 'A, B and C.'),
      [pt(S('Skull or cranium'), 3, label=S('A:')), pt(S('Rib'), 3, label=S('B:')),
       pt(S('Pelvis'), 3, label=S('C:'))], 'bio-2-4', 'parts-of-the-skeleton',
      SQ(10, 'Name the bones labelled A, B and C?'), 9, stem=[Q5], fig='q5-skeleton',
      labels=[L('A', S('Skull or cranium', page=10), True), L('B', S('Rib', page=10), True),
              L('C', S('Pelvis', page=10), True)]),
    T('5c', 'Q5(c)', 'A', [_A(7, 'Which of the following types of joint is located', 'correct box.'),
                           _A(7, 'Immovable', br=True), _A(7, 'Slightly movable', br=True),
                           _A(7, 'Free moving or synovial', br=True)],
      [pt(S('Immovable'), 3)], 'bio-2-4', 'immovable-joints', SQ(10, 'Which of the following types of joint is located'),
      3, stem=[Q5], fig='q5-skeleton'),
    T('5d', 'Q5(d)', 'A', [_A(7, 'Which of the following types of joint describes', 'correct box.'),
                           _A(7, 'Immovable', br=True, after='a hinge or ball and socket joint?'),
                           _A(7, 'Slightly movable', br=True, after='a hinge or ball and socket joint?'),
                           _A(7, 'Free moving or synovial', br=True, after='a hinge or ball and socket joint?')],
      [pt(S('Free-moving or synovial'), 3)], 'bio-2-4', 'synovial-joints',
      SQ(10, 'Which of the following types of joints describes'), 3, stem=[Q5], fig='q5-skeleton'),
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(8, start), [tick(clip, answer)], topic, concept, SQ(10, start), 3,
      stem=[Q6], notes='Question 6 is marked on one ladder, 6(3) + 2.')
    for x, start, clip, answer, topic, concept in [
        ('a', 'The stage of a light microscope holds the slide.', (55, 420, 560, 447), 'True', 'bio-1-3',
         'microscope-stage'),
        ('b', 'Protein synthesis occurs on the ribosome.', (55, 447, 560, 474), 'True', 'bio-2-3',
         'site-of-protein-synthesis'),
        ('c', 'Animal cells have cell walls.', (55, 474, 560, 500), 'False', 'bio-1-3', 'animal-cells-lack-walls'),
        ('d', 'A tissue is a group of organs.', (55, 500, 560, 526), 'False', 'bio-1-3', 'tissues-and-organs'),
        ('e', 'Immobilised enzymes can be reused.', (55, 526, 560, 552), 'True', 'bio-2-1',
         'reusing-immobilised-enzymes'),
        ('f', 'Osmosis is a special case of diffusion.', (55, 552, 560, 580), 'True', 'bio-2-6', 'osmosis'),
        ('g', 'Cell membranes are fully permeable.', (55, 580, 560, 612), 'False', 'bio-2-6',
         'membranes-are-selectively-permeable')]
] + [
    T(f'7{x}', f'Q7({x})', 'A', _A(8, desc, end), [pt(S(answer), 4)], topic, concept, SQ(11, sq), 4,
      stem=Q7, id='bio-2024-ol-q7' if x == 'e' else None,
      decision='Lettered parts are separate printed addresses; the completed example (Safety) and the '
               'sentence introducing it are left out of the stem.' + (
                   ' The old card bundled (a)-(e), and (a)-(d) also had cards of their own; it keeps its '
                   'id for (e), the one part no card carried.' if x == 'e' else ''))
    for x, desc, end, sq, answer, topic, concept in [
        ('a', 'Possible explanation for an observation', None, 'Possible explanation for an observation',
         'Hypothesis', 'bio-u2', 'hypothesis'),
        ('b', 'Used to test a hypothesis', None, 'Used to test a hypothesis', 'Experiment', 'bio-u2', 'experiment'),
        ('c', 'Comparison to a test', None, 'Comparison to a test', 'Control', 'bio-u2', 'control'),
        ('d', 'Information and measurements collected during an investigation', None,
         'Information and measurements', 'Data', 'bio-u2', 'data'),
        ('e', 'Supported hypothesis', None, 'Supported hypothesis', 'Theory', 'bio-u1', 'theory')]
] + [
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(9, 'Define the term habitat.'),
      [pt(S('Place where an organism lives'), 3)], 'bio-3-1', 'habitat', SQ(12, 'Define the term habitat.'), 3),
    T('8aii', 'Q8(a)(ii)', 'B', _A(9, 'What did you use to identify fauna and flora in your habitat study?'),
      [pt(S('Key or other correct'), 3)], 'bio-3-1', 'identifying-organisms',
      SQ(12, 'What did you use to identify fauna and flora'), 3),
    T('8bi', 'Q8(b)(i)', 'B', _A(9, 'Name the three abiotic factors you studied', 'may have used.'),
      [anyn(None, 3, 3, options=[S('(Soil or water) pH'), S('(Soil or water) temperature'), S('Wind speed'),
                                 S('Correct abiotic factor')]),
       anyn(None, 3, 3, options=[S('pH meter'), S('Thermometer'), S('Anemometer'),
                                 S('Matching way abiotic factor is measured')])],
      'bio-3-1', 'measuring-abiotic-factors', SQ(12, 'Name the three abiotic factors you studied'), 18,
      stem=[Q8B],
      decision='"Any three 6(3)": three factors and the way each is measured, the scheme printing each '
               'factor beside its instrument. Two menus of three claims each: the factors, and the '
               'matching ways they are measured.'),
    T('8bii', 'Q8(b)(ii)', 'B', _A(9, 'Name two pieces of collection apparatus', 'habitat study.'),
      [anyn(S('Pooter / pitfall trap', 'other correct'), 2, 3)], 'bio-3-1', 'collecting-organisms',
      SQ(12, 'Name two pieces of collection apparatus'), 6,
      stem=[Q8B, _A(9, 'You will have also used various pieces of apparatus', 'habitat study.')]),
    T('9ai', 'Q9(a)(i)', 'B', _A(10, 'Define the term enzyme.'),
      [pt(S('(Protein) catalyst'), 3)], 'bio-2-1', 'enzyme', SQ(13, 'Define the term enzyme.'), 3,
      id='bio-2024-ol-q9-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(10, 'Name a factor, other than temperature, that affects enzyme activity.'),
      [pt(S('pH or other correct'), 3)], 'bio-2-1', 'factors-affecting-enzymes',
      SQ(13, 'Name a factor, other than temperature'), 3),
    T('9bi', 'Q9(b)(i)', 'B', [_A(10, 'Write down the enzyme you used from the list below', 'this enzyme.'),
                               _A(10, 'List: Amylase; Pepsin;', br=True), _A(10, 'Catalase.')],
      [pt(S('Named enzyme (amylase', 'hydrogen peroxide)'), 3, kind='allOf')], 'bio-2-1', 'enzyme-and-substrate',
      SQ(13, 'Write down the enzyme you used'), 3, stem=[Q9B],
      decision='One 3-mark line for the named enzyme with its matching substrate: one all-of row. The '
               'list of three enzymes is answered on that one line, so it is one card.'),
    T('9bii', 'Q9(b)(ii)', 'B', _A(10, 'Briefly describe how you prepared the enzyme.'),
      [pt(S('Preparation described'), 3, kind='criterion', note_sel=S('Must match named enzyme', 'enzyme'))],
      'bio-2-1', 'preparing-the-enzyme', SQ(13, 'Briefly describe how you prepared'), 3, stem=[Q9B]),
    T('9biii', 'Q9(b)(iii)', 'B', _A(10, 'How did you vary the temperature?'),
      [pt(S('Used water baths or described'), 3)], 'bio-2-1', 'varying-temperature',
      SQ(13, 'How did you vary the temperature?'), 3, stem=[Q9B], id='bio-2024-ol-q9-b-iii-v',
      decision='The old card bundled (b)(iii)-(v); it keeps its id for (iii), and (iv), (v) are added.'),
    T('9biv', 'Q9(b)(iv)', 'B', _A(10, 'Name a factor that you kept constant during the activity.'),
      [pt(S('pH or other correct factor'), 3)], 'bio-2-1', 'controlled-factor',
      SQ(13, 'Name a factor that you kept constant'), 3, stem=[Q9B]),
    T('9bv', 'Q9(b)(v)', 'B', _A(10, 'How was the factor named in part (b) (iv) above kept constant?'),
      [pt(S('pH buffer or other correct'), 3, note_sel=S('Must match named factor', '(iv)'))], 'bio-2-1',
      'keeping-a-factor-constant', SQ(13, 'How was the factor named'), 3,
      stem=[Q9B, M('(iv)', 10), _A(10, 'Name a factor that you kept constant during the activity.')]),
    T('9bvi', 'Q9(b)(vi)', 'B', _A(10, 'Give a safety precaution you took during the activity.'),
      [pt(S('Correct safety precaution given'), 3, kind='criterion')], 'bio-2-1', 'enzyme-safety',
      SQ(13, 'Give a safety precaution you took'), 3, stem=[Q9B]),
    T('9bvii', 'Q9(b)(vii)', 'B', _A(10, 'A graph similar to the one shown below', 'label axes A and B.'),
      [pt(S('Rate'), 3, label=S('A:')), pt(S('Temperature'), 3, label=S('B:'))], 'bio-2-1',
      'temperature-graph-axes', SQ(13, 'Label axes A and B.'), 6, stem=[Q9B], fig='q9-graph'),
    T('10a', 'Q10(a)', 'B', _A(11, 'Give two factors, other than exercise, that have an effect on the circulatory system.'),
      [anyn(S('Diet / smoking / stress / other correct'), 2, 3)], 'bio-2-6', 'factors-affecting-circulation',
      SQ(14, 'Give two factors, other than exercise'), 6),
    T('10bi', 'Q10(b)(i)', 'B', _A(11, 'Describe how the student measured resting PR or resting BR.'),
      [anyn(S('Place fingers on wrist', 'per unit time'), 2, 3)], 'bio-2-6', 'measuring-pulse-or-breathing-rate',
      SQ(14, 'Describe how the student measured resting PR'), 6, stem=[Q10B]),
    T('10bii', 'Q10(b)(ii)', 'B', [_A(11, 'The student’s average results are shown in the table below.'),
                                   _A(11, 'Choosing either pulse or', '(BR).')],
      [pt(S('Suitable graph with three correct points'), 9, kind='criterion', units=[3, 3, 3],
          note_sel=S('Points or levels plotted must match y-axis label'))],
      'bio-2-6', 'graphing-exercise-data', SQ(14, 'Draw a suitable graph to represent the data'), 9, stem=[Q10B],
      qfig='q10b-ii-question',
      decision='"3(3)" for the plotted graph; the table, the y-axis box to name and the grid are shown as '
               'the paper prints them. Pulse or breathing rate is the student\'s choice on the same rows.'),
    T('10biii', 'Q10(b)(iii)', 'B', _A(11, 'State what would happen to the PR or BR after exercise has stopped.'),
      [pt(S('It would return to resting rate'), 3)], 'bio-2-6', 'recovery-after-exercise',
      SQ(14, 'State what would happen to the PR or BR'), 3, stem=[Q10B]),
    T('10biv', 'Q10(b)(iv)', 'B', _A(11, 'Suggest a reason for the student repeating the investigation three times.'),
      [pt(S('Check validity of results or other correct reason'), 3)], 'bio-2-6', 'why-repeat',
      SQ(14, 'Suggest a reason for the student repeating'), 3, stem=[Q10B]),
    T('10bv', 'Q10(b)(v)', 'B', _A(11, 'Describe a safety precaution the student would have taken.'),
      [pt(S('Correct safety precaution described'), 3, kind='criterion')], 'bio-2-6', 'exercise-safety',
      SQ(14, 'Describe a safety precaution the student'), 3, stem=[Q10B]),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'What is the primary source of energy for organisms on Earth?'),
      [pt(S('Sun'), 3)], 'bio-3-1', 'source-of-energy', SQ(15, 'What is the primary source of energy'), 3,
      id='bio-2024-ol-q11-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and the two terms of (ii) '
               'are added, one card each.'),
] + [
    T(f'11aii{n}', f'Q11(a)(ii){n}', 'C', [_C(2, 'Define the following terms as used in ecology:'),
                                          _C(2, f'{n}.', term, after='Define the following terms', br=True)],
      [pt(S(answer), 3)], 'bio-3-1', concept, SQ(15, sq), 3)
    for n, term, sq, answer, concept in [
        (1, 'Biosphere', 'Biosphere:', 'Part(s) of the Earth where life can exist', 'biosphere'),
        (2, 'Niche.', 'Niche:', '(Functional) role of an organism (in its habitat)', 'niche')]
] + [
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Name the producer from the food web.'),
      [pt(S('Grasses'), 3)], 'bio-3-1', 'producer', SQ(15, 'Name the producer from the food web.'), 3,
      stem=[Q11B], fig='q11-food-web'),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Name a primary consumer from the food web.'),
      [pt(S('Snail or mouse or grasshopper or mosquito'), 3)], 'bio-3-1', 'primary-consumer',
      SQ(15, 'Name a primary consumer from the food web.'), 3, stem=[Q11B], fig='q11-food-web'),
    T('11biii', 'Q11(b)(iii)', 'C', _C(2, 'Name a secondary consumer from the food web.'),
      [pt(S('Thrush or robin', 'barn owl'), 3)], 'bio-3-1', 'secondary-consumer',
      SQ(15, 'Name a secondary consumer from the food web.'), 3, stem=[Q11B], fig='q11-food-web'),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'What do the arrows on the diagram mean?'),
      [pt(S('Order of consumption or energy flow'), 3)], 'bio-3-1', 'arrows-in-a-food-web',
      SQ(15, 'What do the arrows on the diagram mean?'), 3, stem=[Q11B], fig='q11-food-web'),
    T('11bv1', 'Q11(b)(v)1', 'C', _C(2, 'Write down any one food chain from the food web.'),
      [pt(S('Food chain starting with producer'), 3, kind='criterion'),
       pt(S('Organisms in correct order'), 3, kind='criterion')], 'bio-3-1', 'food-chain-from-the-web',
      SQ(15, 'Write down any one food chain'), 6, stem=[Q11B], fig='q11-food-web'),
    T('11bv2', 'Q11(b)(v)2', 'C', _C(2, 'How many feeding (trophic) levels are in your food chain?'),
      [pt(S('Correct number of matching feeding levels'), 3, kind='criterion')], 'bio-3-1', 'trophic-levels',
      SQ(15, 'How many feeding (trophic) levels'), 3,
      stem=[Q11B, M('1.', 2), _C(2, 'Write down any one food chain from the food web.')], fig='q11-food-web'),
    T('11bvi', 'Q11(b)(vi)', 'C', _C(2, 'Draw a pyramid of numbers for the food chain', 'above.'),
      [pt(S('Correct shape of pyramid of numbers'), 3, kind='criterion'),
       pt(S('with correct order of named organisms'), 3, kind='criterion',
          note_sel=S('Producer must be at base', 'base'))], 'bio-3-1', 'pyramid-of-numbers',
      SQ(15, 'Sketch a pyramid of numbers'), 6,
      stem=[Q11B, M('(v)', 2), M('1.', 2), _C(2, 'Write down any one food chain from the food web.')],
      fig='q11-food-web'),
] + [
    T(f'11c{key}', f'Q11(c){ref}', 'C', _C(2, start, end), rows, 'bio-3-1', concept, SQ(16, sq), total,
      stem=[Q11C], id=old_id,
      decision=dec)
    for key, ref, start, end, sq, rows, total, concept, old_id, dec in [
        ('i1', '(i)1', 'What is meant by the term pollution?', None, 'What is meant by the term pollution?',
         [pt(S('Harmful addition to the environment'), 3)], 3, 'pollution', 'bio-2024-ol-q11-c-i',
         'The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added.'),
        ('i2', '(i)2', 'Give one example of a pollutant.', None, 'Give one example of a pollutant.',
         [pt(S('Any valid example e.g. carbon dioxide', '(in the sea)'), 3)], 3, 'pollutant', None, ''),
        ('i3', '(i)3', 'Give one way pollution may be controlled.', None, 'Give one way in which pollution may',
         [pt(S('Any valid example e.g. reduce fossil fuel use'), 3)], 3, 'pollution-control', None, ''),
        ('ii1', '(ii)1', 'There are problems associated with waste disposal.', 'Give any one.',
         'There are problems associated with waste disposal.',
         [pt(S('Any valid waste disposal problem'), 3, kind='criterion')], 3, 'waste-disposal-problems', None, ''),
        ('ii2', '(ii)2', 'Give one way in which waste can be minimised.', None,
         'Give one way in which waste can be minimised.',
         [pt(S('Reduce or reuse', 'other correct'), 3)], 3, 'minimising-waste', 'bio-2024-ol-q11-c-ii',
         'The old card carded item 2 only; it keeps its id for 2., and 1. is added.'),
        ('iii1', '(iii)1', 'Explain the term conservation.', None, 'Explain the term conservation.',
         [pt(S('Maintenance of an ecosystem'), 3)], 3, 'conservation', 'bio-2024-ol-q11-c-iii',
         'The old card carded item 1 only; it keeps its id for 1., and 2. is added.'),
        ('iii2', '(iii)2', 'Give one conservation practice from one of the following areas:', 'practice.',
         'Give one conservation practice',
         [pt(S('Valid conservation practice given'), 3, kind='criterion'),
          pt(S('Valid reason for practice stated'), 3, kind='criterion')], 6, 'conservation-practice', None,
         'Agriculture, fisheries or forestry: the scheme marks every area on the same two rows, so the '
         'choice is one card.')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', _C(3, 'Explain the term metabolism.'),
      [pt(S('(All) chemical reactions in an organism'), 3)], 'bio-2-1', 'metabolism',
      SQ(17, 'Explain the term metabolism.'), 3, stem=[Q12A]),
    T('12aii', 'Q12(a)(ii)', 'C', [_C(3, 'State whether each of the following processes is anabolic or catabolic:')]
      + items(3, 'State whether each of the following', ['Respiration', 'Photosynthesis']),
      [pt(S('(Respiration is) catabolic'), 3), pt(S('(Photosynthesis is) anabolic'), 3)], 'bio-2-2',
      'anabolic-and-catabolic', SQ(17, 'State whether each of the following are anabolic'), 6, stem=[Q12A],
      decision='One classification of two numbered processes: two rows.'),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'In your answerbook, write out and complete', 'for aerobic respiration:'),
      [pt(S('CO2'), 3), pt(S('H2O'), 3)], 'bio-2-2', 'aerobic-respiration-equation',
      SQ(17, 'Complete the balanced equation for aerobic respiration:'), 6, stem=[Q12B], qfig='q12b-i-question',
      decision='The equation to complete is printed with subscripts and an arrow the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'What is the name given to the substance with the formula, C6H12O6?'),
      [pt(S('Glucose'), 3)], 'bio-2-2', 'glucose', SQ(17, 'What is the name given to the substance'), 3,
      stem=[Q12B]),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'Where in a cell does stage 1 occur?'),
      [pt(S('Cytosol'), 3)], 'bio-2-2', 'site-of-stage-1', SQ(17, 'Where in a cell does stage 1 occur?'), 3,
      stem=[Q12B]),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'What is the name of the organelle shown in the', 'occurs?'),
      [pt(S('Mitochondrion'), 3)], 'bio-2-2', 'mitochondrion', SQ(17, 'What is the name of the organelle shown in the diagram in which'),
      3, stem=[Q12B], fig='q12-mitochondrion', id='bio-2024-ol-q12-b-iv-fig'),
    T('12bv', 'Q12(b)(v)', 'C', [_C(3, 'Describe the differences between stage 1 and', 'headings:')]
      + items(3, 'Describe the differences between stage 1', ['in stage 1.', 'in stage 2.', 'of stage 1.', 'of stage 2.']),
      [pt(S('Low (or small)'), 3, label=S('Amount of energy released in stage 1')),
       pt(S('High (or large)'), 3, label=S('Amount of energy released in stage 2')),
       pt(S('Oxygen not required'), 3, label=S('Oxygen requirement of stage 1')),
       pt(S('Oxygen required', after='Oxygen requirement of stage 2'), 3, label=S('Oxygen requirement of stage 2'))],
      'bio-2-2', 'stages-of-aerobic-respiration', SQ(17, 'Describe the differences between stage 1'), 12,
      stem=[Q12B], decision='Four required headings of one comparison: one card, a row per heading.'),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'What is the name of the organelle shown?'),
      [pt(S('Chloroplast'), 3)], 'bio-2-2', 'chloroplast', SQ(18, 'What is the name of the organelle shown?'), 3,
      stem=[Q12C], fig='q12-chloroplast', id='bio-2024-ol-q12-c-i-fig'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'What is the name given to the green', 'sunlight energy?'),
      [pt(S('Chlorophyll'), 3)], 'bio-2-2', 'chlorophyll', SQ(18, 'What is the name given to the green pigment'), 3,
      stem=[Q12C, M('(i)', 3), _C(3, 'What is the name of the organelle shown?')], fig='q12-chloroplast'),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'The energy in sunlight is used by the pigment', 'splitting of water.'),
      [pt(S('H+ (ions) or protons'), 3), pt(S('Electrons'), 3), pt(S('Oxygen (gas)'), 3)], 'bio-2-2',
      'splitting-water', SQ(18, 'Name the three components'), 9),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'State what happens to each of the components', 'above.'),
      [pt(S('Used to make glucose or taken up by energy carrier'), 3, label=S('H+ ions:')),
       pt(S('Used to make glucose or taken up by energy carrier', nth=2), 3, label=S('Electrons:')),
       pt(S('Oxygen gas: Used in respiration', 'atmosphere'), 3)], 'bio-2-2', 'fate-of-water-products',
      SQ(18, 'State what happens to each of the components'), 9,
      stem=[M('(iii)', 3), _C(3, 'The energy in sunlight is used by the pigment', 'splitting of water.')]),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Explain in detail the term evolution.'),
      [pt(S('Change in genetic makeup'), 3), pt(S('over time or in response to environment'), 3)], 'bio-1-5',
      'evolution', SQ(19, 'Explain in detail the term evolution.'), 6, id='bio-2024-ol-q13-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Name either one of the 19', 'natural selection.'),
      [pt(S('(Charles) Darwin or (Alfred Russell)-Wallace'), 3)], 'bio-1-5', 'darwin-or-wallace',
      SQ(19, 'Name either one of the 19'), 3,
      decision='Either biologist answers it: the scheme prints both on one row, so it is one card.'),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Both parents were homozygous', 'Explain the underlined terms.'),
      [pt(S('two (or both) alleles (of a gene) are the same'), 3, label=S('Homozygous:')),
       pt(S('Heterozygous: two'), 3)], 'bio-1-4', 'homozygous-and-heterozygous',
      SQ(19, 'Both parents were homozygous'), 6, stem=[Q13B], qfig='q13b-i-question',
      decision='The paper marks the terms to explain by underlining them, which the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Give the genotypes of both', 'parents.'),
      [pt(S('PP'), 3), pt(S('pp'), 3)], 'bio-1-4', 'parent-genotypes', SQ(19, 'Give the genotypes of both parents.'),
      6, stem=[Q13B], fig='q13-cross'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Copy the Punnett square into your', 'genotypes of the F2 offspring.'),
      [pt(S('PP'), 3), pt(S('Pp'), 3), pt(S('Pp', nth=2), 3),
       pt(S('pp'), 3, note='The scheme\'s completed square is shown after reveal.')], 'bio-1-4',
      'monohybrid-punnett-square', SQ(19, 'Copy the Punnett square'), 12, stem=[Q13B, Q13F2],
      qfig='q13b-iii-question', fig='q13b-iii-scheme',
      decision='The scheme answers with a completed Punnett square: its four genotypes are rows (read in '
               'print order) and the square itself is the solution figure; the question, with the blank '
               'square and its parents, is shown as the paper prints it.'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'What fraction or percentage of the F2', 'white-flowered?'),
      [pt(S('25% (or one quarter)'), 3)], 'bio-1-4', 'fraction-white-flowered',
      SQ(19, 'What fraction or percentage of the F2'), 3, stem=[Q13B, Q13F2], fig='q13-punnett'),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Which type of cell division (mitosis or meiosis)', 'gametes?'),
      [pt(S('Meiosis'), 3)], 'bio-2-3', 'meiosis-makes-gametes', SQ(20, 'Which type of cell division'), 3,
      stem=[Q13C]),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Give two agents or substances that can increase', 'potentially cause cancer.'),
      [anyn(S('UV light / cigarette smoke / other correct'), 2, 3)], 'bio-2-3', 'mutagens',
      SQ(20, 'Give two agents or substances'), 6, stem=[Q13C]),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Variation exists within all species.', 'the term species?'),
      [pt(S('Group of (similar) organisms'), 3), pt(S('that can interbreed to produce fertile offspring'), 3)],
      'bio-1-5', 'species', SQ(20, 'What is a ‘species’?'), 6),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'DNA profiling is a laboratory technique', 'DNA profiling.'),
      [anyn(S('Species identification', 'correct'), 2, 3)], 'bio-3-3', 'dna-profiling',
      SQ(20, 'Give two applications (or uses) of DNA profiling.'), 6),
    T('13cv', 'Q13(c)(v)', 'C', _C(4, 'Genetic screening is also a laboratory technique.', 'genetic screening.'),
      [pt(S('Testing for a (mutated) gene'), 3)], 'bio-3-3', 'genetic-screening',
      SQ(20, 'Give one application (or use) of genetic screening.'), 3),
    T('14a', 'Q14(a)', 'C', [_C(5, 'Three kingdoms of organisms include', 'named organisms below:'),
                             M('(i)', 5), _C(5, 'Bacteria'), M('(ii)', 5), _C(5, 'Amoeba'),
                             M('(iii)', 5), _C(5, 'Rhizopus')],
      [pt(S('Monera'), 3, label=S('Bacteria:')), pt(S('Protista'), 3, label=S('Amoeba:')),
       pt(S('Fungi'), 3, label=S('Rhizopus:'))], 'bio-1-1', 'three-kingdoms',
      SQ(21, 'Match each of these kingdoms'), 9,
      decision='One matching exercise over a shared pool of three kingdoms: one card, a row per organism.'),
    T('14bi', 'Q14(b)(i)', 'C', [_C(5, 'Draw a diagram of a bacterial cell and label the following parts:'),
                                 _C(5, 'Cell wall;', br=True), _C(5, 'DNA;'), _C(5, 'Cytosol')],
      [pt(S('Cell wall and cell membrane and DNA'), 3, kind='criterion', label=S('Diagram:')),
       pt(S('Cell wall', after='Labels:'), 3, label=S('Labels:')), pt(S('DNA', after='Labels:'), 3),
       pt(S('Cytosol', after='Labels:'), 3)], 'bio-3-2', 'drawing-a-bacterial-cell',
      SQ(21, 'Draw a diagram of a typical bacterial cell'), 12, stem=[Q14B]),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Bacteria can be classified based on their shape.', 'bacterial shape.'),
      [pt(S('Round or rod or spiral'), 3)], 'bio-3-2', 'bacterial-shapes',
      SQ(21, 'Bacteria can be classified based on their shape.'), 3, stem=[Q14B], id='bio-2024-ol-q14-b-ii-iii',
      decision='The old card bundled (b)(ii) and (iii); it keeps its id for (ii), and (iii) is added.'),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'Some bacteria are pathogenic.', 'Explain the underlined term.'),
      [pt(S('Disease causing'), 3)], 'bio-3-2', 'pathogenic', SQ(21, 'Some bacteria are pathogenic.'), 3,
      stem=[Q14B], qfig='q14b-iii-question',
      decision='The paper marks the term to explain by underlining it, which the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Some bacteria can be beneficial.', 'beneficial bacterium.'),
      [pt(S('Any valid beneficial bacterium'), 3, kind='criterion')], 'bio-3-2', 'beneficial-bacteria',
      SQ(21, 'Give one example of a beneficial bacterium.'), 3, stem=[Q14B]),
    T('14bv', 'Q14(b)(v)', 'C', _C(5, 'Bacterial cells undergo binary fission.', 'binary fission?'),
      [pt(S('(Asexual) reproduction (in bacteria)'), 3)], 'bio-3-2', 'binary-fission',
      SQ(21, 'What is binary fission?'), 3, stem=[Q14B], id='bio-2024-ol-q14-b-v-vi',
      decision='The old card bundled (b)(v) and (vi); it keeps its id for (v), and (vi) is added.'),
    T('14bvi', 'Q14(b)(vi)', 'C', _C(5, 'State any one factor that influences the growth of bacteria.'),
      [pt(S('pH or temperature or other correct'), 3)], 'bio-3-2', 'bacterial-growth-factors',
      SQ(21, 'State any one factor that influences'), 3, stem=[Q14B]),
    T('14ci', 'Q14(c)(i)', 'C', Q14CI,
      [pt(S('B', after='1. Pseudopod:'), 3, label=S('Pseudopod:')),
       pt(S('A', after='2. Nucleus:'), 3, label=S('Nucleus:')),
       pt(S('C', after='3. Contractile vacuole:'), 3, label=S('Contractile vacuole:'))], 'bio-3-2',
      'parts-of-amoeba', SQ(22, 'Match each of the parts of Amoeba'), 9, stem=[Q14C], fig='q14-amoeba',
      labels=[L('A', S('Nucleus', page=22, after='Contractile vacuole'), True),
              L('B', S('Pseudopod', page=22, after='Contractile vacuole'), True),
              L('C', S('Contractile vacuole', page=22, after='Nucleus;'), True)],
      decision='One matching exercise: three rows.'),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Which of the above-mentioned parts does', 'move around?'),
      [pt(S('Pseudopod (or B)'), 3)], 'bio-3-2', 'amoeba-movement', SQ(22, 'Which of the above-mentioned parts does Amoeba use to move'),
      3, stem=[Q14C, M('(i)', 5)] + Q14CI, fig='q14-amoeba', id='bio-2024-ol-q14-c-ii-iii',
      decision='The old card bundled (c)(ii) and (iii); it keeps its id for (ii), and (iii) is added.'),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Which of the above-mentioned parts does', 'inside the cell?', nth=2),
      [pt(S('Contractile vacuole (or C)'), 3)], 'bio-3-2', 'amoeba-water-control',
      SQ(22, 'Which of the above-mentioned parts does Amoeba use to control'), 3,
      stem=[Q14C, M('(i)', 5)] + Q14CI, fig='q14-amoeba'),
    T('14civ', 'Q14(c)(iv)', 'C', [_C(5, 'Match each of the sentences below to the terms asepsis and sterility.')]
      + items(5, 'Match each of the sentences below', ['Absence of pathogens', 'Absence of all microorganisms']),
      [pt(S('Asepsis'), 3, label=S('Absence of pathogens:')),
       pt(S('Sterility'), 3, label=S('Absence of all microorganisms:'))], 'bio-3-2', 'asepsis-and-sterility',
      SQ(22, 'Match each of the sentences below'), 6,
      stem=[_C(5, 'Care must be taken when handling micro-organisms.', 'often used.')],
      decision='One matching exercise: two rows.'),
    T('14cv', 'Q14(c)(v)', 'C', _C(5, 'Describe how you would dispose of micro-organisms', 'laboratory activity.'),
      [pt(S('Soak in disinfectant', 'general waste)', ), 3)], 'bio-3-2', 'safe-disposal',
      SQ(22, 'Describe how you would dispose of micro-organisms'), 3),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'Explain the term secondary sexual characteristics.'),
      [pt(S('Traits that distinguish male from female'), 3), pt(S('other than the sex organs'), 3)], 'bio-2-5',
      'secondary-sexual-characteristics', SQ(23, 'Explain the term secondary sexual characteristics.'), 6,
      id='bio-2024-ol-q15-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Give one example of a secondary sexual characteristic in humans.'),
      [pt(S('Breasts or pubic hair', 'deep voice'), 3)], 'bio-2-5', 'example-of-a-secondary-characteristic',
      SQ(23, 'Give one example of a secondary sexual characteristic'), 3),
    T('15bi', 'Q15(b)(i)', 'C', [_C(6, 'In your answerbook, match each of the parts labelled A, B, and C with the',
                                    'following terms:')]
      + items(6, 'match each of the parts labelled A, B, and C', ['Uterus', 'Fallopian tube', 'Ovary']),
      [pt(S('C', after='1. Uterus:'), 3, label=S('Uterus:')),
       pt(S('A', after='2. Fallopian tube:'), 3, label=S('Fallopian tube:')),
       pt(S('B', after='3. Ovary:'), 3, label=S('Ovary:'))], 'bio-2-5', 'female-reproductive-parts',
      SQ(23, 'Match each of the parts labelled A, B, and C'), 9, stem=[Q15B], fig='q15-female',
      id='bio-2024-ol-q15-b-i-fig',
      labels=[L('A', S('Fallopian tube:', page=23), True), L('B', S('Ovary:', page=23), True),
              L('C', S('Uterus:', page=23), True)],
      decision='One matching exercise: three rows.'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'In which labelled part are egg cells produced?'),
      [pt(S('Ovary (or B)'), 3)], 'bio-2-5', 'where-eggs-are-made', SQ(23, 'In which labelled part are egg cells'), 3,
      stem=[Q15B], fig='q15-female', id='bio-2024-ol-q15-b-ii-iii-fig',
      labels=[L('A', S('Fallopian tube:', page=23), False), L('B', S('Ovary:', page=23), False),
              L('C', S('Uterus:', page=23), False)],
      decision='The old card bundled (b)(ii) and (iii); it keeps its id for (ii), and (iii) is added.'),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Fertilisation is where the sperm cell and egg cell fuse.', 'fertilisation occur?'),
      [pt(S('Fallopian tube (or A)'), 3)], 'bio-2-5', 'site-of-fertilisation',
      SQ(23, 'In which labelled part does fertilisation'), 3, stem=[Q15B], fig='q15-female',
      labels=[L('A', S('Fallopian tube:', page=23), False), L('B', S('Ovary:', page=23), False),
              L('C', S('Uterus:', page=23), False)]),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'Sperm cells and egg cells are gametes.', 'an egg cell?'),
      [pt(S('Egg cell'), 3)], 'bio-2-5', 'larger-gamete', SQ(23, 'Which gamete is larger'), 3),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'Sketch the structure of a sperm cell.'),
      [pt(S('Sketch showing head and tail'), 3, kind='criterion')], 'bio-2-5', 'sperm-sketch',
      SQ(23, 'Sketch the structure of a sperm cell.'), 3),
    T('15bvi', 'Q15(b)(vi)', 'C', _C(6, 'The vagina and endometrium are shown in the diagram.', 'for each.'),
      [pt(S('Receives penis during copulation or birth canal'), 3,
          label=S('One function of vagina', after='Sketch showing head and tail')),
       pt(S('Receives blastocyst', 'or other correct'), 3, label=S('One function of endometrium'))], 'bio-2-5',
      'vagina-and-endometrium', SQ(23, 'One function of vagina'), 6, stem=[Q15B], fig='q15-female'),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'What is meant by the term infertility?'),
      [pt(S('Inability to produce offspring', 'description'), 3)], 'bio-2-5', 'infertility',
      SQ(24, 'What is meant by the term infertility?'), 3, stem=[Q15C], id='bio-2024-ol-q15-c-i-iii',
      decision='The old card bundled (c)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Give one cause of infertility in the human.'),
      [pt(S('Endocrine gland failure', 'other correct'), 3)], 'bio-2-5', 'cause-of-infertility',
      SQ(24, 'Give one cause of infertility'), 3, stem=[Q15C]),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Give a possible corrective measure for infertility.'),
      [pt(S('Hormonal treatment', 'other correct'), 3)], 'bio-2-5', 'treating-infertility',
      SQ(24, 'Give a possible corrective measure'), 3, stem=[Q15C]),
    T('15civ1', 'Q15(c)(iv)1', 'C', _C(6, 'What is meant by the term birth control?'),
      [pt(S('Prevention of fertilisation (or implantation)'), 3)], 'bio-2-5', 'birth-control',
      SQ(24, 'What is meant by the term birth control?'), 3, stem=[Q15C], id='bio-2024-ol-q15-c-iv',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('15civ2', 'Q15(c)(iv)2', 'C', _C(6, 'Give two methods of birth control.'),
      [anyn(S('Surgical / mechanical / chemical / natural / named example'), 2, 3)], 'bio-2-5',
      'methods-of-birth-control', SQ(24, 'Give two methods of birth control.'), 6, stem=[Q15C]),
    T('15cv', 'Q15(c)(v)', 'C', _C(6, 'Breastfeeding has many biological benefits', 'biological benefits.'),
      [anyn(S('Mother-baby bond', 'other correct'), 2, 3)], 'bio-2-5', 'breastfeeding-benefits',
      SQ(24, 'Give any two biological benefits'), 6, stem=[Q15C]),
    # Q16: any two of (a)-(d), each 30.
    T('16ai', 'Q16(a)(i)', 'C', [_C(7, 'In your answerbook, match tissues', 'following terms:')]
      + items(7, 'In your answerbook, match tissues', ['Ground', 'Dermal']),
      [pt(S('B', after='1. Ground:'), 3, label=S('Ground:')), pt(S('A', after='2. Dermal:'), 3, label=S('Dermal:'))],
      'bio-2-6', 'leaf-tissues', SQ(25, 'Match tissues A and B'), 6, stem=[Q16A], fig='q16-leaf',
      id='bio-2024-ol-q16-a-i-fig',
      labels=[L('A', S('Dermal:', page=25), True), L('B', S('Ground:', page=25), True)],
      decision='One matching exercise: two rows.'),
    T('16aii1', 'Q16(a)(ii)1', 'C', _C(7, 'Give one function of xylem.'),
      [pt(S('Transport water or minerals'), 3)], 'bio-2-6', 'xylem-function', SQ(25, 'Give one function of xylem.'), 3,
      stem=[Q16A, Q16AII], fig='q16-leaf', id='bio-2024-ol-q16-a-ii-iii',
      decision='The old card bundled (a)(ii)1-2 and (iii); it keeps its id for (ii)1., and (ii)2. and (iii) '
               'are added.'),
    T('16aii2', 'Q16(a)(ii)2', 'C', _C(7, 'Give one function of phloem.'),
      [pt(S('Transport food'), 3)], 'bio-2-6', 'phloem-function', SQ(25, 'Give one function of phloem.'), 3,
      stem=[Q16A, Q16AII], fig='q16-leaf'),
    T('16aiii', 'Q16(a)(iii)', 'C', [_C(7, 'Which of the following terms', 'airspaces of the leaf?'),
                                     _C(7, 'Transpiration;', br=True), _C(7, 'Respiration', after='Transpiration;')],
      [pt(S('Transpiration'), 3)], 'bio-2-6', 'transpiration', SQ(25, 'Which of the following terms describes'), 3),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'When the water evaporates into the airspaces', 'exit the leaf?'),
      [pt(S('Stoma'), 3)], 'bio-2-6', 'stomata', SQ(25, 'Which labelled structure does the water exit'), 3,
      stem=[Q16A], fig='q16-leaf', id='bio-2024-ol-q16-a-iv-fig'),
    T('16av', 'Q16(a)(v)', 'C', [_C(7, 'Veins in leaves can be arranged', 'following terms:')]
      + items(7, 'Match each of the leaves X and Y', ['Parallel venation', 'Net venation']),
      [pt(S('Y', after='1. Parallel venation:'), 3, label=S('Parallel venation:')),
       pt(S('X', after='2. Net venation'), 3, label=S('Net venation'))], 'bio-2-6', 'leaf-venation',
      SQ(25, 'Match each of the leaves X and Y'), 6, fig='q16-venation', id='bio-2024-ol-q16-a-v-fig',
      labels=[L('X', S('Net venation', page=25), True), L('Y', S('Parallel venation:', page=25), True)],
      decision='One matching exercise: two rows.'),
    T('16avi', 'Q16(a)(vi)', 'C', [_C(7, 'The type of leaf venation usually indicates', 'terms:')]
      + items(7, 'leaf venation (parallel and net)', ['Monocotyledonous', 'Dicotyledonous']),
      [pt(S('Parallel (or Y)'), 3, label=S('Monocotyledonous:')), pt(S('Net (or X)'), 3, label=S('Dicotyledonous:'))],
      'bio-2-6', 'venation-of-monocots-and-dicots', SQ(25, 'Match each of the types of leaf venation'), 6,
      decision='One matching exercise: two rows.'),
    T('16bi', 'Q16(b)(i)', 'C', [_C(7, 'In your answerbook, match each of the parts', 'following terms:')]
      + items(7, 'labelled A, B, C and D', ['Stomach', 'Large intestine', 'Oesophagus', 'Small intestine']),
      [pt(S('B', after='1. Stomach:'), 3, label=S('Stomach:')), pt(S('Large Intestine: D'), 3),
       pt(S('A', after='3. Oesophagus:'), 3, label=S('Oesophagus:')),
       pt(S('C', after='4. Small intestine:'), 3, label=S('Small intestine:'))], 'bio-2-6',
      'parts-of-the-digestive-system', SQ(26, 'Match each of the parts labelled A, B and C'), 12, stem=[Q16B],
      fig='q16-digestive', id='bio-2024-ol-q16-b-i-fig',
      labels=[L('A', S('Oesophagus:', page=26), True), L('B', S('Stomach:', page=26), True),
              L('C', S('Small intestine:', page=26), True), L('D', Q(7, 'Large intestine', doc='040'), True)],
      decision='One matching exercise: four rows.'),
] + [
    T(f'16bii{n}', f'Q16(b)(ii){n}', 'C', [_C(7, 'Explain the following terms:'),
                                          _C(7, f'{n}.', term, after='Explain the following terms:', br=True)],
      [pt(S(answer), 3)], 'bio-2-6', concept, SQ(26, term), 3, id=old_id,
      decision='The old card bundled (b)(ii)1-2 and (iii); it keeps its id for (ii)1., and (ii)2. and (iii) '
               'are added.' if old_id else '')
    for n, term, answer, concept, old_id in [
        (1, 'Ingestion', 'Taking in food', 'ingestion', 'bio-2024-ol-q16-b-ii-iii'),
        (2, 'Digestion', 'Breaking down food', 'digestion', None)]
] + [
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'Why is digestion important in the body?'),
      [pt(S('(So that nutrients) can be absorbed', 'other correct'), 3)], 'bio-2-6', 'why-digest',
      SQ(26, 'Why is digestion is important in the body?'), 3),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'The liver has many functions.', 'Give any one.'),
      [pt(S('To produce bile', 'correct'), 3)], 'bio-2-6', 'liver-function',
      SQ(26, 'Give any one function of the liver.'), 3, id='bio-2024-ol-q16-b-iv-vi',
      decision='The old card bundled (b)(iv)-(vi); it keeps its id for (iv), and (v), (vi) are added.'),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'Symbiotic bacteria are found in the human', 'these bacteria.'),
      [pt(S('Digestion (of cellulose)', 'other correct'), 3)], 'bio-2-6', 'symbiotic-bacteria',
      SQ(26, 'Give one function of symbiotic bacteria.'), 3),
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'Why is fibre an important part of the diet?'),
      [pt(S('Stimulates peristalsis or other correct'), 3)], 'bio-2-6', 'fibre',
      SQ(26, 'Why is fibre an important part of the diet?'), 3),
    T('16ci', 'Q16(c)(i)', 'C', [_C(8, 'In your answerbook, match each of the parts', 'following terms:')]
      + items(8, 'labelled A, B and C with the following terms:', ['Petal', 'Stigma', 'Anther']),
      [pt(S('C', after='Petal:'), 3, label=S('Petal:')), pt(S('A', after='Stigma:'), 3, label=S('Stigma:')),
       pt(S('B', after='Anther:'), 3, label=S('Anther:'))], 'bio-2-5', 'parts-of-a-flower',
      SQ(27, 'Match each of the parts labelled A, B and C'), 9, stem=[Q16C], fig='q16-flower',
      id='bio-2024-ol-q16-c-i-fig',
      labels=[L('A', S('Stigma:', page=27), True), L('B', S('Anther:', page=27), True),
              L('C', S('Petal:', page=27), True)],
      decision='One matching exercise: three rows.'),
    T('16cii', 'Q16(c)(ii)', 'C', [_C(8, 'In your answerbook, match each of the parts', 'following functions:', nth=2)]
      + items(8, 'the following functions:', ['Traps pollen', 'Attracts pollinators (e.g. insects)', 'Produces pollen']),
      [pt(S('Stigma (or A)'), 3, label=S('Traps pollen', after='with the following functions')),
       pt(S('Petal (or C)'), 3, label=S('Attracts pollinators (e.g. insects)', after='with the following functions')),
       pt(S('Anther (or B)'), 3, label=S('Produces pollen', after='with the following functions'))],
      'bio-2-5', 'functions-of-flower-parts', SQ(27, 'Match each of the parts of the flower'), 9, stem=[Q16C],
      fig='q16-flower', labels=[L('A', S('Stigma:', page=27), False), L('B', S('Anther:', page=27), False),
                                L('C', S('Petal:', page=27), False)],
      decision='One matching exercise: three rows.'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'What is meant by the term pollination?'),
      [pt(S('Transfer of pollen from the anther to the stigma'), 3)], 'bio-2-5', 'pollination',
      SQ(27, 'What is meant by the term pollination?'), 3, id='bio-2024-ol-q16-c-iii-iv',
      decision='The old card bundled (c)(iii) and (iv); it keeps its id for (iii), and (iv) is added.'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'State two types of pollination.'),
      [anyn(S('Animal / wind / water / self / cross'), 2, 3)], 'bio-2-5', 'types-of-pollination',
      SQ(27, 'State two types of pollination.'), 6),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Is part B the female or male part of the flower?'),
      [pt(S('Male'), 3)], 'bio-2-5', 'anther-is-male', SQ(27, 'Is part B the female or male part'), 3,
      stem=[Q16C], fig='q16-flower', id='bio-2024-ol-q16-c-v-fig'),
    T('16di', 'Q16(d)(i)', 'C', [_C(8, 'In your answerbook, match', 'terms:', after='the human skin.')]
      + items(8, 'X, Y and Z with the following', ['Blood vessel', 'Hair', 'Sebaceous gland']),
      [pt(S('Z', after='Blood vessel:'), 3, label=S('Blood vessel:')), pt(S('X', after='Hair:'), 3, label=S('Hair:')),
       pt(S('Sebaceous gland: Y'), 3)], 'bio-2-4', 'parts-of-the-skin',
      SQ(28, 'Match each of the parts labelled X, Y and Z'), 9, stem=[Q16D], fig='q16-skin',
      id='bio-2024-ol-q16-d-i-fig',
      labels=[L('X', S('Hair:', page=28), True), L('Y', Q(8, 'Sebaceous gland', doc='040'), True),
              L('Z', S('Blood vessel:', page=28), True)],
      decision='One matching exercise: three rows.'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'The skin is a part of the', 'skin excretes.'),
      [pt(S('Sweat or named component of sweat'), 3)], 'bio-2-6', 'skin-excretes-sweat',
      SQ(28, 'Name one substance that the skin excretes.'), 3, id='bio-2024-ol-q16-d-ii-iv',
      decision='The old card bundled (d)(ii)-(iv); it keeps its id for (ii), and (iii), (iv) are added.'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'The skin is also part of the', 'Explain its role in the general defence system.'),
      [pt(S('Acts as a barrier', 'described'), 3)], 'bio-2-4', 'skin-as-a-barrier',
      SQ(28, 'Explain its role in the general defence system.'), 3),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Using information in the diagram, or otherwise', 'body temperature.'),
      [pt(S('Hair raises to trap air', 'retain heat'), 3)], 'bio-2-4', 'skin-and-body-temperature',
      SQ(28, 'Briefly describe one way the skin can help regulate'), 3, stem=[Q16D], fig='q16-skin'),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Name two other excretory organs', 'each organ excretes.'),
      [pt(S('Lungs'), 3, label=S('Name:')),
       pt(S('Substance excreted: Carbon dioxide or water vapour'), 3, note_sel=S('Must match named organ', 'organ')),
       pt(S('Kidney'), 3, label=S('Name:', after='water vapour')),
       pt(S('Substance excreted: Water or urea', 'other correct'), 3,
          note_sel=S('Must match named organ', 'organ'))],
      'bio-2-6', 'excretory-organs', SQ(28, 'Name two other excretory organs'), 12),
    # Q17: any two of (a)-(d), each 30.
    T('17ai1', 'Q17(a)(i)1', 'C', _C(9, 'Which of the labelled structures', 'contains food?'),
      [pt(S('Endosperm or cotyledon'), 3)], 'bio-2-5', 'food-store-of-a-seed',
      SQ(29, 'Which of the labelled structures contains food?'), 3, stem=[Q17A, Q17AI], fig='q17-seed',
      id='bio-2024-ol-q17-a-i-fig', labels=SEED_LABELS(food=True),
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17ai2', 'Q17(a)(i)2', 'C', _C(9, 'Which of the labelled parts', 'plumule?'),
      [pt(S('Embryo'), 3)], 'bio-2-5', 'embryo', SQ(29, 'Which of the labelled parts consists'), 3,
      stem=[Q17A, Q17AI], fig='q17-seed', labels=SEED_LABELS(food=False)),
    T('17aii1', 'Q17(a)(ii)1', 'C', _C(9, 'Where is the testa located?'),
      [pt(S('On the outside of the seed'), 3)], 'bio-2-5', 'testa-location', SQ(29, 'Where is the testa located?'), 3,
      stem=[Q17A, Q17AII], fig='q17-seed', id='bio-2024-ol-q17-a-ii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17aii2', 'Q17(a)(ii)2', 'C', _C(9, 'What is the function of the testa?'),
      [pt(S('Protection'), 3)], 'bio-2-5', 'testa-function', SQ(29, 'What is the function of the testa?'), 3,
      stem=[Q17A, Q17AII], fig='q17-seed'),
    T('17aiii1', 'Q17(a)(iii)1', 'C', _C(9, 'What is meant by the term dormancy?'),
      [pt(S('Resting period of the seed', 'in seed'), 3)], 'bio-2-5', 'dormancy',
      SQ(29, 'What is meant by the term dormancy?'), 3, stem=[Q17A, Q17AIII], id='bio-2024-ol-q17-a-iii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17aiii2', 'Q17(a)(iii)2', 'C', _C(9, 'Give two advantages of dormancy.'),
      [anyn(S('Allows time for development', 'other correct'), 2, 3)], 'bio-2-5', 'advantages-of-dormancy',
      SQ(29, 'Give two advantages of dormancy'), 6, stem=[Q17A, Q17AIII]),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Germination often follows dormancy.', 'essential for germination.'),
      [pt(S('Oxygen'), 3), pt(S('Water'), 3), pt(S('Warmth or suitable temperature'), 3)], 'bio-2-5',
      'conditions-for-germination', SQ(29, 'List the three factors'), 9, stem=[Q17A]),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'The human ear senses', 'these impulses sent?'),
      [pt(S('Brain'), 3)], 'bio-2-4', 'impulses-to-the-brain', SQ(30, 'To which major organ are these impulses sent?'), 3,
      stem=[Q17B], fig='q17-ear'),
    T('17bii', 'Q17(b)(ii)', 'C', [_C(9, 'In your answerbook, match', 'following terms:')]
      + items(9, 'A, B and C with the', ['Ossicle', 'Eardrum', 'Cochlea']),
      [pt(S('B', after='1. Ossicle:'), 3, label=S('Ossicle:')), pt(S('A', after='2. Eardrum:'), 3, label=S('Eardrum:')),
       pt(S('C', after='3. Cochlea:'), 3, label=S('Cochlea:'))], 'bio-2-4', 'parts-of-the-ear',
      SQ(30, 'Match each of the parts labelled A, B and C'), 9, stem=[Q17B], fig='q17-ear',
      labels=[L('A', S('Eardrum:', page=30), True), L('B', S('Ossicle:', page=30), True),
              L('C', S('Cochlea:', page=30), True)],
      decision='One matching exercise: three rows.'),
    T('17biii', 'Q17(b)(iii)', 'C', [_C(9, 'In your answerbook, match each of the parts of the human ear', 'functions:')]
      + items(9, 'and cochlea) with the following functions:',
              ['middle ear', 'auditory canal', 'Generates nerve impulses']),
      [pt(S('Ossicles (or B)'), 3, label=S('Transfers sound vibrations through the middle ear')),
       pt(S('Eardrum (or A)'), 3, label=S('Receives sound waves from the auditory canal')),
       pt(S('Cochlea (or C)'), 3, label=S('Generates nerve impulses'))], 'bio-2-4', 'functions-of-ear-parts',
      SQ(30, 'Match each of the following parts of the human ear'), 9, stem=[Q17B], fig='q17-ear',
      labels=[L('A', S('Eardrum:', page=30), False), L('B', S('Ossicle:', page=30), False),
              L('C', S('Cochlea:', page=30), False)],
      decision='One matching exercise: three rows.'),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'The Eustachian tube is shown in the diagram.', 'Eustachian tube?'),
      [pt(S('To equalise the pressure', 'described'), 3)], 'bio-2-4', 'eustachian-tube',
      SQ(30, 'Why is the middle ear connected to the throat'), 3, stem=[Q17B], fig='q17-ear',
      id='bio-2024-ol-q17-b-iv-v',
      decision='The old card bundled (b)(iv) and (v); it keeps its id for (iv), and (v) is added.'),
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'Hearing is one of the five senses.', 'two senses.'),
      [anyn(S('Sight / touch / smell / taste'), 2, 3)], 'bio-2-4', 'the-senses', SQ(30, 'Name any other two senses.'), 6),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'What is meant by the term vegetative propagation?'),
      [pt(S('Asexual reproduction in plants'), 3)], 'bio-2-5', 'vegetative-propagation',
      SQ(31, 'What is meant by the term vegetative propagation?'), 3, stem=[Q17C], id='bio-2024-ol-q17-c-i-iii',
      decision='The old card bundled (c)(i) and (iii)1-2 and left out (ii); it keeps its id for (i), and '
               '(ii), (iii)1. and (iii)2. are added.'),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'Give two examples of plants that undergo', 'the plant uses.'),
      [pt(S('Named plant'), 3, kind='criterion'), pt(S('Matching organ used'), 3, kind='criterion'),
       pt(S('Named plant', nth=2), 3, kind='criterion'), pt(S('Matching organ used', nth=2), 3, kind='criterion')],
      'bio-2-5', 'examples-of-vegetative-propagation', SQ(31, 'Give two examples of plants'), 12, stem=[Q17C]),
    T('17ciii1', 'Q17(c)(iii)1', 'C', _C(10, 'Give one advantage that vegetative propagation', 'seed.'),
      [pt(S('Faster or other correct'), 3)], 'bio-2-5', 'advantage-of-vegetative-propagation',
      SQ(31, 'Give one advantage that vegetative propagation'), 3, stem=[Q17C]),
    T('17ciii2', 'Q17(c)(iii)2', 'C', _C(10, 'Give one advantage that reproduction by seed', 'propagation.'),
      [pt(S('Offspring are not genetically identical', 'correct'), 3)], 'bio-2-5', 'advantage-of-seeds',
      SQ(31, 'Give one advantage that reproduction by seed'), 3, stem=[Q17C]),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Artificial propagation methods are widely used', 'these methods.'),
      [anyn(S('Cutting / grafting / layering / micropropagation / other correct'), 3, 3)], 'bio-2-5',
      'artificial-propagation', SQ(31, 'Name any three methods of artificial propagation.'), 9),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'What is meant by the term hormone?'),
      [anyn(S('Chemical / messenger', 'elsewhere (or described)'), 2, 3)], 'bio-2-4', 'hormone',
      SQ(32, 'What is meant by the term hormone?'), 6, stem=[Q17D], fig='q17-endocrine'),
    T('17dii', 'Q17(d)(ii)', 'C', [_C(10, 'In your answerbook, match each gland labelled', 'following terms:')]
      + items(10, 'with the following terms:', ['Thyroid', 'Pancreas', 'Testis']),
      [pt(S('B', after='1. Thyroid:'), 3, label=S('Thyroid:')), pt(S('A', after='2. Pancreas:'), 3, label=S('Pancreas:')),
       pt(S('C', after='3. Testis:'), 3, label=S('Testis:'))], 'bio-2-4', 'endocrine-glands',
      SQ(32, 'Match each of the parts of the endocrine system'), 9, stem=[Q17D], fig='q17-endocrine',
      id='bio-2024-ol-q17-d-ii-fig',
      labels=[L('A', S('Pancreas:', page=32), True), L('B', S('Thyroid:', page=32), True),
              L('C', S('Testis:', page=32), True)],
      decision='One matching exercise: three rows.'),
    T('17diii', 'Q17(d)(iii)', 'C', [_C(10, 'In your answerbook, match each gland labelled', 'following hormones:', nth=2)]
      + items(10, 'with the following hormones:', ['Insulin', 'Thyroxine', 'Testosterone']),
      [pt(S('A', after='1. Insulin:'), 3, label=S('Insulin:')), pt(S('B', after='2. Thyroxine:'), 3, label=S('Thyroxine:')),
       pt(S('C', after='3. Testosterone:'), 3, label=S('Testosterone:'))], 'bio-2-4', 'hormones-and-glands',
      SQ(32, 'Match each gland A, B and C'), 9, stem=[Q17D], fig='q17-endocrine', id='bio-2024-ol-q17-d-iii-fig',
      labels=[L('A', S('Pancreas:', page=32), False), L('B', S('Thyroid:', page=32), False),
              L('C', S('Testis:', page=32), False)],
      decision='One matching exercise: three rows.'),
    T('17div', 'Q17(d)(iv)', 'C', _C(10, 'Some glands in the body have both endocrine and', 'exocrine function.'),
      [pt(S('Pancreas or liver or other correct'), 3)], 'bio-2-4', 'endocrine-and-exocrine',
      SQ(32, 'Name one gland in the body that has an endocrine'), 3, id='bio-2024-ol-q17-d-iv-v',
      decision='The old card bundled (d)(iv) and (v); it keeps its id for (iv), and (v) is added.'),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Give one example of the use of a hormone supplement.'),
      [pt(S('HRT or other correct'), 3)], 'bio-2-4', 'hormone-supplements',
      SQ(32, 'Give one example of the use of a hormone supplement.'), 3),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2-yeast': ('038', 4, (325, 55, 541, 268), SEC, ['X', 'Y', 'Z'],
                 'Diagram of a budding yeast cell: a large oval cell with a small rounded bud on top, joined by a '
                 'narrow neck, both with a thick grey wall. A bracket labelled X spans the bud and a bracket '
                 'labelled Y the larger cell; an arrow from Z points to the large dark round body in the larger '
                 'cell. An empty box labelled Cell wall sits to the left.', False),
    'q3-mitosis': ('038', 5, (104, 78, 541, 252), SEC, ['A', 'B'],
                   'Diagram of a cell going through DNA replication and then mitosis, left to right: a round cell '
                   'with two chromosomes, an arrow labelled A pointing to one of them; an arrow marked DNA '
                   'replication to Stage 1, the chromosomes now doubled; Stage 2, an oval cell with the doubled '
                   'chromosomes lined up across its middle and fibres running from end to end; Stage 3, the cell '
                   'pinching in with chromosomes moving to opposite ends, arrows labelled B pointing to the '
                   'fibres in Stages 2 and 3; Stage 4, two round cells, each with two chromosomes.', False),
    'q4-virus': ('038', 6, (255, 92, 415, 205), SEC, ['A', 'B'],
                 'Diagram of a virus: a thick circular outline with a twisted double strand inside it. Arrow A '
                 'points to the outline; arrow B points to the twisted strand.', False),
    'q5-skeleton': ('038', 7, (355, 58, 541, 458), SEC, ['A', 'B', 'C'],
                    'Front-view drawing of the human skeleton. Arrow A points to the head; arrow B to the curved '
                    'bones of the chest; arrow C to the wide bone at the hips.', False),
    'q9-graph': ('038', 10, (125, 592, 490, 740), SEC, ['A', 'B'],
                 'A graph whose vertical axis is labelled by an empty box A and whose horizontal axis, marked 0°C, '
                 '30°C, 60°C and 90°C, is labelled by an empty box B. The curve rises from the axis at 0°C to a '
                 'peak near 30°C, then falls back towards the axis by about 70°C.', False),
    'q10b-ii-question': ('038', 11, (108, 248, 542, 522), SEC, [],
                         'The printed question: (ii) The student’s average results are shown in the table below. '
                         'A table of PR and BR: Resting 60 and 20; Moderate exercise 100 and 30; Intense exercise '
                         '150 and 60. Beside it: Choosing either pulse or breathing rate, complete the name of the '
                         'y-axis and on the grid provided, draw (using pencil) a suitable graph to represent the '
                         'data of either pulse rate (PR) or breathing rate (BR). To the right, an empty grey box '
                         'before the word rate marks the y-axis name, and a blank grid has Resting, Moderate '
                         'exercise and Intense exercise along its horizontal axis.', False),
    'q11-food-web': ('040', 2, (125, 210, 470, 430), SEC, [],
                     'A food web of drawings joined by arrows. Grasses feed the Snail, Mouse, Grasshopper and '
                     'Mosquito; the Snail feeds the Thrush; the Grasshopper feeds the Robin and the Badger; the '
                     'Mosquito feeds the Bat; the Thrush, Mouse and Robin feed the Fox and the Barn owl; the Bat '
                     'feeds the Badger.', False),
    'q12b-i-question': ('040', 3, (108, 222, 525, 278), SEC, [],
                        'The printed question: (i) In your answerbook, write out and complete the following balanced '
                        'equation for aerobic respiration: C6H12O6 + 6O2, an arrow, then 6 followed by a blank, '
                        'plus 6 followed by a blank, plus energy, with the numbers after each element set as '
                        'subscripts.', False),
    'q12-mitochondrion': ('040', 3, (398, 320, 541, 396), SEC, [],
                          'Drawing of a sausage-shaped organelle cut open: a smooth outer membrane and an inner '
                          'membrane folded into many finger-like folds.', False),
    'q12-chloroplast': ('040', 3, (364, 535, 541, 615), SEC, [],
                        'Drawing of an oval organelle with a double outer membrane; inside, stacks of flat discs '
                        'joined by long membranes.', False),
    'q13b-i-question': ('040', 4, (80, 200, 306, 314), SEC, [],
                        'The printed question: (b) Study the diagram of a cross between two pea plants and answer '
                        'the following questions. (i) Both parents were homozygous and the F1 (first generation) '
                        'offspring were heterozygous. Explain the underlined terms. The words homozygous and '
                        'heterozygous are underlined.', False),
    'q13-cross': ('040', 4, (310, 200, 541, 326), SEC, [],
                  'A boxed diagram of a cross. Parents: a Purple-flowered pea plant crossed (x) with a White-'
                  'flowered one. Gametes: P from the purple parent and p from the white parent. F1 offspring: the '
                  'two gametes join to give a Purple-flowered (Pp) plant.', False),
    'q13b-iii-question': ('040', 4, (108, 348, 542, 467), SEC, [],
                          'The printed question: Two of the F1 offspring were then self-fertilised. The F2 (second '
                          'generation) offspring were not all purple-flowered. (iii) Copy the Punnett square into '
                          'your answerbook and complete it to show the genotypes of the F2 offspring. Beside it, '
                          'an empty two-by-two Punnett square: one Purple-flowered (Pp) parent gives gametes P and '
                          'p along the top, the other gives P and p down the side.', False),
    'q13b-iii-scheme': ('scheme', 19, (215, 445, 378, 572), SEC, [],
                        "The marking scheme's completed Punnett square: P and p along the top, P and p down the "
                        'side; the four boxes read PP and Pp in the top row, Pp and pp in the bottom row.', True),
    'q13-punnett': ('040', 4, (380, 350, 542, 468), SEC, [],
                    'An empty two-by-two Punnett square: a Purple-flowered (Pp) plant gives gametes P and p along '
                    'the top, and another Purple-flowered (Pp) plant gives P and p down the side.', False),
    'q14b-iii-question': ('040', 5, (108, 258, 302, 291), SEC, [],
                          'The printed question: (iii) Some bacteria are pathogenic. Explain the underlined term. '
                          'The word pathogenic is underlined.', False),
    'q14-amoeba': ('040', 5, (355, 425, 541, 575), SEC, ['A', 'B', 'C'],
                   'Drawing of Amoeba: a grey, irregular cell with many finger-like extensions. Arrow A points to '
                   'a dark round body near the middle; arrow B to the tip of one of the extensions; arrow C to a '
                   'large pale round space.', False),
    'q15-female': ('040', 6, (140, 140, 450, 322), SEC, ['A', 'B', 'C'],
                   'Front-view diagram of the female reproductive system. Arrow A points to the tube curving out '
                   'from the top of the uterus on the right; arrow B to the small oval organ below it; arrow C to '
                   'the wall of the uterus. Labels Endometrium, Cervix and Vagina point to the uterus lining, the '
                   'neck of the uterus and the passage below it.', False),
    'q16-leaf': ('040', 7, (325, 95, 541, 243), SEC, ['A', 'B'],
                 'Diagram of a transverse section through a leaf. A labels the thin outer layer of cells along the '
                 'top; a bracket B spans the tissue between the upper and lower surfaces. Labels Xylem and Phloem '
                 'point to a vein in the middle; Air space points to a gap between the rounded lower cells; Stoma '
                 'points to an opening in the lower surface.', False),
    'q16-venation': ('040', 7, (405, 328, 541, 438), SEC, ['X', 'Y'],
                     'Two leaves: X is broad with veins branching from the midrib into a network; Y is long and '
                     'narrow with veins running side by side from base to tip.', False),
    'q16-digestive': ('040', 7, (388, 497, 541, 736), SEC, ['A', 'B', 'C', 'D'],
                      'Diagram of the human digestive system in an outline of the head and body. Arrow A points to '
                      'the tube running down the neck; B to the bag-shaped organ beneath the organ labelled Liver; '
                      'C to the coiled tube in the middle of the abdomen; D to the wider tube looping around it.',
                      False),
    'q16-flower': ('040', 8, (375, 56, 541, 226), SEC, ['A', 'B', 'C'],
                   'Diagram of a flower cut in half. Arrow A points to the top of the central stalk; arrow B to a '
                   'rounded head on one of the stalks around it; arrow C to one of the large outer leaves of the '
                   'flower.', False),
    'q16-skin': ('040', 8, (300, 350, 541, 576), SEC, ['X', 'Y', 'Z'],
                 'Diagram of a section through human skin. Arrow X points to a hair growing out of the surface; '
                 'arrow Y to a small gland beside the hair below the surface; arrow Z to a vessel running through '
                 'the deeper layer.', False),
    'q17-seed': ('040', 9, (345, 88, 541, 258), SEC, [],
                 'Diagram of the inside of a seed split in two halves: labels Cotyledon and Embryo point to the '
                 'small curved structure at the top centre, and Endosperm to the large tissue filling the seed.',
                 False),
    'q17-ear': ('040', 9, (286, 383, 541, 580), SEC, ['A', 'B', 'C'],
                'Diagram of the human ear. Arrow A points to the membrane at the end of the ear canal; arrow B to '
                'the tiny bones beyond it; arrow C to the coiled structure further in. Labels Middle ear, '
                'Eustachian tube, Throat (pharynx) and Auditory nerve point to their parts.', False),
    'q17-endocrine': ('040', 10, (390, 268, 541, 508), SEC, ['A', 'B', 'C'],
                      'Outline of a male body with some glands drawn in. Arrow A points to a gland lying across the '
                      'abdomen; arrow B to a gland in the front of the neck; arrow C to the organs at the base of '
                      'the body.', False),
}
