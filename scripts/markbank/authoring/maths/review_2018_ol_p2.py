"""2018 OL Paper 2: a new paper — 39 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'
MIS = 'Misreading'

ROWS = {
 'maths-2018-ol-p2-q1-a-i': [L(LPC, 'One correct entry.'), L(LPC, 'Work of merit.'), L(HPC, 'Four correct entries.'), L(FC, 'Correct answer without work.'),
     L(ZC, 'Correct answers outside box with no work.')],
 'maths-2018-ol-p2-q1-a-ii': [L(SOL, '(6 + 2)/36 = 8/36 or 2/9'), L(PC, 'Work of merit.'), L(FC, 'Correct answer without work.'),
     L(ZC, 'Probability > 1, without work.')],
 'maths-2018-ol-p2-q1-a-iii': [L(SOL, '(1 + 2 + 4 + 6 + 2)/36 = 15/36 or 5/12'), L(PC, 'Prime Number identified.'), L(PC, 'Work of merit.'),
     L(FC, 'Correct answer without work.'), L(ZC, 'Probability > 1, without work.')],
 'maths-2018-ol-p2-q1-b': [L(SOL, '(18 + 8)/30 = 26/30 = 13/15'), L(ALT, '(30 − 4)/30 = 26/30 = 13/15'), L(ALT, '(18 + (11 + 8) − 11)/30 = 26/30'),
     L(LPC, 'Any relevant work towards creating at least one correct probability. (18 + 8, 30 – 4, 18 + 19 -11)'),
     L(HPC, 'Significant work towards answer.'), L(FC, 'Correct answer without work.'), L(ZC, 'Probability > 1, without work.')],
 'maths-2018-ol-p2-q2-a': [L(SOL, 'Method 1 : Midpoint formula'), L(SOL, '= ((7 + 11)/2, (10 + 4)/2)'), L(SOL, '= (9, 7)'),
     L(ALT, 'Method 2 : Translation (7,10) →(11, 4) X ↑4, y ↓6 (7,10) →(9,7)'),
     L(LPC, 'Correct relevant formula with some correct substitution.'), L(LPC, 'Correct translation identified.'),
     L(HPC, 'Formula fully substituted.'), L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q2-b': [L(SOL, 'Slope of UV = (y₂ − y₁)/(x₂ − x₁) = (7 − 6)/(9 − 4) = 1/5'), L(SOL, 'Slope of QR = (y₂ − y₁)/(x₂ − x₁) = (4 − 2)/(11 − 1) = 2/10'),
     L(SOL, 'Slope of QR = 1/5'), L(SOL, 'Conclusion: Slope of UV = slope of QR or UV ∥ QR'),
     L(LPC, 'Correct relevant formula with some correct or consistent substitution.'), L(MPC, 'One or both formulae fully substituted.'),
     L(HPC, 'Both slopes calculated and no conclusion.')],
 'maths-2018-ol-p2-q2-c': [L(SOL, 'Area = 1/2 |x₁y₂ − x₂y₁|'), L(SOL, '= 1/2 |(−6)(−6) − (4)(−8)|'), L(SOL, '= 1/2 |36 + 32|'), L(SOL, '= 34 square units'),
     L(LPC, 'Area of triangle formula with some relevant substitution.'), L(LPC, 'Translation of any relevant point to (0, 0).'),
     L(MPC, 'Area of triangle formula substituted correctly with TWO from P,Q, and R'),
     L(HPC, 'Formula fully substituted with translated points'),
     L(HPC, 'Area of triangle found from formula fully substituted with TWO from P,Q, and R')],
 'maths-2018-ol-p2-q2-d': [L(SOL, 'U(4,6) → V(9,7)\n(5,1)\nQ(1,2) → S(6,3)'), L(ALT, 'S = ((x₁ + x₂)/2, (y₁ + y₂)/2)'), L(ALT, 'S = ((1 + 11)/2, (2 + 4)/2)'),
     L(ALT, 'S = (6, 3)'), L(LPC, 'Work with a translation which indicates an understanding of the concept.'),
     L(LPC, 'Mid-Point Formula with some relevant substitution.'), L(HPC, 'An incorrect translation applied correctly.'),
     L(HPC, 'Correct translation applied to an incorrect point.'), L(HPC, 'Correct formula fully substituted.'), L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q3-a-i': [L(SOL, '7! = 5040'), L(SOL, '7 × 6 × 5 = 210'), L(LPC, 'Any work of merit towards creating at least one correct solution.'),
     L(HPC, 'One correct answer.'), L(HPC, 'Answers given as correct list with multiplication clearly indicated but answers not worked out.'),
     L(FC, 'Correct answers without work.')],
 'maths-2018-ol-p2-q3-b-i': [
     L(SOL, 'Colour Angle Probability Prize\nRed 72° 1/5 €20\nOrange 30° 1/12 €60\nYellow 45° 1/8 €24\nGreen 90° 1/4 €8\nBlue 60° 1/6 €42\nIndigo 18° 1/20 €90\nViolet 45° 1/8 €48'),
     L(SOL, '= 20 (1/5) + 60 (1/12) + 24 (1/8) + 8 (1/4) + 42 (1/6) + 90 (1/20) + 48 (1/8)'), L(SOL, '= 4 + 5 + 3 + 2 + 7 + 4·5 + 6'), L(SOL, '= 31·50'),
     L(LPC, 'Any work of merit e.g. One correct entry into table.'), L(MPC, 'Four correct entries into table.'),
     L(MPC, 'All incorrect consistent probabilities found.'), L(MPC, 'E(X) correct with no work and no table.'),
     L(HPC, 'Table correct or E(X) correct.'), L(HPC, 'Error/s in completed table and significant work in formulation of E(X).'),
     L(NOTE, 'If expected values are correct but not added then award F*')],
 'maths-2018-ol-p2-q4-a': [L(SOL, 'Centre = ((x₁ + x₂)/2, (y₁ + y₂)/2)'), L(SOL, '= ((1 + 9)/2, (8 + 0)/2)'), L(SOL, '= (5, 4)'),
     L(ALT, 'Method 2 : Translation (1,8) →(Centre) X ↑4, y ↓4 (1,8) →(5,4)'), L(PC, 'Mid-point formula with some correct substitution.'),
     L(PC, 'Leaves answer in fraction form.'), L(PC, 'Indicates centre.'), L(PC, 'Correct translation identified.'), L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q4-b': [L(SOL, '|BC| = √((x₂ − x₁)² + (y₂ − y₁)²)'), L(SOL, '= √((9 − 5)² + (0 − 4)²)'), L(SOL, '= √((4)² + (−4)²)'), L(SOL, '= √(16 + 16)'),
     L(SOL, '= √32'), L(SOL, '= 4√2 units'), L(LPC, 'Correct formula with some correct or consistent substitution.'), L(HPC, 'Formula fully substituted.'),
     L(HPC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q4-c': [L(SOL, '(x − ℎ)² + (y − k)² = r²'), L(SOL, '(x − 5)² + (y − 4)² = √32²'), L(SOL, '(x − 5)² + (y − 4)² = 32'),
     L(ALT, 'x² + y² − 10x − 8y + 9 = 0'), L(LPC, 'Correct formula with some correct or consistent substitution.'),
     L(HPC, 'Answer as (x − 5)² + (y − 4)² = √32²'), L(FC, 'Correct or consistent answer without work.')],
 'maths-2018-ol-p2-q4-d': [L(SOL, 'mr = −1'), L(SOL, 'mT = 1'), L(SOL, 'y − 8 = 1(x − 1)'), L(SOL, 'x − y + 7 = 0'),
     L(LPC, 'Correct relevant formula with some correct substitution.'), L(LPC, 'Finds slope of radius and stops.'),
     L(HPC, 'Eq. of line formula fully substituted.'), L(FC, 'Answer as (−x + y − 7 = 0).'), L(MIS, 'Equation of tangent through B (x − y − 9 = 0).')],
 'maths-2018-ol-p2-q5-a': [L(SOL, 'Method 1: Area of PQRS = Area of ABCD − 4(Area of AQP)'), L(SOL, '= 7 × 7 − 4[1/2(5) × 2]'), L(SOL, '= 49 − 20'),
     L(SOL, '= 29 cm²'), L(ALT, 'Method 2: Area of PQRS |PQ|² = |AQ|² + |AP|²'), L(ALT, '|PQ|² = |5|² + |2|²'), L(ALT, '|PQ|² = 29'),
     L(ALT, '|PQ| = √29'), L(ALT, 'Area of PQRS = (√29)²'), L(ALT, 'Area of PQRS = 29 cm²'), L(LPC, 'Any work of merit e.g. Identifies |QB| = 2.'),
     L(HPC, 'Correct relevant expression for Area of PQRS fully substituted.'), L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q5-b-i': [L(SOL, 'Circumference of u = 2πr = 2π(4) = 8π'), L(SOL, 'Circumference of v = 2πr = 2π(6) = 12π'),
     L(SOL, 'u will rotate (12π × 100)/8π = 150'), L(LPC, 'Circumference formula with some substitution.'),
     L(LPC, 'Any work of merit e.g. ratio of two circles.'), L(MPC, 'One circumference found (in terms of π).'),
     L(MPC, 'Both substitutions fully correct.'), L(HPC, 'Both circumferences found (in terms of π)'),
     L(HPC, 'Finds the number of rotations wheel u makes.')],
 'maths-2018-ol-p2-q6-a-i': [L(SOL, '|BC| = 8·8 cm'), L(LPC, 'A labelled pilot diagram drawn.'), L(LPC, 'One correct length or angle drawn.'),
     L(MPC, 'Any two components correct and stops.'), L(HPC, 'Construction correct but vertices incorrectly named or omitted and stops.'),
     L(MIS, 'Works with |AC|.'), L(NOTE, 'Tolerance ± 0·2 cm.'), L(NOTE, '|BC| must be ONE from the list: [(8·6),(8·7),(8·8),(8·9),(9·0)]')],
 'maths-2018-ol-p2-q6-b-i': [L(SOL, 'α = 115°'), L(SOL, 'β = 180° − 115° = 65°'), L(ALT, 'β = 1/2 [360° − (115° + 115°)] = 65°'), L(PC, 'One correct angle.'),
     L(FC, 'Correct answers without work.')],
 'maths-2018-ol-p2-q6-b-ii': [L(SOL, 'Side: |PQ| = |SR| (Opposite sides of a parallelogram)'),
     L(SOL, 'Angle: |∠PQR| = |∠RSP| (Opposite angles in a parallelogram)'), L(SOL, 'Side: |QR| = |PS| (Opposite sides of a parallelogram)'),
     L(SOL, '[Note that SSS or ASA may also be used]'), L(LPC, 'Any work of merit e.g. One correct statement.'),
     L(HPC, 'Two statements & Two reasons correct.'), L(FC, 'Three statements & Three reasons correct.')],
 'maths-2018-ol-p2-q7-a-i': [L(SOL, '(i) Range= 155 – 47 = 108 mm'), L(SOL, '(ii) Highest June rainfall = 2003'), L(SOL, '(iii) Least sunshine 2002'),
     L(LPC, 'Any work of merit e.g. (a)(i): [155 and/or 47] (a)(ii): [155] (a)(iii):[124]'), L(HPC, 'Two correct answers.'),
     L(HPC, 'Significant work in all answers.')],
 'maths-2018-ol-p2-q7-b': [L(SOL, 'Example 2006 is the year with the best weather. It had the least rainfall and /or the highest number of hours of sunshine.'),
     L(NOTE, 'Other equally valid choices are possible if accompanied by a reasonable reason.'),
     L(PC, 'Mention of year without reference to rainfall or sunshine.'), L(FC, 'Mention of year with reference to rainfall and/or sunshine.'),
     L(ZC, 'A reason with no year identified.')],
 'maths-2018-ol-p2-q7-c': [L(SOL, '47, 72, 84, 94, 94, 101, 133, 134, 149, 155.'), L(SOL, 'Median = (94 + 101)/2 = 97·5 mm.'), L(LPC, 'Effort at ordering data.'),
     L(LPC, 'Median calculated as ((94 + 47)/2) = 70·5.'), L(LPC, 'Consistent Median from an incorrect list (without work).'),
     L(HPC, 'All Data ordered.'), L(HPC, 'Correct Median without list.'), L(HPC, 'Correct Median with Sunshine data [173].'),
     L(FC, 'Correct list and correct Median without work.'), L(MIS, 'Works with a decreasing list.')],
 'maths-2018-ol-p2-q7-d-i': [L(SOL, '= 1818/10'), L(SOL, '= 181·8'), L(LPC, 'Effort at adding data.'), L(LPC, 'Division by 10.'),
     L(HPC, 'Formula fully substituted without calculation.'), L(HPC, 'Gets mean of the rainfall [=106·3].'), L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q7-d-ii': [L(SOL, '5% of 181·8 = 9·09'), L(SOL, '+5% = 190·89 hours'), L(SOL, '−5% = 172·71 hours'), L(SOL, 'Years within: 2003, 2004, 2005'),
     L(LPC, 'Any work of merit e.g. Identifies One year (without work).'), L(LPC, 'Finds 5% of mean [Answer (d)(i)].'),
     L(HPC, 'Two of the years identified (with work).'), L(HPC, 'Establishes [172·71, 190·89] or consistent.'), L(HPC, 'Correct answers without work.')],
 'maths-2018-ol-p2-q7-e': [L(SOL, 'Rainfall σ = 33·46057381'), L(SOL, 'σ = 33·5'), L(PC, 'Mean calculated as 106·3.'), L(PC, 'Calculates σ for sunshine data [32·1].'),
     L(NOTE, 'Answer as 33, or 33·46 merits F*.')],
 'maths-2018-ol-p2-q7-f-i': [L(SOL, 'Plots the remaining 6 pieces of data below.'), L(LPC, 'One correct plot.'), L(HPC, 'Four correct plots.'),
     L(NOTE, 'Tolerance: Within the correct box.')],
 'maths-2018-ol-p2-q7-f-ii': [L(SOL + ', box ticked', '−0·6'), L(SOL, 'Explanation: Correlation is negative and moderate or strong.'),
     L(FC, 'Correct box ticked and explanation is either: Correlation is negative and strong. or Correlation is negative and moderate.'),
     L(ZC, 'All other answers.')],
 'maths-2018-ol-p2-q8-a': [L(SOL, '|PQ|² = |PR|² + |RQ|²'), L(SOL, '6·5² = 3·3² + |RQ|²'), L(SOL, '42·25 = 10·89 + |RQ|²'), L(SOL, '|RQ|² = 42·25 − 10·89'),
     L(SOL, '|RQ|² = 31·36'), L(SOL, '|RQ| = √31·36'), L(SOL, '|RQ| = 5·6 m'), L(LPC, 'Correct relevant formula with some substitution.'),
     L(HPC, 'Correct formula fully substituted.'), L(HPC, 'Answer as √31·36.'), L(HPC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q8-b': [L(SOL, 'sin α = 3·3/6·5'), L(SOL, 'α = sin⁻¹(3·3/6·5)'), L(SOL, 'α = 30·51'), L(SOL, 'α = 31°'),
     L(LPC, 'Correct trigonometric ratio with some correct or consistent substitution.'), L(HPC, 'sin α = 3·3/6·5 (or similar).'),
     L(HPC, 'Finds |∠QPR| = 59° and stops.'), L(HPC, 'Incorrect Calculator Mode ( once only). Rad = 1, Grad = 34.')],
 'maths-2018-ol-p2-q8-c': [L(SOL, 'β = 180° − 31° = 149°'), L(PC, 'Any work of merit.'), L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q8-d': [L(SOL, 'a² = b² + c² − 2bc cos A'), L(SOL, '|RS|² = 8² + 5·6² − 2(8)(5·6) cos 149'), L(SOL, '|RS|² = 64 + 31·36 + 76·80219014'),
     L(SOL, '|RS|² = 172·16219014'), L(SOL, '|RS| = √172·16219014'), L(SOL, '|RS| = 13·121'), L(SOL, '|RS| = 13'),
     L(LPC, 'Any work of merit to identify the correct side required.(Pilot Diagram)'),
     L(LPC, 'Correct relevant formula with some correct or consistent substitution.'),
     L(MPC, 'Two relevant variables correctly substituted into correct relevant formula and stops.'), L(HPC, 'Fully correct substitution.'),
     L(HPC, 'Correct answer without work (13).'), L(HPC, 'Incorrect Calculator Mode ( once only). Rad = 115, Grad = 158.'),
     L(ZC, 'Treats triangle as right angled/Sine Rule.')],
 'maths-2018-ol-p2-q8-e': [L(SOL, 'Arc TS = 2πr × θ/360'), L(SOL, '= 2π(8) × 31/360'), L(SOL, '= 62π/45'), L(SOL, '= 4·3284'), L(SOL, '= 4·3'),
     L(LPC, 'Correct relevant formula with some correct or consistent substitution.'), L(HPC, 'Correct formula fully substituted')],
 'maths-2018-ol-p2-q8-f': [L(SOL, 'Area = πr² × θ/360'), L(SOL, '= π(8)² × 31/360'), L(SOL, '= 248π/45'), L(SOL, '= 17·3136'), L(SOL, '= 17·3'),
     L(LPC, 'Correct relevant formula with some substitution.'), L(HPC, 'Correct formula fully substituted')],
 'maths-2018-ol-p2-q9-a-i': [L(SOL, 'volume = 4/3 πr³'), L(SOL, '= 4/3 π(0·3)³'), L(SOL, '= 0·113097'), L(SOL, '= 0·113'),
     L(PC, 'Volume formula with radius substituted.'), L(FC, 'Correct answer without work.'), L(NOTE, 'Note 1: Answer: 0·113097 (without work). Merits F*'),
     L(NOTE, 'Note: 2 Value(π) Volume Answer 3·14 0·11304')],
 'maths-2018-ol-p2-q9-a-ii': [L(SOL, '0·113 × 19·3 = 2·1809'), L(SOL, '= 2·18'), L(PC, 'Any work of merit e.g. Indicates multiplication by 19·3.'),
     L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q9-a-iii': [L(SOL, '197 g = 6·02 × 10²³ atoms'), L(SOL, '2·18 g = 6·02 × 10²³/197 × 2·18'),
     L(SOL, '= 6·7 × 10²¹'), L(LPC, 'Finds expression for atoms in 1 g.'), L(LPC, 'Two incorrect operations and finishes.'),
     L(HPC, 'Finds expression for atoms in 2·18 g.'), L(HPC, 'One incorrect operation and finishes.')],
 'maths-2018-ol-p2-q9-b-i': [L(SOL, '= 0·025318 = 2·5'), L(LPC, 'Writes 1/√n.'), L(LPC, 'Sets up work as √1560.'),
     L(HPC, 'Correct formula fully substituted i.e. (1/√1560).'), L(HPC, 'MOE formula substituted and calculated as 0·025318 without work.'),
     L(FC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q9-b-ii': [L(SOL, '546/1560 = 0·35 = 35%'), L(SOL, '95% confidence interval = [p̂ − 1/√n , p̂ + 1/√n]'),
     L(SOL, '= [ 35 − 2·5 , 35 + 2·5 ]'), L(SOL, '= [ 32·5 , 37·5 ]'), L(LPC, 'Work of merit e.g. writes answer from (b) (i) in this part.'),
     L(LPC, 'Answer as 546/1560.'), L(LPC, 'p̂ ± 1/√n or p̂ ± 1·96√(p(1−p)/n)'), L(HPC, 'One boundary formed i.e. (35 + 2·5 or 35 – 2·5).'),
     L(HPC, 'Correct answer without work.')],
 'maths-2018-ol-p2-q9-b-iii': [L(SOL, 'H₀: p = 40%'), L(SOL, 'H₁: p ≠ 40%'), L(SOL, '40% ∉ [ 32·5% , 37·5% ]'), L(SOL, 'Reject Hₒ:'),
     L(SOL, 'Percentage of viewers who like the show does not equal 40%'), L(LPC, 'Any of: H₀, H₁, or C. I. correct.'),
     L(HPC, 'All of: H0, H1, and C.I. corrrect.'),
     L(FC, 'Result of Hypothesis Test plus conclusion in context e.g. Reject the Null Hypothesis and hence reject the executive’s claim.')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Parts whose printed model solution is an image (the Q1(a)(i) table of totals, the
# Q6(a) construction, the Q7(f)(i) scatterplot, the Q7(f)(ii) tick box) or loses a
# stacked fraction to the mark-cell filter (the Q8(e), Q8(f) high-partial
# expressions over 360; the Q9(a)(i) note's 22/7; the Q9(a)(iii) atoms in 1 g over
# 197; the Q9(b)(i) 1/√n) carry the SEC's own print of their scheme row (model
# solution and every credit band), shown only after the reveal.
# Crops: scheme_row_figures.py; ids are its output.
SCHEME_ROW_FIGURES = {
    'maths-2018-ol-p2-q1-a-i': 'maths-2018-OL-scheme-p024-i0',
    'maths-2018-ol-p2-q6-a-i': 'maths-2018-OL-scheme-p032-i0',
    'maths-2018-ol-p2-q7-f-i': 'maths-2018-OL-scheme-p035-i0',
    'maths-2018-ol-p2-q7-f-ii': 'maths-2018-OL-scheme-p035-i1',
    'maths-2018-ol-p2-q8-e': 'maths-2018-OL-scheme-p037-i0',
    'maths-2018-ol-p2-q8-f': 'maths-2018-OL-scheme-p037-i1',
    'maths-2018-ol-p2-q9-a-i': 'maths-2018-OL-scheme-p038-i0',
    'maths-2018-ol-p2-q9-a-iii': 'maths-2018-OL-scheme-p038-i1',
    'maths-2018-ol-p2-q9-b-i': 'maths-2018-OL-scheme-p039-i0',
}

p = Paper(2018, 'ol', 'p2', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 3, 7, 10],
                             '10D': [0, 2, 5, 8, 10], '15D': [0, 4, 7, 11, 15]},
          'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
pr = 'probability'
dice = 'An experiment consists of throwing two fair, standard, six-sided dice and recording the sum of the two numbers thrown. Some of the totals are shown in the table.'
A('1-a-i', 'Q1(a)(i)', '5C', [24], [3], '1-2', pr, 'Complete the table. Die 1 (columns): 1, 2, 3, 4, 5, 6. Die 2 = 1: 2, 3, 4, 5, 6, 7. Die 2 = 2: 3, 4, 5, 6, 7, 8. Die 2 = 3: 4, 5, 6, 7, 8, 9. Die 2 = 4: 5, 6, _, _, 9, 10. Die 2 = 5: 6, _, 8, 9, _, 11. Die 2 = 6: _, 8, 9, 10, 11, _.', stem=dice)
A('1-a-ii', 'Q1(a)(ii)', '5B', [24], [3], '1-2', pr, 'Find the probability of getting a total of 7 or 11.', stem=dice)
A('1-a-iii', 'Q1(a)(iii)', '5B', [24], [3], '1-2', pr, 'Find the probability of getting a total which is a prime number.', stem=dice)
A('1-b', 'Q1(b)', '10C', [25], [3], '1-2', pr, 'A car distributor sells Ford cars and Renault cars. It has 30 cars for sale on a particular day; 18 are Ford cars and 12 are Renault cars. 7 of the Ford cars are red and 4 of the Renault cars are red. One of the 30 cars is chosen at random. What is the probability that the car chosen is a Ford car or a car which is not red?')
tri = 'The points P(7, 10), Q(1, 2) and R(11, 4) are the vertices of the triangle shown. The point U(4, 6) is the midpoint of [PQ] and the point V is the midpoint of [PR].'
cl = 'co-ordinate-geometry-of-the-line'
A('2-a', 'Q2(a)', '5C', [26], [4], '2-2', cl, 'Find the co-ordinates of V.', stem=tri)
A('2-b', 'Q2(b)', '5D', [26], [4], '2-2', cl, 'Show, by using slopes, that UV is parallel to QR.', stem=tri)
A('2-c', 'Q2(c)', '10D', [27], [4], '2-2', cl, 'Find the area of the triangle PQR.', stem=tri)
A('2-d', 'Q2(d)', '5C', [27], [4], '2-2', cl, 'The point S is the image of the point Q under the translation UV⃗. Find the coordinates of S.', stem=tri)
A('3-a-i', 'Q3(a)(i),Q3(a)(ii)', '10C', [28], [5], '1-1', 'counting', '(i) Find the number of different arrangements that can be made using all the letters of the word RAINBOW. Each letter is used only once. (ii) Find the number of different 3-letter arrangements that can be made using the letters of the word RAINBOW. Each letter is used at most once.')
A('3-b-i', 'Q3(b)(i),Q3(b)(ii)', '15D', [28], [5], '1-3', pr, '(i) Complete the “Probability” column of the table which shows the probability of the spinner coming to rest in each sector after one spin. (ii) Find the expected value of the prize that a player wins if they play Rainbow.',
  stem='A game, called Rainbow, uses an unbiased circular spinner. The spinner has seven sectors coloured red (R), orange (O), yellow (Y), green (G), blue (B), indigo (I), and violet (V) as shown below. The table below shows the angle of each sector. It also shows the cash prize that a player wins if the spinner stops in that sector. Colour, Angle, Probability, Prize: Red, 72°, _, €20; Orange, 30°, _, €60; Yellow, 45°, 1/8, €24; Green, 90°, _, €8; Blue, 60°, _, €42; Indigo, 18°, _, €90; Violet, 45°, _, €48.')
cw = 'The points A(1, 8) and B(9, 0) are the end-points of a diameter of the circle w, as shown in the diagram.'
q4a = 'Find the co-ordinates of the centre of w.'
q4b = 'Find the length of the radius of w. Give your answer in the form p√q, where p, q ∈ ℕ.'
cc = 'co-ordinate-geometry-the-circle'
A('4-a', 'Q4(a)', '5B', [29], [6], '2-2', cc, q4a, stem=cw)
A('4-b', 'Q4(b)', '5C', [29], [6], '2-2', cc, q4b, stem=cw)
A('4-c', 'Q4(c)', '10C', [29], [6], '2-2', cc, 'Hence write down the equation of the circle w.', stem=cw + ' Part (a): ' + q4a + ' Part (b): ' + q4b)
A('4-d', 'Q4(d)', '5C', [30], [6], '2-2', cc + ',' + cl, 'Find the equation of the line that is a tangent to the circle w at A. Give your answer in the form ax + by + c = 0, where a, b, and c ∈ ℤ.', stem=cw)
av = 'area-volume'
A('5-a', 'Q5(a)', '10C', [31], [7], '3-4', av, 'The square ABCD has sides of length 7 cm. The vertices of the square PQRS lie on the perimeter of ABCD, as shown in the diagram, with |AQ| = 5 cm. Find the area of the square PQRS.')
A('5-b-i', 'Q5(b)(i),Q5(b)(ii)', '15D', [31], [7], '3-4', av, '(i) Find the length of the circumference of each circle. Give your answers in cm in terms of π. (ii) The wheels u and v are in non-slip contact and therefore the rotation of one causes the other to rotate. Find the number of complete rotations wheel u makes if wheel v completes 100 rotations.',
  stem='The circles u and v represent two wheels that are free to rotate about their centres, as shown. The radius of u is 4 cm and the radius of v is 6 cm.')
A('6-a-i', 'Q6(a)(i),Q6(a)(ii)', '10D', [32], [8], '2-1', 'geometry-proofs-and-constructions', '(i) Construct the triangle ABC, where |AB| = 10 cm, |∠CAB| = 60° and |∠ABC| = 40°. Label each vertex clearly. (ii) Measure |BC|, and write your answer in cm, correct to 1 decimal place.')
par = 'The diagram shows a parallelogram with vertices P, Q, R, and S. |∠SPQ| = 115°, |∠QRS| = α° and |∠RSP| = β°.'
A('6-b-i', 'Q6(b)(i)', '5B', [32], [9], '2-1', 'geometry', 'Write down the value of α and the value of β.', stem=par)
A('6-b-ii', 'Q6(b)(ii)', '10C', [32], [9], '2-1', 'geometry', 'Explain why the triangle PQR is congruent to triangle RSP. Give a reason for any statement you make in your explanation.', stem=par)
val = 'The table below shows the total rainfall, in millimetres, and the total sunshine, in hours, at Valentia, County Kerry, during the month of June from 2001 to 2010. Total rainfall and total sunshine at Valentia in June. Year: 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010. Total Rainfall (mm): 72, 133, 155, 101, 94, 47, 149, 134, 94, 84. Total Sunshine (hours): 169, 124, 180, 173, 173, 239, 159, 168, 228, 205. (Source: Met Éireann)'
sc = val + ' Part (f): Part of a scatterplot of the data in the table is shown below. The first four data points are plotted.'
st = 'statistics'
A('7-a-i', 'Q7(a)(i),Q7(a)(ii),Q7(a)(iii)', '10C', [33], [10], '1-6', st, 'Based on the data in the table above write down: (i) the range of the rainfall data (ii) the year with the highest June rainfall (iii) the year with the least June sunshine', stem=val)
A('7-b', 'Q7(b)', '5B', [33], [10], '1-7', st, 'Based on the data in the table, write down the year with the best June weather and give a reason for your answer.', stem=val)
A('7-c', 'Q7(c)', '10C', [33], [10], '1-6', st, 'Write the rainfall data in increasing order and hence find the median of the rainfall.', stem=val)
A('7-d-i', 'Q7(d)(i)', '10C', [34], [10], '1-6', st, 'Find the mean number of sunshine hours for June in Valentia between 2001 and 2010.', stem=val)
A('7-d-ii', 'Q7(d)(ii)', '5C', [34], [10, 11], '1-6', st, 'For what years was the sunshine data within 5% of the mean number of sunshine hours in Valentia?', stem=val + ' Part (d)(i): Find the mean number of sunshine hours for June in Valentia between 2001 and 2010.')
A('7-e', 'Q7(e)', '5B', [34], [10, 11], '1-6', st, 'Find the standard deviation of the rainfall data, in mm, correct to 1 decimal place.', stem=val)
A('7-f-i', 'Q7(f)(i)', '10C', [35], [10, 11], '1-6', st, 'Complete the scatterplot.', stem=sc)
A('7-f-ii', 'Q7(f)(ii)', '5A', [35], [10, 11], '1-7', st, 'One of the numbers in the table on the right is the correlation coefficient for the data above, correct to 1 decimal place. Based on the scatterplot, select the number that you think most accurately reflects this data. Explain your choice. Tick one box: 0·6, 0·1, −0·1, −0·6.', stem=sc)
gd = 'The diagram shows a section of a garden divided into three parts. In the diagram: |PR| = 3·3 m, |PQ| = 6·5 m, |QT| = |QS| = 8 m, |∠QRP| = 90°, |∠PQR| = α°, and |∠RQS| = β°.'
q8e = 'SQT is a sector of a circle whose centre is Q. Find the length of the arc TS. Give your answer in metres, correct to one decimal place.'
tg = 'trigonometry'
A('8-a', 'Q8(a)', '10C', [36], [12], '2-3', tg, 'Use the theorem of Pythagoras to find |RQ|.', stem=gd)
A('8-b', 'Q8(b)', '10C', [36], [12], '2-3', tg, 'Show that α = 31°, correct to the nearest degree.', stem=gd)
A('8-c', 'Q8(c)', '5B', [36], [12], '2-3', tg, 'Use the value of α given in part (b) to find the value of β.', stem=gd)
A('8-d', 'Q8(d)', '15D', [37], [12, 13], '2-3', tg, 'Use the Cosine Rule to find the length of [RS]. Give your answer correct to the nearest metre.', stem=gd)
A('8-e', 'Q8(e)', '5C', [37], [12, 13], '3-4', av, q8e, stem=gd)
A('8-f', 'Q8(f)', '5C', [37], [12, 13], '3-4', av, 'Find the area of the sector SQT. Give your answer in square metres, correct to one decimal place.', stem=gd + ' Part (e): ' + q8e)
q9ai = 'Find the volume of a solid sphere of radius 0·3 cm. Give your answer in cm³, correct to 3 decimal places.'
q9aii = 'The sphere is made of pure gold. Each cm³ of pure gold weighs 19·3 grams. Find the number of grams of pure gold in the sphere. Give your answer correct to 2 decimal places.'
tv = 'A survey was carried out on behalf of a television station to investigate the popularity of a certain show.'
q9bi = 'A random sample of 1560 television viewers was surveyed. Find the margin of error of the survey. Give your answer as a percentage, correct to 1 decimal place.'
q9bii = 'In the survey, 546 of the 1560 viewers surveyed said that they liked the show. Use your answer to part b(i) above to create a 95% confidence interval for the percentage of viewers who liked the show.'
A('9-a-i', 'Q9(a)(i)', '10B', [38], [14], '3-4', av, q9ai)
A('9-a-ii', 'Q9(a)(ii)', '5B', [38], [14], '3-4', av, q9aii, stem='Part (a)(i): ' + q9ai)
A('9-a-iii', 'Q9(a)(iii)', '5C', [38], [14], '3-2', 'indices,number-systems', 'It is known that there are approximately 6·02 × 10²³ atoms in 197 grams of pure gold. Find the number of atoms of pure gold in the sphere. Give your answer in the form a × 10^n, where 1 ≤ a < 10, n ∈ ℕ, and where a is correct to 2 significant figures.', stem='Part (a)(i): ' + q9ai + ' Part (a)(ii): ' + q9aii)
A('9-b-i', 'Q9(b)(i)', '5C', [39], [15], '1-7', st, q9bi, stem=tv)
A('9-b-ii', 'Q9(b)(ii)', '5C', [39], [15], '1-7', st, q9bii, stem=tv + ' Part (b)(i): ' + q9bi)
A('9-b-iii', 'Q9(b)(iii)', '10C', [39], [15], '1-7', st, 'An executive for the television station had claimed that 40% of viewers liked the show. Use your answer to part b(ii) above to conduct a hypothesis test, at the 5% level of significance, to test the executive’s claim. State your null hypothesis, your alternative hypothesis and give your conclusion in the context of the question.', stem=tv + ' Part (b)(ii): ' + q9bii)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 60, '8': 50, '9': 40}
p.check(marks, 39)
p.review(marks,
    'Independent visual reading of all 16 question-paper pages and PDF pages 21–40 of the combined Ordinary Level scheme (the Paper 2 title page 21, the scale table on page 22, the summary of mark allocations on page 23, every Paper 2 model solution and marking note on pages 24–39, and the back cover on page 40). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(21, 41)), [22, 23],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 60 marks, Q8 50 marks, Q9 40 marks). Every question is retained.',
     '39 independently marked units, matching the printed summary of allocations on scheme page 23. Q3(a)(i)+(ii), Q3(b)(i)+(ii), Q5(b)(i)+(ii), Q6(a)(i)+(ii) and Q7(a)(i)+(ii)+(iii) each share one printed scale and are one task.',
     'Paper 2 bands from the 2018 Ordinary scale table on scheme page 22, which differ from Paper 1’s: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,2,5,8,10; 15D 0,4,7,11,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 39 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced, and its Misreading notes keep their own label. The Q3(b) probability table is quoted as one multi-line point. The ticked Q7(f)(ii) box is named in the row label.',
     'Nine parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal: Q1(a)(i), Q6(a), Q7(f)(i) and Q7(f)(ii), whose model solutions are a completed table, a construction, a scatterplot and a tick box printed as images, and Q8(e), Q8(f), Q9(a)(i), Q9(a)(iii) and Q9(b)(i), where a stacked fraction’s denominator or numerator is filtered as a mark cell.',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3], 'wording': 'Answer all nine / all six questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [3], 'wording': 'a Ford car or a car which is not red', 'classification': 'mathematical-context',
      'reason': 'The or-event is the probability being asked for, not a choice between printed prompts.'},
     {'pages': [11], 'wording': 'select the number that you think most accurately reflects this data', 'classification': 'answer-selection',
      'reason': 'The candidate ticks one of four printed correlation values as the answer to one required task; it is not a choice of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('mathematical-context', 'The car chosen being a Ford car or a car which is not red is the event whose probability is asked for, not a choice between printed prompts.') if 'Renault' in t
        else ('answer-selection', 'The candidate ticks one of four printed correlation values as the answer to one required task; it does not offer alternative practice prompts.') if 'scatterplot' in t else None)
p.apply(ROWS, '2018 Ordinary Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()})
