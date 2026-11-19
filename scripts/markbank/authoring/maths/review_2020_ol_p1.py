"""2020 OL Paper 1: a new paper — 40 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
SUB = [L(LPC, 'Some relevant substitution into formula'), L(HPC, 'Formula fully substituted')]

ROWS = {
 'maths-2020-ol-p1-q1-a-i': [L(SOL, '45 × 12·60 + (350 − 200) × 0·22'), L(SOL, '= €600'), L(LPC, '45 × 12·60'), L(LPC, '(350) × 0·22'),
     L(LPC, '(200) × 0·22'), L(HPC, '45 × 12·60 + (350 − 200) × 0·22'), L(HPC, 'Either pay found'), L(NOTE, 'Accept correct answer without work'),
     L(NOTE, '45 × 12·60 + (350) × 0·22 finished correctly merits HPC')],
 'maths-2020-ol-p1-q1-a-ii': [L(SOL, '48 × 12·60 + 3(12·6 × 1·5) = 661·50'), L(SOL, '(713·20 − 661·50) ÷ 0·22 = €235·00'), L(SOL, '€235·00 + 200 = €435·00'),
     L(LPC, '48 × 12·60'), L(LPC, '3(12·6)'), L(MPC, 'Commission found or €661·50'), L(HPC, '(713·20 − 661·50) ÷ 0·22')],
 'maths-2020-ol-p1-q1-b': [L(SOL, '678 × 0·20 + (713·20 − 678) × 0·40'), L(SOL, '= €149·68'), L(SOL, '€149·68 − 26 = 123·68'), L(SOL, '€713·20 − 123·68'),
     L(SOL, '= €589·52 Net Income'), L(LPC, '678 × 0·20'), L(LPC, '713·20 − 678'), L(MPC, 'Gross tax found'), L(HPC, 'Net tax found')],
 'maths-2020-ol-p1-q2-a': [L(SOL, '12((9x − 6)/2) = 12((3x − 14)/3) + 12(9x/4)'), L(SOL, '6(9x − 6) = 4(3x − 14) + 3(9x)'), L(SOL, '54x − 36 = 12x − 56 + 27x'),
     L(SOL, 'x = −20/15 or −4/3'), L(LPC, '12 identified as common denominator'), L(LPC, 'Some relevant multiplication'),
     L(LPC, '4(3x − 14) = 3(9x) without CD'), L(HPC, '54x − 36 = 12x − 56 + 27x or equivalent')],
 'maths-2020-ol-p1-q2-b': [L(SOL, 'y = 3x − 4'), L(SOL, '4x² − 3x(3x − 4) = 4'), L(SOL, '5x² − 12x + 4 = 0'), L(SOL, '(5x − 2)(x − 2) = 0'),
     L(SOL, 'x = 2/5 and x = 2'), L(SOL, 'y = 3(2/5) − 4 = −14/5'), L(SOL, 'y = 3(2) − 4 = 2'), L(SOL, '(2/5, −14/5) and (2, 2)'),
     L(LPC, 'x or y isolated'), L(MPC, '4x² − 3x(3x − 4) = 4 or equivalent equation in one variable'),
     L(HPC, '1 relevant value (root) found from quadratic')],
 'maths-2020-ol-p1-q3-a-i': [L(SOL, 'z₃ = 2i(−2 + i) = −4i + 2i²'), L(SOL, '−2 − 4i'), L(NOTE, '4 items (find z₃ and 3 plots)'), L(LPC, 'One correct item'),
     L(LPC, '(correct plot for incorrect z₃) or (z₁ plotted correctly) or (z₂ plotted correctly) or (z₃ correct but with incorrect plot)'),
     L(MPC, '2 correct items'), L(HPC, '3 correct items')],
 'maths-2020-ol-p1-q3-a-iii': [L(SOL, '|z₁| = √(9 + 16) = 5'), L(LPC, '|z₁| formula'), L(HPC, 'Formula fully substituted')],
 'maths-2020-ol-p1-q3-b': [L(SOL, 'z₄ = (29 + 3i)(3 + 4i)/((3 − 4i)(3 + 4i))'), L(SOL, '= (87 + 116i + 9i + 12i²)/(9 − 16i²)'), L(SOL, '= (75 + 125i)/25'),
     L(SOL, '= 3 + 5i'), L(LPC, 'Some correct substitution'), L(LPC, 'Conjugate identified'),
     L(LPC, 'Some multiplication above and below by same number, even if incorrect conjugate'), L(HPC, '(29 + 3i)(3 + 4i)/((3 − 4i)(3 + 4i))')],
 'maths-2020-ol-p1-q4-a-i': [L(SOL, '10 000 000/3·28² = 929506·2463'), L(SOL, '= 930 000 m²'), L(SOL, '9·3 × 10⁵'), L(LPC, '10 000 000 ÷ 3·28 or equivalent'),
     L(LPC, '10 000 000 × 3·28²'), L(HPC, '10 000 000 ÷ 3·28²')],
 'maths-2020-ol-p1-q4-a-ii': [L(SOL, '= 186 000 litres'), L(SOL, '186 000 ÷ 25'), L(SOL, '= 7440 tins'), L(LPC, 'Relevant use of answer (a)(i)'),
     L(HPC, 'Incorrect litres ÷ 25 correctly')],
 'maths-2020-ol-p1-q4-b': [L(SOL, '2^(9x−1) = (2³)^(2x)'), L(SOL, '2^(9x−1) = 2^(6x)'), L(SOL, '⇒ 9x − 1 = 6x'), L(SOL, '⇒ x = 1/3'), L(LPC, '2³ or 2^(6x)'),
     L(LPC, 'List of powers of 2'), L(HPC, 'Equation in x (Indices handled correctly)')],
 'maths-2020-ol-p1-q5-a': [L(SOL, '(x + 1)(x − 4) = 0'), L(SOL, 'x = −1 or x = 4'), L(ALT, 'x = (3 ± √25)/2'), L(LPC, 'Correct roots formula'),
     L(LPC, 'a or b or c explicitly identified'), L(LPC, 'Effort at factorising'), L(LPC, 'Correct answer without work'), L(HPC, 'Correct factors'),
     L(HPC, '1 correct root'), L(HPC, 'x = (3 ± √25)/2 and stops')],
 'maths-2020-ol-p1-q5-b-i': [L(SOL, 'f(x) –6 0 4 6 6 4 0'), L(LPC, 'One correct table entry'), L(HPC, 'Three correct table entries')],
 'maths-2020-ol-p1-q5-b-ii': [L(LPC, 'One correct plot from table entries'), L(HPC, 'Three correct plots from table entries with some join')],
 'maths-2020-ol-p1-q5-b-iii': [L(LPC, 'One correct point or table entry or plot for g(x)'), L(HPC, 'Three correct points or table entries or plots for g(x)')],
 'maths-2020-ol-p1-q6-a-i': [L(SOL, 'f′(x) = 12x² − 6x + 1'), L(LPC, '1 term [other than –7 (see note)] correctly differentiated'),
     L(HPC, '2 terms correctly differentiated'), L(NOTE, 'differentiation of independent term must be explicit for marks to be awarded i.e. f′(−7) = 0')],
 'maths-2020-ol-p1-q6-a-ii': [L(SOL, '12(1)² − 6(1) + 1 = 7 (Slope)'), L(LPC, 'Any substitution into candidates f′(x)'), L(LPC, 'f′(1) or equivalent written'),
     L(HPC, 'f′(−1) fully substituted')],
 'maths-2020-ol-p1-q6-a-iii': [L(SOL, 'y + 5 = 7(x − 1)'), L(SOL, '7x − y − 12 = 0'), L(LPC, 'Eq. of line formula with some substitution'),
     L(HPC, 'Eq. of line formula fully substituted with (1, 5) but not candidates answer from (a)(ii)')],
 'maths-2020-ol-p1-q6-b': [L(SOL, 'g(2) = 2(2)² + p(2) + q'), L(SOL, '8 + 2p + q = 6'), L(SOL, '2p + q = −2'), L(SOL, 'g′(3) = 4(3) + p = 9'), L(SOL, '⇒ p = −3'),
     L(SOL, 'q = 4'), L(LPC, 'g′(x) found'), L(LPC, 'g(2) found'), L(MPC, 'g′(x) and g(2) found'), L(MPC, '2p + q = −2'), L(HPC, 'p found')],
 'maths-2020-ol-p1-q7-a-i': [L(SOL, '443·66 × 12 × 3 = €15 971·76')] + SUB,
 'maths-2020-ol-p1-q7-a-ii': [L(SOL, '15971·76/12 000 × 100 = 133·09 = 133·1%')] + SUB,
 'maths-2020-ol-p1-q7-b': [L(SOL, '(1 + r)³ = 1·331'), L(SOL, '1 + r = 1·1'), L(SOL, 'r = 0·1 = 10%')] + SUB,
 'maths-2020-ol-p1-q7-c-i': [L(SOL, '32 000(0·8)³ = €16 384')] + SUB,
 'maths-2020-ol-p1-q7-c-ii': [L(SOL, 'x(0·8)³ = 17920'), L(SOL, 'x = 17920/0·8³ = €35 000'), L(LPC, 'Some relevant substitution into formula'),
     L(HPC, 'Formula fully substituted (x isolated)')],
 'maths-2020-ol-p1-q8-a': [L(SOL, 'ℎ(0) = 3/5 m'), L(PC, 'ℎ(0) indicated and stops')],
 'maths-2020-ol-p1-q8-b-i': [L(SOL, '(1/60)(12)² − (1/4)(12) + 3/5 = 0'), L(SOL, '0 = 0')] + SUB,
 'maths-2020-ol-p1-q8-b-ii': [L(SOL, 'x² − 15x + 36 = 0'), L(SOL, '(x − 3)(x − 12) = 0'), L(SOL, 'x = 3 m'), L(LPC, 'ℎ(x) = 0'),
     L(HPC, 'Function factorised correctly'), L(HPC, 'Division of function by (x − 3) indicated')],
 'maths-2020-ol-p1-q8-c-i': [L(SOL, 'ℎ′(x) = (1/30)x − 1/4'), L(LPC, '1 term [other than 3/5 (see note)] correctly differentiated'),
     L(HPC, '2 terms correctly differentiated'), L(NOTE, 'differentiation of independent term must be explicit for marks to be awarded i.e. f′(3/5) = 0')],
 'maths-2020-ol-p1-q8-c-ii': [L(SOL, '(1/30)x − 1/4 = 0'), L(SOL, 'x = 30/4 = 15/2 m'), L(LPC, 'f′(x) = 0 explicit'), L(HPC, '(1/30)x − 1/4 = 0')],
 'maths-2020-ol-p1-q8-c-iii': [L(SOL, 'ℎ(7·5) = (1/60)(7·5)² − (1/4)(7·5) + 3/5'), L(SOL, '= 27/80 m'), L(LPC, 'Some substitution into ℎ(x)'),
     L(HPC, 'ℎ(x) fully substituted with candidates value from (c)(ii)')],
 'maths-2020-ol-p1-q8-d-i': [L(SOL, '(29·33 − 28·5)/28·5 × 100 = 2·9%'), L(SOL, '(30·68 − 29·33)/29·33 × 100 = 4·6%'),
     L(LPC, 'Relevant use of question data to formulate a percentage'), L(HPC, 'One correct percentage found')],
 'maths-2020-ol-p1-q8-d-ii': [L(SOL, '(x − 25·01)/25·01 × 100 = 14·7'), L(SOL, 'x = 28·686'), L(SOL, 'y = 29·518'), L(SOL, 'z = 30·876'),
     L(SOL, 'Total = 25·01 + 28·686 + 29·518 + 30·876'), L(SOL, '=1:54·09'), L(SOL, 'Difference = 1:54·09 – 1:53·36'), L(SOL, '=0·73 Seconds'),
     L(LPC, '50 – 100 m split time formulated using 25·01 and 14·7%'), L(MPC, 'One correct split time found'), L(HPC, 'Three correct split times found')],
 'maths-2020-ol-p1-q9-a': [L(SOL, '3, 7, 11, 15, 19, 23'), L(LPC, 'One correct or consistent table entry'), L(HPC, 'Three correct or consistent table entries')],
 'maths-2020-ol-p1-q9-b-i': [L(SOL, '39'), L(PC, 'Evidence of counting beyond T₆'), L(NOTE, 'Accept correct answer without work')],
 'maths-2020-ol-p1-q9-b-ii': [L(SOL, 'Tn = 3 + (n − 1)4'), L(SOL, 'Tn = 4n − 1'), L(LPC, 'Tn formula written'), L(HPC, 'Formula with some substitution')],
 'maths-2020-ol-p1-q9-b-iii': [L(SOL, '4n − 1 = 147'), L(SOL, 'n = 37'), L(LPC, 'Tn formula written'), L(HPC, 'Formula fully substituted')],
 'maths-2020-ol-p1-q9-c-i': [L(SOL, 'Sn = n/2 [6 + (n − 1)4]'), L(SOL, '= n/2 [4n + 2]'), L(SOL, 'Sn = 2n² + n'), L(LPC, 'Sn formula written'),
     L(HPC, 'Formula with some substitution')],
 'maths-2020-ol-p1-q9-c-ii': [L(SOL, '2n² + n = 820'), L(SOL, '2n² + n − 820 = 0'), L(SOL, '(2n + 41)(n − 20) = 0'), L(SOL, 'n = 20 patterns'),
     L(LPC, 'Sn formula written'), L(LPC, 'Sn = 820'), L(LPC, 'Evidence of counting of sums'), L(HPC, 'Quadratic equation factorised'),
     L(NOTE, 'Accept correct answer without work')],
 'maths-2020-ol-p1-q9-d-i': [L(SOL, '1, 3, 5, 7, 9, 11'), L(LPC, 'One correct or consistent table entry'), L(HPC, 'Three correct or consistent table entries')],
 'maths-2020-ol-p1-q9-d-ii': [L(SOL, '= 4√3(1 + 3 + 5 + 7 + ⋯)'), L(SOL, '= 4√3(S₁₅) where a = 1 and d = 2'), L(SOL, '= 4√3[7·5 × 30]'),
     L(SOL, '= 1558·845727 = 1559 cm²'), L(LPC, 'At least 3 terms of AP identified'), L(LPC, 'Sn formula written'), L(HPC, 'Formula fully substituted')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2020, 'ol', 'p1', {'5B': [0, 2, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 4, 8, 10],
                             '10D': [0, 3, 5, 8, 10], '15D': [0, 5, 7, 11, 15]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
john = 'John works as part of a sales team. He earns a basic rate of €12·60 per hour. In addition to his hourly pay, he earns a commission of 22% on any sales he makes above €200 each week.'
A('1-a-i', 'Q1(a)(i)', '10C', [8], [4], '3-3', 'financial-maths', 'During a particular week, John worked 45 hours at the basic rate and made sales amounting to €350. Find John’s gross pay for this week.', stem=john)
A('1-a-ii', 'Q1(a)(ii)', '5D', [8], [4], '3-3', 'financial-maths,algebra-equations', 'During the following week John worked 51 hours. This included 3 hours on Sunday. If John works on a Sunday he receives 1·5 times the basic rate for those hours. His gross pay for that week was €713·20. Find the amount of sales John made in that week.', stem=john)
A('1-b', 'Q1(b)', '10D', [8], [5], '3-3', 'financial-maths', 'John pays tax at the Standard Rate of 20% and at the Higher Rate of 40%. He has a weekly Tax Credit of €26. The weekly Standard Rate Cut-off Point is €678. Find John’s net income for the week where his salary was €713·20.', stem=john)
A('2-a', 'Q2(a)', '10C', [9], [6], '4-2', 'algebra-equations', 'Solve the equation: (9x − 6)/2 = (3x − 14)/3 + 9x/4.')
A('2-b', 'Q2(b)', '15D', [9], [7], '4-2', 'algebra-equations', 'Solve the simultaneous equations: 3x − y = 4; 4x² − 3xy = 4.')
z3 = 'z₁ = 3 − 4i, z₂ = −2 + i and z₃ = 2iz₂, where i² = −1.'
A('3-a-i', 'Q3(a)(i),Q3(a)(ii)', '10D', [10], [8], '4-4', 'complex-numbers', '(i) Write z₃ in the form a + bi, where a, b ∈ ℤ. (ii) Plot z₁, z₂ and z₃ on the given Argand Diagram. Label each point clearly.', stem=z3)
A('3-a-iii', 'Q3(a)(iii)', '5C', [10], [8], '4-4', 'complex-numbers', 'Find |z₁|.', stem=z3)
A('3-b', 'Q3(b)', '10C', [10], [9], '4-4', 'complex-numbers', 'If z₁ × z₄ = 29 + 3i, write z₄ in the form a + bi, where a, b ∈ ℝ.', stem=z3)
gg = 'The Golden Gate Bridge in San Francisco is constantly being repainted. It is estimated that the surface area of exposed steel that needs to be painted is approximately 10 million square feet.'
A('4-a-i', 'Q4(a)(i)', '10C', [11], [10], '3-1', 'number-systems,area-volume', 'Given that 1 metre is equal to 3·28 feet, convert the surface area of the bridge into square metres, giving your answer in the form a × 10ⁿ, where 1 ≤ a < 10 and n ∈ ℕ. Give the value of a correct to two significant figures.', stem=gg)
A('4-a-ii', 'Q4(a)(ii)', '5C', [11], [10], '3-3', 'number-systems', 'A litre of the paint used on the Golden Gate Bridge will cover approximately 5 square metres. This paint comes in 25 litre tins. Find the minimum number of tins of paint that will be needed to paint the entire bridge.', stem=gg)
A('4-b', 'Q4(b)', '10C', [11], [11], '3-2', 'indices', 'Solve the equation 2^(9x−1) = 8^(2x).')
A('5-a', 'Q5(a)', '5C', [12], [12], '4-2', 'algebra-equations', 'Solve the equation x² − 3x − 4 = 0.')
A('5-b-i', 'Q5(b)(i)', '5C', [12], [13], '5-1', 'graphing-functions,functions', 'Complete the table below to show the value of the function f(x) = −x² − x + 6 for each of the given values of x. x: −4, −3, −2, −1, 0, 1, 2. f(x): _, _, 4, _, _, _, _.')
fb = 'Part (b)(i): Complete the table below to show the value of the function f(x) = −x² − x + 6 for each of the given values of x.'
A('5-b-ii', 'Q5(b)(ii)', '10C', [12], [13], '5-1', 'graphing-functions', 'Hence draw the graph of f in the domain −4 ≤ x ≤ 2, where x ∈ ℝ, on the diagram below.', stem=fb)
A('5-b-iii', 'Q5(b)(iii)', '5C', [13], [13], '5-1', 'graphing-functions,functions', 'On the same diagram as the function f, draw the graph of the function g(x) = f(x − 2), in the domain −2 ≤ x ≤ 4, where x ∈ ℝ. Label the graphs of f(x) and g(x) clearly.', stem=fb)
A('6-a-i', 'Q6(a)(i)', '10C', [14], [14], '5-2', 'differentiation', 'Differentiate the function f(x) = 4x³ − 3x² + x − 7, where x ∈ ℝ, with respect to x.')
A('6-a-ii', 'Q6(a)(ii)', '5C', [14], [14], '5-2', 'differentiation', 'Find the slope of the tangent to the graph of f(x) = 4x³ − 3x² + x − 7 at the point (1, −5).')
A('6-a-iii', 'Q6(a)(iii)', '5C', [14], [14], '5-2', 'differentiation,co-ordinate-geometry-of-the-line', 'Hence find the equation of the tangent to the graph at this point.', stem='Part (a)(ii): Find the slope of the tangent to the graph of f(x) = 4x³ − 3x² + x − 7 at the point (1, −5).')
A('6-b', 'Q6(b)', '5D', [14], [15], '5-2', 'differentiation,algebra-equations', 'The function g(x) = 2x² + px + q, where p, q ∈ ℤ, and x ∈ ℝ. Given that g(2) = 6 and g′(3) = 9, find the value of p and the value of q. Note: g′(3) is the value of the derivative of g(x) at x = 3.')
pat = 'Pat buys a new car for €32 000. He trades in his old car and is given an allowance of €20 000 by the garage. He borrows the balance of the money from the credit union. His fixed monthly repayment over three years is €443·66 per month.'
A('7-a-i', 'Q7(a)(i)', '10C', [15], [16], '3-3', 'financial-maths', 'How much money does Pat pay in total to the credit union for the loan?', stem=pat)
A('7-a-ii', 'Q7(a)(ii)', '5C', [15], [16], '3-3', 'financial-maths', 'Show the amount that Pat repays as a percentage of the amount that he borrows from the credit union is 133·1%, correct to one decimal place.', stem=pat)
A('7-b', 'Q7(b)', '5C', [15], [16], '3-3', 'financial-maths', 'A sum of money is invested at r% per annum compound interest for 3 years. At the end of the 3 years the value of the investment has increased by 33·1%. Find the value of r.')
A('7-c-i', 'Q7(c)(i)', '5C', [15], [17], '3-3', 'financial-maths', 'It is estimated that the value of cars depreciates at a compound rate of 20% per year. Use this percentage to find the value of Pat\'s car after three years (original price €32 000).', stem=pat)
A('7-c-ii', 'Q7(c)(ii)', '10C', [15], [17], '3-3', 'financial-maths', 'Pat\'s friend Caitlín bought a new car three years ago. Its value also depreciated by 20% per year. It is now worth €17 920. Find the original value of the car.', stem='It is estimated that the value of cars depreciates at a compound rate of 20% per year.')
sw = 'A swimmer is on a starting block at the beginning of a race. When she dives off the block until she resurfaces, the level of the swimmer relative to the level of the water is given by the function: h(x) = (1/60)x² − (1/4)x + 3/5. In the function, x is the horizontal distance in metres of the swimmer from the block, 0 ≤ x ≤ 12, where x ∈ ℝ and h(x) is measured in metres.'
A('8-a', 'Q8(a)', '5B', [16], [18], '5-1', 'functions', 'Find the height of the block above the water.', stem=sw)
A('8-b-i', 'Q8(b)(i)', '5C', [16], [18], '5-1', 'functions', 'Show that the swimmer is on the surface of the water (i.e. h(x) = 0) when she is 12 metres from the starting block.', stem=sw)
A('8-b-ii', 'Q8(b)(ii)', '10C', [16], [18], '4-2', 'algebra-equations,functions', 'Find the horizontal distance, in metres, from the starting block to the point where the swimmer enters the water.', stem=sw)
A('8-c-i', 'Q8(c)(i)', '5C', [16], [19], '5-2', 'differentiation', 'Find h′(x), the derivative of h(x) = (1/60)x² − (1/4)x + 3/5.', stem=sw)
A('8-c-ii', 'Q8(c)(ii)', '5C', [17], [19], '5-2', 'differentiation', 'Use your answer to Part (c)(i) to find the horizontal distance (x), in metres, from the starting block to the point at which the swimmer reaches her greatest depth.', stem=sw)
A('8-c-iii', 'Q8(c)(iii)', '5C', [17], [19], '5-2', 'differentiation,functions', 'Hence find this greatest depth.', stem=sw + ' Part (c)(ii): Use your answer to Part (c)(i) to find the horizontal distance (x), in metres, from the starting block to the point at which the swimmer reaches her greatest depth.')
ph = 'In the 2016 Summer Olympics, Michael Phelps, won the 200 m Butterfly final in a time of 1 minute and 53·36 seconds (1: 53·36). The time it took to swim each of the four 50 m sections of the race (split time) is given in the table below. The percentage increase in the time taken to swim one section is also given. Thus, it took the swimmer 14·7% longer to swim the second 50 metres compared to the first 50 metres. Race Section, Split Time (secs), Percentage Increase: 0 – 50 m, 24·85; 50 – 100 m, 28·5, 14·7%; 100 – 150 m, 29·33; 150 – 200 m, 30·68; Total, 1:53·36.'
A('8-d-i', 'Q8(d)(i)', '10C', [18], [20], '3-3', 'number-systems', 'Complete the table by finding the percentage increase in split time by comparing each split time with the previous one. Give your answers correct to one decimal place.', stem=ph)
A('8-d-ii', 'Q8(d)(ii)', '10D', [18], [21], '3-3', 'number-systems', 'Another swimmer in the race completed the first 50 m in a time of 25·01 seconds. His subsequent 50 m split times increased at the same rates as each of Michael Phelps’ times. Using the table below, or otherwise, find the difference between his finishing time and that of Michael Phelps. Give your answers in seconds correct to 2 decimal places.', stem=ph)
m9 = 'The following sequence of patterns is created using matchsticks to form equilateral triangles.'
A('9-a', 'Q9(a)', '10C', [19], [22], '4-1', 'sequences-series', 'Complete the table below to show the number of matchsticks required to make each of the first six patterns of the above sequence. Pattern Number: 1, 2, 3, 4, 5, 6. Number of Matchsticks: 3, 7, _, _, _, _.', stem=m9)
A('9-b-i', 'Q9(b)(i)', '10B', [19], [22], '4-1', 'sequences-series', 'How many matchsticks are required to make pattern 10 of the sequence?', stem=m9)
A('9-b-ii', 'Q9(b)(ii)', '5C', [19], [22], '4-1', 'sequences-series', 'Find a formula for Tₙ, the number of matchsticks required to make pattern n of the sequence.', stem=m9)
A('9-b-iii', 'Q9(b)(iii)', '5C', [19], [23], '4-1', 'sequences-series,algebra-equations', 'Pattern k has 147 matchsticks, where k ∈ ℕ. Find the value of k.', stem=m9)
A('9-c-i', 'Q9(c)(i)', '10C', [20], [23], '4-1', 'sequences-series', 'Find a formula for Sₙ, the total number of matchsticks required to make the first n patterns.', stem=m9)
A('9-c-ii', 'Q9(c)(ii)', '5C', [20], [23], '4-1', 'sequences-series,algebra-equations', 'Find the total number of complete patterns in the sequence that can be made using 820 matchsticks.', stem=m9)
A('9-d-i', 'Q9(d)(i)', '10C', [20], [24], '4-1', 'sequences-series', 'The table below shows the number of triangles formed by each pattern for the first two patterns. Complete the table to show the number of triangles formed for patterns three to six. Pattern Number: 1, 2, 3, 4, 5, 6. Number of Triangles: 1, 3, _, _, _, _.', stem=m9)
A('9-d-ii', 'Q9(d)(ii)', '5C', [20], [24], '4-1', 'sequences-series,area-volume', 'The area of each triangle is 4√3 cm². Find, correct to the nearest cm², the combined total area covered by the first 15 patterns in the sequence.', stem=m9)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 35, '8': 55, '9': 60}
p.check(marks, 40)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 1–21 of the combined Ordinary Level scheme (cover, notes, contents, the Paper 1 scale table on page 5, the summary of mark allocations on page 6, the annotation palette on page 7, every Paper 1 model solution and marking note on pages 8–20, and the Paper 2 title page 21). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 22)), [5, 6],
    ['The 2020 Leaving Certificate examinations were cancelled and replaced by Calculated Grades, but the SEC published this paper and its marking scheme. The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 35 marks, Q8 55 marks, Q9 60 marks). Every question is retained.',
     '40 independently marked units, matching the printed summary of allocations on scheme page 6. Q3(a)(i) and (a)(ii) share one 10D scale (“4 items (find z₃ and 3 plots)”) and are one task.',
     'Paper 1 bands from the Ordinary Level scale table on scheme page 5: 5B 0,2,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,4,8,10; 10D 0,3,5,8,10; 15D 0,5,7,11,15 (the Ordinary Level 15D ladder differs from the Higher Level 0,4,7,11,15, and Q2(b) prints “Scale 15D (0, 5, 7, 11,15)”).',
     'This paper had no authored cards before this review; all 40 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from. Q5(b)(ii)–(iii) are graph tasks whose model solutions are drawings; their cards carry the printed credit criteria and point to the scheme pages.',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [21], 'wording': 'Using the table below, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'The table is one permitted method for the same printed task and scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2020 Ordinary Level Paper 1', expect_added=[c['id'] for c in p.cards],
        question_figures=True)
