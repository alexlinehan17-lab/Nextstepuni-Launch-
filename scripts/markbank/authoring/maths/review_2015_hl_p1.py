"""2015 HL Paper 1: a new paper — 32 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
S1, S2 = 'Solution 1, ', 'Solution 2, '
ALT = 'Model solution (alternative)'
LMPC, HMPC = 'Low Mid Partial Credit', 'High Mid Partial Credit'

# 2015 prints its model solutions as equation images whose text layer is
# scattered digits; the marking notes are prose. The bands are quoted from the
# notes, with the few model-solution lines the text layer carries whole, and
# every card carries the SEC's print of its model solution and notes.
ROWS = {
 'maths-2015-hl-p1-q1-a': [L(LPC, 'Any term correct'), L(HPC, 'Any two terms correct'), L(NOTE, 'Dividing by 3/4 gets high partial credit at most.'),
     L(NOTE, 'Correct decimal values high partial at most.')],
 'maths-2015-hl-p1-q1-b': [L(S1 + LPC, 'Indicates addition of terms'), L(S1 + HPC, 'Recognises double distance after first hop'),
     L(S1 + HPC, 'Sum of all rises or drops'), L(S2 + LPC, 'Indicates addition of terms'), L(S2 + LPC, 'Indicates Geometric Progression'),
     L(S2 + HPC, 'Correct Geometric Progression formula with correct substitution')],
 'maths-2015-hl-p1-q1-c': [L(LPC, 'Recognition of sum to infinity'), L(LPC, 'S∞ formula'), L(HPC, 'Correct formula with correct substitution'),
     L(HPC, 'Sum of all rises or drops')],
 'maths-2015-hl-p1-q2': [L(SOL, '(x ‒ 1) is a factor'), L(LPC, 'Effort at finding root'), L(LMPC, 'Finds one root correctly'),
     L(LMPC, 'x² after division by incorrect factor'), L(LMPC, 'Correct answers in decimal form from calculator with or without work'),
     L(HPC, 'Having got a quadratic equation with no remainder, fills in quadratic formula'), L(HPC, '1 ± √12'),
     L(NOTE, 'If there is a remainder after division can only get maximum of 15 marks.')],
 'maths-2015-hl-p1-q3-a-i': [L(SOL, '35 square units'), L(LPC, 'Any one correct value'), L(LPC, 'Writes formula'), L(MPC, 'Correct table'),
     L(HPC, 'Correct formula for trapezoidal rule, and some correct substitution with ℎ = 1'),
     L(HPC, 'Completely incorrect table but applied correctly in a(ii)'), L(HPC, 'Correct table and 35 without work'),
     L(NOTE, 'Answers in terms of ℎ merit Mid Partial at most.'), L(NOTE, 'Correct formula and some substitution gets High Partial.')],
 'maths-2015-hl-p1-q3-b-i': [L(LPC, 'Any correct integration'), L(LPC, 'Correct % error formula'),
     L(HPC, 'Correct integration with some correct substitution'), L(HPC, '97·2%'), L(FC, 'Accept 2·8% without work for full credit.')],
 'maths-2015-hl-p1-q4-a': [L(S1 + LPC, 'Some rationalisation'), L(S1 + LPC, 'Some relevant rearrangement.'), L(S2 + LPC, 'One complex number correct'),
     L(S2 + MPC, 'Two complex numbers correct')],
 'maths-2015-hl-p1-q4-b': [L(LPC, 'Correct Geometric Progression formula'), L(LPC, 'Correct first term'), L(LPC, 'Correct ratio'),
     L(HPC, 'Values substituted in formula')],
 'maths-2015-hl-p1-q5-a': [L(LPC, 'Indication of squaring'), L(HPC, 'Correct roots'), L(NOTE, 'must indicate required root')],
 'maths-2015-hl-p1-q5-b': [L(PC, 'Any correct differentiation')],
 'maths-2015-hl-p1-q5-c': [L(LPC, 'Differentiation equals 0'), L(HPC, 'Finds x value.'),
     L(NOTE, 'A linear equation from f′(x) gets low partial at most.'), L(NOTE, 'Must put f′(x) = 0 in (c) to get any marks.')],
 'maths-2015-hl-p1-q6-a-i': [L(LPC, 'Correct formula in either part'), L(LPC, 'Correct substitution in incorrect formula'), L(HPC, 'Any one section correct'),
     L(NOTE, 'Rate as 0·367% or 0·00367 gets High Partial.')],
 'maths-2015-hl-p1-q6-b': [L(SOL, '€818'), L(S1 + LPC, 'Any correct step, i.e. correct formula'), L(S1 + HPC, 'Substitution in correct formula.'),
     L(S2 + LPC, 'Correct equation.'), L(S2 + LPC, 'Listing some terms'), L(S2 + LPC, 'Some substitution'),
     L(S2 + HPC, 'Complete substitution and effort at evaluation.'),
     L(NOTE, 'If A and 80 000 interchanged and remainder of work correct, may get High Partial credit.')],
 'maths-2015-hl-p1-q7-a-i': [L(SOL, '⇒ d = 0')],
 'maths-2015-hl-p1-q7-a-ii': [L(SOL, '⇒ c = 0'), L(ALT, 'The plane lands horizontally at O'), L(S1 + FC, 'Begins with c = 0 and shows f(−5) = 0 · 15 or similar')],
 'maths-2015-hl-p1-q7-b-i': [L(LPC, 'Any term correctly differentiated.'), L(HPC, 'Correct differentiation'), L(FC, '−18/625 is a correct answer')],
 'maths-2015-hl-p1-q7-b-ii': [L(SOL, 'Angle of descent'), L(PC, 'Recognition of connection between slope and tan θ'), L(PC, 'Any right angled triangle')],
 'maths-2015-hl-p1-q7-c': [L(HPC, 'Value of x substituted')],
 'maths-2015-hl-p1-q7-d-i': [L(LPC, 'Some correct substitution'), L(HPC, 'Correct expansions')],
 'maths-2015-hl-p1-q7-d-ii': [L(SOL, 'Point of inflection: (−2·5, 0·075)'), L(S1 + LPC, 'Work leading to change in x -value or y -value'),
     L(S1 + HPC, 'Correct change in x and y values'),
     L(S2 + HPC, 'Effort at calculating mid-point')],
 'maths-2015-hl-p1-q8-a-i': [L(PC, 'One correct box')],
 'maths-2015-hl-p1-q8-a-ii': [L(PC, 'At least two points plotted'), L('No credit', 'Bar chart')],
 'maths-2015-hl-p1-q8-a-iii': [L(PC, 'Incomplete equation for volume'), L(PC, 'V = any function of t'), L(PC, 'Attempt at finding slope')],
 'maths-2015-hl-p1-q8-b-i': [L(PC, 'Correct volume formula'), L(PC, 'Converting mm to cm')],
 'maths-2015-hl-p1-q8-b-ii': [L(LPC, 'Mentions a relevant rate of change.'), L(MPC, 'Writing down chain rule.'),
     L(HPC, 'Substitution of values')],
 'maths-2015-hl-p1-q8-c': [L(S1 + LPC, 'Mentions relevant rate of change.'), L(S1 + HPC, 'States chain rule i.e. dA/dt = dA/dr dr/dt'),
     L(S2 + LPC, 'Effort to establish value of A'), L(S2 + HPC, 'A in terms of t'), L(NOTE, 'Must use calculus to get any credit.')],
 'maths-2015-hl-p1-q8-d': [L(LPC, 'r in centimetres'), L(LPC, 'Effort at expression of area'), L(HPC, 'Correct expression for time')],
 'maths-2015-hl-p1-q9-a': [L(SOL, '16 hours 50 minutes'), L(HPC, 'Correct substitution')],
 'maths-2015-hl-p1-q9-b': [L(SOL, '36 days after March 21 is April 26.'), L(HPC, 'Correct equation with t only'), L(NOTE, 'Accept 35 or 36 substituted correctly and tested.')],
 'maths-2015-hl-p1-q9-c': [L(PC, 'Any correct differentiation (note: ‘0’ could be correct differentiation here)'),
     L(NOTE, 'Substituting 180° for π ⇒ one error')],
 'maths-2015-hl-p1-q9-d': [L(SOL, '=17 hours'), L(LPC, 'f′(t) = 0'), L(MPC, 'Value of t'),
     L(NOTE, 'Accept 91 or 92 substituted and evaluated correctly for full marks.')],
 'maths-2015-hl-p1-q9-e': [L(SOL, '15 hours 15 minutes'), L(LPC, 'Correct expression in x or t'), L(LPC, 'Correct formula'), L(LPC, 'Correct limits'),
     L(MPC, 'Any correct integration'), L(HPC, 'Correct integration and effort at substitution'),
     L(NOTE, 'Integration with one error but finished correctly gets High Partial Credit.')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Filled from scheme_solution_figures.py's output once its crops are opened and checked.
SCHEME_ROW_FIGURES = {}

p = Paper(2015, 'hl', 'p1', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 4, 5], '10B': [0, 5, 10], '10C': [0, 4, 8, 10], '10D': [0, 2, 5, 8, 10],
                             '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15], '25E': [0, 5, 10, 15, 20, 25]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
ss = 'sequences-series'
ball = ('Mary threw a ball onto level ground from a height of 2 m. Each time the ball hit the ground it bounced back up to 3/4 of the height of the '
        'previous bounce, as shown.')
q1a = ('Complete the table below to show the maximum height, in fraction form, reached by the ball on each of the first four bounces. '
       'Table: Bounce: 0, 1, 2, 3, 4. Height (m): 2/1, _, _, _, _.')
A('1-a', 'Q1(a)', '5C', [7, 25], [3], '4-1', ss, q1a, stem=ball)
A('1-b', 'Q1(b)', '10C', [7, 25], [3], '4-1', ss, 'Find, in metres, the total vertical distance (up and down) the ball had travelled when it hit the ground for the 5th time. Give your answer in fraction form.',
  stem=ball + ' Part (a): ' + q1a)
A('1-c', 'Q1(c)', '10C', [8, 25], [3], '4-1', ss, 'If the ball were to continue to bounce indefinitely, find, in metres, the total vertical distance it would travel.', stem=ball)
A('2', 'Q2', '25E', [9, 26], [4], '4-2', 'algebra-cubics', 'Solve the equation x³ − 3x² − 9x + 11 = 0. Write any irrational solution in the form a + b√c, where a, b, c ∈ ℤ.')
fx = 'Let f(x) = −x² + 12x − 27, x ∈ ℝ.'
q3a = ('(i) Complete Table 1 below. Table 1: x: 3, 4, 5, 6, 7, 8, 9. f(x): 0, 5, _, _, 8, _, _. (ii) Use Table 1 and the trapezoidal rule to find '
       'the approximate area of the region bounded by the graph of f and the x-axis.')
A('3-a-i', 'Q3(a)(i),Q3(a)(ii)', '15D', [10, 27], [5], '3-4', 'area-volume,functions', q3a, stem=fx)
A('3-b-i', 'Q3(b)(i),Q3(b)(ii)', '10C', [10, 27], [5], '5-2', 'integration', '(i) Find ∫ (from 3 to 9) f(x) dx. (ii) Use your answers above to find the percentage error in your approximation of the area, correct to one decimal place.',
  stem=fx + ' Part (a): ' + q3a)
cx = 'complex-numbers'
A('4-a', 'Q4(a)', '15D', [11, 12, 28], [6], '4-4', cx, 'The complex numbers z₁, z₂ and z₃ are such that 2/z₁ = 1/z₂ + 1/z₃, z₂ = 2 + 3i and z₃ = 3 − 2i, where i² = −1. Write z₁ in the form a + bi, where a, b ∈ ℤ.')
A('4-b', 'Q4(b)', '10C', [12, 28], [6], '4-4', cx + ',' + ss, 'Let ω be a complex number such that ωⁿ = 1, ω ≠ 1, and S = 1 + ω + ω² + ⋯ + ω^(n−1). Use the formula for the sum of a finite geometric series to write the value of S in its simplest form.')
A('5-a', 'Q5(a)', '10C', [13, 29], [7], '4-2', 'algebra-solving-equations', 'Solve the equation x = √(x + 6), x ∈ ℝ.')
A('5-b', 'Q5(b)', '5B', [13, 29], [7], '5-2', 'differentiation-rules', 'Differentiate x − √(x + 6) with respect to x.')
A('5-c', 'Q5(c)', '10C', [13, 29], [7], '5-2', 'differentiation-applications', 'Find the co-ordinates of the turning point of the function y = x − √(x + 6), x ≥ −6.')
fm = 'financial-maths'
loan = 'Donagh is arranging a loan and is examining two different repayment options.'
A('6-a-i', 'Q6(a)(i),Q6(a)(ii)', '10C', [14, 30], [8], '3-3', fm, '(i) Bank A will charge him a monthly interest rate of 0·35%. Find, correct to three significant figures, the annual percentage rate (APR) that is equivalent to a monthly interest rate of 0·35%. (ii) Bank B will charge him a rate that is equivalent to an APR of 4·5%. Find, correct to three significant figures, the monthly interest rate that is equivalent to an APR of 4·5%.',
  stem=loan)
A('6-b', 'Q6(b)', '15C', [15, 30], [9], '3-3', fm + ',' + ss, 'Donagh borrowed €80 000 at a monthly interest rate of 0·35%, fixed for the term of the loan, from Bank A. The loan is to be repaid in equal monthly repayments over ten years. The first repayment is due one month after the loan is issued. Calculate, correct to the nearest euro, the amount of each monthly repayment.',
  stem=loan)
plane = ('A plane is flying horizontally at P at a height of 150 m above level ground when it begins its descent. P is 5 km, horizontally, from the '
         'point of touchdown O. The plane lands horizontally at O. Taking O as the origin, (x, f(x)) approximately describes the path of the plane’s '
         'descent where f(x) = 0·0024x³ + 0·018x² + cx + d, −5 ≤ x ≤ 0, and both x and f(x) are measured in km.')
q7bi = 'Find the value of f′(x), the derivative of f(x), when x = −4.'
q7c = 'Show that (−2·5, 0·075) is the point of inflection of the curve y = f(x).'
q7di = 'If (x, y) is a point on the curve y = f(x), verify that (−x − 5, −y + 0·15) is also a point on y = f(x).'
da = 'differentiation-applications'
A('7-a-i', 'Q7(a)(i)', '5B', [16, 31], [10], '5-1', 'functions', 'Show that d = 0.', stem=plane)
A('7-a-ii', 'Q7(a)(ii)', '5B', [16, 31], [10], '5-1', 'functions,' + da, 'Using the fact that P is the point (−5, 0·15), or otherwise, show that c = 0.', stem=plane)
A('7-b-i', 'Q7(b)(i)', '10C', [16, 31], [10], '5-2', 'differentiation-rules', q7bi, stem=plane, extra={'permittedMarks': [0, 3, 7, 10]})
A('7-b-ii', 'Q7(b)(ii)', '5B', [17, 31], [11], '5-2', da + ',trigonometry-triangles', 'Use your answer to part (b) (i) above to find the angle at which the plane is descending when it is 4 km from touchdown. Give your answer correct to the nearest degree.',
  stem=plane + ' Part (b)(i): ' + q7bi)
A('7-c', 'Q7(c)', '10D', [17, 31], [11], '5-2', da, q7c, stem=plane)
A('7-d-i', 'Q7(d)(i)', '5C', [17, 32], [11], '5-1', 'functions', q7di, stem=plane)
A('7-d-ii', 'Q7(d)(ii)', '10C', [17, 18, 32], [11], '2-2', 'co-ordinate-geometry-of-the-line,functions', 'Find the image of (−x − 5, −y + 0·15) under symmetry in the point of inflection.',
  stem=plane + ' Part (c): ' + q7c + ' Part (d)(i): ' + q7di)
oil = 'An oil-spill occurs off-shore in an area of calm water with no currents. The oil is spilling at a rate of 4 × 10⁶ cm³ per minute. The oil floats on top of the water.'
q8ai = ('Complete the table below to show the total volume of oil on the water after each of the first 6 minutes of the oil-spill. '
        'Table: Time (minutes): 1, 2, 3, 4, 5, 6. Volume (10⁶ cm³): _, 8, _, _, _, _.')
slick = oil + ' Part (b): The spilled oil forms a circular oil slick 1 millimetre thick.'
q8bi = 'Write an equation for the volume of oil in the slick, in cm³, when the radius is r cm.'
A('8-a-i', 'Q8(a)(i)', '5B', [19, 32], [12], '5-1', 'functions', q8ai, stem=oil)
A('8-a-ii', 'Q8(a)(ii)', '5B', [19, 32], [12], '5-1', 'functions', 'Draw a graph to show the total volume of oil on the water over the first 6 minutes.', stem=oil + ' Part (a)(i): ' + q8ai)
A('8-a-iii', 'Q8(a)(iii)', '5B', [19, 32], [12], '5-1', 'functions', 'Write an equation for V(t), the volume of oil on the water, in cm³, after t minutes.', stem=oil)
A('8-b-i', 'Q8(b)(i)', '5B', [19, 32], [12], '3-4', 'area-volume', q8bi, stem=slick)
A('8-b-ii', 'Q8(b)(ii)', '10D', [20, 33], [13], '5-2', da, 'Find the rate, in cm per minute, at which the radius of the oil slick is increasing when the radius is 50 m.',
  stem=slick + ' Part (b)(i): ' + q8bi)
A('8-c', 'Q8(c)', '10C', [20, 33], [13], '5-2', da, 'Show that the area of water covered by the oil slick is increasing at a constant rate of 4 × 10⁷ cm² per minute.', stem=slick)
A('8-d', 'Q8(d)', '10C', [20, 33], [13], '5-2', da + ',area-volume', 'The nearest land is 1 km from the point at which the oil-spill began. Find how long it will take for the oil slick to reach land. Give your answer correct to the nearest hour.',
  stem=slick)
tfi = 'trigonometry-functions-identities'
gal = ('The approximate length of the day in Galway, measured in hours from sunrise to sunset, may be calculated using the function '
       'f(t) = 12·25 + 4·75 sin(2π/365 t), where t is the number of days after March 21st and (2π/365 t) is expressed in radians.')
q9c = 'Find f′(t), the derivative of f(t).'
A('9-a', 'Q9(a)', '10C', [21, 34], [14], '2-3', tfi, 'Find the length of the day in Galway on June 5th (76 days after March 21st). Give your answer in hours and minutes, correct to the nearest minute.', stem=gal)
A('9-b', 'Q9(b)', '10C', [21, 34], [14], '2-3', tfi, 'Find a date on which the length of the day in Galway is approximately 15 hours.', stem=gal)
A('9-c', 'Q9(c)', '10B', [21, 34], [14], '5-2', 'differentiation-rules', q9c, stem=gal)
A('9-d', 'Q9(d)', '10D', [22, 34], [15], '5-2', da, 'Hence, or otherwise, find the length of the longest day in Galway.', stem=gal + ' Part (c): ' + q9c)
A('9-e', 'Q9(e)', '10D', [22, 34], [15], '5-2', 'integration', 'Use integration to find the average length of the day in Galway over the six months from March 21st to September 21st (184 days). Give your answer in hours and minutes, correct to the nearest minute.',
  stem=gal)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 50, '8': 50, '9': 50}
p.check(marks, 32)
p.review(marks,
    'Independent visual reading of all 16 question-paper pages and PDF pages 1–36 of the combined Higher Level scheme (cover, notes, contents, the Paper 1 model solutions on pages 5–22, the scale table on page 23, the summary of mark allocations on page 24, the Paper 1 detailed marking notes on pages 25–34, and the pages before Paper 2). Each task boundary is the published scale in the detailed marking notes, cross-checked against the printed summary.',
    list(range(1, 37)), [23, 24],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7–9, 50 marks each). Every question is retained.',
     '32 independently marked units, matching the printed summary of allocations on scheme page 24. Q3(a)(i)+(ii), Q3(b)(i)+(ii) and Q6(a)(i)+(ii) are each marked “combined” on one printed scale and are one task; Q2 has no parts and is one 25E task.',
     'Bands from the 2015 scale table on scheme page 23: 5B 0,2,5; 5C 0,2,4,5; 10B 0,5,10; 10C 0,4,8,10; 10D 0,2,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15; 25E 0,5,10,15,20,25. The marking notes print the same ladder beside every part except Q7(b)(i), whose notes print Scale 10C (0, 3, 7, 10); that card follows the notes. The summary prints Q9(e) as “10” without a letter; the notes print Scale 10D.',
     'This paper had no authored cards before this review; all 32 units are new. The 2015 scheme sets the paper out with a boxed model solution under each part (pages 5–22) and lists the credit bands separately as detailed marking notes (pages 25–34). The model solutions are equation images whose text layer is scattered digits, so only lines the text layer carries whole are quoted; the bands are quoted from the notes. A band whose maths the text layer garbles (a stacked fraction, an f(x) or x = 0 set as an equation object) is not quoted; Q7(a)(i)’s only band, “Recognises x = 0”, extracts as separate characters, so that card quotes its model solution’s conclusion and the band is carried by the crop.',
     'Every card carries the SEC’s own print of its scheme content, shown only after the reveal: the part’s boxed model solution above its detailed marking notes, cropped from the scheme PDF by scheme_solution_figures.py.',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 2); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 10], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [10, 15], 'wording': 'or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'otherwise' in t else None)
p.apply(ROWS, '2015 Higher Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
