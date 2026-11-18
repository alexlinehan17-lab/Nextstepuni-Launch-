"""2015 Ordinary Paper 1: 35 published scale units, 300 marks, all new."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *

R = {
 '1-a': [L(PC, 'Incorrect use of 1·29')],
 '1-b': [L(PC, 'Equates'), L(PC, 'Indicates division')],
 '1-c': [L(LPC, 'Work on Dollar Euro rate or Sterling Euro rate'), L(HPC, 'Correct Dollar Euro rate or Sterling Euro rate')],
 '2-a': [L(PC, 'Any correct ratio established or one correct amount')],
 '2-b-i': [L(LPC, 'Correct formula or work of relevance in either part'), L(LPC, 'Finds diameter (12756 km)'), L(HPC, 'One part correct'), L(HPC, 'Substitutes correctly into both formulae')],
 '2-c': [L(PC, 'Formulates division')],
 '3-a': [L(PC, 'Some correct attempt at simplifying')],
 '3-b': [L(NOTE, 'Accept {0, 1, 2}'), L(LPC, 'Any correct transposition'), L(HPC, 'Not more than two errors in solving')],
 '3-c': [L(LPC, 'Formulate division'), L(LPC, 'Attempt at factorising'), L(HPC, 'One full correct step in division')],
 '4-a': [L(LPC, 'Correct quadratic formula written'), L(LPC, 'Attempt at factorising'), L(HPC, 'Correct substitution into quadratic formula'), L(HPC, 'Finds one correct solution'), L(HPC, 'Solutions found with not more than 3 errors')],
 '4-b': [L(LPC, 'Differentiates at least one term correctly'), L(LPC, 'Correct answer without work'), L(LPC, 'Some work towards a graphical solution'), L(HPC, 'Finds correct x value'), L(NOTE, 'Accept correct turning point found graphically for full marks.')],
 '4-c': [L(PC, 'Any correct information shown on graph, e.g. indicates scale'), L(PC, 'General shape of curve drawn')],
 '5-a': [L(LPC, 'Any work towards a graphical solution'), L(LPC, 'Finds A and stops'), L(LPC, 'Finds A and B without work'), L(HPC, 'Solve for x values'), L(HPC, 'Show points on the graph'), L(HPC, 'Not more than one error working out points algebraically')],
 '5-b-i': [L(LPC, 'One or more points plotted correctly'), L(LPC, 'Any incorrect quadrilateral drawn'), L(LPC, 'Any relevant formula written'), L(MPC, 'Correct quadrilateral drawn'), L(MPC, 'Correct area of any section, without a quadrilateral established (e.g. OAC)'), L(HPC, 'Correct area of any section, provided quadrilateral established'), L(HPC, 'Area formula established, with correct substitutions, for total area')],
 '6-a-i': [L(LPC, 'One correct value'), L(MPC, 'Two correct values'), L(HPC, 'Three correct values')],
 '6-b-i': [L(PC, 'Cosine formula written'), L(PC, 'Any work of merit')],
 '6-b-ii': [L(LPC, 'ac + bd correct'), L(LPC, 'Any work of merit'), L(HPC, 'one error only in substitution, with conclusion')],
 '7-a': [L(PC, 'Outline triangle drawn'), L(PC, 'Division consistent with pattern, but not 9 triangles in fifth row')],
 '7-b': [L(PC, 'One correct entry')],
 '7-c': [L(LPC, 'Correct sequence of numbers'), L(MPC, 'First difference established'), L(HPC, 'Second difference established')],
 '7-d-i': [L(LPC, 'One correct answer'), L(HPC, 'Two correct answers')],
 '7-e': [L(NOTE, 'Scale 5B (0, 3, 5)')],
 '7-f': [L(NOTE, 'Scale 5B (0,3,5)')],
 '7-g': [L(NOTE, 'Scale 5C (0, 3, 4, 5)')],
 '7-h': [L(LPC, 'Black = 625 – White or White = 625 – Black'), L(LPC, 'Pattern extended'), L(LPC, 'Correct answer without work'), L(HPC, 'Finds n, or number of black, or number of white')],
 '8-a': [L(LPC, 'Relevant work towards finding one p value'), L(MPC, 'One correct p'), L(HPC, 'Two correct p values')],
 '8-b': [L(LPC, 'One point plotted correctly'), L(LPC, 'Correct shape of graph.'), L(MPC, 'Three or four points plotted incorrectly, with a correct shape'), L(HPC, 'Fails to join the five points or joins with a straight line'), L(HPC, 'One or two points plotted incorrectly, with a correct shape')],
 '8-c-i': [L(LPC, 'Some indication from graph that 1750 or 60 000 or both are used'), L(HPC, 'One correct answer')],
 '8-d-i': [L(LPC, 'Indicates that differentiation is being used'), L(HPC, 'Correct differentiation')],
 '8-d-ii': [L(NOTE, 'Scale 5A (0, 5)')],
 '8-e': [L(LPC, 'Evidence of more than one substitution'), L(LPC, 'Graph extended to x-axis'), L(HPC, 'Not more than two errors in solving')],
 '9-a-i': [L(PC, '10 000 or 15 000 indicated on graph, with no further work'), L(PC, 'One value read correctly'), L(PC, 'Answer between 1·55 and 2·05 (inclusive), without work')],
 '9-a-ii': [L(SOL, '4700')],
 '9-a-iii': [L(SOL, 'Exponential')],
 '9-b': [L(PC, '2500 written'), L(PC, '1 or 2 costs per km found (Amanda and/or Cathal)')],
}
ROWS = {'maths-2015-ol-p1-q' + k: v for k, v in R.items()}
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit
SCHEME_ROW_FIGURES = {'maths-2015-ol-p1-q1-a': 'maths-2015-OL-scheme-p007-i0', 'maths-2015-ol-p1-q1-b': 'maths-2015-OL-scheme-p007-i1', 'maths-2015-ol-p1-q1-c': 'maths-2015-OL-scheme-p007-i2', 'maths-2015-ol-p1-q2-a': 'maths-2015-OL-scheme-p008-i0', 'maths-2015-ol-p1-q2-b-i': 'maths-2015-OL-scheme-p008-i1', 'maths-2015-ol-p1-q2-c': 'maths-2015-OL-scheme-p008-i2', 'maths-2015-ol-p1-q3-a': 'maths-2015-OL-scheme-p009-i0', 'maths-2015-ol-p1-q3-b': 'maths-2015-OL-scheme-p009-i1', 'maths-2015-ol-p1-q3-c': 'maths-2015-OL-scheme-p009-i2', 'maths-2015-ol-p1-q4-a': 'maths-2015-OL-scheme-p010-i0', 'maths-2015-ol-p1-q4-b': 'maths-2015-OL-scheme-p010-i1', 'maths-2015-ol-p1-q4-c': 'maths-2015-OL-scheme-p011-i0', 'maths-2015-ol-p1-q5-a': 'maths-2015-OL-scheme-p012-i0', 'maths-2015-ol-p1-q5-b-i': 'maths-2015-OL-scheme-p012-i1', 'maths-2015-ol-p1-q6-a-i': 'maths-2015-OL-scheme-p013-i0', 'maths-2015-ol-p1-q6-b-i': 'maths-2015-OL-scheme-p013-i1', 'maths-2015-ol-p1-q6-b-ii': 'maths-2015-OL-scheme-p013-i2', 'maths-2015-ol-p1-q7-a': 'maths-2015-OL-scheme-p014-i0', 'maths-2015-ol-p1-q7-b': 'maths-2015-OL-scheme-p014-i1', 'maths-2015-ol-p1-q7-c': 'maths-2015-OL-scheme-p015-i0', 'maths-2015-ol-p1-q7-d-i': 'maths-2015-OL-scheme-p015-i1', 'maths-2015-ol-p1-q7-e': 'maths-2015-OL-scheme-p015-i2', 'maths-2015-ol-p1-q7-f': 'maths-2015-OL-scheme-p015-i3', 'maths-2015-ol-p1-q7-g': 'maths-2015-OL-scheme-p015-i4', 'maths-2015-ol-p1-q7-h': 'maths-2015-OL-scheme-p015-i5', 'maths-2015-ol-p1-q8-a': 'maths-2015-OL-scheme-p016-i0', 'maths-2015-ol-p1-q8-b': 'maths-2015-OL-scheme-p016-i1', 'maths-2015-ol-p1-q8-c-i': 'maths-2015-OL-scheme-p016-i2', 'maths-2015-ol-p1-q8-d-i': 'maths-2015-OL-scheme-p017-i0', 'maths-2015-ol-p1-q8-d-ii': 'maths-2015-OL-scheme-p017-i1', 'maths-2015-ol-p1-q8-e': 'maths-2015-OL-scheme-p017-i2', 'maths-2015-ol-p1-q9-a-i': 'maths-2015-OL-scheme-p018-i0', 'maths-2015-ol-p1-q9-a-ii': 'maths-2015-OL-scheme-p018-i1', 'maths-2015-ol-p1-q9-a-iii': 'maths-2015-OL-scheme-p018-i2', 'maths-2015-ol-p1-q9-b': 'maths-2015-OL-scheme-p019-i0'}

p = Paper(2015, 'ol', 'p1', {'5A': [0,5], '5B': [0,3,5], '5C': [0,3,4,5], '5D': [0,2,3,4,5], '10B': [0,3,10], '10D': [0,2,5,9,10], '15B': [0,3,15], '15C': [0,3,10,15], '15D': [0,3,7,11,15]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf', reviewed_at='2026-10-29')
A = p.A
fm = 'financial-maths'
pad = 'Padraic works in America and travels between Ireland and America.'
A('1-a','Q1(a)','10B',[7,22],[3],'3-3',fm,'In Ireland, he exchanged €2000 for US dollars when the exchange rate was €1 = $1·29. Find how many US dollars he received.',stem=pad)
A('1-b','Q1(b)','10B',[7,22],[3],'3-3',fm,'Padraic returned to Ireland and exchanged $21 000 for euro. He received €15 000. Write the exchange rate for this transaction in the form €1 = $□·□□.',stem=pad)
A('1-c','Q1(c)','5C',[7,22],[3],'3-3',fm,'Padraic wants to exchange some dollars for sterling. On a day when the euro to dollar exchange rate is €1 = $1·24 and the euro to sterling exchange rate is €1 = £0·83, find the dollar to sterling exchange rate. Write your answer in the form $1 = £□·□□.',stem=pad)
A('2-a','Q2(a)','15B',[8,22],[4],'3-1','number-systems','John, Mary and Eileen bought a ticket in a draw. The ticket cost €50. John paid €25, Mary paid €15 and Eileen paid €10. The ticket won a prize of €20 000. The prize is divided in proportion to how much each paid. How much prize money does each person receive?')
A('2-b-i','Q2(b)(i),Q2(b)(ii)','5C',[8,22],[4],'3-4','area-volume','(i) Find the length of the equator, correct to the nearest km. (ii) Find the volume of the Earth in the form a × 10ⁿ, where 1 ≤ a < 10 and n ∈ ℕ. Give the value of a correct to three decimal places.',stem='Assuming that the Earth is a sphere of radius 6378 km, as shown in the diagram:')
A('2-c','Q2(c)','5B',[8,22],[4],'3-1','number-systems','The mass of the Earth is 5·97 × 10²⁴ kg. The mass of the Sun is 1·99 × 10³⁰ kg. How many times greater than the mass of the Earth is the mass of Sun? Give your answer correct to the nearest whole number.')
A('3-a','Q3(a)','15B',[9,23],[5],'4-2','algebra','Simplify 3(4 − 5x) − 2(5 − 6x).')
A('3-b','Q3(b)','5C',[9,23],[5],'4-3','algebra','List all the values of x that satisfy the inequality 2 − 3x ≥ −6, x ∈ ℕ.')
A('3-c','Q3(c)','5C',[9,23],[5],'4-2','algebra,functions','g(x) is a function and (2 − 3x) × g(x) = 15x² − 22x + 8, for all x ∈ ℝ. Find g(x).')
fx = 'The function is f(x) = −x² + 6x − 4, x ∈ ℝ.'
q4a = 'Solve the equation −x² + 6x − 4 = 0. Give each solution correct to one decimal place.'
q4b = 'Find the co-ordinates of the turning point of the function f(x) = −x² + 6x − 4, x ∈ ℝ.'
A('4-a','Q4(a)','15C',[10,23],[6],'4-2','algebra-equations',q4a)
A('4-b','Q4(b)','5C',[10,23],[6],'5-2','differentiation',q4b)
A('4-c','Q4(c)','5B',[11,23],[6,7],'5-1','functions','Use your answers to parts (a) and (b) above to sketch the curve y = f(x). Show your scale on both axes.',stem=fx+' Part (a): '+q4a+' Part (b): '+q4b)
q5 = 'The diagram shows the graph of the function f(x) = 5x − x² in the domain 0 ≤ x ≤ 5, x ∈ ℝ.'
q5a = 'The function g is g(x) = x + 3, x ∈ ℝ. The points A(1, k) and B are the points of intersection of f and g. Find the co-ordinates of A and of B.'
A('5-a','Q5(a)','15C',[12,24],[8],'5-1','functions,algebra-equations',q5a,stem=q5)
A('5-b-i','Q5(b)(i),Q5(b)(ii)','10D',[12,24],[8],'3-4','area-volume,functions','The points O(0, 0) and C(5, 0) are on the graph of f. (i) Draw the quadrilateral OCBA on the diagram above. (ii) Find the area of the quadrilateral OCBA.',stem=q5+' Part (a): '+q5a)
z = 'The complex number z₁ = a + bi, where i² = −1, is shown on the Argand diagram below.'
q6a = '(i) Write down the value of a and the value of b. (ii) The image of z₁ under reflection in the real axis is z₂ = c + di. Write down the value of c and the value of d.'
q6b = 'The angle θ is formed by joining z₁ to 0 + 0i to z₂. Find cos θ, correct to one decimal place.'
A('6-a-i','Q6(a)(i),Q6(a)(ii)','15D',[13,24],[9],'4-4','complex-numbers',q6a,stem=z)
A('6-b-i','Q6(b)(i)','5B',[13,24],[9],'4-4','complex-numbers,trigonometry',q6b,stem=z+' Part (a): '+q6a)
A('6-b-ii','Q6(b)(ii)','5C',[13,24],[9],'4-4','complex-numbers,trigonometry','Show that |z₁| × |z₂| × cos θ = ac + bd, where a, b, c, and d are the values from part (a) above.',stem=z+' Part (a): '+q6a+' Part (b)(i): '+q6b)
pat = 'The first three patterns in a sequence of patterns are shown below.'
ss = 'sequences-series'
q7b = 'Complete the table below. Columns: Number of Black Triangles; Number of White Triangles; Total Number of Small Triangles. Pattern 1: 3; 1; T₁ = 4. Pattern 2: _; _; T₂ = _. Pattern 3: _; _; T₃ = _. Pattern 4: _; _; T₄ = _. Pattern 5: _; _; T₅ = _.'
q7e = 'Write an expression in n for the total number of triangles in the nth pattern.'
q7f = 'The number of black triangles in the nth pattern is given by the formula Bₙ = ½n² + ³⁄₂n + c. Find the value of c.'
A('7-a','Q7(a)','15B',[14,25],[10],'4-1',ss,'Draw the fourth pattern in the sequence.',stem=pat)
A('7-b','Q7(b)','15B',[14,25],[10],'4-1',ss,q7b,stem=pat)
A('7-c','Q7(c)','5D',[15,25],[10,11],'4-1',ss,'Show that the numbers of black triangles form a quadratic sequence.',stem=pat+' Part (b): '+q7b)
A('7-d-i','Q7(d)(i),Q7(d)(ii),Q7(d)(iii)','15C',[15,25],[10,11],'4-1',ss,'(i) How many black triangles are in the 9th pattern? (ii) How many white triangles are in the 9th pattern? (iii) How many small triangles, in total, are in the 9th pattern?',stem=pat)
A('7-e','Q7(e)','5B',[15,25],[10,11],'4-1',ss,q7e,stem=pat)
A('7-f','Q7(f)','5B',[15,25],[10,11],'4-1',ss,q7f,stem=pat)
A('7-g','Q7(g)','5C',[15,25],[10,11],'4-1',ss,'Use your answers to parts (e) and (f) above to find a formula for the number of white triangles in the nth pattern.',stem=pat+' Part (e): '+q7e+' Part (f): '+q7f)
A('7-h','Q7(h)','5C',[15,25],[10,11],'4-1',ss,'One particular pattern has a total of 625 triangles. Find the number of black triangles and the number of white triangles in that pattern.',stem=pat)
oil = 'The daily profit of an oil trader is given by the profit function p = 96x − 0·03x², where p is the daily profit, in euro, and x is the number of barrels of oil traded in a day.'
q8a = 'Complete the table below. Number of barrels traded in a day, x: 500, 1000, 1500, 2000, 2500. Daily profit (€), p: 40 500, _, _, _, _.'
q8b = 'Draw the graph of the trader’s profit function on the axes below for 500 ≤ x ≤ 2500, x ∈ ℝ.'
q8di = 'Use calculus to find the number of barrels of oil traded that will earn the maximum daily profit.'
A('8-a','Q8(a)','15D',[16,26],[12],'5-1','functions',q8a,stem=oil)
A('8-b','Q8(b)','15D',[16,26],[12],'5-1','functions',q8b,stem=oil+' Part (a): '+q8a)
A('8-c-i','Q8(c)(i),Q8(c)(ii)','5C',[16,26],[12],'5-1','functions','Use your graph to estimate: (i) The daily profit when 1750 barrels are traded. (ii) The numbers of barrels traded when the daily profit is €60 000.',stem=oil+' Part (a): '+q8a+' Part (b): '+q8b)
A('8-d-i','Q8(d)(i)','5C',[17,26],[12,13],'5-2','differentiation',q8di,stem=oil)
A('8-d-ii','Q8(d)(ii)','5A',[17,26],[12,13],'5-2','differentiation','Find this maximum profit.',stem=oil+' Part (d)(i): '+q8di)
A('8-e','Q8(e)','5C',[17,26],[12,13],'4-2','algebra-equations,functions','The trader will not make a profit if he trades more than k barrels of oil in a day. Calculate the value of k.',stem=oil)
car = 'Amanda buys a new car for €25 000. She knows that the value of cars depreciates by a fixed percentage each year. She draws the graph below to represent the value of her car for the next six years.'
A('9-a-i','Q9(a)(i)','15B',[18,27],[14],'5-1','functions,'+fm,'Use Amanda’s graph to estimate the length of time it will take for the car to depreciate from €15 000 to €10 000.',stem=car)
A('9-a-ii','Q9(a)(ii)','5A',[18,27],[14],'5-1','functions,'+fm,'Continue Amanda’s graph to find the approximate value of the car after 7·5 years.',stem=car)
A('9-a-iii','Q9(a)(iii)','5A',[18,27],[14],'5-1','functions','What name is given to the type of curve Amanda has drawn above?',stem=car)
A('9-b','Q9(b)','5B',[19,27],[14,15],'4-2','algebra-equations,'+fm,'On the day that Amanda bought her car, Cathal also bought a new car. His car cost €22 500. Amanda’s car will travel 15 km on a litre of fuel. Cathal’s car will travel 10 km on a litre of fuel. How many kilometres will the cars have to travel until the cost price of the car plus the cost of fuel are equal, for the two cars? Assume that fuel costs €1·50 per litre over the period.',stem='Amanda buys a new car for €25 000.')
marks = {'1':25,'2':25,'3':25,'4':25,'5':25,'6':25,'7':70,'8':50,'9':30}
p.check(marks,35)
p.review(marks,
 'Independent visual reading of all 16 question-paper pages and scheme PDF pages 1–28, including all Paper 1 model solutions (7–19), scale table and summary (20–21), and detailed marking notes (22–27). Each independently marked task is cross-checked against both the detailed notes and the summary.',
 list(range(1,29)), [20,21],
 ['All nine questions are compulsory: Q1–6 25 marks each, Q7 70, Q8 50, Q9 30; all 300 marks are retained in 35 cards.',
  'Q2(b)(i)+(ii), Q5(b)(i)+(ii), Q6(a)(i)+(ii), Q7(d)(i)+(ii)+(iii), and Q8(c)(i)+(ii) share their printed scale and remain one card each. No unmarked split creates extra marks.',
  'Scales from PDF page 20 match the detailed notes: 5A 0,5; 5B 0,3,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10B 0,3,10; 10D 0,2,5,9,10; 15B 0,3,15; 15C 0,3,10,15; 15D 0,3,7,11,15. The general full-credit-minus-one rule applies; rounding/units penalties apply once per lettered section, not per roman subpart.',
  'The model solutions contain equation objects whose text layer is scrambled. Each card carries the official typeset model solution and complete detailed marking notes after reveal. Only intact prose is quoted as text; Q7(e/f/g) and Q8(d)(ii) quote their printed scale because their answer/credit notation is carried in the image. The official Q5(a) model has a sign typo in its displayed factorisation (x+3); its preceding quadratic and following solutions x=1,3 and coordinates are retained exactly as published. A separately labelled NextStepUni clarification is displayed after reveal: the factorisation is (x − 1)(x − 3) = 0, with A(1,4) and B(3,6) unchanged.',
  'Question and scheme page references are PDF positions; scheme printed page numbers are PDF position minus 2. The scheme LC003GLP000EV.pdf is shared with Paper 2.',
  'Graphs, Argand diagram, triangle patterns, tables and all required preceding prompts accompany dependent tasks. Earlier answers are not inserted into the questions. All 35 tasks were absent before this addition.'],
 [{'pages':[2,3,10], 'wording':'Answer all nine / all six / all three questions', 'classification':'all-questions-required', 'reason':'Every question and every published scale unit is retained.'},
  {'pages':[13], 'wording':'or (between the two answer boxes in Q8(c)(ii))', 'classification':'multiple-solutions-required', 'reason':'Both graph intersections are requested by the plural numbers of barrels; this is not a choose-one prompt pool.'}],
 lambda t: ('all-questions-required','All nine questions and every published scale unit are retained.') if 'Answer all' in t else ('multiple-solutions-required','The two answer boxes represent both roots of the same graph-reading task, not a choice of questions.') if 'or' in t else None)
p.apply(ROWS,'2015 Ordinary Level Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
