"""2023 HL Paper 2: review ledger, restored prompts, re-citations, row repairs, 5 added cards."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 4, 7, 10], '10D': [0, 3, 5, 8, 10],
      '15D': [0, 4, 8, 12, 15], '20D': [0, 6, 12, 17, 20]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None, extra=None):
    c = dict(id='maths-2023-hl-p2-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-higher-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    if extra: c.update(extra)
    cards.append(c)

spin = 'A circular spinner has 12 sectors, as follows: 5 sectors are labelled €6; 3 sectors are labelled €9; the rest are labelled €0. In a game, the spinner is spun once. The spinner is equally likely to land on each sector. The player gets the amount of money shown on the sector that the spinner lands on.'
A('1-a', 'Q1(a)', '10C', [39], [4], '1-2', 'probability', 'Fiona plays the game a number of times. Work out the probability that Fiona gets €6, then €9, then €6 the first three times she plays. Give your answer correct to 4 decimal places.', stem=spin)
A('1-b', 'Q1(b)', '10D', [39], [4, 5], '1-3', 'probability', 'Rohan also plays the game a number of times. Find the probability that Rohan gets €9 for the 3rd time, on the 8th time that he plays the game. Give your answer correct to 4 decimal places.', stem=spin)
A('1-c', 'Q1(c)', '10D', [40], [4, 5], '1-2', 'probability', 'Olga plays the game 2 times. Find the probability that Olga gets less than €16 in total from playing the game. Give your answer correct to 4 decimal places.', stem=spin)
A('2-a', 'Q2(a)', '10C', [41], [6], '2-3', 'trigonometry-functions-identities', 'Prove that sin(A + B) = sin A cos B + cos A sin B.')
A('2-b', 'Q2(b)', '10C', [41], [6], '2-3', 'trigonometry-functions-identities', 'Using the formula in part (a), and without using a calculator, find the value of sin 75°. Give your answer in surd form.', stem='Part (a) proves that sin(A + B) = sin A cos B + cos A sin B.')
A('2-c', 'Q2(c)', '10D', [42], [7], '2-3', 'trigonometry-functions-identities', 'Find all solutions of the following equation in t, for 0° ≤ t ≤ 360°: sin t = sin(2t)')
A('3-a', 'Q3(a)', '15D', [43], [8], '2-2', 'co-ordinate-geometry-of-the-line', 'Find the area of the triangle with vertices (4, 6), (−3, −1), and (0, 11).')
ab = 'A(−1, k) and B(5, l) are two points, where k, l ∈ ℚ.'
A('3-b-i', 'Q3(b)(i)', '5B', [44], [8], '2-2', 'co-ordinate-geometry-of-the-line', 'Show that the midpoint of [AB] is (2, (k + l)/2).', stem=ab)
A('3-b-ii', 'Q3(b)(ii)', '10D', [45], [9], '2-2', 'co-ordinate-geometry-of-the-line,algebra-simultaneous-equations', 'The perpendicular bisector of [AB] is: 3x + 2y − 14 = 0. Find the value of l and the value of k.', stem=ab)
circ = 'The circle c has equation: (x − h)² + (y + 3)² = 12, where h ∈ ℝ.'
A('4-a-i', 'Q4(a)(i)', '10C', [46], [10], '2-2', 'co-ordinate-geometry-of-the-circle', 'Write down the centre and radius of the circle c. Give your answer in terms of h, where appropriate.', stem=circ)
A('4-ii', 'Q4(a)(ii)', '15D', [46], [10], '2-2', 'co-ordinate-geometry-of-the-circle,co-ordinate-geometry-of-the-line', 'The perpendicular distance from the line x − 4y + 7 = 0 to the centre of the circle c is 5 units. Work out the two possible values of h. Give each answer in surd form.', stem=circ)
A('4-b', 'Q4(b)', '5D', [47], [11], '2-2', 'co-ordinate-geometry-of-the-circle', 'The circle s passes through the points (8, 1), (a, 3), and (a, −5), as shown in the diagram on the right (not to scale), where 0 < a < 5, a ∈ ℝ. The radius of the circle s is √20. Find the equation of the circle s.')
cubes = 'Rohan has a large number of small cubes. The cubes are identical in size.'
A('5-a-i', 'Q5(a)(i),Q5(a)(ii),Q5(a)(iii)', '20D', [48], [12], '1-6', 'statistics-descriptive-statistics', '(i) Work out the mean and standard deviation of the number of red cubes per trial, for these 7 trials. Give each answer correct to 1 decimal place. (ii) Work out the correlation coefficient between the number of red cubes and the number of green cubes per trial, for these 7 trials. Give your answer correct to 3 decimal places. (iii) Rohan repeats this experiment a large number of times. Explain why you would expect the correlation coefficient between the number of red cubes and the number of green cubes per trial to be negative.',
  stem=cubes + ' Some of the cubes are red, some are green, and the rest are blue. Rohan carries out an experiment in which he picks out 5 different cubes at random. He records the number of cubes of each colour, and replaces the 5 cubes. He then repeats this process a number of times. The table below shows the number of cubes of each colour the first 7 times Rohan does this, labelled Trial A to Trial G: red 0, 3, 2, 2, 4, 5, 1; green 4, 2, 0, 3, 0, 0, 2; blue 1, 0, 3, 0, 1, 0, 2.')
A('5-b', 'Q5(b)', '10C', [48], [13], '3-4', 'area-volume', 'Rohan makes a solid cuboid of dimensions 5 × 3 × 4 using his small cubes. Each small cube has sides of length 1 unit. Some of the small cubes have 1 face, 2 faces, or 3 faces on the outside of the cuboid. Other small cubes have no faces on the outside of the cuboid. In the diagram below, the small cube that is shaded has 3 faces on the outside of the cuboid. Fill in the table below, showing the number of small cubes with 3 faces, 2 faces, 1 face, or no faces on the outside of this cuboid. Show your working out. One of the values is filled in for you: 22 small cubes have 1 face on the outside.', stem=cubes)
A('6-a', 'Q6(a)', '5B', [49], [14], '2-1', 'geometry-constructions-proofs', 'State whether the following statement is true or false: Two angles are vertically opposite if, and only if, they are equal in size. Justify your answer.')
rect = 'The two diagrams below show the same rectangle, ACEG (not to scale). The points B, D, and F lie on [AC], [CE], and [EG], respectively, as shown. |AB| = 20 cm, |BC| = 30 cm, and |AG| = 90 cm. |∠GFA| = |∠EFD| = |∠DBC| = θ, where θ ∈ ℝ. In Diagram B, [GE] and [BD] are extended, and they meet at the point H.'
A('6-b-i', 'Q6(b)(i)', '15D', [49], [14, 15], '2-1', 'geometry-constructions-proofs', 'Prove that |FE| = |EH|, in Diagram B. Use congruent triangles. Give a reason for each statement that you make in your proof.', stem=rect)
A('6-b-ii', 'Q6(b)(ii)', '10D', [50], [14, 15], '2-3', 'trigonometry-triangles,geometry', 'Hence, or otherwise, find the size of the angle θ. Give your answer correct to the nearest degree.', stem=rect)
olga = 'Olga is a cyclist.'
A('7-a', 'Q7(a)', '10C', [51], [16], '2-3', 'trigonometry-triangles', 'The diagram below shows a road [AB], which is not to scale. AC is horizontal and BC is vertical. |BC| = 9 m and |AB| = 70 m. The gradient of the road [AB] is |BC|/|AC| written as a percentage. Find the gradient of [AB], correct to the nearest percent.', stem=olga)
A('7-b', 'Q7(b)', '10D', [51], [17], '2-3', 'trigonometry-triangles', 'Olga wants to measure the vertical height of a hill. The point H is at the top of the hill. The points R and P are 20 m apart on horizontal ground, at the bottom of the hill. Olga measures the angle of elevation from R to H. Taking O to be the point directly below H that is horizontal with R and P, Olga also measures the angles ∠OPR and ∠ORP. All of these are shown in the diagram below (not to scale): the angle of elevation is 17°, |∠ORP| = 88° and |∠OPR| = 87°. Work out the distance |OH|, the vertical height of the top of the hill relative to the points R and P. Give your answer correct to the nearest metre.', stem=olga)
lungs = olga + ' Olga has some tests done to measure her lung capacity. When she is resting, the volume of air, V, in her lungs after t seconds can be modelled by: V(t) = 2 − 0·4 cos((π/2)t), where V is in litres, t ≥ 0 is the time in seconds from a given point in time, and (π/2)t is in radians. The diagram below shows the graph of the function y = V(t) for the first 9 seconds.'
A('7-c', 'Q7(c),Q7(d)', '10D', [52], [18], '2-3', 'trigonometry-functions-identities,differentiation-applications', '(c) Find the values marked a and b on the graph, the minimum and maximum values of V. (d) What is the connection between V′(t), the derivative of V, and whether Olga is breathing in or breathing out?', stem=lungs)
A('7-e-i', 'Q7(e)(i)', '5B', [52], [18, 19], '2-3', 'trigonometry-functions-identities', 'Use the formula V(t) = 2 − 0·4 cos((π/2)t) to find each of the following, when Olga is resting. Give each answer correct to 3 decimal places. Find the volume of air in Olga’s lungs, half a second after t = 0.', stem=lungs)
A('7-e-ii', 'Q7(e)(ii)', '10C', [52], [18, 19], '5-2', 'differentiation-applications,trigonometry-functions-identities', 'Use the formula V(t) = 2 − 0·4 cos((π/2)t), when Olga is resting, giving your answer correct to 3 decimal places. Find the rate at which the volume of air in Olga’s lungs is increasing, half a second after t = 0.', stem=lungs)
A('7-f', 'Q7(f)', '5D', [53], [18, 19], '2-3', 'trigonometry-functions-identities', 'Olga’s breathing is also measured while she is doing gentle exercise. During this time: when she breathes in fully, the volume of air in her lungs is 3·6 litres; when she breathes out fully, the volume of air in her lungs is 1·3 litres; she breathes in and out twice as many times per minute as when she is resting. Use this information to write a formula for E(t), the volume of air in Olga’s lungs during this time, t seconds after she has breathed out fully. Give your answer in the form E(t) = a + b cos(ct), where a, b, c, t ∈ ℝ, and ct is in radians.', stem=lungs)
game = 'An online word game involves trying to guess a five-letter word in as few attempts as possible. For this game, each player is given a score s, where s ∈ ℝ, based on how many attempts it takes them to guess the word.'
A('8-a', 'Q8(a)', '10D', [54], [20], '1-3', 'statistics-z-scores', 'In Ireland, players’ scores are approximately normally distributed, with a mean of 3·87 and a standard deviation of 0·36. A player is selected at random from the players in Ireland. Find the probability that this player has a score of less than 3·5.', stem=game)
galway = game + ' A random sample of 64 Galway players has a mean score of 3·74. Based on this, a local newspaper claims that Galway players have a different mean score to players in Ireland.'
A('8-b-i', 'Q8(b)(i)', '10C', [54], [20], '1-7', 'statistics-inferential-statistics', 'Use the information about this sample to construct a 95% confidence interval for the mean score of all Galway players. Use the standard deviation of 0·36 in your calculations.', stem=galway)
A('8-ii', 'Q8(b)(ii)', '5C', [55], [21], '1-7', 'statistics-inferential-statistics', 'Carry out a hypothesis test at the 5% level of significance to test the newspaper’s claim that Galway players have a different mean score to players in Ireland. State your null hypothesis, state your alternative hypothesis, state your conclusion, and give a reason for your conclusion.', stem=galway + ' Players in Ireland have a mean score of 3·87 with a standard deviation of 0·36.')
A('8-c', 'Q8(c)', '10D', [56], [21], '1-7', 'statistics-inferential-statistics', 'A national newspaper conducts a survey on a random sample of n teenagers in Ireland. 35% of the sample said they play the online word game every day. Based on this, a 95% confidence interval for the percentage, p, of all teenagers in Ireland who play the game every day was calculated, as accurately as possible. Correct to one decimal place, this interval was: 26·5% ≤ p ≤ 43·5%. Use this to work out the value of n, the number of teenagers surveyed.', stem=game)
tree = game + ' A player wins the game if they guess the word with 6 guesses or less. The organisers of the game record the following statistics for players in Europe: 80% of players win the game each day; 90% of players who win the game will play it again the following day; 25% of players who do not win the game will play it again the following day. Some of this information is shown in the tree diagram below, based on the 360 000 people who played the game on 1st June. The squares represent proportions. The rectangles labelled PLAY, WIN, and LOSE represent the number of people who play, win, and lose the game, respectively. For example, 0·8 of the 360 000 people who played the game on 1st June won the game. Assume that, for people who play the game on a number of days, winning the game on one day is independent of winning it on another day.'
A('8-d-i', 'Q8(d)(i)', '10D', [57], [22, 23], '1-2', 'probability', 'Complete the tree diagram, by writing the proportion associated with each branch of the tree diagram into the appropriate square and writing the number of people who play, win, and lose the game into the appropriate rectangle.', stem=tree)
A('8-d-ii', 'Q8(d)(ii)', '5C', [58], [22, 23], '1-2', 'probability', 'One person is picked at random from those who played the game on all three days (1st, 2nd, and 3rd June). Find the probability that this person lost on 1st June or 2nd June (or on both).', stem=tree)
ava = 'Ava is looking at different tilings, that is, different ways of covering a region with shapes.'
tiles = ava + ' First, she looks at two different tilings: one using identical squares and another using identical regular hexagons. (Note: a regular hexagon can be split into 6 congruent equilateral triangles.) A square tile and a hexagonal tile each have an area of 140 cm².'
A('9-a-i', 'Q9(a)(i)', '5B', [59], [24], '3-4', 'area-volume', 'Work out the length of the side of the square tile, correct to 1 decimal place.', stem=tiles)
A('9-a-ii', 'Q9(a)(ii)', '10C', [60], [24], '2-3', 'trigonometry-triangles,area-volume', 'The hexagonal tile has sides of length x cm, where x ∈ ℝ. Work out the value of x, correct to 1 decimal place.', stem=tiles)
arrow = ava + ' Next, Ava looks at more complicated tilings. The tiling below is made up of two shapes: an arrowhead (ABED) and a quadrilateral (EBCD). The point E lies on the line AC, and both shapes are symmetrical about AC (diagrams not to scale).'
A('9-b-i', 'Q9(b)(i)', '10C', [61], [25], '2-3', 'trigonometry-triangles', '|AD| = 8 cm, |AE| = 6 cm, and |ED| = 4 cm. As shown in the diagram, α = ∠DAE. Show that α = cos⁻¹(7/8).', stem=arrow)
A('9-b-ii', 'Q9(b)(ii)', '10D', [61], [25], '2-3', 'trigonometry-triangles,area-volume', 'In the diagram |∠ADC| = |∠ABC| = 90°. Use this, and part (b)(i), to work out the total area of the quadrilateral ABCD, correct to 2 decimal places.', stem=arrow + ' |AD| = 8 cm and α = ∠DAE = cos⁻¹(7/8).')
unit = ava + ' Ava also looks at a tiling of the inside of the unit circle c: x² + y² = 1. The diagram on the right (not to scale) shows the circle c and another circle, s. The points P and Q are on both circles. The part of s that lies inside c is an edge of a number of tiles. Ava wants to find the equation of the circle s.'
A('9-c-i', 'Q9(c)(i)', '5B', [62], [26], '2-3', 'trigonometry-functions-identities,co-ordinate-geometry-of-the-circle', '|∠QOP| = 45°, where O is the point (0, 0). Show that the point Q has co-ordinates (−1/√2, 1/√2).', stem=unit)
A('9-c-ii', 'Q9(c)(ii)', '10C', [63], [26, 27], '2-2', 'co-ordinate-geometry-of-the-circle', 'The point P lies on the x-axis. The centre of the circle s lies on the tangent to c at the point P and on the tangent to c at the point Q. Find the centre and the radius of the circle s. Give your answers in surd form.', stem=unit + ' |∠QOP| = 45° and Q is the point (−1/√2, 1/√2).')
basin = 'Séamus has a basin in the shape of an inverted right circular cone with the lower part removed, as shown in the diagram on the right below (diagrams not to scale). The radius of the original cone is 15 cm, and |CE|, the slant height of the basin, is 10 cm. The base of the basin is a horizontal circle with a radius of 12 cm, as shown. The basin is open – it does not have a top.'
A('10-a-i', 'Q10(a)(i)', '10C', [64], [28], '2-4', 'geometry,area-volume', 'Show that |BE| = 40 cm.', stem=basin)
A('10-a-ii', 'Q10(a)(ii)', '15D', [64], [28], '3-4', 'area-volume', 'Find the total internal surface area of the basin, correct to 1 decimal place.', stem=basin + ' |BE| = 40 cm.')
A('10-a-iii', 'Q10(a)(iii)', '5D', [65], [28, 29], '3-4', 'area-volume', 'Draw a diagram of the net of the curved surface of the basin. Show your working out. Include on your diagram enough measurements of lengths and/or angles so that the net could be constructed using a ruler, straight edge, compass, and protractor, without any further calculation. Your diagram may need to include lines that are not part of the net itself, like the broken lines in the diagram on the previous page.', stem=basin + ' |BE| = 40 cm.')
pin = 'Séamus needs to pick a new PIN code. It must be a 4-digit code. It must use exactly 4 of the digits from 1 to 9, so no digit can be used more than once.'
A('10-b-i', 'Q10(b)(i)', '5B', [66], [30], '1-1', 'probability', 'Work out how many such codes are possible.', stem=pin)
A('10-b-ii', 'Q10(b)(ii)', '5C', [66], [30], '1-1', 'probability', 'Work out how many of these codes contain the digit 2.', stem=pin)
A('10-b-iii', 'Q10(b)(iii)', '10C', [66], [30], '1-1', 'probability', 'Work out how many of the codes in part (b)(i) have the sum of their first three digits equal to their fourth digit. (The codes can contain the digit 2, although they do not have to.)', stem=pin)

P = Path('paper-trail-corpus/exampapers/2023/LC003ALP200EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2023/LC003ALP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 41
review = dict(schemaVersion=1, subjectId='mathematics', year=2023, level='higher', lang='ev', paperKey='p2',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 35–68 of the combined Higher Level scheme (Paper 2 title page, the Paper 2 scale table on page 36, the summary of allocations on page 37, annotation palette, every Paper 2 model solution and marking note, and the closing pages). Each task boundary is the published scale, cross-checked against the printed summary.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(35, 69)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[36, 37],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '41 independently marked units, matching the printed summary of allocations on scheme page 37. Shared scales keep their parts together: Q5(a)(i)–(iii) 20D and Q7(c)–(d) 10D.',
        'Paper 2 bands from scheme page 36: 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,4,7,10; 10D 0,3,5,8,10; 15D 0,4,8,12,15; 20D 0,6,12,17,20 (the Paper 2 20D differs from Paper 1’s 0,5,10,15,20).',
        'Before this review the deck held 36 of the 41 units and shipped 35. Added: Q2(b), Q8(b)(i), Q8(d)(i), Q8(d)(ii) and Q9(c)(i). Q1(b), refused by the provenance gate over garbled fraction text, now ships with quoted credit notes. Re-cited with the same IDs: “Q4(ii)” is Q4(a)(ii); “Q8(ii)”, which showed the Q8(a) prompt, is the 5C hypothesis test Q8(b)(ii). Q8(a) and Q9(a)(i) had shipped model-solution lines (Q8(a) also carried the Q8(b)(i) solution) plus the scheme page header as marking points; their rows are replaced with the published credit notes. Prompts are restored from the paper and topics corrected as metadata.',
        'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. All page references are PDF positions.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [13], 'wording': 'One of the values is filled in for you', 'classification': 'given-context',
         'reason': 'One table entry is supplied; the candidate completes the rest under one scale.'},
        {'pages': [15], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
         'reason': 'Alternative methods for the same marked task; no printed pool of prompts.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'or otherwise' in t:
        d = ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    elif 'One of the values' in t:
        d = ('given-context', 'One of the four table values is supplied; the candidate completes the others under one scale.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2023-higher-p2.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2023 Higher Level Paper 2 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'The original scheme reader provides the full solution, including graphical answers and all credit notes.'
def pts(cid, quotes):
    return [dict(id=f'{cid}-solution-{i+1}', kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(quotes)]
rows = {
    'maths-2023-hl-p2-q1-b': ['= 0·0779 [4 d.p.]', 'Consider the solution as being the product of four terms:', 'Product of two correct terms evaluated', 'Product of three correct terms', 'for the last day'],
    'maths-2023-hl-p2-q2-b': ['Work of merit, for example 30 + 45, or some correct substitution into relevant formula', 'sin 30 cos 45 + cos 30 sin 45 or equivalent'],
    'maths-2023-hl-p2-q8-a': ['= 0 · 1515', 'Find z -score', 'Find solution', 'Work of merit, for example, some correct substitution into relevant formula, relevant diagram drawn, indicates μ or σ', 'Correct z-score or', 'Finds z-score and further work, for example, finds 0.8485 or indicates'],
    'maths-2023-hl-p2-q8-b-i': ['C.I. : 3 · 6518 ≤ 𝜇≤3 · 8282', 'Note: If √64 is omitted, award Low Partial Credit at most', 'Confidence interval fully substituted', 'One side of interval only caculated'],
    'maths-2023-hl-p2-q8-ii': ['We reject null hypothesis.', 'Galway players do take a different average number of attempts.', '3 · 87 is NOT within the confidence interval', 'Note: If H0 and H1 are reversed, treat as one error', 'Two parts correct'],
    'maths-2023-hl-p2-q8-d-i': ['19 entries to check', 'At least one correct entry', 'Eight correct entries', '14 correct entries', 'One incorrect entry'],
    'maths-2023-hl-p2-q8-d-ii': ['Finds the total number of players who played on all three days', 'Finds the number of players who lost', 'Finds probability', '2 steps correct'],
    'maths-2023-hl-p2-q9-a-i': ['l = 11.8 cm [1 d.p.]', 'Incorrect rounding, or no rounding', 'No unit or incorrect unit'],
    'maths-2023-hl-p2-q9-c-i': ['Note: Check drawing for relevant work of merit', 'Work of merit in finding x or y ordinate', 'But x in 2nd quadrant.'],
}
refs = {'maths-2023-hl-p2-q4-ii': '2023 HL Paper 2 Q4(a)(ii)', 'maths-2023-hl-p2-q8-ii': '2023 HL Paper 2 Q8(b)(ii)'}
ADDED = ['maths-2023-hl-p2-q2-b', 'maths-2023-hl-p2-q8-b-i', 'maths-2023-hl-p2-q8-d-i', 'maths-2023-hl-p2-q8-d-ii', 'maths-2023-hl-p2-q9-c-i']
added, rebuilt = [], []
def _add(built):
    """Append a card this paper adds; on a re-run, rebuild it and require the committed card to match."""
    if 'stem' in built and not built['stem']: built.pop('stem')
    cur = byid.get(built['id'])
    if cur is None:
        added.append(built['id']); authored.append(built)
    elif cur != built:
        raise SystemExit(f"{built['id']}: committed card differs from the rebuilt one")
    else:
        rebuilt.append(built['id'])
for c in cards:
    a = byid.get(c['id'])
    if a is None or c['id'] in ADDED:
        concept = c['id'].split('-2023-')[1].split('-', 1)[1]
        _add(dict(id=c['id'], topicId=c['topicId'], conceptId=concept, level='higher', year=2023, subjectId='maths',
            section='A' if int(re.match(r'Q(\d+)', c['printedParts'][0])[1]) <= 6 else 'B',
            questionRef='2023 HL Paper 2 ' + ', '.join(c['printedParts']), stem=c.get('stem'), questionText=c['questionText'],
            tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'], rows=pts(c['id'], rows[c['id']]), notes=note))
        continue
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] in refs: a['questionRef'] = refs[c['id']]
    if c['id'] in rows:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = pts(c['id'], rows[c['id']])
assert sorted(added + rebuilt) == sorted(ADDED), (added, rebuilt)
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards), 'added', added)
