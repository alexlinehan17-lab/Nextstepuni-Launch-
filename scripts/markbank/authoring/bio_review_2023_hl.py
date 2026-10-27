"""Biology 2023 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover
    (with the note that the 2023 papers were adjusted for disruption to
    learning), p2 instructions, p3-p9 Section A Questions 1-7, p10-p12
    Section B Questions 8-10, p13 Section C answerbook instructions, p14-p15
    graph paper, p16-p39 ruled answer pages, p40 back cover. No
    acknowledgements page.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "Do not hand this question paper up", p12 back cover. The paper
    misprints the label of Q15(b) as "16." (page 6); the scheme reprints it
    as Q15(b), and the cards follow the scheme.
  * LC025ALP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7 Irish-medium
    bonus, p8-p33 Questions 1-17, p34-p35 "BLANK PAGE", p36 back cover.

The sitting was already carded (114 authored cards, 113 shipped). As for
2024 and 2025, every task is re-derived from the PDFs at the scheme's own
mark boundaries and the existing cards are corrected in place: every shipped
id is kept, mapped (`id=`) to the task it was carding, verified or corrected
with its old fields recorded; tasks the old cards bundled or missed are
added. bio-2023-hl-q14-b-ii-fig, a figure twin of bio-2023-hl-q14-b-ii that
never shipped, is withdrawn.

Section A is priced on ordered splits, not per part: Q1 "3(6) + 2(1)" over
the best five of six parts; Q2-Q6 "2(5) + 5(2)" over seven responses; Q7
"4 + 2(1)" over (a)(i)-(iii) and "3(4) + 2(1)" over (b)-(e). What a response
earns depends on how many came before it, so these cards carry an
orderedSplit tariff with no per-row marks, each card's total its responses
at the first rate, as the cards this review corrects already did.

One printed choice is marked differently per option and is split into
routes: Q17(d)(vi) xylem or phloem (different drawing and label rows). The
other choices (Q17(b)(vii) paralysis or Parkinson's disease) share one row
and stay one card ("choice is not a route").
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2023, 'hl'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = '38ac900f1'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2023-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': 'cf3498bf77ee4254096fdd1c5a63b4315d97fa5cdedf687c7f1154a308910c89',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2023-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': 'd310ce617cae60431a5fc07c3bbc63186855831632fe4f82777061c0b877774e',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2023-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'a432f615ff7e154d91a2151aad138eb0cb1bc92e128097a31a2e573f1b8bf50d',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 13)},
            13: 'answerbook-instructions', 14: 'graph-paper', 15: 'graph-paper',
            **{p: 'answer-pages' for p in range(16, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 34)}, 34: 'blank', 35: 'blank', 36: 'back-cover'},
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
LADDERS = {
    # "3(6) + 2(1)" over the best five of six parts: six responses carded at 6.
    1: {'steps': [6, 6, 6, 1, 1], 'responses': 6, 'notation': '3(6) + 2(1)'},
    **{q: {'steps': [5, 5, 2, 2, 2, 2, 2], 'notation': '2(5) + 5(2)'} for q in (2, 3, 4, 5, 6)},
    (7, 'a'): {'steps': [4, 1, 1], 'notation': '4 + 2(1)'},
    (7, 'bcde'): {'steps': [4, 4, 4, 1, 1], 'notation': '3(4) + 2(1)'},
}

CHECKSUMS = {
    1: {6: 6}, **{q: {5: 7} for q in (2, 3, 4, 5, 6)}, 7: {4: 8},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, (8, 'b'): {3: 8}, (9, 'b'): {3: 7, 1: 3}, (10, 'b'): {3: 8},
    **{(n, 'a'): {3: 3} for n in range(11, 16)},
    (11, 'b'): {3: 9}, (11, 'c'): {3: 8}, (12, 'b'): {3: 9}, (12, 'c'): {3: 8},
    (13, 'b'): {3: 9}, (13, 'c'): {3: 8}, (14, 'b'): {1: 3, 3: 8}, (14, 'c'): {3: 8},
    (15, 'b'): {3: 7, 1: 6}, (15, 'c'): {3: 8},
    (16, 'a'): {3: 10}, (16, 'b'): {3: 10}, (16, 'c'): {3: 10}, (16, 'd'): {3: 9, 1: 3},
    (17, 'a'): {3: 8, 2: 3}, (17, 'b'): {3: 10}, (17, 'c'): {3: 10}, (17, 'd'): {3: 8, 1: 6},
}

SCAN_PAGES = {'038': range(2, 13), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the ordered split prices the five.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 4, 'the following', 'Q2 "the following hypothesis": the hypothesis quoted, not a choice.'),
    ('038', 5, 'any two', 'Q3(b) "any two bones": bounded menu; one card.'),
    ('038', 6, 'any one', 'Q4(b) "any one DNA nucleotide": open single answer; one card.'),
    ('038', 7, 'any one', 'Q5(d) "any one factor": open single answer; one card.'),
    ('038', 7, 'any one', 'Q5(e) "any one harmful bacterium": open single answer; one card.'),
    ('038', 8, 'the following', 'Q6 lead-in: every statement explained.'),
    ('038', 9, 'the following', 'Q7 lead-in: every part asked.'),
    ('038', 10, 'any two', 'Section B rubric repeated.'),
    ('038', 10, 'the following', 'Q8(a): both terms asked, one card each.'),
    ('038', 10, 'the following', 'Q8(b) lead-in: both parts asked.'),
    ('038', 10, 'the following', 'Q8(b)(i): both pieces of apparatus; one card.'),
    ('038', 11, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 12, 'the following', 'Q10(b)(i) lead-in: both items asked.'),
    ('038', 12, 'the following', 'Q10(b)(ii) lead-in: both items asked.'),
    ('038', 12, 'or', 'Q10(b)(ii) "an ox\'s or sheep\'s heart": the practical, either heart; one card per item.'),
    ('038', 12, 'the following', 'Q10(b)(iii) lead-in: both items asked.'),
    ('038', 12, 'the following', 'Q10(b)(iv) lead-in: both items asked.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q11(a): every term asked, one card each.'),
    ('040', 2, 'or', 'Q11(b) passage "tolerant or resistant": description.'),
    ('040', 2, 'or', 'Q11(b)(ii) "From the passage, or otherwise": source, not a choice of task.'),
    ('040', 2, 'the following', 'Q11(c): both cycles asked, one card each.'),
    ('040', 3, 'or', 'Q12(a)(ii) "anabolic ... or a catabolic": the answer options.'),
    ('040', 3, 'the following', 'Q12(b)(v): the equation to complete.'),
    ('040', 4, 'or', 'Q13(b)(iv) "a Punnett square, or a genetic cross": method, not a choice of task.'),
    ('040', 4, 'both', 'Q13(b)(iv) "both without haemochromatosis": description.'),
    ('040', 4, 'the following', 'Q13(c): "the following pedigree chart", a figure reference.'),
    ('040', 4, 'or', 'Q13(c)(iii) "a Punnett square or otherwise": method, not a choice of task.'),
    ('040', 5, 'or', 'Q14(c) "vegetative propagation or ... artificial propagation": description.'),
    ('040', 5, 'any two', 'Q14(c)(ii) "any two methods": bounded menu; one card.'),
    ('040', 5, 'any three', 'Q14(c)(iii) "any three methods": bounded menu; one card.'),
    ('040', 6, 'the following', 'Q15(b)(i): every label required; one card.'),
    ('040', 6, 'the following', 'Q15(b)(ii): each part asked, one card per item.'),
    ('040', 6, 'or', 'Q15(b)(iii)3 "or otherwise": source, not a choice of task.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q16(b)(iv): each organism group asked, one card per item.'),
    ('040', 8, 'any one', 'Q16(d)(ii) "any one example": open single answer; one card.'),
    ('040', 8, 'any one', 'Q16(d)(iii) "any one example": open single answer; one card.'),
    ('040', 8, 'or', 'Q16(d) "Rhizopus (or common bread mould)": rewording.'),
    ('040', 8, 'the following', 'Q16(d)(iv): every label required; one card.'),
    ('040', 8, 'the following', 'Q16(d)(v): each part asked, one card per item.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'both', 'Q17(a)(ii) "both an endocrine function and an exocrine function": description.'),
    ('040', 9, 'the following', 'Q17(a)(iii): every gland drawn on one outline; one card.'),
    ('040', 9, 'the following', 'Q17(a)(iv): both glands asked; one card.'),
    ('040', 9, 'either', 'Q17(b)(vii) "either of the following ... disorders": the scheme marks both on one row; one card.'),
    ('040', 9, 'the following', 'Q17(b)(vii), same choice.'),
    ('040', 9, 'or', 'Q17(b)(vii), same choice ("paralysis or Parkinson\'s disease").'),
    ('040', 10, 'the following', 'Q17(c) lead-in: every part asked.'),
    ('040', 10, 'the following', 'Q17(c)(i): each vein asked, one card per item.'),
    ('040', 10, 'or', 'Q17(c)(iii)1 "(X or Y)": the answer options.'),
    ('040', 10, 'either', 'Q17(d)(vi) "either type of vascular tissue": the scheme marks xylem and phloem '
                          'on different rows: ROUTES, one card each.'),
]

ROUTES = {'Q17(d)(vi)': ['xylem', 'phloem']}

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2023-hl-q14-b-ii-fig': 'Never shipped: a figure twin of bio-2023-hl-q14-b-ii, which carries the '
                                'reviewed task and its figure.',
}
WITHDRAW = {'bio-2023-hl-q14-b-ii-fig': ('bio-2023-hl-q14-b-ii', RETAINED['bio-2023-hl-q14-b-ii-fig'])}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


Q1 = _A(3, 'Answer any five of the following parts (a) to (f):')
Q2 = _A(4, 'A horticulturist was carrying out scientific research into germination.', 'below.')
Q3 = _A(5, 'The diagram shows the human skeleton.', 'appendicular skeleton.')
Q4 = _A(6, 'DNA is a complex biological molecule. The diagram shows part of a DNA molecule.')
Q5 = _A(7, 'The picture shows a transmission electron microscope image of a bacterial cell.')
Q5F = _A(7, 'The partially drawn graph below represents the microorganism growth curve.')
Q6 = _A(8, 'Give a brief biological explanation for each of the following:')
Q7 = _A(9, 'The graph shows how the absorption of light varies', 'process of photosynthesis.')
Q8A = _A(10, 'Write down the terms that describe each of the following:')
Q8B = _A(10, 'Answer the following questions based on your study of an ecosystem.')
Q9A = _A(11, 'Many cells can respire by anaerobic respiration, producing small amounts of ATP.')
Q9B = _A(11, 'Answer the following in relation to an investigation to prepare alcohol', 'to show its presence.')
Q10B = _A(12, 'The questions below all relate to Unit 3 practical activities.')
Q10BI = _A(12, 'Answer the following based on the growth of leaf yeast using agar plates.')
Q10BII = _A(12, 'Answer the following based on dissecting, displaying and identifying', 'sheep’s heart.')
Q10BIII = _A(12, 'Answer the following based on investigating the effect of IAA on plant tissue.')
Q10BIV = _A(12, 'Answer the following based on viewing a transverse section', 'the light microscope.')
Q11A = _C(2, 'Explain each of the following terms as used in ecology:')
Q11B = [_C(2, 'Read the passage below and answer the questions that follow.'),
        _C(2, 'Ash dieback is a serious disease', 'in Ireland.'),
        _C(2, 'Adapted from Ash Dieback Disease, www.teagasc.ie')]
Q11C = _C(2, 'Describe the main events of each of the following:')
Q12B = _C(3, 'Aerobic respiration is a metabolic reaction that occurs in two stages in living cells.')
Q12C = _C(3, 'Enzymes are important in all metabolic reactions.')
Q13B = _C(4, 'Haemochromatosis is an inherited condition', 'alleles are inherited.')
Q13C = _C(4, 'Haemophilia is caused by a recessive allele', 'children.')
Q14A = _C(5, 'Meristematic tissue is an important tissue in plants.')
Q14B = _C(5, 'The diagram shows a typical animal-pollinated flower.')
Q14C = _C(5, 'Many plants can undergo vegetative propagation', 'artificial propagation.')
Q15BII = _C(6, 'Give one function for each of the following parts:')
Q15BIII = _C(6, 'The diagram shows a human sperm cell.')
Q15C = _C(6, 'The graphs show the levels of female reproductive hormones', 'female reproductive system.')
Q16A = _C(7, 'The graph shows the changes in mass of plant tissue', 'different sugar concentrations.')
Q16B = _C(7, 'Genetic engineering is an important biological technique.')
Q16C = _C(8, 'Viruses are found in all habitats in nature.')
Q16CV = _C(8, 'The human body can defend itself against viruses', 'specific defence system.')
Q16D = _C(8, 'The photographs show some edible mushrooms', 'kingdom Fungi.')
Q16DIV = _C(8, 'Another member of kingdom Fungi is Rhizopus (or common bread mould).')
Q16DV = _C(8, 'Give one function for each of the following parts:')
Q17B = _C(9, 'The diagram shows two separate neurons in close contact.', 'transfer of nerve impulses.')
Q17C = _C(10, 'Answer the following questions in relation to your knowledge of the human circulatory',
          'breathing systems.')
Q17CI = _C(10, 'In each of the following, name the vein that best matches the description:')
Q17CIII = _C(10, 'The diagrams (X and Y) show the two', 'involved in breathing.')
Q17D = _C(10, 'The diagram shows part of a plant organ composed of various tissues.')

TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Name the three chemical elements that are present in all carbohydrates.'),
      [pt(S('Carbon, hydrogen and oxygen'), 6, kind='allOf', note_sel=S('(accept C, H and O)'))], 'bio-1-2',
      'elements-in-carbohydrates', SQ(8, 'Name the three chemical elements'), 6, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Give the general formula for carbohydrates.'),
      [pt(S('Cx(H2O)y'), 6)], 'bio-1-2', 'carbohydrate-general-formula', SQ(8, 'Give the general formula'), 6,
      stem=[Q1]),
    T('1c', 'Q1(c)', 'A', _A(3, 'Name the smallest unit of a carbohydrate.'),
      [pt(S('Monosaccharide'), 6)], 'bio-1-2', 'monosaccharide', SQ(8, 'Name the smallest unit'), 6, stem=[Q1]),
    T('1d', 'Q1(d)', 'A', _A(3, 'Name the type of carbohydrate formed when many', 'bond together.'),
      [pt(S('Polysaccharide'), 6)], 'bio-1-2', 'polysaccharide', SQ(8, 'Name the type of carbohydrate formed'), 6,
      stem=[Q1]),
    T('1e', 'Q1(e)', 'A', _A(3, 'Give one structural role of carbohydrates in living organisms.'),
      [pt(S('Cell wall or other correct'), 6)], 'bio-1-2', 'structural-role-of-carbohydrate',
      SQ(8, 'Give one structural role'), 6, stem=[Q1]),
    T('1f', 'Q1(f)', 'A', _A(3, 'Carbohydrates are an important component of the diet.',
                             'State one dietary source of carbohydrates.'),
      [pt(S('Bread or pasta or other correct dietary source'), 6)], 'bio-1-2', 'dietary-carbohydrate',
      SQ(8, 'State one dietary source'), 6, stem=[Q1]),
    T('2a', 'Q2(a)', 'A', _A(4, 'Draw a vertical line on the graph above', 'germination of grass seeds.'),
      [pt(S('Correct vertical line drawn through peak'), 5, kind='criterion')], 'bio-u2', 'reading-an-optimum',
      SQ(8, 'Draw a vertical line on the graph'), 5, stem=[Q2], fig='q2-graph'),
    T('2b', 'Q2(b)', 'A', _A(4, 'Explain the term hypothesis.'),
      [pt(S('Proposed (or possible) explanation for an observation'), 5)], 'bio-u2', 'hypothesis',
      SQ(8, 'Explain the term hypothesis.'), 5, stem=[Q2], fig='q2-graph'),
    T('2c', 'Q2(c)', 'A', _A(4, 'State one variable from the investigation described above.'),
      [pt(S('(Soil) pH or percentage germination'), 5)], 'bio-u2', 'variable', SQ(8, 'State one variable'), 5,
      stem=[Q2], fig='q2-graph'),
    T('2d', 'Q2(d)', 'A', _A(4, 'Controls are often used in investigations.', 'function of a control?'),
      [pt(S('To act as a comparison to the test (or results or experiment)'), 5)], 'bio-u2', 'control',
      SQ(8, 'What is the function of a control?'), 5, stem=[Q2], fig='q2-graph'),
    T('2e', 'Q2(e)', 'A', _A(4, 'Where might the horticulturist first publish the results of their research?'),
      [pt(S('Scientific journal (or named)'), 5)], 'bio-u1', 'publishing-results',
      SQ(8, 'Where might the horticulturist first publish'), 5, stem=[Q2], fig='q2-graph'),
    T('2f', 'Q2(f)', 'A', _A(4, 'Give two limitations of the scientific method.'),
      [anyn(S('Extent of knowledge / basis of investigation', 'accidental discovery / bias'), 2, 5)], 'bio-u1',
      'limitations-of-scientific-method', SQ(8, 'Give two limitations of the scientific method.'), 10),
    T('3a', 'Q3(a)', 'A', _A(5, 'Give two functions of the skeleton.'),
      [anyn(S('Protection / movement / support / blood cell production'), 2, 5)], 'bio-2-4',
      'functions-of-the-skeleton', SQ(9, 'Give two functions of the skeleton.'), 10, stem=[Q3], fig='q3-skeleton'),
    T('3b', 'Q3(b)', 'A', _A(5, 'Name any two bones of the axial skeleton.'),
      [anyn(S('Skull / vertebra / rib / sternum / mandible'), 2, 5)], 'bio-2-4', 'axial-skeleton',
      SQ(9, 'Name any two bones of the axial skeleton.'), 10, stem=[Q3], fig='q3-skeleton'),
    T('3c', 'Q3(c)', 'A', _A(5, 'Cartilage is an important part of the skeleton.', 'component of cartilage.'),
      [pt(S('Protein'), 5)], 'bio-2-4', 'cartilage-is-protein', SQ(9, 'Name the biomolecule that is the main'), 5,
      stem=[Q3], fig='q3-skeleton'),
    T('3d', 'Q3(d)', 'A', _A(5, 'The innominate bones are part of the', 'as?'),
      [pt(S('Pelvis or hip (bones)'), 5,
          note_sel=S('† Award the assigned marks for part (d) where a candidate has attempted Q3.'))],
      'bio-2-4', 'innominate-bones', SQ(9, '(d)† What are the innominate bones'), 5, stem=[Q3], fig='q3-skeleton',
      decision='The scheme awards these marks to every candidate who attempted Q3; its note is kept on '
               'the row.'),
    T('3e', 'Q3(e)', 'A', _A(5, 'On the diagram, draw an arrow from the', 'movable joint.'),
      [pt(S('Correct arrow to a slightly movable joint'), 5, kind='criterion')], 'bio-2-4', 'slightly-movable-joints',
      SQ(9, 'Draw an arrow from the letter X'), 5, stem=[Q3], fig='q3-skeleton'),
    T('4a', 'Q4(a)', 'A', _A(6, 'Complete the diagram of the DNA molecule', 'labelling the parts you draw.'),
      [pt(S('A and C correctly drawn and labelled'), 5, kind='criterion')], 'bio-1-2', 'completing-dna',
      SQ(9, 'Complete and label the diagram of the DNA molecule.'), 5, stem=[Q4], fig='q4-dna'),
    T('4b', 'Q4(b)', 'A', _A(6, 'On the diagram above, draw a rectangle around any one DNA nucleotide.'),
      [pt(S('Rectangle correctly indicating one DNA nucleotide', 'and one base'), 5, kind='criterion')], 'bio-1-2',
      'dna-nucleotide', SQ(9, 'Draw a rectangle around any one DNA nucleotide.'), 5, stem=[Q4], fig='q4-dna'),
    T('4c', 'Q4(c)', 'A', _A(6, 'What does DNA stand for?'),
      [pt(S('Deoxyribonucleic acid'), 5)], 'bio-1-2', 'deoxyribonucleic-acid', SQ(9, 'What does DNA stand for?'), 5,
      stem=[Q4], fig='q4-dna'),
    T('4d', 'Q4(d)', 'A', _A(6, 'What type of bonding is represented by the letter X on the diagram?'),
      [pt(S('Hydrogen or H (bonding)'), 5)], 'bio-1-2', 'hydrogen-bonds', SQ(9, 'What type of bonding'), 5,
      stem=[Q4], fig='q4-dna'),
    T('4e', 'Q4(e)', 'A', _A(6, 'T is a pyrimidine base. What type of base is G?'),
      [pt(S('Purine'), 5)], 'bio-1-2', 'purines', SQ(9, 'T is a pyrimidine base.'), 5, stem=[Q4], fig='q4-dna'),
    T('4f', 'Q4(f)', 'A', _A(6, 'Name one organelle in eukaryotic cells, other than the nucleus, which contains DNA.'),
      [pt(S('Mitochondrion or chloroplast'), 5)], 'bio-1-3', 'organelles-with-dna',
      SQ(9, 'Name one organelle in eukaryotic cells'), 5),
    T('4g', 'Q4(g)', 'A', _A(6, 'Name the base present in RNA that is not present in DNA.'),
      [pt(S('Uracil or U'), 5)], 'bio-1-2', 'uracil', SQ(9, 'Name the base present in RNA'), 5),
    T('5a', 'Q5(a)', 'A', _A(7, 'There are three types of bacterial', 'the bacterial cell in the picture?'),
      [pt(S('Rod'), 5)], 'bio-3-2', 'bacterial-shape', SQ(10, 'Which type represents the bacterial cell'), 5,
      stem=[Q5], fig='q5-bacterium', id='bio-2023-hl-q5-a-fig'),
    T('5b', 'Q5(b)', 'A', _A(7, 'On the picture, draw an arrow from', 'bacterial cell wall.'),
      [pt(S('Arrow drawn correctly to cell wall'), 5, kind='criterion')], 'bio-3-2', 'bacterial-cell-wall',
      SQ(10, 'Draw an arrow from X to the location'), 5, stem=[Q5], fig='q5-bacterium'),
    T('5c', 'Q5(c)', 'A', _A(7, 'The bacterium in the picture is reproducing asexually.', 'reproduce asexually?'),
      [pt(S('Binary fission'), 5)], 'bio-3-2', 'binary-fission', SQ(10, 'What term describes how bacteria'), 5,
      stem=[Q5], fig='q5-bacterium'),
    T('5d', 'Q5(d)', 'A', _A(7, 'Give any one factor that affects the growth of bacteria.'),
      [pt(S('Temperature or pH or oxygen or food or any correctly named factor'), 5)], 'bio-3-2',
      'bacterial-growth-factors', SQ(10, 'Give any one factor'), 5),
    T('5e', 'Q5(e)', 'A', _A(7, 'Name any one harmful bacterium.'),
      [pt(S('Any named harmful bacterium'), 5, kind='criterion')], 'bio-3-2', 'harmful-bacteria',
      SQ(10, 'Name any one harmful bacterium.'), 5),
    T('5fi', 'Q5(f)(i)', 'A', _A(7, 'By drawing on the graph, complete the first part of the curve.'),
      [pt(S('Curve showing both lag and log phases'), 5, kind='criterion')], 'bio-3-2', 'growth-curve',
      SQ(10, 'By drawing on the graph, complete'), 5, stem=[Q5F], fig='q5-curve'),
    T('5fii', 'Q5(f)(ii)', 'A', _A(7, 'Name the stage indicated by the letter Z.'),
      [pt(S('Decline or death'), 5)], 'bio-3-2', 'decline-phase', SQ(10, 'Name the stage indicated by the letter Z.'),
      5, stem=[Q5F], fig='q5-curve'),
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(8, start, end), [pt(S(ans, aend), 5)], topic, concept, SQ(11, start), 5,
      stem=[Q6])
    for x, start, end, ans, aend, topic, concept in [
        ('a', 'Food chains are limited in length.', None, 'Low amount of energy passed on', 'trophic level)',
         'bio-3-1', 'why-food-chains-are-short'),
        ('b', 'There is always competition between members of a species.', None, 'Resources are limited',
         'rates', 'bio-3-1', 'intraspecific-competition'),
        ('c', 'Fruit formation by plants.', None, 'To protect seeds or to aid seed dispersal', None, 'bio-2-5',
         'why-fruits-form'),
        ('d', 'Urine volume will be low if a person does not regularly drink fluids.', None,
         'More water is reabsorbed', 'tubule).', 'bio-2-6', 'urine-volume'),
        ('e', 'Doctors do not prescribe antibiotics for viral infections.', None,
         '(Antibiotics) do not affect viruses', None, 'bio-1-1', 'antibiotics-and-viruses'),
        ('f', 'Meiosis halves the number of chromosomes in cells.', None, 'To produce gametes',
         'chromosome number', 'bio-2-3', 'why-meiosis-halves'),
        ('g', 'The septum separates the two sides of the human heart.', None,
         'To prevent oxygenated and deoxygenated blood from mixing', None, 'bio-2-6', 'the-septum')]
] + [
    T('7ai', 'Q7(a)(i)', 'A', _A(9, 'Which colour of light is absorbed most by chlorophyll a?'),
      [pt(S('Violet'), 4)], 'bio-2-2', 'chlorophyll-a-absorption', SQ(12, 'Which colour of light is absorbed most by chlorophyll a?'),
      4, stem=[Q7], fig='q7-graph', id='bio-2023-hl-q7-a-fig',
      decision='The old card bundled (a)(i)-(iii), and (iii) also had a card of its own; it keeps its id '
               'for (i), and (ii) is added.'),
    T('7aii', 'Q7(a)(ii)', 'A', _A(9, 'Which colour of light is absorbed most by chlorophyll b?'),
      [pt(S('Blue'), 4)], 'bio-2-2', 'chlorophyll-b-absorption', SQ(12, 'Which colour of light is absorbed most by chlorophyll b?'),
      4, stem=[Q7], fig='q7-graph'),
    T('7aiii', 'Q7(a)(iii)', 'A', _A(9, 'What happens to green and yellow light when they strike chlorophyll?'),
      [pt(S('It is reflected or not absorbed'), 4)], 'bio-2-2', 'green-light-reflected',
      SQ(12, 'What happens to green and yellow light'), 4, stem=[Q7], fig='q7-graph'),
    T('7b', 'Q7(b)', 'A', _A(9, 'The function of chlorophyll is to absorb sunlight energy', 'energised electrons.'),
      [pt(S('Returns to chlorophyll', '(acceptors)'), 4), pt(S('Transferred to NADP', 'carbohydrate (glucose)'), 4)],
      'bio-2-2', 'fates-of-energised-electrons', SQ(12, 'Give two possible fates'), 8),
    T('7c', 'Q7(c)', 'A', _A(9, 'Name another molecule which can provide electrons during photosynthesis.'),
      [pt(S('Water'), 4)], 'bio-2-2', 'water-gives-electrons', SQ(12, 'Name another molecule'), 4),
    T('7d', 'Q7(d)', 'A', _A(9, 'Identify a source of the molecule you named in part (c) above', 'plant.'),
      [pt(S('Soil (or other correct)'), 4)], 'bio-2-2', 'source-of-water',
      SQ(12, 'Identify a source of the molecule'), 4,
      stem=[M('(c)', 9), _A(9, 'Name another molecule which can provide electrons during photosynthesis.')]),
    T('7e', 'Q7(e)', 'A', _A(9, 'Suggest one reason why horticulturists might use carbon dioxide', 'greenhouse.'),
      [pt(S('Improve (crop) yield or increased photosynthesis'), 4)], 'bio-2-2', 'carbon-dioxide-enrichment',
      SQ(12, 'Suggest one reason why horticulturists'), 4),
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(10, 'The parts of the Earth where life can exist.'),
      [pt(S('Biosphere'), 3)], 'bio-3-1', 'biosphere', SQ(13, 'The parts of the Earth where life can exist.'), 3,
      stem=[Q8A], id='bio-2023-hl-q8-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('8aii', 'Q8(a)(ii)', 'B', _A(10, 'Living factors that have an effect on an ecosystem.'),
      [pt(S('Biotic'), 3)], 'bio-3-1', 'biotic-factors', SQ(13, 'Living factors that have an effect'), 3,
      stem=[Q8A]),
    T('8bi', 'Q8(b)(i)', 'B', _A(10, 'Identify the following animal collection apparatus', 'collect animals.'),
      [pt(S('Apparatus: Pooter'), 3), pt(S('Suck through A and animal enters through B.'), 3, label=S('How used:')),
       pt(S('Apparatus: Tullgren funnel'), 3),
       pt(S('Heat (or warmth or light)', 'downwards'), 3, label=S('How used:', after='Tullgren funnel'))],
      'bio-3-1', 'animal-collection-apparatus', SQ(13, 'Identify the following animal collection apparatus'), 12,
      stem=[Q8B], fig='q8-apparatus', id='bio-2023-hl-q8-b-i-fig'),
    T('8bii', 'Q8(b)(ii)', 'B', _A(10, 'As part of your study of an ecosystem', 'percentage cover technique.'),
      [pt(S('Quadrat'), 3), anyn(S('Random (sample) / how random', 'a correct calculation described'), 3, 3)],
      'bio-3-1', 'percentage-cover', SQ(13, 'Describe how you carried out a quantitative survey'), 12, stem=[Q8B]),
    T('9ai', 'Q9(a)(i)', 'B', _A(11, 'What is meant by the term anaerobic?'),
      [pt(S('Oxygen is absent or oxygen is limiting'), 3)], 'bio-2-2', 'anaerobic',
      SQ(14, 'What is meant by the term anaerobic?'), 3, stem=[Q9A], id='bio-2023-hl-q9-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(11, 'What other substance is produced in animal cells', 'respiration?'),
      [pt(S('*Lactic acid'), 3)], 'bio-2-2', 'lactic-acid', SQ(14, 'What other substance is produced'), 3,
      stem=[Q9A]),
    T('9bi', 'Q9(b)(i)', 'B', _A(11, 'In the space provided below, draw a labelled diagram', 'alcohol using yeast.'),
      [pt(S('Diagram: container and solution'), 3, kind='criterion'),
       pt(S('indication of anaerobic conditions', 'anaerobic lock)'), 3, kind='criterion'),
       anyn(S('flask or beaker / water bath', 'oil or anaerobic lock /'), 3, 1)],
      'bio-2-2', 'preparing-alcohol-apparatus', SQ(14, 'Draw a labelled diagram showing how you set up'), 9,
      stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', _A(11, 'Explain the importance of keeping the yeast cells at an optimum temperature.'),
      [pt(S('Allows the enzymes to work at their best (rate of activity)'), 3)], 'bio-2-2', 'optimum-temperature',
      SQ(14, 'Explain the importance of keeping the yeast cells'), 3, stem=[Q9B], id='bio-2023-hl-q9-b',
      decision='The old card bundled (b)(ii)-(v); it keeps its id for (ii), and (iii)-(v) are added.'),
    T('9biii', 'Q9(b)(iii)', 'B', _A(11, 'Alcohol production eventually stops. Explain why this happens.'),
      [pt(S('(The yeast) runs out of glucose', '(alcohol)'), 3)], 'bio-2-2', 'why-fermentation-stops',
      SQ(14, 'Explain why alcohol production eventually stops.'), 3, stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', _A(11, 'How did you know when the reaction had stopped?'),
      [pt(S('Bubbles stop or solution (or yeast) settles'), 3)], 'bio-2-2', 'end-of-fermentation',
      SQ(14, 'How did you know when the reaction had stopped?'), 3, stem=[Q9B]),
    T('9bv', 'Q9(b)(v)', 'B', _A(11, 'Name a test for alcohol and give the final colour observed if alcohol was present.'),
      [pt(S('Iodoform'), 3, label=S('Name:', after='Name a test for alcohol')), pt(S('Final colour: Yellow'), 3)],
      'bio-2-2', 'test-for-alcohol', SQ(14, 'Name a test for alcohol'), 6, stem=[Q9B]),
    T('10a', 'Q10(a)', 'B', _A(12, 'Distinguish between the terms asepsis and sterility, as applied to living organisms.'),
      [pt(S('Asepsis: Free from pathogens'), 3), pt(S('Sterility: Free from (micro)organisms'), 3)], 'bio-3-2',
      'asepsis-and-sterility', SQ(15, 'Distinguish between the terms, asepsis and sterility'), 6),
] + [
    T(key, ref, 'B', _A(12, ask, aend), rows, topic, concept, SQ(15, sq), 3, stem=[Q10B, lead], id=old_id,
      fig=fig, decision=dec)
    for key, ref, ask, aend, rows, topic, concept, sq, lead, old_id, fig, dec in [
        ('10bi1', 'Q10(b)(i)1', 'Name a nutrient added to the agar to enable the growth of leaf yeast.', None,
         [pt(S('Malt'), 3)], 'bio-3-2', 'leaf-yeast-nutrient', '1. Name a nutrient added to the agar', Q10BI,
         'bio-2023-hl-q10-b-i', None,
         'The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
        ('10bi2', 'Q10(b)(i)2', 'Describe the control you used in this investigation.', None,
         [pt(S('(Agar plate) without a leaf (or a sterilised leaf)'), 3)], 'bio-3-2', 'leaf-yeast-control',
         '2. Describe the control you used', Q10BI, None, None, ''),
        ('10bii1', 'Q10(b)(ii)1', 'Name one instrument you used to make the incisions.', None,
         [pt(S('Scalpel or blade'), 3)], 'bio-2-6', 'dissecting-instrument', '1. Name one instrument you used',
         Q10BII, None, None, ''),
        ('10bii2', 'Q10(b)(ii)2', 'Describe one difference between the walls of the right and left ventricles.', None,
         [pt(S('The walls of the left (ventricle) were thicker', 'right)'), 3)], 'bio-2-6', 'ventricle-walls',
         '2. Describe one difference between the walls', Q10BII, None, None, ''),
        ('10biii1', 'Q10(b)(iii)1', 'Name a suitable plant tissue you used.', None,
         [pt(S('Root or shoot or seed or named seed'), 3)], 'bio-2-4', 'tissue-for-iaa',
         '1. Name a suitable plant tissue you used.', Q10BIII, 'bio-2023-hl-q10-b-iii', None,
         'The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
        ('10biii2', 'Q10(b)(iii)2', 'Describe how you measured the effect of IAA on plant tissue.', None,
         [pt(S('Measured lengths using a ruler (or grid)'), 3)], 'bio-2-4', 'measuring-iaa-effect',
         '2. Describe how you measured the effect of IAA', Q10BIII, None, None, ''),
        ('10biv1', 'Q10(b)(iv)1', 'Explain the importance of the section', 'being thin.',
         [pt(S('So that light can pass through the section', 'clearly'), 3)], 'bio-2-6', 'thin-sections',
         '1. Explain the importance of the section being thin.', Q10BIV, 'bio-2023-hl-q10-b-iv', None,
         'The old card carded item 1 only; it keeps its id for 1., and 2. is added.'),
        ('10biv2', 'Q10(b)(iv)2', 'In the space provided, sketch what you', 'light microscope.',
         [pt(S('Sketch showing dermal and vascular tissue'), 3, kind='criterion',
             note='The scheme\'s sketch is shown after reveal.')], 'bio-2-6', 'dicot-stem-section',
         '2. Sketch what you observed', Q10BIV, None, 'q10b-iv-2-scheme', '')]
] + [
    # ------------------------------------------------------------ Section C --
] + [
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, _C(2, term, br=True)], [pt(S(ans), 3)], 'bio-3-1', concept,
      SQ(16, sq), 3, id='bio-2023-hl-q11-a' if r == 'i' else None,
      decision='The old card bundled (a)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'
      if r == 'i' else '')
    for r, term, ans, sq, concept in [('i', 'Ecosystem', 'Organisms and their environment', 'Ecosystem', 'ecosystem'),
                                      ('ii', 'Habitat', 'Place where an organism lives', 'Habitat', 'habitat'),
                                      ('iii', 'Niche', 'Role of an organism', 'Explain each of the following terms', 'niche')]
] + [
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Name the type of ecological relationship that exists between ash trees',
                                   'causes ash dieback.'),
      [pt(S('Parasitism'), 3)], 'bio-3-1', 'parasitism', SQ(16, 'Name the type of ecological relationship between ash'), 3,
      stem=Q11B, id='bio-2023-hl-q11-b-i-ii',
      decision='The old card bundled (b)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'From the passage, or otherwise, state a way', 'survival of ash trees in Ireland.'),
      [pt(S('Establish a gene bank', 'other correct way'), 3)], 'bio-3-1', 'saving-ash-trees',
      SQ(16, 'State a way that ecologists'), 3, stem=Q11B),
    T('11biii', 'Q11(b)(iii)', 'C', _C(2, 'Write down a food chain (with at least three trophic levels)', 'passage above.'),
      [pt(S('Ash → Moth → Robin'), 3)], 'bio-3-1', 'ash-food-chain', SQ(16, 'Write down a food chain'), 3, stem=Q11B),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'Sketch a pyramid of numbers based on the food chain', 'above.'),
      [pt(S('Correct order with Ash on the bottom'), 3, kind='criterion'),
       pt(S('Partially upright pyramid drawn'), 3, kind='criterion',
          note='The scheme\'s pyramid is shown after reveal.')], 'bio-3-1', 'pyramid-of-numbers',
      SQ(16, 'Sketch a pyramid of numbers'), 6, fig='q11b-iv-scheme',
      stem=Q11B + [M('(iii)', 2), _C(2, 'Write down a food chain (with at least three trophic levels)', 'passage above.')]),
    T('11bv', 'Q11(b)(v)', 'C', _C(2, 'Suggest two possible effects on the ecosystem if all ash trees in Ireland died.'),
      [anyn(S('Moth (or other consumers of ash)', 'correct environmental effect'), 2, 3)], 'bio-3-1',
      'losing-the-ash', SQ(16, 'Suggest two possible effects'), 6, stem=Q11B),
    T('11bvi1', 'Q11(b)(vi)1', 'C', _C(2, 'Name the type of ecological relationship that exists between the robin and',
                                       'the moth.'),
      [pt(S('Predation or predator-prey'), 3)], 'bio-3-1', 'predation', SQ(16, '1. Name the type of ecological'), 3,
      stem=Q11B, id='bio-2023-hl-q11-b-vi',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('11bvi2', 'Q11(b)(vi)2', 'C', _C(2, 'Explain the importance of this type of ecological relationship in nature.'),
      [pt(S('Population control or described'), 3)], 'bio-3-1', 'importance-of-predation',
      SQ(16, '2. Explain the importance'), 3,
      stem=Q11B + [M('1.', 2), _C(2, 'Name the type of ecological relationship that exists between the robin and',
                                  'the moth.')]),
    T('11ci', 'Q11(c)(i)', 'C', [Q11C, _C(2, 'The nitrogen cycle', br=True)],
      [anyn(S('Nitrogen (gas) to usable compounds /', 'any one named process'), 4, 3)], 'bio-3-2', 'nitrogen-cycle',
      SQ(17, 'The nitrogen cycle'), 12),
    T('11cii', 'Q11(c)(ii)', 'C', [Q11C, _C(2, 'The carbon cycle.', br=True)],
      [anyn(S('Carbon dioxide is fixed into plant carbohydrate', 'any one named process'), 4, 3)], 'bio-3-2',
      'carbon-cycle', SQ(17, '(ii) The carbon cycle'), 12),
    T('12ai', 'Q12(a)(i)', 'C', _C(3, 'Explain the term metabolism.'),
      [pt(S('(All) chemical reactions in an organism (or in a cell)'), 3)], 'bio-2-1', 'metabolism',
      SQ(18, 'Explain the term metabolism.'), 3),
    T('12aii', 'Q12(a)(ii)', 'C', _C(3, 'Is the reaction shown below an anabolic reaction or a catabolic reaction?',
                                     'Explain your answer.'),
      [pt(S('*Catabolic'), 3), pt(S('Large molecule broken down', 'energy released'), 3)], 'bio-2-1',
      'catabolic-reaction', SQ(18, 'Is the reaction shown below an anabolic or catabolic?'), 6,
      qfig='q12a-ii-question',
      decision='The reaction is printed as letters joined by a drawn arrow the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'Copy the diagram of the cell into your', 'stage 1 and stage 2.'),
      [pt(S('Stage 2', after='Nucleus'), 3, kind='criterion'),
       pt(S('Stage 1', after='Nucleus'), 3, kind='criterion',
          note='The scheme marks each stage on its copy of the cell, shown after reveal.')], 'bio-2-2',
      'where-respiration-happens', SQ(18, 'Copy the diagram of the cell and indicate'), 6, stem=[Q12B],
      qfig='q12b-i-question', fig='q12b-i-scheme',
      decision='The scheme answers with its own copy of the cell, each stage labelled where it happens: the '
               'labels are its rows and the drawing is the solution figure.'),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'What is the name given to stage 1?'),
      [pt(S('*Glycolysis'), 3)], 'bio-2-2', 'glycolysis', SQ(18, 'What is the name given to stage 1?'), 3,
      stem=[Q12B], id='bio-2023-hl-q12-b-ii-iii',
      decision='The old card bundled (b)(ii) and (iii); it keeps its id for (ii), and (iii) is added.'),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'Stage 1 ends with the formation of a', 'Name this compound.'),
      [pt(S('*Pyruvate or pyruvic acid'), 3)], 'bio-2-2', 'pyruvate', SQ(18, 'Stage 1 ends with the formation'), 3,
      stem=[Q12B]),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'This three-carbon compound is converted', 'electrons after they are removed.'),
      [anyn(S('Pass to NAD', 'to make water'), 3, 3)], 'bio-2-2', 'electron-transport',
      SQ(18, 'Describe in detail what happens to these electrons'), 9, stem=[Q12B]),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'ATP is produced during respiration.', 'missing parts of the equation.'),
      [G('tokens', page=18, clip=(143, 523, 153, 539), expect='P', marks=3),
       G('tokens', page=18, clip=(240, 523, 264, 539), expect='H2O', marks=3,
         note='The scheme\'s completed equation is shown after reveal.')], 'bio-2-2', 'atp-equation',
      SQ(18, 'Complete the missing parts of the equation.'), 6, stem=[Q12B], qfig='q12b-v-question',
      fig='q12b-v-scheme',
      decision='The scheme prints the whole equation and underlines the two parts the paper leaves blank; '
               'those two are its rows, read by position, and the equation with its arrow is the solution '
               'figure.'),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'What is an enzyme?'),
      [pt(S('Protein (or biological) catalyst'), 3)], 'bio-2-1', 'enzyme', SQ(19, 'What is an enzyme?'), 3,
      stem=[Q12C], id='bio-2023-hl-q12-c',
      decision='The old card bundled (c)(i)-(iv); it keeps its id for (i), and (ii)-(iv) are added.'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Describe in detail the active site theory of enzyme action.'),
      [anyn(S('Complementary shape to substrate /', 'enzyme can be reused'), 4, 3)], 'bio-2-1', 'active-site-theory',
      SQ(19, 'Describe in detail the active site theory'), 12, stem=[Q12C]),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Describe what happens to an enzyme if it is overheated.'),
      [pt(S('Loses shape or loses function or becomes denatured'), 3)], 'bio-2-1', 'denaturation',
      SQ(19, 'Describe what happens to an enzyme'), 3, stem=[Q12C]),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Give one example of a catabolic enzyme and one example of an anabolic', 'enzyme.'),
      [pt(S('Amylase or any correct example'), 3, label=S('Catabolic enzyme:')),
       pt(S('Polymerase or any correct example'), 3, label=S('Anabolic enzyme:'))], 'bio-2-1',
      'catabolic-and-anabolic-enzymes', SQ(19, 'Give one example of a catabolic enzyme'), 6, stem=[Q12C]),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Which famous scientist is regarded as the father of genetics?'),
      [pt(S('(Gregor) Mendel'), 3)], 'bio-1-4', 'mendel', SQ(20, 'Which famous scientist'), 3,
      id='bio-2023-hl-q13-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'State the Law of Segregation.'),
      [anyn(S('Each trait is controlled by a pair of factors /', 'for each trait'), 2, 3)], 'bio-1-4',
      'law-of-segregation', SQ(20, 'State the Law of Segregation.'), 6),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Explain each of the underlined terms.'),
      [pt(S('Piece of DNA (or chromosome)', 'inheritance'), 3, label=S('Gene:')),
       pt(S('Recessive: Allele masked by the dominant allele or explained'), 3)], 'bio-1-4', 'gene-and-recessive',
      SQ(20, 'Explain each of the underlined terms'), 6, stem=[Q13B], qfig='q13b-i-question',
      decision='The paper marks the terms to explain by underlining them, which the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Give one possible cause of gene mutations.'),
      [pt(S('Chemicals or radiation or named example'), 3)], 'bio-2-3', 'causes-of-gene-mutation',
      SQ(20, 'Give one possible cause of gene mutations.'), 3, stem=[Q13B], id='bio-2023-hl-q13-b-ii-iii',
      decision='The old card bundled (b)(ii) and (iii); it keeps its id for (ii), and (iii) is added.'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Name another type of mutation and give a condition', 'mutation.'),
      [pt(S('*Chromosome'), 3), pt(S('Down’s syndrome (or other correctly named condition)'), 3)], 'bio-2-3',
      'chromosome-mutation', SQ(20, 'Name another type of genetic mutation'), 6, stem=[Q13B]),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'The letter H can be used to represent the dominant allele', 'condition.'),
      [pt(S('Hh x Hh'), 3, label=S('Parents:', after='Explain how it is possible')),
       pt(S('h', after='Allele passed on'), 3, label=S('Allele passed on from both parents (in gametes):')),
       pt(S('Offspring: hh and sufferer indicated'), 3)], 'bio-1-4', 'carriers-of-haemochromatosis',
      SQ(20, 'Explain how it is possible for two unaffected parents'), 9, stem=[Q13B], id='bio-2023-hl-q13-b-iv-v',
      decision='The old card bundled (b)(iv) and (v); it keeps its id for (iv), and (v) is added.'),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'If the parents have a child without haemochromatosis', 'carrier?'),
      [pt(S('Genetic screening or described'), 3)], 'bio-1-4', 'genetic-screening',
      SQ(20, 'How might they check to see if their child was a carrier?'), 3, stem=[Q13B]),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'What term is used to describe an allele present on the X chromosome?'),
      [pt(S('Sex linked or X-linked'), 3)], 'bio-1-4', 'sex-linkage', SQ(21, 'What term is used to describe an allele'), 3,
      stem=[Q13C], fig='q13-pedigree'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'The letter N can be used to represent the dominant allele', 'which is male.'),
      [pt(S('Chromosome diagrams showing XX and XY'), 3, kind='criterion'),
       pt(S('Correct alleles and loci for each parent'), 3, kind='criterion'),
       pt(S('Male and/or female correctly indicated'), 3, kind='criterion')], 'bio-1-4',
      'sex-linked-chromosome-diagrams', SQ(21, 'Draw two fully labelled chromosome diagrams'), 9, stem=[Q13C],
      fig='q13-pedigree'),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'The pedigree chart above shows that two of their male children', 'haemophilia.', end_nth=2),
      [pt(S('XN'), 3, label=S('Gametes from Parent 1:')),
       pt(S('Y–'), 3, label=S('Gametes from Parent 2:')),
       pt(S('XYN–', 'genotype indicated as a non-sufferer'), 3, label=S('Genotype of son:'))],
      'bio-1-4', 'non-sufferer-son', SQ(21, 'Show how it is possible for the parents'), 9, stem=[Q13C],
      fig='q13-pedigree',
      decision='The scheme prints the gametes and the son\'s genotype inline, as "XN", "Y–" and "XYN–" '
               '(checked on the rendered page): the rows carry them as printed.'),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'Explain clearly why it would be almost impossible for person 7', 'haemophilia.'),
      [pt(S('Person 7 does not have the recessive allele or described'), 3)], 'bio-1-4', 'person-7',
      SQ(21, 'Explain why it would be almost impossible'), 3, stem=[Q13C], fig='q13-pedigree',
      id='bio-2023-hl-q13-c-iv-fig'),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'What is the meristem?'),
      [pt(S('Region where mitosis can occur', '(active) cell division'), 3)], 'bio-2-6', 'meristem',
      SQ(22, 'What is the meristem?'), 3, stem=[Q14A], id='bio-2023-hl-q14-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Give two locations in plants where meristematic tissue may be found.'),
      [anyn(S('Shoot tip / root tip', 'other correct'), 2, 3)], 'bio-2-6', 'meristem-locations',
      SQ(22, 'Give two locations in plants'), 6, stem=[Q14A]),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Name the structures A, B and C.'),
      [pt(S('A: Stigma'), 1), pt(S('B: Anther'), 1), pt(S('C: Sepal'), 1)], 'bio-2-5', 'parts-of-a-flower',
      SQ(22, 'Name structures A, B and C.'), 3, stem=[Q14B], fig='q14-flower', id='bio-2023-hl-q14-b-i-fig',
      labels=[L('A', S('Stigma', page=22, after='Name structures A, B and C.'), True),
              L('B', S('Anther', page=22, after='A: Stigma'), True),
              L('C', S('Sepal', page=22, after='B: Anther'), True)]),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Give one function for each structure A and B.'),
      [pt(S('A: Trap pollen or described'), 3), pt(S('B: Produce (or release) pollen'), 3)], 'bio-2-5',
      'stigma-and-anther', SQ(22, 'Give one function for each structure A and B.'), 6, stem=[Q14B],
      fig='q14-flower',
      labels=[L('A', S('Stigma', page=22, after='Name structures A, B and C.'), True),
              L('B', S('Anther', page=22, after='A: Stigma'), True),
              L('C', S('Sepal', page=22, after='B: Anther'), False)]),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'Describe one way in which a wind-pollinated flower would differ', 'animal-pollinated flower.'),
      [pt(S('Anthers (or stigmas) outside of flower', 'no nectar'), 3)], 'bio-2-5', 'wind-pollinated-flowers',
      SQ(22, 'Describe one way in which a wind-pollinated'), 3, stem=[Q14B], fig='q14-flower'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Embryo sac development occurs in the ovule.', 'development in detail.'),
      [anyn(S('Diploid / megaspore mother cell', 'two polar nuclei (formed)'), 4, 3)], 'bio-2-5',
      'embryo-sac-development', SQ(22, 'Describe embryo sac development in detail.'), 12,
      id='bio-2023-hl-q14-b-iv-v',
      decision='The old card bundled (b)(iv) and (v); it keeps its id for (iv), and (v) is added.'),
    T('14bv', 'Q14(b)(v)', 'C', _C(5, 'What does the ovule develop into if fertilisation occurs?'),
      [pt(S('*Seed'), 3)], 'bio-2-5', 'ovule-to-seed', SQ(22, 'What does the ovule develop into'), 3),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'What is meant by the term vegetative propagation?'),
      [pt(S('Asexual reproduction (in plants)', 'parts (or named part)'), 3)], 'bio-2-5', 'vegetative-propagation',
      SQ(23, 'What is meant by the term vegetative propagation?'), 3, stem=[Q14C], id='bio-2023-hl-q14-c',
      decision='The old card bundled (c)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Name any two methods of vegetative propagation used by plants', 'vegetative propagation.'),
      [anyn(S('Stem / root / leaf / bud'), 2, 3),
       anyn(None, 2, 3, open_list=True,
            options=[S('Stem: e.g. strawberry (or other correct)'), S('Root: e.g. dahlia (or other correct)'),
                     S('Leaf: e.g. kalanchoe (or other correct)'), S('Bud:', 'e.g. onion (or other correct)')],
            note_sel=S('(Two examples, must match methods)'))],
      'bio-2-5', 'methods-of-vegetative-propagation', SQ(23, 'Name any two methods of vegetative propagation'), 12,
      stem=[Q14C]),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Name any three methods horticulturists may use to artificially propagate plants.'),
      [anyn(S('Cutting / layering / grafting / micro propagation (tissue culture)'), 3, 3)], 'bio-2-5',
      'artificial-propagation', SQ(23, 'Name any three examples of methods'), 9, stem=[Q14C]),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'What is meant by the term secondary sexual characteristics?'),
      [pt(S('Features that distinguish male from female', 'at puberty'), 3)], 'bio-2-5',
      'secondary-sexual-characteristics', SQ(24, 'What is meant by the term secondary sexual'), 3,
      id='bio-2023-hl-q15-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Give two examples of secondary sexual characteristics present in males.'),
      [anyn(S('Deep voice / enlarged muscles', 'other correct'), 2, 3)], 'bio-2-5', 'male-secondary-characteristics',
      SQ(24, 'Give two examples of a secondary sexual'), 6),
    T('15bi', 'Q15(b)(i)', 'C', [_C(6, 'Draw a large diagram of the human male reproductive system, labelling the',
                                    'following parts:'),
                                 _C(6, 'testis', br=True), _C(6, 'sperm', 'duct', br=True),
                                 _C(6, 'prostate', 'gland', br=True), _C(6, 'epididymis', br=True),
                                 _C(6, 'penis', br=True), _C(6, 'scrotum', br=True)],
      [pt(S('Penis, testis, urethra and sperm duct'), 6, kind='criterion', units=[3, 3],
          note_sel=S('(Any one missing only 3 marks)')),
       anyn(S('Testis / sperm duct / prostate gland / epididymis / penis / scrotum'), 6, 1)],
      'bio-2-5', 'male-reproductive-system', SQ(24, 'Labelled diagram of male reproductive system.'), 12,
      decision='The paper prints this part\'s label as "16." (a misprint for (b)); the scheme marks it as '
               'Q15(b), and so does the card.'),
    T('15bii1', 'Q15(b)(ii)1', 'C', [Q15BII, _C(6, '1.', 'Prostate gland', after='Give one function for each', br=True)],
      [pt(S('Prostate gland: To produce seminal fluid or described'), 3)], 'bio-2-5', 'prostate-gland',
      SQ(24, 'Give one function for each of the following parts:'), 3, id='bio-2023-hl-q15-b-ii',
      decision='"For each of the following": two separately priced items, one card each; the old card '
               'keeps its id for 1., and 2. is added.'),
    T('15bii2', 'Q15(b)(ii)2', 'C', [Q15BII, _C(6, '2.', 'Epididymis', after='Give one function for each', br=True)],
      [pt(S('To store sperm or to allow sperm mature', 'sperm duct'), 3, label=S('Epididymis:'))], 'bio-2-5',
      'epididymis', SQ(24, 'Give one function for each of the following parts:'), 3),
    T('15biii1', 'Q15(b)(iii)1', 'C', _C(6, 'How many chromosomes are found', 'sperm cell?'),
      [pt(S('*23'), 3)], 'bio-2-5', 'chromosomes-in-a-sperm', SQ(24, '1. How many chromosomes are found'), 3,
      stem=[Q15BIII], fig='q15-sperm', id='bio-2023-hl-q15-b-iii',
      decision='The old card bundled items 1 and 3; it keeps its id for 1., and 2. and 3. are added.'),
    T('15biii2', 'Q15(b)(iii)2', 'C', _C(6, 'Copy out the diagram of the human', 'location of the mitochondria.'),
      [pt(S('Mitochondria', after='Copy out the diagram of the sperm cell'), 3, kind='criterion',
          note='The scheme\'s sperm cell, with the mitochondria marked, is shown after reveal.')], 'bio-2-5',
      'mitochondria-in-sperm', SQ(24, '2. Copy out the diagram of the sperm cell'), 3, stem=[Q15BIII],
      qfig='q15b-iii-2-question', fig='q15b-iii-2-scheme',
      decision='The scheme answers with its own drawing, the mitochondria labelled: the label is the row '
               'and the drawing is the solution figure.'),
    T('15biii3', 'Q15(b)(iii)3', 'C', _C(6, 'In relation to the structure of the sperm cell, or otherwise', 'male infertility.'),
      [pt(S('Low sperm count', 'blockage'), 3)], 'bio-2-5', 'male-infertility', SQ(24, '3. Suggest one possible cause'), 3,
      stem=[Q15BIII], fig='q15-sperm'),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'How long is the typical menstrual cycle in a human female?'),
      [pt(S('28 – 31 days'), 3, note_sel=S('(Accept one month)'))], 'bio-2-5', 'length-of-the-cycle',
      SQ(25, 'How long is the typical menstrual cycle'), 3, stem=[Q15C], fig='q15-graph'),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Name each of the hormones A and B.'),
      [pt(S('A: *Oestrogen'), 3), pt(S('B: *Progesterone'), 3)], 'bio-2-5', 'oestrogen-and-progesterone',
      SQ(25, 'Name each of the hormones A and B.'), 6, stem=[Q15C], fig='q15-graph', id='bio-2023-hl-q15-c-ii-fig',
      labels=[L('A', S('*Oestrogen', page=25), True), L('B', S('*Progesterone', page=25), True)]),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'There are low levels of hormone A and hormone B', 'hormones A and B.'),
      [pt(S('Menstruation or FSH produced or new follicle starts developing'), 3)], 'bio-2-5',
      'low-hormone-levels', SQ(25, 'Describe one effect on the female reproductive system'), 3, stem=[Q15C],
      fig='q15-graph', id='bio-2023-hl-q15-c-iii-iv-vii',
      decision='The old card bundled (c)(iii), (iv) and (vii); it keeps its id for (iii), and (iv), (vii) '
               'are added.'),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Explain why hormone A levels increase after approximately day 5.'),
      [pt(S('Follicle secretes (more) oestrogen', 'production of oestrogen'), 3)], 'bio-2-5', 'rising-oestrogen',
      SQ(25, 'Explain why hormone A levels increase'), 3, stem=[Q15C], fig='q15-graph'),
    T('15cv', 'Q15(c)(v)', 'C', _C(6, 'What event occurs around day 14 of the menstrual cycle?'),
      [pt(S('Ovulation or release of egg (from the ovary)'), 3)], 'bio-2-5', 'ovulation',
      SQ(25, 'What event occurs around day 14'), 3, stem=[Q15C], fig='q15-graph', id='bio-2023-hl-q15-c-v-vi',
      decision='The old card bundled (c)(v) and (vi); it keeps its id for (v), and (vi) is added.'),
    T('15cvi', 'Q15(c)(vi)', 'C', _C(6, 'The event you named in part (c) (v) above is caused by a surge', 'Name this hormone.'),
      [pt(S('*LH (or luteinising hormone)'), 3)], 'bio-2-5', 'luteinising-hormone',
      SQ(25, 'The event you named above is caused'), 3,
      stem=[Q15C, M('(v)', 6), _C(6, 'What event occurs around day 14 of the menstrual cycle?')], fig='q15-graph'),
    T('15cvii', 'Q15(c)(vii)', 'C', _C(6, 'Explain why hormone B levels increase in the days after day 14.'),
      [pt(S('Corpus luteum secretes progesterone', 'progesterone', nth=1), 3)], 'bio-2-5', 'rising-progesterone',
      SQ(25, 'Explain why hormone B levels increase'), 3, stem=[Q15C], fig='q15-graph'),
    # Q16: any two of (a)-(d), each 30.
    T('16ai', 'Q16(a)(i)', 'C', _C(7, 'Name the substance that causes the change in mass of the plant tissue.'),
      [pt(S('*Water'), 3)], 'bio-2-6', 'water-moves', SQ(26, 'Name the substance that causes the change'), 3,
      stem=[Q16A], fig='q16-graph', id='bio-2023-hl-q16-a-i-ii-iv',
      decision='The old card bundled (a)(i), (ii) and (iv); it keeps its id for (i), and (ii), (iv) are added.'),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'What term is given to the movement in and out of the plant tissue', 'above?'),
      [pt(S('*Osmosis'), 3)], 'bio-2-6', 'osmosis', SQ(26, 'What term is given to the movement'), 3,
      stem=[Q16A, M('(i)', 7), _C(7, 'Name the substance that causes the change in mass of the plant tissue.')],
      fig='q16-graph'),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'At what sugar concentration is there no change in the mass of the plant tissue?'),
      [pt(S('*4 g/100cm3'), 3)], 'bio-2-6', 'isotonic-concentration', SQ(26, 'At what sugar concentration'), 3,
      stem=[Q16A], fig='q16-graph'),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'Explain in detail why there is no change in mass at the sugar concentration', 'above.'),
      [pt(S('*Movement of water into the cells equals', 'out of the cells'), 3),
       pt(S('*Due to the sugar concentration inside the cells', 'outside the cells.'), 3)], 'bio-2-6',
      'no-net-osmosis', SQ(26, 'Explain in detail why there is no change in mass'), 6,
      stem=[Q16A, M('(iii)', 7), _C(7, 'At what sugar concentration is there no change in the mass of the plant tissue?')],
      fig='q16-graph'),
    T('16av1', 'Q16(a)(v)1', 'C', _C(7, 'What term is used to describe the condition of the plant cells', 'sugar solution?'),
      [pt(S('*Turgid'), 3)], 'bio-2-6', 'turgidity', SQ(26, '1. What term is used to describe the condition'), 3,
      stem=[Q16A], fig='q16-graph', id='bio-2023-hl-q16-a-v',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. The scheme '
               'reprints the solution as "2 g/100cm3"; the paper asks about 0 g/100 cm3, and the card '
               'carries the paper\'s question.'),
    T('16av2', 'Q16(a)(v)2', 'C', _C(7, 'Explain how plant cells maintain the condition', 'above.'),
      [pt(S('(Presence of) the cell wall', 'as they lose.'), 3)], 'bio-2-6', 'staying-turgid',
      SQ(26, '2. Explain how plant cells maintain'), 3,
      stem=[Q16A, M('1.', 7), _C(7, 'What term is used to describe the condition of the plant cells', 'sugar solution?')],
      fig='q16-graph'),
    T('16avi', 'Q16(a)(vi)', 'C', _C(7, 'Explain in detail why the mass of the plant cells reduces', 'sugar solution.'),
      [pt(S('Water has moved out of the cells (by osmosis)'), 3),
       pt(S('(Water moves) from a region of high water concentration', 'inside the cells.'), 3)], 'bio-2-6',
      'plasmolysis', SQ(26, 'Explain in detail why the mass of the plant cells reduces'), 6, stem=[Q16A],
      fig='q16-graph', id='bio-2023-hl-q16-a-vi-vii',
      decision='The old card bundled (a)(vi) and (vii); it keeps its id for (vi), and (vii) is added.'),
    T('16avii', 'Q16(a)(vii)', 'C', _C(7, 'What do you think would happen to an animal cell in the 0 g/100 cm3', 'solution?'),
      [pt(S('Increase in size or swell or burst'), 3)], 'bio-2-6', 'animal-cell-in-water',
      SQ(26, 'What do you think would happen to an animal cell'), 3),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'What is meant by the term genetic engineering?'),
      [pt(S('(Artificial) manipulation of a gene', 'of DNA)', nth=1), 3)], 'bio-3-3', 'genetic-engineering',
      SQ(27, 'What is meant by the term genetic engineering?'), 3, stem=[Q16B], id='bio-2023-hl-q16-b-i-ii',
      decision='The old card bundled (b)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Describe the process of genetic engineering up to the point', 'gene of interest.'),
      [anyn(S('Isolation of DNA (from cells) /', 'grown (in nutrient medium).'), 4, 3)], 'bio-3-3',
      'process-of-genetic-engineering', SQ(27, 'Describe the process of genetic engineering'), 12, stem=[Q16B]),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'The final part of genetic engineering,', 'involved in protein synthesis.'),
      [pt(S('Messenger RNA (mRNA)'), 3), pt(S('Transfer RNA (tRNA)'), 3)], 'bio-2-3', 'types-of-rna',
      SQ(27, 'Name the two other types of RNA'), 6, stem=[Q16B], fig='q16-ribosome'),
] + [
    T(f'16biv{n}', f'Q16(b)(iv){n}', 'C', [_C(7, 'State one application of genetic engineering for each of the following:'),
                                          _C(7, f'{n}.', group, after='State one application of genetic', br=True)],
      [pt(S('Any correct application given', after=after), 3, kind='criterion')], 'bio-3-3',
      f'genetic-engineering-{slug}', SQ(27, 'State one application of genetic engineering'), 3, stem=[Q16B],
      decision='"For each of the following": three separately priced items, one card each.')
    for n, group, after, slug in [(1, 'Animals', 'Animals:', 'animals'),
                                  (2, 'Microorganisms', '2.', 'microorganisms'),
                                  (3, 'Plants.', 'Plants:', 'plants')]
] + [
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'The diagram shows a typical', 'Name the structures X and Y.'),
      [pt(S('X: Protein (coat) or capsid'), 3), pt(S('Y: Nucleic acid or DNA or RNA'), 3)], 'bio-1-1',
      'structure-of-a-virus', SQ(28, 'Name structures X and Y.'), 6, stem=[Q16C], fig='q16-virus',
      id='bio-2023-hl-q16-c-i-fig',
      labels=[L('X', S('Protein (coat) or capsid', page=28), True), L('Y', S('Nucleic acid or DNA or RNA', page=28), True)]),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Explain the difficulty in describing', 'viruses as living.'),
      [pt(S('Non-cellular or no metabolism'), 3)], 'bio-1-1', 'are-viruses-living',
      SQ(28, 'Explain the difficulty in describing viruses as living.'), 3, stem=[Q16C]),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Name two harmful viruses.'),
      [anyn(S('Common cold virus or coronavirus', 'other correct'), 2, 3, sep=' or ')], 'bio-1-1', 'harmful-viruses',
      SQ(28, 'Name two harmful viruses.'), 6, stem=[Q16C], id='bio-2023-hl-q16-c-iii-iv',
      decision='The old card bundled (c)(iii) and (iv); it keeps its id for (iii), and (iv) is added. The '
               'scheme prices "2(3)" over one "or" list: a menu of two.'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Give one way in which viruses can', 'be beneficial to humans.'),
      [pt(S('Can be used (as a vector)', 'any other valid answer'), 3)], 'bio-1-1', 'beneficial-viruses',
      SQ(28, 'Give one way in which viruses can be beneficial'), 3, stem=[Q16C]),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Give two ways in which the general defence system works', 'viruses.'),
      [anyn(S('Skin acts as a barrier', 'other correct answer'), 2, 3, note_sel=S('General:', 'General:')),
       anyn(S('(B cells) produce antibodies', 'other correct answer'), 2, 3, note_sel=S('Specific:', 'Specific:'))],
      'bio-2-4', 'defending-against-viruses', SQ(28, 'Give two ways in which the general defence system'), 12,
      stem=[Q16C, Q16CV]),
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'Suggest one way in which you could distinguish between edible and poisonous', 'mushrooms.'),
      [pt(S('Using a key or other correct method'), 3)], 'bio-3-2', 'identifying-mushrooms',
      SQ(29, 'Suggest one way in which you could distinguish'), 3, stem=[Q16D], fig='q16-mushrooms',
      id='bio-2023-hl-q16-d-i-iii',
      decision='The old card bundled (d)(i)-(iii); it keeps its id for (i), and (ii), (iii) are added.'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Name any one example of an edible mushroom.'),
      [pt(S('Field or Chestnut or other correct'), 3)], 'bio-3-2', 'edible-mushrooms',
      SQ(29, 'Name any one example of an edible mushroom.'), 3, stem=[Q16D], fig='q16-mushrooms'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Name any one example of a poisonous mushroom.'),
      [pt(S('Death cap or destroying angel or other correct'), 3)], 'bio-3-2', 'poisonous-mushrooms',
      SQ(29, 'Name any one example of a poisonous mushroom.'), 3, stem=[Q16D], fig='q16-mushrooms'),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Draw a diagram showing the basic structure of Rhizopus', 'stolon, rhizoid, sporangium.'),
      [pt(S('stolon and rhizoid and sporangiophore and sporangium', after='Q16 (d) (i) – (iii) Number of correct responses'), 6, kind='criterion', units=[3, 3],
          note_sel=S('(Any one missing only 3 marks)')),
       anyn(S('stolon / rhizoid / sporangium'), 3, 1)], 'bio-3-2', 'drawing-rhizopus',
      SQ(29, 'Diagram of Rhizopus'), 9, stem=[Q16DIV]),
] + [
    T(f'16dv{n}', f'Q16(d)(v){n}', 'C', [Q16DV, _C(8, f'{n}.', part, after='Give one function for each', br=True)],
      [pt(S(ans, aend), 3, label=S(label) if label else None)], 'bio-3-2', f'function-of-the-{slug}',
      SQ(29, 'Give one function for each of the following parts.'), 3, stem=[Q16DIV],
      id='bio-2023-hl-q16-d-v-vi' if n == 1 else None,
      decision=('The old card bundled (d)(v) and (vi); it keeps its id for (v)1., and (v)2., (v)3. and (vi) '
                'are added. ' if n == 1 else '') + '"For each of the following": three separately priced '
                                                   'items, one card each.')
    for n, part, ans, aend, label, slug in [
        (1, 'Stolon', 'spread (out) or growth', 'colonisation', 'Stolon:', 'stolon'),
        (2, 'Rhizoid', 'anchorage or secretion', '(of nutrients)', 'Rhizoid:', 'rhizoid'),
        (3, 'Sporangium', 'Sporangium: asexual reproduction or to produce', 'spores', None, 'sporangium')]
] + [
    T('16dvi', 'Q16(d)(vi)', 'C', _C(8, 'Name the mode of nutrition used by Rhizopus.'),
      [pt(S('Saprophytic or heterotrophic or decomposition'), 3)], 'bio-3-2', 'rhizopus-nutrition',
      SQ(29, 'Name the mode of nutrition used by Rhizopus.'), 3, stem=[Q16DIV]),
    # Q17: any two of (a)-(d), each 30.
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'Give one difference between endocrine and exocrine', 'glands.'),
      [pt(S('Endocrine glands do not have ducts', 'products into ducts'), 3)], 'bio-2-4',
      'endocrine-and-exocrine', SQ(30, 'Give one difference between endocrine and exocrine glands.'), 3,
      id='bio-2023-hl-q17-a-i-ii',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Name a gland that has both an endocrine function and an', 'exocrine product.'),
      [pt(S('Any correct gland', 'other correct)'), 3, label=S('Name:', after='Name its endocrine product')),
       pt(S('Correct matching product'), 3, kind='criterion', label=S('Endocrine product:')),
       pt(S('Correct matching product', nth=2), 3, kind='criterion', label=S('Exocrine product:'))],
      'bio-2-4', 'endocrine-and-exocrine-gland', SQ(30, 'Name a gland that has both'), 9),
    T('17aiii', 'Q17(a)(iii)', 'C', [_C(9, 'Copy the outline of the human body into your', 'answerbook.'),
                                     _C(9, 'Draw in each of the following endocrine glands', 'correct locations:'),
                                     _C(9, '1.', 'Pituitary gland', after='Draw in each of the following'),
                                     _C(9, '2.', 'Thyroid gland', after='Draw in each of the following'),
                                     _C(9, '3.', 'Adrenal glands', after='Draw in each of the following')],
      [pt(S('Pituitary gland'), 2, kind='criterion'), pt(S('Thyroid gland'), 2, kind='criterion'),
       pt(S('Adrenal glands'), 2, kind='criterion',
          note='The scheme\'s outline, each gland drawn in and labelled, is shown after reveal.')],
      'bio-2-4', 'locating-endocrine-glands', SQ(30, 'Draw in and label the location'), 6,
      qfig='q17a-iii-question', fig='q17a-iii-scheme',
      decision='One drawing of three glands on one outline: one card, a row per gland at "3(2)". The '
               'scheme answers with its own labelled outline, the solution figure.'),
    T('17aiv', 'Q17(a)(iv)', 'C', [_C(9, 'For each of the following endocrine glands, name a',
                                       'corresponding function:'),
                                   _C(9, 'thyroid;', br=True), _C(9, 'adrenals', br=True)],
      [pt(S('thyroxine'), 3, label=S('Thyroid:', 'Name of hormone:')),
       pt(S('(stimulates) metabolism'), 3, label=S('Function:', after='thyroxine')),
       pt(S('adrenaline'), 3, label=S('Adrenals: Name of hormone:')),
       pt(S('‘fight or flight’ (response) or other correct function'), 3, label=S('Function:', after='adrenaline'))],
      'bio-2-4', 'thyroid-and-adrenal-hormones', SQ(30, 'For each of the following endocrine glands'), 12),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'What term describes the region where two neurons come into close contact?'),
      [pt(S('*Synapse'), 3)], 'bio-2-4', 'synapse', SQ(31, 'What term describes the region'), 3, stem=[Q17B],
      fig='q17-synapse', id='bio-2023-hl-q17-b-i-ii',
      decision='The old card bundled (b)(i) and (ii), and (ii) also had a card of its own; it keeps its id for (i).'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'What is the name given to the gap between two neurons', 'in the diagram?'),
      [pt(S('*(Synaptic) cleft'), 3)], 'bio-2-4', 'synaptic-cleft', SQ(31, 'What is the name given to the gap'), 3,
      stem=[Q17B], fig='q17-synapse', id='bio-2023-hl-q17-b-ii-fig'),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'What is the general name given to the chemical A in the diagram?'),
      [pt(S('*Neurotransmitter'), 3)], 'bio-2-4', 'neurotransmitter', SQ(31, 'What is the general name given'), 3,
      stem=[Q17B], fig='q17-synapse', id='bio-2023-hl-q17-b-iii-fig'),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'Where in a neuron is chemical A made?'),
      [pt(S('*Cell body'), 3)], 'bio-2-4', 'where-neurotransmitter-is-made',
      SQ(31, 'Where in a neuron is chemical A made?'), 3, stem=[Q17B], fig='q17-synapse',
      id='bio-2023-hl-q17-b-iv-fig'),
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'Describe in detail how nerve impulses travel between two neurons in close',
                                   'contact.'),
      [anyn(S('Impulse arrives (at axon terminal) /', 'postsynaptic'), 3, 3)], 'bio-2-4', 'synaptic-transmission',
      SQ(31, 'Describe in detail how nerve impulses travel'), 9, stem=[Q17B], fig='q17-synapse',
      id='bio-2023-hl-q17-b-iv-v',
      decision='The old card bundled (b)(iv) and (v), and (iv) also had a card of its own; it keeps its id for (v).'),
    T('17bvi', 'Q17(b)(vi)', 'C', _C(9, 'Interneurons are one type of neuron found within the central nervous system.',
                                     'system.', end_nth=2),
      [pt(S('Sensory'), 3), pt(S('Motor'), 3)], 'bio-2-4', 'types-of-neuron',
      SQ(31, 'Give the names of the other two types of neuron'), 6, id='bio-2023-hl-q17-b-vi-vii',
      decision='The old card bundled (b)(vi) and (vii); it keeps its id for (vi), and (vii) is added.'),
    T('17bvii', 'Q17(b)(vii)', 'C', _C(9, 'Describe one possible treatment for either of the following nervous system',
                                       'Parkinson’s disease.'),
      [pt(S('Physiotherapy or surgery or other correct'), 3)], 'bio-2-4', 'treating-nervous-disorders',
      SQ(31, 'Describe one possible treatment for either paralysis'), 3,
      decision='Paralysis or Parkinson\'s disease: the scheme marks both on one row, so the choice is one card.'),
] + [
    T(f'17ci{n}', f'Q17(c)(i){n}', 'C', [Q17CI, _C(10, f'{n}.', desc, after='In each of the following', br=True)],
      [pt(S(ans), 3)], 'bio-2-6', concept, SQ(32, 'In each of the following, name the vein'), 3, stem=[Q17C],
      id='bio-2023-hl-q17-c-i' if n == 1 else None,
      decision=('The old card bundled items 1-4; it keeps its id for 1., and 2.-4. are added. ' if n == 1 else '')
      + '"In each of the following": four separately priced items, one card each.')
    for n, desc, ans, concept in [
        (1, 'Carries blood richest in oxygen.', '*Pulmonary (vein)', 'pulmonary-vein'),
        (2, 'Carries blood between the intestine and the liver.', '*Hepatic portal (vein)', 'hepatic-portal-vein'),
        (3, 'Carries blood lowest in metabolic wastes.', '*Renal (vein)', 'renal-vein'),
        (4, 'Carries blood into the right atrium of the heart.', '*Vena cava', 'vena-cava')]
] + [
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'In your answerbook, sketch the structure of an alveolus', 'carbon dioxide are moving.'),
      [pt(S('Sketch: Alveolus and capillary'), 3, kind='criterion'),
       pt(S('Oxygen from alveolus to blood.'), 3), pt(S('Carbon dioxide from blood to alveolus.'), 3)],
      'bio-2-6', 'alveolus-sketch', SQ(32, 'Sketch the structure of an alveolus'), 9, stem=[Q17C]),
    T('17ciii1', 'Q17(c)(iii)1', 'C', _C(10, 'State which diagram (X or Y)', 'represents inhalation.'),
      [pt(S('*X'), 3)], 'bio-2-6', 'inhalation', SQ(32, '1. State which diagram (X or Y)'), 3,
      stem=[Q17C, Q17CIII], fig='q17-breathing', id='bio-2023-hl-q17-c-iii-1-fig'),
    T('17ciii2', 'Q17(c)(iii)2', 'C', _C(10, 'Explain in detail how you know', 'diagram.'),
      [anyn(S('Ribs are moving outwards', 'moving downwards'), 2, 3)], 'bio-2-6',
      'signs-of-inhalation', SQ(32, '2. Explain in detail how you know'), 6,
      stem=[Q17C, Q17CIII, M('1.', 10), _C(10, 'State which diagram (X or Y)', 'represents inhalation.')],
      fig='q17-breathing', id='bio-2023-hl-q17-c-iii-2-fig'),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'Identify the plant organ.'),
      [pt(S('*Root'), 3)], 'bio-2-6', 'root', SQ(33, 'Identify the plant organ.'), 3, stem=[Q17D], fig='q17-root',
      id='bio-2023-hl-q17-d-i-fig'),
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'Name tissues A and B and the structure labelled C.'),
      [pt(S('A: Dermal'), 1), pt(S('B: Ground'), 1), pt(S('C: Root Hair'), 1)], 'bio-2-6', 'root-tissues',
      SQ(33, 'Name tissues A and B and the structure labelled C.'), 3, stem=[Q17D], fig='q17-root',
      id='bio-2023-hl-q17-d-ii-fig',
      labels=[L('A', S('Dermal', page=33, after='Name tissues A and B'), True),
              L('B', S('Ground', page=33, after='A: Dermal'), True),
              L('C', S('Root Hair', page=33, after='B: Ground'), True)]),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'Give one function for each part A, B and C.'),
      [pt(S('A: Protection'), 3), pt(S('B: Storage or support'), 3), pt(S('C: Absorption'), 3)], 'bio-2-6',
      'functions-of-root-tissues', SQ(33, 'Give one function for each part, A, B and C.'), 9, stem=[Q17D],
      fig='q17-root',
      labels=[L('A', S('Dermal', page=33, after='Name tissues A and B'), False),
              L('B', S('Ground', page=33, after='A: Dermal'), False),
              L('C', S('Root Hair', page=33, after='B: Ground'), False)]),
    T('17div', 'Q17(d)(iv)', 'C', _C(10, 'Give one function of vascular tissue in plants.'),
      [pt(S('Transport or support'), 3)], 'bio-2-6', 'vascular-tissue-function',
      SQ(33, 'Give one function of vascular tissue in plants.'), 3, id='bio-2023-hl-q17-d-iv-v',
      decision='The old card bundled (d)(iv) and (v); it keeps its id for (iv), and (v) is added.'),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Name the two types of vascular tissue present in plants.'),
      [pt(S('Xylem', after='Name the two types'), 3), pt(S('Phloem', after='Name the two types'), 3)], 'bio-2-6',
      'xylem-and-phloem', SQ(33, 'Name the two types of vascular tissue'), 6),
] + [
    T('17dvi', 'Q17(d)(vi)', 'C', _C(10, 'Draw and label a longitudinal section (L.S.) of either type', 'above.'),
      rows, 'bio-2-6', f'drawing-{route}', SQ(33, 'Draw and label a longitudinal section'), 6, route=route,
      stem=[M('(v)', 10), _C(10, 'Name the two types of vascular tissue present in plants.')],
      id='bio-2023-hl-q17-d-vi' if route == 'xylem' else None,
      decision='Xylem or phloem: the scheme marks each with its own drawing and label rows, so each is a '
               'route card.')
    for route, rows in [
        ('xylem', [pt(S('Continuous vessel (or tracheid) with either lignin or pits'), 3, kind='criterion'),
                   anyn(S('pits / lignin / wall / lumen'), 3, 1)]),
        ('phloem', [pt(S('Tube with sieve plates and companion cell'), 3, kind='criterion'),
                    anyn(S('sieve plate / sieve tube / companion cell / cytoplasm'), 3, 1)])]
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2-graph': ('038', 4, (150, 128, 480, 320), SEC, [],
                 'Graph of Percentage (%) germination of grass seeds against Soil pH, from 0 to 10: a smooth hump '
                 'rising from about pH 2, peaking at about pH 6.5 and falling again towards pH 10.', False),
    'q3-skeleton': ('038', 5, (355, 98, 541, 522), SEC, ['X'],
                    'Front-view drawing of the human skeleton, with a boxed letter X beside it at the upper right.',
                    False),
    'q4-dna': ('038', 6, (150, 78, 445, 318), SEC, ['T', 'G', 'X'],
               'Diagram of part of a DNA molecule: two backbones of circles and five-sided rings, one along the top '
               'and one along the bottom. Two bases hang from the lower backbone, labelled T and G, with dashed '
               'lines above them where their partners would join; an arrow labelled X points to the dashed lines '
               'above T.', False),
    'q5-bacterium': ('038', 7, (300, 78, 541, 226), SEC, ['X'],
                     'Transmission electron micrograph of a long, rounded bacterial cell pinching in two, with '
                     'parts of other cells around it, and a boxed letter X at the top left.', False),
    'q5-curve': ('038', 7, (205, 472, 480, 672), SEC, ['Z'],
                 'Partly drawn graph of Population against Time: the axes are drawn, and only the later part of '
                 'the curve, a flat top that bends down into a steep fall, with an arrow labelled Z pointing to '
                 'the falling section.', False),
    'q7-graph': ('038', 9, (160, 105, 465, 302), SEC, [],
                 'Graph of Absorption of light against Colour of light (violet, blue, green, yellow, orange, red), '
                 'with a dotted line for chlorophyll a and a solid line for chlorophyll b. Both are high at the '
                 'violet and blue end, the solid line peaking a little further into the blue; both are low '
                 'through green and yellow; both rise again in the red, the dotted line higher.', False),
    'q8-apparatus': ('038', 10, (136, 262, 500, 395), SEC, ['A', 'B'],
                     'Two pieces of apparatus. Left: a small container closed by a bung through which two bent '
                     'tubes pass, labelled Tube A and Tube B, with a Gauze filter on the end of one tube inside. '
                     'Right: a funnel held in a clamp stand, soil in the funnel under a Light bulb, and a beaker '
                     'below.', False, [(136, 262, 300, 277)]),
    'q10b-iv-2-scheme': ('scheme', 15, (408, 555, 486, 642), SEC, [],
                         "The marking scheme's sketch: a circle with a ring of small separate bundles inside its "
                         'edge.', True),
    'q11b-iv-scheme': ('scheme', 16, (115, 462, 212, 528), SEC, [],
                       "The marking scheme's pyramid of numbers: three stacked boxes, Ash on the bottom, a wider "
                       'Moth box in the middle and Robin on top.', True),
    'q12a-ii-question': ('040', 3, (108, 74, 505, 130), SEC, [],
                         'The printed question: (ii) Is the reaction shown below an anabolic reaction or a catabolic '
                         'reaction? Explain your answer. Below it: A, an arrow, then B + C + Energy.', False),
    'q12b-i-question': ('040', 3, (80, 180, 541, 356), SEC, [],
                        'The printed question: (b) Aerobic respiration is a metabolic reaction that occurs in two '
                        'stages in living cells. (i) Copy the diagram of the cell into your answerbook and indicate '
                        'clearly the specific locations of stage 1 and stage 2. Beside it, a rounded cell: a small '
                        'sausage-shaped organelle with folded inner membranes near the top, and an arrow labelled '
                        'Nucleus pointing to the round body in the lower left.', False, [(80, 249, 360, 356)]),
    'q12b-i-scheme': ('scheme', 18, (150, 292, 330, 372), SEC, [],
                      "The marking scheme's copy of the cell: the label Stage 2 points to the sausage-shaped "
                      'organelle near the top, Stage 1 to the cytoplasm around the nucleus, and the Nucleus is '
                      'labelled.', True),
    'q12b-v-question': ('040', 3, (108, 409, 515, 489), SEC, [],
                        'The printed question: (v) ATP is produced during respiration. Copy the following word '
                        'equation into your answerbook and complete the missing parts of the equation. Below it: '
                        'ADP + a blank + Energy, an arrow, then ATP + a blank.', False),
    'q12b-v-scheme': ('scheme', 18, (110, 519, 266, 540), SEC, [],
                      "The marking scheme's equation: ADP + P + Energy, an arrow, ATP + H2O, with P and H2O "
                      'underlined and the 2 set as a subscript.', True),
    'q13b-i-question': ('040', 4, (108, 114, 541, 179), SEC, [],
                        'The printed passage and question: (b) Haemochromatosis is an inherited condition where '
                        'iron levels in the body slowly build up over many years. Classic hereditary '
                        'haemochromatosis is caused by a gene mutation whereby two recessive alleles are inherited. '
                        '(i) Explain each of the underlined terms. The words gene and recessive are underlined.',
                        False),
    'q13-pedigree': ('040', 4, (110, 415, 540, 542), SEC, [],
                     'A pedigree chart. Parents: person 1, a half-shaded circle (Heterozygous female), and person '
                     '2, an open square (Non-sufferer male). Their children, numbered 3 to 7: 3, a half-shaded '
                     'circle; 4, a shaded square (Haemophiliac male); 5, a half-shaded circle; 6, a shaded square; '
                     '7, an open circle (Non-sufferer female). A key explains the four symbols.', False),
    'q14-flower': ('040', 5, (170, 190, 460, 380), SEC, ['A', 'B', 'C'],
                   'Diagram of an animal-pollinated flower cut in half. Arrow A points to the top of the central '
                   'stalk; arrow B to a head on one of the stalks around it; arrow C to a small leaf-like part at '
                   'the base of the flower. Labels Style, Filament and Ovule point to their parts.', False),
    'q15-sperm': ('040', 6, (350, 215, 541, 290), SEC, [],
                  'Drawing of a human sperm cell: an oval head, a short ridged middle piece and a long, looping '
                  'tail.', False),
    'q15b-iii-2-question': ('040', 6, (108, 219, 541, 323), SEC, [],
                            'The printed question: (iii) The diagram shows a human sperm cell. 2. Copy out the '
                            'diagram of the human sperm cell into your answerbook and indicate on it the location of '
                            'the mitochondria. Beside it, the sperm cell: an oval head, a short ridged middle piece '
                            'and a long, looping tail.', False, [(138, 235, 350, 279)]),
    'q15b-iii-2-scheme': ('scheme', 24, (135, 598, 275, 634), SEC, [],
                          "The marking scheme's sperm cell, with the label Mitochondria pointing to the short "
                          'middle piece behind the head.', True),
    'q15-graph': ('040', 6, (150, 430, 540, 588), SEC, ['A', 'B'],
                  'Graph of Levels in the blood against Days (1, 5, 14) for two hormones: dashed line A rises from '
                  'about day 5 to a sharp peak just before day 14, falls, then rises again in a lower hump; solid '
                  'line B stays low until about day 14, then rises to a large hump and falls back by the end.',
                  False),
    'q16-graph': ('040', 7, (140, 105, 490, 268), SEC, [],
                  'Graph of Percentage (%) change in mass against Sugar concentration (g/100 cm3), from 0 to 12: '
                  'the points fall from +20 at 0, through +4 at 2, to 0 at 4, then below zero, to about -11 at 12.',
                  False),
    'q16-ribosome': ('040', 7, (355, 560, 541, 655), SEC, [],
                     'Diagram of a ribosome on a strand, labelled Ribosome, with a chain of beads labelled Protein '
                     'growing from it.', False),
    'q16-virus': ('040', 8, (370, 58, 530, 188), SEC, ['X', 'Y'],
                  'Diagram of a spherical virus: arrow X points to the thick outer circle, arrow Y to the coiled '
                  'strand inside it.', False),
    'q16-mushrooms': ('040', 8, (170, 397, 425, 482), SEC, ['A', 'B'],
                      'Two photographs of mushrooms. A: stout mushrooms with broad, scaly caps on thick stalks. B: '
                      'slender, pale mushrooms with flat caps on tall stalks, each stalk with a ring.', False),
    'q17a-iii-question': ('040', 9, (108, 86, 541, 280), SEC, [],
                          'The printed question: (iii) Copy the outline of the human body into your answerbook. '
                          'Draw in each of the following endocrine glands labelling them in their correct '
                          'locations: 1. Pituitary gland 2. Thyroid gland 3. Adrenal glands. Beside it, an outline '
                          'of the human body, front view, with no organs drawn in.', False, [(108, 86, 432, 171)]),
    'q17a-iii-scheme': ('scheme', 30, (190, 392, 400, 528), SEC, [],
                        "The marking scheme's outline with the glands drawn in as small circles: Pituitary gland in "
                        'the head, Thyroid gland in the neck, and Adrenal glands, two circles side by side in the '
                        'abdomen.', True),
    'q17-synapse': ('040', 9, (180, 415, 485, 553), SEC, ['A', 'B'],
                    'Diagram of the ends of two neurons in close contact: arrow A points to small dots leaving one '
                    'neuron, and arrow B to the narrow gap between the two.', False),
    'q17-breathing': ('040', 10, (350, 205, 541, 362), SEC, ['X', 'Y'],
                      'Two diagrams of the chest, X and Y. In X, arrows show the ribs moving outwards and the '
                      'diaphragm moving down; in Y, arrows show the ribs moving inwards and the diaphragm moving up.',
                      False),
    'q17-root': ('040', 10, (170, 425, 470, 600), SEC, ['A', 'B', 'C'],
                 'Three-dimensional cutaway of part of a plant organ: arrow A points to the thin outer layer, arrow '
                 'B to the tissue filling the cylinder, and arrow C to a fine hair growing from the surface; a '
                 'label Vascular tissue points to the central core.', False),
}
