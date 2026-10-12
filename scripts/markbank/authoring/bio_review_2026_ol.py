"""Biology 2026 Ordinary Level — reviewed task ledger.

Independent visual sweep (2026-10-11), every page rendered and read:
  * LC025GLP038EV (Sections A and B and Answerbook), 36 pages: p1 cover, p2
    instructions, p3-p11 Questions 1-10, p12 Section C answerbook
    instructions, p13-p14 graph paper, p15-p34 ruled answer pages, p35
    acknowledgements, p36 back cover.
  * LC025GLP040EV (Section C), 12 pages: p1 cover, p2-p10 Questions 11-17,
    p11 acknowledgements, p12 back cover.
  * LC025GLP000EV (marking scheme), 36 pages: p1 cover, p2 note, p3
    introduction, p4-p5 marking examples, p6 annotations and grading table, p7
    Irish-medium bonus, p8-p32 Questions 1-17, p33-p35 blank, p36 back cover.

The Ordinary scheme prices each question (Section A) or part (Sections B and
C) on a "Number of correct responses" ladder: n(m) means every correct
response is worth m. Questions 2, 5 and 6 are "6(3) + (2)": seven responses,
the first six at 3 and the seventh at 2, 20 in all, so each response is
carded at 3 and LADDERS pins the ladder that makes the printed 20.

Task boundary rule, as at Higher: one task per printed address the scheme
prices. A MATCHING exercise (one instruction pairing a fixed set of letters or
terms, its items numbered 1., 2., 3.) is one task with a row per item: the
items share one pool, and as separate cards each would print the other
letters' meanings beside it. Independent numbered asks (14(b)(iii) 1. and 2.)
are separate tasks. Q7(a)'s table prices each of its seven named parts as one
response; seven required rows exceed a card's five, so each named part is its
own card (questionRef "Q7(a) — <part>").

Answers the scheme prints as marks are read from glyph positions and checked
against the reviewer's reading of the rendered page: the answer ticks in Q1(a),
Q2, Q8(a)(ii), Q8(b)(vi), Q9(a); the circled numbers of Q7(a); the letters in
the Punnett and DNA diagrams of Q12; the formula of Q13(b)(ii).

Finite printed routes (one card each, at the route tariff): Q7(c) asthma or
bronchitis; Q13(b)(vi) the electrons or the protons; Q16(c)(vi) smoking or
diet or exercise; Q17(a)(iv) a disorder of the ear or the eye.

EXCLUDED, pending a human decision: Q12(b)(ii)2. The scheme prints "Rr" in
both offspring boxes of its Punnett square; the r-gamete row of a pink (Rr) x
white (rr) cross gives rr, which the scheme's own matching phenotype for that
row ("White") confirms. A card would teach the misprint, and the reviewer may
not write the correction, so the task is reviewed, priced and excluded, with
its reason and evidence recorded in the audit. (The census reads Q12(b)(ii)
as one leaf, already covered by the (ii)1 and (ii)3 cards, so reconcile.py
has no finer leaf for an exclusion entry to land on.)
"""
from bio_review_lib import Q, SQ, S, M, G, pt, anyn, T, L

YEAR, LEVEL = 2026, 'ol'

SOURCES = {
    '038': {'path': 'examiner-reports/biology/papers/2026-ol-038-paper.pdf',
            'fileid': 'LC025GLP038EV.pdf',
            'sha256': '446438a5c540b061f7aadd5a5ee8db45dd353cfda06481c80c93771baf573000',
            'pages': 36},
    '040': {'path': 'examiner-reports/biology/papers/2026-ol-040-paper.pdf',
            'fileid': 'LC025GLP040EV.pdf',
            'sha256': 'b245a4e4d0ca2038953407442a1cd61c4b8adddffb36fcd1edfc1bc9bff309d1',
            'pages': 12},
    'scheme': {'path': 'examiner-reports/biology/schemes/2026-ol.pdf',
               'fileid': 'LC025GLP000EV.pdf',
               'sha256': 'f42244755e482722cc5584503b73b78ffcc9167d92a7a7cd3104ccd2d1b94047',
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
               5: 'marking-examples', 6: 'annotations-grading', 7: 'irish-bonus',
               **{p: 'marking' for p in range(8, 33)}, 33: 'blank', 34: 'blank', 35: 'blank',
               36: 'back-cover'},
}

QUESTION_TOTALS = {
    **{n: 20 for n in range(1, 8)}, **{n: 30 for n in range(8, 11)},
    **{n: 60 for n in range(11, 16)},
}
PART_TOTALS = {
    **{(n, 'a'): 6 for n in (8, 9, 10)}, **{(n, 'b'): 24 for n in (8, 9, 10)},
    **{(n, 'a'): 9 for n in (11, 12, 13, 14)}, **{(n, 'b'): 27 for n in (11, 12, 13, 14)},
    **{(n, 'c'): 24 for n in (11, 12, 13, 14, 15)},
    (15, 'a'): 9, (15, 'b'): 27,
    **{(n, x): 30 for n in (16, 17) for x in 'abcd'},
}
# "6(3) + (2)": seven responses, six at 3 and the seventh at 2.
LADDERS = {q: [3, 3, 3, 3, 3, 3, 2] for q in (2, 5, 6)}

# The scheme's own notation for each ladder, as mark units: {mark: count}.
CHECKSUMS = {
    1: {4: 5}, 2: {3: 7}, 3: {4: 5}, 4: {4: 5}, 5: {3: 7}, 6: {3: 7}, 7: {2: 10},
    **{(n, 'a'): {3: 2} for n in (8, 9, 10)}, **{(n, 'b'): {3: 8} for n in (8, 9, 10)},
    **{(n, 'a'): {3: 3} for n in (11, 12, 13, 14, 15)},
    **{(n, 'b'): {3: 9} for n in (11, 12, 13, 14, 15)},
    **{(n, 'c'): {3: 8} for n in (11, 12, 13, 14, 15)},
    **{(n, x): {3: 10} for n in (16, 17) for x in 'abcd'},
}

SCAN_PAGES = {'038': range(2, 12), '040': range(2, 11)}
SELECTION_SCAN = [
    ('038', 2, 'or', 'Instructions: "blue or black pen", not a question.'),
    ('038', 2, 'any five', 'Section A rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any two', 'Section B rubric: whole-question choice; every question is carded.'),
    ('038', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('038', 3, 'any five', 'Section A rubric repeated.'),
    ('038', 3, 'the following', 'Q1 lead-in: parts (a) to (e), all asked.'),
    ('038', 3, 'one of the following', 'Q1(a): tick one of two printed biomolecules; one answer, one card.'),
    ('038', 4, 'the following', 'Q2 lead-in: every statement is asked.'),
    ('038', 4, 'or', 'Q2 "true or false": the response format, not a choice.'),
    ('038', 4, 'choose', 'Q3 "Choose each term": every lettered description is asked; one card per letter.'),
    ('038', 4, 'the following', 'Q3 list of terms to choose from.'),
    ('038', 5, 'any one', 'Q4(b) "any one of these sources ... or any other one you have studied": open, not a closed pool; one card.'),
    ('038', 5, 'or', 'Q4(b), same sentence.'),
    ('038', 7, 'the following', 'Q6(a) matching: all three letters asked; one card.'),
    ('038', 8, 'one of the following', 'Q7(c) closed choose-one pool of two printed disorders: ROUTES, one card each.'),
    ('038', 8, 'or', 'Q7(c), same pool ("asthma or bronchitis").'),
    ('038', 9, 'any two', 'Section B rubric repeated.'),
    ('038', 9, 'the following', 'Q8(a)(ii): tick one of the printed powers; one answer.'),
    ('038', 10, 'the following', 'Q9(a) lead-in: both questions asked.'),
    ('038', 10, 'one of the following', 'Q9(a)(i): tick one of two printed terms; one answer.'),
    ('038', 10, 'one of the following', 'Q9(a)(ii): tick one of two printed biomolecules; one answer.'),
    ('038', 10, 'the following', 'Q9(b) lead-in: every question asked.'),
    ('038', 10, 'or', 'Q9(b)(iii) "(or equipment)": synonym, not a choice.'),
    ('038', 11, 'the following', 'Q10(b)(i) lead-in: every numbered question asked.'),
    ('038', 11, 'or', 'Q10(b)(i) "an ox\'s or sheep\'s heart": either specimen, one set of answers; not a route.'),
    ('038', 11, 'or', 'Q10(b)(i)3 "(R or L)": the answer options.'),
    ('038', 11, 'the following', 'Q10(b)(ii) lead-in: every numbered question asked.'),
    ('038', 11, 'or', 'Q10(b)(ii)1 "(A or B)": the answer options.'),
    ('040', 2, 'any four', 'Section C rubric: whole-question choice; every question is carded.'),
    ('040', 2, 'the following', 'Q11(a)(i) matching: both words asked; one card.'),
    ('040', 2, 'one of the following', 'Q11(a)(ii): one of two printed descriptions; one answer.'),
    ('040', 2, 'the following', 'Q11(b)(i) matching: both terms asked; one card.'),
    ('040', 2, 'the following', 'Q11(b) lead-in: every question on the article asked.'),
    ('040', 2, 'any two', 'Q11(b)(ii) "any two abiotic factors" from the article: a bounded menu inside one task (one any-two row); one card.'),
    ('040', 3, 'the following', 'Q12(a)(i) matching: both terms asked; one card.'),
    ('040', 3, 'one of the following', 'Q12(a)(ii): one of two printed sentences; one answer.'),
    ('040', 3, 'or', 'Q12(a)(ii) "(X or Y)": the answer options.'),
    ('040', 3, 'the following', 'Q12(b)(ii) "show the following": 1., 2. and 3. all asked; one task each.'),
    ('040', 3, 'or', 'Q12(c)(iv) "(or use)": synonym, not a choice.'),
    ('040', 4, 'or', 'Q13(a)(i) "(A or B)": the answer options.'),
    ('040', 4, 'or', 'Q13(a)(ii) "catabolic or anabolic": the answer options.'),
    ('040', 4, 'the following', 'Q13(b)(i) matching: both compounds asked; one card.'),
    ('040', 4, 'either', 'Q13(b)(vi) closed choose-one pool (the electrons or the protons): ROUTES, one card each.'),
    ('040', 4, 'or', 'Q13(b)(vi), same pool.'),
    ('040', 4, 'either', 'Q13(c) statement "either anaerobic or aerobic", not a choice.'),
    ('040', 4, 'or', 'Q13(c), same statement.'),
    ('040', 4, 'or', 'Q13(c)(i) "(1. or 2.)": the answer options.'),
    ('040', 4, 'or', 'Q13(c)(ii) "(1. or 2.)": the answer options.'),
    ('040', 4, 'or', 'Q13(c)(iii) "(aerobic or anaerobic)": the answer options.'),
    ('040', 4, 'any two', 'Q13(c)(iv) "any two factors": open, one any-two row; one card.'),
    ('040', 4, 'either', 'Q13(c)(v) "either one of the factors you named in (c)(iv)": the candidate\'s own earlier answer, not a printed pool; one card.'),
    ('040', 5, 'the following', 'Q14(b) lead-in: every question asked.'),
    ('040', 5, 'or', 'Q14(b)(iii)1 "(chemical or physical)": the answer options.'),
    ('040', 5, 'or', 'Q14(b)(iii)2 "(chemical or physical)": the answer options.'),
    ('040', 5, 'or', 'Q14(b)(iv)1 "(A or B or C)": the answer options.'),
    ('040', 5, 'or', 'Q14(b)(iv)1, same options.'),
    ('040', 5, 'one of the following', 'Q14(b)(iv)2: one of three printed sequences; one answer.'),
    ('040', 5, 'any one', 'Q14(b)(v)1 "any one enzyme": open single answer; one card.'),
    ('040', 5, 'the following', 'Q14(c) lead-in: every question asked.'),
    ('040', 5, 'one of the following', 'Q14(c)(iii): one of three printed veins; one answer.'),
    ('040', 5, 'any one', 'Q14(c)(v) "any one benefit": open single answer; one card.'),
    ('040', 6, 'the following', 'Q15 lead-in: every part asked.'),
    ('040', 6, 'or', 'Q15(a) "females and/or males": flexible wording, not a pool.'),
    ('040', 6, 'any three', 'Q15(a) "any three methods": open, one any-three row; one card.'),
    ('040', 6, 'the following', 'Q15(b)(iii) matching: all three descriptions asked; one card.'),
    ('040', 6, 'one of the following', 'Q15(b)(iv): one of two printed hormones; one answer.'),
    ('040', 6, 'the following', 'Q15(c)(i) matching: all three terms asked; one card.'),
    ('040', 7, 'any two', 'Q16 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 7, 'the following', 'Q16(a)(i) matching: all three terms asked; one card.'),
    ('040', 7, 'the following', 'Q16(a)(iii) "each of the following types of joint": all three asked; one task each.'),
    ('040', 7, 'one of the following', 'Q16(a)(iv): one of two printed terms; one answer.'),
    ('040', 7, 'the following', 'Q16(b)(i) matching: all four terms asked; one card.'),
    ('040', 7, 'or', 'Q16(b)(v) statement "can be active or passive", not a choice.'),
    ('040', 7, 'or', 'Q16(b)(v) "(active or passive)": the answer options.'),
    ('040', 8, 'the following', 'Q16(c)(i) matching: all three structures asked; one card.'),
    ('040', 8, 'one of the following', 'Q16(c)(vi) closed choose-one pool of three printed factors: ROUTES, one card each.'),
    ('040', 8, 'or', 'Q16(c)(vi), same pool ("smoking or diet").'),
    ('040', 8, 'or', 'Q16(c)(vi), same pool ("diet or exercise").'),
    ('040', 8, 'or', 'Q16(d)(ii) "A or B": the answer options.'),
    ('040', 8, 'or', 'Q16(d)(iii) "A or B": the answer options.'),
    ('040', 8, 'or', 'Q16(d)(iv) "A or B": the answer options.'),
    ('040', 8, 'any one', 'Q16(d)(vi) "any one process": open single answer; one card.'),
    ('040', 9, 'any two', 'Q17 "any two of (a), (b), (c), (d)": whole-part choice; every part is carded.'),
    ('040', 9, 'one of the following', 'Q17(a)(iii): one of two printed nerves; one answer.'),
    ('040', 9, 'or', 'Q17(a)(iii) "Optic nerve or Auditory nerve": the answer options.'),
    ('040', 9, 'or', 'Q17(a)(iv) closed choose-one pool (the ear or the eye): ROUTES, one card each.'),
    ('040', 9, 'or', 'Q17(b)(i) "(exocrine or endocrine)": the answer options.'),
    ('040', 9, 'or', 'Q17(b)(iii) printed table entry "Fight or flight" response, not a choice.'),
    ('040', 10, 'the following', 'Q17(c)(i) matching: all three flower parts asked; one card.'),
    ('040', 10, 'or', 'Q17(c)(ii) "the female or male gamete": the answer options.'),
    ('040', 10, 'any two', 'Q17(c)(vi) "any two ways": open, one any-two row; one card.'),
    ('040', 10, 'the following', 'Q17(d)(i) matching: both organisms asked; one card.'),
    ('040', 10, 'one of the following', 'Q17(d)(ii): one of three printed kingdoms; one answer.'),
    ('040', 10, 'both', 'Q17(d)(ii) "both of these organisms", not a choice.'),
    ('040', 10, 'the following', 'Q17(d)(iii) table to complete: both rows asked; one card.'),
    ('040', 10, 'the following', 'Q17(d)(iii) the two terms to use.'),
    ('040', 10, 'both', 'Q17(d)(iv) statement "Both yeast and Rhizopus are heterotrophic", not a choice.'),
    ('040', 10, 'the following', 'Q17(d)(iv) matching: both descriptions asked; one card.'),
    ('040', 10, 'one of the following', 'Q17(d)(v): one of two printed sequences; one answer.'),
    ('040', 10, 'or', 'Q17(d)(v) "(A or B)": the answer options.'),
    ('040', 10, 'the following', 'Q17(d)(vi) matching: both descriptions asked; one card.'),
]

ROUTES = {
    'Q7(c)': ['asthma', 'bronchitis'],
    'Q13(b)(vi)': ['electrons', 'protons'],
    'Q16(c)(vi)': ['smoking', 'diet', 'exercise'],
    'Q17(a)(iv)': ['ear', 'eye'],
}

# Column and pairing checks on the scheme's two-column layouts: the item must
# sit nearer (by x) to the expected heading than to any other.
LAYOUT_CHECKS = [
    ('scheme', 11, 'allergen or other correct', ['Asthma:', 'Bronchitis:'], 'Asthma:'),
    ('scheme', 11, 'inhaler or other correct', ['Asthma:', 'Bronchitis:'], 'Asthma:'),
    ('scheme', 11, 'viral or bacterial or other correct', ['Asthma:', 'Bronchitis:'], 'Bronchitis:'),
    ('scheme', 11, 'anti-inflammatory medication or', ['Asthma:', 'Bronchitis:'], 'Bronchitis:'),
    ('scheme', 13, 'Free enzyme', ['Cloudy', 'Non-cloudy'], 'Cloudy', (60, 560, 560, 700)),
    ('scheme', 13, 'Immobilised enzyme', ['Cloudy', 'Non-cloudy'], 'Non-cloudy', (60, 560, 560, 700)),
]

SEC = 'State Examinations Commission'
FIGURES = {
    # key suffix: (doc, page, rect in PDF points, credit, letters, alt, solution[, masks])
    # masks: rects (PDF points) of neighbouring page furniture whitened inside the crop.
    'q4-evidence': ('038', 5, (112, 178, 542, 359),
        'Bach H, Bernhardt D, Crome W et al (1967b) Entwicklung der Organismen. Lehrbuch der '
        'Biologie. Volk und Wissen, Berlin; shutterstock.com; James L. Amos, nationalgeographic.com',
        [],
        'Three boxed panels numbered 1 to 3. Panel 1: outline drawings of early embryos of a '
        'fish, a turtle, a chicken and a human, each curled, with a dark eye spot and small slits '
        'behind the head, all very alike. Panel 2: the forelimb bones of a human arm, a cat leg, a '
        'bat wing and a whale flipper side by side, each built from one upper bone, two lower '
        'bones and many finger bones. Panel 3: a photograph of a fossil in rock, captioned '
        'Trilobite (an extinct organism).', False),
    'q5-food-web': ('038', 6, (112, 74, 482, 324), 'dreamstime.com; shutterstock.com', [],
        'Food web of pictured organisms joined by arrows. Oak tree, Leaf litter and Blackberry '
        'bush sit along the bottom. Arrows run from Oak tree to Squirrel, Caterpillar and Wood '
        'mouse; from Leaf litter to Earthworm; from Earthworm to Shrew and Wood mouse; from '
        'Blackberry bush to Shrew, Wood mouse and Fox; from Caterpillar to Shrew; from Squirrel '
        'to Owl; from Shrew to Owl, Badger and Fox; and from Wood mouse to Owl, Badger and Fox.',
        False),
    'q6-bacterium': ('038', 7, (350, 54, 575, 222), 'biorender.com', ['X', 'Y', 'Z'],
        'Diagram of a rod-shaped cell with rounded ends. Arrow X points to a small ring inside '
        'the cell; arrow Y points to the inner line of the cell boundary and arrow Z to its outer '
        'layer. A tangled loop of thread lies in the middle of the cell, and a long whip-like '
        'tail leaving one end is labelled Flagellum.', False),
    'q7-breathing': ('038', 8, (84, 136, 541, 414), SEC, [],
        'Diagram of the human breathing system beside a table. The head and neck are shown in '
        'side section above a tube that runs down the neck and divides into two large sacs, with '
        'a curved band beneath them. Circled numbers point to: 1, the tube in the neck; 3, a '
        'box-shaped part at the top of that tube; 4, the rings along it; 2, one of the two '
        'branches the tube divides into; 7, the two large sacs; 8, the curved band below them. A '
        'magnified circle shows a fine airway, 6, ending in a bunch of tiny round sacs, 5. The '
        'table has columns Named part and Number: Alveolus is struck through with 5 filled in as '
        'the example, then the Number box is empty beside Diaphragm, Lungs, Bronchus, Trachea '
        '(windpipe), Bronchiole, Rings of cartilage and Larynx (voice box).', False),
    'q8-microscope': ('038', 9, (464, 116, 543, 240), 'alamy.com', ['A', 'B'],
        'Photograph of a light microscope. Arrow A points to the short cylinder at the very top '
        'of the body tube; arrow B points to one of the short lenses on the rotating turret above '
        'the stage.', False),
    'q8-photos': ('038', 9, (136, 645, 512, 724), 'microbehunter.com; shutterstock.com', [],
        'Two black-and-white light micrographs side by side. Left: long, many-sided cells packed '
        'in rows, each with a dark nucleus; an arrow from the words Cell wall points to the thick '
        'line between two cells. Right: a few flat, irregular cells with dark nuclei and no thick '
        'boundary lines, beside the words No cell wall.', False),
    'q9-flasks': ('038', 10, (140, 621, 528, 710), 'biorender.com', [],
        'Two conical flasks side by side. The left flask holds grey, opaque liquid, labelled '
        'Cloudy product; the right flask holds clear liquid, labelled Non-cloudy (clear) '
        'product.', False),
    'q10-heart': ('038', 11, (401, 187, 543, 362), 'shutterstock.com', ['R', 'L'],
        'Photograph of a heart with its front side facing up. A label Coronary artery points to a '
        'blood vessel running diagonally down across the front. Arrows mark the two sides near '
        'the base of the heart: R on the left of the photograph and L on the right.', False),
    'q10-stems': ('038', 11, (428, 420, 541, 668), 'alamy.com', ['A', 'B'],
        'Two light micrographs of stem cross-sections, one above the other. A: a round section '
        'with many small dark vascular bundles scattered all through it. B: a round section with '
        'larger vascular bundles set in a single ring near the edge. Arrows from the words '
        'Vascular bundles point to bundles in both sections.', False),
    'q10b-i-1-scheme': ('scheme', 14, (143, 289, 216, 392), 'shutterstock.com', [],
        'The marking scheme\'s copy of the heart photograph with two thick dashed lines drawn on '
        'it, parallel to each other, each running diagonally from upper right down to lower left '
        'across the front of the heart; one crosses its middle and the other lies nearer its '
        'right-hand side.', True),
    'q10b-i-1-question': ('038', 11, (82, 156, 545, 364), 'shutterstock.com', ['R', 'L'],
        'The printed question: (b)(i) The following questions relate to the dissection of an '
        'ox\'s or sheep\'s heart. The photograph shows a heart with its front side facing up. 1. '
        'Using a dotted line (a short row of dots is printed between the brackets), indicate on '
        'the photograph where an incision should be made. Beside it, the photograph of the heart '
        'from the front: a label Coronary artery points to a vessel running diagonally down '
        'across it, and arrows mark R on the left of the photograph and L on the right.', False,
        [(110, 224, 404, 366)]),
    'q12-roses': ('040', 3, (354, 172, 541, 252), 'dreamstime.com', [],
        'Three rose photographs side by side, captioned Red (RR), Pink followed by a blank line, '
        'and White (rr).', False),
    'q12-punnett': ('040', 3, (312, 172, 542, 466), 'dreamstime.com; State Examinations Commission',
        [],
        'Three rose photographs captioned Red (RR), Pink followed by a blank line, and White (rr). '
        'Below them, an empty Punnett square: one box at the top labelled Genotype of white rose '
        'gamete; two boxes down the left side labelled Genotypes of pink rose gametes; two long '
        'boxes labelled Offspring genotypes; and two blank lines to the right labelled Matching '
        'offspring phenotypes.', False,
        [(312, 172, 350, 240), (312, 262, 405, 280)]),
    'q12-dna': ('040', 3, (424, 528, 541, 686), SEC, [],
        'Ladder diagram of a DNA molecule: four rungs leave the left-hand strand from boxes '
        'holding the bases C, G, A and T, top to bottom; each rung is dotted across the middle '
        'and ends in an empty box at the right-hand strand.', False),
    'q13-equation': ('040', 4, (116, 184, 482, 222), SEC, ['A', 'B'],
        'Word equation: Carbon dioxide plus a box labelled A, then an arrow marked Light energy '
        'above and Chlorophyll below, leading to a box labelled B plus Oxygen.', False),
    'q13-formula': ('040', 4, (444, 250, 540, 280), SEC, [],
        'The letters C, H and O, each followed by an empty box for its number.', False),
    'q13-axes': ('040', 4, (210, 618, 382, 746), SEC, [],
        'A pair of blank axes: a vertical arrow and a horizontal arrow meeting at the lower left, '
        'with an empty label box beside the vertical axis and another below the horizontal axis.',
        False),
    'q14-digestive': ('040', 5, (302, 248, 545, 474), 'shutterstock.com', ['A', 'B', 'C'],
        'Line drawing of the human digestive system. Printed labels name the Liver, the Pancreas '
        'and the Small intestine. Arrow A points to the narrow tube entering from the top; arrow '
        'C to the bag-shaped organ that tube leads into, on the right below the liver; arrow B to '
        'the start of the wide, pouched tube that frames the small intestine on three sides.',
        False),
    'q15-foetus': ('040', 6, (398, 216, 542, 390), 'shutterstock.com', [],
        'Side-view diagram of a pregnant abdomen with a foetus curled head-down inside the '
        'uterus. A label Placenta points to the thick ribbed pad on the uterine wall at the left, '
        'joined to the foetus by a coiled cord.', False),
    'q15-sperm': ('040', 6, (372, 481, 545, 604), 'shutterstock.com', ['A', 'B', 'C'],
        'Line drawing of a sperm cell. Arrow C points to the oval end at the upper right; arrow '
        'B to the short beaded section just behind it; arrow A to the long thin thread curving '
        'away to the lower left.', False),
    'q16-joint': ('040', 7, (392, 94, 548, 270), 'shutterstock.com', ['A', 'B', 'C'],
        'Diagram of a joint in section: two bone ends, spongy inside, meet within a capsule. '
        'Arrow A points to the outer band wrapping the joint; two arrows labelled B point to the '
        'smooth caps over the ends of both bones; arrow C points to the dark space between the '
        'bone ends.', False),
    'q16-skin': ('040', 7, (336, 410, 545, 614), 'dreamstime.com', ['P', 'Q', 'R', 'S'],
        'Diagram of a block of skin with hairs growing out of the surface. A bracket labelled P '
        'marks the thin top layer; arrow Q points to a hair shaft where it passes through that '
        'layer; arrow R points to a thin tube rising to the surface from a coiled knot in the '
        'lower layer; arrow S points to a small lobed sac beside the hair.', False),
    'q16-heart': ('040', 8, (405, 54, 545, 268), SEC, ['A', 'B', 'C'],
        'Outline diagram of the right side of the heart. A label Right atrium points into the '
        'upper chamber. Arrow A points to a vessel entering that chamber at the top left; arrow B '
        'to a flap where the upper chamber opens into the lower one; arrow C into the large lower '
        'chamber, from which a vessel rises up the right-hand side.', False),
    'q16-tissues': ('040', 8, (136, 379, 468, 566), SEC, ['A', 'B'],
        'Two drawings of plant vascular tissue side by side. Tissue A: long tubes whose labels '
        'read No end-walls between cells and Thick walls with lignin. Tissue B: a column of cells '
        'whose label reads Cells have end-walls with pores (sieve plate), with a row of smaller '
        'cells alongside, each holding a dark nucleus.', False),
    'q16c-ii-question': ('040', 8, (82, 56, 545, 272), SEC, ['A', 'B', 'C'],
        'The printed question: (c) The diagram shows the right side of the human heart. (ii) Copy '
        'the diagram, without the labels, into your answerbook and draw at least two arrows to '
        'indicate the direction of blood flow through the right-hand side of the heart. Beside '
        'it, the outline diagram of the right side of the heart: a label Right atrium points into '
        'the upper chamber, and arrows A, B and C point to a vessel entering at the top left, a '
        'flap between the upper and lower chambers, and the large lower chamber.', False,
        [(110, 72, 405, 146), (110, 204, 405, 274)]),
    'q16c-ii-scheme': ('scheme', 27, (158, 222, 254, 416), SEC, [],
        'The marking scheme\'s copy of the heart diagram with two arrows drawn on it: one runs '
        'from the vessel at the top left down into the upper chamber; the other runs from the '
        'lower chamber up through the vessel on the right-hand side and out at the top.', True),
    'q17-ear': ('040', 9, (306, 100, 545, 264), 'istockphoto.com', ['A', 'B', 'C', 'D'],
        'Diagram of the human ear in section. Arrow A points to the outer flap of the ear; arrow '
        'B to the thin membrane across the inner end of the ear canal; arrow C to the three looped '
        'tubes above the coiled cochlea; arrow D to the tube running down and away from the '
        'middle ear.', False),
    'q17-table': ('040', 9, (140, 534, 542, 642), SEC, [],
        'Table with three columns: Name of gland, Hormone, and Function of hormone. Row 1: blank, '
        'Growth hormone, Growth. Row 2: blank, blank, Fight or flight response (the phrase in '
        'quotation marks). Row 3: Thyroid, blank, Controls the rate of metabolism.', False),
    'q17-flower': ('040', 10, (388, 56, 545, 180), 'Adapted from Sarah Greenwood, wikimedia.org',
        ['X', 'Y', 'Z'],
        'Diagram of a flower in section. Arrow X points to the top of the central column; arrow Z '
        'to the swollen chamber at its base; arrow Y to the thin stalk of one of the oval '
        'structures around it, one of which is labelled Anther.', False),
    'q17d-table': ('040', 10, (140, 470, 364, 530), SEC, [],
        'Table with two columns, Organism and Reproduces by..., and two rows: Yeast with an '
        'empty box, and Rhizopus with an empty box.', False),
    'q17-organisms': ('040', 10, (380, 323, 540, 466), 'shutterstock.com; dreamstime.com',
        ['A', 'B'],
        'Two boxed diagrams. Diagram A: upright stalks rising from a horizontal thread with '
        'root-like branches below, each stalk topped by a round head full of small dots. Diagram '
        'B: two oval cells, a small one joined to the top of a larger one, each with a dark '
        'nucleus and a pale vacuole.', False),
}


def _A(page, start, end=None, **kw):
    return Q(page, start, end, doc='038', **kw)


def _C(page, start, end=None, **kw):
    return Q(page, start, end, doc='040', **kw)


def listed(page, anchor, ends):
    """A printed numbered list ("1." on its own line, its item on the next),
    each item on its own line as the paper sets it."""
    return [_C(page, f'{i}.', end, after=anchor, br=True) for i, end in enumerate(ends, 1)]


def tick_row(page, clip, choices, expect, marks):
    return G('tick-row', page=page, clip=clip, choices=choices, expect=expect, marks=marks)


Q2_STATEMENTS = [
    ('a', 'A hypothesis is always formulated', (60, 548, 530, 571), 'False', 'hypothesis-and-experiments'),
    ('b', '‘Careful planning and design’', (60, 571, 530, 595), 'True', 'principles-of-experimentation'),
    ('c', 'A control is used as a comparison', (60, 595, 530, 617), 'True', 'controls'),
    ('d', 'Replicates are never required', (60, 617, 530, 639), 'False', 'replicates'),
    ('e', 'A theory is a supported hypothesis.', (60, 639, 530, 661), 'True', 'theory'),
    ('f', 'Data generated from an experiment', (60, 661, 530, 683), 'False', 'data-types'),
    ('g', 'A scientific journal is used', (60, 683, 530, 706), 'True', 'publishing-research'),
]

Q3_ITEMS = [
    ('a', 'An organelle that stores water in plant cells.', None, 'An organelle that stores water',
     'Vacuole', 'bio-1-3', 'vacuole'),
    ('b', 'Controls the activities of a cell.', None, 'Controls the activities',
     'Nucleus', 'bio-1-3', 'nucleus'),
    ('c', 'Movement of water molecules from a region of', 'membrane.', 'Movement of water molecules',
     'Osmosis', 'bio-2-6', 'osmosis'),
    ('d', 'Site of protein synthesis.', None, 'Site of protein synthesis',
     'Ribosome', 'bio-1-3', 'ribosome'),
    ('e', 'Nuclear division where two genetically identical', 'nuclei are produced.',
     'Nuclear division where two', 'Mitosis', 'bio-2-3', 'mitosis'),
]
Q3_STEM = [_A(4, 'Choose each term from the following list', 'as an example.'),
           _A(4, 'Ribosome'), _A(4, 'Nucleus'), _A(4, 'Vacuole'), _A(4, 'Mitosis'), _A(4, 'Osmosis')]
Q4_STEM = _A(5, 'The theory of natural selection was proposed')
Q4C = _A(5, 'Some key terms associated', 'theory of natural selection.')
Q5_STEM = _A(6, 'Study the food web shown')
Q6_STEM = _A(7, 'The diagram shows a bacterial cell.')
Q7_STEM = _A(8, 'The diagram shows the human breathing system.')
Q7_PARTS = [('Diaphragm', '⑧'), ('Lungs', '⑦'), ('Bronchus', '②'), ('Trachea (windpipe)', '①'),
            ('Bronchiole', '⑥'), ('Rings of cartilage', '④'), ('Larynx (voice box)', '③')]
Q8A_STEM = _A(9, 'The light microscope, as shown', 'parts A and B.')
Q8B_STEM = _A(9, 'As part of your practical studies', 'light microscope.')
Q9B_STEM = _A(10, 'Answer the following questions in relation to an investigation', 'its application.')
Q10BI_STEM = _A(11, 'The following questions relate to the dissection', 'facing up.')
Q10BII_STEM = _A(11, 'Answer the following questions in relation to the', '(dicot) stem.')

Q11_ARTICLE = [_C(2, 'Read the article below'),
               _C(2, 'Killarney National Park is an ecosystem', 'biodiversity of the soil.'),
               _C(2, 'Adapted from Progress in', '18 April 2025'),
               _C(2, 'Answer the following questions based on information provided')]
Q12_ROSES = _C(3, 'The images show a red rose', 'Pink roses are heterozygous.')
Q12_CROSS = [_C(3, 'A rose with pink flowers was crossed', 'with a rose with white flowers.'),
             _C(3, 'Copy the Punnett square shown', 'show the following:')]
Q12_DNA = [_C(3, 'The diagram shows a DNA molecule.'),
           _C(3, 'The four bases, C (cytosine)', 'shown on one strand.')]
Q13_C = [_C(4, 'Respiration can be either anaerobic or aerobic.'),
         _C(4, 'Aerobic respiration is a two-stage process.')]
Q14_B = _C(5, 'Answer the following questions in relation to your knowledge of human digestion.')
Q14_C = _C(5, 'Answer the following questions based on the small and large intestines.')
Q15 = _C(6, 'Answer the following questions based on your knowledge of human reproduction.')
Q15_SPERM = _C(6, 'The diagram shows the human male gamete, a sperm cell.')
Q16_JOINT = _C(7, 'The diagram shows a typical synovial joint.')
Q16_JOINTS = _C(7, 'There are three main types of joint found in the', 'following types of joint:')
Q16_SKIN = _C(7, 'The skin is a component of the general', 'entering the body.')
Q16_HEART = _C(8, 'The diagram shows the right side of the human heart.')
Q16_TISSUE = _C(8, 'The diagrams show two types of vascular tissue')
Q17_EAR = _C(9, 'The diagram shows the human ear.')
Q17_FLOWER = _C(10, 'The diagram shows a plant flower.')
Q17_ORG = _C(10, 'The diagrams on the right show two organisms')

MUST_MATCH = 'Must match named enzyme in (b)(i)'

TASKS = [
    # ------------------------------------------------------------ Section A --
    T('1a', 'Q1(a)', 'A',
      [_A(3, 'Which one of the following biomolecules', 'correct box.'),
       _A(3, 'Carbohydrate', br=True), _A(3, 'Protein', br=True)],
      [tick_row(8, (90, 168, 300, 212), ['Carbohydrate', 'Protein'], 'Protein', 4)],
      'bio-1-2', 'protein-contains-nitrogen', SQ(8, 'Which one of the following biomolecules'), 4),
    T('1b', 'Q1(b)', 'A', _A(3, 'Name a food that is a good source of carbohydrate'),
      [pt(S('Bread or rice'), 4)], 'bio-1-2', 'carbohydrate-foods',
      SQ(8, 'Name a food which is a good source of carbohydrate'), 4),
    T('1c', 'Q1(c)', 'A', _A(3, 'Name a food that is a good source of fat'),
      [pt(S('Milk or yoghurt'), 4)], 'bio-1-2', 'fat-foods',
      SQ(8, 'Name a food which is a good source of fat'), 4),
    T('1d', 'Q1(d)', 'A', _A(3, 'Give one example of a fat-soluble vitamin.'),
      [pt(S('A or D or E or K'), 4)], 'bio-1-2', 'fat-soluble-vitamins',
      SQ(8, 'Give one example of a fat-soluble'), 4, stem=[_A(3, 'Vitamins B and C are examples')]),
    T('1e', 'Q1(e)', 'A',
      [_A(3, 'Name another trace element required by organisms.'), _A(3, 'Note:', br=True)],
      [pt(S('Iron or copper or other correct'), 4, note_sel=S('Accept correct chemical symbol'))],
      'bio-1-2', 'trace-elements', SQ(8, 'Name another trace element'), 4,
      stem=[_A(3, 'Zinc (Zn) is an example')]),
] + [
    T(f'2{x}', f'Q2({x})', 'A', _A(4, start),
      [G('tick-col', page=8, clip=clip, headers=['True', 'False'], expect=answer, marks=3)],
      'bio-u2', concept, SQ(8, start), 3,
      stem=[_A(4, 'Indicate whether the following statements', 'in each case.')],
      notes='Question 2 is marked on one ladder, 6(3) + (2).')
    for x, start, clip, answer, concept in Q2_STATEMENTS
] + [
    T(f'3{x}', f'Q3({x})', 'A', _A(4, start, end), [pt(S(answer), 4)], topic, concept,
      SQ(9, sq), 4, stem=Q3_STEM,
      decision='Lettered parts are separate printed addresses; the struck-through example '
               'term (Haploid) is left out of the list the stem carries.')
    for x, start, end, sq, answer, topic, concept in Q3_ITEMS
] + [
    T('4a', 'Q4(a)', 'A', _A(5, 'Name one of these biologists.'),
      [pt(S('(Charles) Darwin'), 4)], 'bio-1-5', 'darwin-and-wallace',
      SQ(9, 'Name one of the biologists.'), 4, stem=[Q4_STEM]),
    T('4b', 'Q4(b)', 'A', _A(5, 'Name any one of these sources', 'you have studied.'),
      [pt(S('Comparative embryology'), 4)], 'bio-1-5', 'evidence-for-evolution',
      SQ(9, 'Name any one these sources'), 4,
      stem=[_A(5, 'Three sources of evidence', 'not drawn to scale.')], fig='q4-evidence'),
    T('4ci', 'Q4(c)(i)', 'A', _A(5, 'Rate of reproduction.'),
      [pt(S('High rate or large numbers'), 4)], 'bio-1-5', 'natural-selection-reproduction',
      SQ(9, 'Rate of reproduction.'), 4, stem=[Q4_STEM, Q4C]),
    T('4cii', 'Q4(c)(ii)', 'A', _A(5, 'Adaptations of organisms.'),
      [pt(S('(Adaptations) that make', 'reference to survival)'), 4)], 'bio-1-5',
      'natural-selection-adaptation', SQ(9, 'Adaptations of organisms.'), 4, stem=[Q4_STEM, Q4C]),
    T('4ciii', 'Q4(c)(iii)', 'A', _A(5, 'Resources.'),
      [pt(S('Food in short supply'), 4)], 'bio-1-5', 'natural-selection-resources',
      SQ(9, 'Resources.'), 4, stem=[Q4_STEM, Q4C]),
    T('5a', 'Q5(a)', 'A', _A(6, 'Identify a producer in the food web above.'),
      [pt(S('Oak tree or Blackberry bush'), 3)], 'bio-3-1', 'producers',
      SQ(10, 'Identify a producer'), 3, stem=[Q5_STEM], fig='q5-food-web'),
    T('5b', 'Q5(b)', 'A', _A(6, 'Identify a primary consumer'),
      [pt(S('Earthworm or Squirrel'), 3)], 'bio-3-1', 'primary-consumers',
      SQ(10, 'Identify a primary consumer'), 3, stem=[Q5_STEM], fig='q5-food-web'),
    T('5c', 'Q5(c)', 'A', _A(6, 'Name a carnivore in the food web above.'),
      [pt(S('Owl or Badger'), 3)], 'bio-3-1', 'carnivores',
      SQ(10, 'Name a carnivore'), 3, stem=[Q5_STEM], fig='q5-food-web'),
    T('5d', 'Q5(d)', 'A', _A(6, 'Write out one food chain from the food web above.'),
      [pt(S('Any correct food chain'), 3, kind='criterion',
          note_sel=S('Food chain must start with a producer')),
       pt(S('Arrows between organisms'), 3, kind='criterion')],
      'bio-3-1', 'food-chains', SQ(10, 'Write out one food chain'), 6, stem=[Q5_STEM],
      fig='q5-food-web',
      decision='Two of the ladder\'s seven responses: the chain and its arrows.'),
    T('5e', 'Q5(e)', 'A', _A(6, 'How many trophic (feeding) levels'),
      [pt(S('2 or 3 or 4'), 3, note_sel=S('Must match food chain given in (d)'))],
      'bio-3-1', 'trophic-levels', SQ(10, 'How many trophic'), 3,
      stem=[Q5_STEM, M('(d)', 6), _A(6, 'Write out one food chain from the food web above.')],
      fig='q5-food-web'),
    T('5f', 'Q5(f)', 'A',
      [_A(6, 'Place a tick', 'in a food chain.'), _A(6, '10%', br=True), _A(6, '90%', br=True)],
      [pt(S('90'), 3)], 'bio-3-1', 'energy-loss-between-levels', SQ(10, 'Place a tick'), 3),
    T('6a', 'Q6(a)', 'A', _A(7, 'Match the parts labelled X, Y and Z', 'plasmid'),
      [pt(S('Plasmid'), 3, label=S('X:')), pt(S('Cell membrane'), 3, label=S('Y:')),
       pt(S('Cell wall'), 3, label=S('Z:'))],
      'bio-3-2', 'bacterial-cell-structure',
      SQ(10, 'Match the parts labelled X', 'Cell membrane, cell wall, plasmid'), 9,
      stem=[Q6_STEM], fig='q6-bacterium',
      labels=[L('X', S('Plasmid', page=10, after='X:'), True),
              L('Y', S('Cell membrane', page=10, after='Y:'), True),
              L('Z', S('Cell wall', page=10, after='Z:'), True)],
      decision='One matching exercise under one letter: three of the ladder\'s responses.'),
    T('6b', 'Q6(b)', 'A', _A(7, 'Give the function of the flagellum.'),
      [pt(S('Movement'), 3)], 'bio-3-2', 'flagellum', SQ(10, 'Give the function of the flagellum'),
      3, stem=[Q6_STEM], fig='q6-bacterium'),
    T('6c', 'Q6(c)', 'A', _A(7, 'State one factor which affects the growth'),
      [pt(S('Temperature or pH', 'other correct'), 3)], 'bio-3-2', 'bacterial-growth-factors',
      SQ(10, 'State one factor which affects'), 3),
    T('6d', 'Q6(d)', 'A', _A(7, 'Give one example of a harmful bacterium'),
      [pt(S('Correct harmful example given'), 3, kind='criterion'),
       pt(S('Correct beneficial example given'), 3, kind='criterion')],
      'bio-3-2', 'harmful-and-beneficial-bacteria', SQ(10, 'Give one example of a harmful'), 6),
] + [
    T(f'7a-{slug}', 'Q7(a)', 'A',
      [_A(8, 'Complete the table below by writing', 'completed as an example.'),
       _A(8, 'Named part:', 'Named part:', br=True), _A(8, *cell)],
      [G('circled', page=11, clip=(230, 172, 400, 362), part=part, expect=f'{part} — {num}', marks=2)],
      'bio-2-6', f'breathing-system-{slug}', SQ(11, 'Complete the table below'), 2,
      stem=[Q7_STEM], fig='q7-breathing', item=(slug, part),
      decision='The table prices each named part as one response of the 10(2) ladder; seven '
               'required rows exceed a card\'s five, so each named part is its own card.')
    for slug, part, num, cell in [
        ('diaphragm', 'Diaphragm', '⑧', ('Diaphragm',)),
        ('lungs', 'Lungs', '⑦', ('Lungs',)),
        ('bronchus', 'Bronchus', '②', ('Bronchus',)),
        ('trachea', 'Trachea (windpipe)', '①', ('Trachea', '(windpipe)')),
        ('bronchiole', 'Bronchiole', '⑥', ('Bronchiole',)),
        ('rings-of-cartilage', 'Rings of cartilage', '④', ('Rings of', 'cartilage')),
        ('larynx', 'Larynx (voice box)', '③', ('Larynx', '(voice box)')),
    ]
] + [
    T('7b', 'Q7(b)', 'A', _A(8, 'In which numbered part of the diagram'),
      [pt(S('5 (accept alveolus)'), 2)], 'bio-2-6', 'site-of-gas-exchange',
      SQ(11, 'In which numbered part'), 2, stem=[Q7_STEM], fig='q7-breathing'),
    T('7c', 'Q7(c)', 'A', _A(8, 'In the case of one of the following breathing', 'named disorder.'),
      [pt(S('allergen or other correct'), 2, label=S('Cause:')),
       pt(S('Treatment: inhaler'), 2)],
      'bio-2-6', 'asthma', SQ(11, 'In the case of one of the following'), 4, route='asthma',
      decision='Closed choose-one pool of two printed disorders: one card each.'),
    T('7c', 'Q7(c)', 'A', _A(8, 'In the case of one of the following breathing', 'named disorder.'),
      [pt(S('viral or bacterial or other correct'), 2, label=S('Cause:', nth=2)),
       pt(S('Treatment: anti-inflammatory', 'other correct'), 2)],
      'bio-2-6', 'bronchitis', SQ(11, 'In the case of one of the following'), 4, route='bronchitis',
      decision='Closed choose-one pool of two printed disorders: one card each.'),
    # ------------------------------------------------------------ Section B --
    T('8ai', 'Q8(a)(i)', 'B', _A(9, 'Name the part of the light microscope labelled A.'),
      [pt(S('Eyepiece'), 3)], 'bio-1-3', 'microscope-eyepiece',
      SQ(12, 'Name the part of the light microscope'), 3, stem=[Q8A_STEM], fig='q8-microscope',
      labels=[L('A', S('Eyepiece', page=12), True)]),
    T('8aii', 'Q8(a)(ii)', 'B',
      [_A(9, 'If the specimen is magnified', 'correct box.'), _A(9, '×10', br=True),
       _A(9, '×40', br=True)],
      [tick_row(12, (115, 205, 240, 238), ['x10', 'x40'], 'x10', 3)],
      'bio-1-3', 'microscope-magnification', SQ(12, 'If the specimen is magnified'), 3,
      stem=[Q8A_STEM], fig='q8-microscope'),
    T('8bi', 'Q8(b)(i)', 'B', _A(9, 'Name the type of plant cells you used.'),
      [pt(S('Correct type named'), 3, kind='criterion')], 'bio-1-3', 'plant-cells-for-microscopy',
      SQ(12, 'Name the type of plant cells'), 3, stem=[Q8B_STEM]),
    T('8bii', 'Q8(b)(ii)', 'B', _A(9, 'Describe how you obtained the plant cells', 'cells for viewing.'),
      [anyn(S('Cut a thin layer', 'place on stage'), 3, 3)], 'bio-1-3', 'preparing-unstained-cells',
      SQ(12, 'Describe how you obtained'), 9, stem=[Q8B_STEM]),
    T('8biii', 'Q8(b)(iii)', 'B', _A(9, 'You then prepared stained plant cells.', 'to the cells.'),
      [pt(S('Iodine or methylene blue'), 3)], 'bio-1-3', 'stains',
      SQ(12, 'Name a stain you applied'), 3, stem=[Q8B_STEM]),
    T('8biv', 'Q8(b)(iv)', 'B', _A(9, 'How did you apply the stain'),
      [pt(S('Pipette (allow dropper)'), 3)], 'bio-1-3', 'applying-a-stain',
      SQ(12, 'How did you apply the stain'), 3, stem=[Q8B_STEM]),
    T('8bv', 'Q8(b)(v)', 'B', _A(9, 'Why was a stain used'),
      [pt(S('Make cells more visible'), 3)], 'bio-1-3', 'why-stain-cells',
      SQ(12, 'Why was a stain used'), 3, stem=[Q8B_STEM]),
    T('8bvi', 'Q8(b)(vi)', 'B', _A(9, 'Which photograph below shows stained', 'correct box.'),
      [G('tick-row', page=12, clip=(100, 600, 520, 700),
         choices=[('Cell wall', (110, 612, 200, 640)), ('No cell wall', (420, 612, 520, 640))],
         expect='Cell wall', marks=3,
         note='The scheme ticks the photograph labelled Cell wall.')],
      'bio-1-3', 'stained-plant-cells', SQ(12, 'Which photograph below shows'), 3,
      stem=[Q8B_STEM], fig='q8-photos'),
    T('9ai', 'Q9(a)(i)', 'B',
      [_A(10, 'Which one of the following terms best describes'),
       _A(10, 'Fibrous', br=True), _A(10, 'Folded (globular)', br=True)],
      [tick_row(13, (115, 115, 370, 146), ['Fibrous', 'Folded (globular)'], 'Folded (globular)', 3)],
      'bio-2-1', 'enzyme-shape', SQ(13, 'Which one of the following terms best'), 3,
      stem=[_A(10, 'Put a tick (✓) in the correct boxes')]),
    T('9aii', 'Q9(a)(ii)', 'B',
      [_A(10, 'Which one of the following biomolecules makes'),
       _A(10, 'Protein', br=True), _A(10, 'Lipid', br=True)],
      [tick_row(13, (115, 158, 300, 190), ['Protein', 'Lipid'], 'Protein', 3)],
      'bio-2-1', 'enzymes-are-proteins', SQ(13, 'Which one of the following biomolecules'), 3,
      stem=[_A(10, 'Put a tick (✓) in the correct boxes')]),
    T('9bi', 'Q9(b)(i)', 'B', _A(10, 'Name the enzyme you used.'),
      [pt(S('Sucrase (accept yeast)'), 3)], 'bio-2-1', 'enzyme-for-immobilisation',
      SQ(13, 'Name the enzyme you used.'), 3, stem=[Q9B_STEM]),
    T('9bii', 'Q9(b)(ii)', 'B', _A(10, 'Name a substance you used to immobilise'),
      [pt(S('Sodium alginate'), 3)], 'bio-2-1', 'immobilising-agent',
      SQ(13, 'Name a substance you used'), 3, stem=[Q9B_STEM]),
    T('9biii', 'Q9(b)(iii)', 'B', _A(10, 'In the space provided below, draw a labelled', 'immobilise the enzyme.'),
      [pt(S('Diagram: Beaker', 'in correct position'), 3, kind='criterion'),
       pt(S('Label:', 'relevant label'), 3, kind='criterion')],
      'bio-2-1', 'immobilisation-apparatus', SQ(13, 'In the space provided below'), 6,
      stem=[Q9B_STEM]),
    T('9biv', 'Q9(b)(iv)', 'B', _A(10, 'Name the substrate of the enzyme.'),
      [pt(S('Sucrose or other correct'), 3, note_sel=S(MUST_MATCH))], 'bio-2-1',
      'substrate-of-immobilised-enzyme', SQ(13, 'Name the substrate'), 3,
      stem=[Q9B_STEM, _A(10, 'You would have also examined the application', 'immobilised enzyme.')]),
    T('9bv', 'Q9(b)(v)', 'B', _A(10, 'Name the product of the enzyme.'),
      [pt(S('Glucose or fructose'), 3, note_sel=S(MUST_MATCH))], 'bio-2-1',
      'product-of-immobilised-enzyme', SQ(13, 'Name the product'), 3, stem=[Q9B_STEM]),
    T('9bvi', 'Q9(b)(vi)', 'B', _A(10, 'Match the terms immobilised enzyme and free enzyme', 'most likely produce.'),
      [pt(S('Free enzyme'), 3, label=S('Cloudy', 'product')),
       pt(S('Immobilised enzyme'), 3, label=S('Non-cloudy', '(clear) product'))],
      'bio-2-1', 'immobilised-versus-free-enzyme', SQ(13, 'Match the terms immobilised'), 6,
      stem=[Q9B_STEM, _A(10, 'In examining the application of the immobilised enzyme', 'was carried out.')],
      fig='q9-flasks'),
    T('10ai', 'Q10(a)(i)', 'B', _A(11, 'What is the function of the pacemaker'),
      [pt(S('To control the rate'), 3)], 'bio-2-6', 'pacemaker', SQ(14, 'What is the function of the pacemaker'), 3),
    T('10aii', 'Q10(a)(ii)', 'B', _A(11, 'Name a location in a plant where meristematic'),
      [pt(S('Root tip or shoot tip'), 3)], 'bio-2-6', 'meristems', SQ(14, 'Name a location in a plant'), 3),
    T('10bi1', 'Q10(b)(i)1', 'B', _A(11, 'Using a dotted line', 'incision should be made.'),
      [pt(S('Only one correctly located dotted line'), 3, kind='criterion')],
      'bio-2-6', 'heart-dissection-incision', SQ(14, 'Using a dotted line'), 3,
      stem=[Q10BI_STEM], fig='q10b-i-1-scheme', qfig='q10b-i-1-question', source_pages=[11],
      decision='The printed question, with its photograph and the dotted-line symbol the text '
               'layer drops, is shown as the paper prints it; the scheme\'s drawing of where the '
               'incision runs waits for the reveal.'),
    T('10bi2', 'Q10(b)(i)2', 'B', _A(11, 'What instrument would be suitable', 'this incision?'),
      [pt(S('Scalpel'), 3)], 'bio-2-6', 'dissecting-instrument',
      SQ(14, 'What instrument would be suitable'), 3, stem=[Q10BI_STEM], fig='q10-heart'),
    T('10bi3', 'Q10(b)(i)3', 'B', _A(11, 'Which letter on the photograph', 'thickest wall?'),
      [pt(S('L'), 3)], 'bio-2-6', 'thickest-heart-wall', SQ(14, 'Which letter on the photograph'), 3,
      stem=[Q10BI_STEM], fig='q10-heart'),
    T('10bi4', 'Q10(b)(i)4', 'B', _A(11, 'State a safety precaution that should be taken'),
      [pt(S('Valid safety precaution given'), 3, kind='criterion')], 'bio-2-6',
      'dissection-safety', SQ(14, 'State a safety precaution'), 3,
      stem=[_A(11, 'The following questions relate to the dissection', 'heart.')],
      decision='The stem stops before the photograph, which this ask does not use.'),
    T('10bii1', 'Q10(b)(ii)1', 'B', _A(11, 'Which image (A or B) shows a dicot stem?', 'Justify your answer.'),
      [pt(S('B'), 3), pt(S('Justify:'), 3)], 'bio-2-6', 'dicot-stem-structure',
      SQ(14, 'Which image (A or B) shows a dicot stem?'), 6, stem=[Q10BII_STEM], fig='q10-stems'),
    T('10bii2', 'Q10(b)(ii)2', 'B', _A(11, 'Name an instrument you used to prepare a thin', 'microscopic examination.'),
      [pt(S('Backed blade or scalpel'), 3)], 'bio-2-6', 'cutting-a-thin-section',
      SQ(14, 'Name an instrument you used'), 3, stem=[Q10BII_STEM]),
    T('10bii3', 'Q10(b)(ii)3', 'B', _A(11, 'Explain why the section had to be thin.'),
      [pt(S('So that light could pass'), 3)], 'bio-2-6', 'why-sections-are-thin',
      SQ(14, 'Explain why the section had to be thin.'), 3, stem=[Q10BII_STEM]),
    # ------------------------------------------------------------ Section C --
    T('11ai', 'Q11(a)(i)', 'C', _C(2, 'Match the words animal and plant', 'Fauna.'),
      [pt(S('Fauna'), 3, label=S('Animal:')), pt(S('Flora'), 3, label=S('Plant:'))],
      'bio-3-1', 'flora-and-fauna', SQ(15, 'Match the words, animal and plant', 'Fauna.'), 6),
    T('11aii', 'Q11(a)(ii)', 'C', _C(2, 'Which one of the following describes the term biotic?', 'Non-living.'),
      [pt(S('Living'), 3)], 'bio-3-1', 'biotic-factors',
      SQ(15, 'Which one of the following describes', 'Non-living.'), 3),
    T('11bi', 'Q11(b)(i)', 'C', [_C(2, 'Match the terms habitat and ecosystem', 'following descriptions:'),
       _C(2, 'A:', 'each other.', br=True), _C(2, 'B:', 'organism lives.', br=True)],
      [pt(S('B or where', after='Habitat:'), 3, label=S('Habitat:')),
       pt(S('Ecosystem:', 'each other'), 3)],
      'bio-3-1', 'habitat-and-ecosystem',
      SQ(15, 'Match the terms habitat and ecosystem', 'Where an organism lives.'), 6),
    T('11bii', 'Q11(b)(ii)', 'C', _C(2, 'Name any two abiotic factors'),
      [anyn(S('Mild climate', 'acidic soils'), 2, 3)], 'bio-3-1', 'abiotic-factors',
      SQ(15, 'Name any two abiotic factors'), 6, stem=Q11_ARTICLE),
    T('11biii', 'Q11(b)(iii)', 'C', _C(2, 'What do you understand by the term invasive?'),
      [pt(S('Taking over or not indigenous'), 3)], 'bio-3-1', 'invasive-species',
      SQ(15, 'What do you understand by the term'), 3, stem=Q11_ARTICLE),
    T('11biv', 'Q11(b)(iv)', 'C', _C(2, 'State two ways in which rhododendron', 'habitat.'),
      [anyn(S('One million seeds', 'dispersed by wind'), 2, 3)], 'bio-3-1', 'how-invasive-plants-spread',
      SQ(15, 'State two ways in which rhododendron'), 6, stem=Q11_ARTICLE),
    T('11bv', 'Q11(b)(v)', 'C', _C(2, 'What effect does the dense coverage', 'habitat?'),
      [pt(S('Smothers all growth below', 'biodiversity of the soil'), 3)], 'bio-3-1',
      'effect-of-invasive-plants', SQ(15, 'What effect does the dense coverage'), 3, stem=Q11_ARTICLE),
    T('11bvi', 'Q11(b)(vi)', 'C', _C(2, 'Suggest one benefit this will have on the ecosystem.'),
      [pt(S('Allows biodiversity to be maintained'), 3)], 'bio-3-1', 'conservation-benefit',
      SQ(15, 'Suggest one benefit this will have'), 3,
      stem=Q11_ARTICLE + [_C(2, 'Ecologists in the park are clearing rhododendron.')]),
    T('11ci', 'Q11(c)(i)', 'C', _C(2, 'Why is nutrient recycling important in nature?'),
      [pt(S('So that nutrients can be reused'), 3)], 'bio-3-2', 'nutrient-recycling',
      SQ(16, 'Why is nutrient recycling important'), 3),
    T('11cii1', 'Q11(c)(ii)1', 'C', _C(2, 'Name two ways in which carbon dioxide', 'during the carbon cycle.'),
      [anyn(S('Respiration / decay', 'other correct'), 2, 3)], 'bio-3-2', 'carbon-cycle',
      SQ(16, 'Name two ways in which carbon dioxide'), 6,
      stem=[_C(2, 'The carbon cycle is a part of nutrient recycling.')]),
    T('11cii2', 'Q11(c)(ii)2', 'C', _C(2, 'Name one other nutrient cycle you have studied.'),
      [pt(S('Nitrogen (cycle)'), 3)], 'bio-3-2', 'nutrient-cycles',
      SQ(16, 'Name one other nutrient cycle'), 3,
      stem=[_C(2, 'The carbon cycle is a part of nutrient recycling.')]),
    T('11ciii', 'Q11(c)(iii)', 'C', _C(2, 'Name one type of micro-organism involved'),
      [pt(S('Bacteria or fungi'), 3)], 'bio-3-2', 'decomposers',
      SQ(16, 'Name one type of micro-organism'), 3),
    T('11civ', 'Q11(c)(iv)', 'C', _C(2, 'State two problems associated with waste disposal.'),
      [anyn(S('Unsightly / smell', 'other correct problem given'), 2, 3)], 'bio-3-1',
      'waste-disposal-problems', SQ(16, 'State two problems associated with waste'), 6,
      stem=[_C(2, 'Waste disposal is a problem for society.')]),
    T('11cv', 'Q11(c)(v)', 'C', _C(2, 'Give one way in which waste can be minimised.'),
      [pt(S('Reduce or reuse', 'or other correct'), 3)], 'bio-3-1', 'minimising-waste',
      SQ(16, 'Give one way in which waste'), 3),
    T('12ai', 'Q12(a)(i)', 'C', [_C(3, 'Match the terms genotype and phenotype', 'following sentences:'),
       _C(3, 'A:', 'an organism', br=True), _C(3, 'B:', 'an organism.', br=True)],
      [pt(S('B or genetic makeup', after='Genotype:'), 3, label=S('Genotype:')),
       pt(S('Phenotype:'), 3)], 'bio-1-4', 'genotype-and-phenotype',
      SQ(17, 'Match the terms genotype and phenotype', 'Genetic makeup of an organism.'), 6),
    T('12aii', 'Q12(a)(ii)', 'C', [_C(3, 'Which one of the following sentences (X or Y)', 'homozygous?'),
       _C(3, 'X:', 'a characteristic', br=True), _C(3, 'Y:', 'a characteristic.', br=True)],
      [pt(S('Y'), 3)], 'bio-1-4', 'homozygous',
      SQ(17, 'Which one of the following sentences (X or Y)', 'control a characteristic.'), 3),
    T('12bi', 'Q12(b)(i)', 'C', _C(3, 'Write down the genotype of a rose with pink flowers.'),
      [pt(S('Rr'), 3)], 'bio-1-4', 'incomplete-dominance-genotype',
      SQ(17, 'Write down the genotype of a rose'), 3, stem=[Q12_ROSES], fig='q12-roses'),
    T('12bii1', 'Q12(b)(ii)1', 'C', _C(3, 'Genotypes of the gametes.'),
      [G('tokens', page=17, clip=(168, 405, 190, 428), expect='r', marks=3,
         label=_C(3, 'Genotype of', 'gamete')),
       G('tokens', page=17, clip=(140, 428, 160, 450), expect='R', marks=3,
         label=_C(3, 'Genotypes', 'gametes', after='phenotypes')),
       G('tokens', page=17, clip=(140, 450, 160, 472), expect='r', marks=3,
         label=_C(3, 'Genotypes', 'gametes', after='phenotypes'))],
      'bio-1-4', 'punnett-square-gametes', SQ(17, '1. Genotypes of the gametes.'), 9,
      stem=[Q12_ROSES] + Q12_CROSS, fig='q12-punnett'),
    T('12bii2', 'Q12(b)(ii)2', 'C', _C(3, 'Genotypes of the possible', 'offspring.'),
      [G('tokens', page=17, clip=(165, 535, 192, 553), expect='Rr', marks=3),
       G('tokens', page=17, clip=(165, 556, 192, 575), expect='Rr', marks=3)],
      'bio-1-4', 'punnett-square-offspring', SQ(17, '2. Genotypes of the possible offspring.'), 6,
      stem=[Q12_ROSES] + Q12_CROSS,
      excluded='The scheme prints "Rr" in both offspring boxes, but the r-gamete row of a pink '
               '(Rr) x white (rr) cross is rr, as the scheme\'s own matching phenotype for that '
               'row ("White") shows. Carding the printed answer would teach the misprint, and '
               'correcting it would be the reviewer writing an answer, so the task is excluded '
               'pending a decision. Its siblings (ii)1 and (ii)3 are carded.',
      evidence='Scheme p.17, Q12(b)(ii) "2. Genotypes of the possible offspring.": both offspring '
               'boxes of the completed Punnett square print "Rr" (read from the glyphs at '
               '(165,535)-(192,553) and (165,556)-(192,575)); "3. Matching phenotypes of the '
               'possible offspring." prints "Pink" and "White" beside the same two rows; the '
               'gametes it prints are R and r for the pink rose and r for the white rose. Paper '
               '040 p.3: a rose with pink flowers crossed with a rose with white flowers, captioned '
               'White (rr).'),
    T('12bii3', 'Q12(b)(ii)3', 'C', _C(3, 'Matching phenotypes of', 'the possible offspring.'),
      [pt(S('Pink'), 3), pt(S('White'), 3)], 'bio-1-4', 'punnett-square-phenotypes',
      SQ(17, '3. Matching phenotypes of the possible offspring.'), 6,
      stem=[Q12_ROSES] + Q12_CROSS, fig='q12-punnett',
      notes='Rows in the order the scheme sets them beside its square: the offspring of the R '
            'gamete, then of the r gamete.'),
    T('12biii', 'Q12(b)(iii)', 'C', _C(3, 'If this cross produced 10 new', 'colour?'),
      [pt(S('5 (allow correct %)'), 3)], 'bio-1-4', 'expected-offspring-ratio',
      SQ(17, 'If this cross produced 10 new plants'), 3, stem=[Q12_ROSES] + Q12_CROSS[:1],
      fig='q12-roses'),
] + [
    T('12ci', 'Q12(c)(i)', 'C', _C(3, 'Copy out the diagram into your answerbook and', 'in the DNA molecule.'),
      [G('pair', page=18, clip=(244, 130, 360, 281), index=i, expect=p, marks=3)
       for i, p in enumerate(['C — G', 'G — C', 'A — T', 'T — A'])],
      'bio-1-2', 'complementary-base-pairs', SQ(18, 'Copy out the diagram into your answerbook'), 12,
      stem=Q12_DNA, fig='q12-dna'),
    T('12cii1', 'Q12(c)(ii)1', 'C', _C(3, 'Where in a cell does transcription take place?'),
      [pt(S('Nucleus'), 3)], 'bio-2-3', 'site-of-transcription', SQ(18, '1. Where in a cell does'), 3,
      stem=[_C(3, 'Protein synthesis is a process by which cells make', 'Transcription is the first step.')]),
    T('12cii2', 'Q12(c)(ii)2', 'C', _C(3, 'Name the type of RNA that is produced during', 'transcription.'),
      [pt(S('Messenger RNA or mRNA'), 3)], 'bio-2-3', 'messenger-rna',
      SQ(18, '2. Name the type of RNA'), 3,
      stem=[_C(3, 'Protein synthesis is a process by which cells make', 'Transcription is the first step.')]),
    T('12ciii', 'Q12(c)(iii)', 'C', _C(3, 'Give one structural difference between DNA and RNA.'),
      [anyn(S('DNA contains thymine', 'other correct'), 1, 3)], 'bio-1-2', 'dna-and-rna',
      SQ(18, 'Give one structural difference'), 3),
    T('12civ', 'Q12(c)(iv)', 'C', _C(3, 'Give one application (or use) of DNA profiling.'),
      [anyn(S('Crime scene investigation', 'other correct'), 1, 3)], 'bio-3-3', 'dna-profiling',
      SQ(18, 'Give one application (or use) of DNA'), 3,
      stem=[_C(3, 'DNA profiling is an important biological technique.')]),
    T('13ai', 'Q13(a)(i)', 'C', [_C(4, 'Which of the sentences (A or B)', 'metabolism?'),
       _C(4, 'A:', 'an organism', br=True), _C(4, 'B:', 'undigested material.', br=True)],
      [pt(S('A or sum of all chemical'), 3)], 'bio-2-2', 'metabolism',
      SQ(19, 'Which of the sentences (A or B)'), 3),
    T('13aii', 'Q13(a)(ii)', 'C', _C(4, 'In photosynthesis, small molecules', 'this type of reaction?'),
      [pt(S('Anabolic'), 3)], 'bio-2-2', 'anabolic-reactions', SQ(19, 'Which term, catabolic'), 3),
    T('13aiii', 'Q13(a)(iii)', 'C', _C(4, 'Light energy is required for photosynthesis.', 'source of light energy.'),
      [pt(S('Sun or solar'), 3)], 'bio-2-2', 'source-of-light-energy',
      SQ(19, 'Name the source of light energy.'), 3),
    T('13bi', 'Q13(b)(i)', 'C', _C(4, 'Match compounds A and B', 'Water.'),
      [pt(S('Water'), 3, label=S('A:')), pt(S('Glucose'), 3, label=S('B:'))], 'bio-2-2',
      'photosynthesis-word-equation', SQ(19, 'Match compounds A and B'), 6,
      stem=[_C(4, 'The word equation for photosynthesis')], fig='q13-equation'),
    T('13bii', 'Q13(b)(ii)', 'C', _C(4, 'The incomplete chemical formula shown', 'in each box.'),
      [G('lines', page=19, clip=(110, 408, 215, 440), expect='C H O — 6 12 6', marks=3)],
      'bio-2-2', 'formula-of-glucose', SQ(19, 'Copy the formula'), 3,
      fig='q13-formula'),
    T('13biii', 'Q13(b)(iii)', 'C', _C(4, 'Name the plant cell organelle in which it is found.'),
      [pt(S('Chloroplast'), 3)], 'bio-2-2', 'chloroplast', SQ(19, 'Name the plant cell organelle'), 3,
      stem=[_C(4, 'Chlorophyll is the green pigment')]),
    T('13biv', 'Q13(b)(iv)', 'C', _C(4, 'Give one source of the carbon dioxide'),
      [pt(S('Atmosphere or respiration'), 3)], 'bio-2-2', 'carbon-dioxide-sources',
      SQ(19, 'Give one source for the carbon dioxide'), 3),
    T('13bv', 'Q13(b)(v)', 'C', _C(4, 'Give one fate for the oxygen gas'),
      [pt(S('Released into the atmosphere'), 3)], 'bio-2-2', 'fate-of-oxygen',
      SQ(19, 'Give one fate for the oxygen'), 3),
] + [
    T('13bvi', 'Q13(b)(vi)', 'C', _C(4, 'Electrons and protons are also released', 'after they are released.'),
      [pt(S(row), 3)], 'bio-2-2', f'fate-of-{route}', SQ(19, 'State what happens to either'), 3,
      route=route, decision='Closed choose-one pool (the electrons or the protons): one card each.')
    for route, row in [('electrons', 'Electrons go to chlorophyll'),
                       ('protons', 'Protons go to the proton pool')]
] + [
    T('13bvii', 'Q13(b)(vii)', 'C', _C(4, 'Using your knowledge of photosynthesis', 'can be increased.'),
      [anyn(S('Increase carbon dioxide', 'increase temperature'), 2, 3)], 'bio-2-2',
      'greenhouse-crop-growth', SQ(19, 'Using your knowledge of photosynthesis'), 6),
    T('13ci', 'Q13(c)(i)', 'C', _C(4, 'Which stage (1. or 2.) releases the most energy?'),
      [pt(S('2.'), 3)], 'bio-2-2', 'stage-two-releases-most-energy',
      SQ(20, 'Which stage (1. or 2.) releases'), 3, stem=Q13_C),
    T('13cii', 'Q13(c)(ii)', 'C', _C(4, 'Which stage (1. or 2.) does not require oxygen?'),
      [pt(S('1.'), 3)], 'bio-2-2', 'stage-one-anaerobic', SQ(20, 'Which stage (1. or 2.) does not'), 3,
      stem=Q13_C),
    T('13ciii', 'Q13(c)(iii)', 'C', _C(4, 'To which type of respiration (aerobic or anaerobic)'),
      [pt(S('Anaerobic'), 3)], 'bio-2-2', 'fermentation', SQ(20, 'To which type of respiration'), 3,
      stem=Q13_C + [_C(4, 'Fermentation is a type of respiration.')]),
    T('13civ', 'Q13(c)(iv)', 'C', _C(4, 'Name any two factors that affect the rate'),
      [anyn(S('Temperature / pH', 'other correct'), 2, 3)], 'bio-2-1', 'factors-affecting-enzymes',
      SQ(20, 'Name any two factors'), 6, stem=[_C(4, 'Enzymes are required for respiration to occur.')]),
    T('13cv', 'Q13(c)(v)', 'C', _C(4, 'Copy the axes shown into your answerbook.', 'rate of enzyme action.'),
      [pt(S('pH or temperature'), 3, label=S('X axis label:')),
       pt(S('rate of activity'), 3, label=S('Y axis label:')),
       pt(S('Shape of graph:'), 3, kind='criterion')],
      'bio-2-1', 'enzyme-activity-graph', SQ(20, 'Copy the axes shown'), 9,
      stem=[M('(iv)', 4), _C(4, 'Name any two factors that affect the rate')], fig='q13-axes',
      decision='"Either one of the factors you named" draws on the candidate\'s own (iv) answer, '
               'not a printed pool: one card.'),
    T('14ai', 'Q14(a)(i)', 'C', _C(5, 'Explain in detail the term'),
      [pt(S('(All) food types'), 3), pt(S('in correct amounts'), 3)], 'bio-2-6', 'balanced-diet',
      SQ(21, 'Explain in detail the term'), 6),
    T('14aii', 'Q14(a)(ii)', 'C', _C(5, 'Give the role of peristalsis'),
      [pt(S('To move food'), 3)], 'bio-2-6', 'peristalsis', SQ(21, 'Give the role of peristalsis'), 3),
    T('14bi', 'Q14(b)(i)', 'C', _C(5, 'What is meant by the term digestion?'),
      [pt(S('The breakdown of food'), 3)], 'bio-2-6', 'digestion', SQ(21, 'What is meant by the term digestion'),
      3, stem=[Q14_B]),
    T('14bii', 'Q14(b)(ii)', 'C', _C(5, 'Why must food be digested?'),
      [pt(S('So it can be absorbed'), 3)], 'bio-2-6', 'why-digest-food', SQ(21, 'Why must food be digested'),
      3, stem=[Q14_B]),
    T('14biii1', 'Q14(b)(iii)1', 'C', _C(5, 'Which term (chemical or physical)', 'enzymes are involved?'),
      [pt(S('Chemical'), 3)], 'bio-2-6', 'chemical-digestion',
      SQ(21, 'Which term (chemical or physical)', 'enzymes are involved?'), 3,
      stem=[Q14_B, _C(5, 'The two types of digestion are chemical and physical.')]),
    T('14biii2', 'Q14(b)(iii)2', 'C', _C(5, 'Which term (chemical or physical)', 'teeth are involved?', nth=2),
      [pt(S('Physical'), 3)], 'bio-2-6', 'physical-digestion',
      SQ(21, 'Which term (chemical or physical)', 'teeth are involved?', nth=2), 3,
      stem=[Q14_B, _C(5, 'The two types of digestion are chemical and physical.')]),
    T('14biv1', 'Q14(b)(iv)1', 'C', _C(5, 'Which labelled part', 'produces acid?'),
      [pt(S('C'), 3)], 'bio-2-6', 'stomach-acid', SQ(21, 'Which labelled part'), 3,
      stem=[_C(5, 'The diagram shows the human digestive system.')], fig='q14-digestive'),
    T('14biv2', 'Q14(b)(iv)2', 'C',
      [_C(5, 'Which one of the', 'canal?'), _C(5, '• A → B → C', br=True),
       _C(5, '• B → A → C', br=True), _C(5, '• A → C → B', br=True)],
      [pt(S('A → C → B'), 3)], 'bio-2-6', 'route-through-the-gut',
      SQ(21, 'Which one of the following sequences'), 3,
      stem=[_C(5, 'The diagram shows the human digestive system.')], fig='q14-digestive'),
    T('14bv1', 'Q14(b)(v)1', 'C', _C(5, 'Name any one enzyme produced by the pancreas.'),
      [pt(S('Amylase or lipase'), 3)], 'bio-2-6', 'pancreatic-enzymes',
      SQ(21, 'Name any one enzyme produced'), 3,
      stem=[Q14_B, _C(5, 'The pancreas and liver are', 'digestive system.')]),
    T('14bv2', 'Q14(b)(v)2', 'C', _C(5, 'Give two functions of the liver.'),
      [anyn(S('Detoxify / produce bile', 'other correct'), 2, 3)], 'bio-2-6', 'liver-functions',
      SQ(21, 'Give two functions of the liver'), 6,
      stem=[Q14_B, _C(5, 'The pancreas and liver are', 'digestive system.')]),
    T('14ci', 'Q14(c)(i)', 'C', _C(5, 'What is the main function of the small intestine?'),
      [pt(S('Absorption of nutrients'), 3)], 'bio-2-6', 'small-intestine-function',
      SQ(22, 'What is the main function'), 3, stem=[Q14_C]),
    T('14cii', 'Q14(c)(ii)', 'C', _C(5, 'The small intestine has many villi.', 'diagram of a villus.'),
      [pt(S('Diagram: Villus outline'), 3, kind='criterion'),
       pt(S('Blood supply or lacteal'), 3, kind='criterion'),
       pt(S('Labels:', 'or other correct'), 3)],
      'bio-2-6', 'villus-diagram', SQ(22, 'Draw a labelled diagram of a villus'), 9, stem=[Q14_C]),
    T('14ciii', 'Q14(c)(iii)', 'C',
      [_C(5, 'Which one of the following veins links'), _C(5, 'Hepatic vein;', br=True),
       _C(5, 'Hepatic portal vein;', br=True), _C(5, 'Renal vein', br=True)],
      [pt(S('Hepatic portal vein'), 3)], 'bio-2-6', 'hepatic-portal-vein',
      SQ(22, 'Which one of the following veins'), 3, stem=[Q14_C]),
    T('14civ', 'Q14(c)(iv)', 'C', _C(5, 'Give a function of the large intestine.'),
      [pt(S('Absorbs water'), 3)], 'bio-2-6', 'large-intestine-function',
      SQ(22, 'Give a function of the large intestine'), 3, stem=[Q14_C]),
    T('14cv', 'Q14(c)(v)', 'C', _C(5, 'State any one benefit of having a diet high in fibre.'),
      [pt(S('Prevent constipation', 'other correct'), 3)], 'bio-2-6', 'fibre',
      SQ(22, 'State any one benefit'), 3, stem=[Q14_C]),
    T('14cvi', 'Q14(c)(vi)', 'C', _C(5, 'Give one function of these symbiotic bacteria.'),
      [pt(S('Help digest food'), 3)], 'bio-2-6', 'gut-bacteria', SQ(22, 'Give one function of these symbiotic'),
      3, stem=[Q14_C, _C(5, 'Symbiotic bacteria are present')]),
    T('15a', 'Q15(a)', 'C', _C(6, 'In relation to females and/or males'),
      [anyn(S('Chemical (or hormonal)', '(e.g. abstinence)'), 3, 3,
            note_sel=S('Any three - only one allowed'))],
      'bio-2-5', 'methods-of-contraception', SQ(23, 'In relation to females and/or males'), 9,
      stem=[Q15],
      decision='"females and/or males" is flexible wording, not a pool: one card.'),
    T('15bi', 'Q15(b)(i)', 'C', [_C(6, 'In your answerbook, match each location', 'listed below:')]
      + listed(6, 'match each location', ['Ovulation', 'Fertilisation', 'Implantation']),
      [pt(S('Ovary'), 3, label=S('1. Ovulation:')),
       pt(S('Fallopian tube'), 3, label=S('2. Fertilisation:')),
       pt(S('Endometrium'), 3, label=S('3. Implantation:'))],
      'bio-2-5', 'where-reproductive-events-happen',
      SQ(23, 'In your answerbook, match each location', 'listed below:'), 9, stem=[Q15],
      decision='One matching exercise: three rows.'),
    T('15bii', 'Q15(b)(ii)', 'C', _C(6, 'Give one function of the placenta.'),
      [pt(S('Produce hormones', 'other correct'), 3)], 'bio-2-5', 'placenta',
      SQ(23, 'Give one function of the placenta'), 3,
      stem=[Q15, _C(6, 'The diagram shows a developing foetus'), _C(6, 'The placenta is shown in the diagram.')],
      fig='q15-foetus'),
    T('15biii', 'Q15(b)(iii)', 'C', [_C(6, 'There are three stages to the birth process:', 'three descriptions:')]
      + listed(6, 'three descriptions:', ['uterus.', 'uterus.', 'uterus.']),
      [pt(S('Birth'), 3, label=S('1: The passage of the foetus')),
       pt(S('Afterbirth'), 3, label=S('2: The passage of the placenta')),
       pt(S('Labour', after='3: Rhythmical'), 3, label=S('3: Rhythmical'))],
      'bio-2-5', 'stages-of-birth',
      SQ(23, 'There are three stages to the birth', 'three descriptions:'), 9, stem=[Q15],
      decision='One matching exercise: three rows.'),
    T('15biv', 'Q15(b)(iv)', 'C',
      [_C(6, 'Which one of the following hormones is', 'milk production?'),
       _C(6, 'Prolactin; Insulin', br=True)],
      [pt(S('Prolactin', after='Insulin'), 3)], 'bio-2-5', 'prolactin',
      SQ(23, 'Which one of the following hormones'), 3,
      stem=[Q15, _C(6, 'Milk production occurs after the birth process.')]),
    T('15bv', 'Q15(b)(v)', 'C', _C(6, 'Give one biological benefit of breastfeeding.'),
      [pt(S('Balanced nutrition', 'other correct'), 3)], 'bio-2-5', 'breastfeeding',
      SQ(23, 'Give one biological benefit'), 3, stem=[Q15]),
    T('15ci', 'Q15(c)(i)', 'C', [_C(6, 'Match each of the parts labelled A, B and C to', 'following terms:')]
      + listed(6, 'Match each of the parts labelled', ['Midpiece (neck)', 'Head', 'Tail']),
      [pt(S('B'), 3, label=S('1. Midpiece (neck)')),
       pt(S('C', after='2. Head'), 3, label=S('2. Head')),
       pt(S('A', after='3. Tail'), 3, label=S('3. Tail'))],
      'bio-2-5', 'parts-of-a-sperm-cell', SQ(24, 'Match each of the parts labelled'), 9,
      stem=[Q15, Q15_SPERM], fig='q15-sperm',
      labels=[L('A', _C(6, 'Tail'), True), L('B', _C(6, 'Midpiece (neck)'), True),
              L('C', _C(6, 'Head'), True)],
      decision='One matching exercise: three rows.'),
    T('15cii', 'Q15(c)(ii)', 'C', _C(6, 'Name the organ in the male reproductive', 'sperm cells are produced.'),
      [pt(S('Testes'), 3)], 'bio-2-5', 'testes', SQ(24, 'Name the organ in the male'), 3, stem=[Q15]),
    T('15ciii', 'Q15(c)(iii)', 'C', _C(6, 'Name the hormone responsible for sperm', 'production.'),
      [pt(S('Testosterone'), 3)], 'bio-2-5', 'testosterone', SQ(24, 'Name the hormone responsible'), 3,
      stem=[Q15]),
    T('15civ', 'Q15(c)(iv)', 'C', _C(6, 'What is meant by the term infertility?'),
      [pt(S('Inability to produce offspring'), 3)], 'bio-2-5', 'infertility',
      SQ(24, 'What is meant by the term infertility'), 3, stem=[Q15]),
    T('15cv', 'Q15(c)(v)', 'C', _C(6, 'Give one cause of infertility in males.'),
      [pt(S('Hormonal or low sperm count'), 3)], 'bio-2-5', 'male-infertility',
      SQ(24, 'Give one cause of infertility'), 3, stem=[Q15]),
    T('15cvi', 'Q15(c)(vi)', 'C', _C(6, 'What is meant by the term in vitro fertilisation?'),
      [pt(S('Fusion of sperm and egg'), 3)], 'bio-2-5', 'in-vitro-fertilisation',
      SQ(24, 'What is meant by the term in vitro'), 3,
      stem=[Q15, _C(6, 'In vitro fertilisation is one method')]),
    # Q16: any two of (a)-(d), each 30.
    T('16ai', 'Q16(a)(i)', 'C', [_C(7, 'Match each of the parts labelled A, B and C to the', 'following terms:')]
      + listed(7, 'Match each of the parts labelled', ['Ligament', 'Synovial fluid', 'Cartilage']),
      [pt(S('A', after='Ligament'), 3, label=S('Ligament')),
       pt(S('C', after='Synovial fluid'), 3, label=S('Synovial fluid')),
       pt(S('B', after='Cartilage'), 3, label=S('Cartilage'))],
      'bio-2-4', 'synovial-joint-parts', SQ(25, 'Match each of the parts labelled'), 9,
      stem=[Q16_JOINT], fig='q16-joint',
      labels=[L('A', _C(7, 'Ligament'), True), L('B', _C(7, 'Cartilage'), True),
              L('C', _C(7, 'Synovial fluid'), True)],
      decision='One matching exercise: three rows.'),
    T('16aii', 'Q16(a)(ii)', 'C', _C(7, 'Give one function of cartilage.'),
      [pt(S('Shock absorption', 'other correct'), 3)], 'bio-2-4', 'cartilage',
      SQ(25, 'Give one function of cartilage'), 3),
] + [
    T(f'16aiii{n}', f'Q16(a)(iii){n}', 'C', _C(7, joint),
      [pt(S(row), 3, kind=kind)], 'bio-2-4', concept, SQ(25, f'{joint}:'), 3, stem=[Q16_JOINTS])
    for n, joint, row, kind, concept in [
        (1, 'A synovial joint', 'Correct location given', 'criterion', 'synovial-joints'),
        (2, 'An immovable joint', 'Skull or other correct', None, 'immovable-joints'),
        (3, 'A slightly movable joint', 'Vertebral column or named example', None,
         'slightly-movable-joints')]
] + [
    T('16aiv', 'Q16(a)(iv)', 'C',
      [_C(7, 'Which one of the following terms is used to describe these muscle pairs?'),
       _C(7, 'Antigen;', br=True), _C(7, 'Antagonistic', br=True)],
      [pt(S('Antagonistic', after='Antagonistic'), 3)], 'bio-2-4', 'antagonistic-muscles',
      SQ(25, 'Which one of the following terms'), 3,
      stem=[_C(7, 'Skeletal muscles generally work in pairs.')]),
    T('16av', 'Q16(a)(v)', 'C', _C(7, 'Describe, using an example, how a muscle pair'),
      [pt(S('When one muscle contracts'), 3), pt(S('At least one muscle named'), 3, kind='criterion')],
      'bio-2-4', 'how-muscle-pairs-move', SQ(25, 'Describe, using an example'), 6),
    T('16bi', 'Q16(b)(i)', 'C', [_C(7, 'In your answerbook, match the labels', 'following terms:')]
      + listed(7, 'In your answerbook, match the labels', ['Hair', 'Sebaceous gland', 'Epidermis', 'Sweat duct']),
      [pt(S('Q', after='Hair'), 3, label=S('Hair')),
       pt(S('S', after='Sebaceous gland'), 3, label=S('Sebaceous gland')),
       pt(S('P', after='Epidermis'), 3, label=S('Epidermis')),
       pt(S('R', after='Sweat duct'), 3, label=S('Sweat duct'))],
      'bio-2-4', 'skin-structure', SQ(26, 'In your answerbook, match the labels'), 12,
      stem=[Q16_SKIN, _C(7, 'The diagram shows the structure of', 'the skin.')], fig='q16-skin',
      decision='One matching exercise: four rows.'),
    T('16bii', 'Q16(b)(ii)', 'C', _C(7, 'Give a function of the skin other than', 'general defence system.'),
      [pt(S('Excretion or vitamin D'), 3)], 'bio-2-4', 'functions-of-skin',
      SQ(26, 'Give a function of the skin'), 3, stem=[Q16_SKIN]),
    T('16biii', 'Q16(b)(iii)', 'C', _C(7, 'What is a pathogen?'),
      [pt(S('Disease-causing organism'), 3)], 'bio-2-4', 'pathogens', SQ(26, 'What is a'), 3,
      stem=[Q16_SKIN]),
    T('16biv', 'Q16(b)(iv)', 'C', _C(7, 'If a pathogen enters the body, give', 'eliminate the pathogen.'),
      [pt(S('Lymphocytes produce antibodies'), 3)], 'bio-2-4', 'specific-defence',
      SQ(26, 'If a pathogen enters the body'), 3, stem=[Q16_SKIN]),
    T('16bv', 'Q16(b)(v)', 'C', _C(7, 'Which type of immunity (active or passive)'),
      [pt(S('Active'), 3)], 'bio-2-4', 'active-immunity', SQ(26, 'Which type of immunity'), 3,
      stem=[_C(7, 'Immunity is the ability to resist infection')]),
    T('16bvi', 'Q16(b)(vi)', 'C', _C(7, 'Name two organs that are part of the specific'),
      [anyn(S('Spleen / thymus', 'lymph nodes'), 2, 3)], 'bio-2-4', 'organs-of-the-immune-system',
      SQ(26, 'Name two organs that are part'), 6),
    T('16ci', 'Q16(c)(i)', 'C', [_C(8, 'Match the letters A, B and C from the diagram to the', 'following structures:')]
      + listed(8, 'Match the letters A, B and C', ['Tricuspid valve', 'Ventricle', 'Vena cava']),
      [pt(S('B', after='Tricuspid valve'), 3, label=S('Tricuspid valve')),
       pt(S('C', after='Ventricle'), 3, label=S('Ventricle')),
       pt(S('A', after='Vena cava'), 3, label=S('Vena cava'))],
      'bio-2-6', 'right-side-of-the-heart', SQ(27, 'Match the letters A, B and C'), 9,
      stem=[Q16_HEART], fig='q16-heart', decision='One matching exercise: three rows.'),
    T('16cii', 'Q16(c)(ii)', 'C', _C(8, 'Copy the diagram, without the labels', 'right-hand side of the heart.'),
      [pt(S('Arrow 1 showing correct direction'), 3, kind='criterion'),
       pt(S('Arrow 2 showing correct direction'), 3, kind='criterion')],
      'bio-2-6', 'blood-flow-through-the-heart', SQ(27, 'Copy the diagram, without the labels'), 6,
      stem=[Q16_HEART], fig='q16c-ii-scheme', qfig='q16c-ii-question', source_pages=[8],
      decision='The printed question and its diagram are shown as the paper prints them; the '
               'scheme\'s drawing of the arrows waits for the reveal.'),
    T('16ciii', 'Q16(c)(iii)', 'C', _C(8, 'To which organ is the blood from part C', 'gain oxygen?'),
      [pt(S('Lungs'), 3)], 'bio-2-6', 'pulmonary-circulation', SQ(27, 'To which organ is the blood'), 3,
      stem=[Q16_HEART], fig='q16-heart'),
    T('16civ', 'Q16(c)(iv)', 'C', _C(8, 'Name the molecule found in red blood cells', 'around the body.'),
      [pt(S('Haemoglobin'), 3)], 'bio-2-6', 'haemoglobin', SQ(27, 'Name the molecule found'), 3),
    T('16cv', 'Q16(c)(v)', 'C', _C(8, 'State two ways in which the structure of arteries and', 'veins differ.'),
      [anyn(S('Arteries have thick walls', 'large lumen'), 2, 3)], 'bio-2-6', 'arteries-and-veins',
      SQ(27, 'State two ways in which the structure'), 6),
] + [
    T('16cvi', 'Q16(c)(vi)', 'C', _C(8, 'Briefly describe the effect of one of the following', 'smoking or diet or exercise.'),
      [pt(S('Any one correct effect'), 3, kind='criterion', note_sel=S('Effect must match factor'))],
      'bio-2-6', f'{factor}-and-the-circulatory-system', SQ(27, 'Briefly describe the effect'), 3,
      route=factor, decision='Closed choose-one pool of three printed factors: one card each.')
    for factor in ROUTES['Q16(c)(vi)']
] + [
    T('16di', 'Q16(d)(i)', 'C', _C(8, 'Based on information provided in the diagrams above', 'tissues labelled A and B.'),
      [pt(S('A:'), 3), pt(S('Phloem'), 3, label=S('B:'))], 'bio-2-6', 'xylem-and-phloem',
      SQ(28, 'Based on information provided'), 6, stem=[Q16_TISSUE], fig='q16-tissues',
      labels=[L('A', S('Xylem', page=28), True), L('B', S('Phloem', page=28), True)]),
    T('16dii', 'Q16(d)(ii)', 'C', _C(8, 'Which tissue, A or B, transports water and minerals?'),
      [pt(S('A or xylem'), 3)], 'bio-2-6', 'xylem-carries-water', SQ(28, 'Which tissue, A or B, transports water'),
      3, stem=[Q16_TISSUE], fig='q16-tissues'),
    T('16diii', 'Q16(d)(iii)', 'C', _C(8, 'Which tissue, A or B, transports food?'),
      [pt(S('B or phloem'), 3)], 'bio-2-6', 'phloem-carries-food', SQ(28, 'Which tissue, A or B, transports food'),
      3, stem=[Q16_TISSUE], fig='q16-tissues'),
    T('16div', 'Q16(d)(iv)', 'C', _C(8, 'In which of the tissues, A or B'),
      [pt(S('B'), 3)], 'bio-2-6', 'companion-cells', SQ(28, 'In which of the tissues'), 3,
      stem=[Q16_TISSUE], fig='q16-tissues'),
    T('16dv', 'Q16(d)(v)', 'C', _C(8, 'Copy the diagram showing tissue A', 'direction of flow.'),
      [pt(S('Arrow point upwards'), 3)], 'bio-2-6', 'direction-of-flow-in-xylem',
      SQ(28, 'Copy the diagram showing tissue A'), 3, stem=[Q16_TISSUE], fig='q16-tissues'),
    T('16dvi', 'Q16(d)(vi)', 'C', _C(8, 'Name any one process that causes the movement'),
      [pt(S('Root pressure or transpiration'), 3)], 'bio-2-6', 'water-movement-in-plants',
      SQ(28, 'Name any one process'), 3),
    T('16dvii', 'Q16(d)(vii)', 'C', _C(8, 'Draw a longitudinal section of a stem'),
      [pt(S('Drawing'), 3, kind='criterion'), pt(S('Vascular tissue labelled'), 3, kind='criterion')],
      'bio-2-6', 'stem-longitudinal-section', SQ(28, 'Draw a longitudinal section'), 6),
    T('16dviii', 'Q16(d)(viii)', 'C', _C(8, 'Name the structures found in the stem'),
      [pt(S('Lenticels'), 3)], 'bio-2-6', 'lenticels', SQ(28, 'Name the structures found'), 3),
    # Q17: any two of (a)-(d), each 30.
    T('17ai', 'Q17(a)(i)', 'C', [_C(9, 'In your answerbook, match the', 'parts listed below:')]
      + listed(9, 'parts listed below:', ['Pinna', 'Eustachian tube', 'Semi-circular canals', 'Eardrum']),
      [pt(S('A', after='Pinna'), 3, label=S('Pinna')),
       pt(S('D', after='Eustachian tube'), 3, label=S('Eustachian tube')),
       pt(S('C', after='Semi-circular canals'), 3, label=S('Semi-circular canals')),
       pt(S('B', after='Eardrum'), 3, label=S('Eardrum'))],
      'bio-2-4', 'parts-of-the-ear', SQ(29, 'In your answerbook, match the labels'), 12,
      stem=[Q17_EAR], fig='q17-ear', decision='One matching exercise: four rows.'),
    T('17aii', 'Q17(a)(ii)', 'C', [_C(9, 'In your answerbook, match', 'functions below:', nth=2)]
      + listed(9, 'to their functions below:', ['Balance', 'Equalisation of air pressure', 'middle ear']),
      [pt(S('C or semi-circular canals'), 3, label=S('Balance')),
       pt(S('D or Eustachian tube'), 3, label=S('Equalisation of air pressure')),
       pt(S('B or eardrum'), 3, label=S('Transfer of sound vibrations'))],
      'bio-2-4', 'functions-of-ear-parts', SQ(29, 'In your answerbook, match three'), 9,
      stem=[Q17_EAR, M('(i)', 9), _C(9, 'In your answerbook, match the', 'parts listed below:')]
      + listed(9, 'parts listed below:', ['Pinna', 'Eustachian tube', 'Semi-circular canals', 'Eardrum']),
      fig='q17-ear',
      decision='One matching exercise: three rows. The stem carries the parts "listed above" in (i).'),
    T('17aiii', 'Q17(a)(iii)', 'C',
      [_C(9, 'Which one of the following nerves carries'), _C(9, 'Optic nerve or Auditory nerve.', br=True)],
      [pt(S('Auditory nerve'), 3)], 'bio-2-4', 'auditory-nerve', SQ(29, 'Which one of the following nerves'), 3),
] + [
    T('17aiv', 'Q17(a)(iv)', 'C', _C(9, 'Name one disorder of the ear or the eye', 'named disorder.'),
      [pt(S('Correctly named disorder'), 3, kind='criterion'),
       pt(S('Correctly given and matching'), 3, kind='criterion')],
      'bio-2-4', f'disorder-of-the-{organ}', SQ(29, 'Name one disorder of the ear'), 6, route=organ,
      decision='Closed choose-one pool (the ear or the eye): one card each.')
    for organ in ROUTES['Q17(a)(iv)']
] + [
    T('17bi', 'Q17(b)(i)', 'C', _C(9, 'Which type of gland (exocrine or endocrine)', 'hormones?'),
      [pt(S('Endocrine'), 3)], 'bio-2-4', 'endocrine-glands', SQ(30, 'Which type of gland'), 3),
    T('17bii', 'Q17(b)(ii)', 'C', _C(9, 'Explain in detail the term hormone.'),
      [anyn(S('A chemical / messenger', 'tissue or organ (or described)'), 2, 3)], 'bio-2-4',
      'hormones', SQ(30, 'Explain in detail the term'), 6),
    T('17biii', 'Q17(b)(iii)', 'C',
      [_C(9, 'Copy the table below into your answerbook and complete it', 'completed as examples.'),
       _C(9, 'List:', 'Adrenaline.', br=True)],
      [pt(S('Pituitary', after='Function of hormone'), 3, label=S('Name of gland'),
          note_sel=S('Growth', after='Growth hormone'), note_lead='Table row:'),
       pt(S('Adrenal', after='Growth hormone'), 3, label=S('Name of gland'),
          note_sel=S('‘Fight or flight’ response'), note_lead='Table row:'),
       pt(S('Adrenaline', after='Growth hormone'), 3, label=S('Hormone'),
          note_sel=S('‘Fight or flight’ response'), note_lead='Table row:'),
       pt(S('Thyroxine', after='Thyroid'), 3, label=S('Hormone'),
          note_sel=S('Controls the rate of metabolism'), note_lead='Table row:')],
      'bio-2-4', 'glands-and-hormones', SQ(30, 'Copy the table below'), 12, fig='q17-table'),
    T('17biv', 'Q17(b)(iv)', 'C', _C(9, 'State two ways in which hormone action differs'),
      [anyn(S('Hormone action is slow', 'localised (or described)'), 2, 3)], 'bio-2-4',
      'hormones-and-nerves', SQ(30, 'State two ways in which hormone action'), 6),
    T('17bv', 'Q17(b)(v)', 'C', _C(9, 'Give one example of the use of hormone supplements.'),
      [pt(S('Hormonal injection'), 3)], 'bio-2-4', 'hormone-supplements',
      SQ(30, 'Give one example of the use of hormone'), 3),
    T('17ci', 'Q17(c)(i)', 'C', [_C(10, 'In your answerbook, match the letters', 'flower parts:')]
      + listed(10, 'X, Y and Z to the following flower parts:', ['Ovary', 'Filament', 'Stigma']),
      [pt(S('Z', after='Ovary'), 3, label=S('Ovary')),
       pt(S('Y', after='Filament'), 3, label=S('Filament')),
       pt(S('X', after='Stigma'), 3, label=S('Stigma'))],
      'bio-2-5', 'parts-of-a-flower', SQ(31, 'In your answer book, match the letters'), 9,
      stem=[Q17_FLOWER], fig='q17-flower', decision='One matching exercise: three rows.'),
    T('17cii', 'Q17(c)(ii)', 'C', _C(10, 'Does the', 'male gamete?'),
      [pt(S('Male'), 3)], 'bio-2-5', 'pollen-carries-the-male-gamete',
      SQ(31, 'Does the pollen grain contain'), 3,
      stem=[_C(10, 'The anther produces', 'pollen grains.')]),
    T('17ciii', 'Q17(c)(iii)', 'C', _C(10, 'Explain the term pollination.'),
      [pt(S('Transfer of pollen from the anther'), 3)], 'bio-2-5', 'pollination',
      SQ(31, 'Explain the term pollination'), 3),
    T('17civ', 'Q17(c)(iv)', 'C', _C(10, 'Name two methods by which plants can be pollinated.'),
      [anyn(S('Self / insect', 'water'), 2, 3)], 'bio-2-5', 'methods-of-pollination',
      SQ(31, 'Name two methods by which plants'), 6),
    T('17cv', 'Q17(c)(v)', 'C', _C(10, 'Which part of the flower is responsible for seed production?'),
      [pt(S('Ovary or Z'), 3)], 'bio-2-5', 'ovary-and-seeds', SQ(31, 'Which part of the flower'), 3,
      stem=[_C(10, 'Following pollination, fertilisation and seed formation occur.')]),
    T('17cvi', 'Q17(c)(vi)', 'C', _C(10, 'Give any two ways in which seeds can be dispersed.'),
      [anyn(S('Wind / water / animal / self'), 2, 3)], 'bio-2-5', 'seed-dispersal',
      SQ(31, 'Give any two ways in which seeds'), 6,
      stem=[_C(10, 'Seeds are dispersed, which means')]),
    T('17di', 'Q17(d)(i)', 'C', [_C(10, 'Match diagram A and diagram B', 'named organisms:')]
      + listed(10, 'Match diagram A and diagram B', ['Yeast', 'Rhizopus (bread mould)']),
      [pt(S('B', after='Yeast'), 3, label=S('Yeast')),
       pt(S('A', after='Rhizopus (bread mould)'), 3, label=S('Rhizopus (bread mould)'))],
      'bio-3-2', 'yeast-and-rhizopus', SQ(32, 'Match diagram A and diagram B'), 6,
      stem=[Q17_ORG], fig='q17-organisms', decision='One matching exercise: two rows.'),
    T('17dii', 'Q17(d)(ii)', 'C',
      [_C(10, 'To which one of the following kingdoms do', 'both of these organisms belong?'),
       _C(10, 'Monera;', br=True), _C(10, 'Protista;', br=True), _C(10, 'Fungi.', br=True)],
      [pt(S('Fungi', after='Fungi.'), 3)], 'bio-3-2', 'kingdom-fungi',
      SQ(32, 'To which one of the following kingdoms'), 3, stem=[Q17_ORG], fig='q17-organisms'),
    T('17diii', 'Q17(d)(iii)', 'C', _C(10, 'Copy the following table into your', 'budding'),
      [pt(S('Budding', after='Reproduces by'), 3, label=S('Yeast', after='Reproduces by')),
       pt(S('Spores', after='Budding'), 3, label=S('Rhizopus', after='Budding'))],
      'bio-3-2', 'asexual-reproduction-in-fungi', SQ(32, 'Copy the following table'), 6,
      stem=[_C(10, 'Yeast and Rhizopus can reproduce asexually.')], fig='q17d-table'),
    T('17div', 'Q17(d)(iv)', 'C', [_C(10, 'Match the terms heterotrophic and autotrophic', 'following descriptions:')]
      + listed(10, 'Match the terms heterotrophic and autotrophic', ['own food.', 'other organisms.']),
      [pt(S('Autotrophic'), 3, label=S('An organism that makes its own food.')),
       pt(S('Heterotrophic'), 3, label=S('An organism that obtains its food'))],
      'bio-3-2', 'autotrophs-and-heterotrophs', SQ(32, 'Match the terms heterotrophic'), 6,
      stem=[_C(10, 'Both yeast and Rhizopus are heterotrophic.')],
      decision='One matching exercise: two rows.'),
    T('17dv', 'Q17(d)(v)', 'C', [_C(10, 'Which one of the following sequences of', 'order?'),
       _C(10, 'A:', 'fertilisation', br=True), _C(10, 'B:', 'fertilisation', br=True)],
      [pt(S('A or Progametangium'), 3)], 'bio-3-2', 'sexual-reproduction-in-rhizopus',
      SQ(32, 'Which one of the following sequences'), 3,
      stem=[_C(10, 'Rhizopus can also', 'reproduce sexually.')]),
    T('17dvi', 'Q17(d)(vi)', 'C', [_C(10, 'Match the terms asepsis and sterility', 'following descriptions:')]
      + listed(10, 'Match the terms asepsis and sterility', ['micro-organisms.', 'pathogens.']),
      [pt(S('Sterility', after='absence of all'), 3, label=S('The technique that ensures absence of all')),
       pt(S('Asepsis', after='absence of pathogens'), 3, label=S('The technique that ensures absence of pathogens'))],
      'bio-3-2', 'asepsis-and-sterility', SQ(32, 'Match the terms, asepsis and sterility'), 6,
      stem=[_C(10, 'Asepsis and sterility are important techniques', 'in the laboratory.')],
      decision='One matching exercise: two rows.'),
]
