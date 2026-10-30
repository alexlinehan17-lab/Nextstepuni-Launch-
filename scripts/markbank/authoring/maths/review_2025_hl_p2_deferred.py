"""Independent visual paper and published-scale review: 2025 deferred HL Paper 2."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper

PREFIX='maths-2025-hl-p2-deferred'
p=Paper(year=2025,level='higher',paper_key='p2',sitting='deferred',
    paper_file='LC003ALP200EV-deferred.pdf',scheme_file='LC003ALP000EV-deferred.pdf',
    prefix=PREFIX,ref='2025 HL Paper 2 — Deferred',
    scales={'5B':[0,2,5],'5C':[0,2,3,5],'5D':[0,2,3,4,5],
            '10B':[0,5,10],'10C':[0,4,7,10],'10D':[0,3,5,7,10],
            '15C':[0,5,10,15],'15D':[0,4,7,11,15]},
    reviewed_at='2026-10-30',general_notes=[2,27,28,29,30],scheme_pages=[1,2]+list(range(26,49)),
    printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
    review_method='Independent visual sweep of all 32 question-paper pages and scheme pages 26–48, with the source introduction on pages 1–2. Each printed task reconciled against its published allocation. All question and solution images independently inspected before publication.',
    source_notes=[
        'All ten questions retained: 380 offered marks, with candidates selecting five Section A and three Section B questions for 300 marks.',
        '43 separately marked tasks. Q2(a)(i)–(ii), Q3(a)(i)–(ii), Q3(b)(i)–(ii), Q4(a)–(b), and Q9(b)(i)–(ii) each share a published scale and remain together.',
        'Scheme page 31 incorrectly heads the section Paper 1 and repeats Q1(a)(i) for the angle row. These are Paper 2 solutions; the second row corresponds to printed Q1(a)(ii).',
        'Q4(b) interchanges the exact cosine and sine magnitudes in an intermediate line. The correct expression is √3/2 − (−1/2); the final value 1.3660 remains correct. A source note explains this.',
        'Q5(a) requires one proof with Diagram, Given, To Prove, Construction, and Proof headings. These headings are not separate questions. Q5(b) asks for one freely chosen valid pair a,d, not a finite option pool.',
        'Q6(a)(i) omits parentheses around −1 when squaring. A note clarifies that (−1)²=1 and the radius is √(4+1+20)=5.',
        'Q7(a) preserves the complete original construction grid, coordinate scale and measurement instruction. Q7(c) is one yes/no-and-justification response. All sequence-dependent parts retain the first-triangle and unit-height context.',
        'Q9(a)(ii) uses A to denote urban voters in its model solution; elsewhere Alayah is a candidate name. The card note identifies the intended event and the correct union calculation.',
        'Q10(a)(i) rounds z to 0.67 before looking up 74.86%. Direct calculation without that intermediate rounding gives about 74.75%. Both approaches are explained without changing the published scale.',
        'Q10(a)(i) high-partial guidance says 3 correct new entries, and Q10(a)(ii) uses probability-of-two/three-results wording. These appear copied from earlier questions. Original notes and numeric bands are retained; no replacement official marking criteria are invented.',
        'Q10(a)(ii) has a tail-sign slip. The required cumulative probability is P(Z ≤ z)=0.5918, giving z≈0.23 and k≈79.4. The note distinguishes this from the printed P(Z > x)=0.5918.',
        'Q10(c)(iii) selects a different second committee, leaving 251 choices, exactly one of which is the complement. The denominator must not silently change to 252.',
    ],out_name='2025-higher-p2-deferred.json',atlas_prefix='mathematics-higher-',section_of=lambda q:'A' if q<=6 else 'B')

def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None,extra=None):
    p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,
          dict(extra or {},figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))

triangle='The three points A(0, 0), B(4, 2), and C(6, −6) form a triangle, as shown in the diagram below. θ is the acute angle between [AB] and [AC].'
A('1-a-i','Q1(a)(i)','10C',[31],[4],'2-2','co-ordinate-geometry-of-the-line',
  'Find slope of the line AB and the slope of AC.',
  ['Some effort at finding a slope','One slope found'],stem=triangle)
A('1-a-ii','Q1(a)(ii)','10C',[31],[4],'2-2','co-ordinate-geometry-of-the-line,trigonometry-triangles',
  'Hence, or otherwise, find the value of θ. Give your answer correct to 1 decimal place.',
  ['Some correct substitution into formula','Fully correct substitution into formula','Apply a * for no or incorrect rounding'],stem=triangle,
  extra={'markingNote':'The scheme repeats the label Q1(a)(i) on this row. Its angle calculation corresponds to Q1(a)(ii) in the question paper.'})
A('1-b','Q1(b)','10C',[31],[4,5],'2-2','co-ordinate-geometry-of-the-line',
  'Find the shortest distance from B to the line AC. Give your answer in the form p√q, where p, q ∈ ℕ.',
  ['Finds the equation of the line AC','Apply a * for incorrect format'],stem=triangle)
A('2-a-i-ii','Q2(a)(i),Q2(a)(ii)','15D',[32],[6],'1-3','statistics-z-scores',
  '(i) Fill in the 6 missing numbers in the diagram above. (ii) Using the empirical rule, or otherwise, find the number of candidates who were awarded a mark between 70 and 235.',
  ['One part correct','One part correct and work of merit in the other part'],
  stem='In an exam, the marks awarded to 30 000 candidates were normally distributed, with a mean mark of 180 and a standard deviation of 55 marks. The scaled diagram below shows the distribution of marks on the exam.')
spinner='A spinner has exactly four different sectors. In a game, the spinner is spun once. The probability of landing on each sector is given in the table below. The amount of money that you get for landing on each sector is also shown. Sector A: probability 3/5, €0; B: probability 1/20, €100; C: probability 1/4, €10; D: probability 1/10, €25.'
A('2-b-i','Q2(b)(i)','10C',[32],[7],'1-3','probability',
  'Work out the cost to play this game, so that the expected value of the profit for someone playing the game would be − €0·50.',
  ['A correct term formulated','All terms formulated'],stem=spinner)
A('2-b-ii','Q2(b)(ii)','5B',[32],[7],'1-2','probability',
  'Each spin of the spinner is independent. The first time that it is spun, it lands on sector C. The spinner is spun a second time. Find the probability that it lands on sector C again, given that it landed on sector C the first time. Justify your answer.',
  ['Correct answer no justification'],stem=spinner)
events='A, B, and C are three events. P(A) = 0·3, P(B) = 0·15, and P(A ∩ B) = 0·05.'
A('3-a-i-ii','Q3(a)(i),Q3(a)(ii)','10D',[33],[8],'1-2','probability',
  '(i) Find the value of P(A \\ B), that is, the probability that A happens but B does not happen. (ii) Find the value of P(A ∪ B).',
  ['One part correct','One part correct and work of merit in the other part'],stem=events)
A('3-b-i-ii','Q3(b)(i),Q3(b)(ii)','10C',[33],[8,9],'1-2','probability',
  '(i) Write down the value of P(A ∪ C), in terms of x. Remember that P(A) = 0·3. (ii) Find the value of P(A | C), the probability that A happens given that C has happened.',
  ['Accept correct answers without work','One part correct'],stem=events+' P(C) = x, where x ∈ ℝ, 0 ≤ x ≤ 1. A and C are mutually exclusive.')
A('3-c','Q3(c)','10C',[33],[8,9],'1-2','probability',
  'P(B ∩ C) = 0·08 and P(B | C) = 1/3. Find the value of x = P(C).',
  ['Relevant work on a Venn diagram'],stem=events+' P(C) = x, where x ∈ ℝ, 0 ≤ x ≤ 1.')
A('4-a-b','Q4(a),Q4(b)','10D',[34],[10],'2-3','trigonometry-functions-identities',
  '(a) cos A = 1/√2 and sin A = −1/√2, where 0 ≤ A ≤ 2π. Find the value of A. (b) f(x) = cos x − sin x, where −2π ≤ x ≤ 2π. Find the value of f(−π/6). Give your answer correct to 4 decimal places.',
  ['One part correct','One part correct and work of merit in the other part','Apply a * for incorrect format'])
A('4-c','Q4(c)','10C',[34],[10],'2-3','trigonometry-functions-identities',
  'Solve the equation: 2 sin(2x) = √3, where 0 ≤ x ≤ 180°.',
  ['One correct value for x'])
A('4-d','Q4(d)','10C',[34],[11],'2-3','trigonometry-functions-identities,functions',
  'The function g(x), where x ∈ ℝ, is defined as follows: g(x) = 140 + 110 cos(3x). Part of the graph of y = g(x) is shown on the diagram below. The horizontal lines y = A and y = B are shown, where A, B ∈ ℕ. The vertical line x = C is also shown, where C ∈ ℝ. Find the value of A, the value of B, and the value of C. Write C in terms of π.',
  ['One value correct','Two values correct'])
A('5-a','Q5(a)','15D',[35],[12],'2-1','geometry-constructions-proofs',
  'Let ABC be a triangle. Prove that, if a line l is parallel to BC and cuts [AB] in the ratio s : t, where s, t ∈ ℕ, then it also cuts [AC] in the same ratio. Use the headings: Diagram, Given, To Prove, Construction, Proof.',
  ['Relevant diagram drawn','Construction clearly indicated','Proof missing 1 relevant step'])
A('5-b','Q5(b)','15C',[35],[13],'2-1','geometry',
  'XYZ is a triangle. The points P and Q lie on [XY] and the points R and S lie on [XZ]. The lines PR, QS, and YZ are all parallel. As shown in the diagram, |XP| = 4, |PQ| = 7, and |QY| = 10. |XR| = a, |RS| = a + d, and |SZ| = a + 2d, where a and d are positive constants. a is not equal to 4. Find one possible value of a (a ≠ 4), and the corresponding value of d.',
  ['One variable written in terms of the other'])
circle='The equation of the circle s is x² + y² − 4x + 2y − 20 = 0.'
A('6-a-i','Q6(a)(i)','5C',[36],[14],'2-2','co-ordinate-geometry-of-the-circle',
  'Write down the co-ordinates of the centre of s and the radius of s.',
  ['Work towards finding the centre or radius','Centre or radius correct'],stem=circle)
A('6-a-ii','Q6(a)(ii)','10D',[36],[14],'2-2','co-ordinate-geometry-of-the-circle',
  'The equation of the circle t is (x + 14)² + (y − 11)² = 225. Show that the circles s and t touch externally.',
  ['Radius and/or centre of circle t found','Some correct substitution into distance formula','Incorrect or no conclusion'],stem=circle)
square='The circle k has centre (0, 0) and radius 2 units. The point A(−2, 0) is on the circle k. ABCD is a square. The point C is on the x-axis, and BC and CD are tangents to k, as shown. h is the perpendicular distance from (0, 0) to AD.'
A('6-b-i','Q6(b)(i)','5B',[36],[15],'2-1','geometry,trigonometry-triangles',
  'Find the value of h. Give your answer in the form √a, where a ∈ ℕ.',
  ['Apply a * for incorrect format'],stem=square)
A('6-b-ii','Q6(b)(ii)','10C',[36],[15],'3-4','geometry,area-volume',
  'Find the area of the square ABCD. Give your answer in the form p + q√2 square units, where p, q ∈ ℕ.',
  ['Length of the side of the square found'],stem=square)
spiral='The first 16 triangles in a sequence of right-angled triangles are shown in the diagram. The first triangle in the sequence has sides of length 1, 1, and √2. The base line of any other triangle in the sequence is the hypotenuse of the previous triangle in the sequence. The perpendicular height of each triangle is always 1 unit.'
A('7-a','Q7(a)','10C',[37],[16],'2-1','geometry-constructions-proofs',
  'The first four triangles in the sequence are shown on the co-ordinate axes below. Construct the next triangle in the sequence on the diagram below. Show clearly all your construction lines. If you make any measurements, write them in an appropriate place on the diagram.',
  ['90° angle correct or 1 unit correct','90° angle correct and 1 unit correct'],stem=spiral)
A('7-b-i','Q7(b)(i)','10C',[37],[16,17],'2-3','trigonometry-triangles',
  'The diagram on the right shows the first two triangles in the sequence. The angles A and B, and the point C, are marked on the diagram. Find, in degrees, the sizes of the angles A and B, and the size of the angle A + B. Give your second and third answers correct to 2 decimal places.',
  ['1 correct angle','2 correct angles'],stem=spiral)
A('7-b-ii','Q7(b)(ii)','5C',[37],[16,17],'2-3','trigonometry-triangles,co-ordinate-geometry-of-the-line',
  'Hence, or otherwise, find the y co-ordinate of the point C, correct to 2 decimal places.',
  ['Finds the x co-ordinate'],stem=spiral+' The diagram shows the first two triangles, with angles A and B and the point C marked.')
A('7-c','Q7(c)','5B',[37],[16,18],'2-1','geometry',
  'Are any two triangles in the sequence similar? Justify your answer. Answer Yes or No.',
  ['Correct answer (No) given'],stem=spiral)
A('7-d','Q7(d)','5B',[37],[16,18],'2-1','geometry,sequences-series',
  'The kth triangle in the sequence has a hypotenuse of length 5√41, where k ∈ ℕ. Find the value of k.',
  ['√1025 found'],stem=spiral)
A('7-e','Q7(e)','15D',[38],[16,19],'2-3','trigonometry-functions-identities,trigonometry-triangles',
  'Two consecutive triangles in the sequence have hypotenuses of length √26 and √27, respectively, as shown in the diagram below. Two of the angles in the diagram are marked X and Y. Find the value of sin(X + Y), without using a calculator. Show all of your working out. Give your answer in the form (r + √t)/√u where r, t, u ∈ ℕ.',
  ['1 step correct','3 steps correct','Apply a * for incorrect format'],stem=spiral)
field='Michelle has a field in the shape of a quadrilateral ABCD. |AC| = 73 m, |AD| = 41 m, |DC| = 58 m, |∠CAB| = 36°, and |∠CBA| = 81°. |∠CDA| = θ and |BC| = x.'
A('8-a-i','Q8(a)(i)','10C',[39],[20],'2-3','trigonometry-triangles',
  'Use the triangle ABC to find the value of x, correct to 1 decimal place.',
  ['Fully substituted sine rule formula'],stem=field)
A('8-a-ii','Q8(a)(ii)','10C',[39],[20,21],'2-3','trigonometry-triangles',
  'Find the value of θ, correct to 1 decimal place.',
  ['Fully substituted cosine rule formula','Apply a * for no or incorrect units'],stem=field)
A('8-a-iii','Q8(a)(iii)','10D',[39],[20,21],'3-4','trigonometry-triangles,area-volume',
  'Michelle is putting topsoil on the field. The topsoil will cover the whole field, and will have a uniform height of 20 cm. Work out the volume of topsoil that Michelle will need, to cover the whole field. Give your answer correct to the nearest m³.',
  ['2 steps correct','3 steps correct'],stem=field)
football='A company makes footballs of different sizes. The surface of one football is made up of 20 hexagons and 12 pentagons, each with sides of length L cm, where L ∈ ℝ. In cm², the area of each hexagon is given by (3√3/2)L² and the area of each pentagon is given by (L²/4)√(5(5 + 2√5)).'
A('8-b-i','Q8(b)(i)','5B',[39],[22],'3-4','area-volume',
  'Use these formulas to write the total surface area of this type of football in terms of L.',
  ['Total area of hexagons or pentagons found in terms of L'],stem=football)
A('8-b-ii','Q8(b)(ii)','10D',[40],[22],'3-4','area-volume',
  'When it is inflated, this football is in the shape of a sphere with a diameter of 22 cm. Use your answer to part (b)(i) to find the value of L, correct to 1 decimal place.',
  ['1 step correct','2 steps correct'],stem=football)
A('8-c','Q8(c)','5D',[40],[23],'3-4','area-volume,indices-and-logs',
  'Some of the other footballs that the company makes are in packaging that is in the shape of a cube. These come in two sizes: small and large. The surface area of a large cube is n times that of a small cube, where n ∈ ℝ. The volume of a large cube is k times that of a small cube, where k ∈ ℝ. Use this to write k in terms of n.',
  ['1 step correct','2 steps correct'])
voters='In a large constituency with rural and urban voters, only two candidates, Alayah and David, stood for election. After the election, a local radio phone-in show released the table below. It was based on all of the callers who phoned in. All of these callers had voted. For example, 10% of the callers are rural voters who voted for Alayah. The table gives 18% rural voters in total, 61·8% Alayah voters in total, and 100% overall.'
A('9-a-i','Q9(a)(i)','10C',[41],[24],'1-2','probability',
  'Complete the table.',
  ['1 correct new entry','3 correct new entries'],stem=voters)
A('9-a-ii','Q9(a)(ii)','5B',[41],[24],'1-2','probability',
  'A caller is selected at random. Find the probability that this caller voted for David or is an urban voter.',
  ['P(D) or P(A)'],stem=voters+' Use the data from the table.')
A('9-a-iii','Q9(a)(iii)','5C',[41],[24,25],'1-2','probability',
  'A caller is selected at random from the callers who voted for Alayah. Find the probability that the caller is an urban voter. Give your answer correct to 4 decimal places.',
  ['51.8 or 61.8'],stem=voters+' Use the data from the table.')
A('9-a-iv','Q9(a)(iv)','5D',[41],[24,25],'1-2','probability',
  'A caller is selected at random. Let P be the event that the caller voted for Alayah. Let Q be the event that the caller is an urban voter. Are the events P and Q independent? Use calculations to support your answer.',
  ['Effort at independent formula','P(P ∩ Q) = 0.518'],stem=voters+' Use the data from the table.')
A('9-b-i-ii','Q9(b)(i),Q9(b)(ii)','10D',[42],[26],'1-1','probability',
  '(i) How many different seating arrangements of the 9 friends are possible? (ii) Find the number of seating arrangements in which three of the friends – Máire, Jake, and Alex – are sitting together.',
  ['One part correct','One part correct and work of merit in the other part'],
  stem='A group of 9 friends are planning a trip abroad to an Ireland hockey match. They buy nine match tickets. All nine tickets are in the same row and the row has exactly nine seats.')
corners='In the match, Ireland take 6 penalty corners. The probability that Ireland score from a penalty corner is roughly 0·35. Assume that the outcome of each penalty corner is independent.'
A('9-c-i','Q9(c)(i)','10B',[42],[27],'1-3','probability',
  'Find the probability that Ireland score from none of the penalty corners in the match. Give your answer correct to 4 decimal places.',
  ['Work of merit, 0.65 written'],stem=corners)
A('9-c-ii','Q9(c)(ii)','5D',[42],[27],'1-3','probability',
  'The probability that Ireland score at least n of their penalty corners is 12%, correct to the nearest percent. Find the value of n ∈ ℕ. Show all your working out.',
  ['Probability of two results set up','Probability of three results set up'],stem=corners)
driving='Mark is analysing a large data set on driving times on the N22 from 2022. The time taken to drive from Killarney to Cork during this period was normally distributed. The mean was 78 minutes and the standard deviation was 6 minutes.'
A('10-a-i','Q10(a)(i)','10C',[43],[28],'1-3','statistics-z-scores',
  'Find the percentage of drivers who completed the journey in 82 minutes or less.',
  ['Some correct substitution into formula'],stem=driving,
  extra={'markingNote':'The printed high-partial note says 3 correct new entries, although this question contains no table. The published numeric awards are retained; no substitute official criterion is assumed.'})
A('10-a-ii','Q10(a)(ii)','10D',[43],[28],'1-3','statistics-z-scores',
  'Exactly 50% of the drivers took between 70 minutes and k minutes to complete the journey, where k ∈ ℝ. Find the value of k, correct to 1 decimal place.',
  ['Apply a * for no or incorrect rounding'],stem=driving,
  extra={'markingNote':'The printed partial-credit notes refer to two or three results, apparently carried over from another question. The original notes and numeric scale are retained without inventing replacement SEC criteria.'})
A('10-b','Q10(b)','10D',[43],[28,29],'1-7','statistics-inferential-statistics',
  'In 2023 major road works were completed on the N22 between Killarney and Cork. Afterwards, Mark decides to carry out a new survey to see if the driving times have changed. He randomly selects 500 drivers to participate in the survey. For this sample the mean driving time was 71 minutes. Mark assumes the population standard deviation is still 6 minutes. Carry out a hypothesis test at the 5% level of significance to see if there has been a change in driving times after the road improvements. State your null hypothesis and your alternative hypothesis, state your conclusion, and give a reason for your conclusion.',
  ['Work of merit in one step','Two steps correct','Three steps correct','award Mid Partial Credit at most'],stem=driving)
committee='A committee of 5 people is picked from a group of 10 people, consisting of 4 men and 6 women.'
A('10-c-i','Q10(c)(i)','10C',[44],[30],'1-1','probability',
  'Find the number of different committees which consist of 2 men and 3 women.',
  ['= 120'],stem=committee)
A('10-c-ii','Q10(c)(ii)','5C',[44],[30],'1-1','probability',
  'Find the number of different committees that have more women than men.',
  ['One possible outcome formulated','Two possible outcomes formulated'],stem=committee)
A('10-c-iii','Q10(c)(iii)','5C',[44],[30],'1-1','probability',
  'One committee is picked at random. A different committee is then picked at random. Find the probability that none of the 10 people are on both of these committees.',
  ['252 and stops'],stem=committee)

assert len(p.cards)==43
selection_review=[
 {'pages':[3,4,16],'wording':'any five / any three questions','classification':'exam-level-selection','reason':'Every question is retained for practice regardless of exam-level selection.'},
 {'pages':[4,6,17],'wording':'or otherwise','classification':'method-choice','reason':'Alternative methods for the same required task, with no expansion.'},
 {'pages':[12],'wording':'Diagram, Given, To Prove, Construction, Proof','classification':'required-headings','reason':'Five required headings within one 15-mark proof.'},
 {'pages':[13],'wording':'one possible value of a','classification':'open-answer','reason':'Freely chosen positive constants satisfying the ratios; not a finite choice pool.'},
 {'pages':[18],'wording':'Are any two triangles ... Answer (Yes or No)','classification':'answer-selection','reason':'One comparison and justification, not selection of triangles for separate answers.'},
 {'pages':[24,26,30],'wording':'David or urban / three friends / committees','classification':'mathematical-context','reason':'These describe event unions or counting constraints, not optional examination tasks.'},
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','Exam-level choice; all questions retained.')
 if 'otherwise' in t:return ('method-choice','Alternative methods for the same task.')
 if 'triangles' in t:return ('answer-selection','One yes/no decision with justification; no triangle-choice expansion.')
 if 'possible value' in t:return ('open-answer','One freely chosen valid value and its corresponding value; not a finite pool.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
