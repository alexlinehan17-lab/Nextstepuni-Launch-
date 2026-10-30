"""2021 HL Paper 2: review ledger, restored prompts, re-quote garbled rows."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from review_lib import *
from rows_2021_hl_p2 import ROWS

p = Paper(2021, 'hl', 'p2', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '10C': [0, 3, 7, 10], '10D': [0, 3, 5, 8, 10], '15D': [0, 4, 8, 12, 15], '20D': [0, 5, 10, 15, 20]},
          'LC003ALP200EV.pdf', 'LC003ALP000EV.pdf')
A = p.A
pr = 'probability'; line = 'co-ordinate-geometry-of-the-line'; circ = 'co-ordinate-geometry-of-the-circle'
foot = 'In a particular population 15% of the people are left footed. A soccer team of 11 players, including 1 goalkeeper, is picked at random from the population.'
A('1-a', 'Q1(a)', '15D', [35], [4], '1-2', pr, 'Find the probability that there is exactly one left footed player on the team. Give you answer correct to three decimal places.', stem=foot)
A('1-b', 'Q1(b)', '10C', [35], [4], '1-2', pr, 'Find the probability that less than three players on the team are left footed. Give you answer correct to two decimal places.', stem=foot)
A('1-c', 'Q1(c)', '5C', [36], [5], '1-2', pr, 'The goalkeeper is left footed. Find the probability that at least eight of the remainder of the team are right footed. Give you answer correct to two decimal places.', stem=foot)
A('2-a', 'Q2(a)', '10C', [37], [6], '2-2', line, 'The line 3x − 6y + 2 = 0 contains the point (k, (2k + 2)/3), where k ∈ ℝ. Find the value of k.')
A('2-b', 'Q2(b)', '10D', [37], [6], '2-2', line, 'The point P(s, t) is on the line x − 2y − 8 = 0. The point P is also a distance of 1 unit from the line 4x + 3y + 6 = 0. Find a value of s and the corresponding value of t.')
abc = 'The points A(4, 2) and C(16, 11) are vertices of the triangle ABC shown below. D and E are points on [CA] and [CB] respectively. The ratio |AD| : |DC| is 2 : 1.'
A('2-i', 'Q2(c)(i)', '5C', [38], [7], '2-2', line, 'Find |AD|.', stem=abc)
A('2-c-ii', 'Q2(c)(ii)', '5C', [38], [7], '2-2', line, '[AB] and [DE] are horizontal line segments. |AB| = 33 units. Find the coordinates of B and of E.', stem=abc)
A('3-a', 'Q3(a)', '15D', [39], [8], '2-2', circ, 'The circle k has centre C(1, −2) and chord [AB] where |AB| = 4√3. The point D(3, 2) is the midpoint of the chord [AB], as shown below. Find the radius of k. Give your answer in the form a√b, where a, b ∈ ℕ.')
cs = 'The circles are c: x² + y² + 4x − 2y − 95 = 0 and s: (x − 7)² + (y − 13)² = 25.'
A('3-b-i', 'Q3(b)(i)', '10D', [39], [9], '2-2', circ, 'Show that the circles c: x² + y² + 4x − 2y − 95 = 0 and s: (x − 7)² + (y − 13)² = 25 touch externally.')
A('3-b-ii', 'Q3(b)(ii)', '5B', [40], [9], '2-2', circ + ',' + line, 'There are an infinite number of circles which touch circle c externally at the same point that s touches c. Find the coordinates of the centre of one of these circles, apart from circle s.', stem=cs)
idn = 'trigonometry-functions-identities'
A('4-a-i', 'Q4(a)(i)', '10C', [41], [10], '2-3', idn, 'Prove that cos 2A = cos² A − sin² A.')
A('4-a-ii', 'Q4(a)(ii)', '10D', [41], [10], '2-3', idn, 'sin(θ/2) = 1/√5, where 0 ≤ θ ≤ π. Use the formula cos 2A = cos² A − sin² A to find the value of cos θ.')
A('4-b', 'Q4(b)', '10D', [42], [11], '2-3', idn, 'Solve the equation: tan(B + 150°) = −√3, for 0° ≤ B ≤ 360°.')
cones = 'Two identical right-circular solid cones meet along their bases and fit exactly inside a sphere, as shown in the diagram.'
A('5-a-i', 'Q5(a)(i)', '15D', [43], [12], '3-4', 'area-volume', 'Prove that the volume of the remaining space inside the sphere is exactly half the total volume of the sphere.', stem=cones)
A('5-a-ii', 'Q5(a)(ii)', '5B', [43], [12], '3-4', 'area-volume', 'The combined volume of the two cones is (686/3)π cm³. Find the radius of one of the cones.', stem=cones)
A('5-b', 'Q5(b)', '10C', [44], [13], '3-3', 'algebra-solving-equations', 'At 9.00 a.m. a delivery van leaves a factory. It travels towards its destination at an average speed of 60 km/h. One hour and 45 minutes later a second van leaves the factory on the same route. It travels at an average speed of 95 km/h. Both vans arrive at their destination at the same time. Find at what time they arrive.')
gp = 'geometry-constructions-proofs'
A('6-a', 'Q6(a)', '20D', [45], [14], '2-1', gp, 'Prove that if two triangles ΔABC and ΔA′B′C′ are similar, then the lengths of their sides are proportional in order: |AB|/|A′B′| = |BC|/|B′C′| = |CA|/|C′A′|. (Diagram, Given, To Prove, Construction, Proof.)')
A('6-b', 'Q6(b)', '10D', [46], [15], '2-1', 'geometry', 'In the diagram below, the lines PA, HK, and BR are parallel. Prove that |AH| × |QB| = |AP| × |HB|. Give a reason for each geometrical statement you use.')
tri = 'The diagram (Triangle ABC) shows the 3 sections of a level triathlon course. In order to complete the triathlon, each contestant must swim 4 km from C to B, cycle from B to A, and then run 28 km from A to C. Mary can cycle at an average speed of 25 km/hour. It takes her 1 hour and 12 minutes to cycle from B to A.'
tri2 = tri + ' Part (a) shows that the total length of the course is 62 km.'
tt = 'trigonometry-triangles'
A('7-a', 'Q7(a)', '5C', [47], [16], '3-3', 'algebra-solving-equations', 'Show that the total length of the course is 62 km.', stem=tri)
A('7-b', 'Q7(b)', '15D', [47], [16], '3-3', 'algebra-solving-equations', 'On average, Mary can run 5·6 times as fast as she can swim. It takes her 4·8 hours to complete the course. Find her average swimming speed in km/h.', stem=tri2)
A('7-c', 'Q7(c)', '10D', [47], [17], '2-3', tt, 'Show that |∠ACB| = 116·5°, correct to 1 decimal place.', stem=tri2)
A('7-d', 'Q7(d)', '5C', [48], [17], '2-3', tt + ',area-volume', 'To comply with safety regulations, the region inside the triangular course must be kept clear of people. Find the area of this region. Give your answer, in km², correct to 1 decimal place.', stem=tri2 + ' |∠ACB| = 116·5°.')
A('7-e', 'Q7(e)', '10C', [48], [17], '2-3', tt, 'Find the shortest distance from the point C to the side AB. Give your answer in km, correct to 1 decimal place.', stem=tri2 + ' |∠ACB| = 116·5°.')
A('7-f', 'Q7(f)', '5C', [48], [18], '2-3', tt, 'The course is viewed from a camera tower which rises vertically from point A. The top of the tower is point T. The angle of elevation of T from B is 0·05°. Find |AT|, the vertical height of the tower. Give your answer correct to the nearest metre.', stem=tri2)
zs = 'statistics-z-scores'; inf = 'statistics-inferential-statistics'
exam = 'In a school all First Years sat a common maths exam. The results, in integer values, were normally distributed with a mean of 176 marks and a standard deviation of 36 marks. The top 10% of students will go forward to a county maths competition.'
A('8-a-i', 'Q8(a)(i)', '10D', [49], [19], '1-7', zs, 'Find the minimum mark needed on the exam to progress to the county stage.', stem=exam)
A('8-a-ii', 'Q8(a)(ii)', '10D', [49], [19], '1-7', zs, 'The school awarded a Certificate of Merit to any student who achieved between 165 marks and 210 marks. Find the percentage of First Years who received the Certificate of Merit.', stem=exam)
news = 'A news report claimed that 6th year students in Ireland studied an average of 21 hours per week, outside of class time. A Leaving Cert class surveyed 60 students in 6th year, chosen at random, from different schools. It found that the average study time was 19·8 hours and the standard deviation was 5·2 hours.'
A('8-b-i', 'Q8(b)(i)', '5C', [50], [20], '1-7', inf, 'Find the test statistic (the z-score) of this sample mean.', stem=news)
A('8-b-ii', 'Q8(b)(ii)', '10D', [50], [20], '1-7', inf, 'Find the p-value of this test statistic. Comment on what can be concluded from its value, in a two-tailed hypothesis test at the 5% level of significance, in relation to the news report claim.', stem=news)
keys = 'The school caretaker has a box with 23 room keys in it. 12 of the keys are for general classrooms, 6 for science labs and 5 for offices.'
A('8-c-i', 'Q8(c)(i)', '10D', [51], [21], '1-2', pr, 'Four keys are drawn at random from the box. What is the probability that the 4th key drawn is the first office key drawn? Give your answer correct to 4 decimal places.', stem=keys)
A('8-c-ii', 'Q8(c)(ii)', '5C', [51], [21], '1-2', pr, 'All the keys are returned to the box. Then 3 keys are drawn at random from the box one after the other, without replacement. What is the probability that one of them is for a general classroom, one is for a science lab and one is for an office? Give your answer correct to 4 decimal places.', stem=keys)
plane = 'An aeroplane flies east from point A for 2 hours at a constant speed of 420 km per hour until it reaches point B. It then changes direction by heading 20° towards the south at the same speed until it reaches point C, as shown in the diagram below. The direct distance from A to C is 1450 km and |∠BAC| = 8·57°.'
A('9-a-i', 'Q9(a)(i)', '10D', [52], [22], '2-3', tt, 'Find how long it took to fly from B to C. Give your answer correct to the nearest minute.', stem=plane)
A('9-a-ii', 'Q9(a)(ii)', '10D', [52], [22], '3-3', tt, 'The average fuel consumption of the plane is 3·8 litres per second and the fuel capacity of the plane is 100 000 litres. Show that the plane will be able to complete the journey from A to B to C and directly back to A at a speed of 420 km/h without refuelling.', stem=plane)
volt = 'The voltage, V(t), (in Volts) of a certain alternating current is given by the function: V(t) = 110√2 sin(120πt), where t is in seconds.'
A('9-b-i', 'Q9(b)(i)', '5C', [53], [23], '2-3', idn, 'Find the period and range of the function V(t).', stem=volt)
A('9-b-ii', 'Q9(b)(ii)', '10C', [53], [23], '2-3', idn, 'Sketch the function for 0 ≤ t ≤ p, where p is the period of V(t). Indicate the period and range of the function on your graph.', stem=volt)
A('9-b-iii', 'Q9(b)(iii)', '5C', [53], [23], '2-3', idn, 'Use V(t) to find the voltage when t = 6·67 seconds. Give your answer correct to two decimal places.', stem=volt)
A('9-b-iv', 'Q9(b)(iv)', '5C', [54], [24], '2-3', idn, 'Find one value for t where the voltage is 110 Volts. Give your answer in the form a/b where a, b ∈ ℕ.', stem=volt)
A('9-b-v', 'Q9(b)(v)', '5C', [54], [24], '5-2', 'differentiation-rules', 'Find the rate of change of the voltage when t = 2 seconds. Give your answer correct to the nearest unit.', stem=volt)
blood = 'People with O-negative blood type are called "universal donors" because their blood can be given to anyone else. In Ireland approximately 8% of the population have O-negative blood type (source: Blood Transfusion Service).'
A('10-a-i', 'Q10(a)(i)', '10D', [55], [25], '1-2', pr, 'At a blood donation clinic, ten donors give blood, one after the other. Find the probability that the tenth person is the third O-negative donor. Give your answer correct to four decimal places.', stem=blood)
A('10-a-ii', 'Q10(a)(ii)', '10C', [55], [25], '1-2', pr, 'At a blood donation clinic, five donors give blood. What is the probability that at least one of the five donates O-negative blood? Give your answer correct to four decimal places.', stem=blood)
A('10-a-iii', 'Q10(a)(iii)', '10D', [55], [26], '3-2', pr + ',indices-and-logs', 'Find the minimum number of blood donors required, so that the probability that at least one of them is type O-negative is greater than 0·97.', stem=blood)
A('10-b', 'Q10(b)', '10C', [56], [26], '1-3', pr, 'A homeowner has a problem with the heating system in her house. A plumber has identified the problem as a faulty part. The homeowner knows that in 80% of cases a repair of the part will fix the problem and this repair will cost €70. If the repair does not work then a new part will have to be bought costing €150 and there will be an additional labour cost of €80 to replace the old part with the new. Find the expected value of the cost of fixing this faulty system.')
A('10-c', 'Q10(c)', '10D', [56], [27], '1-3', pr, 'A life insurance policy pays out €120 000 if the policy holder dies and €40 000 if the policy holder becomes disabled. The insurance company has calculated that in general, in any given year, the probability of death is 0·0001 and the probability of disability is 0·002. The company has 18 000 policy holders on its books at present who are all charged the same premium. The company’s goal is to make €900 000 profit in a particular year. Find the annual premium it should charge its customers which in an average year would generate this level of profit.')

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 42)
p.review(marks,
    'Independent visual reading of all 32 question-paper pages and PDF pages 32–60 of the combined Higher Level scheme (the Paper 2 scale table on page 32, the summary of allocations on page 33, annotation palette, every Paper 2 model solution and marking note, the Irish-language bonus-mark table on page 57 and the blank closing pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(32, 61)), [32, 33],
    ['The 2021 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '42 independently marked units, matching the printed summary of allocations on scheme page 33. Every part has its own scale; none are shared.',
     'Paper 2 bands from scheme page 32: 5B 0,2,5; 5C 0,2,3,5; 10C 0,3,7,10; 10D 0,3,5,8,10; 15D 0,4,8,12,15; 20D 0,5,10,15,20.',
     'All 42 units were already authored and shipping. The Q2(c)(i) card (ID maths-2021-hl-p2-q2-i, kept) had a prompt that merged Q2(a), Q2(b) and Q2(c); it now carries Q2(c)(i) alone with its stem. Seven cards had marking points whose stacked fractions, binomial coefficients and exponents the scheme text layer had scrambled (Q1(b), Q1(c), Q4(a)(ii), Q8(a)(i), Q8(c)(i), Q10(a)(i), Q10(a)(ii)); they are re-quoted from the printed scheme where the text layer keeps a readable form. Formula-only bullets with no readable text form (for example the Q10(a)(i) mid and high partial expressions) are left to the attached scheme page rather than retyped. All existing IDs are kept; prompts are restored from the paper (including its printed “Give you answer” in Q1) and topics corrected as metadata.',
     'The question booklet is LC003ALP200EV.pdf; its indexed scheme LC003ALP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [9], 'wording': 'Find the coordinates of the centre of one of these circles', 'classification': 'open-answer',
      'reason': 'Any valid centre on the line of centres answers the single required task; the scheme accepts any such point.'},
     {'pages': [12], 'wording': 'Find the radius of one of the cones', 'classification': 'given-context',
      'reason': 'The two cones are identical, so one radius is required; there is no choice of prompts.'},
     {'pages': [21, 25, 26], 'wording': 'one of them / at least one of', 'classification': 'mathematical-context',
      'reason': 'Defines the event whose probability is required; there is a single prompt.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('open-answer', 'Any valid centre on the line through the two centres answers the single required task; the scheme accepts any such point.') if 'one of these circles' in t
        else ('given-context', 'The two cones are identical, so the radius of one cone is the single value required; there is no choice of prompts.') if 'one of the cones' in t
        else ('mathematical-context', 'Defines the event (one key of each type, or at least one O-negative donor) whose probability is required; there is a single prompt.') if ('one of them' in t or 'at least one' in t) else None)
p.apply(ROWS, '2021 Higher Level Paper 2', ref_overrides={'maths-2021-hl-p2-q2-i': '2021 HL Paper 2 Q2(c)(i)'})
