"""2023 OL Paper 2: review ledger, restored prompts, restore Q7(c), re-quote garbled rows, move welded deductions."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
from rows_2023_ol_p2 import ROWS
import fitz

SC = {'5B': [0, 3, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 4, 6, 10], '10D': [0, 4, 6, 8, 10],
      '15C': [0, 5, 10, 15], '15D': [0, 5, 8, 12, 15]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None, extra=None):
    c = dict(id='maths-2023-ol-p2-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-ordinary-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    if extra: c.update(extra)
    cards.append(c)

line = 'co-ordinate-geometry-of-the-line'; circ = 'co-ordinate-geometry-the-circle'
ab = 'A(4, 2) and B(1, 8) are two points in the co-ordinate plane.'
A('1-a-i', 'Q1(a)(i)', '10C', [31], [4], '2-2', line, 'Work out the slope of the line AB.', stem=ab)
A('1-a-ii', 'Q1(a)(ii)', '10C', [31], [4], '2-2', line, 'Work out the distance |AB|.', stem=ab)
A('1-b', 'Q1(b)', '5C', [32], [4], '2-2', line, 'Find the equation of the line through the point (−2, 7) with a slope of 1/3. Give your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.')
A('1-c-i', 'Q1(c)(i),Q1(c)(ii)', '5D', [33], [5], '2-2', line, '(i) Draw the line segment through the point (4, 2) with a slope of 2 on the co-ordinate diagram below, with the range −2 ≤ y ≤ 6, y ∈ ℝ. (ii) Draw the line segment through the point (4, 2) with a slope of −2/3 on the co-ordinate diagram below, on the domain −1 ≤ x ≤ 7, x ∈ ℝ.', stem='The point (4, 2) is shown in each of the two co-ordinate diagrams below.')
s = 's is the circle x² + y² = 25.'
A('2-a-i', 'Q2(a)(i),Q2(a)(ii)', '10D', [34], [6], '2-2', circ, '(i) Write down the centre and radius of the circle s. (ii) Show that the point (3, −4) is on the circle s.', stem=s)
A('2-a-iii', 'Q2(a)(iii)', '5C', [34], [6], '2-2', circ, 'Write down the co-ordinates of two other points that are also on the circle s.', stem=s)
A('2-b', 'Q2(b)', '15D', [35], [7], '2-2', circ + ',' + line, 'Find the points of intersection between a different circle, k, and the line l, where: l : 5x − y − 13 = 0; k : x² + y² = 13.')
A('3-a-i', 'Q3(a)(i)', '5C', [36], [8], '1-1', 'counting', 'In how many ways can the letters in the word CAMOGIE be arranged?')
A('3-a-ii', 'Q3(a)(ii)', '10C', [36], [8], '1-1', 'counting', 'How many of the arrangements in part (a)(i) start with M and end with a vowel (A, O, I, or E)?', stem='Part (a)(i) asks: In how many ways can the letters in the word CAMOGIE be arranged?')
A('3-a-iii', 'Q3(a)(iii)', '5B', [36], [8], '1-1', 'counting', 'How many arrangements of 3 different letters can be made from the letters in the word CAMOGIE?')
A('3-b-i', 'Q3(b)(i),Q3(b)(ii)', '10D', [37], [9], '1-6', 'statistics', '(i) Write each of the letters A, B, and C in the correct place in the table below to show which scatterplot corresponds to each correlation coefficient. Use each letter only once. (ii) For scatterplot B, explain why the value you picked is correct.', stem='Three scatterplots are shown below. They are labelled A, B, and C. Each scatterplot has the same axes and scales. The correlation coefficient for each scatterplot was calculated. The results were 0·95, 0·6, and −0·95.')
fr = 'Rohan plays basketball. During a match, Rohan takes a number of free throws. He scores 70% of his free throws, on average. Assume that scoring his free throws are independent events.'
A('4-a-i', 'Q4(a)(i)', '5C', [38], [10], '1-2', 'probability', 'Find the probability that he scores his first 3 free throws.', stem=fr)
A('4-a-ii', 'Q4(a)(ii)', '10C', [38], [10], '1-2', 'probability', 'Find the probability that he scores exactly 2 of his first 3 free throws.', stem=fr)
A('4-a-iii', 'Q4(a)(iii)', '5B', [38], [10], '1-2', 'probability', 'Give one reason why scoring his free throws might not be independent events.', stem=fr)
A('4-b', 'Q4(b)', '10C', [39], [11], '1-6', 'statistics', 'The table below shows the number of games in which Rohan scored each of the given number of points. For example, Rohan scored 12 points in 3 games. Number of points: 0, 6, 8, 10, 12, 16; number of games: 4, 5, 4, 2, 3, 1. Work out Rohan’s mean number of points per game, based on the values in the table. Give your answer correct to 2 decimal places.', stem='Rohan plays basketball.')
sq = 'The diagram below (not to scale) shows a square with sides of length 12 cm. The circle c is inside the square, and touches the four sides of the square. The circle k is outside the square, and goes through the four corners of the square.'
A('5-a', 'Q5(a),Q5(b)', '10D', [40], [12], '3-4', 'area-volume', '(a) Find the length of the radius of the circle c. (b) Work out the area of the circle c. Give your answer correct to 2 decimal places.', stem=sq)
A('5-c', 'Q5(c)', '5C', [40], [13], '3-4', 'area-volume', 'Work out the percentage of the area of the square that is taken up by the circle c, correct to the nearest percent.', stem=sq)
A('5-d', 'Q5(d)', '5C', [41], [13], '2-3', 'trigonometry,geometry', 'Show that the radius of the circle k is 8·49 cm, correct to 2 decimal places.', stem=sq)
A('5-e', 'Q5(e)', '10C', [41], [13], '3-4', 'area-volume', 'Work out the circumference of the circle k, correct to 2 decimal places.', stem=sq)
A('6-a', 'Q6(a)', '15D', [42], [14], '2-1', 'geometry-proofs-and-constructions', 'The diagram below shows the parallelogram ABCD (not to scale). |AB| = 8 cm, |BC| = 6 cm, and |∠ABC| = 130°, as shown. Construct the parallelogram ABCD in the space below. The point A is given, as is part of the line AB.', extra={'measurementRequired': True})
A('6-b', 'Q6(b)', '5C', [42], [15], '2-1', 'geometry', 'The diagram below shows another parallelogram (not to scale). The sizes of three of the angles are given, where x, y ∈ ℝ: 100°, (2x − 30)° and (x + 3y)°. Use the information in the diagram to work out the value of x and the value of y.')
A('6-c', 'Q6(c)', '10C', [43], [15], '2-1', 'geometry', 'State whether the following statement is true or false. Justify your answer. Statement: “Every square is a parallelogram.” True or false? (Tick one box only)')
olga = 'Olga is a cyclist. She is measuring how long and how steep different roads are.'
road = olga + ' The diagram below shows a road [AB]. AC is horizontal and BC is vertical. The diagram is not to scale. The gradient of the road [AB] is |BC|/|AC| written as a percentage. It is a measure of how steep the road is. In parts (a)(i) to (a)(iv), there are four different values for |AB| and |AC|, and four different gradients.'
A('7-a-i', 'Q7(a)(i)', '10C', [44], [16], '2-3', 'trigonometry', 'Find the gradient of the road [AB] when |BC| = 24 m and |AC| = 135 m. Give your answer correct to the nearest percent.', stem=road)
A('7-a-ii', 'Q7(a)(ii)', '10C', [44], [16], '2-3', 'trigonometry', 'Find |AC| when |BC| = 16 m and the gradient of the road [AB] is 12%. Give your answer correct to the nearest metre.', stem=road)
A('7-a-iii', 'Q7(a)(iii)', '10C', [45], [16, 17], '2-3', 'trigonometry', 'Use the Theorem of Pythagoras to find |AC| when |BC| = 27 m and |AB| = 105 m. Give your answer correct to the nearest whole number.', stem=road)
A('7-a-iv', 'Q7(a)(iv)', '10C', [45], [16, 17], '2-3', 'trigonometry', 'Find the size of the angle ∠BAC when the gradient of the road [AB] is 9%. Give your answer correct to the nearest degree.', stem=road)
A('7-b', 'Q7(b)', '5C', [46], [18], '2-3', 'trigonometry', 'Olga wants to measure the distance between two points, R and O. She marks a point P on the ground, so that the distance from R to P is 20 m. She measures the angles ∠OPR and ∠ORP. All of these are shown in the diagram below (not to scale): |RP| = 20 m, |∠ORP| = 88° and |∠OPR| = 87°. Work out the distance |OR|. Give your answer correct to the nearest metre.', stem=olga)
A('7-c', 'Q7(c)', '5C', [46], [19], '2-3', 'trigonometry', 'Olga has already worked out the distances between three points, labelled X, Y, and Z in the diagram on the right (not to scale): |XZ| = 700 m, |ZY| = 550 m and |XY| = 800 m. Work out the size of the angle at X in the triangle XYZ. Give your answer in degrees, correct to 1 decimal place.', stem=olga)
pool = 'A family decides to buy a small paddling pool for their back garden. The pool is in the shape of a cylinder. It has an internal diameter of 2·4 m and an internal depth of 0·9 m.'
seats = pool + ' The family buys 3 pool seats. Each pool seat is a cube, with sides of length 0·5 m.'
cover = pool + ' The family also buys a cover for the pool, to help keep the water clean. It is in the shape of a right circular cone, with a radius of 1·3 m and a vertical height of 0·8 m.'
A('8-a', 'Q8(a)', '10C', [47], [20], '3-4', 'area-volume', 'The instruction manual recommends that the pool should be filled to a maximum depth of 0·75 m. Work out the volume of water in the pool when it is filled to this maximum depth. Give your answer in m³, correct to 2 decimal places.', stem=pool)
A('8-b-i', 'Q8(b)(i)', '10C', [47], [21], '3-4', 'area-volume', 'Show that the total volume of the 3 pool seats is 0·375 m³.', stem=seats)
A('8-b-ii', 'Q8(b)(ii)', '10C', [47], [21], '3-4', 'area-volume', 'The pool is filled with water to a height of 0·6 m. The 3 pool seats are put into the pool, so that each seat is fully covered in water. Find the amount by which the water level in the pool rises. Give your answer in metres, correct to 2 decimal places.', stem=seats)
A('8-c-i', 'Q8(c)(i)', '5C', [48], [22], '3-4', 'area-volume,trigonometry', 'Show that the slant height of the cone, marked l in the diagram above, is 1·53 m, correct to 2 decimal places.', stem=cover)
A('8-c-ii', 'Q8(c)(ii)', '5C', [48], [22], '3-4', 'area-volume', 'Work out the curved surface area of the conical cover. Give your answer correct to 2 decimal places.', stem=cover)
A('8-c-iii', 'Q8(c)(iii)', '10D', [49], [23], '3-4', 'area-volume', 'The diagram below shows the net of the conical cover (not to scale). It is a sector of a circle of radius x. Write down the value of x and work out the size of the angle A, correct to the nearest degree.', stem=cover)
read = 'A group of students decided to investigate the average amount of time that students in Ireland spend reading each day. One Monday morning, they asked the first 200 students who came into their school how long, on average, they spend reading each day. Their results are shown in the table below. Minutes spent reading per day: 0 − 30, 30 − 60, 60 − 90, 90 − 120, 120 − 150, 150 − 180; number of students: 16, 35, 62, 59, 18, 10. Note: 30 − 60 means “30 minutes or more, but less than 60 minutes”, and so on.'
A('9-a-i', 'Q9(a)(i),Q9(a)(iii)', '10C', [50], [24], '1-5', 'statistics', '(i) Work out the maximum number of students in this sample who, on average, could have read for more than 100 minutes per day. (iii) Explain why the method of choosing the students for this survey could limit the validity of the conclusions.', stem=read)
A('9-a-ii', 'Q9(a)(ii)', '5C', [50], [24], '1-6', 'statistics', 'Estimate the median time spent reading by these 200 students, as accurately as possible. Justify your answer.', stem=read)
A('9-a-iv', 'Q9(a)(iv)', '15C', [51], [24, 25], '1-6', 'statistics', 'Draw a graph or chart to represent the data in the table. Show clearly any relevant calculations. Label your graph or chart clearly.', stem=read)
cork = 'A random sample of 500 students in Cork took a statistics test. 61 of these students were given a rating of Excellent.'
A('9-b-i', 'Q9(b)(i)', '10C', [51], [26], '3-3', 'statistics', 'Work out the percentage of students in this sample who were given a rating of Excellent.', stem=cork)
A('9-b-ii', 'Q9(b)(ii)', '5C', [52], [26], '1-7', 'statistics', 'Show that the margin of error for this sample is 4·5%, correct to 1 decimal place.', stem=cork)
A('9-b-iii', 'Q9(b)(iii)', '5D', [52], [26], '1-7', 'statistics', 'In general, 10% of students get a rating of Excellent on this statistics test. Use your answers to parts (b)(i) and (b)(ii) to test the claim that the percentage of students in Cork who would get a rating of Excellent is different to the population percentage, at the 5% level of significance. Show relevant calculations, state your conclusion, and give a reason for your conclusion.', stem=cork)
pent = 'A toy company makes spinners in the shape of a regular pentagon, as shown in the diagram on the right (not to scale). Each of the five sides of the pentagon ABCDE is the same length. The pentagon is divided into five congruent isosceles triangles. Each triangle contains the point O. |∠BOC| = 72° and |AO| = 6 cm.'
A('10-a', 'Q10(a)', '10C', [53], [27], '2-1', 'geometry', 'Work out |∠CBA|, the size of the angle CBA.', stem=pent)
A('10-b', 'Q10(b)', '10C', [53], [27], '2-3', 'trigonometry,area-volume', 'Work out the area of the triangle AOB, and hence work out the area of the pentagon ABCDE. Give each answer correct to 1 decimal place. (You do not need to use your answer from part (a).)', stem=pent)
spin = 'The triangles in the spinner are numbered 1 to 5, as shown. The spinner is spun twice, and each number landed on is recorded.'
spin2 = spin + ' The spinner is spun twice, and the two numbers are added.'
A('10-c-i', 'Q10(c)(i)', '10C', [54], [28], '1-3', 'probability', 'Write down a sample space to show all of the 25 possible outcomes when the spinner is spun twice. It may be useful to draw a two-way table or to list the outcomes in a systematic way.', stem=spin)
A('10-c-ii', 'Q10(c)(ii)', '5C', [54], [28], '1-3', 'probability', 'What are the maximum and minimum possible totals when two numbers from the spinner are added?', stem=spin2)
A('10-c-iii', 'Q10(c)(iii)', '5C', [55], [29], '1-2', 'probability', 'Each time the spinner is spun, each number (1 to 5) is equally likely. Work out the probability of getting a total of either 4 or 5, when the two numbers are added.', stem=spin2)
A('10-d', 'Q10(d)', '10C', [55], [29], '1-3', 'probability', 'In a different spinner, there are 4 different outcomes: N, S, E, or W. In a game, Jena pays €1 to spin this spinner. The table below shows the probability of each outcome, as well as the money Jena will get, depending on the outcome. N: probability 0·3, Jena gets €1; S: 0·2, €0·50; E: 0·4, €0; W: 0·1, €5. Is this game fair? Justify your answer. Work out the expected value of this game as part of your solution.')

P = Path('paper-trail-corpus/exampapers/2023/LC003GLP200EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2023/LC003GLP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 46
assert set(ROWS) <= {c['id'] for c in cards}
review = dict(schemaVersion=1, subjectId='mathematics', year=2023, level='ordinary', lang='ev', paperKey='p2',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 27–60 of the combined Ordinary Level scheme (Paper 2 title page, the Paper 2 scale table on page 28, the slips note and printed summary of allocations on page 29, annotation palette, every Paper 2 model solution and marking note, and the blank closing pages). Each task boundary is the published scale, cross-checked against the printed summary.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(27, 61)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[28, 29],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '46 independently marked units, matching the printed summary of allocations on scheme page 29. Q9(a)(i) and (iii) share one 10C scale although they are not adjacent; one card carries both prompts.',
        'Paper 2 bands from scheme page 28: 5B 0,3,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10C 0,4,6,10; 10D 0,4,6,8,10; 15C 0,5,10,15; 15D 0,5,8,12,15. They differ from the Paper 1 bands at 15C (Paper 1 prints 0,6,10,15).',
        'All 46 units were already authored. Q7(c) (cosine rule, angle at X) was refused by the provenance gate because its last credit band carried the calculator-mode values welded onto it; it now ships with quoted notes. Fifteen cards had their marking points re-quoted from the printed scheme because the text layer had interleaved the solution and notes columns (Q1(c), Q2(b), Q3(b), Q5(a)–(b), Q5(c), Q5(d), Q6(a), Q6(b), Q7(a)(iv)), welded the radian/gradian values onto a band (Q7(b), Q7(c), Q10(b)), mixed a Zero Credit note into a band (Q9(a)(ii)), garbled a stacked fraction (Q9(b)(ii)), or shipped the scheme page header as a marking point (Q9(b)(iii)). On the remaining cards, a “Full Credit (−1)” deduction or “Zero Credit” note welded onto a credit band is moved to the row note, because neither is a band. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
        'Q6(a) is constructed at the printed scale from the given point A and part of [AB], so the page measurement tool is attached. Q1(c) is drawn on printed co-ordinate grids and needs no measurement.',
        'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [24], 'wording': 'the method of choosing the students for this survey', 'classification': 'given-context',
         'reason': 'Describes how the survey sample was chosen; it is the subject of the required Q9(a)(iii) explanation, not a choice of prompts.'},
        {'pages': [29], 'wording': 'a total of either 4 or 5', 'classification': 'mathematical-context',
         'reason': 'Defines the event whose probability is required; there is one prompt.'},
        {'pages': [15], 'wording': 'Tick one box only', 'classification': 'answer-selection',
         'reason': 'True or false is the answer to Q6(c), followed by a required justification, not alternative prompts.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'method of choosing the students' in t:
        d = ('given-context', 'Describes how the survey sample was chosen; it is what Q9(a)(iii) asks the candidate to criticise, not a choice of prompts.')
    elif 'either 4 or 5' in t:
        d = ('mathematical-context', 'Defines the event “a total of 4 or 5” whose probability is required; there is a single prompt.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2023-ordinary-p2.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2023 Ordinary Level Paper 2 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'Each point is labelled with the part of the printed scheme it comes from. The original scheme reader provides the full solution, including diagrams, tables and graphs.'
MARK = re.compile(r'\s*(Full Credit ?\(-1\)|Zero Credit):?\s*')
moved = 0
for c in cards:
    a = byid[c['id']]
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] in ROWS:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = [dict(id=f"{c['id']}-solution-{i+1}", kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(ROWS[c['id']])]
        continue
    for r in a['rows']:
        g = r.get('group')
        if not g: continue
        notes, opts = [], []
        for o in g['options']:
            m = MARK.search(o)
            if m:
                rest = o[m.start():]
                parts = MARK.split(rest)  # ['', label, text, label, text, ...]
                for label, text in zip(parts[1::2], parts[2::2]):
                    text = text.replace('\n', '; ').strip(' ;')
                    kind = 'Full Credit −1 (a deduction, not a band)' if label.startswith('Full') else 'Zero Credit (not a band)'
                    notes.append(f'{kind}: {text}')
                o = o[:m.start()].rstrip()
            opts.append(o)
        if notes:
            assert all(opts), (c['id'], g['options'])
            g['options'] = opts
            r['verbatim'] = opts[0]
            r['contextNote'] = (r.get('contextNote', '').rstrip() + ' ' + '. '.join(notes) + '.').strip()
            moved += 1
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards), 'rows replaced', len(ROWS), 'notes moved', moved)
