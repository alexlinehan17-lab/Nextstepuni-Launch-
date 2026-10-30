"""Independent printed-paper/mark-boundary review: 2025 deferred OL Paper 2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper

PREFIX='maths-2025-ol-p2-deferred'
p=Paper(year=2025,level='ordinary',paper_key='p2',sitting='deferred',
    paper_file='LC003GLP200EV-deferred.pdf',scheme_file='LC003GLP000EV-deferred.pdf',
    prefix=PREFIX,ref='2025 OL Paper 2 — Deferred',
    scales={'5B':[0,2,5],'5C':[0,2,3,5],'10C':[0,4,6,10],'10D':[0,3,5,7,10],'15D':[0,6,8,10,15]},
    reviewed_at='2026-10-30',general_notes=[2,24,25,26,27],scheme_pages=[1,2]+list(range(23,45)),
    printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
    review_method='Independent visual sweep of every page of the 32-page question paper and scheme pages 23–44, with the general source note on pages 1–2. All printed parts reconciled against their own published scales. Every typeset question and solution crop is inspected separately before publication.',
    source_notes=[
        'All ten questions retained: 380 offered marks. Candidates choose five Section A and three Section B questions for 300 marks.',
        '45 separately marked tasks. Q4(a)(i)–(iii), Q5(a)(i)–(ii), and Q10(a)(ii)–(iii) each share a scale and remain together.',
        'The scheme labels printed Q2(b)(i) as (b), and printed Q2(b)(ii) as (c). Cards retain the paper labels and cite the exact scheme rows.',
        'Q7(a)(ii) and Q7(b)(i) print Scale 10C (0,3,7,10) rather than the general Paper 2 (0,4,6,10). The task-specific awards are retained and explained.',
        'Q5(a)(i) prints DE instead of CD and cm after the scale factor in the model answer. The ratio is CD/AB=12/8=1.5, and a scale factor has no units. A source note explains these printing errors.',
        'Q10(b)(i) has a blank model-answer tree in the printed scheme. A separately labelled NextStepUni worked example completes all branches/outcomes from the given probabilities. The original SEC credit notes remain intact.',
        'Q10(b)(iii) says to assume rain on all three days. Under the usual independent-day model its conditional probability is (0.25)^2(0.75)=0.046875, or 0.0469. The scheme instead multiplies 0.1625^2 by 0.4875 to obtain 0.0129, including the chance of rain again. Both source and mathematical clarification are visible; no revised SEC marking rule is invented.',
        'The extracted scheme text at PDF page 38 corrupts the word Median into repeated mathematical M glyphs. Its sole answer line was visually transcribed as Median = 13 from the original row; the source PDF/crop is unchanged.',
        'Q3(d) is one required choice-and-reason answer with all three options, not three cards. The spinner choice in its stem and the flag restrictions in Q7(b)(iv) are situations to analyse, not a choice of examination tasks.',
    ],out_name='2025-ordinary-p2-deferred.json',atlas_prefix='mathematics-ordinary-',section_of=lambda q:'A' if q<=6 else 'B')

def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None,extra=None):
    p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,
        dict(extra or {},figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))

A('1-a','Q1(a)','10C',[27],[4],'2-2','co-ordinate-geometry-of-the-line',
  'The line p has a slope of 3/2 and crosses the y-axis at the point (0, 4). Find the equation of p.',
  ['Formula with partial substitution'])
A('1-b','Q1(b)','10C',[27],[4],'2-2','co-ordinate-geometry-of-the-line,area-volume',
  'Find the area of the triangle formed by joining the following three points: O(0, 0), A(3, 4), B(5, −1).',
  ['Correct formula fully substituted','Apply a * for no units'])
A('1-c','Q1(c)','10C',[27],[5],'2-2','co-ordinate-geometry-of-the-line',
  'The diagram below shows four lines, labelled p, q, r, and s. The slope of each of the four lines is given in the table. Identify each of the lines in the diagram by writing the appropriate label into the space in the table beside the slope. Slopes: −1/5, 2, −1, 1/2.',
  ['Any one slope correct.','Any 2 slopes correct'])
circle='The circle c has equation x² + y² = 169.'
A('2-a-i','Q2(a)(i)','5C',[28],[6],'2-2','co-ordinate-geometry-the-circle',
  'Find the centre and the radius of the circle c.',
  ['Accept correct answers without work','Centre or Radius correct'],stem=circle)
A('2-a-ii','Q2(a)(ii)','5C',[28],[6],'2-2','co-ordinate-geometry-the-circle',
  'Is the point (1, 12) on the circle c? Give a reason for your answer.',
  ['Substitutes in for either x or y','Apply a * for no reason.'],stem=circle)
k='The circle k, shown in the diagram on the right, has its centre on the x-axis and contains the points O(0, 0) and T(4, 0).'
A('2-b-i','Q2(b)(i)','10C',[28],[7],'2-2','co-ordinate-geometry-the-circle',
  'Find the centre and the equation of k.',
  ['Centre and Radius correct','Centre or radius correct'],stem=k,
  extra={'markingNote':'The marking scheme labels this row Q2(b); it corresponds to Q2(b)(i) in the question paper.'})
A('2-b-ii','Q2(b)(ii)','10C',[29],[7],'2-1','geometry,co-ordinate-geometry-the-circle,area-volume',
  'PQRS is a square. S and Q are on the x-axis. PQ, QR, RS, and SP are tangents to k, as shown. Find the area of PQRS.',
  ['Identifies square has a side of 4','Apply a * for no units'],stem=k,
  extra={'markingNote':'The marking scheme labels this row Q2(c); it corresponds to Q2(b)(ii) in the question paper.'})
spinners='Part of a board game involves gathering tokens. At certain points in the game a player can choose to spin one of the two fair spinners shown in the diagrams below. They will collect the number of tokens the arrow stops on. For example, on Spinner A shown below a player would collect 6 tokens. Spinner A has four equal sectors: 4, 0, 6, 2. Spinner B has six equal sectors: 4, 8, 0, 1, 3, 0.'
A('3-a','Q3(a)','5C',[30],[8],'1-1','counting,probability',
  'A player spins Spinner A twice and collects a total of 6 tokens. List the four possible ways this could have happened.',
  ['Identifies one possible way','Identifies two possible ways'],stem=spinners)
A('3-b','Q3(b)','5C',[30],[8],'1-2','probability',
  'A player spins Spinner A once and Spinner B once. What is the probability that the player collects a total of 0 tokens?',
  ['Correct formula written','Equates both fractions but fails to finish'],stem=spinners)
A('3-c','Q3(c)','10D',[30],[8,9],'1-3','probability',
  'Spinner B is spun a large number of times. Find the expected average number of tokens that a player will collect each time.',
  ['Works out any one correct expected value','Finds all correct fractions but fails to add'],stem=spinners)
A('3-d','Q3(d)','10C',[30],[8,9],'1-3','probability',
  'Jill is playing a board game that uses both spinners. She has calculated that the expected average number of tokens for one spin of spinner A is 3. At certain points in the game she can choose one of the three options below: Option 1: Pay 2 tokens and spin Spinner A. Option 2: Pay 2 tokens and spin Spinner B. Option 3: Do not spin either spinner. Jill decides that she will choose one option at the beginning of the game and will always use that option in the game. Based on the expected average number of tokens for one spin of each spinner, which option would you advise Jill to choose? Tick one box only. Give a reason for your answer.',
  ['Writes expected average of B in this part.','Gives correct option but fails to give a reason'],stem=spinners)
A('4-a-i-ii-iii','Q4(a)(i),Q4(a)(ii),Q4(a)(iii)','15D',[31],[10,11],'1-6','statistics',
  '(i) Fill in the six missing numbers on the horizontal axis on the diagram above. (ii) Using the Empirical Rule, or otherwise, find the approximate number of males in the sample who have diastolic blood pressure between 70 and 90. (iii) Use the Empirical Rule to find the approximate percentage of males in the sample who have diastolic blood pressure greater than 90.',
  ['Indicates mean ± standard deviation','Any one part of (i), (ii) or (iii) correct','Any two parts of (i), (ii) or (iii) correct'],
  stem='A sample of 1500 males is selected at random. For this sample, diastolic blood pressure is normally distributed, with a mean of 80 and a standard deviation of 10. The normal curve below shows the blood pressure of the 1500 males in this sample.')
sector='The diagram shows a sector of a circle of radius 12 cm, with an angle of 77°.'
A('4-b-i','Q4(b)(i)','10C',[31],[11],'3-4','area-volume',
  'Find the area of the sector. Give your answer, in cm², correct to 1 decimal place.',
  ['Correct formula fully substituted','Apply a * for no or incorrect rounding'],stem=sector)
A('4-b-ii','Q4(b)(ii)','5C',[31],[11],'3-4','area-volume',
  'Find the length of the perimeter of the sector. Give your answer, in cm, correct to 1 decimal place.',
  ['Correct formula written','Arc length (16·126)','Apply a * for early rounding'],stem=sector)
enlarge='The triangles OAB and OCD are shown in the diagram. The triangle OCD is the image of the triangle OAB under an enlargement of centre O and scale factor k. |AB| = 8 cm. |CD| = 12 cm.'
A('5-a-i-ii','Q5(a)(i),Q5(a)(ii)','10D',[32],[12],'2-4','geometry',
  '(i) Show that k = 1·5. (ii) Given that |OC| = 15 cm, find |OA|, the distance from O to A.',
  ['Either part (i) or part (ii) correct','One part correct and work of merit in the other'],stem=enlarge)
A('5-b','Q5(b)','10C',[32],[12,13],'2-4','geometry,area-volume',
  'Find the area of the triangle OCD. (Remember that k = 1·5.)',
  ['Correct formula fully substituted','Apply a * for no units'],stem=enlarge+' The area of triangle OAB is 36·7 cm².')
A('5-c','Q5(c)','10C',[32],[12,13],'3-4','area-volume',
  'Find the value of h, the perpendicular height of triangle OAB, as shown in the diagram.',
  ['Correct formula fully substituted','Apply a * for no units'],stem=enlarge+' The area of triangle OAB is 36·7 cm².')
tri='In the triangle XYZ: |XY| = 10 cm, |XZ| = 8 cm, and |∠ZXY| = 50°.'
A('6-a-i','Q6(a)(i)','10C',[33],[14],'2-3','trigonometry,area-volume',
  'Find the area of the triangle XYZ. Give your answer, in cm², correct to 1 decimal place.',
  ['Correct formula fully substituted'],stem=tri)
A('6-a-ii','Q6(a)(ii)','10C',[33],[14],'2-1','geometry-proofs-and-constructions',
  'Construct the triangle XYZ in the box below. Show all your construction lines clearly. The point X is shown below. Part of the line XY is also shown.',
  ['Any one line drawn correctly to scale','Two correct elements drawn.','Tolerance of ±0·25 cm and ±5°'],stem=tri)
A('6-b','Q6(b)','10C',[33],[15],'2-1','geometry',
  'The triangle PQR is isosceles with |PQ| = |PR|, as shown in the diagram. P lies on the line QS. |∠SPR| = 122°. Find the size of the angle marked x and the size of the angle marked y, in the diagram.',
  ['x or y found correctly'])
abseil='As part of the Croke Park experience, it is possible to descend by rope (abseil) from the roof of the stadium to ground level. Aidan (A) does this abseil, down a vertical height of 45·7 m. His friend Laura (L) is waiting for him on the ground. She stands 35 m directly across from where he is due to land, as shown in the diagram. The angle θ is the angle from the ground at Laura’s feet to the roof, at the place where Aidan starts his abseil.'
A('7-a-i','Q7(a)(i)','5C',[34],[16],'2-3','trigonometry',
  'Write down tan θ, in the form a/b, where a, b ∈ ℝ, and hence find the value of θ. Give your angle correct to the nearest degree.',
  ['Correct Trig Ratio Formula written','Apply a * for no or incorrect rounding'],stem=abseil)
exception={'permittedMarks':[0,3,7,10],'markingNote':'This task’s printed 10C row awards 3 and 7 partial-credit marks. The general Paper 2 table lists 4 and 6; the task-specific row is used here.'}
A('7-a-ii','Q7(a)(ii)','10C',[34],[16],'2-3','trigonometry',
  'Work out the distance from A to L. Give your answer correct to 1 decimal place.',
  ['One error but finishes correctly','Apply a * for early rounding'],stem=abseil,extra=exception)
A('7-a-iii','Q7(a)(iii)','5B',[34],[17],'3-3','number-systems',
  'Some time later Aidan read a review of the Croke Park experience. He noted that the height of the abseil was given as 150 feet. Use the two measurements for the height of the abseil (150 feet and 45·7 m) to find a general multiplier which will convert feet to metres. That is, find the value of k ∈ ℝ so that: Length in feet × k = length in metres. Give your answer correct to 3 decimal places.',
  ['Fully substitutes the given formula correctly but fails to finish or finishes incorrectly','Apply a * for no or incorrect rounding'])
course='Adam is mapping a course for an Adventure Race. Adam has measurements for some parts of the course. The diagram shows the lengths and the sizes of the angles that Adam knows. He needs to use these measurements to work out some of the remaining lengths.'
A('7-b-i','Q7(b)(i)','10C',[34],[18],'2-3','trigonometry',
  'In the triangle SUV, |SU| = 3·5 km. |∠SUV| = 30°. |∠UVS| = 125°. Use the sine rule to find the length of the side marked y. Give your answer, in km, correct to 2 decimal places.',
  ['Sine Rule Formula fully substituted','Apply a * for no or incorrect rounding'],stem=course,extra=exception)
A('7-b-ii','Q7(b)(ii)','10D',[35],[18],'2-3','trigonometry',
  'In the triangle STU, |∠UST| = 45°. |ST| = 2·5 km. |SU| = 3·5 km. Use the cosine rule to find the length of the side marked z. Give your answer, in km, correct to 2 decimal places.',
  ['Zero Credit: Treats triangle as right angled','Cosine Rule formula fully substituted','Apply a * for no or incorrect rounding'],stem=course)
flags='For each race, Adam must place 6 flags labelled A, B, C, D, E, and F at random locations along the course.'
A('7-b-iii','Q7(b)(iii)','5B',[35],[19],'1-1','counting',
  'In the first race, the flags can be arranged in any order along the course. Find the total number of arrangements of flags that are possible.',
  ['Accept correct answer without work','multiplication of two relevant numbers'],stem=flags)
A('7-b-iv','Q7(b)(iv)','5C',[35],[19],'1-1','counting',
  'In the second race, the first flag must be either A or F and the last flag must be A or F. The remaining flags can be arranged in any order along the course. Find the total number of arrangements of flags that are possible.',
  ['Accept correct answer without work','Identifies correct values to multiply for first and last value, but fails to finish correctly'],stem=flags)
step='A concrete step is 150 cm long, 20 cm high, and 30 cm wide, as shown in the diagram below.'
A('8-a-i','Q8(a)(i)','10C',[36],[20],'3-4','area-volume',
  'Find the volume of the step. Give your answer in cm³.',
  ['Accept correct answer without work','Multiplies any two lengths correctly'],stem=step)
A('8-a-ii','Q8(a)(ii)','10D',[36],[20],'3-4','area-volume',
  'To reduce the weight of a step, 5 holes are bored through each step, removing 5 cylinders of concrete, as shown in the diagram below. Each cylinder of concrete that is removed has a radius of 6 cm and a height of 30 cm. Find the remaining volume of a step when the 5 cylinders of concrete are removed. Give your answer in cm³, correct to 1 decimal place.',
  ['Correctly finds the volume of one cylinder','Correctly finds volume of 5 cylinders but fails to finish'],stem=step)
A('8-b','Q8(b)','10C',[36],[21],'3-3','financial-maths',
  '50 different steps are needed for a special project. The volume of concrete in each step is 0·125 m³. The cost of the concrete for the steps is €185 per m³ before VAT is added. VAT at 13·5% is then added to the cost. Find the overall cost of the 50 steps after VAT is added. Give your answer correct to the nearest euro.',
  ['Finds 1156·25'])
A('8-c','Q8(c)','10C',[37],[22],'3-4','area-volume',
  'A solid garden ornament consists of a cone on top of a sphere. The height of the cone is 16 cm. The radius of the cone is 6 cm. The radius of the sphere is also 6 cm. Find the volume of the garden ornament. Give your answer in cm³, in terms of π.',
  ['Writes formula for cone or sphere.','Finds volume of cone or volume of sphere correctly'])
A('8-d','Q8(d)','10D',[37],[23],'3-4','area-volume',
  'The ornament is put into a closed rectangular box with dimensions 13 cm, 13 cm, and 29 cm, as shown. Find the surface area of this closed rectangular box.',
  ['All side surfaces or top and bottom surfaces identified correctly','All surface areas identified correctly'])
youth='In a Youth Club, the ages of children, in years, are recorded in the following table. Age (years): 12, 13, 14, 15, 16. Number of Children: 13, 10, 8, 5, 4.'
A('9-a-i','Q9(a)(i)','10C',[38],[24],'1-5','statistics',
  'In the grid below, draw a suitable chart or graph to represent the data in the table. If you use a pie chart, show all your calculations clearly.',
  ['4 correct boxes drawn in bar chart','2 sectors in the pie chart'],stem=youth)
A('9-a-ii','Q9(a)(ii)','5B',[38],[24],'1-6','statistics',
  'Find the median age of the children in the table.',
  ['Median = 13'],stem=youth)
A('9-a-iii','Q9(a)(iii)','5B',[38],[24,25],'1-2','probability',
  'One child is picked at random from the children in the youth club. What is the probability that this child is 13 years of age?',
  ['correct numerator or denominator'],stem=youth)
A('9-a-iv','Q9(a)(iv)','10C',[38],[25],'1-2','probability',
  'Three children are picked at random from the children in the youth club. What is the probability that the 3 children were born on the same day of the week? You may assume that the probability of being born on each day is the same. Give your answer correct to 2 decimal places.',
  ['Any one correct probability written','Finds three correct probabilities but fails to finish correctly'])
sample='A random sample of 250 youth club members in Connaught were asked their age. 160 of these were 14 years or older.'
A('9-b-i','Q9(b)(i)','5C',[39],[26],'1-6','statistics',
  'Find the percentage of members in this sample who were 14 years or older.',
  ['160','250','0·64'],stem=sample)
A('9-b-ii','Q9(b)(ii)','5C',[39],[26],'1-7','statistics',
  'Show that, for this sample, the margin of error for a population proportion is 6·3%, correct to 1 decimal place.',
  ['Correct formula fully substituted','Apply a * for no or incorrect rounding'],stem=sample)
A('9-b-iii','Q9(b)(iii)','10D',[39],[26],'1-7','statistics',
  'In Ireland, 60% of youth club members are 14 years or older. Use your answers to parts (b)(i) and (b)(ii) to test the claim that the percentage of youth club members in Connaught who are 14 years or older is different from the population percentage, at the 5% level of significance. Show relevant calculations, state your conclusion, and give a reason for your conclusion.',
  ['Correct range written','Correct range and conclusion given, but no reason written','Correct range and reason given, but incorrect conclusion written'],
  stem=sample+' Part (b)(i) asks for the sample percentage; part (b)(ii) gives the margin of error as 6·3%.')
teams='The students in a PE class are divided into two groups, Team A and Team B. In a speed test, the time that each student took to sprint 50 metres was recorded. The results, in seconds, are shown below. Team A: 5·9, 6·3, 6·9, 6·9, 7·1, 7·1, 7·2, 7·3, 7·5, 7·7, 7·7, 8·2, 8·4, 8·5, 9·1. Team B: 6·3, 6·5, 6·8, 6·8, 6·9, 7·6, 7·6, 8·1, 8·3, 8·4, 9·3, 9·4, 9·5, 9·6, 9·6.'
A('10-a-i','Q10(a)(i)','10D',[40],[27],'1-5','statistics',
  'Complete the back to back stem and leaf diagram below to show the recorded data.',
  ['Either Team A or Team B diagram fully correct','Up to 25 items filled in correctly'],stem=teams)
A('10-a-ii-iii','Q10(a)(ii),Q10(a)(iii)','10C',[40],[27],'1-6','statistics',
  '(ii) Find the range of the sprint times for both teams. (iii) Find the median sprint time for both Team A and Team B.',
  ['Any one Range or Median time written correctly','Either part (ii) or (iii) fully correct'],stem=teams)
A('10-a-iv','Q10(a)(iv)','5B',[40],[27],'1-6','statistics',
  'Use your answers from parts (a)(i), (a)(ii), and (a)(iii) above to write a sentence to compare the performance of Team A and Team B in the speed test.',
  ['incomplete sentence or doesn’t compare A and B'],
  stem=teams+' The preceding parts ask for a back to back stem and leaf diagram, the range for each team, and the median for each team.')
walk='Kim has a dog called Max. When it is raining, the probability of Kim taking Max for a walk is 0·75. When it is dry the probability of her taking Max for a walk is 0·98. On a particular Saturday, the weather forecast is showing a 0·65 chance of rain. This information is shown in the tree diagram below.'
A('10-b-i','Q10(b)(i)','10D',[41],[28],'1-2','probability',
  'Complete the diagram below by filling in the 3 missing outcomes and the 6 missing probabilities. For example, the probability that it is raining and Kim takes the dog for a walk is 0·4875, as shown. Key: Rain R; Dry D; Walk W; No Walk N.',
  ['Any three correct additional outcomes or probabilities added to table','Any three correct additional outcomes and probabilities added to table'],stem=walk)
A('10-b-ii','Q10(b)(ii)','5C',[41],[28,29],'1-2','probability',
  'What is the probability that Kim will bring Max for a walk on Saturday?',
  ['Identifies both probabilities/outcomes but fails to add'],stem=walk)
A('10-b-iii','Q10(b)(iii)','10C',[42],[29],'1-2','probability',
  'Assume that it will rain for the next three days. What is the probability that, during these three days, Kim will bring Max for a walk for the first time on the third day? Give your answer correct to 4 decimal places. Remember that when it is raining, the probability of Kim taking Max for a walk is 0·75.',
  ['Identifies any one correct probability/outcome','Identifies three correct probabilities/outcomes but fails to finish correctly','Apply a * for no or incorrect rounding'])

assert len(p.cards)==45
selection_review=[
 {'pages':[3,4,16],'wording':'any five / any three questions','classification':'exam-level-selection','reason':'Retain every question for practice, including ones not selected in the examination.'},
 {'pages':[8,9],'wording':'choose to spin one of the two / choose one of the three options / Tick one box only','classification':'answer-selection','reason':'These are a probability situation and one required advice-and-reason response. All three options remain visible in the single Q3(d) card.'},
 {'pages':[10],'wording':'Empirical Rule, or otherwise','classification':'method-choice','reason':'Alternative methods solve the same required normal-distribution task.'},
 {'pages':[19],'wording':'first flag must be either A or F','classification':'scenario-constraint','reason':'The task asks for the total number of arrangements, not a choice of questions.'},
 {'pages':[24],'wording':'suitable chart or graph / If you use a pie chart','classification':'method-choice','reason':'One chart task with alternative valid representations, carrying one shared scale.'},
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','Candidate exam selection; every question is retained for practice.')
 if 'spinner' in t or 'option' in t or 'tick' in t:return ('answer-selection','One probability question with the complete choice and justification prompt.')
 if 'otherwise' in t:return ('method-choice','Alternative mathematical methods, not alternative tasks.')
 if 'flag' in t:return ('scenario-constraint','Restrictions within one counting problem, not a task menu.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
