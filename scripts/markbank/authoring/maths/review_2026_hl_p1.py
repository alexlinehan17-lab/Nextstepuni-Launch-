import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from solution_lib import Paper

HL_P1 = {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10],
         '10C': [0, 3, 7, 10], '10D': [0, 2, 5, 8, 10], '15D': [0, 3, 8, 12, 15]}
p = Paper(
    year=2026, level='higher', paper_key='p1', paper_file='LC003ALP100EV.pdf', scheme_file='LC003ALP000EV.pdf',
    prefix='maths-2026-hl-p1', ref='2026 HL Paper 1', scales=HL_P1, reviewed_at='2026-10-11',
    general_notes=[3, 4, 6], scheme_pages=list(range(3, 44)),
    printed_marks={**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}},
    review_method='Independent visual reading of all 32 question-paper pages and PDF pages 3–43 of the combined Higher Level scheme (general notes, the Paper 1 scale table on page 6, and every Paper 1 model solution and marking note). Each task boundary is the published scale, not a parser count.',
    source_notes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained; no combined multi-question cards.',
        '42 independently marked units. Shared scales keep their parts together: Q5(b)(i)–(ii) 10D, Q8(e)(i)–(ii) 5D, Q9(a)–(b) 10D, Q10(a)(i)–(ii) 10C, Q10(b)(i)–(ii) 5C and Q10(f)(i)–(ii) 15D.',
        'Paper 1 bands from scheme page 6: 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,2,5,8,10; 15D 0,3,8,12,15.',
        'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions.',
        'Q1(c) Method 4 continues on scheme page 9 and Q5(b)’s completed Venn diagram is on page 20; both pages are attached to those tasks.',
        'Diagrams (Venn diagram, cylinder, graphs of g, h, f and f′) are read from the attached original question pages; prompts quote the paper’s own wording.',
        'Some scheme text layers mis-map bold digits (for example P(7) prints as a doubled digit), so card rows quote only notes whose text layer matches the printed scheme; the scheme reader shows the full published notes.',
    ],
    out_name='2026-higher-p1.json', atlas_prefix='mathematics-higher-', section_of=lambda q: 'A' if q <= 6 else 'B',
)
A = p.add
# Section A
A('1-a', 'Q1(a)', '5C', [7], [4], '4-2', 'algebra-solving-equations',
  'Solve the following equation in a ∈ ℝ, a ≥ −7: 5 = 1 + √(a + 7)',
  ['a = 9', 'Work of merit, for example, one relevant operation indicated or carried out', 'Linear equation in a'])
A('1-b', 'Q1(b)', '10D', [7], [4], '4-1', 'algebra-expressions-factorising',
  'Rearrange the following to write p in terms of n and s, where n, p, and s are positive real numbers: 1/n + 2/p = 3/s',
  ['Isolates term(s) with p', 'Work of merit, for example, finds a relevant common denominator',
   'Note: a cross on its own (indicating cross-multiplication) is not considered work of merit.'])
A('1-c', 'Q1(c)', '15D', [8, 9], [5], '4-2', 'algebra-cubics',
  '2x² + 4x − 6 is a factor of 8x³ + 6x² − 44x + 30. Using this fact, or otherwise, solve the equation: 8x³ + 6x² − 44x + 30 = 0',
  ['x = −3 or x = 1', 'Factorises 2x² + 4x − 6 / fully substituted quadratic formula', 'Finds two roots of quadratic factor',
   'Sets up long division / array / product'])
A('2-a', 'Q2(a)', '10C', [10], [6], '4-1', 'sequences-series',
  'By writing the recurring part as an infinite geometric series, express the following number in the form a/b where a, b ∈ ℕ: 4·36363636 …',  # e7e0882a8: kept to the printed wording
  ['Formula for sum of infinite geometric series substituted correctly',
   'Work of merit, for example, identifies a or r, or writes two relevant terms in geometric sequence',
   'Award at most Low Partial Credit if an infinite geometric series is not used'])
loan = 'Rya is taking out a loan to buy a car. The annual interest rate (APR) for her loan is 8·4%.'
A('2-b-i', 'Q2(b)(i)', '5C', [11], [7], '3-3', 'financial-maths',
  'Show that this APR is equivalent to a monthly interest rate of 0·67%, correct to 2 decimal places.',
  ['= 0·67% [2 D.P.]', 'No Credit: Correct answer (0·67%) without supporting work'], stem=loan)
A('2-b-ii', 'Q2(b)(ii)', '15D', [12], [7], '3-3', 'financial-maths',
  'Rya’s loan is for €14 000. To pay off the loan, she makes equal repayments each month for 5 years. She makes the first repayment one month after she takes out the loan. Find the amount of each repayment Rya makes, correct to the nearest cent, and hence find the total amount of interest that Rya pays over the 5 years. Assume that the monthly interest rate for the loan is 0·67%.',
  ['= [€]284·14 [2 D.P.]', '= [€]3048·40', 'Fully correct substitution into geometric / amortisation formula',
   'Finds interest, based on A from Step 2'], stem=loan)
A('3-a', 'Q3(a)', '10D', [13], [8], '5-2', 'differentiation-rules',
  'The function f(x) = (7x²)(cos(3x)). Use the product rule to find f′(x), and hence find the value of f′(π), in terms of π.',
  ['= −14π', 'Work of merit in finding f′(x), for example, finds u′(x)',
   'One part is correct (finds f′(x) or f′(π)) and work of merit in the other part'])
g = 'The function g(x) has the following second derivative: g′′(x) = 30x − 18. The slope of the tangent to the curve y = g(x) at the point (−1, 8) is −2.'
A('3-b-i', 'Q3(b)(i)', '10D', [14], [9], '5-2', 'integration',
  'By integrating g′′(x), use this information to find an expression in x for g′(x), the first derivative of g(x).',
  ['g′(x) = 15x² − 18x − 35', 'Constant of integration is needed for Steps 3 or 4 to be correct'], stem=g)
A('3-b-ii', 'Q3(b)(ii)', '10D', [15], [9], '5-2', 'integration',
  'Hence, find an expression in x for g(x).',
  ['g(x) = 5x³ − 9x² − 35x − 13', 'Integrates all terms in g′(x) from part (b)(i)'],
  stem=g + ' Part (b)(i) asks for an expression in x for g′(x), found by integrating g′′(x).')
i2 = 'In this question, i² = −1.'
A('4-a', 'Q4(a)', '10C', [16], [10], '4-4', 'complex-numbers',
  'u is the complex number u = 3 − 7i. u̅ is the complex conjugate of u. Write 2u̅ + 5iu in the form a + bi, where a, b ∈ ℝ.',
  ['= 41 + 29i', 'If i² is not shown / dealt with, award Low Partial Credit at most'], stem=i2)
A('4-b', 'Q4(b)', '15D', [17], [10], '4-4', 'complex-numbers',
  'Use de Moivre’s theorem to find the value of (3 − √3i)⁸. Give your answer in the form a + bi, where a, b ∈ ℝ.',
  ['= −10 368 + 10368√3 i', 'Candidates must engage with polar form or de Moivre’s theorem in order to be awarded any credit',
   'Correct answer with no supporting work is awarded No Credit'], stem=i2)
A('4-c', 'Q4(c)', '5D', [18], [11], '4-4', 'complex-numbers',
  'w and v are the following two complex numbers, where a, b ∈ ℝ and θ is an angle in degrees: w = a (cos 160° + i sin 160°); v = b (cos θ + i sin θ). For these two numbers, |w| = 5 and vw = −15. Use this information to find one possible set of values of a, of b, and of θ.',
  ['Note that |a| = 5 and |b| = 3.', 'And θ = 20° [ or 380°, or … ]', 'If Step 3 is incorrect, award Mid Partial Credit at most.'], stem=i2)
A('5-a', 'Q5(a)', '10C', [19], [12], '3-2', 'indices-and-logs',
  'Write each of the following numbers in the form 4^r, where r ∈ ℚ: 64; 1/16; 2.',
  ['64 = 4³', '2 = √4 = 4^(1/2)', 'Accept correct answers without supporting work',
   'Apply a * once if answer(s) are given as the values of r'])
A('5-b-i-ii', 'Q5(b)(i),Q5(b)(ii)', '10D', [19, 20], [12, 13], '3-1', 'indices-and-logs',
  '(i) Write each of the following numbers in the correct region in the Venn diagram on the previous page: 64, 1/16, √3, √2, 12, 1. (ii) Write down one element in ℝ that is not in any of the sets A, B, or D. Do not use any of the numbers from part (b)(i).',
  ['Any valid answer – a rational number that is neither a multiple of 4 nor a rational power of 4.',
   'Consider solution as having 7 parts: the 6 numbers in (b)(i) that must be put in the correct region of the Venn diagram, and the answer to (b)(ii).'],
  stem='The Venn diagram below shows the following three sets in ℝ: A: all integer multiples of 4 (all numbers that can be written as 4m where m ∈ ℤ); B: all numbers that can be written as 4^r, where r ∈ ℚ; D: ℝ\\ℚ, the set of irrational numbers. The set A ∩ D is shaded – there are no elements in this part of the Venn diagram.')
A('5-c', 'Q5(c)', '10C', [20], [13], '3-2', 'indices-and-logs',
  'For some real number k: 4^k = 9. Find the value of k. Give your answer in the form a/(log₃ b) where a, b ∈ ℕ are constants.',
  ['Step 1: Equation in log₃', 'Step 2: Linear equation in k', 'Step 3: finds k in correct form',
   'Work of merit, for example, 9 = 3², or some relevant use of logs'])
A('6-a', 'Q6(a)', '15D', [21], [14], '3-1', 'induction',
  'Prove by induction that the following is true for all n ∈ ℕ and n ≥ 7: n! > 3^n',
  ['P(k) stated', 'Work of merit, for example, P(n) checked for n ≠ 7; or P(k + 1) stated',
   'Reason for (k + 1) × 3^k > 3 × 3^k, or equivalent, must appear for Step 4 to be correct.'])
A('6-b', 'Q6(b)', '5C', [22], [15], '4-2', 'algebra-solving-equations',
  'Solve this equation in n ∈ ℕ: (n + 1)!/(n − 1)! = 156',
  ['so n = 12 [as n > 0]', 'Some relevant work with factorials required to get any credit.'])
A('6-c', 'Q6(c)', '10C', [23], [15], '4-1', 'sequences-series',
  'T₁, T₂, T₃, … is a geometric sequence, where: the first term, T₁ < 2; the sum of the first two terms, T₁ + T₂ = 2; the sum of the first three terms, T₁ + T₂ + T₃ < 2. Find one possible geometric sequence for which this is true. State the first three terms of your sequence, and find the value of S₃ = T₁ + T₂ + T₃.',
  ['r < 0, as S₃ < S₂', 'and S₃ = 2 + T₃ = −7', 'Step 2 can be considered correct even if T₁ > 0.'])
# Section B
tank = 'A water tank is in the shape of a cylinder. Over a 4-minute period of time, the volume of water in the tank can be modelled by: V(t) = 0·025t³ − 9t² + 550·8t + 68 900, where V is in cm³ and t is the time, in seconds, for 0 ≤ t ≤ 240, t ∈ ℝ.'
A('7-a', 'Q7(a)', '5B', [24], [16], '5-1', 'functions',
  'Find the volume of water in the tank after 1 minute.',
  ['= 74 948 cm³', 'Treat setting t = 1 as an error rather than a slip, as it simplifies the work.'], stem=tank)
A('7-b', 'Q7(b)', '10C', [24], [16], '5-2', 'differentiation-applications',
  'Use differentiation to find the rate at which the volume of water in the tank is changing after exactly 150 seconds (that is, find dV/dt at this time). Give your answer in cm³ per second.',
  ['= −461·7 [cm³ / second]', 'Some differentiation required to get any credit'], stem=tank)
A('7-c', 'Q7(c)', '10D', [25], [16, 17], '5-2', 'differentiation-applications,algebra-inequalities',
  'Find the range of values of t for which the volume of water in the tank is decreasing.',
  ['Answer: t ∈ (36, 204)', 'Accept “between 36 and 204”', 'Quadratic formula fully substituted, or quadratic equation factorised',
   'Apply a * for endpoints of inequality included'], stem=tank)
A('7-d', 'Q7(d)', '10D', [26], [16, 17], '5-2', 'differentiation-applications',
  'The water in the tank is in the shape of a cylinder with a constant radius of 26 cm and a height of h cm, where h ∈ ℝ, h > 0. Find dV/dh and hence, or otherwise, find the rate of change of the height of the water in the tank with respect to time after 150 seconds. Give your answer in cm per second, correct to 2 decimal places.',
  ['= −0·22 [cm/sec] [2 D.P.]', 'Accept correct answers with incorrect or no unit.', 'Incorrect rounding, otherwise correct.'], stem=tank)
c_h = 'Water is poured into another container. The function C(h) can be used to model the rate at which the height of this water is changing, in centimetres per second, when its height is h cm. C(h) is given by: C(h) = 20/(16πh − πh²) for a particular range of values of h ∈ ℝ, so that C(h) is a continuous function of h and has a local minimum value.'
A('7-e', 'Q7(e)', '10D', [27], [18], '5-2', 'differentiation-applications',
  'Find the local minimum value of C(h). Give your answer in cm/second, correct to 1 decimal place. Use differentiation in your solution.',
  ['= 0·1 [cm/sec] [1 D.P.]', 'Carries out all necessary differentiation', 'Sets relevant derivative = 0'], stem=c_h)
A('7-f', 'Q7(f)', '5B', [28], [18, 19], '5-1', 'functions',
  'C(h) is defined for all values of h ∈ ℝ for which 0 < h < M, for a constant M ∈ ℝ. Find the biggest value that M can be.',
  ['M = 16', 'Accept correct answer without supporting work', 'Apply a * for “M < 16”'], stem=c_h)
piano = 'Rían is tuning a piano. He has an app on his phone that can measure the frequency, in Hertz (Hz), of any note on the piano. Rían calls one of the notes Concert A, and tunes it so that it has a frequency of 440 Hz. He then uses the following function F(x), for x ∈ ℝ, to help him tune the other notes on the piano: F(x) = 440 × 2^(x/12). For each note on the piano, Rían counts how many notes above (or below) Concert A it is. Rían tunes the note that is x notes above Concert A to the frequency F(x), for x ∈ ℕ. He tunes the note that is x notes below Concert A to the frequency F(−x), for x ∈ ℕ.'
A('8-a', 'Q8(a)', '5B', [29], [20], '5-1', 'functions,indices-and-logs',
  'Rían tunes the note that is 11 notes above Concert A. By setting x = 11, use F(x) to find the frequency of this note, correct to the nearest whole number.',
  ['= 831 [Hz]', 'Note: must sub in 11 in order to be awarded any credit'], stem=piano)
A('8-b', 'Q8(b)', '10C', [29], [20], '5-1', 'functions,indices-and-logs',
  'Rían tunes the note that is 6 notes below Concert A. Find the frequency of this note. Give your answer in Hz, correct to 4 significant figures.',
  ['= 311·1 [Hz] [4 sig figs]', 'Note: 6 or −6 must appear in substitution for x in order to be awarded any credit'], stem=piano)
A('8-c', 'Q8(c)', '10D', [30], [20, 21], '3-2', 'indices-and-logs',
  'Rían knows that the note that is seven notes above Concert A has a frequency of approximately 660 Hz. Find the actual value of x ∈ ℝ for which F(x) = 660. Give your answer correct to 2 decimal places.',
  ['= 7·02 [2 D.P.]', 'Correct answer with no supporting work is awarded No Credit'], stem=piano)
A('8-d', 'Q8(d)', '5C', [31], [20, 21], '5-2', 'differentiation-rules',
  'Find an expression for F′(x), the derivative of F with respect to x. You do not need to simplify your answer.',
  ['Consider solution as requiring 4 terms', '3 terms correct', 'Accept correct answer without supporting work'], stem=piano)
A('8-e-i-ii', 'Q8(e)(i),Q8(e)(ii)', '5D', [32], [22], '5-2', 'differentiation-applications',
  '(i) Using only this information, estimate the value of G(k + 2). Show your working out. (ii) The function G(x) is of the form G(x) = Ae^(bx), where A and b are positive constants. Based on this, state whether the estimate for G(k + 2) from part (e)(i) is too big or too small, compared to the actual value of G(k + 2), or if we don’t have enough information to be sure. Justify your answer. It may be helpful to draw a diagram. Tick one box only: the estimate is too big; the estimate is too small; we can’t be sure.',
  ['= 208·6', 'The estimate is too small.', 'The graph curves upwards, so it [the graph of the actual value] is always above the tangent line.',
   'One part correct and work of merit in the other part'],
  stem='G(x) is another function that can be used to define the frequency of notes, for x ∈ ℝ. For some number k ∈ ℝ: G(k) = 197 and G′(k) = 5·8.')
A('8-f', 'Q8(f)', '15D', [33], [23], '4-2', 'algebra-simultaneous-equations',
  'Each person in a choir is either a soprano (S), an alto (A), a tenor (T), or a base (B). In this choir: there are 384 people in total; there are twice as many altos as there are sopranos; there are 12 more tenors than there are bases; the number of (sopranos plus altos) is three times the number of (tenors plus bases). Work out the number of sopranos, of altos, of tenors, and of bases in the choir.',
  ['S = 96; A = 192; T = 54; B = 42', 'Writes down 4 correct equations', 'Finds three remaining values'])
swim = 'Ella goes swimming. In one session, she swims in sets. The first three sets are shown in the table below. In each set, she swims a certain number of different distances, called shuttles. There are 3 shuttles in Set 1: first 20 m, then 40 m, then 20 m. This gives a total distance of 80 m for Set 1. The first shuttle in each set is 20 m. The shuttles increase in length by 20 m until they reach the maximum for that set, and then decrease by 20 m until the shuttle length returns to 20 m. The longest shuttle in each set is 20 m longer than the longest shuttle in the previous set. In the table, Set 1 has shuttles 20, 40, 20, 3 shuttles and a total distance of 80 m; Set 2 has shuttles 20, 40, 60, 40, 20 and 5 shuttles; Set 3 has shuttles 20, 40, 60, 80, 60, 40, 20 and a total distance of 320 m; the row for Set 4 is empty.'
onward = swim + ' Suppose that Ella keeps swimming longer and longer sets in this way, indefinitely.'
A('9-a-b', 'Q9(a),Q9(b)', '10D', [34], [24], '4-1', 'sequences-series',
  '(a) Fill in the missing values in the table above – all of the shuttles for Set 4, and the 4 other missing values. Suppose that Ella keeps swimming longer and longer sets in this way, indefinitely. (b) Find the length of the 12th shuttle in Set 14.',
  ['12 × 20 = 240 m', 'Consider solution as requiring 6 parts: the five entries in the table, and part (b)',
   '3 terms correct in the shuttles of Set 4'], stem=swim)
A('9-c', 'Q9(c)', '10D', [35], [24, 25], '4-1', 'sequences-series',
  'Find a formula, in terms of n ∈ ℕ, for the total distance (in metres) for Set n. Give your answer in the form an² + bn + c, where a, b, c ∈ ℝ are constants.',
  ['Dist. = 20n² + 40n + 20', 'Fully substituted closed form'], stem=onward)
A('9-d', 'Q9(d)', '5C', [36], [24, 25], '4-1', 'sequences-series',
  'In Set h, shuttle 21 and shuttle 43 are the same length. Find the value of h.',
  ['So ℎ = 31', 'Middle shuttle is number', 'Finds 32 with supporting work'], stem=onward)
A('9-e', 'Q9(e)', '5C', [36], [24, 25], '4-1', 'sequences-series',
  'Find an expression in k ∈ ℕ for the length of the kth shuttle in Set 18, where 19 ≤ k ≤ 37.',
  ['T₁₉ = 19 × 20 = 380', 'So a = 760', 'a − 20(19) = 380', 'a + 18d = 380'], stem=onward)
weights = 'As part of her training, Ella also lifts weights. The number of times in a row that she can lift any given weight is called the number of reps that she can do with that weight. There are different formulas that Ella can use to estimate the heaviest weight that she could lift just once, called her one-repetition maximum (M). Two of these formulas are shown below. Each formula gives a value for M in kg, using the fact that Ella can do r reps with a weight of w kg. Epley formula: M = w × (1 + r/30). Brzycki formula: M = w × (36/(37 − r)).'
A('9-f', 'Q9(f)', '10C', [36], [26], '4-1', 'algebra-expressions-factorising',
  'Find the difference in the value of M given by each formula for 5 reps (r = 5). Give your answer as a fraction in terms of w.',
  ['Both formulae substituted', 'Apply a * if the answer is the coefficient of w', 'Apply a * if the fraction is not simplified'], stem=weights)
A('9-g', 'Q9(g)', '10D', [37], [26], '4-2', 'algebra-solving-equations,algebra-quadratics',
  'Solve an equation to find the number of reps (r) for which the two formulas give the same value of M, for any given weight w.',
  ['i.e. r = 10 [as r ≥ 0]', 'Forms equation without r in denominator',
   'Apply a * if r = 10 and r = −3 are found, but r = 10 is not selected.'], stem=weights)
darek = 'Darek is looking at patterns in the co-ordinate plane.'
A('10-a-i-ii', 'Q10(a)(i),Q10(a)(ii)', '10C', [38], [27], '5-1', 'functions',
  '(i) The diagram below shows the graphs of the functions g(x) and g(x) + 1. Draw and label the graph of y = g(x) + 3 on the diagram below, using the same axes and scales. (ii) The diagram below shows the graphs of the functions h(x) and h(x − 1). Draw and label the graph of y = h(x + 2) on the diagram below, using the same axes and scales.',
  ['1 part correct ((i) or (ii))', 'Work of merit in both parts',
   'Apply a * once if multiple graphs drawn, but correct graph is not labelled'], stem=darek)
periodic = darek + ' The diagram below shows part of the graph of the periodic function f(x). The diagram shows more than one full period. The graph of the function repeats in this way for all of x ∈ ℝ. Use the graph to answer parts (b), (c), and (d).'
A('10-b-i-ii', 'Q10(b)(i),Q10(b)(ii)', '5C', [39], [28], '5-1', 'functions',
  '(i) State the period of the function f(x). (ii) There are an infinite number of whole numbers n ∈ ℤ, n ≠ 0, for which the graph of y = f(x) and the graph of y = f(x + n) are the same. State three possible values of n. Note that the graph of f(x + n) is the graph of f(x) shifted n units horizontally.',
  ['Any three non-zero multiples of 5, for example: 5, 20, −10', 'Accept period of −5'], stem=periodic)
A('10-c', 'Q10(c)', '10D', [40], [28], '5-2', 'integration',
  'Find the value of ∫ (from 0 to 3) f(x) dx. Show all your working out.',
  ['Here, “area” is taken to mean “signed area”.', 'Finds total signed area',
   'Note: there needs to be some work with negative area in order for Step 4 to be considered correct.'], stem=periodic)
A('10-d', 'Q10(d)', '5C', [41], [28, 29], '5-2', 'differentiation-applications',
  'Based on the graph of f(x) on the previous page, f′(x), the derivative of f(x), is defined for x ∈ ℝ where 0 < x < 6 and x ≠ 1, 2, 5. The diagram on the right shows part of the graph of y = f′(x). It is equal to 3 for 0 < x < 1 and is equal to 0 for 1 < x < 2. Draw the graph of y = f′(x) in the diagram on the right, for 2 < x < 6, x ∈ ℝ, x ≠ 5.',
  ['No penalty is applied for mishandling graph at x = 2, 5, or 6', '1 portion fully correct (for x ∈ (2, 5) or for x ∈ (5, 6))'],
  stem=periodic)
A('10-e', 'Q10(e)', '5D', [42], [29], '5-2', 'integration',
  'j(x) is a different function of x, with j(x) ≥ 0 for all x ∈ ℝ. For a constant a > 1: ∫ (from 1 to a) j(x) dx = 200. Use this to find the value of the following in terms of a and b, where b > 0 is a constant: ∫ (from 1 to a) [ j(x) + b ] dx',
  ['= 200 + b(a − 1)', 'Accept correct answer without supporting work', 'Finds required area.'], stem=darek)
A('10-f-i-ii', 'Q10(f)(i),Q10(f)(ii)', '15D', [43], [30], '5-1', 'functions',
  '(i) Darek knows that h(x + 1) = ax² + 2ax + a + bx + b + c. Use this to find the values of a and b that make the following true for all values of x: h(x + 1) = h(x) + 2. (ii) State what information your values of a and b from part (f)(i) give about the graph of y = h(x).',
  ['It must be a [straight] line with a slope of 2', 'Equates x terms / one correct equation in a and b',
   'Equates constant terms / second correct equation in a and b'],
  stem='Darek is investigating if there are any functions h for which h(x + 1) = h(x) + 2. He begins by looking at functions of the form: h(x) = ax² + bx + c, where a, b, c ∈ ℝ are constants.')

selection_review = [
    {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
     'reason': 'Candidates select independently marked questions; every question is retained. No combined multi-question practice cards.'},
    {'pages': [5, 17], 'wording': 'or otherwise / hence, or otherwise', 'classification': 'method-choice',
     'reason': 'Alternative solution methods for the same marked task; no printed pool of prompts.'},
    {'pages': [11, 13, 15, 28], 'wording': 'one possible set of values / one element / one possible geometric sequence / three possible values of n',
     'classification': 'open-answer',
     'reason': 'Each asks for a valid answer from an unbounded set; the scheme accepts any valid answer under one scale. Nothing finite to expand.'},
    {'pages': [22], 'wording': 'Tick one box only', 'classification': 'answer-selection',
     'reason': 'Choosing too big / too small / can’t be sure is the mathematical answer with its justification, not a choice of practice prompts.'},
    {'pages': [20, 23], 'wording': 'one of the notes / either a soprano, an alto, a tenor, or a base', 'classification': 'given-context',
     'reason': 'Descriptive setup of the context, not a selection instruction.'},
]
def classify(c):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        return ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    if 'or otherwise' in t:
        return ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    if 'one of the notes' in t:
        return ('given-context', 'Rían names one note Concert A; descriptive setup, not a choice of tasks.')
    if 'either a soprano' in t:
        return ('given-context', 'Each choir member belongs to one voice group; this is the data of a required simultaneous-equations task, not a choice of prompts.')
    return None
p.write(selection_review, classify)
