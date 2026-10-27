"""Biology 2013 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2013 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p5 Section A Questions 1-6, p6-p8 Section B Questions 7-9, p9-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q3 and Q15(c) graphs and the Q4 and Q13 drawings carry no
    credit; the Q15(a) article prints its own source lines, lifted with it.
    Section C's Questions 10-13 print no part totals; Q14 and Q15 print
    "(30, 30)".
  * The marking scheme, 20 pages: p1 cover, p2 note, p3 introduction and
    cancelled answers, p4 surplus answers and conventions, p5-p17 Questions
    1-15, p18 and p19 "Blank Page", p20 back cover (no text layer).

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c). Every printed ask is carded.

This scheme prints no reprint of any question, only Q1's terms over their
definitions, Q14(b)'s topic words ("Metabolism:", "Krebs Cycle:", "ADP:") and
a few label words ("Diagram:", "Labels:", "Contest:"). A task is anchored on
its own part marker, found by walking the scheme's numbering down to it (SQ
path); where the marker opens its answer's own line ("(b) Endothermic") it is
a welded bare anchor. A numbered item ("1.", "2.") is anchored on the roman
or letter it is printed under. Q14(b)'s notes are anchored on the scheme's
own topic words.

Tariffs. Section A is priced as a whole question: Q1 "5(4, 2, 0) i.e. best
five answers from (a) - (f)" (six parts, the best five at 4, a part's two
terms 2 each, as 2018 Higher prices "4, 2, 0" over two reasons); Q2 "6(3) +
2" and Q3, Q4 "6(3) + (2)" (seven responses each, ordered splits carded at
their first rate); Q5 and Q6 "1 + 1 + 8 + 6 + 4(1)" (eight responses each).
That last notation is printed only here in the 2010-2026 schemes; read as
the conventions page (p4) defines an ordered split, its first rate is 1, and
each Q5 and Q6 response is carded at 1 under the printed notation (brought
to the coordinator for decision). Sections B and C print a mark against every
row ("3", "2(3)", "5(3)", a drawing's "6, 3, 0", "5, 3, 0" or "3, 0", Q14(b)'s
"4 + 2(3)"), so every Section B and C task is priced row by row against the
paper's Section B rubric "Part (a) carries 6 marks and part (b) carries 24
marks", Section C's 60 a question and Q14/Q15's (30, 30).

Every printed answer fits a per-response tariff, so no part is carded whole.

Alternatives the scheme prints as matched sets are answer variants of one
task: Q9(b)(i)1 "CO2 - vary NaHCO3 conc. OR Light - vary lamp ...", and
Q11(a)(ii)'s points under each source of evidence ("e.g. Fossils:", "e.g.
Embryology:", "e.g. Anatomy:"). Q11(b)(ii)'s answer is a drawing the scheme
prints ("Female XX", "Male XY" over drawn chromosome pairs), read from its own
columns by glyph position, and Q11(b)(iii)'s is a Punnett square; each is
shown after reveal as a crop of the scheme.

The census reader finds all 132 printed asks; no paper.py entry was needed
for this sitting. Its text for Q10(b)(ii) and (iii) is mis-keyed by the
in-sentence cross-reference "part (b) (ii):" (the leaves themselves are
right), and Section C's numbered items are dropped from its leaf text; the
cards lift the paper's own lines.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, G

YEAR, LEVEL = 2013, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2013-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': '60c49460a985dfdb536b251d0e3fd810cf555eff2e8fab413c39551490049951',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2013-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'd2088df58f0b45ef5804810142e9521b53d0256c4a3b6f01f6845af0c92e4120',
               'pages': 20},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 18)}, 18: 'blank', 19: 'blank', 20: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it: "6(3) + 2", "6(3) + (2)"."""
    steps = []
    for term_ in notation.split('+'):
        n, _, m = term_.strip().partition('(')
        if n and m:
            steps += [int(m.rstrip(')'))] * int(n)
        else:
            steps += [int((m or n).rstrip(')'))]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only parts the paper prints a total for: Section B's rubric (p6) and
# Q14/Q15's "(30, 30)". Questions 10-13 print none; their 60 is checked whole.
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p6: "Part (a) carries 6 marks
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # and part (b) carries 24 marks"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
# Q1: six parts, the best five priced at 4 ("5(4, 2, 0)").
BEST_OF = {1: (5, 4)}
LADDERS = {
    2: _ladder('6(3) + 2'), 3: _ladder('6(3) + (2)'), 4: _ladder('6(3) + (2)'),
}

CHECKSUMS = {
    1: {2: 12},   # six parts, each pair of terms "4, 2, 0": 2 for each term
    2: {3: 7}, 3: {3: 7}, 4: {3: 7},
    **{(n, 'a'): {3: 2} for n in (7, 8, 9)}, **{(n, 'b'): {3: 8} for n in (7, 8, 9)},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 3, 2: 9}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 9}, (11, 'c'): {3: 5, 6: 1, 1: 3},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 6, 5: 1, 1: 4}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 3}, (13, 'b'): {1: 6, 3: 7}, (13, 'c'): {3: 8},
    (14, 'a'): {3: 10}, (14, 'b'): {4: 3, 3: 6}, (14, 'c'): {3: 10},
    (15, 'a'): {3: 10}, (15, 'b'): {2: 15}, (15, 'c'): {3: 10},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'any five', 'Q1 "In the case of any five of the following pairs of terms": best five of (a)-(f); '
                             'each part is its own card at 4.'),
    ('paper', 2, 'the following', 'Q1, same lead-in.'),
    ('paper', 2, 'the following', 'Q2 lead-in: every part asked.'),
    ('paper', 3, 'or', 'Q3(a) "Which of the plots, X or Y": the answer options.'),
    ('paper', 4, 'or', 'Q4(c) "haploid or diploid": the answer options.'),
    ('paper', 6, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 6, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 6, 'or', 'Q7(b)(i) "other than temperature or pH": description.'),
    ('paper', 7, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 8, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'either', 'Q9(b)(i) "either carbon dioxide concentration or light intensity": either investigation; '
                           'item 1 is carded with the scheme\'s answer for each as answer variants, item 2 on one row.'),
    ('paper', 8, 'or', 'Q9(b)(i), same choice.'),
    ('paper', 8, 'or', 'Q9(b)(ii)1 "Visking tubing, potato tissue or some similar material": description.'),
    ('paper', 9, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 9, 'the following', 'Q10(b) lead-in: every part asked.'),
    ('paper', 9, 'either', 'Q10(b)(iii)3 "for either its deficiency or its excess": either; one criterion row.'),
    ('paper', 9, 'or', 'Q10(b)(iii)3, same choice.'),
    ('paper', 10, 'or', 'Q11(b)(iii) "using a Punnett square or otherwise": description.'),
    ('paper', 10, 'or', 'Q11(b)(iii) "male or female": description.'),
    ('paper', 10, 'the following', 'Q11(c) lead-in: every part asked.'),
    ('paper', 12, 'the following', 'Q13(b)(ii) "identify the following locations": one card per numbered item.'),
    ('paper', 12, 'the following', 'Q13(c) lead-in: every part asked.'),
    ('paper', 13, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q14(b) "Write notes on each of the following topics": every topic carded.'),
    ('paper', 14, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'or', 'Q15(a)(iii) "birds or chicks": description.'),
    ('paper', 14, 'the following', 'Q15(b)(iv) "each of the following pairs of terms": one card per numbered pair.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
ITEM_ROMAN = 'The scheme prints no reprint: a numbered item is anchored on the roman it is printed under.'
ITEM_LETTER = 'The scheme prints no reprint: a numbered item is anchored on the letter it is printed under.'
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
ITEM_WELDED = ('The scheme prints no reprint: a numbered item is anchored on the roman it is printed under, which '
               'shares its line with the item\'s own number.')
TERMS = 'The scheme sets the part\'s two terms, each over its definition, under its own marker: anchored on it.'
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
ROW_PRICED = 'Sections B and C print a mark against every row.'
WHOLE56 = ('The scheme prints Q{q} as "1 + 1 + 8 + 6 + 4(1)" over its eight responses, a notation printed nowhere '
           'else in the 2010-2026 schemes. Read as the conventions page defines an ordered split, the first two correct '
           'responses would earn 1 mark each, the third 8 and the fourth 6; no reading prices each printed answer on '
           'its own, so the whole question is one card at the Section A rubric\'s 20 ("5(20)"), every row unpriced '
           '(the coordinator\'s whole-part rule; the author had carded each response at 1). Brought to Alex.')


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def term(page, word, br=False, nth=1):
    """A printed term the paper sets before its answer line ("Starch. ____")."""
    return Q(page, word, word, br=br, nth=nth)


def item(page, n, end, anchor, br=False):
    """One entry of a printed numbered list whose number stands on its own line."""
    return Q(page, f'{n}.', end, after=anchor, br=br)


def at(page, *path_and_marker, nth=1, why=NO_REPRINT):
    """The part's own marker, walked down to through the scheme's numbering."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def welded(page, *path_and_marker, nth=1, why=WELDED):
    """The part's marker opening its own answer line ("(b) Endothermic"): a
    welded bare anchor."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth, welded=True)


def pieces(sel_start, sel_end=None, n=2, **kw):
    """Each answer of a printed solidus list, in order: one selector per entry."""
    return [dict(S(sel_start, sel_end, piece=i, **kw)) for i in range(1, n + 1)]


def defined(line):
    """The definition the scheme prints after its term's dash ("– polysaccharide ...")."""
    return S(line, piece=2, psep='– ')


def ladder(q, notation):
    return f'The scheme prints Q{q} as "{notation}": an ordered split, each response carded at its first rate.'


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'In the case of any five of the following pairs of terms,', 'by writing a brief sentence about each.')
Q2 = ask(2, 'Answer the following questions in relation to food chains.')
Q2EI = ask(2, 'Can a parasite be the first member of a food chain?')
Q3 = Q(3, 'The relationship between body temperature and environmental temperature for two animals is',
       'One of these animals is a dog and the other is a lizard.')
Q4 = ask(4, 'The diagram shows a strawberry plant from which a runner has given rise to a daughter plant.')
Q4A = Q(4, 'The runner is a modified stem.', 'How could you tell this from')
Q6AII = ask(5, 'In each case, name the complementary base in RNA for:')
Q7A = ask(6, 'Distinguish between the terms habitat and ecosystem by writing a sentence about each.')
Q7B = ask(6, 'Answer the following questions in relation to a named ecosystem which you have investigated.')
Q7BV = Q(6, 'As part of your study of your selected ecosystem you constructed a pyramid of numbers.',
         'Name the species that occupied the top of your pyramid.')
Q8B = Q(7, 'Answer the following in relation to an activity that you carried out to investigate the effect of',
        'heat denaturation on the activity of an enzyme.')
Q9B = Q(8, 'Answer the following in relation to investigations that you carried out in the course of your',
        'practical studies.')
Q9BI = Q(8, 'When investigating the effect of either carbon dioxide concentration or light intensity',
         'on the rate of photosynthesis:')
Q9BII = ask(8, 'When demonstrating osmosis:')
Q9BIII = ask(8, 'In the microscopic examination of a plant cell:')
Q9BIV = ask(8, 'When investigating digestive activity during seed germination:')
Q10AI = ask(9, 'What term is used for glands that secrete hormones?')
Q10B = Q(9, 'Answer the following by reference to hormones, other than sex hormones, which you have',
         'encountered in the course of your studies.')
Q10BII = ask(9, 'In the case of each of two named hormones secreted in the human body state:')
Q10BIII = ask(9, 'In the case of one of the hormones referred to in part (b) (ii):')
Q11AI = ask(10, 'Give a source of evidence for evolution.')
Q11BI = Q(10, 'Human males and females differ in one of their twenty three pairs of chromosomes.',
          'What name is given to this pair of chromosomes?')
Q11BII = Q(10, 'Draw this pair of chromosomes for a human male and for a human female and label them',
           'appropriately.')
Q11C = ask(10, 'Answer the following questions, which relate to events in the cell cycle.')
Q11CI = ask(10, 'What name is applied to the period of the cell cycle in which division is not taking place?')
Q11CIII = Q(10, 'Draw a labelled diagram to show the position of the chromosomes during metaphase of',
            'mitosis in a nucleus in which 2n = 6.')
Q11CIV1 = Q(10, '1. State a function of one of the structures, other than chromosomes, that you have labelled',
            'in your diagram of metaphase.')
Q12BII = [Q(11, 'Draw a large diagram of a bacterial cell to show:'),
          ask(11, '1. The relative positions of the cell wall, cell membrane and capsule.', br=True),
          Q(11, '2.', 'A plasmid.', after='cell membrane and capsule.', br=True),
          ask(11, 'Label each of the above structures.', br=True)]
Q13AI = Q(12, 'In humans, widening of the female hips is one example of physical changes that distinguish',
          'To what term does the definition in italics refer?')
Q13A = Q(12, 'In humans, widening of the female hips is one example of physical changes that distinguish',
         'the sexes but are not essential for reproduction.')
Q13B = ask(12, 'The diagram shows the reproductive system of the human female.')
Q13BII = ask(12, 'Using the letters from part (i), identify the following locations:')
Q13C = ask(12, 'Answer the following questions in relation to the development of a human zygote.')
Q14A = ask(13, 'The scheme below summarises the process of photosynthesis.')
Q14AII = ask(13, 'In the first stage, pathways I and II relate to the passage of energised electrons.')
Q14AIII = ask(13, 'Give the name of the second stage.')
Q14B = Q(13, 'Write notes on each of the following topics.', 'Marks will not be given for word diagrams alone.')
Q14CII = ask(13, 'Name an organism that is used in industrial fermentation.')
Q14CV = ask(13, 'In industrial fermentations bioprocessing with immobilised cells is sometimes used.')
Q15A = [ask(14, 'Read the article below and answer the questions that follow:'),
        Q(14, 'Cigarettes are bad for your health.', 'fibres found in used cigarette filters.'),
        Q(14, 'Scientists got to wondering whether this habit', 'a butt a day might keep the mites away!'),
        Q(14, '*[Biology Letters:', 'new ingredients for an old recipe.’]'),
        Q(14, 'Adapted from Scientific American', '05/12/2012.')]
Q15BIV = Q(14, 'In the case of each of the following pairs of terms, distinguish between the members of each',
           'pair by writing a sentence about each term.')
Q15C = ask(15, 'The graph below shows the fluctuations in the population of a predatory species over many years.')

# Q1(e)'s second test and its answer, printed on one scheme line (p5).
BENEDICT = 'Benedict’s (Fehling’s) – (test for) reducing sugar (or glucose or maltose)'
# Q13(b)(i)'s parts as the scheme names them (p13).
SYSTEM = [('A', 'Vagina'), ('B', 'Uterus (or womb)'), ('C', 'Endometrium (or lining of uterus or lining of womb)'),
          ('D', 'Fallopian tube (or oviduct)'), ('E', 'Ovary'), ('F', 'Cervix')]
SYSTEM_KEY = [L(x, S(name, page=13), True) for x, name in SYSTEM]
# Q14(b)'s direction to the examiner, printed once above its three notes (p14).
NOTE_14B = S('If any', 'may be awarded.', after='(30, 30)')
# Q15(b)(i)'s eleven bulleted points (p16), each its own printed line.
NITROGEN = ['Nitrogen gas to usable compounds /', 'Plant protein to animal protein /',
            'Excretion releasing N compounds /', 'Death and decomposition /', 'Dead organic matter to ammonium',
            'Ammonium to nitrite /', 'Nitrite to nitrate /', 'Nitrates to plant protein /',
            'Nitrogen compounds to nitrogen gas /', 'One example of bacterial involvement /', 'Role of lightning']

TASKS = [
    # ------------------------------------------------------------ Section A --
    # Each pair's two terms are short, so the card carries Q1's printed
    # lead-in in its question text, the two terms on their own lines.
    T(f'1{x}', f'Q1({x})', 'A', [Q1, term(2, first, br=True), term(2, second, br=True)],
      [pt(defined(ans1), 2, label=lab1), pt(defined(ans2), 2, label=lab2)], 'bio-1-2', concept, sq, 4,
      decision='The scheme prints Q1 as "5(4, 2, 0) i.e. best five answers from (a) – (f)": six parts, the best '
               'five at 4, a part\'s two terms 2 each (one term right earns 2).')
    for x, first, second, lab1, ans1, lab2, ans2, concept, sq in [
        ('a', 'Starch.', 'Glucose.', S('Starch'), '– polysaccharide (or explained) or polymer or correct test',
         S('Glucose'), '– monosaccharide (or explained) or monomer or correct test', 'starch-and-glucose',
         at(5, '1.', '(a)', why=TERMS)),
        ('b', 'Amino acids.', 'Proteins.', S('Amino Acid'), '– building block of protein or monomer or unit of protein',
         S('Protein'), '– polymer (of amino acids) or chain of (or many) amino acids', 'amino-acids-and-proteins',
         welded(5, '1.', '(b)', why=TERMS)),
        ('c', 'Cellulose.', 'Keratin.', S('Cellulose'), '– carbohydrate or polysaccharide or (found in plant) cell wall',
         S('Keratin'), '– protein or (found in human) hair (or nails or skin)', 'cellulose-and-keratin',
         at(5, '1.', '(c)', why=TERMS)),
        ('d', 'Enzymes.', 'Hormones.', S('Enzyme'), '– a catalyst (or explained)',
         S('Hormone'), '– a (chemical) messenger (or explained)', 'enzymes-and-hormones',
         welded(5, '1.', '(d)', why=TERMS))]
] + [
    T('1e', 'Q1(e)', 'A', [Q1, term(2, 'Biuret test.', br=True), term(2, 'Benedict’s (Fehling’s) test.', br=True)],
      [pt(defined('– (test for) protein'), 2, label=S('Biuret')),
       pt(S(BENEDICT, piece=2, psep=' – '), 2, label=S(BENEDICT, piece=1, psep=' – '))],
      'bio-1-2', 'biuret-and-benedicts', at(5, '1.', '(e)', why=TERMS), 4,
      decision='The scheme prints Q1 as "5(4, 2, 0) i.e. best five answers from (a) – (f)": six parts, the best '
               'five at 4, a part\'s two tests 2 each. The scheme sets Benedict\'s (Fehling\'s) and its answer on '
               'one line, cut at its own dash.'),
    T('1f', 'Q1(f)', 'A', [Q1, term(2, 'Fats.', br=True), term(2, 'Oils.', br=True)],
      [pt(defined('– (lipids) solid at room temp'), 2, label=S('Fats')),
       pt(defined('– (lipids) liquid at room temp'), 2, label=S('Oils'))], 'bio-1-2', 'fats-and-oils',
      at(5, '1.', '(f)', why=TERMS), 4,
      decision='The scheme prints Q1 as "5(4, 2, 0) i.e. best five answers from (a) – (f)": six parts, the best '
               'five at 4, a part\'s two terms 2 each (one term right earns 2).'),
] + [
    T(f'2{k}', f'Q2{ref}', 'A', q, [pt(S(ans), 3)], 'bio-3-1', concept, sq, 3, stem=stem,
      decision=ladder(2, '6(3) + 2') + ' Seven responses.')
    for k, ref, q, ans, concept, sq, stem in [
        ('a', '(a)', ask(2, 'Where in a food chain are primary producers found?'), 'First (level)',
         'primary-producers', at(5, '2.', '(a)'), [Q2]),
        ('b', '(b)', ask(2, 'What term is used to describe organisms that feed on primary producers?'),
         'Primary consumer(s) or herbivore(s)', 'primary-consumers', welded(5, '2.', '(b)'), [Q2]),
        ('c', '(c)', ask(2, 'Why are most food chains short (i.e. only consist of a few trophic levels)?'),
         '(Large) energy loss (from one level to next) or small energy transfer', 'short-food-chains',
         at(5, '2.', '(c)'), [Q2]),
        ('d', '(d)', Q(2, 'What deduction may be made if the organisms at the start of the chain are less numerous than '
                          'those', 'that feed upon them?'),
         'Producers are large or primary consumers are parasites', 'inverted-pyramid-of-numbers',
         welded(5, '2.', '(d)'), [Q2]),
        ('ei', '(e)(i)', Q2EI, 'No', 'parasites-in-food-chains', at(5, '2.', '(e)', '(i)'), [Q2]),
        ('eii', '(e)(ii)', ask(2, 'Explain your answer.'),
         '(Parasites) are not producers or (parasites) are consumers (or explained)', 'parasites-are-consumers',
         welded(5, '2.', '(e)', '(ii)'), [Q2, M('(i)', 2), Q2EI]),
        ('f', '(f)', Q(2, 'Energy enters food chains in the form of light.', 'food chains?'), 'Heat',
         'energy-lost-as-heat', at(5, '2.', '(f)'), [Q2])]
] + [
    T('3a', 'Q3(a)', 'A', [ask(3, 'Which of the plots, X or Y, relates to the dog?'),
                           ask(3, 'Explain your answer.', br=True)],
      [pt(S('X'), 3), pt(S('Dog', 'correct reference to graph'), 3)], 'bio-2-4', 'endotherm-plot',
      at(6, '3.', '(a)'), 6, stem=[Q3], fig='q3-graph',
      decision='The plot and its explanation are two responses on the "6(3) + (2)" ladder, as the paper\'s two '
               'answer lines ask. The text layer sets the apostrophe of the scheme\'s "Dog\'s" as U+201F, a font '
               'artefact read as the apostrophe printed (U+2019).'),
] + [
    T(f'3{x}', f'Q3({x})', 'A', q, [pt(S(*ans), 3)], 'bio-2-4', concept, sq, 3, stem=[Q3], fig='q3-graph',
      decision=ladder(3, '6(3) + (2)') + ' Seven responses.')
    for x, q, ans, concept, sq in [
        ('b', ask(3, 'In relation to body temperature, what term is used to describe animals such as the dog?'),
         ('Endothermic',), 'endothermic', welded(6, '3.', '(b)')),
        ('c', ask(3, 'What is the main source of the dog’s body heat?'),
         ('Respiration or metabolism or carbohydrate (or named carbohydrate) or fat (or named fat)',),
         'endotherm-heat-source', at(6, '3.', '(c)')),
        ('d', Q(3, 'Suggest a value to dogs of the relationship between their body temperature and environmental',
                'temperature.'),
         ('(Temperature always suitable) for good enzyme activity or', 'activity independent of environment'),
         'value-of-endothermy', welded(6, '3.', '(d)')),
        ('e', ask(3, 'In relation to body temperature, what term is used to describe animals such as the lizard?'),
         ('Ectothermic',), 'ectothermic', at(6, '3.', '(e)')),
        ('f', ask(3, 'What is the main source of the lizard’s body heat?'), ('Environment or the sun or metabolism',),
         'ectotherm-heat-source', at(6, '3.', '(f)'))]
] + [
    T(f'4a{n}', f'Q4(a){n}', 'A', q, [pt(S(ans), 3)], 'bio-2-6', concept, at(6, '4.', '(a)', why=ITEM_LETTER), 3,
      stem=[Q4, Q4A], fig='q4-strawberry', decision=EACH_ITEM + ' ' + ladder(4, '6(3) + (2)'))
    for n, q, ans, concept in [
        (1, Q(4, '1.', 'external observation?'), 'Bud(s) or node(s) or leaf', 'stem-external-features'),
        (2, Q(4, '2. viewing a thin section of it under the microscope?', piece=1, psep='_'),
         'Vascular bundles [plural only]', 'stem-vascular-bundles')]
] + [
    T('4b', 'Q4(b)', 'A', ask(4, 'What term is used for the type of asexual reproduction that produced the daughter '
                                 'plant?'),
      [pt(S('Vegetative propagation'), 3)], 'bio-2-5', 'vegetative-propagation', welded(6, '4.', '(b)'), 3,
      stem=[Q4], fig='q4-strawberry', decision=ladder(4, '6(3) + (2)') + ' Seven responses.'),
    T('4c', 'Q4(c)', 'A', [ask(4, 'Would you expect the daughter plant to be haploid or diploid?'),
                           Q(4, 'Explain your answer.', piece=1, psep='_', br=True)],
      [pt(S('Diploid'), 3), pt(S('Product of mitosis or genetically identical (to parent) or clone'), 3)], 'bio-2-5',
      'daughter-plant-is-diploid', at(6, '4.', '(c)'), 6, stem=[Q4], fig='q4-strawberry',
      decision='The answer and its explanation are two responses on the "6(3) + (2)" ladder, as the paper\'s two '
               'answer lines ask.'),
    T('4d', 'Q4(d)', 'A', ask(4, 'What evidence is there in the diagram that sexual reproduction has also taken place?'),
      [pt(S('Fruit or (straw)berries or seeds'), 3)], 'bio-2-5', 'evidence-of-sexual-reproduction',
      welded(6, '4.', '(d)'), 3, stem=[Q4], fig='q4-strawberry', decision=ladder(4, '6(3) + (2)') + ' Seven responses.'),
    T('4e', 'Q4(e)', 'A', Q(4, 'Give one method, other than runners, and not involving seeds, that is used by '
                               'horticulturists to', 'produce new plants.'),
      [pt(S('Cuttings or layering or grafting or micro-propagation or tissue culture'), 3)], 'bio-2-5',
      'artificial-propagation', at(6, '4.', '(e)'), 3, stem=[Q4], fig='q4-strawberry',
      decision=ladder(4, '6(3) + (2)') + ' Seven responses.'),
] + [
    # Q5 and Q6: the scheme prints each as "1 + 1 + 8 + 6 + 4(1)" over eight
    # responses. Read as the conventions page defines an ordered split, the
    # first two correct responses would earn 1 mark each and the third 8; no
    # reading of it prices each printed answer on its own, so each question is
    # carded whole at the Section A rubric's 20, every row unpriced.
    T('5', 'Q5', 'A',
      [M('(a)', 5), M('(i)', 5),
       ask(5, 'In relation to structures such as the cell membrane, explain the term selective permeability.'),
       M('(ii)', 5, br=True), ask(5, 'Suggest an advantage to the cell of having a selectively permeable membrane.'),
       M('(iii)', 5, br=True), ask(5, 'Name two substances that enter a human muscle cell by diffusion.'),
       M('(b)', 5, br=True), M('(i)', 5), ask(5, 'Explain the term turgor.'),
       M('(ii)', 5, br=True), ask(5, 'Give a feature of a plant cell that allows it to remain turgid for long periods.'),
       M('(iii)', 5, br=True), ask(5, 'Suggest a way in which turgor is of value to plants.')],
      [pt(S('Only certain substances (or named substances) allowed through'), 0),
       pt(S('Substances can be kept in (or out) or substances can be let in (or out)'), 0),
       anyn(S('Oxygen / glucose / water / amino acids / phosphate (or P) / iron'), 2, 0, note_sel=S('Any two')),
       anyn(S('Pressure / of cell contents (or described) / on cell wall'), 2, 0, note_sel=S('Any two', nth=2)),
       pt(S('Vacuole or cell wall or cell sap'), 0),
       pt(S('Support (or described)'), 0)],
      'bio-2-6', 'membranes-and-turgor', at(7, '5.', '(a)', '(i)'), 20, tariff='questionTotal',
      decision=WHOLE56.format(q=5)),
    T('6', 'Q6', 'A',
      [M('(a)', 5), M('(i)', 5), Q(5, 'In DNA, nitrogenous bases occur in complementary pairs.', 'used here.'),
       M('(ii)', 5, br=True), Q6AII, Q(5, '1. Adenine', piece=1, psep=' _', br=True),
       Q(5, '2. Cytosine', piece=1, psep=' _', br=True),
       M('(iii)', 5, br=True), ask(5, 'Name a carbohydrate that is a component of nucleotides.'),
       M('(iv)', 5, br=True),
       ask(5, 'Name a component of a nucleotide that is neither a carbohydrate nor a nitrogenous base.'),
       M('(b)', 5, br=True), M('(i)', 5), ask(5, 'What does the ‘m’ stand for in mRNA?'),
       M('(ii)', 5, br=True), ask(5, 'Give one difference between RNA and DNA, other than the nitrogenous bases.'),
       M('(iii)', 5, br=True), ask(5, 'Give the role of the enzyme RNA polymerase.')],
      [pt(S('Each base has a (different) corresponding (or matching) (base)'), 0),
       pt(S('Uracil or U'), 0), pt(S('Guanine or G'), 0),
       pt(S('(iii) Ribose or deoxyribose', piece=2, psep=') '), 0),
       pt(S('Phosphate (group) or P'), 0), pt(S('Messenger'), 0),
       pt(S('RNA has ribose or RNA is single stranded', 'or DNA has deoxyribose or DNA is double stranded'), 0),
       pt(S('Joins nucleotides together (to give mRNA product) or to make RNA'), 0)],
      'bio-2-3', 'nucleic-acids', at(7, '6.', '(a)', '(i)'), 20, tariff='questionTotal',
      decision=WHOLE56.format(q=6)),
] + [
    # ------------------------------------------------------------ Section B --
    # "Habitat." and "Ecosystem." are short, so each card carries (a)'s
    # printed lead-in in its question text.
    T(f'7a{r}', f'Q7(a)({r})', 'B', [Q7A, term(6, word, br=True)], [pt(S(ans), 3)], 'bio-3-1', concept,
      at(8, '7.', '(a)', f'({r})'), 3, decision=ROW_PRICED)
    for r, word, ans, concept in [('i', 'Habitat.', 'Where an organism (or plant and animal) lives', 'habitat'),
                                  ('ii', 'Ecosystem.', 'Organisms (interacting) with their environment', 'ecosystem')]
] + [
    T('7bi', 'Q7(b)(i)', 'B', [ask(6, 'How did you investigate a named abiotic factor, other than temperature or pH?'),
                               term(6, 'Abiotic factor.', br=True), term(6, 'How investigated.', br=True)],
      [pt(S('Factor'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('How investigated'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'investigating-an-abiotic-factor',
      at(8, '7.', '(b)', '(i)'), 6, stem=[Q7B],
      decision='The factor and how it was investigated are priced "3" each and the scheme prints neither: two '
               'criterion rows.'),
    T('7bii', 'Q7(b)(ii)', 'B', ask(6, 'How were you able to identify the animals that you found in the ecosystem?'),
      [pt(S('Key or (guide) book or illustrations'), 3)], 'bio-3-1', 'identifying-organisms',
      at(8, '7.', '(b)', '(ii)'), 3, stem=[Q7B]),
    T('7biii', 'Q7(b)(iii)', 'B', Q(6, 'When conducting a quantitative survey of plants, how did you ensure that your '
                                       'sample was', 'random?'),
      [pt(S('Method described must demonstrate randomness'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'random-sampling', welded(8, '7.', '(b)', '(iii)'), 3, stem=[Q7B]),
    T('7biv', 'Q7(b)(iv)', 'B', Q(6, 'In the case of a named animal and a named plant give an example of an adaptation '
                                     'to its', 'habitat that you observed.'),
      [pt(S('Named animal + adaptation'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Named plant + adaptation'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'adaptations',
      welded(8, '7.', '(b)', '(iv)'), 6, stem=[Q7B],
      decision='The animal and the plant are priced "3" each, each with its adaptation, and the scheme prints '
               'neither: two criterion rows.'),
    T('7bv', 'Q7(b)(v)', 'B', Q7BV,
      [pt(S('Named (species) of carnivore or of omnivore or of parasite'), 3, kind='criterion', note=NO_ANSWER)],
      'bio-3-1', 'top-of-pyramid-of-numbers', at(8, '7.', '(b)', '(v)'), 3, stem=[Q7B]),
    T('7bvi', 'Q7(b)(vi)', 'B', ask(6, 'What is the main prey of the species referred to in part (v)?'),
      [pt(S('Matching named prey'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'main-prey',
      welded(8, '7.', '(b)', '(vi)'), 3, stem=[Q7B, M('(v)', 6), Q7BV]),
    T('8ai', 'Q8(a)(i)', 'B', Q(7, 'What term is used for the substance(s) that result(s) from the action of an enzyme '
                                   'on its', 'substrate?'),
      [pt(S('Product(s)'), 3)], 'bio-2-1', 'products', at(8, '8.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('8aii', 'Q8(a)(ii)', 'B', ask(7, 'In relation to an enzyme, explain the term optimum activity.'),
      [pt(S('Working at maximum rate'), 3)], 'bio-2-1', 'optimum-activity', at(8, '8.', '(a)', '(ii)'), 3),
    T('8bi', 'Q8(b)(i)', 'B', ask(7, 'Name the enzyme and the substrate that you used.'),
      [pt(S('Named enzyme'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Matching substrate'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-1', 'enzyme-and-substrate-used',
      at(8, '8.', '(b)', '(i)'), 6, stem=[Q8B],
      decision='The enzyme and its substrate are priced "3" each and the scheme names neither: two criterion rows.'),
    T('8bii', 'Q8(b)(ii)', 'B', Q(7, 'Describe how you carried out the investigation.',
                                  'In your description outline how you measured the activity of the enzyme.'),
      [anyn(S('Temperature', 'how kept constant', skip_marks=True), 5, 3)], 'bio-2-1', 'heat-denaturation-method',
      at(8, '8.', '(b)', '(ii)'), 15, stem=[Q8B],
      decision='"5(3)" over nine printed points: a menu, claim five. The scheme prints its "5(3)" between the '
               'menu\'s third and fourth lines; the mark cell is left out of the menu.'),
    T('8biii', 'Q8(b)(iii)', 'B', ask(7, 'Using suitably labelled axes, draw a graph of the results that you obtained.'),
      [pt(S('Any attempt'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-1', 'graphing-denaturation',
      welded(8, '8.', '(b)', '(iii)'), 3, stem=[Q8B]),
    T('9ai', 'Q9(a)(i)', 'B', ask(8, 'Explain the importance of double-blind testing in scientific experimentation.'),
      [pt(S('Avoidance of bias'), 3)], 'bio-u2', 'double-blind-testing', at(9, '9.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('9aii', 'Q9(a)(ii)', 'B', ask(8, 'How does a hypothesis differ from a theory?'),
      [pt(S('Hypothesis can develop into a theory or explained'), 3)], 'bio-u2', 'hypothesis-and-theory',
      at(9, '9.', '(a)', '(ii)'), 3),
    T('9bi1', 'Q9(b)(i)1', 'B', item(8, 1, 'How did you vary your chosen factor?', 'on the rate of photosynthesis:'),
      [pt(S('vary NaHCO3 conc.'), 3, label=S('CO2 –', piece=1, psep=' –'))], 'bio-2-2', 'varying-the-factor',
      at(9, '9.', '(b)', '(i)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BI],
      decision=EACH_ITEM + ' The scheme prints one answer for carbon dioxide and one for light, joined by "OR", '
               'beside one "3": answer variants of one task.'),
    T('9bi2', 'Q9(b)(i)2', 'B', item(8, 2, 'draw a graph of the results that you obtained.',
                                    'on the rate of photosynthesis:'),
      [pt(S('Graph with labelled axes (rate on y-axis) + rise'), 3, kind='criterion')], 'bio-2-2',
      'graphing-photosynthesis-rate', at(9, '9.', '(b)', '(i)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BI],
      decision=EACH_ITEM + ' The graph is one priced item: one criterion row naming what it must show.'),
] + [
    T(f'9b{r}{n}', f'Q9(b)({r}){n}', 'B', q, [pt(S(ans), 3)], topic, concept,
      at(9, '9.', '(b)', f'({r})', why=ITEM_ROMAN), 3, stem=[Q9B, lead], decision=EACH_ITEM)
    for r, n, q, ans, topic, concept, lead in [
        ('ii', 1, ask(8, '1. For what purpose did you use Visking tubing, potato tissue or some similar material?'),
         'As a selectively permeable membrane', 'bio-2-6', 'visking-tubing', Q9BII),
        ('ii', 2, ask(8, '2. At the end of the demonstration, how did you conclude that osmosis had occurred?'),
         'Change (increase or decrease) in mass (volume) or described', 'bio-2-6', 'evidence-of-osmosis', Q9BII),
        ('iii', 1, item(8, 1, 'Name the stain that you used and the colour it imparted to the cell wall.',
                        'In the microscopic examination of a plant cell:'),
         'e.g. Iodine → yellow (or orange or brown)', 'bio-1-3', 'staining-plant-cells', Q9BIII),
        ('iii', 2, item(8, 2, 'How did you apply the stain to the cells on the slide?',
                        'In the microscopic examination of a plant cell:'),
         'Dropper or use of filter paper', 'bio-1-3', 'applying-the-stain', Q9BIII),
        ('iv', 1, ask(8, '1. How did you supply a substrate suitable for the digestive enzymes?'),
         'Milk agar or starch agar', 'bio-2-5', 'substrate-for-digestion', Q9BIV),
        ('iv', 2, ask(8, '2. How did you ensure that no digestive enzymes were available on the control plate?'),
         'Boiled seeds', 'bio-2-5', 'boiled-seed-control', Q9BIV)]
] + [
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', Q10AI, [pt(S('*Endocrine'), 3)], 'bio-2-4', 'endocrine-glands',
      at(10, '10.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('10aii', 'Q10(a)(ii)', 'C', ask(9, 'How do these glands differ from those that do not secrete hormones?'),
      [pt(S('Ductless'), 3)], 'bio-2-4', 'ductless-glands', at(10, '10.', '(a)', '(ii)'), 3,
      stem=[M('(i)', 9), Q10AI]),
    T('10aiii', 'Q10(a)(iii)', 'C', ask(9, 'Explain why the pancreas may be described as a dual-function gland.'),
      [pt(S('Hormone (or insulin) secretion & non-hormone (enzyme) secretions',
            'or has endocrine and exocrine function (or described)'), 3)], 'bio-2-4', 'pancreas-dual-function',
      welded(10, '10.', '(a)', '(iii)'), 3),
    T('10bi', 'Q10(b)(i)', 'C', ask(9, 'What is the chemical nature of many hormones?'), [pt(S('Protein'), 3)],
      'bio-2-4', 'hormones-are-proteins', at(10, '10.', '(b)', '(i)'), 3, stem=[Q10B]),
    T('10bii', 'Q10(b)(ii)', 'C', [Q10BII, item(9, 1, 'The precise location of the gland that secretes it.',
                                                'two named hormones', br=True),
                                   item(9, 2, 'A function of the hormone.', 'two named hormones', br=True)],
      [pt(S(w), 4, kind='criterion', units=[2, 2], note=NO_ANSWER)
       for w in ('Hormone name', 'Gland location', 'Hormone function')], 'bio-2-4', 'two-named-hormones',
      at(10, '10.', '(b)', '(ii)'), 12, stem=[Q10B],
      decision='The scheme prices the hormones\' names, their glands\' locations and their functions "2(2)" each '
               'and prints none of them: three criterion rows, each worth its two 2s.'),
] + [
    T(f'10biii{n}', f'Q10(b)(iii){n}', 'C', item(9, n, end, 'referred to in part'),
      [pt(S(row), 2, kind='criterion', note=NO_ANSWER)], 'bio-2-4', concept,
      welded(10, '10.', '(b)', '(iii)', why=ITEM_WELDED), 2,
      stem=[Q10B, Q10BIII], decision=EACH_ITEM)
    for n, end, row, concept in [
        (1, 'Give a deficiency symptom.', 'Deficiency symptom', 'hormone-deficiency-symptom'),
        (2, 'Give a symptom of excess secretion.', 'Excess symptom', 'hormone-excess-symptom'),
        (3, 'have chosen.', 'Corrective measure', 'hormone-corrective-measure')]
] + [
    T('10biv', 'Q10(b)(iv)', 'C', ask(9, 'Explain why hormonal responses are slower than nervous responses.'),
      [pt(S('Hormones travel in blood or are chemical'), 3), pt(S('Electrical transmission in nerves'), 3)],
      'bio-2-4', 'hormonal-and-nervous-responses', at(10, '10.', '(b)', '(iv)'), 6,
      decision='The hormones\' point and the nerves\' point are priced "3" each.'),
    T('10ci', 'Q10(c)(i)', 'C', ask(9, 'State two ways in which growth regulators in plants are similar to hormones in '
                                       'animals.'),
      [anyn(S('Made at one site & function at another /', 'chemical (nature)'), 2, 3)], 'bio-2-4',
      'growth-regulators-and-hormones', at(10, '10.', '(c)', '(i)'), 6,
      decision='"2(3)" over four printed points: a menu, claim two.'),
    T('10cii', 'Q10(c)(ii)', 'C', Q(9, 'Name a plant growth regulator that promotes growth and give a precise location '
                                       'for a site of its', 'action.'),
      [pt(S('e.g. IAA (auxin)'), 3), pt(S('Just behind shoot (or root) tip or meristem or zone of elongation'), 3)],
      'bio-2-4', 'growth-promoter-and-site', at(10, '10.', '(c)', '(ii)'), 6,
      decision='The regulator and its site are priced "3" each.'),
    T('10ciii', 'Q10(c)(iii)', 'C', ask(9, 'Through which part of a stem are growth promoters transported?'),
      [pt(S('Vascular bundles or vascular tissue or phloem or xylem'), 3)], 'bio-2-4', 'transport-of-growth-promoters',
      welded(10, '10.', '(c)', '(iii)'), 3),
    T('10civ', 'Q10(c)(iv)', 'C', ask(9, 'Outline two uses of growth promoters in horticulture.'),
      [anyn(S('(Encourage) rooting (in cuttings) / promote ripening / weed killer /',
              'seedless fruit / micro-propagation or tissue culture'), 2, 3)], 'bio-2-4', 'uses-of-growth-promoters',
      welded(10, '10.', '(c)', '(iv)'), 6, decision='"2(3)" over five printed uses: a menu, claim two.'),
    T('10cv', 'Q10(c)(v)', 'C', ask(9, 'Give an example of a growth regulator that inhibits growth.'),
      [anyn(S('IAA / auxin / ethene (ethylene) / abscissic acid'), 1, 3)], 'bio-2-4', 'growth-inhibitors',
      at(10, '10.', '(c)', '(v)'), 3,
      decision='The ask wants one example; the scheme prints four, cut at its solidi, beside one "3": a menu, claim '
               'one. "abscissic" is the scheme\'s spelling, lifted as printed.'),
    T('11ai', 'Q11(a)(i)', 'C', Q11AI,
      [pt(S('Fossils or embryology or anatomy or adaptation of plant or animal', 'or genetics'), 3)], 'bio-1-5',
      'evidence-for-evolution', at(11, '11.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('11aii', 'Q11(a)(ii)', 'C', ask(10, 'Briefly outline the evidence from the source referred to in (i).'),
      [anyn(S('e.g. Fossils: structure / changing / over time / related to environment', piece=2, psep=': '), 2, 3,
            open_list=True, note_sel=S('e.g. Fossils: structure / changing / over time / related to environment',
                                       piece=1, psep=': '))],
      'bio-1-5', 'outlining-the-evidence', at(11, '11.', '(a)', '(ii)'), 6, stem=[M('(i)', 10), Q11AI],
      decision='The scheme prices "Any two points from evidence selected above: 2(3)" and prints example points '
               'for three sources ("e.g. Fossils:", "e.g. Embryology:", "e.g. Anatomy:"): answer variants of one '
               'task, each an open menu, claim two.'),
    T('11bi', 'Q11(b)(i)', 'C', Q11BI, [pt(S('Heterosomes or sex chromosomes'), 3)], 'bio-1-4', 'sex-chromosomes',
      at(11, '11.', '(b)', '(i)'), 3),
    T('11bii', 'Q11(b)(ii)', 'C', Q11BII,
      [G('lines', page=11, clip=(140, 264, 200, 300), expect='Female — XX', marks=3, note_sel=S('3, 0'),
         note_lead='The scheme marks this drawing', note='(The scheme\'s drawing is shown after reveal.)'),
       G('lines', page=11, clip=(260, 264, 320, 300), expect='Male — XY', marks=3, note_sel=S('3, 0'),
         note_lead='The scheme marks this drawing')],
      'bio-1-4', 'drawing-sex-chromosomes', at(11, '11.', '(b)', '(ii)'), 6, stem=[M('(i)', 10), Q11BI],
      fig='q11bii-scheme',
      decision='The scheme prints its answer as a drawing: "Female" over "XX" and "Male" over "XY", each over a '
               'drawn chromosome pair, and prices each "3, 0". Each is read from its own column by glyph position; '
               'the drawing is the scheme crop shown after reveal.'),
    T('11biii', 'Q11(b)(iii)', 'C', Q(10, 'Using the chromosomes referred to in part (b) (ii), show, using a Punnett '
                                         'square or', 'being male or female.'),
      [pt(S(w), 3, kind='criterion', note='The scheme\'s Punnett square is shown after reveal.' if i == 0 else None)
       for i, w in enumerate(('Gametes shown', 'Cross shown', 'F1 genotypes shown'))],
      'bio-1-4', 'inheritance-of-sex', at(11, '11.', '(b)', '(iii)'), 9, stem=[M('(ii)', 10), Q11BII],
      fig='q11biii-scheme',
      decision='The scheme prints a Punnett square (X and X over X and Y, giving XX and XY) beside three priced '
               'criteria: three criterion rows, the square the scheme crop shown after reveal.'),
    T('11biv1', 'Q11(b)(iv)1', 'C', ask(10, '1. What is meant in genetics by the term sex linkage?'),
      [pt(S('Gene(s) on sex or on X or on Y chromosome'), 3)], 'bio-1-4', 'sex-linkage',
      at(11, '11.', '(b)', '(iv)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('11biv2', 'Q11(b)(iv)2', 'C', ask(10, '2. Name two common sex-linked traits.'),
      [pt(s, 3) for s in pieces('Haemophilia / colour blindness')], 'bio-1-4', 'sex-linked-traits',
      at(11, '11.', '(b)', '(iv)', why=ITEM_ROMAN), 6,
      decision=EACH_ITEM + ' "2(3)": the two traits, cut at the scheme\'s own solidus.'),
    T('11ci', 'Q11(c)(i)', 'C', Q11CI, [pt(S('*Interphase'), 3)], 'bio-2-3', 'interphase', at(11, '11.', '(c)', '(i)'),
      3, stem=[Q11C]),
    T('11cii', 'Q11(c)(ii)', 'C', ask(10, 'Give a cellular process that occurs during this period in which the nucleus '
                                         'is not dividing.'),
      [pt(S('Replication or growth or protein synthesis or respiration', 'or photosynthesis', skip_marks=True), 3)],
      'bio-2-3', 'interphase-processes', at(11, '11.', '(c)', '(ii)'), 3, stem=[Q11C, M('(i)', 10), Q11CI],
      decision='The scheme prints its "3" between the answer\'s two lines; the mark cell is left out of the row.'),
    T('11ciii', 'Q11(c)(iii)', 'C', Q11CIII,
      [pt(S('spindle (or outline of cell) + chromosomes on equator', '+ 6 double chromosomes'), 6, kind='criterion',
          label=S('Diagram:'), note_sel=S('6, 3, 0'), note_lead='The scheme marks this diagram'),
       anyn(S('Chromosome(s) / spindle / centromere(s) / cell membrane'), 3, 1, note_sel=S('Labels:'))],
      'bio-2-3', 'drawing-metaphase', at(11, '11.', '(c)', '(iii)'), 9, stem=[Q11C],
      decision='The drawing is one priced item ("6, 3, 0") and its labels "3(1)", three from the printed four.'),
    T('11civ1', 'Q11(c)(iv)1', 'C', Q11CIV1, [pt(S('Function'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-3',
      'function-of-a-labelled-structure', at(11, '11.', '(c)', '(iv)', why=ITEM_ROMAN), 3,
      stem=[Q11C, M('(iii)', 10), Q11CIII], decision=EACH_ITEM),
    T('11civ2', 'Q11(c)(iv)2', 'C', ask(10, '2. How does the structure carry out this function?'),
      [pt(S('How function is carried out'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-3',
      'how-the-structure-works', at(11, '11.', '(c)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q11C, Q11CIV1],
      decision=EACH_ITEM),
    T('11cv', 'Q11(c)(v)', 'C', Q(10, 'What term is used for the group of disorders in which control has been lost over '
                                      'the rate of', 'mitosis?'),
      [pt(S('Cancer'), 3)], 'bio-2-3', 'cancer', at(11, '11.', '(c)', '(v)'), 3, stem=[Q11C]),
    T('12ai', 'Q12(a)(i)', 'C', Q(11, 'A virus has been described as a piece of genetic material that has escaped from '
                                      'a cell.', 'Give one piece of evidence that supports this description.'),
      [pt(S('Composed of nucleic acid (or DNA or RNA)'), 3)], 'bio-1-1', 'viruses-as-genetic-material',
      at(12, '12.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('12aii', 'Q12(a)(ii)', 'C', Q(11, 'Viruses are examples of obligate parasites.', 'Explain why this is the case.'),
      [pt(S('Can only replicate (or reproduce) inside a cell (or host)'), 3)], 'bio-1-1', 'obligate-parasites',
      at(12, '12.', '(a)', '(ii)'), 3),
    T('12aiii', 'Q12(a)(iii)', 'C', ask(11, 'Give an example of how a virus might be beneficial to mankind.'),
      [pt(S('Genetic engineering or vaccine (production) or cancer treatment', 'or pest control or disease control'),
          3)], 'bio-1-1', 'beneficial-viruses', at(12, '12.', '(a)', '(iii)'), 3),
    T('12bi', 'Q12(b)(i)', 'C', ask(11, 'Name the kingdom to which bacteria belong.'), [pt(S('*Monera'), 3)],
      'bio-3-2', 'monera', at(12, '12.', '(b)', '(i)'), 3),
    T('12bii', 'Q12(b)(ii)', 'C', Q12BII,
      [pt(S('Diagram: wall + membrane + capsule + plasmid shown'), 5, kind='criterion', note_sel=S('5, 3, 0'),
          note_lead='The scheme marks this diagram'),
       pt(S('Labels:'), 4, kind='criterion', units=[1, 1, 1, 1], note=NO_ANSWER)],
      'bio-3-2', 'drawing-a-bacterial-cell', at(12, '12.', '(b)', '(ii)'), 9,
      decision='The scheme prices the drawing of items 1 and 2 together ("1 + 2", "5, 3, 0") and the labels "4(1)", '
               'printing no label words: two criterion rows, the second worth its four 1s.'),
    T('12biii1', 'Q12(b)(iii)1', 'C', ask(11, '1. Under what circumstances does a bacterial cell form an endospore?'),
      [pt(S('Harsh conditions or example'), 3)], 'bio-3-2', 'when-endospores-form',
      at(12, '12.', '(b)', '(iii)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('12biii2', 'Q12(b)(iii)2', 'C', ask(11, '2. Describe briefly how an endospore forms.'),
      [anyn(S('DNA replicates / thick wall (or described) / encloses /', 'shrinkage (or water loss) / of cytoplasm'),
            2, 3)], 'bio-3-2', 'endospore-formation', at(12, '12.', '(b)', '(iii)', why=ITEM_ROMAN), 6,
      decision=EACH_ITEM + ' "2(3)" over five printed points, each cut at the scheme\'s own solidus: a menu, claim two.'),
    T('12biv', 'Q12(b)(iv)', 'C', ask(11, 'Name two types of heterotrophic nutrition used by bacteria.'),
      [pt(S('*Saprophytic'), 3), pt(S('*Parasitic'), 3)], 'bio-3-2', 'heterotrophic-bacteria',
      at(12, '12.', '(b)', '(iv)'), 6),
    T('12ci', 'Q12(c)(i)', 'C', ask(11, 'Distinguish clearly between antibodies and antibiotics by writing a note about '
                                       'each.'),
      [anyn(None, 4, 3, options=[S('Antibodies –', 'in response to antigen (or to infection)', piece=i)
                                 for i in (1, 2, 3)]
            + [S('Antibiotics –', 'micro-organisms / do not affect viruses', piece=i) for i in (1, 2, 3)])],
      'bio-2-4', 'antibodies-and-antibiotics', at(12, '12.', '(c)', '(i)'), 12,
      decision='"4(3)" over three printed points under "Antibodies –" and three under "Antibiotics –": one menu, '
               'claim four. Each list\'s first option carries its own printed heading.'),
    T('12cii', 'Q12(c)(ii)', 'C', ask(11, 'In relation to antibodies, distinguish between active and passive immunity.'),
      [pt(S('Active - antibodies produced in body'), 3), pt(S('Passive – antibodies given'), 3)], 'bio-2-4',
      'active-and-passive-immunity', at(12, '12.', '(c)', '(ii)'), 6),
    T('12ciii', 'Q12(c)(iii)', 'C', Q(11, 'Using your knowledge of antibiotics and bacteria, suggest why a person is more '
                                         'likely to pick up an', 'infection in hospital than at home.'),
      [anyn(S('Antibiotic resistance strains / more pathogens /', 'more people (or poor hygiene) / patients weaker'),
            2, 3)], 'bio-3-2', 'hospital-infections', at(12, '12.', '(c)', '(iii)'), 6,
      decision='"2( 3)" over four printed points: a menu, claim two.'),
    T('13ai', 'Q13(a)(i)', 'C', Q13AI, [pt(S('*Secondary sexual characteristics'), 3)], 'bio-2-5',
      'secondary-sexual-characteristics', at(13, '13.', '(a)', '(i)'), 3, qfig='q13ai-question',
      decision=ROW_PRICED + ' The ask points at "the definition in italics", which the text layer cannot show; the '
                            'card\'s question is the printed ask, cropped.'),
    T('13aii', 'Q13(a)(ii)', 'C', ask(12, 'What term is used for the time in a young person’s life when such changes take '
                                         'place?'),
      [pt(S('*Puberty'), 3)], 'bio-2-5', 'puberty', at(13, '13.', '(a)', '(ii)'), 3, stem=[M('(i)', 12), Q13A]),
    T('13aiii', 'Q13(a)(iii)', 'C', ask(12, 'Name the hormone that maintains such changes throughout the life of a male.'),
      [pt(S('*Testosterone'), 3)], 'bio-2-5', 'testosterone', at(13, '13.', '(a)', '(iii)'), 3,
      stem=[M('(i)', 12), Q13A]),
    T('13bi', 'Q13(b)(i)', 'C', ask(12, 'Name the parts labelled A, B, C, D, E and F.'),
      [pt(S(name), 1, label=S(f'{x}.', piece=1, psep='.')) for x, name in SYSTEM], 'bio-2-5',
      'female-reproductive-system', at(13, '13.', '(b)', '(i)'), 6, stem=[Q13B], fig='q13b-system', labels=SYSTEM_KEY,
      decision='"6(1)": the six parts, each its own row with its printed letter.'),
] + [
    T(f'13bii{n}', f'Q13(b)(ii){n}', 'C', ask(12, f'{n}. {where}'), [pt(S(f'*{x}'), 3)], 'bio-2-5', concept,
      at(13, '13.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q13B, Q13BII], fig='q13b-system',
      decision=EACH_ITEM + ' The answer is a letter of the diagram.')
    for n, where, x, concept in [(1, 'Where meiosis occurs.', 'E', 'site-of-meiosis'),
                                 (2, 'Where zygote formation occurs.', 'D', 'site-of-fertilisation'),
                                 (3, 'Where implantation occurs.', 'C', 'site-of-implantation')]
] + [
    T('13biii', 'Q13(b)(iii)', 'C', Q(12, 'Describe the role of oestrogen and progesterone in the control of the events '
                                         'of the menstrual', 'cycle.'),
      [anyn(S(line, piece=2, psep=': '), 2, 3, note_sel=S(line, piece=1, psep=': '))
       for line in ('Oestrogen: Endometrium repair / stimulates LH / inhibits FSH',
                    'Progesterone: Endometrium maintenance / inhibits LH / inhibits FSH')],
      'bio-2-5', 'hormones-of-the-menstrual-cycle', at(13, '13.', '(b)', '(iii)'), 12,
      decision='Oestrogen\'s three points "2(3)" and progesterone\'s three "2(3)": two menus, claim two of each.'),
    T('13ci', 'Q13(c)(i)', 'C', ask(12, 'By which type of cell division does the zygote divide?'), [pt(S('*Mitosis'), 3)],
      'bio-2-5', 'zygote-divides-by-mitosis', at(13, '13.', '(c)', '(i)'), 3, stem=[Q13C]),
    T('13cii', 'Q13(c)(ii)', 'C', Q(12, 'Further divisions result in the formation of a morula.', 'the morula?'),
      [pt(S('*Blastocyst'), 3)], 'bio-2-5', 'blastocyst', at(13, '13.', '(c)', '(ii)'), 3, stem=[Q13C]),
    T('13ciii', 'Q13(c)(iii)', 'C', Q(12, 'The placenta forms from tissues of the mother and the foetus.',
                                      'Give two roles of the placenta.'),
      [anyn(S('Makes progesterone / barrier or one (barrier) example /', 'material transfer or one (transfer) example'),
            2, 3)], 'bio-2-5', 'roles-of-the-placenta', at(13, '13.', '(c)', '(iii)'), 6, stem=[Q13C],
      decision='"2(3)" over three printed roles: a menu, claim two.'),
    T('13civ', 'Q13(c)(iv)', 'C', ask(12, 'Give one change experienced by the mother that indicates to her that the birth '
                                         'process is starting.'),
      [pt(S('(Mucus) show or contractions or waters break'), 3)], 'bio-2-5', 'signs-of-labour',
      at(13, '13.', '(c)', '(iv)'), 3, stem=[Q13C]),
    T('13cv', 'Q13(c)(v)', 'C', ask(12, 'Give a short account of the birth process.'),
      [pt(S('Contractions or amniotic sac breaks or cervix dilates'), 3), pt(S('Baby delivered'), 3),
       pt(S('Afterbirth delivered'), 3)], 'bio-2-5', 'birth', at(13, '13.', '(c)', '(v)'), 9, stem=[Q13C],
      decision='The three stages are priced "3" each.'),
    # Q14(a)
    T('14ai', 'Q14(a)(i)', 'C', ask(13, 'Give the name of the first stage.'), [pt(S('*Light (dependent stage)'), 3)],
      'bio-2-2', 'light-stage', at(14, '14.', '(a)', '(i)'), 3, stem=[Q14A], fig='q14a-scheme', decision=ROW_PRICED),
] + [
    T(f'14aii{n}', f'Q14(a)(ii){n}', 'C', item(13, n, end, 'passage of energised electrons.'),
      [anyn(S(*menu), 2, 3)], 'bio-2-2', concept, at(14, '14.', '(a)', '(ii)', why=ITEM_ROMAN), 6,
      stem=[Q14A, Q14AII], fig='q14a-scheme', decision=EACH_ITEM + ' "2(3)": a menu, claim two.')
    for n, end, menu, concept in [
        (1, 'Explain what happens to these electrons in pathway I.',
         ('(electrons) picked up by acceptor / passed through carriers /', 'back to chlorophyll / (electrons) lose energy'),
         'cyclic-electron-flow'),
        (2, 'Describe the events of pathway II.', ('H2O split / protons to pool /', 'O2 released / ATP produced'),
         'non-cyclic-electron-flow')]
] + [
    T('14aiii', 'Q14(a)(iii)', 'C', Q14AIII, [pt(S('*Dark (stage) (or *light-independent stage)'), 3)], 'bio-2-2',
      'dark-stage', at(14, '14.', '(a)', '(iii)'), 3, stem=[Q14A], fig='q14a-scheme'),
    T('14aiv', 'Q14(a)(iv)', 'C', ask(13, 'Explain why the second stage is given the name referred to in part (iii).'),
      [pt(S('Light not needed'), 3)], 'bio-2-2', 'why-the-dark-stage', at(14, '14.', '(a)', '(iv)'), 3,
      stem=[Q14A, M('(iii)', 13), Q14AIII], fig='q14a-scheme'),
    T('14av', 'Q14(a)(v)', 'C', ask(13, 'Give one reason why the second stage cannot happen without the first stage.'),
      [pt(S('Product (or named product)'), 3)], 'bio-2-2', 'dark-stage-needs-light-stage',
      at(14, '14.', '(a)', '(v)'), 3, stem=[Q14A], fig='q14a-scheme',
      decision='The text layer flattens the superscript of the scheme\'s "1st".'),
    T('14avi', 'Q14(a)(vi)', 'C', ask(13, 'Outline the major events of the second stage.'),
      [pt(S('Sugar formed from CO2'), 3), pt(S('ATP provides energy or NADPH provides hydrogen (or H)'), 3)],
      'bio-2-2', 'events-of-the-dark-stage', at(14, '14.', '(a)', '(vi)'), 6, stem=[Q14A], fig='q14a-scheme',
      decision='The two events are priced "3" each.'),
] + [
    # Q14(b): "Metabolism.", "Krebs Cycle." and "ADP." are short, so each card
    # carries (b)'s printed lead-in in its question text.
    T(f'14b{r}', f'Q14(b)({r})', 'C', [Q14B, term(13, word, br=True)],
      [anyn(S(*menu), 3, 4, steps=[4, 3, 3], note_sel=NOTE_14B)], 'bio-2-2', concept, SQ(14, sq), 10,
      decision='"4 + 2(3)": three points from the printed menu, the first at 4 and the next two at 3. The scheme\'s '
               'direction on word diagrams, printed above the three notes, is the row\'s note.')
    for r, word, menu, concept, sq in [
        ('i', 'Metabolism.', ('(The sum of) all reactions in cell (or organism) / controlled by enzymes /',
                              'anabolism explained or anabolism + example'), 'metabolism', 'Metabolism:'),
        ('ii', 'Krebs Cycle.', ('occurs in second stage of respiration / in mitochondria /', 'CO2 produced'),
         'krebs-cycle', 'Krebs Cycle:'),
        ('iii', 'ADP.', ('Adenosine di-phosphate / a low energy (molecule) / + phosphate (P) /', '+ energy / ATP formed'),
         'adp', 'ADP:')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', ask(13, 'Explain the term fermentation.'), [pt(S('Anaerobic respiration'), 3)],
      'bio-2-2', 'fermentation', at(15, '14.', '(c)', '(i)'), 3),
    T('14cii', 'Q14(c)(ii)', 'C', Q14CII, [pt(S('Yeast'), 3)], 'bio-2-2', 'industrial-fermenter',
      at(15, '14.', '(c)', '(ii)'), 3),
    T('14ciii', 'Q14(c)(iii)', 'C', ask(13, 'To which kingdom does this organism belong?'), [pt(S('*Fungi'), 3)],
      'bio-2-2', 'yeast-is-a-fungus', at(15, '14.', '(c)', '(iii)'), 3, stem=[M('(ii)', 13), Q14CII]),
    T('14civ', 'Q14(c)(iv)', 'C', ask(13, 'Name a compound which is used as a carbon source in the fermentation referred '
                                         'to in part (ii).'),
      [pt(S('Any named carbohydrate'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-2', 'carbon-source',
      at(15, '14.', '(c)', '(iv)'), 3, stem=[M('(ii)', 13), Q14CII]),
    T('14cv1', 'Q14(c)(v)1', 'C', item(13, 1, 'Explain the terms bioprocessing and immobilised.', 'sometimes used.'),
      [pt(S('Bioprocessing: using micro-organisms (or enzymes)'), 3),
       pt(S('to form product(s)'), 3, label=S('Bioprocessing: using micro-organisms (or enzymes)', piece=1, psep=': ')),
       pt(S('Immobilised:', 'material)'), 3)], 'bio-2-1', 'bioprocessing-and-immobilisation',
      at(15, '14.', '(c)', '(v)', why=ITEM_ROMAN), 9, stem=[Q14CV],
      decision=EACH_ITEM + ' Bioprocessing\'s two points and immobilised\'s one are priced "3" each; the second '
                           'bioprocessing point carries the scheme\'s own heading.'),
] + [
    T(f'14cv{n}', f'Q14(c)(v){n}', 'C', item(13, n, end, 'sometimes used.'), [pt(S(ans), 3)], 'bio-2-1', concept,
      at(15, '14.', '(c)', '(v)', why=ITEM_ROMAN), 3, stem=[Q14CV], decision=EACH_ITEM)
    for n, end, ans, concept in [
        (2, 'Give an advantage of using immobilised cells.',
         'Can be re-used (or recovered) or pure product (or described)', 'advantage-of-immobilised-cells'),
        (3, 'Name the compound from which the immobilising beads are formed in the laboratory.', 'Alginate',
         'alginate'),
        (4, 'Give the general name for the vessel used for such reactions.', 'Bioreactor', 'bioreactor')]
] + [
    # Q15(a)
    T(f'15a{r}', f'Q15(a)({r})', 'C', q, rows, 'bio-3-1', concept, at(16, '15.', '(a)', f'({r})'), total, stem=Q15A,
      decision=decision)
    for r, q, rows, concept, total, decision in [
        ('i', ask(14, 'Name one bird from the study and name its parasite.'),
         [pt(S('Finch (or sparrow) + (blood sucking) mites'), 3)], 'birds-and-mites', 3,
         ROW_PRICED + ' The bird and its parasite are priced together, "3".'),
        ('ii', ask(14, 'Explain the term ectoparasite.'),
         [pt(s, 3) for s in pieces('(Organism living on) host (or explained) / causing damage')], 'ectoparasite', 6,
         '"2(3)": the two points, cut at the scheme\'s own solidus.'),
        ('iii', ask(14, 'Suggest one negative effect on birds or chicks of living in parasite-infested nests.'),
         [pt(S('Disease or death or weakened (birds)'), 3)], 'effects-of-parasites', 3, ''),
        ('iv', Q(14, 'Apart from an effect on parasite numbers, suggest a reason for the use of the filter fibres in',
                 'nest building.'),
         [pt(S('Readily available or shortage of normal material or similar',
               'to normal building material or suitable material or insulator'), 3)], 'nest-building-material', 3, ''),
        ('v', ask(14, 'State one benefit to a plant of giving off strong smells.'),
         [pt(S('Repulsion (or described) or attraction (or described)'), 3)], 'plant-smells', 3, ''),
        ('vi', ask(14, 'Suggest what might be trapped in used cigarette filters.'),
         [pt(S('Tar or nicotine (or other named substance) or bacteria'), 3)], 'cigarette-filter-contents', 3, ''),
        ('vii', Q(14, 'Suggest how the scientists might have measured the amount of cigarette filter fibre in one',
                  'nest.'),
         [pt(S('By weighing it'), 3)], 'measuring-fibre', 3, ''),
        ('viii', Q(14, 'The scientists put unused cigarette filters beside the birds’ nests.',
                   'Suggest a reason for this.'),
         [pt(S('Control (or explained)'), 3)], 'unused-filters-as-control', 3, ''),
        ('ix', Q(14, 'The nests containing unused filters showed a normal parasite load.',
                 'Suggest one reason for this observation.'),
         [pt(S('No (mite)-repelling (or mite-killing) chemicals or absence of named', 'chemical'), 3)],
         'unused-filters-result', 3, '')]
] + [
    # Q15(b)
    T('15bi', 'Q15(b)(i)', 'C', ask(14, 'Draw a large labelled diagram to illustrate the main features of the nitrogen '
                                       'cycle.'),
      [anyn(None, 6, 2, options=[S(f'• {p}', piece=[2, 1], psep=['• ', ' /']) for p in NITROGEN],
            note_sel=S('Any six'))],
      'bio-3-2', 'nitrogen-cycle', at(16, '15.', '(b)', '(i)'), 12,
      decision='"Any six 6(2)" over eleven bulleted points, each its own printed line: a menu, claim six.'),
    T('15bii', 'Q15(b)(ii)', 'C', ask(14, 'Outline two biological similarities between the nitrogen cycle and the carbon '
                                         'cycle.'),
      [anyn(S('Fixation (or explained) / bacteria (or micro-organisms) involved /',
              'death and decay / nutrition (or described) / excretion'), 2, 2)], 'bio-3-2',
      'nitrogen-and-carbon-cycles', at(16, '15.', '(b)', '(ii)'), 4,
      decision='"2(2)" over five printed points: a menu, claim two.'),
    T('15biii', 'Q15(b)(iii)', 'C', ask(14, 'Suggest why continual monitoring of the environment is valuable.'),
      [pt(S('To be able to detect change(s) or to remedy effect of change',
            'or to detect levels of pollutants (or example)'), 2)], 'bio-3-1', 'environmental-monitoring',
      at(16, '15.', '(b)', '(iii)'), 2),
] + [
    T(f'15biv{n}', f'Q15(b)(iv){n}', 'C', item(14, n, end, 'pair by writing a sentence about each term.'),
      [pt(S(a1), 2, label=S(l1)), pt(S(a2), 2, label=S(l2))], 'bio-3-1', concept,
      at(16, '15.', '(b)', '(iv)', why=ITEM_ROMAN), 4, stem=[Q15BIV],
      decision=EACH_ITEM + ' Each term of the pair is priced "2".')
    for n, end, l1, a1, l2, a2, concept in [
        (1, 'Contest competition and scramble competition.', 'Contest:', 'one gets all (of the resource)',
         'Scramble:', 'all get some (of the resource)', 'contest-and-scramble-competition'),
        (2, 'Edaphic and aquatic.', 'Edaphic:', 'to do with soil', 'Aquatic:', 'to do with water',
         'edaphic-and-aquatic'),
        (3, 'Climate and weather.', 'Climate:', 'long-term (prevailing) conditions', 'Weather:',
         'short-term (atmospheric) conditions', 'climate-and-weather')]
] + [
    # Q15(c)
    T('15ci', 'Q15(c)(i)', 'C', Q(15, 'Copy the graph into your answer book.', 'might vary over the same timespan.'),
      [pt(S('Out of sync.'), 3, kind='criterion', label=S('Graph:')),
       pt(S('Most prey peaks higher than predator peaks'), 3, kind='criterion')], 'bio-3-1', 'predator-prey-graph',
      at(17, '15.', '(c)', '(i)'), 6, stem=[Q15C], fig='q15c-graph',
      decision=ROW_PRICED + ' The graph\'s two features are priced "3" each: two criterion rows.'),
    T('15cii', 'Q15(c)(ii)', 'C', ask(15, 'Give an explanation of the graph that you have drawn for the prey species.'),
      [pt(S('Explanation of time lag'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Explanation of bigger prey numbers'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'explaining-predator-prey-cycles', at(17, '15.', '(c)', '(ii)'), 6, stem=[Q15C], fig='q15c-graph',
      decision='The two explanations are priced "3" each and the scheme prints neither: two criterion rows.'),
    T('15ciii', 'Q15(c)(iii)', 'C', Q(15, 'Do you think that population graphs for a host species and its main parasite '
                                         'would show', 'Explain your answer.'),
      [pt(S('Yes (or No) + explanation'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'host-and-parasite-populations', at(17, '15.', '(c)', '(iii)'), 3, stem=[Q15C], fig='q15c-graph'),
    T('15civ', 'Q15(c)(iv)', 'C', ask(15, 'Suggest a role for parasites in the overall scheme of nature.'),
      [pt(S('Population control'), 3)], 'bio-3-1', 'role-of-parasites', at(17, '15.', '(c)', '(iv)'), 3),
    T('15cv', 'Q15(c)(v)', 'C', [Q(15, '1.', 'Name two predators.', after='overall scheme of nature.'),
                                 Q(15, '2.', 'in the case of each predator.', after='overall scheme of nature.',
                                   br=True)],
      [pt(S('Name predator 1'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Adaptative technique'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Name predator 2'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Adaptative technique', nth=2), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1',
      'predators-and-adaptations', at(17, '15.', '(c)', '(v)'), 12,
      decision='The scheme prices each predator and its technique "3" each, printed as pairs ("Name predator 1", '
               '"Adaptative technique", ...) and none named: one card for both numbered asks, four criterion rows '
               'in the scheme\'s order. "Adaptative" is the scheme\'s spelling, lifted as printed.'),
]

ANSWER_VARIANTS = {
    '9bi1': [
        ('carbon-dioxide', 'Carbon dioxide concentration',
         [pt(S('vary NaHCO3 conc.'), 3, label=S('CO2 –', piece=1, psep=' –'))]),
        ('light', 'Light intensity',
         [pt(S('vary lamp (or plant) distance or vary lamp wattage'), 3, label=S('Light –', piece=1, psep=' –'))]),
    ],
    '11aii': [
        ('fossils', 'Fossils',
         [anyn(S('e.g. Fossils: structure / changing / over time / related to environment', piece=2, psep=': '), 2, 3,
               open_list=True, note_sel=S('e.g. Fossils: structure / changing / over time / related to environment',
                                          piece=1, psep=': '))]),
        ('embryology', 'Embryology',
         [anyn(S('e.g. Embryology: different organisms / similar embryo /', 'similar development pathways', piece=2,
                 psep=': '), 2, 3, open_list=True,
               note_sel=S('e.g. Embryology: different organisms / similar embryo /', 'similar development pathways',
                          piece=1, psep=': '))]),
        ('anatomy', 'Anatomy',
         [anyn(S('e.g. Anatomy: Named structure / expansion point', piece=2, psep=': '), 2, 3, open_list=True,
               note_sel=S('e.g. Anatomy: Named structure / expansion point', piece=1, psep=': '))]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-graph': ('paper', 3, (70, 91, 516, 398), SEC, ['X', 'Y'],
        'Line graph on a grid: Body temperature (°C), 10 to 40, up the vertical axis against Environmental '
        'temperature (°C), 10 to 40, along the horizontal axis. Line X runs almost flat, from about 38 °C '
        'body temperature at the left to about 40 °C at the right. Line Y is a straight line rising steeply '
        'from about 8 °C body temperature at an environmental temperature of about 6 °C to about 37 °C at '
        'an environmental temperature of about 41 °C.',
        False),
    'q4-strawberry': ('paper', 4, (65, 55, 520, 327), SEC, [],
        'Line drawing of strawberry plants on sloping, hatched ground. On the right, a larger plant '
        'bracketed and labelled parent plant has toothed leaves, a flower, three strawberries and a tuft of '
        'roots. A long thin stem labelled runner arches from its base along the ground to a small plant on '
        'the left, bracketed and labelled daughter plant, which has a few leaves and small roots of its '
        'own.',
        False),
    'q11bii-scheme': ('scheme', 11, (140, 265, 330, 350), SEC, [],
        "The marking scheme's drawing: under the word Female, the letters XX over two long vertical bars of "
        'equal length side by side; under the word Male, the letters XY over one long vertical bar with a '
        'much shorter bar beside it.',
        True),
    'q11biii-scheme': ('scheme', 11, (138, 356, 248, 422), SEC, [],
        "The marking scheme's Punnett square, a grid of three rows and two columns: the top row an empty "
        'cell then X, the second row X then XX, the third row Y then XY.',
        True),
    'q13ai-question': ('paper', 12, (90, 38, 545, 82), SEC, [],
        'Part (i) of Question 13(a) as printed: three lines of the question, in which the phrase from '
        'physical changes to reproduction is set in italics.',
        False),
    'q13b-system': ('paper', 12, (148, 181, 406, 370), SEC, ['A', 'B', 'C', 'D', 'E', 'F'],
        'Shaded diagram of a reproductive system seen from the front: a central chamber with thick walls, a '
        'curved band running out from its top to each side and bending down over a round shape on each '
        'side, and a narrow passage leading down from the bottom of the chamber. Label D points to the '
        "curved band near its right end; C to the inner edge of the chamber's right wall; B to the thick "
        'shaded wall on the right of the chamber; E to the round shape on the left; F to the ring where the '
        'chamber narrows at the bottom; A to the narrow passage at the bottom.',
        False),
    'q14a-scheme': ('paper', 13, (50, 90, 540, 156), SEC, [],
        "The paper's summary on one line: PHOTOSYNTHESIS:, then FIRST STAGE followed by a curly bracket "
        'enclosing PATHWAY I above PATHWAY II, then an arrow pointing right to SECOND STAGE.',
        False),
    'q15c-graph': ('paper', 15, (104, 76, 518, 325), SEC, [],
        'Graph on a grid: Number of predators and prey up the vertical axis and Years along the horizontal '
        'axis, each with an arrow and no scale. One thick line, labelled predator, rises and falls in a '
        'regular wave of flat-topped peaks and flat-bottomed troughs, three troughs in all, starting and '
        'ending at peak height. No other line is drawn.',
        False),
}
