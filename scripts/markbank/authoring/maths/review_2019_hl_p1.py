"""2019 HL Paper 1: a new paper — 35 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
M1, M2, M3 = 'Method 1, ', 'Method 2, ', 'Method 3, '

ROWS = {
 'maths-2019-hl-p1-q1-a': [L(SOL, '(2x + 1)(x² + px + 4)'), L(SOL, '2x³ + 2px² + 8x + x² + px + 4'), L(SOL, '8 + p = 2(2p + 1)'), L(SOL, '3p = 6'), L(SOL, 'p = 2'),
     L(ALT, 'Coefficient of x is 8 + p'), L(ALT, 'Coefficient of x² is 2p + 1'), L(LPC, 'Any relevant multiplication'),
     L(MPC, 'Multiplication completed without error(s)'),
     L(MPC, 'Multiplication completed with errors and correctly identifies (in terms of p) the coefficient of either x² or x'),
     L(MPC, 'Correctly identifies the coefficient of either x or x²'),
     L(HPC, 'Multiplication completed with error(s) but finishes correctly without further errors'),
     L(HPC, 'Relevant coefficients equated (equation in p)'),
     L(HPC, 'Multiplication completed and coefficients of x² and x identified but solves incorrect equation in p')],
 'maths-2019-hl-p1-q1-b': [L(SOL, 'CD: 5(2x + 1)(3x − 1)'), L(SOL, '15(3x − 1) + (4x + 2)(3x − 1) = 10(2x + 1)'), L(SOL, '12x² + 27x − 27 = 0'),
     L(SOL, '4x² + 9x − 9 = 0'), L(SOL, '(x + 3)(4x − 3)=0'), L(SOL, 'x = −3 or x = 3/4'), L(ALT, '(4x + 17)(3x − 1) = 2(10x + 5)'),
     L(LPC, 'CD or partial CD identified'), L(LPC, 'Cross multiply on LHS'), L(LPC, 'Multiplies one term correctly by one of the denominators'),
     L(LPC, 'x = −3 or x = 3/4 substituted and justified as a solution'), L(MPC, 'Equation without fractions'),
     L(HPC, 'Relevant quadratic in the form: ax² + bx + c = 0'),
     L(NOTE, 'No quadratic low partial credit at most, except in the case where the candidate has reached the mid partial stage')],
 'maths-2019-hl-p1-q2-a-i': [L(SOL, '(0, 1) (2, 9)'), L(LPC, '1 point on line found'), L(HPC, '2 points on line found'),
     L(HPC, '1 point found and plotted (apart from (0, 1) and (2, 9))'), L(FCM, 'Freehand graph drawn')],
 'maths-2019-hl-p1-q2-a-ii': [L(SOL, 'g(1·9) = 4(1·9) + 1 = 8·6'), L(SOL, 'f(1·9) = 3^1·9 = 8·06'), L(SOL, 'f(x) < g(x)'), L(LPC, 'g(1·9) written or found'),
     L(LPC, 'f(1·9) written or found'), L(HPC, 'g(1·9) and f(1·9) found')],
 'maths-2019-hl-p1-q2-b': [L(SOL, 'To Prove: 3^n ≥ 4n + 1 for n ≥ 2'), L(SOL, 'P(2): 3² ≥ 4(2) + 1'), L(SOL, '9 ≥ 9, True'),
     L(SOL, 'P(k): 3^k ≥ 4k + 1 for k ≥ 2'), L(SOL, 'P(k + 1): 3^(k+1) ≥ 4(k + 1) + 1'), L(SOL, 'Proof: P(k) × 3: 3^(k+1) ≥ 3(4k + 1)'),
     L(SOL, 'since 4k + 5 < 12k + 3 for k ≥ 2'), L(SOL, '∴ True for all n ≥ 2, n ∈ ℕ.'), L(LPC, 'Step P(2)'),
     L(LPC, 'P(k) or P(k + 1) with incorrect inequality sign'), L(MPC, 'Any two of P(2), P(k) or P(k + 1)'),
     L(HPC, 'Uses Step P(k) to prove Step P(k + 1)'), L(FCM, 'Omits conclusion but otherwise correct'),
     L(NOTE, 'Accept Step P(2), Step P(k), Step P(k + 1) in any order'), L(NOTE, 'Accept f(k) ≥ g(k), k ≥ 2 for Step P(k)')],
 'maths-2019-hl-p1-q3-a': [L(SOL, '(3x + 4)(y − 3)'), L(MPC, 'Any relevant factorisation')],
 'maths-2019-hl-p1-q3-b': [L(SOL, '3x(lnx − 3) + 4(lnx − 3) ='), L(SOL, '(3x + 4)(lnx − 3)'), L(SOL, '3x + 4 = 0 ⇒ x = −4/3'), L(SOL, 'lnx = 3'),
     L(SOL, 'x = e³'), L(LPC, 'Any relevant factorisation of g(x)'), L(LPC, 'Trial and improvement with at least two values tested'),
     L(LPC, 'Substitutes 20 ≤ x ≤ 20·1'), L(LPC, 'y = lnx'), L(MPC, 'Expression fully factorised'), L(HPC, 'lnx = 3'),
     L(FC, 'Both solutions presented'), L(NOTE, 'Accept x = 20·1 for x = e³ in the last line of the solution'),
     L(NOTE, 'If no reference is made to 3x + 4 in the solution, then award high partial credit at most')],
 'maths-2019-hl-p1-q3-c': [L(SOL, 'g′(x) = 3x(1/x) + (3)lnx − 9 + 4(1/x)'), L(SOL, 'g′(e) = 3 + 3 − 9 + 4/e = −1·53'), L(LPC, 'Any relevant differentiation'),
     L(LPC, 'g(e) evaluated correctly to at least 2 decimal places'), L(MPC, 'Expression fully differentiated'),
     L(MPC, 'Product rule not applied but finishes correctly'), L(HPC, 'Derivative fully substituted')],
 'maths-2019-hl-p1-q4-a': [L(SOL, 'x⁴ − 3x² + 10x + C'), L(LPC, 'Any relevant integration'), L(HPC, '3 correct terms')],
 'maths-2019-hl-p1-q4-b-i': [L(SOL, '∫(6x² − 54x + 109) dx'), L(SOL, '= 2x³ − 27x² + 109x + C = f(x)'), L(SOL, '(2, 0) ∈ f(x)'), L(SOL, '126 + C = 0'),
     L(SOL, 'C = −126'), L(LPC, 'Any relevant integration'), L(MPC, '3 correct terms'), L(HPC, 'Relevant equation in C'),
     L(NOTE, 'Must integrate or indicate integration to gain any credit')],
 'maths-2019-hl-p1-q4-b-ii': [L(SOL, '2 is a root'), L(SOL, '⇒ (x − 2) is a factor'), L(SOL, '2x² − 23x + 63 = 0'), L(SOL, '(2x − 9)(x − 7) = 0'),
     L(SOL, 'x = 4·5 or x = 7'), L(SOL, '∴ B(4·5, 0) and C(7, 0)'), L(LPC, '2 identified as root'), L(LPC, '0 given as the y co-ordinate'),
     L(LPC, 'Sets up equation'), L(LPC, 'Any integer fully substituted in f(x) fully worked'), L(LPC, '(x − 2) is a factor'),
     L(MPC, 'Division completed with no remainder'), L(MPC, '7 identified as a root'), L(MPC, 'One coordinate pair found'),
     L(HPC, 'x values found from factors')],
 'maths-2019-hl-p1-q5-a': [L(SOL, '3 − 2i = other root'), L(SOL, '−p = (3 + 2i) + (3 − 2i) = 6'), L(SOL, 'p = −6'), L(SOL, 'q = (3 + 2i)(3 − 2i) = 13'),
     L(ALT, '(3 + 2i)² + p(3 + 2i) + q = 0'), L(ALT, '5 + 12i + 3p + 2pi + q = 0'), L(M1 + LPC, 'Second root identified'),
     L(M1 + HPC, 'Sum and product of roots formulated into equations for p and q'), L(M1 + HPC, 'p or q found correctly'),
     L(M2 + LPC, 'Root substituted into equation'), L(M2 + LPC, 'Any correct substitution'),
     L(M2 + HPC, 'Real and imaginary terms formulated into equations for p and for q'), L(M3 + LPC, 'Some substitution into quadratic formula'),
     L(M3 + HPC, 'Finds p'), L(M3 + HPC, 'Full substitution into quadratic formula and equated to either root.')],
 'maths-2019-hl-p1-q5-b-i': [L(SOL, '|v| = √(4 + 12) = 4'), L(SOL, 'θ = 300°'), L(SOL, 'v = 4(cos 300° + i sin 300°)'), L(SOL, 'θ = 5π/3'),
     L(LPC, 'Correct plot on the Argand diagram'), L(LPC, 'Some use of Pythagoras to find modulus'),
     L(LPC, 'Some use of trigonometry to find argument'), L(HPC, 'Modulus or argument found'),
     L(NOTE, 'Accept 4(cos −π/3 + i sin −π/3) and 4(cos −60° + i sin −60°)')],
 'maths-2019-hl-p1-q5-b-ii': [L(SOL, 'w = ±2(cos 150 + i sin 150)'), L(SOL, 'w = ±(−√3 + i)'), L(SOL, 'w = −√3 + i or √3 − i'),
     L(LPC, 'w written in polar form with index'), L(LPC, 'Some use of De Moivre’s Theorem'), L(LPC, 'w = v^(1/2)'),
     L(HPC, 'De Moivre’s theorem applied to w'), L(HPC, 'One solution found'), L(HPC, 'Solutions in polar form'),
     L(NOTE, 'Accept candidates answer from (b)(i)')],
 'maths-2019-hl-p1-q6-a-i': [L(SOL, 'x + 5x = √128 + √32'), L(SOL, '6x = 8√2 + 4√2'), L(SOL, '6x = 12√2'), L(SOL, 'x = 2√2'),
     L(ALT, '(x − √2)(x − 2√2) = 0'), L(M1 + LPC, 'Any relevant transposing'), L(M1 + LPC, '√32 or √128 in the form a√2'),
     L(M1 + HPC, 'x term isolated in equation'), L(M2 + LPC, 'Any relevant multiplication'), L(M2 + HPC, 'LHS and RHS squared correctly'),
     L(M2 + HPC, 'Solution not in the form a√2'), L(FCM, 'Both solutions presented'),
     L(NOTE, 'If √128 and √32 are converted to decimals, then award low partial credit at most')],
 'maths-2019-hl-p1-q6-a-ii': [L(SOL, '4√2 k, 5√2 k, 7√2 k, 8√2 k'), L(SOL, 'Mean = 24√2 k/4 = 6√2 k'), L(SOL, 'Median = 6√2 k'),
     L(LPC, 'List in ascending or descending order'), L(LPC, 'Any term written in the form a√2k or in the form a√2k²'),
     L(HPC, 'Mean or median found'), L(HPC, 'Verified for a particular value of k'), L(NOTE, 'If decimals are used then award low partial credit at most')],
 'maths-2019-hl-p1-q6-b': [L(SOL, 'Assume √2 is rational'), L(SOL, 'no common factors (simplest form)'), L(SOL, '⇒ 2q² = p²'), L(SOL, '⇒ p is even'),
     L(SOL, '⇒ q² = 2k²'), L(SOL, '⇒ q is even'), L(SOL, '⇒ common factor of 2 (contradiction )'), L(SOL, '∴ √2 cannot be rational.'),
     L(LPC, '√2 = p/q or similar'), L(MPC, 'deduces that p is even or equivalent'), L(MPC, 'p = 2k or equivalent deduced'), L(MPC, 'p² = 2q²'),
     L(HPC, 'q = 2m or equivalent deduced')],
 'maths-2019-hl-p1-q7-a-i': [L(SOL, '1/3, 2/9, 4/27, 8/81, 16/243'), L(LPC, '1 correct fraction given in table'), L(LPC, '1 correct denominator'),
     L(LPC, '1 correct numerator'), L(HPC, '2 correct fractions given in table'), L(HPC, 'All numerators correct'), L(HPC, 'All denominators correct')],
 'maths-2019-hl-p1-q7-a-ii': [L(SOL, 'Sn = a(1 − r^n)/(1 − r)'), L(SOL, 'Sn = 1 − (2/3)^n'), L(LPC, 'Sn formula with some substitution'),
     L(LPC, 'Correct a or correct r identified'), L(HPC, 'Sn formula fully substituted')],
 'maths-2019-hl-p1-q7-a-iii': [L(SOL, 'Infinite Geometric Series a = 1/3 r = 2/3'), L(SOL, 'S∞ = a/(1 − r)'), L(SOL, '= 1'), L(LPC, 'S∞ indicated'),
     L(LPC, 'Correct a or correct r identified'), L(HPC, 'S∞ fully substituted'), L(NOTE, 'If |r| > 1, then award low partial credit at most')],
 'maths-2019-hl-p1-q7-b-i': [L(SOL, '2/3, 2/9, 7/9, 8/9, 7/27, 25/27'), L(LPC, '1 correct fraction given in table'), L(LPC, 'All denominators correct'),
     L(HPC, '4 correct fractions given in table')],
 'maths-2019-hl-p1-q7-b-ii': [L(SOL, 'It is the end point (start point) of a segment'), L(MPC, 'Relevant but incomplete reason given'),
     L(MPC, 'Sum of fractions = 20/81')],
 'maths-2019-hl-p1-q7-b-iii': [L(SOL, 'S∞ = a/(1 − r)'), L(ALT, 'S∞ = 3/8 − 1/8 = 1/4'), L(LPC, 'S∞ indicated'), L(LPC, 'S∞formula with some substitution'),
     L(LPC, 'Correct a or correct r'), L(HPC, 'S∞ formula fully substituted')],
 'maths-2019-hl-p1-q8-a': [L(SOL, 'r(20) = 22500 cos(π/26 (20)) + 37500'), L(SOL, '= €20658·51'), L(SOL, '≈ €20659'), L(LPC, 'Any relevant substitution'),
     L(LPC, 'r(20) or t = 20'), L(HPC, 'Correct substitution'), L(FCM, 'Uses degrees as unit of measurement, giving an answer of €59980')],
 'maths-2019-hl-p1-q8-b': [L(SOL, '22500 cos(π/26 t) + 37500 = 26250'), L(SOL, 'cos(π/26 t) = −1/2'), L(SOL, 'π/26 t = 2π/3 and π/26 t = 4π/3'),
     L(SOL, 't = 52/3 and t = 104/3'), L(LPC, 'Equation formed'), L(LPC, 'Trial and improvement with at least two values tested'),
     L(MPC, 'Equation simplified to: cos(π/26 t) = −1/2'), L(HPC, '1 correct solution to equation found')],
 'maths-2019-hl-p1-q8-c': [L(SOL, 'r′(t) = 22500[−sin(π/26 t)](π/26)'), L(SOL, '= −11250/13 π[sin(π/26 t)]'), L(LPC, 'Some relevant differentiation'),
     L(HPC, 'Chain rule applied')],
 'maths-2019-hl-p1-q8-d': [L(SOL, 'r′(30) = −11250/13 π[sin(π/26 (30))]'), L(SOL, '= 402·164π'), L(SOL, '= 1263·44'), L(SOL, '⇒ Increasing'),
     L(LPC, 'Some relevant substitution into answer from (c)'), L(LPC, 'r′(t) > 0'), L(LPC, 'dy/dx > 0'),
     L(HPC, 'r′(30) found but no conclusion or incorrect conclusion'), L(NOTE, 'If calculus is not used then award no credit for the solution')],
 'maths-2019-hl-p1-q8-e': [L(SOL, 'sin(π/26 t) = 0'), L(SOL, 't = 0 and t = 26'), L(SOL, 'r′′(t) = −11250/13 π[cos(π/26 t)](π/26)'),
     L(SOL, 't = 0: r′′(t) < 0 ⇒ Max'), L(SOL, 't = 26: r′′(t) > 0 ⇒ Min'), L(LPC, 'r′(t) = 0'), L(LPC, 'dy/dx = 0'),
     L(LPC, 'States r′′(t) > 0 at minimum value'), L(LPC, 't = 26 and no further work'), L(MPC, 't = 0 or t = 26 found with supporting work'),
     L(MPC, 'r′′(t) found'), L(HPC, 't = 26 found with supporting work and r′′(t) found (including use of chain rule)')],
 'maths-2019-hl-p1-q9-a-i': [L(SOL, '= 2(x) + 2(y) + 1/2 (2π)(x)'), L(SOL, '= 2x + 2y + πx'), L(LPC, 'Some relevant substitution into perimeter formula'),
     L(LPC, 'Circumference of circle of radius x found i.e. 2πx'), L(HPC, 'Two of the three terms found')],
 'maths-2019-hl-p1-q9-a-ii': [L(SOL, '2x + 2y + πx = 12'), L(SOL, '2y = 12 − 2x − πx'), L(SOL, 'y = (12 − (2 + π)x)/2'),
     L(LPC, 'Some relevant substitution into equation'), L(HPC, 'y term isolated correctly in equation'),
     L(NOTE, 'Accept candidates answer from (a)(i) provided it doesn’t oversimplify the work.'), L(NOTE, 'Must draw a relevant conclusion from incorrect work')],
 'maths-2019-hl-p1-q9-b-i': [L(SOL, 'Table and Graph'), L(LPC, 'One correct table entry'), L(LPC, 'One correct plot of incorrect point'),
     L(MPC, '2 table entries correct'), L(MPC, '2 incorrect points plotted and joined'),
     L(HPC, '2 correct points plotted but not joined with correct table entries'),
     L(FCM, 'Two correct points plotted and joined but the function is not graphed in the stated domain'),
     L(NOTE, 'Accept 2·25 ≤ x ≤ 2·5 for x−intercept')],
 'maths-2019-hl-p1-q9-b-iii': [L(SOL, 'y = 6 − ((2 + π)/2)x'), L(SOL, 'm = −((2 + π)/2)'), L(SOL, 'm = −2·57'),
     L(SOL, 'For each 1m rise in the radius of the semi-circle, the height of the rectangle falls by approximately 2·57 m'),
     L(LPC, 'Some substitution into slope formula'), L(LPC, 'Slope isolated in the equation of the line formula'), L(LPC, 'Some effort at differentiation'),
     L(HPC, 'Slope found'), L(NOTE, 'Accept −2·7 ≤ slope ≤ −2·5 from relevant work')],
 'maths-2019-hl-p1-q9-c-i': [L(SOL, 'a = 2xy + πx²/2'), L(SOL, '= (24x − (π + 4)x²)/2'), L(LPC, 'area of rectangle correct'), L(LPC, 'area of semi-circle correct'),
     L(HPC, 'Both areas correct in terms of x and added')],
 'maths-2019-hl-p1-q9-c-ii': [L(SOL, 'a′(x) = 1/2 (24 − 2(π + 4)x)'), L(SOL, '= 12 − (π + 4)x'), L(MPC, 'Some correct differentiation')],
 'maths-2019-hl-p1-q9-c-iii': [L(SOL, 'a′(x) = 0'), L(SOL, '12 − (π + 4)x = 0'), L(SOL, 'x = 12/(π + 4) (1·68)'), L(SOL, '= 24/(2(π + 4))'),
     L(SOL, 'Area Max when height equals the radius'), L(LPC, 'a′(x) used'), L(LPC, 'States dy/dx = 0'), L(MPC, 'Value of x at maximum found'),
     L(HPC, 'Value of y at maximum fully substituted')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2019, 'hl', 'p1', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 4, 7, 10], '10D': [0, 4, 5, 8, 10], '15D': [0, 4, 7, 11, 15]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
A('1-a', 'Q1(a)', '10D', [8], [4], '4-1', 'algebra-expressions-factorising', 'In the expansion of (2x + 1)(x² + px + 4), where p ∈ ℕ, the coefficient of x is twice the coefficient of x². Find the value of p.')
A('1-b', 'Q1(b)', '15D', [9], [5], '4-2', 'algebra-solving-equations,algebra-quadratics', 'Solve the equation 3/(2x + 1) + 2/5 = 2/(3x − 1) where x ≠ −1/2, 1/3, and x ∈ ℝ.')
f2 = 'The graph of the function f(x) = 3^x, where x ∈ ℝ, cuts the y-axis at (0, 1) as shown in the diagram below.'
f2g = f2 + ' Part (a)(i): Draw the graph of the function g(x) = 4x + 1 on the diagram.'
A('2-a-i', 'Q2(a)(i)', '5C', [10], [6], '5-1', 'functions', 'Draw the graph of the function g(x) = 4x + 1 on the diagram.', stem=f2)
A('2-a-ii', 'Q2(a)(ii)', '5C', [10], [6], '5-1', 'functions,indices-and-logs', 'Use substitution to verify that f(x) < g(x), for x = 1·9.', stem=f2g)
A('2-b', 'Q2(b)', '15D', [11], [7], '3-1', 'induction', 'Prove, using induction, that f(n) ≥ g(n), where n ≥ 2 and n ∈ ℕ.', stem=f2g)
A('3-a', 'Q3(a)', '5B', [12], [8], '4-1', 'algebra-expressions-factorising', 'Factorise fully: 3xy − 9x + 4y − 12.')
A('3-b', 'Q3(b)', '10D', [12], [8], '3-2', 'indices-and-logs,algebra-expressions-factorising', 'g(x) = 3x ln x − 9x + 4 ln x − 12. Using your answer to part (a) or otherwise, solve g(x) = 0.', stem='Part (a): Factorise fully: 3xy − 9x + 4y − 12.')
A('3-c', 'Q3(c)', '10D', [13], [9], '5-2', 'differentiation-rules', 'Evaluate g′(e) correct to 2 decimal places.', stem='g(x) = 3x ln x − 9x + 4 ln x − 12.')
A('4-a', 'Q4(a)', '5C', [14], [10], '5-2', 'integration', 'Find ∫(4x³ − 6x + 10) dx.')
cub = 'Part of the graph of a cubic function f(x) is shown below (graph not to scale). The graph cuts the x-axis at the three points A(2, 0), B, and C.'
A('4-b-i', 'Q4(b)(i)', '10D', [14], [10], '5-2', 'integration', 'Given that f′(x) = 6x² − 54x + 109, show that f(x) = 2x³ − 27x² + 109x − 126.', stem=cub)
A('4-b-ii', 'Q4(b)(ii)', '10D', [15], [11], '4-2', 'algebra-cubics', 'Find the co-ordinates of the point B and the point C.', stem=cub + ' Part (b)(i): Given that f′(x) = 6x² − 54x + 109, show that f(x) = 2x³ − 27x² + 109x − 126.')
A('5-a', 'Q5(a)', '10C', [16], [12], '4-4', 'complex-numbers', '3 + 2i is a root of z² + pz + q = 0, where p, q ∈ ℝ, and i² = −1. Find the value of p and the value of q.')
vq = 'v = 2 − 2√3i. Write v in the form r(cos θ + i sin θ), where r ∈ ℝ and 0 ≤ θ ≤ 2π.'
A('5-b-i', 'Q5(b)(i)', '5C', [17], [12], '4-4', 'complex-numbers', vq)
A('5-b-ii', 'Q5(b)(ii)', '10C', [17], [13], '4-4', 'complex-numbers', 'Use your answer to part (b)(i) to find the two possible values of w, where w² = v. Give your answers in the form a + ib, where a, b ∈ ℝ.', stem='Part (b)(i): ' + vq)
A('6-a-i', 'Q6(a)(i)', '10C', [18], [14], '3-1', 'algebra-solving-equations', 'Given that x − √32 = √128 − 5x, find the value of x, where x ∈ ℝ. Give your answer in the form a√2, where a ∈ ℕ.')
A('6-a-ii', 'Q6(a)(ii)', '5C', [18], [14], '1-6', 'statistics-descriptive-statistics', 'A = {√(32k²), √(50k²), √(128k²), √(98k²)}, where k ∈ ℕ. Show that the mean of set A is equal to the median of set A.')
A('6-b', 'Q6(b)', '10D', [19], [15], '3-1', 'induction', 'Prove, using contradiction, that √2 is not a rational number.')
can = 'The closed line segment [0, 1] is shown below. The first three steps in the construction of the Cantor Set are also shown: Step 1 removes the open middle third of the line segment [0, 1] leaving two closed line segments (i.e. the end points of the segments remain in the Cantor Set); Step 2 removes the middle third of the two remaining segments leaving four closed line segments; Step 3 removes the middle third of the four remaining segments leaving eight closed line segments. The process continues indefinitely. The set of points in the line segment [0, 1] that are not removed during the process is the Cantor Set.'
ss = 'sequences-series'
A('7-a-i', 'Q7(a)(i)', '10C', [20], [16], '4-1', ss, 'Complete the table below to show the length of the line segment(s) removed at each step for the first 5 steps. Give your answers as fractions. Step: Step 1, Step 2, Step 3, Step 4, Step 5. Length Removed: 1/3, 2/9, _, _, _.', stem=can)
A('7-a-ii', 'Q7(a)(ii)', '5C', [20], [16, 17], '4-1', ss, 'Find the total length of all of the line segments removed from the initial line segment of length 1 unit, after a finite number (n) of steps in the process. Give your answer in terms of n.', stem=can)
A('7-a-iii', 'Q7(a)(iii)', '5C', [20], [16, 17], '4-1', ss, 'Find the total length removed, from the initial line segment, after an infinite number of steps of the process.', stem=can)
A('7-b-i', 'Q7(b)(i)', '10C', [21], [16, 17], '4-1', ss, 'Complete the table below to identify the end-points labelled in the diagram. Give your answers as fractions. Label: A, B, C, D, E, F. End-point: _, _, _, _, _, _.', stem=can)
A('7-b-ii', 'Q7(b)(ii)', '5B', [21], [16, 18], '4-1', ss, 'Give a reason why 1/3 − 1/9 + 1/27 − 1/81 is a point in the Cantor Set.', stem=can)
A('7-b-iii', 'Q7(b)(iii)', '10C', [21], [16, 18], '4-1', ss, 'The limit of the series 1/3 − 1/9 + 1/27 − ⋯ is a point in the Cantor Set. Find this point.', stem=can)
rev = 'The weekly revenue produced by a company manufacturing air conditioning units is seasonal. The revenue (in euro) can be approximated by the function: r(t) = 22 500 cos((π/26)t) + 37 500, t ≥ 0, where t is the number of weeks measured from the beginning of July and ((π/26)t) is in radians.'
tf = 'trigonometry-functions-identities'
A('8-a', 'Q8(a)', '10C', [22], [19], '2-3', tf, 'Find the approximate revenue produced 20 weeks after the beginning of July. Give your answer correct to the nearest euro.', stem=rev)
A('8-b', 'Q8(b)', '10D', [22], [19], '2-3', tf, 'Find the two values of the time t, within the first 52 weeks, when the revenue is approximately €26 250.', stem=rev)
A('8-c', 'Q8(c)', '5C', [23], [20], '5-2', 'differentiation-rules,' + tf, 'Find r′(t), the derivative of r(t) = 22 500 cos((π/26)t) + 37 500.', stem=rev)
A('8-d', 'Q8(d)', '10C', [23], [20], '5-2', 'differentiation-applications', 'Use calculus to show that the revenue is increasing 30 weeks after the beginning of July.', stem=rev)
A('8-e', 'Q8(e)', '15D', [24], [21], '5-2', 'differentiation-applications', 'Find a value for the time t, within the first 52 weeks, when the revenue is at a minimum. Use r′′(t), to verify your answer.', stem=rev)
nw = 'Norman windows consist of a rectangle topped by a semi-circle as shown above. Let the height of the rectangle be y metres and the radius of the semi-circle be x metres as shown. The perimeter of the window is P.'
nwy = nw + ' Part (a)(ii): In a particular Norman window the perimeter P = 12 metres. Show that y = (12 − (2 + π)x)/2 for 0 ≤ x ≤ 12/(2 + π) where x ∈ ℝ.'
A('9-a-i', 'Q9(a)(i)', '5C', [25], [22], '3-4', 'area-volume', 'Write P in terms of x, y, and π.', stem=nw)
A('9-a-ii', 'Q9(a)(ii)', '5C', [25], [22], '4-2', 'algebra-solving-equations', 'In a particular Norman window the perimeter P = 12 metres. Show that y = (12 − (2 + π)x)/2 for 0 ≤ x ≤ 12/(2 + π) where x ∈ ℝ.', stem=nw)
A('9-b-i', 'Q9(b)(i),Q9(b)(ii)', '15D', [26], [23], '5-1', 'functions,co-ordinate-geometry-of-the-line', '(i) Complete the table on the right. x: 0, 12/(2 + π). y = (12 − (2 + π)x)/2: _, _. (ii) On the diagram below, draw the graph of the linear function, y = (12 − (2 + π)x)/2 for 0 ≤ x ≤ 12/(2 + π) where x ∈ ℝ.', stem=nwy)
A('9-b-iii', 'Q9(b)(iii)', '5C', [27], [23], '2-2', 'co-ordinate-geometry-of-the-line', 'Find the slope of the graph of y, correct to 2 decimal places. Interpret this slope in the context of the question.', stem=nwy)
ar = 'The Norman window shown below has a perimeter of 12 metres and y = (12 − (2 + π)x)/2. Show that the function a(x) = (24x − (π + 4)x²)/2 represents the area of the window, in terms of x and π.'
A('9-c-i', 'Q9(c)(i)', '5C', [27], [24], '3-4', 'area-volume,functions', ar, stem=nw)
A('9-c-ii', 'Q9(c)(ii)', '5B', [28], [24], '5-2', 'differentiation-rules', 'Find a′(x).', stem=nw + ' Part (c)(i): ' + ar)
A('9-c-iii', 'Q9(c)(iii)', '15D', [28], [25], '5-2', 'differentiation-applications', 'Find the relationship between x and y when the area of the window in part (c)(i) is at its maximum.', stem=nw + ' Part (c)(i): ' + ar)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 45, '8': 50, '9': 55}
p.check(marks, 35)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 1–29 of the combined Higher Level scheme (cover, notes, contents, the Paper 1 scale table on page 4, the summary of mark allocations on page 5, the annotation notes on pages 6–7, every Paper 1 model solution and marking note on pages 8–28, and the Paper 2 title page 29). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 30)), [4, 5],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 45 marks, Q8 50 marks, Q9 55 marks). Every question is retained.',
     '35 independently marked units, matching the printed summary of allocations on scheme page 5. Q9(b)(i) and (ii) share one 15D scale (“(b)(i)+(ii)”) and are one task.',
     'Paper 1 bands from the 2019 scale table on scheme page 4, which differ from later years: 5B 0,2,5; 5C 0,2,3,5; 10C 0,4,7,10; 10D 0,4,5,8,10; 15D 0,4,7,11,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 35 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; Q5(a) and Q6(a)(i) keep each printed method’s ladder separately. Tables in prompts carry the printed values with blanks for the cells the candidate fills.',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [8], 'wording': 'Using your answer to part (a) or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2019 Higher Level Paper 1', expect_added=[c['id'] for c in p.cards])
