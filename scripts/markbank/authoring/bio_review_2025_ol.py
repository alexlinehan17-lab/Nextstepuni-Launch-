"""Biology 2025 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 36 pages: p1 cover, p2
    instructions, p3-p8 Section A Questions 1-7, p9-p11 Section B Questions
    8-10, p12 Section C answerbook instructions, p13-p14 graph paper, p15-p34
    ruled answer pages, p35 acknowledgements, p36 back cover.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 acknowledgements, p12 back cover.
  * LC025GLP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7 Irish-medium
    bonus, p8-p34 Questions 1-17, p35 blank page, p36 back cover.

The sitting was already carded (133 cards, all shipped). As for 2025 Higher,
the review re-derives every task from the PDFs at the scheme's own mark
boundaries and corrects the existing cards in place: every id is kept, mapped
(`id=`) to the task it was carding, verified or corrected with its old fields
recorded; tasks the old cards bundled or missed are added. One shipped card,
bio-2025-ol-q16-ciii-fig ("Q16(c)(iii)-(iv)"), duplicated two others that
already carded (iii) and (iv) separately; it is withdrawn with a progress
alias to the (iii) card, which carries its task.

The Ordinary scheme prices Section A on ladders: Q1 and Q2 5(4); Q3-Q7 6(3)
+ 2, seven responses carded at 3 each with LADDERS pinning the ladder that
makes 20. Sections B and C print n(3) per part.

Finite printed routes: Q14(b)(v) xylem or phloem; Q17(b)(vi) arthritis or
osteoporosis. Q7(d)'s two printed pairs of differences are answer variants of
one task.

Answers the scheme prints as marks or drawings are read from glyph positions:
the Q3 true/false ticks; the Q1(b) formula letters; the labels of the Q1(c)
triglyceride the scheme reprints (its drawing is the solution figure); the
Q6(a) words written into the blanks.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2025, 'ol'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = '98d985b9d'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2025-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': '18d7bbfd7c80dd3a4d794f0b93f5b7b3878ad98235ae5ca4a3d364f4e9b37ae1',
            'pages': 36},
    '040': {'path': 'examiner-reports/biology/papers/2025-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': 'cb5f36e52e4ed56d66d6903ac53afe72759eea3881def5ef8bd627bfaefe1b35',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2025-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': 'abe98d1dd4ba6b6b10fec7064156fde4dd13ed4679e663aaafb4440d897cad8e',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 12)},
            12: 'answerbook-instructions', 13: 'graph-paper', 14: 'graph-paper',
            **{p: 'answer-pages' for p in range(15, 35)}, 35: 'acknowledgements',
            36: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'acknowledgements',
            12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 35)}, 35: 'blank', 36: 'back-cover'},
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
# "6(3) + 2": seven responses, six at 3 and the seventh at 2.
LADDERS = {q: [3, 3, 3, 3, 3, 3, 2] for q in (3, 4, 5, 6, 7)}

CHECKSUMS = {
    1: {4: 5}, 2: {4: 5}, **{q: {3: 7} for q in (3, 4, 5, 6, 7)},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in range(11, 16)}, **{(n, 'b'): {3: 9} for n in range(11, 16)},
    **{(n, 'c'): {3: 8} for n in range(11, 16)},
    **{(n, x): {3: 10} for n in (16, 17) for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 12), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'one of the following', 'Q1(a): one of two printed biomolecules; one answer.'),
    ('038', 3, 'one of the following', 'Q1(c): one of two printed structures; one answer.'),
    ('038', 4, 'choose', 'Q2 "Choose each term": a matching list, every term placed; one card per lettered description.'),
    ('038', 4, 'the following', 'Q2 term list.'),
    ('038', 4, 'the following', 'Q3 lead-in: every statement asked.'),
    ('038', 4, 'or', 'Q3 "true or false": the answer options.'),
    ('038', 5, 'or', 'Q4(a)(i) "plant cell or an animal cell": the answer options.'),
    ('038', 5, 'or', 'Q4(b) "the letter A or B": the answer options.'),
    ('038', 5, 'or', 'Q4(c) "the letter A or B": the answer options.'),
    ('038', 6, 'the following', 'Q5 list of four tropisms: every tropism matched.'),
    ('038', 6, 'one of the following', 'Q5(c): one of three printed tissues; one answer.'),
    ('038', 7, 'the following', 'Q6(a) word list: every word placed.'),
    ('038', 7, 'the following', 'Q6(b) word list: one word answers.'),
    ('038', 7, 'the following', 'Q6(c) lead-in: both functions asked.'),
    ('038', 9, 'any two', 'Section B rubric repeated.'),
    ('038', 9, 'the following', 'Q8(a)(ii): one of two printed units; one answer.'),
    ('038', 9, 'the following', 'Q8(b) lead-in: all four biomolecules asked.'),
    ('038', 10, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 11, 'the following', 'Q10(b) "the following diagram": a figure reference.'),
    ('038', 11, 'or', 'Q10(b)(ii) "A, B, C or D": the answer options.'),
    ('038', 11, 'or', 'Q10(b)(vi) "more reliable or fair": one question.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'one of the following', 'Q11(a)(iii): one of three printed terms; one answer.'),
    ('040', 2, 'the following', 'Q11(b) passage.'),
    ('040', 2, 'the following', 'Q11(c) word diagrams.'),
    ('040', 3, 'the following', 'Q12(a)(i) matching: both descriptions.'),
    ('040', 3, 'the following', 'Q12(a)(ii) the sentence to complete.'),
    ('040', 3, 'the following', 'Q12(b)(i) matching: both descriptions.'),
    ('040', 3, 'the following', 'Q12(c)(i) matching: all three descriptions.'),
    ('040', 3, 'any one', 'Q12(c)(iv)1 "any one application": open single answer; one card.'),
    ('040', 3, 'or', 'Q12(c)(iv)1 "(or use)": rewording.'),
    ('040', 3, 'any one', 'Q12(c)(iv)2 "any one application": open single answer; one card.'),
    ('040', 3, 'or', 'Q12(c)(iv)2 "(or use)": rewording.'),
    ('040', 4, 'one of the following', 'Q13(a)(i): one of two printed sentences; one answer.'),
    ('040', 4, 'or', 'Q13(a)(i) "(A or B)": the answer options.'),
    ('040', 4, 'the following', 'Q13(a)(ii) matching: both organelles.'),
    ('040', 4, 'the following', 'Q13(b) lead-in: every part asked.'),
    ('040', 4, 'or', 'Q13(b)(v) "anabolic or catabolic": the answer options.'),
    ('040', 4, 'the following', 'Q13(c)(ii)2: every statement classified.'),
    ('040', 4, 'or', 'Q13(c)(ii)2 "stage 1 or stage 2": the answer options.'),
    ('040', 4, 'one of the following', 'Q13(c)(iv): one of three printed terms; one answer.'),
    ('040', 5, 'or', 'Q14(b)(i) "1 or 2": the answer options.'),
    ('040', 5, 'or', 'Q14(b)(ii) "monocotyledonous or dicotyledonous": the answer options.'),
    ('040', 5, 'the following', 'Q14(b)(iii) matching: all three tissues.'),
    ('040', 5, 'either', 'Q14(b)(v) closed choose-one pool (xylem or phloem): ROUTES, one card each.'),
    ('040', 5, 'or', 'Q14(b)(v), same pool.'),
    ('040', 5, 'the following', 'Q14(c) lead-in: every part asked.'),
    ('040', 5, 'or', 'Q14(c)(i)1 "asexual or sexual": the answer options.'),
    ('040', 5, 'the following', 'Q14(c)(i)3 matching: all three images.'),
    ('040', 5, 'or', 'Q14(c)(ii)1 "asexual or sexual": the answer options.'),
    ('040', 5, 'any one', 'Q14(c)(ii)2 "any one method": open single answer; one card.'),
    ('040', 6, 'the following', 'Q15 lead-in: every part asked.'),
    ('040', 6, 'the following', 'Q15(b) lead-in: every part asked.'),
    ('040', 6, 'or', 'Q15(b)(i) "womb (or uterus)": rewording.'),
    ('040', 6, 'one of the following', 'Q15(b)(viii): one of two printed hormones; one answer.'),
    ('040', 6, 'the following', 'Q15(c)(i) matching: all three parts.'),
    ('040', 6, 'the following', 'Q15(c)(iv): both labels required.'),
    ('040', 6, 'or', 'Q15(c)(iv) "tail (or flagellum)": rewording.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'one of the following', 'Q16(a)(i): one of two printed terms; one answer.'),
    ('040', 7, 'or', 'Q16(a)(iii)1 "enzymes or living cells": one method immobilises either; the scheme prices one description; one card.'),
    ('040', 7, 'the following', 'Q16(b) lead-in: every part asked.'),
    ('040', 7, 'any two', 'Q16(b)(ii)2 "any two causes": open, priced per cause; one card.'),
    ('040', 7, 'the following', 'Q16(b)(iii) matching: all three terms.'),
    ('040', 8, 'the following', 'Q16(c) lead-in: every part asked.'),
    ('040', 8, 'both', 'Q16(c)(i) "both belong": description.'),
    ('040', 8, 'the following', 'Q16(c)(i) kingdom list: one answer.'),
    ('040', 8, 'the following', 'Q16(c)(ii) matching: all four parts.'),
    ('040', 8, 'one of the following', 'Q16(c)(v): one of two printed types; one answer.'),
    ('040', 8, 'or', 'Q16(c)(vi)1 "unicellular or multicellular": the answer options.'),
    ('040', 8, 'the following', 'Q16(d) lead-in: every part asked.'),
    ('040', 8, 'the following', 'Q16(d)(i): both labels required.'),
    ('040', 8, 'any two', 'Q16(d)(iii) "any two harmful examples": open, priced per example; one card.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'the following', 'Q17(a)(i) matching: all three parts.'),
    ('040', 9, 'or', 'Q17(a)(iv) "X or Y": the answer options.'),
    ('040', 9, 'any two', 'Q17(a)(v) "Name any two" blood groups: the groups are not printed; priced per group; one card.'),
    ('040', 9, 'the following', 'Q17(b)(ii) list of vertebra types: one answer each.'),
    ('040', 9, 'the following', 'Q17(b)(iv) matching: all three parts.'),
    ('040', 9, 'any one', 'Q17(b)(v) closed choose-one pool of the three parts named in (b)(iv): ROUTES, one card each.'),
    ('040', 9, 'either', 'Q17(b)(vi) closed choose-one pool (arthritis or osteoporosis): ROUTES, one card each.'),
    ('040', 10, 'the following', 'Q17(c)(i) matching: all three parts.'),
    ('040', 10, 'or', 'Q17(c)(ii)2 "(or characteristic)": rewording.'),
    ('040', 10, 'one of the following', 'Q17(c)(iii): one of two printed statements; one answer.'),
    ('040', 10, 'or', 'Q17(c)(iii) "(X or Y)": the answer options.'),
    ('040', 10, 'one of the following', 'Q17(c)(iv): one of two printed statements; one answer.'),
    ('040', 10, 'or', 'Q17(c)(iv) "(X or Y)": the answer options.'),
    ('040', 10, 'or', 'Q17(c)(vi) "(or windpipe)": rewording.'),
    ('040', 10, 'the following', 'Q17(d)(iii) "Which three": all three organs make one answer; one card.'),
    ('040', 10, 'or', 'Q17(d)(iv) statement A, "after vaccination or after an infection": description.'),
    ('040', 10, 'both', 'Q17(d)(v) "both the general and specific": description.'),
]

ROUTES = {
    'Q14(b)(v)': ['xylem', 'phloem'],
    'Q17(b)(v)': ['cartilage', 'synovial-fluid', 'ligament'],
    'Q17(b)(vi)': ['arthritis', 'osteoporosis'],
}

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2025-ol-q16-ciii-fig': 'A shipped duplicate: "Q16(c)(iii)-(iv)" carded the two parts '
                                'bio-2025-ol-q16-c-iii and bio-2025-ol-q16-c-iv already card '
                                'separately. Withdrawn with a progress alias to '
                                'bio-2025-ol-q16-c-iii, which carries its first part.',
}
WITHDRAW = {'bio-2025-ol-q16-ciii-fig': ('bio-2025-ol-q16-c-iii', RETAINED['bio-2025-ol-q16-ciii-fig'])}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def listed(page, anchor, ends, doc='040'):
    return [Q(page, f'{i}.', end, doc=doc, after=anchor, br=True) for i, end in enumerate(ends, 1)]


def lettered(page, anchor, letters_ends, doc='040'):
    """Printed lettered options ("A:" on its own line, its text on the next)."""
    return [Q(page, f'{x}:', end, doc=doc, after=anchor, br=True) for x, end in letters_ends]


def tick_col(page, clip, answer):
    return G('tick-col', page=page, clip=clip, headers=['True', 'False'], expect=answer, marks=3)


Q1 = _A(3, 'Carbohydrates, proteins, lipids and vitamins are all biomolecules.')
Q2_STEM = [_A(4, 'Choose each term from the following list', 'Column A.'),
           _A(4, 'Habitat'), _A(4, 'Conservation'), _A(4, 'Biosphere'), _A(4, 'Ecosystem'),
           _A(4, 'Pollution')]
Q3_STEM = _A(4, 'State whether each of the following statements', 'in each case.')
Q4 = _A(5, 'Cells are the basic unit of life.', 'The diagram shows a cell.')
Q5 = [_A(6, 'Plants respond to their environment using tropisms.'),
      _A(6, 'Geotropism'), _A(6, 'Phototropism'), _A(6, 'Hydrotropism'), _A(6, 'Chemotropism')]
Q6 = _A(7, 'The nervous and endocrine systems in humans allow us')
Q6C = [_A(7, 'The eye is one of the sense organs of the', 'human nervous system.'),
       _A(7, 'Using information provided on the', 'following functions:')]
Q7 = _A(8, 'The images below show and describe the stages', 'not in the correct order.')
Q8B = _A(9, 'In the course of your studies you carried out food tests.')
Q9B = _A(10, 'Answer the following questions based on an experiment', 'of an enzyme.')
Q10A = _A(11, 'Germination is the growth of the plant embryo')
Q10B = _A(11, 'A student drew the following diagram', 'factors that affect germination.')
Q11B = [_C(2, 'Read the following passage'), _C(2, 'The lesser horseshoe bat is so-named', 'cover.'),
        _C(2, 'Adapted from “The global importance')]
Q11C = _C(2, 'Study the following word diagrams, X and Y')
Q12B = _C(3, 'In pea plants, the allele for tallness', 'controlled by pairs of alleles.')
Q12C = _C(3, 'Study the table below showing diagrams', 'DNA, RNA and amino acids.')
Q13A = _C(4, 'Photosynthesis and respiration are metabolic reactions in cells.')
Q13B = _C(4, 'Study the diagram showing photosynthesis and answer', 'following questions.')
Q13C = _C(4, 'The diagram shows human skeletal muscle cells.')
Q13CII = _C(4, 'Aerobic respiration takes place in two main', 'stage 1 and stage 2.')
Q14A = _C(5, 'The diagram shows the two major systems of a', 'flowering plant.')
Q14B = _C(5, 'The diagrams show transverse sections of a root and a stem')
Q14C = _C(5, 'Answer the following questions in relation to reproduction in plants.')
Q14CI = _C(5, 'Plants use seed dispersal as part of reproduction.')
Q14CII = _C(5, 'Plants can also undergo vegetative propagation.')
Q15 = _C(6, 'The following questions relate to the human reproductive system.')
Q15B = _C(6, 'Answer the following questions in relation to the female reproductive system.')
Q15C = _C(6, 'The diagram shows the male reproductive system.')
Q16A = _C(7, 'Enzymes are important biological molecules.')
Q16B = _C(7, 'Answer the following questions in relation to genetics.')
Q16BII = _C(7, 'Genetic variation within members of the same species', 'reproduction and mutations.')
Q16BIV = _C(7, 'Darwin and Wallace came up with a famous theory', 'better able to survive.')
Q16C = _C(8, 'Answer the following questions in relation to Rhizopus and yeast.')
Q16D = _C(8, 'Answer the following questions in relation to microbiology.')
Q17A = _C(9, 'The diagram shows the human heart.')
Q17C = _C(10, 'The diagram below shows the human breathing system.')
Q17D = _C(10, 'The human body’s defence (immune) system has general', 'defend against pathogens.')

TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', [_A(3, 'Which one of the following biomolecules is the main source', 'the body?'),
                           _A(3, 'Tick (✓) the correct box.'),
                           _A(3, 'Carbohydrate', br=True, after='Which one of the following biomolecules'),
                           _A(3, 'Protein', br=True)],
      [pt(S('Carbohydrate'), 4)], 'bio-1-2', 'main-energy-source-carbohydrate',
      SQ(8, 'Which one of the following biomolecules'), 4, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Using the chemical symbols for hydrogen', 'general formula for carbohydrates.'),
      [G('tokens-x', page=8, clip=(95, 210, 260, 258), expect='C x ( H 2 O )y', marks=4,
         note='The scheme sets x, 2 and y as subscripts: its formula is shown after reveal.')],
      'bio-1-2', 'carbohydrate-general-formula', SQ(8, 'Using the chemical symbols'), 4, stem=[Q1],
      fig='q1b-scheme', qfig='q1b-question',
      decision='The paper prints the formula as boxes to fill, with x, 2 and y set small beside them; the '
               'scheme fills the boxes. The row reads the scheme\'s letters and numbers in print order, '
               'and both are shown as printed: the question with its frame, the filled formula after reveal.'),
    T('1c', 'Q1(c)', 'A', [_A(3, 'Which one of the following structures represents a triglyceride?'),
                           _A(3, 'Tick (✓) the correct box.', nth=2)],
      [G('lines', page=8, clip=(100, 298, 260, 368), expect='Fatty acid — Glycerol Fatty acid — Fatty acid',
         marks=4, note='The scheme reprints the triglyceride: its drawing is shown after reveal.')],
      'bio-1-2', 'triglyceride-structure', SQ(8, 'Which one of the following structures'), 4, stem=[Q1],
      fig='q1c-scheme', qfig='q1c-question',
      decision='The scheme answers with a reprint of the correct structure, not a tick: its labels '
               'are read from the drawing and the drawing is the solution figure; the question, with its '
               'table of two structures, is shown as the paper prints it.'),
    T('1d', 'Q1(d)', 'A', _A(3, 'Name a water-soluble vitamin.'),
      [pt(S('B or C or named water-soluble vitamin'), 4)], 'bio-1-2', 'water-soluble-vitamins',
      SQ(8, 'Name a water-soluble vitamin.'), 4, stem=[Q1]),
    T('1e', 'Q1(e)', 'A', _A(3, 'Name a fat-soluble vitamin.'),
      [pt(S('A or D or E or K or named fat-soluble vitamin'), 4)], 'bio-1-2', 'fat-soluble-vitamins',
      SQ(8, 'Name a fat-soluble vitamin.'), 4, stem=[Q1]),
] + [
    T(f'2{x}', f'Q2({x})', 'A', _A(4, start, end), [pt(S(answer, after=sq), 4)], 'bio-3-1', concept,
      SQ(9, sq), 4, stem=Q2_STEM, id='bio-2025-ol-q2-a-e' if x == 'a' else None,
      decision='Lettered parts are separate printed addresses; the completed example (Abiotic) and '
               'the sentence introducing it are left out of the stem.' + (
                   ' The old card bundled (a)-(e); it keeps its id for (a).' if x == 'a' else ''))
    for x, start, end, sq, answer, concept in [
        ('a', 'Parts of the Earth where life exists.', None, 'Parts of the Earth', 'Biosphere', 'biosphere'),
        ('b', 'Area where organisms interact with each other and their', 'environment.', 'Area where organisms',
         'Ecosystem', 'ecosystem'),
        ('c', 'Management of the environment.', None, 'Management of the environment', 'Conservation',
         'conservation'),
        ('d', 'Place where an organism lives.', None, 'Place where an organism lives', 'Habitat', 'habitat'),
        ('e', 'Harmful addition to the environment.', None, 'Harmful addition', 'Pollution', 'pollution')]
] + [
    T(f'3{x}', f'Q3({x})', 'A', _A(4, start), [tick_col(9, clip, answer)], topic, concept, SQ(9, start), 3,
      stem=[Q3_STEM], notes='Question 3 is marked on one ladder, 6(3) + 2.')
    for x, start, clip, answer, topic, concept in [
        ('a', 'Safety is an important principle of experimentation.', (60, 478, 560, 505), 'True', 'bio-u2',
         'safety-in-experiments'),
        ('b', 'Fauna refers to plants.', (60, 505, 560, 531), 'False', 'bio-3-1', 'fauna'),
        ('c', 'Osmosis is a special type of diffusion.', (60, 531, 560, 558), 'True', 'bio-2-6', 'osmosis'),
        ('d', 'Salt and sugar are used in food preservation.', (60, 558, 560, 585), 'True', 'bio-3-2',
         'food-preservation'),
        ('e', 'Endocrine glands have ducts.', (60, 585, 560, 611), 'False', 'bio-2-4', 'endocrine-glands'),
        ('f', 'The meninges are the protective covering around the heart.', (60, 611, 560, 637), 'False',
         'bio-2-4', 'meninges'),
        ('g', 'Lenticels are present on plant stems.', (60, 637, 560, 664), 'True', 'bio-2-6', 'lenticels')]
] + [
    T('4ai', 'Q4(a)(i)', 'A', [_A(5, 'Is this a plant cell or an animal cell?'), _A(5, 'Tick (✓) the correct box.'),
                               _A(5, 'Plant cell', br=True), _A(5, 'Animal cell', br=True)],
      [pt(S('Plant cell'), 3)], 'bio-1-3', 'plant-or-animal-cell', SQ(10, 'Is this a plant cell'), 3,
      stem=[Q4], fig='q4-cell', id='bio-2025-ol-q4-a-fig',
      decision='The old card bundled (a)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('4aii', 'Q4(a)(ii)', 'A', _A(5, 'Give two reasons for your answer in', 'part (i) above.'),
      [anyn(S('Chloroplast present / large vacuole present / cell wall present'), 2, 3)], 'bio-1-3',
      'plant-cell-features', SQ(10, 'Give two reasons for your answer.'), 6,
      stem=[Q4, M('(i)', 5), _A(5, 'Is this a plant cell or an animal cell?')], fig='q4-cell'),
    T('4b', 'Q4(b)', 'A', _A(5, 'The parts labelled A and B are cell components.', 'in the table below.'),
      [pt(S('B', after='Vacuole'), 3, label=S('Vacuole', after='Letter')),
       pt(S('A', after='Cell membrane'), 3, label=S('Cell membrane'))], 'bio-1-3', 'vacuole-and-membrane',
      SQ(10, 'Write the letter A or B beside the correct cell component'), 6, stem=[Q4], fig='q4-cell',
      id='bio-2025-ol-q4-b-fig',
      labels=[L('A', S('Cell membrane', page=10), True), L('B', S('Vacuole', page=10, after='Letter'), True)]),
    T('4c', 'Q4(c)', 'A', [_A(5, 'Cell components A and B have specific functions.'),
                           _A(5, 'Write the letter A or B beside the correct function', 'in the table below.')],
      [pt(S('A', after='and leaves the cell'), 3, label=S('Controls what enters', 'and leaves the cell')),
       pt(S('B', after='Storage'), 3, label=S('Storage'))], 'bio-1-3', 'membrane-and-vacuole-functions',
      SQ(10, 'Write the letter A or B beside the correct function'), 6, stem=[Q4], fig='q4-cell',
      id='bio-2025-ol-q4-c-fig'),
    T('5a', 'Q5(a)', 'A', _A(6, 'Using the correct term from the list above', 'below.'),
      [pt(S('Geotropism'), 3, label=S('Gravity')),
       pt(S('Hydrotropism'), 3, label=S('Water in', 'pot')),
       pt(S('Chemotropism'), 3, label=S('Minerals', 'in the soil')),
       pt(S('Phototropism'), 3, label=S('Light', after='in the soil'))],
      'bio-2-4', 'tropisms', SQ(11, 'Match each tropism with the diagrams below.'), 12, stem=Q5,
      fig='q5-tropisms', decision='One matching exercise: a row per diagram, four of the ladder\'s responses.'),
    T('5b', 'Q5(b)', 'A', _A(6, 'Why are tropisms important for plants?'),
      [pt(S('To allow for more growth'), 3)], 'bio-2-4', 'why-tropisms-matter',
      SQ(11, 'Why are tropisms important'), 3, stem=Q5[:1]),
    T('5c', 'Q5(c)', 'A', [_A(6, 'Auxin is a growth regulator in plants.'),
                           _A(6, 'Which one of the following tissues is the main way', 'the correct box.'),
                           _A(6, 'Dermal tissue', br=True), _A(6, 'Vascular tissue', br=True),
                           _A(6, 'Ground tissue', br=True)],
      [pt(S('Vascular tissue'), 3)], 'bio-2-4', 'auxin-transport', SQ(11, 'Which one of the following tissues'), 3),
    T('5d', 'Q5(d)', 'A', _A(6, 'Give one way in which plant growth regulators are used commercially.'),
      [pt(S('Correct commercial use given'), 3, kind='criterion')], 'bio-2-4', 'growth-regulators-in-use',
      SQ(11, 'Give one way in which plant growth regulators'), 3),
    T('6a', 'Q6(a)', 'A', [_A(7, 'Fill in the blanks in the box below', 'following list:'),
                           _A(7, 'impulses', br=True), _A(7, 'bloodstream'), _A(7, 'neurons'), _A(7, 'hormones'),
                           _A(7, 'The endocrine system carries messages', '.', br=True),
                           _A(7, 'The nervous system sends', '.', br=True)],
      [G('tokens', page=12, clip=clip, expect=word, marks=3, strip='_.') for clip, word in [
          ((118, 184, 232, 200), 'hormones'), ((373, 184, 497, 200), 'bloodstream'),
          ((248, 219, 374, 235), 'impulses'), ((118, 249, 238, 265), 'neurons')]],
      'bio-2-4', 'nervous-and-endocrine-messages', SQ(12, 'Fill in the blanks in the box below'), 12, stem=[Q6],
      decision='One passage with four blanks: four of the ladder\'s responses, in the order of the blanks.'),
    T('6b', 'Q6(b)', 'A', [_A(7, 'Using a word from the following list, complete the', 'sentence below.'),
                           _A(7, 'distal', br=True), _A(7, 'central'), _A(7, 'portal'),
                           _A(7, 'The human nervous system is divided into two main', 'nervous system.', br=True)],
      [pt(S('Central'), 3)], 'bio-2-4', 'central-nervous-system', SQ(12, 'Using a word from the following list'), 3,
      stem=[Q6]),
    T('6ci', 'Q6(c)(i)', 'A', _A(7, 'Controls the amount of light', 'entering the eye.'),
      [pt(S('Iris'), 3)], 'bio-2-4', 'iris', SQ(12, 'Controls the amount of light'), 3, stem=Q6C, fig='q6-eye',
      id='bio-2025-ol-q6-c-fig',
      decision='The old card bundled (c)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('6cii', 'Q6(c)(ii)', 'A', _A(7, 'Contains receptors that detect', 'light.'),
      [pt(S('Retina'), 3)], 'bio-2-4', 'retina', SQ(12, 'Contains receptors that detect light.'), 3, stem=Q6C,
      fig='q6-eye'),
    T('7a', 'Q7(a)', 'A', _A(8, 'Write the letters A, B, C, D in the correct order', 'during mitosis.'),
      [pt(S('C, B, D, A'), 6, units=[3, 3], note_sel=S('Correct order and position', 'Fully correct = 6'))],
      'bio-2-3', 'order-of-mitosis', SQ(13, 'Write the letters, A, B, C, D'), 6, stem=[Q7], fig='q7-mitosis'),
    T('7b', 'Q7(b)', 'A', _A(8, 'Name the organelle labelled X in image A.'),
      [pt(S('Nucleus'), 3)], 'bio-2-3', 'nucleus-in-mitosis', SQ(13, 'Name the organelle labelled X'), 3,
      stem=[Q7], fig='q7-mitosis', labels=[L('X', S('Nucleus', page=13), True)]),
    T('7c', 'Q7(c)', 'A', _A(8, 'Name the structures that hold and separate the chromosomes during mitosis.'),
      [pt(S('(Spindle) fibres'), 3)], 'bio-2-3', 'spindle-fibres', SQ(13, 'Name the structures that hold'), 3),
    T('7d', 'Q7(d)', 'A', [_A(8, 'Meiosis is the other type of cell division.'),
                           _A(8, 'Give one difference between meiosis and mitosis.')],
      [pt(S('Meiosis produces 4 daughter cells'), 3), pt(S('Mitosis produces 2 daughter cells'), 3)],
      'bio-2-3', 'meiosis-versus-mitosis', SQ(13, 'Give one difference between meiosis'), 6,
      decision='The scheme prints two matched pairs (cell numbers, or variation against identical '
               'cells) as alternatives: answer variants of one task, two of the ladder\'s responses.'),
    T('7e', 'Q7(e)', 'A', _A(8, 'What term is used to describe a group of disorders', 'division?'),
      [pt(S('Cancer'), 3)], 'bio-2-3', 'cancer', SQ(13, 'What term is used to describe a group'), 3),
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(9, 'Name an element always present in proteins'),
      [pt(S('Nitrogen'), 3)], 'bio-1-2', 'nitrogen-in-protein', SQ(14, 'Name an element always present'), 3),
    T('8aii', 'Q8(a)(ii)', 'B', [_A(9, 'Which of the following is the smallest unit', 'carbohydrate?'),
                                 _A(9, 'Tick (✓) the correct box.'), _A(9, 'Polysaccharide', br=True),
                                 _A(9, 'Monosaccharide', br=True)],
      [pt(S('Monosaccharide'), 3)], 'bio-1-2', 'monosaccharide', SQ(14, 'Which of the following is the smallest'), 3),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', [_A(9, 'Briefly describe how you tested', 'following biomolecules:'),
                                     _A(9, food, br=True)], [
        pt(S('Named test or named reagent', after=after), 3, kind='criterion'),
        pt(S('Initial colour (or observation)', 'procedural point', after=after), 3, kind='criterion')],
      'bio-1-2', f'test-for-{slug}', SQ(14, food), 6, stem=[Q8B])
    for r, food, after, slug in [('i', 'Starch', 'Starch', 'starch'),
                                 ('ii', 'A reducing sugar', 'A reducing sugar', 'reducing-sugar'),
                                 ('iii', 'Protein', 'Protein', 'protein'), ('iv', 'Lipid', 'Lipid', 'lipid')]
] + [
    T('9ai', 'Q9(a)(i)', 'B', [_A(10, 'Which biomolecule makes up enzymes?'), _A(10, 'Carbohydrate', br=True),
                               _A(10, 'Protein', br=True)],
      [pt(S('Protein'), 3)], 'bio-2-1', 'enzymes-are-protein', SQ(15, 'Which biomolecule makes up enzymes?'), 3),
    T('9aii', 'Q9(a)(ii)', 'B', _A(10, 'Name a factor, other than pH, that affects enzyme activity.'),
      [pt(S('Temperature or other correct'), 3)], 'bio-2-1', 'factors-affecting-enzymes',
      SQ(15, 'Name a factor, other than pH'), 3),
    T('9bi', 'Q9(b)(i)', 'B', _A(10, 'Name the enzyme you used.'),
      [pt(S('Correctly named enzyme'), 3, kind='criterion')], 'bio-2-1', 'enzyme-used',
      SQ(15, 'Name the enzyme you used.'), 3, stem=[Q9B]),
    T('9bii', 'Q9(b)(ii)', 'B', _A(10, 'Name the substrate of the enzyme you named above'),
      [pt(S('Correctly named and matching substrate'), 3, kind='criterion')], 'bio-2-1', 'substrate',
      SQ(15, 'Name the substrate of the enzyme'), 3,
      stem=[Q9B, M('(i)', 10), _A(10, 'Name the enzyme you used.')]),
    T('9biii', 'Q9(b)(iii)', 'B', _A(10, 'How did you vary the pH?'),
      [pt(S('Used (pH) buffers or described'), 3)], 'bio-2-1', 'varying-ph', SQ(15, 'How did you vary the pH?'), 3,
      stem=[Q9B]),
    T('9biv', 'Q9(b)(iv)', 'B', _A(10, 'Name a factor that you kept constant during the activity.'),
      [pt(S('Temperature or other correct factor'), 3)], 'bio-2-1', 'controlled-factor',
      SQ(15, 'Name a factor that you kept constant'), 3, stem=[Q9B], id='bio-2025-ol-q9-b-iv-v',
      decision='The old card bundled (b)(iv) and (v); it keeps its id for (iv), and (v) is added.'),
    T('9bv', 'Q9(b)(v)', 'B', _A(10, 'How did you keep the factor you named above'),
      [pt(S('Used a water bath or described'), 3, note_sel=S('Must match named factor from part (iv)'))],
      'bio-2-1', 'keeping-a-factor-constant', SQ(15, 'How did you keep the factor'), 3,
      stem=[Q9B, M('(iv)', 10), _A(10, 'Name a factor that you kept constant during the activity.')]),
    T('9bvi', 'Q9(b)(vi)', 'B', _A(10, 'Briefly describe a safety precaution'),
      [pt(S('Correct safety precaution given'), 3, kind='criterion')], 'bio-2-1', 'enzyme-safety',
      SQ(15, 'Briefly describe a safety precaution'), 3, stem=[Q9B]),
    T('9bvii', 'Q9(b)(vii)', 'B', _A(10, 'A graph similar to the one shown below', 'label axes A and B.'),
      [pt(S('Rate'), 3, label=S('A:')), pt(S('pH', after='Rate'), 3, label=S('B:'))], 'bio-2-1',
      'ph-graph-axes', SQ(15, 'Label axes A and B.'), 6, stem=[Q9B], fig='q9-graph'),
    T('10ai', 'Q10(a)(i)', 'B', [_A(11, 'Which term below describes the period of inactivity?'),
                                 _A(11, 'Tick (✓) the correct box.'), _A(11, 'Fertilisation', br=True),
                                 _A(11, 'Dormancy', br=True)],
      [pt(S('Dormancy'), 3)], 'bio-2-5', 'dormancy', SQ(16, 'Which term below describes'), 3, stem=[Q10A]),
    T('10aii', 'Q10(a)(ii)', 'B', [_A(11, 'Which location in the seed contains stored food?'),
                                   _A(11, 'Tick (✓) the correct box.', nth=2), _A(11, 'Testa', br=True),
                                   _A(11, 'Cotyledon', br=True)],
      [pt(S('Cotyledon'), 3)], 'bio-2-5', 'cotyledon', SQ(16, 'Which location in the seed'), 3, stem=[Q10A]),
    T('10bi', 'Q10(b)(i)', 'B', _A(11, 'Name a suitable seed that can be used in this activity.'),
      [pt(S('Correctly named suitable seed'), 3, kind='criterion')], 'bio-2-5', 'seed-for-germination',
      SQ(16, 'Name a suitable seed'), 3, stem=[Q10B], fig='q10-dishes'),
    T('10bii', 'Q10(b)(ii)', 'B', _A(11, 'Which dish (A, B, C or D) represents the control?', 'Justify your answer.'),
      [pt(S('A', after='Dish:'), 3, label=S('Dish:')), pt(S('Dish has all three factors'), 3, label=S('Justify:'))],
      'bio-2-5', 'control-dish', SQ(16, 'Which dish (A, B, C or D)'), 6, stem=[Q10B], fig='q10-dishes',
      id='bio-2025-ol-q10-b-ii-fig'),
    T('10biii', 'Q10(b)(iii)', 'B', _A(11, 'Dish C was placed in an anaerobic jar.', 'from the air?'),
      [pt(S('Oxygen'), 3)], 'bio-2-5', 'anaerobic-jar', SQ(16, 'What gas does this remove'), 3, stem=[Q10B],
      fig='q10-dishes', id='bio-2025-ol-q10-b-iii-v-fig',
      decision='The old card bundled (b)(iii)-(v); it keeps its id for (iii), and (iv), (v) are added.'),
    T('10biv', 'Q10(b)(iv)', 'B', _A(11, 'Which factor affecting germination is being investigated in dish B?'),
      [pt(S('Temperature'), 3)], 'bio-2-5', 'temperature-and-germination', SQ(16, 'Which factor affecting'), 3,
      stem=[Q10B], fig='q10-dishes'),
    T('10bv', 'Q10(b)(v)', 'B', _A(11, 'There is unlikely to be germination in dishes B and C.', 'Justify your answer.'),
      [pt(S('D', after='Identify one other dish', nth=2), 3, label=S('Dish:', after='Identify one other dish')),
       pt(S('Dish D is lacking water.'), 3, label=S('Justify:', after='Identify one other dish'))],
      'bio-2-5', 'water-and-germination', SQ(16, 'Identify one other dish'), 6, stem=[Q10B], fig='q10-dishes'),
    T('10bvi', 'Q10(b)(vi)', 'B', _A(11, 'How could you make the activity described above more reliable'),
      [pt(S('Use more seeds (in each dish) or repeat'), 3)], 'bio-2-5', 'reliable-germination-test',
      SQ(16, 'How could you make the activity'), 3, stem=[Q10B], fig='q10-dishes'),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'What is the main source of energy for the Earth’s ecosystems?'),
      [pt(S('Sun'), 3)], 'bio-3-1', 'energy-source', SQ(17, 'What is the main source of energy'), 3),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Why are food chains limited in length?'),
      [pt(S('There is a large loss of energy'), 3)], 'bio-3-1', 'food-chain-length',
      SQ(17, 'Why are food chains limited in length?'), 3),
    T('11aiii', 'Q11(a)(iii)', 'C', [_C(2, 'Which one of the following terms describes interconnected food chains?'),
                                     _C(2, 'Food net', br=True), _C(2, 'Food web', br=True),
                                     _C(2, 'Food diagram', br=True)],
      [pt(S('Food web'), 3)], 'bio-3-1', 'food-web', SQ(17, 'Which one of the following terms describes'), 3),
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Give one adaptation of the lesser horseshoe bat.'),
      [pt(S('Correct adaptation given'), 3, kind='criterion')], 'bio-3-1', 'bat-adaptation',
      SQ(17, 'Give one adaptation of the lesser horseshoe bat.'), 3, stem=Q11B),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Name a habitat of the lesser horseshoe bat.'),
      [pt(S('Correct habitat named'), 3, kind='criterion')], 'bio-3-1', 'bat-habitat',
      SQ(17, 'Name a habitat of the lesser horseshoe bat.'), 3, stem=Q11B),
    T('11biii', 'Q11(b)(iii)', 'C', _C(2, 'What is the niche of the lesser horseshoe bat?'),
      [pt(S('Keep the numbers of mosquitoes under control'), 3)], 'bio-3-1', 'bat-niche',
      SQ(17, 'What is the niche of the lesser horseshoe bat?'), 3, stem=Q11B),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'Give one way the lesser horseshoe bat population has been protected.'),
      [pt(S('Conservation legislation or increased woodland cover'), 3)], 'bio-3-1', 'bat-conservation',
      SQ(17, 'Give one way the lesser horseshoe bat population'), 3, stem=Q11B),
    T('11bv', 'Q11(b)(v)', 'C', _C(2, 'From the information provided in the passage, write out', 'secondary consumer.'),
      [pt(S('three organisms named in the correct order'), 3, kind='criterion', label=S('Food chain:')),
       pt(S('with arrows pointing the correct direction'), 3, kind='criterion'),
       pt(S('grass'), 3, label=S('Producer:')), pt(S('mosquito'), 3, label=S('Primary consumer:')),
       pt(S('Secondary consumer:'), 3)],
      'bio-3-1', 'bat-food-chain', SQ(17, 'From the information provided in the passage'), 15, stem=Q11B),
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Name the nutrient cycle represented in diagram X.'),
      [pt(S('Nitrogen'), 3)], 'bio-3-2', 'nitrogen-cycle', SQ(18, 'Name the nutrient cycle represented in diagram X.'), 3,
      stem=[Q11C], fig='q11-cycles'),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'In your answer book, match the terms, nitrification', 'diagram X.'),
      [pt(S('A: Nitrogen fixation'), 3), pt(S('B: Nutrition'), 3), pt(S('C: Nitrification'), 3)],
      'bio-3-2', 'nitrogen-cycle-processes', SQ(18, 'Match the terms, nitrification'), 9, stem=[Q11C],
      fig='q11-cycles'),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'Name the nutrient cycle represented in diagram Y.'),
      [pt(S('Carbon'), 3)], 'bio-3-2', 'carbon-cycle', SQ(18, 'Name the nutrient cycle represented in diagram Y.'), 3,
      stem=[Q11C], fig='q11-cycles'),
    T('11civ', 'Q11(c)(iv)', 'C', _C(2, 'In your answer book, match the terms, respiration', 'diagram Y.'),
      [pt(S('D: Photosynthesis'), 3), pt(S('Combustion'), 3, label=S('E:')), pt(S('Respiration'), 3, label=S('F:'))],
      'bio-3-2', 'carbon-cycle-processes', SQ(18, 'Match the terms, respiration'), 9, stem=[Q11C],
      fig='q11-cycles'),
    T('12ai', 'Q12(a)(i)', 'C', [_C(3, 'Match the terms genotype and phenotype', 'following descriptions:')]
      + [ _C(3, 'A:', 'an organism', br=True), _C(3, 'B:', 'an organism', br=True)],
      [pt(S('Phenotype'), 3, label=S('A:')), pt(S('Genotype'), 3, label=S('B:'))], 'bio-1-4',
      'genotype-and-phenotype', SQ(19, 'Match the terms genotype and phenotype'), 6),
    T('12aii', 'Q12(a)(ii)', 'C', [_C(3, 'Copy the following sentence into your answerbook', 'correct word.'),
                                   _C(3, 'Chromosomes are composed of DNA and', br=True)],
      [pt(S('Protein'), 3)], 'bio-1-4', 'chromosome-composition', SQ(19, 'Chromosomes are composed of DNA'), 3),
    T('12bi', 'Q12(b)(i)', 'C', [_C(3, 'Match the terms allele and recessive', 'following descriptions:')]
      + [_C(3, 'A:', 'homozygous condition.', br=True, after='Match the terms allele and recessive'),
         _C(3, 'B:', 'different forms exist.', br=True, after='Match the terms allele and recessive')],
      [pt(S('Recessive'), 3, label=S('A:')), pt(S('Allele'), 3, label=S('B:'))], 'bio-1-4',
      'allele-and-recessive', SQ(19, 'Match the terms allele and recessive'), 6, stem=[Q12B]),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'Give two possible genotypes for a tall plant.'),
      [pt(S('TT'), 3), pt(S('Tt'), 3)], 'bio-1-4', 'tall-genotypes', SQ(19, 'Give two possible genotypes'), 6,
      stem=[Q12B]),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'Give the only possible genotype for a short plant.'),
      [pt(S('tt'), 3)], 'bio-1-4', 'short-genotype', SQ(19, 'Give the only possible genotype'), 3, stem=[Q12B]),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'A gardener planted pea seeds that came from a cross between two short plants.',
                                     'Justify your answer.'),
      [pt(S('No'), 3), pt(S('Justify:', after='No'), 3)], 'bio-1-4', 'short-by-short-cross',
      SQ(19, 'Is it possible that any of these plants grew up to be tall?'), 6, stem=[Q12B]),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'A gardener planted pea seeds that came from a cross between two tall plants.',
                                   'Justify your answer.'),
      [pt(S('Yes'), 3), pt(S('Justify:', '(for shortness)', after='Yes'), 3)], 'bio-1-4', 'tall-by-tall-cross',
      SQ(19, 'Is it possible that any of these plants grew up to be short?'), 6, stem=[Q12B]),
    T('12ci', 'Q12(c)(i)', 'C', [_C(3, 'In your answerbook, match the diagrams, A, B and C', 'descriptions:')]
      + listed(3, 'In your answerbook, match the diagrams', ['transcribed', 'DNA replication', 'translated']),
      [pt(S('C', after='1. The DNA code is transcribed'), 3, label=S('1. The DNA code is transcribed')),
       pt(S('A', after='2. DNA replication'), 3, label=S('2. DNA replication')),
       pt(S('B', after='3. The code is translated'), 3, label=S('3. The code is translated'))],
      'bio-2-3', 'replication-transcription-translation', SQ(20, 'Match the diagrams, A, B and C'), 9,
      stem=[Q12C], fig='q12-processes', decision='One matching exercise: three rows.'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'What shape is DNA?'),
      [pt(S('(Double) helical or (double) helix'), 3)], 'bio-1-2', 'dna-shape', SQ(20, 'What shape is DNA?'), 3),
    T('12ciii1', 'Q12(c)(iii)1', 'C', _C(3, 'Adenine, thymine, cytosine, guanine and uracil', 'but not DNA?'),
      [pt(S('Uracil'), 3)], 'bio-1-2', 'uracil', SQ(20, 'Which one of the above bases'), 3,
      id='bio-2025-ol-q12-c-iii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('12ciii2', 'Q12(c)(iii)2', 'C', _C(3, 'DNA and RNA have another structural difference.', 'between DNA and RNA.'),
      [pt(S('DNA is double stranded, RNA is single stranded'), 3)], 'bio-1-2', 'dna-and-rna-strands',
      SQ(20, 'State one other structural difference'), 3,
      stem=[Q12C, M('1.', 3), _C(3, 'Adenine, thymine, cytosine, guanine and uracil', 'but not DNA?')],
      fig='q12-processes'),
    T('12civ1', 'Q12(c)(iv)1', 'C', _C(3, 'Give any one application (or use) of DNA profiling.'),
      [pt(S('Crime scene investigation', 'correct'), 3)], 'bio-3-3', 'dna-profiling',
      SQ(20, 'Give any one application (or use) of DNA profiling.'), 3,
      stem=[_C(3, 'DNA profiling and genetic engineering are important', 'by biologists.')],
      id='bio-2025-ol-q12-c-iv'),
    T('12civ2', 'Q12(c)(iv)2', 'C', _C(3, 'Give any one application (or use) of genetic engineering.'),
      [pt(S('Valid application given'), 3, kind='criterion')], 'bio-3-3', 'genetic-engineering',
      SQ(20, 'Give any one application (or use) of genetic engineering.'), 3,
      stem=[_C(3, 'DNA profiling and genetic engineering are important', 'by biologists.')]),
    T('13ai', 'Q13(a)(i)', 'C', [_C(4, 'Which one of the following sentences (A or B) describes metabolism?')]
      + [_C(4, 'A:', 'in a cell.', br=True), _C(4, 'B:', 'from the body.', br=True)],
      [pt(S('The sum of all chemical reactions in a cell or A.'), 3)], 'bio-2-2', 'metabolism',
      SQ(21, 'Which one of the following sentences (A or B)'), 3, stem=[Q13A]),
    T('13aii', 'Q13(a)(ii)', 'C', [_C(4, 'Match the terms photosynthesis and respiration to the following cell organelles:')]
      + listed(4, 'Match the terms photosynthesis and respiration', ['Mitochondrion', 'Chloroplast.']),
      [pt(S('Respiration'), 3, label=S('1. Mitochondrion')), pt(S('Photosynthesis'), 3, label=S('2. Chloroplast'))],
      'bio-2-2', 'organelles-of-metabolism', SQ(21, 'Match the terms photosynthesis and respiration'), 6,
      stem=[Q13A], decision='One matching exercise: two rows.'),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'What is the name of the green pigment in leaves', 'energy in sunlight?'),
      [pt(S('Chlorophyll'), 3)], 'bio-2-2', 'chlorophyll', SQ(21, 'What is the name of the green pigment'), 3,
      stem=[Q13B], fig='q13-photosynthesis'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Name gas X in the diagram.'),
      [pt(S('Carbon dioxide'), 3)], 'bio-2-2', 'carbon-dioxide', SQ(21, 'Name gas X in the diagram.'), 3,
      stem=[Q13B], fig='q13-photosynthesis', id='bio-2025-ol-q13-b-fig'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Give a possible source for the water required in', 'photosynthesis.'),
      [pt(S('Ground or soil or roots or rain'), 3)], 'bio-2-2', 'water-source',
      SQ(21, 'Give a possible source for the water'), 3, stem=[Q13B], fig='q13-photosynthesis'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'During photosynthesis, water is split into protons,', 'produced in photosynthesis.'),
      [pt(S('Used in respiration'), 3), pt(S('Released to the atmosphere'), 3)], 'bio-2-2', 'fate-of-oxygen',
      SQ(21, 'Describe two possible outcomes for the oxygen'), 6, stem=[Q13B], fig='q13-photosynthesis'),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'Is photosynthesis an anabolic or catabolic', 'Justify your answer.'),
      [pt(S('Anabolic'), 3), pt(S('Justify:', after='Anabolic'), 3)], 'bio-2-2', 'photosynthesis-anabolic',
      SQ(21, 'Is photosynthesis an anabolic process'), 6),
    T('13bvi', 'Q13(b)(vi)', 'C', _C(4, 'From your knowledge of photosynthesis, suggest', 'in a greenhouse.'),
      [pt(S('Valid way suggested'), 3, kind='criterion')], 'bio-2-2', 'greenhouse-growth',
      SQ(21, 'From your knowledge of photosynthesis'), 3),
    T('13bvii', 'Q13(b)(vii)', 'C', _C(4, 'Photosynthesis is critical for human life on Earth.', 'photosynthesis.'),
      [pt(S('No oxygen would be produced or other correct'), 3)], 'bio-2-2', 'why-photosynthesis-matters',
      SQ(21, 'Suggest one reason that life'), 3),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Why do you think a muscle cell needs to', 'large amounts of respiration?'),
      [pt(S('Because muscles require a lot of energy'), 3)], 'bio-2-2', 'muscle-respiration',
      SQ(22, 'Why do you think a muscle cell'), 3, stem=[Q13C], fig='q13-muscle'),
    T('13cii1', 'Q13(c)(ii)1', 'C', _C(4, 'Where in a cell does stage 1 occur?'),
      [pt(S('Cytosol'), 3)], 'bio-2-2', 'stage-1-site', SQ(22, '1. Where in a cell does stage 1 occur?'), 3,
      stem=[Q13CII]),
    T('13cii2', 'Q13(c)(ii)2', 'C', [_C(4, 'In your answerbook, state whether each of the following statements refers',
                                       'to stage 1 or stage 2.')]
      + lettered(4, 'to stage 1 or stage 2.', [('A', 'Requires oxygen.'), ('B', 'Does not require oxygen.'),
                                                ('C', 'small amount of energy.'), ('D', 'large amount of energy.')]),
      [pt(S('Stage 2', after='A. Requires oxygen.'), 3, label=S('A. Requires oxygen.')),
       pt(S('Stage 1', after='B. Does not require oxygen.'), 3, label=S('B. Does not require oxygen.')),
       pt(S('Stage 1', after='C. Releases a small amount of energy.'), 3, label=S('C. Releases a small amount of energy.')),
       pt(S('Stage 2', after='D. Releases a large amount of energy.'), 3, label=S('D. Releases a large amount of energy.'))],
      'bio-2-2', 'stages-of-aerobic-respiration', SQ(22, '2. State whether each of the following'), 12,
      stem=[Q13CII], decision='One classification of four lettered statements: four rows.'),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Anaerobic respiration can occur in human muscle cells.', 'cell.'),
      [pt(S('Intense exercise or other correct'), 3)], 'bio-2-2', 'anaerobic-respiration-in-muscle',
      SQ(22, 'Suggest a situation where anaerobic'), 3),
    T('13civ', 'Q13(c)(iv)', 'C', [_C(4, 'Anaerobic respiration can also occur in micro-organisms.',
                                      'form of anaerobic respiration?'),
                                   _C(4, 'Filtration', br=True), _C(4, 'Fermentation', br=True),
                                   _C(4, 'Diffusion', br=True)],
      [pt(S('Fermentation'), 3)], 'bio-2-2', 'fermentation', SQ(22, 'Which one of the following terms describes this'), 3),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'Give a function for the root system.'),
      [pt(S('Absorbs correctly named substance'), 3)], 'bio-2-6', 'root-system-function',
      SQ(23, 'Give a function for the root system.'), 3, stem=[Q14A], fig='q14-plant'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Name the system represented by the letter X.'),
      [pt(S('Shoot'), 3)], 'bio-2-6', 'shoot-system', SQ(23, 'Name the system represented'), 3, stem=[Q14A],
      fig='q14-plant'),
    T('14aiii', 'Q14(a)(iii)', 'C', _C(5, 'Give a function for the system you named', 'in (a) (ii) above.'),
      [pt(S('Photosynthesis or reproduction'), 3)], 'bio-2-6', 'shoot-system-function',
      SQ(23, 'Give a function for the system named'), 3,
      stem=[Q14A, M('(ii)', 5), _C(5, 'Name the system represented by the letter X.')], fig='q14-plant'),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Which diagram, 1 or 2, represents the transverse section of the root?',
                                   'Justify your answer.'),
      [G('tokens', page=23, clip=(108, 305, 125, 325), expect='2', marks=3),
       pt(S('Justify: There are root hairs present'), 3)], 'bio-2-6', 'root-transverse-section',
      SQ(23, 'Which diagram, 1 or 2'), 6, stem=[Q14B], fig='q14-sections', id='bio-2025-ol-q14-b-i-ii-fig',
      decision='The old card bundled (b)(i) and (ii); it keeps its id for (i), and (ii) is added.'),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Is this plant monocotyledonous or dicotyledonous?', 'Justify your answer.', nth=1),
      [pt(S('Dicotyledonous'), 3), pt(S('Justify: The vascular bundles'), 3)], 'bio-2-6', 'dicot-stem',
      SQ(23, 'Is this plant monocotyledonous'), 6, stem=[Q14B], fig='q14-sections'),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'The labels in the diagram represent three different', 'Ground, Dermal, Vascular.'),
      [pt(S('B', after='Ground'), 3, label=S('Ground', after='following terms')),
       pt(S('A', after='Dermal'), 3, label=S('Dermal')), pt(S('C', after='Vascular'), 3, label=S('Vascular'))],
      'bio-2-6', 'plant-tissue-types', SQ(23, 'Match the tissues labelled A, B and C'), 9, stem=[Q14B],
      fig='q14-sections', id='bio-2025-ol-q14-b-iii-fig',
      labels=[L('A', S('Dermal', page=23), True), L('B', S('Ground', page=23, after='following terms'), True),
              L('C', S('Vascular', page=23, after='Dermal'), True)],
      decision='One matching exercise: three rows.'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Which one of the tissues named above contains xylem and phloem?'),
      [pt(S('Vascular or C'), 3)], 'bio-2-6', 'vascular-tissue', SQ(23, 'Which one of the tissues named above'), 3,
      stem=[Q14B, M('(iii)', 5), _C(5, 'The labels in the diagram represent three different', 'Ground, Dermal, Vascular.')],
      fig='q14-sections'),
] + [
    T('14bv', 'Q14(b)(v)', 'C', _C(5, 'Give one function for either xylem or phloem.'),
      [pt(S(row), 3)], 'bio-2-6', f'{route}-function', SQ(23, 'Give one function for either xylem'), 3,
      route=route, id='bio-2025-ol-q14-b-v' if route == 'xylem' else None,
      decision='Closed choose-one pool (xylem or phloem): one card each.')
    for route, row in [('xylem', 'Xylem: transports water or minerals'), ('phloem', 'Phloem: transports food')]
] + [
    T('14ci1', 'Q14(c)(i)1', 'C', _C(5, 'Is seed formation part of asexual or sexual reproduction in plants?'),
      [pt(S('Sexual'), 3)], 'bio-2-5', 'seed-formation-sexual', SQ(24, '1. Is seed formation part'), 3,
      stem=[Q14C, Q14CI], id='bio-2025-ol-q14-c-i',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('14ci2', 'Q14(c)(i)2', 'C', _C(5, 'Why do you think seed dispersal is an important part of plant reproduction?'),
      [pt(S('Colonise new habitats or other correct'), 3)], 'bio-2-5', 'why-seeds-disperse',
      SQ(24, '2. Why do you think seed dispersal'), 3, stem=[Q14C, Q14CI]),
    T('14ci3', 'Q14(c)(i)3', 'C', _C(5, 'Plants use various methods for seed dispersal including', 'images, A, B and C.'),
      [pt(S('Water'), 3, label=S('A:', after='images, A, B and C.')), pt(S('Wind'), 3, label=S('B:', after='Water')),
       pt(S('Animal'), 3, label=S('C:', after='Wind'))], 'bio-2-5', 'seed-dispersal-methods',
      SQ(24, '3. Match each type of seed dispersal'), 9, stem=[Q14C, Q14CI], fig='q14-dispersal',
      id='bio-2025-ol-q14-c-i3-fig', decision='One matching exercise: three rows.'),
    T('14cii1', 'Q14(c)(ii)1', 'C', _C(5, 'Is vegetative propagation part of asexual or sexual', 'Justify your answer.'),
      [pt(S('Asexual'), 3), pt(S('It does not involve production of seeds'), 3, label=S('Justify:', after='Asexual'))],
      'bio-2-5', 'vegetative-propagation-asexual', SQ(24, '1. Is vegetative propagation part'), 6,
      stem=[Q14C, Q14CII], id='bio-2025-ol-q14-c-ii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('14cii2', 'Q14(c)(ii)2', 'C', _C(5, 'Give any one method of vegetative propagation in plants.'),
      [pt(S('Stem or root or leaf or bud'), 3)], 'bio-2-5', 'vegetative-propagation-method',
      SQ(24, '2. Give any one method of vegetative propagation'), 3, stem=[Q14C, Q14CII]),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'Name the male hormone responsible for male secondary sexual characteristics.'),
      [pt(S('Testosterone'), 3)], 'bio-2-5', 'testosterone', SQ(25, 'Name the male hormone'), 3, stem=[Q15]),
    T('15aii', 'Q15(a)(ii)', 'C', [_C(6, 'Two hormones in females that are involved', 'progesterone and oestrogen.'),
                                   _C(6, 'From the hormones named above, identify which hormone', 'for:')]
      + listed(6, 'From the hormones named above', ['endometrium.', 'pregnancy.']),
      [pt(S('Oestrogen'), 3, label=S('1. Building-up of the endometrium.')),
       pt(S('Progesterone'), 3, label=S('2. Maintaining the endometrium for pregnancy.'))],
      'bio-2-5', 'oestrogen-and-progesterone', SQ(25, '…identify which hormone'), 6, stem=[Q15],
      decision='One matching exercise: two rows.'),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'What happens in the womb (or uterus) during menstruation', '1 – 5)?'),
      [pt(S('The endometrium is released from the body'), 3)], 'bio-2-5', 'menstruation',
      SQ(25, 'What happens in the womb'), 3, stem=[Q15B]),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'Ovulation occurs on approximately day 14.', 'What happens during ovulation?'),
      [pt(S('Egg released from ovary'), 3)], 'bio-2-5', 'ovulation', SQ(25, 'What happens during ovulation?'), 3,
      stem=[Q15B]),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'The time around ovulation is described as the fertile period.',
                                       'fertilisation to occur?'),
      [pt(S('Fallopian tube'), 3)], 'bio-2-5', 'site-of-fertilisation', SQ(25, 'Where in the female reproductive system'), 3,
      stem=[Q15B]),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'What is meant by the term infertility?'),
      [pt(S('Inability to produce offspring'), 3)], 'bio-2-5', 'infertility', SQ(25, 'What is meant by the term infertility?'), 3,
      stem=[Q15B]),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'Give one method used to treat infertility.'),
      [pt(S('IVF or other correct'), 3)], 'bio-2-5', 'infertility-treatment', SQ(25, 'Give one method used to treat'), 3,
      stem=[Q15B]),
    T('15bvi', 'Q15(b)(vi)', 'C', _C(6, 'The diagram shows a developing foetus.', 'identify X and Y.'),
      [pt(S('Placenta'), 3, label=S('X:')), pt(S('Foetus'), 3, label=S('Y:'))], 'bio-2-5', 'placenta-and-foetus',
      SQ(25, 'Using the terms placenta and foetus'), 6, stem=[Q15B], fig='q15-foetus'),
    T('15bvii', 'Q15(b)(vii)', 'C', _C(6, 'Give one function of the placenta.'),
      [pt(S('Keeps bloods from mixing'), 3)], 'bio-2-5', 'placenta-function', SQ(25, 'Give one function of the placenta.'), 3,
      stem=[Q15B]),
    T('15bviii', 'Q15(b)(viii)', 'C', [_C(6, 'Lactation is the production of milk.', 'is involved in lactation?'),
                                       _C(6, 'Growth hormone', br=True), _C(6, 'Prolactin', br=True)],
      [pt(S('Prolactin', after='Growth hormone', nth=2), 3)], 'bio-2-5', 'prolactin',
      SQ(25, 'Which one of the following hormones'), 3, stem=[Q15B]),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'In your answerbook, match each of the parts', 'testis, prostate gland, sperm duct.'),
      [pt(S('C', after='1. Testis'), 3, label=S('Testis', after='following terms')),
       pt(S('B', after='2. Prostate gland'), 3, label=S('Prostate gland')),
       pt(S('A', after='3. Sperm duct'), 3, label=S('Sperm duct'))],
      'bio-2-5', 'male-reproductive-parts', SQ(26, 'Match each of the parts labelled A, B and C'), 9,
      stem=[Q15C], fig='q15-male', labels=[L('A', S('Sperm duct', page=26), True),
                                           L('B', S('Prostate gland', page=26), True),
                                           L('C', S('Testis', page=26, after='following terms'), True)],
      decision='One matching exercise: three rows.'),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Which part named above produces sperm?'),
      [pt(S('C or testis'), 3)], 'bio-2-5', 'testis', SQ(26, 'Which part named above produces sperm?'), 3,
      stem=[Q15C, M('(i)', 6), _C(6, 'In your answerbook, match each of the parts', 'testis, prostate gland, sperm duct.')],
      fig='q15-male'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Name any method of contraception.'),
      [pt(S('Correct method named'), 3, kind='criterion')], 'bio-2-5', 'contraception',
      SQ(26, 'Name any method of contraception.'), 3),
    T('15civ', 'Q15(c)(iv)', 'C', [_C(6, 'Sketch the basic structure of a sperm cell and', 'two parts:'),
                                   _C(6, 'head', br=True), _C(6, 'tail (or flagellum).', br=True)],
      [pt(S('Sketch showing head and tail'), 3, kind='criterion'),
       pt(S('Two correctly positioned and named labels'), 6, kind='criterion', units=[3, 3])],
      'bio-2-5', 'sperm-sketch', SQ(26, 'Sketch the basic structure of a sperm cell'), 9),
    # Q16: any two of (a)-(d), each 30.
    T('16ai', 'Q16(a)(i)', 'C', [_C(7, 'Which one of the following terms best describes the shape of enzymes?'),
                                 _C(7, 'Fibrous', br=True), _C(7, 'Folded (globular)', br=True)],
      [pt(S('Folded (globular)', after='Folded (globular)'), 3)], 'bio-2-1', 'enzyme-shape',
      SQ(27, 'Which one of the following terms best describes'), 3, stem=[Q16A]),
    T('16aii', 'Q16(a)(ii)', 'C', [_C(7, 'Copy the table below into your answerbook.'),
                                   _C(7, 'Using the words listed, complete the table.'),
                                   _C(7, 'List:', br=True), _C(7, 'Protease'), _C(7, 'Maltose'), _C(7, 'Starch'),
                                   _C(7, 'Lipase')],
      [pt(S('Starch', after='Product'), 3, label=S('Substrate'),
          note_sel=S('Amylase', after='Starch'), note_lead='Table row:'),
       pt(S('Maltose', after='Amylase'), 3, label=S('Product'),
          note_sel=S('Amylase', after='Starch'), note_lead='Table row:'),
       pt(S('Lipase', after='Lipids'), 3, label=S('Enzyme'),
          note_sel=S('Lipids', after='Maltose'), note_lead='Table row:'),
       pt(S('Protease', after='Protein'), 3, label=S('Enzyme'),
          note_sel=S('Protein', after='Triglycerides'), note_lead='Table row:')],
      'bio-2-1', 'substrates-enzymes-products', SQ(27, '…..complete the table.'), 12, stem=[Q16A],
      fig='q16-table', decision='One table with four blanks: four rows.'),
    T('16aiii1', 'Q16(a)(iii)1', 'C', _C(7, 'Describe briefly how enzymes or living cells can be immobilised.'),
      [pt(S('Sodium alginate or other correct immobilising agent'), 3),
       pt(S('Named piece of equipment or physical manipulation described'), 3, kind='criterion')],
      'bio-2-1', 'immobilisation-method', SQ(27, '1. Describe briefly how enzymes'), 6,
      stem=[Q16A, _C(7, 'Enzymes and living cells can be immobilised.')]),
    T('16aiii2', 'Q16(a)(iii)2', 'C', _C(7, 'Give two advantages of using immobilised enzymes.'),
      [anyn(S('Stable / re-usable / pure product / other correct'), 2, 3)], 'bio-2-1',
      'advantages-of-immobilisation', SQ(27, '2. Give two advantages'), 6, stem=[Q16A],
      id='bio-2025-ol-q16-a-iii-2'),
    T('16aiii3', 'Q16(a)(iii)3', 'C', _C(7, 'What name is given to containers in which bioprocessing occurs?'),
      [pt(S('Bioreactor'), 3)], 'bio-2-1', 'bioreactor', SQ(27, '3. What name is given to containers'), 3,
      stem=[Q16A], id='bio-2025-ol-q16-a-iii-3'),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'What is meant by non-coding DNA?'),
      [pt(S('DNA that does not contain the genetic sequence'), 3)], 'bio-1-4', 'non-coding-dna',
      SQ(28, 'What is meant by non-coding DNA?'), 3, stem=[Q16B]),
    T('16bii1', 'Q16(b)(ii)1', 'C', _C(7, 'What is a mutation?'),
      [pt(S('Change in the structure or amount of DNA'), 3)], 'bio-2-3', 'mutation',
      SQ(28, 'What is a mutation?'), 3, stem=[Q16B, Q16BII], id='bio-2025-ol-q16-b-ii-1'),
    T('16bii2', 'Q16(b)(ii)2', 'C', _C(7, 'Give any two causes of mutations.'),
      [anyn(S('UV light / cigarette smoke / other correct'), 2, 3)], 'bio-2-3', 'causes-of-mutation',
      SQ(28, '2. Give any two causes of mutations.'), 6, stem=[Q16B, Q16BII], id='bio-2025-ol-q16-b-ii-2'),
    T('16biii', 'Q16(b)(iii)', 'C', [_C(7, 'In your answerbook, match each of the following terms, heredity', 'description below:')]
      + lettered(7, 'description below:', [('A', 'fertile offspring.'), ('B', 'to the next.'), ('C', 'code in DNA.')]),
      [pt(S('Species'), 3, label=S('A:')), pt(S('Heredity'), 3, label=S('B:')), pt(S('Gene expression'), 3, label=S('C:'))],
      'bio-1-4', 'heredity-species-gene-expression', SQ(28, 'Match each of the following terms, heredity'), 9,
      stem=[Q16B], decision='One matching exercise: three rows.'),
    T('16biv1', 'Q16(b)(iv)1', 'C', _C(7, 'What is this theory called?'),
      [pt(S('(Theory of) evolution'), 3)], 'bio-1-5', 'theory-of-evolution', SQ(28, '1. What is this theory called?'), 3,
      stem=[Q16B, Q16BIV]),
    T('16biv2', 'Q16(b)(iv)2', 'C', _C(7, 'Name and briefly describe one piece of evidence'),
      [pt(S('Fossils or embryology or other correct'), 3),
       pt(S('(Fossils) have become more complex', 'other matching description'), 3)], 'bio-1-5',
      'evidence-for-evolution', SQ(28, '2. Name and briefly describe one piece'), 6, stem=[Q16B, Q16BIV],
      id='bio-2025-ol-q16-b-iv-2'),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'Rhizopus and yeast both belong to the same', 'Fungi, Monera, Protista.'),
      [pt(S('Fungi'), 3)], 'bio-3-2', 'kingdom-fungi', SQ(29, 'Identify this kingdom'), 3, stem=[Q16C]),
    T('16cii', 'Q16(c)(ii)', 'C', [_C(8, 'The diagram shows Rhizopus (a type of bread', 'mould).'),
                                   _C(8, 'In your answerbook, match each of the parts', 'sporangium, stolon.')],
      [pt(S('A: Sporangium'), 3), pt(S('Sporangiophore'), 3, label=S('B:')), pt(S('Rhizoid'), 3, label=S('C:')),
       pt(S('D: Stolon'), 3)], 'bio-3-2', 'parts-of-rhizopus',
      SQ(29, 'Match each of the parts labelled A, B, C and D'), 12, stem=[Q16C], fig='q16-rhizopus',
      id='bio-2025-ol-q16-ci-fig',
      labels=[L('A', S('Sporangium', page=29, after='stolon.'), True), L('B', S('Sporangiophore', page=29), True),
              L('C', S('Rhizoid', page=29, after='C:'), True), L('D', S('Stolon', page=29, after='Rhizoid'), True)],
      decision='One matching exercise: four rows. The old card bundled (c)(i) and (ii), and (i) also '
               'had a card of its own; it keeps its id for (ii).'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Which part named above contains spores?'),
      [pt(S('Sporangium or A'), 3)], 'bio-3-2', 'sporangium', SQ(29, 'Which part named above contains spores?'), 3,
      stem=[Q16C, M('(ii)', 8), _C(8, 'The diagram shows Rhizopus (a type of bread', 'mould).'),
            _C(8, 'In your answerbook, match each of the parts', 'sporangium, stolon.')],
      fig='q16-rhizopus'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'What is the function of the spores?'),
      [pt(S('Asexual reproduction'), 3)], 'bio-3-2', 'spore-function', SQ(29, 'What is the function of the spores?'), 3,
      stem=[Q16C]),
    T('16cv', 'Q16(c)(v)', 'C', [_C(8, 'Which one of the following types of nutrition does', 'Rhizopus use?'),
                                 _C(8, 'Saprophytic', br=True), _C(8, 'Autotrophic', br=True)],
      [pt(S('Saprophytic', after='Autotrophic'), 3)], 'bio-3-2', 'rhizopus-nutrition',
      SQ(29, 'Which one of the following types of nutrition'), 3, stem=[Q16C]),
    T('16cvi1', 'Q16(c)(vi)1', 'C', _C(8, 'Is yeast a unicellular or multicellular', 'organism?'),
      [pt(S('Unicellular'), 3)], 'bio-3-2', 'yeast-unicellular', SQ(29, '1. Is yeast a unicellular'), 3, stem=[Q16C],
      id='bio-2025-ol-q16-c-vi',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('16cvi2', 'Q16(c)(vi)2', 'C', _C(8, 'What term describes how yeasts reproduce?'),
      [pt(S('Budding'), 3)], 'bio-3-2', 'budding', SQ(29, '2. What term describes how yeast reproduce?'), 3,
      stem=[Q16C]),
    T('16di', 'Q16(d)(i)', 'C', [_C(8, 'Draw a diagram of a virus and label the following parts:'),
                                 _C(8, 'Protein coat', br=True), _C(8, 'Nucleic acid.', br=True)],
      [pt(S('Drawing', after='Nucleic acid.'), 3, kind='criterion'),
       pt(S('Labels (protein coat and DNA) correctly positioned'), 6, kind='criterion', units=[3, 3])],
      'bio-1-1', 'virus-diagram', SQ(30, 'Draw a diagram of a virus'), 9, stem=[Q16D]),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Why is it difficult to classify viruses as living organisms?'),
      [pt(S('Non-cellular or other correct'), 3)], 'bio-1-1', 'viruses-living',
      SQ(30, 'Why it is difficult to classify viruses'), 3, stem=[Q16D]),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Name any two harmful examples of viruses.'),
      [pt(S('Two correctly named'), 6, kind='criterion', units=[3, 3])], 'bio-1-1', 'harmful-viruses',
      SQ(30, 'Name any two harmful examples of viruses.'), 6, stem=[Q16D]),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Antibiotics are not given to a person suffering', 'Suggest a reason for this.'),
      [pt(S('Antibiotics have no effect on viruses'), 3)], 'bio-1-1', 'antibiotics-and-viruses',
      SQ(30, 'Antibiotics are not given'), 3, stem=[Q16D]),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Match each of the shapes spherical, rod and spiral to the diagrams X, Y and Z.'),
      [pt(S('X: Rod'), 3), pt(S('Y: Spherical'), 3), pt(S('Z: Spiral'), 3)], 'bio-3-2', 'bacterial-shapes',
      SQ(30, 'Match each of the shapes spherical'), 9,
      stem=[Q16D, _C(8, 'Bacteria can also be harmful.', 'based on their shape.')], fig='q16-bacteria',
      id='bio-2025-ol-q16-dv-fig', decision='One matching exercise: three rows.'),
    # Q17: any two of (a)-(d), each 30.
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'In your answerbook, match each of the parts', 'septum, vena cava, pulmonary artery.'),
      [pt(S('Vena cava'), 3, label=S('A:')), pt(S('Pulmonary artery'), 3, label=S('B:')),
       pt(S('Septum', after='C:'), 3, label=S('C:'))], 'bio-2-6', 'parts-of-the-heart',
      SQ(31, 'Match each of the parts labelled A, B and C'), 9, stem=[Q17A], fig='q17-heart',
      labels=[L('A', S('Vena cava', page=31), True), L('B', S('Pulmonary artery', page=31), True),
              L('C', S('Septum', page=31, after='C:'), True)],
      decision='One matching exercise: three rows.'),
    T('17aii', 'Q17(a)(ii)', 'C', [_C(9, 'The left atrium receives blood from the lungs', 'listed below:')]
      + listed(9, 'In your answerbook, match each chamber', ['Deoxygenated blood', 'Oxygenated blood.']),
      [pt(S('Right ventricle'), 3, label=S('1. Deoxygenated blood')),
       pt(S('Left atrium'), 3, label=S('2. Oxygenated blood'))], 'bio-2-6', 'chambers-and-blood',
      SQ(31, 'Match each chamber, the left atrium'), 6, stem=[Q17A], fig='q17-heart',
      decision='One matching exercise: two rows.'),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'The heart contains valves.', 'function of these valves?'),
      [pt(S('Prevent backflow of blood'), 3)], 'bio-2-6', 'heart-valves', SQ(31, 'What is the function of these valves?'), 3),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'The image shows a transverse section of a', 'Justify your answer.'),
      [pt(S('X', after='Justify your answer.'), 3), pt(S('Thicker wall or smaller lumen'), 3)], 'bio-2-6',
      'artery-or-vein', SQ(31, 'Which do you think is the artery'), 6, fig='q17-vessels'),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'There are four main blood groups in', 'Name any two.'),
      [anyn(S('A / B / AB / O'), 2, 3)], 'bio-2-6', 'blood-groups', SQ(31, 'There are four main blood groups'), 6),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'State two functions of the human skeleton.'),
      [anyn(S('Protection / movement / other correct'), 2, 3)], 'bio-2-4', 'skeleton-functions',
      SQ(32, 'State two functions of the human skeleton.'), 6),
    T('17bii1', 'Q17(b)(ii)1', 'C', _C(9, 'Which type of vertebra is found in the neck region?'),
      [pt(S('Cervical'), 3)], 'bio-2-4', 'cervical-vertebrae', SQ(32, '1. Which type of vertebra is found'), 3,
      stem=[_C(9, 'Vertebrae are a type of bone found', 'sacral, and coccyx.')], id='bio-2025-ol-q17-b-ii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17bii2', 'Q17(b)(ii)2', 'C', _C(9, 'Which type of vertebra forms joints with the ribs?'),
      [pt(S('Thoracic'), 3)], 'bio-2-4', 'thoracic-vertebrae', SQ(32, '2. Which type of vertebra form joints'), 3,
      stem=[_C(9, 'Vertebrae are a type of bone found', 'sacral, and coccyx.')]),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'Name one other bone of the axial skeleton.'),
      [pt(S('Breastbone (or sternum)'), 3)], 'bio-2-4', 'axial-skeleton', SQ(32, 'Name one other bone of the axial'), 3,
      stem=[_C(9, 'The vertebrae and ribs form part of the axial skeleton.')]),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'The diagram shows the structure of one type of joint.', 'synovial fluid.'),
      [pt(S('P: Cartilage'), 3), pt(S('Q: Synovial fluid'), 3), pt(S('R: Ligament'), 3)], 'bio-2-4',
      'synovial-joint-parts', SQ(32, 'Match each of the parts labelled P, Q and R'), 9, fig='q17-joint',
      id='bio-2025-ol-q17-biv-fig',
      labels=[L('P', S('Cartilage', page=32, after='synovial fluid.'), True),
              L('Q', S('Synovial fluid', page=32, after='P:'), True), L('R', S('Ligament', page=32, after='Q:'), True)],
      decision='One matching exercise: three rows.'),
] + [
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'Give a function of any one of the parts named', 'in (b) (iv) above.'),
      [pt(S('Correct matching function given'), 3, kind='criterion')], 'bio-2-4', f'function-of-{route}',
      SQ(32, 'Give a function of any one of the parts'), 3, route=route,
      stem=[M('(iv)', 9), _C(9, 'The diagram shows the structure of one type of joint.', 'synovial fluid.')],
      fig='q17-joint', decision='Closed choose-one pool of the three parts named in (b)(iv): one card each.')
    for route in ROUTES['Q17(b)(v)']
] + [
    T('17bvi', 'Q17(b)(vi)', 'C', _C(9, 'Arthritis and osteoporosis are two disorders of the', 'disorders named above.'),
      [pt(S('Correct possible cause given'), 3, kind='criterion')], 'bio-2-4', f'cause-of-{route}',
      SQ(32, 'Give one possible cause of either'), 3, route=route,
      decision='Closed choose-one pool (arthritis or osteoporosis): one card each.')
    for route in ROUTES['Q17(b)(vi)']
] + [
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'In your answer book, match each of the parts labelled A, B and C with the',
                                   'trachea, bronchus, intercostal muscle.'),
      [pt(S('A: Intercostal muscle'), 3), pt(S('B: Bronchus'), 3), pt(S('C: Trachea'), 3)], 'bio-2-6',
      'breathing-system-parts', SQ(33, 'Match each of the parts labelled A, B and C'), 9, stem=[Q17C],
      fig='q17-breathing',
      labels=[L('A', S('Intercostal muscle', page=33), True), L('B', S('Bronchus', page=33, after='A:'), True),
              L('C', S('Trachea', page=33, after='B:'), True)],
      decision='One matching exercise: three rows.'),
    T('17cii1', 'Q17(c)(ii)1', 'C', _C(10, 'What is the function of the', 'alveolus?'),
      [pt(S('Gas exchange'), 3)], 'bio-2-6', 'alveolus-function', SQ(33, 'What is the function of the alveolus?'), 3,
      stem=[Q17C], fig='q17-breathing', id='bio-2025-ol-q17-c-ii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17cii2', 'Q17(c)(ii)2', 'C', _C(10, 'Give one adaptation (or', 'function.'),
      [pt(S('Thin walled or moist or elastic'), 3)], 'bio-2-6', 'alveolus-adaptation',
      SQ(33, 'Give one adaptation (or characteristic)'), 3, stem=[Q17C], fig='q17-breathing'),
    T('17ciii', 'Q17(c)(iii)', 'C', [_C(10, 'Which one of the following', 'inhalation?')]
      + lettered(10, 'the diaphragm moves during', [('X', 'moves down.'), ('Y', 'moves up.')]),
      [pt(S('X: Contracts and moves down.'), 3, whole=True)], 'bio-2-6', 'diaphragm-in-inhalation',
      SQ(33, 'Which one of the following statements (X or Y) describes how the diaphragm'), 3),
    T('17civ', 'Q17(c)(iv)', 'C', [_C(10, 'Which one of the following', 'inhalation?', nth=2)]
      + lettered(10, 'the ribcage moves during', [('X', 'inwards.'), ('Y', 'upwards and outwards.')]),
      [pt(S('Y: Moves upwards and outwards.'), 3, whole=True)], 'bio-2-6', 'ribcage-in-inhalation',
      SQ(33, 'Which one of the following statements (X or Y) describes how the ribcage'), 3),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'Name a disorder of the breathing system and give a treatment for this disorder.'),
      [pt(S('Valid disorder of the breathing system named'), 3, kind='criterion'),
       pt(S('Valid and matching treatment given'), 3, kind='criterion')], 'bio-2-6', 'breathing-disorder',
      SQ(33, 'Name a disorder of the breathing system'), 6),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'The trachea (or windpipe) is surrounded by rings of cartilage.',
                                     'rings of cartilage?'),
      [pt(S('Keep the trachea open'), 3)], 'bio-2-6', 'tracheal-cartilage', SQ(33, 'What is the function of these rings'), 3),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'What is a pathogen?'),
      [pt(S('Disease-causing organism'), 3)], 'bio-2-4', 'pathogen', SQ(34, 'What is a pathogen?'), 3, stem=[Q17D]),
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'Describe two ways the general defence system prevents entry of pathogens.'),
      [anyn(S('Mucus (or tears or sweat) /', 'phagocytes / other correct'), 2, 3)], 'bio-2-4', 'general-defence',
      SQ(34, 'Describe two ways the general defence system'), 6, stem=[Q17D]),
    T('17diii', 'Q17(d)(iii)', 'C', [_C(10, 'Which three of the following organs are specific parts of the immune system?'),
                                     _C(10, 'Spleen', br=True), _C(10, 'Heart', br=True), _C(10, 'Thymus', br=True),
                                     _C(10, 'Lung', br=True), _C(10, 'Lymph node', br=True)],
      [pt(S('Spleen', after='Lymph node'), 3), pt(S('Thymus', after='Lymph node'), 3),
       pt(S('Lymph node', after='Thymus', nth=1), 3)], 'bio-2-4', 'organs-of-the-immune-system',
      SQ(34, 'Which three of the following organs'), 9, stem=[Q17D]),
    T('17div', 'Q17(d)(iv)', 'C', [_C(10, 'Match the terms active and passive to the sentences below:')]
      + lettered(10, 'Match the terms active and passive', [('A', 'after an infection.'), ('B', 'organism.')]),
      [pt(S('Active'), 3, label=S('A:')), pt(S('Passive'), 3, label=S('B:'))], 'bio-2-4', 'active-and-passive-immunity',
      SQ(34, 'Match the terms active and passive'), 6,
      stem=[Q17D, _C(10, 'The presence of antibodies provides induced immunity.', 'active and passive.')],
      decision='One matching exercise: two rows.'),
    T('17dv1', 'Q17(d)(v)1', 'C', _C(10, 'What is the name given to this other circulatory fluid?'),
      [pt(S('Lymph'), 3)], 'bio-2-6', 'lymph', SQ(34, '1. What is the name given to this other'), 3,
      stem=[_C(10, 'White blood cells are involved in both the general', 'circulatory fluid of the body.')],
      id='bio-2025-ol-q17-d-v',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17dv2', 'Q17(d)(v)2', 'C', _C(10, 'A certain type of circulatory vessel transports the fluid', 'similar to a vein.'),
      [pt(S('Thin walls or large lumen or valves present'), 3)], 'bio-2-6', 'lymph-vessels',
      SQ(34, '2. Give one way in which this vessel'), 3,
      stem=[_C(10, 'White blood cells are involved in both the general', 'circulatory fluid of the body.'),
            M('1.', 10), _C(10, 'What is the name given to this other circulatory fluid?')]),
]

ANSWER_VARIANTS = {
    '7d': [
        ('cell-number', 'Cells produced',
         [pt(S('Meiosis produces 4 daughter cells'), 3), pt(S('Mitosis produces 2 daughter cells'), 3)]),
        ('variation', 'Variation',
         [pt(S('Meiosis produces variation'), 3), pt(S('Mitosis produces genetically identical cells'), 3)]),
    ],
}

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q1b-question': ('038', 3, (80, 232, 545, 316), SEC, [],
                     'The printed question: (b) Using the chemical symbols for hydrogen (H), carbon (C) and '
                     'oxygen (O), complete the general formula for carbohydrates. Below it, the answer frame: an '
                     'empty box with a small x after it, then an opening bracket, an empty box, a small 2, another '
                     'empty box, and a closing bracket with a small y after it.', False),
    'q1b-scheme': ('scheme', 8, (88, 212, 250, 257), SEC, [],
                   "The marking scheme's filled frame: C in the first box with a subscript x, then a bracket "
                   'holding H in a box, a subscript 2 and O in a box, closed with a subscript y.', True),
    'q1c-question': ('038', 3, (80, 327, 440, 582), SEC, [],
                     'The printed question: (c) Which one of the following structures represents a '
                     'triglyceride? Tick the correct box. Below it, a table headed Structure and Tick, with two '
                     'rows and an empty Tick column. Row one: an upright bar labelled Glycerol joined to a circle '
                     'labelled P and to two bars labelled Fatty acid, with the note P = phosphate. Row two: an '
                     'upright bar labelled Glycerol joined to three bars labelled Fatty acid.', False),
    'q1c-scheme': ('scheme', 8, (98, 292, 218, 366), SEC, [],
                   "The marking scheme's structure: an upright bar labelled Glycerol joined to three bars, each "
                   'labelled Fatty acid.', True),
    'q4-cell': ('038', 5, (358, 55, 540, 292), 'Created on biorender.com', ['A', 'B'],
                'Diagram of a six-sided cell with a thick, dark outer layer. A line labelled A points to the thin '
                'boundary just inside that layer. B labels a large, pale, rounded sac filling the upper part of the '
                'cell. Small oval bodies, some striped inside, small dots and a rounded body near the bottom fill '
                'the rest of the cell.', False),
    'q5-tropisms': ('038', 6, (112, 132, 540, 442), 'shutterstock.com', [],
                    'Four diagrams of seedlings, two above two, with empty answer boxes under each row. Top left: '
                    'a pot tipped on its side, its shoot curving up and its roots growing down, beside a downward '
                    'arrow labelled Gravity. Top right: a seedling in soil, its roots growing towards a small pot '
                    'labelled Water in a porous pot. Bottom left: a seedling in a tray, its roots growing towards '
                    'dots labelled Minerals in the soil. Bottom right: a seedling inside a clear cylinder, bending '
                    'towards a beam labelled Light.', False),
    'q6-eye': ('038', 7, (318, 480, 540, 652), 'shutterstock.com', [],
               'Diagram of a section through the human eye with six labels: Retina, on the inner lining at the '
               'back; Iris, on the ring in front of the lens; Lens; Cornea, on the clear front surface; Vitreous '
               'humour, in the jelly filling the eye; and Optic nerve, leaving the back of the eye.', False),
    'q7-mitosis': ('038', 8, (90, 92, 522, 262), 'Adapted from sciencephoto.com', ['A', 'B', 'C', 'D', 'X'],
                   'Four micrographs of a dividing cell, labelled A to D, each with a caption. A: The cell is '
                   'beginning to divide in two; it holds two dark rounded bodies, and an arrow labelled X points to '
                   'the lower one. B: Chromosomes line up on the equator of the cell. C: Chromosomes become visible '
                   'in the cell. D: Chromosomes are being pulled to the poles of the cell.', False),
    'q9-graph': ('038', 10, (130, 556, 480, 706), SEC, ['A', 'B'],
                 'A graph whose vertical axis is labelled by an empty box A and whose horizontal axis, numbered 2, '
                 '4, 6, 8, 10 and 12, is labelled by an empty box B. A narrow peak rises from the axis at about 6, '
                 'tops out at about 7 and falls back to the axis by about 8.', False),
    'q10-dishes': ('038', 11, (115, 218, 536, 312), SEC, ['A', 'B', 'C', 'D'],
                   'Four Petri dishes side by side, each holding one seed. Dish A: stored at room temperature, on '
                   'wet cotton wool. Dish B: stored in the refrigerator, on wet cotton wool. Dish C: stored in an '
                   'anaerobic jar, on wet cotton wool. Dish D: stored at room temperature, on dry cotton wool.',
                   False),
    'q11-cycles': ('040', 2, (112, 488, 538, 645), SEC, ['A', 'B', 'C', 'D', 'E', 'F'],
                   'Two word diagrams. Diagram X: arrow A runs down from Nitrogen gas in the atmosphere to Nitrates '
                   'in the soil, and another arrow runs back up; Nitrates in the soil lead to Plant protein, arrow B '
                   'runs from Plant protein to Animal protein, both proteins lead to Ammonia, and arrow C runs from '
                   'Ammonia up to Nitrates in the soil. Diagram Y: arrow D runs down from Carbon dioxide gas in the '
                   'atmosphere to Plant carbohydrate, and an arrow F runs back up; Plant carbohydrate leads to Animal '
                   'carbohydrate, from which another arrow F runs to the atmosphere; arrow E runs from Fossil fuels '
                   'to the atmosphere; both carbohydrates lead to Dead organic matter, which leads round to Fossil '
                   'fuels.', False),
    'q12-processes': ('040', 3, (84, 376, 540, 538), 'shutterstock.com; alamy.com', ['A', 'B', 'C'],
                      'A table of three diagrams. A: a twisted ladder labelled DNA (two identical strands). B: a '
                      'large rounded body labelled Ribosome sitting on a strand labelled Messenger RNA, with a '
                      'chain of beads labelled Protein growing from it. C: a rounded body labelled Enzyme on a '
                      'twisted ladder labelled DNA code, with a single strand labelled Messenger RNA (single '
                      'stranded) peeling away from it.', False),
    'q13-photosynthesis': ('040', 4, (395, 180, 540, 382), 'dreamstime.com', ['X'],
                           'Diagram of a leaf under the sun. Arrows labelled Sunlight point down at the leaf; an '
                           'arrow from a box labelled X curves into the leaf, and an arrow labelled Water H2O enters '
                           'it from below; arrows leave the leaf to Oxygen O2 and to Glucose C6H12O6.', False),
    'q13-muscle': ('040', 4, (368, 460, 540, 524), 'dreamstime.com', [],
                   'Drawing of four long, cylindrical, cross-striped cells lying side by side, with small oval '
                   'bodies along them.', False),
    'q14-plant': ('040', 5, (395, 52, 540, 166), 'Created on biorender.com', ['X'],
                  'Drawing of a flowering plant. A bracket labelled X spans everything above the ground; a bracket '
                  'labelled Root system spans the roots below.', False),
    'q14-sections': ('040', 5, (160, 208, 446, 322), 'shutterstock.com; dreamstime.com', ['A', 'B', 'C'],
                     'Two circular transverse sections, numbered 1 and 2. Section 1 has a ring of separate dark '
                     'bundles near its edge; section 2 has fine hairs on its outer edge and a dark central core. '
                     'Arrows labelled A point to the outer layer of each section, arrows labelled B to the tissue '
                     'filling each, and arrows labelled C to a dark bundle of section 1 and to the central core of '
                     'section 2.', False),
    'q14-dispersal': ('040', 5, (168, 600, 520, 678),
                      'seedparade.co.uk; istockphoto.com; ©Jacqui Geux – predatorfreenz.org', ['A', 'B', 'C'],
                      'Three photographs. A: a large seed lying half in water at the edge of a shore. B: a '
                      'dandelion clock with its seeds drifting away. C: a small bird perched on a branch.', False),
    'q15-foetus': ('040', 6, (410, 362, 540, 519), 'shutterstock.com', ['X', 'Y'],
                   'Diagram of a developing baby curled inside the womb. An arrow labelled X points to the thick '
                   'disc of tissue on the womb wall; an arrow labelled Y points to the curled-up body.', False),
    'q15-male': ('040', 6, (395, 558, 540, 720), 'shutterstock.com', ['A', 'B', 'C'],
                 'Front-view diagram of the male reproductive system. An arrow labelled A points to a tube that '
                 'loops up and over from each side; B labels the gland below the bladder that the tubes pass '
                 'through; C labels one of the two oval organs hanging at the bottom.', False),
    'q16-table': ('040', 7, (140, 184, 540, 292), SEC, [],
                  'A table with columns Substrate, Enzyme and Product. Row 1: blank, Amylase, blank. Row 2: Lipids, '
                  'blank, Triglycerides. Row 3: Protein, blank, Amino acid.', False),
    'q16-rhizopus': ('040', 8, (405, 72, 540, 278), 'shutterstock.com', ['A', 'B', 'C', 'D'],
                     'Diagram of the bread mould Rhizopus: upright stalks, each topped by a round head full of '
                     'dots, rise from a horizontal thread, with branched root-like threads below. Arrow A points to '
                     'a round head; arrow B to an upright stalk; arrow C to the branched threads at the bottom; '
                     'arrow D to the horizontal thread.', False),
    'q16-bacteria': ('040', 8, (175, 512, 455, 626), 'Created in biorender.com', ['X', 'Y', 'Z'],
                     'Three drawings of bacteria labelled X, Y and Z: X is a long capsule shape, Y is a ball, and '
                     'Z is a wavy corkscrew.', False),
    'q17-heart': ('040', 9, (380, 80, 540, 272), SEC, ['A', 'B', 'C'],
                  'Diagram of a section through the heart, two of its chambers labelled Left atrium and Right '
                  'ventricle. Arrow A points to a large vessel entering the chamber at the upper left of the '
                  'diagram; arrow B points to a vessel leaving the top of the heart; C labels the thick wall '
                  'dividing the two sides.', False),
    'q17-vessels': ('040', 9, (365, 288, 540, 386), 'University of Birmingham, UK', ['X', 'Y'],
                    'Micrograph of a transverse section through two blood vessels: X is small and round with a '
                    'thick wall; Y is larger and flattened with a thin wall.', False),
    'q17-joint': ('040', 9, (410, 515, 540, 716),
                  'Adapted from "The Development of Synovial Joints", I.M. Khan et al., 2007, Current Topics in '
                  'Development Biology.', ['P', 'Q', 'R'],
                  'Diagram of a joint between the rounded ends of two long bones, enclosed in a capsule. Arrow P '
                  'points to the dark layer capping the end of the upper bone; arrow Q points into the space '
                  'between the two bone ends; arrow R points to the band around the outside of the joint.', False),
    'q17-breathing': ('040', 10, (320, 98, 540, 350), SEC, ['A', 'B', 'C'],
                      'Diagram of the human breathing system: a ringed tube runs down from the throat and splits '
                      'into the two lungs, which sit inside the ribs above a curved sheet labelled Diaphragm. An '
                      'inset, labelled Capillary and Alveolus, enlarges an air sac at the end of an airway. Arrow C '
                      'points to the ringed tube, arrow B to one of the two tubes it splits into, and arrow A to the '
                      'tissue between two ribs; a label Rib points to a rib.', False),
}
