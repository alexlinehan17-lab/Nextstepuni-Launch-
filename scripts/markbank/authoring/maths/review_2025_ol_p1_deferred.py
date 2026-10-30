"""2025 deferred OL Paper 1: every published scale, independently read in print."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper

PREFIX = 'maths-2025-ol-p1-deferred'
p = Paper(
    year=2025, level='ordinary', paper_key='p1', sitting='deferred',
    paper_file='LC003GLP100EV-deferred.pdf', scheme_file='LC003GLP000EV-deferred.pdf',
    prefix=PREFIX, ref='2025 OL Paper 1 — Deferred',
    scales={'5B':[0,2,5], '5C':[0,2,3,5], '10C':[0,3,7,10], '10D':[0,3,5,8,10], '20D':[0,5,10,15,20]},
    reviewed_at='2026-10-30', general_notes=[2,4,5,6,7], scheme_pages=list(range(1,24)),
    printed_marks={**{str(q):30 for q in range(1,7)}, **{str(q):50 for q in range(7,11)}},
    review_method='Independent visual sweep of all 32 question-paper pages and scheme PDF pages 1–23. Every printed part was compared with its own scheme row; shared scales stay together. Original question crops and complete solution/credit-note rows are separately inspected before publication.',
    source_notes=[
        'All ten questions retained: 380 offered marks; the candidate chooses five 30-mark and three 50-mark questions for 300 marks.',
        '41 separately marked tasks. Shared scales: Q2(a)(i)–(ii), Q3(b)(i)–(ii), Q5(b)(i)–(ii), Q9(a)(ii)–(iii), Q9(b)(i)–(ii), Q10(a)(i)–(ii), Q10(b)(i)–(ii).',
        'Q1(c) prints Scale 10D (0,3,5,7,10) on scheme page 8, whereas the general Paper 1 table prints (0,3,5,8,10). The task-specific row is retained exactly, with the discrepancy disclosed.',
        'The Q3(b) model-solution row puts the positive tick above the x-values; the card follows the question paper order and retains the complete official scheme row.',
        'Deferred booklet identities carry -deferred in Paper Trail/Storage; the local SEC deferred archive uses the undecorated filename. June and deferred tasks are distinct.',
        'The general SEC note explains that deferred schemes may contain less detail than main-sitting schemes; no additional marking criteria have been invented.',
    ],
    out_name='2025-ordinary-p1-deferred.json', atlas_prefix='mathematics-ordinary-', section_of=lambda q:'A' if q<=6 else 'B',
)

def A(suffix, parts, scale, scheme, pages, topic, atlas, prompt, quotes, stem=None, extra=None):
    extra = dict(extra or {}, figureKey=f'{PREFIX}-q{suffix}-solution', questionFigureKey=f'{PREFIX}-q{suffix}-question')
    p.add(suffix, parts, scale, scheme, pages, topic, atlas, prompt, quotes, stem, extra)

A('1-a','Q1(a)','10C',[7],[4],'4-2','algebra-equations',
  'Solve the following equation, where x ∈ ℝ: 4(x − 2) + 10 = 3x',
  ['Carries out some relevant correct operation e.g. writes 4x'])
A('1-b','Q1(b)','10C',[7],[4],'4-2','algebra-equations',
  'Solve the following equation in x: 2x² − 4x − 13 = 0. Give each answer correct to 2 decimal places.',
  ['Quadratic formula written','Apply a * for no or incorrect rounding'])
A('1-c','Q1(c)','10D',[8],[5],'4-1','algebra',
  'Express as a single fraction in its simplest form: (3x − 1)/2 − (2x + 2)/5',
  ['One step correct','Two steps correct','Three steps correct'],
  extra={'permittedMarks':[0,3,5,7,10], 'markingNote':'The task-specific scheme row awards 7 marks for high partial credit. This differs from the general 10D table, which lists 8.'})
z='In this question, i² = −1. z₁ = 4 + 3i and z₂ = 2 − i are complex numbers.'
A('2-a-i-ii','Q2(a)(i),Q2(a)(ii)','10D',[9],[6],'3-1','number-systems',
  '(i) Plot and label the two complex numbers z₁ and z₂ on the Argand diagram below. (ii) The complex number w is shown on the Argand diagram. Write w in the form p + qi, where p, q ∈ ℝ.',
  ['One item correct','Work of merit in two items','Two items correct'],stem=z)
A('2-b','Q2(b)','10C',[9],[6,7],'3-1','number-systems',
  'z₃ = z₁ − 3z₂. Write z₃ in the form a + bi, where a, b ∈ ℤ.',
  ['Some correct expansion of −3(2 − i)'],stem=z)
A('2-c','Q2(c)','10D',[10],[6,7],'3-1','number-systems',
  'z₄ = z₁/z₂. Write z₄ in the form c + di, where c, d ∈ ℤ.',
  ['Some relevant correct multiplication','Correct substitution AND correct conjugate written'],stem=z)
f='f(x) = x² − x − 2, where x ∈ ℝ.'
A('3-a-i','Q3(a)(i)','10C',[11],[8],'5-1','functions',
  'Find f(5) and f(−3).',['Some correct substitution into function'],stem=f)
A('3-a-ii','Q3(a)(ii)','10C',[11],[8],'4-2','algebra-equations,functions',
  'Find the co-ordinates of the points where f(x) crosses the x-axis. (That is, where f(x) = 0.)',
  ['Some attempt at factorising or quadratic formula'],stem=f)
A('3-b-i-ii','Q3(b)(i),Q3(b)(ii)','10D',[11],[9],'5-2','differentiation,graphing-functions',
  '(i) Write down two values of x for which g′(x) = 0, where g′(x) is the derivative of g(x). (ii) Is g′(11) positive or negative? Give a reason for your answer. You may include work on the diagram. Tick one box only: Positive or Negative.',
  ['One part correct','Work of merit in both parts'],stem='Part of the graph of the function g(x) is shown in the diagram below.')
f='f(x) = x³ + 2x² − 5.'
A('4-a','Q4(a)','5B',[12],[10],'5-2','differentiation',
  'Find f′(x), where f′(x) is the derivative of f(x).',['Some correct differentiation'],stem=f)
A('4-b','Q4(b)','10C',[12],[10],'5-2','differentiation',
  'Show that f′(1) = 7.',['Fully correct substitution.'],stem=f)
A('4-c','Q4(c)','10C',[12],[10],'5-2','differentiation,co-ordinate-geometry-of-the-line',
  'Hence, find the equation of the tangent to f(x) when x = 1.',
  ['Finds equation','Two steps correct'],stem=f+' The preceding part asks you to show that f′(1) = 7.')
A('4-d','Q4(d)','5B',[12],[10,11],'5-1','functions',
  'g(x) = x + 11. Find g(f(x)) in terms of x.',
  ['Work of merit, for example, attempts to'],stem=f)
graph='The graph of the function f(x) in the domain −2 ≤ x ≤ 3, where x ∈ ℝ, is shown in the diagram on the right. This graph is symmetrical.'
A('5-a-i','Q5(a)(i)','10C',[13],[12],'5-1','graphing-functions',
  'Use the points shown on the graph to complete the table below. The table gives x = −2, −1, 0, 1, 2, 3, with f(−2) = 0, f(0) = 6 and f(2) = 4.',
  ['One value correct','Two values correct'],stem=graph)
A('5-a-ii','Q5(a)(ii)','10C',[13],[12],'3-4','area-volume',
  'Use the Trapezoidal Rule to estimate the area between the graph and the x-axis. (Use the values of f(x) from your table as your heights.)',
  ['Formula fully substituted correctly','Apply a * for no or incorrect units'],stem=graph)
A('5-b-i-ii','Q5(b)(i),Q5(b)(ii)','10D',[13],[13],'3-2','indices',
  '(i) Express 16 and 32 in the form 2^k, where k ∈ ℕ. (ii) Hence, or otherwise, find the value of x for which 16^x = 32, where x ∈ ℝ.',
  ['One part correct','Work of merit in both parts'])
A('6-a','Q6(a)','10C',[14],[14],'3-3','financial-maths',
  'John invested €3400 for 2 years. The interest rate was 4% for year 1 and 5% for year 2. Find the amount of the investment at the end of year 2.',
  ['Amount at the end of year one correct'])
A('6-b','Q6(b)','10C',[14],[14],'3-3','financial-maths',
  'John’s car was valued at €25 000 one year ago. Today it has a value of €21 250. Find the percentage decrease in the value of the car over the course of the year.',
  ['Work of merit, for example, finds decrease'])
A('6-c','Q6(c)','10D',[14],[15],'3-3','financial-maths',
  'Mary bought a painting 3 years ago. The value of the painting increased by 20% during each year for the last 3 years. The painting is now worth €8640. Find the value of the painting when Mary bought it.',
  ['Works back one year correctly','Works back two years correctly'])
house='Anna and Ross are saving to buy a house. Anna’s gross annual salary is €50 800 and Ross’s gross annual salary is €48 500. The maximum that they can borrow is 4 times their gross combined salaries.'
A('7-a-i','Q7(a)(i)','10C',[15],[16],'3-3','financial-maths',
  'What is the maximum amount of money that they can borrow?',
  ['Finds 99300','Multiplies one of the incomes by 4 and then adds on the other income'],stem=house)
A('7-a-ii','Q7(a)(ii)','5B',[15],[16],'3-3','financial-maths',
  'They are interested in buying a house that costs €395 000. In order to qualify for a mortgage they must have a deposit of at least 12·5% of the price of a house. How much of a deposit do they need to have in order to qualify for a mortgage for this house?',
  ['Accept correct answer without work for full credit'],stem=house)
A('7-a-iii','Q7(a)(iii)','10C',[15],[17],'3-3','financial-maths',
  'The builder expects to make a profit of 15% when this house is sold for €395 000. Find the cost of building this house. Give your answer correct to the nearest euro.',
  ['Apply a * for no or incorrect rounding'])
A('7-b','Q7(b)','10C',[15],[18],'3-3','financial-maths',
  'Mary earns €55 000 per year. She pays €10 100 tax on her income. She also pays €1561·42 in U.S.C. (Universal Social Charge). Find her net income and write it as a percentage of her gross income. Give your second answer correct to 1 decimal place.',
  ['Subtracts one of the deductions from gross income','Apply a * for no or incorrect rounding'])
A('7-c-i','Q7(c)(i)','10D',[16],[19],'3-3','financial-maths',
  'John earns €49 572 per year. The table on the right shows the rates at which U.S.C. is charged. Find how much U.S.C. John pays per annum. First €12,012: 0·5%; next €10,908: 2%; next €47,124: 4%; balance: 8%.',
  ['Finds one correct amount of USC'])
A('7-c-ii','Q7(c)(ii)','5C',[16],[19],'3-3','financial-maths',
  'John gets a pay rise. He pays tax at 40% and U.S.C. at 4% on this extra income. His net salary increases by €1400 per year after tax and U.S.C. are deducted. Find his gross pay rise.',
  ['Work of merit, for example, writes 44% or 56%'])
dots='The diagram below shows the first three patterns of a sequence of patterns of dots and lines.'
A('8-a-i','Q8(a)(i)','10C',[17],[20],'4-1','sequences-series',
  'Draw pattern 4 of the sequence in the box below.',
  ['16 items: 4 lines and 12 dots','Any one item drawn','8 items correct'],stem=dots)
A('8-a-ii','Q8(a)(ii)','5C',[17],[20],'4-1','sequences-series',
  'Complete the table below showing the number of dots in each pattern. Pattern: 1, 2, 3, 4, 5. Number of dots: 1, 5, with the remaining entries left to complete.',
  ['1 correct entry','2 correct entries'],stem=dots)
A('8-a-iii','Q8(a)(iii)','5C',[17],[20,21],'4-1','sequences-series',
  'Tₙ is the number of dots in pattern n of the sequence, where n ∈ ℕ. Tₙ is given by: Tₙ = 2n² + bn + c, where b, c ∈ ℤ are constants. T₁ = 1 and T₂ = 5. Show that this means that: b + c = −1; 2b + c = −3.',
  ['Any one correct equation found'],stem=dots)
A('8-a-iv','Q8(a)(iv)','10C',[17],[21],'4-2','algebra-equations',
  'Solve these simultaneous equations to find the value of b and the value of c: b + c = −1; 2b + c = −3.',
  ['Some work of merit','Either b or c found'])
A('8-b','Q8(b)','5B',[17],[22],'4-1','sequences-series',
  'The total distance Dan has driven, in km, is shown on the dashboard of his car. The table below shows the readings on the dashboard at the start of each week for 4 weeks, where p, q ∈ ℕ. Dashboard reading (km): Week 1, 100 000; Week 2, p; Week 3, q; Week 4, 104 500. Dan drives the same total distance each week. Hence, find the value of p and the value of q.',
  ['Accept correct answers without work'])
lights='The sequence of colours and timings of a set of traffic lights is shown in the table below. This sequence repeats as the lights change during the day. Green: 13 seconds; Amber: 2 seconds; Red: 20 seconds.'
A('8-c-i','Q8(c)(i)','10C',[18],[23],'4-1','sequences-series',
  'Dan is walking along the road and notices that the lights change from amber to red. He continues to look at the lights. How long will it be, from the time the light first changes to red, until Dan sees it change to amber for the third time? Give your answer in seconds.',
  ['Total time is 103 seconds'],stem=lights)
A('8-c-ii','Q8(c)(ii)','5C',[18],[23],'4-1','sequences-series',
  'What colour will the lights be exactly 25 minutes from the time Dan notices the first change from amber to red? Show any calculations you make to arrive at your answer.',
  ['Finds 25 minutes in seconds','The light will be Green!'],stem=lights)
race='Paul O’Donovan and Fintan McCarthy are Irish rowers. They won a gold medal in the 2020 Olympic Games. The course they raced on was 2000 m in length. The following table shows their time since the start of the race as they pass various markers at set distances along the course. Their time is in seconds and the distances are measured in metres. Distance (m): 0, 500, 1000, 1500, 2000. Time (s): 0, 78·6, 182·4, 261·6, 366·43.'
A('9-a-i','Q9(a)(i)','10D',[19],[24],'5-1','graphing-functions',
  'Draw a graph of their progress in the race on the grid below. You may assume that their rate of rowing was constant in between the markers.',
  ['Note: Solution requires 6 items, 5 points plotted and joined','Apply a * if 5 items correct'],stem=race)
A('9-a-ii-iii','Q9(a)(ii),Q9(a)(iii)','10D',[19],[24,25],'5-1','graphing-functions',
  'Use your graph to answer part (a)(ii) and part (a)(iii). Show your work clearly on the graph. (ii) Estimate how much time had passed when they had travelled 750 m from the start. (iii) How far did they travel during minute 5 of the race (between 240 and 300 seconds)?',
  ['One part correct','Work of merit in both parts','Apply a * for no or incorrect units'],stem=race)
A('9-b-i-ii','Q9(b)(i),Q9(b)(ii)','10D',[19],[24,25],'3-3','number-systems',
  '(i) Paul and Fintan finished the race in a time of 366·43 seconds. Find their average speed. Give your answer, in metres per second (m/s), correct to 2 decimal places. (ii) Paul and Fintan also won gold at the 2022 world championships over the same distance (2000 m). In that race, they rowed at an average speed of 5·31 m/s. How long did it take them to finish that race? Give your answer in minutes and seconds, correct to the nearest second.',
  ['Distance Speed Time formula written','One part correct'],stem='The course they raced on was 2000 m in length.')
A('9-c-i','Q9(c)(i)','10C',[20],[26],'3-3','number-systems',
  'Two different rowers, A and B, compete in a race. As they row, their bodies burn calories. They burn calories in the ratio A : B = 10 : 11. During the race they burned a total of 53·55 calories between them. Find how many calories each rower burned during the race.',
  ['Rower A: 25·5','Rower B: 28·05'])
A('9-c-ii','Q9(c)(ii)','10C',[20],[26],'3-3','number-systems',
  'The two rowers, A and B, compete in a different race. In this race they burn calories in the ratio A : B = 1 : R, where R ∈ ℝ is a constant. At the end of the race they have burned a total of 57·5 calories between them. Rower A has burned 25 calories. Find the value of R in the ratio.',
  ['Work of merit, for example, some relevant subtraction'])
wind='Functions can be used to model wind speed as it changes over time. The function f(x) = x³ − 12x² + 36x + 10, where 0 ≤ x ≤ 8 and x ∈ ℝ, was used to model wind speed on a certain night at a particular location over an eight-hour period between midnight and 8 a.m. The wind speed was measured in km/hour and x is the time, in hours, after midnight.'
A('10-a-i-ii','Q10(a)(i),Q10(a)(ii)','20D',[21],[27],'5-1','graphing-functions',
  '(i) Complete the table, to show the values of f(x) for the given values of x. The table gives x = 0, 1, 2, 3, 4, 5, 6, 7, 8, with f(2) = 42 and f(7) = 17. (ii) Draw the graph of f(x) on the axes below for 0 ≤ x ≤ 8, where x ∈ ℝ.',
  ['Note: Solution requires 17 items, 7 values in table, 9 points plotted and joined','Apply a * if 16 items correct'],stem=wind)
A('10-b-i-ii','Q10(b)(i),Q10(b)(ii)','10D',[21],[28],'5-1','graphing-functions',
  'In the case of parts (b)(i) and (b)(ii) below, show your work on the graph. (Remember that, on the graph, 1 on the x-axis represents 1 a.m., and so on.) (i) What was the wind speed at 3 a.m.? Give your answer in km/hour. (ii) On the Beaufort Wind Scale, winds between 75 km/hour and 88 km/hour are referred to as Strong Gale Force winds. Use the graph to complete the sentence below. On that night, Strong Gale Force winds were blowing between ___ a.m. and ___ a.m.',
  ['Between 4 a.m. and 6 a.m.','One part correct'],stem='The diagram below shows the graph of a model for the wind speed, in km/hour, on a different night at the same location over the eight-hour period between midnight and 8 a.m.')
wind2='On a third night the quadratic function g(x) = −x² + 8x + 9, where 0 ≤ x ≤ 8 and x ∈ ℝ, was used to model the wind speed, in km/hour, at the same location over the eight hour period between midnight and 8 a.m.'
A('10-c-i','Q10(c)(i)','10C',[21],[29],'4-2','algebra-equations,functions',
  'Solve a quadratic equation to find the two times when the wind speed was exactly 24 km/hour, according to g(x).',
  ['Sets up g(x) = 24','Writes quadratic formula'],stem=wind2)
A('10-c-ii','Q10(c)(ii)','10D',[22],[29],'5-2','differentiation',
  'Use differentiation to find the time when the wind speed was at its maximum and find this maximum wind speed, according to g(x).',
  ['Correct differentiation','Equates derivative to zero','Solves for x','Finds the maximum value'],stem=wind2)

assert len(p.cards)==41
selection_review=[
    {'pages':[3,4,16], 'wording':'any five / any three questions', 'classification':'exam-level-selection', 'reason':'All independently marked questions remain available for practice.'},
    {'pages':[13], 'wording':'Hence, or otherwise', 'classification':'method-choice', 'reason':'Different methods solve the same required equation; there is no finite pool of tasks.'},
    {'pages':[9], 'wording':'Tick one box only', 'classification':'answer-selection', 'reason':'Positive/negative is the answer to the required graph interpretation, not a choice of prompts.'},
]
def classify(c):
    t=c['context'].lower()
    if 'questions' in t and 'any' in t: return ('exam-level-selection','Choose examination questions; retain every question for practice.')
    if 'or otherwise' in t: return ('method-choice','Alternative methods for the same equation, with no finite prompt pool.')
    return None

if __name__=='__main__': p.write(selection_review,classify)
