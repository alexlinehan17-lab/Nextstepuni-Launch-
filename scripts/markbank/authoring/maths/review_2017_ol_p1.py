"""2017 OL Paper 1: a new paper — 35 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'

ROWS = {
 'maths-2017-ol-p1-q1-a': [L(SOL, 'A = 30 000(1 − 0·15)⁵'), L(SOL, 'A = €13 311·16'), L(ALT, 'List Method\n30000\n25500\n21675\n18423·75\n15660·19\n13311·16'),
     L(LPC, '30 000 × 15% or equivalent'), L(LPC, '0·85'), L(LPC, 'at least one correct substitution'), L(LPC, 'correct formula written'),
     L(HPC, '(0·85)⁵'), L(HPC, '3 or 4 years correct by list method'), L(HPC, 'fully correct substitution into formula but fails to finish'),
     L(HPC, 'correct answer without work (13311)')],
 'maths-2017-ol-p1-q1-b': [L(SOL, 'P(1 + 0·03)² = 30 000'), L(SOL, 'P = €28 277·88'), L(ALT, 'List Method\n30000\n29126·21\n28277·88 or 28277·87'),
     L(LPC, '1·03'), L(LPC, 'at least 1 correct substitution'), L(LPC, 'correct formula written'), L(LPC, '2 unsuccessful efforts at trial and improvement'),
     L(HPC, 'correct answer without work, 28277 or 28278')],
 'maths-2017-ol-p1-q1-c': [L(SOL, '26 530·2 = 25 000(1 + i)³'), L(SOL, '1 + i = 1·02'), L(SOL, 'i = 2%'), L(LPC, '1530·20'),
     L(LPC, 'at least 1 correct substitution or correct formula written'), L(LPC, 'correct answer without work'), L(HPC, '1·02')],
 'maths-2017-ol-p1-q2-a-i': [L(SOL, '(a = 3, b = −1)'), L(PC, 'a = −1, b = 3'), L(PC, 'one correct value only')],
 'maths-2017-ol-p1-q2-a-ii': [L(SOL, 'Correct plot of −1 + 2i on diagram')],
 'maths-2017-ol-p1-q2-a-iii': [L(SOL, 'z₃ = −1 − i'), L(LPC, 'at least 1 correct substitution'), L(MPC, 'conjugate identified'),
     L(MPC, 'some multiplication above and below by the same number, even if incorrect conjugate'),
     L(HPC, 'correct multiplication using correct conjugate'), L(HPC, 'answer not in correct form')],
 'maths-2017-ol-p1-q2-b': [L(SOL, '2z − 6(4 − 6i) = (−1 + i)(4 − 2i)'), L(SOL, '2z = 22 − 30i'), L(SOL, 'z = 11 − 15i'), L(LPC, 'any correct multiplication'),
     L(HPC, 'multiplication fully correct')],
 'maths-2017-ol-p1-q3-a': [L(SOL, 'x = 2·91485 or − 0·9485'), L(SOL, 'x = 2·9 or − 0·9'), L(LPC, 'correct roots formula'),
     L(LPC, 'a, b, and c explicitly identified'), L(LPC, 'attempt at factorising'), L(MPC, 'formula fully substituted'), L(HPC, 'one correct root')],
 'maths-2017-ol-p1-q3-b': [L(SOL, 'x = 1'), L(SOL, 'y = −11'), L(LPC, 'any correct differentiation'), L(LPC, 'some work towards a graphical solution'),
     L(LPC, 'correct answer without work'), L(MPC, '6x − 6 or 6x − 6 = 0'), L(HPC, 'finds x value correctly'),
     L(NOTE, 'Accept correct turning point found graphically for full marks')],
 'maths-2017-ol-p1-q4-a': [L(SOL, '11x − 5(2x − 1) = 3(6 − x) + 3'), L(SOL, 'x = 4'), L(LPC, 'any correct multiplication'), L(LPC, 'correct answer without work'),
     L(HPC, 'multiplication fully correct'), L(HPC, 'error in expanding brackets but finishes correctly')],
 'maths-2017-ol-p1-q4-b': [L(SOL, 'y = 2x − 5'), L(SOL, 'x² + (2x − 5)² = 25'), L(SOL, '5x(x − 4) = 0'), L(SOL, 'x = 0 or x = 4'), L(SOL, 'y = −5 or y = 3'),
     L(LPC, 'isolates one variable'), L(MPC, 'substitution into quadratic'), L(HPC, 'solve (2 values) for 1 variable'),
     L(HPC, 'finds one correct couple from a quadratic'), L(NOTE, '(2x − 5)² = 4x² + 25 and continues correctly merits MPC')],
 'maths-2017-ol-p1-q5-a': [L(SOL, 'A = 145·8 m²'), L(LPC, 'correct relevant area formula with some substitution'), L(HPC, 'formula fully substituted'),
     L(HPC, 'uses Simpsons Rule and finishes correctly')],
 'maths-2017-ol-p1-q5-b': [L(SOL, '4x = 19·6'), L(SOL, 'x = 4·9'), L(LPC, 'correct relevant area formula with some substitution'),
     L(MPC, 'Formula fully substituted'), L(HPC, 'x isolated from formula'), L(HPC, 'uses Simpsons Rule and finishes correctly')],
 'maths-2017-ol-p1-q6-a': [L(SOL, '150 + 0·2(1000) + 0·3(2000)'), L(SOL, '€950 per week'), L(LPC, '1000 × 20% or equivalent'), L(LPC, '2000'),
     L(HPC, 'both commissions found, 200 and 600')],
 'maths-2017-ol-p1-q6-b': [L(SOL, '1160 − (150 + 200) = €810 at 30%'), L(SOL, '= €2700 higher sales'), L(SOL, '2700 + 1000 = €3700 total sales'),
     L(ALT, '1160 – 950 = 210\n210 = 30%\n700 = 100%\nTotal Sales = 3000 + 700 = €3700'), L(LPC, '1160 – 150'), L(LPC, '1160 – 200'), L(MPC, '810'),
     L(HPC, '2700')],
 'maths-2017-ol-p1-q7-a': [L(SOL, 'Pattern 4')],
 'maths-2017-ol-p1-q7-b': [L(SOL, '1, 5\n2, 8\n3, 11\n4, 14\n5, 17'), L(LPC, '1 or 2 correct new entries'), L(HPC, '3 correct or consistent new entries')],
 'maths-2017-ol-p1-q7-c-i': [L(SOL, 'Tn = a + (n − 1)d'), L(SOL, 'Tn = 5 + (n − 1)3'), L(SOL, 'Tn = 3n + 2'), L(ALT, 'p + q = 5'), L(ALT, '2p + q = 8'),
     L(ALT, 'p = 3 q = 2'), L(LPC, 'Tn formula written with some substitution'), L(LPC, '1 or 2 relevant equations in p & q'),
     L(LPC, 'd = 3 or a = 5 written'), L(HPC, 'Tn formula fully substituted'), L(HPC, 'value of p or value of q found'),
     L(NOTE, 'Accept 3n + 2 without work for full marks')],
 'maths-2017-ol-p1-q7-c-ii': [L(SOL, 'T20 = 62'), L(PC, 'formula with some substitution'),
     L(PC, 'listing of terms (>10) but T20 not identified or incorrectly identified'), L(NOTE, 'Accept correct answer without work')],
 'maths-2017-ol-p1-q7-c-iii': [L(SOL, '3n + 2 = 290'), L(SOL, 'n = 96'), L(PC, 'correct answer without work'), L(PC, 'equation (with formula) written'),
     L(PC, '3n + 2 on its own'), L(PC, 'finds T290 = 872, but 872 without work is zero marks')],
 'maths-2017-ol-p1-q7-d-i': [L(LPC, 'correct formula with some correct substitution'), L(LPC, 'a = 5 and/or d = 3'), L(HPC, 'formula fully substituted')],
 'maths-2017-ol-p1-q7-d-ii': [L(LPC, 'formula = 1455'), L(LPC, 'finds Sn = 30'), L(LPC, 'a = 5 and/or d = 3'),
     L(LPC, 'evidence of addition of terms in trial and improvement method'), L(HPC, 'quadratic equation formed'),
     L(HPC, 'substitutes correctly into either Sn formula')],
 'maths-2017-ol-p1-q8-a': [L(SOL, '€2000'), L(PC, 'x = 0')],
 'maths-2017-ol-p1-q8-b': [L(SOL, '275x − x² − 2000 = 8350'), L(SOL, '−x² + 275x − 10350 = 0'), L(SOL, 'x = 45, x = 230'),
     L(SOL, 'x = 230 is not possible as production limit is 200'), L(SOL, 'x = 45 km'), L(LPC, 'quadratic equation written'), L(LPC, '45 without work'),
     L(HPC, 'roots of quadratic'), L(NOTE, '45 subbed in to get 8350 is full Marks')],
 'maths-2017-ol-p1-q8-c-i': [L(SOL, '50 60 70 80 90 100'), L(SOL, '9250 10 900 12 350 13 600 14 650 15 500'), L(LPC, '1 or 2 correct new entries'),
     L(HPC, '3 or 4 correct new entries')],
 'maths-2017-ol-p1-q8-c-ii': [L(SOL, 'Graph above'), L(LPC, '1, 2 or 3 correct plots'), L(LPC, 'bar chart'), L(HPC, '4 or 5 correct plots'),
     L(HPC, '6 correct plots but not joined')],
 'maths-2017-ol-p1-q8-c-iii': [L(SOL, 'Lower 55 Upper 83'), L(SOL, '(Lines to be shown on diagram)'), L(PC, 'evidence of use of graph'),
     L(PC, 'one correct range found'), L(PC, 'correct answers without work')],
 'maths-2017-ol-p1-q8-d': [L(SOL, '2x = 170'), L(SOL, 'x = 85'), L(LPC, 'effort at calculus'), L(HPC, 'correct differentiation')],
 'maths-2017-ol-p1-q9-a': [L(SOL, 'male = 174·87 cm'), L(SOL, 'female = 172·98 cm'), L(LPC, 'substitution into either formula'),
     L(HPC, 'one relevant height found'), L(NOTE, 'Correct answer without work, award full marks')],
 'maths-2017-ol-p1-q9-b': [L(SOL, '2·3x + 65·53 = 184'), L(SOL, 'x = 51·51 cm'), L(PC, 'equation formed')],
 'maths-2017-ol-p1-q9-c': [L(SOL, '2·3(44·2) + 65·53 = 167·19'), L(SOL, '171 − 167·19 = 3·81'), L(SOL, '2·23%'), L(LPC, 'formula = 167·19'),
     L(LPC, 'correct substitution into formula'), L(LPC, 'correct answer no work'), L(MPC, 'error found, 3·81'), L(HPC, '% error formulated'),
     L(HPC, '97·77% found')],
 'maths-2017-ol-p1-q9-d': [L(SOL, '2·3x + 65·53 = 2·5x + 54·13'), L(SOL, '0·2x = 11·4'), L(SOL, 'x = 57 cm'), L(SOL, 'm(57) or f(57) = 196·63 cm'),
     L(LPC, 'Formulas equated'), L(HPC, 'transpose completed'), L(HPC, 'length of femur found ( x ) and stops')],
 'maths-2017-ol-p1-q9-e-i': [L(SOL, 'P = 17·7'), L(LPC, 'some relevant substitution into formula'), L(HPC, 'formula fully substituted')],
 'maths-2017-ol-p1-q9-e-ii': [L(SOL, 'Pℎ³ = M'), L(PC, 'some relevant transpose')],
 'maths-2017-ol-p1-q9-e-iii': [L(SOL, 'ℎ = 1·7316'), L(SOL, 'ℎ = 1·73'), L(LPC, 'some relevant substitution into formula'), L(LPC, 'correct answer without work'),
     L(HPC, 'formula fully substituted')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Every part that lost a model-solution line or a credit band to the text layer
# (a stacked fraction's lone numerator or denominator is filtered as a mark cell;
# the Q7(a) tile pattern and Q8(c)(ii) graph are images) carries the SEC's own print
# of its scheme row (model solution and every credit band), shown only after the
# reveal. Crops: scheme_row_figures.py; ids are its output.
CROPPED = ['q1-b', 'q1-c', 'q2-a-iii', 'q3-a', 'q3-b', 'q5-a', 'q5-b', 'q6-b', 'q7-a', 'q7-d-i', 'q7-d-ii', 'q8-c-ii', 'q8-d', 'q9-c',
           'q9-e-i', 'q9-e-ii', 'q9-e-iii']
SCHEME_ROW_FIGURES = {
    'maths-2017-ol-p1-q1-b': 'maths-2017-OL-scheme-p008-i0',
    'maths-2017-ol-p1-q1-c': 'maths-2017-OL-scheme-p008-i1',
    'maths-2017-ol-p1-q2-a-iii': 'maths-2017-OL-scheme-p009-i0',
    'maths-2017-ol-p1-q3-a': 'maths-2017-OL-scheme-p010-i0',
    'maths-2017-ol-p1-q3-b': 'maths-2017-OL-scheme-p010-i1',
    'maths-2017-ol-p1-q5-a': 'maths-2017-OL-scheme-p012-i0',
    'maths-2017-ol-p1-q5-b': 'maths-2017-OL-scheme-p012-i1',
    'maths-2017-ol-p1-q6-b': 'maths-2017-OL-scheme-p013-i0',
    'maths-2017-ol-p1-q7-a': 'maths-2017-OL-scheme-p014-i0',
    'maths-2017-ol-p1-q7-d-i': 'maths-2017-OL-scheme-p015-i0',
    'maths-2017-ol-p1-q7-d-ii': 'maths-2017-OL-scheme-p015-i1',
    'maths-2017-ol-p1-q8-c-ii': 'maths-2017-OL-scheme-p017-i0',
    'maths-2017-ol-p1-q8-d': 'maths-2017-OL-scheme-p017-i1',
    'maths-2017-ol-p1-q9-c': 'maths-2017-OL-scheme-p018-i0',
    'maths-2017-ol-p1-q9-e-i': 'maths-2017-OL-scheme-p019-i0',
    'maths-2017-ol-p1-q9-e-ii': 'maths-2017-OL-scheme-p019-i1',
    'maths-2017-ol-p1-q9-e-iii': 'maths-2017-OL-scheme-p019-i2',
}
assert sorted(SCHEME_ROW_FIGURES) == sorted(f'maths-2017-ol-p1-{c}' for c in CROPPED)

p = Paper(2017, 'ol', 'p1', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10B': [0, 5, 10], '10C': [0, 4, 6, 10], '10D': [0, 4, 6, 8, 10],
                             '15C': [0, 6, 10, 15], '15D': [0, 5, 7, 10, 15]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
fm = 'financial-maths'
A('1-a', 'Q1(a)', '10C', [8], [3], '3-3', fm, 'A new machine is bought for €30 000. Its value depreciates by 15% each year for five years. Find the value of the machine at the end of the five years.')
A('1-b', 'Q1(b)', '10C', [8], [3], '3-3', fm, 'A sum of money was invested for two years at 3% compound interest per year. At the end of the two years it amounted to €30 000. Find the sum invested.')
A('1-c', 'Q1(c)', '5C', [8], [3], '3-3', fm + ',indices', 'A company invested €25 000 for three years at a fixed rate of compound interest. At the end of the three years it amounted to €26 530·20. Find the rate of interest.')
z1 = 'The complex number z₁ = a + bi, where i² = −1, is shown on the Argand Diagram below.'
cx = 'complex-numbers'
A('2-a-i', 'Q2(a)(i)', '5B', [9], [4], '4-4', cx, 'Write down the value of a and the value of b.', stem=z1)
A('2-a-ii', 'Q2(a)(ii)', '5A', [9], [4], '4-4', cx, 'z₂ = −1 + 2i. Plot z₂ on the Argand Diagram.', stem=z1)
A('2-a-iii', 'Q2(a)(iii)', '10D', [9], [4], '4-4', cx, 'z₃ = z₁/z₂. Write z₃ in the form x + yi, where x, y ∈ ℝ.', stem=z1 + ' Part (a)(ii): z₂ = −1 + 2i.')
A('2-b', 'Q2(b)', '5C', [9], [5], '4-4', cx, 'Solve for z: 2z − 6(4 − 6i) = (−1 + i)(4 − 2i).')
ae = 'algebra-equations'
A('3-a', 'Q3(a)', '10D', [10], [6], '4-2', ae, 'Find the two values of x for which 3x² − 6x − 8 = 0. Give each answer correct to 1 decimal place.')
A('3-b', 'Q3(b)', '15D', [10], [6], '5-2', 'differentiation,functions', 'Find the co-ordinates of the minimum point of the function f(x) = 3x² − 6x − 8, where x ∈ ℝ.')
A('4-a', 'Q4(a)', '10C', [11], [7], '4-2', ae, 'Solve for x: 11x − 5(2x − 1) = 3(6 − x) + 3.')
A('4-b', 'Q4(b)', '15D', [11], [7], '4-2', ae, 'Solve the simultaneous equations: y + 5 = 2x; x² + y² = 25.')
av = 'area-volume'
A('5-a', 'Q5(a)', '10C', [12], [8], '3-4', av, 'A field is divided into eight sections as shown below. The width of each section is 3 metres. The height, in metres, of each section is given in the diagram. Use the Trapezoidal rule to estimate the area of the field.')
A('5-b', 'Q5(b)', '15D', [12], [8], '3-4', av + ',' + ae, 'The area of the same field was re-estimated by applying the Trapezoidal rule again. This time, a different section width (4 m) and a different set of section heights were used, as shown below. The area was found to be 145·6 m². Use this information to find the value of the height marked x on the diagram.')
sal = 'A salesman earns a basic salary of €150 per week. In addition, he gets commission of 20% on sales up to the value of €1000 in the week and 30% commission on any sales above this.'
ns = 'number-systems'
A('6-a', 'Q6(a)', '10C', [13], [9], '3-3', ns + ',' + fm, 'Find his total income for a week when his total sales amount to €3000.', stem=sal)
A('6-b', 'Q6(b)', '15D', [13], [9], '3-3', ns + ',' + fm, 'On a different week his total income is €1160. Find his total sales for this week.', stem=sal)
pt = 'The first three patterns in a sequence of patterns of tiles are shown in the diagram below.'
q7ci = 'Assuming the pattern continues, the number of tiles in the nth pattern of the sequence is given by the formula Tₙ = pn + q, where p and q ∈ ℕ. Find the value of p and the value of q.'
q7di = 'Show that Sₙ = (3n² + 7n)/2 is a formula for the total number of tiles needed to build the first n patterns.'
ss = 'sequences-series'
A('7-a', 'Q7(a)', '5A', [14], [10], '4-1', ss, 'Draw the next pattern of tiles onto the diagram above.', stem=pt)
A('7-b', 'Q7(b)', '5C', [14], [10], '4-1', ss, 'Based on the patterns shown, complete the table below. Pattern number (n): 1, 2, 3, 4, 5. Number of Tiles: 5, _, _, _, _.', stem=pt)
A('7-c-i', 'Q7(c)(i)', '10C', [14], [10], '4-1', ss, q7ci, stem=pt)
A('7-c-ii', 'Q7(c)(ii)', '5B', [15], [10, 11], '4-1', ss, 'How many tiles are in the 20th pattern?', stem=pt + ' Part (c)(i): ' + q7ci)
A('7-c-iii', 'Q7(c)(iii)', '5B', [15], [10, 11], '4-1', ss + ',' + ae, 'Find which pattern has exactly 290 tiles.', stem=pt + ' Part (c)(i): ' + q7ci)
A('7-d-i', 'Q7(d)(i)', '15C', [15], [10, 11], '4-1', ss, q7di, stem=pt)
A('7-d-ii', 'Q7(d)(ii)', '5C', [15], [10, 11], '4-1', ss, 'Find the total number of tiles needed to build the first 30 patterns.', stem=pt + ' Part (d)(i): ' + q7di)
cab = 'A company makes and sells fibre optic cable. It can sell, at most, 200 kilometres of cable in a week. For a certain range of its production the company has found that profit can be modelled using the function: P(x) = 275x − x² − 2000, where x ≤ 200. In the function, x is the number of kilometres of fibre optic cable sold and P(x) is the profit in euro.'
tab = 'The table below shows some of the data representing the profit on sales. Use the profit function, P(x), to complete the table. Number of km of cable sold (x): 50, 60, 70, 80, 90, 100. Profit (€): _, _, 12 350, _, _, _.'
q8cii = 'Use the data in the table to draw the graph of the profit function on the axes below for 50 ≤ x ≤ 100, x ∈ ℝ.'
A('8-a', 'Q8(a)', '5B', [16], [12], '5-1', 'functions', 'Use the profit function, P(x), to find how much money the company loses if it does not sell any cable.', stem=cab)
A('8-b', 'Q8(b)', '10C', [16], [12], '4-2', ae + ',functions', 'In a particular week the company made a profit of €8350. Find the number of kilometres of cable it sold that week.', stem=cab)
A('8-c-i', 'Q8(c)(i)', '10C', [16], [12], '5-1', 'functions', tab, stem=cab)
A('8-c-ii', 'Q8(c)(ii)', '5C', [17], [12, 13], '5-1', 'graphing-functions', q8cii, stem=cab + ' Part (c)(i): ' + tab)
A('8-c-iii', 'Q8(c)(iii)', '5B', [17], [12, 13], '5-1', 'graphing-functions', 'Use your graph to estimate the lower and upper range of sales (in km of cable) in order to make a profit of between €10 000 and €14 000 in a particular week. Show your work on the graph above.', stem=cab + ' Part (c)(ii): ' + q8cii)
A('8-d', 'Q8(d)', '10C', [17], [12, 13], '5-2', 'differentiation', 'Use calculus to find the number of kilometres of cable sold when the profit is increasing at a rate of €105 per km.', stem=cab)
fem = 'Forensic scientists can estimate the height of a person from the lengths of their bones. One method uses a function which relates the length of the femur bone, x, to the height of the person. Using this method the heights of males and females are estimated using the following functions: Male: m(x) = 2·3x + 65·53, where m(x) is the height and x is the length of the femur, in cm. Female: f(x) = 2·5x + 54·13, where f(x) is the height and x is the length of the femur, in cm.'
pon = 'The Ponderal Index is a number which relates a person’s height to their weight. The formula for the Ponderal Index, P, is P = M/h³ where M is weight in kg and h is height in metres.'
q9eii = 'Rearrange the formula P = M/h³ to give a formula which will give the height of a person in terms of their weight and Ponderal index.'
A('9-a', 'Q9(a)', '10C', [18], [14], '5-1', 'functions', 'Use the functions above to estimate the height of a male and the height of a female each of whose femur is 47·54 cm in length. Give both answers correct to 2 decimal places.', stem=fem)
A('9-b', 'Q9(b)', '5B', [18], [14], '4-2', ae + ',functions', 'Use m(x) to estimate the femur length of a male whose height is 184 cm. Give your answer correct to 2 decimal places.', stem=fem)
A('9-c', 'Q9(c)', '10D', [18], [14, 15], '3-3', ns, 'Conor’s femur length is 44·2 cm. His height is 171 cm. Find the percentage error in using m(x) to estimate his height. Give your answer correct to 2 decimal places.', stem=fem)
A('9-d', 'Q9(d)', '10C', [18], [14, 15], '4-2', ae + ',functions', 'Find the length of a femur for which the estimated height of a male and the estimated height of a female are the same and find this estimated height.', stem=fem)
A('9-e-i', 'Q9(e)(i)', '5C', [19], [16], '3-2', 'indices', 'Find the Ponderal Index for a person who is 1·60 m tall and weighs 72·5 kg. Give your answer correct to 1 decimal place.', stem=pon)
A('9-e-ii', 'Q9(e)(ii)', '10B', [19], [16], '4-1', 'algebra,indices', q9eii, stem=pon)
A('9-e-iii', 'Q9(e)(iii)', '5C', [19], [16], '3-2', 'indices,' + ae, 'Mary has a Ponderal Index of 13 and a weight of 67·5 kg. Find her height. Give your answer in metres, correct to 2 decimal places.', stem=pon + ' Part (e)(ii): ' + q9eii)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 50, '8': 45, '9': 55}
p.check(marks, 35)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 1–20 of the combined Ordinary Level scheme (cover, notes, contents, the Paper 1 title page 5, the scale table on page 6, the summary of mark allocations on page 7, every Paper 1 model solution and marking note on pages 8–19, and the blank page 20). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 21)), [6, 7],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 50 marks, Q8 45 marks, Q9 55 marks). Every question is retained.',
     '35 independently marked units. The printed summary on scheme page 7 labels Question 2’s units (a)(i) 5B, (a)(ii) 5A, (b) 10D, (c) 5C, but the paper prints Q2(a)(i), (a)(ii), (a)(iii) and (b), and the model-solution page 9 labels the same four scales (a)(i) 5B, (a)(ii) 5A, (a)(iii) 10D, (b) 5C; the cards follow the paper and the solution page.',
     'Paper 1 bands from the 2017 Ordinary scale table on scheme page 6: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 10B 0,5,10; 10C 0,4,6,10; 10D 0,4,6,8,10; 15C 0,6,10,15; 15D 0,5,7,10,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 35 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced, and a credit band that depends on a stacked fraction is not quoted as a fragment. List-method alternatives and the Q7(b) table are quoted as one multi-line point.',
     'Seventeen parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because a model-solution line or band was lost to the text layer or is an image: Q1(b), Q1(c), Q2(a)(iii), Q3(a), Q3(b), Q5(a), Q5(b), Q6(b), Q7(a), Q7(d)(i), Q7(d)(ii), Q8(c)(ii), Q8(d), Q9(c), Q9(e)(i), Q9(e)(ii), Q9(e)(iii).',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 10], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t else None)
p.apply(ROWS, '2017 Ordinary Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
