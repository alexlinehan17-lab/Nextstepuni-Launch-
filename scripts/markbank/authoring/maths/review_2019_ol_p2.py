"""2019 OL Paper 2: a new paper — 39 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
FCW = L(FC, 'Correct answer without work')
WOM = L(LPC, 'Work of merit')
PZ = L(ZC, 'Probability > 1, without work')

ROWS = {
 'maths-2019-ol-p2-q1-a': [L(SOL, 'KEY: 1⎮9 = 19 years of age'), L(LPC, 'Attempt at ordering ages'), L(LPC, 'One correct entry'), L(HPC, '15 correct entries'), FCW],
 'maths-2019-ol-p2-q1-b': [L(SOL, '= 50%'), WOM, L(LPC, 'Mention of 14 or 28'), L(LPC, 'Reference to × by 100'), FCW],
 'maths-2019-ol-p2-q1-c-i': [L(SOL, '3/28'), WOM, FCW, PZ],
 'maths-2019-ol-p2-q1-c-ii': [L(SOL, '= 7/28'), WOM, L(HPC, 'Both probabilities calculated correctly'), FCW, PZ],
 'maths-2019-ol-p2-q2-a': [L(SOL, '= (5 − 2)/(8 − 4)'), L(SOL, '= 3/4'), WOM, L(LPC, 'Formula with some correct substitution'), L(HPC, 'Formula substituted correctly'),
     FCW, L('Misreading', 'Finds slope of PR or QR')],
 'maths-2019-ol-p2-q2-b': [L(SOL, 'y − 2 = 3/4 (x − 4)'), L(SOL, '3x − 4y − 4 = 0'), L(LPC, 'Formula with some correct or consistent substitution'),
     L(HPC, 'Formula substituted correctly or consistently'), L(HPC, 'One incorrect substitution followed by correct solution'),
     L(HPC, 'Answer not in the required format'), L(NOTE, 'Accept −3x + 4y + 4 = 0')],
 'maths-2019-ol-p2-q2-c': [L(SOL, '−4/3'), L(MPC, 'Work of merit'), FCW],
 'maths-2019-ol-p2-q2-d': [L(SOL, '(4, 2) (8, 5) (2, 11)'), L(SOL, '(0, 0) (4, 3) (−2, 9)'), L(SOL, '= 1/2 |(4)(9) − (−2)(3)|'), L(SOL, '= 1/2 |36 + 6|'),
     L(SOL, '= 21 square units'), L(LPC, 'Translation of any relevant point to (0,0)'), L(LPC, 'Area of triangle formula with some substitution'),
     L(MPC, 'Area of triangle formula substituted fully with 2 from P,Q, and R'), L(HPC, 'Formula substituted correctly with translated points'),
     L(HPC, 'Area of triangle found from formula substituted fully with 2 from P,Q, R'), L(HPC, 'An incorrect translation applied correctly')],
 'maths-2019-ol-p2-q3-a': [L(SOL, '1 − 0·7 = 0·3'), L(MPC, 'Work of merit'), FCW, PZ],
 'maths-2019-ol-p2-q3-b': [L(SOL, '0·7 × 0·7 = 0·49'), WOM, L(HPC, 'Correct answer indicated but not calculated'), L(HPC, '0·3 × 0·3 = 0·09'), FCW, PZ],
 'maths-2019-ol-p2-q3-c': [L(SOL, '0·7 × 0·7 × 0·3 × 3'), L(SOL, '= 0·147 × 3'), L(SOL, '= 0·441'), L(LPC, 'Work of merit, e.g. List given'),
     L(HPC, 'Correct answer indicated but not calculated'), FCW, PZ],
 'maths-2019-ol-p2-q3-d': [L(SOL, '= 0·0189'), L(LPC, 'Work of merit, e.g. Correct list'), L(HPC, 'Correct answer indicated but not calculated'), FCW, PZ],
 'maths-2019-ol-p2-q4-a': [L(SOL, 'S(−4, 11) → P(2, 3)'), L(SOL, 'R(4, 17) → Q(10, 9)'), WOM, L(LPC, 'Translation identified or indicated on the diagram'),
     L(HPC, 'One co-ordinate correct'), L(HPC, 'An incorrect translation applied correctly'), L(HPC, 'Correct translation applied to an incorrect point'), FCW],
 'maths-2019-ol-p2-q4-b': [L(SOL, 'Mid-point of PR'), L(SOL, '= (3, 10)'), L(LPC, 'Formula with some relevant substitution'), L(LPC, 'Indicates the centre on the diagram'),
     L(HPC, 'Formula substituted correctly'), FCW],
 'maths-2019-ol-p2-q4-c': [L(SOL, 'Radius = 1/2 |RS| or 1/2 |SP|'), L(SOL, '= √64 + 36 = 10'), L(SOL, 'r = 1/2 (10) = 5 units'),
     L(LPC, 'Distance formula with some relevant substitution'), L(HPC, 'Formula substituted correctly'), L(HPC, 'Correct answer without work')],
 'maths-2019-ol-p2-q4-d': [L(SOL, 'Centre = (3,10)'), L(SOL, 'Radius = 5'), WOM, L(HPC, 'One error in substitution and finished correctly'),
     L(FC, 'Correct or consistent answer without work'), L(NOTE, 'Accept work with candidates centre and radius')],
 'maths-2019-ol-p2-q5-a': [L(SOL, '= 9 π'), L(SOL, '= 6·25 π'), L(SOL, '= 8·64 cm2'), L(SOL, '= 6π'), L(SOL, '= 5π'), L(SOL, '= 34·56 cm'),
     L(LPC, 'Area formula with some substitution or Circumference formula with some substitution'),
     L(MPC, 'Area or perimeter of crescent worked correctly'), L(MPC, 'All four formulae substituted correctly'),
     L(HPC, 'Expression for Area and Perimeter substituted correctly with no conclusion'),
     L(HPC, 'Incorrect operator (– or +) in either part but finishes correctly'), L(HPC, 'Answers in terms of π')],
 'maths-2019-ol-p2-q5-b': [L(SOL, '= 196π'), L(SOL, '= 615·7521601'), L(SOL, '= 1·23150432 minutes'), L(SOL, '= 1·23150432 × 60'), L(SOL, '= 73·89025'),
     L(SOL, '= 74 seconds'), WOM, L(LPC, 'Volume formula with some substitution'), L(MPC, 'Formula substituted correctly'), L(HPC, 'Volume found correctly')],
 'maths-2019-ol-p2-q6-a-i': [L(LPC, 'A labelled pilot diagram drawn'), L(LPC, 'One correct length or angle drawn'), L(MPC, 'Any 2 components constructed correctly'),
     L(HPC, 'Any three components constructed correctly')],
 'maths-2019-ol-p2-q6-a-ii': [L(SOL, 'Area = ab sin C'), L(SOL, '= 9(5) sin 65°'), L(SOL, '= 45(0·906307787)'), L(SOL, '= 40·78 cm2'), L(ALT, '= 9[(5) sin 65°]'),
     L(LPC, 'Formula with some substitution'), L(LPC, 'Perpendicular distance between sides measured and used correctly to find area'),
     L(HPC, 'Formula substituted correctly'), L(HPC, 'Incorrect calculator mode (apply once only on paper)')],
 'maths-2019-ol-p2-q6-b': [L(SOL, 'α = 52°'), L(SOL, '2β = 38°'), L(SOL, 'β = 19°'), WOM, L(LPC, 'Pilot diagram'), L(MPC, '|∠YOX| = 104° clearly stated or shown on the diagram'),
     L(MPC, '|∠WYX| = 90° clearly stated or shown on the diagram'), L(HPC, 'One value correct'), L(FC, 'Correct answers without work')],
 'maths-2019-ol-p2-q7-a': [L(SOL, 'Maximum 254 177 175 172'), L(SOL, 'Minimum 54 59 65 48'), L(SOL, 'Range 200 118 110 124'), WOM, L(HPC, 'Four correct entries')],
 'maths-2019-ol-p2-q7-b': [L(SOL, '48 62 77 86 95 104 111 116 125 136 137 150 172'), L(SOL, 'Median = 111'), WOM, L(LPC, 'Effort at ordering data'),
     L(LPC, 'Median taken from an unordered list'), L(HPC, 'All data ordered'), L(HPC, 'Correct median without work'),
     L(HPC, 'Correct median from an incorrect food category'), L(HPC, 'Correct median from a decreasing list')],
 'maths-2019-ol-p2-q7-c-i': [L(SOL, 'Sum = 1456'), L(SOL, 'Mean = €112'), WOM, L(HPC, 'Formula substituted correctly but not evaluated'),
     L(HPC, 'Calculates the mean of an incorrect food category'), FCW],
 'maths-2019-ol-p2-q7-c-ii': [L(SOL, 'S. D. = € 51')],
 'maths-2019-ol-p2-q7-c-iii': [L(SOL, '112 + 51 = 163'), L(SOL, '112 − 51 = 61'), L(SOL, '[61,163]'), L(SOL, 'Macedonia, Poland and Switzerland'), WOM,
     L(HPC, 'Range found')],
 'maths-2019-ol-p2-q7-d': [L(SOL, 'Poland 18·36 18·56 12·35 14·26 63·53'), L(SOL, '31·32/108 × 64 = 18·56'), L(SOL, '24·32/128 × 65 = 12·35'),
     L(SOL, '31·28/136 × 62 = 14·26'), L(LPC, 'Any work of merit'), L(HPC, 'Two food categories filled correctly'), L(HPC, 'Correct answers without work')],
 'maths-2019-ol-p2-q8-a-i': [L(SOL, 'V = 36π'), WOM, L(HPC, 'Formula substituted correctly'), FCW],
 'maths-2019-ol-p2-q8-a-ii': [L(SOL, 'ℎ = 36π/25π'), L(SOL, 'ℎ = 36/25 cm or 1·44 cm'), WOM, L(LPC, 'Volume formula with some substitution'),
     L(HPC, 'Formula substituted correctly and equation formed'), L(HPC, 'One error in substitution in the equation and finishes correctly')],
 'maths-2019-ol-p2-q8-a-iii': [L(SOL, 'C.S.A = 2πrℎ'), L(SOL, '= 2π(5)(18)'), L(SOL, '= 180π'), L(SOL, 'Material left over = 35 × 20 − [180π]'), L(SOL, '= 700 − 565·49'),
     L(SOL, '= 134·51'), WOM, L(HPC, '2 area formulae substituted correctly and stops'),
     L(HPC, 'One error in substitution in getting the area and finishes correctly')],
 'maths-2019-ol-p2-q8-b-i': [L(SOL, '= 3·5355'), L(SOL, '= 3·54%'), L(LPC, 'Sets up work as √800'), L(HPC, 'Formula substituted correctly'),
     L(HPC, 'Answer as 0·035355 without work'), FCW, L(NOTE, 'Special Case Without Work Award 3·5355% Full Credit –1')],
 'maths-2019-ol-p2-q8-b-ii': [L(SOL, 'p̂ = 350/800 = 43·75%'), L(SOL, '43·75 − 3·54 < p < 43·75 + 3·54'), L(SOL, '40·21% < p < 47·29%'), WOM,
     L(HPC, 'One boundary formed:'), L(HPC, '(43·75 − 3·54 or 43·75 + 3·54)'), L(HPC, 'Correct answer without work'), L(HPC, 'Use of version of formula from HL'),
     L(HPC, 'Answer in decimal form')],
 'maths-2019-ol-p2-q8-b-iii': [L(SOL, '= the level of support is 50%'), L(SOL, '= the level of support is not 50%'), L(SOL, '50% ∉ [40·21%, 47·29%]'),
     L(SOL, '50% is not within the 95% CI so there is not enough evidence to support the claim.'), L(LPC, 'Null hypothesis stated'), L(LPC, 'C. I. written'),
     L(HPC, 'Conclusion OK but reason incorrect or omitted'), L(HPC, '50% ∉ [40·21%, 47·29%] with conclusion incorrect or omitted')],
 'maths-2019-ol-p2-q9-a': [L(SOL, '|QR| = 120 sin 30°'), L(SOL, '|QR| = 60 km'), WOM,
     L(LPC, 'Correct trigonometric ratio or relevant formula with some substitution'), L(HPC, 'Formula substituted correctly'),
     L(HPC, 'One incorrect substitution and finished correctly'), L(HPC, 'Incorrect calculator mode (apply once only on paper)')],
 'maths-2019-ol-p2-q9-b': [L(SOL, '= 10000 − 3600'), L(SOL, '|QS| = √6400'), L(SOL, '|QS| = 80 km'), WOM, L(LPC, 'Pythagoras formulated with some substitution'),
     L(HPC, 'Pythagoras substituted correctly'), L(HPC, 'Answer as √6400')],
 'maths-2019-ol-p2-q9-c': [L(SOL, '|PQ| = 103·92304'), L(SOL, '|PS| = |PQ| − |QS|'), L(SOL, '|PS| = 103·92 − 80'), L(SOL, '|PS| = 23·92'), L(SOL, '|PS| ≈ 24 km'),
     WOM, L(LPC, 'Pythagoras formulated with some substitution'), L(LPC, '|PS| = |PQ| − 80'),
     L(HPC, 'Pythagoras substituted correctly and |PQ| evaluated correctly or consistently')],
 'maths-2019-ol-p2-q9-d-i': [L(SOL, '|TS| = 2|QS|'), L(SOL, '= 2 × 80'), L(SOL, '= 160'), L(SOL, '20000 cos θ = 10000 + 10000 − 25600'), L(SOL, 'θ = 106·26'), WOM, L(LPC, 'Cosine formula with some substitution'),
     L(MPC, 'Two variables correctly substituted into the Cosine formula'), L(HPC, 'Formula substituted correctly'),
     L(HPC, 'One incorrect substitution followed by correct calculation'), L(HPC, 'Incorrect calculator mode (apply once in paper)'),
     L('No Credit', 'Treats triangle as right angled')],
 'maths-2019-ol-p2-q9-d-ii': [L(SOL, '= 185·0049'), L(SOL, 'Difference = 185 − 160'), L(SOL, '= 25 km'), WOM,
     L(LPC, 'Arc/circumference formula with some substitution'), L(HPC, 'Calculates arc length = 185')],
 'maths-2019-ol-p2-q9-d-iii': [L(SOL, '= 9250·245'), L(SOL, '= 370'), WOM, L(LPC, 'Formula with some substitution'),
     L(MPC, 'Formula substituted correctly'), L(HPC, 'Area of sector evaluated correctly'), L(HPC, 'One error in substitution and finishes correctly or consistently')],
}
# Parts whose printed scheme content cannot be lifted as text (ASCII-flattened
# sub/superscripts, filtered stacked-fraction denominators) carry the SEC's own
# print of their scheme row -- model solution and every credit band -- shown
# only after the reveal. Crops: scheme_row_figures.py; ids are its output.
SCHEME_ROW_FIGURES = {
    'maths-2019-ol-p2-q1-a': 'maths-2019-OL-scheme-p028-i0',
    'maths-2019-ol-p2-q1-b': 'maths-2019-OL-scheme-p028-i1',
    'maths-2019-ol-p2-q1-c-i': 'maths-2019-OL-scheme-p029-i0',
    'maths-2019-ol-p2-q1-c-ii': 'maths-2019-OL-scheme-p029-i1',
    'maths-2019-ol-p2-q2-a': 'maths-2019-OL-scheme-p030-i0',
    'maths-2019-ol-p2-q2-b': 'maths-2019-OL-scheme-p030-i1',
    'maths-2019-ol-p2-q2-d': 'maths-2019-OL-scheme-p031-i0',
    'maths-2019-ol-p2-q3-d': 'maths-2019-OL-scheme-p033-i0',
    'maths-2019-ol-p2-q4-b': 'maths-2019-OL-scheme-p034-i0',
    'maths-2019-ol-p2-q4-c': 'maths-2019-OL-scheme-p034-i1',
    'maths-2019-ol-p2-q4-d': 'maths-2019-OL-scheme-p035-i0',
    'maths-2019-ol-p2-q5-a': 'maths-2019-OL-scheme-p036-i0',
    'maths-2019-ol-p2-q5-b': 'maths-2019-OL-scheme-p036-i1',
    'maths-2019-ol-p2-q7-c-i': 'maths-2019-OL-scheme-p039-i0',
    'maths-2019-ol-p2-q8-a-i': 'maths-2019-OL-scheme-p041-i0',
    'maths-2019-ol-p2-q8-a-ii': 'maths-2019-OL-scheme-p041-i1',
    'maths-2019-ol-p2-q8-a-iii': 'maths-2019-OL-scheme-p041-i2',
    'maths-2019-ol-p2-q8-b-i': 'maths-2019-OL-scheme-p042-i0',
    'maths-2019-ol-p2-q8-b-ii': 'maths-2019-OL-scheme-p042-i1',
    'maths-2019-ol-p2-q8-b-iii': 'maths-2019-OL-scheme-p042-i2',
    'maths-2019-ol-p2-q9-a': 'maths-2019-OL-scheme-p043-i0',
    'maths-2019-ol-p2-q9-b': 'maths-2019-OL-scheme-p043-i1',
    'maths-2019-ol-p2-q9-c': 'maths-2019-OL-scheme-p043-i2',
    'maths-2019-ol-p2-q9-d-i': 'maths-2019-OL-scheme-p044-i0',
    'maths-2019-ol-p2-q9-d-ii': 'maths-2019-OL-scheme-p044-i1',
    'maths-2019-ol-p2-q9-d-iii': 'maths-2019-OL-scheme-p045-i0',
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2019, 'ol', 'p2', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 4, 6, 10],
                             '10D': [0, 3, 5, 8, 10], '15C': [0, 5, 9, 15], '15D': [0, 4, 7, 11, 15]},
          'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
ages = 'A business has 28 employees. Their ages, in years, are given below: 32, 41, 57, 64, 19, 21, 35, 18, 43, 54, 63, 65, 33, 22, 39, 58, 18, 42, 20, 34, 21, 49, 33, 55, 34, 57, 43, 63.'
st = 'statistics'
A('1-a', 'Q1(a)', '10C', [28], [4], '1-6', st, 'Complete the stem-and-leaf diagram, showing the ages of all 28 employees. (Stems 1 to 6; KEY: 1|9 = 19 years of age.)', stem=ages)
A('1-b', 'Q1(b)', '5C', [28], [4], '1-6', st, 'Find the percentage of employees who are older than 40 years of age.', stem=ages)
agp = ages + ' One employee is chosen at random on a day when all employees are present at work.'
A('1-c-i', 'Q1(c)(i)', '5C', [29], [5], '1-2', 'probability', 'Find the probability that the employee is a teenager (<20 years of age).', stem=agp)
A('1-c-ii', 'Q1(c)(ii)', '5C', [29], [5], '1-2', 'probability', 'Find the probability that the employee chosen is a person in their thirties whose age is even or a person in their forties whose age is odd.', stem=agp)
pqr = 'The diagram shows the line PQ and the line QR. The co-ordinates of the points are P(4, 2), Q(8, 5) and R(2, 11).'
cl = 'co-ordinate-geometry-of-the-line'
A('2-a', 'Q2(a)', '10C', [30], [6], '2-2', cl, 'Find the slope of PQ.', stem=pqr)
A('2-b', 'Q2(b)', '5C', [30], [6], '2-2', cl, 'Find the equation of the line PQ. Give your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.', stem=pqr)
A('2-c', 'Q2(c)', '5B', [30], [7], '2-2', cl, 'Write down the slope of any line perpendicular to PQ.', stem=pqr)
A('2-d', 'Q2(d)', '5D', [31], [7], '2-2', cl + ',area-volume', 'Find the area of the triangle PQR.', stem=pqr)
blue = 'In a population, the probability that a person has blue eyes is 0·7.'
pb = 'probability'
A('3-a', 'Q3(a)', '10B', [32], [8], '1-2', pb, 'One person is chosen at random from the population. What is the probability that this person does not have blue eyes?', stem=blue)
A('3-b', 'Q3(b)', '5C', [32], [8], '1-2', pb, 'Two people are chosen at random. What is the probability that both have blue eyes?', stem=blue)
A('3-c', 'Q3(c)', '5C', [32], [8], '1-2', pb, 'Three people are chosen at random. What is the probability that exactly two of them have blue eyes?', stem=blue)
A('3-d', 'Q3(d)', '5C', [33], [9], '1-2', pb, 'Four people are chosen at random, one after another. What is the probability that the fourth person of the four chosen is the only one to have blue eyes?', stem=blue)
sq = 'The circle c is enclosed in the square PQRS and touches all four sides, as shown in the diagram. The co-ordinates of three of the vertices are P(2, 3), R(4, 17), and S(−4, 11).'
cc = 'co-ordinate-geometry-the-circle'
A('4-a', 'Q4(a)', '5C', [34], [10], '2-2', cl, 'Find the co-ordinates of Q.', stem=sq)
A('4-b', 'Q4(b)', '5C', [34], [10], '2-2', cl + ',' + cc, 'Find the co-ordinates of the centre of c.', stem=sq)
A('4-c', 'Q4(c)', '5C', [34], [11], '2-2', cl + ',' + cc, 'Find the length of the radius of c.', stem=sq)
A('4-d', 'Q4(d)', '10C', [35], [11], '2-2', cc, 'Find the equation of circle c.', stem=sq)
A('5-a', 'Q5(a)', '10D', [36], [12], '3-4', 'area-volume', 'The crescent, shown in the shaded part of the diagram, was created by removing a disc of radius 2·5 cm from a disc of radius 3 cm. Find the area and the perimeter of the crescent. Give each answer correct to two decimal places.')
A('5-b', 'Q5(b)', '15D', [36], [13], '3-4', 'area-volume', 'An empty inverted cone of vertical height 12 cm and radius 7 cm is filled with water from a pipe. The water flows from the pipe at a steady rate of 0·5 litres per minute. Find the time it takes to fill the cone. Give your answer correct to the nearest second.')
pg = 'Construct the parallelogram PQRS, where |PQ| = 9 cm, |PS| = 5 cm and |∠SPQ| = 65°. The point P has been marked in for you. Show all your construction lines, arcs and labels clearly.'
A('6-a-i', 'Q6(a)(i)', '15D', [37], [14], '2-1', 'geometry-proofs-and-constructions', pg, extra={'sourceMaterial': {'measurementRequired': True}} if False else None)
A('6-a-ii', 'Q6(a)(ii)', '5C', [37], [14], '2-3', 'trigonometry,area-volume', 'Find the area of the parallelogram PQRS. Give your answer correct to 2 decimal places.', stem='Part (a)(i): ' + pg)
A('6-b', 'Q6(b)', '5D', [37], [15], '2-1', 'geometry', 'In the diagram O is the centre of the circle s. Find the value of α and the value of β.')
food = 'Table A shows the price index for thirteen countries in four food categories for the year 2015. (Source: Central Statistics Office.) It shows, for example, that if you paid €132 for meat in Austria, then the same quantity of similar meat would cost you €117 in Germany, €106 in Ireland, €63 in Lithuania and so on. The description is the same for the other food categories. Table A (€) — Country: Meat, Fish, Milk Cheese and Eggs, Fruits Vegetables and Potatoes. Austria: 132, 125, 105, 125. Germany: 117, 109, 91, 111. Ireland: 106, 108, 128, 136. Lithuania: 63, 73, 85, 77. Macedonia: 56, 59, 71, 48. Netherlands: 111, 99, 93, 104. Norway: 157, 117, 175, 150. Poland: 54, 64, 65, 62. Spain: 85, 89, 96, 95. Sweden: 131, 115, 116, 137. Switzerland: 254, 177, 148, 172. Turkey: 78, 105, 122, 86. United Kingdom: 112, 105, 118, 116.'
A('7-a', 'Q7(a)', '10C', [38], [16], '1-6', st, 'Complete Table B below, to show the maximum value, the minimum value and the range of the data for the four food categories. Table B (€) — Meat: Maximum 254, Minimum 54, Range 200; Fish, Milk Cheese and Eggs, and Fruits Vegetables and Potatoes: to be completed.', stem=food)
A('7-b', 'Q7(b)', '10C', [38], [17], '1-6', st, 'Write the data for the Fruits, Vegetables and Potatoes category in increasing order and hence find the median for that food category.', stem=food)
A('7-c-i', 'Q7(c)(i)', '15C', [39], [17], '1-6', st, 'Find the mean of the data in the Meat category.', stem=food)
A('7-c-ii', 'Q7(c)(ii)', '5A', [39], [18], '1-6', st, 'Use your calculator to find the standard deviation for the data in the Meat category. Give your answer correct to the nearest whole number.', stem=food)
A('7-c-iii', 'Q7(c)(iii)', '5C', [39], [18], '1-6', st, 'List all the countries in the Meat category that are not within one standard deviation of the mean.', stem=food)
A('7-d', 'Q7(d)', '5C', [40], [19], '1-6', st + ',number-systems', 'A customer in Ireland buys some meat, fish, milk, cheese, eggs, fruits, vegetables and potatoes as detailed in Table C. A customer in Poland buys the same items in the same quantities. Complete Table C. Table C (€) — Country: Meat, Fish, Milk Cheese and Eggs, Fruits Vegetables and Potatoes, Total Cost. Ireland: 36·04, 31·32, 24·32, 31·28, 122·96. Poland: 18·36, _, _, _, _.', stem=food)
sph = 'A solid sphere of radius 3 cm is placed inside a cylinder and then water is poured into the cylinder until it is full, as shown in the diagram.'
av = 'area-volume'
A('8-a-i', 'Q8(a)(i)', '10C', [41], [20], '3-4', av, 'Find the volume of the sphere, in terms of π.', stem=sph)
A('8-a-ii', 'Q8(a)(ii)', '5C', [41], [20], '3-4', av, 'The sphere is now removed. The internal radius of the cylinder is 5 cm. Find the drop, in cm, in the height of the water.', stem=sph)
A('8-a-iii', 'Q8(a)(iii)', '10C', [41], [20], '3-4', av, 'The cylinder has a height of 18 cm. The curved surface of the cylinder is cut from a rectangular piece of metal measuring 35 cm by 20 cm, as shown. Find how much metal will be left over when the curved surface of the cylinder is cut out. Give your answer correct to 1 decimal place.', stem=sph + ' The internal radius of the cylinder is 5 cm.')
dst = 'In September 2018 a European Commission report stated that it is considering a proposal to abolish daylight saving time. This would mean that the clocks would not go forward one hour in March and then not go back one hour the following October. A Transition Year class carried out a survey to find out local people’s views on the proposal.'
A('8-b-i', 'Q8(b)(i)', '10C', [42], [21], '1-7', st, 'The class surveyed a random sample of 800 people in the local area. Find the margin of error of the survey. Give your answer as a percentage, correct to 2 decimal places.', stem=dst)
dst2 = dst + ' The class surveyed a random sample of 800 people in the local area.'
A('8-b-ii', 'Q8(b)(ii)', '5C', [42], [21], '1-7', st, 'In the survey 350 people said they supported the EU proposal to abolish daylight saving time. Use your answer to part (b)(i) above to create a 95% confidence interval for the percentage of the population who supported the EU proposal.', stem=dst2)
A('8-b-iii', 'Q8(b)(iii)', '5C', [42], [21], '1-7', st, 'A local newspaper had reported that 50% of people in the area supported the EU proposal. Use your answer to part (b)(ii) above to conduct a hypothesis test, at the 5% level of significance, to test the newspaper’s claim. Clearly state your conclusion in the context of the question and give a reason for your conclusion.', stem=dst2 + ' In the survey 350 people said they supported the EU proposal to abolish daylight saving time.')
rad = 'R is a radar station located 120 km north of a port P. The circle c, centred at R and with radius 100 km shows the detection range of the radar. When a ship enters the circle it will be detected by the radar station at R. Figure 1 shows a ship leaving port P and sailing in the direction north 30° east. The ship enters the circle c at S and exits at T. At Q, the ship is closest to R and |∠PQR| = 90°.'
tg = 'trigonometry'
A('9-a', 'Q9(a)', '15C', [43], [22], '2-3', tg, 'The triangle PQR taken from Figure 1 is shown in Figure 2. Find |QR|, the length of [QR].', stem=rad)
A('9-b', 'Q9(b)', '10C', [43], [22], '2-3', tg, 'The triangle QRS taken from Figure 1 is shown in Figure 3. Use your answer from part (a) to find |QS|.', stem=rad)
A('9-c', 'Q9(c)', '10C', [43], [23], '2-3', tg, 'Find |PS|. Give your answer correct to the nearest km.', stem=rad)
A('9-d-i', 'Q9(d)(i)', '5D', [44], [23], '2-3', tg, 'Consider the triangle RST. Use the Cosine Rule to find an expression for cos θ, where θ is the measure of the angle TRS. Hence show that θ = 106°, correct to the nearest degree.', stem=rad)
rad106 = rad + ' In the triangle RST, θ = |∠TRS| = 106°.'
A('9-d-ii', 'Q9(d)(ii)', '10C', [44], [24], '3-4', av + ',' + tg, 'John sails directly from S to T. Mary sails from S to T along the minor arc ST. Find the difference between the distance that John sails and the distance that Mary sails. Give your answer correct to the nearest km.', stem=rad106)
A('9-d-iii', 'Q9(d)(iii)', '5D', [45], [24], '3-4', av, 'The sea in this region is estimated to have an average of 1 ship per 25 square kilometres at any time. Use this estimate to find the number of ships in the sector RST. Give your answer correct to the nearest whole number.', stem=rad106)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 50, '8': 45, '9': 55}
p.check(marks, 39)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 25–48 of the combined Ordinary Level scheme (the Paper 2 title page 25, the Paper 2 scale table on page 26, the summary of mark allocations on page 27, every Paper 2 model solution and marking note on pages 28–45, and the blank pages 46–48). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(25, 49)), [26, 27],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 50 marks, Q8 45 marks, Q9 55 marks). Every question is retained.',
     '39 independently marked units, matching the printed summary on scheme page 27.',
     'Paper 2 bands from the scale table on scheme page 26, which differ from Paper 1’s: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,4,6,10; 10D 0,3,5,8,10; 15C 0,5,9,15; 15D 0,4,7,11,15. Each part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 39 units are new. Marking points are lifted line by line from the scheme and labelled with the part of the scheme they come from. As on Paper 1, the scheme’s text layer encodes subscripts and superscripts as ASCII (squares extract as “8”), and the provenance reader cannot rejoin a stacked fraction’s denominator, so marking points that depend on either are not retyped as text. Instead the 26 parts affected (Q1(a), Q1(b), Q1(c)(i), Q1(c)(ii), Q2(a), Q2(b), Q2(d), Q3(d), Q4(b), Q4(c), Q4(d), Q5(a), Q5(b), Q7(c)(i), Q8(a)(i)–(iii), Q8(b)(i)–(iii), Q9(a), Q9(b), Q9(c), Q9(d)(i)–(iii)) carry a crop of their printed scheme row — model solution and every credit band the scheme prints — shown only after the reveal. Q6(a)(i) is a construction whose model solution is a drawing; its card carries the printed credit criteria.',
     'Data tables in prompts carry the printed values, with blanks for the cells the candidate fills.',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t else None)
p.apply(ROWS, '2019 Ordinary Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
