"""2024 HL Paper 1: review ledger + restored prompts for existing cards, restore Q9(b), add Q8(a)."""
from pathlib import Path
import hashlib, json, re, sys
sys.path.insert(0, 'scripts/markbank/mathematics')
from audit import selection_candidates
import fitz

SC = {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 4, 10],
      '10C': [0, 4, 6, 10], '10D': [0, 3, 5, 7, 10], '15C': [0, 6, 8, 15], '15D': [0, 4, 6, 8, 15], '20D': [0, 8, 11, 13, 20]}
cards = []
def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, stem=None, quotes=None):
    c = dict(id='maths-2024-hl-p1-q' + suffix, printedParts=parts.split(','), totalMarks=int(scale[:-1]), scale=scale,
             permittedMarks=SC[scale], schemePages=scheme, topicId='maths-' + topic, sourcePages=pages,
             examTopicIds=['mathematics-higher-' + a for a in atlas.split(',')])
    if stem: c['stem'] = stem
    c['questionText'] = prompt
    if quotes: c['solutionQuotes'] = quotes
    cards.append(c)

A('1-a', 'Q1(a)', '10D', [6], [4], '4-2', 'algebra-solving-equations', 'Solve the following equation for n ∈ ℕ: n − 3 = √(3n + 1)')
A('1-b', 'Q1(b)', '10C', [6], [4], '4-1', 'algebra-expressions-factorising', 'Write the following expression as a single fraction in terms of t: 4/(2t + 1) − 7/(12t)')
A('1-c', 'Q1(c)', '10D', [7], [5], '4-2', 'algebra-simultaneous-equations', 'Solve the following simultaneous equations for x, y, w ∈ ℤ: x + 2y = 143; y + 3w = −74; 4x + 5w = 4')
i2 = 'In this question, i² = −1.'
A('2-a', 'Q2(a)', '5D', [8], [6], '4-4', 'complex-numbers,algebra-quadratics', 'Find the two solutions of the following equation in z, where z is a complex number. Give each answer in the form a + bi, where a, b ∈ ℝ. z² + 12z + 261 = 0', stem=i2)
A('2-b', 'Q2(b)', '10D', [9], [6], '4-4', 'complex-numbers', 'Use de Moivre’s theorem to write (1 − √3 i)⁹ in the form a + bi, where a, b ∈ ℝ.', stem=i2)
A('2-c-i', 'Q2(c)(i),Q2(c)(ii)', '15D', [10], [7], '4-4', 'complex-numbers', '(i) Plot and label the complex number u = 4(cos π/6 + i sin π/6) on the diagram, as accurately as possible. (ii) The complex number o is 0 + 0i. Find the size of the angle ∠wou. Give your answer in radians.', stem=i2 + ' The point w = −2 + 2i is shown in the Argand diagram below.')
A('3-a', 'Q3(a)', '5B', [11], [8], '5-2', 'integration', 'Find the integral: ∫ cos 6x dx')
f3 = 'The function f is defined for x ∈ ℝ as: f(x) = 2x³ − 9x² + 5x − 11'
A('3-b-i', 'Q3(b)(i)', '5D', [11], [8], '5-2', 'differentiation-applications,co-ordinate-geometry-of-the-line', 'Find the equation of the tangent to the graph of f at the point where x = 2. You do not need to simplify your answer.', stem=f3)
A('3-b-ii', 'Q3(b)(ii)', '5C', [12], [8], '5-2', 'differentiation-applications', 'Find the x co-ordinate of the point of inflection of f.', stem=f3)
A('3-c', 'Q3(c)', '15D', [12], [9], '5-2', 'differentiation-applications', 'The diagram below shows the curve y = p(x) and the line y = l(x), for 0 ≤ x ≤ 10, x ∈ ℝ. There are two values of x in the domain 0 ≤ x ≤ 10 for which: p′(x) = l′(x), where p′(x) is the derivative of p(x). Use the infomation in the diagram to estimate these two values of x, as accurately as you can. Show your work on the diagram.')
A('4-a', 'Q4(a)', '10D', [13], [10], '5-2', 'differentiation-rules', 'Differentiate the following function from first principles, with respect to x: f(x) = x² − 7x − 10')
A('4-b', 'Q4(b)', '10D', [13], [11], '5-2', 'differentiation-rules', 'The function g(x) is defined for x ∈ ℝ by: g(x) = (6x + 1)/(x⁴ + 3). Find the value of g′(−2), the derivative of g(x) when x = −2.')
A('4-c', 'Q4(c)', '10B', [13], [11], '5-1', 'functions,differentiation-applications', 'h: ℝ → ℝ is a continuous function. The graph of h(x) has a local minimum at the point (0, 5). State whether the following statement is true or false: “The value of h(x) must be at least 5 for all real values of x.” Justify your answer.')
A('5-a', 'Q5(a)', '5C', [14], [12], '4-1', 'sequences-series', 'The first three terms of an arithmetic sequence are as follows, where p ∈ ℝ: T₁ = 2p + 1; T₂ = 5p − 3; T₃ = 6p + 7. Find the value of p.')
A('5-b', 'Q5(b)', '5C', [14], [12], '4-1', 'sequences-series', 'G₇ = 6 and G₁₁ = 3/8 are the 7th and 11th terms of a geometric sequence, respectively. Find the two possible values of r, the common ratio of this sequence, where r ∈ ℝ.')
A('5-c-i', 'Q5(c)(i),Q5(c)(ii)', '20D', [14], [13], '5-2', 'differentiation-rules,sequences-series', '(i) Write F₁ and F₂ in terms of x. (ii) Find the first value of n for which Fₙ = 0.', stem='A sequence of functions F₀, F₁, F₂, … is defined as follows, for x ∈ ℝ, x > 0: F₀ = x²⁰²⁴; for n ≥ 1, the function Fₙ is the derivative of Fₙ₋₁ with respect to x.')
A('6-a', 'Q6(a)', '10C', [15], [14], '4-1', 'algebra-expressions-factorising', 'h(x) = x² + bx − 12, where x ∈ ℝ and b is a constant. Find the value of b for which x − 4 is a factor of h(x).')
fg = 'Two functions, f(x) and g(x), are defined as follows, for x ∈ ℝ, x > 0: f(x) = e^(9x); g(x) = ln √x. Use these functions to answer parts (b)(i), (b)(ii), and (b)(iii).'
A('6-b-i', 'Q6(b)(i)', '5B', [15], [14], '3-2', 'indices-and-logs', 'Find the value of f(1·2). Give your answer in the form a × 10ⁿ, where a ∈ ℝ, 1 ≤ a < 10, n ∈ ℕ, and a is correct to 1 decimal place.', stem=fg)
A('6-b-ii', 'Q6(b)(ii)', '5C', [16], [14, 15], '3-2', 'indices-and-logs', 'Find the value of x for which g(x) = 3·5. Give your answer in the form e^p, where p ∈ ℝ.', stem=fg)
A('6-b-iii', 'Q6(b)(iii)', '10C', [16], [14, 15], '5-1', 'functions,indices-and-logs', 'Write the function g(f(x)) in terms of x, in its simplest form.', stem=fg)
A('7-a', 'Q7(a)', '10D', [17], [16], '3-3', 'financial-maths', 'Fiadh has a gross annual salary of €54 000. She pays income tax at a rate of 20% on the first €40 000 of her salary and at a rate of 40% on the remainder. She has an annual tax credit of €1775. Work out her net annual pay, assuming that there are no other deductions.')
A('7-b-i', 'Q7(b)(i),Q7(b)(ii)', '15D', [18], [16, 17], '3-3', 'financial-maths', '(i) Write down the present value of each of their first three monthly repayments, at the time when they take out the mortgage. Give each value as a fraction. Do not multiply out any powers. (ii) Work out the amount of money that Fiadh and her partner borrowed for their mortgage. Give your answer correct to the nearest euro.', stem='Fiadh and her partner take out a 25-year mortgage with a monthly interest rate of 0·279%. They make equal monthly repayments of €1647·75 at the end of each month. They make the first repayment exactly one month after they take out the mortgage.')
sav = 'Fiadh puts money in a savings account, and leaves it there for a number of years. The following expression gives F(t), the amount of money in the account in euro after t years, where t ∈ ℝ, t ≥ 0: F(t) = 5000e^(0·04t). Use this expression to answer parts (c)(i), (c)(ii), and (c)(iii).'
A('7-c-i', 'Q7(c)(i)', '10C', [19], [17], '5-2', 'differentiation-applications', 'Use differentiation to find the rate at which the amount of money in the account is increasing after 3·5 years. Give your answer correct to the nearest euro per year.', stem=sav)
A('7-c-ii', 'Q7(c)(ii)', '10D', [19], [17, 18], '5-2', 'integration', 'Use integration to find the average amount of money in the account over the first 5 years. Give your answer correct to the nearest euro.', stem=sav)
A('7-c-iii', 'Q7(c)(iii)', '5B', [20], [17, 18], '3-3', 'financial-maths,indices-and-logs', 'Work out the annual rate of interest (AER) for this account. That is, find the percentage increase in the amount of money in the account over the course of one year. Give your answer as a percentage, correct to 2 decimal places.', stem=sav)
A('8-a-i-ii', 'Q8(a)(i),Q8(a)(ii)', '10D', [21], [19], '5-1', 'functions', '(i) Fill in the table below, showing the value of T(x) for each of the given values of x. Give each value correct to the nearest whole number. Two values have already been filled in: T(60) = 43 and T(360) = 78; the values for x = 0, 120, 180, 240 and 300 are blank. (ii) Draw the graph of y = T(x) on the axes below, for 0 ≤ x ≤ 360, x ∈ ℝ.',
  stem='A clothing company sells t-shirts. The daily sales of t-shirts over a 360-day period can be modelled using the following function, T(x), where 0 ≤ x ≤ 360, x ∈ ℝ: T(x) = ((x − 240)/60)³ + 70',
  quotes=['Solution consists of 13 parts:', 'Points joined appropriately (not with line segments)', 'Work of merit in finding one value of T', '10 parts correct', '12 parts correct', 'Correct graph with no table entries'])
scarves = 'The clothing company also sells scarves. The daily sales of scarves can be modelled using the following function, S(t), which is a periodic function with a period of 365 days: S(t) = 21 + 19 cos(2πt/365). Here, t ∈ ℝ is the time, in days, from 1 January 2024, t ≥ 0, and 2πt/365 is in radians.'
cmod = scarves + ' A different function, C(t), can also be used to model the daily sales of scarves, where: C(t) = S(t) − 2·4 + 0·03t. Again, t ∈ ℝ is the time, in days, from 1 January 2024, t ≥ 0, and 2πt/365 is in radians.'
A('8-b', 'Q8(b)', '5C', [22], [20], '2-3', 'trigonometry-functions-identities,functions', 'Work out the maximum and minimum daily sales of scarves, according to S(t). You do not need to use differentiation.', stem=scarves)
A('8-c', 'Q8(c)', '10C', [22], [20], '4-2', 'algebra-solving-equations,functions', 'Find the value of t for which S(t) and C(t) give the same number of daily sales.', stem=cmod)
A('8-d', 'Q8(d)', '15C', [22], [20, 21], '5-1', 'functions,trigonometry-functions-identities', 'The graphs, J, K, and L, of three functions are shown below (not to scale). One of these graphs shows the function C(t) over a number of years, where C(t) = S(t) − 2·4 + 0·03t. Write down which graph this is. Justify your answer.', stem=cmod)
A('8-e', 'Q8(e)', '10C', [23], [20, 21], '5-2', 'differentiation-applications,trigonometry-functions-identities', 'The derivative of C(t) is given by C′(t) = 0·03 − (38π/365) sin(2πt/365). Find the value of t that gives the first local maximum of C, that is, the first time that C′(t) = 0. Give your answer correct to the nearest day.', stem=cmod)
cap = 'A sphere has a radius of R units. The part of the sphere that is cut off by a flat surface is called a “cap”, and has a volume of: C = (πk²/3)(3R − k). Here, C is the volume of the cap and k is the height of the cap, with 0 < k ≤ R.'
A('9-a', 'Q9(a)', '5C', [24], [22], '3-4', 'area-volume', 'Find the value of C, the volume of the cap, when R = 13 and k = 4. Give your answer in terms of π.', stem=cap)
A('9-b-i', 'Q9(b)(i),Q9(b)(ii)', '10D', [24], [22, 23], '4-2', 'algebra-quadratics,area-volume', '(i) Use this, and the expression for C above, to show that: (y/3)(24 − y) = 36. (ii) Multiply out and solve the equation (y/3)(24 − y) = 36 to find the height of this cap.',
  stem=cap + ' A different sphere has a radius of 8 units and a cap with a height of y units, with 0 < y ≤ 8. The volume of this cap is (36πy) units³.',
  quotes=['(y − 6)(y − 18) = 0', 'Ans: y = 6 [as y ≤ 8]', 'Work of merit in one part, for example, some relevant substitution in C', 'Part (i) correct', 'Part (ii) correct', 'y = 18 not eliminated'])
hemi = 'A hemisphere has a diameter of x cm. V(x), the volume of this hemisphere in cm³, is given by: V(x) = (π/12)x³.'
A('9-c', 'Q9(c)', '15C', [24], [23], '3-4', 'area-volume', 'Find the value of x when the volume of the hemisphere is 3 litres. Give your answer correct to 1 decimal place.', stem=hemi)
A('9-d', 'Q9(d)', '10D', [25], [23, 24], '5-2', 'differentiation-applications', 'The volume of the hemisphere is increasing at a constant rate of 450 cm³ per second. Find the rate at which the diameter (x) of the hemisphere is increasing with respect to time, when x = 20 cm. Give your answer in cm per second, correct to 1 decimal place. Remember that the volume of the hemisphere is V(x) = (π/12)x³.', stem=hemi)
A('9-e', 'Q9(e)', '10C', [25], [25], '4-1', 'algebra-expressions-factorising', 'A cone has a radius of r cm and a height of h cm. The curved surface area of the cone, S, can be written as: S = πr√(r² + h²). Rearrange this to write h in terms of S, r, and π. Give your answer in the form √(S² − arⁿ)/(br), where a, b, and n are constants.')
plants = 'A company grows and sells plants.'
w = plants + ' The function W(x) is defined below. It can be used to model the height, in mm, of a water spinach plant, for the first 35 days after it starts to grow. W(x) = 0·667x + 1·5x² − 0·025x³. Here, x is the number of days after the plant starts to grow, where 0 ≤ x ≤ 35, x ∈ ℝ.'
A('10-a-i', 'Q10(a)(i)', '5B', [26], [26], '5-1', 'functions', 'Use W(x) to estimate the height of a water spinach plant after 15 days. Give your answer correct to the nearest mm.', stem=w)
A('10-a-ii', 'Q10(a)(ii)', '5B', [26], [26], '5-2', 'differentiation-rules', 'Write down W′(x), the derivative of W(x).', stem=w)
A('10-b', 'Q10(b)', '10D', [26], [27], '4-3', 'algebra-inequalities,algebra-quadratics', 'The height of a different plant can be modelled by the function P(x), where x is again the number of days after the plant starts to grow. The derivative of this function is: P′(x) = 1·1 + 2·73x − 0·078x². Find the range of values of x for which P′(x) > 24. In your answer, give each value correct to the nearest whole number.', stem=plants)
logo = plants + ' The logo for the company is shown on the co-ordinate diagram below. The logo is the region enclosed by three curves, defined by the following functions c, s, and k: c(x) = x², for −1 ≤ x ≤ 1, x ∈ ℝ; s(x) = 2x − x², for 0 ≤ x ≤ 1, x ∈ ℝ; k(x) is the image of s(x) under axial symmetry in the y-axis.'
A('10-c-i', 'Q10(c)(i)', '5D', [27], [28], '5-2', 'integration', 'Use integration to work out the area of the logo. Hint: find the area of the logo in the first quadrant, and then double it.', stem=logo)
A('10-c-ii', 'Q10(c)(ii)', '15C', [28], [28, 29], '5-1', 'functions', 'The function k can be written in the form k(x) = −x² + bx + c, where b, c ∈ ℝ are constants. Find the value of b and the value of c. Remember that k is the image of s under axial symmetry in the y-axis.', stem=logo)
A('10-d', 'Q10(d)', '10D', [28], [29], '4-1', 'algebra-expressions-factorising', 'In this part, p and r are constants, with p, r ∈ ℝ and 0 < r < 0·9p. The company sells bags of plant food. The usual price of one bag is €p. In a sale, the customer can choose to pay using either Option 1 or Option 2, as follows: Option 1: the usual price reduced by 10%, and then reduced by a further €r; Option 2: the usual price reduced by €r, and then this new price reduced by 10%. Which option (1 or 2), if either, is cheaper? Write the price for each option (1 and 2) in terms of p and r, to support your answer. Tick one box only: Option 1; Option 2; It depends on the value of p and of r.', stem=plants)

P = Path('paper-trail-corpus/exampapers/2024/LC003ALP100EV.pdf'); S = Path('paper-trail-corpus/markingschemes/2024/LC003ALP000EV.pdf')
marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
tot = {}
for c in cards:
    q = re.match(r'Q(\d+)', c['printedParts'][0])[1]; tot[q] = tot.get(q, 0) + c['totalMarks']
assert tot == marks, tot
assert len(cards) == 41
review = dict(schemaVersion=1, subjectId='mathematics', year=2024, level='higher', lang='ev', paperKey='p1',
    paperFileid=P.name, schemeFileid=S.name, specificationId='mathematics:2015',
    paperSha256=hashlib.sha256(P.read_bytes()).hexdigest(), schemeSha256=hashlib.sha256(S.read_bytes()).hexdigest(),
    reviewedAt='2026-10-11',
    reviewMethod='Independent visual reading of all 32 question-paper pages and PDF pages 1–29 of the combined Higher Level scheme (cover, notes, the Paper 1 scale table on page 4, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale, not a parser count.',
    paperPagesInspected=list(range(1, len(fitz.open(P)) + 1)), schemePagesInspected=list(range(1, 30)),
    printedQuestionMarks=marks, fullCreditMinusOne=True, generalNotesPages=[4, 5],
    sourceNotes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained.',
        '41 independently marked units. Shared scales keep their parts together: Q2(c)(i)–(ii) 15D, Q5(c)(i)–(ii) 20D, Q7(b)(i)–(ii) 15D, Q8(a)(i)–(ii) 10D and Q9(b)(i)–(ii) 10D.',
        'Paper 1 bands from scheme page 4: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,4,10; 10C 0,4,6,10; 10D 0,3,5,7,10; 15C 0,6,8,15; 15D 0,4,6,8,15; 20D 0,8,11,13,20.',
        'The 2024 scheme prints no general notes on slips; Full Credit −1 is applied only where a marking note names it, as printed beside each scale. Pages 4–5 (scale table and annotation palette) are attached as general notes.',
        'Before this review the deck held 39 of the 41 units. Q8(a)(i)–(ii) had no card and is added. Q9(b)(i)–(ii) was authored but refused by the provenance gate because its third credit band is welded to the model solution in the scheme text layer; it is restored with marking points quoted where the text layer matches the printed scheme. All 39 existing card IDs, rows and figures are kept; prompts are restored from the paper and topics corrected as metadata.',
        'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions. The paper prints “infomation” in Q3(c); the prompt keeps the printed spelling.',
    ], cards=cards,
    selectionReview=[
        {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
         'reason': 'Candidates select independently marked questions; every question is retained.'},
        {'pages': [21], 'wording': 'One of these graphs shows the function C(t)', 'classification': 'answer-selection',
         'reason': 'Graphs J, K and L are answer options for one required identification with justification, not alternative prompts.'},
        {'pages': [29], 'wording': 'either Option 1 or Option 2 / Tick one box only', 'classification': 'answer-selection',
         'reason': 'The two pricing options are the objects compared; the ticked box is the answer to one required task.'},
    ])
dec = {}
for c in selection_candidates(P):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        d = ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    elif 'One of these graphs' in t:
        d = ('answer-selection', 'Exactly one of the printed graphs J, K, L shows C(t); identifying it with justification is one required task.')
    elif 'Option' in t or 'if either' in t:
        d = ('answer-selection', 'The customer’s two pricing options are compared in one required task (tick Option 1, Option 2 or “it depends”); not a choice of practice prompts.')
    else:
        raise SystemExit(c)
    dec[c['id']] = {'classification': d[0], 'reason': d[1]}
review['selectionDecisions'] = dec
out = Path('scripts/markbank/mathematics/reviews/2024-higher-p1.json')
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')

ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
byid = {c['id']: c for c in authored}
note = 'Prompt, grouped parts and context visually checked against the original 2024 Higher Level Paper 1 on 2026-10-11; exact question and scheme pages attached by the independent review.'
ADDED = ['maths-2024-hl-p1-q8-a-i-ii']
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
        assert c['id'] == 'maths-2024-hl-p1-q8-a-i-ii'
        _add(dict(id=c['id'], topicId=c['topicId'], conceptId='p1-q8-a-i-ii', level='higher', year=2024, subjectId='maths',
            section='B', questionRef='2024 HL Paper 1 Q8(a)(i), (ii)', stem=c['stem'], questionText=c['questionText'],
            tariffModel={'kind': 'questionTotal'}, totalMarks=c['totalMarks'],
            rows=[dict(id=f"{c['id']}-solution-{i+1}", kind='point', verbatim=q, marks=None,
                       contextNote='The original scheme reader provides the full solution, including graphical answers and all credit notes.')
                  for i, q in enumerate(c['solutionQuotes'])], notes=note))
        continue
    assert a['totalMarks'] == c['totalMarks'], c['id']
    a['questionText'] = c['questionText']
    if c.get('stem'): a['stem'] = c['stem']
    else: a.pop('stem', None)
    a['notes'] = note
    if c['id'] == 'maths-2024-hl-p1-q9-b-i':
        a['tariffModel'] = {'kind': 'questionTotal'}
        a['rows'] = [dict(id=f"{c['id']}-solution-{i+1}", kind='point', verbatim=q, marks=None,
                          contextNote='The original scheme reader provides the full solution, including graphical answers and all credit notes.')
                     for i, q in enumerate(c['solutionQuotes'])]
assert sorted(added + rebuilt) == sorted(ADDED), (added, rebuilt)
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
for c in cards: c.pop('solutionQuotes', None)
review['cards'] = cards
out.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
print('tasks', len(cards), 'marks', sum(c['totalMarks'] for c in cards))
