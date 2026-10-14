"""Biology 2018 Higher Level — reviewed task ledger, carded from the paper for the first time.

Independent visual sweep (2026-10-14), every page rendered and read:
  * The 2018 paper is one booklet, 16 pages: p1 cover and instructions,
    p2-p6 Section A Questions 1-6, p7-p9 Section B Questions 7-9, p10-p15
    Section C Questions 10-15, p16 "Blank Page". Sections A and B are
    answered on the paper; Section C in an answer book.
  * The marking scheme, 24 pages: p1 cover, p2 note, p3-p5 introduction,
    cancelled and surplus answers, conventions, p6-p22 Questions 1-15 ("Page
    1 of 17" to "Page 17 of 17"), p23 "Blank Page", p24 back cover.

The paper's shape is the long-standing one: any five of Section A's six
questions, any two of Section B's three, any four of Section C's six, and
Q14 and Q15 are each any two of (a), (b), (c). Every printed ask is carded.

Every tariff in this scheme is an ordered split, carded at its first rate:
Q1 is the best five of six at 4; Q2-Q6 "2(5) + 5(2)" over seven responses;
Section B (a) "4 + 2" and (b) "4(4) + 4(2)"; Section C "4 + 3 + 2" for
(a), "2(5) + 3(4) + 2 + 3(1)" or "2(5) + 2(4) + 3 + 3(1)" for (b) and
(c), "4 + 2(2) + 1" for Q11(a), and "2(5) + 4(4) + 4(1)" for the parts of
Q14 and Q15. Where a part holds a drawing priced on its own (Q11(b)(i),
Q12(b)(i)'s equation, Q14(b)(i)) the drawing keeps its own marks beside a
second ladder over the rest of the part ("2(3) + 2 + 2(1)", "5 + 3(4) +
4(1)", "4(3) + 4(1)"); a ladder over a drawing's labels ("2(3) + 2 + 3(1)",
"2(3) + 2(1)") is one menu priced step by step.

The paper prints Q14(a)'s fifth part as "(iv)" a second time; the scheme
numbers it (v), and so do the cards (the census reader is told, gated to
this sitting).

Printed choices the scheme marks differently per option are routes: Q5(c)(i)
and (ii) shoot or root, Q10(c)(i) moving or sessile animals, Q13(c)(iii)
fossils, embryology, anatomy or biochemistry.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, allof, T, L, G

YEAR, LEVEL = 2018, 'hl'
REVIEWED_AT = '2026-10-14'

SOURCES = {
    'paper': {'path': 'examiner-reports/biology/papers/2018-hl-paper.pdf',
              'fileid': 'LC025ALP000EV.pdf',
              'sha256': 'db8bc21dffed971869311c1abf978c023b8a6e2ea4eda5d50ccf183b2a23ffd5',
              'pages': 16},
    'scheme': {'path': 'examiner-reports/biology/schemes/2018-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '61d87b1be7544b7fda5671c4eddf5311c9ef0f3558a901d49591a2eead57c6e5',
               'pages': 24},
}

PAGE_ROLES = {
    'paper': {1: 'cover', **{p: 'questions' for p in range(2, 16)}, 16: 'blank'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples', 5: 'conventions',
               **{p: 'marking' for p in range(6, 23)}, 23: 'blank', 24: 'back-cover'},
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
PART_TOTALS = {}
BEST_OF = {1: (5, 4)}
LADDERS = {
    **{q: _ladder('2(5) + 5(2)') for q in range(2, 7)},
    **{(n, 'a'): _ladder('4 + 2') for n in (7, 8, 9)},
    **{(n, 'b'): _ladder('4(4) + 4(2)') for n in (7, 8, 9)},
    **{(n, 'a'): _ladder('4 + 3 + 2') for n in (10, 12, 13)},
    (10, 'b'): _ladder('2(5) + 3(4) + 2 + 3(1)'), (10, 'c'): _ladder('2(5) + 2(4) + 3 + 3(1)'),
    (11, 'a'): _ladder('4 + 2(2) + 1'),
    # Q11(b)(i): the drawing "6, 4, 0" and its labels "2(3) + 2 + 3(1)" are
    # priced on their own; "2(3) + 2 + 2(1)" runs over (ii) and (iii).
    (11, 'B'): _ladder('2(3) + 2 + 2(1)', fixed={6: 1, 3: 2, 2: 1, 1: 3}),
    (11, 'c'): _ladder('2(5) + 2(4) + 3 + 3(1)'),
    # Q12(b)(i): "Equation 6, 4, 0"; "parts (ii) to (vi), inclusive 5 + 3(4) + 4(1)".
    (12, 'B'): _ladder('5 + 3(4) + 4(1)', fixed={6: 1}),
    (12, 'c'): _ladder('2(5) + 2(4) + 3 + 3(1)'),
    (13, 'b'): _ladder('2(5) + 3(4) + 2 + 3(1)'), (13, 'c'): _ladder('2(5) + 2(4) + 3 + 3(1)'),
    (14, 'a'): _ladder('2(5) + 4(4) + 4(1)'),
    # Q14(b)(i): "Drawing 6, 4, 0; labels 2(3) + 2(1)"; "(ii), (iii), (iv), (v) 4(3) + 4(1)".
    (14, 'B'): _ladder('4(3) + 4(1)', fixed={6: 1, 3: 2, 1: 2}),
    (14, 'c'): _ladder('2(5) + 4(4) + 4(1)'),
    **{(15, x): _ladder('2(5) + 4(4) + 4(1)') for x in 'abc'},
}
LADDER_OF = {
    **{k: (11, 'B') for k in ('11bi', '11bii1', '11bii2', '11biii')},
    **{k: (12, 'B') for k in ('12bi', '12bii1', '12bii2', '12biii', '12biv', '12bv', '12bvi')},
    **{k: (14, 'B') for k in ('14bi', '14bii', '14biii', '14biv', '14bv')},
}
LADDER_EXEMPT = {'11bi', '12bi', '14bi'}

CHECKSUMS = {
    1: {4: 5, 2: 2},   # best five of six; (a) "4, 2, 0" over its two reasons
    **{q: {5: 7} for q in range(2, 7)},
    **{(n, 'a'): {4: 2} for n in (7, 8, 9)}, **{(n, 'b'): {4: 8} for n in (7, 8, 9)},
    (10, 'a'): {4: 3}, (10, 'b'): {5: 9}, (10, 'c'): {5: 8},
    (11, 'a'): {4: 4}, (11, 'b'): {6: 1, 3: 7, 2: 1, 1: 3}, (11, 'c'): {5: 8},
    (12, 'a'): {4: 3}, (12, 'b'): {6: 1, 5: 8}, (12, 'c'): {5: 8},
    (13, 'a'): {4: 3}, (13, 'b'): {5: 9}, (13, 'c'): {5: 8},
    (14, 'a'): {5: 10}, (14, 'b'): {6: 1, 3: 10, 1: 2}, (14, 'c'): {5: 10},
    **{(15, x): {5: 10} for x in 'abc'},
}

SCAN_PAGES = {'paper': range(1, 16)}
SELECTION_SCAN = [
    ('paper', 1, 'any five', 'Cover rubric, Section A: whole-question choice; every question is carded.'),
    ('paper', 1, 'any two', 'Cover rubric, Section B: whole-question choice; every question is carded.'),
    ('paper', 1, 'any four', 'Cover rubric, Section C: whole-question choice; every question is carded.'),
    ('paper', 2, 'any five', 'Section A rubric repeated.'),
    ('paper', 2, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the best five make 20.'),
    ('paper', 2, 'the following', 'Q1 parts list.'),
    ('paper', 2, 'or', 'Q1(f) "Name a test or give the chemicals": either form of the one answer; one row.'),
    ('paper', 2, 'the following', 'Q2 lead-in: every term asked, one card per letter.'),
    ('paper', 4, 'the following', 'Q4(b) "the following steps": all four steps ordered in one response.'),
    ('paper', 4, 'any two', 'Q4(e) "in any two of: an animal, a plant, a micro-organism": one menu of the three printed answer lists, claim two.'),
    ('paper', 5, 'either', 'Q5(c)(i) "either a shoot or a root": separate answers per option: ROUTES.'),
    ('paper', 5, 'or', 'Q5(c)(i), same choice.'),
    ('paper', 5, 'or', 'Q5(c)(i) "OR" between the Shoot and Root answer lines, same choice.'),
    ('paper', 5, 'or', 'Q5(c)(ii) "in a shoot or in a root": separate answers per option: ROUTES.'),
    ('paper', 5, 'or', 'Q5(c)(ii) "OR" between the answer lines, same choice.'),
    ('paper', 5, 'or', 'Q5(d) "auxins or related compounds": description.'),
    ('paper', 7, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('paper', 7, 'or', 'Q7(b)(i)1 "reactants or organisms": description.'),
    ('paper', 7, 'or', 'Q7(b)(i)2 "reactants or organisms": description.'),
    ('paper', 8, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('paper', 8, 'or', 'Q8(b) "light intensity or carbon dioxide concentration": either factor; marked on the same rows.'),
    ('paper', 9, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('paper', 9, 'or', 'Q9(b)(v) "few or no leaf yeasts": description.'),
    ('paper', 10, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('paper', 10, 'or', 'Q10(a)(iii) "three or four levels": description.'),
    ('paper', 10, 'the following', 'Q10(b) lead-in: every topic asked, one card each.'),
    ('paper', 10, 'any one', 'Q10(c)(iii) "any one of the abiotic conditions": one response.'),
    ('paper', 11, 'the following', 'Q11(b)(i) "labelling each of the following": all six labels; one menu.'),
    ('paper', 11, 'the following', 'Q11(c) lead-in: every part asked.'),
    ('paper', 11, 'the following', 'Q11(c)(i) "each of the following": one card per numbered item.'),
    ('paper', 12, 'the following', 'Q12(b) lead-in: every part asked.'),
    ('paper', 12, 'any one', 'Q12(b)(v) "any one of the products": one menu of the printed fates, claim one.'),
    ('paper', 12, 'the following', 'Q12(c) lead-in: every part asked.'),
    ('paper', 12, 'or', 'Q12(c)(iii) "enzymes or yeast cells": description.'),
    ('paper', 13, 'both', 'Q13(a) lead-in "both nucleic acids": description.'),
    ('paper', 13, 'both', 'Q13(b)(ii) "heterozygous for both height and seed colour": description.'),
    ('paper', 13, 'any one', 'Q13(c)(iii) "any one named source": separate answers per source: ROUTES.'),
    ('paper', 14, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 14, 'both', 'Q14(c)(i) "both an exocrine and endocrine organ": description.'),
    ('paper', 15, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('paper', 15, 'the following', 'Q15(b) lead-in: every explanation asked, one card each.'),
    ('paper', 15, 'or', 'Q15(b)(v) "high sugar or high salt": either; marked on the same rows.'),
    ('paper', 15, 'the following', 'Q15(c)(i) "each of the following": one card per numbered item.'),
    ('paper', 15, 'or', 'Q15(c)(iii) "of the eye or of the ear": marked on one disorder row and one measure row; one card.'),
]

ROUTES = {
    'Q5(c)(i)': ['shoot', 'root'],
    'Q5(c)(ii)': ['shoot', 'root'],
    'Q10(c)(i)': ['moving-animals', 'sessile-animals'],
    'Q13(c)(iii)': ['fossils', 'embryology', 'anatomy', 'biochemistry'],
}

SEC = 'State Examinations Commission'
COMPRESSED = 'The scheme heads each answer with a compressed reprint of the ask.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry.'
NO_REPRINT = 'The scheme heads this part with its marker and tariff only, no reprint of the ask.'


def item(page, n, end, anchor):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, after=anchor, br=True)


def term(page, word, br=False):
    """A printed term the paper sets before its answer line ("Habitat. ____")."""
    return Q(page, word, word, br=br)


Q1 = Q(2, 'Answer any five of the following parts (a) to (f):')
Q2 = Q(2, 'From your knowledge of ecology, explain the following terms:')
Q3 = Q(3, 'The diagram represents the cell cycle.')
Q5B = Q(5, 'With regard to auxins, state:')
Q6 = Q(6, 'The diagram shows the structure of a nephron and part of its associated blood supply.')
Q7BI = Q(7, 'When carrying out certain experiments at the laboratory bench:')
Q7BII = Q(7, 'When you used yeast to prepare alcohol:')
Q7BIII = Q(7, 'When using a microscope to examine biological specimens, describe how you:')
Q7BIV = Q(7, 'In relation to investigations you carried out on food, state:')
Q8A = Q(8, 'The process of photosynthesis in plants is divided into two stages, the light stage and the',
        'dark stage.')
Q8B = Q(8, 'Answer the following questions in relation to an activity that you carried out to investigate',
        'the influence of light intensity or carbon dioxide concentration on the rate of photosynthesis.')
Q9B = Q(9, 'Answer the following questions in relation to your investigation into the growth of leaf',
        'yeast using agar plates.')
Q10B = Q(10, 'Write notes on the following.')
Q11C = Q(11, 'Answer the following questions from your knowledge of the human nervous system.')
Q11CI = Q(11, 'Outline the role of each of the following in the transmission of a nerve impulse:')
Q12B = Q(12, 'Answer the following questions from your knowledge of respiration.')
Q12C = Q(12, 'Answer the following questions from your knowledge of enzymes.')
Q13A = Q(13, 'Most organisms contain both nucleic acids, RNA and DNA.')
Q13B = Q(13, 'Gregor Mendel studied the inheritance of various traits in pea plants.',
         'The results of some of his investigations are presented in the table.')
Q14AV = Q(14, 'The graph below shows variations in the dry mass of peas over a period of time',
          'after germination. Give a reason for:')
Q14CII = Q(14, 'Using your knowledge of the endocrine role of the pancreas, state:')
Q15AII = Q(15, 'Bacteria reproduce asexually.')
Q15AIII = Q(15, 'Penicillin is an example of an antibiotic produced in large quantities using the batch',
            'processing method.')
Q15B = Q(15, 'Give a detailed biological explanation for each of the following.')
Q15CI = Q(15, 'In relation to the human eye, name and explain the role of each of the following:')

F1_NOTE = S('Correct genotype and matching phenotype', 'Each excess incorrect F1 cancels a correct answer')
HEART_NOTE = S('Accept ‘controls heart rate’ once only i.e. for role of either SA node or AV node')
CROSS = [(f'F1 {i + 1}', clip, want) for i, (clip, want) in enumerate([
    ((225, 335, 282, 389), 'TtYy Tall Yellow'), ((298, 335, 340, 389), 'Ttyy Tall Green'),
    ((370, 335, 425, 389), 'ttYy Dwarf Yellow'), ((443, 335, 485, 389), 'ttyy Dwarf Green')])]

TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', Q(2, 'Give the two main reasons why living organisms require food.'),
      [pt(S('Energy (source) or (cellular) respiration'), 2),
       pt(S('(Raw materials) for growth or (raw materials) for repair or anabolism'), 2)], 'bio-1-2',
      'why-food-is-needed', SQ(6, 'Why living organisms require food:'), 4, stem=[Q1],
      decision='The scheme prices the two reasons "4, 2, 0": 2 for each.'),
] + [
    T(f'1{x}', f'Q1({x})', 'A', Q(2, *ask), [pt(S(*ans), 4)], 'bio-1-2', concept, SQ(6, sq), 4, stem=[Q1])
    for x, ask, ans, concept, sq in [
        ('b', ('What is a polysaccharide?',), ('(A carbohydrate or molecule composed of) many sugar (or named',
                                               'monosaccharide) units (or molecules)'), 'polysaccharide',
         'Polysaccharide:'),
        ('c', ('Name the main structural polysaccharide in plants.',), ('Cellulose [allow pectin]',), 'cellulose',
         'Main structural polysaccharide in plants:'),
        ('d', ('Describe the composition of a triglyceride molecule.',), ('Glycerol and three fatty acids',),
         'triglyceride', 'Triglyceride molecule composition:'),
        ('e', ('Give a structural role of lipids in the human body.',), ('(Found in) membranes [allow insulation]',),
         'structural-role-of-lipids', 'Structural role of lipids:'),
        ('f', ('Name a test or give the chemicals used to demonstrate the presence of protein in a food', 'sample.'),
         ('Biuret or copper sulfate and sodium hydroxide',), 'test-for-protein',
         'Name of test or chemicals used to demonstrate the presence of protein:')]
] + [
    T(f'2{x}', f'Q2({x})', 'A', term(2, word), [pt(S(*ans), 5)], 'bio-3-1', concept, SQ(6, sq), 5, stem=[Q2])
    for x, word, ans, concept, sq in [
        ('a', 'Biotic factor.', ('Living (factor)',), 'biotic-factor', 'Biotic factor:'),
        ('b', 'Habitat.', ('Where an organism (or a plant or an animal) lives [allow plurals]',), 'habitat',
         'Habitat:'),
        ('c', 'Community.', ('All the organisms in an area (or habitat or ecosystem)',), 'community', 'Community:'),
        ('d', 'Population.', ('All the organisms of a (particular) species (living in an area)',
                              'or all the organisms of the same species (living in an area)'), 'population',
         'Population:'),
        ('e', 'Niche.', ('The role of an organism (or plant or animal or population)', '(in its ecosystem)'), 'niche',
         'Niche:'),
        ('f', 'Biosphere.', ('The part of the earth (planet) where life can exist',
                             'or the part of the earth (planet) inhabited by (living) organisms'), 'biosphere',
         'Biosphere:'),
        ('g', 'Qualitative survey.', ('(To establish) the presence (or absence) of species (or organism)',),
         'qualitative-survey', 'Qualitative survey:')]
] + [
    T('3a', 'Q3(a)', 'A', Q(3, 'What stage of the cell cycle is represented by X?'),
      [pt(S('X = Interphase'), 5)], 'bio-2-3', 'interphase', SQ(7, '(a)', path=['3.'], bare=True, paired=NO_REPRINT),
      5, stem=[Q3], fig='q3-cell-cycle', labels=[L('X', S('X = Interphase', page=7, piece=2, psep=' = '), True)]),
    T('3b', 'Q3(b)', 'A', Q(3, 'There are two types of cell division, mitosis and meiosis. Define mitosis.'),
      [pt(S('(Cell or nuclear division) forming two'), 5),
       pt(S('Identical (daughter) cells (or nuclei) or same chromosome number as parent'), 5)], 'bio-2-3',
      'mitosis', SQ(7, 'Mitosis:'), 10, stem=[Q3], fig='q3-cell-cycle',
      decision='The scheme prints the definition as two lines, each a response on the ladder.'),
    T('3c', 'Q3(c)', 'A', Q(3, 'State two ways in which meiosis differs from mitosis.'),
      [anyn(S('Four (new cells or nuclei) produced/ variation (or not identical)/ chromosome number', 'halved'),
            2, 5)], 'bio-2-3', 'meiosis-and-mitosis', SQ(7, 'Two ways meiosis differs from mitosis:'), 10,
      stem=[Q3], fig='q3-cell-cycle'),
    T('3d', 'Q3(d)', 'A', Q(3, 'Explain the term cancer.'),
      [pt(S('(A group of disorders due to) uncontrolled'), 5), pt(S('(Rate of) mitosis (or cell division)'), 5)],
      'bio-2-3', 'cancer', SQ(7, 'Cancer:'), 10, stem=[Q3], fig='q3-cell-cycle',
      decision='The scheme prints the explanation as two lines, each a response on the ladder.'),
    T('4a', 'Q4(a)', 'A', Q(4, 'What is meant by the term genetic engineering?'),
      [pt(S('Manipulation of genes or alteration of genes or alteration of genotypes or alteration of', 'DNA'), 5)],
      'bio-3-3', 'genetic-engineering', SQ(7, 'Genetic engineering:'), 5),
    T('4b', 'Q4(b)', 'A', [Q(4, 'Genetic engineering involves the following steps but not necessarily in the order given.',
                             'Rewrite these steps, placing them in the correct order.'),
                           Q(4, 'Transformation; Cutting; Isolation; Expression.', br=True)],
      [allof([(None, S('1. Isolation')), (None, S('2. Cutting')), (None, S('3. Transformation')),
              (None, S('4. Expression'))], 5)], 'bio-3-3', 'steps-of-genetic-engineering',
      SQ(7, 'Genetic engineering steps:'), 5,
      decision='The order is one response on the ladder: the four steps in one row.'),
] + [
    T(f'4c-{slug}', 'Q4(c)', 'A', [Q(4, 'Briefly explain what is meant by isolation and expression in relation to genetic engineering.'),
                           term(4, label + '.', br=True)],
      [pt(S(*ans), 5)], 'bio-3-3', f'{slug}-in-genetic-engineering', SQ(7, f'{label}:'), 5, item=(slug, label),
      decision=EACH_ITEM)
    for slug, label, ans in [
        ('isolation', 'Isolation', ('Identifying (or locating) gene or removal of a gene (or of a piece of',
                                    'DNA or of a plasmid)')),
        ('expression', 'Expression', ('(The gene causes the) production of protein (or product)',))]
] + [
    T('4d', 'Q4(d)', 'A', Q(4, 'In genetic engineering, DNA molecules called cloning vectors are used during',
                            'cloning vectors.'),
      [pt(S('Plasmids'), 5)], 'bio-3-3', 'plasmids', SQ(7, 'Rings of DNA in bacteria used as cloning vectors:'), 5),
    T('4e', 'Q4(e)', 'A', [Q(4, 'Give one application of genetic engineering in any two of:'),
                           Q(4, 'an animal, a plant, a micro‐organism.')],
      [anyn(None, 2, 5, options=[S('in animals:', 'Clotting factors or lactose-free milk or growth hormone or other valid answer'),
                                 S('in plants:', 'or rice producing Vitamin A or improved yield or other valid answer'),
                                 S('in micro-organisms:', 'of antibiotics) or oil breakdown or other valid answer')])],
      'bio-3-3', 'applications-of-genetic-engineering', SQ(7, 'Application of genetic engineering'), 10,
      decision='Any two of three kinds of organism: one menu of the three printed answer lists.'),
    T('5a', 'Q5(a)', 'A', Q(5, 'What is an auxin?'),
      [pt(S('A plant growth regulator (or promoter or inhibitor)'), 5)], 'bio-2-4', 'auxin', SQ(8, 'Auxin:'), 5),
    T('5bi', 'Q5(b)(i)', 'A', Q(5, 'A precise location in plants where they are produced.'),
      [pt(S('Shoot tips or root tips or meristematic (tissue) or seeds or buds or young leaves'), 5)], 'bio-2-4',
      'where-auxin-is-made', SQ(8, 'Precise location of auxin production in plants:'), 5, stem=[Q5B]),
    T('5bii', 'Q5(b)(ii)', 'A', Q(5, 'One example of an inhibitory function.'),
      [pt(S('Apical dominance or slows (prevents) the growth in side branches or slows mitosis',
            '(or slows cell division)'), 5)], 'bio-2-4', 'inhibitory-auxin', SQ(8, 'Inhibitory function of auxin:'), 5,
      stem=[Q5B]),
] + [
    T('5ci', 'Q5(c)(i)', 'A', Q(5, 'Exactly how does an unequal concentration of auxin in the elongation zone affect',
                                'the growth of either a shoot or a root?'),
      [pt(S(*ans), 5)], 'bio-2-4', f'unequal-auxin-in-{route}', SQ(8, 'How unequal concentration of auxin affects growth of shoot or root:'),
      5, route=route,
      decision='Shoot or root: the scheme prints a separate answer for each, joined by "OR", so each is a route card.')
    for route, ans in [('shoot', ('Shoot: higher auxin concentration results in higher rate of cell division (or more',
                                  'growth) (or vice-versa)')),
                       ('root', ('Root: higher auxin concentration results in lower rate of cell division (or less',
                                 'growth) (or vice-versa)'))]
] + [
    T('5cii', 'Q5(c)(ii)', 'A', Q(5, 'Suggest what could cause an unequal concentration of auxin in a shoot or in a root?'),
      [pt(S(ans), 5)], 'bio-2-4', f'cause-of-unequal-auxin-in-{route}',
      SQ(8, 'Cause of unequal concentration of auxin in shoot or root:'), 5, route=route,
      decision='Shoot or root: the scheme prints a separate answer for each, joined by "OR", so each is a route card.')
    for route, ans in [('shoot', 'Shoot: Difference in light direction (or explained) or gravity'),
                       ('root', 'Root: Gravity or difference in water concentration')]
] + [
    T('5d', 'Q5(d)', 'A', Q(5, 'State two uses in horticulture of auxins or related compounds.'),
      [anyn(S('(Promote) ripening in fruit/ tissue culture/ rooting powder/ weed killers/ seedless fruit'), 2, 5)],
      'bio-2-4', 'uses-of-auxins', SQ(8, 'Uses of auxins in horticulture:'), 10),
] + [
    T(f'6a-{x.lower()}', 'Q6(a)', 'A', Q(6, 'Name the structures labelled X and Y.'),
      [pt(S(ans, after=f'{x} ='), 5)], 'bio-2-6', concept, SQ(8, f'{x} =', paired='The scheme names each letter '
                                                                               'under its own "X =" / "Y =".'),
      5, stem=[Q6], fig='q6-nephron', item=(x.lower(), x), decision=EACH_ITEM,
      labels=[L(y, S(a, page=8, after=f'{y} ='), y == x) for y, a in [('X', 'Bowman’s capsule'),
                                                               ('Y', 'Distal (convoluted) tubule (or DCT)')]])
    for x, ans, concept in [('X', 'Bowman’s capsule', 'bowmans-capsule'),
                            ('Y', 'Distal (convoluted) tubule (or DCT)', 'distal-tubule')]
] + [
    T('6b', 'Q6(b)', 'A', Q(6, 'Draw a line from the ‘Target area’ box above, to a precise location on the diagram to',
                            'indicate where the hormone ADH has its effect.'),
      [pt(S('Line drawn to distal convoluted tubule or to collecting duct'), 5, kind='criterion')], 'bio-2-6',
      'where-adh-acts', SQ(8, 'Target area of ADH:'), 5, stem=[Q6], fig='q6-nephron'),
    T('6c', 'Q6(c)', 'A', Q(6, 'Briefly describe the effect of ADH on its target area.'),
      [pt(S('It becomes more permeable to water or more water is reabsorbed'), 5)], 'bio-2-6', 'effect-of-adh',
      SQ(8, 'Effect of ADH on target area:'), 5, stem=[Q6], fig='q6-nephron'),
    T('6d', 'Q6(d)', 'A', Q(6, 'What change in blood composition triggers the secretion of ADH?'),
      [pt(S('Increasing (salt) concentration or decreasing water concentration'), 5)], 'bio-2-6', 'trigger-for-adh',
      SQ(8, 'Change in blood composition that triggers secretion of ADH:'), 5, stem=[Q6], fig='q6-nephron'),
    T('6e', 'Q6(e)', 'A', Q(6, 'Name the endocrine gland in which ADH is produced.'),
      [pt(S('Hypothalamus [allow (posterior) pituitary]'), 5)], 'bio-2-6', 'where-adh-is-made',
      SQ(8, 'Where ADH produced:'), 5, stem=[Q6], fig='q6-nephron'),
    T('6f', 'Q6(f)', 'A', Q(6, 'Suggest one possible treatment for kidney failure.'),
      [pt(S('Dialysis or transplant'), 5)], 'bio-2-6', 'kidney-failure', SQ(8, 'Possible treatment for kidney failure:'),
      5, stem=[Q6], fig='q6-nephron'),
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', Q(7, 'Why is it important that scientists publish the results of their research?'),
      [pt(S('Information made widely available or to spread knowledge or peer review'), 4)], 'bio-u2', 'why-publish',
      SQ(9, 'Why it is important that scientists publish results of their research:'), 4),
    T('7aii', 'Q7(a)(ii)', 'B', Q(7, 'How can scientists avoid bias in scientific experiments?'),
      [pt(S('Large sample size or replicates or double blind testing or random sampling or use', 'of placebo'), 4)],
      'bio-u2', 'avoiding-bias', SQ(9, 'How scientists avoid bias in experiments:'), 4),
] + [
    T(f'7b{r}{n}', f'Q7(b)({r}){n}', 'B', item(7, n, end, anchor), [pt(S(*ans), 4)], topic, concept, SQ(9, sq), 4,
      stem=[stem], decision=EACH_ITEM)
    for r, n, end, anchor, stem, ans, topic, concept, sq in [
        ('i', 1, 'constant pH over a period of a few hours?', 'at the laboratory bench:', Q7BI,
         ('(Use) a (pH) buffer',), 'bio-2-1', 'constant-ph', '1.'),
        ('i', 2, 'constant temperature over a period of a few hours?', 'at the laboratory bench:', Q7BI,
         ('Water bath or incubator',), 'bio-2-1', 'constant-temperature', '2.'),
        ('ii', 1, 'What other product was produced during the fermentation?', 'When you used yeast to prepare alcohol:',
         Q7BII, ('Carbon dioxide (or CO2)',), 'bio-2-2', 'other-product-of-fermentation', '1.'),
        ('ii', 2, 'What test did you use to confirm the presence of alcohol?', 'When you used yeast to prepare alcohol:',
         Q7BII, ('Iodoform (test) or sodium hypochlorite + potassium iodide or other valid', 'test'), 'bio-2-2',
         'testing-for-alcohol', '2.'),
        ('iii', 1, 'Calculated the magnifying power of the microscope.', 'describe how you:', Q7BIII,
         ('Multiply (the power of the) eyepiece (lens) by (the power of the) objective', '(lens)'), 'bio-1-3',
         'magnifying-power', '1.'),
        ('iii', 2, 'Altered the amount of light shining on your specimens.', 'describe how you:', Q7BIII,
         ('Adjust the diaphragm (or condenser) or adjust the lamp or adjust the mirror',), 'bio-1-3',
         'adjusting-the-light', '2.'),
        ('iv', 1, 'dry out.', 'In relation to investigations you carried out on food, state:', Q7BIV,
         ('To ensure (translucent) stain is not just water (or explained)',), 'bio-1-2', 'drying-the-fat-test', '1.'),
        ('iv', 2, 'Which other food test required the application of heat.',
         'In relation to investigations you carried out on food, state:', Q7BIV,
         ('Reducing sugar or Benedict’s or Fehling’s (test)',), 'bio-1-2', 'food-test-needing-heat', '2.')]
] + [
    T('8ai', 'Q8(a)(i)', 'B', Q(8, 'Where in the cell does the dark stage take place?'),
      [pt(S('*Chloroplast'), 4)], 'bio-2-2', 'where-the-dark-stage-happens',
      SQ(10, 'Where in cell dark stage takes place:'), 4, stem=[Q8A]),
    T('8aii', 'Q8(a)(ii)', 'B', Q(8, 'Why is the dark stage called the dark stage?'),
      [pt(S('Light is not required or light independent or can occur in the dark'), 4)], 'bio-2-2',
      'why-dark-stage', SQ(10, 'Why dark stage is called dark stage:'), 4, stem=[Q8A]),
    T('8bi', 'Q8(b)(i)', 'B', Q(8, 'Name the plant you used for this investigation.'),
      [pt(S('Elodea (or pondweed) or named aquatic plant'), 4)], 'bio-2-2', 'plant-for-photosynthesis',
      SQ(10, 'Plant:', paired=COMPRESSED), 4, stem=[Q8B]),
    T('8bii', 'Q8(b)(ii)', 'B', Q(8, 'Give a reason for using this plant.'),
      [pt(S('(Aquatic plant) produces bubbles or gas easily seen'), 4)], 'bio-2-2', 'why-pondweed',
      SQ(10, 'Why this plant:'), 4, stem=[Q8B]),
    T('8biii', 'Q8(b)(iii)', 'B', Q(8, 'How did you measure the rate of photosynthesis?'),
      [pt(S('(Counted) the number of bubbles per unit time or (measured) the volume of gas',
            'per unit time (or per stated time)'), 4)], 'bio-2-2', 'measuring-photosynthesis',
      SQ(10, 'How rate of photosynthesis measured:'), 4, stem=[Q8B]),
    T('8biv', 'Q8(b)(iv)', 'B', Q(8, 'Label the axes below, and sketch a graph to show how the rate of photosynthesis',
                                  'would change as your chosen factor varied over a wide range.'),
      [pt(S('X-axis = Light (intensity) or carbon dioxide (concentration) and Y-axis = rate or',
            'number of bubbles (or volume) per unit time (or per stated time)'), 4),
       pt(S('Graph increasing'), 4, kind='criterion', label=S('Plot:')),
       pt(S('Graph levels off'), 4, kind='criterion', label=S('Plot:'))], 'bio-2-2', 'photosynthesis-graph',
      SQ(10, 'Graph axes:', paired=COMPRESSED), 12, stem=[Q8B], qfig='q8b-iv-axes',
      decision='The axes and the plot are three responses on the ladder; the printed axes are shown as printed.'),
    T('8bv', 'Q8(b)(v)', 'B', Q(8, 'Explain the shape of your graph.'),
      [pt(S('As light (intensity) increases or as carbon dioxide (concentration) increases, rate',
            '(or photosynthesis) increases'), 4),
       pt(S('Rate levels off as saturation point reached (or due to limiting factor) (or explained)'), 4)],
      'bio-2-2', 'shape-of-the-graph', SQ(10, 'Reason for shape of graph:'), 8, stem=[Q8B]),
    T('9ai', 'Q9(a)(i)', 'B', Q(9, 'Name the fungus, other than yeast, that you have studied as part of your course.'),
      [pt(S('Rhizopus'), 4)], 'bio-3-2', 'rhizopus', SQ(11, 'Other fungus:'), 4),
    T('9aii', 'Q9(a)(ii)', 'B', Q(9, 'Give one way the fungus you have named in part (i) differs from yeast.'),
      [pt(S('Multicellular or has hyphae (or mycelium or rhizoids) or produces (zygo)spores'), 4)], 'bio-3-2',
      'rhizopus-and-yeast', SQ(11, 'How different from yeast:', paired=COMPRESSED), 4),
    T('9bi', 'Q9(b)(i)', 'B', Q(9, 'Mention two aseptic techniques you carried out to ensure a pathogen‐free',
                                'environment.'),
      [anyn(S('Minimal opening of containers/ wash bench with disinfectant/ flaming (or', 'disinfectant'), 2, 4)],
      'bio-3-2', 'aseptic-technique', SQ(11, 'Aseptic techniques'), 8, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', Q(9, 'What type of agar is recommended for optimal growth of yeast and other fungi?'),
      [pt(S('Malt (agar) [allow nutrient (agar)]'), 4)], 'bio-3-2', 'malt-agar', SQ(11, 'Type of agar for fungi:'), 4,
      stem=[Q9B]),
    T('9biii', 'Q9(b)(iii)', 'B', Q(9, 'Describe how the plates were stored, from introduction of the yeast source until',
                                    'yeast growth was visible on the agar.'),
      [anyn(S('Right side up/ (right-side up) for (first) 24 – 48 hours/ upside down/ in incubator (or',
              'at 15 - 30 ◦C)/ for 2-7 days'), 3, 4)], 'bio-3-2', 'storing-the-plates',
      SQ(11, 'How plates stored until yeasts visible:'), 12, stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', Q(9, 'How did you identify the leaf yeast growing on the agar?'),
      [pt(S('Pink (colonies)'), 4)], 'bio-3-2', 'identifying-leaf-yeast', SQ(11, 'How identify leaf yeast on agar:'), 4,
      stem=[Q9B]),
    T('9bv', 'Q9(b)(v)', 'B', Q(9, 'Suggest a reason why few or no leaf yeasts may have grown on the agar.'),
      [pt(S('(Air) pollution or time of year or recent rainfall or unsuitable temperature or wind',
            'or damage during handling or no yeast on leaf'), 4)], 'bio-3-2', 'few-leaf-yeasts',
      SQ(11, 'Why few or no leaf yeasts on the agar:'), 4, stem=[Q9B]),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', [Q(10, 'Draw a pyramid of numbers to represent the information in the food chain below.'),
                                 Q(10, 'Rose bush Caterpillars Blackbirds Hawk', br=True)],
      [pt(S('Correct pyramid'), 4, kind='criterion')], 'bio-3-1', 'pyramid-of-numbers',
      SQ(12, 'Pyramid of numbers:'), 4, qfig='q10a-i-chain',
      decision='The food chain is printed with arrows between its organisms: shown as printed.'),
    T('10aii', 'Q10(a)(ii)', 'C', Q(10, 'What term is used to describe the organisms at the top of food chains?'),
      [pt(S('Top (or tertiary) consumer(or carnivore or predator)'), 4)], 'bio-3-1', 'top-consumer',
      SQ(12, 'Organisms at top of food chains:'), 4),
    T('10aiii', 'Q10(a)(iii)', 'C', Q(10, 'Explain why pyramids of numbers are usually restricted to three or four levels.'),
      [pt(S('Due to large energy loss (at each level) or to small energy transfer (at each level)'), 4)], 'bio-3-1',
      'levels-in-a-pyramid', SQ(12, 'Why pyramids of numbers usually restricted to three or four levels:'), 4),
    T('10bi', 'Q10(b)(i)', 'C', Q(10, 'Factors which influence the size of the human population.'),
      [anyn(None, 3, 5, options=[S('War:'), S('Famine:'), S('Disease:'), S('Contraception:')],
            note_sel=S('Named factor and matching note'))], 'bio-3-1', 'human-population',
      SQ(12, 'Factors which influence the size of the human population:'), 15, stem=[Q10B]),
    T('10bii', 'Q10(b)(ii)', 'C', Q(10, 'Organism adaptations.'),
      [anyn(S('A structural feature (or change)/ a behavioural feature (or change)/ example/',
              'matching benefit/ natural selection or explained'), 3, 5)], 'bio-3-1', 'adaptations',
      SQ(12, 'Organism adaptations:'), 15, stem=[Q10B]),
    T('10biii', 'Q10(b)(iii)', 'C', Q(10, 'Conservation.'),
      [anyn(S('Management of the environment/ to maintain biodiversity/ to prevent extinction/',
              'named practice/ benefit of named practice'), 3, 5)], 'bio-3-1', 'conservation',
      SQ(12, 'Conservation:'), 15, stem=[Q10B]),
] + [
    T('10ci', 'Q10(c)(i)', 'C', Q(10, 'Describe the steps you would take to estimate the size of the population of a',
                                  'particular animal species in the ecosystem you have studied.'),
      [anyn(S(*menu), 5, 5, note_sel=S(lead))], 'bio-3-1', f'estimating-{route}',
      SQ(12, 'Estimation of size of an animal population:'), 25, route=route,
      decision='Moving or sessile animals: the scheme prints a separate menu of steps for each, joined by "OR", '
               'so each is a route card.')
    for route, lead, menu in [
        ('moving-animals', 'For moving animals:', ('Capture/ how captured / mark/ release in same place/ recapture/ count/ formula',
                                                   'or calculation described')),
        ('sessile-animals', 'For sessile or slow-moving animals:',
         ('Quadrat/ random/ how random/ count/ repeat (several times)/ record numbers (or', 'area)/ calculate population'))]
] + [
    T('10cii', 'Q10(c)(ii)', 'C', Q(10, 'Name a plant from the ecosystem you have studied and indicate two abiotic',
                                    'conditions which favour its presence.'),
      [anyn(S('e.g. light (intensity)/ (soil) pH/ temperature/ water (or rain)/ other valid condition'), 2, 5,
            note_sel=S('(Plant name) with two matching abiotic conditions'))], 'bio-3-1', 'abiotic-conditions',
      SQ(12, 'Abiotic conditions favouring a particular plant’s presence:'), 10),
    T('10ciii', 'Q10(c)(iii)', 'C', Q(10, 'How did you measure any one of the abiotic conditions mentioned in (ii)?'),
      [pt(S('Matching method to measure any one condition named in (ii)'), 5, kind='criterion')], 'bio-3-1',
      'measuring-an-abiotic-factor', SQ(12, 'How measured one abiotic factor:', paired=COMPRESSED), 5,
      stem=[M('(ii)', 10), Q(10, 'Name a plant from the ecosystem you have studied and indicate two abiotic',
                             'conditions which favour its presence.')]),
    T('11ai', 'Q11(a)(i)', 'C', Q(11, 'Blood acts as a transport medium in the human body. Name two substances, other',
                                  'than food molecules and water, that are transported in the blood.'),
      [anyn(S('Urea/ hormones (or a named hormone)/ antibodies/ oxygen/ carbon dioxide/',
              '(plasma) proteins/enzymes/ clotting factors (or a named clotting factor) Any two'), 2, 4)], 'bio-2-6',
      'what-blood-carries', SQ(13, 'Substances, other than food molecules and water, transported in the blood:'), 8),
    T('11aii', 'Q11(a)(ii)', 'C', Q(11, 'Give the location in the body where each of the substances you named in (i) enters',
                                    'the blood.'),
      [anyn(S('Urea enters at liver/ hormones enter at endocrine gland/ antibodies enter from (B)',
              'enzymes (or clotting factors or proteins) enter from liver Any two'), 2, 4)], 'bio-2-6',
      'where-substances-enter-blood', SQ(13, 'Locations where substances enter the blood:'), 8,
      stem=[M('(i)', 11), Q(11, 'Blood acts as a transport medium in the human body. Name two substances, other',
                            'than food molecules and water, that are transported in the blood.')]),
    T('11bi', 'Q11(b)(i)', 'C', [Q(11, 'Draw a diagram to show the structure of the human heart and associated blood',
                                   'vessels, labelling each of the following:'),
                                 Q(11, 'Vena cava; tricuspid valve; aorta; left ventricle; semi‐lunar valve; pulmonary artery.',
                                   br=True)],
      [pt(S('Drawing: Four chambers including their valves + four correctly placed main blood',
            'vessels + left ventricle wall thicker than right ventricle wall'), 6, kind='criterion',
          note_sel=S('Drawing 6, 4, 0')),
       anyn(S('Vena cava/ tricuspid valve/ aorta/ left ventricle/ semi-lunar valve/', 'pulmonary artery'), 6, 3,
            steps=[3, 3, 2, 1, 1, 1])],
      'bio-2-6', 'drawing-the-heart', SQ(13, '(i)', path=['11.', '11.'], bare=True, paired=NO_REPRINT), 17,
      decision='The drawing ("6, 4, 0") and its labels ("2(3) + 2 + 3(1)") are priced on their own.'),
    T('11bii1', 'Q11(b)(ii)1', 'C', item(11, 1, 'State the precise location and describe the role of the sinoatrial (SA) node.',
                                         'Draw a diagram to show the structure of the human heart'),
      [pt(S('*Right atrium'), 3),
       pt(S('Generates (or sends) (electrical) impulses or causes contraction in the atria (or',
            'causes atrial systole) or controls the heart rate'), 3, label=S('Role of SA node:'), note_sel=HEART_NOTE)],
      'bio-2-6', 'sa-node', SQ(13, '1. Precise location of the SA node:'), 6, decision=EACH_ITEM),
    T('11bii2', 'Q11(b)(ii)2', 'C', Q(11, '2. State the precise location and describe the role of the atrioventricular (AV) node.'),
      [pt(S('In septum between right atrium and right ventricle or in septum near tricuspid', 'valve'), 3),
       pt(S('Generates (or sends) (electrical) impulses or causes contraction in the ventricles (or',
            'causes ventricular systole) or controls the heart rate'), 3, label=S('Role of AV node:'), note_sel=HEART_NOTE)],
      'bio-2-6', 'av-node', SQ(13, '2. Precise location of the AV node:'), 6, decision=EACH_ITEM),
    T('11biii', 'Q11(b)(iii)', 'C', Q(11, 'What exactly is being measured when a person’s blood pressure is taken?'),
      [pt(S('Force of the blood against the wall of the artery or force required to stop flow of',
            'blood in the artery or systolic and diastolic pressures'), 3)], 'bio-2-6', 'blood-pressure',
      SQ(13, 'What is measured when a person’s blood pressure is taken:'), 3),
] + [
    T(f'11ci{n}', f'Q11(c)(i){n}', 'C', item(11, n, end, 'in the transmission of a nerve impulse:'),
      [pt(S(*ans), 5)], 'bio-2-4', concept, SQ(14, sq), 5, stem=[Q11C, Q11CI], decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'Dendrites', ('Receive impulses or carry impulses towards cell body',), 'dendrites', 'Role of dendrites:'),
        (2, 'Axon', ('Carries impulses away from cell body or carries impulses to effector (or named', 'example)'),
         'axon', 'Role of the axon:'),
        (3, 'Cell body.', ('Receives impulses or produces neurotransmitters or controls passage of impulses',
                           'or passes impulse to axon'), 'cell-body', 'Role of cell body:')]
] + [
    T('11cii', 'Q11(c)(ii)', 'C', Q(11, 'Describe how a nerve impulse is transmitted across a synaptic cleft, from one neuron',
                                    'to the next.'),
      [anyn(S('Impulse arrives (at synaptic knob)/ neurotransmitter(or named)/ released into',
              'recycled (or reabsorbed)'), 4, 5)], 'bio-2-4', 'synapse',
      SQ(14, 'How nerve impulse transmitted across synaptic cleft:'), 20, stem=[Q11C]),
    T('11ciii', 'Q11(c)(iii)', 'C', Q(11, 'Explain the importance of the myelin sheath in the transmission of a nerve impulse.'),
      [pt(S('Speeds up (transmission of nerve impulse)'), 5)], 'bio-2-4', 'myelin-sheath',
      SQ(14, 'Importance of myelin sheath in transmission of nerve impulse:'), 5, stem=[Q11C]),
    T('12ai', 'Q12(a)(i)', 'C', Q(12, 'Suggest an advantage to the cell of using ATP as an energy source, instead of',
                                  'breaking down a sugar molecule every time energy is needed.'),
      [pt(S('ATP releases energy in suitable (or fixed or manageable) quantities', 'recycled'), 4)], 'bio-1-2',
      'why-atp', SQ(15, 'Advantage to cell of using ATP as energy source:'), 4),
    T('12aii', 'Q12(a)(ii)', 'C', Q(12, 'Name the nitrogenous base and the sugar present in ATP.'),
      [pt(S('*Adenine'), 4), pt(S('*Ribose'), 4)], 'bio-1-2', 'adenine-and-ribose',
      SQ(15, 'Nitrogenous base in ATP:', paired='The scheme prints no "(ii)": it heads the base and the sugar '
                                                'with their own reprints.'), 8),
    T('12bi', 'Q12(b)(i)', 'C', Q(12, 'Give a balanced chemical equation to summarise the process of aerobic respiration.'),
      [pt(S('C6H12O6 + 6O2 → 6H2O + 6CO2'), 6, kind='criterion')], 'bio-2-2', 'respiration-equation',
      SQ(15, 'Balanced equation to summarise aerobic respiration:'), 6, stem=[Q12B],
      decision='The equation is priced "6, 4, 0" on its own, beside the ladder over (ii) to (vi).'),
    T('12bii1', 'Q12(b)(ii)1', 'C', item(12, 1, 'Name the storage polysaccharide in humans from which glucose is produced.',
                                         'Give a balanced chemical equation to summarise the process of aerobic respiration.'),
      [pt(S('*Glycogen'), 5)], 'bio-2-2', 'glycogen', SQ(15, '1. Human storage polysaccharide:'), 5,
      stem=[Q12B], decision=EACH_ITEM),
    T('12bii2', 'Q12(b)(ii)2', 'C', item(12, 2, 'Give one major storage location of this polysaccharide in the body.',
                                         'Give a balanced chemical equation to summarise the process of aerobic respiration.'),
      [pt(S('Liver or muscle'), 5)], 'bio-2-2', 'where-glycogen-is-stored',
      SQ(15, '2. A major storage location of this polysaccharide:'), 5,
      stem=[Q12B, item(12, 1, 'Name the storage polysaccharide in humans from which glucose is produced.',
                        'Give a balanced chemical equation to summarise the process of aerobic respiration.')],
      decision=EACH_ITEM),
    T('12biii', 'Q12(b)(iii)', 'C', Q(12, 'What happens to pyruvate molecules that prepares them for the Krebs cycle?'),
      [pt(S('Lose a carbon (atom) or lose CO2 or change from 3C to 2C or change to acetyl (Co-A)'), 5)], 'bio-2-2',
      'pyruvate', SQ(15, 'What happens to pyruvate molecules before Krebs cycle:'), 5, stem=[Q12B]),
    T('12biv', 'Q12(b)(iv)', 'C', Q(12, 'Name three products of the Krebs cycle.'),
      [anyn(S('ATP/ CO2/ NADH or hydrogen ions or electrons'), 3, 5)], 'bio-2-2', 'krebs-products',
      SQ(15, 'Krebs cycle products:'), 15, stem=[Q12B]),
    T('12bv', 'Q12(b)(v)', 'C', Q(12, 'Briefly describe the fate of any one of the products mentioned in part (iv) above.'),
      [anyn(None, 1, 5, options=[S('ATP:', 'in anabolic reaction (or example)'),
                                 S('CO2:', 'Released into atmosphere or used in photosynthesis'),
                                 S('NADH:', 'system'), S('H (ions):', 'Forms water')])], 'bio-2-2', 'fate-of-a-krebs-product',
      SQ(15, 'Fate of any one product:'), 5,
      stem=[Q12B, M('(iv)', 12), Q(12, 'Name three products of the Krebs cycle.')],
      decision='Any one product: one menu of the four printed fates, each with its product.'),
    T('12bvi', 'Q12(b)(vi)', 'C', Q(12, 'What is the final electron acceptor in aerobic respiration?'),
      [pt(S('*Oxygen'), 5)], 'bio-2-2', 'final-electron-acceptor',
      SQ(15, 'Final electron acceptor in aerobic respiration:'), 5, stem=[Q12B]),
    T('12ci', 'Q12(c)(i)', 'C', Q(12, 'Explain enzyme specificity with reference to the active site.'),
      [pt(S('Only one substrate'), 5), pt(S('Fits (or matches) the (shape of) active site'), 5)], 'bio-2-1',
      'specificity', SQ(15, 'Enzyme specificity with reference to the active site:'), 10, stem=[Q12C]),
    T('12cii', 'Q12(c)(ii)', 'C', Q(12, 'What happens to the activity of enzymes when they are placed in a medium',
                                    'Explain your answer.'),
      [pt(S('What happens: (Activity is) reduced'), 5),
       pt(S('Why: Shape of active site (or enzyme) changed or (enzyme) denatured'), 5)], 'bio-2-1', 'ph-and-enzymes',
      SQ(15, 'What happens to enzyme activity when outside optimum pH:'), 10, stem=[Q12C]),
    T('12ciii', 'Q12(c)(iii)', 'C', Q(12, 'Name two substances used in the school laboratory to immobilise enzymes or yeast',
                                      'cells.'),
      [pt(S('(Sodium) *alginate'), 5), pt(S('*Calcium chloride'), 5)], 'bio-2-1', 'immobilising-enzymes',
      SQ(15, 'Substances to immobilise enzymes:'), 10, stem=[Q12C]),
    T('12civ', 'Q12(c)(iv)', 'C', Q(12, 'Give two advantages of using immobilised enzymes.'),
      [anyn(S('Reusable (or longer-lasting)/ recovered easily/ pure product/ (allows for)', 'continuous flow process'),
            2, 5)], 'bio-2-1', 'immobilised-enzymes', SQ(15, 'Advantages of immobilised enzymes:'), 10, stem=[Q12C]),
    T('13ai', 'Q13(a)(i)', 'C', Q(13, 'Name the biologically active entities, each of which contains only one type',
                                  'of nucleic acid.'),
      [pt(S('*Viruses'), 4)], 'bio-1-2', 'viruses-nucleic-acid', SQ(16, 'Biologically active entities:'), 4, stem=[Q13A]),
    T('13aii', 'Q13(a)(ii)', 'C', Q(13, 'Name two locations in eukaryotic cells where RNA but no DNA is found.'),
      [pt(S('*Cytosol or *cytoplasm'), 4), pt(S('*Ribosome'), 4)], 'bio-1-2', 'where-rna-is-found',
      SQ(16, 'Where RNA but no DNA found in eukaryotic cells:'), 8, stem=[Q13A]),
] + [
    T(f'13bi-{slug}', 'Q13(b)(i)', 'C', Q(13, 'As a result of his work, he put forward two laws, the Law of Segregation and the Law',
                                  'of Independent Assortment. State each of these laws.'),
      [pt(S(*ans), 5)], 'bio-1-4', f'law-of-{slug}', SQ(16, f'{name}:'), 5, stem=[Q13B], fig='q13-table',
      item=(slug, name), decision=EACH_ITEM)
    for slug, name, ans in [
        ('segregation', 'Law of Segregation',
         ('Traits (or characteristics) are controlled by pairs of factors (or by pairs of genes) (or',
          'by a pair of alleles) which separate at gamete formation')),
        ('independent-assortment', 'Law of Independent Assortment',
         ('Members of a pair of factors (or genes or alleles) separate independently of',
          'can combine (randomly) with either member of another pair'))]
] + [
    T('13bii', 'Q13(b)(ii)', 'C', Q(13, 'A dwarf pea plant with green seeds was crossed with a plant heterozygous for', 'genes.'),
      [G('tokens', page=16, clip=(250, 268, 425, 288), expect='ttyy × TtYy', marks=5, label=S('Parents')),
       G('tokens', page=16, clip=(250, 295, 445, 315), expect='ty TY, Ty, tY, ty', marks=5, label=S('Gametes'))]
      + [G('tokens', page=16, clip=clip, expect=want, marks=5, note_sel=F1_NOTE) for _, clip, want in CROSS],
      'bio-1-4', 'dihybrid-cross', SQ(16, '(ii)', path=['13.', '13.'], bare=True,
                                       paired='The scheme sets the cross as a diagram under the marker "(ii)".'),
      30, stem=[Q13B], fig='q13-table', decision='Parents, gametes and the four offspring are six responses; each '
                                                 'offspring box is read from its printed position.'),
    T('13biii', 'Q13(b)(iii)', 'C', Q(13, 'Explain how the results of the cross in (ii) above would differ if the genes for height',
                                      'and seed colour were linked.'),
      [pt(S('They would be mostly (or all) parental phenotypes or mostly (or all) tall, yellow and',
            'yellow or would not get same (1:1:1:1) ratio or less variation'), 5)], 'bio-1-4', 'linkage',
      SQ(16, 'How results would differ if genes linked:'), 5, stem=[Q13B], fig='q13-table'),
    T('13ci', 'Q13(c)(i)', 'C', Q(13, 'What is meant by the term evolution?'),
      [pt(S('Inheritable (or genetic) change within a population (or species)'), 5),
       pt(S('In response to change in the environment or over time'), 5)], 'bio-1-5', 'evolution',
      SQ(16, 'Evolution:'), 10),
    T('13cii', 'Q13(c)(ii)', 'C', Q(13, 'Outline the theory of evolution by natural selection.'),
      [anyn(S('Variation/competition/ survival of better adapted/ better adapted leave more',
              'offspring/ traits passed on/ new species'), 3, 5)], 'bio-1-5', 'natural-selection',
      SQ(16, 'Theory of evolution by natural selection:'), 15),
] + [
    T('13ciii', 'Q13(c)(iii)', 'C', Q(13, 'Describe evidence in support of evolution from any one named source.'),
      [pt(S('Fossils or embryology or anatomy or biochemistry', piece=n, psep=' or '), 5, label=S('Source:')),
       pt(S(*ans, piece=1), 5, label=S(f'{name}:')), pt(S(*ans, piece=2), 5, label=S(f'{name}:'))],
      'bio-1-5', f'evidence-from-{route}', SQ(16, 'Evidence for evolution:'), 15, route=route,
      decision='Each named source has its own two answers ("Both answers for any one named source"), so each is a '
               'route card.')
    for n, route, name, ans in [
        (1, 'fossils', 'Fossils', ('Structure changing/ over time or related to environment',)),
        (2, 'embryology', 'Embryology', ('Different organisms have similar embryo stages/ similar', 'development pathways')),
        (3, 'anatomy', 'Anatomy', ('Named structure/ expansion point to emphasise common', 'ancestor')),
        (4, 'biochemistry', 'Biochemistry', ('Molecular structures common in related species/ similar',
                                              'metabolism in different species'))]
] + [
    T('14ai', 'Q14(a)(i)', 'C', [Q(14, 'Define dispersal in relation to seeds.'),
                                 Q(14, 'Suggest two reasons why dispersal is important to plants.')],
      [pt(S('Carrying the seeds (away from the parent plant)'), 5),
       anyn(S('Reduces competition/ avoids overcrowding/ ensures better survival rate/ colonises',
              'new areas or increases numbers'), 2, 5)], 'bio-2-5', 'dispersal', SQ(17, 'Dispersal:'), 15),
    T('14aii', 'Q14(a)(ii)', 'C', Q(14, 'Give one way in which a knowledge of seed dormancy is useful to humans.'),
      [pt(S('Correct environment for storage or optimum sowing time or maximise growing',
            'season or seed treatment before growth'), 5)], 'bio-2-5', 'dormancy',
      SQ(17, 'How knowledge of seed dormancy useful to humans:'), 5),
    T('14aiii', 'Q14(a)(iii)', 'C', Q(14, 'Other than water, name two essential environmental requirements for',
                                      'successful germination of seeds.'),
      [pt(S('Oxygen and (suitable) temperature'), 5)], 'bio-2-5', 'conditions-for-germination',
      SQ(17, 'Other environmental conditions for successful germination:'), 5,
      decision='The scheme prints both requirements as one answer, one response on the ladder.'),
    T('14aiv', 'Q14(a)(iv)', 'C', Q(14, 'What is the role of digestion and the role of respiration in seed germination?'),
      [pt(S('(Provides) soluble nutrients (or food)'), 5),
       pt(S('Provides (or releases) energy for growth or provides energy for embryo'), 5,
          label=S('Role of respiration in germination:'))], 'bio-2-5', 'digestion-and-respiration-in-germination',
      SQ(17, 'Role of digestion in germination:'), 10),
] + [
    T(f'14av{n}', f'Q14(a)(v){n}', 'C', Q(14, '1. The initial decrease in mass', piece=n, psep=psep),
      [pt(S(ans), 5)], 'bio-2-5', concept, SQ(17, sq), 5, stem=[Q14AV], fig='q14a-graph', decision=EACH_ITEM)
    for n, psep, ans, concept, sq in [
        (1, ' 2. ', 'Respiration or food being used up', 'initial-loss-of-mass', '1. Why initial decrease in mass:'),
        (2, '1. The initial decrease in mass ', 'Photosynthesis or food being made', 'later-gain-in-mass',
         '2. Why subsequent increase in mass:')]
] + [
    T('14avi', 'Q14(a)(vi)', 'C', Q(14, 'Name a substance which, because of its changing quantities in the seed, could be',
                                    'responsible for the changes shown in the graph.'),
      [pt(S('Glucose (or other named sugar) or starch or lipids'), 5)], 'bio-2-5', 'food-store-in-seeds',
      SQ(17, 'Substance that could be responsible for changes:'), 5, fig='q14a-graph'),
    T('14bi', 'Q14(b)(i)', 'C', Q(14, 'Draw a labelled diagram of a transverse section through a leaf.'),
      [pt(S('Upper epidermis + lower epidermis + two correctly-positioned', 'ground tissues'), 6, kind='criterion',
          label=S('Drawing:')),
       anyn(None, 4, 3, steps=[3, 3, 1, 1], options=[
           S('cuticle or upper epidermis or dermal tissue'), S('vascular bundle or vascular tissue or xylem or phloem'),
           S('palisade layer or spongy mesophyll or ground tissue or air spaces'), S('guard cells or stomata')])],
      'bio-2-6', 'drawing-a-leaf', SQ(18, 'T.S. of leaf:', 'T.S. of leaf:', paired=NO_REPRINT), 14,
      decision='The drawing ("6, 4, 0") and its labels ("2(3) + 2(1)") are priced on their own.'),
    T('14bii', 'Q14(b)(ii)', 'C', Q(14, 'Place the letter X on your diagram, to show the part of the leaf in which most',
                                    'photosynthesis occurs and explain why it occurs mostly there.'),
      [pt(S('X in correct position (on palisade layer)'), 3, kind='criterion'),
       pt(S('Closer to sunlight or more chloroplasts'), 3, label=S('Why there:'))], 'bio-2-2',
      'where-photosynthesis-happens', SQ(18, 'Where most photosynthesis occurs:'), 6),
    T('14biii', 'Q14(b)(iii)', 'C', Q(14, 'State two other ways in which the leaf is well adapted for photosynthesis.'),
      [anyn(S('Flat (or broad) (or large surface area)/ thin/ air spaces/ vascular system/ large',
              'number of chloroplasts/ stomata'), 2, 3)], 'bio-2-2', 'leaf-adaptations',
      SQ(18, 'Other ways leaf adapted for photosynthesis:'), 6),
    T('14biv', 'Q14(b)(iv)', 'C', Q(14, 'Name three substances which are involved in leaf metabolism and which pass',
                                    'through the stomata.'),
      [anyn(S('Carbon dioxide/ oxygen/ water'), 3, 3)], 'bio-2-6', 'gases-through-stomata',
      SQ(18, 'Three metabolic substances that pass through stomata:'), 9),
    T('14bv', 'Q14(b)(v)', 'C', Q(14, 'The concentration of which gas influences the diameter of the stomata?'),
      [pt(S('*Carbon dioxide'), 3)], 'bio-2-6', 'stomata-and-carbon-dioxide',
      SQ(18, 'Gas that influences diameter of stomata:'), 3),
    T('14ci', 'Q14(c)(i)', 'C', Q(14, 'The pancreas is both an exocrine and endocrine organ. Define the term endocrine.'),
      [pt(S('Ductless or secretes (products) into bloodstream'), 5)], 'bio-2-4', 'endocrine', SQ(19, 'Endocrine:'), 5),
] + [
    T(f'14cii{n}', f'Q14(c)(ii){n}', 'C', item(14, n, end, 'Using your knowledge of the endocrine role of the pancreas, state:'),
      [pt(S(*ans), 5)], 'bio-2-4', concept, SQ(19, sq), 5,
      stem=[Q14CII] + ([item(14, 1, 'A substance produced.', 'Using your knowledge of the endocrine role of the pancreas, state:')]
                       if n > 2 else []), decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'A substance produced.', ('Insulin',), 'insulin', '1. A substance produced:'),
        (2, 'The name of the endocrine tissue in the pancreas that produces it.', ('Islets of Langerhans',),
         'islets-of-langerhans', '2. Endocrine tissue:'),
        (3, 'A site of action of the substance mentioned in 1.', ('(Body) cells or liver',), 'where-insulin-acts',
         '3. A site of action of the substance:'),
        (4, 'The role of the substance mentioned in 1.', ('Absorption of glucose from blood',
                                                         'or lowers (or regulates) (blood) sugar levels'),
         'role-of-insulin', '4. The role of the substance:')]
] + [
    T('14ciii', 'Q14(c)(iii)', 'C', Q(14, 'Describe how a feedback mechanism works in the human endocrine system.'),
      [anyn(S('Production (or inhibition) of one hormone/ inhibits (or stimulates) the production',
              'of/ itself (or another hormone)/ can be positive or negative'), 3, 5,
            note_sel=S('[allow named hormones or other example]'))], 'bio-2-4', 'feedback',
      SQ(19, 'Feedback mechanism:'), 15),
    T('14civ', 'Q14(c)(iv)', 'C', Q(14, 'Give two examples of the use of hormone supplements.'),
      [anyn(S('Treatment of deficiency of named hormone (or of a named condition)/',
              'contraception/ fertility treatments/ HRT (for menopause)/ any valid answer'), 2, 5)], 'bio-2-4',
      'hormone-supplements', SQ(19, 'Uses of hormone supplements:'), 10),
    T('15ai', 'Q15(a)(i)', 'C', Q(15, 'Give one example of a beneficial effect of bacteria, other than the production of',
                                  'antibiotics, and one example of a harmful effect of bacteria.'),
      [pt(S('Decomposition or nutrient recycling or food production or vaccine (or hormone)',
            'production or aid digestion or produce vitamins in digestive system'), 5),
       pt(S('Food decay or (cause) disease or pathogenic'), 5, label=S('Harmful effect of bacteria:'))], 'bio-3-2',
      'bacteria-good-and-bad', SQ(20, 'Beneficial effect of bacteria:'), 10),
    T('15aii1', 'Q15(a)(ii)1', 'C', item(15, 1, 'Name the specific method of asexual reproduction used by bacteria.',
                                         'Bacteria reproduce asexually.'),
      [pt(S('*Binary fission'), 5)], 'bio-3-2', 'binary-fission', SQ(20, '1. Bacterial method of asexual reproduction:'),
      5, stem=[Q15AII], decision=EACH_ITEM),
    T('15aii2', 'Q15(a)(ii)2', 'C', item(15, 2, 'Describe this process of asexual reproduction.', 'Bacteria reproduce asexually.'),
      [anyn(S('DNA replicates/ cell elongates/ DNA (copies) move to opposite sides/ ingrowth of',
              'membrane (or walls)/ cell splits in two'), 3, 5)], 'bio-3-2', 'how-bacteria-divide',
      SQ(20, '2. Description of bacterial asexual reproduction:'), 15, stem=[Q15AII], decision=EACH_ITEM),
    T('15aiii1', 'Q15(a)(iii)1', 'C', item(15, 1, 'Describe batch processing.', 'processing method.'),
      [anyn(S('Fixed amount of nutrient added (at start)/ product removed at the end/ bacteria go',
              'through all (4/5) stages of the growth curve'), 2, 5, sep='/ ')], 'bio-3-2', 'batch-processing',
      SQ(20, '1. Batch processing:'), 10, stem=[Q15AIII],
      decision=EACH_ITEM + ' The menu is cut at "/ ": "(4/5) stages" is one answer.'),
    T('15aiii2', 'Q15(a)(iii)2', 'C', Q(15, '2. Explain why overuse of antibiotics is potentially dangerous.'),
      [pt(S('Development of resistant bacteria or described'), 5)], 'bio-3-2', 'antibiotic-overuse',
      SQ(20, '2. Why overuse of antibiotics is potentially dangerous:'), 5, stem=[Q15AIII], decision=EACH_ITEM),
    T('15aiv', 'Q15(a)(iv)', 'C', Q(15, 'How do certain bacteria survive when environmental conditions become',
                                    'unfavourable?'),
      [pt(S('(Form an) endospore'), 5)], 'bio-3-2', 'endospores',
      SQ(20, 'How certain bacteria respond to unfavourable conditions:'), 5),
] + [
    T(f'15b{r}', f'Q15(b)({r})', 'C', Q(15, *ask), [anyn(S(*menu), 2, 5)], topic, concept, SQ(21, sq), 10,
      stem=[Q15B])
    for r, ask, menu, topic, concept, sq in [
        ('i', ('Bile contains bile salts e.g. sodium hydrogencarbonate (NaHCO3).',),
         ('(They) emulsify fats/ neutralise acid from stomach or neutralise chyme/',
          'provide optimum (or suitable) pH for enzymes (in the duodenum)'), 'bio-2-6', 'bile-salts',
         'Bile contains bile salts:'),
        ('ii', ('Active immunity results in long‐lasting immunity.',),
         ('Antibodies produced/ by (body’s own) lymphocytes/ (production of)', 'memory cells'), 'bio-2-4',
         'active-immunity', 'Active immunity lasts:'),
        ('iii', ('Humans sweat during exercise.',),
         ('(Body) temperature increases/ sweat (or water) evaporates using heat', 'from body/ lowers (body) temperature'),
         'bio-2-4', 'sweating', 'Humans sweat during exercise:'),
        ('iv', ('Antibiotics should not be prescribed to directly treat influenza.',),
         ('Antibiotics are not effective against viruses (or influenza)/ influenza is', 'resistant bacteria'),
         'bio-3-2', 'antibiotics-and-flu', 'Antibiotics should not be prescribed for the flu:'),
        ('v', ('High sugar or high salt concentrations are used in the preservation of food.',),
         ('(The high sugar or salt concentration) causes bacteria (or fungi) to lose', 'bacteria (or fungi)'),
         'bio-2-6', 'preserving-food', 'High sugar or high salt concentrations used in food preservation:')]
] + [
    T('15ci1', 'Q15(c)(i)1', 'C', item(15, 1, 'The fluid that fills the rear chamber.', 'name and explain the role of each'),
      [pt(S('*Vitreous humour'), 5, label=S('Name:')),
       pt(S('Gives shape or transmits light or supports lens'), 5, label=S('Function:'))], 'bio-2-4',
      'vitreous-humour', SQ(22, '1. Fluid that fills rear chamber:'), 10, stem=[Q15CI], decision=EACH_ITEM),
    T('15ci2', 'Q15(c)(i)2', 'C', item(15, 2, 'The two types of light receptor cells.', 'name and explain the role of each'),
      [pt(S('*Rods and cones'), 5, label=S('Name:')),
       pt(S('Rods active (work in) dim light or BW vision'), 5, label=S('Function:')),
       pt(S('Cones active (work in) bright light or colour vision'), 5, label=S('Function:', nth=2))], 'bio-2-4',
      'rods-and-cones', SQ(22, '2. Both types of light receptor cells:'), 15, stem=[Q15CI], decision=EACH_ITEM),
    T('15ci3', 'Q15(c)(i)3', 'C', item(15, 3, 'The transparent covering in front of the cornea.',
                                       'name and explain the role of each'),
      [pt(S('*Conjunctiva'), 5, label=S('Name:')),
       pt(S('Protection against infection (or irritants) or moistens (or', 'lubricates)'), 5, label=S('Function:'))],
      'bio-2-4', 'conjunctiva', SQ(22, '3. Transparent covering on cornea:'), 10, stem=[Q15CI], decision=EACH_ITEM),
    T('15cii', 'Q15(c)(ii)', 'C', Q(15, 'Suggest an advantage to humans of having two eyes.'),
      [pt(S('Depth perception (judge distance) or increased visual field or 3D vision or', 'binocular vision'), 5)],
      'bio-2-4', 'two-eyes', SQ(22, 'Advantage of having two eyes:'), 5),
    T('15ciii', 'Q15(c)(iii)', 'C', Q(15, 'Name a disorder of the eye or of the ear and give a corrective measure for the',
                                      'disorder referred to.'),
      [pt(S('Appropriate disorder'), 5, kind='criterion'), pt(S('Matching corrective measure'), 5, kind='criterion')],
      'bio-2-4', 'eye-or-ear-disorder', SQ(22, 'Disorder of eye or ear with corrective measure:'), 10),
]

FIGURES = {
    'q3-cell-cycle': ('paper', 3, (204, 86, 401, 280), SEC, ['X', 'Y'],
                      'Circle divided into two sectors, a large one labelled X and a smaller wedge labelled Y, with a '
                      'curved arrow at the centre.', False),
    'q6-nephron': ('paper', 6, (160, 55, 385, 332), SEC, ['X', 'Y'],
                   'Drawing of a nephron and its blood supply, with label lines X and Y, and an empty box labelled '
                   'Target area below it.', False),
    'q8b-iv-axes': ('paper', 8, (100, 444, 545, 666), SEC, [],
                    'Part (iv) as printed: "Label the axes below, and sketch a graph to show how the rate of '
                    'photosynthesis would change as your chosen factor varied over a wide range." Below it a pair of '
                    'empty axes.', False),
    'q10a-i-chain': ('paper', 10, (100, 118, 545, 168), SEC, [],
                     'Part (a)(i) as printed: "Draw a pyramid of numbers to represent the information in the food '
                     'chain below." Below it the chain Rose bush, Caterpillars, Blackbirds, Hawk, joined by arrows.',
                     False),
    'q13-table': ('paper', 13, (148, 213, 442, 314), SEC, [],
                  'Table with two columns, Parental Cross and F1 Phenotype: Round x Wrinkled Seeds, All Round; Yellow x '
                  'Green Seeds, All Yellow; Purple x White Flowers, All Purple; Tall x Dwarf Plants, All Tall.', False),
    'q14a-graph': ('paper', 14, (225, 292, 420, 446), SEC, [],
                   'Graph of dry mass (g) against time (weeks), 1 to 4: the line falls a little at first to a low point '
                   'before week 1, then rises steadily to a peak between weeks 3 and 4 and turns down slightly.', False),
}
