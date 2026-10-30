"""2016 OL Paper 2: a new paper — 39 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'
NC = 'No Credit'
G, N, AL = 'Graphical method, ', 'Numerical method, ', 'Algebraic method, '

ROWS = {
 'maths-2016-ol-p2-q1-a-i': [L(LPC, 'Any work of merit.'), L(HPC, 'One correct/consistent entry calculated or inserted in diagram.'),
     L(FC, 'Correctly filled in diagram without work.')],
 'maths-2016-ol-p2-q1-a-ii': [L(SOL, '64/168 or 8/21'), L(LPC, 'Works with 64 or 168 ≠#(E), #(S).')],
 'maths-2016-ol-p2-q1-a-iii': [L(SOL, '(37 + 48)/168 = 50∙59 = 50·6%'), L(LPC, 'Works with 37, 48, 168 (or consistent).'), L(HPC, 'Works to 85. (or consistent)'),
     L(HPC, 'Correct answer without work.')],
 'maths-2016-ol-p2-q1-b': [L(SOL, 'BWV = 1/2 × 1/3 × 1/2 = 1/12'), L(SOL, 'SWV = 1/2 × 1/3 × 1/2 = 1/12'), L(SOL, '= 2/12 or 1/6'),
     L(LPC, 'Any relevant continuation of the tree diagram.'), L(LPC, 'One probability formulated correctly.'), L(HPC, 'Tree diagram fully correct.'),
     L(HPC, 'Probability worked to 2/12 correct but tree diagram incomplete.')],
 'maths-2016-ol-p2-q2-a': [L(SOL, '1/2 (8)(12) sin 30° = 24 cm²'), L(LPC, 'Writes correct relevant formula for area of triangle. e.g. (1/2 ab sinC)'),
     L(MPC, 'One/Two variables correctly substituted into sine formula.'), L(HPC, 'Full correct substitution without calculation.'),
     L(HPC, 'One incorrect or omitted length substitution with area calculated.'), L(HPC, 'Incorrect calculator mode but otherwise correct. (once only)'),
     L(HPC, 'Radian = −47·42 , Gradian = 21·79.'), L(HPC, 'Correct answer without work.'),
     L(NC, 'Answer as 1/2 (8)(12) or 1/2 sin(30° ) without formula.')],
 'maths-2016-ol-p2-q2-b': [L(SOL, '7² = 5² + 3² − 2(3)(5) cos A'), L(SOL, '49 − 9 − 25 = −30 cos A'), L(SOL, 'cos A = −1/2'), L(SOL, 'A = 120°'),
     L(LPC, 'Any work of merit to identify the correct angle required.(Pilot Diagram)'), L(LPC, 'Writes Cosine Rule correctly.'),
     L(MPC, 'Two variables correctly substituted into correct relevant formula.'), L(HPC, 'Fully correct substitution.'),
     L(HPC, 'One incorrect substitution followed by correct calculation.'), L(HPC, 'Calculates a different angle correctly.'), L(HPC, '(21·79°, 38·21°)'),
     L(HPC, 'A correct or consistent answer without work.'), L(HPC, 'Incorrect calculator mode but otherwise correct. (only once)'),
     L(HPC, 'Radian = 2·09, Gradian = 133·33'), L(HPC, 'Correct answer without work.'), L(NC, 'Treats triangle as right angled.')],
 'maths-2016-ol-p2-q3-a': [L(SOL, '(x − 2)² + (y + 3)² = 4²'), L(LPC, 'Identifies correct formula.'), L(LPC, 'Labels any one of (2, –3) or 4 correctly.'),
     L(LPC, 'Works to r² = 4².'), L(HPC, 'Answer as (x − 2)² + (y − 3)² = 4².'), L(HPC, 'Substitutes centre or radius correctly into formula.')],
 'maths-2016-ol-p2-q3-b': [L(LPC, 'Any work of merit e.g. Marks centre on grid.'), L(HPC, 'Any TWO of the three components, centre, radius or drawing correct.')],
 'maths-2016-ol-p2-q3-c': [L(SOL, '(3 − 2)² + (1 + 3)²'), L(SOL, '1 + 16 > 16'), L(ALT, '√((3 − 2)² + (1 + 3)²)'), L(ALT, '√17 > 4'), L(LPC, 'Plots (3,1).'),
     L(LPC, 'Identifies correct relevant formula.'), L(LPC, 'Substitutes (3, 1) into correct/consistent formula .'),
     L(HPC, '(1 + 16) or 17 but no conclusion. (>16)'), L(HPC, '√17 but no conclusion. (>4)')],
 'maths-2016-ol-p2-q3-d': [L(SOL, '8 × 8 = 64 cm²'), L(LPC, 'Drawing on grid. (Any one dimension)'), L(HPC, 'Identifies correct/consistent square.'),
     L(HPC, 'Scale error in dimensions calculated correctly.')],
 'maths-2016-ol-p2-q4-a': [L(SOL, 'm = (0 − 5)/(2 − 4) = 5/2'), L(SOL, 'y − 5 = 5/2 (x − 4)'), L(SOL, '2y − 10 = 5x − 20'), L(SOL, '5x − 2y − 10 = 0'),
     L(LPC, 'Identifies a correct relevant formula.'), L(MPC, 'Slope formula with some substitution.'), L(MPC, 'Equation of line formula with some substitution.'),
     L(MPC, 'Slope correct and stops.'), L(HPC, 'Equation of line formula fully substituted correctly (consistently).'),
     L(NOTE, 'Accept (−5x + 2y + 10 = 0, in any order).')],
 'maths-2016-ol-p2-q4-b': [L(SOL, 'x = 0, y = 4 ⇒ (0, 4)'), L(SOL, 'y = 0, x = 8 ⇒ (8, 0)'), L(LPC, 'x = 0 or y = 0 written.'),
     L(LPC, 'Any work of merit working with line k.'), L(HPC, 'Finds two correct points but no plots or line on graph.')],
 'maths-2016-ol-p2-q4-c': [L(SOL + ', algebraic', 'x + 2y = 8'), L(SOL + ', algebraic', '5x − 2y = 10'), L(SOL + ', algebraic', '6x = 18'), L(SOL + ', algebraic', 'x = 3'),
     L(G + LPC, 'Effort to draw line l.'), L(G + HPC, 'l drawn correctly on grid ( in this part) and point of intersection marked but not written.'),
     L(N + LPC, 'Effort at substituting a value of x into equations of one or both lines.'),
     L(AL + LPC, 'Effort to solve using simultaneous equations.'), L(AL + HPC, 'x and/ or y calculated correctly.'), L(AL + HPC, 'Writes l∩k as (y, x).')],
 'maths-2016-ol-p2-q5-a': [L(SOL, 'Mode = 12'), L(SOL, 'Median = (24+25)÷2=24·5'), L(LPC, 'Any work of merit in finding Mode or Median.'),
     L(HPC, 'Mode or Median correct.'), L(FC, 'Both answers correct without work.')],
 'maths-2016-ol-p2-q5-b': [L(SOL, '=22·6875'), L(SOL, '=22·7'), L(HPC, 'Count correct (16), (21).'), L(FC, 'Correct answer without work.')],
 'maths-2016-ol-p2-q5-c': [L(LPC, 'Any effort at ordering results.'), L(LPC, 'Any correct entry.'), L(HPC, 'Nine correct entries.')],
 'maths-2016-ol-p2-q6-a-i': [L(SOL, '|AC| = 4·5'), L(SOL, '|BC| = 5·4'), L(SOL, 'Sum = 9∙9 cm'), L(LPC, 'One correct line or angle drawn.'),
     L(LPC, 'Any triangle drawn.(Pilot Diagram)'), L(MPC, 'Two correct elements drawn & stops.'), L(HPC, 'Construction correct.'),
     L(HPC, 'Two correct elements and finished correctly/consistently.'), L(HPC, 'Tolerance : ±0·25 cm , ± 2·5°')],
 'maths-2016-ol-p2-q6-b': [L(SOL, 'Answer: Triangle 2'), L(SOL, 'Reason: The sides 6 and 7 are not long enough to reach the side of length 15.'),
     L(NC, 'Nominates Triangle 1.'), L(PC, 'Triangle correct but no reason.'), L(PC, 'Reason correct but no Triangle.'),
     L(PC, 'Any work of merit leading towards correct triangle or reason.')],
 'maths-2016-ol-p2-q6-c': [L(SOL, '(x + 1)² = 5² + x²'), L(SOL, 'x² + 2x + 1 = 25 + x²'), L(SOL, '2x = 24'), L(SOL, 'x = 12'),
     L(LPC, 'Pythagoras with some substitution.'), L(LPC, 'Trial and error to try and find x = 12.'), L(HPC, 'Pythagoras fully substituted correctly.'),
     L(FC, '13² = 12² + 5².'), L(FC, '(5, 12, 13) identified.')],
 'maths-2016-ol-p2-q7-a': [L(SOL, '165 × 10³ × 10⁶'), L(SOL, '= 165 × 10⁹'), L(SOL, '= 1·65 × 10¹¹'), L(PC + ', accept any one of the following', '16·5 × 10¹⁰'),
     L(PC + ', accept any one of the following', '165 × 10⁹'), L(PC + ', accept any one of the following', '10⁹'),
     L(PC + ', accept any one of the following', '10⁶'), L(PC + ', accept any one of the following', '10³'),
     L(PC + ', accept any one of the following', '165 000 000 000'), L(PC + ', accept any one of the following', '1∙65')],
 'maths-2016-ol-p2-q7-b-i': [L(SOL, 'r = 9 m'), L(PC, 'Writes answer as 18/2 or similar.')],
 'maths-2016-ol-p2-q7-b-ii': [L(SOL, 'V = 4/3 πr³'), L(SOL, '4/3 π(9)³'), L(SOL, '= 972π'), L(SOL, '= 3053·63 m³'), L(LPC, 'Identifies correct volume formula.'),
     L(LPC, 'Writes answer from part (b)(i) in this section.'), L(HPC, 'Formula fully substituted correctly (consistently).'),
     L(HPC, 'One error in substitution followed by correct calculation.'), L(HPC, 'Answer as 972π.'), L(NOTE, 'π = 3·14, (3052∙08 m³)'),
     L(NOTE, 'π = 22/7 , (3054∙86 m³)')],
 'maths-2016-ol-p2-q7-c': [L(SOL, 'A = 9 × 4πr²'), L(SOL, '= 9 × 4 × π × (9)²'), L(SOL, '= 2916π'), L(SOL, '= 9160·88'), L(SOL, '= 9161 m²'),
     L(LPC, 'Identifies correct formula.'), L(LPC, 'Identifies radius correctly or consistently (in this part).'), L(LPC, 'Indicates multiplication by 9.'),
     L(HPC, 'Expression fully substituted.'), L(HPC, 'S.A. of one sphere correctly calculated.(1018 m²)'), L(NOTE, 'π = 3·14, (9156 m²)'),
     L(NOTE, 'π = 22/7 , (9165 m²)')],
 'maths-2016-ol-p2-q7-d-i': [L(SOL, 'CSA = 8 × 2 × π × r × ℎ'), L(SOL, '= 8 × 2 × π × 1·65 × 23'), L(SOL, '= 8(75∙9π)'), L(SOL, '= 607·2π'), L(SOL, '= 1907·57'),
     L(SOL, '= 1908 m²'), L(LPC, 'Identifies correct formula.'), L(LPC, 'Identifies r = 1·65, or ℎ = 23.'), L(LPC, 'Indicates multiplication by 8.'),
     L(HPC, 'Expression fully substituted.'), L(HPC, 'Area of one pipe correct.'), L(NOTE, 'π = 3·14, (1907 m²)'), L(NOTE, 'π = 22/7 , (1908 m²)')],
 'maths-2016-ol-p2-q7-d-ii': [L(SOL, '3170/12 = 264·17'), L(SOL, '2 × π × (1·45) × ℎ = 264·17'), L(SOL, 'ℎ = 28·997'), L(SOL, 'ℎ = 29'), L(LPC, '÷ 12 indicated.'),
     L(LPC, 'Identifies correct formula.'), L(LPC, 'Indicates r = 1·45.'), L(HPC, 'Equation fully substituted.')],
 'maths-2016-ol-p2-q7-d-iii': [L(SOL, '1908 + 3170 + 9161 = 14 239'), L(SOL, '14 239 × 70 ='), L(SOL, '€996 730')],
 'maths-2016-ol-p2-q8-a': [L(SOL, '100 − 76 = 24%'), L(PC, '100% − (any relevant percentage).'), L(PC, 'Indicates addition of given percentages.')],
 'maths-2016-ol-p2-q8-b-i': [L(SOL, '1% = 46∙8/13 = 3∙6°'), L(ALT, '360°/100 = 3∙6°'), L(LPC, 'Works with 3·6 or similar.'), L(LPC, 'One correct angle.'),
     L(LPC, 'Three incorrect but consistent angles.'), L(LPC, 'Any use of 360°'), L(HPC, 'Three correct angles.'), L(HPC, 'All incorrect consistent angles.'),
     L(HPC, 'Correct answer without work.')],
 'maths-2016-ol-p2-q8-b-ii': [L(LPC, 'Circle with a sector(s) drawn.'), L(HPC, 'Any 3 sectors drawn correctly. i.e. (with angle and label indicated).'),
     L(HPC, 'All sectors drawn correctly but either angle or label omitted.')],
 'maths-2016-ol-p2-q8-c-i': [L(SOL, 'Total = 3937'), L(LPC, 'Indicates one correct water calculation.'), L(HPC, 'Four correct water calculations.')],
 'maths-2016-ol-p2-q8-c-ii': [L(SOL, '3937 × 52 = 204 724'), L(SOL, '204724/1000 = 204·724'), L(SOL, '204·724×1·85=378·7394'), L(SOL, 'Cost = €378·74'),
     L(LPC, 'Any use of answer to (c)(i).')],
 'maths-2016-ol-p2-q8-c-iii': [L(SOL, '378∙74×1·135=€429·87')],
 'maths-2016-ol-p2-q8-d': [L(SOL, '260/((1·85)(1·135)) =123·8242648'), L(SOL, '=123 824∙3'), L(SOL, 'or = 123 825'),
     L(HPC, 'Formulates correctly with both divisions.'), L(HPC, '123·824 or equivalent and stops.')],
 'maths-2016-ol-p2-q9-a-i': [L(SOL, 'F = ( 4, 1 )'), L(PC, 'One ordinate correct.'), L(PC, 'Answer as (1, 4).')],
 'maths-2016-ol-p2-q9-a-ii': [L(PC, 'Point correct. (No label)'), L(PC, 'Point plotted as (B), but not in the correct position.'), L(PC, 'Plot and label as (4, 6).'),
     L(PC, 'Any plot North of F.'), L(NC, 'All other incorrect points with no labels.')],
 'maths-2016-ol-p2-q9-b': [L(SOL, 'd = √((−2 − 4)² + (7 − 6)²)'), L(SOL, '= √37'), L(SOL, '= 6·08'), L(LPC, 'Writes co-ordinates of B and/or Q.'), L(LPC, 'Any work of merit.'),
     L(HPC, 'Fully correct/consistent substitution without calculation.'), L(HPC, 'One incorrect substitution with correct calculation.'),
     L(HPC, 'One consistent error throughout.')],
 'maths-2016-ol-p2-q9-c': [L(SOL, 'T = (−2, 2)'), L(PC, 'Any work of merit. (Join F to B)'), L(PC, 'One ordinate correct.'), L(PC, 'Answer as ( 2, ‒ 2).')],
 'maths-2016-ol-p2-q9-d': [L(SOL, 'Area = 2 × Area ΔTBF'), L(SOL, '|(6)(−1) − (4)(6)|'), L(SOL, '= 30'), L(LPC, 'Correct relevant formula identified.'),
     L(LPC, 'Triangle co-ordinates identified correctly.'), L(LPC, 'Triangle translated correctly.'), L(LPC, 'Works with 5, 6, or 6·08.'),
     L(MPC, 'Triangle formula fully substituted.'), L(MPC, 'One error in substitution followed by correct calculation of triangle.'),
     L(HPC, 'Area of triangle calculated correctly.'), L(HPC, 'One error in substitution followed by correct calculation of parallelogram.'),
     L(HPC, 'Parallelogram formula fully substituted.'), L(HPC, 'A correct answer without work.')],
 'maths-2016-ol-p2-q9-e': [L(LPC, 'Correct relevant formula.'), L(LPC, 'Work of merit on diagram.'), L(HPC, 'Sine rule fully substituted.'),
     L(HPC, 'Incorrect calculator mode. (once only)'), L(HPC, 'Radian = 0·8 Gradian = 35·9'), L(HPC, 'Correct answer without work.'),
     L(NC, 'Treats as right-angled or isosceles Triangle.')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Filled from scheme_row_figures.py's output once its crops are opened and checked.
SCHEME_ROW_FIGURES = {
    'maths-2016-ol-p2-q1-a-i': 'maths-2016-OL-scheme-p024-i0',
    'maths-2016-ol-p2-q1-a-ii': 'maths-2016-OL-scheme-p024-i1',
    'maths-2016-ol-p2-q1-b': 'maths-2016-OL-scheme-p025-i0',
    'maths-2016-ol-p2-q3-b': 'maths-2016-OL-scheme-p027-i0',
    'maths-2016-ol-p2-q4-b': 'maths-2016-OL-scheme-p029-i0',
    'maths-2016-ol-p2-q4-c': 'maths-2016-OL-scheme-p030-i0',
    'maths-2016-ol-p2-q5-b': 'maths-2016-OL-scheme-p031-i0',
    'maths-2016-ol-p2-q5-c': 'maths-2016-OL-scheme-p031-i1',
    'maths-2016-ol-p2-q6-a-i': 'maths-2016-OL-scheme-p032-i0',
    'maths-2016-ol-p2-q8-b-i': 'maths-2016-OL-scheme-p035-i0',
    'maths-2016-ol-p2-q8-b-ii': 'maths-2016-OL-scheme-p036-i0',
    'maths-2016-ol-p2-q8-c-i': 'maths-2016-OL-scheme-p037-i0',
    'maths-2016-ol-p2-q8-c-ii': 'maths-2016-OL-scheme-p037-i1',
    'maths-2016-ol-p2-q8-d': 'maths-2016-OL-scheme-p038-i0',
    'maths-2016-ol-p2-q9-a-ii': 'maths-2016-OL-scheme-p039-i0',
    'maths-2016-ol-p2-q9-d': 'maths-2016-OL-scheme-p040-i0',
    'maths-2016-ol-p2-q9-e': 'maths-2016-OL-scheme-p040-i1',
}

p = Paper(2016, 'ol', 'p2', {'5A': [0, 5], '5B': [0, 1, 5], '5C': [0, 1, 2, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 2, 4, 10], '15B': [0, 4, 15],
                             '15C': [0, 3, 5, 15], '15D': [0, 2, 4, 8, 15], '20C': [0, 5, 10, 20], '20D': [0, 5, 10, 15, 20]},
          'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
pr, st = 'probability', 'statistics'
venn = ('A survey of 168 people was carried out. Participants were asked whether they owned a cat or a dog. Some of the results are recorded in the '
        'Venn diagram below. Diagram labels: U, Cats, Dogs, 64, 48.')
q1ai = 'Of those surveyed, 19 people did not own either a cat or a dog. Complete the diagram.'
A('1-a-i', 'Q1(a)(i)', '5C', [24], [3], '1-2', pr, q1ai, stem=venn)
A('1-a-ii', 'Q1(a)(ii)', '5C', [24], [3], '1-2', pr, 'A person is chosen at random from those surveyed. What is the probability that the person owned both a cat and a dog?', stem=venn)
A('1-a-iii', 'Q1(a)(iii)', '5C', [24], [3], '1-2', pr + ',' + st, 'What percentage of the people surveyed owned one animal only? Give your answer correct to one decimal place.',
  stem=venn + ' Part (a)(i): ' + q1ai)
A('1-b', 'Q1(b)', '10C', [25], [3], '1-1', pr + ',counting', 'Mandy wants to buy a ticket to the theatre. She can choose a ticket in the Balcony (B) or the Stalls (S). Mandy can go on Monday (M), Wednesday (W) or Friday (F). For an extra charge she can choose a VIP ticket (V) where she will meet the band or she can choose the show only (O). Complete the tree diagram below, and hence or otherwise, find the probability that Mandy chooses a VIP ticket on a Wednesday. You may assume that all choices are equally likely.')
tg = 'trigonometry'
A('2-a', 'Q2(a)', '5D', [26], [4], '2-3', tg + ',area-volume', 'Find the area of the given triangle. Diagram labels: 8 cm, 30°, 12 cm.')
A('2-b', 'Q2(b)', '20D', [26], [4], '2-3', tg, 'A triangle has sides of length 3 cm, 5 cm, and 7 cm. Find the size of the largest angle in the triangle.')
circ, cl = 'co-ordinate-geometry-the-circle', 'co-ordinate-geometry-of-the-line'
cc = 'The circle c has centre (2, –3) and a radius of 4 cm.'
A('3-a', 'Q3(a)', '5C', [27], [5], '2-2', circ, 'Write down the equation of c.', stem=cc)
A('3-b', 'Q3(b)', '5C', [27], [5], '2-2', circ, 'Draw the circle c on the grid opposite. Each unit on the co-ordinate grid is 1 cm.', stem=cc)
A('3-c', 'Q3(c)', '10C', [27], [5], '2-2', circ, 'Verify, using algebra, that the point (3, 1) is outside of c.', stem=cc)
A('3-d', 'Q3(d)', '5C', [28], [5], '2-2', circ + ',area-volume', 'Find the area of the smallest four-sided figure that will fit around the circle c.', stem=cc)
q4a = 'The line l contains the points A(4, 5) and B(2, 0). Find the equation of l. Give your answer in the form ax + by + c = 0 where a, b, and c ∈ ℤ.'
q4b = 'Draw the line k: x + 2y = 8 on the axes below.'
A('4-a', 'Q4(a)', '15D', [29], [6], '2-2', cl, q4a)
A('4-b', 'Q4(b)', '5C', [29], [6], '2-2', cl, q4b)
A('4-c', 'Q4(c)', '5C', [30], [6], '2-2', cl + ',algebra-equations', 'Use a graphic, numeric or algebraic method to find the co-ordinates of l ∩ k.',
  stem='Part (a): ' + q4a + ' Part (b): ' + q4b)
dent = ('The waiting times, in minutes, for 16 patients at a dentist’s surgery are recorded for a particular week (Week 1) on the following stem and '
        'leaf plot. Week 1: 0 | 5 8; 1 | 2 2 2 3; 2 | 0 4 5 7; 3 | 0 1 2 4 4; 4 | 4. Key: 1|3 = 13 minutes.')
A('5-a', 'Q5(a)', '15C', [31], [7], '1-6', st, 'Find the mode and the median of the data.', stem=dent)
A('5-b', 'Q5(b)', '5C', [31], [7], '1-6', st, 'Find the mean waiting time for Week 1, correct to 1 decimal place.', stem=dent)
A('5-c', 'Q5(c)', '5C', [31], [7], '1-6', st, 'The waiting times were recorded again the following week. The results were: 27, 23, 6, 15, 18, 29, 16, 17, 15, 18, 40, 32, 16, 12, 28, 9. Show these results on the plot above (under Week 2), creating a back-to-back stem and leaf plot to display the data.', stem=dent)
geo = 'geometry'
A('6-a-i', 'Q6(a)(i),Q6(a)(ii)', '5D', [32], [8], '2-1', 'geometry-proofs-and-constructions,' + geo, '(i) Construct a triangle ABC, where |AB| = 7 cm, |∠BAC| = 50°, and |AC| = 4·5 cm. (ii) Measure the length of [BC] and hence find the sum of the lengths of the sides [AC] and [BC], correct to one decimal place. |AC| = 4·5 cm; |BC| = _; Sum = _.')
A('6-b', 'Q6(b)', '5B', [32], [8], '2-1', 'geometry-proofs-and-constructions,' + geo, 'State which one of the following triangles can not be constructed. Give a reason to support your answer. Table: Triangle 1: Sides of lengths (cm) 3·2, 2·9, 5·4. Triangle 2: Sides of lengths (cm) 6, 7, 15.')
A('6-c', 'Q6(c)', '15C', [32], [9], '2-1', geo + ',algebra-equations', 'The lengths of the sides of a right-angled triangle are 5, x, and x + 1 as shown. Use the Theorem of Pythagoras to find the value of x.')
av = 'area-volume'
atom = ('The Atomium in Brussels is one of Belgium\'s most famous landmarks. It consists of 9 identical spheres joined by two types of cylindrical pipes.')
sph = atom + ' Part (b): The diameter of each sphere in the Atomium is 18 metres.'
pipes = atom + ' Part (d): Each of the 8 cylindrical pipes extending from the centre sphere has a radius of 1·65 m and a length of 23 m.'
q7di = 'Find the sum of the curved surface areas of all 8 pipes, correct to the nearest m².'
q7dii = ('The other 12 cylindrical pipes connect the outer spheres to each other. Each pipe has a radius of 1·45 m. All 12 pipes are equal in length. '
         'The sum of the curved surface areas of the 12 pipes is 3170 m². Find the length of one pipe. Give your answer correct to the nearest metre.')
q7c = 'Find the combined surface area of all 9 spheres in the Atomium, correct to the nearest m².'
A('7-a', 'Q7(a)', '15B', [33], [10], '3-1', 'number-systems', 'The Atomium is modelled on an iron atom that has been magnified 165 billion times. Given that a billion is a thousand million, write 165 billion in the form a × 10ⁿ, where n ∈ ℤ, and 1 ≤ a < 10.', stem=atom)
A('7-b-i', 'Q7(b)(i)', '5B', [33], [10], '3-4', av, 'Find the radius of each sphere.', stem=sph)
A('7-b-ii', 'Q7(b)(ii)', '5C', [33], [10], '3-4', av, 'Find the volume of each sphere, correct to 2 decimal places.', stem=sph)
A('7-c', 'Q7(c)', '5C', [33], [10], '3-4', av, q7c, stem=sph)
A('7-d-i', 'Q7(d)(i)', '5C', [34], [11], '3-4', av, q7di, stem=pipes)
A('7-d-ii', 'Q7(d)(ii)', '15C', [34], [11], '3-4', av, q7dii, stem=pipes)
A('7-d-iii', 'Q7(d)(iii)', '5A', [34], [11], '3-3', av + ',number-systems', 'The curved surfaces of the 20 pipes and 9 spheres are covered in stainless steel. Stainless steel costs €70 per square metre. Use the areas you have calculated or have been given above to find the approximate cost of the stainless steel required to resurface the Atomium.',
  stem=pipes + ' Part (c): ' + q7c + ' Part (d)(i): ' + q7di + ' Part (d)(ii): ' + q7dii)
water = ('The following table shows some of the data gathered by a company on average water usage in homes. Table: Activity, Percentage used, Angle '
         '(Degrees). WC flushing, 30%, _; Personal Washing – Baths and Taps, 21%, _; Personal Washing – Showers, 12%, _; Clothes Washing, 13%, 46·8°; Other, _, _.')
pie = water + ' Part (b): A pie chart representing the data is to be drawn.'
q8bi = 'The size of the angle representing ‘Clothes Washing’ on the pie chart is 46·8°. Complete the table above to show the remaining angles in the pie chart.'
john = ('John compiled a table showing the amount of water used in his own household over the course of a week. He recorded the number of litres '
        'required for each activity and the number of times each activity was undertaken. The data are shown in the table below. Table: John’s weekly '
        'household water usage. Activity, Water Required per activity, Frequency, Number of litres used. One Bath, 80 litres, 3 baths, 240; One Shower, '
        '125 litres, 20 showers, _; Brushing Teeth with Tap Running, 6 litres per minute, 32 minutes, _; One WC Flush, 6 litres, 60 flushes, _; One Use of '
        'Washing Machine, 45 litres, 8 uses, _; One Use of Dishwasher, 20 litres, 7 uses, _; Washing One Car with a Bucket, 10 litres, 1 wash, _; '
        'Hosepipe, 9 litres per minute, 15 minutes, _. Total number of litres used: _.')
q8cii = 'If water were charged at €1·85 per 1000 litres, find what John’s household would pay for the water used in one year if the household uses the same amount of water each week.'
A('8-a', 'Q8(a)', '5B', [35], [12], '1-6', st, 'Find the percentage used for the ‘Other’ activity, and write it in the table.', stem=water)
A('8-b-i', 'Q8(b)(i)', '5C', [35], [12], '1-6', st, q8bi, stem=pie)
A('8-b-ii', 'Q8(b)(ii)', '5C', [36], [13], '1-6', st, 'Draw a pie chart to represent the data. Label the sector corresponding to each activity and write the size of the angle in each sector.',
  stem=pie + ' Part (b)(i): ' + q8bi)
A('8-c-i', 'Q8(c)(i)', '5C', [37], [14], '3-3', 'number-systems', 'Complete the table to show the number of litres used for the various activities and the total number of litres used in the week.', stem=john)
A('8-c-ii', 'Q8(c)(ii)', '5C', [37], [14], '3-3', 'number-systems,financial-maths', q8cii, stem=john)
A('8-c-iii', 'Q8(c)(iii)', '5A', [38], [15], '3-3', 'financial-maths', 'Find John’s total bill for this water if VAT were to be included at a rate of 13·5%.', stem=john + ' Part (c)(ii): ' + q8cii)
A('8-d', 'Q8(d)', '20C', [38], [15], '3-3', 'financial-maths,number-systems', 'John would like to reduce his water bill to €260 per year. If water were charged at €1·85 plus VAT at 13·5% per 1000 litres, find the number of litres of water he could purchase for €260.')
farm = 'Joe wants to draw a diagram of his farm. He uses axes and co-ordinates to plot his farmhouse at the point F on the diagram below.'
q9aii = 'A barn is 5 units directly North of the farmhouse. Plot the point representing the position of the barn on the diagram. Label this point B.'
q9c = "Joe's tractor is at the point T, where FBQT is a parallelogram. Plot T on the diagram and write the co-ordinates of T in the space below. T = ( , )"
A('9-a-i', 'Q9(a)(i)', '5B', [39], [16], '2-2', cl, 'Write down the co-ordinates of the point F. F = ( , )', stem=farm)
A('9-a-ii', 'Q9(a)(ii)', '5B', [39], [16], '2-2', cl, q9aii, stem=farm)
A('9-b', 'Q9(b)', '5C', [39], [16], '2-2', cl, "Joe's quad bike is marked with the point Q on the diagram. Find the distance from the barn (B) to the quad (Q). Give your answer correct to 2 decimal places.",
  stem=farm + ' Part (a)(ii): ' + q9aii)
A('9-c', 'Q9(c)', '5B', [39], [16], '2-2', cl + ',' + geo, q9c, stem=farm + ' Part (a)(ii): ' + q9aii)
A('9-d', 'Q9(d)', '5D', [40], [17], '2-2', cl + ',' + av, 'Joe wants to plough the land enclosed by the parallelogram FBQT. Find the area of this parallelogram in square units.',
  stem=farm + ' Part (c): ' + q9c)
A('9-e', 'Q9(e)', '20C', [40], [17], '2-3', tg, 'Given that |∠QFB| = 45°, use trigonometric methods to find |∠BQF|. Give your answer in degrees correct to one decimal place.',
  stem=farm + ' Part (c): ' + q9c)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 50, '9': 45}
p.check(marks, 39)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 21–44 of the combined Ordinary Level scheme (the Paper 2 title page 21, the scale table on page 22 (misheaded “Paper 1”), the summary of mark allocations on page 23, every Paper 2 model solution and marking note on pages 24–40, the Irish-language bonus-marks page 41 and the blank back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(21, 45)), [22, 23],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 50 marks, Q9 45 marks). Every question is retained.',
     '39 independently marked units, matching the printed summary of allocations on scheme page 23. Q6(a)(i)+(ii) share one printed scale and are one task.',
     'Paper 2 bands are the ladders printed beside each part, which differ from Paper 1’s: 5A 0,5; 5B 0,1,5; 5C 0,1,2,5; 5D 0,2,3,4,5; 10C 0,2,4,10; 15B 0,4,15; 15C 0,3,5,15; 15D 0,2,4,8,15; 20C 0,5,10,20; 20D 0,5,10,15,20. The scale table on page 22 prints the same ladders.',
     'This paper had no authored cards before this review; all 39 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced. Stacked fractions are written a/b. The Q4(c) bands are labelled by the method the scheme prints them under (graphical, numerical, algebraic).',
     'Seventeen parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because their model solution is a diagram, graph, table, construction or chart, or a band could not be quoted (mixed numbers, an italic Q and an italic h the text layer mangles): Q1(a)(i), Q1(a)(ii), Q1(b), Q3(b), Q4(b), Q4(c), Q5(b), Q5(c), Q6(a)(i)+(ii), Q8(b)(i), Q8(b)(ii), Q8(c)(i), Q8(c)(ii), Q8(d), Q9(a)(ii), Q9(d) and Q9(e).',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. Scheme page references are PDF positions (printed page number + 2); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 10], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [3], 'wording': 'She can choose … hence or otherwise', 'classification': 'mathematical-context',
      'reason': 'The choices are the outcomes of the probability experiment the task models, not a choice between printed prompts; “hence or otherwise” offers alternative methods for the same task.'},
     {'pages': [8], 'wording': 'State which one of the following triangles can not be constructed', 'classification': 'mathematical-context',
      'reason': 'Identifying the impossible triangle is the required task itself; both triangles are part of one prompt.'},
     {'pages': [3], 'wording': 'did not own either a cat or a dog', 'classification': 'mathematical-context',
      'reason': '“Either a cat or a dog” describes the survey data in a required task, not a choice between printed prompts.'},
     {'pages': [10], 'wording': 'one of Belgium\'s most famous landmarks … two types of cylindrical pipes', 'classification': 'mathematical-context',
      'reason': 'Both pipe types are measured in required tasks; there is no printed choice of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('mathematical-context', 'Identifying the impossible triangle is the required task itself; both triangles are part of one prompt.') if 'triangles can' in t
        else ('mathematical-context', 'The choices are the outcomes of the probability experiment the task models, not a choice between printed prompts; “hence or otherwise” offers alternative methods for the same task.') if ('choose' in t or 'otherwise' in t)
        else ('mathematical-context', 'Both pipe types are measured in required tasks; there is no printed choice of prompts.') if ('types of' in t or 'Belgium' in t)
        else ('mathematical-context', '“Either a cat or a dog” describes the survey data in a required task, not a choice between printed prompts.') if 'either a cat or a dog' in t else None)
p.apply(ROWS, '2016 Ordinary Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
