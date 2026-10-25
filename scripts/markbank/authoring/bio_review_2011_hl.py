"""Biology 2011 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2011 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p4 Section A Questions 1-6, p5-p7 Section B Questions 7-9, p8-p12
    Section C Questions 10-15, p13-p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q4(b) and Q14(a) graphs and the Q5(b), Q12(c), Q15(a) and
    Q15(c) drawings carry no credit. Questions 10-13 print their part totals
    "(9)", "(27)", "(24)"; Q14 and Q15 print "(30, 30)".
  * The marking scheme, 20 pages: p1 cover, p2 blank (no text layer), p3
    introduction, cancelled answers and surplus answers, p4 surplus answers
    (continued) and conventions, p5-p17 Questions 1-15, p18 and p19 blank (no
    text layer), p20 back cover (no text layer). Its p5 text layer reads Q2
    before Q1, though the page prints Q1 first.

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c). Every printed ask is carded.

This scheme prints no reprint of any question, only a few label words
("Mechanical:", "Contest:", "Qualitative:", "Gene:", "Cutting:", "Diagram:"):
each answer stands under its own question number, letter and roman, each on
its own printed line. A task is anchored on its own part marker, found by
walking the scheme's numbering down to it (SQ path); a numbered item ("1.",
"2.") is anchored on the roman it is printed under.

Tariffs. Section A is ordered splits, carded at their first rate: Q1 "5(4)
i.e. best FIVE answers from (a) - (f)" (six parts, the best five at 4), Q2 and
Q3 "6(3) + 2", Q4, Q5 and Q6 "6 (3) + 2" (seven responses each). Sections B
and C print a mark against every row ("3", "2(3)", "3(3)", "6(1)", a drawing's
"3, 0"), except Q10(b), whose five observations are priced "3(7) + 2(3)", an
ordered split carded at its first rate. Every other Section B and C task is
priced row by row against the paper's Section B rubric "Part (a) carries 6
marks and part (b) carries 24 marks", Section C's (9), (27), (24) and Q14 and
Q15's (30, 30).

Every printed answer fits a per-response tariff, so no part is carded whole.
Q5(a)(iii) asks for a sentence on each of mechanical and chemical digestion
and the scheme prints both under the one roman; Q5's seven printed parts are
the seven responses of "6 (3) + 2", so (iii) is one response whose two
printed answers are given together (one allof row).

Alternatives the scheme prints joined by "OR" are answer variants of one task:
Q10(c)(iii)'s quadrat and transect menus, Q13(b)(ii)1's two symbol sets for the
genotypes, and Q14(a)(ii)'s two ways of measuring the rate.

The census reader finds all 140 printed asks, keyed as the paper prints them;
no paper.py entry was needed for this sitting. Its leaves Q6(a)(i) and (ii)
are the paper's two answer lines under (a)'s one ask ("Give two differences
... (i) ____ (ii) ____"), so their extracted text is only the ruled line; the
one Q6(a) task claims both.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, allof, T, L, G  # noqa: F401

YEAR, LEVEL = 2011, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2011-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': '46726519ae71e6c5d9cc926a7c59f9c7d9d253c3997ecb68288b5265e83ad8a2',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2011-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '63f5cf1e1a6d140d3073fa16ccec33290ed4f12c08117a091de173b327626f93',
               'pages': 20},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 13)}, **{p: 'blank' for p in range(13, 17)}},
    'scheme': {1: 'cover', 2: 'blank', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 18)}, 18: 'blank', 19: 'blank', 20: 'back-cover'},
}


def _ladder(notation, **extra):
    """An ordered split as the scheme prints it: "6(3) + 2", "3(7) + 2(3)"."""
    steps = []
    for term_ in notation.split('+'):
        n, _, m = term_.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)}, 14: 90, 15: 90,   # Q14, Q15: any two of three 30s
}
# Only parts priced row by row: Q10(b)'s cards are carded at its ladder's
# first rate, so their sum is not its printed (27).
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p5: "Part (a) carries 6 marks
    **{(n, 'b'): 24 for n in (7, 8, 9)},   # and part (b) carries 24 marks"
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
    **{(n, 'b'): 27 for n in (11, 12, 13)},   # "(27)"
    **{(n, 'c'): 24 for n in (10, 11, 12, 13)},   # "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
# Q1: six parts, the best five priced at 4 ("5(4) i.e. best FIVE answers").
BEST_OF = {1: (5, 4)}
LADDERS = {
    2: _ladder('6(3) + 2'), 3: _ladder('6(3) + 2'),
    4: _ladder('6 (3) + 2'), 5: _ladder('6 (3) + 2'), 6: _ladder('6 (3) + 2'),
    (10, 'b'): _ladder('3(7) + 2(3)'),
}

CHECKSUMS = {
    1: {4: 6},   # six parts at 4, the best five counted
    2: {3: 7}, 3: {3: 7}, 4: {3: 7}, 5: {3: 7}, 6: {3: 7},
    **{(n, 'a'): {3: 2} for n in (7, 8, 9)}, **{(n, 'b'): {3: 8} for n in (7, 8, 9)},
    (10, 'a'): {3: 3}, (10, 'b'): {7: 5}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 9}, (11, 'c'): {3: 8},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 7, 2: 3}, (12, 'c'): {1: 6, 3: 6},
    (13, 'a'): {3: 3}, (13, 'b'): {3: 9}, (13, 'c'): {3: 8},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 9, 1: 3},
    (15, 'a'): {2: 3, 3: 8}, (15, 'b'): {3: 10}, (15, 'c'): {3: 10},
}

SCAN_PAGES = {'paper': range(1, 13)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 "Answer five of the following": best five of (a)-(f); each part is its own card '
                                  'at 4.'),
    ('paper', 2, 'or', 'Q1(a) "Sudan III or brown paper": description.'),
    ('paper', 2, 'or', 'Q1(c) "the Fehling\'s or Benedict\'s test": description.'),
    ('paper', 2, 'the following', 'Q2 lead-in: every part asked.'),
    ('paper', 3, 'choose', 'Q3 "Choose suitable terms from the list below": the answer options (eight terms for seven '
                           'descriptions); every description is carded.'),
    ('paper', 3, 'the following', 'Q3, same lead-in.'),
    ('paper', 3, 'or', 'Q3(a) "lives on or in a second species": description.'),
    ('paper', 4, 'or', 'Q6 "in one stage or two stages": description.'),
    ('paper', 5, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 5, 'the following', 'Q7(a) "explain each of the following": both terms asked, one card each.'),
    ('paper', 5, 'the following', 'Q7(b) lead-in: every part asked.'),
    ('paper', 6, 'the following', 'Q8(a) "State a use for each of the following": both asked, one card each.'),
    ('paper', 7, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 8, 'the following', 'Q10(b) "each of the following observations": every observation asked, one card '
                                  'each on the "3(7) + 2(3)" ladder.'),
    ('paper', 9, 'the following', 'Q12(b)(i) "Label the following parts of your diagram": every label asked, one row '
                                  'each.'),
    ('paper', 10, 'either', 'Q13(a)(ii) "Name either of the scientists": one response; the alternatives on one row.'),
    ('paper', 10, 'the following', 'Q13(c) "each of the following pairs of terms": every pair asked, one card each.'),
    ('paper', 11, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 11, 'either', 'Q14(a) "either light intensity or CO2 concentration": the candidate addresses one factor; '
                            'the scheme marks both on the same rows, so no route.'),
    ('paper', 11, 'or', 'Q14(a), same choice.'),
    ('paper', 11, 'choose', 'Q14(a) "indicate clearly which factor you choose to address": same choice.'),
    ('paper', 11, 'the following', 'Q14(a) lead-in: every part asked.'),
    ('paper', 11, 'the following', 'Q14(b)(iii) "In each of the following cases": one card per numbered item.'),
    ('paper', 11, 'or', 'Q14(b)(iii) "anabolic or catabolic": the answer options.'),
    ('paper', 12, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 12, 'or', 'Q15(a)(iv) "a named defect of hearing or vision": the candidate names one; the scheme marks '
                        'either on the same two rows.'),
]

ROUTES = {}

SEC = 'State Examinations Commission'
NO_REPRINT = 'The scheme prints no reprint of any question: anchored on the part\'s own marker.'
ITEM_ROMAN = 'The scheme prints no reprint: a numbered item is anchored on the roman it is printed under.'
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
ROW_PRICED = 'Sections B and C print a mark against every row.'


def ask(page, sentence, **kw):
    """A one-line ask closed by its own punctuation."""
    return Q(page, sentence, sentence, **kw)


def term(page, word, br=False):
    """A printed term the paper sets before its answer line ("Theory. ____")."""
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


def eq(line, marks, **kw):
    """A scheme line "A = cochlea": the answer after " = ", labelled with what precedes it."""
    return pt(S(line, piece=2, psep=' = '), marks, label=S(line, piece=1, psep=' = '), **kw)


# ------------------------------------------------------------ question text --
Q1 = Q(2, 'Answer five of the following:')
Q2 = ask(2, 'Use your knowledge of mitosis to answer the following questions:')
Q2B = Q(2, 'What medical term is used for the group of disorders', 'mitosis?')
Q2D = Q(2, 'Name the stage of mitosis in which the chromosomes', 'before they begin to separate.')
Q3 = [ask(3, 'Choose suitable terms from the list below that most closely match each of the following descriptions:'),
      ask(3, 'population; producers; competition; predation; community; symbiosis; decomposers; parasitism')]
Q4B = ask(3, 'The graph shows daily variations of human body temperature over three days.')
Q4BII = ask(3, 'At what time each day does body temperature drop to its lowest level?')
Q5B = ask(4, 'The diagram shows part of the human alimentary canal and associated structures.')
Q6 = ask(4, 'Cellular respiration may occur in one stage or two stages.')
Q6C = ask(4, 'What term is used to describe respiration in which only Stage 1 occurs?')
Q6E = Q(4, 'In Stage 2 of respiration electrons pass', 'molecule is this energy stored in the cell?')
Q7A = ask(5, 'In relation to the scientific method, explain each of the following.')
Q7B = Q(5, 'Scientists investigated the effect of a certain mineral on the growth of wheat.',
        'answer the following questions.')
Q7BII = Q(5, 'The compost in which the wheat plants were grown was sterilised', 'investigation.')
Q8A = ask(6, 'State a use for each of the following in the biology laboratory:')
Q9B = Q(7, 'Answer the following questions by referring to the procedures', 'plant tissue.')
Q9BI = ask(7, 'Having obtained a plant tissue e.g. onion,')
Q9BI1 = ask(7, '1. What was the first procedure that you followed?')
Q9BIV1 = ask(7, '1. What is a protease?')
Q9BV = ask(7, 'The final stage of the isolation involves the use of freezer-cold ethanol.')
Q10B = ask(8, 'What deduction is it possible to make from each of the following observations?')
Q11BI = ask(8, 'Name the group of substances in plants which control responses to external stimuli.')
Q11BII1 = ask(8, '1. What name is given to the regions in plants in which these substances are produced?')
Q11BIII = ask(8, 'Most plant shoots are positively phototropic. Explain the underlined term.')
Q11CIII1 = ask(8, '1. What is meant by feedback in relation to hormone action?')
Q12BI = Q(9, 'Draw a large labelled diagram of a vertical section through a human kidney.', 'cortex, medulla, pelvis.')
Q12BIII1 = ask(9, '1. Name the blood vessel that supplies blood to a kidney.')
Q12C = ask(9, 'The diagram above shows the structure of a nephron and its associated blood supply.')
Q13B = Q(10, 'In the antirrhinum (snapdragon) there is no dominance',
         'These pairs of alleles are located on different chromosome pairs.')
Q13BII = Q(10, 'A plant which had pink flowers and was heterozygous', 'with one which had white flowers and a short stem.')
Q13BII1 = ask(10, '1. Using suitable symbols determine the genotypes of all the possible offspring of this cross.')
Q13C = Q(10, 'Distinguish between the members of each of the following pairs of terms,',
         'about each member of each pair.')
Q14A = [Q(11, 'The graph shows the results of a classroom investigation', 'or CO2 concentration.'),
        Q(11, 'In your answer book, indicate clearly which factor', 'following questions:')]
Q14AIII = ask(11, 'Name a factor that must be kept constant during this investigation.')
Q14AVI1 = [Q(11, '1.', 'investigation is', after='Why is it necessary to keep that factor constant?'),
           ask(11, 'A. carried out at 25°C?', br=True), ask(11, 'B. carried out at 35°C?', br=True)]
Q14BIII = ask(11, 'In each of the following cases state whether the process is anabolic or catabolic.')
Q14CII = ask(11, 'With what type of cell do you associate membrane-bound organelles?')
Q15AI = ask(12, 'The diagram above shows the internal structure of the human ear.')
Q15BI = ask(12, 'Name the tissue in plant stems through which water rises to the leaves.')
Q15C = ask(12, 'The diagram below shows part of the mycelium of the fungus Rhizopus.')
Q15CIII = ask(12, 'The nutrition of Rhizopus is described as being saprophytic.')

# Q5(b)'s two letters as the scheme names them (p7).
CANAL_W = [L('W', S('Duodenum or small intestine', page=7), True)]
CANAL_X = [L('X', S('Gall bladder or liver', page=7), True)]
# Q12(c)(i)1's six numbered parts (p12), each on its own printed line closed
# by a semicolon (the last by none).
NEPHRON = ['1 = Bowman’s capsule;', '2 = glomerulus;', '3 = afferent arteriole;', '4 = efferent arteriole;',
           '5 = proximal (convoluted) tubule;', '6 = distal (convoluted) tubule']
# Q15(a)(i)'s three named parts (p16); D and E are given only as functions.
EAR = ['A = cochlea', 'B = eardrum', 'C = auditory nerve']
EAR_KEY = [L(ln[0], S(ln, page=16, piece=2, psep=' = '), True) for ln in EAR]
EAR_NAMED = [L(ln[0], S(ln, page=16, piece=2, psep=' = '), False) for ln in EAR]
RHIZOPUS_A = [L('A', S('A = rhizoids', page=17, piece=2, psep=' = '), True)]
RHIZOPUS_B = [L('B', S('B = sporangium', page=17, piece=2, psep=' = '), True)]
# Q13(b)(ii)'s direction under its genotype and phenotype rows (p13), printed
# once for both items.
EXCESS = S('Each excess incorrect cancels a correct answer')
# Q14(c)(vii)'s labels line (p15), over two printed lines.
OSMOSIS_LABELS = ('Labels: Membrane or plant tissue / solution 1 indicated / solution 2', 'indicated')

TASKS = [
    # ------------------------------------------------------------ Section A --
    T(f'1{x}', f'Q1({x})', 'A', q, [row], 'bio-1-2', concept, at(5, '1.', f'({x})'), 4, stem=[Q1],
      decision='The scheme prints Q1 as "5(4) i.e. best FIVE answers from (a) – (f)": six parts, the best five at 4, '
               'each part its own card.')
    for x, q, row, concept in [
        ('a', ask(2, 'Which food type may be identified in the laboratory by the use of Sudan III or brown paper?'),
         pt(S('Fat (or oil or lipid)'), 4), 'test-for-fat'),
        ('b', ask(2, 'Give one role for a named mineral in plants.'), crit(S('Role matching named mineral'), 4),
         'minerals-in-plants'),
        ('c', ask(2, 'What colour indicates a strong positive result of the Fehling’s or Benedict’s test for reducing '
                     'sugar?'),
         pt(S('Orange or red'), 4), 'reducing-sugar-test'),
        ('d', ask(2, 'Give a role of lipids in cells.'),
         pt(S('Component of membranes (or of named membrane)', 'phospholipid (or lipoprotein)'), 4), 'roles-of-lipids'),
        ('e', ask(2, 'Give a role of water in the human body other than as a component of cytoplasm and body fluids.'),
         pt(S('Solvent (or example of solvent)', 'lubrication qualified or protection qualified'), 4),
         'roles-of-water'),
        ('f', ask(2, 'How many common amino acids are found in proteins?'), pt(S('20 (common amino acids)'), 4),
         'twenty-amino-acids')]
] + [
    T(f'2{x}', f'Q2({x})', 'A', q, [row], 'bio-2-3', concept, at(5, '2.', f'({x})'), 3, stem=stem,
      decision=ladder(2, '6(3) + 2') + ' Seven responses.')
    for x, q, row, concept, stem in [
        ('a', ask(2, 'What is the role of mitosis in single-celled organisms?'), pt(S('Reproduction'), 3),
         'mitosis-in-single-celled-organisms', [Q2]),
        ('b', Q2B, pt(S('Cancer'), 3), 'cancer', [Q2]),
        ('c', ask(2, 'Suggest a possible cause of one of the group of disorders referred to in (b).'),
         crit(S('Named carcinogen'), 3), 'causes-of-cancer', [Q2, M('(b)', 2), Q2B]),
        ('d', Q2D, pt(S('Metaphase'), 3), 'metaphase', [Q2]),
        ('e', ask(2, 'To what are the chromosomes attached in the stage of mitosis referred to in (d)?'),
         pt(S('Spindle'), 3), 'spindle', [Q2, M('(d)', 2), Q2D]),
        ('f', ask(2, 'Towards the end of mitosis, in what type of cell does a cell plate form?'),
         pt(S('Plant (cell) or named example'), 3), 'cell-plate', [Q2]),
        ('g', ask(2, 'Give one way in which mitosis differs from meiosis.'),
         pt(S('Two (daughter) cells or identical (daughter) cells', 'or can occur in haploid cells'), 3),
         'mitosis-and-meiosis', [Q2])]
] + [
    T(f'3{x}', f'Q3({x})', 'A', ask(3, q), [pt(S(ans), 3)], 'bio-3-1', concept, at(6, '3.', f'({x})'), 3, stem=Q3,
      decision=ladder(3, '6(3) + 2') + ' Seven responses.')
    for x, q, ans, concept in [
        ('a', 'A situation in which one organism lives on or in a second species, feeding on it and causing it harm.',
         'Parasitism', 'parasitism'),
        ('b', 'Organisms capable of making their own food.', 'Producers', 'producers'),
        ('c', 'All the members of a species living in an area.', 'Population', 'population'),
        ('d', 'Micro-organisms and other organisms that return nutrients to the environment by decay.', 'Decomposers',
         'decomposers'),
        ('e', 'A situation in which two organisms of different species live together and at least one benefits.',
         'Symbiosis', 'symbiosis'),
        ('f', 'A struggle between organisms for a scarce resource.', 'Competition', 'competition'),
        ('g', 'One organism killing and eating another organism.', 'Predation', 'predation')]
] + [
    T(f'4{k}', f'Q4{ref}', 'A', q, [pt(S(*ans), 3)], 'bio-2-4', concept, at(6, '4.', *path), 3, stem=stem,
      fig=fig, decision=ladder(4, '6 (3) + 2') + ' Seven responses.')
    for k, ref, q, ans, concept, path, stem, fig in [
        ('ai', '(a)(i)', ask(3, 'What is an endotherm?'),
         ('(An animal that) produces its', '(temperature of) environment'), 'endotherm', ('(a)', '(i)'), [], None),
        ('aii', '(a)(ii)', ask(3, 'What word is used to describe animals which are not endotherms?'), ('Ectotherms',),
         'ectotherms', ('(a)', '(ii)'), [], None),
        ('aiii', '(a)(iii)', ask(3, 'Suggest an advantage of being an endotherm.'),
         ('(Temperature always suitable) for good enzyme activity', 'activity independent of environmental temperature'),
         'advantage-of-endothermy', ('(a)', '(iii)'), [], None),
        ('bi', '(b)(i)', Q(3, 'What is the maximum range of body temperature', 'graph?'),
         ('35.7°C to 37.6°C or 1.9°C or 36°C to 37.6° or 1.6°C',), 'range-of-body-temperature', ('(b)', '(i)'),
         [Q4B], 'q4b-graph'),
        ('bii', '(b)(ii)', Q4BII, ('(Any quoted time from) 3 a.m. to 6 a.m. inclusive',), 'lowest-body-temperature',
         ('(b)', '(ii)'), [Q4B], 'q4b-graph'),
        ('biii', '(b)(iii)', ask(3, 'Suggest a reason for the drop in temperature at the time referred to in (ii).'),
         ('Low metabolism (or explained) or sleep (or inactivity)',), 'night-time-temperature-drop', ('(b)', '(iii)'),
         [Q4B, M('(ii)', 3), Q4BII], 'q4b-graph'),
        ('biv', '(b)(iv)', ask(3, 'Children typically have higher body temperatures than adults. Suggest a reason for '
                                  'this.'),
         ('High metabolism or growing', 'teething'), 'body-temperature-in-children', ('(b)', '(iv)'), [Q4B],
         'q4b-graph')]
] + [
    T('5ai', 'Q5(a)(i)', 'A', ask(4, 'What is meant by the term digestion?'), [pt(S('The breakdown of food'), 3)],
      'bio-2-6', 'digestion', at(7, '5.', '(a)', '(i)'), 3, decision=ladder(5, '6 (3) + 2') + ' Seven responses.'),
    T('5aii', 'Q5(a)(ii)', 'A', ask(4, 'Why is digestion necessary?'),
      [pt(S('For solubility or for absorption or for transport'), 3)], 'bio-2-6', 'why-digestion',
      at(7, '5.', '(a)', '(ii)'), 3, decision=ladder(5, '6 (3) + 2') + ' Seven responses.'),
    T('5aiii', 'Q5(a)(iii)', 'A', ask(4, 'Distinguish between mechanical and chemical digestion by writing a sentence '
                                        'about each.'),
      [allof([(S('Mechanical:'), S('physical or grinding or cutting or churning or chewing or emulsifying')),
              (S('Chemical:'), S('(action of) enzyme or named enzyme or (action of) acid or named acid'))], 3)],
      'bio-2-6', 'mechanical-and-chemical-digestion', at(7, '5.', '(a)', '(iii)'), 3,
      decision=ladder(5, '6 (3) + 2') + ' Q5 prints seven parts, the seven responses of its notation, so (iii) is one '
               'response: the scheme\'s two answers under it ("Mechanical:", "Chemical:") are given together, one '
               'row. Brought to the coordinator: if each sentence were its own response, Q5 would have eight '
               'responses for a seven-step ladder.'),
] + [
    T(f'5b{r}', f'Q5(b)({r})', 'A', q, [pt(S(ans), 3)], 'bio-2-6', concept, at(7, '5.', '(b)', f'({r})'), 3,
      stem=[Q5B], fig='q5b-canal', labels=labels, decision=ladder(5, '6 (3) + 2') + ' Seven responses.')
    for r, q, ans, concept, labels in [
        ('i', ask(4, 'What part of the alimentary canal is labelled W?'), 'Duodenum or small intestine', 'duodenum',
         CANAL_W),
        ('ii', ask(4, 'The bile duct is connected to X. Name X.'), 'Gall bladder or liver', 'gall-bladder', CANAL_X),
        ('iii', ask(4, 'From which part of the alimentary canal does food arrive into W?'), 'Stomach',
         'stomach-to-duodenum', None),
        ('iv', ask(4, 'State one digestive function of the pancreas.'),
         '(Produces) enzymes or named enzyme or neutralises (chyme)', 'pancreas-in-digestion', None)]
] + [
    T('6a', 'Q6(a)', 'A', ask(4, 'Give two differences, other than location, between Stage 1 and Stage 2.'),
      [pt(S('Stage 1 does not require O2 or is anaerobic'), 3),
       pt(S('produces a small amount of energy (or produces a small amount of ATP)'), 3)], 'bio-2-2',
      'stage-1-and-stage-2', at(7, '6.', '(a)'), 6, stem=[Q6],
      decision='The two differences, on the paper\'s answer lines (i) and (ii) and printed by the scheme under '
               '"(i), (ii)", are two responses on the "6 (3) + 2" ladder: one card for both lines.'),
] + [
    T(f'6{x}', f'Q6({x})', 'A', q, [pt(S(ans), 3)], 'bio-2-2', concept, at(7, '6.', f'({x})'), 3, stem=stem,
      decision=ladder(6, '6 (3) + 2') + ' Seven responses.')
    for x, q, ans, concept, stem in [
        ('b', ask(4, 'Where in a cell does Stage 1 occur?'), 'Cytoplasm or cytosol', 'site-of-stage-1', [Q6]),
        ('c', Q6C, 'Anaerobic or fermentation', 'anaerobic-respiration', [Q6]),
        ('d', ask(4, 'Name a chemical end product of the type of respiration referred to in (c).'),
         'Ethanol or lactic acid or CO2', 'products-of-fermentation', [Q6, M('(c)', 4), Q6C]),
        ('e', Q6E, 'ATP', 'atp', [Q6]),
        ('f', ask(4, 'To what are these electrons transferred at the end of the electron transport chain?'),
         'Oxygen or H+ (or protons)', 'final-electron-acceptor', [Q6, M('(e)', 4), Q6E])]
] + [
    # ------------------------------------------------------------ Section B --
    # "Theory." alone is below the build's eight-character floor, so that card
    # carries (a)'s printed lead-in in its question text instead of its stem.
    T(f'7a{r}', f'Q7(a)({r})', 'B', [Q7A, term(5, word, br=True)] if len(word) < 8 else term(5, word),
      [pt(S(ans), 3)], 'bio-u2', concept, at(8, '7.', '(a)', f'({r})'), 3, stem=[] if len(word) < 8 else [Q7A],
      decision=ROW_PRICED)
    for r, word, ans, concept in [('i', 'Experiment.', 'Test of hypothesis or test of prediction', 'experiment'),
                                  ('ii', 'Theory.', 'Hypothesis (or explained) supported (by experiment)', 'theory')]
] + [
    T('7bi', 'Q7(b)(i)', 'B', ask(5, 'Suggest a reason why the seeds used were all taken from one parent plant.'),
      [pt(S('To minimise (genetic) variation'), 3)], 'bio-u2', 'seeds-from-one-parent', at(8, '7.', '(b)', '(i)'), 3,
      stem=[Q7B]),
    T('7bii1', 'Q7(b)(ii)1', 'B', ask(5, '1. Suggest a way in which the scientists may have sterilised the compost.'),
      [pt(S('Heat (or method of heating) or named chemical or irradiation (or', 'named)'), 3)], 'bio-u2',
      'sterilising-compost', at(8, '7.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q7B, Q7BII], decision=EACH_ITEM),
    T('7bii2', 'Q7(b)(ii)2', 'B', ask(5, '2. State one reason why it was important to sterilise the compost.'),
      [pt(S('To kill organisms or to prevent contamination or to eliminate', 'or to eliminate disease or described'),
          3)], 'bio-u2', 'why-sterilise-compost', at(8, '7.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[Q7B, Q7BII],
      decision=EACH_ITEM),
    T('7biii', 'Q7(b)(iii)', 'B', ask(5, 'Why did the scientists divide the young wheat plants into two equal groups?'),
      [pt(S('As control (or described)'), 3)], 'bio-u2', 'control-group', at(8, '7.', '(b)', '(iii)'), 3,
      stem=[Q7B]),
    T('7biv', 'Q7(b)(iv)', 'B', Q(5, 'During the investigation the scientists kept the two groups of plants under '
                                     'identical', 'Why was this?'),
      [pt(S('To have only one variable (or explained)'), 3)], 'bio-u2', 'identical-conditions',
      at(8, '7.', '(b)', '(iv)'), 3, stem=[Q7B]),
    T('7bv', 'Q7(b)(v)', 'B', Q(5, 'Name two conditions you think the scientists would have kept constant during the',
                                'investigation.'),
      [anyn(S('Temperature / Light / pH / CO2 / humidity / other minerals / H2O', 'H2O'), 2, 3)], 'bio-u2',
      'conditions-kept-constant', at(8, '7.', '(b)', '(v)'), 6, stem=[Q7B],
      decision='"Any 2 2(3)" over seven printed conditions: a menu, claim two.'),
    T('7bvi', 'Q7(b)(vi)', 'B', Q(5, 'Why did the scientists repeat the investigation several times', 'a scientific '
                                     'journal?'),
      [pt(S('To ensure (statistical) reliability'), 3)], 'bio-u2', 'repeating-for-reliability',
      at(8, '7.', '(b)', '(vi)'), 3, stem=[Q7B]),
    T('8ai', 'Q8(a)(i)', 'B', term(6, 'Buffer solution.'), [pt(S('To keep pH constant'), 3)], 'bio-2-1',
      'use-of-buffer-solution', at(8, '8.', '(a)', '(i)'), 3, stem=[Q8A], decision=ROW_PRICED),
    T('8aii', 'Q8(a)(ii)', 'B', term(6, 'Biuret test.'), [pt(S('To detect presence of protein'), 3)], 'bio-1-2',
      'use-of-biuret-test', at(8, '8.', '(a)', '(ii)'), 3, stem=[Q8A]),
    T('8bi', 'Q8(b)(i)', 'B', Q(6, 'In the course of your practical studies you used a solution of iodine',
                                'State two different uses of the iodine solution.'),
      [pt(S('Starch detection (or use of)'), 3), pt(S('Examining cells (or described)'), 3)], 'bio-1-2',
      'uses-of-iodine', at(8, '8.', '(b)', '(i)'), 6, decision='The two uses are priced "3" each.'),
    T('8bii', 'Q8(b)(ii)', 'B', ask(6, 'State two different uses of a water bath in biological investigations.'),
      [anyn(S('Keep temperature constant (or example) / to vary temperature (or example)',
              '/ denaturing enzyme / heating'), 2, 3)], 'bio-2-1', 'uses-of-a-water-bath', at(8, '8.', '(b)', '(ii)'),
      6, decision='"Any 2 2(3)" over four printed uses: a menu, claim two.'),
    T('8biii', 'Q8(b)(iii)', 'B', Q(6, 'In the course of your practical studies you found that heart rate',
                                    'Explain why this is the case.'),
      [anyn(S('More energy (required) / more oxygen (required) / more CO2 (produced)'), 2, 3)], 'bio-2-6',
      'exercise-and-breathing-rate', at(8, '8.', '(b)', '(iii)'), 6,
      decision='"Any 2 2(3)" over three printed points: a menu, claim two.'),
    T('8biv', 'Q8(b)(iv)', 'B', Q(6, 'In the course of your practical work you prepared', 'How did you prepare the '
                                     'T.S.?'),
      [pt(S('Cutting: Cut thin (section) or (cut) away (from self) or with scalpel (or', 'blade or microtome)'), 3),
       pt(S('Placed onto slide with water or how cover slip applied'), 3, label=S('Mounting:'))], 'bio-2-6',
      'preparing-a-stem-section', at(8, '8.', '(b)', '(iv)'), 6,
      decision='Cutting and mounting are priced "3" each, each with the scheme\'s own label.'),
    T('9ai', 'Q9(a)(i)', 'B', ask(7, 'How are the two strands of a DNA molecule joined together?'),
      [pt(S('Hydrogen bonds'), 3)], 'bio-1-2', 'hydrogen-bonds-in-dna', at(9, '9.', '(a)', '(i)'), 3,
      decision=ROW_PRICED),
    T('9aii', 'Q9(a)(ii)', 'B', ask(7, 'What is ‘junk’ DNA?'), [pt(S('Non-coding (or described)'), 3)], 'bio-1-2',
      'junk-dna', at(9, '9.', '(a)', '(ii)'), 3),
    T('9bi1', 'Q9(b)(i)1', 'B', Q9BI1, [pt(S('Chop'), 3)], 'bio-1-2', 'chopping-the-tissue',
      at(9, '9.', '(b)', '(i)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BI], decision=EACH_ITEM),
    T('9bi2', 'Q9(b)(i)2', 'B', Q(7, '2.', 'What was the reason for that procedure?', after='What was the first procedure'),
      [pt(S('To disrupt structure (or described) or to increase surface area'), 3)], 'bio-1-2', 'why-chop',
      at(9, '9.', '(b)', '(i)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BI, Q9BI1], decision=EACH_ITEM),
    T('9bii', 'Q9(b)(ii)', 'B', ask(7, 'Washing-up liquid is then used in the isolation. Give a reason for its use.'),
      [pt(S('To disrupt membranes'), 3)], 'bio-1-2', 'washing-up-liquid', at(9, '9.', '(b)', '(ii)'), 3, stem=[Q9B]),
    T('9biii', 'Q9(b)(iii)', 'B', ask(7, 'Salt (sodium chloride) is also used in the isolation. Give a reason for its '
                                        'use.'),
      [pt(S('To clump the DNA (or described) or to protect DNA from other positive', 'ions'), 3)], 'bio-1-2',
      'salt-in-dna-isolation', at(9, '9.', '(b)', '(iii)'), 3, stem=[Q9B]),
    T('9biv1', 'Q9(b)(iv)1', 'B', Q9BIV1, [pt(S('An enzyme that digests protein'), 3)], 'bio-1-2', 'protease',
      at(9, '9.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q9B], decision=EACH_ITEM),
    T('9biv2', 'Q9(b)(iv)2', 'B', Q(7, '2.', 'Why is a protease necessary when isolating DNA?',
                                    after='What is a protease?'),
      [pt(S('Because DNA is combined with protein'), 3)], 'bio-1-2', 'why-protease',
      at(9, '9.', '(b)', '(iv)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BIV1], decision=EACH_ITEM),
    T('9bv1', 'Q9(b)(v)1', 'B', ask(7, '1. Describe how it is used.'),
      [pt(S('Added down the side of the test tube or added slowly'), 3)], 'bio-1-2', 'adding-cold-ethanol',
      at(9, '9.', '(b)', '(v)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BV], decision=EACH_ITEM),
    T('9bv2', 'Q9(b)(v)2', 'B', ask(7, '2. For what purpose is it used?'),
      [pt(S('To bring the DNA out of solution'), 3)], 'bio-1-2', 'why-cold-ethanol',
      at(9, '9.', '(b)', '(v)', why=ITEM_ROMAN), 3, stem=[Q9B, Q9BV], decision=EACH_ITEM),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', Q(8, 'Distinguish between contest competition and scramble competition', 'each.'),
      [pt(S('(Results in) winner takes all (of a limited resource)'), 3, label=S('Contest:')),
       pt(S('(Results in) each gets some (of a limited resource)'), 3, label=S('Scramble:'))], 'bio-3-1',
      'contest-and-scramble-competition', at(10, '10.', '(a)', '(i)'), 6,
      decision=ROW_PRICED + ' Each kind of competition is priced "3", with the scheme\'s own label.'),
    T('10aii', 'Q10(a)(ii)', 'C', ask(8, 'Name a factor, other than competition, that controls wild populations.'),
      [pt(S('disease or parasitism or predation or hunting or reference to other named', 'environmental condition'), 3)],
      'bio-3-1', 'population-control-factors', at(10, '10.', '(a)', '(ii)'), 3),
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', q, [row], 'bio-3-1', concept, at(10, '10.', '(b)', f'({r})'), 7, stem=[Q10B],
      decision=ladder(10, '3(7) + 2(3)').replace('Q10', 'Q10(b)') + ' Five responses, one per observation.' + extra)
    for r, q, row, concept, extra in [
        ('i', Q(8, 'In a particular area the population of a predator', 'in the population of its main prey.'),
         pt(S('Different prey'), 7), 'predator-and-prey-numbers', ''),
        ('ii', ask(8, 'Mortality levels resulting from infection by a particular virus tend to decline over the years.'),
         pt(S('(Host) immunity develops or comment on natural selection (or described)',
              'or most virulent strains die off or vaccination'), 7), 'declining-virus-mortality', ''),
        ('iii', Q(8, 'Where some members of a species remain in the same general area', 'population.'),
         pt(S('Hazards encountered on migration (or particular example of a hazard)'), 7), 'hazards-of-migration', ''),
        ('iv', Q(8, 'There is a greater variety of herbaceous (non woody) plants',
                 'than in areas where grazing species are less plentiful.'),
         pt(S('(Grazing results in) reduced competition (or described)'), 7), 'grazing-and-plant-variety', ''),
        ('v', Q(8, 'In some species of migratory ducks', 'than those of the females.'),
         crit(S('Accept any biological knowledge-based statement that would provide a',
                'plausible rationale for a differential migratory pattern'), 7), 'differential-migration',
         ' The scheme prints only what earns the marks: one criterion row.')]
] + [
    T('10ci', 'Q10(c)(i)', 'C', Q(8, 'In relation to a study of an ecosystem distinguish clearly',
                                  'quantitative surveys by writing a sentence about each.'),
      [pt(S('What is present'), 3, label=S('Qualitative:')), pt(S('How many present'), 3, label=S('Quantitative:'))],
      'bio-3-1', 'qualitative-and-quantitative-surveys', at(10, '10.', '(c)', '(i)'), 6, decision=ROW_PRICED),
    T('10cii', 'Q10(c)(ii)', 'C', ask(8, 'How were you able to identify the different plants in the ecosystem that you '
                                        'investigated?'),
      [pt(S('Key(s) or illustrations'), 3)], 'bio-3-1', 'identifying-plants', at(10, '10.', '(c)', '(ii)'), 3),
    T('10ciii', 'Q10(c)(iii)', 'C', ask(8, 'Describe how you carried out a quantitative survey of the major plant '
                                          'species.'),
      [anyn(S('Quadrat / random / how random / count (or estimate) / many times /', 'calculate (or record)'), 3, 3)],
      'bio-3-1', 'quantitative-plant-survey', at(10, '10.', '(c)', '(iii)'), 9,
      decision='The scheme prints a quadrat menu and a transect menu joined by "OR", each "Any 3", beside one "3(3)": '
               'answer variants of one task, each a menu, claim three.'),
    T('10civ', 'Q10(c)(iv)', 'C', ask(8, 'Give two possible sources of error that may have arisen in the course of your '
                                        'survey.'),
      [anyn(S('Misidentification / non-random (quadrat distribution) / not enough times /',
              'miscount (or miscalculation)'), 2, 3)], 'bio-3-1', 'sources-of-error', at(10, '10.', '(c)', '(iv)'), 6,
      decision='"Any 2 2(3)" over five printed sources: a menu, claim two.'),
    T('11ai', 'Q11(a)(i)', 'C', ask(8, 'What do you understand by the term adverse external environment?'),
      [pt(S('Surroundings that are harmful to organism(s)'), 3)], 'bio-2-4', 'adverse-external-environment',
      at(11, '11.', '(a)', '(i)'), 3, decision=ROW_PRICED),
    T('11aii', 'Q11(a)(ii)', 'C', ask(8, 'Give two ways in which plants protect themselves from adverse external '
                                        'environments.'),
      [anyn(S('Thick cuticle / changed transpiration (rate) / leaf fall / toxic parts / thorns /', 'heat shock proteins'),
            2, 3)], 'bio-2-4', 'plant-protection', at(11, '11.', '(a)', '(ii)'), 6,
      decision='"Any 2 2(3)" over nine printed ways: a menu, claim two.'),
    T('11bi', 'Q11(b)(i)', 'C', Q11BI, [pt(S('(Plant) growth regulators or auxins (or other named group)'), 3)],
      'bio-2-4', 'growth-regulators', at(11, '11.', '(b)', '(i)'), 3),
    T('11bii1', 'Q11(b)(ii)1', 'C', Q11BII1, [pt(S('Meristems'), 3)], 'bio-2-4', 'meristems',
      at(11, '11.', '(b)', '(ii)', why=ITEM_ROMAN), 3, stem=[M('(i)', 8), Q11BI], decision=EACH_ITEM),
    T('11bii2', 'Q11(b)(ii)2', 'C', ask(8, '2. Give locations for two of these regions.'),
      [anyn(S('Root tip / shoot (or stem) tip / bud / embryo (or named part) / fruit',
              'between xylem and phloem (or vascular bundle)'), 2, 3)], 'bio-2-4', 'locations-of-meristems',
      at(11, '11.', '(b)', '(ii)', why=ITEM_ROMAN), 6, stem=[M('(i)', 8), Q11BI, Q11BII1],
      decision=EACH_ITEM + ' "Any 2 2(3)" over seven printed locations: a menu, claim two.'),
    T('11biii', 'Q11(b)(iii)', 'C', Q11BIII, [pt(S('Growth towards light'), 3)], 'bio-2-4', 'positive-phototropism',
      at(11, '11.', '(b)', '(iii)'), 3, qfig='q11biii-question',
      decision='The ask points at "the underlined term", which the text layer cannot show; the card\'s question is '
               'the printed ask, cropped.'),
    T('11biv', 'Q11(b)(iv)', 'C', ask(8, 'How does the plant benefit from this response?'),
      [pt(S('Increased photosynthesis'), 3)], 'bio-2-4', 'benefit-of-phototropism', at(11, '11.', '(b)', '(iv)'), 3,
      stem=[M('(iii)', 8), ask(8, 'Most plant shoots are positively phototropic.')]),
    T('11bv', 'Q11(b)(v)', 'C', ask(8, 'Explain the mechanism of response by a plant to a named external stimulus.'),
      [anyn(S('Named stimulus / diffusion of growth regulator / unequal distribution (of', 'results in bending'), 3, 3)],
      'bio-2-4', 'mechanism-of-a-tropism', at(11, '11.', '(b)', '(v)'), 9,
      decision='"Any 3 3(3)" over five printed points: a menu, claim three.'),
    T('11ci', 'Q11(c)(i)', 'C', ask(8, 'What is a hormone?'),
      [pt(S('A chemical messenger or product of endocrine (or ductless) gland'), 3)], 'bio-2-4', 'hormone',
      at(11, '11.', '(c)', '(i)'), 3),
    T('11cii', 'Q11(c)(ii)', 'C', ask(8, 'State two ways in which hormones are similar to the group of substances '
                                        'referred to in (b)(i).'),
      [anyn(S('Produced in one location / acts in different location / prolonged effect'), 2, 3)], 'bio-2-4',
      'hormones-and-growth-regulators', at(11, '11.', '(c)', '(ii)'), 6, stem=[M('(b)', 8), M('(i)', 8), Q11BI],
      decision='"Any 2 2(3)" over three printed points: a menu, claim two.'),
    T('11ciii1', 'Q11(c)(iii)1', 'C', Q11CIII1,
      [pt(S('When the level of a hormone (in the blood)'), 3), pt(S('controls (the production) of another (or itself)'), 3)],
      'bio-2-4', 'hormone-feedback', at(11, '11.', '(c)', '(iii)', why=ITEM_ROMAN), 6,
      decision=EACH_ITEM + ' The scheme prices its two lines "3" each.'),
    T('11ciii2', 'Q11(c)(iii)2', 'C', ask(8, '2. Give a brief account of the feedback mechanism for a named hormone.'),
      [crit(S('Named hormone'), 3), pt(S('inhibits (or causes production of) a named hormone'), 3)], 'bio-2-4',
      'feedback-mechanism', at(11, '11.', '(c)', '(iii)', why=ITEM_ROMAN), 6, stem=[Q11CIII1],
      decision=EACH_ITEM + ' The scheme prices its two lines "3" each; the first names no hormone.'),
    T('11civ', 'Q11(c)(iv)', 'C', ask(8, 'Describe one deficiency symptom of a named hormone.'),
      [crit(S('One deficiency symptom of a named hormone'), 3)], 'bio-2-4', 'hormone-deficiency',
      at(11, '11.', '(c)', '(iv)'), 3),
    T('12ai', 'Q12(a)(i)', 'C', ask(9, 'What is meant by the term excretion?'),
      [pt(S('Eliminating waste'), 3), pt(S('Made in the body'), 3)], 'bio-2-6', 'excretion',
      at(12, '12.', '(a)', '(i)'), 6, decision=ROW_PRICED + ' The two points are priced "3" each.'),
    T('12aii', 'Q12(a)(ii)', 'C', ask(9, 'Mention one method of excretion in flowering plants.'),
      [pt(S('Diffusion or leaf fall or transpiration or through lenticels (or through', 'stomata)'), 3)], 'bio-2-6',
      'excretion-in-plants', at(12, '12.', '(a)', '(ii)'), 3),
    T('12bi', 'Q12(b)(i)', 'C', Q12BI,
      [crit(S('Diagram:'), 3, note_sel=S('3, 0'), note_lead='The scheme marks this diagram')]
      + [pt(S('Labels: cortex, medulla, pelvis', piece=[2, i], psep=[': ', ', ']), 2,
            label=S('Labels: cortex, medulla, pelvis', piece=1, psep=': ')) for i in (1, 2, 3)],
      'bio-2-6', 'drawing-the-kidney', at(12, '12.', '(b)', '(i)'), 9,
      decision='The diagram is one priced item ("3, 0") with no printed content, and its three labels "3(2)", each '
               'cut at the scheme\'s own commas.'),
    T('12bii', 'Q12(b)(ii)', 'C', ask(9, 'Indicate clearly on your diagram where re-absorption takes place.'),
      [crit(S('Position of reabsorption indicated'), 3)], 'bio-2-6', 'site-of-reabsorption',
      at(12, '12.', '(b)', '(ii)'), 3, stem=[M('(i)', 9), Q12BI]),
    T('12biii1', 'Q12(b)(iii)1', 'C', Q12BIII1, [pt(S('*Renal artery'), 3)], 'bio-2-6', 'renal-artery',
      at(12, '12.', '(b)', '(iii)', why=ITEM_ROMAN), 3, decision=EACH_ITEM),
    T('12biii2', 'Q12(b)(iii)2', 'C', ask(9, '2. From which blood vessel does the blood vessel referred to in (iii)1 '
                                            'arise?'),
      [pt(S('*Aorta'), 3)], 'bio-2-6', 'aorta', at(12, '12.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q12BIII1],
      decision=EACH_ITEM),
    T('12biv', 'Q12(b)(iv)', 'C', ask(9, 'In which cavity of the body are the kidneys located?'),
      [pt(S('*Abdominal (cavity) or *Abdomen'), 3)], 'bio-2-6', 'kidneys-in-the-abdomen', at(12, '12.', '(b)', '(iv)'),
      3),
    T('12bv', 'Q12(b)(v)', 'C', ask(9, 'Name one substance, other than water, excreted in the urine.'),
      [pt(S('Urea or salt or uric acid'), 3)], 'bio-2-6', 'substances-in-urine', at(12, '12.', '(b)', '(v)'), 3),
    T('12bvi', 'Q12(b)(vi)', 'C', ask(9, 'Give a feature of the kidney which indicates that it is an exocrine gland.'),
      [pt(S('Has ducts or does not produce hormones'), 3)], 'bio-2-6', 'kidney-as-exocrine-gland',
      at(12, '12.', '(b)', '(vi)'), 3),
    T('12ci1', 'Q12(c)(i)1', 'C', ask(9, '1. Name the parts numbered 1 to 6.'),
      [pt(S(ln, piece=[2, 1], psep=[' = ', ';']), 1, label=S(ln, piece=1, psep=' = ')) for ln in NEPHRON], 'bio-2-6',
      'parts-of-the-nephron', at(12, '12.', '(c)', '(i)', why=ITEM_ROMAN), 6, stem=[Q12C], fig='q12c-nephron',
      decision=EACH_ITEM + ' "6(1)": the six parts, each its own row with its printed number, cut at the scheme\'s '
                           'own "=" and semicolon.'),
    T('12ci2', 'Q12(c)(i)2', 'C', ask(9, '2. Indicate clearly by number where filtration takes place.'),
      [pt(S('*1 or *2 or *1 and 2*'), 3)], 'bio-2-6', 'site-of-filtration',
      at(12, '12.', '(c)', '(i)', why=ITEM_ROMAN), 3, stem=[Q12C], fig='q12c-nephron',
      decision=EACH_ITEM + ' The answer is a number of the diagram.'),
    T('12ci3', 'Q12(c)(i)3', 'C', ask(9, '3. Name the hormone associated with changing the permeability of the structure '
                                        'at 7.'),
      [pt(S('Anti-diuretic hormone or ADH or vasopressin'), 3)], 'bio-2-6', 'adh',
      at(12, '12.', '(c)', '(i)', why=ITEM_ROMAN), 3, stem=[Q12C], fig='q12c-nephron', decision=EACH_ITEM),
] + [
    T(f'12c{r}', f'Q12(c)({r})', 'C',
      [Q(9, '1. Would you consider this to be normal?', '1. Would you consider this to be normal?', after=lead),
       Q(9, '2. Explain your answer.', '2. Explain your answer.', after=lead, br=True)],
      [pt(S('*No'), 3, **note), pt(S(why), 3)], 'bio-2-6', concept, at(12, '12.', '(c)', f'({r})'), 6,
      stem=[ask(9, lead)], decision=decision)
    for r, lead, why, concept, note, decision in [
        ('ii', 'A sample of urine was found to contain protein.', 'Protein molecules too big (to pass into the filtrate)',
         'protein-in-urine',
         {'note_sel': S('Note: ‘Yes’ correctly qualified (e.g. low level or pregnancy) for 6m')},
         'The answer and its explanation are priced "3" each; the scheme\'s note under them prices a qualified "Yes" '
         'at 6 for both items together, so the two items are one card, the note on its first row.'),
        ('iii', 'A sample of urine was found to contain glucose.', 'Glucose (in the filtrate should have been) reabsorbed',
         'glucose-in-urine', {},
         'The answer and its explanation are priced "3" each: one card for both items, as (ii).')]
] + [
    T('13ai', 'Q13(a)(i)', 'C', ask(10, 'What is meant by the term evolution?'),
      [anyn(S('Inheritable change within a population (or species) / in response to', 'over time'), 2, 3)],
      'bio-1-5', 'evolution', at(13, '13.', '(a)', '(i)'), 6,
      decision='"Any 2 2(3)" over four printed points: a menu, claim two.'),
    T('13aii', 'Q13(a)(ii)', 'C', ask(10, 'Name either of the scientists responsible for the Theory of Natural Selection.'),
      [pt(S('Darwin or Wallace'), 3)], 'bio-1-5', 'darwin-and-wallace', at(13, '13.', '(a)', '(ii)'), 3),
    T('13bi', 'Q13(b)(i)', 'C', Q(10, 'What is the significance of the fact that the two allele pairs',
                                  'chromosome pairs?'),
      [pt(S('Independent assortment (or described) can occur or more variation (in', 'offspring)'), 3)], 'bio-1-4',
      'independent-assortment', at(13, '13.', '(b)', '(i)'), 3, stem=[Q13B]),
    T('13bii1', 'Q13(b)(ii)1', 'C', Q13BII1,
      [pt(S(g), 3, **({'note_sel': EXCESS} if i == 0 else {})) for i, g in enumerate(('RrTt', 'Rrtt', 'rrTt', 'rrtt'))],
      'bio-1-4', 'dihybrid-cross-genotypes', at(13, '13.', '(b)', '(ii)', why=ITEM_ROMAN), 12,
      stem=[Q13B, Q13BII],
      decision=EACH_ITEM + ' "4(3)": the four genotypes, each its own cell of the scheme\'s table. The scheme prints '
                           'them in two symbol sets joined by "OR": answer variants of one task.'),
    T('13bii2', 'Q13(b)(ii)2', 'C', ask(10, '2. For each of your answers, state the phenotype that would result.'),
      [pt(S(p), 3, **({0: {'note_sel': S('Phenotype must match a correct genotype')},
                        1: {'note_sel': EXCESS}}.get(i, {})))
       for i, p in enumerate(('pink + tall', 'pink + short', 'white + tall', 'white + short'))],
      'bio-1-4', 'dihybrid-cross-phenotypes', at(13, '13.', '(b)', '(ii)', why=ITEM_ROMAN), 12,
      stem=[Q13B, Q13BII, Q13BII1],
      decision=EACH_ITEM + ' "4(3)": the four phenotypes, each its own cell of the scheme\'s table; the scheme\'s '
                           'two directions printed under them are the first two rows\' notes.'),
] + [
    T(f'13c{r}', f'Q13(c)({r})', 'C', term(10, pair),
      [pt(S(*a1), 3, label=S(l1)), pt(S(*a2), 3, label=S(l2))], 'bio-1-4', concept, at(13, '13.', '(c)', f'({r})'), 6,
      stem=[Q13C], decision='Each term of the pair is priced "3", with the scheme\'s own label.')
    for r, pair, l1, a1, l2, a2, concept in [
        ('i', 'Gene and allele.', 'Gene:', ('a section of DNA that codes for one polypeptide (or',
                                            'protein or trait) or unit of heredity'),
         'Allele:', ('(an alternative) form of a gene',), 'gene-and-allele'),
        ('ii', 'Homozygous and heterozygous.', 'Homozygous:', ('identical alleles',), 'Heterozygous:',
         ('different alleles (of a gene)',), 'homozygous-and-heterozygous'),
        ('iii', 'Genotype and phenotype.', 'Genotype:', ('genetic makeup or genes (alleles) present',), 'Phenotype:',
         ('the expression of the genotype (and environment) or', 'physical makeup (or appearance)'),
         'genotype-and-phenotype'),
        ('iv', 'Linkage and sex linkage.', 'Linkage:', ('genes on the same chromosome',), 'Sex-linkage:',
         ('(located) on sex-chromosome or on X- chromosome or', 'on Y-chromosome'), 'linkage-and-sex-linkage')]
] + [
    # Q14(a)
    T('14ai', 'Q14(a)(i)', 'C', ask(11, 'Suggest a suitable plant for such an investigation.'),
      [pt(S('Aquatic plant or named (e.g. Elodea)'), 3)], 'bio-2-2', 'plant-for-photosynthesis-investigation',
      at(14, '14.', '(a)', '(i)'), 3, stem=Q14A, fig='q14a-graph', decision=ROW_PRICED),
    T('14aii', 'Q14(a)(ii)', 'C', ask(11, 'How was the rate of photosynthesis measured?'),
      [pt(S('Counted bubbles (or measured volume) / per unit time', piece=i), 3) for i in (1, 2)], 'bio-2-2',
      'measuring-photosynthesis-rate', at(14, '14.', '(a)', '(ii)'), 6, stem=Q14A, fig='q14a-graph',
      decision='The scheme prints two ways joined by "OR", each two points cut at its own solidus, beside one "2(3)": '
               'answer variants of one task.'),
    T('14aiii', 'Q14(a)(iii)', 'C', Q14AIII,
      [pt(S('Light (if CO2 addressed) or CO2 (if light addressed) or temperature'), 3)], 'bio-2-2',
      'factor-kept-constant', at(14, '14.', '(a)', '(iii)'), 3, stem=Q14A, fig='q14a-graph'),
    T('14aiv', 'Q14(a)(iv)', 'C', ask(11, 'Explain how you would keep constant the factor referred to in (iii).'),
      [pt(S('Fixed lamp distance (or wattage) or NaHCO3 or water bath (or described)'), 3)], 'bio-2-2',
      'keeping-a-factor-constant', at(14, '14.', '(a)', '(iv)'), 3, stem=Q14A + [M('(iii)', 11), Q14AIII],
      fig='q14a-graph'),
    T('14av', 'Q14(a)(v)', 'C', ask(11, 'Why is it necessary to keep that factor constant?'),
      [pt(S('To ensure that any change is not due to that factor'), 3)], 'bio-2-2', 'why-keep-a-factor-constant',
      at(14, '14.', '(a)', '(v)'), 3, stem=Q14A + [M('(iii)', 11), Q14AIII], fig='q14a-graph'),
    T('14avi1', 'Q14(a)(vi)1', 'C', Q14AVI1,
      [pt(S('It does not increase any further or levels off'), 3, label=S('A')),
       pt(S('It increases or does not level off'), 3, label=S('B'))], 'bio-2-2', 'rate-at-x',
      at(14, '14.', '(a)', '(vi)', why=ITEM_ROMAN), 6, stem=Q14A, fig='q14a-graph',
      decision=EACH_ITEM + ' A and B are priced "3" each, each row with the scheme\'s own letter.'),
    T('14avi2', 'Q14(a)(vi)2', 'C', Q(11, '2.', 'Give a reason for each answer.', after='B. carried out at 35°C?'),
      [pt(S('Temperature is limiting or photosynthesis can not go any faster', '(at that temperature)'), 3,
          label=S('A', after='It increases or does not level off')),
       pt(S('Temperature is not limiting or increased temperature allows', 'greater rate'), 3,
          label=S('B', after='(at that temperature)'))], 'bio-2-2', 'temperature-as-a-limiting-factor',
      at(14, '14.', '(a)', '(vi)', why=ITEM_ROMAN), 6, stem=Q14A + Q14AVI1, fig='q14a-graph',
      decision=EACH_ITEM + ' A\'s reason and B\'s are priced "3" each, each row with the scheme\'s own letter.'),
    # Q14(b)
    T('14bi', 'Q14(b)(i)', 'C', ask(11, 'What is meant by the term metabolism?'),
      [pt(S('(All) the chemical reactions in living cells'), 3)], 'bio-2-1', 'metabolism', at(14, '14.', '(b)', '(i)'),
      3),
    T('14bii', 'Q14(b)(ii)', 'C', Q(11, '“Enzymes are essential for metabolism”.', 'Explain why this statement is true.'),
      [pt(S('(Enzymes) are catalysts'), 3), pt(S('(Enzymes) control rate of (metabolic) reactions'), 3)], 'bio-2-1',
      'enzymes-and-metabolism', at(14, '14.', '(b)', '(ii)'), 6, decision='The two points are priced "3" each.'),
] + [
    T(f'14biii{n}', f'Q14(b)(iii){n}', 'C', ask(11, f'{n}. {case}'), [pt(S('*Anabolic', nth=n), 3)], 'bio-2-1',
      concept, at(14, '14.', '(b)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q14BIII],
      decision=EACH_ITEM + ' "3(3)": one answer per case, the scheme\'s n-th "*Anabolic" for the n-th case.')
    for n, case, concept in [(1, 'Protein synthesis.', 'protein-synthesis-is-anabolic'),
                             (2, 'Conversion of ADP to ATP.', 'atp-formation-is-anabolic'),
                             (3, 'Reactions in which product molecules are larger than substrate molecules.',
                              'larger-products-is-anabolic')]
] + [
    T('14biv', 'Q14(b)(iv)', 'C', ask(11, 'State one way by which an enzyme may be denatured.'),
      [pt(S('High temperature or high (or low) pH or agitation (or described) or high', 'salinity or alcohol'), 3)],
      'bio-2-1', 'denaturing-an-enzyme', at(14, '14.', '(b)', '(iv)'), 3),
    T('14bv', 'Q14(b)(v)', 'C', ask(11, 'Give two features of a denatured enzyme.'),
      [pt(S('Changed structure'), 3), pt(S('Loss of function'), 3)], 'bio-2-1', 'denatured-enzyme',
      at(14, '14.', '(b)', '(v)'), 6, decision='The two features are priced "3" each.'),
    T('14bvi', 'Q14(b)(vi)', 'C', Q(11, 'Apart from carbon, hydrogen and oxygen, there is one other element',
                                    'Name that element.'),
      [pt(S('Nitrogen'), 3)], 'bio-2-1', 'nitrogen-in-enzymes', at(14, '14.', '(b)', '(vi)'), 3),
    # Q14(c)
    T('14ci', 'Q14(c)(i)', 'C', ask(11, 'State the precise location of the cell membrane in plant cells.'),
      [pt(S('Immediately inside the cell wall'), 3)], 'bio-1-3', 'cell-membrane-location',
      at(15, '14.', '(c)', '(i)'), 3),
    T('14cii', 'Q14(c)(ii)', 'C', Q14CII, [pt(S('*Eukaryotic'), 3)], 'bio-1-3', 'eukaryotic',
      at(15, '14.', '(c)', '(ii)'), 3),
    T('14ciii', 'Q14(c)(iii)', 'C', ask(11, 'What corresponding term is used to describe bacterial cells?'),
      [pt(S('*Prokaryotic'), 3)], 'bio-1-3', 'prokaryotic', at(15, '14.', '(c)', '(iii)'), 3,
      stem=[M('(ii)', 11), Q14CII]),
    T('14civ', 'Q14(c)(iv)', 'C', ask(11, 'The cell membrane is described as being selectively permeable. What does this '
                                        'mean?'),
      [pt(S('Only some substances are allowed through'), 3)], 'bio-1-3', 'selective-permeability',
      at(15, '14.', '(c)', '(iv)'), 3),
    T('14cv', 'Q14(c)(v)', 'C', ask(11, 'Why is diffusion alternatively known as passive transport?'),
      [pt(S('No (or little) energy (or ATP) required'), 3)], 'bio-2-6', 'passive-transport',
      at(15, '14.', '(c)', '(v)'), 3),
    T('14cvi', 'Q14(c)(vi)', 'C', ask(11, 'Osmosis may be described as “a special case of diffusion”. Explain why.'),
      [pt(S('Movement of water or (osmosis) requires a membrane'), 3)], 'bio-2-6', 'osmosis-as-diffusion',
      at(15, '14.', '(c)', '(vi)'), 3),
    T('14cvii', 'Q14(c)(vii)', 'C', ask(11, 'Describe, with the aid of a labelled diagram, how you demonstrated osmosis '
                                          'in the laboratory.'),
      [pt(S('Diagram: Container + 2 solutions separated by a membrane'), 3, kind='criterion', note_sel=S('(3,0)'),
          note_lead='The scheme marks this diagram')]
      + [pt(S(*OSMOSIS_LABELS, piece=i), 1, **({} if i == 1 else {'label': S(*OSMOSIS_LABELS, piece=1, psep=':')}))
         for i in (1, 2, 3)]
      + [crit(S('Result: Shown in diagram or stated'), 3)],
      'bio-2-6', 'demonstrating-osmosis', at(15, '14.', '(c)', '(vii)'), 9,
      decision='The diagram is one priced item ("3,0"), its three labels "3(1)", cut at the scheme\'s own solidus, '
               'and the result "3".'),
    T('14cviii', 'Q14(c)(viii)', 'C', ask(11, 'Name the structure by which Amoeba gets rid of excess water that has '
                                            'entered by osmosis.'),
      [pt(S('Contractile vacuole'), 3)], 'bio-2-6', 'contractile-vacuole', at(15, '14.', '(c)', '(viii)'), 3),
    # Q15(a)
    T('15ai1', 'Q15(a)(i)1', 'C', ask(12, '1. Name the structures labelled A, B, C.'), [eq(ln, 2) for ln in EAR],
      'bio-2-4', 'parts-of-the-ear', at(16, '15.', '(a)', '(i)', why=ITEM_ROMAN), 6, stem=[Q15AI], fig='q15a-ear',
      labels=EAR_KEY, decision=EACH_ITEM + ' The three parts are priced "2" each, each its own row with its letter.'),
    T('15ai2', 'Q15(a)(i)2', 'C', ask(12, '2. Give the functions of parts D and E.'),
      [eq('D = posture or balance', 3), eq('E = pressure equalisation', 3)], 'bio-2-4', 'functions-of-ear-parts',
      at(16, '15.', '(a)', '(i)', why=ITEM_ROMAN), 6, stem=[Q15AI], fig='q15a-ear', labels=EAR_NAMED,
      decision=EACH_ITEM + ' D\'s and E\'s functions are priced "3" each. The scheme never names D or E, so the '
                           'card keys the letters it does name, none asked.'),
    T('15ai3', 'Q15(a)(i)3', 'C', ask(12, '3. Which letters denote the parts of the ear in which nerve impulses are '
                                        'generated?'),
      [pt(S('A', after='E = pressure equalisation'), 3), pt(S('D', after='E = pressure equalisation'), 3)],
      'bio-2-4', 'where-the-ear-makes-impulses', at(16, '15.', '(a)', '(i)', why=ITEM_ROMAN), 6, stem=[Q15AI],
      fig='q15a-ear', decision=EACH_ITEM + ' The two letters are priced "3" each; the answers are letters of the '
                                           'diagram.'),
    T('15aii', 'Q15(a)(ii)', 'C', ask(12, 'In what part of the eye are nerve impulses generated?'),
      [pt(S('Retina or named part of retina'), 3)], 'bio-2-4', 'retina', at(16, '15.', '(a)', '(ii)'), 3),
    T('15aiii', 'Q15(a)(iii)', 'C', ask(12, 'Suggest one way by which the ear may be protected.'),
      [pt(S('Skull (or bone) or wax or wear ear protection or avoid noisy environments'), 3)], 'bio-2-4',
      'protecting-the-ear', at(16, '15.', '(a)', '(iii)'), 3),
    T('15aiv', 'Q15(a)(iv)', 'C', ask(12, 'Explain how a corrective measure for a named defect of hearing or vision '
                                        'works.'),
      [crit(S('Named defect'), 3), crit(S('Corrective measure or how this works to correct named defect'), 3)],
      'bio-2-4', 'correcting-a-defect', at(16, '15.', '(a)', '(iv)'), 6,
      decision='The defect and its correction are priced "3" each; the scheme names neither.'),
    # Q15(b)
    T('15bi', 'Q15(b)(i)', 'C', Q15BI, [pt(S('*Xylem'), 3)], 'bio-2-6', 'xylem', at(16, '15.', '(b)', '(i)'), 3),
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', ask(12, q), [pt(S(ans), 3)], 'bio-2-6', concept, at(16, '15.', '(b)', f'({r})'),
      3, stem=[M('(i)', 12), Q15BI])
    for r, q, ans, concept in [
        ('ii', 'Give one way in which this tissue is adapted for the transport of water.',
         'Narrow or lignified (or rigid) or continuous lumen or wettable', 'xylem-adaptations'),
        ('iii', 'Give a precise location of this tissue in the stem.', 'In vascular bundles or next to phloem',
         'location-of-xylem'),
        ('iv', 'State another function of the tissue referred to in (i).', 'Support or other transport function',
         'other-function-of-xylem')]
] + [
    T('15bv', 'Q15(b)(v)', 'C', Q(12, 'The cohesion-tension model of transport attempts to explain water movement in',
                                  'Name this force.'),
      [pt(S('*Gravity'), 3)], 'bio-2-6', 'gravity', at(16, '15.', '(b)', '(v)'), 3),
    T('15bvi', 'Q15(b)(vi)', 'C', ask(12, 'Describe the principal features of the cohesion-tension model.'),
      [anyn(S('Water (molecules) stick together / (due to) H-bonding / continuous chain', 'water up'), 3, 3)],
      'bio-2-6', 'cohesion-tension-model', at(16, '15.', '(b)', '(vi)'), 9,
      decision='"Any three 3(3)" over five printed features: a menu, claim three.'),
    T('15bvii', 'Q15(b)(vii)', 'C', ask(12, 'Name the two scientists mainly associated with the cohesion-tension model of '
                                          'transport.'),
      [pt(S('*Dixon'), 3), pt(S('*Joly'), 3)], 'bio-2-6', 'dixon-and-joly', at(16, '15.', '(b)', '(vii)'), 6,
      decision='The two scientists are priced "3" each.'),
    # Q15(c)
    T('15ci', 'Q15(c)(i)', 'C', ask(12, 'Give the name and state a function of the part labelled A.'),
      [eq('A = rhizoids', 3), eq('Function = digestion or secretion or absorption or anchorage', 3)], 'bio-3-2',
      'rhizoids', at(17, '15', '(c)', '(i)'), 6, stem=[Q15C], fig='q15c-rhizopus', labels=RHIZOPUS_A,
      decision=ROW_PRICED + ' The name and the function are priced "3" each.'),
    T('15cii', 'Q15(c)(ii)', 'C', ask(12, 'Name part B and explain why the reproduction associated with it is asexual.'),
      [eq('B = sporangium', 3),
       pt(S('(the spores all develop from) one parent or no gametes involved'), 3,
          note_sel=S('(Reproduction is asexual because)'))], 'bio-3-2', 'sporangium',
      at(17, '15', '(c)', '(ii)'), 6, stem=[Q15C], fig='q15c-rhizopus', labels=RHIZOPUS_B,
      decision='The name and the reason are priced "3" each; the scheme\'s bracketed lead-in to the reason is that '
               'row\'s note.'),
    T('15ciii1', 'Q15(c)(iii)1', 'C', ask(12, '1. What does the term saprophytic mean?'),
      [pt(S('Feeding on dead matter'), 3)], 'bio-3-2', 'saprophytic', at(17, '15', '(c)', '(iii)', why=ITEM_ROMAN), 3,
      stem=[Q15CIII], decision=EACH_ITEM),
    T('15ciii2', 'Q15(c)(iii)2', 'C', ask(12, '2. Explain the importance of saprophytic nutrition in the overall scheme '
                                            'of nature.'),
      [pt(S('Breakdown of dead matter or breakdown of organic matter or', 'recycling'), 3)], 'bio-3-2',
      'importance-of-saprophytes', at(17, '15', '(c)', '(iii)', why=ITEM_ROMAN), 3, stem=[Q15CIII],
      decision=EACH_ITEM),
    T('15civ', 'Q15(c)(iv)', 'C', Q(12, 'Saprophytic nutrition is a form of heterotrophic nutrition.',
                                    'What does the term heterotrophic mean?'),
      [pt(S('Obtains food from other organisms or does not make its own food'), 3)], 'bio-3-2', 'heterotrophic',
      at(17, '15', '(c)', '(iv)'), 3),
    T('15cv', 'Q15(c)(v)', 'C', ask(12, 'Name another form of nutrition employed by some fungi.'),
      [pt(S('Parasitic'), 3)], 'bio-3-2', 'parasitic-fungi', at(17, '15', '(c)', '(v)'), 3,
      stem=[M('(iii)', 12), Q15CIII]),
    T('15cvi', 'Q15(c)(vi)', 'C', ask(12, 'Give two examples of harmful members of the kingdom Fungi.'),
      [pt(S('Any two correct'), 6, kind='criterion', units=[3, 3], note=NO_ANSWER)], 'bio-3-2', 'harmful-fungi',
      at(17, '15', '(c)', '(vi)'), 6,
      decision='"Any two correct 2(3)": the scheme names no fungus; one criterion row worth its two 3s.'),
]

ANSWER_VARIANTS = {
    '10ciii': [
        ('quadrat', 'Quadrat',
         [anyn(S('Quadrat / random / how random / count (or estimate) / many times /', 'calculate (or record)'), 3, 3)]),
        ('transect', 'Transect',
         [anyn(S('Transect / stations / intervals / count (or estimate) / how (counted) / result', 'described'), 3, 3)]),
    ],
    '13bii1': [
        ('r-and-r', 'R and r for flower colour',
         [pt(S(g), 3, **({'note_sel': EXCESS} if i == 0 else {})) for i, g in enumerate(('RrTt', 'Rrtt', 'rrTt', 'rrtt'))]),
        ('r-and-w', 'R and W for flower colour',
         [pt(S(g), 3, **({'note_sel': EXCESS} if i == 0 else {})) for i, g in enumerate(('RWTt', 'RWtt', 'WWTt', 'WWtt'))]),
    ],
    '14aii': [
        ('bubbles', 'Counting bubbles',
         [pt(S('Counted bubbles (or measured volume) / per unit time', piece=i), 3) for i in (1, 2)]),
        ('datalogging', 'Datalogging',
         [pt(S('datalogging / named sensor (or mention of time)', piece=i), 3) for i in (1, 2)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q4b-graph': ('paper', 3, (125, 478, 465, 655), SEC, [],
        'Line graph on a squared grid. Vertical axis: mouth temperature/°C, from 35 to 38. Horizontal axis: time '
        'over three days, labelled DAY 1, DAY 2 and DAY 3, each day marked 4, 8, 12 a.m. then 4, 8, 12 p.m. A '
        'dashed horizontal line is drawn at 37. On days 1 and 2 the plotted line follows the same pattern: from '
        'about 36.5 at the start it falls to about 36 soon after midnight and stays near 36 until about 8 a.m., '
        'rises to a small peak just below 37 before noon, dips a little after noon, climbs above 37 in the '
        'afternoon to a flat peak just above 37.5 around 8 p.m., then falls steeply through the night. After the '
        'second evening it falls further, to a trough just below 36 around 4 a.m. on day 3, then rises above 37 '
        'by about noon and wavers between 37 and about 37.4 for the rest of day 3.',
        False),
    'q5b-canal': ('paper', 4, (150, 178, 440, 345), SEC, ['W', 'X'],
        'Outline drawing. A large oval at the top is labelled X; a narrow tube runs down from its underside, '
        'labelled bile duct. Lower down this tube is joined by a second tube coming from the left end of a long '
        'narrow oval at the lower right, labelled pancreas, and the joined tube opens into the inner side of a '
        'curved C-shaped tube on the left, labelled W, whose two ends are drawn dotted where the tube continues '
        'beyond the drawing.',
        False),
    'q11biii-question': ('paper', 8, (104, 503.8, 462, 516.8), SEC, [],
        'Part (iii) of Question 11(b) as printed, on one line, with the words positively phototropic underlined.',
        False),
    'q12c-nephron': ('paper', 9, (150, 186, 480, 450), SEC, [],
        'Shaded drawing of a nephron and its blood vessels, with nine numbered arrows. On the left a dark and a '
        'pale vessel run upward from two curved vessels at the bottom left. A thin vessel leads from the left '
        'into a dark tangled knot inside a rounded cup: arrow 3 points to that thin vessel, arrow 2 to the dark '
        'knot, and arrow 1, pointing up from below, to the lower edge of the cup. Arrow 4 points to a thin vessel '
        'leaving the knot upwards. A tube leaves the cup and coils at the top centre, where arrow 5 points; from '
        'there a long hairpin loop runs down to the bottom and back up, with arrow 8 at the bend of the loop and '
        'arrow 9 at a vessel of the network of thin vessels wrapped around it. Arrow 6 points to a second coiled '
        'tube at the top right, which joins a tall branched tube on the far right, at which arrow 7 points.',
        False),
    'q14a-graph': ('paper', 11, (110, 106, 480, 330), SEC, ['X'],
        'Graph with no scale. Vertical axis: rate of photosynthesis, with an arrow pointing up. Horizontal axis: '
        'light intensity or carbon dioxide concentration, with an arrow pointing right. A straight line rises '
        'from the origin. At a point marked X a horizontal line branches off to the right, labelled 25°C; the '
        'rising line continues higher, then turns into a second horizontal line to the right, labelled 35°C.',
        False),
    'q15a-ear': ('paper', 12, (160, 60, 485, 260), SEC, ['A', 'B', 'C', 'D', 'E', 'F'],
        'Drawing of the human ear in section: the outer ear on the left and a canal running right into the '
        'head. Label B points to a shaded oval closing the inner end of the canal; F to small dark irregular '
        'shapes just beyond it; D to the top of a group of loops above them; A to a coiled shape on the right; '
        'C to a dark band running off to the upper right from beside the coil; E to a narrow channel running '
        'down and to the right below the coil.',
        False),
    'q15c-rhizopus': ('paper', 12, (185, 499, 445, 669), SEC, ['A', 'B'],
        'Line drawing of part of a fungal mycelium: a long double-lined thread runs across the middle. An upright '
        'thread rises from it to a round head filled with small oval bodies, labelled B. Below the horizontal '
        'thread, branched finger-like outgrowths spread downward; two lines from the label A point to them. On '
        'the right a short upright branch with a rounded tip rises from the thread, with smaller branched '
        'outgrowths beneath it.',
        False),
}
