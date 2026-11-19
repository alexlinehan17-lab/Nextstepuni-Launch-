"""2017 HL Paper 2: a new paper — 37 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'
M2, M3 = 'Method 2, ', 'Method 3, '

ROWS = {
 'maths-2017-hl-p2-q1-a': [L(SOL, '= 0·0032768')],
 'maths-2017-hl-p2-q1-b': [L(SOL, 'or 0·016384')],
 'maths-2017-hl-p2-q1-c': [L(SOL, '1 − (4/5)^n'), L(PC, 'any correct term from the expansion')],
 'maths-2017-hl-p2-q1-d': [L(SOL, '1 − (4/5)^n > 0·99'), L(SOL, '(4/5)^n < 0·01'), L(SOL, '≈ 0·01000000517'), L(SOL, 'n = 21'),
     L(LPC, 'Ans (c) > 0·99'), L(HPC, 'viable solution to inequality'), L(HPC, 'n = 20·6377 and stops')],
 'maths-2017-hl-p2-q2-a': [L(SOL, 'Correlation coefficient = −0·957')],
 'maths-2017-hl-p2-q2-b': [L(SOL, 'Plots'), L(SOL, 'Line of Best Fit on Graph'), L(LPC, '3 correct plots'),
     L(HPC, 'All plots correct with an incorrect line of best fit'), L(HPC, 'All plots correct and no line of best fit')],
 'maths-2017-hl-p2-q2-c': [L(SOL, 'As speed increases by 1 km/h the average distance travelled on 1 litre of fuel decreases by 0·15km'),
     L(ALT, 'The rate at which fuel consumption in km/l is decreasing as the speed in km/h increases'),
     L(PC, 'Some reference to speed and fuel consumption'), L(PC, 'Reference to rate of change')],
 'maths-2017-hl-p2-q2-d-i': [L(SOL, '= 23·21'), L(SOL, '= 23 to nearest minute'), L(HPC, 'Answer in hours')],
 'maths-2017-hl-p2-q2-d-ii': [L(SOL, '= €6·98'), L(LPC, 'Amount of Mary’s fuel or amount of Jane’s fuel')],
 'maths-2017-hl-p2-q3-a': [L(SOL, 'P = (1 , −1)'), L(ALT, 'P = (x, y)'), L(ALT, 'x = 1, y = −1'), L(ALT, '= (1, −1)'),
     L(LPC, 'Ratio formula with some substitution'),
     L(HPC, 'one relevant co-ordinate of P found')],
 'maths-2017-hl-p2-q3-b': [L(SOL, 'C(4, 2) → P(1, −1 ) → B(1 − 3, −1 − 3)'), L(SOL, '= (−2, −4 )'), L(SOL, 'x = −2, y = −4'), L(SOL, 'B = (−2 , −4)'),
     L(LPC, 'P as mid-point of BC'), L(HPC, 'one relevant co-ordinate of B found'), L(NOTE, 'Accept (‒2, ‒4) without work'),
     L(NOTE, 'Accept correct graphical solution')],
 'maths-2017-hl-p2-q3-c': [L(SOL, 'AC ⊥ BC'), L(SOL, '−1 × 1 = −1'), L(SOL, 'lines are perpendicular'), L(ALT, 'Slope AB = 5.'),
     L(ALT, '→ x + 5y = 14 …. (i).'), L(ALT, 'Slope AC = −1.'), L(ALT, 'Altitude from B : y + 4 = 1(x + 2)'), L(ALT, '→ x − y = 2 …… (ii)'),
     L(ALT, '→ Solving (i)and (ii) x = 4 y = 2'), L(LPC, 'Identifies significance of right-angled triangle'),
     L(LPC, 'one equation of perpendicular from vertex to opposite side found'),
     L(HPC, 'slope of AC and slope of BC found but no conclusion'), L(HPC, 'two equations of perpendiculars from vertex to opposite side found')],
 'maths-2017-hl-p2-q4-a': [L(SOL, 'x² + y² + 2gx + 2fy + c = 0'), L(SOL, '(0, 0) ⇒ 0+0+0+0+c = 0 ⇒ c = 0\n(6·5, 0) ⇒ 42·25+0+13g+0+0=0 ⇒ g = −3·25'),
     L(SOL, '14f = −84\nf = −6\nx² + y² − 6·5x − 12y = 0'),
     L('Method 1, ' + LPC, 'c = 0'), L('Method 1, ' + LPC, 'One relevant equation in g and/or f'), L('Method 1, ' + MPC, '2 of g, f, c found'),
     L('Method 1, ' + HPC, 'g , f, and c found or equivalent'), L(M2 + LPC, 'Effort at formulating equation of 1 ⊥ bisector'),
     L(M2 + MPC, 'Point t of intersection of 2 ⊥ bisectors found'), L(M2 + HPC, 'Point of intersection of 2 ⊥ bisectors and radius'),
     L(M3 + LPC, 'c = 0'), L(M3 + LPC, 'One point substituted into equation of circle'), L(M3 + LPC, 'Midpoint (0,0) and (6·5, 0) formulated'),
     L(M3 + MPC, '2 of g, f, c found'), L(M3 + HPC, 'g , f, and c found or equivalent')],
 'maths-2017-hl-p2-q4-b': [L(SOL, 'θ = 28·44'), L(ALT, 'Cosine rule |AB|² = 42·25,'), L(ALT, '|AC|² = 149'), L(ALT, '|BC|² =61·25'), L(ALT, '⇒ θ = 28·44'),
     L(LPC, 'one relevant slope'), L(HPC, 'tan θ fully substituted'), L(M2 + LPC, 'one relevant length'), L(M2 + HPC, 'cos θ fully substituted')],
 'maths-2017-hl-p2-q5-a': [L(SOL, 'Proof:'), L(SOL, '|< AEF| = |< AED| … rigℎt angles'), L(SOL, '|< FAE| + |< EAD| = 90o'),
     L(SOL, '|< EAD| + |< ADE| = 90o remaining angles in ∆AED'), L(SOL, '∴ |< FAE| = |< ADE|'), L(SOL, '∴ |< AFE| = |< DAE|'),
     L(SOL, '∴ ∆AFE and ∆DAE equiangular ∴ similar'), L(LPC, 'Identifies one angle of same size in each triangle'),
     L(HPC, 'Identifies second angle of same size in each triangle'), L(HPC, 'Implies triangles are similar without justifying |< FAE| = |< ADE|')],
 'maths-2017-hl-p2-q5-b': [L(SOL, '|AD| = 31·2 cm'), L(LPC, '|AF| = 13'), L(LPC, 'One set of corresponding sides identified')],
 'maths-2017-hl-p2-q5-c': [L(SOL, '|AB| = 3 × 12 = 36 cm'), L(LPC, '|AG| = 39'), L(LPC, 'One set of corresponding sides identified')],
 'maths-2017-hl-p2-q5-d': [L(SOL, 'Area = AreaABCD ‒ Area∆AFD −∆AreaABG + Area∆AFE'), L(SOL, '= 680·4 cm²'),
     L(ALT, 'or (method 2) Area = AreaABCD ‒ Area∆ABG ‒ Area∆AED'), L(ALT, '= 1123·2 − 270 − 172·8'),
     L(ALT, 'or (method 3) Area = Area∆DCG + Area∆GED'), L(ALT, '= 291·6 + 388·8'), L(LPC, 'One relevant area formulated'),
     L(LPC, 'Relevant equation for area GCDE'), L(HPC, 'Relevant individual areas found but fails to finish'),
     L(HPC, 'Area calculated but with one relevant area omitted (except method 3)')],
 'maths-2017-hl-p2-q6-a': [L(SOL, '|AJ| = 6371 + 0·214'), L(SOL, '|JH|² = |AJ|² − |AH|²'), L(SOL, '|JH| = √((6371 + 0·214)² − 6371²)'), L(SOL, '= 52·21 = 52'),
     L(LPC, '|AJ| formulated'), L(LPC, 'indication of Pythagoras'), L(HPC, 'Pythagoras fully substituted')],
 'maths-2017-hl-p2-q6-b': [L(SOL, 'rS1 = 6371 × cos 53 = 3834·1635'), L(SOL, 'lS1 = 2πrS1 = 2π(3834·1635) = 24091'), L(LPC, 'cos 53° or sin 47°'),
     L(HPC, 'radius of s₁ calculated and stops'), L(HPC, 'length of circle formula fully substituted')],
 'maths-2017-hl-p2-q7-a': [L(SOL, 'Vol of space = Cylinder ‒ 2×Cone'), L(LPC, 'A relevant volume formulated'),
     L(HPC, 'Vol of space formulated in terms of π and R')],
 'maths-2017-hl-p2-q7-b-i': [L(SOL, '12² = 6² + |AB|²'), L(SOL, '|AB| = √(12² − 6²) = √108 = 6√3'), L(PC, 'indication of Pythagoras')],
 'maths-2017-hl-p2-q7-b-ii': [L(SOL, 'r = 6 cm'), L(LPC, 'indication of similar triangles'), L(LPC, 'indication of a relevant ratio'),
     L(HPC, 'corresponding ratios identified but fails to finish'), L(NOTE, 'Accept correct answer without work')],
 'maths-2017-hl-p2-q7-b-iii': [L(SOL, 'Cylinder = π12² − π6² = 108π'), L(SOL, 'Sphere = π(6√3)² = 108π'), L(LPC, 'Surface Area in Fig. 3 substituted'),
     L(LPC, 'Surface Area in Fig 4 substituted'), L(HPC, 'One Surface Area found')],
 'maths-2017-hl-p2-q7-c': [L(SOL, 'Vol = π(12²)(6)'), L(SOL, 'Vol = 360π cm³'), L(LPC, 'Vol of cylinder found'), L(LPC, 'Vol of truncated cone substituted'),
     L(LPC, 'Vol of one cone found (12 or 6)'), L(HPC, 'Volume fully substituted but fails to finish'), L(HPC, 'Volume of truncated cone found')],
 'maths-2017-hl-p2-q8-a-i': [L(SOL, 'μ = 63·5 σ = 10'), L(SOL, 'P(z > −1·35) = P(z < 1·35)'), L(SOL, '= 0·9115'), L(SOL, '91·15%'), L(LPC, 'μ or σ identified'),
     L(MPC, 'z found'), L(HPC, 'P(z < 1·35)and stops')],
 'maths-2017-hl-p2-q8-a-ii': [L(SOL, 'P(x > Z) = 0·015'), L(SOL, 'P(x < Z) = 0·985'), L(SOL, 'Z = 2·17'), L(SOL, 'x = 85·2 kg'), L(LPC, 'identifies 0·985'),
     L(MPC, 'identifies 2·17'), L(HPC, 'formula for x fully substituted')],
 'maths-2017-hl-p2-q8-a-iii': [L(SOL, 'n = 150, x̅ = 62, s = 10 kg'), L(SOL, 'Ho → mean weight has not changed'), L(SOL, 'H1 → mean weight has changed'),
     L(SOL, '= −1·8371 > −1·96'), L(SOL, 'Mean weight has not changed'), L(ALT, '62 ± 1·96(0·8165)'), L(ALT, '62 ± 1·6003'), L(ALT, '[60·3997, 63·6003]'),
     L(ALT, '63·5 falls within this interval ∴ insufficient evidence to reject the null hypothesis The mean weight has not changed'),
     L(LPC, 'z formulated with some substitution'), L(LPC, 'states null/alternative hypothesis only'), L(LPC, 'reference to ±1·96'),
     L(MPC, 'z fully substituted'), L(HPC, 'z = −1·8371 > −1·96'), L(HPC, 'fails to contextualise the answer')],
 'maths-2017-hl-p2-q8-b-i': [L(LPC, '3 boxes filled correctly'), L(HPC, '10 boxes filled correctly')],
 'maths-2017-hl-p2-q8-b-ii': [L(SOL, 'or 0·2125'), L(LPC, '2 relevant fractions transferred'), L(HPC, '4 relevant fractions identified but fails to complete')],
 'maths-2017-hl-p2-q8-b-iii': [L(SOL, 'or 0·5490'), L(LPC, 'P(L)'), L(LPC, 'P(R ∩ L)'), L(HPC, 'Formula fully substituted')],
 'maths-2017-hl-p2-q9-a': [L(SOL, '√3|CT| = |TE|'), L(PC, 'tan 60°'), L(PC, 'effort to express |TE| in terms of another side of the triangle')],
 'maths-2017-hl-p2-q9-b': [L(LPC, 'tan 30°'), L(LPC, 'Use of Pythagoras for |DT|'), L(LPC, 'Effort at expressing |DT | in terms of another side of ∆DET')],
 'maths-2017-hl-p2-q9-c': [L(SOL, '= 5·3033 m'), L(SOL, '= 5·3 m'), L(LPC, 'equates both expressions'), L(HPC, 'Isolate |CT| in equation')],
 'maths-2017-hl-p2-q9-d': [L(SOL, '|TE| = √3|CT| = 9·17986 m = 9·2 m'), L(LPC, 'Substitution into formula for |TE|')],
 'maths-2017-hl-p2-q9-e': [L(SOL, 'θ = 54·7'), L(LPC, 'Some relevant substitution for cos θ'), L(HPC, 'Formula for cos θ substituted in terms of |CT|')],
 'maths-2017-hl-p2-q9-f': [L(SOL, '= 0·3038'), L(SOL, '= 30·4'), L(LPC, '(Answer to part (e))×2'), L(LPC, '360°'), L(HPC, 'P fully formulated')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# This scheme sets most of its working as stacked fractions, binomial coefficients and
# diagrams, which the text layer cannot carry (a lone numerator or denominator is
# filtered as a mark cell). Every part that lost a model-solution line or a credit
# band to that carries the SEC's own print of its scheme row (model solution and
# every credit band), shown only after the reveal; the parts that lost nothing
# (Q2(a), Q2(c), Q5(a), Q6(a), Q7(b)(i), Q7(b)(iii), Q9(d)) do not.
# Crops: scheme_row_figures.py; ids are its output.
CROPPED = ['q1-a', 'q1-b', 'q1-c', 'q1-d', 'q2-b', 'q2-d-i', 'q2-d-ii', 'q3-a', 'q3-b', 'q3-c', 'q4-a', 'q4-b', 'q5-b', 'q5-c', 'q5-d',
           'q6-b', 'q7-a', 'q7-b-ii', 'q7-c', 'q8-a-i', 'q8-a-ii', 'q8-a-iii', 'q8-b-i', 'q8-b-ii', 'q8-b-iii', 'q9-a', 'q9-b', 'q9-c',
           'q9-e', 'q9-f']

SCHEME_ROW_FIGURES = {
    'maths-2017-hl-p2-q1-a': 'maths-2017-HL-scheme-p028-i0',
    'maths-2017-hl-p2-q1-b': 'maths-2017-HL-scheme-p028-i1',
    'maths-2017-hl-p2-q1-c': 'maths-2017-HL-scheme-p029-i0',
    'maths-2017-hl-p2-q1-d': 'maths-2017-HL-scheme-p029-i1',
    'maths-2017-hl-p2-q2-b': 'maths-2017-HL-scheme-p030-i0',
    'maths-2017-hl-p2-q2-d-i': 'maths-2017-HL-scheme-p030-i1',
    'maths-2017-hl-p2-q2-d-ii': 'maths-2017-HL-scheme-p030-i2',
    'maths-2017-hl-p2-q3-a': 'maths-2017-HL-scheme-p031-i0',
    'maths-2017-hl-p2-q3-b': 'maths-2017-HL-scheme-p031-i1',
    'maths-2017-hl-p2-q3-c': 'maths-2017-HL-scheme-p032-i0',
    'maths-2017-hl-p2-q4-a': 'maths-2017-HL-scheme-p033-i0',
    'maths-2017-hl-p2-q4-b': 'maths-2017-HL-scheme-p034-i0',
    'maths-2017-hl-p2-q5-b': 'maths-2017-HL-scheme-p035-i0',
    'maths-2017-hl-p2-q5-c': 'maths-2017-HL-scheme-p035-i1',
    'maths-2017-hl-p2-q5-d': 'maths-2017-HL-scheme-p036-i0',
    'maths-2017-hl-p2-q6-b': 'maths-2017-HL-scheme-p037-i0',
    'maths-2017-hl-p2-q7-a': 'maths-2017-HL-scheme-p038-i0',
    'maths-2017-hl-p2-q7-b-ii': 'maths-2017-HL-scheme-p038-i1',
    'maths-2017-hl-p2-q7-c': 'maths-2017-HL-scheme-p038-i2',
    'maths-2017-hl-p2-q8-a-i': 'maths-2017-HL-scheme-p039-i0',
    'maths-2017-hl-p2-q8-a-ii': 'maths-2017-HL-scheme-p039-i1',
    'maths-2017-hl-p2-q8-a-iii': 'maths-2017-HL-scheme-p039-i2',
    'maths-2017-hl-p2-q8-b-i': 'maths-2017-HL-scheme-p040-i0',
    'maths-2017-hl-p2-q8-b-ii': 'maths-2017-HL-scheme-p041-i0',
    'maths-2017-hl-p2-q8-b-iii': 'maths-2017-HL-scheme-p041-i1',
    'maths-2017-hl-p2-q9-a': 'maths-2017-HL-scheme-p042-i0',
    'maths-2017-hl-p2-q9-b': 'maths-2017-HL-scheme-p042-i1',
    'maths-2017-hl-p2-q9-c': 'maths-2017-HL-scheme-p042-i2',
    'maths-2017-hl-p2-q9-e': 'maths-2017-HL-scheme-p043-i0',
    'maths-2017-hl-p2-q9-f': 'maths-2017-HL-scheme-p043-i1',
}
assert sorted(SCHEME_ROW_FIGURES) == sorted(f'maths-2017-hl-p2-{c}' for c in CROPPED)

p = Paper(2017, 'hl', 'p2', {'5A': [0, 5], '5B': [0, 3, 5], '5C': [0, 2, 4, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 4, 5, 10],
                             '10D': [0, 3, 5, 8, 10], '15C': [0, 6, 9, 15], '15D': [0, 5, 7, 9, 15]},
          'LC003ALP200EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
ph = 'When Conor rings Ciara’s house, the probability that Ciara answers the phone is 1/5.'
pr = 'probability'
A('1-a', 'Q1(a)', '10C', [28], [3], '1-3', pr, 'Conor rings Ciara’s house once every day for 7 consecutive days. Find the probability that she will answer the phone on the 2nd, 4th, and 6th days but not on the other days.', stem=ph)
A('1-b', 'Q1(b)', '5D', [28], [3], '1-3', pr, 'Find the probability that she will answer the phone for the 4th time on the 7th day.', stem=ph + ' Part (a): Conor rings Ciara’s house once every day for 7 consecutive days.')
q1c = 'Conor rings her house once every day for n days. Write, in terms of n, the probability that Ciara will answer the phone at least once.'
A('1-c', 'Q1(c)', '5B', [29], [3], '1-3', pr, q1c, stem=ph)
A('1-d', 'Q1(d)', '5C', [29], [3], '1-3', pr + ',indices-and-logs', 'Find the minimum value of n for which the probability that Ciara will answer the phone at least once is greater than 99%.', stem=ph + ' Part (c): ' + q1c)
fuel = 'An experiment measures the fuel consumption at various speeds for a particular model of car. The data collected are shown in Table 1 below. Table 1: Speed (km/hour): 40, 48, 56, 64, 88, 96, 112. Fuel consumption (km/litre): 21, 16, 18, 16, 13, 11, 9.'
jr = fuel + ' Part (d): Mary drove from Cork to Dublin at an average speed of 96 km/h. Jane drove the same journey at an average speed of 112 km/h. Each travelled 260 km and paid 132·9 cents per litre for the fuel. Both used the model of car used to generate the data in Table 1.'
ds = 'statistics-descriptive-statistics'
A('2-a', 'Q2(a)', '5A', [30], [4], '1-6', ds, 'Find the correlation coefficient of the data in Table 1, correct to 3 decimal places.', stem=fuel)
A('2-b', 'Q2(b)', '5C', [30], [4], '1-6', ds, 'Plot the points from the table on the grid below and draw the line of best fit (by eye).', stem=fuel)
A('2-c', 'Q2(c)', '5B', [30], [4], '1-7', ds, 'The slope of the line of best fit is found to be −0·15. What does this value represent in the context of the data?', stem=fuel)
A('2-d-i', 'Q2(d)(i)', '5C', [30], [5], '3-3', ds, 'Find how much longer it took Mary to complete the journey. Give your answer correct to the nearest minute.', stem=jr)
A('2-d-ii', 'Q2(d)(ii)', '5C', [30], [5], '1-7', ds, 'Based on the data in Table 1 and their average speeds, find how much more Jane spent on fuel during the course of this journey.', stem=jr)
abc = 'ABC is a triangle where the co-ordinates of A and C are (0, 6) and (4, 2) respectively. G(2/3, 4/3) is the centroid of the triangle ABC. AG intersects BC at the point P. |AG| : |GP| = 2 : 1.'
cl = 'co-ordinate-geometry-of-the-line'
A('3-a', 'Q3(a)', '10C', [31], [6], '2-2', cl, 'Find the co-ordinates of P.', stem=abc)
A('3-b', 'Q3(b)', '5C', [31], [6], '2-2', cl, 'Find the co-ordinates of B.', stem=abc + ' Part (a): Find the co-ordinates of P.')
A('3-c', 'Q3(c)', '10C', [32], [6], '2-2', cl + ',geometry', 'Prove that C is the orthocentre of the triangle ABC.', stem=abc + ' Part (b): Find the co-ordinates of B.')
circ = 'A(0, 0), B(6·5, 0) and C(10, 7) are three points on a circle.'
A('4-a', 'Q4(a)', '10D', [33], [7], '2-2', 'co-ordinate-geometry-of-the-circle', 'Find the equation of the circle.', stem=circ)
A('4-b', 'Q4(b)', '15C', [34], [7], '2-3', 'trigonometry-triangles,' + cl, 'Find |∠BCA|. Give your answer in degrees, correct to 2 decimal places.', stem=circ)
rect = 'ABCD is a rectangle. F ∈ [AB], G ∈ [BC], [FD] ∩ [AG] = {E}, and FD ⊥ AG. |AE| = 12 cm, |EG| = 27 cm, and |FE| = 5 cm.'
q5a = 'Prove that ∆AFE and ∆DAE are similar (equiangular).'
q5c = '∆AFE and ∆AGB are similar. Show that |AB| = 36 cm.'
geo = 'geometry'
A('5-a', 'Q5(a)', '10C', [35], [8], '2-1', geo + ',geometry-constructions-proofs', q5a, stem=rect)
A('5-b', 'Q5(b)', '5C', [35], [8], '2-1', geo, 'Find |AD|.', stem=rect + ' Part (a): ' + q5a)
A('5-c', 'Q5(c)', '5C', [35], [8], '2-1', geo, q5c, stem=rect)
A('5-d', 'Q5(d)', '5C', [36], [8], '3-4', 'area-volume,' + geo, 'Find the area of the quadrilateral GCDE.', stem=rect + ' Part (b): Find |AD|. Part (c): ' + q5c)
A('6-a', 'Q6(a)', '15C', [37], [9], '2-1', geo + ',trigonometry-triangles', 'Take the earth as a sphere with radius 6371 km. Jack is standing on the Cliffs of Moher at the point J which is 214 metres above sea level. He is looking out to sea at a point H on the horizon. Taking A as the centre of the earth, find |JH|, the distance from Jack to the horizon. Give your answer correct to the nearest km.')
A('6-b', 'Q6(b)', '10C', [37], [9], '2-3', 'trigonometry-triangles', 'The Cliffs of Moher, at point C, are at latitude 53° north of the equator. On the diagram, s₁ represents the circle that is at latitude 53°. s₂ represents the equator (which is at latitude 0°). A is the centre of the earth. s₁ and s₂ are on parallel planes. Find the length of the circle s₁. Give your answer correct to the nearest km.', stem='Take the earth as a sphere with radius 6371 km.')
cones = 'Two solid cones, each of radius R cm and height R cm are welded together at their vertices and placed in the smallest possible hollow cylinder, as shown in Figure 1 below.'
wat = cones + ' Part (b): In the remainder of this question, R = 12 cm. Water is poured into both the cylinder and the sphere to a depth of 6 cm as shown below (Figure 3 and Figure 4 respectively).'
q7bi = 'Find |AB|, the radius of the circular surface of the water in the sphere (Figure 4). Give your answer in the form a√b cm, where a, b ∈ ℕ.'
q7bii = 'Find |CD|, the radius of the cone at water level, as shown in Figure 3.'
av = 'area-volume'
A('7-a', 'Q7(a)', '10C', [38], [10], '3-4', av, 'Show that the capacity (volume) of the empty space in the cylinder is equal to the capacity of an empty sphere of radius R cm (Figure 2).', stem=cones)
A('7-b-i', 'Q7(b)(i)', '10B', [38], [10, 11], '3-4', av + ',trigonometry-triangles', q7bi, stem=wat)
A('7-b-ii', 'Q7(b)(ii)', '10C', [38], [10, 11], '3-4', av + ',geometry', q7bii, stem=wat)
A('7-b-iii', 'Q7(b)(iii)', '5C', [38], [10, 11], '3-4', av, 'Verify that the area of the surface of the water in the sphere is equal to the area of the surface of the water in the cylinder.', stem=wat + ' Part (b)(i): ' + q7bi + ' Part (b)(ii): ' + q7bii)
A('7-c', 'Q7(c)', '5C', [38], [10, 11, 12], '3-4', av, 'The mathematician Cavalieri discovered that, at the same depth, the volume of water in the available space in the cylinder is equal to the volume of water in the sphere. Use this discovery to find the volume of water in the sphere when the depth is 6 cm. Give your answer in terms of π.', stem=wat)
wt = 'In 2015, in a particular country, the weights of 15 year olds were normally distributed with a mean of 63·5 kg and a standard deviation of 10 kg.'
zs = 'statistics-z-scores'
A('8-a-i', 'Q8(a)(i)', '10D', [39], [12], '1-7', zs, 'In 2015, Mariska was a 15 year old in that country. Her weight was 50 kg. Find the percentage of 15 year olds in that country who weighed more than Mariska.', stem=wt)
A('8-a-ii', 'Q8(a)(ii)', '5D', [39], [12, 13], '1-7', zs, 'In 2015, Kamal was a 15 year old in that country. 1·5% of 15 year olds in that country were heavier than Kamal. Find Kamal’s weight.', stem=wt)
A('8-a-iii', 'Q8(a)(iii)', '15D', [39], [12, 13], '1-7', 'statistics-inferential-statistics,' + zs, 'In 2016, 150 of the 15 year olds in that country were randomly selected and their weights recorded. It was found that their weights were normally distributed with a mean weight of 62 kg and a standard deviation of 10 kg. Test the hypothesis, at the 5% level of significance, that the mean weight of 15 year olds, in that country, had not changed from 2015 to 2016. State the null hypothesis and your alternative hypothesis. Give your conclusion in the context of the question.', stem=wt)
gal = 'In Galway, rain falls in the morning on 1/3 of the school days in the year. When it is raining the probability of heavy traffic is 1/2. When it is not raining the probability of heavy traffic is 1/4. When it is raining and there is heavy traffic, the probability of being late for school is 1/2. When it is not raining and there is no heavy traffic, the probability of being late for school is 1/8. In any other situation the probability of being late for school is 1/5. Some of this information is shown in the tree diagram below.'
q8bi = 'Write the probability associated with each branch of the tree diagram and the probability of each outcome into the blank boxes provided. Give each answer in the form a/b, where a, b ∈ ℕ.'
q8bii = 'On a random school day in Galway, find the probability of being late for school.'
A('8-b-i', 'Q8(b)(i)', '15C', [40], [14], '1-2', pr, q8bi, stem=gal)
A('8-b-ii', 'Q8(b)(ii)', '10C', [41], [14, 15], '1-2', pr, q8bii, stem=gal + ' Part (b)(i): ' + q8bi)
A('8-b-iii', 'Q8(b)(iii)', '5C', [41], [14, 15], '1-2', pr, 'On a random school day in Galway, find the probability that it rained in the morning, given that you were late for school.', stem=gal + ' Part (b)(ii): ' + q8bii)
tree = 'Conor’s property is bounded by the straight bank of a river, as shown in Figure 1 above. T is the base of a vertical tree that is growing near the opposite bank of the river. |TE| is the height of the tree, as shown in Figure 2 above. From the point C, which is due west of the tree, the angle of elevation of E, the top of the tree, is 60°. From the point D, which is 15 m due north of C, the angle of elevation of E is 30° (see Figure 2). The land on both sides of the river is flat and at the same level.'
q9a = 'Use triangle ECT, to express |TE| in the form √a|CT| metres, where a ∈ ℕ.'
q9b = 'Show that |TE| may also be expressed as √((225 + |CT|²)/3) metres.'
q9c = 'Hence find |CT|, the distance from the base of the tree to the bank of the river at Conor’s side. Give your answer correct to 1 decimal place.'
q9e = 'The tree falls across the river and hits the bank at Conor’s side at the point F. Find the maximum size of the angle FTC. Give your answer in degrees, correct to 1 decimal place.'
tt = 'trigonometry-triangles'
A('9-a', 'Q9(a)', '10B', [42], [16], '2-3', tt, q9a, stem=tree)
A('9-b', 'Q9(b)', '5C', [42], [16], '2-3', tt, q9b, stem=tree)
A('9-c', 'Q9(c)', '10C', [42], [16, 17], '2-3', tt + ',algebra-solving-equations', q9c, stem=tree + ' Part (a): ' + q9a + ' Part (b): ' + q9b)
A('9-d', 'Q9(d)', '10B', [43], [16, 17], '2-3', tt, 'Find |TE|, the height of the tree. Give your answer correct to 1 decimal place.', stem=tree + ' Part (a): ' + q9a + ' Part (c): ' + q9c)
A('9-e', 'Q9(e)', '5C', [43], [16, 17], '2-3', tt, q9e, stem=tree)
A('9-f', 'Q9(f)', '10C', [43], [16, 17], '1-2', pr + ',' + tt, 'If the tree was equally likely to fall in any direction, find the probability that it would hit the bank at Conor’s side, when it falls. Give your answer as a percentage, correct to 1 decimal place.', stem=tree + ' Part (e): ' + q9e)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 40, '8': 60, '9': 50}
p.check(marks, 37)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 25–48 of the combined Higher Level scheme (the Paper 2 title page 25, the scale table on page 26, the summary of mark allocations on page 27, every Paper 2 model solution and marking note on pages 28–43, the Irish-language bonus-marks page 44 and the remaining back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(25, 49)), [26, 27],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 40 marks, Q8 60 marks, Q9 50 marks). Every question is retained.',
     '37 independently marked units, matching the printed summary of allocations on scheme page 27.',
     'Paper 2 bands from the 2017 scale table on scheme page 26 (headed “Paper 1” in print, but it is the Paper 2 table and its ladders differ from Paper 1’s): 5A 0,5; 5B 0,3,5; 5C 0,2,4,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,4,5,10; 10D 0,3,5,8,10; 15C 0,6,9,15; 15D 0,5,7,9,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 37 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; Q4(a) keeps each printed method’s ladder separately. The scheme sets most of its working as stacked fractions, binomial coefficients and diagrams the text layer cannot carry, and a credit band that depends on one is not quoted as a fragment.',
     'Thirty parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal: every part that lost a model-solution line or a credit band to the text layer, including the Q2(b) graph and the Q8(b)(i) tree diagram. Q2(a), Q2(c), Q5(a), Q6(a), Q7(b)(i), Q7(b)(iii) and Q9(d) are quoted in full.',
     'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 10], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t else None)
p.apply(ROWS, '2017 Higher Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
