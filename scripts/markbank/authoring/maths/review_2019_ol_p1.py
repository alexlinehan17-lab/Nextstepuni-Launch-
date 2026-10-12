"""2019 OL Paper 1: a new paper — 36 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, os
from review_lib import *
ALT = 'Model solution (alternative)'
M2 = 'Method 2, '

ROWS = {
 'maths-2019-ol-p1-q1-a': [L(SOL, '35300 × 0·2 = €7060'), L(SOL, '4700 × 0·4 = €1880'), L(SOL, '€7060 + 1880 = €8940'), L(SOL, '€8940 − 1650 = €7290 net tax'),
     L(LPC, 'Use of 20%, 40% or similar'), L(LPC, 'Finds 4700'), L(MPC, 'Both taxes formulated'), L(MPC, 'One tax found correctly'),
     L(HPC, 'Both taxes found and added')],
 'maths-2019-ol-p1-q1-b': [L(SOL, '40000 − (7290 + 1500) = €31210'), L(LPC, 'Brings down answer from (a)'), L(LPC, 'Finds 8790'),
     L(HPC, 'Income formulated correctly'), L(HPC, 'Correct answer without work')],
 'maths-2019-ol-p1-q1-c': [L(SOL, '35300 × 0·2 + 2700 × 0·4 = 8140'), L(SOL, '8140 − 1650 = 6490'), L(SOL, '38000 − 6490 = 31510'), L(SOL, '31510 − 31210 = €300'),
     L(SOL, '⟹ €300 increase'), L(LPC, 'Use of 7060'), L(LPC, 'Finds 2700'), L(MPC, 'Finds 8140 or equivalent'), L(HPC, 'Finds 6490 and 31510 or equivalent')],
 'maths-2019-ol-p1-q2-a-i': [L(SOL, '= 2(2 + i) = 4 + 2i'), L(SOL, '= 2 − i'), L(MPC, 'Finds 4 + 2i and 2 − i'),
     L(HPC, 'Mixes up axes but finds, plots and labels correctly'), L(NOTE, 'Ignore extra incorrect plotting')],
 'maths-2019-ol-p1-q2-a-iii': [L(LPC, 'Correct formula'), L(LPC, 'Some correct substitution')],
 'maths-2019-ol-p1-q2-b': [L(SOL, '9 − 9 + 4i − 4i = 0'), L(ALT, '= 2 ± i'), L(LPC, 'Some relevant substitution'),
     L(NOTE, 'failure to draw a relevant conclusion from incorrect work to be treated as an error'),
     L(M2 + LPC, 'Some relevant substitution into quadratic roots formula'), L(M2 + LPC, 'Quadratic roots formula written'),
     L(M2 + HPC, 'Full substitution with some errors but with complex roots and relevant conclusion given')],
 'maths-2019-ol-p1-q3-a-i': [L(SOL, 'f(x) 2 -2 2 8 10 2'), L(LPC, 'Relevant work towards finding a value for f(x)'), L(LPC, 'One point found correctly'),
     L(LPC, 'One point from candidates table plotted correctly'), L(MPC, 'Table fully correct'),
     L(MPC, 'All points from candidates incorrect table plotted and/or joined correctly'),
     L(HPC, 'All correct points found and plotted correctly, but not joined or joined incorrectly'),
     L(HPC, '4 or 5 correct points on table plotted correctly with joining')],
 'maths-2019-ol-p1-q3-a-ii': [L(SOL, 'Roots ≈ −0·7, 0·7'), L(MPC, 'One correct/relevant root given or indicated on graph')],
 'maths-2019-ol-p1-q3-b': [L(SOL, '= −6x + 8 = 0'), L(SOL, 'x = 4/3'), L(LPC, 'Any correct differentiation')],
 'maths-2019-ol-p1-q4-a': [L(SOL, '6x + 2 + 5x − 10 = 47'), L(SOL, 'x = 5'), L(LPC, '10 identified as common denominator'), L(LPC, 'Some relevant multiplication'),
     L(LPC, '2(3x + 1) + 5(x − 2) without CD'), L(LPC, 'Tests a value/s for x not equal to 5'), L(HPC, '6x + 2 + 5x − 10 = 47 or equivalent'),
     L(NOTE, 'Accept Trial and Improvement method for x = 5 verified for full marks')],
 'maths-2019-ol-p1-q4-b': [L(SOL, 'x = 5y − 13'), L(SOL, '(y − 2)(y − 3) = 0'), L(SOL, 'y = 2 and y = 3'), L(SOL, '⟹ x = −3 and x = 2'), L(SOL, '(−3, 2) and (2, 3)'),
     L(LPC, 'Isolates one variable or transposes correctly'), L(HPC, 'One relevant value (root) found from quadratic')],
 'maths-2019-ol-p1-q5-a': [L(SOL, '[0+0+2(15+18+15+12+15+18+15]'), L(SOL, 'A = 324 m²'), L(LPC, 'Any correct dimension identified'), L(LPC, 'Correct answer without work'),
     L(MPC, 'Correct formula with some correct substitution'), L(HPC, 'Correct formula fully substituted correctly')],
 'maths-2019-ol-p1-q5-b': [L(SOL, '1·6 × 60 × 60 ÷ 1000 = 5·76'), L(LPC, '1·6 × 60 or equivalent'), L(LPC, 'Any work of merit'), L(HPC, '1·6 × 60 × 60 = 5760'),
     L(HPC, '1·6 × 60 × 60 ÷ 1000 not finished')],
 'maths-2019-ol-p1-q6-a': [L(SOL, '6 − 2x < 8'), L(SOL, '2x > −2'), L(SOL, 'x > −1'), L(LPC, 'Any correct multiplication'), L(MPC, 'Correct transposing from correct work'),
     L(HPC, 'x > −1 but no plot or incorrectly plotted'), L(HPC, 'x < −1 and correctly plotted')],
 'maths-2019-ol-p1-q6-b': [L(SOL, '⇒ 2x − 1 = 6'), L(SOL, '2x = 7'), L(LPC, 'List of powers of 2'), L(LPC, 'Correct answer no work'),
     L(HPC, 'Equation in x, 2x − 1 = 6'), L(ZC, '4x − 2 = 64')],
 'maths-2019-ol-p1-q7-a': [L(SOL, 'f(0) = 1'), L(MPC, 'f(0)'), L(MPC, 't = 0')],
 'maths-2019-ol-p1-q7-b-i': [L(SOL, 'Height (m) 1 8 13 16 17 16 13 8 1'), L(LPC, 'Up to 6 correct entries'), L(MPC, 'Between 7 and 12 correct entries'),
     L(HPC, '13 to 17 correct entries, no joining or incorrect joined with a straight line'), L(NOTE, 'An entry is a calculation or a plot')],
 'maths-2019-ol-p1-q7-c-i': [L(LPC, '4·1 or similar, but no extension shown on graph'), L(LPC, 'Extension to graph only'),
     L(HPC, 'Clear indication on graph, but no value given')],
 'maths-2019-ol-p1-q7-c-ii': [L(SOL, 'Work to be shown on graph.'), L(SOL, '3·4 − 0·6 = 2·8'), L(LPC, 'f(3·4)found or indicated on graph'),
     L(LPC, 'f(0·6)found or indicated on graph'), L(HPC, '3·4 − 0·6 or equivalent and fails to finish')],
 'maths-2019-ol-p1-q7-d-i': [L(SOL, '= −8t + 16'), L(MPC, 'Any correct differentiation')],
 'maths-2019-ol-p1-q7-d-ii': [L(SOL, '−8(4·0) + 16 = −16'), L(SOL, 'Speed =16'), L(NOTE, 'Accept -16')],
 'maths-2019-ol-p1-q7-d-iii': [L(SOL, '−8t + 16 = −8'), L(SOL, '8t = 24'), L(SOL, 't = 3'), L(HPC, '−8t + 16 = −8 and fails to finish')],
 'maths-2019-ol-p1-q8-a-i': [L(SOL, '= 228·48'), L(SOL, '= 228'), L(LPC, 'Some relevant substitution into formula'),
     L(HPC, 'Formula fully substituted')],
 'maths-2019-ol-p1-q8-a-ii': [L(SOL, 'R = 5252 P/T'), L(LPC, 'Any relevant transposing'), L(HPC, 'Transposing complete but with one error')],
 'maths-2019-ol-p1-q8-b-i': [L(SOL, 'Profit (€) −4000 −3750 −3500 −3250 −3000 −2750'), L(NOTE, 'One additional correct entry'), L(HPC, 'Two correct entries')],
 'maths-2019-ol-p1-q8-b-ii': [L(SOL, '= −4000 + (n − 1)250'), L(SOL, '= 250n − 4250'), L(LPC, 'Identifies correct a and/or d'), L(HPC, 'Formula fully substituted')],
 'maths-2019-ol-p1-q8-b-iii': [L(SOL, '= 250(25) − 4250'), L(SOL, '= €2000'), L(LPC, 'Some relevant substitution into formula'),
     L(LPC, 'Month by month method incomplete'), L(HPC, 'Formula fully substituted but fails to finish')],
 'maths-2019-ol-p1-q8-b-iv': [L(SOL, '250n − 4250 = 0'), L(SOL, 'n = 17'), L(LPC, 'Some relevant substitution into formula'), L(LPC, 'Month by month method incomplete'),
     L(LPC, 'n = 17 without work'), L(HPC, '250n − 4250 = 0')],
 'maths-2019-ol-p1-q8-b-v': [L(SOL, '= n/2 [2(−4000) + (n − 1)250]'), L(SOL, '= n/2 [−8000 + 250n − 250]'), L(SOL, '= n/2 [−8250 + 250n]'),
     L(LPC, 'Identifies a and/or d'), L(HPC, 'Formula fully substituted correctly')],
 'maths-2019-ol-p1-q8-b-vi': [L(SOL, '= 37/2 [−8250 + 250(37)]'), L(SOL, '= 18500'), L(HPC, 'Correct formula fully substituted but work not complete')],
 'maths-2019-ol-p1-q9-a': [L(SOL, '= 330598·817'), L(SOL, '⇒ 330598 or 330599'), L(MPC, 'Some relevant substitution into formula')],
 'maths-2019-ol-p1-q9-b': [L(SOL, '31493 × 1·8 = 56687·4'), L(SOL, '= 56687'), L(LPC, 'Some relevant substitution into formula'),
     L(LPC, 'Incomplete trial and improvement to find m'), L(HPC, 'm = 4 found by trial and improvement but multiplied by 1·8 incorrectly')],
 'maths-2019-ol-p1-q9-c-i': [L(SOL, '600000 × 0·0012 = €720'), L(MPC, 'Use of 600000 and/or 0·0012'), L(MPC, 'Decimal error')],
 'maths-2019-ol-p1-q9-c-ii': [L(SOL, '1285·37/0·0012 = 1071141·667'), L(SOL, '= 1071142 or 1071141'), L(LPC, '1285·3 × 0·0012'), L(HPC, '1285·37 ÷ 0·0012')],
 'maths-2019-ol-p1-q9-c-iii': [L(SOL, '31492·8 × 0·0012 = €37·79'), L(SOL, '37·79 − 80 = €42·21 Loss'), L(SOL, '3470494·144 × 0·0012 = €4164·59'),
     L(SOL, '4164·59 − 80 = €4084·59 Gain'), L(LPC, 'Either month formulated correctly'), L(LPC, 'Finds number of users for either month'),
     L(MPC, 'Income for either month evaluated correctly'), L(MPC, 'Finds number of users for both months'),
     L(HPC, 'Incomes for both months evaluated correctly'), L(HPC, 'Profit/Loss for one month evaluated correctly')],
 'maths-2019-ol-p1-q9-d': [L(SOL, 'Exchange Rate = 55/62·70'), L(SOL, 'Exchange Rate = 0·8772')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2019, 'ol', 'p1', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10],
                             '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15], '20D': [0, 5, 10, 15, 20]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
em = 'Eimear earns a gross wage of €40 000 per annum with Company A.'
ema = em + ' Eimear pays income tax at a rate of 20% on income up to the standard rate cut-off point of €35 300. She pays tax at a rate of 40% on the remainder. She has annual tax credits of €1650.'
fm = 'financial-maths'
A('1-a', 'Q1(a)', '10D', [9], [4], '3-3', fm, 'Eimear pays income tax at a rate of 20% on income up to the standard rate cut-off point of €35 300. She pays tax at a rate of 40% on the remainder. She has annual tax credits of €1650. Find how much income tax she pays per annum.', stem=em)
A('1-b', 'Q1(b)', '5C', [9], [4], '3-3', fm, 'Eimear pays her health insurance which costs her €1500 net. Find her annual income after paying income tax and health insurance (i.e. her net annual income).', stem=ema)
A('1-c', 'Q1(c)', '10D', [9], [5], '3-3', fm, 'Eimear is planning to change jobs. She is offered a job by Company B with a gross wage of €38 000 and a bonus of €1500 (tax free to Eimear) to be paid by the company, which she would use to pay her health insurance. Her tax rates and credits would remain the same. Find by how much Eimear’s net annual income (after paying income tax and health insurance) will increase if she accepts the job with Company B.', stem=ema + ' Eimear pays her health insurance which costs her €1500 net.')
z = 'The complex number z₁ = 2 + i, where i² = −1, is shown on the Argand Diagram below.'
cx = 'complex-numbers'
A('2-a-i', 'Q2(a)(i),Q2(a)(ii)', '10D', [10], [6], '4-4', cx, '(i) z₂ = 2z₁. Find the value of z₂, and plot and label it on the Argand Diagram. (ii) z̅₁ is the complex conjugate of z₁. Write down the value of z̅₁, and plot and label it on the Argand Diagram.', stem=z)
A('2-a-iii', 'Q2(a)(iii)', '5D', [10], [6], '4-4', cx, 'Investigate if |z₂| = |z₁ + z̅₁|.', stem=z + ' z₂ = 2z₁, and z̅₁ is the complex conjugate of z₁.')
A('2-b', 'Q2(b)', '10C', [11], [7], '4-4', cx + ',algebra-equations', 'Show that z₁ = 2 + i is a solution of the equation z² − 4z + 5 = 0.', stem=z)
f3 = 'The function f is defined as f(x) = −x³ + 4x² + x − 2, where x ∈ ℝ.'
A('3-a-i', 'Q3(a)(i)', '15D', [12], [8], '5-1', 'graphing-functions,functions', 'Complete the table below for the values of f in the domain −1 ≤ x ≤ 4 and hence draw the graph of the function f(x) in the domain −1 ≤ x ≤ 4, x ∈ ℝ. x: −1, 0, 1, 2, 3, 4. f(x): _, _, _, _, 10, _.', stem=f3)
A('3-a-ii', 'Q3(a)(ii)', '5B', [13], [8], '5-1', 'graphing-functions', 'Use your graph to estimate the two roots of f(x) which are in the domain −1 ≤ x ≤ 4.', stem=f3)
A('3-b', 'Q3(b)', '5C', [13], [9], '5-2', 'differentiation', 'Find the value of x for which f″(x) = 0, where f″(x) is the second derivative of f(x).', stem=f3)
A('4-a', 'Q4(a)', '10C', [14], [10], '4-2', 'algebra-equations', 'Solve for x: (3x + 1)/5 + (x − 2)/2 = 47/10')
A('4-b', 'Q4(b)', '15D', [14], [11], '4-2', 'algebra-equations', 'Solve the simultaneous equations: x − 5y = −13; x² + y² = 13.')
A('5-a', 'Q5(a)', '15D', [15], [12], '3-4', 'area-volume', 'Harry draws a scale diagram of the portion of his garden that is covered in lawn. His diagram is shown below. Each box on the grid is 1 cm × 0·5 cm. Each cm on Harry’s diagram represents 3 m. In order to estimate the area of the lawn Harry divides the diagram into eight sections. Use the trapezoidal rule to estimate the area of the lawn using the scale: 1 cm = 3 m.')
A('5-b', 'Q5(b)', '10C', [15], [13], '3-3', 'number-systems', 'Nuala can walk at a speed of 1·6 metres per second. Write this speed in kilometres per hour.')
A('6-a', 'Q6(a)', '10D', [16], [14], '4-3', 'algebra', 'Solve the following inequality for x ∈ ℝ and show your solution on the numberline below: 2(3 − x) < 8.')
A('6-b', 'Q6(b)', '15C', [16], [15], '3-2', 'indices', 'Solve for x: 2^(2x−1) = 64.')
cam = 'A camogie goalkeeper, on a level pitch, hit a ball straight up into the air. The path that the ball travelled can be modelled by the function: f(t) = −4t² + 16t + 1, t ∈ ℝ, where t is the time, in seconds, from when the ball is hit and f(t) was the height of the ball, in metres, above the pitch. The ball landed on the ground without being hit again.'
A('7-a', 'Q7(a)', '5B', [17], [16], '5-1', 'functions', 'At what height was the ball when it was hit by the goalkeeper?', stem=cam)
A('7-b-i', 'Q7(b)(i),Q7(b)(ii)', '20D', [17, 18], [16, 17], '5-1', 'graphing-functions,functions', '(i) Complete the table below to show the height of the ball at various intervals during the first 4 seconds of its flight. Time (t): 0, 0·5, 1, 1·5, 2, 2·5, 3, 3·5, 4. Height (m): _, _, _, _, _, 16, _, _, _. (ii) On the grid below draw a graph to show the height of the ball while it was in the air.', stem=cam)
camg = cam + ' Part (b) completes a table of heights and draws the graph of the height of the ball while it was in the air.'
A('7-c-i', 'Q7(c)(i)', '5C', [18], [17], '5-1', 'graphing-functions', 'Use your graph to estimate (show your work on the graph): the length of time the ball was in the air from the time it was hit until it landed on the ground.', stem=camg)
A('7-c-ii', 'Q7(c)(ii)', '5C', [18], [17], '5-1', 'graphing-functions', 'Use your graph to estimate (show your work on the graph): the length of time the ball was 10 m, or more, above the ground.', stem=camg)
A('7-d-i', 'Q7(d)(i)', '5B', [19], [18], '5-2', 'differentiation', 'Find f′(t), the derivative of f(t) = −4t² + 16t + 1.', stem=cam)
A('7-d-ii', 'Q7(d)(ii)', '10C', [19], [18], '5-2', 'differentiation', 'Use your answer from part (d)(i) to find the speed of the ball when it had been in the air for 4 seconds. Give your answer in metres per second.', stem=cam + ' Part (d)(i): Find f′(t), the derivative of f(t) = −4t² + 16t + 1.')
A('7-d-iii', 'Q7(d)(iii)', '5C', [19], [18], '5-2', 'differentiation', 'Use your answer from part (d)(i) to find the value of t for which the ball was descending and travelling at a speed of 8 metres per second.', stem=cam + ' Part (d)(i): Find f′(t), the derivative of f(t) = −4t² + 16t + 1.')
pw = 'The power (P) of an engine is measured in horsepower using the formula: P = (R × T)/5252, where R is the engine speed measured in revolutions per minute (RPM) and T is the torque measured in appropriate units.'
A('8-a-i', 'Q8(a)(i)', '5C', [20], [19], '4-1', 'algebra', 'Find the power of an engine that generates 480 units of torque at 2500 RPM. Give your answer correct to the nearest whole number.', stem=pw)
A('8-a-ii', 'Q8(a)(ii)', '10C', [20], [19], '4-1', 'algebra', 'Rearrange the formula to write R in terms of P and T.', stem=pw)
co = 'A company was set up in January 2016 to repair engines. In the first month of its existence the company made a loss of €4000. This loss reduced by €250 a month for each month that the company traded.'
ss = 'sequences-series'
A('8-b-i', 'Q8(b)(i)', '5C', [20], [20], '4-1', ss, 'Complete the table below to show the company’s loss/profit for each of the first six months of trading. Month: 1, 2, 3, 4, 5, 6. Profit (€): −4000, −3750, _, −3250, _, _.', stem=co)
A('8-b-ii', 'Q8(b)(ii)', '10C', [20], [20], '4-1', ss, 'Show that the profit the company makes in month n is given by the formula Tₙ = 250n − 4250.', stem=co)
cot = co + ' The profit the company makes in month n is given by the formula Tₙ = 250n − 4250.'
A('8-b-iii', 'Q8(b)(iii)', '5C', [21], [20], '4-1', ss, 'What profit does the company make in January 2018 (i.e. month 25)?', stem=cot)
A('8-b-iv', 'Q8(b)(iv)', '5C', [21], [21], '4-1', ss + ',algebra-equations', 'Find the month in which the company breaks even (i.e. €0 profit).', stem=cot)
A('8-b-v', 'Q8(b)(v)', '10C', [21], [21], '4-1', ss, 'Find Sₙ, the general term for the total profit of the company after n months.', stem=cot)
A('8-b-vi', 'Q8(b)(vi)', '5C', [21], [21], '4-1', ss, 'Hence, or otherwise, find the total profit of the company at the end of January 2019 (i.e. month 37).', stem=cot + ' Part (b)(v): Find Sₙ, the general term for the total profit of the company after n months.')
web = 'Avril has a website. For a certain period of time, the total number of registered users of the website, U(m), can be estimated by using the formula: U(m) = 3000(1·8)^m, where m is the number of months from when the website was launched.'
A('9-a', 'Q9(a)', '5B', [22], [22], '3-2', 'indices', 'Use the formula to estimate the number of registered users 8 months after the website was launched.', stem=web)
A('9-b', 'Q9(b)', '5C', [22], [22], '3-2', 'indices,number-systems', 'There are 31 493 registered users at the end of a particular month. Estimate how many users there will be one month later.', stem=web)
adv = web + ' Users can register free of charge on the website. Through advertising, Avril earns €0·0012 each month, for every user who is registered.'
A('9-c-i', 'Q9(c)(i)', '5B', [22], [22], '3-3', 'number-systems', 'How much would she earn in a month when there were 600 000 registered users?', stem=adv)
A('9-c-ii', 'Q9(c)(ii)', '10C', [22], [22], '3-3', 'number-systems', 'Avril earns €1285·37 for a particular month. How many registered users did the website have in that month.', stem=adv)
A('9-c-iii', 'Q9(c)(iii)', '10D', [23], [23], '3-3', fm + ',indices', 'A web design company charges Avril €80 per month to maintain and host the site. How much will Avril make or lose in month 4 and in month 12 from the website.', stem=adv)
A('9-d', 'Q9(d)', '5C', [23], [23], '3-3', fm, 'Another web design company in the UK offers to host and maintain her website for £55 sterling per month. Avril uses the exchange rate on a particular day to find how much this would cost in euro. She finds that it would cost €62·70. Find the exchange rate for 1 euro on that day. Give your answer correct to 4 decimal places.', stem='Avril has a website.')

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 55, '9': 40}
p.check(marks, 36)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 1–25 of the combined Ordinary Level scheme (cover, notes, contents, the Paper 1 title page, the Paper 1 scale table on page 5, the summary of mark allocations on page 6, the annotation palette on pages 7–8, every Paper 1 model solution and marking note on pages 9–23, the blank page 24 and the Paper 2 title page 25). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 26)), [5, 6],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 55 marks, Q9 40 marks). Every question is retained.',
     '36 independently marked units, matching the printed summary on scheme page 6. Shared scales are one task each: Q2(a)(i)+(ii) 10D and Q7(b)(i)+(ii) 20D.',
     'Paper 1 bands from the 2019 Ordinary Level scale table on scheme page 5: 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15; 20D 0,5,10,15,20.',
     'This paper had no authored cards before this review; all 36 units are new. Marking points are lifted line by line from the scheme and labelled with the part of the scheme they come from. This scheme’s text layer encodes subscripts and superscripts as unrelated ASCII characters (z₂ extracts as “z8”, f′ as “fL”, 2^(2x−1) as “28TE;”), which no glyph map can repair because the characters are ordinary ASCII. Marking points containing them are not quoted; the scheme reader carries them. For the same reason Q2(a)(iii), Q3(b), Q7(d)(ii) and Q9(d) quote fewer credit bands than the scheme prints. Q8(b)(i) prints its first bullet (“One additional correct entry”) under no band heading, so it is quoted as a note.',
     'Graph and table tasks (Q3(a)(i), Q7(b), Q7(c)) carry their printed credit criteria; the drawn graphs are in the scheme reader.',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [21], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2019 Ordinary Level Paper 1', expect_added=[c['id'] for c in p.cards])
