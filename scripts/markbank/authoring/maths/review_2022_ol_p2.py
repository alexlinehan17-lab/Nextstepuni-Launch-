"""2022 OL Paper 2: review ledger, restored prompts, add Q9(d), re-quote garbled rows, move welded deductions."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *

ROWS = {
 'maths-2022-ol-p2-q5-b': [L(SOL, '|GK|² = |GH|² + |HK|²'), L(SOL, '|HK|² = 756'), L(SOL, '|HK| = 27.5cm'),
     L(LPC, 'Pythagoras Theorem written'), L(MPC, 'A fully correctly-substituted formula'), L(HPC, '|HK| = √756'),
     L(FCM, 'Correct answer, no unit or incorrect unit'), L(FCM, 'Correct answer, incorrect rounding')],
 'maths-2022-ol-p2-q6-a-i': [L(SOL, '90°'), L(NOTE, 'Hit or Miss')],
 'maths-2022-ol-p2-q6-a-iii': [L(SOL, 'Minor arc:'), L(SOL, '130/360 × 2π(18) = 13π [cm]'), L(SOL, 'Major arc:'), L(SOL, '(360 − 130)/360 × 2π(18) = 23π [cm]'),
     L(LPC, 'Work of merit'), L(LPC, 'Correct relevant formula written'), L(HPC, 'Finds circumference'),
     L(HPC, 'Fully correctly-substituted arc-length formula'), L(HPC, 'Answer not in terms of π'),
     L('Misreading (−1)', 'If a different arc is correctly calculated')],
 'maths-2022-ol-p2-q7-a-ii': [L(SOL, 'That the weight of the dogs has increased from Day X to Day Y'), L(PC, 'Work of merit'),
     L(NOTE, 'Word ”Increase” or similar must feature in conclusion.')],
 'maths-2022-ol-p2-q8-a-ii': [L(SOL, 'So h = 4 m'), L(LPC, 'Formula for cylinder written with no substitution'), L(LPC, 'Substitutes r = 3 into cylinder formula'),
     L(LPC, 'Sets cylinder formula = 36π'), L(MPC, 'Forms correct equation in h'),
     L(HPC, 'Correct equation in h and further significant work of merit in solving for h')],
 'maths-2022-ol-p2-q8-b-i': [L(SOL, 'A = 80·93349°'), L(SOL, 'A = 81°[nearest degree]'), L(LPC, 'Correct trigonometric ratio'),
     L(LPC, 'a² = (7·5)² + (47)²'), L(HPC, 'Fully substituted trigonometric ratio'),
     L(HPC, 'Incorrect calculator mode but otherwise correct (only once in the paper)')],
 'maths-2022-ol-p2-q9-d': [L(NOTE, '|AB| ≅ 4·0 cm'), L(NOTE, '|AC| ≅ 4·6 cm'), L(NOTE, '|AD| ≅ 3·5cm'), L(NOTE, '|AE| ≅ 2·4 cm'),
     L(LPC, 'Work of merit'), L(LPC, 'Draws enlarged image correctly without construction line.'),
     L(LPC, 'Draws THREE or FOUR rays with at least one image point marked'), L(LPC, 'Marks off any of the image points to satisfy the Scale Factor (3)'),
     L(HPC, 'Draws ray AD1 along with TWO other correct rays and at least ONE correct image point'),
     L(HPC, 'Constructs D1 along with TWO other correct image points')],
 'maths-2022-ol-p2-q10-b-i': [L(SOL, 'M.E. = 1/√1500'), L(SOL, '= 0·0258 × 100'), L(SOL, '= 2·58 %'), L(SOL, '= 2·6 %'),
     L(LPC, '1/√n written and stops'), L(HPC, 'Formula substituted correctly but not evaluated'), L(HPC, 'Answer given as 0.0258'),
     L(FC, 'Correct answer with supporting work')],
 'maths-2022-ol-p2-q10-b-iii': [L(SOL, '71 − 2·6 ≤ p ≤ 71 + 2·6'), L(SOL, '68·4 ≤ p ≤ 73·6 [C.I.]'),
     L(SOL, 'Reject the Null hypothesis and conclude that the figure of 65% has changed in 2022'), L(SOL, 'The figure 65% is outside the 95% C.I.'),
     L(LPC, 'Work of merit'), L(LPC, 'Either lower or upper boundary as 68·4 or 73·6 in (iii)'),
     L(LPC, 'Conclusion without reason correct in part (iv)'), L(LPC, 'Reason without interpretation knowledge shown in part (iv)'),
     L(MPC, 'Either part (iii) or part (iv) correct'), L(MPC, 'Significant work of merit in both parts (Correct substitution in both parts)'),
     L(HPC, 'Either part correct and significant work in the other part')],
 'maths-2022-ol-p2-q10-e': [L(SOL, 'Gold − Silver = €670 − €420 = €250'), L(SOL, 'So least number = 42 [classes]'), L(SOL, '420 + 6n > 670'),
     L(SOL, 'n = 42 [as n ∈ ℕ]'), L(LPC, 'One relevant operation'), L(LPC, '420 + 6n or similar'),
     L(HPC, '420 + 6n > 670 and further work: finds 6n > 250 or mishandles 420 but divides by 6 to find n'),
     L(FCM, 'Finds n, but no or incorrect rounding')],
}
if len(sys.argv) > 1: quotes(ROWS, sys.argv[1]); raise SystemExit

p = Paper(2022, 'ol', 'p2', {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 3, 7, 10],
          '10D': [0, 3, 5, 8, 10], '15D': [0, 4, 8, 12, 15]}, 'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
line = 'co-ordinate-geometry-of-the-line'; circ = 'co-ordinate-geometry-the-circle'; st = 'statistics'; pr = 'probability'
q1 = 'Parts of the lines AC and BC are shown in the co-ordinate diagram below (not to scale): A is on the x-axis at (−2, 0), C is on the y-axis at (0, 3), and B is on the x-axis at (5, 0).'
A('1-a-i', 'Q1(a)(i)', '5C', [33], [4], '2-2', line, 'Find the slope of AC.', stem=q1)
A('1-a-ii', 'Q1(a)(ii)', '10C', [33], [4], '2-2', line, 'By using slopes, investigate if AC is perpendicular to BC. Justify your answer. (Tick one box only: AC is perpendicular to BC; AC is not perpendicular to BC.)', stem=q1)
lmn = 'The triangle LMN is shown on the co-ordinate diagram below (not to scale). The point M has co-ordinates (9, 1). The triangle LMN is symmetrical about the y-axis.'
A('1-b-i', 'Q1(b)(i),Q1(b)(ii)', '5C', [34], [5], '2-2', line, '(i) Find the length |LM|. (ii) Write down the equation of the horizontal line LM.', stem=lmn)
A('1-b-iii', 'Q1(b)(iii)', '10C', [34], [5], '2-2', line, 'The line NM has equation x + 4y − 13 = 0, where x, y ∈ ℝ. Use this equation to find the co-ordinates of the point N.', stem=lmn)
k = 'The circle k has equation (x − 4)² + (y + 2)² = 169.'
A('2-a-i', 'Q2(a)(i)', '10C', [35], [6], '2-2', circ, 'Write down the centre and radius of the circle k.', stem=k)
A('2-a-ii', 'Q2(a)(ii)', '5C', [35], [6], '2-2', circ, 'Is the point (11, 10) on the circle k, inside the circle k, or outside the circle k? Show your working out. (Tick one box only.)', stem=k)
st2 = 'The diagram below shows two circles, s and t. The circle s has centre (22, 13). The two circles touch at the point (12, 11).'
A('2-b-i', 'Q2(b)(i)', '5B', [36], [7], '2-2', circ, 'Find the co-ordinates of another point on the circle s, other than (12, 11).', stem=st2)
A('2-b-ii', 'Q2(b)(ii)', '10C', [36], [7], '2-2', circ, 'The radius of the circle t is half the radius of s. Find the co-ordinates of the centre of the circle t.', stem=st2)
nums = 'A list of 7 numbers is shown below: 17, 8, 9, 8, 14, 11, 28'
A('3-a-i', 'Q3(a)(i)', '5C', [37], [8], '1-6', st, 'Find the mean of these 7 numbers, correct to 1 decimal place.', stem=nums)
A('3-a-ii', 'Q3(a)(ii)', '5B', [37], [8], '1-6', st, 'Find the median of these 7 numbers.', stem=nums)
A('3-a-iii', 'Q3(a)(iii)', '5C', [37], [8], '1-6', st, 'One more number is added to the list. The new median is 10·5. Find the number that was added to the list.', stem=nums)
ben = 'Ben has to choose three subjects to study. He must pick one subject from each of these three groups: Group A (3 subjects): French, Spanish, German. Group B (4 subjects): Biology, Physics, Chemistry, Business. Group C (5 subjects): Art, Accounting, History, Geography, Home Economics.'
A('3-b-i', 'Q3(b)(i)', '5B', [38], [9], '1-1', 'counting', 'How many different choices of three subjects can Ben make, picking one from each group?', stem=ben)
A('3-b-ii', 'Q3(b)(ii)', '10C', [38], [9], '1-1', 'counting', 'The school is going to add one extra subject to one of these groups (A, B, or C). Which group should the extra subject be added to, in order to make the number of different choices of three subjects that Ben can make as large as possible? Justify your answer.', stem=ben)
A('4-a', 'Q4(a)', '15D', [39], [10], '1-6', st, 'A group of students sat an exam. Each student was given a grade. The following table shows how many students got each grade: Distinction 8, High Merit 12, Merit 39, Achieved 13. Complete the pie chart below to show this information. Label each sector clearly. Show your working out. The sector for Distinction is already given. It has an angle of 40°.')
read = 'A large group of people took a reading test. The scores were normally distributed, with a mean of 100 and a standard deviation of 20. Use the empirical rule to answer parts (b)(i) and (b)(ii).'
A('4-b-i', 'Q4(b)(i),Q4(b)(ii)', '10C', [40], [11], '1-3', st, '(i) What percentage of the people had scores between 80 and 120? (ii) The top 2·5% of scores were given a grade of ‘Exceptional’. What was the least score that was needed to get this grade?', stem=read)
A('4-c', 'Q4(c)', '5C', [41], [11], '1-6', st, 'The scores of six people on this test were as follows: 104, 82, 94, 113, 98, 105. Find the range and the standard deviation of these numbers. Give the standard deviation correct to 1 decimal place.')
pqr = 'An equilateral triangle PQR has sides of length 8 cm.'
tr = 'trigonometry'
A('5-a-i', 'Q5(a)(i),Q5(a)(ii)', '10C', [42], [12], '2-3', tr + ',geometry', '(i) Write down the size of the angle ∠PQR. (ii) Show that the area of the triangle PQR is 16√3 cm².', stem=pqr)
A('5-a-iii', 'Q5(a)(iii)', '10C', [42], [12], '2-3', tr, 'Hence, or otherwise, find the perpendicular height of the triangle PQR, taking PQ as the base. Give your answer in the form a√b cm, where a, b ∈ ℕ.', stem=pqr + ' The area of the triangle PQR is 16√3 cm².')
A('5-b', 'Q5(b)', '10D', [43], [13], '2-3', tr, 'GHK is a right-angled triangle. |∠GHK| = 90°, |GH| = 12 cm, and |GK| = 30 cm. Using the theorem of Pythagoras, find the distance |HK|. Give your answer correct to 1 decimal place.')
circ6 = 'The circle c is shown in the diagram below (not to scale). Its centre is at the point O. The points A, B, and D lie on the circle, and [AB] is a diameter of the circle.'
A('6-a-i', 'Q6(a)(i)', '5A', [44], [14], '2-1', 'geometry', 'Write down |∠ADB|, the size of the total angle at the point D.', stem=circ6)
A('6-a-ii', 'Q6(a)(ii)', '5C', [44], [14], '2-1', 'geometry', '|∠AOD| = 130°. Work out the size of the angle marked X in the diagram.', stem=circ6)
A('6-a-iii', 'Q6(a)(iii)', '10C', [45], [14], '3-4', 'area-volume', 'The radius of the circle is 18 cm. Find the length of the arc AD. Give your answer in cm, in terms of π.', stem=circ6 + ' |∠AOD| = 130°.')
A('6-b-i', 'Q6(b)(i),Q6(b)(ii)', '10D', [45], [15], '2-1', 'geometry', 'For each statement, put a tick (✓) in the correct box to show if it is true or false. Give a reason for your answer in each case. (i) Statement A: If two triangles are similar, then they must be congruent. (ii) Statement B: If two triangles are congruent, then they must be similar.', stem='Two statements, A and B, are shown below.')
dogs = 'An animal shelter takes cats and dogs. The staff record the weight of each animal in the shelter on two different days: the day they are taken in to the shelter (Day X) and a number of days later (Day Y). The table below shows the weights of 10 dogs (labelled A to J) on these two days. Weight Day X (kg): 4·5, 4·9, 5·3, 5·3, 5·5, 5·7, 6·7, 6·9, 7·3, 7·4. Weight Day Y (kg): 4·8, 5·4, 5·5, 6·1, 6·3, 6·0, 7·0, 7·6, 8·1, 7·9.'
A('7-a-i', 'Q7(a)(i)', '15D', [46], [16], '1-6', st, 'Draw a back-to-back stem-and-leaf plot to show this information. (Key: 6 | 0 = 6·0 kg)', stem=dogs)
A('7-a-ii', 'Q7(a)(ii)', '5B', [46], [16], '1-6', st, 'What does the stem-and-leaf plot show about the weights of the dogs on Day X and Day Y?', stem=dogs)
A('7-a-iii', 'Q7(a)(iii)', '5B', [46], [17], '1-6', st, 'r is the correlation coefficient between the weight on Day X and the weight on Day Y. Based on the data in the table, pick the most likely value of r from the list below. Give a reason for your answer, based on the data in the table. Most likely value of r (tick one box only): −0·9, −0·2, 0·2, 0·9.', stem=dogs)
shelter = 'An animal shelter takes cats and dogs. The table below shows the breakdown of the animals in the shelter, by type of animal (cat or dog) and by sex (male or female), on a particular Monday. Cats: 5 male, 9 female, 14 in total. Dogs: 11 male. Total: 40 animals.'
A('7-b', 'Q7(b)', '10D', [47], [18], '1-2', pr, 'Complete the table, by filling in the four missing values.', stem=shelter)
A('7-c-i', 'Q7(c)(i),Q7(c)(ii)', '5D', [47], [18], '1-2', pr, '(i) Find the probability that the first animal picked was a cat. (ii) Find the probability that all three animals picked were male dogs. Give your answer correct to 3 decimal places.', stem=shelter + ' Three different animals were picked at random from the animals in the shelter on this Monday.')
A('7-d', 'Q7(d)', '5B', [47], [19], '1-1', 'counting', 'The 9 female cats were put in 9 separate pens. Work out the number of ways in which this could have been done (that is, the number of different possible arrangements).', stem=shelter)
A('7-e', 'Q7(e)', '5C', [48], [19], '1-2', pr, 'By the end of this week, 10 of the animals had left the shelter, and no new animals had been taken in. If an animal was picked at random at the end of this week, the probability of picking a dog would be 11/15. Work out how many cats left the shelter during this week.', stem=shelter)
light = 'The top of a particular lighthouse is in the shape of a hemisphere on top of a cylinder. The hemisphere and the cylinder both have a radius of 3 m.'
av = 'area-volume'
A('8-a-i', 'Q8(a)(i)', '5C', [49], [20], '3-4', av, 'Find the volume of the hemisphere. Give your answer in m³ in terms of π.', stem=light)
A('8-a-ii', 'Q8(a)(ii)', '10D', [49], [20], '3-4', av, 'The volume of the cylinder is 36π m³. Work out h, the height of the cylinder.', stem=light)
base = 'The diagram on the right below shows part of the base of the lighthouse (not to scale). It is in the shape of a cone of radius 7·5 m, from which the top part has been removed, leaving a horizontal circle of radius 3 m.'
A('8-b-i', 'Q8(b)(i)', '5C', [50], [21], '2-3', tr, 'The height of the cone before the top part is removed is 47 m. Work out the size of the angle at the base of the cone, marked A in the diagram above. Give your answer correct to the nearest degree.', stem=base)
A('8-b-ii', 'Q8(b)(ii)', '5C', [50], [21], '2-3', tr + ',geometry', 'Find the distance marked k on the diagram, the height after the top part is removed.', stem=base + ' The height of the cone before the top part is removed is 47 m.')
fast = 'Assume that the Fastnet lighthouse can be seen from anywhere within a circle of radius 50 km.'
A('8-c-i', 'Q8(c)(i)', '5B', [51], [22], '3-4', av, 'Work out the area of the circle within which the Fastnet lighthouse can be seen. Give your answer correct to the nearest km².', stem=fast)
A('8-c-ii', 'Q8(c)(ii)', '10B', [51], [22], '3-3', 'number-systems', '50 km = 27 nautical miles. Use this to work out how many km are in 1 nautical mile. Give your answer correct to 4 significant figures.', stem=fast)
A('8-d', 'Q8(d)', '10D', [51], [23], '2-3', tr, 'The top of the Fastnet lighthouse, F, is 49 m above sea level. The angle of elevation of the top of the lighthouse from a ship S is 1·2°, as shown in the diagram below (not to scale). Find the horizontal distance marked d below, from the ship to the base of the lighthouse. Give your answer in kilometres, correct to 2 decimal places.')
shed = 'Seán has built a shed. The diagrams below show the dimensions of Seán’s shed. The shed is in the shape of a prism. Its front face is in the shape of a triangle on top of a rectangle. Its highest point is directly above the centre of its base. The front face is 12 m wide, its walls are 7 m high and its highest point is 8·5 m high; the shed is 18 m long.'
A('9-a', 'Q9(a)', '5B', [52], [24], '3-3', 'number-systems', 'State which of the following statements is most likely to be true, and write down a possible height of Seán that would support your answer. Tick (✓) one box only: The shed at the highest point is 3 times as high as Seán; 5 times as high as Seán; 8 times as high as Seán.', stem=shed)
A('9-b', 'Q9(b)', '10D', [52], [24, 25], '3-4', av, 'Seán says that his shed has a capacity of over one million litres, where 1 m³ = 1000 litres. Work out the volume of Seán’s shed, to show that he is correct.', stem=shed)
A('9-c', 'Q9(c)', '10D', [53], [25], '2-3', tr, 'Use the theorem of Pythagoras to find the length of the distance marked d in the diagram below, the slant length of the roof. Give your answer in metres, correct to 1 decimal place.', stem=shed)
A('9-d', 'Q9(d)', '10C', [54], [26], '2-4', 'geometry', 'A scale diagram of the front of the shed is shown below. One point on the diagram is marked A. Construct an enlargement of the diagram below, with centre A and a scale factor of 3. Show all of your construction lines clearly.', stem=shed, extra={'measurementRequired': True})
roof = 'The diagram below shows part of the roof of a smaller shed (not to scale). Some measurements are marked on the diagram: |AB| = 3 m, |AC| = 7 m and |∠BAC| = 30°.'
A('9-e-i', 'Q9(e)(i)', '10D', [55], [27], '2-3', tr, 'Show that |BC| = 4·65 m, correct to 2 decimal places.', stem=roof)
A('9-e-ii', 'Q9(e)(ii)', '5C', [56], [27], '2-3', tr, 'Find |∠ACB|, the angle that the roof makes at the point C. Give your answer correct to the nearest degree. Remember that |BC| = 4·65 m, correct to 2 decimal places.', stem=roof)
surv = 'A survey was carried out to investigate the amount and type of exercise that adults in Ireland are taking in 2022. This survey was carried out on a sample of adults in Ireland.'
A('10-a', 'Q10(a)', '5B', [57], [28], '1-5', st, 'Write down one advantage and one disadvantage of carrying out a survey on a sample instead of a population.', stem=surv)
A('10-b-i', 'Q10(b)(i)', '5C', [57], [28], '1-7', st, 'A random sample of 1500 people took part in the survey. Show that the margin of error for the survey is 2·6%, correct to 1 decimal place.', stem=surv)
A('10-b-ii', 'Q10(b)(ii)', '5B', [57], [28], '1-5', st, '71% of the sample said that they walk for recreation. Find the number of people from the sample who said that they walk for recreation.', stem=surv + ' A random sample of 1500 people took part in the survey.')
A('10-b-iii', 'Q10(b)(iii),Q10(b)(iv)', '10D', [58], [29], '1-7', st, '(iii) Use the percentages given in (b)(i) and (b)(ii) to write down a 95% confidence interval for the percentage of all adults in Ireland who walk for recreation, in 2022. (iv) According to the 2019 Irish Sport Monitor Report, 65% of the adults in Ireland walked for recreation. Carry out a Hypothesis Test, at the 5% level of significance, to find out if this figure of 65% has changed in 2022, based on the results of the above survey. Clearly state your conclusion and give a reason for your conclusion.', stem=surv + ' A random sample of 1500 people took part in the survey; the margin of error is 2·6%. 71% of the sample said that they walk for recreation.')
A('10-c', 'Q10(c)', '5C', [58], [29], '1-2', pr, 'Assume that 20% of adults in Ireland jog for recreation. Three adults are picked at random. Find the probability that exactly one of these adults jogs for recreation.')
gym = 'Sinéad is joining a gym. She will be able to use the gym, and also go to classes.'
A('10-d', 'Q10(d)', '10C', [58], [30], '1-3', pr, 'She could pay for individual classes, at €6 per class. Sinéad estimates that there is: a 30% chance she will go to no classes in the year, a 60% chance she will go to 1 class a week, so 52 classes in a year, and a 10% chance she will go to 2 classes a week, so 104 classes a year. Use these figures to work out the expected value of the cost of the classes for a year.', stem=gym)
A('10-e', 'Q10(e)', '10C', [59], [30], '3-3', 'financial-maths', 'There are two price plans for the gym, Silver and Gold, as follows: Silver, €420 for the year and pay €6 for each class; Gold, €670 for the year and all classes are free. Work out the least number of classes that Sinéad would have to go to in a year, so that the Gold plan would cost less than the Silver plan.', stem=gym)

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 50)
p.review(marks,
    'Independent visual reading of all 32 question-paper pages and PDF pages 29–60 of the combined Ordinary Level scheme (Paper 2 title page, the Paper 2 scale table on page 30, the summary of allocations on page 31, annotation palette, every Paper 2 model solution and marking note, and the closing page). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(29, 61)), [30, 31],
    ['The 2022 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '50 independently marked units, matching the printed summary of allocations on scheme page 31. Shared scales keep their parts together: Q1(b)(i)–(ii) 5C, Q4(b)(i)–(ii) 10C, Q5(a)(i)–(ii) 10C, Q6(b)(i)–(ii) 10D, Q7(c)(i)–(ii) 5D and Q10(b)(iii)–(iv) 10D.',
     'Paper 2 bands from scheme page 30: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,3,5,8,10; 15D 0,4,8,12,15. They differ from Paper 1, which prints no A, 5D or 10B scales.',
     'Before this review the deck held 49 of the 50 units. Q9(d) (enlargement of the shed diagram, centre A, scale factor 3; 10C) had no card and is added with the page measuring tool, since the scheme checks image lengths in centimetres. Ten cards had their marking points re-quoted from the printed scheme because the text layer had garbled them: Q5(b) and Q8(a)(ii) interleaved bands, Q6(a)(i) carried the diagram labels as its marking points, and Q6(a)(iii), Q7(a)(ii), Q8(b)(i), Q10(b)(i), Q10(b)(iii)–(iv) and Q10(e) shipped broken solution lines or merged bullets. On the remaining cards, “Full Credit (−1)” deductions welded onto a credit band are moved to the row note. All existing IDs are kept; prompts are restored from the paper and topics corrected as metadata.',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [9], 'wording': 'pick one subject from each of these three groups / add one extra subject to one of these groups', 'classification': 'counting-context',
      'reason': 'The choices are the objects counted (3 × 4 × 5), and the extra subject is the answer to one required comparison; not a choice of prompts.'},
     {'pages': [12], 'wording': 'Hence, or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task; no printed pool of prompts.'},
     {'pages': [4, 6, 15, 17, 24], 'wording': 'Tick one box only', 'classification': 'answer-selection',
      'reason': 'Perpendicular or not, on/inside/outside, true/false, the value of r and the height ratio are answers with justification, not alternative prompts.'},
     {'pages': [29], 'wording': 'exactly one of these adults', 'classification': 'mathematical-context',
      'reason': 'Defines the event whose probability is required; there is a single prompt.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('counting-context', 'The groups are the subjects counted (one from each), or the extra subject is the answer to one required comparison; not a choice of prompts.') if 'Group' in t or 'groups' in t
        else ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.') if 'or otherwise' in t
        else ('mathematical-context', 'Defines the event “exactly one of three adults jogs” whose probability is required; there is a single prompt.') if 'exactly one' in t else None)
p.apply(ROWS, '2022 Ordinary Level Paper 2', expect_added=['maths-2022-ol-p2-q9-d'])
