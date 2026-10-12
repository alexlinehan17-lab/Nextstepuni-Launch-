"""2023 OL Paper 1: review ledger, restored prompts, add Q3(b), restore Q2(a)(iv), repair Q8(e)/(f)."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5B': [0, 3, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 7, 10], '10C': [0, 4, 6, 10], '10D': [0, 4, 6, 8, 10],
      '15C': [0, 6, 10, 15], '20D': [0, 7, 10, 15, 20]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None):
    c = dict(id='maths-2023-ol-p1-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-ordinary-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    cards.append(c)

houses = 'The prices of houses in a particular area have been increasing over a number of years.'
A('1-a', 'Q1(a)', '10C', [7], [4], '3-3', 'financial-maths', 'A house is valued at €240 000 at the start of 2019. By the start of 2020, the price of the house has increased by 8%. By the start of 2021, the price of the house has increased by a further 9%, based on the 2020 price. Work out the price of the house at the start of 2020, and the price at the start of 2021.', stem=houses)
A('1-b', 'Q1(b)', '10C', [7], [4], '3-3', 'financial-maths', 'Another house was valued at €460 000. One year later, the value of this house had gone up to €472 000. Work out the percentage increase in the value of this house over the year. Give your answer correct to 1 decimal place.', stem=houses)
A('1-c', 'Q1(c)', '10C', [8], [5], '3-3', 'financial-maths', 'A third house was valued at €265 000. Over the following 4 years, the value of the house increased by r% each year compared to the previous year, where r ∈ ℝ. After 4 years, the house was valued at €370 000. Work out the value of r, by setting F = 370 000, P = 265 000, and t = 4 in this equation: F = P(1 + r/100)^t. Give your answer correct to 1 decimal place.', stem=houses)
i2 = 'In this question, i² = −1.'
z = i2 + ' The complex number z₁ is shown on the Argand diagram below. z₂ and z₃ are two other complex numbers. z₂ = 5 + i and z₃ = 6 − 2i.'
A('2-a-i', 'Q2(a)(i),Q2(a)(ii)', '10D', [9], [6], '3-1', 'complex-numbers', '(i) Plot and label z̅₁, the complex conjugate of z₁, on the diagram above. (ii) Plot and label z₂ and z₃ on the diagram above.', stem=z)
A('2-a-iii', 'Q2(a)(iii)', '10C', [9], [6], '3-1', 'complex-numbers', 'Write 4z₂ − 5z₃ in the form a + bi, where a, b ∈ ℤ.', stem=z)
A('2-a-iv', 'Q2(a)(iv)', '5C', [10], [6, 7], '3-1', 'complex-numbers', 'Work out the value of |z₃|. Give your answer in surd form.', stem=z)
A('2-b', 'Q2(b)', '5B', [10], [7], '3-1', 'complex-numbers', 'The complex numbers z₄, z₅, z₆, and z₇ are shown on the Argand diagram below. The diagram is to scale. Tick one box to indicate which of z₄, z₅, z₆, or z₇ has the largest modulus. Give a reason for your answer.', stem=i2)
A('3-a', 'Q3(a)', '15C', [11], [8], '4-2', 'algebra-equations', 'Solve the following equation in x ∈ ℝ: 3(2x + 4) − 5 = 3')
A('3-b', 'Q3(b)(i),Q3(b)(ii),Q3(b)(iii)', '5D', [11], [8], '4-3', 'algebra', 'Graph each of the following inequalities on the given number line (−4 to 4). Note that x comes from a different set of numbers in each case. (i) x ≤ 2·8, where x ∈ ℝ. (ii) x ≤ 2·8, where x ∈ ℤ. (iii) x ≤ 2·8, where x ∈ ℕ.')
A('3-c', 'Q3(c)', '10D', [12], [9], '4-2', 'algebra-equations', 'Use algebra to solve the following simultaneous equations: x − y + 1 = 0; 2x + 4y = 19')
g = 'The graph of the function g is shown on the co-ordinate diagram below, for −3 ≤ x ≤ 2, x ∈ ℝ. Use the graph to answer parts (a)(i) to (a)(iv).'
A('4-a-i', 'Q4(a)(i),Q4(a)(ii),Q4(a)(iii)', '10D', [13], [10], '5-1', 'graphing-functions', '(i) Estimate the value of g(1·5). Show your work on the graph. (ii) Estimate the value of x for which g(x) = −6. Show your work on the graph. (iii) Tick one box to show how many real roots the function g(x) has in this domain (0, 1, 2 or 3). Give a reason for your answer.', stem=g)
A('4-a-iv', 'Q4(a)(iv)', '5B', [13], [10, 11], '5-1', 'graphing-functions', 'From the graph, estimate the co-ordinates of the local maximum point and the local minimum point of g(x), as accurately as possible.', stem=g)
h = 'A different function, h(x), has the following equation: h(x) = x³ + 2x² − x − 8'
A('4-b-i', 'Q4(b)(i)', '10C', [14], [11], '5-2', 'differentiation', 'Find h′(x), the derivative of h(x).', stem=h)
A('4-b-ii', 'Q4(b)(ii)', '5C', [14], [11], '5-2', 'differentiation,co-ordinate-geometry-of-the-line', 'Find the equation of the tangent to h(x) at the point (2, 6).', stem=h)
rail = 'A company is repairing a railway line. As part of this work, it is laying new railway tracks.'
A('5-a-i', 'Q5(a)(i)', '10B', [15], [12], '3-3', 'number-systems', 'It costs €12 000 to lay 240 metres of railway track. Work out how much would it cost to lay 320 metres of railway track, at the same rate.', stem=rail)
A('5-a-ii', 'Q5(a)(ii)', '5C', [15], [12], '3-3', 'number-systems', 'It would take 6 people 8 days to replace the tracks on a different part of the railway line. Work out how long it would take 4 people to replace these tracks, each working at the same speed.', stem=rail)
train = 'Two towns, A and B, are 120 km apart. A train travels from A to B at an average speed of 180 km/hour.'
A('5-b-i', 'Q5(b)(i)', '10B', [15], [13], '3-3', 'number-systems', 'Work out the time it takes the train to get from A to B. Give your answer in hours, as a fraction.', stem=train)
A('5-b-ii', 'Q5(b)(ii)', '5D', [16], [13], '3-3', 'number-systems', 'On the way back from B to A, the train travels at an average speed of 220 km/hour. Work out the average speed of the train for the entire journey, while it is travelling from A to B and back again. Give your answer in km/hour. Hint: first work out the total time taken for the entire journey.', stem=train)
gx = 'g(x) is the following function in x ∈ ℝ: g(x) = x² + 8x − 6'
A('6-a-i', 'Q6(a)(i)', '5B', [17], [14], '5-1', 'functions', 'Find the value of g(−5).', stem=gx)
A('6-a-ii', 'Q6(a)(ii)', '5B', [17], [14], '5-2', 'differentiation', 'Use calculus to find the value of x which gives the minimum value of g(x).', stem=gx)
A('6-b', 'Q6(b)', '10C', [17], [14], '4-1', 'algebra', 'Expand and simplify (2x − 4)² − 6.')
A('6-c', 'Q6(c)', '10C', [18], [15], '4-2', 'algebra-equations', 'Solve the following equation in x: 9x² + 6x − 5 = 0. Give each answer correct to 2 decimal places.')
runoff = 'When it rains on land, some of the rain soaks into the land, and the rest runs off the land. The runoff curve number, C, is a number used when estimating the amount of rain that runs off a particular area of land. C is given by: C = 1000/(S + 10), where S is a measure of the maximum amount of rain that can soak into the soil.'
A('7-a-i', 'Q7(a)(i)', '10B', [19], [16], '5-1', 'functions', 'Find the value of C when S = 15.', stem=runoff)
A('7-a-ii', 'Q7(a)(ii)', '5B', [19], [16], '5-1', 'functions', 'When S increases, does C increase or decrease? Justify your answer, using the equation C = 1000/(S + 10).', stem=runoff)
A('7-a-iii', 'Q7(a)(iii)', '5C', [19], [16, 17], '4-1', 'algebra', 'Rearrange the equation to write S in terms of C.', stem=runoff)
A('7-a-iv', 'Q7(a)(iv)', '10C', [20], [16, 17], '4-2', 'algebra-equations,functions', 'The values for C go from 30 to 100. Use your answer from part (a)(iii), or otherwise, to find the range of values of S.', stem=runoff)
rain = 'Over the course of one day (24 hours), the probability that it is raining in Waterville, P(t), could be modelled by the following function: P(t) = 0·3 + 0·02t. Here, P(t) is the probability that it is raining t hours after the start of the day, with 0 ≤ t ≤ 24, t ∈ ℝ.'
A('7-b-i', 'Q7(b)(i)', '10C', [20], [18], '5-1', 'functions,probability', 'Write down the probability that it is raining at the start and the end of the day, that is, find the value of P(0) and P(24).', stem=rain)
A('7-b-ii', 'Q7(b)(ii)', '5B', [20], [18], '5-2', 'differentiation', 'Find the value of P′(t), the derivative of t, and explain what the value of P′(t) means in this context.', stem=rain)
A('7-b-iii', 'Q7(b)(iii)', '5B', [20], [18], '5-1', 'functions,probability', 'At a certain time, the probability that it is raining, according to this model, is 0·35. Work out the probability that it is raining exactly 1 hour later, according to this model.', stem=rain)
garden = 'A rectangular garden (50 m by 30 m) contains an irregularly shaped pond of length 18 m, as shown in the diagram below (not to scale).'
A('8-a', 'Q8(a)', '10B', [21], [19], '3-4', 'area-volume', 'Find the area of the whole garden (that is, the total area of the rectangle).', stem=garden)
A('8-b', 'Q8(b)', '5C', [21], [19], '3-4', 'area-volume', 'The width of the pond is measured at intervals of 3 metres, starting at the right-hand edge of the pond. These measurements are given on the diagram, correct to the nearest metre (2, 8, 10, 12, 14, 10 m and 0 at the left-hand point). Use the Trapezoidal Rule (and the measurements in the diagram above) to work out an estimate for the area of the pond.', stem=garden)
A('8-c', 'Q8(c)', '5B', [21], [19, 20], '3-4', 'area-volume', 'Suggest a way by which the Trapezoidal Rule could be used (with different measurements) to get a potentially more accurate estimate of the area of the pond.', stem=garden)
A('8-d', 'Q8(d)', '10C', [21], [20], '3-4', 'area-volume,financial-maths', 'Apart from the pond, the rest of the rectangular garden is covered in grass. The actual area of the pond is 172 m². All of the grass in the garden needs to be resown. The cost is €2·55 per square metre that needs to be resown. Work out the cost of resowing the grass. Give your answer correct to the nearest ten euro.', stem=garden)
A('8-e', 'Q8(e)', '10C', [22], [21], '3-3', 'financial-maths', 'Some materials were imported from England by the gardener for resowing the grass. The cost of the materials was £840. This included an Import Duty of 16·9%. Work out the cost of the materials before the Import Duty was added. Give your answer correct to the nearest penny (that is, to 2 decimal places).')
A('8-f', 'Q8(f)', '10C', [22], [21], '3-3', 'financial-maths', 'The gardener paid the £840 in euro. The exchange rate was €1 = £0·8547. He also paid a fee of 2·5% of the £840 as a commission. Work out how much he paid in total, in euro, correct to the nearest cent.', stem='Some materials were imported from England by the gardener for resowing the grass. The cost of the materials was £840.')
cases = 'The diagram below shows the actual daily number of new cases of a disease, from day t = 0 to day t = 25. It also shows the number of cases according to a mathematical model over this period of time.'
A('9-a-i', 'Q9(a)(i)', '10B', [23], [22], '5-1', 'graphing-functions', 'From the diagram, estimate the number of actual new cases there were on day t = 12, using the relevant dot.', stem=cases)
A('9-a-ii', 'Q9(a)(ii)', '5B', [23], [22], '3-3', 'number-systems', 'According to the model (the curve), there were 1000 new cases on day t = 12. Work out the percentage error in the model’s value for day t = 12. Use your answer to part (a)(i) above as the actual value for day t = 12. Give your answer correct to the nearest percent.', stem=cases)
A('9-a-iii', 'Q9(a)(iii)', '5B', [23], [22, 23], '5-1', 'graphing-functions', 'Show that it takes approximately 5 days for the daily number of new cases to double, according to the model (that is, according to the curve in the diagram).', stem=cases)
A('9-a-iv', 'Q9(a)(iv)', '5C', [23], [22, 23], '4-1', 'sequences-series,graphing-functions', 'Hence, estimate on what day (value of t) the number of new cases will first be at least 100 000, according to the model. Show your working out.', stem=cases + ' The daily number of new cases doubles approximately every 5 days, according to the model.')
dt = 'The daily number of new cases of a different disease can be modelled using the function: D(t) = 2100 × 1·18^t, where D is the daily number of new cases and t is the time in days from t = 0 to t = 14.'
A('9-b-i', 'Q9(b)(i),Q9(b)(ii)', '20D', [24], [24], '5-1', 'graphing-functions,indices', '(i) Fill in the table below to show the values of D(t) for the given values of t. Give each value correct to the nearest whole number. The table gives D(2) = 2924 and D(6) = 5669 and leaves t = 0, 1, 3, 4 and 5 to complete. (ii) Draw the graph of y = D(t) on the axes below, for 0 ≤ t ≤ 6 and t ∈ ℝ.', stem=dt)
A('9-b-iii', 'Q9(b)(iii)', '5C', [24], [25], '3-2', 'indices', 'Measures are put in place to slow down the spread of the disease. From t = 14 days onwards, the number of new daily cases starts to decrease. For t ≥ 14, the daily number of new cases on day t can be modelled by: K(t) = a × 0·83^t. On t = 14 days, there are 21 309 cases, according to this model. Use this to work out the value of a. Give your answer in the form b × 10ⁿ, where 1 ≤ b < 10, n ∈ ℕ, and b is correct to 2 decimal places.', stem=dt)
A('10-a-i', 'Q10(a)(i)', '5B', [25], [26], '3-4', 'area-volume', 'Find the volume of a cylinder with a diameter of 18 mm and a height of 5 mm. Give your answer correct to the nearest mm³.')
A('10-a-ii', 'Q10(a)(ii)', '5C', [25], [26], '3-4', 'area-volume', 'A metal ring could be made by removing a cylinder of diameter 14 mm and height 5 mm from the cylinder in part (a)(i). Work out the volume of metal in this ring, correct to the nearest mm³.', stem='Part (a)(i) is a cylinder with a diameter of 18 mm and a height of 5 mm.')
gold = 'Many gold rings are made of a mixture of pure gold and other metals.'
A('10-b-i', 'Q10(b)(i),Q10(b)(ii)', '10D', [25], [26, 27], '3-3', 'number-systems', '(i) One particular ring weighs 8 grams. It contains 3 grams of pure gold. Work out the percentage of the weight of this ring that is pure gold. (ii) Pink gold is made up of pure gold, copper, and silver. The ratio of the weight of pure gold to copper to silver is 15 : 4 : 1, respectively. Work out the number of grams of pure gold in a pink gold ring that weighs 25 grams.', stem=gold)
A('10-b-iii', 'Q10(b)(iii)', '5C', [26], [27], '3-1', 'number-systems', 'Rose gold is made up of 75% pure gold, 22·25% copper, and 2·75% silver. Express the ratio of pure gold : copper : silver in rose gold in the ratio a : b : c, in its simplest form, where a, b, c ∈ ℕ.', stem=gold)
ins = 'The cost of insuring a piece of jewellery depends on its value. The table below shows the rates charged per year by one insurance company, where r ∈ ℝ, r > 0: first €1000 at 1% of the value; next €9000 at 2% of the excess over €1000, plus the cost of insuring the first €1000; amount in excess of €10 000 at r% of the excess over €10 000, plus the cost of insuring the first €10 000.'
A('10-c-i', 'Q10(c)(i)', '5C', [26], [28], '3-3', 'financial-maths', 'Work out the cost per year of insuring a ring valued at €1800.', stem=ins)
A('10-c-ii', 'Q10(c)(ii)', '10C', [26], [28], '3-3', 'financial-maths', 'The cost of insuring a particular necklace is €142·80 per year. Work out the value of this necklace.', stem=ins)
A('10-c-iii', 'Q10(c)(iii)', '10D', [26], [28, 29], '3-3', 'financial-maths', 'A brooch is valued at €17 500. The cost per year of insuring the brooch is €435. Work out r, the rate of the insurance charged on the amount of the value of the brooch which is in excess of €10 000. Give your answer as a percentage, correct to 1 decimal place.', stem=ins)

P = Path('paper-trail-corpus/exampapers/2023/LC003GLP100EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2023/LC003GLP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 48
review = dict(schemaVersion=1, subjectId='mathematics', year=2023, level='ordinary', lang='ev', paperKey='p1',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 1–27 of the combined Ordinary Level scheme (cover, notes, the Paper 1 scale table on page 4, the slips note and summary of allocations on page 5, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale, cross-checked against the printed summary.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(1, 28)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[4, 5],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '48 independently marked units, matching the printed summary of allocations on scheme page 5.',
        'Paper 1 bands from scheme page 4: 5B 0,3,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10B 0,7,10; 10C 0,4,6,10; 10D 0,4,6,8,10; 15C 0,6,10,15; 20D 0,7,10,15,20.',
        'Before this review the deck held 47 of the 48 units and shipped 46. Q3(b)(i)–(iii) (graphing the same inequality over ℝ, ℤ and ℕ, one 5D scale) is added. Q2(a)(iv), refused by the provenance gate over garbled credit text, now ships with quoted notes. Q8(e) carried a garbled stacked fraction and Q8(f) shipped its model-solution lines plus the scheme page header as marking points; their rows are re-quoted from the printed scheme. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
        'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions. The paper prints “the derivative of t” in Q7(b)(ii); the prompt keeps the printed wording.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [17], 'wording': 'or otherwise', 'classification': 'method-choice',
         'reason': 'Alternative solution methods for the same marked task; no printed pool of prompts.'},
        {'pages': [7, 10], 'wording': 'Tick one box', 'classification': 'answer-selection',
         'reason': 'The number with the largest modulus and the number of real roots are answers with justification, not alternative prompts.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'or otherwise' in t:
        d = ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2023-ordinary-p1.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2023 Ordinary Level Paper 1 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'The original scheme reader provides the full solution, including graphical answers and all credit notes.'
def pts(cid, quotes):
    return [dict(id=f'{cid}-solution-{i+1}', kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(quotes)]
rows = {
    'maths-2023-ol-p1-q2-a-iv': ['Writes 6² or (−2)²', 'Note: Accept correct answer without supporting work for full credit', 'Note: Full Credit -1 : 6 · 3 without work'],
    'maths-2023-ol-p1-q3-b': ['Work of merit, for example, shows knowledge of ℝ, ℤ, or ℕ.', 'One of the three inequalities graphed correctly', 'Work of merit in 2 or 3 inequalities', 'Two of the inequalities graphed correctly', 'Note: Accept 0 in (iii)', 'Note: Apply a * the first time ≥ is used instead of ≤; accept it thereafter'],
    'maths-2023-ol-p1-q8-e': ['= £718 · 56 [nearest penny]', 'Writes 116 · 9% or 100 + 16 · 9 or 1 · 169', 'Note: Apply F* if incorrect or no rounding'],
    'maths-2023-ol-p1-q8-f': ['€1007 · 37', 'Work of merit in either the exchange rate calculation or the commission calculation', 'Writes 21 or 861', 'Writes 982.80 with or without work', 'Note: Apply F* if incorrect or no rounding'],
}
ADDED = ['maths-2023-ol-p1-q3-b']
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
        _add(dict(id=c['id'], topicId=c['topicId'], conceptId='p1-q3-b', level='ordinary', year=2023, subjectId='maths',
            section='A', questionRef='2023 OL Paper 1 Q3(b)(i)–(iii)', questionText=c['questionText'],
            tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'], rows=pts(c['id'], rows[c['id']]), notes=note))
        continue
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] in rows:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = pts(c['id'], rows[c['id']])
assert sorted(added + rebuilt) == sorted(ADDED), (added, rebuilt)
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards), 'added', added)
