"""2021 HL Paper 1: review ledger, restored prompts, add Q9(a)(i), re-quote garbled rows, move welded deductions."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *
from rows_2021_hl_p1 import ROWS

p = Paper(2021, 'hl', 'p1', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10], '15D': [0, 4, 8, 12, 15], '20D': [0, 5, 10, 15, 20]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
cx = 'complex-numbers'
A('1-a', 'Q1(a)', '10C', [7], [4], '4-4', cx, '(4 − 2i)/(2 + 4i) = 0 + ki, where k ∈ ℤ, and i² = −1. Find the value of k.')
A('1-b', 'Q1(b)', '10D', [8], [4], '4-4', cx, 'Find √(−5 + 12i). Give both of your answers in the form a + bi, where a, b ∈ ℝ.')
A('1-c', 'Q1(c)', '10D', [9], [5], '4-4', cx, 'Use De Moivre’s theorem to find the three roots of z³ = −8. Give each of your answers in the form a + bi, where a, b ∈ ℝ, and i² = −1.')
A('2-a', 'Q2(a)', '10D', [10], [6], '4-2', 'algebra-solving-equations', 'Given that x = −3 is a solution to |x + p| = 5, find the two values of p, where p ∈ ℤ.')
A('2-b', 'Q2(b)', '20D', [11], [7], '4-2', 'algebra-cubics', '(x + 4) is a factor of f(x) = x³ + qx² − 22x + 56, where x ∈ ℝ and q ∈ ℤ. Show that q = −5, and find the three roots of f(x).')
A('3-a', 'Q3(a)', '10D', [12], [8], '3-4', 'area-volume,indices-and-logs', 'Find the volume of the cuboid in the form a√b cm³, where a, b ∈ ℕ.', stem='The diagram shows a cuboid with dimensions x, y and z cm. The areas, in cm², of three of its faces are also shown: 2√2, 8√6 and 4√3.')
A('3-b-i', 'Q3(b)(i)', '10C', [12], [9], '4-2', 'algebra-quadratics', 'Given that f(x) = 3x² + 8x − 35, where x ∈ ℝ, find the two roots of f(x) = 0.')
A('3-b-ii', 'Q3(b)(ii)', '10D', [13], [9], '3-2', 'indices-and-logs,algebra-quadratics', 'Hence or otherwise, solve the equation 3^(2m + 1) = 35 − 8(3^m), where m ∈ ℝ. Give your answer in the form m = log₃ p − q, where p, q ∈ ℕ.', stem='Part (b)(i): f(x) = 3x² + 8x − 35, where x ∈ ℝ.')
A('4-a', 'Q4(a)', '15D', [14], [10], '3-1', 'induction', 'Prove using induction that 2^(3n − 1) + 3 is divisible by 7 for all n ∈ ℕ.')
ar = 'p, p + 7, p + 14, p + 21, … is an arithmetic sequence, where p ∈ ℕ.'
A('4-b-i', 'Q4(b)(i)', '5B', [14], [11], '4-1', 'sequences-series', 'Find the nth term, Tₙ, in terms of n and p, where n ∈ ℕ.', stem=ar)
A('4-b-ii', 'Q4(b)(ii)', '10C', [15], [11], '4-1', 'sequences-series', 'Find the smallest value of p for which 2021 is a term in the sequence.', stem=ar)
f5 = 'The derivative of f(x) = 2x³ + 6x² − 12x + 3 can be expressed in the form f′(x) = a(x + b)² + c, where a, b, c ∈ ℤ and x ∈ ℝ.'
A('5-a-i', 'Q5(a)(i)', '10D', [16], [12], '5-2', 'differentiation-rules,algebra-quadratics', 'Find the value of a, the value of b, and the value of c.', stem=f5)
A('5-a-ii', 'Q5(a)(ii)', '10D', [16], [12], '5-2', 'differentiation-rules,algebra-inequalities', 'If g(x) = 36x + 5, find the range of values of x for which f′(x) > g′(x).', stem=f5)
A('5-b', 'Q5(b)', '10D', [17], [13], '5-2', 'differentiation-applications,co-ordinate-geometry-of-the-line', 'The diagram below shows t, the tangent line to h(x) = 2 sin(2x), where 0 ≤ x ≤ π, at the point where x = π/6. A(0, k), where k ∈ ℝ, is the point where t cuts the y-axis. Find the value of k correct to two decimal places.')
hd = 'The diagram below shows the graph of h′(x) the derivative of a cubic function h(x). The graph cuts the x-axis at −1 and 3 and the y-axis at 6.'
A('6-a', 'Q6(a)', '10D', [18], [14], '5-1', 'functions,algebra-quadratics', 'Show that h′(x) = −2x² + 4x + 6.', stem=hd)
A('6-b', 'Q6(b)', '10C', [19], [14], '5-2', 'differentiation-applications', 'Use h′(x) to find the maximum positive value of the slope of a tangent to h(x).', stem=hd)
A('6-c', 'Q6(c)', '10D', [19], [15], '5-2', 'integration', 'The graph of h(x) passes through the point (0, −2). Find the equation of h(x).', stem=hd)
pend = 'The tip of the pendulum of a grandfather clock swings initially through an arc length of 45 cm. On each successive swing the length of the arc is 90% of the previous length.'
ss = 'sequences-series'
A('7-a-i', 'Q7(a)(i)', '5C', [20], [16], '4-1', ss, 'Complete the table below by filling in the missing lengths. Swing 1: 45 cm; swing 3: 729/20 cm; swings 2, 4 and 5 are blank.', stem=pend)
A('7-a-ii', 'Q7(a)(ii)', '5C', [20], [16], '4-1', ss, 'Tₙ = 45(0·9)^(n − 1) is the arc length of swing n. Find the arc length of swing 25, correct to 1 decimal place.', stem=pend)
A('7-a-iii', 'Q7(a)(iii)', '5C', [20], [17], '4-1', ss, 'Find the total distance travelled by the tip of the pendulum when it has completed swing 40. Give your answer, in cm, correct to the nearest whole number.', stem=pend)
A('7-a-iv', 'Q7(a)(iv)', '10C', [21], [17], '3-2', ss + ',indices-and-logs', 'Swing p is the first swing which has an arc length of less than 2 cm. Find the value of p.', stem=pend + ' Tₙ = 45(0·9)^(n − 1) is the arc length of swing n.')
A('7-b-i', 'Q7(b)(i)', '10C', [21], [18], '3-4', 'area-volume', 'If the length of the pendulum is 1 m, show that the angle, θ, of swing 1 of the pendulum is 26°, correct to the nearest degree.', stem=pend)
A('7-b-ii', 'Q7(b)(ii)', '10C', [22], [18], '4-1', ss, 'Hence, find the total accumulated angle that the pendulum swings through (i.e. the sum of all the angles it swings through until it stops swinging). Give your answer correct to the nearest degree.', stem=pend + ' The length of the pendulum is 1 m and the angle of swing 1 is 26°.')
A('7-b-iii', 'Q7(b)(iii)', '5C', [22], [19], '4-1', ss, 'Hence, or otherwise, find the total distance travelled by the tip of the pendulum when it has moved through half of the total accumulated angle. Give your answer, in cm, correct to the nearest integer.', stem=pend + ' The length of the pendulum is 1 m and the angle of swing 1 is 26°.')
hx = 'The table in Part (a)(ii) below shows some of the values of the function: h(x) = 0·001x³ − 0·12x² + px + 5, x ∈ ℝ, in the domain 0 ≤ x ≤ 75.'
A('8-a-i', 'Q8(a)(i)', '5C', [23], [20], '5-1', 'functions', 'Use h(10) = 30 to show that p = 3·6.', stem=hx)
A('8-a-ii', 'Q8(a)(ii)', '15D', [23], [20], '5-1', 'functions', 'Complete the table below and hence draw the graph of h(x) in the domain 0 ≤ x ≤ 75 on the grid below. The table gives h(10) = 30, h(40) = 21, h(60) = 5 and h(75) = 21·875, and leaves x = 0, 20, 30, 50 and 70 to complete.', stem=hx)
roller = 'The function h(x) = 0·001x³ − 0·12x² + 3·6x + 5 can be used to model the height above level ground (in metres) of a section of the path followed by a rollercoaster track, where x is the horizontal distance from a fixed point.'
A('8-b-i', 'Q8(b)(i)', '5C', [23], [21], '5-2', 'differentiation-rules', 'Find h′(x), the derivative of h(x).', stem=roller)
A('8-b-ii', 'Q8(b)(ii)', '10C', [24], [21], '5-2', 'differentiation-applications', 'Show that this section of the track reaches its maximum height above level ground when x = 20.', stem=roller)
A('8-b-iii', 'Q8(b)(iii)', '5C', [24], [22], '5-2', 'differentiation-applications', 'Find, using calculus, the height above ground, in metres, at the instant the track passes through an inflection point. The function h(x) = 0·001x³ − 0·12x² + 3·6x + 5.', stem=roller)
A('8-c', 'Q8(c)', '10D', [25], [22], '5-2', 'integration', 'Use the function h(x) = 0·001x³ − 0·12x² + 3·6x + 5, x ∈ ℝ, to find the average height of this section of the track above level ground, from x = 0 to x = 75. Give your answer in metres correct to 2 decimal places.', stem=roller)
cof = 'A cup of coffee is freshly brewed to 95° C. The temperature, T, in degrees centigrade, of the coffee as it cools is given by the formula T(t) = Ae^(−0·081t) + 20, where A is constant and t is time measured in minutes from when the coffee was brewed.'
A('9-a-i', 'Q9(a)(i)', '5C', [26], [23], '3-2', 'indices-and-logs', 'Show that A = 75.', stem=cof)
A('9-a-ii', 'Q9(a)(ii)', '5B', [26], [23], '5-1', 'functions', 'Explain what the value 20 in the formula represents in the context of the coffee cooling.', stem=cof)
A('9-a-iii', 'Q9(a)(iii)', '10C', [26], [23], '3-2', 'indices-and-logs', 'Find the decrease in the temperature of the coffee 10 minutes after brewing. Give your answer correct to the nearest whole number.', stem=cof)
A('9-b', 'Q9(b)', '10D', [27], [24], '3-2', 'indices-and-logs', 'T(t) = 75e^(−0·081t) + 20 gives the temperature of the coffee at time t. If the ideal temperature to drink coffee is 82°C, find the time, to the nearest second, that it takes for the coffee to reach this temperature.', stem='A cup of coffee is freshly brewed to 95° C.')
A('9-c', 'Q9(c)', '10D', [27], [24], '5-2', 'differentiation-rules,indices-and-logs', 'Find, to the nearest °C, the temperature the coffee has reached when T′(t) = −4·05, where T′(t) is the rate at which the coffee is cooling, in °C per minute.', stem='A cup of coffee is freshly brewed to 95° C. T(t) = 75e^(−0·081t) + 20 gives the temperature of the coffee at time t.')
A('9-d', 'Q9(d)', '10D', [28], [25], '5-2', 'differentiation-applications', 'A sugar cube is put into the coffee. The sugar keeps its cube shape as it dissolves. As the sugar cube dissolves, its volume decreases at the constant rate of 1/20 cm³/sec. Let x(t) be the sidelength of the cube at time t. Find the rate of change of x(t) when the volume of the cube reaches 1/64 cm³.')
tank = 'Water is flowing into and being removed from a tank. The volume of water in the tank is measured on a daily basis, starting at day 0. The volume of water, in litres, in the tank can be modelled by the formula V(t) = 60 + 41t − 3t², while V(t) ≥ 0, where t ∈ ℝ is the time in days, starting at day 0. Use the function V(t) to answer the following 4 questions.'
A('10-a-i', 'Q10(a)(i)', '5C', [29], [26], '4-2', 'algebra-quadratics', 'Find the value of t when the tank empties.', stem=tank)
A('10-a-ii', 'Q10(a)(ii)', '10C', [29], [26], '5-2', 'differentiation-applications', 'Find the rate at which the volume of water in the tank is changing when t = 5.', stem=tank)
A('10-a-iii', 'Q10(a)(iii)', '5B', [29], [26], '5-2', 'differentiation-applications', 'Find the value of t when the volume of water in the tank is a maximum.', stem=tank)
A('10-a-iv', 'Q10(a)(iv)', '5B', [29], [27], '5-2', 'differentiation-applications', 'Find the maximum volume of the water in the tank, correct to the nearest litre.', stem=tank)
tree = 'Trees of the same age, size and type are growing at the same rate in a forest. It is possible to measure the radius of the trunk of a tree at the end of each growing season. The increase in the radius of the trunks of these trees each year, in cm, during a particular 10 year period can be modelled by the formula: I(t) = 1·5 + sin(πt/5), where 1 ≤ t ≤ 10 and t ∈ ℕ is measured in years. Therefore r(1) = r(0) + I(1), r(2) = r(1) + I(2), …, r(t + 1) = r(t) + I(t + 1), where r(t) is the radius of the trunk of the tree after t years and r(0) is the radius of the trunk of a tree at the beginning of year 1.'
trig = 'trigonometry-functions-identities'
A('10-b-i', 'Q10(b)(i)', '5B', [30], [28], '2-3', trig, 'In order for the model to be reasonable it must satisfy a number of conditions. One condition is written below: “The radius of the trees is increasing year on year.” Show that r(t) satisfies this condition.', stem=tree)
A('10-b-ii', 'Q10(b)(ii)', '10C', [30], [28], '2-3', trig, 'Show that I(6) < I(5) and explain what this means in the context of the growth of a tree.', stem=tree)
A('10-b-iii', 'Q10(b)(iii)', '5C', [30], [29], '4-1', ss + ',' + trig, 'Two identical trees are growing in the forest. At the beginning of year 1, a tree was cut down and a section of its trunk, in the shape of a cylinder of radius 10 cm, standard length h cm, and volume V₁ cm³ was sent to a sawmill. Given that r(0) = 10, the formula r(t + 1) = r(t) + I(t + 1), where t ∈ ℕ, can be used to find the radius of the second tree for subsequent values of t. Find r(2), the radius of the second tree at t = 2. Give your answer in the form a + sin(bπ/5) + sin(cπ/5), where a, b, and c ∈ ℕ.', stem=tree)
A('10-b-iv', 'Q10(b)(iv)', '5C', [31], [29], '3-4', 'area-volume,' + ss, 'At t = 10 the second tree was also cut down. A section of its trunk, in the shape of a cylinder, of radius r(10) cm, standard length h cm, and volume V₂ cm³ was also sent to a sawmill. If V₂ = kV₁, where k ∈ ℝ, find the value of k.', stem=tree + ' A section of the first tree’s trunk, a cylinder of radius 10 cm, standard length h cm and volume V₁ cm³, was sent to a sawmill.')

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 44)
p.review(marks,
    'Independent visual reading of all 32 question-paper pages and PDF pages 1–32 of the combined Higher Level scheme (cover, contents, the Paper 1 scale table on page 4, the summary of allocations on page 5, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 scale table). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 33)), [4, 5],
    ['The 2021 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '44 independently marked units, matching the printed summary of allocations on scheme page 5. Every part has its own scale; none are shared.',
     'Paper 1 bands from scheme page 4: 5B 0,2,5; 5C 0,2,3,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15D 0,4,8,12,15; 20D 0,5,10,15,20.',
     'Before this review the deck held 43 of the 44 units. Q9(a)(i) (show that A = 75, 5C) had no card and is added. Seven cards had marking points garbled by the scheme text layer (stacked fractions and exponents read out of order, the two Q2(a) and Q3(a) method ladders merged into one, solution lines shipped instead of credit notes) and are re-quoted from the printed scheme, labelled by band and method. On the remaining cards, any “Full Credit (−1)” deduction welded onto a credit band is moved to the row note. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [9, 19], 'wording': 'Hence or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task; no printed pool of prompts.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.') if 'or otherwise' in t.lower() else None)
p.apply(ROWS, '2021 Higher Level Paper 1', expect_added=['maths-2021-hl-p1-q9-a-i'])
