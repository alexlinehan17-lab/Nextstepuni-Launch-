"""Independent visual review of every 2022 deferred Ordinary Paper 1 task."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper
PREFIX='maths-2022-ol-p1-deferred'
p=Paper(year=2022,level='ordinary',paper_key='p1',sitting='deferred',
 paper_file='LC003GLP100EV-deferred.pdf',scheme_file='LC003GLP000EV-deferred.pdf',prefix=PREFIX,ref='2022 OL Paper 1 — Deferred',
 scales={'5B':[0,2,5],'5C':[0,2,3,5],'10C':[0,3,7,10],'10D':[0,3,5,8,10],'15C':[0,5,10,15],'15D':[0,4,8,12,15]},
 reviewed_at='2026-10-31',general_notes=[2,4,5],scheme_pages=list(range(1,25)),
 printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
 review_method='Independent visual sweep of all 32 paper pages and scheme pages 1–24. Every printed task reconciled against its detailed allocation, including shared scales, diagrams, dependencies and alternatives. Final presentation images inspected before publication.',
 source_notes=[
 'All ten questions retained: 45 tasks, 380 offered marks, despite 220 candidate marks. Q4(a)(i–ii), Q8(a)(i–ii), and Q8(b)(i–iii) each remain one shared 15D task.',
 'Q1(a) requires both index expressions under one 10D scale. Q1(c) retains the original denominator restrictions x≠5/7 and x≠−1/3.',
 'Q2(b) compares two representations of one quantity, not a choice of website or answer. The scheme’s first conversion is 3.01×10^8 m/s, not its printed km/s; the alternative km/year route is correct.',
 'Q3(a) keeps both complex numbers together. Q3(b)(ii) is one open construction: any appropriately plotted complex number of modulus √5 is valid, not only the two source examples. Q3(c) retains both alternative solution routes under one 5C award.',
 'Q4(a) includes the full continuous real ray and its closed endpoint. Q4(b)(ii) retains the original graph and y-intercept, so the multiplier 4 can be recovered independently.',
 'Q5(b) asks for all three stationary points with labels, not a choice. Q6(b)(ii) keeps both roots together and retains the preceding composition identity as printed context.',
 'Q7(b) requires all five missing table entries. Q7(c)(i) retains the given Day 2 count. Q7(d) asks for tiles laid ON day 15, so subtract cumulative totals T15−T14. Q7(e)(ii) uses proportional area pricing, not rounding to whole 20 m² blocks.',
 'Q8(a)(i–ii) shares 15D across four missing table values and six plotted points with a curve. Q8(b)(i–iii) shares a separate 15D across three graph readings and their working. Clearly attributed reconstructed graphs show the required work; original SEC credit notes and accepted ranges remain attached.',
 'Q8(c)(i) the source omits the factor 1.5 after 10 in its substituted g(1.5) line. Correct calculation is 18+10(1.5)−5(1.5)²=21.75, and the difference is 5 m. Q8(c)(ii) requires calculus. Q8(c)(iii) solves for equal heights at t=2.125 and gives 16.7 m; the balls do not physically collide.',
 'Q9(a) keeps all ten entries in one table task; Q9(c) keeps all three box counts together. Q9(b) is a yes/no determination with justification, not a choice pool. Q9(d) uses only the rates printed in this historical examination.',
 'Q10(b) uses cycling time, excluding the one-hour break. Q10(c)(i) Brendan’s graph starts at noon, passes Alan at (14:00,48 km), and reaches Q at 14:40. Reconstructed diagrams stop at that endpoint; he does not continue past Q.',
 'Q10(d)(ii) retains both riders’ complete data and the original graph. A reconstructed reading gives about 13:03, within the source’s 13:00–13:20 range (source example about 13:05). Q10(e) uses t in hours from 10:00; Q10(f) converts 30 minutes to 0.5 hours.'
 ],out_name='2022-ordinary-p1-deferred.json',atlas_prefix='mathematics-ordinary-',section_of=lambda q:'A' if q<=6 else 'B')
def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None,extra=None):
 p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,dict(extra or {},figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))
A('1-a','Q1(a)','10D',[7],[4],'3-2','indices','Write 5^(−3) and 4^(3/2) without using indices.',['Relevant work with indices in either part','One correct solution together with relevant work with indices in the other part'])
A('1-b','Q1(b)','10C',[7],[4],'3-2','indices','Given that (√8)⁶/8⁵ = 8^t where t ∈ ℤ, find the value of t.',['Relevant work with indices'])
A('1-c','Q1(c)','10C',[8],[5],'4-1','algebra','Write the following as a single fraction in its simplest form: 2/(7x−5) − 4/(3x+1).',['writes the LCM','Full 2nd Line of the solution'])
car='Gina buys a car for €22 000. It depreciates (decreases in value) by 20% each year.'
A('2-a-i','Q2(a)(i)','10C',[9],[6],'3-3','financial-maths','Work out how much it will be worth exactly 2 years after Gina buys it.',['Correct relevant formula written'],car)
A('2-a-ii','Q2(a)(ii)','10C',[9],[6],'3-3','financial-maths','On 1 January 2025, the value of this car will be €10 000. Work out its value exactly 1 year earlier, on 1 January 2024.',['P(0.8) = 10000'],car)
A('2-b','Q2(b)','10C',[10],[7],'3-3','number-systems','Given that a trillion is a million million, find out whether or not these two answers are consistent with each other.',['Effort at converting km to m','Either expression fully formulated'],'Two students are looking on the internet to find the value of the speed of light. One website gives it as 3×10⁸ metres per second. Another says that light travels approximately 9·5 trillion kilometres in a year.')
argand='Two complex numbers, u and v, are shown on the Argand diagram below.'
A('3-a','Q3(a)','10D',[11],[8],'4-4','complex-numbers','Write u and v in the form a+bi, where a,b ∈ ℝ and i²=−1.',['4 items','2 correct items'],argand)
A('3-b-i','Q3(b)(i)','5C',[11],[8],'4-4','complex-numbers','Verify, by calculation, that |u|=|v|. Show your working out.',['Modulus formula written with or without some substitution','Either modulus found'],argand)
A('3-b-ii','Q3(b)(ii)','10C',[11],[8],'4-4','complex-numbers','Draw a complex number w on the diagram above, so that |w|=|u|=|v|, and write w in the form a+bi, where a,b ∈ ℝ and i²=−1.',['correct complex number OR a correct plot'],argand)
A('3-c','Q3(c)','5C',[12],[8,9],'4-4','complex-numbers','z is a complex number, so that u×z=v. Find z. Give your answer in the form a+bi, where a,b ∈ ℝ and i²=−1.',['Conjugate identified','2 relevant equations found'],argand)
A('4-a-i-ii','Q4(a)(i),Q4(a)(ii)','15D',[13],[10],'4-3','algebra-equations','(i) Solve the following inequality, for x ∈ ℝ: 5−2x≤11. (ii) Show the solution set on the number line below. Remember that x ∈ ℝ.',['Any relevant step towards solving inequality','Treats as equation'])
quad='The graph of the quadratic function d(x) is shown on the co-ordinate diagram below.'
A('4-b-i','Q4(b)(i)','10C',[13],[11],'5-1','graphing-functions,algebra-equations','Use the graph to write down the two solutions of the equation d(x)=0.',['indicates value(s) on the diagram'],quad)
A('4-b-ii','Q4(b)(ii)','5B',[13],[11],'4-2','algebra,graphing-functions','Hence, write d(x) in the form d(x)=ax²+bx−12, where a,b ∈ ℝ.',['an answer from part (i) written'],quad+' Part (i) asks for the two solutions of d(x)=0.')
f='Let f(x)=2x³−3x²+7x, where x ∈ ℝ.'
A('5-a-i','Q5(a)(i)','10C',[14],[12],'5-2','differentiation','Find f′(x), the derivative of f.',['1 term correctly differentiated','2 terms correctly differentiated'],f)
A('5-a-ii','Q5(a)(ii)','5C',[14],[12],'5-2','differentiation','Find the value of f′(x) when x=1.',['Any substitution into candidates'],f)
A('5-a-iii','Q5(a)(iii)','10C',[14],[12],'5-2','differentiation','Find the equation of the tangent to the curve y=f(x) at x=1.',['m=7 AND (1,6)'],f)
A('5-b','Q5(b)','5C',[14],[13],'5-2','differentiation,graphing-functions','On the graph, mark the three points for which g′(x)=0, where g′(x) is the derivative of g. Label these points A, B, and C.',['one correct point plotted','2 correct points plotted'],'The graph of y=g(x) is shown on the co-ordinate diagram below, for a particular range of x ∈ ℝ.')
func='The functions h and p are defined for x ∈ ℝ as follows: h: x↦2x−3; p: x↦x²−1.'
A('6-a','Q6(a)','15C',[15],[14],'5-1','functions','Find p(5).',['Accept correct answer without work'],func)
A('6-b-i','Q6(b)(i)','5C',[15],[14],'5-1','functions','Show that p(h(x))=4x²−12x+8.',['Finds h(p(x))'],func)
A('6-b-ii','Q6(b)(ii)','10C',[15],[14,15],'4-2','algebra-equations,functions','Solve p(h(x))=4. Give each answer correct to 2 decimal places.',['Fully substituted -b formula'],func+' Part (i) gives p(h(x))=4x²−12x+8.')
tiles='Darragh is laying square tiles to make a large patio. He draws a diagram at the end of each day to record his progress. The diagrams below show the tiles that have been laid up to the end of each of the first 3 days. Darragh expects to follow the pattern shown below for several weeks in order to complete the work.'
A('7-a','Q7(a)','10C',[16],[16],'4-1','sequences-series','Using the pattern above, draw a diagram to show the tiles that have been laid up to the end of Day 4.',['One line or column missing'],tiles)
A('7-b','Q7(b)','10D',[16],[16,17],'4-1','sequences-series','Complete the table below to show the total number of square tiles that have been laid up to the end of each of the first 7 days. The first two have already been done for you. Day 1: 8; Day 2: 14; Days 3–7: blank.',['3 correct entries','4 correct entries'],tiles)
tn='Darragh works out that Tₙ, the total number of tiles laid up to the end of day n, is given by the following formula, as long as Darragh is still laying tiles on day n ∈ ℕ: Tₙ=(n+2)²−n.'
A('7-c-i','Q7(c)(i)','5B',[16],[17],'4-1','sequences-series','Show that this formula gives the correct value for the total number of tiles that have been laid up to the end of Day 2.',['substitutes 2 for n'],tn+' The table gives 14 tiles at the end of Day 2.')
A('7-c-ii','Q7(c)(ii)','5B',[16],[17],'4-1','algebra,sequences-series','Write the formula for Tₙ above in the form Tₙ=an²+bn+c, where a,b,c ∈ ℤ.',['brings down the Tn formula from the question'],tn)
A('7-d','Q7(d)','10D',[17],[17,18],'4-1','sequences-series','Work out how many tiles Darragh laid on the 15th day.',['Finds BOTH T14 AND T15'],tn)
patio='When the patio is completed, it will be made up of 554 square tiles. Each square tile measures 60 cm by 60 cm.'
A('7-e-i','Q7(e)(i)','5B',[17],[19],'3-4','area-volume','Work out the total area of the patio, in m², once it is completed.',['0.6 or area formula'],patio)
A('7-e-ii','Q7(e)(ii)','5B',[17],[19],'3-3','financial-maths,area-volume','Darragh charges €700 for each 20 m² of patio, plus VAT at 23%. Work out how much Darragh charges, in total, for the patio. Give your answer correct to the nearest euro.',['answer from (e)(i) written'],patio)
balls='Gina is on the roof of a building and Harry is at the bottom of the building. Harry throws a ball upwards when t=0. Its height above the ground is h(t), with time t in seconds and height in metres; its graph is shown. When t=1, Gina throws her ball downwards. The balls do not collide. Gina’s ball has height g(t)=18+10t−5t², for t≥1.'
A('8-a-i-ii','Q8(a)(i),Q8(a)(ii)','15D',[18],[20,21],'5-1','graphing-functions,functions','(i) Complete the table below to show the values of g(t) for the given values of t. t: 1, 1·5, 2, 2·5, 3, 3·1; g(t): blank, 21·75, blank, blank, blank, 0·95. (ii) Draw the graph of y=g(t) on the co-ordinate diagram on the next page, using the same axes and scales. Note: t≥1 for g(t).',['4 values in the table, and 6 points plotted','8 correct elements'],balls)
A('8-b-i-ii-iii','Q8(b)(i),Q8(b)(ii),Q8(b)(iii)','15D',[19],[20,21],'5-1','graphing-functions','Use the graphs of h(t) and g(t) to estimate each answer. In each case, show your work on the diagram. (i) How much higher than Harry’s ball is Gina’s ball, half a second after Gina drops her ball (at t=1·5)? (ii) How long does it take Harry’s ball to reach its maximum height? (iii) At what height does Gina’s ball pass Harry’s ball?',['2 parts correct','incomplete graph work'],balls+' Plot g(t) on the supplied axes as required in part (a).')
ballfunc=balls+' The height of Harry’s ball is given by h(t)=1+18t−5t². These are the same questions as in part (b), but here you will need to use algebra to answer them.'
A('8-c-i','Q8(c)(i)','10D',[19],[20,22],'5-1','functions','How much higher than Harry’s ball is Gina’s ball, half a second after Gina drops her ball (t=1·5)? Show your working out.',['Finds BOTH h(1.5) AND g(1.5)'],ballfunc)
A('8-c-ii','Q8(c)(ii)','5B',[19],[20,22],'5-2','differentiation','Use calculus to find how long it takes Harry’s ball to reach its maximum height.',['Some correct differentiation','Equates h’(t) = 0'],ballfunc)
A('8-c-iii','Q8(c)(iii)','5B',[20],[20,22,23],'4-2','algebra-equations,functions','By solving an equation, find the height at which Gina’s ball passes Harry’s ball. Give your answer correct to 1 decimal place.',['either expression for h(t) or g(t) written'],ballfunc)
coins='Mary is saving money. She starts saving with 136 coins, worth a total of €51. Each week, Mary’s mother gives her €3 to add to her savings, as follows: she gives Mary one €1 coin, two 50-cent coins, and five 20-cent coins.'
A('9-a','Q9(a)','15D',[21],[24],'4-1','sequences-series','Use this information to complete the table below, showing the total number of coins and the total amount of money that Mary has saved as the weeks pass. Each answer in the last row should be an expression in terms of n. Rows: Start (136 coins, €51), after 1 week, 2 weeks, 3 weeks, 4 weeks, and n weeks (n ∈ ℕ).',['5 correct entries','8 correct entries'],coins)
A('9-b','Q9(b)','5B',[21],[24,25],'4-2','algebra-equations,sequences-series','Will there ever be a time at which the total number of coins that Mary has is equal to the total amount of money (in euro) that she has saved? If so, find when that happens; if not, explain why not.',['not equal initially and coins increasing by 8'],coins)
A('9-c','Q9(c)','10C',[21],[25],'3-3','number-systems','Work out the number of coins in each money box at this time.',['One correct value','2 correct values'],'Mary keeps her money in three different money boxes. Box 1 has only €1 coins, Box 2 has only 50-cent coins, and Box 3 has only 20-cent coins. Each box contains the same amount of money. Mary starts with 136 coins in total in her three money boxes, worth a total of €51.')
usc='Mary’s mother pays USC at each of the three rates shown in the following table: first €12 012 at 0·5%; €12 012 to €20 484 at 2%; above €20 484 at 4·5%.'
A('9-d-i','Q9(d)(i)','10D',[22],[26],'3-3','financial-maths','Work out the USC that Mary’s mother pays at the 0·5% rate and the 2% rate.',['Finds 60.06 OR 8472','Finds 60.06 AND 8472'],usc)
A('9-d-ii','Q9(d)(ii)','10D',[22],[26,27],'3-3','financial-maths','Mary’s mother pays a total of €822·72 in USC. Work out her gross income.',['Finds 593.22','Finds 13182.67'],usc)
journey='Two friends, Alan and Brendan, separately cycled a 64 km journey from P to Q. A third friend, Colin, cycled from Q to P on the same day. The diagram shows Alan’s journey. Time is measured in hours, starting at 10:00; distance is measured in kilometres from P along the route. Alan left P at 10:00, cycled at a constant speed, stopped for an hour, then continued at the same speed to Q. He arrived at 15:00.'
brendan='Brendan left P at 12:00. He cycled at a constant speed, without stopping, until he reached Q. He passed Alan at 14:00.'
colin='Colin cycled in the opposite direction, from Q to P along the same road. Colin left Q at 10:00 and cycled at a constant speed, without stopping, until he reached P. He arrived at P at 15:00.'
A('10-a','Q10(a)','5B',[23],[28],'5-1','graphing-functions','At what time of the day did Alan stop for a break?',['Indication on the graph'],journey)
A('10-b','Q10(b)','10C',[23],[28],'3-3','number-systems,graphing-functions','Work out Alan’s constant speed when he was cycling.',['Formula fully substituted'],journey)
A('10-c-i','Q10(c)(i)','10C',[23],[28,29],'5-1','graphing-functions','Draw the graph of Brendan’s journey on the diagram on the previous page, using the same axes and scales. Label the graph clearly.',['Any use of 12:00 or any straight line drawn','Indicates point of intersection'],journey+' '+brendan)
A('10-c-ii','Q10(c)(ii)','5B',[23],[28,29],'3-3','number-systems,graphing-functions','Work out Brendan’s constant speed when he was cycling.',['Work of merit, for example, formula written'],journey+' '+brendan)
A('10-d-i','Q10(d)(i)','5B',[23],[28,29],'5-1','graphing-functions','Draw the graph of Colin’s journey on the diagram on the previous page, using the same axes and scales. Label the graph clearly.',['One correct point plotted'],journey+' '+colin)
A('10-d-ii','Q10(d)(ii)','5B',[23],[28,29],'5-1','graphing-functions','Use your graphs to estimate the time of the day at which Colin and Brendan passed each other.',['Some indication on the graph','13:00 – 13:20'],journey+' '+brendan+' '+colin+' Plot both riders’ journeys on the supplied axes as in parts (c)(i) and (d)(i).')
A('10-e','Q10(e)','5B',[23],[30],'5-1','functions','Write a formula to represent Colin’s distance from P at any given time during his journey. Your formula should be written in terms of t, where t ∈ ℝ is the time in hours from 10:00. Remember that Colin left Q at 10:00 and arrived at P, 64 km away, at 15:00.',['Correct formula written','12.8'])
A('10-f','Q10(f)','5C',[24],[30],'5-2','differentiation','Alan’s speed during the race is given by d′(t), the derivative of d(t). Use this to find Alan’s speed 30 minutes after the start of the race.',['one correct term differentiated','Fully correct differentiation'],'On a different day, Alan cycles in a race. This time, his speed changes throughout the race. The distance, in km, he has travelled from the starting line during the race is given by d(t)=6t³−12t²+40t, where t is the time in hours from the start of the race, and t ∈ ℝ, 0≤t≤1.')
assert len(p.cards)==45
selection_review=[
 {'pages':[3,4,16],'wording':'any four / any two questions','classification':'exam-level-selection','reason':'Retain all ten questions and 380 offered marks.'},
 {'pages':[7],'wording':'whether or not these two answers are consistent','classification':'comparison','reason':'One required dimensional comparison, not a student choice.'},
 {'pages':[8],'wording':'Draw a complex number w','classification':'open-answer','reason':'Any appropriate point with the required modulus; the source examples do not create a finite pool.'},
 {'pages':[13],'wording':'the three points','classification':'required-answers','reason':'All three stationary points and their labels required together.'},
 {'pages':[20,22],'wording':'each of the following / same questions as in part (b)','classification':'required-answers','reason':'Both graphical and algebraic approaches are required in distinct published allocations.'},
 {'pages':[25],'wording':'If so / if not','classification':'conditional-response','reason':'One yes/no determination with the corresponding justification.'},
 {'pages':[26],'wording':'each of the three rates','classification':'scenario-context','reason':'USC bands are cumulative problem data, not alternatives.'}
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','All ten questions retained.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
