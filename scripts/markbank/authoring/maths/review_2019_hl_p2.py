"""2019 HL Paper 2: a new paper — 32 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
M1, M2, M3 = 'Method 1, ', 'Method 2, ', 'Method 3, '
SUB = [L(LPC, 'Some relevant substitution'), L(HPC, 'Formula fully substituted')]

ROWS = {
 'maths-2019-hl-p2-q1-a-i': [L(SOL, '12/20 × 8/19 + 8/20 × 12/19 = 192/380 or 48/95'), L(ALT, '1 − [12/20 × 11/19 + 8/20 × 7/19] = 1 − 188/380'),
     L(LPC, '1 probability given e.g. 12/20 or equivalent'), L(LPC, '1 combination indicated e.g. (12 1) or (8 1) or (20 2)'),
     L(LPC, '12/20 × 8/19 or 8/20 × 12/19 or equivalent and stops'), L(HPC, '12/20 × 8/19 or 8/20 × 12/19 or equivalent and continues')],
 'maths-2019-hl-p2-q1-a-ii': [L(SOL, '12/20 × 11/19 × 10/18 × 8/17 = 10560/116280 or 88/969'), L(LPC, '1 probability given'), L(LPC, '1 combination indicated'),
     L(MPC, '3 or 4 correct probabilities indicated'), L(HPC, '3 correct probabilities with multiplication completed'),
     L(HPC, '4 probabilities with correct operator')],
 'maths-2019-hl-p2-q1-b': [L(SOL, '(6 3) × (8 4) = 1400'), L(ALT, '(1 1) × (6 3) × (8 4) = 1400'), L(LPC, '(6 3) or (8 4) or (1 1)'), L(HPC, '(6 3) × (8 4) and stops')],
 'maths-2019-hl-p2-q2-a': [L(SOL, 'm = (b − 0)/(0 − a) = −b/a'), L(SOL, 'y − 0 = −b/a (x − a)'), L(SOL, 'ay = −bx + ab'), L(SOL, 'bx + ay = ab'),
     L(SOL, 'Now divide across by ab'), L(SOL, 'x/a + y/b = 1'), L(M1 + LPC, 'Slope formula with some substitution'),
     L(M1 + HPC, 'Equation of line formula fully substituted'), L(M2 + HPC, 'm expressed in terms of a and b, and c in terms of b'),
     L(M3 + LPC, '(a, 0) or ((0, b) correctly substituted e.g. a/a + 0/b'), L(M3 + HPC, '(a, 0) and (0, b) correctly substituted')],
 'maths-2019-hl-p2-q2-b-i': [L(SOL, 'y − 0 = m(x − 6) or y = m(x − 6)'), L(SOL, 'y = mx − 6m'), L(MPC, 'Equation of line formula with some relevant substitution')],
 'maths-2019-hl-p2-q2-b-ii': [L(SOL, '=> 4x + 3m(x − 6) = 25'), L(SOL, '=>x = (25 + 18m)/(3m + 4)'), L(SOL, '= m/(3m + 4)'),
     L(M1 + LPC, 'Indication of use of simultaneous equations'), L(M1 + MPC, 'One relevant substitution'), L(M1 + HPC, 'x or y value found'),
     L(M2 + MPC, 'One successful elimination in equations')],
 'maths-2019-hl-p2-q3-a': [L(SOL, '(−2 − 2)² + (k − 3)² = 65'), L(SOL, '(k − 3)² = 49'), L(SOL, 'k − 3 = ±√49 = ±7'), L(SOL, 'k = 10 and k = −4'),
     L(ALT, 'k² − 6k − 40 = 0'), L(LPC, 'Some relevant substitution'), L(LPC, 'Centre or radius'), L(HPC, 'Equation in k²')],
 'maths-2019-hl-p2-q3-b': [L(SOL, 'Both axes are tangents to the circle.'), L(SOL, 'centre (-g,-g) and radius is g'), L(SOL, 'g + 6 = ±5g'),
     L(SOL, 'Centre (1, 1) and radius 1'), L(SOL, 'Equation: (x − 1)² + (y − 1)² = 1'), L(ALT, '2g² − g − 3 = 0'),
     L(M1 + LPC, 'centre (-g,-g) or equivalent'), L(M1 + MPC, 'Substitution into perpendicular distance formula completed'),
     L(M1 + MPC, 'Perpendicular distance of centre to tangent equals radius with some substitution'), L(M1 + HPC, 'equation in g or equivalent'),
     L(M2 + LPC, 'c = g² or f²'), L(M2 + LPC, 'Effort to express x in terms of y or equivalent'),
     L(M2 + MPC, 'Substitution into circle equation completed'), L(M2 + HPC, 'Quadratic equation in g or f')],
 'maths-2019-hl-p2-q4-a': [L(SOL, 'cos(A + B) = cos A cos B − sin A sin B'), L(SOL, 'cos 2A = cos²A − sin²A'), L(SOL, 'cos 2A = (1 − sin²A) − sin²A'),
     L(SOL, 'cos 2A = 1 − 2sin²A'), L(ALT, '(cos A + i sin A)² = cos 2A + i sin 2A'), L(M1 + LPC, 'cos(A + B) formula with some substitution'),
     L(M1 + LPC, 'cos²A + sin²A = 1 indicated or clearly implied'), L(M1 + HPC, 'cos 2A = cos²A − sin²A'), L(M3 + LPC, '(cos A + i sin A)² expanded')],
 'maths-2019-hl-p2-q4-b': [L(SOL, 'Let length of side be x'), L(SOL, 'Diagonal of any face = √(x² + x²) = √2x'), L(SOL, 'cos A = 1/3'),
     L(LPC, 'Length of any diagonal formulated'), L(MPC, 'Internal diagonal found'), L(HPC, 'Fully substituted cosine rule'),
     L(NOTE, 'Accept and mark work where a consistent numerical value is assigned to one side of the cube.'), L(M2 + HPC, 'sin A/2 fully substituted')],
 'maths-2019-hl-p2-q5-a': [L(SOL, 'Standard Orthocentre Construction'), L(LPC, 'Some correct element of construction'),
     L(LPC, 'Some evidence of understanding of term orthocentre'), L(MPC, 'One correct altitude'), L(HPC, 'Two correct altitudes but not intersecting.')],
 'maths-2019-hl-p2-q5-b': [L(SOL, '|DC| = |OB| Given'), L(SOL, '⇒ |DC| = Radius'), L(SOL, '⇒ ∆ODC is equilateral'), L(SOL, '⇒ ∠AOD = 60 Alternate'),
     L(SOL, '|∠ABE| = 90° as BE tangent'), L(SOL, '|∠BEA| = 180 − 90 − 60 = 30°'), L(LPC, '1 relevant step listed or shown on diagram'),
     L(MPC, '3 relevant steps listed or shown on diagram'), L(HPC, 'All valid steps included but with no justification')],
 'maths-2019-hl-p2-q6-a': [L(SOL, 'P(F ∩ S) = P(F) × P(S) since the events are independent.'), L(SOL, 'So P(S\\F) = 4/9 − 1/5 = 11/45 = x'),
     L(SOL, 'y = 1 − 11/45 − 1/5 − 1/4 = 11/36'), L(LPC, 'P(F ∩ S) = P(F) × P(S) or equivalent'), L(LPC, 'P(F) = 1/4 + 1/5'),
     L(LPC, 'P(S) = x + 1/5'), L(LPC, '1/4 + 1/5 + x + y = 1'), L(HPC, 'x found')],
 'maths-2019-hl-p2-q6-b': [L(SOL, 'If n Germans then 2n Irish and 3n+10 children in total'), L(SOL, 'n/(3n + 10) × (2n + 10)/(3n + 9) = 1/6'),
     L(SOL, '3n² + 3n − 90 = 0'), L(SOL, '(n + 6)(n − 5) = 0'), L(SOL, 'n = 5 German children.'),
     L(SOL, 'There are 10 Irish (and 10 Spanish) so 25 children in the club.'), L(M1 + LPC, '2n'), L(M1 + LPC, '3n+10'),
     L(M1 + LPC, 'One correct probability e.g. n/(3n+10)'), L(M1 + HPC, 'n/(3n + 10) × (2n + 10)/(3n + 9) = 1/6'),
     L(M2 + LPC, 'Some correct element in approach'), L(M2 + MPC, 'Tests more than one value'),
     L(M2 + HPC, 'Correct number of each nationality but not verified that probability is 1/6'),
     L(M2 + HPC, 'Correct answer (25) with no supporting work')],
 'maths-2019-hl-p2-q7-a-i': [L(SOL, '|AD|² = 90² − 60²'), L(SOL, '|AD| = √(8100 − 3600) = √4500 = 30√5'), L(LPC, '|OD| = 60'), L(LPC, 'Pythagoras formulated'),
     L(LPC, 'Effort to find angle other than ∠ODA'), L(HPC, '√(8100 − 3600) or equivalent')],
 'maths-2019-hl-p2-q7-a-ii': [L(SOL, 'cos(∠DOA) = 60/90'), L(SOL, 'cos⁻¹(6/9) = 0·84'), L(SOL, '|∠DOA| = 0·84139 = 0·84'),
     L(LPC, 'Relevant trigonometric ratio formulated'), L(HPC, 'Relevant trigonometric ratio fully substituted')],
 'maths-2019-hl-p2-q7-a-iii': [L(SOL, 'Area of sector: 1/2 r²θ'), L(SOL, '1/2(0·9)² × 2(0·84) = 0·6804 m²'), L(SOL, 'Area of segment = 0·6804 – 0·40 = 0·28'),
     L(LPC, 'Formula for area of sector with some substitution'), L(LPC, 'Formula for area of Δ ACO with some substitution'),
     L(MPC, 'One relevant area fully substituted'), L(HPC, 'Both relevant areas fully substituted'), L(HPC, 'Mishandling conversion of units')],
 'maths-2019-hl-p2-q7-a-iv': [L(SOL, 'Volume = 0·28 × 2·5 = 0·7'), L(LPC, 'Formula for volume of trough with some substitution'),
     L(LPC, 'Indicates some relevant use of 2·5'), L(HPC, 'Formula fully substituted')],
 'maths-2019-hl-p2-q7-b-i': [L(SOL, '= 4·0906 + 17·1805 + 2·4544'), L(SOL, '= 23·73'), L(LPC, '1 volume formula with some substitution'),
     L(MPC, '2 volumes fully substituted'), L(HPC, '3 volumes fully substituted')],
 'maths-2019-hl-p2-q7-b-ii': [L(SOL, '23·73 × 0 02 = 0·4746 cm³'), L(SOL, 'r/ℎ = 1·25/1·5 = 5/6'), L(SOL, 'ℎ = 0·87'), L(LPC, 'volume × 0·98 or equivalent'),
     L(LPC, 'volume multiplied by 2%'), L(LPC, 'effort at r : h'), L(HPC, 'Volume formula expressed in one variable')],
 'maths-2019-hl-p2-q8-a-i': [L(SOL, '0·188913 < p < 0·246087'), L(SOL, '0·1889 < p < 0·2461'), L(SOL, '18·89% < p < 24·61%'), L(LPC, '0·2175 or 174/800'),
     L(LPC, 'CI formulated with some substitution'), L(HPC, 'CI fully substituted')],
 'maths-2019-hl-p2-q8-a-ii': [L(SOL, '(95 − 87·3)/12 = 0·64167 (z score)'), L(SOL, '=> p(Z ≤ 0·64167) = 0·7389'), L(SOL, 'P(z ≥ 0·64) = 1 − 0·7389'),
     L(SOL, '= 0·2611 or 26·11%'), L(LPC, 'μ or σ identified'), L(MPC, 'z found'), L(HPC, 'P(z < 0·64) and stops or continues incorrectly')],
 'maths-2019-hl-p2-q8-a-iii': [L(SOL, 'z = −0·52 = (x − 87·3)/12'), L(SOL, '=> x = 81·06 km/h'), L(SOL, 'x = 81 km/h'), L(LPC, '(x − 87·3)/12'),
     L(LPC, 'z ∈ [0·52, 0·53] or z ∈ [−0·52, −0·53] and stops'), L(HPC, 'Formula for x fully substituted')],
 'maths-2019-hl-p2-q8-b-i': [L(SOL, 'Average speed has changed'), L(SOL, 'p-value < 0·05'), L(MPC, 'Answer or reason correct')],
 'maths-2019-hl-p2-q8-b-ii': [L(SOL, '0·024 = 2(1 − P(z ≤ |T|))'), L(SOL, '=> P(z ≤ |T|) = 0·988'), L(SOL, 'Therefore z = 2·26 or − 2·26.'),
     L(SOL, 'Because the mean has reduced z = −2·26'), L(SOL, '=> x = 84·588 km/h'), L(SOL, '=> x = 84·6'), L(LPC, '0·024 = 2(0·012)'),
     L(LPC, 'Value(s) of z found'), L(HPC, 'Formula for x fully substituted')],
 'maths-2019-hl-p2-q9-a': [L(SOL, '|SG|² = 30² + 58² − 2(30)(58)(cos 68)'), L(SOL, '= 2960·369'), L(SOL, '|SG| = 54·409 m'), L(SOL, '|SG| = 54·4'),
     L(LPC, 'Some relevant substitution into correct cosine formula'), L(HPC, 'Formula fully substituted')],
 'maths-2019-hl-p2-q9-b': [L(SOL, '54·4/sin 68 = 30/sin ∠HSG'), L(SOL, 'sin ∠HSG = 0·51131'), L(SOL, '|∠HSG| = 30·75'),
     L(LPC, 'Some relevant substitution into relevant formula'), L(HPC, 'Formula fully substituted')],
 'maths-2019-hl-p2-q9-c': [L(SOL, 'Area ∆GSH = 1/2(30)(58) sin 68 = 806·65'), L(LPC, 'Some substitution into area formula'), L(HPC, 'Formula fully substituted')],
 'maths-2019-hl-p2-q9-d-i': [L(SOL, '1/2 (58)(r) or 29r'), L(MPC, 'Right angle indicated'), L(MPC, 'Relevant triangle indicated on diagram'),
     L(MPC, 'Area of triangle formula with some substitution')],
 'maths-2019-hl-p2-q9-d-ii': [L(SOL, '= 15r + 27·2r + 29r = 71·2r'), L(LPC, 'Relevant use of previous answer in this part'),
     L(LPC, 'Indication of 3 relevant triangle areas to be added'), L(LPC, 'Area of 1 additional triangle (in terms of r)'),
     L(HPC, 'Addition of 2 areas ( each written in terms of r)')],
 'maths-2019-hl-p2-q9-d-iii': [L(SOL, '71·2r = 806·62'), L(SOL, '= 11·3289 = 11·3'), L(LPC, 'Both relevant answers presented'), L(HPC, 'Areas equated')],
 'maths-2019-hl-p2-q9-e': [L(SOL, 'tan 14 = |TS|/|PS|'), L(SOL, '=> |PS| = 42·619'), L(SOL, '|TS| = 10·626 = 10·6'), L(ALT, '|PS| = 42·73'),
     L(ALT, '|TS| = 10·653 = 10·7')] + SUB,
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2019, 'hl', 'p2', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 4, 7, 10], '10D': [0, 4, 5, 8, 10], '15C': [0, 5, 10, 15], '15D': [0, 5, 7, 11, 15]},
          'LC003ALP200EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
cls = 'A class consists of 12 boys and 8 girls.'
A('1-a-i', 'Q1(a)(i)', '10C', [32], [4], '1-2', 'probability', 'Two students are selected at random from the class. What is the probability that the two students selected will be a boy and a girl in any order?', stem=cls)
A('1-a-ii', 'Q1(a)(ii)', '10D', [32], [4], '1-2', 'probability', 'Four students are selected, one at a time, at random from the class. What is the probability that the first three students selected will be boys and the fourth will be a girl?', stem=cls)
A('1-b', 'Q1(b)', '5C', [33], [5], '1-1', 'probability', 'An examination paper is made up of two sections, Section A consisting of 7 questions and Section B consisting of 8 questions. The paper contains the following instruction: “From section A you must answer question 1 and any three other questions. From Section B you must also answer any four questions.” Find how many different combinations of questions may be answered if a candidate follows this instruction.')
A('2-a', 'Q2(a)', '10C', [34], [6], '2-2', 'co-ordinate-geometry-of-the-line', 'The line p makes an intercept on the x-axis at (a, 0) and on the y-axis at (0, b), where a, b ≠ 0. Show that the equation of p can be written as x/a + y/b = 1.')
ln = 'The line l has a slope m, and contains the point A(6, 0).'
A('2-b-i', 'Q2(b)(i)', '5B', [35], [6], '2-2', 'co-ordinate-geometry-of-the-line', 'Write the equation of the line l in terms of m.', stem=ln)
A('2-b-ii', 'Q2(b)(ii)', '10D', [35], [7], '2-2', 'co-ordinate-geometry-of-the-line,algebra-simultaneous-equations', 'The line l cuts the line k: 4x + 3y = 25 at P. Find the co-ordinates of P in terms of m. Give each co-ordinate as a fraction in its simplest form.', stem=ln + ' Part (b)(i): Write the equation of the line l in terms of m.')
A('3-a', 'Q3(a)', '10C', [36], [8], '2-2', 'co-ordinate-geometry-of-the-circle', 'The point (−2, k) is on the circle (x − 2)² + (y − 3)² = 65. Find the two possible values of k, where k ∈ ℤ.')
A('3-b', 'Q3(b)', '15D', [37], [9], '2-2', 'co-ordinate-geometry-of-the-circle', 'The circle s is in the first quadrant. It touches both the x-axis and the y-axis. The line t: 3x − 4y + 6 = 0 is a tangent to s as shown. Find the equation of s.')
A('4-a', 'Q4(a)', '10C', [38], [10], '2-3', 'trigonometry-functions-identities', 'Show that cos 2θ = 1 − 2 sin² θ.')
A('4-b', 'Q4(b)', '15D', [39], [11], '2-3', 'trigonometry-triangles', 'Find the cosine of the acute angle between two diagonals of a cube.')
A('5-a', 'Q5(a)', '15D', [40], [12], '2-1', 'geometry-constructions-proofs', 'Construct and label the orthocentre of the triangle ABC in the diagram below. Show any construction lines or arcs clearly.')
A('5-b', 'Q5(b)', '10D', [40], [13], '2-1', 'geometry', 'In the diagram below O is the centre of circle s. [AB] is a diameter of s. BE is a tangent to s at point B. [CD] is a chord of circle s. |CD| = ½|AB| and CD is parallel to AB. Find, with justification, |∠BEA|.')
A('6-a', 'Q6(a)', '10C', [41], [14], '1-2', 'probability', 'Two independent events F and S are represented in the Venn diagram shown below. P(F \\ S) = 1/4, P(F ∩ S) = 1/5, P(S \\ F) = x, and P(F ∪ S)′ = y, where x, y ≠ 0. Find the value of x and the value of y.')
A('6-b', 'Q6(b)', '15D', [42], [15], '1-2', 'probability,algebra-quadratics', 'In a club there are German, Irish and Spanish children only. There are 10 Spanish children. There are twice as many Irish children as German children. They are all in a group waiting to get on a swing. One child will be selected at random to go first and will not re-join the group. Then a second child will be selected at random to go next. The probability that the first child selected will be German and that the second child selected will not be German is 1/6. Find how many children are in the club.')
tr = 'A cattle feeding trough of uniform cross section and 2·5 m in length, is shown in Figure 1. The front of the trough (segment ABC) is shown in Figure 2. The front of the trough is a segment of a circle of radius 90 cm. The height of the trough, |DB|, is 30 cm. |OA| = |OC| = |OB| = 90 cm. [OB] ⊥ [AC].'
A('7-a-i', 'Q7(a)(i)', '10C', [43], [16], '3-4', 'area-volume,trigonometry-triangles', 'Find |AD|. Give your answer in the form a√b cm, where a, b ∈ ℤ.', stem=tr)
A('7-a-ii', 'Q7(a)(ii)', '5C', [43], [16, 17], '2-3', 'trigonometry-triangles', 'Find |∠DOA|. Give your answer in radians, correct to 2 decimal places.', stem=tr)
A('7-a-iii', 'Q7(a)(iii)', '10D', [43], [16, 17], '3-4', 'area-volume', 'Find the area of the segment ABC. Give your answer in m² correct to 2 decimal places.', stem=tr)
A('7-a-iv', 'Q7(a)(iv)', '5C', [43], [16, 17], '3-4', 'area-volume', 'Find the volume of the trough. Give your answer in m³, correct to 2 decimal places.', stem=tr)
st = 'A sand timer for games is shown in the diagram. Each half of the timer consists of a hemisphere, a cylinder of height 3·5 cm and a cone of height 1·5 cm. All of the parts have a radius of 1·25 cm.'
A('7-b-i', 'Q7(b)(i)', '15D', [44], [18], '3-4', 'area-volume', 'The upper half of the timer is full of sand. Find the volume of sand in the upper half of the timer. Give your answer in cm³ correct to 2 decimal places.', stem=st)
A('7-b-ii', 'Q7(b)(ii)', '5C', [44], [19], '3-4', 'area-volume', 'Sand flows from the top half of the timer into the bottom part. As it flows the top surfaces in both parts remain level. At a certain time, 98% of the sand has flowed into the bottom half of the timer. Find h, the height of the remaining sand (in the conical part of the top of the timer). Give your answer in cm, correct to 2 decimal places.', stem=st + ' The upper half of the timer is full of sand.')
mag = 'A motoring magazine collected data on cars on a particular stretch of road. Certain details on 800 cars were recorded.'
spd = ' The data on the speeds of these 800 vehicles is normally distributed with an average speed of 87·3 km per hour and a standard deviation of 12 km per hour.'
A('8-a-i', 'Q8(a)(i)', '10C', [45], [20], '1-7', 'statistics-inferential-statistics', 'The ages of the 800 cars were recorded. 174 of them were new (less than 1 year old). Find the 95% confidence interval for the proportion of new cars on this road. Give your answer correct to 4 significant figures.', stem=mag)
A('8-a-ii', 'Q8(a)(ii)', '15D', [45], [20], '1-3', 'statistics-z-scores', spd.strip() + ' What proportion of cars on this stretch of road would you expect to find travelling at over 95 km per hour?', stem=mag)
A('8-a-iii', 'Q8(a)(iii)', '10C', [45], [21], '1-3', 'statistics-z-scores', 'The driver of a car was told that 70% of all the speeds recorded were higher than his speed. Find the speed at which this driver was recorded. Give your answer correct to the nearest whole number.', stem=mag + spd)
rs = 'A road safety programme was carried out in the area using posters, signs and radio slots. After the programme the motoring magazine recorded the speeds of 100 passing cars. The magazine carried out a hypothesis test, at the 5% level of significance, to determine whether the average speed had changed. The p-value of the test was 0·024.'
A('8-b-i', 'Q8(b)(i)', '5B', [46], [21], '1-7', 'statistics-inferential-statistics', rs + ' What can the magazine conclude based on this p-value? Give a reason for your answer.', stem=mag)
A('8-b-ii', 'Q8(b)(ii)', '5C', [46], [21], '1-7', 'statistics-inferential-statistics,statistics-z-scores', 'The magazine found that the average speed of this sample was lower than the previously established average speed of 87·3 km per hour. Find the average speed of the cars in this sample, correct to 1 decimal place.', stem=mag + spd + ' Part (b)(i): ' + rs)
heli = 'The diagram below shows a triangular patch of ground ∆SGH, with |SH| = 58 m, |GH| = 30 m, and |∠GHS| = 68°. The circle is a helicopter pad. It is the incircle of ∆SGH and has centre P.'
tt = 'trigonometry-triangles'
A('9-a', 'Q9(a)', '10C', [47], [22], '2-3', tt, 'Find |SG|. Give your answer in metres, correct to 1 decimal place.', stem=heli)
A('9-b', 'Q9(b)', '10C', [47], [22], '2-3', tt, 'Find |∠HSG|. Give your answer in degrees, correct to 2 decimal places.', stem=heli)
A('9-c', 'Q9(c)', '15C', [47], [23], '2-3', tt + ',area-volume', 'Find the area of ∆SGH. Give your answer in m², correct to 2 decimal places.', stem=heli)
A('9-d-i', 'Q9(d)(i)', '5B', [47], [23], '2-1', 'geometry,area-volume', 'Find the area of ∆HSP, in terms of r, where r is the radius of the helicopter pad.', stem=heli)
A('9-d-ii', 'Q9(d)(ii)', '5C', [48], [23], '2-1', 'geometry,area-volume', 'Show that the area of ∆SGH, in terms of r, can be written as 71·2r m².', stem=heli)
A('9-d-iii', 'Q9(d)(iii)', '5C', [48], [23], '2-1', 'geometry,area-volume', 'Find the value of r. Give your answer in metres, correct to 1 decimal place.', stem=heli)
A('9-e', 'Q9(e)', '5C', [48], [24], '2-3', tt, '[ST] is a vertical pole at the point S. The angle of elevation of the top of the pole from the point P is 14°. Find the height of the pole. Give your answer, in metres, correct to 1 decimal place.', stem=heli)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 50, '8': 45, '9': 55}
p.check(marks, 32)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 29–50 of the combined Higher Level scheme (the Paper 2 title page 29, the Paper 2 scale table on page 30, the summary of mark allocations on page 31, every Paper 2 model solution and marking note on pages 32–48 and the blank back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(29, 51)), [30, 31],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 50 marks, Q8 45 marks, Q9 55 marks). Every question is retained.',
     '32 independently marked units, matching the printed summary on scheme page 31. The summary labels Q4(b), Q5(b) and Q6(a) as “(b)(i)” and “(a)(i)”, and the scheme labels Q9(e) “(e)(ii)”; the paper prints each as a single undivided part, which the cards cite.',
     'Paper 2 bands from the scale table on scheme page 30 and the ladders printed beside each part: 5B 0,2,5; 5C 0,2,3,5; 10C 0,4,7,10; 10D 0,4,5,8,10; 15C 0,5,10,15; 15D 0,5,7,11,15 (Paper 2’s 15D ladder differs from Paper 1’s 0,4,7,11,15).',
     'This paper had no authored cards before this review; all 32 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; parts with several printed methods keep each method’s ladder. Q5(a) is a construction whose model solution is a drawing; its card carries the printed credit criteria.',
     'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [5], 'wording': '“From section A you must answer question 1 and any three other questions. From Section B you must also answer any four questions.”', 'classification': 'mathematical-counting',
      'reason': 'The quoted instruction is the counting problem itself (choose 3 of 6 and 4 of 8), not an instruction to the candidate sitting this paper.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('mathematical-counting', 'The quoted exam instruction is the data of a counting task (choose 3 of 6 and 4 of 8); it does not select prompts on this paper.') if 'any three other questions' in t or 'any four questions' in t else None)
p.apply(ROWS, '2019 Higher Level Paper 2', expect_added=[c['id'] for c in p.cards])
