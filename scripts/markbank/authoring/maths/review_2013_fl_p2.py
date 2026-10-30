"""Independently inspected 2013 Foundation Phase 2 P2, including every finite menu route."""
import os,sys,itertools
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R={}
def bands(k,lo=None,mid=None,hi=None,partial=None):
 R[k]=[L(label,s) for label,values in [(LPC,lo),(MPC,mid),(HPC,hi),(PC,partial)] for s in (values or [])]
for k in ('1-a-i','1-a-ii'):bands(k,['One correct answer or relevant work'],hi=['Two correct answers'])
bands('1-b-i',partial=['Any work of merit'])
for k in ('1-b-ii','1-b-iii'):bands(k,['Any work of merit'],hi=['Correct numerator or correct denominator','Inverted fraction'])
for k in ('2-a-i','2-a-ii'):bands(k,['One correct value'],hi=['Correct values chosen'])
bands('2-b',['One correct entry or relevant work'],['Two or three correct entries'],['Four correct entries'])
bands('2-c',['One correct part or relevant work'],hi=['Two correct parts'])
bands('3-a',['One course correct','Any work of merit'],hi=['Two courses correct'])
bands('3-b',['Any work of merit'],hi=['4 × 3 × 5 without evaluating','Answer of 12 given'])
bands('3-c',['Any work of merit'],['One correct answer'],['Two correct answers'])
for k in ('4-a','4-b','4-c','4-d'):bands(k,partial=['Any work of merit'])
bands('4-e',['Less than three correct entries'],hi=['Three or more correct entries'])
bands('5-a',['Any work of merit'],hi=['One point correct','x and y co-ordinates obviously interchanged'])
bands('5-b-i',['Incorrect midpoint identified'],hi=['Correct midpoint of [AC] or [BC]'])
for k in ('5-b-ii','5-c','6-b'):bands(k,['Identifies the correct formula'],hi=['Substitutes incorrectly into formula and finishes'])
bands('6-a',['Any work of merit'],['One plot correct'],['Any two plots correct','x and y co-ordinates interchanged with line drawn'])
bands('6-c',['Any meaningful attempt at a correct reason'],hi=['Correct assumption with no reason given'])
bands('7-a',['Any work of merit'],['Image of one side constructed'],['Image of two sides constructed or incorrect scale factor'])
for k in ('7-b-i','7-b-ii'):bands(k,['Any work of merit'],hi=['Correct use of scale factor'])
bands('7-b-iii',['Any work of merit e.g. formula written'],hi=['Substitutes incorrectly into formula and finishes'])
bands('8a-a',['One side constructed or relevant work'],['Two sides constructed'],['Two sides and angle constructed'])
bands('8a-b',['Any work of merit'],['Image of one side constructed'],['Image of two sides constructed'])
bands('8a-c',partial=['Measures incorrect angle'])
bands('8b-a',partial=['Any work of merit'])
bands('8b-b',['Relevant geometrical statement'],hi=['Some relevant with work ∠DAB'])
bands('8b-c',partial=['Identifies a line correctly'])
bands('8b-d',['Relevant geometrical statement'],hi=['Correct assumption but no reason given'])
bands('8b-e',['Image of one side or one point constructed'],hi=['Image of two or three sides constructed'])
bands('9-a',partial=['Incorrect day chosen'])
bands('9-b',['One amount identified'],hi=['Highest and lowest amounts identified'])
bands('9-c',['Any work of merit'],hi=['Diagram mainly correct but with some error(s)'])
bands('9-d',['Any work of merit'],['Numerator or denominator correct'],['Numerator and denominator correct'])
bands('9-e',['Any work of merit'],['Calculates amount spent Monday to Friday'],['Calculates amount spent on Saturday and Sunday'])
bands('9-f',['Any work of merit'],hi=['Calculates relevant mean amount'])
bands('10-a-i',partial=['Any work of merit'])
bands('10-a-ii',['Any work of merit'],hi=['Equation formulated correctly'])
bands('10-b-i',['Any work of merit'],hi=['α = tan⁻¹(70/50) or similar'])
bands('10-b-ii',['Any work of merit'],hi=['Pythagoras substituted correctly'])
bands('10-c',['Any work of merit e.g. formula written'],['Some correct substitution'],['Fully correct substitution but error(s) made in calculation'])
STARTERS=['Melon','Soup','Goats cheese salad','Smoked salmon']
MAINS=['Roast beef','Fish of the day','Vegetation curry']
DESSERTS=['Fruit salad','Chocolate brownie','Apple crumble','Pear flan','Ice cream']
MEALS=list(itertools.product(STARTERS,MAINS,DESSERTS))
MEAL_POOL=[' / '.join(x) for x in MEALS]
for i in range(60):R[f'3-a-meal-{i+1:02}']=R['3-a']
del R['3-a']
for route in ('ab-dc','ad-bc'):R['8b-c-'+route]=R['8b-c']
del R['8b-c']
ROWS={'maths-2013-fl-p2-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5B':[0,2,5],'5C':[0,3,4,5],'5D':[0,2,3,4,5],'10C':[0,4,8,10],'10D':[0,4,8,9,10],'15B':[0,7,15],'15C':[0,5,13,15],'15D':[0,4,8,12,15]}
p=Paper(2013,'fl','p2',SC,'LC003BLP200EV.pdf','LC003BLP000EV.pdf',reviewed_at='2026-10-29',full_credit_minus_one=False)
STAR={'7-b-i','7-b-ii','7-b-iii','8b-a','10-a-ii','10-b-ii','10-c'}
def A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=None,extra=None):
 e=extra or {}
 if s in STAR:e['fullCreditMinusOne']=True
 if s in {'7-a','8a-a','8a-b','8a-c','8b-e'}:e['measurementRequired']=True
 p.A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=stem,extra=e)
def variant(group,pool,selected,page,directive,instruction):return {'selectionVariant':{'groupId':group,'pool':pool,'choose':1,'selected':[selected],'practiceInstruction':instruction,'sourcePage':page,'sourceDirective':directive}}
A('1-a-i','Q1(a)(i)','5C',[31,48],[3],'1-2','probability','Give the probability of each event: certain to happen; will never happen; has a 50:50 chance of happening.')
A('1-a-ii','Q1(a)(ii)','5C',[31,48],[3],'1-2','probability','A standard fair die is tossed. Give one example of each: an event with a 50:50 chance of happening; an event that will never happen; an event certain to happen.')
venn='The Venn diagram represents 30 students studying German and French: 10 study German only, 5 study both, and 15 study French only.'
A('1-b-i','Q1(b)(i)','5B',[31,48],[3],'1-2','probability','How many students study both German and French?',venn)
A('1-b-ii','Q1(b)(ii)','5C',[31,48],[3],'1-2','probability','A student is picked at random. Find the probability that the student studies both German and French.',venn)
A('1-b-iii','Q1(b)(iii)','5C',[31,48],[3],'1-2','probability','A student is picked at random. Find the probability that the student studies French but not German.',venn)
blood='The paper’s blood-group table gives percentages O+: 8, O−: 47, A+: 5, A−: 26, B+: 2, B−: 9, AB+: 1, AB−: 2. The + and − signs indicate rhesus positive and negative.'
A('2-a-i','Q2(a)(i)','10C',[32,49],[4],'1-2','probability','Find the percentage of the population in blood group O.',blood)
A('2-a-ii','Q2(a)(ii)','5C',[32,49],[4],'1-2','probability','Find the percentage of the population with rhesus positive blood.',blood)
A('2-b','Q2(b)','5D',[32,49],[4],'1-2','probability','A person is picked at random. Find all five probabilities: is in blood group A+; is in AB; is in A or B; has rhesus negative blood; is not in O.',blood)
A('2-c','Q2(c)(i),Q2(c)(ii),Q2(c)(iii)','5C',[33,49],[4,5],'1-2','probability','Over a period, 8000 people donate blood. How many would you expect to donate (i) type AB blood, (ii) rhesus negative blood, and (iii) rhesus positive blood?',blood)
menu='Sarah selects a starter, a main course and a dessert. Starters: Melon, Soup, Goats cheese salad, Smoked salmon. Main courses: Roast beef, Fish of the day, Vegetation curry (as printed). Desserts: Fruit salad, Chocolate brownie, Apple crumble, Pear flan, Ice cream.'
for i,meal in enumerate(MEALS):
 selected=MEAL_POOL[i]
 A(f'3-a-meal-{i+1:02}','Q3(a)','15C',[34,50],[6],'1-2','probability','Write one three-course lunch that Sarah could select. Practise the menu route: '+selected+'.',menu,variant('q3-a-menu',MEAL_POOL,selected,6,'Write one three-course lunch that Sarah could select.','For this practice, write a lunch using '+selected+'. The original question allows any starter, main course and dessert from the menu.'))
A('3-b','Q3(b)','5C',[34,50],[6],'1-2','probability','How many possible different selections can Sarah make?',menu)
A('3-c','Q3(c)','5D',[34,50],[6],'1-2','probability','Assuming each selection is equally likely, find all three probabilities: smoked salmon as starter; smoked salmon followed by roast beef; smoked salmon followed by roast beef followed by fruit salad or ice cream.',menu)
stemleaf='The stem-and-leaf plot records patient ages over two hours. Rows: 0 | 6,8,8,9; 1 | 0,4,5,6,8; 2 | 4,4,7; 3 | 1,2,6,6,6,9; 4 | 3,6; 5 | 0,0,5,8; 6 | 2,2,7,9; 7 | 1,4,5,5,6,8; 8 | 2,3,7. Key: 4 | 3 = 43.'
for s,scale,prompt in [('a','5B','How many patients visited the accident department during the two-hour period?'),('b','5B','What was the age of the oldest patient?'),('c','5B','What was the modal age?'),('d','5B','Find the median age.'),('e','5C','List the ages of all patients aged between 30 and 60.')]:A('4-'+s,'Q4('+s+')',scale,[35,51],[7],'1-6','data-statistics',prompt,stemleaf)
triangle='The original coordinate grid shows triangle ABC, with A = (5, 4). B is at (−3, 6) and C is at (1, −2) on the supplied diagram.'
A('5-a','Q5(a)','10C',[36,52],[8],'2-2','co-ordinate-geometry-of-the-line','Write down the coordinates of B and C.','The original coordinate grid shows triangle ABC, with A = (5, 4). Read B and C from the diagram.')
A('5-b-i','Q5(b)(i)','5C',[36,52],[8],'2-2','co-ordinate-geometry-of-the-line','On the diagram mark M, the midpoint of [AB].',triangle)
A('5-b-ii','Q5(b)(ii)','5C',[36,52],[8],'2-2','co-ordinate-geometry-of-the-line','Use a formula to find the coordinates of M, the midpoint of [AB].',triangle)
A('5-c','Q5(c)','5C',[36,52],[8],'2-2','co-ordinate-geometry-of-the-line','Use a formula to find the length of [BC], the longest side of the triangle.',triangle)
lines='Line l₁ passes through P(1, 6) and Q(4, 2). Line l₂ has equation 3x − 4y − 4 = 0.'
for s,scale,prompt in [('a','15D','Plot P and Q on the supplied grid and show line l₁.'),('b','5C','Find the slope of line l₁.'),('c','5C','State whether l₁ and l₂ are perpendicular. Give a reason.')]:A('6-'+s,'Q6('+s+')',scale,[37,53],[9],'2-2','co-ordinate-geometry-of-the-line',prompt,lines)
enlarge='The original diagram shows C and right-angled triangle XYZ. X′Y′Z′ is its image under an enlargement centred at C with scale factor 2·5.'
A('7-a','Q7(a)','10D',[38,54],[10],'2-4','geometry','Construct X′Y′Z′ on the supplied diagram.',enlarge)
A('7-b-i','Q7(b)(i)','5C',[39,54],[10,11],'2-4','geometry','Given |XY| = 2 cm, find |X′Y′|.',enlarge)
A('7-b-ii','Q7(b)(ii)','5C',[39,54],[10,11],'2-4','geometry','Given |Z′Y′| = 8 cm, find |ZY|. Show your calculations.',enlarge)
A('7-b-iii','Q7(b)(iii)','5C',[39,54],[10,11],'3-4','area-volume','Find the area of triangle XYZ.',enlarge+' |XY| = 2 cm and |Z′Y′| = 8 cm; the right angle is at Y.')
construct='Construct triangle PQR with |PQ| = 7 cm, |QR| = 5 cm and ∠PQR = 80°. P is marked on the supplied line.'
A('8a-a','Q8A(a)','10D',[40,55],[12],'2-1','geometry',construct)
A('8a-b','Q8A(b)','10D',[40,55],[12],'2-1','geometry','On your diagram from part (a), construct the image of triangle PQR under central symmetry in P.',construct)
A('8a-c','Q8A(c)','5B',[40,55],[12],'2-1','geometry','Use your protractor to measure ∠RPQ.',construct)
para='ABCD is a parallelogram. Its diagonals intersect at O. |AB| = 9 cm, |BC| = 6 cm and ∠DAB = 60°. The original diagram is supplied.'
A('8b-a','Q8B(a)','5B',[41,56],[13],'2-1','geometry','Find |DC|.',para)
A('8b-b','Q8B(b)','5C',[41,56],[13],'2-1','geometry','Find ∠ABC.',para)
for route,selected,start in [('ab-dc','AB and DC','AB'),('ad-bc','AD and BC','AD')]:
 A('8b-c-'+route,'Q8B(c)','5B',[41,56],[13],'2-1','geometry','Name one pair of parallel lines in the diagram. For this practice use the pair containing '+start+'.',para,variant('q8b-c-parallel-pair',['AB and DC','AD and BC'],selected,13,'Name one pair of parallel lines','For this practice, name the parallel pair containing '+start+'. The original question allows either pair.'))
A('8b-d','Q8B(d)','5C',[41,56],[13],'2-1','geometry','Is the statement |DO| = |OB| and |AO| = |OC| true or false? Give a reason.',para)
A('8b-e','Q8B(e)','5C',[41,56],[13],'2-1','geometry','Construct the image of ABCD under axial symmetry in line AB on the supplied diagram.',para)
shop='Michelle and Jerry visit a shop daily. Monday to Sunday, Michelle spends €16, €12, €20, €5, €24, €8, €27. Jerry spends €10, €18, €25, €19, €26 on Monday to Friday; Saturday and Sunday are blank in the original table.'
for s,scale,pages,sp,prompt in [('a','5B',[14],42,'On which day did Michelle spend the most?'),('b','5C',[14],42,'Find the difference between the most and least amount Michelle spent in a day.'),('c','15C',[14],42,'Draw a bar chart to show the amount Michelle spent each day.'),('d','10D',[14,15],43,'Calculate the mean amount per day spent by Michelle during that week.'),('e','10D',[14,15],43,'Jerry spent €140 during the week and equal amounts on Saturday and Sunday. How much did he spend on Saturday?'),('f','5C',[14,15],43,'Jerry spent €140 during the week. On average he spent €4 per day more than Michelle. Justify this statement.')]:A('9-'+s,'Q9('+s+')',scale,[sp,57],pages,'1-6','data-statistics',prompt,shop)
balloon='Tom stands 40 m from the base of the basket of a hot-air balloon. The angle of elevation to its top is 35°. Its height is h.'
A('10-a-i','Q10(a)(i)','15B',[44,58],[16],'2-3','trigonometry','Find tan 35°.',balloon)
A('10-a-ii','Q10(a)(ii)','10C',[44,58],[16],'2-3','trigonometry','Find h, the height of the balloon.',balloon)
raised='The balloon rises vertically until its top is 70 m above the ground. Tom moves to a position 50 m horizontally from the point vertically under the basket. The diagram labels the distance from Tom to the top as d.'
A('10-b-i','Q10(b)(i)','10C',[44,58],[16],'2-3','trigonometry','Find the new angle of elevation to the top of the balloon.',raised)
A('10-b-ii','Q10(b)(ii)','10C',[45,58],[16,17],'2-1','geometry','Use the Theorem of Pythagoras to find d, the distance from Tom to the top of the balloon.',raised)
A('10-c','Q10(c)','5D',[45,58],[17],'3-4','area-volume','Tom estimates that the volume of air in the balloon equals the volume of a sphere of radius 11 m. Find his estimate.')
marks={str(q):25 for q in range(1,8)}|{'8A':25,'8B':25,'9':50,'10':50}
p.check(marks|{'3':910,'8B':30},107)
assert sum(c['totalMarks'] for c in p.cards if not c.get('selectionVariant'))+15+5==325
p.review(marks,'Independent visual inspection of all 20 original paper pages and scheme PDF pages 29–60. All 47 published marking units retained; 60 mechanically generated menu routes and both parallel-pair routes give 107 cards.',list(range(29,61)),[46,47],
 ['Candidate total is 300: Q1–7 plus either Q8A or Q8B and both Q9–10. All offered tasks total 325 before finite route expansion.',
 'Paper 2 has different scale ladders from Paper 1. The PDF 46 table governs these cards. Exactly seven units are starred: Q7(b)(i–iii), Q8B(a), Q10(a)(ii), Q10(b)(ii), Q10(c).',
 'Q2(b), Q2(c)(i–iii), Q3(c) retain one published scale each; all entries remain required. Q3(a) expands the Cartesian product of the printed 4 starters × 3 mains × 5 desserts, all with the shared 15C tariff.',
 'Q8B(c) explicitly asks for one pair in the supplied parallelogram. Both possible parallel pairs are retained. Q1(a)(ii) asks for open descriptions of events, not a closed supplied pool.',
 'Phase 2 Q4(e) correctly lists 12 ages with one 55. Do not import the duplicate-age correction from the parallel Phase 3 edition.',
 'The original blood percentages and menu spelling Vegetation curry are preserved. Mathematical glyph criteria in Q3(b), Q5(b)(i), Q8B(b), Q10(b)(i) are retained in the complete printed notes and labelled text rows.',
 'Q8A construction, central symmetry and angle measurement retain the complete original template and prior construction context. Q7(b)(iii) carries both given lengths and the enlargement factor.'],
 [{'pages':[2,12,13],'wording':'either Question 8A or Question 8B','classification':'finite-question-alternatives','reason':'Both complete alternatives retained at all their published scales.'},{'pages':[6],'wording':'Write one three-course lunch that Sarah could select.','classification':'finite-cartesian-product','reason':'4 × 3 × 5 = 60 distinct meals generated with itertools.product; each route retains 15C.'},{'pages':[13],'wording':'Name one pair of parallel lines','classification':'finite-choose-one-of-two','reason':'Both opposite-side parallel pairs in the supplied diagram retained.'},{'pages':[3],'wording':'give one example of each','classification':'open-example-all-required','reason':'All three event types required; no closed list of event descriptions supplied.'},{'pages':[4,5,6,7],'wording':'A or B; fruit salad or ice cream; each; List the ages','classification':'all-required-or-event-union','reason':'Probability unions and required entries are mathematical tasks, not optional answer selections.'}],
 lambda t:('finite-question-alternatives','Both Q8 alternatives retained.') if 'either' in t or '8A or 8B' in t else ('finite-cartesian-product','All 60 menu combinations retained.') if 'three-course' in t or 'starter' in t else ('finite-choose-one-of-two','Both parallel pairs retained.') if 'pair of parallel' in t else ('open-example-all-required','All event types required; examples open.') if 'example' in t else ('all-required','All specified questions and data entries retained.') if 'Answer' in t else None)
SCHEME_ROW_FIGURES = {'maths-2013-fl-p2-q1-a-i': 'maths-2013-FL-scheme-p031-i0', 'maths-2013-fl-p2-q1-a-ii': 'maths-2013-FL-scheme-p031-i1', 'maths-2013-fl-p2-q1-b-i': 'maths-2013-FL-scheme-p031-i2', 'maths-2013-fl-p2-q1-b-ii': 'maths-2013-FL-scheme-p031-i3', 'maths-2013-fl-p2-q1-b-iii': 'maths-2013-FL-scheme-p031-i4', 'maths-2013-fl-p2-q2-a-i': 'maths-2013-FL-scheme-p032-i0', 'maths-2013-fl-p2-q2-a-ii': 'maths-2013-FL-scheme-p032-i1', 'maths-2013-fl-p2-q2-b': 'maths-2013-FL-scheme-p032-i2', 'maths-2013-fl-p2-q2-c': 'maths-2013-FL-scheme-p033-i0', 'maths-2013-fl-p2-q3-a-meal-01': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-b': 'maths-2013-FL-scheme-p034-i1', 'maths-2013-fl-p2-q3-c': 'maths-2013-FL-scheme-p034-i2', 'maths-2013-fl-p2-q4-a': 'maths-2013-FL-scheme-p035-i0', 'maths-2013-fl-p2-q4-b': 'maths-2013-FL-scheme-p035-i1', 'maths-2013-fl-p2-q4-c': 'maths-2013-FL-scheme-p035-i2', 'maths-2013-fl-p2-q4-d': 'maths-2013-FL-scheme-p035-i3', 'maths-2013-fl-p2-q4-e': 'maths-2013-FL-scheme-p035-i4', 'maths-2013-fl-p2-q5-a': 'maths-2013-FL-scheme-p036-i0', 'maths-2013-fl-p2-q5-b-i': 'maths-2013-FL-scheme-p036-i1', 'maths-2013-fl-p2-q5-b-ii': 'maths-2013-FL-scheme-p036-i2', 'maths-2013-fl-p2-q5-c': 'maths-2013-FL-scheme-p036-i3', 'maths-2013-fl-p2-q6-a': 'maths-2013-FL-scheme-p037-i0', 'maths-2013-fl-p2-q6-b': 'maths-2013-FL-scheme-p037-i1', 'maths-2013-fl-p2-q6-c': 'maths-2013-FL-scheme-p037-i2', 'maths-2013-fl-p2-q7-a': 'maths-2013-FL-scheme-p038-i0', 'maths-2013-fl-p2-q7-b-i': 'maths-2013-FL-scheme-p039-i0', 'maths-2013-fl-p2-q7-b-ii': 'maths-2013-FL-scheme-p039-i1', 'maths-2013-fl-p2-q7-b-iii': 'maths-2013-FL-scheme-p039-i2', 'maths-2013-fl-p2-q8a-a': 'maths-2013-FL-scheme-p040-i0', 'maths-2013-fl-p2-q8a-b': 'maths-2013-FL-scheme-p040-i1', 'maths-2013-fl-p2-q8a-c': 'maths-2013-FL-scheme-p040-i2', 'maths-2013-fl-p2-q8b-a': 'maths-2013-FL-scheme-p041-i0', 'maths-2013-fl-p2-q8b-b': 'maths-2013-FL-scheme-p041-i1', 'maths-2013-fl-p2-q8b-c-ab-dc': 'maths-2013-FL-scheme-p041-i2', 'maths-2013-fl-p2-q8b-d': 'maths-2013-FL-scheme-p041-i3', 'maths-2013-fl-p2-q8b-e': 'maths-2013-FL-scheme-p041-i4', 'maths-2013-fl-p2-q9-a': 'maths-2013-FL-scheme-p042-i0', 'maths-2013-fl-p2-q9-b': 'maths-2013-FL-scheme-p042-i1', 'maths-2013-fl-p2-q9-c': 'maths-2013-FL-scheme-p042-i2', 'maths-2013-fl-p2-q9-d': 'maths-2013-FL-scheme-p043-i0', 'maths-2013-fl-p2-q9-e': 'maths-2013-FL-scheme-p043-i1', 'maths-2013-fl-p2-q9-f': 'maths-2013-FL-scheme-p043-i2', 'maths-2013-fl-p2-q10-a-i': 'maths-2013-FL-scheme-p044-i0', 'maths-2013-fl-p2-q10-a-ii': 'maths-2013-FL-scheme-p044-i1', 'maths-2013-fl-p2-q10-b-i': 'maths-2013-FL-scheme-p044-i2', 'maths-2013-fl-p2-q10-b-ii': 'maths-2013-FL-scheme-p045-i0', 'maths-2013-fl-p2-q10-c': 'maths-2013-FL-scheme-p045-i1', 'maths-2013-fl-p2-q3-a-meal-02': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-03': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-04': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-05': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-06': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-07': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-08': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-09': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-10': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-11': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-12': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-13': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-14': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-15': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-16': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-17': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-18': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-19': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-20': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-21': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-22': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-23': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-24': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-25': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-26': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-27': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-28': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-29': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-30': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-31': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-32': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-33': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-34': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-35': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-36': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-37': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-38': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-39': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-40': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-41': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-42': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-43': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-44': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-45': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-46': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-47': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-48': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-49': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-50': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-51': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-52': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-53': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-54': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-55': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-56': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-57': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-58': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-59': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q3-a-meal-60': 'maths-2013-FL-scheme-p034-i0', 'maths-2013-fl-p2-q8b-c-ad-bc': 'maths-2013-FL-scheme-p041-i2'}
overrides={c['id']:{'section':'A' if int(re.match(r'Q(\d+)',c['printedParts'][0])[1])<=8 else 'B',**({'figureKey':SCHEME_ROW_FIGURES[c['id']]} if c['id'] in SCHEME_ROW_FIGURES else {})} for c in p.cards}
p.apply(ROWS,'2013 Foundation Project Maths Phase 2 Paper 2',expect_added=[c['id'] for c in p.cards],card_overrides=overrides,question_figures=True)
