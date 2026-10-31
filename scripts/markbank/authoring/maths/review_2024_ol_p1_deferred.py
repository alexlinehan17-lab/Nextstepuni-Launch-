"""Independent visual review of every task in 2024 deferred Ordinary Paper 1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper
PREFIX='maths-2024-ol-p1-deferred'
p=Paper(year=2024,level='ordinary',paper_key='p1',sitting='deferred',
 paper_file='LC003GLP100EV-deferred.pdf',scheme_file='LC003GLP000EV-deferred.pdf',prefix=PREFIX,ref='2024 OL Paper 1 — Deferred',
 scales={'5B':[0,2,5],'5C':[0,2,3,5],'10C':[0,4,6,10],'10D':[0,3,5,7,10],'15D':[0,5,7,9,15]},
 reviewed_at='2026-10-31',general_notes=[2,4,5],scheme_pages=list(range(1,21)),
 printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
 review_method='Independent visual sweep of all 32 paper pages and scheme pages 1–20. Every task reconciled against its published mark boundary; all question and solution crops inspected before publication.',
 source_notes=[
 'All ten questions retained: 42 tasks and 380 offered marks. Exam-level choice does not remove practice questions. Shared published allocations remain together.',
 'Q1(a)(ii): the printed compound-interest expression has an extra exponent. Correct working is 1545 × 1.03 or 1500 × (1.03)^2 = 1591.35.',
 'Q2(a)(i)–(ii): the scheme says four items but lists three: two plotted points and the conjugate. Preserve its actual numeric credit bands and listed criteria.',
 'Q4(a)(ii): the mid-partial note prints (x=3)^2 instead of (x+3)^2.',
 'Q5(a)(ii): the exact intermediate cost uses 1385.424 kWh; the printed multiplier 1385.42 has been rounded prematurely. The final €186.48 is correct.',
 'Q5(a)(iii): detailed marking notes give 5C (0,2,3,5); the summary says 5D. Use the explicit detailed numeric allocation.',
 'Q6(b) matches all three functions to their derivatives in one response. The six diagrams are required context, not six selectable tasks.',
 'Q7(a)(i): the rest is from 40 to 50 seconds on the paper. The partial-credit example says 45 to 55; the final duration of 10 seconds is correct.',
 'Q7(d)(ii): subtracting 4.6993 from 25 gives 20.3007, not the printed intermediate 20.27. The final 20.3 degrees Celsius is correct.',
 'Q7(a)(iii) retains all three printed choices and justification in one card.',
 'Q8(a)(ii)–(iii): the official partial-credit descriptions overlap at twelve correct items. Preserve the wording and make the ambiguity explicit rather than inventing a replacement criterion.',
 'Q8(a)(iv) and Q9(d)(ii)–(iii) require work on graphs, but the scheme supplies only text. Attributed NextStepUni worked graphs supply the missing drawings while retaining the original SEC criteria.',
 'Q9(c): use the byte values printed in the exam table, including its nonstandard 1 petabyte = 2^60 bytes; do not silently change the examination data.',
 'Q9(d)(ii): the continuous model crosses 200 zettabytes during 2027, not at the start of 2028. The scheme labels the two shared-task credit notes (i),(ii), corresponding to paper (ii),(iii).',
 'Q10(c): the scheme uses T_n for grey tiles; Q10(d) uses T_n for total tiles. Keep these distinct: grey n+2, white n(n+1), total n^2+2n+2.',
 ],out_name='2024-ordinary-p1-deferred.json',atlas_prefix='mathematics-ordinary-',section_of=lambda q:'A' if q<=6 else 'B')
def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None):
 p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,dict(figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))
A('1-a-i-ii','Q1(a)(i),Q1(a)(ii)','15D',[6],[4],'3-3','financial-maths',
 '(i) Find how much money will be in the account after 1 year. (ii) Hence, or otherwise, find how much money will be in the account at the end of 2 years.',
 ['At least one correct substitution'],
 'Fiadh has €1500 saved. She put this money in a savings account with a rate of 3% per annum compound interest.')
A('1-b-i-ii','Q1(b)(i),Q1(b)(ii)','15D',[6],[5],'3-3','financial-maths',
 '(i) At what annual income does a worker start paying the top rate of USC? (ii) Mike’s annual income for 2024 is €65 000. Work out how much he will pay in USC for 2024.',
 ['Correct formulation of any two USC rates','Work of merit in both parts'],
 'The table gives the 2024 USC rates: first €12 012 at 0·5%; next €13 748 at 2%; next €44 284 at 4%; balance at the top rate.')
complex_stem='In this question, i² = −1. z₁ = −4 + 2i and z₂ = 2 − i are two complex numbers.'
A('2-a-i-ii','Q2(a)(i),Q2(a)(ii)','10D',[7],[6],'4-4','complex-numbers',
 '(i) Plot and label z₁ and z₂ on the Argand Diagram below. (ii) Write down the complex conjugate of z₁.',
 ['One item correct','Two items correct'],complex_stem)
A('2-a-iii','Q2(a)(iii)','10C',[7],[6],'4-4','complex-numbers',
 'Work out the modulus of z₁. That is, find |z₁|. Give your answer in the form a√b.',
 ['Modulus formula','Fully correct substitution into modulus formula'],complex_stem)
A('2-b','Q2(b)','10D',[8],[7],'4-4','complex-numbers',
 'u = 1 + 4i and v = a + bi are two complex numbers, where a, b ∈ ℤ. Given that u − 2v = −3 + 10i, find the value of a and the value of b.',
 ['Any relevant substitution in the given equation.'])
A('3-a','Q3(a)','10D',[9],[8],'4-3','algebra-equations',
 'Solve the following inequality in x ∈ ℕ: 5(x − 3) + 2 < 11. List your solutions. Remember that x ∈ ℕ.',
 ['but solution set not listed.'])
A('3-b','Q3(b)','5C',[9],[8],'4-1','algebra',
 'Write the following expression as a single fraction, where x ≠ 0, x ≠ −1, x ∈ ℝ: 1/x − 2/(x + 1). Give your answer in its simplest form.',
 ['identified as the lowest common denominator.','Some relevant multiplication.'])
A('3-c','Q3(c)','15D',[9],[9],'4-2','algebra-equations',
 'Use algebra to solve the simultaneous equations: xy = 6; x − y = 1.',
 ['Writes one variable in terms of the other','Finds the two co-ordinate sets','Three steps correct'])
A('4-a-i-ii','Q4(a)(i),Q4(a)(ii)','15D',[10],[10],'5-1','functions,algebra',
 '(i) Find the value of f(0). (ii) Write f(x) in the form ax² + bx + c, where a, b, c ∈ ℝ.',
 ['some correct substitution in (i) or some correct expansion in (ii)','(i) correct and work of merit in (ii).'],
 'f(x) = (x + 3)² + 5, where x ∈ ℝ.')
A('4-b','Q4(b)','10C',[10],[10],'4-2','algebra-equations',
 'Solve the following equation in x: 3x² − 4x − 9 = 0. Give each answer correct to 2 decimal places.',
 ['Quadratic formula written','Formula fully correctly substituted','Apply a * for no or incorrect rounding'])
A('4-c','Q4(c)','5C',[10],[11],'5-1','graphing-functions,functions',
 'The graph of the quadratic function g(x) is shown below, drawn to scale. The y-axis is not shown. Using the information below, draw the y-axis into the diagram. The roots are x = −2 and x = 3; g(0) = −6. Label the y-axis and the points where g(x) cuts both axes.',
 ['axis drawn but no labels','axis not labelled'])
A('5-a-i-ii','Q5(a)(i),Q5(a)(ii)','15D',[11],[12],'3-3','financial-maths,number-systems',
 '(i) The conversion rate is 1 m³ = 11·5452 kilowatt-hours. Find the volume of gas used since the previous reading, in m³, and hence show this is equal to 1385·424 kilowatt-hours. (ii) Gas costs 13·46 cent per kilowatt-hour. Find the cost of the gas used during this period, in euro, correct to 2 decimal places.',
 ['Volume of gas used:','One part correct and work of merit in the other part'],
 'In Caoimhe’s gas bill the volume of gas used is converted to kilowatt-hours. Her current gas-meter reading is 12 518 m³ and her previous reading was 12 398 m³.')
A('5-a-iii','Q5(a)(iii)','5C',[11],[12],'3-3','financial-maths',
 'Caoimhe’s total gas bill is €227·47 before VAT. Work out her total gas bill after VAT at 9% has been added. Give your answer in euro, correct to 2 decimal places.',
 ['some relevant use of 9%','Finds the total VAT'])
A('5-b','Q5(b)','10C',[11],[13],'3-4','area-volume',
 'Caoimhe wants to estimate the area of her farm, in m². She measures at intervals of 200 m, starting at the right-hand edge. The measurements are shown on the diagram, correct to the nearest metre. Use the Trapezoidal Rule and the measurements to estimate the area of the farm, in m².',
 ['Trapezoidal rule written.','Fully correct substitution.'])
cubic='h(x) = x³ − 6x² + 7x + 6, where x ∈ ℝ.'
A('6-a-i-ii','Q6(a)(i),Q6(a)(ii)','15D',[12],[14],'5-2','differentiation',
 '(i) Find h′(x), the derivative of h(x). (ii) Hence, find the slope of the tangent when x = 1.',
 ['some correct differentiation in (i) or some correct substitution in (ii)','One part correct and work of merit in the other part'],cubic)
A('6-a-iii','Q6(a)(iii)','5B',[12],[14],'5-2','differentiation,graphing-functions',
 'The graph of h(x) is shown for −0·5 ≤ x ≤ 4·5, x ∈ ℝ. Draw the tangent to the graph at the point where x = 1. Use the same axes and scales.',
 ['The point (1, 8) indicated on the diagram.','A line with a consistent slope with (a)(ii)'],cubic)
A('6-b','Q6(b)','10C',[12],[15],'5-2','differentiation,graphing-functions',
 'The first three diagrams show the graphs of a, b and c, which are cubic, quadratic and linear respectively. The next three show d, e and f, each a slope function (derivative) of a, b or c. Write d, e and f in the correct place in the table to match every function to its slope function.',
 ['some relevant work on diagrams','One correct.'])
swim='Lillian and Darragh visit a 50 m swimming pool. Lillian swims 50 m at a constant speed, rests, then swims a second 50 m at a different constant speed. The graph L shows her distance for the first 110 seconds.'
A('7-a-i','Q7(a)(i)','5B',[13],[16],'5-1','graphing-functions',
 'How long does Lillian stop for? Give your answer in seconds.',
 ['Indicates the period on the diagram.'],swim)
A('7-a-ii','Q7(a)(ii)','5C',[13],[16],'3-3','number-systems,graphing-functions',
 'Find Lillian’s speed for the first 50 m. Give your answer in metres per second.',
 ['Time = 40','or equivalent fraction'],swim)
A('7-a-iii','Q7(a)(iii)','5B',[13],[16,17],'5-1','graphing-functions',
 'Does Lillian’s speed increase, decrease or stay the same for the second 50 m? Tick one box only: Increases / Decreases / Stays the same. Give a reason for your answer.',
 ['Decreases','The slope is steeper for the first 50 m','Correct answer with no reason or incorrect reason'],swim)
A('7-b-i-ii','Q7(b)(i),Q7(b)(ii)','15D',[13],[16,17],'5-1','graphing-functions,number-systems',
 'Darragh swims at a constant speed of 10 m every 7 seconds. (i) How many seconds does it take him to swim 50 m? (ii) Darragh starts swimming 10 seconds after Lillian. He swims 50 m, stops for 5 seconds, then swims a second 50 m at the same constant speed. Graph the distance Darragh swims on the diagram and label it D. Use the same axes and scales.',
 ['Any relevant point on the graph.','(i) correct and one section of the graph correct'],swim)
A('7-c','Q7(c)','5B',[14],[18],'3-3','number-systems',
 'The average speed for the world record of the women’s 100 m freestyle is 1·934 metres per second. Work out how long it took her to swim the 100 m, in seconds. Give your answer correct to 2 decimal places.',
 ['Some use of given values','Apply a * for no or incorrect rounding'])
A('7-d-i-ii','Q7(d)(i),Q7(d)(ii)','15D',[14],[19],'4-2','algebra-equations,financial-maths',
 'Mike’s pool has volume 9 m³ and he wants to heat it to 25°C. Electricity costs €0·431 per kWh. (i) Work out the heating cost when the average air temperature is 13°C, in euro to 2 decimal places. (ii) Find the average air temperature T₁ when the heating cost is €21·20, in degrees Celsius to 1 decimal place.',
 ['some correct substitution into the given formula in (i) or (ii)','One part correct and work of merit in the other part'],
 'C = 1·163 P V (T₂ − T₁), where P is the electricity cost per kWh, V is the pool volume in m³, T₁ is the average air temperature in °C, and T₂ is the heated pool temperature in °C.')
firework='A firework is set off from a harbour. Its height above sea level is h(t) = −4·8t² + 41·65t + 20 metres, where t is seconds since set off, t ≥ 0, t ∈ ℝ and h(t) > 0.'
A('8-a-i','Q8(a)(i)','5B',[15],[20],'5-1','functions',
 'Show that the firework is set off from a height of 20 metres above sea level.',
 ['some correct substitution'],firework)
A('8-a-ii-iii','Q8(a)(ii),Q8(a)(iii)','15D',[15],[20],'5-1','graphing-functions,functions',
 '(ii) Complete the table of h(t) for t = 0, 1, 2, 3, 4, 5, 6, 7, 8, to the nearest whole number. The table supplies h(0) = 20, h(3) = 102 and h(8) = 46. (iii) Draw the graph of h(t) for 0 ≤ t ≤ 8, t ∈ ℝ.',
 ['Solution requires 16 items, 6 values in table, 9 points plotted and the curve','Apply a * if 15 items correct'],firework)
A('8-a-iv','Q8(a)(iv)','5B',[15],[20,21],'5-1','graphing-functions',
 'The firework fails to explode. Continue your graph from part (a)(iii) to find how long it takes from set off to reach sea level: find t for which h(t) = 0. Show your work on the graph and give your answer in seconds.',
 ['9.1','continues the graph.'],firework)
A('8-b-i-ii','Q8(b)(i),Q8(b)(ii)','10D',[15],[22],'5-2','differentiation',
 'The firework is designed to explode at its maximum height. (i) Use calculus to find t when it is at its maximum height. (ii) Use your answer to find its maximum height.',
 ['some correct differentiation in (i) or some relevant substitution in (ii)','Work of merit in both parts','No units or incorrect units'],
 'A second firework’s height above sea level is g(t) = −5t² + 45t + 20 metres, where t is seconds since set off, t ≥ 0, t ∈ ℝ and g(t) > 0.')
mixture='In this exam question, a pyrotechnician’s mixture contains 3/4 potassium nitrate, 3/20 charcoal and 1/10 sulphur.'
A('8-c-i','Q8(c)(i)','10C',[16],[23],'3-3','number-systems',
 'Express potassium nitrate : charcoal : sulphur in the ratio a : b : c in its simplest form, where a, b, c ∈ ℕ.',
 ['Correct common denominator identified.','but ratio not in simplest form.'],mixture)
A('8-c-ii','Q8(c)(ii)','5B',[16],[23],'3-3','number-systems',
 'There are 25 grams of charcoal in the mixture. Work out how many grams of potassium nitrate are in this mixture.',
 ['125 g of potassium nitrate in the mixture.'],mixture)
A('9-a-i-ii','Q9(a)(i),Q9(a)(ii)','15D',[17],[24],'3-3','financial-maths',
 'A company sells memory sticks. (i) A memory stick costs €19·99, reduced to €16·99 in a sale. Find the percentage discount, to the nearest percent. (ii) The company buys 10 000 memory sticks from the USA at $9·50 each. Use €1 = $1·09 to find the total cost in euro, correct to 2 decimal places.',
 ['Finds the discount.','Finds the cost of 10000 units in dollars.','Apply a * for no or incorrect rounding'])
A('9-b','Q9(b)','5C',[17],[24],'3-3','number-systems',
 'Seán’s flight from Shannon to New York took off at 09:45. New York is 5 hours behind Ireland. The flight time is 7 hours 35 minutes. What is the local time when his flight is due to land?',
 ['some relevant addition or subtraction','17:20 or 5.20 found'])
bytes='Use the examination table: 1 gigabyte = 2³⁰ bytes; 1 terabyte = 2⁴⁰ bytes; 1 petabyte = 2⁶⁰ bytes.'
A('9-c-i','Q9(c)(i)','5B',[17],[25],'3-2','indices',
 'Write the number of bytes in one gigabyte in the form a × 10ⁿ, where 1 ≤ a < 10 and n ∈ ℤ. Give a correct to 3 significant figures.',
 ['Apply a * for no or incorrect rounding'],bytes)
A('9-c-ii','Q9(c)(ii)','10C',[17],[25],'3-2','indices',
 'A desktop computer has 1 terabyte of storage. A NASA super computer has 7·6 petabytes. Work out how many desktop computers are needed to equal the NASA computer’s storage. Give your answer correct to the nearest whole number.',
 ['Converts either 1 terabyte or 7 ∙6 petabytes to bytes.','Apply a * for no or incorrect rounding'],bytes)
data='At the start of 2021 the world had approximately 64 zettabytes of data. The predicted growth up to the start of 2029 is d(t) = 64(1·19)^t, where t is years since the start of 2021, 0 ≤ t ≤ 8, t ∈ ℝ.'
A('9-d-i','Q9(d)(i)','5C',[18],[26],'5-1','functions,indices',
 'Use d(t) to find the predicted amount of data in the world by the start of 2026, in zettabytes to 1 decimal place.',
 ['in the given function.','Apply a * for no or incorrect rounding'],data)
A('9-d-ii-iii','Q9(d)(ii),Q9(d)(iii)','10C',[18],[26,27],'5-1','graphing-functions',
 '(ii) In which year will the predicted amount of data first reach 200 zettabytes? (iii) Use suitable values from the graph to estimate the number of years it takes for the amount of data to double, to the nearest whole number. Show your work for both parts on the graph.',
 ['2027','approximately 4 years for data to double','Or similar'],data)
tiles='The first three patterns shown contain grey tiles and white tiles.'
A('10-a','Q10(a)','5B',[19],[28],'4-1','sequences-series',
 'Draw the fourth pattern in the sequence into the box below.',
 ['correct number of grey tiles.','No shading','One tile missing'],tiles)
A('10-b','Q10(b)','10C',[19],[28],'4-1','sequences-series',
 'Complete the table to show the number of grey tiles, white tiles and total tiles in the first four patterns. Given entries: pattern 1 has 3 grey, 2 white, total 5; pattern 2 total 10; pattern 3 has 5 grey; pattern 4 has 20 white.',
 ['Solution consists of 6 table entries:','1 correct table entry.','4 correct table entries.'],tiles)
A('10-c-i','Q10(c)(i)','5C',[19],[28,29],'4-1','sequences-series',
 'Find a formula in terms of n for the number of grey tiles in pattern n, where n ∈ ℕ.',
 ['Correct formula'],tiles)
A('10-c-ii','Q10(c)(ii)','5B',[19],[28,29],'4-1','sequences-series',
 'Using your formula from part (c)(i), or otherwise, work out the number of grey tiles in the 25th pattern.',
 ['some correct substitution into formula derived in (i).','Finds a new term in the pattern'],tiles)
A('10-c-iii','Q10(c)(iii)','5C',[20],[28,29],'4-1','sequences-series',
 'Find the total number of grey tiles in the first 25 patterns of the sequence.',
 ['375 tiles','Formula fully substituted.'],tiles)
A('10-c-iv','Q10(c)(iv)','5B',[20],[28,29],'4-1','sequences-series',
 'Find how many white tiles are in the 8th pattern of the sequence.',
 ['72 tiles','finding Pattern 5.'],tiles)
A('10-d-i-ii','Q10(d)(i),Q10(d)(ii)','15D',[20],[30],'4-2','algebra-equations,sequences-series',
 '(i) Remember T₂ = 10. Substitute in the formula to show that 2b + c = 6. (ii) Solve b + c = 4 and 2b + c = 6 to find b and c.',
 ['Some work of merit in forming equation.','One part correct and work of merit in the other part'],
 'The total number of tiles in pattern n is Tₙ = n² + bn + c, where b, c ∈ ℝ are constants.')
assert len(p.cards)==42
selection_review=[
 {'pages':[3,4,16],'wording':'any five / any three questions','classification':'exam-level-selection','reason':'Every offered question retained for practice.'},
 {'pages':[4,29],'wording':'or otherwise','classification':'method-choice','reason':'Alternative methods solve the same task.'},
 {'pages':[15],'wording':'either a, b or c','classification':'answer-selection','reason':'All three graph matches required in one shared allocation; the six graphs are not alternative tasks.'},
 {'pages':[17],'wording':'Tick one box only','classification':'answer-selection','reason':'All three speed choices and justification retained in one card.'},
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','Examination choice; retain every question for practice.')
 if 'or otherwise' in t:return ('method-choice','Alternative ways to solve the same required task.')
 if 'slope function' in t or 'derivative' in t:return ('answer-selection','All three function matches required together, not alternative practice tasks.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
