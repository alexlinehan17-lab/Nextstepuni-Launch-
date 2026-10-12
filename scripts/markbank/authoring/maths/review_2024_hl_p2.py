"""2024 HL Paper 2: review ledger, restored prompts, boundary fixes, add Q7(a)(ii)."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5],
      '10C': [0, 4, 6, 10], '10D': [0, 3, 5, 7, 10], '15C': [0, 6, 8, 15], '15D': [0, 4, 6, 8, 15], '20D': [0, 8, 11, 13, 20]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None, extra=None):
    c = dict(id='maths-2024-hl-p2-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-higher-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    if extra: c.update(extra)
    cards.append(c)

swim = 'A group of 22 students was tested to see how far, in metres, each of them could swim without stopping for a rest. The results of the testing are shown in the ordered stem and leaf plot below. Four of the entries have been replaced with the letters a, b, c, and d. Stem 2: b, 2, 7; stem 3: a, 4, 4, 5, 8; stem 4: 0, 1, d, 5, 6, 9; stem 5: 2, 3, 7, 7, 8; stem 6: 1, 8, c. Key: 2|7 = 27 metres.'
A('1-a-i', 'Q1(a)(i),Q1(a)(ii),Q1(a)(iii)', '15D', [32], [4], '1-6', 'statistics-descriptive-statistics', '(i) The mode of the data is 34 metres. Use this to write down the value of a. (ii) The range of the data is 49 metres. Use this to find the value of b and the value of c. (iii) The median of the data is 43·5 metres. Use this to find the value of d.', stem=swim)
A('1-b', 'Q1(b),Q1(c)', '15C', [32], [5], '1-6', 'statistics-descriptive-statistics', '(b) How would you best describe how the results changed for these students, from the initial test to the re-test? (c) The swimming coach worked out r, the correlation coefficient between the distance in the initial test and the distance in the re-test, for these seven students. Find the value of r, correct to 4 decimal places.',
  stem='Seven of the 22 students took swimming lessons. They were re-tested after the lessons, to see how far they could now swim without stopping. The table and graph below show the results of the initial test and of the re-test for these students. The initial-test distances are 22, 34, 38, 45, 49, 57 and 61 m; the matching re-test distances are 25, 40, 65, 96, 142, 262 and 350 m.')
A('2-a', 'Q2(a)', '10C', [33], [6], '1-2', 'probability', 'The table below shows the prizes, in euro, that a player can win in a game, as well as the probability of winning each prize. The player wins at most one prize each time that she plays. Some of the prizes are given in terms of x ∈ ℝ. The table gives the prizes None, 2, x − 10 and x with probabilities 30%, 40%, 28% and 2%. It costs €10 to play the game once. The game is fair – that is, the expected value of the winnings, taking the cost into account, is €0. Work out the value of x.')
A('2-b', 'Q2(b)', '5B', [33], [6], '1-2', 'probability', 'A and B are mutually exclusive events. P(A) = 0·1 and P(B) = 0·4. Write down the value of each of the following: P(A ∩ B) and P(A ∪ B).')
A('2-c', 'Q2(c)', '10C', [33], [7], '1-2', 'probability', 'C and D are two other events, with universal set U. P(C) = 0·5 and P(D) = 0·7. Find the maximum value of P[(C ∪ D)′]. Note: (C ∪ D)′ is the complement of the set C ∪ D in the set U.')
A('2-d', 'Q2(d)', '5A', [33], [7], '1-2', 'probability', 'E is the event that it will be raining tomorrow morning. F is the event that I will wear a coat going outside tomorrow morning. Explain why it would not be reasonable to assume that E and F are independent events.')
A('3-a', 'Q3(a)', '15C', [34], [8], '2-3', 'trigonometry-triangles,area-volume', 'ABCD is a parallelogram. |AB| = 10 cm, |BC| = 13 cm, and |∠ABC| = 110°. Find the area of ABCD, correct to the nearest cm².')
A('3-b', 'Q3(b)', '5D', [34], [8], '2-3', 'trigonometry-functions-identities', 'X is an angle, with 0° ≤ X ≤ 360°, and cos(2X) = √3/2. Find all the possible values of X.')
A('3-c', 'Q3(c)', '10D', [34], [9], '2-3', 'trigonometry-triangles', 'KLM is a triangle where |MK| = 15√3 cm, |ML| = 45 cm, and |∠KLM| = 25°. θ is the angle ∠LKM. Work out the two possible values of θ, for 0° < θ < 180°. Give each answer correct to the nearest degree.')
A('4-a', 'Q4(a)', '15D', [35], [10], '2-1', 'geometry-constructions-proofs', 'Construct the centroid of the triangle PQR below. Show all your construction lines clearly. Where measurement is used, show all relevant measurements and calculations clearly.', extra={'measurementRequired': True})
A('4-b', 'Q4(b)', '15D', [35], [11], '2-1', 'geometry-constructions-proofs', 'The lines AD, BE, and CF in the diagram below are parallel. E ∈ DF and B ∈ AC. |AB| = |BC|. Prove that |DE| = |EF|. (That is, prove that if three parallel lines cut off equal segments on some transversal line, then they will cut off equal segments on any other transversal.) Give a reason for each statement that you make in your proof, as appropriate.')
s5 = 'The circle s has equation: x² + y² + 4x − 6y + 5 = 0'
A('5-a-i', 'Q5(a)(i)', '10D', [36], [12], '2-2', 'co-ordinate-geometry-of-the-circle', 'Write down the centre and radius of the circle s.', stem=s5)
A('5-a-ii', 'Q5(a)(ii)', '10D', [36], [12], '2-2', 'co-ordinate-geometry-of-the-circle', 'The circle c has equation: (x − 2)² + (y + 1)² = 72. Show that the circles s and c touch internally.', stem=s5)
A('5-b', 'Q5(b)', '10D', [37], [13], '2-2', 'co-ordinate-geometry-of-the-circle', 'Another circle has its centre on the vertical line through the point (9, 0). The points (7, 10) and (12, 8) are on this circle. Find the equation of this circle. Note that your answer may contain non-integer values.')
A('6-a', 'Q6(a)', '5D', [38], [14], '2-2', 'co-ordinate-geometry-of-the-line', '[AB] is a line segment. The point C (6, 11) divides the line segment [AB] internally in the ratio 1 : 3. A is the point (1, 13). Find the co-ordinates of the point B.')
A('6-b', 'Q6(b)', '10C', [38], [14], '2-2', 'co-ordinate-geometry-of-the-line', 'Find the perpendicular distance from the point (5, −2) to the line: y = (4/3)x − 11')
A('6-c-i', 'Q6(c)(i),Q6(c)(ii)', '15D', [39], [15], '1-1', 'probability,co-ordinate-geometry-of-the-line', '(i) How many different pairs of points can be picked from these 16 points? (ii) The two points that are picked are joined with a straight line. Find the probability that this line is horizontal.',
  stem='In the co-ordinate diagram below, 16 points are marked with a dot (●). These are all of the points of the form (m, n), where m, n ∈ ℕ and m, n ≤ 4. A pair of these points is picked at random.')
pk = 'PK Hotels is a hotel chain in Europe.'
ages = pk + ' The ages of the people who stayed in a PK Hotel in 2023 are roughly normally distributed, with a mean age of 48·2 years and a standard deviation of 10·6 years.'
A('7-a-i', 'Q7(a)(i)', '5C', [40], [16], '1-3', 'statistics-z-scores', 'One person is picked at random from the people who stayed in a PK Hotel in 2023. Find the probability that this person is less than 50 years old.', stem=ages)
A('7-a-ii', 'Q7(a)(ii)', '10C', [40], [16], '1-3', 'statistics-z-scores', 'Exactly 10% of people who stayed in a PK Hotel in 2023 are at least A years old. Find the value of A, correct to the nearest whole number.', stem=ages)
pool = pk + ' During their most recent stay, 1/5 of PK Hotel customers used the pool. Use this to answer parts (b)(i) and (b)(ii).'
A('7-b-i', 'Q7(b)(i)', '5C', [40], [16], '1-3', 'probability', '6 of the PK Hotel customers are picked at random. Find the probability that exactly 2 of them used the pool.', stem=pool)
A('7-b-ii', 'Q7(b)(ii)', '5C', [41], [16, 17], '1-3', 'probability,indices-and-logs', 'n of the PK Hotel customers are picked at random, where n ∈ ℕ. The probability that none of them used the pool, correct to 4 decimal places, is 0·0047. Work out the value of n.', stem=pool)
A('7-c', 'Q7(c)', '15D', [41], [17], '1-2', 'probability', 'PK Hotels are testing a new booking system. 45% of people who log on to the PK Hotels website are shown the old booking system; the other 55% are shown the new booking system. People are assigned the booking system (old or new) at random. One third of people who see the old booking system end up booking a room. Two fifths of people who see the new booking system end up booking a room. One person is selected at random from those who booked a room through the PK Hotels website. Find the probability that this person used the new booking system. Give your answer as a percentage, correct to the nearest percent.', stem=pk)
A('7-d', 'Q7(d)', '10D', [42], [18], '1-7', 'statistics-inferential-statistics', 'In 2020, PK Hotels were rated the best hotel chain in Europe by 75% of their customers. In 2024, PK Hotels carried out a survey of a random sample of 1000 of their customers to see if this percentage had changed. Of these, 765 rated PK Hotels the best hotel chain in Europe. Carry out a hypothesis test at the 5% level of significance to see if this shows a change in the percentage of their customers who rate PK Hotels the best chain in Europe. State your null hypothesis and your alternative hypothesis, state your conclusion, and give a reason for your conclusion.', stem=pk)
tommy = 'Tommy makes ornaments from metal and glass.'
A('8-a', 'Q8(a)', '5C', [43], [19], '3-4', 'area-volume', 'He makes an open metal cylinder with a height of 15 cm and a radius of 5 cm. The net of this cylinder is a rectangle. Find the dimensions of this rectangle. Give your answers in cm, correct to 1 decimal place where appropriate.', stem=tommy)
A('8-b', 'Q8(b)', '5D', [43], [19], '3-4', 'area-volume', 'Tommy makes another cylinder with a height of 22 cm and a diameter of 12 cm. This cylinder fits exactly inside a glass sphere. The top and bottom edges of the cylinder touch the sphere. Find the volume of the sphere, in cm³, correct to 1 decimal place. Use the Theorem of Pythagoras in your solution.', stem=tommy)
cones = tommy + ' Another ornament is made of two cones inscribed in a sphere. The top cone is upright; the bottom cone is inverted. The cones have the same base. A vertical cross-section of the ornament, taken through the centre of the sphere, shows the cones as two triangles, ABC and ADB, with a common side [AB]. ABC is the top cone. The points A, B, C, and D all lie on the circle s, which represents the cross-section of the sphere. The lines AB and CD intersect at the point E.'
A('8-c-i', 'Q8(c)(i),Q8(c)(ii)', '20D', [44], [20], '2-1', 'geometry,geometry-constructions-proofs', '(i) The diagram is symmetrical about the line DC. State why |∠CBD| = 90°. (ii) Hence, or otherwise, prove that the triangles BCE and DBE are similar. Give a reason for each statement that you make, where appropriate.', stem=cones)
A('8-c-iii', 'Q8(c)(iii)', '10C', [44], [20, 21], '2-1', 'geometry', 'The top cone has a radius of r and a height of h; that is, |EB| = r and |EC| = h. The sphere, represented by s, has a radius of 10 cm. Use the similar triangles BCE and DBE to show that: r² = 20h − h²', stem=cones)
A('8-c-iv', 'Q8(c)(iv)', '10C', [44, 45], [20, 21], '5-2', 'differentiation-applications,area-volume', 'Hence, write the volume of the top cone in terms of h and π, and find the value of h that gives the maximum volume for the top cone.', stem=cones + ' The top cone has a radius of r and a height of h; that is, |EB| = r and |EC| = h. The sphere, represented by s, has a radius of 10 cm. Part (c)(iii) shows that r² = 20h − h².')
race = 'Ameena, Petro, and Fiadh are taking part in an adventure race. The co-ordinate diagram below shows part of the course for this race. Each unit on the diagram represents 100 metres.'
stream = race + ' The arc in the diagram represents part of a stream. The arc is part of a circle s with centre C(1, 17) and radius 12.'
A('9-a-i', 'Q9(a)(i)', '5B', [46], [22], '2-2', 'co-ordinate-geometry-of-the-circle', 'Write down the equation of the circle s.', stem=stream)
A('9-a-ii', 'Q9(a)(ii)', '5C', [46], [22, 23], '2-2', 'co-ordinate-geometry-of-the-circle', 'Ameena is at the point (a, 8) on the stream (circle s), where a ∈ ℝ, a > 0. Work out the value of a. Give your answer in surd form.', stem=stream)
A('9-a-iii', 'Q9(a)(iii)', '10C', [46], [22, 23], '2-2', 'co-ordinate-geometry-of-the-circle', 'Petro is at the point P(10, 6). Work out the shortest distance from the point P to the stream (circle s). Give your answer correct to the nearest metre. Remember that each unit on the diagram represents 100 metres.', stem=stream)
A('9-b', 'Q9(b)', '5B', [46], [24], '2-2', 'co-ordinate-geometry-of-the-circle', 'There is a straight path, l, that is not shown on the diagram. l is parallel to the y-axis, and is a tangent to the stream s in the first quadrant. Write down the equation of this path l. Remember that the radius of s is 12.', stem=stream)
road = race + ' The line segment w represents a road, where w has the equation: x − 3y = 9 for 0 ≤ y ≤ 8.'
A('9-c', 'Q9(c)', '10D', [47], [24], '2-2', 'co-ordinate-geometry-of-the-line', 'Find the co-ordinates of the point on the road w that is closest to the point P(10, 6). It might be useful to find the equation of the line through P that is perpendicular to w.', stem=road)
A('9-d', 'Q9(d)', '15D', [48], [24, 25], '2-2', 'co-ordinate-geometry-of-the-line,trigonometry-triangles', 'Fiadh is at the point F(9, 0) on the road w. She travels 1200 m along the road w away from the point F, in the first quadrant, and then stops. Work out the co-ordinates of the point at which she stops. Give each value correct to 1 decimal place. Remember that each unit on the diagram represents 100 metres.', stem=road)
wiper = 'A company makes windscreen wipers. In this question, the rectangle PQRS has a width of 180 cm and a height of 100 cm. M is the midpoint of [PQ], N is the midpoint of [SR], and O ∈ NM. All lengths are given in cm.'
blade = wiper + ' In the diagram below, the line segment [AB] shows a type of wiper blade. [AB] rotates around the point O, where O ∈ AB, until it reaches the position [A′B′]. The region that it cleans is ABB′A′, which is the sector OBB′ with the sector OAA′ removed. A, A′, B, and B′ lie on the rectangle PQRS, and N lies on the arc from B to B′. The line segment [RQ] is extended 20 cm to T, as shown. ∠OTR is a right angle.'
A('10-a-i', 'Q10(a)(i)', '5B', [49], [26], '2-1', 'geometry', 'Show that |OB| = 120 cm.', stem=blade)
A('10-a-ii', 'Q10(a)(ii)', '10C', [49], [26, 27], '2-3', 'trigonometry-triangles', 'Hence, show that |∠BOT| = 41·4°, correct to 1 decimal place.', stem=blade)
A('10-a-iii', 'Q10(a)(iii)', '10D', [49], [26, 27], '3-4', 'area-volume,trigonometry-triangles', 'Hence, work out the area of ABB′A′. Remember that ABB′A′ is the sector OBB′ with the sector OAA′ removed. Give your answer correct to the nearest cm².', stem=blade)
A('10-b', 'Q10(b)', '10D', [50], [28], '2-3', 'trigonometry-triangles', 'Moving the point O along the line NM changes the size of the wiper blade and the region that it cleans. In the diagram below, [DE] rotates about O, where O ∈ DE, until it reaches [D′E′]. As in part (a), E and E′ lie on the rectangle PQRS. Here, |∠E′OE| = 105°. By setting |OE| = x, use the triangle OEE′ and the Cosine Rule to find the value of |OE|. Give your answer in cm, correct to 1 decimal place.', stem=wiper)
lights = 'Mattie is driving home. On the way, she passes five traffic lights. Each traffic light is either red (R), green (G), or orange (O) when she arrives at it. One day, she notes the pattern made by the colour of each traffic light when she arrives at it. For example, this pattern could be R R O G R.'
A('10-c-i', 'Q10(c)(i)', '5B', [50], [29], '1-1', 'probability', 'How many different patterns could the five traffic lights make?', stem=lights)
A('10-c-ii', 'Q10(c)(ii),Q10(c)(iii)', '10D', [51], [29], '1-1', 'probability', '(ii) How many different patterns could the five traffic lights make, if the first light is red and the fifth light is not red? (iii) How many different patterns could the five traffic lights make if no two consecutive lights are the same colour?', stem=lights)

P = Path('paper-trail-corpus/exampapers/2024/LC003ALP200EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2024/LC003ALP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 40
review = dict(schemaVersion=1, subjectId='mathematics', year=2024, level='higher', lang='ev', paperKey='p2',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 29–56 of the combined Higher Level scheme (Paper 2 title page, the Paper 2 scale table on page 30, annotation palette, every Paper 2 model solution and marking note, and the blank closing pages). Each task boundary is the published scale, not a parser count.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(29, 57)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[30, 31],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '40 independently marked units. Shared scales keep their parts together: Q1(a)(i)–(iii) 15D, Q1(b)–(c) 15C across two letters, Q6(c)(i)–(ii) 15D, Q8(c)(i)–(ii) 20D and Q10(c)(ii)–(iii) 10D.',
        'Paper 2 bands from scheme page 30: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10C 0,4,6,10; 10D 0,3,5,7,10; 15C 0,6,8,15; 15D 0,4,6,8,15; 20D 0,8,11,13,20. Q7(a)(ii) prints “Scale (0, 4, 6, 10)” without a letter; its ladder is the 10C ladder.',
        'Before this review the deck held 39 cards for this paper. The Q7(a) card claimed both (i) and (ii) at 5 marks and its rows mixed the (ii) model solution into (i); it is re-cited as Q7(a)(i) with credit notes from its own 5C scale, and Q7(a)(ii) (10C) is added. The Q1(b) card is re-cited as Q1(b), (c): both letters share one 15C scale, and its question crop showed only part (b) without the seven-student table, so the card now shows the lifted prompt for both letters with the original page. Q2(d) and Q10(c)(i) carried scheme page furniture (“Mathematics – Higher Level”) as a marking point; those rows are replaced with the printed answer and notes. All 39 existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
        'Q4(a) is a construction that permits measurement, so it carries the calibrated measuring ruler.',
        'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. All page references are PDF positions.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [20], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
         'reason': 'Alternative proof methods for the same marked task; no printed pool of prompts.'},
        {'pages': [29], 'wording': 'either red (R), green (G), or orange (O)', 'classification': 'counting-context',
         'reason': 'The three colours are the outcomes being counted, not a choice of tasks.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'or otherwise' in t:
        d = ('method-choice', 'Alternative proof methods for the same marked task, with no printed pool of prompts.')
    elif 'either red' in t:
        d = ('counting-context', 'Each light shows one of three colours; these are the outcomes counted in required tasks, not a choice of prompts.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2024-higher-p2.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2024 Higher Level Paper 2 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'The original scheme reader provides the full solution, including graphical answers and all credit notes.'
def pts(cid, quotes):
    return [dict(id=f'{cid}-solution-{i+1}', kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(quotes)]
replace_rows = {
    'maths-2024-hl-p2-q7-a-i': ['P(z < 0·17) = 0·5675', '56·75%', 'Work of merit, for example, some correct substitution into relevant formula, relevant diagram drawn, indicates μ or σ', 'Finds z-score'],
    'maths-2024-hl-p2-q2-d': ['If it is raining I am more likely to wear a coat than if it isn’t'],
    'maths-2024-hl-p2-q10-c-i': ['3⁵ = 243', 'Accept correct answer without work', 'Work of merit, for example, lists some correct patterns'],
}
new_refs = {'maths-2024-hl-p2-q7-a-i': '2024 HL Paper 2 Q7(a)(i)', 'maths-2024-hl-p2-q1-b': '2024 HL Paper 2 Q1(b), (c)'}
ADDED = ['maths-2024-hl-p2-q7-a-ii']
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
        assert c['id'] == 'maths-2024-hl-p2-q7-a-ii'
        _add(dict(id=c['id'], topicId=c['topicId'], conceptId='p2-q7-a-ii', level='higher', year=2024, subjectId='maths',
            section='B', questionRef='2024 HL Paper 2 Q7(a)(ii)', stem=c['stem'], questionText=c['questionText'],
            tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'],
            rows=pts(c['id'], ['A = 62 [nearest whole number]', 'Oldest 10% ∴ 90% less than ‘A’ years old', 'Finds z-value', 'Writes equation in A', 'Finds value of A',
                               'Work of merit, for example, mentions 90%, or finds z-value of 10%', 'Apply a * for incorrect or no rounding']),
            notes=note))
        continue
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] in new_refs: a['questionRef'] = new_refs[c['id']]
    if c['id'] in replace_rows:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = pts(c['id'], replace_rows[c['id']])
    if c['id'] == 'maths-2024-hl-p2-q1-b':
        a.pop('questionFigureKey', None)
assert sorted(added + rebuilt) == sorted(ADDED), (added, rebuilt)
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards))
