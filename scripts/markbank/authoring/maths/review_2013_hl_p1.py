"""2013 Higher Project Maths Phase 2 Paper 1: all eight questions, including old-syllabus calculus."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R={
'1-a':[L(LPC,'Does not multiply by conjugate'),L(LPC,'Incomplete cross-multiplication'),L(HPC,'Work not simplified')],
'1-b':[L(LPC,'Work with modulus'),L(LPC,'Plotting z'),L(HPC,'Correct z but incorrect or no plotting')],
'1-c':[L(LPC,'Some work with De Moivre'),L(LPC,'De Moivre not used correctly'),L(HPC,'Answer not simplified'),L(NOTE,'Allow for full marks candidates incorrect angle from (b), with correct conclusion')],
'2-a':[L(LPC,'Factorises'),L(LPC,'Gets roots'),L(HPC,'Wrong shape of graph, but otherwise correct'),L(HPC,'Correct shading on x-axis')],
'2-b':[L(LPC,'Any relevant step to solution'),L(MPC,'Reduces to two unknowns correctly in one equation'),L(HPC,'Evaluates one unknown')],
'3-a':[L(PC,'Value correctly substituted into e')],
'3-b':[L(LPC,'Correct statement'),L(LPC,'Uses logs (correctly or incorrectly)'),L(LPC,'Makes an effort to isolate t'),L(HPC,'Gets correct linear equation for t'),L(NOTE,'Incomplete rounding or incorrect rounding or no rounding gets 9 marks.')],
'4-a-i':[L(LPC,'Any relevant first step'),L(LPC,'Correct statement with no work'),L(NOTE,'Incomplete rounding or incorrect rounding or no rounding gets 4 marks.')],
'4-a-ii':[L(LPC,'Any relevant step'),L(MPC,'Recognises G.P.'),L(HPC,'Expression for sum of G.P.'),L('Alternative method, '+LPC,'No present value or incorrect present value'),L('Alternative method, '+MPC,'Present value correct'),L('Alternative method, '+HPC,'Correct substitution of all values in formula')],
'4-b':[L(LPC,'Any relevant step'),L(HPC,'Correct substitution of all values in formula'),L(HPC,'Expression for sum of G.P. in solution')],
'5-a':[L(PC,'(20−18)1000 or equivalent')],
'5-b':[L(PC,'Expression (20 − x)')],
'5-c':[L(PC,'Correct number of people and/or correct rate in terms of x')],
'5-d':[L(PC,'Some correct differentiation of a quadratic function'),L(PC,'Correct testing with incorrect deduction or no deduction'),L(PC,'Possible to get full marks without use of calculus'),L(PC,'Correct answer and no work')],
'5-e':[L(PC,'Some effort at substitution of 16 or equivalent')],
'5-f':[L(LPC,'Use of expression'),L(LPC,'Use of 25000'),L(LPC,'Some use of tables'),L(LPC,'Equation solved'),L(LPC,'Price of ticket found'),L(HPC,'Total income from sales')],
'5-g':[L(LPC,'Correct number of family tickets'),L(LPC,'Income from single tickets'),L(LPC,'Income from family tickets'),L(MPC,'Two correct linear equations for income in two unknowns'),L(HPC,'Correct value for p (single ticket)'),L(HPC,'Correct value for y (family ticket)'),L('Alternative method, '+LPC,'Correct equation'),L('Alternative method, '+MPC,'Three correct equations'),L('Alternative method, '+HPC,'One unknown calculated')],
'6-a-i':[L(PC,'Incomplete 4th line')],
'6-a-ii':[L(LPC,'One or two correct entries in empty boxes'),L(HPC,'Three correct entries in empty boxes')],
'6-b':[L(PC,'Second differences calculated')],
'6-c':[L(PC,'Recognition of series 6, 9, 12,.... or similar'),L('Alternative method, '+PC,'Second differences calculated')],
'6-d':[L(HPC,'Two correct linear equations'),L('Alternative method, '+LPC,'Recognition of A.P.')],
'6-e':[L(LPC,'Expression of un in one variable only'),L(LPC,'Quadratic equation'),L(HPC,'Values of n')],
'7-a':[L(HPC,'Correct formula and full differentiation')],
'7-b-i':[L(HPC,'unsimplified')],
'7-b-ii':[L(LPC,'Value of t'),L(LPC,'Equation of tangent only with no substitution'),L(MPC,'Value of y'),L(MPC,'Value of slope'),L(HPC,'All values necessary for substitution')],
'7-c-i':[L(LPC,'Correct value of sin y'),L(LPC,'Correct value of cos y'),L(HPC,'Correct differentiation of correct function')],
'7-c-ii':[L(LPC,'Some correct differentiation')],
'8-a':[L(LPC,'Some correct integration'),L(HPC,'Correct integration')],
'8-b-i':[L(LPC,'Some differentiation correct'),L(MPC,'One correct expression in a and b'),L(HPC,'Two correct equations in a and b')],
'8-b-ii':[L(LPC,'Curve of correct shape'),L(HPC,'No sketch but turning points calculated correctly')],
'8-c-i':[L(PC,'Some values calculated')],
'8-c-ii':[L(LPC,'Points of intersection calculated or indicated (from Tables)'),L(LPC,'Correct limits'),L(LPC,'Area under one curve only found'),L(LPC,'Correct area indicated'),L(HPC,'Area under each curve calculated correctly, but enclosed area not found')],
'8-c-iii':[L(PC,'Total area correct, but no reason given')],
}
ROWS={'maths-2013-hl-p1-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5B':[0,2,5],'5C':[0,2,4,5],'5D':[0,2,3,4,5],'10B':[0,5,10],'10C':[0,3,7,10],'10D':[0,3,5,8,10],'15B':[0,7,15],'15C':[0,5,10,15],'15D':[0,4,7,11,15]}
p=Paper(2013,'hl','p1',SC,'LC003ALP100EV.pdf','LC003ALP000EV.pdf',reviewed_at='2026-10-29',full_credit_minus_one=False)
STAR={'3-b','4-a-i','4-a-ii','4-b'}
def A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=None):
 p.A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=stem,extra={'fullCreditMinusOne':True} if s in STAR else None)
z='z = 4/(1 + √3i) is a complex number, where i² = −1.'
A('1-a','Q1(a)','10C',[7,29],[3],'3-1','complex-numbers','Verify that z can be written as 1 − √3i.',z)
A('1-b','Q1(b)','10C',[7,29],[3],'3-1','complex-numbers','Plot z on an Argand diagram and write z in polar form.',z)
A('1-c','Q1(c)','5C',[8,29],[3],'3-1','complex-numbers','Use De Moivre’s theorem to show that z¹⁰ = −2⁹(1 − √3i).',z)
A('2-a','Q2(a)','10C',[9,30],[4],'4-3','algebra-inequalities','Find the set of all real values of x for which 2x² + x − 15 ≥ 0.')
A('2-b','Q2(b)','15D',[9,30],[4],'4-2','algebra-simultaneous-equations','Solve the simultaneous equations: x + y + z = 16; (5/2)x + y + 10z = 40; 2x + (1/2)y + 4z = 21.')
carbon='Scientists can estimate the age of certain ancient items by measuring the proportion of carbon–14, relative to the total carbon content in the item. The formula used is Q = e^(−0·693t/5730), where Q is the proportion of carbon–14 remaining and t is the age, in years, of the item.'
A('3-a','Q3(a)','15B',[10,30],[5],'5-1','indices-and-logs','An item is 2000 years old. Use the formula to find the proportion of carbon–14 in the item.',carbon)
A('3-b','Q3(b)','10C',[10,30],[5],'5-1','indices-and-logs','The proportion of carbon–14 in an item found at Lough Boora, County Offaly, was 0·3402. Estimate, correct to two significant figures, the age of the item.',carbon)
save='Niamh has saved to buy a car. She saved an equal amount at the beginning of each month in an account that earned an annual equivalent rate (AER) of 4%.'
A('4-a-i','Q4(a)(i)','5C',[11,31],[6],'3-3','financial-maths','Show that the rate of interest, compounded monthly, which is equivalent to an AER of 4% is 0·327%, correct to 3 decimal places.',save)
A('4-a-ii','Q4(a)(ii)','10D',[11,12,31],[6],'3-3','financial-maths,sequences-series','Niamh has €15 000 in the account at the end of 36 months. How much has she saved each month, correct to the nearest euro?',save+' Part (a)(i): the equivalent monthly interest rate is 0·327%, correct to 3 decimal places.')
A('4-b','Q4(b)','10C',[13,31],[7],'3-3','financial-maths','Conall borrowed to buy a car. He borrowed €15 000 at a monthly interest rate of 0·866%. He made 36 equal monthly payments to repay the entire loan. How much, to the nearest euro, was each of his monthly payments?')
stadium='A stadium can hold 25 000 people. People attending a regular event at the stadium must purchase a ticket in advance. When the ticket price is €20, the expected attendance at an event is 12 000 people. The results of a survey carried out by the owners suggest that for every €1 reduction, from €20, in the ticket price, the expected attendance would increase by 1000 people.'
A('5-a','Q5(a)','10B',[14,32],[8],'3-1','financial-maths','If the ticket price was €18, how many people would be expected to attend?',stadium)
A('5-b','Q5(b)','5B',[14,32],[8],'5-1','functions','Let x be the ticket price, where x ≤ 20. Write down, in terms of x, the expected attendance at such an event.',stadium)
A('5-c','Q5(c)','5B',[14,32],[8],'5-1','functions','Write down a function f that gives the expected income from the sale of tickets for such an event.',stadium+' Let x be the ticket price, where x ≤ 20.')
A('5-d','Q5(d)','10B',[14,32],[8],'5-2','differentiation-applications','Find the price at which tickets should be sold to give the maximum expected income.',stadium)
A('5-e','Q5(e)','5B',[14,32],[8,9],'5-1','functions','Find this maximum expected income.',stadium+' Part (d): find the ticket price that maximises expected income.')
A('5-f','Q5(f)','10C',[15,32],[8,9],'5-1','functions','Suppose that tickets are instead priced at a value that is expected to give a full attendance at the stadium. Find the difference between the income from the sale of tickets at this price and the maximum income calculated at (e) above.',stadium)
A('5-g','Q5(g)','5D',[15,16,33],[8,9],'4-2','algebra-simultaneous-equations','The stadium was full for a recent special event. Two types of tickets were sold, a single ticket for €16 and a family ticket (2 adults and 2 children) for a certain amount. The income from this event was €365 000. If 1000 more family tickets had been sold, the income from the event would have been reduced by €14 000. How many family tickets were sold?','The stadium can hold 25 000 people.')
match='Shapes in the form of small equilateral triangles can be made using matchsticks of equal length. These shapes can be put together into patterns. The first three triangular patterns are shown in the original diagrams. The table for patterns 1–4 gives numbers of small triangles: 1, blank, 9, blank; and numbers of matchsticks: 3, 9, blank, blank.'
A('6-a-i','Q6(a)(i)','5B',[17,34],[10],'3-1','sequences-series','Draw the fourth pattern in the sequence.',match)
A('6-a-ii','Q6(a)(ii)','5C',[17,34],[10],'3-1','sequences-series','The table below shows the number of small triangles in each pattern and the number of matchsticks needed to create each pattern. Complete the table.',match)
A('6-b','Q6(b)','10B',[18,34],[10],'3-1','sequences-series','Write an expression in n for the number of triangles in the nth pattern in the sequence.',match)
A('6-c','Q6(c)','10B',[18,19,34],[10,11],'3-1','sequences-series','Find an expression, in n, for the number of matchsticks needed to turn the (n − 1)th pattern into the nth pattern.',match)
A('6-d','Q6(d)','10C',[19,20,35],[10,11],'3-1','sequences-series','The number of matchsticks in the nth pattern in the sequence can be represented by the function uₙ = an² + bn where a, b ∈ ℚ and n ∈ ℕ. Find the value of a and the value of b.',match)
A('6-e','Q6(e)','10C',[20,35],[10,11],'3-1','sequences-series','One of the patterns in the sequence has 4134 matchsticks. How many small triangles are in that pattern?',match+' Part (d): the number of matchsticks is represented by uₙ = an² + bn, where a, b ∈ ℚ and n ∈ ℕ.')

A('7-a','Q7(a)','15C',[21,36],[12],'5-2','differentiation-rules','Differentiate 5x/(x + 4), with respect to x, for x ≠ −4.')
param='A curve is defined by the parametric equations x = 1 + e^(−t), y = t² + 2e^t.'
A('7-b-i','Q7(b)(i)','10C',[22,36],[12],'5-2','differentiation-rules','Show that dy/dx = −2e^t(t + e^t).',param)
A('7-b-ii','Q7(b)(ii)','5D',[22,36],[12],'5-2','differentiation-applications','Hence, find the equation of the tangent to the curve at the point x = 2.',param+' Part (b)(i): dy/dx = −2e^t(t + e^t).')
A('7-c-i','Q7(c)(i)','5C',[23,36],[13],'5-2','differentiation-rules','Write x in terms of sin y, using the diagram. Hence, show that dy/dx = 1/√(1 − x²).','The original right-angled triangle has hypotenuse 1, side x opposite angle y and a marked right angle.')
A('7-c-ii','Q7(c)(ii)','15D',[23,37],[13],'5-2','differentiation-rules','If y = x + sin⁻¹x, prove that (1 − x²)d²y/dx² − x dy/dx + x = 0.')
A('8-a','Q8(a)','10C',[24,38],[14],'5-2','integration','Evaluate ∫₀² 12e^(3x) dx and give your answer in the form a(e^b − 1).')
cubic='The function f(x) = x³ + ax² + bx has turning points at x = 2 and x = −4/3.'
A('8-b-i','Q8(b)(i)','10D',[24,38],[14],'5-2','differentiation-applications','Find the value of a and the value of b.',cubic)
A('8-b-ii','Q8(b)(ii)','10C',[24,38],[14],'5-2','differentiation-applications','Find the co-ordinates of the turning points and then draw a sketch of the curve y = f(x).',cubic+' Part (b)(i): find a and b.')
curves='The graphs are y = 4x and y = x³ in the domain −2 ≤ x ≤ 2, x ∈ ℝ.'
A('8-c-i','Q8(c)(i)','5B',[25,38],[15],'5-1','functions','Draw the graphs of y = 4x and y = x³ in the domain −2 ≤ x ≤ 2, x ∈ ℝ.')
A('8-c-ii','Q8(c)(ii)','10C',[25,38],[15],'5-2','integration','Find the area of the region in the first quadrant enclosed by the two graphs.',curves)
A('8-c-iii','Q8(c)(iii)','5B',[26,38],[15],'5-2','integration','Write down the total area enclosed between the two graphs and give a reason for your answer.',curves+' Part (c)(ii): find the area enclosed in the first quadrant.')
marks={str(i):25 if i<=4 else 50 for i in range(1,9)}
p.check(marks,34)
p.review(marks,'Independent visual reading of all 20 original Phase 2 paper pages and scheme PDF pages 1–38, including all model solutions, credit notes and allocation/scale tables. Distinct from the Phase 3 booklet.',list(range(1,39)),[27,28],
 ['Sections A (Q1–4), B (Q5–6), C (Q7–8, Functions and Calculus, old syllabus) are all required.','Only Q3(b), Q4(a)(i), Q4(a)(ii), Q4(b) have starred scales and permit Full Credit minus one.','Q4(a)(ii) prints both beginning-of-month (€392) and end-of-month (€393) models; retain both with a labelled source note.','All detailed credit notes, including mathematical expressions that cannot be quoted reliably as text, are preserved in the original solution images.'],
 [{'pages':[2,3,8,12],'wording':'Answer all eight / all four / both questions','classification':'all-required','reason':'All 34 independently marked tasks are retained; no finite optional question routes.'},{'pages':[11],'wording':'One of the patterns','classification':'given-data','reason':'Identifies the pattern with 4134 matchsticks; not a choice of tasks.'}],
 lambda t:('all-required','All printed tasks retained.') if 'Answer all' in t or 'Answer both' in t else ('given-data','Identifies a pattern using the given count, not a task choice.') if 'One of the patterns' in t else None)
SCHEME_ROW_FIGURES = {'maths-2013-hl-p1-q1-a': 'maths-2013-HL-scheme-p007-i0', 'maths-2013-hl-p1-q1-b': 'maths-2013-HL-scheme-p007-i1', 'maths-2013-hl-p1-q1-c': 'maths-2013-HL-scheme-p008-i0', 'maths-2013-hl-p1-q2-a': 'maths-2013-HL-scheme-p009-i0', 'maths-2013-hl-p1-q2-b': 'maths-2013-HL-scheme-p009-i1', 'maths-2013-hl-p1-q3-a': 'maths-2013-HL-scheme-p010-i0', 'maths-2013-hl-p1-q3-b': 'maths-2013-HL-scheme-p010-i1', 'maths-2013-hl-p1-q4-a-i': 'maths-2013-HL-scheme-p011-i0', 'maths-2013-hl-p1-q4-a-ii': 'maths-2013-HL-scheme-p011-i1', 'maths-2013-hl-p1-q4-b': 'maths-2013-HL-scheme-p013-i0', 'maths-2013-hl-p1-q5-a': 'maths-2013-HL-scheme-p014-i0', 'maths-2013-hl-p1-q5-b': 'maths-2013-HL-scheme-p014-i1', 'maths-2013-hl-p1-q5-c': 'maths-2013-HL-scheme-p014-i2', 'maths-2013-hl-p1-q5-d': 'maths-2013-HL-scheme-p014-i3', 'maths-2013-hl-p1-q5-e': 'maths-2013-HL-scheme-p014-i4', 'maths-2013-hl-p1-q5-f': 'maths-2013-HL-scheme-p015-i0', 'maths-2013-hl-p1-q5-g': 'maths-2013-HL-scheme-p015-i1', 'maths-2013-hl-p1-q6-a-i': 'maths-2013-HL-scheme-p017-i0', 'maths-2013-hl-p1-q6-a-ii': 'maths-2013-HL-scheme-p017-i1', 'maths-2013-hl-p1-q6-b': 'maths-2013-HL-scheme-p018-i0', 'maths-2013-hl-p1-q6-c': 'maths-2013-HL-scheme-p018-i1', 'maths-2013-hl-p1-q6-d': 'maths-2013-HL-scheme-p019-i0', 'maths-2013-hl-p1-q6-e': 'maths-2013-HL-scheme-p020-i0', 'maths-2013-hl-p1-q7-a': 'maths-2013-HL-scheme-p021-i0', 'maths-2013-hl-p1-q7-b-i': 'maths-2013-HL-scheme-p022-i0', 'maths-2013-hl-p1-q7-b-ii': 'maths-2013-HL-scheme-p022-i1', 'maths-2013-hl-p1-q7-c-i': 'maths-2013-HL-scheme-p023-i0', 'maths-2013-hl-p1-q7-c-ii': 'maths-2013-HL-scheme-p023-i1', 'maths-2013-hl-p1-q8-a': 'maths-2013-HL-scheme-p024-i0', 'maths-2013-hl-p1-q8-b-i': 'maths-2013-HL-scheme-p024-i1', 'maths-2013-hl-p1-q8-b-ii': 'maths-2013-HL-scheme-p024-i2', 'maths-2013-hl-p1-q8-c-i': 'maths-2013-HL-scheme-p025-i0', 'maths-2013-hl-p1-q8-c-ii': 'maths-2013-HL-scheme-p025-i1', 'maths-2013-hl-p1-q8-c-iii': 'maths-2013-HL-scheme-p026-i0'}
overrides={c['id']:{'section':'A' if int(c['printedParts'][0].split('(')[0][1:])<=4 else 'B' if int(c['printedParts'][0].split('(')[0][1:])<=6 else 'C'} for c in p.cards}
for cid,key in SCHEME_ROW_FIGURES.items():overrides[cid]['figureKey']=key
p.apply(ROWS,'2013 Higher Project Maths Phase 2 Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides=overrides,question_figures=True)
