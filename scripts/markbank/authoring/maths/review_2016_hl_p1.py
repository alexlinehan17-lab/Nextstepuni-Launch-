"""2016 HL Paper 1: a new paper — 35 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'
M1, M2, M3, M4, M5 = 'Method 1, ', 'Method 2, ', 'Method 3, ', 'Method 4, ', 'Method 5, '

ROWS = {
 'maths-2016-hl-p1-q1-a': [L(SOL, '−4 − 3i'), L(PC, 'real or imaginary part correct')],
 'maths-2016-hl-p1-q1-b': [L(SOL, 'r = √(1² + 1²) = √2 θ = π/4'), L(SOL, '(1 + i)⁸ = {√2 (cos π/4 + i sin π/4)}⁸'), L(SOL, '(1 + i)⁸ = {16(cos 2π + i sin 2π)}'), L(SOL, '(1 + i)⁸ = 16(1) = 16'),
     L(LPC, 'correct answer without use of De Moivre’s'), L(LPC, 'modulus or argument correct'), L(LPC, 'formula'), L(LPC, 'statement of De Moivre’s'),
     L(HPC, '16(cos 2π + i sin 2π)'), L(NOTE, 'not De Moivre and incorrect answer merits 0 marks')],
 'maths-2016-hl-p1-q1-c': [L(SOL, 'z = ((2 − i) ± √((−2 + i)² − 4(3 − i)))/2'), L(SOL, '= (2 − i ± 3i)/2'), L(SOL, '= 1 − 2i or 1 + i'), L(ALT, '1 + i + z₁ = 2 − i'),
     L(M1 + LPC, 'root formula with some substitution'), L(M1 + HPC, 'formula fully substituted'),
     L(M2 + LPC, 'equation rearranged'), L(M2 + HPC, 'correct substitution'),
     L(M3 + LPC, 'correct factor(s)'), L(M3 + HPC, 'identification of equal terms'),
     L(M4 + LPC, 'long division formulated correctly'), L(M4 + HPC, 'two correct lines in division'),
     L(M5 + LPC, 'correct multiplication'), L(M5 + LPC, 'substitution of (m + ni) into quadratic and stops'), L(M5 + HPC, 'identification of equal terms'),
     L(NOTE, 'substitution of (1 + i) merits 0 marks')],
 'maths-2016-hl-p1-q2-a': [L(SOL, 'x² − 8x + 16 ≥ 4'), L(SOL, 'x² − 8x + 12 ≥ 0'), L(SOL, '(x − 2)(x − 6) ≥ 0'), L(SOL, 'x = 2 x = 6'),
     L(ALT, 'x ≥ 6 ∪ x ≤ 2'), L(M1 + LPC, 'either side squared'), L(M1 + LPC, 'one correct linear inequality written'),
     L(M1 + LPC, 'stating range of natural numbers only'), L(M1 + HPC, 'correct solutions to quadratic'), L(FC, 'correct answer without work'),
     L(NOTE, 'use of natural numbers in range merits High Partial Credit at most'),
     L(M2 + LPC, 'any one straight line'), L(M2 + HPC, 'three straight lines')],
 'maths-2016-hl-p1-q2-b': [L(SOL, 'x = (−3y − 1)/2'), L(SOL, '11y² + 4y − 15 = 0'), L(SOL, '(11y + 15)(y − 1) = 0'), L(SOL, 'y = −15/11 or y = 1'), L(SOL, 'x = 17/11 or x = −2'), L(ALT, '11x² + 5x − 34 = 0'), L(ALT, '(11x − 17)(x + 2) = 0'),
     L(LPC, 'effort to isolate x (or y)'), L(HPC, 'fully correct substitution into quadratic')],
 'maths-2016-hl-p1-q3-a-i': [L(LPC, 'one entry correct'), L(HPC, '5 entries correct')],
 'maths-2016-hl-p1-q3-a-ii': [L(LPC, 'one plot correct'), L(HPC, '5 plots correct'), L(HPC, 'one correct graph'), L(HPC, 'no labelling'),
     L(NOTE, 'straight lines NOT acceptable'), L(NOTE, 'one clear label merits full credit'), L(NOTE, 'one ambiguous label merits High Partial Credit at most')],
 'maths-2016-hl-p1-q3-a-iii': [L(PC, 'point of intersection clearly indicated on graph, but value of x not stated')],
 'maths-2016-hl-p1-q3-b': [L(SOL, 'e^(2x) − e^x = 2'), L(SOL, '(e^x − 2)(e^x + 1) = 0'), L(SOL, 'e^x = 2 or e^x = −1'), L(SOL, 'x = ln 2 or x = 0·693'),
     L(ALT, 'Let y = e^x ⇒ y² − y − 2 = 0'), L(ALT, '⇒ y = 2 or y = −1 (not possible)'), L(ALT, 'y = e^x ⇒ e^x = 2'),
     L(M1 + LPC, 'substitution correct'), L(M1 + HPC, 'correct factors of quadratic'), L(M1 + HPC, 'root formula correctly substituted'),
     L(M2 + LPC, 'substitution correct'), L(M2 + HPC, 'root formula correctly substituted'),
     L(NOTE, 'oversimplification of equation (i.e. not treating as quadratic) merits Low Partial Credit at most')],
 'maths-2016-hl-p1-q4-a': [L(SOL, 'P1: 8¹ − 1 = 7 (divisible by 7)'), L(SOL, 'Pk: Assume 8^k − 1 is divisible by 7'), L(SOL, '8^k − 1 = 7M'),
     L(SOL, 'Pk+1: 8^(k+1) − 1 = 8(8^k) − 1'), L(SOL, '= 8(7M + 1) − 1'), L(SOL, '= 56M + 7'), L(SOL, '= 7(8M + 1)'), L(SOL, 'Pk+1 is divisible by 7'), L(SOL, 'So, Pk+1 true whenever Pk true.'),
     L(SOL, 'Since P1 true, then, by induction, Pn is true for all natural numbers ≥ 1'),
     L(LPC, 'P1 step'), L(MPC, 'Pk step'), L(MPC, 'Pk+1 step'), L(HPC, 'use of Pk step to prove Pk+1 step'),
     L(NOTE, 'accept P1 step, Pk step and Pk+1 step in any order')],
 'maths-2016-hl-p1-q4-b-i': [L(SOL, 'log_a 8/3 = log_a 8 − log_a 3'), L(SOL, '= log_a (2)³ − log_a 3'), L(SOL, '= 3 log_a 2 − log_a 3'), L(SOL, '= 3p − q'), L(LPC, 'log_a 8 − log_a 3'), L(HPC, 'log_a 8 = 3 log_a 2 (and/or = 3p)')],
 'maths-2016-hl-p1-q4-b-ii': [L(SOL, 'log_a 9a²/16 = log_a (3a)² − log_a (2)⁴'), L(SOL, '= 2 log_a 3 + 2 log_a a − 4 log_a 2'), L(SOL, '= 2q + 2(1) − 4p'), L(SOL, '= 2q + 2 − 4p'),
     L(LPC, 'log_a 9a² − log_a 16'), L(MPC, '2log_a 3'), L(MPC, '2 log_a a'), L(MPC, '4 log_a 2'), L(MPC, '4p or 2q or 2')],
 'maths-2016-hl-p1-q5-a-i': [L(SOL, '(5x − 9)² = (x − 1)² + (4x)²'), L(SOL, '8x² − 88x + 80 = 0'), L(SOL, 'x² − 11x + 10 = 0'), L(SOL, '(x − 1)(x − 10) = 0'),
     L(SOL, 'x = 1 or x = 10'), L(SOL, 'x = 10'), L(LPC, 'any use of Pythagoras'), L(MPC, 'fully correct substitution'), L(HPC, 'both roots correct')],
 'maths-2016-hl-p1-q5-a-ii': [L(SOL, 'Sides=9, 40, 41'), L(SOL, '9² + 40² = 41²'), L(SOL, '81 + 1600 = 1681'), L(SOL, '1681 = 1681'),
     L(PC, '9 or 40 or 41'), L(PC, 'using 1 or −10 from candidates work')],
 'maths-2016-hl-p1-q5-b-i': [L(SOL, 'Function is bijective if inverse exists'), L(SOL, 'f⁻¹(x) = (x + 2)/3'), L(SOL, '⇒ Function is injective.'), L(ALT, 'Horizontal line test.'),
     L(ALT, 'f(a) = f(b)'), L(ALT, '3a − 2 = 3b − 2'), L(ALT, '⟹ a = b'),
     L(PC, 'f⁻¹(x) written'), L(PC, 'f(x) drawn'), L(PC, 'f(a) = f(b)')],
 'maths-2016-hl-p1-q5-b-ii': [L(SOL, 'f(x) = 3x − 2'), L(SOL, 'f⁻¹(x) = (x + 2)/3'), L(PC, 'any relevant transpose')],
 'maths-2016-hl-p1-q6-a': [L(SOL, 'f(x + ℎ) − f(x) = (2x + 2ℎ + 4)² − (2x + 4)²'), L(SOL, '= 8x + 16'),
     L(ALT, 'f(x) = (2x + 4)² = 4x² + 16x + 16'), L(ALT, 'f(x + ℎ) = 4(x + ℎ)² + 16(x + ℎ) + 16'), L(ALT, '= 4x² + 8ℎx + 4ℎ² + 16x + 16ℎ + 16'),
     L(LPC, 'any f(x + ℎ)'), L(MPC, 'limit of (f(x+ℎ) − f(x))/ℎ'), L(HPC, 'limit of ((2x+2ℎ+4)² − (2x+4)²)/ℎ'),
     L(NOTE, 'omission of limit sign penalised once only'), L(NOTE, 'answer not from 1st Principles merits 0 marks')],
 'maths-2016-hl-p1-q6-b-i': [L(SOL, '= 0∙15'), L(LPC, 'any correct differentiation'), L(MPC, 'product rule applied'), L(HPC, 'correct differentiation'),
     L(NOTE, 'one penalty for calculator in wrong mode')],
 'maths-2016-hl-p1-q7-a-i': [L(SOL, 'v = 4/3 πr³ ⟹ dv/dr = 4πr²'), L(SOL, 'dv/dt = 250 cm³/s'), L(SOL, 'dr/dt = dr/dv . dv/dt'), L(SOL, 'dr/dt = 250/(4π400) = 5/(32π) cm/s'), L(LPC, 'work towards dv/dr or dv/dt or dr/dt'), L(HPC, 'correct expression for dr/dt')],
 'maths-2016-hl-p1-q7-a-ii': [L(SOL, 'a = 4πr² ⟹ da/dr = 8πr'), L(SOL, 'da/dt = da/dr . dr/dt = 8πr . 5/(32π)'), L(SOL, '= 5(20)/4'), L(SOL, '= 25 cm²/s'), L(LPC, 'work towards da/dr or da/dt'), L(HPC, 'correct expression for da/dt')],
 'maths-2016-hl-p1-q7-b-i': [L(SOL, '−x² + 10x = 0'), L(SOL, 'x(−x + 10) = 0'), L(SOL, 'x = 0 or x = 10'), L(LPC, 'quadratic equation formed'),
     L(LPC, 'gets x = 0 only'), L(HPC, 'quadratic factorised'), L(NOTE, 'f′(x) = 0 ⇒ 2x − 10 = 0 ⇒ x = 5 merits 0 marks')],
 'maths-2016-hl-p1-q7-b-ii': [L(SOL + ', limits 0 to 10', '1/(10 − 0) ∫ (−x² + 10x)dx'), L(SOL, '= 1/10 [(−1000/3 + 500) − 0]'), L(SOL, '= −100/3 + 50 = 50/3 m'), L(LPC, 'integration set up'), L(HPC, 'correct integration with some substitution')],
 'maths-2016-hl-p1-q8-a-i': [L(SOL, 'f(x) = −0∙274x² + 1∙193x + 3∙23'), L(SOL, 'f′(x) = −0∙548x + 1∙193 = 0'), L(SOL, 'x = 2∙177 m'),
     L(SOL, '= −1∙2986 + 2∙5972 + 3∙23'), L(SOL, '= 4·529 m'), L(ALT, '−0∙274(x² − 1193/274 x − 1615/137)'), L(ALT, '−0∙274(x − 1193/548)² + 4.5285'), L(ALT, 'Max Height = 4·529 m'),
     L(LPC, 'any correct differentiation'), L(LPC, 'effort made at completing square'), L(LPC, 'trial and error with more than one value of x tested'),
     L(HPC, 'x value correct'),
     L(NOTE, 'if correct answer by trial and error, must show points on each side of max point to be lower to earn full credit')],
 'maths-2016-hl-p1-q8-a-ii': [L(SOL, 'tan θ = −0∙548(4∙5)+1∙193'), L(SOL, 'tan θ = −1∙273'), L(SOL, 'θ = 51∙8° = 52°'), L(PC, 'tan'),
     L(NOTE, 'right angled triangles may appear in diagram given in equation')],
 'maths-2016-hl-p1-q8-a-iii': [L(SOL, 'Map A → C'), L(SOL, '(–0∙5, 2∙565) → (0, 2)'), L(SOL, '2·177— (−0·5) = 2·677'), L(SOL, '4·529 − 0·565 = 3·964'),
     L(SOL, '(2∙177, 4∙529) → (2∙677, 3∙964)'), L(PC, '(−0·5, 2·565) → (0, 2)')],
 'maths-2016-hl-p1-q8-a-iv': [L(SOL, 'g(x) = ax² + bx + c'), L(SOL, 'C(0, 2) ∈ g(x) => c = 2'), L(SOL, '3∙05=a(4∙5)² + b(4∙5)+2'),
     L(SOL, 'g′(x) = 2ax + b = 0'), L(SOL, 'g(x) = −0∙273x² + 1∙462x + 2'),
     L(ALT, 'g(x) = −0·274[(x − 2·677)²] + 3·964'),
     L(M1 + LPC, 'c value found'), L(M1 + LPC, 'relevant equation in a, b and/or c'), L(M1 + MPC, 'formulated correctly any two equations'),
     L(M1 + HPC, 'formulated correctly any three equations'), L(NOTE, 'ax² + bx + c not in an equation merits 0 marks'),
     L(M2 + LPC, 'equation of curve'), L(M2 + LPC, 'use of C'), L(M2 + MPC, 'using peak value'), L(M2 + HPC, 'value of a found')],
 'maths-2016-hl-p1-q8-b-i': [L(SOL, 'y = 4∙99087(42∙5 − 23∙8)^1∙81'), L(SOL, 'y = 1000'), L(SOL, 'y = 15∙9803(58∙2 − 3∙8)^1∙04'), L(SOL, 'y = 1020'),
     L(LPC, 'some relevant substitution into one formula'), L(MPC, 'one value of y found'), L(MPC, 'some relevant substitution into both formulas'),
     L(HPC, 'one value correct and some relevant substitution into second formula'), L(HPC, 'uses incorrect formula (once only)')],
 'maths-2016-hl-p1-q8-b-ii': [L(SOL, '1295 = 15∙9803(x − 3∙8)^1∙04'), L(SOL, '81·0373=(x − 3∙8)^1∙04= z^1∙04'), L(SOL, 'log z = log 81∙0373/1∙04'), L(SOL, 'z = 68∙4343 = (x − 3∙8)'), L(SOL, 'x = 72∙2343 = 72∙23 m'),
     L(PC, 'some relevant substitution into formula')],
 'maths-2016-hl-p1-q8-b-iii': [L(SOL, '1087 = 0∙11193(254 − 121∙84)^c'), L(SOL, '1087/0∙11193 = (132∙16)^c'), L(SOL, 'log 9711∙426 = c log 132∙16'), L(SOL, 'c = log 9711∙426/log 132∙16'), L(SOL, '= 1∙88'),
     L(LPC, 'some relevant substitution into formula'), L(HPC, 'fully correct substitution into formula')],
 'maths-2016-hl-p1-q9-a-i': [L(SOL, '4, 2, 1, 1/2, 1/4, 1/8, 1/16'), L(SOL, 'Sn = a(1 − r^n)/(1 − r)'), L(SOL, '= 7∙9375'), L(SOL, '−1/2^n = −1/128'), L(SOL, 'n = 7'), L(LPC, 'some listing of terms'), L(LPC, 'Sn formula'),
     L(HPC, 'listing of exactly 7 correct terms'), L(HPC, 'formula fully substituted')],
 'maths-2016-hl-p1-q9-a-ii': [L(SOL, '= 8'), L(LPC, 'S∞ formula'), L(HPC, 'formula fully substituted')],
 'maths-2016-hl-p1-q9-a-iii': [L(SOL, '(16/5, 8/5) or (3∙2, 1∙6)'), L(LPC, '2 extra entries correct in either row'), L(MPC, 'either row fully correct'), L(HPC, 'one co-ordinate correct'),
     L(NOTE, 'need to see S∞ correctly used to move beyond Mid Partial Credit'), L(NOTE, 'no S∞ merits Mid Partial Credit at most')],
 'maths-2016-hl-p1-q9-b-i': [L(SOL, 'G₅=Female,Male,Female,Female,Male'), L(PC, 'one correct entry')],
 'maths-2016-hl-p1-q9-b-ii': [L(SOL, 'G₆ = G₅ + G₄ = 5 + 3 = 8'), L(SOL, 'G₇ = G₆ + G₅ = 8 + 5 = 13'), L(LPC, 'G₆ = G₅ + G₄'), L(LPC, 'G₇ = G₆ + G₅'),
     L(LPC, 'G₇ or G₆ correct'), L(LPC, '8 and/or 13 without work'), L(HPC, 'correct substitution in both')],
 'maths-2016-hl-p1-q9-b-iii': [L(SOL, 'G₃ = ((1 + √5)³ − (1 − √5)³)/(2³√5)'), L(SOL, '(1 + √5)³ = (1 + 3√5 + 3√5² + √5³)'), L(SOL, '= 16 + 8√5'), L(SOL, '= 16 − 8√5'), L(SOL, '= 16/8 = 2 Q. E. D.'),
     L(PC, 'some correct substitution'), L(PC, 'using approximate value for √5'), L(PC, 'G₃ = 2'), L(PC, 'some effort at cubing'),
     L(NOTE, 'use of √5 as approximation, even if rounded off to 2 at end of work merits at most Partial Credit')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Filled from scheme_row_figures.py's output once its crops are opened and checked.
SCHEME_ROW_FIGURES = {
    'maths-2016-hl-p1-q1-c': 'maths-2016-HL-scheme-p008-i0',
    'maths-2016-hl-p1-q2-a': 'maths-2016-HL-scheme-p010-i0',
    'maths-2016-hl-p1-q3-a-i': 'maths-2016-HL-scheme-p012-i0',
    'maths-2016-hl-p1-q3-a-ii': 'maths-2016-HL-scheme-p012-i1',
    'maths-2016-hl-p1-q3-a-iii': 'maths-2016-HL-scheme-p012-i2',
    'maths-2016-hl-p1-q4-b-ii': 'maths-2016-HL-scheme-p015-i0',
    'maths-2016-hl-p1-q6-a': 'maths-2016-HL-scheme-p017-i0',
    'maths-2016-hl-p1-q6-b-i': 'maths-2016-HL-scheme-p018-i0',
    'maths-2016-hl-p1-q7-b-ii': 'maths-2016-HL-scheme-p019-i0',
    'maths-2016-hl-p1-q8-a-iv': 'maths-2016-HL-scheme-p021-i0',
    'maths-2016-hl-p1-q9-a-i': 'maths-2016-HL-scheme-p023-i0',
    'maths-2016-hl-p1-q9-a-ii': 'maths-2016-HL-scheme-p023-i1',
    'maths-2016-hl-p1-q9-a-iii': 'maths-2016-HL-scheme-p024-i0',
    'maths-2016-hl-p1-q9-b-iii': 'maths-2016-HL-scheme-p025-i0',
}

p = Paper(2016, 'hl', 'p1', {'5B': [0, 2, 5], '5C': [0, 2, 4, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 3, 7, 10], '10D': [0, 2, 5, 8, 10],
                             '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
cx = 'complex-numbers'
A('1-a', 'Q1(a)', '5B', [8], [3], '4-4', cx, '(−4 + 3i) is one root of the equation az² + bz + c = 0, where a, b, c ∈ ℝ, and i² = −1. Write the other root.')
A('1-b', 'Q1(b)', '10C', [8], [3], '4-4', cx, 'Use De Moivre’s Theorem to express (1 + i)⁸ in its simplest form.')
A('1-c', 'Q1(c)', '10C', [8, 9], [3], '4-4', cx + ',algebra-quadratics', '(1 + i) is a root of the equation z² + (−2 + i)z + 3 − i = 0. Find its other root in the form m + ni, where m, n ∈ ℝ, and i² = −1.')
A('2-a', 'Q2(a)', '10C', [10], [4], '4-3', 'algebra-inequalities', 'Find the range of values of x for which |x − 4| ≥ 2, where x ∈ ℝ.')
A('2-b', 'Q2(b)', '15C', [11], [4], '4-2', 'algebra-simultaneous-equations', 'Solve the simultaneous equations: x² + xy + 2y² = 4; 2x + 3y = −1.')
fg = 'f(x) = 2/e^x and g(x) = e^x − 1, where x ∈ ℝ.'
tab = 'x: 0, 0·5, 1, ln(4). f(x) = 2/e^x: _, _, _, _. g(x) = e^x − 1: _, _, _, _.'
q3ai = 'Complete the table below. Write your values correct to two decimal places where necessary. ' + tab
q3aii = 'In the grid on the right, use the table to draw the graphs of f(x) and g(x) in the domain 0 ≤ x ≤ ln(4). Label each graph clearly.'
A('3-a-i', 'Q3(a)(i)', '5C', [12], [5], '5-1', 'functions,indices-and-logs', q3ai, stem=fg)
A('3-a-ii', 'Q3(a)(ii)', '5C', [12], [5], '5-1', 'functions', q3aii, stem=fg + ' Part (a)(i): ' + q3ai)
A('3-a-iii', 'Q3(a)(iii)', '5B', [12], [5], '5-1', 'functions', 'Use your graphs to estimate the value of x for which f(x) = g(x).', stem=fg + ' Part (a)(ii): ' + q3aii)
A('3-b', 'Q3(b)', '10C', [13], [5], '3-2', 'indices-and-logs,algebra-quadratics', 'Solve f(x) = g(x) using algebra.', stem=fg)
A('4-a', 'Q4(a)', '15D', [14], [6], '3-1', 'induction', 'Prove by induction that 8ⁿ − 1 is divisible by 7 for all n ∈ ℕ.')
logs = 'Given logₐ 2 = p and logₐ 3 = q, where a > 0, write each of the following in terms of p and q:'
A('4-b-i', 'Q4(b)(i)', '5C', [15], [7], '3-2', 'indices-and-logs', 'logₐ (8/3)', stem=logs)
A('4-b-ii', 'Q4(b)(ii)', '5D', [15], [7], '3-2', 'indices-and-logs', 'logₐ (9a²/16).', stem=logs)
tri = 'The lengths of the sides of a right-angled triangle are given by the expressions x − 1, 4x, and 5x − 9, as shown in the diagram.'
A('5-a-i', 'Q5(a)(i)', '10D', [16], [8], '4-2', 'algebra-quadratics,geometry', tri + ' Find the value of x.')
A('5-a-ii', 'Q5(a)(ii)', '5B', [16], [8], '4-2', 'algebra-quadratics,geometry', 'Verify, with this value of x, that the lengths of the sides of the triangle above form a pythagorean triple.',
  stem=tri + ' Part (a)(i): Find the value of x.')
A('5-b-i', 'Q5(b)(i)', '5B', [16], [9], '5-1', 'functions', 'Show that f(x) = 3x − 2, where x ∈ ℝ, is an injective function.')
A('5-b-ii', 'Q5(b)(ii)', '5B', [16], [9], '5-1', 'functions', 'Given that f(x) = 3x − 2, where x ∈ ℝ, find a formula for f⁻¹, the inverse function of f. Show your work.')
A('6-a', 'Q6(a)', '10D', [17], [10], '5-2', 'differentiation-rules', 'Differentiate the function (2x + 4)² from first principles, with respect to x.')
A('6-b-i', 'Q6(b)(i),Q6(b)(ii)', '15D', [18], [10, 11], '5-2', 'differentiation-rules,differentiation-applications',
  '(i) If y = x sin(1/x), find dy/dx. (ii) Find the slope of the tangent to the curve y = x sin(1/x), when x = 4/π. Give your answer correct to two decimal places.')
da = 'differentiation-applications'
air = 'Air is pumped into a spherical exercise ball at the rate of 250 cm³ per second.'
q7ai = 'Find the rate at which the radius is increasing when the radius of the ball is 20 cm. Give your answer in terms of π.'
A('7-a-i', 'Q7(a)(i)', '10C', [19], [12], '5-2', da, air + ' ' + q7ai)
A('7-a-ii', 'Q7(a)(ii)', '10C', [19], [12], '5-2', da, 'Find the rate at which the surface area of the ball is increasing when the radius of the ball is 20 cm.',
  stem=air + ' Part (a)(i): ' + q7ai)
kick = ('The inflated ball is kicked into the air from a point O on the ground. Taking O as the origin, (x, f(x)) approximately describes the path '
        'followed by the ball in the air, where f(x) = −x² + 10x and both x and f(x) are measured in metres.')
A('7-b-i', 'Q7(b)(i)', '10C', [19], [13], '5-1', 'functions,algebra-quadratics', 'Find the values of x when the ball is on the ground.', stem=kick)
A('7-b-ii', 'Q7(b)(ii)', '10C', [19], [13], '5-2', 'integration', 'Find the average height of the ball above the ground, during the interval from when it is kicked until it hits the ground again.',
  stem=kick + ' Part (b)(i): Find the values of x when the ball is on the ground.')
sarah = ('The diagram shows Sarah’s first throw at the basket in a basketball game. The ball left her hands at A and entered the basket at B. '
         'Using the co-ordinate plane with A(−0·5, 2·565) and B(4·5, 3·05), the equation of the path of the centre of the ball is '
         'f(x) = −0·274x² + 1·193x + 3·23, where both x and f(x) are measured in metres.')
q8ai = 'Find the maximum height reached by the centre of the ball, correct to three decimal places.'
q8aiii = ('Sarah took a second throw. This throw followed the path of the parabola g(x) as shown. The ball left Sarah’s hands at the point C(0, 2). '
          'The graph y = g(x) is the image of the graph y = f(x) under the translation which maps A onto C. Using your result from part a(i), show that '
          'the centre of this ball reached its maximum height at the point (2·677, 3·964), correct to three decimal places.')
A('8-a-i', 'Q8(a)(i)', '10C', [20], [14], '5-2', da, q8ai, stem=sarah)
A('8-a-ii', 'Q8(a)(ii)', '5B', [20], [14], '5-2', da + ',trigonometry-triangles', 'Find the acute angle to the horizontal at which the ball entered the basket. Give your answer correct to the nearest degree.', stem=sarah)
A('8-a-iii', 'Q8(a)(iii)', '5B', [20], [15], '5-1', 'functions', q8aiii, stem=sarah + ' Part (a)(i): ' + q8ai)
A('8-a-iv', 'Q8(a)(iv)', '10D', [21], [15], '5-1', 'functions,algebra-simultaneous-equations', 'Hence, or otherwise, find the equation of the parabola g(x).',
  stem=sarah + ' Part (a)(iii): ' + q8aiii)
hep = ('The heptathlon is an Olympic competition. It consists of seven events including the 200 m race and the javelin. The scoring system uses '
       'formulas to calculate a score for each event. The table below shows the formulas for two of the events and the values of constants used in '
       'these formulas, where x is the time taken (in seconds) or distance achieved (in metres) by the competitor and y is the number of points scored '
       'in the event. Table: Event, x, Formula, a, b, c. 200 m race, Time (s), y = a(b − x)^c, 4·99087, 42·5, 1·81. '
       'Javelin, Distance (m), y = a(x − b)^c, 15·9803, 3·8, 1·04.')
il = 'indices-and-logs'
A('8-b-i', 'Q8(b)(i)', '10D', [22], [16], '3-2', il + ',functions', 'In the heptathlon, Jessica ran 200 m in 23·8 s and threw the javelin 58·2 m. Use the formulas in the table to find the number of points she scored in each of these events, correct to the nearest point.', stem=hep)
A('8-b-ii', 'Q8(b)(ii)', '5B', [22], [16], '3-2', il, 'The world record distance for the javelin, in the heptathlon, would merit a score of 1295 points. Find the world record distance for the javelin, in the heptathlon, correct to two decimal places.', stem=hep)
A('8-b-iii', 'Q8(b)(iii)', '10C', [22], [17], '3-2', il, 'The formula used to calculate the points for the 800 m race, in the heptathlon, is the same formula used for the 200 m race but with different constants. Jessica ran the 800 m race in 2 minutes and 1·84 seconds which merited 1087 points. If a = 0·11193 and b = 254 for the 800 m race, find the value of c for this event, correct to two decimal places.', stem=hep)
ss = 'sequences-series'
pat = ('At the first stage of a pattern, a point moves 4 units from the origin in the positive direction along the x-axis. For the second stage, it '
       'turns left and moves 2 units parallel to the y-axis. For the third stage, it turns left and moves 1 unit parallel to the x-axis. At each stage, '
       'after the first one, the point turns left and moves half the distance of the previous stage, as shown.')
A('9-a-i', 'Q9(a)(i)', '10C', [23], [18], '4-1', ss, 'How many stages has the point completed when the total distance it has travelled, along its path, is 7·9375 units?', stem=pat)
A('9-a-ii', 'Q9(a)(ii)', '10C', [23], [18], '4-1', ss, 'Find the maximum distance the point can move, along its path, if it continues in this pattern indefinitely.', stem=pat)
A('9-a-iii', 'Q9(a)(iii)', '15D', [24], [19], '4-1', ss + ',co-ordinate-geometry-of-the-line',
  'Complete the second row of the table below showing the changes to the x co-ordinate, the first nine times the point moves to a new position. '
  'Hence, or otherwise, find the x co-ordinate and the y co-ordinate of the final position that the point is approaching, if it continues indefinitely in this pattern. '
  'Table: Stage: 1st, 2nd, 3rd, 4th, 5th, 6th, 7th, 8th, 9th. Change in x: +4, 0, –1, _, _, _, _, _, _. Change in y: _, _, _, _, _, _, _, _, _.', stem=pat)
bee = ('A male bee comes from an unfertilised egg, i.e. he has a female parent but he does not have a male parent. A female bee comes from a fertilised '
       'egg, i.e. she has a female parent and a male parent.')
q9bii = ('The number of ancestors of this bee in each generation can be calculated by the formula Gₙ₊₂ = Gₙ₊₁ + Gₙ, where G₁ = 1 and G₂ = 1, as in the '
         'diagram. Use this formula to calculate the number of ancestors in G₆ and in G₇.')
A('9-b-i', 'Q9(b)(i)', '5B', [24], [20], '4-1', ss, 'The following diagram shows the ancestors of a certain male bee. We identify his generation as G₁ and our diagram goes back to G₄. Continue the diagram to G₅.', stem=bee)
A('9-b-ii', 'Q9(b)(ii)', '10C', [24], [20], '4-1', ss, q9bii, stem=bee)
A('9-b-iii', 'Q9(b)(iii)', '5B', [25], [20], '4-1', ss + ',indices-and-logs', 'The number of ancestors in each generation can also be calculated by using the formula '
  'Gₙ = ((1 + √5)ⁿ − (1 − √5)ⁿ)/(2ⁿ√5). Use this formula to verify the number of ancestors in G₃.', stem=bee + ' Part (b)(ii): ' + q9bii)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 40, '8': 55, '9': 55}
p.check(marks, 35)
p.review(marks,
    'Independent visual reading of all 24 question-paper pages and PDF pages 1–26 of the combined Higher Level scheme (cover, notes, contents, the Paper 1 title page 5, the scale table on page 6, the summary of mark allocations on page 7, every Paper 1 model solution and marking note on pages 8–25, and the blank page 26). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 27)), [6, 7],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 40 marks, Q8 55 marks, Q9 55 marks). Every question is retained.',
     '35 independently marked units, matching the printed summary of allocations on scheme page 7. Q6(b)(i)+(ii) share one printed scale (15D) and are one task.',
     'Bands from the 2016 scale table on scheme page 6: 5B 0,2,5; 5C 0,2,4,5; 5D 0,2,3,4,5; 10C 0,3,7,10; 10D 0,2,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 35 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced. Exponents written as letters use caret notation (e^x, 8^k, (x − 3·8)^1·04), stacked fractions are written a/b, and the scheme’s italic h is written ℎ. Q4(b)(ii)’s high partial credit prints log_a a, whose doubled italic a the text layer collapses, so it is not quoted.',
     'Fourteen parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because their model solution is printed as an image or a layout the text layer cannot carry (the Q2(a) graphs, the Q3(a) table and graphs, the Q1(c) long division, the first-principles and integral layouts, the Q9(a) table) or a credit band could not be quoted: Q1(c) (both pages), Q2(a), Q3(a)(i), Q3(a)(ii), Q3(a)(iii), Q4(b)(ii), Q6(a), Q6(b)(i)+(ii), Q7(b)(ii), Q8(a)(iv), Q9(a)(i), Q9(a)(ii), Q9(a)(iii) and Q9(b)(iii).',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 12], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [15, 19], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2016 Higher Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
