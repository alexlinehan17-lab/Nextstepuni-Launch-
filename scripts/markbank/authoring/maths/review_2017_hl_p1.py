"""2017 HL Paper 1: a new paper — 33 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'

ROWS = {
 'maths-2017-hl-p1-q1-a': [L(SOL, '2(x² − 7/2 x − 5)'), L(SOL, '= 2((x − 7/4)² − 129/16)'), L(SOL, '= 2((x − 7/4)²) − 129/8'),
     L(LPC, 'a = 2 identified explicitly or as factor'), L(MPC, 'Completed square'), L(HPC, 'ℎ or k identified from work')],
 'maths-2017-hl-p1-q1-b': [L(SOL, '(7/4, −129/8)'), L(PC, 'One relevant co-ordinate identified')],
 'maths-2017-hl-p1-q1-c-i': [L(SOL, 'f(x) has min point as a > 0'), L(SOL, 'y co-ordinate of min < 0 ⇒ graph must cut x-axis twice hence two real roots.'),
     L(ALT, 'b² − 4ac = 49 + 80 > 0'), L(ALT, 'Therefore real roots'), L(PC, 'Mention of a > 0'), L(PC, 'b² − 4ac'),
     L(PC, 'Identifies location of one or two roots, e.g. between 4 and 5.')],
 'maths-2017-hl-p1-q1-c-ii': [L(SOL, '2x² − 7x − 10 = 0'), L(SOL, '(x − 7/4)² = 129/16'), L(SOL, 'x − 7/4 = ± √129/4'),
     L(SOL, 'x = 7/4 ± √(129/16)'), L(ALT, 'x = 7/4 ± √(129/16)'),
     L(LPC, 'Formula with some substitution'), L(LPC, 'Equation rewritten with some transpose'), L(HPC, 'x − 7/4 = ± √129/4 or equivalent')],
 'maths-2017-hl-p1-q2-a': [L(SOL, 'z = 2(cos 5π/6 + i sin 5π/6)'), L(SOL, 'z⁴ = (2(cos 5π/6 + i sin 5π/6))⁴'), L(SOL, 'z⁴ = 16(cos 10π/3 + i sin 10π/3)'),
     L(SOL, '= −8 − 8√3i'), L(LPC, 'θ or |z| found'), L(MPC, 'z written in polar form'), L(HPC, 'De Moivre’s Theorem applied correctly'),
     L(NOTE, 'Not using De Moivre: Low partial credit for fully correct work')],
 'maths-2017-hl-p1-q2-b': [L(SOL, 'w = 3(cos30 + i sin30)'), L(SOL, 'zw = 2(cos 5π/6 + i sin 5π/6) × 3(cos π/6 + i sin π/6)'), L(SOL, 'zw = 6(cos π + i sin π)'),
     L(SOL, '= 6(−1 + 0i)'), L(SOL, '= −6'), L(ALT, 'w = a + bi'), L(ALT, 'a² + b² = 9'), L(ALT, 'b/3 = sin 30° = 1/2'), L(ALT, 'a² = 27/4'), L(ALT, 'w = a + bi = 3√3/2 + 3/2 i'), L(ALT, 'zw = (−√3 + i)(3√3/2 + 3/2 i)'),
     L(LPC, 'Work towards w in Cartesian or polar form'), L(MPC, 'zw expressed as a product'), L(HPC, 'zw in Cartesian or polar form')],
 'maths-2017-hl-p1-q3-a': [L(SOL, 'f(x + ℎ) = 1/3 (x + ℎ)² − (x + ℎ) + 3'), L(SOL, 'f(x) = 1/3 x² − x + 3'), L(SOL, 'f(x + ℎ) − f(x) = 2xℎ/3 + ℎ²/3 − ℎ'),
     L(SOL, '(f(x + ℎ) − f(x))/ℎ = 2x/3 + ℎ/3 − 1'), L(SOL, 'lim ℎ→0 (f(x + ℎ) − f(x))/ℎ = 2x/3 − 1'), L(LPC, 'any f(x + ℎ)'),
     L(MPC, 'f(x + ℎ) − f(x) with some correct work'), L(HPC, '(1/3(x + ℎ)² − (x + ℎ) + 3 − (x²/3 − x + 3))/ℎ simplified'),
     L(NOTE, 'omission of limit sign penalised once only'), L(NOTE, 'answer not from 1st Principles merits 0 marks')],
 'maths-2017-hl-p1-q3-b': [L(SOL, '= 0·372'),
     L(ALT, 'f(x) = ln(3x² + 2)'), L(ALT, 'g(x) = (x + 5)'), L(ALT, 'f[g(x)] = ln[3(x + 5)² + 2]'), L(ALT, '= ln(3x² + 30x + 77)'),
     L(ALT, 'f′(x) = (6x + 30)/(3x² + 30x + 77)'), L(ALT, 'x = 1/4: f′(x) = 31·5/84·6875 = 0·3719'), L(ALT, '= 0·372'),
     L(LPC, 'Any correct differentiation'), L(LPC, 'fg(x) formulated'), 
     L(NOTE, 'Work with f(x) × g(x) merits low partial credit at most')],
 'maths-2017-hl-p1-q4-a': [L(SOL, 'r = 42·75/95 = 9/20'), L(SOL, 'Tn = ar^(n−1) < 0·01'), L(SOL, '95(9/20)^(n−1) < 0·01'), L(SOL, '(9/20)^(n−1) < 0·01/95'),
     L(SOL, '(n − 1) log(9/20) < log(0.01/95)'), L(SOL, '(n − 1) > log(0.01/95)/log(9/20)'), L(SOL, '(since log(9/20) is negative)'),
     L(SOL, 'n − 1 > 11·47'), L(SOL, 'n > 12·47'), L(SOL, '12th day'), L(LPC, 'r found'), L(LPC, 'Tn of a GP with some substitution'),
     L(MPC, 'Inequality in n written'), L(HPC, 'Inequality in n simplified (log handled)'), L(FC, 'Accept n = 12·47')],
 'maths-2017-hl-p1-q4-b': [L(SOL, '4(2) + 4√2 + 4 + ⋯'), L(SOL, 'a = 8 r = 1/√2'), L(SOL, 'S∞ = a/(1 − r)'), L(SOL, 'S∞ = 8/(1 − 1/√2)'), L(SOL, 'S∞ = 8(1 + 1/√2)/(1/2)'), L(SOL, 'S∞ = 16 + 8√2'),
     L(LPC, 'length of one side of new square'), L(HPC, 'S∞ fully substituted'), L(HPC, 'Correct work with one side only')],
 'maths-2017-hl-p1-q5-a': [L(SOL, 'f(−3) = 2(−3)³ + 5(−3)² − 4(−3) − 3'), L(SOL, '= −54 + 45 + 12 − 3'), L(SOL, 'f(−3) = 0'), L(SOL, '⇒ (x + 3) is a factor'),
     L(SOL, 'f(x) = (x + 3)(2x² − x − 1)'), L(SOL, 'f(x) = (x + 3)(2x + 1)(x − 1)'), L(SOL, 'x = −3 x = −1/2 x = 1'), L(LPC, 'Shows f(−3) = 0'),
     L(HPC, 'quadratic factor of f(x) found'), L(NOTE, 'No remainder in division may be stated as reason for x = −3 as root')],
 'maths-2017-hl-p1-q5-b': [L(SOL, 'y = 2x³ + 5x² − 4x − 3'), L(SOL, 'dy/dx = 6x² + 10x − 4 = 0'), L(SOL, '3x² + 5x − 2 = 0'), L(SOL, '(x + 2)(3x − 1) = 0'),
     L(SOL, '3x − 1 = 0 x + 2 = 0'), L(SOL, 'x = 1/3 x = −2'), L(SOL, 'f(1/3) = −100/27 f(−2) = 9'), L(SOL, 'Max = (−2, 9) Min = (1/3, −100/27)'),
     L(LPC, 'dy/dx found (Some correct differentiation)'), L(HPC, 'roots and one y value found'),
     L(NOTE, 'One of Max/Min must be identified for full credit')],
 'maths-2017-hl-p1-q5-c': [L(SOL, 'a > 100/27 or a < −9'), L(PC, 'one value identified'), L(PC, 'no range identified (from 2 values)')],
 'maths-2017-hl-p1-q6-a': [L(SOL, 'g(x) = e^x ℎ(x) = e^(−x) = 1/e^x'), L(SOL + ', g(x) for x from 0 to 1', '1 1·22 1·49 1·82 2·23 2·72'),
     L(SOL + ', h(x) for x from 0 to 1', '1 0·82 0·67 0·55 0·45 0·37'), L(LPC, 'one point correct'), L(HPC, 'Graph not in required domain')],
 'maths-2017-hl-p1-q6-b': [L(SOL, '= e^x + e^(−x)'), L(SOL, 'e^0·75 + e^(−0·75) − [e^0 + e^0]'), L(SOL, '= 0·5894'),
     L(LPC, 'Formulates integration for area under one curve with limits'), L(HPC, 'integrates twice for correct area under both curves'),
     L(NOTE, 'Trapezoidal rule must have at least 5 divisions AND fully correct work gets Low Partial Credit')],
 'maths-2017-hl-p1-q7-a': [L(SOL, 'Se^(·1(0)) × 10⁶ = 1100000'), L(SOL, 'S = 1·1'), L(PC, 'equation in S with substitution')],
 'maths-2017-hl-p1-q7-b': [L(SOL, 'p(5) = 1·1e^(0·1(5)) × 10⁶'), L(SOL, '= 1·813593 × 10⁶'), L(SOL, '= 1813593'), L(PC, 'substitution into formula for p(5)')],
 'maths-2017-hl-p1-q7-c': [L(SOL, 'p(6) = 1·1e^0·6 × 10⁶'), L(SOL, 'p(5) = 1·1e^0·5 × 10⁶'), L(SOL, 'p(6) − p(5) = (1·1e^0·6 − 1·1e^0·5) × 10⁶'),
     L(SOL, '= 0·1907372 × 10⁶'), L(SOL, '= 190737'), L(LPC, 'substitution into formula for p(6)'), L(LPC, 'use of p(5) from previous part'),
     L(LPC, 'p(6) − p(5) written or implied'), L(HPC, 'Formulates p(6) − p(5) with some substitution')],
 'maths-2017-hl-p1-q7-d': [L(SOL, 'q(t) = 3·9e^(kt) × 10⁶'), L(SOL, '3709795 = 3·9e^k × 10⁶'), L(SOL, '3·709795/3·9 = e^k'), L(SOL, 'log_e (3·709795/3·9) = k'),
     L(SOL, 'k = −0·0499 = −0·05'), L(LPC, 'Either substitution into formula for k'), L(LPC, 'Verifies k value only.'), L(HPC, 'relevant equation in k')],
 'maths-2017-hl-p1-q7-e': [L(SOL, 'p(t) = q(t)'), L(SOL, '1·1e^(0·1t) × 10⁶ = 3·9e^(−0·05t) × 10⁶'), L(SOL, '1·1e^(0·1t) = 3·9e^(−0·05t)'),
     L(SOL, 'e^(0·1t)/e^(−0·05t) = 3·9/1·1'), L(SOL, 'e^(0·15t) = 39/11'), L(SOL, 'ln 39/11 = 0·15t'), L(SOL, 't = 8·44 years'),
     L(SOL, 'In 2018 both populations equal'), L(LPC, 'p(t) = q(t) written or implied'), L(HPC, 'relevant equation in t')],
 'maths-2017-hl-p1-q7-f': [L(SOL, '2·743694 × 10⁶'), L(SOL, '2743694'), L(LPC, 'integral formulated (with limits)'), L(HPC, 'integration with full substitution')],
 'maths-2017-hl-p1-q7-g': [L(SOL, 'q(t) = 3.9e^(−0.05t) × 10⁶'), L(SOL, 'q′(t) = −0·05(3·9e^(−0·05t) × 10⁶)'), L(SOL, 'q′(8) = −0·05(3·9e^(−0·05(8)) × 10⁶)'),
     L(SOL, '= −130712'), L(LPC, 'q′(t)'), L(HPC, 'q′(t) fully substituted')],
 'maths-2017-hl-p1-q8-a': [L(LPC, 'P = A/(1 + i)'), L(LPC, 'A = P(1 + i)'), L(LPC, 'Sn formula with some substitution'),
     L(HPC, 'full substitution for P (or A) into Sn formula.')],
 'maths-2017-hl-p1-q8-b-i': [L(SOL, '2·5% × 5000 = 125'), L(PC, 'Any one unknown')],
 'maths-2017-hl-p1-q8-b-ii': [L(SOL, '(1 + i)^(1/12) = (1·2175)^(1/12) = 1·016535'), L(SOL, 'Rate = 1·65%'), L(PC, 'Formula with some substitution')],
 'maths-2017-hl-p1-q8-b-iii': [L(SOL, '1, 125, 82·50, 42·50, 4957·50'), L(SOL, '2, 125, 81·80, 43·20, 4914·30'), L(SOL, '3, 125, 81·09, 43·91, 4870·39'),
     L(LPC, 'One correct additional entry'), L(HPC, '6 correct additional entries'),
     L(NOTE, 'Where interest rate in b(ii) is not 1·65%, then check the validity of all values given.')],
 'maths-2017-hl-p1-q8-b-iv': [L(SOL, 'A[(1 + i)^t − 1] = pi(1 + i)^t'), L(SOL, 'A(1 + i)^t − A = pi(1 + i)^t'), L(SOL, 'A = (1 + i)^t[A − pi]'),
     L(SOL, '125/42·5 = (1·0165)^t'), L(SOL, 'log(125/42·5) = t log(1·0165)'), L(SOL, 't = 65·920'), L(SOL, 't = 66 months'),
     L(ALT, '50(1·0165^t − 1) = 33(1·0165^t)'), L(ALT, '1·0165^t(17) = 50'), L(ALT, '1·0165^t = 50/17'), L(ALT, 't log 1·0165 = log 50/17'),
     L(LPC, 'Formula with some substitution'), L(LPC, 'Some relevant manipulation of formula.'), L(HPC, 'Equation in t (t no longer an index)')],
 'maths-2017-hl-p1-q8-b-v': [L(SOL, '= €36·16'), L(ALT, 'Weekly interest rate (1 + i)⁵² = 1·085'), L(ALT, '1 + i = 1·00157'), L(ALT, 'i = 0·00157'),
     L(ALT, 'A = 5000(0·00157)(1·00157)¹⁵⁶/((1·00157)¹⁵⁶ − 1)'), L(LPC, 'r (weekly) found'), L(HPC, 'Fully substituted equation')],
 'maths-2017-hl-p1-q8-b-vi': [L(SOL, '125 × 66 − (36·16)(156)'), L(SOL, '=€2609·04'), L(PC, 'Total repayment by either method found')],
 'maths-2017-hl-p1-q9-a': [L(LPC, 'Vertical axis drawn'), L(LPC, 'Horizontal axis drawn.'), L(HPC, 'Horizontal axis fully scaled and positioned OR'),
     L(HPC, 'Vertical axis fully scaled\nUse relevant portions of axes'), L(NOTE, 'P can be on vertical axis')],
 'maths-2017-hl-p1-q9-b-i': [L(SOL, 'f(t) = a + b cos ct'), L(SOL, 'Range: [(a + b), (a − b)]'), L(SOL, 'a + b = 5·5 a − b = 1·7'), L(SOL, 'a = 3·6 b = 1·9'),
     L(LPC, 'one equation in a and b'), L(LPC, 'Range in terms of a and b'), L(HPC, 'a or b found'), L(NOTE, 'Accept correct answer without work')],
 'maths-2017-hl-p1-q9-b-ii': [L(SOL, 'Time between two successive high tides is: 12 34/60 hours'), L(SOL, 'period = 12 34/60'), L(SOL, 'period = 2π/c'), L(LPC, 'Period identified or 2π/c or 12·34'), L(HPC, 'equation in c with some substitution')],
 'maths-2017-hl-p1-q9-c': [L(SOL, '5·2 = a + b cos ct'), L(SOL, '5·2 = 3·6 + 1·9 cos 0·5t'), L(SOL, '0·5t = cos⁻¹(1·6/1·9) = 0·569621319'), L(SOL, '0·5t = 0·5696'),
     L(SOL, 't = 1·139 hours'), L(SOL, '(before and after high tide at 14:34)'), L(SOL, 'Time = 1 hour 8 minutes'), L(SOL, 'Times: (14:34) ± 1 hour 8 min'),
     L(SOL, '⇒ 13:26 and 15:42'), L(LPC, 'equation with some substitution'), L(HPC, 'solution for t'), L(NOTE, 'Low partial at most if formula not used')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Parts whose printed model solution is an image (the Q5(a) long division, the
# Q6(a) and Q6(b) graphs, the Q9(a) axes) or loses lines to the text layer (a
# stacked fraction's lone numerator or denominator filtered as a mark cell; the
# Q3(b) d(fg(x))/dx, whose f and g extract as unassigned code points) carry the
# SEC's own print of their scheme row (model solution and every credit band),
# shown only after the reveal. Crops: scheme_row_figures.py; ids are its output.
SCHEME_ROW_FIGURES = {
    'maths-2017-hl-p1-q1-c-ii': 'maths-2017-HL-scheme-p009-i0',
    'maths-2017-hl-p1-q3-b': 'maths-2017-HL-scheme-p012-i0',
    'maths-2017-hl-p1-q4-b': 'maths-2017-HL-scheme-p013-i0',
    'maths-2017-hl-p1-q5-a': 'maths-2017-HL-scheme-p014-i0',
    'maths-2017-hl-p1-q6-a': 'maths-2017-HL-scheme-p016-i0',
    'maths-2017-hl-p1-q6-b': 'maths-2017-HL-scheme-p017-i0',
    'maths-2017-hl-p1-q7-f': 'maths-2017-HL-scheme-p019-i0',
    'maths-2017-hl-p1-q8-a': 'maths-2017-HL-scheme-p020-i0',
    'maths-2017-hl-p1-q8-b-v': 'maths-2017-HL-scheme-p022-i0',
    'maths-2017-hl-p1-q9-a': 'maths-2017-HL-scheme-p023-i0',
    'maths-2017-hl-p1-q9-b-ii': 'maths-2017-HL-scheme-p024-i0',
}

p = Paper(2017, 'hl', 'p1', {'5B': [0, 3, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 4, 10], '10C': [0, 5, 8, 10],
                             '10D': [0, 4, 7, 8, 10], '15C': [0, 5, 10, 15], '15D': [0, 5, 8, 12, 15], '20C': [0, 10, 18, 20],
                             '20D': [0, 5, 14, 17, 20]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
q1a = 'Write the function f(x) = 2x² − 7x − 10, where x ∈ ℝ, in the form a(x + h)² + k, where a, h, and k ∈ ℚ.'
aq = 'algebra-quadratics'
A('1-a', 'Q1(a)', '5D', [8], [3], '4-2', aq, q1a)
A('1-b', 'Q1(b)', '10B', [8], [3], '5-1', 'functions,' + aq, 'Hence, write the minimum point of f.', stem='Part (a): ' + q1a)
A('1-c-i', 'Q1(c)(i)', '5B', [9], [3], '4-2', aq, 'Explain why f must have two real roots.', stem='Part (a): ' + q1a)
A('1-c-ii', 'Q1(c)(ii)', '5C', [9], [3], '4-2', aq, 'Write the roots of f(x) = 0 in the form p ± √q, where p and q ∈ ℚ.', stem='Part (a): ' + q1a)
zz = 'z = −√3 + i, where i² = −1.'
cx = 'complex-numbers'
A('2-a', 'Q2(a)', '15D', [10], [4], '4-4', cx, 'Use De Moivre’s Theorem to write z⁴ in the form a + b√c i, where a, b, and c ∈ ℤ.', stem=zz)
A('2-b', 'Q2(b)', '10D', [10, 11], [4], '4-4', cx, 'The complex number w is such that |w| = 3 and w makes an angle of 30° with the positive sense of the real axis. If t = zw, write t in its simplest form.', stem=zz)
A('3-a', 'Q3(a)', '20D', [12], [5], '5-2', 'differentiation-rules', 'Differentiate (1/3)x² − x + 3 from first principles with respect to x.')
A('3-b', 'Q3(b)', '5C', [12], [5], '5-2', 'differentiation-rules,functions,indices-and-logs', 'f(x) = ln(3x² + 2) and g(x) = x + 5, where x ∈ ℝ. Find the value of the derivative of f(g(x)) at x = 1/4. Give your answer correct to 3 decimal places.')
ss = 'sequences-series'
A('4-a', 'Q4(a)', '15D', [13], [6], '4-1', ss + ',indices-and-logs', 'The amount of a substance remaining in a solution reduces exponentially over time. An experiment measures the percentage of the substance remaining in the solution. The percentage is measured at the same time each day. The data collected over the first 4 days are given in the table below. Based on the data in the table, estimate which is the first day on which the percentage of the substance in the solution will be less than 0·01%. Day: 1, 2, 3, 4. Percentage of substance (%): 95, 42·75, 19·2375, 8·6569.')
A('4-b', 'Q4(b)', '10C', [13], [7], '4-1', ss, 'A square has sides of length 2 cm. The midpoints of the sides of this square are joined to form another square. This process is continued. The first three squares in the process are shown below. Find the sum of the perimeters of the squares if this process is continued indefinitely. Give your answer in the form a + b√c cm, where a, b, and c ∈ ℕ.')
cub = 'The function f is such that f(x) = 2x³ + 5x² − 4x − 3, where x ∈ ℝ.'
q5b = 'Find the co-ordinates of the local maximum point and the local minimum point of the function f.'
A('5-a', 'Q5(a)', '15C', [14], [8], '4-2', 'algebra-cubics', 'Show that x = −3 is a root of f(x) and find the other two roots.', stem=cub)
A('5-b', 'Q5(b)', '5C', [15], [8, 9], '5-2', 'differentiation-applications', q5b, stem=cub)
A('5-c', 'Q5(c)', '5B', [15], [8, 9], '5-1', 'functions,algebra-cubics', 'f(x) + a, where a is a constant, has only one real root. Find the range of possible values of a.', stem=cub + ' Part (b): ' + q5b)
gx = 'The graph of the function g(x) = e^x, x ∈ ℝ, 0 ≤ x ≤ 1, is shown on the diagram below.'
q6a = 'On the same diagram, draw the graph of h(x) = e^(−x), x ∈ ℝ, in the domain 0 ≤ x ≤ 1.'
A('6-a', 'Q6(a)', '15C', [16], [10], '5-1', 'functions', q6a, stem=gx)
A('6-b', 'Q6(b)', '10C', [17], [10, 11], '5-2', 'integration', 'Find the area enclosed by g(x) = e^x, h(x) = e^(−x), and the line x = 0·75. Give your answer correct to 4 decimal places.', stem=gx + ' Part (a): ' + q6a)
pop = 'Sometimes it is possible to predict the future population in a city using a function. The population in Sapphire City, over time, can be predicted using the following function: p(t) = Se^(0·1t) × 10⁶. The population in Avalon, over time, can be predicted using the following function: q(t) = 3·9e^(kt) × 10⁶. In the functions above, t is time, in years; t = 0 is the beginning of 2010; and both S and k are constants.'
q7a = 'The population in Sapphire City at the beginning of 2010 is 1 100 000 people. Find the value of S.'
q7d = 'The predicted population in Avalon at the beginning of 2011 is 3 709 795 people. Write down and solve an equation in k to show that k = −0·05, correct to 2 decimal places.'
il = 'indices-and-logs'
A('7-a', 'Q7(a)', '10B', [18], [12], '3-2', il, q7a, stem=pop)
A('7-b', 'Q7(b)', '10B', [18], [12], '3-2', il, 'Find the predicted population in Sapphire City at the beginning of 2015.', stem=pop + ' Part (a): ' + q7a)
A('7-c', 'Q7(c)', '5C', [18], [12], '3-2', il, 'Find the predicted change in the population in Sapphire City during 2015.', stem=pop + ' Part (a): ' + q7a)
A('7-d', 'Q7(d)', '15C', [19], [12, 13], '3-2', il, q7d, stem=pop)
A('7-e', 'Q7(e)', '5C', [19], [12, 13], '3-2', il, 'Find the year during which the populations in both cities will be equal.', stem=pop + ' Part (a): ' + q7a + ' Part (d): ' + q7d)
A('7-f', 'Q7(f)', '5C', [19], [12, 13], '5-2', 'integration', 'Find the predicted average population in Avalon from the beginning of 2010 to the beginning of 2025.', stem=pop + ' Part (d): ' + q7d)
A('7-g', 'Q7(g)', '5C', [19], [12, 14], '5-2', 'differentiation-applications', 'Use the function q(t) = 3·9e^(−0·05t) × 10⁶ to find the predicted rate of change of the population in Avalon at the beginning of 2018.', stem=pop)
fm = 'financial-maths'
q8a = 'When a loan of €P is repaid in equal repayments of amount €A, at the end of each of t equal periods of time, where i is the periodic compound interest rate (expressed as a decimal), the formula below can be used to find the amount of each repayment. A = P i(1 + i)^t/((1 + i)^t − 1).'
cc = 'Alex has a credit card debt of €5000. One method of clearing this debt is to make a fixed repayment at the end of each month. The amount of this repayment is 2·5% of the original debt.'
q8bi = 'What is the fixed monthly repayment, €A, required to pay the debt of €5000?'
q8bii = 'The annual percentage rate (APR) charged on debt by the credit card company is 21·75%, fixed for the term of the debt. Find as a percentage, correct to 3 significant figures, the monthly interest rate that is equivalent to an APR of 21·75%.'
q8bv = 'Alex decides to borrow €5000 from the local Credit Union to pay off this credit card debt of €5000. The APR charge for the Credit Union loan is 8·5% fixed for the term of the loan. The loan is to be repaid in equal weekly repayments, at the end of each week, for 156 weeks. Find the amount of each weekly repayment.'
A('8-a', 'Q8(a)', '5C', [20], [15], '3-3', fm + ',' + ss, q8a + ' Show how this formula is derived. You may use the formula for the sum of a finite geometric series.')
A('8-b-i', 'Q8(b)(i)', '10B', [20], [16], '3-3', fm, q8bi, stem=cc)
A('8-b-ii', 'Q8(b)(ii)', '10B', [20], [16], '3-3', fm, q8bii, stem=cc)
A('8-b-iii', 'Q8(b)(iii)', '10C', [20], [16], '3-3', fm, 'Assume Alex pays the fixed monthly repayment, €A, each month and does not have any further transactions on that card. Complete the table below to show how the balance of the debt of €5000 is reducing each month for the first three months, assuming an APR of 21·75%, charged and compounded monthly. Columns: Payment number; Fixed monthly payment, €A; Interest; Previous balance reduced by (€); New balance of debt (€). Payment 0: new balance 5000. Payment 1: _, _, 42·50, 4957·50. Payment 2: _, _, _, _. Payment 3: _, _, _, _.', stem=cc + ' Part (b)(i): ' + q8bi + ' Part (b)(ii): ' + q8bii)
A('8-b-iv', 'Q8(b)(iv)', '5C', [21], [15, 16], '3-3', fm, 'Using the formula you derived on the previous page, or otherwise, find how long it would take to pay off a credit card debt of €5000, using the repayment method outlined at the beginning of part (b) above. Give your answer in months, correct to the nearest month.', stem='Part (a): ' + q8a + ' Part (b): ' + cc + ' Part (b)(ii): ' + q8bii)
A('8-b-v', 'Q8(b)(v)', '10C', [22], [16, 17], '3-3', fm, q8bv, stem='Part (a): ' + q8a + ' Part (b): ' + cc)
A('8-b-vi', 'Q8(b)(vi)', '5B', [22], [16, 17], '3-3', fm, 'How much will Alex save by paying off the credit card debt using the loan from the Credit Union instead of paying the fixed repayment from part (b)(i) each month to the credit card company?', stem=cc + ' Part (b)(i): ' + q8bi + ' Part (b)(v): ' + q8bv)
tide = 'The depth of water, in metres, at a certain point in a harbour varies with the tide and can be modelled by a function of the form f(t) = a + b cos ct where t is the time in hours from the first high tide on a particular Saturday and a, b, and c are constants. (Note: ct is expressed in radians.) On that Saturday, the following were noted: The depth of the water in the harbour at high tide was 5·5 m; The depth of the water in the harbour at low tide was 1·7 m; High tide occurred at 02:00 and again at 14:34.'
tf = 'trigonometry-functions-identities'
A('9-a', 'Q9(a)', '20C', [23], [18], '2-3', tf, 'Use the information you are given to add, as accurately as you can, labelled and scaled axes to the diagram below to show the graph of f over a portion of that Saturday. The point P should represent the depth of the water in the harbour at high tide on that Saturday morning.', stem=tide)
A('9-b-i', 'Q9(b)(i)', '10C', [24], [18, 19], '2-3', tf, 'Find the value of a and the value of b.', stem=tide)
A('9-b-ii', 'Q9(b)(ii)', '5C', [24], [18, 19], '2-3', tf, 'Show that c = 0·5, correct to 1 decimal place.', stem=tide)
A('9-c', 'Q9(c)', '5C', [24], [18, 19], '2-3', tf, 'Use the equation f(t) = a + b cos ct to find the times on that Saturday afternoon when the depth of the water in the harbour was exactly 5·2 m. Give each answer correct to the nearest minute.', stem=tide + ' Part (b)(i): Find the value of a and the value of b. Part (b)(ii): Show that c = 0·5, correct to 1 decimal place.')

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 55, '9': 40}
p.check(marks, 33)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 1–25 of the combined Higher Level scheme (cover, notes, contents, the Paper 1 title page 5, the scale table on page 6, the summary of mark allocations on page 7, every Paper 1 model solution and marking note on pages 8–24, and the Paper 2 title page 25). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 26)), [6, 7],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 55 marks, Q9 40 marks). Every question is retained.',
     '33 independently marked units, matching the printed summary of allocations on scheme page 7.',
     'Paper 1 bands from the 2017 scale table on scheme page 6: 5B 0,3,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10B 0,4,10; 10C 0,5,8,10; 10D 0,4,7,8,10; 15C 0,5,10,15; 15D 0,5,8,12,15; 20C 0,10,18,20; 20D 0,5,14,17,20. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 33 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced. Exponents in prompts use caret notation (e^x, e^(−0·05t)). The Q2(b) model solution continues onto scheme page 11 and is quoted from both pages.',
     'Eleven parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because lines of their model solution cannot be carried by the text layer (a stacked fraction’s lone numerator or denominator, filtered as a mark cell) or are printed as images: Q1(c)(ii), Q3(b) (whose high partial credit d(fg(x))/dx extracts its f and g as unassigned code points and is not quoted), Q4(b), Q5(a) (the long division), Q6(a), Q6(b), Q7(f), Q8(a), Q8(b)(v), Q9(a) (the scaled graph) and Q9(b)(ii).',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 12], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [16], 'wording': 'Using the formula you derived on the previous page, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2017 Higher Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
