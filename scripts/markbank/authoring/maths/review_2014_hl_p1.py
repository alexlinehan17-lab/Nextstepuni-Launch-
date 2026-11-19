"""2014 Higher Paper 1 (Project Maths): 34 published scales, 300 marks."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *

R = {
 '1-a':[L(LPC,'Only one value verified'),L(LPC,'Recognising one factor'),L(HPC,'Two relevant roots tested')],
 '1-b-i':[L(LPC,'Cubic equation not factorised'),L(HPC,'Roots identified')],
 '1-b-ii':[L(LPC,'Only one point indicated on graph'),L(HPC,'Two points identified'),L(HPC,'Two points plotted but no graph drawn')],
 '2-a':[L(LPC,'Identifies another root'),L(LPC,'Forms an equation'),L(MPC,'Works with correct quadratic factor'),L(HPC,'Finds third factor')],
 '2-b-i':[L(LPC,'Plots one point correctly'),L(HPC,'Points plotted but not labelled or labelled incorrectly'),L(HPC,'Two points plotted and labelled')],
 '2-b-ii':[L(LPC,'Length of any one side of triangle calculated correctly'),L(LPC,'Correct definition of trig ratio'),L(LPC,'Correct cos rule'),L(HPC,'cos value calculated but angle not found')],
 '3-a':[L(LPC,'One correct step in induction'),L(MPC,'Some work with'),L(HPC,'Correct RHS'),L(HPC,'No conclusion')],
 '3-b':[L(LPC,'Recognising 2 as common factor'),L(MPC,'Correct equation from (a)'),L(MPC,'Taking 2 out of series'),L(HPC,'Work not completed'),L(LPC,'Correct AP formula only'),L(HPC,'Work not fully simplified'),L(HPC,'Answer not in required form')],
 '3-c':[L(PC,'Use of correct series from (b)')],
 '4-a':[L(MPC,'RHS only')],
 '4-b':[L(MPC,'correct but not simplified'),L(HPC,'Correct values of x from students work')],
 '5-a':[L(PC,'Some correct integration'),L(PC,'Integrand does not contain c'),L(PC,'c only')],
 '5-b-i':[L(LPC,'Some correct integration'),L(LPC,'Integrand does not contain c'),L(LPC,'c only'),L(HPC,'Substitutes (−2, 0) but c not simplified')],
 '5-b-ii':[L(LPC,'Correct formula only'),L(LPC,'Some correct integration'),L(LPC,'Indication of integration with correct limits'),L(HPC,'Limits inserted into function but not calculated'),L(NOTE,'NO CREDIT – differentiation'),L(NOTE,'NO CREDIT – no integration')],
 '6-a-i':[L(NOTE,'When particular values are used in ALL sections give Low Partial Credit at most each time'),L(LPC,'Only one term correct')],
 '6-a-ii':[L(NOTE,'When particular values are used in ALL sections give Low Partial Credit at most each time'),L(LPC,'Uses two consecutive general terms'),L(LPC,'Recognition of common difference and no more'),L(HPC,'Shows series arithmetic but does not state common difference')],
 '6-b':[L(NOTE,'When particular values are used in ALL sections give Low Partial Credit at most each time'),L(LPC,'Correct AP formula stated'),L(HPC,'Correct substitution into formula')],
 '6-c':[L(NOTE,'When particular values are used in ALL sections give Low Partial Credit at most each time'),L(NOTE,'log is not needed in first solution box')],
 '7-a-i':[L(PC,'Correct substitution of chosen value'),L(PC,'Not squaring values'),L(NOTE,'Mark particular case with scheme for (a)(i) wherever it occurs'),L(NOTE,'Mark general case with scheme for (a)(ii) wherever it occurs')],
 '7-a-ii':[L(MPC,'Any two terms'),L(HPC,'Three terms fully squared'),L(NOTE,'Mark particular case with scheme for (a)(i) wherever it occurs'),L(NOTE,'Mark general case with scheme for (a)(ii) wherever it occurs')],
 '7-b-i':[L(LPC,'Any appropriate construction line'),L(MPC,'Correct expression of two sides in terms of x'),L(HPC,'Correct expression of three sides in terms of x'),L(HPC,'Correct expression of function in x not simplified')],
 '7-b-ii':[L(LPC,'Any correct differentiation'),L(HPC,'Finding value of x'),L(LPC,'3 as factor')],
 '8-a':[L(LPC,'Any correct differentiation')],
 '8-b':[L(HPC,'Values in quadratic formula'),L(HPC,'Gets x values only')],
 '8-c':[L(LPC,'Any area formula'),L(LPC,'Area under curve from A to B'),L(LPC,'Area under curve from D to E'),L(LPC,'Correct limits'),L(MPC,'Any correct integration'),L(MPC,'One correct area only'),L(HPC,'Both areas'),L(MPC,'Translation')],
 '8-d':[L(LPC,'Attempt at equating like to like'),L(LPC,'Attempt at completing square'),L(HPC,'Values of two of the constants found')],
 '8-e':[L(PC,'One correct value for the equivalent of k, p or h in equation')],
 '9-a':[L(LPC,'Value of y only'),L(LPC,'Some use of 100 and/or 23'),L(HPC,'Correct substitution into equation'),L(HPC,'A calculated from incorrect y')],
 '9-b':[L(LPC,'Value of y only'),L(LPC,'Some use of 88 and/or 23'),L(HPC,'Correct expression for k'),L(HPC,'k calculated from incorrect y')],
 '9-c':[L(LPC,'Value of y only'),L(HPC,'Correct expression for t'),L(HPC,'t calculated from incorrect y')],
 '9-d':[L(LPC,'Any one point identified'),L(LPC,'Graph of correct shape, even if no point correct or no point calculated'),L(LPC,'Accept candidates value of k'),L(HPC,'Three points correctly plotted, but graph incomplete or no graph'),L(NOTE,'do not accept straight line graph')],
 '9-e-i':[L(LPC,'Any attempt at similar graph'),L(LPC,'No graph but correct deduction'),L(HPC,'Correct graph plotted but graph incomplete, or no graph')],
 '9-f-i':[L(LPC,'Treats e as x in differentiation')],
 '9-f-ii':[L(LPC,'Attempt at deduction from numerical values')],
}
ROWS={'maths-2014-hl-p1-q'+k:v for k,v in R.items()}
if len(sys.argv)>1: quotes(ROWS,sys.argv[1]);raise SystemExit
p=Paper(2014,'hl','p1',{'5B':[0,3,5],'5C':[0,3,4,5],'5D':[0,2,3,4,5],'10B':[0,5,10],'10C':[0,5,7,10],'10D':[0,3,7,8,10],'15C':[0,7,10,15],'15D':[0,5,9,12,15]},'LC003ALP130EV.pdf','LC003ALP000EV.pdf',reviewed_at='2026-10-29')
A=p.A
cubic='The graph of a cubic function f(x) cuts the x-axis at x = −3, x = −1 and x = 2, and the y-axis at (0, −6), as shown.'
q1a='Verify that f(x) can be written as f(x) = x³ + 2x² − 5x − 6.'
A('1-a','Q1(a)','15C',[7,30],[3],'4-2','algebra-cubics,functions',q1a,stem=cubic)
A('1-b-i','Q1(b)(i)','5C',[8,30],[3],'4-2','algebra-cubics,functions','The graph of the function g(x) = −2x − 6 intersects the graph of the function f(x) above. Let f(x) = g(x) and solve the resulting equation to find the co-ordinates of the points where the graphs of f(x) and g(x) intersect.',stem=cubic+' '+q1a)
A('1-b-ii','Q1(b)(ii)','5C',[7,8,30],[3],'5-1','functions','Draw the graph of the function g(x) = −2x − 6 on the diagram above.',stem=cubic+' '+q1a)
z='Let z₁ = 1 − 2i, where i² = −1.'
q2bi='Let w = z₁conjugate(z₁), where conjugate(z₁) is the conjugate of z₁. Plot z₁, conjugate(z₁) and w on the Argand diagram and label each point.'
A('2-a','Q2(a)','5D',[9,31],[4],'4-4','complex-numbers,algebra-cubics','The complex number z₁ is a root of the equation 2z³ − 7z² + 16z − 15 = 0. Find the other two roots of the equation.',stem=z)
A('2-b-i','Q2(b)(i)','10C',[9,31],[4],'4-4','complex-numbers',q2bi,stem=z)
A('2-b-ii','Q2(b)(ii)','10C',[10,31],[4],'4-4','complex-numbers,trigonometry-triangles','Find the measure of the acute angle, conjugate(z₁)wz₁, formed by joining conjugate(z₁) to w to z₁ on the diagram above. Give your answer correct to the nearest degree.',stem=z+' Part (b)(i): '+q2bi)
q3a='Prove, by induction, that the sum of the first n natural numbers, 1 + 2 + 3 + ⋯ + n, is n(n + 1)/2.'
q3b='Hence, or otherwise, prove that the sum of the first n even natural numbers, 2 + 4 + 6 + ⋯ + 2n, is n² + n.'
A('3-a','Q3(a)','10D',[11,32],[5],'4-1','induction,sequences-series',q3a)
A('3-b','Q3(b)','10D',[11,32],[5],'4-1','sequences-series,induction',q3b,stem='Part (a): '+q3a)
A('3-c','Q3(c)','5B',[12,32],[5],'4-1','sequences-series','Using the results from (a) and (b) above, find an expression for the sum of the first n odd natural numbers in its simplest form.',stem='Part (a): '+q3a+' Part (b): '+q3b)
A('4-a','Q4(a)','15D',[13,33],[6],'5-2','differentiation-rules','Differentiate the function 2x² − 3x − 6 with respect to x from first principles.')
A('4-b','Q4(b)','10D',[13,33],[6],'5-2','differentiation-applications,differentiation-rules','Let f(x) = 2x/(x + 2), x ≠ −2, x ∈ ℝ. Find the co-ordinates of the points at which the slope of the tangent to the curve y = f(x) is 1/4.')
curve='The slope of the tangent to a curve y = f(x) at each point (x, y) is 2x − 2. The curve cuts the x-axis at (−2, 0).'
A('5-a','Q5(a)','5B',[14,34],[7],'5-2','integration','Find ∫ 5 cos 3x dx.')
A('5-b-i','Q5(b)(i)','10C',[14,34],[7],'5-2','integration','Find the equation of f(x).',stem=curve)
A('5-b-ii','Q5(b)(ii)','10C',[14,34],[7],'5-2','integration','Find the average value of f over the interval 0 ≤ x ≤ 3, x ∈ ℝ.',stem=curve+' Part (b)(i): Find the equation of f(x).')
seq='The nth term of a sequence is Tₙ = ln aⁿ, where a > 0 and a is a constant.'
A('6-a-i','Q6(a)(i)','10C',[15,35],[8],'4-1','sequences-series,indices-and-logs','Show that T₁, T₂ and T₃ are in arithmetic sequence.',stem=seq)
A('6-a-ii','Q6(a)(ii)','5C',[15,35],[8],'4-1','sequences-series,indices-and-logs','Prove that the sequence is arithmetic and find the common difference.',stem=seq)
A('6-b','Q6(b)','5C',[15,35],[8],'4-1','sequences-series,indices-and-logs','Find the value of a for which T₁ + T₂ + T₃ + ⋯ + T₉₈ + T₉₉ + T₁₀₀ = 10 100.',stem=seq)
A('6-c','Q6(c)','5C',[16,35],[8,9],'4-1','sequences-series','Verify that, for all values of a, (T₁ + T₂ + T₃ + ⋯ + T₁₀) + 100d = (T₁₁ + T₁₂ + T₁₃ + ⋯ + T₂₀), where d is the common difference of the sequence.',stem=seq)
triple='Three natural numbers a, b and c, such that a² + b² = c², are called a Pythagorean triple.'
A('7-a-i','Q7(a)(i)','10B',[17,36],[10],'4-1','algebra-expressions-factorising','Let a = 2n + 1, b = 2n² + 2n and c = 2n² + 2n + 1. Pick one natural number n and verify that the corresponding values of a, b and c form a Pythagorean triple.',stem=triple)
A('7-a-ii','Q7(a)(ii)','10D',[17,36],[10],'4-1','algebra-expressions-factorising','Prove that a = 2n + 1, b = 2n² + 2n and c = 2n² + 2n + 1, where n ∈ ℕ, will always form a Pythagorean triple.',stem=triple)
rect='ADEC is a rectangle with |AC| = 7 m and |AD| = 2 m, as shown. B is a point on [AC] such that |AB| = 5 m. P is a point on [DE] such that |DP| = x m.'
q7bi='Let f(x) = |PA|² + |PB|² + |PC|². Show that f(x) = 3x² − 24x + 86, for 0 ≤ x ≤ 7, x ∈ ℝ.'
A('7-b-i','Q7(b)(i)','5D',[18,36],[11],'4-1','algebra-expressions-factorising,geometry',q7bi,stem=rect)
A('7-b-ii','Q7(b)(ii)','15C',[19,36],[11],'5-2','differentiation-applications,algebra-quadratics','The function f(x) has a minimum value at x = k. Find the value of k and the minimum value of f(x).',stem=rect+' Part (b)(i): '+q7bi)
bridge='In 2011, a new footbridge was opened at Mizen Head, the most south-westerly point of Ireland. The arch of the bridge is in the shape of a parabola, as shown. The length of the span of the arch, [AB], is 48 metres.'
q8a='Using the co-ordinate plane, with A(0, 0) and B(48, 0), the equation of the parabola is y = −0·013x² + 0·624x. Find the co-ordinates of C, the highest point of the arch.'
q8b='The perpendicular distance between the walking deck, [DE], and [AB] is 5 metres. Find the co-ordinates of D and of E. Give your answers correct to the nearest whole number.'
q8d='Write the equation of the parabola in part (a) in the form y − k = p(x − h)², where k, p, and h are constants.'
A('8-a','Q8(a)','15C',[20,37],[12],'5-2','differentiation-applications,algebra-quadratics',q8a,stem=bridge)
A('8-b','Q8(b)','10C',[21,37],[12],'4-2','algebra-quadratics',q8b,stem=bridge+' Part (a): '+q8a)
A('8-c','Q8(c)','10D',[22,23,37],[12,13],'5-2','integration','Using integration, find the area of the shaded region, ABED, shown in the diagram below. Give your answer correct to the nearest whole number.',stem=bridge+' Part (a): '+q8a+' Part (b): '+q8b)
A('8-d','Q8(d)','10C',[24,38],[12,13],'4-2','algebra-quadratics',q8d,stem=bridge+' Part (a): '+q8a)
A('8-e','Q8(e)','5B',[24,38],[13],'4-2','algebra-quadratics','Using what you learned in part (d) above, or otherwise, write down the equation of a parabola for which the coefficient of x² is −2 and the co-ordinates of the maximum point are (3, −4).',stem='Part (d): '+q8d)
water='Ciarán is preparing food for his baby and must use cooled boiled water. The equation y = Ae^(kt) describes how the boiled water cools. In this equation: t is the time, in minutes, from when the water boiled; y is the difference between the water temperature and room temperature at time t, measured in degrees Celsius; A and k are constants. The temperature of the water when it boils is 100°C and the room temperature is a constant 23°C.'
q9a='Write down the value of the temperature difference, y, when the water boils and find the value of A.'
q9b='After five minutes, the temperature of the water is 88°C. Find the value of k, correct to three significant figures.'
q9d='Using your values for A and k, sketch the curve f(t) = Ae^(kt) for 0 ≤ t ≤ 100, t ∈ ℝ.'
A('9-a','Q9(a)','10C',[25,39],[14],'5-1','functions,indices-and-logs',q9a,stem=water)
A('9-b','Q9(b)','10C',[25,39],[14],'3-2','indices-and-logs',q9b,stem=water+' Part (a): '+q9a)
A('9-c','Q9(c)','10C',[25,39],[14],'3-2','indices-and-logs','Ciarán prepares the food for his baby when the water has cooled to 50°C. How long does it take, correct to the nearest minute, for the water to cool to this temperature?',stem=water+' Part (a): '+q9a+' Part (b): '+q9b)
A('9-d','Q9(d)','15C',[26,39],[14,15],'5-1','functions',q9d,stem=water+' Part (a): '+q9a+' Part (b): '+q9b)
A('9-e-i','Q9(e)(i),Q9(e)(ii)','5C',[26,27,40],[14,15],'5-1','functions','(i) On the same diagram, sketch a curve g(t) = Ae^(mt), showing the water cooling at a faster rate, where A is the value from part (a), and m is a constant. Label each graph clearly. (ii) Suggest one possible value for m for the sketch you have drawn and give a reason for your choice.',stem=water+' Part (a): '+q9a+' Part (b): '+q9b+' Part (d): '+q9d)
A('9-f-i','Q9(f)(i)','5C',[27,40],[14,15,16],'5-2','differentiation-applications','Find the rates of change of the function f(t) after 1 minute and after 10 minutes. Give your answers correct to two decimal places.',stem=water+' Part (a): '+q9a+' Part (b): '+q9b+' Part (d): '+q9d)
A('9-f-ii','Q9(f)(ii)','5C',[27,40],[14,15,16],'5-2','differentiation-applications','Show that the rate of change of f(t) will always increase over time.',stem=water+' Part (a): '+q9a+' Part (b): '+q9b+' Part (d): '+q9d)
marks={'1':25,'2':25,'3':25,'4':25,'5':25,'6':25,'7':40,'8':50,'9':60}
p.check(marks,34)
p.review(marks,'Independent visual review of all 20 original question pages and scheme PDF pages 1–41, including all Paper 1 model solutions, every credit note, the scale table and allocation summary. All printed parts reconciled against 300 marks.',list(range(1,42)),[28,29],
 ['All nine questions are compulsory; 34 official marking boundaries cover all 300 marks.',
  'Q9(e)(i)+(ii) share one 5C scale. Every other printed subpart has its own published scale. Alternative solution methods remain within their one card.',
  'The 2014 credit ladders are taken from this Paper 1 scheme: 10C uses 0,5,7,10; 10D uses 0,3,7,8,10; 15C uses 0,7,10,15; 15D uses 0,5,9,12,15.',
  'Dependent cards retain the original graph, diagram, equation and earlier prompts. Question 6 uses the general-case restriction from the notes on each card. Question 7(a) preserves the shared instruction to mark particular/general work wherever it occurs.',
  'Q7(a)(i) asks the student to choose a natural number within the mathematical problem, not to choose an examination question. Hence/or otherwise wording offers a method, not an alternative task.',
  'Question source file LC003ALP130EV is the indexed Project Maths edition. Printed scheme page numbers are two less than PDF positions. Mathematical working and all credit notes are presented as original typeset source images.'],
 [{'pages':[2,3,10],'wording':'Answer all nine / six / three questions','classification':'all-questions-required','reason':'Every task is retained.'},
  {'pages':[5,13],'wording':'Hence, or otherwise / Using what you learned ... or otherwise','classification':'alternative-method','reason':'These are alternative methods for the same marked task.'},
  {'pages':[10],'wording':'Pick one natural number','classification':'mathematical-example','reason':'The selected number is part of the proof task, not exam-task choice.'}],
 lambda t:('all-questions-required','Every printed task is retained.') if 'Answer all' in t else ('alternative-method','Alternative methods for one marked task.') if 'or otherwise' in t else None)
SCHEME_ROW_FIGURES = {'maths-2014-hl-p1-q1-a': 'maths-2014-HL-scheme-p007-i0', 'maths-2014-hl-p1-q1-b-i': 'maths-2014-HL-scheme-p008-i0', 'maths-2014-hl-p1-q1-b-ii': 'maths-2014-HL-scheme-p008-i1', 'maths-2014-hl-p1-q2-a': 'maths-2014-HL-scheme-p009-i0', 'maths-2014-hl-p1-q2-b-i': 'maths-2014-HL-scheme-p009-i1', 'maths-2014-hl-p1-q2-b-ii': 'maths-2014-HL-scheme-p010-i0', 'maths-2014-hl-p1-q3-a': 'maths-2014-HL-scheme-p011-i0', 'maths-2014-hl-p1-q3-b': 'maths-2014-HL-scheme-p011-i1', 'maths-2014-hl-p1-q3-c': 'maths-2014-HL-scheme-p012-i0', 'maths-2014-hl-p1-q4-a': 'maths-2014-HL-scheme-p013-i0', 'maths-2014-hl-p1-q4-b': 'maths-2014-HL-scheme-p013-i1', 'maths-2014-hl-p1-q5-a': 'maths-2014-HL-scheme-p014-i0', 'maths-2014-hl-p1-q5-b-i': 'maths-2014-HL-scheme-p014-i1', 'maths-2014-hl-p1-q5-b-ii': 'maths-2014-HL-scheme-p014-i2', 'maths-2014-hl-p1-q6-a-i': 'maths-2014-HL-scheme-p015-i0', 'maths-2014-hl-p1-q6-a-ii': 'maths-2014-HL-scheme-p015-i1', 'maths-2014-hl-p1-q6-b': 'maths-2014-HL-scheme-p015-i2', 'maths-2014-hl-p1-q6-c': 'maths-2014-HL-scheme-p016-i0', 'maths-2014-hl-p1-q7-a-i': 'maths-2014-HL-scheme-p017-i0', 'maths-2014-hl-p1-q7-a-ii': 'maths-2014-HL-scheme-p017-i1', 'maths-2014-hl-p1-q7-b-i': 'maths-2014-HL-scheme-p018-i0', 'maths-2014-hl-p1-q7-b-ii': 'maths-2014-HL-scheme-p019-i0', 'maths-2014-hl-p1-q8-a': 'maths-2014-HL-scheme-p020-i0', 'maths-2014-hl-p1-q8-b': 'maths-2014-HL-scheme-p021-i0', 'maths-2014-hl-p1-q8-c': 'maths-2014-HL-scheme-p022-i0', 'maths-2014-hl-p1-q8-d': 'maths-2014-HL-scheme-p024-i0', 'maths-2014-hl-p1-q8-e': 'maths-2014-HL-scheme-p024-i1', 'maths-2014-hl-p1-q9-a': 'maths-2014-HL-scheme-p025-i0', 'maths-2014-hl-p1-q9-b': 'maths-2014-HL-scheme-p025-i1', 'maths-2014-hl-p1-q9-c': 'maths-2014-HL-scheme-p025-i2', 'maths-2014-hl-p1-q9-d': 'maths-2014-HL-scheme-p026-i0', 'maths-2014-hl-p1-q9-e-i': 'maths-2014-HL-scheme-p027-i0', 'maths-2014-hl-p1-q9-f-i': 'maths-2014-HL-scheme-p027-i1', 'maths-2014-hl-p1-q9-f-ii': 'maths-2014-HL-scheme-p027-i2'}
p.apply(ROWS,'2014 Higher Level Paper 1 (Project Maths)',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
