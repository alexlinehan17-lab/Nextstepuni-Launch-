"""2024 OL Paper 2: review ledger, restored prompts, row repairs, Q2(c)-(d) re-citation."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 4, 10],
      '10C': [0, 4, 5, 10], '10D': [0, 3, 5, 7, 10], '15C': [0, 6, 9, 15], '15D': [0, 4, 6, 8, 15]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None, extra=None):
    c = dict(id='maths-2024-ol-p2-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-ordinary-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    if extra: c.update(extra)
    cards.append(c)

hist = 'The scores for 9 students in a history test are given in the table below. X is the lowest score and Y is the highest score, where X, Y ∈ ℕ. The scores are X, 91, 76, 82, 37, 42, 74, 54 and Y.'
A('1-a-i', 'Q1(a)(i),Q1(a)(ii)', '15D', [27], [4], '1-6', 'statistics', '(i) Write the scores in order, from the lowest to the highest in the spaces below. (ii) Find the median of these scores and explain what this score means in the context of the question.', stem=hist)
A('1-a-iii', 'Q1(a)(iii)', '5C', [27], [4, 5], '1-6', 'statistics', 'All students received different scores in the test. The range of the scores is 61. Work out the maximum possible value of X and the corresponding value of Y.', stem=hist)
A('1-b', 'Q1(b)', '10C', [27], [5], '1-6', 'statistics', 'A different group of five students did a maths question. Their scores were as follows, where t ∈ ℕ: 15, 16, 19, t, 26. The mean of the five scores is 19·6. Work out the value of t.')
cardsg = 'Seán is playing a game with 14 cards. 7 of the cards are green (G), numbered 1 to 7. The other 7 cards are red (R), also numbered 1 to 7.'
A('2-a', 'Q2(a)', '10C', [28], [6], '1-1', 'probability,counting', 'Complete the table below to show all possible outcomes when a card is chosen. Some have already been completed for you. For example, G2 means the green card with the number 2. The table already shows G2 and R5.', stem=cardsg)
A('2-b', 'Q2(b)', '5B', [28], [6], '1-2', 'probability', 'A card is chosen at random. Work out the probability of getting a card with an even number.', stem=cardsg)
A('2-c', 'Q2(c),Q2(d)', '15D', [28], [6, 7], '1-2', 'probability', '(c) Seán picks a card at random and doesn’t replace it. It is Red 5 (R5). He then picks a second card at random. What is the probability that the second card is a green card? Seán puts back the two cards. (d) Seán picks a card at random and doesn’t replace it. He then picks a second card at random. Find the probability that the second card is a different colour and a different number from the first card.', stem=cardsg)
A('3-a-i', 'Q3(a)(i),Q3(a)(ii)', '15D', [29], [8], '2-2', 'co-ordinate-geometry-of-the-line', '(i) Show that the point (4, 1) lies on l. (ii) Draw the line l on the co-ordinate diagram below, in the domain −4 ≤ x ≤ 5, x ∈ ℝ.', stem='A line, l, has the equation: y = (1/2)x − 1')
A('3-b', 'Q3(b)', '10C', [29], [9], '2-2', 'co-ordinate-geometry-of-the-line', 'Four lines are drawn on the co-ordinate diagram below, labelled a, b, c and d. Their slopes are given in the table below: 3, −1, 1/2 and 0. Write a, b, c and d in the correct place in the table to match each line to its slope.')
A('3-c', 'Q3(c)', '5D', [30], [9], '2-2', 'co-ordinate-geometry-of-the-line', 'Find the equation of the line through the points (0, 6) and (2, 9).')
k = 'The circle k has equation: (x − 5)² + (y + 3)² = 25'
A('4-a-i', 'Q4(a)(i)', '5C', [31], [10], '2-2', 'co-ordinate-geometry-the-circle', 'Write down the centre and radius of the circle k.', stem=k)
A('4-a-ii', 'Q4(a)(ii)', '5C', [31], [10], '2-2', 'co-ordinate-geometry-the-circle', 'Use algebra to investigate if the point (9, 2) is on, inside, or outside the circle k. Tick one box only: (9, 2) is on k; (9, 2) is inside k; (9, 2) is outside k.', stem=k)
A('4-b', 'Q4(b)', '10C', [31], [10], '2-2', 'co-ordinate-geometry-the-circle', 'A different circle has centre (4, −1) and radius 3. Construct this circle on the co-ordinate diagram below.')
A('4-c', 'Q4(c)', '10C', [32], [11], '2-2', 'co-ordinate-geometry-the-circle', 'The point (2, 1) is the lowest point on the circle s with centre c, as shown in the diagram below. The y-axis is a tangent to the circle s. Work out the radius and the centre of the circle s.')
sleep = 'A large group of 17-year-olds were asked how many hours of sleep they got on the previous night. The results were normally distributed. The middle 68% slept between 7·2 and 8·4 hours, as shown on the diagram below. Use the empirical rule to answer parts (a)(i) and (a)(ii).'
A('5-a-i', 'Q5(a)(i)', '5C', [33], [12], '1-3', 'statistics', 'Fill in the three missing numbers on the horizontal axis.', stem=sleep)
A('5-a-ii', 'Q5(a)(ii)', '10C', [33], [12], '1-3', 'statistics', 'Research says that a 17-year-old should get at least 9 hours of sleep each night. What percentage of this sample got at least 9 hours of sleep on the previous night?', stem=sleep)
A('5-b-i', 'Q5(b)(i),Q5(b)(ii)', '15D', [34], [13], '1-2', 'probability', '(i) What is the probability that he does not get the recommended amount of sleep on a particular night? (ii) Beginning on a Sunday night, Owen records his sleep each night for a week. Find the probability that Owen gets the recommended amount of sleep for the first time on Tuesday night (the third night). Assume that the number of hours of sleep Owen gets on different nights are independent.', stem='Owen records the number of hours of sleep that he gets each night for several weeks. Based on this, he calculates that he gets the recommended amount of sleep 10% of the time.')
A('6-a-i', 'Q6(a)(i),Q6(a)(ii)', '15C', [35], [14], '2-1', 'geometry-proofs-and-constructions', '(i) Construct the bisector of the angle XYZ, using only a compass and straight edge. Show all your construction lines and arcs clearly. (ii) Hence, construct the incentre of the triangle XYZ below.', stem='The diagram below shows the triangle XYZ.')
enl = 'The diagram below shows the triangles ABC and ADE (not to scale). The triangle ADE is the image of the triangle ABC under enlargement. Some of the lengths are shown in the diagram: |AC| = 6, |BC| = 4 and |DE| = 14.'
A('6-b-i', 'Q6(b)(i),Q6(b)(ii)', '10D', [35], [15], '2-4', 'geometry', '(i) Use |BC| and |DE| to show the scale factor is 3·5. (ii) |AC| = 6 units. Use the scale factor to find the distance from C to E, that is, find |CE|.', stem=enl)
A('6-b-iii', 'Q6(b)(iii)', '5B', [35], [15], '2-4', 'geometry,area-volume', 'The area of the triangle ABC is 11 units². Find the area of the triangle ADE.', stem=enl + ' The scale factor is 3·5.')
heart = 'A company was interested in investigating the fitness of its employees. The table below shows the heart rates of ten employees measured before and after exercise. Their heart rates are measured in beats per minute (bpm). Employees A to J: before exercise 60, 76, 68, 89, 67, 65, 77, 83, 88, 70; after exercise 71, 81, 79, 108, 91, 83, 102, 113, 118, 87.'
A('7-a-i', 'Q7(a)(i)', '10C', [36], [16], '1-6', 'statistics', 'Complete the back-to-back stem-and-leaf plot below to show this information. Two values are already filled in (0 | 6 = 60 bpm before exercise and 7 | 1 = 71 bpm after exercise).', stem=heart)
A('7-a-ii', 'Q7(a)(ii)', '10C', [36], [16, 17], '1-6', 'statistics', 'Work out the mean and standard deviation of the heart rate after exercise. Give each answer correct to 1 decimal place.', stem=heart)
A('7-a-iii', 'Q7(a)(iii)', '5B', [36], [16, 17], '1-6', 'statistics', 'Based on your stem-and-leaf plot, how has the standard deviation changed following exercise? Give a reason for your answer. Tick one box only: Increased; Decreased; Stayed the same.', stem=heart)
A('7-a-iv', 'Q7(a)(iv)', '5B', [36], [16, 18], '1-7', 'statistics', 'A scatter plot of the data is shown in the diagram below. r is the correlation coefficient between the heart rate before exercise and the heart rate after exercise. Based on the diagram above, pick the value from the list below that is closest to r. Give a reason for your answer. Tick one box only: −0·8, −0·2, 0·3 or 0·9.', stem=heart)
park = 'A random sample of 355 people was picked from everyone who took part in a park run in 2023 in Galway.'
A('7-b-i', 'Q7(b)(i)', '5C', [37], [19], '1-7', 'statistics', 'Show that, for this sample, the margin of error for a population proportion is 5·3%, correct to 1 decimal place.', stem=park)
A('7-b-ii', 'Q7(b)(ii)', '5C', [37], [19], '3-3', 'statistics', '96 of the 355 runners finished the run in under 25 minutes. Work out the percentage of runners in this sample who finished the park run in under 25 minutes. Give your answer correct to the nearest percent.', stem=park)
A('7-b-iii', 'Q7(b)(iii)', '10D', [38], [19], '1-7', 'statistics', 'A running club commentator said that Galway park run times have changed since 2019. In 2019 it was reported that 24% of all runners finished the park run in under 25 minutes. Use your answers to parts (b)(i) and (b)(ii) to test the claim that the percentage of runners who finish the park run in under 25 minutes has changed since 2019, at the 5% level of significance. Show relevant calculations, state your conclusion, and give a reason for your conclusion.', stem=park + ' The margin of error is 5·3%, and 96 of the 355 runners (27%) finished in under 25 minutes.')
sign = 'A fish shop has a vertical sign outside its front door. In the diagram below, the sign is represented by [FH], with |FH| = 3 m. A cable is tied at the top of the sign, F, and is secured at the point G on the horizontal ground. G is 1·4 m from the base of the sign H, as shown in the diagram below (not to scale).'
A('8-a-i', 'Q8(a)(i)', '10C', [39], [20], '2-3', 'trigonometry', 'Use the Theorem of Pythagoras to find the length of the cable, |GF|. Give your answer in metres, correct to 1 decimal place.', stem=sign)
A('8-a-ii', 'Q8(a)(ii)', '5C', [39], [20], '2-3', 'trigonometry', 'Show that the size of the angle ∠FGH = 65°, correct to the nearest degree.', stem=sign)
A('8-a-iii', 'Q8(a)(iii)', '5C', [39], [20, 21], '2-3', 'trigonometry', 'A second cable from G is tied to the sign, at the point K, where K is half way up the sign [FH]. Mairéad says that the size of the new angle ∠KGH is half the size of the angle ∠FGH. Is Mairéad correct? Use calculations to support your answer. Tick one box only: Yes or No.', stem=sign)
logo = 'The fish shop has a logo with some measurements as shown in the diagram below (not to scale).'
A('8-b-i', 'Q8(b)(i)', '10C', [40], [22], '2-3', 'trigonometry', '|AB| = 12 cm, |AC| = 10 cm, and |∠ABC| = 37°. Work out the size of the angle θ, where θ is the angle ∠BCA. Give your answer correct to the nearest degree.', stem=logo)
A('8-b-ii', 'Q8(b)(ii)', '10C', [40], [22, 23], '2-3', 'trigonometry', '|CF| = 22 cm, |EF| = 11·8 cm, and |∠EFC| = 110°. Use the cosine rule to work out the distance |CE|. Give your answer correct to 1 decimal place.', stem=logo)
A('8-b-iii', 'Q8(b)(iii)', '10C', [40], [22, 23], '2-3', 'trigonometry,area-volume', 'CDEF is symmetrical about [CE]. Work out the total area of CDEF. Give your answer correct to the nearest cm².', stem=logo + ' |CF| = 22 cm, |EF| = 11·8 cm, and |∠EFC| = 110°.')
van = 'Diarmuid owns an ice cream van.'
A('9-a-i', 'Q9(a)(i),Q9(a)(ii)', '10D', [41], [24], '1-1', 'counting', '(i) How many different choices are available if you must choose only one flavour, one topping, and either a cone or a tub? (ii) Diarmuid wants to maximise the number of choices available to his customers. He can only add either an extra flavour or an extra topping. Should he add an extra flavour or an extra topping? Use calculations to support your answer. Tick one box only: Extra flavour or Extra topping.', stem=van + ' Diarmuid sells: 7 different flavours of ice cream; 4 different toppings; 2 containers: a choice of a cone or a tub.')
venn = van + ' One day, Diarmuid recorded the ice cream choices of the first 100 customers. Vanilla (V) flavour was bought by 42 customers. A cone (C) was bought by 37 customers. 45 customers bought neither vanilla nor a cone. This information is shown in the Venn diagram below.'
A('9-b-i', 'Q9(b)(i)', '10B', [41], [25], '1-2', 'probability', 'Complete the Venn diagram below, to show the number of customers in each region.', stem=venn)
A('9-b-ii', 'Q9(b)(ii)', '5B', [41], [25], '1-2', 'probability', 'A customer is picked at random from the first 100 customers. Find the probability that this customer bought a cone with a flavour other than vanilla.', stem=venn)
A('9-c', 'Q9(c)', '10C', [42], [26], '1-2', 'probability', 'In general, sales of ice creams increase as weather conditions improve. Diarmuid’s typical ice cream sales for different weather conditions are shown in the table below. The table also shows the probability of each weather condition next Sunday: Wet €150 (30%); Dry and cold €200 (45%); Dry and warm €450 (25%). Use the information in the table to work out the expected value of Diarmuid’s ice cream sales next Sunday.', stem=van)
cone = van + ' Diarmuid has a logo of an ice cream cone on the side of his van. The logo is made up of a sector of a circle with radius 20 cm, and two identical right-angled triangles, as shown in the diagram (not to scale). The arc of the sector is labelled s. The sizes of some of the angles are shown: two angles of 70° at the centre.'
A('9-d-i', 'Q9(d)(i)', '10C', [42], [27], '3-4', 'area-volume,trigonometry', 'Find the size of the angle θ and hence, find the length of the arc s. Give the length in cm, correct to 1 decimal place.', stem=cone)
A('9-d-ii', 'Q9(d)(ii)', '5C', [42], [27], '2-3', 'trigonometry', 'Use trigonometry to work out the length of the side labelled l. Give your answer correct to the nearest cm.', stem=cone)
A('10-a-i', 'Q10(a)(i),Q10(a)(ii),Q10(a)(iii)', '10D', [43], [28], '3-3', 'number-systems', '(i) Use the conversion rate of 1 mile = 1·61 km to convert 121 miles to km. (ii) Convert one hour to seconds. (iii) Use your answers to parts (a)(i) and (a)(ii) to convert 121 miles per hour to metres per second. Give your answer correct to 2 decimal places.', stem='In Wimbledon Tennis Tournament 2023, the fastest women’s serve was by Aryna Sabalenka at 121 miles per hour. (Source www.wimbledon.org)')
A('10-b', 'Q10(b)', '5C', [43], [29], '3-4', 'area-volume', 'Tennis balls are in the shape of a sphere. For professional tennis matches, tennis balls can be of slightly different sizes. The smallest size allowed has a radius of 3·27 cm. Find the surface area of this tennis ball. Give your answer in cm², correct to 2 decimal places.')
A('10-c', 'Q10(c)', '10D', [44], [29], '3-4', 'area-volume', 'The cross-section of a tennis ball is shown in the diagram on the right. The ball is made up of an air-filled centre and a rubber layer of uniform thickness. The external radius (r₁) of the tennis ball is 3·4 cm. The internal radius (r₂) of the rubber layer is 3·1 cm. Find the volume of the rubber layer. Give your answer in cm³, correct to 2 decimal places.')
tube = 'The diagram on the right shows the smallest closed cylindrical container that contains three identical tennis balls, arranged one directly on top of the other. The radius of each tennis ball is 3·4 cm. The height of the cylinder is h.'
A('10-d-i', 'Q10(d)(i),Q10(d)(ii)', '10D', [45], [30], '3-4', 'area-volume', '(i) Show that h = 20·4 cm. (ii) Hence, calculate the volume of the cylinder. Give your answer correct to nearest whole number.', stem=tube)
A('10-d-iii', 'Q10(d)(iii)', '15C', [45], [30], '3-4', 'area-volume', 'The three tennis balls could also be arranged, one directly on top of the other, inside a closed rectangular box, as shown below. Find the surface area of the smallest such rectangular box, in cm².', stem=tube)

P = Path('paper-trail-corpus/exampapers/2024/LC003GLP200EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2024/LC003GLP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 43
review = dict(schemaVersion=1, subjectId='mathematics', year=2024, level='ordinary', lang='ev', paperKey='p2',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 23–48 of the combined Ordinary Level scheme (Paper 2 title page, the Paper 2 scale table on page 24, the slips note and printed summary of allocations on page 25, annotation palette, every Paper 2 model solution and marking note, and the closing pages). Each task boundary is the published scale, cross-checked against the printed summary.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(23, 49)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[24, 25],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '43 independently marked units, matching the printed summary of allocations on scheme page 25.',
        'Paper 2 bands from scheme page 24: 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,4,10; 10C 0,4,5,10; 10D 0,3,5,7,10; 15C 0,6,9,15; 15D 0,4,6,8,15. They differ from the Paper 1 bands (for example 10C is 0,4,6,10 on Paper 1).',
        'All 43 units were already in the deck. Corrections, all keeping IDs: Q2(c) shares one 15D scale with Q2(d), so its card is re-cited as Q2(c), (d) and carries both prompts. Q5(a)(ii) had lost its high-partial band; Q8(a)(ii) carried a text-layer artefact (“TTTTTT AA”); Q7(b)(iii) carried its boundary inequalities out of order; their marking points are re-quoted from the printed scheme. Where a “Full Credit (−1)” deduction had been welded onto the last credit band, it is moved to the note, because it is a deduction and not a band. Prompts are restored from the paper and topics corrected as metadata.',
        'Q6(a) is a compass-and-straight-edge construction (no measurement); no ruler is attached.',
        'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [24], 'wording': 'choose only one flavour, one topping, and either a cone or a tub / either an extra flavour or an extra topping', 'classification': 'counting-context',
         'reason': 'The menu choices are the objects counted (7 × 4 × 2); the extra flavour/topping box is the answer to one required comparison.'},
        {'pages': [10, 17, 18, 21], 'wording': 'Tick one box only', 'classification': 'answer-selection',
         'reason': 'On/inside/outside, increased/decreased, the closest r and Yes/No are answers with justification, not alternative prompts.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'flavour' in t or 'topping' in t or 'cone or a tub' in t:
        d = ('counting-context', 'The menu choices are the outcomes counted, or the extra-item box is the answer to one required comparison; not a choice of prompts.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2024-ordinary-p2.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2024 Ordinary Level Paper 2 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'The original scheme reader provides the full solution, including graphical answers and all credit notes.'
replace_rows = {
    'maths-2024-ol-p2-q5-a-ii': ['100% − 97·5%', '= 2·5 [%]', 'Work of merit, for example, shades in correct area or μ + 2σ', '95%', 'Use of Z score would merit at most L.P.C.', '5% OR 97·5%'],
    'maths-2024-ol-p2-q8-a-ii': ['A = 65[°]', 'Work of merit', 'using trigonometry (25°)', 'Apply a * for no or incorrect rounding'],
    'maths-2024-ol-p2-q7-b-iii': ['21·7 ≤ p ≤ 32·3', 'No change to the population percentage', '24% is inside the range found. Within the CI.', 'Work of merit, for example, writes answer from (b)(i) or (b)(ii) in this part', 'Either conclusion OR reason missing OR incorrect'],
    'maths-2024-ol-p2-q2-c': ['= 7/13', '= 6/13', 'Relevant partial listing', 'Work of merit in (c) AND (d)', '(c) OR (d) correct', 'One part correct and work of merit in the other part'],
}
moved = 0
for c in cards:
    a = byid[c['id']]
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] == 'maths-2024-ol-p2-q2-c':
        a['questionRef'] = '2024 OL Paper 2 Q2(c), (d)'
    if c['id'] in replace_rows:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = [dict(id=f"{c['id']}-solution-{i+1}", kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(replace_rows[c['id']])]
        continue
    for r in a['rows']:
        g = r.get('group')
        if not g: continue
        deductions = []
        opts = []
        for o in g['options']:
            m = re.search(r'\s*Full Credit \(-1\):?\s*', o)
            if m:
                deductions.append(o[m.end():].replace('\n', '; ').strip(' ;'))
                o = o[:m.start()].rstrip()
            opts.append(o)
        if deductions:
            g['options'] = opts
            r['verbatim'] = opts[0]
            r['contextNote'] = (r.get('contextNote', '').rstrip() + ' Full Credit −1 (a deduction, not a band): ' + '; '.join(d for d in deductions if d) + '.').strip()
            moved += 1
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards), 'deductions moved', moved)
