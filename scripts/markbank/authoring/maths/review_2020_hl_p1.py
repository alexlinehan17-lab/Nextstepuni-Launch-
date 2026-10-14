"""2020 HL Paper 1: a new paper — 36 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *
ALT = 'Model solution (alternative)'
NC = 'No Credit'

ROWS = {
 'maths-2020-hl-p1-q1-a-i': [L(SOL, 'f(−3) = 0'), L(SOL, 'f(−3) = −3² + 5(−3) + p = 0'), L(SOL, '9 − 15 + p = 0'), L(SOL, 'p = 6'),
     L(ALT, 'x² + 5x + p = (x + 3)(x + a)'), L(ALT, 'a + 3 = 5'), L(ALT, 'a = 2'), L(ALT, 'p = 3a'),
     L(LPC, 'Demonstrates understanding of x + 3 as factor or – 3 as root e.g. (x + 3), f(−3)'),
     L(HPC, 'Relevant equation in p (with p as only unknown)')],
 'maths-2020-hl-p1-q1-a-ii': [L(SOL, 'x² + 5x + p = (x − α)(x − α − 3)'), L(SOL, '−2α − 3 = 5'), L(SOL, 'α = −4'), L(SOL, 'p = 16 − 12'), L(SOL, 'p = 4'),
     L(ALT, 'α, α + 3 = roots'), L(ALT, 'α + α + 3 = −5'), L(ALT, 'and α + 3 = −1'), L(ALT, 'p = (−1)(−4) = 4'),
     L(LPC, 'Demonstrates understanding of 3 as difference of roots e.g. α with α ± 3'), L(LPC, 'x² − x(sum) + product = 0'),
     L(LPC, 'One correct value for p'), L(LPC, 'x² + 5x + p > 0'), L(LPC, 'Sketch of U-shaped quadratic with turning point above the x-axis'),
     L(HPC, 'Relevant equation in α (with α as only unknown)')],
 'maths-2020-hl-p1-q1-a-iii': [L(SOL, 'b² − 4ac < 0'), L(SOL, '5² − 4(1)(p) < 0'), L(SOL, '25 − 4p < 0'), L(SOL, '4p > 25'), L(SOL, 'p > 6·25'),
     L(SOL, 'p = 7 and p = 8'), L(LPC, 'b² − 4ac'), L(LPC, 'One correct value for p'), L(LPC, 'x² + 5x + p > 0'),
     L(HPC, 'Relevant inequality in p (with p as only unknown)'), L(FCM, 'p > 6·25')],
 'maths-2020-hl-p1-q1-b': [L(SOL, '−1 ≤ 2x + 5 ≤ 1'), L(SOL, '−6 ≤ 2x ≤ −4'), L(SOL, '−3 ≤ x ≤ −2'),
     L(ALT, '(2x + 5)² ≤ 1'), L(ALT, '4x² + 20x + 24 ≤ 0'), L(ALT, 'x² + 5x + 6 ≤ 0'), L(ALT, '(x + 2)(x + 3) ≤ 0'),
     L(LPC, '(2x + 5)² ≤ 1'), L(LPC, 'one linear inequality'), L(MPC, '−1 ≤ 2x + 5 ≤ 1'), L(MPC, 'Identifies both linear inequalities'),
     L(MPC, 'Quadratic inequality involving 0'), L(HPC, 'Finding –3 and –2 in Methods 1 or 2'), L(HPC, 'Roots of quadratic found'),
     L(HPC, '−6 ≤ 2x ≤ −4 or equivalent'), L(NOTE, 'Accept −3 < x < −2')],
 'maths-2020-hl-p1-q2-a': [L(SOL, 'i(iz₁) = i(−4 + 3i)'), L(SOL, '−z₁ = −4i + 3i²'), L(SOL, 'z₁ = 3 + 4i'), L(SOL, '3z₁ − z₂ = 3(3 + 4i) − z₂ = 11 + 17i'),
     L(SOL, 'z₂ = 9 + 12i − 11 − 17i'), L(SOL, 'z₂ = −2 − 5i'), L(LPC, 'Either equation multiplied/divided by i'), L(MPC, 'z₁ found'),
     L(MPC, 'z₂ written in terms of z₁ with z₁ substituted'), L(MPC, 'z₁ eliminated'), L(HPC, 'z₁ found and substituted into second equation'),
     L(HPC, 'z₂ found by elimination')],
 'maths-2020-hl-p1-q2-b-i': [L(SOL, 'r = T₂/T₁'), L(SOL, 'r = (15 − 13i − 2)/(9 + 4)'), L(SOL, 'r = (13 − 13i)/13'), L(SOL, 'r = 1 − i'),
     L(LPC, 'T₂/T₁')],
 'maths-2020-hl-p1-q2-b-ii': [L(SOL, 'T₉ = ar⁸'), L(SOL, 'T₉ = (3 + 2i)(1 − i)⁸'), L(SOL, 'T₉ = (3 + 2i)(16)(cos 14π + i sin 14π)'),
     L(SOL, 'T₉ = (3 + 2i)(16)(1 + 0i)'), L(SOL, 'T₉ = 48 + 32i'), L(LPC, 'T₉ = ar⁸'), L(LPC, 'Any correct use of De Moivre'),
     L(LPC, 'Some use of De Moivre’s Theorem on r'), L(MPC, 'Modulus and argument found for r'),
     L(HPC, 'Solution in polar form with some simplification'), L(NOTE, 'Accept candidates r from (b)(i)')],
 'maths-2020-hl-p1-q3-a': [L(SOL, 'fg(x) = 6((x + 5)/6) − 5 = x'), L(SOL, 'gf(x) = g(6x − 5)'), L(LPC, 'g(6x − 5)'),
     L(LPC, 'Particular case verification'), L(HPC, 'One correct composition simplified to x')],
 'maths-2020-hl-p1-q3-b-i': [L(SOL, 'log₅ y = log₅ 5x²'), L(SOL, 'log₅ y = log₅ 5 + log₅ x²'), L(SOL, 'log₅ y = 1 + 2 log₅ x'), L(SOL, 'a = 1 and b = 2'),
     L(LPC, 'log₅ 5x² = log₅ y'), L(HPC, 'log₅ y = log₅ 5 + log₅ x²')],
 'maths-2020-hl-p1-q3-b-ii': [L(SOL, '5x² = 126x − 25'), L(SOL, '5x² − 126x + 25 = 0'), L(SOL, '(5x − 1)(x − 25) = 0'),
     L(SOL, 'or y = 5(25)² = 3125'), L(LPC, 'Some relevant use of laws of logs'), L(MPC, 'Quadratic equation'), L(HPC, 'x values found'),
     L(NOTE, 'If 2 is incorrectly (non log) dealt with then award MPC at most'),
     L(NOTE, 'If incorrect work leads to a non-quadratic equation then award MPC at most')],
 'maths-2020-hl-p1-q4-a': [L(SOL, 'f′(x) = 3x² + 2kx + 15'), L(SOL, '3(3)² + 2k(3) + 15 = −12'), L(SOL, '27 + 6k + 15 = −12'), L(SOL, '6k = −54'),
     L(SOL, 'k = −9'), L(LPC, 'Any relevant differentiation'), L(MPC, 'Expression fully differentiated'),
     L(HPC, 'Derivative fully substituted'), L(NC, 'No differentiation')],
 'maths-2020-hl-p1-q4-b': [L(SOL, 'f′(x) = 3x² + 2(−9)x + 15'), L(SOL, '3x² − 18x + 15 = 0'), L(SOL, 'x² − 6x + 5 = 0'), L(SOL, 'x = 1 x = 5'),
     L(SOL, 'f(1) = 15 (1, 15)'), L(SOL, 'f(5) = −17 (5, −17)'), L(SOL, 'y − 15 = −8(x − 1)'), L(SOL, 'g(x): 8x + y − 23 = 0'),
     L(LPC, 'Any relevant differentiation'), L(MPC, 'Both x values found'), L(HPC, 'Turning points found')],
 'maths-2020-hl-p1-q4-c': [L(SOL, 'f′′(x) = 6x − 18 = 0'), L(SOL, 'x = 3'), L(SOL, 'f(3) = −1'), L(SOL, '(3, −1) is the point of inflection'),
     L(SOL, '8(3) + (−1) − 23 = 0'), L(SOL, '⇒ (3, −1) ∈ g(x).'), L(LPC, 'f′′(x)'), L(HPC, 'x coordinate of point of inflection found'),
     L(HPC, 'Point of inflection found'), L(NOTE, 'Accept candidates g(x) from (b) with relevant statement')],
 'maths-2020-hl-p1-q5-a': [L(SOL, 'A = 250000(0·00287)(1·00287)³⁰⁰ / ((1·00287)³⁰⁰ − 1)'), L(SOL, 'A = €1244·06'),
     L(ALT, '200·9544372 × A = 250000'), L(LPC, 'Formula with some correct substitution'), L(HPC, 'Formula fully substituted')],
 'maths-2020-hl-p1-q5-b': [L(SOL, '1771/1·003 + 1771/1·003² + ⋯ + 1771/1·003¹⁶⁷'), L(SOL, '+ 1771/1·003¹⁶⁸'), L(SOL, '= €233438·25'),
     L(LPC, '1771/1·003'), L(MPC, 'S₁₆₈ formula with some substitution'), L(HPC, 'Formula fully substituted')],
 'maths-2020-hl-p1-q6-a': [L(SOL, 'f(x) = (3x − 5)(2x + 4)'), L(SOL, '= 6x² + 2x − 20'), L(SOL, 'f(x + ℎ) = 6(x + ℎ)² + 2(x + ℎ) − 20'),
     L(SOL, '= 6x² + 12ℎx + 6ℎ² + 2x + 2ℎ − 20'), L(SOL, 'f(x + ℎ) − f(x) = 12ℎx + 6ℎ² + 2ℎ'), L(SOL, '(f(x + ℎ) − f(x))/ℎ = 12x + 6ℎ + 2'), L(SOL, 'lim ℎ→0 (f(x + ℎ) − f(x))/ℎ = 12x + 2'),
     L(SOL, 'f′(x) = 12x + 2'), L(LPC, 'Some substitution into f(x + ℎ) or y + Δy'), L(HPC, 'f(x + ℎ) − f(x) = 12ℎx + 6ℎ² + 2ℎ'),
     L(NC, 'Not from first principles')],
 'maths-2020-hl-p1-q6-b-i': [L(SOL, 'ℎ′(x) = 1/2 (1/(2x + 3))(2)'), L(SOL, '= 1/(2x + 3)'), L(LPC, 'Any relevant differentiation'), L(HPC, '1/2 (1/(2x + 3))')],
 'maths-2020-hl-p1-q6-b-ii': [L(SOL, '½ (ln(2A + 3) − ln 3) = ln 3'), L(SOL, '((2A + 3)/3)^½ = 3'), L(SOL, '(2A + 3)/3 = 9'), L(SOL, '2A + 3 = 27'),
     L(SOL, '2A = 24'), L(SOL, 'A = 12'), L(LPC, 'Integration indicated'), L(MPC, 'Substitutes limits into integral and stops'),
     L(MPC, 'Correct integration with some substitution'),
     L(HPC, 'Integral evaluated at x = A only (i.e. omits ln 3 on LHS and finishes)'), L(NOTE, 'Must have integration to gain any credit')],
 'maths-2020-hl-p1-q7-a-i': [L(SOL, '10 15 21 28 36'), L(LPC, 'One correct new entry'), L(HPC, 'Three correct new entries')],
 'maths-2020-hl-p1-q7-a-ii': [L(SOL, '(n/2)(n + 1) = 1275'), L(SOL, '(n − 50)(n + 51) = 0'), L(SOL, 'n = 50'),
     L(SOL, '1275 is the 50th triangular number'), L(LPC, '(n/2)(n + 1) = 1275'), L(HPC, 'n = 50'), L(NOTE, 'accept T₅₀ as valid reason')],
 'maths-2020-hl-p1-q7-b-i': [L(SOL, 'Tₙ₊₁ = Tₙ + (n + 1)'), L(SOL, '= (n/2)(n + 1) + (n + 1)'), L(SOL, '= (n(n + 1) + 2(n + 1))/2'),
     L(SOL, '= (n + 1)(n + 2)/2'), L(LPC, '2 identified as C.D.'), L(LPC, 'Correct numerator'), L(HPC, '= (n(n + 1) + 2(n + 1))/2')],
 'maths-2020-hl-p1-q7-b-ii': [L(SOL, 'Tₙ₊₁ + Tₙ'), L(SOL, '= (n + 1)(n + 2)/2 + (n/2)(n + 1)'), L(SOL, '= (n + 1)(2n + 2)/2'),
     L(SOL, '= 2(n + 1)(n + 1)/2'), L(SOL, '= (n + 1)²'), L(LPC, 'Tₙ₊₁ + Tₙ with some substitution'), L(LPC, 'Particular case verification'),
     L(HPC, '(n + 1)(n + 2)/2 + (n/2)(n + 1)')],
 'maths-2020-hl-p1-q7-b-iii': [L(SOL, '(n + 1)² = 12544'), L(SOL, 'n + 1 = √12544 = 112'), L(SOL, 'n = 111'), L(SOL, 'T₁₁₁ is the smaller term'),
     L(SOL, 'T₁₁₁ = 111(112)/2'), L(SOL, 'T₁₁₁ = 6216'), L(LPC, '(n + 1)²'), L(HPC, 'n = 111, or n = 112')],
 'maths-2020-hl-p1-q7-c': [L(SOL, '= 1225'), L(LPC, 'Formula with some substitution'), L(HPC, 'Formula fully substituted'),
     L(FC, 'Correct answer with no work shown')],
 'maths-2020-hl-p1-q7-d': [L(SOL, 'P(1): 1 = 1(2)(3)/6'), L(SOL, 'P(k): 1 + 4 + 9 + ⋯ + k² = k(k + 1)(2k + 1)/6'),
     L(SOL, 'P(k + 1): 1 + 4 + 9 + ⋯ + k² + (k + 1)² = (k + 1)(k + 2)(2k + 3)/6'),
     L(SOL, 'LHS = k(k + 1)(2k + 1)/6 + (k + 1)²'), L(SOL, 'LHS = (k + 1)[k(2k + 1) + 6(k + 1)]/6'), L(SOL, 'LHS = (k + 1)[2k² + 7k + 6]/6'),
     L(SOL, 'Thus the proposition is true for n = k + 1 provided it is true for n = k but it is true for n = 1 and therefore true for all positive integers.'),
     L(LPC, 'Step P(1)'), L(MPC, 'Step P(k + 1)'), L(HPC, 'Uses Step P(k) to prove Step P(k + 1)'), L(FCM, 'Concluding statement missing'),
     L(NOTE, 'Accept Step P(1), Step P(k), Step P(k + 1) in any order')],
 'maths-2020-hl-p1-q8-a-i': [L(SOL, 'cos θ = x/5 sin θ = y/5'), L(SOL, '5 cos θ = x 5 sin θ = y'), L(SOL, '(x, y) = (5 cos θ, 5 sin θ)'),
     L(SOL, '∴ a = 5, b = 5'), L(LPC, 'cos θ = x/5 or equivalent'), L(HPC, 'a or b found'), L(HPC, 'Correct answer without work')],
 'maths-2020-hl-p1-q8-a-ii': [L(SOL, 'A(θ) = (10 cos θ) × (10 sin θ)'), L(SOL, 'A(θ) = 100 cos θ sin θ'), L(SOL, '= 50 × 2 cos θ sin θ'),
     L(SOL, '= 50(sin 2θ)'), L(LPC, 'xy'), L(LPC, '(10 cos θ) × (10 sin θ)'), L(HPC, '100 cos θ sin θ')],
 'maths-2020-hl-p1-q8-a-iii': [L(SOL, 'A′(θ) = 50 cos 2θ × 2'), L(SOL, 'A′(θ) = 100 cos 2θ = 0'), L(SOL, 'cos 2θ = 0'), L(SOL, '2θ = π/2'),
     L(SOL, 'θ = π/4'), L(SOL, '2x = 2(5 cos(π/4)) = 5√2'), L(SOL, '2y = 2(5 sin(π/4)) = 5√2'), L(SOL, '⟹ Square'),
     L(LPC, 'a′(θ)'), L(LPC, 'States dy/dx = 0'), L(MPC, 'Correct differentiation'), L(HPC, 'Value of θ at maximum found'),
     L(HPC, 'Value of x or y at maximum fully substituted'), L(NC, 'No differentiation')],
 'maths-2020-hl-p1-q8-a-iv': [L(SOL, 'Max area = 5√2 × 5√2'), L(SOL, '= 50 Square units'), L(ALT, 'Max area = 50(sin 2θ)'),
     L(LPC, 'xy'), L(LPC, 'length × width'), L(LPC, '50(sin 2θ)'), L(HPC, 'Area formula fully substituted')],
 'maths-2020-hl-p1-q8-b': [L(SOL, 'dx/dt = dx/dl ∙ dl/dt'), L(SOL, '2/5 = x/(l + x)'), L(SOL, '2l + 2x = 5x'), L(SOL, 'x = (2/3)l'),
     L(SOL, 'dx/dl = 2/3'), L(SOL, 'dx/dt = 2/3 × 3/2'), L(SOL, 'dx/dt = 1 m/sec'),
     L(LPC, 'dx/dt or dx/dl or dl/dt given'), L(LPC, 'Reference to similar triangles'), L(LPC, '2/5 or 5/2'),
     L(MPC, 'dx/dt = dx/dl ∙ dl/dt or equivalent with one relevant substitution'), L(MPC, 'x = (2/3)l'), L(HPC, 'dx/dl and dl/dt found')],
 'maths-2020-hl-p1-q9-a-i': [L(SOL, 'N(4·5) = 450e^(0·065(4·5))'), L(SOL, '= 602·89'), L(SOL, '= 603'), L(LPC, 'Some substitution into function'),
     L(LPC, 'Correct answer without work'), L(HPC, '450e^(0·065(4·5))')],
 'maths-2020-hl-p1-q9-a-ii': [L(SOL, 'N(t)/450 = e^(0·065t)'), L(SOL, 'Convert to log equation'), L(SOL, 'ln(N(t)/450) = 0·065t'),
     L(SOL, 't = (ln(790) − ln 450)/0·065'), L(SOL, 't = 8·7'), L(LPC, 'Some substitution into function'), L(LPC, 'Full substitution and stops'),
     L(HPC, 'Equation in t ( i.e. logs handled correctly)')],
 'maths-2020-hl-p1-q9-b': [L(SOL, '= 743·2'), L(SOL, 'Average no. = 743'), L(LPC, 'Integration indicated'), L(MPC, 'Integration correct'),
     L(HPC, 'Substitutes limits into integral and stops'), L(NOTE, 'Must have integration to gain any credit')],
 'maths-2020-hl-p1-q9-c': [L(SOL, 'N′(t) = 450e^(0·065t) × 0·065'), L(SOL, 'N′(12) = 29·25e^(0·065(12))'), L(SOL, '= 63·8'),
     L(SOL, 'At hour 12 the population is growing at a rate of 64 bacteria per hour'),
     L(SOL, 'or At hour 12 the population is growing at a rate of 63·8 bacteria per hour'),
     L(LPC, 'N′(t) stated or indicated'), L(HPC, 'Derivative fully substituted'), L(HPC, 'N′(12) = 63·8 and stops')],
 'maths-2020-hl-p1-q9-d': [L(SOL, 'N′(t) = 29·25e^(0·065k) > 90'), L(SOL, 'e^(0·065k) > 90/29·25'), L(SOL, 'k > 17·29'), L(SOL, 'k = 18'),
     L(LPC, '29·25e^(0·065k) > 90'), L(HPC, 'Equation in k ( i.e. taking logs handled correctly)'), L(NC, 'No differentiation'),
     L(NOTE, 'if k > 17·29 ⇒ k = 17 Award Full credit (–1)')],
 'maths-2020-hl-p1-q9-e': [L(SOL, '450e^(0·065t) = 220e^(0·17t)'), L(SOL, '450/220 = e^(0·105t)'), L(SOL, 'ln(450/220) = 0·105t'),
     L(SOL, 't = 6·82'), L(SOL, 't = 7 hours'), L(LPC, '450e^(0·065t) = 220e^(0·17t)'),
     L(HPC, 'Equation in t ( i.e. taking logs handled correctly)')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2020, 'hl', 'p1', {'5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 4, 8, 10], '10D': [0, 3, 5, 8, 10],
                             '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
f1 = 'f(x) = x² + 5x + p where x ∈ ℝ, −3 ≤ p ≤ 8, and p ∈ ℤ.'
A('1-a-i', 'Q1(a)(i)', '10C', [8], [4], '4-1', 'algebra-expressions-factorising,algebra-quadratics', 'Find the value of p for which x + 3 is a factor of f(x).', stem=f1)
A('1-a-ii', 'Q1(a)(ii)', '5C', [9], [4], '4-2', 'algebra-quadratics', 'Find the value of p for which f(x) has roots which differ by 3.', stem=f1)
A('1-a-iii', 'Q1(a)(iii)', '5C', [9], [5], '4-3', 'algebra-quadratics,algebra-inequalities', 'Find the two values of p for which the graph of f(x) will not cross the x-axis.', stem=f1)
A('1-b', 'Q1(b)', '5D', [10], [5], '4-3', 'algebra-inequalities', 'Find the range of values of x for which |2x + 5| − 1 ≤ 0, where x ∈ ℝ.')
A('2-a', 'Q2(a)', '5D', [11], [6], '4-4', 'complex-numbers', 'Find the two complex numbers z₁ and z₂ that satisfy the following simultaneous equations, where i² = −1: iz₁ = −4 + 3i; 3z₁ − z₂ = 11 + 17i. Write your answers in the form a + bi where a, b ∈ ℤ.')
g2 = 'The complex numbers 3 + 2i and 5 − i are the first two terms of a geometric sequence.'
A('2-b-i', 'Q2(b)(i)', '5C', [11], [7], '4-4', 'complex-numbers,sequences-series', 'Find r, the common ratio of the sequence. Write your answer in the form a + bi where a, b ∈ ℤ.', stem=g2)
A('2-b-ii', 'Q2(b)(ii)', '15D', [11], [7], '4-4', 'complex-numbers,sequences-series', 'Use de Moivre’s Theorem to find T₉, the ninth term of the sequence. Write your answer in the form a + bi, where a, b ∈ ℤ.', stem=g2)
A('3-a', 'Q3(a)', '10C', [12], [8], '5-1', 'functions', 'f(x) = 6x − 5 and g(x) = (x + 5)/6. Investigate if f(g(x)) = g(f(x)).')
y3 = 'The real variables y and x are related by y = 5x².'
A('3-b-i', 'Q3(b)(i)', '5C', [12], [8], '3-2', 'indices-and-logs', 'The equation y = 5x² can be rewritten in the form log₅ y = a + b log₅ x. Find the value of a and the value of b.', stem=y3)
A('3-b-ii', 'Q3(b)(ii)', '10D', [12], [9], '3-2', 'indices-and-logs,algebra-quadratics', 'Hence, or otherwise, find the real values of y for which log₅ y = 2 + log₅((126/25)x − 1).', stem=y3)
f4 = 'The diagram below shows two functions f(x) and g(x). The function f(x) is given by the formula f(x) = x³ + kx² + 15x + 8, where k ∈ ℤ, and x ∈ ℝ.'
A('4-a', 'Q4(a)', '15D', [13], [10], '5-2', 'differentiation-rules', 'Given that f′(3) = −12, show that k = −9, where f′(3) is the derivative of f(x) at x = 3.', stem=f4)
A('4-b', 'Q4(b)', '5D', [13], [11], '5-2', 'differentiation-applications,co-ordinate-geometry-of-the-line', 'The function g(x) is the line that passes through the two turning points of f(x) = x³ − 9x² + 15x + 8, as shown on the previous page. Find the equation of g(x).', stem=f4)
A('4-c', 'Q4(c)', '5C', [13], [11], '5-2', 'differentiation-applications', 'Show that the graph of g(x) contains the point of inflection of f(x).', stem=f4 + ' The function g(x) is the line that passes through the two turning points of f(x) = x³ − 9x² + 15x + 8.')
A('5-a', 'Q5(a)', '15C', [14], [12], '3-3', 'financial-maths', 'A couple agree to take out a €250 000 mortgage in order to purchase a new home. The loan is to be paid back monthly over 25 years with the repayments due at the end of each month. The bank charges an annual percentage rate (APR) which is equivalent to a monthly rate of 0·287%. Using the amortisation formula, or otherwise, find the couples’ monthly repayment on the mortgage. Give your answer in euro correct to the nearest cent.')
A('5-b', 'Q5(b)', '10D', [14], [13], '3-3', 'financial-maths,sequences-series', 'Another couple agree to take out a mortgage of €350 000, at a rate of 0·3% per month, in order to purchase a new home. This loan is also to be paid back monthly over 25 years with the repayments due at the end of each month. The amount of each repayment is €1771. After exactly 11 years of repayments, the couple receive a financial windfall. They decide to repay the remaining balance on the mortgage. Write down a series (including the first two and last two terms) which shows the total of the present values of all the remaining monthly repayments due over the remaining 14 years of the mortgage (after the last monthly repayment at the end of year 11). Hence, find how much the couple will need to repay in order to clear their mortgage entirely. Give your answer correct to the nearest cent.')
A('6-a', 'Q6(a)', '15C', [15], [14], '5-2', 'differentiation-rules', 'Differentiate (3x − 5)(2x + 4) with respect to x from first principles.')
h6 = 'h(x) = ½ ln(2x + 3) + C, where C is a constant.'
A('6-b-i', 'Q6(b)(i)', '5C', [15], [15], '5-2', 'differentiation-rules', 'Find h′(x), the derivative of h(x).', stem=h6)
A('6-b-ii', 'Q6(b)(ii)', '5D', [15], [15], '5-2', 'integration', 'The diagram below shows part of the graph of the function h′(x). The shaded region in the diagram is between the graph and the x-axis, from x = 0 to x = A. This shaded region has an area of ln 3 square units. Find the value of A.', stem=h6)
t7 = 'A number of the form 1 + 2 + 3 + ⋯ + n is sometimes called a triangular number because it can be represented as an equilateral triangle. The diagram below shows the first three terms in the sequence of triangular numbers: T₁ = 1, T₂ = 1 + 2 = 3, T₃ = 1 + 2 + 3 = 6.'
A('7-a-i', 'Q7(a)(i)', '10C', [16], [16], '4-1', 'sequences-series', 'Complete the table below to list the next five triangular numbers.', stem=t7)
tn = t7 + ' The nth triangular number can be found directly using the formula Tₙ = n(n + 1)/2.'
A('7-a-ii', 'Q7(a)(ii)', '5C', [16], [16], '4-1', 'sequences-series,algebra-quadratics', 'Is 1275 a triangular number? Give a reason for your answer.', stem=tn)
tb = tn + ' The (n + 1)th triangular number can be written as Tₙ₊₁ = Tₙ + (n + 1), where n ∈ ℕ.'
A('7-b-i', 'Q7(b)(i)', '5C', [16], [17], '4-1', 'sequences-series,algebra-expressions-factorising', 'Write the expression n(n + 1)/2 + (n + 1) as a single fraction in its simplest form.', stem=tb)
A('7-b-ii', 'Q7(b)(ii)', '5C', [16], [17], '4-1', 'sequences-series,algebra-expressions-factorising', 'Prove that the sum of any two consecutive triangular numbers will always be a square number (a number in the form k², where k ∈ ℕ).', stem=tb)
A('7-b-iii', 'Q7(b)(iii)', '5C', [17], [17], '4-1', 'sequences-series,algebra-quadratics', 'Two consecutive triangular numbers sum to 12 544. Find the smaller of these two numbers.', stem=tb)
A('7-c', 'Q7(c)', '5C', [17], [18], '4-1', 'sequences-series', 'Some numbers are both triangular and square, for example 36. Leonhard Euler (1778) discovered the following formula for these numbers: Nₖ = (((3 + 2√2)^k − (3 − 2√2)^k)/(4√2))², where Nₖ is the kth number that is both triangular and square. Use Euler’s formula to find N₃, the third number that is both triangular and square.', stem=t7)
A('7-d', 'Q7(d)', '15D', [18], [19], '3-1', 'induction,sequences-series', 'Prove using induction that, for all n ∈ ℕ, the sum of the first n square numbers can be found using the formula: 1² + 2² + 3² + 4² + ⋯ + n² = n(n + 1)(2n + 1)/6.')
r8 = 'A rectangle is inscribed in a circle of radius 5 units and centre O(0, 0) as shown below. Let R(x, y), where x, y ∈ ℝ, be the vertex of the rectangle in the first quadrant as shown. Let θ be the angle between [OR] and the positive x-axis, where 0 ≤ θ ≤ π/2.'
trig = 'trigonometry-functions-identities'
A('8-a-i', 'Q8(a)(i)', '5C', [19], [20], '2-3', trig + ',co-ordinate-geometry-of-the-circle', 'The point R(x, y) can be written as (a cos θ, b sin θ), where a, b ∈ ℝ. Find the value of a and the value of b.', stem=r8)
A('8-a-ii', 'Q8(a)(ii)', '10C', [19], [20], '2-3', trig + ',area-volume', 'Show that A(θ), the area of the rectangle, measured in square units, can be written as A(θ) = 50 sin 2θ.', stem=r8)
r8a = r8 + ' A(θ), the area of the rectangle, measured in square units, can be written as A(θ) = 50 sin 2θ.'
A('8-a-iii', 'Q8(a)(iii)', '15D', [19], [21], '5-2', 'differentiation-applications,' + trig, 'Use calculus to show that the rectangle with maximum area is a square.', stem=r8a)
A('8-a-iv', 'Q8(a)(iv)', '5C', [19], [21], '5-2', 'differentiation-applications,' + trig, 'Find this maximum area.', stem=r8a + ' Use calculus to show that the rectangle with maximum area is a square.')
A('8-b', 'Q8(b)', '10D', [20], [22], '5-2', 'differentiation-applications', 'A person who is 2 m tall is walking towards a streetlight of height 5 m at a speed of 1·5 m/s. Find the rate, in m/s, at which the length of the person’s shadow (x), cast by the streetlight, is changing.')
b9 = 'The number of bacteria in the early stages of a growing colony of bacteria can be approximated using the function: N(t) = 450e^(0·065t), where t is the time, measured in hours, since the colony started to grow, and N(t) is the number of bacteria in the colony at time t.'
A('9-a-i', 'Q9(a)(i)', '10C', [21], [23], '3-2', 'indices-and-logs', 'Find the number of bacteria in the colony after 4·5 hours. Give your answer correct to the nearest whole number.', stem=b9)
A('9-a-ii', 'Q9(a)(ii)', '10C', [21], [23], '3-2', 'indices-and-logs', 'Find the time, in hours, that it takes the colony to grow to 790 bacteria. Give your answer correct to 1 decimal place.', stem=b9)
A('9-b', 'Q9(b)', '10D', [22], [24], '5-2', 'integration', 'Using the function N(t) = 450e^(0·065t), find the average number of bacteria in the colony during the period from t = 3 to t = 12. Give your answer correct to the nearest whole number.', stem=b9)
A('9-c', 'Q9(c)', '10C', [22], [24], '5-2', 'differentiation-applications', 'Find the rate at which N(t) = 450e^(0·065t) is changing when t = 12. Give your answer correct to one decimal place. Interpret this value in the context of the question.', stem=b9)
A('9-d', 'Q9(d)', '5C', [23], [25], '5-2', 'differentiation-applications,indices-and-logs', 'After k hours, the rate of increase of N(t) is greater than 90 bacteria per hour. Find the least value of k, where k ∈ ℕ.', stem=b9)
A('9-e', 'Q9(e)', '10C', [23], [25], '3-2', 'indices-and-logs', 'The number of bacteria in the early stages of a different colony of bacteria can be approximated using the function: P(t) = 220e^(0·17t), where P(t) is the number of bacteria and t is measured in hours. Assume that both colonies start growing at the same time. Find the time, to the nearest hour, at which the number of bacteria in both colonies will be equal.', stem=b9)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 50, '8': 45, '9': 55}
p.check(marks, 36)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 1–23 of the combined Higher Level scheme (cover, notes, the Paper 1 scale table on page 5, the summary of mark allocations on page 6, the annotation palette on page 7, and every Paper 1 model solution and marking note), plus the Paper 2 title page 24. Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 25)), [5, 6],
    ['The 2020 Leaving Certificate examinations were cancelled and replaced by Calculated Grades, but the SEC published this paper and its marking scheme. The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 50 marks, Q8 45 marks, Q9 55 marks). Every question is retained.',
     '36 independently marked units, matching the printed summary of allocations on scheme page 6. No two parts share a scale on this paper.',
     'Paper 1 bands from the scale table on scheme page 5: 5C 0,3,4,5; 10C 0,4,8,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15. The table prints no 5-mark D scale; the 5D parts (Q1(b), Q2(a), Q4(b), Q6(b)(ii)) print their ladder beside the scale, “Scale 5D (0, 2, 3, 4, 5)”.',
     'This paper had no authored cards before this review; all 36 units are new. Marking points are lifted line by line from the scheme and labelled with the part of the scheme they come from. The scheme’s text layer encodes its equation font in Syriac and NKo code points; the repair map was extended from glyph ids (derive_glyphs.py run over the 2019 and 2020 Higher and Ordinary schemes), not by hand.',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [9, 12], 'wording': 'Hence, or otherwise / Using the amortisation formula, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'},
     {'pages': [17], 'wording': 'the sum of any two consecutive triangular numbers', 'classification': 'mathematical-context',
      'reason': 'A universal statement to be proved for every pair; not a choice between prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t
        else ('mathematical-context', '“Any two consecutive triangular numbers” is the universal claim to be proved, not a choice between prompts.') if 'any two consecutive' in t else None)
p.apply(ROWS, '2020 Higher Level Paper 1', expect_added=[c['id'] for c in p.cards],
        question_figures=True)
