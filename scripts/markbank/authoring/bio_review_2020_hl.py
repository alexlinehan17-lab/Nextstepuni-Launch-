"""Biology 2020 Higher Level — reviewed task ledger, carded from the papers for the first time.

Independent visual sweep (2026-10-13), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover,
    p2 instructions, p3-p8 Section A Questions 1-6, p9-p11 Section B
    Questions 7-9, p12 Section C answerbook instructions, p13-p35 ruled
    answer pages, p36-p39 graph paper, p40 back cover with the copyright
    notice. No acknowledgements page.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p9 Questions 10-15,
    p10-p11 "Do not write on this page", p12 back cover with the copyright
    notice.
  * LC025ALP000EV (marking scheme), 29 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7-p27 Questions
    1-15, p28 blank under the running header, p29 back cover.

The 2020 paper keeps the long-standing shape: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Questions 14 and 15 are each any two of (a), (b), (c). Every printed question
is carded. No Biology card existed for 2020 before this review.

Section A: Q1 is the best five of six parts at 4 ("5(4)"); Q2-Q6 are each
"6(3) + 2" over seven responses, an ordered split carded at 3 a response.
Sections B and C print a mark per row, with 1-mark label rows in Q13(b)(iv),
Q14(c)(i) and Q15(c)(ii).

The Q3 true/false key prints no reprint of the statements: a letter, T or F,
under each part's column header. Each part is read from the column its
header heads, and the task is anchored on that header alone.

One printed choice is marked differently per option and is split into routes:
Q6(f) paralysis or Parkinson's disease, which the scheme answers in two
columns of causes and treatments. Every other choice is marked on shared rows
and is one card ("choice is not a route"): Q8(b)'s starch or skimmed-milk
agar, Q9(b)(iv)'s semilunar valve. Q12(a)(ii) prints Mendel's second law in
two wordings separated by "OR": answer variants of one task.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, allof, T, L

YEAR, LEVEL = 2020, 'hl'
REVIEWED_AT = '2026-10-13'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2020-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': '345f1b98c137a5041458d9676b5a7a57e06f4b5c0b907bffbd08b02e66997dca',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2020-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': '5838f923f9d86219e405f0845a5eb75ae27ab2f8b01fc75c21891868aec38709',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2020-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '0727b8e65364d92e73ef68f73a00d478c57a0dbd701670e013914fc26e6fa9f4',
               'pages': 29},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 12)},
            12: 'answerbook-instructions', **{p: 'answer-pages' for p in range(13, 36)},
            **{p: 'graph-paper' for p in range(36, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 10)}, 10: 'blank', 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', **{p: 'marking' for p in range(7, 28)},
               28: 'blank', 29: 'back-cover'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)},
}
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (7, 8, 9)}, **{(n, 'b'): 24 for n in (7, 8, 9)},
    **{(n, 'a'): 9 for n in range(10, 14)}, **{(n, 'b'): 27 for n in range(10, 14)},
    **{(n, 'c'): 24 for n in range(10, 14)},
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},
}
BEST_OF = {1: (5, 4)}
LADDERS = {q: {'steps': [3, 3, 3, 3, 3, 3, 2], 'notation': '6(3) + 2'} for q in range(2, 7)}

CHECKSUMS = {
    1: {4: 6},   # printed "5(4)": the best five of the six 4-mark parts carded here
    **{q: {3: 7} for q in range(2, 7)},
    **{(n, 'a'): {3: 2} for n in (7, 8, 9)}, **{(n, 'b'): {3: 8} for n in (7, 8, 9)},
    **{(n, 'a'): {3: 3} for n in range(10, 14)},
    **{(n, 'b'): {3: 9} for n in (10, 11, 12)}, (13, 'b'): {3: 7, 1: 6},
    **{(n, 'c'): {3: 8} for n in range(10, 14)},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 9, 1: 3},
    (15, 'a'): {3: 10}, (15, 'b'): {3: 10}, (15, 'c'): {3: 9, 1: 3},
}

SCAN_PAGES = {'038': range(2, 12), '040': range(2, 10)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the best five make 20.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 5, 'the following', 'Q3 lead-in: every statement asked.'),
    ('038', 5, 'or', 'Q3 "true or false": the answer options.'),
    ('038', 7, 'the following', 'Q5 lead-in: every structure asked, one card per lettered part.'),
    ('038', 8, 'or', 'Q6(b) "(or group of substances)": the same ask, not a choice.'),
    ('038', 8, 'choose', 'Q6(f) "Choose either Parkinson\'s disease or paralysis": separate causes and treatments per '
                         'option: ROUTES.'),
    ('038', 8, 'either', 'Q6(f), same choice.'),
    ('038', 8, 'or', 'Q6(f), same choice.'),
    ('038', 9, 'any two', 'Section B rubric repeated.'),
    ('038', 9, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('038', 9, 'or', 'Q7(b) "an enzyme or cell": either form; marked on the same rows.'),
    ('038', 9, 'or', 'Q7(b) "Name the enzyme or cell", same.'),
    ('038', 9, 'or', 'Q7(b)(i) "that enzyme or cell", same.'),
    ('038', 9, 'or', 'Q7(b)(ii) "immobilised enzyme or cell", same.'),
    ('038', 10, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('038', 10, 'or', 'Q8(b) "starch agar or skimmed milk (protein) agar": marked on shared rows ("must match agar '
                      'type"); one card per part.'),
    ('038', 11, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 11, 'or', 'Q9(b) "a sheep\'s or an ox\'s heart": either heart; marked the same.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'or', 'Q10(b) source title "ornamental wonder or ecological menace": passage text.'),
    ('040', 2, 'or', 'Q10(c)(ii)3 "four or five members": description.'),
    ('040', 3, 'or', 'Q11(b)(ii) "A, B or C": the answer options.'),
    ('040', 3, 'the following', 'Q11(c) lead-in: every part asked.'),
    ('040', 4, 'any two', 'Q12(b)(iii) "any two applications": the scheme prints two application rows; one card.'),
    ('040', 4, 'the following', 'Q12(c)(ii) "the following chickens": a reference.'),
    ('040', 5, 'the following', 'Q13(b)(iv) "Label the following parts": all six labels; one card.'),
    ('040', 5, 'the following', 'Q13(c) "The following table": a reference.'),
    ('040', 6, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 6, 'the following', 'Q14(b) lead-in: every part asked.'),
    ('040', 8, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 8, 'or', 'Q15(a)(iv) "agriculture or horticulture": either setting; one menu.'),
    ('040', 9, 'the following', 'Q15(c) lead-in: every part asked.'),
    ('040', 9, 'any three', 'Q15(c)(ii) "any three zones": a bounded menu on one card.'),
]

ROUTES = {'Q6(f)': ['paralysis', 'parkinsons-disease']}

LAYOUT_CHECKS = [
    ('scheme', 10, item, ['Paralysis', 'Parkinson’s Disease'], want)
    for item, want in [('Damage (injury) to Spinal Cord', 'Paralysis'),
                       ('Decrease in dopamine levels', 'Parkinson’s Disease'),
                       ('Physical Therapy', 'Paralysis'),
                       ('Levo (L)-Dopa (with carbidopa)', 'Parkinson’s Disease')]
]

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


TF_KEY = (90, 90, 520, 135)


def tf(x, answer):
    return G('under', page=8, clip=TF_KEY, head=f'({x})', expect=answer, marks=3)


NO_REPRINT = 'The scheme prints no reprint of this part, only its own marker over its answer.'
EACH_ITEM = '"Each of" a printed list, every entry priced on its own: one card per entry.'

Q2 = [_A(4, 'Answer this question in relation to the principles of experimentation.'),
      _A(4, 'A scientist carried out a trial, to investigate the effect of herbal', 'monitored over a 24 hour period.')]
Q3 = _A(5, 'Indicate whether the following statements are true or false', 'appropriate box in each case.')
Q4 = _A(6, 'The diagram shows part of the structure of DNA.')
Q5 = _A(7, 'Give one function of each of the following structures in the human body:')
Q6 = _A(8, 'The diagram shows the structure of a sensory neuron in the human body.')
Q7B = _A(9, 'Answer the following questions in relation to an investigation that you carried out to',
         'immobilise an enzyme or cell and examine its application.')
Q7BN = _A(9, 'Name the enzyme or cell that you used.')
Q8B = [_A(10, 'Answer the following questions in relation to an investigation you carried out to show',
          'digestive activity during seed germination.'),
       _A(10, 'State whether your used starch agar or skimmed milk (protein) agar.')]
Q9B = _A(11, 'Answer the following in relation to an investigation you carried out to dissect, display',
         'and identify the parts of a sheep’s or an ox’s heart.')
Q10B = [_C(2, 'Gunnera (Gunnera tinctoria), known as giant rhubarb is', 'else.'),
        _C(2, 'Gunnera spreads largely by its creeping surface rhizomes', 'rather than by birds eating the seeds.'),
        _C(2, 'Eradication schemes by county councils', 'wait their turn to take over.'),
        _C(2, 'Gunnera is one of the few flowering plants', 'its hinterland.'),
        _C(2, '(Adapted from', '2013.)')]
Q10CII = _C(2, 'Organisms’ roles in energy transfer in an ecosystem can be represented using',
            'different methods.')
Q11B = _C(3, 'The diagram is that of a transverse section (T.S.) of a leaf growing in a sunny area.')
Q11C = _C(3, 'Answer the following questions in relation to the second stage of aerobic respiration.')
Q11CI = [M('(i)', 3), _C(3, 'Name the 3‐carbon molecule which enters the mitochondrion.')]
Q11CII = [M('(ii)', 3), _C(3, 'Name the two carbon containing molecules produced when the 3‐carbon',
                           'molecule at (i) above is broken down.')]
Q12B = _C(4, 'The series of images below represents the four main stages of the DNA profiling',
          'technique invented by Sir Alec Jeffreys in 1984.')
Q12C = _C(4, 'In Andalusian chickens the allele for black feathers (B) exhibits incomplete dominance',
          'known as “blue”.')
Q13B = _C(5, 'Urine produced by the kidney contains water, salts and urea.')
Q13BIII = _C(5, 'A diagram of a human kidney is shown on', 'the right.')
Q13C = _C(5, 'The following table shows the representative composition of blood plasma, glomerular',
          'g/100 cm3 of fluid).')
Q13CII = _C(5, 'Using the data from the table above, in relation to glucose, explain the findings',
            'in the composition of the fluids between:')
Q13CIII = _C(5, 'Using your knowledge of homeostasis and excretion:')
Q14A = _C(6, 'The diagram below summarises some of the changes that take place in a typical human', 'diagram.')
Q14AII = [M('(ii)', 6), _C(6, 'Name the event that occurs between days 1‐5 of the cycle.')]
Q14B = _C(6, 'Answer the following questions from your knowledge of sexual reproduction in', 'flowering plants.')
Q14BI = _C(6, 'Describe in detail:')
Q14C = _C(7, 'Multi‐antibiotic (drug) resistant Clostridium difficile', 'adverse environmental conditions.')
Q14CI = [M('(ii)', 7), _C(7, 'Name the method of asexual reproduction exhibited by bacteria.')]
Q14CIV = _C(7, 'The diagram below is that of a typical growth curve for microorganisms;')
Q15A = _C(8, 'Plants produce chemicals called growth regulators such as auxin to regulate tropisms.')
Q15B = _C(9, 'Human papilloma virus (HPV) is a virus that can infect cells', 'induced immunity in humans.')
Q15BV = [M('(v)', 9), _C(9, 'Immunity is the ability to resist infection. Name the two types of induced', 'immunity.')]
Q15C = _C(9, 'Answer the following questions about a plant root.')
Q15CI = [M('(i)', 9), _C(9, 'Draw a diagram of the longitudal section (L.S.) of a typical root.')]
Q15CV = [M('(v)', 9), _C(9, 'Name the tissue that transports water in roots.')]

L_DNA = [L('G', S('Guanine', page=8), False), L('J', S('Nucleotide', page=8), False),
         L('K', S('Base pair or complementary bases', page=8), False), L('L', S('Hydrogen (bonding)', page=8), False)]
L_NEURON = [L('B', S('Axon', page=10), True)]
L_GROWTH = [L('A', S('*Lag', page=24), True), L('B', S('*Log', page=24), True),
            L('C', S('*Stationary', page=24), True)]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Give one example of a trace element in the human diet.'),
      [pt(S('Iron or zinc or copper or any correct example'), 4)], 'bio-1-2', 'trace-elements',
      SQ(7, 'Give an example of trace element in human diet:'), 4, stem=[_A(3, 'Answer any five of the following')]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Name the three chemical elements found in all lipids.'),
      [pt(S('Carbon (C), Hydrogen (H) and Oxygen (O)'), 4, note_sel=S('All three'))], 'bio-1-2',
      'elements-in-lipids', SQ(7, 'Name the chemical elements found in all lipids:'), 4,
      stem=[_A(3, 'Answer any five of the following')]),
    T('1c', 'Q1(c)', 'A', _A(3, 'Name the basic unit that makes up lipids.'),
      [pt(S('3 Fatty Acids (joined to) glycerol or Triglyceride'), 4)], 'bio-1-2', 'unit-of-lipids',
      SQ(7, 'Name the basic unit that makes up all lipids:'), 4, stem=[_A(3, 'Answer any five of the following')]),
    T('1d', 'Q1(d)', 'A', _A(3, 'Respiration is an example of a metabolic pathway in organisms.', 'is in question?'),
      [pt(S('Catabolic (Catabolism)'), 4)], 'bio-1-2', 'catabolic-pathway',
      SQ(7, 'Respiration is an example of:'), 4, stem=[_A(3, 'Answer any five of the following')]),
    T('1e', 'Q1(e)', 'A', _A(3, 'What is meant by the term polysaccharide?'),
      [pt(S('Many (greater than two) sugar (or named monosaccharide) units (or', 'molecules)'), 4)], 'bio-1-2',
      'polysaccharides', SQ(7, 'What is a polysaccharide?'), 4, stem=[_A(3, 'Answer any five of the following')]),
    T('1f', 'Q1(f)', 'A', _A(3, 'Name a storage polysaccharide found in animals.'),
      [pt(S('Glycogen'), 4)], 'bio-1-2', 'glycogen', SQ(7, 'Name a storage polysaccharide in animals:'), 4,
      stem=[_A(3, 'Answer any five of the following')]),
    T('2a', 'Q2(a)', 'A', _A(4, 'What is the purpose of carrying out an experiment?'),
      [pt(S('To test the hypothesis (or explanation or conclusion or prediction or idea)'), 3)], 'bio-u2',
      'purpose-of-an-experiment', SQ(7, 'What is the purpose of carrying out an experiment?'), 3, stem=Q2),
    T('2b', 'Q2(b)', 'A', _A(4, 'Why is a control normally used when carrying out an experiment?'),
      [pt(S('To compare (the results of the experiment)'), 3)], 'bio-u2', 'why-a-control',
      SQ(7, 'Why is a control normally used when carrying out an experiment?'), 3, stem=Q2),
    T('2c', 'Q2(c)', 'A', _A(4, 'Which group was the control group?'),
      [pt(S('B or (group drinking glass of water)'), 3)], 'bio-u2', 'identifying-the-control',
      SQ(7, 'Which group was the control group?'), 3, stem=Q2),
    T('2d', 'Q2(d)', 'A', _A(4, 'Give two reasons why the method of selecting the participants reduces the reliability',
                             'of the results.'),
      [anyn(S('Not random or biased (or unfair)/only friends', 'small'), 2, 3)], 'bio-u2', 'unreliable-selection',
      SQ(7, 'Give two reasons why the method of sample selection used reduces the reliability:'), 6, stem=Q2),
    T('2e', 'Q2(e)', 'A', _A(4, 'Using examples from the text, other than the selection of participants, give two ways',
                             'to show how the experimental design could be improved.'),
      [anyn(S('Longer period of time/', 'double blind testing (or no labels on glass)'), 2, 3,
            note_sel=S('NOT SAMPLE SELECTION'))], 'bio-u2', 'improving-the-design',
      SQ(7, 'Give two ways to show how the experimental design could be improved:'), 6, stem=Q2),
] + [
    T(f'3{x}', f'Q3({x})', 'A', _A(5, start), [tf(x, answer)], topic, concept,
      SQ(8, f'({x})', paired=NO_REPRINT + ' The key prints T or F under each part\'s column header.', bare=True), 3,
      stem=[Q3])
    for x, start, answer, topic, concept in [
        ('a', 'Spindle fibres contract during metaphase of mitosis.', 'F', 'bio-2-3', 'spindle-in-metaphase'),
        ('b', 'Glucose is produced by yeast cells during fermentation.', 'F', 'bio-2-2', 'products-of-fermentation'),
        ('c', 'The process of translation results in a protein being made.', 'T', 'bio-2-3', 'translation'),
        ('d', 'Prokaryotic cells contain a nucleus.', 'F', 'bio-1-3', 'prokaryotic-cells'),
        ('e', 'Darwin and Wallace proposed the Theory of Natural Selection.', 'T', 'bio-1-5', 'natural-selection'),
        ('f', 'A mutation to a cell’s DNA always has a negative impact for the cell.', 'F', 'bio-2-3',
         'effects-of-mutation'),
        ('g', 'The ribosome of the cell contains the chromosomes.', 'F', 'bio-1-3', 'ribosomes')]
] + [
    T('4a', 'Q4(a)', 'A', _A(6, 'What do the letters DNA stand for?'),
      [pt(S('Deoxyribonucleic Acid'), 3)], 'bio-1-2', 'dna-name', SQ(8, 'What do the letters DNA stand for?'), 3,
      stem=[Q4], fig='q4-dna'),
    T('4b', 'Q4(b)', 'A', _A(6, 'Identify molecule G.'),
      [pt(S('Guanine'), 3)], 'bio-1-2', 'guanine', SQ(8, 'Identify molecule G:'), 3, stem=[Q4], fig='q4-dna',
      labels=asked(L_DNA, 'G')),
    T('4c', 'Q4(c)', 'A', _A(6, 'The structure labelled J is a sub‐unit of DNA.', 'Identify the structure labelled J.'),
      [pt(S('Nucleotide'), 3)], 'bio-1-2', 'nucleotide', SQ(8, 'Identify the structure labelled as “J”:'), 3,
      stem=[Q4], fig='q4-dna', labels=asked(L_DNA, 'J')),
    T('4d', 'Q4(d)', 'A', _A(6, 'Name the part labelled K.'),
      [pt(S('Base pair or complementary bases'), 3)], 'bio-1-2', 'base-pairs', SQ(8, 'Part of Molecule labelled K:'),
      3, stem=[Q4], fig='q4-dna', labels=asked(L_DNA, 'K')),
    T('4e', 'Q4(e)', 'A', _A(6, 'What type of bonding occurs at L?'),
      [pt(S('Hydrogen (bonding)'), 3)], 'bio-1-2', 'hydrogen-bonds', SQ(8, 'Type of Bonding labelled L:'), 3,
      stem=[Q4], fig='q4-dna', labels=asked(L_DNA, 'L')),
    T('4f', 'Q4(f)', 'A', _A(6, 'State one structural difference between DNA and RNA, other than the number of',
                             'strands.'),
      [pt(S('DNA has (the sugar) deoxyribose and RNA has (the sugar) ribose', 'or RNA has shorter (strand)'), 3,
          note_sel=S('Any one difference'))], 'bio-1-2', 'dna-and-rna',
      SQ(8, 'One structural difference between DNA and RNA'), 3, stem=[Q4], fig='q4-dna'),
    T('4g', 'Q4(g)', 'A', _A(6, 'Give one non‐nuclear location of DNA in cells.'),
      [pt(S('Chloroplast or Mitochondrion'), 3)], 'bio-1-2', 'non-nuclear-dna',
      SQ(8, 'Give one non-nuclear location of DNA in cells:'), 3, stem=[Q4], fig='q4-dna'),
] + [
    T(f'5{x}', f'Q5({x})', 'A', _A(7, ask), rows, 'bio-2-4', concept, SQ(9, sq), 3, stem=[Q5])
    for x, ask, rows, concept, sq in [
        ('a', 'Cones in the eye.', [pt(S('To detect colour'), 3)], 'cones', 'Function of cones:'),
        ('b', 'The optic nerve.', [pt(S('To send impulse (or message) from eye to brain'), 3)], 'optic-nerve',
         'Function of the optic nerve:'),
        ('c', 'Iris in the eye.', [pt(S('To control the amount of light entering', '(the eye).'), 3,
                                      note_sel=S('Accept controls pupil size'))], 'iris',
         'Function of the iris in the eye:'),
        ('d', 'The Eustachian tube in the ear.',
         [pt(S('To equalise (or balance) pressure or to relieve pressure or to prevent pressure', 'build up'), 3)],
         'eustachian-tube', 'Function of the Eustachian tube in the ear:'),
        ('e', 'The semi‐circular canals in the ear.', [pt(S('(To control) balance'), 3)], 'semicircular-canals',
         'Function of semi-circular canals in the ear:'),
        ('f', 'Ligaments in joints.', [pt(S('To join bone to bone'), 3)], 'ligaments',
         'Function of Ligament in joints:'),
        ('g', 'Cartilage around the ends of bones.', [pt(S('Shock absorber or to reduce friction (or described)'), 3)],
         'cartilage', 'Function of cartilage around the ends of bones:')]
] + [
    T('6a', 'Q6(a)', 'A', _A(8, 'Identify the part of the neuron labelled B.'),
      [pt(S('Axon'), 3)], 'bio-2-4', 'axon', SQ(10, 'Identify the part labelled B:'), 3, stem=[Q6],
      fig='q6-neuron', labels=L_NEURON),
    T('6b', 'Q6(b)', 'A', _A(8, 'Name the substance (or group of substances) released by A during a nerve impulse.'),
      [pt(S('Neurotransmitter (or named example)'), 3)], 'bio-2-4', 'neurotransmitters',
      SQ(10, 'Name the substance produced A:',
         paired='The scheme\'s "Name the substance produced A" for the paper\'s "released by A during a nerve '
                'impulse".'), 3, stem=[Q6], fig='q6-neuron'),
    T('6c', 'Q6(c)', 'A', _A(8, 'Name the substance produced by the Schwann cell.'),
      [pt(S('Myelin'), 3)], 'bio-2-4', 'myelin', SQ(10, 'Name the substance produced by the schwann cell:'), 3,
      stem=[Q6], fig='q6-neuron'),
    T('6d', 'Q6(d)', 'A', _A(8, 'What is the function of this substance named at (c) during a nerve impulse?'),
      [pt(S('To speed up the impulse or to insulate (the axon)'), 3)], 'bio-2-4', 'function-of-myelin',
      SQ(10, 'What is the function of this substance?'), 3,
      stem=[Q6, M('(c)', 8), _A(8, 'Name the substance produced by the Schwann cell.')], fig='q6-neuron'),
    T('6e', 'Q6(e)', 'A', _A(8, 'Draw an arrow, in the box provided near the diagram, to show the direction of the',
                             'impulse.'),
      [pt(S('Arrow drawn on diagram From Right to Left'), 3, kind='criterion')], 'bio-2-4', 'direction-of-impulse',
      SQ(10, '(e)', paired=NO_REPRINT, bare=True), 3, stem=[Q6], fig='q6-neuron'),
] + [
    T('6f', 'Q6(f)', 'A', _A(8, 'Parkinson’s disease and paralysis are two disorders of the human nervous system.',
                             'treated.'),
      [pt(S(cause, cause_end), 3, label=S('Cause:')), pt(S(treat, 'treatment'), 3, label=S('Treatment:'))],
      'bio-2-4', f'{route}-cause-and-treatment', SQ(10, '(f)', paired=NO_REPRINT, bare=True), 6, route=route,
      decision='Paralysis or Parkinson\'s disease: the scheme prints a separate column of causes and of '
               'treatments for each, so each is a route card.')
    for route, cause, cause_end, treat in [
        ('paralysis', 'Damage (injury) to Spinal Cord', 'cause', 'Physical Therapy or'),
        ('parkinsons-disease', 'Decrease in dopamine levels or', 'or aging or other valid cause',
         'Levo (L)-Dopa (with carbidopa)')]
] + [
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', _A(9, 'What is an immobilised enzyme?'),
      [pt(S('An enzyme that is fixed (or attached or trapped)', 'or an enzyme in (or on) a gel (or an inert substance)'),
          3)], 'bio-2-1', 'immobilised-enzymes', SQ(11, 'What is an immobilised enzyme?'), 3),
    T('7aii', 'Q7(a)(ii)', 'B', _A(9, 'Give one advantage of using immobilised enzymes.'),
      [pt(S('Can be recovered or can be reused or pure product'), 3)], 'bio-2-1', 'advantages-of-immobilisation',
      SQ(11, 'Give one advantage of using immobilised enzymes:'), 3),
    T('7b', 'Q7(b)', 'B', Q7BN,
      [pt(S('Named enzyme or Yeast'), 3, kind='criterion')], 'bio-2-1', 'enzyme-or-cell-immobilised',
      SQ(11, 'Name the enzyme or cell that you used:'), 3, stem=[Q7B],
      decision='The ask printed under (b) before its (i): its own 3-mark row, carded as Q7(b).'),
    T('7bi', 'Q7(b)(i)', 'B', _A(9, 'Describe how you immobilised that enzyme or cell.'),
      [anyn(S('(Sodium) alginate/', 'Rinse'), 4, 3)], 'bio-2-1', 'immobilising-method',
      SQ(11, 'Describe how you immobilised that enzyme or cell:'), 12, stem=[Q7B, Q7BN]),
    T('7bii', 'Q7(b)(ii)', 'B', _A(9, 'Outline how you used the immobilised enzyme or cell to examine its application.'),
      [anyn(S('Add to matching substrate/', 'Control described'), 3, 3)], 'bio-2-1', 'using-immobilised-enzymes',
      SQ(11, 'Outline how you used the immobilised enzyme or cell'), 9, stem=[Q7B, Q7BN]),
    T('8ai', 'Q8(a)(i)', 'B', _A(10, 'What is meant by the term germination?'),
      [pt(S('Growth (or development) of a seed (into new plant)', 'or growth of embryo (or named part of embryo)'), 3)],
      'bio-2-5', 'germination', SQ(12, 'What is meant by the term germination?'), 3),
    T('8aii', 'Q8(a)(ii)', 'B', _A(10, 'State three factors necessary for successful germination.'),
      [pt(S('Oxygen and water and suitable temperature'), 3, note_sel=S('All three'))], 'bio-2-5',
      'conditions-for-germination', SQ(12, 'State three factor necessary for successful germination:'), 3),
    T('8bi', 'Q8(b)(i)', 'B', _A(10, 'Why were the seeds soaked in water prior to the investigation?'),
      [pt(S('To start germination or breaking dormancy or needed for', 'or to soften testa or to dissolve nutrients'),
          3)], 'bio-2-5', 'soaking-seeds', SQ(12, 'Why were the seeds soaked in water prior to the experiment?'), 3,
      stem=Q8B),
    T('8bii', 'Q8(b)(ii)', 'B', _A(10, 'Describe how you further prepared the seeds and added them to the agar plate(s).'),
      [anyn(S('Split (or cut) the seeds/', '(Control) boiled or dead seeds'), 3, 3)], 'bio-2-5', 'preparing-the-seeds',
      SQ(12, 'Describe how you further prepared the seeds and add them to the agar plate(s):'), 9, stem=Q8B),
    T('8biii', 'Q8(b)(iii)', 'B', _A(10, 'Under what conditions did you store the plate(s) containing the seeds to allow',
                                     'germination to occur?'),
      [pt(S('Incubator or at suitable temperature (15°C – 30°C)'), 3), pt(S('For a period of time (1 – 7 days)'), 3)],
      'bio-2-5', 'incubating-the-plates', SQ(12, 'Under what conditions did you store the plate(s)'), 6, stem=Q8B),
    T('8biv', 'Q8(b)(iv)', 'B', _A(10, 'How did you test to show that digestion had occurred?'),
      [pt(S('Add iodine or biuret solution'), 3, note_sel=S('(must match agar type)'))], 'bio-2-5',
      'testing-for-digestion', SQ(12, 'How did you test to show that digestion had occurred?'), 3, stem=Q8B,
      decision='Starch or skimmed-milk agar is marked on one row ("must match agar type"): one card.'),
    T('8bv', 'Q8(b)(v)', 'B', _A(10, 'State the result that showed digestion had occurred.'),
      [pt(S('(Blue black with) clear areas (or yellow or brown areas) under', 'clear area under (or around) seeds'), 3,
          note_sel=S('(must match test in (iv))'))], 'bio-2-5', 'evidence-of-digestion',
      SQ(12, 'State the result of the plate that showed that digestion had occurred:'), 3, stem=Q8B),
    T('9ai', 'Q9(a)(i)', 'B', _A(11, 'Why is the blood in the right side of the heart kept separate from the blood in the left?'),
      [pt(S('Prevents oxygenated and deoxygenated blood mixing', 'or oxygenated on LHS and deoxygenated on RHS'), 3)],
      'bio-2-6', 'separate-circulations',
      SQ(13, 'Why is the blood in the right side of the heart being kept separate from the blood', 'in the left?'), 3),
    T('9aii', 'Q9(a)(ii)', 'B', _A(11, 'In relation to the heartbeat, what is meant by the term diastole?'),
      [pt(S('Relaxation'), 3)], 'bio-2-6', 'diastole', SQ(13, 'What is meant by the term diastole?'), 3),
    T('9bi', 'Q9(b)(i)', 'B', _A(11, 'How did you identify the right hand side from the left hand side of the heart?'),
      [pt(S('Left thicker (or firmer)'), 3)], 'bio-2-6', 'left-and-right-sides',
      SQ(13, 'How did you identify the right-hand side from the left-hand side of the heart?'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', _A(11, 'On which surface of the heart did you observe the coronary artery (groove)?'),
      [pt(S('Front or ventral'), 3)], 'bio-2-6', 'coronary-artery',
      SQ(13, 'On which surface of the heart did you observe the coronary artery (groove)?'), 3, stem=[Q9B]),
    T('9biii', 'Q9(b)(iii)', 'B', _A(11, 'Describe how you dissected the heart to identify the bicuspid valve.'),
      [anyn(S('(Shallow) cut (incision)/', '(Valve) between top and bottom chambers (atria and ventricle)'), 4, 3)],
      'bio-2-6', 'finding-the-bicuspid-valve',
      SQ(13, 'Describe how you dissected the heart to identify the bicuspid valve:'), 12, stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', _A(11, 'State the precise location of one semilunar valve and describe how you further',
                                   'dissected the heart to locate this valve.'),
      [pt(S('Base of aorta or base of pulmonary artery'), 3,
          note_sel=S('or between ventricle and aorta (or pulmonary artery)')),
       pt(S('Cut into the aorta or cut into the pulmonary artery'), 3)], 'bio-2-6', 'finding-a-semilunar-valve',
      SQ(13, 'State the precise location of one semilunar valve:'), 6, stem=[Q9B],
      decision='Either semilunar valve is marked on the same two rows: one card.'),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', _C(2, 'Why is it necessary for an organism to possess an adaptation to its habitat?'),
      [pt(S('To increase chance of survival (of species) or to compete better'), 3)], 'bio-3-1', 'why-adaptations',
      SQ(14, 'Why necessary for an organism to possess an adaptation to its habitat?'), 3),
    T('10aii', 'Q10(a)(ii)', 'C', _C(2, 'Name two types of adaptation that an organism can exhibit.'),
      [anyn(S('Structural or Competitive or Behavioural'), 2, 3, sep=' or ')], 'bio-3-1', 'types-of-adaptation',
      SQ(14, 'Two types of adaptation that an organism can exhibit:'), 6),
    T('10bi', 'Q10(b)(i)', 'C', _C(2, 'Give two methods by which Gunnera outcompetes native Irish plants.'),
      [anyn(S('Shades out (native vegetation)/', 'spreads by the scattering of plant fragments'), 2, 3)], 'bio-3-1',
      'gunnera-outcompetes', SQ(14, 'Two methods by which Gunnera outcompetes native plants:'), 6, stem=Q10B),
    T('10bii', 'Q10(b)(ii)', 'C', _C(2, 'What method is usually used to control the population of Gunnera?'),
      [pt(S('Glyphosate or herbicide'), 3)], 'bio-3-1', 'controlling-gunnera',
      SQ(14, 'What method is usually used to control the population of Gunnera?'), 3, stem=Q10B),
    T('10biii', 'Q10(b)(iii)', 'C', _C(2, 'Suggest one reason why Gunnera is so successful at growing in poor quality soil.'),
      [pt(S('(The plant) can fix its (own) nitrogen (or explained)'), 3)], 'bio-3-1', 'gunnera-in-poor-soil',
      SQ(14, 'Suggest one reason why Gunnera is so successful at growing in poor quality'), 3, stem=Q10B),
    T('10biv', 'Q10(b)(iv)', 'C', _C(2, 'Biological control, using herbivores, might not be successful at controlling the',
                                     'population of Gunnera. Suggest one reason why.'),
      [pt(S('Toxic (Cyano)bacteria or poisoned by (Cyano)bacteria or too', 'stream sides)'), 3)], 'bio-3-1',
      'biological-control-of-gunnera', SQ(14, 'Suggest why biological control using herbivores not successful:'), 3,
      stem=Q10B),
    T('10bv', 'Q10(b)(v)', 'C', _C(2, 'Suggest two ways how Gunnera may invade and colonise new areas.'),
      [anyn(S('Creeping surface rhizomes/', '(animals) scatter seeds/ seed banks'), 2, 3)], 'bio-3-1',
      'gunnera-spreading', SQ(14, 'Suggest two ways how Gunnera many invade and colonise new areas:'), 6, stem=Q10B),
    T('10bvi', 'Q10(b)(vi)', 'C', _C(2, 'Name two abiotic factors that have limited the spread of Gunnera in Ireland.'),
      [anyn(S('(low) water/(low) humidity / frost (accept low temperature)'), 2, 3)], 'bio-3-1',
      'abiotic-limits-on-gunnera', SQ(14, 'Name two abiotic factors that has limited the spread of Gunnera in Ireland:'),
      6, stem=Q10B),
    T('10ci', 'Q10(c)(i)', 'C', _C(2, 'State one reason why ecological surveying is important.'),
      [pt(S('Conservation or find out what species (or organisms) are present or',
            'or monitor human impact on an ecosystem'), 3)], 'bio-3-1', 'why-survey',
      SQ(15, 'Suggest one reason why ecological surveying is important:'), 3),
] + [
    T(f'10cii{n}', f'Q10(c)(ii){n}', 'C', item(2, n, end, 'Organisms’ roles in energy transfer'), rows, 'bio-3-1',
      concept, sq, total, stem=[Q10CII], decision=EACH_ITEM)
    for n, end, rows, concept, sq, total in [
        (1, 'Name the ecosystem you studied.', [pt(S('Correctly named ecosystem'), 3, kind='criterion')],
         'naming-the-ecosystem', SQ(15, '1. Named ecosystem:'), 3),
        (2, '(trophic levels).', [pt(S('If no arrows read from left to right or from bottom to top'), 3,
                                     kind='criterion')],
         'drawing-a-food-chain', SQ(15, '2. Draw a food chain from this named ecosystem containing four members.'), 3),
        (3, 'Why are food chains mostly limited to four or five members?',
         [pt(S('Large energy loss or little energy available to be passed on'), 3)], 'length-of-food-chains',
         SQ(15, '3. Why are food chains mostly limited to four or five members?'), 3),
        (4, 'Draw a pyramid of numbers to represent this food chain.',
         [pt(S('Must match food chain above'), 3, kind='criterion')], 'drawing-a-pyramid-of-numbers',
         SQ(15, '4. Pyramid of numbers:'), 3),
        (5, '2. the secondary consumer.',
         [pt(S('at the bottom'), 3, label=S('Position of producer:', after='Must match food chain above')),
          pt(S('third from bottom'), 3, label=S('Position of secondary consumer:'))], 'positions-in-the-pyramid',
         SQ(15, '5.', 'Position of producer:'), 6),
        (6, 'Give one limitation of the use of pyramids of numbers.',
         [pt(S('Do not take size of organism into account or difficult to draw to',
               'or maybe inverted or some populations cannot be estimated'), 3)], 'limits-of-pyramids',
         SQ(15, '6. Give one limitation of the use of pyramids of numbers:'), 3)]
] + [
    T('11ai', 'Q11(a)(i)', 'C', _C(3, 'Name the type of nutrition exhibited by organisms that carry out photosynthesis.'),
      [pt(S('Autotrophic'), 3)], 'bio-2-2', 'autotrophic-nutrition',
      SQ(16, 'Name the type of nutrition exhibited by organisms that carry out photosynthesis:'), 3),
    T('11aii', 'Q11(a)(ii)', 'C', _C(3, 'Write a balanced chemical equation to summarise photosynthesis.'),
      [pt(S('All formulae correct'), 3, kind='criterion', note_sel=S('6CO2 + 6H2O → C6H12O6 + 6O2')),
       pt(S('Correctly balanced'), 3, kind='criterion')], 'bio-2-2', 'photosynthesis-equation',
      SQ(16, 'Write a balanced chemical equation to summarise photosynthesis:'), 6),
    T('11bi', 'Q11(b)(i)', 'C', _C(3, 'What is the role of the stomata in photosynthesis?'),
      [pt(S('Gas exchange'), 3, note_sel=S('Allow entry of CO2 or exit of O2'))], 'bio-2-2', 'stomata',
      SQ(16, 'What is the role of stomata in photosynthesis?'), 3, stem=[Q11B], fig='q11-leaf'),
    T('11bii', 'Q11(b)(ii)', 'C', _C(3, 'Which of the labelled part (A, B or C) would you expect to contain the most',
                                     'chloroplasts?'),
      [pt(S('Label B'), 3)], 'bio-2-2', 'palisade-chloroplasts',
      SQ(16, 'The cells of which labelled part contain the most chloroplasts in its cells?'), 3, stem=[Q11B],
      fig='q11-leaf'),
    T('11biii', 'Q11(b)(iii)', 'C', _C(3, 'Chloroplasts contain chlorophyll molecules. What is the role of the chlorophyll',
                                       'molecules in photosynthesis?'),
      [pt(S('Traps (or absorbs) light'), 3)], 'bio-2-2', 'role-of-chlorophyll',
      SQ(16, 'What is the role of the chlorophyll molecules in photosynthesis?'), 3, stem=[Q11B], fig='q11-leaf'),
    T('11biv', 'Q11(b)(iv)', 'C', _C(3, 'What particles are released from chlorophyll during the light dependent stage of',
                                     'photosynthesis.'),
      [pt(S('*Electrons (e-)'), 3)], 'bio-2-2', 'electrons-from-chlorophyll',
      SQ(16, 'What particles are released from chlorophyll during the light dependent stage?'), 3, stem=[Q11B],
      fig='q11-leaf'),
    T('11bv', 'Q11(b)(v)', 'C', [_C(3, 'These particles enter one of two pathways.'),
                                 _C(3, 'Give an account of the events of pathway 2.')],
      [anyn(S('Electrons trapped by NADP', 'chlorophyll/ ATP formed'), 5, 3)], 'bio-2-2', 'pathway-two',
      SQ(16, 'Give an account of the events of pathway 2:'), 15,
      stem=[Q11B, M('(iv)', 3), _C(3, 'What particles are released from chlorophyll during the light dependent stage of',
                                   'photosynthesis.')], fig='q11-leaf'),
    T('11ci', 'Q11(c)(i)', 'C', _C(3, 'Name the 3‐carbon molecule which enters the mitochondrion.'),
      [pt(S('*Pyruvate (*Pyruvic acid)'), 3)], 'bio-2-2', 'pyruvate',
      SQ(17, 'Name the 3-Carbon molecule which enters the mitochondrion:'), 3, stem=[Q11C]),
    T('11cii', 'Q11(c)(ii)', 'C', _C(3, 'Name the two carbon containing molecules produced when the 3‐carbon',
                                     'molecule at (i) above is broken down.'),
      [pt(S('*CO2'), 3), pt(S('*Acetyl (Co A)'), 3)], 'bio-2-2', 'breakdown-of-pyruvate',
      SQ(17, 'Name the two products formed when the 3-Carbon molecule at (i) above is', 'broken down:'), 6,
      stem=[Q11C] + Q11CI),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(3, 'One of these carbon containing molecules formed at (ii) above enters a series of',
                                       'reactions. Name this series of reactions.'),
      [pt(S('Krebs Cycle'), 3)], 'bio-2-2', 'krebs-cycle',
      SQ(17, 'Name the series of reactions that take place:',
         paired='The scheme\'s "Name the series of reactions" for the paper\'s two-sentence ask ending "Name this '
                'series of reactions".'), 3,
      stem=[Q11C] + Q11CII),
    T('11civ', 'Q11(c)(iv)', 'C', _C(3, 'Outline the events that take place in the electron transport chain (system).'),
      [anyn(S('High energy electrons/', 'to form water.'), 4, 3)], 'bio-2-2', 'electron-transport-chain',
      SQ(17, 'Outline the events that take place in the electron transport chain (system)'), 12, stem=[Q11C]),
    T('12ai', 'Q12(a)(i)', 'C', _C(4, 'What is meant by the term heredity?'),
      [pt(S('Passing on (or transmission) of characteristics (traits or genes)', 'from one generation (or cell) to the next'),
          3)], 'bio-1-4', 'heredity', SQ(18, 'What is meant by the term heredity?'), 3),
    T('12aii', 'Q12(a)(ii)', 'C', _C(4, 'State Mendel’s Law of Independent Assortment (2nd Law).'),
      [pt(S('Each member of one pair of alleles can combine (randomly)'), 3),
       pt(S('With either member of another pair (at gamete formation)'), 3)], 'bio-1-4', 'independent-assortment',
      SQ(18, 'State Mendel’s Law of Independent Assortment (2nd Law):'), 6,
      decision='The scheme prints the law in two wordings, each on two 3-mark rows, joined by "OR": answer '
               'variants of one task.'),
    T('12bi', 'Q12(b)(i)', 'C', _C(4, 'Distinguish between DNA profiling and genetic screening.'),
      [pt(S('Generating a pattern of bands from a (DNA) sample'), 3,
          label=S('DNA Profiling:', after='State Mendel’s Law of Independent Assortment')),
       pt(S('(Test) to show presence (or absence) of a gene'), 3, label=S('Genetic screening:'))], 'bio-3-3',
      'profiling-and-screening', SQ(18, 'DNA Profiling:'), 6, stem=[Q12B], fig='q12-profiling'),
] + [
    T(f'12bii{n}', 'Q12(b)(ii)', 'C', _C(4, 'Explain each of the Stages, 1 to 4, of DNA profiling shown above.'),
      [pt(S(ans), 3, label=S(f'Stage {n}:', f'Stage {n}:'))], 'bio-3-3', concept,
      SQ(18, 'Explain each of the Stages, 1 to 4, of DNA Profiling:'), 3, stem=[Q12B], fig='q12-profiling',
      item=(f'stage-{n}', f'Stage {n}'), decision=EACH_ITEM)
    for n, ans, concept in [(1, 'DNA is isolated (or extracted or released)', 'profiling-isolation'),
                            (2, 'DNA (strands are) cut (into fragments using enzymes)', 'profiling-cutting'),
                            (3, 'Fragments are separated on the basis of size', 'profiling-separation'),
                            (4, '(The pattern) is analysed (or compared or examined)', 'profiling-analysis')]
] + [
    T('12biii', 'Q12(b)(iii)', 'C', _C(4, 'Give any two applications of DNA profiling.'),
      [pt(S('Forensic (or example)'), 3), pt(S('Medical (or example)'), 3)], 'bio-3-3', 'uses-of-profiling',
      SQ(18, 'State two applications of DNA Profiling:'), 6, stem=[Q12B], fig='q12-profiling',
      decision='The scheme prints two application areas, one row each: one card.'),
    T('12biv', 'Q12(b)(iv)', 'C', _C(4, 'Identical twins have the same DNA profile. Explain why this is so.'),
      [pt(S('(Both) have same genotype (or same genes)', 'or (both) come from same zygote (fertilised egg)'), 3)],
      'bio-3-3', 'identical-twins', SQ(18, 'Explain why identical twins have the same DNA profile:'), 3, stem=[Q12B],
      fig='q12-profiling'),
] + [
    T(f'12ci-{slug}', 'Q12(c)(i)', 'C', _C(4, 'Explain the terms underlined in the passage above.'),
      [pt(S(start, end), 3)], 'bio-1-4', slug, SQ(19, sq), 3, stem=[Q12C], qfig='q12c-passage',
      item=(slug, name), decision=EACH_ITEM)
    for slug, name, sq, start, end in [
        ('allele', 'Allele', 'Allele:', 'A version (variant) of a gene or alternative form of a gene', None),
        ('incomplete-dominance', 'Incomplete dominance', 'Incomplete dominance:', 'When both alleles are expressed',
         'or heterozygous condition is intermediate'),
        ('homozygous', 'Homozygous', 'Homozygous:', '(When) identical alleles are present (for a trait)', None),
        ('phenotype', 'Phenotype', 'Phenotype:', 'The (physical) expression of a gene (or of genotype)', None)]
] + [
    T('12cii', 'Q12(c)(ii)', 'C', _C(4, 'Determine all the possible genotypes and phenotypes of the offspring of a',
                                     'Include in your answer the ratio of the resulting phenotypes.'),
      [pt(S('BB, Bb, bb'), 3, label=S('Offspring Genotypes:')),
       pt(S('Black, Blue (or speckled), White'), 3, label=S('Offspring Phenotypes:')),
       pt(S('1 Black: 2 Blue: 1 White'), 3, label=S('Ratio of offspring Phenotypes:'))], 'bio-1-4',
      'incomplete-dominance-cross', SQ(19, '“Blue” Rooster X “Blue” Hen.'), 9, stem=[Q12C]),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(4, 'What would be the effect on the offspring phenotype ratio, in the genetic cross',
                                       'the recessive trait?'),
      [pt(S('* 3 Black: 1 White', after='1 Black: 2 Blue: 1 White'), 3)], 'bio-1-4', 'complete-dominance-ratio',
      SQ(19, 'Ratio:', 'Ratio:'), 3,
      stem=[Q12C, M('(ii)', 4), _C(4, 'Determine all the possible genotypes and phenotypes of the offspring of a',
                                   'Include in your answer the ratio of the resulting phenotypes.')]),
    T('13ai', 'Q13(a)(i)', 'C', _C(5, 'Explain what is meant by the term homeostasis.'),
      [pt(S('(Ability to) maintain a constant (or stable) internal environment'), 3)], 'bio-2-4', 'homeostasis',
      SQ(20, 'Homeostasis:'), 3),
    T('13aii', 'Q13(a)(ii)', 'C', _C(5, 'Give one reason why homeostasis is important in organisms.'),
      [pt(S('(For) metabolism or (for) enzyme activity'), 3)], 'bio-2-4', 'why-homeostasis',
      SQ(20, 'Why is homeostasis important:'), 3),
    T('13aiii', 'Q13(a)(iii)', 'C', _C(5, 'Explain what is meant by the term excretion.'),
      [pt(S('Removal of metabolic waste or getting rid of waste products from', 'cells (or body)'), 3)], 'bio-2-6',
      'excretion', SQ(20, 'Excretion'), 3),
    T('13bi', 'Q13(b)(i)', 'C', _C(5, 'State the precise location in the body', 'where urea is made.'),
      [pt(S('*Liver'), 3)], 'bio-2-6', 'where-urea-is-made', SQ(20, 'Precise location where urea is made:'), 3,
      stem=[Q13B]),
    T('13bii', 'Q13(b)(ii)', 'C', _C(5, 'Name the food biomolecule from which', 'urea is derived.'),
      [pt(S('*Protein (*Amino acids)'), 3)], 'bio-2-6', 'source-of-urea',
      SQ(20, 'Name the food source from which urea is derived:'), 3, stem=[Q13B]),
] + [
    T(f'13biii{n}', f'Q13(b)(iii){n}', 'C', item(5, n, end, 'A diagram of a human kidney is shown on'),
      [pt(S(ans, after=anchor), 3)], 'bio-2-6', concept, SQ(20, sq, sq), 3, stem=[Q13B, Q13BIII], fig='q13-kidney',
      decision=EACH_ITEM)
    for n, end, ans, anchor, concept, sq in [
        (1, 'Bowman’s capsule located?', '*Cortex', '*Protein (*Amino acids)', 'bowmans-capsule-location',
         'Location of Bowman’s capsule:'),
        (2, 'the Loop of Henle located?', '*Medulla', '*Cortex', 'loop-of-henle-location',
         'Location of loop of Henle:'),
        (3, 'Name the part labelled ‘A’.', '*Ureter', '*Medulla', 'ureter', 'Name the part labelled ‘A’.')]
] + [
    T('13biv', 'Q13(b)(iv)', 'C', _C(5, 'Draw a large diagram of a nephron and its associated blood supply from a human',
                                     'kidney. Label the following parts:'),
      [pt(S('Bowman’s capsule + 2 convoluted tubules with loop'), 3, kind='criterion'),
       pt(S('Glomerulus + capillary (blood vessels) surrounding tubules'), 3, kind='criterion'),
       anyn(S('Bowman’s capsule, Loop of Henle, proximal convoluted tubule,',
              'collecting duct, distal convoluted tubule, glomerulus.'), 6, 1, sep=',')], 'bio-2-6',
      'drawing-a-nephron', SQ(20, 'Drawing:'), 12, stem=[Q13B], qfig='q13b-iv-labels',
      decision='The parts to label are printed as a table: shown as the question\'s own print.'),
    T('13ci', 'Q13(c)(i)', 'C', _C(5, 'Using the data from the table above, what is the main difference between the',
                                   'Explain why this is so.'),
      [pt(S('Plasma has proteins (7g/100 cm3) filtrate has none'), 3),
       pt(S('Proteins too big to be pass through (the glomerulus wall)'), 3, label=S('Explain why:'))], 'bio-2-6',
      'plasma-and-filtrate', SQ(21, 'What is the main difference between plasma and filtrate?'), 6, stem=[Q13C],
      fig='q13-table'),
] + [
    T(f'13cii{n}', f'Q13(c)(ii){n}', 'C', item(5, n, end, 'in relation to glucose, explain the findings'), rows,
      'bio-2-6', concept, SQ(21, sq), 3, stem=[Q13C, Q13CII], fig='q13-table', decision=EACH_ITEM)
    for n, end, rows, concept, sq in [
        (1, 'Blood plasma and glomerular filtrate.',
         [pt(S('Glucose (molecules) small enough to pass through (the',
               'wall) or all the glucose passes through (or is filtered)', skip_marks=True), 3)],
         'glucose-in-filtrate', '1. Blood plasma and filtrate:'),
        (2, 'Glomerular filtrate and urine.', [pt(S('(All) glucose is reabsorbed (back into the blood)'), 3)],
         'glucose-reabsorption', '2. Glomerular filtrate and urine:')]
] + [
    T('13ciii1', 'Q13(c)(iii)1', 'C', item(5, 1, 'by a high salt intake.', 'Using your knowledge of homeostasis'),
      [pt(S('(volume) decreases (or lowers) or low (volume)'), 3)], 'bio-2-6', 'salt-and-urine-volume',
      SQ(21, '1. What is the effect on the volume of urine produced by a high salt intake?'), 3,
      stem=[Q13C, Q13CIII], fig='q13-table', decision=EACH_ITEM),
    T('13ciii2', 'Q13(c)(iii)2', 'C', item(5, 2, 'Explain your answer to part 1.', 'Using your knowledge of homeostasis'),
      [anyn(S('ADH/ from pituitary/', 'more water reabsorbed'), 3, 3)], 'bio-2-6', 'adh-and-urine-volume',
      SQ(21, 'Explain:'), 9,
      stem=[Q13C, Q13CIII, item(5, 1, 'by a high salt intake.', 'Using your knowledge of homeostasis')],
      fig='q13-table', decision=EACH_ITEM),
    T('14ai', 'Q14(a)(i)', 'C', _C(6, 'What is the role of the menstrual cycle?'),
      [pt(S('To prepare (endometrium or uterus) for pregnancy (or for',
            'implantation) or egg development or egg release (or ovulation)'), 3)], 'bio-2-5', 'role-of-menstrual-cycle',
      SQ(22, 'What is the role of the menstrual cycle?'), 3, stem=[Q14A], fig='q14-cycle'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(6, 'Name the event that occurs between days 1‐5 of the cycle.'),
      [pt(S('Menstruation or (having) a period'), 3)], 'bio-2-5', 'menstruation',
      SQ(22, 'Name the event that involves the Uterine lining between days 1-4 of the cycle:',
         paired='The scheme\'s reprint reads days 1-4 where the paper prints days 1-5; the same event is asked.'),
      3, stem=[Q14A], fig='q14-cycle'),
    T('14aiii', 'Q14(a)(iii)', 'C', _C(6, 'The event you have named at (ii) is triggered by a large drop in a certain',
                                       'hormone. Name the hormone.'),
      [pt(S('*Progesterone'), 3)], 'bio-2-5', 'progesterone-drop',
      SQ(22, 'The event is triggered by a large drop in what Hormone?'), 3, stem=[Q14A] + Q14AII, fig='q14-cycle'),
    T('14aiv', 'Q14(a)(iv)', 'C', _C(6, 'Where is the hormone oestrogen produced?'),
      [pt(S('*Graafian follicle or *ovary'), 3)], 'bio-2-5', 'where-oestrogen-is-made',
      SQ(22, 'Where is oestrogen produced?'), 3, stem=[Q14A], fig='q14-cycle'),
    T('14av', 'Q14(a)(v)', 'C', _C(6, 'Using the time axis from the graph above, sketch a graph in your answer book, to',
                                   'indicate the changes in oestrogen levels during the cycle.'),
      [pt(S('Rise day 4-14 and drop day 14-28'), 3, kind='criterion')], 'bio-2-5', 'oestrogen-levels',
      SQ(22, 'Sketch graph to show changes in oestrogen levels:'), 3, stem=[Q14A], fig='q14-cycle'),
    T('14avi', 'Q14(a)(vi)', 'C', _C(6, 'Name the event that occurs at day 14 and name the hormone which causes this',
                                     'to happen.'),
      [pt(S('*Ovulation (or egg release)'), 3), pt(S('*LH or *Luteinising hormone'), 3)], 'bio-2-5',
      'ovulation-and-lh', SQ(22, 'Name the event that occurs at day 14:'), 6, stem=[Q14A], fig='q14-cycle'),
    T('14avii', 'Q14(a)(vii)', 'C', _C(6, 'Name the structure that the Graafian follicle develops into after day 14.'),
      [pt(S('*Corpus luteum'), 3)], 'bio-2-5', 'corpus-luteum',
      SQ(22, 'Name the structure that the follicle turns into after day 14'), 3, stem=[Q14A], fig='q14-cycle'),
    T('14aviii', 'Q14(a)(viii)', 'C', _C(6, 'Does the graph indicate that the woman became pregnant during this menstrual',
                                         'cycle? Explain your answer.'),
      [pt(S('*No'), 3), pt(S('Uterine lining breaks down (at the end)', 'or corpus luteum breaks down'), 3,
                           label=S('Explain:'))], 'bio-2-5', 'reading-the-cycle-for-pregnancy',
      SQ(22, 'Does graph indicate pregnancy?'), 6, stem=[Q14A], fig='q14-cycle'),
] + [
    T(f'14bi{n}', f'Q14(b)(i){n}', 'C', item(6, n, end, 'Describe in detail:'), [anyn(S(start, close), 3, 3)],
      'bio-2-5', concept, SQ(23, sq, sq_end), 9, stem=[Q14B, Q14BI], decision=EACH_ITEM)
    for n, end, start, close, concept, sq, sq_end in [
        (1, 'from a microspore mother cell.', 'Diploid (microspore) mother cell /',
         'two haploid nuclei/ the generative nucleus/ the tube nucleus', 'pollen-development',
         '1. Describe in detail the development of the pollen grain from a microspore', 'mother cell:'),
        (2, 'double fertilisation.', 'Pollen tube grows (down the style)/', 'the other fuses with polar nuclei',
         'pollination-to-fertilisation', '2. Describe the events grain following pollination up to and including double',
         'fertilisation:')]
] + [
    T('14bii', 'Q14(b)(ii)', 'C', _C(6, 'Give two adaptations of wind‐pollinated flowers that increase their chance of',
                                     'successful pollination.'),
      [anyn(S('Anthers (or stigma or stamens) outside (flower)/', 'pollen grains light/ stigma is feathery'), 2, 3)],
      'bio-2-5', 'wind-pollination', SQ(23, 'Give two adaptations of wind-pollinated flowers:'), 6, stem=[Q14B]),
    T('14biii', 'Q14(b)(iii)', 'C', _C(6, 'State two advantages of sexual reproduction versus asexual reproduction in',
                                       'plants.'),
      [anyn(S('Variation/ dispersal/', 'disease'), 2, 3)], 'bio-2-5', 'advantages-of-sexual-reproduction',
      SQ(23, 'State two advantages of sexual reproduction over asexual reproduction:'), 6, stem=[Q14B]),
    T('14ci', 'Q14(c)(i)', 'C', _C(7, 'Draw a large labelled diagram of a typical bacterial cell.'),
      [pt(S('Cell wall + cell membrane'), 3, kind='criterion'), pt(S('Indication of nucleic acid'), 3, kind='criterion'),
       anyn(S('Cell wall/ cell membrane/', 'flagella/capsule or slime layer'), 3, 1)], 'bio-3-2',
      'drawing-a-bacterium', SQ(24, 'Drawing:'), 9, stem=[Q14C]),
    T('14cii', 'Q14(c)(ii)', 'C', _C(7, 'Name the method of asexual reproduction exhibited by bacteria.'),
      [pt(S('*Binary fission'), 3)], 'bio-3-2', 'binary-fission',
      SQ(24, 'Name the method of asexual reproduction in bacteria:'), 3, stem=[Q14C]),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(7, 'Describe the process of this asexual reproduction in bacteria.'),
      [anyn(S('DNA replicates/', 'two new bacteria formed'), 3, 3)], 'bio-3-2', 'process-of-binary-fission',
      SQ(24, 'Describe the process of binary fission:',
         paired='The scheme names the process ("binary fission") where the paper says "this asexual reproduction".'),
      9, stem=[Q14C] + Q14CI),
    T('14civ1', 'Q14(c)(iv)1', 'C', _C(7, '1. Name each of the stages of the growth curve labelled A, B and C.'),
      [allof([(S('Name stage A:', 'Name stage A:'), S('*Lag')), (S('Name stage B:', 'Name stage B:'), S('*Log')),
              (S('Name stage C:', 'Name stage C:'), S('*Stationary'))], 3, note_sel=S('All three'))], 'bio-3-2',
      'stages-of-growth', SQ(24, '(iv)', paired=NO_REPRINT + ' Its items are reprinted as row labels.', bare=True), 3,
      stem=[Q14C, Q14CIV], fig='q14-growth', labels=L_GROWTH, decision=EACH_ITEM),
    T('14civ2', 'Q14(c)(iv)2', 'C', _C(7, '2. What is a suitable label for axis Y?'),
      [pt(S('Population or number (of micro-organisms)'), 3)], 'bio-3-2', 'growth-curve-axis',
      SQ(24, '2. Name suitable label for axis Y:'), 3, stem=[Q14C, Q14CIV], fig='q14-growth', decision=EACH_ITEM),
    T('14cv', 'Q14(c)(v)', 'C', _C(7, 'Copy the growth curve in your answer book and indicate on your diagram',
                                   'when endospore formation is most likely to occur.'),
      [pt(S('Anywhere on stationery or anywhere on decline'), 3, kind='criterion')], 'bio-3-2', 'endospore-formation',
      SQ(24, 'Indicate in diagram when endospore formation most likely to occur:'), 3, stem=[Q14C, Q14CIV],
      fig='q14-growth'),
    T('15ai', 'Q15(a)(i)', 'C', _C(8, 'What is a tropism?'),
      [pt(S('Growth response to a stimulus'), 3)], 'bio-2-4', 'tropism', SQ(25, 'What is a tropism?'), 3, stem=[Q15A]),
    T('15aii', 'Q15(a)(ii)', 'C', _C(8, 'Where precisely in plants are auxins produced?'),
      [pt(S('Meristem or root tip or shoot tip or bud'), 3)], 'bio-2-4', 'where-auxins-are-made',
      SQ(25, 'Where precisely are auxins produced?'), 3, stem=[Q15A]),
    T('15aiii', 'Q15(a)(iii)', 'C', _C(8, 'What is the precise benefit to the plant that the shoot is positively phototropic?'),
      [pt(S('(Absorb) more light or more photosynthesis'), 3)], 'bio-2-4', 'benefit-of-phototropism',
      SQ(25, 'What is the precise benefit to the plant of being positively phototropic'), 3, stem=[Q15A]),
    T('15aiv', 'Q15(a)(iv)', 'C', _C(8, 'Give two uses in agriculture or horticulture of plant growth regulators.'),
      [anyn(S('Herbicide (or weed killer) /rooting powder/', 'seedless fruit /larger fruit'), 2, 3)], 'bio-2-4',
      'uses-of-growth-regulators', SQ(25, 'Give two uses of growth regulators in agriculture or horticulture:'), 6,
      stem=[Q15A]),
    T('15av', 'Q15(a)(v)', 'C', [_C(8, 'The graph below shows the result of a student’s investigation on the effect of',
                                    'roots and shoots.'),
                                 _C(8, 'Compare the effects the different concentrations of IAA have on the growth of',
                                    'the roots and the shoots.')],
      [pt(S('Any three valid points from graph (must refer to root and shoot)'), 9, kind='criterion', units=[3, 3, 3],
          note_sel=S('At least one point from each'))], 'bio-2-4', 'iaa-concentration',
      SQ(25, 'What is the effect of different IAA concentration of growth of roots and shoots?'), 9, stem=[Q15A],
      fig='q15-iaa'),
    T('15avi', 'Q15(a)(vi)', 'C', _C(8, 'State two reasons why the action of an auxin is considered to be similar to',
                                     'the action of a hormone in the human body.'),
      [anyn(S('Chemical (action)/', 'prolonged effect or widespread effect'), 2, 3)], 'bio-2-4', 'auxins-as-hormones',
      SQ(25, 'State two reasons why the action of auxin is similar to action of a hormone:'), 6, stem=[Q15A]),
    T('15bi', 'Q15(b)(i)', 'C', _C(9, 'From which biochemical component are viral coats made?'),
      [pt(S('*Protein'), 3)], 'bio-1-1', 'viral-coat', SQ(26, 'What biochemical component of viral coats?'), 3,
      stem=[Q15B]),
    T('15bii', 'Q15(b)(ii)', 'C', _C(9, 'Name the other main chemical component of a virus.'),
      [pt(S('Nucleic acid or DNA or RNA'), 3)], 'bio-1-1', 'viral-nucleic-acid',
      SQ(26, 'Name the other main chemical component of a virus:'), 3, stem=[Q15B]),
    T('15biii', 'Q15(b)(iii)', 'C', _C(9, 'Why can viruses be described as obligate parasites?'),
      [pt(S('Can only replicate (reproduce) in a host (or cell)'), 3)], 'bio-1-1', 'obligate-parasites',
      SQ(26, 'Why can viruses be described as obligate parasites?'), 3, stem=[Q15B]),
    T('15biv', 'Q15(b)(iv)', 'C', _C(9, 'Describe how virus particles can infect and replicate in host cells.'),
      [anyn(S('Attachment (of virus to host cell)/', 'assembles / (new) virus (particles) produced (or released)'), 3, 3)],
      'bio-1-1', 'viral-replication', SQ(26, 'Describe how viral particles can infect and replicate in a host cell:'), 9,
      stem=[Q15B]),
    T('15bv', 'Q15(b)(v)', 'C', _C(9, 'Immunity is the ability to resist infection. Name the two types of induced',
                                   'immunity.'),
      [pt(S('*Active'), 3), pt(S('*Passive'), 3)], 'bio-2-4', 'induced-immunity',
      SQ(26, 'Name two types of induced immunity:'), 6, stem=[Q15B]),
    T('15bvi', 'Q15(b)(vi)', 'C', _C(9, 'Which of these types of immunity that you have named at (v), occurs after a',
                                     'vaccination with the HPV vaccine?'),
      [pt(S('*Active'), 3)], 'bio-2-4', 'immunity-from-vaccination',
      SQ(26, 'Which type of immunity occurs after vaccination?'), 3, stem=[Q15B] + Q15BV),
    T('15bvii', 'Q15(b)(vii)', 'C', _C(9, 'Give one difference between the types of induced immunity that you have',
                                       'named at (v).'),
      [pt(S('Active is longer lasting (than passive)', 'receives antibodies'), 3)], 'bio-2-4',
      'active-and-passive-immunity', SQ(26, 'Give one difference between the active and passive immunity:'), 3,
      stem=[Q15B] + Q15BV),
    T('15ci', 'Q15(c)(i)', 'C', _C(9, 'Draw a diagram of the longitudal section (L.S.) of a typical root.'),
      [pt(S('Long tip + root hairs'), 3, kind='criterion')], 'bio-2-6', 'drawing-a-root', SQ(27, 'Drawing:'), 3,
      stem=[Q15C]),
    T('15cii', 'Q15(c)(ii)', 'C', _C(9, 'Label any three zones on your diagram.'),
      [anyn(S('Meristematic (or cell division) / elongation/', 'cap (or protection)'), 3, 1)], 'bio-2-6',
      'zones-of-the-root', SQ(27, 'Labels of zones:'), 3, stem=[Q15C] + Q15CI),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(9, 'In which zone is water absorbed from the soil?'),
      [pt(S('*Differentiation'), 3)], 'bio-2-6', 'zone-of-absorption',
      SQ(27, 'In which zone is water absorbed from the soil?'), 3, stem=[Q15C]),
    T('15civ', 'Q15(c)(iv)', 'C', _C(9, 'Name the process through which water is absorbed from the soil.'),
      [pt(S('*Osmosis'), 3)], 'bio-2-6', 'osmosis-into-roots',
      SQ(27, 'Name the process through water is absorbed from the soil:'), 3, stem=[Q15C]),
    T('15cv', 'Q15(c)(v)', 'C', _C(9, 'Name the tissue that transports water in roots.'),
      [pt(S('*Xylem'), 3)], 'bio-2-6', 'xylem', SQ(27, 'Name the tissue that transports water in roots:'), 3,
      stem=[Q15C]),
    T('15cvi', 'Q15(c)(vi)', 'C', _C(9, 'Give two ways in which this tissue is adapted to transporting water.'),
      [anyn(S('Hollow/ continuous tube/narrow/', 'lignin'), 2, 3)], 'bio-2-6', 'xylem-adaptations',
      SQ(27, 'Give two ways in which this tissue is adapted to transporting water:'), 6, stem=[Q15C] + Q15CV),
    T('15cvii', 'Q15(c)(vii)', 'C', _C(9, 'Two Irish scientists, Dixon and Joly, first proposed the theory of water movement',
                                       'through this tissue to the leaves in a plant.'),
      [anyn(S('Water molecules stick together or cohesion/', 'water upwards'), 3, 3)], 'bio-2-6', 'cohesion-tension',
      SQ(27, 'Describe the mechanism by which water moves through this tissue to the', 'leaves:'), 9,
      stem=[Q15C] + Q15CV),
]

ANSWER_VARIANTS = {
    '12aii': [
        ('alleles-combine', 'Alleles can combine',
         [pt(S('Each member of one pair of alleles can combine (randomly)'), 3),
          pt(S('With either member of another pair (at gamete formation)'), 3)]),
        ('factors-separate', 'Factors separate independently',
         [pt(S('Members of one pair of factors (alleles) separate independently'), 3),
          pt(S('Of members of another pair of factors (alleles) (at gamete', 'formation)'), 3)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q4-dna': ('038', 6, (130, 80, 512, 276), SEC, ['G', 'J', 'K', 'L'],
               'Diagram of part of a DNA molecule: two sugar-phosphate backbones, with sugars marked S and phosphates '
               'marked P, joined by paired bases A-T, T-A, G-C and C-G. A box labelled K encloses one base pair, '
               'L points at the dotted bonds between a pair of bases, a tall box labelled J encloses a phosphate, '
               'sugar and base, and a label reads "Identify G" beside a base marked G.', False),
    'q6-neuron': ('038', 8, (88, 72, 495, 278), SEC, ['A', 'B'],
                  'Diagram of a sensory neuron: branched endings at the left marked A, a long fibre marked B '
                  'wrapped in segments with a Schwann cell labelled, a cell body on a short side branch labelled '
                  'Cell body, and an empty box near the fibre for an arrow.', False),
    'q11-leaf': ('040', 3, (176, 132, 462, 307), SEC, ['A', 'B', 'C'],
                 'Drawing of a transverse section of a leaf: a flat upper layer marked A, a row of tall column-shaped '
                 'cells marked B, loosely packed rounded cells with air spaces marked C, a vein, and openings in the '
                 'lower surface labelled Stomata.', False),
    'q12-profiling': ('040', 4, (86, 172, 512, 272), SEC, [],
                      'Four arrows numbered 1 to 4 link five pictures: a sample tube labelled "Sample used to create a '
                      'DNA profile", a long DNA strand, DNA cut into short pieces, bands in the lanes of a gel, and a '
                      'pattern of bands labelled "A DNA profile".', False),
    'q12c-passage': ('040', 4, (108, 418, 540, 481), SEC, [],
                     'The printed passage about Andalusian chickens, with the words allele, incomplete dominance, '
                     'homozygous and phenotype underlined.', False),
    'q13-kidney': ('040', 5, (358, 128, 528, 258), SEC, ['A'],
                   'Drawing of a human kidney cut lengthways: the outer region labelled Cortex, the inner region '
                   'labelled Medulla, the central cavity labelled Pelvis, and the tube leaving it marked A.', False),
    'q13b-iv-labels': ('040', 5, (140, 346, 540, 392), SEC, [],
                       'A table of the six parts to label: Bowman\'s capsule, Loop of Henle, Proximal convoluted '
                       'tubule, Collecting duct, Distal convoluted tubule, Glomerulus.', False),
    'q13-table': ('040', 5, (168, 466, 512, 532), SEC, [],
                  'Table of composition in grams per 100 cm3 of fluid. Urea: blood plasma 0.03, glomerular filtrate '
                  '0.03, urine 1.8. Glucose: 0.1, 0.1, 0. Proteins: 7, 0, 0.', False),
    'q14-cycle': ('040', 6, (124, 150, 545, 322), SEC, [],
                  'Diagram of the menstrual cycle over days 1 to 28: the top row shows a follicle developing, '
                  'bursting at day 14 and then changing into a body that shrinks; the bottom row shows the uterine '
                  'lining breaking away from day 1 to day 5, then thickening steadily to day 28.', False),
    'q14-growth': ('040', 7, (210, 238, 400, 432), SEC, ['A', 'B', 'C'],
                   'Growth curve for microorganisms: the y-axis is labelled Y and the x-axis Time (hours). The line '
                   'starts flat at A, rises steeply at B, levels off at C, then falls.', False),
    'q15-iaa': ('040', 8, (150, 288, 470, 516), SEC, [],
                'Graph of growth promotion (+) above zero and inhibition (-) below against IAA concentration from '
                '0.001 to 100 mg/l, low to high. The root line (solid) rises to a peak at about 0.01 and falls below '
                'zero from about 0.1; the shoot line (dashed) rises to a higher peak at about 1.0 and falls below '
                'zero near 100.', False),
}
