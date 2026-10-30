"""2013 Foundation Project Maths P1: independently reviewed scales and all five Q10(b,c) routes."""
import os,sys,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R={
'1':[L(LPC,'Any work of merit'),L(MPC,'One correct answer and no further work'),L(MPC,'Work of merit in only two parts'),L(HPC,'Two correct answers'),L(HPC,'Work of merit in all three parts')],
'2-a':[L(LPC,'Any work of merit'),L(MPC,'Work of merit in both parts'),L(MPC,'Part (i) or part (ii) correct only'),L(HPC,'Part (i) correct and work of merit in part (ii)'),L(HPC,'Part (ii) correct and work of merit in part (i)')],
'2-b':[L(LPC,'Any work of merit'),L(HPC,'One correct answer'),L(HPC,'Some work of merit in both parts'),L(NOTE,'Accept the use of candidates answer from part (i)')],
'3-a':[L(LPC,'Any work of merit'),L(HPC,'One correct answer'),L(HPC,'Some work of merit in both parts'),L(NOTE,'Accept the use of candidates answer from part (i) in answering part (ii)')],
'3-b':[L(LPC,'Any work of merit'),L(HPC,'One correct answer'),L(HPC,'Some work of merit in both parts')],
'4-a':[L(LPC,'Any work of merit'),L(HPC,'Gets the answer €14000 and fails to finish or finishes incorrectly')],
'4-b':[L(LPC,'Any work of merit'),L(HPC,'Correct substitution into formula and fails to finish or finishes incorrectly'),L(HPC,'Works out the amount due after two years and fails to finish or finishes incorrectly'),L(NOTE,'Accept the use of candidates answer from part (a)')],
'5-a':[L(LPC,'Any work of merit'),L(HPC,'One correct answer'),L(HPC,'Work of merit in both parts')],
'5-b':[L(PC,'Any work of merit.'),L(NOTE,'Accept the use of candidates answer from part (a)')],
'5-c':[L(LPC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from part (b)')],
'6-a':[L(LPC,'Any work of merit')],
'6-b':[L(PC,'Any work of merit')],
'6-c':[L(LPC,'Any work of merit'),L(LPC,'Incorrect factors and fails to finish'),L(LPC,'Effort at solution by trial and improvement'),L(HPC,'Correct factors, but roots not found'),L(HPC,'Incorrect factors, but finished correctly.'),L(HPC,'One correct solution from trial and improvement, but must be verified'),L(FC,'For correct solutions from trial and improvement, if both are verified')],
'7-a':[L(LPC,'Any work of merit'),L(HPC,'Multiplies out correctly and fails to finish or finishes incorrectly'),L(HPC,'One mistake in multiplication and finishes correctly')],
'7-b':[L(LPC,'Any work of merit'),L(LPC,'Attempt to solve equation by trial and improvement'),L(HPC,'Correct method but with one error'),L(FC,'Correct solution verified by trial and improvement')],
'7-c':[L(LPC,'Any work of merit'),L(LPC,'Attempt to solve equation by trial and improvement'),L(HPC,'Correct solution to equation but ignores inequality'),L(HPC,'Correct method, but with one error'),L(HPC,'Correct, verified solution by trial and improvement but without a solution set')],
'8-a-i':[L(LPC,'One or two values correct'),L(LPC,'Any work of merit'),L(HPC,'Three, four or five values correct')],
'8-a-ii':[L(PC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from (a)(i)')],
'8-a-iii':[L(PC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from (a)(ii)')],
'8-b':[L(LPC,'Any work of merit'),L(HPC,'One unknown, x or y correct')],
'9-a-i':[L(PC,'One correct answer'),L(PC,'Relevant work for both answers'),L(NOTE,'Accept the use of candidates answer from (i) when marking (ii), (iii) & (iv)')],
'9-b-i':[L(LPC,'Any work of merit'),L(HPC,'One calculation completed correctly')],
'9-b-ii':[L(LPC,'Any work of merit'),L(HPC,'Cost of accommodation or insurance worked out correctly'),L(NOTE,'Accept the use of candidates answer from part (i)')],
'9-b-iii':[L(LPC,'Any work of merit'),L(HPC,'One error in answering'),L(NOTE,'Accept the use of candidates answer from part (ii)')],
'10-a':[L(LPC,'One correct answer'),L(HPC,'Two correct answers.')],
'10-b':[L(LPC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from (b) in (c) and (d)')],
'10-d':[L(LPC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from (b) in (c) and (d)')],
'10-e':[L(LPC,'Any work of merit')],
'10-f':[L(LPC,'Any work of merit'),L(HPC,'One correct answer')],
'10-g':[L(LPC,'One correct point'),L(LPC,'Any work of merit'),L(HPC,'Two correct points'),L(FC,'Line drawn'),L(NOTE,'Accept the use of candidates answer from (e)')],
'10-h':[L(LPC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from (g)')],
}
for s in ('ii','iii','iv'):R['9-a-'+s]=[L(PC,'Any work of merit'),L(NOTE,'Accept the use of candidates answer from (i) when marking (ii), (iii) & (iv)')]
ROUTES=list(itertools.combinations(['2','3','4','5','6'],1))
for (n,) in ROUTES:R['10-b-row-'+n]=R['10-b']
del R['10-b']
ROWS={'maths-2013-fl-p1-project-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5B':[0,2,5],'5C':[0,2,4,5],'10B':[0,5,10],'10C':[0,3,7,10],'15C':[0,6,10,15],'15D':[0,4,7,11,15],'20C':[0,7,13,20],'25D':[0,6,12,19,25]}
p=Paper(2013,'fl','p1',SC,'LC003BLP130EV.pdf','LC003BLP030EV.pdf',reviewed_at='2026-10-29',edition='project',full_credit_minus_one=False)
STAR={'1','3-a','3-b','5-a','5-b','5-c'}
def A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=None,extra=None):
 e=extra or {}
 if s in STAR:e['fullCreditMinusOne']=True
 p.A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=stem,extra=e)
A('1','Q1(a),Q1(b),Q1(c)','25D',[7,22],[3],'3-1','number-systems','Use your calculator. (a) Find ∛264·3, correct to two decimal places. (b) Find the exact value of 1/(0·5)² − (1·2)³. (c) Write down the whole number closest to √70 × tan 56°.')
nums='The table lists 3, −2, −0·5, √2, 2⅔, sin 30° and π. Its columns are natural numbers ℕ, integers ℤ, rational numbers ℚ and real numbers ℝ. The original table and number line are supplied.'
A('2-a','Q2(a)(i),Q2(a)(ii)','15D',[8,22],[4],'3-1','number-systems','(i) Tick each box opposite a number if it belongs to that set. (ii) Mark every number in the table on the number line and label each clearly.',nums)
A('2-b','Q2(b)(i),Q2(b)(ii)','10C',[8,22],[4],'3-1','number-systems,arithmetic','(i) Write this distance as a whole number of kilometres. (ii) It took Apollo astronauts 3 days and 4 hours to travel from earth to the moon. Find their average speed in km per hour.','The average distance from the earth to the moon is 3·84 × 10⁵ km.')
pitch='Liam draws a soccer pitch at a scale of 1 cm = 6·25 m. His rectangle is 16 cm long and 11 cm wide; the original diagram includes the centre circle.'
A('3-a','Q3(a)(i),Q3(a)(ii)','15C',[9,23],[5],'3-4','area-volume','(i) Find the length of the soccer pitch. (ii) Find its perimeter.',pitch)
A('3-b','Q3(b)(i),Q3(b)(ii)','10C',[9,23],[5],'3-4','area-volume','The centre circle has radius 9·15 m. (i) Calculate its area on the soccer pitch. (ii) Find the correct radius for Liam’s scaled diagram.',pitch)
car='Mary buys a new car costing €26 000. The garage gives her €8400 for her old car and she has savings of €5600. She borrows the remainder.'
A('4-a','Q4(a)','20C',[10,23],[6],'3-3','arithmetic','How much does she borrow?',car)
A('4-b','Q4(b)','5C',[10,23],[6],'3-3','arithmetic','She borrows the money for three years at an annual equivalent rate (AER) of 11%. She repays all the money and interest in one repayment at the end of the three years. How much interest will she pay?',car)
net='The original diagram shows the net of a figure with a square base and four triangular sides. Each grid unit is 5 mm. The base length is labelled w and each triangular side’s height is labelled d.'
A('5-a','Q5(a)','15C',[11,24],[7],'3-4','area-volume','Find w, the length of the base, and d, the height of each triangular side.',net)
A('5-b','Q5(b)','5B',[11,24],[7],'3-4','area-volume','Find the area of the base of the figure.',net)
A('5-c','Q5(c)','5B',[11,24],[7],'3-4','area-volume','Find the total surface area of the figure.',net)
A('6-a','Q6(a)','15C',[12,24],[8],'4-1','algebra','Find the value of a² + b² when a = 20 and b = 21.')
A('6-b','Q6(b)','5B',[12,24],[8],'4-1','algebra','Given that a² + b² = c², find the value of c.','In part (a), a = 20 and b = 21.')
A('6-c','Q6(c)','5C',[12,24],[8],'4-2','algebra','Solve the equation x² − 3x − 10 = 0.')
A('7-a','Q7(a)','5C',[13,25],[9],'4-1','algebra','Simplify 2(3x − 6) − (4x − 8).')
A('7-b','Q7(b)','15C',[13,25],[9],'4-2','algebra','Solve the equation 7x − 4 = 5x + 16.')
A('7-c','Q7(c)','5C',[13,25],[9],'4-2','algebra','Write down the natural numbers which satisfy 3x − 2 ≤ 13.')
lines='The two lines are x − y = 1 and 3x + y = 7. Both tables use x = −1, 1, 3. The first has rows x, −1, y and already gives y = −2, 0 for x = −1, 1; the second has rows −3x, +7, y and already gives y = 10, −2 for x = −1, 3.'
A('8-a-i','Q8(a)(i)','10C',[14,26],[10],'5-1','graphs-of-functions','Complete the two tables for the lines.',lines)
A('8-a-ii','Q8(a)(ii)','5B',[14,26],[10],'5-1','graphs-of-functions','Draw the graph of each line on the supplied grid.',lines)
A('8-a-iii','Q8(a)(iii)','5B',[14,26],[10],'5-1','graphs-of-functions','Write down the co-ordinates of the point at which the lines cross on your graph.',lines+' Part (ii): draw both lines on the supplied grid.')
A('8-b','Q8(b)','5C',[15,26],[11],'4-2','algebra','Solve the simultaneous equations x − y = 1 and 3x + y = 7.')
travel='Mr and Mrs Murphy and their three children plan a week’s holiday from Dublin to Arrecife. Outbound E107 operates Monday, Thursday, Friday and Saturday, 06:45–10:40; E117 Saturday, 13:15–17:25. Return E108 operates Monday, Thursday, Friday and Saturday, 11:55–15:55; E118 Saturday, 18:40–22:35. They book the early outbound flight on Saturday and the latest return flight on the following Saturday afternoon.'
A('9-a-i','Q9(a)(i)','10B',[16,27],[12],'3-1','arithmetic','Give the flight numbers for both their outbound flight and their return flight.',travel)
A('9-a-ii','Q9(a)(ii)','5B',[16,27],[12],'3-1','arithmetic','The latest check-in time at Dublin is 1 hour 50 minutes before departure. What is the latest check-in time for their outbound flight?',travel)
A('9-a-iii','Q9(a)(iii)','5B',[16,27],[12],'3-1','arithmetic','How long does their flight from Dublin to Arrecife take?',travel)
A('9-a-iv','Q9(a)(iv)','5B',[16,27],[12],'3-1','arithmetic','Their return flight is delayed by 1 hour 40 minutes. At what time does it arrive back in Dublin?',travel)
cost='The Murphy family consists of two adults and three children. Return airfare is €360 per adult and €270 per child. A week’s hotel accommodation costs €420 per adult and €210 for each of the first two children; the third child is free. Insurance costs €18·75 per person.'
A('9-b-i','Q9(b)(i)','10C',[17,27],[12,13],'3-3','arithmetic','Find the total cost of the airfares for the Murphy family.',cost)
A('9-b-ii','Q9(b)(ii)','5C',[17,27],[12,13],'3-3','arithmetic','Find the total cost of the holiday for the Murphy family.',cost)
A('9-b-iii','Q9(b)(iii)','10C',[17,27],[12,13],'3-3','arithmetic','An internet booking gives a discount of 5% of the total cost. How much money could the Murphys save?',cost)
fence='Jim builds a fence with three horizontal rails between each two vertical posts. The original diagrams show two, three and four posts. The table has post counts x = 2, 3, 4, 5, 6, with rail counts y = 3, 6 and three blanks.'
jim='Jim’s rule: subtract 1 from the number of posts and multiply the answer by 3.'
ann='Ann’s rule: multiply the number of posts by 3, then subtract 3.'
A('10-a','Q10(a)','15C',[18,28],[14],'4-1','algebra','Complete the table.',fence)
for (n,) in ROUTES:
 A('10-b-row-'+n,'Q10(b),Q10(c)','5B',[18,28],[14],'4-1','algebra','(b) Write an algebraic expression for Jim’s rule using x for posts and y for rails. (c) Test your expression using the table row with '+n+' posts. This is one of the five valid row selections.',fence+' '+jim,{'selectionVariant':{'groupId':'q10-b-c','pool':['2','3','4','5','6'],'choose':1,'selected':[n],'practiceInstruction':'For this practice, test Jim’s expression using the row with '+n+' posts. The original question allows any one of the five rows.','sourcePage':14,'sourceDirective':'Test your expression in (b) above using the numbers in one row of the table.'}})
A('10-d','Q10(d)','5B',[18,28],[14],'4-1','algebra','Jim uses 60 posts. Find the number of rails he needs.',fence+' '+jim)
A('10-e','Q10(e)','5B',[18,28],[14],'4-1','algebra','Write an algebraic expression for Ann’s rule using x for posts and y for rails.',fence+' '+ann)
A('10-f','Q10(f)(i),Q10(f)(ii)','5C',[19,28],[14,15],'4-1','algebra','Use Ann’s rule. (i) Find how many rails are needed for 10 posts. (ii) Find how many posts are used if 228 rails are needed.',fence+' '+ann)
A('10-g','Q10(g)','10C',[19,28],[14,15],'5-1','graphs-of-functions','Draw the graph representing Ann’s rule for 0 ≤ x ≤ 75, x ∈ ℝ, on the supplied grid.',fence+' '+ann)
A('10-h','Q10(h)','5B',[19,28],[14,15],'5-1','graphs-of-functions','Ann needs 180 rails for another fence built in the same way. Use your graph to find the number of posts.',fence+' '+ann+' Part (g): draw the graph for 0 ≤ x ≤ 75.')
marks={str(q):25 for q in range(1,9)}|{'9':50,'10':50}
p.check(marks|{'10':70},38)
assert sum(c['totalMarks'] for c in p.cards if not c.get('selectionVariant'))+5==300
page=' '.join(fitz.open(p.P)[13].get_text().split())
assert 'Test your expression in (b) above using the numbers in one row of the table.' in page
p.review(marks,'Independent visual inspection of all 16 original paper pages and scheme PDF pages 1–28. All 34 published scale units retained; five finite Q10(b,c) row routes generated mechanically, giving 38 cards.',list(range(1,29)),[20,21],
 ['Q1(a,b,c) is one 25D task. Q2(a), Q2(b), Q3(a), Q3(b), Q10(f) retain shared scales; Q10(b,c) is one 5B task for each of five row choices. Candidate tariff remains 300 marks.',
 'Only Q1, Q3(a,b) and Q5(a,b,c) allow Full Credit minus one. Foundation has its own 5B, 5C, 10C, 15C and 20C ladders; Q2(a) uses 15D 0,4,7,11,15 from the detailed notes.',
 'Every original table, number line, net, flight timetable and graph grid is retained with required prior context. Required number-set rows are not optional answer routes.',
 'The detailed notes incorrectly label the final section C; the original paper and allocation summary identify Section B, questions 9–10. Q6(a) high partial criterion contains mathematical glyphs and is preserved in the complete printed solution/notes image.'],
 [{'pages':[2,3,12],'wording':'Answer all ten questions; Answer all eight questions; Answer both Question 9 and Question 10.','classification':'all-required','reason':'Every printed task retained.'},{'pages':[14],'wording':'using the numbers in one row of the table','classification':'finite-choose-one-of-five','reason':'Five row routes generated, each sharing the complete Q10(b,c) 5B task.'},{'pages':[4,10,14],'wording':'Tick each box; Mark each of the numbers; complete the tables','classification':'all-required-entries','reason':'Every table entry is required; no optional pool.'}],
 lambda t:('all-required','All questions in both sections retained.') if 'Answer all' in t or 'Answer both' in t else ('finite-choose-one-of-five','All five table-row routes retained.') if 'one row' in t else None)
SCHEME_ROW_FIGURES={'maths-2013-fl-p1-project-q1': 'maths-2013-FL-scheme-project-p007-i0', 'maths-2013-fl-p1-project-q2-a': 'maths-2013-FL-scheme-project-p008-i0', 'maths-2013-fl-p1-project-q2-b': 'maths-2013-FL-scheme-project-p008-i1', 'maths-2013-fl-p1-project-q3-a': 'maths-2013-FL-scheme-project-p009-i0', 'maths-2013-fl-p1-project-q3-b': 'maths-2013-FL-scheme-project-p009-i1', 'maths-2013-fl-p1-project-q4-a': 'maths-2013-FL-scheme-project-p010-i0', 'maths-2013-fl-p1-project-q4-b': 'maths-2013-FL-scheme-project-p010-i1', 'maths-2013-fl-p1-project-q5-a': 'maths-2013-FL-scheme-project-p011-i0', 'maths-2013-fl-p1-project-q5-b': 'maths-2013-FL-scheme-project-p011-i1', 'maths-2013-fl-p1-project-q5-c': 'maths-2013-FL-scheme-project-p011-i2', 'maths-2013-fl-p1-project-q6-a': 'maths-2013-FL-scheme-project-p012-i0', 'maths-2013-fl-p1-project-q6-b': 'maths-2013-FL-scheme-project-p012-i1', 'maths-2013-fl-p1-project-q6-c': 'maths-2013-FL-scheme-project-p012-i2', 'maths-2013-fl-p1-project-q7-a': 'maths-2013-FL-scheme-project-p013-i0', 'maths-2013-fl-p1-project-q7-b': 'maths-2013-FL-scheme-project-p013-i1', 'maths-2013-fl-p1-project-q7-c': 'maths-2013-FL-scheme-project-p013-i2', 'maths-2013-fl-p1-project-q8-a-i': 'maths-2013-FL-scheme-project-p014-i0', 'maths-2013-fl-p1-project-q8-a-ii': 'maths-2013-FL-scheme-project-p014-i1', 'maths-2013-fl-p1-project-q8-a-iii': 'maths-2013-FL-scheme-project-p014-i2', 'maths-2013-fl-p1-project-q8-b': 'maths-2013-FL-scheme-project-p015-i0', 'maths-2013-fl-p1-project-q9-a-i': 'maths-2013-FL-scheme-project-p016-i0', 'maths-2013-fl-p1-project-q9-a-ii': 'maths-2013-FL-scheme-project-p016-i1', 'maths-2013-fl-p1-project-q9-a-iii': 'maths-2013-FL-scheme-project-p016-i2', 'maths-2013-fl-p1-project-q9-a-iv': 'maths-2013-FL-scheme-project-p016-i3', 'maths-2013-fl-p1-project-q9-b-i': 'maths-2013-FL-scheme-project-p017-i0', 'maths-2013-fl-p1-project-q9-b-ii': 'maths-2013-FL-scheme-project-p017-i1', 'maths-2013-fl-p1-project-q9-b-iii': 'maths-2013-FL-scheme-project-p017-i2', 'maths-2013-fl-p1-project-q10-a': 'maths-2013-FL-scheme-project-p018-i0', 'maths-2013-fl-p1-project-q10-b-row-2': 'maths-2013-FL-scheme-project-p018-i1', 'maths-2013-fl-p1-project-q10-d': 'maths-2013-FL-scheme-project-p018-i2', 'maths-2013-fl-p1-project-q10-e': 'maths-2013-FL-scheme-project-p018-i3', 'maths-2013-fl-p1-project-q10-f': 'maths-2013-FL-scheme-project-p019-i0', 'maths-2013-fl-p1-project-q10-g': 'maths-2013-FL-scheme-project-p019-i1', 'maths-2013-fl-p1-project-q10-h': 'maths-2013-FL-scheme-project-p019-i2', 'maths-2013-fl-p1-project-q10-b-row-3': 'maths-2013-FL-scheme-project-p018-i1', 'maths-2013-fl-p1-project-q10-b-row-4': 'maths-2013-FL-scheme-project-p018-i1', 'maths-2013-fl-p1-project-q10-b-row-5': 'maths-2013-FL-scheme-project-p018-i1', 'maths-2013-fl-p1-project-q10-b-row-6': 'maths-2013-FL-scheme-project-p018-i1'}
overrides={c['id']:{'section':'A' if int(re.match(r'Q(\d+)',c['printedParts'][0])[1])<=8 else 'B',**({'figureKey':SCHEME_ROW_FIGURES[c['id']]} if c['id'] in SCHEME_ROW_FIGURES else {})} for c in p.cards}
p.apply(ROWS,'2013 Foundation Project Maths Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides=overrides,question_figures=True)
