"""Biology 2012 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2012 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p13
    Section C Questions 10-15, p14-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q3, Q5, Q12(a) and Q15(a) drawings and the Q12(b) graph carry no
    credit. Questions 10-13 print their part totals "(9)", "(27)", "(24)";
    Q14 and Q15 print "(30, 30)".
  * The marking scheme, 20 pages: p1 cover, p2 blank (no text layer), p3
    introduction, cancelled answers and surplus answers, p4 surplus answers
    (continued) and conventions, p5-p17 Questions 1-15, p18 and p19 blank (no
    text layer), p20 back cover (no text layer). Its p5 text layer reads Q2 and
    Q3 before Section A's heading and Q1, though the page prints Q1 first.

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c).

This scheme prints no reprint of any question, only a few label words
("Pollutant:", "Chain:", "Segregation:", "CNS:", "Cerebrum:", "diffusion:"):
each answer stands under its own question number, letter and roman. A task is
anchored on its own part marker, found by walking the scheme's numbering down
to it (SQ path); Q1 is walked to through "Section A", since Q2(b)(ii)'s items
print the "1." the walk would otherwise stop on. Where the marker opens its
answer's own line ("(iii) 1. Animal example.") it is a welded bare anchor. A
numbered item ("1.", "2.") is anchored on the roman it is printed under.

Tariffs. Section A is ordered splits, carded at their first rate: Q1 "2(7) +
3(2) i.e. best FIVE answers from (a) – (f)" (six parts, the best five
priced), Q2 and Q5 "8 + 7 + 5(1)" (seven responses each), Q3, Q4 and Q6 "2(7)
+ 6(1)" (eight responses each). Sections B and C print a mark against every
row ("3", "2(3)", "6(2)", "3(3)", a drawing's "6, 3, 0", Q11(b)(v)'s "6, 0"),
so every Section B and C task is priced row by row against the paper's
Section B rubric "Part (a) carries 6 marks and part (b) carries 24 marks",
Section C's (9), (27), (24) and Q14/Q15's (30, 30).

Every printed answer fits a per-response tariff, so no part is carded whole.

Alternatives the scheme prints as matched sets are answer variants of one
task: Q11(b)(v) items 2 and 3 ("Yes, because ..." OR "No, because ...", one
item "2+3." priced "6, 0"), and Q13(c)(iii)'s cause and treatment for
Parkinson's disease OR paralysis.

Brought to the coordinator: Q9(b)(vii) item 2 ("drawing a graph to show how the
rate of enzyme action varied with temperature", priced "3") is answered in the
scheme (p9) only by a drawn curve, an image with no words at all, so no row can
be lifted for it; item 1 is carded and item 2 is left out of TASKS.

The census reader finds all 127 printed asks; no paper.py entry was needed
for this sitting.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, G  # noqa: F401

YEAR, LEVEL = 2012, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2012-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': '382e74c07982e0622627abb59eceea4d18a5fda5dd27d0dd8f8c7b73b670251a',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2012-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'eb0b3fc9779e41418057f2878f1fe452ed39a28248dc623d67a68d546799ae98',
               'pages': 20},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 14)}, **{p: 'blank' for p in range(14, 17)}},
    'scheme': {1: 'cover', 2: 'blank', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 18)}, 18: 'blank', 19: 'blank', 20: 'back-cover'},
}


def _ladder(notation, **extra):
    steps = []
    for term_ in notation.split('+'):
        n, _, m = term_.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only parts priced row by row: a ladder question's cards are carded at the
# ladder's first rate, so their sum is not the printed total.
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p5: "Part (a) carries 6 marks
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # and part (b) carries 24 marks"
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
    **{(n, 'b'): 27 for n in (10, 11, 12, 13)},   # "(27)"
    **{(n, 'c'): 24 for n in (10, 11, 12, 13)},   # "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
LADDERS = {
    # Q1: six parts, the best five priced "2(7) + 3(2)".
    1: _ladder('2(7) + 3(2)', responses=6),
    2: _ladder('8 + 7 + 5(1)'), 5: _ladder('8 + 7 + 5(1)'),
    3: _ladder('2(7) + 6(1)'), 4: _ladder('2(7) + 6(1)'), 6: _ladder('2(7) + 6(1)'),
}

CHECKSUMS = {
    1: {7: 6}, 2: {8: 7}, 3: {7: 8}, 4: {7: 8}, 5: {8: 7}, 6: {7: 8},
    (7, 'a'): {3: 2}, (7, 'b'): {3: 8},
    (8, 'a'): {3: 2}, (8, 'b'): {3: 8},
    (9, 'a'): {3: 2}, (9, 'b'): {3: 8},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 9}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 7, 6: 1}, (11, 'c'): {2: 12},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 9}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 3}, (13, 'b'): {6: 1, 1: 6, 3: 5}, (13, 'c'): {3: 8},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 6, 6: 1, 2: 3},
    (15, 'a'): {3: 10}, (15, 'b'): {3: 10}, (15, 'c'): {3: 10},
}

SCAN_PAGES = {'paper': range(1, 14)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 "Answer five of the following": best five of (a)-(f); each part is its own card '
                                  'on the "2(7) + 3(2)" ladder.'),
    ('paper', 3, 'or', 'Q4(b)(ii) "domestic, agricultural or industrial sources": the candidate selects one; marked on '
                       'the same rows.'),
    ('paper', 5, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 5, 'the following', 'Q7(a) "explain each of the following": every term asked, one card each.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 5, 'or', 'Q7(b)(i) "the sheep\'s or ox\'s heart": description.'),
    ('paper', 6, 'or', 'Q8(a)(i) "prokaryotic or eukaryotic": the answer options.'),
    ('paper', 6, 'or', 'Q8(b)(i) "fungi or bacteria": description.'),
    ('paper', 7, 'the following', 'Q9(a) lead-in: every part asked.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 8, 'both', 'Q10(a)(ii) "Give both of the specific base pairs": both asked, one priced item.'),
    ('paper', 8, 'or', 'Q10(c)(ii) "all or some of the following procedures": description.'),
    ('paper', 8, 'the following', 'Q10(c)(ii): every term asked, one row each.'),
    ('paper', 8, 'any two', 'Q10(c)(iii) "in any two of the following": a bounded menu of three categories, claim two.'),
    ('paper', 8, 'the following', 'Q10(c)(iii), same lead-in.'),
    ('paper', 9, 'both', 'Q11(c)(iv) "both natural and artificial": one of each asked, one row each.'),
    ('paper', 10, 'the following', 'Q12(a)(i) "From the following list": the answer options.'),
    ('paper', 10, 'or', 'Q12(b)(iv) "glasshouses or tunnels": description.'),
    ('paper', 10, 'the following', 'Q12(c) "a brief note on each of the following items": every item asked, one card '
                                   'each.'),
    ('paper', 11, 'any two', 'Q13(b)(ii) "any two parts found only in neurons": two asked, one row each.'),
    ('paper', 11, 'or', 'Q13(b)(iii) "on or near your diagram": description.'),
    ('paper', 11, 'any two', 'Q13(b)(iv) "any two types of neuron": two asked, one row each.'),
    ('paper', 11, 'the following', 'Q13(c)(i) "each of the following parts": every part asked, one row each.'),
    ('paper', 11, 'either', 'Q13(c)(iii) "either paralysis or Parkinson\'s disease": either disorder; the scheme\'s '
                            'answers for each are answer variants of one task.'),
    ('paper', 11, 'or', 'Q13(c)(iii), same choice.'),
    ('paper', 12, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'the following', 'Q14(a)(i) "each of the following": one card per numbered item.'),
    ('paper', 12, 'any one', 'Q14(a)(iv) "Name any one of these structures": one asked; alternatives on one row.'),
    ('paper', 12, 'the following', 'Q14(b) lead-in: every part asked.'),
    ('paper', 12, 'the following', 'Q14(c)(i) lead-in: every item asked.'),
    ('paper', 12, 'the following', 'Q14(c)(ii) lead-in: every item asked.'),
    ('paper', 13, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 13, 'the following', 'Q15(a)(iii) "which of the following": the answer options.'),
    ('paper', 13, 'any three', 'Q15(b)(iii)2 "Name any three types of T cell": a bounded menu, claim three.'),
    ('paper', 13, 'or', 'Q15(c)(ii) "tissues, or between itself and the external environment": description.'),
    ('paper', 13, 'the following', 'Q15(c)(iii) "each of the following": one card per numbered item.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
ITEM_ROMAN = 'The scheme prints no reprint: a numbered item is anchored on the roman it is printed under.'
WELDED = ('The scheme prints no reprint and sets this part\'s marker on its answer\'s own line: anchored on that '
          'marker.')
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
ROW_PRICED = 'Sections B and C print a mark against every row.'


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def term(page, word, br=False):
    """A printed term the paper sets before its answer line ("Data. ____")."""
    return Q(page, word, word, br=br)


def item(page, n, end, anchor, br=True):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, after=anchor, br=br)


def at(page, *path_and_marker, nth=1, why=NO_REPRINT):
    """The part's own marker, walked down to through the scheme's numbering."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth)


def welded(page, *path_and_marker, nth=1, why=WELDED):
    """The part's marker opening its own answer line: a welded bare anchor."""
    *path, marker = path_and_marker
    return SQ(page, marker, path=path, paired=why, bare=True, nth=nth, welded=True)


def pieces(sel_start, sel_end=None, n=2, **kw):
    """Each answer of a printed solidus list, in order: one selector per entry."""
    return [dict(S(sel_start, sel_end, piece=i, **kw)) for i in range(1, n + 1)]


def eg_menu(line, n, per, page=None):
    """A criterion the scheme follows with "e.g." and comma-separated examples
    ("Example of animal tissue e.g. muscle, connective, ..."): the examples are
    an open menu, the criterion its note."""
    return anyn(None, 1, per, open_list=True,
                options=[S(line, page=page, piece=[2, i], psep=[' e.g. ', ', ']) for i in range(1, n + 1)],
                note_sel=S(line, page=page, piece=1, psep=' e.g. '))


def ladder(q, notation):
    return f'The scheme prints Q{q} as "{notation}": an ordered split, each response carded at its first rate.'


def crit(sel, marks, **kw):
    """A row the scheme prices without printing an answer."""
    return pt(sel, marks, kind='criterion', note=NO_ANSWER, **kw)


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Answer five of the following:')
Q1A = ask(2, 'Name a monosaccharide.')
Q2AII = ask(2, 'Give an example of an animal tissue.')
Q3A = ask(3, 'The diagram shows the macroscopic structure of part of a long bone.')
Q3BI = ask(3, 'Show clearly on the diagram where you would expect to find cartilage.')
Q4BII = Q(3, 'Pollution may result from domestic, agricultural or industrial sources.',
          'produced by a named pollutant.')
Q4C = ask(3, 'In relation to the incineration of domestic waste, suggest:')
Q5 = ask(4, 'The diagram shows a transverse section through the stem of a monocotyledonous (monocot) plant.')
Q5D = ask(4, 'How do you know from the diagram that the section is taken from:')
Q7A = ask(5, 'In relation to the scientific method, explain each of the following:')
Q7B = Q(5, 'Answer the following by reference to some of the investigations that you carried out in the course of',
        'your studies.')
Q7BIII = ask(5, 'What type of agar plates did you use when investigating the digestive activity of seeds?')
Q8BIII = ask(6, 'Describe how you introduced the leaf yeasts into agar plates.')
Q9A = ask(7, 'Answer the following in relation to enzymes.')
Q9B = Q(7, 'Answer the following in relation to an investigation that you carried out into the effect of',
        'temperature on the rate of enzyme action.')
Q9BI = ask(7, 'Name the enzyme that you used.')
Q10AI = Q(8, 'Nucleic acids are composed of subunits called nucleotides.', 'a phosphate group and a nitrogenous base.')
Q10B = Q(8, 'In the sweet pea plant the texture and colour of the testa (seed coat) are governed by two pairs of',
         'the allele for yellow (Y) is dominant to the allele for green (y).')
Q10BII = Q(8, 'Using the above symbols, and taking particular care to differentiate between upper case and',
           'lower case letters:')
Q10BII1 = item(8, 1, 'heterozygous in respect of seed colour.', 'lower case letters:')
Q11B = Q(9, 'Organisms that are introduced into new environments outside their natural ranges are referred to as',
         'attempted introductions have been unsuccessful.')
Q11BIV = Q(9, 'Use the knowledge that you have gained in your studies of ecology to suggest how the',
           'introduction of an exotic species may:')
Q11BV = Q(9, 'It has been stated that an exotic species has a good chance of becoming established in a new',
          'environment if there is a vacant niche.')
Q11C = ask(9, 'Name the ecosystem which you investigated during your study of ecology.')
Q12B = Q(10, 'Chlorophyll is composed of various pigments.', 'and chlorophyll b.', end_nth=2)
Q12C = ask(10, 'Write a brief note on each of the following items in relation to respiration.')
Q13BI = ask(11, 'Draw a large labelled diagram of a motor neuron.')
Q14AI = ask(12, 'Give a brief account of the role of each of the following in flowering plant reproduction.')
Q14AIII = ask(12, 'Within the pollen tube the generative nucleus divides to form two male gametes.')
Q14B = ask(12, 'Answer the following questions from your knowledge of early human development in the womb.')
Q14BI1 = item(12, 1, 'Name the three germ layers in the early human embryo.', 'development in the womb.')
Q14BIII1 = item(12, 1, 'What is the amnion?', 'From which tissues does the placenta develop?')
Q14CI = ask(12, 'Answer the following questions in relation to sexual reproduction in the mould Rhizopus.')
Q14CII = ask(12, 'Answer the following questions in relation to asexual reproduction in yeast.')
Q15A = ask(13, 'The diagram shows part of a transverse section through the small intestine.')
Q15BIII = Q(13, 'Lymphocytes may be divided into B cells and T cells.', 'B cells produce antibodies.')
Q15BIII2 = item(13, 2, 'Name any three types of T cell.', 'B cells produce antibodies.')
Q15CIII = ask(13, 'State one way in which each of the following contributes to homeostasis.')

# Q3(a)(ii)'s three parts, printed on one scheme line (p5), cut at its own
# semicolons; each letter's meaning is what follows its " = ".
BONE = 'X = spongy bone or marrow; Y = medullary cavity or marrow; Z = compact bone'
BONE_KEY = [L(x, S(BONE, page=5, piece=[i, 2], psep=['; ', ' = ']), True) for i, x in enumerate('XYZ', 1)]
STEM_A = [L('A', S('Vascular bundles', page=6), True)]
ORGANELLES = [L('A', S('(A =) *mitochondrion', page=12, piece=2, psep=') '), True),
              L('B', S('(B =) *chloroplast', page=12, piece=2, psep=') '), True)]
VILLUS = [L('X', S('(X =) *Villus', page=16, piece=2, psep=') '), True),
          L('Y', S('(Y =) *Lacteal', page=16, piece=2, psep=') '), True)]
TISSUE_EG = 'Example of animal tissue e.g. muscle, connective, epithelial, nervous'
BONE_EG = 'Name of long bone e.g. femur, tibia, fibula, humerus, radius, ulna'
SKIN_HOT = 'Too hot: Sweat / dilation of blood vessels / hair flat'
SKIN_COLD = ('Too cold: Constriction of of blood vessels / hair stands up/ insulation by', '(subcutaneous) fat')

TASKS = [
    # ------------------------------------------------------------ Section A --
    T(f'1{x}', f'Q1({x})', 'A', q, [pt(S(ans), 7)], 'bio-1-2', concept, at(5, 'Section A', '1.', f'({x})'), 7,
      stem=stem, decision=ladder(1, '2(7) + 3(2) i.e. best FIVE answers from (a) – (f)') + ' Six parts, the best '
      'five priced.' + extra)
    for x, q, ans, concept, stem, extra in [
        ('a', Q1A, 'Name of monosaccharide e.g. Glucose', 'monosaccharide', [Q1], ''),
        ('b', ask(2, 'Give the formula of the monosaccharide referred to in (a).'),
         'Formula of monosaccharide from (a) e.g. C6H12O6 for glucose', 'glucose-formula', [Q1, M('(a)', 2), Q1A],
         ' The text layer flattens the subscripts of C6H12O6.'),
        ('c', ask(2, 'Name a polysaccharide that can be formed from the monosaccharide referred to in (a).'),
         'Polysaccharide from (a) e.g. starch (from glucose)', 'polysaccharide', [Q1, M('(a)', 2), Q1A], ''),
        ('d', Q(2, 'Give one way in which an amino acid differs from a monosaccharide, in terms of chemical',
                'composition.'),
         'Contains N or contains –NH2 or contains –COOH (group)', 'amino-acid-composition', [Q1],
         ' The text layer flattens the subscript of –NH2.'),
        ('e', ask(2, 'What do carbohydrates and fats have in common, in terms of chemical composition?'),
         '(mostly) composed of C, H and O', 'elements-in-carbohydrates-and-fats', [Q1], ''),
        ('f', ask(2, 'How may one fat differ from another, in terms of chemical composition?'),
         'Different (fatty) acids or some are phosphorylated (or have phosphate)', 'fats-differ', [Q1], '')]
] + [
    T('2ai', 'Q2(a)(i)', 'A', ask(2, 'What is a tissue?'), [pt(S('A group of cells with the same function'), 8)],
      'bio-1-3', 'tissue', at(5, '2.', '(a)', '(i)'), 8, decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('2aii', 'Q2(a)(ii)', 'A', Q2AII, [eg_menu(TISSUE_EG, 4, 8)], 'bio-1-3', 'animal-tissues',
      at(5, '2.', '(a)', '(ii)'), 8,
      decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses. The scheme prints "Example of animal tissue" and four '
               'examples after "e.g.", cut at its commas: an open menu, claim one.'),
    T('2aiii', 'Q2(a)(iii)', 'A', ask(2, 'State a role of the animal tissue referred to in (ii).'),
      [crit(S('Matching structural or physiological role of given animal tissue'), 8)], 'bio-1-3',
      'role-of-animal-tissue', at(5, '2.', '(a)', '(iii)'), 8, stem=[M('(ii)', 2), Q2AII],
      decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('2aiv', 'Q2(a)(iv)', 'A', ask(2, 'Give one way in which the tissue referred to in (ii) is adapted to carry out its '
                                       'function(s).'),
      [crit(S('Matching structural or matching physiological adaptation of given animal tissue'), 8)], 'bio-1-3',
      'tissue-adaptation', at(5, '2.', '(a)', '(iv)'), 8, stem=[M('(ii)', 2), Q2AII],
      decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('2bi', 'Q2(b)(i)', 'A', ask(2, 'Explain the term tissue culture.'),
      [pt(S('Cells grown on (or in) medium or cells grown outside organism'), 8)], 'bio-1-3', 'tissue-culture',
      at(5, '2.', '(b)', '(i)'), 8, decision=ladder(2, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('2bii', 'Q2(b)(ii)', 'A', ask(2, 'Give two examples of the use of tissue culture.'),
      [crit(S('First example'), 8), crit(S('Second example'), 8)], 'bio-1-3', 'uses-of-tissue-culture',
      at(5, '2.', '(b)', '(ii)'), 16,
      decision='The two examples, numbered 1. and 2. by the scheme, are two responses on the "8 + 7 + 5(1)" ladder; '
               'the scheme names neither.'),
] + [
    T(f'3{k}', ref, 'A', q, rows, 'bio-2-4', concept, at(5, '3.', *path), total, stem=stem, fig='q3-bone',
      labels=labels, decision=ladder(3, '2(7) + 6(1)') + ' Eight responses.' + extra)
    for k, ref, q, rows, concept, path, total, stem, labels, extra in [
        ('ai', 'Q3(a)(i)', ask(3, 'Name a long bone in the human body.'), [eg_menu(BONE_EG, 6, 7)], 'long-bones',
         ('(a)', '(i)'), 7, [Q3A], None,
         ' The scheme prints "Name of long bone" and six examples after "e.g.", cut at its commas: an open menu, '
         'claim one.'),
        ('aii', 'Q3(a)(ii)', ask(3, 'Name parts X, Y and Z in the diagram.'),
         [pt(S(BONE, piece=i, psep='; '), 7) for i in (1, 2, 3)], 'parts-of-a-long-bone', ('(a)', '(ii)'), 21, [Q3A],
         BONE_KEY, ' X, Y and Z are three responses, cut at the scheme\'s own semicolons.'),
        ('aiii', 'Q3(a)(iii)', ask(3, 'State a function of X.'),
         [pt(S('X: Strength (or rigidity) or lowers density', 'marrow'), 7)], 'spongy-bone', ('(a)', '(iii)'), 7,
         [Q3A], None, ''),
        ('aiv', 'Q3(a)(iv)', ask(3, 'State a function of Y.'),
         [pt(S('Y: Makes (yellow) marrow or stores fat or makes blood cells (or named)'), 7)], 'medullary-cavity',
         ('(a)', '(iv)'), 7, [Q3A], None, ''),
        ('bi', 'Q3(b)(i)', Q3BI, [crit(S('Indication of cartilage on diagram'), 7)], 'cartilage-in-bone',
         ('(b)', '(i)'), 7, [Q3A], None, ''),
        ('bii', 'Q3(b)(ii)', ask(3, 'State one role of this cartilage.'),
         [pt(S('Prevents bone damage or friction free movement or shock absorption'), 7)], 'role-of-cartilage',
         ('(b)', '(ii)'), 7, [Q3A, M('(i)', 3), Q3BI], None, '')]
] + [
    T('4ai', 'Q4(a)(i)', 'A', ask(3, 'What does an ecologist mean by the term conservation?'),
      [pt(S('Management of environment or management of species (or organism(s))'), 7)], 'bio-3-1', 'conservation',
      at(6, '4.', '(a)', '(i)'), 7, decision=ladder(4, '2(7) + 6(1)') + ' Eight responses.'),
    T('4aii', 'Q4(a)(ii)', 'A', ask(3, 'Suggest a reason why nature reserves are important for conservation.'),
      [pt(S('To allow species to develop or (maintaining) biodiversity', 'or prevent extinction or protection'), 7)],
      'bio-3-1', 'nature-reserves', at(6, '4.', '(a)', '(ii)'), 7,
      decision=ladder(4, '2(7) + 6(1)') + ' Eight responses.'),
    T('4bi', 'Q4(b)(i)', 'A', ask(3, 'Explain the term pollution.'),
      [pt(S('Harmful addition to the environment (or named part of environment)'), 7)], 'bio-3-1', 'pollution',
      at(6, '4.', '(b)', '(i)'), 7, decision=ladder(4, '2(7) + 6(1)') + ' Eight responses.'),
    T('4bii', 'Q4(b)(ii)', 'A', Q4BII,
      [crit(S('Any relevant pollutant'), 7, label=S('Pollutant:')),
       crit(S('Must match pollutant'), 7, label=S('Effect:'))], 'bio-3-1', 'pollutant-and-effect',
      at(6, '4.', '(b)', '(ii)'), 14,
      decision='The pollutant and its effect, on the paper\'s two answer lines ("Pollutant:", "Effect:"), are two '
               'responses on the "2(7) + 6(1)" ladder; the scheme names neither.'),
    T('4biii', 'Q4(b)(iii)', 'A', ask(3, 'How may the pollution referred to in (ii) be controlled?'),
      [crit(S('Matching control measure for pollutant from (ii)'), 7)], 'bio-3-1', 'pollution-control',
      at(6, '4.', '(b)', '(iii)'), 7, stem=[M('(ii)', 3), Q4BII],
      decision=ladder(4, '2(7) + 6(1)') + ' Eight responses.'),
    T('4ci', 'Q4(c)(i)', 'A', [Q4C, M('(i)', 3, br=True), ask(3, 'an advantage of the process.')],
      [pt(S('Amount of waste greatly reduced or useable heat', 'or reduced landfill'), 7)], 'bio-3-1',
      'incineration-advantage', at(6, '4.', '(c)', '(i)'), 7,
      decision=ladder(4, '2(7) + 6(1)') + ' Eight responses. The ask completes (c)\'s printed lead-in, carried in the '
               'question text.'),
    T('4cii', 'Q4(c)(ii)', 'A', [Q4C, M('(ii)', 3, br=True), ask(3, 'a disadvantage of the process.')],
      [pt(S('Harmful products'), 7)], 'bio-3-1', 'incineration-disadvantage', at(6, '4.', '(c)', '(ii)'), 7,
      decision=ladder(4, '2(7) + 6(1)') + ' Eight responses. The ask completes (c)\'s printed lead-in, carried in the '
               'question text.'),
    T('5a', 'Q5(a)', 'A', ask(4, 'What is meant by the term monocotyledonous?'),
      [pt(S('One seed leaf or one embryonic leaf'), 8)], 'bio-2-6', 'monocotyledon', at(6, '5.', '(a)'), 8,
      decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('5b', 'Q5(b)', 'A', ask(4, 'Give an example of a monocotyledonous plant.'), [crit(S('Example of monocot'), 8)],
      'bio-2-6', 'monocot-example', at(6, '5.', '(b)'), 8, decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('5c', 'Q5(c)', 'A', ask(4, 'Name the structures labelled A.'), [pt(S('Vascular bundles'), 8)], 'bio-2-6',
      'vascular-bundles', at(6, '5.', '(c)'), 8, stem=[Q5], fig='q5-stem', labels=STEM_A,
      decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses.'),
] + [
    T(f'5d{r}', f'Q5(d)({r})', 'A', [Q5D, M(f'({r})', 4, br=True), term(4, word)], [pt(S(ans), 8)], 'bio-2-6',
      concept, at(6, '5.', '(d)', f'({r})'), 8, stem=[Q5], fig='q5-stem',
      decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses. "' + word + '" alone is below the build\'s floor for a '
               'question, so the card carries (d)\'s printed lead-in in its question text.')
    for r, word, ans, concept in [('i', 'a stem?', 'More than one (vascular) bundle', 'stem-section'),
                                  ('ii', 'a monocot?', 'Bundles scattered or described', 'monocot-stem')]
] + [
    T('5e', 'Q5(e)', 'A', ask(4, 'How are the veins arranged in the leaves of monocots?'),
      [pt(S('Parallel or described'), 8)], 'bio-2-6', 'parallel-venation', at(6, '5.', '(e)'), 8,
      decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('5f', 'Q5(f)', 'A', ask(4, 'How does the vein arrangement in the leaves of dicot plants differ from that in '
                                 'monocots?'),
      [pt(S('Reticulate or net or branched or described'), 8)], 'bio-2-6', 'net-venation', at(6, '5.', '(f)'), 8,
      decision=ladder(5, '8 + 7 + 5(1)') + ' Seven responses.'),
    T('6a', 'Q6(a)', 'A', ask(4, 'In genetics, what is meant by the term variation?'),
      [pt(S('Differences (within a population or within a species or between individuals)'), 7)], 'bio-1-5',
      'variation', at(7, '6.', '(a)'), 7, decision=ladder(6, '2(7) + 6(1)') + ' Eight responses.'),
    T('6b', 'Q6(b)', 'A', Q(4, 'Variation can result from mutation.', 'Name one other cause of variation.'),
      [pt(S('Sexual reproduction or meiosis or independent assortment or environmental'), 7)], 'bio-1-5',
      'causes-of-variation', at(7, '6.', '(b)'), 7, decision=ladder(6, '2(7) + 6(1)') + ' Eight responses.'),
    T('6c', 'Q6(c)', 'A', ask(4, 'Name two types of mutation.'),
      [pt(S('Gene (mutation)'), 7), pt(S('Chromosome (mutation)'), 7)], 'bio-2-3', 'types-of-mutation',
      at(7, '6.', '(c)'), 14,
      decision='The two types, (i) and (ii) in the scheme, are two responses on the "2(7) + 6(1)" ladder.'),
    T('6d', 'Q6(d)', 'A', ask(4, 'Name two agents responsible for increased rates of mutation.'),
      [crit(S('Example 1'), 7), crit(S('Example 2'), 7)], 'bio-2-3', 'mutagens', at(7, '6.', '(d)'), 14,
      decision='The two agents, (i) and (ii) in the scheme, are two responses on the "2(7) + 6(1)" ladder; the '
               'scheme names neither.'),
    T('6e', 'Q6(e)', 'A', ask(4, 'Briefly explain the significance of mutation in relation to natural selection.'),
      [pt(s, 7) for s in pieces('New phenotypes or new types or new features /',
                                'or less well adapted (or disadvantageous)')], 'bio-1-5', 'mutation-and-natural-selection',
      at(7, '6.', '(e)'), 14,
      decision='Two points, cut at the scheme\'s own solidus: two responses on the "2(7) + 6(1)" ladder.'),
    # ------------------------------------------------------------ Section B --
] + [
    T(f'7a{r}', f'Q7(a)({r})', 'B', [Q7A, term(5, word, br=True)] if len(word) < 8 else term(5, word),
      [pt(S(ans), 3)], 'bio-u2', concept, at(8, '7.', '(a)', f'({r})'), 3, stem=[] if len(word) < 8 else [Q7A],
      decision=ROW_PRICED + (' "' + word + '" alone is below the build\'s floor for a question, so the card carries '
                             '(a)\'s printed lead-in in its question text.' if len(word) < 8 else ''))
    for r, word, ans, concept in [('i', 'Data.', 'Observations or results or other', 'data'),
                                  ('ii', 'Replicates.', 'Repeats (or copies) of experiment', 'replicates')]
] + [
    T(f'7b{r}', f'Q7(b)({r})', 'B', q, rows, topic, concept, at(8, '7.', '(b)', f'({r})'), 3, stem=[Q7B] + extra)
    for r, q, rows, topic, concept, extra in [
        ('i', ask(5, 'How did you expose the semi-lunar valves when dissecting the sheep’s or ox’s heart?'),
         [pt(S('Cut (open) the aorta or cut (open) the pulmonary artery'), 3)], 'bio-2-6', 'exposing-semilunar-valves',
         []),
        ('ii', Q(5, 'How did you show that alcohol was present when investigating the production of alcohol by',
                 'yeast?'),
         [crit(S('Named chemicals or named test'), 3)], 'bio-2-2', 'testing-for-alcohol', []),
        ('iii', Q7BIII, [pt(S('Milk or starch'), 3)], 'bio-2-5', 'starch-agar', []),
        ('iv', Q(5, 'How did you demonstrate that digestive activity had taken place in the investigation referred',
                 'to in part (iii)?'),
         [pt(S('Does not give a positive result where digestive activity occurred or described'), 3)], 'bio-2-5',
         'evidence-of-digestion', [M('(iii)', 5), Q7BIII]),
        ('v', Q(5, 'How did you demonstrate the requirement for oxygen when investigating the factors',
                'necessary for seed germination?'),
         [pt(S('Anaerobic jar (or described) or boiled water + oil', 'or one with O2 and one without O2 (and compare)'),
             3)], 'bio-2-5', 'oxygen-for-germination', []),
        ('vi', Q(5, 'What did you use as the selectively permeable membrane in your investigation of', 'osmosis?'),
         [pt(S('Visking tubing or named plant tissue'), 3)], 'bio-2-6', 'visking-tubing', []),
        ('vii', ask(5, 'What growth regulator did you use when investigating plant growth?'), [pt(S('IAA'), 3)],
         'bio-2-4', 'iaa', []),
        ('viii', Q(5, 'A microscope has an eyepiece lens marked ×10 and an objective lens marked ×20.',
                   'What is the total magnification of the image?'),
         [pt(S('*200'), 3)], 'bio-1-3', 'total-magnification', [])]
] + [
    T('8ai', 'Q8(a)(i)', 'B', ask(6, 'Are fungi prokaryotic or eukaryotic?'), [pt(S('*Eukaryotic'), 3)], 'bio-3-2',
      'fungi-are-eukaryotic', at(8, '8.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('8aii', 'Q8(a)(ii)', 'B', ask(6, 'Name one structure in plant cells not found in fungi.'),
      [pt(S('Chloroplast'), 3)], 'bio-3-2', 'plant-cells-and-fungi', at(8, '8.', '(a)', '(ii)'), 3),
    T('8bi', 'Q8(b)(i)', 'B', ask(6, 'What is the purpose of using agar when growing fungi or bacteria in the laboratory?'),
      [pt(S('(Source of) nutrients or substrate (for growth) or medium or visibility'), 3)], 'bio-3-2', 'agar',
      at(8, '8.', '(b)', '(i)'), 3),
    T('8bii', 'Q8(b)(ii)', 'B', ask(6, 'Suggest one reason why leaf yeasts are more plentiful in July than in March.'),
      [pt(S('More leaves or more suitable temperature or more reproduction'), 3)], 'bio-3-2', 'leaf-yeast-numbers',
      at(8, '8.', '(b)', '(ii)'), 3),
    T('8biii', 'Q8(b)(iii)', 'B', Q8BIII,
      [crit(S('Description of an aseptic technique in transfer (of leaf) or method of',
              'attachment of leaf to lid'), 3)], 'bio-3-2', 'introducing-leaf-yeast', at(8, '8.', '(b)', '(iii)'), 3),
    T('8biv', 'Q8(b)(iv)', 'B', ask(6, 'What was the precise purpose of a control in this investigation?'),
      [pt(S('To show that the yeast came from the leaf (or did not come from agar)'), 3)], 'bio-3-2',
      'leaf-yeast-control', at(8, '8.', '(b)', '(iv)'), 3, stem=[M('(iii)', 6), Q8BIII]),
    T('8bv', 'Q8(b)(v)', 'B', ask(6, 'How did you recognise the leaf yeasts when they appeared on the agar?'),
      [pt(S('Pink (colonies)'), 3)], 'bio-3-2', 'leaf-yeast-colonies', at(8, '8.', '(b)', '(v)'), 3),
    T('8bvi', 'Q8(b)(vi)', 'B', ask(6, 'How did you safely dispose of the plates at the end of the investigation?'),
      [pt(S('(Immerse in) disinfectant or autoclave'), 3)], 'bio-3-2', 'disposing-of-plates',
      at(8, '8.', '(b)', '(vi)'), 3, stem=[M('(iii)', 6), Q8BIII]),
    T('8bvii', 'Q8(b)(vii)', 'B', Q(6, 'Using the axes below, draw a graph to show how the number of leaf yeasts varied',
                                    'following their introduction into the plate.'),
      [pt(S('Lag'), 3), pt(S('Log + stationary or log + decline'), 3)], 'bio-3-2', 'leaf-yeast-growth-curve',
      at(8, '8.', '(b)', '(vii)'), 6, fig='q8bvii-axes',
      decision='The graph\'s two printed features are priced "3" each: two rows. The printed axes are the figure.'),
    T('9ai', 'Q9(a)(i)', 'B', ask(7, 'What is their chemical nature?'), [pt(S('Protein'), 3)], 'bio-2-1',
      'enzymes-are-proteins', at(9, '9.', '(a)', '(i)'), 3, stem=[Q9A], decision=ROW_PRICED),
    T('9aii', 'Q9(a)(ii)', 'B', ask(7, 'Comment upon their molecular shape.'), [pt(S('Folded'), 3)], 'bio-2-1',
      'enzyme-shape', at(9, '9.', '(a)', '(ii)'), 3, stem=[Q9A]),
    T('9bi', 'Q9(b)(i)', 'B', Q9BI, [crit(S('Name of enzyme'), 3)], 'bio-2-1', 'enzyme-used',
      at(9, '9.', '(b)', '(i)'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', ask(7, 'Name the substrate of this enzyme.'), [crit(S('Matching substrate'), 3)],
      'bio-2-1', 'substrate-used', at(9, '9.', '(b)', '(ii)'), 3, stem=[Q9B, M('(i)', 7), Q9BI]),
    T('9biii', 'Q9(b)(iii)', 'B', ask(7, 'Why was it necessary to keep the pH constant in the course of the investigation?'),
      [pt(S('To eliminate it as a possible influence on rate or only one variable'), 3)], 'bio-2-1',
      'controlling-ph', at(9, '9.', '(b)', '(iii)'), 3, stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', ask(7, 'How did you keep the pH constant?'), [pt(S('Buffer'), 3)], 'bio-2-1',
      'buffer', at(9, '9.', '(b)', '(iv)'), 3, stem=[Q9B]),
    T('9bv', 'Q9(b)(v)', 'B', ask(7, 'How did you vary the temperature in the course of the investigation?'),
      [pt(S('Water baths or water bath at different temperatures'), 3)], 'bio-2-1', 'varying-temperature',
      at(9, '9.', '(b)', '(v)'), 3, stem=[Q9B]),
    T('9bvi', 'Q9(b)(vi)', 'B', ask(7, 'How did you know that the enzyme was working?'),
      [crit(S('Description of visible result matching enzyme (or substrate)'), 3)], 'bio-2-1',
      'evidence-of-enzyme-action', at(9, '9.', '(b)', '(vi)'), 3, stem=[Q9B]),
    T('9bvii1', 'Q9(b)(vii)1', 'B',
      [ask(7, 'Use the axes below to summarise the results of your investigation.'), Q(7, 'Do this by', br=True),
       item(7, 1, 'labelling the axes,', 'Do this by')],
      [pt(S('y-axis = Rate and x-axis = Temperature'), 3)], 'bio-2-1', 'labelling-enzyme-graph-axes',
      at(9, '9.', '(b)', '(vii)', why=ITEM_ROMAN), 3, stem=[Q9B], fig='q9bvii-axes',
      decision=EACH_ITEM),
    T('9bvii2', 'Q9(b)(vii)2', 'B',
      [ask(7, 'Use the axes below to summarise the results of your investigation.'), Q(7, 'Do this by', br=True),
       item(7, 2, 'drawing a graph to show how the rate of enzyme action varied with temperature.', 'Do this by')],
      [pt(S('2.'), 3, note='The scheme answers item 2 with a drawing only, shown after reveal: a curve that rises to '
                           'a single peak and then falls.')],
      'bio-2-1', 'graph-of-enzyme-activity-against-temperature', at(9, '9.', '(b)', '(vii)', why=ITEM_ROMAN), 3,
      stem=[Q9B], fig='q9bvii2-scheme', source_pages=[7],
      decision=EACH_ITEM + ' The scheme prices item 2 "3" and prints no words for it, only its marker "2." beside '
               'a drawn curve: the row is that printed marker, the scheme\'s drawing is the solution figure shown '
               'after reveal, and the question page (the printed axes) opens from the card, as 2026 Higher Q4(d) '
               'is carded. Coordinator\'s decision on the item the author brought for it.'),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', ask(8, 'Name the two types of nitrogenous base found in DNA.'),
      [pt(S('*Purines'), 3), pt(S('*Pyrimidines'), 3)], 'bio-1-2', 'purines-and-pyrimidines',
      at(10, '10.', '(a)', '(i)'), 6, stem=[Q10AI], decision=ROW_PRICED + ' The two types are priced "3" each.'),
    T('10aii', 'Q10(a)(ii)', 'C', ask(8, 'Give both of the specific base pairs in DNA structure.'),
      [pt(S('*A + T and *G + C'), 3)], 'bio-1-2', 'base-pairing', at(10, '10.', '(a)', '(ii)'), 3,
      decision='Both pairs are one priced item, "3".'),
    T('10bi', 'Q10(b)(i)', 'C', ask(8, 'State the Law of Segregation and the Law of Independent Assortment.'),
      [pt(s, 3, label=S('Segregation:')) for s in pieces('Traits are governed by pairs of factors', 'one factor)')]
      + [pt(S('Either member of a pair of alleles', 'member of another pair (in gamete formation)'), 3,
            label=S('Assortment:'))],
      'bio-1-4', 'mendels-laws', at(10, '10.', '(b)', '(i)'), 9, stem=[Q10B],
      decision='Segregation "2(3)", its two points cut at the scheme\'s own solidus, and Assortment "3".'),
    T('10bii1', 'Q10(b)(ii)1', 'C', Q10BII1, [pt(S('*SSYy or *ssYy'), 3)], 'bio-1-4', 'writing-a-genotype',
      at(10, '10.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q10B, Q10BII], decision=EACH_ITEM),
    T('10bii2', 'Q10(b)(ii)2', 'C', item(8, 2, 'referred to in 1.', 'lower case letters:'),
      [pt(S('(SSYy) → Smooth + yellow', '(ssYy) → Wrinkled + yellow'), 3)], 'bio-1-4', 'genotype-to-phenotype',
      at(10, '10.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q10B, Q10BII, Q10BII1],
      decision=EACH_ITEM + ' The phenotype matches whichever genotype item 1 gave; the scheme prints both, joined by '
               '"or".'),
    T('10biii', 'Q10(b)(iii)', 'C', Q(8, 'What phenotype will be produced by the genotype SsYy?',
                                      'that you have already given in response to part (ii) 1.'),
      [pt(S('*Smooth + yellow'), 3), pt(S('*SSYY or *SsYY or *SSYy if not used above b(ii) 1.'), 3)], 'bio-1-4',
      'dihybrid-phenotypes', at(10, '10.', '(b)', '(iii)'), 6, stem=[Q10B],
      decision='The phenotype and the other genotype are priced "3" each.'),
    T('10biv', 'Q10(b)(iv)', 'C', Q(8, 'If the allele for smooth were linked to the allele for green and the allele for '
                                       'wrinkled were', 'would produce in the greatest numbers.'),
      [pt(S('*Sy'), 3), pt(S('*sY'), 3)], 'bio-1-4', 'linkage-and-gametes', at(10, '10.', '(b)', '(iv)'), 6,
      stem=[Q10B], decision='The two gametes are priced "3" each.'),
    T('10ci', 'Q10(c)(i)', 'C', ask(8, 'What is meant by the term genetic engineering?'),
      [pt(S('Manipulation of genes or alteration of genes or alteration of genotypes'), 3)], 'bio-3-3',
      'genetic-engineering', at(10, '10.', '(c)', '(i)'), 3),
    T('10cii', 'Q10(c)(ii)', 'C',
      [ask(8, 'In genetic engineering all or some of the following procedures may be involved.'),
       Q(8, 'Isolation;', br=True), Q(8, 'Cutting (restriction);', br=True), Q(8, 'Transformation (ligation);', br=True),
       Q(8, 'Introduction of base sequence changes;', br=True), Q(8, 'Expression.', br=True),
       ask(8, 'Briefly explain each of the above terms in the context of genetic engineering.', br=True)],
      [pt(S('Locating or identififying or removal of a gene (or a', 'piece of DNA or a plasmid)'), 3,
          label=S('Isolation:')),
       pt(S('(Cutting) the DNA (or plasmid) with an (restriction)', 'enzyme'), 3, label=S('Cutting', '(restriction):')),
       pt(S('Transformation : uptake of DNA (or plasmid or gene)', 'Ligation: the joining of DNA (or plasmid or gene)'),
          3, kind='alt', whole=True),
       pt(S('(the order of bases in) the host DNA is now different'), 3,
          label=S('Introduction of base', 'sequence changes:')),
       pt(S('the activation of the inserted gene (in its new position)', 'or production of product'), 3,
          label=S('Expression:'))],
      'bio-3-3', 'stages-of-genetic-engineering', at(10, '10.', '(c)', '(ii)'), 15,
      decision='Each of the five terms is priced "3": five rows, each under the scheme\'s own term. Transformation '
               'and ligation are printed as alternatives joined by "OR", one priced item: one row. The scheme prints '
               '"identififying"; lifted as printed.'),
    T('10ciii', 'Q10(c)(iii)', 'C',
      [ask(8, 'Give one application of genetic engineering in any two of the following.'),
       Q(8, '1. An animal.', br=True), Q(8, '2. A plant.', br=True), Q(8, '3. A micro-organism.', br=True)],
      [anyn(None, 2, 3, note=NO_ANSWER,
            options=[S(w, w) for w in ('Animal example.', 'Plant example.', 'Micro-organism example.')])],
      'bio-3-3', 'applications-of-genetic-engineering', welded(10, '10.', '(c)', '(iii)'), 6,
      decision='"Any two 2(3)" over the scheme\'s three printed categories, none with an example: a menu of its '
               'criteria, claim two.'),
    T('11ai', 'Q11(a)(i)', 'C', Q(9, 'Distinguish between a food chain and a food web.',
                                   'Include a clear reference to each in your answer.'),
      [pt(S('One species at each trophic (or feeding) level', 'or described or diagram'), 3, label=S('Chain:')),
       pt(S('Web: Interconnected food chains or described or diagram or more than',
            'one species at each trophic (or feeding) level'), 3)],
      'bio-3-1', 'food-chain-and-food-web', at(11, '11.', '(a)', '(i)'), 6,
      decision=ROW_PRICED + ' The chain and the web are priced "3" each.'),
    T('11aii', 'Q11(a)(ii)', 'C', ask(9, 'What do ecologists mean by a pyramid of numbers?'),
      [pt(S('(Diagram) that shows the number of organisms at each trophic level'), 3)], 'bio-3-1',
      'pyramid-of-numbers', at(11, '11.', '(a)', '(ii)'), 3),
    T('11bi', 'Q11(b)(i)', 'C', ask(9, 'Suggest a reason for attempting to establish an exotic species in a new country.'),
      [pt(S('Food source or biological control or aesthetic or sporting or other'), 3)], 'bio-3-1',
      'why-introduce-exotic-species', at(11, '11.', '(b)', '(i)'), 3, stem=[Q11B]),
    T('11bii', 'Q11(b)(ii)', 'C', Q(9, 'Suggest two reasons why the great majority of attempted introductions have been',
                                    'unsuccessful.'),
      [anyn(S('Failure to adapt / example of failure to adapt', 'numbers / dispersal / competition'), 2, 3)],
      'bio-3-1', 'failed-introductions', at(11, '11.', '(b)', '(ii)'), 6, stem=[Q11B],
      decision='"Any two 2(3)" over the six printed reasons: a menu, claim two.'),
    T('11biii', 'Q11(b)(iii)', 'C', Q(9, 'Use your knowledge of the life cycle of flowering plants to suggest how an exotic '
                                        'plant may', 'escape from captivity.'),
      [pt(S('Seed dispersal or fruit'), 3)], 'bio-2-5', 'seed-dispersal', at(11, '11.', '(b)', '(iii)'), 3,
      stem=[Q11B]),
] + [
    T(f'11biv{n}', f'Q11(b)(iv){n}', 'C', item(9, n, end, 'introduction of an exotic species may:'), [pt(sel, 3)],
      'bio-3-1', concept, at(11, '11.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q11B, Q11BIV], decision=EACH_ITEM)
    for n, end, sel, concept in [
        (1, 'impact negatively on an existing community.',
         S('Increased competition or (increased) predation or example of',
           'increased competition or example of increased predation', skip_marks=True), 'negative-impact-of-exotics'),
        (2, 'impact positively on an existing community.', S('Control of nuisance species or food or shelter or other'),
         'positive-impact-of-exotics')]
] + [
    T('11bv1', 'Q11(b)(v)1', 'C', item(9, 1, 'Explain the term niche in this context.', 'vacant niche.'),
      [pt(S('Role of organism (in an ecosystem) or explained e.g.', 'how it fits’'), 3)], 'bio-3-1', 'niche',
      at(11, '11.', '(b)', '(v)', why=ITEM_ROMAN), 3, stem=[Q11BV],
      decision=EACH_ITEM + ' The text layer reads the quotation marks around "how it fits" as a low and a raised '
               'double comma, a font artefact read as the single quotes printed.'),
    T('11bv23', 'Q11(b)(v)', 'C', [item(9, 2, 'Do you agree with the above statement?', 'vacant niche.'),
                                   item(9, 3, 'Explain your answer.', 'vacant niche.')],
      [pt(S('Yes, because it is adapted (or is suited) or explained'), 6, note_sel=S('6, 0'),
          note_lead='The scheme marks this answer')], 'bio-3-1', 'vacant-niche',
      at(11, '11.', '(b)', '(v)', why=ITEM_ROMAN), 6, stem=[Q11BV], item=('2-3', 'items 2 and 3'),
      decision='The scheme prints items 2 and 3 as one entry, "2+3.", priced "6, 0", with two answers joined by '
               '"OR" ("Yes, because ..." or "No, because ..."): one card for both items, the answers its variants.'),
] + [
    T(f'11ci{n}', f'Q11(c)(i){n}', 'C', [Q(9, 'Explain the terms'), item(9, n, word, 'Explain the terms')],
      [pt(S(ans), 2)], 'bio-3-1', concept, at(11, '11.', '(c)', '(i)', why=ITEM_ROMAN), 2, stem=[Q11C],
      decision=EACH_ITEM + ' "' + word + '" alone is below the build\'s floor for a question, so the card carries '
               '(i)\'s printed lead-in in its question text. The scheme prints "Name of investigated ecosystem:" '
               'under (c) with no mark against it; the paper\'s ask is the stem of every (c) card.')
    for n, word, ans, concept in [(1, 'Flora,', '*Plants', 'flora'), (2, 'Fauna.', '*Animals', 'fauna')]
] + [
    T('11cii', 'Q11(c)(ii)', 'C', Q(9, 'Name one animal from your named ecosystem and describe how you carried out a',
                                    'quantitative study of that animal.'),
      [crit(S('Named animal (must match named ecosystem and method if given)'), 2),
       crit(S('Details of method:'), 12, units=[2] * 6)],
      'bio-3-1', 'quantitative-study-of-an-animal', at(11, '11.', '(c)', '(ii)'), 14, stem=[Q11C],
      decision='The named animal "2" and the method "6(2)"; the scheme prints no method points, so the method is one '
               'criterion row worth its six 2s.'),
    T('11ciii', 'Q11(c)(iii)', 'C', ask(9, 'Suggest one way in which marking an animal might endanger it.'),
      [pt(S('More conspicuous (to predators) or social outcast or toxic marker'), 2)], 'bio-3-1',
      'marking-animals', at(11, '11.', '(c)', '(iii)'), 2, stem=[Q11C]),
    T('11civ', 'Q11(c)(iv)', 'C', Q(9, 'Ecosystems are subject to changes, both natural and artificial.',
                                    'Mention one of each type of change as it applies to your named ecosystem.'),
      [crit(S('relevant matching example'), 2, label=S('Natural:')),
       crit(S('relevant matching example', nth=2), 2, label=S('Artificial:'))],
      'bio-3-1', 'changes-to-an-ecosystem', at(11, '11.', '(c)', '(iv)'), 4, stem=[Q11C],
      decision='The natural and the artificial change are priced "2" each; the scheme names neither.'),
    T('12ai', 'Q12(a)(i)', 'C', [Q(10, 'From the following list, write into your answer book any term', 'typical plant:'),
                                  Q(10, 'parasitic; heterotrophic; saprophytic; autotrophic.', br=True)],
      [pt(S('*Autotrophic'), 3)], 'bio-2-2', 'autotrophic-nutrition', at(12, '12.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('12aii', 'Q12(a)(ii)', 'C', ask(10, 'Identify, in your answer book, the cell organelles A and B.'),
      [pt(S('(A =) *mitochondrion'), 3), pt(S('(B =) *chloroplast'), 3)], 'bio-1-3', 'mitochondrion-and-chloroplast',
      at(12, '12.', '(a)', '(ii)'), 6, fig='q12a-organelles', labels=ORGANELLES,
      decision='A and B are priced "3" each.'),
    T('12bi1', 'Q12(b)(i)1', 'C', item(10, 1, 'absorbed most by chlorophyll a?', 'The graph below shows'),
      [pt(S('*Violet'), 3), pt(S('*Red'), 3)], 'bio-2-2', 'chlorophyll-a-absorption',
      at(12, '12.', '(b)', '(i)', why=ITEM_ROMAN), 6, stem=[Q12B], fig='q12b-graph',
      decision=EACH_ITEM + ' The two colours are priced "3" each.'),
    T('12bi2', 'Q12(b)(i)2', 'C', item(10, 2, 'absorbed most by chlorophyll b?', 'The graph below shows'),
      [pt(S('*Blue'), 3)], 'bio-2-2', 'chlorophyll-b-absorption', at(12, '12.', '(b)', '(i)', why=ITEM_ROMAN), 3,
      stem=[Q12B], fig='q12b-graph', decision=EACH_ITEM),
    T('12bii', 'Q12(b)(ii)', 'C', ask(10, 'What happens to yellow light when it strikes a leaf?'),
      [pt(S('Not absorbed or little absorption or it is reflected'), 3)], 'bio-2-2', 'yellow-light',
      at(12, '12.', '(b)', '(ii)'), 3, stem=[Q12B], fig='q12b-graph'),
    T('12biii', 'Q12(b)(iii)', 'C', ask(10, 'Suggest one possible benefit to plants of having more than one chlorophyll '
                                            'pigment.'),
      [pt(S('Able to absorb more light (or energy) or able to absorb more (or different)', 'production)'), 3)],
      'bio-2-2', 'several-pigments', at(12, '12.', '(b)', '(iii)'), 3, stem=[Q12B], fig='q12b-graph'),
    T('12biv', 'Q12(b)(iv)', 'C', Q(10, 'From the information provided by the graph suggest how a commercial grower',
                                    'might try to increase crop yield in his glasshouses or tunnels.'),
      [pt(S('Use violet (or blue or orange or red) light'), 3)], 'bio-2-2', 'lighting-glasshouses',
      at(12, '12.', '(b)', '(iv)'), 3, stem=[Q12B], fig='q12b-graph'),
    T('12bv1', 'Q12(b)(v)1', 'C', item(10, 1, 'photosynthesis?', 'might try to increase crop yield'),
      [pt(S('*Air (or atmosphere) or *respiration'), 3)], 'bio-2-2', 'carbon-dioxide-source',
      at(12, '12.', '(b)', '(v)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('12bv2', 'Q12(b)(v)2', 'C', item(10, 2, 'in the dark stage of photosynthesis.', 'might try to increase crop yield'),
      [anyn(S('to transport electrons / to transport energy / H-carrier'), 1, 3, note_sel=S('NADP:')),
       pt(S('Energy source or energy store'), 3, label=S('ATP:'))], 'bio-2-2', 'nadp-and-atp',
      at(12, '12.', '(b)', '(v)', why=ITEM_ROMAN), 6,
      decision=EACH_ITEM + ' NADP\'s role and ATP\'s are priced "3" each; NADP\'s three printed roles, cut at the '
               'scheme\'s own solidus, are a menu, claim one, as the paper asks for one role.'),
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C', term(10, word), [anyn(S(first, last), 2, 3)], 'bio-2-2', concept,
      at(12, '12.', '(c)', f'({r})'), 6, stem=[Q12C],
      decision='"2(3)": two points from the printed list, cut at the scheme\'s own solidus.')
    for r, word, first, last, concept in [
        ('i', 'Glycolysis.', 'First stage of respiration /', 'produces pyruvate / low energy release', 'glycolysis'),
        ('ii', 'Acetyl Co-enzyme A.', 'Aerobic / formed from pyruvate', 'mitochondrion', 'acetyl-coenzyme-a'),
        ('iii', 'Adenosine triphosphate.', 'High energy bonds', 'large ATP production in stage 2', 'atp'),
        ('iv', 'Electron transport chain.', 'Aerobic / in mitochondrion', 'energy release', 'electron-transport-chain')]
] + [
    T('13ai', 'Q13(a)(i)', 'C', Q(11, 'Distinguish between the central nervous system and the peripheral nervous system.',
                                   'Include a clear reference to each in your answer.'),
      [pt(S('brain and spinal cord'), 3, label=S('CNS:')),
       pt(S('nerves leading to and from CNS or nerves not in CNS'), 3, label=S('PNS:'))], 'bio-2-4', 'cns-and-pns',
      at(13, '13.', '(a)', '(i)'), 6, decision=ROW_PRICED + ' The CNS and the PNS are priced "3" each.'),
    T('13aii', 'Q13(a)(ii)', 'C', ask(11, 'Give one way in which a nervous response differs from a hormonal response.'),
      [pt(S('Faster or shorter-lived or electrical'), 3)], 'bio-2-4', 'nervous-and-hormonal-responses',
      at(13, '13.', '(a)', '(ii)'), 3),
    T('13bi', 'Q13(b)(i)', 'C', Q13BI,
      [pt(S('cell body with dendrites + axon + terminal dendrites shown'), 6, kind='criterion', label=S('Diagram:'),
          note_sel=S('Diagram of a sensory neuron gets 0 marks')),
       anyn(S('Cell body / dendrites / axon / myelin sheath / Schwann cells /', '(neurotransmitter) vesicles (or swellings)'),
            6, 1, note_sel=S('Labels:'))],
      'bio-2-4', 'drawing-a-motor-neuron', at(13, '13.', '(b)', '(i)'), 12,
      decision='The drawing is one priced item ("6, 3, 0"): one criterion row naming what it must show, with the '
               'scheme\'s direction on a sensory neuron. Its labels "6(1)": all six printed labels.'),
    T('13bii', 'Q13(b)(ii)', 'C', ask(11, 'Give one function each of any two parts found only in neurons.'),
      [crit(S('Function first named part'), 3), crit(S('Function of second named part'), 3)], 'bio-2-4',
      'parts-of-neurons', at(13, '13.', '(b)', '(ii)'), 6,
      decision='The two functions are priced "3" each; the scheme names no part.'),
    T('13biii', 'Q13(b)(iii)', 'C', ask(11, 'Place an arrow on or near your diagram to indicate the direction of impulse '
                                            'transmission.'),
      [crit(S('*Arrow'), 3)], 'bio-2-4', 'direction-of-impulse', at(13, '13.', '(b)', '(iii)'), 3,
      stem=[M('(i)', 11), Q13BI],
      decision='The scheme prices "*Arrow" and does not say which way it points: a criterion row.'),
    T('13biv', 'Q13(b)(iv)', 'C', ask(11, 'Name and state the role of any two types of neuron, other than the motor '
                                          'neuron.'),
      [pt(S('Sensory neuron carry impulses to CNS (or to named part of CNS)'), 3),
       pt(S('Interneuron carry impulses within CNS or Interneuron carry impulses',
            'from sensory to motor neuron or connect sensory and motor neurons'), 3)],
      'bio-2-4', 'sensory-neurons-and-interneurons', at(13, '13.', '(b)', '(iv)'), 6,
      decision='Each neuron, named with its role, is priced "3".'),
    T('13ci', 'Q13(c)(i)', 'C',
      [ask(11, 'State one function for each of the following parts of the human brain.'),
       Q(11, 'Cerebrum;', br=True), Q(11, 'Hypothalamus;', br=True), Q(11, 'Cerebellum;', br=True),
       Q(11, 'Medulla oblongata.', br=True)],
      [pt(S('language or reason or consciousness or senses or', 'memory or intelligence or emotions or other'), 3,
          label=S('Cerebrum:')),
       pt(S('homeostasis or example of homeostasis or', 'endocrine function or other'), 3, label=S('Hypothalamus:')),
       pt(S('movement or balance or coordination or example'), 3, label=S('Cerebellum:')),
       pt(S('involuntary muscle control or example'), 3, label=S('Medulla oblongata:'))],
      'bio-2-4', 'parts-of-the-brain', at(13, '13.', '(c)', '(i)'), 12,
      decision='Each of the four parts is priced "3": four rows, each under the scheme\'s own name for the part.'),
    T('13cii', 'Q13(c)(ii)', 'C', Q(11, 'In relation to the nervous system, distinguish between grey matter and white '
                                        'matter.', 'Include a clear reference to each in your answer.'),
      [pt(S('few axons or little myelin or mostly cell bodies'), 3, label=S('Grey:')),
       pt(S('many axons or much myelin or few cell bodies'), 3, label=S('White:'))], 'bio-2-4',
      'grey-and-white-matter', at(13, '13.', '(c)', '(ii)'), 6,
      decision='Grey and white matter are priced "3" each.'),
    T('13ciii', 'Q13(c)(iii)', 'C',
      [ask(11, 'In the case of either paralysis or Parkinson’s disease state:'),
       Q(11, '1.', 'a possible cause, other than accident;', after='In the case of either', br=True),
       Q(11, '2.', 'a method of treatment.', after='In the case of either', br=True)],
      [pt(S('Parkinson’s – lack of dopamine or genetic or toxins'), 3, label=S('Cause:')),
       pt(S('Parkinson’s - levodopa or drugs that mimic dopamine', 'or physiotherapy or exercise OR', piece=1,
            psep=' OR'), 3, label=S('Treatment:'))],
      'bio-2-4', 'parkinsons-or-paralysis', at(13, '13.', '(c)', '(iii)'), 6,
      decision='The cause (item 1) and the treatment (item 2) are priced "3" each, for whichever disorder the '
               'candidate chose: the scheme prints Parkinson\'s disease OR paralysis for each, answer variants of '
               'one task. The text layer reads the apostrophe of "Parkinson’s" as a raised double comma, a '
               'font artefact read as the apostrophe printed.'),
] + [
    T(f'14ai{n}', f'Q14(a)(i){n}', 'C', [Q14AI, item(12, n, word, 'Give a brief account of the role of each')],
      [pt(S(ans), 3)], 'bio-2-5', concept, at(14, '14.', '(a)', '(i)', why=ITEM_ROMAN), 3,
      decision=EACH_ITEM + ' "' + word + '" alone is below the build\'s floor for a question, so the card carries '
               '(i)\'s printed lead-in in its question text.')
    for n, word, ans, concept in [
        (1, 'Petal.', 'Attracts insects (or other pollinators)', 'petal'),
        (2, 'Anther.', '(Site of) pollen manufacture or (site of) pollen release', 'anther'),
        (3, 'Stigma.', 'Pollen lands on it or pollen sticks to it or pollen germination', 'stigma')]
] + [
    T('14aii', 'Q14(a)(ii)', 'C', ask(12, 'Name one structure through which the pollen tube grows in order to reach the '
                                          'embryo sac.'),
      [pt(S('Stigma or style or ovary or micropyle'), 3)], 'bio-2-5', 'path-of-pollen-tube',
      at(14, '14.', '(a)', '(ii)'), 3),
] + [
    T(f'14aiii{n}', f'Q14(a)(iii){n}', 'C', item(12, n, end, 'two male gametes.'), [pt(S(a), 3) for a in answers],
      'bio-2-5', concept, at(14, '14.', '(a)', '(iii)', why=ITEM_ROMAN), 3 * len(answers), stem=[Q14AIII],
      decision=EACH_ITEM + ('' if len(answers) == 1 else ' The two answers are priced "3" each.'))
    for n, end, answers, concept in [
        (1, 'What type of division takes place?', ['*mitosis'], 'division-of-generative-nucleus'),
        (2, 'With what does each male gamete fuse in the embryo sac?',
         ['egg [allow ovum or female gamete]', 'polar nuclei'], 'double-fertilisation'),
        (3, 'Name the product of each fusion.', ['*zygote', 'endosperm (nucleus)'], 'zygote-and-endosperm')]
] + [
    T('14aiv', 'Q14(a)(iv)', 'C', Q(12, 'As the seed forms following fertilisation, a food store develops in one of two '
                                        'structures.', 'Name any one of these structures.'),
      [pt(S('Endosperm or cotyledon (or seed leaf or embryonic leaf)'), 3)], 'bio-2-5', 'food-store-in-seeds',
      at(14, '14.', '(a)', '(iv)'), 3),
    T('14bi1', 'Q14(b)(i)1', 'C', Q14BI1, [pt(S(w), 3) for w in ('ectoderm', 'mesoderm', 'endoderm')], 'bio-2-5',
      'germ-layers', at(14, '14.', '(b)', '(i)', why=ITEM_ROMAN), 9, stem=[Q14B],
      decision=EACH_ITEM + ' The three layers are priced "3" each.'),
    T('14bi2', 'Q14(b)(i)2', 'C', item(12, 2, 'that develops from it.', 'development in the womb.'),
      [pt(S('e.g nervous system'), 3, label=S('ectoderm:')), pt(S('e.g skeletal system'), 3, label=S('mesoderm:')),
       pt(S('e.g. digestive system'), 3, label=S('endoderm:'))], 'bio-2-5', 'germ-layer-derivatives',
      at(14, '14.', '(b)', '(i)', why=ITEM_ROMAN), 9, stem=[Q14B, Q14BI1],
      decision=EACH_ITEM + ' Each layer\'s structure is priced "3"; the scheme prints one example for each.'),
    T('14bii', 'Q14(b)(ii)', 'C', ask(12, 'From which tissues does the placenta develop?'),
      [pt(S('Embryonic'), 3), pt(S('Uterine or endometrium'), 3)], 'bio-2-5', 'placenta-origin',
      at(14, '14.', '(b)', '(ii)'), 6, stem=[Q14B], decision='The two tissues are priced "3" each.'),
    T('14biii1', 'Q14(b)(iii)1', 'C', Q14BIII1,
      [pt(S('A membrane (or sac) that surrounds the embryo (or foetus)'), 3)], 'bio-2-5', 'amnion',
      at(14, '14.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q14B], decision=EACH_ITEM),
    T('14biii2', 'Q14(b)(iii)2', 'C', item(12, 2, 'Explain the importance of the amnion for the foetus.',
                                           'From which tissues does the placenta develop?'),
      [pt(S('It contains (or secretes) (amniotic) fluid or protects embryo'), 3)], 'bio-2-5', 'role-of-amnion',
      at(14, '14.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q14B, Q14BIII1], decision=EACH_ITEM),
    T('14ci1', 'Q14(c)(i)1', 'C', item(12, 1, 'Suggest one such stimulus.', 'sexual reproduction in the mould'),
      [pt(S('Dehydration or other named'), 3)], 'bio-3-2', 'trigger-for-zygospores',
      at(15, '14.', '(c)', '(i)', why=ITEM_ROMAN), 3, stem=[Q14CI], decision=EACH_ITEM),
    T('14ci2', 'Q14(c)(i)2', 'C', item(12, 2, 'other than the zygospore.', 'sexual reproduction in the mould'),
      [crit(S('Diagrams:'), 6),
       anyn(S('+ and - / progametangia / gametangia / hypha / zygote'), 3, 2, note_sel=S('Labels:'))],
      'bio-3-2', 'sexual-reproduction-in-rhizopus', at(15, '14.', '(c)', '(i)', why=ITEM_ROMAN), 12, stem=[Q14CI],
      decision=EACH_ITEM + ' The diagrams are one priced item ("6, 3, 0") the scheme does not describe: one criterion '
               'row. Its labels "3(2)": three from the printed five.'),
    T('14ci3', 'Q14(c)(i)3', 'C', item(12, 3, 'Give two advantages to Rhizopus of zygospore formation.',
                                       'sexual reproduction in the mould'),
      [pt(s, 3) for s in pieces('Can survive drought (or named adverse condition) / dispersal')], 'bio-3-2',
      'advantages-of-zygospores', at(15, '14.', '(c)', '(i)', why=ITEM_ROMAN), 6, stem=[Q14CI],
      decision=EACH_ITEM + ' "2(3)": the two advantages, cut at the scheme\'s own solidus.'),
] + [
    T(f'14cii{n}', f'Q14(c)(ii){n}', 'C', item(12, n, end, 'asexual reproduction in yeast.'), [pt(S(ans), 3)],
      'bio-3-2', concept, at(15, '14.', '(c)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q14CII], decision=EACH_ITEM)
    for n, end, ans, concept in [
        (1, 'What term is used to describe the process of asexual reproduction in yeast?', '*Budding', 'budding'),
        (2, 'What happens to the new cells formed in the process?', 'Forms a colony or break away (from the mother cell)',
         'yeast-daughter-cells'),
        (3, 'How does asexual reproduction in Rhizopus differ from that in yeast?', '(Rhizopus) produces spores',
         'rhizopus-and-yeast')]
] + [
    T('15ai', 'Q15(a)(i)', 'C', ask(13, 'Name structures X and Y.'),
      [pt(S('(X =) *Villus'), 3), pt(S('(Y =) *Lacteal'), 3)], 'bio-2-6', 'villus-and-lacteal',
      at(16, '15.', '(a)', '(i)'), 6, stem=[Q15A], fig='q15a-intestine', labels=VILLUS,
      decision='X and Y are priced "3" each.'),
    T('15aii', 'Q15(a)(ii)', 'C', ask(13, 'What process results from the contraction of the two parts of tissue Z?'),
      [pt(S('*Peristalsis'), 3)], 'bio-2-6', 'peristalsis', at(16, '15.', '(a)', '(ii)'), 3, stem=[Q15A],
      fig='q15a-intestine'),
    T('15aiii', 'Q15(a)(iii)', 'C', [Q(13, 'In your answer book, indicate which of the following most accurately',
                                       'the contents of the small intestine.'),
                                     Q(13, 'Acidic. Neutral. Alkaline.', br=True)],
      [pt(S('*Alkaline'), 3)], 'bio-2-6', 'ph-in-small-intestine', at(16, '15.', '(a)', '(iii)'), 3),
    T('15aiv', 'Q15(a)(iv)', 'C', ask(13, 'Name two glands that pass their secretions into the small intestine.'),
      [pt(S('*Pancreas'), 3), pt(S('*Liver'), 3)], 'bio-2-6', 'pancreas-and-liver', at(16, '15.', '(a)', '(iv)'), 6,
      decision='The two glands are priced "3" each.'),
    T('15av1', 'Q15(a)(v)1', 'C', item(13, 1, 'What are symbiotic bacteria?', 'into the small intestine.'),
      [pt(S('(Bacteria) living on or in another organism involving benefit'), 3)], 'bio-2-6', 'symbiotic-bacteria',
      at(16, '15.', '(a)', '(v)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('15av2', 'Q15(a)(v)2', 'C', item(13, 2, 'in the human alimentary canal.', 'into the small intestine.'),
      [anyn(S('Vitamin production / compete with pathogens / reference to digestion /', 'inhibits cancer cells'), 2, 3)],
      'bio-2-6', 'roles-of-gut-bacteria', at(16, '15.', '(a)', '(v)', why=ITEM_ROMAN), 6,
      decision=EACH_ITEM + ' "2(3)" over four printed functions: a menu, claim two.'),
    T('15avi', 'Q15(a)(vi)', 'C', ask(13, 'Where in the human alimentary canal is most water absorbed?'),
      [pt(S('*Colon or *large intestine'), 3)], 'bio-2-6', 'water-absorption', at(16, '15.', '(a)', '(vi)'), 3),
    T('15bi', 'Q15(b)(i)', 'C', ask(13, 'State two ways, other than colour, in which red blood cells differ from white '
                                        'blood cells.'),
      [anyn(S('Smaller / more of them / biconcave', 'transport CO2'), 2, 3)], 'bio-2-6', 'red-and-white-blood-cells',
      at(16, '15.', '(b)', '(i)'), 6, decision='"2(3)" over the nine printed differences: a menu, claim two.'),
    T('15bii', 'Q15(b)(ii)', 'C', ask(13, 'Name a group of white blood cells, other than lymphocytes.'),
      [pt(S('Phagocytic (white cells) or monocytes'), 3)], 'bio-2-6', 'phagocytes', at(16, '15.', '(b)', '(ii)'), 3),
    T('15biii1', 'Q15(b)(iii)1', 'C', item(13, 1, 'What is the role of antibodies in the body?',
                                           'B cells produce antibodies.'),
      [pt(S('To inactivate antigens (or described)'), 3)], 'bio-2-4', 'role-of-antibodies',
      at(16, '15.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q15BIII], decision=EACH_ITEM),
    T('15biii2', 'Q15(b)(iii)2', 'C', Q15BIII2, [anyn(S('Helper / killer / suppressor / memory'), 3, 3)], 'bio-2-4',
      'types-of-t-cell', at(16, '15.', '(b)', '(iii)', why=ITEM_ROMAN), 9, stem=[Q15BIII],
      decision=EACH_ITEM + ' "Any three 3(3)" over four printed types: a menu, claim three.'),
    T('15biii3', 'Q15(b)(iii)3', 'C', item(13, 3, 'that you named in part 2.', 'B cells produce antibodies.'),
      [anyn(None, 3, 3, options=[
          S('Helper: recognise antigens', 'production) or activate killer cell'),
          S('Killer: attack infected cells or secrete perforin'), S('Suppressor: stop immune responses'),
          S('Memory: long term protection', 'exposed) or explained')])],
      'bio-2-4', 'roles-of-t-cells', at(16, '15.', '(b)', '(iii)', why=ITEM_ROMAN), 9, stem=[Q15BIII, Q15BIII2],
      decision=EACH_ITEM + ' "Any three 3(3)": the role of each of the three types named in item 2, from the four '
               'the scheme prints, each under its own type: a menu, claim three.'),
    T('15ci', 'Q15(c)(i)', 'C', ask(13, 'Explain the term homeostasis.'),
      [pt(S('Maintenance of a constant internal environment'), 3)], 'bio-2-4', 'homeostasis',
      at(17, '15.', '(c)', '(i)'), 3),
    T('15cii', 'Q15(c)(ii)', 'C', Q(13, 'Homeostasis often requires an organism to exchange materials between different',
                                    'Explain each of the underlined terms.'),
      [pt(S('movement of substances with (along) a concentration', 'gradient or explained'), 3,
          label=S('diffusion:')),
       pt(S('movement of water through a selectively permeable', 'concentration'), 3, label=S('osmosis:')),
       pt(S('movement of molecules against a concentration gradient', 'or movement of molecules using energy'), 3,
          label=S('active transport:'))],
      'bio-2-6', 'diffusion-osmosis-active-transport', at(17, '15.', '(c)', '(ii)'), 9, qfig='q15c-ii-question',
      decision='Each of the three terms is priced "3": three rows, each under the scheme\'s own term. The paper marks '
               'the terms to explain by underlining them: the question is shown as printed.'),
] + [
    T(f'15ciii{n}', f'Q15(c)(iii){n}', 'C', [Q15CIII, item(13, n, word, 'contributes to homeostasis.')],
      [pt(sel, 3)], 'bio-2-4', concept, at(17, '15.', '(c)', '(iii)', why=ITEM_ROMAN), 3,
      decision=EACH_ITEM + ' The organ alone is too short to stand as a question, so the card carries (iii)\'s printed '
               'lead-in in its question text.')
    for n, word, sel, concept in [
        (1, 'Liver.', S('Absorption of glucose or release of glucose or heat generation'), 'liver-in-homeostasis'),
        (2, 'Lungs.', S('Excretion of water or excretion of CO2 or release of heat'), 'lungs-in-homeostasis'),
        (3, 'Nephrons of kidneys.', S('Excretion of water or reabsorption of water or excretion of salts (or',
                                      'ions) or reabsorbtion of salts (or ions)'), 'kidneys-in-homeostasis')]
] + [
    T('15civ', 'Q15(c)(iv)', 'C', ask(13, 'Describe the role of the skin in controlling body temperature.'),
      [anyn(None, 3, 3, options=[S(SKIN_HOT, piece=i) for i in (1, 2, 3)]
            + [S(*SKIN_COLD, piece=i) for i in (1, 2, 3)])],
      'bio-2-4', 'skin-and-temperature', at(17, '15.', '(c)', '(iv)'), 9,
      decision='"Any three 3(3)" over the six printed responses (three when too hot, three when too cold), each cut '
               'at the scheme\'s own solidus: a menu, claim three. The scheme prints "Constriction of of blood '
               'vessels"; lifted as printed.'),
]

ANSWER_VARIANTS = {
    '11bv23': [
        ('yes', 'Yes', [pt(S('Yes, because it is adapted (or is suited) or explained'), 6, note_sel=S('6, 0'),
                           note_lead='The scheme marks this answer')]),
        ('no', 'No', [pt(S('No, because it is not adapted (or is not suited) or explained'), 6, note_sel=S('6, 0'),
                         note_lead='The scheme marks this answer')]),
    ],
    '13ciii': [
        ('parkinsons', 'Parkinson’s disease',
         [pt(S('Parkinson’s – lack of dopamine or genetic or toxins'), 3, label=S('Cause:')),
          pt(S('Parkinson’s - levodopa or drugs that mimic dopamine', 'or physiotherapy or exercise OR', piece=1,
               psep=' OR'), 3, label=S('Treatment:'))]),
        ('paralysis', 'Paralysis',
         [pt(S('Paralysis – damage to spinal cord'), 3, label=S('Cause:')),
          pt(S('Paralysis – surgery or psysiotherapy'), 3, label=S('Treatment:'))]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-bone': ('paper', 3, (160, 58, 360, 212), SEC, ['X', 'Y', 'Z'],
        'Shaded drawing of the end of a long bone, cut open lengthways: a broad, rounded, two-lobed head on a '
        'narrower shaft running down out of the picture. The cut face of the head is filled with a speckled, '
        'spongy texture inside a thin smooth outer layer. Label X points into the speckled interior of the head; '
        'label Y points to a pale, smooth area at the top of the shaft, just below the speckled region; label Z '
        'points to the smooth outer layer along the left side of the head.',
        False),
    'q5-stem': ('paper', 4, (170, 55, 432, 216), SEC, ['A'],
        'Line drawing of a circular section with a thick outer line, labelled Epidermis by a line to its edge. '
        'Dozens of small dark oval spots, each with a small pale patch, are scattered over the whole interior with '
        'no ring pattern. Two lines from the label A point to two of the spots near the right-hand edge.',
        False),
    'q8bvii-axes': ('paper', 6, (175, 550, 440, 760), SEC, [],
        'A pair of empty axes: a vertical line and a horizontal line meeting at the bottom left. Beside the '
        'vertical axis an arrow points up over the word Number; below the horizontal axis the word Time is '
        'followed by an arrow pointing right. No scale and no plot.',
        False),
    'q9bvii-axes': ('paper', 7, (234, 545, 472, 692), SEC, [],
        'A pair of empty axes: a vertical line and a horizontal line meeting at the bottom left, with no labels, '
        'no scale and no plot.',
        False),
    'q9bvii2-scheme': ('scheme', 9, (160, 345, 420, 452), SEC, [],
        'The marking scheme\'s drawing for item 2: a pair of axes with no labels or scale, and one smooth curve '
        'that rises from low on the left to a single peak in the middle and falls again towards the right.',
        True),
    'q12a-organelles': ('paper', 10, (165, 122, 425, 232), SEC, ['A', 'B'],
        'Two shaded drawings side by side. A: an oval organelle with a smooth outer outline and an inner membrane '
        'folded into many finger-like projections reaching into the interior, with a few small round dots. B: a '
        'larger, irregular oval organelle with a thick outer border, holding stacks of flat discs joined by thin '
        'lines, and two pale rounded patches.',
        False),
    'q12b-graph': ('paper', 10, (125, 296, 522, 470), SEC, [],
        'Line graph: Absorption of light up the vertical axis, an upward arrow and no scale, against Colour of '
        'light along the bottom, marked violet, blue, green, yellow, orange and red. A key shows a solid line for '
        'chlorophyll a and a dashed line for chlorophyll b. The solid line starts at a moderate height at the '
        'left, rises to a peak just right of violet, falls to a low that runs from blue to yellow, rises to a '
        'second peak at red and falls again at the right. The dashed line starts at zero at the left, rises to its '
        'tallest peak at blue, falls to a low through green and yellow, rises to a small peak near orange and '
        'falls again.',
        False),
    'q15a-intestine': ('paper', 13, (128, 84, 425, 252), SEC, ['X', 'Y', 'Z'],
        'Line drawing of part of a section through the wall of the small intestine. Along the top, three tall '
        'finger-like folds, each with a thin outer layer and a dark vessel running up its centre, crossed by a '
        'ladder of fine lines; below them, thin horizontal bands of tissue. At the bottom, a separate block of two '
        'layers, a streaked layer over a dotted layer, above a dark base line. Label X points to the outer edge of '
        'the right-hand fold, label Y to the dark central vessel inside it, and a bracket labelled Z spans the two '
        'layers of the bottom block.',
        False),
    'q15c-ii-question': ('paper', 13, (104, 632, 528, 677), SEC, [],
        'Part (ii) of Question 15(c) as printed: three lines of the question, in which the words diffusion, '
        'osmosis and active transport are underlined.',
        False),
}
