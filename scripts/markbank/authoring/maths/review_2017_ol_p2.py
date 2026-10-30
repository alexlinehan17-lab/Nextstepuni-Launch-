"""2017 OL Paper 2: a new paper — 41 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'
SPC = 'Special case (without work)'
MIS = 'Misreading'

ROWS = {
 'maths-2017-ol-p2-q1-a-i': [L(SOL, '65909 − 32290 = 33619'), L(PC, 'Indicates relevant subtraction.'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q1-a-ii': [L(SOL, '=0·51(51·01%)'), L(LPC, 'Either #(E) or #(S) correct. (Answer must be shown in fraction format).'),
     L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q1-b-i': [L(SOL, '(0·51)³ = 0·132651 = 0·1327'), L(SOL, '(0·51)²(0·49) = 0 ·127449 = 0·1274'), L(LPC, '0·49'),
     L(HPC, 'One correct answer.'), L(HPC, 'Substantial work in both parts.'), L(FC, 'Correct answers without work.')],
 'maths-2017-ol-p2-q1-c-i': [L(SOL, '1 – (0·14+0·15+0·18+0·15+0·12+0·1)'), L(SOL, '= 1 – 0·84'), L(SOL, '= 0·16'),
     L(PC, 'Formulates addition of some probabilities.'), L(PC, '1 ‒ (incorrect) Sum'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q1-c-ii': [L(SOL, 'Tuesday Babies = 1300 × 0·16 = 208'), L(PC, 'Probability of (Tuesday) used.'), L(PC, 'Work of merit with 1300.'),
     L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q2-a': [L(SOL, 'x² + y² = 25'), L(LPC, 'Equation of circle formula with some substitution. e.g. x² + y² =.'), L(LPC, '25 or 5².'),
     L(HPC, 'Equation of circle formula fully substituted. i.e. x² + y² = 5²')],
 'maths-2017-ol-p2-q2-b-i': [L(SOL, '16 + k² = 25'), L(SOL, 'k = 3'), L(LPC, '(‒4) or k substituted into equation of circle.'), L(HPC, '(−4)² + k² = 25.'),
     L(HPC, 'Leaves as k² = 9.'), L(HPC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q2-b-ii': [L(SOL, 'AB is the diameter of the circle so the triangle is right-angled at P'), L(ALT, 'mPA = 3'), L(ALT, 'mPA × mPB = –1'),
     L(LPC, 'Correct relevant formula with some substitution.'), L(LPC, 'AB is the diameter (but fails to draw conclusion).'),
     L(LPC, 'Demonstrates understanding of a requirement to use slopes. e.g. [m₁ × m₂ = –1]'), L(LPC, 'One correct slope, or length.'),
     L(HPC, 'Both slopes correct but no conclusion.'), L(HPC, 'Triangle ABP is right angled.'), L(ZC, 'Triangle drawn with P identified as right angled.')],
 'maths-2017-ol-p2-q2-c': [L(SOL, 'Aregion = Asemi-circle − Atriangle'), L(SOL, 'Aregion = 39·2699 − 15'), L(SOL, 'Aregion = 24·2699'), L(SOL, 'Aregion = 24·27'),
     L(LPC, 'Area of circle or semi‐circle formula with some substitution.'), L(LPC, 'Area of triangle formula with some substitution.'),
     L(LPC, 'Area = Area of semicircle ‒ Area of triangle (or equivalent).'), L(HPC, 'Both areas found.')],
 'maths-2017-ol-p2-q3-a-i': [L(SOL, '|AD| = √(1 + 4) = √5'), L(LPC, 'Correct relevant formula with some substitution.'),
     L(LPC, 'Work with Pythagoras (check candidates diagram)'), L(HPC, 'Distance formula fully substituted.'), L(HPC, 'Pythagoras’s fully substituted.'),
     L(ZC, 'Measurement from diagram (2·2).')],
 'maths-2017-ol-p2-q3-a-ii': [L(SOL, '|CD| = √(16 + 4) = √20'), L(SOL, 'Area = √20 × √5'), L(SOL, 'Area = 10'), L(LPC, 'Area = |AD| × |CD|.'),
     L(LPC, 'Correct relevant formula with some substitution.'), L(HPC, 'Area of triangles calculated.'), L(HPC, 'Area = √20 × √5.'),
     L(HPC, 'Area = 20 – (4+4+1+1).'), L(ZC, 'Measurement from diagram (2·2, 4·5).'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q3-b': [L(SOL, 'mBC = −2'), L(SOL, 'y − 3 = −2(x − 6)'), L(SOL, '2x + y − 15 = 0'), L(LPC, 'Correct relevant formula with some substitution.'),
     L(HPC, 'Eq. of line formula fully substituted.'), L(HPC, 'One incorrect substitution followed by correct solution.')],
 'maths-2017-ol-p2-q3-c': [L(SOL, 'Showing ∠ABD = 26·565 = 27°'), L(LPC, 'Any work of merit e.g. identifies ∠ABD.'),
     L(LPC, 'Work of merit with correct trigonometric ratio.'), L(LPC, 'Correct relevant formula with some substitution.'),
     L(HPC, 'Sets up a correct trigonometric ratio.'), L(HPC, 'Correct relevant formula fully substituted.'), L(MIS + ' (−1)', 'Finds |∠ADB| correctly.'),
     L(NOTE, 'Rad = 0·4636 Grad = 29·5167')],
 'maths-2017-ol-p2-q4-a': [L(LPC, 'Pilot diagram drawn.'), L(LPC, 'One correct length drawn.'), L(HPC, 'TWO correct lengths drawn.'),
     L(HPC, 'Construction correct without arcs (having checked length of sides).'), L(HPC, 'Construction correct but vertices incorrectly named or omitted.'),
     L(FC, 'Correct construction with sides or vertices labelled correctly.')],
 'maths-2017-ol-p2-q4-b-i': [L(SOL, 'Area = 2k × 2k'), L(SOL, '= 4k² cm²'), L(LPC, 'Area of square written as L × W (or similar).'),
     L(HPC, 'Correct relevant formula fully substituted.'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q4-b-ii': [L(SOL, '4k² = 20² + 20²'), L(SOL, 'k² = 200'), L(SOL, 'k = 10√2 = 14·14'), L(SOL, 'Area = 4k² − Area ∆'), L(SOL, 'Area = 600(599·7584) cm²'),
     L(LPC, 'Any use of Pythagoras’s Theorem.'), L(LPC, 'Area of Triangle Formula with some substitution.'), L(LPC, 'Formulates for area using subtraction.'),
     L(MPC, 'Value of k found.'), L(MPC, 'Area of Triangle = 200.'), L(HPC, 'Area of square and area of triangle found.'),
     L(NOTE, 'Accept correct rounding of answers.')],
 'maths-2017-ol-p2-q5-a-i': [L(SOL, '55 70 Given 100 115 130 145'), L(LPC, 'One correct new entry.'), L(LPC, 'Writes x̅ = 100 or σ = 15.'),
     L(LPC, 'Writes x̅ , σ, 2σ or 3σ on axis correctly.'), L(HPC, 'Four correct new entries.')],
 'maths-2017-ol-p2-q5-a-ii': [L(SOL, '0·68 × 1200 = 816'), L(LPC, 'Shows some understanding of the Empirical Rule.'), L(LPC, 'Work of merit with 1200.'),
     L(HPC, 'One correct answer. [e.g. p = 0·95(95%)]'), L(HPC, 'Error in the use of the Empirical Rule. [e.g. (a)(ii) 68% and (a)(iii) 95% of 1200 = 1140]'),
     L(HPC, 'Substantial work in both parts.')],
 'maths-2017-ol-p2-q5-b': [L(PC, 'Any relevant work towards creating at least one correct probability.'), L(PC, 'Answer as 10 + 5.'), L(ZC, 'Answer as 15.'),
     L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q6-a': [L(SOL, 'x = 8·84 cm'), L(LPC, 'Any work of merit. [e.g. Third Angle = 52°]'), L(LPC, 'Sine rule with some substitution.'),
     L(MPC, 'Finds the length of the base side. (10·17)'), L(HPC, 'Full correct substitution without calculation.'),
     L(HPC, 'Incorrect calculator mode but otherwise correct. (once only)'), L(HPC, 'Correct answer without work.'),
     L(NOTE, 'Rad = 58·95392809 Grad = 8·721730163')],
 'maths-2017-ol-p2-q6-b': [L(SOL, 'y² = 8·5² + 10·2² − 2(8·5)(10·2) cos 53·8'), L(SOL, 'y² = 73·87897723'), L(SOL, 'y = 8·595288083'), L(SOL, 'y = 8·60 cm'),
     L(LPC, 'Writes Cosine Rule correctly with some substitution.'), L(MPC, 'Two variables correctly substituted into correct relevant formula.'),
     L(MPC, 'y² = 73·878977 without work and stops.'), L(HPC, 'Fully correct substitution.'),
     L(HPC, 'One incorrect substitution followed by correct calculation.'), L(HPC, 'Incorrect calculator mode but otherwise correct. (once only)'),
     L(HPC, 'Correct answer without work.'), L(ZC, 'Treating triangle as right‐angled.'), L(NOTE, 'Rad = 18·34 Grad = 7·82')],
 'maths-2017-ol-p2-q7-a-i': [L(SOL, 'ℎ = 2r'), L(SOL, '= 2(2·25)'), L(SOL, '= 4·5 m'), L(PC, 'Correct relationship identified.'), L(PC, '2·25 ÷ 2'),
     L(PC, 'ℎ = d drawn on a diagram.'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q7-a-ii': [L(SOL, 'l² = h² + r²'), L(SOL, 'l² = (4·5)² + (2·25)²'), L(SOL, 'l² = 25·3125'), L(SOL, 'l = √25·3125 = 5·03'),
     L(LPC, 'Some use of Pythagoras.'), L(LPC, 'Work of merit. [e.g. Work with 2·25 / 4·5].'), L(MPC, 'Uses (5·03) to give: (5·03)² = (4·5)² + (2·25)²'),
     L(HPC, 'Pythagoras fully substituted.'), L(HPC, 'Finishes with only one error.'), L(HPC, 'Stops at √25·3125')],
 'maths-2017-ol-p2-q7-b-i': [L(SOL, 'CSA = 14 × πrl'), L(SOL, '= 14 × π (2·25)(5·03)'), L(SOL, '= 497·77 m²'),
     L(LPC, 'CSA formula written with some correct substitution.'), L(LPC, 'Work of merit. [ e.g. Use of 2·25/5·03].'),
     L(LPC, 'Indicates multiplication by 14.'), L(HPC, 'Fully correct substitution.'), L(HPC, 'Finishes with only one error.'),
     L(HPC, 'CSA of one cone calculated (35·55).')],
 'maths-2017-ol-p2-q7-b-ii': [L(SOL, '= 41'), L(PC, 'Works with answer to (b) (i).'), L(PC, 'Works with 12·25.')],
 'maths-2017-ol-p2-q7-b-iii': [L(SOL, 'Cost = 9 × 110'), L(SOL, '= A$ 990'), L(SOL, '= 990 × €0·68'), L(SOL, '= €673·20'), L(SOL, '= €673'),
     L(MPC, 'Finds correct number of containers. (without work)'), L(HPC, 'Finds A$990 or consistent equivalent.'), L(HPC, 'Finishes with only one error.')],
 'maths-2017-ol-p2-q7-c-i': [L(SOL, '= 2π (2·25)'), L(SOL, '= 14·14 m'), L(SOL, 'θ = 161°'),
     L(LPC, 'Correct relevant formula written with some correct substitution.'), L(LPC, 'Identifies r = 2·25 or CSA = (35·55).'),
     L(LPC, 'Correct use of 360°'), L(HPC, 'One correct.'), L(HPC, 'Substantial work in both parts.')],
 'maths-2017-ol-p2-q8-a': [L(SOL, 'A = (1, −2) B = (4, 2)'), L(SOL, 'D = (6, −6) E = (15, 6)'), L(LPC, 'ONE correct point.'), L(HPC, 'THREE correct points.'),
     L(HPC, 'All answers written consistently as (y, x)')],
 'maths-2017-ol-p2-q8-b': [L(SOL, 'Conclusion: Parallel, or slopes are the same.'), L(LPC, 'Any mention of same slopes or similar.'),
     L(LPC, 'Slope formula written with some relevant substitution.'), L(LPC, 'Rise over Run (Written or indicated).'),
     L(MPC, 'Slope formula fully substituted for one slope.'), L(MPC, 'One correct slope.'), L(HPC, 'Both slopes but no conclusion.'),
     L(HPC, 'One error in substitution followed by correct calculation and consistent conclusion.'), L(FC, 'Equal slopes and conclusion.')],
 'maths-2017-ol-p2-q8-c-i': [L(SOL, 'A = (1, −2) B = (4, 2) C = (4·5, 0)'), L(SOL, 'A = (0, 0) B = (3, 4) C = (3·5, 2)'),
     L(LPC, 'Correct relevant formula with some correct/consistent substitution.'), L(LPC, 'One point translated to (0, 0).'),
     L(HPC, 'Error in translation and area calculated correctly.'),
     L(HPC, 'No translation but uses TWO of the points A, B, C and area calculated correctly.'),
     L(HPC, 'One error in substitution followed by correct calculation.')],
 'maths-2017-ol-p2-q8-c-ii': [L(SOL, '|AB| = √(3² + 4²) = 5 units'), L(LPC, 'Correct relevant formula with some substitution.'),
     L(LPC, 'Any work of merit indicated in this part.'), L(HPC, 'Correct substitution without calculation.'),
     L(HPC, 'One error in substitution followed by correct calculation.'), L(HPC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q8-c-iii': [L(PC, 'Use of answer to part (c)(ii).'), L(PC, 'Scale factor formula written or indicated.'),
     L(PC, 'Attempts to calculate |AB| in this part.'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q8-c-iv': [L(SOL, 'Area = 4 × 3² = 36 units²'), L(LPC, 'Work of merit with answer from (c)(iii).'),
     L(LPC, 'Work of merit with answer from (c)(i).'), L(HPC, 'Area as 3 × 4 = 12 or equivalent.'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q9-a-i': [L(SOL, '33 577 342 − 33 551 983 = 25 359 invalid votes'), L(ALT, 'Total ‒ (leave + remain) = 25 359'),
     L(PC, 'Relevant addition or subtraction indicated.'), L(FC, 'Correct answer without work.'),
     L(NOTE, 'If Correct answer not written in Table 1 Award F.*')],
 'maths-2017-ol-p2-q9-a-ii': [L(SOL, '= 52(%)'), L(LPC, 'Any correct element in relevant fraction.'),
     L(HPC, 'Ignores or mishandles % calculation. [e.g. = 0·52% or 0·5189%].'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q9-b-i': [L(SOL, 'Charts above:'), L(LPC, 'Effort to draw a chart. [e.g. One data point displayed correctly]'),
     L(HPC, 'One fully correct chart.'), L(HPC, 'Two substantial charts shown. [e.g. Three or more data elements illustrated with scales and axes]')],
 'maths-2017-ol-p2-q9-b-ii': [L(SOL, 'Remain mean = 52·33%'), L(SOL, 'Leave mean = 47·67%'), L(LPC, 'Indicates some relevant addition.'),
     L(LPC, 'Relevant formula with some correct substitution.'), L(HPC, 'One mean correct.'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q9-b-iii': [L(SOL, 'The number of voters in each age group is not used in the calculation of the mean in (b)(ii). The mean is based on percentage data of voters in each age group and is therefore unreliable.'),
     L(PC, 'The number of voters in each age group is not used.'), L(PC, 'The mean values calculated in (b)(ii) are based on percentage data.')],
 'maths-2017-ol-p2-q9-c-i': [L(SOL, '= 2·88675%'), L(SOL, '= 3%'), L(LPC, 'Sets up work as √1200'), L(FC, 'Correct answer without work.')],
 'maths-2017-ol-p2-q9-c-ii': [L(SOL, '48 − 3 < p < 48 + 3'), L(SOL, '45 < p < 51'), L(LPC, 'Work of merit with margin of error from (c)(i).'),
     L(HPC, 'One boundary formed (48+3 or 48–3)'), L(HPC, 'Correct answer without work.'), L(HPC, 'Use of version of formula from HL.')],
 'maths-2017-ol-p2-q9-c-iii': [L(SOL, 'H0 = p = 53%'), L(SOL, 'H1 = p ≠ 53%'), L(SOL, '53% is not within the C. I. at (c)(ii)'), L(SOL, '45·17 < p < 51·17'),
     L(SOL, 'Reject H0, Party claim is false'), L(LPC, 'Null hypothesis stated.'), L(LPC, 'C. I. written.'),
     L(HPC, 'Conclusion OK but not given in the context of the question. (Reject null hypothesis but no mention of party claim).')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Every part that lost a model-solution line or a credit band to the text layer
# (stacked fractions filtered as mark cells, mangled bold maths) or whose model
# solution is an image (the Q4(a) construction, the Q5(a) Empirical Rule figure,
# the Q9(b)(i) chart, the Q3(a)(ii) diagram) carries the SEC's own print of its
# scheme row (model solution and every credit band), shown only after the reveal.
# Crops: scheme_row_figures.py; ids are its output.
CROPPED = ['q1-a-ii', 'q1-b-i', 'q1-c-i', 'q2-b-ii', 'q2-c', 'q3-a-ii', 'q3-b', 'q3-c', 'q4-a', 'q4-b-ii', 'q5-a-ii', 'q5-b', 'q6-a',
           'q7-b-ii', 'q7-b-iii', 'q7-c-i', 'q8-b', 'q8-c-i', 'q8-c-iii', 'q9-a-ii', 'q9-b-i', 'q9-b-ii', 'q9-c-i', 'q9-c-ii']
SCHEME_ROW_FIGURES = {
    'maths-2017-ol-p2-q1-a-ii': 'maths-2017-OL-scheme-p024-i0',
    'maths-2017-ol-p2-q1-b-i': 'maths-2017-OL-scheme-p025-i0',
    'maths-2017-ol-p2-q1-c-i': 'maths-2017-OL-scheme-p025-i1',
    'maths-2017-ol-p2-q2-b-ii': 'maths-2017-OL-scheme-p026-i0',
    'maths-2017-ol-p2-q2-c': 'maths-2017-OL-scheme-p027-i0',
    'maths-2017-ol-p2-q3-a-ii': 'maths-2017-OL-scheme-p028-i0',
    'maths-2017-ol-p2-q3-b': 'maths-2017-OL-scheme-p028-i1',
    'maths-2017-ol-p2-q3-c': 'maths-2017-OL-scheme-p029-i0',
    'maths-2017-ol-p2-q4-a': 'maths-2017-OL-scheme-p030-i0',
    'maths-2017-ol-p2-q4-b-ii': 'maths-2017-OL-scheme-p031-i0',
    'maths-2017-ol-p2-q5-a-ii': 'maths-2017-OL-scheme-p032-i0',
    'maths-2017-ol-p2-q5-b': 'maths-2017-OL-scheme-p032-i1',
    'maths-2017-ol-p2-q6-a': 'maths-2017-OL-scheme-p033-i0',
    'maths-2017-ol-p2-q7-b-ii': 'maths-2017-OL-scheme-p035-i0',
    'maths-2017-ol-p2-q7-b-iii': 'maths-2017-OL-scheme-p035-i1',
    'maths-2017-ol-p2-q7-c-i': 'maths-2017-OL-scheme-p035-i2',
    'maths-2017-ol-p2-q8-b': 'maths-2017-OL-scheme-p036-i0',
    'maths-2017-ol-p2-q8-c-i': 'maths-2017-OL-scheme-p036-i1',
    'maths-2017-ol-p2-q8-c-iii': 'maths-2017-OL-scheme-p037-i0',
    'maths-2017-ol-p2-q9-a-ii': 'maths-2017-OL-scheme-p038-i0',
    'maths-2017-ol-p2-q9-b-i': 'maths-2017-OL-scheme-p039-i0',
    'maths-2017-ol-p2-q9-b-ii': 'maths-2017-OL-scheme-p040-i0',
    'maths-2017-ol-p2-q9-c-i': 'maths-2017-OL-scheme-p041-i0',
    'maths-2017-ol-p2-q9-c-ii': 'maths-2017-OL-scheme-p041-i1',
}
assert sorted(SCHEME_ROW_FIGURES) == sorted(f'maths-2017-ol-p2-{c}' for c in CROPPED)

p = Paper(2017, 'ol', 'p2', {'5A': [0, 5], '5B': [0, 3, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 3, 7, 10],
                             '10D': [0, 4, 5, 7, 10], '15C': [0, 7, 10, 15], '15D': [0, 5, 7, 9, 15]},
          'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
cso = 'According to the Central Statistics Office (CSO) there were 65 909 babies born in Ireland in 2015. Of these 32 290 were girls.'
q1aii = 'Find the probability that a baby picked at random from those born in Ireland in 2015 is a boy. Give your answer correct to 2 decimal places.'
pr = 'probability'
A('1-a-i', 'Q1(a)(i)', '5B', [24], [3], '1-2', pr, 'How many boys were born in Ireland in 2015?', stem=cso)
A('1-a-ii', 'Q1(a)(ii)', '5C', [24], [3], '1-2', pr, q1aii, stem=cso)
A('1-b-i', 'Q1(b)(i),Q1(b)(ii)', '5C', [25], [3], '1-2', pr, 'Eight babies were born in Limerick’s Maternity Hospital on 1 May 2015. (i) Use your answer to part (a)(ii) to find the probability that the first three babies born were boys. Give your answer correct to 4 decimal places. (ii) Find the probability that the third birth was the first girl born in the hospital that day. Give your answer correct to 4 decimal places.',
  stem=cso + ' Part (a)(ii): ' + q1aii)
dow = 'The table below shows the probability of being born on a particular day of the week.'
tab = 'Day: Mon, Tue, Wed, Thu, Fri, Sat, Sun. Probability: 0·14, _, 0·15, 0·18, 0·15, 0·12, 0·1.'
A('1-c-i', 'Q1(c)(i)', '5B', [25], [3], '1-2', pr, 'Complete the table. ' + tab, stem=dow)
A('1-c-ii', 'Q1(c)(ii)', '5B', [25], [3], '1-2', pr, 'In a particular week 1300 babies were born. Find the number of babies expected to be born on the Tuesday of that week.', stem=dow + ' ' + tab + ' Part (c)(i): Complete the table.')
cc = 'co-ordinate-geometry-the-circle'
semi = 'The circle c has centre (0, 0) and radius 5 units. Part (b): The diagram shows a semi-circle which is part of c. Diagram labels: A(−5, 0), B(5, 0), P(−4, k).'
q2bi = 'The point P(−4, k), k > 0, is on the semi-circle. Find the value of k.'
A('2-a', 'Q2(a)', '5C', [26], [4], '2-2', cc, 'The circle c has centre (0, 0) and radius 5 units. Write down the equation of c.')
A('2-b-i', 'Q2(b)(i)', '5C', [26], [4], '2-2', cc, q2bi, stem=semi)
A('2-b-ii', 'Q2(b)(ii)', '5C', [26], [4], '2-2', cc + ',co-ordinate-geometry-of-the-line', 'Show that the triangle ABP is right-angled at P.', stem=semi + ' Part (b)(i): ' + q2bi)
A('2-c', 'Q2(c)', '10C', [27], [4, 5], '3-4', 'area-volume', 'Find the area of the region which is inside the semi-circle but outside the triangle ABP. Give your answer, in square units, correct to 2 decimal places.', stem=semi + ' Part (b)(i): ' + q2bi)
rect = 'The points A(2, 1), B(6, 3), C(5, 5), and D(1, 3) are the vertices of the rectangle ABCD as shown.'
cl = 'co-ordinate-geometry-of-the-line'
A('3-a-i', 'Q3(a)(i)', '5C', [28], [6], '2-2', cl, 'Show that |AD| = √5 units.', stem=rect)
A('3-a-ii', 'Q3(a)(ii)', '5C', [28], [6], '2-2', cl + ',area-volume', 'Find, in square units, the area of the rectangle ABCD.', stem=rect + ' Part (a)(i): Show that |AD| = √5 units.')
A('3-b', 'Q3(b)', '10C', [28], [6], '2-2', cl, 'Find the equation of the line BC. Give your answer in the form ax + by + c = 0, where a, b, and c ∈ ℤ.', stem=rect)
A('3-c', 'Q3(c)', '5C', [29], [6, 7], '2-3', 'trigonometry', 'Use trigonometry to find the measure of the angle ABD. Give your answer correct to the nearest degree.', stem=rect)
A('4-a', 'Q4(a)', '10C', [30], [8], '2-1', 'geometry-proofs-and-constructions', 'Construct the triangle ABC, where |AB| = 8 cm, |AC| = 5 cm, and |BC| = 7 cm.')
sq = 'The diagram shows a square of side length 2k cm.'
A('4-b-i', 'Q4(b)(i)', '5C', [30], [8], '3-4', 'area-volume,algebra', 'Write down, in terms of k, an expression for the area of the square.', stem=sq)
A('4-b-ii', 'Q4(b)(ii)', '10D', [31], [8, 9], '3-4', 'area-volume,trigonometry', 'An isosceles triangle with side lengths of 20 cm and hypotenuse of length 2k cm is removed from the square, as shown. Find the value of k (correct to 2 decimal places) and the area of the remaining (shaded) section.', stem=sq + ' Part (b)(i): Write down, in terms of k, an expression for the area of the square.')
iq = 'In a survey, the IQ scores of 1200 people were recorded. The mean score was 100 points and the standard deviation was 15 points. Assuming that IQ scores are normally distributed, the data are shown on the diagram below.'
st = 'statistics'
A('5-a-i', 'Q5(a)(i)', '15C', [32], [10], '1-6', st, 'Fill in the missing numbers on the horizontal axis. Boxes: _, _, 85, _, _, _, _.', stem=iq)
A('5-a-ii', 'Q5(a)(ii),Q5(a)(iii)', '5C', [32], [10], '1-7', st + ',' + pr, '(ii) A person is chosen at random from those surveyed. Use the Empirical Rule to find the probability that this person has an IQ score between 70 and 130 points. (iii) Use the Empirical Rule to find the approximate number of people surveyed with an IQ score of between 85 and 115 points.', stem=iq)
A('5-b', 'Q5(b)', '5B', [32], [10], '1-2', pr, 'A class of 24 pupils is made up of 10 boys and 14 girls. Chemistry is studied by 6 of the boys and 9 of the girls. A pupil is chosen at random from the class. Find the probability that the pupil chosen is a boy or is a pupil who does not study chemistry.')
tg = 'trigonometry'
A('6-a', 'Q6(a)', '10D', [33], [11], '2-3', tg, 'Find the distance x in the diagram below (not to scale). Give your answer correct to 2 decimal places. Diagram labels: 65°, x, 10 cm, 63°.')
A('6-b', 'Q6(b)', '15D', [33], [11], '2-3', tg, 'Find the distance y in the diagram below (not to scale). Give your answer correct to 2 decimal places. Diagram labels: 8·5 cm, y, 53·8°, 10·2 cm.')
cones = 'Cones is a sculpture in the National Gallery of Australia. It consists of 14 identical steel cones arranged into pairs which are joined together as shown.'
pol = cones + ' Part (b): In order to maintain the steel’s reflective shine, the surface is polished regularly.'
q7bi = 'Find the curved surface area of the entire sculpture (14 cones). Give your answer correct to 2 decimal places.'
q7bii = 'One litre of polish will cover 12·25 m². Find how many litres are needed to polish the entire sculpture. Give your answer correct to the nearest litre.'
av = 'area-volume'
q7ai = 'The height of each cone is equal to the diameter of its base. If the radius of the base is 2·25 m, write the height of a cone.'
q7aii = 'Show that, correct to 2 decimal places, the slant height, l, of a cone is 5·03 m.'
A('7-a-i', 'Q7(a)(i)', '10B', [34], [12], '3-4', av, q7ai, stem=cones)
A('7-a-ii', 'Q7(a)(ii)', '5D', [34], [12], '3-4', av + ',' + tg, q7aii, stem=cones + ' Part (a)(i): ' + q7ai)
A('7-b-i', 'Q7(b)(i)', '10C', [34], [12], '3-4', av, q7bi, stem=pol + ' Part (a)(i): ' + q7ai + ' Part (a)(ii): ' + q7aii)
A('7-b-ii', 'Q7(b)(ii)', '10B', [35], [12, 13], '3-4', av + ',number-systems', q7bii, stem=pol + ' Part (b)(i): ' + q7bi)
A('7-b-iii', 'Q7(b)(iii)', '10D', [35], [12, 13], '3-3', 'number-systems,financial-maths', 'A container of polish contains 5 litres and costs A$110. Find the number of containers of polish that must be purchased in order to polish the entire sculpture and hence find the cost of the polish in euro ( A$1 = €0·68 ). Give your answer correct to the nearest euro.', stem=pol + ' Part (b)(ii): ' + q7bii)
A('7-c-i', 'Q7(c)(i),Q7(c)(ii)', '10C', [35], [12, 13], '3-4', av, 'The diagram (not to scale) shows the net of the outer surface of one of the cones of the sculpture. It is a sector of a circle of radius length 5·03 m with arc length p m and angle θ at the centre, as shown below. (i) Find p, the length of the arc of the sector. Give your answer correct to 2 decimal places. (ii) Find θ, the angle at the centre of the sector. Show all your working out. Give your answer correct to the nearest degree.', stem=cones + ' Part (a)(i): ' + q7ai + ' Part (a)(ii): ' + q7aii)
tri = 'The diagram below shows the triangles CBA and CDE. The coordinates of C are (4·5, 0).'
q8a = 'From the diagram, write down the coordinates of the points A, B, D, and E.'
q8cii = 'Find |AB|, the distance from A to B.'
q8ciii = 'The triangle CDE is an enlargement of the triangle CBA. Given that |DE| = 15 units, find the scale factor of the enlargement.'
A('8-a', 'Q8(a)', '10C', [36], [14], '2-2', cl, q8a, stem=tri)
A('8-b', 'Q8(b)', '10D', [36], [14], '2-2', cl, 'Show, using slopes, that the line segments [AB] and [DE] are parallel.', stem=tri + ' Part (a): ' + q8a)
A('8-c-i', 'Q8(c)(i)', '5C', [36], [14, 15], '2-2', cl, 'Show that the area of the triangle CBA is 4 square units.', stem=tri + ' Part (a): ' + q8a)
A('8-c-ii', 'Q8(c)(ii)', '5C', [37], [14, 15], '2-2', cl, q8cii, stem=tri + ' Part (a): ' + q8a)
A('8-c-iii', 'Q8(c)(iii)', '5B', [37], [14, 15], '2-1', 'geometry', q8ciii, stem=tri + ' Part (c)(ii): ' + q8cii)
A('8-c-iv', 'Q8(c)(iv)', '5C', [37], [14, 15], '2-1', 'geometry', 'Use this scale factor to find the area of the triangle CDE.', stem=tri + ' Part (c)(i): Show that the area of the triangle CBA is 4 square units. Part (c)(iii): ' + q8ciii)
ref = 'In June 2016 the UK held a referendum on its membership of the EU. Table 1 below summarises the results. Table 1, United Kingdom EU Membership Referendum 2016, Votes: Leave the EU 17 410 742; Remain a member of the EU 16 141 241; Valid votes 33 551 983; Invalid or blank votes _; Total votes 33 577 342. Source: The UK Electoral Commission.'
t2 = ' Part (b): Table 2 shows the percentages of “Remain” and “Leave” voters in various age groups of those who voted in the referendum. Table 2, Age Group, Remain (%), Leave (%): 18 ‒ 24, 73, 27; 25 ‒ 34, 62, 38; 35 ‒ 44, 52, 48; 45 ‒ 54, 44, 56; 55 ‒ 64, 43, 57; 65+, 40, 60.'
q9bii = 'Find the mean of the “Remain” values given in Table 2 and find the mean of the “Leave” values given in Table 2. Give your answers as percentages, correct to 2 decimal places.'
irl = 'In the days following the UK referendum, a survey was conducted in Ireland on attitudes towards a British exit from the European Union.'
q9ci = '1200 people were surveyed. Find the margin of error of this survey. Write your answer as a percentage. Give your answer correct to the nearest percent.'
q9cii = 'In the Irish survey 578 of the 1200 surveyed agreed that a UK exit would have a negative effect on the Irish economy. Use your answer to part c(i) above to create a 95% confidence interval for the proportion of the Irish population who agreed that a UK exit would have a negative effect on the Irish economy.'
A('9-a-i', 'Q9(a)(i)', '5B', [38], [16], '3-3', 'number-systems', 'Write the number of Invalid or blank votes into the table.', stem=ref)
A('9-a-ii', 'Q9(a)(ii)', '5C', [38], [16], '3-3', 'number-systems', 'Write the number who voted to leave the EU as a percentage of the valid votes. Give your answer correct to the nearest percent.', stem=ref)
A('9-b-i', 'Q9(b)(i)', '15C', [39], [16, 17], '1-6', st, 'Draw a suitable chart or charts to represent the data in Table 2.', stem=ref + t2)
A('9-b-ii', 'Q9(b)(ii)', '10C', [40], [16, 17], '1-6', st, q9bii, stem=ref + t2)
A('9-b-iii', 'Q9(b)(iii)', '5B', [40], [16, 17], '1-7', st, 'Explain why the answers to part b(ii) do not accurately reflect the actual outcome of the referendum.', stem=ref + t2 + ' Part (b)(ii): ' + q9bii)
A('9-c-i', 'Q9(c)(i)', '5C', [41], [18], '1-7', st, q9ci, stem=irl)
A('9-c-ii', 'Q9(c)(ii)', '5C', [41], [18], '1-7', st, q9cii, stem=irl + ' Part (c)(i): ' + q9ci)
A('9-c-iii', 'Q9(c)(iii)', '5C', [41], [18], '1-7', st, 'After the survey, a political party claimed that 53% of the Irish population believed that the decision of the UK to leave the EU would have a negative effect on the Irish economy. Use your answer to part c(ii) above to conduct a hypothesis test, at the 5% level of significance, to test the party’s claim. Give your conclusion in the context of the question.', stem=irl + ' Part (c)(ii): ' + q9cii)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 40, '9': 55}
p.check(marks, 41)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 21–44 of the combined Ordinary Level scheme (the Paper 2 title page 21, the scale table on page 22, the summary of mark allocations on page 23, every Paper 2 model solution and marking note on pages 24–41, the Irish-language bonus-marks page 42 and the back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(21, 45)), [22, 23],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 40 marks, Q9 55 marks). Every question is retained.',
     '41 independently marked units, matching the printed summary of allocations on scheme page 23. Q1(b)(i)+(ii), Q5(a)(ii)+(iii) and Q7(c)(i)+(ii) each share one printed scale and are one task.',
     'Paper 2 bands from the 2017 Ordinary scale table on scheme page 22, which differ from Paper 1’s: 5A 0,5; 5B 0,3,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,4,5,7,10; 15C 0,7,10,15; 15D 0,5,7,9,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 41 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced, and a line or band that depends on a stacked fraction or mangled bold maths is not quoted as a fragment. The Q2(b), Q6(a) and Q6(b) prompts list the printed diagram labels; the diagrams themselves are in the question paper.',
     'Twenty-four parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal: every part that lost a model-solution line or a credit band to the text layer, and the image-only model solutions (the Q3(a)(ii) diagram, the Q4(a) construction, the Q5(a) Empirical Rule figure and the Q9(b)(i) chart).',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 12], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [13], 'wording': 'the net of the outer surface of one of the cones', 'classification': 'mathematical-context',
      'reason': 'All fourteen cones are identical; “one of the cones” names the object measured in one required task, not a choice between printed prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('mathematical-context', 'All fourteen cones are identical; “one of the cones” names the object measured in one required task, not a choice between printed prompts.') if 'one of the cones' in t else None)
p.apply(ROWS, '2017 Ordinary Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
