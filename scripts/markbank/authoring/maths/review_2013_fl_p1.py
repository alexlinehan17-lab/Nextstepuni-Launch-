"""2013 Foundation Phase 2 P1: independently reviewed scales and all five Q9(b,c) routes."""
import os,sys,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R={'1': ['Low Partial Credit — Any work of merit',
       'Mid Partial Credit — One correct answer and no further work',
       'Mid Partial Credit — Work of merit in only two parts',
       'High Partial Credit — Two correct answers',
       'High Partial Credit — Work of merit in all three parts'],
 '2-a': ['Low Partial Credit — Any work of merit',
         'Mid Partial Credit — Work of merit in both parts',
         'Mid Partial Credit — Part (i) or part (ii) correct only',
         'High Partial Credit — Part (i) correct and work of merit in part (ii)',
         'High Partial Credit — Part (ii) correct and work of merit in part (i)'],
 '2-b': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — One correct answer',
         'High Partial Credit — Some work of merit in both parts',
         'Note — Accept the use of candidates answer from part (i)'],
 '3-a': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — One correct answer',
         'High Partial Credit — Some work of merit in both parts',
         'Note — Accept the use of candidates answer from part (i) in answering part (ii)'],
 '3-b': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — One correct answer',
         'High Partial Credit — Some work of merit in both parts'],
 '4-a': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — Gets the answer €14000 and fails to finish or finishes incorrectly'],
 '4-b': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — Correct substitution into formula and fails to finish or finishes incorrectly',
         'High Partial Credit — Works out the amount due after two years and fails to finish or finishes incorrectly',
         'Note — Accept the use of candidates answer from part (a)'],
 '5-a': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — One correct answer',
         'High Partial Credit — Work of merit in both parts'],
 '5-b': ['Partial Credit — Any work of merit.', 'Note — Accept the use of candidates answer from part (a)'],
 '5-c': ['Partial Credit — Any work of merit', 'Note — Accept the use of candidates answer from part (b)'],
 '6-a': ['Low Partial Credit — Any work of merit', 'High Partial Credit — Correctly finds a² and b² and fails to add'],
 '6-b': ['Partial Credit — Any work of merit'],
 '6-c': ['Low Partial Credit — Any work of merit',
         'Low Partial Credit — Incorrect factors and fails to finish',
         'Low Partial Credit — Effort at solution by trial and improvement',
         'High Partial Credit — Correct factors, but roots not found',
         'High Partial Credit — Incorrect factors, but finished correctly.',
         'High Partial Credit — One correct solution from trial and improvement, but must be verified',
         'Full Credit — For correct solutions from trial and improvement, if both are verified'],
 '7-a': ['Low Partial Credit — Any work of merit',
         'High Partial Credit — Multiplies out correctly and fails to finish or finishes incorrectly',
         'High Partial Credit — One mistake in multiplication and finishes correctly'],
 '7-b': ['Low Partial Credit — Any work of merit',
         'Low Partial Credit — Attempt to solve equation by trial and improvement',
         'High Partial Credit — Correct method but with one error',
         'Full Credit — Correct solution verified by trial and improvement'],
 '7-c': ['Low Partial Credit — Any work of merit',
         'Low Partial Credit — Attempt to solve equation by trial and improvement',
         'High Partial Credit — Correct solution to equation but ignores inequality',
         'High Partial Credit — Correct method, but with one error',
         'High Partial Credit — Correct, verified solution by trial and improvement but without a solution set'],
 '8-a-i': ['Partial Credit — One correct answer',
           'Partial Credit — Relevant work for both answers',
           'Note — Accept the use of candidates answer from (a)(i) when marking (a)(ii), (a)(iii) & (a)(iv)'],
 '8-b-i': ['Low Partial Credit — Any work of merit', 'High Partial Credit — One calculation completed correctly'],
 '8-b-ii': ['Low Partial Credit — Any work of merit',
            'High Partial Credit — Cost of accommodation or insurance worked out correctly',
            'Note — Accept the use of candidates answer from (b)(i)'],
 '9-a': ['Low Partial Credit — One correct answer', 'High Partial Credit — Two correct answers.'],
 '9-b': ['Partial Credit — Any work of merit', 'Note — Accept the use of candidates answer from (b) in (c) and (d)'],
 '9-d': ['Partial Credit — Any work of merit', 'Note — Accept the use of candidates answer from (b) in (c) and (d)'],
 '9-e': ['Partial Credit — Any work of merit'],
 '9-f': ['Low Partial Credit — Any work of merit', 'High Partial Credit — One correct answer'],
 '8-a-ii': ['Partial Credit — Any work of merit',
            'Note — Accept the use of candidates answer from (a)(i) when marking (a)(ii), (a)(iii) & (a)(iv)'],
 '8-a-iii': ['Partial Credit — Any work of merit',
             'Note — Accept the use of candidates answer from (a)(i) when marking (a)(ii), (a)(iii) & (a)(iv)'],
 '8-a-iv': ['Partial Credit — Any work of merit',
            'Note — Accept the use of candidates answer from (a)(i) when marking (a)(ii), (a)(iii) & (a)(iv)'],
 '10-a': ['Points / Low Partial Credit — One point correct',
          'Points / Low Partial Credit — Any work of merit',
          'Points / Mid Partial Credit — Two or three points correct',
          'Points / High Partial Credit — Four or five points correct',
          'Graph / Low Partial Credit — One, two or three points plotted correctly',
          'Graph / Low Partial Credit — Any work of merit',
          'Graph / High Partial Credit — Four, five or six points plotted correctly',
          'Graph / Full Credit — All points plotted and curve completed correctly'],
 '10-b': ['Low Partial Credit — One or two correct answers',
          'Low Partial Credit — Any work of merit',
          'High Partial Credit — Three correct answers']}
ROUTES=list(itertools.combinations(['2','3','4','5','6'],1))
for (n,) in ROUTES:R['9-b-row-'+n]=R['9-b']
del R['9-b']
ROWS={'maths-2013-fl-p1-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5B':[0,2,5],'5C':[0,2,4,5],'10B':[0,5,10],'10C':[0,3,7,10],'15C':[0,6,10,15],'15D':[0,4,7,11,15],'20C':[0,7,13,20],'25D':[0,6,12,19,25]}
p=Paper(2013,'fl','p1',SC,'LC003BLP100EV.pdf','LC003BLP000EV.pdf',reviewed_at='2026-10-29',full_credit_minus_one=False)
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
travel='Mr and Mrs Murphy and their three children plan a week’s holiday from Dublin to Arrecife. Outbound E107 operates Monday, Thursday, Friday and Saturday, 06:45–10:40; E117 Saturday, 13:15–17:25. Return E108 operates Monday, Thursday, Friday and Saturday, 11:55–15:55; E118 Saturday, 18:40–22:35. They book the early outbound flight on Saturday and the latest return flight on the following Saturday afternoon.'
A('8-a-i','Q8(a)(i)','10B',[14, 26],[10],'3-1','arithmetic','Give the flight numbers for both their outbound flight and their return flight.',travel)
A('8-a-ii','Q8(a)(ii)','5B',[14, 26],[10],'3-1','arithmetic','The latest check-in time at Dublin is 1 hour 50 minutes before departure. What is the latest check-in time for their outbound flight?',travel)
A('8-a-iii','Q8(a)(iii)','5B',[14, 26],[10],'3-1','arithmetic','How long does their flight from Dublin to Arrecife take?',travel)
A('8-a-iv','Q8(a)(iv)','5B',[14, 26],[10],'3-1','arithmetic','Their return flight is delayed by 1 hour 40 minutes. At what time does it arrive back in Dublin?',travel)
cost='The Murphy family consists of two adults and three children. Return airfare is €360 per adult and €270 per child. A week’s hotel accommodation costs €420 per adult and €210 for each of the first two children; the third child is free. Insurance costs €18·75 per person.'
A('8-b-i','Q8(b)(i)','10C',[15, 26],[10, 11],'3-3','arithmetic','Find the total cost of the airfares for the Murphy family.',cost)
A('8-b-ii','Q8(b)(ii)','5C',[15, 26],[10, 11],'3-3','arithmetic','Find the total cost of the holiday for the Murphy family.',cost)
fence='Jim builds a fence with three horizontal rails between each two vertical posts. The original diagrams show two, three and four posts. The table has post counts x = 2, 3, 4, 5, 6, with rail counts y = 3, 6 and three blanks.'
jim='Jim’s rule: subtract 1 from the number of posts and multiply the answer by 3.'
ann='Ann’s rule: multiply the number of posts by 3, then subtract 3.'
A('9-a','Q9(a)','15C',[16, 27],[12],'4-1','algebra','Complete the table.',fence)
for (n,) in ROUTES:
 A('9-b-row-'+n,'Q9(b),Q9(c)','5B',[16, 27],[12],'4-1','algebra','(b) Write an algebraic expression for Jim’s rule using x for posts and y for rails. (c) Test your expression using the table row with '+n+' posts. This is one of the five valid row selections.',fence+' '+jim,{'selectionVariant':{'groupId':'q9-b-c','pool':['2','3','4','5','6'],'choose':1,'selected':[n],'practiceInstruction':'For this practice, test Jim’s expression using the row with '+n+' posts. The original question allows any one of the five rows.','sourcePage':12,'sourceDirective':'Test your expression in (b) above using the numbers in one row of the table.'}})
A('9-d','Q9(d)','5B',[16, 27],[12],'4-1','algebra','Jim uses 60 posts. Find the number of rails he needs.',fence+' '+jim)
A('9-e','Q9(e)','5B',[16, 27],[12],'4-1','algebra','Write an algebraic expression for Ann’s rule using x for posts and y for rails.',fence+' '+ann)
A('9-f','Q9(f)(i),Q9(f)(ii)','5C',[17, 27],[12, 13],'4-1','algebra','Use Ann’s rule. (i) Find how many rails are needed for 10 posts. (ii) Find how many posts are used if 228 rails are needed.',fence+' '+ann)
function='Let f(x) = 2x² − 3x − 6, for −2 ≤ x ≤ 3, x ∈ ℝ.'
p.C('10-a','Q10(a)',[{'id':'points','label':'Points','code':'25D'},{'id':'graph','label':'Graph','code':'10C','fullCreditMinusOne':True}],[18,28],[14],'5-1','graphs-of-functions','Draw the graph of the function f on the supplied grid.',stem=function)
A('10-b','Q10(b)(i),Q10(b)(ii),Q10(b)(iii),Q10(b)(iv)','15C',[18,19,28],[14,15],'5-1','graphs-of-functions','Use your graph to estimate: (i) f(1·5); (ii) the minimum value of f(x); (iii) the values of x for which f(x) = 2; (iv) the range of values of x for which f(x) is decreasing.',function+' Part (a): draw the graph on the supplied grid.')
marks={str(q):25 for q in range(1,8)}|{'8':40,'9':35,'10':50}
p.check(marks|{'9':55},33)
assert sum(c['totalMarks'] for c in p.cards if not c.get('selectionVariant'))+5==300
assert len(ROUTES)==5
page=' '.join(fitz.open(p.P)[11].get_text().split())
assert 'Test your expression in (b) above using the numbers in one row of the table.' in page
p.review(marks,'Independent visual inspection of all 16 original paper pages and scheme PDF pages 1–28. All 29 printed task groups (30 component scales) retained; five finite Q9(b,c) row routes generated mechanically, giving 33 cards.',list(range(1,29)),[20,21],
 ['Q1(a,b,c) is one 25D task. Q2(a), Q2(b), Q3(a), Q3(b), Q9(f) and all four Q10(b) read-offs retain shared scales. Q9(b,c) is one 5B task for each of five row choices. Candidate tariff remains 300 marks.',
 'Six whole-task starred units: Q1, Q3(a,b), Q5(a,b,c). Q10(a) has independent Points 25D and Graph 10C components; only Graph permits Full Credit minus one. It does not depend on full points credit.',
 'Foundation scales: 5B 0,2,5; 5C 0,2,4,5; 10B 0,5,10; 10C 0,3,7,10; 15C 0,6,10,15; 20C 0,7,13,20; 25D 0,6,12,19,25. Q2(a) uses 15D 0,4,7,11,15 from the detailed notes.',
 'Every original table, number line, pyramid net, flight timetable, fence diagram and graph grid retained with prior context. Required entries are not optional answer routes.',
 'Sections A/B/C follow the original paper and scheme: Q1–7, Q8–9, Q10. Graph-reading estimates retain all four official answers. No Phase 3-only simultaneous-equation or discount tasks imported.'],
 [{'pages':[2,3,10,14],'wording':'Answer all ten questions; Answer all seven questions; Answer both Question 8 and Question 9; Answer Question 10','classification':'all-required','reason':'Every task across all three sections retained.'},{'pages':[12],'wording':'using the numbers in one row of the table','classification':'finite-choose-one-of-five','reason':'All five row routes generated at the joint Q9(b,c) 5B boundary.'},{'pages':[4,12],'wording':'Tick each box; Mark each of the numbers; complete the table','classification':'all-required-entries','reason':'Every table entry is required; no optional pool.'}],
 lambda t:('all-required','All required questions in all three sections retained.') if 'Answer all' in t or 'Answer both' in t else ('finite-choose-one-of-five','All five table-row routes retained.') if 'one row' in t else None)
SCHEME_ROW_FIGURES = {'maths-2013-fl-p1-q1': 'maths-2013-FL-scheme-p007-i0', 'maths-2013-fl-p1-q2-a': 'maths-2013-FL-scheme-p008-i0', 'maths-2013-fl-p1-q2-b': 'maths-2013-FL-scheme-p008-i1', 'maths-2013-fl-p1-q3-a': 'maths-2013-FL-scheme-p009-i0', 'maths-2013-fl-p1-q3-b': 'maths-2013-FL-scheme-p009-i1', 'maths-2013-fl-p1-q4-a': 'maths-2013-FL-scheme-p010-i0', 'maths-2013-fl-p1-q4-b': 'maths-2013-FL-scheme-p010-i1', 'maths-2013-fl-p1-q5-a': 'maths-2013-FL-scheme-p011-i0', 'maths-2013-fl-p1-q5-b': 'maths-2013-FL-scheme-p011-i1', 'maths-2013-fl-p1-q5-c': 'maths-2013-FL-scheme-p011-i2', 'maths-2013-fl-p1-q6-a': 'maths-2013-FL-scheme-p012-i0', 'maths-2013-fl-p1-q6-b': 'maths-2013-FL-scheme-p012-i1', 'maths-2013-fl-p1-q6-c': 'maths-2013-FL-scheme-p012-i2', 'maths-2013-fl-p1-q7-a': 'maths-2013-FL-scheme-p013-i0', 'maths-2013-fl-p1-q7-b': 'maths-2013-FL-scheme-p013-i1', 'maths-2013-fl-p1-q7-c': 'maths-2013-FL-scheme-p013-i2', 'maths-2013-fl-p1-q8-a-i': 'maths-2013-FL-scheme-p014-i0', 'maths-2013-fl-p1-q8-a-ii': 'maths-2013-FL-scheme-p014-i1', 'maths-2013-fl-p1-q8-a-iii': 'maths-2013-FL-scheme-p014-i2', 'maths-2013-fl-p1-q8-a-iv': 'maths-2013-FL-scheme-p014-i3', 'maths-2013-fl-p1-q8-b-i': 'maths-2013-FL-scheme-p015-i0', 'maths-2013-fl-p1-q8-b-ii': 'maths-2013-FL-scheme-p015-i1', 'maths-2013-fl-p1-q9-a': 'maths-2013-FL-scheme-p016-i0', 'maths-2013-fl-p1-q9-b-row-2': 'maths-2013-FL-scheme-p016-i1', 'maths-2013-fl-p1-q9-d': 'maths-2013-FL-scheme-p016-i2', 'maths-2013-fl-p1-q9-e': 'maths-2013-FL-scheme-p016-i3', 'maths-2013-fl-p1-q9-f': 'maths-2013-FL-scheme-p017-i0', 'maths-2013-fl-p1-q10-a': 'maths-2013-FL-scheme-p018-i0', 'maths-2013-fl-p1-q10-b': 'maths-2013-FL-scheme-p019-i0', 'maths-2013-fl-p1-q9-b-row-3': 'maths-2013-FL-scheme-p016-i1', 'maths-2013-fl-p1-q9-b-row-4': 'maths-2013-FL-scheme-p016-i1', 'maths-2013-fl-p1-q9-b-row-5': 'maths-2013-FL-scheme-p016-i1', 'maths-2013-fl-p1-q9-b-row-6': 'maths-2013-FL-scheme-p016-i1'}
overrides={c['id']:{'section':'A' if int(re.match(r'Q(\d+)',c['printedParts'][0])[1])<=7 else 'B' if int(re.match(r'Q(\d+)',c['printedParts'][0])[1])<=9 else 'C',**({'figureKey':SCHEME_ROW_FIGURES[c['id']]} if c['id'] in SCHEME_ROW_FIGURES else {})} for c in p.cards}
p.apply(ROWS,'2013 Foundation Project Maths Phase 2 Paper 1',expect_added=[c['id'] for c in p.cards],card_overrides=overrides,question_figures=True)
