"""2022 OL Paper 1: review ledger, restored prompts, add Q5(a), re-quote Q1(a)-(b) and Q3(c)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *

ROWS = {
 'maths-2022-ol-p1-q1-a': [L(SOL, 'z₁ = −2 − 3i and z̅₁ = −2 + 3i'),
     L(LPC, 'Work of merit, for example, real or imaginary part of z₁ or z̅₁ correct, or real or imaginary part of z₂ or z₃ plotted correctly'),
     L(LPC, '1 part correct'), L(MPC, '2 parts correct'), L(HPC, '4 parts correct'), L(NOTE, 'Apply F* if labels omitted')],
 'maths-2022-ol-p1-q3-c': [L(SOL, '80 × 12 = €960 total annual increase'), L(SOL, '60% of increase = €960'), L(SOL, '1% of increase = 960/60 = 16'),
     L(SOL, '100% of increase = 16 × 100 = [€]1600'), L(SOL, 'Trial and improvement leading to solution'),
     L(LPC, 'Work of merit, for example, finds 960'), L(LPC, 'Indicates 60%'), L(LPC, 'Shows use of trial and improvement'),
     L(HPC, 'Correct answer based on monthly increase'), L(HPC, 'Finds total 960 and indicates 60%'),
     L(FC, 'Using trial and improvement leading to correct answer')],
 'maths-2022-ol-p1-q5-a': [L(SOL, '1·2 × 10³'), L(SOL, '2·7 × 10⁻¹'),
     L(LPC, 'Work of merit, for example, a or n correct in one part, or one number correctly written in form a × 10ⁿ but where a < 1 or a > 10'),
     L(LPC, '1000 or 1/10'), L(HPC, 'One part correct')],
}
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2022, 'ol', 'p1', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10], '15D': [0, 4, 8, 12, 15]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
cx = 'complex-numbers'
z1 = 'The complex number z₁ is shown on the Argand diagram below.'
z23 = z1 + ' z₂ and z₃ are two other complex numbers. z₂ = −5 + 3i and z₃ = 4 − 2i, where i² = −1.'
A('1-a', 'Q1(a)(i),Q1(a)(ii),Q1(b)', '15D', [8], [4, 5], '4-4', cx, '(a) Using the Argand diagram: (i) write down the values of z₁ and z̅₁, where z̅₁ is the complex conjugate of z₁; (ii) plot and label z̅₁ on the Argand diagram above. (b) z₂ and z₃ are two other complex numbers. z₂ = −5 + 3i and z₃ = 4 − 2i, where i² = −1. Plot and label z₂ and z₃ on the Argand diagram on the previous page.', stem=z1)
A('1-c', 'Q1(c)', '10D', [8], [5], '4-4', cx, 'Write z₂ − z₃ in the form a + bi, where a, b ∈ ℝ, i² = −1, and hence find |z₂ − z₃|.', stem=z23)
A('1-d', 'Q1(d)', '5C', [9], [5], '4-4', cx, 'Investigate if z₃ = 4 − 2i is a solution of the equation z² + 2iz − 7i = 0.', stem=z23)
A('2-a', 'Q2(a)', '10C', [10], [6], '4-2', 'algebra-equations', 'Solve the following equation in x: 2(3x − 5) + 8 = 4x − 5')
A('2-b', 'Q2(b)', '5B', [10], [6], '3-2', 'indices', 'Write (3⁴)⁵/3⁶ in the form 3^k, where k ∈ ℝ.')
A('2-c', 'Q2(c)', '15D', [10], [7], '4-2', 'algebra-equations', 'Solve the simultaneous equations below to find the value of x and the value of y: 3x + 2y = 1; 7x + 5y = −2')
tax = 'Joe, Émile, and Wei are all PAYE workers. Each of them has an annual tax credit of €3300. Their tax rates and bands are shown in the table below: annual income, first €35 300 taxed at 20%; balance taxed at 40%. Assume that no other deductions are made from their income.'
fm = 'financial-maths'
A('3-a', 'Q3(a)', '10C', [11], [8], '3-3', fm, 'Joe’s gross annual income is €27 500. Joe only pays tax at the lower rate. Work out Joe’s net annual income.', stem=tax)
A('3-b', 'Q3(b)', '10D', [11], [8], '3-3', fm, 'Émile’s gross annual income is €43 450. Work out Émile’s net annual income.', stem=tax)
A('3-c', 'Q3(c)', '10C', [12], [9], '3-3', fm, 'Wei’s gross annual income is over €35 300, so she pays tax at both rates. Wei is looking for a pay rise. She wants her net income to increase by €80 each month. Work out how much her gross annual income will need to increase by, in order for this to happen.', stem=tax)
g = 'g(x) = x³ − 7x² + x − 12, where x ∈ ℝ.'
A('4-a-i', 'Q4(a)(i)', '10C', [13], [10], '5-1', 'functions', 'Work out the value of g(5).', stem=g)
A('4-a-ii', 'Q4(a)(ii)', '5B', [13], [10], '5-2', 'differentiation', 'Find g′(x), the derivative of g(x).', stem=g)
A('4-a-iii', 'Q4(a)(iii)', '10C', [13], [10], '5-2', 'differentiation,co-ordinate-geometry-of-the-line', 'g′(5) = 6. Use this to find the equation of the tangent to the curve y = g(x) when x = 5. Give your answer in the form ax + by + c = 0, where a, b, c ∈ ℝ.', stem=g)
A('4-b-i', 'Q4(b)(i),Q4(b)(ii)', '5C', [13, 14], [11], '5-2', 'differentiation,graphing-functions', '(i) Using the graph, write down a value of x for which u′(x) is negative. (ii) On the diagram above, draw the tangent to u(x) at the point (4, 2) and use the tangent that you draw to work out an estimate for the value of u′(4).', stem='The graph of the function y = u(x) is shown below, for 0 ≤ x ≤ 10, x ∈ ℝ. u′(x) is the derivative of u(x).')
A('5-a', 'Q5(a)(i),Q5(a)(ii)', '10C', [15], [12], '3-2', 'indices,number-systems', 'Write each of the following values in the form a × 10ⁿ where 1 ≤ a < 10 and n ∈ ℤ. (i) 1200 (ii) 0·27')
A('5-b', 'Q5(b)', '10D', [15], [12], '3-3', 'number-systems', 'A falcon can dive at a speed of up to 120 miles per hour. 1 mile is approximately 1·6 kilometres. Use this to work out how long it would take the falcon to travel 100 metres, when diving at this speed. Give your answer in seconds, correct to one decimal place.')
A('5-c-i', 'Q5(c)(i),Q5(c)(ii)', '10D', [16], [13], '5-1', 'graphing-functions', 'Use the graphs to estimate each of the following, for 0 ≤ x ≤ 5: (i) the two values of x for which m(x) = 0; (ii) the range of values of x for which k(x) is less than m(x).', stem='The diagram below shows the graphs of the functions k(x) and m(x), for 0 ≤ x ≤ 5, x ∈ ℝ.')
seq = 'The nth term of an arithmetic sequence is given by the following expression, for n ∈ ℕ: Tₙ = −254 + (n − 1)(4)'
A('6-a-i', 'Q6(a)(i)', '5B', [17], [14], '4-1', 'sequences-series', 'Find the value of T₁, the first term of this sequence.', stem=seq)
A('6-a-ii', 'Q6(a)(ii)', '5C', [17], [14], '4-1', 'sequences-series', 'Find the value of the common difference for this sequence (that is, T₂ − T₁).', stem=seq)
A('6-b', 'Q6(b)', '10C', [17], [14], '4-3', 'sequences-series,algebra', 'Find the smallest value of n ∈ ℕ for which −254 + (n − 1)(4) > 0', stem=seq)
A('6-c', 'Q6(c)', '10C', [18], [15], '4-2', 'sequences-series,algebra-equations', 'The sum of the first n terms of this sequence is given by Sₙ = (n/2)[2(−254) + 4n − 4]. Solve the following equation for n ∈ ℕ. Note that n ≠ 0. (n/2)[2(−254) + 4n − 4] = 0', stem=seq)
hr = 'Joseph is doing a training session. During the session, his heart-rate, h(x), is measured in beats per minute (BPM). For part of the session, h(x) can be modelled using the following function: h(x) = −0·38x³ + 2·6x² − 0·13x + 158, where x is the time, in minutes, from the start of the session, and 0 ≤ x ≤ 6, x ∈ ℝ.'
A('7-a-i', 'Q7(a)(i),Q7(a)(ii)', '15D', [19], [16], '5-1', 'functions,graphing-functions', '(i) Complete the table below to show the values of h(x) for the given values of x (0 to 6 minutes; the table gives 160 at 1 minute, 171 at 3 minutes and 169 at 6 minutes). Give each value of h(x) correct to the nearest whole number. (ii) Draw the graph of y = h(x) on the axes below, for 0 ≤ x ≤ 6, x ∈ ℝ. Note that the point A (6, 169) is on the graph.', stem=hr)
A('7-b', 'Q7(b)', '5B', [19], [17], '5-1', 'functions', 'Explain what the co-ordinates of the point A (6, 169) represent, in the context of Joseph’s heart-rate.', stem=hr)
A('7-c', 'Q7(c)', '10C', [19, 20], [16, 17], '5-1', 'graphing-functions', 'Using the same axes and scales, continue your graph on the previous page to show the following information. From the point represented by A (6, 169), Joseph’s heart-rate: stays at the same level for the next 2 minutes, and then decreases at a steady rate of 10 BPM per minute for 2 minutes.', stem=hr)
A('7-d', 'Q7(d)', '5B', [20], [17], '5-1', 'functions', 'During his training session, the number of calories per minute that Joseph is burning after x minutes can be modelled by c(x) as follows, where h(x) is Joseph’s heart-rate at that time: c(x) = 0·1 h(x) − 7. Using the information in the table or graph, work out c(6), the number of calories per minute that Joseph is burning 6 minutes after the start of the session.', stem=hr)
A('7-e', 'Q7(e)', '5B', [20], [18], '3-3', 'number-systems', 'Joseph has a smart watch that beeps every 15 seconds during the session. It beeps for the first time at exactly 2:55 p.m., as Joseph starts his session. It beeps for the last time at exactly 3:23 p.m., as Joseph finishes his session. Work out how many times, in total, the smart watch beeps during the session, including the first and last beep.', stem=hr)
A('7-f', 'Q7(f)', '10C', [21], [18], '5-2', 'differentiation,algebra-equations', 'Solve the equation h′(x) = −1·14x² + 5·2x − 0·13 = 0 to find how long after the start of the session Joseph’s heart-rate is at a maximum, for 0 ≤ x ≤ 6, x ∈ ℝ. Give your answer in minutes, correct to 2 decimal places.', stem=hr)
acid = 'Jessica is a scientist. Jessica is making up a solution of acid. She has two different bottles, each with the following concentration of the acid: Bottle A, concentration 12%; Bottle B, concentration 5%. This means that, for example, in every 100 ml of liquid in Bottle A, there are 12 ml of acid.'
ns = 'number-systems'
A('8-a-i', 'Q8(a)(i)', '5B', [22], [19], '3-3', ns, 'Work out how many ml of acid are in 200 ml of liquid from Bottle A.', stem=acid)
A('8-a-ii', 'Q8(a)(ii)', '10C', [22], [19], '3-3', ns, 'Jessica mixes 200 ml of liquid from Bottle A with 300 ml of liquid from Bottle B. Work out the overall concentration of the acid in Jessica’s mixture. Give your answer as a percentage.', stem=acid)
A('8-a-iii', 'Q8(a)(iii)', '5B', [22], [19], '3-3', ns, 'Explain why Jessica could not make a solution with a 4% concentration of acid by mixing liquid from Bottle A and Bottle B.', stem=acid)
A('8-a-iv', 'Q8(a)(iv)', '5C', [22], [20], '3-3', ns, 'When she is making another mixture, Jessica makes a mistake in measuring. She wants to measure out 250 ml but she measures out 260 ml instead. Work out the percentage error in this measurement.', stem=acid)
euler = 'If a solid is made up of faces with straight edges, then the following identity is often true: C − E + F = 2, where C is the number of corners, E is the number of edges, and F is the number of faces.'
A('8-b-i', 'Q8(b)(i)', '5C', [23], [20], '3-4', 'area-volume', 'Write down the values of C, E, and F for a cube, and show that C − E + F = 2 for these values. The value for E has already been filled in: E = 12.', stem=euler)
A('8-b-ii', 'Q8(b)(ii)', '10C', [23], [21], '3-4', 'area-volume', 'Each of the faces of a different solid is in the shape of a triangle of area 5 cm². This solid has 12 corners (C) and 30 edges (E), and C − E + F = 2 for this solid. Work out the surface area of this solid, in cm².', stem=euler)
A('8-b-iii', 'Q8(b)(iii)', '10D', [23], [21], '4-2', 'algebra-equations', 'The surface of a third solid is made up of h hexagons and p pentagons, where h, p ∈ ℕ. For this solid: (6h + 5p)/3 − (6h + 5p)/2 + h + p = 2. Use this equation to find the number of pentagons in the surface of this solid (that is, the value of p).', stem=euler)
car = 'Brian buys a new car. The graph below represents a model that can be used to predict the value of this car, V, for the next number of years. This model assumes that the value of the car reduces (depreciates) by a fixed percentage each year.'
A('9-a-i', 'Q9(a)(i)', '5B', [24], [22], '3-3', fm + ',graphing-functions', 'Use the graph to write down V(0), the initial value of Brian’s car, and V(1), the value of Brian’s car after 1 year.', stem=car)
A('9-a-ii', 'Q9(a)(ii)', '5C', [24], [22, 23], '3-3', fm, 'Show that the value of the car will reduce by 20% in its first year, according to this model.', stem=car)
A('9-b-i', 'Q9(b)(i)', '5C', [24], [23], '3-3', fm, 'Based on this model, write a formula for V(t), the value of Brian’s car after t years, in terms of the age of the car (t). Use the fact that the value decreases by 20% each year.', stem=car)
A('9-b-ii', 'Q9(b)(ii)', '10C', [24], [23], '3-3', fm, 'Hence, or otherwise, work out the value of Brian’s car after 4 years, according to this model. Show your working out.', stem=car)
A('9-c-i', 'Q9(c)(i),Q9(c)(ii)', '5B', [25], [24], '5-1', 'graphing-functions,' + fm, 'The graph from part (a) is shown again below. A different (linear) model assumes that the value of the car reduces (depreciates) by a fixed amount each year. The value of the car will also reduce by 20% in its first year, according to this model. (i) Draw a line on the diagram above, passing through the first two points on the graph with whole-number values of t (t = 0 and t = 1). Continue your line until it reaches the horizontal axis. (ii) Hence, or otherwise, estimate T, the age of Brian’s car when its value would be €0, according to this new model.', stem=car)
A('9-d', 'Q9(d)', '10D', [25], [25], '3-3', fm, 'Eva buys a new car that has a price of €19 445. She pays 30% of this price as a deposit and makes repayments of €206·97 each month for the following 3 years. At the end of the 3 years, she pays an additional lump sum of €7389. Work out the total cost of the car for Eva.')
A('9-e', 'Q9(e)', '10C', [25], [25], '3-3', ns, 'Eva drives her car home from the garage, a distance of 12 km. Eva usually drives this journey at an average speed of 60 km/hr. On this day, there are roadworks, so her average speed is only 40 km/hr for the journey. Work out the percentage increase in the time it takes Eva to drive home, because of the roadworks.')
hurl = 'Keith plays hurling. During a match, Keith hits the ball with his hurl. The height of the ball could be modelled by the following quadratic function: h = −2t² + 5t + 1·2, where h is the height of the ball, in metres, t seconds after being hit, and t ∈ ℝ.'
A('10-a-i', 'Q10(a)(i)', '5B', [26], [26], '5-1', 'functions', 'How high, in metres, was the ball when it was hit (when t = 0)?', stem=hurl)
A('10-a-ii', 'Q10(a)(ii)', '5B', [26], [26], '5-1', 'functions', 'The ball was caught after 2·4 seconds. How high, in metres, was the ball when it was caught?', stem=hurl)
A('10-a-iii', 'Q10(a)(iii)', '10D', [26], [27], '4-2', 'algebra-equations', 'When the ball passed over the halfway line, it was at a height of 3·2 metres and its height was decreasing. How many seconds after it was hit did the ball pass over the halfway line? Remember that h = −2t² + 5t + 1·2.', stem=hurl)
A('10-a-iv', 'Q10(a)(iv)', '10C', [27], [27], '5-2', 'differentiation', 'Find dh/dt and hence find how long it took the ball to reach its greatest height. Give your answer in seconds.', stem=hurl)
A('10-b', 'Q10(b)', '10D', [27, 28], [28], '5-1', 'graphing-functions', 'Later in the game, Keith hit the ball again. This time, the height of the ball t seconds after it was hit could be modelled by a different quadratic function, y = k(t), where k is in metres. This time, the ball was 1 metre high when Keith hit it. Its greatest height was 5 metres, which it reached after 2 seconds. It hit the ground without being caught. Using the information above, write down the co-ordinates of three points that must be on the graph of y = k(t), and draw the graph of y = k(t) on the axes below, from when the ball is hit until it hits the ground.', stem='Keith plays hurling.')
A('10-c-i', 'Q10(c)(i)', '5C', [28], [29], '3-3', fm, 'Keith buys a new hurl. It usually costs €33. Keith gets a student discount of 15%. Work out the price Keith pays for the hurl.', stem='Keith plays hurling.')
A('10-c-ii', 'Q10(c)(ii)', '5C', [28], [29], '3-3', fm, 'Keith also buys a jersey. This costs €49·50, including VAT at 23%. Work out the VAT on this jersey. Give your answer correct to the nearest cent.', stem='Keith plays hurling.')

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 47)
p.review(marks,
    'Independent visual reading of all 32 question-paper pages and PDF pages 1–29 of the combined Ordinary Level scheme (cover, notes, the Paper 1 scale table on page 4, the summary of allocations on page 5, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 30)), [4, 5],
    ['The 2022 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '47 independently marked units, matching the printed summary of allocations on scheme page 5. Shared scales keep their parts together: Q1(a)(i)–(ii) with Q1(b) 15D, Q4(b)(i)–(ii) 5C, Q5(a)(i)–(ii) 10C, Q5(c)(i)–(ii) 10D, Q7(a)(i)–(ii) 15D and Q9(c)(i)–(ii) 5B.',
     'Paper 1 bands from scheme page 4: 5B 0,2,5; 5C 0,2,3,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15D 0,4,8,12,15.',
     'Before this review the deck held 46 of the 47 units. Q5(a)(i)–(ii) (writing 1200 and 0·27 in the form a × 10ⁿ, one 10C scale) had no card and is added. Q1(a)–(b) had carried the Argand-diagram axis label “Re” into its high-partial band, and Q3(c) shipped its model-solution lines (including the scheme’s editorial query “Need to show solving using a variable?”) instead of its credit notes; both are re-quoted from the printed notes and labelled by band. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [23, 24], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task; no printed pool of prompts.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2022 Ordinary Level Paper 1', expect_added=['maths-2022-ol-p1-q5-a'])
