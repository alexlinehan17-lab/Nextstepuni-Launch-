"""2023 HL Paper 1: review ledger, restored prompts, ship 3 held-back cards, add Q10(c), fix Q10(e)(ii) rows."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 4, 7, 10], '10D': [0, 3, 5, 8, 10],
      '15C': [0, 6, 12, 15], '15D': [0, 4, 8, 12, 15], '20D': [0, 5, 10, 15, 20]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None):
    c = dict(id='maths-2023-hl-p1-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-higher-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    cards.append(c)

A('1-a', 'Q1(a)', '15D', [7], [4], '4-2', 'algebra-solving-equations', 'Find the two values of m ∈ ℝ for which |5 + 3m| = 11.')
A('1-b', 'Q1(b)', '10D', [8], [4], '4-1', 'algebra-expressions-factorising', 'For the real numbers h, j, and k: 1/h = k/(j + k). Express k in terms of h and j.')
A('1-c', 'Q1(c)', '5D', [9], [5], '4-2', 'algebra-cubics', 'x² − px + 1 is a factor of x³ − 2x − 3r, where p, r ∈ ℝ and p < 0. Find the value of p and the value of r.')
A('2-a', 'Q2(a)', '15D', [10], [6], '5-2', 'differentiation-applications,algebra-quadratics', 'f(x) = x² + bx + c, where b, c ∈ ℝ. f(x) has a local minimum point at (3, −1). Find the value of b and the value of c.')
A('2-b', 'Q2(b)', '5C', [10], [6], '4-1', 'sequences-series', 'Find the value of the following limit, where n ∈ ℕ: lim (n → ∞) [ n/(n + 1) + (n + 1000)/n + (1/3)ⁿ ]')
A('2-c', 'Q2(c)(i),Q2(c)(ii)', '10C', [11], [7], '5-1', 'functions', '(i) Draw the graph of g(x) − 2 on the co-ordinate diagram below, for x ∈ ℝ, on as large a domain as possible. (ii) Draw the graph of g(x + 3) on the co-ordinate diagram below, for x ∈ ℝ, on as large a domain as possible.', stem='The function g(x) is defined for −2 ≤ x ≤ 2, x ∈ ℝ. Its graph is shown in each of the two diagrams below.')
A('3-a', 'Q3(a)', '10D', [12], [8], '3-1', 'induction', 'Prove that √2 is not a rational number.')
A('3-b', 'Q3(b)', '10D', [12], [9], '3-2', 'indices-and-logs', 't is a positive real number, with: log₃ t + log₉ t + log₂₇ t + log₈₁ t = 10. Find the value of t. Give your answer in the form 3^r, where r ∈ ℚ. Hint: use the formula logₐ b = (log꜀ b)/(log꜀ a).')
A('3-c-i', 'Q3(c)(i),Q3(c)(ii)', '10C', [13], [9], '3-2', 'indices-and-logs', '(i) Explain what log₆ m means, where m is a positive real number. (ii) m is a real number, and m > 6. What information does this give about the value of log₆ m?')
i2 = 'In this question, i² = −1.'
A('4-a', 'Q4(a)', '5C', [14], [10], '4-4', 'complex-numbers', 'The complex number z₁ = 1 + i is a root of the equation z² + (3 − 2i)z + p = 0. Find the value of p, where p = a + bi, with a, b ∈ ℤ.', stem=i2)
A('4-b', 'Q4(b)', '15D', [15], [10], '4-4', 'complex-numbers', 'Use De Moivre’s Theorem to find the values of w for which w² = −1 + √3i. Give each value of w in the form a + bi, with a, b ∈ ℝ.', stem=i2)
A('4-c-i', 'Q4(c)(i),Q4(c)(ii),Q4(c)(iii)', '10D', [16], [11], '4-4', 'complex-numbers', '(i) Write the complex numbers iu and i̅u̅ (the conjugate of iu) in their simplest form, in terms of a and b, where the conjugate of iu is written with a bar over iu. (ii) Plot and label the complex numbers iu and its conjugate on the diagram above, as accurately as possible. (iii) State a transformation, or series of transformations, that would send u to the conjugate of iu. Do not include a translation in your answer.', stem=i2 + ' The Argand diagram below shows the complex number u = a + bi, where a, b ∈ ℝ.')
A('5-a', 'Q5(a)', '15C', [17], [12], '5-2', 'differentiation-rules', 'The function f is defined as follows, for x ∈ ℝ: f(x) = 1/(5x² + 7). Find f′(x), the derivative of f. Give your answer in its simplest form.')
A('5-b', 'Q5(b)', '5D', [17], [12], '5-2', 'differentiation-rules', 'The function g(x) is defined as follows, for x ∈ ℝ, 0 < x < π: g(x) = (tan(x/2))(ln x). Find the value of g′(π/2). Give your answer in the form a + ln b, where a, b ∈ ℝ.')
A('5-c-i', 'Q5(c)(i),Q5(c)(ii)', '10D', [18], [13], '5-1', 'functions', '(i) Find the value of g(f(3)). (ii) Explain why g: B → C is injective but not surjective (that is, one-to-one but not onto).', stem='The diagram below shows three sets, A, B, and C, and two functions, f and g, where f: A → B and g: B → C. #A = #C = 4 and #B = 3.')
fg = 'f and g are two functions of x ∈ ℝ, where: f(x) = x + 4; g(x) = x² − 2.'
A('6-a-i', 'Q6(a)(i)', '10C', [19], [14], '4-2', 'algebra-quadratics,functions', 'Find the two values of x for which f(x) = g(x).', stem=fg)
A('6-a-ii', 'Q6(a)(ii)', '15D', [20], [14], '5-2', 'integration', 'Find the area of the shaded region in the diagram below (not to scale), the region between the graphs of f(x) = x + 4 and g(x) = x² − 2, from x = −1 to x = 2.', stem=fg)
A('6-b', 'Q6(b)', '5D', [21], [15], '5-2', 'integration,indices-and-logs', 'b ∈ ℝ is a positive constant, and: ∫ (from 0 to b) b e^(bx) dx = e. Work out the value of b.')
fiona = 'Fiona is driving on a motorway. She passes a point A on the motorway. Her speed is given by: v(t) = (2/3)t³ − 6t² + 13t + 109, where v is her speed in km/hour t minutes after passing the point A, for 0 ≤ t ≤ 5 and t ∈ ℝ.'
A('7-a', 'Q7(a)', '5B', [21], [16], '5-1', 'functions', 'Work out Fiona’s speed when she passes the point A.', stem=fiona)
A('7-b', 'Q7(b)', '10C', [21], [16], '5-2', 'differentiation-applications', 'Work out Fiona’s acceleration (that is, the rate at which her speed is increasing) 5 minutes after she passes the point A. Give your answer in km/hour per minute.', stem=fiona)
A('7-c', 'Q7(c)', '10C', [22], [16], '5-2', 'differentiation-applications', 'Find the time (value of t) at which Fiona reaches her maximum speed, during the first 4 minutes after she passes the point A. Give your answer correct to 2 decimal places.', stem=fiona)
A('7-d', 'Q7(d)', '10D', [23], [16, 17], '5-2', 'integration', 'Use integration to work out Fiona’s average speed over the 5 minutes after she passes the point A. Give your answer correct to 2 decimal places.', stem=fiona)
A('7-e', 'Q7(e)', '5C', [24], [16, 17], '5-2', 'differentiation-applications', 'Taking v′(t) to be the derivative of v, and v′′(t) to be the second derivative of v: v′(1) > 0 and v′′(1) < 0. Four graphs, A, B, C, and D, are shown below. Close to where t = 1, the graph of y = v(t) must look like one of the four graphs given above. Write down which graph this is. Justify your answer, using both v′(1) and v′′(1).', stem=fiona)
zone = 'There is an Average Speed Zone on the motorway, starting at the point A and ending at point B. The distance from A to B along the motorway is 10 km. Cameras record the time taken for each car to travel from the point A to the point B. Each car’s average speed from A to B is then calculated.'
A('7-f', 'Q7(f)', '5B', [25], [18], '3-3', 'functions', 'Work out the minimum time, in minutes, that a driver could get from A to B, while not driving above 100 km/hour.', stem=zone)
A('7-g', 'Q7(g)', '5D', [25], [18], '3-3', 'functions', 'Rohan drives from A to B. He passes the point A driving at a constant speed of 120 km/hour. After 2 minutes driving at this speed, he starts to decelerate (reduce his speed) at a constant rate, until he reaches the point B. Overall, his average speed in driving from A to B is 100 km/hour. Work out Rohan’s deceleration. Give your answer in km/hour per minute.', stem=zone)
banks = 'Olga, Chen, Fiona, and Rohan all have bank accounts.'
A('8-a', 'Q8(a)', '5B', [26], [19], '3-3', 'financial-maths', 'Olga puts €3000 in a savings account. Interest is added annually at a rate of 2·4% per year. Work out the amount in Olga’s account after 5 years, correct to the nearest cent.', stem=banks)
A('8-b-i', 'Q8(b)(i),Q8(b)(ii)', '10D', [26], [19], '3-3', 'financial-maths', '(i) Explain what is meant by the “present value” of a payment of €1000 in 1 year’s time, at a particular interest rate. (ii) Chen puts a different amount in a savings account with the same interest rate (2·4% per year). After 6 years, Chen has €4000 in the account. Work out how much money Chen put in the account initially, correct to the nearest cent.', stem=banks)
A('8-c', 'Q8(c)', '5C', [26], [20], '3-3', 'financial-maths', 'Fiona is taking out a loan at the same annual interest rate (2·4% per year). Fiona makes payments quarterly (that is, 4 times per year). Work out the quarterly interest rate that would be equivalent to an APR of 2·4%. Give your answer as a percentage, correct to 2 decimal places.', stem=banks)
A('8-d-i', 'Q8(d)(i),Q8(d)(ii)', '15D', [27], [20], '3-3', 'financial-maths,sequences-series', '(i) Taking €A to be the amount Rohan puts in his account at the start of each month, write down a geometric series in €A to show the total amount of money in the account at the end of the 3 years. Include the first two and the last two terms. (ii) Hence, find the value of €A that will give a total of €12 000 in the account after 3 years. Give your answer correct to the nearest cent.', stem=banks + ' Rohan wants to put the same amount of money in a savings account at the start of each month for 36 months so that, at the end of 3 years, he will have a total of €12 000 in the account. Interest is calculated at a rate of 0·11% per month.')
A('8-e', 'Q8(e)', '10C', [27], [21], '1-2', 'probability,algebra-solving-equations', 'A park sells three types of ticket: child, student, and adult. The table below gives information on the price of each ticket and the percentage of tickets sold: child €11 (52%); student €5 less than an adult ticket (15%); adult €x (33%). For example, 15% of all tickets sold are student tickets. The expected value of the price of a ticket is €13·85. Work out the value of x, the price of an adult ticket.')
A('8-f', 'Q8(f)', '5B', [27], [21], '3-3', 'financial-maths', 'When an item is being sold: the mark up is the profit as a percentage of the cost price, and the margin is the profit as a percentage of the selling price. A shop sells an item with a margin of 18%. Work out the mark up for this item. Give your answer as a percentage, correct to the nearest percent.')
ava = 'Ava is investigating factors of different numbers.'
A('9-a-i', 'Q9(a)(i),Q9(a)(ii),Q9(a)(iii)', '15D', [28], [22], '3-2', 'indices-and-logs', '(i) List the 5 different factors of 2⁴. You can write each one as a power of 2. (ii) Work out how many different factors 3⁷ has. (iii) Work out how many different factors 2¹⁰ × 3¹² has.', stem=ava + ' First, she looks at numbers that can be written as powers of a prime number.')
A('9-b-i', 'Q9(b)(i),Q9(b)(ii),Q9(b)(iii)', '20D', [28], [23], '5-1', 'functions', '(i) Complete the table below, showing the 6 pairs of factors (x and y) of 12. The table gives x = 1, 2, 3, 6 and y = 4 (for x = 3) and y = 1. (ii) Plot the 6 points above on the co-ordinate diagram below. One of the points is shown. (iii) Ava realises that the relationship between x and y is y = 12/x. On the co-ordinate diagram above, draw the graph of y = 12/x for x ∈ ℝ, in the domain 1 ≤ x ≤ 12.', stem=ava + ' Ava also looks at the relationship between pairs of factors of a number. She makes a table to show the pairs of factors of 12 (that is, the pairs of natural numbers x and y with xy = 12).')
A('9-c-i', 'Q9(c)(i)', '10D', [29], [24], '5-2', 'differentiation-applications,co-ordinate-geometry-of-the-line', 'A tangent to the curve y = 12/x is drawn at the point (p, 12/p), where p ∈ ℝ and p > 0. Show that the equation of this tangent is: y = −(12/p²)x + 24/p', stem=ava)
A('9-c-ii', 'Q9(c)(ii)', '5D', [30], [25], '2-2', 'co-ordinate-geometry-of-the-line,area-volume', 'The area of the triangle formed by the x-axis, the y-axis, and the tangent y = −(12/p²)x + 24/p is always k square units, where k ∈ ℕ is a constant. Work out the value of k.', stem=ava)
tri = 'A triangle has a base of length 2 units and a perpendicular height of 8 units, as shown in the diagram on the right. The diagrams below show T₁, T₂, and T₃, the first three shapes in a sequence of shapes based on this triangle. For each value of n ∈ ℕ, the shape Tₙ is made up of n rectangles of equal height laid on top of each other. Tₙ is the collection of the smallest such rectangles that completely covers the triangle.'
A('10-a', 'Q10(a)', '5B', [31], [26], '3-4', 'area-volume', 'Draw T₄ in the grid below, based on the triangle given on the grid.', stem=tri)
A('10-b', 'Q10(b)', '10C', [31], [26], '3-4', 'area-volume', 'Show that the total area of the three rectangles in T₃ is 32/3 square units.', stem=tri)
A('10-c', 'Q10(c)', '5C', [32], [26, 27], '4-1', 'sequences-series,area-volume', 'Find the total area of the n rectangles in Tₙ, for n ∈ ℕ. Give your answer in square units in terms of n, in its simplest form.', stem=tri)
A('10-d', 'Q10(d)', '10D', [33], [27], '4-3', 'algebra-inequalities,sequences-series', 'The total area of the rectangles in the nth term of a different sequence of groups of rectangles is as follows, for n ∈ ℕ: Total area = Aₙ = 8(n − 1)/n. Work out the first value of n for which Aₙ is greater than 95% of the area of the triangle on the right (base 2, height 8).')
pyr = 'Diagram A below shows a square-based pyramid, with base sides of length c units. The base of the pyramid is horizontal, and its perpendicular height is h units (where c, h ∈ ℝ). Diagram B below shows the same pyramid. It also shows a horizontal square that lies within the pyramid, a distance of x units down from the top of the pyramid, where x ∈ ℝ, 0 < x < h. The area of the shaded square in Diagram B is S(x) = x²c²/h².'
A('10-e-i', 'Q10(e)(i)', '10C', [33], [28], '5-2', 'integration,area-volume', 'The volume of the pyramid is ∫ (from 0 to h) S(x) dx. Use integration to find the volume of the pyramid in cubic units, in terms of c and h.', stem=pyr)
A('10-e-ii', 'Q10(e)(ii)', '10D', [34], [28, 29], '5-2', 'differentiation-applications', 'x starts to increase at a rate of 3 units per second. This causes S(x) to increase as well. Find the rate of change of S(x) with respect to time, at the instant when x is half the perpendicular height of the pyramid. Give your answer in square units per second, in terms of c and h.', stem=pyr)

P = Path('paper-trail-corpus/exampapers/2023/LC003ALP100EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2023/LC003ALP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 41
review = dict(schemaVersion=1, subjectId='mathematics', year=2023, level='higher', lang='ev', paperKey='p1',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 1–35 of the combined Higher Level scheme (cover, notes, the Paper 1 scale table on page 4, the summary of allocations on page 5, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale beside its model solution.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(1, 36)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[4, 5],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '41 independently marked units. Shared scales keep their parts together: Q2(c)(i)–(ii) 10C, Q3(c)(i)–(ii) 10C, Q4(c)(i)–(iii) 10D, Q5(c)(i)–(ii) 10D, Q8(b)(i)–(ii) 10D, Q8(d)(i)–(ii) 15D, Q9(a)(i)–(iii) 15D and Q9(b)(i)–(iii) 20D.',
        'Paper 1 bands from scheme page 4: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10A 0,10; 10B 0,5,10; 10C 0,4,7,10; 10D 0,3,5,8,10; 15C 0,6,12,15; 15D 0,4,8,12,15; 20D 0,5,10,15,20.',
        'The printed summary on scheme page 5 lists Question 3 as “(a) 10D, (b)(i) 10D, (b)(ii) 10C”, but the paper prints Q3(a), Q3(b) and Q3(c)(i)–(ii); the scales beside the model solutions (pages 12–13) are authoritative: (a) 10D, (b) 10D, (c)(i)(ii) 10C.',
        'Before this review the deck held 40 of the 41 units and shipped 37. Q10(c) (5C) had no card and is added. Q2(b), Q8(b) and Q8(d) were authored but refused by the provenance gate because their credit text was garbled by the scheme text layer; their marking points are now quoted line by line. Q10(e)(ii) had shipped the model-solution lines plus the scheme page header as its marking points; its rows are replaced with the published credit notes. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
        'Q3(a) (proof that √2 is irrational) is filed under the syllabus proof topic 3.1 Number systems and the Atlas Induction/proof shelf.',
        'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [17], 'wording': 'must look like one of the four graphs', 'classification': 'answer-selection',
         'reason': 'Graphs A–D are answer options for one required identification with justification, not alternative prompts.'},
        {'pages': [23], 'wording': 'One of the points is shown', 'classification': 'given-context',
         'reason': 'States that one plotted point is supplied; every point must still be plotted under one scale.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'one of the four graphs' in t:
        d = ('answer-selection', 'Exactly one of graphs A–D matches v′(1) > 0 and v′′(1) < 0; identifying and justifying it is one required task.')
    elif 'One of the points is shown' in t:
        d = ('given-context', 'One of the six points is pre-plotted as an example; the candidate plots the others under one scale.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2023-higher-p1.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2023 Higher Level Paper 1 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ctx = 'The original scheme reader provides the full solution, including graphical answers and all credit notes.'
def pts(cid, quotes):
    return [dict(id=f'{cid}-solution-{i+1}', kind='point', verbatim=q, marks=None, contextNote=ctx) for i, q in enumerate(quotes)]
replace_rows = {
    'maths-2023-hl-p1-q2-b': ['= 2', 'Note: Full credit for correct answer without work.', 'Work of merit, for example, indicates sum of limits', 'Substitutes ∞ for n', 'One limit correctly evaluated and work of merit in any one of the other two limits'],
    'maths-2023-hl-p1-q8-b-i': ['It is the amount that should be invested today to amount to €1000 in 1 years’ time at the particular interest rate.', 'P = €3469·45', '2.4% written as a decimal', '(i) or (ii) correct', 'Work of merit in both parts', 'One part correct and work of merit in the other part'],
    'maths-2023-hl-p1-q8-d-i': ['A = €326·60 [2 D.P.]', 'Finds geometric series', 'Substitutes into geometric formula', 'Finds A', '1 step correct', 'Substantial work of merit in both parts', '2 steps correct'],
    'maths-2023-hl-p1-q10-e-ii': ['= 6c²x/h²', 'States a relevant derivative, for example', 'Some correct differentiation', 'Any two of the following:', 'from the MPC list above'],
}
ADDED = ['maths-2023-hl-p1-q10-c']
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
        assert c['id'] == 'maths-2023-hl-p1-q10-c'
        _add(dict(id=c['id'], topicId=c['topicId'], conceptId='p1-q10-c', level='higher', year=2023, subjectId='maths',
            section='B', questionRef='2023 HL Paper 1 Q10(c)', stem=c['stem'], questionText=c['questionText'],
            tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'],
            rows=pts(c['id'], ['or equivalent', 'Identifies 2n (or n) small triangles', 'Base length of each small triangle found', 'or equivalent not in closed form', 'Finds sum of the areas of the small triangles']),
            notes=note))
        continue
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] in replace_rows:
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = pts(c['id'], replace_rows[c['id']])
assert sorted(added + rebuilt) == sorted(ADDED), (added, rebuilt)
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards))
