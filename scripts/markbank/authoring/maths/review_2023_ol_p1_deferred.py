"""Independent visual review of every task in 2023 deferred Ordinary Paper 1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper
PREFIX='maths-2023-ol-p1-deferred'
p=Paper(year=2023,level='ordinary',paper_key='p1',sitting='deferred',
 paper_file='LC003GLP100EV-deferred.pdf',scheme_file='LC003GLP000EV-deferred.pdf',prefix=PREFIX,ref='2023 OL Paper 1 — Deferred',
 scales={'5B':[0,2,5],'5C':[0,2,3,5],'5D':[0,2,3,4,5],'10B':[0,7,10],'10C':[0,3,7,10],'10D':[0,4,6,8,10],'15C':[0,5,10,15],'15D':[0,4,8,12,15]},
 reviewed_at='2026-10-31',general_notes=[2,4,5],scheme_pages=list(range(1,24)),
 printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
 review_method='Independent visual sweep of all 32 paper pages and scheme pages 1–23. Each printed task reconciled against its detailed mark boundary; all final source crops inspected before publication.',
 source_notes=[
 'All ten questions retained: 44 tasks, 380 offered marks. Q2(c)(i)–(ii) share 15D; Q4(c)(i)–(iii) share 10D; Q8(c)(i)–(iii) share 10D. Each shared allocation remains one card.',
 'Q10(a)(iii) and (iv) are swapped in the summary: the detailed scheme awards (iii) 5C (0,2,3,5) and (iv) 5D (0,2,3,4,5). Preserve those explicit detailed scales and their matching credit notes.',
 'Q2(a) asks for real solutions. A clearly attributed NextStepUni number line shows the complete ray x≥−2 with a closed endpoint, clarifying that the printed dots do not restrict answers to integers.',
 'Q3(a) partial-credit example says substitute −7 for y, but the paper gives x=−7. The model calculation correctly substitutes for x and finds y=−9.',
 'Q3(c) requires both solution pairs: (x,y)=(−1,−3) and (3,1). No optional choice is implied by the two roots.',
 'Q4(b) simplifies to 3x−4 only on the original domain x≠5/2; the paper’s x∈R omits this denominator restriction.',
 'Q4(c) is one three-part graph-reading task. The original annotated graph is retained. Its Mid Partial Credit line “Work of Merit in” is incomplete; retain it without inventing missing official criteria. The explicit complete mid-credit alternative is one correct section.',
 'Q6(b) includes the complete original graph on −2≤x≤4. The six new plotted values exclude the given endpoint f(4)=−20. Q6(c)(ii) keeps both labelled extrema together under 5C.',
 'Q7(d) mixes minutes and seconds in its first printed equation. The consistent equation is 10n+60(n−1)=(32−10−9)×60=780 seconds, giving n=12. There are n−1 jogs between n sprints.',
 'Q8(c) charges a full hourly unit for a part-hour: 4 hours 15 minutes is five billed hours, giving A=€400 and B=€430. The equality n=2 concerns the whole billed-hour count used by the question.',
 'Q9(a) uses height above the ground and a separate schematic flight path. Maximum height is 45 m at 1 second; the ball hits the ground after 4 seconds. The negative time is discarded.',
 'Q9(b)(ii) applies the 15% discount before isolating VAT: 125×0.85=106.25, then 106.25×23/123≈19.87. The source’s “€125−15%” is shorthand, not a subtraction of unlike units.',
 'Q10(b) contains two investment scenarios as problem data, not a student choice. Both required calculations are retained. Year-start deposits in Option 2 grow for three, two and one years respectively.'
 ],out_name='2023-ordinary-p1-deferred.json',atlas_prefix='mathematics-ordinary-',section_of=lambda q:'A' if q<=6 else 'B')
def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None,extra=None):
 p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,dict(extra or {},figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))
complex_stem='Note: In this question, i² = −1. Let z₁ = 3 − 2i and z₂ = −2 + 3i.'
A('1-a-i','Q1(a)(i)','15D',[6],[4],'4-4','complex-numbers','Plot and label z₁, z₂, and the complex conjugate of z₂ on the Argand Diagram below.',['3 parts correct','Apply F* if labels omitted'],stem=complex_stem)
A('1-a-ii','Q1(a)(ii)','5C',[6],[4],'4-4','complex-numbers','Find |z₁ − z₂|. Give your answer in surd form.',['formula for Modulus'],stem=complex_stem)
A('1-b','Q1(b)','5C',[7],[4,5],'4-4','complex-numbers','Write 3(2 − i) + i(5 + 2i) in the form x + yi, where x, y ∈ ℝ.',['expansion of brackets','Multiplication fully correct'],stem='In this question, i² = −1.')
A('1-c','Q1(c)','5C',[7],[4,5],'4-4','complex-numbers','The real numbers p and k are such that 2 − 3pi − 9 − ki = 4k + 1 − i. Find the value of p and the value of k.',['identifies reals or','Correctly finds'],stem='In this question, i² = −1.')
A('2-a','Q2(a)','10C',[8],[6],'4-3','algebra-equations','Solve the inequality (2x − 5)/3 ≥ (x − 4)/2, where x ∈ ℝ, and show the solution set on a number line.',['Carries out some relevant correct','transposing but finishes correctly'])
A('2-b','Q2(b)','5C',[8],[6],'4-1','algebra','Write q in terms of p and t when 3(2p + q) = t.',['multiplying brackets but finishes'])
A('2-c-i-ii','Q2(c)(i),Q2(c)(ii)','15D',[8],[7],'5-1','functions','(i) Find f(6). (ii) Find f(g(2)).',['3 steps in the solution','2 steps correct'],stem='The function f is as follows for x ∈ ℝ: f(x) = 3x² − 8x − 35. The function g is as follows for x ∈ ℝ: g(x) = 2x − 7.')
A('3-a','Q3(a)','15C',[9],[8],'4-2','algebra-equations','Given that 5x − 4y = 1, find the value of y when x = −7.',['Error in transposing but finishes correctly'])
A('3-b','Q3(b)','5C',[9],[8],'3-2','indices','Find the value of x for which 2ˣ = √32, where x ∈ ℚ.',['2 steps correct'])
A('3-c','Q3(c)','10D',[9],[9],'4-2','algebra-equations','Solve the simultaneous equations: x − y = 2; x² + y² = 10.',['Finds correct quadratic equation','Finds values of'])
A('4-a','Q4(a)','15C',[10],[10],'4-2','algebra-equations','Solve the equation x² − 6x + 3 = 0. Give each solution correct to 1 decimal place.',['Identifies a, b, and c','Fully substituted formula'])
A('4-b','Q4(b)','5C',[10],[10],'4-1','algebra,functions','The function h is as follows for x ∈ ℝ: h(x) = (6x² − 23x + 20)/(2x − 5). Express h(x) in the form ax + b, where a, b ∈ ℤ.',['Correct factors of quadratic found'],extra={'markingNote':'The original denominator is zero at x=5/2. The simplified formula 3x−4 is valid for x≠5/2; cancellation does not restore that missing input.'})
A('4-c-i-ii-iii','Q4(c)(i),Q4(c)(ii),Q4(c)(iii)','10D',[11],[11],'5-1','graphing-functions,functions','Use the graph to estimate each of the following: (i) the 3 roots of g(x). Note: In the case of the next two parts, show your work clearly on the graph. (ii) g(3·5). (iii) The values of x for which g(x) = −8.',['Any 1 correct section','Correct solutions but no work on graph'],stem='The graph of a cubic function g(x) is shown below.',extra={'markingNote':'All three printed parts share 10D. One mid-credit bullet is incomplete in the source (“Work of Merit in”). Its numeric bands and original wording are retained; no missing official criterion is invented.'})
seq='Term n of an arithmetic sequence is given by Tₙ = 4n + 1, for n ∈ ℕ.'
A('5-a-i','Q5(a)(i)','10C',[12],[12],'4-1','sequences-series','Write down the first three terms of the sequence.',['Any one term correct','Any two terms correct'],stem=seq)
A('5-a-ii','Q5(a)(ii)','5C',[12],[12],'4-1','sequences-series,algebra-equations','Term k of the sequence is 101. Find the value of k.',['Writes Tn formula'],stem=seq)
sum_stem='The following identity is true for all n ∈ ℕ: 1 + 2 + 3 + 4 + … + n = n(n + 1)/2.'
A('5-b-i','Q5(b)(i)','5B',[12],[13],'4-1','sequences-series','Use the expression n(n + 1)/2 to find the sum of the natural numbers from 1 to 12 inclusive.',['substitutes 12'],stem=sum_stem)
A('5-b-ii','Q5(b)(ii)','10C',[12],[13],'4-2','algebra-equations,sequences-series','The sequence of numbers 1, 2, 3, 4, …, n add to 325. Solve the equation n(n + 1)/2 = 325, to find the value of n.',['Finds correct quadratic','fails to eliminate answer'],stem=sum_stem)
f='Let f(x) = x³ − 3x² − 9x, where x ∈ ℝ.'
A('6-a','Q6(a)','10C',[13],[14],'5-1','functions','Complete the table below to show the value of f(x) for each of the given values of x. x: −2, −1, 0, 1, 2, 3, 4. f(x): blank, blank, blank, blank, blank, blank, −20.',['Any one correct value','4 correct'],stem=f)
A('6-b','Q6(b)','5C',[13],[14],'5-1','graphing-functions','Draw the graph of f(x) in the domain −2 ≤ x ≤ 4 where x ∈ ℝ, on the grid below.',['4/5 points plotted correctly','failure to join or joined'],stem=f)
A('6-c-i','Q6(c)(i)','10C',[14],[14,15],'5-2','differentiation','Find f′(x), the derivative of f(x).',['Any two parts differentiated correctly'],stem=f)
A('6-c-ii','Q6(c)(ii)','5C',[14],[14,15],'5-2','differentiation,graphing-functions','Use your derivative to find the co-ordinates of the local maximum point and the local minimum point of f(x).',['Finds x values','fails to identify Max and'],stem=f)
run='A 5 km run takes place every Saturday morning over the same course, starting at 9:30 a.m.'
A('7-a','Q7(a)','15C',[15],[16],'3-3','number-systems','The average time taken to finish the run is 34 minutes 30 seconds. Find the average time it takes to complete 1 km of the run. Give your answer in minutes and seconds.',['Finds total number of seconds'],stem=run)
aoife='One Saturday morning Aoife ran as follows: First km: 5 minutes 10 seconds. Second km: 5 minutes 45 seconds. Third km: 6 minutes 25 seconds. Fourth and fifth km: constant speed. She finished the race at 10:05 a.m.'
A('7-b-i','Q7(b)(i)','10C',[15],[16],'3-3','number-systems','How long did it take her to run the last km?',['Finds how long final two kilometres take'],stem=run+' '+aoife)
A('7-b-ii','Q7(b)(ii)','5B',[15],[16,17],'3-3','number-systems','Find Aoife’s average speed over the 5 km run. Give your answer, in km/hr, correct to 1 decimal place.',['5km in 35 minutes','Ans: 8·6 km/hr'],stem=run+' '+aoife)
A('7-c','Q7(c)','10D',[15],[16,17],'3-3','number-systems','One Saturday Brian arrived late and started his run 3 minutes later than everyone else (at 9:33 a.m.). His average speed, while he was running, was 15 km/hr. Shane, who started on time (9:30 a.m.), ran at an average speed of 12·5 km/hr. Which of the two finished the run first and by how many minutes?',['Finds finish time of Brian or Shane','Brian finishes first by 1 minute'],stem=run)
A('7-d','Q7(d)','10C',[16],[18],'4-2','algebra-equations,number-systems','It takes Shane exactly 32 minutes to complete this session. Work out the value of n, the number of 10-second sprints he does during this session.',['Fully correct equation set up'],stem='Shane is training for the run. One of his training sessions is as follows, where n ∈ ℕ: Warm up: 10 minutes. Sprints: n sprints for 10 seconds each; jog for 60 seconds between each pair of sprints. Warm down: 9 minutes.')
oil='An oil lorry delivered heating oil to John’s home. Before the delivery the meter reading in the lorry showed that it contained 10 360 litres of oil. After the delivery the meter reading was 9160 litres.'
A('8-a-i','Q8(a)(i)','10C',[17],[19],'3-3','financial-maths','One litre of oil costs €0·6168. Find the cost of the heating oil that was delivered to John’s home.',['number of litres 1200'],stem=oil)
A('8-a-ii','Q8(a)(ii)','10B',[17],[19],'3-3','financial-maths','The cost in part (a)(i) does not include VAT. Find the total cost of the heating oil after VAT at 13·5% is included.',['Total Cost = €840·08'],stem=oil+' One litre of oil costs €0·6168 before VAT.')
A('8-b','Q8(b)','10C',[17],[19],'3-3','financial-maths','Six months later the same amount of oil, including VAT at the same rate, cost €1157·70. What was the price per litre of this oil excluding VAT? Give your answer correct to the nearest cent.',['Finds 0·96475 or 1020'],stem=oil+' The VAT rate is 13·5%.')
repair='John discovered a leak in his oil tank. He contacted two companies and asked for quotes to repair the tank. Each company included a call out charge and a rate per hour, or part of an hour, for the repair work. They emailed the following quotes for the repair work: Company A: €100 call out charge plus €60 per hour (or part thereof). Company B: €80 call out charge plus €70 per hour (or part thereof).'
A('8-c-i-ii-iii','Q8(c)(i),Q8(c)(ii),Q8(c)(iii)','10D',[18],[20],'4-2','algebra-equations,financial-maths','(i) If the repair will take 4 hours 15 minutes to complete, how much would each company charge? (ii) Write a formula to show the total amount that each company charges for n hours of repair work, where n ∈ ℕ. (iii) After how many hours would the cost be the same for both companies?',['Any one section correct','Any 2 sections correct'],stem=repair)
A('8-d','Q8(d)','10C',[18],[21],'3-4','area-volume','John’s oil tank is in the shape of a cylinder. It is 2 m long and can hold 1500 litres of oil. Find the radius of the oil tank. Give your answer correct to the nearest cm. (Note: 1 Litre = 1000 cm³.)',['correct formula for cylinder','correctly and fails to finish'])
golf='A golf ball was placed on top of a vertical cliff above some level ground. Florence, standing on the edge of the cliff hit the ball with a golf club, off the cliff and into the air. While it was travelling through the air, the height of the ball above the ground was given by h(t) = 40 + 10t − 5t², where h is the height in metres and t is the time in seconds after the ball was hit.'
A('9-a-i','Q9(a)(i)','5B',[19],[22],'5-1','functions','Find the height of the cliff, in metres.',['substitutes 0'],stem=golf)
A('9-a-ii','Q9(a)(ii)','10C',[19],[22],'5-1','functions','What was the height of the ball above the ground after 1·5 seconds?',['Substitutes 1·5'],stem=golf)
A('9-a-iii','Q9(a)(iii)','5C',[19],[22,23],'5-2','differentiation','Find the maximum height of the ball above the ground.',['Finds t = 1','Max Height = 45 m'],stem=golf)
A('9-a-iv','Q9(a)(iv)','10C',[19],[22,23],'4-2','algebra-equations,functions','How long was the ball in the air before it hit the ground?',['Ans: After 4 seconds','fails to eliminate'],stem=golf)
A('9-a-v','Q9(a)(v)','5C',[20],[22,23],'2-1','geometry','The ball landed 240 m from the foot of the cliff. Find the distance between the ball and the top edge of the cliff when it landed. Give your answer, in metres, correct to 2 decimal places.',['Pythagoras or sets up equation correctly'],stem=golf)
A('9-b-i','Q9(b)(i)','10C',[20],[24],'3-3','financial-maths','Florence bought a golf club online from a company in Britain. The cost was £138·75 sterling. The exchange rate was €1 = £0·8338. How much did the golf club cost in euro? Give your answer correct to the nearest cent.',['Sets up division correctly'])
A('9-b-ii','Q9(b)(ii)','5B',[20],[25],'3-3','financial-maths','Florence also bought a golf bag at her local golf club during a sale. The original cost was €125, including VAT at 23%. She got a discount of 15% in the sale. Work out how much VAT Florence paid. Give your answer correct to the nearest cent.',['price without VAT','€19·87 VAT'])
tax='Mary got a new job where she was earning €950 per week. When she started the job, Mary had to pay emergency tax as she did not have a tax credit certificate. Emergency tax meant that all of her income was taxed at 40% and she had no tax credits.'
normal_tax='When Mary got her tax credit certificate, she started to pay tax at the correct rate. Now, each week she pays tax at the standard rate of 20% on the first €678·85 of her income and 40% on the remainder. She also had tax credits of €65·38 each week.'
A('10-a-i','Q10(a)(i)','10B',[21],[26],'3-3','financial-maths','How much tax did she pay each week while she was on emergency tax?',['0·4 = 40%'],stem=tax)
A('10-a-ii','Q10(a)(ii)','10C',[21],[26],'3-3','financial-maths','How much does Mary now pay in tax each week?',['Finds 271·15','Finds Gross Tax'],stem=tax+' '+normal_tax)
A('10-a-iii','Q10(a)(iii)','5C',[21],[26,27],'3-3','financial-maths','Mary was on emergency tax for a total of six weeks. At the end of that time she got a refund of the tax that she had overpaid while she was on the emergency tax rate. Find the total amount of the refund she got for these six weeks.',['Finds 2280 and 1073·10'],stem=tax+' '+normal_tax,extra={'markingNote':'The detailed task-specific allocation is 5C (0,2,3,5). The summary mistakenly lists 5D for this part and swaps it with part (iv).'})
A('10-a-iv','Q10(a)(iv)','5D',[21],[26,27],'3-3','financial-maths,algebra-equations','Mary gets a pay increase of €x per week. She continues to pay tax at the standard rate of 20% on the first €678·85 of her income and 40% on the remainder. She still had tax credits of €65·38 each week. She now pays €218·85 in tax each week. Find the value of x.',['Finds new tax @ 40% after pay increase','Finds new taxable income after pay'],stem='Mary was earning €950 per week before the pay increase.',extra={'markingNote':'The detailed task-specific allocation is 5D (0,2,3,4,5), including a 3-mark mid-partial band. The summary mistakenly lists 5C for this part and swaps it with part (iii).'})
invest='Mary has €15 000 in a savings account and would like to invest the money for a maximum of 3 years. An investment broker is offering two investment options, Option 1 and Option 2, as shown in the table below. Option 1: Invest €15 000 at an annual compound rate of r% and receive €16 153·36 at the end of 3 years. Option 2: Invest €5000 at the beginning of each year for 3 years at an annual compound rate of 4·2%.'
A('10-b-i','Q10(b)(i)','10C',[22],[28],'3-3','financial-maths','Find the value of the annual compound interest rate, r, in Option 1.',['Formula fully substituted correctly'],stem=invest)
A('10-b-ii','Q10(b)(ii)','10C',[22],[28],'3-3','financial-maths','Mary chooses Option 2. She will invest €5000 at the beginning of year 1, another €5000 at the beginning of year 2, and another €5000 at the beginning of year 3. Find how much money Mary will receive at the end of the 3 year period. Give your answer correct to the nearest cent.',['Finds 10210'],stem=invest)
assert len(p.cards)==44
selection_review=[
 {'pages':[3,4,16],'wording':'any five / any three questions','classification':'exam-level-selection','reason':'All ten questions retained for practice.'},
 {'pages':[11],'wording':'the 3 roots / next two parts','classification':'required-answers','reason':'All roots and both graph readings are required within one shared 10D allocation, not a choice.'},
 {'pages':[17],'wording':'Which of the two','classification':'comparison','reason':'One required comparison of named runners, including the time difference.'},
 {'pages':[28],'wording':'two investment options / Mary chooses Option 2','classification':'scenario-context','reason':'The options describe required calculations in separate marked tasks; the student is not invited to omit one.'}
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','All ten questions retained.')
 if 'one of his training' in t:return ('scenario-context','The table gives the one required training session, not a choice.')
 if 'chooses option 2' in t or 'investment options' in t:return ('scenario-context','Both investment tasks are required; the choice is made by the person in the scenario.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
