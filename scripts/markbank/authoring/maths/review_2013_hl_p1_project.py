"""2013 Higher Project Maths Paper 1, kept separate from the parallel legacy booklet."""
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
'5-a':[L(LPC,'One or two correct entries'),L(MPC,'Three to five correct entries'),L(HPC,'Six to ten correct entries')],
'5-b':[L(PC,'Some correct statement regarding the first or second derivative of a function'),L(PC,'Correct explanation of either first or second derivative')],
'6-a':[L(LPC,'One or two correct entries'),L(HPC,'Three to six correct entries')],
'6-b':[L(LPC,'Correct formula.'),L(HPC,'Correct substitution in the formula and stops')],
'6-c':[L(LPC,'Correct limits'),L(HPC,'Correct integration')],
'6-d':[L(PC,'Any correct relevant step')],
'7-a':[L(PC,'(20−18)1000 or equivalent')],
'7-b':[L(PC,'Expression (20 − x)')],
'7-c':[L(PC,'Correct number of people and/or correct rate in terms of x')],
'7-d':[L(PC,'Some correct differentiation of a quadratic function'),L(PC,'Correct testing with incorrect deduction or no deduction'),L(PC,'Possible to get full marks without use of calculus'),L(PC,'Correct answer and no work')],
'7-e':[L(PC,'Some effort at substitution of 16 or equivalent')],
'7-f':[L(LPC,'Use of expression'),L(LPC,'Use of 25000'),L(LPC,'Some use of tables'),L(LPC,'Equation solved'),L(LPC,'Price of ticket found'),L(HPC,'Total income from sales')],
'7-g':[L(LPC,'Correct number of family tickets'),L(LPC,'Income from single tickets'),L(LPC,'Income from family tickets'),L(MPC,'Two correct linear equations for income in two unknowns'),L(HPC,'Correct value for p (single ticket)'),L(HPC,'Correct value for y (family ticket)'),L('Alternative method, '+LPC,'Correct equation'),L('Alternative method, '+MPC,'Three correct equations'),L('Alternative method, '+HPC,'One unknown calculated')],
'8-a':[L(LPC,'Some correct substitution into s(t)'),L(HPC,'Correct substitution.'),L(FC,'Correct answer without work')],
'8-b':[L(LPC,'Any correct differentiation'),L(HPC,'Fails to select correct value for t')],
'8-c':[L(LPC,'Some correct differentiation of the first derivative'),L(HPC,'Sets up correct equation.')],
'8-d':[L(LPC,'Some correct substitution'),L(LPC,'Finds distance travelled after initial 10 seconds i.e. 540m'),L(LPC,'Correct differentiation (relevant for terminal velocity)'),L(MPC,'Finds k.'),L(HPC,'Finds time travelling at terminal velocity and stops')],
'8-e':[L(LPC,'Any relevant step'),L(HPC,'Correct substitution into chain rule'),L(HPC,'Fails to substitute for r')],
'9-a-i':[L(PC,'Incomplete 4th line')],
'9-a-ii':[L(LPC,'One or two correct entries in empty boxes'),L(HPC,'Three correct entries in empty boxes')],
'9-b':[L(PC,'Second differences calculated')],
'9-c':[L(PC,'Recognition of series 6, 9, 12,.... or similar'),L('Alternative method, '+PC,'Second differences calculated')],
'9-d':[L(HPC,'Two correct linear equations'),L('Alternative method, '+LPC,'Recognition of A.P.')],
'9-e':[L(LPC,'Expression of un in one variable only'),L(LPC,'Quadratic equation'),L(HPC,'Values of n')],
}
ROWS={'maths-2013-hl-p1-project-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5B':[0,2,5],'5C':[0,2,4,5],'5D':[0,2,3,4,5],'10B':[0,5,10],'10C':[0,3,7,10],'10D':[0,3,5,8,10],'15B':[0,7,15],'15D':[0,4,7,11,15]}
p=Paper(2013,'hl','p1',SC,'LC003ALP130EV.pdf','LC003ALP030EV.pdf',reviewed_at='2026-10-29',edition='project',full_credit_minus_one=False)
STAR={'3-b','4-a-i','4-a-ii','4-b','6-a','8-a','8-b','8-c','8-d','8-e'}
def A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=None):
 p.A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=stem,extra={'fullCreditMinusOne':True} if s in STAR else None)
z='z = 4/(1 + √3i) is a complex number, where i² = −1.'
A('1-a','Q1(a)','10C',[7,28],[3],'3-1','complex-numbers','Verify that z can be written as 1 − √3i.',z)
A('1-b','Q1(b)','10C',[7,28],[3],'3-1','complex-numbers','Plot z on an Argand diagram and write z in polar form.',z)
A('1-c','Q1(c)','5C',[8,28],[3],'3-1','complex-numbers','Use De Moivre’s theorem to show that z¹⁰ = −2⁹(1 − √3i).',z)
A('2-a','Q2(a)','10C',[9,29],[4],'4-3','algebra-inequalities','Find the set of all real values of x for which 2x² + x − 15 ≥ 0.')
A('2-b','Q2(b)','15D',[9,29],[4],'4-2','algebra-simultaneous-equations','Solve the simultaneous equations: x + y + z = 16; (5/2)x + y + 10z = 40; 2x + (1/2)y + 4z = 21.')
carbon='Scientists can estimate the age of certain ancient items by measuring the proportion of carbon–14, relative to the total carbon content in the item. The formula used is Q = e^(−0·693t/5730), where Q is the proportion of carbon–14 remaining and t is the age, in years, of the item.'
A('3-a','Q3(a)','15B',[10,29],[5],'5-1','indices-and-logs','An item is 2000 years old. Use the formula to find the proportion of carbon–14 in the item.',carbon)
A('3-b','Q3(b)','10C',[10,29],[5],'5-1','indices-and-logs','The proportion of carbon–14 in an item found at Lough Boora, County Offaly, was 0·3402. Estimate, correct to two significant figures, the age of the item.',carbon)
save='Niamh has saved to buy a car. She saved an equal amount at the beginning of each month in an account that earned an annual equivalent rate (AER) of 4%.'
A('4-a-i','Q4(a)(i)','5C',[11,30],[6],'3-3','financial-maths','Show that the rate of interest, compounded monthly, which is equivalent to an AER of 4% is 0·327%, correct to 3 decimal places.',save)
A('4-a-ii','Q4(a)(ii)','10D',[11,12,30],[6],'3-3','financial-maths,sequences-series','Niamh has €15 000 in the account at the end of 36 months. How much has she saved each month, correct to the nearest euro?',save+' Part (a)(i): the equivalent monthly interest rate is 0·327%, correct to 3 decimal places.')
A('4-b','Q4(b)','10C',[13,30],[7],'3-3','financial-maths','Conall borrowed to buy a car. He borrowed €15 000 at a monthly interest rate of 0·866%. He made 36 equal monthly payments to repay the entire loan. How much, to the nearest euro, was each of his monthly payments?')
graphs='Each diagram shows part of the graph of a function: f, g, h and k. Each function is either quadratic or cubic or trigonometric or exponential (not necessarily in that order). Diagrams A–D show their first derivatives, and I–IV their second derivatives, not necessarily in the same order. Refer to all twelve original graphs.'
A('5-a','Q5(a)','15D',[14,31],[8],'5-2','differentiation-applications','Complete the table by matching the function to its first derivative and its second derivative. Rows: Quadratic, Cubic, Trigonometric, Exponential. Columns: Function, First derivative, Second derivative.',graphs)
A('5-b','Q5(b)','10B',[14,31],[8],'5-2','differentiation-applications','For one row in the table, explain your choice of first derivative and second derivative.',graphs+' Part (a): match each of the four function types to its function, first derivative and second derivative.')
sine='The diagram shows the graph of the function y = sin x in the domain 0 ≤ x ≤ π, x ∈ ℝ. The table lists x = 0, π/6, π/3, π/2, 2π/3, 5π/6, π, with y values left blank.'
A('6-a','Q6(a)','5C',[15,32],[9],'5-1','trigonometry-functions-identities','Complete the table below, correct to three decimal places.',sine)
A('6-b','Q6(b)','10C',[15,32],[9],'3-4','area-volume','Use the trapezoidal rule to find the approximate area of the region enclosed between the curve and the x-axis in the given domain.',sine)
A('6-c','Q6(c)','5C',[15,32],[9],'5-2','integration','Use integration to find the actual area of the region shown above.',sine)
A('6-d','Q6(d)','5B',[15,32],[9],'3-1','area-volume','Find the percentage error in your answer to (b) above.',sine+' Part (b): use the trapezoidal rule to approximate the area. Part (c): use integration to find the actual area.')
stadium='A stadium can hold 25 000 people. People attending a regular event at the stadium must purchase a ticket in advance. When the ticket price is €20, the expected attendance at an event is 12 000 people. The results of a survey carried out by the owners suggest that for every €1 reduction, from €20, in the ticket price, the expected attendance would increase by 1000 people.'
A('7-a','Q7(a)','10B',[16,33],[10],'3-1','financial-maths','If the ticket price was €18, how many people would be expected to attend?',stadium)
A('7-b','Q7(b)','5B',[16,33],[10],'5-1','functions','Let x be the ticket price, where x ≤ 20. Write down, in terms of x, the expected attendance at such an event.',stadium)
A('7-c','Q7(c)','5B',[16,33],[10],'5-1','functions','Write down a function f that gives the expected income from the sale of tickets for such an event.',stadium+' Let x be the ticket price, where x ≤ 20.')
A('7-d','Q7(d)','10B',[16,33],[10],'5-2','differentiation-applications','Find the price at which tickets should be sold to give the maximum expected income.',stadium)
A('7-e','Q7(e)','5B',[16,33],[10,11],'5-1','functions','Find this maximum expected income.',stadium+' Part (d): find the ticket price that maximises expected income.')
A('7-f','Q7(f)','10C',[17,33],[10,11],'5-1','functions','Suppose that tickets are instead priced at a value that is expected to give a full attendance at the stadium. Find the difference between the income from the sale of tickets at this price and the maximum income calculated at (e) above.',stadium)
A('7-g','Q7(g)','5D',[17,18,34],[10,11],'4-2','algebra-simultaneous-equations','The stadium was full for a recent special event. Two types of tickets were sold, a single ticket for €16 and a family ticket (2 adults and 2 children) for a certain amount. The income from this event was €365 000. If 1000 more family tickets had been sold, the income from the event would have been reduced by €14 000. How many family tickets were sold?','The stadium can hold 25 000 people.')
rain='The speed at which a raindrop falls increases until a maximum speed, called its terminal velocity, is reached. The raindrop then continues to fall at this terminal velocity. The distance, s metres, it falls is given by s(t) = 6t + 0·3t² − 0·01t³ for 0 ≤ t ≤ 10, and k(t − 10) for t > 10, as printed. Here t is the time in seconds from the instant the raindrop begins to fall and k is a constant.'
A('8-a','Q8(a)','10C',[19,35],[12],'5-1','functions','How far has this raindrop fallen after 10 seconds?',rain)
A('8-b','Q8(b)','10D',[19,35],[12],'5-2','differentiation-applications','After how many seconds is the raindrop falling at a speed of 8·25 metres per second?',rain)
A('8-c','Q8(c)','10C',[19,35],[12],'5-2','differentiation-applications','The acceleration of the raindrop is decreasing for the first 10 seconds of its fall. Find the value of t for which the acceleration is 0·006 m s⁻².',rain)
A('8-d','Q8(d)','10D',[19,20,35],[12,13],'5-2','differentiation-applications','The raindrop falls vertically from a height of 620 metres. How long will it take the raindrop to fall to ground level?',rain)
A('8-e','Q8(e)','10D',[20,36],[13],'5-2','differentiation-applications','A raindrop increases in size as it falls. The volume of a spherical raindrop increases at a rate of 6 cubic millimetres per second. Find the rate at which the radius of the raindrop is increasing when the radius is 1·5 mm.')
match='Shapes in the form of small equilateral triangles can be made using matchsticks of equal length. These shapes can be put together into patterns. The first three triangular patterns are shown in the original diagrams. The table for patterns 1–4 gives numbers of small triangles: 1, blank, 9, blank; and numbers of matchsticks: 3, 9, blank, blank.'
A('9-a-i','Q9(a)(i)','5B',[21,37],[14],'3-1','sequences-series','Draw the fourth pattern in the sequence.',match)
A('9-a-ii','Q9(a)(ii)','5C',[21,37],[14],'3-1','sequences-series','The table below shows the number of small triangles in each pattern and the number of matchsticks needed to create each pattern. Complete the table.',match)
A('9-b','Q9(b)','10B',[22,37],[14],'3-1','sequences-series','Write an expression in n for the number of triangles in the nth pattern in the sequence.',match)
A('9-c','Q9(c)','10B',[22,23,37],[14,15],'3-1','sequences-series','Find an expression, in n, for the number of matchsticks needed to turn the (n − 1)th pattern into the nth pattern.',match)
A('9-d','Q9(d)','10C',[24,38],[14,15],'3-1','sequences-series','The number of matchsticks in the nth pattern in the sequence can be represented by the function uₙ = an² + bn where a, b ∈ ℚ and n ∈ ℕ. Find the value of a and the value of b.',match)
A('9-e','Q9(e)','10C',[25,38],[14,15],'3-1','sequences-series','One of the patterns in the sequence has 4134 matchsticks. How many small triangles are in that pattern?',match+' Part (d): the number of matchsticks is represented by uₙ = an² + bn, where a, b ∈ ℚ and n ∈ ℕ.')
marks={str(i):25 if i<=6 else 50 for i in range(1,10)}
p.check(marks,34)
p.review(marks,'Independent visual reading of all 20 original Project Maths paper pages and scheme PDF pages 1–38, including every model, detailed credit note and scale table. Parallel legacy edition remains separate.',list(range(1,39)),[26,27],
 ['Only starred scales allow Full Credit minus one; the default is false, with explicit task overrides.','Q5(b) permits an explanation of any one of four rows. All four graphs/derivative options remain in the card; the choice is an example within one task.','Printed source issues: Q6(d) model cross-reference; Q8 missing distance offset after t=10; Q9(e) first model mistypes 4234 instead of 4134.'],
 [{'pages':[2,3,10],'wording':'Answer all nine/six/three questions','classification':'all-required','reason':'All 34 marking units retained.'},{'pages':[8],'wording':'For one row in the table','classification':'example-choice-within-task','reason':'All four rows and twelve graphs are retained; the candidate explains one pair of derivative relationships.'}],
 lambda t:('all-required','All printed tasks retained.') if 'Answer all' in t else ('function-category','Describes the graph categories, not optional exam tasks.') if 'either quadratic' in t else ('graph-correspondence','Each diagram corresponds to one function; all diagrams remain available.') if 'derivative of one of' in t else ('data-reference','The pattern count is given data, not a question choice.') if 'One of the patterns' in t else None)
SCHEME_ROW_FIGURES = {'maths-2013-hl-p1-project-q1-a': 'maths-2013-HL-scheme-project-p007-i0', 'maths-2013-hl-p1-project-q1-b': 'maths-2013-HL-scheme-project-p007-i1', 'maths-2013-hl-p1-project-q1-c': 'maths-2013-HL-scheme-project-p008-i0', 'maths-2013-hl-p1-project-q2-a': 'maths-2013-HL-scheme-project-p009-i0', 'maths-2013-hl-p1-project-q2-b': 'maths-2013-HL-scheme-project-p009-i1', 'maths-2013-hl-p1-project-q3-a': 'maths-2013-HL-scheme-project-p010-i0', 'maths-2013-hl-p1-project-q3-b': 'maths-2013-HL-scheme-project-p010-i1', 'maths-2013-hl-p1-project-q4-a-i': 'maths-2013-HL-scheme-project-p011-i0', 'maths-2013-hl-p1-project-q4-a-ii': 'maths-2013-HL-scheme-project-p011-i1', 'maths-2013-hl-p1-project-q4-b': 'maths-2013-HL-scheme-project-p013-i0', 'maths-2013-hl-p1-project-q5-a': 'maths-2013-HL-scheme-project-p014-i0', 'maths-2013-hl-p1-project-q5-b': 'maths-2013-HL-scheme-project-p014-i1', 'maths-2013-hl-p1-project-q6-a': 'maths-2013-HL-scheme-project-p015-i0', 'maths-2013-hl-p1-project-q6-b': 'maths-2013-HL-scheme-project-p015-i1', 'maths-2013-hl-p1-project-q6-c': 'maths-2013-HL-scheme-project-p015-i2', 'maths-2013-hl-p1-project-q6-d': 'maths-2013-HL-scheme-project-p015-i3', 'maths-2013-hl-p1-project-q7-a': 'maths-2013-HL-scheme-project-p016-i0', 'maths-2013-hl-p1-project-q7-b': 'maths-2013-HL-scheme-project-p016-i1', 'maths-2013-hl-p1-project-q7-c': 'maths-2013-HL-scheme-project-p016-i2', 'maths-2013-hl-p1-project-q7-d': 'maths-2013-HL-scheme-project-p016-i3', 'maths-2013-hl-p1-project-q7-e': 'maths-2013-HL-scheme-project-p016-i4', 'maths-2013-hl-p1-project-q7-f': 'maths-2013-HL-scheme-project-p017-i0', 'maths-2013-hl-p1-project-q7-g': 'maths-2013-HL-scheme-project-p017-i1', 'maths-2013-hl-p1-project-q8-a': 'maths-2013-HL-scheme-project-p019-i0', 'maths-2013-hl-p1-project-q8-b': 'maths-2013-HL-scheme-project-p019-i1', 'maths-2013-hl-p1-project-q8-c': 'maths-2013-HL-scheme-project-p019-i2', 'maths-2013-hl-p1-project-q8-d': 'maths-2013-HL-scheme-project-p020-i0', 'maths-2013-hl-p1-project-q8-e': 'maths-2013-HL-scheme-project-p020-i1', 'maths-2013-hl-p1-project-q9-a-i': 'maths-2013-HL-scheme-project-p021-i0', 'maths-2013-hl-p1-project-q9-a-ii': 'maths-2013-HL-scheme-project-p021-i1', 'maths-2013-hl-p1-project-q9-b': 'maths-2013-HL-scheme-project-p022-i0', 'maths-2013-hl-p1-project-q9-c': 'maths-2013-HL-scheme-project-p022-i1', 'maths-2013-hl-p1-project-q9-d': 'maths-2013-HL-scheme-project-p024-i0', 'maths-2013-hl-p1-project-q9-e': 'maths-2013-HL-scheme-project-p025-i0'}
p.apply(ROWS,'2013 Higher Project Maths Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
