import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from solution_lib import Paper

HL_P2 = {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5],
         '10C': [0, 3, 7, 10], '10D': [0, 2, 5, 8, 10], '15D': [0, 3, 8, 12, 15]}
p = Paper(
    year=2026, level='higher', paper_key='p2', paper_file='LC003ALP200EV.pdf', scheme_file='LC003ALP000EV.pdf',
    prefix='maths-2026-hl-p2', ref='2026 HL Paper 2', scales=HL_P2, reviewed_at='2026-10-11',
    general_notes=[3, 4, 44], scheme_pages=[3, 4] + list(range(44, 81)),
    printed_marks={**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}},
    review_method='Independent visual reading of all 32 question-paper pages and PDF pages 3–4 and 44–80 of the combined Higher Level scheme (general notes, the Paper 2 scale table on page 44, every Paper 2 model solution and marking note, and the blank closing pages). Each task boundary is the published scale, not a parser count.',
    source_notes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained; no combined multi-question cards.',
        '41 independently marked units. Shared scales keep their parts together: Q2(b)(i)–(ii) 15D, Q5(b)(i)–(ii) 10D, Q5(b)(iii)–(iv) 15D, Q8(b)(i)–(iii) 5C and Q10(b)(i)–(ii) 5C.',
        'Paper 2 bands from scheme page 44: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10C 0,3,7,10; 10D 0,2,5,8,10; 15D 0,3,8,12,15. Q2(c) and Q10(c)(ii) are 5A (all or nothing).',
        'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. All page references are PDF positions.',
        'Q3(a) is a construction marked with a ±3 mm tolerance on the printed triangle, so it carries the calibrated measuring ruler.',
        'Diagrams (stem-and-leaf graph, pie-chart circle, triangle t and line l, cuboid, circle sketch, cos² graph, unit circle, triangles, scatter graph, belt drive, net, lawn region) are read from the attached original question pages; prompts quote the paper’s own wording.',
        'Scheme text layers set some letters in characters that do not match plain text (for example h as ℎ, or doubled letters in |AD|), so card rows quote only notes whose text layer matches the printed scheme; the scheme reader shows the full published notes.',
    ],
    out_name='2026-higher-p2.json', atlas_prefix='mathematics-higher-', section_of=lambda q: 'A' if q <= 6 else 'B',
)
A = p.add
sales = 'A shop records the number of sales that it makes each hour over a period of time. Some of the results are shown in the stem-and-leaf graph below: 5 | 4 4 5 5 7 7 8; 6 | 2 3 3 4 5 7 9 9; 7 | 0 3 7; 8 | 0 5. Key: 5|7 = 57 sales.'
A('1-a', 'Q1(a)', '10D', [45], [4], '1-6', 'statistics-descriptive-statistics',
  'Work out the following statistics for the data above: the median, the range and the interquartile range. (The table already gives n, the number of observations, as 20.)',
  ['so = 63·5', 'Range: 85 − 54 = 31', 'Then IQR = 69·5 − 57 = 12·5', 'Uses 5th, 10th, 15th value, otherwise correct'], stem=sales)
A('1-b', 'Q1(b)', '10D', [46], [4, 5], '1-6', 'statistics-descriptive-statistics',
  'Draw a pie chart to represent this data. Use the classes 50 − 59, 60 − 69, 70 − 79, and 80 − 89. Label each sector and the size of each angle clearly. Show all of your calculations.',
  ['Tolerance of ±3°', 'Note: Only need to calculate 3 angles.', 'Calculates remaining 2 angles',
   '2 angles calculated correctly, and 2 sectors correctly drawn'], stem=sales)
A('1-c', 'Q1(c)', '10C', [46], [4, 5], '1-6', 'statistics-descriptive-statistics,algebra-solving-equations',
  'The shop records the number of sales each hour for a further k hours. Each of these k hours had sales in the range 70 − 79. When the sales for these k hours were combined with the sales in the stem-and-leaf graph on the previous page, 32% of the total number of hours had sales in the range 70 − 79. Work out the value of k.',
  ['and k = 5', 'Sets up equation in k (1st line, or equivalent)', 'Note: Correct value of k verified, award full marks'], stem=sales)
phones = 'A company makes mobile phones.'
A('2-a', 'Q2(a)', '10C', [47], [6], '1-7', 'statistics-inferential-statistics',
  'The company carries out a survey on a random sample of n of their customers, where n ∈ ℕ. Based on this survey, the margin of error for the population proportion, 1/√n, is 3·4%, correct to 1 decimal place. Find one possible value of n.',
  ['Note: n = 841 to n = 891 inclusive will give correct margin of error.', 'Accept a correct value of n, fully verified',
   'Note: can use margin of error between 0·0335 and 0·0345.'], stem=phones)
A('2-b-i-ii', 'Q2(b)(i),Q2(b)(ii)', '15D', [48], [6, 7], '1-7', 'statistics-inferential-statistics',
  '(i) Use this information to find a 95% confidence interval for the population mean time. Give each value in your answer in minutes, correct to 1 decimal place. (ii) The mean time taken to charge the old model mobile phone from empty to fully charged is 44 minutes. The company says that the mean time taken to charge the new model mobile phone is the same as this. Using your answer to part (b)(i), or otherwise, carry out a hypothesis test at the 5% level of significance to test the company’s claim. The null hypothesis is given: The mean time taken to fully charge the new model mobile phone is 44 minutes. State clearly the alternative hypothesis, your conclusion, and the reason for your conclusion. If necessary, provide calculations.',
  ['= (44·7, 46·1)', 'Correct alternative hypothesis', 'Alternative: “The mean time taken to charge is not 44 minutes”',
   'Reason: “44 is outside the 95% C.I.”'],
  stem=phones + ' The company makes two types of mobile phones: an old model and a new model. A random sample of 80 of the company’s new mobile phones is tested, to see how long it takes to charge them from empty to fully charged. The mean time for this sample is 45·4 minutes, with a standard deviation of 3·1 minutes.')
A('2-c', 'Q2(c)', '5A', [49], [7], '1-7', 'statistics-inferential-statistics',
  'In a different survey, two hypothesis tests were carried out at the 5% level of significance. The p-value for the first test was 0·046. The p-value for the second test was 0·0002. Write a sentence to explain what the difference in the sizes of these p-values means about the conclusions to these two tests. You do not need to carry out any calculations.',
  ['We would have more confidence in the conclusion of the second test', 'The conclusion of the second test is more reliable'], stem=phones)
A('3-a', 'Q3(a)', '10C', [50], [8], '2-4', 'geometry-constructions-proofs',
  'The diagram below shows the triangle t and the line l. Construct the image of the triangle t under axial symmetry in l. Show all construction lines clearly. If you use measurements, write them in an appropriate place on your solution.',
  ['Tolerance: ±3 mm', 'Correct image (triangle) drawn, but no construction lines or measurements',
   'Two vertices reflected correctly, with the required construction lines / measurements'], extra={'measurementRequired': True})
A('3-b', 'Q3(b)', '10D', [50], [8], '3-4', 'area-volume',
  'A right circular cone has a height of h cm and a radius of h/4 cm, where h ∈ ℕ is a constant. The volume of the cone is 36 000π cm³. Work out the value of h.',
  ['and ℎ = ∛1 728 000 = 120', 'Deals with squaring and power of ℎ',
   'Note: there must be a ℎ² or higher power of ℎ in order for Step 3 to be considered correct'])
A('3-c', 'Q3(c)', '10D', [51], [9], '3-4', 'area-volume',
  'A cuboid has sides of length 24 cm, 36 cm, and 60 cm. This cuboid lies inside a sphere, so that the eight vertices (corners) of the cuboid lie on the surface of the sphere. Work out the volume of the sphere. Give your answer in the form a√38 π cm³, where a ∈ ℕ. It might be helpful to find the length of the internal diagonal of the cuboid.',
  ['= 10 944√38 π [cm³]', 'Note: If Pythagoras is not used, award Low Partial Credit at most.', 'Volume formula fully substituted'])
A('4-a', 'Q4(a)', '10C', [52], [10], '2-2', 'co-ordinate-geometry-of-the-line',
  'The lines l and k have the following equations: l: 3x − 2y = 0; k: y = −(3/2)x + 7. Are the lines l and k perpendicular? Justify your answer using calculations.',
  ['Answer: No', 'Work of merit in justification, for example, finds one or two slopes'])
A('4-b', 'Q4(b)', '10D', [52], [10], '2-2', 'co-ordinate-geometry-of-the-line,algebra-inequalities',
  'A line has equation y = mx + 8, where m ∈ ℝ is a constant. Find the ranges of values of m for which this line does not intersect the line segment from (3, 7) to (3, 11). It may be helpful to draw a diagram.',
  ['Finds one relevant slope', 'Finds second relevant slope', 'Finds inequalities in correct direction'])
A('4-c', 'Q4(c)', '10D', [53], [11], '2-2', 'co-ordinate-geometry-of-the-line',
  'P is the point (1, 0). The perpendicular distance from P to the line ax + y − 5 = 0 is 5, where a ∈ ℝ is a constant. Find the two possible values of a.',
  ['a(24a + 10) = 0', 'a = 0 or 24a + 10 = 0', 'Note: if denominator = 1, Step 2 is not considered correct (oversimplified)'])
A('5-a', 'Q5(a)', '5C', [54], [12], '2-2', 'co-ordinate-geometry-of-the-circle',
  'The circle c has equation: x² + y² + 4x − 10y − 52 = 0. Write down the centre and radius of the circle c.',
  ['Centre: (−2, 5)', 'Centre or radius correct'])
dice = 'Three standard unbiased 6-sided dice are labelled h, k, and r. Gino rolls the three dice and uses the numbers shown to form the equation of a circle in the form: (x − h)² + (y − k)² = r², where h, k, and r are the numbers shown on each of the dice. Each different set of values for h, k, and r gives a different circle.'
A('5-b-i-ii', 'Q5(b)(i),Q5(b)(ii)', '10D', [54], [12], '1-1', 'co-ordinate-geometry-of-the-circle,probability',
  '(i) Write down an example of one set of numbers h, k, and r that Gino could throw, and write down the equation of the circle formed using these numbers. (ii) In total, how many different circles can Gino make in this way?',
  ['Any valid combination and the matching circle, for example', '6 × 6 × 6 [= 216]', '1 part correct and work of merit in the other part'], stem=dice)
A('5-b-iii-iv', 'Q5(b)(iii),Q5(b)(iv)', '15D', [55], [12, 13], '2-2', 'co-ordinate-geometry-of-the-circle,probability',
  '(iii) How many of these circles have both the x-axis and the y-axis as a tangent? (iv) How many of these circles lie entirely inside the first quadrant? (That is, how many neither touch nor cross the x-axis nor the y-axis?)',
  ['Answer = 6', '= 55', '(iii) correct and work of merit in (iv)'], stem=dice)
A('6-a', 'Q6(a)', '10C', [56], [14], '2-3', 'trigonometry-functions-identities',
  'θ is an acute angle, with sin θ = 1/4. Find the value of cos θ, without using a calculator. Give your answer in surd form. Show your working out.',
  ['x² = 4² − 1² = 15', 'Finds length of third side', 'Clear calculator work is not considered correct work / work of merit'])
A('6-b', 'Q6(b)', '5C', [57], [14], '2-3', 'trigonometry-functions-identities',
  'The diagram below shows the graph of y = cos² x for a limited domain. On the diagram, draw and label the graph of y = sin² x, using the same axes and scales. Use the fact that cos² A + sin² A = 1.',
  ['correct start, middle, and end points', 'local max at middle point', 'Graph of y = −cos² x drawn'])
A('6-c', 'Q6(c)', '15D', [58], [15], '2-3', 'trigonometry-functions-identities',
  'Prove that: cos(A − B) = cos A cos B + sin A sin B, where A and B are angles, with A > B. It might be helpful to use two points, P and Q, on the unit circle.',
  ['So cos(A − B) = cos A cos B + sin A sin B', 'Finishes proof', 'Accept a correct proof, even if inconsistent with labelling on diagram'])
sticks = 'In this question, all lengths are in cm. Áine has 100 sticks. Each stick has a different integer length from 1 to 100, so the lengths are: 1 cm, 2 cm, 3 cm, …, 99 cm, 100 cm. Áine makes triangles, using three of these sticks each time.'
tri_a = sticks + ' Áine makes the triangle shown below, with sides of length 12, 20, and x, where x ∈ ℕ. The size of the angle between the sides of length 12 and 20 is 58°, correct to the nearest degree.'
A('7-a-i', 'Q7(a)(i)', '5C', [59], [16], '2-3', 'trigonometry-triangles',
  'Find the area of the triangle, correct to the nearest cm².',
  ['= 102 [cm²] [∈ ℕ]', 'Full substituted area formula'], stem=tri_a)
A('7-a-ii', 'Q7(a)(ii)', '10C', [59], [16, 17], '2-3', 'trigonometry-triangles',
  'Find the value of x ∈ ℕ.',
  ['= 17 [cm] [∈ ℕ]', 'Fully substituted Cosine formula', 'Accept 17·0'], stem=tri_a)
A('7-b', 'Q7(b)', '10D', [60], [17], '2-3', 'trigonometry-triangles',
  'Áine also makes the triangle shown below. One side has a length of 72 and another has a length of y, where y ∈ ℕ. The sizes of two of the angles are 34° and 59°, each correct to the nearest degree, as shown. Find the value of y ∈ ℕ.',
  ['= 62 [∈ ℕ]', 'Finds third angle in triangle', 'Fully substituted Sine Rule'], stem=sticks)
tri_c = sticks + ' Áine makes a number of different triangles with sides of length n, n + 5, and n + 10, where n ∈ ℕ. The angle between the sides of length n and n + 5 is A, as shown in the diagram below. When Áine changes the value of n, this changes the shape of the triangle and the size of the angle A.'
A('7-c-i', 'Q7(c)(i)', '15D', [61], [18], '2-1', 'trigonometry-triangles,algebra-quadratics',
  'A = 90° for one value of n ∈ ℕ. Find this value of n.',
  ['i.e. n = 15 [as n > 0]', 'Sets up Pythagoras Theorem'], stem=tri_c)
A('7-c-ii', 'Q7(c)(ii)', '5B', [61], [18, 19], '2-3', 'trigonometry-triangles',
  'Estimate the limit of the size of the angle A, as n tends to infinity. Write a sentence to justify your answer. For this part only, assume that n can get extremely big (beyond 100).',
  ['Answer: 60°', 'As n gets very big, the triangle gets closer and closer to being equilateral.',
   'Incorrect answer, but indicates equilateral triangle'], stem=tri_c)
A('7-d', 'Q7(d)', '5D', [62], [19], '2-1', 'geometry',
  'Áine makes another triangle with three of her sticks, with sides of length 12, 24, and 30. Find how many different (non-congruent) triangles Áine could make that would be similar to this triangle. Show your working out. Remember that Áine only uses three sticks for each triangle, and that the length of each stick is a different whole number from 1 to 100, inclusive.',
  ['Answer = 19', 'Smallest such triangle is 2, 4, 5', 'Apply a * if the given triangle is not excluded (i.e. answer = 20)'], stem=sticks)
solar = 'This question is about solar panels. The graph below shows the energy produced each day by a number of solar panels, depending on the number of daylight hours. The axes do not meet at (0, 0). The energy produced is measured in kWh.'
best_fit = solar + ' According to the line of best fit, a day with 13 daylight hours corresponds to 10·7 kWh of energy being produced.'
A('8-a', 'Q8(a)', '5C', [63], [20], '1-6', 'statistics-descriptive-statistics',
  'Which of the following is closest to the value of r, the correlation coefficient, for this data? Justify your answer, based on the information in the graph. The values given are −0·95, −0·80, −0·25, 0·25, 0·80 and 0·95.',
  ['Answer: 0·8', 'Accept “positive” instead of “increasing”', 'Direction and strength acceptable in justification'], stem=solar)
A('8-b-i-ii-iii', 'Q8(b)(i),Q8(b)(ii),Q8(b)(iii)', '5C', [64], [20, 21], '1-6', 'statistics-descriptive-statistics',
  '(i) Plot a point on the diagram on the previous page to represent this information. Label this point P. (ii) Draw the line of best fit, by eye, on the diagram on the previous page. Your line of best fit should go through the point P. (iii) Use the line of best fit that you have drawn to estimate the amount of energy that would be produced for a day with 11 daylight hours. Show your work on the diagram.',
  ['Point P plotted and labelled', 'Reasonable line of best fit', 'Value read from line of best fit.'], stem=best_fit)
A('8-b-iv', 'Q8(b)(iv)', '10C', [65], [20, 21], '2-2', 'co-ordinate-geometry-of-the-line,statistics-descriptive-statistics',
  'Find the equation of the line of best fit that you drew in part (b)(ii). Use the point P you plotted in part (b)(i) and your answer from part (b)(iii). Give your answer in the form y = ax + b, where x ∈ ℝ is the number of daylight hours, y is the energy produced (in kWh), and a and b are constants.',
  ['Equation found using (13, 10·7) and their answer to part (b)(iii)', 'Fully substituted formula for equation of a line',
   'Equation in the required form'], stem=best_fit)
farm = 'Lee has a solar farm.'
A('8-c', 'Q8(c)', '10C', [66], [22], '1-2', 'probability',
  'There are 128 solar panels in Lee’s solar farm. Each week, he chooses 2 of the 128 solar panels at random to test. Find the probability that, in a given week, he chooses at least one of the same solar panels as he chose the week before. Give your answer correct to 3 decimal places.',
  ['P(at least 1) = 1 − P(none in common)', '= 0·0311 … = 0·031 [3 D.P.]', 'Correct answer, not evaluated'], stem=farm)
daylight = farm + ' The number of daylight hours per day in the solar farm over the course of one year can be modelled by the following function, H(t), for 0 ≤ t ≤ 365, t ∈ ℤ: H(t) = 4·5 sin((2π/365)t) + 12. Here, H is in hours, t is the number of days after 21st March, and (2π/365)t is in radians.'
A('8-d-i', 'Q8(d)(i)', '5C', [67], [22], '2-3', 'trigonometry-functions-identities',
  'Use H(t) to find the number of daylight hours on 28th March. Give your answer correct to 2 decimal places.',
  ['= 12·54 [2 D.P.]', 'Note: if the calculator is in a mode other than radian mode, this is considered an error, so Step 3 will not be correct.'], stem=daylight)
A('8-d-ii', 'Q8(d)(ii)', '15D', [68], [22, 23], '2-3', 'trigonometry-functions-identities',
  'Using H(t), solve an equation to find the first day (value of t) and the last day (value of t), after 21st March, for which the number of daylight hours is less than 8. Give each answer as a value of t ∈ ℤ, with 0 ≤ t ≤ 365. You do not need to find the actual date for each day.',
  ['So first day: t = 247 [first day after 246·10]', 'and last day: t = 301 [last day before 301·39]', 'Finds second value of t'], stem=daylight)
belt = 'The diagram below shows a belt drive system. In the diagram, the belt is the path from A to D to C to B and back to A, made up of two line segments and two major arcs of circles. The circles k and s have centres P and Q, respectively. A and B are points on k, and C and D are points on s. AD and BC are tangents to both circles, as shown, and intersect at the point O, which lies on PQ.'
A('9-a', 'Q9(a)', '10D', [69], [24], '2-1', 'geometry-constructions-proofs',
  'Fill in the two missing statements and four missing reasons in the table below to prove that the triangles POA and POB are congruent. The table gives Statement 1 as |PA| = |PB|, leaves Statements 2 and 3 blank, and gives the Conclusion as: Therefore, Δ POA and Δ POB are congruent.',
  ['Tangents are perpendicular to radii at point of contact', 'Common side',
   'Note: For each statement on the left, must give matching reason on the right.'], stem=belt)
belt_b = belt + ' The radius of the circle k is |PA| = 12 cm. The size of the angle ∠APO is 70°.'
A('9-b-i', 'Q9(b)(i)', '5C', [69], [24, 25], '2-3', 'trigonometry-triangles',
  'Find the distance |AO|, correct to 1 decimal place.',
  ['= 33·0 cm [1 D.P.]', 'Accept 33 (i.e. 33·0 not required)'], stem=belt_b)
A('9-b-ii', 'Q9(b)(ii)', '15D', [70], [24, 25], '3-4', 'trigonometry-triangles,area-volume',
  'The triangles POA and QOC are similar. The radius of circle s is |QC| = 8 cm. Find the total length of the belt, that is, the path from A to D to C to B and back to A. Give your answer correct to the nearest cm.',
  ['= 187 [cm] [∈ ℕ]', 'Finds total length', 'Apply a * once for incorrect rounding'], stem=belt_b)
A('9-c', 'Q9(c)', '10D', [71], [26], '3-4', 'area-volume',
  'The gear belt is packed in a closed box. The net of the box is the shaded part in the diagram below. It can be cut from a sheet of cardboard of size 55 cm by 120 cm. The height of the box, when assembled, is x cm, as shown. Two other lengths are marked j and k in the diagram. Find the volume of the box in cm³, when assembled. Give your answer in the form ax³ + bx² + cx, where a, b, c ∈ ℝ are constants. As part of your solution, express the lengths marked j and k in terms of x.',
  ['j = 55 − 2x', 'k = 60 − x', '= 2x³ − 175x² + 3300x', 'Multiplies two linear factors (simplification not required)'])
A('9-d', 'Q9(d)', '10D', [72], [27], '3-4', 'area-volume',
  'The gear belt is part of a robot lawnmower. It is used to cut the grass in the region shown in the diagram below. The perimeter of this region is made up of a number of line segments, plus the arc of one quarter of a circle from A to B with its centre on the side BC. BC is divided into six segments of equal length. The length, in metres, of five line segments are shown in the diagram (6·7, 9·1, 10·2, 8·8 and 8·8). Each of these line segments is perpendicular to BC. Liam uses the trapezoidal rule to estimate the total area of this region. By finding the actual total area, or otherwise, work out the error in Liam’s estimate for the total area of this region. Give your answer correct to the nearest m².',
  ['= 8 [m²] [∈ ℕ]', 'Finds area of quarter circle',
   'Step 4 cannot be considered correct unless Step 1 and Step 3 are both completed (with or without errors)'])
spend = 'The amount of money spent on entertainment per month by the adult population in a particular city is roughly normally distributed, with a mean of €46·02 and a standard deviation of €11·72.'
A('10-a-i', 'Q10(a)(i)', '10D', [73], [28], '1-3', 'statistics-z-scores',
  'Work out the percentage of the adult population who spend more than €50 on entertainment per month. Give your answer correct to the nearest percent.',
  ['= 37 [%] [∈ ℕ]', 'Finds z-score (0·33 or 0·34)', 'Finds required probability'], stem=spend)
A('10-a-ii', 'Q10(a)(ii)', '10D', [74], [28], '1-3', 'statistics-z-scores',
  '90% of the adult population spend less than €X on entertainment per month. Work out the value of X, correct to the nearest whole number.',
  ['= [€] 61 [∈ ℕ]', 'Finds z-score (1·28 or 1·29)', 'Equation in X'], stem=spend)
game = 'In a game, each player wants to collect as many tokens as possible. When each player takes their turn, they roll a standard unbiased 6-sided die once. Each time they roll the die: if they roll a 1, 2, 3, or 4, they get nothing; if they roll a 5 or a 6, they get 1 token.'
A('10-b-i-ii', 'Q10(b)(i),Q10(b)(ii)', '5C', [74], [29], '1-3', 'probability',
  '(i) Write down the probability that a player gets 1 token on their first turn. Amelie takes her turn 5 times in total. (ii) Work out the probability that she gets 1 token for the first time on her 5th turn. Give your answer as a fraction.',
  ['(i) correct and work of merit in (ii)', '(ii) correct',
   'Apply a * if probability is as a decimal rather than a fraction in part (ii)'], stem=game)
A('10-b-iii', 'Q10(b)(iii)', '10D', [75], [29], '1-3', 'probability',
  'Work out the probability that she gets 4 or more tokens in her 5 turns. Give your answer as a fraction.',
  ['P(4 or more) = P(4 or 5)', 'P(less than 4) evaluated', 'Apply a * if probability is as a decimal rather than a fraction'],
  stem=game + ' Amelie takes her turn 5 times in total.')
rules = game + ' The rules of the game are changed. Each time a player takes their turn, if they roll a 1, 2, 3, or 4, they still get nothing. If a player rolls a 5 or a 6, they have a choice. They can either: take 1 token and finish their turn; or: roll the die again, as part of the same turn. If they roll a 1, 2, 3, or 4 this time, they get nothing at all for this turn. If they roll a 5 or a 6, they get a total of 4 tokens for this turn. p is the probability that a player who gets a 5 or a 6 when they roll the die the first time will take 1 token and finish their turn, where 0 ≤ p ≤ 1.'
A('10-c-i', 'Q10(c)(i)', '10D', [76], [29, 30], '1-2', 'probability',
  'Work out the expected value (in tokens) of taking one turn using these rules. Remember that a turn can involve one or two rolls of the die. Give your answer in the form (a + bp)/9 where a, b are constants. It may be helpful to draw a tree diagram.',
  ['Probability of rolling again = 1 − p', 'Note: if 1 − p is not used in Step 3, then Step 4 cannot be considered correct.',
   'Answer (in correct form)'], stem=rules)
A('10-c-ii', 'Q10(c)(ii)', '5A', [76], [29, 30], '1-2', 'probability',
  'The expected value from part (c)(i) is biggest when p = 0. Explain what this means each player should do, in order to maximise the expected value (in tokens) of each turn.',
  ['Player should roll again [if they get a 5 or a 6]'], stem=rules)

selection_review = [
    {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
     'reason': 'Candidates select independently marked questions; every question is retained. No combined multi-question practice cards.'},
    {'pages': [7, 27], 'wording': 'or otherwise', 'classification': 'method-choice',
     'reason': 'Alternative solution methods for the same marked task; no printed pool of prompts.'},
    {'pages': [6, 12], 'wording': 'one possible value of n / an example of one set of numbers', 'classification': 'open-answer',
     'reason': 'Any valid value or example earns the same scale; the scheme accepts n = 841 to 891 and any valid dice combination. Nothing finite to expand into separate prompts.'},
    {'pages': [20], 'wording': 'Which of the following is closest to the value of r', 'classification': 'answer-selection',
     'reason': 'The six listed values are answer options for one required judgement with justification, not alternative practice prompts.'},
    {'pages': [22], 'wording': 'chooses 2 of the 128 solar panels at random / at least one of the same', 'classification': 'probability-sample-space',
     'reason': 'Random selection inside the probability model, not a selection of tasks.'},
    {'pages': [30], 'wording': 'They can either: take 1 token … or: roll the die again', 'classification': 'given-context',
     'reason': 'The player’s choice is the game being modelled through p; the candidate answers one required expected-value task.'},
]
def classify(c):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        return ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    if 'or otherwise' in t:
        return ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    if 'solar panels' in t:
        return ('probability-sample-space', 'Random choice of panels inside the probability model; one required probability task.')
    if 'either' in t and 'token' in t:
        return ('given-context', 'The game rule offers players a strategy modelled by p; the candidate answers one required expected-value task.')
    return None
p.write(selection_review, classify)
