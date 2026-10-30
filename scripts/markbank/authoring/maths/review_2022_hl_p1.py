"""2022 HL Paper 1: review ledger, restored prompts, re-quote Q3(b), Q6(b), Q8(e)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *

ROWS = {
 'maths-2022-hl-p1-q3-b': [L(SOL, 'so A = 30°, so θ = 330°'), L(SOL, '= 512(cos 2970 + i sin 2970)'), L(SOL, '= 0 + 512i'),
     L(SOL, 'a = 0, b = 512'), L(NOTE, 'polar form must be used to achieve any credit'), L(NOTE, 'Accept 0 + 512i for Full Credit'),
     L(STEP, 'Finds r'), L(STEP, 'Finds θ'), L(STEP, 'Subs into de Moivre’s Theorem'), L(STEP, 'Evaluates'),
     L(LPC, 'Work of merit, for example, plots √3 − i, or some correct substitution into de Moivre’s Theorem'),
     L(MPC, '2 steps correct'), L(HPC, '3 steps correct'), L(FCM, 'a and b not explicitly stated and solution given as 512i')],
 'maths-2022-hl-p1-q6-b': [L(SOL, 'A = l × w = 4x × x = 4x²'), L(SOL, 'When A = 225, 4x² = 225,'), L(SOL, 'so x² = 225/4, i.e. x = 15/2'), L(SOL, 'dA/dx = 8x'),
     L(SOL, 'dA/dx = 1/2 (30)(4) = 60 cm²/cm'), L(NOTE, 'Accept without unit'), L('Method 1, ' + LPC, 'Work of merit, for example, l = 4x ; mentions dA/dx'), L('Method 1, ' + MPC, '2 steps correct'),
     L('Method 1, ' + HPC, '3 steps correct'), L('Method 2, ' + LPC, 'States relevant derivative, for example, dA/dx'), L('Method 2, ' + MPC, 'Any two of the following:'),
     L('Method 2, ' + HPC, 'and any two others from the MPC list above')],
 'maths-2022-hl-p1-q8-e': [L(SOL, '60 cos(π/3 t) = 72 − 110 = −38'), L(SOL, '(π/3)t₂ = π + 0·8849 … radians'),
     L(SOL, '1st time: Quadrant 2'), L(SOL, '2nd time: Quadrant 3'), L(SOL, 't = 3(π + 0·8849…)/π = 3·845 … = 3·85 mins'),
     L(STEP, 'Isolates cos(π/3 t)'), L(STEP, 'Finds reference angle or (π/3)t₁'), L(STEP, 'Finds (π/3)t₂ or t₁'), L(STEP, 'Finds t'),
     L(LPC, 'Work of merit, for example, some correct work towards isolating cos(π/3 t)'), L(MPC, '2 steps correct'),
     L(HPC, '3 steps correct'), L(FCM, 'Calculator in degree mode, otherwise correct')],
}
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2022, 'hl', 'p1', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10], '15D': [0, 4, 8, 12, 15]},
          'LC003ALP100EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
A('1-a', 'Q1(a)', '10C', [7], [4], '4-2', 'algebra-quadratics', 'Find the two values of m ∈ ℤ for which the following equation in x has exactly one solution: 3x² − mx + 3 = 0')
A('1-b', 'Q1(b)', '5B', [8], [4], '4-2', 'algebra-quadratics', 'Explain why the following equation in x has no real solutions: (2x + 3)² + 7 = 0')
A('1-c-i', 'Q1(c)(i),Q1(c)(ii)', '15D', [9], [5], '4-1', 'algebra-expressions-factorising,algebra-quadratics', '(i) Show that x = −1 is not a solution of 3x² + 2x + 5 = 0. (ii) Find the remainder when 3x² + 2x + 5 is divided by x + 1. That is, find the value of c when 3x² + 2x + 5 is written in the form 3x² + 2x + 5 = (x + 1)(ax + b) + c, where a, b, c ∈ ℤ.')
A('2-a', 'Q2(a)', '5C', [10], [6], '5-2', 'integration', 'g(x) = 2x² + 5x + 6, where x ∈ ℝ. Find ∫ g(x) dx.')
fK = 'The diagram shows the graph of a function f(x) = ax² + bx + c, where a, b, c ∈ ℤ. Three regions on the diagram are marked K, L, and N. Each of these regions is bounded by the x-axis, the graph of f(x), and two vertical lines.'
A('2-b-i', 'Q2(b)(i)', '10D', [10], [6], '5-2', 'integration', 'The area of region K is 538 square units. Use integration of f(x) to show that: 4a + 3b + 3c = 807', stem=fK)
A('2-b-ii', 'Q2(b)(ii)', '15D', [11], [7], '4-2', 'algebra-simultaneous-equations', 'The areas of the three regions K, L, and N give the following three equations (including the equation from part (b)(i)): 4a + 3b + 3c = 807; 28a + 9b + 3c = 879; 76a + 15b + 3c = 663. Solve these equations to find the values of a, b, and c.', stem=fK)
z = 'z = 6 + 2i, where i² = −1.'
A('3-a-i', 'Q3(a)(i)', '5C', [12], [8], '4-4', 'complex-numbers', 'Show that z − iz = 8 − 4i.', stem=z)
A('3-a-ii', 'Q3(a)(ii)', '10D', [12], [8], '4-4', 'complex-numbers', 'Show that |z|² + |iz|² = |z − iz|²', stem=z)
A('3-a-iii', 'Q3(a)(iii)', '5C', [12], [8, 9], '4-4', 'complex-numbers,co-ordinate-geometry-of-the-circle', 'The circle c passes through the points z, iz, and 0, as shown in the diagram below (not to scale). z and iz are endpoints of a diameter of the circle. Find the area of the circle c in terms of π.', stem=z)
A('3-b', 'Q3(b)', '10D', [13], [9], '4-4', 'complex-numbers', '(√3 − i)⁹ can be written in the form a + ib, where a, b ∈ ℤ and i² = −1. Use de Moivre’s Theorem to find the value of a and the value of b.')
A('4-a', 'Q4(a)', '10C', [14], [10], '4-1', 'sequences-series,indices-and-logs', 'A sequence u₁, u₂, u₃, ... is defined as follows, for n ∈ ℕ: u₁ = 2, u₂ = 64, uₙ₊₁ = √(uₙ/uₙ₋₁). Write u₃ in the form 2^p, where p ∈ ℝ.')
ar = 'The first three terms in an arithmetic sequence are as follows, where k ∈ ℝ: 5e^(−k), 13, 5e^k'
A('4-b-i', 'Q4(b)(i)', '10C', [14], [11], '4-1', 'sequences-series,indices-and-logs', 'By letting y = e^k in this arithmetic sequence, show that: 5y² − 26y + 5 = 0', stem=ar)
A('4-b-ii', 'Q4(b)(ii)', '10D', [15], [11], '3-2', 'indices-and-logs,algebra-quadratics', 'Use the equation in y in part (b)(i) to find the two possible values of k. Give each value in the form ln p or −ln p, where p ∈ ℕ.', stem=ar)
A('5-a', 'Q5(a)', '5B', [16], [12], '5-2', 'differentiation-rules', 'g(x) = x² − 1/x where x ∈ ℝ. Find g′(x), the derivative of g(x).')
f5 = 'f(x) = 2x³ − 21x² + 40x + 63, where x ∈ ℝ.'
A('5-b-i', 'Q5(b)(i)', '15D', [16], [12], '4-2', 'algebra-cubics', 'x + 1 is a factor of f(x). Find the three values of x for which f(x) = 0.', stem=f5)
A('5-b-ii', 'Q5(b)(ii)', '10D', [17], [13], '5-2', 'differentiation-applications,algebra-inequalities', 'Find the range of values of x for which f′(x) is negative, correct to 2 decimal places.', stem=f5)
A('6-a', 'Q6(a)', '15D', [18], [14], '5-2', 'differentiation-rules', 'Differentiate f(x) = 2x² + 4x with respect to x, from first principles.')
A('6-b', 'Q6(b)', '10D', [19], [14, 15], '5-2', 'differentiation-applications', 'A rectangle is expanding in area. Its width is x cm, where x ∈ ℝ and x > 0. Its length is always four times its width. Find the rate of change of the area of the rectangle with respect to its width, x, when the area of the rectangle is 225 cm².')
A('6-c', 'Q6(c)', '5C', [20], [15], '5-2', 'differentiation-applications,functions', 'The graph of a cubic function p(x) is shown in the first diagram below, for 0 ≤ x ≤ 4, x ∈ ℝ. The maximum value of p′(x) in this domain is 1, and p′(0) = −3, where p′(x) is the derivative of p(x). Use this information to draw the graph of p′(x) on the second set of axes below, for 0 ≤ x ≤ 4, x ∈ ℝ.')
h = 'Hannah is doing a training session. During this session, her heart-rate, h(x), is measured in beats per minute (BPM), where x is the time in minutes from the start of the session, x ∈ ℝ. For the first 8 minutes of the session, Hannah does a number of exercises. As she does these exercises, her heart-rate changes. In this time, h(x) is given by: h(x) = 2x³ − 28·5x² + 105x + 70'
A('7-a', 'Q7(a),Q7(b)', '10D', [21], [16], '5-2', 'differentiation-rules,functions', '(a) Work out Hannah’s heart-rate 4 minutes after the start of the session. (b) Find h′(x).', stem=h)
A('7-c', 'Q7(c)', '5C', [21], [16], '5-2', 'differentiation-applications', 'Find h′(2), and explain what this value means in the context of Hannah’s heart-rate.', stem=h)
hg = h + ' The graph below shows y = h(x), where 0 ≤ x ≤ 8, x ∈ ℝ.'
A('7-d', 'Q7(d)', '15D', [22], [17], '5-2', 'differentiation-applications', 'Find the least value and the greatest value of h(x), for 0 ≤ x ≤ 8, x ∈ ℝ. Use calculus in your solution. You may also use information from the graph above, which is to scale.', stem=hg)
A('7-e', 'Q7(e)', '10C', [22], [18], '5-2', 'differentiation-applications', 'How long after the start of the session is Hannah’s heart-rate decreasing most quickly, within the first 8 minutes? Give your answer in minutes and seconds. Remember that h(x) = 2x³ − 28·5x² + 105x + 70.', stem=h)
bkm = h + ' Bruno, Karen, and Martha start a training session at the same time as Hannah. All of their heart-rates are measured in BPM.'
A('7-f', 'Q7(f)(i),Q7(f)(ii)', '5C', [23], [18], '5-2', 'differentiation-rules', '(i) For the first 8 minutes of the session, Bruno’s heart-rate, b(x), is always 15 BPM more than Hannah’s heart-rate. Use this information to write b′(x) in terms of h′(x), where 0 ≤ x ≤ 8, x ∈ ℝ. (ii) For the first 8 minutes of the session, Karen’s heart-rate, k(x), is always 10% less than Hannah’s heart-rate. Use this information to write k′(x) in terms of h′(x), where 0 ≤ x ≤ 8, x ∈ ℝ.', stem=bkm)
A('7-g', 'Q7(g)', '5B', [23], [19], '5-1', 'functions', 'Martha does each exercise for a longer time than Hannah. For 0 ≤ x ≤ 10, Martha’s heart-rate, m(x), is: m(x) = h(0·8x). Use h(x) = 2x³ − 28·5x² + 105x + 70 to write m(x) in the form: m(x) = ax³ + bx² + cx + d, where a, b, c, d ∈ ℝ, for 0 ≤ x ≤ 10.', stem=bkm)
fw = 'A Ferris wheel has a diameter of 120 m. When it is turning, it completes exactly 10 full rotations in one hour. The diagram above shows the Ferris wheel before it starts to turn. At this stage, the point A is the lowest point on the circumference of the wheel, and it is at a height of 12 m above ground level. The height, h, of the point A after the wheel has been turning for t minutes is given by: h(t) = 72 − 60 cos(π/3 t), where h is in metres, t ∈ ℝ, and (π/3)t is in radians.'
trig = 'trigonometry-functions-identities'
A('8-a', 'Q8(a),Q8(b)', '15D', [24], [20, 21], '2-3', trig, '(a) Complete the table below for t = 0, 1, 2, …, 8. The value of h(1) is given: h(1) = 42. (b) Draw the graph of y = h(t) for 0 ≤ t ≤ 8, t ∈ ℝ.', stem=fw)
A('8-c', 'Q8(c)', '5C', [24], [21], '2-3', trig, 'Find the period and range of h(t).', stem=fw)
A('8-d', 'Q8(d)', '10C', [25], [21], '2-3', trig, 'During a 50-minute period, what is the greatest number of minutes for which the point A could be higher than 42 m?', stem=fw)
A('8-e', 'Q8(e)', '10D', [25], [22], '2-3', trig, 'By solving the following equation, find the second time (value of t) that the point A is at a height of 110 m, after it starts turning: 72 − 60 cos(π/3 t) = 110. Give your answer in minutes, correct to 2 decimal places.', stem=fw)
A('8-f', 'Q8(f)', '10D', [26], [23], '5-2', 'integration,' + trig, 'Use integration to find the average height of the point A over the first 8 minutes that the wheel is turning. Give your answer correct to 1 decimal place. Remember that h(t) = 72 − 60 cos(π/3 t).', stem=fw)
drug = 'Alex gets injections of a medicinal drug. Each injection has 15 mg of the drug. Each day, the amount of the drug left in Alex’s body from an injection decreases by 40%. So, the amount of the drug (in mg) left in Alex’s body t days after a single injection is given by: 15(0·6)^t, where t ∈ ℝ.'
A('9-a', 'Q9(a)', '5B', [27], [24], '3-2', 'indices-and-logs', 'Find the amount of the drug left in Alex’s body 2·5 days after a single 15 mg injection. Give your answer in mg, correct to 2 decimal places.', stem=drug)
A('9-b', 'Q9(b)', '10C', [27], [24], '3-2', 'indices-and-logs', 'How long after a single 15 mg injection will there be exactly 1 mg of the drug left in Alex’s body? Give your answer in days, correct to 1 decimal place.', stem=drug)
daily = drug + ' Alex is given a 15 mg injection of the drug at the same time every day for a long period of time.'
A('9-c', 'Q9(c)', '5A', [27], [25], '4-1', 'sequences-series', 'Explain why the total amount of the drug, in mg, in Alex’s body immediately after the 4th injection is given by: 15 + 15(0·6) + 15(0·6)² + 15(0·6)³', stem=daily)
A('9-d', 'Q9(d)', '10C', [27], [25], '4-1', 'sequences-series', 'Find the total amount of the drug in Alex’s body immediately after the 10th injection. Give your answer in mg, correct to 2 decimal places.', stem=daily)
A('9-e', 'Q9(e)', '5B', [28], [25], '4-1', 'sequences-series', 'Use the formula for the sum to infinity of a geometric series to estimate the amount of the drug (in mg) in Alex’s body, after a long period of time during which he gets daily injections.', stem=daily)
jess = 'Jessica also gets daily injections of a medicinal drug at the same time every day. She gets d mg of the drug in each injection, where d ∈ ℝ. Each day, the amount of the drug left in Jessica’s body from an injection decreases by 15%.'
A('9-f-i', 'Q9(f)(i)', '10C', [28], [26], '4-1', 'sequences-series', 'Use the sum of a geometric series to show that the total amount of the drug (in mg) in Jessica’s body immediately after the nth injection, where n ∈ ℕ, is: 20d(1 − 0·85ⁿ)/3', stem=jess)
A('9-f-ii', 'Q9(f)(ii)', '5C', [28], [26, 27], '4-1', 'sequences-series,algebra-solving-equations', 'Immediately after the 7th injection, there are 50 mg of the drug in Jessica’s body. Find the amount of the drug in one of Jessica’s daily injections. Give your answer correct to the nearest mg.', stem=jess + ' Part (f)(i) shows that the total amount of the drug (in mg) in Jessica’s body immediately after the nth injection is 20d(1 − 0·85ⁿ)/3.')
mem = 'A student is asked to memorise a long list of digits, and then write down the list some time later. The proportion, P, of the digits recalled correctly after t hours can be modelled by the function: P(t) = 0·82 − 0·12 ln(t + 1), for 0 ≤ t ≤ 12 and t ∈ ℝ.'
A('10-a', 'Q10(a)', '5B', [29], [28], '3-2', 'indices-and-logs', 'Find the proportion of the digits recalled correctly after 3 hours, according to this model. Give your answer correct to 2 decimal places.', stem=mem)
A('10-b', 'Q10(b)', '10D', [29], [28], '3-2', 'indices-and-logs', 'After how many hours would exactly 55% of the digits be recalled correctly, according to this model? Give your answer correct to 2 decimal places.', stem=mem)
A('10-c-i', 'Q10(c)(i),Q10(c)(ii)', '10C', [29], [29], '5-2', 'differentiation-rules,differentiation-applications', '(i) Find the value of P′(1). (ii) P′(t) is always negative for 0 ≤ t ≤ 12, t ∈ ℝ. What does this tell you about the proportion of digits recalled correctly after t hours, according to this model?', stem=mem)
A('10-d', 'Q10(d)', '10C', [30], [29], '5-2', 'differentiation-applications', 'Use calculus to show that the graph of y = P(t) has no points of inflection, for 0 ≤ t ≤ 12, t ∈ ℝ.', stem=mem)
skill = 'If we learn a skill, and then don’t practise it, how well we can do it usually decreases over time. For example, if you learn to play the guitar, and then don’t play the guitar for a number of months, you will probably not be as good at playing the guitar the first time you try it again. This effect can be modelled by the following equation: A = B(t + 1)^c, where A is a measure of how well the skill can be done at a certain time (t = 0); B is a measure of how well the skill can be done t months later, without practising; c is a constant; and A, B, c, t ∈ ℝ.'
A('10-e-i', 'Q10(e)(i)', '10C', [30], [30], '3-2', 'indices-and-logs', 'Write c in terms of log₁₀ A, log₁₀ B, and log₁₀(t + 1).', stem=skill)
A('10-e-ii', 'Q10(e)(ii)', '5C', [30], [30], '3-2', 'indices-and-logs', 'A student got 80% on a guitar exam. After two years of not playing the guitar, the student got 47% on the same exam. Use this to find the value of c in the model above, correct to 3 decimal places.', stem=skill)

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 43)
p.review(marks,
    'Independent visual reading of all 32 question-paper pages and PDF pages 1–31 of the combined Higher Level scheme (cover, notes, the Paper 1 scale table on page 4, the summary of allocations on page 5, annotation palette, every Paper 1 model solution and marking note, and the Paper 2 title page). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(1, 32)), [4, 5],
    ['The 2022 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '43 independently marked units, matching the printed summary of allocations on scheme page 5. Shared scales keep their parts together: Q1(c)(i)–(ii) 15D, Q7(a)–(b) 10D, Q7(f)(i)–(ii) 5C, Q8(a)–(b) 15D and Q10(c)(i)–(ii) 10C.',
     'Paper 1 bands from scheme page 4: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15D 0,4,8,12,15.',
     'All 43 units were already authored and shipping. Prompts are restored from the paper (several had lost superscripts, fractions and their preamble). Q3(b), Q6(b) and Q8(e) carried marking points garbled by the scheme text layer (interleaved columns, a stacked 15/2 read as “( )/2 15”); they are re-quoted line by line and labelled with their scheme band. Topics are corrected as metadata; all IDs are kept.',
     'The question booklet is LC003ALP100EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 2. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [27], 'wording': 'the amount of the drug in one of Jessica’s daily injections', 'classification': 'given-context',
      'reason': 'Every injection has the same size d; one value is required, not a choice of prompts.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('given-context', 'Every daily injection is the same d mg, so “one of” the injections names the single value required; there is no choice of prompts.') if 'one of Jessica' in t else None)
p.apply(ROWS, '2022 Higher Level Paper 1', ref_overrides={'maths-2022-hl-p1-q7-f': '2022 HL Paper 1 Q7(f)(i), (ii)'})
