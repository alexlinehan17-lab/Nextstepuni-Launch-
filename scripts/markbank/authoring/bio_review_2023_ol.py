"""Biology 2023 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 40 pages: p1 cover
    (with the note that the 2023 papers were adjusted for disruption to
    learning), p2 instructions, p3-p8 Section A Questions 1-7, p9-p11
    Section B Questions 8-10, p12 Section C answerbook instructions,
    p13-p14 graph paper, p15-p39 ruled answer pages, p40 back cover. No
    acknowledgements page.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "Do not hand this question paper up", p12 back cover.
  * LC025GLP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7 Irish-medium
    bonus, p8-p32 Questions 1-17, p33-p35 "BLANK PAGE", p36 back cover.

The sitting was already carded (100 authored cards, 99 shipped). As for
2024 and 2025, every task is re-derived from the PDFs at the scheme's own
mark boundaries and the existing cards are corrected in place: every shipped
id is kept, mapped (`id=`) to the task it was carding, verified or corrected
with its old fields recorded; tasks the old cards bundled or missed are
added. bio-2023-ol-q16b-ii-v-fig, a figure twin of bio-2023-ol-q16b-ii-v that
never shipped, is withdrawn.

Every part of this scheme is priced on an ordered split, read from its
"Number of correct responses" table: Q1 and Q3 "2(7) + 3(2)", Q2 and Q4-Q7
"8 + 7 + 5(1)"; Section B (a) "5 + 1" and (b) "2(9) + 6(1)"; Section C (a)
"5 + 2(2)", (b) "3(5) + 6(2)", (c) "2(6) + 6(2)", and each part of Q16 and
Q17 "2(7) + 8(2)". What a response earns depends on how many came before
it, so every card carries an orderedSplit tariff with no per-row marks, its
total its responses at the first rate, as the cards this review corrects
already did.

One printed choice is open here: Q16(b)(vii) a disorder of the eye or the
ear. The scheme marks both on the same rows (a named disorder and its
matching corrective measure), under the same syllabus topic, so it is one
card ("choice is not a route").
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2023, 'ol'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = '985abf905'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2023-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': '94e4584df499b78bf8034587f98e4fd6175d98e327eccc775b9b94d907ae79ed',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2023-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': 'b7b1e3356bc87a0968d42babeb22788672b5e69892eaa4f3203b5a2d1aae0a75',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2023-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '992f9b1ea2a29628f7bf8b547ab7a5f1a8b234a7823d5ac5c9ecb891e357e8ff',
               'pages': 36},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 12)},
            12: 'answerbook-instructions', 13: 'graph-paper', 14: 'graph-paper',
            **{p: 'answer-pages' for p in range(15, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 33)}, 33: 'blank', 34: 'blank', 35: 'blank',
               36: 'back-cover'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 8)}, **{n: 30 for n in range(8, 11)},
    **{n: 60 for n in range(11, 16)}, 16: 120, 17: 120,
}
# Every part is laddered: the ladders, not the cards, make the printed totals.
PART_TOTALS = {}


def _ladder(notation):
    steps = []
    for term in notation.split(' + '):
        n, _, m = term.partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation}


LADDERS = {
    1: _ladder('2(7) + 3(2)'), 3: _ladder('2(7) + 3(2)'),
    **{q: _ladder('8 + 7 + 5(1)') for q in (2, 4, 5, 6, 7)},
    **{(n, 'a'): _ladder('5 + 1') for n in (8, 9, 10)},
    **{(n, 'b'): _ladder('2(9) + 6(1)') for n in (8, 9, 10)},
    **{(n, 'a'): _ladder('5 + 2(2)') for n in range(11, 16)},
    **{(n, 'b'): _ladder('3(5) + 6(2)') for n in range(11, 16)},
    **{(n, 'c'): _ladder('2(6) + 6(2)') for n in range(11, 16)},
    **{(n, x): _ladder('2(7) + 8(2)') for n in (16, 17) for x in 'abcd'},
}

# The "Number of correct responses" table under each part: how many
# responses it counts, each carded at the ladder's first rate.
CHECKSUMS = {
    1: {7: 5}, 3: {7: 5}, **{q: {8: 7} for q in (2, 4, 5, 6, 7)},
    **{(n, 'a'): {5: 2} for n in (8, 9, 10)}, **{(n, 'b'): {9: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {5: 3} for n in range(11, 16)}, **{(n, 'b'): {5: 9} for n in range(11, 16)},
    **{(n, 'c'): {6: 8} for n in range(11, 16)},
    **{(n, x): {7: 10} for n in (16, 17) for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 12), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: every part asked.'),
    ('038', 4, 'the following', 'Q2 lead-in: every statement asked.'),
    ('038', 4, 'or', 'Q2 "true or false": the answer options.'),
    ('038', 4, 'choose', 'Q3 "Choose each term": a matching list, every term placed; one card per lettered description.'),
    ('038', 4, 'the following', 'Q3 term list.'),
    ('038', 5, 'the following', 'Q4 "The following word equation": a figure reference.'),
    ('038', 7, 'the following', 'Q6 lead-in: every part asked.'),
    ('038', 7, 'any two', 'Q6(b) "any two nitrogenous bases": bounded menu; one card.'),
    ('038', 8, 'any one', 'Q7(e) "any one disorder": open single answer; one card.'),
    ('038', 9, 'any two', 'Section B rubric repeated.'),
    ('038', 9, 'both', 'Q8(b)(iii) "Label both axes": both required; one card.'),
    ('038', 11, 'the following', 'Q10(b) "The following data table": a figure reference.'),
    ('040', 2, 'any four', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q11(b) lead-in: every part asked.'),
    ('040', 2, 'the following', 'Q11(b)(i): both pyramids matched; one card.'),
    ('040', 2, 'any two', 'Q11(c)(ii) "any two essential nutrients": bounded menu; one card.'),
    ('040', 2, 'any two', 'Q11(c)(iii) "any two soil factors": bounded menu; one card.'),
    ('040', 3, 'the following', 'Q12(b)(iii): one of two printed terms; one answer.'),
    ('040', 4, 'or', 'Q13(b)(iv) "the atmosphere or the cells of the leaf": description.'),
    ('040', 5, 'the following', 'Q14(b)(vi): each location asked, one card per item.'),
    ('040', 5, 'the following', 'Q14(c) lead-in: every part asked.'),
    ('040', 5, 'any one', 'Q14(c)(i) "any one function": open single answer; one card.'),
    ('040', 5, 'any two', 'Q14(c)(iii) "any two biological benefits": bounded menu; one card.'),
    ('040', 6, 'the following', 'Q15(b) lead-in: every part asked.'),
    ('040', 6, 'the following', 'Q15(b)(iv): each role asked, one card per item.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q16(a)(ii) matching: all three parts; one card.'),
    ('040', 7, 'the following', 'Q16(a)(v): each location asked, one card per item.'),
    ('040', 7, 'the following', 'Q16(b)(i) matching: all three parts; one card.'),
    ('040', 7, 'or', 'Q16(b)(vii) "the eye or the ear": the scheme marks both on the same rows, one topic; '
                     'one card.'),
    ('040', 8, 'the following', 'Q16(c)(i) matching: all three tissues; one card.'),
    ('040', 8, 'any two', 'Q16(c)(v) "any two ways": the scheme prints two answers; one card.'),
    ('040', 8, 'the following', 'Q16(d)(i) matching: all three parts; one card.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'the following', 'Q17(a) lead-in: every part asked.'),
    ('040', 9, 'the following', 'Q17(a)(iv) matching: all three parts; one card.'),
    ('040', 9, 'the following', 'Q17(b) lead-in: every part asked.'),
    ('040', 9, 'or', 'Q17(b)(ii) table entry "fight or flight": printed example.'),
    ('040', 10, 'or', 'Q17(c)(iv) "a parasite or a saprophyte": the answer options.'),
    ('040', 10, 'both', 'Q17(c)(v) "both sexual and asexual reproduction": description.'),
    ('040', 10, 'either', 'Q17(d)(iv) "either autotrophic or heterotrophic": both terms explained; one card.'),
    ('040', 10, 'or', 'Q17(d)(iv), same terms.'),
]

ROUTES = {}

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2023-ol-q16b-ii-v-fig': 'Never shipped: a figure twin of bio-2023-ol-q16b-ii-v, which carries Q16(b)(ii) '
                                 'with its figure.',
}
WITHDRAW = {'bio-2023-ol-q16b-ii-v-fig': ('bio-2023-ol-q16b-ii-v', RETAINED['bio-2023-ol-q16b-ii-v-fig'])}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor):
    """One entry of a printed numbered list ("1." on its own line, its item on the next)."""
    return _C(page, f'{n}.', end, after=anchor, br=True)


def tick(clip, answer):
    return G('tick-col', page=8, clip=clip, headers=['True', 'False'], expect=answer, marks=8)


def bundled(parts, also=''):
    return f'The old card bundled {parts}; it keeps its id for {also}.'


Q1 = _A(3, 'Answer the following parts (a) to (e):')
Q2 = _A(4, 'Indicate whether the following statements', 'appropriate box in each case.')
Q3 = [_A(4, 'Choose each term from the following list', 'Column A.'), _A(4, 'Villi'), _A(4, 'Liver'),
      _A(4, 'Bile'), _A(4, 'Egestion'), _A(4, 'Peristalsis')]
Q4 = _A(5, 'An athlete obtains energy from glucose in aerobic', 'summary of aerobic respiration.')
Q5 = _A(6, 'The diagram shows a light microscope.')
Q6 = _A(7, 'The diagram represents a part of a DNA molecule.', 'Complete the following in relation to DNA.')
Q7 = _A(8, 'The diagram shows a neuron (nerve cell).')
Q8B = _A(9, 'The table shows the results of an ecological', 'follow based on this survey.')
Q10A = _A(11, 'It is important to use sterile apparatus when working with micro-organisms.')
Q10B = _A(11, 'The following data table shows the difference', 'months of May and September.')
Q11B = _C(2, 'Answer the following questions in relation to ecological pyramids.')
Q11C = [_C(2, 'Read the passage below and answer the questions that follow.'),
        _C(2, 'Essential nutrients, such as nitrogen', 'content of the soil.'),
        _C(2, 'Moist soil allows chemical reactions', 'important for healthy soils.'),
        _C(2, 'Adapted from “The dark mysteries of the soil beneath our feet”', '17th September 2021.')]
Q12B = _C(3, 'In humans, the allele for brown eyes (B) is dominant', 'blue eyes (b).')
Q12C = _C(3, 'Tissue culture is an important biological technique', 'nutrient medium.')
Q13A = _C(4, 'Photosynthesis is an important metabolic reaction in biology.')
Q13B = _C(4, 'The diagram shows a cross section of the internal', 'occur within the cells of the leaf.')
Q14A = _C(5, 'Oestrogen is one of the female reproductive hormones.')
Q14B = _C(5, 'The diagram shows the reproductive system of a human female.')
Q14C = _C(5, 'Answer the following questions in relation to', 'pregnancy and birth.')
Q15B = _C(6, 'The following questions relate to the human breathing system.')
Q15C = _C(6, 'The diagram shows a section through a human heart.')
Q16A = _C(7, 'The diagram shows a section through a human', 'responsible for excretion.')
Q16B = _C(7, 'The diagram shows a section through', 'the human eye.', after='Name an excretory organ')
Q16C = _C(8, 'The diagram shows a transverse section', 'through part of a root.')
Q16D = _C(8, 'The diagram shows the structure of an', 'animal-pollinated flower.')
Q17A = _C(9, 'Answer the following questions based on the', 'human skeletal system.')
Q17B = _C(9, 'Answer the following questions based on the human endocrine system.')

TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Give one source of carbohydrate in the diet.'),
      [pt(S('Any correct source'), 7, kind='criterion')], 'bio-1-2', 'dietary-carbohydrate',
      SQ(8, 'Give one source of carbohydrate in the diet.'), 7, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'Name one element found in carbohydrates.'),
      [pt(S('Carbon or hydrogen or oxygen'), 7)], 'bio-1-2', 'elements-in-carbohydrates',
      SQ(8, 'Name one element found in carbohydrates.'), 7, stem=[Q1], id='bio-2023-ol-q1-b'),
    T('1c', 'Q1(c)', 'A', _A(3, 'Give one structural role of carbohydrates in living organisms.'),
      [pt(S('They make up plant cell walls or other correct role'), 7)], 'bio-1-2',
      'structural-role-of-carbohydrate', SQ(8, 'Give one structural role of carbohydrates'), 7, stem=[Q1],
      id='bio-2023-ol-q1-c'),
    T('1d', 'Q1(d)', 'A', _A(3, 'Two monosaccharides can join together to form a'),
      [pt(S('Disaccharide'), 7)], 'bio-1-2', 'disaccharide', SQ(8, 'Two monosaccharides can join together'), 7,
      stem=[Q1], id='bio-2023-ol-q1-d'),
    T('1e', 'Q1(e)', 'A', _A(3, 'Name a polysaccharide found in plants.'),
      [pt(S('Starch or cellulose or pectin or other correct'), 7)], 'bio-1-2', 'plant-polysaccharides',
      SQ(8, 'Name a polysaccharide found in plants.'), 7, stem=[Q1], id='bio-2023-ol-q1-e'),
] + [
    T(f'2{x}', f'Q2({x})', 'A', _A(4, start), [tick(clip, answer)], topic, concept, SQ(8, start), 8,
      stem=[Q2], id=f'bio-2023-ol-q2-{x}')
    for x, start, clip, answer, topic, concept in [
        ('a', 'A hypothesis is a possible explanation for an observation.', (55, 420, 560, 444), 'True', 'bio-u2',
         'hypothesis'),
        ('b', 'A good experiment requires a small sample size.', (55, 444, 560, 467), 'False', 'bio-u2',
         'sample-size'),
        ('c', 'Data always involves numbers.', (55, 467, 560, 489), 'False', 'bio-u2', 'data'),
        ('d', 'Safety is an important principle of experimentation.', (55, 489, 560, 512), 'True', 'bio-u2',
         'safety'),
        ('e', 'Random selection is an important principle of experimentation.', (55, 512, 560, 535), 'True',
         'bio-u2', 'random-selection'),
        ('f', 'The scientific method has limitations.', (55, 535, 560, 559), 'True', 'bio-u1',
         'limitations-of-scientific-method'),
        ('g', 'A theory is an unsupported hypothesis.', (55, 559, 560, 583), 'False', 'bio-u1', 'theory')]
] + [
    T(f'3{x}', f'Q3({x})', 'A', _A(4, desc, end), [pt(S(answer), 7)], 'bio-2-6', concept, SQ(9, sq), 7,
      stem=Q3, id='bio-2023-ol-q3' if x == 'a' else None,
      decision='Lettered parts are separate printed addresses; the completed example (Hydrochloric acid) and '
               'the sentence introducing it are left out of the stem.' + (
                   ' The old card bundled (a)-(e); it keeps its id for (a).' if x == 'a' else ''))
    for x, desc, end, sq, answer, concept in [
        ('a', 'Contraction and relaxation of the', 'muscles of the gut wall', 'Contraction and relaxation of the',
         'Peristalsis', 'peristalsis'),
        ('b', 'Stored in the gall bladder', None, 'Stored in the gall bladder.', 'Bile', 'bile'),
        ('c', 'Increase surface area for absorption in', 'the small intestine', 'Increase surface area for',
         'Villi', 'villi'),
        ('d', 'Process by which food waste is passed', 'from the body', 'Process by which food waste is',
         'Egestion', 'egestion'),
        ('e', 'Organ that breaks down alcohol', None, 'Organ that breaks down alcohol.', 'Liver',
         'liver-breaks-down-alcohol')]
] + [
    T('4a', 'Q4(a)', 'A', _A(5, 'Identify gases X and Y.'),
      [pt(S('X: O2 or oxygen'), 8), pt(S('Y: CO2 or carbon dioxide'), 8)], 'bio-2-2', 'respiration-gases',
      SQ(9, 'Identify gases X and Y.'), 16, stem=[Q4], fig='q4-equation'),
    T('4b', 'Q4(b)', 'A', _A(5, 'Aerobic respiration consists of two stages', 'amount of energy released.'),
      [pt(S('Stage 1: small amount of energy released'), 8), pt(S('Stage 2: large amount of energy released'), 8)],
      'bio-2-2', 'energy-from-each-stage', SQ(9, 'Describe the difference between the two stages'), 16,
      stem=[Q4], fig='q4-equation', id='bio-2023-ol-q4-b'),
    T('4c', 'Q4(c)', 'A', _A(5, 'State two ways in which the released energy may be used in living organisms.'),
      [anyn(S('Growth / repair / movement / other correct'), 2, 8)], 'bio-2-2', 'uses-of-energy',
      SQ(9, 'State two ways in which the released energy'), 16, stem=[Q4], fig='q4-equation',
      id='bio-2023-ol-q4-c'),
    T('4d', 'Q4(d)', 'A', _A(5, 'The athlete can also respire anaerobically', 'anaerobic respiration.'),
      [pt(S('Lactic acid'), 8)], 'bio-2-2', 'lactic-acid', SQ(9, 'Name the product formed in the athlete'), 8,
      stem=[Q4], fig='q4-equation', id='bio-2023-ol-q4-d'),
    T('5a', 'Q5(a)', 'A', _A(6, 'Names the parts of the microscope labelled A and B.'),
      [pt(S('A: Eye piece'), 8), pt(S('B: Objective (lens)'), 8)], 'bio-1-3', 'microscope-parts',
      SQ(10, 'Names the parts of the microscope labelled A and B.'), 16, stem=[Q5], fig='q5-microscope',
      id='bio-2023-ol-q5-a-fig',
      labels=[L('A', S('Eye piece', page=10), True), L('B', S('Objective (lens)', page=10), True)]),
    T('5b', 'Q5(b)', 'A', _A(6, 'Using the letter', 'source of light.'),
      [pt(S('Correct location indicated'), 8, kind='criterion')], 'bio-1-3', 'microscope-light-source',
      SQ(10, 'Using the letter'), 8, stem=[Q5], fig='q5-microscope'),
    T('5c', 'Q5(c)', 'A', _A(6, 'What is the function of the stage on the microscope?'),
      [pt(S('Hold the specimen (or slide)'), 8)], 'bio-1-3', 'microscope-stage',
      SQ(10, 'What is the function of the stage on the microscope?'), 8, stem=[Q5], fig='q5-microscope',
      id='bio-2023-ol-q5-c'),
    T('5d', 'Q5(d)', 'A', _A(6, 'If the magnification of lens A is x10', 'total magnification?'),
      [pt(S('X400'), 8)], 'bio-1-3', 'microscope-magnification', SQ(10, 'If the magnification of lens A'), 8,
      stem=[Q5], fig='q5-microscope', id='bio-2023-ol-q5-d'),
    T('5e', 'Q5(e)', 'A', _A(6, 'What is the function of a stain when using the light microscope?'),
      [pt(S('To make the cells more visible'), 8)], 'bio-1-3', 'why-stain',
      SQ(10, 'What is the function of a stain'), 8, stem=[Q5], fig='q5-microscope', id='bio-2023-ol-q5-e'),
    T('5f', 'Q5(f)', 'A', _A(6, 'The light microscope is one type of microscope.', 'another type of microscope.'),
      [pt(S('Electron'), 8)], 'bio-1-3', 'electron-microscope', SQ(10, 'Name another type of microscope.'), 8,
      stem=[Q5], fig='q5-microscope', id='bio-2023-ol-q5-f'),
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(7, ask, aend), rows, 'bio-1-2', concept, SQ(10, sq), total, stem=[Q6],
      fig='q6-dna', id=f'bio-2023-ol-q6-{x}')
    for x, ask, aend, rows, concept, sq, total in [
        ('a', 'How many strands make up a DNA molecule?', None, [pt(S('Two'), 8)], 'dna-strands',
         'How many strands make up a DNA molecule?', 8),
        ('b', 'Name any two nitrogenous bases found in DNA.', None,
         [anyn(S('Adenine / guanine / thymine / cytosine'), 2, 8)], 'dna-bases', 'Name any two nitrogenous bases',
         16),
        ('c', 'Three bases together are known as a', None, [pt(S('Codon or triplet'), 8)], 'codon',
         'Three bases together are known as a', 8),
        ('d', 'Where in the human cell would you expect to find most DNA?', None, [pt(S('Nucleus'), 8)],
         'where-dna-is', 'Where in the cell would you expect to find most DNA?', 8),
        ('e', 'DNA contains the instructions needed to make protein.', 'code.', [pt(S('Genetic'), 8)],
         'genetic-code', 'DNA contains the instructions needed to make protein.', 8),
        ('f', 'Name a complementary structure to DNA that is involved in protein synthesis.', None,
         [pt(S('RNA'), 8)], 'rna', 'Name a complementary structure to DNA', 8)]
] + [
    T('7a', 'Q7(a)', 'A', _A(8, 'Name the parts labelled A, B and C.'),
      [pt(S('Dendrite'), 8, label=S('A:')), pt(S('Axon'), 8, label=S('B:')),
       pt(S('Schwann cell or myelin sheath'), 8, label=S('C:'))], 'bio-2-4', 'parts-of-a-neuron',
      SQ(11, 'Name the parts A, B and C.'), 24, stem=[Q7], fig='q7-neuron',
      labels=[L('A', S('Dendrite', page=11), True), L('B', S('Axon', page=11), True),
              L('C', S('Schwann cell or myelin sheath', page=11), True)]),
    T('7b', 'Q7(b)', 'A', _A(8, 'Give the function of the part labelled A.'),
      [pt(S('Receive impulses'), 8)], 'bio-2-4', 'dendrite-function',
      SQ(11, 'Give the function of the part labelled A.'), 8, stem=[Q7], fig='q7-neuron',
      labels=[L('A', S('Dendrite', page=11), False), L('B', S('Axon', page=11), False),
              L('C', S('Schwann cell or myelin sheath', page=11), False)]),
    T('7c', 'Q7(c)', 'A', _A(8, 'In the box on the diagram above, draw an arrow', 'travel in this neuron.'),
      [pt(S('Arrow from left to right'), 8, kind='criterion')], 'bio-2-4', 'direction-of-impulse',
      SQ(11, 'Draw an arrow showing the direction'), 8, stem=[Q7], fig='q7-neuron'),
    T('7d', 'Q7(d)', 'A', _A(8, 'Name the chemicals used to transmit nerve impulses from one neuron to another.'),
      [pt(S('Neurotransmitters or named neurotransmitter'), 8)], 'bio-2-4', 'neurotransmitters',
      SQ(11, 'Name the chemicals used to transmit'), 8, stem=[Q7], fig='q7-neuron', id='bio-2023-ol-q7-d'),
    T('7e', 'Q7(e)', 'A', _A(8, 'Name any one disorder of the nervous system.'),
      [pt(S('Parkinson’s or paralysis or any other correct'), 8)], 'bio-2-4', 'nervous-disorders',
      SQ(11, 'Name any one disorder of the nervous system.'), 8, stem=[Q7], fig='q7-neuron',
      id='bio-2023-ol-q7-e'),
    # ------------------------------------------------------------ Section B --
    T('8a', 'Q8(a)', 'B', _A(9, 'Describe the difference between the terms, flora and fauna', 'note on each.'),
      [pt(S('Plants'), 5, label=S('Flora:')), pt(S('Animals'), 5, label=S('Fauna:'))], 'bio-3-1',
      'flora-and-fauna', SQ(12, 'Describe the difference between the terms, flora and fauna'), 10,
      id='bio-2023-ol-q8-a'),
    T('8bi', 'Q8(b)(i)', 'B', _A(9, 'Describe how this survey may have been', 'carried out.'),
      [anyn(S('Pen thrown over shoulder or randomly /', 'calculation / repeat'), 3, 9)], 'bio-3-1',
      'frequency-survey', SQ(12, 'Describe how this survey may have been carried out.'), 27, stem=[Q8B],
      fig='q8-table', id='bio-2023-ol-q8-b-i'),
    T('8bii', 'Q8(b)(ii)', 'B', _A(9, 'Calculate the percentage frequency of dandelion and grass in this habitat.'),
      [pt(S('Dandelion: 60%'), 9), pt(S('100%'), 9, label=S('Grass:', after='Dandelion: 60%'))], 'bio-3-1',
      'percentage-frequency', SQ(12, 'Calculate the percentage frequency'), 18, stem=[Q8B], fig='q8-table'),
    T('8biii', 'Q8(b)(iii)', 'B', _A(9, 'On the axes below, sketch (using pencil) a bar chart', 'Label both axes.'),
      [pt(S('Type of plant (or grass and dandelion)'), 9, label=S('x axis:')),
       pt(S('% frequency'), 9, label=S('y axis:')),
       pt(S('Bars representing dandelion and grass'), 9, kind='criterion')], 'bio-3-1', 'frequency-bar-chart',
      SQ(12, 'Sketch a bar chart to represent'), 27, stem=[Q8B], fig='q8-table', id='bio-2023-ol-q8-b-iii'),
    T('9a', 'Q9(a)', 'B', _A(10, 'What is meant by the term osmosis?'),
      [pt(S('Movement of water'), 5),
       pt(S('Through a semi-permeable membrane or from a region', 'region of low water concentration'), 5)],
      'bio-2-6', 'osmosis', SQ(13, 'What is meant by the term osmosis?'), 10, id='bio-2023-ol-q9-a'),
    T('9bi', 'Q9(b)(i)', 'B', _A(10, 'Draw a labelled diagram of the apparatus that you used to demonstrate osmosis.'),
      [pt(S('Diagram showing two solutions and membrane or tissue'), 9, kind='criterion'),
       pt(S('Any two correct labels'), 18, kind='criterion', units=[9, 9])], 'bio-2-6', 'osmosis-apparatus',
      SQ(13, 'Draw a labelled diagram of the apparatus'), 27, id='bio-2023-ol-q9-b-i'),
    T('9bii', 'Q9(b)(ii)', 'B', _A(10, 'Describe how you carried out the experiment to demonstrate osmosis.'),
      [anyn(S('Material described or tissue mentioned /', 'or other correct step'), 4, 9)], 'bio-2-6',
      'demonstrating-osmosis', SQ(13, 'Describe how you carried out the experiment'), 36, id='bio-2023-ol-q9-b-ii'),
    T('9biii', 'Q9(b)(iii)', 'B', _A(10, 'How were you able to tell that osmosis had taken place?'),
      [pt(S('Mass or volume or shape changed'), 9)], 'bio-2-6', 'evidence-of-osmosis',
      SQ(13, 'How were you able to tell that osmosis had taken place?'), 9, id='bio-2023-ol-q9-b-iii'),
    T('10ai', 'Q10(a)(i)', 'B', _A(11, 'What is meant by the term sterile?'),
      [pt(S('Free from microorganisms'), 5)], 'bio-3-2', 'sterile', SQ(14, 'What is meant by the term sterile?'), 5,
      stem=[Q10A], id='bio-2023-ol-q10-a', decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added')),
    T('10aii', 'Q10(a)(ii)', 'B', _A(11, 'Give one method of sterilising apparatus.'),
      [pt(S('Autoclave or flaming'), 5)], 'bio-3-2', 'sterilising-apparatus',
      SQ(14, 'Give one method of sterilising apparatus.'), 5, stem=[Q10A]),
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'B', _A(11, ask, aend), rows, 'bio-3-2', concept, SQ(14, sq), total,
      stem=[Q10B], fig='q10-table', id=old, decision=dec)
    for r, ask, aend, rows, concept, sq, total, old, dec in [
        ('i', 'Name a suitable plant from which leaves can be obtained', 'investigation.',
         [pt(S('Ash or other correct'), 9)], 'plant-for-leaf-yeast', 'Name a suitable plant from which leaves', 9,
         'bio-2023-ol-q10-b-i-iii', bundled('(b)(i)-(iii)', '(i), and (ii), (iii) are added')),
        ('ii', 'Name a suitable container that can be used to grow leaf yeast.', None,
         [pt(S('Petri dish'), 9)], 'container-for-leaf-yeast', 'Name a suitable container', 9, None, ''),
        ('iii', 'Suggest a reason for the presence of malt in the agar.', None,
         [pt(S('Food source for yeast'), 9)], 'malt-agar', 'Suggest a reason for the presence of malt', 9, None, ''),
        ('iv', 'Describe how leaf yeast could be introduced into the malt agar.', None,
         [anyn(S('Cut leaf to size /', 'agar'), 2, 9)], 'introducing-leaf-yeast',
         'Describe how leaf yeast could be introduced', 18, 'bio-2023-ol-q10-b-iv-v',
         bundled('(b)(iv) and (v)', '(iv), and (v) is added')),
        ('v', 'Describe a suitable control for this investigation.', None,
         [pt(S('Same setup with no leaf or same setup with a sterilised leaf'), 9)], 'leaf-yeast-control',
         'Describe a suitable control for this investigation.', 9, None, ''),
        ('vi', 'What colour are leaf yeast colonies on malt agar?', None, [pt(S('Pink'), 9)], 'leaf-yeast-colour',
         'What colour are leaf yeast colonies on malt agar?', 9, 'bio-2023-ol-q10-b-vi-vii',
         bundled('(b)(vi) and (vii)', '(vi), and (vii) is added')),
        ('vii', 'Suggest a reason for the lower number of leaf yeast colonies', 'May versus September.',
         [pt(S('Younger leaves or not enough time for leaf yeast to grow'), 9)], 'fewer-colonies-in-may',
         'Suggest a reason for the lower number of leaf yeast', 9, None, '')]
] + [
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'What is meant by the term pollution?'),
      [pt(S('Any harmful addition to the environment'), 5)], 'bio-3-1', 'pollution',
      SQ(15, 'What is meant by the term pollution?'), 5, id='bio-2023-ol-q11-a-i'),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Describe one human activity that may cause pollution', 'could be controlled.'),
      [pt(S('Human activity: Any valid activity'), 5, kind='criterion'),
       pt(S('Any valid and matching preventative measure'), 5, kind='criterion', label=S('Prevent:'))],
      'bio-3-1', 'pollution-and-control', SQ(15, 'Describe one human activity that may cause pollution'), 10),
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Match pyramids A and B above', 'marine.'),
      [pt(S('Woodland or grassland'), 5, label=S('A:', after='Match pyramids A and B')),
       pt(S('Rocky seashore or marine'), 5, label=S('B:', after='Woodland or grassland'))], 'bio-3-1',
      'pyramids-and-ecosystems', SQ(15, 'Match pyramids A and B above'), 10, stem=[Q11B], fig='q11-pyramids',
      id='bio-2023-ol-q11-b-i-ii-iv-fig', decision=bundled('(b)(i), (ii) and (iv)', '(i), and (ii), (iv) are added')),
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', _C(2, ask, aend), [pt(S(ans), 5)], 'bio-3-1', concept, SQ(15, sq), 5,
      stem=[Q11B], fig='q11-pyramids', id=old, decision=dec)
    for r, ask, aend, ans, concept, sq, old, dec in [
        ('ii', 'Name the producer in pyramid A.', None, 'Grass', 'producer', 'Name a producer in pyramid A.', None, ''),
        ('iii', 'Name a source of energy for a producer.', None, 'Sun', 'energy-source',
         'Name the source of energy for the producer.', 'bio-2023-ol-q11-b-iii-v-viii',
         bundled('(b)(iii), (v) and (viii)', '(iii), and (v), (viii) are added')),
        ('iv', 'Name the primary consumer in pyramid B.', None, 'Sea slug', 'primary-consumer',
         'Name the primary consumer in pyramid B.', None, ''),
        ('v', 'What information do ecological pyramids provide us with?', None,
         '(Relative) numbers of organisms (at each trophic level)', 'what-pyramids-show',
         'What information do ecological pyramids provide us with?', None, ''),
        ('vi', 'Suggest what might happen if the bladderwrack was removed', 'pyramid B.',
         'The numbers of sea slugs would decrease or other correct', 'removing-the-producer',
         'Suggest what might happen if the bladderwrack', 'bio-2023-ol-q11-b-vi-vii-fig',
         bundled('(b)(vi) and (vii)', '(vi), and (vii) is added')),
        ('vii', 'Suggest what might happen if the top consumer in pyramid A died off', 'disease.',
         'The numbers of mice would increase or other correct', 'losing-the-top-consumer',
         'Suggest what might happen if the top consumer', None, ''),
        ('viii', 'How might you identify the animals and plants listed in the pyramids?', None,
         'Key or other correct', 'identifying-organisms', 'How might you identify the animals and plants', None, '')]
] + [
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'What ecological term describes soil factors?'),
      [pt(S('Edaphic'), 6)], 'bio-3-1', 'edaphic-factors', SQ(16, 'What ecological term describes soil factors?'), 6,
      stem=Q11C, id='bio-2023-ol-q11-c-i-iii', decision=bundled('(c)(i)-(iii)', '(i), and (ii), (iii) are added')),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Name any two essential nutrients present in healthy soil.'),
      [anyn(S('Nitrogen / potassium / other correct'), 2, 6)], 'bio-3-1', 'soil-nutrients',
      SQ(16, 'Name any two essential nutrients present in healthy soil.'), 12, stem=Q11C),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'Name any two soil factors that can have an effect', 'the soil.'),
      [anyn(S('pH / temperature / moisture content /', 'size / other correct'), 2, 6)], 'bio-3-1', 'soil-factors',
      SQ(16, 'Name any two soil factors'), 12, stem=Q11C),
    T('11civ', 'Q11(c)(iv)', 'C', _C(2, 'Give one biotic factor mentioned in the article.'),
      [pt(S('Any one correct'), 6, kind='criterion')], 'bio-3-1', 'biotic-factor-in-soil',
      SQ(16, 'Give one biotic factor mentioned in the article.'), 6, stem=Q11C),
    T('11cv', 'Q11(c)(v)', 'C', _C(2, 'Suggest a possible source of nitrogen compounds in the soil.'),
      [pt(S('Decay of organic matter or other correct'), 6)], 'bio-3-2', 'nitrogen-in-soil',
      SQ(16, 'Suggest a possible source of nitrogen compounds'), 6, stem=Q11C, id='bio-2023-ol-q11-c-v-vi',
      decision=bundled('(c)(v) and (vi)', '(v), and (vi) is added')),
    T('11cvi', 'Q11(c)(vi)', 'C', _C(2, 'Decomposers are important in recycling nutrients.', 'to be recycled.'),
      [pt(S('So they can be reused by other organisms or so they do not run out'), 6)], 'bio-3-2',
      'why-recycle-nutrients', SQ(16, 'Give a reason why it is important for nutrients'), 6, stem=Q11C),
    T('12ai', 'Q12(a)(i)', 'C', _C(3, 'Name the two biochemicals that make up chromosomes.'),
      [pt(S('Protein'), 5), pt(S('DNA'), 5)], 'bio-1-4', 'chromosome-composition',
      SQ(17, 'Name the two biochemicals that make up chromosomes.'), 10, id='bio-2023-ol-q12-a',
      decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added')),
    T('12aii', 'Q12(a)(ii)', 'C', _C(3, 'How many chromosomes are in a diploid human cell?'),
      [pt(S('46'), 5)], 'bio-1-4', 'diploid-number', SQ(17, 'How many chromosomes are in a diploid human cell?'), 5),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'Explain the underlined terms.'),
      [pt(S('Form of a gene'), 5, label=S('Allele:')), pt(S('Masks effect of recessive allele'), 5,
                                                          label=S('Dominant:'))],
      'bio-1-4', 'allele-and-dominant', SQ(17, 'Explain the underlined terms.'), 10, stem=[Q12B],
      qfig='q12b-i-question', id='bio-2023-ol-q12-b-i',
      decision='The paper marks the terms to explain by underlining them, which the text layer drops: the '
               'question is shown as the paper prints it.'),
    T('12bii', 'Q12(b)(ii)', 'C', _C(3, 'Jack’s genotype is Bb.', 'What colour are Jack’s eyes?'),
      [pt(S('Brown'), 5)], 'bio-1-4', 'heterozygous-phenotype', SQ(17, 'What colour are Jack’s eyes?'), 5,
      stem=[Q12B], id='bio-2023-ol-q12-b-ii-iv-fig', decision=bundled('(b)(ii)-(iv)', '(ii), and (iii), (iv) are added')),
    T('12biii', 'Q12(b)(iii)', 'C', [_C(3, 'Which of the following terms describes Jack’s genotype?'),
                                     _C(3, 'homozygous;', 'heterozygous.', br=True)],
      [pt(S('Heterozygous'), 5)], 'bio-1-4', 'heterozygous', SQ(17, 'Which of the following terms describes'), 5,
      stem=[Q12B, _C(3, 'Jack’s genotype is Bb.', 'Jack’s genotype is Bb.')]),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'Sarah has blue eyes.', 'genotype for eye colour.'),
      [pt(S('bb'), 5)], 'bio-1-4', 'homozygous-recessive', SQ(17, 'Write out Sarah’s genotype for eye colour.'), 5,
      stem=[Q12B]),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'Give the genotypes of the two possible gametes that Jack can produce.'),
      [pt(S('B'), 5), pt(S('b'), 5)], 'bio-1-4', 'gametes', SQ(17, 'Give the genotypes of the two possible gametes'),
      10, stem=[Q12B, _C(3, 'Jack’s genotype is Bb.', 'Jack’s genotype is Bb.')], id='bio-2023-ol-q12-b-v-vi-fig',
      decision=bundled('(b)(v) and (vi)', '(v), and (vi) is added')),
    T('12bvi', 'Q12(b)(vi)', 'C', _C(3, 'If Sarah and Jack were to have children', 'possible offspring.'),
      [pt(S('Brown eyes'), 5), pt(S('Blue eyes'), 5)], 'bio-1-4', 'offspring-phenotypes',
      SQ(17, 'Write out the two phenotypes of their possible offspring.'), 10,
      stem=[Q12B, _C(3, 'Jack’s genotype is Bb.', 'Jack’s genotype is Bb.'), _C(3, 'Sarah has blue eyes.', 'Sarah has blue eyes.')]),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'Distinguish between a tissue and an organ', 'on each.'),
      [pt(S('Group of cells with a shared function'), 6, label=S('Tissue:')),
       pt(S('A group of tissues with a shared function.'), 6, label=S('Organ:'))], 'bio-1-3', 'tissues-and-organs',
      SQ(18, 'Distinguish between a tissue and an organ'), 12, stem=[Q12C], id='bio-2023-ol-q12-c-i-ii',
      decision=bundled('(c)(i) and (ii)', '(i), and (ii) is added')),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Name two types of tissue found in animals.'),
      [anyn(S('Muscle / epithelial (or epidermal) / nervous / connective'), 2, 6)], 'bio-1-3', 'animal-tissues',
      SQ(18, 'Name two types of tissue found in animals.'), 12, stem=[Q12C]),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Suggest one reason why sterile conditions are necessary in tissue culture.'),
      [pt(S('Prevent contamination (with unwanted microorganisms)'), 6)], 'bio-1-3', 'tissue-culture-conditions',
      SQ(18, 'Suggest one reason why sterile conditions'), 6, stem=[Q12C], id='bio-2023-ol-q12-c-iii-vi',
      decision=bundled('(c)(iii)-(vi)', '(iii), and (iv)-(vi) are added')),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Name the type of cell division that occurs in tissue culture', 'are grown.'),
      [pt(S('Mitosis'), 6)], 'bio-2-3', 'mitosis-in-tissue-culture', SQ(18, 'Name the type of cell division'), 6,
      stem=[Q12C]),
    T('12cv', 'Q12(c)(v)', 'C', _C(3, 'How many cells result from one cell undergoing', 'part (c) (iv) above?'),
      [pt(S('2'), 6)], 'bio-2-3', 'products-of-mitosis', SQ(18, 'How many cells result from one cell'), 6,
      stem=[Q12C, M('(iv)', 3), _C(3, 'Name the type of cell division that occurs in tissue culture', 'are grown.')]),
    T('12cvi', 'Q12(c)(vi)', 'C', _C(3, 'Give one application of tissue culture.'),
      [pt(S('Plant breeding or micropropagation or cancer research or skin grafts or other correct'), 6)],
      'bio-1-3', 'tissue-culture-uses', SQ(18, 'Give one application of tissue culture.'), 6, stem=[Q12C]),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Name a pigment essential for photosynthesis.'),
      [pt(S('Chlorophyll'), 5)], 'bio-2-2', 'chlorophyll', SQ(19, 'Name a pigment essential for photosynthesis.'), 5,
      stem=[Q13A], id='bio-2023-ol-q13-a', decision=bundled('(a)(i)-(iii)', '(i), and (ii), (iii) are added')),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Where in a plant cell can the pigment you named', 'be found?'),
      [pt(S('Chloroplast'), 5)], 'bio-2-2', 'chloroplast', SQ(19, 'Where in a plant cell can the pigment'), 5,
      stem=[Q13A, M('(i)', 4), _C(4, 'Name a pigment essential for photosynthesis.')]),
    T('13aiii', 'Q13(a)(iii)', 'C', _C(4, 'This pigment is involved in trapping energy.', 'source of this energy.'),
      [pt(S('Sunlight (or other correct)'), 5)], 'bio-2-2', 'light-energy', SQ(19, 'Give one source of this energy.'),
      5, stem=[Q13A, M('(i)', 4), _C(4, 'Name a pigment essential for photosynthesis.')]),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Water is split into three products during', 'Name the three products.'),
      [pt(S('Oxygen or O2'), 5), pt(S('Electrons or e–'), 5), pt(S('Protons or H+ or H ions'), 5)], 'bio-2-2',
      'splitting-water', SQ(19, 'Name the three products of the splitting of water.'), 15, stem=[Q13B],
      fig='q13-leaf', id='bio-2023-ol-q13-b-i'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Where does the plant obtain the water', 'required for photosynthesis?'),
      [pt(S('Through roots or from the soil or from xylem or other correct'), 5)], 'bio-2-2', 'source-of-water',
      SQ(19, 'Where does the plant obtain the water'), 5, stem=[Q13B], fig='q13-leaf', id='bio-2023-ol-q13-b-ii-vi',
      decision=bundled('(b)(ii), (iii), (v) and (vi)', '(ii), and (iii), (v), (vi) are added')),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Suggest a reason for the leaf being very thin.'),
      [pt(S('To allow light to penetrate the leaf or other correct reason'), 5)], 'bio-2-2', 'thin-leaves',
      SQ(19, 'Suggest a reason for the leaf being very thin.'), 5, stem=[Q13B], fig='q13-leaf'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'Gas X is required for photosynthesis and can', 'Name gas X.'),
      [pt(S('Carbon dioxide'), 5)], 'bio-2-2', 'carbon-dioxide', SQ(19, 'Name gas X.'), 5, stem=[Q13B],
      fig='q13-leaf', id='bio-2023-ol-q13-b-iv-fig'),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'What is the main product of photosynthesis?'),
      [pt(S('Glucose or sugar'), 5)], 'bio-2-2', 'glucose', SQ(19, 'What is the main product of photosynthesis?'), 5,
      stem=[Q13B], fig='q13-leaf'),
    T('13bvi', 'Q13(b)(vi)', 'C', _C(4, 'Using your knowledge of photosynthesis, describe two methods', 'greenhouses.'),
      [anyn(S('Carbon dioxide enrichment /', 'other correct'), 2, 5)], 'bio-2-2',
      'greenhouse-methods', SQ(19, 'Describe two methods horticulturists'), 10, stem=[Q13B], fig='q13-leaf'),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Chemicals called enzymes are involved in metabolism within cells.',
                                   'Explain the underlined terms.'),
      [pt(S('Biological catalysts'), 6, label=S('Enzymes:')),
       pt(S('(All) chemical reactions within an organism'), 6, label=S('Metabolism:'))], 'bio-2-1',
      'enzymes-and-metabolism', SQ(20, 'Explain the underlined terms.'), 12, qfig='q13c-i-question',
      id='bio-2023-ol-q13-c-i-iii',
      decision=bundled('(c)(i)-(iii)', '(i), and (ii), (iii) are added') + ' The paper marks the terms to '
               'explain by underlining them: the question is shown as the paper prints it.'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Where in a cell are enzymes produced?'),
      [pt(S('Ribosomes'), 6)], 'bio-2-1', 'where-enzymes-are-made', SQ(20, 'Where in a cell are enzymes produced?'),
      6),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Name two factors that can affect enzyme', 'action.'),
      [anyn(S('pH / temperature / enzyme concentration / substrate concentration'), 2, 6)], 'bio-2-1',
      'factors-affecting-enzymes', SQ(20, 'Name two factors that can affect enzyme action.'), 12),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'The diagram shows immobilised enzymes.', 'enzyme?'),
      [pt(S('Trapping in an inert material'), 6)], 'bio-2-1', 'immobilisation',
      SQ(20, 'What is meant by the immobilisation of an enzyme?'), 6, fig='q13-immobilised',
      id='bio-2023-ol-q13-c-iv-v', decision=bundled('(c)(iv) and (v)', '(iv), and (v) is added')),
    T('13cv', 'Q13(c)(v)', 'C', _C(4, 'Give two advantages of bioprocessing', 'using immobilised enzymes.'),
      [anyn(S('Can be reused / cleaner product / more efficient'), 2, 6)], 'bio-2-1', 'immobilised-enzyme-advantages',
      SQ(20, 'Give two advantages of bioprocessing'), 12),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'State one function of oestrogen.'),
      [pt(S('Causes lining of endometrium (uterus) to thicken or other correct'), 5)], 'bio-2-5', 'oestrogen',
      SQ(21, 'State one function of oestrogen'), 5, stem=[Q14A], id='bio-2023-ol-q14-a',
      decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added')),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Name one other female reproductive hormone and state its function.'),
      [pt(S('Progesterone'), 5, label=S('Name:', after='Name one other female reproductive hormone')),
       pt(S('Function: Keep lining of uterus built up or other correct'), 5)], 'bio-2-5', 'progesterone',
      SQ(21, 'Name one other female reproductive hormone'), 10, stem=[Q14A]),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Name the parts labelled A, B, and C.'),
      [pt(S('Ovary'), 5, label=S('A:')), pt(S('Fallopian tube'), 5, label=S('B:')), pt(S('Uterus'), 5, label=S('C:'))],
      'bio-2-5', 'female-reproductive-system', SQ(21, 'Name the parts labelled A, B, and C.'), 15, stem=[Q14B],
      fig='q14-female', id='bio-2023-ol-q14-b-i-fig',
      labels=[L('A', S('Ovary', page=21, after='Name the parts labelled A, B, and C.'), True),
              L('B', S('Fallopian tube', page=21), True), L('C', S('Uterus', page=21), True)]),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'In which labelled part is the ovum', '(egg) formed?'),
      [pt(S('Ovary or A'), 5)], 'bio-2-5', 'where-eggs-form', SQ(21, 'In which labelled part is the ovum'), 5,
      stem=[Q14B], fig='q14-female', id='bio-2023-ol-q14-b-ii-iv',
      decision=bundled('(b)(ii)-(iv)', '(ii), and (iii), (iv) are added')),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'What type of cell division is', 'ovum (egg)?'),
      [pt(S('Meiosis'), 5)], 'bio-2-5', 'meiosis-makes-eggs', SQ(21, 'What type of cell division is involved'), 5,
      stem=[Q14B], fig='q14-female'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'State one way in which the ovum', 'differs from a sperm cell.'),
      [pt(S('Non-motile or no tail or larger'), 5)], 'bio-2-5', 'egg-and-sperm', SQ(21, 'State one way in which the ovum'),
      5, stem=[Q14B], fig='q14-female'),
    T('14bv', 'Q14(b)(v)', 'C', _C(5, 'Explain the term fertilisation.'),
      [pt(S('Fusion of gametes or formation of zygote'), 5)], 'bio-2-5', 'fertilisation',
      SQ(21, 'Explain the term fertilisation.'), 5, stem=[Q14B], fig='q14-female', id='bio-2023-ol-q14-b-v-vi',
      decision=bundled('(b)(v) and (vi)', '(v), and (vi) 1. and 2. are added')),
] + [
    T(f'14bvi{n}', f'Q14(b)(vi){n}', 'C', [_C(5, 'State the location from the diagram', 'occurs:'),
                                         item(5, n, what, 'each of the following')],
      [row], 'bio-2-5', concept, SQ(21, 'State the location from the diagram above'), 5, stem=[Q14B],
      fig='q14-female', decision='"Each of the following": two separately priced items, one card each.')
    for n, what, row, concept in [
        (1, 'Fertilisation', pt(S('B or fallopian tube'), 5, label=S('Fertilisation:')), 'where-fertilisation-happens'),
        (2, 'Implantation', pt(S('Implantation: C or uterus or endometrium'), 5), 'where-implantation-happens')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'The placenta is a very important organ in', 'function of the placenta.'),
      [pt(S('Hormone production or transfer of nutrients', 'or other correct'), 6)], 'bio-2-5', 'placenta',
      SQ(22, 'Give any one function of the placenta.'), 6, stem=[Q14C], id='bio-2023-ol-q14-c-i-ii',
      decision=bundled('(c)(i) and (ii)', '(i), and (ii) is added')),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Describe the main events of the birth', 'process in humans.'),
      [pt(S('Labour or contractions or waters break or cervix dilates'), 6),
       pt(S('Parturition or baby passes through birth canal'), 6),
       pt(S('Afterbirth (or described) or umbilical cord cut'), 6)], 'bio-2-5', 'birth',
      SQ(22, 'Describe the main events of the birth process'), 18, stem=[Q14C]),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Describe any two biological benefits of', 'breastfeeding.'),
      [anyn(S('Baby receives antibodies /', 'any other correct benefit'), 2, 6)], 'bio-2-5', 'breastfeeding',
      SQ(22, 'Describe any two biological benefits'), 12, stem=[Q14C], id='bio-2023-ol-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'Name two methods of contraception.'),
      [pt(S('Any two correct methods or examples'), 12, kind='criterion', units=[6, 6])], 'bio-2-5', 'contraception',
      SQ(22, 'Name two methods of contraception.'), 12, stem=[Q14C]),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'Give two differences between an artery and a vein.'),
      [anyn(S('Arteries have thicker walls than veins /', 'carry blood towards heart.'), 2, 5)], 'bio-2-6',
      'arteries-and-veins', SQ(23, 'Give two differences between an artery and vein.'), 10, id='bio-2023-ol-q15-a',
      decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added')),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Name the small blood vessels that are responsible', 'with body cells.'),
      [pt(S('Capillaries'), 5)], 'bio-2-6', 'capillaries', SQ(23, 'Name the small blood vessels'), 5),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'Where in the body are the lungs located?'),
      [pt(S('Chest or thorax or behind ribs'), 5)], 'bio-2-6', 'where-the-lungs-are',
      SQ(23, 'Where in the body are the lungs located?'), 5, stem=[Q15B], id='bio-2023-ol-q15-b-i-iii',
      decision=bundled('(b)(i)-(iii)', '(i), and (ii), (iii) are added')),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'What is the function of the rings of cartilage found in the trachea?'),
      [pt(S('Keep trachea open or prevent collapse of trachea'), 5)], 'bio-2-6', 'tracheal-cartilage',
      SQ(23, 'What is the function of the rings of cartilage'), 5, stem=[Q15B]),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Give the function of the alveoli in the lungs', 'carry out this role.'),
      [pt(S('Function: Gas exchange'), 5), pt(S('Feature: Thin wall or moisture layer or surrounded by capillaries'), 5)],
      'bio-2-6', 'alveoli', SQ(23, 'Give the function of alveoli'), 10, stem=[Q15B]),
] + [
    T(f'15biv{n}', f'Q15(b)(iv){n}', 'C', [_C(6, 'Describe the role of each of the following during inhalation:'),
                                         item(6, n, what, 'during inhalation:')],
      [row], 'bio-2-6', concept, SQ(23, 'Describe the role of each of the following during inhalation:'), 5,
      stem=[Q15B], id='bio-2023-ol-q15-b-iv' if n == 1 else None,
      decision=('The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added. ' if n == 1 else '')
      + '"Each of the following": three separately priced items, one card each.')
    for n, what, row, concept in [
        (1, 'Diaphragm', pt(S('Contracts or moves down or increases chest volume'), 5,
                            label=S('Diaphragm', after='Describe the role of each')), 'diaphragm-in-inhalation'),
        (2, 'Intercostal muscles', pt(S('Intercostal muscles: Contracts or causes', 'increases chest volume'), 5),
         'intercostals-in-inhalation'),
        (3, 'Brain', pt(S('Brain sends signal to muscles'), 5, label=S('Brain:')), 'brain-in-inhalation')]
] + [
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'Name one breathing disorder and give a possible cause.'),
      [pt(S('Bronchitis or asthma or other correct'), 5, label=S('Name:', after='breathing disorder')),
       pt(S('Matching cause named or described'), 5, kind='criterion', label=S('Cause:'))], 'bio-2-6',
      'breathing-disorder', SQ(23, 'Name one breathing disorder'), 10, stem=[Q15B], id='bio-2023-ol-q15-b-v'),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'Name the blood vessel labelled A.'),
      [pt(S('Aorta'), 6)], 'bio-2-6', 'aorta', SQ(24, 'Name the blood vessel labelled A.'), 6, stem=[Q15C],
      fig='q15-heart', id='bio-2023-ol-q15-c-i-ii-fig', decision=bundled('(c)(i) and (ii)', '(i), and (ii) is added'),
      labels=[L('A', S('Aorta', page=24), True)]),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Give one reason why the wall of', 'of chamber C.'),
      [pt(S('Pumps blood further or maintains blood pressure'), 6)], 'bio-2-6', 'left-ventricle-wall',
      SQ(24, 'Give one reason why the wall of chamber B'), 6, stem=[Q15C], fig='q15-heart'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'What is the role of the bicuspid', 'valve?'),
      [pt(S('Prevents backflow of blood (into the left atrium)'), 6)], 'bio-2-6', 'bicuspid-valve',
      SQ(24, 'What is the role of the bicuspid valve?'), 6, stem=[Q15C], fig='q15-heart', id='bio-2023-ol-q15-c-iii-v',
      decision=bundled('(c)(iii)-(v)', '(iii), and (iv), (v) 1. and 2. are added')),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Which part of the heart prevents', 'deoxygenated blood?'),
      [pt(S('Septum'), 6)], 'bio-2-6', 'septum', SQ(24, 'Which part of the heart prevents'), 6, stem=[Q15C],
      fig='q15-heart'),
    T('15cv1', 'Q15(c)(v)1', 'C', _C(6, 'Name the artery through', 'receives blood.'),
      [pt(S('Coronary (artery)'), 6)], 'bio-2-6', 'coronary-artery', SQ(24, '1. Name the artery through which'), 6,
      stem=[Q15C], fig='q15-heart'),
    T('15cv2', 'Q15(c)(v)2', 'C', _C(6, 'Suggest what might happen if this artery became blocked.'),
      [pt(S('Heart attack'), 6)], 'bio-2-6', 'blocked-coronary-artery', SQ(24, '2. Suggest what might happen'), 6,
      stem=[Q15C, M('1.', 6), _C(6, 'Name the artery through', 'receives blood.')], fig='q15-heart'),
    T('15cvi', 'Q15(c)(vi)', 'C', _C(6, 'Give one factor that can cause an increase in heart rate.'),
      [pt(S('Exercise or smoking or other correct'), 6)], 'bio-2-6', 'raising-heart-rate',
      SQ(24, 'Give one factor that can cause an increase in heart rate.'), 6, stem=[Q15C], fig='q15-heart',
      id='bio-2023-ol-q15-c-vi-vii', decision=bundled('(c)(vi) and (vii)', '(vi), and (vii) is added')),
    T('15cvii', 'Q15(c)(vii)', 'C', _C(6, 'State one feature of the diet that can harm the circulatory system.'),
      [pt(S('High fat diet or diet high in cholesterol or diet high in salt'), 6)], 'bio-2-6', 'diet-and-heart',
      SQ(24, 'State one feature of the diet'), 6, stem=[Q15C], fig='q15-heart'),
    # Q16: any two of (a)-(d), each 30, laddered "2(7) + 8(2)".
    T('16ai', 'Q16(a)(i)', 'C', _C(7, 'Explain in detail the term excretion.'),
      [pt(S('Removal of waste products'), 7), pt(S('Of metabolism or from the cell or made in the body'), 7)],
      'bio-2-6', 'excretion', SQ(25, 'Explain in detail the term excretion.'), 14, stem=[Q16A], fig='q16-kidney',
      id='bio-2023-ol-q16a-i'),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'Match the parts labelled D, E and F with the', 'cortex'),
      [pt(S('Cortex'), 7, label=S('D:')), pt(S('Medulla'), 7, label=S('E:')), pt(S('(Renal) pelvis'), 7, label=S('F:'))],
      'bio-2-6', 'parts-of-the-kidney', SQ(25, 'Match the parts labelled D, E, and F'), 21, stem=[Q16A],
      fig='q16-kidney', id='bio-2023-ol-q16a-ii-fig',
      labels=[L('D', S('Cortex', page=25, after='Match the parts labelled D'), True),
              L('E', S('Medulla', page=25), True), L('F', S('(Renal) pelvis', page=25), True)]),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'The ureter connects the kidney to another', 'Name this other part.'),
      [pt(S('Bladder'), 7)], 'bio-2-6', 'bladder', SQ(25, 'Name this other part.'), 7, stem=[Q16A], fig='q16-kidney',
      id='bio-2023-ol-q16-a-iii'),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'The kidneys are surrounded by a thick layer of fat.', 'layer of fat.', end_nth=2),
      [pt(S('Protection'), 7)], 'bio-2-6', 'fat-around-kidneys', SQ(25, 'Give one function of this layer of fat.'), 7,
      stem=[Q16A], fig='q16-kidney', id='bio-2023-ol-q16-a-iv'),
] + [
    T(f'16av{n}', f'Q16(a)(v){n}', 'C', [_C(7, 'Filtration, reabsorption and secretion are essential', 'following:'),
                                       item(7, n, what, 'Give the location in the kidney')],
      [row], 'bio-2-6', concept, SQ(25, 'Give the locations in the kidney for each of the following:'), 7,
      stem=[Q16A], fig='q16-kidney', id='bio-2023-ol-q16a-v-vi' if n == 1 else None,
      decision=('The old card bundled (a)(v) and (vi); it keeps its id for (v)1., and (v)2. and (vi) are added. '
                if n == 1 else '') + '"Each of the following": two separately priced items, one card each.')
    for n, what, row, concept in [
        (1, 'Filtration', pt(S('Cortex or D or Bowman’s capsule or glomerulus'), 7, label=S('Filtration:')),
         'where-filtration-happens'),
        (2, 'Reabsorption', pt(S('Reabsorption: Cortex or D or medulla or E', 'part of nephron'), 7),
         'where-reabsorption-happens')]
] + [
    T('16avi', 'Q16(a)(vi)', 'C', _C(7, 'Name an excretory organ in the human body, other than the kidney.'),
      [pt(S('Skin or lungs'), 7)], 'bio-2-6', 'other-excretory-organs', SQ(25, 'Name an excretory organ'), 7,
      stem=[Q16A], fig='q16-kidney'),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'Match the parts labelled', 'cornea', after='the human eye.'),
      [pt(S('X: Iris'), 7), pt(S('Y: Cornea'), 7), pt(S('Z: Lens'), 7)], 'bio-2-4', 'parts-of-the-eye',
      SQ(26, 'Match the parts labelled X, Y and Z'), 21, stem=[Q16B], fig='q16-eye', id='bio-2023-ol-q16b-i-fig',
      labels=[L('X', S('Iris', page=26), True), L('Y', S('Cornea', page=26), True), L('Z', S('Lens', page=26), True)]),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'What is the function of the', 'part labelled Y?'),
      [pt(S('Allows light to enter the eye'), 7)], 'bio-2-4', 'cornea-function',
      SQ(26, 'What is the function of the part labelled Y?'), 7, stem=[Q16B], fig='q16-eye',
      id='bio-2023-ol-q16b-ii-v', decision=bundled('(b)(ii)-(v)', '(ii), and (iii)-(v) are added'),
      labels=[L('X', S('Iris', page=26), False), L('Y', S('Cornea', page=26), True), L('Z', S('Lens', page=26), False)]),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'Which labelled part focuses', 'the light rays?'),
      [pt(S('Z or lens (allow Y or cornea)'), 7)], 'bio-2-4', 'focusing-light',
      SQ(26, 'Which labelled part focuses the light rays?'), 7, stem=[Q16B], fig='q16-eye'),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'Where are light rays usually focused?'),
      [pt(S('Retina'), 7)], 'bio-2-4', 'retina', SQ(26, 'Where are light rays usually focused?'), 7, stem=[Q16B],
      fig='q16-eye'),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'The diameter (d) of the pupil changes', 'in bright light?'),
      [pt(S('Gets smaller'), 7)], 'bio-2-4', 'pupil-in-bright-light', SQ(26, 'What would you expect to happen'), 7,
      stem=[Q16B], fig='q16-eye'),
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'The optic nerve carries impulses.', 'do these impulses travel?'),
      [pt(S('Brain'), 7)], 'bio-2-4', 'optic-nerve', SQ(26, 'To which organ do these impulses travel?'), 7,
      stem=[Q16B], fig='q16-eye', id='bio-2023-ol-q16-b-vi'),
    T('16bvii', 'Q16(b)(vii)', 'C', _C(7, 'Name a disorder of the eye or the ear and give a corrective measure.'),
      [pt(S('Eye: Named disorder', 'Ear: Named disorder'), 7, kind='criterion', whole=True),
       pt(S('Matching corrective measure'), 7, kind='criterion')], 'bio-2-4', 'eye-or-ear-disorder',
      SQ(26, 'Name a disorder of the eye or the ear'), 14, stem=[Q16B], fig='q16-eye',
      decision='Eye or ear: the scheme marks both on the same two rows, under one topic, so the choice is one card.'),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'Match the plant tissues labelled', 'dermal'),
      [pt(S('A: Vascular'), 7), pt(S('Ground'), 7, label=S('B:')), pt(S('Dermal'), 7, label=S('C:'))], 'bio-2-6',
      'root-tissues', SQ(27, 'Match the plant tissues labelled A, B and C'), 21, stem=[Q16C], fig='q16-root',
      id='bio-2023-ol-q16c-i-fig',
      labels=[L('A', S('Vascular', page=27), True), L('B', S('Ground', page=27), True),
              L('C', S('Dermal', page=27, after='Ground'), True)]),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Give two substances that are', 'labelled A.'),
      [anyn(S('Water / food / mineral / other correct'), 2, 7)], 'bio-2-6', 'vascular-transport',
      SQ(27, 'Give two substances that are transported'), 14, stem=[Q16C], fig='q16-root',
      id='bio-2023-ol-q16c-ii-iii-fig', decision=bundled('(c)(ii) and (iii)', '(ii), and (iii) is added'),
      labels=[L('A', S('Vascular', page=27), False), L('B', S('Ground', page=27), False), L('C', S('Dermal', page=27, after='Ground'), False)]),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Name a type of cell located in the tissue labelled A.'),
      [pt(S('Xylem (tracheid or vessel) or phloem or sieve tube or companion (cell)'), 7)], 'bio-2-6',
      'vascular-cells', SQ(27, 'Name a type of cell located in the tissue labelled A.'), 7, stem=[Q16C],
      fig='q16-root', labels=[L('A', S('Vascular', page=27), False), L('B', S('Ground', page=27), False), L('C', S('Dermal', page=27, after='Ground'), False)]),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'What is the function of the root hair?'),
      [pt(S('Absorption'), 7)], 'bio-2-6', 'root-hair', SQ(27, 'What is the function of the root hair?'), 7,
      stem=[Q16C], fig='q16-root', id='bio-2023-ol-q16c-iv-v-fig',
      decision=bundled('(c)(iv) and (v)', '(iv), and (v) is added')),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Name any two ways in which a section through the stem', 'diagram above.'),
      [pt(S('No root hairs'), 7), pt(S('Many vascular bundles'), 7)], 'bio-2-6', 'stem-and-root-sections',
      SQ(27, 'Name any two ways in which a section'), 14, stem=[Q16C], fig='q16-root'),
    T('16cvi', 'Q16(c)(vi)', 'C', _C(8, 'What term describes a root’s growth in response to gravity?'),
      [pt(S('Geotropism'), 7)], 'bio-2-4', 'geotropism', SQ(27, 'What term describes a root’s growth'), 7,
      stem=[Q16C], fig='q16-root', id='bio-2023-ol-q16c-vi'),
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'Match the parts labelled X, Y and', 'stigma'),
      [pt(S('Stigma'), 7, label=S('X:')), pt(S('Ovule'), 7, label=S('Y:')), pt(S('Sepal'), 7, label=S('Z:'))],
      'bio-2-5', 'parts-of-a-flower', SQ(28, 'Match the parts X, Y and Z'), 21, stem=[Q16D], fig='q16-flower',
      id='bio-2023-ol-q16d-i-fig',
      labels=[L('X', S('Stigma', page=28), True), L('Y', S('Ovule', page=28), True), L('Z', S('Sepal', page=28), True)]),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'What is the function of the part', 'labelled Z?'),
      [pt(S('Protection (of the developing flower)'), 7)], 'bio-2-5', 'sepal-function',
      SQ(28, 'What is the function of the part labelled Z?'), 7, stem=[Q16D], fig='q16-flower',
      id='bio-2023-ol-q16d-ii-iii-fig', decision=bundled('(d)(ii) and (iii)', '(ii), and (iii) is added'),
      labels=[L('X', S('Stigma', page=28), False), L('Y', S('Ovule', page=28), False),
              L('Z', S('Sepal', page=28), True)]),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Pollen is produced by the anther.', 'grains received?'),
      [pt(S('X or stigma'), 7)], 'bio-2-5', 'where-pollen-lands', SQ(28, 'On which labelled part are pollen grains'),
      7, stem=[Q16D], fig='q16-flower'),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Give one possible adaptation of', 'animal-pollinated.'),
      [pt(S('Coloured petals or nectar or anthers (or stigma) inside flower or other correct'), 7)], 'bio-2-5',
      'animal-pollination-adaptations', SQ(28, 'Give one possible adaptation'), 7, stem=[Q16D], fig='q16-flower',
      id='bio-2023-ol-q16d-iv-v-fig', decision=bundled('(d)(iv) and (v)', '(iv), and (v) is added')),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Give one feature of a wind-pollinated flower.'),
      [pt(S('Small petals or green petals or feathery stigma or anthers outside flower or other correct'), 7)],
      'bio-2-5', 'wind-pollinated-flowers', SQ(28, 'Give one feature of a wind-pollinated flower.'), 7, stem=[Q16D], fig='q16-flower'),
    T('16dvi', 'Q16(d)(vi)', 'C', _C(8, 'In which labelled part does the seed develop?'),
      [pt(S('Y or ovule (accept ovary)'), 7)], 'bio-2-5', 'where-seeds-develop',
      SQ(28, 'In which labelled part does the seed develop?'), 7, stem=[Q16D], fig='q16-flower',
      id='bio-2023-ol-q16d-vi-viii', decision=bundled('(d)(vi)-(viii)', '(vi), and (vii), (viii) are added')),
    T('16dvii', 'Q16(d)(vii)', 'C', _C(8, 'Fruit formation follows seed formation.', 'fruit of a plant.'),
      [pt(S('Seed dispersal'), 7)], 'bio-2-5', 'fruit-function', SQ(28, 'Give one function of the fruit of a plant.'),
      7, stem=[Q16D], fig='q16-flower'),
    T('16dviii', 'Q16(d)(viii)', 'C', _C(8, 'Dormancy is a period during which the seed', 'benefit to a plant.'),
      [pt(S('Allows survival of adverse conditions or allows time for', 'or other correct'), 7)], 'bio-2-5',
      'dormancy', SQ(28, 'Give one reason why dormancy is of benefit'), 7, stem=[Q16D], fig='q16-flower'),
    # Q17: any two of (a)-(d), each 30, laddered "2(7) + 8(2)".
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'Give two functions of the human skeleton.'),
      [anyn(S('Strength / support / shape / movement / protection / blood cell production'), 2, 7)], 'bio-2-4',
      'functions-of-the-skeleton', SQ(29, 'Give two functions of the human skeleton.'), 14, stem=[Q17A],
      id='bio-2023-ol-q17a-i-iii', decision=bundled('(a)(i)-(iii)', '(i), and (ii), (iii) are added')),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Give one location in the human body where', 'a hinge joint is found.'),
      [pt(S('Knee or elbow or other correct'), 7)], 'bio-2-4', 'hinge-joints',
      SQ(29, 'Give one location in the human body where a hinge joint'), 7, stem=[Q17A]),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'Name one other type of synovial joint.'),
      [pt(S('Ball and socket'), 7)], 'bio-2-4', 'ball-and-socket', SQ(29, 'Name one other type of synovial joint.'), 7,
      stem=[Q17A]),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'The diagram shows a typical synovial joint.', 'ligament'),
      [pt(S('Ligament'), 7, label=S('D:')), pt(S('Cartilage'), 7, label=S('E:')),
       pt(S('Synovial fluid'), 7, label=S('F:'))], 'bio-2-4', 'parts-of-a-synovial-joint',
      SQ(29, 'Match the parts labelled D, E and F'), 21, stem=[Q17A], fig='q17-joint', id='bio-2023-ol-q17a-iv-fig',
      labels=[L('D', S('Ligament', page=29, after='Match the parts labelled D'), True),
              L('E', S('Cartilage', page=29, after='Match the parts labelled D'), True),
              L('F', S('Synovial fluid', page=29, after='Match the parts labelled D'), True)]),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'There are seven cervical vertebrae in the spine.', 'types of vertebrae.'),
      [anyn(S('Thoracic / lumbar / sacral / caudal (or coccyx)'), 2, 7)], 'bio-2-4', 'vertebrae',
      SQ(29, 'Name another two types of vertebrae.'), 14, stem=[Q17A], id='bio-2023-ol-q17a-v-vi',
      decision=bundled('(a)(v) and (vi)', '(v), and (vi) is added')),
    T('17avi', 'Q17(a)(vi)', 'C', _C(9, 'Name one disorder of the musculoskeletal system.'),
      [pt(S('Arthritis or osteoporosis or other correct'), 7)], 'bio-2-4', 'musculoskeletal-disorders',
      SQ(29, 'Name one disorder of the musculoskeletal system.'), 7, stem=[Q17A]),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'Explain in detail the term hormone.'),
      [pt(S('Chemical messenger'), 7), pt(S('Secreted into the bloodstream'), 7)], 'bio-2-4', 'hormone',
      SQ(30, 'Explain in detail the term hormone.'), 14, stem=[Q17B], id='bio-2023-ol-q17b-i'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Copy the table below into your answerbook and complete it.',
                                     'filled in as examples.'),
      [pt(S('Thyroid'), 7, label=S('Name of Gland')), pt(S('(Regulate)', 'metabolism'), 7, label=S('Function of Hormone')),
       pt(S('Adrenal'), 7, label=S('Name of Gland')), pt(S('Testosterone'), 7, label=S('Hormone')),
       pt(S('Sperm production'), 7, label=S('Function of Hormone'),
          note='The scheme\'s completed table is shown after reveal.')],
      'bio-2-4', 'glands-and-hormones', SQ(30, 'Complete the table:'), 35, stem=[Q17B], qfig='q17b-ii-question',
      fig='q17b-ii-scheme', id='bio-2023-ol-q17-b-ii',
      decision='The table\'s five empty cells are its responses, each row a cell headed by its printed column; '
               'the table is shown as the paper prints it and the scheme\'s completed table waits for the '
               'reveal.'),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'State two ways in which hormone action differs from nerve action.'),
      [anyn(S('Chemical is carried in blood / slow acting / long lasting'), 2, 7)], 'bio-2-4',
      'hormones-and-nerves', SQ(30, 'State two ways in which hormone action differs'), 14, stem=[Q17B],
      id='bio-2023-ol-q17b-iii-iv', decision=bundled('(b)(iii) and (iv)', '(iii), and (iv) is added')),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'Give one example of the use of hormone supplements.'),
      [pt(S('Hormone replacement therapy or other correct'), 7)], 'bio-2-4', 'hormone-supplements',
      SQ(30, 'Give one example of the use of hormone supplements.'), 7, stem=[Q17B]),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'To which kingdom does Rhizopus belong?'),
      [pt(S('Fungi'), 7)], 'bio-3-2', 'rhizopus-kingdom', SQ(31, 'To which kingdom does Rhizopus belong?'), 7,
      id='bio-2023-ol-q17c-i-iv', decision=bundled('(c)(i), (iii) and (iv)', '(i), and (iii), (iv) are added')),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'Draw a labelled diagram of Rhizopus.'),
      [pt(S('Sporangium and sporangiophore'), 7, kind='criterion', label=S('Diagram:')),
       pt(S('Any two correct labels'), 14, kind='criterion', units=[7, 7], label=S('Labels:'))], 'bio-3-2',
      'drawing-rhizopus', SQ(31, 'Draw a labelled diagram of Rhizopus.'), 21, id='bio-2023-ol-q17-c-ii'),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Name one food on which Rhizopus commonly grows.'),
      [pt(S('Bread'), 7)], 'bio-3-2', 'rhizopus-food', SQ(31, 'Name one food on which Rhizopus commonly grows.'), 7),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'In terms of nutrition, is Rhizopus a parasite or a saprophyte?',
                                     'Explain your answer.'),
      [pt(S('Saprophyte'), 7), pt(S('Lives or feeds on dead (organic) matter'), 7, label=S('Explain:'))], 'bio-3-2',
      'rhizopus-nutrition', SQ(31, 'In terms of nutrition, is Rhizopus a parasite'), 14),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'Rhizopus can undergo both sexual and asexual', 'reproduction in Rhizopus.'),
      [pt(S('Spores produced by sporangium and released'), 7),
       pt(S('Spores land on a suitable substrate and germinate'), 7)], 'bio-3-2', 'rhizopus-asexual-reproduction',
      SQ(31, 'Describe asexual reproduction in Rhizopus.'), 14, id='bio-2023-ol-q17c-v-vi',
      decision=bundled('(c)(v) and (vi)', '(v), and (vi) is added')),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'Yeast belong to the same kingdom as Rhizopus.', 'reproduction in yeast?'),
      [pt(S('Budding'), 7)], 'bio-3-2', 'budding', SQ(31, 'What term describe asexual reproduction in yeast?'), 7,
      fig='q17-yeast'),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'To which kingdom do bacteria belong?'),
      [pt(S('Monera'), 7)], 'bio-3-2', 'bacteria-kingdom', SQ(32, 'To which kingdom do bacteria belong?'), 7,
      id='bio-2023-ol-q17d-i-iv', decision=bundled('(d)(i), (iii) and (iv)', '(i), and (iii), (iv) are added')),
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'What shape of bacterium is shown?'),
      [pt(S('Spiral'), 7)], 'bio-3-2', 'bacterial-shape', SQ(32, 'What shape of bacteria is shown?'), 7,
      fig='q17-bacterium', id='bio-2023-ol-q17d-ii-fig'),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'Name the method by which bacteria', 'reproduce.'),
      [pt(S('Binary fission'), 7)], 'bio-3-2', 'binary-fission', SQ(32, 'Name the method by which bacteria reproduce.'),
      7),
    T('17div', 'Q17(d)(iv)', 'C', _C(10, 'In terms of nutrition, bacteria can be', 'Explain the underlined terms.'),
      [pt(S('Organism that makes its own food'), 7, label=S('Autotrophic:')),
       pt(S('Heterotrophic: Organism that takes in food'), 7)], 'bio-3-2', 'autotrophs-and-heterotrophs',
      SQ(32, 'Explain the underlined terms.'), 14, qfig='q17d-iv-question',
      decision='The paper marks the terms to explain by underlining them: the question is shown as the paper '
               'prints it.'),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Give one example of how bacteria can be useful to humans.'),
      [pt(S('Production of antibiotics or production of yoghurt', 'or other correct'), 7)], 'bio-3-2',
      'useful-bacteria', SQ(32, 'Give one example of how bacteria can be useful'), 7, id='bio-2023-ol-q17d-v-vi',
      decision=bundled('(d)(v) and (vi)1', '(v), and (vi) 1. and 2. are added')),
    T('17dvi1', 'Q17(d)(vi)1', 'C', _C(10, 'What are pathogenic bacteria?'),
      [pt(S('Disease causing (organisms)'), 7)], 'bio-3-2', 'pathogenic-bacteria',
      SQ(32, 'What are pathogenic bacteria?'), 7),
    T('17dvi2', 'Q17(d)(vi)2', 'C', _C(10, 'Give one example of a pathogenic bacterium.'),
      [pt(S('Named pathogenic bacterium (e.g. E. coli)'), 7, kind='criterion')], 'bio-3-2', 'a-pathogenic-bacterium',
      SQ(32, '2. Give one example of a pathogenic bacterium.'), 7,
      stem=[M('1.', 10), _C(10, 'What are pathogenic bacteria?')]),
    T('17dvii1', 'Q17(d)(vii)1', 'C', _C(10, 'What are antibiotics?'),
      [pt(S('chemicals (produced by bacteria to) to kill bacteria or fungi'), 7, label=S('Antibiotics:'))], 'bio-3-2',
      'antibiotics', SQ(32, 'What are antibiotics?'), 7, id='bio-2023-ol-q17d-vii',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('17dvii2', 'Q17(d)(vii)2', 'C', _C(10, 'Give one reason why is it important that antibiotics are not misused.'),
      [pt(S('can lead to antibiotic resistance or other correct reason'), 7, label=S('Misuse:'))], 'bio-3-2',
      'antibiotic-misuse', SQ(32, '2. Give one reason why it is important'), 7,
      stem=[M('1.', 10), _C(10, 'What are antibiotics?')]),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q4-equation': ('038', 5, (138, 110, 365, 136), SEC, ['X', 'Y'],
                    'The printed word equation: Glucose + X, an arrow, then Y + Water.', False),
    'q5-microscope': ('038', 6, (160, 75, 420, 365), SEC, ['A', 'B'],
                      'Drawing of a light microscope: arrow A points to the tube at the top where the eye looks in, '
                      'arrow B to one of the lenses on the turret above the stage, and a label Stage points to the '
                      'flat platform; a round light source sits on the base below the stage.', False),
    'q6-dna': ('038', 7, (384, 54, 541, 280), SEC, [],
               'Drawing of a DNA double helix: two twisted strands joined by rungs, with arrows from the label '
               'Nitrogenous base pairs pointing to two of the rungs.', False),
    'q7-neuron': ('038', 8, (88, 88, 508, 284), SEC, ['A', 'B', 'C'],
                  'Drawing of a neuron: a cell body with branching extensions on the left, arrow A pointing to one '
                  'of them, a long fibre running right, arrow B pointing to the fibre between two of the beads along '
                  'it and arrow C to one of the beads, and branching endings on the right. An empty box sits below '
                  'the fibre.', False),
    'q8-table': ('038', 9, (370, 213, 539, 297), SEC, [],
                 'Table of Presence (tick) / absence (cross) in five samples: Dandelion tick, cross, tick, cross, tick; '
                 'Grass tick, tick, tick, tick, tick.', False),
    'q10-table': ('038', 11, (143, 214, 470, 256), SEC, [],
                  'Data table of Number of colonies: May 5, September 14.', False),
    'q11-pyramids': ('040', 2, (120, 200, 522, 276), SEC, ['A', 'B'],
                     'Two pyramids of numbers. A: Grass on the bottom, a narrower Mouse box above, Hawk on top. B: '
                     'Bladderwrack on the bottom, a narrower Sea slug box above, Seagull on top.', False),
    'q12b-i-question': ('040', 3, (80, 122, 530, 292), SEC, [],
                        'The printed question: (b) In humans, the allele for brown eyes (B) is dominant to the allele '
                        'for blue eyes (b). The words allele and dominant are underlined. Below, drawings of a Blue '
                        'eye and a Brown eye, then (i) Explain the underlined terms.', False),
    'q13-leaf': ('040', 4, (376, 192, 541, 372), SEC, ['X'],
                 'Drawing of a cross section of a leaf: a row of tall, closely packed cells below the upper surface, '
                 'rounded cells with air spaces beneath, and a label Gas X in one of the air spaces near the lower '
                 'surface.', False),
    'q13c-i-question': ('040', 4, (80, 518, 470, 555), SEC, [],
                        'The printed question: (c) (i) Chemicals called enzymes are involved in metabolism within '
                        'cells. Explain the underlined terms. The words enzymes and metabolism are underlined.', False),
    'q13-immobilised': ('040', 4, (374, 556, 541, 675), SEC, [],
                        'Drawing of a beaker of liquid with small beads settled at the bottom, labelled Immobilised '
                        'enzymes.', False),
    'q14-female': ('040', 5, (322, 178, 541, 352), SEC, ['A', 'B', 'C'],
                   'Drawing of the female reproductive system, front view: arrow A points to the oval body at the end '
                   'of one tube, arrow B to one of the tubes leading from it, and arrow C to the central chamber.',
                   False),
    'q15-heart': ('040', 6, (318, 405, 541, 614), SEC, ['A', 'B', 'C'],
                  'Drawing of a section through the heart: A labels the large vessel arching from the top; B labels '
                  'the chamber with the thick wall on the lower right and C the chamber beside it; labels point to the '
                  'Semilunar valve, Bicuspid valve, Tricuspid valve, Vena cava and Septum.', False),
    'q16-kidney': ('040', 7, (372, 86, 541, 238), SEC, ['D', 'E', 'F'],
                   'Drawing of a section through a kidney: arrow D points to the outer layer, arrow E to one of the '
                   'cone-shaped regions inside it, arrow F to the central space, and a label Ureter points to the tube '
                   'leaving it.', False),
    'q16-eye': ('040', 7, (312, 430, 541, 596), SEC, ['X', 'Y', 'Z', 'd'],
                'Drawing of a section through the eye: arrow X points to the coloured ring at the front, arrow Y to '
                'the clear curved layer covering the front, arrow Z to the oval body behind the opening, and a '
                'double-headed arrow d spans the opening; labels point to the Retina and the Optic nerve at the '
                'back.', False),
    'q16-root': ('040', 8, (338, 55, 545, 182), SEC, ['A', 'B', 'C'],
                 'Drawing of a transverse section of a root: a bracket A spans the cross-shaped core, arrow B points '
                 'to the tissue filling the circle, arrow C to the thin outer layer, and a label Root hair points to '
                 'a fine hair growing from the edge.', False),
    'q16-flower': ('040', 8, (312, 360, 541, 578), SEC, ['X', 'Y', 'Z'],
                   'Drawing of an animal-pollinated flower cut in half: arrow X points to the top of the central '
                   'stalk, arrow Y to a small body inside the swollen base, arrow Z to a small leaf-like part below '
                   'the petals, and a label Anther points to the head of one of the stalks around the centre.',
                   False),
    'q17-joint': ('040', 9, (366, 88, 541, 268), SEC, ['D', 'E', 'F'],
                  'Drawing of a synovial joint between two bones: arrow D points to the band on the outside joining '
                  'the bones, arrow E to the smooth layer capping the end of a bone, and arrow F to the space between '
                  'the bone ends.', False),
    'q17b-ii-question': ('040', 9, (108, 430, 541, 622), SEC, [],
                         'The printed question: (ii) Copy the table below into your answerbook and complete it. Some '
                         'boxes have been filled in as examples. A table with columns Name of gland, Hormone and '
                         'Function of hormone: row 1 gives the hormone Thyroxine; row 2 gives the hormone Adrenaline '
                         'and its function, To prepare the body for "fight or flight"; row 3 gives the gland Testes. '
                         'The other cells are empty.', False),
    'q17b-ii-scheme': ('scheme', 30, (134, 175, 458, 304), SEC, [],
                       "The marking scheme's completed table: Thyroid, Thyroxine, (Regulate) metabolism; Adrenal, "
                       'Adrenaline, To prepare the body for "fight or flight"; Testes, Testosterone, Sperm production. '
                       'The cells the paper filled in are shaded.', True),
    'q17-yeast': ('040', 10, (434, 154, 541, 287), SEC, [],
                  'Electron micrograph of a round yeast cell with a smaller round bud growing from its top.', False),
    'q17-bacterium': ('040', 10, (354, 341, 541, 465), SEC, [],
                      'Micrograph of a long, thin, wavy bacterium.', False),
    'q17d-iv-question': ('040', 10, (108, 427, 330, 479), SEC, [],
                         'The printed question: (iv) In terms of nutrition, bacteria can be either autotrophic or '
                         'heterotrophic. Explain the underlined terms. The words autotrophic and heterotrophic are '
                         'underlined.', False),
}
