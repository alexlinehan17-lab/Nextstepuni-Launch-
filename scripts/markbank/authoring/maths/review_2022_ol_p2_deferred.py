"""Independent visual review of every 2022 deferred Ordinary Paper 2 task."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper
PREFIX='maths-2022-ol-p2-deferred'
p=Paper(year=2022,level='ordinary',paper_key='p2',sitting='deferred',
 paper_file='LC003GLP200EV-deferred.pdf',scheme_file='LC003GLP000EV-deferred.pdf',prefix=PREFIX,ref='2022 OL Paper 2 — Deferred',
 scales={'5A':[0,5],'5B':[0,3,5],'5C':[0,2,3,5],'10B':[0,5,10],'10C':[0,3,7,10],'10D':[0,3,5,8,10],'15D':[0,4,8,12,15]},
 reviewed_at='2026-10-31',general_notes=[2,26,27],scheme_pages=[1,2]+list(range(25,56)),
 printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
 review_method='Independent visual sweep of all 32 paper pages and scheme pages 1–2 and 25–55. Every task matched to its detailed allocation, including shared parts, dependencies, diagrams and answer selections. Final images inspected before publication.',
 source_notes=[
 'All ten questions retained: 53 separately marked tasks and 380 offered marks, despite 220 candidate marks. Q5(b)(i–ii) shares 10D; Q7(a)(iii–iv) shares 15D.',
 'Paper 2 uses 5B (0,3,5), unlike Paper 1 (0,2,5). Detailed Q4(a) and Q5(a) use 10B (0,5,10), even though the general table omits that scale. Q6(b)(iii) is 5A, hit or miss.',
 'Q1(a) keeps both points together. Q1(d) retains the original diagram and references to the area and hypotenuse tasks, so the perpendicular distance is independently recoverable.',
 'Q2(a): the source intermediate line h²=25 is a typo; h²=25−9=16 gives h=4 cm and area 36 cm². Q2(b) specifically requires the trapezoidal rule, with ordinates 0,2,4,6,6,6,6,6 at 1 cm intervals.',
 'Q3(b)(ii) retains the original tangencies; the common centre is (−2,2) and the new squared radius is 8. Both source alternative methods remain available.',
 'Q4(c) retains both accepted quartile conventions: IQR 11 or 12 cm. Q4(e) counts 13 of 20 heights between 142.2 and 156.8 cm, giving 65%.',
 'Q5 draws are repeated independent games. The two identical long straws remain two equally likely physical outcomes. Q5(d) is a fixed winnings calculation, not a choice of order; €7−€2−€2+€3=€6.',
 'Q6(a) keeps the exact original triangle and construction area. The reconstructed worked example uses that triangle, two side midpoints and two medians; the original scheme is also retained. Q6(b)(ii) requires both alpha and beta under one 10D award.',
 'Q7(a)(iii–iv) is one shared table-completion task, with all nine ordered outcomes and probabilities retained. The tree is context, not an additional separately marked task. Q7(a)(v) includes both AB and BA.',
 'Q7(b)(i) requires all 15 missing products in the 4×4 table, not a selection. Q7(b)(ii) is one fairness decision with justification. Q7(b)(iii) fixes the order 4,3,16, so do not multiply by permutations.',
 'Q8(a)(iii) retains the survey data and confidence-interval instruction. Failing to reject 34% does not prove it true; the source phrase has not changed is too strong.',
 'Q8(b)(i) adds all four shaded points (6,161),(6,163),(6.5,167),(6.5,164). Q8(b)(iii) is one answer-selection card containing all five coefficients; 1 is the closest listed value, not the actual coefficient.',
 'Q8(b)(v) retains the full data and plot. A reconstructed reasonable by-eye line and reading demonstrates a shoe size around 9–9.5; the original marking guidance remains attached. Q8(b)(vi): median stays 172 cm; mean rises from 170.5 to 3588/21≈170.857 cm.',
 'Q9(b) divides the absolute height error by the actual 34 m, not the measured height. Q9(c)(i) uses actual height 34 m and model height 1.7 m. Q9(c)(iii) includes the 3 cm overlap, so b=28π+3≈91 cm.',
 'Q9(d) source rounds slant height to 26.1 before multiplying, giving 1147.9 cm². Keeping full precision gives 14π√680=1146.917989… cm², or 1146.9 cm². Both the source route and the precise route are explained; official credit notes stay intact.',
 'Q10(e)(i) requires construction lines as well as (0,6). Q10(e)(ii) retains the original diagram and line/construction instructions without revealing their answers. Q10(f) retains both trig routes to 50.9 degrees.'
 ],out_name='2022-ordinary-p2-deferred.json',atlas_prefix='mathematics-ordinary-',section_of=lambda q:'A' if q<=6 else 'B')
def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None,extra=None):
 p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,dict(extra or {},figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))
coord='In the co-ordinate diagram below, the point P has co-ordinates (12,5). A is the point on the x-axis vertically below P. B is the point on the y-axis horizontally across from P.'
A('1-a','Q1(a)','10C',[29],[4],'2-2','co-ordinate-geometry-of-the-line','Write down the co-ordinates of A and of B.',['One correct set of coordinates'],coord)
A('1-b','Q1(b)','5C',[29],[4],'2-2','co-ordinate-geometry-of-the-line,area-volume','Find the area of the triangle APB.',['Fully correct substitution into a correct relevant formula'],coord)
A('1-c','Q1(c)','10C',[30],[4],'2-2','co-ordinate-geometry-of-the-line','Find the length |AB|.',['Relevant formula correctly substituted'],coord)
A('1-d','Q1(d)','5C',[30],[4,5],'2-2','co-ordinate-geometry-of-the-line,area-volume','Using your answers to part (b) and part (c), find the length of the shortest line segment from P to the line AB. Give your answer correct to 2 decimal places.',['Equation correctly substituted'],coord+' Part (b) asks for the area of APB and part (c) for |AB|.')
A('2-a','Q2(a)','15D',[31],[6],'3-4','area-volume,trigonometry','Find the value of h, and hence find area of the parallelogram.',['Pythagoras’s formula fully substituted','Correct answer, no units'],'The diagram below shows a parallelogram ABCD. It has sides of length 9 cm and 5 cm, and a perpendicular height of h (taking the base to be 9 cm), where h ∈ ℝ. The point E lies on the side [AB], so that ∠AED is a right angle. |AE|=3 cm, as shown.')
A('2-b','Q2(b)','15D',[31],[7],'3-4','area-volume','Use the Trapezoidal Rule to find the area of this quadrilateral. Show all of your working out.',['Identifies h = 1','Fully correct substitution into the Trapezoidal Rule Formula'],'The diagram below shows a different quadrilateral (not to scale). Two of the sides are parallel. The other two sides are not parallel. The vertical lines on the diagram are a distance of 1 cm apart.')
circle='A circle has equation x²+y²=10, where x,y ∈ ℝ.'
A('3-a-i','Q3(a)(i)','10C',[32],[8],'2-2','co-ordinate-geometry-the-circle','Verify that the point (3,−1) is on the circle.',['Incorrect or no conclusion given'],circle)
A('3-a-ii','Q3(a)(ii)','5C',[32],[8],'2-2','co-ordinate-geometry-the-circle','Find the slope of the tangent to the circle at the point (3,−1).',['Calculates slope of radius'],circle)
tangent='A circle c touches the x-axis at (−2,0) and touches the y-axis at (0,2), as shown.'
A('3-b-i','Q3(b)(i)','10C',[33],[9],'2-2','co-ordinate-geometry-the-circle','Find the equation of the circle c.',['Formula substituted with both centre and radius'],tangent)
A('3-b-ii','Q3(b)(ii)','5C',[33],[9],'2-2','co-ordinate-geometry-the-circle','Find the equation of the circle which has the same centre as the circle c, and which passes through the point (0,0).',['Circle formula substituted with both centre and radius'],tangent)
heights='Below is a stem-and-leaf plot of the heights of a group of students, in centimetres. Split stems: 13|5 7; 14|0 1 3; 14|6 7 7 9; 15|0 1 2 3 3; 15|5 6 6 8; 16|0 1. Key: 13|5 means 135 cm.'
A('4-a','Q4(a)','10B',[34],[10],'1-7','statistics','How many students are in the group?',['Attempt at counting entries'],heights)
A('4-b','Q4(b)','5B',[34],[10],'1-7','statistics','Find the range of the heights of this group of students.',['Maximum or Minimum values identified'],heights)
A('4-c','Q4(c)','5C',[34],[10],'1-7','statistics','Find the interquartile range of the heights of this group of students.',['Identifies Q1 and Q3'],heights)
A('4-d','Q4(d)','5C',[35],[10,11],'1-7','statistics','Use the mean height to work out the sum of the heights of all the students in the group. Show your working out.',['Formula fully substituted'],heights+' The mean height of the students in the group is 149.5 cm.')
A('4-e','Q4(e)','5C',[35],[10,11],'1-7','statistics','The standard deviation of the heights of the students is 7.3 cm, correct to 1 decimal place. Find the percentage of the students whose height is within 1 standard deviation of the mean height of the group.',['Both boundaries indicated'],heights+' The mean height is 149.5 cm.')
straws='A game is played using three straws: two identical long straws (L and L) and one short straw (S). In the game, a player picks one of the three straws at random. The player wins the game if they pick the short straw.'
A('5-a','Q5(a)','10B',[36],[12],'1-2','probability','Noel plays one game. Write down the probability that he wins the game.',['Correct numerator or denominator'],straws)
A('5-b-i-ii','Q5(b)(i),Q5(b)(ii)','10D',[36],[12],'1-2','probability','Noel plays the game three times. In this set of three games: (i) what is the probability that Noel does not draw the short straw (that is, he loses all three games)? (ii) what is the probability that Noel wins the first two games and loses the third game?',['Part (i) or (ii) correct','Incorrect order in (ii)'],straws)
A('5-c','Q5(c)','5C',[37],[12,13],'1-2','probability','Noel decides to continue playing the game until he wins for the first time. What is the probability that Noel wins for the first time on the fifth game he plays?',['Correct answer without supporting work.'],straws)
A('5-d','Q5(d)','5C',[37],[13],'3-3','number-systems','Noel starts with €7. How much money will he have if he plays 3 games and wins exactly 1 of them?',['3 possible outcomes with same result'],'Noel bets €2 on each game. If he loses the game, he loses the €2. If he wins the game, he gets his €2 back, and also another €3.')
A('6-a','Q6(a)','10D',[38],[14],'2-1','geometry-proofs-and-constructions','Construct the centroid of the triangle below. Show clearly any construction lines. (Note: all instruments are permitted. If you are using measurements, show your measurements and calculations.)',['One midpoint constructed correctly','No construction lines award Mid Partial Credit at most'])
angles='In the diagram below, O is the centre of the circle s. The points W, X, and Y lie on s, and α,β ∈ ℝ.'
A('6-b-i','Q6(b)(i)','5B',[38],[15],'2-1','geometry','Give a reason why |∠XYW|=90°.',['Mentions [WX] is a diameter or equivalent'],angles)
A('6-b-ii','Q6(b)(ii)','10D',[38],[15],'2-1','geometry','Find the value of α and the value of β.',['Writes a correct relationship for either','α or β calculated'],angles)
A('6-b-iii','Q6(b)(iii)','5A',[38],[15],'2-1','geometry','Which point in the diagram is the circumcentre of the triangle WXY?',['Point O','Hit or Miss'],angles,extra={'fullCreditMinusOne':False})
prizes='A teacher sets two tasks for a class. Task 1 is to solve a maths problem; Task 2 is to complete a physics experiment. Each task ends when one student completes it, and its winner gets a prize. Winning Task 1 and winning Task 2 are independent events. Probabilities: Task 1, Ann 0.5 and Billy 0.2; Task 2, Ann 0.1 and Billy 0.25. The table includes a blank column for neither Ann nor Billy.'
A('7-a-i','Q7(a)(i)','5B',[39],[16],'1-2','probability','Write down the probability that Billy will not win the prize for Task 1.',['Mentions total probability = 1'],prizes)
A('7-a-ii','Q7(a)(ii)','5C',[39],[16],'1-2','probability','Complete the table above by writing in the probability neither Ann nor Billy will win the prize for each task.',['One correct answer written'],prizes)
tree='The tree diagram shows possible winners of the two tasks. Each outcome is written as the winner of Task 1, followed by the winner of Task 2. A stands for Ann, B for Billy, and N for neither. For example, (A,N) means Ann wins Task 1 and neither Ann nor Billy wins Task 2.'
A('7-a-iii-iv','Q7(a)(iii),Q7(a)(iv)','15D',[40],[16,17],'1-2','probability','(iii) Complete the list of outcomes in the table above. (iv) Write the probability of each outcome in the space beside it in the table above.',['6 correct values','11 correct values'],prizes+' '+tree)
A('7-a-v','Q7(a)(v)','5C',[41],[16,17],'1-2','probability','Work out the probability that Ann wins one prize and that Billy wins the other prize.',['Both relevant probabilities identified'],prizes)
product='Eric and Chidalu play a game involving multiplying numbers. Each picks a number at random from {1,2,3,4}. The two numbers are multiplied and the product is recorded as the result. Eric wins if the result is less than 8; Chidalu wins if the result is greater than or equal to 8.'
A('7-b-i','Q7(b)(i)','10D',[41],[18],'1-2','probability','Fill in the two-way table below to show the result (the product) for each possible pair of numbers. One is already done for you.',['4 correct values','12 correct values'],product)
A('7-b-ii','Q7(b)(ii)','5C',[41],[18],'1-2','probability','Use the two-way table to decide whether or not this game is fair (that is, if Eric and Chidalu are equally likely to win). Justify your answer.',['Answer: Game is not fair','Both relevant probabilities identified'],product)
A('7-b-iii','Q7(b)(iii)','5C',[42],[18],'1-2','probability','Eric and Chidalu play the game a number of times. Find the probability that the first three results of the game are 4, 3, and 16, in that order. Give your answer correct to 4 decimal places.',['Incorrect rounding','Incorrect order'],product)
survey='A polling company carried out a survey on 625 people, selected at random from those who bought tickets for a music festival.'
A('8-a-i','Q8(a)(i)','5C',[43],[19],'1-7','statistics','Work out the margin of error (1/√n) for this sample. Give your answer as a percentage.',['Identifies n=625'],survey)
A('8-a-ii','Q8(a)(ii)','5C',[43],[19],'1-7','statistics','In the survey, 230 people said that they would buy a souvenir t-shirt at the festival. Using the margin of error from part (a)(i), create a 95% confidence interval for the percentage of people who will buy a t-shirt at the festival.',['One boundary formed','Answers in decimal or fraction form'],survey+' Part (a)(i) asks for the margin of error 1/√n.')
A('8-a-iii','Q8(a)(iii)','5C',[44],[19],'1-7','statistics','A music journalist claims that 34% of people who will attend the festival will buy a t-shirt. Use your answer to part (a)(ii) to conduct a hypothesis test, at the 5% level of significance, to test the journalist’s claim. Give your conclusion, and a reason for this conclusion.',['Fail to reject the claim.','unless some interval in part (ii) is given'],survey+' In the survey, 230 people said they would buy a t-shirt. Construct the 95% confidence interval using margin of error 1/√n as in part (a)(ii).')
shoe='A student asks 20 boys on a hurling panel to state their shoe size and their height (to the nearest centimetre). The table records heights under each shoe size: 6:161,163,165; 6.5:167,164,169; 7:168,169; 7.5:172,173,170; 8:174,172,173; 8.5:176,173,174,175; 9:175,177. A partially completed scatter plot is shown.'
A('8-b-i','Q8(b)(i)','10C',[44],[20],'1-7','statistics','The four shaded heights in the table above have not been included on the scatter plot. Draw four points on the scatter plot to show these.',['One point plotted correctly','More than one point plotted correctly'],shoe)
A('8-b-ii','Q8(b)(ii)','5B',[44],[20],'1-7','statistics','Describe the relationship between shoe size and height, based on the scatter plot.',['There is a strong positive correlation'],shoe)
A('8-b-iii','Q8(b)(iii)','5B',[45],[20],'1-7','statistics','Which of the following values is closest to the correlation coefficient between shoe size and height, based on the data in the table and the graph? Tick one box only: −1, −0.5, 0, 0.5, 1.',['Correct box ticked','All other Answers'],shoe,extra={'fullCreditMinusOne':False})
A('8-b-iv','Q8(b)(iv)','5C',[45],[20,21],'1-7','statistics','Calculate the mean height of the 20 boys.',['Correct Addition (Ans = 3410)'],shoe)
A('8-b-v','Q8(b)(v)','5C',[45],[20,21],'1-7','statistics','A new player joins the hurling panel. He has height of 178 cm. Use the information in the scatter plot to estimate this boy’s shoe size. Show your work on the diagram.',['Draws a best fit line on the scatter plot.'],shoe)
A('8-b-vi','Q8(b)(vi)','5C',[46],[20,21],'1-7','statistics','Which will have a bigger increase, the mean or the median, if we include the new player in the data? Justify your answer.',['The Median doesn’t change at all (172 cm)'],shoe+' A new player joins the hurling panel with height 178 cm.')
tower='Jane and Alan visit the round tower at Kilmacduagh, Co. Galway. The tower is roughly a cylinder with a conical roof. Its entrance is 8 m above the ground. Standing x m from the base on level ground, they measure an elevation angle of 20° to the bottom of the entrance and 56° to the top of the cylindrical part. The two diagrams show these measurements (not to scale).'
A('9-a','Q9(a)','15D',[47],[22],'2-3','trigonometry','Work out the value of x, and hence work out the value of h, the height of the cylindrical part of the tower. Give each distance in metres, correct to 1 decimal place.',['Establishes correct equation for x or h','Calculates the length of the base (x)'],tower)
A('9-b','Q9(b)','5C',[48],[22,23],'3-3','number-systems,trigonometry','Later, Jane and Alan read on the internet that the actual height of the cylindrical part of the tower is approximately 34 m. Using 34 m as the actual height of the cylindrical part of the tower, find the percentage error in the answer from part (a). Give your answer correct to the nearest percent.',['% error formula substituted correctly'],tower)
model='Alan wants to make a scale model of the round tower. Excluding the roof, the model is a cylinder with diameter 28 centimetres and height 1.7 metres.'
A('9-c-i','Q9(c)(i)','5C',[48],[23],'2-1','geometry,area-volume','Use the fact that this is a scale model to work out the actual diameter of the round tower at Kilmacduagh. Use the approximate actual height given in part (b). Give your answer in metres.',['Finds Scale factor'],model+' The actual height of the cylindrical part of the tower is approximately 34 m.')
A('9-c-ii','Q9(c)(ii)','5C',[49],[24],'3-4','area-volume','Work out the curved surface area of Alan’s model, excluding the roof. Give your answer correct to the nearest cm². Remember that it will be in the shape of a cylinder, with a diameter of 28 centimetres and a height of 1.7 metres.',['Fully correctly-substituted C.S.A. formula'])
A('9-c-iii','Q9(c)(iii)','10C',[49],[23,24],'3-4','area-volume','Find the value of a and the value of b. Give b correct to the nearest cm.',['One correct dimension indicated'],model+' Alan makes this from a rectangular sheet of card of length a cm and width b cm. An extra 3 cm of card along one edge overlaps the other edge when he makes the cylinder, as shown.')
A('9-d','Q9(d)','10C',[50],[25],'3-4','area-volume,trigonometry','Find l, the slant height of the cone, and hence find the curved surface area of the cone. Give each answer correct to 1 decimal place.',['Correct answer, no units','Not rounding as required'],'The roof of Alan’s model will be a cone with diameter 28 cm and vertical height 22 cm.')
tri='The co-ordinate diagram shows triangles ABC and DEF: A(5,3), B(9,3), C(8,7), D(10,0), E(18,0), F(16,8).'
enlarge=tri+' DEF is the image of ABC under an enlargement with scale factor k.'
A('10-a-i','Q10(a)(i)','5C',[51],[26],'2-2','co-ordinate-geometry-of-the-line','Show that the slope of AC is equal to the slope of DF.',['slope formula written down'],tri)
A('10-a-ii','Q10(a)(ii)','5B',[51],[26],'2-2','co-ordinate-geometry-of-the-line','What does this tell you about the lines AC and DF?',['Mentions that the slopes are equal with no inference'],tri+' Part (a)(i) asks you to show that their slopes are equal.')
A('10-b','Q10(b)','5C',[51],[26],'2-1','geometry','Find the value of k, the scale factor of this enlargement.',['Corresponding lengths or areas calculated'],enlarge)
A('10-c','Q10(c)','5C',[51],[26,27],'2-1','geometry,area-volume','The area of the triangle ABC is 8 square units. Hence, or otherwise, find the area of the triangle DEF.',['Relevant formula written'],enlarge)
A('10-d','Q10(d)','10C',[52],[26,27],'2-2','co-ordinate-geometry-of-the-line','Find the equation of the line BE. Give your answer in the form y=mx+c, where m,c ∈ ℝ.',['Answer not in the required format'],tri)
A('10-e-i','Q10(e)(i)','5C',[52],[26,27],'2-1','geometry-proofs-and-constructions','By drawing suitable lines on the diagram, construct the centre of this enlargement, and write down the co-ordinates of this centre.',['One correct construction line drawn'],enlarge)
A('10-e-ii','Q10(e)(ii)','5C',[52],[26,27],'2-2','co-ordinate-geometry-of-the-line,geometry','Using your answers to part (d) and part (e)(i), show, by substitution, that the centre of enlargement lies on the line BE.',['Fully correct substitution into equation of line'],enlarge+' Part (d) asks for the equation of BE; part (e)(i) asks for the centre of enlargement.')
A('10-f','Q10(f)','10C',[53],[28],'2-3','trigonometry','Use trigonometry to find the size of ∠DFE. Give your answer correct to 1 decimal place.',['Formula substituted correctly or consistently'],tri)
assert len(p.cards)==53
selection_review=[
 {'pages':[3,4,16],'wording':'any four / any two questions','classification':'exam-level-selection','reason':'Retain every offered question, for 380 offered marks.'},
 {'pages':[12],'wording':'picks one of the three straws','classification':'scenario-random-selection','reason':'One random draw within a probability problem; both long straws and the short straw remain in the sample space.'},
 {'pages':[14],'wording':'all instruments are permitted','classification':'method-choice','reason':'Permitted construction methods for one centroid task, with working required.'},
 {'pages':[17,18],'wording':'Complete the list / each outcome / each possible pair','classification':'required-answers','reason':'All missing table entries are required, not a chosen subset.'},
 {'pages':[18],'wording':'whether or not this game is fair','classification':'decision-with-justification','reason':'One required conclusion with supporting probability calculation.'},
 {'pages':[20],'wording':'Which of the following / Tick one box only','classification':'answer-selection','reason':'All five correlation choices remain on one card.'},
 {'pages':[21],'wording':'mean or the median','classification':'answer-selection','reason':'One comparison with a required justification, not two alternative tasks.'},
 {'pages':[27],'wording':'Hence, or otherwise','classification':'method-choice','reason':'Alternative routes to the same area, not a choice pool.'}
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','All ten offered questions retained.')
 if 'straw' in t:return ('scenario-random-selection','Random draw in the probability scenario, not a question choice.')
 if 'tick one' in t or 'correlation' in t:return ('answer-selection','All five choices retained on one card.')
 if 'or otherwise' in t:return ('method-choice','Alternative methods for the same required task.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
