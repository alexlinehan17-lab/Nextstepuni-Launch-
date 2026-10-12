"""2018 HL Paper 1: a new paper — 33 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ACC = 'Accept'

ROWS = {
 'maths-2018-hl-p1-q1-a': [L(SOL, '2x + 3y − z = −4 × (2)'), L(SOL, '3x + 2y + 2z = 14 × (−3)'), L(SOL, '4x + 6y − 2z = −8'),
     L(SOL, '−9x − 6y − 6z = −42'), L(SOL, '−5x − 8z = −50'), L(SOL, 'x − 3z = −13 × (5)'), L(SOL, '5x − 15z = −65'),
     L(SOL, '−23z = −115'), L(SOL, 'z = 5 ⇒ x = 2 ⇒ y = −1 {2, −1, 5}'),
     L(LPC, 'Matches coefficient of 1 variable in 2 equations'), L(LPC, 'Writes x in terms of z in eq (iii)'),
     L(MPC, '1 unknown found with errors'), L(MPC, 'Eliminates one unknown'), L(MPC, '1 unknown found and stops'), L(HPC, '2 unknowns found')],
 'maths-2018-hl-p1-q1-b': [L(SOL, '(2x − 3)/(x + 2) ≥ 3 × (x + 2)²'), L(SOL, '(2x − 3)(x + 2) ≥ 3(x + 2)²'), L(SOL, '2x² + x − 6 ≥ 3x² + 12x + 12'),
     L(SOL, 'x² + 11x + 18 ≤ 0'), L(SOL, '(x + 2)(x + 9) ≤ 0'), L(SOL, '−9 ≤ x < −2'), L(LPC, 'Use of (x + 2)²'),
     L(LPC, 'Relevant work but with linear inequality'), L(LPC, 'Squares both sides with some subsequent work (low partial credit at most)'),
     L(MPC, 'Quadratic inequality involving 0'), L(HPC, 'Roots of quadratic found'), L(NOTE, 'Accept −9 ≤ x ≤ −2')],
 'maths-2018-hl-p1-q2-a': [L(SOL, '(5x − 8)/x² = (x + 8)/(5x − 8)'), L(SOL, '(5x − 8)² = x²(x + 8)'), L(SOL, '25x² − 80x + 64 = x³ + 8x²'),
     L(SOL, 'x³ − 17x² + 80x − 64 = 0'), L(LPC, '(5x − 8)/x² or (x + 8)/(5x − 8)'),
     L(LPC, 'Some effort at finding r in a geometric sequence (must use at least one of the terms)'), L(LPC, 'r = Tn/Tn−1 or similar'),
     L(HPC, '(5x − 8)/x² = (x + 8)/(5x − 8)'), L(HPC, '(5x − 8)² and x²(x + 8)'), L(ZC, 'Treats as an arithmetic sequence')],
 'maths-2018-hl-p1-q2-b': [L(SOL, 'f(1) = (1)³ − 17(1)² + 80(1) − 64 = 0'), L(SOL, '⇒ (x − 1) is a factor'), L(SOL, 'x²(x − 1) − 16x(x − 1) + 64(x − 1)'),
     L(SOL, 'x² − 16x + 64 = 0'), L(SOL, '(x − 8)(x − 8) = 0'), L(SOL, 'x = 8'), L(LPC, 'Shows f(1) = 0'), L(LPC, 'Any correct substitution'),
     L(HPC, 'Quotient in quadratic form found'), L(NOTE, 'Accept x = 8 without work if f(1) = 0 has been shown')],
 'maths-2018-hl-p1-q2-c': [L(SOL, 'x = 1: 1², 5(1) − 8, 1 + 8'), L(SOL, '1, −3, 9 which doesn′t have a sum to infinity (|r| > 1)'),
     L(SOL, 'x = 8: 8², 5(8) − 8, 8 + 8'), L(SOL, '64, 32, 16 …. a = 64 and r = 1/2'), L(SOL, 'S∞ = a/(1 − r) = 64/(1 − 1/2) = 64/(1/2) = 128'),
     L(LPC, 'Substitution used to identify x = 8 as the required value'), L(LPC, 'Substitution used to exclude x = 1 as the required value'),
     L(LPC, 'Finds a/(1 − r) for x = 1'), L(LPC, 'S∞ = x²/(1 − (5x − 8)/x²)'), L(LPC, 'Relevant substitution into correct formula'),
     L(HPC, 'GP identified (a and r)'),
     L(HPC, 'If the candidate works with both x = 1 and x = 8 but fails to eliminate x = 1 or chooses the incorrect answer'),
     L(NOTE, 'if |r| > 1 then Low Partial Credit at most')],
 'maths-2018-hl-p1-q3-a': [L(SOL, 'ℎ′(x) = −2 sin(2x)'), L(SOL, 'At x = π/3: ℎ′(π/3) = −2 sin(2π/3) = −2(√3/2) = −√3'), L(SOL, 'tan θ = −√3'),
     L(SOL, 'θ = 120°'), L(LPC, 'Differentiation indicated'), L(LPC, 'Use of 2'), L(MPC, 'Derivative found'), L(HPC, 'tan θ = evaluated derivative'),
     L(HPC, 'θ = −60°'), L(NOTE, 'Must use differentiation to gain any credit'), L(NOTE, 'If integration symbol appears then 0 credit')],
 'maths-2018-hl-p1-q3-b': [L(SOL, '1/(π/4 − 0) ∫ cos(2x) dx'), L(SOL, '= 4/π (sin(2x)/2)'),
     L(SOL, '= 4/π (sin(π/2)/2 − sin 0/2)'), L(SOL, '= 4/π (1/2) = 2/π'), L(LPC, 'Integration indicated'),
     L(MPC, 'cos 2x integrated correctly (sin(2x)/2)'), L(MPC, '−2 sin 2x and finishes correctly'),
     L(HPC, 'Substitutes limits into integral and stops'), L(HPC, 'Integral evaluated at x = π/4 (i.e. omits 1/(π/4 − 0)) and finishes'),
     L(NOTE, 'errors in integration could include An error in the trig function (including sign)'), L(NOTE, 'An error in the angle'),
     L(NOTE, 'An error in the application of the chain rule'), L(NOTE, 'Must have integration to gain any credit')],
 'maths-2018-hl-p1-q4-a': [L(SOL, 'P(1) (cos θ + i sin θ)¹ = cos(1θ) + i sin(1θ)'), L(SOL, 'P(k): Assume (cos θ + i sin θ)^k = cos(kθ) + i sin(kθ)'),
     L(SOL, 'Test P(k + 1): (cos θ + i sin θ)^(k+1) = = cos(k + 1)θ + i sin(k + 1)θ'),
     L(SOL, '(cos θ + i sin θ)^(k+1) = (cos θ + i sin θ)^k . (cos θ + i sin θ)¹'), L(SOL, '= (cos(kθ) + i sin(kθ)). (cos θ + i sin θ)'),
     L(SOL, '= [cos(kθ) cos θ − sin(kθ) sin θ] + i[cos(kθ) sin θ + cos θ sin(kθ)]'), L(SOL, '= cos(k + 1)θ + i sin(k + 1)θ'),
     L(SOL, 'Thus the proposition is true for n = k + 1 provided it is true for n = k but it is true for n = 1 and therefore true for all positive integers.'),
     L(LPC, 'Step P(1)'), L(MPC, 'Step P(k) or Step P(k + 1)'), L(HPC, 'Uses Step P(k) to prove Step P(k + 1)'),
     L(NOTE, 'Accept Step P(1), Step P(k), Step P(k + 1) in any order'), L(FCM, 'Omits conclusion but otherwise correct'),
     L(FC, '[r(cos θ + i sin θ)]^n = r^n (cos(nθ) + i sin(nθ)) proved correctly')],
 'maths-2018-hl-p1-q4-b': [L(SOL, '(−1/2 + (√3/2)i)³ = 1(cos 2π/3 + i sin 2π/3)³'), L(SOL, '= (cos(3) 2π/3 + i sin(3) 2π/3)'),
     L(SOL, '= (cos 2π + i sin 2π) = 1 + 0i = 1'), L(LPC, 'Modulus or argument correct'), L(LPC, 'Some correct multiplication'),
     L(LPC, 'Apply De Moivre correctly with incorrect modulus and argument'), L(HPC, '(cos(3) 2π/3 + i sin(3) 2π/3)'),
     L(HPC, 'Multiplication correct but un-simplified'), L(FCM, 'cos 2π + i sin 2π or cos 360° + i sin 360°'),
     L(ACC, 'Answer with reference to cube root of unity')],
 'maths-2018-hl-p1-q5-a-i': [L(SOL, 'row 2: S45 = 45/2 [14 + 44(5)] = 5265'), L(SOL, 'row 1: S45 = 45/2 [8 + 44(3)] = 3150'), L(SOL, '∴ Difference = 2115'),
     L(LPC, 'Formulates S45 for row 1 or row 2'), L(LPC, '3+5+7 …'), L(LPC, 'Identifies a or r for either row 1 or row 2'),
     L(HPC, 'S45 found for row 1 or row 2'), L(FCM, 'Fails to subtract')],
 'maths-2018-hl-p1-q5-a-ii': [L(SOL, 'T1 (in row 60): T60 = 4 + (60 − 1)3 = 181'), L(SOL, 'T2 (in row 60) = T60 of 7, 12, 17, 22 ….'),
     L(SOL, 'T60 = 7 + (60 − 1)5 = 302'), L(SOL, '∴ T70 of 181, 302, … …. = 181 + (70 − 1)121 = 8530'),
     L(LPC, 'Identifies T60 in column 1 or T70 In row 1 or equivalent'), L(LPC, 'Some relevant substitution into correct formula'),
     L(LPC, 'Identifies a or d for either row 1 or row 2'), L(MPC, 'Finds a in row 60 or row 70'), L(MPC, 'Finds d in row 60 or row 70'),
     L(HPC, 'Formulates substituted expression for T70 in row 60 or T60 in column 70'), L(HPC, 'Finds both a and d in row 60 or row 70')],
 'maths-2018-hl-p1-q5-b': [L(SOL, 'a₃ = a₂ − a₁ = 2 − 4 = −2'), L(SOL, 'a₄ = a₃ − a₂ = −2 − 2 = −4'), L(SOL, 'a₅ = a₄ − a₃ = −4 − (−2) = −2'),
     L(SOL, 'a₆ = a₅ − a₄ = −2 − (−4) = 2'), L(SOL, 'a₇ = a₆ − a₅ = 2 − (−2) = 4'), L(SOL, 'a₈ = a₇ − a₆ = 4 − 2 = 2'),
     L(SOL, 'Therefore, the sequence consists of a repeating pattern of 4, 2, −2, −4, −2, 2'), L(SOL, '∴ a₂₀₁₆ = 2 (multiple of 6)'),
     L(SOL, '⇒ a₂₀₁₉ = −2'), L(LPC, 'a₃ = −2'), L(LPC, 'a₃ = a₂ − a₁ or similar'), L(HPC, 'Any 4 from a₃, a₄, a₅, a₆, a₇ and a₈ found'),
     L(FCM, 'a₃, a₄, a₅, a₆, and a₂₀₁₉ found')],
 'maths-2018-hl-p1-q6-a': [L(SOL, 'x³ = x'), L(SOL, '⟹ x³ − x = 0'), L(SOL, '⟹ x(x² − 1) = 0'), L(SOL, 'x(x − 1)(x + 1) = 0'), L(SOL, 'x = 0 or x = ±1'),
     L(SOL, '(−1, −1), (0, 0), (1, 1)'), L(LPC, 'Equation written'), L(LPC, 'One correct solution from the graph'),
     L(LPC, 'Solution of the form (a, a) where a ≠ 0, 1'), L(HPC, 'Equation factorised (3 factors)'), L(HPC, '2 correct points'), L(HPC, 'x values only')],
 'maths-2018-hl-p1-q6-b-i': [L(SOL + ', limits 0 to 1', '2 ∫ x − x³ dx'), L(SOL, '= 2[x²/2 − x⁴/4] = 2[1/2 − 1/4 − 0] = 1/2 unit²'),
     L(LPC, 'Integral indicated'), L(LPC, 'One relevant area found'), L(HPC, 'Integral evaluated at x = 1 (upper limit)'),
     L(HPC + ', limits −1 to 1', '∫ x − x³ dx = 0')],
 'maths-2018-hl-p1-q6-b-ii': [L(SOL, 'k⁻¹(x) = x^(1/3)'), L(PC, 'Incomplete image'), L(PC, '2 correct image points')],
 'maths-2018-hl-p1-q7-a': [L(SOL, '35·96 = k ln(1 − 35/80)'), L(SOL, '35·96 = k ln(45/80)'), L(SOL, 'k = 35·96/ln(45/80)'),
     L(SOL, 'k = −62·5 to one place of decimals'), L(LPC, 'Effort at transposing'), L(LPC, 'Some substitution into function'),
     L(LPC, 'Full substitution and stops'), L(HPC, 'Function written in terms of k and fully substituted'),
     L(HPC, 'One incorrect substitution worked correctly and with some reference to k ≠ −62·5')],
 'maths-2018-hl-p1-q7-b': [L(SOL, '100 = −62·5 ln(1 − x/80)'), L(SOL, '100/(−62·5) = ln(1 − x/80)'), L(SOL, 'e^(100/(−62·5)) = 1 − x/80'),
     L(SOL, 'x = −80(e^(100/(−62·5)) − 1)'), L(SOL, 'x = 64 wpm (To the nearest whole number)'), L(LPC, 'Some substitution into function'),
     L(LPC, 'Trial and improvement (more than 1 iteration)'), L(LPC, 'Correct answer without work'), L(HPC, 'e^(100/(−62·5)) = 1 − x/80'),
     L(HPC, 'Equation rewritten in terms of x or x/80 =')],
 'maths-2018-hl-p1-q7-c': [L(SOL, '0, 8, 18, 29, 43, 61, 87, 130'), L(LPC, 'One entry correct'), L(LPC, 'One plot (from candidates table) correct'),
     L(MPC, '4 entries correct and 4 plots of table values'),
     L(HPC, 'All plots consistent with candidates table values (with at least 1 correct value)'), L(HPC, 'Table correct but incorrect plots')],
 'maths-2018-hl-p1-q7-d': [L(LPC, 'One point on line identified'), L(LPC, 'One point (not origin) plotted'), L(HPC, '2 points on line identified and plotted')],
 'maths-2018-hl-p1-q7-e-i': [L(SOL, 'Approx 62 wpm'), L(PC, 'Point of intersection indicated on graph'), L(PC, 'h(x) written in terms of x'),
     L(NOTE, 'Tolerance: ± 2 wpm')],
 'maths-2018-hl-p1-q7-e-ii': [L(SOL, 'For Maximum Value: Set ℎ′(x) = 0'), L(SOL, 'ℎ(x) = 1·5x + 62·5 ln(1 − x/80)'),
     L(SOL, '62·5/(80 − x) = 1·5'), L(SOL, 'x = 80 − 62·5/1·5'),
     L(SOL, 'x = 38·3 = 38 words'), L(SOL, 'ℎ(38 1/3) = 1·5(38 1/3) + 62·5 ln(1 − (38 1/3)/80) = 16·73'), L(SOL, '= 17 days'),
     L(LPC, 'Any correct differentiation'), L(LPC, 'ℎ(x) = 1·5x + 62·5 ln(1 − x/80)'), L(LPC, 'ℎ′(x) = 0'),
     L(HPC, 'Differentiation correct but un-simplified'), L(HPC, 'Value for x and stops')],
 'maths-2018-hl-p1-q8-a': [L(SOL, '= (1/√(2π))(1)'),
     L(SOL, '∴ (0, 1/√(2π)) is the y intercept'), L(LPC, 'x = 0'), L(LPC, 'Value for x substituted into f(x)'), L(HPC, '1/√(2π)'),
     L(FCM, '(0, 0·3989)')],
 'maths-2018-hl-p1-q8-b': [L(SOL, '= 0·484 Units²'), L(LPC, 'length = 2'), L(LPC, 'Width = [y co-ordinate]'),
     L(HPC, '[(1)(1/√(2πe))]'), L(FCM, 'Area = −0·484'), L(ZC, 'Integrating original function')],
 'maths-2018-hl-p1-q8-c': [L(SOL, 'C(1, 1/√(2πe)) due to symmetry'), L(SOL, '⟹ Decreasing'),
     L(LPC, 'x = 1 identified'), L(LPC, 'Some correct differentiation'), L(LPC, 'Indicates significance of dy/dx < 0'), L(HPC, 'Derivative found')],
 'maths-2018-hl-p1-q8-d': [L(SOL, 'f′′(−1) = 0 as 1² − 1 = 0'), L(SOL, '⟹ point of inflection at x = −1'), L(LPC, 'f′(x) transferred or found'),
     L(LPC, 'Mention of f′′(x)'), L(LPC, 'Identifies x = −1'), L(MPC, 'f′′(x) identified and some correct differentiation'), L(HPC, 'f′′(x) found'),
     L(NOTE, 'if the product rule and chain rule are not applied in finding f′′(x) then the candidate can be awarded mid partial credit at most')],
 'maths-2018-hl-p1-q9-a': [L(LPC, 'One correct entry'), L(HPC, 'Three correct entries'), L(FCM, 'Answers as decimals')],
 'maths-2018-hl-p1-q9-b-i': [L(SOL, '3^n'), L(PC, '3n written'), L(PC, 'n³ written'), L(FCM, '3^(n−1) written')],
 'maths-2018-hl-p1-q9-b-ii': [L(SOL, '3^k > 1,000,000,000'), L(SOL, 'log₃ 3^k > log₃ 1 000 000 000'), L(SOL, 'k log₃ 3 > log₃ 1 000 000 000'),
     L(SOL, 'k > log₃ 1 × 10⁹'), L(SOL, 'k > 18·863'), L(SOL, 'k = 19'), L(LPC, '3^k > 1,000,000,000'),
     L(HPC, 'Inequality with k not written as an index'), L(NOTE, 'if 3k or k³ from above used fully here then award low partial credit at most')],
 'maths-2018-hl-p1-q9-c-i': [L(SOL, 'ln (3/4)^ℎ < ln 1/100'), L(SOL, 'ℎ ln (3/4) < ln 1/100'),
     L(SOL, 'ℎ > ln(1/100)/ln(3/4)'), L(SOL, 'ℎ > 16·007'), L(SOL, '⇒ ℎ = 17'), L(LPC, 'Correct answer without work'),
     L(LPC, '(3/4)^ℎ or candidates ratio to the power of ℎ'), L(LPC, 'r = 3/4'), L(LPC, 'Lists two or more terms'),
     L(HPC, 'Inequality with ℎ not written as an index'), L(FCM, '(3/4)^(ℎ−1) < 1/100 and finishes correctly')],
 'maths-2018-hl-p1-q9-c-ii': [L(SOL, 'lim n→∞ (3/4)^n = 0'), L(SOL, '⟹ Fraction remaining = 0'), L(PC, 'lim n→∞'), L(PC, 'Some use of 3/4'),
     L(FC, 'Correct answer without work'), L(FC, '1/∞ or equivalent')],
 'maths-2018-hl-p1-q9-d-i': [L(SOL, '3, 9/2, 27/4, 81/8, 243/16'), L(LPC, 'One correct entry'),
     L(LPC, 'All numerators correct with all incorrect denominators'), L(LPC, 'All denominators correct with all incorrect numerators'),
     L(HPC, 'Two correct entries')],
 'maths-2018-hl-p1-q9-d-ii': [L(SOL, 'Pattern: 3¹/2⁰, 3²/2¹, 3³/2² … … …. 3^(n+1)/2^n'), L(SOL, '∴ step 35 = 3³⁶/2³⁵'), L(SOL, '= 4 368 329'),
     L(SOL, 'Or T35 = (9/2)(3/2)³⁴ = 4 368 329'), L(SOL, 'Or T35 = (3)(3/2)³⁵ = 4 368 329'), L(LPC, 'Pattern identified'),
     L(LPC, 'Recognises r = 3/2'), L(LPC, 'Some relevant substitution into Tn = ar^(n−1)'), L(LPC, 'a = 3 or a = 4·5'),
     L(HPC, 'Step 35 = 3³⁶/2³⁵ or equivalent'), L(FCM, 'T35 = (3)(3/2)³⁴')],
 'maths-2018-hl-p1-q9-d-iii': [L(SOL, 'Area = 0'), L(SOL, 'lim n→∞ (3^(n+1)/2^n) = ∞'), L(SOL, '⟹ Perimeter → ∞'),
     L(LPC, 'lim n→∞ (3^(n+1)/2^n) or equivalent'), L(LPC, 'Area is getting smaller'), L(LPC, 'Perimeter is increasing'),
     L(HPC, 'Area approaches 0'), L(HPC, 'Perimeter → ∞ identified'), L(HPC, 'Area is getting smaller and Perimeter is increasing')],
}
# Parts whose printed model solution cannot be lifted as text (a stacked-fraction
# numerator extracts as a lone "1", filtered as a mark cell) or is printed as an
# image (a table or a graph) carry the SEC's own print of their scheme row --
# model solution and every credit band -- shown only after the reveal.
# Crops: scheme_row_figures.py; ids are its output.
SCHEME_ROW_FIGURES = {
    'maths-2018-hl-p1-q3-b': 'maths-2018-HL-scheme-p011-i0',
    'maths-2018-hl-p1-q6-b-ii': 'maths-2018-HL-scheme-p014-i0',
    'maths-2018-hl-p1-q7-c': 'maths-2018-HL-scheme-p015-i0',
    'maths-2018-hl-p1-q7-d': 'maths-2018-HL-scheme-p016-i0',
    'maths-2018-hl-p1-q7-e-ii': 'maths-2018-HL-scheme-p016-i1',
    'maths-2018-hl-p1-q8-a': 'maths-2018-HL-scheme-p017-i0',
    'maths-2018-hl-p1-q8-b': 'maths-2018-HL-scheme-p017-i1',
    'maths-2018-hl-p1-q8-c': 'maths-2018-HL-scheme-p017-i2',
    'maths-2018-hl-p1-q8-d': 'maths-2018-HL-scheme-p018-i0',
    'maths-2018-hl-p1-q9-a': 'maths-2018-HL-scheme-p019-i0',
    'maths-2018-hl-p1-q9-c-i': 'maths-2018-HL-scheme-p020-i0',
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2018, 'hl', 'p1', {'5B': [0, 2, 5], '5C': [0, 3, 4, 5], '10C': [0, 4, 8, 10], '10D': [0, 3, 5, 8, 10], '15C': [0, 5, 10, 15],
                             '15D': [0, 5, 7, 11, 15], '20D': [0, 5, 10, 15, 20]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
A('1-a', 'Q1(a)', '15D', [8], [3], '4-2', 'algebra-simultaneous-equations', 'Solve the simultaneous equations. 2x + 3y − z = −4; 3x + 2y + 2z = 14; x − 3z = −13.')
A('1-b', 'Q1(b)', '10D', [8], [3], '4-3', 'algebra-inequalities', 'Solve the inequality (2x − 3)/(x + 2) ≥ 3, where x ∈ ℝ and x ≠ −2.')
gs = 'The first three terms of a geometric series are x², 5x − 8, and x + 8, where x ∈ ℝ.'
fb = 'If f(x) = x³ − 17x² + 80x − 64, x ∈ ℝ, show that f(1) = 0, and find another value of x for which f(x) = 0.'
A('2-a', 'Q2(a)', '10C', [9], [4], '4-1', 'sequences-series,algebra-cubics', gs + ' Use the common ratio to show that x³ − 17x² + 80x − 64 = 0.')
A('2-b', 'Q2(b)', '10C', [9], [4], '4-2', 'algebra-cubics', fb)
A('2-c', 'Q2(c)', '5C', [10], [4, 5], '4-1', 'sequences-series', 'In the case of one of the values of x from part (b), the terms in part (a) will generate a geometric series with a finite sum to infinity. Find this value of x and hence find the sum to infinity.',
  stem=gs + ' Part (b): ' + fb)
ha = 'Let h(x) = cos(2x), where x ∈ ℝ.'
A('3-a', 'Q3(a)', '10D', [11], [6], '5-2', 'differentiation-applications,trigonometry-functions-identities', ha + ' A tangent is drawn to the graph of h(x) at the point where x = π/3. Find the angle that this tangent makes with the positive sense of the x-axis.')
A('3-b', 'Q3(b)', '15D', [11], [6], '5-2', 'integration', 'Find the average value of h(x) over the interval 0 ≤ x ≤ π/4, x ∈ ℝ. Give your answer in terms of π.', stem=ha)
dm = 'Prove, using induction, that if n is a positive integer then (cos θ + i sin θ)^n = cos(nθ) + i sin(nθ), where i² = −1.'
A('4-a', 'Q4(a)', '15D', [12], [7], '4-4', 'complex-numbers,induction', dm)
A('4-b', 'Q4(b)', '10C', [12], [7], '4-4', 'complex-numbers', 'Hence, or otherwise, find (−1/2 + (√3/2)i)³ in its simplest form.', stem='Part (a): ' + dm)
sv = 'The Sieve of Sundaram is an infinite table of arithmetic sequences. The terms in the first 4 rows and the first 4 columns of the table are shown below. 4, 7, 10, 13; 7, 12, 17, 22; 10, 17, 24, 31; 13, 22, 31, 40.'
ss = 'sequences-series'
A('5-a-i', 'Q5(a)(i)', '10C', [13], [8], '4-1', ss, 'Find the difference between the sums of the first 45 terms in the first two rows.', stem=sv)
A('5-a-ii', 'Q5(a)(ii)', '10D', [13], [8], '4-1', ss, 'Find the number which is in the 60th row and 70th column of the table.', stem=sv)
A('5-b', 'Q5(b)', '5C', [13], [9], '4-1', ss, 'The first two terms of a sequence are a₁ = 4 and a₂ = 2. The general term is defined by aₙ = aₙ₋₁ − aₙ₋₂, when n ≥ 3. Write out the next 6 terms of the sequence and hence find the value of a₂₀₁₉.')
hk = 'Parts of the graphs of the functions h(x) = x and k(x) = x³, x ∈ ℝ, are shown in the diagram below.'
A('6-a', 'Q6(a)', '10C', [14], [10], '5-1', 'functions', 'Find the co-ordinates of the points of intersection of the graphs of the two functions.', stem=hk)
A('6-b-i', 'Q6(b)(i)', '10C', [14], [10, 11], '5-2', 'integration', 'Find the total area enclosed between the graphs of the two functions.', stem=hk)
A('6-b-ii', 'Q6(b)(ii)', '5B', [14], [10, 11], '5-1', 'functions', 'On the diagram on the previous page, using symmetry or otherwise, draw the graph of k⁻¹, the inverse function of k.', stem=hk)
ty = 'The time, in days of practice, it takes Jack to learn to type x words per minute (wpm) can be modelled by the function: t(x) = k[ln(1 − x/80)], where 0 ≤ x ≤ 70, x ∈ ℝ, and k is a constant.'
q7a = 'Based on the function t(x), Jack can learn to type 35 wpm in 35·96 days. Write the function above in terms of k and hence show that k = −62·5, correct to 1 decimal place.'
q7c = 'Complete the table below, correct to the nearest whole number and hence draw the graph of t(x) for 0 ≤ x ≤ 70, x ∈ ℝ.'
q7d = 'A simpler function that could also be used to model the number of days needed to attain x wpm is p(x) = 1·5x. Draw, on the diagram above, the graph of p(x) for 0 ≤ x ≤ 70, x ∈ ℝ.'
ty_a = ty + ' Part (a): ' + q7a
A('7-a', 'Q7(a)', '15C', [15], [12], '3-2', 'indices-and-logs', q7a, stem=ty)
A('7-b', 'Q7(b)', '5C', [15], [12], '3-2', 'indices-and-logs', 'Find the number of wpm that Jack can learn to type with 100 days of practice. Give your answer correct to the nearest whole number.', stem=ty_a)
A('7-c', 'Q7(c)', '20D', [15], [12, 13], '5-1', 'functions', q7c + ' x (wpm): 0, 10, 20, 30, 40, 50, 60, 70. t(x) (days): _, _, _, _, _, _, _, _.', stem=ty_a)
A('7-d', 'Q7(d)', '5C', [16], [12, 13], '5-1', 'functions', q7d, stem=ty_a + ' Part (c): ' + q7c)
A('7-e-i', 'Q7(e)(i)', '5B', [16], [12, 13], '5-1', 'functions', 'Let h(x) = p(x) − t(x). Use your graphs above to estimate the solution to h(x) = 0 for x > 0.', stem=ty_a + ' Part (c): ' + q7c + ' Part (d): ' + q7d)
A('7-e-ii', 'Q7(e)(ii)', '5C', [16], [12, 13], '5-2', 'differentiation-applications', 'Let h(x) = p(x) − t(x). Use calculus to find the maximum value of h(x) for 0 ≤ x ≤ 70, x ∈ ℝ. Give your answer correct to the nearest whole number.', stem=ty_a + ' Part (d): ' + q7d)
nf = 'The graph of the symmetric function f(x) = (1/√(2π)) e^(−(1/2)x²) is shown below.'
nb = nf + ' Part (b): The co-ordinates of B are (−1, 1/√(2πe)).'
A('8-a', 'Q8(a)', '10C', [17], [14], '5-1', 'functions', 'Find the co-ordinates of A, the point where the graph intersects the y-axis. Give your answer in terms of π.', stem=nf)
A('8-b', 'Q8(b)', '10C', [17], [14], '5-1', 'functions', 'The co-ordinates of B are (−1, 1/√(2πe)). Find the area of the shaded rectangle in the diagram above. Give your answer correct to 3 decimal places.', stem=nf)
A('8-c', 'Q8(c)', '10C', [17], [14], '5-2', 'differentiation-applications', 'Use calculus to show that f(x) is decreasing at C.', stem=nb)
A('8-d', 'Q8(d)', '10D', [18], [14, 15], '5-2', 'differentiation-applications', 'Show that the graph of f(x) has a point of inflection at B.', stem=nb)
st = 'The diagram below shows the first 4 steps of an infinite pattern which creates the Sierpinski Triangle. The sequence begins with a black equilateral triangle. Each step is formed by removing an equilateral triangle from the centre of each black triangle in the previous step, as shown. Each equilateral triangle that is removed is formed by joining the midpoints of the sides of a black triangle from the previous step.'
pd = 'The side length of the triangle in Step 0 is 1 unit. The table below shows the total perimeter of all the black triangles in each of the first 5 steps.'
A('9-a', 'Q9(a)', '10C', [19], [16], '4-1', ss, 'The table below shows the number of black triangles at each of the first 4 steps and the fraction of the original triangle remaining at each step. Complete the table. Step: 0, 1, 2, 3. Number of black triangles: 1, _, _, _. Fraction of the original triangle remaining: 1, _, 9/16, _.', stem=st)
A('9-b-i', 'Q9(b)(i)', '5B', [19], [16], '4-1', ss, 'Write an expression in terms of n for the number of black triangles in step n of the pattern.', stem=st)
A('9-b-ii', 'Q9(b)(ii)', '5C', [19], [16], '3-2', 'indices-and-logs,' + ss, 'Step k is the first step of the pattern in which the number of black triangles exceeds one thousand million (i.e. 1 × 10⁹) for the first time. Find the value of k.', stem=st)
A('9-c-i', 'Q9(c)(i)', '10C', [20], [16, 17], '3-2', 'indices-and-logs,' + ss, 'Step h is the first step of the pattern in which the fraction of the original triangle remaining is less than 1/100 of the original triangle. Find the value of h.', stem=st)
A('9-c-ii', 'Q9(c)(ii)', '5B', [20], [16, 17], '4-1', ss, 'What fraction of the original triangle remains after an infinite number of steps of the pattern?', stem=st)
A('9-d-i', 'Q9(d)(i)', '10C', [20], [16, 18], '4-1', ss, pd + ' Complete the table below. Step: 0, 1, 2, 3, 4. Perimeter: 3, _, 27/4, _, _.', stem=st)
A('9-d-ii', 'Q9(d)(ii)', '5C', [21], [16, 18], '4-1', ss, 'Find the total perimeter of the black triangles in step 35 of the pattern. Give your answer correct to the nearest unit.', stem=st + ' Part (d)(i): ' + pd)
A('9-d-iii', 'Q9(d)(iii)', '5C', [21], [16, 17, 18], '4-1', ss, 'Use your answers to part (c)(ii) and part (d)(ii) to comment on the total area and the total perimeter of the black triangles in step n of the pattern, as n tends to infinity.', stem=st + ' Part (d)(i): ' + pd)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 40, '9': 55}
p.check(marks, 33)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 1–23 of the combined Higher Level scheme (cover, notes, contents, the Paper 1 title page 5, the scale table on page 6, the summary of mark allocations on page 7, every Paper 1 model solution and marking note on pages 8–21, the blank page 22 and the Paper 2 title page 23). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 24)), [6, 7],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 40 marks, Q9 55 marks). Every question is retained.',
     '33 independently marked units, matching the printed summary of allocations on scheme page 7.',
     'Paper 1 bands from the 2018 scale table on scheme page 6: 5B 0,2,5; 5C 0,3,4,5; 10C 0,4,8,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,5,7,11,15; 20D 0,5,10,15,20. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 33 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from. Lines whose stacked-fraction numerator extracts as a lone "1" (the f(x), f′(x) and f′′(x) working in Q8, one line each in Q7(e)(ii) and Q9(c)(i)) cannot be checked as text, and the model solutions of Q9(a) (a table) and Q6(b)(ii), Q7(c) and Q7(d) (graphs) are printed as images. Those parts, and Q3(b) whose integral limits the text layer cannot carry, eleven in all (Q3(b), Q6(b)(ii), Q7(c), Q7(d), Q7(e)(ii), Q8(a)–(d), Q9(a), Q9(c)(i)), carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal. The Q6(b)(i) integral limits are named in the row label.',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 12], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [7, 11], 'wording': 'Hence, or otherwise / using symmetry or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'},
     {'pages': [5], 'wording': 'In the case of one of the values of x from part (b)', 'classification': 'mathematical-context',
      'reason': 'The candidate identifies which value of x gives a finite sum to infinity; it is part of the one required task, not a choice between printed prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t
        else ('mathematical-context', 'One of the two values of x found in part (b) gives a finite sum to infinity; identifying it is part of the one required task, not a choice between printed prompts.') if 'one of the values' in t else None)
p.apply(ROWS, '2018 Higher Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()})
