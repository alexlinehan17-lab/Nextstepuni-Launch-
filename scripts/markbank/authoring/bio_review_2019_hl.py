"""Biology 2019 Higher Level — reviewed task ledger, carded from the papers for the first time.

Independent visual sweep (2026-10-14), every page rendered and read:
  * LC025ALP038EV (Sections A and B), 12 pages: p1 cover, p2 instructions,
    p3-p8 Section A Questions 1-6, p9-p11 Section B Questions 7-9, p12 back
    cover ("Do not write on this page"). The 2019 booklet has no Section C
    answer pages: Section C was answered in a separate answerbook.
  * LC025ALP040EV (Section C), 8 pages: p1 cover, p2 instructions, p3-p8
    Questions 10-15 (p8 also carries the back-cover notice).
  * LC025ALP000EV (marking scheme, "V2"), 28 pages: p1 cover, p2 note, p3-p5
    introduction, cancelled and surplus answers, conventions and annotations,
    p6-p24 Questions 1-15, p25-p27 "Blank Page", p28 back cover.

The paper's shape: any five of Section A's six questions, any two of Section
B's three, any four of Section C's six; Q14 and Q15 are each any two of (a),
(b), (c), and Q14(b) is "notes on three of" five topics. Every printed
question is carded, including two parts the SEC itself withdrew (below).

Tariffs are the scheme's ordered splits, carded at their first rate: Q1 is
the best five of six at 4 (its (a) "2 + 2"); Q2-Q6 "4 + 2 + 2 + 2 + 2 + 2 +
6" over seven responses; every Section B (a) "4 + 2"; Q7(b) "4 + 2 + 2 + 2 +
2 + 2 + 2 + 8"; Q8(b)(ii)-(vii) and Q9(b)(i)-(v) "4 + 2 + 2 + 2 + 2 + 6",
beside drawings the scheme prices on their own (3 + 3). Section C prints a
mark per row; each Q14(b) topic is "4 + 3 + 3".

Q7(b)(iii) and (iv): the scheme's footnote says they were deemed outside the
range of the syllabus and not examinable, and their marks were credited to
every candidate who attempted Q7(b). First kept out of the bank (2026-10-14);
carded as printed since 2026-10-24 under Alex's rule that a printed ask is
never left out: each carries the scheme's printed "possible answer" at its
place on the Q7(b) ladder, with the footnote's effect as the row's note.

Printed choices the scheme marks differently per option are split into
routes: Q6(c) asthma or bronchitis, Q10(c)(ii) quadrat or transect, Q13(b)(iii)
fibroids or endometriosis, and Q14(b)(iii) phototropism, geotropism in the
root or geotropism in the shoot.
"""
from bio_review_lib import Q, SQ, S, M, pt, anyn, T, L

YEAR, LEVEL = 2019, 'hl'
REVIEWED_AT = '2026-10-14'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2019-hl-038-paper.pdf',
            'fileid': 'LC025ALP038EV.pdf',
            'sha256': 'bae9656e62f7955c71fc5903ff8d1799ff4e0dbd2d3219f61dfbade24110d218',
            'pages': 12},
    '040': {'path': 'examiner-reports/biology/papers/2019-hl-040-paper.pdf',
            'fileid': 'LC025ALP040EV.pdf',
            'sha256': '45f45b9faa113fb0b32bbc17cb8aed43565c611225a45061e24c7766fdd79b87',
            'pages': 8},
    'scheme': {'path': 'examiner-reports/biology/schemes/2019-hl.pdf',
               'fileid': 'LC025ALP000EV.pdf',
               'sha256': '635cd0de3b01f43bb55b2bffe6a0b3743ee7e659aaac4f1963b45c47f8dfd4a8',
               'pages': 28},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 12)}, 12: 'back-cover'},
    '040': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 9)}},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples', 5: 'conventions',
               **{p: 'marking' for p in range(6, 25)}, 25: 'blank', 26: 'blank', 27: 'blank', 28: 'back-cover'},
}


def _ladder(notation, **extra):
    steps = []
    for term in notation.split('+'):
        n, _, m = term.strip().partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **extra}


QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 7)}, **{n: 30 for n in range(7, 10)},
    **{n: 60 for n in range(10, 14)},
}
PART_TOTALS = {
    **{(n, 'a'): 9 for n in range(10, 14)}, **{(n, 'b'): 27 for n in range(10, 14)},
    **{(n, 'c'): 24 for n in range(10, 14)},
    (14, 'a'): 30, (14, 'c'): 30,   # Q14(b) is notes on any three of five topics at 10
    **{(15, x): 30 for x in 'abc'},
}
BEST_OF = {1: (5, 4)}
LADDERS = {
    **{q: _ladder('4 + 2 + 2 + 2 + 2 + 2 + 6') for q in range(2, 7)},
    **{(n, 'a'): _ladder('4 + 2') for n in (7, 8, 9)},
    (7, 'b'): _ladder('4 + 2 + 2 + 2 + 2 + 2 + 2 + 8'),
    (8, 'b'): _ladder('4 + 2 + 2 + 2 + 2 + 6', fixed={3: 2}),
    (9, 'b'): _ladder('4 + 2 + 2 + 2 + 2 + 6', fixed={3: 2}),
}
LADDER_EXEMPT = {'8bi', '9bvi'}

CHECKSUMS = {
    1: {4: 5, 2: 2},   # "5(4)": best five of six, (a) printed "2 + 2"
    **{q: {4: 7} for q in range(2, 7)},
    **{(n, 'a'): {4: 2} for n in (7, 8, 9)}, (7, 'b'): {4: 8},
    (8, 'b'): {3: 2, 4: 6}, (9, 'b'): {4: 6, 3: 2},
    (10, 'a'): {3: 3}, (10, 'b'): {3: 9}, (10, 'c'): {3: 8},
    (11, 'a'): {3: 3}, (11, 'b'): {3: 9}, (11, 'c'): {3: 8},
    (12, 'a'): {3: 3}, (12, 'b'): {3: 9}, (12, 'c'): {3: 8},
    (13, 'a'): {3: 3}, (13, 'b'): {6: 1, 1: 6, 3: 5}, (13, 'c'): {3: 6, 6: 1},
    (14, 'a'): {1: 6, 3: 8}, (14, 'b'): {4: 5, 3: 10}, (14, 'c'): {3: 10},
    (15, 'a'): {6: 1, 1: 6, 3: 6}, (15, 'b'): {3: 10}, (15, 'c'): {3: 9, 1: 3},
}

SCAN_PAGES = {'038': range(2, 12), '040': range(2, 9)}
SELECTION_SCAN = [
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'any five', 'Q1 best five of (a)-(f): each part is its own card; the best five make 20.'),
    ('038', 3, 'the following', 'Q1 parts list.'),
    ('038', 8, 'any three', 'Q6(b) "any three features": a bounded menu on one card.'),
    ('038', 8, 'or', 'Q6(b) "alveoli or their capillaries": one menu of both columns.'),
    ('038', 9, 'any two', 'Section B rubric repeated.'),
    ('038', 9, 'the following', 'Q7(a) lead-in: every reagent asked.'),
    ('038', 9, 'or', 'Q7(a)(ii) "Benedict’s (or Fehling’s) solution": either reagent; the same row.'),
    ('038', 10, 'the following', 'Q8(b) lead-in: every part asked.'),
    ('038', 11, 'the following', 'Q9(b) lead-in: every part asked.'),
    ('040', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('040', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('040', 3, 'any four', 'Section C rubric repeated.'),
    ('040', 3, 'or', 'Q10(b) passage: "decline or extinction".'),
    ('040', 3, 'both', 'Q10(b) passage: "Both common and black-headed gulls".'),
    ('040', 3, 'both', 'Q10(b) passage: "Both are considered".'),
    ('040', 3, 'both', 'Q10(b) passage: "kill both adults and chicks".'),
    ('040', 4, 'both', 'Q11(b) lead-in: "both transcription and translation".'),
    ('040', 4, 'the following', 'Q11(c)(i) lead-in: every term asked, one card per term.'),
    ('040', 4, 'both', 'Q11(c)(ii)1 "for both sex and haemophilia": both asked, one card.'),
    ('040', 5, 'or', 'Q12(c)(i) "A or B": the answer options.'),
    ('040', 6, 'the following', 'Q13 lead-in: every part asked.'),
    ('040', 6, 'the following', 'Q13(b)(i) "label the following parts": all six labels; one card.'),
    ('040', 6, 'the following', 'Q13(c)(iii) "each of the following": one card per numbered item.'),
    ('040', 7, 'any two', 'Q14 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 7, 'both', 'Q14(a)(iii) "both grey matter and white matter": one card per numbered item.'),
    ('040', 7, 'both', 'Q14(a)(vi) "both endocrine and exocrine function": one gland.'),
    ('040', 7, 'the following', 'Q14(b) "three of the following topics": each topic is its own card.'),
    ('040', 7, 'or', 'Q14(b)(iii) "phototropism or of geotropism": separate menus per option: ROUTES.'),
    ('040', 7, 'the following', 'Q14(c) lead-in: every part asked.'),
    ('040', 8, 'any two', 'Q15 "any two of (a), (b), (c)": whole-part choice; every part is carded.'),
    ('040', 8, 'the following', 'Q15(b) lead-in: every part asked.'),
    ('040', 8, 'the following', 'Q15(c) lead-in: every part asked.'),
    ('040', 8, 'the following', 'Q15(c)(iii) "label the following parts": all three labels; one card.'),
]

ROUTES = {
    'Q6(c)': ['asthma', 'bronchitis'],
    'Q10(c)(ii)': ['quadrat', 'transect'],
    'Q13(b)(iii)': ['fibroids', 'endometriosis'],
    'Q14(b)(iii)': ['phototropism', 'geotropism-in-root', 'geotropism-in-shoot'],
}

LAYOUT_CHECKS = [
    ('scheme', 10, item, ['Asthma', 'Bronchitis'], want)
    for item, want in [('Pet dander or allergens', 'Asthma'), ('Viruses or bacteria', 'Bronchitis'),
                       ('An inhaler (bronchodilator)', 'Asthma'), ('Cough medicine', 'Bronchitis')]
] + [
    ('scheme', 10, item, ['Alveoli', 'Capillaries'], want)
    for item, want in [('Membrane (or wall) is thin', 'Alveoli'), ('Large surface area/', 'Alveoli'),
                       ('Large numbers/', 'Alveoli'), ('Moist surface/', 'Alveoli'),
                       ('Wall is thin (or is 1 cell thick)/', 'Capillaries'), ('Close contact with alveoli/', 'Capillaries'),
                       ('Large number or (capillary) network', 'Capillaries'), ('large surface area', 'Capillaries')]
] + [
    ('scheme', 18, item, ['Fibroids', 'Endometriosis'], want)
    for item, want in [('Abnormal hormonal', 'Fibroids'), ('Menstrual blood flowing', 'Endometriosis')]
]

SEC = 'State Examinations Commission'
COMPRESSED = 'The scheme heads each answer with a compressed reprint of the ask.'
EACH_ITEM = 'A list the scheme prices entry by entry: one card per entry.'
WITHDRAWN = ('Not examinable: the SEC deemed Q7(b)(iii) and (iv) outside the range of the Biology syllabus and '
             'credited their marks to every candidate who attempted any part of Q7(b).')
WITHDRAWN_EVIDENCE = ('Scheme p11 footnote: "Candidate’s that attempted any part of Q7(b), were credited with the '
                      'marks assigned for parts (iii) and (iv) for these questions. These questions were deemed to be '
                      'outside the range of the Biology Syllabus and not examinable. The information presented here '
                      'are possible answers to the questions."')


# Alex's rule (2026-10-24): a part the SEC withdrew is still a printed ask, so it
# is carded as printed, with what the scheme prints for it and a factual note of
# the footnote's effect -- not kept out of the bank.
WITHDRAWN_NOTE = ('The SEC deemed this part outside the range of the Biology syllabus and not examinable: '
                  'every candidate who attempted any part of Q7(b) was credited with its marks. The scheme '
                  'prints this as a possible answer.')
WITHDRAWN_DECISION = ('Carded as printed with the scheme\'s possible answer and its place on the Q7(b) ladder; '
                      'the footnote\'s effect is the row\'s note. ' + WITHDRAWN_EVIDENCE)


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor, doc='040'):
    """One entry of a printed numbered list."""
    return Q(page, f'{n}.', end, doc=doc, after=anchor, br=True)


def at(page, q, *path_and_marker, why=COMPRESSED):
    *path, marker = path_and_marker
    return SQ(page, marker, path=[str(q), *path], paired=why, bare=True)


Q1 = _A(3, 'Answer any five of the following parts (a) to (f):')
Q2 = _A(4, 'In relation to the principles of experimentation:')
Q3 = _A(5, 'Organisation is one of the characteristics of life.', 'organisation of cells.')
Q4 = [_A(6, 'The photograph below is of plant cells undergoing different stages of mitosis.'),
      _A(6, 'The cells are not shown in any particular order.')]
Q5 = _A(7, 'Some typical human red blood cells are shown below.', 'They are disc shaped.')
Q6 = _A(8, 'The diagram shows microscopic detail of an alveolus and a capillary from the human lung.')
Q7A = _A(9, 'State a use of each of the following in the biology laboratory.')
Q8A = _A(10, 'Yeast cells produce alcohol (ethanol) in a process called fermentation.')
Q8B = _A(10, 'Answer the following in relation to a laboratory activity you carried out to prepare',
         'alcohol using yeast, and to show its presence.')
Q9A = _A(11, 'In the course of your practical studies you prepared and examined with a microscope a',
         'transverse section (T.S.) of a dicotyledonous (dicot) plant stem.')
Q9B = _A(11, 'Answer the following questions in relation to your preparation and microscopic',
         'examination of a transverse section of a dicotyledonous stem.')
Q10B = [_C(3, 'Invasive mammals have been shown to have a detrimental impact on island', 'kill both adults and chicks.'),
        _C(3, 'Adapted from www.invasivespeciesireland.com')]
Q11B = _C(4, 'Protein synthesis is a complex process, involving both transcription and translation,',
          'that occurs in all cells.')
Q11CII = _C(4, 'The diagram below shows the pattern of inheritance of haemophilia in a family.',
            'is sex‐linked and recessive.')
Q12B = [_C(5, '“The single most important property of enzymes', 'occurring in living organisms”'),
        _C(5, 'Adapted from “Enzyme Activity”')]
Q12C_LEAD = _C(5, 'Photosysthesis occurs in two stages, the light‐dependent stage and the', 'light‐independent (dark) stage.')
Q12C = [Q12C_LEAD, _C(5, 'Two structures found in plant cells are shown below.')]
Q13 = _C(6, 'Answer the following questions from your knowledge of human reproduction.')
Q13A = _C(6, 'Contraception can include natural, mechanical, and chemical methods.')
Q14AI = [_C(7, 'The diagram shows parts of the human central nervous system and some related', 'structures.'),
         _C(7, 'In your answer book, match each of the parts labelled A ‒ F to one of the names', 'from the list below.'),
         _C(7, 'cerebrum medulla oblongata pituitary gland cerebellum hypothalamus spinal cord', br=True)]
Q14B = _C(7, 'Write notes on three of the following topics:')
Q14C = _C(7, 'Answer the following questions from your knowledge of the human musculoskeletal', 'system.')
Q15B = _C(8, 'Answer the following questions from your knowledge of the human digestive system.')
Q15C = _C(8, 'Answer the following questions from your knowledge of sexual reproduction in', 'flowering plants.')
Q15CII = _C(8, 'A double fertilisation occurs in the embryo sac.')

F_LINE = 'F on usual location of fertilisation: Oviduct (Fallopian tube)'
# The scheme prints a solidus inside its last option ("enzyme returns to /
# original shape"): the option runs on to "can be reused", so it is cut at the
# solidus before it, not at its own.
HOW_ENZYMES_WORK = ('Active site complementary shape to substrate / Active site changes shape to',
                    'original shape or enzyme (or active site) can be reused')

RESISTANCE = ('(Antibiotic resistant bacteria) are not affected (by antibiotics) / Can be',
              'kill (or slow down the growth of) bacteria (or fungi or microorganisms)')

L_BRAIN = [L(x, S(name, page=19), False) for x, name in
           [('A', 'Cerebellum'), ('B', 'Cerebrum'), ('C', 'Pituitary gland'), ('D', 'Medulla oblongata'),
            ('E', 'Spinal cord'), ('F', 'Hypothalamus')]]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'State the two main reasons why food is required by all living organisms.'),
      [pt(S('Energy (source) or (cellular) respiration'), 2),
       pt(S('(Raw materials for) growth or (raw materials for) repair', 'repair (of tissue)'), 2)], 'bio-1-2',
      'why-food-is-needed', SQ(6, 'Two reasons why food necessary:'), 4, stem=[Q1]),
    T('1b', 'Q1(b)', 'A', _A(3, 'What is the ratio of hydrogen atoms to oxygen atoms in a carbohydrate?'),
      [pt(S('2:1'), 4)], 'bio-1-2', 'h-to-o-ratio', SQ(6, 'Ratio of H to O in carbohydrate:',
                                                        paired=COMPRESSED), 4, stem=[Q1]),
    T('1c', 'Q1(c)', 'A', _A(3, 'Give a structural role of lipids in cells.'),
      [pt(S('(Component of) membrane(s)'), 4)], 'bio-1-2', 'structural-role-of-lipids',
      SQ(6, 'Structural role of lipids in cells:'), 4, stem=[Q1]),
    T('1d', 'Q1(d)', 'A', _A(3, 'Give a metabolic role of lipids in cells.'),
      [pt(S('Energy (source or store)'), 4)], 'bio-1-2', 'metabolic-role-of-lipids',
      SQ(6, 'Metabolic role of lipids in cells:'), 4, stem=[Q1]),
    T('1e', 'Q1(e)', 'A', _A(3, 'Give an example of a fat‐soluble vitamin.'),
      [pt(S('A, D, E, K'), 4, note_sel=S('[allow letters or names]'))], 'bio-1-2', 'fat-soluble-vitamins',
      SQ(6, 'Fat-soluble vitamin:'), 4, stem=[Q1]),
    T('1f', 'Q1(f)', 'A', _A(3, 'Name a disorder due to a dietary deficiency of the vitamin referred to in (e).'),
      [pt(S('A = e.g. Night blindness', 'K = e.g. Bleeding (or easy bruising)'), 4)], 'bio-1-2',
      'vitamin-deficiency-disorders', SQ(6, 'Disorder matched to answer at (e):'), 4,
      stem=[Q1, M('(e)', 3), _A(3, 'Give an example of a fat‐soluble vitamin.')]),
    T('2a', 'Q2(a)', 'A', _A(4, 'What is meant by the term hypothesis?'),
      [pt(S('Proposed (or possible) explanation or an explanation of an observation or an educated guess or',
            'untested (or unproven) idea or prediction'), 4)], 'bio-u2', 'hypothesis', SQ(7, 'Hypothesis:'), 4,
      stem=[Q2]),
    T('2b', 'Q2(b)', 'A', _A(4, 'Explain what is meant by double‐blind testing.'),
      [pt(S('Neither the tester nor the subject knows who gets the drug (or who gets the placebo)'), 4)], 'bio-u2',
      'double-blind-testing', SQ(7, 'Double-blind testing:'), 4, stem=[Q2]),
    T('2c', 'Q2(c)', 'A', _A(4, 'Explain the necessity for random selection.'),
      [pt(S('Reduces bias or greater reliability or greater validity', 'or fair (test)'), 4)], 'bio-u2',
      'random-selection', SQ(7, 'Necessity for random selection:'), 4, stem=[Q2]),
    T('2d', 'Q2(d)', 'A', _A(4, 'Give two other features of good experimental design.'),
      [anyn(S('A control/ only one variable/'), 2, 4,
            note_sel=S('[do not allow random selection or double-blind testing]'))], 'bio-u2',
      'good-experimental-design', SQ(7, 'Other good experimental design features:'), 8, stem=[Q2]),
    T('2e', 'Q2(e)', 'A', _A(4, 'Where are the results of scientific research usually first published?'),
      [pt(S('A scientific journal (or publication or website) or named scientific journal'), 4)], 'bio-u2',
      'publishing-results', SQ(7, 'Where results of scientific research published:'), 4, stem=[Q2]),
    T('2f', 'Q2(f)', 'A', _A(4, 'Why is it important that scientists publish the results of their research?'),
      [pt(S('For peer review or so that others can learn', 'information made widely available'), 4)], 'bio-u2',
      'why-publish', SQ(7, 'Why important to publish research:'), 4, stem=[Q2]),
    T('3a', 'Q3(a)', 'A', _A(5, 'What is meant by the term tissue?'),
      [pt(S('(A group of) cells with the same function or (a group of) cells working together'), 4)], 'bio-1-3',
      'tissue', SQ(8, 'Tissue:'), 4, stem=[Q3]),
    T('3b', 'Q3(b)', 'A', _A(5, 'Name two types of animal tissue.'),
      [anyn(S('Epithelial (or epidermis)/ muscle/', 'ligament/'), 2, 4)], 'bio-1-3', 'animal-tissues',
      SQ(8, 'Animal tissues:', paired=COMPRESSED), 8, stem=[Q3]),
    T('3c', 'Q3(c)', 'A', _A(5, 'State how each of these tissue types is adapted to carry out its function.'),
      [pt(S('Correct adaptation matching named tissues'), 8, kind='criterion', units=[4, 4])], 'bio-1-3',
      'tissue-adaptations', SQ(8, 'How each at (b) adapted:', paired=COMPRESSED), 8,
      stem=[Q3, M('(b)', 5), _A(5, 'Name two types of animal tissue.')]),
    T('3d', 'Q3(d)', 'A', [_A(5, 'Stem cell research is an application of tissue culture.'),
                           _A(5, 'What is meant by the term tissue culture?')],
      [pt(S('Growth of cells on (or in) a medium or growth of cells in vitro'), 4,
          note_sel=S('[Allow growth of cells outside an organism'))], 'bio-1-3', 'tissue-culture',
      SQ(8, 'Tissue culture:'), 4, stem=[Q3]),
    T('3e', 'Q3(e)', 'A', _A(5, 'Give one other application of tissue culture.'),
      [anyn(S('Plant breeding/ micro-propagation or example/', 'antibody production/ replacement organs'), 1, 4,
            note_sel=S('[Do not allow any reference to stem cells]'))], 'bio-1-3', 'uses-of-tissue-culture',
      SQ(8, 'Another tissue culture application:'), 4, stem=[Q3]),
    T('4a', 'Q4(a)', 'A', _A(6, 'Which type of microscope is used in the school laboratory to observe cells like these?'),
      [pt(S('Light (microscope)'), 4)], 'bio-1-3', 'light-microscope', SQ(8, 'School laboratory microscope:',
                                                                         paired=COMPRESSED), 4,
      stem=Q4, fig='q4-mitosis'),
    T('4b', 'Q4(b)', 'A', _A(6, 'The first cell is in prophase. Give two observable events that happen during prophase.'),
      [anyn(S('Nuclear membrane disappears (or breaks down)/ spindle forms /', 'double stranded'), 2, 4)], 'bio-2-3',
      'prophase', SQ(8, 'Observable prophase events:'), 8, stem=Q4, fig='q4-mitosis'),
    T('4c', 'Q4(c)', 'A', _A(6, 'On the photograph, use the letter M to label a cell that is undergoing metaphase.'),
      [pt(S('Sixth cell from LH end'), 4, kind='criterion')], 'bio-2-3', 'metaphase', SQ(8, 'M on metaphase:'), 4,
      stem=Q4, fig='q4-mitosis'),
    T('4d', 'Q4(d)', 'A', _A(6, 'On the photograph, use the letter A to label a cell that is undergoing anaphase.'),
      [pt(S('Second cell from LH end'), 4, kind='criterion')], 'bio-2-3', 'anaphase', SQ(8, 'A on anaphase:'), 4,
      stem=Q4, fig='q4-mitosis'),
    T('4e', 'Q4(e)', 'A', [_A(6, 'After mitosis, the cell divides in two.'),
                           _A(6, 'This happens differently in animal cells and in plant cells.'),
                           _A(6, 'Describe what happens in animal cells and in plant cells during this stage.')],
      [pt(S('Cleavage (or furrow) or described'), 4, label=S('In animal cells:', 'In animal cells:')),
       pt(S('(Cell) plate or described'), 4, label=S('In plant cells:'))], 'bio-2-3', 'cytokinesis',
      at(8, 4, '(e)', why='The scheme sets its heading on the answer\'s own line.'), 8),
    T('5a', 'Q5(a)', 'A', _A(7, 'What word is used to describe the shape of the two faces of these cells?'),
      [pt(S('Concave or biconcave'), 4)], 'bio-2-6', 'biconcave', SQ(9, 'Word to describe shape of the two faces:'), 4,
      stem=[Q5], fig='q5-red-cells'),
    T('5b', 'Q5(b)', 'A', [_A(7, 'Red blood cells are wider than some capillaries.'),
                           _A(7, 'What feature of red blood cells allows them to pass through the narrow capillaries?')],
      [pt(S('Flexible or described'), 4)], 'bio-2-6', 'flexible-red-cells',
      SQ(9, 'Red blood cell feature to get through capillaries:'), 4, stem=[Q5], fig='q5-red-cells'),
    T('5c', 'Q5(c)', 'A', _A(7, 'Name the molecule in red blood cells that carries oxygen.'),
      [pt(S('Haemoglobin'), 4)], 'bio-2-6', 'haemoglobin', SQ(9, 'O2-carrying molecule in red blood cells:',
                                                             paired=COMPRESSED), 4, stem=[Q5], fig='q5-red-cells'),
    T('5d', 'Q5(d)', 'A', [_A(7, 'Human red blood cells live for about 120 days.'),
                           _A(7, 'Give a reason for this, based on the composition of these cells.')],
      [pt(S('No nucleus or no mitochondria or no organelles or cannot reproduce'), 4)], 'bio-2-6',
      'red-cell-lifespan', SQ(9, 'Reason for red blood cell limited lifespan:', paired=COMPRESSED), 4, stem=[Q5],
      fig='q5-red-cells'),
] + [
    T(f'5e{n}', f'Q5(e){n}', 'A', item(7, n, end, 'Give a location in the body where red blood cells are:', doc='038'),
      [pt(S(ans), 4)], 'bio-2-6', concept, SQ(9, sq), 4,
      stem=[Q5, _A(7, 'Give a location in the body where red blood cells are:')], fig='q5-red-cells',
      decision=EACH_ITEM)
    for n, end, ans, concept, sq in [(1, 'Produced.', '(Bone) marrow', 'where-red-cells-are-made',
                                      'Where red blood cells produced:'),
                                     (2, 'Usually broken down.', 'Liver or spleen', 'where-red-cells-are-broken-down',
                                      'Where red blood cells usually broken down:')]
] + [
    T('5f', 'Q5(f)', 'A', [_A(7, 'Red blood cells are transported in the blood plasma.'),
                           _A(7, 'Name the transport fluid in humans that does not contain red blood cells.')],
      [pt(S('Lymph'), 4)], 'bio-2-6', 'lymph', SQ(9, 'Human transport fluid not containing red blood cells:'), 4,
      stem=[Q5], fig='q5-red-cells'),
    T('6a', 'Q6(a)', 'A', _A(8, 'Name the blood vessel from which the capillary arises.'),
      [pt(S('Pulmonary artery (arteriole)'), 4)], 'bio-2-6', 'pulmonary-artery',
      SQ(10, 'Blood vessel that capillary arises from:'), 4, stem=[Q6], fig='q6-alveolus'),
    T('6b', 'Q6(b)', 'A', _A(8, 'Give any three features of alveoli or their capillaries that allow for efficient gas exchange.'),
      [anyn(None, 3, 4, options=[S(o, *e, piece=1) for o, *e in [
          ('Membrane (or wall) is thin (or is 1 cell thick)/',), ('Large surface area/',), ('Large numbers/',),
          ('Moist surface/',), ('Wall is thin (or is 1 cell thick)/',), ('Close contact with alveoli/',),
          ('Large number or (capillary) network or highly', 'branched/'), ('large surface area',)]])],
      'bio-2-6', 'gas-exchange-surfaces',
      SQ(10, 'Features for efficient gas exchange:', paired=COMPRESSED), 12, stem=[Q6], fig='q6-alveolus',
      decision='The scheme sets the features in two columns, alveoli and capillaries, each with its own "large '
               'surface area"; one menu of both, the alveoli column first (column membership layout-checked).'),
] + [
    T('6c', 'Q6(c)', 'A', _A(8, 'Name a disorder of the human breathing system and suggest how it is caused and treated.'),
      [pt(S(name), 4, label=S('Disorder:')), pt(S(*cause), 4, label=S('Cause:')),
       pt(S(*treat), 4, label=S('Treatment:'), **kw)], 'bio-2-6', f'{route}-cause-and-treatment',
      at(10, 6, '(c)', why='The scheme answers (c) in a table with no reprint of the ask.'), 12, route=route,
      decision='Asthma or bronchitis: the scheme prints a separate column of causes and treatments for each, so '
               'each is a route card.')
    for route, name, cause, treat, kw in [
        ('asthma', 'Asthma', ('Pet dander or allergens or', 'smoke or dust'), ('An inhaler (bronchodilator)',),
         {'note_sel': S('[allow named ones]')}),
        ('bronchitis', 'Bronchitis', ('Viruses or bacteria or smoke or', 'airborne particles'),
         ('Cough medicine or inhalers or', 'inflammatories or antibiotics'), {})]
] + [
    # ------------------------------------------------------------ Section B --
    T('7ai', 'Q7(a)(i)', 'B', _A(9, 'Biuret reagent (a solution containing copper sulfate and sodium hydroxide).'),
      [pt(S('(To test for) protein'), 4)], 'bio-1-2', 'use-of-biuret', SQ(11, 'Biuret:'), 4, stem=[Q7A]),
    T('7aii', 'Q7(a)(ii)', 'B', _A(9, 'Benedict’s (or Fehling’s) solution.'),
      [pt(S('(To test for) reducing sugar'), 4)], 'bio-1-2', 'use-of-benedicts', SQ(11, 'Benedict’s / Fehling’s:'), 4,
      stem=[Q7A]),
] + [
    T(f'7b{r}{n}', f'Q7(b)({r}){n}', 'B', item(9, n, end, anchor, doc='038'),
      [pt(S(*ans, **sk), 4, note=WITHDRAWN_NOTE if excl else None)], topic, concept,
      sq, 4, stem=[_A(9, anchor)], decision=EACH_ITEM + (' ' + WITHDRAWN_DECISION if excl else ''))
    for r, n, end, anchor, ans, sk, topic, concept, sq, excl in [
        ('i', 1, 'Place a coverslip over the cells?', 'When preparing a sample of cheek cells on a microscope slide',
         ('To prevent (the cells) from drying out or to protect the (objective) lens (from',
          'or to hold sample in place or easier to see'), {}, 'bio-1-3', 'coverslip', SQ(11, 'Why coverslip:'), False),
        ('i', 2, 'Apply methylene blue to the cells?', 'When preparing a sample of cheek cells on a microscope slide',
         ('To stain (the cells) or to make (the cells) easier to see',), {}, 'bio-1-3', 'methylene-blue',
         SQ(11, 'Why methylene blue:'), False),
        ('ii', 1, 'Washing‐up liquid?', 'When extracting DNA from plant tissue, why did you use:',
         ('Breakdown membrane',), {}, 'bio-1-2', 'washing-up-liquid', SQ(11, 'Why washing-up liquid:'), False),
        ('ii', 2, 'Freezer‐cold ethanol?', 'When extracting DNA from plant tissue, why did you use:',
         ('To precipitate (the DNA) or to make (the DNA) insoluble', 'or to make (the DNA) visible'), {}, 'bio-1-2',
         'freezer-cold-ethanol', SQ(11, 'Why freezer-cold ethanol:'), False),
        ('iii', 1, 'Carry out a serial dilution of an IAA solution?', 'When using seeds to investigate the effect of IAA',
         ('(To make solutions of) different concentrations (of IAA)',), {'after': '1(iii)'}, 'bio-2-4',
         'serial-dilution', SQ(11, 'Why serial dilution:', paired=COMPRESSED), True),
        ('iii', 2, 'Place the seeds on a grid in Petri dishes?', 'When using seeds to investigate the effect of IAA',
         ('To measure the growth (of root or shoot accurately)',), {'after': '1(iii)'}, 'bio-2-4', 'seed-grid',
         SQ(11, 'Why seeds on Petri dish grid:', paired=COMPRESSED), True),
        ('iv', 1, 'Why did you use Visking™tubing?', 'When carrying out an activity to investigate osmosis:',
         ('To act as a selectively permeable membrane or to mimic the plasma membrane',), {}, 'bio-2-6',
         'visking-tubing', SQ(11, 'Why Visking™ tubing:'), True),
        ('iv', 2, 'How did you know osmosis had taken place?', 'When carrying out an activity to investigate osmosis:',
         ('Mass of tubing increased (or decreased) or tubing got fuller (or less', 'full) or increased turgidity'), {},
         'bio-2-6', 'evidence-of-osmosis', SQ(11, 'How know osmosis has happened:', paired=COMPRESSED), True)]
] + [
    T('8ai', 'Q8(a)(i)', 'B', _A(10, 'Is oxygen necessary for this process?'),
      [pt(S('*No'), 4)], 'bio-2-2', 'fermentation-and-oxygen', SQ(12, 'Does fermentation need oxygen:'), 4,
      stem=[Q8A]),
    T('8aii', 'Q8(a)(ii)', 'B', _A(10, 'Where in the cell does this process take place?'),
      [pt(S('*Cytosol or *cytoplasm'), 4)], 'bio-2-2', 'where-fermentation-happens',
      SQ(12, 'Location of fermentation in cell:'), 4, stem=[Q8A]),
    T('8bi', 'Q8(b)(i)', 'B', _A(10, 'Draw a labelled diagram of the apparatus you used.'),
      [pt(S('Reaction vessel with liquid surface and anaerobic condition'), 3, kind='criterion'),
       anyn(S('Airlock or oil/ yeast/'), 1, 3)], 'bio-2-2', 'fermentation-apparatus',
      at(12, 8, '(b)', '(i)', why='The scheme prices the drawing and its label on their own, under "(b) (i)".'), 6,
      stem=[Q8B], decision='The drawing and its label are priced at 3 each beside the (b) ladder.'),
] + [
    T(f'8b{r}', f'Q8(b)({r})', 'B', _A(10, *ask), [pt(S(*ans), 4, **kw)], 'bio-2-2', concept, sq, 4, stem=[Q8B])
    for r, ask, ans, kw, concept, sq in [
        ('ii', ('From which substance did the yeast make the alcohol?',),
         ('Glucose or sugar or other named sugar [allow starch]',), {}, 'substrate-for-fermentation',
         SQ(12, 'Which substance alcohol made from:')),
        ('iii', ('What is the optimum temperature for this fermentation process?',),
         ('Any temperature or range within 20 °C – 35 °C',), {'kind': 'criterion'}, 'fermentation-temperature',
         SQ(12, 'Optimum temperature:')),
        ('iv', ('How did you maintain this temperature at a constant level for the duration of the', 'fermentation?'),
         ('Water bath or incubator',), {}, 'keeping-temperature-constant',
         SQ(12, 'How optimum temperature maintained:', paired=COMPRESSED)),
        ('v', ('How did you know when the fermentation was finished?',),
         ('No more gas (carbon dioxide) produced / no more bubbles',), {}, 'end-of-fermentation',
         SQ(12, 'How know fermentation finished:')),
        ('vi', ('How did you test for the presence of alcohol?',),
         ('Iodoform test or (potassium) iodide (or I-) and (sodium) hypochlorite (or ClO-)',), {}, 'testing-for-alcohol',
         SQ(12, 'Test for alcohol:')),
        ('vii', ('Give the colour of the positive result of the test.',), ('*Yellow',), {}, 'positive-iodoform-test',
         SQ(12, 'Positive colour:'))]
] + [
    T('9a', 'Q9(a)', 'B', _A(11, 'What is meant by the term dicotyledonous?'),
      [pt(S('Two'), 4), pt(S('Seed leaves'), 4)], 'bio-2-6', 'dicotyledonous', SQ(13, 'Dicotyledonous:'), 8,
      stem=[Q9A], decision='The scheme prices the definition as two responses on the "4 + 2" split.'),
] + [
    T(f'9b{r}', f'Q9(b)({r})', 'B', _A(11, *ask), rows, topic, concept, sq, total, stem=[Q9B])
    for r, ask, rows, topic, concept, sq, total in [
        ('i', ('Name the plant you used.',),
         [pt(S('Buttercup or sunflower or rose or ivy or busy lizzy or geranium or other named dicot'), 4)], 'bio-2-6',
         'a-dicot', SQ(13, 'Plant used:'), 4),
        ('ii', ('Why is it important to use a very thin section when examining the tissues in the', 'stem?'),
         [pt(S('To allow light to pass through (effectively or well) or to see (the cells) clearly'), 4)], 'bio-1-3',
         'thin-sections', SQ(13, 'Why thin section:'), 4),
        ('iii', ('Describe two steps you took to cut the stem safely.',),
         [anyn(S('Microtome or (backed or safety) blade or scalpel or sharp knife / stem held in pith (or',
                 'named support)/cut away from body'), 2, 4)], 'bio-2-6', 'cutting-safely',
         SQ(13, 'To cut stem safely:'), 8),
        ('iv', ('How did you transfer the section to the microscope slide?',),
         [pt(S('Paintbrush or forceps or tweezers or blade or finger'), 4)], 'bio-1-3', 'transferring-the-section',
         SQ(13, 'How section transferred to slide:'), 4),
        ('v', ('Name the part of the microscope you used to bring the section into a sharp', 'focus.'),
         [pt(S('Fine (or coarse) wheel (or knob or adjuster)'), 4)], 'bio-1-3', 'focusing',
         SQ(13, 'Part of microscope for sharp focus:'), 4)]
] + [
    T('9bvi', 'Q9(b)(vi)', 'B', _A(11, 'Draw a labelled diagram of the section that you observed under the microscope.'),
      [pt(S('Epidermis and vascular bundles in a ring'), 3, kind='criterion'),
       pt(S('Vascular (bundle or tissue) or xylem or phloem or dermal or ground'), 3)], 'bio-2-6',
      'drawing-a-dicot-stem', at(13, 9, '(vi)', why='The scheme prices the drawing and its label on their own.'), 6,
      stem=[Q9B], decision='The drawing and its label are priced at 3 each beside the (b) ladder.'),
    # ------------------------------------------------------------ Section C --
    T('10ai', 'Q10(a)(i)', 'C', _C(3, 'What is the importance in nature of recycling elements such as carbon and nitrogen?'),
      [pt(S('To return (elements) to environment or so that (elements) can be reused (by', 'or finite amount'), 3)],
      'bio-3-2', 'why-recycle-elements', SQ(14, 'Importance of recycling:', paired=COMPRESSED), 3),
    T('10aii', 'Q10(a)(ii)', 'C', _C(3, 'Name two of the types of bacteria that play a role in the nitrogen cycle.'),
      [anyn(S('Nitrogen fixing/ nitrifying/ denitrifying/ decomposers or saprophytes'), 2, 3)], 'bio-3-2',
      'nitrogen-cycle-bacteria', SQ(14, 'Bacterial types in N-cycle:', paired=COMPRESSED), 6),
] + [
    T(f'10bi{n}', f'Q10(b)(i){n}', 'C', [_C(3, 'Explain what is meant by the terms'), item(3, n, end, 'Explain what is meant by the terms')],
      [pt(S(*ans), 3)], 'bio-3-1', concept, SQ(14, sq), 3, stem=Q10B, decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'Predation', ('Catching (or hunting) and killing and eating another organism',), 'predation',
         '1. Predation:'),
        (2, 'Conservation (of species).', ('Management of the environment (or of ecosystem or of habitat) or management of',
                                           'or prevention of extinction'), 'conservation', '2. Conservation (of species):')]
] + [
    T(f'10b{r}', f'Q10(b)({r})', 'C', _C(3, *ask), [pt(S(*ans), 3)], 'bio-3-1', concept, SQ(14, sq, paired=COMPRESSED), 3,
      stem=Q10B)
    for r, ask, ans, concept, sq in [
        ('ii', ('Suggest why the mink has become a successful predator of the gulls.',),
         ('Mink have adaptations suitable (for catching gulls) or example or can kill both adults',
          'never encountered mink before or lack of competition'), 'mink-as-predator', 'Why mink successful predator'),
        ('iii', ('Mink are omnivores. Why is this an advantage when mink invade an island?',),
         ('They can benefit from both animal and plant matter as food or able to survive from a', 'greater range of food'),
         'omnivory', 'Why omnivory advantageous to mink:'),
        ('iv', ('Other than predation, suggest a way in which the mink could cause a decline in', 'the populations of these gulls.'),
         ('Introduce disease or introduce a parasite or eat the food that gulls normally eat or', 'disturbance'),
         'mink-and-gull-decline', 'Another way mink could cause gull population decline:'),
        ('v', ('Suggest another impact on food chains in this ecosystem caused by the presence', 'of mink on these islands.'),
         ('Could lead to an overpopulation of the gull’s prey or overpopulation of primary',
          'consumers or the population of producers could decline or decline in other predators'), 'mink-and-food-chains',
         'Another food chain impact caused by mink:')]
] + [
    T('10bvi', 'Q10(b)(vi)', 'C', _C(3, 'Sketch and label a graph to show the typical relationship between the',
                                     'populations of a predator and its prey.'),
      [pt(S('Two curves with indication of a repeating cycle'), 3, kind='criterion'),
       pt(S('Predator showing lower peaks or predator curve showing time lag [Either',
            'predator or prey line must be labelled for this point]'), 3, kind='criterion'),
       pt(S('Time on horizontal axis and Population on vertical axis'), 3, kind='criterion')], 'bio-3-1',
      'predator-prey-graph', SQ(14, 'Predator-prey graph:'), 9),
] + [
    T(f'10ci{n}', f'Q10(c)(i){n}', 'C', [_C(3, 'From your knowledge of ecological surveys, explain the meaning of the terms:'),
                                       item(3, n, end, 'explain the meaning of the terms:')],
      [pt(S(*ans), 3)], 'bio-3-1', concept, SQ(15, sq, paired=COMPRESSED) if n == 1 else SQ(15, sq), 3,
      decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'Quantitative', ('Number of (or amount of or measurement of) organisms (or', 'abiotic factor'),
         'quantitative-survey', 'Quantitative:'),
        (2, 'Qualitative.', ('Presence of (or absence) an organism (or species or plant or', 'animal)'),
         'qualitative-survey', 'Qualitative:')]
] + [
    T('10cii', 'Q10(c)(ii)', 'C', [_C(3, 'In the course of your ecological studies you investigated an ecosystem.'),
                                   _C(3, 'Name this ecosystem and describe how you conducted a quantitative survey of',
                                      'flora present in it.')],
      [pt(S('Named ecosystem'), 3, kind='criterion'), anyn(S(*menu), 3, 3)], 'bio-3-1', f'{route}-survey',
      SQ(15, 'Quantitative survey of ecosystem flora:'), 12, route=route,
      decision='Quadrat or transect: the scheme prints a separate menu of steps for each, joined by "OR", so each '
               'is a route card.')
    for route, menu in [('quadrat', ('Quadrat/ Random (sample)/ how random/repeat a number of times/ count (or',
                                     'record or take average or note)')),
                        ('transect', ('Transect/ select starting position/ why selected/ (survey) regular points/count',
                                      '(or record or note)'))]
] + [
    T('10ciii', 'Q10(c)(iii)', 'C', _C(3, 'How did you present the results of your survey?'),
      [pt(S('Table or chart or graph'), 3)], 'bio-3-1', 'presenting-results', SQ(15, 'Presentation of results:', paired=COMPRESSED), 3),
    T('10civ', 'Q10(c)(iv)', 'C', _C(3, 'Suggest a possible source of error in your survey.'),
      [pt(S('Not random or sample too small or plant misidentified or miscounting or', 'Miscalculating'), 3)], 'bio-3-1',
      'survey-errors', SQ(15, 'Possible source of error:'), 3),
    T('11ai', 'Q11(a)(i)', 'C', _C(4, 'Name the sugar present in DNA.'),
      [pt(S('*Deoxyribose'), 3)], 'bio-1-2', 'deoxyribose', SQ(16, 'Sugar in DNA:'), 3),
    T('11aii', 'Q11(a)(ii)', 'C', _C(4, 'Other than the sugar, give two structural differences between DNA and RNA.'),
      [pt(S('DNA is double-stranded or RNA is single-stranded'), 3), pt(S('DNA has Thymine or RNA has Uracil'), 3)],
      'bio-1-2', 'dna-and-rna', SQ(16, 'Two other structural differences:'), 6),
    T('11bi', 'Q11(b)(i)', 'C', _C(4, 'Where does transcription occur in animal and plant cells?'),
      [pt(S('*Nucleus'), 3)], 'bio-2-3', 'where-transcription-happens',
      SQ(16, 'Location of transcription in animal and plant cells:'), 3, stem=[Q11B]),
    T('11bii', 'Q11(b)(ii)', 'C', _C(4, 'Where precisely in the cell does translation occur?'),
      [pt(S('*Ribosome'), 3)], 'bio-2-3', 'where-translation-happens', SQ(16, 'Where translation occurs:'), 3,
      stem=[Q11B]),
    T('11biii', 'Q11(b)(iii)', 'C', _C(4, 'Name the three types of RNA involved in protein synthesis.'),
      [pt(S('Messenger RNA (or mRNA)'), 3), pt(S('Ribosomal RNA (or rRNA)'), 3), pt(S('Transfer RNA (or tRNA)'), 3)],
      'bio-2-3', 'types-of-rna', SQ(16, 'Three RNAs in protein synthesis:'), 9, stem=[Q11B]),
    T('11biv', 'Q11(b)(iv)', 'C', _C(4, 'Describe the events that occur during translation, leading to the formation of a',
                                     'functional protein.'),
      [anyn(S('mRNA (transcribed DNA code) goes to a ribosome / tRNA molecules bring amino',
              'mention of start (or stop) codon'), 4, 3)], 'bio-2-3', 'translation', SQ(16, 'Translation events:', paired=COMPRESSED), 12,
      stem=[Q11B]),
] + [
    T(f'11ci{n}', f'Q11(c)(i){n}', 'C', [_C(4, 'Explain the following terms used in genetics:'),
                                       item(4, n, end, 'Explain the following terms used in genetics:')],
      [pt(S(*ans, after=after), 3)], 'bio-1-4', concept, SQ(16, sq, sq), 3, decision=EACH_ITEM)
    for n, end, ans, after, concept, sq in [
        (1, 'Sex linkage', ('A gene (or genes) present on the X (or Y, or sex) chromosome',), None, 'sex-linkage',
         '1. Sex linkage:'),
        (2, 'Heterozygous', ('When two alleles (for a trait) are different or alleles for a trait are different or',
                             'dominant and recessive alleles (or genes) present (for a trait)'), None, 'heterozygous',
         '2. Heterozygous:'),
        (3, 'Genotype.', ('The genetic make-up or the genes present',), None, 'genotype', '3. Genotype:')]
] + [
    T('11cii1', 'Q11(c)(ii)1', 'C', item(4, 1, 'for both sex and haemophilia?', 'is sex‐linked and recessive.'),
      [pt(S('1. XNXn'), 3), pt(S('2. XNY'), 3)], 'bio-1-4', 'parents-genotypes',
      SQ(16, 'Parents’ genotypes for both sex and haemophilia:'), 6, stem=[Q11CII], fig='q11-pedigree',
      decision=EACH_ITEM),
    T('11cii2', 'Q11(c)(ii)2', 'C', [_C(4, '• If person 7 has a carrier daughter', 'of the daughter’s father.', br=True),
                                     _C(4, '• What was the chance of that couple having a carrier daughter?', br=True)],
      [pt(S('Phenotype: (Male) haemophiliac', page=17), 3), pt(S('Genotype: XnY', page=17), 3),
       pt(S('(From all possible daughters:) 100% or (from all possible children:) 50%', page=17), 3)], 'bio-1-4',
      'daughters-father', SQ(16, 'Phenotype and full genotype of daughter’s father:'), 9,
      stem=[Q11CII], fig='q11-pedigree', decision=EACH_ITEM),
    T('12ai', 'Q12(a)(i)', 'C', _C(5, 'What is meant by the term metabolism?'),
      [pt(S('(All) the chemical reactions in an organism (or in cells or in the body)'), 3)], 'bio-1-1', 'metabolism',
      SQ(17, 'Metabolism:'), 3),
    T('12aii', 'Q12(a)(ii)', 'C', _C(5, 'Give an example of one anabolic reaction and one catabolic reaction in animals.'),
      [pt(S('Protein synthesis or DNA replication (synthesis) or other described'), 3,
          label=S('Anabolic reaction in animals:')),
       pt(S('Respiration or digestion or other described'), 3, label=S('Catabolic reaction in animals:'))], 'bio-1-2',
      'anabolic-and-catabolic', at(17, 12, '(a)', '(ii)', why='The scheme heads each of the two answers separately.'), 6),
    T('12bi', 'Q12(b)(i)', 'C', _C(5, 'What is an enzyme?'),
      [pt(S('Biological catalyst or protein catalyst'), 3)], 'bio-2-1', 'enzyme', SQ(17, 'Enzyme is:'), 3, stem=Q12B),
    T('12bii', 'Q12(b)(ii)', 'C', _C(5, 'Which type of biomolecule are enzymes?'),
      [pt(S('*Protein'), 3)], 'bio-2-1', 'enzymes-are-proteins', SQ(17, 'Enzymes are:', paired=COMPRESSED), 3,
      stem=Q12B),
    T('12biii', 'Q12(b)(iii)', 'C', _C(5, 'Name two factors that affect enzyme action.'),
      [anyn(S('Temperature / pH'), 2, 3)], 'bio-2-1', 'factors-affecting-enzymes',
      SQ(17, 'Factors that affect enzyme action:'), 6, stem=Q12B),
    T('12biv', 'Q12(b)(iv)', 'C', _C(5, 'What is meant by the term specificity in relation to enzyme activity.'),
      [pt(S('(An enzyme) can act on only one (or on a particular or a certain) substrate',
            '[allow food type for substrate]'), 3)],
      'bio-2-1', 'specificity', SQ(17, 'Specificity:'), 3, stem=Q12B),
    T('12bv', 'Q12(b)(v)', 'C', _C(5, 'Name the part of an enzyme responsible for its specificity.'),
      [pt(S('*Active site'), 3)], 'bio-2-1', 'active-site', SQ(17, 'Part of enzyme responsible for specificity'), 3,
      stem=Q12B),
    T('12bvi', 'Q12(b)(vi)', 'C', _C(5, 'Give a detailed account of how enzymes work.'),
      [anyn(None, 3, 3, options=[S(*HOW_ENZYMES_WORK, piece=n) for n in (1, 2, 3, 4)]
            + [S(*HOW_ENZYMES_WORK, piece=2, psep='released / ')])], 'bio-2-1',
      'how-enzymes-work', SQ(17, 'How enzymes work:', paired=COMPRESSED), 9, stem=Q12B),
    T('12ci', 'Q12(c)(i)', 'C', _C(5, 'In which of the two structures, A or B, does photosynthesis occur?'),
      [pt(S('*B'), 3)], 'bio-2-2', 'chloroplast', SQ(18, 'Photosynthesis in A or B:'), 3, stem=Q12C,
      fig='q12-organelles'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(5, 'Give a balanced chemical equation to summarise the process of photosynthesis.'),
      [pt(S('6CO2 + 6H2O → C6H12O6 + 6O2'), 6, units=[3, 3])], 'bio-2-2', 'photosynthesis-equation',
      SQ(18, 'Balanced photosynthesis equation:'), 6, stem=[Q12C_LEAD],
      decision='The scheme prints the equation once at "3 + 3": one row worth both marks.'),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(5, 'Name two products of the light‐dependent stage of photosynthesis.'),
      [anyn(S('ATP/ NADPH or protons (or H+ or H ions) or electrons)/ oxygen'), 2, 3)], 'bio-2-2',
      'light-stage-products', SQ(18, 'Products of light dependent stage:'), 6, stem=[Q12C_LEAD]),
    T('12civ', 'Q12(c)(iv)', 'C', _C(5, 'Some of the products of the light‐dependent stage are used in the',
                                     'Outline the events of the light‐independent stage.'),
      [pt(S('ATP to ADP (+ P) or ATP supplies energy'), 3),
       pt(S('NADPH to NADP or NADPH provides electrons or NADPH provides H or', 'NADPH provides H+ (or H ions or protons)'), 3),
       pt(S('CO2 converted to glucose (or other named carbohydrate)'), 3)], 'bio-2-2', 'dark-stage',
      SQ(18, 'Events of light-independent stage:'), 9, stem=[Q12C_LEAD]),
] + [
    T(f'13a-{slug}', 'Q13(a)', 'C', _C(6, 'Give one example of each of the above types of contraception.'),
      [pt(S(*ans), 3)], 'bio-2-5', f'{slug}-contraception',
      SQ(18, f'{name}:', paired=COMPRESSED) if slug != 'natural' else SQ(18, 'Natural:', paired=COMPRESSED), 3,
      stem=[Q13, Q13A], item=(slug, name), decision=EACH_ITEM)
    for slug, name, ans in [('natural', 'Natural', ('Withdrawal or abstinence or rhythm',)),
                            ('mechanical', 'Mechanical', ('Condom or diaphragm or coil (or IUD) or vasectomy or tube', 'ligation')),
                            ('chemical', 'Chemical', ('Pill or hormonal or vaginal ring or spermicide or implant',))]
] + [
    T('13bi', 'Q13(b)(i)', 'C', [_C(6, 'Draw a large diagram of the human female reproductive system.'),
                                 _C(6, 'On your diagram, label the following parts.'),
                                 _C(6, 'oviduct (Fallopian tube) cervix ovary vagina uterus endometrium', br=True)],
      [pt(S('Ovaries + oviducts + uterus + vagina'), 6, kind='criterion', note_sel=S('6, 3, 0')),
       anyn(S('Oviduct (Fallopian tube)/ cervix/ ovary/ vagina/ uterus/ endometrium'), 6, 1)], 'bio-2-5',
      'drawing-the-female-system', SQ(18, 'Drawing:'), 12, stem=[Q13]),
    T('13bii', 'Q13(b)(ii)', 'C', [_C(6, 'On your diagram,', after='(ii)'), _C(6, 'use the letter M to label the site of meiosis,'),
                                   _C(6, 'use the letter F to label the usual site of fertilisation.')],
      [pt(S('M on location of meiosis: Ovary'), 3),
       pt(S(F_LINE, piece=2, psep=': '), 3, label=S(F_LINE, piece=1, psep=': '))], 'bio-2-5', 'meiosis-and-fertilisation-sites',
      at(18, 13, '(b)', '(ii)', why='The scheme sets each heading on its answer\'s line.'), 6, stem=[Q13]),
] + [
    T('13biii', 'Q13(b)(iii)', 'C', [_C(6, 'Name a human female menstrual disorder.'), _C(6, 'For this disorder give:'),
                                     item(6, 1, 'A possible cause', 'For this disorder give:'),
                                     item(6, 2, 'A method of treatment.', 'For this disorder give:')],
      [pt(S(name), 3), pt(S(*cause), 3, label=S('1. Cause:')),
       pt(S('Surgery or HRT', nth=nth), 3, label=S('2. Treatment'))], 'bio-2-5', f'{route}-cause-and-treatment',
      SQ(18, 'Menstrual disorder:'), 9, stem=[Q13], route=route,
      decision='Fibroids or endometriosis: the scheme prints a separate column for each, so each is a route card.')
    for route, name, cause, nth in [('fibroids', 'Fibroids', ('Abnormal hormonal', 'response or genetic'), 1),
                                    ('endometriosis', 'Endometriosis', ('Menstrual blood flowing', 'into oviduct or genetic'), 2)]
] + [
    T('13ci', 'Q13(c)(i)', 'C', _C(6, 'What is meant by the term implantation?'),
      [pt(S('Embedding (or attaching) (of the fertilised egg) (in)to the endometrium (or', 'lining of uterus)'), 3)],
      'bio-2-5', 'implantation', SQ(19, 'Implantation:'), 3),
    T('13cii', 'Q13(c)(ii)', 'C', _C(6, 'Name, in the correct order, the developmental stages from the fertilised egg',
                                     'to implantation.'),
      [pt(S('1. Morula', '2. Blastocyst'), 6, note_sel=S('[must be in correct order]'))], 'bio-2-5',
      'stages-before-implantation', SQ(19, 'Developmental stages:'), 6,
      decision='One row priced "6, 3, 0": both stages in order.'),
] + [
    T(f'13ciii{n}', f'Q13(c)(iii){n}', 'C', item(6, n, end, 'after implantation has taken'),
      [pt(S(ans, after=after), 3)], 'bio-2-5', concept, SQ(19, sq, sq), 3,
      stem=[_C(6, 'Outline what happens to each of the following after implantation has taken', 'place:')],
      decision=EACH_ITEM)
    for n, end, ans, after, concept, sq in [
        (1, 'The level of the hormone progesterone in the blood', 'Increases', None, 'progesterone-after-implantation',
         '1. Progesterone level:'),
        (2, 'The endometrium.', 'Is maintained or thickens', None, 'endometrium-after-implantation',
         '2. Endometrium:')]
] + [
    T('13civ', 'Q13(c)(iv)', 'C', [_C(6, 'Embryo cells organise into three germ layers.'), _C(6, 'Name each of these layers.')],
      [pt(S('*Ectoderm'), 3), pt(S('*Mesoderm'), 3), pt(S('*Endoderm'), 3)], 'bio-2-5', 'germ-layers',
      SQ(19, 'Embryo germ layers:'), 9),
] + [
    T(f'14ai-{x.lower()}', 'Q14(a)(i)', 'C', Q14AI, [pt(S(name, after='CNS parts:'), 1)], 'bio-2-4',
      f'brain-part-{x.lower()}', SQ(19, 'CNS parts:', paired=COMPRESSED), 1, qfig='q14a-i', labels=asked(L_BRAIN, x),
      item=(x.lower(), x), decision=EACH_ITEM + ' The names to choose from are printed as a spaced row, so the ask is '
                                                'shown as the question\'s own print.')
    for x, name in [('A', 'Cerebellum'), ('B', 'Cerebrum'), ('C', 'Pituitary gland'), ('D', 'Medulla oblongata'),
                    ('E', 'Spinal cord'), ('F', 'Hypothalamus')]
] + [
    T(f'14aii{n}', f'Q14(a)(ii){n}', 'C', item(7, n, end, '(ii)' if n == 1 else 'Give a function of the medulla oblongata.'),
      [pt(S(*ans), 3)], 'bio-2-4', concept, SQ(19, sq), 3, decision=EACH_ITEM)
    for n, end, ans, concept, sq in [
        (1, 'Give a function of the medulla oblongata.',
         ('Controls (or regulates) involuntary actions', 'or coughing or swallowing or blood pressure or vomiting)'),
         'medulla-oblongata', '1. Medulla oblongata function:'),
        (2, 'Give a function of the cerebellum.',
         ('Controls (or regulates) voluntary movements', 'muscle movements or speech) or coordination'), 'cerebellum',
         '2. Cerebellum function:')]
] + [
    T(f'14aiii{n}', f'Q14(a)(iii){n}', 'C', item(7, n, end, 'The brain is composed of both grey matter and white matter.'),
      [pt(S(ans), 3)], 'bio-2-4', concept, SQ(20, sq), 3,
      stem=[_C(7, 'The brain is composed of both grey matter and white matter.')], decision=EACH_ITEM)
    for n, end, ans, concept, sq in [(1, 'Why is grey matter so called?', 'Composed of cell bodies', 'grey-matter',
                                      '1. Grey matter:'),
                                     (2, 'Why is white matter so called?', 'Composed of myelin or composed of axons',
                                      'white-matter', '2. White matter:')]
] + [
    T('14aiv', 'Q14(a)(iv)', 'C', _C(7, 'Endocrine glands produce hormones. What is meant by the term endocrine?'),
      [pt(S('Ductless or secretes directly into blood (or into lymph)'), 3)], 'bio-2-4', 'endocrine',
      SQ(20, 'Endocrine:'), 3),
] + [
    T(f'14av{n}', f'Q14(a)(v){n}', 'C', item(7, n, end, 'The pituitary gland is an example of an endocrine gland.'),
      [pt(S(*ans), 3, **kw)], 'bio-2-4', concept, SQ(20, sq), 3,
      stem=[_C(7, 'The pituitary gland is an example of an endocrine gland.')] + extra, decision=EACH_ITEM)
    for n, end, ans, kw, concept, sq, extra in [
        (1, 'Name a hormone secreted by the pituitary gland.',
         ('ACTH or FSH or GH or LH or TSH or ADH (vasopressin) or oxytocin or prolactin', 'or MSH'), {},
         'pituitary-hormones', '1. Hormone secreted by the pituitary:', []),
        (2, 'Give a function of this hormone in the human body.', ('Correct matching function',), {'kind': 'criterion'},
         'function-of-a-pituitary-hormone', '2. Function of named hormone:',
         [item(7, 1, 'Name a hormone secreted by the pituitary gland.',
               'The pituitary gland is an example of an endocrine gland.')])]
] + [
    T('14avi', 'Q14(a)(vi)', 'C', _C(7, 'Name one gland in the human body that has both endocrine and exocrine function.'),
      [pt(S('Pancreas or testis or ovary or liver or kidney'), 3)], 'bio-2-4', 'endocrine-and-exocrine',
      SQ(20, 'Gland with both endocrine and exocrine function'), 3),
] + [
    T('14bii', 'Q14(b)(ii)', 'C', _C(7, 'Antibiotic resistance in bacteria.'),
      [anyn(None, 3, 4, steps=[4, 3, 3], options=[S(*RESISTANCE, page=20, piece=n) for n in (1, 2, 3)]
            + [S(*RESISTANCE, page=20, piece=[2, 1], psep=['change) / ', '/ resistant']),
               S(*RESISTANCE, page=20, piece=6), S(*RESISTANCE, page=20, piece=9)])],
      'bio-3-2', 'antibiotic-resistance', SQ(20, 'Antibiotic resistance in bacteria:'), 10, stem=[Q14B],
      decision='The scheme prints "other bacteria/ resistant population (or example)" twice in a row; the menu '
               'carries it once. "acquired by bacteria from / other bacteria" is one option, cut at the solidus '
               'before it, not at its own.'),
] + [
    T(f'14b{r}', f'Q14(b)({r})', 'C', _C(7, topic_line), [anyn(S(*menu, page=pg), 3, 4, steps=[4, 3, 3])], topic,
      concept, SQ(pg, sq), 10, stem=[Q14B])
    for r, topic_line, menu, pg, topic, concept, sq in [
        ('i', 'Vaccination.', ('A non-harmful (or attenuated or weakened or dead) dose of the pathogen',
                               'spread of disease'), 20, 'bio-2-4', 'vaccination', 'Vaccination:'),
        ('iv', 'Batch food processing.', ('Carried out in a bioreactor/ Certain amount of micro-organisms (or',
                                          'through all stages/ Product is removed (at the end of the process)'),
         21, 'bio-3-2', 'batch-processing', 'Batch processing:'),
        ('v', 'The sounds created during the cardiac cycle.', ('The sounds are ‘lub’ + ‘dub’/ Caused by valves closing/',
                                                              'sound'),
         21, 'bio-2-6', 'heart-sounds', 'The sounds created during the cardiac cycle:')]
] + [
    T('14biii', 'Q14(b)(iii)', 'C', _C(7, 'The mechanism of phototropism or of geotropism in plants.'),
      [anyn(S(*menu), 3, 4, steps=[4, 3, 3])], 'bio-2-4', f'{route}-mechanism',
      SQ(21, sq), 10, stem=[Q14B], route=route,
      decision='Phototropism, or geotropism in the root or in the shoot: the scheme prints a separate menu for each, '
               'joined by "OR", so each is a route card.')
    for route, menu, sq in [
        ('phototropism', ('Auxin produced in shoot tip (or meristem) / Plant shoot exposed to (more)',
                          'grows (or bends) towards the light'), 'Mechanism of phototropism:'),
        ('geotropism-in-root', ('Auxin produced in root tip (or in meristem) / (More) auxin on the lower',
                                '(Root) growth (or bend) downwards'), 'Mechanism of geotropism: in root'),
        ('geotropism-in-shoot', ('Auxin produced in shoot tip (or in meristem) / (More) auxin on the lower',
                                 '(Shoot) grow (or bends) upwards'), 'Mechanism of geotropism: in shoot')]
] + [
    T('14ci', 'Q14(c)(i)', 'C', _C(7, 'Give two functions of the skeleton.'),
      [anyn(S('Movement / protection (of internal organs) / support (or shape) / production', 'of blood cells'), 2, 3)],
      'bio-2-4', 'functions-of-the-skeleton', SQ(21, 'Functions of skeleton:'), 6, stem=[Q14C]),
    T('14cii', 'Q14(c)(ii)', 'C', _C(7, 'Name the two main parts of the appendicular skeleton, to which the limbs are',
                                     'attached.'),
      [pt(S('Pectoral girdle (or shoulders)'), 3), pt(S('Pelvis (or pelvic girdle or hips)', page=22), 3)], 'bio-2-4',
      'girdles', SQ(21, 'Limbs are attached to:'), 6, stem=[Q14C]),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(7, 'Name two of the types of bones that make up the foot.'),
      [anyn(S('Tarsals/ metatarsals/ phalanges (or digits)'), 2, 3)], 'bio-2-4', 'bones-of-the-foot',
      SQ(22, 'Types of bones in the foot:'), 6, stem=[Q14C]),
    T('14civ', 'Q14(c)(iv)', 'C', _C(7, 'What is meant by the term antagonistic muscle pair?'),
      [pt(S('(Two) muscles that work with opposing actions or (two) muscles that have',
            'opposite effects or when one contracts the other relaxes'), 3)], 'bio-2-4', 'antagonistic-pairs',
      SQ(22, 'Antagonistic muscle pair:'), 3, stem=[Q14C]),
    T('14cv', 'Q14(c)(v)', 'C', _C(7, 'Name an antagonistic muscle pair in the human body.'),
      [pt(S('Biceps and triceps'), 3)], 'bio-2-4', 'an-antagonistic-pair', SQ(22, 'An antagonistic muscle pair:'), 3,
      stem=[Q14C]),
    T('14cvi', 'Q14(c)(vi)', 'C', _C(7, 'Describe in full how this antagonistic muscle pair works.'),
      [pt(S('(Biceps) contract to flex (or raise or bend) the arm (or elbow)'), 3),
       pt(S('(Triceps) contract to extend (or lower or straighten) the arm (or elbow)'), 3)], 'bio-2-4',
      'how-antagonistic-pairs-work', SQ(22, 'How given antagonistic muscle pair works:'), 6,
      stem=[Q14C, M('(v)', 7), _C(7, 'Name an antagonistic muscle pair in the human body.')]),
    T('15ai', 'Q15(a)(i)', 'C', _C(8, 'Draw a large labelled diagram to show the structure of Rhizopus during asexual',
                                   'reproduction.'),
      [pt(S('Stolon and sporangiophore and sporangium and rhizoids'), 6, kind='criterion', note_sel=S('6, 3, 0')),
       anyn(S('Mycelium / rhizoid / hypha / stolon/ sporangiophore / apophysis /', 'columella / sporangium / sporangiospores (spores)'),
            6, 1)], 'bio-3-2', 'drawing-rhizopus', SQ(22, 'Rhizopus during asexual reproduction:'), 12),
    T('15aii', 'Q15(a)(ii)', 'C', _C(8, 'What mode of nutrition does Rhizopus use?'),
      [pt(S('*Saprophytic (saprophyte) or *heterotrophic'), 3)], 'bio-3-2', 'rhizopus-nutrition',
      SQ(22, 'Rhizopus nutrition:'), 3),
    T('15aiii', 'Q15(a)(iii)', 'C', _C(8, 'Describe an environmental condition that would cause Rhizopus to reproduce',
                                       'sexually.'),
      [pt(S('Lack of water or unsuitable (or adverse or extreme) temperature',
            'or unsuitable (or adverse or extreme) pH or lack of nutrients'), 3)], 'bio-3-2', 'trigger-for-sexual-reproduction',
      SQ(22, 'Environmental condition to cause Rhizopus to reproduce sexually.'), 3),
    T('15aiv', 'Q15(a)(iv)', 'C', _C(8, 'Describe in detail the process of sexual reproduction in Rhizopus.'),
      [anyn(S('Opposite ( or + and - ) strains (of hypha) / Swellings form (or nuclei',
              'Zygospore formation/ Germination of zygospore / By meiosis'), 4, 3)], 'bio-3-2',
      'sexual-reproduction-in-rhizopus', SQ(22, 'Sexual reproduction in Rhizopus:'), 12),
    T('15bi', 'Q15(b)(i)', 'C', _C(8, 'What is meant by the term digestion?'),
      [pt(S('Breaking down food'), 3)], 'bio-2-6', 'digestion', SQ(22, 'Digestion:'), 3, stem=[Q15B]),
    T('15bii', 'Q15(b)(ii)', 'C', _C(8, 'Give two reasons why digestion is necessary.'),
      [anyn(S('To make food soluble/ easier to absorb/ easier to transport'), 2, 3)], 'bio-2-6', 'why-digest-food',
      SQ(23, 'Why digestion necessary:'), 6, stem=[Q15B]),
    T('15biii', 'Q15(b)(iii)', 'C', _C(8, 'Name and describe the method by which food is passed along the alimentary',
                                       'canal.'),
      [pt(S('*Peristalsis'), 3), pt(S('Muscular contractions (of the walls of the alimentary canal)'), 3,
                                    label=S('Description of peristalsis:'))], 'bio-2-6', 'peristalsis',
      SQ(23, 'How food passed along alimentary canal:'), 6, stem=[Q15B]),
    T('15biv', 'Q15(b)(iv)', 'C', _C(8, 'Name an enzyme that digests dietary protein.'),
      [pt(S('Protease or pepsin (or other named protease)'), 3)], 'bio-2-6', 'protease',
      SQ(23, 'Enzyme that digests dietary protein:'), 3, stem=[Q15B]),
    T('15bv', 'Q15(b)(v)', 'C', _C(8, 'Where is this enzyme produced?'),
      [pt(S('Stomach or small intestine or duodenum or ileum or pancreas'), 3, note_sel=S('[must match answer (iv)]'))],
      'bio-2-6', 'where-protease-is-made', SQ(23, 'Where this enzyme produced:'), 3,
      stem=[Q15B, M('(iv)', 8), _C(8, 'Name an enzyme that digests dietary protein.')]),
    T('15bvi', 'Q15(b)(vi)', 'C', _C(8, 'Where is this enzyme active?'),
      [pt(S('Stomach or small intestine or duodenum or ileum'), 3,
          note_sel=S('[must match answer (iv) and must also match (v) where (v) is answered', 'correctly]'))],
      'bio-2-6', 'where-protease-works', SQ(23, 'Where this enzyme active:'), 3,
      stem=[Q15B, M('(iv)', 8), _C(8, 'Name an enzyme that digests dietary protein.')]),
    T('15bvii', 'Q15(b)(vii)', 'C', _C(8, 'Name the products formed by the complete digestion of a protein molecule.'),
      [pt(S('*Amino acids'), 3)], 'bio-2-6', 'amino-acids', SQ(23, 'Products formed by complete protein digestion:'), 3,
      stem=[Q15B]),
    T('15bviii', 'Q15(b)(viii)', 'C', [_C(8, 'These products are transported to the liver.'),
                                       _C(8, 'Name the blood vessel that transports these digestion products to the liver.')],
      [pt(S('*Hepatic portal vein'), 3)], 'bio-2-6', 'hepatic-portal-vein',
      SQ(23, 'Blood vessel that transports protein digestion products to liver:'), 3, stem=[Q15B]),
    T('15ci', 'Q15(c)(i)', 'C', _C(8, 'Describe in detail the development of the embryo sac from a megaspore',
                                   'mother‐cell.'),
      [anyn(S('(Diploid megaspore mother-cell) divides by meiosis / Giving four haploid',
              '(haploid nucleus) becomes the egg (nucleus).'), 4, 3)], 'bio-2-5', 'embryo-sac-development',
      SQ(23, 'Megaspore mother-cell development:'), 12, stem=[Q15C]),
    T('15cii1', 'Q15(c)(ii)1', 'C', _C(8, '1. Outline what happens during each fertilisation.'),
      [pt(S('One (male) gamete (or sperm nucleus) fuses (or joins or combines) with the', 'egg'), 3),
       pt(S('One (male) gamete (or sperm nucleus) fuses (or joins or combines) with the', '(two) polar nuclei', page=24), 3)],
      'bio-2-5', 'double-fertilisation', SQ(23, '1. What happens during each fertilisation:'), 6,
      stem=[Q15C, Q15CII], decision=EACH_ITEM),
    T('15cii2', 'Q15(c)(ii)2', 'C', _C(8, '2. State what is produced by each fertilisation.'),
      [pt(S('A (diploid) zygote'), 3), pt(S('A triploid nucleus or a triploid endosperm'), 3,
                                          note_sel=S('[if order not agreeing with 1, must say which fusion gives which result]'))],
      'bio-2-5', 'products-of-fertilisation', SQ(24, '2. What is produced by each fertilisation:'), 6,
      stem=[Q15C, Q15CII, _C(8, '1. Outline what happens during each fertilisation.')], decision=EACH_ITEM),
    T('15ciii', 'Q15(c)(iii)', 'C', [_C(8, 'Draw a large diagram of a seed and label the following parts:'),
                                     _C(8, 'testa plumule radicle', br=True)],
      [pt(S('Testa and plumule and radicle'), 3, kind='criterion'), anyn(S('Testa / plumule / radicle'), 3, 1)],
      'bio-2-5', 'drawing-a-seed', SQ(24, 'Drawing:', paired=COMPRESSED), 6,
      stem=[Q15C]),
]

FIGURES = {
    'q4-mitosis': ('038', 6, (75, 112, 548, 210), SEC, [],
                   'Photograph of a row of plant cells at different stages of mitosis, the first labelled Prophase.',
                   False),
    'q5-red-cells': ('038', 7, (218, 104, 376, 248), SEC, [],
                     'Drawing of three human red blood cells seen at an angle.', False),
    'q6-alveolus': ('038', 8, (86, 86, 537, 286), SEC, [],
                    'Microscopic detail of an alveolus wrapped by a capillary, labelled Capillary, Alveolus and Blood '
                    'flow, with an arrow showing the direction of blood flow.', False),
    'q11-pedigree': ('040', 4, (110, 392, 535, 518), SEC, [],
                     'Pedigree of haemophilia in a family: parents 1 (a carrier female) and 2 (a normal male); their '
                     'children 3 (carrier female), 4 (haemophiliac male), 5 (carrier female), 6 (haemophiliac male) '
                     'and 7 (normal female), with a phenotypes key for normal female, carrier female, normal male and '
                     'haemophiliac male.', False),
    'q12-organelles': ('040', 5, (145, 350, 492, 468), SEC, [],
                       'Two cut-away cell structures: A, a long oval body with folded inner membranes; B, a rounded '
                       'body containing stacks of discs.', False),
    'q14a-i': ('040', 7, (80, 80, 545, 329), SEC, ['A', 'B', 'C', 'D', 'E', 'F'],
               'Part (a)(i) as printed: "The diagram shows parts of the human central nervous system and some '
               'related structures. In your answer book, match each of the parts labelled A ‒ F to one of the names '
               'from the list below." Below it the names cerebrum, medulla oblongata, pituitary gland, cerebellum, '
               'hypothalamus and spinal cord, and a section through the human brain and the top of the spinal cord '
               'with six label lines: A to the folded structure at the back below the main brain, B to the large '
               'folded upper part, C to a small body hanging below the centre, D to the stalk at the base of the '
               'brain, E to the cord running down from it, and F to a region at the centre just above C.', False),
}
