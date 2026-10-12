"""2018 HL Paper 2: a new paper — 32 scale units, all added."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
ALT = 'Model solution (alternative)'
M12, M2, M3 = 'Methods 1 and 2, ', 'Method 2, ', 'Method 3, '

ROWS = {
 'maths-2018-hl-p2-q1-a': [L(SOL, '1/20 (9000) + 1/10 (7000) + 1/4 (3000)'), L(SOL, '= 1900'), L(SOL, 'E(x) = 2000 − 1900 = 100'),
     L(ALT, 'E(x) = 1/20 (−7000) + 1/10 (−5000) + 1/4 (−1000) + 3/5 (2000)'), L(ALT, '= −350 − 500 − 250 + 1200 = 100'),
     L(SOL, 'So expected gain for organisers of competition and therefore a loss for Mary of 100'),
     L(LPC, 'E(x) partially formulated (1 or 2 terms)'), L(HPC, 'E(x) fully formulated (sum of all three/all four terms)')],
 'maths-2018-hl-p2-q1-b': [L(SOL, '1/20 (9000 + x) + 1/10 (7000 + x)'), L(SOL, '+ 1/4 (3000 + x) = 2000'), L(SOL, '(1900 + 8/20 x) = 2000\n8/20 x = 100\nx = 250'),
     L(ALT, 'From (a) to break even it will take €100.\nx/20 + x/10 + x/4 = 100\n(x + 2x + 5x)/20 = 100'),
     L(ALT, 'E(x) = 1/20 (−7000 − x) + 1/10 (−5000 − x) + 1/4 (−1000 − x) + 3/5 (2000) = 0'),
     L(ALT, '−7000 − x − 10 000 − 2x − 5000 − 5x + 24 000 = 0\n2000 = 8x ⇒ 250 = x'),
     L(M12 + LPC, 'Any relevant use of x, excluding (9000 + x)'), L(M12 + MPC, 'E(x) fully formulated (LHS).'),
     L(M12 + MPC, '(1900 + 8/20 x) or equivalent and stops.'), L(M12 + MPC, 'x/20 + x/10 + x/4'), L(M12 + HPC, 'Relevant equation in x'),
     L(M3 + LPC, 'Any relevant use of x e.g. (−7000 + x)'), L(M3 + MPC, 'E(x) fully formulated (LHS).'),
     L(M3 + MPC, '(100 − 8/20 x) or equivalent and stops.'), L(M3 + HPC, 'Relevant equation in x')],
 'maths-2018-hl-p2-q2-a': [L(SOL, 'P(z < z₁) = 0·67'), L(SOL, 'z = 0·44'), L(PC, 'P(z < z₁) = 0·67')],
 'maths-2018-hl-p2-q2-b-i': [L(SOL, 'Mary Maths (65 − 70)/15 = −1/3'), L(SOL, 'Mary English (68 − 72)/10 = −2/5'), L(SOL, '−1/3 > −2/5'),
     L(SOL, 'Mary did better in Maths'), L(SOL, 'Justification: −1/3 > −2/5'), L(LPC, 'Relevant formula with some correct substitution'),
     L(LPC, '(65 − 70)/15 or (68 − 72)/10.'), L(HPC, '(65 − 70)/15 and (68 − 72)/10')],
 'maths-2018-hl-p2-q2-b-ii': [L(SOL, 'P(z > z₁) = 0·15'), L(SOL, 'z = (x − 72)/10 = 1·04'), L(SOL, 'x = 82·4%'), L(SOL, 'x = 83'),
     L(LPC, '0·15'), L(LPC, '1·04'), L(LPC, 'Relevant formula with some correct substitution'), L(HPC, 'Relevant equation in x')],
 'maths-2018-hl-p2-q2-b-iii': [L(SOL, '82 is 1 st. dev. above mean ⇒ ≈ 68/2% above'), L(SOL, '52 is 2 st. dev. below mean ⇒ ≈ 95/2% below'),
     L(SOL, '34 + 47·5 = 81·5%'), L(ALT, 'From tables: 82 is 1 deviation off mean ⇒ 0·6826/2 = 0·3413'),
     L(ALT, '52 is 2 dev. off mean ⇒ 0·9544/2 = 0·4772'), L(ALT, '0·3413 + 0·4772 = 0·8185 = 81·85%'),
     L(ALT, 'z = (52 − 72)/10 = −2 z = (82 − 72)/10 = 1'), L(ALT, 'P(−2 < z < 1)\nP(z < 1) − [1 − P(z < 2)]'),
     L(ALT, '0·8413 – [1 – 0·9772] = 0·8185 = 81·85%'),
     L(LPC, 'Evidence of relevant linking of deviation and mean.'), L(LPC, '68/2 or 95/2'), L(LPC, '(52 − 72)/10 or (82 − 72)/10'),
     L(LPC, '0·6826/2 or 0·9544/2'), L(HPC, '68/2 and 95/2'), L(HPC, '(52 − 72)/10 and (82 − 72)/10'), L(HPC, '0·6826/2 and 0·9544/2')],
 'maths-2018-hl-p2-q3-a-i': [L(SOL, '10⁵ × 1 or 100 000'), L(LPC, 'Some use of 10.'), L(LPC, 'Identifies that 5 other digits are required to complete code.'),
     L(HPC, '9⁵ or equivalent'), L(HPC, '10⁶')],
 'maths-2018-hl-p2-q3-a-ii': [L(SOL, '1 × 10 × 10 + 10 × 1 × 10 + 10 × 10 × 1'), L(SOL, '3 × 10 × 10 or 3 × 10² or 300'), L(PC, '10 × 10')],
 'maths-2018-hl-p2-q3-b': [L(SOL, '(n + 3)! (n + 2)!/((n + 1)! (n + 1)!) ='), L(SOL, '(n + 3)(n + 2)(n + 2) ='), L(SOL, 'n³ + 7n² + 16n + 12'),
     L(ALT, '(n + 3)! (n + 2)!/((n + 1)! (n + 1)!) = an³ + bn² + cn + d'), L(ALT, 'n = 0 → 3! .2!/(1! 1!) = 12 = d'),
     L(ALT, 'n = 1 → a + b + c + d = 36'), L(ALT, 'n = 2 → 8a + 4b + 2c + d = 80'), L(ALT, 'n = 3 → 27a + 9b + 3c + d = 150'),
     L(ALT, 'Solving the simultaneous equations a = 1, b = 7, c = 16, d = 12'),
     L(LPC, 'Factorial expansion (e.g. (n + 3)! = (n + 3)(n + 2)(n + 1) … … … .1)'),
     L(LPC, 'Effort at a numerical value for n on both LHS and RHS (method 2)'), L(HPC, '(n + 3)(n + 2)(n + 2)'), L(HPC, 'Four simultaneous equations')],
 'maths-2018-hl-p2-q4-a': [L(SOL, '2x = 150 + 360n or 2x = 210 + 360n'), L(SOL, 'x = 75 + 180n'), L(SOL, 'x = 105 + 180n'), L(SOL, 'n = 0 ⟹ x = 75°'),
     L(SOL, 'n = 0 ⟹ x = 105°'), L(SOL, 'n = 1 ⟹ x = 255°'), L(SOL, 'n = 1 ⟹ x = 285°'), L(LPC, '30° or 150° or 210°'), L(HPC, '2 relevant values of x')],
 'maths-2018-hl-p2-q4-b': [L(SOL, '2² = y² + z²'), L(SOL, 'z = √(4 − y²)'), L(SOL, 'sin 2A = 2 sin A cos A'), L(SOL, '2(√(4 − y²)/2)(y/2)'),
     L(SOL, '= y√(4 − y²)/2'), L(ALT, 'sin 2A = 2 tan A/(1 + tan² A)'), L(ALT, '= 2y√(4 − y²)/(y² + 4 − y²) = y√(4 − y²)/2'),
     L(LPC, '√(4 − y²)'), L(LPC, '2 sin A cos A without substitution'), L(LPC, 'sin 2A expressed in tan A format'),
     L(LPC, 'Relevant labelled diagram (2, y, A)'), L(HPC, 'Substitution for sin A or cos A in formula'), L(HPC, 'sin A = (√(4 − y²)/2)'),
     L(HPC, 'tan A = √(4 − y²)/y')],
 'maths-2018-hl-p2-q5-a': [L(SOL, '2(−2) + 3(1) + 1 = 0 or −4 + 3 + 1 = 0'), L(LPC, 'Substitution for x or y in equation of line'),
     L(HPC, 'Substitution for x and y in eq. of line (LHS when no indication of 0)')],
 'maths-2018-hl-p2-q5-b': [L(SOL, 'Slope of m or n = −2/3\nSlope of AB is 3/2 and (–2, 1) is on AB'), L(SOL, 'y − 1 = 3/2 (x − (−2))\nequation of AB is 3x − 2y + 8 = 0'),
     L(SOL, 'Solve for (x, y) between 3x − 2y + 8 = 0 and 2x + 3y − 51 = 0\nn ∩ AB = (6, 13) = B'),
     L(ALT, 'coordinates of B(x, y)\n|AB| = √((x + 2)² + (y − 1)²)\nPerp. distance (–2, 1) to 2x + 3y − 51 = 0'),
     L(ALT, '|−4 + 3 − 51|/√13 = 52/√13 = 4√13\n∴ (x + 2)² + (y − 1)² = (4√13)²'),
     L(ALT, 'Substituting x = 1/2(−3y + 51)\n((−3y + 55)/2)² + (y − 1)² = (4√13)²\n13y² − 338y + 2197 = 0\ny² − 26y + 169 = 0\n(y − 13)² = 0 → y = 13'),
     L(LPC, 'Slope of AB'), L(LPC, 'Equation of line formula with some substitution'), L(MPC, 'Equation of AB'),
     L(HPC, 'Effort at finding intersection of lines'),
     L(NOTE, 'Point of intersection, found correctly, of n and a relevant AB (with errors) merits Mid Partial Credit at least.'),
     L(M2 + LPC, 'Perpendicular distance formula with some substitution'), L(M2 + LPC, 'Distance formula with some substitution'),
     L(M2 + MPC, 'Quadratic equation in x and y'), L(M2 + HPC, 'Quadratic equation in either x or y')],
 'maths-2018-hl-p2-q5-c': [L(SOL, 'AB⃗ = x up 8 and y up 12\nCentre of s is 1/8(8) − 2 = −1 = ℎ and 1/8(12) + 1 = 2·5 = k\nEqn s: (x + 1)² + (y − 2·5)² = (√13/2)²'),
     L(ALT, 's ∩ t ((3(−2) + 1(6))/(3 + 1), (3(1) + 1(13))/(3 + 1)) = (0, 4)\nCentre s: ((0 − 2)/2, (4 + 1)/2) = (−1, 2·5)\nRadius : distance (−1, 2·5) to either (−2, 1) or (0, 4) or calculated otherwise √3·25 or √13/2\n(x + 1)² + (y − 2·5)² = (√13/2)²'),
     L(ALT, 'using ratio 1 : 7 centre s: ((1(6) + 7(−2))/(1 + 7), (1(13) + 7(1))/(1 + 7)) = (−1, 2·5)\nRadius as above or (1/8)|AB| = √13/2\n(x + 1)² + (y − 2·5)² = (√13/2)²'),
     L('Method 1, ' + LPC, '8 up or 12 up'), L('Method 1, ' + LPC, 'Indication 4√13 from(b) of relevance'),
     L('Method 1, ' + HPC, 'Centre and radius of circle'), L(M2 + LPC, 'Some relevant use of 1 : 3'),
     L(M2 + LPC, 'Midpoint of AB found once but no further work of relevance'), L(M2 + LPC, 'Formula with some relevant substitution'),
     L(M2 + HPC, 'Centre and radius of circle'), L(M3 + LPC, 'Some relevant use of 1 : 7'), L(M3 + LPC, 'Formula with some relevant substitution'),
     L(M3 + HPC, 'Centre and radius of circle')],
 'maths-2018-hl-p2-q6-a': [L(SOL, 'Given: A triangle ABC and a line XY parallel to BC which cuts AB in the ratio s : t where s, t ∈ ℕ.'),
     L(SOL, 'To Prove: [AY] : [YC] = s : t'),
     L(SOL, 'Construction: Divide [AB] into s +t equal parts, s of them lying along [AX] and t of them lying along [XB]. Through each point of division draw a line parallel to [BC]'),
     L(SOL, 'Proof: By a previous theorem the parallel lines cut off segments of equal length along [AC]. Therefore [AC] is divided into s + t equal parts with s of them forming [AY] and t of them forming [YC].'),
     L(SOL, 'Let k be the length of one segment on [AC].'), L(SOL, '[AY] : [YC] = ks : kt = s : t'),
     L(LPC, 'Relevant diagram drawn'), L(MPC, 'Construction clearly indicated'), L(HPC, 'Proof missing 1 relevant step')],
 'maths-2018-hl-p2-q6-b': [L(SOL, '|XY| = √(4² + 3²) = 5'), L(SOL, '|ZC| = 5'), L(SOL, '|BZ| = 10cm'), L(ALT, '8/4 or 2/1 = |BZ|/5 → |BZ| = 10cm'),
     L(ALT, '4/12 = 5/(5 + |BZ|)'), L(ALT, '4|BZ| + 20 = 60 → |BZ| = 10 cm'), L(ALT, 'Similarly: 3/9 = 5/(5 + |BZ|)'),
     L(LPC, '|XY| or |BX| or |CY| found'), L(LPC, 'Pythagoras with some substitution'), L(HPC, '|ZC| or |BC| found'),
     L(HPC, 'Ratios formulated with |BZ| the sole unknown')],
 'maths-2018-hl-p2-q7-a': [L(SOL, 'V = 4/3 π3³ = 36π = 113·1'), L(SOL, '113·1(1 − 1·75⁵)/(1 − 1·75) = 2324·29'), L(SOL, '= 2324'),
     L(ALT, 'Volume A = 113·1'), L(ALT, 'Volume B = 197·925'), L(ALT, 'Volume C = 346·36875'), L(ALT, 'Volume D = 606·1453125'),
     L(ALT, 'Volume E = 1060·754296875'), L(ALT, 'Total: 2324·293359375 = 2324'), L(LPC, 'Volume formula with some substitution'),
     L(MPC, 'Volume of 2 spheres'), L(MPC, 'GP formula with some substitution'), L(HPC, 'Volume of 5 spheres'), L(HPC, 'G P formula fully substituted')],
 'maths-2018-hl-p2-q7-b-i': [L(SOL, '4πr² = 503 ⇒ r = √(503/4π) = 6·33'), L(SOL, 'Height = 120 − 2(6·33) = 107·3'),
     L(ALT, '4/3 πr³ = 1060·754 from(a)'), L(ALT, 'r = 6·326'), L(ALT, 'Height : 120 − 2(6·326) = 107·348 = 107·3'),
     L(LPC, '4πr² = 503'), L(LPC, '4/3 πr³ = volume from (a)'), L(HPC, 'r found')],
 'maths-2018-hl-p2-q7-b-ii': [L(SOL, 'A: π1²ℎ = 71·3π ⇒ ℎ = 71·3'), L(SOL, 'Height difference: 107·3 − 71·3 = 36'), L(SOL, '36/4 = 9 step up in each bar.'),
     L(ALT, 'T5 = 71·3 + 4d = 107·3 → d = 9'), L(SOL, 'Height of each bar (in cm) 71·3, 80·3, 89·3, 98·3, 107·3'),
     L(LPC, 'Vol formula with some substitution'), L(LPC, 'πr²ℎ = 71·3π'), L(MPC, 'Height of bar A'),
     L(HPC, 'Difference in height between bar A and bar E')],
 'maths-2018-hl-p2-q7-c': [L(SOL, '150 − (20 + 20 + 9(2)) = 92'), L(SOL, '92/8 cm or 11·5 cm'), L(LPC, 'Recognises 8 equal divisions'),
     L(LPC, 'Indicates subtraction of one relevant length'), L(LPC, '9 × 2'), L(HPC, '150 − 40 − 18 or equivalent')],
 'maths-2018-hl-p2-q7-d': [L(SOL, 'VB = 1·75 (4/3 π3³) = 63π'), L(SOL, 'VB = 4/3 πr³ = 63π => rb = 3·62 cm'), L(SOL, '|XY| = 1 + 11·5 + 1 = 13·5'),
     L(SOL, '|ZW| = (9 − 3) + 3·62 = 9·62'), L(SOL, '|TW| = √(13·5² + 9·62²) = 16·576'),
     L(ALT, 'tan∠WTZ = 9·62/13·5 → |∠WTZ| = 35·459°'), L(ALT, 'cos∠WTZ = 13·5/|TW| → |TW| = 16·576'),
     L(SOL, 'The rod is: |TW| − 3 − 3·62'), L(SOL, '= 16·576 − 3 − 3·62 = 9·95'), L(SOL, '|TW| = 10'),
     L(PC, 'VB formulated with some substitution'), L(PC, '|XY| formulated'), L(PC, '|TW| evaluated'),
     L(PC, 'rod = |TW| − rb − ra formulated with 2 relevant values')],
 'maths-2018-hl-p2-q8-a-i': [L(SOL, 'z₁ = (4·6 − 4·64)/(0·12/√10) = −1·05409'), L(SOL, 'z₂ = (4·7 − 4·64)/(0·12/√10) = 1·581138'),
     L(SOL, 'p(−1·05 < z < 1·58)'), L(SOL, '= 0·9429 − (1 − 0·8531)'), L(SOL, '= 0·796'), L(SOL, 'or 79·6%'),
     L(LPC, 'z₁ formulated with some correct substitution'), L(LPC, 'z₂ formulated with some correct substitution'),
     L(MPC, 'z₁ and z₂ fully substituted'), L(HPC, '–1·05 and 1·58 or equivalents')],
 'maths-2018-hl-p2-q8-a-ii': [L(SOL, 'Confidence Interval: p̂ ± 1·96√(p̂(1 − p̂)/n)'),
     L(SOL, '0·81 − 1·96√(0·81 × 0·19/400) ≤ p'), L(SOL, '≤ 0·81 + 1·96√(0·81 × 0·19/400)'), L(SOL, '0·77155 ≤ p ≤ 0·848445'), L(SOL, '0·77 ≤ p ≤ 0·85'),
     L(LPC, 'CI formulated with some correct substitution'), L(LPC, '1·96'), L(LPC, 'p̂ ± 1/√n incomplete or completed'), L(HPC, 'CI fully substituted')],
 'maths-2018-hl-p2-q8-b-i': [
     L(SOL + ', Always True', '1. When forming confidence intervals (for fixed n and p̂), an increased confidence level implies a wider interval.'),
     L(SOL + ', Sometimes True', '2. As the value of p̂ increases (for fixed n), the estimated standard error of the population proportion increases.'),
     L(SOL + ', Always True', '3. As the value of p̂(1 − p̂) increases (for fixed n), the estimated standard error of the population proportion increases.'),
     L(SOL + ', Never True', '4. As n, the number of people sampled, increases (for fixed p̂), the estimated standard error of the population proportion increases.'),
     L(LPC, 'Any 1 correct'), L(HPC, 'Any 2 correct')],
 'maths-2018-hl-p2-q8-b-ii': [L(SOL, 'M = p̂ − p̂²'), L(SOL, 'dM/dp̂ = 1 − 2p̂'), L(SOL, 'dM/dp̂ = 1 − 2p̂ = 0'), L(SOL, 'p̂ = 1/2'),
     L(SOL, 'Mmax = 1/2 − 1/4 = 1/4'), L(ALT, 'f(p) = p̂ − p̂² = −(p̂² p̂)'), L(ALT, '= −[(p̂² − p̂ + (−1/2)²) − (−1/2)²]'),
     L(ALT, '= 1/4 − (p̂ − 1/2)²'), L(ALT, 'p̂ = 1/2 Mmax = 1/2 − 1/4 = 1/4'),
     L(SOL, '1·96√(p̂(1 − p̂)/n) = 1·96√(1/4n) = 0·03464 = 3·46%'), L(LPC, 'Any relevant calculus'), L(LPC, '1/√n = 1/√800'),
     L(LPC, 'Effort at completing the square'), L(MPC, 'p̂ = 1/2 or equivalent'), L(HPC, 'Maximum value')],
 'maths-2018-hl-p2-q8-c': [L(SOL, '20 000 + 20 000(1·01)/1·024 + 20 000(1·01²)/1·024² + 20 000(1·01³)/1·024³ + ⋯ + 20 000(1·01²⁵)/1·024²⁵'),
     L(SOL, '20 000 [1 + 1·01/1·024 + 1·01²/1·024² + 1·01³/1·024³ + ⋯ + 1·01²⁵/1·024²⁵]'), L(SOL, 'a = 1, r = 1·01/1·024 = 505/512, n = 26'),
     L(SOL, '= €440 132·40'), L(LPC, '20000(1·01) or 20000/1·024'),
     L(MPC, '20 000(1·01)/1·024 or similar term'),
     L(MPC, 'Correctly handles inflation element or completes correctly present values element and finishes'),
     L(HPC, 'GP with a, r and n identified'), L(NOTE, 'Treat n = 25 as a misreading')],
 'maths-2018-hl-p2-q9-a': [L(SOL, '10/sin 15 = 30/sin x'), L(SOL, 'sin x = 30 sin 15/10'), L(SOL, 'sin x = 0·77645'), L(SOL, 'x = 51°'),
     L(LPC, 'Sine rule formulated with some substitution'), L(HPC, 'sin x')],
 'maths-2018-hl-p2-q9-b-i': [L(SOL, 'period = 2π Range = [10, 30]'), L(LPC, 'Period or range correct'), L(HPC, 'Period correct and range partly correct'),
     L(HPC, 'Period and range in incorrect order')],
 'maths-2018-hl-p2-q9-b-ii': [L(SOL, '30, 18·28, 10, 18·28, 30'), L(LPC, '1 correct new value'), L(HPC, '2 correct new values')],
 'maths-2018-hl-p2-q9-b-iii': [L(LPC, '1 point from table plotted'), L(HPC, '3 points from table plotted')],
 'maths-2018-hl-p2-q9-b-iv': [L(SOL, 'Answer: diagram 2'), L(SOL, 'refer to the steepness of their graph at the three corresponding points'),
     L(SOL, 'or rely on the original geometry of the situation: the closer ∠CDO is to a right angle the more the connecting rod will get pulled or pushed by a small change in the crank angle'),
     L(PC, 'Diagram 2 identified but without reason or with invalid reason')],
 'maths-2018-hl-p2-q9-c': [L(SOL, 'r² = 36² + (31 + r)² − 2(36)(31 + r) cos 10°'), L(SOL, 'r² = 1296 + 961 + 62r + r² − (2232 cos 10° − 72r cos 10°)'),
     L(SOL, '8·906r = 58·91'), L(SOL, 'r = 6·62\nr = 7'), L(ALT, '|BX|² = 36² + 31² − 2 × 36 × 31cos10°'), L(ALT, '|BX|² = 58·91'),
     L(ALT, '|BX| = 7·675'), L(ALT, 'sin 10°/7·675 = sin ∠BXA/36'), L(ALT, '∠BXA = 125·462° ⇒ ∠BXO = 54·53795°'),
     L(ALT, 'ΔBXO is isosceles ⇒ ∠BOX = 70·924°'), L(ALT, 'sin 70·924°/7·675 = sin 54·53795°/r'), L(ALT, 'r = 6·6145\nr = 7'),
     L(LPC, 'Cosine rule formulated with some substitution'), L(LPC, '(31 + r)'), L(HPC, 'Relevant equation in r')],
}
assert all(len(v) <= 16 for v in ROWS.values()), [k for k, v in ROWS.items() if len(v) > 16]
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

# Parts whose printed model solution cannot be lifted as text -- a diagram or graph
# the working refers to, the tick table of Q8(b)(i), or a line whose stacked-fraction
# digits extract as lone numerals (filtered as mark cells) -- carry the SEC's own
# print of their scheme row (model solution and every credit band), shown only
# after the reveal. Crops: scheme_row_figures.py; ids are its output.
SCHEME_ROW_FIGURES = {
    'maths-2018-hl-p2-q4-b': 'maths-2018-HL-scheme-p031-i0',
    'maths-2018-hl-p2-q6-a': 'maths-2018-HL-scheme-p034-i0',
    'maths-2018-hl-p2-q7-d': 'maths-2018-HL-scheme-p037-i0',
    'maths-2018-hl-p2-q8-b-i': 'maths-2018-HL-scheme-p039-i0',
    'maths-2018-hl-p2-q8-c': 'maths-2018-HL-scheme-p040-i0',
    'maths-2018-hl-p2-q9-b-iii': 'maths-2018-HL-scheme-p042-i0',
}

p = Paper(2018, 'hl', 'p2', {'5B': [0, 2, 5], '5C': [0, 2, 4, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10], '15C': [0, 4, 11, 15],
                             '15D': [0, 4, 7, 11, 15], '20C': [0, 7, 13, 20], '20D': [0, 5, 10, 15, 20]},
          'LC003ALP200EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
comp = 'In a competition Mary has a probability of 1/20 of winning, a probability of 1/10 of finishing in second place, and a probability of 1/4 of finishing in third place. If she wins the competition she gets €9000. If she comes second she gets €7000 and if she comes third she gets €3000. In all other cases she gets nothing. Each participant in the competition must pay €2000 to enter.'
A('1-a', 'Q1(a)', '15C', [26], [3], '1-3', 'probability', 'Find the expected value of Mary’s loss if she enters the competition.', stem=comp)
A('1-b', 'Q1(b)', '10D', [27], [3], '1-3', 'probability', 'Each of the 3 prizes in the competition above is increased by the same amount (€x) but the entry fee is unchanged. For example, if Mary wins the competition now, she would get €(9000 + x). Mary now expects to break even. Find the value of x.', stem=comp)
zs = 'statistics-z-scores'
A('2-a', 'Q2(a)', '5B', [28], [4], '1-3', zs, 'The diagram shows the standard normal curve. The shaded area represents 67% of the data. Find the value of z₁.')
ex = 'The percentage results in a Maths exam for a class had a mean mark of 70 with a standard deviation of 15. The percentage results in an English exam for the same class had a mean mark of 72 with a standard deviation of 10. The results in both exams were normally distributed.'
A('2-b-i', 'Q2(b)(i)', '10C', [28], [4], '1-3', zs, 'Mary got 65 in Maths and 68 in English. In which exam did Mary do better relative to the other students in the class? Justify your answer.', stem=ex)
A('2-b-ii', 'Q2(b)(ii)', '5C', [28], [4, 5], '1-3', zs, 'In English the top 15% of students were awarded an A grade. Find the least whole number mark that merited the award of an A grade in English.', stem=ex)
A('2-b-iii', 'Q2(b)(iii)', '5C', [29], [4, 5], '1-3', zs, 'Using the empirical rule, or otherwise, estimate the percentage of students in the class who scored between 52 and 82 in the English test.', stem=ex)
code = 'A security code consists of six digits chosen at random from the digits 0 to 9. The code may begin with zero and digits may be repeated. For example 0 7 1 7 3 7 is a valid code.'
A('3-a-i', 'Q3(a)(i)', '15C', [30], [6], '1-1', 'probability', 'Find how many of the possible codes will end with a zero.', stem=code)
A('3-a-ii', 'Q3(a)(ii)', '5B', [30], [6], '1-1', 'probability', 'Find how many of the possible codes will contain the digits 2 0 1 8 together and in this order.', stem=code)
A('3-b', 'Q3(b)', '5C', [30], [6], '1-1', 'probability,algebra-expressions-factorising', 'Find a, b, c, and d, if ((n + 3)! (n + 2)!)/((n + 1)! (n + 1)!) = an³ + bn² + cn + d, where a, b, c, and d ∈ ℕ.')
tf = 'trigonometry-functions-identities'
A('4-a', 'Q4(a)', '20C', [31], [7], '2-3', tf, 'Find all the values of x for which cos(2x) = −√3/2, where 0° ≤ x ≤ 360°.')
A('4-b', 'Q4(b)', '5C', [31], [7], '2-3', tf + ',trigonometry-triangles', 'Let cos A = y/2, where 0° < A < 90°. Write sin(2A) in terms of y.')
mn = 'The line m: 2x + 3y + 1 = 0 is parallel to the line n: 2x + 3y − 51 = 0.'
q5b = 'Find the coordinates of B, the point on the line n closest to A, as shown below.'
cl = 'co-ordinate-geometry-of-the-line'
A('5-a', 'Q5(a)', '10C', [32], [8], '2-2', cl, 'Verify that A(−2, 1) is on m.', stem=mn)
A('5-b', 'Q5(b)', '10D', [32], [8], '2-2', cl, q5b, stem=mn + ' Part (a): Verify that A(−2, 1) is on m.')
A('5-c', 'Q5(c)', '5C', [33], [8, 9], '2-2', 'co-ordinate-geometry-of-the-circle', 'Two touching circles, s and t, are shown in the diagram. m is a tangent to s at A and n is a tangent to t at B. The ratio of the radius of s to the radius of t is 1 : 3. Find the equation of s.',
  stem=mn + ' Part (a): Verify that A(−2, 1) is on m. Part (b): ' + q5b)
A('6-a', 'Q6(a)', '15D', [34], [10, 11], '2-1', 'geometry-constructions-proofs', 'Let ΔABC be a triangle. Prove that if a line l is parallel to BC and cuts [AB] in the ratio s : t, where s, t ∈ ℕ, then it also cuts [AC] in the same ratio.')
A('6-b', 'Q6(b)', '10C', [35], [11], '2-1', 'geometry', 'In the triangle ABC shown below: |∠CAB| = 90°, |AX| = 4 cm, |AY| = 3 cm, XY ∥ BC, XZ ∥ AC, and |AX| : |XB| = 1 : 2. Find |BZ|.')
rail = 'A section of a garden railing is shown below. This section consists of nine cylindrical bars, labelled A to I, with a solid sphere attached to the centre of the top of each bar. The volume of each sphere from B to E is 1·75 times the volume of the previous sphere.'
q7a = 'The radius of sphere A is 3 cm. Find the sum of the volumes of the five spheres A, B, C, D, and E. Give your answer correct to the nearest cm³.'
q7bi = 'The surface area of sphere E can be taken to be 503 cm². The height of the railing at E (i.e. the sum of the heights of bar E and sphere E) is 1·2 metres. Find the height of bar E, in cm, correct to 1 decimal place.'
q7bii = 'The radius of each bar is 1 cm. The volume of bar A is 71·3π cm³. The heights of the bars A, B, C, D, and E form an arithmetic sequence. Find, in cm, the height of each bar.'
q7c = 'There is a wall on each side of the section of railing, as shown in the diagram below which is not to drawn to scale. The distance from wall to wall is 1·5 m. The distance from the wall to bar A is 20 cm and similarly from the other wall to bar I is 20 cm. The radius of each bar is 1 cm. The gap between each bar is identical. Find the size of this gap.'
av = 'area-volume'
A('7-a', 'Q7(a)', '10D', [36], [12], '3-4', av + ',sequences-series', q7a, stem=rail)
A('7-b-i', 'Q7(b)(i)', '10C', [36], [12, 13], '3-4', av, q7bi, stem=rail + ' Part (a): ' + q7a)
A('7-b-ii', 'Q7(b)(ii)', '10D', [36], [12, 13], '3-4', av + ',sequences-series', q7bii, stem=rail + ' Part (b)(i): ' + q7bi)
A('7-c', 'Q7(c)', '15C', [37], [12, 14], '3-4', av, q7c, stem=rail)
A('7-d', 'Q7(d)', '5B', [37], [12, 13, 14], '2-3', 'trigonometry-triangles,' + av, 'The sphere on bar A and the sphere on bar B are to be joined by a straight rod as shown in the diagram below which is not to drawn to scale. Find the length of the shortest rod that will join sphere A to sphere B. Give your answer in cm, correct to 1 decimal place.',
  stem=rail + ' Part (a): ' + q7a + ' Part (b)(ii): ' + q7bii + ' Part (c): ' + q7c)
ac = 'Acme Confectionery makes cakes and chocolate bars.'
inf = 'statistics-inferential-statistics'
A('8-a-i', 'Q8(a)(i)', '20D', [38], [15], '1-7', inf + ',' + zs, 'Acme Confectionery has launched a new bar called Chocolate Crunch. The weights of these new bars are normally distributed with a mean of 4·64 g and a standard deviation of 0·12 g. A sample of 10 bars is selected at random and the mean weight of the sample is found. Find the probability that the mean weight of the sample is between 4·6 g and 4·7 g.', stem=ac)
A('8-a-ii', 'Q8(a)(ii)', '15C', [38], [15], '1-7', inf, 'A company surveyed 400 people, chosen from the population of people who had bought at least one Chocolate Crunch bar. Of those surveyed, 324 of them said they liked the new bar. Create the 95% confidence interval for the population proportion who liked the new bar. Give your answer correct to 2 decimal places.', stem=ac)
A('8-b-i', 'Q8(b)(i)', '5C', [39], [15, 16], '1-7', inf, 'Put one tick into the table for each statement to indicate whether the statement is Always True, Sometimes True or Never True. In the table, n is the size of the sample and p̂ is the sample proportion. Statement 1. When forming confidence intervals (for fixed n and p̂), an increased confidence level implies a wider interval. Statement 2. As the value of p̂ increases (for fixed n), the estimated standard error of the population proportion increases. Statement 3. As the value of p̂(1 − p̂) increases (for fixed n), the estimated standard error of the population proportion increases. Statement 4. As n, the number of people sampled, increases (for fixed p̂), the estimated standard error of the population proportion increases.', stem=ac)
A('8-b-ii', 'Q8(b)(ii),Q8(b)(iii)', '10D', [40], [15, 16], '1-7', inf + ',differentiation-applications', '(ii) Using calculus or otherwise, find the maximum value of p̂(1 − p̂). (iii) Hence, find the largest possible value of the radius of the 95% confidence interval for a population proportion, given a random sample of size 800.', stem=ac)
A('8-c', 'Q8(c)', '10D', [40], [15, 17], '3-3', 'financial-maths,sequences-series', 'Acme Confectionery has an employee pension plan. For an employee who qualifies for the full pension, Acme Confectionery will pay a sum of €20 000 on the day of retirement. It will then pay a sum on the same date each subsequent year for the next 25 years. Each year the employee is paid a sum that is 1% more than the amount paid in the previous year. What sum of money must the company have set aside on the day of retirement in order to fund this pension? Assume an annual interest rate (AER) of 2·4%.', stem=ac)
cr = 'In engineering, a crank-and-slider mechanism can be used to change circular motion into motion back and forth in a straight line. In the diagrams below, the crank [OD] rotates about the fixed point O. The point C slides back and forth in a horizontal line. [CD] is the rod that connects C to the crank. The diagrams below show three of the possible positions for C and D. |OD| = 10 cm and |DC| = 30 cm.'
fa = cr + ' Part (b): As D moves in a circle around O, the angle α in the diagram below increases. The distance |CX| can be considered to be a function of α and written as f(α).'
tt = 'trigonometry-triangles'
A('9-a', 'Q9(a)', '10C', [41], [18], '2-3', tt, 'The diagram below shows a particular position of the mechanism with |∠DCO| = 15°. Find |∠COD|, correct to the nearest degree.', stem=cr)
A('9-b-i', 'Q9(b)(i)', '5C', [41], [18, 19], '2-3', tf, 'Write down the period and range of f.', stem=fa)
A('9-b-ii', 'Q9(b)(ii)', '5C', [41], [18, 19], '2-3', tf + ',' + tt, 'Complete the table below for f(α). Give your answers correct to 2 decimal places where appropriate. (Note: Diagram 1 at the start of this question represents α = 0°). α: 0°, 90°, 180°, 270°, 360°. f(α) (cm): 30, _, _, _, _.', stem=fa)
A('9-b-iii', 'Q9(b)(iii)', '10C', [42], [18, 19], '2-3', tf, 'Use your values from the table to draw a rough sketch of f in the domain 0° ≤ α ≤ 360°.', stem=fa + ' Part (b)(ii): Complete the table below for f(α). α: 0°, 90°, 180°, 270°, 360°. f(α) (cm): 30, _, _, _, _.')
A('9-b-iv', 'Q9(b)(iv)', '5B', [42], [18, 19, 20], '2-3', tf, 'Referring to Diagrams 1, 2, and 3 near the start of this question, for which of the three positions of the mechanism will a 1 degree change in α cause the greatest change in the position of C? Explain your answer.', stem=fa)
A('9-c', 'Q9(c)', '5C', [43], [18, 20], '2-3', tt, 'The diagram below shows another crank-and-slider mechanism with different dimensions. In the diagram, |AB| = 36 cm, |AX| = 31 cm, and |∠BAO| = 10°. (Note: |∠OBA| ≠ 90°) Find r, the length of the crank. Give your answer in cm, correct to the nearest cm.', stem=cr)

marks = {'1': 25, '2': 25, '3': 25, '4': 25, '5': 25, '6': 25, '7': 50, '8': 60, '9': 40}
p.check(marks, 32)
p.review(marks,
    'Independent visual reading of all 24 question-paper pages and PDF pages 23–44 of the combined Higher Level scheme (the Paper 2 title page 23, the scale table on page 24, the summary of mark allocations on page 25, every Paper 2 model solution and marking note on pages 26–43, and the back cover on page 44). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(23, 45)), [24, 25],
    ['The paper is 300 marks: candidates answer all nine questions (Section A Q1–6, 25 marks each; Section B Q7 50 marks, Q8 60 marks, Q9 40 marks). Every question is retained.',
     '32 independently marked units, matching the printed summary of allocations on scheme page 25. Q8(b)(ii) and (iii) share one 10D scale (“(b)(ii)+(iii)”) and are one task.',
     'Paper 2 bands from the scale table on scheme page 24 (headed “Paper 1” in print, but it is the Paper 2 table and its ladders differ from Paper 1’s): 5B 0,2,5; 5C 0,2,4,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15C 0,4,11,15; 15D 0,4,7,11,15; 20C 0,7,13,20; 20D 0,5,10,15,20. Every part prints the same ladder beside its scale.',
     'This paper had no authored cards before this review; all 32 units are new. Marking points are lifted line by line from the scheme (read through the glyph repair map) and labelled with the part of the scheme they come from; Q1(b), Q5(b) and Q5(c) keep each printed method’s ladder separately, and a few long methods are quoted as one multi-line point to stay within the row limit. The Q8(b)(i) tick table is quoted statement by statement with the ticked column in the label.',
     'Six parts carry the SEC’s own print of their scheme row (model solution and every credit band), cropped from the scheme PDF and shown only after the reveal, because the working refers to a diagram or graph, a tick table, or a line whose stacked-fraction digits extract as lone numerals: Q4(b), Q6(a), Q7(d), Q8(b)(i), Q8(c), Q9(b)(iii).',
     'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. Scheme page references are PDF positions (printed page number + 3); question-paper PDF positions match the printed page numbers.'],
    [{'pages': [2, 3, 12], 'wording': 'Answer all nine / all six / all three questions', 'classification': 'all-questions-required',
      'reason': 'Every question on the paper is required; every published scale unit is retained.'},
     {'pages': [5, 16], 'wording': 'Using the empirical rule, or otherwise / Using calculus or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task, with no printed pool of prompts.'}],
    lambda t: ('all-questions-required', 'All nine questions are required, including all six Section A and all three Section B questions; every published scale unit is retained.') if 'Answer all' in t
        else ('method-choice', 'Alternative methods solve the same printed task and share its scale; there is no printed pool of prompts.') if 'or otherwise' in t else None)
p.apply(ROWS, '2018 Higher Level Paper 2', expect_added=[c['id'] for c in p.cards],
        card_overrides={k: {'figureKey': v} for k, v in SCHEME_ROW_FIGURES.items()})
