"""2016 OL Paper 1: a new paper — 39 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'

ROWS = {
 'maths-2016-ol-p1-q1-a': [L(SOL, '5 × 2 = 10'), L(SOL, '28 − 10 = 18'), L(SOL, '18 ÷ 2 = 9'), L(SOL, '€9 per hour'), L(LPC, 'Any use of 2, 5 or 28'),
     L(HPC, '18 calculated')],
 'maths-2016-ol-p1-q1-b': [L(SOL, 'w = 9h+2d')],
 'maths-2016-ol-p1-q1-c': [L(SOL, '9(6)+12(2)+5(13·5)+2d = 161·50'), L(SOL, '145·5 + 2d = 161·50'), L(SOL, '2d = 16'), L(SOL, 'd = 8'),
     L(LPC, '9(6) or 12(2) or 78 formulated calculated or used'), L(LPC, '13·5 written'), L(HPC, '83·5 and/or 67·5')],
 'maths-2016-ol-p1-q2-a': [L(SOL, 'z₃ = 1 + 3i + 2(2 − i)'), L(SOL, 'z₃ = 5 + i'), L(LPC, 'Any correct substitution'), L(HPC, 'Correct multiplication')],
 'maths-2016-ol-p1-q2-b': [L(LPC, 'One Point correctly plotted'), L(LPC, '2 points correctly plotted but without labels'),
     L(HPC, '2 points correctly plotted and labelled'), L(HPC, '3 points correctly plotted without labels'),
     L(HPC, 'Mixes up real and imaginary axes with label of 3 correct points')],
 'maths-2016-ol-p1-q2-c': [L(SOL, '|−3 − 2i| = √13'), L(SOL, '| 3 + 2i| = √13')],
 'maths-2016-ol-p1-q2-d': [L(SOL, 'w = (1 + 3i)(2 + i)/(2 − i)(2 + i)'), L(SOL, '(2 + i + 6i + 3i²)/(4 + 2i − 2i − i²)'), L(SOL, 'w = (−1 + 7i)/5'),
     L(SOL, 'w = −1/5 + 7/5 i'), L(LPC, 'Any correct substitution'), L(MPC, 'Conjugate identified'),
     L(MPC, 'Some multiplication above and below, even if by wrong conjugate'), L(HPC, 'multiply out correctly')],
 'maths-2016-ol-p1-q3-a': [L(SOL, '3x − 21 + 5x − 20 = 15'), L(SOL, '8x = 56'), L(SOL, 'x = 7'), L(LPC, 'Any correct multiplication'), L(LPC, 'Correct answer no work'),
     L(HPC, 'Both multiplications done correctly and fails to finish'), L(HPC, 'Error in expanding brackets and finishes correctly')],
 'maths-2016-ol-p1-q3-b': [L(SOL, '4a + 3b = −3'), L(SOL, '5a − 2b = 25'), L(SOL, '8a + 6b = −6'), L(SOL, '15a − 6b = 75'), L(SOL, '23a = 69'), L(SOL, 'a = 3'),
     L(SOL, 'b = −5'), L(PC, 'Some correct work in solving')],
 'maths-2016-ol-p1-q3-c': [L(SOL, '4x − 6 + 6x < 25'), L(SOL, '10x < 31'), L(SOL, 'x < 3·1'), L(SOL, '{1, 2, 3}'), L(NOTE, 'accept {0, 1, 2, 3}'),
     L(LPC, 'Any correct step'), L(LPC, 'Correct answer without work'), L(HPC, 'Solves for x'), L(HPC, 'Error in multiplication but finishes correctly')],
 'maths-2016-ol-p1-q4-a': [L(SOL, 'x = 0'), L(SOL, 'y = 7'), L(PC, 'x = 0, written'), L(PC, 'Zero correctly substituted into equation')],
 'maths-2016-ol-p1-q4-b': [L(SOL, '1 + 1 − 2 + 7 = 7'), L(SOL, '7 = 7'), L(PC, 'Any correct substitution')],
 'maths-2016-ol-p1-q4-c-i': [L(SOL, 'f′(x) = 3x² + 2x − 2'), L(SOL, 'at x = 1'), L(SOL, 'f′(x) = 3(1)² + 2(1) − 2'), L(SOL, 'm = 3'),
     L(LPC, 'Any correct differentiation'), L(MPC, 'Fully correct differentiation'), L(HPC, 'Correct substitution for slope')],
 'maths-2016-ol-p1-q4-c-ii': [L(SOL, 'y − 7 = 3(x − 1)'), L(SOL, 'y = 3x + 4'), L(SOL, '3x − y + 4 = 0'), L(PC, 'Shows m = 3'),
     L(PC, 'Correct equation of a line formula'), L(PC, 'Any correct substitution')],
 'maths-2016-ol-p1-q5-a-i': [L(SOL, '2nd difference is constant implies quadratic'), L(LPC, 'One or two correct terms'),
     L(HPC, '3 terms correct but fails to show quadratic')],
 'maths-2016-ol-p1-q5-b': [L(SOL, '1 + b + c = 13'), L(SOL, '4 + 2b + c = 15'), L(SOL, 'b + c = 12'), L(SOL, '2b + c = 11'), L(SOL, 'b = −1'), L(SOL, 'c = 13'),
     L(LPC, 'Derives one correct equation'), L(HPC, 'Derives two correct equations')],
 'maths-2016-ol-p1-q5-c': [L(SOL, 'a = 12'), L(SOL, 'd = 2'), L(SOL, 'Tn = 12 + 2(n − 1)'), L(SOL, 'Tn = 10 + 2n'), L(SOL, 'T30 = 10 + 2(30) = 70'),
     L(LPC, 'a or d identified'), L(LPC, 'Writes Tn = a + (n − 1)d'), L(HPC, 'Tn correct and stops'),
     L(HPC, 'Finds T30 correctly using list method, without finding Tn')],
 'maths-2016-ol-p1-q6-a': [L(SOL, '1300 × 0·2 = 260'), L(SOL, '250 × 0·4 = 100'), L(SOL, '260 + 100 = 360'), L(SOL, '360 − 126 = 234'),
     L(LPC, 'Sets up 20% of 1300'), L(LPC, 'calculates €250'), L(LPC, 'Finds €260 or €100'), L(HPC, 'Finds €260 and €100, or finds €360')],
 'maths-2016-ol-p1-q6-b': [L(SOL, '462×0·01 + 214×0·03 + 874×0·055'), L(SOL, '4·62 + 6·42 + 48·07'), L(SOL, '= 59·11'), L(LPC, 'Finds one correct amount'),
     L(LPC, 'Formulates a % correctly'), L(LPC, 'Finds €874 or €676'), L(HPC, 'Finds two correct amounts')],
 'maths-2016-ol-p1-q6-c-i': [L(SOL, '18 + 234 + 59·11 = 311·11'), L(SOL, '311·11/1550 × 100/1 = 20·1%'), L(LPC, '€234 or €59·11 written in this section'),
     L(LPC, 'Some correct addition for (c)(i)'), L(HPC, 'Correct deductions found, €311·11'), L(HPC, 'Formulates % correctly for (c)(ii)')],
 'maths-2016-ol-p1-q7-a': [L(SOL, '8000(1·02)(1·03)(1·05) = 8825·04'), L(ALT, '8000(1·02) = 8160'), L(ALT, '8160(1·03) = 8404·8'), L(ALT, '8404·8(1·05) = 8825·04'),
     L(LPC, 'Any effort at calculation of interest on €8000 at 2% or 3% or 5%'), L(MPC, 'One correct calculation, €160 or €8160'),
     L(MPC, 'Uses simple interest leading to €8800 or €800'), L(HPC, 'Two correct calculations, €244·80 or €8404·80'),
     L(HPC, 'Finds correct interest for each year but fails to finish'), L(HPC, 'Fully correct formulation of amount')],
 'maths-2016-ol-p1-q7-b': [L(SOL, '8000(1·037)³ = 8921·26'), L(ALT, '8000(1·037) = 8296'), L(ALT, '8296(1·037) = 8602·95'), L(ALT, '8602·95(1·037) = 8921·26'),
     L(LPC, 'Relevant use of 3·7%'), L(MPC, 'One correct calculation, €296 or €8296'), L(MPC, 'Use of simple interest leading to €8888, or €888'),
     L(HPC, 'Two correct calculations, €306·95 or €8602·95'), L(HPC, 'Finds correct interest for each year but fails to finish'),
     L(HPC, 'Fully correct formulation of amount')],
 'maths-2016-ol-p1-q7-c': [L(SOL, 'Might want the flexibility of taking money out before the end.'), L(ALT, 'Choose the one that gives the most money')],
 'maths-2016-ol-p1-q7-d': [L(SOL, '8000(1 + x/100)³ = 9000'), L(SOL, '1 + x/100 = ∛(9/8)'), L(SOL, 'x = 4%'), L(LPC, 'At least one correct substitution'),
     L(LPC, 'Correct formula'), L(LPC, 'Correct answer no work'), L(LPC, '9000 ‒ 8000 = 1000'), L(HPC, 'Fully correct substitution into formula but fails to finish')],
 'maths-2016-ol-p1-q7-e-i': [L(SOL, 'v = 8000 + 36(12) − 1·2(12)²'), L(SOL, 'v = 8259·20'), L(LPC, 'Any correct substitution into formula'),
     L(HPC, 'Fully correct substitution into formula but fails to finish'), L(HPC, 'Subs t = 1 giving answer of 8034·80')],
 'maths-2016-ol-p1-q7-e-ii': [L(SOL, '259·20/8000 × 100 =3·24'), L(SOL, 'Rate = 3·24'), L(ALT, '8259·20/8000 =1·0324'), L(LPC, 'Brings down interest or amount from e(i)'),
     L(LPC, 'Relevant work'), L(HPC, 'Formulates correctly')],
 'maths-2016-ol-p1-q8-a': [L(SOL, '2x + 2y = 21'), L(SOL, 'x + y = 10·5'), L(SOL, 'y = 10·5 − x'), L(PC, 'Some correct work on perimeter'), L(PC, 'Relevant work on diagram')],
 'maths-2016-ol-p1-q8-b-i': [L(LPC, 'relevant calculations without any correct entry'), L(LPC, '1, 2, 3 or 4 correct entries to table (y or A)'),
     L(MPC, '5 or 6 correct pairs of entries (y and A) or full y line correct'), L(HPC, '7, 8 or 9 correct pairs of entries (y and A)')],
 'maths-2016-ol-p1-q8-b-ii': [L(LPC, '1, 2, 3 or 4 correct plots'), L(LPC, 'Graphs y only'), L(MPC, '5, 6, 7 or 8 correct plots'),
     L(HPC, '9, 10 or 11 correct plots but no joining or incorrect joining')],
 'maths-2016-ol-p1-q8-c': [L(SOL, 'Maximum area 27·5 ≤ A ≤ 28'), L(SOL, 'x value 5 ≤ X ≤ 5·5'), L(SOL, 'y value 5·5 ≥ Y ≥ 5'),
     L(LPC, 'Maximum area identified from graph'), L(HPC, 'Area and one corresponding value')],
 'maths-2016-ol-p1-q8-d-i': [L(SOL, 'A = xy'), L(SOL, 'A = x(10·5 − x)'), L(SOL, 'A = 10·5x − x²'), L(LPC, 'Relevant area formula'),
     L(HPC, 'Correct substitution into area formula')],
 'maths-2016-ol-p1-q8-d-ii': [L(SOL, 'dA/dx = 10·5 − 2x'), L(PC, 'Any correct differentiation')],
 'maths-2016-ol-p1-q8-d-iii': [L(SOL, '10·5 − 2x = 0'), L(SOL, 'x = 5·25'), L(NOTE, 'Must have calculus in (d)(ii) to get any marks in this section'),
     L(LPC, 'Any use of answer to (d)(ii)'), L(HPC, 'Lets their derivative = 0')],
 'maths-2016-ol-p1-q8-d-iv': [L(SOL, 'A = xy'), L(SOL, 'A = 5·25×5·25'), L(SOL, 'A = 27·56'), L(ALT, 'A = 10·5(5·25) − (5·25)²'), L(ALT, '55·125 − 27·5625'),
     L(PC, 'Any substitution into area formula or equation given in (d)(i)'), L(PC, 'Writes area formula')],
 'maths-2016-ol-p1-q9-a-i': [L(LPC, 'relevant calculations'), L(LPC, '1, 2, 3 or 4 correct entries into table'), L(MPC, '5 or 6 correct entries'),
     L(HPC, '7, 8 or 9 correct entries')],
 'maths-2016-ol-p1-q9-a-ii': [L(LPC, '1, 2, 3 or 4 correct plots'), L(MPC, '5 to 11 correct plots'), L(HPC, 'All plots correct but no joining or incorrect joining'),
     L(HPC, '9, 10 or 11 points plotted correct and joined correctly')],
 'maths-2016-ol-p1-q9-b': [L(SOL, 'B = €40'), L(SOL, 'A = €52'), L(SOL, 'B is cheaper (from graph)'), L(PC, 'A or B clearly identified on graph'),
     L(PC, 'B given as answer but no reason')],
 'maths-2016-ol-p1-q9-c': [L(SOL, 'ℎ ≈ 3·2'), L(PC, 'Point clearly indicated on graph')],
 'maths-2016-ol-p1-q9-d': [L(SOL, 'A(6) = 30 + 9·5(6) = 87'), L(SOL, 'B(6) = 10(1·74)⁶ = 277·52'), L(SOL, 'Difference = 190·52'),
     L(LPC, 'A(6) or B(6) substituted correctly'), L(MPC, 'A(6) or B(6) evaluated correctly'), L(HPC, 'A(6) and B(6) evaluated correctly')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Filled from scheme_row_figures.py's output once its crops are opened and checked.
SCHEME_ROW_FIGURES = {
    'maths-2016-ol-p1-q2-b': 'maths-2016-OL-scheme-p008-i0',
    'maths-2016-ol-p1-q5-a-i': 'maths-2016-OL-scheme-p011-i0',
    'maths-2016-ol-p1-q5-b': 'maths-2016-OL-scheme-p011-i1',
    'maths-2016-ol-p1-q8-b-i': 'maths-2016-OL-scheme-p016-i0',
    'maths-2016-ol-p1-q8-b-ii': 'maths-2016-OL-scheme-p016-i1',
    'maths-2016-ol-p1-q9-a-i': 'maths-2016-OL-scheme-p018-i0',
    'maths-2016-ol-p1-q9-a-ii': 'maths-2016-OL-scheme-p019-i0',
}

p = Paper(2016, 'ol', 'p1', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 4, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 3, 10], '10C': [0, 2, 5, 10],
                             '10D': [0, 2, 4, 6, 10], '15C': [0, 3, 7, 15], '15D': [0, 4, 7, 11, 15]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
emma = 'Emma works part time after school at the local takeaway. She is paid a rate per hour and also receives €2 for each delivery she makes.'
q1a = 'One day, she works for 2 hours, makes 5 deliveries and is paid a total of €28. Find her hourly rate of pay.'
ns, ae = 'number-systems', 'algebra-equations'
A('1-a', 'Q1(a)', '10C', [7], [3], '3-3', ns + ',' + ae, q1a, stem=emma)
A('1-b', 'Q1(b)', '5A', [7], [3], '4-1', 'algebra', 'One week, she works for h hours and makes d deliveries. Write a formula in h and d for the wage (w) she receives.', stem=emma + ' Part (a): ' + q1a)
A('1-c', 'Q1(c)', '10C', [7], [3], '4-2', ae + ',' + ns, 'Another week, she works for 6 hours and makes 12 deliveries. She also works 5 hours on a Sunday, at time and a half, and makes some deliveries. In total, she receives €161·50 for that week. Find how many deliveries she makes on the Sunday.',
  stem=emma + ' Part (a): ' + q1a)
cx = 'complex-numbers'
zz = 'z₁ = 1 + 3i and z₂ = 2 − i, where i² = −1, are two complex numbers.'
q2a = 'Let z₃ = z₁ + 2z₂. Find z₃ in the form a + bi where a, b ∈ ℤ.'
A('2-a', 'Q2(a)', '5C', [8], [4], '4-4', cx, q2a, stem=zz)
A('2-b', 'Q2(b)', '5C', [8], [4], '4-4', cx, 'Plot z₁, z₂, and z₃ on the given Argand diagram and label each point clearly.', stem=zz + ' Part (a): ' + q2a)
A('2-c', 'Q2(c)', '5A', [8], [4], '4-4', cx, 'Investigate if |z₂ − z₃| = |z₁ + z₂|.', stem=zz + ' Part (a): ' + q2a)
A('2-d', 'Q2(d)', '10D', [8], [5], '4-4', cx, 'Find the complex number w, such that w = z₁/z₂. Give your answer in the form a + bi, where a, b ∈ ℝ.', stem=zz)
A('3-a', 'Q3(a)', '5C', [9], [6], '4-2', ae, 'Solve for x: 3(x − 7) + 5(x − 4) = 15, where x ∈ ℝ.')
A('3-b', 'Q3(b)', '10B', [9], [6], '4-2', ae, 'Solve the equations below to find the value of a and the value of b: 4a + 3b = −3; 5a = 25 + 2b.')
A('3-c', 'Q3(c)', '10C', [9], [6], '4-3', 'algebra', 'List all the values of x that satisfy the inequality 2(2x − 3) + 6x < 25, where x ∈ ℕ.')
fn = 'The function f : x ↦ x³ + x² − 2x + 7 is defined for x ∈ ℝ.'
q4ci = 'Find f′(x), the derivative of f(x). Hence find the slope of the tangent to the graph of f when x = 1.'
A('4-a', 'Q4(a)', '5B', [10], [7], '5-1', 'functions', 'Find the coordinates of the point at which the graph of f cuts the y-axis.', stem=fn)
A('4-b', 'Q4(b)', '5B', [10], [7], '5-1', 'functions', 'Verify, using algebra, that the point A(1, 7) is on the graph of f.', stem=fn)
A('4-c-i', 'Q4(c)(i)', '10D', [10], [7], '5-2', 'differentiation', q4ci, stem=fn)
A('4-c-ii', 'Q4(c)(ii)', '5B', [10], [7], '5-2', 'differentiation,co-ordinate-geometry-of-the-line', 'Hence, find the equation of the tangent to the graph of f at the point A(1, 7).',
  stem=fn + ' Part (c)(i): ' + q4ci)
ss = 'sequences-series'
pat = ('The first five numbers in a pattern of numbers are given in the table below. Table: Term, Number. U1 13; U2 15; U3 19; U4 25; U5 33; U6 _; '
       'U7 _; U8 _.')
A('5-a-i', 'Q5(a)(i),Q5(a)(ii)', '5C', [11], [8], '4-1', ss, '(i) Follow the pattern in the table above to write the next three numbers into the table. (ii) Use the data in the table to show that the pattern is quadratic.', stem=pat)
A('5-b', 'Q5(b)', '15C', [11], [8], '4-1', ss + ',' + ae, 'Uₙ = n² + bn + c where b, c ∈ ℤ. Find the value of b and the value of c.', stem=pat)
A('5-c', 'Q5(c)', '5C', [12], [9], '4-1', ss, 'The table below shows the first five terms of an arithmetic sequence. Find an expression for Tₙ, the nth term of the sequence. Hence, or otherwise, find the value of T₃₀, the 30th term. Table: Term, Number. T1 12; T2 14; T3 16; T4 18; T5 20.')
fm = 'financial-maths'
fiona = 'Fiona earns a gross wage of €1550 every fortnight. She pays income tax, a Universal Social Charge (USC), and Pay Related Social Insurance (PRSI) on this wage.'
q6a = 'Each fortnight, Fiona pays income tax at the rate of 20% on the first €1300 she earns and 40% on the remainder. She has tax credits of €126 per fortnight. Find how much income tax she pays per fortnight.'
q6b = 'Each fortnight, Fiona also pays USC on her gross wage. The rates are: 1% on the first €462 she earns, 3% on the next €214, and 5·5% on the balance. Find the total amount of USC she pays each fortnight.'
A('6-a', 'Q6(a)', '5C', [13], [10], '3-3', fm, q6a, stem=fiona)
A('6-b', 'Q6(b)', '10C', [13], [10], '3-3', fm, q6b, stem=fiona)
A('6-c-i', 'Q6(c)(i),Q6(c)(ii)', '10C', [13], [11], '3-3', fm, '(i) Fiona pays PRSI amounting to €18 each fortnight. Find the sum of her fortnightly deductions. (ii) Write the sum of her fortnightly deductions as a percentage of her gross wage. Give your answer correct to one decimal place.',
  stem=fiona + ' Part (a): ' + q6a + ' Part (b): ' + q6b)
paul = ('Paul has €8000 that he wants to invest for a maximum of 3 years. His local bank is offering him two options, Option 1 and Option 2, as shown in '
        'the table below. Table: Option 1: 2% interest in Year 1; 3% interest in Year 2; 5% interest in Year 3; Money can be taken out at the end of Year 1 '
        'or Year 2 without penalty. Option 2: 3·7% compound interest per year, for 3 years; Money may not be taken out until the end of Year 3.')
fund = ('Another bank offers to invest his €8000 in a special fund. The bank has found that, in the short term, the amount of money in this fund follows '
        'the formula v = 8000 + 36t − 1·2t² where v is the value of the fund, in euro, and t is the time, in months, since the €8000 was invested.')
q7ei = 'Find the value of the money in the fund after 12 months.'
A('7-a', 'Q7(a)', '10D', [14], [12], '3-3', fm, 'Find the value of the investment at the end of 3 years if Paul chooses Option 1 and does not take any money out.', stem=paul)
A('7-b', 'Q7(b)', '10D', [14], [12], '3-3', fm, 'Find the value of the investment at the end of 3 years if Paul chooses Option 2.', stem=paul)
A('7-c', 'Q7(c)', '5A', [14], [12], '3-3', fm, 'Give one issue, other than the rate of interest earned, that Paul might take into account when deciding between Option 1 and Option 2.', stem=paul)
A('7-d', 'Q7(d)', '10C', [14], [13], '3-3', fm, 'Paul would like his investment of €8000 to amount to €9000 after 3 years. What annual rate of compound interest would be required for this to happen? Give your answer as a percentage.')
A('7-e-i', 'Q7(e)(i)', '10C', [15], [13], '3-3', fm + ',functions', q7ei, stem=fund)
A('7-e-ii', 'Q7(e)(ii)', '10C', [15], [13], '3-3', fm, 'Mary invests €8000 for 1 year at r % per annum. After 1 year her investment is worth the same amount as the answer to part (e)(i) above. Find the value of r, correct to 2 decimal places.',
  stem=fund + ' Part (e)(i): ' + q7ei)
kier = 'Kieran has 21 metres of fencing. He wants to enclose a vegetable garden in a rectangular shape as shown.'
q8a = 'By writing an expression for the perimeter of the vegetable garden in terms of x (length in metres) and y (width in metres), show that y = 10·5 − x.'
q8bi = ('Complete the table below to show the values of y and A (the area of the garden) for each given value of x. Table: x (m): 0, 1, 2, 3, 4, 5, 6, 7, 8, '
        '9, 10. y (m): _, _, _, _, 6·5, _, _, _, _, _, _. A (m²): _, _, _, _, 26, _, _, _, _, _, _.')
q8bii = 'Use the values of x and A from the table to plot the graph of A on the grid below.'
q8di = 'Show that the area of the rectangle can be written as A = 10·5x − x².'
q8dii = 'Find dA/dx.'
q8diii = 'Hence, find the value of x which will give the maximum area.'
gf, df, av = 'graphing-functions', 'differentiation', 'area-volume'
A('8-a', 'Q8(a)', '5B', [16], [14], '4-1', 'algebra,' + av, q8a, stem=kier)
A('8-b-i', 'Q8(b)(i)', '5D', [16], [14], '5-1', gf + ',' + av, q8bi, stem=kier + ' Part (a): ' + q8a)
A('8-b-ii', 'Q8(b)(ii)', '5D', [16], [14], '5-1', gf, q8bii, stem=kier + ' Part (b)(i): ' + q8bi)
A('8-c', 'Q8(c)', '5C', [17], [15], '5-1', gf, 'Use your graph to estimate the maximum value of A and write the corresponding length and width. Table: A: Maximum area (m²) _; Length (m) _; Width (m) _.',
  stem=kier + ' Part (b)(ii): ' + q8bii)
A('8-d-i', 'Q8(d)(i)', '15C', [17], [15], '4-1', 'algebra,' + av, q8di, stem=kier + ' Part (a): ' + q8a)
A('8-d-ii', 'Q8(d)(ii)', '5B', [17], [15], '5-2', df, q8dii, stem=kier + ' Part (d)(i): ' + q8di)
A('8-d-iii', 'Q8(d)(iii)', '5C', [17], [15], '5-2', df, q8diii, stem=kier + ' Part (d)(ii): ' + q8dii)
A('8-d-iv', 'Q8(d)(iv)', '5B', [17], [15], '5-2', df + ',' + av, 'Find this maximum area.', stem=kier + ' Part (d)(i): ' + q8di + ' Part (d)(iii): ' + q8diii)
comp = ('Company A uses the following formula to charge a customer for a job: A(h) = 30 + 9·5h, where A(h) is the cost of the job, in euro, and h is the '
        'length of time that the job takes in hours. Company B uses the following formula to charge a customer for the same job: B(h) = 10(1·74)^h where '
        'B(h) is the cost of the job, in euro, and h is again the length of time that the job takes in hours.')
q9ai = ('Complete the table below to show what Company A charges and what Company B charges for jobs that take up to 5 hours. Where necessary give the '
        'charge correct to the nearest cent. Table: Time (hours): 0, 1, 2, 3, 4, 5. A(h) (€): _, _, _, _, 68, _. B(h) (€): _, _, _, _, 91·66, _.')
q9aii = 'On the grid below draw separate graphs to show the charge for Company A and the charge for Company B. Label each graph clearly.'
A('9-a-i', 'Q9(a)(i)', '10D', [18], [16], '5-1', gf + ',functions', q9ai, stem=comp)
A('9-a-ii', 'Q9(a)(ii)', '15D', [19], [16], '5-1', gf, q9aii, stem=comp + ' Part (a)(i): ' + q9ai)
A('9-b', 'Q9(b)', '5B', [20], [17], '5-1', gf, 'Which company would charge least for a job that takes 2½ hours to complete? Give a reason for your answer.', stem=comp + ' Part (a)(ii): ' + q9aii)
A('9-c', 'Q9(c)', '5B', [20], [17], '5-1', gf, 'Use your graphs to estimate the value of h for which the charge is the same for both companies.', stem=comp + ' Part (a)(ii): ' + q9aii)
A('9-d', 'Q9(d)', '10D', [20], [17], '5-1', 'functions,indices', 'Find the difference in cost for a job that takes 6 hours to complete.', stem=comp)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 50, '9': 45}
p.check(marks, 39)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 1–20 of the combined Ordinary Level scheme (cover, notes, the Paper 1 title page, the scale table on page 5, the summary of mark allocations on page 6, and every Paper 1 model solution and marking note on pages 7–20). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 21)), [5, 6],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 50 marks, Q9 45 marks). Every question is retained.',
     '39 independently marked units, matching the printed summary of allocations on scheme page 6. Q5(a)(i)+(ii) and Q6(c)(i)+(ii) each share one printed scale and are one task.',
     'Paper 1 bands from the 2016 Ordinary scale table on scheme page 5: 5A 0,5; 5B 0,2,5; 5C 0,2,4,5; 5D 0,2,3,4,5; 10B 0,3,10; 10C 0,2,5,10; 10D 0,2,4,6,10; 15C 0,3,7,15; 15D 0,4,7,11,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 39 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced. Stacked fractions are written a/b and exponents in prompts use caret notation (10(1·74)^h). The Q5(b) model solution names its terms with a U the text layer cannot carry, so its equations are quoted without the U1/U2 labels and its “Some relevant substitution into Un” band is not quoted.',
     'Seven parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal: Q2(b) (the Argand diagram), Q5(a)(i)+(ii) (the completed table and differences), Q5(b) (the band naming Un), Q8(b)(i) (the table), Q8(b)(ii) (the graph), Q9(a)(i) (the table) and Q9(a)(ii) (the graphs).',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 2); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 12], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [9], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'},
     {'pages': [12], 'wording': 'Option 1 and Option 2', 'classification': 'mathematical-context',
      'reason': 'The two investment options are both evaluated in required tasks (a) and (b), and (c) asks about choosing between them; there is no printed choice of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'otherwise' in t
        else ('mathematical-context', 'The two investment options are both evaluated in required tasks (a) and (b), and (c) asks about choosing between them; there is no printed choice of prompts.') if 'Option' in t else None)
p.apply(ROWS, '2016 Ordinary Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
