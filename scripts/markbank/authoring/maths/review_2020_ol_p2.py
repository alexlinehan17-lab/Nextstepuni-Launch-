"""2020 OL Paper 2: a new paper — 40 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
FCW = L(FC, 'Correct answer without supporting work')
SUB = [L(LPC, 'Formula with some substitution'), L(HPC, 'Formula fully substituted')]

ROWS = {
 'maths-2020-ol-p2-q1-a-i': [L(SOL, '4 × 6 × 8 = 192 available'), L(LPC, 'Indication of multiplication involving any two of 4, 6, and 8'),
     L(HPC, 'Any three numbers multiplied which include any two of 4, 6, and 8'), FCW],
 'maths-2020-ol-p2-q1-a-ii': [L(SOL, '4 × 6 × x = 120'), L(SOL, 'x = 120/24 = 5 desserts'), L(LPC, '4 × 6 indicated'), L(HPC, 'Answer as 4 × 6 × x = 120')],
 'maths-2020-ol-p2-q1-b-i': [L(SOL, '7/8 × 7/8 × 7/8 × 1/8 = 343/4096 or 0·08374'), L(LPC, 'Probability as 1/8 or 7/8'), L(HPC, '7/8 × 7/8 × 7/8 × 1/8 and stops'),
     L(NOTE, 'Treat 1/8 × 1/8 × 1/8 × 7/8 and continues correctly as Full Credit (–1)'), FCW],
 'maths-2020-ol-p2-q1-b-ii': [L(SOL, '3(1/8 × 1/8 × 7/8) = 21/512 or 0·04101'), L(LPC, '1/8 × 7/8 or 1/8 × 1/8 in any way'),
     L(HPC, '3(1/8 × 1/8 × 7/8) or (1/8 × 1/8 × 7/8) = 7/512'), FCW],
 'maths-2020-ol-p2-q2-a': [L(SOL, '|AB| = √((x₂ − x₁)² + (y₂ − y₁)²)'), L(SOL, '= √((−2 − 4)² + (2 − 6)²)'), L(SOL, '= √(36 + 16)'), L(SOL, '= √52'),
     L(SOL, '(= 2√13)'), L(LPC, 'Formula with some substitution'), L(HPC, 'Formula fully substituted'),
     L(HPC, 'Incorrect substitution into formula and completed correctly'), L(NOTE, 'Accept 1√52 or √52 for full marks')],
 'maths-2020-ol-p2-q2-b-i': [L(SOL, 'Mid pt = ((x₁ + x₂)/2, (y₁ + y₂)/2)'), L(SOL, '= ((4 − 2)/2, (6 + 2)/2)'), L(SOL, '= (1, 4)'), L(LPC, 'Formula with some substitution'),
     L(HPC, 'Formula fully substituted'), L(HPC, 'Incorrect substitution into formula and completed correctly'), FCW],
 'maths-2020-ol-p2-q2-b-ii': [L(SOL, 'mDE = (3 − 4)/(7 − 1) = −1/6'), L(SOL, 'mBC = (0 − 2)/(10 + 2) = −2/12 = −1/6'), L(LPC, 'Formula with some substitution'),
     L(LPC, 'States slopes are equal (or similar)'), L(HPC, 'One correct slope'), L(HPC, 'Incorrect substitution into formula and completed correctly')],
 'maths-2020-ol-p2-q2-c': [L(SOL, 'A(4, 6) B(−2, 2) C(10, 0)'), L(SOL, 'x down 10, y no change'), L(SOL, '(−6, 6) (−12, 2) (0, 0)'),
     L(SOL, 'Area = 1/2 |x₁y₂ − x₂y₁|'), L(SOL, '= 1/2 |(−6)(2) − (−12)(6)|'), L(SOL, '= 30 units²'),
     L(LPC, 'Translation of any relevant point to (0, 0) indicated'), L(LPC, 'Formula with some substitution'),
     L(MPC, 'Formula fully substituted with 2 from A, B, and C'), L(HPC, 'Formula fully substituted with translated points'),
     L(HPC, 'Area of triangle found from formula fully substituted with 2 from A, B, and C'), L(HPC, 'Area of triangle found from an incorrect translation')],
 'maths-2020-ol-p2-q3-a-i': [L(SOL, '1/√1000'), L(SOL, '= 0·031622 = 3·2%'), L(LPC, 'Writes 1/√n'), L(LPC, 'Sets up work as √1000'),
     L(HPC, 'Formula fully substituted. (1/√1000)'), L(HPC, 'Answer as 0·031622 without work'), FCW,
     L(NOTE, 'Special Case Without Work Award 3·1622% F* Full Credit (–1)')],
 'maths-2020-ol-p2-q3-a-ii': [L(SOL, '762/1000 = 0·762 = 76·2%'), L(SOL, '= [76·2% − 3·2%, 76·2% + 3·2%]'), L(SOL, '= [73%, 79·4%]'),
     L(SOL, '(95% C. I.) 73% ≤ μ ≤ 79·4%'), L(LPC, 'Works correctly with margin of error from (a)(i)'), L(LPC, 'p̂ = 762/1000.'),
     L(HPC, 'One boundary formed: (76·2% − 3·2% or 76·2% + 3·2%)'), L(HPC, 'Correct answer without supporting work'),
     L(NOTE, 'Accept use of version of formula from HL (73·6 < μ < 78·8)')],
 'maths-2020-ol-p2-q3-a-iii': [L(SOL, 'H₀ = 80%'), L(SOL, 'H₁ ≠ 80%'), L(SOL, '80% is not within the 95% C.I. above'),
     L(SOL, 'Therefore there is sufficient evidence to reject H0, and conclude that the percentage of people who believe that it is safe to give their credit card details online is not 80% .'),
     L(LPC, 'Null hypothesis stated'), L(LPC, '95% C. I. written'), L(HPC, 'Conclusion OK but reason incorrect or omitted'),
     L(HPC, 'Reason OK but conclusion incorrect, omitted or not in context')],
 'maths-2020-ol-p2-q3-b-i': [L(SOL, 'A = 390 B = 570'), L(PC, 'One boundary written [480 − 90]')],
 'maths-2020-ol-p2-q3-b-ii': [L(SOL, 'x̅ ± σ = 68%'), L(SOL, '68% of 6500 = 4420'), L(LPC, '68% identified'), L(LPC, 'Knowledge of Empirical Rule displayed'),
     L(HPC, '68% of incorrect value found correctly'), L(HPC, 'Correct use of incorrect percentage (95 % = 6175, 99·7 % = 6480·5'), FCW],
 'maths-2020-ol-p2-q4-a-i': [L(SOL, 'Centre (1, −4)'), L(SOL, 'Radius 5'), L(PC, 'Centre or radius correct'), FCW],
 'maths-2020-ol-p2-q4-a-ii': [L(SOL, '(1 − 1)² + (k + 4)² = 25'), L(SOL, 'k² + 8k − 9 = 0'), L(SOL, '(k − 1)(k + 9) = 0'), L(SOL, 'k = 1 k = −9'),
     L(ALT, 'k + 4 = ± 5'), L(LPC, 'Formula with some substitution'), L(MPC, 'Formula fully substituted'), L(MPC, '(1 − 1)² + (k + 4)² = 25'),
     L(HPC, 'k² + 8k − 9 = 0'), L(HPC, 'k + 4 = ± 5'), L(HPC, 'Substituting (k, 1) into formula and completed correctly')],
 'maths-2020-ol-p2-q4-b': [L(SOL, '⇒ Perpendicular slope = 3/2'), L(SOL, 'y + 2 = 3/2 (x − 3)'), L(SOL, '2y + 4 = 3x − 9'), L(SOL, '3x − 2y − 13 = 0'),
     L(ALT, '(x − 0)(3 − 0) + (y − 0)(−2 − 0) = 13'), L(LPC, 'Formula with some substitution'), L(MPC, 'mR and/or mT found'),
     L(MPC, 'HL Formula with any 2 of the 3 elements substituted correctly'), L(HPC, 'Eq. of line formula fully substituted'),
     L(HPC, 'One incorrect substitution followed by correct solution'), L(NOTE, 'Accept (−3x + 2y + 13 = 0)')],
 'maths-2020-ol-p2-q5-a': [L(SOL, 'sin 55 = 100/ℎ'), L(SOL, 'ℎ = 100/sin 55'), L(SOL, 'ℎ = 122·077'), L(SOL, 'ℎ = 122')] + SUB + [FCW],
 'maths-2020-ol-p2-q5-b': [L(SOL, 'sin θ = 100/200 = 1/2'), L(SOL, '⟹ θ = sin⁻¹(1/2) = 30°')] + SUB + [FCW],
 'maths-2020-ol-p2-q5-c': [L(SOL, '|∠X| = 180 − (45 + 40) = 95°'), L(SOL, 'd² = (141·4)² + (155·6)² − 2(141·4)(155·6) cos 95°'), L(SOL, 'd = 219·181'),
     L(SOL, 'd = 219'), L(ALT, 'd/sin 95 = 155·6/sin 45'), L(ALT, 'd = 219·214')] + SUB + [L(HPC, 'One incorrect substitution followed by correct solution')],
 'maths-2020-ol-p2-q6-a': [L(SOL, '(3x + y) + (x + y) + 80 = 180'), L(SOL, '⟹ 4x + 2y = 100'), L(SOL, '⟹ 2x + y = 50'), L(SOL, '3x + y = 60'), L(SOL, 'x = 10'),
     L(SOL, '⟹ y = 30'), L(LPC, 'Knowledge of sum of angles in a triangle = 180° shown'), L(LPC, 'Knowledge of vertically opposite angles being equal shown'),
     L(MPC, 'One relevant equation found'), L(HPC, 'Two relevant equations found'), L(HPC, 'Finds one solution'),
     L(HPC, 'Correct answer without supporting work')],
 'maths-2020-ol-p2-q6-b': [L(SOL, 'x/5 = 18/12'), L(SOL, '12x = 90'), L(SOL, 'x = 7·5 cm'), L(LPC, 'Any relevant work with ratio of lengths'),
     L(HPC, 'Correct ratio equality'), L(HPC, 'Incorrect ratio equality and finished correctly')],
 'maths-2020-ol-p2-q7-a-i': [L(SOL, '60° + 45° = 105°'), L(SOL, 'or 180° − (30° + 45°) = 105°'), L(PC, 'Knowledge of sum of angles in a triangle = 180° shown')],
 'maths-2020-ol-p2-q7-a-ii': [L(SOL, 'y/sin 30 = 100/sin 105'), L(SOL, 'y = 100 sin 30/sin 105'), L(SOL, 'y = 51·7638'), L(SOL, 'y = 51·8 m')] + SUB,
 'maths-2020-ol-p2-q7-a-iii': [L(SOL, 'sin 45 = ℎ/51·8'), L(SOL, 'h = 36·62813'), L(SOL, 'h = 36·6 m'), L(SOL, 'sin 30 = 36·6/x'), L(SOL, 'x = 73·2 m'),
     L(LPC, 'Formula with some substitution'), L(MPC, 'ℎ or x found'), L(HPC, 'Both formula fully substituted'),
     L(HPC, 'Incorrect substitution followed by correct solution')],
 'maths-2020-ol-p2-q7-b': [L(SOL, '1·23[25(73·2 + 51·8) + 580(36·6)]'), L(SOL, '= 1·23(24353)'), L(SOL, '= €29 954·19'), L(LPC, 'Cost of any element indicated'),
     L(HPC, 'Each element excluding VAT formulated')],
 'maths-2020-ol-p2-q7-c-i': [L(SOL, 'Area = 6[1/2(8)(8) sin 60]'), L(SOL, '= 6[27·71281292]'), L(SOL, '= 166·28 (km²)')] + SUB
     + [L(HPC, 'One incorrect substitution followed by correct solution')],
 'maths-2020-ol-p2-q7-c-ii': [L(SOL, 'Area = 1/6[π(8²) − 166·28]'), L(SOL, '= 1/6[34·78192983]'), L(SOL, '= 5·7969'), L(SOL, '= 5·8 (km²)'),
     L(LPC, 'Formula with some substitution'), L(HPC, 'Shaded area fully substituted')],
 'maths-2020-ol-p2-q8-a-i': [L(SOL, '1833 × 100/2779 − 1344 × 100/2547'), L(SOL, '= 65·95% − 52·77%'), L(SOL, '= 13·18%'), L(SOL, '= 13·2%'),
     L(LPC, 'Any correct element 1833/2779 or 1344/2547'), L(HPC, 'Significant work. Both 1833'), L(HPC + ' (continued)', '2779 and 1344/2547 shown')],
 'maths-2020-ol-p2-q8-a-ii': [L(SOL, '(2779 + 3100 + 3175 + 3104 + 2825 + 2580 + 2547) ÷ 7'), L(SOL, '= 20110/7'), L(SOL, '= 2872·857'), L(SOL, '= 2872·9 kt'),
     L(LPC, 'Formula with some substitution'), L(HPC, 'Formula fully substituted'),
     L(HPC, 'Calculates the mean of the waste sent to landfill (Ans = 1761·7)'), FCW],
 'maths-2020-ol-p2-q8-a-iii': [L(SOL, '(1724 + 1496 + 1344 + x)/4 = 1398'), L(SOL, '(4564 + x)/4 = 1398'), L(SOL, 'x = 1028 kt'),
     L(LPC, 'Effort at adding 3 relevant landfill waste data'), L(LPC, 'Indicates the total value as: 1398 × 4'), L(HPC, '1398 = ∑ Landfill data')],
 'maths-2020-ol-p2-q8-b-i': [L(SOL, '31 + 11 + 13 + 12 + 13 = 80'), L(SOL, '100 − 80 = 20%'), L(LPC, 'Addition or indication of addition of some of Denmark data'), FCW],
 'maths-2020-ol-p2-q8-b-ii': [L(SOL, 'Cyprus, Luxemburg, Malta, Netherlands.'), L(LPC, 'Any correctly identified country'), L(HPC, 'Three correct only'),
     L(HPC, 'Four correct but with additional incorrect data')],
 'maths-2020-ol-p2-q8-b-iii': [L(SOL, 'Cyprus or Malta')],
 'maths-2020-ol-p2-q8-b-iv': [L(SOL, '42/100 × 360 = 151·2 = 151°'), L(SOL, '13/100 × 360 = 46·8 = 47°'), L(SOL, '24/100 × 360 = 86·4 = 86°'),
     L(SOL, '15/100 × 360 = 54°'), L(LPC, 'One new angle correctly formulated'), L(MPC, 'Two angles found'), L(HPC, 'Three angles found'),
     L(HPC, 'Completes using [6% = 22°]'), FCW],
 'maths-2020-ol-p2-q8-b-v': [L(LPC, 'One correct/ relevant new sector added to the pie chart'), L(MPC, 'Two correct/ relevant new sectors added to the pie chart'),
     L(HPC, 'Labels omitted')],
 'maths-2020-ol-p2-q9-a-i': [L(SOL, '10 + Diameter = 16'), L(SOL, 'Diameter = 6'), L(SOL, 'Radius = 3 (cm)'), L(LPC, 'Vertical diameter indicated on diagram'),
     L(HPC, 'Finds Diameter = 6')],
 'maths-2020-ol-p2-q9-a-ii': [L(SOL, 'y = 2πr'), L(SOL, '= 2π(3)'), L(SOL, '= 6π'), L(SOL, '= 19 (cm)'), L(PC, 'Formula with some substitution'), FCW],
 'maths-2020-ol-p2-q9-a-iii': [L(SOL, 'Area of sheet = 6π × 16 = 96π'), L(SOL, 'C. S. A = 6π × 10 = 60π'), L(SOL, 'Area of circles = 2π(3)² = 18π'),
     L(SOL, 'Waste = 96π − (60π + 18π)'), L(SOL, '= 57 (cm²)'), L(LPC, 'Any area formula with some substitution'),
     L(HPC, 'Two of the three required areas calculated correctly.'), L(HPC, 'Uses only one circle and finishes consistently')],
 'maths-2020-ol-p2-q9-b-i': [L(SOL, 'Volume = 4/3 π(1·5)³'), L(SOL, '= 4/3 π(27/8)'), L(SOL, '= 9π/2 cm³'), L(PC, 'Formula with some substitution'),
     L(PC, 'Answer not in terms of π (14·137 cm³)'), FCW],
 'maths-2020-ol-p2-q9-b-ii': [L(SOL, 'π(3·5)²ℎ = 3(9π/2)'), L(SOL, 'ℎ = 27/(2(3·5)²)'), L(SOL, '= 1·102'), L(SOL, '= 1·1 cm'),
     L(LPC, 'Formula with some substitution'), L(MPC, 'Both volume formulae fully substituted correctly'),
     L(HPC, 'Volume equation set up correctly and correctly substituted'), L(HPC, 'Equation written with h as subject')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2020, 'ol', 'p2', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 4, 8, 10],
                             '10D': [0, 3, 5, 8, 10], '20D': [0, 5, 10, 15, 20]},
          'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
menu = 'A restaurant is offering a three-course meal consisting of one starter, one main course and one dessert. There are 4 different starters, 6 different main courses and 8 different desserts to choose from.'
A('1-a-i', 'Q1(a)(i)', '5C', [24], [4], '1-1', 'counting', 'How many different three-course meal combinations are available?', stem=menu)
A('1-a-ii', 'Q1(a)(ii)', '10C', [24], [4], '1-1', 'counting,algebra-equations', 'When Jack visits the restaurant he discovers that the restaurant still has the 4 starters and the 6 main courses available but is sold out of some of the desserts. Jack now has 120 different three-course meal combinations to choose from. How many different desserts are still available to Jack?', stem=menu)
ten = 'In a large population 1 in 8 of the people play tennis.'
A('1-b-i', 'Q1(b)(i)', '5C', [25], [5], '1-2', 'probability', 'Four people are chosen at random from the population. What is the probability that the fourth person chosen is the only one to play tennis?', stem=ten)
A('1-b-ii', 'Q1(b)(ii)', '5C', [25], [5], '1-2', 'probability', 'Three people are chosen at random from the population. What is the probability that exactly two of them play tennis?', stem=ten)
tri = 'The points A(4, 6), B(−2, 2) and C(10, 0) are the vertices of the triangle ABC shown below.'
A('2-a', 'Q2(a)', '10C', [26], [6], '2-2', 'co-ordinate-geometry-of-the-line', 'Find |AB|, the length of [AB]. Give your answer in the form a√b units, where a, b ∈ ℕ.', stem=tri)
A('2-b-i', 'Q2(b)(i)', '5C', [26], [6], '2-2', 'co-ordinate-geometry-of-the-line', 'Find the coordinates of D, the midpoint of [AB].', stem=tri)
A('2-b-ii', 'Q2(b)(ii)', '5C', [27], [7], '2-2', 'co-ordinate-geometry-of-the-line', 'In the triangle ABC, the point E(7, 3) is the midpoint of [AC]. Show that DE is parallel to BC.', stem=tri + ' Part (b)(i): Find the coordinates of D, the midpoint of [AB].')
A('2-c', 'Q2(c)', '5D', [27], [7], '2-2', 'co-ordinate-geometry-of-the-line,area-volume', 'Find the area of the triangle ABC.', stem=tri)
srv = 'In a survey, 1000 people are selected at random and asked some questions about online shopping.'
A('3-a-i', 'Q3(a)(i)', '5C', [28], [8], '1-7', 'statistics', 'Find the margin of error of the survey. Give your answer as a percentage correct to 1 decimal place.', stem=srv)
A('3-a-ii', 'Q3(a)(ii)', '5C', [28], [8], '1-7', 'statistics', 'Of those asked, 762 said they believe it is safe to give their credit card details when shopping online. Use your answer to Part a(i) above to create a 95% confidence interval for the percentage of people who believe it is safe to give their credit card details when shopping online.', stem=srv)
A('3-a-iii', 'Q3(a)(iii)', '5C', [29], [8], '1-7', 'statistics', 'An online media company claims that 80% of people believe it is safe to give their credit card details when shopping online. Conduct a hypothesis test, at the 5% level of significance, to test the company\'s claim. Give your conclusion in the context of the question and give a reason for your conclusion.', stem=srv + ' Of those asked, 762 said they believe it is safe to give their credit card details when shopping online.')
apt = 'An aptitude test was taken by 6500 candidates. The test scores were normally distributed. The mean score was 480 and the standard deviation was 90. On the distribution shown below, the shaded area represents all candidates who were within one standard deviation of the mean.'
A('3-b-i', 'Q3(b)(i)', '5B', [29], [9], '1-7', 'statistics', 'Write the value of A and the value of B into the boxes below.', stem=apt)
A('3-b-ii', 'Q3(b)(ii)', '5C', [29], [9], '1-7', 'statistics', 'Use the Empirical Rule to estimate the number of candidates in the shaded region.', stem=apt)
circ = 'The circle c has equation (x − 1)² + (y + 4)² = 25.'
A('4-a-i', 'Q4(a)(i)', '10B', [30], [10], '2-2', 'co-ordinate-geometry-the-circle', 'Find the centre and radius of c.', stem=circ)
A('4-a-ii', 'Q4(a)(ii)', '5D', [30], [10], '2-2', 'co-ordinate-geometry-the-circle,algebra-equations', 'The point (1, k) is on c. Find the two possible values of k.', stem=circ)
A('4-b', 'Q4(b)', '10D', [31], [11], '2-2', 'co-ordinate-geometry-the-circle,co-ordinate-geometry-of-the-line', 'The circle s has equation x² + y² = 13. The point A(3, −2) is on s. Find the equation of t, the tangent to the circle at the point A. Give your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.')
lake = 'Two swimmers A and B stand at the same point X, on one shore of a long, still rectangular shaped lake that is 100 m wide, as shown below. (Diagram not to scale.) Both swim to the opposite side of the lake.'
A('5-a', 'Q5(a)', '10C', [32], [12], '2-3', 'trigonometry', 'Swimmer A swims to the left, making an angle of 55° with the side of the lake as shown. Find the distance that A swims to reach the other side. Give you answer correct to the nearest metre.', stem=lake)
A('5-b', 'Q5(b)', '5C', [32], [12], '2-3', 'trigonometry', 'Swimmer B swims to the right and travels a distance of 200 m to reach the other side, making an angle of θ degrees with the bank on the other side of the lake, as shown. Find the value of θ.', stem=lake)
A('5-c', 'Q5(c)', '10C', [33], [13], '2-3', 'trigonometry', 'The next day the swimmers again swim to the opposite side of the lake but in slightly different directions. Swimmer A swims to the left, making an angle of 45° with the side of the lake and travels 141·4 metres as shown. Swimmer B swims to the right, making an angle of 40° with the side of the lake and travels 155·6 metres as shown. Find d, the distance both swimmers are apart when they reach the opposite side of the lake. Give you answer correct to the nearest metre.', stem=lake)
A('6-a', 'Q6(a)', '20D', [34], [14], '2-1', 'geometry,algebra-equations', 'Find the value of x and the value of y.', stem='In the diagram below: |∠CAB| = 80° and |∠DCE| = 60°. |∠ABC| = (x + y)° and |∠BCA| = (3x + y)°, where x, y ∈ ℕ.')
A('6-b', 'Q6(b)', '5C', [34], [15], '2-1', 'geometry', 'In the diagram below, DE is parallel to FG. |DH| = 5 cm. |HE| = 12 cm. |HG| = 30 cm. The distance from D to F is x cm. Find the value of x.')
mast = 'A vertical mobile phone mast, [DC], of height h m, is secured with two cables: [AC] of length x m, and [BC] of length y m, as shown in the diagram. The angle of elevation to the top of the mast from A is 30° and from B is 45°.'
A('7-a-i', 'Q7(a)(i)', '10B', [35], [16], '2-3', 'geometry,trigonometry', 'Explain why |∠BCA| is 105°.', stem=mast)
A('7-a-ii', 'Q7(a)(ii)', '10C', [35], [16], '2-3', 'trigonometry', 'The horizontal distance from A to B is 100 m. Use the triangle ABC to find the length of y. Give your answer correct to one decimal place.', stem=mast)
mast100 = mast + ' The horizontal distance from A to B is 100 m.'
A('7-a-iii', 'Q7(a)(iii)', '10D', [35], [17], '2-3', 'trigonometry', 'Using your answer to Part (a)(ii) or otherwise, find the value of h and the value of x. Give your answers correct to 1 decimal place.', stem=mast100)
A('7-b', 'Q7(b)', '10C', [36], [17], '3-3', 'financial-maths', 'The two cables to secure the mast costs €25 per metre. The mast itself costs €580 per metre. VAT at 23% is then added in each case. Calculate the total cost of the cables and mast after VAT is included.', stem=mast100)
hexs = 'The mast can provide a strong signal for an area in the shape of a regular hexagon of side 8 km, as shown in the diagram.'
A('7-c-i', 'Q7(c)(i)', '10C', [36], [18], '3-4', 'area-volume,trigonometry', hexs + ' Find the area of the hexagon. Give your answer in km², correct to 2 decimal places.')
A('7-c-ii', 'Q7(c)(ii)', '5C', [36], [18], '3-4', 'area-volume', 'A circle which touches all vertices of the hexagon can show areas where the signal is weak. One of these areas is shaded in the diagram. Find this shaded area. Give your answer in km², correct to 1 decimal place.', stem=hexs)
waste = 'The table below shows data (measured in kilotonnes) on how municipal waste was dealt with in Ireland from 2005 to 2011. Year, Total Waste Collected (Kilotonnes), Waste Sent to Landfill (Kilotonnes): 2005, 2779, 1833; 2006, 3100, 1981; 2007, 3175, 2015; 2008, 3104, 1939; 2009, 2825, 1724; 2010, 2580, 1496; 2011, 2547, 1344. Source: Environmental Protection Agency.'
A('8-a-i', 'Q8(a)(i)', '5C', [37], [19], '1-6', 'statistics', 'Find the difference between the percentage of the waste collected which was sent to landfill in 2005 and the percentage of waste sent to landfill in 2011. Give your answer correct to 1 decimal place.', stem=waste)
A('8-a-ii', 'Q8(a)(ii)', '10C', [37], [19], '1-6', 'statistics', 'Find the mean amount of waste collected each year, from 2005 to 2011. Give your answer correct to 1 decimal place.', stem=waste)
A('8-a-iii', 'Q8(a)(iii)', '5C', [37], [19], '1-6', 'statistics,algebra-equations', 'The mean amount of waste sent to landfill in the 4 years from 2009 to 2012 was 1398 kilotonnes. Find the amount of waste sent to landfill in 2012.', stem=waste)
energy = 'The table below shows the percentages of all the different types of energy sources used in each of 13 European countries during 2014. % of total energy — Country: Renewable, Oil, Solid Fuel, Gas, Electricity, Other. Austria: 25, 31, 8, 17, 13, 6. Bulgaria: 8, 19, 28, 11, 11, 23. Cyprus: 5, 82, 0, 0, 13, 0. Denmark: _, 31, 11, 13, 12, 13. France: 7, 26, 3, 11, 12, 41. Germany: 10, 29, 22, 17, 12, 10. Greece: 9, 43, 24, 9, 15, 0. Ireland: 6, 42, 13, 24, 15, 0. Latvia: 31, 26, 1, 20, 11, 11. Luxembourg: 4, 61, 1, 19, 12, 3. Malta: 2, 82, 0, 0, 16, 0. Netherlands: 4, 38, 10, 33, 10, 5. Portugal: 21, 38, 10, 13, 15, 3. Source: Eurostat.'
A('8-b-i', 'Q8(b)(i)', '5B', [38], [20], '1-6', 'statistics', 'What percentage of the energy used in Denmark in 2014 was renewable?', stem=energy)
A('8-b-ii', 'Q8(b)(ii)', '5C', [38], [20], '1-6', 'statistics', 'Name the four countries that used a lower percentage of renewable energy than Ireland.', stem=energy)
A('8-b-iii', 'Q8(b)(iii)', '5A', [38], [20], '1-6', 'statistics', 'Name a country which did not use gas as a fuel source.', stem=energy)
pie = 'The table below shows the percentage of the different types of energy that were used in Ireland during 2014. It also shows one of the angles in a pie chart to represent this data. The angle for renewable energy (6%) is 22°. Type, Percentage, Angle: Renewable, 6, 22°; Oil, 42, _; Solid Fuel, 13, _; Gas, 24, _; Electricity, 15, _.'
A('8-b-iv', 'Q8(b)(iv)', '10D', [39], [21], '1-6', 'statistics', 'Complete the table to show the angle for each energy type. Give each angle correct to the nearest degree.', stem=pie)
A('8-b-v', 'Q8(b)(v)', '10D', [39], [21], '1-6', 'statistics', 'Complete the pie chart below to show the energy types used in Ireland in 2014. Label each section clearly.', stem=pie)
can = 'A rectangular sheet of aluminium is used to make a cylindrical can of radius r cm and height 10 cm, as shown below. The aluminium does not overlap in the finished can.'
A('9-a-i', 'Q9(a)(i)', '10C', [40], [22], '3-4', 'area-volume', 'Show that r, the radius of the cylinder, is 3 cm.', stem=can)
A('9-a-ii', 'Q9(a)(ii)', '5B', [40], [22], '3-4', 'area-volume', 'Find the distance y. Give your answer correct to the nearest centimetre.', stem=can)
A('9-a-iii', 'Q9(a)(iii)', '5C', [40], [22], '3-4', 'area-volume', 'Find the area, in cm², of the waste aluminium after the top, bottom and side of the cylindrical can have been removed from the rectangular sheet. Give your answer correct to the nearest cm².', stem=can)
A('9-b-i', 'Q9(b)(i)', '10B', [41], [23], '3-4', 'area-volume', 'Find the volume of a spherical ice cube of radius 1·5 cm. Give your answer in terms of π.')
A('9-b-ii', 'Q9(b)(ii)', '10D', [41], [23], '3-4', 'area-volume', 'Three of the spherical ice cubes of radius 1·5 cm are added to a cylinder of internal radius 3·5 cm which is partially filled with water. All of the ice cubes are completely submerged in the water and the water does not overflow. Find the rise, h cm, in the water level. Give your answer correct to 1 decimal place.')

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 55, '9': 40}
p.check(marks, 40)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 21–44 of the combined Ordinary Level scheme (the Paper 2 title page 21, the Paper 2 scale table on page 22, the summary of mark allocations on page 23, every Paper 2 model solution and marking note on pages 24–41, the Irish-language bonus table on page 42 and the blank back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(21, 45)), [22, 23],
    ['The 2020 Leaving Certificate examinations were cancelled and replaced by Calculated Grades, but the SEC published this paper and its marking scheme. The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 55 marks, Q9 40 marks). Every question is retained.',
     '40 independently marked units, matching the printed summary of allocations on scheme page 23.',
     'Bands from the Paper 2 scale table on scheme page 22 and the ladders printed beside each part: 5A 0,5; 5B 0,2,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,4,8,10; 10D 0,3,5,8,10; 20D 0,5,10,15,20. The page 22 table misprints the 10D ladder as “0, 3, 15, 8, 10”; every 10D part prints “Scale 10D (0, 3, 5, 8, 10)” beside its solution, which the cards follow.',
     'This paper had no authored cards before this review; all 40 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from. Where the scheme stacks a fraction across lines that the provenance reader cannot rejoin, a bullet is quoted in two consecutive pieces (Q8(a)(i) high partial credit). Data tables are carried in the stem as the printed values. Q8(b)(v) is a pie-chart drawing; its card carries the printed credit criteria.',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [4], 'wording': 'desserts to choose from / meal combinations to choose from', 'classification': 'mathematical-counting',
      'reason': 'The menu is the sample space to be counted; the task asks for the number of combinations.'},
     {'pages': [17], 'wording': 'Using your answer to Part (a)(ii) or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'},
     {'pages': [18, 21], 'wording': 'One of these areas is shaded / one of the angles in a pie chart', 'classification': 'given-context',
      'reason': 'The shaded region and the given angle are data for one required task, not a choice between prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('mathematical-counting', 'The menu is the mathematical sample space; the candidate counts combinations rather than choosing a prompt.') if 'choose from' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t
        else ('given-context', 'Names the shaded region or the given pie-chart angle: data for one required task, not a choice between prompts.') if ('One of these areas' in t or 'one of the angles' in t) else None)
p.apply(ROWS, '2020 Ordinary Level Paper 2', expect_added=[c['id'] for c in p.cards],
        question_figures=True)
