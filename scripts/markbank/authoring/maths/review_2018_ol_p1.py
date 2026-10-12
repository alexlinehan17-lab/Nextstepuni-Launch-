"""2018 OL Paper 1: a new paper — 37 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'

ROWS = {
 'maths-2018-ol-p1-q1-a': [L(SOL, 'Contract A 35000 + 400000 × 0·02'), L(SOL, '= €43 000'), L(SOL, 'Contract B 30000 + 400000 × 0·03'), L(SOL, '= €42 000'),
     L(LPC, 'Use of 2% or 3%'), L(MPC, '8000 or 12000 or both'), L(HPC, 'One contract correct'), L(NOTE, 'Accept correct answer without work')],
 'maths-2018-ol-p1-q1-b': [L(SOL, '50000 − 35000 = 15000'), L(SOL, '(15000 ÷ 0·02) = €750 000'), L(LPC, '50000 − 35000 formulated or 15000'),
     L(HPC, '15000 × 0·02 or equivalent = 300'), L(NOTE, 'Accept correct answer without work')],
 'maths-2018-ol-p1-q1-c': [L(SOL, '35000 + 0·02x = 30000 + 0·03x'), L(SOL, 'x = €500 000'), L(ALT, '1% = €5000'), L(ALT, 'Answer = €500 000'),
     L(LPC, '35000 − 30000 or 5000 written'), L(LPC, 'correct answer without work'), L(HPC, '35000 + 0·02x = 30000 + 0·03x'), L(HPC, 'x/100 = 5000')],
 'maths-2018-ol-p1-q2-a': [L(SOL, 'z₃ = −2 + 3i + 3 + 2i = 1 + 5i'), L(LPC, 'z₃ = z₁ − z₂ with some substitution'),
     L(LPC, '1 or 2 correct plots (z₁ and/or z₂) without labels'), L(MPC, 'z₃ correct, with or without plotting'),
     L(MPC, '2 correct plots (z₁ and z₂) with labels'), L(HPC, 'Plot of incorrect z₃ and 2 correct plots labelled'),
     L(HPC, 'Mixes up real and imaginary axes but plots and labels 3 points ‘correctly’')],
 'maths-2018-ol-p1-q2-b': [L(SOL, '√13 + √13 ≠ √26'), L(LPC, '|z₁| or |z₂| or |z₃| formulated with some substitution'), L(LPC, 'Correct formula'),
     L(MPC, '|z₁| or |z₂| or |z₃| correct'), L(HPC, '|z₁| and |z₂| and |z₃| correct but no conclusion or incorrect conclusion')],
 'maths-2018-ol-p1-q2-c': [L(SOL, '((−2 + 3i)(−3 + 2i))/((−3 − 2i)(−3 + 2i))'), L(SOL, '= 0 − 1i'), L(LPC, 'Some correct substitution'),
     L(LPC, 'Conjugate identified'), L(LPC, 'Some multiplication above and below by same number, even if incorrect conjugate'),
     L(LPC, 'correct answer without work'), L(HPC, '((−2 + 3i)(−3 + 2i))/((−3 − 2i)(−3 + 2i))')],
 'maths-2018-ol-p1-q3-a': [L(SOL, '= 3·89 or −0·39'), L(LPC, 'correct roots formula'), L(LPC, 'a or b or c identified'),
     L(LPC, 'attempt at factorising'), L(LPC, 'correct answer without work'), L(MPC, 'formula fully substituted'), L(HPC, 'one root calculated'),
     L(HPC, 'x = (7 ± √73)/4 and stops')],
 'maths-2018-ol-p1-q3-b': [L(SOL, '−2a − 3b = −15'), L(SOL, '15a + 3b = −24'), L(SOL, '13a = −39'), L(SOL, 'a = −3 and b = 7'),
     L(LPC, 'effort to equate a or b coefficient in both equations'), L(LPC, 'correct answer without work'), L(MPC, 'eliminates one unknown'),
     L(HPC, '1 unknown found')],
 'maths-2018-ol-p1-q4-a': [L(PC, 'correct diagram, no shading'), L(PC, '5² written')],
 'maths-2018-ol-p1-q4-b': [L(SOL, 'Pattern number (n), Number of Grey Tiles, Number of White Tiles, Total Number of Tiles'), L(SOL, '1, 4, 2, 6'),
     L(SOL, '2, 9, 2, 11'), L(SOL, '3, 16, 2, 18'), L(SOL, '4, 25, 2, 27'), L(SOL, '5, 36, 2, 38'), L(LPC, 'At least 1 correct new entry'),
     L(HPC, 'At least 6 correct or consistent new entries')],
 'maths-2018-ol-p1-q4-c': [L(SOL, '(n + 1)² + 2'), L(SOL, 'n² + 2n + 3'), L(ALT, 'n = 1 ⇒ b + c = 5'), L(ALT, 'n = 2 ⇒ 2b + c = 7'), L(ALT, 'b = 2'),
     L(ALT, 'c = 3'), L(LPC, '(n)² + 2 written and stops or continues'), L(LPC, 'Effort at substitution to derive one equation in a and b'),
     L(LPC, 'correct answer without work'), L(HPC, '(n + 1)² + 2'), L(HPC, '2 relevant equations derived')],
 'maths-2018-ol-p1-q4-d': [L(SOL, 'n² + 2n + 3 = 443'), L(SOL, 'n² + 2n − 440 = 0'), L(SOL, 'n = 20'), L(ALT, '6, 11, 18, ., ., ., 443'), L(ALT, 'n = 20'),
     L(LPC, 'n² + 2n + 3 = 443'), L(LPC, 'effort at trial and error involving any term beyond T5'), L(HPC, 'n² + 2n − 440 = 0'),
     L(HPC, '(21)² + 2 = 443'), L(NOTE, 'Accept n = 20 without work for full marks')],
 'maths-2018-ol-p1-q5-a': [L(SOL, 'A = (0, 6)'), L(SOL, 'B = (−2, 0)'), L(SOL, 'C = (3, 0)'), L(LPC, '1 point correctly identified'),
     L(HPC, '2 points correctly identified'), L(HPC, 'mixes up axes consistently for the 3 points')],
 'maths-2018-ol-p1-q5-b': [L(SOL, 'f(x) = ax² + bx + c'), L(SOL, 'c = 6'), L(SOL, '0 = (−2)²a + b(−2) + 6'), L(SOL, '−6 = 4a − 2b'), L(SOL, '0 = (3)²a + b(3) + 6'),
     L(SOL, '−6 = 9a + 3b'), L(SOL, 'a = −1, b = 1'), L(ALT, '−(x + 2)(x − 3)\n= −x² + x + 6'), L(LPC, 'c = 6'),
     L(LPC, 'substitution of A or B or C into given equation or ax² + bx + c'), L(LPC, '1 factor written'),
     L(HPC, 'substitution of any 2 of A, B, or C into given equation worked out'), L(HPC, 'substitution of A, B, and C into ax² + bx + c'),
     L(HPC, '±(x + 2)(x − 3)'), L(NOTE, 'A, B and C substituted into −x² + x + 6 and fully verified merits full marks')],
 'maths-2018-ol-p1-q5-c': [L(SOL, 'f(x) = −x² + x + 6'), L(SOL, 'f′(x) = −2x + 1 = 0'), L(SOL, 'x = 1/2'), L(SOL, '−(1/2)² + 1/2 + 6 = 6·25'),
     L(LPC, 'any effort at differentiation'), L(LPC, 'states f′(x) = 0'), L(HPC, 'x = 1/2')],
 'maths-2018-ol-p1-q6-a': [L(SOL, '(x + 5)(3x − 4) − 3(x² + 2) + 4 = 0'), L(SOL, '3x² − 4x + 15x − 20 − 3x² − 6 + 4 = 0'), L(SOL, '11x = 22'), L(SOL, 'x = 2'),
     L(LPC, 'any correct multiplication'), L(LPC, 'correct answer without work'), L(HPC, 'multiplication fully correct'),
     L(HPC, 'error in expanding brackets but finishes correctly')],
 'maths-2018-ol-p1-q6-b': [L(SOL, '(2x)(x + 3)(5/(x + 3) − 1/x) = 1/2 (2x)(x + 3)'), L(SOL, '10x − 2(x + 3) = x(x + 3)'), L(SOL, 'x² − 5x + 6 = 0'),
     L(SOL, 'x = 2 and x = 3'), L(LPC, 'common denominator identified'), L(LPC, '5x − (x + 3) or similar'),
     L(LPC, 'correct answer without work, 2 and/or 3'), L(LPC, 'writes (−b ± √((b)² − 4ac))/2a'),
     L(MPC, '10x − 2(x + 3) = x(x + 3) or similar'), L(HPC, 'x² − 5x + 6 = 0 or equivalent')],
 'maths-2018-ol-p1-q7-a': [L(SOL, '37'), L(PC, 'correct number of seats for any row between row 4 and row 9 (inclusive)'), L(NOTE, 'Accept 37 without work')],
 'maths-2018-ol-p1-q7-b': [L(SOL, '28 + (n − 1)1 = 50'), L(SOL, '27 + n = 50'), L(SOL, 'n = 23'), L(ALT, '50 – 37 = 13'), L(ALT, '13 + 10 = 23'),
     L(LPC, 'any evidence of counting (e.g. listing 28, 29,…)'), L(LPC, '13 or 22 without work'), L(LPC, 'writes Tn = a + (n-1)d'),
     L(LPC, 'a or d identified'), L(HPC, '50 – 28 or 50 – 37'), L(HPC, '28 + (n − 1)1 = 50'), L(NOTE, 'Accept 23 without work')],
 'maths-2018-ol-p1-q7-c': [L(SOL, 'S23 = 23/2 [2(28) + (22)(1)]'), L(SOL, 'S23 = 897 (seats)'), L(ALT, '28 + 29 + . . . + 50 = 897'), L(LPC, 'Sn formula written'),
     L(LPC, 'any evidence of counting (e.g. listing 28 + 29 + 30 +…)'), L(LPC, 'a or d identified'),
     L(HPC, 'full listing with addition indicated but incorrect solution'), L(HPC, 'Sn formula fully substituted'), L(NOTE, 'Accept 897 without work')],
 'maths-2018-ol-p1-q7-d': [L(SOL, 'n/2 (56 + n − 1) = 600'), L(SOL, 'n² + 55n − 1200 = 0'), L(SOL, 'n = 16·7'), L(SOL, 'S16 = 568'),
     L(SOL, '600 − 568 = 32 people in next row'), L(ALT, '[28 + 29 + . . .+ 43] = 568\n600 – 568 = 32\n16 rows and 32 in next'),
     L(ALT, '([28 + 29 + . . .+ 44] = 612\n612 – 44 = 568\n600 – 568 = 32\n(17 –1 = 16) rows and 32 in next'), L(LPC, 'Sn formula written'),
     L(LPC, 'a or d identified'), L(LPC, 'any evidence of counting (e.g. listing 28 + 29 + 30 +…)'), L(HPC, 'n² + 55n − 1200 = 0'),
     L(HPC, 'n/2(56 + n − 1) = 600'), L(HPC, 'full listing to 16 or 17 terms with addition indicated but incorrect solution'),
     L(NOTE, 'Accept (16, 32) without work')],
 'maths-2018-ol-p1-q7-e': [L(SOL, '276(25) + 212(12)'), L(SOL, '6900 + 2544 = €9 444'), L(LPC, '276(25)'), L(LPC, '212(12)'),
     L(HPC, '276(25) + 212(12) formulated'), L(NOTE, 'Accept correct answer without work')],
 'maths-2018-ol-p1-q7-f-i': [L(SOL, '752/4 = 188 Children’s tickets'), L(SOL, '188 × 3 = 564 Adult tickets'), L(LPC, '4'), L(LPC, '752/x, x ≠ 4, 1'),
     L(HPC, '188 found or 564'), L(NOTE, 'Accept correct answer without work')],
 'maths-2018-ol-p1-q7-f-ii': [L(SOL, '188x + 564(2·5x) = 17 578'), L(SOL, '1598x = 17 578'), L(SOL, 'x = €11'), L(LPC, 'x, 2·5x'),
     L(LPC, 'correct answer without work'), L(HPC, '188x + 564(2·5x) = 17 578, or consistent with f(i)')],
 'maths-2018-ol-p1-q8-a': [L(SOL, 'C(4) = −(4³) + 4·5(4)² + 54(4)'), L(SOL, '= 224'), L(LPC, 'Function with some substitution of 4'),
     L(HPC, 'Function fully substituted')],
 'maths-2018-ol-p1-q8-b': [L(SOL, '0, 57·5, 118, 175·5, 224, 257·5, 270, 255·5, 208, 121·5'), L(LPC, '1, 2 or 3 correct new entries'),
     L(HPC, '4, 5 or 6 correct new entries')],
 'maths-2018-ol-p1-q8-c': [L(LPC, '1 to 4 correct plots'), L(HPC, '5 to 9 correct plots'), L(HPC, 'all points correctly plotted but incorrect or no joining')],
 'maths-2018-ol-p1-q8-d-i': [L(SOL, '200 units'), L(LPC, '3·5 shown on horizontal axis'), L(HPC, 'correct construction shown but no indication of 200')],
 'maths-2018-ol-p1-q8-d-ii': [L(SOL, '1 hour 45 mins'), L(LPC, '100 clearly indicated on vertical axis'),
     L(HPC, 'correct construction shown but no indication of 1 hour 45 minutes')],
 'maths-2018-ol-p1-q8-e-i': [L(SOL, 'C′(t) = −3t² + 9t + 54'), L(LPC, 'any correct differentiation or indication of differentiation'),
     L(HPC, '2 terms correctly differentiated')],
 'maths-2018-ol-p1-q8-e-ii': [L(SOL, 'C′(4) = −3(4)² + 9(4) + 54'), L(SOL, '= 42 units / hour'), L(LPC, 'some substitution of 4 into C′ or writes C′(4)'),
     L(HPC, 'C′(4) = −3(4)² + 9(4) + 54'), L(NOTE, 'Accept correct or consistent answer without work')],
 'maths-2018-ol-p1-q8-e-iii': [L(SOL, '−3t² + 9t + 54 = 0'), L(SOL, 't² − 3t − 18 = 0'), L(SOL, '(t − 6)(t + 3) = 0'), L(SOL, 't = 6, t = −3'), L(SOL, 't = 6'),
     L(SOL, 'Amount of drug = 270 units'), L(LPC, 'C′(t) = 0'), L(LPC, 'correct answer without work'), L(HPC, 't = 6 from calculus')],
 'maths-2018-ol-p1-q8-e-iv': [L(SOL, 'C′(7) = −3(7)² + 9(7) + 54'), L(SOL, '= −30 units / hour'), L(SOL, 'Rate is negative so the amount of the drug is decreasing'),
     L(LPC, 'some substitution of 7 into C′ or writes C′(7)'), L(MPC, 'C′(7) = −3(7)² + 9(7) + 54'), L(HPC, '−30 units / hour')],
 'maths-2018-ol-p1-q9-a-i': [L(SOL, 's = √(9·8(2000)) = 140'), L(PC, 'Any relevant substitution'), L(NOTE, 'Accept correct answer without work')],
 'maths-2018-ol-p1-q9-a-ii': [L(SOL, '400000/140 = 2857·14 sec'), L(SOL, '= 47·62 mins'), L(SOL, '= 48 mins'), L(LPC, 'use of answer to Part (a)(i)'),
     L(LPC, 'correct answer without work'), L(LPC, '400000 written'), L(HPC, '400000/140')],
 'maths-2018-ol-p1-q9-b-i': [L(SOL, 's² = g × d'), L(SOL, 'd = s²/g'), L(LPC, 'effort to square both sides')],
 'maths-2018-ol-p1-q9-b-ii': [L(SOL, 'd = 55²/9·8'), L(SOL, 'd = 308·67'), L(SOL, 'd = 309'), L(ALT, '55 = √(9·8 × d)'), L(ALT, 'd = 55²/9·8'),
     L(ALT, 'd = 308·67'), L(ALT, 'd = 309'), L(LPC, 'some substitution into either formula'), L(LPC, 'correct answer without work'),
     L(HPC, 'd = 55²/9·8')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Parts whose printed model solution is an image (the Q2(a) Argand diagram, the
# Q4(a) tile diagram, the Q8(c) graph) or loses a stacked fraction's denominator
# (the Q3(a) roots formula over 4, filtered as a mark cell) carry the SEC's own
# print of their scheme row (model solution and every credit band), shown only
# after the reveal. Crops: scheme_row_figures.py; ids are its output.
SCHEME_ROW_FIGURES = {
    'maths-2018-ol-p1-q2-a': 'maths-2018-OL-scheme-p009-i0',
    'maths-2018-ol-p1-q3-a': 'maths-2018-OL-scheme-p010-i0',
    'maths-2018-ol-p1-q4-a': 'maths-2018-OL-scheme-p011-i0',
    'maths-2018-ol-p1-q8-c': 'maths-2018-OL-scheme-p017-i0',
}

p = Paper(2018, 'ol', 'p1', {'5B': [0, 3, 5], '5C': [0, 3, 4, 5], '5D': [0, 2, 3, 4, 5], '10C': [0, 3, 8, 10], '10D': [0, 2, 6, 8, 10],
                             '15C': [0, 4, 12, 15], '15D': [0, 3, 7, 13, 15]},
          'LC003GLP100EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
fm = 'financial-maths'
sal = 'When Sean joined a sales company he was offered a choice of two different salary contracts. The details of the contracts are outlined in the table below. Contract A: salary €35 000, end of year commission on total sales 2%. Contract B: salary €30 000, end of year commission on total sales 3%.'
A('1-a', 'Q1(a)', '10D', [8], [3], '3-3', fm, 'Find how much Sean would earn under each contract in a year where his total sales were €400 000.', stem=sal)
A('1-b', 'Q1(b)', '5C', [8], [3], '3-3', fm, 'Another employee, Mary, earned €50 000 in a particular year. She is on Contract A. Find her total sales for that year.', stem=sal)
A('1-c', 'Q1(c)', '10C', [8], [3], '3-3', fm + ',algebra-equations', 'Find the total sales for which a salesperson would earn the same amount of money under each contract.', stem=sal)
zz = 'z₁ = −2 + 3i and z₂ = −3 − 2i, where i² = −1. z₃ = z₁ − z₂.'
cx = 'complex-numbers'
A('2-a', 'Q2(a)', '15D', [9], [4], '4-4', cx, 'Plot z₁, z₂, and z₃ on the Argand Diagram. Label each point clearly.', stem=zz)
A('2-b', 'Q2(b)', '5D', [9], [4], '4-4', cx, 'Investigate if |z₃| = |z₁| + |z₂|.', stem=zz)
A('2-c', 'Q2(c)', '5C', [9], [4], '4-4', cx, 'z₄ = z₁/z₂. Write z₄ in the form x + yi, where x, y ∈ ℝ.', stem=zz)
ae = 'algebra-equations'
A('3-a', 'Q3(a)', '10D', [10], [5], '4-2', ae, 'Solve the equation 2x² − 7x − 3 = 0. Give each answer correct to 2 decimal places.')
A('3-b', 'Q3(b)', '15D', [10], [5], '4-2', ae, 'Solve the simultaneous equations below to find the value of a and the value of b. 2a + 3b = 15; 5a + b = −8.')
tl = 'The first three stages in a pattern of grey and white tiles are shown in the diagram below.'
q4c = 'Assuming the pattern continues, the total number of tiles in stage n (Tₙ) is given by the formula Tₙ = n² + bn + c, where b and c ∈ ℕ. Find the value of b and the value of c.'
ss = 'sequences-series'
A('4-a', 'Q4(a)', '5B', [11], [6], '4-1', ss, 'Draw the next stage of tiles (Stage 4) onto the diagram above.', stem=tl)
A('4-b', 'Q4(b)', '5C', [11], [6], '4-1', ss, 'Based on the pattern shown, complete the table below. Stage (n): 1, 2, 3, 4, 5. Number of Grey Tiles: 4, _, _, _, _. Number of White Tiles: _, _, _, _, _. Total: 6, _, _, _, _.', stem=tl)
A('4-c', 'Q4(c)', '5C', [12], [6, 7], '4-1', ss + ',algebra', q4c, stem=tl)
A('4-d', 'Q4(d)', '10C', [12], [6, 7], '4-2', ss + ',' + ae, 'Find the number of the stage which has 443 tiles in total.', stem=tl + ' Part (c): ' + q4c)
qf = 'The diagram on the right shows the graph of a quadratic function, f.'
A('5-a', 'Q5(a)', '5C', [13], [8], '5-1', 'graphing-functions', 'Write down the co-ordinates of A, B, and C.', stem=qf)
A('5-b', 'Q5(b)', '10C', [13], [8], '5-1', 'functions,' + ae, 'Show that the function can be written as f(x) = −x² + x + 6.', stem=qf)
A('5-c', 'Q5(c)', '10C', [13], [8], '5-2', 'differentiation', 'Show, using calculus, that the maximum point of f(x) is (0·5, 6·25).', stem=qf + ' Part (b): Show that the function can be written as f(x) = −x² + x + 6.')
A('6-a', 'Q6(a)', '10C', [14], [9], '4-2', ae, 'Solve for x. (x + 5)(3x − 4) − 3(x² + 2) + 4 = 0')
A('6-b', 'Q6(b)', '15D', [14], [9], '4-2', ae, 'Find the solutions of 5/(x + 3) − 1/x = 1/2 where x ≠ −3, 0, x ∈ ℝ.')
th = 'Part of the seating arrangement in a theatre is shown in the diagram below. The seats are arranged in rows. Row 1 is nearest the stage and has 28 seats. Each subsequent row behind that contains one more seat. i.e. row 2 has 29 seats, row 3 has 30 seats, and so on.'
q7b = 'There are 50 seats in the last row. How many rows of seats are there in the theatre?'
q7fi = 'For a different show 752 tickets were sold. The ratio of adult tickets sold to children’s tickets sold is 3 : 1. Find how many adult tickets and how many children’s tickets were sold for that show.'
ns = 'number-systems'
A('7-a', 'Q7(a)', '5B', [15], [10], '4-1', ss, 'Find the number of seats in row 10.', stem=th)
A('7-b', 'Q7(b)', '10C', [15], [10], '4-1', ss, q7b, stem=th)
A('7-c', 'Q7(c)', '10C', [15], [10], '4-1', ss, 'Find the total number of seats in the theatre.', stem=th + ' Part (b): ' + q7b)
A('7-d', 'Q7(d)', '10C', [16], [10], '4-1', ss + ',' + ae, 'On a particular night 600 people are at a show in the theatre. Assume that people are seated only in the rows closest to the stage, i.e. they have filled the first n rows and there are some people seated in the next row. Find the value of n and find the number of people seated in the next row.', stem=th)
A('7-e', 'Q7(e)', '5C', [16], [10, 11], '3-3', ns, 'For a particular show, adult tickets cost €25 each and children’s tickets cost €12 each. Find the total income from ticket sales if 276 adult tickets and 212 children’s tickets were sold.', stem=th)
A('7-f-i', 'Q7(f)(i)', '5C', [16], [10, 11], '3-3', ns, q7fi, stem=th)
A('7-f-ii', 'Q7(f)(ii)', '10C', [16], [10, 11], '3-3', ns + ',' + ae, 'For the show referred to in part f(i) an adult ticket cost 2½ times as much as a children’s ticket. The income was €17 578. Find the cost of a children’s ticket for this show.', stem=th + ' Part (f)(i): ' + q7fi)
dr = 'The amount, in appropriate units, of a certain medicinal drug in the bloodstream t hours after it has been taken can be estimated by the function: C(t) = −t³ + 4·5t² + 54t, where 0 ≤ t ≤ 9, t ∈ ℝ.'
tab = 't (Hours): 0, 1, 2, 3, 4, 5, 6, 7, 8, 9. C(t) (Units): 0, 57·5, _, _, 224, _, _, _, _, _.'
q8c = 'Draw the graph of the function C(t) for 0 ≤ t ≤ 9 where t ∈ ℝ.'
q8ei = 'Use the drug amount function C(t) = −t³ + 4·5t² + 54t to find, in terms of t, the rate at which the drug amount is changing after t hours.'
dd = 'Use your graph to estimate each of the following values. In each case show your work on the graph above.'
A('8-a', 'Q8(a)', '10C', [17], [12], '5-1', 'functions', 'Use the drug amount function, C(t), to show that the amount of the drug in the bloodstream 4 hours after the drug has been taken is 224 units.', stem=dr)
A('8-b', 'Q8(b)', '10C', [17], [12], '5-1', 'functions', 'Use the function C(t) to complete the table below. ' + tab, stem=dr)
A('8-c', 'Q8(c)', '5C', [17], [12, 13], '5-1', 'graphing-functions', q8c, stem=dr + ' Part (b): Use the function C(t) to complete the table below. ' + tab)
A('8-d-i', 'Q8(d)(i)', '5C', [18], [12, 13], '5-1', 'graphing-functions', dd + ' The amount of the drug in the bloodstream after 3½ hours.', stem=dr + ' Part (c): ' + q8c)
A('8-d-ii', 'Q8(d)(ii)', '10C', [18], [12, 13], '5-1', 'graphing-functions', dd + ' How long after taking the drug will the amount of the drug in the bloodstream be 100 units?', stem=dr + ' Part (c): ' + q8c)
A('8-e-i', 'Q8(e)(i)', '10C', [18], [12, 14], '5-2', 'differentiation', q8ei, stem=dr)
A('8-e-ii', 'Q8(e)(ii)', '5C', [18], [12, 14], '5-2', 'differentiation', 'Use your answer to part e(i) to find the rate at which the drug amount is changing after 4 hours.', stem=dr + ' Part (e)(i): ' + q8ei)
A('8-e-iii', 'Q8(e)(iii)', '5C', [19], [12, 14], '5-2', 'differentiation', 'Use your answer to part e(i) to find the maximum amount of the drug in the bloodstream over the first 9 hours.', stem=dr + ' Part (e)(i): ' + q8ei)
A('8-e-iv', 'Q8(e)(iv)', '5D', [19], [12, 14], '5-2', 'differentiation', 'Use your answer to part e(i) to show that the drug amount in the bloodstream is decreasing 7 hours after the drug has been taken. Explain your reasoning.', stem=dr + ' Part (e)(i): ' + q8ei)
ts = 'When earthquakes occur under the sea, they can cause large tidal waves called tsunamis. Scientists can estimate the arrival times of tsunamis to nearby countries. The average speed at which a tsunami travels is given by the formula: s = √(g × d) where s is the speed of the tsunami (in metres per second), d is the depth of the ocean (in metres) at the location where the earthquake occurred, and g = 9·8 metres per second².'
q9ai = 'Find s, the speed of a tsunami when the an earthquake occurs at a depth of 2000 m. Give your answer in metres per second.'
A('9-a-i', 'Q9(a)(i)', '5B', [20], [15], '3-3', ns, q9ai, stem=ts)
A('9-a-ii', 'Q9(a)(ii)', '5C', [20], [15], '3-3', ns, 'A tsunami has been identified as beginning 400 km from land. The depth of the ocean at that point is 2000 m. Find how long it will take this tsunami to reach land. Give your answer correct to the nearest minute.', stem=ts + ' Part (a)(i): ' + q9ai)
A('9-b-i', 'Q9(b)(i)', '5B', [20], [15], '4-1', 'algebra', 'Rearrange the formula to give d in terms of g and s.', stem=ts)
A('9-b-ii', 'Q9(b)(ii)', '15C', [20], [15], '4-2', ae, 'Hence, or otherwise, find the depth of the ocean at the place where an earthquake occurred, if the resulting tsunami has a speed of 55 metres per second. Give your answer correct to the nearest metre', stem=ts + ' Part (b)(i): Rearrange the formula to give d in terms of g and s.')

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 55, '8': 65, '9': 30}
p.check(marks, 37)
p.review(marks,
    'Independent visual reading of all 16 question-paper pages and PDF pages 1–21 of the combined Ordinary Level scheme (cover, notes, contents, the Paper 1 title page 5, the scale table on page 6, the summary of mark allocations on page 7, every Paper 1 model solution and marking note on pages 8–20, and the Paper 2 title page 21). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 22)), [6, 7],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 55 marks, Q8 65 marks, Q9 30 marks). Every question is retained.',
     '37 independently marked units, matching the printed summary of allocations on scheme page 7.',
     'Paper 1 bands from the 2018 Ordinary scale table on scheme page 6: 5B 0,3,5; 5C 0,3,4,5; 5D 0,2,3,4,5; 10C 0,3,8,10; 10D 0,2,6,8,10; 15C 0,4,12,15; 15D 0,3,7,13,15. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 37 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; the scheme’s bullets are not reproduced. Q9(b)(i) prints “Low Partial Credit” on its 5B scale and is labelled as printed. Two alternative methods in Q7(d) are quoted as one multi-line point each to stay within the row limit.',
     'Four parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because the model solution is an image (the Q2(a) Argand diagram, the Q4(a) tile diagram, the Q8(c) graph) or its roots formula loses the denominator 4 to the mark-cell filter (Q3(a)).',
     'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 10], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [15], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2018 Ordinary Level Paper 1', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()})
