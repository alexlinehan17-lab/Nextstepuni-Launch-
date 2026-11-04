"""Biology 2022 Ordinary Level — reviewed task ledger, correcting the sitting in place.

Independent visual sweep (2026-10-13), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 40 pages: p1 cover
    (with the note that the 2022 papers were adjusted for disruption to
    learning), p2 instructions, p3-p7 Section A Questions 1-7, p8-p10
    Section B Questions 8-10, p11 Section C answerbook instructions,
    p12-p13 graph paper, p14-p39 ruled answer pages, p40 back cover. No
    acknowledgements page.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 "Do not hand this question paper up", p12 back cover.
  * LC025GLP000EV (marking scheme), 28 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations, p7-p24 Questions
    1-17, p25-p27 "BLANK PAGE", p28 back cover.

The 2022 papers set fewer questions to answer: any four of Section A, any one
of Section B and any three of Section C. Every printed question is carded.

The sitting was already carded (167 authored cards, 166 shipped). As for the
later sittings, every task is re-derived from the PDFs at the scheme's own
mark boundaries and the existing cards are corrected in place: every shipped
id is kept, mapped (`id=`) to the task it was carding, verified or corrected
with its old fields recorded; tasks the old cards bundled or missed are
added. bio-2022-ol-q16-a-ii-fig, a figure twin of bio-2022-ol-q16-a-ii that
never shipped, is withdrawn.

Tariffs as printed. Q1 and Q7 are "5(4)", a 4-mark line per lettered part.
Q2-Q6 are each "6(3) + 2" over seven responses, an ordered split carded at
3 a response. Section B prints a mark per row ((a) "2(3)", (b) "8(3)").
Section C is laddered: (a) "5 + 2(2)", (b) "3(5) + 6(2)", (c) "2(6) + 6(2)",
and each part of Q16 and Q17 "2(7) + 8(2)"; every response is carded at its
ladder's first rate and the ladder, not the cards, makes the printed total.
Response counts are checked against each "Number of correct responses" table.
Q11(b) and Q12(b) print eight answers under a table that runs to nine
(27 marks): the eight printed responses are carded and the ladder is pinned
with `responses: 8`; no ninth answer is invented.

One printed choice is marked differently per option and is split into
routes: Q13(c)(i) asthma or bronchitis (two scheme columns, each with its own
symptom, cause and treatment), one card per numbered item and condition.
Q13(c)(ii) and (iv) ("either breathing or pulse rate") are marked on the same
rows for both and are one card each ("choice is not a route").

The 2021 and 2022 booklets set the degree sign as a superscript o before C;
the reader shows it as the page does ("4 °C", "17°C to 32°C").
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2022, 'ol'
REVIEWED_AT = '2026-10-13'
BASELINE_COMMIT = '2cf70f227'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2022-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': '452a9748ea5733b932cc3fda0b4a3f4b7d85a7614ac5a0b2dbc6131b8e0ba454',
            'pages': 40},
    '040': {'path': 'examiner-reports/biology/papers/2022-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': 'b35173bd0b7af6e00fab438730e5cf6f7e11b9aaee8116a7d4cec3a194d63f71',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2022-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': '57840b70d4a9bdcce5646474e6a7ca095410ae76c170afcce274278738bfaee9',
               'pages': 28},
}

PAGE_ROLES = {
    '038': {1: 'cover', 2: 'instructions', **{p: 'questions' for p in range(3, 11)},
            11: 'answerbook-instructions', 12: 'graph-paper', 13: 'graph-paper',
            **{p: 'answer-pages' for p in range(14, 40)}, 40: 'back-cover'},
    '040': {1: 'cover', **{p: 'questions' for p in range(2, 11)}, 11: 'blank', 12: 'back-cover'},
    'scheme': {1: 'cover', 2: 'note', 3: 'introduction', 4: 'marking-examples',
               5: 'marking-examples', 6: 'annotations', **{p: 'marking' for p in range(7, 25)},
               25: 'blank', 26: 'blank', 27: 'blank', 28: 'back-cover'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 8)}, **{n: 30 for n in range(8, 11)},
    **{n: 60 for n in range(11, 16)}, 16: 120, 17: 120,
}
PART_TOTALS = {**{(n, 'a'): 6 for n in (8, 9, 10)}, **{(n, 'b'): 24 for n in (8, 9, 10)}}


def _ladder(notation, responses=None):
    steps = []
    for term in notation.split(' + '):
        n, _, m = term.partition('(')
        steps += [int(m.rstrip(')'))] * int(n) if m else [int(n)]
    return {'steps': steps, 'notation': notation, **({'responses': responses} if responses else {})}


LADDERS = {
    **{q: _ladder('6(3) + 2') for q in (2, 3, 4, 5, 6)},
    **{(n, 'a'): _ladder('5 + 2(2)') for n in range(11, 16)},
    # Q11(b) and Q12(b): eight printed answers under a nine-response table.
    **{(n, 'b'): _ladder('3(5) + 6(2)', 8 if n in (11, 12) else None) for n in range(11, 16)},
    **{(n, 'c'): _ladder('2(6) + 6(2)') for n in range(11, 16)},
    **{(n, x): _ladder('2(7) + 8(2)') for n in (16, 17) for x in 'abcd'},
}

CHECKSUMS = {
    1: {4: 5}, 7: {4: 5}, **{q: {3: 7} for q in (2, 3, 4, 5, 6)},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {5: 3} for n in range(11, 16)},
    (11, 'b'): {5: 8}, (12, 'b'): {5: 8}, **{(n, 'b'): {5: 9} for n in (13, 14, 15)},
    **{(n, 'c'): {6: 8} for n in range(11, 16)},
    **{(n, x): {7: 10} for n in (16, 17) for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 11), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any four', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any one', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any three', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any four', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: every part asked.'),
    ('038', 3, 'any three', 'Q1(a) "any three elements": the scheme prints one line naming all three; one card.'),
    ('038', 6, 'or', 'Q5(a) "A or B or C": the answer options.'),
    ('038', 6, 'or', 'Q5(a), same options.'),
    ('038', 6, 'any one', 'Q5(c) "any one pair": open single answer; one card.'),
    ('038', 7, 'the following', 'Q6 lead-in: every statement asked.'),
    ('038', 7, 'or', 'Q6 "true or false": the answer options.'),
    ('038', 7, 'choose', 'Q7 "Choose each term": a matching list, every term placed; one card per lettered '
                         'description.'),
    ('038', 7, 'the following', 'Q7 term list.'),
    ('038', 8, 'any one', 'Section B rubric repeated.'),
    ('038', 9, 'or', 'Q9(b)(vi) "the test, or the chemicals": either form; one answer.'),
    ('040', 2, 'any three', 'Section C rubric repeated.'),
    ('040', 2, 'the following', 'Q11(a): every term asked, one card per roman.'),
    ('040', 2, 'any one', 'Q11(b)(vii) "any one food chain": open single answer; one card.'),
    ('040', 2, 'the following', 'Q11(c) "the following passage": a reference.'),
    ('040', 2, 'or', 'Q11(c) passage "sewage or slurry": passage text.'),
    ('040', 3, 'the following', 'Q12(a): every term asked, one card per roman.'),
    ('040', 3, 'the following', 'Q12(b)(ii): each genotype asked, one card per item.'),
    ('040', 4, 'the following', 'Q13(c) "the following passages": a reference.'),
    ('040', 4, 'either', 'Q13(c)(i) "either asthma or bronchitis": separate symptom, cause and treatment per '
                         'option: ROUTES.'),
    ('040', 4, 'or', 'Q13(c)(i), same choice.'),
    ('040', 4, 'or', 'Q13(c) asthma passage "cold air or dust": passage text.'),
    ('040', 4, 'either', 'Q13(c)(ii) "either breathing or pulse rate": marked on the same rows; one card.'),
    ('040', 4, 'or', 'Q13(c)(ii), same choice.'),
    ('040', 4, 'either', 'Q13(c)(iv) "either breathing or pulse rate": one answer for both; one card.'),
    ('040', 4, 'or', 'Q13(c)(iv), same choice.'),
    ('040', 5, 'or', 'Q14(c)(iii) "A or B": the answer options.'),
    ('040', 6, 'the following', 'Q15(c)(i): each part asked, one card per item.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q16 rubric, same choice.'),
    ('040', 8, 'any one', 'Q16(c)(ii) "any one bone ... in each": one open answer per item; one card per item.'),
    ('040', 8, 'the following', 'Q16(c)(ii): each part of the skeleton asked, one card per item.'),
    ('040', 8, 'the following', 'Q16(c)(iii): all three parts labelled; one card.'),
    ('040', 8, 'or', 'Q16(d) "vegetative propagation or artificial propagation": description.'),
    ('040', 8, 'the following', 'Q16(d)(vi): each heading asked, one card per item.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'the following', 'Q17 rubric, same choice.'),
    ('040', 9, 'or', 'Q17(a)(v) "Name or give an example": either form; one answer.'),
    ('040', 9, 'the following', 'Q17(a)(vii): each heading asked, one card per item.'),
    ('040', 9, 'both', 'Q17(b)(ii) "Name both biologists": both required; one card.'),
    ('040', 10, 'any two', 'Q17(c)(iv) "any two blood groups": bounded menu; one card.'),
    ('040', 10, 'both', 'Q17(d)(ii) "Both can occur in the mouth": description.'),
    ('040', 10, 'both', 'Q17(d)(ii)1 "both types": both required; one card.'),
    ('040', 10, 'both', 'Q17(d)(ii)2 "both types": description.'),
]

ROUTES = {f'Q13(c)(i){n}': ['asthma', 'bronchitis'] for n in (1, 2, 3)}

LAYOUT_CHECKS = [
    ('scheme', 17, item, ['Name: Asthma', 'Name: Bronchitis'], want)
    for item, want in [
        ('Difficulty breathing or tightening of', 'Name: Asthma'),
        ('Inflammation or cough or pain', 'Name: Bronchitis'),
        ('Presence of cold air or dust or allergens', 'Name: Asthma'),
        ('Presence of pathogen (or infection) or', 'Name: Bronchitis'),
        ('Inhaler or avoid allergen or medication', 'Name: Asthma'),
        ('Medication or antibiotics or pain killers or give', 'Name: Bronchitis')]
]

ATLAS_UNIT_EQUIV = {'bio-u1': 'bio-u2'}

RETAINED = {
    'bio-2022-ol-q16-a-ii-fig': 'Never shipped: a figure twin of bio-2022-ol-q16-a-ii, which carries the '
                                'reviewed task and its figure.',
}
WITHDRAW = {'bio-2022-ol-q16-a-ii-fig': ('bio-2022-ol-q16-a-ii', RETAINED['bio-2022-ol-q16-a-ii-fig'])}

SEC = 'State Examinations Commission'


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def item(page, n, end, anchor):
    """One entry of a printed numbered list ("1." on its own line, its item on the next)."""
    return _C(page, f'{n}.', end, after=anchor, br=True)


def tick(clip, answer):
    return G('tick-col', page=9, clip=clip, headers=['True', 'False'], expect=answer, marks=3)


def bundled(parts, keep):
    return f'The old card bundled {parts}; it keeps its id for {keep}.'


EACH_ITEM = 'Numbered items are separately counted responses: one card each.'

Q1 = _A(3, 'Use your knowledge of nutrition to answer the following questions.')
Q3 = _A(4, 'The diagram shows Rhizopus, a microorganism that causes food spoilage.')
Q4 = _A(5, 'The diagram shows a section through human skin.')
Q5 = _A(6, 'During an investigation a DNA profile was carried out', 'The diagram shows the DNA profiles obtained.')
Q6 = _A(7, 'State whether each of the following statements is true or false', 'appropriate box in each case.')
Q7 = [_A(7, 'Choose each term from the following list', 'Column A.'), _A(7, 'Data'), _A(7, 'Double blind test'),
      _A(7, 'Variable'), _A(7, 'Control'), _A(7, 'Hypothesis')]
Q8B = _A(8, 'A student conducted a survey in a habitat close to her home', 'different plants in the habitat.')
Q8T = _A(8, 'The table below shows the data collected during the survey.')
Q10A = _A(10, 'Germination is the regrowth of the plant embryo after a period of inactivity.')
Q10B = _A(10, 'The diagram below shows an apparatus used to investigate', 'germination.')
Q11A = _C(2, 'Explain the following terms used in ecology:')
Q11B = _C(2, 'The diagram shows an example of interconnected food chains.')
Q11C = [_C(2, 'Read the following passage and answer the questions that follow.'),
        _C(2, 'A recent Environmental Protection Agency (EPA) report', 'levels often cause fish kills.'),
        _C(2, '(Adapted from www.epa.ie, 13 November 2019)')]
Q12A = _C(3, 'Explain the following terms used in genetics:')
Q12B = [_C(3, 'Read the passage below and answer the questions that follow.'),
        _C(3, 'Cystic fibrosis (CF) is caused by a mutated gene', 'family history of CF.'),
        _C(3, '(Adapted from mayoclinic.org)')]
Q12C = _C(3, 'The cell cycle consists of two stages, interphase and mitosis (cell division).')
Q12CIII = [Q12C, M('(iii)', 3), _C(3, 'Name another form of cell division that introduces variation', 'daughter cells.')]
Q13B = _C(4, 'The diagram shows the structure of the', 'human breathing system.')
Q13C = [_C(4, 'Read the following passages and, using either asthma or bronchitis', 'questions that follow.'),
        _C(4, 'Asthma is a condition that affects', 'leaving less room for air to flow.'),
        _C(4, '(Adapted from www.asthma.ie)'),
        _C(4, 'Bronchitis is a condition that affects', 'long-term condition.'),
        _C(4, '(Adapted from www.mayoclinic.org)')]
Q13CX = _C(4, 'As part of her preparation for a race an athlete investigated', 'breathing rate and pulse rate.')
Q14BV = _C(5, 'During photosynthesis water is absorbed and split into oxygen and two other', 'products.')
Q14BVI = _C(5, 'Carbon dioxide is absorbed by plants during photosynthesis.')
Q14C1 = _C(5, 'Water enters the roots of plants by osmosis, which is a special case of diffusion.')
Q14C2 = _C(5, 'Turgor is also important for plants.', 'show two plants cells.')
Q15B = _C(6, 'The diagram shows a section through a plant stem.')
Q15C = _C(6, 'The diagram shows a plant flower.')
Q16A = _C(7, 'The diagram shows the human male reproductive system.')
Q16CII = _C(8, 'The human skeleton shown in the diagram can be', 'in each of the following parts:')
Q16D = _C(8, 'Plants can undergo a process of vegetative propagation or artificial propagation.')
Q16DG = _C(8, 'The diagram above shows grafting, a form of artificial propagation.')
Q16DVI = _C(8, 'Compare reproduction by seed with reproduction by vegetative propagation', 'the following headings:')
Q17A = _C(9, 'The diagram shows a section through the spinal cord with attached nerves.')
Q17AVII = _C(9, 'Compare a nervous system response with a hormonal system response under', 'the following headings:')
Q17B = _C(9, 'The theory of evolution by natural selection was developed by two famous biologists.')
Q17BGE = _C(9, 'Genetic engineering is also an important area of biology.')
Q17C = _C(10, 'The circulatory system is one of two systems that carry fluids within the body.')
Q17DII = _C(10, 'Chemical digestion and mechanical digestion are part of nutrition.', 'occur in the mouth.')

L_RHIZOPUS = [L('A', S('Sporangium', page=8), True), L('B', S('Stolon (hypha)', page=8), True),
              L('C', S('Rhizoid (allow hypha if not used for B)', page=8), True)]
L_SKIN = [L('A', S('Hair', page=8), True), L('B', S('Sebaceous gland', page=8), True)]
L_LUNGS = [L('A', S('Larynx (voice box)', page=16), True), L('B', S('Bronchus', page=16), True),
           L('C', S('Bronchiole', page=16), True)]
L_STEM = [L('A', S('Dermal', page=20), True), L('B', S('Ground', page=20), True),
          L('C', S('Vascular bundle', page=20), True)]
L_MALE = [L('A', S('Penis', page=21), True), L('B', S('Sperm duct (vas deferens)', page=21), True),
          L('C', S('Testes', page=21), True), L('D', S('Urethra', page=21), True)]
L_GRAFT = [L('A', S('Leaf', page=22, after='Name parts labelled A and B.'), True),
           L('B', S('Stem', page=22, after='Name parts labelled A and B.'), True)]
L_SPINAL = [L('A', S('Sensory neuron', page=23), True), L('B', S('Interneuron', page=23), True),
            L('C', S('Motor neuron', page=23), True)]
L_BLOOD = [L('X', S('Red blood cell', page=24), True), L('Y', S('White blood cell', page=24), True)]


def asked(keys, *letters):
    return [dict(k, asked=k['letter'] in letters) for k in keys]


TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A', _A(3, 'Name any three elements found in fats.'),
      [pt(S('C, H and O (allow P)'), 4, kind='allOf')], 'bio-1-2', 'elements-in-fats',
      SQ(7, 'Name any three elements found in fats.'), 4, stem=[Q1], id='bio-2022-ol-q1-a',
      decision='One 4-mark line naming all three elements: one all-of row.'),
    T('1b', 'Q1(b)', 'A', _A(3, 'In a triglyceride, three molecules of fatty acids are joined to one molecule of'),
      [pt(S('Glycerol'), 4)], 'bio-1-2', 'glycerol', SQ(7, '3 fatty acids are joined to one molecule of'), 4,
      stem=[Q1], id='bio-2022-ol-q1-b'),
    T('1c', 'Q1(c)', 'A', _A(3, 'Name a fat-soluble vitamin.'),
      [pt(S('A or D or E or K'), 4)], 'bio-1-2', 'fat-soluble-vitamins', SQ(7, 'Name a fat-soluble vitamin.'), 4,
      stem=[Q1], id='bio-2022-ol-q1-c'),
    T('1d', 'Q1(d)', 'A', _A(3, 'Name a laboratory test used to detect fats in food.'),
      [pt(S('Brown paper or translucent spot or Sudan (III)'), 4)], 'bio-1-2', 'test-for-fats',
      SQ(7, 'Laboratory test for fats.'), 4, stem=[Q1], id='bio-2022-ol-q1-d'),
    T('1e', 'Q1(e)', 'A', _A(3, 'How do fats differ from oils?'),
      [pt(S('Fats are solid or oils are liquid (at room temperature)'), 4)], 'bio-1-2', 'fats-and-oils',
      SQ(7, 'How do fats differ from oils?'), 4, stem=[Q1], id='bio-2022-ol-q1-e'),
    T('2a', 'Q2(a)', 'A', _A(3, 'What is respiration?'),
      [pt(S('Release of energy (from food)'), 3)], 'bio-2-2', 'respiration', SQ(7, 'What is respiration?'), 3,
      id='bio-2022-ol-q2-a'),
    T('2b', 'Q2(b)', 'A', _A(3, 'Name the two products of aerobic respiration.'),
      [anyn(S('Carbon dioxide / water / ATP (energy)'), 2, 3)], 'bio-2-2', 'products-of-aerobic-respiration',
      SQ(7, 'Name two products of aerobic respiration.'), 6, id='bio-2022-ol-q2-b'),
    T('2c', 'Q2(c)', 'A', _A(3, 'Name the gas needed for aerobic respiration to occur.'),
      [pt(S('Oxygen'), 3)], 'bio-2-2', 'oxygen-for-respiration', SQ(7, 'Name the gas needed for aerobic respiration.'),
      3, id='bio-2022-ol-q2-c'),
    T('2d', 'Q2(d)', 'A', _A(3, 'Aerobic respiration occurs in two stages.', 'Where in the cell does each stage occur?'),
      [pt(S('Cytosol (accept cytoplasm)'), 3, label=_A(3, 'Stage 1:')),
       pt(S('Mitochondria'), 3, label=_A(3, 'Stage 2:'))], 'bio-2-2', 'where-respiration-happens',
      SQ(7, 'Location for stage one and stage two reactions.',
         paired='The (d) under the scheme\'s Question 2, reprinted as "Location for stage one and stage two '
                'reactions": its rows 1. and 2. answer the paper\'s Stage 1 and Stage 2 boxes.'), 6, id='bio-2022-ol-q2-d'),
    T('2e', 'Q2(e)', 'A', _A(3, 'Which stage of aerobic respiration produces the most energy?'),
      [pt(S('(Stage) 2'), 3)], 'bio-2-2', 'stage-releasing-most-energy',
      SQ(7, 'Which stage releases the most energy?'), 3, id='bio-2022-ol-q2-e'),
    T('3a', 'Q3(a)', 'A', _A(4, 'Name the parts labelled A, B, C on the diagram.'),
      [pt(S('Sporangium'), 3, label=S('A:')), pt(S('Stolon (hypha)'), 3, label=S('B:')),
       pt(S('Rhizoid (allow hypha if not used for B)'), 3, label=S('C:'))], 'bio-3-2', 'parts-of-rhizopus',
      SQ(8, 'Name the parts A, B, C.'), 9, stem=[Q3], fig='q3-rhizopus', labels=L_RHIZOPUS,
      id='bio-2022-ol-q3-a-fig'),
    T('3b', 'Q3(b)', 'A', _A(4, 'What is the function of the spores produced by Rhizopus?'),
      [pt(S('(Asexual) reproduction'), 3)], 'bio-3-2', 'rhizopus-spores', SQ(8, 'Function of spores.'), 3,
      stem=[Q3], fig='q3-rhizopus', id='bio-2022-ol-q3-b'),
    T('3c', 'Q3(c)', 'A', _A(4, 'Rhizopus is a saprophyte.', 'saprophytic nutrition?'),
      [pt(S('Feeding on dead organic matter'), 3)], 'bio-3-2', 'saprophytic-nutrition',
      SQ(8, 'Saprophytic nutrition.'), 3, stem=[Q3], fig='q3-rhizopus', id='bio-2022-ol-q3-c'),
    T('3d', 'Q3(d)', 'A', _A(4, 'Name the kingdom in which Rhizopus is classified.'),
      [pt(S('Fungi'), 3)], 'bio-3-2', 'kingdom-fungi', SQ(8, 'Name the kingdom in which Rhizopus is classified.'), 3,
      stem=[Q3], fig='q3-rhizopus', id='bio-2022-ol-q3-d'),
    T('3e', 'Q3(e)', 'A', _A(4, 'State one other organism that belongs to the kingdom', 'part (d) above.'),
      [pt(S('Yeast or other correct'), 3)], 'bio-3-2', 'other-fungi', SQ(8, 'State one other organism that belongs'),
      3, stem=[Q3, M('(d)', 4), _A(4, 'Name the kingdom in which Rhizopus is classified.')], fig='q3-rhizopus',
      id='bio-2022-ol-q3-e'),
    T('4a', 'Q4(a)', 'A', _A(5, 'Name the parts labelled A and B in the diagram.'),
      [pt(S('A: Hair'), 3), pt(S('B: Sebaceous gland'), 3)], 'bio-2-4', 'parts-of-the-skin',
      SQ(8, 'Name the parts A, B in skin.'), 6, stem=[Q4], fig='q4-skin', labels=L_SKIN, id='bio-2022-ol-q4-a'),
    T('4b', 'Q4(b)', 'A', _A(5, 'Sweat is produced by sweat glands.', 'State two components of sweat.'),
      [anyn(S('Water / salt / urea'), 2, 3)], 'bio-2-4', 'components-of-sweat',
      SQ(8, 'Sweat is produced by sweat glands.'), 6, stem=[Q4], fig='q4-skin', id='bio-2022-ol-q4-b'),
    T('4c', 'Q4(c)', 'A', _A(5, 'Describe two ways the human body responds to cold conditions.'),
      [anyn(S('Hair stands up / shivering / blood vessels constrict (or reduced blood flow)'), 2, 3)], 'bio-2-4',
      'responding-to-cold', SQ(8, 'Two ways the body responds to cold.'), 6, stem=[Q4], fig='q4-skin',
      id='bio-2022-ol-q4-c'),
    T('4d', 'Q4(d)', 'A', _A(5, 'Ectotherms are organisms that cannot easily control', 'example of an ectotherm.'),
      [pt(S('Frog or snake or insect or lizard or worm or fish or other correct'), 3)], 'bio-2-4', 'ectotherms',
      SQ(8, 'Example of an ectotherm.'), 3, id='bio-2022-ol-q4-d'),
    T('5a', 'Q5(a)', 'A', _A(6, 'Which suspect DNA profile, A or B or C matches', 'scene?'),
      [pt(S('B'), 3)], 'bio-3-3', 'matching-a-dna-profile', SQ(9, 'Which suspect matches the DNA profile?'), 3,
      stem=[Q5], fig='q5-profiles', id='bio-2022-ol-q5-a'),
    T('5b', 'Q5(b)', 'A', [_A(6, 'Place each of the numbers 1, 2, 3, 4 in the correct box', 'creating a DNA profile.'),
                           M('(i)', 6), _A(6, 'Separate DNA fragments based on their sizes'),
                           M('(ii)', 6), _A(6, 'Analyse pattern of fragments'),
                           M('(iii)', 6), _A(6, 'DNA is released from cells using detergent'),
                           M('(iv)', 6), _A(6, 'DNA is cut into fragments using enzymes')],
      [pt(S('3', after='Separate DNA fragments:'), 3, label=S('Separate DNA fragments:')),
       pt(S('4', after='Analyse pattern of fragments:'), 3, label=S('Analyse pattern of fragments:')),
       pt(S('1', after='DNA is released from cells:'), 3, label=S('DNA is released from cells:')),
       pt(S('2', after='DNA is cut into fragments'), 3, label=S('DNA is cut into fragments'))], 'bio-3-3',
      'dna-profiling-steps', SQ(9, 'Put steps in correct order.',
                                paired='The (b) under the scheme\'s Question 5: its rows (i)-(iv) reprint the '
                                       'paper\'s four steps.'), 12, stem=[Q5], fig='q5-profiles', id='bio-2022-ol-q5-b',
      decision='One sequence: the four numbered boxes place the same four steps in order, so they are one task '
               'with a response per box.'),
    T('5c', 'Q5(c)', 'A', _A(6, 'DNA strands are composed of linked pairs of bases.', 'one pair of these bases.'),
      [pt(S('Adenine-thymine or cytosine-guanine or A-T or G-C'), 3)], 'bio-1-2', 'base-pairs',
      SQ(9, 'Name any one base pair found in DNA.'), 3, stem=[Q5], fig='q5-profiles', id='bio-2022-ol-q5-c'),
    T('5d', 'Q5(d)', 'A', _A(6, 'State one other application for DNA profiling.'),
      [pt(S('Paternity testing or other correct'), 3)], 'bio-3-3', 'uses-of-dna-profiling',
      SQ(9, 'State one other application of DNA profiling.'), 3, stem=[Q5], fig='q5-profiles',
      id='bio-2022-ol-q5-d'),
] + [
    T(f'6{x}', f'Q6({x})', 'A', _A(7, start), [tick(clip, answer)], topic, concept, SQ(9, start), 3,
      stem=[Q6], id=f'bio-2022-ol-q6-{x}')
    for x, start, clip, answer, topic, concept in [
        ('a', 'Hormones are produced by endocrine glands.', (55, 385, 560, 410), 'True', 'bio-2-4',
         'endocrine-glands'),
        ('b', 'Fertilisation usually occurs in the fallopian tube.', (55, 410, 560, 436), 'True', 'bio-2-5',
         'site-of-fertilisation'),
        ('c', 'Hydrochloric acid is produced by the liver.', (55, 436, 560, 462), 'False', 'bio-2-6',
         'hydrochloric-acid'),
        ('d', 'Bile is produced by the kidney.', (55, 462, 560, 489), 'False', 'bio-2-6', 'where-bile-is-made'),
        ('e', 'Neurotransmitters are produced by nerve cells.', (55, 489, 560, 515), 'True', 'bio-2-4',
         'neurotransmitters'),
        ('f', 'Antibiotics are produced by viruses.', (55, 515, 560, 540), 'False', 'bio-3-2', 'antibiotics'),
        ('g', 'Amylase is produced by the salivary glands.', (55, 540, 560, 566), 'True', 'bio-2-6', 'amylase')]
] + [
    T(f'7{x}', f'Q7({x})', 'A', _A(7, desc, end), [pt(S(answer), 4)], 'bio-u2', concept, SQ(10, sq), 4,
      stem=Q7, id=old,
      decision='Lettered parts are separate printed addresses; the completed example (Theory, struck through '
               'in the list) is left out of the stem.' + (f' {dec}' if dec else ''))
    for x, desc, end, sq, answer, concept, old, dec in [
        ('a', 'A factor that can change during an', 'investigation', 'Factor that changes during an', 'Variable',
         'variable', 'bio-2022-ol-q7-a-e', 'The old card bundled (a)-(e); it keeps its id for (a).'),
        ('b', 'An educated guess to explain an', 'observation', 'Educated guess to explain an', 'Hypothesis',
         'hypothesis', 'bio-2022-ol-q7-b', ''),
        ('c', 'Information and measurements collected', 'during an investigation', 'Information and measurements',
         'Data', 'data', 'bio-2022-ol-q7-c', ''),
        ('d', 'A method used to prevent bias during an', 'investigation', 'Method to prevent bias',
         'Double blind test', 'double-blind-test', None, ''),
        ('e', 'Comparison to an experiment', None, 'Comparison to an experiment', 'Control', 'control', None, '')]
] + [
    # ------------------------------------------------------------ Section B --
    T('8a', 'Q8(a)', 'B', _A(8, 'Distinguish between a quantitative survey and a qualitative survey.'),
      [pt(S('Quantitative: Numbers of organisms'), 3), pt(S('Types or names of organisms'), 3, label=S('Qualitative:'))],
      'bio-3-1', 'quantitative-and-qualitative', SQ(11, 'Distinguish between quantitative and qualitative.'), 6,
      id='bio-2022-ol-q8-a'),
    T('8bi', 'Q8(b)(i)', 'B', _A(8, 'Describe the procedures she would have taken to carry out the survey.'),
      [anyn(S('Quadrat / random (or unbiased) / how random / count / record / repeat /', 'average'), 4, 3)],
      'bio-3-1', 'frequency-survey', SQ(11, 'Describe the procedures she would have taken'), 12, stem=[Q8B],
      id='bio-2022-ol-q8-b-i'),
    T('8bii', 'Q8(b)(ii)', 'B', _A(8, 'Which plant had the highest % frequency?'),
      [pt(S('Daisy'), 3)], 'bio-3-1', 'highest-frequency', SQ(11, 'Which plant had the highest % frequency?'), 3,
      stem=[Q8B, Q8T], fig='q8-table', id='bio-2022-ol-q8-b-ii'),
    T('8biii', 'Q8(b)(iii)', 'B', _A(8, 'What is the % frequency of the other two named plants in the table above?'),
      [pt(S('3/5 = 60%'), 3, label=S('Plantain:')), pt(S('2/5 = 40%'), 3, label=S('Dandelion:'))], 'bio-3-1',
      'percentage-frequency', SQ(11, 'What is the % frequency of the other two named plants'), 6, stem=[Q8B, Q8T],
      fig='q8-table', id='bio-2022-ol-q8-b-iii'),
    T('8biv', 'Q8(b)(iv)', 'B', _A(8, 'What could the student have used to identify the plants correctly?'),
      [pt(S('(Biological) key or other correct'), 3)], 'bio-3-1', 'identifying-plants',
      SQ(11, 'What could the student have used to identify'), 3, stem=[Q8B], id='bio-2022-ol-q8-b-iv'),
    T('9ai', 'Q9(a)(i)', 'B', _A(9, 'Fermentation is a process that does not use'),
      [pt(S('Oxygen'), 3)], 'bio-2-2', 'fermentation-is-anaerobic', SQ(12, 'Fermentation is a process that does not use'),
      3, id='bio-2022-ol-q9-a-i'),
    T('9aii', 'Q9(a)(ii)', 'B', _A(9, 'Name the gas produced during alcohol fermentation.'),
      [pt(S('Carbon dioxide'), 3)], 'bio-2-2', 'gas-from-fermentation',
      SQ(12, 'Name the gas produced during alcohol fermentation.'), 3, id='bio-2022-ol-q9-a-ii'),
    T('9bi', 'Q9(b)(i)', 'B', _A(9, 'Draw a labelled diagram in the space below of the apparatus', 'in the laboratory.'),
      [pt(S('Container and liquid / anaerobic step (e.g. fermentation lock or oil layer) /', 'water bath'), 3,
          kind='criterion', note_sel=S('(Diagram must contain any two)')),
       pt(S('Any two correct labels'), 6, kind='criterion', units=[3, 3], label=S('Labels:'))], 'bio-2-2',
      'fermentation-apparatus', SQ(12, 'Draw a labelled diagram in the space below'), 9, id='bio-2022-ol-q9-b-i'),
    T('9bii', 'Q9(b)(ii)', 'B', _A(9, 'Describe one safety precaution you took during the activity.'),
      [pt(S('Wore lab coat or wore safety gloves or wore safety goggles or any valid', 'precaution'), 3)], 'bio-2-2',
      'fermentation-safety', SQ(12, 'One safety precaution.'), 3, id='bio-2022-ol-q9-b-ii'),
    T('9biii', 'Q9(b)(iii)', 'B', _A(9, 'Give a suitable temperature for this activity.'),
      [pt(S('17°C to 32°C'), 3)], 'bio-2-2', 'fermentation-temperature', SQ(12, 'Suitable temperature.'), 3,
      id='bio-2022-ol-q9-b-iii'),
    T('9biv', 'Q9(b)(iv)', 'B', _A(9, 'How did you know alcohol production had stopped?'),
      [pt(S('No more bubbles'), 3)], 'bio-2-2', 'end-of-fermentation',
      SQ(12, 'How did you know alcohol production had stopped?'), 3, id='bio-2022-ol-q9-b-iv'),
    T('9bv', 'Q9(b)(v)', 'B', _A(9, 'Briefly describe how you set up the control for this activity.'),
      [pt(S('Same setup with no yeast (or no sugar)'), 3)], 'bio-2-2', 'fermentation-control', SQ(12, 'Set up control?'),
      3, id='bio-2022-ol-q9-b-v'),
    T('9bvi', 'Q9(b)(vi)', 'B', _A(9, 'Name the test, or the chemicals you used, to show that alcohol was present.'),
      [pt(S('Iodoform (or sodium hypochlorite and potassium iodide)'), 3)], 'bio-2-2', 'test-for-alcohol',
      SQ(12, 'Name of test or chemicals used to show presence of alcohol.'), 3, id='bio-2022-ol-q9-b-vi'),
    T('10ai', 'Q10(a)(i)', 'B', _A(10, 'What is the name given to this period of inactivity?'),
      [pt(S('Dormancy'), 3)], 'bio-2-5', 'dormancy', SQ(13, 'Name this period of inactivity.'), 3, stem=[Q10A],
      id='bio-2022-ol-q10-a-i'),
    T('10aii', 'Q10(a)(ii)', 'B', _A(10, 'Give one location in a seed where food is stored.'),
      [pt(S('Cotyledon or endosperm'), 3)], 'bio-2-5', 'food-store-in-seed',
      SQ(13, 'Give one location in seed where food is stored.'), 3, stem=[Q10A], id='bio-2022-ol-q10-a-ii'),
    T('10bi', 'Q10(b)(i)', 'B', _A(10, 'Name a seed that could be used in this activity.'),
      [pt(S('Cress (or another correctly named seed)'), 3)], 'bio-2-5', 'seed-for-germination',
      SQ(13, 'Name a seed that could be used in this activity.'), 3, stem=[Q10B], fig='q10-germination',
      id='bio-2022-ol-q10-b-i'),
    T('10bii', 'Q10(b)(ii)', 'B', _A(10, 'Why was dry cotton wool used in test tube A?'),
      [pt(S('To exclude water'), 3)], 'bio-2-5', 'germination-needs-water',
      SQ(13, 'Why was dry cotton wool used in test tube A?'), 3, stem=[Q10B], fig='q10-germination',
      id='bio-2022-ol-q10-b-ii'),
    T('10biii', 'Q10(b)(iii)', 'B', _A(10, 'Why was boiled water and an oil layer used in test tube C?'),
      [pt(S('To exclude oxygen'), 3)], 'bio-2-5', 'germination-needs-oxygen',
      SQ(13, 'Why was boiled water and an oil layer used'), 3, stem=[Q10B], fig='q10-germination',
      id='bio-2022-ol-q10-b-iii'),
    T('10biv', 'Q10(b)(iv)', 'B', _A(10, 'How was a temperature of 4 °C maintained in test tube D?'),
      [pt(S('Placed in fridge'), 3)], 'bio-2-5', 'keeping-seeds-cold',
      SQ(13, 'How was a temperature of 4°C maintained'), 3, stem=[Q10B], fig='q10-germination',
      id='bio-2022-ol-q10-b-iv'),
    T('10bv', 'Q10(b)(v)', 'B', _A(10, 'State the results observed for each test tube.'),
      [pt(S('No germination'), 3, label=S('A:')), pt(S('Germination', after='B:'), 3, label=S('B:')),
       pt(S('No germination', after='C:'), 3, label=S('C:')),
       pt(S('No germination (allow some germination)'), 3, label=S('D:'))], 'bio-2-5', 'germination-results',
      SQ(13, 'State the results observed for each tube.'), 12, stem=[Q10B], fig='q10-germination',
      id='bio-2022-ol-q10-b-v'),
] + [
    # ------------------------------------------------------------ Section C --
    T(f'11a{r}', f'Q11(a)({r})', 'C', [Q11A, _C(2, term, br=True)], rows, 'bio-3-1', concept,
      SQ(14, 'Explain the following terms used in ecology:'), 5,
      id='bio-2022-ol-q11-a' if r == 'i' else None,
      decision=bundled('(a)(i)-(iii)', '(i), and (ii), (iii) are added') if r == 'i' else '')
    for r, term, rows, concept in [
        ('i', 'Biosphere', [pt(S('Biosphere: Region of earth where life can exist'), 5)], 'biosphere'),
        ('ii', 'Abiotic', [pt(S('Non-living'), 5, label=S('Abiotic:'))], 'abiotic'),
        ('iii', 'Niche', [pt(S('Role (of organism)'), 5, label=S('Niche:'))], 'niche')]
] + [
    T(f'11b{r}', f'Q11(b)({r})', 'C', _C(2, ask, aend), rows, 'bio-3-1', concept, SQ(14, sq), total,
      stem=[Q11B], fig='q11-food-web', id=f'bio-2022-ol-q11-b-{r}',
      decision=dec)
    for r, ask, aend, rows, concept, sq, total, dec in [
        ('i', 'What term describes a collection of', 'interconnected food chains?', [pt(S('Food web'), 5)],
         'food-web', 'What term describes a collection of interconnected food chains?', 5,
         'The scheme\'s nine-response table under (b) holds eight printed answers; each is carded.'),
        ('ii', 'What is the primary source of energy', 'for a producer in a food chain?', [pt(S('Sun'), 5)],
         'energy-source', 'What is the primary source of energy for a producer', 5, ''),
        ('iii', 'Identify a producer from the diagram.', None, [pt(S('Blackberry or grass'), 5)], 'producer',
         'Identify a producer from the diagram.', 5, ''),
        ('iv', 'Name one carnivore from the diagram.', None, [pt(S('Owl or spider'), 5)], 'carnivore',
         'Name one carnivore from the diagram.', 5, ''),
        ('v', 'What is an omnivore?', None, [pt(S('Animal that eats plant and animal material'), 5)], 'omnivore',
         'What is an omnivore?', 5, ''),
        ('vi', 'Name one omnivore from the diagram.', None, [pt(S('Fox or blackbird or shrew'), 5)],
         'omnivore-in-the-web', 'Name one omnivore from the diagram.', 5, ''),
        ('vii', 'Write out any one food chain from the', 'diagram.',
         [pt(S('E.g. Grass → grasshopper → shrew → owl'), 5, kind='criterion',
             note_sel=S('Food chain must start with a producer'))], 'food-chain',
         'Write out any one food chain from the diagram.', 5, ''),
        ('viii', 'Suggest what would happen to the', 'reduced the spider population.',
         [pt(S('(The aphid population) would increase'), 5)], 'losing-a-predator',
         'What would happen to the population of aphids', 5, '')]
] + [
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Explain the two underlined terms.'),
      [pt(S('Ecosystem: organisms and environment'), 6), pt(S('plants'), 6, label=S('Flora:'))], 'bio-3-1',
      'ecosystem-and-flora', SQ(14, 'Explain the terms ‘ecosystem’ and ‘flora’ in the article.'), 12, stem=Q11C,
      qfig='q11c-i-question', id='bio-2022-ol-q11-c-i',
      decision='The paper marks the terms to explain by underlining them in the passage, which the text layer '
               'drops: the question is shown as printed.'),
    T('11cii', 'Q11(c)(ii)', 'C', _C(2, 'Name two activities, referred to in the article', 'pollutants in rivers.'),
      [pt(S('Sewage (or slurry) discharge'), 6), pt(S('Fertiliser runoff'), 6)], 'bio-3-1', 'sources-of-river-pollution',
      SQ(14, 'Name two activities that lead to high levels of pollutants'), 12, stem=Q11C, id='bio-2022-ol-q11-c-ii'),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'State two harmful effects, referred to in the article', 'ecosystems.'),
      [anyn(S('Fish kills / raised nitrate / lowered oxygen / overgrowth of plants'), 2, 6)], 'bio-3-1',
      'effects-of-river-pollution', SQ(14, 'State two harmful effects of pollutants'), 12, stem=Q11C,
      id='bio-2022-ol-q11-c-iii'),
    T('11civ', 'Q11(c)(iv)', 'C', _C(2, 'Name the important biomolecule in living things that requires nitrogen.'),
      [pt(S('Protein'), 6)], 'bio-1-2', 'nitrogen-in-protein', SQ(14, 'Name the important biomolecule'), 6, stem=Q11C,
      id='bio-2022-ol-q11-c-iv'),
    T('11cv', 'Q11(c)(v)', 'C', _C(2, 'Nutrient recycling is essential for healthy ecosystems.', 'nitrogen cycle.'),
      [pt(S('Bacteria or fungi or insects or worms or other correct'), 6)], 'bio-3-2', 'decomposers',
      SQ(14, 'Name a group of organisms that act as decomposers'), 6, stem=Q11C, id='bio-2022-ol-q11-c-v'),
] + [
    T(f'12a{r}', f'Q12(a)({r})', 'C', [Q12A, _C(3, term, br=True)], [pt(S(ans), 5, label=S(f'{term}:'))],
      'bio-1-4', concept, SQ(15, 'Explain the following terms used in genetics:'), 5,
      id='bio-2022-ol-q12-a' if r == 'i' else None,
      decision=bundled('(a)(i)-(iii)', '(i), and (ii), (iii) are added') if r == 'i' else '')
    for r, term, ans, concept in [
        ('i', 'Diploid', 'Two sets of chromosomes (or chromosomes in pairs)', 'diploid'),
        ('ii', 'Haploid', 'One set of chromosomes (chromosomes appear singly)', 'haploid'),
        ('iii', 'Allele', '(Different) form of a gene', 'allele')]
] + [
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'What is the cause of cystic fibrosis?'),
      [pt(S('Mutated or altered gene'), 5)], 'bio-1-4', 'cause-of-cystic-fibrosis',
      SQ(15, 'What is the cause of cystic fibrosis (CF)?'), 5, stem=Q12B, id='bio-2022-ol-q12-b-i',
      decision='The scheme\'s nine-response table under (b) holds eight printed answers; each is carded.'),
] + [
    T(f'12bii{n}', f'Q12(b)(ii){n}', 'C', [_C(3, 'State the genotype of each of the following:'),
                                         item(3, n, what, 'State the genotype')],
      rows, 'bio-1-4', concept, SQ(15, 'State the genotype of each of the following:'), 5, stem=Q12B,
      id='bio-2022-ol-q12-b-ii' if n == 1 else None,
      decision=('The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added. '
                if n == 1 else '') + EACH_ITEM)
    for n, what, rows, concept in [
        (1, 'A person who is a carrier of the CF gene.', [pt(S('Nn'), 5)], 'carrier-genotype'),
        (2, 'A person with the CF condition.', [pt(S('nn', after='2. Person with CF:'), 5)], 'cf-genotype'),
        (3, 'The possible gametes a carrier can produce.',
         [pt(S('N and n'), 5, note_sel=S('(must have gap between the two letters)'))], 'carrier-gametes')]
] + [
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'Using a Punnett square, determine the percentage chance', 'child with CF.'),
      [pt(S('nn', after='Using a Punnett square'), 5, note='The scheme\'s completed Punnett square is shown '
                                                          'after reveal.'),
       pt(S('25%'), 5)], 'bio-1-4', 'cf-punnett-square', SQ(15, 'Using a Punnett square determine'), 10, stem=Q12B,
      fig='q12b-iii-scheme', id='bio-2022-ol-q12-b-iii',
      decision='The scheme answers with a Punnett square that brackets the genotypes it does not credit and sets '
               'nn in bold: nn and 25% are its two responses, and the square is the solution figure.'),
    T('12biv', 'Q12(b)(iv)', 'C', _C(3, 'What genotype should one parent have', 'the CF condition?'),
      [pt(S('NN'), 5)], 'bio-1-4', 'protective-genotype', SQ(15, 'Genotype that at least one parent must be'), 5,
      stem=Q12B, id='bio-2022-ol-q12-b-iv'),
    T('12bv', 'Q12(b)(v)', 'C', _C(3, 'What is the purpose of genetic screening?'),
      [pt(S('Detecting a (mutated) gene'), 5)], 'bio-1-4', 'genetic-screening',
      SQ(15, 'What is the purpose of genetic screening?'), 5, stem=Q12B, id='bio-2022-ol-q12-b-v'),
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'Explain the underlined term.'),
      [pt(S('(Resting period of the cell cycle) when the cell is not dividing'), 6)], 'bio-2-3', 'interphase',
      SQ(15, 'Explain interphase.'), 6, stem=[Q12C], qfig='q12c-i-question', id='bio-2022-ol-q12-c-i',
      decision='The paper marks the term to explain by underlining it: the question is shown as printed.'),
    T('12cii', 'Q12(c)(ii)', 'C', _C(3, 'Describe the process of mitosis.', 'answer.'),
      [pt(S('Chromosomes become visible or chromosome duplicate or nucleus disappears or', '(spindle) fibres form'), 6),
       pt(S('Chromosomes line up (on the equator) or fibres attach to chromosomes'), 6),
       pt(S('Chromosomes are pulled apart to opposite ends of the cell'), 6),
       pt(S('Nuclear membranes form around each set of chromosomes or two nuclei form or cell', 'divides in two'), 6)],
      'bio-2-3', 'mitosis', SQ(15, 'Describe the process of mitosis.'), 24, stem=[Q12C], id='bio-2022-ol-q12-c-ii'),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Name another form of cell division that introduces variation', 'daughter cells.'),
      [pt(S('Meiosis'), 6)], 'bio-2-3', 'meiosis', SQ(15, 'Name another form of cell division.'), 6, stem=[Q12C],
      id='bio-2022-ol-q12-c-iii'),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Name one cell in the human body produced by', 'at part (c) (iii) above.'),
      [pt(S('Egg (in the female) or sperm (in the male)'), 6)], 'bio-2-3', 'cells-made-by-meiosis',
      SQ(15, 'Name one cell in the human body produced'), 6, stem=Q12CIII, id='bio-2022-ol-q12-c-iv'),
    T('12cv', 'Q12(c)(v)', 'C', _C(3, 'Name one organ in the human body in which', 'at part (c) (iii) above occurs.'),
      [pt(S('Ovary or testis (does not have to match (iv))'), 6)], 'bio-2-3', 'where-meiosis-happens',
      SQ(15, 'Name one organ in the human body in which'), 6, stem=Q12CIII, id='bio-2022-ol-q12-c-v'),
    T('13ai', 'Q13(a)(i)', 'C', _C(4, 'Where are the lungs located in the body?'),
      [pt(S('Chest or inside rib cage or thorax'), 5)], 'bio-2-6', 'where-the-lungs-are',
      SQ(16, 'Where are the lungs located?'), 5, id='bio-2022-ol-q13-a-i'),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'Name two substances excreted by the lungs.'),
      [pt(S('Water'), 5), pt(S('Carbon dioxide'), 5)], 'bio-2-6', 'excreted-by-the-lungs',
      SQ(16, 'Name two substances excreted by the lungs.'), 10, id='bio-2022-ol-q13-a-ii'),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Name the parts A, B, C.'),
      [pt(S('Larynx (voice box)'), 5, label=S('A:')), pt(S('Bronchus'), 5, label=S('B:')),
       pt(S('Bronchiole'), 5, label=S('C:'))], 'bio-2-6', 'parts-of-the-breathing-system',
      SQ(16, 'Name the parts A, B, C in the diagram'), 15, stem=[Q13B], fig='q13-breathing', labels=L_LUNGS,
      id='bio-2022-ol-q13-b-i'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'What is the function of the', 'trachea?'),
      [pt(S('Carry air in and out of the lungs'), 5)], 'bio-2-6', 'trachea', SQ(16, 'What is the function of the trachea?'),
      5, stem=[Q13B], fig='q13-breathing', id='bio-2022-ol-q13-b-ii'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Name the two muscles involved in', 'breathing.'),
      [pt(S('Diaphragm'), 5), pt(S('Intercostal (muscles)'), 5)], 'bio-2-6', 'breathing-muscles',
      SQ(16, 'Name the two muscles involved in breathing.'), 10, stem=[Q13B], fig='q13-breathing',
      id='bio-2022-ol-q13-b-iii'),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'Name the small air-sacs in the lungs,', 'in which gas exchange occurs.'),
      [pt(S('Alveoli'), 5)], 'bio-2-6', 'alveoli', SQ(16, 'Name the small air-sacs in the lungs'), 5, stem=[Q13B],
      fig='q13-breathing', labels=asked(L_LUNGS), id='bio-2022-ol-q13-b-iv'),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'Give two ways in which these', 'their function.'),
      [anyn(S('Thin walled / surrounded by capillaries / moisture layer / elastic'), 2, 5)], 'bio-2-6',
      'adaptations-of-alveoli', SQ(16, 'Give two ways in which these air-sacs are adapted'), 10, fig='q13-breathing',
      stem=[Q13B, M('(iv)', 4), _C(4, 'Name the small air-sacs in the lungs,', 'in which gas exchange occurs.')],
      id='bio-2022-ol-q13-b-v'),
] + [
    T(f'13ci{n}-{route}', f'Q13(c)(i){n}', 'C', [_C(4, 'Write down the name of one of the conditions and:'),
                                                item(4, n, what, 'Write down the name')],
      [pt(S(*sel), 6)], 'bio-2-6', f'{route}-{concept}', SQ(17, sq, nth=1 if route == 'asthma' else 2), 6,
      stem=Q13C, route=route, id=f'bio-2022-ol-q13-c-i-{route}' if n == 1 else None,
      decision=('The old cards carded each condition with items 1-3 together; each keeps its id for item 1, and '
                '2. and 3. are added. ' if n == 1 else '')
      + 'Closed choose-one pool of two printed conditions, each with its own scheme column: one card per item '
        'and condition.')
    for n, what, sq, concept, route, sel in [
        (1, 'Give a symptom of the named condition.', '1. Give a symptom.', 'symptom', 'asthma',
         ('Difficulty breathing or tightening of', 'inflammation')),
        (1, 'Give a symptom of the named condition.', '1. Give a symptom.', 'symptom', 'bronchitis',
         ('Inflammation or cough or pain',)),
        (2, 'Describe a cause.', '2. Describe a cause.', 'cause', 'asthma',
         ('Presence of cold air or dust or allergens',)),
        (2, 'Describe a cause.', '2. Describe a cause.', 'cause', 'bronchitis',
         ('Presence of pathogen (or infection) or', 'smoking')),
        (3, 'Suggest a possible treatment.', '3. Suggest a possible treatment.', 'treatment', 'asthma',
         ('Inhaler or avoid allergen or medication', '(or named medication)')),
        (3, 'Suggest a possible treatment.', '3. Suggest a possible treatment.', 'treatment', 'bronchitis',
         ('Medication or antibiotics or pain killers or give', 'up smoking'))]
] + [
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Describe how an athlete might have measured either breathing or pulse rate.'),
      [pt(S('Count'), 6), pt(S('per minute'), 6)], 'bio-2-6', 'measuring-breathing-or-pulse',
      SQ(17, 'Describe how an athlete measured either breathing or pulse rate.'), 12, stem=[Q13CX],
      id='bio-2022-ol-q13-c-ii',
      decision='"Either breathing or pulse rate": the scheme marks both on the same rows; one card.'),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'After measuring the resting rate, what other steps', 'the investigation?'),
      [pt(S('Exercised'), 6), pt(S('count again'), 6)], 'bio-2-6', 'completing-the-exercise-investigation',
      SQ(17, 'What other steps would the athlete carry out'), 12, stem=[Q13CX], id='bio-2022-ol-q13-c-iii'),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'What is the effect of increased exercise on either breathing or pulse rate?'),
      [pt(S('Increased'), 6)], 'bio-2-6', 'effect-of-exercise', SQ(17, 'What is the effect of increased exercise'), 6,
      stem=[Q13CX], id='bio-2022-ol-q13-c-iv',
      decision='"Either breathing or pulse rate": one answer for both; one card.'),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'What is an enzyme?'),
      [pt(S('Protein'), 5), pt(S('catalyst'), 5)], 'bio-2-1', 'enzyme', SQ(18, 'What is an enzyme?'), 10,
      id='bio-2022-ol-q14-a-i'),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Name one factor that affects the rate of action of an enzyme.'),
      [pt(S('pH or temperature or substrate (or product) concentration'), 5)], 'bio-2-1', 'enzyme-rate-factors',
      SQ(18, 'Name one factor that affects the rate'), 5, id='bio-2022-ol-q14-a-ii'),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'Photosynthesis is an anabolic process.', 'Explain the term anabolic.'),
      [pt(S('Building up of large (molecules) from smaller molecules (using energy)'), 5)], 'bio-2-2', 'anabolic',
      SQ(18, 'Explain the term anabolic.'), 5, id='bio-2022-ol-q14-b-i'),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Name the cell organelle in which photosynthesis occurs.'),
      [pt(S('Chloroplast'), 5)], 'bio-2-2', 'chloroplast', SQ(18, 'Name the cell organelle in which photosynthesis'),
      5, id='bio-2022-ol-q14-b-ii'),
    T('14biii', 'Q14(b)(iii)', 'C', _C(5, 'Name the pigment that absorbs light energy for photosynthesis.'),
      [pt(S('Chlorophyll'), 5)], 'bio-2-2', 'chlorophyll', SQ(18, 'Name the pigment that absorbs light energy'), 5,
      id='bio-2022-ol-q14-b-iii'),
    T('14biv', 'Q14(b)(iv)', 'C', _C(5, 'Cx(H2O)y is the general formula for one of the products', 'formula represent?'),
      [pt(S('Carbohydrate (or sugars)'), 5)], 'bio-1-2', 'carbohydrate-formula',
      SQ(18, 'What group of biomolecules does this general formula represent?'), 5, qfig='q14b-iv-question',
      id='bio-2022-ol-q14-b-iv',
      decision='The formula prints its x, 2 and y as subscripts, which the text layer flattens: the question is '
               'shown as printed.'),
    T('14bv1', 'Q14(b)(v)1', 'C', item(5, 1, 'splitting of water.', 'During photosynthesis water'),
      [pt(S('Hydrogen ions or H+'), 5), pt(S('Electrons or e–'), 5)], 'bio-2-2', 'products-of-splitting-water',
      SQ(18, '1. Name the other two products produced'), 10, stem=[Q14BV], id='bio-2022-ol-q14-b-v-1'),
    T('14bv2', 'Q14(b)(v)2', 'C', item(5, 2, 'fate for the oxygen.', 'During photosynthesis water'),
      [pt(S('Released to the atmosphere or used in respiration'), 5)], 'bio-2-2', 'fate-of-oxygen',
      SQ(18, '2. Give one possible fate for the oxygen.'), 5, stem=[Q14BV], id='bio-2022-ol-q14-b-v-2'),
    T('14bvi1', 'Q14(b)(vi)1', 'C', item(5, 1, 'source for the carbon dioxide.', 'Carbon dioxide is absorbed'),
      [pt(S('Atmosphere or respiration'), 5)], 'bio-2-2', 'source-of-carbon-dioxide',
      SQ(18, '1. State a source of CO₂.'), 5, stem=[Q14BVI], id='bio-2022-ol-q14-b-vi-1'),
    T('14bvi2', 'Q14(b)(vi)2', 'C', item(5, 2, 'enters plants.', 'Carbon dioxide is absorbed'),
      [pt(S('Stomata (allow lenticels)'), 5)], 'bio-2-2', 'carbon-dioxide-entry',
      SQ(18, '2. Structure through which CO2 enters plants.'), 5, stem=[Q14BVI], id='bio-2022-ol-q14-b-vi-2'),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'Explain the term osmosis.'),
      [anyn(S('Movement of water / across a membrane / from dilute to concentrated solution.'), 2, 6)], 'bio-2-6',
      'osmosis', SQ(19, 'Explain the term ‘osmosis’.'), 12, stem=[Q14C1], id='bio-2022-ol-q14-c-i'),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'Explain the term turgor.'),
      [pt(S('(Water in the) cytoplasm pushes the cell membrane out against the cell wall'), 6)], 'bio-2-6', 'turgor',
      SQ(19, 'Explain the term ‘turgor’.'), 6, stem=[Q14C2], fig='q14-cells', id='bio-2022-ol-q14-c-ii'),
    T('14ciii', 'Q14(c)(iii)', 'C', _C(5, 'Which cell, A or B, is turgid?'),
      [pt(S('Cell A'), 6)], 'bio-2-6', 'turgid-cell', SQ(19, 'Which cell is turgid?'), 6, stem=[Q14C2],
      fig='q14-cells', id='bio-2022-ol-q14-c-iii'),
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'Name the cell part that prevents a plant cell from bursting.'),
      [pt(S('Cell wall'), 6)], 'bio-2-6', 'cell-wall', SQ(19, 'Name cell part that prevents bursting of cell.'), 6,
      stem=[Q14C2], fig='q14-cells', id='bio-2022-ol-q14-c-iv'),
    T('14cv', 'Q14(c)(v)', 'C', _C(5, 'Name organelle X, an important storage organelle in plant cells.'),
      [pt(S('Vacuole'), 6)], 'bio-2-6', 'vacuole', SQ(19, 'Name organelle X.'), 6, stem=[Q14C2], fig='q14-cells',
      id='bio-2022-ol-q14-c-v'),
    T('14cvi', 'Q14(c)(vi)', 'C', _C(5, 'Explain in detail what has happened to cell B.'),
      [pt(S('Cell membrane has peeled away from the cell wall (or plasmolysis)'), 6), pt(S('Due to a loss of water'), 6)],
      'bio-2-6', 'plasmolysis', SQ(19, 'Explain what has happened to cell B.'), 12, stem=[Q14C2], fig='q14-cells',
      id='bio-2022-ol-q14-c-vi'),
    T('15ai', 'Q15(a)(i)', 'C', _C(6, 'Name the growth response in which plant stems grow towards light.'),
      [pt(S('Phototropism'), 5)], 'bio-2-4', 'phototropism', SQ(20, 'Name the growth response'), 5,
      id='bio-2022-ol-q15-a-i'),
    T('15aii', 'Q15(a)(ii)', 'C', _C(6, 'How do plants benefit from increased light intensity?'),
      [pt(S('Increased photosynthesis or more food'), 5)], 'bio-2-4', 'benefit-of-light',
      SQ(20, 'How do plants benefit from increased light intensity?'), 5, id='bio-2022-ol-q15-a-ii'),
    T('15aiii', 'Q15(a)(iii)', 'C', _C(6, 'Name another environmental factor that regulates plant growth.'),
      [pt(S('Day length or gravity or touch or water or chemicals (or named environmental chemical)', 'or temperature'),
          5)], 'bio-2-4', 'growth-regulating-factors', SQ(20, 'Name another environmental factor'), 5,
      id='bio-2022-ol-q15-a-iii'),
    T('15bi', 'Q15(b)(i)', 'C', _C(6, 'Name the tissues labelled A and B.'),
      [pt(S('Dermal'), 5, label=S('A:')), pt(S('Ground'), 5, label=S('B:'))], 'bio-2-6', 'stem-tissues',
      SQ(20, 'Name the tissues labelled A and B.'), 10, stem=[Q15B], fig='q15-stem', labels=asked(L_STEM, 'A', 'B'),
      id='bio-2022-ol-q15-b-i'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'State a function for each of the tissues you named at part (b) (i) above.'),
      [pt(S('protection'), 5, label=S('A:')), pt(S('support or storage'), 5, label=S('B:'))], 'bio-2-6',
      'functions-of-stem-tissues', SQ(20, 'Function of tissues A and B.'), 10,
      stem=[Q15B, M('(i)', 6), _C(6, 'Name the tissues labelled A and B.')], fig='q15-stem', labels=asked(L_STEM),
      id='bio-2022-ol-q15-b-ii'),
    T('15biii', 'Q15(b)(iii)', 'C', _C(6, 'Name the structure labelled C.'),
      [pt(S('Vascular bundle'), 5)], 'bio-2-6', 'vascular-bundle', SQ(20, 'Name the structure C.'), 5, stem=[Q15B],
      fig='q15-stem', labels=asked(L_STEM, 'C'), id='bio-2022-ol-q15-b-iii'),
    T('15biv', 'Q15(b)(iv)', 'C', _C(6, 'Name the cells found in structure C that transport water.'),
      [pt(S('Xylem vessel or xylem tracheids'), 5)], 'bio-2-6', 'xylem', SQ(20, 'Name the cells found in structure C '
                                                                                'that transports water.'), 5,
      stem=[Q15B], fig='q15-stem', labels=asked(L_STEM), id='bio-2022-ol-q15-b-iv'),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'Name the cells found in structure C that transport food.'),
      [pt(S('Phloem sieve tube cells (accept companion cells)'), 5)], 'bio-2-6', 'phloem',
      SQ(20, 'Name the cells found in structure C that transports food.'), 5, stem=[Q15B], fig='q15-stem',
      labels=asked(L_STEM), id='bio-2022-ol-q15-b-v'),
    T('15bvi', 'Q15(b)(vi)', 'C', _C(6, 'State one way in which a section through a root', 'section above.'),
      [pt(S('Vascular tissue at the centre or root hairs'), 5)], 'bio-2-6', 'root-and-stem-sections',
      SQ(20, 'State one way in which a section through a root'), 5, stem=[Q15B], fig='q15-stem',
      id='bio-2022-ol-q15-b-vi'),
    T('15bvii', 'Q15(b)(vii)', 'C', _C(6, 'State one reason why the diagram above represents', 'plant stem.'),
      [pt(S('Vascular bundles in a ring'), 5)], 'bio-2-6', 'dicot-stem', SQ(20, 'State one reason why the diagram'), 5,
      stem=[Q15B], fig='q15-stem', id='bio-2022-ol-q15-b-vii'),
] + [
    T(f'15ci{n}', f'Q15(c)(i){n}', 'C', [_C(6, 'In your answer book, state which letter represents', 'following parts:'),
                                       item(6, n, part, 'In your answer book')],
      [pt(S(letter), 6)], 'bio-2-5', concept, SQ(20, 'In your answer book, state which letter'), 6, stem=[Q15C],
      fig='q15-flower', id='bio-2022-ol-q15-c-i-fig' if n == 1 else None,
      decision=('The old card bundled items 1-3; it keeps its id for 1., and 2. and 3. are added. '
                if n == 1 else '') + EACH_ITEM)
    for n, part, letter, concept in [(1, 'Stigma', 'X', 'stigma'), (2, 'Sepal', 'Z', 'sepal'),
                                     (3, 'Anther.', 'Y', 'anther')]
] + [
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Name the structure in the flower that forms the fruit.'),
      [pt(S('Ovary or receptacle'), 6)], 'bio-2-5', 'fruit-formation', SQ(20, 'Name the structure in the flower'), 6,
      stem=[Q15C], fig='q15-flower', id='bio-2022-ol-q15-c-ii'),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Explain the term pollination.'),
      [pt(S('Transfer of pollen'), 6), pt(S('from anther to stigma (or from Y to X)'), 6)], 'bio-2-5', 'pollination',
      SQ(20, 'Explain the term pollination.'), 12, stem=[Q15C], fig='q15-flower', id='bio-2022-ol-q15-c-iii'),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'Name two methods by which plants are pollinated.'),
      [anyn(S('Wind / animal (e.g. insect, bird, other correct) / water / self'), 2, 6)], 'bio-2-5',
      'methods-of-pollination', SQ(20, 'Name two methods by which plants are pollinated.'), 12,
      id='bio-2022-ol-q15-c-iv'),
    # Q16 -------------------------------------------------------------------
    T('16ai', 'Q16(a)(i)', 'C', _C(7, 'Name the parts labelled A, B, C, D.'),
      [pt(S('Penis'), 7, label=S('A:')), pt(S('Sperm duct (vas deferens)'), 7, label=S('B:')),
       pt(S('Testes'), 7, label=S('C:')), pt(S('Urethra'), 7, label=S('D:'))], 'bio-2-5',
      'male-reproductive-system', SQ(21, 'Name the parts labelled A, B, C, D.'), 28, stem=[Q16A], fig='q16-male',
      labels=L_MALE, id='bio-2022-ol-q16-a-i-fig'),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'Name the male hormone produced by the structure labelled C.'),
      [pt(S('Testosterone'), 7)], 'bio-2-5', 'testosterone', SQ(21, 'Name the male hormone'), 7, stem=[Q16A],
      fig='q16-male', labels=asked(L_MALE), id='bio-2022-ol-q16-a-ii'),
    T('16aiii', 'Q16(a)(iii)', 'C', _C(7, 'Give one function of the hormone named at part (ii) above.'),
      [pt(S('Male sexual characteristics (accept example) or male primary sex organ development or',
            'sperm production'), 7)], 'bio-2-5', 'role-of-testosterone', SQ(21, 'Give one function of the hormone'), 7,
      stem=[Q16A, M('(ii)', 7), _C(7, 'Name the male hormone produced by the structure labelled C.')],
      fig='q16-male', labels=asked(L_MALE), id='bio-2022-ol-q16-a-iii'),
    T('16aiv', 'Q16(a)(iv)', 'C', _C(7, 'What is meant by the term infertility?'),
      [pt(S('Inability to produce gametes or inability to have children'), 7)], 'bio-2-5', 'infertility',
      SQ(21, 'What is meant by the term'), 7, id='bio-2022-ol-q16-a-iv'),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'Give a cause of infertility.'),
      [pt(S('Low sperm count or low sperm motility or blockage in fallopian tubes or hormonal'), 7)], 'bio-2-5',
      'causes-of-infertility', SQ(21, 'Give a cause of infertility.'), 7, id='bio-2022-ol-q16-a-v'),
    T('16avi', 'Q16(a)(vi)', 'C', _C(7, 'Explain the term contraception and give one example.'),
      [pt(S('Method of preventing pregnancy'), 7, label=S('Explain:')),
       pt(S('Example: Barrier or chemical or natural or surgical or any valid examples'), 7)], 'bio-2-5',
      'contraception', SQ(21, 'Explain the term'), 14, id='bio-2022-ol-q16-a-vi'),
    T('16bi', 'Q16(b)(i)', 'C', _C(7, 'Draw a large labelled diagram of a typical bacterial cell.'),
      [pt(S('Diagram: Includes cell wall and cell membrane and indication of DNA'), 7, kind='criterion'),
       anyn(S('Cell wall / cell membrane / cytoplasm / DNA / plasmid'), 2, 7)], 'bio-3-2', 'drawing-a-bacterium',
      SQ(21, 'Draw a large labelled diagram of a typical bacterial cell.'), 21, id='bio-2022-ol-q16-b-i'),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Name two bacterial shapes.'),
      [anyn(S('Rods / cocci (round) / spiral'), 2, 7)], 'bio-3-2', 'bacterial-shapes',
      SQ(21, 'Name two bacterial shapes.'), 14, id='bio-2022-ol-q16-b-ii'),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'Explain the term binary fission.'),
      [pt(S('(Asexual) reproduction'), 7)], 'bio-3-2', 'binary-fission', SQ(21, 'Explain the term ‘binary fission’.'), 7,
      id='bio-2022-ol-q16-b-iii'),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'What term is used to describe bacteria and other microorganisms', 'disease?'),
      [pt(S('Pathogen(ic)'), 7)], 'bio-3-2', 'pathogens', SQ(21, 'What term is used to describe bacteria'), 7,
      id='bio-2022-ol-q16-b-iv'),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'What are antibiotics?'),
      [pt(S('Chemicals (produced by microorganisms)'), 7), pt(S('that kill bacteria'), 7)], 'bio-3-2', 'antibiotics',
      SQ(21, 'What are antibiotics?'), 14, id='bio-2022-ol-q16-b-v'),
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'Describe a disadvantage of the overuse of antibiotics.'),
      [pt(S('Resistance builds up (in pathogens)'), 7)], 'bio-3-2', 'antibiotic-resistance',
      SQ(21, 'Describe a disadvantage of the overuse of antibiotics.'), 7, id='bio-2022-ol-q16-b-vi'),
    T('16ci', 'Q16(c)(i)', 'C', _C(8, 'Give two functions of the skeleton.'),
      [anyn(S('Movement / support / protection / shape (or structure) / manufacture of blood cells'), 2, 7)],
      'bio-2-4', 'functions-of-the-skeleton', SQ(22, 'Two functions of the skeleton:'), 14, id='bio-2022-ol-q16-c-i'),
    T('16cii1', 'Q16(c)(ii)1', 'C', item(8, 1, 'axial skeleton', 'The human skeleton shown'),
      [pt(S('e.g. skull or ribs or sternum or vertebrae (or spine)'), 7, kind='criterion')], 'bio-2-4',
      'axial-skeleton', SQ(22, '1. Name any one bone in the axial skeleton.'), 7, stem=[Q16CII], fig='q16-skeleton',
      id='bio-2022-ol-q16-c-ii-1'),
    T('16cii2', 'Q16(c)(ii)2', 'C', item(8, 2, 'appendicular skeleton.', 'The human skeleton shown'),
      [pt(S('e.g. femur or humerus or other correct'), 7, kind='criterion')], 'bio-2-4', 'appendicular-skeleton',
      SQ(22, '2. Name any one bone found in the appendicular skeleton.'), 7, stem=[Q16CII], fig='q16-skeleton',
      id='bio-2022-ol-q16-c-ii-2'),
    T('16ciii', 'Q16(c)(iii)', 'C', [_C(8, 'Draw a diagram of a long bone and label the', 'following parts:'),
                                     _C(8, 'compact bone;', br=True), _C(8, 'spongy bone;', br=True),
                                     _C(8, 'bone marrow', br=True)],
      [pt(S('one annotation'), 7, kind='criterion', label=S('Diagram:'),
          note='The scheme\'s labelled long bone is shown after reveal.'),
       pt(S('three annotations'), 21, kind='criterion', units=[7, 7, 7], label=S('Labels:'))], 'bio-2-4',
      'drawing-a-long-bone', SQ(22, 'Labelled diagram of long bone.'), 28, fig='q16c-iii-scheme',
      decision='The scheme counts the drawing as one response and each of the three labels as one; its labelled '
               'drawing is the solution figure.'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Name the flexible tissue present between bones in', 'give its function.'),
      [pt(S('Cartilage'), 7), pt(S('Shock absorption or friction-free movement or protection (of end of bones)'), 7)],
      'bio-2-4', 'cartilage', SQ(22, 'Name of flexible tissue.'), 14, id='bio-2022-ol-q16-c-iv'),
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'What is meant by the term vegetative propagation?'),
      [pt(S('Asexual reproduction (in plants)'), 7)], 'bio-2-5', 'vegetative-propagation',
      SQ(22, 'What is meant by the term'), 7, stem=[Q16D], id='bio-2022-ol-q16-d-i'),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Name one method of vegetative propagation and state the plant organ involved.'),
      [anyn(None, 1, 7, options=[S('Runners', '(strawberries)'), S('Root suckers', '(holly bush)'),
                                 S('Leaflets', '(Devil’s backbone)'), S('Bulbs', '(Daffodil)')]),
       anyn(None, 1, 7, options=[S('Stem', after='Organ:'), S('Root', after='Organ:'), S('Leaf', after='Organ:'),
                                 S('Bud', after='Organ:')],
            note_sel=S('Any one (must', 'match method)'))], 'bio-2-5', 'methods-of-vegetative-propagation',
      SQ(22, 'Name one method of vegetative propagation and state organ involved.'), 14, stem=[Q16D],
      id='bio-2022-ol-q16-d-ii',
      decision='The scheme prints its examples as a table, each method above its organ: one any-one menu for '
               'the method and one for the organ, which must match it.'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Name the parts of the plant labelled A and B on the diagram.'),
      [pt(S('A: Leaf'), 7), pt(S('Stem', after='B:'), 7, label=S('B:'))], 'bio-2-5', 'grafting',
      SQ(22, 'Name parts labelled A and B.'), 14, stem=[Q16DG], fig='q16-grafting', labels=L_GRAFT,
      id='bio-2022-ol-q16-d-iii-fig'),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'Name two other methods of artificial propagation.'),
      [anyn(S('Cutting / layering / micro propagation / budding'), 2, 7)], 'bio-2-5', 'artificial-propagation',
      SQ(22, 'Name two other methods of artificial propagation.'), 14, stem=[Q16DG], fig='q16-grafting',
      id='bio-2022-ol-q16-d-iv'),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Suggest one advantage of artificial propagation for horticulturists.'),
      [pt(S('(Reproduction is) cheaper or faster or all good traits of plant retained'), 7)], 'bio-2-5',
      'advantage-of-artificial-propagation', SQ(22, 'Suggest one advantage of artificial propagation'), 7,
      stem=[Q16DG], fig='q16-grafting', id='bio-2022-ol-q16-d-v'),
] + [
    T(f'16dvi{n}', f'Q16(d)(vi){n}', 'C', item(8, n, head, 'Compare reproduction by seed'),
      [pt(S(ans), 7)], 'bio-2-5', concept, SQ(22, 'Compare reproduction by seed'), 7, stem=[Q16D, Q16DVI],
      id='bio-2022-ol-q16-d-vi' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, head, ans, concept in [(1, 'Variation', 'More (variation) (in reproduction by seed)', 'variation-from-seed'),
                                  (2, 'Dispersal.', 'Wider (dispersal) (in reproduction by seed)', 'dispersal-of-seed')]
] + [
    # Q17 -------------------------------------------------------------------
    T('17ai', 'Q17(a)(i)', 'C', _C(9, 'White matter contains axons.', 'What is the function of an axon?'),
      [pt(S('Carry nerve impulse away from cell body'), 7)], 'bio-2-4', 'axon', SQ(23, 'Function of axon.'), 7,
      stem=[Q17A], fig='q17-spinal-cord', id='bio-2022-ol-q17-a-i'),
    T('17aii', 'Q17(a)(ii)', 'C', _C(9, 'Grey matter contains cells bodies and dendrites.', 'function of dendrites?'),
      [pt(S('Carry nerve impulse towards cell body'), 7)], 'bio-2-4', 'dendrites', SQ(23, 'Function of dendrites.'), 7,
      stem=[Q17A], fig='q17-spinal-cord', id='bio-2022-ol-q17-a-ii'),
    T('17aiii', 'Q17(a)(iii)', 'C', _C(9, 'Name the nerve cells labelled A, B, C in the diagram.'),
      [pt(S('Sensory neuron'), 7, label=S('A:')), pt(S('Interneuron'), 7, label=S('B:')),
       pt(S('Motor neuron'), 7, label=S('C:'))], 'bio-2-4', 'types-of-neuron',
      SQ(23, 'Name the nerve cells labelled A, B, C in the diagram.'), 21, stem=[Q17A], fig='q17-spinal-cord',
      labels=L_SPINAL, id='bio-2022-ol-q17-a-iii-fig'),
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Give an example of a sense organ.'),
      [pt(S('Eye or ear or nose or skin or tongue'), 7)], 'bio-2-4', 'sense-organs',
      SQ(23, 'Give an example of a sense organ.'), 7, id='bio-2022-ol-q17-a-iv'),
    T('17av', 'Q17(a)(v)', 'C', _C(9, 'Name or give an example of an automatic response to a stimulus.'),
      [pt(S('Reflex or example (e.g. blinking, startle, grasp, suckling, knee jerk, iris dilation)'), 7)], 'bio-2-4',
      'reflex', SQ(23, 'Name an automatic response to a stimulus that may occur', 'in the diagram.',
                         paired='The (v) under the scheme\'s Question 17 (a): it rewords "Name or give an example of an '
                                'automatic response" and adds "through the nerve cells in the diagram".'), 7, id='bio-2022-ol-q17-a-v'),
    T('17avi', 'Q17(a)(vi)', 'C', _C(9, 'How does an automatic response to a stimulus benefit the human body?'),
      [pt(S('Protection'), 7)], 'bio-2-4', 'why-reflexes', SQ(23, 'How does this automatic response'), 7,
      id='bio-2022-ol-q17-a-vi'),
] + [
    T(f'17avii{n}', f'Q17(a)(vii){n}', 'C', item(9, n, head, 'Compare a nervous system response'),
      [pt(S(*ans), 7)], 'bio-2-4', concept, SQ(23, 'Compare a nervous system response'), 7, stem=[Q17AVII],
      id='bio-2022-ol-q17-a-vii' if n == 1 else None,
      decision=('The old card bundled items 1 and 2; it keeps its id for 1., and 2. is added. ' if n == 1 else '')
      + EACH_ITEM)
    for n, head, ans, concept in [
        (1, 'Speed', ('Nervous system is faster or hormonal is slower',), 'speed-of-response'),
        (2, 'Duration of effect.', ('Nervous effect is short lived or hormonal is long lived',), 'duration-of-response')]
] + [
    T('17bi-evolution', 'Q17(b)(i)', 'C', _C(9, 'Explain the underlined terms.'),
      [pt(S('Genetic change (in an organisms)'), 7, label=S('Evolution:')),
       pt(S('In response to the environment (over time)'), 7)], 'bio-1-5', 'evolution',
      SQ(23, 'Explain underlined terms:'), 14, stem=[Q17B], qfig='q17b-i-question', item=('evolution', 'Evolution'),
      id='bio-2022-ol-q17-b-i-evolution',
      decision='Each underlined term is explained on its own scheme rows; the shipped cards carded them '
               'separately and keep their ids, one term each. The paper marks the terms by underlining them: the '
               'question is shown as printed.'),
    T('17bi-natural-selection', 'Q17(b)(i)', 'C', _C(9, 'Explain the underlined terms.'),
      [pt(S('Natural selection: Organisms better adapted'), 7), pt(S('tend to survive'), 7),
       pt(S('and produce more offspring.'), 7)], 'bio-1-5', 'natural-selection',
      SQ(23, 'Explain underlined terms:'), 21, stem=[Q17B], qfig='q17b-i-question',
      item=('natural-selection', 'Natural selection'), id='bio-2022-ol-q17-b-i-natural-selection',
      decision='Each underlined term is explained on its own scheme rows: one card each.'),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Name both biologists who developed the theory', 'selection.'),
      [pt(S('(Charles) Darwin'), 7), pt(S('(Alfred Russell)-Wallace'), 7)], 'bio-1-5', 'darwin-and-wallace',
      SQ(23, 'Name both biologists.'), 14, stem=[Q17B], id='bio-2022-ol-q17-b-ii'),
    T('17biii', 'Q17(b)(iii)', 'C', _C(9, 'Explain the term genetic engineering.'),
      [pt(S('Alteration of genes'), 7)], 'bio-3-3', 'genetic-engineering', SQ(23, 'Explain the term'), 7,
      stem=[Q17BGE], id='bio-2022-ol-q17-b-iii'),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'Give one example of genetic engineering involving a plant', 'an animal.'),
      [pt(S('Any valid example'), 7, kind='criterion', label=S('Plant:')),
       pt(S('Animal: Any valid example'), 7, kind='criterion')], 'bio-3-3', 'examples-of-genetic-engineering',
      SQ(23, 'Give one example of genetic engineering'), 14, stem=[Q17BGE]),
    T('17ci', 'Q17(c)(i)', 'C', _C(10, 'The heart is an organ of the circulatory system.', 'of the human heart.'),
      [pt(S('Four chambers and septum and valves'), 7, kind='criterion', label=S('Diagram:')),
       pt(S('Any two correct labels'), 14, kind='criterion', units=[7, 7], label=S('Labels:'))], 'bio-2-6',
      'drawing-the-heart', SQ(24, 'Heart diagram and internal structures.'), 21, stem=[Q17C], id='bio-2022-ol-q17-c-i'),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'The diagram shows two cell types (X and Y)', 'Name the two cell types X and Y.'),
      [pt(S('Red blood cell'), 7, label=S('X:')), pt(S('White blood cell'), 7, label=S('Y:'))], 'bio-2-6',
      'blood-cells', SQ(24, 'Name the two cell types X and Y.'), 14, stem=[Q17C], fig='q17-blood', labels=L_BLOOD,
      id='bio-2022-ol-q17-c-ii-fig'),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Platelets are another cell type', 'Give one role of platelets.'),
      [pt(S('Clotting'), 7)], 'bio-2-6', 'platelets', SQ(24, 'One role of platelets:'), 7, stem=[Q17C],
      id='bio-2022-ol-q17-c-iii'),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Name any two blood groups found in humans.'),
      [anyn(S('A / B / AB / O / or other correct'), 2, 7)], 'bio-2-6', 'blood-groups',
      SQ(24, 'Name any two blood groups found in humans.'), 14, stem=[Q17C], id='bio-2022-ol-q17-c-iv'),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'Name the other system that carries fluid within the body.'),
      [pt(S('Lymphatic'), 7)], 'bio-2-6', 'lymphatic-system', SQ(24, 'Name the other system.'), 7, stem=[Q17C],
      id='bio-2022-ol-q17-c-v'),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'Name the fluid carried by the system named at part (c) (v) above.'),
      [pt(S('Lymph'), 7)], 'bio-2-6', 'lymph', SQ(24, 'Name the fluid carried.'), 7,
      stem=[Q17C, M('(v)', 10), _C(10, 'Name the other system that carries fluid within the body.')],
      id='bio-2022-ol-q17-c-vi'),
    T('17di', 'Q17(d)(i)', 'C', _C(10, 'Distinguish between autotrophic and heterotrophic nutrition', 'sentence on each.'),
      [pt(S('(Organisms) make their own food'), 7, label=S('Autotrophic:')),
       pt(S('(Organisms) obtain food from other organisms'), 7, label=S('Heterotrophic:'))], 'bio-1-1',
      'autotrophs-and-heterotrophs', SQ(24, 'Distinguish between autotrophic and heterotrophic nutrition.'), 14,
      id='bio-2022-ol-q17-d-i'),
    T('17dii1', 'Q17(d)(ii)1', 'C', item(10, 1, 'take place in the mouth.', 'Chemical digestion and mechanical'),
      [pt(S('Enzymes breakdown food'), 7, label=S('Chemical:')),
       pt(S('Mechanical: Chewing or action of tongue or swallowing'), 7)], 'bio-2-6', 'digestion-in-the-mouth',
      SQ(24, '1. Describe how both types of digestion occur in mouth.'), 14, stem=[Q17DII],
      id='bio-2022-ol-q17-d-ii-1'),
    T('17dii2', 'Q17(d)(ii)2', 'C', item(10, 2, 'of digestion take place.', 'Chemical digestion and mechanical'),
      [pt(S('Stomach (or other correct)'), 7)], 'bio-2-6', 'where-both-digestions-happen',
      SQ(24, '2. Name one other location.'), 7, stem=[Q17DII], id='bio-2022-ol-q17-d-ii-2'),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'What is the name given to the muscular contractions', 'alimentary canal?'),
      [pt(S('Peristalsis'), 7)], 'bio-2-6', 'peristalsis', SQ(24, 'Muscular contraction of the alimentary canal.'), 7,
      id='bio-2022-ol-q17-d-iii'),
    T('17div', 'Q17(d)(iv)', 'C', [_C(10, 'The list below shows some of the organs of the alimentary canal.',
                                       'starting with the mouth.'),
                                   _C(10, 'mouth;', br=True),
                                   _C(10, 'stomach; rectum; large intestine; small intestine; oesophagus', br=True)],
      [pt(S('→ oesophagus → stomach → small intestine → large intestine → rectum'), 7,
          note_sel=S('All or nothing'))], 'bio-2-6', 'order-of-the-alimentary-canal',
      SQ(24, 'Correct order of the alimentary canal organs.'), 7, id='bio-2022-ol-q17-d-iv'),
    T('17dv', 'Q17(d)(v)', 'C', _C(10, 'Egestion is a necessary part of the process of nutrition.', 'term egestion?'),
      [pt(S('Egestion is the getting rid of undigested food'), 7)], 'bio-2-6', 'egestion',
      SQ(24, 'What is meant by egestion?'), 7, id='bio-2022-ol-q17-d-v'),
    T('17dvi', 'Q17(d)(vi)', 'C', _C(10, 'Symbiotic bacteria are present in the alimentary canal.', 'these bacteria.'),
      [anyn(S('Make vitamins / digest cellulose / prevent harmful microorganisms from growing'), 2, 7)], 'bio-2-6',
      'gut-bacteria', SQ(24, 'Two functions of symbiotic bacteria.'), 14, id='bio-2022-ol-q17-d-vi'),
]

FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    'q3-rhizopus': ('038', 4, (140, 88, 445, 350), SEC, ['A', 'B', 'C'],
                    'Drawing of Rhizopus: upright stalks rising from a branching network, each ending in a round '
                    'head; arrow A points to one round head, arrow B to a horizontal thread running along the surface, '
                    'arrow C to the branched threads growing down at the base, and arrows labelled Spores point to '
                    'the dots released from a burst head.', False),
    'q4-skin': ('038', 5, (130, 86, 492, 336), SEC, ['A', 'B'],
                'Drawing of a section through human skin: arrow A points to a hair rising out of the surface, arrow '
                'B to a small bulging structure beside the hair below the surface; labels point to a coiled Sweat '
                'gland on the left and a looped Blood vessel on the right.', False),
    'q5-profiles': ('038', 6, (145, 100, 480, 343), SEC, [],
                    'DNA profiles: a column of dark bands labelled Crime scene, and beside it three columns of bands '
                    'labelled A, B and C, each with its own pattern of bands at different heights.', False),
    'q8-table': ('038', 8, (111, 473, 542, 583), SEC, [],
                 'Table of ticks at five stations: Plantain ticked at stations 2, 4 and 5; Daisy at stations 1, 2, 3 '
                 'and 5; Dandelion at stations 1 and 3.', False),
    'q10-germination': ('038', 10, (110, 223, 548, 390), SEC, [],
                        'Four test tubes of seeds: A, seeds in dry cotton wool at 20 °C; B, seeds in wet cotton wool '
                        'at 20 °C; C, seeds in boiled water at 20 °C under an oil layer; D, seeds in wet cotton wool '
                        'at 4 °C.', False),
    'q11-food-web': ('040', 2, (340, 196, 545, 426), SEC, [],
                     'Food web drawn with arrows: Grass, Blackberry, Grasshopper, Hare, Aphid, Shrew, Spider, '
                     'Blackbird, Owl and Fox, each pictured and named, with arrows running from each food to the '
                     'animals that eat it.', False),
    'q11c-i-question': ('040', 2, (80, 456, 545, 602), SEC, [],
                        'The printed question: (c) Read the following passage and answer the questions that follow, '
                        'the EPA passage on nitrogen in Ireland\'s rivers in which the words ecosystems and flora are '
                        'underlined, then (i) Explain the two underlined terms.', False),
    'q12b-iii-scheme': ('scheme', 15, (100, 282, 225, 350), SEC, [],
                        "The marking scheme's Punnett square: N and n along the top, N and n down the side; the "
                        'boxes read (NN) and (Nn) in the top row, (Nn) and nn in the bottom row, with nn in bold; '
                        'below it, 25%.', True),
    'q12c-i-question': ('040', 3, (80, 514, 480, 551), SEC, [],
                        'The printed question: (c) The cell cycle consists of two stages, interphase and mitosis (cell '
                        'division). The word interphase is underlined. (i) Explain the underlined term.', False),
    'q13-breathing': ('040', 4, (330, 112, 545, 332), SEC, ['A', 'B', 'C'],
                      'Drawing of the human breathing system: arrow A points to the box-like structure at the top of '
                      'the windpipe, arrow B to one of the two tubes the windpipe divides into, arrow C to the smaller '
                      'branching tubes inside a lung; labels point to the Trachea, the Small air-sacs and the '
                      'Muscles between the ribs and below the lungs.', False),
    'q14b-iv-question': ('040', 5, (108, 206, 510, 242), SEC, [],
                         'The printed question: (iv) Cx(H2O)y is the general formula for one of the products of '
                         'photosynthesis, with x, 2 and y set as subscripts. What group of biomolecules does this '
                         'general formula represent?', False),
    'q14-cells': ('040', 5, (160, 480, 460, 608), SEC, ['A', 'B', 'X'],
                  'Two plant cells. A: the cell contents fill the cell wall. B: the contents have shrunk away from the '
                  'wall. Labels point to the Nucleus and the Cell membrane, and arrows labelled X point to the large '
                  'central space in each cell.', False),
    'q15-stem': ('040', 6, (180, 135, 420, 297), SEC, ['A', 'B', 'C'],
                 'Drawing of a section through a plant stem: a circle with a ring of small oval bundles near its edge; '
                 'arrow A points to the outer edge of the circle, arrow B to the tissue filling the centre, and a '
                 'bracket C marks one of the oval bundles.', False),
    'q15-flower': ('040', 6, (220, 468, 445, 620), SEC, ['X', 'Y', 'Z'],
                   'Drawing of a section through a flower: arrow X points to the tip of the central stalk, arrow Y to '
                   'the head of one of the stalks around it, arrow Z to one of the small leaf-like parts at the base.',
                   False),
    'q16-male': ('040', 7, (178, 105, 400, 360), SEC, ['A', 'B', 'C', 'D'],
                 'Drawing of the human male reproductive system, side view: a label points to the Bladder; arrow A '
                 'points to the organ hanging at the front, arrow B to the tube looping up from below, arrow C to the '
                 'oval body in the sac, arrow D to the tube running through the organ at the front.', False),
    'q16-skeleton': ('040', 8, (395, 52, 525, 340), SEC, [],
                     'Photograph of a human skeleton, standing, front view.', False),
    'q16c-iii-scheme': ('scheme', 22, (80, 198, 374, 280), SEC, [],
                        "The marking scheme's labelled long bone: a bone with a knob at each end, Compact bone "
                        'labelled along the shaft wall, Spongy bone at one end and Bone marrow in the hollow '
                        'centre of the shaft.', True),
    'q16-grafting': ('040', 8, (205, 405, 410, 600), SEC, ['A', 'B'],
                     'Drawing of grafting: a young plant with arrow A pointing to one of its leaves and arrow B to its '
                     'main upright part; a box on it is shown enlarged beside it, a cut piece fitted into a notch and '
                     'bound in place.', False),
    'q17-spinal-cord': ('040', 9, (115, 105, 540, 282), SEC, ['A', 'B', 'C'],
                        'Drawing of a section through the spinal cord: grey matter shaped like a butterfly inside '
                        'white matter, labelled. A nerve pathway runs from a Sense organ on the right, arrow A '
                        'pointing to the nerve cell carrying it in, arrow B to the short cell inside the grey matter, '
                        'and arrow C to the cell leading out to the Effector.', False),
    'q17b-i-question': ('040', 9, (80, 530, 540, 567), SEC, [],
                        'The printed question: (b) The theory of evolution by natural selection was developed by two '
                        'famous biologists. The words evolution and natural selection are underlined. (i) Explain the '
                        'underlined terms.', False),
    'q17-blood': ('040', 10, (185, 150, 440, 272), SEC, ['X', 'Y'],
                  'Two kinds of blood cell. X: several smooth discs, dented in the middle. Y: a single larger rounded '
                  'cell with a lobed dark centre.', False),
}
