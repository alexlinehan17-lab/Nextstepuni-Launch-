"""Independent visual paper and published-scale review: 2025 deferred HL Paper 1."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper

PREFIX='maths-2025-hl-p1-deferred'
p=Paper(year=2025,level='higher',paper_key='p1',sitting='deferred',
    paper_file='LC003ALP100EV-deferred.pdf',scheme_file='LC003ALP000EV-deferred.pdf',
    prefix=PREFIX,ref='2025 HL Paper 1 — Deferred',
    scales={'5B':[0,2,5],'5C':[0,2,3,5],'5D':[0,2,3,4,5],
            '10B':[0,5,10],'10C':[0,4,6,10],'10D':[0,2,4,6,10],
            '15C':[0,4,8,15],'15D':[0,4,7,10,15]},
    reviewed_at='2026-10-30',general_notes=[2,4,5,6,7],scheme_pages=list(range(1,26)),
    printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
    review_method='Independent visual sweep of all 32 question-paper pages and scheme pages 1–25. Every printed part cross-checked against its own published scale; all question and solution images are separately inspected before publication.',
    source_notes=[
        'All ten questions retained: 380 offered marks, with candidates selecting five Section A and three Section B questions for 300 marks.',
        '40 independently marked tasks. Q6(c)(i)–(ii) share one 10C scale; Q7(a)–(b) share one 10D scale and remain together.',
        'Q4(b) and Q7(d) each require one tick and a justification. All printed options remain in one card; no combinations are generated.',
        'Q1(c) uses n in the paper, but the final lines of the model solution use x. A note explains that these lines refer to n; n=1 satisfies the domain and n=-2 is excluded.',
        'Q3(c): the model answer’s sum 6 and product 10 refer to the conjugate pair, not all three roots. A note makes this explicit.',
        'Q4(b): a horizontal line sufficiently close to and below the local maximum meets the continuous graph on both sides. The scheme’s phrase for all values of y<12 is too broad; the student-facing note gives the local argument.',
        'Q7(a)–(b): the scheme prints A(1)=101.3 for the constant A, and labels 32.68 as 1 d.p. The question asks for two decimal places; the note retains A=101.3 and 32.68 to two decimal places.',
        'Q9(b)(ii): the scheme calculates the positive magnitude 1.35 m³/hour of the decrease. The signed derivatives are dh/dt=-0.03 and dV/dt=-1.35; the distinction is explained.',
        'Q10(a)(i): the printed model graph is clipped at its right edge and contains paragraph glyphs. An explicitly attributed NextStepUni table and complete 0–32 second graph, calculated from the paper formula, precede the original SEC credit notes. The original full scheme remains accessible.',
        'Q10(a)(iii) prints Scale 10C (0,4,6,10), but also describes a Mid Partial Credit category. No extra numeric band is invented: the printed numeric scale and complete original notes are retained with an explicit inconsistency note.',
    ],out_name='2025-higher-p1-deferred.json',atlas_prefix='mathematics-higher-',section_of=lambda q:'A' if q<=6 else 'B')

def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None,extra=None):
    p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,
          dict(extra or {},figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))

A('1-a','Q1(a)','10C',[8],[4],'4-2','algebra-solving-equations,algebra-quadratics',
  'Solve the following equation in x. Give each answer correct to 2 decimal places. 2x² − 8x − 11 = 0.',
  ['Fully substituted quadratic formula','Apply a * for no rounding or incorrect rounding'])
A('1-b','Q1(b)','10D',[8],[4],'4-3','algebra-inequalities',
  'Find the range of values of p ∈ ℝ for which: |2p + 7| ≥ 3.',
  ['One value of p found','Both values of p found','Apply a * once if strict inequality/inequalities are used'])
A('1-c','Q1(c)','10D',[9],[5],'3-2','indices-and-logs',
  'Solve the following equation for n ∈ ℝ, where n > 0: log₂(8 − 4n) − 2 log₂ n = 2.',
  ['Simplifies to an equation in n with one log','Equation written without logs','Apply a * for incorrect solution not eliminated'])
A('2-a','Q2(a)','15D',[10],[6],'3-1','induction',
  'Prove by induction that the following identity is true for all n ∈ ℕ: 1 + 2 + 3 + … + n = n(n + 1)/2.',
  ['2 steps correct','3 steps correct','Omits part or all of conclusion but otherwise correct.'])
A('2-b-i','Q2(b)(i)','5D',[10],[7],'4-2','algebra-solving-equations,algebra-quadratics',
  'Solve the equation 1/y + 2y = 3, where y ∈ ℝ, y ≠ 0.',
  ['Sets up quadratic equation','Factors found','Correctly substituted quadratic formula'])
A('2-b-ii','Q2(b)(ii)','10D',[11],[7],'3-2','indices-and-logs',
  'Hence, or otherwise, find the values of x ∈ ℝ for which: 4⁻ˣ + 2(4ˣ) = 3.',
  ['Finds one correct value of x'],stem='Part (b)(i) asks you to solve 1/y + 2y = 3, where y ∈ ℝ, y ≠ 0.')
A('3-a','Q3(a)','5C',[12],[8],'4-4','complex-numbers',
  'The complex number z₁ is shown in the Argand diagram below. Three other complex numbers are plotted, and are labelled A, B, and C, respectively. Write A, B, and C in the appropriate spaces in the table below, to show which point represents each complex number: −z₁, the complex conjugate of z₁, and iz₁.',
  ['One point correctly identified'],stem='In this question, i² = −1. The original Argand diagram and table are included.')
A('3-b','Q3(b)','15D',[12],[8],'4-4','complex-numbers',
  'Use De Moivre’s theorem to solve the equation w² = 4i. Give each answer in the form a + bi, where a, b ∈ ℝ.',
  ['2 steps correct','3 steps correct','Roots found correctly, but one or both in polar form'],stem='In this question, i² = −1.')
A('3-c','Q3(c)','10C',[13],[9],'4-4','complex-numbers,algebra-cubics',
  'z = (3 − i) is a root of the equation: z³ − 2z² − 14z + 40 = 0. Find the other two roots of this equation. One should be complex and the other should be real.',
  ['Finds quadratic factor'],stem='In this question, i² = −1.')
A('4-a','Q4(a)','10D',[14],[10],'4-2','algebra-simultaneous-equations',
  'Solve the following pair of simultaneous equations in x, y ∈ ℝ: y = 3x² − 32x + 54; y = 2x + 14.',
  ['Equation in one variable correctly established','x values found, but no y values','y values found, but no x values'])
A('4-b','Q4(b)','10C',[14],[10],'5-1','functions',
  'f: ℝ → ℝ is a continuous function. The graph of y = f(x) has one local maximum point, which is at (7, 12). Is y = f(x) injective (one-to-one) on the interval x ∈ [6, 8]? Justify your answer. Hint: draw a sketch of the graph of y = f(x) near the point (7, 12). Tick one box only: Yes; No; We don’t have enough information to be sure.',
  ['Correct box ticked','Correct box ticked with work of merit in justification'])
A('4-c','Q4(c)','10D',[15],[11],'5-2','integration',
  'The diagram shows the graphs of the functions h(x) and k(x), where h(x) = −½x² + 4x + 1 and k(x) = 9 − x. Note that h(2) = k(2) and h(8) = k(8). Use integration to find the area enclosed between the graphs of h(x) and k(x), from x = 2 to x = 8.',
  ['Integration indicated','Integration of both functions (or combined function) fully correct'])
A('5-a','Q5(a)','10C',[16],[12],'4-1','algebra-expressions-factorising',
  'Multiply out and simplify (x − 1)³.',
  ['Binomial expanded correctly','One error in binomial expansion, but otherwise correct'])
A('5-b','Q5(b)','10D',[16],[12],'5-2','differentiation-applications',
  'A cubic function h(x) has the following equation in x ∈ ℝ: h(x) = x³ − 6x² − 15x + 10. Find the co-ordinates of the local maximum point and the local minimum point of h(x).',
  ['Differentiation fully correct','x values found','Turning points found, but max/min not identified'])
A('5-c','Q5(c)','10D',[16],[13],'5-2','differentiation-rules,differentiation-applications',
  'f is the following function, where x ∈ ℝ, x ≠ ½: f(x) = 2x + 5 + 1/(2x − 1). Find the values of x for which f′(x) = 0.',
  ['Award Low Partial Credit at most, if chain or quotient rule is not used','Differentiation fully correct','Quadratic without fraction'])
A('6-a','Q6(a)','10D',[17],[14],'3-2','indices-and-logs',
  'The population of a region is now 6·7 million people. This population is growing at a rate of 10% per year. At this growth rate, the population will be greater than 20 million for the first time n years from now, where n ∈ ℕ. Find the value of n.',
  ['Equation / inequality set up','Log equation in n'])
A('6-b','Q6(b)','10D',[17],[14],'5-2','differentiation-rules',
  'f is the following function, where x ∈ ℝ is in radians: f(x) = sin 3x cos x. Use the product rule to find the value of f′(π/4).',
  ['Award LP credit at most if product rule is not used.','One step correct','Two steps correct'])
A('6-c-i-ii','Q6(c)(i),Q6(c)(ii)','10C',[17],[15],'5-1','functions',
  '(i) k ∈ ℝ is a constant. The horizontal line y = k does not cut the graph of y = g(x). Write down one possible value of k. (ii) p ∈ ℝ is a constant. The horizontal line y = p cuts the graph of y = g(x) at exactly 2 points. Write down the ranges of possible values of p.',
  ['Part (i) correct','Part (ii) correct'],
  stem='The continuous function y = g(x) is defined for −10 ≤ x ≤ 50, x ∈ ℝ. Its graph is shown below. It has three turning points: two local minimum points and one local maximum point. All of these are shown on the graph. The two endpoints of the graph are also shown. Use the information in the graph to answer the following questions.')
air='Air pressure is the pressure caused by the weight of air pressing down on the earth. Air pressure decreases as the height above sea level increases. Air pressure, P, can be estimated using the formula P(h) = Ae^(kh), where k = (ln 0·88)/1000, A is a constant, and h is the height in metres above sea level. Use this formula to answer parts (a) to (d).'
A('7-a-b','Q7(a),Q7(b)','10D',[18],[16],'5-1','functions,indices-and-logs',
  '(a) The air pressure at sea level (h = 0) is 101·3 units. Show that A = 101·3. (b) Find the air pressure at the top of Mount Everest, which is 8849 m above sea level. Give your answer correct to 2 decimal places.',
  ['One part correct','One part correct and work of merit in the 2nd part'],stem=air)
A('7-c','Q7(c)','10C',[18],[16,17],'3-2','indices-and-logs',
  'Altitude sickness is caused by low air pressure. Some people start to feel sick when the air pressure is at 80 units. At what height above sea level would these people start to feel sick? Give your answer correct to the nearest metre.',
  ['Some correct substitution','Equation in ℎ with no indices (logs handled correctly)'],stem=air+' Part (a) establishes A = 101·3.')
A('7-d','Q7(d)','10C',[18],[16,17],'5-1','functions,indices-and-logs',
  'A ball, B, is at sea level, so h = 0. A second ball, C, is at a height above sea level of H metres, where H > 0. Each ball is raised up 40 m, so that the air pressure on each decreases. Which ball, if any, will have a greater decrease in air pressure? Justify your answer. Tick one box only: B; C; B and C will have the same decrease.',
  ['Correct box ticked','Some relevant calculations','Correct box ticked with relevant but incomplete calculations given'],stem=air+' Part (a) establishes A = 101·3.')
air2='John is researching the connection between air pressure and height above sea level. On a website, he finds a different formula to estimate air pressure, P: P(h) = 101·325(1 − 2·2557 × 10⁻⁵ × h)⁵·²⁵⁵⁸, where h ≥ 0 is the height in metres above sea level. Use this formula to answer parts (e)(i) and (e)(ii).'
A('7-e-i','Q7(e)(i)','5B',[19],[18],'5-1','functions,indices-and-logs',
  'Find the air pressure at the top of Mount Everest, which is 8849 m above sea level. Give your answer correct to 2 decimal places.',
  ['Correct substitution for ℎ'],stem=air2)
A('7-e-ii','Q7(e)(ii)','15C',[19],[18],'3-2','indices-and-logs',
  'Work out the value of h for which the air pressure is 80 units, according to this formula. Give your answer correct to the nearest metre.',
  ['Equation with ℎ term to the power of 1','Apply a * for incorrect rounding or no rounding'],stem=air2)
pension='Jon has decided to put money into a pension fund for the next 25 years. He puts €285 into his pension fund at the start of every month for 300 months, at an interest rate of 0·35% per month.'
A('8-a-i','Q8(a)(i)','5C',[20],[19],'3-3','financial-maths,sequences-series',
  'Write the total amount of money in his pension fund at the end of the 25 years as the sum of a series. Include the first two and last two terms of the series.',
  ['2 correct terms'],stem=pension)
A('8-a-ii','Q8(a)(ii)','10C',[20],[19],'3-3','financial-maths,sequences-series',
  'Find the total amount of money in the pension fund at the end of the 25 years. Give your answer correct to the nearest cent.',
  ['formula with fully correct substitution','Apply a * for no rounding or incorrect rounding'],stem=pension)
A('8-b','Q8(b)','10C',[20],[20],'3-3','financial-maths',
  'At the end of the 25 years, Jon also puts an additional lump sum into his pension fund. His total pension fund is now €165 646·20. At this point, Jon retires, and stops paying money into his pension fund. Instead, he is now going to take out €A per month at the end of each month, for the next 20 years. Assuming that the interest rate remains at 0·35% per month, work out the maximum value that A can be. (That is, the value of A that would mean there is no money left in the pension fund after 20 years.)',
  ['Formula with some substitution','Fully substituted amortisation/Sn formula'])
cameras='Before he retired, Jon worked for a company making two types of speed camera, X and Y. In 2020, the company made x cameras of Type X, and y cameras of Type Y. In 2020, 40% of the cameras the company made were Type X.'
A('8-c-i','Q8(c)(i)','5B',[21],[20],'4-1','algebra-expressions-factorising',
  'Use this to write y in terms of x.',
  ['Accept correct answer without work','mentions 60%'],stem=cameras)
A('8-c-ii','Q8(c)(ii)','10D',[21],[20,21],'4-2','algebra-simultaneous-equations',
  'In 2021, the company increased the number of Type X cameras it made by 1500, and increased the number of Type Y cameras by 900. As a result, in 2021, 50% of the cameras the company made were Type X. Work out the total number of cameras the company made in 2021.',
  ['Finds the value of x or y'],stem=cameras)
A('8-d','Q8(d)','10C',[21],[21],'3-3','algebra-solving-equations',
  'According to a Type X speed camera, a car is travelling at 112 km/hour. The company claims that their Type X speed camera can measure speed with a maximum error of 3·5%. Use this to work out the maximum actual speed of the car. Give your answer in km/hour, correct to 1 decimal place.',
  ['Formula with full substitution','Apply a * for incorrect rounding or no rounding'])
net='The net of a closed cylinder with a radius x cm and a height h cm is cut out from a rectangular sheet of tin. The width of the sheet is 20 cm. The diagram below shows the sheet of tin, as well as the net of the cylinder cut from this sheet (the shaded region). The net is made up of a rectangle with a width of h cm (which is the height of the cylinder), and two circles, each of radius x cm. Each circle has two tangents in the diagram.'
A('9-a-i','Q9(a)(i)','5B',[22],[22],'4-1','algebra-expressions-factorising,area-volume',
  'Use this information to write h in terms of x.',
  ['diameter = 4x'],stem=net)
A('9-a-ii','Q9(a)(ii)','10C',[22],[22],'3-4','area-volume',
  'Show that the volume of the cylinder can be written as: V(x) = 20πx² − 4πx³.',
  ['Accept candidates expression for h from part(i)','Volume of cylinder formula fully substituted in terms of x'],stem=net)
A('9-a-iii','Q9(a)(iii)','10D',[22],[23],'5-2','differentiation-applications',
  'Use differentiation to find the maximum volume that such a cylinder can have. Give your answer correct to the nearest cm³. Remember that V(x) = 20πx² − 4πx³.',
  ['1 step correct','2 steps correct'],stem='V(x) is the volume, in cm³, of a cylinder cut from the sheet of tin in part (a), with radius x cm.')
A('9-a-iv','Q9(a)(iv)','5C',[23],[22,23],'4-2','algebra-cubics,functions',
  'The graph on the right shows V(x) for a range of values of x ∈ ℝ. The x-axis is shown, but the y-axis is not. The graph of V(x) cuts the x-axis at the points (a, 0) and (b, 0), with a < b, as shown. By referring to the diagram on the previous page, or otherwise, find the value of a and the value of b.',
  ['Accept correct answers without work','One value of x given'],stem=net+' V(x) = 20πx² − 4πx³.')
liquid='The volume, V, of liquid in a different container can be calculated using the formula: V(h) = (5h² + 4)^(3/2) − 6, where h is the height of the liquid in the container, in m, and V is measured in m³.'
A('9-b-i','Q9(b)(i)','5C',[23],[24],'3-2','indices-and-logs',
  'Find the height of the liquid in the container when the volume of liquid is 203·285 m³. Give your answer in metres, correct to 1 decimal place.',
  ['Equation set up','Equation with index removed'],stem=liquid)
A('9-b-ii','Q9(b)(ii)','15D',[23],[24,25],'5-2','differentiation-applications',
  'Liquid is leaking from this container. At a certain time, the height of the liquid in the container is 1 m. At this time, the height of the liquid is decreasing at a rate of 0·03 m/hour. Find the rate at which the volume of liquid in the container is decreasing at this time. Give your answer in m³/hour.',
  ['Steps can happen in different orders.','Step 2 does not need to be explicitly stated','2 steps correct','3 steps correct'],stem=liquid)
speed='The speed, in metres per second (m/s), of a skydiver who jumps from an airplane is given by: V(t) = 54(1 − e^(−0·2t)), where t is the time, in seconds, that has passed since the jump.'
A('10-a-i','Q10(a)(i)','15D',[24],[26],'5-1','functions',
  'Complete the table below and hence draw the graph of V(t) in the domain 0 ≤ t ≤ 32, t ∈ ℝ, on the grid below. Give your values correct to 1 decimal place. The table gives t = 0, 4, 8, 12, 16, 20, 24, 28, 32, with V(4) = 29·7 and V(24) = 53·6 already supplied.',
  ['3 parts correct','8 parts correct','14 parts correct','16 parts correct'],stem=speed)
A('10-a-ii','Q10(a)(ii)','10C',[24],[26],'5-2','differentiation-applications',
  'Find the acceleration (rate of change of speed) of the skydiver one second after they jump from the airplane. Give your answer, in m/s², correct to 1 decimal place.',
  ['Differentiation fully correct','Apply a * for incorrect rounding or no rounding'],stem=speed)
A('10-a-iii','Q10(a)(iii)','10C',[25],[26,27],'5-2','integration',
  'Use integration to find the average speed of the skydiver over the first 10 seconds after the jump. Give your answer correct to the nearest m/s.',
  ['Indication of integration is required to be awarded any credit','Accept correct answer without unit','2 steps correct','3 steps correct'],stem=speed,
  extra={'markingNote':'The printed row gives Scale 10C (0, 4, 6, 10), but also mentions Mid Partial Credit without assigning a separate mark. The numeric scale is retained; the original notes are available below.'})
A('10-a-iv','Q10(a)(iv)','10B',[25],[26,27],'5-1','functions',
  'Find the terminal velocity of the skydiver, that is, find the value of lim V(t) as t → ∞.',
  ['Accept correct answers without work','substitutes 2 or more positive integers for t'],stem=speed)
A('10-b','Q10(b)','5B',[25],[28],'3-3','algebra-expressions-factorising',
  'The airplane flies d km out to a jumpsite, at an average speed of x km/hour. It then flies d km back from the jumpsite. Throughout the return journey, its speed is 10% less than x km/hour. Find the percentage increase in the time it will take for the return journey. Give your answer as a percentage, correct to 1 decimal place.',
  ['Work of merit, for example, return speed'])

assert len(p.cards)==40
selection_review=[
 {'pages':[3,4,16],'wording':'Any five / Any three questions','classification':'exam-level-selection','reason':'Every question is retained for practice, including questions not selected during the examination.'},
 {'pages':[7,23],'wording':'or otherwise','classification':'method-choice','reason':'Alternative solution methods within the same task; no task selection or expansion.'},
 {'pages':[10,17],'wording':'Tick one box only','classification':'answer-selection','reason':'Each question is one choice-and-justification task. All three printed options remain together.'},
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','Exam-level selection; all questions retained for practice.')
 if 'tick' in t or 'box' in t:return ('answer-selection','One choice-and-justification task with all printed options.')
 if 'otherwise' in t:return ('method-choice','Alternative mathematical methods for the same required task.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
