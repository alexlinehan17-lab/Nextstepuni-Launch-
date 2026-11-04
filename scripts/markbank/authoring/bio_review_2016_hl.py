"""Biology 2016 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-25), every page rendered and read:
  * The 2016 paper is one booklet (M44), 16 pages: p1 cover and instructions,
    p2-p6 Section A Questions 1-6, p7-p9 Section B Questions 7-9, p10-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book. No acknowledgements
    page: the Q3 and Q5 drawings carry no credit.
  * The marking scheme, 20 pages: p1 cover, p2 note, p3 introduction,
    cancelled answers and surplus answers, p4 surplus answers (continued) and
    conventions, p5-p18 Questions 1-15, p19 "Blank Page", p20 back cover.

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c). Every printed ask is carded.

Tariffs. Section A is ordered splits, carded at their first rate: Q1 "2(7) +
3(2) i.e. best five answers from (a) - (f)" (six parts, the best five
priced), Q2 "2(3) + 7(2)", Q3 and Q6 "2(5) + 5(2)", Q4 and Q5 "5(3) +
5(1)". Section B prints "2(3)" for each (a) (two parts at 3, priced on their
own) and "4(4) + 4(2)" for each (b). Section C prints a mark against every
row ("3", "2(3)", "3(3)", Q13(b)(i)'s labels "6(2)", Q15(a)(i)'s drawings
"3, 0" and labels "3(1)", Q15(c)(ii)'s recognitions "3, 2, 0"), so every
Section C task is priced row by row against the paper's (9), (27), (24) and
Q14/Q15's (30, 30).

Every printed answer fits a per-response tariff, so no part is carded whole.

Alternatives the scheme prints as matched sets joined by "OR" are answer
variants of one task: Q4(b)(iii) the female's two boxes, Q5(d) the two
fates, Q11(b)(iv) "Water split/ using light" or "Photolysis/ of water",
Q15(b)(i) each change with its days. Q11(c)(iii)'s "Any one further point
from 1 or from 2." is carded as two variants, the further point taken from
the Krebs cycle list or from the electron transport list.

Printed choices the scheme marks differently per option are routes:
Q13(c)(iv) carnivores or herbivores, Q15(b)(v) oestrogen or progesterone.

The census reader welded Q13(b)(ii) onto the end of Q13(b)(i) (the page sets
"(ii)" on its own line under the bold row of parts to label); a gated
WELDED_HEADS entry in paper.py splits it, which takes the census from 122
leaves to the paper's 123.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L, G

YEAR, LEVEL = 2016, 'hl'
REVIEWED_AT = '2026-10-25'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2016-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': 'afbf44d46e589cadc5727dceba18531395aac3403b4cca700e17e823cc353e8d',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2016-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '798683962ed9508d51fd735aba732d7f85ad0336c4fc178e8961b4e5537f81b7',
               'pages': 20},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'conventions',
               **{p: 'marking' for p in range(5, 19)}, 19: 'blank', 20: 'back-cover'},
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
    **{(n, 'a'): 6 for n in (7, 8, 9)},   # p7: "Part (a) carries 6 marks"
    **{(n, 'a'): 9 for n in (10, 11, 12, 13)},   # the paper's "(9)"
    **{(n, 'b'): 27 for n in (10, 11, 12, 13)},   # "(27)"
    **{(n, 'c'): 24 for n in (10, 11, 12, 13)},   # "(24)"
    **{(n, x): 30 for n in (14, 15) for x in 'abc'},   # "(30, 30)"
}
LADDERS = {
    # Q1: six parts, the best five priced "2(7) + 3(2)".
    1: _ladder('2(7) + 3(2)', responses=6),
    2: _ladder('2(3) + 7(2)'), 3: _ladder('2(5) + 5(2)'), 4: _ladder('5(3) + 5(1)'),
    5: _ladder('5(3) + 5(1)'), 6: _ladder('2(5) + 5(2)'),
    # Section B (a) "2(3)" is two parts at 3, priced on their own beside (b)'s ladder.
    **{(n, 'b'): _ladder('4(4) + 4(2)') for n in (7, 8, 9)},
}

CHECKSUMS = {
    1: {7: 6}, 2: {3: 9}, 3: {5: 7}, 4: {3: 10}, 5: {3: 10}, 6: {5: 7},
    **{(n, 'a'): {3: 2} for n in (7, 8, 9)}, **{(n, 'b'): {4: 8} for n in (7, 8, 9)},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 9}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 9}, (11, 'c'): {3: 8},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 9}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 3}, (13, 'b'): {2: 6, 3: 5}, (13, 'c'): {3: 8},
    (14, 'a'): {3: 10}, (14, 'b'): {3: 10}, (14, 'c'): {3: 10},
    (15, 'a'): {3: 9, 1: 3}, (15, 'b'): {3: 10}, (15, 'c'): {3: 10},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'the following', 'Q1 "Explain five of the following terms": best five of (a)-(f); each part is its '
                                  'own card on the "2(7) + 3(2)" ladder.'),
    ('paper', 4, 'the following', 'Q4(a) "In each of the following three crosses": every cross asked, one card each.'),
    ('paper', 4, 'or', 'Q4(b)(ii) "human females or human males": the answer options.'),
    ('paper', 6, 'any two', 'Q6(d) "Give any two other changes": a bounded menu, claim two.'),
    ('paper', 7, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 7, 'either', 'Q7(b)(i) "either Benedict\'s or Fehling\'s test": either test; one control answer.'),
    ('paper', 7, 'or', 'Q7(b)(i), same choice.'),
    ('paper', 7, 'the following', 'Q7(b)(ii) "In each of the following instances": one card per numbered item.'),
    ('paper', 7, 'or', 'Q7(b)(iii) "human cheek cells or other animal cells": either; marked on the same rows.'),
    ('paper', 8, 'the following', 'Q8(a) lead-in: every part asked.'),
    ('paper', 8, 'or', 'Q8(a)(ii) "(or temple, or neck)": description.'),
    ('paper', 8, 'or', 'Q8(a)(ii), same description.'),
    ('paper', 8, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 8, 'or', 'Q8(b) "breathing rate or pulse rate": either investigation; marked on the same rows.'),
    ('paper', 8, 'or', 'Q8(b)(iii) "two curves or plots": description.'),
    ('paper', 8, 'or', 'Q8(b)(iv) "breathing rate or pulse rate": description.'),
    ('paper', 9, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 9, 'or', 'Q9(b) "starch agar or skimmed milk (protein) agar": either; marked on the same rows, '
                       'which the scheme matches to the substrate named.'),
    ('paper', 10, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 10, 'the following', 'Q10(b)(i) "each of the following": one card per numbered item.'),
    ('paper', 11, 'the following', 'Q11(b) lead-in: every part asked.'),
    ('paper', 11, 'the following', 'Q11(c) lead-in: every part asked.'),
    ('paper', 11, 'both', 'Q11(c)(i) "in both aerobic and anaerobic respiration": description.'),
    ('paper', 13, 'the following', 'Q13(b)(i) "labelling each of the following parts": all six labels, each its '
                                   'own row.'),
    ('paper', 13, 'either', 'Q13(c)(iv) "either carnivores or herbivores": separate answers per option: ROUTES.'),
    ('paper', 13, 'or', 'Q13(c)(iv), same choice.'),
    ('paper', 13, 'either', 'Q13(c)(iv) "a benefit of either arrangement", same choice.'),
    ('paper', 14, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'either', 'Q14(b)(i) "either prokaryotic or eukaryotic": description.'),
    ('paper', 14, 'or', 'Q14(b)(i), same description.'),
    ('paper', 15, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 15, 'the following', 'Q15(a)(ii) "In each of the following cases": one card per numbered vein.'),
    ('paper', 15, 'both', 'Q15(a)(ii)5 "capillaries at both ends": description.'),
    ('paper', 15, 'the following', 'Q15(b) lead-in: every part asked.'),
    ('paper', 15, 'both', 'Q15(c)(i) "both yellow marrow and red marrow": one function of each, two rows.'),
    ('paper', 15, 'the following', 'Q15(c)(ii) "In each of the following cases": one card per numbered case.'),
    ('paper', 15, 'the following', 'Q15(c)(iii) "each of the following": one card per numbered item.'),
]

ROUTES = {
    'Q13(c)(iv)': ['carnivores', 'herbivores'],
    'Q15(b)(v)': ['oestrogen', 'progesterone'],
}

SEC = 'State Examinations Commission'
COMPRESSED = 'The scheme heads each answer with a compressed reprint of the ask.'
EACH_ITEM = 'A numbered list the scheme prices entry by entry: one card per entry.'
NO_REPRINT = 'The scheme heads this part with its marker only, no reprint of the ask.'
NO_ANSWER = 'The scheme prints no answer here, only what earns the marks.'
ROW_PRICED = 'Section C prints a mark against every row.'
SECTION_B_A = 'Section B (a) is "2(3)": each part 3, priced on its own.'


def item(page, n, end, anchor):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, after=anchor, br=True)


def term(page, word, br=False):
    """A printed term the paper sets before its answer line ("Ecology. ____")."""
    return Q(page, word, word, br=br)


def lab(page, label, **kw):
    """The scheme's compressed reprint where it shares its line with the answer
    ("Ecology: The study of ..."): the label alone is the pairing anchor."""
    return SQ(page, label, label, **kw)


def same(start, after, end=None, **kw):
    """An answer the scheme prints on its label's own line: the text after the
    label's colon. The reprint anchor ends on that line, so the search starts
    after a printed line before it."""
    return S(start, end, after=after, piece=2, psep=': ', **kw)


AGAR = ('The scheme directs that if neither starch agar nor skimmed milk agar is stated, (b) earns at most six '
        'points ("[4(4) + 2(2)]").')
REAGENT_NOTE = S('Named reagent colour changes must match named substrate in parts (iv) and (v)', after='4(4) + 4(2)')


def nine_b(r, q, rows, concept, sq, total, extra=()):
    """A Q9(b) part: the investigation's lead-in, and its starch-or-milk choice, as the stem."""
    return T(f'9b{r}', f'Q9(b)({r})', 'B', q, rows, 'bio-2-5', concept, sq, total, stem=Q9B + list(extra),
             decision=AGAR)


Q1 = Q(2, 'Explain five of the following terms.')
Q2D = Q(2, 'Name the two different biomolecular components of a lipid.')
Q3 = Q(3, 'The diagram shows asexual reproduction in yeast.')
Q3CI = Q(3, 'How does the genetic make-up of the new yeast cell relate to that of the parent cell?')
Q4A = [Q(4, 'In a certain breed of cattle there is incomplete dominance between the allele for red coat and the',
         'Heterozygous individuals are roan.'),
       Q(4, 'In each of the following three crosses state, in the space provided, the percentage chance that a calf',
         'of the cross will have a red coat.')]
Q4BII = Q(4, 'Would human females or human males be more likely to suffer from sex-linked diseases such',
          'as haemophilia?')
Q5 = Q(5, 'The diagram shows some details of sexual reproduction in a flowering plant.')
Q6A = Q(6, 'What term is used to describe the long stage of the cell cycle when cell division is not occurring?')
Q7BI = Q(7, 'When testing a solution for the presence of a reducing sugar, you used either Benedict’s or',
         'A control was included.')
Q7BII = Q(7, 'During your practical studies you carried out certain routine procedures.', 'describe how you:')
Q7BIII = Q(7, 'When preparing a microscope slide of human cheek cells or other animal cells,', 'describe how you:')
Q7BIV = Q(7, 'When immobilising an enzyme you used a gel substance to trap the enzyme.', 'make the gel insoluble.')
Q8A = Q(8, 'Answer the following questions in relation to the human pulse.')
Q8B = Q(8, 'Answer the following questions in relation to the investigation you carried out on the effect of',
        'exercise on the breathing rate or pulse rate.')
Q9B = [Q(9, 'Answer the following questions in relation to the investigation you carried out to show digestive',
         'activity during seed germination.'),
       Q(9, 'State whether you carried out this investigation using starch agar or skimmed milk (protein) agar.')]
Q9BIII = Q(9, 'When preparing the seeds, they were also split and sterilised.')
Q9BV = Q(9, 'How did you know that digestive activity had not occurred on one of your', 'investigation plates?')
Q10AII = Q(10, 'From your investigations of a named ecosystem, give one example each of:')
Q10B = Q(10, 'In the course of your studies you carried out an investigation of an ecosystem.')
Q10BI = Q(10, 'In the case of this named ecosystem, explain how you carried out each of the following.')
Q10C = [Q(10, 'A typical grazing food chain, consisting of four trophic levels, is shown below.',
          'Each letter represents a different species.'),
        Q(10, 'A → B → C → D')]
Q11B = Q(11, 'Answer the following questions from your knowledge of photosynthesis.')
Q11BIII = Q(11, 'In which pathway of the light stage is oxygen produced?')
Q11C = Q(11, 'Answer the following questions from your knowledge of respiration.')
Q11CI = Q(11, 'Name the 3-carbon molecule that is an intermediate compound in both aerobic and anaerobic',
          'respiration.')
Q11CIV = Q(11, 'What is produced from the intermediate compound referred to in (i) above when oxygen is not',
           'available')
Q12BI = Q(12, 'Name two excretory products, other than water, of mammals.')
Q12CII = Q(12, 'Increased metabolic rate, piloerection and vasoconstriction are responses in mammals to',
           'falling external temperatures.')
Q13A = Q(13, 'Growth regulators are important substances found in plants. They play a role in responses to',
         'environmental factors.')
Q13CII = Q(13, 'Light passes through the pupil in the eye.')
Q13CIII = Q(13, 'Certain parts of the eye are transparent and have curved surfaces.')
Q14AII = Q(14, 'What term is used to describe the differences which exist between individuals of a species?')
Q14AIII = Q(14, 'The differences referred to in (ii) form the basis of evolution by natural selection.')
Q14AV = Q(14, 'Give one example each of a disorder caused by:')
Q14BII = Q(14, 'Give one function of one named tissue found in plants.')
Q14BIII = Q(14, 'Give one function of one named tissue found in animals.')
Q15AII = Q(15, 'In each of the following cases name a vein which fits the description.')
Q15B = Q(15, 'Answer the following questions in relation to the typical human female menstrual cycle.')
Q15BI = Q(15, 'State one change that occurs, and the approximate day(s) of the cycle on which it occurs')
Q15BII = Q(15, 'FSH and LH each plays a role in the cycle.', 'in the cycle.')
Q15BIV = Q(15, 'Name two other hormones that play a role in the cycle.')
Q15CII = Q(15, 'Diseases in humans occur for a number of different reasons. In each of the following cases',
           'explain how the presence of a named disease may be recognised.')
Q15CIII = Q(15, 'Explain the biological basis of each of the following.')

# Q13(b)(i): the scheme's row of parts to label, each part's name read from
# its own place in the row (138-506 points across, 207-218 down, page 13).
EAR_PARTS = [((130, 200, 174, 226), 'pinna'), ((174, 200, 276, 226), 'semi-circular canals'),
             ((276, 200, 321, 226), 'stirrup'), ((321, 200, 373, 226), 'eardrum'),
             ((373, 200, 424, 226), 'cochlea'), ((424, 200, 515, 226), 'Eustachian tube')]
Q5_LABELS = [('A', 'A: Stigma'), ('B', 'B: Pollen tube'), ('C', 'C: Egg (or female gamete or ovum)')]
# Q5(b)-(d) ask about D and E, which the scheme never names: their key decodes
# the letters it does name (A-C, F), none of them asked, shown after the reveal.
Q5_KEY = [L(y, S(ln, page=7, piece=2, psep=': '), False) for y, ln in Q5_LABELS] + [L('F', S('Ovule', page=7), False)]

TASKS = [
    # ------------------------------------------------------------ Section A --
    # "Biotic." alone is below the build's eight-character floor, so that card
    # carries Q1's printed lead-in in its question text instead of its stem.
    T(f'1{x}', f'Q1({x})', 'A', [Q1, term(2, word, br=True)] if len(word) < 8 else term(2, word), [pt(row, 7)],
      topic, concept, sq, 7, stem=[] if len(word) < 8 else [Q1],
      decision='The scheme prints Q1 as "2(7) + 3(2) i.e. best five answers from (a) – (f)": an ordered split over '
               'the best five, each part carded at its first rate.')
    for x, word, sq, row, topic, concept in [
        ('a', 'Ecology.', lab(5, 'Ecology:'), same('Ecology:', 'best five answers'), 'bio-3-1', 'ecology'),
        ('b', 'Symbiosis.', lab(5, 'Symbiosis:'), same('Symbiosis:', 'best five answers'), 'bio-3-1', 'symbiosis'),
        ('c', 'Nutrient recycling.', SQ(5, 'Nutrient recycling:'), S('Reuse (of nutrients)'), 'bio-3-2',
         'nutrient-recycling'),
        ('d', 'Contest competition.', lab(5, 'Contest competition:'), same('Contest competition:', 'best five answers'),
         'bio-3-1', 'contest-competition'),
        ('e', 'Edaphic.', lab(5, 'Edaphic:'), same('Edaphic:', 'best five answers'), 'bio-3-1', 'edaphic'),
        ('f', 'Biotic.', SQ(5, 'Biotic:'), S('(Relating to) living (organisms)'), 'bio-3-1', 'biotic')]
] + [
    T('2a', 'Q2(a)', 'A', Q(2, 'Identify a non-metallic element, other than C, H, O and N, commonly found in proteins.'),
      [pt(S('Sulphur (or S)'), 3)], 'bio-1-2', 'sulphur-in-proteins', SQ(5, 'Non-metallic element in proteins:'), 3),
    T('2b', 'Q2(b)', 'A', Q(2, 'Give a metabolic role of proteins in the human body.'),
      [pt(S('Enzymes or hormones or antibodies or contractile (protein)', 'or named protein + role'), 3)], 'bio-1-2',
      'metabolic-role-of-protein', SQ(5, 'Metabolic role of protein:'), 3),
    T('2c', 'Q2(c)', 'A', Q(2, 'Give a structural role of proteins in the human body.'),
      [pt(same('Structural role of protein:', 'or named protein + role'), 3)], 'bio-1-2', 'structural-role-of-protein',
      lab(5, 'Structural role of protein:'), 3),
    T('2d', 'Q2(d)', 'A', Q2D, [pt(S('Glycerol'), 3), pt(S('Fatty acid'), 3)], 'bio-1-2', 'components-of-a-lipid',
      SQ(5, 'Components of lipid:'), 6, decision='The two components are two responses on the ladder.'),
    T('2e', 'Q2(e)', 'A', Q(2, 'Where would you expect to find phospholipids in human cells?'),
      [pt(S('Membrane(s)'), 3)], 'bio-1-2', 'phospholipids', SQ(5, 'Where phospholipids:'), 3),
    T('2f', 'Q2(f)', 'A', Q(2, 'Give a role of a named mineral, other than iron, which is required in the human body.'),
      [pt(S('Named mineral', after='Where phospholipids:'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Matching role'), 3, kind='criterion', note=NO_ANSWER)], 'bio-1-2', 'mineral-for-humans',
      SQ(5, 'Named mineral'), 6,
      decision='The scheme prices the named mineral and its matching role as two responses on the ladder, and '
               'prints neither.'),
    T('2g', 'Q2(g)', 'A', Q(2, 'What is the approximate percentage of water, by mass, in a human cell?',
                            'in a human cell?'),
      [pt(same('Human cell water % by mass:', 'Matching role'), 3)], 'bio-1-2', 'water-in-cells',
      lab(5, 'Human cell water % by mass:'), 3),
    T('3a', 'Q3(a)', 'A', Q(3, 'How do you know from the diagram that the reproduction is asexual?'),
      [pt(S('Only one parent (cell)'), 5)], 'bio-3-2', 'why-budding-is-asexual', SQ(6, 'Why asexual:'), 5,
      stem=[Q3], fig='q3-yeast'),
    T('3b', 'Q3(b)', 'A', Q(3, 'What name is given to this type of asexual reproduction?'),
      [pt(S('Budding'), 5)], 'bio-3-2', 'budding', SQ(6, 'Asexual reproduction. in yeast:'), 5, stem=[Q3],
      fig='q3-yeast'),
    T('3ci', 'Q3(c)(i)', 'A', Q3CI, [pt(same('Genetic make-up compared to parent:', 'Budding'), 5)], 'bio-3-2',
      'identical-offspring', lab(6, 'Genetic make-up compared to parent:'), 5, stem=[Q3], fig='q3-yeast'),
    T('3cii', 'Q3(c)(ii)', 'A', Q(3, 'Explain your answer.', 'Explain your answer.'), [pt(same('Explain:', 'Genetic make-up compared'), 5)],
      'bio-3-2', 'budding-is-mitosis', lab(6, 'Explain:'), 5, stem=[Q3, M('(i)', 3), Q3CI], fig='q3-yeast'),
    T('3d', 'Q3(d)', 'A', Q(3, 'Give an advantage and a disadvantage of asexual reproduction in organisms such as yeast.'),
      [pt(S('Rapid or characteristics maintained (or example) or no variation'), 5,
          label=S('Advantage:', after='(Reproduced by) mitosis')),
       pt(S('Increased risk of disease or overcrowding or increased competition', 'or no variation'), 5,
          label=S('Disadvantage:'))], 'bio-3-2', 'asexual-reproduction', SQ(6, 'Advantage:'), 10,
      decision='The advantage and the disadvantage are two responses on the ladder.'),
    T('3e', 'Q3(e)', 'A', Q(3, 'Name another organism which belongs to the same kingdom as yeast.'),
      [pt(same('Same kingdom as yeast:', 'or no variation'), 5)], 'bio-3-2', 'fungi',
      lab(6, 'Same kingdom as yeast:'), 5),
] + [
    T(f'4a{r}', f'Q4(a)({r})', 'A', Q(4, cross), [pt(same(label, '5(3) + 5(1)'), 3)], 'bio-1-4', concept,
      lab(6, label), 3, stem=Q4A)
    for r, cross, label, concept in [
        ('i', 'roan × white', 'Chance roan × white → red:', 'roan-cross-white'),
        ('ii', 'roan × red', 'Chance roan × red → red:', 'roan-cross-red'),
        ('iii', 'roan × roan', 'Chance roan × roan → red:', 'roan-cross-roan')]
] + [
    T('4bi', 'Q4(b)(i)', 'A', Q(4, 'In genetics, what is meant by the term sex-linkage?'),
      [pt(S('When genes are carried on the sex (or X or Y) chromosome(s)'), 3)], 'bio-1-4', 'sex-linkage',
      SQ(6, 'Sex-linkage:'), 3),
    T('4bii', 'Q4(b)(ii)', 'A', Q4BII, [pt(S('Males'), 3)], 'bio-1-4', 'sex-linked-sufferers', SQ(6, 'More likely:'), 3),
    T('4biii', 'Q4(b)(iii)', 'A', Q(4, 'Explain your answer to part (ii) by referring below to possible genotypes and their',
                                    'corresponding phenotypes.'),
      [pt(S('XnY–'), 3, label=S('Genotype:'), note_sel=S('Male genotypes and phenotypes:', after='Males')),
       pt(S('Sufferer'), 3, label=S('Phenotype:')),
       pt(S('XnXn'), 3, label=S('Genotype:', nth=2), note_sel=S('Female genotypes and phenotypes:')),
       pt(S('Sufferer', nth=2), 3, label=S('Phenotype:', nth=2), note_sel=S('(or lethal for haemophilia)')),
       pt(S('Male only needs to inherit the recessive allele (from mother)', 'is a sufferer (or lethal for haemophilia)'),
          3, label=S('Explain:'))],
      'bio-1-4', 'sex-linked-genotypes', SQ(6, 'Male genotypes and phenotypes:'), 15, stem=[M('(ii)', 4), Q4BII],
      decision='Five responses on the ladder: the male genotype and phenotype, the female genotype and phenotype, '
               'and the explanation. The scheme prints the female in two boxes joined by "OR" (XnXn sufferer, or '
               'XNXn normal): answer variants of one task. The text layer flattens the superscript alleles: "XnY–" '
               'is X with a raised n and Y with a raised dash.'),
] + [
    # Q5(a): one card per letter, the letters' meanings lifted from the scheme.
    T(f'5a-{x.lower()}', 'Q5(a)', 'A', Q(5, 'Name the parts labelled A, B and C.'),
      [pt(S(line, piece=2, psep=': '), 3)], 'bio-2-5', concept,
      SQ(7, '(a)', path=['5.'], bare=True, paired=NO_REPRINT + ' It names each letter on its own line ("A: ...").'),
      3, stem=[Q5], fig='q5-flower', item=(x.lower(), x),
      decision='A lettered figure the scheme prices letter by letter: one card per letter.',
      labels=[L(y, S(ln, page=7, piece=2, psep=': '), y == x) for y, ln in Q5_LABELS])
    for x, line, concept in [('A', 'A: Stigma', 'stigma'), ('B', 'B: Pollen tube', 'pollen-tube'),
                             ('C', 'C: Egg (or female gamete or ovum)', 'egg-cell')]
] + [
    T('5b', 'Q5(b)', 'A', Q(5, 'Suggest two ways by which the structure labelled D could have arrived at its position on the',
                            'structure labelled A.'),
      [pt(S('Wind'), 3), pt(S('Insect (or animal)'), 3)], 'bio-2-5', 'pollination', SQ(7, 'How D to A:'), 6,
      stem=[Q5], fig='q5-flower', labels=Q5_KEY, decision='The two ways are two responses on the ladder.'),
    T('5c', 'Q5(c)', 'A', Q(5, 'By what process does the structure labelled D give rise to the two structures labelled E?'),
      [pt(S('Mitosis'), 3)], 'bio-2-5', 'male-gametes-by-mitosis', SQ(7, 'How E from D:'), 3, stem=[Q5],
      fig='q5-flower', labels=Q5_KEY),
    T('5d', 'Q5(d)', 'A', Q(5, 'What is the fate of each of the two structures labelled E?'),
      [pt(S('(One) fuses with the egg (nucleus)'), 3), pt(S('(The other) fuses with the (2) polar nuclei'), 3)],
      'bio-2-5', 'double-fertilisation', SQ(7, 'Fate of Es:', paired=COMPRESSED), 6, stem=[Q5], fig='q5-flower', labels=Q5_KEY,
      decision='The scheme prints two pairs of fates joined by "OR": answer variants of one task, each pair two '
               'responses on the ladder.'),
    T('5e', 'Q5(e)', 'A', Q(5, 'Name the structure labelled F and say what it develops into after fertilisation.'),
      [pt(S('Ovule'), 3, label=S('Name F:', after='(The other) disintegrates')),
       pt(S('Seed'), 3, label=S('Develops into:'))], 'bio-2-5', 'ovule-to-seed', SQ(7, 'Name F:'), 6, stem=[Q5],
      fig='q5-flower', labels=[L('F', S('Ovule', page=7), True)],
      decision='The name and what it develops into are two responses on the ladder.'),
    T('6a', 'Q6(a)', 'A', Q6A, [pt(S('Interphase'), 5)], 'bio-2-3', 'interphase', SQ(7, 'Long stage of cell cycle:'), 5),
    T('6b', 'Q6(b)', 'A', Q(6, 'Name two types of biomolecule that are produced in the cell during this stage of the cell cycle.'),
      [anyn(S('Nucleic acid (or DNA or RNA)/ protein/ fat/ carbohydrate'), 2, 5, note_sel=S('Any two'))], 'bio-2-3',
      'biomolecules-made-in-interphase', SQ(7, 'Biomolecule types produced:'), 10, stem=[M('(a)', 6), Q6A]),
    T('6c', 'Q6(c)', 'A', Q(6, 'Name one organelle that is replicated at this stage of the cell cycle.'),
      [pt(S('Mitochondrion or chloroplast or ribosomes or centriole'), 5)], 'bio-2-3', 'organelles-replicated',
      SQ(7, 'Organelle replicated:'), 5, stem=[M('(a)', 6), Q6A]),
    T('6d', 'Q6(d)', 'A', Q(6, 'Give any two other changes which will have occurred in the cell by the end of this stage of the cell',
                            'cycle.'),
      [anyn(same('Two other changes:', 'Organelle replicated:', 'or DNA replicated'), 2, 5, note_sel=S('Any two'))],
      'bio-2-3', 'changes-in-interphase', lab(7, 'Two other changes:'), 10, stem=[M('(a)', 6), Q6A]),
    T('6e', 'Q6(e)', 'A', Q(6, 'Suggest why mature human red blood cells do not undergo cell division.'),
      [pt(S('No nucleus'), 5)], 'bio-2-3', 'red-cells-do-not-divide', SQ(7, 'Why no division of red blood cells:'), 5),
    # ------------------------------------------------------------ Section B --
    T('7a', 'Q7(a)', 'B', Q(7, 'Give two examples of limitations of the scientific method.'),
      [anyn(same('Two scientific method limitations:', '2(3)', 'of change/ accidental discovery'), 2, 3,
            note_sel=S('Any two'))], 'bio-u2', 'limitations-of-scientific-method',
      lab(8, 'Two scientific method limitations:'), 6, decision=SECTION_B_A),
] + [
    T(f'7b{r}{n}', f'Q7(b)({r}){n}', 'B', item(7, n, end, anchor), [pt(S(ans), 4)], topic, concept,
      SQ(8, sq, paired=COMPRESSED if paired else None), 4, stem=[stem], decision=EACH_ITEM)
    for r, n, end, anchor, stem, ans, topic, concept, sq, paired in [
        ('i', 1, 'Name the substance which you used as a control.', 'A control was included.', Q7BI,
         'Water or a non-reducing sugar (or example)', 'bio-1-2', 'control-for-reducing-sugar', 'Control substance:',
         False),
        ('i', 2, 'What colour were the contents of the control tube at the end of the test?', 'A control was included.',
         Q7BI, 'Blue', 'bio-1-2', 'colour-of-the-control', 'Control colour at end', False),
        ('ii', 1, 'Added a very small volume of a solution.', 'routine procedures.', Q7BII,
         'Dropper or pipette or syringe', 'bio-u2', 'adding-small-volumes', 'How add small volume:', False),
        ('ii', 2, 'Ensured that the pH of a solution remained constant.', 'routine procedures.', Q7BII,
         'Use a (pH) buffer', 'bio-2-1', 'constant-ph', 'How keep pH constant:', False),
        ('iii', 1, 'Transferred the cells to the slide.', 'microscope slide of human cheek', Q7BIII,
         'Transfer described (e.g. swab)', 'bio-1-3', 'transferring-cheek-cells', 'How transfer cells:', True),
        ('iii', 2, 'Improved the visibility of the cells on the slide.', 'microscope slide of human cheek', Q7BIII,
         'Add a stain (or named stain) or add a coverslip', 'bio-1-3', 'making-cells-visible',
         'How improve visibility:', True),
        ('iv', 1, 'Name the gel substance you used to trap the enzyme.', 'make the gel insoluble.', Q7BIV,
         '(Sodium) alginate', 'bio-2-1', 'alginate-gel', 'Gel:', False),
        ('iv', 2, 'Name the second substance you used to make the gel insoluble.', 'make the gel insoluble.', Q7BIV,
         'Calcium chloride', 'bio-2-1', 'calcium-chloride', 'To make gel insoluble:', False)]
] + [
    T('8ai', 'Q8(a)(i)', 'B', Q(8, 'What is the pulse?'),
      [pt(S('The (rhythmic) stretching (or expanding or vibrating) of an artery'), 3)], 'bio-2-6', 'pulse',
      SQ(8, 'Pulse:'), 3, stem=[Q8A], decision=SECTION_B_A),
    T('8aii', 'Q8(a)(ii)', 'B', Q(8, 'What makes the wrist (or temple, or neck) a suitable part of the body to detect a pulse?'),
      [pt(S('Artery near the surface'), 3)], 'bio-2-6', 'where-to-take-a-pulse', SQ(8, 'Why pulse at wrist:'), 3,
      stem=[Q8A], decision=SECTION_B_A),
    T('8bi', 'Q8(b)(i)', 'B', Q(8, 'What was the control in this investigation?'),
      [pt(same('Control:', 'Artery near the surface'), 4)], 'bio-2-6', 'exercise-control', lab(8, 'Control:'), 4,
      stem=[Q8B]),
    T('8bii', 'Q8(b)(ii)', 'B', Q(8, 'What is the purpose of this control?'),
      [pt(S('To compare with the results (of the experiment)'), 4)], 'bio-2-6', 'purpose-of-a-control',
      SQ(8, 'Purpose of control:'), 4, stem=[Q8B]),
    T('8biii', 'Q8(b)(iii)', 'B', [Q(8, 'You carried out this investigation on two women of the same age.',
                                    'The other (B) was overweight and rarely took exercise.'),
                                  Q(8, '1. Appropriately label each of the axes below.', br=True),
                                  Q(8, '2. Draw two curves or plots to summarise the most likely results of your investigation,',
                                    'clearly labelling which curve relates to which individual.', br=True)],
      [pt(S('x-axis ‘duration (of exercise)’ or ‘time’ or level of exercise'), 4), pt(S('y-axis ‘rate’'), 4),
       pt(S('B increases by a greater amount'), 4, kind='criterion', label=S('Curve or plot showing:'))],
      'bio-2-6', 'exercise-graph', SQ(8, 'Axes labels'), 12, stem=[Q8B], fig='q8b-axes',
      decision='The x-axis label, the y-axis label and the curves are three responses on the ladder; the printed '
               'empty axes are shown as printed.'),
    T('8biv', 'Q8(b)(iv)', 'B', Q(8, 'Recovery time is the duration of the period following exercise during which the breathing rate',
                                  'Suggest how you might measure recovery time.'),
      [anyn(same('How measure recovery time:', 'B increases by a greater amount', 'until resting rate reached'), 3, 4,
            note_sel=S('Any three'))], 'bio-2-6', 'recovery-time', lab(8, 'How measure recovery time:'), 12,
      stem=[Q8B]),
    T('9ai', 'Q9(a)(i)', 'B', Q(9, 'Explain what is meant by the term dormancy in seeds.'),
      [pt(S('Period of low (or no) metabolism or period during which germination',
            'period of low (or no) activity'), 3)], 'bio-2-5', 'dormancy', SQ(9, 'Dormancy:'), 3, decision=SECTION_B_A),
    T('9aii', 'Q9(a)(ii)', 'B', Q(9, 'How does digestion contribute to successful seed germination?'),
      [pt(same('Contribution of digestion:', 'period of low (or no) activity', 'more easily absorbed (by embryo)'), 3)],
      'bio-2-5', 'digestion-in-germination', lab(9, 'Contribution of digestion:', paired=COMPRESSED), 3,
      decision=SECTION_B_A),
] + [
    nine_b('i', Q(9, 'Name a type of enzyme in the seed that carries out this digestion.'),
           [pt(S('Amylase or protease (or named protease)'), 4,
               note_sel=S('Enzyme in (i) must match named substrate i.e. starch or protein', after='4(4) + 4(2)'))],
           'enzymes-in-germination', SQ(9, 'Type of enzyme:'), 4),
    nine_b('ii', Q(9, 'Why were the seeds soaked in water at the start of the investigation?'),
           [pt(S('To enable metabolic activity (or digestion) or to start up the',
                 'or to soften the testa or to break dormancy'), 4)], 'soaking-seeds', SQ(9, 'Why soak seeds:'), 4),
] + [
    T(f'9biii{n}', f'Q9(b)(iii){n}', 'B', item(9, n, end, 'split and sterilised.'), [pt(S(ans), 4)], 'bio-2-5', concept,
      SQ(9, sq), 4, stem=Q9B + [Q9BIII], decision=EACH_ITEM + ' ' + AGAR)
    for n, end, ans, concept, sq in [
        (1, 'Why is it recommended that you sterilise the seeds?', 'To kill (or remove) all microorganisms',
         'sterilising-seeds', 'Why sterilise seeds:'),
        (2, 'Why were the split seeds placed open-side down on the agar?',
         'Enzyme exposed to (or in contact with) the substrate', 'seeds-open-side-down', 'Why open-side down:')]
] + [
    nine_b('iv', Q(9, 'How did you know that digestive activity had occurred on one of your investigation', 'plates?'),
           [pt(S('(Flooded plates with) iodine or biuret (solution)'), 4, note_sel=REAGENT_NOTE),
            pt(S('Clear areas around (under) seeds (or described)'), 4)], 'evidence-of-digestion',
           SQ(9, 'How know had occurred:'), 8),
    nine_b('v', Q9BV, [pt(S('No clear areas or all areas stain positive colour'), 4, note_sel=REAGENT_NOTE)],
           'no-digestion', SQ(9, 'How know had not occurred:'), 4),
    nine_b('vi', Q(9, 'Give one reason for what you observed in part (v).'),
           [pt(S('Seeds were dead or enzyme had been denatured'), 4)], 'why-no-digestion',
           SQ(9, 'Reason for observation in (v):'), 4, extra=[M('(v)', 9), Q9BV]),
] + [
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', Q(10, 'What is the precise meaning of the term niche as used by ecologists?'),
      [pt(same('Niche:', '4(60)'), 3)], 'bio-3-1', 'niche', lab(10, 'Niche:'), 3, decision=ROW_PRICED),
] + [
    T(f'10aii{n}', f'Q10(a)(ii){n}', 'C', item(10, n, end, 'give one example each of:'),
      [pt(S(ans), 3, note_sel=S('If answers do not match named ecosystem, maximum of 3 marks', after='Niche:'))],
      'bio-3-1', concept, SQ(10, sq), 3, stem=[Q10AII], decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'A safety hazard.', 'Any valid hazard (e.g. wet grass or broken glass)', 'ecology-safety-hazard',
         'Safety hazard:'),
        (2, 'A source of error.', 'Any valid error (e.g. miscounting or misidentification)', 'ecology-source-of-error',
         'Source of error:')]
] + [
    T('10bi1', 'Q10(b)(i)1', 'C', item(10, 1, 'Collection of fauna using a named method.', 'explain how you carried out each'),
      [pt(same('Animal collection method:', 'Any valid error', 'any named suitable method'), 3)], 'bio-3-1',
      'collecting-fauna', lab(10, 'Animal collection method:'), 3, stem=[Q10B, Q10BI], decision=EACH_ITEM),
    T('10bi2', 'Q10(b)(i)2', 'C', item(10, 2, 'Identification of the collected fauna.', 'explain how you carried out each'),
      [pt(same('Identification:', 'any named suitable method'), 3)], 'bio-3-1', 'identifying-fauna',
      lab(10, 'Identification:'), 3, stem=[Q10B, Q10BI], decision=EACH_ITEM),
    T('10bi3', 'Q10(b)(i)3', 'C', item(10, 3, 'In your answer explain how you ensured that the sample was random.',
                                       'explain how you carried out each'),
      [anyn(same('Quantitative method details:', '(Identification) key', 'how result expressed'), 2, 3),
       pt(S('How random'), 3, kind='criterion', note=NO_ANSWER)], 'bio-3-1', 'quantitative-plant-study',
      lab(10, 'Quantitative method details:', paired=COMPRESSED), 9, stem=[Q10B, Q10BI],
      decision=EACH_ITEM + ' The scheme prices two method details "2(3)" and how the sample was made random "3".'),
    T('10bii', 'Q10(b)(ii)', 'C', Q(10, 'Why is it essential to use a random sampling technique?'),
      [pt(S('To prevent bias'), 3)], 'bio-3-1', 'random-sampling', SQ(10, 'Why random:'), 3, stem=[Q10B]),
    T('10biii', 'Q10(b)(iii)', 'C', Q(10, 'Suggest two abiotic factors that could affect the distribution of the named plant species.'),
      [anyn(same('Abiotic factors:', 'To prevent bias', 'altitude/ soil type'), 2, 3)], 'bio-3-1', 'abiotic-factors',
      lab(10, 'Abiotic factors:'), 6, stem=[Q10B]),
    T('10biv', 'Q10(b)(iv)', 'C', Q(10, 'State one way in which human activity can have an impact on your named ecosystem.'),
      [pt(same('Human activity:', 'altitude/ soil type'), 3)], 'bio-3-1', 'human-impact', lab(10, 'Human activity:'), 3,
      stem=[Q10B]),
    T('10ci', 'Q10(c)(i)', 'C', Q(10, 'What is meant by the term trophic level?'),
      [pt(S('Position on the food chain or feeding level or energy level', 'or feeding stage', skip_marks=True), 3)],
      'bio-3-1', 'trophic-level', SQ(10, 'Trophic level:'), 3, stem=Q10C, fig='q10c-chain',
      decision='The scheme prints the row\'s mark between its two lines; the answer is read without it.'),
    T('10cii', 'Q10(c)(ii)', 'C', Q(10, 'Explain why food chains are generally short.'),
      [pt(S('Little (10%) energy passed on to next level', 'or large amount (90%) of energy lost at each level'), 3)],
      'bio-3-1', 'short-food-chains', SQ(10, 'Why chains short:'), 3, stem=Q10C, fig='q10c-chain'),
    T('10ciii', 'Q10(c)(iii)', 'C', Q(10, 'Which letter represents the secondary consumer?'),
      [pt(same('Secondary consumer:', 'of energy lost at each level'), 3)], 'bio-3-1', 'secondary-consumer',
      lab(10, 'Secondary consumer:'), 3, stem=Q10C, fig='q10c-chain'),
    T('10civ', 'Q10(c)(iv)', 'C', Q(10, 'Give a possible reason why the population of C may decline naturally.'),
      [pt(same('Why C might decline:', 'Secondary consumer:', 'or lack of B or migration'), 3)], 'bio-3-1',
      'population-decline', lab(10, 'Why C might decline:'), 3, stem=Q10C, fig='q10c-chain'),
    T('10cv', 'Q10(c)(v)', 'C', Q(10, 'Suggest a possible consequence for the population of A if the population of C was',
                                  'significantly reduced. Explain your answer.'),
      [pt(S('(Population A) falls'), 3, label=S('Consequence:', after='or lack of B or migration')),
       pt(S('Population of primary consumers increases or population', 'of B increases (which eat large amount of producer A)'),
          3, label=S('Explanation:'))], 'bio-3-1', 'knock-on-effects', SQ(10, 'Consequence:'), 6, stem=Q10C, fig='q10c-chain'),
    T('10cvi', 'Q10(c)(vi)', 'C', Q(10, 'Suggest how members of species D might respond, if the population of C was significantly',
                                    'reduced.'),
      [pt(same('How D might respond:', 'of B increases'), 3)], 'bio-3-1', 'predator-response',
      lab(10, 'How D might respond:'), 3, stem=Q10C, fig='q10c-chain'),
    T('10cvii', 'Q10(c)(vii)', 'C', Q(10, 'A food web is a series of interconnected food chains. Suggest how it may be possible for the',
                                      'secondary consumer, in the food chain above, to be a primary consumer in another food chain.'),
      [pt(same('How possible primary consumer in other food chain:', 'Migrate or switch prey'), 3)], 'bio-3-1',
      'omnivores', lab(10, 'How possible primary consumer in other food chain:'), 3, stem=Q10C, fig='q10c-chain'),
    T('11ai', 'Q11(a)(i)', 'C', Q(11, 'In the context of cell metabolism, what does NAD stand for?'),
      [pt(same('NAD:', '11.'), 3)], 'bio-2-2', 'nad', lab(11, 'NAD:'), 3, decision=ROW_PRICED),
    T('11aii', 'Q11(a)(ii)', 'C', Q(11, 'Name two types of particle that are transferred by NAD.'),
      [pt(S('Electrons (e-)'), 3), pt(S('Protons (or hydrogen ions or H+)'), 3)], 'bio-2-2', 'what-nad-carries',
      SQ(11, 'Particles transferred:', paired=COMPRESSED), 6),
    T('11bi', 'Q11(b)(i)', 'C', Q(11, 'Where in plant cells does the process take place?'), [pt(S('Chloroplast'), 3)],
      'bio-2-2', 'chloroplast', SQ(11, 'Where:'), 3, stem=[Q11B]),
    T('11bii', 'Q11(b)(ii)', 'C', Q(11, 'Name a substance which absorbs light energy for the process.'),
      [pt(S('Chlorophyll'), 3)], 'bio-2-2', 'chlorophyll', SQ(11, 'Substance:'), 3, stem=[Q11B]),
    T('11biii', 'Q11(b)(iii)', 'C', Q11BIII, [pt(S('Pathway 2'), 3)], 'bio-2-2', 'pathway-2', SQ(11, 'Pathway:'), 3,
      stem=[Q11B]),
    T('11biv', 'Q11(b)(iv)', 'C', Q(11, 'Outline how this oxygen is produced.'),
      [pt(S('Water split/ using light (energy)', piece=1), 3), pt(S('Water split/ using light (energy)', piece=2), 3)],
      'bio-2-2', 'photolysis', SQ(11, 'How O2 produced:', paired=COMPRESSED), 6,
      stem=[Q11B, M('(iii)', 11), Q11BIII],
      decision='"2(3)" over either pair the scheme prints, joined by "OR": answer variants of one task, each pair cut '
               'at the scheme\'s own solidus.'),
    T('11bv', 'Q11(b)(v)', 'C', Q(11, 'Give one fate of this oxygen.'),
      [pt(S('Released (to the atmosphere) or (used in) respiration'), 3)], 'bio-2-2', 'fate-of-oxygen',
      SQ(11, 'Fate of O2:', paired=COMPRESSED), 3, stem=[Q11B, M('(iii)', 11), Q11BIII]),
    T('11bvi', 'Q11(b)(vi)', 'C', Q(11, 'What is the fate of the carbon in the carbon dioxide used in the dark stage?'),
      [pt(same('Fate of carbon:', '(used in) respiration'), 3)], 'bio-2-2', 'fate-of-carbon', lab(11, 'Fate of carbon:'),
      3, stem=[Q11B]),
    T('11bvii', 'Q11(b)(vii)', 'C', Q(11, 'Give one reason why a suitable temperature is necessary for the dark stage to occur.'),
      [pt(same('Why suitable temperature:', 'Makes carbohydrate'), 3)], 'bio-2-2', 'temperature-and-the-dark-stage',
      lab(11, 'Why suitable temperature:'), 3, stem=[Q11B]),
    T('11bviii', 'Q11(b)(viii)', 'C', Q(11, 'Aquatic plants such as Elodea are particularly suitable for investigating photosynthesis.',
                                        'Suggest a reason for this.'),
      [pt(S('Bubbles (of oxygen visible for counting)'), 3)], 'bio-2-2', 'why-elodea', SQ(11, 'Why Elodea:'), 3,
      stem=[Q11B]),
    T('11ci', 'Q11(c)(i)', 'C', Q11CI, [pt(S('*Pyruvate or *pyruvic acid'), 3)], 'bio-2-2', 'pyruvate',
      SQ(11, '3-carbon intermediate:'), 3, stem=[Q11C]),
    T('11cii', 'Q11(c)(ii)', 'C', Q(11, 'What name is given to the biochemical pathway by which this intermediate compound is',
                                    'produced?'),
      [pt(S('*Glycolysis'), 3)], 'bio-2-2', 'glycolysis', SQ(11, 'Pathway:', nth=2), 3,
      stem=[Q11C, M('(i)', 11), Q11CI]),
    T('11ciii', 'Q11(c)(iii)', 'C', [Q(11, 'What happens to the intermediate compound referred to in (i) above when oxygen is available',
                                       'and used in the breakdown of glucose?'),
                                     Q(11, 'In your answer refer to:', br=True),
                                     Q(11, '1.', 'Krebs cycle.', after='In your answer refer to:', br=True),
                                     Q(11, '2.', 'Electron transport system.', after='In your answer refer to:', br=True)],
      [pt(S('Oxidative fate of pyruvate: Converted to Acetyl (Co- Enzyme A) or enters', 'mitochondrion', piece=2,
            psep=': '), 3),
       anyn(S('CO2 produced/ ATP produced/ NADH produced'), 2, 3,
            note_sel=S('Any one further point from 1 or from 2.')),
       anyn(S('or electron transport system: protons (or H+ ions) combine with O2 or electrons', 'to make ATP',
              piece=2, psep=': '), 1, 3)],
      'bio-2-2', 'aerobic-fate-of-pyruvate',
      SQ(11, '(iii)', path=['11.', '(c)'], bare=True,
         paired='The scheme heads this part "Oxidative fate of pyruvate", not a reprint of the ask.'), 12,
      stem=[Q11C, M('(i)', 11), Q11CI],
      decision='The scheme prices (iii) as four 3s: the fate of pyruvate, a Krebs cycle point (its "1."), an '
               'electron transport point (its "2.") and "Any one further point from 1 or from 2.". Two answer '
               'variants: the further point from the Krebs cycle list, or from the electron transport list.'),
] + [
    T(f'11civ{n}', f'Q11(c)(iv){n}', 'C', item(11, n, end, 'when oxygen is not'), [pt(S(ans), 3)], 'bio-2-2', concept,
      SQ(11, sq, paired=COMPRESSED), 3, stem=[Q11C, Q11CIV], decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'in muscle?', '*Lactic acid or *lactate', 'lactic-acid', 'Anaerobic product in muscle:'),
        (2, 'in yeast?', '*Ethanol (and carbon dioxide)', 'ethanol', 'Anaerobic product in yeast:')]
] + [
    T('12ai', 'Q12(a)(i)', 'C', Q(12, 'Distinguish between the terms excretion and egestion by writing a sentence about each term.'),
      [pt(S('Removal of metabolic waste'), 3, label=S('Excretion:', after='12.')),
       pt(S('Removal of undigested (or unabsorbed) material'), 3, label=S('Egestion:'))], 'bio-2-6',
      'excretion-and-egestion', SQ(12, 'Excretion:'), 6, decision=ROW_PRICED),
    T('12aii', 'Q12(a)(ii)', 'C', Q(12, 'Suggest how excretion may occur in simple organisms such as Amoeba.'),
      [pt(same('Simple excretion:', 'Removal of undigested'), 3)], 'bio-2-6', 'excretion-in-amoeba',
      lab(12, 'Simple excretion:'), 3),
    T('12bi', 'Q12(b)(i)', 'C', Q12BI,
      [anyn(same('Excretory products:', 'Diffusion or contractile vacuole'), 2, 3)], 'bio-2-6', 'excretory-products',
      lab(12, 'Excretory products:'), 6),
    T('12bii', 'Q12(b)(ii)', 'C', Q(12, 'For each product referred to in (i), give a location in the body in which it is produced.'),
      [pt(S('First product + matching location'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Second product + matching location'), 3, kind='criterion', note=NO_ANSWER)], 'bio-2-6',
      'where-excretory-products-form', SQ(12, 'Excretory product production locations:'), 6,
      stem=[M('(i)', 12), Q12BI]),
    T('12biii', 'Q12(b)(iii)', 'C', Q(12, 'Describe the role of ADH (vasopressin) in human excretion.'),
      [anyn(same('ADH:', 'Second product + matching location', 'urine volume lowered (or urine more conc.)'), 3, 3)],
      'bio-2-6', 'adh', lab(12, 'ADH:'), 9),
    T('12biv', 'Q12(b)(iv)', 'C', Q(12, 'Suggest two structures in flowering plants which play a role in excretion.'),
      [anyn(S('Stomata/ lenticels/ leaves'), 2, 3)], 'bio-2-6', 'excretion-in-plants', SQ(12, 'Plant structures:'), 6),
    T('12ci', 'Q12(c)(i)', 'C', Q(12, 'What is meant by the term homeostasis?'),
      [pt(S('Maintenance of a constant internal environment'), 3)], 'bio-2-4', 'homeostasis', SQ(12, 'Homeostasis'), 3),
    T('12cii1', 'Q12(c)(ii)1', 'C', item(12, 1, 'Explain the term metabolism.', 'vasoconstriction are responses'),
      [pt(same('Metabolism:', 'Maintenance of a constant'), 3)], 'bio-1-1', 'metabolism', lab(12, 'Metabolism:'), 3,
      stem=[Q12CII], decision=EACH_ITEM),
    T('12cii2', 'Q12(c)(ii)2', 'C', item(12, 2, 'temperatures?', 'vasoconstriction are responses'),
      [pt(same('Effect of increase:', 'All chemical reactions'), 3)], 'bio-2-4', 'metabolic-heat',
      lab(12, 'Effect of increase:'), 3, stem=[Q12CII], decision=EACH_ITEM),
    T('12cii3', 'Q12(c)(ii)3', 'C', item(12, 3, 'What term is used to describe animals that can vary their metabolic rate significantly?',
                                         'vasoconstriction are responses'),
      [pt(S('*Endotherm(s) or *Endothermic'), 3)], 'bio-2-4', 'endotherms', SQ(12, 'Term:'), 3, stem=[Q12CII],
      decision=EACH_ITEM),
    T('12cii4', 'Q12(c)(ii)4', 'C', item(12, 4, 'falling external temperatures.', 'vasoconstriction are responses'),
      [pt(S('Ectotherm response:', piece=2, psep=': '), 3)], 'bio-2-4', 'ectotherms',
      SQ(12, '(ii)', path=['12.', '(c)'], bare=True,
         paired='The scheme labels this item "Ectotherm response", a term the paper does not print.'), 3,
      stem=[Q12CII], decision=EACH_ITEM),
    T('12cii5', 'Q12(c)(ii)5', 'C', item(12, 5, 'Explain how piloerection can be an important response to falling external temperatures.',
                                         'vasoconstriction are responses'),
      [pt(S('Hairs standing up'), 3, label=S('Piloerection:', after='or hibernate')),
       pt(S('Traps air or insulates or reduces heat loss'), 3, label=S('Importance:'))], 'bio-2-4', 'piloerection',
      SQ(12, 'Piloerection:'), 6, stem=[Q12CII], decision=EACH_ITEM),
    T('12cii6', 'Q12(c)(ii)6', 'C', item(12, 6, 'temperatures.', 'vasoconstriction are responses'),
      [pt(S('Reduces blood flow to skin or reduces heat loss'), 3)], 'bio-2-4', 'vasoconstriction',
      SQ(12, 'Vasoconstriction importance:', paired=COMPRESSED), 3, stem=[Q12CII], decision=EACH_ITEM),
    T('13ai', 'Q13(a)(i)', 'C', Q(13, 'What name is given to the regions of plants which secrete growth regulators?'),
      [pt(same('Where growth regulators secreted:', '13.'), 3)], 'bio-2-4', 'meristems',
      lab(13, 'Where growth regulators secreted:', paired=COMPRESSED), 3, stem=[Q13A], decision=ROW_PRICED),
    T('13aii', 'Q13(a)(ii)', 'C', Q(13, 'Give an example of a growth regulator which has a negative effect on plant growth.'),
      [pt(S('Ethene or IAA (or any named growth regulator)'), 3)], 'bio-2-4', 'growth-inhibitors',
      SQ(13, 'Negative regulator:'), 3, stem=[Q13A]),
    T('13aiii', 'Q13(a)(iii)', 'C', Q(13, 'Explain the term thigmotropism.'),
      [pt(S('Growth response (of a plant) to touch'), 3)], 'bio-2-4', 'thigmotropism', SQ(13, 'Thigmotropism:'), 3,
      stem=[Q13A]),
    T('13bi', 'Q13(b)(i)', 'C', [Q(13, 'Draw a large diagram to show the structure of the human ear, labelling each of the following',
                                   'parts:'),
                                 Q(13, 'pinna semi-circular canals stirrup ear drum cochlea Eustachian tube', br=True)],
      [G('tokens', page=13, clip=clip, expect=part, marks=2,
         **({'note_sel': S('Diagram: with correctly located labelled parts', after='Growth response (of a plant)')}
            if i == 0 else {}))
       for i, (clip, part) in enumerate(EAR_PARTS)],
      'bio-2-4', 'drawing-the-ear', SQ(13, 'Diagram: with correctly located labelled parts', paired=COMPRESSED), 12,
      decision='The scheme prices "Diagram: with correctly located labelled parts 6(2)": each of the six parts, '
               'correctly located and labelled, 2. It prints no mark for the drawing itself. Each part\'s name is '
               'read from its own place in the scheme\'s row of parts.'),
] + [
    T(f'13bii{n}', f'Q13(b)(ii){n}', 'C', item(13, n, end, 'pinna semi-circular canals'), [pt(row, 3)], 'bio-2-4',
      concept, sq, 3, decision=EACH_ITEM)
    for n, end, row, concept, sq in [
        (1, 'Briefly outline the function of the pinna.', S('Collects sound'), 'pinna', SQ(13, 'Function of pinna:')),
        (2, 'To which part of the body does the Eustachian tube link the ear?', S('Throat or pharynx'),
         'eustachian-tube-link', SQ(13, 'Eustachian tube connected to:')),
        (3, 'What is the role of the Eustachian tube?', same('Role of Eustachian tube:', 'Throat or pharynx'),
         'eustachian-tube-role', lab(13, 'Role of Eustachian tube:')),
        (4, 'Name another part of the ear that has a function similar to that of the stirrup.', S('Hammer or anvil'),
         'ossicles', SQ(13, '(ii)', path=['13.', '(b)'], bare=True,
                        paired='The scheme labels this item "Other ossicle", a word the paper does not print.')),
        (5, 'Suggest why there are three semi-circular canals in each ear.',
         same('Why three semi-circular canals:', 'Hammer or anvil', '(or dimensions or axes)'), 'semicircular-canals',
         lab(13, 'Why three semi-circular canals:'))]
] + [
    T('13ci', 'Q13(c)(i)', 'C', Q(13, 'Name the part of the eye that has a corresponding function to the cochlea of the ear.',
                                  'Explain your answer.'),
      [pt(S('*Retina or *fovea'), 3),
       pt(S('Both contain receptors (or both detect stimuli) or both generate impulses', 'or both send impulses to the brain'),
          3, label=S('Why:'))], 'bio-2-4', 'retina-and-cochlea', SQ(13, 'Corresponding part of eye:'), 6),
    T('13cii1', 'Q13(c)(ii)1', 'C', item(13, 1, 'Name the structure that determines the diameter of the pupil.',
                                         'Light passes through the pupil'),
      [pt(S('*Iris'), 3)], 'bio-2-4', 'iris', SQ(13, 'Structure that determines pupil diameter:'), 3, stem=[Q13CII],
      decision=EACH_ITEM),
    T('13cii2', 'Q13(c)(ii)2', 'C', item(13, 2, 'Why is there a mechanism for changing the diameter of the pupil?',
                                         'Light passes through the pupil'),
      [pt(same('Why pupil diameter changeable:', '*Iris', 'to let more light enter the eye'), 3)], 'bio-2-4',
      'pupil-size', lab(13, 'Why pupil diameter changeable:'), 3, stem=[Q13CII], decision=EACH_ITEM),
    T('13ciii1', 'Q13(c)(iii)1', 'C', item(13, 1, 'Name two such parts.', 'transparent and have curved'),
      [pt(same('Transparent and curved:', 'to let more light enter the eye'), 3), pt(S('Lens'), 3)], 'bio-2-4',
      'cornea-and-lens', lab(13, 'Transparent and curved:'), 6, stem=[Q13CIII], decision=EACH_ITEM),
    T('13ciii2', 'Q13(c)(iii)2', 'C', item(13, 2, 'How does the curvature contribute to the functioning of the eye?',
                                           'transparent and have curved'),
      [pt(same('How curvature helps eye:', 'Lens'), 3)], 'bio-2-4', 'refraction-in-the-eye',
      lab(13, 'How curvature helps eye:'), 3, stem=[Q13CIII], decision=EACH_ITEM),
] + [
    T('13civ', 'Q13(c)(iv)', 'C', Q(13, 'The eyes of carnivores are located relatively close together at the front of the skull.',
                                    'suggest a benefit of either arrangement.'),
      [pt(S(*ans), 3, label=label)], 'bio-2-4', f'eye-position-in-{route}', SQ(13, sq), 3, route=route,
      decision='Carnivores or herbivores: the scheme prints an answer for each, joined by "OR", so each is a route card.')
    for route, sq, label, ans in [
        ('carnivores', 'Carnivores:', S('Carnivores:', after='How curvature helps eye'),
         ('Better judgement of distance or better focus on prey',)),
        ('herbivores', 'Herbivores:', S('Herbivores:', after='Better judgement of distance'),
         ('Better detection of predators or wider field of vision (to detect', 'predators)'))]
] + [
    T('14ai', 'Q14(a)(i)', 'C', Q(14, 'Explain the term species.'), [pt(same('Species:', '14.'), 3)], 'bio-1-5', 'species',
      lab(14, 'Species:'), 3, decision=ROW_PRICED),
    T('14aii', 'Q14(a)(ii)', 'C', Q14AII, [pt(S('*Variation'), 3)], 'bio-1-5', 'variation',
      SQ(14, 'Intraspecific differences:', paired=COMPRESSED), 3),
] + [
    T(f'14aiii{n}', f'Q14(a)(iii){n}', 'C', item(14, n, end, 'form the basis of evolution'), [anyn(S(*menu), 2, 3)],
      'bio-1-5', concept, SQ(14, sq), 6, stem=[M('(ii)', 14), Q14AII, Q14AIII], decision=EACH_ITEM)
    for n, end, menu, concept, sq in [
        (1, 'Explain the term evolution.', ('Genetic changes (in populations)/ in response to environment/',
                                            'over time/ giving rise to new species'), 'evolution', 'Evolution:'),
        (2, 'Outline the role of natural selection in evolution.',
         ('Better adapted survive/ reproduce/ adaptation is inherited/ adaptation', '(becomes) more common'),
         'natural-selection', 'Role of natural selection:')]
] + [
    T('14aiv', 'Q14(a)(iv)', 'C', Q(14, 'Explain the term mutation.'),
      [pt(S('A change in DNA (or gene or chromosome or genetic material)'), 3)], 'bio-2-3', 'mutation',
      SQ(14, 'Mutation:'), 3),
    T('14av1', 'Q14(a)(v)1', 'C', item(14, 1, 'Gene mutation.', 'disorder caused by:'),
      [pt(S('Sickle cell anaemia or any valid example'), 3)], 'bio-2-3', 'gene-mutation-disorder',
      SQ(14, 'Gene mutation disorder:'), 3, stem=[Q14AV], decision=EACH_ITEM),
    T('14av2', 'Q14(a)(v)2', 'C', item(14, 2, 'Chromosome mutation.', 'disorder caused by:'),
      [pt(same('Chromosome mutation disorder:', 'Sickle cell anaemia'), 3)], 'bio-2-3', 'chromosome-mutation-disorder',
      lab(14, 'Chromosome mutation disorder:'), 3, stem=[Q14AV], decision=EACH_ITEM),
    T('14avi', 'Q14(a)(vi)', 'C', Q(14, 'Give one cause of the differences referred to in (ii) above, other than mutation.'),
      [pt(S('Sexual reproduction or meiosis or formation of gametes', 'or fertilisation of gametes or independent assortment'),
          3)], 'bio-1-5', 'causes-of-variation', SQ(14, 'Cause of variation:', paired=COMPRESSED), 3,
      stem=[M('(ii)', 14), Q14AII]),
    T('14bi', 'Q14(b)(i)', 'C', Q(14, 'Cells can be classified as either prokaryotic or eukaryotic.',
                                  'Give two features of eukaryotic cells which distinguish them from prokaryotic cells.'),
      [anyn(same('Eukaryotic cell features:', 'or fertilisation of gametes', '(or chloroplasts or mitochondria)'), 2, 3)],
      'bio-1-3', 'eukaryotic-features', lab(14, 'Eukaryotic cell features:'), 6, decision=ROW_PRICED),
    T('14bii', 'Q14(b)(ii)', 'C', Q14BII,
      [pt(S('Named tissue + matching function (plant)'), 3, kind='criterion', note=NO_ANSWER)], 'bio-1-3',
      'plant-tissue-function', SQ(14, 'Function of plant tissue:'), 3),
    T('14biii', 'Q14(b)(iii)', 'C', Q14BIII,
      [pt(same('Function of animal tissue:', 'Named tissue + matching function (plant)'), 3, kind='criterion',
          note=NO_ANSWER)], 'bio-1-3', 'animal-tissue-function', lab(14, 'Function of animal tissue:'), 3),
    T('14biv', 'Q14(b)(iv)', 'C', Q(14, 'In the case of each of the tissues referred to in (ii) and (iii) above, state one way in which the',
                                    'tissue is adapted to carry out the function that you have indicated.'),
      [pt(S('Named plant tissue + matching adaptation'), 3, kind='criterion', note=NO_ANSWER),
       pt(S('Named animal tissue + matching adaptation'), 3, kind='criterion', note=NO_ANSWER)], 'bio-1-3',
      'tissue-adaptations',
      SQ(14, '(iv)', path=['14.', '(b)'], bare=True,
         paired='The scheme heads this part "Adaptations", not a reprint of the ask.'), 6,
      stem=[M('(ii)', 14), Q14BII, M('(iii)', 14), Q14BIII]),
    T('14bv', 'Q14(b)(v)', 'C', Q(14, 'How does an organ differ from a tissue?'),
      [pt(S('Organ is a group of tissues (working together)'), 3)], 'bio-1-3', 'organs-and-tissues',
      SQ(14, 'Organ v. tissue:'), 3),
    T('14bvi1', 'Q14(b)(vi)1', 'C', item(14, 1, 'What is meant by the term tissue culture?', 'How does an organ differ'),
      [pt(same('Tissue culture:', 'Organ is a group of tissues', 'outside the organism or growth of cells in vitro'), 3)],
      'bio-1-3', 'tissue-culture', lab(14, 'Tissue culture:'), 3, decision=EACH_ITEM),
    T('14bvi2', 'Q14(b)(vi)2', 'C', item(14, 2, 'State two requirements for successful tissue culture.', 'How does an organ differ'),
      [anyn(same('Requirements:', 'growth of cells in vitro', 'oxygen supply'), 2, 3)], 'bio-1-3',
      'tissue-culture-requirements', lab(14, 'Requirements:'), 6, decision=EACH_ITEM),
    T('14ci1', 'Q14(c)(i)1', 'C', item(14, 1, 'What do you understand by the term turgor in plant cells?', '2. State two requirements'),
      [pt(S('Pressure of cell contents against the cell wall'), 3)], 'bio-2-6', 'turgor', SQ(15, 'Turgor:'), 3,
      decision=EACH_ITEM),
    T('14ci2', 'Q14(c)(i)2', 'C', item(14, 2, 'How do plant cells remain turgid for a considerable period of time?',
                                       '2. State two requirements'),
      [pt(same('How plant cells stay turgid:', 'Pressure of cell contents'), 3), pt(S('By osmosis (or explained)'), 3)],
      'bio-2-6', 'staying-turgid', lab(15, 'How plant cells stay turgid:'), 6, decision=EACH_ITEM),
    T('14ci3', 'Q14(c)(i)3', 'C', item(14, 3, 'What happens to a plant if many of its cells lose turgidity?',
                                       '2. State two requirements'),
      [pt(same('Consequence for plant of turgidity loss:', 'By osmosis', 'or droop'), 3)], 'bio-2-6', 'wilting',
      lab(15, 'Consequence for plant of turgidity loss:', paired=COMPRESSED), 3, decision=EACH_ITEM),
    T('14ci4', 'Q14(c)(i)4', 'C', item(14, 4, 'Explain your answer.', '2. State two requirements'),
      [pt(S('Bursts'), 3, label=S('Animal cell:', after='or droop')), pt(S('No cell wall'), 3, label=S('Why:'))],
      'bio-2-6', 'animal-cells-burst', SQ(15, 'Animal cell:'), 6, decision=EACH_ITEM),
    T('14cii1', 'Q14(c)(ii)1', 'C', item(14, 1, 'by writing one sentence about each term.', 'turgid, suggest what may happen'),
      [pt(S('Diffusion: Movement (of material) from region of high concentration to a', 'region of low(er) concentration',
            after='No cell wall'), 3),
       pt(S('Osmosis: Movement of water from a region of high water concentration to a', 'membrane'), 3)],
      'bio-2-6', 'diffusion-and-osmosis', lab(15, 'Diffusion:'), 6, decision=EACH_ITEM),
    T('14cii2', 'Q14(c)(ii)2', 'C', item(14, 2, 'Name the location and a material involved.', 'turgid, suggest what may happen'),
      [pt(S('Nephron or named part'), 3, label=S('Active transport; location:', after='membrane')),
       pt(S('Glucose or amino acid(s) or salt(s) or water'), 3, label=S('Active transport; material:'))], 'bio-2-6',
      'active-transport', SQ(15, 'Active transport; location:'), 6, decision=EACH_ITEM),
    T('15ai', 'Q15(a)(i)', 'C', Q(15, 'Draw a labelled diagram of a transverse section and a labelled diagram of a longitudinal',
                                  'section through a human vein to show its structure.'),
      [pt(S('thin wall + large lumen (> 50% total diameter)'), 3, kind='criterion',
          label=S('T.S. vein diagram:', after='15.'), note_sel=S('3, 0'), note_lead='The scheme marks this diagram'),
       pt(S('clearly longitudinal + valve'), 3, kind='criterion', label=S('L.S. vein diagram:'),
          note_sel=S('3, 0', after='L.S. vein diagram:'), note_lead='The scheme marks this diagram'),
       anyn(S('lumen/ muscle or wall or endothelium/ valve'), 3, 1)], 'bio-2-6', 'drawing-a-vein',
      SQ(16, 'T.S. vein diagram:', paired=COMPRESSED), 9,
      decision='Each drawing is priced as one item ("3, 0") and its labels "3(1)": the two drawings and the label '
               'menu are the part\'s rows.'),
] + [
    T(f'15aii{n}', f'Q15(a)(ii){n}', 'C', item(15, n, end, 'name a vein which fits'), [pt(row, 3)], 'bio-2-6', concept,
      sq, 3, stem=[Q15AII], decision=EACH_ITEM)
    for n, end, row, concept, sq in [
        (1, 'Transports blood out of the muscle of the heart.', same('Heart muscle:', '3(1)'), 'coronary-vein',
         lab(16, 'Heart muscle:')),
        (2, 'Brings blood away from the kidneys.', S('Renal (vein)'), 'renal-vein', SQ(16, 'Kidney:')),
        (3, 'Carries very little carbon dioxide.', S('Pulmonary (vein)'), 'pulmonary-vein',
         SQ(16, 'Little CO2:', paired=COMPRESSED)),
        (4, 'Brings blood into the right atrium.', S('Vena cava'), 'vena-cava', SQ(16, 'Into R.A.:', paired=COMPRESSED)),
        (5, 'Has capillaries at both ends.', same('Capillaries at both ends:', 'Vena cava'), 'hepatic-portal-vein',
         lab(16, 'Capillaries at both ends:'))]
] + [
    T('15aiii', 'Q15(a)(iii)', 'C', Q(15, 'Briefly describe how blood is moved through veins.'),
      [anyn(S('(Skeletal or voluntary) muscles contracting (squeezing)/ valves prevent backflow'), 2, 3)], 'bio-2-6',
      'blood-flow-in-veins', SQ(16, 'How blood moved through veins:'), 6),
    T('15bi1', 'Q15(b)(i)1', 'C', item(15, 1, 'in the endometrium.', 'State one change that occurs'),
      [pt(S('Breaks down (shed)'), 3), pt(S('(Days) 1 – 5'), 3)], 'bio-2-5', 'endometrium-in-the-cycle',
      SQ(17, 'Endometrium:'), 6, stem=[Q15B, Q15BI],
      decision=EACH_ITEM + ' The scheme prints each change with its days ("3 + 3"), the changes joined by "or": '
                           'answer variants of one task.'),
    T('15bi2', 'Q15(b)(i)2', 'C', item(15, 2, 'in the ovary.', 'State one change that occurs'),
      [pt(S('Follicle (or ovum or egg) matures'), 3), pt(S('(Days) 1 – 14'), 3)], 'bio-2-5', 'ovary-in-the-cycle',
      SQ(17, 'Ovary:'), 6, stem=[Q15B, Q15BI],
      decision=EACH_ITEM + ' The scheme prints each change with its days ("3 + 3"), the changes joined by "or": '
                           'answer variants of one task.'),
    T('15bii', 'Q15(b)(ii)', 'C', Q(15, 'FSH and LH each plays a role in the cycle. Where in the body are these hormones produced?'),
      [pt(same('Where FSH and LH produced:', '(Days) 15 – 28'), 3)], 'bio-2-5', 'pituitary',
      lab(17, 'Where FSH and LH produced:'), 3, stem=[Q15B]),
    T('15biii', 'Q15(b)(iii)', 'C', Q(15, 'State one role of each of these hormones in the cycle.'),
      [pt(S('Stimulates follicle (egg) to develop (in ovary) or stimulates (ovary) to',
            'produce oestrogen or stimulates LH (production)'), 3, label=S('FSH:', after='*Pituitary')),
       pt(S('Stimulates ovulation or described or causes (Graafian follicle) to develop',
            'into corpus luteum or stimulates progesterone (production)'), 3, label=S('LH:'))], 'bio-2-5',
      'fsh-and-lh', SQ(17, 'FSH:'), 6, stem=[Q15B, M('(ii)', 15), Q15BII]),
    T('15biv', 'Q15(b)(iv)', 'C', Q15BIV, [anyn(same('Other hormones:', 'into corpus luteum'), 2, 3)], 'bio-2-5',
      'oestrogen-and-progesterone', lab(17, 'Other hormones:'), 6, stem=[Q15B]),
] + [
    T('15bv', 'Q15(b)(v)', 'C', Q(15, 'Stating clearly which of the two hormones you have chosen from (iv), give a function in the',
                                  'cycle of that hormone.'),
      [pt(S(ans), 3, label=S(lab_))], 'bio-2-5', f'function-of-{route}',
      SQ(17, '(v)', path=['15', '(b)'], bare=True, paired=NO_REPRINT), 3, route=route,
      stem=[Q15B, M('(iv)', 15), Q15BIV],
      decision='Oestrogen or progesterone: the scheme prints a function for each, joined by "OR", so each is a '
               'route card.')
    for route, lab_, ans in [
        ('oestrogen', 'Fn oestrogen:', 'Causes endometrium to build up or inhibits FSH or stimulates LH'),
        ('progesterone', 'Fn progesterone:', 'Maintains endometrium or inhibits LH or inhibits FSH')]
] + [
    T('15ci', 'Q15(c)(i)', 'C', Q(15, 'Long bones contain both yellow marrow and red marrow.',
                                  'Give one function of each type of marrow.'),
      [pt(S('Yellow marrow: YStores fat or converts to red marrow', after='15.', piece=2, psep=': Y'), 3,
          label=S('Yellow marrow: YStores fat or converts to red marrow', after='15.', piece=1, psep=': Y')),
       pt(S('Produces blood cells'), 3, label=S('Red marrow:'))], 'bio-2-4', 'bone-marrow', lab(18, 'Yellow marrow:'),
      6, decision='The text layer carries a stray "Y" before "Stores fat", a glyph the page masks to a sliver; the '
                  'answer is cut from its label at the scheme\'s colon and that glyph.'),
] + [
    T(f'15cii{n}', f'Q15(c)(ii){n}', 'C', item(15, n, end, 'presence of a named disease'),
      [pt(row, 3, kind='criterion', note=NO_ANSWER)], topic, concept, sq, 3, stem=[Q15CII],
      decision=EACH_ITEM + ' The scheme marks each "3, 2, 0".')
    for n, end, row, topic, concept, sq in [
        (1, 'A dietary deficiency of a named water-soluble vitamin.',
         same('Lack of water-soluble vitamin in diet:', '(ii)', 'matching recognition'), 'bio-1-2',
         'vitamin-deficiency', lab(18, 'Lack of water-soluble vitamin in diet:')),
        (2, 'A genetically sex-linked disease, other than haemophilia.', S('Named disease + matching recognition'),
         'bio-1-4', 'sex-linked-disease', SQ(18, 'Sex-linked:')),
        (3, 'Excessive secretion of a named hormone.', S('Named hormone + matching recognition'), 'bio-2-4',
         'excess-hormone', SQ(18, 'Excess hormone:', paired=COMPRESSED)),
        (4, 'Caused by a virus.', S('Named disease + matching recognition'), 'bio-1-1', 'viral-disease',
         SQ(18, 'Virus:'))]
] + [
    T(f'15ciii{n}', f'Q15(c)(iii){n}', 'C', item(15, n, end, 'biological basis of each'), [pt(row, 3)], topic, concept,
      sq, 3, stem=[Q15CIII], decision=EACH_ITEM)
    for n, end, row, topic, concept, sq in [
        (1, 'The use of micro-organisms in waste management.', S('Composting or decomposition or decay'), 'bio-3-2',
         'microorganisms-and-waste', SQ(18, 'Microorganisms & waste:', paired=COMPRESSED)),
        (2, 'Vaccination.', same('Vaccination:', 'Composting or decomposition'), 'bio-2-4', 'vaccination',
         lab(18, 'Vaccination:')),
        (3, 'The artificial propagation of flowering plants.', same('Artificial propagation:', 'Stimulates antibody'),
         'bio-2-5', 'artificial-propagation', lab(18, 'Artificial propagation:')),
        (4, 'Increasing the amount of wholegrain foods in the diet.',
         same('Increasing wholegrain foods in diet:', 'Maintain desired trait', 'alimentary canal'), 'bio-2-6',
         'wholegrain-foods', lab(18, 'Increasing wholegrain foods in diet:'))]
]

ANSWER_VARIANTS = {
    '4biii': [
        ('sufferer-female', 'Sufferer female',
         [pt(S('XnY–'), 3, label=S('Genotype:'), note_sel=S('Male genotypes and phenotypes:', after='Males')),
          pt(S('Sufferer'), 3, label=S('Phenotype:')),
          pt(S('XnXn'), 3, label=S('Genotype:', nth=2), note_sel=S('Female genotypes and phenotypes:')),
          pt(S('Sufferer', nth=2), 3, label=S('Phenotype:', nth=2), note_sel=S('(or lethal for haemophilia)')),
          pt(S('Male only needs to inherit the recessive allele (from mother)',
               'is a sufferer (or lethal for haemophilia)'), 3, label=S('Explain:'))]),
        ('normal-female', 'Normal female',
         [pt(S('XnY–'), 3, label=S('Genotype:'), note_sel=S('Male genotypes and phenotypes:', after='Males')),
          pt(S('Sufferer'), 3, label=S('Phenotype:')),
          pt(S('XNXn'), 3, label=S('Genotype:', nth=3), note_sel=S('Female genotypes and phenotypes:')),
          pt(S('Normal'), 3, label=S('Phenotype:', nth=3)),
          pt(S('Male only needs to inherit the recessive allele (from mother)',
               'is a sufferer (or lethal for haemophilia)'), 3, label=S('Explain:'))]),
    ],
    '5d': [
        ('fuse', 'Fuse with egg and polar nuclei',
         [pt(S('(One) fuses with the egg (nucleus)'), 3), pt(S('(The other) fuses with the (2) polar nuclei'), 3)]),
        ('gametes', 'Form gametes and disintegrate',
         [pt(S('(One) forms gametes'), 3), pt(S('(The other) disintegrates'), 3)]),
    ],
    '11biv': [
        ('water-split', 'Water split',
         [pt(S('Water split/ using light (energy)', piece=1), 3), pt(S('Water split/ using light (energy)', piece=2), 3)]),
        ('photolysis', 'Photolysis',
         [pt(S('Photolysis/ of water', piece=1), 3), pt(S('Photolysis/ of water', piece=2), 3)]),
    ],
    '11ciii': [
        ('further-krebs', 'Further point from the Krebs cycle',
         [pt(S('Oxidative fate of pyruvate: Converted to Acetyl (Co- Enzyme A) or enters', 'mitochondrion', piece=2,
               psep=': '), 3),
          anyn(S('CO2 produced/ ATP produced/ NADH produced'), 2, 3,
               note_sel=S('Any one further point from 1 or from 2.')),
          anyn(S('or electron transport system: protons (or H+ ions) combine with O2 or electrons', 'to make ATP',
                 piece=2, psep=': '), 1, 3)]),
        ('further-electron-transport', 'Further point from the electron transport system',
         [pt(S('Oxidative fate of pyruvate: Converted to Acetyl (Co- Enzyme A) or enters', 'mitochondrion', piece=2,
               psep=': '), 3),
          anyn(S('CO2 produced/ ATP produced/ NADH produced'), 1, 3),
          anyn(S('or electron transport system: protons (or H+ ions) combine with O2 or electrons', 'to make ATP',
                 piece=2, psep=': '), 2, 3, note_sel=S('Any one further point from 1 or from 2.'))]),
    ],
    '15bi1': [
        ('breaks-down', 'Breaks down', [pt(S('Breaks down (shed)'), 3), pt(S('(Days) 1 – 5'), 3)]),
        ('thickens', 'Thickens', [pt(S('Thickens'), 3), pt(S('(Days) 6 – 28'), 3)]),
    ],
    '15bi2': [
        ('follicle-matures', 'Follicle matures',
         [pt(S('Follicle (or ovum or egg) matures'), 3), pt(S('(Days) 1 – 14'), 3)]),
        ('ovulation', 'Ovulation', [pt(S('Ovulation'), 3), pt(S('(Days) 13 – 15'), 3)]),
        ('corpus-luteum', 'Corpus luteum develops', [pt(S('Corpus luteum develops'), 3), pt(S('(Days) 15 – 28'), 3)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-yeast': ('paper', 3, (215, 58, 390, 228), SEC, [],
                 'Line drawing of two joined cells: a large round cell, labelled parent cell, with a small round '
                 'nucleus holding coiled threads near its base, and a much smaller round cell, with a nucleus of its '
                 'own, attached to the top of the large cell by a narrow neck.', False),
    'q5-flower': ('paper', 5, (205, 68, 410, 275), SEC, ['A', 'B', 'C', 'D', 'E', 'F'],
                  'Shaded drawing of a flask-shaped structure: a flattened top on a long stalk over a swollen base. '
                  'Label A points to the flattened top and D to a small dark oval sitting on it. A pale band runs '
                  'from that oval down through the stalk into the base, B pointing to it in the stalk. In the base a '
                  'bracket marks out a region, labelled F, around a pale round sac with two small dots and a small '
                  'ringed dot, labelled C, near its foot, curved lines around it; the pale band ends beside the '
                  'ringed dot, and two lines labelled E point to two small dark dots inside the band near its end.',
                  False),
    'q10c-chain': ('paper', 10, (236, 497, 369, 523), SEC, [],
                   'The food chain as the paper prints it on one line: the capital letters A, B, C and D in a row, '
                   'with an arrow pointing from each letter to the next.', False),
    'q8b-axes': ('paper', 8, (120, 385, 515, 625), SEC, [],
                 'A pair of empty axes: a vertical line and a horizontal line meeting at the bottom left, with no '
                 'labels, scale or plotted lines.', False),
}
