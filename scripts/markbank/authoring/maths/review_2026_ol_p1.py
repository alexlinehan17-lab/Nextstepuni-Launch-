import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from solution_lib import Paper

OL_P1 = {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5],
         '10C': [0, 4, 7, 10], '10D': [0, 3, 5, 8, 10], '15C': [0, 5, 11, 15]}
p = Paper(
    year=2026, level='ordinary', paper_key='p1', paper_file='LC003GLP100EV.pdf', scheme_file='LC003GLP000EV.pdf',
    prefix='maths-2026-ol-p1', ref='2026 OL Paper 1', scales=OL_P1, reviewed_at='2026-10-11',
    general_notes=[3, 4, 6], scheme_pages=list(range(3, 23)),
    printed_marks={**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}},
    review_method='Independent visual reading of all 32 question-paper pages and PDF pages 3–22 of the combined Ordinary Level scheme (general notes, annotation palette, the Paper 1 scale table on page 6 and every Paper 1 model solution and marking note). Each task boundary is the published scale, not a parser count.',
    source_notes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained; no combined multi-question cards.',
        '42 independently marked units. Shared scales keep their parts together: Q1(b)(i)–(ii) 10D, Q3(c)(i)–(ii) 10D, Q4(c)(i)–(iii) 10D, Q5(a)(ii)–(iii) 10D, Q6(a)(i)–(ii) 15C, Q7(a)(i)–(ii) 10D, Q8(a)(i)–(ii) 10D, Q8(b)(ii)–(iii) 10D, Q9(a)(i)–(ii) 5C, Q10(a)(i)–(ii) 10C and Q10(a)(iv)–(v) 10D. Q10(b)(i)–(ii) and Q10(c)(i)–(ii) share one cross-letter 10D scale.',
        'Paper 1 bands from scheme page 6: 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10C 0,4,7,10; 10D 0,3,5,8,10; 15C 0,5,11,15. These differ from the Higher Level bands.',
        'The question booklet is LC003GLP100EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 2. All page references are PDF positions.',
        'Diagrams and tables (Argand diagrams, k(x) and its three candidate derivative graphs, the bus timetable, tax table, sales axes, running table, walkway, slide co-ordinate diagram and number lines) are read from the attached original question pages; prompts quote the paper’s own wording.',
        'Scheme text layers set some symbols as characters that do not match plain text (for example the h′(x) model line), so card rows quote only notes whose text layer matches the printed scheme; the scheme reader shows the full published notes.',
    ],
    out_name='2026-ordinary-p1.json', atlas_prefix='mathematics-ordinary-', section_of=lambda q: 'A' if q <= 6 else 'B',
)
A = p.add
A('1-a', 'Q1(a)', '10C', [7], [4], '3-3', 'financial-maths',
  'Sara pays for lunch for herself and a friend. Sara’s lunch costs €34·60 and her friend’s lunch costs €28·90. A service charge of 12% is then added on. Find the total cost of lunch, after the service charge has been added on.',
  ['(34·6 + 28·9)1·12 = [€]71·12', 'Accept correct answer without work', 'Finds total service charge (7·62)'])
A('1-b-i-ii', 'Q1(b)(i),Q1(b)(ii)', '10D', [7], [4], '3-3', 'financial-maths',
  '(i) How much does the car depreciate by in the 1st year? (ii) Find the value of the car after 2 years.',
  ['22 600 × 0·18 = 4068', '18 532 × 0·82 = [€]15 196·24', 'One part correct and work of merit in the other part'],
  stem='David buys a car for €22 600. It depreciates (goes down in value) by 18% each year, compounded annually.')
A('1-c', 'Q1(c)', '10C', [7], [5], '3-3', 'financial-maths',
  'A machine was bought for €28 000. The value of the machine depreciated by k% each year for 2 years, where k ∈ ℝ. After 2 years, the machine was valued at €20 230. Using the following formula, or otherwise, work out the value of k, where F is the value of the machine after t years and P is the initial value of the machine: F = P(1 − k/100)^t',
  ['k = 15%', 'Formula fully substituted', 'Work of merit, for example, some correct substitution or trial and improvement'])
A('2-a', 'Q2(a)', '10C', [8], [6], '4-1', 'algebra',
  'Expand and simplify: (3x − 5)² + 4x + 6',
  ['9x² − 26x + 31', '9x² − 30x + 25'])
A('2-b', 'Q2(b)', '15C', [8], [6], '4-2', 'algebra-equations',
  'Solve the following equation in x ∈ ℝ: 3x² − 4x − 5 = 0. Give each answer correct to 2 decimal places.',
  ['= 2·12', '= −0·79', 'Formula fully substituted', 'Apply a * for second value of x not found'])
A('2-c', 'Q2(c)', '5D', [8], [7], '4-2', 'algebra-equations',
  'Solve the following equation in x ∈ ℝ, where x ≠ 3, −3: 5/(x + 3) − 5/(x − 3) = 6',
  ['x = 2 , −2', 'Note: Use of CD leading to linear equation then LPC at most', 'Sets up quadratic equation'])
A('3-a', 'Q3(a)', '15C', [9], [8], '3-3', 'number-systems',
  'Kim is making bread. She prepares 2200 grams of bread mix. For every 500 grams of mix, she needs to bake it for 25 minutes. Work out how many minutes it takes to bake the bread.',
  ['4·4 × 25 = 110 [minutes]', 'Finds 4·4'])
A('3-b', 'Q3(b)', '5C', [9], [8], '3-1', 'number-systems',
  'Write 140 as a product of its prime factors.',
  ['2 × 2 × 5 × 7', 'Three prime factors of 140 identified', 'A correct product of 140 including two prime factors'])
A('3-c-i-ii', 'Q3(c)(i),Q3(c)(ii)', '10D', [9], [9], '4-1', 'algebra',
  '(i) Write down two factors of this function. (ii) Hence, or otherwise, find the value of p and the value of r, where p, r ∈ ℤ.',
  ['Factor one = x − 3', 'Factor two = x + 7', 'p = 4 r = −21'],
  stem='x² + px + r is a quadratic function in which p, r are constants. This function has roots at x = 3 and x = −7.')
i2 = 'In this question, i² = −1.'
A('4-a', 'Q4(a)', '10C', [10], [10], '3-1', 'complex-numbers',
  'The complex numbers z₁ and z₂ are shown on the Argand diagram below. Using the Argand diagram, write down the values of z₁ and z₂ in the form a + bi, where a, b ∈ ℤ.',
  ['z₁ = −2 + 3i', 'z₂ = 4 + i', 'Answers not given in the correct form'], stem=i2)
A('4-b', 'Q4(b)', '10C', [10], [10], '3-1', 'complex-numbers',
  'Find the value of the following expression: i(2 − i) + i²(2 − i). Give your answer in the form a + bi, where a, b ∈ ℤ.',
  ['−1 + 3i', 'Correct multiplication AND substitutes −1 for i²'], stem=i2)
A('4-c-i-ii-iii', 'Q4(c)(i),Q4(c)(ii),Q4(c)(iii)', '10D', [10], [11], '3-1', 'complex-numbers',
  '(i) Write down one possible complex number that u could be. Give your answer in the form a + bi, where a, b ∈ ℤ. (ii) Plot and label u̅ as accurately as you can on the Argand diagram above, where u̅ is the complex conjugate of u. (iii) Which of the complex numbers A, B, C, or D is equal to u + u̅? Tick one box only.',
  ['1 + 3i', '(iii) Box C ticked', 'Note: In (ii) if u̅ plotted correctly but not labelled apply * penalty for part (ii)'],
  stem=i2 + ' The complex number u is shown on the Argand diagram below. Four other complex numbers, labelled, A, B, C, and D, are also shown on the Argand diagram. The diagram is drawn to scale. Use the diagram to answer parts (c)(i) to (c)(iii).')
seq = 'The first three terms of an arithmetic sequence are: 12, 17, 22, …'
A('5-a-i', 'Q5(a)(i)', '5C', [11], [12], '4-1', 'sequences-series',
  'Write down the next three terms of the sequence.', ['27, 32, 37', 'Finds term four'], stem=seq)
A('5-a-ii-iii', 'Q5(a)(ii),Q5(a)(iii)', '10D', [11], [12], '4-1', 'sequences-series',
  '(ii) Find an expression for Tₙ, the nth term of the sequence. (iii) Hence, or otherwise, find the value of T₂₀, the 20th term in the sequence.',
  ['T₂₀ = 5(20) + 7 = 107', 'One part correct and work of merit in the other part'], stem=seq)
A('5-b', 'Q5(b)', '10C', [11], [13], '4-1', 'sequences-series',
  'The first three terms of a different arithmetic sequence are: 6, x, −4, … Find the value of x.',
  ['x = 1', 'Finds d'])
A('5-c', 'Q5(c)', '5D', [11], [13], '4-1', 'sequences-series',
  'The first three terms of another arithmetic sequence are: 43, 39, 35, … The first n terms of this sequence are added so that their sum is less than zero. Find the smallest such value of n.',
  ['n = 23', 'Answer given as 22·5', 'Sn formula fully substituted AND equated to 0 or < 0'])
A('6-a-i-ii', 'Q6(a)(i),Q6(a)(ii)', '15C', [12], [14], '5-1', 'functions',
  '(i) Find g(4). (ii) Find the value of x for which g(x) = 11.',
  ['g(4) = 2(4) − 3 = 5', 'x = 7', 'One part correct'], stem='The function g is defined as g(x) = 2x − 3, for x ∈ ℝ.')
A('6-b', 'Q6(b)', '10D', [12], [14], '5-2', 'differentiation',
  'The function h is defined as h(x) = 3x² − 2x + 1. Find h′(x), the derivative of h(x), and hence find the co-ordinates of the local minimum point of h.',
  ['6x − 2 = 0', 'Correct differentiation', 'Solves for x', 'Answer not written as a couple'])
A('6-c', 'Q6(c)', '5C', [12], [15], '5-2', 'differentiation,graphing-functions',
  'The diagram below shows the graph of the quadratic function k(x). The three diagrams below, A, B, and C, show the graphs of three linear functions. One of these is the graph of k′(x), that is, the derivative of k(x). Which of the graphs in the diagrams A, B, or C is the graph of k′(x)? Justify your answer. Tick one box only.',
  ['Box C ticked', 'Positive slope AND positive x intercept', 'Box C ticked and work of merit in explanation'])
timetable = 'Part of the bus timetable from Dublin Airport to Waterford Bus Station is shown below. Use the timetable to answer parts (a)(i), (a)(ii), and (a)(iii). The timetable on the original page gives the times of routes A to F at each stop from Dublin Airport to Waterford Bus Station.'
A('7-a-i-ii', 'Q7(a)(i),Q7(a)(ii)', '10D', [13], [16], '3-3', 'number-systems',
  '(i) Cathal took one of the buses from the table above and arrived in Waterford Bus Station between 18:00 and 21:00. Which bus did he take? Tick one box only: A, B, C, D, E or F. (ii) Work out how long it takes Bus B to travel from Dublin Airport to Waterford Bus Station.',
  ['Box D ticked', '14: 00 − 10: 50 = 3: 10', 'One part correct and work of merit in the other part'], stem=timetable)
A('7-a-iii', 'Q7(a)(iii)', '10C', [13], [16, 17], '3-3', 'number-systems,algebra-equations',
  'In the table, T represents the time that bus E arrives at Gowran. It takes bus E 3 minutes less to travel from Royal Oak to Gowran than it does to travel from Gowran to Thomastown. Find the time represented by T.',
  ['= 21: 33', 'Finds 9 minutes'], stem=timetable)
A('7-b', 'Q7(b)', '10D', [14], [17], '4-2', 'algebra-equations',
  'The cost of an adult ticket from Dublin Airport to Waterford Bus Station is €x and the cost of a child ticket is €y. 3 adult tickets and 4 child tickets cost €144. 2 adult tickets and 1 child ticket cost €71. Find the value of x and the value of y.',
  ['x = [€]28', 'y = [€]15', 'Two equations in terms of x and y written.'])
tax = 'Luan, Shea, and Tara are all PAYE workers. Their tax rates and bands are shown in the table below: the first €44 000 of annual income is taxed at 20% and the balance at 40%. Assume that no other deductions are made from their income.'
A('7-c-i', 'Q7(c)(i)', '5C', [14], [18], '3-3', 'financial-maths',
  'Luan has a gross annual income of €37 600. He only pays tax at the lower rate. He has an annual tax credit of €4000. Work out his net annual tax and hence work out his net annual pay.',
  ['7520 − 4000 = 3520', '37 600 − 3520 = [€]34 080', 'Apply a * if net annual tax is not written'], stem=tax)
A('7-c-ii', 'Q7(c)(ii)', '10D', [15], [18], '3-3', 'financial-maths',
  'Shea has a gross annual income of €63 400. He has an annual tax credit of €4000. Work out his net annual tax.',
  ['(16 560) − 4000 = [€]12 560', 'Finds tax paid at higher rate'], stem=tax)
A('7-c-iii', 'Q7(c)(iii)', '5D', [15], [18, 19], '3-3', 'financial-maths',
  'Tara has a net annual tax of €17 000. She pays income tax at both tax rates. She has an annual tax credit of €4000. Work out her gross annual income.',
  ['= [€]74 500', 'Finds gross pay at which higher rate is paid (30 500)'], stem=tax)
sales = 'The travel agency Sunshine Escapes are planning how much money to spend on advertising per month. They predict that their monthly sales can be modelled by the function: S(x) = −x³ + 9·6x² + 25, where S(x) is the monthly sales (in thousands of euro) and x is the amount spent on advertising per month (the advertising spend in thousands of euro), with 0 ≤ x ≤ 7, x ∈ ℝ.'
A('8-a-i-ii', 'Q8(a)(i),Q8(a)(ii)', '10D', [16], [20], '5-1', 'graphing-functions',
  '(i) Complete the table below to show the value of S(x) for each of the given values of x. Give each answer correct to the nearest whole number, where relevant. The table gives S(1) = 34, S(5) = 140 and S(7) = 152, and leaves x = 0, 2, 3, 4 and 6 to complete. (ii) Draw the graph of S(x) on the axes below, for 0 ≤ x ≤ 7, x ∈ ℝ.',
  ['Note: Solution requires 14 items, 5 values in table, 8 points plotted and the curve', 'Apply a * if 13 items correct'], stem=sales)
A('8-a-iii', 'Q8(a)(iii)', '5B', [16], [20], '5-1', 'graphing-functions',
  'Use your graph to estimate the advertising spend (in thousands of euro) that is needed to give monthly sales of €100 000. Show your work on the graph.',
  ['3·5 or 3500', 'Work of merit, for example, some relevant work on diagram'], stem=sales)
A('8-a-iv', 'Q8(a)(iv)', '10D', [17], [20, 21], '5-2', 'differentiation',
  'Use calculus to find the value of x that gives the maximum monthly sales according to the model. Remember: S(x) = −x³ + 9·6x² + 25.',
  ['S′(x) = −3x² + 19·2x', 'x = 6·4', 'Equates S′(x) to zero'], stem=sales)
A('8-a-v', 'Q8(a)(v)', '10C', [17], [20, 21], '3-3', 'number-systems',
  'The sales team spent €5000 on advertising in one particular month and the actual sales were €125 000 in the same month. Using the relevant value from the table on the previous page, find the percentage error in the predicted sales model, S(x), for that month.',
  ['Error = 140 000 − 125 000 = 15 000', 'Formula fully substituted'], stem=sales)
pay = 'The weekly pay for a holiday representative, €P, is given by the formula: P = rh + 2rt, where: r = hourly rate of pay; h = the number of hours worked at the hourly rate of pay, and t = the number of overtime hours worked.'
A('8-b-i', 'Q8(b)(i)', '5C', [17], [22], '4-1', 'algebra',
  'Philip has an hourly rate of pay of €15 per hour. On a particular week, Philip worked 39 hours at the hourly rate of pay. He also worked 5 hours overtime. Find Philip’s pay for this week.',
  ['P = [€]735', 'Fully correct substitution into P'], stem=pay)
A('8-b-ii-iii', 'Q8(b)(ii),Q8(b)(iii)', '10D', [18], [22], '4-1', 'algebra',
  '(ii) Rearrange the formula P = rh + 2rt to write r in terms of P, h, and t. (iii) Philip’s hourly rate of pay is increased. The next week he is paid a total of €892·50 for working 35 hours at the hourly rate of pay and 8 hours overtime. Using your answer from (b)(ii), or otherwise, work out Philip’s new hourly rate of pay.',
  ['= [€]17·5 [per hour]', 'One part correct and work of merit in the other part'], stem=pay)
club = 'Dean, Saoirse, Kayla, and Olor are all members of a running club.'
runs = club + ' Dean does a number of sets as part of his running training session. One set consists of four 10-second runs and four 10-second rests. The times and the distances for each run are shown in the table below: Run 1 38 m, Run 2 41 m, Run 3 44 m and Run 4 41 m, each run and each rest taking 10 seconds. For example, in Run 1 Dean runs 38 m.'
A('9-a-i-ii', 'Q9(a)(i),Q9(a)(ii)', '5C', [19], [23], '3-3', 'number-systems',
  '(i) Find how many seconds it takes Dean to do one set, that is, find the total time of the 4 runs and 4 rests. (ii) Find the distance, in metres, that Dean runs in one set.',
  ['80 [seconds]', '164 [metres]', 'One part correct'], stem=runs)
A('9-a-iii', 'Q9(a)(iii)', '10C', [19], [23], '3-3', 'number-systems',
  'Dean keeps repeating the set above. Find the total distance Dean will have run after 7 minutes.',
  ['820 + 38 = 858 m', '5 full sets plus 20 seconds', 'Apply a * for no units'], stem=runs)
A('9-b', 'Q9(b)', '10D', [19], [24], '3-3', 'financial-maths',
  'Dean, Saoirse, Kayla, and Olor enter the London marathon. The entry fee is £80 sterling per person plus a carbon offset levy of £145 sterling per person. The total cost, in euro, for the 4 people is €1020. Work out the exchange rate used, that is, work out how much sterling is equal to €1. Give your answer correct to 3 decimal places.',
  ['€1 = [£]0·882', 'Finds 225 AND 255', 'Finds 900'], stem=club)
A('9-c', 'Q9(c)', '10C', [19], [24], '3-3', 'number-systems',
  'Saoirse completes a 5 km run in 25 minutes. Work out her average speed for the 5 km run. Give your answer in metres per second correct to 1 decimal place.',
  ['= 3·3 [m/s]'], stem=club)
walk = club + ' The diagram below shows a walkway, from the start point A to the point B. The length of the walkway is 4·8 km. When a person reaches the point B they must then go back to the start point A. Kayla and Olor both leave the point A at the same time. Kayla is running 2 times as fast as Olor is walking, and they both move at a constant speed.'
A('9-d-i', 'Q9(d)(i)', '5B', [20], [25], '3-3', 'number-systems',
  'When Kayla reaches the point B, how far will Olor have walked?',
  ['2·4 km', 'Apply a * for no units'], stem=walk)
A('9-d-ii', 'Q9(d)(ii)', '10C', [20], [25], '3-3', 'number-systems',
  'Work out the distance Olor will have walked from A, in km, when he meets Kayla, as she is running back along the walkway from B to A.',
  ['= 3·2 [km]', 'Identifies ratio as 2: 1', 'Finds 6·4 (distance run by Kayla)'], stem=walk)
slide = 'The co-ordinate diagram below shows the cross section of the ladder and top of a child’s slide. A, B, and C are points on the slide. The slide is on horizontal ground (x-axis). Each unit in the diagram is 1 m. The ladder, labelled l(x), goes from the point A to the point B. The top of the slide goes from the point B to the point C. You will draw the downward part of the slide later.'
A('10-a-i-ii', 'Q10(a)(i),Q10(a)(ii)', '10C', [21], [26], '2-2', 'co-ordinate-geometry-of-the-line',
  '(i) Write down the height of the slide in metres. (ii) Write down the length of the top of the slide, that is, the distance from B to C. Give your answer in centimetres.',
  ['2 [m]', '40 [cm]', 'In (ii) answer given as 0·4'], stem=slide)
A('10-a-iii', 'Q10(a)(iii)', '10C', [21], [26, 27], '5-2', 'differentiation,co-ordinate-geometry-of-the-line',
  'In the diagram on the previous page, the graph of the function l(x) from A to B represents the ladder, where: l(x) = 2·5x + 3. Find l′(x) and explain what this means in the context of the question.',
  ['l′(x) = 2·5', 'Slope of the ladder', 'l′(x) = 2·5 written but explanation is incorrect'], stem=slide)
A('10-a-iv-v', 'Q10(a)(iv),Q10(a)(v)', '10D', [21], [26, 27], '5-1', 'graphing-functions',
  '(iv) Complete the table below to show the value of d(x) for each of the given values of x. Give each value of d(x) correct to 2 decimal places, where relevant. The table gives d(0) = 2, d(0·2) = 1·45, d(0·8) = 0·55 and d(1·6) = 0·15, and leaves x = 0·4, 0·6, 1, 1·2 and 1·4 to complete. (v) Draw the graph of d(x) on the axes on the previous page, for 0 ≤ x ≤ 1·6, x ∈ ℝ.',
  ['Note: Solution requires 14 items, 5 values in table, 8 points plotted and the curve', 'Apply a * if 13 items correct'],
  stem=slide + ' The height of the downward part of the slide can be modelled by the function: d(x) = 2 × 0·2^x, where d(x) is the height of the slide, for 0 ≤ x ≤ 1·6, x ∈ ℝ.')
A('10-b-c', 'Q10(b)(i),Q10(b)(ii),Q10(c)(i),Q10(c)(ii)', '10D', [22], [28], '4-3', 'algebra',
  '(b) All children using the slide must be at least 95 cm tall. (i) By writing in the missing symbol (<, >, ≤, or ≥), complete the inequality below to show this information, where h cm is the height of a child: h ☐ 95. (ii) Graph the inequality from part (b)(i) on the following number line for h ∈ ℝ, showing the allowable heights. (c) All children using the slide must also be at least 4 years old but younger than 12 years old. (i) By writing in the missing symbols, complete the inequality below to show this information, where A years is the age of a child: 4 ☐ A ☐ 12. (ii) Graph the inequality from part (c)(i) on the following number line for A ∈ ℝ, showing the allowable ages.',
  ['4 years ≤ A < 12 years', '(b) OR (c) correct', 'Work of merit in (b) AND (c)'],
  stem='Another slide in a children’s play area has two restrictions on its use.')
A('10-d', 'Q10(d)', '10C', [22], [29], '3-3', 'number-systems',
  'It takes 4 employees 13 hours working together to make a slide. On a particular day, the 4 employees work together for 2 hours making a slide. Then 1 employee leaves and the other 3 continue to finish making the slide. Find how long it takes the remaining 3 employees to finish making the slide. Assume that all employees work at the same rate. Give your answer in hours and minutes.',
  ['= 14 [hours] 40 [minutes]', 'Finds 44', 'Apply a * if answer given in hours or minutes'])

selection_review = [
    {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
     'reason': 'Candidates select independently marked questions; every question is retained. No combined multi-question practice cards.'},
    {'pages': [5, 9, 12, 22], 'wording': 'or otherwise / hence, or otherwise', 'classification': 'method-choice',
     'reason': 'Alternative solution methods for the same marked task; no printed pool of prompts.'},
    {'pages': [11, 15, 16], 'wording': 'Tick one box only', 'classification': 'answer-selection',
     'reason': 'Choosing the correct complex number, derivative graph or bus is the mathematical answer to one required task, not a choice of practice prompts.'},
    {'pages': [11], 'wording': 'one possible complex number that u could be', 'classification': 'open-answer',
     'reason': 'Any value consistent with the scale drawing earns the same scale (“Or similar”); nothing finite to expand.'},
]
def classify(c):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        return ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    if 'or otherwise' in t:
        return ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    if 'One of these is the graph' in t:
        return ('answer-selection', 'Exactly one of the three printed graphs is k′(x); identifying it with justification is one required task, not a choice of prompts.')
    if 'took one of the buses' in t:
        return ('answer-selection', 'The timetable determines the one bus that arrives between 18:00 and 21:00; this is the answer to a required task, not a choice of prompts.')
    return None
p.write(selection_review, classify)
