"""2020 HL Paper 2: a new paper — 30 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
M1, M2, M3 = 'Method 1, ', 'Method 2, ', 'Method 3, '

ROWS = {
 'maths-2020-hl-p2-q1-a': [L(SOL, 'Equation BC 3x + 2y + 6 = 0.'), L(SOL, '(3(2) + 2(−6) + 6)/√(3² + 2²) = (6 − 12 + 6)/√13 = 0/√13 = 0.'),
     L(SOL, 'Therefore A, B and C are collinear.'), L(LPC, 'Slope formula with some substitution'),
     L(LPC, 'Equation of line formula with some substitution'), L(LPC, 'Effort at finding are of triangle ABC'), L(MPC, 'Equation of BC'),
     L(HPC, 'Perp. Distance formula with some substitution from relevant line'), L(HPC, 'Area of triangle ABC = 0 but perp. distance not explicit'),
     L(FCM, 'Distance = 0 but conclusion omitted'), L(FCM, 'Area of triangle ABC = 0 and perp. dist. = 0 but conclusion omitted')],
 'maths-2020-hl-p2-q1-b': [L(SOL, 'Slope of b = tan 60° = √3'), L(SOL, '= ±(−8 + 5√3)'), L(SOL, 'θ = 33·435°'), L(ALT, 'θ + 26·565° + 120° = 180°'),
     L(M1 + LPC, 'Slope of a = 1/2'), L(M1 + LPC, 'Slope of b = tan 60°'), L(M1 + MPC, 'Tan formula with some relevant substitution'),
     L(M1 + HPC, 'Tan formula fully substituted'), L(M1 + FCM, 'θ = +tan⁻¹(−8 + 5√3)'), L(M2 + LPC, 'Slope of a = 1/2'), L(M2 + LPC, '120°'),
     L(M2 + MPC, 'tan⁻¹ 1/2 + 120°'), L(M2 + HPC, 'θ + 26·565° + 120° = 180° and fails to finish')],
 'maths-2020-hl-p2-q2-a': [L(SOL, 'Centre: (2, −1)'), L(SOL, 'Radius: √(2² + (−1)² + 4) = 3'), L(SOL, 'Distance from centre to B: √90'),
     L(SOL, 'Pythagoras: |BT|² = 90 − 3² = 81'), L(SOL, '⟹ |BT| = 9'), L(LPC, 'Centre or radius'), L(MPC, '√90'),
     L(HPC, 'Pythagoras fully substituted (: |BT|²)')],
 'maths-2020-hl-p2-q2-b': [L(SOL, 'Centre (– g, 0).'), L(SOL, '⟹ g² + 2g − 8 = 0'), L(SOL, 'Centres are (−2, 0) and (4, 0)'),
     L(SOL, '(x + 2)² + y² = 25,'), L(SOL, '(x − 4)² + y² = 25'), L(M1 + LPC, 'Centre (– g, 0) or equivalent'),
     L(M1 + LPC, 'Some substitution of (1, 4) into general equation of circle'), L(M1 + MPC, '2 relevant equations in g and c'),
     L(M1 + HPC, 'Quadratic in g (g² + 2g − 8 = 0 or equivalent)'), L(M2 + LPC, 'Some substitution into distance formula'),
     L(M2 + MPC, 'Distance formula fully substituted'), L(M2 + HPC, 'Quadratic in g'), L(M3 + LPC, 'Diagram with (1, 0) identified'),
     L(M3 + MPC, '-2 or 4 identified'), L(M3 + HPC, 'g = −4 and g = 2')],
 'maths-2020-hl-p2-q3-a': [L(SOL, '6/sin 17° = |HF|/sin 35°'), L(SOL, '|HF| = 6 sin 35°/sin 17° = 11·771'), L(SOL, 'x = 11·771(sin 33°)/sin 95°'),
     L(SOL, 'x = 6·44 m'), L(SOL, '(Or x = 6·43 m from rounded |HF|)'), L(LPC, '|∠FHE| = 17°'), L(LPC, '|∠GHF| = 33°'),
     L(LPC, 'Some relevant substitution into relevant formula'), L(HPC, '|HF| found and stops'), L(HPC, '|HE| = 16·17 found and stops'),
     L(HPC, 'Incorrect value of |HF| (or |HE|) used correctly to find x')],
 'maths-2020-hl-p2-q3-b': [L(SOL, '|∠BOA| = 60° => |∠COA| = 30°'), L(SOL, 'sin ∠COA = r/DO = 1/2'), L(SOL, '⟹ |DO| = 2r'), L(SOL, '⟹ |OC| = 3r'),
     L(SOL, 'Area c = πr²'), L(SOL, 'Area s = π(3r)² = 9πr²'), L(SOL, 'Area s : Area c = 9 : 1 ⟹ k = 9'), L(LPC, '30°'), L(LPC, 'Area c = πr²'),
     L(MPC, '|DO| = 2r'), L(HPC, '|OC| = 3r')],
 'maths-2020-hl-p2-q4-a': [L(SOL, 'Reference angle: π/6'), L(SOL, '2nd Quadrant: π − π/6 = 5π/6'), L(SOL, 'θ/2 = 5π/6 + 2nπ'), L(SOL, 'θ = 5π/3 + 4nπ'),
     L(SOL, 'n = 0 ⟹ θ = 5π/3 = 300°'), L(SOL, '4nd Quadrant: 2π − π/6 = 11π/6'), L(SOL, 'θ = 11π/3 + 4nπ'), L(SOL, 'n = 0 ⟹ θ = 11π/3 = 660°'),
     L(LPC, '30° or –30°'), L(LPC, 'Mention of 2nd or 4th quadrants'), L(MPC, '150° or 330° or equivalent'), L(HPC, '150° and 330° or equivalent')],
 'maths-2020-hl-p2-q4-b': [L(SOL, 'Area of ∆COA = Area of Sector − 21'), L(SOL, '= ½r²θ − 21 = 8·4'), L(SOL, 'Area of ∆COA: 1/2|CO||7| sin 1·2 = 8·4'),
     L(SOL, '|CO| = 8·4/(3·5 sin 1·2) = 2·57'), L(SOL, '|BC| = 7 − 2·6 = 4·4 cm'), L(LPC, 'Area of ∆COA'), L(LPC, 'Area of Sector COA'),
     L(MPC, 'Area of ∆COA = Area of Sector − 21'), L(HPC, '½|CO||7| sin 1·2 = 8·4'), L(FCM, 'Distance |CO| found and stops')],
 'maths-2020-hl-p2-q5-a-i': [L(SOL, 'P(B|A) = P(A ∩ B)/P(A)'), L(SOL, '= 2/3'), L(LPC, 'Formula for P(B|A)'), L(HPC, 'Formula fully substituted')],
 'maths-2020-hl-p2-q5-a-ii': [L(SOL, 'P(A ∪ B) = P(A) + P(B) − P(A ∩ B)'), L(SOL, '11/12 = 3/4 + P(B) − 1/2'), L(SOL, '11/12 − 1/4 = P(B) = 2/3'),
     L(SOL, 'Check if: P(A) × P(B) = P(A ∩ B)'), L(SOL, '3/4 × 2/3 = 6/12 = 1/2 = P(A ∩ B)'), L(SOL, '⇒ Independent'), L(ALT, 'P(B|A) = P(B)'),
     L(LPC, 'Condition for independent events'), L(HPC, 'P(B) = 2/3'),
     L(HPC, 'P(A) × P(B) = P(A ∩ B) fully checked for any relevant value (< 1) of P(B) with a valid conclusion')],
 'maths-2020-hl-p2-q5-b': [L(SOL, 'Lee has 6 chances to win.'), L(SOL, 'The others only have 5 chances'), L(SOL, '⟹ It is not a fair game'),
     L(LPC, 'Any relevant listing of remainders/sums'), L(HPC, 'All remainders listed but no conclusion or incorrect conclusion or unsound conclusion')],
 'maths-2020-hl-p2-q6-a': [L(SOL, 'P(VW) = 0·21 + 0·15 + 0·009'), L(SOL, '= 0·369'), L(LPC, 'Any relevant probability from line 1 written'),
     L(MPC, 'Any 1 relevant probability from line 3 formulated or written'), L(HPC, 'All 3 relevant probability from line 3 formulated or written')],
 'maths-2020-hl-p2-q6-b-i': [L(SOL, '(3/4)³ 1/4 = 135/2048'), L(LPC, '(5 2) or 3/4 or (1/4)² or (1/4)³'),
     L(HPC, '(5 2)(1/4)^x (3/4)^y where x, y ≠ 1')],
 'maths-2020-hl-p2-q6-b-ii': [L(SOL, 'P(2 or less) = P(0 pass + 1 pass + 2 pass)'), L(SOL, 'P(0 pass) = (1/2)^n'),
     L(SOL, '= (2 + 2n + n² − n)/2^(n+1) = (n² + n + 2)/2^(n+1)'), L(SOL, '⟹ a = 1, b = 1, c = 2.'), L(LPC, 'P(0 pass + 1 pass + 2 pass)'),
     L(HPC, 'Any two of (1/2)^n or [(n 1)(1/2)¹(1/2)^(n−1)] or [(n 2)(1/2)²(1/2)^(n−2)]')],
 'maths-2020-hl-p2-q7-a-i': [L(SOL, '9² = 3·3² + ℎ²'), L(SOL, 'ℎ² = 81 − 10·89'), L(SOL, 'ℎ = 8·37'), L(LPC, 'Pythagoras formulated'),
     L(HPC, '√(9² − 3·3²) or equivalent')],
 'maths-2020-hl-p2-q7-a-ii': [L(SOL, 'CSA = πrl = π3·3(9) = 93·31 cm²'), L(LPC, 'Formula for CSA with some substitution'), L(HPC, 'Formula fully substituted')],
 'maths-2020-hl-p2-q7-a-iii': [L(SOL, 'Circumference of cup = 2πr = 2π(3·3)'), L(SOL, 'Arc length of sector = (2π × 9θ)/360°'), L(SOL, 'θ = 3·3(360)/9 = 132°'),
     L(LPC, 'Formula for circumference or arc length with some substitution'), L(HPC, 'Both formulas fully substituted')],
 'maths-2020-hl-p2-q7-b': [L(SOL, '3·3/8·37 = r/7·37'), L(SOL, 'r = 2·905 cm'), L(SOL, 'v = 1/3 π(2·905)² 7·37'), L(SOL, '65·16 cm³'), L(SOL, '65·2 cm³'),
     L(LPC, 'Any relevant effort to find r using similar triangles'), L(MPC, 'r found'), L(HPC, 'Volume formula fully substituted'),
     L(NOTE, 'If r = 3·3 used then award MPC at most')],
 'maths-2020-hl-p2-q7-c': [L(SOL, 'Volume of water in one second π0·8²(2·5)'), L(SOL, '= 5·0265 cm³'), L(SOL, 'Time taken is 65·2/(π0·8²(2·5)) = 13'),
     L(LPC, 'Any relevant effort to find volume of water'), L(MPC, 'π0·8²(2·5)'), L(HPC, 'Time formula fully substituted'),
     L(NOTE, 'Accept work using candidates volume from part (b)')],
 'maths-2020-hl-p2-q7-d': [L(SOL, '3·3/8·37 = r/ℎ'), L(SOL, 'r = 3·3ℎ/8·37'), L(SOL, 'ℎ³ = (60 × 8·37² × 3)/(π3·3²)'), L(SOL, 'x = 8·37 − 7·169 = 1·2'),
     L(LPC, 'Effort to link r and ℎ'), L(MPC, 'r and ℎ linked'), L(HPC, 'ℎ³ = (60 × 8·37² × 3)/(π3·3²) or equivalent')],
 'maths-2020-hl-p2-q8-a-i': [L(SOL, 'z = (x − x̅)/σ'), L(SOL, '(x − 280)/90 = 0·68'), L(SOL, '⟹ x = 341·2'), L(SOL, 'x = 342'), L(LPC, 'μ or σ identified'),
     L(MPC, '0·68'), L(HPC, 'Equation in x fully substituted and stops or continues incorrectly')],
 'maths-2020-hl-p2-q8-a-ii': [L(SOL, 'Eileen’s z-score = (260 − 280)/90 = −0·222 = z'), L(SOL, '40% z-score = −0·25 i.e. z score for 60%'),
     L(SOL, '−0·222 > −0·25'), L(SOL, 'Eileen is eligible to re-sit the test.'), L(ALT, 'P(0·222) = 0·5871'), L(ALT, '1 − 0·5871 = 0·4129'),
     L(ALT, '41·29%'), L(LPC, 'μ or σ identified'), L(MPC, '(260 − 280)/90 or −0·222 or −0·25'), L(HPC, '−0·222 and −0·25'), L(NOTE, 'Allow −0·26')],
 'maths-2020-hl-p2-q8-b-i': [L(SOL, '95% of the of the data lies in the interval −1·96 ≤ z ≤ 1·96'), L(PC, '95% without context')],
 'maths-2020-hl-p2-q8-b-ii': [L(SOL, '1·96√(p̂(1 − p̂)/2500) = 0·01568'), L(SOL, '⟹ p̂² − p̂ + 4/25 = 0'), L(SOL, 'p̂ = 4/5 or 1/5'),
     L(SOL, '1/5 outside the range'), L(SOL, '⟹ p̂ = 4/5'), L(LPC, '√(p̂(1 − p̂)/2500) or equivalent written'), L(MPC, 'Formula fully substituted'),
     L(HPC, 'Quadratic in form ap̂² + bp̂ + c = 0')],
 'maths-2020-hl-p2-q8-c': [L(SOL, 'H₀: Mean weight of bags has not changed'), L(SOL, 'H₁: Mean weight of bags has changed'),
     L(SOL, 'z = (x̅ − μ)/(σ/√n) = (13·1 − 12)/(4·5/√80) = 2·186'), L(SOL, '2·186 > 1·96'), L(SOL, 'Mean weight of the bags has changed'),
     L(LPC, 'CI formulated with some correct substitution'), L(LPC, '1·96'), L(LPC, 'H₀ or H₁'), L(HPC, 'z score fully substituted')],
 'maths-2020-hl-p2-q8-d': [L(SOL, 'P(weight > 3000)'), L(SOL, '= P(Average of those on bus > 3000/40)'), L(SOL, 'P(x̅ > 75) = 1 − P(x̅ < 75)'),
     L(SOL, 'z = (75 − 73)/(12/√40) = 1·054'), L(SOL, 'This gives a proportion of 0·8531.'), L(SOL, '1 − 0·8531 = 0·1469'), L(SOL, '= 14·69%'),
     L(SOL, 'This is the probability that the bus with 40 passengers will be above the maximum weight allowance.'), L(LPC, '3000/40'),
     L(LPC, 'μ or σ identified'), L(MPC, 'z formula fully substituted'), L(HPC, '1·054')],
 'maths-2020-hl-p2-q8-e': [L(SOL, 'Median is 12·5 ⟹ D + E = 25'), L(SOL, 'LQ is 7·5 ⟹ B + C = 15'), L(SOL, '⟹ The upper quartile = 19·5'),
     L(SOL, 'G = 23 so F = 39 – 23 = 16'), L(SOL, 'So A + H = 108 – 79 = 29'), L(SOL, 'A = 4 and H = 25'),
     L(SOL, 'D + E = 25 so D = 11, E = 14 (cannot be 12 and 13 also cannot be 10 and 15)'),
     L(SOL, 'B + C = 15 so B = 6, C = 9 (cannot be 7 and 8 also cannot be 5 and 10)'), L(LPC, 'One unknown number given'),
     L(LPC, 'One relevant equation written'), L(MPC, 'Three unknown numbers given'), L(MPC, 'Three relevant equations written'),
     L(HPC, 'Five unknown numbers given'), L(HPC, 'Five relevant equations written')],
 'maths-2020-hl-p2-q9-a': [L(SOL, 'd = √((90 − 15/2)² + (30/2)²)'), L(SOL, 'd = √((82·5)² + (15)²)'), L(SOL, 'd = 83·85 km'), L(LPC, '15/2 or 30/2'),
     L(LPC, 'Indication of Pythagoras'), L(HPC, 'Pythagoras fully substituted')],
 'maths-2020-hl-p2-q9-b': [L(SOL, 's² = (90 − 15t)² + (30t)²'), L(SOL, 's² = 8100 − 2700t + 225t² + 900t²'), L(SOL, 's² = 1125t² − 2700t + 8100'),
     L(SOL, 's = (1125t² − 2700t + 8100)^(1/2)'), L(LPC, '90 – 15t or 30t'), L(HPC, 'Pythagoras fully substituted')],
 'maths-2020-hl-p2-q9-c': [L(SOL, 'ds/dt = (2250t − 2700)/(2√(1125t² − 2700t + 8100))'), L(SOL, '⟹ 2250t − 2700 = 0'), L(SOL, 't = 2700/2250 = 1·2 hours'),
     L(SOL, 's = 80·4984 ≈ 80·5 km'), L(LPC, 'Any correct differntiation'), L(MPC, 'Value of t found'), L(HPC, 'Formula for s fully substituted'),
     L(HPC, 'Incorrect value of t (found through calculus) substituted and worked correctly.'), L(NOTE, 'No calculus ⇒ 0 credit')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2020, 'hl', 'p2', {'5B': [0, 2, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 4, 8, 10], '10D': [0, 3, 5, 8, 10],
                             '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15]},
          'LC003ALP200EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
A('1-a', 'Q1(a)', '15D', [28], [4], '2-2', 'co-ordinate-geometry-of-the-line', 'The coordinates of three points are A(2, −6), B(6, −12), and C(−4, 3). Find the perpendicular distance from A to BC. Based on your answer, what can you conclude about the relationship between the points A, B, and C?')
A('1-b', 'Q1(b)', '10D', [29], [5], '2-2', 'co-ordinate-geometry-of-the-line,trigonometry-functions-identities', 'The diagram below shows two lines a and b. The equation of a is x − 2y + 1 = 0. The acute angle between a and b is θ. Line b makes an angle of 60° with the positive sense of the x-axis, as shown in the diagram. Find the value of θ, in degrees, correct to 3 decimal places.')
A('2-a', 'Q2(a)', '10D', [30], [6], '2-2', 'co-ordinate-geometry-of-the-circle', 'The circle c has equation x² + y² − 4x + 2y − 4 = 0. The point A is the centre of the circle. The line l is a tangent to c at the point T, as shown in the diagram. The point B(5, 8) is on l. Find |BT|.')
A('2-b', 'Q2(b)', '15D', [30, 31], [7], '2-2', 'co-ordinate-geometry-of-the-circle', 'Two circles, c₁ and c₂, have their centres on the x-axis. Each circle has a radius of 5 units. The point (1, 4) lies on each circle. Find the equation of c₁ and the equation of c₂.')
A('3-a', 'Q3(a)', '15C', [32], [8], '2-3', 'trigonometry-triangles', 'A flagpole [GH], shown in the diagram, is vertical and the ground is inclined at an angle of 5° to the horizontal between E and G. The angles of elevation from E and F to the top of the pole are 35° and 52° respectively. The distance from E to F along the incline is 6 m. Find how far F is from the base of the pole (G) along the incline. Give your answer correct to two decimal places.')
A('3-b', 'Q3(b)', '10D', [32], [9], '2-1', 'geometry,trigonometry-triangles', 'In the diagram the large circle s has centre O and the small circle c has centre D. The circle c touches the circle s at the point C. OA and OB are tangents to c as shown. The radius of c is r. |∠BOA| = 60°. The ratio of the area of s to the area of c is k : 1. Find the value of k.')
A('4-a', 'Q4(a)', '15D', [33], [10], '2-3', 'trigonometry-functions-identities', 'Find the two values of θ for which tan(θ/2) = −1/√3, where 0 ≤ θ ≤ 4π.')
A('4-b', 'Q4(b)', '10D', [33], [11], '2-3', 'trigonometry-triangles,area-volume', 'The diagram shows OAB, a sector of a circle of radius 7 cm with centre O. In the sector, |∠BOA| = 1·2 radians. The area of the shaded region is 21 cm². Find |BC|. Give your answer correct to 1 decimal place.')
ab = 'Two events A and B are such that P(A) = 3/4 and P(A ∩ B) = 1/2.'
A('5-a-i', 'Q5(a)(i)', '15C', [34], [12], '1-2', 'probability', 'Find P(B|A). Give your answer as a fraction in its simplest form.', stem=ab)
A('5-a-ii', 'Q5(a)(ii)', '5C', [34], [12], '1-2', 'probability', 'P(A ∪ B) = 11/12. Investigate if the events A and B are independent.', stem=ab)
A('5-b', 'Q5(b)', '5C', [35], [13], '1-2', 'probability', 'A spinner consists of 4 segments, as shown. Each segment is equally likely to be landed on. Liam, Sorcha and Lee play a game in which the spinner is spun twice and the numbers landed on are added together. The result is divided by 3 and the remainder is recorded. If the remainder is 0 then Liam wins the game. If the remainder is 1 then Sorcha wins the game. If the remainder is 2 then Lee wins the game. Is this a fair game? (i.e. Are all 3 participants equally likely to win?) Justify your answer by relevant calculations.')
A('6-a', 'Q6(a)', '10D', [36], [14], '1-2', 'probability', 'A class group carried out a study of the makes and fuel types of cars in a large carpark. It found that 30% of the cars ran on diesel and 70% of these diesel cars were Volkswagen. It found that 60% of the cars ran on petrol and 25% of these petrol cars were Volkswagen. It found that 10% of the cars were hybrid/electric and 9% of these cars were Volkswagen. One car is selected at random from the car park. Find the probability that it is a Volkswagen car.')
rsa = 'The Road Safety Authority has data on driving test pass rates at all its test centres.'
A('6-b-i', 'Q6(b)(i)', '10C', [36], [14], '1-2', 'probability', 'In a particular Driving Test Centre the probability that a person taking the test for the first time will pass is 1/4. All of the test results are independent. In this centre on a particular day Joe, along with 5 others, takes the test. All six are taking the test for the first time. Find the probability that Joe passes the test along with exactly 2 others.', stem=rsa)
A('6-b-ii', 'Q6(b)(ii)', '5C', [36], [15], '1-2', 'probability,algebra-expressions-factorising', 'The overall pass rate for all drivers at another centre is 1/2 (Whether it is their first attempt or a subsequent attempt). On a particular day, n people take the test in this centre. The probability that two people or less than two people pass the test can be written in the form (an² + bn + c)/2^(n+1), where a, b, c ∈ ℕ. Find the value of a, the value of b, and the value of c.', stem=rsa)
cup = 'A company makes biodegradable paper cups in the shape of a right circular cone. Each cup has a radius of 3·3 cm and a slant height of 9 cm, as shown.'
A('7-a-i', 'Q7(a)(i)', '10C', [37], [16], '3-4', 'area-volume', 'Show that the vertical height of the cup is 8·37 cm, correct to 2 decimal places.', stem=cup)
A('7-a-ii', 'Q7(a)(ii)', '10C', [37], [16], '3-4', 'area-volume', 'Find the curved surface area of the cup correct to 2 decimal places.', stem=cup)
A('7-a-iii', 'Q7(a)(iii)', '10C', [37], [16], '3-4', 'area-volume', 'The diagram shows the net of the cup. Find, in degrees, the size of the angle θ.', stem=cup)
A('7-b', 'Q7(b)', '10D', [37], [17], '3-4', 'area-volume,geometry', 'In order to avoid spillages each cup is marked with a dotted line at F which is 1 cm vertically below the top of the cup, as shown. Find the volume of water in the cup when it is filled as far as the dotted line. Give your answer correct to 1 decimal place.', stem=cup)
cupf = cup + ' In order to avoid spillages each cup is marked with a dotted line at F which is 1 cm vertically below the top of the cup.'
A('7-c', 'Q7(c)', '5D', [38], [17], '3-4', 'area-volume', 'Water flows into one of these cups through a cylindrical pipe of radius 0·8 cm at a flow rate of 2·5 cm/sec. Find, to the nearest second, how long it will take to fill the cup to the line at F.', stem=cupf)
A('7-d', 'Q7(d)', '10D', [38], [18], '3-4', 'area-volume,geometry', 'The company decides to change the position of the line F in order to limit the capacity of the cup to 60 cm³. How far, vertically below the rim of the cup, should the line F be drawn? Give your answer, in cm, correct to 1 decimal place.', stem=cupf)
apt = 'An airline company Trans-sky Airways has designed an aptitude test for people applying for jobs as trainee pilots. The aptitude test is scored out of 500 marks. The results are normally distributed with a mean score of 280 and a standard deviation of 90.'
A('8-a-i', 'Q8(a)(i)', '15D', [39], [19], '1-3', 'statistics-z-scores', 'The top 25% of people taking the aptitude test are invited back for an interview. Find the minimum mark needed on the test in order to be invited back for interview.', stem=apt)
A('8-a-ii', 'Q8(a)(ii)', '10D', [39], [19], '1-3', 'statistics-z-scores', 'Anyone who scores above the 40th percentile can re-sit the test later. Eileen scored 260 marks in the test. Find out whether or not Eileen is eligible to re-sit the test.', stem=apt)
A('8-b-i', 'Q8(b)(i)', '5B', [39], [20], '1-7', 'statistics-inferential-statistics,statistics-z-scores', 'Explain the relevance of the z-scores −1·96 and 1·96 in the standard normal distribution.')
A('8-b-ii', 'Q8(b)(ii)', '10D', [40], [20], '1-7', 'statistics-inferential-statistics,algebra-quadratics', 'Trans-sky Airways surveyed 2500 of its passengers about a new service it proposed to introduce. The variable p̂ is the proportion of respondents in the survey who said they would use the new service. The radius of the 95% confidence interval of the survey was 0·01568. Find the value of p̂, where 0·5 < p̂ ≤ 1.')
A('8-c', 'Q8(c)', '10C', [40], [21], '1-7', 'statistics-inferential-statistics', 'The weight of the Airline passengers’ carry-on luggage is normally distributed with a mean of 12 kg. The Airline has recently introduced a fee for non-carry-on luggage. After the fee was introduced, the Airline expected the mean weight of the carry-on luggage to change. They selected a random sample of 80 passengers and weighed their carry-on luggage. The sample mean was 13·1 kg and the sample standard deviation was 4·5 kg. Test the hypothesis, at the 5% level of significance, that the mean weight of the carry-on luggage has changed. State the null hypothesis and the alternative hypothesis. Give your conclusion in the context of the question.')
A('8-d', 'Q8(d)', '10D', [41], [22], '1-7', 'statistics-inferential-statistics,statistics-z-scores', 'The company bus can carry passengers up to a total maximum weight allowance of 3000 kg. The weight of passengers is normally distributed with a mean of 73 kg and a standard deviation of 12 kg. 40 passengers board the bus. Find the probability that the total passenger weight will be over the maximum weight allowance. Give your answer as a percentage correct to 2 decimal places.')
A('8-e', 'Q8(e)', '10D', [42], [23], '1-6', 'statistics-descriptive-statistics', 'A list consists of eight whole numbers. They are labelled from A to H as shown below. The numbers are all greater than zero and are ordered from smallest to largest. The difference between any two adjacent numbers is 2 or more. The median of the list is 12·5. The lower quartile (the median of the 4 lowest numbers) of the list is 7·5. The interquartile range is 12. The second largest number is 23, as shown. The range of the list is 21. The mean of the list is 13·5. Find the numbers which satisfy all of the above conditions and write them into the boxes below.')
ship = 'Two ships set sail at the same time, Ship A from Port A and Ship B from Port B. Port A is 90 km due west of Port B, as shown below. Ship A is traveling due east at a speed of 15 km/h. Ship B is travelling due south at a speed of 30 km/h.'
A('9-a', 'Q9(a)', '15C', [43], [24], '2-3', 'trigonometry-triangles', 'Find the distance between the two ships 30 minutes after they set sail. Give your answer in km, correct to 2 decimal places.', stem=ship)
A('9-b', 'Q9(b)', '5C', [43], [24], '5-1', 'functions,trigonometry-triangles', 't is the time in hours after the ships set sail. Show that the distance between the ships at time t can be given by the function s(t) = (1125t² − 2700t + 8100)^(1/2), where 0 ≤ t ≤ 6.', stem=ship)
A('9-c', 'Q9(c)', '5D', [43], [25], '5-2', 'differentiation-applications', 'Use calculus to find the value of t when the ships are closest to each other, and find the distance between the ships at your value of t. Give the distance in km, correct to 1 decimal place.', stem=ship + ' t is the time in hours after the ships set sail. The distance between the ships at time t can be given by the function s(t) = (1125t² − 2700t + 8100)^(1/2), where 0 ≤ t ≤ 6.')

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 70, '9': 25}
p.check(marks, 30)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 24–48 of the combined Higher Level scheme (the Paper 2 title page, the Paper 2 scale table on page 26, the summary of mark allocations on page 27, every Paper 2 model solution and marking note on pages 28–43, the Irish-language bonus table on page 44 and the blank back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(24, 49)), [26, 27],
    ['The 2020 Leaving Certificate examinations were cancelled and replaced by Calculated Grades, but the SEC published this paper and its marking scheme. The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 70 marks, Q9 25 marks). Every question is retained.',
     '30 independently marked units, matching the printed summary on scheme page 27 except Q4: the summary lists Q4(a) 10C and Q4(b) 15D, but the scale printed beside each model solution on page 33 is Q4(a) “Scale 15D (0, 4, 7, 11, 15)” and Q4(b) “Scale 10D (0, 3, 5, 8, 10)”, and both marking notes carry low, mid and high partial credit, which only a D scale has. The cards follow the scales printed beside the solutions; Q4 totals 25 marks either way.',
     'Paper 2 bands from the scale table on scheme page 26: 5B 0,2,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10C 0,4,8,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15.',
     'This paper had no authored cards before this review; all 30 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; Q1(b) and Q2(b) keep each printed method’s ladder separately.',
     'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4], 'wording': 'Answer all nine / all six questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [17], 'wording': 'Water flows into one of these cups', 'classification': 'given-context',
      'reason': 'Every cup is identical; “one of these cups” names the single situation, not a choice between prompts.'},
     {'pages': [23], 'wording': 'The difference between any two adjacent numbers is 2 or more', 'classification': 'mathematical-context',
      'reason': 'A condition on every pair of adjacent numbers in the list; not a choice between prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A questions; every published scale unit is retained.') if 'Answer all' in t
        else ('given-context', 'Every cup is the same cone; “one of these cups” names the single situation to calculate, not a choice between prompts.') if 'one of these cups' in t
        else ('mathematical-context', '“Any two adjacent numbers” is a condition on every adjacent pair in the list, not a choice between prompts.') if 'any two adjacent' in t else None)
p.apply(ROWS, '2020 Higher Level Paper 2', expect_added=[c['id'] for c in p.cards])
