"""2024 OL Paper 1: review ledger, restored prompts, fix the three held-back cards."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 4, 10],
      '10C': [0, 4, 6, 10], '10D': [0, 3, 5, 7, 10], '15C': [0, 5, 8, 15], '15D': [0, 5, 7, 9, 15], '20D': [0, 7, 10, 12, 20]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None):
    c = dict(id='maths-2024-ol-p1-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-ordinary-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    cards.append(c)

A('1-a-i', 'Q1(a)(i),Q1(a)(ii)', '10D', [7], [4], '3-3', 'financial-maths', '(i) Find the value of the machine after 1 year. (ii) Hence, or otherwise, find the value of the machine after 2 years.', stem='A farmer buys a new machine for €30 000. It depreciates (decreases in value) by 20% each year.')
A('1-b', 'Q1(b)', '10C', [7], [5], '3-3', 'financial-maths', 'A farmer bought some livestock for €4716, including VAT. The cost of the livestock was €4500, excluding VAT. Calculate the percentage VAT rate used.')
A('1-c', 'Q1(c)', '10C', [8], [5], '3-3', 'financial-maths', 'The farmer also bought land. One year later its value had increased by 12·5% and was now €52 875. Find the value of the land when the farmer bought it.')
i2 = 'In this question, i² = −1.'
A('2-a-i', 'Q2(a)(i),Q2(a)(ii)', '10D', [9], [6], '3-1', 'complex-numbers', '(i) Using the Argand diagram, write down the values of z₁, z₂ and z₃ in the form a + bi where a, b ∈ ℤ. (ii) Write down the value of |z₂|.', stem=i2 + ' The complex numbers z₁, z₂, and z₃ are shown on the Argand diagram below. One of these numbers is on the imaginary axis.')
A('2-b', 'Q2(b)', '15C', [9], [6], '3-1', 'complex-numbers', 'v = 15/(1 + 2i). Write v in the form a + bi, where a, b ∈ ℤ.', stem=i2)
A('2-c', 'Q2(c)', '5B', [9], [7], '3-1', 'complex-numbers', 'The complex number w = 1 + 2i is shown on the Argand diagram below (drawn to scale). The three complex numbers labelled A, B, and C are also shown on the Argand diagram. One of these is w̅, the complex conjugate of w. Which of the complex numbers A, B or C is w̅? Give a reason for your answer. Tick one box only.', stem=i2)
A('3-a', 'Q3(a)', '10C', [10], [8], '3-3', 'number-systems', 'A toy shop sells two different sets of the same building blocks, Set A and Set B, as shown in the table below: Set A has 60 blocks and costs €12; Set B has 150 blocks and costs €28. Which set of building blocks works out cheaper per block? Use calculations to support your answer. Tick one box only: Set A or Set B.')
A('3-b', 'Q3(b)', '5C', [10], [8], '4-2', 'algebra-equations', 'Solve the following equation in x ∈ ℝ: 3x² − 5x + 1 = 0. Give each answer correct to 2 decimal places.')
A('3-c', 'Q3(c)', '15D', [10], [9], '4-2', 'algebra-equations', 'Use algebra to solve the simultaneous equations: 2x + y = 5; x² + y² = 25. Hint: first, use 2x + y = 5 to write y in terms of x.')
A('4-a', 'Q4(a)', '10C', [11], [10], '4-2', 'algebra-equations', 'Solve the following equation in x ∈ ℝ: 4(2x − 5) − 1 = 3x + 7')
A('4-b', 'Q4(b)', '10C', [11], [10], '3-3', 'number-systems', 'Liam, Joan and Martha split a bill in the following ratio: Liam : Joan : Martha = 4 : 3 : 5. Liam and Joan paid €154 in total between them. Martha paid the rest of the bill. Work out how much Martha paid.')
A('4-c-i', 'Q4(c)(i),Q4(c)(ii)', '10C', [11], [11], '3-2', 'indices', '(i) Write 128 in the form 2^k, where k ∈ ℕ. (ii) Hence, or otherwise, solve the following equation, where x ∈ ℝ: 2^(4x+1) = 128')
A('5-a', 'Q5(a)', '5C', [11], [12], '4-1', 'algebra', 'Find the value of the following expression when x = 2. Give your answer in the form a/b where a, b ∈ ℕ. (3x + 5)/10 − 1/(x + 3)')
A('5-b', 'Q5(b)', '20D', [11], [12], '5-2', 'differentiation', 'The function f is defined as f(x) = 5x² − 20x + 2, where x ∈ ℝ. Use calculus to find the co-ordinates of the local minimum point of f.')
A('5-c', 'Q5(c)', '5B', [11], [13], '5-2', 'differentiation,graphing-functions', 'The graph of the linear function g(x) is shown below. Use the graph to find the rate of change of g(x), that is, find g′(x). Give your answer in the form a/b where a, b ∈ ℕ.')
kgraph = 'The graph of a function k(x) is shown on the co-ordinate diagram below, for 0 ≤ x ≤ 5, x ∈ ℝ.'
A('6-a-i', 'Q6(a)(i),Q6(a)(ii)', '15D', [12], [14], '5-1', 'graphing-functions', '(i) Estimate the value of k(x) when x = 2·5. Show your work on the graph. (ii) Estimate the range of values of x, for which k(x) ≤ 7. Show your work on the graph.', stem=kgraph)
trap = kgraph + ' Liam uses the Trapezoidal Rule to estimate the area under the graph of k(x) between 0 and 5. He takes the following measurements from the graph: k(0) = 12, k(1) = 9, k(2) = 6·8, k(3) = 5·1, k(4) = 3·8, k(5) = 2·8.'
A('6-b-i', 'Q6(b)(i)', '5C', [12], [14, 15], '3-4', 'area-volume', 'Using the values of k(x) in the table above, show that the Trapezoidal Rule will give an estimate of 32·1 units² for this area.', stem=trap)
A('6-b-ii', 'Q6(b)(ii)', '10C', [12], [14, 15], '3-3', 'number-systems,area-volume', 'The actual area under k(x), between 0 and 5, is 31·8 units². Liam estimated the area was 32·1 units² by using the Trapezoidal Rule. Work out the percentage error in Liam’s estimate. Give your answer as a percent, correct to 2 decimal places.', stem=trap)
bact = 'During an experiment, the number of bacteria in a dish can be modelled by the function: p(t) = t³ − 6t² + 6t + 20, where p(t) is the number of bacteria, in thousands, and t is the time in hours since the start of the experiment, with 0 ≤ t ≤ 5, t ∈ ℝ.'
A('7-a-i', 'Q7(a)(i),Q7(a)(ii)', '10D', [13], [16], '5-1', 'graphing-functions', '(i) Complete the table below to show the values of p(t) for the given values of t. The table gives p(2) = 16 and p(4) = 12 and leaves t = 0, 1, 3 and 5 to complete. (ii) Draw the graph of p(t) on the axes below, for 0 ≤ t ≤ 5, t ∈ ℝ.', stem=bact)
A('7-a-iii', 'Q7(a)(iii),Q7(a)(iv)', '5D', [13], [16, 17], '5-2', 'differentiation', '(iii) Find p′(t), the derivative of p(t). Remember that: p(t) = t³ − 6t² + 6t + 20 (iv) Find the value of p′(2).', stem=bact)
A('7-a-v', 'Q7(a)(v)', '10B', [13], [16, 17], '5-2', 'differentiation', 'p′(4) = 6. Explain what this means in terms of the number of bacteria.', stem=bact)
kt = 'The number of bacteria in a different experiment can be modelled by the function: k(t) = 3000 × 2·72^(0·5t), where k(t) is the number of bacteria and t is the time in hours since the start of the experiment, with 0 ≤ t ≤ 8, t ∈ ℝ. There are 3000 bacteria at the beginning of the experiment.'
A('7-b-i', 'Q7(b)(i)', '10C', [14], [18], '5-1', 'functions,indices', 'Use k(t) to find the number of bacteria after 1 hour and after 2 hours. Give each answer correct to the nearest whole number.', stem=kt)
A('7-b-ii', 'Q7(b)(ii)', '15C', [14], [18], '5-1', 'functions,indices', 'After n hours, there are at least 35 000 bacteria according to k(t), where n ∈ ℕ. By continuing the pattern above, or otherwise, find the smallest possible value of n.', stem=kt)
cyc = 'Liam left home at 07:00. He cycled at a constant speed for 20 km, until he reached the point A. He then changed speed and cycled at a constant speed for a further 12 km, until he reached the point B. The graph shows his distance from home along the route cycled until he reached B.'
A('8-a-i', 'Q8(a)(i)', '5B', [15], [19], '5-1', 'graphing-functions', 'Use the graph to estimate the distance Liam had cycled by 08:00. Show your work on the diagram above.', stem=cyc)
A('8-a-ii', 'Q8(a)(ii)', '10C', [15], [19], '3-3', 'number-systems', 'Find his speed in km/hour while he was travelling from A to B.', stem=cyc)
A('8-a-iii', 'Q8(a)(iii)', '10C', [15], [19], '5-1', 'graphing-functions', 'Use the following information to complete the graph on the diagram above to show the rest of Liam’s journey: Liam stopped at B for 30 minutes; He then cycled the 32 km back home at a constant speed. This took him 1 hour.', stem=cyc)
run = 'Ellie takes up running. In the first week she runs 6 km. Each week after this she runs 1·5 km more than the previous week.'
A('8-b-i', 'Q8(b)(i),Q8(b)(ii)', '10D', [16], [20], '4-1', 'sequences-series', '(i) Complete the table below to show the distance Ellie runs each week for the first six weeks. The table gives week 1 as 6 km and week 2 as 7·5 km. (ii) If Ellie continued with this pattern, find the distance she would run in week 100.', stem=run)
A('8-b-iii', 'Q8(b)(iii)', '5A', [16], [20], '4-1', 'sequences-series', 'Explain why Ellie cannot continue this pattern indefinitely.', stem=run)
A('8-b-iv', 'Q8(b)(iv),Q8(b)(v)', '10D', [16], [20, 21], '4-1', 'sequences-series', '(iv) Sₙ is the total distance, in km, run by Ellie after n weeks, where n ∈ ℕ. Write Sₙ in terms of n. (v) Using your answer to part (b)(iv), or otherwise, find the total distance run by Ellie, in km, after 10 weeks if she continues the pattern (that is, find S₁₀).', stem=run)
A('9-a-i', 'Q9(a)(i),Q9(a)(ii)', '15D', [17], [22], '3-3', 'financial-maths', '(i) Using the exchange rate €1 = £0·85, find the cost of the concert ticket, in euro. (ii) Liam is a member of the venue’s Loyalty Club, so he gets a discount of 20% on all tickets. He buys 8 tickets for the concert. Work out the total cost of the 8 tickets, in euro.', stem='A ticket for a concert in Wales costs £59·50.')
A('9-b', 'Q9(b)', '10C', [17], [23], '3-3', 'number-systems', 'Liam flies to the concert. He finds the following information: The aeroplane emits 28 000 grams of carbon per km, during the flight; His total flight distance is 394 km; There are 244 passengers on the flight. Work out the amount of carbon emitted during the flight, per passenger. Give your answer in kg, correct to 1 decimal place.')
att = 'The number of people who will attend a concert (the attendance) can change depending on the price of a ticket. For a particular concert, this can be modelled by the function: A(x) = 17 600 − 160x, where A(x) is the attendance at the concert and x is the price of a ticket, in euro, with 0 ≤ x ≤ 110, x ∈ ℝ. Use the function A(x) to answer parts (c)(i) and (c)(ii).'
A('9-c-i', 'Q9(c)(i)', '5B', [17], [24], '5-1', 'functions', 'Find the attendance at this concert if the price of a ticket is €20.', stem=att)
A('9-c-ii', 'Q9(c)(ii)', '10C', [18], [24], '4-2', 'algebra-equations,functions', 'Find the price of a ticket (value of x) for which the attendance would be 12 800.', stem=att)
A('9-d-i', 'Q9(d)(i),Q9(d)(ii)', '10D', [18], [25], '4-2', 'algebra-equations', '(i) For this concert the total tickets sales are €360 000. Use this information to show that: x² − 100x + 2400 = 0 (ii) Solve the equation x² − 100x + 2400 = 0 to find the two possible ticket prices for this concert.', stem='For a different concert the total tickets sales, in euro, can be modelled by: 15 000x − 150x². Again, x is the price of a ticket, in euro.')
A('10-a-i', 'Q10(a)(i),Q10(a)(ii)', '5D', [19], [26], '3-3', 'financial-maths', '(i) Work out his net annual income. (ii) Hence, write his net annual income as a percentage of his gross annual income. Give your answer correct to the nearest percent.', stem='In 2023 Joseph has a gross annual income of €48 000. He pays net annual income tax of €7650, annual PRSI of €1920, and pays €1407 in USC each year. He has no further deductions from his gross income.')
tax = 'The two income tax rates in Ireland in 2023 are given in the table below: the first €40 000 of annual income is taxed at 20% and the balance at 40%.'
A('10-b-i', 'Q10(b)(i),Q10(b)(ii)', '15D', [19], [27], '3-3', 'financial-maths', '(i) Olivia’s gross annual income is €34 000 and her annual tax credit is €3550. Find her net annual income. (ii) Caroline’s gross annual income is €50 000. Her annual tax credit is €3550. Find how much annual income tax she pays.', stem=tax)
A('10-b-iii', 'Q10(b)(iii)', '10B', [20], [27, 28], '3-3', 'financial-maths', 'The personal tax credit for an employee in Ireland in 2023 is €3550. Find the greatest amount of income an employee can earn before paying any income tax. Hint: The lowest income tax rate is 20%.', stem=tax)
A('10-b-iv', 'Q10(b)(iv)', '5C', [20], [27, 28], '3-3', 'financial-maths', 'In 2024, the amount of income being taxed at the 20% rate was increased from €40 000 to €42 000. Work out how much less income tax a person earning more than €42 000 would pay in 2024 compared to 2023 due to this increase.', stem=tax)
A('10-c-i', 'Q10(c)(i),Q10(c)(ii)', '15D', [20], [29], '3-3', 'financial-maths', '(i) Anne’s annual electricity bill was €1950 and broadband bill was €400. She worked from home for 120 days in the year. Find how much tax relief she can claim. Give your answer correct to the nearest cent. (ii) Tara also worked from home for a number of days. Tara’s total electricity and broadband bills were €2250. She claimed tax relief of €135 for working from home. Calculate how many days she worked from home.',
  stem='An employee who works from home may qualify for tax relief on their electricity and broadband bills. The amount of tax relief such an employee can claim, A, is calculated using the formula: A = (Total annual electricity and broadband bills) × d/365 × 0·3, where d is the number of days worked from home.')

P = Path('paper-trail-corpus/exampapers/2024/LC003GLP100EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2024/LC003GLP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 39
review = dict(schemaVersion=1, subjectId='mathematics', year=2024, level='ordinary', lang='ev', paperKey='p1',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 1–23 of the combined Ordinary Level scheme (cover, notes, the Paper 1 scale table on page 4, the slips note and printed summary of allocations on page 5, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale, cross-checked against the printed summary.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(1, 24)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[4, 5],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '39 independently marked units, matching the printed summary of allocations on scheme page 5.',
        'Paper 1 bands from scheme page 4: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,4,10; 10C 0,4,6,10; 10D 0,3,5,7,10; 15C 0,5,8,15; 15D 0,5,7,9,15; 20D 0,7,10,12,20.',
        'All 39 units were already authored, but three never shipped: Q2(c) was refused for naming lettered points without a decoded figure (the original page now supplies the Argand diagram), and Q3(a) and Q10(b)(iv) were refused because their joined credit-band text does not match the scheme text layer. Their marking points are now quoted line by line from the printed scheme. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata (complex numbers follow the Ordinary precedent of 3.1 Number systems).',
        'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [4, 11, 18, 21], 'wording': 'Hence, or otherwise / or otherwise', 'classification': 'method-choice',
         'reason': 'Alternative solution methods for the same marked task; no printed pool of prompts.'},
        {'pages': [7, 8], 'wording': 'Tick one box only', 'classification': 'answer-selection',
         'reason': 'Choosing A, B or C (the conjugate) and Set A or Set B is the answer to one required task with justification, not a choice of prompts.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'or otherwise' in t:
        d = ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    elif 'One of these' in t:
        d = ('given-context', 'States that one of the printed numbers lies on an axis (or is the conjugate); data for a required task, not a choice of prompts.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2024-ordinary-p1.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2024 Ordinary Level Paper 1 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'The original scheme reader provides the full solution, including graphical answers and all credit notes.'
replace_rows = {
    'maths-2024-ol-p1-q2-c': ['Box C ticked', 'The conjugate is reflected in the real axis', 'Correct box ticked', 'Work of merit in reason, for example, 1 − 2i'],
    'maths-2024-ol-p1-q3-a': ['Set B', 'Correct box ticked', 'Work of merit, for example, a correct calculation/setup', 'A full comparable calculation worked out', 'Correct box ticked and work of merit'],
    'maths-2024-ol-p1-q10-b-iv': ['(42 000 − 40 000) × 0·2 = [€]400', 'Work of merit, for example, finding', '2000 × 20%', 'Finding total tax for a person earning 42 000 or more for both years'],
}
for c in cards:
    a = byid[c['id']]
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] in replace_rows:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = [dict(id=f"{c['id']}-solution-{i+1}", kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(replace_rows[c['id']])]
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards))
