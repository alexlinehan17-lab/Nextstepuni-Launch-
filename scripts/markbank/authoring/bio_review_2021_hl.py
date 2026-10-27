"""Biology 2021 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-13), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover
    (with the note that the 2021 papers were adjusted for disruption to
    learning), p2 instructions, p3-p9 Section A Questions 1-7, p10-p12
    Section B Questions 8-10, p13 Section C answerbook instructions,
    p14-p17 graph paper, p18-p39 ruled answer pages, p40 back cover. No
    acknowledgements page.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "Do not hand this question paper up", p12 back cover.
  * LC025ALP000EV (marking scheme), 28 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7-p25 Questions
    1-17, p26-p27 "BLANK PAGE", p28 back cover.

The 2021 papers set fewer questions to answer: any four of Section A, any one
of Section B and any three of Section C. Every printed question is carded.

The sitting was already carded (177 authored cards, all shipped). As for the
later sittings, every task is re-derived from the PDFs at the scheme's own
mark boundaries and the existing cards are corrected in place: every shipped
id is kept, mapped (`id=`) to the task it was carding, verified or corrected
with its old fields recorded; tasks the old cards bundled or missed are
added.

Section A: Q1 is the best five of six parts at 4 ("5(4)"); Q2-Q6 are each
"6(3) + 2" over seven responses, an ordered split carded at 3 a response;
Q7 is "10(2)", a 2-mark line for each term of each pair. Sections B and C
print a mark per row, with 1-mark label rows in Q14(c)(iv), Q15(b)(i) and
Q16(b)(i).

No printed choice here is marked differently per option, so none is split
("choice is not a route"): Q11(c)(ii) agriculture or fisheries or forestry is
marked on one named-practice row and one description row, and Q11(c)(iii)2's
moving or sessile animals are answer variants of one task.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2021, 'hl'
REVIEWED_AT = '2026-10-13'
BASELINE_COMMIT = 'a585b6d89'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2021-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': '73adc0bfbd91031ed7072cf1c7b84e3c69a2a7bb3865c789ffa4f64c0183432e',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2021-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': '8270273dec85fd363078779d5369e57145f1e521ae29ed7b820db79b339f1dbc',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2021-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '734448a721f9216d91ab7a07d2148339d9bff10245160aa3c20e4511f762031a',
               'pages': 28},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 13)},
            13: 'answerbook-instructions', **{p: 'graph-paper' for p in range(14, 18)},
            **{p: 'answer-pages' for p in range(18, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', **{p: 'marking' for p in range(7, 26)},
               26: 'blank', 27: 'blank', 28: 'back-cover'},
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
BEST_OF = {1: (5, 4)}
LADDERS = {q: {'steps': [3, 3, 3, 3, 3, 3, 2], 'notation': '6(3) + 2'} for q in range(2, 7)}

CHECKSUMS = {
    1: {4: 6},   # printed "5(4)": the best five of the six 4-mark parts carded here
    **{q: {3: 7} for q in range(2, 7)}, 7: {2: 10},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in range(11, 16)},
    **{(n, 'b'): {3: 9} for n in (11, 12, 13, 14)}, (15, 'b'): {3: 8, 1: 3},
    **{(n, 'c'): {3: 8} for n in (11, 12, 13, 15)}, (14, 'c'): {3: 7, 1: 3},
    (16, 'a'): {3: 10}, (16, 'b'): {3: 8, 1: 6}, (16, 'c'): {3: 10}, (16, 'd'): {3: 10},
    **{(17, x): {3: 10} for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 13), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any four', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any one', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any three', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any four', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the best five make 20.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 5, 'the following', 'Q3 lead-in: every part asked.'),
    ('038', 8, 'the following', 'Q6 lead-in: every statement asked.'),
    ('038', 8, 'or', 'Q6 "true or false": the answer options.'),
    ('038', 9, 'the following', 'Q7: every pair distinguished, one card per lettered pair.'),
    ('038', 10, 'any one', 'Section B rubric repeated.'),
    ('038', 10, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('038', 10, 'or', 'Q8(b)(i)1 "reagent or chemicals": either form; one answer.'),
    ('038', 12, 'or', 'Q10(a)(i) "unicellular or multicellular": the answer options.'),
    ('040', 2, 'any three', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q11(a)(i) "the following food chain": a reference.'),
    ('040', 2, 'the following', 'Q11(b) passage "the following spring": passage text.'),
    ('040', 2, 'both', 'Q11(b) passage "both poisoning bats": passage text.'),
    ('040', 2, 'or', 'Q11(b) passage "pipistrelle or soprano pipistrelle": passage text.'),
    ('040', 2, 'or', 'Q11(b) passage "3,500 or so": passage text.'),
    ('040', 2, 'or', 'Q11(b)(v) "From the text, or otherwise": source, not a choice of task.'),
    ('040', 2, 'or', 'Q11(c)(ii) "agriculture or fisheries or forestry": marked on the same two rows for every '
                     'area; one card.'),
    ('040', 2, 'or', 'Q11(c)(ii), same choice.'),
    ('040', 2, 'or', 'Q11(c)(iii) "monitor or survey": description.'),
    ('040', 3, 'both', 'Q12(b)(i) "heterozygous for both traits": description.'),
    ('040', 3, 'both', 'Q12(b)(iv) "recessive for both": description.'),
    ('040', 3, 'the following', 'Q12(b)(iv) "the following results": a reference.'),
    ('040', 3, 'the following', 'Q12(c)(ii): each step asked, one card per item.'),
    ('040', 6, 'or', 'Q15(b)(ii) "insect or wind-pollinated": the answer options.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'both', 'Q16(a)(iv) "both excretion and temperature regulation": description.'),
    ('040', 7, 'the following', 'Q16(b)(i): every part labelled; one card.'),
    ('040', 7, 'the following', 'Q16(b)(ii): each heading asked, one card per item.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
]

ROUTES = {}

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list ("1." on its own line, its item on the next)."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


def tick(clip, answer):
    return G('tick-col', page=9, clip=clip, headers=['True', 'False'], expect=answer, marks=3)


def bundled(parts, keep):
    return f'The old card bundled {parts}; it keeps its id for {keep}.'


EACH_ITEM = '"Each of the following": separately priced items, one card each.'

Q1 = _A(3, 'Answer any five of the following parts (a) to (f):')
Q2 = _A(4, 'The diagram below outlines some stages in the nitrogen cycle.')
Q3 = _A(5, 'The diagram shows a nucleus of a diploid cell undergoing one stage of mitosis.', 'relation to mitosis.')
Q4 = _A(6, 'A current theory of enzyme action is illustrated in the diagram below.')
Q5 = _A(7, 'The diagram shows some of the early stages in the development of a human embryo.')
Q6 = _A(8, 'Indicate whether the following statements are true or false', 'appropriate box in each case.')
Q7 = _A(9, 'In the case of each of the following pairs of terms', 'writing a brief sentence about each.')
Q8A = _A(10, 'Answer parts (i) and (ii) in relation to the principles of experimentation.')
Q8B = _A(10, 'Answer the following in relation to some laboratory investigations that you carried out.')
Q8BI = _A(10, 'When conducting qualitative food tests:')
Q8BII = _A(10, 'When isolating DNA from a plant tissue:')
Q9B1 = _A(11, 'Answer parts (i) and (ii) in relation to a laboratory activity to investigate heat',
          'denaturation of an named enzyme.')
Q9B2 = _A(11, 'Answer parts (iii) and (iv) in relation to a laboratory investigation on the effect of',
          'temperature on the rate of activity of a named enzyme.')
Q10B = _A(12, 'In an investigation on the growth of leaf yeasts', 'incubator at 25°C for 7 days.')
Q11B = [_C(2, 'After mating in the autumn, Irish bats hibernate', 'robbing them of their insect prey.'),
        _C(2, 'A single pipistrelle or soprano pipistrelle', 'biting insects on balmy summer evenings.'),
        _C(2, '(Adapted from “Batty about Irish bats!”', '2012)')]
Q11C3 = _C(2, 'Ecologists monitor or survey animal population numbers on a regular basis.')
Q12B = [_C(3, 'There is variation in seed shape and seed colour in pea plants.'),
        _C(3, 'Round (R) seed is dominant to wrinkled seed', 'These genes are not linked.')]
Q12BI = [M('(i)', 3), _C(3, 'Write the genotype of a plant heterozygous for both traits.')]
Q12C = _C(3, 'The haemophilia gene (n) is sex', 'to affected people.')
Q12CII = _C(3, 'Outline what happens in each of the following steps of genetic engineering:')
Q13B = _C(4, 'The diagram outlines some of the main steps that may occur during respiration of a', 'carbon sugar.')
Q13C = _C(4, 'Chlorophyll is a green pigment found in plants.', 'chemicals.')
Q14B = _C(5, 'The diagram shows a longitudinal section (L.S.) of a villus from the human digestive', 'system.')
Q14C = _C(5, 'The ‘transpiration stream’ has an important role', 'vascular tissues.')
Q14CIII = _C(5, 'Xylem and phloem are two vascular tissues in plants.')
Q15A = _C(6, 'Organisms can respond to changes in their external and internal environment in',
          'including through homeostasis.')
Q15B = _C(6, 'The diagram is of a flower.')
Q15BVI = _C(6, 'Seed and fruit development follow successful fertilisation.')
Q15C = _C(6, 'Germination in seeds follows dispersal and a period of dormancy.')
Q16A = _C(7, 'The diagram shows some parts of the longitudinal section (L.S.) of human skin.',
          'temperature regulation.')
Q16AIV = [M('(iv)', 7), _C(7, 'Which labelled structure is involved in both excretion and temperature', 'regulation?')]
Q16BII = _C(7, 'Describe the differences between the human male and female type of gamete', 'following headings:')
Q16C = _C(8, 'SARS', 'antibodies are produced.')
Q16CV = _C(8, 'The graph below shows the antibody production after a person receives a',
           'infected with the virus (B).')
Q16DIII = [M('(iii)', 8), _C(8, 'Identify the gas, soluble in blood plasma, which controls the rate of breathing.')]
Q17A = _C(9, 'The diagram shows an organism you have studied.')
Q17AIII = [M('(iii)', 9), _C(9, 'State the mode of nutrition used by this organism.')]
Q17B = _C(9, 'The diagram below shows a unicellular organism.')
Q17BIII = _C(9, 'The organism labelled Euglena, is a prey species of the larger organism.')
Q17C = _C(10, 'The diagram shows a cross section of the spinal cord along with some neurons from',
          'the peripheral nervous system.')
Q17D = [_C(10, 'A scientist used a light microscope to view images A and B', 'different concentrations.'),
        _C(10, 'The dark grey shaded areas show the vacuoles filled with solution.')]
Q17DVII = _C(10, 'When preparing plant cells for viewing using the microscope')

L_MITOSIS = [L('X', S('Spindle', page=8, after='Identify the part labelled X'), True)]
L_EMBRYO = [L('B', S('Morula', page=9), True), L('C', S('Blastocyst', page=9), True)]
L_VILLUS = [L('X', S('*Lacteal', page=18), True)]
L_FLOWER = [L('A', S('*Anther', page=20), True), L('B', S('*Filament', page=20), True),
            L('C', S('*Ovary', page=20), True)]
L_AMOEBA_B = [L('B', S('*Contractile vacuole', page=24), True)]
L_AMOEBA_C = [L('C', S('*Food vacuole', page=24), True)]
L_SPINAL = [L('X', S('*Meninges', page=25), True)]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Identify one difference between fats and oils at room temperature.'),
      [pt(S('Fats are solid and oils are liquid (Allow Fats are saturated and oils are unsaturated)'), 4)],
      'bio-1-2', 'fats-and-oils', SQ(7, 'Identify one difference between fats and oils'), 4, stem=[Q1],
      id='bio-2021-hl-q1-a'),
    T('1b', 'Q1(b)', 'A', _A(3, 'Triglycerides and phospholipids are two types of lipid.', 'and a phospholipid.'),
      [pt(S('Triglyceride has three fatty acids and phospholipid has two fatty acids',
            'Triglyceride has no phosphate and phospholipid has a phosphate'), 4)],
      'bio-1-2', 'triglycerides-and-phospholipids', SQ(7, 'Identify one difference between a triglyceride'), 4,
      stem=[Q1], id='bio-2021-hl-q1-b'),
    T('1c', 'Q1(c)', 'A', _A(3, 'Identify one metabolic role for lipids in cells.'),
      [pt(S('Energy (source or store)'), 4)], 'bio-1-2', 'metabolic-role-of-lipids',
      SQ(7, 'Identify one metabolic role for lipids in cells:'), 4, stem=[Q1], id='bio-2021-hl-q1-c'),
    T('1d', 'Q1(d)', 'A', _A(3, 'Name one fat', 'present in food.'),
      [pt(S('A or D or E or K'), 4)], 'bio-1-2', 'fat-soluble-vitamins', SQ(7, 'Name one fat soluble vitamin'), 4,
      stem=[Q1], id='bio-2021-hl-q1-d'),
    T('1e', 'Q1(e)', 'A', _A(3, 'Name one disorder associated with a deficiency of the vitamin', 'above.'),
      [pt(S('A: Night blindness or D: Rickets', 'fat-soluble vitamin disorder'), 4, whole=True)], 'bio-1-2',
      'vitamin-deficiency-disorders', SQ(7, 'Name one deficiency disorder:'), 4,
      stem=[Q1, M('(d)', 3), _A(3, 'Name one fat', 'present in food.')], id='bio-2021-hl-q1-e',
      decision='The scheme pairs each disorder with its vitamin on one line: one row, read whole.'),
    T('1f', 'Q1(f)', 'A', _A(3, 'Name one element present in dissolved salts in food.'),
      [pt(S('Sodium (Na) or Calcium (Ca) or Magnesium (Mg) or Chlorine (Cl) or Potassium (K)'), 4)], 'bio-1-2',
      'elements-in-salts', SQ(7, 'Name one element present in dissolved salts:'), 4, stem=[Q1],
      id='bio-2021-hl-q1-f'),
    T('2a', 'Q2(a)', 'A', _A(4, 'Why do organisms need nitrogen?'),
      [pt(S('To make protein (or named type of protein) or to make DNA', 'make ATP (or ADP or NAD(P))'), 3)],
      'bio-1-2', 'why-nitrogen', SQ(7, 'Why do organisms need nitrogen?'), 3, stem=[Q2], fig='q2-nitrogen-cycle',
      id='bio-2021-hl-q2-a'),
    T('2b', 'Q2(b)', 'A', _A(4, 'Name the processes indicated at A and B in the diagram above.'),
      [pt(S('Nitrogen fixation'), 3, label=S('A:')), pt(S('Denitrification'), 3, label=S('B:'))], 'bio-3-2',
      'fixation-and-denitrification', SQ(7, 'Name the processes that occur at A and B:'), 6, stem=[Q2],
      fig='q2-nitrogen-cycle'),
    T('2c', 'Q2(c)', 'A', _A(4, 'Name the type of bacteria involved in the process indicated by C', 'diagram above.'),
      [pt(S('Nitrifying (bacteria) (or correctly named bacteria)'), 3)], 'bio-3-2', 'nitrifying-bacteria',
      SQ(7, 'Name the type of bacteria involved in process C:'), 3, stem=[Q2], fig='q2-nitrogen-cycle'),
    T('2d', 'Q2(d)', 'A', _A(4, 'The application of fertilisers in agriculture', 'outcomes of this practice.'),
      [anyn(S('More nitrification / more nitrogen absorbed by plants', 'any other valid outcomes'), 2, 3)],
      'bio-3-2', 'effects-of-fertilisers', SQ(7, 'Two possible outcomes of this practice'), 6, stem=[Q2],
      fig='q2-nitrogen-cycle', id='bio-2021-hl-q2-d'),
    T('2e', 'Q2(e)', 'A', _A(4, 'On the diagram, place the letter D on one location where decomposers act.'),
      [pt(S('On one arrow to soil ammonia (from animals or from pea plants)'), 3, kind='criterion')], 'bio-3-2',
      'where-decomposers-act', SQ(7, 'On diagram, place letter D'), 3, stem=[Q2], fig='q2-nitrogen-cycle',
      id='bio-2021-hl-q2-e'),
    T('3a', 'Q3(a)', 'A', _A(5, 'Name the stage of mitosis shown in the diagram.'),
      [pt(S('Anaphase'), 3)], 'bio-2-3', 'anaphase', SQ(8, 'Name the stage of mitosis shown in the diagram:'), 3,
      stem=[Q3], fig='q3-mitosis', id='bio-2021-hl-q3-a-fig'),
    T('3b', 'Q3(b)', 'A', _A(5, 'Justify your answer at part (a) above.'),
      [pt(S('Spindle (or X) shortening or spindle contracting', 'chromosomes moving to the poles'), 3)], 'bio-2-3',
      'recognising-anaphase', SQ(8, 'Justify your answer:'), 3,
      stem=[Q3, M('(a)', 5), _A(5, 'Name the stage of mitosis shown in the diagram.')], fig='q3-mitosis',
      id='bio-2021-hl-q3-b-fig'),
    T('3c', 'Q3(c)', 'A', _A(5, 'Identify the part labelled X in the diagram.'),
      [pt(S('Spindle'), 3)], 'bio-2-3', 'spindle', SQ(8, 'Identify the part labelled X in the diagram:'), 3,
      stem=[Q3], fig='q3-mitosis', labels=L_MITOSIS, id='bio-2021-hl-q3-c-fig'),
    T('3d', 'Q3(d)', 'A', _A(5, 'Explain the term diploid.'),
      [pt(S('Two copies of each chromosome (in the nucleus)', 'chromosomes'), 3)], 'bio-2-3', 'diploid',
      SQ(8, 'Explain what is meant by the term diploid:'), 3, stem=[Q3], fig='q3-mitosis', id='bio-2021-hl-q3-d'),
    T('3e', 'Q3(e)', 'A', _A(5, 'What is the diploid number of this cell?'),
      [pt(S('Four'), 3)], 'bio-2-3', 'diploid-number', SQ(8, 'State the diploid number of the cell'), 3,
      stem=[Q3], fig='q3-mitosis', id='bio-2021-hl-q3-e-fig'),
    T('3f', 'Q3(f)', 'A', _A(5, 'Outline one function of mitosis in humans.'),
      [pt(S('Growth or repair tissue or replace tissue (cells)'), 3)], 'bio-2-3', 'functions-of-mitosis',
      SQ(8, 'Outline one function of mitosis in humans:'), 3, stem=[Q3], fig='q3-mitosis', id='bio-2021-hl-q3-f'),
    T('3g', 'Q3(g)', 'A', _A(5, 'Give one example of a human cell not produced by mitosis.'),
      [pt(S('Sperm or egg or gamete or sex cell'), 3)], 'bio-2-3', 'cells-not-from-mitosis',
      SQ(8, 'Give one example of a human cell not produced by mitosis:'), 3, stem=[Q3], fig='q3-mitosis', id='bio-2021-hl-q3-g'),
    T('4a', 'Q4(a)', 'A', _A(6, 'Identify what is represented by each of the labels A and B.'),
      [pt(S('Substrate'), 3, label=S('A:')), pt(S('Enzyme-substrate complex'), 3, label=S('B:'))], 'bio-2-1',
      'substrate-and-complex', SQ(8, 'Identify the parts labelled A and B:',
                                paired='The (a) under the scheme\'s Question 4: "the parts labelled A and B" for the paper\'s '
                                       '"each of the labels A and B".'), 6, stem=[Q4], fig='q4-enzyme',
      id='bio-2021-hl-q4-a-fig'),
    T('4b', 'Q4(b)', 'A', _A(6, 'Which theory of enzyme action is illustrated by the diagram?'),
      [pt(S('Induced fit or active site (theory)'), 3, note_sel=S('(Accept ‘lock and key’)'))], 'bio-2-1',
      'induced-fit', SQ(8, 'What theory is illustrated in the diagram?'), 3, stem=[Q4], fig='q4-enzyme',
      id='bio-2021-hl-q4-b-fig'),
    T('4c', 'Q4(c)', 'A', _A(6, 'What type of metabolic reaction is illustrated by the diagram?'),
      [pt(S('Catabolic'), 3)], 'bio-2-1', 'catabolic', SQ(8, 'What type of metabolic reaction is illustrated'), 3,
      stem=[Q4], fig='q4-enzyme', id='bio-2021-hl-q4-c-fig'),
    T('4d', 'Q4(d)', 'A', _A(6, 'Justify your answer at part (c) above.'),
      [pt(S('Substrate (or molecule or A) broken down'), 3)], 'bio-2-1', 'recognising-catabolism',
      SQ(8, 'Justify your answer at (c) above:'), 3,
      stem=[Q4, M('(c)', 6), _A(6, 'What type of metabolic reaction is illustrated by the diagram?')],
      fig='q4-enzyme', id='bio-2021-hl-q4-d-fig'),
    T('4e', 'Q4(e)', 'A', _A(6, 'What is meant by specificity in relation to enzymes?'),
      [pt(S('Only acts on one substrate (type)'), 3)], 'bio-2-1', 'specificity',
      SQ(8, 'What is meant by the term specificity'), 3, stem=[Q4], fig='q4-enzyme', id='bio-2021-hl-q4-e'),
    T('4f', 'Q4(f)', 'A', _A(6, 'Identify the cell organelle where enzymes are produced.'),
      [pt(S('Ribosome'), 3)], 'bio-1-3', 'ribosome', SQ(8, 'Identify the cell organelle where enzymes are produced:'),
      3, stem=[Q4], fig='q4-enzyme', id='bio-2021-hl-q4-f'),
    T('5a', 'Q5(a)', 'A', _A(7, 'Name the event that occurs at A in the diagram.'),
      [pt(S('Ovulation'), 3)], 'bio-2-5', 'ovulation', SQ(9, 'Name the event that occurs at A:'), 3, stem=[Q5],
      fig='q5-embryo'),
    T('5b', 'Q5(b)', 'A', _A(7, 'Identify the hormone responsible for the event named at part (a) above.'),
      [pt(S('Luteinising (hormone) or LH'), 3)], 'bio-2-5', 'luteinising-hormone',
      SQ(9, 'Identify the hormone responsible for the event'), 3,
      stem=[Q5, M('(a)', 7), _A(7, 'Name the event that occurs at A in the diagram.')], fig='q5-embryo',
      id='bio-2021-hl-q5-b'),
    T('5c', 'Q5(c)', 'A', _A(7, 'Identify the stages labelled B and C in the development of the embryo.'),
      [pt(S('Morula'), 3, label=S('B:')), pt(S('Blastocyst'), 3, label=S('C:'))], 'bio-2-5', 'morula-and-blastocyst',
      SQ(9, 'Identify the stages labelled B and C:'), 6, stem=[Q5], fig='q5-embryo', labels=L_EMBRYO),
    T('5d', 'Q5(d)', 'A', _A(7, 'What event is illustrated by D in the diagram?'),
      [pt(S('Implantation (or described)'), 3)], 'bio-2-5', 'implantation', SQ(9, 'What event is illustrated by D?'),
      3, stem=[Q5], fig='q5-embryo'),
    T('5e', 'Q5(e)', 'A', _A(7, 'Name the two tissues involved in the formation of the placenta.'),
      [pt(S('Endometrium or uterine or uterus lining'), 3, label=S('Tissue 1:')),
       pt(S('Embryonic or embryo (tissue)'), 3, label=S('Tissue 2:'),
          note_sel=S('(Accept chorionic or trophoblastic)'))], 'bio-2-5', 'placenta',
      SQ(9, 'Name the two tissues involved in the formation of the placenta:'), 6, stem=[Q5], fig='q5-embryo', id='bio-2021-hl-q5-e'),
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(8, start), [tick(clip, answer)], topic, concept, SQ(9, start), 3,
      stem=[Q6], id=f'bio-2021-hl-q6-{x}')
    for x, start, clip, answer, topic, concept in [
        ('a', 'Adrenaline is secreted into the blood when experiencing a threat.', (60, 326, 560, 345), 'True',
         'bio-2-4', 'adrenaline'),
        ('b', 'Plants are producers; however, they still need mitochondria.', (60, 345, 560, 364), 'True',
         'bio-2-2', 'plants-respire'),
        ('c', 'Neurotransmitters are transported in the blood.', (60, 364, 560, 383), 'False', 'bio-2-4',
         'neurotransmitters'),
        ('d', 'A potato is a root modified to store food.', (60, 383, 560, 402), 'False', 'bio-2-6', 'potato'),
        ('e', 'Tissue culture involves growing cells on an artificial medium.', (60, 402, 560, 420), 'True',
         'bio-1-3', 'tissue-culture'),
        ('f', 'There are four bones in the middle ear.', (60, 420, 560, 439), 'False', 'bio-2-4',
         'middle-ear-bones'),
        ('g', 'Monocotyledonous plants are almost always herbaceous.', (60, 439, 560, 458), 'True', 'bio-2-6',
         'monocots')]
] + [
    T(f'7{x}', f'Q7({x})', 'A', _A(9, ask), rows, 'bio-2-4', concept, SQ(9, 'Distinguish between the following pairs of terms:'), 4, stem=[Q7],
      id=f'bio-2021-hl-q7-{x}')
    for x, ask, rows, concept, sq in [
        ('a', 'Carpal and tarsal.', [pt(S('Bones in the wrist'), 2, label=S('Carpal:')),
                                     pt(S('Bones in the ankle or heel'), 2, label=S('Tarsal:'))],
         'carpals-and-tarsals', 'Carpal:'),
        ('b', 'Tendon and ligament.', [pt(S('Connects muscle to bone'), 2, label=S('Tendon:')),
                                       pt(S('Connects bone to bone'), 2, label=S('Ligament:'))],
         'tendons-and-ligaments', 'Tendon:'),
        ('c', 'Biceps and triceps.', [pt(S('(Muscle) contracts to bend arm', 'humerus (upper arm)'), 2,
                                         label=S('Biceps:')),
                                      pt(S('(Muscle) contracts to straighten arm', 'humerus (upper arm)'), 2,
                                         label=S('Triceps:'))], 'biceps-and-triceps', 'Biceps:'),
        ('d', 'Osteoblast and osteoclast.', [pt(S('Osteoblast: (Cell that) builds up bone'), 2),
                                             pt(S('Osteoclast: (Cell that) breaks down bone'), 2)],
         'osteoblasts-and-osteoclasts', 'Osteoblast:'),
        ('e', 'Axial skeleton and appendicular skeleton.',
         [pt(S('Skull and vertebrae (or spine or backbone)'), 2, label=S('Axial skeleton:')),
          pt(S('Appendicular skeleton: Limbs', 'girdle (or hips)'), 2)], 'axial-and-appendicular', 'Axial skeleton:')]
] + [
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(10, 'Where are the results of an investigation normally reported and published?'),
      [pt(S('Scientific journal or scientific website'), 3)], 'bio-u1', 'publishing-results',
      SQ(10, 'Where are the results of an investigation normally reported'), 3, stem=[Q8A], id='bio-2021-hl-q8-a-i'),
    T('8aii', 'Q8(a)(ii)', 'B', _A(10, 'Explain why random selection is important in experimental design.'),
      [pt(S('Reduces bias or increases reliability or fair (test)'), 3)], 'bio-u2', 'random-selection',
      SQ(10, 'Explain why random selection is important'), 3, stem=[Q8A], id='bio-2021-hl-q8-a-ii'),
] + [
    T(f'8bi{n}', f'Q8(b)(i){n}', 'B', item(10, n, ask, 'When conducting qualitative food tests', doc='038'),
      [pt(S(ans), 3)], 'bio-1-2', concept, SQ(10, sq), 3, stem=[Q8B, Q8BI], id=f'bio-2021-hl-q8-b-i-{n}')
    for n, ask, ans, concept, sq in [
        (1, 'presence of protein?', '*Biuret (reagent) (or copper sulphate (CuSO4) and sodium hydroxide (NaOH))',
         'test-for-protein', '1. What reagent or chemicals did you use'),
        (2, 'in a food sample?', '*Purple (or lilac or violet)', 'positive-protein-test',
         '2. What colour indicates the presence of protein')]
] + [
    T(f'8bii{n}', f'Q8(b)(ii){n}', 'B', item(10, n, ask, 'When isolating DNA from a plant tissue', doc='038'),
      rows, 'bio-1-2', concept, SQ(10, sq), total, stem=[Q8B, Q8BII], id=f'bio-2021-hl-q8-b-ii-{n}')
    for n, ask, rows, concept, sq, total in [
        (1, 'Why did you chop the tissue?',
         [pt(S('To break (or disrupt) the cell walls or allow cytoplasm to leak out or to', 'increase surface area'),
             3)], 'chopping-the-tissue', '1. Why did you chop the plant tissue?', 3),
        (2, 'Why did you add salt to the chopped tissue?',
         [pt(S('To cause the DNA to clump or protect (shield) the DNA from the protein'), 3)], 'adding-salt',
         '2. Why add salt to the chopped tissue?', 3),
        (3, 'Why did you add washing up liquid to the chopped tissue and salt?',
         [pt(S('Breaks down membranes (cell or nuclear) or to release (or free) DNA from', 'nucleus (within cell)'),
             3)], 'adding-washing-up-liquid', '3. Why add washing up liquid', 3),
        (4, 'Describe how the DNA was then isolated from this solution.',
         [anyn(S('Cool / blend for 3 seconds / filter (solution) / (add) protease (or named',
                 'DNA is visible or DNA removed'), 3, 3)], 'isolating-dna', '4. Describe how the DNA was then isolated:',
         9)]
] + [
    T('9ai', 'Q9(a)(i)', 'B', _A(11, 'What is meant by enzyme denaturation?'),
      [pt(S('Active site destroyed or loss of shape or loss of function'), 3)], 'bio-2-1', 'denaturation',
      SQ(11, 'What is meant by enzyme denaturation?'), 3, id='bio-2021-hl-q9-a-i'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(11, 'Other than temperature, give one condition that will denature an enzyme.'),
      [pt(S('(Unsuitable) pH or agitation or ethanol or radiation'), 3)], 'bio-2-1', 'denaturing-conditions',
      SQ(11, 'Other than temperature, give one condition'), 3, id='bio-2021-hl-q9-a-ii'),
    T('9bi', 'Q9(b)(i)', 'B', _A(11, 'Describe how the enzyme was treated in the test investigation and in the control.'),
      [pt(S('Boiled (or heated to above 60°C)'), 3, label=S('Test:')),
       pt(S('Not boiled (or not heated strongly)'), 3, label=S('Control:'))], 'bio-2-1', 'heat-denaturation-setup',
      SQ(11, 'Describe how the enzyme was treated in the:'), 6, stem=[Q9B1], id='bio-2021-hl-q9-b-i',
      notes='The scheme: answers must match the named enzyme.'),
    T('9bii', 'Q9(b)(ii)', 'B', _A(11, 'Compare the results of the test investigation to that of the control.'),
      [pt(S('No activity or no foam (or bubbles) or blue-black'), 3, label=S('Test:')),
       pt(S('High level of activity or foam (or bubbles) produced or no blue-black'), 3, label=S('Control'))],
      'bio-2-1', 'heat-denaturation-results', SQ(11, 'Compare the results:'), 6, stem=[Q9B1],
      id='bio-2021-hl-q9-b-ii'),
    T('9biii', 'Q9(b)(iii)', 'B', _A(11, 'How did you measure the rate of enzyme activity?'),
      [pt(S('Catalase:', 'disappearance of purple or violet colour'), 3, whole=True, kind='criterion'),
       pt(S('per minute (or per unit time or time taken for change to occur)'), 3)], 'bio-2-1',
      'measuring-enzyme-rate', SQ(11, 'How did you measure the rate of activity of the enzyme?'), 6, stem=[Q9B2],
      id='bio-2021-hl-q9-b-iii',
      decision='The scheme prints the measurement for each named enzyme on one 3-mark row: one row, read whole.'),
    T('9biv', 'Q9(b)(iv)', 'B', _A(11, 'Label the axes below and draw a curve', 'varies with temperature.'),
      [pt(S('x: Temperature (°C) and y: Rate (or indication of time)'), 3, kind='criterion', label=S('Axes:'),
          whole=True),
       pt(S('Rising and falling curve'), 3, kind='criterion', label=S('Plot:'))], 'bio-2-1',
      'rate-against-temperature', SQ(11, 'Label axes and draw a curve'), 6, stem=[Q9B2], qfig='q9b-iv-question',
      id='bio-2021-hl-q9-b-iv',
      decision='The ask points at axes printed below it: the question is shown as printed, with the axes.'),
    T('10ai', 'Q10(a)(i)', 'B', _A(12, 'Is leaf yeast a unicellular or a multicellular organism?'),
      [pt(S('*Unicellular'), 3)], 'bio-3-2', 'leaf-yeast-is-unicellular', SQ(12, 'Is leaf yeast cell unicellular'), 3,
      id='bio-2021-hl-q10-a-i'),
    T('10aii', 'Q10(a)(ii)', 'B', _A(12, 'Name the type of asexual reproduction in yeast.'),
      [pt(S('*Budding'), 3)], 'bio-3-2', 'budding', SQ(12, 'Name the type of asexual reproduction in yeast:'), 3,
      id='bio-2021-hl-q10-a-ii'),
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'B', _A(12, ask, aend), rows, 'bio-3-2', concept, SQ(12, sq), total,
      stem=[Q10B], fig='q10-table', id=f'bio-2021-hl-q10-b-{r}')
    for r, ask, aend, rows, concept, sq, total in [
        ('i', 'What is the purpose of malt in these plates?', None, [pt(S('Food (or nutrients)'), 3)], 'malt',
         'What is the purpose of malt on these plates?', 3),
        ('ii', 'Why was the underside of the leaf facing the agar?', None,
         [pt(S('Leaf yeast mostly live on under-surface', 'that yeast could fall onto the agar'), 3)],
         'leaf-underside', 'Why was the underside of the leaf facing the agar?', 3),
        ('iii', 'What is the purpose of plate A in this investigation?', None,
         [pt(S('A control (or described) or to compare to the results'), 3)], 'control-plate',
         'What is the purpose of plate A', 3),
        ('iv', 'Identify the colour of the leaf yeast colonies on plate B.', None, [pt(S('Pink (or red)'), 3)],
         'leaf-yeast-colour', 'Describe the colour of leaf yeast colonies', 3),
        ('v', 'Suggest one reason for the difference in results between plates B and C.', None,
         [pt(S('(More) pollution in the urban air', '(smoke / sulphur dioxide / harmful chemicals)'), 3)],
         'pollution-and-leaf-yeast', 'Suggest one reason for the difference in results', 3),
        ('vi', 'Describe two aseptic techniques that were carried out in this investigation to',
         'prevent growth of other microbes.',
         [anyn(S('Wipe surface with disinfectant', 'keep Bunsen lit (nearby)'), 2, 3)], 'aseptic-technique',
         'Describe two aseptic techniques', 6),
        ('vii', 'State one correct disposal method for these plates after the investigation.', None,
         [pt(S('Soaked in disinfectant (or named disinfectant) or autoclaved', 'biohazard bag'), 3)],
         'disposing-of-plates', 'State one correct disposal method', 3)]
] + [
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', [_C(2, 'Draw a pyramid of numbers from the following food chain:'),
                                 _C(2, 'Cowslips', br=True), _C(2, 'Moth'), _C(2, 'Bat'), _C(2, 'Mites')],
      [pt(S('Draw a pyramid of numbers:', after='Question 11'), 3, kind='criterion',
          note='The scheme draws the three pyramid shapes it accepts; they are shown after reveal.'),
       pt(S('Correct organism at each trophic level'), 3, kind='criterion',
          note_sel=S('Cowslips must be at the bottom'))], 'bio-3-1', 'drawing-a-pyramid-of-numbers',
      SQ(13, 'Draw a pyramid of numbers:'), 6, qfig='q11a-i-question', fig='q11a-i-scheme',
      id='bio-2021-hl-q11-a-i',
      decision='The scheme marks the shape on its drawings (any of the three) and the organisms on a row; its '
               'drawings are the solution figure. The food chain\'s arrows are drawn, not in the text layer: the '
               'question is shown as printed.'),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Give one limitation of the use of pyramids of numbers in ecology.'),
      [pt(S('Does not take size (or mass) of organisms into account', 'cannot be estimated'), 3)], 'bio-3-1',
      'limits-of-pyramids', SQ(13, 'Give one limitation with the use of pyramid of numbers:'), 3,
      id='bio-2021-hl-q11-a-ii'),
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Suggest one advantage of females giving birth in early summer and not in spring.'),
      [pt(S('More (insects) food (for bats to feed offspring)', 'other relevant point'), 3)], 'bio-3-1',
      'timing-of-births', SQ(13, 'Suggest one advantage of females giving birth'), 3, stem=Q11B,
      id='bio-2021-hl-q11-b-i'),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Name and explain one human activity that impacts on Irish bat populations.'),
      [pt(S('Development (building or disruption) or (use of) pesticides or other', 'conservation practice'), 3,
          label=S('Name:')),
       pt(S('Development: (Decreases', 'conservation activity explained'), 3, whole=True, label=S('Explain:'))],
      'bio-3-1', 'human-impact-on-bats', SQ(13, 'Name and explain one human activity'), 6, stem=Q11B,
      id='bio-2021-hl-q11-b-ii'),
    T('11biii', 'Q11(b)(iii)', 'C', [_C(2, 'A bat and an insect are involved in a predator'),
                                     _C(2, 'Sketch and fully label a predator', 'species fluctuate.')],
      [pt(S('Time on horizontal axis and Population (number) on vertical axis'), 3, kind='criterion',
          label=S('Axes:')),
       pt(S('Two curves with indication of a repeating cycle'), 3, kind='criterion', label=S('Graph:')),
       pt(S('Bat (predator) showing lower peaks and predator curve showing time lag'), 3, kind='criterion')],
      'bio-3-1', 'predator-prey-graph', SQ(13, 'Sketch and label a predator-prey relationship graph:'), 9, stem=Q11B,
      id='bio-2021-hl-q11-b-iii'),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'Name one type of adaptation necessary for organisms to survive.'),
      [pt(S('Structural or behavioural or competitive'), 3)], 'bio-3-1', 'types-of-adaptation',
      SQ(13, 'Name one type of adaptation necessary'), 3, stem=Q11B, id='bio-2021-hl-q11-b-iv'),
    T('11bv', 'Q11(b)(v)', 'C', _C(2, 'From the text, or otherwise, give two adaptations that bats possess.'),
      [anyn(S('Hibernate / nocturnal / sleep upside down / varied diet / can fly / use', 'any valid example'), 2, 3)],
      'bio-3-1', 'bat-adaptations', SQ(13, 'Give two adaptations that bats possess:'), 6, stem=Q11B,
      id='bio-2021-hl-q11-b-v'),
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'What is meant by the conservation of species?'),
      [pt(S('Management (or preservation or protection) of organisms', 'ecosystems)'), 3)], 'bio-3-1',
      'conservation', SQ(14, 'What is meant by the conservation of species?'), 3, id='bio-2021-hl-q11-c-i'),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Name and describe one conservation practice from agriculture', 'forestry.'),
      [pt(S('Agriculture: Mixed farming', 'Any valid example'), 3, whole=True),
       pt(S('Practice correctly described or expansion point given'), 3, kind='criterion')], 'bio-3-1',
      'conservation-practice', SQ(14, 'Name and describe one conservation practice'), 6, id='bio-2021-hl-q11-c-ii',
      decision='"Agriculture or fisheries or forestry": the scheme marks every area on one named-practice row and '
               'one description row; one card.'),
    T('11ciii1', 'Q11(c)(iii)1', 'C', item(2, 1, 'Suggest one advantage of carrying out these surveys.',
                                         'Ecologists monitor or survey'),
      [pt(S('Monitor (or investigate) changes or biodiversity', 'extinction'), 3)], 'bio-3-1', 'why-survey',
      SQ(14, '1. Suggest one advantage of carrying out surveys'), 3, stem=[Q11C3], id='bio-2021-hl-q11-c-iii-1'),
    T('11ciii2', 'Q11(c)(iii)2', 'C', item(2, 2, 'species in the ecosystem you have studied.',
                                         'Ecologists monitor or survey'),
      [pt(S('Named animal'), 3, kind='criterion', note_sel=S('Animal must match method below')),
       anyn(S('Captured (or how captured) /', 'formula (or calculation) described'), 3, 3)], 'bio-3-1',
      'estimating-animal-populations', SQ(14, '2. Describe the steps taken to estimate the population'), 12,
      stem=[Q11C3], id='bio-2021-hl-q11-c-iii-2',
      decision='The scheme prints two step lists, for moving and for sessile or slow-moving animals, either '
               'matched to the named animal: answer variants of one task.'),
    T('12ai', 'Q12(a)(i)', 'C', _C(3, 'State two agents that can cause mutations.'),
      [anyn(S('Chemicals or named chemical / radiation or UV or X-ray / biological agent (or', 'named)'), 2, 3)],
      'bio-2-3', 'mutagens', SQ(15, 'State two agents that can be responsible for mutation rates:'), 6,
      id='bio-2021-hl-q12-a-i'),
    T('12aii', 'Q12(a)(ii)', 'C', _C(3, 'Identify one characteristic of mutant alleles in a population.'),
      [pt(S('Random occurrence or low frequency or disadvantageous or advantageous'), 3)], 'bio-2-3',
      'mutant-alleles', SQ(15, 'Identify one characteristic of mutant alleles'), 3, id='bio-2021-hl-q12-a-ii'),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'Write the genotype of a plant heterozygous for both traits.'),
      [pt(S('*RrYy'), 3)], 'bio-1-4', 'dihybrid-genotype', SQ(15, 'Write the genotype of a plant heterozygous'), 3,
      stem=Q12B, id='bio-2021-hl-q12-b-i'),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'What are the possible gametes produced by this plant at part (i) above?'),
      [pt(S('*RY / *Ry / *rY / *ry'), 6, kind='criterion', units=[3, 3],
          note_sel=S('Any two = 3 marks; final 2 for further 3 marks'))], 'bio-1-4', 'dihybrid-gametes',
      SQ(15, 'What are the possible gametes produced by this plant?'), 6, stem=Q12B + Q12BI,
      id='bio-2021-hl-q12-b-ii',
      decision='"Any two = 3 marks; final 2 for further 3 marks": one row of two 3-mark units.'),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'How does the production of these gametes at part (ii) above demonstrate',
                                       '(independent assortment)?'),
      [pt(S('R or r can combine with either Y or y', '(at gamete formation)'), 3)], 'bio-1-4',
      'independent-assortment', SQ(15, 'How do these gametes demonstrate Mendel’s second law?'), 3, stem=Q12B,
      id='bio-2021-hl-q12-b-iii'),
    T('12biv', 'Q12(b)(iv)', 'C', [_C(3, 'The plant at part (i) above was crossed', 'seed shape and seed colour.'),
                                   _C(3, 'Show using a Punnet square how the following results were obtained.')],
      [pt(S('Punnet square'), 3, kind='criterion'), pt(S('Gametes of the other parent: *ry'), 3),
       pt(S('*RrYy : Rryy : rrYy : rryy'), 3, label=S('Genotypes of offspring:'),
          note_sel=S('Must be in a 1:1:1:1 ratio'))], 'bio-1-4', 'dihybrid-test-cross',
      SQ(15, 'Show using a Punnet square how these results were obtained:'), 9, stem=Q12B + Q12BI,
      qfig='q12b-iv-question', id='bio-2021-hl-q12-b-iv',
      decision='The results to explain are printed as a table: the question is shown as printed.'),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'Identify the genotypes of the offspring that introduce variation', 'part (iv) above.'),
      [pt(S('*Rryy'), 3), pt(S('*rrYy'), 3)], 'bio-1-4', 'recombinant-offspring',
      SQ(15, 'Identify the genotypes of the offspring that introduce variation'), 6, stem=Q12B,
      id='bio-2021-hl-q12-b-v'),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'Explain the three underlined terms.'),
      [pt(S('Unit of inheritance or piece of DNA that codes for a protein'), 3, label=S('Gene:')),
       pt(S('Gene located on the sex (or X or Y) chromosome'), 3, label=S('Sex-linked:')),
       pt(S('Genetic engineering: (Artificial) manipulation (or alteration) of genes'), 3)], 'bio-1-4',
      'gene-sex-linkage-genetic-engineering', SQ(15, 'Explain the meaning of:',
                                                  paired='The (c)(i) under the scheme\'s Question 12: its rows name the '
                                                         'three underlined terms.'), 9, stem=[Q12C],
      qfig='q12c-i-question', id='bio-2021-hl-q12-c-i',
      decision='One printed ask naming three underlined terms, each priced: one card, a row per term. The paper '
               'marks the terms by underlining them: the question is shown as printed.'),
] + [
    T(f'12cii{n}', f'Q12(c)(ii){n}', 'C', item(3, n, step, 'Outline what happens in each'), rows, 'bio-3-3', concept,
      SQ(15, 'Outline what happens in each of the following steps'), 3, stem=[Q12C, Q12CII],
      id='bio-2021-hl-q12-c-ii' if n == 1 else None,
      decision=('The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, step, rows, concept in [
        (1, 'Isolation', [pt(S('Removing (a piece of) DNA (or gene or plasmid) from a cell'), 3)], 'isolation'),
        (2, 'Cutting', [pt(S('DNA (or plasmid) is cut using (restriction) enzymes or gene is',
                             'cut out using (restriction) enzymes'), 3)], 'cutting'),
        (3, 'Gene expression.', [pt(S('Production of protein'), 3)], 'gene-expression')]
] + [
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Give one application of genetic engineering in animals', 'haemophilia.'),
      [pt(S('Any valid example'), 3, kind='criterion')], 'bio-3-3', 'genetic-engineering-in-animals',
      SQ(15, 'Give one application in animals:'), 3, stem=[Q12C]),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Give one application of genetic engineering in plants.'),
      [pt(S('Any valid example'), 3, kind='criterion')], 'bio-3-3', 'genetic-engineering-in-plants',
      SQ(15, 'Give one application in plants:'), 3, stem=[Q12C]),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Define metabolism.'),
      [pt(S('All the chemical reactions in a cell (or organism or in the body)'), 3)], 'bio-1-1', 'metabolism',
      SQ(16, 'Define metabolism:'), 3, id='bio-2021-hl-q13-a-i'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Write a balanced chemical equation for aerobic respiration.'),
      [pt(S('All chemical formulae correct'), 3, kind='criterion',
          note='The scheme\'s equation is shown after reveal.'),
       pt(S('Correctly balanced'), 3, kind='criterion')], 'bio-2-2', 'respiration-equation',
      SQ(16, 'Write a balanced chemical equation for aerobic respiration:'), 6, fig='q13a-ii-scheme',
      id='bio-2021-hl-q13-a-ii',
      decision='The scheme prints the equation with subscripted formulae, which the text layer flattens: its '
               'equation is the solution figure and its two criteria are the rows.'),
] + [
    T(f'13b{r}', f'Q13(b)({r})', 'C', _C(4, ask, aend), rows, 'bio-2-2', concept, SQ(16, sq), total, stem=[Q13B],
      fig='q13-respiration', id=f'bio-2021-hl-q13-b-{r}')
    for r, ask, aend, rows, concept, sq, total in [
        ('i', 'What name is given to stage 1 as shown on the diagram?', None, [pt(S('*Glycolysis'), 3)],
         'glycolysis', 'Give the name of stage 1:', 3),
        ('ii', 'Identify molecule V which is released during stage 1.', None,
         [pt(S('ATP (adenosine triphosphate) or NADH'), 3)], 'molecule-v', 'Identify molecule V:', 3),
        ('iii', 'Describe how molecule V is made.', None,
         [pt(S('If ATP: ADP + P', 'and (2) electrons'), 3, whole=True)], 'making-atp-or-nadh',
         'Explain how this molecule V is made:', 3),
        ('iv', 'Name the 3', 'formed in stage 1.', [pt(S('*Pyruvic acid (or pyruvate)'), 3)], 'pyruvate',
         'Name the 3-carbon molecule formed in stage 1:', 3),
        ('v', 'Identify organelle W.', None, [pt(S('*Mitochondrion'), 3)], 'mitochondrion', 'Identify organelle W:',
         3),
        ('vi', 'Name the 2', 'molecule X.', [pt(S('*Acetyl (co-enzyme A)'), 3)], 'acetyl-coa',
         'Name the 2-carbon molecule X:', 3),
        ('vii', 'Name the series of events represented by Y.', None, [pt(S('*Krebs’ cycle'), 3)], 'krebs-cycle',
         'Name the series of events represented by Y:', 3),
        ('viii', 'What substance is represented by the letter Z in the diagram?', None,
         [pt(S('*Lactic acid (or lactate)'), 3)], 'lactic-acid', 'What substance is represented by the letter Z', 3),
        ('ix', 'Using your knowledge of respiration, compare the amount of energy released',
         'when oxygen is used and not used.',
         [pt(S('When O2 is used: high energy', 'low levels of ATP (released)'), 3, whole=True)],
         'energy-with-and-without-oxygen', 'Amount of energy released when oxygen is used', 3)]
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', _C(4, ask, aend), rows, 'bio-2-2', concept, SQ(17, sq), total, stem=[Q13C],
      id=f'bio-2021-hl-q13-c-{r}')
    for r, ask, aend, rows, concept, sq, total in [
        ('i', 'Name the cell organelle which contains chlorophyll.', None, [pt(S('*Chloroplast'), 3)], 'chloroplast',
         'Name the cell organelle which contains chlorophyll:', 3),
        ('ii', 'What is the function of chlorophyll in plants?', None, [pt(S('To absorb (or trap) light (energy)'), 3)],
         'role-of-chlorophyll', 'What is the function of chlorophyll in plants?', 3),
        ('iii', 'Suggest why it is an advantage that chlorophyll contains a number of chemicals', 'rather than just one.',
         [pt(S('Absorb (or trap) more energy', 'wavelengths)'), 3)], 'mixed-pigments',
         'Suggest why it is an advantage that chlorophyll contains', 3),
        ('iv', 'Outline the events of the dark stage of photosynthesis.', None,
         [anyn(S('Energy from ATP /', 'to form glucose (or carbohydrate)'), 3, 3)], 'dark-stage',
         'Outline the events of the dark stage of photosynthesis:', 9),
        ('v', 'Explain how the dark stage is necessary for the continuation of the light stage.', None,
         [pt(S('Product(s) (or named product(s)) of dark stage is used in the light stage'), 3)],
         'dark-stage-feeds-light-stage', 'Explain how the dark stage is necessary', 3),
        ('vi', 'Using your knowledge of chlorophyll and photosynthesis, describe one way to',
         'increase plant production in a greenhouse.',
         [pt(S('Heat to (or keep at) optimum temperature', 'described'), 3)], 'greenhouse-production',
         'Describe one way to increase plant production in a greenhouse:', 3)]
] + [
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'What is meant by the term digestion?'),
      [pt(S('The breakdown of food'), 3)], 'bio-2-6', 'digestion', SQ(18, 'What is meant by the term digestion?'), 3,
      id='bio-2021-hl-q14-a-i'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Why is digestion necessary in humans?'),
      [pt(S('To make nutrients (or food) soluble', 'transport of nutrients (or food)'), 3)], 'bio-2-6',
      'why-digest', SQ(18, 'Why is digestion necessary in humans?'), 3, id='bio-2021-hl-q14-a-ii'),
    T('14aiii', 'Q14(a)(iii)', 'C', _C(5, 'What name is given to the removal of undigested wastes from the human body?'),
      [pt(S('*Egestion'), 3)], 'bio-2-6', 'egestion', SQ(18, 'What name is given to the removal of undigested'), 3,
      id='bio-2021-hl-q14-a-iii'),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Give the precise location where villi are', 'most abundant.'),
      [pt(S('Small intestine or ileum or duodenum or jejunum'), 3)], 'bio-2-6', 'where-villi-are',
      SQ(18, 'Give the precise location in the where these villi are most abundant?'), 3, stem=[Q14B],
      fig='q14-villus', id='bio-2021-hl-q14-b-i-fig'),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'What is the main function of villi?'),
      [pt(S('To increase surface area or for absorption (of nutrients)'), 3)], 'bio-2-6', 'role-of-villi',
      SQ(18, 'What is the main function of villi'), 3, stem=[Q14B], fig='q14-villus', id='bio-2021-hl-q14-b-ii'),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'Name the part labelled X and state its role.'),
      [pt(S('*Lacteal'), 3, label=S('Name:')), pt(S('To absorb (digested) fats (or fatty acids)'), 3,
                                                  label=S('Role:'))], 'bio-2-6', 'lacteal',
      SQ(18, 'Name the part labelled X and state its role:'), 6, stem=[Q14B], fig='q14-villus', labels=L_VILLUS,
      id='bio-2021-hl-q14-b-iii-fig'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Name the blood vessel that carries', 'system.', after='(iv)'),
      [pt(S('*Hepatic portal vein'), 3)], 'bio-2-6', 'hepatic-portal-vein',
      SQ(18, 'Name the blood vessel that carries the digested nutrients:'), 3, stem=[Q14B], fig='q14-villus',
      id='bio-2021-hl-q14-b-iv'),
    T('14bv', 'Q14(b)(v)', 'C', _C(5, 'To what organ in the body are digested', 'first transported?'),
      [pt(S('*Liver'), 3)], 'bio-2-6', 'liver', SQ(18, 'To what organ in the body are these nutrients'), 3,
      stem=[Q14B], fig='q14-villus', id='bio-2021-hl-q14-b-v'),
    T('14bvi', 'Q14(b)(vi)', 'C', _C(5, 'Give one function of the organ you named', 'nutrients.', after='(vi)'),
      [pt(S('Detoxification or produces bile', 'any other valid function'), 3)], 'bio-2-6', 'functions-of-the-liver',
      SQ(18, 'Give one other function of the liver other than storage:'), 3,
      stem=[Q14B, M('(v)', 5), _C(5, 'To what organ in the body are digested', 'first transported?')],
      fig='q14-villus', id='bio-2021-hl-q14-b-vi'),
    T('14bvii', 'Q14(b)(vii)', 'C', _C(5, 'Name and explain the process of how food', 'digestive system.'),
      [pt(S('*Peristalsis'), 3, label=S('Name:')), pt(S('Explain: Muscular contractions'), 3)], 'bio-2-6',
      'peristalsis', SQ(18, 'Name the process and explain how food is moved'), 6, stem=[Q14B],
      fig='q14-villus', id='bio-2021-hl-q14-b-vii'),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'Which of the three plants would you expect to show the lowest rate of',
                                   'Explain your answer.'),
      [pt(S('*B'), 3), pt(S('Lowest number (or density) of stomata'), 3)], 'bio-2-6', 'stomatal-density',
      SQ(19, 'Which plant would you expect to show the lowest rate of transpiration?'), 6, stem=[Q14C],
      fig='q14c-table', id='bio-2021-hl-q14-c-i',
      decision='The stomatal-density sentence prints "mm2" with a superscript the text layer flattens: it is '
               'shown in the figure with its table, not lifted into the stem.'),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Indicate two other ways plants use to control transpiration.'),
      [anyn(S('Waxy cuticle / action of stomata / location of stomata / any other valid methods'), 2, 3)], 'bio-2-6',
      'controlling-transpiration', SQ(19, 'Indicate two other methods plants use'), 6, stem=[Q14C],
      id='bio-2021-hl-q14-c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Give two structural differences between xylem and phloem.'),
      [anyn(S('Xylem has pits and phloem does not /', 'Xylem has vessels or tracheids and phloem does not'), 2, 3)],
      'bio-2-6', 'xylem-and-phloem', SQ(19, 'Give two structural differences between xylem and phloem:'), 6,
      stem=[Q14C, Q14CIII], id='bio-2021-hl-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'Draw and label a longitudinal section (L.S.) of a xylem vessel.'),
      [pt(S('Continuous vessel(s) with lignin or pits'), 3, kind='criterion', label=S('Drawing:')),
       anyn(S('Pits / lignin / wall'), 3, 1)], 'bio-2-6', 'drawing-xylem',
      SQ(19, 'Draw and label a detailed longitudinal section'), 6, stem=[Q14C, Q14CIII], id='bio-2021-hl-q14-c-iv'),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'Explain the underlined term.'),
      [pt(S('Maintaining a constant (or stable) internal environment'), 3)], 'bio-2-4', 'homeostasis',
      SQ(20, 'Explain homeostasis:'), 3, stem=[Q15A], qfig='q15a-i-question', id='bio-2021-hl-q15-a-i',
      decision='The paper marks the term to explain by underlining it: the question is shown as printed.'),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Name one anatomical and one chemical way plants can protect themselves.'),
      [pt(S('Anatomical: Thorns or stinging hairs or cuticle or any valid example'), 3),
       pt(S('Heat shock proteins or stress proteins', 'any valid example'), 3, label=S('Chemical:'))], 'bio-2-4',
      'plant-defences', SQ(20, 'Name one anatomical and one chemical way'), 6, stem=[Q15A], id='bio-2021-hl-q15-a-ii'),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'Name the structures labelled A, B and C.'),
      [pt(S('*Anther'), 1, label=S('A:')), pt(S('*Filament'), 1, label=S('B:')), pt(S('*Ovary'), 1, label=S('C:'))],
      'bio-2-5', 'parts-of-a-flower', SQ(20, 'Name the structures:'), 3, stem=[Q15B], fig='q15-flower',
      labels=L_FLOWER, id='bio-2021-hl-q15-b-i-fig'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'Is this flower insect or wind', 'pollinated?'),
      [pt(S('*Wind'), 3)], 'bio-2-5', 'wind-pollinated', SQ(20, 'Is this flower insect or wind-pollinated?'), 3,
      stem=[Q15B], fig='q15-flower', id='bio-2021-hl-q15-b-ii-fig'),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Using the diagram, give two reasons to support your answer', 'above.'),
      [anyn(S('Large stigma (or anther) / feathery stigma', 'Letter labels from diagram acceptable'), 2, 3)],
      'bio-2-5', 'signs-of-wind-pollination', SQ(20, 'Using the diagram, give two reasons'), 6,
      stem=[Q15B, M('(ii)', 6), _C(6, 'Is this flower insect or wind', 'pollinated?')], fig='q15-flower',
      id='bio-2021-hl-q15-b-iii-fig',
      decision='The scheme prints its note "Letter labels from diagram acceptable" on the menu\'s last line; it is '
               'kept with that option as printed.'),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'What is the role of each of the parts labelled A and D?'),
      [pt(S('A: Produce pollen or release pollen'), 3), pt(S('D: Trap (or catch) pollen'), 3)], 'bio-2-5',
      'anther-and-stigma-roles', SQ(20, 'What are the roles of A and D?',
                                     paired='The (iv) under the scheme\'s Question 15 (b), reworded.'), 6, stem=[Q15B], fig='q15-flower',
      labels=asked(L_FLOWER), id='bio-2021-hl-q15-b-iv-fig'),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'This flower can exhibit self', 'pollination.', end_nth=2),
      [pt(S('Less (genetic) variation or offspring will be more susceptible to disease'), 3)], 'bio-2-5',
      'self-pollination', SQ(20, 'Give one disadvantage of self-pollination:'), 3, stem=[Q15B],
      fig='q15-flower', id='bio-2021-hl-q15-b-v'),
    T('15bvi1', 'Q15(b)(vi)1', 'C', item(6, 1, 'Which labelled part develops into the fruit?', 'Seed and fruit development'),
      [pt(S('*C (or ovary)'), 3)], 'bio-2-5', 'fruit-from-ovary', SQ(20, '1. Which labelled part develops'), 3,
      stem=[Q15B, Q15BVI], fig='q15-flower', id='bio-2021-hl-q15-b-vi-1-fig'),
    T('15bvi2', 'Q15(b)(vi)2', 'C', item(6, 2, 'Give one way seedless fruits may develop.', 'Seed and fruit development'),
      [pt(S('Spray with growth regulators (auxin) or selective breeding (or described)'), 3)], 'bio-2-5',
      'seedless-fruit', SQ(20, '2. Give one way seedless fruit may develop:'), 3, stem=[Q15B, Q15BVI],
      fig='q15-flower', id='bio-2021-hl-q15-b-vi-2'),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'Explain each of the underlined terms.'),
      [pt(S('Growth of seed (or embryo) into a (new) plant (or named parts of plant)'), 3, label=S('Germination:', after='Question 15 (continued)')),
       pt(S('Carrying (or scattering) of seed away from the parent plant (or described)'), 3, label=S('Dispersal:', after='Question 15 (continued)')),
       pt(S('Period of no growth (or reduced growth or low metabolism or inactivity)'), 3, label=S('Dormancy:', after='Question 15 (continued)'))],
      'bio-2-5', 'germination-dispersal-dormancy', SQ(21, 'Germination:',
      paired='The (c)(i) under the scheme\'s Question 15: its rows name the three underlined terms.'), 9, stem=[Q15C], qfig='q15c-i-question',
      id='bio-2021-hl-q15-c-i',
      decision='One printed ask naming three underlined terms, each priced: one card, a row per term. The paper '
               'marks the terms by underlining them: the question is shown as printed.'),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Outline how dormancy in seeds benefits plant species.'),
      [pt(S('(Seeds) germinate when conditions are suitable', 'embryo time to mature'), 3)], 'bio-2-5',
      'why-dormancy', SQ(21, 'Outline how dormancy in seeds benefits the plant species:'), 3, stem=[Q15C],
      id='bio-2021-hl-q15-c-ii'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Give two roles of water in the process of germination.'),
      [anyn(S('Soften (or split) testa (seed coat) /', 'dissipate inhibitors'), 2, 3)], 'bio-2-5',
      'water-in-germination', SQ(21, 'Give two roles of water in the process of germination:'), 6, stem=[Q15C],
      id='bio-2021-hl-q15-c-iii'),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Identify two possible food stores in seeds.'),
      [pt(S('Cotyledon (or seed leaf)'), 3), pt(S('Endosperm'), 3)], 'bio-2-5', 'food-stores-in-seeds',
      SQ(21, 'Identify two possible food stores in seeds:'), 6, stem=[Q15C], id='bio-2021-hl-q15-c-iv'),
    # Q16 -------------------------------------------------------------------
    T('16ai', 'Q16(a)(i)', 'C', _C(7, 'Which labelled structure is involved in vasoconstriction?'),
      [pt(S('*B (or arteriole)'), 3)], 'bio-2-4', 'arterioles', SQ(22, 'Which labelled structure is involved in '
                                                                       'vasoconstriction?'), 3,
      stem=[Q16A], fig='q16-skin', id='bio-2021-hl-q16-a-i-fig'),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'Describe in detail the role of vasoconstriction in temperature regulation.'),
      [anyn(S('In cold conditions / arterioles (or blood vessels) narrow', 'heat lost or more heat retained'), 3, 3)],
      'bio-2-4', 'vasoconstriction', SQ(22, 'Explain the role of vasoconstriction'), 9, stem=[Q16A],
      fig='q16-skin', id='bio-2021-hl-q16-a-ii'),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'Which labelled structure is involved in piloerection?'),
      [pt(S('*A (or hair)'), 3)], 'bio-2-4', 'piloerection', SQ(22, 'Which labelled structure is involved in '
                                                                    'piloerection?'), 3,
      stem=[Q16A], fig='q16-skin', id='bio-2021-hl-q16-a-iii-fig'),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'Which labelled structure is involved in both excretion and temperature',
                                     'regulation?'),
      [pt(S('*C (or sweat gland)'), 3)], 'bio-2-6', 'sweat-gland', SQ(22, 'Which labelled structure is involved in '
                                                                         'both'), 3,
      stem=[Q16A], fig='q16-skin', id='bio-2021-hl-q16-a-iv-fig'),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'Name the excretory product produced by the structure stated at part (iv) above.'),
      [pt(S('Sweat (or two named components)'), 3)], 'bio-2-6', 'sweat', SQ(22, 'Name the excretory product'), 3,
      stem=[Q16A] + Q16AIV, fig='q16-skin', id='bio-2021-hl-q16-a-v-fig'),
    T('16avi', 'Q16(a)(vi)', 'C', _C(7, 'Humans can generate their own heat', 'given to such organisms?'),
      [pt(S('*Endotherm'), 3)], 'bio-2-4', 'endotherms', SQ(22, 'Name given to organisms that can generate'), 3,
      stem=[Q16A], fig='q16-skin', id='bio-2021-hl-q16-a-vi'),
    T('16avii', 'Q16(a)(vii)', 'C', _C(7, 'Name two other systems in which the skin has a role.'),
      [pt(S('Nervous (or sensory)'), 3), pt(S('Defence (or immune)'), 3)], 'bio-2-4', 'roles-of-the-skin',
      SQ(22, 'Name two other systems in which the skin has a role:'), 6, stem=[Q16A], fig='q16-skin', id='bio-2021-hl-q16-a-vii'),
    T('16bi', 'Q16(b)(i)', 'C', [_C(7, 'Draw a large diagram of the reproductive system of the human male.'),
                                 _C(7, 'Label the following parts:'), _C(7, 'Testis', br=True),
                                 _C(7, 'Sperm', 'duct'), _C(7, 'Prostate', 'gland'), _C(7, 'Urethra'),
                                 _C(7, 'Penis'), _C(7, 'Scrotum')],
      [pt(S('Diagram: Penis and urethra and sperm duct and testis', after='Question 16 (b)'), 6, kind='criterion', units=[3, 3],
          note_sel=S('Any one missing only 3 marks')),
       anyn(S('Testis / sperm duct / prostate gland / urethra / penis / scrotum'), 6, 1)], 'bio-2-5',
      'drawing-the-male-system', SQ(22, 'Diagram: Penis and urethra and sperm duct and testis'), 12,
      id='bio-2021-hl-q16-b-i',
      decision='"3 + 3" for the drawing (all four parts; only 3 with any one missing) and "6(1)" for the labels.'),
] + [
    T(f'16bii{n}', f'Q16(b)(ii){n}', 'C', item(7, n, head, 'Describe the differences between the human male'),
      [pt(S(*ans), 3)], 'bio-2-5', concept, SQ(22, 'Give the differences between the human male and female gametes'),
      3, stem=[Q16BII], id='bio-2021-hl-q16-b-ii' if n == 1 else None,
      decision=('The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, head, ans, concept in [
        (1, 'Relative numbers of each produced', ('A low number of female gametes (or eggs) and a high number of male',
                                                  'gametes (or sperm)'), 'numbers-of-gametes'),
        (2, 'Frequency of production of gametes', ('Monthly (or from puberty to menopause) in females and continuously',
                                                   'in males'), 'frequency-of-gamete-production'),
        (3, 'Relative size.', ('Large in females (or egg is large) and small in males (or sperm are small)',),
         'size-of-gametes')]
] + [
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'What is meant by secondary sexual characteristics?'),
      [pt(S('Features that distinguish male from female other than sex organs', 'puberty'), 3)], 'bio-2-5',
      'secondary-sexual-characteristics', SQ(22, 'What is meant by secondary sexual characteristics?'), 3,
      id='bio-2021-hl-q16-b-iii'),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'Name the hormone responsible for the development of male', 'characteristics.'),
      [pt(S('*Testosterone'), 3)], 'bio-2-5', 'testosterone', SQ(22, 'Name the hormone responsible for male secondary'),
      3, id='bio-2021-hl-q16-b-iv'),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'Give one cause of male infertility.'),
      [pt(S('Low sperm count or low sperm motility or hormonal'), 3)], 'bio-2-5', 'male-infertility',
      SQ(22, 'Give one cause of male infertility:'), 3, id='bio-2021-hl-q16-b-v'),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'Mucous membrane linings produce mucus', 'linings are found.'),
      [anyn(S('Respiratory tract / digestive tract / reproductive tract / any correct examples'), 2, 3)], 'bio-2-4',
      'mucous-membranes', SQ(23, 'Name two places in the body where mucous membrane linings are found:'), 6,
      stem=[Q16C], id='bio-2021-hl-q16-c-i'),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Give the precise location in the body where lymphocytes are produced.'),
      [pt(S('*(Red) bone marrow'), 3)], 'bio-2-4', 'where-lymphocytes-form',
      SQ(23, 'Give precise location where lymphocytes are produced:'), 3, stem=[Q16C], id='bio-2021-hl-q16-c-ii'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Identify the specific type of lymphocyte that produces antibodies.'),
      [pt(S('*B (lymphocytes)'), 3)], 'bio-2-4', 'b-lymphocytes',
      SQ(23, 'Identify the particular type of white blood cell that produces antibodies:',
         paired='The (iii) under the scheme\'s Question 16 (c): it reprints the paper\'s "type of lymphocyte" as '
                '"type of white blood cell".'), 3, stem=[Q16C], id='bio-2021-hl-q16-c-iii'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Identify one type of white blood cell, other than lymphocytes', 'response.'),
      [pt(S('Monocyte or macrophage or phagocyte (phagocytic) or other correctly named WBC'), 3)], 'bio-2-4',
      'other-white-blood-cells', SQ(23, 'Identify one other type of white blood cell:'), 3, stem=[Q16C],
      id='bio-2021-hl-q16-c-iv'),
    T('16cv1', 'Q16(c)(v)1', 'C', item(8, 1, 'infected with the virus at B.', 'The graph below shows'),
      [pt(S('(Antibody response) is slow after vaccine (or A) and fast after infection (or B)'), 3),
       pt(S('Number (of antibodies) produced is low after vaccine (or A) and high after', 'infection (or B)'), 3)],
      'bio-2-4', 'vaccine-and-infection-responses', SQ(23, '1. Compare the antibody response'), 6,
      stem=[Q16C, Q16CV], fig='q16c-graph', id='bio-2021-hl-q16-c-v-1-fig'),
    T('16cv2', 'Q16(c)(v)2', 'C', item(8, 2, 'Suggest a reason for your answer at part 1. above.', 'The graph below shows'),
      [pt(S('After A, 1st time infected (or described) or no memory cells (present)', 'After B, memory cells present'),
          3)], 'bio-2-4', 'memory-cells', SQ(23, '2. Suggest a reason for this:'), 3,
      stem=[Q16C, Q16CV, M('1.', 8), _C(8, 'Using the information from the graph', 'infected with the virus at B.')],
      fig='q16c-graph', id='bio-2021-hl-q16-c-v-2-fig'),
    T('16cvi', 'Q16(c)(vi)', 'C', _C(8, 'Identify the part of the virus that is recognised by antibodies.'),
      [pt(S('Protein (coat) or capsid or antigen'), 3)], 'bio-2-4', 'antigens',
      SQ(23, 'Identify the part of the virus that is recognised by antibodies:'), 3, stem=[Q16C],
      id='bio-2021-hl-q16-c-vi'),
    T('16cvii', 'Q16(c)(vii)', 'C', _C(8, 'Explain why antibiotics are not prescribed to cure COVID'),
      [pt(S('Antibiotics have no effect against viruses or antibiotics only kill bacteria'), 3)], 'bio-2-4',
      'antibiotics-and-viruses', SQ(23, 'Explain why an antibiotic is not prescribed'), 3, stem=[Q16C],
      id='bio-2021-hl-q16-c-vii'),
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'Name the structures located at the end of the breathing tract', 'exchange.'),
      [pt(S('*Alveoli'), 3)], 'bio-2-6', 'alveoli', SQ(23, 'Name the structures involved in gaseous exchange:'), 3,
      id='bio-2021-hl-q16-d-i'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'State two adaptations of the structures named at part (i) above',
                                     'efficiency of gaseous exchange.'),
      [anyn(S('Large surface area / rich (blood) capillary supply / moist surface / membranes',
              'walls one cell thick'), 2, 3)], 'bio-2-6', 'adaptations-of-alveoli',
      SQ(23, 'State two adaptations of these structures'), 6,
      stem=[M('(i)', 8), _C(8, 'Name the structures located at the end of the breathing tract', 'exchange.')],
      id='bio-2021-hl-q16-d-ii'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Identify the gas, soluble in blood plasma, which controls the rate of breathing.'),
      [pt(S('*Carbon dioxide (CO2)'), 3)], 'bio-2-6', 'carbon-dioxide-controls-breathing',
      SQ(23, 'Identify the gas that controls the rate of breathing:'), 3, id='bio-2021-hl-q16-d-iii'),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Identify the region of the human brain which detects the gas', 'part (iii) above.'),
      [pt(S('*Medulla oblongata'), 3)], 'bio-2-6', 'medulla-oblongata', SQ(23, 'Identify the region of the human brain'),
      3, stem=Q16DIII, id='bio-2021-hl-q16-d-iv'),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'How does the breathing system respond to a high level of the gas named at',
                                   'part (iii) above?'),
      [pt(S('Increases rate or increases depth (of breathing)'), 3)], 'bio-2-6', 'responding-to-carbon-dioxide',
      SQ(23, 'How does the breathing system respond'), 3, stem=Q16DIII, id='bio-2021-hl-q16-d-v'),
    T('16dvi', 'Q16(d)(vi)', 'C', _C(8, 'Describe in detail the process of inhalation.'),
      [anyn(S('Brain sends impulse (message) to muscles /', 'air moves in'), 4, 3)], 'bio-2-6', 'inhalation',
      SQ(23, 'Process of inhalation:'), 12, id='bio-2021-hl-q16-d-vi'),
    # Q17 -------------------------------------------------------------------
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'Name the organism shown in the diagram and the kingdom to which it belongs.'),
      [pt(S('Rhizopus or bread mould'), 3, label=S('Name:', after='Question 17 (a)')), pt(S('*Fungus (fungi)'), 3, label=S('Kingdom:'))],
      'bio-3-2', 'rhizopus', SQ(24, 'Name:', after='Question 17 (a)'), 6, stem=[Q17A], fig='q17-rhizopus',
      id='bio-2021-hl-q17-a-i-fig'),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Name the part labelled A.'),
      [pt(S('*Sporangiophore'), 3)], 'bio-3-2', 'sporangiophore', SQ(24, 'Name the parts labelled A:'), 3,
      stem=[Q17A], fig='q17-rhizopus', labels=[L('A', S('*Sporangiophore', page=24), True)],
      id='bio-2021-hl-q17-a-ii-fig'),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'State the mode of nutrition used by this organism.'),
      [pt(S('*Saprophytic or *heterotrophic'), 3)], 'bio-3-2', 'saprophytic-nutrition',
      SQ(24, 'State the mode of nutrition used by this organism:'), 3, stem=[Q17A], fig='q17-rhizopus', id='bio-2021-hl-q17-a-iii'),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Discuss the importance in nature of the type of nutrition', 'above.'),
      [pt(S('Decomposer or recycles minerals or described'), 3)], 'bio-3-2', 'decomposition',
      SQ(24, 'Discuss the importance of this type of nutrition in nature:'), 3, stem=[Q17A] + Q17AIII,
      fig='q17-rhizopus', id='bio-2021-hl-q17-a-iv'),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'Name the horizontal hyphae labelled B and state their role.'),
      [pt(S('*Stolons'), 3, label=S('Name:')), pt(S('Spreading the fungus or asexual reproduction'), 3,
                                                  label=S('State:'))], 'bio-3-2', 'stolons',
      SQ(24, 'Name the horizontal hyphae labelled B'), 6, stem=[Q17A], fig='q17-rhizopus',
      labels=[L('B', S('*Stolons', page=24), True)], id='bio-2021-hl-q17-a-v-fig'),
    T('17avi', 'Q17(a)(vi)', 'C', _C(9, 'Spores and rhizoids are labelled in the diagram.', 'Give one function of each.'),
      [pt(S('(Asexual) reproduction or dispersal'), 3, label=S('Spores:')),
       pt(S('Rhizoids: Absorption or anchorage or secretion'), 3)], 'bio-3-2', 'spores-and-rhizoids',
      SQ(24, 'Give one function of:'), 6, stem=[Q17A], fig='q17-rhizopus', id='bio-2021-hl-q17-a-vi'),
    T('17avii', 'Q17(a)(vii)', 'C', _C(9, 'Describe one environmental condition which may stimulate sexual reproduction',
                                       'in this organism.'),
      [pt(S('Drought or unsuitable temperature or named adverse condition'), 3)], 'bio-3-2',
      'triggering-sexual-reproduction', SQ(24, 'Describe one environmental condition'), 3, stem=[Q17A],
      fig='q17-rhizopus', id='bio-2021-hl-q17-a-vii'),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'Name the unicellular organism shown in the diagram and the kingdom to which',
                                   'it belongs.'),
      [pt(S('*Amoeba'), 3, label=S('Name:', after='Question 17 (b)')), pt(S('*Protist(a) (or Protoctista)'), 3, label=S('Kingdom:'))],
      'bio-3-2', 'amoeba', SQ(24, 'Name:', after='Question 17 (b)'), 6, stem=[Q17B], fig='q17-amoeba',
      id='bio-2021-hl-q17-b-i-fig'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Suggest a typical habitat for this organism.'),
      [pt(S('(Fresh) water or example (pond, lake, etc.)'), 3)], 'bio-3-1', 'amoeba-habitat',
      SQ(24, 'Suggest a typical habitat for this organism:'), 3, stem=[Q17B], fig='q17-amoeba', id='bio-2021-hl-q17-b-ii'),
    T('17biii', 'Q17(b)(iii)', 'C', [Q17BIII, _C(9, 'Name structure A forming around this prey.')],
      [pt(S('*Pseudopod'), 3)], 'bio-1-3', 'pseudopod', SQ(24, 'Name structure A:'), 3, stem=[Q17B],
      fig='q17-amoeba', id='bio-2021-hl-q17-b-iii-fig'),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'Give one function for structure A named at part (iii) above', 'prey.'),
      [pt(S('*Movement'), 3)], 'bio-1-3', 'role-of-pseudopods', SQ(24, 'Give one function for this structure'), 3,
      stem=[Q17B, M('(iii)', 9), Q17BIII, _C(9, 'Name structure A forming around this prey.')], fig='q17-amoeba',
      id='bio-2021-hl-q17-b-iv-fig'),
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'Name the structure labelled B and state its function.'),
      [pt(S('*Contractile vacuole'), 3), pt(S('Osmoregulation or get rid of excess water (or explained)'), 3,
                                            label=S('Function of part B:'))], 'bio-1-3', 'contractile-vacuole',
      SQ(24, 'Name the structure labelled B:'), 6, stem=[Q17B], fig='q17-amoeba', labels=L_AMOEBA_B,
      id='bio-2021-hl-q17-b-v-fig'),
    T('17bvi', 'Q17(b)(vi)', 'C', _C(9, 'Name the structure labelled C.'),
      [pt(S('*Food vacuole'), 3)], 'bio-1-3', 'food-vacuole', SQ(24, 'Name structure C:'), 3, stem=[Q17B],
      fig='q17-amoeba', labels=L_AMOEBA_C, id='bio-2021-hl-q17-b-vi-fig'),
    T('17bvii', 'Q17(b)(vii)', 'C', _C(9, 'Describe two ways in which the cell of this organism differs', 'bacterial cell.'),
      [anyn(S('Amoeba is eukaryotic and bacteria are prokaryotic /', 'Bacteria can have capsule and Amoeba does not'),
            2, 3)], 'bio-1-3', 'amoeba-and-bacteria', SQ(24, 'Describe two ways the cell of this organism differs'), 6,
      stem=[Q17B], fig='q17-amoeba', id='bio-2021-hl-q17-b-vii'),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'Name the tissue labelled X which covers and protects the spinal cord.'),
      [pt(S('X: *Meninges'), 3)], 'bio-2-4', 'meninges', SQ(25, 'Name the tissue labelled X:'), 3, stem=[Q17C],
      fig='q17-spinal-cord', labels=L_SPINAL, id='bio-2021-hl-q17-c-i-fig'),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'What is a reflex action?'),
      [pt(S('Automatic (or involuntary) response to a stimulus'), 3)], 'bio-2-4', 'reflex-action',
      SQ(25, 'What is a reflex action?'), 3, stem=[Q17C], fig='q17-spinal-cord', id='bio-2021-hl-q17-c-ii'),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Give one example of a reflex action in the human body.'),
      [pt(S('Blinking or iris response to light or knee jerk or grasp or startle or any correct example'), 3)],
      'bio-2-4', 'examples-of-reflexes', SQ(25, 'Give an example of a reflex action in the human body:'), 3,
      stem=[Q17C], fig='q17-spinal-cord', id='bio-2021-hl-q17-c-iii'),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Give one advantage of a reflex action.'),
      [pt(S('Protection or fast or involuntary'), 3)], 'bio-2-4', 'why-reflexes',
      SQ(25, 'Give one advantage of a reflex action:'), 3, stem=[Q17C], fig='q17-spinal-cord', id='bio-2021-hl-q17-c-iv'),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'Using the labels from the diagram, describe in detail how a reflex action works.'),
      [anyn(S('Stimulus (or named) detected by receptor /', 'effector reacts'), 4, 3)], 'bio-2-4', 'reflex-arc',
      SQ(25, 'Describe how a reflex action works:'), 12, stem=[Q17C], fig='q17-spinal-cord',
      id='bio-2021-hl-q17-c-v'),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'Give two ways in which a nervous response differs from a hormonal response.'),
      [anyn(S('Nervous response is fast and hormonal response is slow / nervous response is',
              'hormonal response is prolonged'), 2, 3)], 'bio-2-4', 'nervous-and-hormonal-responses',
      SQ(25, 'Give two ways in which a nervous response differs'), 6, stem=[Q17C], fig='q17-spinal-cord', id='bio-2021-hl-q17-c-vi'),
] + [
    T(f'17d{r}', f'Q17(d)({r})', 'C', _C(10, ask, aend), rows, topic, concept,
      sq if isinstance(sq, dict) else SQ(25, sq), total, stem=Q17D,
      fig='q17-onion-cells', id=old)
    for r, ask, aend, rows, topic, concept, sq, total, old in [
        ('i', 'Name the condition which describes the cells shown in A.', None, [pt(S('*Turgid'), 3)], 'bio-2-6',
         'turgid', 'Name of the condition of cells in A:', 3, 'bio-2021-hl-q17-d-i-fig'),
        ('ii', 'Describe how the cells in A maintain this shape.', None,
         [pt(S('Turgor pressure or explained or cell wall'), 3)], 'bio-2-6', 'turgor',
         SQ(25, 'Describe how the cells in image A maintain their current shape:',
            paired='The (ii) under the scheme\'s Question 17 (d), reworded.'), 3, 'bio-2021-hl-q17-d-ii-fig'),
        ('iii', 'Suggest how solution B differs from solution A.', None,
         [pt(S('Solution B has more solute (or example) (than A) or solution B is more concentrated', '(than A)'), 3)],
         'bio-2-6', 'concentrated-solution', 'Suggest how solution B differs from solution A:', 3,
         'bio-2021-hl-q17-d-iii'),
        ('iv', 'Name and describe in detail the process which has occurred to the cells in B.', None,
         [pt(S('Osmosis'), 3),
          pt(S('Describe: Water moved from high water concentration to low water concentration'), 3),
          pt(S('Across the selectively permeable membrane or from the inside of the cell to', 'the outside'), 3)],
         'bio-2-6', 'osmosis', 'Name of process that occurred to cells in B:', 9, 'bio-2021-hl-q17-d-iv'),
        ('v', 'How could these cells in B be restored to the condition shown in A?', None,
         [pt(S('Place in water (with little or no solutes)'), 3)], 'bio-2-6', 'restoring-turgor',
         'How could these cells be restored to the condition A?', 3, 'bio-2021-hl-q17-d-v'),
        ('vi', 'Describe how a knowledge of the process shown in the cells in solution B can be',
         'applied to food production.',
         [pt(S('Can kill bacteria (or fungi or microorganisms) (on food)', 'shelf-life'), 3)], 'bio-2-6',
         'osmosis-and-food-preservation', 'How can knowledge of the process shown in image B', 3,
         'bio-2021-hl-q17-d-vi')]
] + [
    T(f'17dvii{n}', f'Q17(d)(vii){n}', 'C', item(10, n, ask, 'When preparing plant cells for viewing'),
      [pt(S(*ans), 3)], 'bio-1-3', concept, SQ(25, sq), 3, stem=Q17D + [Q17DVII], id=f'bio-2021-hl-q17-d-vii-{n}')
    for n, ask, ans, concept, sq in [
        (1, 'Outline how a scientist uses a coverslip.', ('Lowered slowly or lowered at an angle or lowered with a needle',),
         'lowering-a-coverslip', 'Outline how the scientist uses a coverslip:'),
        (2, 'Explain why a coverslip is used.', ('Prevent specimen from drying out or to protect the (objective) lens or '
                                                 'to hold', 'specimen in place'),
         'why-a-coverslip', 'Explain why a coverslip is used:')]
]

ANSWER_VARIANTS = {
    '11ciii2': [
        ('moving-animals', 'For moving animals',
         [pt(S('Named animal'), 3, kind='criterion', note_sel=S('Animal must match method below')),
          anyn(S('Captured (or how captured) /', 'formula (or calculation) described'), 3, 3)]),
        ('sessile-animals', 'Steps for sessile or slow-moving animals',
         [pt(S('Named animal'), 3, kind='criterion', note_sel=S('Animal must match method below')),
          anyn(S('Quadrat /', 'calculated population (density)'), 3, 3)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q2-nitrogen-cycle': ('038', 4, (148, 92, 470, 306), SEC, ['A', 'B', 'C'],
                          'Diagram of part of the nitrogen cycle: boxes for Atmospheric nitrogen, Soil nitrates, Pea '
                          'plants, Animals, Soil ammonia and Soil nitrites joined by arrows; arrows labelled A run from '
                          'atmospheric nitrogen to soil nitrates and to the pea plants, the arrow labelled B runs from '
                          'soil nitrites up to atmospheric nitrogen, and arrows labelled C run from soil ammonia to '
                          'soil nitrites and from soil nitrites to soil nitrates.', False),
    'q3-mitosis': ('038', 5, (112, 86, 400, 238), SEC, ['X'],
                   'Drawing of a nucleus during mitosis: fibres run from each pole to the chromosomes, which are being '
                   'drawn apart towards the two poles; arrow X points to the fibres at the top pole, and a label '
                   'Chromosome (sister chromatid) points to one chromosome.', False),
    'q4-enzyme': ('038', 6, (95, 88, 515, 182), SEC, ['A', 'B', 'C'],
                  'Three drawings joined by arrows: an enzyme labelled Enzyme with a small molecule A beside its '
                  'opening; the two fitted together, bracketed B; then the enzyme beside two separate smaller pieces, '
                  'arrows labelled C pointing to them.', False),
    'q5-embryo': ('038', 7, (140, 86, 480, 368), SEC, ['A', 'B', 'C', 'D'],
                  'Drawing of an ovary, fallopian tube and uterus: arrow A points to an egg leaving the ovary, a '
                  'label Fertilisation marks the egg and sperm in the tube with an enlarged view above, arrow B points '
                  'to a small ball of cells further along the tube, arrow C to a hollow ball nearer the uterus, and '
                  'arrow D to the ball attached to the uterus wall with an enlarged view below.', False),
    'q9b-iv-question': ('038', 11, (108, 537, 540, 722), SEC, [],
                        'The printed question: (iv) Label the axes below and draw a curve to show how the rate of '
                        'enzyme activity varies with temperature. Below it, a blank pair of axes.', False),
    'q10-table': ('038', 12, (110, 199, 542, 273), SEC, [],
                  'Table of plates. A: Unopened, 0 colonies. B: 5 leaf discs from an ash tree from a quiet rural '
                  'setting, 10 colonies. C: 5 leaf discs from an ash tree from a busy urban setting, 4 colonies.',
                  False),
    'q11a-i-question': ('040', 2, (80, 115, 545, 160), SEC, [],
                        'The printed question: 11. (a) (i) Draw a pyramid of numbers from the following food chain: '
                        'Cowslips, an arrow, Moth, an arrow, Bat, an arrow, Mites.', False),
    'q11a-i-scheme': ('scheme', 13, (115, 110, 385, 153), SEC, [],
                      "The marking scheme's three accepted pyramid shapes, separated by 'or': each is a stack of four "
                      'bars, the bottom bar narrow with a wide bar above it in the first two and the widest bar at '
                      'the bottom in the third.', True),
    'q12b-iv-question': ('040', 3, (108, 236, 545, 352), SEC, [],
                         'The printed question: (iv) The plant at part (i) above was crossed with a plant homozygous '
                         'recessive for both seed shape and seed colour. Show using a Punnet square how the following '
                         'results were obtained. A table: 115 plants with round yellow seeds, 115 plants with wrinkled '
                         'yellow seeds, 114 plants with round green seeds, 116 plants with wrinkled green seeds.',
                         False),
    'q12c-i-question': ('040', 3, (80, 425, 545, 499), SEC, [],
                        'The printed question: (c) The haemophilia gene (n) is sex-linked and recessive. There is '
                        'currently no cure for haemophilia but recently in trials, genetic engineering has been used '
                        'to transfer a working copy of the human gene to affected people. The words gene, sex-linked '
                        'and genetic engineering are underlined. (i) Explain the three underlined terms.', False),
    'q13a-ii-scheme': ('scheme', 16, (115, 108, 320, 125), SEC, [],
                       "The marking scheme's equation: C6H12O6 + 6O2, an arrow, 6CO2 + 6H2O, with the small numbers "
                       'in the formulae set as subscripts.', True),
    'q13-respiration': ('040', 4, (150, 136, 445, 382), SEC, [],
                        'Flow diagram of respiration: a 6-carbon sugar splits in Stage 1, releasing V on both sides, '
                        'into a 3-carbon molecule. On the left (if O2 not used) it goes to Human muscle cells and then '
                        'Z; on the right (if O2 used) it Enters an organelle W, becomes 2-carbon molecule X and then '
                        'enters a circular series labelled Y.', False),
    'q14-villus': ('040', 5, (360, 155, 545, 416), SEC, ['X'],
                   'Drawing of a longitudinal section of villi: finger-like folds, a label Epithelium pointing to the '
                   'outer layer, arrow X pointing to the central vessel running up inside a villus, and a label Blood '
                   'capillary pointing to the network of vessels around it.', False),
    'q14c-table': ('040', 5, (108, 494, 545, 610), SEC, [],
                   'The printed sentence: The stomatal density (number of stomata per mm², the 2 set as a superscript) '
                   'from the leaves of three different plants was measured and the results shown in the table. The '
                   'table: plant A 43, plant B 28, plant C 68.', False),
    'q15a-i-question': ('040', 6, (80, 58, 545, 108), SEC, [],
                        'The printed question: 15. (a) Organisms can respond to changes in their external and internal '
                        'environment in different ways including through homeostasis. The word homeostasis is '
                        'underlined. (i) Explain the underlined term.', False),
    'q15-flower': ('040', 6, (160, 168, 410, 356), SEC, ['A', 'B', 'C', 'D'],
                   'Drawing of a flower seen from the side: long stalks hang out of the flower with arrow A pointing '
                   'to the tip of one and arrow B to the stalk itself; arrow C points to the base inside the flower and '
                   'arrow D to a feathery structure hanging below it.', False),
    'q15c-i-question': ('040', 6, (80, 543, 545, 585), SEC, [],
                        'The printed question: (c) Germination in seeds follows dispersal and a period of dormancy. '
                        'The words germination, dispersal and dormancy are underlined. (i) Explain each of the '
                        'underlined terms.', False),
    'q16-skin': ('040', 7, (188, 122, 444, 322), SEC, ['A', 'B', 'C'],
                 'Drawing of a block of human skin with hairs: arrow A points to a hair in its follicle, arrow B to a '
                 'looped blood vessel near the surface, and arrow C to a coiled tube deep in the skin.', False),
    'q16c-graph': ('040', 8, (120, 272, 480, 420), SEC, ['A', 'B'],
                   'Graph of relative antibody concentration against time (days): from A the curve rises slowly to a '
                   'small low peak and falls back; from B it rises steeply to a much higher peak before falling.',
                   False),
    'q17-rhizopus': ('040', 9, (212, 92, 418, 262), SEC, ['A', 'B'],
                     'Drawing of a mould: upright stalks end in round heads, with Spores scattering from one; arrow A '
                     'points to one upright stalk, arrows B to the threads running along the surface, and a label '
                     'Rhizoid points to the branched threads below.', False),
    'q17-amoeba': ('040', 9, (165, 425, 495, 568), SEC, ['A', 'B', 'C'],
                   'Drawing of a single-celled organism with an irregular outline: arrow B points to a clear round '
                   'space, a label Nucleus to the dark round body, a bracket A marks extensions of the cell closing '
                   'around a small cell labelled Euglena, and arrow C points to a small space holding a taken-in '
                   'particle.', False),
    'q17-spinal-cord': ('040', 10, (140, 98, 475, 275), SEC, ['X', 'A', 'B', 'C'],
                        'Drawing of a cross section of the spinal cord with neurons: arrow X points to the outer '
                        'covering of the cord; Neuron B runs in from a Receptor, Neuron C lies inside the cord, and '
                        'Neuron A runs out to an Effector.', False),
    'q17-onion-cells': ('040', 10, (112, 445, 512, 570), SEC, ['A', 'B'],
                        'Two micrographs of red onion epidermal cells. A: Epidermal cells in solution A, each filled '
                        'by its dark grey vacuole. B: Epidermal cells in solution B, the dark grey vacuoles shrunk '
                        'into the middle of each cell.', False),
}
