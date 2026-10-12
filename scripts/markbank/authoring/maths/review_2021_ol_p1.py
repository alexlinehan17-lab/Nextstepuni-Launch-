"""2021 OL Paper 1: review ledger, restored prompts, ship held-back Q2(b), re-quote garbled rows."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *
from rows_2021_ol_p1 import ROWS

p = Paper(2021, 'ol', 'p1', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10], '15D': [0, 4, 7, 11, 15], '20D': [0, 5, 10, 15, 20]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
fm = 'financial-maths'; cx = 'complex-numbers'; eq = 'algebra-equations'; ss = 'sequences-series'
A('1-a', 'Q1(a)', '5C', [8], [4], '3-3', fm, 'A television costs €380 before VAT at 21% has been added. Find the cost of the television after VAT has been added.')
A('1-b', 'Q1(b)', '5C', [8], [4], '3-3', fm, 'When VAT at 21% is included, the price of a laptop increases by €130·20. Find the total cost of the laptop including VAT.')
A('1-c', 'Q1(c)', '10C', [9], [4], '3-3', fm, 'A printer is priced at €290·40 including VAT at 21%. Find how much VAT is included in the price of this printer.')
A('1-d', 'Q1(d)', '10C', [9], [5], '3-3', fm, 'On September 1, 2020 the Standard Rate of VAT in Ireland was reduced from 23% to 21%. A company bought 30 computers in September, all at the same price. The company calculated that it saved €336 due to the reduction in the VAT rate. Find the price of one computer before VAT had been added.')
z = 'z₁ = −3 + 4i and z₂ = 4 + 3i, where i² = −1.'
A('2-a', 'Q2(a)', '10D', [10], [6], '4-4', cx, 'Plot and label z₁, z₂, and z₁ + z₂ on the Argand Diagram.', stem=z)
A('2-b', 'Q2(b)', '10C', [10], [6], '4-4', cx, 'z₃ = z₁/z₂. Find z₃ in the form a + bi, where a, b ∈ ℤ.', stem=z)
A('2-c', 'Q2(c)', '10D', [11], [7], '4-4', cx, 'Find |z̅₁ − z₂|, where z̅₁ is the complex conjugate of z₁. Give your answer in the form p√q, where p and q ∈ ℕ.', stem=z)
A('3-a', 'Q3(a)', '10C', [12], [8], '4-2', eq, 'Show that x = 4 is a solution of the equation x² − 2x − 8 = 0.')
A('3-b', 'Q3(b)', '10D', [12], [8], '4-2', eq, 'The equation x² + ax + b = 0, where a, b ∈ ℤ, has solutions x = 5 and x = −2. Find the value of a and the value of b.')
A('3-c', 'Q3(c)', '10C', [12], [9], '4-2', eq, 'Find the solutions of the equation 5x² − 2x − 9 = 0, where x ∈ ℝ. Give each answer correct to 2 decimal places.')
A('4-a', 'Q4(a)', '10C', [13], [10], '4-2', eq, 'Solve the equation: 4(2x + 3) − 7 = 3(x − 5), where x ∈ ℝ.')
A('4-b', 'Q4(b)', '20D', [13], [11], '4-2', eq, 'Solve the simultaneous equations: 2x − y = 7; x² + y² = 49.')
f = 'The function, f is defined as f(x) = 3x² − 6x + 7, where x ∈ ℝ.'
A('5-a', 'Q5(a)', '10C', [14], [12], '5-1', 'functions', 'Find f(0·67), correct to 2 decimal places.', stem=f)
A('5-b', 'Q5(b)', '10C', [14], [12], '4-2', eq + ',functions', 'Find the value of x when f(x) = 4.', stem=f)
A('5-c', 'Q5(c)', '10D', [15], [13], '5-2', 'differentiation', 'Use calculus to find the co-ordinates of the local minimum point of f.', stem=f)
ar = 'The first three terms of an arithmetic sequence are −5, k, 1.'
A('6-a-i', 'Q6(a)(i)', '5C', [16], [14], '4-1', ss, 'Find k and hence or otherwise show that the common difference is 3.', stem=ar)
A('6-a-ii', 'Q6(a)(ii)', '5C', [16], [14], '4-1', ss, 'Find T₁₀, the 10th term in the sequence.', stem=ar)
A('6-a-iii', 'Q6(a)(iii)', '10C', [17], [14], '4-1', ss, 'Find which term in the sequence has a value of 247.', stem=ar)
A('6-b', 'Q6(b)', '10C', [17], [15], '4-1', ss, 'The first three terms of a different arithmetic sequence are 4, 9, 14. Find S₅₀, the sum of the first 50 terms of the sequence.')
usc = 'The rates and thresholds of the Universal Social Charge (USC) in Ireland (excluding the top rate) during 2020 are given in the table below. Standard rates and thresholds for USC 2020: first €12 012 at 0·5%; next €8472 at 2%; next €49 560 at 4·5%; balance at the top rate. (Source: www.revenue.ie)'
A('7-a', 'Q7(a)', '5C', [18], [16], '3-3', fm, 'At what level of annual income does a worker start paying the top rate of USC?', stem=usc)
A('7-b', 'Q7(b)', '10D', [18], [16], '3-3', fm, 'How much USC will a worker have paid in total if they pay the maximum amount due at each of the first three rates?', stem=usc)
A('7-c', 'Q7(c)', '10D', [18], [16], '3-3', fm, 'John’s annual income is €54 800. Find the amount of USC he will pay.', stem=usc)
A('7-d', 'Q7(d)', '10D', [19], [17], '3-3', fm, 'Mary pays €1602·72 in USC in 2020. Find her annual income.', stem=usc)
A('7-e', 'Q7(e)', '15D', [19], [17], '3-3', fm, 'Patrick has an annual income of €83 000 and pays a total of €3496·18 in USC. Find the top rate of USC.', stem=usc)
box = 'A square sheet of cardboard, of side 10 units, is used to make an open box. Squares of side x units, where x ∈ ℝ, are removed from each corner of the cardboard and it is then folded along the dotted lines, as shown in the diagram below, in order to create the box.'
A('8-a', 'Q8(a)', '5C', [20], [18], '3-4', 'area-volume', 'The length (l), breadth (b) and height (h) of the box are shown in the diagram above. Write l, b, and h in terms of x.', stem=box)
A('8-b', 'Q8(b)', '10D', [20], [18], '3-4', 'area-volume,algebra', 'Show that the volume of the box can be written as V(x) = 4x³ − 40x² + 100x.', stem=box)
A('8-c', 'Q8(c)', '5B', [20], [18], '3-4', 'area-volume', 'Explain why a box of height 6 units cannot be made from the sheet of cardboard.', stem=box)
A('8-d', 'Q8(d),Q8(e)', '20D', [21], [19], '5-1', 'graphing-functions', '(d) Complete the table below to show the values of V(x) = 4x³ − 40x² + 100x, where x ∈ ℝ, for the given values of x in the domain 0 ≤ x ≤ 5 (x = 0, 0·5, 1, …, 5; the table gives V(0·5) = 40·5 and V(4·5) = 4·5). (e) Draw the graph of the function V(x) on the grid below.', stem=box)
A('8-f-i', 'Q8(f)(i),Q8(f)(ii),Q8(f)(iii)', '10D', [22], [19], '5-1', 'graphing-functions', 'Use your graph to estimate each of the following values. In each case show your work on the graph above. (i) The maximum volume of the box. (ii) The values of x which will create a box which has a volume of 30 units cubed. (iii) The volume of the box when x is 2·8 units.', stem=box + ' V(x) = 4x³ − 40x² + 100x, for 0 ≤ x ≤ 5.')
pat = 'The first three patterns in a sequence of patterns containing dots and crosses are shown below. Pattern 1 has 1 dot above 1 cross; pattern 2 has 2 dots above a 2 × 2 block of crosses; pattern 3 has 3 dots above a 3 × 3 block of crosses.'
A('9-a-i', 'Q9(a)(i)', '5C', [23], [20], '4-1', ss, 'Draw the fourth pattern in the sequence into the box below.', stem=pat)
A('9-a-ii', 'Q9(a)(ii)', '5C', [23], [20], '4-1', ss, 'Find a formula, in n, for the number of dots in pattern n of the sequence (Tₙ).', stem=pat)
A('9-a-iii', 'Q9(a)(iii)', '5C', [23], [21], '4-1', ss, 'Find the total number of dots in the first 20 patterns of the sequence.', stem=pat)
A('9-a-iv', 'Q9(a)(iv)', '10D', [24], [21], '4-1', ss, 'The table shows the number of crosses for the first two patterns (pattern 1: 1; pattern 2: 4). Complete the table for patterns 3 to 6, and hence find a formula for the number of crosses in pattern n of the sequence.', stem=pat)
A('9-a-v', 'Q9(a)(v)', '5C', [24], [21], '4-1', ss, 'Find the number of crosses in pattern 12 of the sequence.', stem=pat)
A('9-a-vi', 'Q9(a)(vi)', '5C', [24], [21], '4-1', ss, 'Find the number of shapes (dots and crosses) in pattern 10 of the sequence.', stem=pat)
quad = 'The first two patterns in a sequence of patterns of crosses are shown below: pattern 1 has 1 cross; pattern 2 has 3 crosses. The number of crosses in pattern n is Tₙ. The general term describing Tₙ can be written in the form: Tₙ = n²/2 + bn + c, where b, c ∈ ℝ.'
A('9-b-i', 'Q9(b)(i)', '5C', [25], [22], '4-1', ss + ',algebra', 'Use substitution for n to write T₁ and T₂ in terms of b, c, and a number.', stem=quad)
A('9-b-ii', 'Q9(b)(ii)', '10C', [25], [22], '4-2', eq, 'Hence, or otherwise, find the value of b and the value of c.', stem=quad)
dam = 'The water behind a dam is normally released at a rate of 250 000 litres per second.'
ns = 'number-systems'
A('10-a-i', 'Q10(a)(i)', '10C', [26], [23], '3-3', ns, 'Find how long it takes to release 1 million cubic metres (1 000 000 m³) of water. Note 1 m³ = 1000 litres. Give your answer correct to the nearest minute.', stem=dam)
A('10-a-ii', 'Q10(a)(ii)', '10D', [26], [23], '3-3', ns, 'Due to heavy rainfall, the operators of the dam decide to increase the flow by 10% for 24 hours. Find how many m³ of water were released in that 24 hour period. Give your answer in the form a × 10ⁿ, where 1 ≤ a < 10, and n ∈ ℕ. Give the value of a correct to 3 significant figures.', stem=dam)
A('10-b-i', 'Q10(b)(i)', '10D', [26], [24], '3-4', 'area-volume,' + ns, 'John walks around a circular trail of radius 0·5 km at a steady speed of 6 km/h. How long will it take him to complete 3 full circuits of the trail? Give your answer correct to the nearest minute.')
A('10-b-ii', 'Q10(b)(ii)', '10D', [27], [24], '3-3', ns, 'Mary decides to walk every day over a 5 day period. She walks a distance of 3 km on day one. She increases the length of her walk by 15% each day for the next four days. Her average speed on day 5 is 4 km/h. Find how long it will take her to complete her walk on day 5. Give your answer in minutes, correct to the nearest minute.')
A('10-b-iii', 'Q10(b)(iii)', '10D', [28], [25], '3-3', ns, 'One day, during John’s walk he meets Mary at point P on the trail. Mary is walking in the opposite direction at a steady speed of 4 km/h. John continues walking at 6 km/h. How far will he travel until he meets Mary again? Give your answer correct to the nearest metre.', stem='John walks around a circular trail of radius 0·5 km at a steady speed of 6 km/h.')

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 42)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 1–29 of the combined Ordinary Level scheme (cover, contents, the Paper 1 scale table on page 5, the summary of allocations on page 6, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 30)), [5, 6],
    ['The 2021 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '42 independently marked units, matching the printed summary of allocations on scheme page 6. Shared scales keep their parts together: Q8(d)–(e) 20D and Q8(f)(i)–(iii) 10D.',
     'Paper 1 bands from scheme page 5: 5B 0,2,5; 5C 0,2,3,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15D 0,4,7,11,15; 20D 0,5,10,15,20. The 15D ladder (0,4,7,11,15) differs from the later 0,4,8,12,15.',
     'All 42 units were already authored; 41 shipped. Q2(b) was refused by the build because its prompt carried one unreadable glyph (U+0BED) from a broken font subset. The glyph is Cambria glyph id 3053, which sits directly after glyph 3052 (italic y) at the end of the italic small-letter run 3028 = a … 3052 = y and is never seen with a correct ToUnicode in any Maths paper or scheme; cropping it from paper page 6 shows the z of z₁ and z₂. It is recorded as italic z in derive_glyphs.py’s neighbour table and glyphmap.json, and the prompt is restored from the paper. Eight cards had marking points garbled by the text layer (stacked fractions dropped, a missing mid band on Q5(c) and Q7(d), solution lines shipped as credit notes) and are re-quoted from the printed scheme, labelled by band. All existing IDs are kept; topics are corrected as metadata.',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [14, 22], 'wording': 'hence or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task; no printed pool of prompts.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.') if 'or otherwise' in t.lower() else None)
p.apply(ROWS, '2021 Ordinary Level Paper 1', ref_overrides={'maths-2021-ol-p1-q8-d': '2021 OL Paper 1 Q8(d), (e)', 'maths-2021-ol-p1-q8-f-i': '2021 OL Paper 1 Q8(f)(i), (ii), (iii)'})
