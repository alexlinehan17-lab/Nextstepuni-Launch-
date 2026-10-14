"""2016 HL Paper 2: a new paper — 34 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'

ROWS = {
 'maths-2016-hl-p2-q1-a': [L(SOL, 'Slope AC = −2/3'), L(SOL, 'perp. slope = 3/2'), L(SOL, 'y − 3 = 3/2 (x − 5)'), L(SOL, '3x − 2y = 9'),
     L(LPC, 'slope formula with some relevant substitution'), L(LPC, '3 = 5m+c'), L(LPC, 'y − y1 = m(x − x1) with x1 or y1 or both substituted'),
     L(HPC, 'perpendicular slope'), L(HPC, 'equation of line through B parallel to AC')],
 'maths-2016-hl-p2-q1-b': [L(SOL, 'Slope AB = (3 + 2)/(5 − 6) = −5/1'), L(SOL, 'perp. slope = 1/5'), L(SOL, 'y − 4 = 1/5(x + 3)'), L(SOL, 'x − 5y + 23 = 0'),
     L(SOL, 'Orthocentre: 3x − 2y = 9 ⋂ x − 5y = −23'), L(SOL, '(7, 6)'), L(ALT, 'Equation: 8x − y = 50'),
     L(LPC, 'demonstration of understanding of orthocentre ( e.g. mentions altitude)'), L(LPC, 'slope formula with some relevant substitution'),
     L(LPC, 'altitude from part (a)'), L(MPC, 'equation of an altitude other than (a)'),
     L(MPC, 'some relevant substitution towards finding a second altitude and altitude from (a)'), L(MPC, 'correct construction'),
     L(HPC, 'two correct altitudes'), L(HPC, 'correct construction with orthocentre (7, 6)')],
 'maths-2016-hl-p2-q2-a': [L(SOL, 'y − 6 = 1/7 (x + 1)'), L(SOL, 'x − 7y + 43 = 0'), L(LPC, 'equation of line formula with some relevant substitution'),
     L(HPC, 'equation of line not in required form')],
 'maths-2016-hl-p2-q2-b': [L(SOL, 'D = |ax1 + by1 + c|/√(a² + b²)'), L(SOL, '−3g − 4f − 21 = ±25'), L(SOL, '⟹ 3g + 4f = −46 … (i)'), L(SOL, 'and 3g + 4f = 4 … (ii)'),
     L(SOL, 'But (−g, −f) ∈ x − 7y + 43 = 0'), L(SOL, '−g + 7f + 43 = 0 ... (iii)'), L(SOL, 'f = −7 and g = −6'), L(SOL, 'Centre (6, 7)'),
     L(SOL, '(x − 6)² + (y − 7)² = 25'), L(ALT, 'f = −5 and g = 8'), L(ALT, '(x + 8)² + (y − 5)² = 25'),
     L(LPC, 'some correct substitution into relevant formula (line, circle, perpendicular distance).'),
     L(MPC, 'one relevant equation in g and f ( either(i) or (ii) or (iii))'), L(HPC, 'two relevant equations ( either (i) and (iii) or (ii) and (iii))')],
 'maths-2016-hl-p2-q3-a': [L(SOL, '= (2 cos 4A cos 3A)/(2 cos 4A sin 3A)'), L(SOL, '= cos 3A/sin 3A'), L(SOL, '= cot 3A'),
     L(LPC, 'sum to product formula with some substitution'), L(HPC, 'sum to product formula fully substituted')],
 'maths-2016-hl-p2-q3-b': [L(SOL + ', Method 1', 'cos²θ = 1/2 (1 + cos 2θ)'), L(SOL + ', Method 1', 'cos θ = ± √5/3'),
     L(SOL + ', Method 3', '9 − 9 tan²θ = 1 + tan²θ'),
     L(LPC, 'Use of a relevant formula in cos2θ'), L(LPC, 'cos⁻¹(1/9) = 83·62°'), L(LPC, 'θ = 41·8°'),
     L(MPC, 'correct substitution (method 1)'), L(MPC, 'expression in sin²θ (method 2)'), L(MPC, 'expression in tan²θ (method 3)'),
     L(MPC, 'expression in cos²θ (method 4)'), L(MPC, 'θ = 41·8° and θ = 132·2° or θ = 221·8°'),
     L(HPC, 'one value only'), L(HPC, 'values found for cos 41·8° and cos 138·2° or cos 221·8°')],
 'maths-2016-hl-p2-q4-a-i': [L(SOL, '|∠ABD| = |∠CBD| = 90°…….(i)'), L(SOL, '|∠BDC| + |∠BCD| = 90° …angles in triangle sum to 180°'),
     L(SOL, '|∠ADB| + |∠BDC| = 90° …. angle in semicircle'), L(SOL, '|∠ADB| + |∠BDC| = |∠BDC| + |∠BCD|'), L(SOL, '|∠ADB| = |∠BCD|……..(ii)'),
     L(SOL, '∴ Triangles are equiangular (or similar)'), L(LPC, 'identifies one angle of same size in each triangle'),
     L(HPC, 'identifies second angle of same size in each triangle'),
     L(HPC, 'implies triangles are similar without justifying (ii) in model solution or equivalent')],
 'maths-2016-hl-p2-q4-a-ii': [L(SOL, '⟹ y² = x'), L(SOL, 'y = √x'), L(ALT, '|AD|² + |DC|² = |AC|²'), L(ALT, '|AD| = √(x² + y²)'), L(ALT, '|DC| = √(y² + 1)'),
     L(ALT, 'x² + y² + y² + 1 = (x + 1)²'), L(ALT, '2y² = 2x'), L(LPC, 'one set of corresponding sides identified'),
     L(LPC, 'indicates relevant use of Pythagoras'), L(HPC, 'corresponding sides fully substituted'), L(HPC, 'expression in y² or y⁴, i.e. fails to finish')],
 'maths-2016-hl-p2-q4-b': [L(LPC, 'perpendicular line drawn at U or T'), L(LPC, 'relevant use of 1 cm length'),
     L(LPC, 'mid point of incorrect extended segment constructed'), L(HPC, 'correct mid-point constructed')],
 'maths-2016-hl-p2-q5-a-i': [L(PC, '1 correct column')],
 'maths-2016-hl-p2-q5-a-ii': [L(SOL, 'P(win) = (1/5 × 1/6 × 3/4) + (1/5 × 5/6 × 1/4) + (4/5 × 1/6 × 1/4) + (1/5 × 1/6 × 1/4)'), L(SOL, '= 13/120'),
     L(LPC, 'one correct triple (numerical or descriptive)'), L(LPC, 'probability of any one Miss'), L(HPC, '4 correct triples (numerical)')],
 'maths-2016-hl-p2-q5-b': [L(SOL, 'P(A∩B) = P(A) × P(B)'), L(SOL, '0·1 = (x + 0·1) × 0·4'), L(SOL, '0·4x = 0·06'), L(SOL, 'x = 0·15'),
     L(ALT, 'P(A|B) = P(A)'), L(ALT, '0·1/0·4 = x + 0·1'), L(LPC, 'formula written or implied'), L(LPC, 'writes P(A) = x + 0·1'),
     L(HPC, 'formula fully substituted')],
 'maths-2016-hl-p2-q6-a': [L(SOL, 'P(M, 3, 3) = 1/26 × 1/10 × 1/10 = 1/2600'), L(LPC, 'any correct relevant probability'),
     L(HPC, 'correct probabilities but not expressed as single fraction or equivalent'), L(NOTE, 'Accept correct answer without supporting work')],
 'maths-2016-hl-p2-q6-b': [L(SOL, '∑x. P(x) = 5950/2600 = 2·29'), L(SOL, 'Club loses 29 cent per play'), L(LPC, '1 correct entry to table'),
     L(HPC, 'all entries correct but fails to finish or finishes incorrectly'), L(HPC, 'no conclusion')],
 'maths-2016-hl-p2-q6-c': [L(SOL, 'Profit = Revenue – Pay-out'), L(SOL, '600 = 845(x − 2·29)'), L(SOL, 'x = (600 + 845(2∙29))/845'), L(SOL, 'x = 3'),
     L(ALT, '600/845 = 0∙71'), L(ALT, '0·71 + 2·29 = 3'), L(LPC, 'links profit, revenue and payout'), L(HPC, 'formula fully substituted')],
 'maths-2016-hl-p2-q7-a-i': [L(SOL, '|EC|² = 3² + 2·5² = 15·25'), L(SOL, '|EC| = √15·25'), L(SOL, '|EC| = 3·905'), L(SOL, '⟹ |AC| = 1·9525'), L(SOL, '= 1·95'),
     L(LPC, 'Pythagoras with relevant substitution'), L(HPC, '|EC| correct'), L(HPC, '|AC| = 1/2 √15·25')],
 'maths-2016-hl-p2-q7-a-ii': [L(SOL, 'tan 50° = |AB|/1·95'), L(SOL, '|AB| = 1·95(1·19175) = 2·23239'), L(SOL, '|AB| = 2·3'), L(PC, 'tan formulated correctly')],
 'maths-2016-hl-p2-q7-a-iii': [L(SOL, '|BC|² = 1·95² + 2·3²'), L(SOL, 'BC = 3 · 015377'), L(SOL, '|BC| = 3'), L(ALT, 'sin 40° = 1·95/|BC|'),
     L(LPC, 'Pythagoras with relevant substitution'), L(HPC, 'Pythagoras fully substituted'), L(HPC, '|BC| = 1·95/sin 40° ( i.e. |BC| isolated)')],
 'maths-2016-hl-p2-q7-a-iv': [L(SOL, '3² = 3² + 2·5² − 2(3)(2·5) cos ∝'), L(SOL, '15 cos ∝ = 6·25'), L(SOL, '∝ = 65°'), L(ALT, 'cos ∝ = 1·25/3'),
     L(LPC, 'cosine rule with some relevant substitution'), L(LPC, 'cosine ratio with some relevant substitutions'),
     L(LPC, 'identifies three sides of triangle BCD'), L(HPC, 'cosine rule with full relevant substitutions'),
     L(HPC, 'cosine ratio with full relevant substitutions')],
 'maths-2016-hl-p2-q7-a-v': [L(SOL, 'A = 2isosceles triangle +2equilateral triangle'), L(SOL, '= 2× [1/2 (2·5)(3) sin 65°] + 2 × [1/2 (3)(3) sin 60°]'),
     L(SOL, '= 14·59'), L(SOL, 'A=15'), L(LPC, 'recognises area of 4 triangles'), L(MPC, 'Area of 1 triangle correct'),
     L(HPC, 'area of isosceles triangle and equilateral triangle'), L(NOTE, 'Area = 4 isosceles or 4 equilateral triangles merit HPC at most')],
 'maths-2016-hl-p2-q7-b': [L(SOL, 'tan 60° = 3/|CA|'), L(SOL, '⟹ |CA| = √3'), L(SOL, '|CE| = 2√3'), L(SOL, 'x² + x² = (2√3)²'), L(SOL, 'x = √6'),
     L(LPC, 'effort at Pythagoras but without |CA| (or |CE|)'), L(LPC, '|CA| found'), L(HPC, '|CE| = 2√3')],
 'maths-2016-hl-p2-q8-a': [L(SOL, 'Period = 2π/(π/6) = 12 hours'), L(SOL, 'Range = [1·6 − 1·5 , 1·6 + 1·5 ]= [0·1 m, 3·1 m]'), L(LPC, 'some use of 2π or π/6'), L(LPC, 'range of cos function'),
     L(HPC, 'period or range correct'), L(NOTE, 'Accept correct period and/or range without work')],
 'maths-2016-hl-p2-q8-b': [L(SOL, 'Max = 1·6 + 1·5(1) =3·1 m.'), L(ALT, '3·1 m from range'), L(PC, 'max occurs when cos A = 1 or t = 0'),
     L(PC, 'effort at ℎ′(t)'), L(NOTE, 'Accept correct answer without work')],
 'maths-2016-hl-p2-q8-c': [L(SOL, 'ℎ′(t) = 1·5(−sin πt/6) π/6'), L(SOL, 'ℎ′(2) = 1·5(−sin 2π/6) π/6'), L(SOL, '= ‒ 0·68017 =−0·68 m/h'),
     L(SOL, 'Tide is going out at a rate of 0·68 m per hour at 2 am'), L(LPC, 'effort at differentiation'),
     L(HPC, 'correct numerical answer but not in context')],
 'maths-2016-hl-p2-q8-d-i': [L(LPC, 'one correct height'), L(HPC, 'five correct heights')],
 'maths-2016-hl-p2-q8-d-ii': [L(LPC, 'one correct plot'), L(HPC, 'at least 7 correct plots'), L(HPC, 'plots correct but graph not sketched or sketched incorrectly')],
 'maths-2016-hl-p2-q8-e': [L(SOL, 'Low tide = 0·1 m'), L(SOL, 'High tide = 3·1 m'), L(SOL, 'Difference = 3·1 − 0·1 =3 m'),
     L(PC, 'height of Low tide or High tide correctly identified'), L(NOTE, '(i) candidates may show work for this section on graph'),
     L(NOTE, '(ii) accept values from candidate’s graph'), L(NOTE, '(iii) accept correct answer from graph without work')],
 'maths-2016-hl-p2-q8-f': [L(SOL, 'Enter port at 9:30 approx'), L(SOL, 'Leave port before 15:15 approx'), L(SOL, 'Time = 15:15 – 9:30 = 5 hr 45 min approx.'),
     L(PC, 'time of entry to port or leave port correctly identified'), L(PC, 'value(s) for h = 2 and/or h = 1·5 on sketch'),
     L(PC, 'time estimated using relevant values other than those required for the maximum time.'),
     L(NOTE, '(i) candidates may show relevant work for this section on graph'), L(NOTE, '(ii) accept values from candidate’s graph')],
 'maths-2016-hl-p2-q9-a-i': [L(SOL, 'μ = 39400, σ = 12920'), L(SOL, 'z = 1·59'), L(SOL, 'P(z > 1·59) = 1 − P(z < 1·59)'), L(SOL, '= 1 − 0·9441 = 0·0559'),
     L(SOL, '= 5·59%'), L(SOL, '= 5·6%'), L(LPC, 'μ and σ identified'), L(MPC, 'z = 1·59'), L(HPC, 'identifies 0·9441')],
 'maths-2016-hl-p2-q9-a-ii': [L(SOL, 'P(z ≤ z1) = 0·9'), L(SOL, 'z1 = 1·28'), L(SOL, '⟹ z2 = −1·28'), L(SOL, '⟹ (x − 39400)/12920 = −1·28'), L(SOL, 'x = 22862·40'),
     L(SOL, '= €22 862'), L(LPC, 'identifies 1·28 but fails to progress'), L(HPC, 'formula for x fully substituted')],
 'maths-2016-hl-p2-q9-a-iii': [L(SOL, 'x̅ = 38280, n = 1000'), L(SOL, 'H0 ⇒ μ = 39400'), L(SOL, 'H1 ⇒ μ ≠ 39400'), L(SOL, '= −2·74'), L(SOL, '−2·74 < −1∙96'),
     L(SOL, 'Result is significant. There is evidence to reject the null hypothesis'), L(SOL, 'The mean income has changed.'),
     L(LPC, 'z formulated with some substitution'), L(LPC, 'states null and/or alternative hypothesis only'), L(LPC, 'reference to 1·96'),
     L(MPC, 'z fully substituted'), L(HPC, 'z = −2·74 and stops'), L(HPC, 'fails to state the null and alternative hypothesis correctly'),
     L(HPC, 'fails to contextualise the answer')],
 'maths-2016-hl-p2-q9-b': [L(SOL, '26974 − 1∙96 (5120/√400) ≤ μ ≤ 26974 + 1∙96 (5120/√400)'), L(SOL, '26472∙24 ≤ μ ≤ 27475∙76'),
     L(LPC, 'interval formulated with some correct substitution'), L(HPC, 'interval formulated with fully correct substitution')],
 'maths-2016-hl-p2-q9-c': [L(SOL, 'The distribution of sample means will be normally distributed'), L(PC, 'mentions 30 (or more) but not contextualised')],
 'maths-2016-hl-p2-q9-d': [L(SOL, '1/√n = 0∙045'), L(SOL, '1/0∙045 = √n'), L(SOL, '= 493∙827'), L(LPC, '1/√n'),
     L(HPC, 'n formulated with fully correct substitution'), L(NOTE, 'Accept 493 farmers or 494 farmers')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Filled from scheme_row_figures.py's output once its crops are opened and checked.
SCHEME_ROW_FIGURES = {
    'maths-2016-hl-p2-q3-a': 'maths-2016-HL-scheme-p032-i0',
    'maths-2016-hl-p2-q3-b': 'maths-2016-HL-scheme-p032-i1',
    'maths-2016-hl-p2-q4-a-ii': 'maths-2016-HL-scheme-p034-i0',
    'maths-2016-hl-p2-q4-b': 'maths-2016-HL-scheme-p035-i0',
    'maths-2016-hl-p2-q5-a-i': 'maths-2016-HL-scheme-p036-i0',
    'maths-2016-hl-p2-q6-b': 'maths-2016-HL-scheme-p037-i0',
    'maths-2016-hl-p2-q8-d-i': 'maths-2016-HL-scheme-p042-i0',
    'maths-2016-hl-p2-q8-d-ii': 'maths-2016-HL-scheme-p043-i0',
    'maths-2016-hl-p2-q9-a-iii': 'maths-2016-HL-scheme-p045-i0',
}

p = Paper(2016, 'hl', 'p2', {'5B': [0, 2, 5], '5C': [0, 2, 4, 5], '10B': [0, 5, 10], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10],
                             '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15]},
          'LC003ALP200EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
cl, cc = 'co-ordinate-geometry-of-the-line', 'co-ordinate-geometry-of-the-circle'
pts = 'The points A(6, −2), B(5, 3) and C(–3, 4) are shown on the diagram.'
q1a = 'Find the equation of the line through B which is perpendicular to AC.'
A('1-a', 'Q1(a)', '10C', [30], [3], '2-2', cl, q1a, stem=pts)
A('1-b', 'Q1(b)', '15D', [30], [3], '2-2', cl + ',geometry', 'Use your answer to part (a) above to find the co-ordinates of the orthocentre of the triangle ABC.',
  stem=pts + ' Part (a): ' + q1a)
xc = 'A point X has co-ordinates (−1, 6) and the slope of the line XC is 1/7.'
q2a = 'Find the equation of XC. Give your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.'
A('2-a', 'Q2(a)', '10C', [31], [4], '2-2', cl, q2a, stem=xc)
A('2-b', 'Q2(b)', '15D', [31], [4], '2-2', cc + ',' + cl, 'C is the centre of a circle s, of radius 5 cm. The line l: 3x + 4y − 21 = 0 is a tangent to s and passes through X, as shown. Find the equation of one such circle s.',
  stem=xc + ' Part (a): ' + q2a)
tfi = 'trigonometry-functions-identities'
A('3-a', 'Q3(a)', '15C', [32], [5], '2-3', tfi, 'Show that (cos 7A + cos A)/(sin 7A − sin A) = cot 3A.')
A('3-b', 'Q3(b)', '10D', [32, 33], [5], '2-3', tfi, 'Given that cos 2θ = 1/9, find cos θ in the form ± √a/b, where a, b ∈ ℕ.')
semi = 'The diagram shows a semi-circle standing on a diameter [AC], and [BD] ⊥ [AC].'
q4aii = 'If |AB| = x, |BC| = 1, and |BD| = y, write y in terms of x.'
A('4-a-i', 'Q4(a)(i)', '15C', [34], [6], '2-1', 'geometry-constructions-proofs,geometry', 'Prove that the triangles ABD and DBC are similar.', stem=semi)
A('4-a-ii', 'Q4(a)(ii)', '5C', [34], [6], '2-1', 'geometry', q4aii, stem=semi + ' Part (a)(i): Prove that the triangles ABD and DBC are similar.')
A('4-b', 'Q4(b)', '5C', [35], [6, 7], '2-1', 'geometry-constructions-proofs', 'Use your result from part (a)(ii) to construct a line segment equal in length (in centimetres) to the square root of the length of the line segment [TU] which is drawn below.',
  stem=semi + ' Part (a)(ii): ' + q4aii)
pr = 'probability'
arch = ('In an archery competition, the team consisting of John, David, and Mike will win 1st prize if at least two of them hit the bullseye with '
        'their last arrows. From past experience, they know that the probability that John, David, and Mike will hit the bullseye on their last '
        'arrow is 1/5, 1/6, and 1/4 respectively.')
q5ai = ('Complete the table below to show all the ways in which they could win 1st prize. Table: Way 1, Way 2, Way 3, Way 4. John: ✓, _, _, _. '
        'David: ✓, _, _, _. Mike: ×, _, _, _. ✓ = Hit, × = Miss.')
A('5-a-i', 'Q5(a)(i)', '5B', [36], [8], '1-2', pr, q5ai, stem=arch)
A('5-a-ii', 'Q5(a)(ii)', '10C', [36], [8], '1-2', pr, 'Hence or otherwise find the probability that they will win the competition.', stem=arch + ' Part (a)(i): ' + q5ai)
A('5-b', 'Q5(b)', '10C', [36], [8], '1-2', pr, 'Two events, A and B, are represented in the diagram. P(A ∩ B) = 0·1, P(B \\ A) = 0·3 and P(A \\ B) = x. Write P(A) in terms of x and hence, or otherwise, find the value of x for which the events A and B are independent.')
lotto = ('A local sports club is planning to run a weekly lotto. To win the Jackpot of €1000, contestants must match one letter chosen from the 26 '
         'letters in the alphabet and two numbers chosen, in the correct order, from the numbers 0 to 9. In this lotto, repetition of numbers is '
         'allowed (e.g. M, 3, 3 is an outcome).')
q6b = ('If a contestant matches the letter only, or the letter and one number (but not both numbers), they will win €50. Using the table below, or '
       'otherwise, find how much the club should expect to make or lose on each play, correct to the nearest cent, if they charge €2 per play. '
       'Table: Event, Payout (x) €, Probability (P(x)), x.P(x). Rows: Win Jackpot; Match letter and first number only; Match letter and second number only; '
       'Match letter and neither number; Fail to win.')
A('6-a', 'Q6(a)', '10C', [37], [9], '1-1', pr, 'Calculate the probability that M, 3, 3 would be the winning outcome in a particular week.', stem=lotto)
A('6-b', 'Q6(b)', '10C', [37], [9], '1-2', pr, q6b, stem=lotto)
A('6-c', 'Q6(c)', '5C', [38], [9], '1-2', pr, 'The club estimates that the average number of plays per week will be 845. If the club wants to make an average profit of €600 per week from the lotto, how much should the club charge per play, correct to the nearest cent?',
  stem=lotto + ' Part (b): ' + q6b)
tt = 'trigonometry-triangles'
lan = ('A glass Roof Lantern in the shape of a pyramid has a rectangular base CDEF and its apex is at B as shown. The vertical height of the pyramid '
       'is |AB|, where A is the point of intersection of the diagonals of the base as shown in the diagram. Also |CD| = 2·5 m and |CF| = 3 m.')
q7aii = 'The angle of elevation of B from C is 50° (i.e. |∠BCA| = 50°). Show that |AB| = 2·3 m, correct to one decimal place.'
q7aiii = 'Find |BC|, correct to the nearest metre.'
q7aiv = 'Find |∠BCD|, correct to the nearest degree.'
A('7-a-i', 'Q7(a)(i)', '10C', [39], [10], '2-3', tt, 'Show that |AC| = 1·95 m, correct to two decimal places.', stem=lan)
A('7-a-ii', 'Q7(a)(ii)', '10B', [39], [10], '2-3', tt, q7aii, stem=lan + ' Part (a)(i): Show that |AC| = 1·95 m, correct to two decimal places.')
A('7-a-iii', 'Q7(a)(iii)', '10C', [39], [10], '2-3', tt, q7aiii, stem=lan + ' Part (a)(ii): ' + q7aii)
A('7-a-iv', 'Q7(a)(iv)', '10C', [39], [11], '2-3', tt, q7aiv, stem=lan + ' Part (a)(iii): ' + q7aiii)
A('7-a-v', 'Q7(a)(v)', '10D', [40], [11], '2-3', tt + ',area-volume', 'Find the area of glass required to glaze all four triangular sides of the pyramid. Give your answer correct to the nearest m².',
  stem=lan + ' Part (a)(iii): ' + q7aiii + ' Part (a)(iv): ' + q7aiv)
A('7-b', 'Q7(b)', '5C', [40], [12], '2-3', tt, 'Another Roof Lantern, in the shape of a pyramid, has a square base CDEF. The vertical height |AB| = 3 m, where A is the point of intersection of the diagonals of the base as shown. The angle of elevation of B from C is 60° (i.e. |∠BCA| = 60°). Find the length of the side of the square base of the lantern. Give your answer in the form √a m, where a ∈ ℕ.')
tide = ('The height of the water in a port was measured over a period of time. The average height was found to be 1·6 m. The height measured in '
        'metres, h(t), was modelled using the function h(t) = 1·6 + 1·5 cos(π/6 t) where t represents the number of hours since the last recorded '
        'high tide and (π/6 t) is expressed in radians.')
q8di = ('On a particular day the high tide occurred at midnight (i.e. t = 0). Use the function to complete the table and show the height, h(t), of the '
        'water between midnight and the following midnight. Table: Time: Midnight, 3 a.m., 6 a.m., 9 a.m., 12 noon, 3 p.m., 6 p.m., 9 p.m., Midnight. '
        't (hours): 0, 3, _, _, _, _, _, _, _. h(t) (m): _, _, _, _, _, _, _, _, _.')
q8dii = 'Sketch the graph of h(t) between midnight and the following midnight.'
A('8-a', 'Q8(a)', '5C', [41], [13], '2-3', tfi, 'Find the period and range of h(t).', stem=tide)
A('8-b', 'Q8(b)', '5B', [41], [13], '2-3', tfi, 'Find the maximum height of the water in the port.', stem=tide)
A('8-c', 'Q8(c)', '5C', [41], [13], '5-2', 'differentiation-applications,' + tfi, 'Find the rate at which the height of the water is changing when t = 2, correct to two decimal places. Explain your answer in the context of the question.', stem=tide)
A('8-d-i', 'Q8(d)(i)', '10C', [42], [14], '2-3', tfi, q8di, stem=tide)
A('8-d-ii', 'Q8(d)(ii)', '10C', [43], [14], '2-3', tfi, q8dii, stem=tide + ' Part (d)(i): ' + q8di)
A('8-e', 'Q8(e)', '5B', [44], [15], '2-3', tfi, 'Find, from your sketch, the difference in water height between low tide and high tide.', stem=tide + ' Part (d)(ii): ' + q8dii)
A('8-f', 'Q8(f)', '5B', [44], [15], '2-3', tfi, 'A fully loaded barge enters the port, unloads its cargo and departs some time later. The fully loaded barge requires a minimum water level of 2 m. When the barge is unloaded it only requires 1·5 m. Use your graph to estimate the maximum amount of time that the barge can spend in port, without resting on the sea-bed.',
  stem=tide + ' Part (d)(ii): ' + q8dii)
earn = ('Data on earnings were published for a particular country. The data showed that the annual income of people in full-time employment was '
        'normally distributed with a mean of €39 400 and a standard deviation of €12 920.')
zs, inf = 'statistics-z-scores', 'statistics-inferential-statistics'
A('9-a-i', 'Q9(a)(i)', '10D', [45], [16], '1-3', zs, 'The government intends to impose a new tax on incomes over €60 000. Find the percentage of full-time workers who will be liable for this tax, correct to one decimal place.', stem=earn)
A('9-a-ii', 'Q9(a)(ii)', '5C', [45], [16], '1-3', zs, 'The government will also provide a subsidy to the lowest 10 % of income earners. Find the level of income at which the government will stop paying the subsidy, correct to the nearest euro.', stem=earn)
A('9-a-iii', 'Q9(a)(iii)', '15D', [45, 46], [16], '1-7', inf, 'Some time later a research institute surveyed a sample of 1000 full-time workers, randomly selected, and found that the mean annual income of the sample was €38 280. Test the hypothesis, at the 5 % level of significance, that the mean annual income of full-time workers has changed since the national data were published. State the null hypothesis and the alternative hypothesis. Give your conclusion in the context of the question.', stem=earn)
A('9-b', 'Q9(b)', '10C', [47], [17], '1-7', inf, 'The research institute surveyed 400 full-time farmers, randomly selected from all the full-time farmers in the country, and found that the mean income for the sample was €26 974 and the standard deviation was €5120. Assuming that annual farm income is normally distributed in this country, create a 95 % confidence interval for the mean income of full-time farmers.')
A('9-c', 'Q9(c)', '5B', [47], [17], '1-7', inf, 'It is known that data on farm size are not normally distributed. The research institute could take many large random samples of farm size and create a sampling distribution of the means of all these samples. Give one reason why they might do this.')
A('9-d', 'Q9(d)', '5C', [47], [17], '1-7', inf, 'The research institute also carried out a survey into the use of agricultural land. n farmers were surveyed. If the margin of error of the survey was 4·5 %, find the value of n.')

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 45, '9': 50}
p.check(marks, 34)
p.review(marks,
    'Independent visual reading of all 20 question-paper pages and PDF pages 27–52 of the combined Higher Level scheme (the Paper 2 title page 27, the scale table on page 28 (misheaded “Paper 1”), the summary of mark allocations on page 29, every Paper 2 model solution and marking note on pages 30–47, the Irish-language bonus-marks page 48 and the blank back pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(27, 53)), [28, 29],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 45 marks, Q9 50 marks). Every question is retained.',
     '34 independently marked units, matching the printed summary of allocations on scheme page 29.',
     'Paper 2 bands from the scale table on scheme page 28, which differ from Paper 1’s in the 10D ladder: 5B 0,2,5; 5C 0,2,4,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 34 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced. Stacked fractions are written a/b. Q3(b)’s mid partial credit prints 132·2° where its high partial credit prints 138·2°; both are quoted as printed.',
     'Nine parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because their model solution is a table, graph, construction or layout the text layer cannot carry: Q3(a) (the sum-to-product working), Q3(b) (method 4 continues on page 33), Q4(a)(ii), Q4(b) (the construction), Q5(a)(i) (the table), Q6(b) (the expected-value table), Q8(d)(i) (the table), Q8(d)(ii) (the graph) and Q9(a)(iii) (the confidence-interval methods continue on page 46).',
     'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. Scheme page references are PDF positions (printed page number + 4 in this half of the scheme); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 10], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [8, 9], 'wording': 'Hence or otherwise / hence, or otherwise / Using the table below, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'otherwise' in t else None)
p.apply(ROWS, '2016 Higher Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()},
        question_figures=True)
