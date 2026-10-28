"""Biology 2017 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-24), every page rendered and read:
  * The 2017 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p6 Section A Questions 1-6, p7-p9 Section B Questions 7-9, p10-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q13(a) photograph carries no credit.
  * The marking scheme, 24 pages: p1 cover, p2 note, p3 introduction and
    cancelled answers, p4 surplus answers and conventions, p5 conventions
    (ordered splits), p6-p21 Questions 1-15, p22-p23 "Blank Page", p24 back
    cover.

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c). Every printed ask is carded.

Tariffs. Q1 is "5(4) i.e. best five answers from (a) - (f)". Q2-Q6 are
ordered splits carded at their first rate ("2(5) + 5(2)", "2(4) + 6(2)",
"5(3) + 5(1)"). Section B prints "2(3)" for each (a) (two parts at 3) and
an ordered split for each (b) ("4(4) + 8(1)", "4(4) + 4(2)"). Section C
prints a mark per row for each (a) and an ordered split for each (b) and
(c) ("3(4) + 3(3) + 3(2)", "3(4) + 2(3) + 3(2)"), except Q13(c): (i) "4",
the anaphase diagram "4, 2, 0" with its labels "2(2)", and two ordered
splits "4 + 2" over (iii) and (iv). Q14 and Q15 parts are "5(4)+5(2)".
A part the scheme prices on its own beside a ladder keeps its marks
(LADDER_EXEMPT) and is counted as that question's fixed units (LADDER_OF).

Two Q1 parts print answers with no per-response tariff they fit: (c) a
mineral and its matching role, (d) "Any two" reasons, each part worth the
"5(4)"'s 4. Each is carded whole at 4 (questionTotal), the rows unpriced.

The scheme prints Q5's key as the letters T and F in its True and False
columns (no ticks); each is read from its own column cell on the page.

Printed choices the scheme marks differently per option are routes:
Q8(b)(ii) and (iv) catalase or amylase (the scheme's two boxed columns and
its "Catalase: ... OR Amylase: ..." lines), Q15(a)(v) asthma or bronchitis.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, G

YEAR, LEVEL = 2017, 'hl'
REVIEWED_AT = '2026-10-24'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2017-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': 'd87229756fb90df6dab5d4f7703e9c749f34716fb633d20f76a75614a2a7fa64',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2017-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '9a1d6777f5a1d9968787013a74698768febcb6af5cb01a4f4a848d335f20aadb',
               'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples', 5: 'conventions',
               **{p: 'marking' for p in range(6, 22)}, 22: 'blank', 23: 'blank', 24: 'back-cover'},
}


def _ladder(notation, **extra):
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only parts priced row by row: a ladder part's cards are carded at the
# ladder's first rate, so their sum is not the printed part total.
PART_TOTALS = {
    (1, 'c'): 4, (1, 'd'): 4,   # "5(4)": each part 4; carded whole (questionTotal)
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p7: "Part (a) carries 6 marks"
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
}
BEST_OF = {1: (5, 4)}
LADDERS = {
    2: _ladder('2(5) + 5(2)'), 3: _ladder('2(4) + 6(2)'), 4: _ladder('2(5) + 5(2)'),
    5: _ladder('2(5) + 5(2)'), 6: _ladder('5(3) + 5(1)'),
    # Section B (a) "2(3)" is two parts at 3, priced on their own beside (b)'s ladder.
    (7, 'b'): _ladder('4(4) + 8(1)', fixed={3: 2}),
    (8, 'b'): _ladder('4(4) + 4(2)', fixed={3: 2}),
    (9, 'b'): _ladder('4(4) + 4(2)', fixed={3: 2}),
    # Section C (a): a mark per row ("3", "3", "3"), beside (b)'s ladder.
    (10, 'b'): _ladder('3(4) + 3(3) + 3(2)', fixed={3: 3}), (10, 'c'): _ladder('3(4) + 2(3) + 3(2)'),
    (11, 'b'): _ladder('3(4) + 3(3) + 3(2)', fixed={3: 3}), (11, 'c'): _ladder('3(4) + 2(3) + 3(2)'),
    (12, 'b'): _ladder('3(4) + 3(3) + 3(2)', fixed={3: 3}), (12, 'c'): _ladder('3(4) + 2(3) + 3(2)'),
    (13, 'b'): _ladder('3(4) + 3(3) + 3(2)', fixed={3: 3}),
    # Q13(c): (i) "4" and (ii) "4, 2, 0" + "2(2)" priced on their own; "4 + 2"
    # over (iii)'s two answers and again over (iv)'s.
    (13, 'C3'): _ladder('4 + 2', fixed={4: 2, 2: 2}), (13, 'C4'): _ladder('4 + 2'),
    **{(n, x): _ladder('5(4) + 5(2)') for n in (14, 15) for x in 'abc'},
}
LADDER_OF = {
    **{k: (7, 'b') for k in ('7ai', '7aii')}, **{k: (8, 'b') for k in ('8ai', '8aii')},
    **{k: (9, 'b') for k in ('9ai', '9aii')},
    **{k: (10, 'b') for k in ('10ai', '10aii', '10aiii')}, **{k: (11, 'b') for k in ('11ai', '11aii')},
    '12a': (12, 'b'), **{k: (13, 'b') for k in ('13ai', '13aii')},
    '13ci': (13, 'C3'), '13cii': (13, 'C3'), '13ciii': (13, 'C3'), '13civ': (13, 'C4'),
}
LADDER_EXEMPT = {'7ai', '7aii', '8ai', '8aii', '9ai', '9aii', '10ai', '10aii', '10aiii', '11ai', '11aii',
                 '12a', '13ai', '13aii', '13ci', '13cii'}

# Q1 has no checksum: its (c) and (d) are carded whole, with no units to count.
CHECKSUMS = {
    2: {5: 7}, 3: {4: 8}, 4: {5: 7}, 5: {5: 7}, 6: {3: 10},
    **{(n, 'a'): {3: 2} for n in (7, 8, 9)}, (7, 'b'): {4: 12}, (8, 'b'): {4: 8}, (9, 'b'): {4: 8},
    **{(n, 'a'): {3: 3} for n in (10, 11, 12, 13)},
    **{(n, 'b'): {4: 9} for n in (10, 11, 12, 13)},
    **{(n, 'c'): {4: 8} for n in (10, 11, 12)}, (13, 'c'): {4: 6, 2: 2},
    **{(n, x): {4: 10} for n in (14, 15) for x in 'abc'},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the best five make 20.'),
    ('paper', 2, 'the following', 'Q1 parts list.'),
    ('paper', 2, 'or', 'Q1(f) "Benedict\'s or Fehling\'s solution": either reagent; one answer.'),
    ('paper', 5, 'the following', 'Q4 lead-in "each of the following terms": every term asked, one card per letter.'),
    ('paper', 5, 'the following', 'Q5 lead-in: every statement asked, one card per letter.'),
    ('paper', 5, 'or', 'Q5 "true or false": the answer options of each statement.'),
    ('paper', 6, 'the following', 'Q6 lead-in: every part asked.'),
    ('paper', 6, 'both', 'Q6 lead-in "in both flowering plants and humans": each part asks for both; one card per letter.'),
    ('paper', 6, 'either', 'Q6(a) "If more than one type occurs in either case": description.'),
    ('paper', 7, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 7, 'the following', 'Q7(a) lead-in: every part asked.'),
    ('paper', 7, 'or', 'Q7(a)(ii) "minimised or eliminated": description.'),
    ('paper', 7, 'or', 'Q7(b)(i) "In the space below or in your answer book": where to answer.'),
    ('paper', 8, 'the following', 'Q8(a) lead-in: every part asked.'),
    ('paper', 8, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 9, 'the following', 'Q9(b)(ii) lead-in "answer the following": both numbered items asked, one card each.'),
    ('paper', 10, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 10, 'the following', 'Q10(a) lead-in: every term asked, one card each.'),
    ('paper', 10, 'or', 'Q10(b) passage "reused or recycled": description.'),
    ('paper', 10, 'one of the following', 'Q10(b)(v) a named pollutant "from one of the following areas": the scheme '
                                          'marks any relevant pollutant the same way; one card.'),
    ('paper', 11, 'both', 'Q11(b)(vii) "Name both Irish scientists": both names, one answer.'),
    ('paper', 13, 'the following', 'Q13(b) lead-in: every part asked.'),
    ('paper', 13, 'or', 'Q13(b)(ii) "anabolic or catabolic": the answer options.'),
    ('paper', 13, 'both', 'Q13(b)(iii) "both ADP and NADP+": one answer for both.'),
    ('paper', 13, 'the following', 'Q13(c) lead-in: every part asked.'),
    ('paper', 14, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'or', 'Q14(a) passage "late afternoon or evening": description.'),
    ('paper', 14, 'or', 'Q14(a) passage "a small head or the head stops growing": description.'),
    ('paper', 14, 'or', 'Q14(a)(i) "childbearing age or those who were pregnant": description.'),
    ('paper', 14, 'any three', 'Q14(b)(iii) "List any three types": a bounded menu, claim three.'),
    ('paper', 14, 'the following', 'Q14(c) lead-in "In each of the following": every structure asked, one card each.'),
    ('paper', 15, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 15, 'any two', 'Q15(b)(i) "Name any two of these regions": a bounded menu, claim two, with their numbers.'),
    ('paper', 15, 'the following', 'Q15(c) lead-in: every part asked.'),
]

ROUTES = {
    'Q8(b)(ii)1': ['catalase', 'amylase'],
    'Q8(b)(ii)2': ['catalase', 'amylase'],
    'Q8(b)(iv)': ['catalase', 'amylase'],
    'Q15(a)(v)': ['asthma', 'bronchitis'],
}

SEC = 'State Examinations Commission'
COMPRESSED = 'The scheme heads each answer with a compressed reprint of the ask.'
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_REPRINT = 'The scheme heads this part with its marker only, no reprint of the ask.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
WHOLE_PART = ('The scheme prints Q1 as "5(4) i.e. best five answers from (a) - (f)": this part is worth 4, '
              'and the scheme prints its answers with no split of the 4 between them, so the part is carded '
              'whole at its 4, the rows unpriced.')


def item(page, n, end, anchor):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, after=anchor, br=True)


def tf(clip, answer):
    """Q5's key: the letter the scheme prints in the True or False column cell."""
    return G('tokens', page=8, clip=clip, expect=answer, marks=5)


TRUE_X, FALSE_X = (440, 490), (490, 560)

Q1 = Q(2, 'Answer any five of the following parts (a) to (f):')
Q4 = Q(5, 'From your knowledge of microorganisms, explain what is meant by each of the following terms.')
Q5 = Q(5, 'Indicate whether the following statements are true or false by placing a tick (✓) in the',
       'appropriate box in each case.')
Q6 = Q(6, 'The following questions refer to sexual reproduction in both flowering plants and humans.')
Q7A = Q(7, 'Answer the following questions by reference to a named ecosystem which you have', 'investigated.')
Q8A = Q(8, 'Answer the following in relation to enzymes.')
Q8B = Q(8, 'Answer the following in relation to an investigation you carried out into the effect of pH on',
        'the rate of enzyme activity.')
Q8BI = Q(8, 'Name the enzyme that you used in this investigation.')
Q9BI = Q(9, 'When investigating the conditions necessary for seed germination, describe how you:')
Q9BII = Q(9, 'In relation to an investigation you carried out to prepare and examine with a',
          'microscope a transverse section of a dicotyledonous stem, answer the following.')
Q9BIII = Q(9, 'When demonstrating osmosis:')
Q9BIV = Q(9, 'When isolating DNA from plant tissue:')
Q10A = Q(10, 'Explain the following terms as used in ecology.')
Q10B = Q(10, 'A new waste‐to‐energy incinerator is currently being built in Poolbeg, Dublin. The facility',
         'will generate energy from domestic waste that cannot be reused or recycled.')
Q10BV = Q(10, 'Give an account of the effect of a named pollutant from one of the following areas:',
          'domestic, agriculture, industry.')
Q10CII = Q(10, 'Draw a graph, appropriately labelling axes and curves, to show how population',
           'numbers fluctuate in a predator‐prey relationship.')
Q11AI = Q(11, 'Name the vascular tissue through which the products of photosynthesis are transported', 'in plants.')
Q11B = Q(11, 'The graph shows the relationship between the rate of transpiration and the rate of water',
         'uptake for a particular plant on a fine summer day.')
Q12C = Q(12, 'DNA contains the genetic code for the formation of all proteins.')
Q13A = Q(13, 'The photograph below shows a system of promoting grass growth on a football pitch', 'photosynthesis.')
Q13AI = Q(13, 'Give two ways, other than the method shown in the photograph, by which',
          'photosynthesis could be accelerated in horticulture.')
Q13B = Q(13, 'Answer the following questions about photosynthesis.')
Q13C = Q(13, 'Answer the following questions in relation to the cell cycle.')
Q14A = [Q(14, 'Read the passage below and answer the questions that follow.'),
        Q(14, 'Zika virus is a mosquito‐borne virus.', 'Games.')]
Q14C = Q(14, 'In each of the following, state two features that show how the named structure is adapted',
         'to carry out the named function.')
Q15B = Q(15, 'The vertebral column is part of the human axial skeleton and is composed of bones called',
         'vertebrae, with intervertebral discs.')
Q15BIII = Q(15, 'Bone tissue is continually broken down and reformed during life.')
Q15C = Q(15, 'Answer the following questions in relation to human sexual reproduction.')
Q15CI = Q(15, 'During in vitro fertilisation treatment (IVF) several eggs are removed from the woman.')

# Q15(b)(i): the scheme's table, each region's name over its number, read column by column.
REGIONS = [((135, 120, 195, 190), 'cervical — 7'), ((195, 120, 260, 190), 'thoracic — 12'),
           ((260, 120, 315, 190), 'lumbar — 5'), ((315, 120, 365, 190), 'sacral — 5'),
           ((365, 120, 428, 190), 'coccygeal — 4')]


def plants_humans(plant_head, plant_ans, human_head, human_ans, plant_note=None):
    """Q6: the scheme's flowering-plant row and human row, each labelled with
    the words its own reprint ends on ("... in flowering plants:")."""
    return [pt(S(*plant_ans), 3, label=S(plant_head, after='6.', piece=2, psep=' in '),
               note_sel=S(plant_note) if plant_note else None),
            pt(S(*human_ans, after=human_head), 3, label=S(human_head, piece=2, psep=' in '))]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', Q(2, 'Name a protein that has a fibrous structure.'),
      [pt(S('Keratin or collagen or other fibrous protein'), 4)], 'bio-1-2', 'fibrous-protein',
      SQ(6, 'Fibrous protein:'), 4, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', Q(2, 'Where in the human body would you expect to find the fibrous protein referred to above?'),
      [pt(S('Must match named fibrous protein'), 4, kind='criterion', note=NO_ANSWER)], 'bio-1-2',
      'where-fibrous-protein-is-found', SQ(6, 'Location of fibrous protein:'), 4,
      stem=[Q1, M('(a)', 2), Q(2, 'Name a protein that has a fibrous structure.')]),
    T('1c', 'Q1(c)', 'A', Q(2, 'Give a role of a named mineral, other than calcium, which is required by plants.'),
      [pt(S('e.g. Magnesium (or Mg)'), None, label=S('Plant mineral:', after='1.')),
       pt(S('Must match named mineral'), None, kind='criterion', label=S('Role:'), note=NO_ANSWER)],
      'bio-1-2', 'mineral-for-plants', SQ(6, 'Plant mineral:'), 4, stem=[Q1], tariff='questionTotal',
      decision=WHOLE_PART + ' The answers: a mineral (the scheme prints Magnesium as its example) and a role that '
                            'matches it.'),
    T('1d', 'Q1(d)', 'A', Q(2, 'State two reasons why water is required by living organisms.'),
      [anyn(S('Solvent (or example of solvent)/ reaction medium/ transport/ reactant (or example of',
              'regulation/ turgidity in cells or turgor in plants'), 2, None, note_sel=S('Any two'))],
      'bio-1-2', 'why-water-is-needed', SQ(6, 'Why organisms need water:'), 4, stem=[Q1], tariff='questionTotal',
      decision=WHOLE_PART + ' The answers: any two of the printed reasons.'),
    T('1e', 'Q1(e)', 'A', Q(2, 'Name the metallic element present in haemoglobin.'),
      [pt(S('Iron (or Fe)'), 4)], 'bio-1-2', 'iron-in-haemoglobin',
      SQ(6, 'Metal in haemoglobin:', paired=COMPRESSED), 4, stem=[Q1]),
    T('1f', 'Q1(f)', 'A', Q(2, 'Which type of food biomolecule may be identified by the use of Benedict’s or Fehling’s',
                            'solution?'),
      [pt(S('Reducing sugar'), 4)], 'bio-1-2', 'benedicts-test', SQ(6, 'What identified by Benedict’s or Fehling’s:'),
      4, stem=[Q1]),
] + [
    T(f'2{x}', f'Q2({x})', 'A', Q(3, *ask), [pt(S(*ans), 5, note_sel=S(note) if note else None)], 'bio-3-2',
      concept, SQ(6, sq, paired=COMPRESSED if paired else None), 5)
    for x, ask, ans, note, concept, sq, paired in [
        ('a', ('Why is it important that nutrients are recycled in nature?',),
         ('So can be reused or used by other organisms',), None, 'why-recycle-nutrients', 'Why nutrients recycled:',
         False),
        ('b', ('During the nitrogen cycle, nitrogen from the air is converted to nitrates.', 'Of what benefit is this?'),
         ('Plants can absorb (or use or avail of) nitrate',), None, 'benefit-of-nitrates',
         'Benefit of N2 changing to nitrates:', True),
        ('c', ('Nitrates are formed directly from other molecules in the soil.', 'Name one of these molecules.'),
         ('Nitrite (NO2-) [allow ammonia]',), None, 'nitrite', 'Nitrate in soil formed directly from:', False),
        ('d', ('Mention one role of animals, other than as consumers, in the nitrogen cycle.',),
         ('Excrete (or egest) nitrogen (compounds) or die (or decay or decompose) and release', '(compounds)'),
         None, 'animals-in-the-nitrogen-cycle', 'Animal role (not consumer) in N-cycle:', False),
        ('e', ('Name the family of plants which have a symbiotic relationship with nitrogen‐fixing bacteria.',),
         ('Legumes',), None, 'legumes', 'Plants in symbiosis with N-fixing bacteria:', True),
        ('f', ('The nitrogen in the air is converted to nitrates but the percentage of nitrogen in the air',
               'does not change. What process is responsible for this?'),
         ('Denitrification or described',), None, 'denitrification', 'Process keeping N2 in air constant:', True),
        ('g', ('What is the role of modern fertilisers in the nitrogen cycle?',),
         ('Supply nitrate (or other valid example) (to the soil) or supply fixed (or soluble or usable)',
          'nitrogen (to the soil)'), None, 'fertilisers-in-the-nitrogen-cycle', 'Fertilisers’ role in N-cycle:',
         False)]
] + [
    T(f'3a-{x.lower()}', 'Q3(a)', 'A', Q(4, 'Name the molecules labelled A and B.'),
      [pt(S(line, piece=2, psep=' = '), 4)], 'bio-1-3', concept,
      SQ(7, '(a)', path=['3.'], bare=True, paired=NO_REPRINT + ' It names each letter on its own line ("A = ...").'),
      4, stem=[Q(4, 'The diagram below shows part of the ultrastructure of a cell membrane.')], fig='q3-membrane',
      item=(x.lower(), x), decision=EACH_ITEM.replace('A numbered list', 'A lettered figure'),
      labels=[L(y, S(ln, page=7, piece=2, psep=' = '), y == x) for y, ln in
              [('A', 'A = Protein'), ('B', 'B = Lipid or phospholipid or fatty acid')]])
    for x, line, concept in [('A', 'A = Protein', 'membrane-protein'),
                             ('B', 'B = Lipid or phospholipid or fatty acid', 'membrane-lipid')]
] + [
    T('3b', 'Q3(b)', 'A', Q(4, 'Molecules can move through cell membranes by various processes.', 'Name two such processes.'),
      [anyn(S('Osmosis/ diffusion/ active transport'), 2, 4)], 'bio-2-6', 'movement-across-membranes',
      SQ(7, 'How molecules get through membranes:'), 8,
      stem=[Q(4, 'The diagram below shows part of the ultrastructure of a cell membrane.')], fig='q3-membrane'),
    T('3c', 'Q3(c)', 'A', Q(4, 'Suggest a reason why the organelle involved in aerobic respiration is found in different',
                            'amounts in different cells.'),
      [pt(S('(Cells) need different amounts of energy'), 4)], 'bio-1-3', 'numbers-of-mitochondria',
      SQ(7, 'Why different amounts of aerobic respiration organelle:'), 4),
    T('3d', 'Q3(d)', 'A', Q(4, 'What term is used to describe organisms whose cells contain a nucleus?'),
      [pt(S('Eukaryotes (eukaryotic)'), 4)], 'bio-1-3', 'eukaryotes', SQ(7, 'Organisms whose cells have a nucleus:'), 4),
    T('3e', 'Q3(e)', 'A', Q(4, 'What term is used to describe organisms that do not have nuclei?'),
      [pt(S('Prokaryotes (prokaryotic) or bacteria (or Monera)'), 4)], 'bio-1-3', 'prokaryotes',
      SQ(7, 'Organisms lacking nuclei:'), 4),
    T('3f', 'Q3(f)', 'A', Q(4, 'Name an organelle other than the nucleus which contains genetic material.'),
      [pt(S('Mitochondrion or chloroplast'), 4)], 'bio-1-3', 'organelles-with-dna',
      SQ(7, 'Organelle (not nucleus) that has genetic material:'), 4),
] + [
    T(f'4{x}', f'Q4({x})', 'A', Q(5, word), [pt(S(*ans), 5)], 'bio-3-2', concept, SQ(7, sq), 5, stem=[Q4])
    for x, word, ans, concept, sq in [
        ('a', 'Pathogen.', ('Disease-causing (organism or agent)',), 'pathogen', 'Pathogen:'),
        ('b', 'Saprophyte.', ('(An organism that) feeds on dead (or decaying) matter',), 'saprophyte', 'Saprophyte:'),
        ('c', 'Heterotroph.', ('(An organism that) obtains its food from other organisms or feeds on organic material or',
                               'cannot make its own food'), 'heterotroph', 'Heterotroph:'),
        ('d', 'Antibiotic.', ('(Chemical) produced by microorganisms (or bacteria and fungi) to kill (or stop growth of)',
                              'other microorganisms (or bacteria or fungi)'), 'antibiotic', 'Antibiotic:'),
        ('e', 'Asepsis.', ('Free of pathogens',), 'asepsis', 'Asepsis:'),
        ('f', 'Bioprocessing.', ('Using microorganisms (or enzymes or cells) to form products',), 'bioprocessing',
         'Bioprocessing:'),
        ('g', 'Bioreactor.', ('Vessel (or described) in which products are made by microorganisms (or enzymes or',
                              'cells) or vessel in which bioprocessing occurs'), 'bioreactor', 'Bioreactor:')]
] + [
    T(f'5{x}', f'Q5({x})', 'A', Q(5, start), [tf((cx[0], y0, cx[1], y1), answer)], 'bio-2-2', concept,
      SQ(8, sq, paired=COMPRESSED if paired else None), 5, stem=[Q5],
      decision='The scheme prints the answer as the letter ' + answer + ' in its ' +
               ('True' if answer == 'T' else 'False') + ' column, read from that cell.')
    for x, start, sq, y0, y1, cx, answer, concept, paired in [
        ('a', 'Aerobic respiration occurs entirely in the cytosol.', 'Aerobic respiration occurs entirely in the cytosol:',
         100, 130, FALSE_X, 'F', 'where-aerobic-respiration-happens', False),
        ('b', 'Glycolysis is an anaerobic process.', 'Glycolysis is anaerobic:', 130, 158, TRUE_X, 'T',
         'glycolysis-is-anaerobic', False),
        ('c', 'None of the energy released in respiration is lost as heat.', 'No energy from respiration lost as heat:',
         158, 187, FALSE_X, 'F', 'energy-lost-as-heat', False),
        ('d', 'In respiration, all of the ATP molecules are produced in the Krebs cycle.',
         'All respiration ATP made in Krebs cycle:', 187, 216, FALSE_X, 'F', 'where-atp-is-made', False),
        ('e', 'ADP requires an input of energy to produce ATP.', 'ADP needs energy to make ATP:', 216, 245, TRUE_X,
         'T', 'making-atp', True),
        ('f', 'When glucose is fermented by yeast, ethanol and water are formed.',
         'Ethanol and water made when yeast ferments glucose:', 245, 274, FALSE_X, 'F', 'products-of-fermentation',
         False),
        ('g', 'Fermentation releases more energy than aerobic respiration.',
         'More energy released from fermentation than from aerobic respiration:', 274, 302, FALSE_X, 'F',
         'energy-from-fermentation', False)]
] + [
    T('6a', 'Q6(a)', 'A', Q(6, 'Which types of cell division occur during production of the female gametes in flowering',
                            'in which they occur.'),
      plants_humans('Which type(s) of cell division form(s) female gametes in flowering plants:',
                    ('Meiosis (followed by) mitosis',),
                    'Which type(s) of cell division forms(s) female gametes in humans:', ('Meiosis',)),
      'bio-2-5', 'forming-female-gametes', SQ(8, 'Which type(s) of cell division form(s) female gametes in flowering plants:'),
      6, stem=[Q6], decision='The plant and the human answers are two responses on the ladder.'),
    T('6b', 'Q6(b)', 'A', Q(6, 'Give the precise location of the production of the female gametes.'),
      plants_humans('Precise location of production of female gametes in flowering plants:', ('Embryo sac',),
                    'Precise location of production of female gametes in humans:',
                    ('(Graafian) follicle [allow ovary]',), plant_note='[allow ovule]'),
      'bio-2-5', 'where-female-gametes-form',
      SQ(8, 'Precise location of production of female gametes in flowering plants:'), 6, stem=[Q6]),
    T('6c', 'Q6(c)', 'A', Q(6, 'Give the precise location of fertilisation under normal circumstances.'),
      plants_humans('Precise location of normal fertilisation in flowering plants:', ('Embryo sac',),
                    'Precise location of normal fertilisation in humans:', ('Oviduct (Fallopian tube)',),
                    plant_note='[allow ovule]'),
      'bio-2-5', 'where-fertilisation-happens', SQ(8, 'Precise location of normal fertilisation in flowering plants:'),
      6, stem=[Q6]),
    T('6d', 'Q6(d)', 'A', Q(6, 'Name the next stage of development following formation of the zygote.'),
      plants_humans('Next stage after zygote in flowering plants:', ('Embryo',),
                    'Next stage after zygote in humans:', ('Morula',)),
      'bio-2-5', 'after-the-zygote', SQ(8, 'Next stage after zygote in flowering plants:'), 6, stem=[Q6]),
    T('6e', 'Q6(e)', 'A', Q(6, 'Give an advantage and a disadvantage of sexual reproduction in organisms.'),
      [pt(S('(Increased) variation (or described)'), 3, label=S('Advantage of sexual reproduction:', after='6.')),
       pt(S('Requires two parents (or difficulty in finding a mate) or longer (or more complex) life',
            'cycle (or to maturity)'), 3, label=S('Disadvantage of sexual reproduction:'),
          note_sel=S('[allow (increased) variation if potential disadvantage is explained]'))],
      'bio-2-5', 'sexual-reproduction', SQ(8, 'Advantage of sexual reproduction:'), 6, stem=[Q6]),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', Q(7, 'Give one example of a possible error in ecological surveying.'),
      [pt(S('Non-random (or biased) or misidentification or miscounting or sample size too', 'small or quadrat size unsuitable'),
          3)], 'bio-3-1', 'surveying-errors', SQ(9, 'One possible ecological surveying error:'), 3, stem=[Q7A],
      decision='Section B (a) is "2(3)": each part 3, priced on its own.'),
    T('7aii', 'Q7(a)(ii)', 'B', Q(7, 'Suggest how this error might be minimised or eliminated.'),
      [pt(S('Method of minimisation must be described and match possible error given above'), 3, kind='criterion',
          note=NO_ANSWER)], 'bio-3-1', 'minimising-surveying-errors', SQ(9, 'How might this error be minimised:'), 3,
      stem=[Q7A, M('(i)', 7), Q(7, 'Give one example of a possible error in ecological surveying.')],
      decision='Section B (a) is "2(3)": each part 3, priced on its own.'),
    T('7bi', 'Q7(b)(i)', 'B', [Q(7, 'As part of your study you constructed a food web. In the space below or in your',
                                 'containing:'),
                               Q(7, '1. At least three food chains, and', br=True),
                               Q(7, '2. At least four trophic levels.', br=True)],
      [pt(S('Three interlinked valid food chains'), 4, kind='criterion', note=NO_ANSWER),
       pt(S('Four valid trophic levels in at least one of the food chains'), 4, kind='criterion', note=NO_ANSWER)],
      'bio-3-1', 'food-web', SQ(9, 'Food web diagram:'), 8, stem=[Q7A],
      decision='The food web is the student\'s own: the scheme prints its two criteria, each a response on the ladder.'),
    T('7bii', 'Q7(b)(ii)', 'B', Q(7, 'Many animals must be captured for identification and counting in ecological',
                                  'capture. Give an example of one such adaptive feature.'),
      [pt(S('Appropriate adaptive feature named'), 4, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'escape-adaptation', SQ(9, 'Animal adaptive feature:'), 4),
    T('7biii', 'Q7(b)(iii)', 'B', Q(7, 'Explain how this adaptation helps the animal escape capture.'),
      [pt(S('Matching benefit'), 4, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'how-the-adaptation-helps',
      SQ(9, 'How adaptive feature helps animal escape capture:'), 4,
      stem=[M('(ii)', 7), Q(7, 'Many animals must be captured for identification and counting in ecological',
                             'capture. Give an example of one such adaptive feature.')]),
    T('7biv', 'Q7(b)(iv)', 'B', Q(7, 'Suggest why ecological surveying is important.'),
      [pt(S('Monitors biodiversity or detects changes or pollution monitoring or to provide',
            'baseline (for comparison) or example described'), 4)], 'bio-3-1', 'why-survey',
      SQ(9, 'Why ecological surveying important:'), 4),
    T('7bv', 'Q7(b)(v)', 'B', Q(7, 'Describe how you carried out a quantitative survey of a plant species named in your',
                                'food web above.'),
      [anyn(S('Quadrat/ random/ how random/ count (or estimate cover)/ repeat/ several times/',
              'frequency (or % cover))'), 7, 4)], 'bio-3-1', 'quantitative-plant-survey',
      SQ(9, 'Plant quantitative survey description:'), 28),
    T('8ai', 'Q8(a)(i)', 'B', Q(8, 'Give a factor, other than pH, which affects enzyme activity.'),
      [pt(S('Temperature'), 3)], 'bio-2-1', 'factors-affecting-enzymes',
      SQ(10, 'Factor other than pH that affects enzyme activity:'), 3, stem=[Q8A],
      decision='Section B (a) is "2(3)": each part 3, priced on its own.'),
    T('8aii', 'Q8(a)(ii)', 'B', Q(8, 'Explain the term optimum activity.'),
      [pt(S('(Enzyme) working at its most efficient (or best) or best rate'), 3, note_sel=S('[allow fastest (rate)]'))],
      'bio-2-1', 'optimum-activity', SQ(10, 'Optimum activity:'), 3, stem=[Q8A],
      decision='Section B (a) is "2(3)": each part 3, priced on its own.'),
    T('8bi', 'Q8(b)(i)', 'B', Q8BI,
      [anyn(None, 1, 4, options=[S('Catalase'), S('Amylase')])], 'bio-2-1', 'enzyme-for-ph',
      SQ(10, 'Enzyme used:'), 4, stem=[Q8B],
      decision='The scheme prints two enzymes in boxed columns joined by "OR": one menu, claim one.'),
] + [
    T('8bii1', 'Q8(b)(ii)1', 'B', [Q(8, 'State:'), item(8, 1, 'The source of this enzyme.', 'State:')],
      [pt(S(src), 4, note_sel=S('Source must match named enzyme'))], 'bio-2-1', f'source-of-{route}',
      SQ(10, 'Enzyme source:'), 4, route=route, stem=[Q8B, M('(i)', 8), Q8BI],
      decision='Catalase or amylase: the scheme prints each enzyme\'s answers in its own column, joined by "OR", '
               'so each is a route card. ' + EACH_ITEM)
    for route, src in [('catalase', 'e.g. Celery'), ('amylase', 'e.g. Saliva')]
] + [
    T('8bii2', 'Q8(b)(ii)2', 'B', [Q(8, 'State:'), item(8, 2, 'The substrate of this enzyme.', 'State:')],
      [pt(S(*sub), 4, note_sel=S('Substrate must match either named enzyme or source'))], 'bio-2-1',
      f'substrate-of-{route}', SQ(10, 'Enzyme substrate:'), 4, route=route, stem=[Q8B, M('(i)', 8), Q8BI],
      decision='Catalase or amylase: the scheme prints each enzyme\'s answers in its own column, joined by "OR", '
               'so each is a route card. ' + EACH_ITEM)
    for route, sub in [('catalase', ('Hydrogen peroxide', '(or H2O2)')), ('amylase', ('Starch', '(or amylose)'))]
] + [
    T('8biii', 'Q8(b)(iii)', 'B', Q(8, 'Explain why changing the pH would have an effect on enzyme activity.'),
      [pt(S('Active site shape is altered or (enzyme is) denatured'), 4)], 'bio-2-1', 'ph-and-enzymes',
      SQ(10, 'Why pH change affects enzyme activity:', paired=COMPRESSED), 4, stem=[Q8B]),
] + [
    T('8biv', 'Q8(b)(iv)', 'B', Q(8, 'How did you measure the rate of enzyme activity?'),
      [pt(S(a), 4, label=S(lab), note_sel=S('Must match named enzyme')), pt(S(b), 4, label=S(lab))],
      'bio-2-1', f'measuring-{route}-activity', SQ(10, 'How measured enzyme rate:'), 8, route=route, stem=[Q8B],
      decision='Catalase or amylase: the scheme prints each enzyme\'s two answers under its own name, joined by '
               '"OR", so each is a route card.')
    for route, lab, a, b in [('catalase', 'Catalase:', 'Measure (volume or height of) foam', 'Per minute'),
                             ('amylase', 'Amylase:', 'Measure time', 'For blue-black to disappear')]
] + [
    T('8bv', 'Q8(b)(v)', 'B', Q(8, 'Label the axes and sketch a graph to show the effect of pH on enzyme activity.'),
      [pt(S('Y-axis = activity (or rate) and X-axis = pH'), 4),
       pt(S('(Sharply) up and down'), 4, kind='criterion', label=S('Plot:'))], 'bio-2-1', 'ph-graph',
      SQ(10, 'Axes:'), 8, stem=[Q8B], qfig='q8b-v-axes',
      decision='The axes and the plot are two responses on the ladder; the printed axes are shown as printed.'),
    T('9ai', 'Q9(a)(i)', 'B', Q(9, 'What is the purpose of replicates in scientific experimentation?'),
      [pt(S('To ensure reliability or to verify result or to avoid bias'), 3)], 'bio-u2', 'replicates',
      SQ(11, 'Why replicates:'), 3, decision='Section B (a) is "2(3)": each part 3, priced on its own.'),
    T('9aii', 'Q9(a)(ii)', 'B', Q(9, 'What is meant by the term hypothesis?'),
      [pt(S('An untested explanation (of an observed phenomenon) or described'), 3)], 'bio-u2', 'hypothesis',
      SQ(11, 'Hypothesis:'), 3, decision='Section B (a) is "2(3)": each part 3, priced on its own.'),
] + [
    T(f'9b{r}{n}', f'Q9(b)({r}){n}', 'B', item(9, n, end, anchor), [pt(S(*ans), 4)], topic, concept,
      SQ(11, sq, paired=COMPRESSED if paired else None), 4, stem=[stem], decision=EACH_ITEM)
    for r, n, end, anchor, stem, ans, topic, concept, sq, paired in [
        ('i', 1, 'Provided an oxygen‐free environment.', 'describe how you:', Q9BI,
         ('Anaerobic jar or boiled water which has been cooled (or oil-covered)',), 'bio-2-5',
         'germination-without-oxygen', 'How ensured no oxygen:', True),
        ('i', 2, 'Determined that germination had taken place.', 'describe how you:', Q9BI,
         ('Radicles (roots) observed or plumules (shoots) observed',), 'bio-2-5', 'signs-of-germination',
         'Germination determination:', True),
        ('ii', 1, 'How did you prepare the section?', 'microscope a transverse section', Q9BII,
         ('Cut a thin (section) or add water or add stain',), 'bio-2-6', 'preparing-a-stem-section',
         'How prepared section:', True),
        ('ii', 2, 'Why is a coverslip used?', 'microscope a transverse section', Q9BII,
         ('To prevent (cells) from drying out or to protect the lens or to make it easier', 'to see or to keep sample in place'),
         'bio-2-6', 'why-a-coverslip', 'Why coverslip:', False),
        ('iii', 1, 'What did you use as a selectively‐permeable membrane?', 'When demonstrating osmosis:', Q9BIII,
         ('Visking tubing or cellophane or plant cell membrane',), 'bio-2-6', 'selectively-permeable-membrane',
         'Selectively permeable membrane:', False),
        ('iii', 2, 'What led you to conclude that osmosis had occurred?', 'When demonstrating osmosis:', Q9BIII,
         ('Increase in mass (or volume) of the more concentrated solution (or solution', 'in tubing)'), 'bio-2-6',
         'evidence-of-osmosis', 'How know osmosis occurred:', False),
        ('iv', 1, 'Give a reason for adding salt (NaCl) to the chopped plant tissue.', 'When isolating DNA from plant tissue:',
         Q9BIV, ('To clump DNA or to separate protein from DNA or to precipitate proteins (or', 'carbohydrates)'),
         'bio-1-2', 'salt-in-dna-isolation', 'Why salt added:', False),
        ('iv', 2, 'liquid kept at 60 °C for a period of time?', 'When isolating DNA from plant tissue:', Q9BIV,
         ('To denature DNases or to denature enzymes that would destroy DNA',), 'bio-1-2', 'heating-in-dna-isolation',
         'Why 60 °C:', False)]
] + [
    # ------------------------------------------------------------ Section C --
    T(f'10a{r}', f'Q10(a)({r})', 'C', Q(10, word), [pt(S(*ans), 3)], 'bio-3-1', concept, SQ(12, sq), 3,
      stem=[Q10A], decision='The scheme prints a mark per row in Q10(a): "3".')
    for r, word, ans, concept, sq in [
        ('i', 'Scramble competition.', ('A struggle for a (scarce) resource and all get some',), 'scramble-competition',
         'Scramble competition:'),
        ('ii', 'Ecosystem.', ('Organisms (or plants and animals) and (their interactions with) their', 'environment'),
         'ecosystem', 'Ecosystem:'),
        ('iii', 'Conservation.', ('Management of the environment or maintenance of biodiversity',), 'conservation',
         'Conservation:')]
] + [
    T('10bi', 'Q10(b)(i)', 'C', Q(10, 'Suggest two reasons why this new incinerator is located in Dublin.'),
      [anyn(S('Large population so a lot of waste/ large population so high energy',
              'buildings/ extensive transport links for waste'), 2, 4)], 'bio-3-1', 'siting-an-incinerator',
      SQ(12, 'Why incinerator in Dublin:'), 8, stem=[Q10B]),
    T('10bii', 'Q10(b)(ii)', 'C', Q(10, 'Give one advantage and one disadvantage of incineration in waste disposal.'),
      [pt(S('Amount of waste reduced or useable heat (or energy) or reduced', 'landfill or quick waste disposal'), 4,
          label=S('Advantage of incineration:', after='10.')),
       pt(S('Harmful products or named example'), 4, label=S('Disadvantage of incineration:'))], 'bio-3-1',
      'incineration', SQ(12, 'Advantage of incineration:'), 8, stem=[Q10B]),
    T('10biii', 'Q10(b)(iii)', 'C', Q(10, 'What is the main role of microorganisms in waste disposal?'),
      [pt(S('Decomposers (or described)'), 4)], 'bio-3-1', 'microorganisms-in-waste-disposal',
      SQ(12, 'Main role of microorganisms:'), 4, stem=[Q10B]),
    T('10biv', 'Q10(b)(iv)', 'C', Q(10, 'What is meant by the term pollutant?'),
      [pt(S('Any harmful addition to the environment'), 4)], 'bio-3-1', 'pollutant', SQ(12, 'Pollutant:'), 4,
      stem=[Q10B]),
    T('10bv', 'Q10(b)(v)', 'C', Q10BV,
      [pt(S('Any relevant pollutant'), 4, kind='criterion', note=NO_ANSWER),
       pt(S('Effect (must match)'), 4, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'pollutant-and-effect',
      SQ(12, 'Effect of particular pollutant:'), 8, stem=[Q10B]),
    T('10bvi', 'Q10(b)(vi)', 'C', Q(10, 'Describe how the pollutant referred to in (v) is controlled.'),
      [pt(S('Matching control measure for pollutant named in (v)'), 4, kind='criterion', note=NO_ANSWER)],
      'bio-3-1', 'controlling-pollution', SQ(12, 'How pollutant controlled:'), 4,
      stem=[Q10B, M('(v)', 10), Q10BV]),
    T('10ci', 'Q10(c)(i)', 'C', Q(10, 'List two species from an ecosystem you have studied, which are involved in a',
                                  'predator‐prey relationship.'),
      [pt(S('Any named predator and matching prey'), 4, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'predator-and-prey', SQ(12, 'A predator and its prey:'), 4,
      decision='The scheme prices the named pair as one response.'),
    T('10cii', 'Q10(c)(ii)', 'C', Q10CII,
      [pt(S('X-axis = Time and Y-axis = Number or population'), 4),
       pt(S('Most prey peaks higher than predator peaks (at least one labelled and', 'at least 2 peaks for each curve)'),
          4, kind='criterion', label=S('Predator-prey graph:')),
       pt(S('Predator and prey curves out of sync'), 4, kind='criterion', label=S('Predator-prey graph:'))],
      'bio-3-1', 'predator-prey-graph', SQ(12, 'Axes:'), 12,
      decision='The axes and the two features of the curves are three responses on the ladder.'),
    T('10ciii', 'Q10(c)(iii)', 'C', Q(10, 'Explain the fluctuations shown in the graph.'),
      [pt(S('Increased prey (population) allows increased predator (population)'), 4),
       pt(S('As prey (numbers) decline, predator (numbers) decline'), 4),
       pt(S('Time lag for predator (numbers) to respond (to lower or higher prey', 'numbers) (or described)'), 4)],
      'bio-3-1', 'predator-prey-explanation', SQ(12, 'Fluctuation explanations:', paired=COMPRESSED), 12,
      stem=[M('(ii)', 10), Q10CII],
      notes='"The graph" is the one the student draws in (ii); the paper prints no graph for this part.'),
    T('10civ', 'Q10(c)(iv)', 'C', Q(10, 'Outline a role in nature of such a predator‐prey relationship.'),
      [pt(S('Population control (or described) or natural selection in action'), 4)], 'bio-3-1',
      'role-of-predation', SQ(12, 'Role in nature of predator-prey relationship:'), 4),
    T('11ai', 'Q11(a)(i)', 'C', Q11AI, [pt(S('*Phloem'), 3)], 'bio-2-6', 'phloem',
      SQ(13, 'Vascular tissue that transports photosynthesis products:'), 3,
      decision='The scheme prints a mark per row in Q11(a): "3" and "2(3)".'),
    T('11aii', 'Q11(a)(ii)', 'C', Q(11, 'Give two structural features of the tissue referred to in (i).'),
      [anyn(S('Sieve tubes (or sieve tube elements)/ companion cells/ sieve plates/', 'cytoplasm pushed to edges'), 2, 3)],
      'bio-2-6', 'structure-of-phloem', SQ(13, 'Structural features of phloem:'), 6, stem=[M('(i)', 11), Q11AI],
      decision='The scheme prints a mark per row in Q11(a): "3" and "2(3)".'),
    T('11bi', 'Q11(b)(i)', 'C', Q(11, 'Describe the relationship between the rate of transpiration and the rate of water',
                                  'uptake during the day. Suggest a reason for this relationship.'),
      [pt(S('As water uptake increases (or decreases) transpiration also increases', 'together)'), 4,
          label=S('Relationship between rates of transpiration and water uptake:', after='11.')),
       pt(S('High water uptake makes more water available for transpiration or', 'lost)'), 4,
          label=S('Reason for relationship:'))], 'bio-2-6', 'transpiration-and-water-uptake',
      SQ(13, 'Relationship between rates of transpiration and water uptake:'), 8, stem=[Q11B], fig='q11b-graph'),
    T('11bii', 'Q11(b)(ii)', 'C', Q(11, 'Under what two conditions does the highest rate of transpiration occur on that day?'),
      [pt(S('Hottest (or warmest or highest temperature)'), 4), pt(S('Brightest or sunniest'), 4)], 'bio-2-6',
      'peak-transpiration', SQ(13, 'Conditions for highest transpiration rate:'), 8, stem=[Q11B], fig='q11b-graph'),
    T('11biii', 'Q11(b)(iii)', 'C', Q(11, 'Name the cells which control the opening and closing of stomata.'),
      [pt(S('*Guard cells'), 4)], 'bio-2-6', 'guard-cells', SQ(13, 'Cells controlling stomata:'), 4, stem=[Q11B],
      fig='q11b-graph'),
    T('11biv', 'Q11(b)(iv)', 'C', Q(11, 'What is the advantage to plants of having most of their stomata on the underside of the',
                                    'leaves?'),
      [pt(S('Reduces water loss by transpiration or reduces water loss by', 'evaporation'), 4)], 'bio-2-6',
      'stomata-underneath', SQ(13, 'Advantage of stomata underneath:'), 4, stem=[Q11B], fig='q11b-graph'),
    T('11bv', 'Q11(b)(v)', 'C', Q(11, 'Give a disadvantage to plants of a high rate of transpiration.'),
      [pt(S('Wilting (or described)'), 4)], 'bio-2-6', 'wilting', SQ(13, 'Disadvantage of high transpiration rate:'), 4,
      stem=[Q11B], fig='q11b-graph'),
    T('11bvi', 'Q11(b)(vi)', 'C', Q(11, 'What do plants do in response to the disadvantage referred to in (v)?'),
      [pt(S('Close stomata or stomata reduce in size'), 4)], 'bio-2-6', 'closing-stomata',
      SQ(13, 'Plant response to (v):'), 4,
      stem=[Q11B, M('(v)', 11), Q(11, 'Give a disadvantage to plants of a high rate of transpiration.')],
      fig='q11b-graph'),
    T('11bvii', 'Q11(b)(vii)', 'C', Q(11, 'Name both Irish scientists who proposed the theory of water movement in plants.'),
      [pt(S('Dixon and Joly'), 4)], 'bio-2-6', 'dixon-and-joly', SQ(13, 'Irish scientists:'), 4, stem=[Q11B],
      fig='q11b-graph', decision='The scheme prints both names as one answer, one response on the ladder.'),
    T('11ci', 'Q11(c)(i)', 'C', Q(11, 'Some plants can reproduce by means of vegetative propagation.',
                                  'Explain the term vegetative propagation.'),
      [pt(S('(Plant) asexual reproduction or explained'), 4)], 'bio-2-5', 'vegetative-propagation',
      SQ(13, 'Vegetative propagation:'), 4),
    T('11cii', 'Q11(c)(ii)', 'C', Q(11, 'Give two features of vegetative propagation.'),
      [anyn(S('No gametes (or no seeds)/ one parent/ no variation (or identical', 'offspring)'), 2, 4)], 'bio-2-5',
      'features-of-vegetative-propagation', SQ(13, 'Features of vegetative propagation'), 8),
    T('11ciii', 'Q11(c)(iii)', 'C', Q(11, 'Give one example of natural vegetative propagation from a leaf',
                                      'and one example from a bud.'),
      [pt(S('e.g. Begonia or other valid'), 4,
          label=S('Natural vegetative propagation – leaf:', after='11.', piece=2, psep=' – ')),
       pt(S('Bulb (or named example)'), 4, label=S('Natural vegetative propagation – bud:', piece=2, psep=' – '))],
      'bio-2-5', 'natural-vegetative-propagation', SQ(13, 'Natural vegetative propagation – leaf:'), 8),
    T('11civ', 'Q11(c)(iv)', 'C', Q(11, 'Artificial vegetative propagation is widely used in horticulture.',
                                    'Give two examples of artificial vegetative propagation.'),
      [anyn(S('Tissue culture/ cuttings/ grafting/ layering / budding'), 2, 4)], 'bio-2-5',
      'artificial-vegetative-propagation', SQ(13, 'Artificial vegetative propagation:'), 8),
    T('11cv', 'Q11(c)(v)', 'C', Q(11, 'Suggest a benefit of artificial vegetative propagation.'),
      [pt(S('Rapid or more reliable or desirable characteristics maintained'), 4)], 'bio-2-5',
      'benefit-of-artificial-propagation', SQ(13, 'Benefit of artificial vegetative propagation:'), 4),
    T('12a', 'Q12(a)', 'C', Q(12, 'Give a brief account of how you would produce a DNA profile.'),
      [pt(S('(DNA) cut with (restriction) enzymes'), 3), pt(S('Fragments separated'), 3),
       pt(S('According to size or by electrophoresis (or described)'), 3)], 'bio-3-3', 'dna-profiling',
      SQ(14, 'DNA profile:'), 9, decision='The scheme prints a mark per row in Q12(a): "3", "3", "3".'),
    T('12bi', 'Q12(b)(i)', 'C', Q(12, 'In the context of natural selection, explain how numbers in a population remain',
                                  'relatively constant despite the production of many offspring.'),
      [pt(S('Competition or struggle for scarce resources'), 4),
       pt(S('Best adapted (best suited) survive or non-suited don’t survive'), 4),
       pt(S('Death rate equals reproduction rate (or described)'), 4)], 'bio-1-5', 'natural-selection',
      SQ(14, 'Natural selection to explain stable population:'), 12),
    T('12bii', 'Q12(b)(ii)', 'C', Q(12, 'The son of a haemophiliac father was not haemophiliac.',
                                    'Explain in detail how this situation might have arisen.'),
      [pt(S('Haemophilia gene recessive and sex-linked'), 4), pt(S('Son: XNY-'), 4),
       pt(S('Mother: XNXN or XNXn'), 4), pt(S('Father: XnY_'), 4),
       pt(S('Son gets XN from egg (or from mother)'), 4),
       pt(S('Son gets Y_ from sperm (or from father)'), 4,
          note_sel=S('Award a maximum of two unit marks for an otherwise correct cross', 'that has no indication of gender'))],
      'bio-1-4', 'sex-linkage', SQ(14, 'How son of haemophiliac father not haemophiliac:'), 24,
      decision='Six printed answers, six responses on the ladder. The scheme sets the Y\'s dash as a small raised '
               'glyph, which the text layer reads as "_" ("XnY_", "Y_").'),
    T('12ci', 'Q12(c)(i)', 'C', Q(12, 'Name the two purine bases in DNA.'),
      [pt(S('*Adenine'), 4), pt(S('*Guanine'), 4)], 'bio-1-2', 'purines',
      SQ(14, 'Both DNA purines:', paired=COMPRESSED), 8, stem=[Q12C]),
    T('12cii', 'Q12(c)(ii)', 'C', Q(12, 'Describe fully the roles played in protein synthesis by the three different',
                                    'types of RNA.'),
      [pt(S('Messenger RNA (mRNA) gets code from DNA'), 4), pt(S('Messenger RNA (mRNA) carries code to ribosome'), 4),
       pt(S('Ribosomal RNA (rRNA) forms the ribosome (ribosomal subunits) or', 'binds (or holds) mRNA in place'), 4),
       anyn(S('Transfer RNA (tRNA) transfers amino acids to mRNA (or to',
              'acids in sequence or translates mRNA code to amino acid sequence'), 2, 4, note_sel=S('Any two'))],
      'bio-2-3', 'types-of-rna', SQ(14, 'Roles of different RNAs in protein synthesis:'), 20, stem=[Q12C],
      decision='Five responses: the two mRNA lines, the rRNA line and any two of the tRNA menu (the ladder\'s eight '
               'less (i)\'s two and (iii)\'s one).'),
    T('12ciii', 'Q12(c)(iii)', 'C', Q(12, 'Once a protein has been synthesised, a final step is required for it to become fully',
                                      'functional. What is this step?'),
      [pt(S('Folding (or described)'), 4)], 'bio-2-3', 'protein-folding', SQ(14, 'Final step for functional protein:'), 4,
      stem=[Q12C]),
    T('13ai', 'Q13(a)(i)', 'C', Q13AI,
      [pt(S('Increase CO2 (concentration)'), 3), pt(S('Increase temperature'), 3)], 'bio-2-2',
      'speeding-up-photosynthesis', SQ(15, 'Two other ways to increase rate of photosynthesis:'), 6, stem=[Q13A],
      fig='q13a-photo', decision='The scheme prints a mark per row in Q13(a): "3", "3" and "3".'),
    T('13aii', 'Q13(a)(ii)', 'C', Q(13, 'Explain how one of the methods referred to in part (i) could accelerate',
                                    'photosynthesis.'),
      [anyn(None, 1, 3, options=[S('Increased CO2 concentration: Increased supply of C (atoms) (to dark stage)'),
                                 S('Increased temperature: Increased enzyme activity')])], 'bio-2-2',
      'how-photosynthesis-is-sped-up',
      SQ(15, '(ii)', path=['13.'], bare=True, paired='The scheme heads this part "How they work", not a reprint of the ask.'),
      3, stem=[Q13A, M('(i)', 13), Q13AI], fig='q13a-photo',
      decision='Either method: the scheme prints one answer per method joined by "OR"; one menu, claim one.'),
    T('13bi', 'Q13(b)(i)', 'C', Q(13, 'In relation to electrons, describe the main events of each pathway in the light stage.'),
      [pt(S('Energised (electrons) leave the chlorophyll (molecule)'), 4),
       pt(S('(The electrons) lose energy'), 4, label=S('Pathway 1')),
       pt(S('(Same electrons) return to chlorophyll'), 4, label=S('Pathway 1')),
       anyn(S('(The electrons) lose energy /', 'different electrons go to chlorophyll', after='Pathway 2'), 2, 4,
            note_sel=S('Pathway 2'))], 'bio-2-2', 'light-stage-electrons',
      SQ(15, 'Photosynthesis electron events:'), 20, stem=[Q13B],
      decision='Five responses: the opening line, Pathway 1\'s two lines and any two of Pathway 2\'s menu.'),
    T('13bii', 'Q13(b)(ii)', 'C', Q(13, 'Is the dark stage of photosynthesis anabolic or catabolic? Explain your answer.'),
      [pt(S('Anabolic; because small molecules (CO2 and H2O) form larger molecules', '(glucose)'), 4)], 'bio-2-2',
      'dark-stage-is-anabolic', SQ(15, 'Dark stage anabolic or catabolic; and why:'), 4, stem=[Q13B],
      decision='The scheme prints the answer and its reason as one line, one response on the ladder.'),
    T('13biii', 'Q13(b)(iii)', 'C', Q(13, 'What happens to both ADP and NADP+ at the end of the dark stage?'),
      [pt(S('(Both) return to the light stage'), 4)], 'bio-2-2', 'fate-of-adp-and-nadp',
      SQ(15, 'Fate of both ADP and NADP+:'), 4, stem=[Q13B]),
    T('13biv', 'Q13(b)(iv)', 'C', Q(13, 'Name the two types of particle transferred from NADPH to CO2 in the dark stage.'),
      [pt(S('*Electrons or *e-'), 4), pt(S('*Protons or *hydrogen ions or *H+ (ions)'), 4)], 'bio-2-2',
      'what-nadph-carries', SQ(15, 'Two particle types moved from NADPH to CO2 in dark stage'), 8, stem=[Q13B]),
    T('13ci', 'Q13(c)(i)', 'C', Q(13, 'Explain the term diploid.'),
      [pt(S('Two of each chromosome or chromosomes in pairs [allow two sets of', 'chromosomes]'), 4)], 'bio-2-3',
      'diploid', SQ(15, 'Diploid:'), 4, stem=[Q13C], decision='The scheme prices (i) on its own: "4".'),
    T('13cii', 'Q13(c)(ii)', 'C', Q(13, 'Draw a labelled diagram to show the position of the chromosomes during anaphase',
                                    'of mitosis in a diploid nucleus in which 2n = 4.'),
      [pt(S('Showing eight chromosomes, correctly positioned, chromosome label'), 4, kind='criterion',
          note_sel=S('4, 2, 0'), note_lead='The scheme marks the diagram'),
       anyn(S('Chromosome, spindle, centromere'), 2, 2, sep=',')], 'bio-2-3', 'drawing-anaphase',
      SQ(15, 'Anaphase diagram:'), 8, stem=[Q13C],
      decision='The diagram ("4, 2, 0") and its labels ("Any two 2(2)") are priced on their own.'),
    T('13ciii', 'Q13(c)(iii)', 'C', Q(13, 'After telophase of mitosis, how do 1. animal cells; 2. plant cells, split in two?'),
      [pt(S('Cleavage (or furrow) formation or described'), 4, label=S('Animal cells:')),
       pt(S('Cell plate formation or described'), 4, label=S('Plant cells:'))], 'bio-2-3', 'cytokinesis',
      SQ(15, 'Splitting in two after telophase:'), 8, stem=[Q13C],
      decision='"4 + 2" over the two answers, carded at its first rate.'),
    T('13civ', 'Q13(c)(iv)', 'C', Q(13, 'What is the function of mitosis in 1. single‐celled organisms; 2. multi‐celled',
                                    'organisms?'),
      [pt(S('(Asexual) reproduction'), 4, label=S('Single-celled organisms:')),
       pt(S('Repair (or renewal) of tissue or growth'), 4, label=S('Multi-celled organisms:'))], 'bio-2-3',
      'functions-of-mitosis', SQ(15, 'Function of mitosis in:'), 8, stem=[Q13C],
      decision='"4 + 2" over the two answers, carded at its first rate.'),
    T('14ai', 'Q14(a)(i)', 'C', Q(14, 'Suggest a reason why the World Health Organisation (WHO) advised women of',
                                  'outbreak was occurring.'),
      [pt(S('To prevent microcephaly or described or from passage'), 4,
          note_sel=S('[allow to minimise Zika transmission]'))], 'bio-1-1', 'zika-and-pregnancy',
      SQ(16, 'Why childbearing age women advised not to go:'), 4, stem=Q14A),
    T('14aii', 'Q14(a)(ii)', 'C', Q(14, 'Give two precautions people could take to prevent Zika virus transmission if they did',
                                    'travel to affected areas.'),
      [anyn(S('Protect against mosquito bites (nets or repellents or clothing) /',
              'months or use condoms for sex (or don’t have sex)'), 2, 4)], 'bio-1-1', 'preventing-zika',
      SQ(16, 'Precautions against transmission if people went anyway:', paired=COMPRESSED), 8, stem=Q14A),
    T('14aiii', 'Q14(a)(iii)', 'C', Q(14, 'Although the Zika virus can cause harm, other viruses can be beneficial.',
                                      'Give one example of a beneficial virus.'),
      [pt(S('e.g. Bacteriophages (which kill bacteria) or used to treat certain', 'described)'), 4)], 'bio-1-1',
      'beneficial-viruses', SQ(16, 'A beneficial virus:'), 4, stem=Q14A),
    T('14aiv', 'Q14(a)(iv)', 'C', Q(14, 'Describe how a virus replicates.'),
      [anyn(S('Virus attaches to cell (or to host)/ (viral) nucleic acid into cell (or into',
              'virus assembly/ release (or lysis or cell bursts)'), 4, 4,
            note_sel=S('If ‘cell’ not mentioned at least once award a maximum of three unit marks'))], 'bio-1-1',
      'viral-replication', SQ(16, 'Virus replication:', paired=COMPRESSED), 16, stem=Q14A),
    T('14av', 'Q14(a)(v)', 'C', Q(14, 'Discuss the statement “Viruses are not considered to be living organisms”.'),
      [pt(S('Cannot reproduce independently (or explained) or obligate parasites'), 4),
       pt(S('Non-cellular or no organelles or no metabolism (or no metabolism', 'described) or only one type of nucleic acid'), 4)],
      'bio-1-1', 'viruses-not-living', SQ(16, 'Why viruses considered not to be alive:'), 8, stem=Q14A),
    T('14bi', 'Q14(b)(i)', 'C', Q(14, 'An outbreak of measles occurred in Ireland during the summer of 2016.',
                                  'Name a group of people who would be most at risk if exposed to such an outbreak.'),
      [pt(S('Non-vaccinated (or example) or those with weakened immune', 'systems (or example) or babies'), 4)],
      'bio-2-4', 'at-risk-from-measles', SQ(17, 'Most at-risk group:'), 4),
    T('14bii', 'Q14(b)(ii)', 'C', Q(14, 'What is a vaccine and how does it result in immunity?'),
      [pt(S('Non-disease-causing dose of pathogen (or antigen)'), 4, label=S('Vaccine:', after='14.')),
       pt(S('(Introduces) antigen'), 4, label=S('How vaccine gives immunity:')),
       pt(S('Stimulates antibody production'), 4, label=S('How vaccine gives immunity:'))], 'bio-2-4', 'vaccination',
      SQ(17, 'Vaccine:'), 12),
    T('14biii', 'Q14(b)(iii)', 'C', Q(14, 'List any three types of T lymphocyte active in the human immune response.'),
      [anyn(S('Helper/ killer/ suppressor/ memory'), 3, 4)], 'bio-2-4', 't-lymphocyte-types',
      SQ(17, 'T lymphocyte types:'), 12),
    T('14biv', 'Q14(b)(iv)', 'C', Q(14, 'Describe the role of each of the T cells referred to in part (iii) above.'),
      [anyn(S('Helper T cells:', 'Remember antigens or long-term protection'), 3, 4,
            note_sel=S('Any one role from each of three types'))], 'bio-2-4', 't-lymphocyte-roles',
      SQ(17, 'T lymphocyte roles:'), 12,
      stem=[M('(iii)', 14), Q(14, 'List any three types of T lymphocyte active in the human immune response.')],
      decision='Any one role from each of three types: one menu of the four printed types, each with its roles, '
               'cut at the scheme\'s own solidus.'),
] + [
    T(f'14c{r}', f'Q14(c)({r})', 'C', Q(14, ask), [anyn(S(*menu), 2, 4)], topic, concept, SQ(18, sq), 8, stem=[Q14C])
    for r, ask, menu, topic, concept, sq in [
        ('i', 'The lens of the eye for focusing light.', ('Transparent/ curved/ can change curvature (or shape)',),
         'bio-2-4', 'lens-adaptations', 'Lens:'),
        ('ii', 'A neuron for transmitting impulses.', ('Receptors / insulated (or myelin)/ axon/ dendrites /',
                                                        'neurotransmitters (or named neurotransmitter)'),
         'bio-2-4', 'neuron-adaptations', 'Neuron:'),
        ('iii', 'An intestinal villus for absorbing soluble food.',
         ('Wall one cell thick/ large surface area (or microvilli)/ lacteal/ rich', 'blood supply'), 'bio-2-6',
         'villus-adaptations', 'Villus:'),
        ('iv', 'A glomerulus for filtering blood.',
         ('Consists of capillaries/ high (blood) pressure/ wall one cell thick/ large', 'surface area'), 'bio-2-6',
         'glomerulus-adaptations', 'Glomerulus:'),
        ('v', 'A wind‐pollinated flower for pollination.',
         ('Small (or absent) petals or not colourful (or no colour)/ exposed', 'vast amount of pollen/ no nectar'),
         'bio-2-5', 'wind-pollinated-flowers', 'Wind-pollinated flower:')]
] + [
    T('15ai', 'Q15(a)(i)', 'C', Q(15, 'Explain the term homeostasis.'),
      [pt(S('Maintenance of constant internal environment'), 4)], 'bio-2-4', 'homeostasis', SQ(19, 'Homeostasis:'), 4),
    T('15aii', 'Q15(a)(ii)', 'C', Q(15, 'Why is homeostasis important in the human body?'),
      [pt(S('Allows normal (efficient) metabolic activity or keeps temperature (or', 'pH) suitable for enzyme reactions'), 4)],
      'bio-2-4', 'why-homeostasis', SQ(19, 'Why homeostasis important:'), 4),
    T('15aiii', 'Q15(a)(iii)', 'C', Q(15, 'Describe in detail the process of inhalation.'),
      [anyn(S('Increased CO2/ message from brain/ diaphragm contracts and', 'lungs) decreases/ air in'), 5, 4)],
      'bio-2-6', 'inhalation', SQ(19, 'Inhalation:'), 20),
    T('15aiv', 'Q15(a)(iv)', 'C', Q(15, 'Name a human breathing disorder.'),
      [pt(S('Asthma or bronchitis or any valid disorder'), 4)], 'bio-2-6', 'breathing-disorder',
      SQ(19, 'Breathing disorder:'), 4),
] + [
    T('15av', 'Q15(a)(v)', 'C', Q(15, 'State a cause and a treatment for the breathing disorder referred to in part (iv).'),
      [pt(S(*cause), 4, label=S(clab)), pt(S(*treat), 4, label=S(tlab))], 'bio-2-6', f'{route}-cause-and-treatment',
      SQ(19, '(v)', path=['15.'], bare=True, paired=NO_REPRINT), 8, route=route,
      stem=[M('(iv)', 15), Q(15, 'Name a human breathing disorder.')],
      decision='Asthma or bronchitis: the scheme prints a cause and a treatment for each, joined by "OR", so each is '
               'a route card.')
    for route, clab, cause, tlab, treat in [
        ('asthma', 'Cause of asthma', ('Constriction of (lower) bronchioles or by allergens e.g. dust',),
         'Treatment for asthma:', ('Avoid (or minimise exposure) to allergens or use an inhaler or other', 'valid')),
        ('bronchitis', 'Cause of bronchitis:', ('Infection or caused by irritants e.g. smoke',),
         'Treatment for bronchitis:', ('Antibiotics or other valid',))]
] + [
    T('15bi', 'Q15(b)(i)', 'C', Q(15, 'There are five regions in the vertebral column. Name any two of these regions and',
                                  'state how many bones are found in each named region.'),
      [anyn(None, 2, 4, options=[S('cervical'), S('thoracic'), S('lumbar'), S('sacral'), S('coccygeal')]),
       anyn(None, 2, 4, options=[G('lines', page=20, clip=clip, expect=want) for clip, want in REGIONS],
            note_sel=S('Any two', 'i.e. 4 points'))],
      'bio-2-4', 'regions-of-the-vertebral-column', SQ(20, 'Vertebral column regions:'), 16, stem=[Q15B],
      decision='"Any two names, with their numbers i.e. 4 points": two names and their two numbers are four '
               'responses on the ladder. The names are one menu; each region\'s number is read with its name from '
               'its own column of the scheme\'s table.'),
    T('15bii', 'Q15(b)(ii)', 'C', Q(15, 'What are the intervertebral discs made of and what is their function?'),
      [pt(S('*Cartilage'), 4, label=S('What discs made of:', after='15.')),
       pt(S('Shock absorber or to reduce friction (or described)'), 4, label=S('Function of cartilage:'))],
      'bio-2-4', 'intervertebral-discs', SQ(20, 'What discs made of:'), 8, stem=[Q15B]),
] + [
    T(f'15biii{n}', f'Q15(b)(iii){n}', 'C', item(15, n, end, 'Bone tissue is continually'), [pt(S(ans), 4)], 'bio-2-4',
      concept, SQ(20, sq, paired=COMPRESSED), 4, stem=[Q15B, Q15BIII], decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'Name the cells that break down bone.', '*Osteoclasts', 'osteoclasts', 'Bone destroyers:'),
        (2, 'Name the cells that build bone.', '*Osteoblasts', 'osteoblasts', 'Bone builders:')]
] + [
    T('15biv', 'Q15(b)(iv)', 'C', Q(15, 'Give two factors on which the continued renewal of bone depends.'),
      [anyn(S('Diet (or specific reference to supply of calcium (or phosphate) or supply',
              'of vitamin D)/ exercise/ age/ reference to hormones or gender'), 2, 4)], 'bio-2-4', 'bone-renewal',
      SQ(20, 'Factors on which continued renewal of bone depends:'), 8, stem=[Q15B]),
    T('15ci1', 'Q15(c)(i)1', 'C', item(15, 1, 'Explain the term in vitro fertilisation.', 'During in vitro fertilisation'),
      [pt(S('Gametes (sperm and egg) fuse'), 4), pt(S('Outside the body'), 4)], 'bio-2-5', 'ivf',
      SQ(21, 'In vitro fertilisation:'), 8, stem=[Q15C, Q15CI], decision=EACH_ITEM),
    T('15ci2', 'Q15(c)(i)2', 'C', item(15, 2, 'Suggest a reason for the removal of several eggs.', 'During in vitro fertilisation'),
      [pt(S('To increase chance of successful implantation (or pregnancy) or',
            'fertilised or can be stored (for future use)'), 4)], 'bio-2-5', 'why-several-eggs',
      SQ(21, 'Why several eggs:'), 4, stem=[Q15C, Q15CI], decision=EACH_ITEM),
    T('15cii', 'Q15(c)(ii)', 'C', Q(15, 'Identify the germ layer from which the skin of the developing embryo arises.'),
      [pt(S('*Ectoderm'), 4)], 'bio-2-5', 'ectoderm', SQ(21, 'Germ layer from which skin develops:'), 4, stem=[Q15C]),
    T('15ciii', 'Q15(c)(iii)', 'C', Q(15, 'From which tissues does the placenta form?'),
      [pt(S('Endometrium or uterine lining'), 4), pt(S('Chorionic (tissue) [allow trophoblastic (or embryonic) tissue]'), 4)],
      'bio-2-5', 'placenta', SQ(21, 'Tissues from which placenta forms:'), 8, stem=[Q15C]),
    T('15civ', 'Q15(c)(iv)', 'C', Q(15, 'One function of the placenta is to stop the blood of the mother and foetus mixing.',
                                    'Give two reasons why such mixing must not occur.'),
      [anyn(S('Blood pressure difference/ blood group difference/ to prevent', 'transfer of certain infections'), 2, 4)],
      'bio-2-5', 'separate-blood-supplies', SQ(21, 'Why mother’s and foetus’s blood must not mix:'), 8, stem=[Q15C]),
    T('15cv', 'Q15(c)(v)', 'C', Q(15, 'State two other functions of the placenta.'),
      [pt(S('Produces hormones'), 4),
       pt(S('Food (or oxygen or antibodies) to baby (or from mother) or waste to', 'mother (or from baby)'), 4)],
      'bio-2-5', 'placenta-function', SQ(21, 'Other placenta functions:'), 8, stem=[Q15C]),
]

FIGURES = {
    'q3-membrane': ('paper', 4, (80, 64, 515, 274), SEC, ['A', 'B'],
                    'Drawing of part of a cell membrane: an upper and a lower row of black dots, each dot on an open '
                    'rectangular shape pointing in towards the middle, with large stippled oval shapes set among them, '
                    'some spanning both rows. Label line A points into the first stippled shape; label line B points '
                    'to one of the rectangular shapes in the lower row.', False),
    'q8b-v-axes': ('paper', 8, (100, 562, 545, 770), SEC, [],
                   'Part (v) as printed: "Label the axes and sketch a graph to show the effect of pH on enzyme '
                   'activity." Below it a pair of empty axes.', False),
    'q11b-graph': ('paper', 11, (148, 156, 522, 373), SEC, [],
                   'Graph of rate against time of day, from midnight through 6am, midday and 6pm to midnight, with two '
                   'curves: a solid line labelled water uptake and a dashed line labelled transpiration. Overnight the '
                   'solid line sits a little above the dashed one; they cross in the early morning, both rise to peak '
                   'just after midday, the dashed transpiration curve peaking higher and slightly earlier, then both '
                   'fall through the afternoon and evening, the dashed one falling lower. Faint print from the other '
                   'side of the source page shows through behind the graph.', False),
    'q13a-photo': ('paper', 13, (115, 205, 478, 443), SEC, [],
                   'Black and white photograph of an empty football stadium: a large frame of very bright lamps on '
                   'wheeled stands sits on part of the pitch, cables trailing from it, lighting the grass beneath it '
                   'while the empty stands around it are in shadow.',
                   False),
}
