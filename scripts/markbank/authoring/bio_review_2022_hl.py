"""Biology 2022 Higher Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-12), every page rendered and read:
  * LC025ALP038EV (Sections A and B and Answerbook), 40 pages: p1 cover
    (with the note that the 2022 papers were adjusted for disruption to
    learning), p2 instructions, p3-p9 Section A Questions 1-7, p10-p12
    Section B Questions 8-10, p13 Section C answerbook instructions,
    p14-p15 graph paper, p16-p39 ruled answer pages, p40 back cover. No
    acknowledgements page.
  * LC025ALP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "Do not hand this question paper up", p12 back cover.
  * LC025ALP000EV (marking scheme), 32 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7-p29 Questions
    1-17, p30-p31 "BLANK PAGE", p32 back cover.

The 2022 papers set fewer questions to answer: any four of Section A, any one
of Section B and any three of Section C. Every printed question is carded.

The sitting was already carded (144 authored cards, 142 shipped). As for the
later sittings, every task is re-derived from the PDFs at the scheme's own
mark boundaries and the existing cards are corrected in place: every shipped
id is kept, mapped (`id=`) to the task it was carding, verified or corrected
with its old fields recorded; tasks the old cards bundled or missed are
added. Two authored cards that never shipped are withdrawn:
bio-2022-hl-q17-d-ii (half of Q17(d)(ii), which bio-2022-hl-q17-d-ii-fig
carries whole) and bio-2022-hl-q16-b-iii-fig (a figure twin of
bio-2022-hl-q16-b-iii).

Section A: Q1 is the best five of six parts at 4 ("5(4)"); Q2-Q7 are each
"6(3) + 2" over seven responses, an ordered split carded at 3 a response.
Sections B and C print a mark per row.

Printed choices the scheme marks differently per option are split into
routes: Q16(a)(vi) paralysis or Parkinson's disease, Q16(b)(v) long
sightedness or short sightedness or a hearing defect, Q16(c)(vii) arthritis
or osteoporosis, Q17(d)(vii) smoking or exercise. Q11(c)(ii) ("either of the
factors you named") is marked on one row and is one card.
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2022, 'hl'
REVIEWED_AT = '2026-10-12'
BASELINE_COMMIT = 'a9e7a9861'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2022-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': 'a8b64511a0818f10d514a481394d096c18b1b0a03f1fbd66d186e40f2cc3dc34',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2022-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': '12994344215696d8a262bb959948d90994a562ba3f425f8535d8df49fe0a490a',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2022-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': 'df45e49a3932ddda99320b313cfdf714ada48f250c0e7804006c0753af8c3a38',
               'pages': 32},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 13)},
            13: 'answerbook-instructions', 14: 'graph-paper', 15: 'graph-paper',
            **{p: 'answer-pages' for p in range(16, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', **{p: 'marking' for p in range(7, 30)},
               30: 'blank', 31: 'blank', 32: 'back-cover'},
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
BEST_OF = {1: (5, 4)}
LADDERS = {q: {'steps': [3, 3, 3, 3, 3, 3, 2], 'notation': '6(3) + 2'} for q in range(2, 8)}

CHECKSUMS = {
    1: {4: 6},   # printed "5(4)": the best five of the six 4-mark parts carded here
    **{q: {3: 7} for q in range(2, 8)},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in (11, 12, 14, 15)}, (13, 'a'): {3: 2, 1: 3},
    (11, 'b'): {3: 8, 1: 3}, (12, 'b'): {3: 9}, (13, 'b'): {3: 9}, (14, 'b'): {3: 9}, (15, 'b'): {3: 8, 1: 3},
    (11, 'c'): {3: 8}, (12, 'c'): {3: 8}, (13, 'c'): {3: 8}, (14, 'c'): {3: 7, 1: 3}, (15, 'c'): {3: 7, 1: 3},
    (16, 'a'): {3: 9, 1: 3}, (16, 'b'): {3: 9, 1: 3}, (16, 'c'): {3: 10}, (16, 'd'): {3: 10},
    **{(17, x): {3: 10} for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 13), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any four', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any one', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any three', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any four', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the best five make 20.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 3, 'any one', 'Q1(d) "any one fibrous protein": open single answer; one card.'),
    ('038', 4, 'the following', 'Q2: every term explained, one card each.'),
    ('038', 5, 'or', 'Q3(b) "a female or a male": the answer options.'),
    ('038', 5, 'or', 'Q3(f) "application (or use)": rewording.'),
    ('038', 7, 'the following', 'Q5 lead-in: every statement asked.'),
    ('038', 7, 'or', 'Q5 "true or false": the answer options.'),
    ('038', 8, 'both', 'Q6 "both lipase and bile salts": description.'),
    ('038', 10, 'any one', 'Section B rubric repeated.'),
    ('038', 10, 'the following', 'Q8(b) "the following images": a figure reference.'),
    ('038', 10, 'or', 'Q8(b)(i) "A or B": the answer options.'),
    ('038', 11, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('038', 11, 'or', 'Q9(b) "light intensity or carbon dioxide": the student\'s practical, one set of rows; '
                      'one card per part.'),
    ('038', 11, 'or', 'Q9(b)(vi) axis label "Light intensity or CO2 concentration": figure text.'),
    ('038', 12, 'the following', 'Q10(b) lead-in: every part asked.'),
    ('038', 12, 'any one', 'Q10(b)(iv) "any one result": open single answer; one card.'),
    ('040', 2, 'any three', 'Section C rubric repeated.'),
    ('040', 2, 'any two', 'Q11(b)(iii)1 "any two examples": both required, one row at 2(3); one card.'),
    ('040', 2, 'or', 'Q11(c) "batch or continuous flow": description.'),
    ('040', 2, 'either', 'Q11(c)(ii) "either of the factors you named": one matching-explanation row; one card.'),
    ('040', 3, 'the following', 'Q12(a): three terms in one ask, a row each; one card.'),
    ('040', 3, 'the following', 'Q12(b) "the following passage": a reference.'),
    ('040', 3, 'the following', 'Q12(b)(v): each effect asked, one card per item.'),
    ('040', 3, 'or', 'Q12(c)(iv) "agriculture or fisheries or forestry": one open row; one card.'),
    ('040', 3, 'or', 'Q12(c)(iv), same choice.'),
    ('040', 3, 'or', 'Q12(c)(v) "global warming or pollution": exclusion, not a choice.'),
    ('040', 4, 'any one', 'Q13(a) "any one nucleotide": open single answer; one card.'),
    ('040', 4, 'both', 'Q13(c) "homozygous dominant for both": description.'),
    ('040', 4, 'both', 'Q13(c) "homozygous recessive for both": description.'),
    ('040', 4, 'or', 'Q13(c)(iii) "a Punnet square, or otherwise": method, not a choice of task.'),
    ('040', 6, 'or', 'Q15(b)(iii) "by name or label": either form; one answer.'),
    ('040', 6, 'the following', 'Q15(c)(ii): every tissue labelled; one card.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q16(a)(ii): every part labelled; one card.'),
    ('040', 7, 'either', 'Q16(a)(vi) "either paralysis or Parkinson\'s disease": separate causes per option: ROUTES.'),
    ('040', 7, 'or', 'Q16(a)(vi), same choice.'),
    ('040', 7, 'one of the following', 'Q16(b)(v) long or short sightedness or a hearing defect: separate '
                                       'corrections per option: ROUTES.'),
    ('040', 7, 'or', 'Q16(b)(v), same choice.'),
    ('040', 7, 'or', 'Q16(b)(v), same choice.'),
    ('040', 8, 'either', 'Q16(c)(vii) "either arthritis or osteoporosis": separate causes per option: ROUTES.'),
    ('040', 8, 'or', 'Q16(c)(vii), same choice.'),
    ('040', 8, 'the following', 'Q16(d) lead-in: every part asked.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'the following', 'Q17(b) lead-in: every part asked.'),
    ('040', 10, 'the following', 'Q17(c) lead-in: every part asked.'),
    ('040', 10, 'the following', 'Q17(c)(vi): each process asked, one card per item.'),
    ('040', 10, 'or', 'Q17(d)(ii) "X or Y or Z": the answer options.'),
    ('040', 10, 'or', 'Q17(d)(ii), same options.'),
    ('040', 10, 'either', 'Q17(d)(vii) "either one of the following: smoking or exercise": separate effects per '
                          'option: ROUTES.'),
    ('040', 10, 'one of the following', 'Q17(d)(vii), same choice.'),
    ('040', 10, 'or', 'Q17(d)(vii), same choice.'),
]

ROUTES = {
    'Q16(a)(vi)': ['paralysis', 'parkinsons-disease'],
    'Q16(b)(v)': ['long-sightedness', 'short-sightedness', 'hearing-defect'],
    'Q16(c)(vii)': ['arthritis', 'osteoporosis'],
    'Q17(d)(vii)': ['smoking', 'exercise'],
}

LAYOUT_CHECKS = [
    ('scheme', 22, 'Injury (damage) to spinal cord', ['Paralysis:', 'Parkinson’s disease:'], 'Paralysis:'),
    ('scheme', 22, 'Decrease in dopamine levels', ['Paralysis:', 'Parkinson’s disease:'], 'Parkinson’s disease:'),
    ('scheme', 23, 'Convex lens', ['Long sightedness:', 'Short sightedness:', 'Hearing defect:'], 'Long sightedness:'),
    ('scheme', 23, 'Concave lens', ['Long sightedness:', 'Short sightedness:', 'Hearing defect:'],
     'Short sightedness:'),
    ('scheme', 24, 'Wear and tear (or injury)', ['Arthritis:', 'Osteoporosis:'], 'Arthritis:'),
    ('scheme', 24, 'Hormonal', ['Arthritis:', 'Osteoporosis:'], 'Osteoporosis:'),
    ('scheme', 29, 'increase blood', ['Smoking', 'Exercise'], 'Smoking'),
    ('scheme', 29, 'heart muscle', ['Smoking', 'Exercise'], 'Exercise'),
]

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2022-hl-q17-d-ii': 'Never shipped: the explanation half of Q17(d)(ii), which bio-2022-hl-q17-d-ii-fig '
                            'carries whole with its diagram.',
    'bio-2022-hl-q16-b-iii-fig': 'Never shipped: a figure twin of bio-2022-hl-q16-b-iii, which carries the '
                                 'reviewed task and its figure.',
}
WITHDRAW = {'bio-2022-hl-q17-d-ii': ('bio-2022-hl-q17-d-ii-fig', RETAINED['bio-2022-hl-q17-d-ii']),
            'bio-2022-hl-q16-b-iii-fig': ('bio-2022-hl-q16-b-iii', RETAINED['bio-2022-hl-q16-b-iii-fig'])}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list ("1." on its own line, its item on the next)."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


def tick(clip, answer):
    return G('tick-col', page=9, clip=clip, headers=['True', 'False'], expect=answer, marks=3)


def bundled(parts, keep):
    return f'The old card bundled {parts}; it keeps its id for {keep}.'


EACH_ITEM = '"Each of the following": separately priced items, one card each.'

Q1 = _A(3, 'Answer any five of the following parts (a) to (f):')
Q2 = _A(4, 'Write a brief sentence explaining each of the following terms.')
Q3 = _A(5, 'Study the image below which shows a set of human chromosomes', 'Down’s syndrome.')
Q4 = _A(6, 'The image shows a transverse section through a mitochondrion', 'transmission electron microscope.')
Q4C = _A(6, 'Aerobic respiration involves two stages.')
Q5 = _A(7, 'Indicate whether the following statements are true or false', 'appropriate box in each case.')
Q6 = _A(8, 'A student carried out an experiment comparing the action of lipase', 'experimental results.')
Q7 = _A(9, 'The diagram below shows the structure of a typical virus', 'COVID-19 in humans.')
Q8B = _A(10, 'A student observed the following images', 'image B at x100.')
Q8BIV = _A(10, 'When examining cells with a microscope:')
Q9B = _A(11, 'Answer the following questions based on an activity', 'rate of photosynthesis.')
Q10B = _A(12, 'Answer the following questions based on an investigation', 'on a plant tissue.')
Q11B3 = _C(2, 'Harmful bacteria can cause disease in humans.')
Q11C = [_C(2, 'Food processing is carried out in a bioreactor', 'and some fungi.'),
        _C(2, 'It can be carried out as batch or continuous flow food processing.')]
Q12B = [_C(3, 'Read the following passage and answer the questions that follow.'),
        _C(3, 'Dragonflies are a deadly group of Irish predators.', 'compound eyes.'),
        _C(3, 'Dragonflies hunt close to river banks', 'survey their habitats.'),
        _C(3, '(Adapted from “Irish dragonflies: supreme killing machines”', '5 September 2019)')]
Q12C = [_C(3, 'Global warming is occurring at an unprecented rate.'),
        _C(3, 'This is as a result of pollution of the atmosphere with greenhouse gases.')]
Q13B = _C(4, 'The diagram illustrates some of the events of protein synthesis.')
Q13C = _C(4, 'In squash plants, the allele for white fruit (F) is dominant', 'homozygous recessive for both.')
Q14B = _C(5, 'The process of photosynthesis occurs over two stages as shown below.',
          'Study the diagram carefully and answer the questions that follow.')
Q14C = _C(5, 'Interphase and mitosis occur during the cell cycle.', 'telophase).')
Q15B = _C(6, 'The diagrams below are of a human kidney and one of its nephrons.', 'distal convoluted tubule)')
Q15C = _C(6, 'Plants require water for survival.')
Q16A1 = _C(7, 'The human nervous system is divided into two parts.')
Q16B = _C(7, 'The diagram shows the internal structure of the human eye.')
Q16C = _C(8, 'A joint in the human skeleton is where two bones meet.', 'A synovial joint is shown in the diagram.')
Q16D = _C(8, 'Answer the following questions from your knowledge of sexual reproduction', 'flowering plants.')
Q17A = [_C(9, 'The photographs are of the two scientists', 'natural selecton is:'),
        _C(9, 'There is variation among members of a', 'these variations are inherited.'),
        _C(9, 'Variations are differences among members of the same species.', 'contribute to these variations.')]
Q17B = _C(9, 'Answer the following questions based on human reproduction.')
Q17C = _C(10, 'Answer the following questions from your knowledge of reproduction in flowering', 'plants.')
Q17D = _C(10, 'Diagrams X, Y and Z below show the heart during periods', 'answer the questions that follow.')

L_KIDNEY = [L('A', S('*Cortex', page=20), False), L('B', S('*Medulla (pyramid)', page=20), False),
            L('C', S('*Pelvis', page=20), False)]
L_EYE = [L('P', S('*Lens', page=23), False), L('Q', S('*Cornea', page=23), False),
         L('R', S('*Optic nerve', page=23), False)]
L_JOINT = [L('A', S('*Ligament', page=24), False), L('B', S('*Cartilage', page=24), False)]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Name the four elements found in all proteins.'),
      [pt(S('Carbon (C), Hydrogen (H), Oxygen (O), Nitrogen (N)'), 4, kind='allOf')], 'bio-1-2',
      'elements-in-proteins', SQ(7, 'Name the four elements found in all proteins.'), 4, stem=[Q1],
      id='bio-2022-hl-q1-a', decision='One 4-mark line naming all four elements: one all-of row.'),
    T('1b', 'Q1(b)', 'A', _A(3, 'Name an element that is only sometimes found in proteins.'),
      [pt(S('Phosphorous (P) or Sulfur (S)'), 4)], 'bio-1-2', 'sometimes-in-proteins',
      SQ(7, 'Name an element that is only sometimes found in proteins.'), 4, stem=[Q1], id='bio-2022-hl-q1-b'),
    T('1c', 'Q1(c)', 'A', _A(3, 'How many common amino acids are found in proteins?'),
      [pt(S('Twenty (20)'), 4)], 'bio-1-2', 'amino-acid-count', SQ(7, 'How many common amino acids'), 4,
      stem=[Q1], id='bio-2022-hl-q1-c'),
    T('1d', 'Q1(d)', 'A', _A(3, 'Fibrous proteins have structural roles in living organisms.', 'fibrous protein.'),
      [pt(S('Keratin or myosin or collagen or any other valid example'), 4)], 'bio-1-2', 'fibrous-proteins',
      SQ(7, 'Name any one fibrous protein.'), 4, stem=[Q1], id='bio-2022-hl-q1-d'),
    T('1e', 'Q1(e)', 'A', _A(3, 'Give one metabolic role of proteins in living organisms.'),
      [pt(S('Enzymes or hormones or antibodies or any other valid example or any role described'), 4)],
      'bio-1-2', 'metabolic-role-of-protein', SQ(7, 'Give one metabolic role of proteins.'), 4, stem=[Q1],
      id='bio-2022-hl-q1-e'),
    T('1f', 'Q1(f)', 'A', _A(3, 'Give one good source of protein in the diet.'),
      [pt(S('Meat or fish or chicken or nuts or lentils', 'any other valid example'), 4)], 'bio-1-2',
      'dietary-protein', SQ(7, 'Give one good source of protein in the diet.'), 4, stem=[Q1], id='bio-2022-hl-q1-f'),
] + [
    T(f'2{x}', f'Q2({x})', 'A', [Q2, _A(4, term, br=True)], [pt(S(ans, aend), 3)], topic, concept,
      SQ(7, term, after='Question 2'), 3, id=f'bio-2022-hl-q2-{x}')
    for x, term, ans, aend, topic, concept in [
        ('a', 'Ecology', 'The study of the (interactions between) organisms', None, 'bio-3-1', 'ecology'),
        ('b', 'Food chain', 'Sequence of organisms showing transfer of energy', None, 'bio-3-1', 'food-chain'),
        ('c', 'Edaphic factor', '(Factor relating to) soil', None, 'bio-3-1', 'edaphic-factor'),
        ('d', 'Quantitative study', 'Measuring the amount (or number) of organisms.', None, 'bio-3-1',
         'quantitative-study'),
        ('e', 'Omnivore', '(Organism that) eats plants and animals', None, 'bio-3-1', 'omnivore'),
        ('f', 'Contest competition', 'Struggle for a resource (in short supply)', None, 'bio-3-1',
         'contest-competition'),
        ('g', 'Nitrogen fixation', '(Conversion of atmospheric) nitrogen', None, 'bio-3-2', 'nitrogen-fixation')]
] + [
    T('3a', 'Q3(a)', 'A', _A(5, 'Name the two chemical components that make up chromosomes.'),
      [pt(S('DNA'), 3), pt(S('Protein'), 3)], 'bio-1-4', 'chromosome-composition',
      SQ(8, 'Name the two chemical components'), 6, stem=[Q3], fig='q3-karyotype', id='bio-2022-hl-q3-a'),
    T('3b', 'Q3(b)', 'A', _A(5, 'Is the karyotype shown above from a female or a male?'),
      [pt(S('Female'), 3)], 'bio-1-4', 'karyotype-sex', SQ(8, 'Is the karyotype shown above'), 3, stem=[Q3],
      fig='q3-karyotype', id='bio-2022-hl-q3-bc-fig',
      decision=bundled('(b) and (c)', '(b), and (c) is added')),
    T('3c', 'Q3(c)', 'A', _A(5, 'Justify the answer you have given at part (b) above.'),
      [pt(S('Has two X chromosomes or no Y chromosome'), 3)], 'bio-1-4', 'two-x-chromosomes',
      SQ(8, 'Justify the answer you have given'), 3,
      stem=[Q3, M('(b)', 5), _A(5, 'Is the karyotype shown above from a female or a male?')], fig='q3-karyotype'),
    T('3d', 'Q3(d)', 'A', _A(5, 'What evidence is shown in the karyotype that this person', 'Down’s syndrome?'),
      [pt(S('There is an extra chromosome present', 'copies of one of the chromosomes.'), 3)], 'bio-2-3',
      'downs-syndrome-evidence', SQ(8, 'What evidence is shown in the karyotype'), 3, stem=[Q3],
      fig='q3-karyotype', id='bio-2022-hl-q3-d-fig'),
    T('3e', 'Q3(e)', 'A', _A(5, 'Sickle-cell anaemia is a condition caused', 'Name this other type of mutation.'),
      [pt(S('Gene or point (mutation)'), 3)], 'bio-2-3', 'gene-mutation', SQ(8, 'Name this other type of mutation.'),
      3, stem=[Q3], fig='q3-karyotype', id='bio-2022-hl-q3-e'),
    T('3f', 'Q3(f)', 'A', _A(5, 'Scientific analysis of chromosome karyotypes', 'application (or use) of tissue culture.'),
      [pt(S('Cancer research or plant breeding', 'any valid example.'), 3)], 'bio-1-3', 'tissue-culture-uses',
      SQ(8, 'Give one other application of tissue culture'), 3, stem=[Q3], fig='q3-karyotype',
      id='bio-2022-hl-q3-f'),
    T('4a', 'Q4(a)', 'A', _A(6, 'Explain why the image above cannot be produced using a light microscope.'),
      [pt(S('(Mitochondria) are too small', 'light microscope).'), 3)], 'bio-1-3', 'electron-microscope-images',
      SQ(8, 'Explain why the image cannot be produced'), 3, stem=[Q4], fig='q4-mitochondrion',
      id='bio-2022-hl-q4-a-fig'),
    T('4b', 'Q4(b)', 'A', _A(6, 'Name one type of animal cell that does not have mitochondria.'),
      [pt(S('Red blood cell (or erythrocyte)'), 3)], 'bio-1-3', 'cells-without-mitochondria',
      SQ(8, 'Name one type of animal cell'), 3, stem=[Q4], fig='q4-mitochondrion', id='bio-2022-hl-q4-b'),
    T('4ci', 'Q4(c)(i)', 'A', _A(6, 'Name and give the location of the stage', 'mitochondrion.'),
      [pt(S('Glycolysis'), 3, label=S('Name:')), pt(S('Location: Cytosol (accept cytoplasm)'), 3)], 'bio-2-2',
      'glycolysis', SQ(8, 'Name and give the location of the stage'), 6, stem=[Q4, Q4C], fig='q4-mitochondrion',
      id='bio-2022-hl-q4-c-i'),
    T('4cii', 'Q4(c)(ii)', 'A', _A(6, 'Name the series of chemical reactions, involving acetyl', 'mitochondrion.'),
      [pt(S('Krebs’ cycle'), 3)], 'bio-2-2', 'krebs-cycle', SQ(8, 'Name the series of chemical reactions'), 3,
      stem=[Q4, Q4C], fig='q4-mitochondrion', id='bio-2022-hl-q4-c-ii'),
    T('4ciii', 'Q4(c)(iii)', 'A', _A(6, 'State the number of carbon atoms in a molecule of acetyl Co. A.'),
      [pt(S('Two (2)'), 3)], 'bio-2-2', 'acetyl-coa', SQ(8, 'State the number of carbon atoms'), 3,
      stem=[Q4, Q4C], fig='q4-mitochondrion', id='bio-2022-hl-q4-c-iii'),
    T('4d', 'Q4(d)', 'A', _A(6, 'Sometimes lactic acid is produced during respiration.', 'this may occur.'),
      [pt(S('Anaerobic (conditions) or oxygen deficiency or described'), 3)], 'bio-2-2', 'lactic-acid-conditions',
      SQ(8, 'Sometimes lactic acid is produced'), 3, stem=[Q4], fig='q4-mitochondrion', id='bio-2022-hl-q4-d'),
] + [
    T(f'5{x}', f'Q5({x})', 'A', _A(7, start), [tick(clip, answer)], topic, concept, SQ(9, sq), 3,
      stem=[Q5], id=f'bio-2022-hl-q5-{x}')
    for x, start, sq, clip, answer, topic, concept in [
        ('a', 'Copper (Cu) is one of the common elements present in food.', 'Copper (Cu) is one of the common',
         (55, 104, 560, 131), 'False', 'bio-1-2', 'elements-in-food'),
        ('b', 'Response is a characteristic of life.', 'Response is a characteristic of life.', (55, 131, 560, 156),
         'True', 'bio-1-1', 'characteristics-of-life'),
        ('c', 'An animal cell will burst if placed in a concentrated sugar solution.', 'An animal cell will burst',
         (55, 156, 560, 182), 'False', 'bio-2-6', 'animal-cell-in-concentrated-solution'),
        ('d', 'Macrophages are white blood cells that secrete perforin.', 'Macrophages are white blood cells',
         (55, 182, 560, 208), 'False', 'bio-2-4', 'macrophages'),
        ('e', 'Organs are groups of tissues with a shared function.', 'Organs are groups of tissues',
         (55, 208, 560, 233), 'True', 'bio-1-3', 'organs'),
        ('f', 'Ethene is used to ripen fruit.', 'Ethene is used to ripen fruit.', (55, 233, 560, 258), 'True',
         'bio-2-4', 'ethene'),
        ('g', 'All members of Kingdom Fungi are heterotrophic.', 'All members of the Kingdom Fungi',
         (55, 258, 560, 286), 'True', 'bio-3-2', 'fungi-are-heterotrophic')]
] + [
    T('6a', 'Q6(a)', 'A', _A(8, 'What conclusion could the student make about lipid digestion', 'results shown above?'),
      [pt(S('(Lipid digestion) is faster (higher rate)', 'with lipase alone.'), 3)], 'bio-2-6',
      'bile-speeds-lipid-digestion', SQ(9, 'What conclusion could the student make'), 3, stem=[Q6], fig='q6-graph',
      id='bio-2022-hl-q6-a'),
    T('6b', 'Q6(b)', 'A', _A(8, 'Name the two products of complete lipid digestion by lipase.'),
      [pt(S('Fatty acids'), 3), pt(S('Glycerol'), 3)], 'bio-2-6', 'products-of-lipid-digestion',
      SQ(9, 'Name the two products of complete lipid digestion'), 6, stem=[Q6], fig='q6-graph', id='bio-2022-hl-q6-b'),
    T('6c', 'Q6(c)', 'A', _A(8, 'Name a location in the digestive system where lipase digests lipids.'),
      [pt(S('Duodenum (accept jejunum or ileum or small intestine or stomach)'), 3)], 'bio-2-6',
      'where-lipase-works', SQ(9, 'Name a location in the digestive system'), 3, stem=[Q6], fig='q6-graph',
      id='bio-2022-hl-q6-c'),
    T('6d', 'Q6(d)', 'A', _A(8, 'Suggest an optimum pH for digestion of lipids in the location', 'above.'),
      [pt(S('7-9 (matched to small intestine)'), 3, note_sel=S('(accept in range of 1-5 matched to stomach)'))],
      'bio-2-6', 'lipase-optimum-ph', SQ(9, 'Suggest an optimum pH for digestion of lipids'), 3,
      stem=[Q6, M('(c)', 8), _A(8, 'Name a location in the digestive system where lipase digests lipids.')],
      fig='q6-graph', id='bio-2022-hl-q6-d'),
    T('6e', 'Q6(e)', 'A', _A(8, 'Describe the action of bile salts on lipids.'),
      [pt(S('Emulsifies (or described) or increases surface area'), 3)], 'bio-2-6', 'bile-salts',
      SQ(9, 'Describe the action of bile on lipids.'), 3, stem=[Q6], fig='q6-graph', id='bio-2022-hl-q6-e'),
    T('6f', 'Q6(f)', 'A', _A(8, 'Villi are microscopic structures in the digestive system', 'products of lipid digestion.'),
      [pt(S('Lacteal'), 3)], 'bio-2-6', 'lacteal', SQ(9, 'Name the structure inside each villus'), 3,
      id='bio-2022-hl-q6-f'),
    T('7a', 'Q7(a)', 'A', _A(9, 'Name molecule A.'),
      [pt(S('Nucleic acid or RNA or DNA'), 3)], 'bio-1-1', 'viral-nucleic-acid', SQ(10, 'Name molecule A.'), 3,
      stem=[Q7], fig='q7-virus', id='bio-2022-hl-q7-a-fig'),
    T('7b', 'Q7(b)', 'A', _A(9, 'Antigens are present in viruses.', 'location of an antigen.'),
      [pt(S('Correct arrow'), 3, kind='criterion')], 'bio-1-1', 'viral-antigens',
      SQ(10, 'Draw an arrow from'), 3, stem=[Q7], fig='q7-virus'),
    T('7c', 'Q7(c)', 'A', _A(9, 'Explain why viruses are described as obligate parasites.'),
      [pt(S('Need a host to replicate (or reproduce) or cannot replicate by themselves'), 3)], 'bio-1-1',
      'obligate-parasites', SQ(10, 'Explain why viruses are described as obligate parasites.'), 3, stem=[Q7],
      fig='q7-virus', id='bio-2022-hl-q7-c'),
    T('7d', 'Q7(d)', 'A', _A(9, 'Vaccination has proved to be very effective', 'the term vaccination.'),
      [pt(S('Administration of a non-disease-causing', 'or described'), 3, label=S('What it is:')),
       pt(S('What it does: Stimulates production of antibodies', 'memory cells'), 3)], 'bio-2-4', 'vaccination',
      SQ(10, 'Explain in detail what is meant by the term vaccination.'), 6, stem=[Q7], fig='q7-virus',
      id='bio-2022-hl-q7-d'),
    T('7e', 'Q7(e)', 'A', _A(9, 'Name one harmful virus, other than SARS-CoV-2 (coronavirus).'),
      [pt(S('Any valid harmful virus.'), 3, kind='criterion')], 'bio-1-1', 'harmful-viruses',
      SQ(10, 'Name one harmful virus other than SARS-CoV-2.'), 3, stem=[Q7], fig='q7-virus'),
    T('7f', 'Q7(f)', 'A', _A(9, 'Give one example of a beneficial application of a virus.'),
      [pt(S('Genetic engineering (vector) or treat bacterial infection', 'valid answer'), 3)], 'bio-1-1',
      'beneficial-viruses', SQ(10, 'Give one example of a beneficial application of a virus.'), 3, stem=[Q7],
      fig='q7-virus', id='bio-2022-hl-q7-f'),
    # ------------------------------------------------------------ Section B --
    T('8a', 'Q8(a)', 'B', _A(10, 'Distinguish clearly between a eukaryotic cell and a prokaryotic cell', 'sentence on each.'),
      [pt(S('Contains a nucleus or organelles enclosed by membranes'), 3, label=S('Eukaryotic:')),
       pt(S('Does not contain a nucleus or does not contain organelles enclosed by membranes'), 3,
          label=S('Prokaryotic:'))], 'bio-1-3', 'eukaryotic-and-prokaryotic',
      SQ(11, 'Distinguish between:'), 6, id='bio-2022-hl-q8-a'),
    T('8bi', 'Q8(b)(i)', 'B', _A(10, 'Which image, A or B, represents plant tissue?'),
      [pt(S('*B'), 3)], 'bio-1-3', 'plant-tissue-image', SQ(11, 'Which image, A or B, represents a plant tissue?'), 3,
      stem=[Q8B], fig='q8-cells'),
    T('8bii', 'Q8(b)(ii)', 'B', _A(10, 'Give a reason for your answer at part (b) (i) above.'),
      [pt(S('Cell wall present or comment on shape of cells', 'valid comment'), 3)], 'bio-1-3',
      'recognising-plant-cells', SQ(11, 'Give a reason for your answer at part (b) (i) above.'), 3,
      stem=[Q8B, M('(i)', 10), _A(10, 'Which image, A or B, represents plant tissue?')], fig='q8-cells',
      id='bio-2022-hl-q8-b-ii'),
    T('8biii', 'Q8(b)(iii)', 'B', _A(10, 'Identify structure Z.'),
      [pt(S('*Nucleus'), 3)], 'bio-1-3', 'nucleus', SQ(11, 'Identify structure Z.'), 3, stem=[Q8B], fig='q8-cells'),
    T('8biv1', 'Q8(b)(iv)1', 'B', _A(10, 'Name a stain that can be used.'),
      [pt(S('Methylene blue or iodine or other correct example'), 3)], 'bio-1-3', 'stains',
      SQ(11, '1. Name a stain you used.'), 3, stem=[Q8B, Q8BIV], id='bio-2022-hl-q8-b-iv',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added.'),
    T('8biv2', 'Q8(b)(iv)2', 'B', _A(10, 'Give one benefit of using a stain.'),
      [pt(S('Make (cells) more visible or (make cells) easier to see'), 3)], 'bio-1-3', 'why-stain',
      SQ(11, '2. Give one benefit of using a stain.'), 3,
      stem=[Q8B, Q8BIV, M('1.', 10), _A(10, 'Name a stain that can be used.')]),
    T('8bv', 'Q8(b)(v)', 'B', _A(10, 'The image of the cell in A was 2 cm wide.', 'width of this cell?'),
      [pt(S('0.005 (cm) or 2/400 (cm) or 1/200 (cm)', 'correct)'), 3)], 'bio-1-3', 'actual-size',
      SQ(11, 'The image of the cell in A was 2 cm wide.'), 3, stem=[Q8B], fig='q8-cells', id='bio-2022-hl-q8-b-v'),
    T('8bvi', 'Q8(b)(vi)', 'B', _A(10, 'Image B shows cells at x100.', 'view these cells at x400.'),
      [pt(S('Select (or use) high power or select (or use) x40 (objective lens)'), 3), pt(S('Use fine focus'), 3)],
      'bio-1-3', 'changing-magnification', SQ(11, 'Image B shows cells at x100.'), 6, stem=[Q8B], fig='q8-cells',
      id='bio-2022-hl-q8-b-vi'),
    T('9ai', 'Q9(a)(i)', 'B', _A(11, 'What is meant by the term autotrophic?'),
      [pt(S('(An organism that) can make its own food'), 3)], 'bio-2-2', 'autotrophic',
      SQ(12, 'What is meant by the term autotrophic?'), 3, id='bio-2022-hl-q9-a-i'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(11, 'Explain why photosynthesis is an anabolic reaction.'),
      [pt(S('Glucose is built up from CO2 and H2O', 'input of energy.'), 3)], 'bio-2-2', 'photosynthesis-is-anabolic',
      SQ(12, 'Explain why photosynthesis is an anabolic reaction.'), 3, id='bio-2022-hl-q9-a-ii'),
    T('9bi', 'Q9(b)(i)', 'B', _A(11, 'Name a suitable photosynthetic organism you used for this investigation.'),
      [pt(S('Elodea (or Pondweed) or other correctly named organism'), 3)], 'bio-2-2', 'organism-for-photosynthesis',
      SQ(12, 'Name a suitable photosynthetic organism'), 3, stem=[Q9B], id='bio-2022-hl-q9-b-i-ii',
      decision=bundled('(b)(i) and (ii)', '(i), and (ii) is added')),
    T('9bii', 'Q9(b)(ii)', 'B', _A(11, 'Why was the organism named at part (b) (i) above suitable', 'investigation?'),
      [pt(S('Aquatic plant or bubbles can be seen', 'measured'), 3)], 'bio-2-2', 'why-elodea',
      SQ(12, 'Why was the organism named at part (b) (i) above suitable'), 3,
      stem=[Q9B, M('(i)', 11), _A(11, 'Name a suitable photosynthetic organism you used for this investigation.')]),
    T('9biii', 'Q9(b)(iii)', 'B', _A(11, 'Why was it important to keep other factors', 'the investigation?'),
      [pt(S('Only one variable or (they) don’t affect the rate', 'enzyme activity'), 3)], 'bio-2-2', 'fair-test',
      SQ(12, 'Why was it important to keep other factors constant?'), 3, stem=[Q9B], id='bio-2022-hl-q9-b-iii'),
    T('9biv', 'Q9(b)(iv)', 'B', _A(11, 'How did you keep the temperature of the organism constant for this activity?'),
      [pt(S('Water-bath or described'), 3)], 'bio-2-2', 'water-bath', SQ(12, 'How did you keep the temperature'), 3,
      stem=[Q9B], id='bio-2022-hl-q9-b-iv'),
    T('9bv', 'Q9(b)(v)', 'B', _A(11, 'Explain how you measured the rate of photosynthesis.'),
      [pt(S('Count the number of bubbles or measure volume'), 3),
       pt(S('per minute (or unit time) or over set period of time'), 3)], 'bio-2-2', 'measuring-photosynthesis',
      SQ(12, 'Explain how you measured the rate of photosynthesis.'), 6, stem=[Q9B], id='bio-2022-hl-q9-b-v'),
    T('9bvi1', 'Q9(b)(vi)1', 'B', _A(11, 'Using a solid line (', 'expected result at 25 °C.'),
      [pt(S('Increasing line (from zero) (eventually levelling off)'), 3, kind='criterion')], 'bio-2-2',
      'rate-at-25', SQ(12, '1. Sketch of expected result at 25°C'), 3, qfig='q9b-vi-1-question',
      id='bio-2022-hl-q9-b-vi',
      decision='The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. The solid line '
               'the paper draws in the ask is not in its text layer: the question is shown as printed.'),
    T('9bvi2', 'Q9(b)(vi)2', 'B', _A(11, 'Using a dashed line', 'been carried out at 60 °C.'),
      [pt(S('Line on x axis or very close to x axis'), 3, kind='criterion')], 'bio-2-2', 'rate-at-60',
      SQ(12, '2. Sketch of expected result at 60°C'), 3, qfig='q9b-vi-2-question',
      decision='Shown as printed, with the axes to sketch on.'),
    T('10ai', 'Q10(a)(i)', 'B', _A(12, 'State a location in plants where growth regulators are produced.'),
      [pt(S('Meristem or root tip or shoot tip or any correctly named meristem or location'), 3)], 'bio-2-4',
      'where-growth-regulators-form', SQ(13, 'State a location in plants where growth regulators'), 3,
      id='bio-2022-hl-q10-a', decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added')),
    T('10aii', 'Q10(a)(ii)', 'B', _A(12, 'How are growth regulators transported around a plant?'),
      [pt(S('(By) diffusion or (through) vascular tissue or phloem or xylem'), 3,
          note_sel=S('(accept dissolved in water)'))], 'bio-2-4', 'transporting-growth-regulators',
      SQ(13, 'How are growth regulators transported around a plant?'), 3),
    T('10bi', 'Q10(b)(i)', 'B', _A(12, 'Name a suitable plant tissue you used in this investigation.'),
      [pt(S('Root or shoot or seed (or named seed)'), 3)], 'bio-2-4', 'tissue-for-iaa',
      SQ(13, 'Name a suitable plant tissue you used'), 3, stem=[Q10B], id='bio-2022-hl-q10-b-i'),
    T('10bii', 'Q10(b)(ii)', 'B', _A(12, 'Describe how you set up the investigation.'),
      [anyn(S('Different concentrations (of IAA) /', 'any other correct practical step'), 4, 3)], 'bio-2-4',
      'setting-up-iaa', SQ(13, 'Describe how you set up the investigation.'), 12, stem=[Q10B],
      id='bio-2022-hl-q10-b-ii'),
    T('10biii', 'Q10(b)(iii)', 'B', _A(12, 'Describe how you measured the effect of IAA on the plant tissue.'),
      [pt(S('Use ruler (or grid) to measure length (or growth) of tissue'), 3)], 'bio-2-4', 'measuring-iaa-effect',
      SQ(13, 'Describe how you measured the effect of IAA'), 3, stem=[Q10B], id='bio-2022-hl-q10-b-iii'),
    T('10biv', 'Q10(b)(iv)', 'B', _A(12, 'Describe any one result of your investigation.'),
      [pt(S('More root growth in low concentration', 'concentration'), 3)], 'bio-2-4', 'iaa-result',
      SQ(13, 'Describe any one result of your investigation.'), 3, stem=[Q10B], id='bio-2022-hl-q10-b-iv'),
    T('10bv', 'Q10(b)(v)', 'B', _A(12, 'Describe one safety precaution you took in carrying out this investigation.'),
      [pt(S('Use gloves or lab coat or mask or any other correct precaution'), 3)], 'bio-2-4', 'iaa-safety',
      SQ(13, 'Describe one safety precaution'), 3, stem=[Q10B], id='bio-2022-hl-q10-b-v'),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'Give one precaution scientists use when working with microorganisms', 'laboratory.'),
      [pt(S('Wipe surface with disinfectant', '(i.e. PPE)'), 3)], 'bio-3-2', 'lab-precautions',
      SQ(14, 'Give one precaution scientists use'), 3, id='bio-2022-hl-q11-a-i'),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Explain the terms asepsis and sterility as applied to living organisms.'),
      [pt(S('Asepsis: free of pathogens'), 3), pt(S('Sterility: free of microorganisms'), 3)], 'bio-3-2',
      'asepsis-and-sterility', SQ(14, 'Explain the terms applied to living organisms.'), 6, id='bio-2022-hl-q11-a-ii'),
    T('11bi', 'Q11(b)(i)', 'C', _C(2, 'Draw a large labelled diagram of a typical bacterial cell.'),
      [pt(S('Cell wall + cell membrane + indication of nucleic acid'), 3, kind='criterion'),
       anyn(S('Cell wall / cell membrane / cytoplasm /', 'capsule or slime layer'), 3, 1)], 'bio-3-2',
      'drawing-a-bacterium', SQ(14, 'Drawing of a typical bacterial cell:'), 6, id='bio-2022-hl-q11-b-i'),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Many species of bacteria can form endospores.', 'endospore formation.'),
      [anyn(S('DNA replicates /', '(cell) rounds up'), 3, 3)], 'bio-3-2', 'endospores',
      SQ(14, 'Describe the main events of endospore formation.'), 9, id='bio-2022-hl-q11-b-ii'),
    T('11biii1', 'Q11(b)(iii)1', 'C', _C(2, 'Give any two examples of harmful bacteria.'),
      [pt(S('Any two correctly named bacteria or named bacterial diseases'), 6, kind='criterion', units=[3, 3])],
      'bio-3-2', 'harmful-bacteria', SQ(14, '1. Give any two examples of harmful bacteria.'), 6, stem=[Q11B3],
      id='bio-2022-hl-q11-b-iii',
      decision='The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added.'),
    T('11biii2', 'Q11(b)(iii)2', 'C', _C(2, 'Bacterial infections can be treated with antibiotics.', 'What is an antibiotic?'),
      [pt(S('A chemical that kills (or inhibits growth of) bacteria'), 3)], 'bio-3-2', 'antibiotic',
      SQ(14, '2. Bacterial infections can be treated'), 3, stem=[Q11B3]),
    T('11biii3', 'Q11(b)(iii)3', 'C', _C(2, 'State one possible reason why antibiotic resistance', 'in bacteria.'),
      [pt(S('Overuse (misuse) or mutation in bacteria'), 3)], 'bio-3-2', 'antibiotic-resistance',
      SQ(14, '3. State one possible reason why antibiotic resistance'), 3, stem=[Q11B3]),
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Give two factors that affect the growth of microorganisms', 'bacteria.'),
      [anyn(S('Temperature / oxygen concentration / pH /', 'presence of waste products'), 2, 3)], 'bio-3-2',
      'growth-factors', SQ(15, 'Give two factors that affect the growth of microorganisms.'), 6, stem=Q11C,
      id='bio-2022-hl-q11-c-i'),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Explain how either of the factors you named at part (c) (i)', 'affects growth.'),
      [pt(S('Matching explanation (accept enzyme activity', 'water availability, etc)'), 3, kind='criterion')],
      'bio-3-2', 'how-a-factor-affects-growth', SQ(15, 'Explain how one these factors affect growth.'), 3,
      stem=Q11C + [M('(i)', 2), _C(2, 'Give two factors that affect the growth of microorganisms', 'bacteria.')],
      decision='"Either of the factors you named": one matching-explanation row; one card.'),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'Distinguish between batch and continuous flow', 'each type.'),
      [pt(S('Batch: organisms go through all phases', 'emptied at end.'), 3),
       pt(S('Continuous flow: organisms maintained in one', 'products constantly removed.'), 3)], 'bio-3-2',
      'batch-and-continuous-flow', SQ(15, 'Distinguish between:'), 6, stem=Q11C, id='bio-2022-hl-q11-c-iii'),
    T('11civ', 'Q11(c)(iv)', 'C', [_C(2, 'Sketch a plot of a microorganism growth curve.', 'is not in the correct order.'),
                                   _C(2, 'stationary', br=True), _C(2, 'survival', br=True), _C(2, 'log', br=True),
                                   _C(2, 'decline', br=True), _C(2, 'lag', br=True, after='decline')],
      [pt(S('All five phases visible on curve'), 3, kind='criterion', label=S('Sketch:')),
       pt(S('x-axis: Time and y-axis: Population or Number of organisms'), 3, kind='criterion', whole=True,
          label=S('Axes labels:')),
       pt(S('Curve labels: Correctly labelled with all five phases in the correct order'), 3, kind='criterion',
          whole=True)], 'bio-3-2', 'growth-curve', SQ(15, 'Sketch plot of a growth curve.'), 9, stem=Q11C,
      id='bio-2022-hl-q11-c-iv'),
    T('12a', 'Q12(a)', 'C', _C(3, 'Explain the following three ecological terms: biosphere; niche; symbiosis.'),
      [pt(S('Biosphere: Part of the earth where life can exist.'), 3),
       pt(S('Role of the organism (or plant or animal)'), 3, label=S('Niche:')),
       pt(S('Symbiosis: Relationship between species involving benefit (or described)'), 3)], 'bio-3-1',
      'biosphere-niche-symbiosis', SQ(16, '(a) Explain the following three ecological terms:'), 9,
      id='bio-2022-hl-q12-a', decision='One printed ask listing three terms, each priced: one card, a row per term.'),
] + [
    T(f'12b{r}', f'Q12(b)({r})', 'C', _C(3, ask, aend), rows, 'bio-3-1', concept, SQ(16, sq), total, stem=Q12B,
      id=f'bio-2022-hl-q12-b-{r}' if r in ('i', 'ii', 'iii', 'iv', 'vi', 'vii') else
      ('bio-2022-hl-q12-b-v' if r == 'v1' else None), decision=dec)
    for r, ask, aend, rows, concept, sq, total, dec in [
        ('i', 'Suggest one reason why dragonflies are such successful predators.', None,
         [pt(S('Huge eyes or compound eyes', 'other correct'), 3)], 'successful-predators',
         'Suggest one reason why dragonflies are such successful predators.', 3, ''),
        ('ii', 'Give two benefits for dragonfly populations living near freshwater vegetation.', None,
         [pt(S('Protection'), 3), pt(S('Laying eggs'), 3)], 'freshwater-vegetation',
         'Give two benefits for dragonfly populations', 6, ''),
        ('iii', 'Suggest a benefit of the adult and the nymph having different food sources.', None,
         [pt(S('Not in competition (for same resource) or greater chance of survival'), 3)], 'different-food-sources',
         'Suggest a benefit of the adult and the nymph', 3, ''),
        ('iv', 'What type of ecological relationship exists between swallows and dragonflies?', None,
         [pt(S('Predator-prey or predation'), 3)], 'predation', 'What type of ecological relationship exists', 3, ''),
        ('vi', 'Suggest one reason why volunteers are being asked to identify dragonflies.', None,
         [pt(S('Conservation or monitor numbers', 'monitor water quality'), 3)], 'why-survey-dragonflies',
         'Suggest one reason why volunteers', 3, ''),
        ('vii', 'What might a volunteer use to help them identify a dragonfly?', None,
         [pt(S('Key or compare pictures or charts'), 3)], 'identifying-dragonflies',
         'What might a volunteer use to help them identify', 3, '')]
] + [
    T(f'12bv{n}', f'Q12(b)(v){n}', 'C', [_C(3, 'Suggest one possible effect on the dragonfly population', 'of the following:'),
                                        item(3, n, what, 'Suggest one possible effect')],
      [pt(S(ans), 3, label=S(lab))] if lab else [pt(S(ans), 3)], 'bio-3-1', concept,
      SQ(16, 'Suggest one possible effect on the dragonfly population of:'), 3, stem=Q12B,
      id='bio-2022-hl-q12-b-v' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, what, ans, lab, concept in [
        (1, 'a disease affecting the swallows', 'Increases', None, 'fewer-predators'),
        (2, 'cutting of vegetation (e.g. reeds) along the river banks.', 'Decreases', None, 'losing-vegetation')]
] + [
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'Outline the main events of the carbon cycle.'),
      [anyn(S('Brief note on role of: Photosynthesis /', 'any other valid point'), 3, 3)], 'bio-3-2', 'carbon-cycle',
      SQ(16, 'Outline the main events of the carbon cycle.'), 9, id='bio-2022-hl-q12-c-i-ii',
      decision=bundled('(c)(i) and (ii)', '(i), and (ii) is added')),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Explain why the carbon cycle is critical to life on Earth.'),
      [pt(S('For C to be reused by organisms', 'basis of food chains'), 3)], 'bio-3-2', 'why-the-carbon-cycle-matters',
      SQ(16, 'Explain why the carbon cycle is critical'), 3),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Explain the underlined term.'),
      [pt(S('Any harmful addition to environment'), 3)], 'bio-3-1', 'pollution', SQ(16, 'Explain the term'), 3,
      qfig='q12c-iii-question', id='bio-2022-hl-q12-c-iii',
      decision='The paper marks the term to explain by underlining it, which the text layer drops: the question '
               'is shown as the paper prints it.'),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Waste management is important in controlling pollution.', 'forestry.'),
      [pt(S('Any valid example'), 3, kind='criterion')], 'bio-3-1', 'waste-management',
      SQ(16, 'Give one example of waste management'), 3, stem=Q12C),
    T('12cv', 'Q12(c)(v)', 'C', _C(3, 'Other than global warming or pollution, give two factors', 'human population.'),
      [anyn(S('War / famine / contraception / disease / any valid example'), 2, 3)], 'bio-3-1', 'human-population',
      SQ(16, 'Other than global warming or pollution'), 6, id='bio-2022-hl-q12-c-v'),
    T('13a', 'Q13(a)', 'C', _C(4, 'Nucleic acids are composed of subunits called nucleotides.', 'any one nucleotide.'),
      [pt(S('Drawing', after='Draw and label the structure'), 6, kind='criterion', units=[3, 3],
          note_sel=S('6, 3, 0')),
       pt(S('Phosphate (or P)'), 1), pt(S('Deoxyribose or ribose'), 1), pt(S('Base or any one named base or letter'), 1)],
      'bio-1-2', 'drawing-a-nucleotide', SQ(17, 'Draw and label the structure of any one nucleotide.'), 9,
      id='bio-2022-hl-q13-a'),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'What is the name of process K that results in the formation of molecule L?'),
      [pt(S('*Transcription'), 3)], 'bio-2-3', 'transcription', SQ(17, 'What is the name of process K'), 3,
      stem=[Q13B], fig='q13-protein-synthesis', id='bio-2022-hl-q13-b-i-ii',
      decision=bundled('(b)(i) and (ii)', '(i), and (ii) is added')),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'Name molecule L.'),
      [pt(S('*mRNA or *messenger RNA'), 3)], 'bio-2-3', 'mrna', SQ(17, 'Name molecule L.'), 3, stem=[Q13B],
      fig='q13-protein-synthesis'),
    T('13biii', 'Q13(b)(iii)', 'C', [_C(4, 'Part of the sequence of nitrogenous bases in the gene is as follows:'),
                                     _C(4, 'Base sequence: A C G T G C T G A', br=True),
                                     _C(4, 'Using this sequence, write out in order', 'found in molecule L.', br=True)],
      [pt(S('U G C A C G A C U'), 3, note_sel=S('(all must be correct for 3)'))], 'bio-2-3', 'complementary-bases',
      SQ(17, 'Write out the complementary sequence of bases'), 3, stem=[Q13B], fig='q13-protein-synthesis',
      id='bio-2022-hl-q13-b-iii'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'Give the name of the opening through which molecule L leaves organelle J.'),
      [pt(S('*Nuclear pore'), 3)], 'bio-2-3', 'nuclear-pore', SQ(17, 'Give the name of the opening'), 3, stem=[Q13B],
      fig='q13-protein-synthesis', id='bio-2022-hl-q13-b-iv-v',
      decision=bundled('(b)(iv) and (v)', '(iv), and (v) 1. and 2. are added')),
    T('13bv1', 'Q13(b)(v)1', 'C', _C(4, 'Identify structure M.'),
      [pt(S('*Ribosome'), 3)], 'bio-2-3', 'ribosome', SQ(17, '1. Identify structure M.'), 3,
      stem=[Q13B, _C(4, 'Molecule L arrives at structure M in the cytosol as shown.')], fig='q13-protein-synthesis'),
    T('13bv2', 'Q13(b)(v)2', 'C', _C(4, 'Name the main molecule from which structure M is made.'),
      [pt(S('*rRNA or *Ribosomal RNA'), 3)], 'bio-2-3', 'ribosomal-rna', SQ(17, '2. Name the main molecule'), 3,
      stem=[Q13B, _C(4, 'Molecule L arrives at structure M in the cytosol as shown.')], fig='q13-protein-synthesis'),
    T('13bvi', 'Q13(b)(vi)', 'C', _C(4, 'Describe the events that occur at structure M', 'functioning protein.'),
      [anyn(S('tRNA brings amino acids to ribosome /', 'start or stop codon'), 3, 3)], 'bio-2-3', 'translation',
      SQ(17, 'Describe the events that occur at structure M'), 9, stem=[Q13B], fig='q13-protein-synthesis',
      id='bio-2022-hl-q13-b-vi', labels=[L('M', S('*Ribosome', page=17), False)]),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Explain the underlined terms.'),
      [pt(S('A version (variant) of a gene or (alternative) form of a gene'), 3, label=S('Allele:')),
       pt(S('Homozygous: (When) identical alleles are present (for a trait)'), 3)], 'bio-1-4', 'allele-and-homozygous',
      SQ(17, 'Explain the terms:'), 6, qfig='q13c-i-question', id='bio-2022-hl-q13-c-i',
      decision='The paper marks the terms to explain by underlining them: the question is shown as printed.'),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Draw two chromosome diagrams (one for each parent)', 'homozygous recessive.'),
      [pt(S('Chromosome diagrams shows 2 pairs of homologous chromosomes for each', 'parent.'), 3, kind='criterion',
          note_sel=S('(Chromosomes for first parent must match chromosomes for second parent)')),
       pt(S('1 parent clearly FFDD or ffdd'), 3, kind='criterion'),
       pt(S('Loci of the alleles for each parent'), 3, kind='criterion', note_sel=S('(must be correct and matching)')),
       pt(S('(Homozygous) recessive and (homozygous) dominant correctly indicated.'), 3, kind='criterion')],
      'bio-1-4', 'dihybrid-chromosome-diagrams', SQ(17, 'Draw two chromosome diagrams'), 12, stem=[Q13C],
      id='bio-2022-hl-q13-c-ii'),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'Using a Punnet square, or otherwise, describe the result of this cross.'),
      [pt(S('*FfDd'), 3), pt(S('*White and disc-shaped fruit'), 3)], 'bio-1-4', 'dihybrid-cross',
      SQ(17, 'Using a Punnet square, or otherwise'), 6, stem=[Q13C]),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'In which cell organelle does photosynthesis occur?'),
      [pt(S('*Chloroplast'), 3)], 'bio-2-2', 'chloroplast', SQ(18, 'In which cell organelle does photosynthesis occur?'),
      3, id='bio-2022-hl-q14-a-i-ii', decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added')),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Name the pigment essential for photosynthesis.'),
      [pt(S('*Chlorophyll'), 3)], 'bio-2-2', 'chlorophyll', SQ(18, 'Name the pigment essential for photosynthesis.'), 3),
    T('14aiii', 'Q14(a)(iii)', 'C', _C(5, 'Describe one way in which horticulturists can increase', 'greenhouses.'),
      [pt(S('Heat to (or keep at) optimum temperature', 'non-photosynthetic reason'), 3)], 'bio-2-2',
      'greenhouse-yields', SQ(18, 'Describe one way in which horticulturists'), 3, id='bio-2022-hl-q14-a-iii'),
] + [
    T(f'14b{r}', f'Q14(b)({r})', 'C', _C(5, ask, aend), rows, 'bio-2-2', concept, SQ(18, sq), total, stem=[Q14B],
      fig='q14-photosynthesis', id=old, decision=dec)
    for r, ask, aend, rows, concept, sq, total, old, dec in [
        ('i', 'Water is split during stage 1 using the energy in light.', 'name given to this process?',
         [pt(S('*Photolysis'), 3)], 'photolysis', 'Water is split during stage 1', 3, 'bio-2022-hl-q14-b-i-ii',
         bundled('(b)(i) and (ii)', '(i), and (ii) is added')),
        ('ii', 'Identify molecule X, produced as a by-product of the splitting of water.', None,
         [pt(S('*Oxygen (or O2)'), 3)], 'oxygen-by-product', 'Identify molecule X', 3, None, ''),
        ('iii', 'Identify molecule Y.', None, [pt(S('*NADPH'), 3)], 'nadph', 'Identify molecule Y.', 3, None, ''),
        ('iv', 'Describe how molecule Y is produced.', None,
         [pt(S('Added (or picked up) electrons (e–)'), 3), pt(S('Added (or picked up) proton (hydrogen ion or H+)'), 3)],
         'making-nadph', 'Describe how molecule Y is produced.', 6, 'bio-2022-hl-q14-b-iv', ''),
        ('v', 'Name stage 2 shown in the diagram above.', None,
         [pt(S('*Light independent stage (or dark stage or Calvin Cycle)'), 3)], 'light-independent-stage',
         'Name stage 2 shown in the diagram.', 3, 'bio-2022-hl-q14-b-v', ''),
        ('vi', 'What does ATP stand for?', None, [pt(S('*Adenosine triphosphate'), 3)], 'atp',
         'What does ATP stand for?', 3, 'bio-2022-hl-q14-b-vi', ''),
        ('vii', 'What is the role of ATP in stage 2 of photosynthesis', 'above?',
         [pt(S('To transfer energy or to carry energy or to release energy'), 3)], 'role-of-atp',
         'What is the role of ATP in stage 2', 3, 'bio-2022-hl-q14-b-vii-viii',
         bundled('(b)(vii) and (viii)', '(vii), and (viii) is added')),
        ('viii', 'Identify molecule Z, the end product of stage 2.', None, [pt(S('Glucose (or formula)'), 3)],
         'glucose', 'Identify molecule Z, the end product of stage 2.', 3, None, '')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'Describe two events that occur during prophase.'),
      [anyn(S('Nuclear membrane breaks down', 'spindle forms'), 2, 3)], 'bio-2-3', 'prophase',
      SQ(19, 'Describe two events that happen during prophase.'), 6, stem=[Q14C], id='bio-2022-hl-q14-c-i-ii',
      decision=bundled('(c)(i) and (ii)', '(i), and (ii) is added')),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Describe one event that occurs during metaphase.'),
      [pt(S('Chromosome along equator (middle)', 'centromere)'), 3)], 'bio-2-3', 'metaphase',
      SQ(19, 'Describe one event that occurs during metaphase.'), 3, stem=[Q14C]),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Draw a large labelled diagram of a cell with a diploid number', 'of mitosis.'),
      [pt(S('Diagram: Eight chromosomes'), 3, kind='criterion'),
       pt(S('Chromosomes being pulled apart'), 3, kind='criterion'),
       anyn(S('chromosome / spindle / equator / poles / centromere'), 3, 1)], 'bio-2-3', 'drawing-anaphase',
      SQ(19, 'Draw a labelled diagram of a cell with a diploid number'), 9, stem=[Q14C], id='bio-2022-hl-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'At the end of mitosis, the cell divides.', 'and in a plant cell.'),
      [pt(S('An animal cell: Cleavage furrow forms or described'), 3),
       pt(S('Cell plate forms or described'), 3, label=S('A plant cell:'))], 'bio-2-3', 'cytokinesis',
      SQ(19, 'Describe how cell division occurs in:'), 6, stem=[Q14C], id='bio-2022-hl-q14-c-iv'),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'Explain the underlined terms.'),
      [pt(S('Removal of metabolic waste from a cell (or organism)'), 3, label=S('Excretion:')),
       pt(S('Homeostasis: Maintaining a constant internal environment'), 3)], 'bio-2-4', 'excretion-and-homeostasis',
      SQ(20, 'Explain the underlined terms.'), 6, qfig='q15a-i-question', id='bio-2022-hl-q15-a',
      decision=bundled('(a)(i) and (ii)', '(i), and (ii) is added') + ' The terms are marked by underlining: the '
               'question is shown as printed.'),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'Name one excretory organ in plants.'),
      [pt(S('Leaf or stem or root'), 3, note_sel=S('(accept stomata and lenticel)'))], 'bio-2-6',
      'excretion-in-plants', SQ(20, 'Name one excretory organ in plants.'), 3,
      stem=[_C(6, 'Excretion is an important process in homeostasis in living organisms.')]),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'The kidneys are located in the abdomen', 'function of this layer of fat?'),
      [pt(S('Protection (accept insulation)'), 3)], 'bio-2-6', 'fat-around-kidneys',
      SQ(20, 'What is the function of the layer of fat'), 3, stem=[Q15B], fig='q15-kidney', id='bio-2022-hl-q15-b-i'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'Identify the regions of the kidney labelled A, B and C.'),
      [pt(S('A: *Cortex'), 1), pt(S('B: *Medulla (pyramid)'), 1), pt(S('C: *Pelvis'), 1)], 'bio-2-6', 'regions-of-the-kidney',
      SQ(20, 'Identify the regions of the kidney labelled A, B, and C.'), 3, stem=[Q15B], fig='q15-kidney',
      labels=asked(L_KIDNEY, 'A', 'B', 'C')),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Identify the region in the kidney, by name or label', 'occurs.'),
      [pt(S('*A or *cortex'), 3)], 'bio-2-6', 'where-filtration-happens', SQ(20, 'Identify the region in the kidney'),
      3, stem=[Q15B], fig='q15-kidney', id='bio-2022-hl-q15-b-iii-iv',
      decision=bundled('(b)(iii) and (iv)', '(iii), and (iv) is added')),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'Explain the importance of blood entering the glomerulus under pressure.'),
      [pt(S('Force filtered (or ultrafiltration)', '(or described)'), 3)], 'bio-2-6', 'glomerular-pressure',
      SQ(20, 'Explain the importance of blood entering the glomerulus'), 3, stem=[Q15B], fig='q15-kidney'),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'State two reasons why there are many capillaries', 'nephron.'),
      [pt(S('Reabsorption (or described)'), 3), pt(S('Secretion (or described)'), 3)], 'bio-2-6',
      'capillaries-around-the-nephron', SQ(20, 'State two reasons why there are many capillaries'), 6, stem=[Q15B],
      fig='q15-kidney', id='bio-2022-hl-q15-b-v'),
    T('15bvi', 'Q15(b)(vi)', 'C', _C(6, 'Describe how ADH (anti-diuretic hormone) affects the volume of urine.'),
      [pt(S('(ADH) acts on collecting duct (or DCT)', 'water reabsorbed'), 3),
       pt(S('(More ADH) leads to low volume of urine'), 3, note_sel=S('(converse also accepted)'))], 'bio-2-6', 'adh',
      SQ(20, 'Describe how ADH affects the volume of urine.'), 6, stem=[Q15B], fig='q15-kidney',
      id='bio-2022-hl-q15-b-vi-vii',
      decision=bundled('(b)(vi) and (vii)', '(vi), and (vii) is added')),
    T('15bvii', 'Q15(b)(vii)', 'C', _C(6, 'Urine collects at the region labelled C', 'urine travels to the bladder.'),
      [pt(S('*Ureter'), 3)], 'bio-2-6', 'ureter', SQ(20, 'Name the structure through which urine travels'), 3,
      stem=[Q15B], fig='q15-kidney', labels=asked(L_KIDNEY, 'C')),
    T('15ci', 'Q15(c)(i)', 'C', _C(6, 'By what process does water enter the root hairs?'),
      [pt(S('*Osmosis'), 3)], 'bio-2-6', 'osmosis-into-root-hairs', SQ(21, 'By what process does water enter'), 3,
      stem=[Q15C], id='bio-2022-hl-q15-c-i'),
    T('15cii', 'Q15(c)(ii)', 'C', [_C(6, 'Draw a large diagram of a transverse section of a root', 'tissues:'),
                                   _C(6, 'dermal;', br=True), _C(6, 'ground;', br=True), _C(6, 'vascular.', br=True)],
      [pt(S('Dermal tissue + Vascular + Root hair', after='Drawing T.S of root:'), 3, kind='criterion'),
       pt(S('Dermal', after='Labels:'), 1, kind='criterion'), pt(S('Ground', after='Labels:'), 1, kind='criterion'),
       pt(S('Vascular', after='Labels:'), 1, kind='criterion')], 'bio-2-6', 'root-section',
      SQ(21, 'Labels:', after='Drawing T.S of root:'), 6, stem=[Q15C], id='bio-2022-hl-q15-c-ii'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Name the two Irish scientists who first described', 'water in plants.'),
      [pt(S('(Henry) Dixon'), 3), pt(S('(John) Joly'), 3)], 'bio-2-6', 'dixon-and-joly',
      SQ(21, 'Name the two Irish scientists'), 6, stem=[Q15C], id='bio-2022-hl-q15-c-iii-iv',
      decision=bundled('(c)(iii) and (iv)', '(iii), and (iv) is added')),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Describe in detail the upward movement of water in plants.'),
      [anyn(S('Root pressure pushes (water) /', 'tension or pull'), 3, 3)], 'bio-2-6', 'water-transport',
      SQ(21, 'Describe in detail the upward movement of water'), 9, stem=[Q15C]),
    # Q16: any two of (a)-(d), each 30.
    T('16ai', 'Q16(a)(i)', 'C', _C(7, 'Name each of these parts.'),
      [pt(S('Central nervous system (CNS)'), 3), pt(S('Peripheral nervous system (PNS)'), 3)], 'bio-2-4',
      'parts-of-the-nervous-system', SQ(22, 'Name each of these parts of the human nervous system.'), 6,
      stem=[Q16A1], id='bio-2022-hl-q16-a-i'),
    T('16aii', 'Q16(a)(ii)', 'C', [_C(7, 'Draw a large diagram of a neuron and label the following parts:'),
                                   _C(7, 'dendrites;', 'myelin sheath.', br=True)],
      [pt(S('Cell body + dendrites + axon visible'), 6, kind='criterion', units=[3, 3],
          note_sel=S('(any one missing = 3)')),
       pt(S('Dendrites', after='Labels:'), 1, kind='criterion'), pt(S('Axon', after='Labels:'), 1, kind='criterion'),
       pt(S('Myelin sheath', after='Labels:'), 1, kind='criterion')], 'bio-2-4', 'drawing-a-neuron',
      SQ(22, 'Drawing of a neuron:'), 9, id='bio-2022-hl-q16-a-ii'),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'Distinguish between the function of an interneuron', 'on each.'),
      [pt(S('Transmit impulse within the CNS (or from sensory to motor neuron)'), 3, label=S('Interneuron:')),
       pt(S('Sensory neuron: Transmit impulse (from sense organ) to CNS'), 3)], 'bio-2-4', 'neuron-functions',
      SQ(22, 'Distinguish between the function of an interneuron'), 6, id='bio-2022-hl-q16-a-iii'),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'How is a nerve impulse conducted along a neuron?'),
      [pt(S('(Movement of) ions (or example)'), 3)], 'bio-2-4', 'impulse-conduction',
      SQ(22, 'How is a nerve impulse conducted along a neuron?'), 3, id='bio-2022-hl-q16-a-iv-v',
      decision=bundled('(a)(iv) and (v)', '(iv), and (v) is added')),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'Name the gap that exists between two neurons in close contact.'),
      [pt(S('*Synaptic cleft'), 3)], 'bio-2-4', 'synaptic-cleft', SQ(22, 'Name the gap that exists'), 3),
] + [
    T('16avi', 'Q16(a)(vi)', 'C', [_C(7, 'Give one possible cause for either paralysis or Parkinson’s disease.'),
                                   _C(7, 'In your answer, state clearly to which nervous system disorder', 'referring.')],
      [pt(S(start, end), 3, note_sel=S('Cause must match name disorder', 'Cause must match name disorder'))], 'bio-2-4', f'cause-of-{route}',
      SQ(22, 'Give one possible cause for either:'), 3, route=route,
      id='bio-2022-hl-q16-a-vi' if route == 'paralysis' else None,
      decision='Paralysis or Parkinson\'s disease: the scheme prints a separate list of causes for each, so each '
               'is a route card.')
    for route, start, end in [('paralysis', 'Injury (damage) to spinal cord or', 'valid cause'),
                              ('parkinsons-disease', 'Decrease in dopamine levels or decrease in',
                               'or aging or other valid cause')]
] + [
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'Name the parts of the eye labelled P, Q and R.'),
      [pt(S('*Lens'), 1, label=S('P:')), pt(S('*Cornea'), 1, label=S('Q:')), pt(S('*Optic nerve'), 1, label=S('R:'))],
      'bio-2-4', 'parts-of-the-eye', SQ(23, 'Name the parts of the eye labelled P, Q and R.'), 3, stem=[Q16B],
      fig='q16-eye', id='bio-2022-hl-q16-b-i-fig', labels=asked(L_EYE, 'P', 'Q', 'R')),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Name the two types of light receptor cells in the retina', 'each type.'),
      [pt(S('*Rods'), 3), pt(S('*Cones'), 3), pt(S('Rods: vision in dim light or black & white vision'), 3),
       pt(S('Cones: vision in bright light or colour vision'), 3)], 'bio-2-4', 'rods-and-cones',
      SQ(23, 'Name the two types of light receptor in the retina.'), 12, stem=[Q16B], fig='q16-eye',
      id='bio-2022-hl-q16-b-ii'),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'Explain why damage to the part labelled R could result in blindness.'),
      [pt(S('No impulse (or message) will be sent to the brain (to be interpreted)'), 3)], 'bio-2-4', 'optic-nerve',
      SQ(23, 'Explain why damage to the part labelled R'), 3, stem=[Q16B], fig='q16-eye', id='bio-2022-hl-q16-b-iii',
      labels=asked(L_EYE, 'R')),
] + [
    T(f'16biv{n}', f'Q16(b)(iv){n}', 'C', [_C(7, 'The iris and pupil are affected by light intensity.',
                                             'front of the eye to show:'), item(7, n, what, 'front of the eye to show:')],
      [pt(S(row), 3)], 'bio-2-4', concept, SQ(23, 'Sketch two diagrams of the front of the eye to show:'), 3,
      stem=[Q16B], fig='q16-eye', id='bio-2022-hl-q16-b-iv' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, what, row, concept in [(1, 'the iris and pupil in bright light', 'Pupil small',
                                   'pupil-in-bright-light'),
                                  (2, 'the iris and pupil in dim light.', 'Pupil large', 'pupil-in-dim-light')]
] + [
    T('16bv', 'Q16(b)(v)', 'C', [_C(7, 'Describe one corrective measure for one of the following:'),
                                 _C(7, 'long sightedness or short sightedness or a named hearing defect.', br=True),
                                 _C(7, 'In your answer, state clearly to which disorder you are referring.', br=True)],
      rows, 'bio-2-4', f'correcting-{route}', SQ(23, 'Describe corrective measures for one of the following:'), 3,
      stem=[Q16B], fig='q16-eye', route=route, id='bio-2022-hl-q16-b-v' if route == 'long-sightedness' else None,
      decision='Long sightedness, short sightedness or a named hearing defect: the scheme prints a separate '
               'correction for each, so each is a route card.')
    for route, rows in [('long-sightedness', [pt(S('Convex lens'), 3)]),
                        ('short-sightedness', [pt(S('Concave lens'), 3)]),
                        ('hearing-defect', [pt(S('Valid named defect', 'any valid answer'), 3, kind='criterion')])]
] + [
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'Vision and hearing are two of the five senses in humans.', 'with this sense.'),
      [pt(S('Touch and skin or smell and nose or taste and tongue'), 3)], 'bio-2-4', 'other-senses',
      SQ(23, 'Name one other sense and name an organ'), 3, stem=[Q16B], fig='q16-eye', id='bio-2022-hl-q16-b-vi'),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'Name one type of synovial joint and give one location', 'found.'),
      [pt(S('Hinge or Ball and socket'), 3, label=S('Type:')),
       pt(S('Knee or elbow or Hip or shoulder'), 3, label=S('Location:'), note_sel=S('(must match type)'))],
      'bio-2-4', 'synovial-joints', SQ(24, 'Name one type of synovial joint'), 6, stem=[Q16C], fig='q16-joint',
      id='bio-2022-hl-q16-c-i'),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Name the structure A that connect two bones in a joint.'),
      [pt(S('*Ligament'), 3)], 'bio-2-4', 'ligament', SQ(24, 'Name the structure A that connect two bones'), 3,
      stem=[Q16C], fig='q16-joint', id='bio-2022-hl-q16-c-ii'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'Name and give one function of the part labelled B.'),
      [pt(S('*Cartilage'), 3), pt(S('Shock absorber or protects bone or reduces friction'), 3)], 'bio-2-4', 'cartilage',
      SQ(24, 'Name part B:'), 6, stem=[Q16C], fig='q16-joint', id='bio-2022-hl-q16-c-iii', labels=asked(L_JOINT, 'B')),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Name the structure that connects muscles to bones.'),
      [pt(S('*Tendon'), 3)], 'bio-2-4', 'tendon', SQ(24, 'Name the structure that connects muscles to bones.'), 3,
      stem=[Q16C], fig='q16-joint', id='bio-2022-hl-q16-c-iv-v', decision=bundled('(c)(iv) and (v)', '(iv), and (v) is added')),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'Give one function of compact bone.'),
      [pt(S('Strength or rigidity or shape or structure or support'), 3)], 'bio-2-4', 'compact-bone',
      SQ(24, 'Give one function of compact bone.'), 3, stem=[Q16C], fig='q16-joint'),
    T('16cvi', 'Q16(c)(vi)', 'C', _C(8, 'Spongy bone contains bony bars and plates', 'function of this tissue.'),
      [pt(S('*(Bone) marrow'), 3), pt(S('Makes blood cells or stores fat'), 3)], 'bio-2-4', 'bone-marrow',
      SQ(24, 'Name the tissue that fills these spaces'), 6, stem=[Q16C], fig='q16-joint', id='bio-2022-hl-q16-c-vi'),
] + [
    T('16cvii', 'Q16(c)(vii)', 'C', [_C(8, 'Give one possible cause for either arthritis or osteoporosis.'),
                                     _C(8, 'In your answer, state clearly to which musculoskeletal', 'referring.')],
      [pt(S(start), 3, note_sel=S('(must mention which condition)'))], 'bio-2-4', f'cause-of-{route}',
      SQ(24, 'Give one possible cause for either arthritis or osteoporosis.'), 3, stem=[Q16C], fig='q16-joint',
      route=route,
      id='bio-2022-hl-q16-c-vii' if route == 'arthritis' else None,
      decision='Arthritis or osteoporosis: the scheme prints a separate list of causes for each, so each is a '
               'route card.')
    for route, start in [('arthritis', 'Wear and tear (or injury) or genetic'),
                         ('osteoporosis', 'Hormonal or dietary or genetic')]
] + [
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'State the collective term used to describe the anther and filament', 'flower.'),
      [pt(S('*Stamen'), 3)], 'bio-2-5', 'stamen', SQ(25, 'State the collective term'), 3, stem=[Q16D],
      id='bio-2022-hl-q16-d-i'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Pollen grains are produced in the anther.', 'pollen grains in the anther.'),
      [anyn(S('Diploid / microspore mother cell /', 'the tube nucleus.'), 3, 3)], 'bio-2-5', 'pollen-development',
      SQ(25, 'Outline the main events in the development of pollen grains.'), 9, stem=[Q16D], id='bio-2022-hl-q16-d-ii'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'What is meant by the term pollination?'),
      [pt(S('Transfer of pollen from the anther to the stigma'), 3)], 'bio-2-5', 'pollination',
      SQ(25, 'What is meant by the term'), 3, stem=[Q16D], id='bio-2022-hl-q16-d-iii-iv',
      decision=bundled('(d)(iii) and (iv)', '(iii), and (iv) is added')),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Name two methods by which pollination can occur.'),
      [anyn(S('Wind / insect (animal) / water / self'), 2, 3)], 'bio-2-5', 'pollination-methods',
      SQ(25, 'Name two methods by which pollination can occur.'), 6, stem=[Q16D]),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Describe the main events that occur immediately after pollination.'),
      [anyn(S('Pollen grain germinates (develops) /', 'triploid endosperm.'), 3, 3)], 'bio-2-5', 'fertilisation-in-plants',
      SQ(25, 'Describe the main events that occur immediately after pollination.'), 9, stem=[Q16D],
      id='bio-2022-hl-q16-d-v'),
    # Q17: any two of (a)-(d), each 30.
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'Name the two scientists credited with developing the theory', 'natural selection.'),
      [pt(S('Darwin'), 3), pt(S('Wallace'), 3)], 'bio-1-5', 'darwin-and-wallace',
      SQ(26, 'Name the two scientists credited'), 6, stem=Q17A, fig='q17-scientists', id='bio-2022-hl-q17-a-i'),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Explain the three underlined terms.'),
      [pt(S('Evolution: Genetic changes in populations in response to environmental conditions.'), 3),
       pt(S('(Group of) organisms capable of reproducing (or breeding) to produce', 'fertile offspring.'), 3,
          label=S('Species:')),
       pt(S('Inherited: (Passed from parents) to offspring using genes.'), 3)], 'bio-1-5',
      'evolution-species-inherited', SQ(26, 'Explain the three underlined terms.'), 9, qfig='q17a-ii-question',
      id='bio-2022-hl-q17-a-ii',
      decision='The paper marks the terms to explain by underlining them across its passage: the passage and '
               'question are shown as printed.'),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'Explain how meiosis contributes to variation.'),
      [pt(S('It rearranges genetic material (or described) or it produces non-identical cells'), 3,
          note_sel=S('(accept crossing over)'))], 'bio-1-5', 'meiosis-and-variation',
      SQ(26, 'Explain how meiosis contributes to variation.'), 3, stem=Q17A, fig='q17-scientists',
      id='bio-2022-hl-q17-a-iii'),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Describe three points put forward in the theory of natural selection', 'above.'),
      [anyn(S('High reproductive rates /', 'with each generation.'), 3, 3)], 'bio-1-5', 'natural-selection',
      SQ(26, 'Describe three points put forward'), 9, stem=Q17A, fig='q17-scientists', id='bio-2022-hl-q17-a-iv-v',
      decision=bundled('(a)(iv) and (v)', '(iv), and (v) is added')),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'Give one piece of evidence that supports the theory of natural selection.'),
      [pt(S('Fossils or comparative embryology or comparative anatomy or other correct answer'), 3)], 'bio-1-5',
      'evidence-for-evolution', SQ(26, 'Give one piece of evidence'), 3),
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'The placenta forms from tissues of the mother and the embryo.', 'placenta.'),
      [anyn(S('Movement of food from mother to foetus', 'from mixing'), 2, 3)], 'bio-2-5', 'placenta',
      SQ(27, 'Give two roles of the placenta.'), 6, stem=[Q17B], id='bio-2022-hl-q17-b-i'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Give an outline description of the birth process', 'hormones.'),
      [pt(S('Change in level of (named) hormone'), 3),
       anyn(S('Mucus plug falls out', 'umbilical cord is cut'), 3, 3)], 'bio-2-5', 'birth',
      SQ(27, 'Give an outline description of the birth process'), 12, stem=[Q17B], id='bio-2022-hl-q17-b-ii'),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'State one method of birth control.'),
      [pt(S('Condom or the (contraceptive) pill', 'any valid example'), 3)], 'bio-2-5', 'birth-control',
      SQ(27, 'State one method of birth control.'), 3, stem=[Q17B], id='bio-2022-hl-q17-b-iii-iv',
      decision=bundled('(b)(iii) and (iv)', '(iii), and (iv) is added')),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'Name the hormone responsible for milk production.'),
      [pt(S('*Prolactin'), 3)], 'bio-2-5', 'prolactin', SQ(27, 'Name the hormone responsible for milk production.'), 3,
      stem=[Q17B]),
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'State two biological benefits of breastfeeding.'),
      [anyn(S('Balanced supply of nutrients /', 'any correct benefit'), 2, 3)], 'bio-2-5', 'breastfeeding',
      SQ(27, 'State two biological benefits of breastfeeding.'), 6, stem=[Q17B], id='bio-2022-hl-q17-b-v'),
] + [
    T(f'17ci{n}', f'Q17(c)(i){n}', 'C', [_C(10, 'State the location where food is usually stored in a:'),
                                        item(10, n, what, 'usually stored in a:')],
      [row], 'bio-2-5', concept, SQ(28, 'State the location where food is usually stored in a:'), 3, stem=[Q17C],
      id='bio-2022-hl-q17-c-i' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, what, row, concept in [
        (1, 'monocoytledonous seed', pt(S('Monocotyledonous seed: *Endosperm'), 3), 'food-store-monocot'),
        (2, 'dicotyledonous seed', pt(S('Cotyledon (accept seed leaf)'), 3, label=S('Dicotyledonous seed:')),
         'food-store-dicot')]
] + [
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'Describe how seeds contribute to the formation of fruit.'),
      [pt(S('Produce growth regulators or named'), 3)], 'bio-2-5', 'seeds-and-fruit',
      SQ(28, 'Describe how seeds contribute to the formation of fruit.'), 3, stem=[Q17C], id='bio-2022-hl-q17-c-ii-iii',
      decision=bundled('(c)(ii) and (iii)', '(ii), and (iii) is added')),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Name one part of a flower from which a fruit may develop.'),
      [pt(S('Ovary (accept receptacle)'), 3)], 'bio-2-5', 'where-fruit-forms',
      SQ(28, 'Name one part of a flower from which a fruit may develop.'), 3, stem=[Q17C]),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Outline one role of genetics in fruit production.'),
      [pt(S('Seedless fruits or more advantageous traits (or described)'), 3)], 'bio-2-5', 'genetics-and-fruit',
      SQ(28, 'Outline one role of genetics in fruit production.'), 3, stem=[Q17C], id='bio-2022-hl-q17-c-iv'),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'Dispersal is where seeds are transferred away', 'advantages of seed dispersal.'),
      [anyn(S('Reduces competition /', 'better chance of survival'), 2, 3)], 'bio-2-5', 'seed-dispersal',
      SQ(28, 'Give two advantages of seed dispersal.'), 6, stem=[Q17C], id='bio-2022-hl-q17-c-v'),
] + [
    T(f'17cvi{n}', f'Q17(c)(vi){n}', 'C', [_C(10, 'Germination is the regrowth of a plant embryo.',
                                             'in germination:'), item(10, n, what, 'in germination:')],
      [row], 'bio-2-5', concept, SQ(28, 'Describe the roles of the following in germination:'), 3, stem=[Q17C],
      id='bio-2022-hl-q17-c-vi' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, what, row, concept in [
        (1, 'Digestion', pt(S('Produce soluble nutrients or make nutrients available'), 3, label=S('Digestion:')),
         'digestion-in-germination'),
        (2, 'Respiration', pt(S('Release of energy from food'), 3, label=S('Respiration:')),
         'respiration-in-germination')]
] + [
    T('17cvii', 'Q17(c)(vii)', 'C', _C(10, 'Many flowering plants can reproduce asexually.', 'flowering plants.'),
      [pt(S('Any named example'), 3, kind='criterion')], 'bio-2-5', 'asexual-reproduction-in-plants',
      SQ(28, 'Give one example of asexual reproduction'), 3, stem=[Q17C]),
] + [
    T(f'17di{n}', f'Q17(d)(i){n}', 'C', [_C(10, 'Name the period of the heart cycle when the cardiac muscle',
                                           'heart is:'), item(10, n, what, 'cardiac muscle of the heart is:')],
      [row], 'bio-2-6', concept, SQ(29, 'Name the period of the heart cycle'), 3, stem=[Q17D], fig='q17-heart-cycle',
      id='bio-2022-hl-q17-d-i' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, what, row, concept in [
        (1, 'Contracting', pt(S('*Systole'), 3, label=S('Contracting:')), 'systole'),
        (2, 'Not contracting', pt(S('*Diastole'), 3, label=S('Not contracting:')), 'diastole')]
] + [
    T('17dii', 'Q17(d)(ii)', 'C', _C(10, 'In which diagram, X or Y or Z, are the ventricles contracting?',
                                     'Explain how you know the ventricles are contracting.'),
      [pt(S('*Z'), 3), pt(S('(Ventricle) volumes are reduced', 'out of heart)'), 3)], 'bio-2-6', 'ventricular-systole',
      SQ(29, 'In which diagram, X, Y or Z, are the ventricles contracting?'), 6, stem=[Q17D], fig='q17-heart-cycle',
      id='bio-2022-hl-q17-d-ii-fig'),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'State the location of the sinoatrial (SA) node in the heart.'),
      [pt(S('(Wall of) right atrium'), 3)], 'bio-2-6', 'sa-node', SQ(29, 'State the location of the sinoatrial'), 3,
      stem=[Q17D], id='bio-2022-hl-q17-d-iii-iv',
      decision=bundled('(d)(iii) and (iv)', '(iii), and (iv) 1. and 2. are added')),
] + [
    T(f'17div{n}', f'Q17(d)(iv){n}', 'C', [_C(10, 'There is a two-circuit circulatory system in humans.',
                                             'Name the circuit to which:'), item(10, n, what, 'Name the circuit to which:')],
      [row], 'bio-2-6', concept, SQ(29, 'There is a two-circuit circulatory system'), 3, stem=[Q17D],
      decision=EACH_ITEM)
    for n, what, row, concept in [
        (1, 'the right ventricle pumps blood.', pt(S('*Pulmonary (circuit)'), 3), 'pulmonary-circuit'),
        (2, 'the left ventricle pumps blood.', pt(S('*Systemic (circuit)'), 3), 'systemic-circuit')]
] + [
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Each heartbeat creates two audible sounds.', 'What causes these sounds?'),
      [pt(S('Valves closing'), 3)], 'bio-2-6', 'heart-sounds', SQ(29, 'What causes these sounds?'), 3, stem=[Q17D],
      id='bio-2022-hl-q17-d-v'),
    T('17dvi', 'Q17(d)(vi)', 'C', _C(10, 'What is the function of the coronary (cardiac) artery?'),
      [pt(S('To supply heart (cardiac) muscle (or tissue or cells) with blood'), 3)], 'bio-2-6', 'coronary-artery',
      SQ(29, 'What is the function of the coronary (cardiac) artery?'), 3, stem=[Q17D], id='bio-2022-hl-q17-d-vi-vii',
      decision=bundled('(d)(vi) and (vii)', '(vi), and (vii) is added as two route cards')),
] + [
    T('17dvii', 'Q17(d)(vii)', 'C', _C(10, 'Describe the effect on the circulatory system of either one', 'exercise.'),
      [pt(S(start, end), 3)], 'bio-2-6', f'{route}-and-the-circulation', SQ(29, 'Describe the effect on the circulatory'),
      3, stem=[Q17D], route=route,
      decision='Smoking or exercise: the scheme prints a separate set of effects for each, so each is a route card.')
    for route, start, end in [('smoking', 'Increase heart rate or increase blood', 'pressure or any valid effect'),
                              ('exercise', 'Increase heart rate or strengthens', 'heart muscle or any valid effect')]
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-karyotype': ('038', 5, (105, 122, 490, 352), SEC, ['X', 'Y'],
                     'Photograph of a human karyotype: chromosomes in numbered pairs 1 to 22, then X and Y. Pair 21 '
                     'has three chromosomes; there are two X chromosomes and none above Y.', False),
    'q4-mitochondrion': ('038', 6, (138, 92, 457, 251), SEC, [],
                         'Transmission electron micrograph of a mitochondrion in section: an oval body with a double '
                         'outer membrane and many folded inner membranes across it.', False),
    'q6-graph': ('038', 8, (120, 104, 480, 298), SEC, [],
                 'Graph of Mass of lipid digested against Time: a solid line for Lipase and bile salts rises steeply '
                 'and levels off high; a dashed line for Lipase rises more slowly and stays below it.', False),
    'q7-virus': ('038', 9, (195, 96, 480, 262), SEC, ['A', 'X'],
                 'Diagram of a spherical virus with club-shaped projections all round its surface; an arrow labelled '
                 'A points to the coiled strand inside it. A boxed letter X stands to the right.', False),
    'q8-cells': ('038', 10, (412, 290, 538, 527), SEC, ['A', 'B', 'Z'],
                 'Two micrographs of stained cells. A (x400): a single irregular cell with a dark body inside, '
                 'labelled Z, and an arrow marking its width as 2 cm. B (x100): many long, regular, joined cells.',
                 False),
    'q9b-vi-1-question': ('038', 11, (108, 486, 541, 745), SEC, [],
                          'The printed question: (vi) On the axes below, sketch two graphs as described below: 1. '
                          'Using a solid line (a short solid line is printed), sketch the expected result at 25 °C. '
                          'Below, empty axes: Rate of photosynthesis against Light intensity or CO2 concentration.',
                          False, [(138, 522, 541, 553)]),
    'q9b-vi-2-question': ('038', 11, (108, 486, 541, 745), SEC, [],
                          'The printed question: (vi) On the axes below, sketch two graphs as described below: 2. '
                          'Using a dashed line (- - - - - -), sketch the expected result if the activity had been '
                          'carried out at 60 °C. Below, empty axes: Rate of photosynthesis against Light intensity or '
                          'CO2 concentration.', False, [(138, 504, 541, 521)]),
    'q12c-iii-question': ('040', 3, (108, 582, 541, 637), SEC, [],
                          'The printed passage and question: Global warming is occurring at an unprecented rate. This '
                          'is as a result of pollution of the atmosphere with greenhouse gases. (iii) Explain the '
                          'underlined term. The word pollution is underlined.', False),
    'q13-protein-synthesis': ('040', 4, (110, 108, 541, 358), SEC, ['J', 'K', 'L', 'M'],
                              'Diagram of a cell: inside Organelle J, a Chromosome and its Gene, an arrow for Process K '
                              'making Molecule L; Molecule L leaves through the organelle boundary into the Cytosol and '
                              'arrives at a body M, from which a chain labelled Protein grows. The Cell membrane is '
                              'labelled.', False),
    'q13c-i-question': ('040', 4, (80, 555, 541, 668), SEC, [],
                        'The printed passage and question: (c) In squash plants, the allele for white fruit (F) is '
                        'dominant to the allele for yellow fruit (f). The allele for disc-shaped fruit (D) is dominant '
                        'to the allele for spherical-shaped fruit (d). The genes that control fruit colour and fruit '
                        'shape are located on different chromosomes. A squash plant, homozygous dominant for both fruit '
                        'colour and shape, was crossed with a squash plant homozygous recessive for both. (i) Explain '
                        'the underlined terms. The words allele and homozygous are underlined.', False),
    'q14-photosynthesis': ('040', 5, (114, 189, 532, 388), SEC, ['X', 'Y', 'Z'],
                           'Diagram of the two stages of photosynthesis. Light energy and H2O enter Stage 1, which '
                           'gives off Molecule X. NADP+ and ADP + P pass from Stage 2 to Stage 1, and Molecule Y and '
                           'ATP pass back to Stage 2. A Gas enters Stage 2, which produces Molecule Z.', False),
    'q15-kidney': ('040', 6, (112, 147, 533, 400), SEC, ['A', 'B', 'C'],
                   'Two diagrams. Left: a kidney cut in half, arrow A to the outer layer, arrow B to the cone-shaped '
                   'regions inside, arrow C to the central space where the tube leaves. Right: an enlarged nephron '
                   'with the Glomerulus, PCT, Loop of Henle, DCT and a Capillary labelled.', False),
    'q15a-i-question': ('040', 6, (80, 55, 541, 88), SEC, [],
                        'The printed question: (a) Excretion is an important process in homeostasis in living '
                        'organisms. (i) Explain the underlined terms. The words Excretion and homeostasis are '
                        'underlined.', False),
    'q16-eye': ('040', 7, (164, 278, 472, 486), SEC, ['P', 'Q', 'R'],
                'Diagram of the human eye in section: P labels the oval body behind the pupil, Q the clear curved '
                'front layer, R the nerve leaving the back of the eye; the Retina, Blind spot, Iris and Pupil are '
                'labelled.', False),
    'q16-joint': ('040', 8, (226, 123, 432, 312), SEC, ['A', 'B'],
                  'Diagram of a synovial joint between two bones: A labels the band joining the bones on the outside, '
                  'B the smooth layers capping the bone ends; Compact bone and Spongy bone are labelled.', False),
    'q17a-ii-question': ('040', 9, (80, 85, 541, 342), SEC, [],
                         'The printed passage and question: (a) The photographs are of the two scientists credited '
                         'with the co-development of the theory of evolution by natural selection. One of the points '
                         'put forward by the theory of natural selecton is: There is variation among members of a '
                         'species and these variations are inherited. Variations are differences among members of the '
                         'same species. Mutations and meiosis contribute to these variations. (ii) Explain the three '
                         'underlined terms. The words evolution, species and inherited are underlined. Beside the '
                         'passage, photographs of two bearded elderly men.', False, [(108, 290, 541, 324)]),
    'q17-scientists': ('040', 9, (348, 85, 541, 215), SEC, [],
                       'Two black-and-white photographs of elderly bearded men: on the left a man with a long white '
                       'beard, on the right a man with a white beard seated at a desk.', False),
    'q17-heart-cycle': ('040', 10, (109, 355, 536, 503), SEC, ['X', 'Y', 'Z'],
                        'Three diagrams of the heart in section, X, Y and Z. In X, arrows show blood entering the atria '
                        'from above; in Y, arrows show blood passing down into the ventricles; in Z, arrows show blood '
                        'leaving the ventricles upwards into the arteries.', False),
}
