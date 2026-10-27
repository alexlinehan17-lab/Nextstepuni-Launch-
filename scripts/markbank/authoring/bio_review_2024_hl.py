"""Biology 2024 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover, p2
    instructions, p3-p9 Section A Questions 1-7, p10-p12 Section B Questions
    8-10, p13 Section C answerbook instructions, p14-p15 graph paper, p16-p39
    ruled answer pages, p40 back cover. This paper prints no acknowledgements
    page, so no figure carries a third-party credit.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "There is no examination material on this page", p12 back cover.
  * LC025ALP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7 Irish-medium
    bonus, p8-p32 Questions 1-17, p33-p34 "BLANK PAGE", p35 blank, p36 back
    cover.

The sitting was already carded (132 cards, all shipped). As for 2025, the
review re-derives every task from the PDFs at the scheme's own mark
boundaries and corrects the existing cards in place: every id is kept,
mapped (`id=`) to the task it was carding, verified or corrected with its old
fields recorded; tasks the old cards bundled or missed are added. One shipped
card, bio-2024-hl-q8-b2 ("Q8(b) [2 of 2]"), was the second half of a single
printed task cut in two; the task is one card again, and the half is
withdrawn with a progress alias to bio-2024-hl-q8-b1, which carries it.

Tariffs as the scheme prints them: Q1 best five of six at 4; Q2, Q4, Q5 and
Q7 one ladder each, 6(3) + 2 (seven responses carded at 3); Q3 prices (a)
3(1) and then (b)-(f) on the ladder 5(3) + 2; Q6 10(2). The Q5 ticks are
Wingdings 2 check marks read from their positions; row (f)'s True box
carries two overlapping marks, and its row clip takes the first.

No closed choose-one pool here prints different marking per option, so none
is split into routes ("choice is not a route"): Q10(b) "either starch agar or
skimmed milk plates" and Q16(b)(iii)3 "either its deficiency or excess" are
one card each, the scheme's own alternatives on the row. Q16(b)(ii) asks for
a hormone and function for EACH of glands X, Y and Z: three items, every one
answered, carded per gland because six rows would pass a card's five.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2024, 'hl'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = '913bc5e57'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2024-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': '9213c5666f1816378111bb526ed7c27294a6336e70869830a918835d9ea99937',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2024-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': '876631d384f0a5b73573df1c4e628ba43504a744eb133c714cab54a0cf7708c0',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2024-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '1ffe460a25c6636ca1a1e62ec9d7dfa4d796857d68c0ad74b4d201c9b2ccbf3b',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 13)},
            13: 'answerbook-instructions', 14: 'graph-paper', 15: 'graph-paper',
            **{p: 'answer-pages' for p in range(16, 40)}, 40: 'back-cover'},
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
# Q1: "Best five answers from (a) - (f)": six parts at 4, the best five count.
BEST_OF = {1: (5, 4)}
# "6(3) + 2": seven responses, six at 3 and the seventh at 2. Q3 prices its
# (a) "3(1)" on its own and puts (b)-(f) on "5(3) + 2".
LADDERS = {
    **{q: [3, 3, 3, 3, 3, 3, 2] for q in (2, 4, 5, 7)},
    3: {'steps': [3, 3, 3, 3, 3, 2], 'fixed': {1: 3}},
}

# The examiner tick summary under each scheme block, as {mark value: count}.
CHECKSUMS = {
    1: {4: 6},   # printed "5": the best five of the six 4-mark parts carded here
    2: {3: 7}, 3: {1: 3, 3: 6}, 4: {3: 7}, 5: {3: 7}, 6: {2: 10}, 7: {3: 7},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in range(11, 16)},
    (11, 'b'): {1: 3, 3: 8}, (11, 'c'): {3: 8},
    (12, 'b'): {2: 5, 3: 3, 4: 2}, (12, 'c'): {3: 6, 2: 3},
    (13, 'b'): {3: 9}, (13, 'c'): {3: 8},
    (14, 'b'): {1: 3, 3: 8}, (14, 'c'): {3: 8},
    (15, 'b'): {3: 9}, (15, 'c'): {3: 8},
    (16, 'a'): {1: 6, 4: 6}, (16, 'b'): {2: 12, 3: 2}, (16, 'c'): {3: 10}, (16, 'd'): {3: 10},
    (17, 'a'): {4: 3, 3: 4, 2: 3}, (17, 'b'): {1: 3, 3: 9}, (17, 'c'): {1: 6, 3: 8},
    (17, 'd'): {3: 10},
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
    ('038', 4, 'the following', 'Q2 lead-in: every part asked.'),
    ('038', 4, 'any one', 'Q2(d) "any one limitation": open single answer; one card.'),
    ('038', 6, 'any one', 'Q4(a) "Label any one structure": open single answer; one card.'),
    ('038', 6, 'or', 'Q4(e)(i) "monocot ... or dicot": the answer options.'),
    ('038', 7, 'the following', 'Q5 lead-in: every statement asked.'),
    ('038', 7, 'or', 'Q5 "true or false": the answer options.'),
    ('038', 8, 'the following', 'Q6 lead-in: every pair asked.'),
    ('038', 9, 'the following', 'Q7(c) "for each of the following": every item asked, one card each.'),
    ('038', 10, 'any two', 'Section B rubric repeated.'),
    ('038', 10, 'or', 'Q8(b) "a named plant or named plant tissue": one description; one card.'),
    ('038', 11, 'the following', 'Q9(a) lead-in: both parts asked.'),
    ('038', 11, 'or', 'Q9(b)(i) "enzyme or cell": one answer.'),
    ('038', 11, 'or', 'Q9(b)(ii) "enzyme or cell": one procedure.'),
    ('038', 11, 'or', 'Q9(b)(iii) "enzyme or cell": one description.'),
    ('038', 12, 'either', 'Q10(b) "either starch agar or skimmed milk plates": the scheme marks both '
                          'on the same rows ("Iodine or Biuret test", "Must match test"); one card.'),
    ('038', 12, 'or', 'Q10(b), same choice.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'or', 'Q11(b)(ii) "(visible or otherwise)": description.'),
    ('040', 2, 'both', 'Q11(b)(v) "both of these fertilisations": both required; one card.'),
    ('040', 2, 'either', 'Q11(c) "either one or two cotyledons": description.'),
    ('040', 2, 'or', 'Q11(c), same description.'),
    ('040', 2, 'or', 'Q11(c) "monocotyledonous (monocot) or dicotyledonous (dicot)": description.'),
    ('040', 2, 'any two', 'Q11(c)(iii)1 "any two methods": bounded menu; one card.'),
    ('040', 3, 'the following', 'Q12(a): every term asked; one card.'),
    ('040', 3, 'the following', 'Q12(c)(i) "each of the following": every item asked, one card each.'),
    ('040', 5, 'the following', 'Q14(b) lead-in: every part asked.'),
    ('040', 5, 'any three', 'Q14(b)(i) "label any three parts": bounded menu; one card.'),
    ('040', 5, 'or', 'Q14(b)(ii) "prokaryotic or eukaryotic": the answer options.'),
    ('040', 6, 'both', 'Q15(b)(ii) "both plants": both required; one card.'),
    ('040', 6, 'or', 'Q15(b)(iii) "a Punnett square, or otherwise": method, not a choice of task.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'any two', 'Q16(a)(v) "any two methods": bounded menu; one card.'),
    ('040', 7, 'or', 'Q16(b)(iii) "(male or female) hormone": open choice of hormone; one card per item.'),
    ('040', 7, 'either', 'Q16(b)(iii)3 "either its deficiency or excess": one scheme row covers both; one card.'),
    ('040', 7, 'or', 'Q16(b)(iii)3, same choice.'),
    ('040', 7, 'any one', 'Q16(b)(iv) "any one human hormone": open single answer; one card.'),
    ('040', 8, 'any one', 'Q16(c)(v) "any one plant growth response": open; one card.'),
    ('040', 8, 'any two', 'Q16(c)(vii) "any two methods": bounded menu; one card.'),
    ('040', 8, 'the following', 'Q16(d) lead-in: every part asked.'),
    ('040', 8, 'any two', 'Q16(d)(i)1 "any two methods": bounded menu; one card.'),
    ('040', 8, 'any one', 'Q16(d)(i)2 "any one organ": open single answer; one card.'),
    ('040', 8, 'any two', 'Q16(d)(ii)3 "any two types": bounded menu; one card.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'or', 'Q17(a)(ii) "(A or B)": the answer options.'),
    ('040', 9, 'the following', 'Q17(b)(iii) lead-in: both items asked.'),
    ('040', 9, 'any two', 'Q17(b)(iv) "any two examples": bounded menu; one card.'),
    ('040', 10, 'the following', 'Q17(c) lead-in: every part asked.'),
    ('040', 10, 'any two', 'Q17(c)(iv)1 "any two parts": bounded menu; one card.'),
    ('040', 10, 'any two', 'Q17(c)(iv)2 "any two other substances": bounded menu; one card.'),
    ('040', 10, 'any two', 'Q17(d)(ii) "any two cell activities": bounded menu; one card.'),
]

ROUTES = {}

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2024-hl-q8-b2': 'The second half of Q8(b), one printed task the old cards cut in two '
                         '("[1 of 2]", "[2 of 2]"). Withdrawn with a progress alias to '
                         'bio-2024-hl-q8-b1, which now carries the whole task.',
}
WITHDRAW = {'bio-2024-hl-q8-b2': ('bio-2024-hl-q8-b1', RETAINED['bio-2024-hl-q8-b2'])}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


Q1 = _A(3, 'Answer any five of the following parts (a) to (f):')
Q2 = _A(4, 'Answer the following questions based on your knowledge of the scientific method.')
Q3 = _A(5, 'The diagram shows the human alimentary canal.')
Q4 = _A(6, 'The diagram shows a longitudinal view of xylem vessels and phloem in plants.')
Q4E = _A(6, 'The image shows how the tissue containing xylem and', 'transverse section (TS) of a stem.')
Q5 = _A(7, 'Indicate whether the following statements are true or false', 'appropriate box in each case.')
Q6 = _A(8, 'Distinguish clearly between each member of the following pairs of terms.')
Q7 = _A(9, 'Isolation of DNA is the first stage of genetic engineering.', 'in the diagram.')
Q7C = _A(9, 'Give one application of genetic engineering for each of the following:')
Q9A = _A(11, 'Answer the following in relation to enzymes and enzyme immobilisation.')
Q9B = _A(11, 'During your practical studies, you prepared one enzyme immobilisation', 'its application.')
Q10B = _A(12, 'During your practical studies you investigated the action', 'skimmed milk plates.')
Q11B = _C(2, 'The diagram shows a wind-pollinated flower.')
Q11C = _C(2, 'Seeds can have either one or two cotyledons', 'dicotyledonous (dicot).')
Q11CIII = _C(2, 'Fruit formation often follows seed formation.', 'then occurs.')
Q12B = _C(3, 'The graph shows the fluctuating numbers of prey', 'over time in a habitat.')
Q12BI = _C(3, 'Copy the graph into your answerbook.', 'same time period.')
Q12C = _C(3, 'The diagram below shows a food web from a marine ecosystem.', 'questions that follow.')
Q12CI = _C(3, 'Give one example of each of the following from the food web shown above:')
Q12CIII = _C(3, 'Write out a complete food chain from this food web.')
Q13A = _C(4, 'Photosynthesis and respiration are metabolic reactions.')
Q13B = _C(4, 'The image shows a transverse section (TS) through a', 'aerobic respiration.')
Q13BIII = _C(4, 'Aerobic respiration involves two stages', '(stage 1 and stage 2).')
Q13C = _C(4, 'The image shows leaf cells under the light', 'pathway 2.')
Q13CV = _C(4, 'Compounds of the general formula', 'independent stage of photosynthesis.')
Q14A = None
Q14C = _C(5, 'Viruses are shown in the image.')
Q14CIV = _C(5, 'Some viruses can be harmful and some can', 'be beneficial.')
Q15B = _C(6, 'In snapdragon plants, the allele for tallness', 'The two genes are not linked.')
Q15BII = _C(6, 'A homozygous tall, red snapdragon plant is crossed', 'snapdragon plant.')
Q15C = _C(6, 'Two famous biologists independently developed', 'selection.')
Q16A = _C(7, 'The diagram shows the human male reproductive system.', 'Answer the questions that follow.')
Q16B = _C(7, 'The diagram shows an outline of the human', 'by the letters X, Y and Z.')
Q16BIII = _C(7, 'For any named human (male or female)', 'hormone, give:')
Q16C = _C(8, 'The photograph shows a plant growing', 'towards light.')
Q16D = _C(8, 'Answer the following questions in relation to the human defence system.')
Q16DI = _C(8, 'The human defence system can be categorised', 'specific defence system (immune system).')
Q16DII = _C(8, 'The organs of the immune system have lymphocytes', 'antibody response.')
Q17A = _C(9, 'The graph below shows how the rate of activity of two human digestive', 'changes with pH.')
Q17B = _C(9, 'Fungi can be classified into saprophytic and parasitic forms.')
Q17BIII = _C(9, 'Answer the following in relation to the life cycle of Rhizopus:')
Q17C = _C(10, 'Answer the following questions in relation to the kidneys and urine formation.')
Q17CIV = _C(10, 'Large amounts of water are reabsorbed into the blood during urine formation.')
Q17D = _C(10, 'The image shows a stage of mitosis in an onion cell.', 'Mitosis is a stage of the cell cycle.')


def tick(clip, answer):
    return G('tick-col', page=10, clip=clip, headers=['True', 'False'], expect=answer, marks=3)


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Which three chemical elements are present in all lipids?'),
      [pt(S('Carbon, hydrogen, oxygen (or C, H, O)'), 4, kind='allOf')], 'bio-1-2', 'lipid-elements',
      SQ(8, 'Which three chemical elements'), 4, stem=[Q1],
      decision='One 4-mark line naming all three elements: one all-of row.'),
    T('1b', 'Q1(b)', 'A', _A(3, 'How do fats and oils differ at room temperature?'),
      [pt(S('Fats are solid and oils are liquid'), 4)], 'bio-1-2', 'fats-vs-oils-room-temperature',
      SQ(8, 'How do fats and oils differ'), 4, stem=[Q1]),
    T('1c', 'Q1(c)', 'A', _A(3, 'Give one way phospholipids differ from triglycerides.'),
      [pt(S('Phospholipids have phosphate and triglyceride do not or', 'have three fatty acids'), 4)],
      'bio-1-2', 'phospholipid-vs-triglyceride', SQ(8, 'Give one way phospholipids differ'), 4, stem=[Q1]),
    T('1d', 'Q1(d)', 'A', _A(3, 'Give one metabolic role of lipids in cells.'),
      [pt(S('Energy (storage) or hormone production or other correct'), 4)], 'bio-1-2',
      'lipid-metabolic-role', SQ(8, 'Give one metabolic role'), 4, stem=[Q1]),
    T('1e', 'Q1(e)', 'A', _A(3, 'Give one structural role of lipids in cells.'),
      [pt(S('(Cell) membrane'), 4)], 'bio-1-2', 'lipid-structural-role', SQ(8, 'Give one structural role'), 4,
      stem=[Q1]),
    T('1f', 'Q1(f)', 'A', _A(3, 'Name one fat-soluble vitamin.'),
      [pt(S('A or D or E or K'), 4)], 'bio-1-2', 'fat-soluble-vitamins',
      SQ(8, 'Name one fat-soluble vitamin.'), 4, stem=[Q1]),
    T('2a', 'Q2(a)', 'A', _A(4, 'After making an observation, a biologist often', 'What is a hypothesis?'),
      [pt(S('Proposed (or possible) explanation for an observation', 'correct description.'), 3)],
      'bio-u2', 'hypothesis-definition', SQ(8, 'What is a hypothesis?'), 3, stem=[Q2]),
    T('2b', 'Q2(b)', 'A', _A(4, 'A biologist tests their hypothesis by designing', 'good experimentation.'),
      [anyn(S('Safety / random selection', 'other correct'), 2, 3)], 'bio-u2',
      'principles-of-good-experimentation', SQ(8, 'State two principles of good experimentation.'), 6,
      stem=[Q2]),
    T('2c', 'Q2(c)', 'A', _A(4, 'Outline the steps of the scientific method that follow the design of an experiment.'),
      [anyn(S('Carry out the procedure / gathering', 'principle'), 3, 3,
            note_sel=S('Any three in a valid sequence'))], 'bio-u2', 'scientific-method-steps-after-design',
      SQ(8, 'Outline the steps of the scientific method'), 9, stem=[Q2]),
    T('2d', 'Q2(d)', 'A', _A(4, 'The scientific method also has limitations.', 'limitation of the scientific method.'),
      [pt(S('Extent of knowledge', 'accidental discovery or bias'), 3)], 'bio-u1',
      'limitations-of-scientific-method', SQ(8, 'State any one limitation'), 3, stem=[Q2]),
    T('3a', 'Q3(a)', 'A', _A(5, 'Name tube A, organ B and gland C.'),
      [pt(S('Oesophagus'), 1, label=S('Tube A:')), pt(S('Organ B: Liver'), 1),
       pt(S('Pancreas'), 1, label=S('Gland C:'))], 'bio-2-6', 'naming-the-parts-of-the-alimentary-canal',
      SQ(9, 'Name tube A, organ B and gland C.'), 3, stem=[Q3], fig='q3-canal',
      labels=[L('A', S('Oesophagus', page=9), True), L('B', S('Liver', page=9), True),
              L('C', S('Pancreas', page=9), True)],
      decision='The scheme prices (a) "3(1)" on its own, outside the ladder for (b)-(f).'),
    T('3b', 'Q3(b)', 'A', _A(5, 'Give one function of tube A.'),
      [pt(S('Transport food to the stomach'), 3)], 'bio-2-6', 'function-of-the-oesophagus',
      SQ(9, 'Give one function of tube A.'), 3, stem=[Q3], fig='q3-canal'),
    T('3c', 'Q3(c)', 'A', _A(5, 'Give one function of organ B.'),
      [pt(S('Produce bile or stores vitamins', 'or other correct'), 3)], 'bio-2-6', 'function-of-the-liver',
      SQ(9, 'Give one function of organ B.'), 3, stem=[Q3], fig='q3-canal'),
    T('3d', 'Q3(d)', 'A', _A(5, 'Give one function of gland C in relation to the', 'digestive system.'),
      [pt(S('Produces pancreatic juice or correctly named substance or named enzyme'), 3)], 'bio-2-6',
      'function-of-the-pancreas-in-digestion', SQ(9, 'Give one function of gland C'), 3, stem=[Q3],
      fig='q3-canal'),
    T('3e', 'Q3(e)', 'A', _A(5, 'State one structural feature of the small intestine', 'function.'),
      [pt(S('Long or has villi', 'or other correct'), 3)], 'bio-2-6', 'small-intestine-structural-feature',
      SQ(9, 'State one structural feature of the small intestine'), 3),
    T('3f', 'Q3(f)', 'A', _A(5, 'Symbiotic bacteria are present in the alimentary canal.', 'symbiotic bacteria.'),
      [anyn(S('Vitamin (B and K) production', 'correct'), 2, 3)], 'bio-2-6',
      'symbiotic-bacteria-alimentary-canal', SQ(9, 'Give two functions of these symbiotic bacteria'), 6),
    T('4a', 'Q4(a)', 'A', _A(6, 'Label any one structure on the diagram below', 'to the named structure.'),
      [pt(S('Correct label and correct arrow indicating structure'), 3, kind='criterion')], 'bio-2-6',
      'labelling-xylem-and-phloem', SQ(9, 'Label any one structure on the diagram'), 3, stem=[Q4],
      fig='q4-vessels'),
    T('4b', 'Q4(b)', 'A', _A(6, 'To which type of plant tissue do xylem and phloem belong?'),
      [pt(S('Vascular'), 3)], 'bio-2-6', 'xylem-phloem-tissue-type', SQ(9, 'To which type of plant tissue'), 3),
    T('4c', 'Q4(c)', 'A', _A(6, 'Give one function of xylem.'),
      [pt(S('Transport water (or minerals or other correct) or support'), 3)], 'bio-2-6', 'xylem-function',
      SQ(9, 'Give one function of xylem.'), 3),
    T('4d', 'Q4(d)', 'A', _A(6, 'Give one function of phloem.'),
      [pt(S('Transport food'), 3)], 'bio-2-6', 'phloem-function', SQ(9, 'Give one function of phloem.'), 3),
    T('4ei', 'Q4(e)(i)', 'A', _A(6, 'Is this stem a monocotyledonous (monocot) stem or a', 'dicotyledonous (dicot) stem?'),
      [pt(S('Monocot'), 3)], 'bio-2-6', 'monocot-vs-dicot-stem', SQ(9, 'Is this stem a monocotyledonous'), 3,
      stem=[Q4E], fig='q4-stem', id='bio-2024-hl-q4-e-fig',
      decision='The old card bundled (e)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('4eii', 'Q4(e)(ii)', 'A', _A(6, 'Justify your answer above.'),
      [pt(S('(Vascular) bundles are scattered'), 3)], 'bio-2-6', 'monocot-stem-evidence',
      SQ(9, 'Justify your answer above.'), 3,
      stem=[Q4E, M('(i)', 6), _A(6, 'Is this stem a monocotyledonous (monocot) stem or a', 'dicotyledonous (dicot) stem?')],
      fig='q4-stem'),
    T('4f', 'Q4(f)', 'A', _A(6, 'State the location of the tissue containing xylem and phloem', 'a root.'),
      [pt(S('Centre or described'), 3)], 'bio-2-6', 'root-vascular-tissue-location',
      SQ(9, 'State the location of the tissue'), 3),
] + [
    T(f'5{x}', f'Q5({x})', 'A', _A(7, start), [tick(clip, answer)], topic, concept, SQ(10, start), 3,
      stem=[Q5], notes='Question 5 is marked on one ladder, 6(3) + 2.')
    for x, start, clip, answer, topic, concept in [
        ('a', 'Cell walls are only found in plant cells.', (60, 100, 560, 133), 'False', 'bio-1-3',
         'which-cells-have-cell-walls'),
        ('b', 'A turgid cell has lost a lot of water.', (60, 133, 560, 165), 'False', 'bio-2-6',
         'what-a-turgid-cell-is'),
        ('c', 'Fermentation does not use oxygen.', (60, 165, 560, 196), 'True', 'bio-2-2',
         'fermentation-is-anaerobic'),
        ('d', 'DNA is only found in the nucleus.', (60, 196, 560, 227), 'False', 'bio-1-3',
         'where-dna-is-found-in-the-cell'),
        ('e', 'There are no hydrogen bonds in a molecule of DNA.', (60, 227, 560, 259), 'False', 'bio-1-2',
         'hydrogen-bonds-in-dna'),
        ('f', 'Adenine and guanine are purine bases.', (60, 259, 560, 278), 'True', 'bio-1-2',
         'which-bases-are-purines'),
        ('g', 'Chromosomes are composed of DNA and protein.', (60, 290, 560, 322), 'True', 'bio-1-2',
         'what-chromosomes-are-made-of')]
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(8, pair), rows, topic, concept, SQ(10, sq), 4, stem=[Q6])
    for x, pair, sq, rows, topic, concept in [
        ('a', 'Ectotherm and endotherm', 'Ectotherm:',
         [pt(S('Animal whose (body) temperature varies'), 2, label=S('Ectotherm:', after='Distinguish clearly')),
          pt(S('Endotherm: Animal with a constant'), 2)], 'bio-2-4', 'ectotherm-vs-endotherm'),
        ('b', 'Ligament and tendon', 'Ligament:',
         [pt(S('Attaches (joins) bone to bone'), 2, label=S('Ligament:', after='Endotherm:')),
          pt(S('Attaches (joins) muscle to bone'), 2, label=S('Tendon:'))], 'bio-2-4', 'ligament-vs-tendon'),
        ('c', 'Carpal and carpel', 'Carpal:',
         [pt(S('Bone in the wrist'), 2, label=S('Carpal:', after='Attaches (joins) muscle')),
          pt(S('Female part of the flower'), 2, label=S('Carpel:'))], 'bio-2-4', 'carpal-vs-carpel'),
        ('d', 'Haploid and diploid', 'Haploid:',
         [pt(S('One set of chromosomes or one copy of each chromosome'), 2,
             label=S('Haploid:', after='Female part')),
          pt(S('Two sets of chromosomes or two copies of each chromosome'), 2, label=S('Diploid:'))],
         'bio-2-3', 'haploid-vs-diploid'),
        ('e', 'Systole and diastole', 'Systole:',
         [pt(S('Heart muscle is contracting'), 2, label=S('Systole:', after='Two sets of chromosomes')),
          pt(S('Heart muscle is relaxing'), 2, label=S('Diastole:'))], 'bio-2-6', 'systole-vs-diastole')]
] + [
    T('7a', 'Q7(a)', 'A', _A(9, 'Explain the term genetic engineering.'),
      [pt(S('(Artificial) manipulation (or alteration) of a gene (or of DNA)'), 3)], 'bio-3-3',
      'genetic-engineering-definition', SQ(11, 'Explain the term genetic engineering.'), 3),
    T('7b', 'Q7(b)', 'A', _A(9, 'Name each stage X, Y and Z.'),
      [pt(S('Cutting (accept restriction)'), 3, label=S('Stage X:')),
       pt(S('Transformation or introduction of base sequence changes'), 3, label=S('Stage Y:')),
       pt(S('Expression'), 3, label=S('Stage Z:'))], 'bio-3-3', 'naming-the-stages-of-genetic-engineering',
      SQ(11, 'Name each stage X, Y and Z.'), 9, stem=[Q7], fig='q7-stages',
      labels=[L('X', S('Cutting (accept restriction)', page=11), True),
              L('Y', S('Transformation or introduction', page=11), True),
              L('Z', S('Expression', page=11), True)]),
] + [
    T(f'7c{r}', f'Q7(c)({r})', 'A', [Q7C, _A(9, item, br=True, after='Give one application of genetic')],
      [pt(S('Any correct application given', after=after, nth=nth), 3, kind='criterion')], 'bio-3-3',
      f'genetic-engineering-application-{slug}', SQ(11, 'Give one application of genetic engineering'), 3,
      decision='"For each of the following": three separately priced items, one card each.')
    for r, item, after, nth, slug in [('i', 'Plant', 'Plant:', 1, 'plant'),
                                      ('ii', 'Animal', '(ii) Animal:', 1, 'animal'),
                                      ('iii', 'Micro-organism', '(ii) Animal:', 2, 'micro-organism')]
] + [
    # ------------------------------------------------------------ Section B --
    T('8a', 'Q8(a)', 'B', _A(10, 'Distinguish between the terms coding DNA and non-coding DNA.'),
      [pt(S('Has genetic instructions to produce a protein'), 3, label=S('Coding DNA:')),
       pt(S('Non-coding DNA: Has genetic'), 3)], 'bio-1-4', 'coding-vs-non-coding-dna',
      SQ(12, 'Distinguish between the terms coding DNA'), 6),
    T('8b', 'Q8(b)', 'B', _A(10, 'As part of your practical studies you isolated DNA from plant tissue.',
                             'labelled diagram if you wish.'),
      [pt(S('Correctly named plant or plant tissue'), 3, kind='criterion', label=S('Named plant or tissue:')),
       anyn(S('Relevant piece of apparatus named or any correct reference', 'and ethanol)'), 7, 3,
            note_sel=S('Points may be obtained'))],
      'bio-1-2', 'dna-isolation-from-plant-tissue', SQ(12, 'Describe how you isolated the DNA'), 24,
      id='bio-2024-hl-q8-b1',
      decision='One printed task: the named plant and seven separately priced procedure points '
               '("7(3)", no printed boundary between them), one all-of-seven group. The old cards '
               'cut it in two and left out the named plant and the apparatus point; [1 of 2] keeps '
               'its id for the task, and [2 of 2] is withdrawn with an alias to it.'),
    T('9ai', 'Q9(a)(i)', 'B', _A(11, 'Briefly explain the term enzyme.'),
      [pt(S('Biological (or organic or protein) catalyst'), 3)], 'bio-2-1', 'enzyme-definition',
      SQ(13, 'Briefly explain the term enzyme.'), 3, stem=[Q9A]),
    T('9aii', 'Q9(a)(ii)', 'B', _A(11, 'State one advantage of immobilising enzymes.'),
      [pt(S('Pure product or easily recovered or reusable'), 3)], 'bio-2-1', 'immobilised-enzyme-advantages',
      SQ(13, 'State one advantage of immobilising'), 3, stem=[Q9A]),
    T('9bi', 'Q9(b)(i)', 'B', _A(11, 'Name the enzyme or cell you immobilised.'),
      [pt(S('Correctly named enzyme or cell'), 3, kind='criterion')], 'bio-2-1', 'enzyme-or-cell-immobilised',
      SQ(13, 'Name the enzyme or cell you immobilised.'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', _A(11, 'Describe the procedure you used to immobilise', 'labelled diagram if you wish.'),
      [anyn(S('Relevant piece of apparatus named or reference to valid safety', 'or rinsed'), 4, 3,
            note_sel=S('Points may be obtained'))], 'bio-2-1', 'enzyme-immobilisation-procedure',
      SQ(13, 'Describe the procedure you used'), 12, stem=[Q9B],
      decision='Four separately priced procedure points ("4(3)"): one all-of-four group.'),
    T('9biii', 'Q9(b)(iii)', 'B', _A(11, 'Describe how you examined the application of the immobilised enzyme or cell.'),
      [anyn(S('Matching substrate /', 'Result described'), 3, 3)], 'bio-2-1', 'testing-immobilised-enzyme',
      SQ(13, 'Describe how you examined the application'), 9, stem=[Q9B]),
    T('10ai', 'Q10(a)(i)', 'B', _A(12, 'What is meant by dormancy in seeds?'),
      [pt(S('Period of low metabolic activity or period of no growth'), 3)], 'bio-2-5',
      'seed-dormancy-definition', SQ(14, 'What is meant by dormancy in seeds?'), 3),
    T('10aii', 'Q10(a)(ii)', 'B', _A(12, 'Give one advantage of seed dormancy for plants.'),
      [pt(S('Survive adverse conditions or give time for dispersal or other correct'), 3)], 'bio-2-5',
      'seed-dormancy-advantages', SQ(14, 'Give one advantage of seed dormancy'), 3),
    T('10bi', 'Q10(b)(i)', 'B', _A(12, 'Describe how you set up the apparatus for this investigation.',
                                    'labelled diagram if you wish.'),
      [anyn(S('Relevant piece of apparatus named or suitable temperature', 'suitable control described /'), 5, 3,
            note_sel=S('Points may be obtained'))], 'bio-2-5', 'setting-up-the-seed-digestion-investigation',
      SQ(14, 'Describe how you set up the apparatus'), 15, stem=[Q10B],
      decision='Five separately priced set-up points ("5(3)"): one all-of-five group.'),
    T('10bii', 'Q10(b)(ii)', 'B', _A(12, 'Explain how you knew digestion had occurred.'),
      [pt(S('Iodine or Biuret test'), 3),
       pt(S('Agar underneath seeds remained clear (showed digestion)'), 3,
          note_sel=S('Must match test', after='remained clear')),
       pt(S('Agar underneath control seeds showed positive', 'digestion)'), 3,
          note_sel=S('Must match test', after='control seeds'))],
      'bio-2-5', 'seed-digestion-investigation-results', SQ(14, 'Explain how you knew digestion'), 9,
      stem=[Q10B]),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'What is meant by the term pollination?'),
      [pt(S('Transfer of pollen from anther to stigma'), 3)], 'bio-2-5', 'pollination-definition',
      SQ(15, 'What is meant by the term pollination?'), 3),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Distinguish between self-pollination and cross-pollination', 'type of pollination.'),
      [pt(S('Self: (Pollination) within the same plant.'), 3),
       pt(S('Cross: (Pollination) between different plants.'), 3)], 'bio-2-5', 'self-vs-cross-pollination',
      SQ(15, 'Distinguish between self-pollination'), 6),
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Name the parts of the flower', 'labelled A, B and C.'),
      [pt(S('*Anther'), 1, label=S('A:')), pt(S('*Filament'), 1, label=S('B:')),
       pt(S('*Stigma'), 1, label=S('C:'))], 'bio-2-5', 'naming-the-parts-of-a-wind-pollinated-flower',
      SQ(15, 'Name the parts of the flower labelled'), 3, stem=[Q11B], fig='q11-flower',
      labels=[L('A', S('*Anther', page=15), True), L('B', S('*Filament', page=15), True),
              L('C', S('*Stigma', page=15), True)]),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Give one adaptation of this', 'that shows it is wind-pollinated.'),
      [pt(S('Large (or long) stamen', 'light pollen'), 3)], 'bio-2-5', 'adaptations-for-wind-pollination',
      SQ(15, 'Give one adaptation of this flower'), 3, stem=[Q11B], fig='q11-flower'),
    T('11biii', 'Q11(b)(iii)', 'C', _C(2, 'In which of the labelled parts is', 'pollen formed?'),
      [pt(S('*A or anther'), 3)], 'bio-2-5', 'where-pollen-is-formed',
      SQ(15, 'In which of the labelled parts is pollen formed?'), 3, stem=[Q11B], fig='q11-flower',
      labels=[L('A', S('*Anther', page=15), True), L('B', S('*Filament', page=15), False),
              L('C', S('*Stigma', page=15), False)]),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'Describe the main events of', 'pollen grain development.'),
      [anyn(S('Diploid (2n) (microspore) mother cell', 'a tube nucleus'), 4, 3)], 'bio-2-5',
      'pollen-grain-development', SQ(15, 'Describe the main events of pollen grain'), 12),
    T('11bv', 'Q11(b)(v)', 'C', _C(2, 'Two fertilisations occur during', 'both of these fertilisations.'),
      [pt(S('1st fertilisation:'), 3), pt(S('2nd fertilisation:', 'endosperm'), 3)], 'bio-2-5',
      'double-fertilisation', SQ(15, 'Describe what happens during both'), 6),
    T('11ci1', 'Q11(c)(i)1', 'C', _C(2, 'What is a cotyledon?'),
      [pt(S('A seed leaf'), 3)], 'bio-2-5', 'cotyledon-structure-function', SQ(16, 'What is a cotyledon?'), 3,
      stem=[Q11C], id='bio-2024-hl-q11-c-i',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('11ci2', 'Q11(c)(i)2', 'C', _C(2, 'Give one function of the cotyledon.'),
      [pt(S('Store food or supplies nutrients to embryo or absorbs food from endosperm'), 3)], 'bio-2-5',
      'cotyledon-function', SQ(16, 'Give one function of the cotyledon.'), 3, stem=[Q11C]),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Other parts of a seed include the testa', 'for each part.'),
      [pt(S('Protects the seed'), 3, label=S('Testa:')), pt(S('Plumule: Develops'), 3),
       pt(S('Develops into the (young) root'), 3, label=S('Radicle:'))], 'bio-2-5', 'seed-parts-functions',
      SQ(16, 'Give one function for each part.'), 9),
    T('11ciii1', 'Q11(c)(iii)1', 'C', _C(2, 'Give any two methods of fruit and seed dispersal.'),
      [anyn(S('Animal / wind / water / self'), 2, 3)], 'bio-2-5', 'fruit-and-seed-dispersal',
      SQ(16, 'Give any two methods of fruit and seed dispersal.'), 6, stem=[Q11CIII],
      id='bio-2024-hl-q11-c-iii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('11ciii2', 'Q11(c)(iii)2', 'C', _C(2, 'Give one reason why fruit and seed dispersal', 'benefit to plants.'),
      [pt(S('Allows plant to colonise new habitats', 'or other correct'), 3)], 'bio-2-5',
      'benefit-of-dispersal', SQ(16, 'Give one reason why fruit and seed dispersal'), 3, stem=[Q11CIII]),
    T('12a', 'Q12(a)', 'C', _C(3, 'Define each of the following terms: ecology; biosphere; conservation.'),
      [pt(S('The study of (interactions'), 3, label=S('Ecology:')),
       pt(S('Where life can exist on Earth'), 3, label=S('Biosphere:')),
       pt(S('Management (or preservation', 'ecosystems)'), 3, label=S('Conservation:'))],
      'bio-3-1', 'ecology-biosphere-conservation', SQ(17, 'Define each of the following terms'), 9),
    T('12bi', 'Q12(b)(i)', 'C', Q12BI,
      [pt(S('Dashed line lower peaks than prey'), 2, kind='criterion'),
       pt(S('Dashed line out of sync compared to prey.'), 2, kind='criterion')], 'bio-3-1',
      'drawing-the-predator-curve', SQ(17, 'Show how the population of the predator species varies'), 4,
      stem=[Q12B], fig='q12-graph'),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'Give a detailed explanation of the graph that', 'for the predator species.'),
      [pt(S('Increases due to food (prey) availability', 'food (prey)'), 2, label=S('Line:')),
       pt(S('Number: Lower number due to loss of energy', 'usually larger in size).'), 2),
       pt(S('Delay in increase', 'time taken to breed.'), 2, label=S('Time:'))], 'bio-3-1',
      'explaining-a-predator-prey-graph', SQ(17, 'Give a detailed explanation of the graph'), 6,
      stem=[Q12B, M('(i)', 3), Q12BI], fig='q12-graph'),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'If a disease affected the predator at time X', 'Explain your answer.'),
      [pt(S('Prey (population) increases'), 3), pt(S('Less predators or greater chance of survival'), 3)],
      'bio-3-1', 'what-happens-to-prey-if-the-predator-fails', SQ(17, 'If a disease affected the predator'), 6,
      stem=[Q12B], fig='q12-graph'),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'Give a role for predation in the overall scheme of nature.'),
      [pt(S('Population control or described'), 3)], 'bio-3-1', 'role-of-predation',
      SQ(17, 'Give a role for predation'), 3),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'Human population numbers do not follow a similar pattern', 'Suggest two reasons for this.'),
      [anyn(S('Healthcare / food supply / lack of predators / other correct'), 2, 4)], 'bio-3-1',
      'why-human-numbers-do-not-follow-the-curve', SQ(17, 'Suggest two reasons human population'), 8,
      stem=[Q12B], fig='q12-graph'),
] + [
    T(f'12ci{n}', f'Q12(c)(i){n}', 'C', [Q12CI, _C(3, f'{n}.', ask, after='Give one example of each', br=True)],
      [pt(S(answer), 3)], 'bio-3-1', concept, SQ(18, ask), 3, stem=[Q12C], fig='q12-food-web',
      decision='"Each of the following": three separately priced items, one card each.')
    for n, ask, answer, concept in [
        (1, 'A producer', 'Phytoplankton or seaweed', 'producer-in-the-food-web'),
        (2, 'A secondary consumer', 'Salmon or herring or octopus', 'secondary-consumer-in-the-food-web'),
        (3, 'A top consumer (top carnivore)', 'Peregrine falcon or orca whale', 'top-consumer-in-the-food-web')]
] + [
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'What is meant by the term producer?'),
      [pt(S('Organism that makes its own food.'), 3)], 'bio-3-1', 'producer-definition',
      SQ(18, 'What is meant by the term producer?'), 3),
    T('12ciii', 'Q12(c)(iii)', 'C', Q12CIII,
      [pt(S('Any correct food chain from the food web.'), 3, kind='criterion')], 'bio-3-1',
      'food-chain-from-the-web', SQ(18, 'Write out a complete food chain'), 3, stem=[Q12C], fig='q12-food-web'),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'How many trophic levels are in the food chain you wrote', 'above?'),
      [pt(S('5'), 3)], 'bio-3-1', 'counting-trophic-levels', SQ(18, 'How many trophic levels'), 3,
      stem=[Q12C, M('(iii)', 3), Q12CIII], fig='q12-food-web'),
    T('12cv', 'Q12(c)(v)', 'C', _C(3, 'What is meant by the term trophic?'),
      [pt(S('Feeding or nutrition'), 2)], 'bio-3-1', 'trophic-levels-energy-loss',
      SQ(18, 'What is meant by the term trophic?'), 2, id='bio-2024-hl-q12-c-v-vi',
      decision='The old card bundled (c)(v) and (vi); it keeps its id for (v), and (vi) is added.'),
    T('12cvi', 'Q12(c)(vi)', 'C', _C(3, 'Explain why food chains have a limited number of trophic levels.'),
      [pt(S('Large amount of energy is lost between'), 2)], 'bio-3-1', 'why-food-chains-are-short',
      SQ(18, 'Explain why food chains have a limited'), 2),
    T('12cvii', 'Q12(c)(vii)', 'C', _C(3, 'Name the type of diagram an ecologist may draw', 'trophic levels.'),
      [pt(S('Pyramid of numbers or ecological pyramid'), 2)], 'bio-3-1', 'naming-the-ecological-pyramid',
      SQ(18, 'Name the type of diagram'), 2),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Explain the term metabolism.'),
      [pt(S('(All) chemical reactions in a cell (or organism).'), 3)], 'bio-2-1', 'metabolism-anabolic-catabolic',
      SQ(19, 'Explain the term metabolism.'), 3, stem=[Q13A], id='bio-2024-hl-q13-a',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Distinguish between the terms anabolic and catabolic.'),
      [pt(S('building up large molecules', 'energy'), 3, label=S('Anabolic:')),
       pt(S('Catabolic: breaking down', 'releasing energy'), 3)], 'bio-2-1', 'anabolic-vs-catabolic',
      SQ(19, 'Distinguish between the terms anabolic'), 6, stem=[Q13A]),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Identify the cell organelle shown in the image.'),
      [pt(S('*Mitochondrion'), 3)], 'bio-1-3', 'mitochondrion-identification',
      SQ(19, 'Identify the cell organelle shown'), 3, stem=[Q13B], fig='q13-mitochondrion',
      id='bio-2024-hl-q13-b-i-fig'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Write out the balanced chemical equation for', 'aerobic respiration.'),
      [pt(S('First point: formulae; second point: balancing'), 6, kind='criterion', units=[3, 3], whole=True,
          note='The scheme\'s equation, with its subscripts and arrow, is shown after reveal.')],
      'bio-2-2', 'aerobic-respiration-equation', SQ(19, 'Write out the balanced chemical equation'), 6,
      fig='q13b-ii-scheme',
      decision='The scheme prints the equation with subscripts and an arrow the text layer drops; its '
               'row lifts the scheme\'s pricing line, and the equation is the scheme crop shown after '
               'reveal.'),
    T('13biii1', 'Q13(b)(iii)1', 'C', _C(4, 'What is the name given to stage 1?'),
      [pt(S('*Glycolysis'), 3)], 'bio-2-2', 'glycolysis-events', SQ(19, 'What is the name given to stage 1?'), 3,
      stem=[Q13BIII], id='bio-2024-hl-q13-b-iii-1-2',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('13biii2', 'Q13(b)(iii)2', 'C', _C(4, 'Describe the events in stage 1.'),
      [anyn(S('Glucose is broken down into (2) pyruvic acid', 'protons'), 3, 3)], 'bio-2-2', 'events-of-glycolysis',
      SQ(19, 'Describe the events in stage 1.'), 9, stem=[Q13BIII]),
    T('13biii3', 'Q13(b)(iii)3', 'C', _C(4, 'Stage 2 involves the Krebs cycle', 'NAD in stage 2.'),
      [anyn(S('Picks up electrons', 'to make water'), 2, 3)], 'bio-2-2', 'nad-role-stage-two',
      SQ(19, 'Describe the role of the energy carrier NAD'), 6, stem=[Q13BIII]),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Name these cell organelles which are', 'responsible for photosynthesis.'),
      [pt(S('*Chloroplasts'), 3)], 'bio-2-2', 'chloroplast-identification',
      SQ(20, 'Name these organelles which are responsible'), 3, stem=[Q13C], fig='q13-leaf-cells',
      id='bio-2024-hl-q13-c-i-fig'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Where do the energised electrons come from?'),
      [pt(S('*Chlorophyll'), 3)], 'bio-2-2', 'source-of-energised-electrons',
      SQ(20, 'Where do the energised electrons come from?'), 3, stem=[Q13C], fig='q13-leaf-cells'),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Briefly describe what happens to these energised electrons in pathway 1.'),
      [anyn(S('Picked up by (electron) acceptor', 'returns to chlorophyll'), 2, 3)], 'bio-2-2',
      'fate-of-the-energised-electrons-in-pathway-1', SQ(20, 'Briefly describe what happens to these'), 6,
      stem=[Q13C], fig='q13-leaf-cells'),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'What is another name for the light-independent stage?'),
      [pt(S('*Dark'), 3)], 'bio-2-2', 'light-independent-stage-name',
      SQ(20, 'What is another name for the light-independent'), 3, stem=[Q13C], fig='q13-leaf-cells'),
    T('13cv1', 'Q13(c)(v)1', 'C', _C(4, 'What name is given to the group of compounds described', 'formula?'),
      [pt(S('*Carbohydrates'), 3)], 'bio-2-2', 'carbohydrates-from-photosynthesis',
      SQ(20, 'What name is given to the group of compounds'), 3, stem=[Q13CV]),
    T('13cv2', 'Q13(c)(v)2', 'C', _C(4, 'Name the simple molecule from which a plant obtains the protons',
                                     'used to make these compounds.'),
      [pt(S('*Water (H2O)'), 3)], 'bio-2-2', 'photosynthesis-raw-materials',
      SQ(20, 'Name the simple molecule from which a plant obtains the protons'), 3, stem=[Q13CV],
      id='bio-2024-hl-q13-c-v',
      decision='The old card bundled items 2 and 3 and left out 1.; it keeps its id for 2., and 1. and '
               '3. are added.'),
    T('13cv3', 'Q13(c)(v)3', 'C', _C(4, 'Name another simple molecule from which plants obtain the carbon',
                                     'used to make these compounds.'),
      [pt(S('*Carbon dioxide (CO2)'), 3)], 'bio-2-2', 'carbon-source-of-photosynthesis',
      SQ(20, 'Name another simple molecule'), 3, stem=[Q13CV]),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'In relation to micro-organisms such as bacteria and fungi', 'distribution in nature.'),
      [pt(S('They can survive in all habitats or they are found everywhere'), 3)], 'bio-3-2',
      'microorganism-distribution', SQ(21, 'In relation to microorganisms'), 3),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Explain the terms asepsis and sterility as applied to micro-organisms.'),
      [pt(S('Absence of pathogens'), 3, label=S('Asepsis:')),
       pt(S('Absence of all (micro)organisms'), 3, label=S('Sterility:'))], 'bio-3-2', 'asepsis-and-sterility',
      SQ(21, 'Explain the terms asepsis and sterility'), 6),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Draw the structure of a bacterial cell and label any three parts.'),
      [pt(S('Diagram: Cell wall and cell membrane and DNA'), 3, kind='criterion'),
       anyn(S('Cell wall / cell membrane / cytosol', 'other correct'), 3, 1)], 'bio-1-3',
      'drawing-and-labelling-a-bacterial-cell', SQ(21, 'Draw the structure of a bacterial cell'), 6),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Are bacteria prokaryotic or eukaryotic? Justify your answer.'),
      [pt(S('*Prokaryotic'), 3),
       pt(S('(Cell) without nucleus', 'organelles (or examples)'), 3, label=S('Justify:'))], 'bio-1-3',
      'bacteria-prokaryotic-justification', SQ(21, 'Are bacteria prokaryotic or eukaryotic?'), 6),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'Bacteria reproduce asexually. Name and describe this process.'),
      [pt(S('*Binary fission'), 3, label=S('Name:')),
       anyn(S('DNA replicates / DNA moves', 'identical cells formed.'), 2, 3)], 'bio-3-2', 'binary-fission',
      SQ(21, 'Bacteria reproduce asexually. Name and describe'), 9),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Some bacteria are pathogenic. Explain the term pathogenic.'),
      [pt(S('Disease causing'), 3)], 'bio-3-2', 'pathogenic-term', SQ(21, 'Explain the term pathogenic.'), 3),
    T('14bv', 'Q14(b)(v)', 'C', _C(5, 'Antibiotics are used to treat pathogenic bacterial', 'misuse of antibiotics.'),
      [pt(S('(Antibiotic) resistance or described or other correct'), 3)], 'bio-3-2',
      'antibiotic-misuse-resistance', SQ(21, 'Give a possible effect of the misuse'), 3),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'Explain the difficulty in describing viruses as', 'living organisms.'),
      [pt(S('Non-cellular or no metabolism or other correct'), 3)], 'bio-1-1', 'viruses-as-living-organisms',
      SQ(22, 'Explain the difficulty in describing viruses'), 3, stem=[Q14C], fig='q14-viruses'),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Name the two biochemical components', 'that make up all viruses.'),
      [pt(S('Protein'), 3), pt(S('Nucleic acid (or DNA or RNA)'), 3)], 'bio-1-1', 'virus-biochemical-components',
      SQ(22, 'Name the two biochemical components'), 6),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Describe the process of viral replication.'),
      [anyn(S('(Virus) attaches or DNA', 'released.'), 3, 3)], 'bio-1-1', 'viral-replication',
      SQ(22, 'Describe the process of viral replication.'), 9),
    T('14civ1', 'Q14(c)(iv)1', 'C', _C(5, 'Give one example of a harmful virus.'),
      [pt(S('Common cold virus or coronavirus', 'other correct'), 3)], 'bio-1-1', 'viruses-harmful-and-beneficial',
      SQ(22, 'Give one example of a harmful virus.'), 3, stem=[Q14CIV], id='bio-2024-hl-q14-c-iv',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('14civ2', 'Q14(c)(iv)2', 'C', _C(5, 'Give one way in which viruses can be beneficial.'),
      [pt(S('Can be used (as a vector)', 'other valid answer'), 3)], 'bio-1-1', 'beneficial-viruses',
      SQ(22, 'Give one way in which viruses can be beneficial.'), 3, stem=[Q14CIV]),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'What is meant by the term species?'),
      [pt(S('Group of organisms that can reproduce', 'fertile offspring.'), 3)], 'bio-1-5', 'species-definition',
      SQ(23, 'What is meant by the term species?'), 3),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Give two causes of variation within a species.'),
      [anyn(S('Mutation / sexual reproduction / other correct'), 2, 3)], 'bio-1-5', 'causes-of-variation',
      SQ(23, 'Give two causes of variation'), 6),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'Explain the underlined terms.'),
      [pt(S('form of a gene'), 3, label=S('Allele:')), pt(S('Heterozygous: two different alleles'), 3)],
      'bio-1-4', 'allele-and-heterozygous', SQ(23, 'Explain the underlined terms.'), 6, stem=[Q15B],
      qfig='q15b-i-question',
      decision='The paper marks the terms to explain by underlining them, which the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'Using suitable letters, give the genotypes of both plants in the above cross.'),
      [pt(S('*TTRR'), 3), pt(S('*ttRr'), 3, note_sel=S('Allow alternative letters'))], 'bio-1-4',
      'genotypes-of-the-parent-plants', SQ(23, 'Give the genotypes of both plants'), 6, stem=[Q15B, Q15BII]),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Using a Punnett square, or otherwise, show the possible genotypes',
                                       'cross described above.'),
      [pt(S('*TtRR'), 3, label=S('Genotype:')), pt(S('*Tall and Red flowered'), 3, label=S('Phenotype:')),
       pt(S('*TtRr'), 3, label=S('Genotype:', after='Red flowered')),
       pt(S('*Tall and Pink flowered'), 3, label=S('Phenotype:', after='*TtRr'))], 'bio-1-4',
      'offspring-genotypes-and-phenotypes-of-the-cross', SQ(23, 'Show the possible genotypes and phenotypes'), 12,
      stem=[Q15B, M('(ii)', 6), Q15BII]),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'What percentage of the offspring of the cross have pink flowers?'),
      [pt(S('*50%'), 3)], 'bio-1-4', 'percentage-of-pink-offspring',
      SQ(23, 'What percentage of the offspring'), 3, stem=[Q15B, M('(ii)', 6), Q15BII]),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'Name these two famous biologists.'),
      [pt(S('*(Charles) Darwin'), 3), pt(S('*(Alfred Russell) Wallace'), 3)], 'bio-1-5',
      'who-proposed-natural-selection', SQ(24, 'Name the two famous biologists.'), 6, stem=[Q15C]),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'What is meant by the term evolution?'),
      [pt(S('Genetic (inheritable) changes in a population (or species)'), 3),
       pt(S('over a period of time or in response to a change in the environment'), 3)], 'bio-1-5',
      'evolution-definition', SQ(24, 'What is meant by the term evolution?'), 6),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Describe the main points of the theory of natural selection.'),
      [anyn(S('High reproductive rates (or overbreeding) /', 'will dominate'), 3, 3)], 'bio-1-5',
      'natural-selection-main-points', SQ(24, 'Describe the main points of the theory'), 9),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Give one piece of evidence that supports the theory of natural selection.'),
      [pt(S('Fossils or comparative anatomy', 'other correct'), 3)], 'bio-1-5', 'evidence-for-natural-selection',
      SQ(24, 'Give one source of evidence'), 3),
    # Q16: any two of (a)-(d), each 30.
    T('16ai1', 'Q16(a)(i)1', 'C', _C(7, 'Give the names of tubes A and B and the', 'name of gland C.'),
      [pt(S('*Urethra'), 1, label=S('A:')), pt(S('*Sperm duct (or vas deferens)'), 1, label=S('B:')),
       pt(S('*Prostate (gland)'), 1, label=S('C:'))], 'bio-2-5', 'male-reproductive-system-parts',
      SQ(25, 'Give the names of tubes A and B'), 3, stem=[Q16A], fig='q16-male', id='bio-2024-hl-q16-a-i-1-fig',
      labels=[L('A', S('*Urethra', page=25), True), L('B', S('*Sperm duct (or vas deferens)', page=25), True),
              L('C', S('*Prostate (gland)', page=25), True)]),
    T('16ai2', 'Q16(a)(i)2', 'C', _C(7, 'Give one function for each structure labelled', 'A, B and C.'),
      [pt(S('Release semen or release urine'), 1, label=S('A:')),
       pt(S('Carries sperm from testes to urethra (or penis)'), 1, label=S('B:')),
       pt(S('Produces seminal fluid'), 1, label=S('C:'))], 'bio-2-5', 'male-reproductive-system-functions',
      SQ(25, 'Give one function for each structure labelled'), 3, stem=[Q16A], fig='q16-male',
      id='bio-2024-hl-q16-a-i-2-fig',
      labels=[L('A', S('*Urethra', page=25), False), L('B', S('*Sperm duct (or vas deferens)', page=25), False),
              L('C', S('*Prostate (gland)', page=25), False)]),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'In which part of the male reproductive system does', 'meiosis occur?'),
      [pt(S('*Testes'), 4)], 'bio-2-5', 'site-of-meiosis-male', SQ(25, 'In which part of the male reproductive system does'), 4),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'Which part of the male reproductive system is', 'involved in copulation?'),
      [pt(S('*Penis'), 4)], 'bio-2-5', 'copulation-organ', SQ(25, 'Which part of the male reproductive system is directly'), 4),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'Give one cause of male infertility and a corrective measure.'),
      [pt(S('Low sperm count', 'other correct'), 4, label=S('Cause:')),
       pt(S('Corrective measure: IVF or other correct'), 4)], 'bio-2-5', 'male-infertility-cause-and-correction',
      SQ(25, 'Give one cause of male infertility'), 8),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'Give any two methods of contraception.'),
      [anyn(S('Mechanical / surgical / natural / chemical / named examples'), 2, 4)], 'bio-2-5',
      'contraception-methods', SQ(25, 'Give any two methods of contraception.'), 8),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'Name glands X, Y and Z.'),
      [pt(S('X: *Thyroid'), 2), pt(S('Y: *Adrenal'), 2), pt(S('Z: *Ovary'), 2)], 'bio-2-4',
      'endocrine-gland-identification', SQ(26, 'Name glands X, Y and Z.'), 6, stem=[Q16B], fig='q16-female',
      id='bio-2024-hl-q16-b-i-fig',
      labels=[L('X', S('*Thyroid', page=26), True), L('Y', S('*Adrenal', page=26), True),
              L('Z', S('*Ovary', page=26), True)]),
] + [
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Name one hormone secreted by each gland', 'hormone.'),
      [pt(S(f'Hormone: {hormone} or other correct'), 2),
       pt(S(f'Function: {function} or other correct'), 2, note_sel=S('Must match', 'Must match', after=function))],
      'bio-2-4', concept, SQ(26, 'Name one hormone secreted by each gland'), 4,
      stem=[Q16B, M('(i)', 7), _C(7, 'Name glands X, Y and Z.')], fig='q16-female', item=(slug, letter),
      id=old_id,
      decision='A hormone and its function for each of glands X, Y and Z: every gland is answered, and '
               'its six rows would pass a card\'s five, so each gland is its own card.')
    for slug, letter, hormone, function, concept, old_id in [
        ('x', 'X', 'Thyroxine', 'Controls the rate of metabolism', 'thyroid-hormone-and-function',
         'bio-2024-hl-q16-b-ii-1'),
        ('y', 'Y', 'Adrenaline', 'Fight or flight response', 'adrenal-hormone-and-function',
         'bio-2024-hl-q16-b-ii-2'),
        ('z', 'Z', 'Oestrogen', 'Secondary sexual characteristics', 'ovary-hormone-and-function',
         'bio-2024-hl-q16-b-ii-3')]
] + [
    T(f'16biii{n}', f'Q16(b)(iii){n}', 'C', _C(7, start, end, after='hormone, give:'),
      [pt(S(row), 2, kind='criterion')], 'bio-2-4', concept, SQ(26, sq), 2, stem=[Q16BIII])
    for n, start, end, sq, row, concept in [
        (1, 'a symptom of its deficiency.', None, 'a symptom of its deficiency.',
         'Deficiency symptom to match hormone named', 'hormone-deficiency-symptom'),
        (2, 'a symptom of its excess.', None, 'a symptom of its excess.', 'Excess symptom to match hormone named',
         'hormone-excess-symptom'),
        (3, 'a corrective measure for either its', 'deficiency or excess.', 'a corrective measure for either',
         'Corrective measure to match either symptom', 'correcting-a-hormone-imbalance')]
] + [
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'Briefly describe the feedback mechanism of', 'any one human hormone.'),
      [pt(S('The concentration (or secretion) of one (named) hormone'), 3),
       pt(S('Inhibits or stimulates', 'or itself'), 3)], 'bio-2-4', 'hormone-feedback-mechanism',
      SQ(26, 'Briefly describe the feedback mechanism'), 6),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'What name is given to the growth', 'response of plants to light?'),
      [pt(S('*Phototropism'), 3)], 'bio-2-4', 'phototropism-and-its-benefit',
      SQ(27, 'What name is given to the growth response of plants to light?'), 3, stem=[Q16C],
      fig='q16-phototropism', id='bio-2024-hl-q16-c-i',
      decision='The old card bundled (c)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'How does this growth response', 'benefit plants?'),
      [pt(S('Get more light or more photosynthesis', 'or described'), 3)], 'bio-2-4', 'benefit-of-phototropism',
      SQ(27, 'How does this growth response benefit plants?'), 3,
      stem=[Q16C, M('(i)', 8), _C(8, 'What name is given to the growth', 'response of plants to light?')],
      fig='q16-phototropism'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Name any other type of growth', 'response in plants.'),
      [pt(S('Geotropism or thigmotropism or chemotropism or hydrotropism'), 3)], 'bio-2-4', 'other-plant-tropisms',
      SQ(27, 'Name any other type of growth response'), 3,
      stem=[Q16C, M('(i)', 8), _C(8, 'What name is given to the growth', 'response of plants to light?')],
      fig='q16-phototropism'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Growth regulators are important in', 'Explain the term growth regulator.'),
      [pt(S('Chemical that controls (or influences) growth (in plants)'), 3)], 'bio-2-4', 'growth-regulator-term',
      SQ(27, 'Explain the term growth regulator.'), 3),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Describe the mechanism of any one plant growth response', 'stimulus.'),
      [anyn(S('Where regulator produced /', 'Result on growth'), 3, 3)], 'bio-2-4', 'plant-tropism-mechanism',
      SQ(27, 'Describe the mechanism of any one plant growth'), 9, id='bio-2024-hl-q16-c-v-fig'),
    T('16cvi', 'Q16(c)(vi)', 'C', _C(8, 'Give one example of the use of plant growth regulators, e.g. by horticulturists.'),
      [pt(S('Seedless fruits or rooting powder', 'or other correct'), 3)], 'bio-2-4',
      'uses-of-plant-growth-regulators', SQ(27, 'Give one example of the use of plant growth regulators'), 3),
    T('16cvii', 'Q16(c)(vii)', 'C', _C(8, 'Plants have adaptations that help in protection.', 'to protect themselves.'),
      [anyn(S('Bark / cuticle / guard cells / thorns / chemicals / other correct'), 2, 3)], 'bio-2-4',
      'plant-protection-methods', SQ(27, 'Give any two methods plants use to protect'), 6),
    T('16di1', 'Q16(d)(i)1', 'C', _C(8, 'Name any two methods used by the general defence system.'),
      [anyn(S('Barrier (e.g. skin) / phagocytosis', 'other correct'), 2, 3)], 'bio-2-4',
      'general-defence-and-immune-organs', SQ(28, 'Name any two methods used by the general defence'), 6,
      stem=[Q16D, Q16DI], id='bio-2024-hl-q16-d-i',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('16di2', 'Q16(d)(i)2', 'C', _C(8, 'Name any one organ that is specific to the immune system.'),
      [pt(S('Spleen or thymus or lymph node or tonsils or other correct'), 3)], 'bio-2-4', 'immune-organs',
      SQ(28, 'Name any one organ that is specific'), 3, stem=[Q16D, Q16DI]),
    T('16dii1', 'Q16(d)(ii)1', 'C', _C(8, 'Distinguish between the terms antigen and antibody', 'on each term.'),
      [pt(S('chemical (or molecule) that stimulates'), 3, label=S('Antigen:')),
       pt(S('Antibody: protein produced in response', 'inactivates an antigen'), 3)], 'bio-2-4',
      'antigen-vs-antibody', SQ(28, 'Distinguish between the terms antigen and antibody.'), 6,
      stem=[Q16D, Q16DII]),
    T('16dii2', 'Q16(d)(ii)2', 'C', _C(8, 'T cells are one type of lymphocyte', 'Name the other type of lymphocyte.'),
      [pt(S('*B'), 3)], 'bio-2-4', 'lymphocyte-types', SQ(28, 'Name the other type of lymphocyte.'), 3,
      stem=[Q16D, Q16DII],
      decision='The old card bundled items 2 and 3; it keeps its id for 2., and 3. is added.'),
    T('16dii3', 'Q16(d)(ii)3', 'C', _C(8, 'There are four types of T cells', 'function for each named type.'),
      [anyn(S('Suppressor (or regulatory) / helper / killer (cytotoxic) / memory'), 2, 3),
       pt(S('Matching functions'), 6, kind='criterion', units=[3, 3])], 'bio-2-4', 't-cell-types',
      SQ(28, 'Name any two types (of T cell)'), 12, stem=[Q16D, Q16DII]),
    # Q17: any two of (a)-(d), each 30.
    T('17ai1', 'Q17(a)(i)1', 'C', _C(9, 'What is the optimal pH of enzyme A?'),
      [pt(S('*2'), 4)], 'bio-2-1', 'optimal-ph-of-a-stomach-enzyme', SQ(29, 'What is the optimal pH of enzyme A?'), 4,
      stem=[Q17A], fig='q17-graph', id='bio-2024-hl-q17-a-i',
      decision='The old card carded item 1 only; it keeps its id for 1., and 2. is added.'),
    T('17ai2', 'Q17(a)(i)2', 'C', _C(9, 'What is the optimal pH of enzyme B?'),
      [pt(S('*7'), 4)], 'bio-2-1', 'optimal-ph-of-enzyme-b', SQ(29, 'What is the optimal pH of enzyme B?'), 4,
      stem=[Q17A], fig='q17-graph'),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Which of these enzymes (A or B) is most likely', 'Justify your answer.'),
      [pt(S('Enzyme: *A'), 4), pt(S('pH in the stomach is low'), 3, label=S('Justify:'))], 'bio-2-1',
      'which-enzyme-works-in-the-stomach', SQ(29, 'Which enzyme (A or B) is most likely'), 7, stem=[Q17A],
      fig='q17-graph'),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'Describe the active site theory of enzyme action', 'specificity.'),
      [anyn(S('Active site has a complementary shape', 'enzyme can be reused'), 3, 3)], 'bio-2-1',
      'active-site-theory', SQ(29, 'Describe the active site theory'), 9),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Amylase, lipase and protease are three enzymes', 'product(s) of each enzyme.'),
      [pt(S('*Maltose'), 2, label=S('Amylase:')), pt(S('*Glycerol and fatty acids'), 2, label=S('Lipase:')),
       pt(S('Protease: *Amino acids or peptides'), 2)], 'bio-2-1', 'digestive-enzyme-products',
      SQ(29, 'Give the product(s) of each enzyme.'), 6),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'Explain the terms saprophytic and parasitic.'),
      [pt(S('(organism that) feeds on dead organic matter'), 3, label=S('Saprophytic:')),
       pt(S('(organism that) feeds on another living organism causing it harm'), 3, label=S('Parasitic:'))],
      'bio-3-2', 'saprophytic-and-parasitic', SQ(30, 'Explain the terms saprophytic and parasitic.'), 6,
      stem=[Q17B]),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Rhizopus is an example of a fungus.', 'involved in asexual reproduction.'),
      [pt(S('Diagram: sporangiophore and sporangium'), 3, kind='criterion'),
       pt(S('stolon or rhizoid'), 3, kind='criterion'),
       anyn(S('stolon / rhizoid / sporangiophore', 'other correct'), 3, 1),
       pt(S('Spores or sporangium indicated'), 3, kind='criterion')], 'bio-3-2',
      'drawing-rhizopus-in-asexual-reproduction', SQ(30, 'Draw a large labelled diagram of Rhizopus'), 12),
    T('17biii1', 'Q17(b)(iii)1', 'C', _C(9, 'Sexual reproduction in Rhizopus results', 'name of this structure?'),
      [pt(S('*Zygospore'), 3)], 'bio-3-2', 'zygospore', SQ(30, 'What is the name of this structure?'), 3,
      stem=[Q17BIII]),
    T('17biii2', 'Q17(b)(iii)2', 'C', _C(9, 'What happens to the structure you named in part (b) (iii) 1. above if',
                                         'suitable conditions return?'),
      [pt(S('Germinates or described'), 3)], 'bio-3-2', 'zygospore-germination',
      SQ(30, 'What happens to the structure you named above'), 3,
      stem=[Q17BIII, M('1.', 9), _C(9, 'Sexual reproduction in Rhizopus results', 'name of this structure?')],
      id='bio-2024-hl-q17-b-iii',
      decision='The old card carded item 2 only; it keeps its id for 2., and 1. is added.'),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'Fungi can be beneficial.', 'examples of beneficial fungi.'),
      [anyn(S('Named edible mushrooms / yeast / other correct named'), 2, 3)], 'bio-3-2', 'beneficial-fungi',
      SQ(30, 'Give any two examples of beneficial fungi.'), 6),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'The kidneys are important in maintaining', 'the body?', nth=1),
      [pt(S('*Homeostasis'), 3)], 'bio-2-4', 'homeostasis-term', SQ(31, 'What term describes in maintenance'), 3,
      stem=[Q17C]),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'The nephron is the functional unit of the kidney.', 'supply.'),
      [pt(S('Diagram: Bowman’s capsule and', 'Henle'), 3, kind='criterion'),
       pt(S('Glomerulus or other blood supply'), 3, kind='criterion'),
       anyn(S('glomerulus / Bowman’s capsule / proximal', 'capillary'), 6, 1, open_list=True,
            note_sel=S('Any six correct labels e.g.', 'e.g.'))],
      'bio-2-6', 'drawing-and-labelling-the-nephron', SQ(31, 'Draw a large labelled diagram of the human nephron'), 12,
      stem=[Q17C]),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Give one way in which the composition of blood', 'glomerular filtrate.'),
      [pt(S('Blood contains blood cells', 'Other correctly described difference'), 3)], 'bio-2-6',
      'blood-vs-glomerular-filtrate', SQ(31, 'Give one way in which the composition of blood'), 3, stem=[Q17C]),
    T('17civ1', 'Q17(c)(iv)1', 'C', _C(10, 'Name any two parts of the nephron that reabsorb water.'),
      [anyn(S('Proximal convoluted tubule / loop of Henle', 'duct'), 2, 3)], 'bio-2-6', 'nephron-reabsorption',
      SQ(31, 'Name any two parts of the nephron'), 6, stem=[Q17C, Q17CIV], id='bio-2024-hl-q17-c-iv',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17civ2', 'Q17(c)(iv)2', 'C', _C(10, 'Name any two other substances that are reabsorbed', 'formation.'),
      [anyn(S('Glucose / amino acids / minerals / salts / ions / other correct'), 2, 3)], 'bio-2-6',
      'substances-reabsorbed', SQ(31, 'Name any two other substances'), 6, stem=[Q17C, Q17CIV]),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'What name is given to the stage of the cell cycle when', 'non-division?'),
      [pt(S('*Interphase'), 3)], 'bio-2-3', 'interphase-name', SQ(32, 'What is the name given to the stage when'), 3),
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'Give any two cell activities that occur during the state', 'of non-division.'),
      [anyn(S('Photosynthesis / respiration / DNA replication / protein synthesis / other correct'), 2, 3)],
      'bio-2-3', 'interphase-activities', SQ(32, 'Give any two cell activities'), 6),
    T('17diii1', 'Q17(d)(iii)1', 'C', _C(10, 'What name is given to the stage of mitosis shown', 'in the image?'),
      [pt(S('*Anaphase'), 3)], 'bio-2-3', 'anaphase-identification',
      SQ(32, 'What name is given to the stage of mitosis shown'), 3, stem=[Q17D], fig='q17-onion',
      id='bio-2024-hl-q17-d-iii-fig',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17diii2', 'Q17(d)(iii)2', 'C', _C(10, 'Explain how you know it is this stage.'),
      [pt(S('Chromosomes are being pulled apart or spindles contracting (shortening)'), 3)], 'bio-2-3',
      'recognising-anaphase', SQ(32, 'Explain how you know it is this stage.'), 3,
      stem=[Q17D, M('1.', 10), _C(10, 'What name is given to the stage of mitosis shown', 'in the image?')],
      fig='q17-onion'),
    T('17div', 'Q17(d)(iv)', 'C', _C(10, 'What stage of mitosis occurs immediately before the', '(d) (iii) 1. above?'),
      [pt(S('*Metaphase'), 3)], 'bio-2-3', 'mitosis-stage-order',
      SQ(32, 'What stage of mitosis occurs immediately before'), 3,
      stem=[Q17D, M('1.', 10), _C(10, 'What name is given to the stage of mitosis shown', 'in the image?')],
      fig='q17-onion', id='bio-2024-hl-q17-d-iv-fig'),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Sketch a diagram of a cell with a diploid number', 'part (d) (iv) above.'),
      [pt(S('Diagram: Cell with 4 duplicated chromosomes'), 3, kind='criterion'),
       pt(S('Spindle fibres from chromosomes to the ends'), 3, kind='criterion')], 'bio-2-3',
      'sketching-a-cell-at-metaphase', SQ(32, 'Sketch a simple cell with a diploid number'), 6,
      stem=[M('(iv)', 10), _C(10, 'What stage of mitosis occurs immediately before the', '(d) (iii) 1. above?')]),
    T('17dvi', 'Q17(d)(vi)', 'C', _C(10, 'What is the function of mitosis in multicellular organisms such as the onion?'),
      [pt(S('Growth or repair (of tissue)'), 3)], 'bio-2-3', 'function-of-mitosis',
      SQ(32, 'What is the function of mitosis'), 3),
    T('17dvii', 'Q17(d)(vii)', 'C', _C(10, 'What name is given to the group of disorders where', 'cell divisions?'),
      [pt(S('*Cancer'), 3)], 'bio-2-3', 'loss-of-control-of-mitosis',
      SQ(32, 'What name is given to the group of disorders'), 3),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-canal': ('038', 5, (372, 55, 545, 455), SEC, ['A', 'B', 'C'],
                 'Diagram of the human alimentary canal from the mouth down. An arrow labelled A points to the '
                 'tube running down the neck to the stomach; B labels the large organ at the upper left of '
                 'the abdomen; C labels the gland lying beneath the stomach; a label Small intestine points '
                 'to the coiled tube in the middle of the abdomen.', False),
    'q4-vessels': ('038', 6, (385, 108, 540, 290), SEC, [],
                   'Diagram of a longitudinal view of plant transport tissue: on the left, tubes with spiral '
                   'and ring-shaped thickening on their walls, with upward arrows inside them; on the right, '
                   'columns of long cells joined end to end by perforated cross-walls, with smaller cells '
                   'beside them and arrows pointing both up and down.', False),
    'q4-stem': ('038', 6, (417, 499, 542, 612), SEC, [],
                'Micrograph of a transverse section of a stem: a round section with many small dark bundles '
                'spread all through it.', False),
    'q7-stages': ('038', 9, (92, 92, 495, 320), SEC, ['X', 'Y', 'Z'],
                  'Flow diagram of genetic engineering. A cell leads by Isolation to a chromosome; an enzyme '
                  '(drawn as a small triangle) cuts it at Stage X, giving a gene. A plasmid (vector) is also '
                  'cut by the enzyme at Stage X, and the gene and the cut plasmid join as Recombinant DNA. '
                  'Stage Y takes the recombinant DNA into a host cell, which divides; Stage Z leads from the '
                  'host cells to Product.', False),
    'q11-flower': ('040', 2, (300, 240, 540, 425), SEC, ['A', 'B', 'C'],
                   'Drawing of a wind-pollinated flower: long stalks hang large pollen sacs outside the '
                   'flower, and feathery structures rise from its centre. Arrow A points to one of the large '
                   'hanging sacs, arrow B to the long stalk carrying it, and arrow C to one of the feathery '
                   'structures.', False),
    'q12-graph': ('040', 3, (375, 87, 540, 200), SEC, [],
                  'Graph of Numbers of organisms against Time: a solid wavy line labelled Prey rises and falls '
                  'in regular peaks. A point X is marked on the time axis near its right end.', False),
    'q12-food-web': ('040', 3, (115, 330, 500, 545), SEC, [],
                     'A marine food web of drawings joined by arrows. Phytoplankton feed Zooplankton and Shrimp; '
                     'Seaweed feeds Shrimp and Hermit crab; Zooplankton feed Salmon; Shrimp feed Salmon and '
                     'Herring; Hermit crab feeds Octopus; Salmon feed Seagull; Herring and Octopus '
                     'feed Seal; Seagull feeds Peregrine falcon; Seal feeds Orca whale.', False),
    'q13-mitochondrion': ('040', 4, (382, 122, 540, 250), SEC, [],
                          'Electron micrograph of a transverse section through an oval organelle with a smooth '
                          'outer membrane and many folds of an inner membrane running across its interior.',
                          False),
    'q13-leaf-cells': ('040', 4, (382, 318, 540, 450), SEC, [],
                       'Light micrograph of leaf cells: each cell is packed around its edge with many small dark '
                       'oval bodies, and arrows from the label Organelles point to them.', False),
    'q13b-ii-scheme': ('scheme', 19, (106, 343, 262, 362), SEC, [],
                       "The marking scheme's balanced equation: C6H12O6 + 6O2, an arrow, then 6CO2 + 6H2O, "
                       'with the number after each element printed as a subscript.', True),
    'q14-viruses': ('040', 5, (365, 312, 540, 455), SEC, [],
                    'Electron micrograph of virus particles: each has a many-sided head on a short tail.',
                    False),
    'q15b-i-question': ('040', 6, (80, 117, 545, 226), SEC, [],
                        'The printed question: (b) In snapdragon plants, the allele for tallness is dominant over '
                        'the allele for dwarfness. However, the allele for red flower shows incomplete dominance '
                        'with the allele for white flower. Pink flower is the phenotype that results in the '
                        'heterozygous condition. The two genes are not linked. (i) Explain the underlined terms. '
                        'The first "allele" and "heterozygous" are underlined.', False),
    'q16-male': ('040', 7, (400, 92, 540, 240), SEC, ['A', 'B', 'C'],
                 'Side-view diagram of the human male reproductive system. Arrow A points to the tube running '
                 'through the penis; arrow B to the tube looping up from the testis; C labels the gland at the '
                 'base of the bladder.', False),
    'q16-female': ('040', 7, (365, 355, 540, 690), SEC, ['X', 'Y', 'Z'],
                   'Outline of a human female body with organs drawn in. Arrow X points to a gland in the '
                   'front of the neck; two arrows Y point to the small glands sitting on top of the organs '
                   'labelled Kidney; two arrows Z point to the two small oval organs on either side of the '
                   'uterus.', False),
    'q16-phototropism': ('040', 8, (322, 55, 540, 200), SEC, [],
                         'Photograph of a seedling in a small pot, its stem bending sideways towards a lamp at the '
                         'left of the picture.', False),
    'q17-graph': ('040', 9, (195, 112, 400, 295), SEC, [],
                  'Graph of Enzyme activity against pH, from 0 to 10. A solid curve A rises from about pH 1, '
                  'peaks at pH 2 and falls to zero by about pH 3; a dashed curve B rises from about pH 6, peaks '
                  'at pH 7 and falls to zero by about pH 8.', False),
    'q17-onion': ('040', 10, (420, 368, 540, 510), SEC, [],
                  'Light micrograph of an onion cell dividing: two groups of dark, V-shaped chromosomes are '
                  'moving apart towards opposite ends of the cell.', False),
}
