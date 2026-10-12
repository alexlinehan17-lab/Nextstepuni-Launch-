"""2021 OL Paper 2: review ledger, restored prompts, add Q1(b)(i), ship held-back Q5(b)(ii), re-cite Q6, re-quote rows."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys, json
from pathlib import Path
from review_lib import *
from rows_2021_ol_p2 import ROWS

p = Paper(2021, 'ol', 'p2', {'5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10], '10C': [0, 3, 7, 10],
          '10D': [0, 3, 5, 8, 10], '15C': [0, 5, 10, 15], '15D': [0, 4, 7, 11, 15]}, 'LC003GLP200EV.pdf', 'LC003GLP000EV.pdf')
A = p.A
pr = 'probability'; line = 'co-ordinate-geometry-of-the-line'; circ = 'co-ordinate-geometry-the-circle'; st = 'statistics'; tr = 'trigonometry'; av = 'area-volume'
tw = 'The game “Twister” is played using two spinners and a mat with coloured spots. The two spinners needed for the game are shown below. Both consist of four equal sections: one spinner shows Left Hand, Right Hand, Left Foot and Right Foot; the other shows Yellow, Red, Blue and Green. A player spins both spinners and must then place their selected hand/foot on the selected coloured spot on the game mat. The spinners below show the outcome Right Hand on a Yellow Spot.'
A('1-a', 'Q1(a)', '10C', [32], [4], '1-1', 'counting,' + pr, 'How many different possible outcomes are there in the game?', stem=tw)
A('1-b-i', 'Q1(b)(i)', '5C', [33], [5], '1-2', pr, 'Kate spins each spinner once. What is the probability that she must use her left foot?', stem=tw)
A('1-b-ii', 'Q1(b)(ii)', '5C', [33], [5], '1-2', pr, 'Kate spins each spinner once. What is the probability that she must use a red or yellow coloured spot?', stem=tw)
A('1-c-i', 'Q1(c)(i)', '5C', [34], [5], '1-2', pr, 'Jack spins each spinner once. What is the probability that the outcome is his right hand and a blue spot?', stem=tw)
A('1-c-ii', 'Q1(c)(ii)', '5C', [34], [5], '1-2', pr, 'Jack spins each spinner once. What is the probability that the outcome is his right hand or a blue spot?', stem=tw)
coco = 'At a stall in a fun fair, the probability of knocking a coconut off its support is 0·34.'
A('2-a-i', 'Q2(a)(i)', '10C', [35], [6], '1-2', pr, 'What is the probability of not knocking a coconut off its support?', stem=coco)
A('2-a-ii', 'Q2(a)(ii)', '10C', [35], [6], '1-2', pr, 'David is given three attempts to knock the coconut off its support. What is the probability that he knocks the coconut for the first time, on his third attempt? Give your answer correct to three decimal places.', stem=coco)
A('2-b', 'Q2(b)', '10D', [35], [7], '3-4', av + ',geometry', 'The figure ABCDE shown in the diagram consists of a large square ACDE standing on the diagonal [AC] of a smaller square ABCF. The smaller square has a side length of 2 cm. Find the area and perimeter of the figure ABCDE. Give your answer for the perimeter correct to two decimal places.')
A('3-a', 'Q3(a)', '10D', [36], [8], '2-2', line, 'A line n passes through the points A(−1, 2) and B(0, −2). Write the equation of n in the form y = mx + c, where m, c ∈ ℤ.')
lp = 'The diagram below shows the line l: 3x − 4y = 5 and the point P(6, −3).'
A('3-b-i', 'Q3(b)(i)', '10D', [37], [8], '2-2', line, 'Find the equation of the line k through the point P that is perpendicular to the line l. Write your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.', stem=lp)
A('3-b-ii', 'Q3(b)(ii)', '10C', [37], [9], '2-2', line + ',algebra-equations', 'Find the point of intersection of the lines l: 3x − 4y = 5 and h: 2x − y = 10.', stem=lp)
ab = 'The co-ordinate diagram below shows two points A and B.'
A('4-a-i', 'Q4(a)(i)', '5C', [38], [10], '2-2', line, 'Write down the co-ordinates of A and of B.', stem=ab)
A('4-a-ii', 'Q4(a)(ii)', '5C', [38], [10], '2-2', line, 'Find the co-ordinates of the midpoint of [AB].', stem=ab)
A('4-a-iii', 'Q4(a)(iii)', '5C', [39], [10], '2-2', circ, 'Use a compass to construct the circle c, which has AB as its diameter on the diagram above.', stem=ab)
A('4-a-iv', 'Q4(a)(iv)', '10D', [39], [11], '2-2', circ, 'Find the length of the radius of the circle c, and hence write down the equation of c.', stem=ab + ' The circle c has [AB] as its diameter.')
A('4-b', 'Q4(b)', '5D', [40], [11], '2-2', circ, 'The point P(2, k) is in the first quadrant and is on c. Use algebra to find the value of k and plot the point P on the diagram on the previous page.', stem=ab + ' The circle c has [AB] as its diameter.')
A('5-a', 'Q5(a)', '10C', [41], [12], '1-3', st, 'The heights of a given population are normally distributed. 95% of the population fall within the height range [147·9 cm ↔ 178·7 cm]. Using the empirical rule, find the mean and the standard deviation of the distribution of heights in the population.')
arm = 'The following table shows data on the height and arm span of twenty teenagers. Females 1–12, height (cm) and arm span (cm): 162, 155; 169, 174; 164, 144; 157, 160; 160, 160; 170, 170; 174, 170; 159, 154; 153, 148; 167, 167; 150, 152; 139, 129. Males 13–20 (the shaded section): 168, 169; 147, 150; 134, 121; 177, 176; 172, 170; 160, 163; 152, 151; 153, 151.'
A('5-b-i', 'Q5(b)(i)', '10D', [41], [13], '1-6', st, 'Complete the scatter plot below by adding in the data for the males (the data in the shaded section of the table).', stem=arm)
A('5-b-ii', 'Q5(b)(ii)', '5B', [41], [13], '1-6', st, 'The table on the right shows three numbers: 0·2, 0·9 and −0·6. One of the numbers is the correlation coefficient of the data shown in the table above. Tick (✓) the one which you think best represents the correlation coefficient between height and arm span for this data set.', stem=arm)
A('5-b-iii', 'Q5(b)(iii)', '5B', [41], [13], '1-6', st, 'Explain what this correlation coefficient tells us about the relationship between height and arm span for this data set.', stem=arm)
A('6-a-i', 'Q6(a)(i)', '5C', [42], [14], '2-1', 'geometry-proofs-and-constructions', 'On the diagram below showing the triangle ABC, construct the perpendicular bisector of the side [AC]. Show all your construction lines and arcs clearly.', extra={'measurementRequired': True})
A('6-a-ii', 'Q6(a)(ii)', '10D', [42], [14], '2-1', 'geometry-proofs-and-constructions', 'Construct the circumcircle of the given triangle ABC. Show all your construction lines and arcs clearly.', stem='The diagram shows the triangle ABC.', extra={'measurementRequired': True})
enl = 'The triangle PQR is the image of the triangle DEF under an enlargement. (The diagram is not drawn to scale.) The scale factor of the enlargement, k, is 2·5. |EF| = 3 cm.'
A('6-b-i', 'Q6(b)(i)', '5B', [43], [15], '2-4', 'geometry', 'Use the scale factor to find |QR|.', stem=enl)
A('6', 'Q6(b)(ii)', '10C', [43], [15], '2-4', 'geometry,' + av, 'The area of the triangle PQR is 18·75 cm². Find the area of triangle DEF.', stem=enl)
age = 'The following table shows the age profiles of all of the people in Ireland, aged between 15 and 65, who subscribed to an online streaming platform. Age group 15 − 25: 24%; 25 − 35: 27%; 35 − 45: 25%; 45 − 55: 16%; 55 − 65: 8% of subscribers. Note: 25 − 35 means 25 years and over but less than 35 years.'
A('7-a-i', 'Q7(a)(i)', '15C', [44], [16], '1-6', st, 'Draw a Histogram to represent the data.', stem=age)
A('7-a-ii', 'Q7(a)(ii)', '5C', [44], [16], '1-6', st, 'In a survey of 1000 subscribers, aged between 15 and 65, how many people would you expect to be between 25 years and 55 years?', stem=age)
A('7-a-iii', 'Q7(a)(iii)', '5B', [44], [17], '1-6', st, 'Use the table or the histogram to write down the age group which contains the median age.', stem=age)
A('7-a-iv', 'Q7(a)(iv)', '10C', [45], [17], '1-6', st, 'Use the mid-interval values of the groups in the table to estimate the mean age of the subscribers. Give your answer correct to one decimal place.', stem=age)
net = 'Prior to the COVID-19 pandemic, Netflix held the largest share of the online streaming market with 65% of all streaming subscribers in the 15 to 65 age group. Aiden thought that this percentage might have changed during the pandemic and surveyed a sample of subscribers in this age group to get data. He then carried out a Hypothesis Test to test his theory.'
A('7-b-i', 'Q7(b)(i)', '5C', [46], [18], '1-7', st, 'If 540 people responded to his survey, calculate the margin of error of his survey. Give your answer as a percentage, correct to one decimal place.', stem=net)
A('7-b-ii', 'Q7(b)(ii)', '5C', [46], [18], '1-7', st, 'His survey revealed that 372 of the responders said they now have a Netflix account. Use your answer to Part (b)(i) above to create a 95% confidence interval for the percentage of the population that have a Netflix account.', stem=net + ' 540 people responded to his survey.')
A('7-b-iii', 'Q7(b)(iii)', '5C', [47], [18], '1-7', st, 'Use your answer to Part (b)(ii) above to conduct the Hypothesis Test, at the 5% level of significance to test Aiden’s claim that the percentage of subscribers to Netflix had changed. State clearly your null hypothesis, your alternative hypothesis and give your conclusion in the context of the question.', stem=net + ' 540 people responded to his survey and 372 said they now have a Netflix account.')
lake = 'The diagram on the right shows the plan of a lake. The line segment [PQ] represents the distance from the pier, P, to the far side of the lake. At equal intervals of 10 m along this line, perpendicular measures are made to the sides of the lake as shown.'
A('8-a-i', 'Q8(a)(i)', '15D', [48], [19], '3-4', av, 'Use the Trapezoidal Rule to estimate the surface area of the lake.', stem=lake)
A('8-a-ii', 'Q8(a)(ii)', '5B', [48], [19], '3-4', av, 'If the lake is on average 8 m deep, estimate the volume of water in the lake.', stem=lake)
A('8-b-i', 'Q8(b)(i)', '5B', [49], [20], '3-4', av, 'Calculate the volume, in cm³, of a hemisphere of radius 21 cm. Give your answer terms of π.')
A('8-b-ii', 'Q8(b)(ii)', '10D', [50], [20], '3-4', av, 'A buoy on the lake is in the shape of a hemisphere of radius 21 cm surmounted by a cone. The volume of the cone is equal to the volume of the hemisphere. Find h, the total height of the buoy.')
A('8-c', 'Q8(c)', '15D', [50], [21], '2-3', tr, 'The buoy is situated at B, 43 m from the pier P and 26 m from the point Q, as shown in the diagram above (|PQ| = 60 m). Find |∠QBP|, the angle at the buoy shown on the diagram. Give your answer correct to two decimal places.', stem=lake)
run = 'The line segment [SE], shown below, represents an airport runway. The point S and the point E represent the start and end points of the runway respectively. The diagram is drawn to a scale of 1 unit = 250 metres.'
A('9-a-i', 'Q9(a)(i)', '10C', [51], [22], '3-3', 'number-systems', 'Find the length of the runway. Give your answer in km.', stem=run)
A('9-a-ii', 'Q9(a)(ii)', '5B', [51], [22], '2-3', tr, 'An aircraft starts at the point S and travels 1 250 m to a point L where it lifts off. From the point L, the aircraft makes an angle of 14° with the ground, [LE]. The aeroplane travels along this path until it is directly above E. Plot and label the lift-off point L, and draw the aircraft’s flight path for this part of its journey, on the diagram above.', stem=run)
A('9-a-iii', 'Q9(a)(iii)', '10D', [52], [22], '2-3', tr, 'Find the total distance the aeroplane has travelled when it is directly above E. Give your answer, in metres, correct to the nearest metre.', stem=run + ' An aircraft starts at the point S and travels 1 250 m to a point L where it lifts off. From the point L, the aircraft makes an angle of 14° with the ground, [LE], and travels along this path until it is directly above E.')
fly = 'The aircraft flies from airport A to airport B, and then on to airport C, at the same altitude. The pilot records the flight summary on the given diagram: |AB| = 260 km, the angle at A is 47° and the angle at B is 97°.'
A('9-b-i', 'Q9(b)(i)', '15D', [53], [23], '2-3', tr, 'Find the distance from airport B to airport C. Give your answer correct to the nearest km.', stem=fly)
A('9-b-ii', 'Q9(b)(ii)', '10D', [53], [23], '3-4', av, 'When the plane was directly over airport C, the pilot was instructed to “circle” until a runway was available. She therefore flew 10 km away from C before turning and flying along a circular arc of 70° and then returning to the airport. This path was all flown at the same altitude. Find the total distance travelled. Give your answer, in km, correct to two decimal places.')
map_ = 'A TY maths class has created a game involving a co-ordinate treasure map, as shown below. The game consists of tasks that involve directions, distances, and locations. The tasks in the game are based on the map, which shows the points B(6, 4), C(−3, 2) and A(3, −5) and a line l.'
A('10-a-i', 'Q10(a)(i)', '10B', [54], [24], '2-2', line, 'Treasure is hidden at location T(−2, −5). Mark T on the map where this treasure can be found.', stem=map_)
A('10-a-ii', 'Q10(a)(ii)', '5C', [54], [24], '2-2', line, 'Food is located at a point F on the map. The point F is on a line which contains the point A(3, −5) and has a slope of −1. The point F is also on a line which contains B(6, 4) and has a slope of 0. By drawing appropriate lines on the map above, or otherwise, find the co-ordinates of F.', stem=map_)
A('10-b-i', 'Q10(b)(i)', '10C', [55], [25], '2-2', line, 'A clue to another treasure is hidden in a locked box at point B(6, 4). The 4-digit code to open the box is d⁴, where d is the distance from B to C(−3, 2), and d ∈ ℕ. Find the 4-digit code (d⁴).', stem=map_)
A('10-b-ii', 'Q10(b)(ii)', '5D', [55], [25], '2-2', line, 'A meeting point P(2, m) is below the x-axis. P is a distance of √41 from point B(6, 4). Find the value of m and plot P on the map above.', stem=map_)
A('10-c-i', 'Q10(c)(i)', '5C', [56], [26], '2-2', line, 'The line k has equation x − y − 3 = 0. Verify, using substitution, that the point T(−2, −5) is on k.', stem=map_)
A('10-c-ii', 'Q10(c)(ii)', '5C', [56], [26], '2-2', line, 'Another treasure also needs be somewhere on the line k. You must pick a spot along k to contain this treasure. Use algebra to find another point on k, other than T.', stem=map_ + ' The line k has equation x − y − 3 = 0 and T(−2, −5) is on k.')
A('10-c-iii', 'Q10(c)(iii)', '10C', [57], [26], '2-2', line, 'A spade for digging is hidden on line l which is parallel to k. The line l contains the point C(−3, 2). Find the equation of line l.', stem=map_ + ' The line k has equation x − y − 3 = 0.')

marks = {**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}}
p.check(marks, 48)
p.review(marks,
    'Independent visual reading of all 28 question-paper pages and PDF pages 29–60 of the combined Ordinary Level scheme (the Paper 2 title page, the scale table on page 30, the summary of allocations on page 31, every Paper 2 model solution and marking note, and the closing pages). Each task boundary is the published scale beside its model solution, cross-checked against the printed summary.',
    list(range(29, 61)), [30, 31],
    ['The 2021 paper was adjusted for COVID-19 (220 marks): candidates answer any four of Q1–6 (30 marks each) and any two of Q7–10 (50 marks each), so 380 marks are offered and 220 count. Every question is retained.',
     '48 independently marked units. The printed summary on scheme page 31 lists Q9(b)(ii) as 15D, which would make Question 9 total 55; the scale printed beside the model solution (page 53) is 10D, giving the printed 50 marks, and is authoritative.',
     'Paper 2 bands from scheme page 30: 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,3,7,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,4,7,11,15.',
     'Before this review the deck held 47 of the 48 units and shipped 46. Q1(b)(i) (left foot, 5C) had no card and is added. Q5(b)(ii) was refused by the build over one unreadable glyph, U+F061, in “Tick ( )”: in this paper it is Webdings glyph id 68, which renders as a tick, but the same code point is SymbolMT’s alpha in 2011 Higher Paper 2 (cropped and read: “α + β = 90°”). A map keyed by character cannot hold both, so U+F061 stays out of glyphmap.json and the gate still refuses it everywhere; this card ships because its prompt is restored from the paper. The card maths-2021-ol-p2-q6 (ID kept) carried Q6(b)(ii)’s scale and marking notes under a prompt merged from Q6(a); it is re-cited as Q6(b)(ii) with its own prompt, and maths-2021-ol-p2-q6-a-i and maths-2021-ol-p2-q6-b-i are re-cited to the single parts their scales cover. Twelve cards had marking points garbled by the text layer (merged method ladders, notes inside bands, calculator-mode values, stacked fractions) and are re-quoted from the printed scheme, labelled by band and method.',
     'Outside the census: maths-2021-ol-p2-q3 duplicates Q3(a). The scheme prints two method ladders for that one 10D unit, and the deck had carded the second as its own card under a prompt merged from Q3(a) and Q3(b)(i). Both ladders are now quoted on maths-2021-ol-p2-q3-a. The duplicate’s prompt is restored to the printed Q3(a) wording, but withdrawing it needs a progress alias and a change to the frozen ordinary preservation count, which is left for a separate decision.',
     'Q6(a)(i) and Q6(a)(ii) are constructions on the printed triangle with a ±0·2 cm tolerance, so the page measuring tool is attached.',
     'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions, which match the printed scheme page numbers.'],
    [{'pages': [3, 4, 16], 'wording': 'any four / any two questions', 'classification': 'exam-level-selection',
      'reason': 'Candidates select independently marked questions; every question is retained.'},
     {'pages': [13], 'wording': 'Tick (✓) the one which you think best represents', 'classification': 'answer-selection',
      'reason': '0·2, 0·9 or −0·6 is the answer to Q5(b)(ii), not a choice of prompts.'},
     {'pages': [24], 'wording': 'or otherwise', 'classification': 'method-choice',
      'reason': 'Alternative methods for the same marked task; no printed pool of prompts.'}],
    lambda t: ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.') if 'questions' in t and 'any' in t.lower()
        else ('answer-selection', 'Ticking 0·2, 0·9 or −0·6 is the answer to the single required task, not a choice of prompts.') if 'Tick' in t
        else ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.') if 'or otherwise' in t.lower() else None)
p.apply(ROWS, '2021 Ordinary Level Paper 2', expect_added=['maths-2021-ol-p2-q1-b-i'],
        ref_overrides={'maths-2021-ol-p2-q6': '2021 OL Paper 2 Q6(b)(ii)', 'maths-2021-ol-p2-q6-a-i': '2021 OL Paper 2 Q6(a)(i)',
                       'maths-2021-ol-p2-q6-b-i': '2021 OL Paper 2 Q6(b)(i)'})
# The withdrawn duplicate keeps its ID, questionRef and scheme ladder in the authored deck; its prompt is restored from the paper.
ap = Path('scripts/markbank/authored/maths.json'); authored = json.loads(ap.read_text())
dup = next(c for c in authored if c['id'] == 'maths-2021-ol-p2-q3')
dup['questionText'] = 'A line n passes through the points A(−1, 2) and B(0, −2). Write the equation of n in the form y = mx + c, where m, c ∈ ℤ.'
dup.pop('stem', None)
# 999d76469 withdrew the duplicate through card-corrections.json and a CARD_ID_ALIASES progress alias.
dup['notes'] = "Withdrawn as a duplicate of maths-2021-ol-p2-q3-a (Q3(a), the scheme's second method ladder) through card-corrections.json and a CARD_ID_ALIASES progress alias, 2026-10-12."
ap.write_text(json.dumps(authored, ensure_ascii=False, indent=1) + '\n')
