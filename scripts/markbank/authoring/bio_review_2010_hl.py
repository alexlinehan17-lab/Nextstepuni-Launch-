"""Biology 2010 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2010 paper is one booklet (M44), 12 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p11
    Section C Questions 10-15, p12 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: Q12(b) prints its own source line under Graph A and Graph B
    ("[Adapted from Biology for You by Gareth Williams; Stanley Thomas
    (Publishers) Ltd, 2nd edition 2002.]"), and the Q3 and Q6 drawings carry
    no credit. Questions 10-13 print their part totals "(9)", "(27)", "(24)";
    Q14 and Q15 print "(30, 30)".
  * The marking scheme, 15 pages: p1 cover, p2 blank (no text layer), p3
    introduction, cancelled answers and surplus answers (printed page 4), p4
    surplus answers (continued) and conventions, p5-p13 Questions 1-15, set as
    ruled tables with the marks in a right-hand column, p14 blank (printed
    page 15 only), p15 back cover (no text layer).

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c).

This scheme prints no reprint of any question, only a few label words
("Transcription:", "Haploid:", "Sepals:", "Water:", "Labels:"): each answer
stands in its table row under its own question number, letter and roman. A
task is anchored on its own part marker, found by walking the scheme's
numbering down to it (SQ path). A numbered item ("1.", "2.") is anchored on
the roman (or, in Q3(f), the letter) it is printed under. Q6(a) prints no
romans: (i) and (ii) are both anchored on "(a)", each answer on its own line
("A = protein;", "B = Nucleic acid or DNA or RNA").

Tariffs. Section A: Q1 "5(4) any FIVE points out of SIX" (six parts, the best
five at 4; (d)'s two vitamin groups "(4, 2, 0)", 2 each, as 2018 Higher
prices "4, 2, 0" over two reasons), Q2 "4(5)" (four parts at 5), Q4 and Q5
"6 (3) + 2" (seven responses each, an ordered split carded at its first
rate); Q3 and Q6 print a mark against every row ("3", "2", "3(3)", Q3(a)'s
three labels "3, 2, 1, 0", 1 each, and Q6(c)'s "3 + 2" over its two points, a
menu with its steps as 2015 Higher Q14(c)(i)). Sections B and C print a mark
against every row ("3", "2(3)", "4(3)", "3(2)", a drawing's "6, 3, 0" or "3,
0"), so every Section B and C task is priced row by row against the paper's
Section B rubric "Part (a) carries 6 marks and part (b) carries 24 marks",
Section C's (9), (27), (24) and Q14/Q15's (30, 30).

Every printed answer fits a per-response tariff, so no part is carded whole.

Alternatives the scheme prints joined by "or" on their own line are answer
variants of one task: Q12(c)(iii) "True" with its reason, or "False" with a
valid reason.

Q14(a)(iii)1 ("Where do the energised electrons come from?", priced "3"): the
scheme (p12) prints its one answer in a narrow table cell broken mid-word with
no hyphen, "1. Chlorophy" over "ll". The author held it, since the lifter joins
two printed lines with a space unless the first ends in a hyphen; the
coordinator added S(..., wordbreak=True), which joins exactly two printed
lines broken between letters, and the task is carded as "Chlorophyll".

Three scheme lines are lifted as printed although they read oddly: Q13(b)(i)
"micospores" (for microspores); Q15(a)(iii)'s menu, whose first printed line
ends "more bone" and second opens "enlargement of testes" with no solidus
between (each line is cut at its own solidi, one option per piece); Q8(b)(ii)
"To see (or measure ) gas". Q14(b)(iv)'s labels are broken mid-word in the
same narrow cell ("Immobili" / "sation:", "Bioreact" / "or:") and are not
used: each item is its own card.

Q13(c)(iv)'s temperature row is printed against "Suitable temperature:"; a row
opening with those words is refused by the deck build's content-free gate, so
that row carries the factor's printed name in its note, not as its label.

The census reader finds all 126 printed asks, keyed as the paper prints them;
no paper.py entry was needed for this sitting. Its leaves Q1(d)(i) and (ii)
are the paper's two answer lines under (d)'s one ask ("Name these two groups.
(i) ____ (ii) ____"), so their extracted text is only the dotted line; the one
Q1(d) task claims both.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, allof, T, L, G  # noqa: F401

YEAR, LEVEL = 2010, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2010-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': '079cba0377f9159d029a0686cf16ab6216282eb4bf9e4eb84346cb355dac9ae3',
              'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2010-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'ce3e3ee8f4fd26dff26b02f9d69605eb255b2181c9cfaf7560a357fc855d24a1',
               'pages': 15},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 12)}, 12: 'blank'},
    'scheme': {1: 'cover', 2: 'blank', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 14)}, 14: 'blank', 15: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it: "6 (3) + 2"."""
    steps = []
    for term_ in notation.split('+'):
        n, _, m = term_.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p5: "Part (a) carries 6 marks
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # and part (b) carries 24 marks"
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
    **{(n, 'b'): 27 for n in (10, 11, 12, 13)},   # "(27)"
    **{(n, 'c'): 24 for n in (10, 11, 12, 13)},   # "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
# Q1: six parts, the best five priced at 4 ("5(4) any FIVE points out of SIX").
BEST_OF = {1: (5, 4)}
LADDERS = {4: _ladder('6 (3) + 2'), 5: _ladder('6 (3) + 2')}

CHECKSUMS = {
    1: {4: 5, 2: 2},   # five parts at 4; (d)'s two groups "(4, 2, 0)", 2 each
    2: {5: 4},   # "4(5)"
    3: {1: 3, 3: 5, 2: 1},   # (a) "3, 2, 1, 0" over three labels; (b)-(f)1 "3"; (f)2 "2"
    4: {3: 7}, 5: {3: 7},
    6: {3: 6, 2: 1},   # (a) 3, 3; (b) "3(3)"; (c) "3 + 2"
    (7, 'a'): {3: 2}, (7, 'b'): {3: 6, 2: 3},
    (8, 'a'): {3: 2}, (8, 'b'): {3: 8},
    (9, 'a'): {3: 2}, (9, 'b'): {3: 8},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 9}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 5, 6: 1, 2: 3}, (11, 'c'): {3: 8},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 9}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 3}, (13, 'b'): {3: 9}, (13, 'c'): {3: 8},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 8, 6: 1},
    (15, 'a'): {3: 8, 6: 1}, (15, 'b'): {3: 8, 2: 3}, (15, 'c'): {3: 10},
}

SCAN_PAGES = {'paper': range(1, 12)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 "Answer five of the following": best five of (a)-(f); each part is its own card '
                                  'at 4.'),
    ('paper', 2, 'the following', 'Q2 "In each of the following cases": every case asked, one card each.'),
    ('paper', 2, 'choose', 'Q2 "from the list below, choose the correct percentage chance": the answer options (six '
                           'percentages); every case is carded.'),
    ('paper', 3, 'or', 'Q3(c) "prokaryotic or eukaryotic": the answer options.'),
    ('paper', 4, 'the following', 'Q5 "Explain each of the following terms": every term asked, one card each.'),
    ('paper', 5, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 5, 'or', 'Q7(b) "an ox\'s or a sheep\'s heart": description; the scheme marks either on the same rows.'),
    ('paper', 6, 'the following', 'Q8(b) "each of the following": every item asked, one card each.'),
    ('paper', 6, 'or', 'Q8(b)(i) "Methylene blue or iodine solution": description; one purpose asked.'),
    ('paper', 6, 'or', 'Q8(b)(iii)1 "Washing-up liquid or other detergent": description.'),
    ('paper', 6, 'or', 'Q8(b)(v)1 "Biuret solution or alkaline copper sulphate": description.'),
    ('paper', 6, 'or', 'Q8(b)(v)2 "Brown paper or Sudan III": description.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 8, 'the following', 'Q10(c) "the terms in the following pairs": every pair asked, one card each.'),
    ('paper', 8, 'or', 'Q11(a)(ii)2 "A means of prevention or a treatment": the candidate gives either; the scheme '
                       'marks either on the same row.'),
    ('paper', 9, 'the following', 'Q12(c) "each of the following statements": every statement asked, one card each.'),
    ('paper', 9, 'or', 'Q12(c) "true or false": the answer options; Q12(c)(iii)\'s scheme prices both, answer '
                       'variants of one task.'),
    ('paper', 10, 'the following', 'Q13(a) "each of the following parts of a flower": all three asked, one row each.'),
    ('paper', 10, 'the following', 'Q13(c)(v) "each of the following parts of the seedling": one card per numbered '
                                   'item.'),
    ('paper', 10, 'any two', 'Q14 "Answer any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 10, 'or', 'Q14(c)(iv) "high sugar or high salt concentrations": description; the scheme marks both on '
                        'the same rows.'),
    ('paper', 11, 'any two', 'Q15 "Answer any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 11, 'the following', 'Q15(a)(ii) "each of the following occurs": all four asked, one row each.'),
    ('paper', 11, 'the following', 'Q15(c) "each of the following observations": every observation asked, one card '
                                   'each.'),
    ('paper', 11, 'or', 'Q15(c)(i) "(or if a breast pump is regularly used)": description.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
WILLIAMS = 'Biology for You by Gareth Williams; Stanley Thomas (Publishers) Ltd, 2nd edition 2002 (adapted)'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
ITEM_ROMAN = 'The scheme prints no reprint: a numbered item is anchored on the roman it is printed under.'
ITEM_LETTER = 'The scheme prints no reprint: a numbered item is anchored on the letter it is printed under.'
NO_ROMAN = ('The scheme prints no reprint and no romans under Q6(a): each roman is anchored on "(a)", its answer on '
            'its own line.')
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
ROW_PRICED = 'The scheme prints a mark against every row.'


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def dots(page, sentence, sep='…', **kw):
    """An ask that runs straight into its printed answer dots: the line cut at the dots."""
    return Q(page, sentence, piece=1, psep=sep, **kw)


def term(page, word, br=False):
    """A printed term or pair of terms set on its own line."""
    return Q(page, word, word, br=br)


def at(page, *path_and_marker, nth=1, why=NO_REPRINT):
    """The part's own marker, walked down to through the scheme's numbering."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def ladder(q, notation):
    return f'The scheme prints Q{q} as "{notation}": an ordered split, each response carded at its first rate.'


def crit(sel, marks, **kw):
    """A row the scheme prices without printing an answer."""
    return pt(sel, marks, kind='criterion', note=NO_ANSWER, **kw)


def inline(line, marks, **kw):
    """A scheme line closed by its own square-bracketed direction ("... [allow digestion]"): the answer is the
    line up to the bracket, the direction its note."""
    return pt(S(line, piece=1, psep=' ['), marks, note_sel=S(line, piece=[2, 1], psep=[' [', ']']), **kw)


def pieces(line, n, marks, **kw):
    """Each answer of a printed solidus list priced one by one ("2(3)"): one row per entry."""
    return [pt(S(line, piece=i), marks, **kw) for i in range(1, n + 1)]


# ------------------------------------------------------------ question text --
Q1 = ask(2, 'Answer five of the following by filling in the blank spaces.')
Q2 = [Q(2, 'In each of the following cases read the information provided', 'in each case.'),
      Q(2, '0% 10% 25% 50% 75% 100%')]
Q3 = ask(3, 'The diagram shows the structure of Amoeba.')
Q3C = ask(3, 'Is the cell of Amoeba prokaryotic or eukaryotic?')
Q4B = dots(3, 'Name a tissue found in plants', sep=' .')
Q4D = dots(3, 'Name a tissue found in animals')
Q4F = dots(3, 'Explain what is meant by the term tissue culture')
Q5 = ask(4, 'Explain each of the following terms from your study of ecology.')
Q6 = ask(4, 'The diagram shows a virus attached to a host cell.')
Q7B = Q(5, 'Answer the following questions in relation to a dissection', 'structure of an ox’s or a sheep’s heart.')
Q8A = ask(6, 'Answer parts (i) and (ii) in relation to the scientific method.')
Q8B = ask(6, 'For which purpose did you use each of the following in the course of your practical studies?')
Q9B = Q(7, 'Answer the following in relation to an investigation', 'regulator IAA on plant tissue.')
Q10C = Q(8, 'Distinguish between the terms in the following pairs', 'member of each pair.')
Q11AI = ask(8, 'Name a disorder of the human nervous system.')
Q11AII = ask(8, 'In the case of the disorder referred to in part (i) state:')
Q11BIV = ask(8, 'The parts of the nervous system involved in a reflex action make up a reflex arc.')
Q11CII1 = ask(8, '1. Name a hormone-producing gland in the human body.')
Q11CII3 = [M('3.', 8), ask(8, 'Name a hormone that this gland secretes.')]
Q12B = Q(9, 'A paper factory pumps liquid effluent into a river.', 'dissolved in the river water.')
GRAPH_A = ask(9, 'Graph A shows changes in water conditions for several kilometres downstream from the factory outflow.')
GRAPH_B = ask(9, 'Graph B shows the changes in oxygen concentration and the number of fish in the same river.')
Q12BIV = ask(9, 'Describe how the oxygen demand changes as the number of bacteria in the water changes.')
Q12C = Q(9, 'In your answer book, say whether each of the following statements', 'for your choice in each case:')
Q13CV = Q(10, 'Which part of the embryo in a germinating seed gives rise', 'the seedling?')
Q14AIII = ask(10, 'During the first stage of photosynthesis energised electrons enter two pathways.')
Q14BIV = ask(10, 'Bioprocessing often involves the use of immobilised enzymes in a bioreactor.')
Q15C = ask(11, 'Suggest a biological explanation for each of the following observations:')

# Q3(a)'s three parts, printed on one scheme line (p5), cut at its own
# semicolons; each letter's meaning is what follows its " = ".
AMOEBA = 'A = pseudopods (false feet); B = contractile vacuole; C = food vacuoles'
AMOEBA_KEY = [L(x, S(AMOEBA, page=5, piece=[i, 2], psep=['; ', ' = ']), True) for i, x in enumerate('ABC', 1)]
AMOEBA_A = [L('A', S(AMOEBA, page=5, piece=[1, 2], psep=['; ', ' = ']), False)]
AMOEBA_B = [L('B', S(AMOEBA, page=5, piece=[2, 2], psep=['; ', ' = ']), False)]
VIRUS_A = [L('A', S('A = protein;', page=6, piece=[2, 1], psep=[' = ', ';']), True)]
VIRUS_B = [L('B', S('B = Nucleic acid or DNA or RNA', page=6, piece=2, psep=' = '), True)]
TRACE = 'e.g. Fe, Cu, Zn or other correct'
CATABOLIC = 'Respiration or fermentation or glycolysis [allow digestion]'
REFLEX_EG = 'e.g. coughing, blinking, sneezing etc.'
DISORDER = 'Paralysis or Parkinson'
SUPPLEMENT = 'e.g. 1. Treatment of diabetes 2. Contraception'
STIGMA = 'traps (or catches) pollen [allow where pollen lands if qualified]'
HEART_LABELS = 'Labels: Right atrium, tricuspid valve, right ventricle'
LIVER_LABELS = 'Labels (liver, intestine and portal vein)'
# Its three labels, cut from the bracketed list at its own comma, "and" and
# closing bracket.
LIVER_CUTS = [([2, 1], ['(', ', ']), ([2, 2, 1], ['(', ', ', ' and ']), ([2, 2, 2, 1], ['(', ', ', ' and ', ')'])]
MALE_CHAR = ['Broken voice (or enlarged larynx) / body hair / more muscle / more bone',
             'enlargement of testes / enlargement of penis']

TASKS = [
    # ------------------------------------------------------------ Section A --
    T(f'1{x}', f'Q1({x})', 'A', q, rows, 'bio-1-2', concept, at(5, '1.', f'({x})'), 4, stem=[Q1],
      decision='The scheme prints Q1 as "5(4) any FIVE points out of SIX": six parts, the best five at 4, each part '
               'its own card.' + extra)
    for x, q, rows, concept, extra in [
        ('a', ask(2, 'In relation to the human diet, what is meant by a trace element?'),
         [pt(S('Small amount (needed) or indication of e.g. < 0.01%'), 4)], 'trace-element', ''),
        ('b', dots(2, 'Give an example of a trace element', sep=' .'),
         [anyn(None, 1, 4, open_list=True,
               options=[S(TRACE, piece=[2, 1], psep=['e.g. ', ', ']), S(TRACE, piece=[2, 2], psep=['e.g. ', ', ']),
                        S(TRACE, piece=[2, 3, 1], psep=['e.g. ', ', ', ' or '])])],
         'trace-element-examples',
         ' The scheme prints "e.g. Fe, Cu, Zn or other correct": an open menu of its three examples, claim one.'),
        ('c', dots(2, 'State one way in which an oil differs from a fat'),
         [pt(S('Oil is liquid (at room temperature) or fat is solid or oils are unsaturated or', 'explained'), 4)],
         'oils-and-fats', ''),
        ('d', Q(2, 'Vitamins may be divided into two groups', 'Name these two groups.'),
         [pt(S('Fat-soluble'), 2, note_sel=S('(4, 2, 0)'), note_lead='The scheme marks the two groups'),
          pt(S('Water-soluble'), 2)], 'vitamin-groups',
         ' (d)\'s two groups are priced "(4, 2, 0)": 2 for each, as 2018 Higher prices "4, 2, 0" over two reasons.'),
        ('e', ask(2, 'What is a triglyceride?'),
         [pt(S('Fat (or lipid or oil) unit (or molecule) or glycerol and three fatty acids or ester'), 4)],
         'triglyceride', ''),
        ('f', dots(2, 'Give an example of a catabolic reaction in a cell'), [inline(CATABOLIC, 4)],
         'catabolic-reaction', '')]
] + [
    T(f'2{x}', f'Q2({x})', 'A', Q(2, start, end), [pt(S(ans), 5)], 'bio-1-4', concept, at(5, '2.', f'({x})'), 5,
      stem=Q2, decision='The scheme prints Q2 as "4(5)": four cases at 5, each its own card.')
    for x, start, end, ans, concept in [
        ('a', 'In the fruit fly Drosophila', 'full wing?', '100%', 'dominant-cross-full-wing'),
        ('b', 'In roses there is incomplete dominance', 'white petals?', '50%', 'incomplete-dominance-cross'),
        ('c', 'In Dalmatian dogs', 'black spots?', '75%', 'heterozygous-cross-black-spots'),
        ('d', 'Red hair in humans', 'red hair?', '50%', 'red-hair-cross')]
] + [
    T('3a', 'Q3(a)', 'A', ask(3, 'Name the parts labelled A, B and C.'),
      [pt(S(AMOEBA, piece=[i, 2], psep=['; ', ' = ']), 1, label=S(AMOEBA, piece=[i, 1], psep=['; ', ' = ']),
          **({'note_sel': S('3, 2, 1, 0'), 'note_lead': 'The scheme marks the three labels'} if i == 1 else {}))
       for i in (1, 2, 3)],
      'bio-3-2', 'parts-of-amoeba', at(5, '3.', '(a)'), 3, stem=[Q3], fig='q3-amoeba', labels=AMOEBA_KEY,
      decision='The scheme prints the three parts on one line, cut at its own semicolons, priced "3, 2, 1, 0": 1 for '
               'each label, as 2018 Higher prices "4, 2, 0" over two reasons at 2 each.'),
    T('3b', 'Q3(b)', 'A', ask(3, 'To which kingdom does Amoeba belong?'), [pt(S('Protista or Protoctista'), 3)],
      'bio-3-2', 'kingdom-of-amoeba', at(5, '3.', '(b)'), 3, decision=ROW_PRICED),
    T('3c', 'Q3(c)', 'A', Q3C, [pt(S('Eukaryotic'), 3)], 'bio-1-3', 'amoeba-is-eukaryotic', at(5, '3.', '(c)'), 3),
    T('3d', 'Q3(d)', 'A', dots(3, 'Give a reason for your answer to part (c)'),
      [pt(S('Membrane-bound organelles or named membrane-bound organelle'), 3, note_sel=S('[allow nucleus]'))],
      'bio-1-3', 'why-eukaryotic', at(5, '3.', '(d)'), 3, stem=[M('(c)', 3), Q3C]),
    T('3e', 'Q3(e)', 'A', dots(3, 'Give one function of A in Amoeba'), [pt(S('Feeding (or explained) or movement'), 3)],
      'bio-3-2', 'function-of-pseudopods', at(5, '3.', '(e)'), 3, stem=[Q3], fig='q3-amoeba', labels=AMOEBA_A),
    T('3f1', 'Q3(f)1', 'A', [Q(3, '1.', '1.'), dots(3, 'Give one function of B in Amoeba')],
      [pt(S('Osmoregulation or explained'), 3, note_sel=S('[allow excretion or homeostasis]'))], 'bio-3-2',
      'function-of-contractile-vacuole', at(5, '3.', '(f)', why=ITEM_LETTER), 3, stem=[Q3], fig='q3-amoeba',
      labels=AMOEBA_B, decision=EACH_ITEM + ' Items 1 and 2 are priced "3" and "2".'),
    T('3f2', 'Q3(f)2', 'A', [M('2.', 3), ask(3, 'Suggest one reason why B is more active in freshwater amoebae than in '
                                                 'marine amoebae.')],
      [pt(S('Freshwater more hypotonic or more H2O intake or reference to concentration', 'difference'), 2)],
      'bio-3-2', 'contractile-vacuole-in-fresh-water', at(5, '3.', '(f)', why=ITEM_LETTER), 2, stem=[Q3],
      fig='q3-amoeba', labels=AMOEBA_B, decision=EACH_ITEM + ' The text layer flattens the subscript of H2O.'),
] + [
    T(f'4{x}', f'Q4({x})', 'A', q, [row], 'bio-1-3', concept, at(6, '4.', f'({x})'), 3, stem=stem,
      decision=ladder(4, '6 (3) + 2') + ' Seven responses.')
    for x, q, row, concept, stem in [
        ('a', ask(3, 'What is a tissue?'), pt(S('Cells with common function (or with common structure)'), 3), 'tissue',
         []),
        ('b', Q4B, pt(S('Dermal or ground or vascular (or xylem or phloem) or meristematic'), 3), 'plant-tissues', []),
        ('c', dots(3, 'Give a function of the tissue referred to in part (b)'),
         crit(S('Function relevant to tissue named in (b)'), 3), 'function-of-a-plant-tissue', [M('(b)', 3), Q4B]),
        ('d', Q4D, pt(S('Epithelial or Muscular or Connective or Nervous or named example'), 3), 'animal-tissues', []),
        ('e', dots(3, 'Give a function of the tissue referred to in part (d)'),
         crit(S('Function relevant to tissue named in (d)'), 3), 'function-of-an-animal-tissue', [M('(d)', 3), Q4D]),
        ('f', Q4F, pt(S('Cells grown on (or in) medium or cells grown outside organism'), 3), 'tissue-culture', []),
        ('g', dots(3, 'Give one application of tissue culture'), crit(S('Appropriate application'), 3),
         'applications-of-tissue-culture', [M('(f)', 3), Q4F])]
] + [
    # "Habitat" and "Fauna" are below the build's eight-character floor, so
    # those cards carry Q5's printed lead-in in their question text instead of
    # their stem.
    T(f'5{x}', f'Q5({x})', 'A',
      [Q5, dots(4, word, br=True)] if len(word) < 8 else dots(4, word), [pt(S(ans), 3)], 'bio-3-1', concept,
      at(6, '5.', f'({x})'), 3, stem=[] if len(word) < 8 else [Q5],
      decision=ladder(5, '6 (3) + 2') + ' Seven responses.')
    for x, word, ans, concept in [
        ('a', 'Biosphere', 'Part(s) of earth that supports life', 'biosphere'),
        ('b', 'Ecosystem', 'Organisms and their (interactions with) environment', 'ecosystem'),
        ('c', 'Habitat', '(Place) where a species (or an organism) lives', 'habitat'),
        ('d', 'Symbiosis', 'Relationship between (different) species in which at least one benefits', 'symbiosis'),
        ('e', 'Biotic factor', 'Living (organism’s influence on another organism)', 'biotic-factor'),
        ('f', 'Food Web', 'Interconnected food chains or more than one species at each trophic level', 'food-web'),
        ('g', 'Fauna', 'Animals', 'fauna')]
] + [
    T('6ai', 'Q6(a)(i)', 'A', ask(4, 'What is part A made of ?'),
      [pt(S('A = protein;', piece=[2, 1], psep=[' = ', ';']), 3, label=S('A = protein;', piece=1, psep=' = '))],
      'bio-1-1', 'virus-protein-coat', at(6, '6.', '(a)', why=NO_ROMAN), 3, stem=[Q6], fig='q6-virus',
      labels=VIRUS_A, decision=ROW_PRICED + ' The answer is printed as "A = protein;", cut at its own "=" and '
                                            'semicolon.'),
    T('6aii', 'Q6(a)(ii)', 'A', ask(4, 'What is part B made of ?'),
      [pt(S('B = Nucleic acid or DNA or RNA', piece=2, psep=' = '), 3,
          label=S('B = Nucleic acid or DNA or RNA', piece=1, psep=' = '))],
      'bio-1-1', 'virus-nucleic-acid', at(6, '6.', '(a)', why=NO_ROMAN), 3, stem=[Q6], fig='q6-virus',
      labels=VIRUS_B, decision=ROW_PRICED),
    T('6b', 'Q6(b)', 'A', dots(4, 'Briefly describe how viruses reproduce'),
      [anyn(S('Attachment / (viral) nucleic acid into (host) cell / uses host structures (or', 'release (or lysis)'),
            3, 3)], 'bio-1-1', 'viral-reproduction', at(6, '6.', '(b)'), 9,
      decision='"Any three 3(3)" over six printed points: a menu, claim three.'),
    T('6c', 'Q6(c)', 'A', Q(4, 'During 2009 swine flu spread through the population', 'suggest a reason for this.'),
      [anyn(S('(Older people) previous exposure / antibodies (or active immunity or memory', 'cells)'), 2, 3,
            steps=[3, 2])], 'bio-2-4', 'swine-flu-and-immunity', at(6, '6.', '(c)'), 5,
      decision='"3 + 2" printed over one row of two points: a menu with its steps, the first correct point 3 and '
               'the second 2, as 2015 Higher Q14(c)(i).'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', dots(5, 'Name the cavity of the body in which the heart and lungs are located'),
      [pt(S('Thoracic or chest'), 3)], 'bio-2-6', 'thoracic-cavity', at(7, '7.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('7aii', 'Q7(a)(ii)', 'B', dots(5, 'State one way in which heart muscle differs from other muscles in the body'),
      [pt(S('Doesn’t tire'), 3, note_sel=S('[allow involuntary]'))], 'bio-2-6', 'heart-muscle',
      at(7, '7.', '(a)', '(ii)'), 3),
    T('7bi', 'Q7(b)(i)', 'B', Q(5, 'Describe the steps that you followed', 'heart. Use suitably labelled diagrams if '
                                                                           'necessary.'),
      [anyn(S('Identify front (or back or left or right) / how identified / named cutting',
              'safety precaution described'), 4, 3,
            note_sel=S('(any of the above points can be got from labelled diagrams)'))], 'bio-2-6',
      'heart-dissection-steps', at(7, '7.', '(b)', '(i)'), 12, stem=[Q7B],
      decision='"4(3)" over seven printed steps: a menu, claim four; the scheme\'s bracketed direction is its note.'),
    T('7bii', 'Q7(b)(ii)', 'B', ask(5, 'What did you do in order to expose a semi-lunar valve?'),
      [pt(S('Cut open aorta or cut open pulmonary artery'), 3)], 'bio-2-6', 'exposing-a-semilunar-valve',
      at(7, '7.', '(b)', '(ii)'), 3, stem=[Q7B]),
    T('7biii', 'Q7(b)(iii)', 'B', Q(5, 'In the space below draw and label sufficient of your dissection', 'the right '
                                                                                                         'ventricle.'),
      [crit(S('Diagram of dissection'), 3, note_sel=S('3, 0'), note_lead='The scheme marks this diagram')]
      + [pt(S(HEART_LABELS, piece=[2, i], psep=[': ', ', ']), 2, label=S(HEART_LABELS, piece=1, psep=': '))
         for i in (1, 2, 3)],
      'bio-2-6', 'drawing-the-dissected-heart', at(7, '7.', '(b)', '(iii)'), 9, stem=[Q7B],
      decision='The diagram is one priced item ("3, 0") the scheme does not describe, and its three labels "3(2)", '
               'each cut at the scheme\'s own commas.'),
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'What is a hypothesis?'), [pt(S('Educated guess or (possible) explanation'), 3)],
      'bio-u2', 'hypothesis', at(7, '8.', '(a)', '(i)'), 3, stem=[Q8A], decision=ROW_PRICED),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'Why is a control normally used when carrying out an experiment?'),
      [pt(S('Comparison (with experiment)'), 3)], 'bio-u2', 'why-a-control', at(7, '8.', '(a)', '(ii)'), 3,
      stem=[Q8A]),
    T('8bi', 'Q8(b)(i)', 'B', ask(6, 'Methylene blue or iodine solution when examining cells with the microscope.'),
      [pt(S('As a stain or to see more clearly'), 3)], 'bio-1-3', 'staining-cells', at(7, '8.', '(b)', '(i)'), 3,
      stem=[Q8B]),
    T('8bii', 'Q8(b)(ii)', 'B', Q(6, 'An aquatic plant such as pondweed', 'of photosynthesis.'),
      [pt(S('To see (or measure ) gas (or bubbles)'), 3, note_sel=S('[negative for terrestrial plants]'))],
      'bio-2-2', 'why-an-aquatic-plant', at(7, '8.', '(b)', '(ii)'), 3, stem=[Q8B],
      decision='The scheme\'s bracketed direction is the row\'s note; "measure )" is printed with its space.'),
] + [
    T(f'8b{r}{n}', f'Q8(b)({r}){n}', 'B', ask(6, q), [pt(S(ans), 3)], topic, concept,
      at(7, '8.', '(b)', f'({r})', why=ITEM_ROMAN), 3, stem=[Q8B], decision=EACH_ITEM)
    for r, n, q, ans, topic, concept in [
        ('iii', 1, '1. Washing-up liquid or other detergent while extracting DNA from plant tissue.',
         '(Detergent) breaks down membranes', 'bio-1-2', 'detergent-in-dna-extraction'),
        ('iii', 2, '2. Freezer-cold ethanol while extracting DNA from plant tissue.', 'To separate (or see) the DNA',
         'bio-1-2', 'cold-ethanol-in-dna-extraction'),
        ('iv', 1, '1. Antiseptic wash solution in the investigation of the growth of leaf yeast on agar plates.',
         'To prevent contamination or described', 'bio-3-2', 'antiseptic-in-leaf-yeast-investigation'),
        ('iv', 2, '2. Petroleum jelly in the investigation of the growth of leaf yeast on agar plates.',
         'Attach leaves (or leaf parts)', 'bio-3-2', 'petroleum-jelly-in-leaf-yeast-investigation'),
        ('v', 1, '1. Biuret solution or alkaline copper sulphate in food testing.', 'Test for (soluble) protein',
         'bio-1-2', 'biuret-test'),
        ('v', 2, '2. Brown paper or Sudan III in food testing.', 'Test for fat (or lipid or oil)', 'bio-1-2',
         'test-for-fat')]
] + [
    T('9ai', 'Q9(a)(i)', 'B', ask(7, 'What is a tropism?'), [pt(S('Growth of a plant in response to a stimulus'), 3)],
      'bio-2-4', 'tropism', at(7, '9.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('9aii', 'Q9(a)(ii)', 'B', ask(7, 'What is a plant growth regulator?'), [pt(S('Controls the growth (of a plant)'), 3)],
      'bio-2-4', 'plant-growth-regulator', at(7, '9.', '(a)', '(ii)'), 3),
    T('9bi', 'Q9(b)(i)', 'B', ask(7, 'What plant tissue did you use?'), [crit(S('Named plant tissue (or part)'), 3)],
      'bio-2-4', 'tissue-for-iaa-investigation', at(7, '9.', '(b)', '(i)'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', ask(7, 'Describe how you carried out the investigation.'),
      [anyn(S('Tissue or part(s) placed in apparatus / different concentrations / how IAA', 'part(s) / replicates'),
            4, 3)], 'bio-2-4', 'iaa-investigation-method', at(7, '9.', '(b)', '(ii)'), 12, stem=[Q9B],
      decision='"4(3)" over six printed steps: a menu, claim four.'),
    T('9biii', 'Q9(b)(iii)', 'B', ask(7, 'Describe the control that you used.'), [pt(S('Water or no IAA'), 3)],
      'bio-2-4', 'iaa-investigation-control', at(7, '9.', '(b)', '(iii)'), 3, stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', ask(7, 'Compare the results that you obtained in the experiment and in the control.'),
      pieces('Test results described / control results described', 2, 3, kind='criterion', note=NO_ANSWER),
      'bio-2-4', 'iaa-investigation-results', at(7, '9.', '(b)', '(iv)'), 6, stem=[Q9B],
      decision='"2(3)": the two descriptions, cut at the scheme\'s own solidus; the scheme describes neither result.'),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', ask(8, 'Name the base in DNA that pairs with cytosine.'), [pt(S('*Guanine'), 3)],
      'bio-2-3', 'guanine', at(8, '10.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('10aii', 'Q10(a)(ii)', 'C', ask(8, 'What are the two main events in the replication of DNA?'),
      pieces('(DNA) opens (or unzips) / new strands (made)', 2, 3), 'bio-2-3', 'events-of-dna-replication',
      at(8, '10.', '(a)', '(ii)'), 6, decision='"2(3)": the two events, cut at the scheme\'s own solidus.'),
    T('10bi', 'Q10(b)(i)', 'C', ask(8, 'Explain the terms transcription and translation.'),
      [pt(S('making of (m)RNA using DNA (template)'), 3, label=S('Transcription:')),
       pt(S('making a protein using (m)RNA (code)'), 3, label=S('Translation:'))], 'bio-2-3',
      'transcription-and-translation', at(8, '10.', '(b)', '(i)'), 6,
      decision=ROW_PRICED + ' Each term is priced "3", with the scheme\'s own label.'),
    T('10bii', 'Q10(b)(ii)', 'C', ask(8, 'In which structures in the cell does translation occur?'),
      [pt(S('*Ribosome(s)'), 3)], 'bio-2-3', 'ribosomes', at(8, '10.', '(b)', '(ii)'), 3),
    T('10biii', 'Q10(b)(iii)', 'C', ask(8, 'How many bases in sequence make up a codon in mRNA?'), [pt(S('*Three'), 3)],
      'bio-2-3', 'codon-length', at(8, '10.', '(b)', '(iii)'), 3),
    T('10biv', 'Q10(b)(iv)', 'C', Q(8, 'Each mRNA codon specifies one of three possible outcomes',
                                    'Name these three possible outcomes.'),
      [pt(S('Start;', piece=1, psep=';'), 3), pt(S('Adding an amino acid;', piece=1, psep=';'), 3), pt(S('Stop'), 3)],
      'bio-2-3', 'codon-outcomes', at(8, '10.', '(b)', '(iv)'), 9,
      decision='The three outcomes are priced "3" each, each on its own printed line closed by a semicolon (the last '
               'by none).'),
    T('10bv', 'Q10(b)(v)', 'C', ask(8, 'What does the letter ‘t’ stand for in tRNA?'), [pt(S('*Transfer'), 3)],
      'bio-2-3', 'transfer-rna', at(8, '10.', '(b)', '(v)'), 3),
    T('10bvi', 'Q10(b)(vi)', 'C', Q(8, 'During translation one end of a tRNA molecule',
                                    'What is usually attached to the other end of the tRNA molecule?'),
      [pt(S('*An amino acid'), 3)], 'bio-2-3', 'trna-carries-amino-acid', at(8, '10.', '(b)', '(vi)'), 3),
] + [
    T(f'10c{r}', f'Q10(c)({r})', 'C', term(8, pair),
      [pt(S(*a1), 3, label=S(*l1)), pt(S(*a2), 3, label=S(*l2))], 'bio-1-4', concept, at(8, '10.', '(c)', f'({r})'),
      6, stem=[Q10C], decision='Each term of the pair is priced "3", with the scheme\'s own label.')
    for r, pair, l1, a1, l2, a2, concept in [
        ('i', 'Haploid and diploid', ('Haploid:',),
         ('(A nucleus having) one set of chromosomes', '(or one copy of each chromosome)'), ('Diploid:',),
         ('(A nucleus having) Two sets of chromosomes', '(or two copies of each chromosome)'), 'haploid-and-diploid'),
        ('ii', 'Homozygous and heterozygous', ('Homozygous:',), ('alleles the same',), ('Heterozygous:',),
         ('alleles different',), 'homozygous-and-heterozygous'),
        ('iii', 'Genotype and phenotype', ('Genotype:',), ('genetic make-up or genes (alleles) present',),
         ('Phenotype:',), ('expression of genotype (and environment)', 'or physical make up'),
         'genotype-and-phenotype'),
        ('iv', 'Segregation and independent assortment.', ('Segregation:',),
         ('only one (member) of a pair of alleles (or chromosomes)', 'enters a gamete'), ('Independent', 'assortment:'),
         ('Either member of a pair of alleles (or chromosomes) can', 'pair (in gamete formation)'),
         'segregation-and-independent-assortment')]
] + [
    T('11ai', 'Q11(a)(i)', 'C', Q11AI,
      [anyn(None, 1, 3, open_list=True,
            options=[S(DISORDER, piece=1, psep=' or '), S(DISORDER, piece=[2, 1], psep=[' or ', ' .'])])],
      'bio-2-4', 'nervous-system-disorder', at(9, '11.', '(a)', '(i)'), 3,
      decision=ROW_PRICED + ' The scheme prints "Paralysis or Parkinson’s . . .": an open menu of its two examples '
                            '(the closing dots leave it open), claim one.'),
    T('11aii1', 'Q11(a)(ii)1', 'C', ask(8, '1. A possible cause.'), [crit(S('Relevant cause'), 3)], 'bio-2-4',
      'cause-of-a-nervous-disorder', at(9, '11.', '(a)', '(ii)', why=ITEM_ROMAN), 3,
      stem=[M('(i)', 8), Q11AI, M('(ii)', 8), Q11AII], decision=EACH_ITEM),
    T('11aii2', 'Q11(a)(ii)2', 'C', ask(8, '2. A means of prevention or a treatment.'),
      [crit(S('Relevant means of prevention or treatment'), 3)], 'bio-2-4', 'treating-a-nervous-disorder',
      at(9, '11.', '(a)', '(ii)', why=ITEM_ROMAN), 3, stem=[M('(i)', 8), Q11AI, M('(ii)', 8), Q11AII],
      decision=EACH_ITEM),
    T('11bi', 'Q11(b)(i)', 'C', ask(8, 'What is a reflex action?'),
      [anyn(S('automatic / response to a stimulus / involuntary (or not controlled by brain)'), 2, 3)], 'bio-2-4',
      'reflex-action', at(9, '11.', '(b)', '(i)'), 6, decision='"Any two 2(3)" over three printed points: a menu, '
                                                               'claim two.'),
    T('11bii', 'Q11(b)(ii)', 'C', ask(8, 'Give one example of a reflex action.'),
      [anyn(None, 1, 3, open_list=True,
            options=[S(REFLEX_EG, piece=[2, 1], psep=['e.g. ', ', ']), S(REFLEX_EG, piece=[2, 2], psep=['e.g. ', ', ']),
                     S(REFLEX_EG, piece=[2, 3, 1], psep=['e.g. ', ', ', ' etc'])])],
      'bio-2-4', 'examples-of-reflexes', at(9, '11.', '(b)', '(ii)'), 3,
      decision='The scheme prints "e.g. coughing, blinking, sneezing etc.": an open menu of its three examples, cut '
               'at its commas, claim one.'),
    T('11biii', 'Q11(b)(iii)', 'C', ask(8, 'Suggest an advantage of reflex actions.'),
      [pt(S('Protection or fast (response)'), 3)], 'bio-2-4', 'advantage-of-reflexes', at(9, '11.', '(b)', '(iii)'), 3),
    T('11biv1', 'Q11(b)(iv)1', 'C', ask(8, '1. Draw a large labelled diagram to show the structures involved in a reflex '
                                          'arc.'),
      [pt(S('(sensory neuron, motor neuron, spinal cord and correct position of', 'cell bodies for 6 marks)'), 6,
          kind='criterion', label=S('Diagram'), note_sel=S('6, 3, 0'), note_lead='The scheme marks this diagram'),
       anyn(S('receptor (or named), sensory neuron, inter neuron,', 'motor neuron, cell body, effector (or named)'), 3,
            2, sep=',')],
      'bio-2-4', 'drawing-the-reflex-arc', at(9, '11.', '(b)', '(iv)', why=ITEM_ROMAN), 12, stem=[Q11BIV],
      decision=EACH_ITEM + ' The diagram is one priced item ("6, 3, 0": one criterion row naming what it must show) '
                           'and its labels "Any three 3(2)", a menu of the six printed labels cut at the scheme\'s '
                           'commas.'),
    T('11biv2', 'Q11(b)(iv)2', 'C', Q(8, '2. Place arrows on your diagram', 'arc.'),
      [pt(S('Arrow in (dorsal) + arrow out (ventral)'), 3)], 'bio-2-4', 'direction-of-impulses-in-a-reflex-arc',
      at(9, '11.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q11BIV],
      decision=EACH_ITEM + ' Both arrows make one priced item ("3").'),
    T('11ci', 'Q11(c)(i)', 'C', ask(8, 'What term is used to describe the glands that secrete hormones in the human body?'),
      [pt(S('*Endocrine (or ductless)'), 3)], 'bio-2-4', 'endocrine-glands', at(9, '11.', '(c)', '(i)'), 3),
    T('11cii1', 'Q11(c)(ii)1', 'C', Q11CII1, [crit(S('Name of a hormone-producing gland'), 3)], 'bio-2-4',
      'hormone-producing-gland', at(9, '11.', '(c)', '(ii)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('11cii2', 'Q11(c)(ii)2', 'C', [M('2.', 8), ask(8, 'Where in the body is the gland located?')],
      [crit(S('Location of named gland'), 3)], 'bio-2-4', 'location-of-a-gland',
      at(9, '11.', '(c)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q11CII1], decision=EACH_ITEM),
    T('11cii3', 'Q11(c)(ii)3', 'C', Q11CII3, [crit(S('Hormone secreted by named gland'), 3)], 'bio-2-4',
      'hormone-of-a-gland', at(9, '11.', '(c)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q11CII1], decision=EACH_ITEM),
    T('11cii4', 'Q11(c)(ii)4', 'C', [M('4.', 8), ask(8, 'State a role of this hormone.')],
      [crit(S('Role of hormone'), 3)], 'bio-2-4', 'role-of-a-hormone', at(9, '11.', '(c)', '(ii)', why=ITEM_ROMAN), 3,
      stem=[Q11CII1] + Q11CII3, decision=EACH_ITEM),
    T('11cii5', 'Q11(c)(ii)5', 'C', [M('5.', 8), ask(8, 'Describe what happens if the body experiences a deficiency of '
                                                       'this hormone.')],
      [crit(S('Description of deficiency symptom'), 3, note_sel=S('[Accept named condition]'))], 'bio-2-4',
      'hormone-deficiency', at(9, '11.', '(c)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q11CII1] + Q11CII3,
      decision=EACH_ITEM),
    T('11ciii', 'Q11(c)(iii)', 'C', ask(8, 'Give two examples of the use of hormone supplements.'),
      [anyn(None, 2, 3, open_list=True,
            options=[S(SUPPLEMENT, piece=[2, 1], psep=['e.g. 1. ', ' 2. ']),
                     S(SUPPLEMENT, piece=[2, 2], psep=['e.g. 1. ', ' 2. '])])],
      'bio-2-4', 'hormone-supplements', at(9, '11.', '(c)', '(iii)'), 6,
      decision='"2(3)" over the scheme\'s two numbered examples after "e.g.": an open menu, claim two.'),
    T('12ai', 'Q12(a)(i)', 'C', ask(9, 'Where are primary producers found in a pyramid of numbers?'),
      [pt(S('Base or bottom'), 3)], 'bio-3-1', 'producers-in-a-pyramid', at(10, '12.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('12aii', 'Q12(a)(ii)', 'C', ask(9, 'Using named examples, construct a simple inverted pyramid of numbers.'),
      [crit(S('Pyramid showing any inversion (at least two levels)'), 3),
       crit(S('Any two named organisms in inverted relationship'), 3)], 'bio-3-1', 'inverted-pyramid-of-numbers',
      at(10, '12.', '(a)', '(ii)'), 6, decision='The pyramid and its organisms are priced "3" each; the scheme names '
                                                'no organisms.'),
    T('12bi', 'Q12(b)(i)', 'C', ask(9, 'To which kingdom do bacteria belong?'), [pt(S('Monera or Prokaryotae'), 3)],
      'bio-3-2', 'kingdom-of-bacteria', at(10, '12.', '(b)', '(i)'), 3, stem=[Q12B, GRAPH_A], fig='q12b-graph-a'),
    T('12bii', 'Q12(b)(ii)', 'C', Q(9, 'Give one reason why the number of bacteria increases', 'outflow.'),
      [pt(S('Availability of organic effluent or sugar or more food'), 3)], 'bio-3-1', 'bacteria-increase-downstream',
      at(10, '12.', '(b)', '(ii)'), 3, stem=[Q12B, GRAPH_A], fig='q12b-graph-a',
      decision='The scheme prints "Graph A" in its question column beside (ii) and "Graph B" beside (vi); each task '
               'is still anchored on its own roman.'),
    T('12biii', 'Q12(b)(iii)', 'C', Q(9, 'Give one reason why the number of bacteria then decreases', 'outflow.'),
      [pt(S('Decrease of organic effluent or sugar decreased or less food'), 3)], 'bio-3-1',
      'bacteria-decrease-downstream', at(10, '12.', '(b)', '(iii)'), 3, stem=[Q12B, GRAPH_A], fig='q12b-graph-a'),
    T('12biv', 'Q12(b)(iv)', 'C', Q12BIV,
      [pt(S('(Oxygen demand) increases as bacteria increase'), 3,
          note_sel=S('[allow 6 marks for relationship is directly proportional]')),
       pt(S('(Oxygen demand) decreases as bacteria decrease'), 3)], 'bio-3-1', 'oxygen-demand-and-bacteria',
      at(10, '12.', '(b)', '(iv)'), 6, stem=[Q12B, GRAPH_A], fig='q12b-graph-a',
      decision='The two changes are priced "3" each; the scheme\'s bracketed direction, which prices one answer '
               'for both, is the first row\'s note.'),
    T('12bv', 'Q12(b)(v)', 'C', ask(9, 'Give a reason for your answer to part (iv).'),
      [pt(S('More bacteria need more O2 or fewer bacteria need less O2'), 3)], 'bio-3-1', 'why-oxygen-demand-changes',
      at(10, '12.', '(b)', '(v)'), 3, stem=[Q12B, GRAPH_A, M('(iv)', 9), Q12BIV], fig='q12b-graph-a',
      decision='The text layer flattens the subscript of O2.'),
    T('12bvi', 'Q12(b)(vi)', 'C', ask(9, 'Explain why the curve for fish numbers is the same shape as that for oxygen '
                                        'concentration.'),
      [pt(S('Fish need O2 (for respiration)'), 3)], 'bio-3-1', 'fish-and-oxygen', at(10, '12.', '(b)', '(vi)'), 3,
      stem=[Q12B, GRAPH_B], fig='q12b-graph-b'),
    T('12bvii', 'Q12(b)(vii)', 'C', Q(9, 'The oxygen concentration in the river water eventually increases',
                                      'Suggest two ways by which this oxygen may enter the water.'),
      [anyn(S('Agitation (weirs, waterfalls) / photosynthesis / from atmosphere'), 2, 3)], 'bio-3-1',
      'how-oxygen-enters-water', at(10, '12.', '(b)', '(vii)'), 6, stem=[Q12B, GRAPH_B], fig='q12b-graph-b',
      decision='"2(3)" over three printed ways: a menu, claim two.'),
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', Q(9, *q), [pt(S(tf), 3), row], 'bio-3-1', concept,
      at(10, '12.', '(c)', f'({r})'), 6, stem=[Q12C],
      decision='True or false and the reason are priced "3" each.' + extra)
    for r, q, tf, row, concept, extra in [
        ('i', ('Food chains are usually short.', 'Food chains are usually short.'), 'True',
         pt(S('Energy lost at (or between) levels or described'), 3), 'short-food-chains', ''),
        ('ii', ('The herbivores in an ecosystem normally live long lives.',
                'The herbivores in an ecosystem normally live long lives.'), 'False',
         pt(S('Usually eaten by 2nd level consumers (or carnivores)'), 3), 'herbivore-lifespans', ''),
        ('iii', ('The only remaining natural ecosystems in Ireland,', 'mankind has no use.'), 'True',
         pt(S('Use causes change or no abuse or no economic value'), 3), 'remaining-natural-ecosystems',
         ' The scheme prints "True" with its reason, "or", then "False" with "Valid reason": answer variants of one '
         'task.'),
        ('iv', ('HIV / AIDS has orphaned many children in sub-Saharan Africa.',
                'HIV / AIDS has orphaned many children in sub-Saharan Africa.'), 'True',
         pt(S('Premature death of parents or poor living conditions', 'or an example of a cultural reason'), 3),
         'hiv-aids-orphans', '')]
] + [
    T('13a', 'Q13(a)', 'C', ask(10, 'Give a role for each of the following parts of a flower: sepals, anther, stigma.'),
      [pt(S('protect flower (or bud) or photosynthesis or attract insects'), 3, label=S('Sepals:')),
       pt(S('produce pollen'), 3, label=S('Anthers:')),
       inline(STIGMA, 3, label=S('Stigma:'))], 'bio-2-5', 'roles-of-flower-parts', at(11, '13.', '(a)'), 9,
      decision=ROW_PRICED + ' Each part is priced "3", with the scheme\'s own label; the stigma\'s bracketed '
                            'direction is its note.'),
    T('13bi', 'Q13(b)(i)', 'C', ask(10, 'Describe the development of pollen grains from microspore mother cells.'),
      [anyn(S('Meiosis / 4 (or tetrad ) / haploid / micospores / (divides by) mitosis / tube',
              'and generative nucleus / pollen grain matures (or wall forms)'), 4, 3)], 'bio-2-5',
      'pollen-development', at(11, '13.', '(b)', '(i)'), 12,
      decision='"Any four 4(3)" over seven printed points: a menu, claim four. "micospores" is printed so.'),
    T('13bii', 'Q13(b)(ii)', 'C', ask(10, 'What is meant by the term fertilisation?'),
      [pt(S('Fusion of gametes or formation of zygote'), 3)], 'bio-2-5', 'fertilisation',
      at(11, '13.', '(b)', '(ii)'), 3),
    T('13biii', 'Q13(b)(iii)', 'C', ask(10, 'Give a brief account of the process of fertilisation in flowering plants.'),
      [anyn(S('Generative nucleus / mitosis / two male gametes (or nuclei) / one fuses',
              'polar nuclei / to form endosperm'), 4, 3)], 'bio-2-5', 'double-fertilisation',
      at(11, '13.', '(b)', '(iii)'), 12, decision='"Any four 4(3)" over seven printed points: a menu, claim four.'),
    T('13ci', 'Q13(c)(i)', 'C', ask(10, 'What is meant by the dormancy of seeds?'),
      [pt(S('Period of reduced metabolism (or period of reduced activity) or period of', 'no growth.'), 3)], 'bio-2-5',
      'seed-dormancy', at(11, '13.', '(c)', '(i)'), 3),
    T('13cii', 'Q13(c)(ii)', 'C', ask(10, 'Give one way in which the dormancy of seeds is of benefit to plants.'),
      [pt(S('Survival or germination delayed until conditions suitable for growth or', 'reduced competition'), 3)],
      'bio-2-5', 'benefit-of-dormancy', at(11, '13.', '(c)', '(ii)'), 3),
    T('13ciii', 'Q13(c)(iii)', 'C', ask(10, 'Suggest one way in which a knowledge of dormancy is useful to farmers and '
                                          'gardeners.'),
      [pt(S('(Optimum) storage conditions or (optimum) sowing (or ploughing) time', 'examples)'), 3)], 'bio-2-5',
      'dormancy-and-farming', at(11, '13.', '(c)', '(iii)'), 3),
    T('13civ', 'Q13(c)(iv)', 'C', Q(10, 'Water, oxygen and a suitable temperature are all required',
                                    'describe its effect on the process of germination.'),
      [pt(S('for enzyme action (or example of enzyme action) or as a', 'solvent or transport of materials or bursting '
                                                                        'the testa'), 3,
          label=S('Water:'), note_sel=S('[allow washing away inhibitors]')),
       pt(S('required for (optimum or increased) enzyme activity'), 3,
          note_sel=S('Suitable', 'temperature:', piece=1, psep=':'), note_lead='Factor:'),
       pt(S('needed for (aerobic) respiration'), 3, label=S('Oxygen:'))], 'bio-2-5', 'germination-factors',
      at(11, '13.', '(c)', '(iv)'), 9,
      decision=ROW_PRICED + ' Each factor is priced "3". Water and oxygen carry the scheme\'s own label; the '
                            'temperature row carries its printed factor name in its note, because a row opening with '
                            'it is refused by the deck build\'s content-free gate.'),
    T('13cv1', 'Q13(c)(v)1', 'C', term(10, '1. The root'), [pt(S('*Radicle'), 3)], 'bio-2-5', 'radicle',
      at(11, '13.', '(c)', '(v)', why=ITEM_ROMAN), 3, stem=[Q13CV], decision=EACH_ITEM),
    T('13cv2', 'Q13(c)(v)2', 'C', ask(10, '2. The shoot.'), [pt(S('*Plumule'), 3)], 'bio-2-5', 'plumule',
      at(11, '13.', '(c)', '(v)', why=ITEM_ROMAN), 3, stem=[Q13CV], decision=EACH_ITEM),
    # Q14(a)
    T('14ai', 'Q14(a)(i)', 'C', ask(10, 'Where in a plant cell does photosynthesis take place?'),
      [pt(S('Chloroplast'), 3)], 'bio-2-2', 'chloroplast', at(12, '14.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('14aii', 'Q14(a)(ii)', 'C', ask(10, 'Give the alternative name of the first stage of photosynthesis.'),
      [pt(S('*Light (stage)'), 3)], 'bio-2-2', 'light-stage', at(12, '14.', '(a)', '(ii)'), 3),
    T('14aiii1', 'Q14(a)(iii)1', 'C', ask(10, '1. Where do the energised electrons come from?'),
      [pt(S('Chlorophy', 'll', wordbreak=True), 3)], 'bio-2-2', 'source-of-energised-electrons',
      at(12, '14.', '(a)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q14AIII],
      decision=EACH_ITEM + ' Scheme p12 sets its answer "Chlorophy" over "ll" in a narrow cell with no hyphen; '
               'the two printed lines are joined as one word (S wordbreak), as the page prints the word.'),
    T('14aiii2', 'Q14(a)(iii)2', 'C', ask(10, '2. Briefly describe the main events of each of these pathways.'),
      [anyn(S('(Energised electrons) release energy / ATP formed /', '(electrons) return to chlorophyll'), 2, 3),
       anyn(S('Electrons taken up by NADP / photolysis (or water', 'chlorophyll /ATP formed'), 2, 3)],
      'bio-2-2', 'pathways-of-energised-electrons', at(12, '14.', '(a)', '(iii)', why=ITEM_ROMAN), 12,
      stem=[Q14AIII], decision=EACH_ITEM + ' The scheme prints two pathways, each headed "Pathway :" and each "Any '
                                           'two 2(3)": two menus, claim two from each.'),
    T('14aiv1', 'Q14(a)(iv)1', 'C', Q(10, '1. In the second stage of photosynthesis compounds',
                                      'What name is given to this group of compounds?'),
      [pt(S('*Carbohydrates'), 3)], 'bio-2-2', 'carbohydrates-from-the-dark-stage',
      at(12, '14.', '(a)', '(iv)', why=ITEM_ROMAN), 3,
      decision=EACH_ITEM + ' The text layer flattens the subscripts of Cx(H2O)y.'),
    T('14aiv2', 'Q14(a)(iv)2', 'C', Q(10, '2. From which simple compound does the plant obtain the H',
                                      'general formula Cx(H2O)y?'),
      [pt(S('*Water (or H2O)'), 3)], 'bio-2-2', 'source-of-hydrogen', at(12, '14.', '(a)', '(iv)', why=ITEM_ROMAN), 3,
      decision=EACH_ITEM + ' The text layer flattens the subscripts of Cx(H2O)y and H2O.'),
    T('14av', 'Q14(a)(v)', 'C', Q(10, 'Name the simple compound that supplies the necessary energy', 'reactions.'),
      [pt(S('*Adenosine Triphosphate (or ATP)'), 3)], 'bio-2-2', 'atp-for-the-dark-stage',
      at(12, '14.', '(a)', '(v)'), 3),
    # Q14(b)
    T('14bi', 'Q14(b)(i)', 'C', ask(10, 'What is an enzyme?'),
      [pt(S('Biological (or protein) catalyst (or explained)'), 3)], 'bio-2-1', 'enzyme', at(12, '14.', '(b)', '(i)'),
      3),
    T('14bii', 'Q14(b)(ii)', 'C', ask(10, 'What is meant by the specificity of an enzyme?'),
      [pt(S('(Enzyme) acts on only a particular substrate'), 3)], 'bio-2-1', 'enzyme-specificity',
      at(12, '14.', '(b)', '(ii)'), 3),
    T('14biii', 'Q14(b)(iii)', 'C', ask(10, 'Explain how the Active Site Theory may be used to explain the specificity '
                                          'of enzymes.'),
      [anyn(S('Substrate / matching enzyme’s active site / active site changes shape /',
              '(formation of) enzyme-substrate complex / product(s) formed'), 3, 3)], 'bio-2-1', 'active-site-theory',
      at(12, '14.', '(b)', '(iii)'), 9, decision='"Any three 3(3)" over five printed points: a menu, claim three.'),
    T('14biv1', 'Q14(b)(iv)1', 'C', ask(10, '1. What does the term immobilisation refer to when used about enzymes?'),
      [pt(S('attached to an inert substance (or example of', 'inert substance) or fixed to each other'), 3)],
      'bio-2-1', 'immobilisation', at(12, '14.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q14BIV],
      decision=EACH_ITEM + ' The scheme\'s label is broken mid-word in its narrow cell ("Immobili" / "sation:") and '
                           'is not used.'),
    T('14biv2', 'Q14(b)(iv)2', 'C', ask(10, '2. Explain the term bioreactor.'),
      [pt(S('vessel in which products are made by cells (or', 'organisms)'), 3)], 'bio-2-1', 'bioreactor',
      at(12, '14.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q14BIV],
      decision=EACH_ITEM + ' The scheme\'s label is broken mid-word in its narrow cell ("Bioreact" / "or:") and is '
                           'not used.'),
    T('14bv', 'Q14(b)(v)', 'C', Q(10, 'Give one example of the use of immobilised enzymes in bioreactors.',
                                  'In your answer name the enzyme, the substrate and the product.'),
      [crit(S('Enzyme'), 3), crit(S('Substrate (must match enzyme)'), 3),
       crit(S('Product (must match enzyme or substrate)'), 3)], 'bio-2-1', 'immobilised-enzyme-example',
      at(12, '14.', '(b)', '(v)'), 9, decision='The enzyme, substrate and product are priced "3" each; the scheme '
                                               'names none of them.'),
    # Q14(c)
    T('14ci', 'Q14(c)(i)', 'C', ask(10, 'In relation to membranes in cells, explain what is meant by selective '
                                       'permeability.'),
      [pt(S('Allowing some substances to pass through'), 3)], 'bio-1-3', 'selective-permeability',
      at(12, '14.', '(c)', '(i)'), 3),
    T('14cii', 'Q14(c)(ii)', 'C', ask(10, 'Give two locations in a cell at which there is a selectively permeable '
                                         'membrane.'),
      [anyn(S('Chloroplast / mitochondrion / nucleus / vacuole'), 2, 3, note_sel=S('[allow cell membrane]'))],
      'bio-1-3', 'selectively-permeable-membranes', at(12, '14.', '(c)', '(ii)'), 6,
      decision='"Any two 2(3)" over four printed locations: a menu, claim two; the bracketed direction is its note.'),
    T('14ciii1', 'Q14(c)(iii)1', 'C', ask(10, '1. What is diffusion?'),
      [pt(S('Movement of molecules (or substances)'), 3),
       pt(S('from area of high concentration to area of low concentration', '(or along a concentration gradient)'), 3)],
      'bio-2-6', 'diffusion', at(12, '14.', '(c)', '(iii)', why=ITEM_ROMAN), 6,
      decision=EACH_ITEM + ' The scheme prices its definition "3" and "3", the second mark printed beside the end of '
                           'the second point.'),
    T('14ciii2', 'Q14(c)(iii)2', 'C', Q(10, '2. In the case of a named molecule,', 'body.'),
      [crit(S('Named molecule and location'), 6)], 'bio-2-6', 'diffusion-in-the-body',
      at(12, '14.', '(c)', '(iii)', why=ITEM_ROMAN), 6, decision=EACH_ITEM + ' One priced item, "6".'),
    T('14civ', 'Q14(c)(iv)', 'C', Q(10, 'Explain the biological basis for the use of high sugar', 'preservation of food.'),
      [anyn(S('Bacteria / lose water / by osmosis / inactivity or death'), 3, 3)], 'bio-2-6', 'preserving-with-sugar-or-salt',
      at(12, '14.', '(c)', '(iv)'), 9, decision='"Any three 3(3)" over four printed points: a menu, claim three.'),
    # Q15(a)
    T('15ai', 'Q15(a)(i)', 'C', ask(11, 'What is semen?'), [pt(S('Sperm (cells) and (seminal) fluid'), 3)], 'bio-2-5',
      'semen', at(13, '15.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('15aii', 'Q15(a)(ii)', 'C',
      [ask(11, 'Draw a labelled diagram of the reproductive system of the human male.'),
       ask(11, 'On your diagram, indicate clearly and name the part at which each of the following occurs:', br=True)]
      + [ask(11, s, br=True) for s in ('1. Production of sperm cells.', '2. Maturing of sperm cells.',
                                       '3. Mixing of fluid with sperm cells.', '4. Transport of semen.')],
      [pt(S('Diagram (testis, sperm duct, urethra, penis)'), 6, kind='criterion', note_sel=S('6, 3, 0'),
          note_lead='The scheme marks this diagram'),
       pt(S('1. Testis'), 3, note_sel=S('Four parts located and named:')),
       pt(S('2. Epididymis'), 3),
       pt(S('3. Sperm duct or prostate gland'), 3, note_sel=S('[allow seminal vesicles]')),
       pt(S('4. Urethra or sperm duct'), 3)],
      'bio-2-5', 'drawing-the-male-system', at(13, '15.', '(a)', '(ii)'), 18,
      decision='The diagram is one priced item ("6, 3, 0": one criterion row naming what it must show) and the four '
               'parts "3" each, each row with its printed number matching the paper\'s.'),
    T('15aiii', 'Q15(a)(iii)', 'C', ask(11, 'State two secondary sexual characteristics of the human male.'),
      [anyn(None, 2, 3, options=[S(MALE_CHAR[0], piece=i) for i in (1, 2, 3, 4)]
            + [S(MALE_CHAR[1], piece=i) for i in (1, 2)])], 'bio-2-5', 'male-secondary-sexual-characteristics',
      at(13, '15.', '(a)', '(iii)'), 6,
      decision='"Any two 2(3)" over six printed characteristics: a menu, claim two. The scheme prints no solidus '
               'between its first line\'s last entry ("more bone") and its second line\'s first ("enlargement of '
               'testes"), so each line is cut at its own solidi.'),
    T('15aiv', 'Q15(a)(iv)', 'C', ask(11, 'What maintains the secondary sexual characteristics in the adult human male?'),
      [pt(S('*Testosterone'), 3)], 'bio-2-5', 'testosterone', at(13, '15.', '(a)', '(iv)'), 3),
    # Q15(b)
    T('15bi', 'Q15(b)(i)', 'C', Q(11, 'Draw a labelled diagram to show the relationship between the liver,',
                                  'the hepatic portal vein.'),
      [pt(S('Diagram (liver, connection, gut)'), 3, kind='criterion', note_sel=S('3, 0'),
          note_lead='The scheme marks this diagram')]
      + [pt(S(LIVER_LABELS, piece=p, psep=s), 2, label=S(LIVER_LABELS, piece=1, psep=' ('))
         for p, s in LIVER_CUTS],
      'bio-2-6', 'drawing-the-hepatic-portal-system', at(13, '15.', '(b)', '(i)'), 9,
      decision='The diagram is one priced item ("3, 0": one criterion row naming what it must show) and its three '
               'labels "3(2)", each cut from the scheme\'s bracketed list.'),
    T('15bii', 'Q15(b)(ii)', 'C', ask(11, 'Name a substance transported to the liver by the blood in the hepatic portal '
                                         'vein.'),
      [pt(S('Named food or CO2'), 3, note='The scheme names no food here, only that a named one earns the marks.')],
      'bio-2-6', 'hepatic-portal-vein-contents', at(13, '15.', '(b)', '(ii)'), 3,
      decision='The text layer flattens the subscript of CO2.'),
    T('15biii', 'Q15(b)(iii)', 'C', ask(11, 'Name the blood vessel that brings oxygenated blood to the liver.'),
      [pt(S('*Hepatic artery'), 3)], 'bio-2-6', 'hepatic-artery', at(13, '15.', '(b)', '(iii)'), 3),
    T('15biv', 'Q15(b)(iv)', 'C', ask(11, 'Where in the human body is the liver located in relation to the stomach?'),
      [pt(S('Above or to the right or behind'), 3)], 'bio-2-6', 'position-of-the-liver', at(13, '15.', '(b)', '(iv)'),
      3),
    T('15bv', 'Q15(b)(v)', 'C', ask(11, 'Where is bile stored after it has been made in the liver?'),
      [pt(S('*Gall bladder'), 3)], 'bio-2-6', 'gall-bladder', at(13, '15.', '(b)', '(v)'), 3),
    T('15bvi', 'Q15(b)(vi)', 'C', ask(11, 'Give one role that the bile salts play in the digestive process.'),
      [pt(S('Emulsify fats (or explained) or neutralise (or comment on pH)'), 3)], 'bio-2-6', 'role-of-bile-salts',
      at(13, '15.', '(b)', '(vi)'), 3),
    T('15bvii', 'Q15(b)(vii)', 'C', ask(11, 'Give two further functions of the liver, other than the manufacture of '
                                          'bile.'),
      [anyn(S('Storage of (fat-soluble) vitamins (or glycogen or named mineral) /', 'cholesterol production'), 2, 3)],
      'bio-2-6', 'functions-of-the-liver', at(13, '15.', '(b)', '(vii)'), 6,
      decision='"Any two 2(3)" over six printed functions: a menu, claim two.'),
] + [
    # Q15(c)
    T(f'15c{r}', f'Q15(c)({r})', 'C', Q(11, *q), [anyn(S(*menu), 2, 3)], topic, concept,
      at(13, '15.', '(c)', f'({r})'), 6, stem=[Q15C],
      decision=f'"Any two 2(3)" over {n} printed points: a menu, claim two.')
    for r, q, menu, n, topic, concept in [
        ('i', ('As long as a baby feeds regularly', 'the milk will continue to flow.'),
         ('(Sucking or pumping) stimulates (pituitary) / production of hormone (or', 'promotes milk flow'), 'three',
         'bio-2-5', 'lactation'),
        ('ii', ('Doctors are reluctant to prescribe antibiotics', 'symptoms.'),
         ('Common cold is a viral disease / antibiotics do not affect viruses / (overuse',
          'antibiotic resistance in bacteria (in patients)'), 'three', 'bio-3-2', 'antibiotics-and-colds'),
        ('iii', ('A person who has suffered from constipation', 'in her/his diet.'),
         ('Adds fibre / fibre absorbs water / peristalsis encouraged / faster digestive', 'transit'), 'four', 'bio-2-6',
         'fibre-and-constipation'),
        ('iv', ('After a long session of heavy exercise,', 'low in volume.'),
         ('Water lost by exhaling (or by sweating) / less water in blood / ADH', 'water'), 'five', 'bio-2-6',
         'concentrated-urine-after-exercise'),
        ('v', ('A person’s fingers may turn white when exposed to low temperature for a period of time.',
               'A person’s fingers may turn white when exposed to low temperature for a period of time.'),
         ('Arterioles / constrict / less blood (in fingers) / heat loss minimised',), 'four', 'bio-2-4',
         'white-fingers-in-the-cold')]
]

ANSWER_VARIANTS = {
    '12ciii': [
        ('true', 'True', [pt(S('True'), 3), pt(S('Use causes change or no abuse or no economic value'), 3)]),
        ('false', 'False', [pt(S('False'), 3), crit(S('Valid reason'), 3)]),
    ],
}

# Brought to the coordinator, not in TASKS: the scheme (p12) prints this
# item's one answer broken mid-word over two lines of its narrow cell,
# "1. Chlorophy" over "ll", with no hyphen, so the lifter can only read it as
# "Chlorophy ll". Ready to move into TASKS once the runner can join an
# unhyphenated in-word break (or the split lift is accepted).

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-amoeba': ('paper', 3, (95, 56, 516, 230), SEC, ['A', 'B', 'C'],
        'Line drawing of a single irregular cell with a wavy outline drawn out into several rounded lobes. Printed '
        'labels: Nucleus, pointing to a dark oval near the top right; B, pointing to a small circle near the top '
        'left ringed by short radiating dashes; C, a line ending at a curly bracket around three small oval bodies '
        'on the left; A, a line ending at a curly bracket beside a rounded lobe of the outline at the lower right.',
        False),
    'q6-virus': ('paper', 4, (150, 290, 548, 460), SEC, ['A', 'B'],
        'Line drawing of a large oval labelled Host cell. Attached to its upper right edge is a small six-sided '
        'shape with a coiled line inside it, from which short angled legs reach the cell surface; a curly bracket '
        'over the small shape is labelled Virus. Label A points to the edge of the six-sided shape; label B points '
        'to the coiled line inside it.',
        False),
    'q12b-graph-a': ('paper', 9, (100, 150, 380, 302), WILLIAMS, [],
        'Sketch graph headed Graph A, with no scales. Vertical axis: quantity. Horizontal axis: distance '
        'downstream, with an upward arrow at the origin labelled outflow. Three curves, each named by a label and '
        'arrow. Organic effluent: starts high on the vertical axis, falls steeply, then levels off at a lower '
        'value. Oxygen demand: starts a little above the origin, rises to a peak a short distance downstream, then '
        'falls and levels off below the organic effluent curve. Bacteria: starts at the origin, rises to a peak at '
        'about the same distance, then falls almost to the horizontal axis, staying below the oxygen demand curve.',
        False),
    'q12b-graph-b': ('paper', 9, (100, 428, 380, 574), WILLIAMS, [],
        'Sketch graph headed Graph B, with no scales. Vertical axis: quantity. Horizontal axis: distance '
        'downstream, with an upward arrow at the origin labelled outflow. Two curves of the same U shape, each '
        'named by a label and arrow: oxygen concentration, the upper curve, and fish, the lower. Both start part '
        'way up the vertical axis, fall to a low point a short distance downstream, then rise steadily, ending '
        'higher than they started.',
        False),
}
