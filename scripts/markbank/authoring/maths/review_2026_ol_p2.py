import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sys
from solution_lib import Paper

OL_P2 = {'5A': [0, 5], '5B': [0, 2, 5], '5C': [0, 2, 3, 5], '5D': [0, 2, 3, 4, 5], '10B': [0, 5, 10],
         '10C': [0, 4, 7, 10], '10D': [0, 3, 5, 8, 10], '15C': [0, 5, 10, 15], '15D': [0, 4, 8, 12, 15]}
p = Paper(
    year=2026, level='ordinary', paper_key='p2', paper_file='LC003GLP200EV.pdf', scheme_file='LC003GLP000EV.pdf',
    prefix='maths-2026-ol-p2', ref='2026 OL Paper 2', scales=OL_P2, reviewed_at='2026-10-11',
    general_notes=[3, 4, 23], scheme_pages=[3, 4, 5, 6] + list(range(23, 41)),
    printed_marks={**{str(q): 30 for q in range(1, 7)}, **{str(q): 50 for q in range(7, 11)}},
    review_method='Independent visual reading of all 32 question-paper pages and PDF pages 3–6 and 23–40 of the combined Ordinary Level scheme (general notes, the Paper 2 scale table on page 23, every Paper 2 model solution and marking note, and the blank closing pages). Each task boundary is the published scale, not a parser count.',
    source_notes=[
        'Candidates answer any five of Q1–6 (30 marks each) and any three of Q7–10 (50 marks each): 380 offered marks, 300 candidate marks. Every question is retained; no combined multi-question cards.',
        '45 independently marked units. Shared scales keep their parts together: Q2(a)(ii)–(iii) 5D, Q3(a)(i)–(ii) 15D, Q3(b)(ii)–(iii) 10D, Q5(a)(ii)–(iii) 10D, Q6(a)(ii)–(iii) 10D and Q7(c)(i)–(ii) 10D.',
        'Paper 2 bands from scheme page 23: 5A 0,5; 5B 0,2,5; 5C 0,2,3,5; 5D 0,2,3,4,5; 10B 0,5,10; 10C 0,4,7,10; 10D 0,3,5,8,10; 15C 0,5,10,15; 15D 0,4,8,12,15. The table prints the 5D ladder as “0, 2, 3. 4. 5”; it is 0, 2, 3, 4, 5. Paper 2 15D differs from Paper 1, which has no 15D.',
        'The question booklet is LC003GLP200EV.pdf; its indexed scheme LC003GLP000EV.pdf is shared with Paper 1. All page references are PDF positions. The paper omits “(30 marks)” beside Question 5; the scheme’s scales total 30.',
        'Q6(a)(i) asks the candidate to measure printed lengths (scheme: |AB| = 4 cm, |EF| = 10 cm), so it carries the calibrated measuring ruler.',
        'Diagrams and tables (line l, the group and pairings tables, activity categories, isosceles triangle, spinner, rectangles ABCD and EFGH, concentric circles, co-ordinate grids, the camps, the island, the boat route, the sector, the songs table, the cone, the can table and the shelf) are read from the attached original question pages; prompts quote the paper’s own wording.',
        'Some scheme text layers lose letters in point names (for example |OP| and |SQ| print as repeated glyphs), so card rows quote only notes whose text layer matches the printed scheme; the scheme reader shows the full published notes.',
    ],
    out_name='2026-ordinary-p2.json', atlas_prefix='mathematics-ordinary-', section_of=lambda q: 'A' if q <= 6 else 'B',
)
A = p.add
line = 'The diagram below shows the line l: 2x + 3y − 18 = 0.'
A('1-a-i', 'Q1(a)(i)', '10C', [24], [4], '2-2', 'co-ordinate-geometry-of-the-line',
  'l cuts the y-axis at the point P. Show that the point P is (0, 6).',
  ['2(0) + 3(6) − 18 = 0', 'Point fully substituted into equation'], stem=line)
A('1-a-ii', 'Q1(a)(ii)', '5C', [24], [4], '2-2', 'co-ordinate-geometry-of-the-line,area-volume',
  'The line l cuts the x-axis at the point (9, 0). Find the area of the triangle, in units², made between the x-axis, the y-axis, and the line l.',
  ['Formula fully substituted', 'Work of merit, for example, relevant formula or relevant work on the diagram'],
  stem=line + ' l cuts the y-axis at the point P (0, 6).')
A('1-b-i', 'Q1(b)(i)', '5B', [24], [5], '2-2', 'co-ordinate-geometry-of-the-line',
  'Find the slope of the line l: 2x + 3y − 18 = 0', ['Accept correct answer without work'], stem=line)
A('1-b-ii', 'Q1(b)(ii)', '10D', [24], [5], '2-2', 'co-ordinate-geometry-of-the-line',
  'The line k passes through the points A(4, −2) and B(r, 7) and is perpendicular to the line l, where r ∈ ℤ. Work out the value of r.',
  ['r = 10', 'Perpendicular slope found from (b)(i)', 'Slope formula fully substituted in terms of r', 'r found using a translation'], stem=line)
chess = 'Eight schools (A, B, C, D, W, X, Y, and Z) are competing in a chess tournament. The schools are divided into two groups, as shown in the table below: Group 1 is A, B, C and D; Group 2 is W, X, Y and Z. At the beginning of the tournament, each school has an equal chance of winning its group. The winner of group 1 will play the winner of group 2 in the final.'
A('2-a-i', 'Q2(a)(i)', '10C', [25], [6], '1-1', 'probability,counting',
  'Complete the table below to show all possible pairings for the final. Some have already been completed for you. For example, AW means that school A and school W play in the final. The table already shows AW, AX, BZ, DX and DZ.',
  ['1 correct entry', '7 correct entries'], stem=chess)
A('2-a-ii-iii', 'Q2(a)(ii),Q2(a)(iii)', '5D', [25], [6], '1-2', 'probability',
  '(ii) Write down the probability that School B plays in the final. (iii) School D withdraws before the tournament begins. The groups remain the same but without school D. Each remaining school in Group 1 still has an equal chance of winning that group. Work out the probability that school B or school Z, but not both, now play in the final.',
  ['Work of merit, for example, correct numerator or denominator in either part or relevant work on the table',
   'One part correct and work of merit in the other part'], stem=chess)
erika = 'Erika and Peter play against each other in a different chess tournament. The probability that Erika wins a game is 0·6 and this remains the same each time they play. There are no draws.'
A('2-b-i', 'Q2(b)(i)', '5B', [25], [7], '1-2', 'probability',
  'Write down the probability that Peter wins a game.', ['1 − 0·6 = 0·4', 'Use of 1'], stem=erika)
A('2-b-ii', 'Q2(b)(ii)', '10D', [25], [7], '1-3', 'probability',
  'The first player who wins two games wins the match. For example, Erika could win the match by winning the first game, losing the second game, and winning the third game. Work out the probability that Erika wins the match.',
  ['EE or EPE or PEE', '0·36 + 0·144 + 0·144', 'Probability of two outcomes correctly formulated'], stem=erika)
A('3-a-i-ii', 'Q3(a)(i),Q3(a)(ii)', '15D', [26], [8], '1-1', 'counting',
  '(i) Find how many different choices are possible if Tara chooses one activity from each of the three categories. (ii) The organisers need to remove one activity from one of the categories. From which category should they remove an activity if they want to keep the greatest number of possible choices? Use calculations to support your answer. Tick one box only: Category 1, Category 2 or Category 3.',
  ['5 × 6 × 4 = 120', 'Category 2 box ticked', 'Category 2: 5 × 5 × 4 = 100'],
  stem='Tara is going on a school trip. She must choose one activity from each of three categories shown below. Category 1: Zipline, Kayaking, Archery, Rock Climbing, Paddle-Boarding. Category 2: Pottery, Painting, Drama, Animation, Singing, Crochet. Category 3: Pizza-Making, Baking, Smoothie-Bar, BBQ.')
exams = 'Tara is sitting her fifth-year summer exams. She will have exams in 7 subjects which can be arranged in any order on the timetable.'
A('3-b-i', 'Q3(b)(i)', '5B', [26], [9], '1-1', 'counting',
  'In how many ways could the order of the 7 exams be arranged?',
  ['7! = 5040', 'Work of merit, for example, relevant multiplication to 7 or relevant setup'], stem=exams)
A('3-b-ii-iii', 'Q3(b)(ii),Q3(b)(iii)', '10D', [26], [9], '1-1', 'counting',
  '(ii) How many arrangements of 3 different exams can be made from the 7 exams? (iii) It is decided that Maths will be the first subject examined on Monday. How many arrangements can now be made for the remaining exams on Monday?',
  ['7 × 6 × 5 = 210', '6 × 5 = 30', 'One part correct and work of merit in the other part'],
  stem=exams + ' Tara will have 3 exams on Monday.')
iso = 'The diagram below shows an isosceles triangle with the base extended. Some measurements are given: the two equal sides are 12 cm and the angle between them is 44°.'
A('4-a-i', 'Q4(a)(i)', '10C', [27], [10], '2-1', 'geometry',
  'Find the size of the angle marked A and the size of the angle marked B.',
  ['180 − 44 = 136', 'B = 44 + 68 = 112[°]', 'One angle correct'], stem=iso)
A('4-a-ii', 'Q4(a)(ii)', '5C', [27], [10], '2-3', 'trigonometry,area-volume',
  'Find the area of the triangle. Give your answer correct to the nearest whole number.',
  ['Formula fully substituted', 'Apply a * for no units'], stem=iso)
A('4-b', 'Q4(b)', '15D', [27], [11], '2-3', 'trigonometry',
  'A triangle PQR has the measurements: |PR| = 12 cm, |PQ| = 9 cm, |QR| = 10 cm. Use the cosine rule to work out the size of the angle ∠QPR. Give your answer correct to the nearest degree. Hint: It may be useful to draw a diagram.',
  ['θ ≈ 55[°]', 'Formula fully substituted correctly', 'Diagram fully labelled correctly'])
guesses = '7 friends at a match guessed in which minute the first goal would be scored. The guesses were: 8, 11, 15, 17, 20, 20, 23.'
A('5-a-i', 'Q5(a)(i)', '15C', [28], [12], '1-6', 'statistics',
  'Write down the mode of the 7 numbers and find the range of the 7 numbers.',
  ['Mode: 20', 'Range: 15 [mins] (23 − 8)', 'Mode or range correct'], stem=guesses)
A('5-a-ii-iii', 'Q5(a)(ii),Q5(a)(iii)', '10D', [28], [12], '1-6', 'statistics',
  '(ii) Write down the median of the 7 numbers. (iii) Seán joined these 7 friends just before the match started and also guessed in which minute the first goal would be scored. The new median, including Seán’s guess, is now 16. Which of the following must be true about Seán’s guess? Justify your answer. It may be helpful to try some values for Seán’s guess. Seán’s guess must be (tick one box only): Equal to 16; Less than or equal to 15; More than or equal to 17.',
  ['Median: 17 [minutes]', 'Less than or equal to 15 box ticked',
   'Work of merit in (iii), for example, correct box ticked or a value trialled'], stem=guesses)
A('5-b', 'Q5(b)', '5D', [28], [13], '1-3', 'probability',
  'A board game has a spinner. A player either wins or loses points depending on which sector the spinner lands on. The size of some of the angles of the sectors and the number of points won or lost for each sector are shown in the diagram below: the diagram gives the angles 60° and 120° and labels the sectors Win X points, Win 19 points and Lose 20 points. In one sector a player wins X points. Work out the value of X, so that the spinner is fair, that is, so that the expected value of the number of points won is equal to 0 points.',
  ['x = 22', 'One correct term', 'Two correct terms'])
enl = 'The rectangle EFGH is an enlargement of the rectangle ABCD, as shown in the diagram below. The points A and B lie on [EF] as shown.'
A('6-a-i', 'Q6(a)(i)', '10B', [29], [14], '2-4', 'geometry',
  'Measure the length of [AB] and the length of [EF], in cm.',
  ['10 [cm]', 'One correct measurement'], stem=enl, extra={'measurementRequired': True})
A('6-a-ii-iii', 'Q6(a)(ii),Q6(a)(iii)', '10D', [29], [14], '2-4', 'geometry-proofs-and-constructions,geometry',
  '(ii) Use your answers to (a)(i) to work out the scale factor of the enlargement. (iii) Construct the centre of enlargement on the diagram above, and label it K.',
  ['Apply a * for not labelling K',
   'Work of merit in (ii), for example, relevant work towards the construction of the centre of enlargement'],
  stem=enl + ' Part (a)(i) asks you to measure the length of [AB] and the length of [EF], in cm.', extra={'measurementRequired': True})
circles = 'The point O is the centre of the circle u, and also the centre of the circle t. The points P and Q are on the circle u, and the points S and R are on the circle t. S ∈ [OP] and R ∈ [OQ]. |∠QOP| = 120°.'
A('6-b-i', 'Q6(b)(i)', '5A', [29], [15], '2-1', 'geometry',
  'Explain why |OP| = |OQ|.', ['are both radii of the circle u'], stem=circles)
A('6-b-ii', 'Q6(b)(ii)', '5C', [29], [15], '2-1', 'geometry',
  'Show that the triangles OPQ and OSR are similar. Give a reason for each statement that you make, where relevant.',
  ['Common angle', 'Both triangles are isosceles', 'A second angle is equal, (30° or similar explanation given'], stem=circles)
game = 'In a computer game there are a number of overhead lights that each create a circle on the ground. These circles are positioned using a co-ordinate diagram.'
cc = game + ' One of the circles, c, has equation x² + y² = 72.'
A('7-a-i', 'Q7(a)(i)', '10C', [30], [16], '2-2', 'co-ordinate-geometry-the-circle',
  'Write down the centre and radius of the circle c. Give the radius in surd form.',
  ['Centre: (0, 0)', 'Radius: √72', 'Apply a * for radius in incorrect form'], stem=cc)
A('7-a-ii', 'Q7(a)(ii)', '10C', [30], [16], '2-2', 'co-ordinate-geometry-the-circle',
  'In the game, the player must move their character so they avoid the circles of light. Tony’s character is at the point (−4, 9). Investigate if the point (−4, 9) is inside or outside the circle c. Use calculations to support your answer. Tick one box only: inside c; outside c.',
  ['97 > 72', 'Outside c', 'Point substituted correctly'], stem=cc)
A('7-b-i', 'Q7(b)(i)', '10D', [30], [17], '2-2', 'co-ordinate-geometry-of-the-line',
  'First, Tony moves his character from the point A(−4, 9) to the point B(0, 12). Find the equation of the line containing the points A and B. Give your answer in the form ax + by + c = 0.',
  ['3x − 4y + 48 = 0', 'Slope substituted into line formula', 'Point substituted into line formula'], stem=cc)
A('7-b-ii', 'Q7(b)(ii)', '5C', [30], [17], '2-2', 'co-ordinate-geometry-the-circle',
  'Next, Tony moves his character along a line l. He does not want his character to enter the circle c, where: l: x + y = 12; c: x² + y² = 72. Using simultaneous equations, or otherwise, show that the line l is a tangent to the circle c.',
  ['(y − 6)² = 0', 'Equation in terms of one variable'], stem=cc)
A('7-c-i-ii', 'Q7(c)(i),Q7(c)(ii)', '10D', [31], [18], '2-2', 'co-ordinate-geometry-the-circle',
  '(i) Construct the circle s on the co-ordinate diagram on the right. (ii) Write down the equation of the circle s.',
  ['(x − 5)² + (y + 10)² = 10²', 'One part correct and work of merit in the other part'],
  stem=game + ' Another light creates the circle s, with centre (5, −10) and radius 10.')
A('7-d', 'Q7(d)', '5B', [31], [18], '2-2', 'co-ordinate-geometry-the-circle',
  'Two more lights create the circles t and u, each with radius 10. t and u are shown on the co-ordinate diagram on the right. Tony wants to move his character along a horizontal line between the circle t and the circle u, without touching either circle. Write down the equation of one such horizontal line.',
  ['y = k, where 10 < k < 15', 'Work of merit, for example, relevant formula or relevant work on diagram'], stem=game)
island = 'Contestants on a reality show are based on an island. They are divided into Team A and Team B.'
camps = island + ' The diagram below shows the camp for each team. Both camps are in the shape of right-angled triangles. Some measurements are also shown: |PS| = 25 m, |PQ| = 60 m and |SR| = 45 m, with right angles at P and R.'
A('8-a-i', 'Q8(a)(i)', '10C', [32], [19], '2-3', 'trigonometry',
  'A fence runs along the line SQ to separate the two camps. Use the theorem of Pythagoras to show that |SQ| = 65 m.',
  ['25² + 60² = 65²', 'Formula fully substituted'], stem=camps)
A('8-a-ii', 'Q8(a)(ii)', '5C', [32], [19], '2-3', 'trigonometry',
  'Find the size of the angle marked θ in the diagram, that is, find |∠SQR|. Give your answer correct to 1 decimal place.',
  ['θ = 43·8[°]', 'Apply a * for no or incorrect rounding'], stem=camps + ' |SQ| = 65 m.')
tasks = island + ' The teams must complete tasks.'
A('8-b', 'Q8(b)', '10D', [32], [20], '3-4', 'area-volume',
  'One task is to approximate the area of the island. A contestant uses a map and measures the width of the island at 0·5 km intervals. These widths are given in the diagram below (1·2 km, 1·5 km, 1·3 km, 0·9 km and 0·8 km). Use the trapezoidal rule to estimate the area of the island, in km².',
  ['= 2·85 [km²]', 'Formula fully substituted', 'Some correct substitution'], stem=tasks)
A('8-c', 'Q8(c)', '10D', [33], [21], '2-3', 'trigonometry',
  'Another task is to row a boat from the point W to the point X, and then to the point Y. As shown in the diagram below: XY is perpendicular to AB, |∠AXW| = 42°, |∠XYW| = 65°, and |WX| = 122 m. Work out the distance from X to Y. Give your answer correct to the nearest metre.',
  ['= 124 [m]', 'Sine rule formula fully substituted'], stem=tasks)
sector = tasks + ' The final task involves contestants building a fence around a piece of land. The piece of land is in the shape of a sector with an angle of 225° and a radius of 50 m, as shown in the diagram on the right.'
A('8-d-i', 'Q8(d)(i)', '10D', [33], [22], '3-4', 'area-volume',
  'The team must build a fence all around the perimeter of the sector. Work out the total length of the perimeter of the sector. Give your answer correct to the nearest metre.',
  ['= 296 [m]', 'Length of arc found'], stem=sector)
A('8-d-ii', 'Q8(d)(ii)', '5C', [33], [22], '3-4', 'area-volume',
  'The following year, the area of the sector is doubled. This is done by increasing the radius. The angle of the sector remains 225°. Work out the length of the new radius of the sector. Give your answer in metres, correct to 1 decimal place.',
  ['r = 70·7 [m]', 'Correct equation formed'], stem=sector)
fest = 'Noreen went to a music festival.'
songs = fest + ' Noreen counted the number of songs each of 10 bands played during their particular set. The results are shown in the table below: 10, 5, 10, 11, 10, 12, 9, 10, 12, 13.'
A('9-a-i', 'Q9(a)(i)', '15C', [34], [23], '1-6', 'statistics',
  'Work out the mean and standard deviation of the 10 numbers in the table above. Give each answer correct to 1 decimal place.',
  ['Mean: 10·2', 'Standard Deviation: 2·088 … = 2·1', 'One correct answer'], stem=songs)
A('9-a-ii', 'Q9(a)(ii)', '5B', [34], [23], '1-7', 'statistics',
  'One band played 5 songs. Is this an outlier for the data in the table above? Refer to a measure of variability to explain your choice. Tick one box only: 5 is an outlier; 5 is not an outlier.',
  ['5 is an outlier', 'It is more than 2 standard deviations below the mean', 'The range halves when 5 is excluded'], stem=songs)
A('9-b', 'Q9(b)', '5C', [34], [24], '1-3', 'statistics',
  'The number of hours people at the festival spent watching bands were roughly normally distributed. The mean was 17 hours. The middle 95% of people spent between 14·2 and H hours watching bands. Using the Empirical Rule, find the standard deviation and find the value of H.',
  ['H = 17 + 2·8 = 19·8', 'One correct answer'], stem=fest)
sample = fest + ' A random sample of 540 people was picked from all those who attended the music festival in 2025. They were asked if they had also attended the festival in 2024.'
A('9-c-i', 'Q9(c)(i)', '5C', [34], [24], '1-7', 'statistics',
  'Show that, for this sample, the margin of error for a population proportion is 4·3%, correct to 1 decimal place.',
  ['= 4·3[%]', 'Formula fully substituted'], stem=sample)
A('9-c-ii', 'Q9(c)(ii)', '10C', [35], [24], '3-3', 'statistics',
  '350 of the 540 people had been at the festival in 2024. Work out the percentage of people in this sample who attended the festival in 2024. Give your answer correct to the nearest percent.',
  ['= 65[%]'], stem=sample)
A('9-c-iii', 'Q9(c)(iii)', '5C', [35], [24, 25], '1-7', 'statistics',
  'In the past (before 2025), 67% of people who attend the festival in a given year also attended the festival the previous year. Use your answers to parts (c)(i) and (c)(ii) to test the claim that this percentage has changed for the people who attended the festival in 2025, at the 5% level of significance. Show relevant calculations, state your conclusion, and give a reason for your conclusion.',
  ['60·7% ≤ p ≤ 69·3%', 'Conclusion: The percentage has not changed', 'Reason: 67% is between 60·7% and 69·3%'],
  stem=sample + ' 350 of the 540 people had been at the festival in 2024.')
A('9-c-iv', 'Q9(c)(iv)', '5B', [35], [24, 25], '1-7', 'statistics',
  'The organisers want to reduce the margin of error for the survey. Should they increase or decrease the number of people in the sample? Remember the margin of error for the population proportion was 4·3%. Use calculations to support your answer. Tick one box only: Increase; Decrease.',
  ['Increase box ticked', 'A larger sample reduces the margin of error'], stem=sample)
A('10-a', 'Q10(a)', '10C', [36], [26], '3-4', 'area-volume',
  'An ice-cream cone has a radius of 2·8 cm and a vertical height of 13·4 cm, as shown in the diagram below. The entire cone is filled with ice-cream. There is also a hemisphere, of the same radius, of ice-cream on top of the cone. By finding the volume of the cone and the volume of the hemisphere, work out the total volume of ice-cream, correct to the nearest cm³.',
  ['= 156 [cm³]', 'Volume of cone OR hemisphere formulated'])
cans = 'Some soft drinks companies have changed the dimensions of their cylindrical cans. The table below shows the approximate dimensions of the old and the new designs: the old can design (cylinder) has radius 3·3 cm and height 11·5 cm; the new can design (cylinder) has radius 3 cm and height h.'
A('10-b-i', 'Q10(b)(i)', '10C', [36], [27], '3-4', 'area-volume',
  'Each can design has a volume of 393·4 cm³, correct to 1 decimal place. Work out the height, h, of the new can design. Give your answer correct to 1 decimal place.',
  ['13·9 cm', 'Equation set up', 'Apply a * for no units'], stem=cans)
A('10-b-ii', 'Q10(b)(ii)', '10D', [36], [27], '3-4', 'area-volume,number-systems',
  'The total surface area of the new can design is 318·6 cm² correct to 1 decimal place. Work out the percentage increase in the total surface area from the old can design to the new can design. Give your answer as a percent correct to 1 decimal place.',
  ['3·8 [%]', 'Total surface area found', 'Curved surface area OR area of circle formulated'], stem=cans)
A('10-b-iii', 'Q10(b)(iii)', '10C', [37], [27, 28], '3-4', 'area-volume',
  'Remember that the radius of the old can is 3·3 cm and that the radius of the new can is 3 cm. A shop has a shelf of length 62 cm and depth 32 cm. All cans are placed upright and are not stacked on top of each other. The cans are in rows, where the first row is placed along the edge of the shelf and each other row is placed directly behind the first row. The entire base of each can must be in contact with the shelf. The diagram below shows some of the cans on the shelf. Work out how many more cans could be placed on this shelf if the new can design was used instead of the old can design.',
  ['9 × 4 = 36 cans', '10 × 5 = 50 cans', '50 − 36 = 14 extra cans', '36 OR 50 correctly found'], stem=cans)
A('10-c', 'Q10(c)', '10D', [37], [29], '3-3', 'number-systems',
  'In 2020, a soft drink had 35 grams of sugar in a 330 millilitre can. In 2021, the company made a new recipe with 30% less sugar. In 2025, the company reduced the sugar in the 2021 recipe by a further 20%. Work out how many grams of sugar are in a 500 millilitre bottle of the 2025 recipe. Give your answer correct to 1 decimal place.',
  ['= 29·7 [g] of sugar', 'Finds 70% of a relevant number', 'Converts a sugar content from 330 ml to 500 ml'])

selection_review = [
    {'pages': [3, 4, 16], 'wording': 'any five / any three questions', 'classification': 'exam-level-selection',
     'reason': 'Candidates select independently marked questions; every question is retained. No combined multi-question practice cards.'},
    {'pages': [8], 'wording': 'choose one activity from each of three categories / remove one activity from one of the categories', 'classification': 'counting-context',
     'reason': 'The choices are the objects being counted (5 × 6 × 4) and the category to tick is the answer to a required comparison; nothing is a menu of practice prompts.'},
    {'pages': [8, 12, 16, 23, 25], 'wording': 'Tick one box only', 'classification': 'answer-selection',
     'reason': 'The ticked category, median condition, inside/outside, outlier and increase/decrease boxes are the mathematical answers with justification, not alternative prompts.'},
    {'pages': [13], 'wording': 'A player either wins or loses points', 'classification': 'given-context',
     'reason': 'Describes the spinner outcomes used in one expected-value task.'},
    {'pages': [17], 'wording': 'Using simultaneous equations, or otherwise', 'classification': 'method-choice',
     'reason': 'Alternative solution methods for the same marked task; no printed pool of prompts.'},
    {'pages': [18], 'wording': 'Write down the equation of one such horizontal line', 'classification': 'open-answer',
     'reason': 'Any line y = k with 10 < k < 15 earns the same scale; the set is not a finite printed pool.'},
]
def classify(c):
    t = c['context']
    if 'questions' in t and 'any' in t.lower():
        return ('exam-level-selection', 'Select separately marked questions for the examination; every question is retained for practice.')
    if 'or otherwise' in t:
        return ('method-choice', 'Alternative solving methods for the same marked task, with no printed pool of prompts.')
    if 'activity from' in t:
        return ('counting-context', 'Choosing one activity per category is the counting situation itself (or the category to tick is the answer); every printed ask is required.')
    if 'either wins or loses' in t:
        return ('given-context', 'Describes the spinner outcomes of a single expected-value task.')
    if 'One of the circles' in t:
        return ('given-context', 'Names the circle c from the game; not a selection instruction.')
    if 'one such horizontal line' in t:
        return ('open-answer', 'Any horizontal line strictly between the circles is accepted under one 5B scale (y = k, 10 < k < 15); nothing finite to expand.')
    return None
p.write(selection_review, classify)
