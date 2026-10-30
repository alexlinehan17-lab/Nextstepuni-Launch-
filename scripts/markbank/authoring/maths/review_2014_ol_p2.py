"""2014 Ordinary Project Maths Paper 2: all tasks, including both Q6 alternatives."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *

R={
'1-a-i':[L(LPC,'Relevant work in one or both sections.'),L(HPC,'One correct section.'),L(FC,'Accept correct answers without work.')],
'1-b-i':[L(LPC,'Any correct #E or #S.'),L(HPC,'Calculates the probability with replacement.'),L(HPC,'Correct answer without work.')],
'1-b-ii':[L(LPC,'Any relevant work towards creating at least one correct probability.'),L(HPC,'Correct answer without work.')],
'1-c':[L(LPC,'Any relevant work towards creating at least one correct probability.'),L(HPC,'Correct answer without work.')],
'2-a':[L(PC,'Writes the correct #E or #S.'),L(PC,'Any incomplete work with 1.'),L(FC,'Accept correct answers without work.')],
'2-b':[L(LPC,'Identifies the probability of scoring here.'),L(HPC,'Fails to finish.'),L(FC,'Accept correct answers without work.')],
'2-c':[L(FC,'Accept correct answers without work.')],
'2-d':[L(LPC,'Correctly identifies P(S) and/or P(M).'),L(HPC,'A fully correct substitution.'),L(FC,'Accept correct answers without work.')],
'3-a-i':[L(LPC,'Relevant work in one section.'),L(HPC,'One section correct.')],
'3-b-i':[L(LPC,'Any correct or consistent substitution.'),L(HPC,'Formula substituted correctly'),L(HPC,'Calculates slope with one incorrect substitution.')],
'3-b-ii':[L(LPC,'Correct or consistent slope identified in this part and stops.'),L(HPC,'A fully correct or consistent substitution.'),L(HPC,'Calculates equation of line with one incorrect substitution.')],
'3-c':[L(LPC,'Writes slope of k equal to slope of t.'),L(LPC,'Work with a translation which indicates an understanding of the concept.'),L(HPC,'An incorrect translation correctly applied.'),L(HPC,'A correct graphical solution.')],
'4-a-i':[L(PC,'Any correct substitution into formula.'),L(PC,'Calculates a distance with one incorrect substitution.'),L(FC,'Accept correct answer without work.')],
'4-a-ii':[L(LPC,'Writes a correct formula for the area of the triangle'),L(HPC,'A fully correct substitution.'),L(HPC,'Calculates area with one incorrect substitution.')],
'4-b-i':[L(LPC,'Relevant work in one section.'),L(LPC,'Work of merit in at least one section.'),L(HPC,'One section correct.')],
'5-a':[L(NOTE,'A correct answer without work shown award full credit.')],
'5-b-i':[L(LPC,'Writes the correct formula for the sector area or area of circle.'),L(HPC,'Formula substituted correctly.'),L(HPC,'Calculates area of sector with one incorrect substitution.')],
'5-b-ii':[L(PC,'Calculates a relevant area.'),L(PC,'Concept of shaded area by difference indicated but not fully developed.'),L(NOTE,'Accept an answer consistent with previous work.')],
'5-c':[L(FC,'Correct answer.'),L(NOTE,'Accept an answer consistent with previous work.')],
'6a-a-i':[L(PC,'Any work of merit e.g. One arc drawn from a vertex.'),L(FC,'An incircle constructed with at least one side of the triangle a tangent to the circle')],
'6a-a-ii':[L(SOL,'3·6 cm')],
'6a-b':[L(PC,'Any relevant work in the use of Pythagoras or recognition of angle standing on diameter')],
'6b':[L(LPC,'Any work of merit such as joining B to X.')],
'7-a-i':[L(LPC,'Any work of merit towards estimating the number of properties registered or suggesting a partially plausible reason.'),L(HPC,'One section correct.')],
'7-b':[L('Angle Determination, '+LPC,'One sector angle correct'),L('Angle Determination, '+HPC,'One consistent error in the calculation of sector angle.'),L('Pie Chart, '+PC,'Any one sector indicated.')],
'7-c-i':[L('Number of Properties, '+LPC,'One correct entry.'),L('Number of Properties, '+HPC,'One consistent error in the calculation.'),L('Total Tax due, '+LPC,'One correct entry.'),L('Total Tax due, '+HPC,'One consistent error in the calculation.')],
'7-c-ii':[L(PC,'Some addition of the correct values indicated.'),L(FC,'Accept a correct or consistent answer without work.')],
'7-c-iii':[L(PC,'Writes 241,000,000 or Answer c(ii).'),L(FC,'Accept a correct or consistent answer without work.')],
'7-c-iv':[L(PC,'Work of merit with any of the values [1 550 970, 159 030, 51 649 990].')],
'7-c-v':[L(PC,'Any work of merit in finding the number of properties changing band'),L(PC,'Identifies the difference in the band valuation.'),L(PC,'Fully correct substitution.')],
'8-a-i':[L(PC,'Any work of merit. e.g. Joins tips of blades or draws circle on diagram.'),L(FC,'Accept a correct answer without work.')],
'8-a-ii':[L(LPC,'Writes the correct formula.'),L(LPC,'Identifies the radius correctly.'),L(HPC,'A fully correct substitution.'),L(HPC,'Calculates the area of circle with one incorrect substitution.')],
'8-a-iii':[L(LPC,'Writes a correct formula for area of a triangle.'),L(LPC,'Any work of merit such as a triangle drawn in this section with the tips of blades joined.'),L(HPC,'Calculates the area of the triangle with one incorrect substitution.')],
'8-a-iv':[L(PC,'Any work of merit in the determination of working life or number of rotations.'),L(FC,'A correct answer.')],
'8-b':[L(LPC,'Any correct relevant work such as a trigonometric ratio or the Sine Rule identified.'),L(HPC,'Calculates the height with one incorrect substitution.')],
'8-c-i':[L(LPC,'Any work of merit involving Pythagoras Theorem, Tan ratio or identification of a right angled triangle.'),L(HPC,'Correct substitution into formula')],
'8-c-ii':[L(LPC,'Any work of merit. e.g. Calculates the size of the error or writes % error formula.'),L(HPC,'Calculates the % error with one incorrect substitution.')],
'9-a-i':[L(LPC,'A correct relevant formula written e.g. Pythagoras, Cosine Rule,'),L(HPC,'A fully correct substitution.')],
'9-a-ii':[L(LPC,'Indicates correct relevant information on the diagram.'),L(LPC,'Correct trigonometric ratio set up or similar work of merit.'),L(HPC,'A fully correct substitution.')],
'9-b-i':[L(LPC,'Indicates correct or consistent relevant information on the diagram.'),L(LPC,'Any work of merit. e.g. Total angle measure in a straight line = 180° .'),L(HPC,'A fully correct or consistent substitution.')],
'9-b-ii':[L(LPC,'Indicates correct or consistent relevant information on the diagram.'),L(LPC,'Identification or use of relevant trigonometric formula. e.g. Cosine Rule.'),L(HPC,'A fully correct or consistent substitution.'),L(NOTE,'Accept an answer consistent with previous work.')],
}
ROWS={'maths-2014-ol-p2-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
p=Paper(2014,'ol','p2',{'5A':[0,5],'5B':[0,3,5],'5C':[0,3,4,5],'10B':[0,5,10],'10C':[0,4,7,10],'15B':[0,7,15],'20B':[0,10,20],'25E':[0,5,10,15,20,25]},'LC003GLP230EV.pdf','LC003GLP000EV.pdf',reviewed_at='2026-10-29')
A=p.A
cars='A garage has 5 black cars, 9 red cars and 10 silver cars for sale.'
two='A car is selected at random. Then a second car is selected at random from those remaining.'
A('1-a-i','Q1(a)(i),Q1(a)(ii)','10C',[35,54],[3],'1-2','probability','A car is selected at random. What is the probability that: (i) The car is black? (ii) The car is black or red?',stem=cars)
A('1-b-i','Q1(b)(i)','5C',[35,54],[3],'1-2','probability','What is the probability that the first car is silver and the second car is black?',stem=cars+' '+two)
A('1-b-ii','Q1(b)(ii)','5C',[35,54],[3],'1-2','probability','What is the probability that one of the selected cars is red and the other is black?',stem=cars+' '+two)
A('1-c','Q1(c)','5C',[35,54],[3],'1-2','probability','Three of the black cars, two of the red cars and four of the silver cars have diesel engines. One car from the garage is again selected at random. What is the probability that it is a red car or a diesel car?',stem=cars)
pen='When taking a penalty kick, the probability that Kevin scores is always 3/4.'
A('2-a','Q2(a)','10B',[36,55],[4],'1-2','probability','Kevin takes a penalty. What is the probability that he does not score?',stem=pen)
A('2-b','Q2(b)','5C',[36,55],[4],'1-2','probability','Kevin takes two penalties. What is the probability that he scores both?',stem=pen)
A('2-c','Q2(c)','5A',[36,55],[4],'1-2','probability','Kevin takes three penalties. What is the probability that he scores exactly twice?',stem=pen)
A('2-d','Q2(d)','5C',[36,55],[4],'1-2','probability','Kevin takes five penalties. What is the probability that he scores for the first time on his fifth penalty?',stem=pen)
circle='The circle c has equation (x + 2)² + (y − 3)² = 100.'
geo='co-ordinate-geometry-the-circle'
A('3-a-i','Q3(a)(i),Q3(a)(ii)','5C',[37,56],[5],'2-3',geo,'(i) Write down the co-ordinates of A, the centre of c. Write down r, the length of the radius of c. (ii) Show that the point P(−8, 11) is on the circle c.',stem=circle)
circle+=' A is the centre of c and P(−8, 11) is on c.'
A('3-b-i','Q3(b)(i)','10C',[37,56],[5],'2-3',geo,'Find the slope of the radius [AP].',stem=circle)
A('3-b-ii','Q3(b)(ii)','5C',[37,56],[5],'2-3',geo,'Hence, find the equation of t, the tangent to c at P.',stem=circle+' Part (b)(i): Find the slope of the radius [AP].')
A('3-c','Q3(c)','5C',[37,56],[5],'2-3',geo,'A second line k is a tangent to c at the point Q and k ∥ t. Find the co-ordinates of Q.',stem=circle+' The line t is the tangent to c at P.')
tri='The points A(−9, 3), B(−4, 3) and C(−4, 10) are the vertices of the triangle ABC, as shown.'
line='co-ordinate-geometry-of-the-line'
A('4-a-i','Q4(a)(i)','10B',[38,57],[6],'2-2',line,'Find the length of [AB].',stem=tri)
A('4-a-ii','Q4(a)(ii)','10C',[38,39,57],[6,7],'2-2',line,'Find the area of the triangle ABC.',stem=tri)
A('4-b-i','Q4(b)(i),Q4(b)(ii)','5C',[38,39,57],[6,7],'2-1','geometry,'+line,'X(2, −4) and Y(2, 1) are two points. (i) Draw, on the diagram above, a triangle, XYZ, which is congruent to the triangle ABC. (ii) Write down the co-ordinates of Z and explain why the triangle XYZ is congruent to the triangle ABC.',stem=tri)
sq='The square ABCD has an area of 81 cm².'
A('5-a','Q5(a)','5B',[40,58],[8],'3-4','area-volume','Find |AD|.',stem=sq)
sector='A sector of a circle, centre B and radius |BC|, is drawn inside ABCD as shown by the shaded region.'
A('5-b-i','Q5(b)(i)','10C',[40,58],[8],'3-4','area-volume','Find the area of the sector, correct to one decimal place.',stem=sq+' '+sector)
A('5-b-ii','Q5(b)(ii)','5B',[40,58],[8],'3-4','area-volume','A second sector of a circle, centre D and radius |DA|, is drawn. Find the area of the shaded region (the overlap of the two sectors), correct to one decimal place.',stem=sq+' '+sector)
A('5-c','Q5(c)','5A',[40,58],[8],'3-4','area-volume,trigonometry','The point P is on the arc of the sector DAC, as shown. The triangle APC is isosceles. Find the area of the triangle APC, correct to one decimal place.',stem=sq+' A sector of a circle, centre D and radius |DA|, is drawn inside ABCD.')
construct='Construct the incircle of the triangle ABC below. Show all your construction lines clearly.'
A('6a-a-i','Q6A(a)(i)','15B',[41,59],[9],'2-1','geometry-proofs-and-constructions',construct,extra={'measurementRequired':True})
A('6a-a-ii','Q6A(a)(ii)','5B',[41,59],[9],'2-1','geometry-proofs-and-constructions','Measure the length of the radius of the circle constructed in part (i).',stem='Part (a)(i): '+construct,extra={'measurementRequired':True})
A('6a-b','Q6A(b)','5B',[42,59],[10],'2-1','geometry,trigonometry','Find the value of x.',stem='The point P is on the circle c with centre O and diameter [MN], as shown. The length of the radius of c is 2√5 cm. |MP| = x cm and |PN| = 2x cm.')
A('6b','Q6B','25E',[43,59],[11],'2-1','geometry-proofs-and-constructions','Prove that X is on the line AC.',stem='Two circles, c₁ and c₂, intersect at the points B and X, as shown. The circle c₁ has diameter [AB]. The circle c₂ has diameter [BC]. The line CB is a tangent to c₁.')
news='A newspaper report in October 2013 stated that 90% of homeowners who were liable for property tax had registered for it. The total number of properties liable for the tax was estimated at 1·9 million.'
A('7-a-i','Q7(a)(i),Q7(a)(ii)','10C',[44,60],[12],'3-1','number-systems','(i) Estimate the number of properties that were registered. (ii) Suggest one reason why some properties were not registered.',stem=news)
vals='Homeowners, who registered, were required to value their property in one of a number of given Valuation Bands. Percentage of registered homeowners: €0–€100 000, 24·9%; €100 001–€150 000, 28·6%; €150 001–€200 000, 21·9%; €200 001–€250 000, 10·4%; €250 001–€300 000, 4·9%; over €300 000, 9·3%.'
p.C('7-b','Q7(b)',[{'id':'angles','label':'Angle Determination','code':'5C'},{'id':'pie-chart','label':'Pie Chart','code':'20B'}],[44,60],[12],'1-6','statistics', 'Represent the data in the table using the pie chart below. Label each sector you create and show the angle in each sector clearly.',stem=news+' '+vals)
tax='Tax per property by valuation band: €0–€100 000: €45; €100 001–€150 000: €112; €150 001–€200 000: €157; €200 001–€250 000: €202; €250 001–€300 000: €247; over €300 000: NA. The table gives 425 790 properties and €19 160 550 total tax for the first band, and 489 060 properties for the second. NA = Not Available.'
p.C('7-c-i','Q7(c)(i)',[{'id':'properties','label':'Number of Properties','code':'5C'},{'id':'tax','label':'Total Tax due','code':'10C'}],[45,60],[12,13],'3-3','financial-maths','Use the data in the table above and your answer to part (a)(i) above to complete the following table: Number of properties and Total tax due (€).',stem=news+' '+vals+' '+tax)
A('7-c-ii','Q7(c)(ii)','5B',[45,46,61],[12,13,14],'3-3','financial-maths','Find the total tax due on those properties, registered by October 2013, with a valuation up to €300 000.',stem=news+' '+vals+' '+tax)
alltax='The total tax due on all the properties that were registered was estimated at €241 million.'
A('7-c-iii','Q7(c)(iii)','5B',[45,46,61],[12,13,14],'3-3','financial-maths',alltax+' Find the total tax due on those properties with a valuation over €300 000.',stem=news+' '+vals+' '+tax)
A('7-c-iv','Q7(c)(iv)','5B',[45,46,61],[12,13,14],'3-3','financial-maths','Find the mean estimated tax per property on those properties with a valuation over €300 000.',stem=news+' '+vals+' '+tax+' '+alltax)
A('7-c-v','Q7(c)(v)','5B',[45,46,61],[12,13,14],'3-3','financial-maths','Some homeowners may under-value their property in order to pay less tax. For example, one estimate stated that 20% of properties in the €100 001–€150 000 band should have been valued in the €150 001–€200 000 band. Based on this estimate, find the amount of extra tax that would be raised if these properties were registered in the correct Valuation Band.',stem=news+' '+vals+' '+tax)
wind='A wind turbine, used to generate electricity, has three equally spaced blades 65 metres long.'
A('8-a-i','Q8(a)(i)','10B',[47,62],[15],'2-1','geometry','Write down the size of the angle between two blades.',stem=wind)
A('8-a-ii','Q8(a)(ii)','10C',[47,62],[15],'3-4','area-volume','Find the area of the disc traced out by one full rotation of the blades, correct to the nearest whole number.',stem=wind)
A('8-a-iii','Q8(a)(iii)','5C',[47,62],[15],'3-4','area-volume,trigonometry','Find the area of the triangle formed by joining the tips of the three blades, correct to the nearest whole number.',stem=wind)
A('8-a-iv','Q8(a)(iv)','10B',[48,62],[15,16],'3-1','number-systems','The expected lifetime of the turbine is 25 years. On average, the turbine operates 31% of the time. The blades rotate 15 times per minute when the turbine is operating. Find the number of times the blades will rotate during the expected lifetime of the turbine (ignore leap years). Write your answer in the form a × 10ⁿ, where 1 ≤ a < 10 and n ∈ ℤ.',stem=wind)
gr='Gráinne stood at a point B, which is on level ground 100 metres from the base of the tower supporting the blades, as shown. From there, she measured the angle of elevation to the top of the tower as 60°.'
A('8-b','Q8(b)','5C',[48,63],[16],'2-4','trigonometry','Find the height of the tower, using Gráinne’s measurements. Give your answer correct to the nearest metre.',stem=gr)
actual='Gráinne recognises that her measurement of the angle may not be totally accurate. She read elsewhere that the actual height of the tower is 154 m.'
A('8-c-i','Q8(c)(i)','5C',[48,49,63],[16,17],'2-4','trigonometry','If Gráinne measured the 100 m accurately, find the actual size of the angle at B, correct to the nearest degree.',stem=gr+' '+actual)
A('8-c-ii','Q8(c)(ii)','5C',[48,49,63],[16,17],'3-1','number-systems,trigonometry','Find the percentage error in Gráinne’s measurement of the angle of elevation, correct to one decimal place.',stem=gr+' '+actual+' Part (c)(i): Find the actual size of the angle at B, correct to the nearest degree.')
zipline='At an activity centre a zip-line, [BD], runs between two vertical poles, [AB] and [CD], on level ground, as shown. The point E is on the ground, directly below the zip-line. |AE| = 12 m, |BE| = 14 m, |CD| = 1·95 m, and |EC| = 10 m.'
A('9-a-i','Q9(a)(i)','10C',[50,64],[18],'2-4','trigonometry','Find the distance |ED|, correct to one decimal place.',stem=zipline)
A('9-a-ii','Q9(a)(ii)','5C',[50,64],[18],'2-4','trigonometry','Find |∠AEB|, correct to the nearest degree.',stem=zipline)
A('9-b-i','Q9(b)(i)','10C',[51,64],[18,19],'2-4','trigonometry','Find |∠DEB|, given that |∠CED| = 11°, correct to the nearest degree.',stem=zipline)
A('9-b-ii','Q9(b)(ii)','5C',[51,65],[18,19],'2-4','trigonometry','Hence, or otherwise, find the distance |DB|. Give your answer correct to one decimal place.',stem=zipline+' Part (b)(i): Find |∠DEB|, given that |∠CED| = 11°, correct to the nearest degree.')
marks={'1':25,'2':25,'3':25,'4':25,'5':25,'6A':25,'6B':25,'7':70,'8':50,'9':30}
p.check(marks,41)
p.review(marks,'Independent visual review of all 20 original paper pages and scheme PDF pages 33–68, including models 35–51, scale and allocation tables 52–53 and detailed notes 54–65. Both Q6 alternatives retained; every printed task reconciled to the detailed marking boundaries.',list(range(33,69)),[52,53],
 ['325 offered marks, 300 candidate marks. Both Q6A and Q6B retained.',
  'Q1(a)(i)+(ii), Q3(a)(i)+(ii), Q4(b)(i)+(ii) and Q7(a)(i)+(ii) each use one shared scale. Q7(b) has separate 5C angle/20B chart components; Q7(c)(i) has 5C property-count/10C tax components.',
  'Paper 2 scales differ from Paper 1: 5B 0,3,5; 5C 0,3,4,5; 10C 0,4,7,10; 15B 0,7,15; 25E 0,5,10,15,20,25. Do not reuse Paper 1 ladders.',
  'Q6A construction and radius measurement retain original page access. Q6B is one unlettered 25E proof.',
  'Q7(b) model solution prints 37·44° approximately 90° in the sector-D working, but the chart correctly labels 37°. Preserve source and disclose typo after reveal.',
  'Q7(a) model answer 1·71 is in millions; disclose units. Q8(c)(ii) follows the rounded angle requested in (c)(i).',
  'All earlier required prompts, tables and diagrams accompany dependent tasks; no earlier answers are supplied in the questions. All 41 cards are new.'],
 [{'pages':[2,9,11],'wording':'either Question 6A or Question 6B; OR','classification':'numbered-alternatives','reason':'Both alternatives retained, with 25 marks each.'},{'pages':[2,3,12],'wording':'Answer all nine / all six / all three questions','classification':'all-questions-with-alternative','reason':'All tasks retained including both Q6 alternatives.'}],
 lambda t:('numbered-alternatives','Both Q6A and Q6B retained, 25 marks each.') if '6A' in t or '6B' in t or t.strip()=='OR' else ('all-questions-with-alternative','All printed tasks retained, including both Q6 alternatives.') if 'Answer all' in t else ('random-selection-context','Probability event, not a choice of examination tasks.') if 'selected cars' in t else ('data-category','Valuation-band classification, not a choice of examination tasks.') if 'Valuation Bands' in t else ('alternative-methods','One required distance; any valid method accepted.') if 'or otherwise' in t else None)
SCHEME_ROW_FIGURES = {'maths-2014-ol-p2-q1-a-i': 'maths-2014-OL-scheme-p035-i0', 'maths-2014-ol-p2-q1-b-i': 'maths-2014-OL-scheme-p035-i1', 'maths-2014-ol-p2-q1-b-ii': 'maths-2014-OL-scheme-p035-i2', 'maths-2014-ol-p2-q1-c': 'maths-2014-OL-scheme-p035-i3', 'maths-2014-ol-p2-q2-a': 'maths-2014-OL-scheme-p036-i0', 'maths-2014-ol-p2-q2-b': 'maths-2014-OL-scheme-p036-i1', 'maths-2014-ol-p2-q2-c': 'maths-2014-OL-scheme-p036-i2', 'maths-2014-ol-p2-q2-d': 'maths-2014-OL-scheme-p036-i3', 'maths-2014-ol-p2-q3-a-i': 'maths-2014-OL-scheme-p037-i0', 'maths-2014-ol-p2-q3-b-i': 'maths-2014-OL-scheme-p037-i1', 'maths-2014-ol-p2-q3-b-ii': 'maths-2014-OL-scheme-p037-i2', 'maths-2014-ol-p2-q3-c': 'maths-2014-OL-scheme-p037-i3', 'maths-2014-ol-p2-q4-a-i': 'maths-2014-OL-scheme-p038-i0', 'maths-2014-ol-p2-q4-a-ii': 'maths-2014-OL-scheme-p039-i0', 'maths-2014-ol-p2-q4-b-i': 'maths-2014-OL-scheme-p039-i1', 'maths-2014-ol-p2-q5-a': 'maths-2014-OL-scheme-p040-i0', 'maths-2014-ol-p2-q5-b-i': 'maths-2014-OL-scheme-p040-i1', 'maths-2014-ol-p2-q5-b-ii': 'maths-2014-OL-scheme-p040-i2', 'maths-2014-ol-p2-q5-c': 'maths-2014-OL-scheme-p040-i3', 'maths-2014-ol-p2-q6a-a-i': 'maths-2014-OL-scheme-p041-i0', 'maths-2014-ol-p2-q6a-a-ii': 'maths-2014-OL-scheme-p041-i1', 'maths-2014-ol-p2-q6a-b': 'maths-2014-OL-scheme-p042-i0', 'maths-2014-ol-p2-q6b': 'maths-2014-OL-scheme-p043-i0', 'maths-2014-ol-p2-q7-a-i': 'maths-2014-OL-scheme-p044-i0', 'maths-2014-ol-p2-q7-b': 'maths-2014-OL-scheme-p044-i1', 'maths-2014-ol-p2-q7-c-i': 'maths-2014-OL-scheme-p045-i0', 'maths-2014-ol-p2-q7-c-ii': 'maths-2014-OL-scheme-p046-i0', 'maths-2014-ol-p2-q7-c-iii': 'maths-2014-OL-scheme-p046-i1', 'maths-2014-ol-p2-q7-c-iv': 'maths-2014-OL-scheme-p046-i2', 'maths-2014-ol-p2-q7-c-v': 'maths-2014-OL-scheme-p046-i3', 'maths-2014-ol-p2-q8-a-i': 'maths-2014-OL-scheme-p047-i0', 'maths-2014-ol-p2-q8-a-ii': 'maths-2014-OL-scheme-p047-i1', 'maths-2014-ol-p2-q8-a-iii': 'maths-2014-OL-scheme-p047-i2', 'maths-2014-ol-p2-q8-a-iv': 'maths-2014-OL-scheme-p048-i0', 'maths-2014-ol-p2-q8-b': 'maths-2014-OL-scheme-p048-i1', 'maths-2014-ol-p2-q8-c-i': 'maths-2014-OL-scheme-p049-i0', 'maths-2014-ol-p2-q8-c-ii': 'maths-2014-OL-scheme-p049-i1', 'maths-2014-ol-p2-q9-a-i': 'maths-2014-OL-scheme-p050-i0', 'maths-2014-ol-p2-q9-a-ii': 'maths-2014-OL-scheme-p050-i1', 'maths-2014-ol-p2-q9-b-i': 'maths-2014-OL-scheme-p051-i0', 'maths-2014-ol-p2-q9-b-ii': 'maths-2014-OL-scheme-p051-i1'}
p.apply(ROWS,'2014 Ordinary Level Paper 2',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
