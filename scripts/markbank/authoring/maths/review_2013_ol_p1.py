"""2013 Ordinary Phase 2 Paper 1: independently reviewed paper, scales and finite routes."""
import os,sys,itertools,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R={'1-a': ['Low Partial Credit — A correct real or imaginary part plotted for either point.',
         'Low Partial Credit — Both numbers plotted correctly but real and imaginary axes interchanged.',
         'High Partial Credit — Plots one point correctly.'],
 '1-b': ['Low Partial Credit — Correct answer given without a reason or reason given is without merit.',
         'Low Partial Credit — Answer not given, or incorrect, but some merit in the reason such as reference to distance.',
         'High Partial Credit — Correct answer with a reason given that refers to distance.',
         'High Partial Credit — A fully correct reason without an answer given.'],
 '1-c': ['Low Partial Credit — Correct modulus formula written.',
         'Low Partial Credit — Each point joined to origin.',
         'Low Partial Credit — Use of z₁ or z₂.',
         'High Partial Credit — One modulus value calculated correctly.',
         'High Partial Credit — Correct substitution into formula for both numbers but neither value correct.',
         'Note — Both modulus values correct, without comparison shown, award full credit.'],
 '1-d': ['Low Partial Credit — Correct substitution for z₁ and/or z₂.',
         'High Partial Credit — Multiplication above and below by correct conjugate shown and some subsequent work.'],
 '2-a': ['Low Partial Credit — One or two correct values only in the table.',
         'Mid Partial Credit — Three or four correct values only in the table.',
         'High Partial Credit — Five or six correct values in the table.'],
 '2-b': ['Low Partial Credit — Writes the correct trapezoidal rule, without further work of merit.',
         'Low Partial Credit — Simpson’s rule with substantially correct substitution and calculation.',
         'High Partial Credit — Trapezoidal rule with correct substitution.',
         'High Partial Credit — Trapezoidal rule with incorrect substitution (maximum of 2) with correct calculation.',
         'High Partial Credit — Correct answer without work shown.',
         'Note — Formula and correct answer, without work shown, award full credit.'],
 '3-a': ['Partial Credit — Either a (unrounded) or n correct.',
         'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted round-off, provided full marks otherwise.'],
 '3-b-i': ['Low Partial Credit — One or two numbers only (other than A) written correctly.',
           'High Partial Credit — Three, four or five numbers only (other than A) written correctly.'],
 '3-b-ii': ['Low Partial Credit — One or two numbers only plotted correctly.',
            'High Partial Credit — Three or four numbers only plotted correctly.'],
 '3-c': ['Low Partial Credit — Some work of merit with indices.',
         'Low Partial Credit — Some work of merit in solving linear equation.',
         'Low Partial Credit — Solves the equation 2x = x + 10 correctly.',
         'Low Partial Credit — Correct answer without work shown.',
         'High Partial Credit — Correct equation in indices set up but fails to finish correctly.',
         'High Partial Credit — Incorrect equation in indices but solves “equation of indices” correctly.',
         'Note — Correct answer by trial and improvement shown for both sides, award full credit.'],
 '4-a': ['Partial Credit — Some work of merit e.g. 1·015.',
         'Partial Credit — Multiplies by 12.',
         'Partial Credit — Accept (1·15)¹² = 5·3502… or (1·0015)¹² = 1·0181… with or without work shown.',
         'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted round-off, provided full marks otherwise.'],
 '4-b': ['Low Partial Credit — Writes correct formula without further work of merit.',
         'Low Partial Credit — Some correct substitution into an incorrect formula, e.g. depreciation.',
         'Low Partial Credit — Calculates 1·5% of an amount correctly.',
         'High Partial Credit — Correct substitution into correct formula but error in calculations.',
         'High Partial Credit — Calculates the amount at the end of each of 15 months, but with minor errors.'],
 '4-c': ['Partial Credit — Writes 95/0·8473 and stops.',
         'Partial Credit — Gives an answer of €80·49 with or without work shown.',
         'Note — Correct answer without work shown, award full credit.',
         'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted round-off, provided full marks otherwise.'],
 '5-a': ['Low Partial Credit — Table for one tank with two correct entries.',
         'Mid Partial Credit — Table for one tank correct.',
         'Mid Partial Credit — Table for two tanks correct for 1 minute.',
         'High Partial Credit — Four terms or less missing or incorrect, allowing for consistent terms.',
         'High Partial Credit — Tables which begin with A(10) = 25 and B(10) = 10 and continue correctly.',
         'High Partial Credit — Tables which begin with A(0) = 0 and B(0) = 0 and continue correctly.',
         'Note — Accept tables which are fully correct but do not include the values at t = 0.',
         'Note — Accept answers in (b), (c) and (d) based on candidate’s tables.'],
 '5-b': ['Partial Credit — One correct answer.',
         'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted units, provided full marks otherwise.',
         'Note — Accept answers in (b), (c) and (d) based on candidate’s tables.'],
 '5-c': ['Partial Credit — Writes Tₙ = a + (n − 1)d.',
         'Partial Credit — Some work at setting up a formula.',
         'Note — Accept answers in (b), (c) and (d) based on candidate’s tables.'],
 '5-d': ['Low Partial Credit — Correct point plotted for one line.',
         'Low Partial Credit — A line of some relevance drawn.',
         'High Partial Credit — One graph fully correct or both graphs substantially correct.',
         'High Partial Credit — Correct graphs drawn freehand.',
         'Note — Accept answers in (b), (c) and (d) based on candidate’s tables.',
         'Note — Accept answers in (e) and (f) based on candidate’s graph.'],
 '5-e': ['Partial Credit — Point of intersection identified.',
         'Partial Credit — Answer indicated on axis but value not written.',
         'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted units, provided full marks otherwise.',
         'Note — Accept answers in (e) and (f) based on candidate’s graph.'],
 '5-f': ['Low Partial Credit — Formulae written but not equated.',
         'High Partial Credit — Error in solving equation.',
         'High Partial Credit — Substitutes correctly into one formula only.',
         'Note — Accept answers in (e) and (f) based on candidate’s graph.'],
 '6-a': ['Low Partial Credit — One correct entry.',
         'Mid Partial Credit — Errors in three or more terms, allowing for consistent errors.',
         'High Partial Credit — Errors in two or less terms, allowing for consistent errors.'],
 '6-b': ['Note — Accept answers based on candidate’s work.'],
 '6-c-i': ['Partial Credit — Shows some understanding of an arithmetic sequence.'],
 '6-c-ii': ['Partial Credit — Correct answer without valid explanation.',
            'Partial Credit — Correct explanation without giving an answer.'],
 '6-d': ['Partial Credit — Correctly identifies a or d for Eoin’s salary.',
         'Partial Credit — Correctly identifies a and d for Peter’s salary.',
         'Partial Credit — Writes Tₙ = a + (n − 1)d.'],
 '6-e': ['Low Partial Credit — Finds the correct value of n and stops.',
         'Low Partial Credit — Continues the pattern for one more term.',
         'Low Partial Credit — Attempts substitution into candidate’s formula.',
         'Low Partial Credit — Some merit in work with the general term.',
         'High Partial Credit — Continues pattern correctly but stops at the tenth year.',
         'High Partial Credit — Substitutes n = 10 into formula and calculates answer.'],
 '6-f': ['Low Partial Credit — Writes Sₙ = n/2 [2a + (n − 1)d] or other valid formula.',
         'Low Partial Credit — Identifies a or d for Peter’s salary.',
         'Low Partial Credit — Identifies a and d for Eoin’s salary.',
         'High Partial Credit — A correct formula substituted, except for one error, for Peter.',
         'High Partial Credit — A correct formula applied to Eoin’s data, correctly.'],
 '6-g': ['Note — Accept candidate’s answers from (f).',
         'Low Partial Credit — Finds the correct value of n and stops.',
         'Low Partial Credit — Continues the pattern for one more term.',
         'Low Partial Credit — Attempts substitution into candidate’s formula.',
         'Low Partial Credit — Some merit in work with the Sₙ formula.',
         'Low Partial Credit — Uses Eoin’s data incorrectly.',
         'High Partial Credit — Continues the pattern correctly to 2015 but doesn’t add the terms.',
         'High Partial Credit — Continues the pattern incorrectly (stops at n = 10 or one error with consistent terms) but adds '
         'the terms.',
         'High Partial Credit — Substitutes n = 10 into formula and calculates answer.',
         'High Partial Credit — Substitutes correctly into formula but doesn’t calculate answer.',
         'High Partial Credit — Uses Eoin’s data correctly.'],
 '6-h': ['Partial Credit — A reason with some merit.'],
 '7-a': ['Low Partial Credit — Correct differentiation of one term only.',
         'High Partial Credit — Correct differentiation of two terms only.',
         'High Partial Credit — Correct coefficient for each term but error(s) in indices.',
         'High Partial Credit — Correct indices for each term but error(s) in coefficients.'],
 '7-b-i': ['Low Partial Credit — Correct formula written without further work of merit.',
           'Low Partial Credit — Identifies u or v.',
           'Low Partial Credit — Some correct differentiation.',
           'Low Partial Credit — Incomplete multiplication of the given product before differentiation.',
           'High Partial Credit — Correct structure to the answer but some errors.',
           'High Partial Credit — Substantially correct multiplication and differentiation of given product.'],
 '7-b-ii': ['Low Partial Credit — Substitution of x = 0 into given equation.',
            'Low Partial Credit — Correct formula written without further work of merit.',
            'Low Partial Credit — Identifies u or v.',
            'Mid Partial Credit — Correct structure to the answer with some errors, including failure to substitute into '
            'derivative.',
            'High Partial Credit — Correct structure to the answer with some errors, but some correct substitution of x = 0 into '
            'derivative.'],
 '7-c-i': ['Low Partial Credit — Inverted slope formula with otherwise correct work.',
           'Low Partial Credit — Correct formula with errors in substitution.',
           'High Partial Credit — Correct substitution with errors in simplification.'],
 '7-c-ii': ['Low Partial Credit — Correct differentiation of one term only.',
            'High Partial Credit — Correct differentiation of two terms only.',
            'High Partial Credit — Correct coefficient for each term but error(s) in indices.',
            'High Partial Credit — Correct indices for each term but error(s) in coefficients.'],
 '7-c-iii': ['Low Partial Credit — Shows f(−1) = −3.',
             'Low Partial Credit — Substitutes x = −1 into f′(x) and stops.',
             'Low Partial Credit — Error in substitution into derivative.',
             'High Partial Credit — Correct substitution with errors in simplification.'],
 '7-c-iv': ['Low Partial Credit — Attempt at finding slope of l₂.',
            'Low Partial Credit — Attempts to work with f′(x).',
            'Low Partial Credit — Correct answer without work shown.',
            'Low Partial Credit — Finds the x co-ordinate only, graphically.',
            'High Partial Credit — Finds the x co-ordinate only of the point of contact using differentiation.',
            'High Partial Credit — Correct answer obtained graphically.'],
 '8-a': ['Low Partial Credit — One term differentiated correctly.',
         'Low Partial Credit — Differentiation with one coefficient or one index correct.',
         'Low Partial Credit — Solves f(x) = 0, correctly.',
         'Mid Partial Credit — Two or three terms differentiated correctly and stops.',
         'Mid Partial Credit — Puts f′(x) = 0, where f′(x) has at least one term correct, and stops or continues.',
         'High Partial Credit — Correct differentiation and puts f′(x) = 0 without solving correctly.',
         'High Partial Credit — Differentiation, with one error, puts f′(x) = 0 and solves correctly.',
         'High Partial Credit — Calculates f′(0).'],
 '8-b-i': ['Low Partial Credit — One term differentiated correctly.',
           'Low Partial Credit — Correct maximum and minimum co-ordinates found graphically.',
           'Low Partial Credit — g′(x) linear.',
           'Mid Partial Credit — Correct structure to solving g′(x) = 0, but two or more significant errors.',
           'Mid Partial Credit — Correct differentiation of g(x) and stops.',
           'High Partial Credit — Correct work (other than some minor errors or one major error) at solving and finding both '
           'co-ordinates of points.'],
 '8-b-ii': ['Partial Credit — Some correct aspect to the sketch, based on candidate’s work, other than axes drawn.'],
 '8-c-i': ['Low Partial Credit — Some work at substituting t = 1.',
           'High Partial Credit — Correct substitution with errors in simplification.',
           'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted units, provided full marks otherwise.'],
 '8-c-ii': ['Low Partial Credit — Some correct differentiation.',
            'Low Partial Credit — Incorrect derivative set equal to 0 and stops.',
            'Low Partial Credit — No differentiation with s(2) calculated.',
            'High Partial Credit — Correct differentiation and stops.',
            'High Partial Credit — Incorrect derivative set equal to 0 and attempts to solve.',
            'Full Credit −1 (deduction) — Penalise one mark for incorrect or omitted units, provided full marks otherwise.'],
 '8-c-iii': ['Partial Credit — Attempt at second derivative.',
             'Partial Credit — Showing that first derivative is decreasing by trial and improvement.',
             'Note — Correct answer without work shown, award full credit.']}
R['1-d'].append(L(FCM,'Penalise one mark for not writing correct answer in the form −1 − 2i.'))
ROUTES=list(itertools.combinations('ABCDEFG',5))
for route in ROUTES:R['3-b-ii-'+''.join(route).lower()]=R['3-b-ii']
del R['3-b-ii']
ROWS={'maths-2013-ol-p1-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5A':[0,5],'5B':[0,2,5],'5C':[0,2,4,5],'10B':[0,5,10],'10C':[0,3,7,10],'10D':[0,2,5,8,10],'15C':[0,5,10,15],'15D':[0,4,7,11,15],'25C':[0,8,17,25]}
p=Paper(2013,'ol','p1',SC,'LC003GLP100EV.pdf','LC003GLP000EV.pdf',reviewed_at='2026-10-29',full_credit_minus_one=False)
STAR={'1-d','3-a','4-a','4-c','5-b','5-e','8-c-i','8-c-ii'}
def A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=None,extra=None):
 e=extra or {}
 if s in STAR:e['fullCreditMinusOne']=True
 p.A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=stem,extra=e)
z='Let z₁ = 3 − 4i and z₂ = 1 + 2i, where i² = −1. The original Argand diagram is provided.'
A('1-a','Q1(a)','5C',[7,22],[3],'3-1','complex-numbers','Plot z₁ and z₂ on the Argand diagram.',z)
A('1-b','Q1(b)','5C',[7,22],[3],'3-1','complex-numbers','From your diagram, is it possible to say that |z₁| > |z₂|? Give the reason for your answer.',z+' Part (a): plot z₁ and z₂.')
A('1-c','Q1(c)','5C',[7,22],[3],'3-1','complex-numbers','Verify algebraically that |z₁| > |z₂|.',z)
A('1-d','Q1(d)','10C',[7,22],[3],'3-1','complex-numbers','Find z₁/z₂ in the form x + yi, where x, y ∈ ℝ.',z)
f='The diagram shows the graph of f(x) = 6x − x² in the domain 0 ≤ x ≤ 6, x ∈ ℝ.'
A('2-a','Q2(a)','10D',[8,23],[4],'5-1','graphing-functions','Find f(0), f(1), f(2), f(3), f(4), f(5) and f(6). Hence, complete the table.',f)
A('2-b','Q2(b)','15C',[8,23],[4],'3-4','area-volume','Use the trapezoidal rule to estimate the area of the region enclosed between the curve and the x-axis in the given domain.',f+' Part (a): evaluate the function at every integer from 0 to 6.')
A('3-a','Q3(a)','5B',[9,24],[5],'3-1','number-systems','The mean distance from the earth to the sun is 149 597 871 km. Write this number in the form a × 10ⁿ, where 1 ≤ a < 10 and n ∈ ℤ, correct to two significant figures.')
numbers='The table contains A: 2·1; B: √5; C: 243/85; D: tan 70°; E: 3π/4; F: 250%; G: (1 + 1/10)¹⁰. A is already written as 2·10.'
A('3-b-i','Q3(b)(i)','5C',[9,24],[5],'3-1','number-systems','Write each number as a decimal correct to two decimal places. Complete the table.',numbers)
for route in ROUTES:
 suffix='3-b-ii-'+''.join(route).lower()
 A(suffix,'Q3(b)(ii)','5C',[9,24],[5],'3-1','number-systems','Plot '+', '.join(route)+' on the number line and label each number clearly. This is one of the 21 valid selections for the original instruction to mark five of the seven numbers.',numbers,{'selectionVariant':{'groupId':'q3-b-ii','pool':list('ABCDEFG'),'choose':5,'selected':list(route),'practiceInstruction':'For this practice, plot '+', '.join(route)+' and label each number. The original question allows any five of the seven numbers.','sourcePage':5,'sourceDirective':'Mark 5 of the numbers in the table on the number line below'}})
A('3-c','Q3(c)','10C',[9,24],[5],'4-1','indices','Solve the equation 27^(2x) = 3^(x + 10).')
A('4-a','Q4(a)','5B',[10,25],[6],'3-1','financial-maths','Given that R = (1 + 0·015)¹², find the value of R, correct to 2 decimal places.')
A('4-b','Q4(b)','10C',[10,25],[6],'3-3','financial-maths','Michael has a credit card with a credit limit of €1000. Interest is charged monthly at 1·5% of the amount owed. Michael gets a bill at the end of each month. At the start of January, Michael owes €800 on his credit card. If Michael makes no repayments and no more purchases, show that he will exceed his credit limit after 15 months.')
A('4-c','Q4(c)','10B',[11,25],[7],'3-3','financial-maths','Michael buys an item costing £95 on the internet and pays with his credit card. If the exchange rate is €1 = £0·8473, calculate, correct to the nearest cent, the amount that will be included on Michael’s credit card bill.')
tanks='Two identical cylindrical tanks, A and B, are being filled with water. At a particular time, the water in A is 25 cm deep and its depth increases steadily by 5 cm every 10 seconds. At the same time, the water in B is 10 cm deep and its depth increases steadily by 7·5 cm every 10 seconds.'
A('5-a','Q5(a)','10D',[12, 26],[8],'4-1','sequences-series','Draw up a table showing the depth of water in each tank at 10 second intervals over two minutes, beginning at the time mentioned above.',tanks)
A('5-b','Q5(b)','5B',[12, 26],[8],'4-2','algebra-equations','Each tank is 1 m in height. Find how long it takes to fill each tank.',tanks)
A('5-c','Q5(c)','5B',[12, 26],[8],'4-1','graphing-functions','For each tank, write down a formula which gives the depth of water in the tank at any given time. State clearly the meaning of any letters used.',tanks)
A('5-d','Q5(d)','10C',[13, 26, 27],[8, 9],'5-1','graphing-functions','For each tank, draw the graph to represent the depth of water over the 2 minutes. Use the supplied axes, time 0–120 seconds and depth 0–100 cm.',tanks)
A('5-e','Q5(e)','5B',[13, 27],[8, 9],'5-1','graphing-functions','Find, from your graphs, how much time passes before the depth of water is the same in each tank.',tanks+' Part (d): graph both depths over the first two minutes.')
A('5-f','Q5(f)','5C',[13, 27],[8, 9],'4-2','algebra-equations','Verify your answer to part (e) using your formulas from part (c).',tanks+' Part (c): write depth as a function of time for each tank. Part (e): find graphically when both depths are equal.')
salaries='Eoin and Peter began work in 2005 on starting salaries of €20 000 and €17 000 per annum, respectively. Eoin’s salary increased by €500 per annum and Peter’s by €1250 per annum. This salary pattern will continue. Year 1 is 2005.'
A('6-a','Q6(a)','15D',[14, 28],[10],'4-1','sequences-series','Complete the table, showing the annual salary of each for the years 2005 to 2010.',salaries)
A('6-b','Q6(b)','5A',[14, 28],[10],'4-1','sequences-series','In what year will both brothers earn the same amount?',salaries)
A('6-c-i','Q6(c)(i)','5B',[14, 28],[10],'4-1','sequences-series','Explain what an arithmetic sequence is.',salaries+' Eoin claims their salaries over the years can be represented by an arithmetic sequence.')
A('6-c-ii','Q6(c)(ii)','5B',[14, 28],[10],'4-1','sequences-series','Do you agree with Eoin? Explain your answer.',salaries+' Eoin claims their salaries over the years can be represented by an arithmetic sequence.')
A('6-d','Q6(d)','5B',[14, 28],[10],'4-1','sequences-series','Find, in terms of n, a formula that gives Eoin’s salary in the nth year of the pattern.',salaries)
A('6-e','Q6(e)','10C',[14, 28],[10],'4-1','sequences-series','Using your formula, or otherwise, find Eoin’s salary in 2015.',salaries+' Part (d): find Eoin’s salary in the nth year.')
A('6-f','Q6(f)','5C',[15, 29],[10, 11],'4-1','sequences-series','Find, in terms of n, a formula that gives the total amount earned by Peter from the first to the nth year of the pattern.',salaries)
A('6-g','Q6(g)','5C',[15, 29],[10, 11],'4-1','sequences-series','Using your formula, or otherwise, find the total amount earned by Peter from the start of 2005 up to the end of 2015.',salaries+' Part (f): find the sum of Peter’s first n annual salaries.')
A('6-h','Q6(h)','5B',[15, 29],[10, 11],'5-1','graphing-functions','Give one reason why the graph below is not an accurate way to represent Peter’s salary over the period 2005 to 2011.',salaries+' Refer to the original salary graph.')
A('7-a','Q7(a)','10C',[16,30],[12],'5-2','differentiation','Let y = 2x³ − 3x² − 1. Find dy/dx.')
A('7-b-i','Q7(b)(i)','5C',[16,30],[12],'5-2','differentiation','Differentiate (2x² + 3x + 1)(x³ − x + 2) with respect to x.')
A('7-b-ii','Q7(b)(ii)','10D',[16,30],[12],'5-2','differentiation','Let y = 3x/(2x + 5), where 2x + 5 ≠ 0. Find the value of dy/dx at x = 0.')
tangent='The diagram shows the quadratic function f(x) = x² + 3x − 1, x ∈ ℝ, and line l₁. Line l₁ passes through (2, 0) and is a tangent to the curve at (−1, −3).'
A('7-c-i','Q7(c)(i)','5C',[17,31],[13],'2-4','co-ordinate-geometry-of-the-line','Find the slope of l₁, using a slope formula.',tangent)
A('7-c-ii','Q7(c)(ii)','10C',[17,31],[13],'5-2','differentiation','Find f′(x), the derivative of f(x).',tangent)
A('7-c-iii','Q7(c)(iii)','5C',[17,31],[13],'5-2','differentiation','Verify your answer to (i) above by finding the value of f′(x) at x = −1.',tangent+' Part (i): find the slope of l₁.')
A('7-c-iv','Q7(c)(iv)','5C',[17,31],[13],'5-2','differentiation','Line l₂ is perpendicular to l₁ and is also a tangent to f(x). Find the co-ordinates of the point at which l₂ touches the curve.',tangent)
A('8-a','Q8(a)','15D',[18,32],[14],'5-2','differentiation','Given that f(x) = 12 − x − x², find the value of x for which f′(x) = 0, where f′(x) is the derivative of f(x).')
g='Let g(x) = x³ − 9x² + 24x − 20, where x ∈ ℝ.'
A('8-b-i','Q8(b)(i)','15D',[18,32],[14],'5-2','differentiation','Find the co-ordinates of the local maximum point and of the local minimum point of the function g.',g)
A('8-b-ii','Q8(b)(ii)','5B',[18,32],[14],'5-1','graphing-functions','Hence, draw a sketch of the function g.',g+' Part (i): find the co-ordinates of its local maximum and local minimum.')
stone='A stone is thrown vertically upwards. Its height s metres after t seconds is given by s = 5(4t − t²).'
A('8-c-i','Q8(c)(i)','5C',[19,33],[15],'5-1','graphing-functions','Find the height of the stone after 1 second.',stone)
A('8-c-ii','Q8(c)(ii)','5C',[19,33],[15],'5-2','differentiation','Show that the stone momentarily stops two seconds after being thrown, and find its height at that time.',stone)
A('8-c-iii','Q8(c)(iii)','5B',[19,33],[15],'5-2','differentiation','Show that the acceleration of the stone is constant.',stone)
marks={str(q):25 for q in range(1,5)}|{'5':40,'6':60,'7':50,'8':50}
p.check(marks|{'3':125},61)
assert sum(c['totalMarks'] for c in p.cards if not c.get('selectionVariant'))+5 == 300
assert len(ROUTES)==21
page=' '.join(fitz.open(p.P)[4].get_text().split())
assert re.search(r'Mark 5 of the numbers in the table on the number line below',page),page
p.review(marks,'Independently visually inspected all 16 original paper pages and scheme PDF pages 1–34. Each published scale is retained, including all 21 Q3(b)(ii) selections and every old-syllabus calculus task.',list(range(1,35)),[20,21],
 ['Q3(b)(ii): all C(7,5)=21 five-mark routes retained; only one route contributes to the candidate total of 300 marks.',
  'Q7 calculus tasks have seven separate published scales. Unlike the Phase 3 paper, the product and quotient rules are assessed separately and no exceptional 25C grouping applies.',
  'Eight starred tasks allow Full Credit minus one: Q1(d), Q3(a), Q4(a), Q4(c), Q5(b), Q5(e), Q8(c)(i), Q8(c)(ii).',
  'Phase 2 notes contain additional credit conditions absent from the Phase 3 scheme, retained verbatim in substance. Tank table/graph carry-forward rules accompany affected tasks.',
  'Sections A, B and C retained: Q1–4, Q5–6, Q7–8. Original graphs, number line, tables and mathematical notation retained.'],
 [{'pages':[2,3,8,12],'wording':'Answer all eight/all four/both questions','classification':'all-required','reason':'Every printed task retained.'},{'pages':[5],'wording':'Mark 5 of the numbers in the table','classification':'finite-choose-five-of-seven','reason':'All 21 combinations generated mechanically and pinned to the source wording.'},{'pages':[11],'wording':'Give one reason','classification':'open-response','reason':'No finite pool of reasons is supplied.'}],
 lambda t:('all-required','Every printed task retained.') if 'Answer all' in t or 'Answer both' in t else ('alternative-method','All valid methods preserved within one task.') if 'or otherwise' in t else None)
SCHEME_ROW_FIGURES = {'maths-2013-ol-p1-q1-a': 'maths-2013-OL-scheme-p007-i0', 'maths-2013-ol-p1-q1-b': 'maths-2013-OL-scheme-p007-i1', 'maths-2013-ol-p1-q1-c': 'maths-2013-OL-scheme-p007-i2', 'maths-2013-ol-p1-q1-d': 'maths-2013-OL-scheme-p007-i3', 'maths-2013-ol-p1-q2-a': 'maths-2013-OL-scheme-p008-i0', 'maths-2013-ol-p1-q2-b': 'maths-2013-OL-scheme-p008-i1', 'maths-2013-ol-p1-q3-a': 'maths-2013-OL-scheme-p009-i0', 'maths-2013-ol-p1-q3-b-i': 'maths-2013-OL-scheme-p009-i1', 'maths-2013-ol-p1-q3-b-ii-abcde': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-c': 'maths-2013-OL-scheme-p009-i3', 'maths-2013-ol-p1-q4-a': 'maths-2013-OL-scheme-p010-i0', 'maths-2013-ol-p1-q4-b': 'maths-2013-OL-scheme-p010-i1', 'maths-2013-ol-p1-q4-c': 'maths-2013-OL-scheme-p011-i0', 'maths-2013-ol-p1-q5-a': 'maths-2013-OL-scheme-p012-i0', 'maths-2013-ol-p1-q5-b': 'maths-2013-OL-scheme-p012-i1', 'maths-2013-ol-p1-q5-c': 'maths-2013-OL-scheme-p012-i2', 'maths-2013-ol-p1-q5-d': 'maths-2013-OL-scheme-p013-i0', 'maths-2013-ol-p1-q5-e': 'maths-2013-OL-scheme-p013-i1', 'maths-2013-ol-p1-q5-f': 'maths-2013-OL-scheme-p013-i2', 'maths-2013-ol-p1-q6-a': 'maths-2013-OL-scheme-p014-i0', 'maths-2013-ol-p1-q6-b': 'maths-2013-OL-scheme-p014-i1', 'maths-2013-ol-p1-q6-c-i': 'maths-2013-OL-scheme-p014-i2', 'maths-2013-ol-p1-q6-c-ii': 'maths-2013-OL-scheme-p014-i3', 'maths-2013-ol-p1-q6-d': 'maths-2013-OL-scheme-p014-i4', 'maths-2013-ol-p1-q6-e': 'maths-2013-OL-scheme-p014-i5', 'maths-2013-ol-p1-q6-f': 'maths-2013-OL-scheme-p015-i0', 'maths-2013-ol-p1-q6-g': 'maths-2013-OL-scheme-p015-i1', 'maths-2013-ol-p1-q6-h': 'maths-2013-OL-scheme-p015-i2', 'maths-2013-ol-p1-q7-a': 'maths-2013-OL-scheme-p016-i0', 'maths-2013-ol-p1-q7-b-i': 'maths-2013-OL-scheme-p016-i1', 'maths-2013-ol-p1-q7-b-ii': 'maths-2013-OL-scheme-p016-i2', 'maths-2013-ol-p1-q7-c-i': 'maths-2013-OL-scheme-p017-i0', 'maths-2013-ol-p1-q7-c-ii': 'maths-2013-OL-scheme-p017-i1', 'maths-2013-ol-p1-q7-c-iii': 'maths-2013-OL-scheme-p017-i2', 'maths-2013-ol-p1-q7-c-iv': 'maths-2013-OL-scheme-p017-i3', 'maths-2013-ol-p1-q8-a': 'maths-2013-OL-scheme-p018-i0', 'maths-2013-ol-p1-q8-b-i': 'maths-2013-OL-scheme-p018-i1', 'maths-2013-ol-p1-q8-b-ii': 'maths-2013-OL-scheme-p018-i2', 'maths-2013-ol-p1-q8-c-i': 'maths-2013-OL-scheme-p019-i0', 'maths-2013-ol-p1-q8-c-ii': 'maths-2013-OL-scheme-p019-i1', 'maths-2013-ol-p1-q8-c-iii': 'maths-2013-OL-scheme-p019-i2', 'maths-2013-ol-p1-q3-b-ii-abcdf': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abcdg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abcef': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abceg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abcfg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abdef': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abdeg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abdfg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-abefg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-acdef': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-acdeg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-acdfg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-acefg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-adefg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-bcdef': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-bcdeg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-bcdfg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-bcefg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-bdefg': 'maths-2013-OL-scheme-p009-i2', 'maths-2013-ol-p1-q3-b-ii-cdefg': 'maths-2013-OL-scheme-p009-i2'}
p.apply(ROWS,'2013 Ordinary Project Maths Phase 2 Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides={c['id']:{**({'figureKey':SCHEME_ROW_FIGURES[c['id']]} if c['id'] in SCHEME_ROW_FIGURES else {}),'section':'A' if int(c['printedParts'][0][1])<=4 else 'B' if int(c['printedParts'][0][1])<=6 else 'C'} for c in p.cards},question_figures=True)
