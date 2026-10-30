"""2014 Ordinary Project Maths Paper 1: all 39 published scale units, 300 marks."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *

R = {
 '1-a':[L(LPC,'Finds cost of blazers or trousers'),L(HPC,'Finds cost of 25 of each')],
 '1-b':[L(PC,'Subtracts either 20 or 30 from 89·95'),L(PC,'Cost of 1 set = €50')],
 '1-c':[L(LPC,'Finds SP of 22 sets'),L(MPC,'Finds total selling price'),L(HPC,'Correct expression for mark-up written but fails to finish or finishes incorrectly')],
 '2-a-i':[L(LPC,'Correct substitution for z1 or z2 in expression'),L(HPC,'Correct substitution for z1 and z2 in expression but error in finishing')],
 '2-a-ii':[L(LPC,'Use of candidate’s answer from (i)'),L(LPC,'Correct modulus formula written'),L(HPC,'One modulus correctly calculated')],
 '2-a-iii':[L(PC,'Incomplete explanation but mentions distance or length or squaring')],
 '2-b':[L(LPC,'Terms rearranged'),L(LPC,'Correct substitution'),L(HPC,'Multiplication above and below by correct conjugate and some subsequent work')],
 '3-a-i':[L(LPC,'Some correct attempt at solving'),L(HPC,'Not more than 2 errors in solving')],
 '3-a-ii':[L(PC,'Some correct substitution of answers from (i)'),L(PC,'No conclusion or incorrect conclusion if not equal')],
 '3-b':[L(LPC,'Some correct attempt at isolating x or y in linear equation'),L(MPC,'Correctly substitutes into quadratic'),L(HPC,'Solves correctly for 1 variable only and stops or one (x, y) only')],
 '4-a':[L(LPC,'Some correct effort at factorising'),L(LPC,'Correct quadratic formula written'),L(HPC,'Correct factors found')],
 '4-b':[L(SOL,'Graph D'),L(NOTE,'Linked to (a)')],
 '4-c-i':[L(LPC,'1 or 2 graphs of correct shape drawn'),L(HPC,'Both drawn correctly but not labelled or incorrectly labelled'),L(HPC,'1 graph drawn correctly and labelled')],
 '5-a-i':[L(LPC,'Some correct substitution in either or both expressions'),L(HPC,'One expression worked out correctly'),L(HPC,'Both expressions worked out but with errors')],
 '5-b':[L(LPC,'Differentiates at least one term correctly'),L(MPC,'Correct differentiation and stops'),L(HPC,'Finds x values only of turning points')],
 '5-c':[L(LPC,'Plots 2 or 3 relevant points correctly'),L(LPC,'Sketches the correct shape with no reference to relevant points'),L(HPC,'Plots 4 relevant points correctly, but does not sketch a curve, or sketches an incorrectly shaped curve')],
 '6-a-i':[L(LPC,'Finds one term only'),L(HPC,'Finds 2 terms correctly')],
 '6-a-ii':[L(LPC,'Some attempt at substitution'),L(HPC,'List method, but fails to identify term or number of the terms'),L(HPC,'Sign error when solving inequality')],
 '6-b-i':[L(LPC,'Correct formula written'),L(LPC,'Identifies a and/or d'),L(HPC,'Correct formula substituted with 1 error')],
 '6-b-ii':[L(LPC,'Some correct simplification of expression for Sn carried to (b)(ii)')],
 '7-a':[L(LPC,'Writes correct formula without further work of merit'),L(LPC,'Use of appreciation method'),L(HPC,'Calculates the amount at the end of each of 4 years, but with errors')],
 '7-b-i':[L(LPC,'Calculates the balance to be borrowed and stops'),L(HPC,'Calculates interest only')],
 '7-b-ii':[L(LPC,'Calculates amount to be repaid at end of 6 months'),L(LPC,'Uses Simple Interest'),L(HPC,'Principal correct and calculates correctly for 3 or more months')],
 '7-b-iii':[L(PC,'Correct conclusion with no justification'),L(PC,'Correct conclusion from incorrect total repayment(s)')],
 '8-a':[L(PC,'12×12 and stops')],
 '8-b':[L(HPC,'1 value correct')],
 '8-c':[L(LPC,'Correct formula written'),L(LPC,'Some relevant attempt at multiplying terms'),L(HPC,'Errors in finding product')],
 '8-d':[L(LPC,'One or two terms differentiated correctly'),L(MPC,'Correct differentiation and stops'),L(HPC,'Correct derivative = 0 and stops or error(s) in solving it')],
 '8-e':[L(PC,'Value of h from (d) substituted into V(h)'),L(PC,'More than one effort at trial and error')],
 '9-a':[L(LPC,'At least one correct value'),L(LPC,'Substitutes correctly at least once'),L(HPC,'5 or 6 correct values')],
 '9-b':[L(LPC,'At least 1 point plotted correctly'),L(HPC,'Points connected with straight edge'),L(HPC,'At least 5 points plotted correctly and joined'),L(HPC,'All points plotted correctly but not joined')],
 '9-c-i':[L(PC,'Uses t = 2·5 to solve')],
 '9-c-ii':[L(PC,'Correct h ordinate indicated on graph')],
 '9-c-iii':[L(PC,'Only one ordinate given'),L(PC,'Coordinates reversed')],
 '9-d-i':[L(LPC,'Any work of merit e.g. correct formula given'),L(MPC,'One slope calculated correctly'),L(HPC,'Both slopes calculated correctly with incorrect or no conclusion')],
 '9-e-i':[L(PC,'1 term differentiated correctly')],
 '9-e-ii':[L(HPC,'The candidate’s value of t substituted into expression for h')],
 '9-e-iii':[L(SOL,'4 m/s')],
 '9-f':[L(LPC,'Correct answer with no work or without calculus'),L(HPC,'The candidate’s value of t substituted into expression for h and stops or continues with errors')],
}
ROWS = {'maths-2014-ol-p1-q'+k:v for k,v in R.items()}
if len(sys.argv)>1: quotes(ROWS,sys.argv[1]); raise SystemExit
SCHEME_ROW_FIGURES = {'maths-2014-ol-p1-q1-a': 'maths-2014-OL-scheme-p007-i0', 'maths-2014-ol-p1-q1-b': 'maths-2014-OL-scheme-p007-i1', 'maths-2014-ol-p1-q1-c': 'maths-2014-OL-scheme-p007-i2', 'maths-2014-ol-p1-q2-a-i': 'maths-2014-OL-scheme-p008-i0', 'maths-2014-ol-p1-q2-a-ii': 'maths-2014-OL-scheme-p008-i1', 'maths-2014-ol-p1-q2-a-iii': 'maths-2014-OL-scheme-p008-i2', 'maths-2014-ol-p1-q2-b': 'maths-2014-OL-scheme-p008-i3', 'maths-2014-ol-p1-q3-a-i': 'maths-2014-OL-scheme-p009-i0', 'maths-2014-ol-p1-q3-a-ii': 'maths-2014-OL-scheme-p009-i1', 'maths-2014-ol-p1-q3-b': 'maths-2014-OL-scheme-p009-i2', 'maths-2014-ol-p1-q4-a': 'maths-2014-OL-scheme-p010-i0', 'maths-2014-ol-p1-q4-b': 'maths-2014-OL-scheme-p010-i1', 'maths-2014-ol-p1-q4-c-i': 'maths-2014-OL-scheme-p011-i0', 'maths-2014-ol-p1-q5-a-i': 'maths-2014-OL-scheme-p012-i0', 'maths-2014-ol-p1-q5-b': 'maths-2014-OL-scheme-p012-i1', 'maths-2014-ol-p1-q5-c': 'maths-2014-OL-scheme-p012-i2', 'maths-2014-ol-p1-q6-a-i': 'maths-2014-OL-scheme-p013-i0', 'maths-2014-ol-p1-q6-a-ii': 'maths-2014-OL-scheme-p013-i1', 'maths-2014-ol-p1-q6-b-i': 'maths-2014-OL-scheme-p013-i2', 'maths-2014-ol-p1-q6-b-ii': 'maths-2014-OL-scheme-p013-i3', 'maths-2014-ol-p1-q7-a': 'maths-2014-OL-scheme-p014-i0', 'maths-2014-ol-p1-q7-b-i': 'maths-2014-OL-scheme-p014-i1', 'maths-2014-ol-p1-q7-b-ii': 'maths-2014-OL-scheme-p015-i0', 'maths-2014-ol-p1-q7-b-iii': 'maths-2014-OL-scheme-p015-i1', 'maths-2014-ol-p1-q8-a': 'maths-2014-OL-scheme-p016-i0', 'maths-2014-ol-p1-q8-b': 'maths-2014-OL-scheme-p016-i1', 'maths-2014-ol-p1-q8-c': 'maths-2014-OL-scheme-p016-i2', 'maths-2014-ol-p1-q8-d': 'maths-2014-OL-scheme-p017-i0', 'maths-2014-ol-p1-q8-e': 'maths-2014-OL-scheme-p017-i1', 'maths-2014-ol-p1-q9-a': 'maths-2014-OL-scheme-p018-i0', 'maths-2014-ol-p1-q9-b': 'maths-2014-OL-scheme-p018-i1', 'maths-2014-ol-p1-q9-c-i': 'maths-2014-OL-scheme-p019-i0', 'maths-2014-ol-p1-q9-c-ii': 'maths-2014-OL-scheme-p019-i1', 'maths-2014-ol-p1-q9-c-iii': 'maths-2014-OL-scheme-p019-i2', 'maths-2014-ol-p1-q9-d-i': 'maths-2014-OL-scheme-p019-i3', 'maths-2014-ol-p1-q9-e-i': 'maths-2014-OL-scheme-p020-i0', 'maths-2014-ol-p1-q9-e-ii': 'maths-2014-OL-scheme-p020-i1', 'maths-2014-ol-p1-q9-e-iii': 'maths-2014-OL-scheme-p020-i2', 'maths-2014-ol-p1-q9-f': 'maths-2014-OL-scheme-p020-i3'}
p = Paper(2014,'ol','p1',{'5A':[0,5],'5B':[0,2,5],'5C':[0,2,3,5],'10B':[0,5,10],'10C':[0,3,7,10],'10D':[0,3,5,8,10],'15C':[0,5,10,15]},'LC003GLP130EV.pdf','LC003GLP000EV.pdf',reviewed_at='2026-10-29')
A=p.A
fm='financial-maths'
shop='A shopkeeper bought 25 school blazers at €30 each and 25 trousers at €20 each.'
A('1-a','Q1(a)','10C',[7,23],[3],'3-3',fm,'Find the total cost to the shopkeeper.',stem=shop)
A('1-b','Q1(b)','5B',[7,23],[3],'3-3',fm,'The shopkeeper sells a blazer and a trousers as a set for €89·95. Find her profit on this transaction.',stem=shop)
A('1-c','Q1(c)','10D',[7,23],[3],'3-3',fm,'The shopkeeper sells 22 blazer and trouser sets at €89·95 each. She sells the remaining 3 sets at a discount of 20% on the selling price. Find her mark up (profit as a percentage of cost price) on the total transaction.',stem=shop)
z='Let z₁ = 5 − i and z₂ = 4 + 3i, where i² = −1.'
A('2-a-i','Q2(a)(i)','10C',[8,24],[4],'4-4','complex-numbers','Find z₁ − z₂.',stem=z)
A('2-a-ii','Q2(a)(ii)','5C',[8,24],[4],'4-4','complex-numbers','Verify that |z₁ − z₂| = |z₂ − z₁|.',stem=z)
A('2-a-iii','Q2(a)(iii)','5B',[8,24],[4],'4-4','complex-numbers','Give a reason why |z − w| = |w − z| will always be true, for any complex numbers z and w.')
A('2-b','Q2(b)','5C',[8,24],[4],'4-4','complex-numbers','Find a complex number z₃ such that z₁ = z₂/z₃. Give your answer in the form a + bi, where a, b ∈ ℝ.',stem=z)
q3='Solve for x: 2(4 − 3x) + 12 = 7x − 5(2x − 7).'
A('3-a-i','Q3(a)(i)','10C',[9,25],[5],'4-2','algebra-equations',q3)
A('3-a-ii','Q3(a)(ii)','5B',[9,25],[5],'4-2','algebra-equations','Verify your answer to (i) above.',stem='Part (a)(i): '+q3)
A('3-b','Q3(b)','10D',[9,25],[5],'4-2','algebra-equations','Solve the simultaneous equations: x + y = 7; x² + y² = 25.')
A('4-a','Q4(a)','15C',[10,26],[6],'4-2','algebra-equations','Solve the equation x² − x − 6 = 0.')
A('4-b','Q4(b)','5A',[10,26],[6],'5-1','functions','The graphs of four quadratic functions are shown below. Which of the graphs above is that of the function f: x ↦ x² − x − 6, where x ∈ ℝ?')
A('4-c-i','Q4(c)(i),Q4(c)(ii)','5C',[11,26],[7],'5-1','functions','The graph of g(x) = x² − 2x, where x ∈ ℝ, is shown on the diagram below. On the same diagram, sketch the graph of each of the functions: (i) h(x) = g(x) + 2. (ii) k(x) = g(x + 2). Label each sketch clearly.')
f='The function f is defined as f: x ↦ x³ + 3x² − 9x + 5, where x ∈ ℝ.'
q5a='(i) Find the co-ordinates of the point where the graph of f cuts the y-axis. (ii) Verify that the graph of f cuts the x-axis at x = −5.'
q5b='Find the co-ordinates of the local maximum turning point and of the local minimum turning point of f.'
A('5-a-i','Q5(a)(i),Q5(a)(ii)','10C',[12,27],[8],'5-1','functions',q5a,stem=f)
A('5-b','Q5(b)','10D',[12,27],[8],'5-2','differentiation',q5b,stem=f)
A('5-c','Q5(c)','5C',[12,27],[8],'5-1','functions','Hence, sketch the graph of the function f on the axes below.',stem=f+' Part (a): '+q5a+' Part (b): '+q5b)
seq='The general term of an arithmetic sequence is Tₙ = 15 − 2n, where n ∈ ℕ.'
A('6-a-i','Q6(a)(i)','10C',[13,28],[9],'4-1','sequences-series','Write down the first three terms of the sequence.',stem=seq)
A('6-a-ii','Q6(a)(ii)','5C',[13,28],[9],'4-1','sequences-series','Find the first negative term of the sequence.',stem=seq)
q6bi='Find Sₙ = T₁ + T₂ + ⋯ + Tₙ, the sum of the first n terms of the series, in terms of n.'
A('6-b-i','Q6(b)(i)','5C',[13,28],[9],'4-1','sequences-series',q6bi,stem=seq)
A('6-b-ii','Q6(b)(ii)','5C',[13,28],[9],'4-1','sequences-series','Find the value of n for which the sum of the first n terms of the series is 0.',stem=seq+' Part (b)(i): '+q6bi)
A('7-a','Q7(a)','10C',[14,29],[10],'3-3',fm,'Mary bought a new car for €20 000 on the 1st July 2010. The value of the car depreciated at a compound rate of 15% each year. Find the value of the car, correct to the nearest euro, on the 1st July 2014.')
car='Mary wishes to buy a new car, which costs €24 000, on the 1st July 2014.'
q7bi='Buy Right Car Sales offers Mary €10 500 for her old car. She can borrow the balance for one year at a rate of 11·5%. How much would she repay on 1st July 2015?'
q7bii='Bargain Deals Car Sales offers Mary €10 000 for her old car and an interest free loan of the balance for six months. At the end of the six months Mary would make a payment of €4000 and would be charged interest at a compound rate of 1·5% per month for the next six months. How much would Mary repay on 1st July 2015?'
A('7-b-i','Q7(b)(i)','10C',[14,29],[10],'3-3',fm,q7bi,stem=car)
A('7-b-ii','Q7(b)(ii)','5C',[15,29],[10,11],'3-3',fm,q7bii,stem=car)
A('7-b-iii','Q7(b)(iii)','10B',[15,29],[10,11],'3-3',fm,'Which of the above options should Mary choose if she wishes to pay the least amount? Justify your answer by calculation.',stem=car+' Option (i): '+q7bi+' Option (ii): '+q7bii)
A('8-a','Q8(a)','5B',[16,30],[12],'3-4','area-volume','The length of the side of a square sheet of cardboard is 12 cm. Find the area of the sheet.')
box='The diagram below shows a square sheet of cardboard of side length 12 cm, from which four small squares, each of side length h, have been removed. The sheet can be folded to form an open rectangular box of height h.'
q8c='Show that the volume of the box, in terms of h, is 4h³ − 48h² + 144h.'
q8d='Find the value of h which gives the maximum volume of the box.'
A('8-b','Q8(b)','10C',[16,30],[12],'3-4','area-volume','Write the length and the width of the box in terms of h.',stem=box)
A('8-c','Q8(c)','10C',[16,30],[12],'3-4','area-volume,algebra',q8c,stem=box)
A('8-d','Q8(d)','10D',[17,30],[12,13],'5-2','differentiation,area-volume',q8d,stem=box+' Part (c): '+q8c)
A('8-e','Q8(e)','5B',[17,30],[12,13],'3-4','area-volume,differentiation','Find the maximum volume of the box.',stem=box+' Part (c): '+q8c+' Part (d): '+q8d)
rocket='A small rocket is fired into the air from a fixed position on the ground. Its flight lasts ten seconds. The height, in metres, of the rocket above the ground after t seconds is given by h = 10t − t².'
q9a='Complete the table below. Time, t: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10. Height, h: _, _, _, _, _, 25, 24, 21, 16, _, _.'
q9b='Draw a graph to represent the height of the rocket during the ten seconds.'
A('9-a','Q9(a)','15C',[18,31],[14],'5-1','functions',q9a,stem=rocket)
A('9-b','Q9(b)','15C',[18,31],[14],'5-1','functions',q9b,stem=rocket+' Part (a): '+q9a)
A('9-c-i','Q9(c)(i)','5B',[18,19,31],[14,15],'5-1','functions','Use your graph to estimate the height of the rocket after 2·5 seconds.',stem=rocket+' Part (b): '+q9b)
A('9-c-ii','Q9(c)(ii)','5B',[18,19,31],[14,15],'5-1','functions','Use your graph to estimate the time when the rocket will again be at this height.',stem=rocket+' Part (b): '+q9b+' Part (c)(i): Use your graph to estimate the height of the rocket after 2·5 seconds.')
A('9-c-iii','Q9(c)(iii)','5B',[18,19,31],[14,15],'5-1','functions','Use your graph to estimate the co-ordinates of the highest point reached by the rocket.',stem=rocket+' Part (b): '+q9b)
A('9-d-i','Q9(d)(i),Q9(d)(ii)','10D',[19,31],[14,15],'5-1','functions,co-ordinate-geometry-of-the-line','(i) Find the slope of the line joining the points (6, 24) and (7, 21). (ii) Would you expect the line joining the points (7, 21) and (8, 16) to be steeper than the line joining (6, 24) and (7, 21) or not? Give a reason for your answer.',stem=rocket)
A('9-e-i','Q9(e)(i)','5B',[20,32],[14,16],'5-2','differentiation','Find dh/dt.',stem=rocket)
A('9-e-ii','Q9(e)(ii)','5C',[20,32],[14,16],'5-2','differentiation','Hence, find the maximum height reached by the rocket.',stem=rocket+' Part (e)(i): Find dh/dt.')
A('9-e-iii','Q9(e)(iii)','5B',[20,32],[14,16],'5-2','differentiation','Find the speed of the rocket after 3 seconds.',stem=rocket)
A('9-f','Q9(f)','5C',[20,32],[14,16],'5-2','differentiation','Find the co-ordinates of the point at which the slope of the tangent to the graph is 2.',stem=rocket)
marks={'1':25,'2':25,'3':25,'4':25,'5':25,'6':25,'7':35,'8':40,'9':75}
p.check(marks,39)
p.review(marks,
 'Independent visual inspection of all 20 original question-paper pages and all scheme PDF pages 1–32: models 7–20, scales/allocation 21–22, detailed notes 23–32. Every printed task was cross-checked against the detailed marking boundaries.',
 list(range(1,33)),[21,22,23],
 ['All nine questions are compulsory; all 300 marks and 39 scale units retained.',
  'Q4(c)(i)+(ii), Q5(a)(i)+(ii) and Q9(d)(i)+(ii) remain one card per published shared scale.',
  'Q4(c) is 5C in the detailed notes (PDF 26), but 10C in the summary (PDF 22). The card follows detailed notes, giving Q4 its printed 25 marks (15+5+5), not 30. Original sources retained and separately labelled disclosure shown after reveal.',
  'Paper 1 credit ladders: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,3,5,8,10; 15C 0,5,10,15. General full-credit-minus-one rule applies. Rounding/units deductions apply once per lettered section.',
  'Q6(a)(i) detailed notes omit the parent (a) and truncate Scale; its identity is confirmed against paper, model and allocation table. Q9(c) shared tolerance ±½ unit applies to each graph-reading card.',
  'Full question diagrams, graphs, tables and earlier required prompts accompany dependent tasks without inserting answers. Typeset solutions and all detailed notes carry mathematical notation that the PDF text layer scrambles.',
  'Scheme printed pages are PDF positions minus 2. All 39 cards are new; no existing task IDs are replaced.'],
 [{'pages':[2,3,10],'wording':'Answer all nine / all six / all three questions','classification':'all-questions-required','reason':'Every question and published scale unit retained.'},
  {'pages':[11],'wording':'Which of the above options should Mary choose','classification':'compare-given-options','reason':'One separately marked comparison of both loan offers, not a choice of exam tasks.'},
  {'pages':[15],'wording':'steeper ... or not','classification':'binary-conclusion-with-reason','reason':'Both possible conclusions belong to one required reasoning task, not selectable prompts.'}],
 lambda t: ('all-questions-required','All questions and all published scale units retained.') if 'Answer all' in t else ('compare-given-options','One required comparison of both loan offers.') if 'choose' in t.lower() else ('binary-conclusion-with-reason','One required conclusion and reason, not a choice of tasks.') if 'or not' in t else None)
p.apply(ROWS,'2014 Ordinary Level Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
