"""2015 HL Paper 2: all 35 tasks / 300 marks, with the three-component Q6(b)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *

RAW_ROWS = {
 '1-a': [(LPC,'At least one other correct entry'),(LPC,'Partially correct table with at least 5 correct totals or couples'),(HPC,'Five or more correct entries including at least one other loss and one other win'),(HPC,'Table correctly completed with totals or couples but no indication of W or L')],
 '1-b-i': [(LPC,'Favourable outcomes identified')],
 '1-c': [(LPC,'Relevant binomial formula with some substitution'),(LPC,'Listing at least any two of the ten throws'),(HPC,'Probability of two wins in nine throws')],
 '2-a': [(LPC,'Relevant formula with or without substitution')],
 '2-b': [(LPC,'One relevant step e.g. null hypothesis or alternative hypothesis stated'),(LPC,'Some work towards finding z'),(MPC,'z calculated'),(MPC,'Either null or alternative hypothesis stated and relevant work towards finding z'),(MPC,'Confidence interval from (a) and either null or alternative hypothesis stated'),(HPC,'Not accepting or rejecting hypothesis'),(HPC,'Incorrect conclusion for hypothesis')],
 '2-c': [(HPC,'p value correct'),(HPC,'Not contextualising answer correctly')],
 '3-a': [(MPC,'Both slopes found'),(HPC,'Slopes linked to perpendicularity')],
 '3-b': [(LPC,'Relevant formula with some correct substitution'),(HPC,'Substitution into formula fully correct')],
 '3-c-i': [(LPC,'Relevant formula with some correct substitution'),(MPC,'One value for k found'),(MPC,'Work indicating two values for k'),(HPC,'Both values of k'),(HPC,'Positive value for k evaluated and distance calculated')],
 '4-a': [(PC,'Centre or radius')],
 '4-b-i': [(LPC,'Formula for ratio with some correct substitution'),(LPC,'Effort at setting up translation'),(HPC,'Substitution into ratio formula fully correct'),(HPC,'One ordinate only found'),(HPC,'Correct answer without supporting work')],
 '4-b-ii': [(LPC,'Identifies centre'),(LPC,'Identifies radius'),(HPC,'Equation of circle formed but error in substitution')],
 '4-c': [(LPC,'Slope AB or slope of tangent'),(LPC,'Some correct substitution into relevant formula'),(HPC,'Equation of line fully substituted')],
 '5-a': [(LPC,'Tan function in terms of Sine and Cosine'),(MPC,'sin (A+B) or cos (A+B) expanded'),(MPC,'Numerator or denominator in fraction form (method 2)'),(HPC,'Numerator and denominator divided by cosA.cosB (Method 1)'),(HPC,'Both numerator and denominator expressed in form of a single fraction (Method 2)')],
 '5-b': [(LPC,'One value for 3x'),(MPC,'One value for x'),(MPC,'Two or more values for 3x'),(HPC,'Three or more values for x')],
 '6-a': [(LPC,'Some relevant calculation'),(LPC,'One side bisected'),(LPC,'One midpoint indicated'),(HPC,'One median drawn')],
 '6-b': [('Diagram and Given, '+PC,'Effort at Diagram or Given'),('Construction, '+PC,'Construction attempted (diagram and/or description)'),('Proof, '+LPC,'More than one critical step omitted but still some substantial work of merit'),('Proof, '+HPC,'Proof completed with one critical step omitted')],
 '7-a': [(LPC,'BT drawn correctly'),(LPC,'Pythagoras formula with some correct substitution'),(HPC,'Pythagoras formula fully substituted')],
 '7-b': [(LPC,'Indicates two areas'),(LPC,'Effort at area of rectangle only'),(LPC,'Effort at area of triangle only'),(HPC,'Area of triangle correct'),(HPC,'Area of rectangle correct')],
 # Here the text layer breaks every equation into isolated glyphs. Quote the
 # printed band heading; the complete band and solution are in the verified crop.
 '7-c-i': [(NOTE,'Scale 5C (0, 2, 4, 5)')],
 '7-c-ii': [(SOL,'Area large sector HAP + 2 area HABK + area sector KBQ'),(LPC,'Effort at area of one region'),(MPC,'Area of one sector with correct substitution'),(HPC,'Area of two sectors with substitution correct in both.')],
 '8-a': [(LPC,'One correct probability'),(HPC,'Identifies all three probabilities correctly'),(HPC,'Three probabilities multiplied of which two are correct')],
 '8-b': [(LPC,'One correct probability'),(HPC,'Identifies all three probabilities correctly'),(HPC,'Three probabilities multiplied of which two are correct')],
 '8-c': [(LPC,'Lists one new way'),(MPC,'Full listing only'),(MPC,'One new probability'),(HPC,'Sum of three probabilities'),(HPC,'Identifies all four probabilities correctly')],
 '8-d-i': [(LPC,'Indicates P(S, S) and/or P(U, S) or equivalent')],
 '8-d-ii': [(PC,'Partial substitution into equation')],
 '8-e-i': [(NOTE,'Scale 5C (0, 2, 4, 5)')],
 '8-e-ii': [(NOTE,'Scale 5C (0, 2, 4, 5)')],
 '8-f-i': [(SOL,'Events not independent'),(PC,'(i) correct only or (ii) correct only')],
 '9-a': [(LPC,'Effort at expressing sine function in terms of 15 and 150'),(LPC,'Finds third side of triangle and makes effort to find an angle'),(HPC,'Half angle found')],
 '9-b': [(LPC,'Cosine Rule with some correct substitution'),(LPC,'Effort at calculating AX or TX'),(HPC,'Cosine Rule substituted correctly'),(HPC,'Finds AX and formulates for TX (or vice versa)')],
 '9-c-i': [(PC,'t = 0 indicated'),(NOTE,'Accept h = 8 m without work')],
 '9-c-ii': [(LPC,'h = 0 indicated'),(HPC,'OB found for positive value for t')],
 '9-d-i': [(NOTE,'Scale 5B (0, 2, 5)')],
 '9-d-ii': [(SOL,'h = 10 m'),(LPC,'Pythagoras with some correct substitution.'),(LPC,'Effort at evaluating θ'),(MPC,'Pythagoras correctly substituted'),(HPC,'Quadratic equation expanded correctly')],
}
ROWS = {'maths-2015-hl-p2-q'+key: [L(label,text) for label,text in rows] for key,rows in RAW_ROWS.items()}
if len(sys.argv)>1: quotes(ROWS,sys.argv[1]); raise SystemExit

# Scheme keys are filled after the generated crops have been visually checked.
SCHEME_ROW_FIGURES = {'maths-2015-hl-p2-q1-a': 'maths-2015-HL-scheme-p037-i0', 'maths-2015-hl-p2-q1-b-i': 'maths-2015-HL-scheme-p037-i1', 'maths-2015-hl-p2-q1-c': 'maths-2015-HL-scheme-p037-i2', 'maths-2015-hl-p2-q2-a': 'maths-2015-HL-scheme-p038-i0', 'maths-2015-hl-p2-q2-b': 'maths-2015-HL-scheme-p038-i1', 'maths-2015-hl-p2-q2-c': 'maths-2015-HL-scheme-p039-i0', 'maths-2015-hl-p2-q3-a': 'maths-2015-HL-scheme-p040-i0', 'maths-2015-hl-p2-q3-b': 'maths-2015-HL-scheme-p040-i1', 'maths-2015-hl-p2-q3-c-i': 'maths-2015-HL-scheme-p040-i2', 'maths-2015-hl-p2-q4-a': 'maths-2015-HL-scheme-p041-i0', 'maths-2015-hl-p2-q4-b-i': 'maths-2015-HL-scheme-p041-i1', 'maths-2015-hl-p2-q4-b-ii': 'maths-2015-HL-scheme-p041-i2', 'maths-2015-hl-p2-q4-c': 'maths-2015-HL-scheme-p041-i3', 'maths-2015-hl-p2-q5-a': 'maths-2015-HL-scheme-p042-i0', 'maths-2015-hl-p2-q5-b': 'maths-2015-HL-scheme-p042-i1', 'maths-2015-hl-p2-q6-a': 'maths-2015-HL-scheme-p043-i0', 'maths-2015-hl-p2-q6-b': 'maths-2015-HL-scheme-p044-i0', 'maths-2015-hl-p2-q7-a': 'maths-2015-HL-scheme-p045-i0', 'maths-2015-hl-p2-q7-b': 'maths-2015-HL-scheme-p046-i0', 'maths-2015-hl-p2-q7-c-i': 'maths-2015-HL-scheme-p046-i1', 'maths-2015-hl-p2-q7-c-ii': 'maths-2015-HL-scheme-p046-i2', 'maths-2015-hl-p2-q8-a': 'maths-2015-HL-scheme-p047-i0', 'maths-2015-hl-p2-q8-b': 'maths-2015-HL-scheme-p047-i1', 'maths-2015-hl-p2-q8-c': 'maths-2015-HL-scheme-p047-i2', 'maths-2015-hl-p2-q8-d-i': 'maths-2015-HL-scheme-p048-i0', 'maths-2015-hl-p2-q8-d-ii': 'maths-2015-HL-scheme-p048-i1', 'maths-2015-hl-p2-q8-e-i': 'maths-2015-HL-scheme-p048-i2', 'maths-2015-hl-p2-q8-e-ii': 'maths-2015-HL-scheme-p049-i0', 'maths-2015-hl-p2-q8-f-i': 'maths-2015-HL-scheme-p049-i1', 'maths-2015-hl-p2-q9-a': 'maths-2015-HL-scheme-p050-i0', 'maths-2015-hl-p2-q9-b': 'maths-2015-HL-scheme-p050-i1', 'maths-2015-hl-p2-q9-c-i': 'maths-2015-HL-scheme-p052-i0', 'maths-2015-hl-p2-q9-c-ii': 'maths-2015-HL-scheme-p052-i1', 'maths-2015-hl-p2-q9-d-i': 'maths-2015-HL-scheme-p053-i0', 'maths-2015-hl-p2-q9-d-ii': 'maths-2015-HL-scheme-p053-i1'}
p = Paper(2015,'hl','p2', {'5B':[0,2,5],'5C':[0,2,4,5],'5D':[0,2,3,4,5],
    '10B':[0,5,10],'10C':[0,4,8,10],'10D':[0,2,5,8,10],'15C':[0,5,12,15],'15D':[0,4,7,11,15]},
    'LC003ALP200EV.pdf','LC003ALP000EV.pdf',reviewed_at='2026-10-29')
A=p.A
prob='probability'; stat='statistics-inferential-statistics'; line='co-ordinate-geometry-of-the-line'; circle='co-ordinate-geometry-of-the-circle'; trig='trigonometry-triangles'; ident='trigonometry-functions-identities'; geo='geometry-constructions-proofs'; seq='sequences-series'
dice='An experiment consists of throwing two fair, standard, six-sided dice and noting the sum of the two numbers thrown. If the sum is 9 or greater it is recorded as a “win” (W). If the sum is 8 or less it is recorded as a “loss” (L).'
A('1-a','Q1(a)','10C',[37,56],[3],'1-2',prob,'Complete the table below to show all possible outcomes of the experiment.',stem=dice)
A('1-b-i','Q1(b)(i),Q1(b)(ii)','10C',[37,56],[3],'1-2',prob,'(i) Find the probability of a win on one throw of the two dice. (ii) Find the probability that each of 3 successive throws of the two dice results in a loss. Give your answer correct to four decimal places.',stem=dice)
A('1-c','Q1(c)','5C',[37,56],[3],'1-2',prob,'The experiment is repeated until a total of 3 wins occur. Find the probability that the third win occurs on the tenth throw of the two dice. Give your answer correct to four decimal places.',stem=dice)
shop='A survey of 100 shoppers, randomly selected from a large number of Saturday supermarket shoppers, showed that the mean shopping spend was €90·45. The standard deviation of this sample was €20·73.'
q2a='Find a 95% confidence interval for the mean amount spent in a supermarket on that Saturday.'
q2b='A supermarket has claimed that the mean amount spent by shoppers on a Saturday is €94. Based on the survey, test the supermarket’s claim using a 5% level of significance. Clearly state your null hypothesis, your alternative hypothesis, and your conclusion.'
A('2-a','Q2(a)','10C',[38,57],[4],'1-7',stat,q2a,stem=shop)
A('2-b','Q2(b)','10D',[38,57],[4],'1-7',stat,q2b,stem=shop+' Part (a): '+q2a)
A('2-c','Q2(c)','5C',[39,57],[4],'1-7',stat,'Find the p-value of the test you performed in part (b) above and explain what this value represents in the context of the question.',stem=shop+' Part (b): '+q2b)
l1='The line l₁ is 3x − 4y − 12 = 0.'
A('3-a','Q3(a)','10D',[40,58],[5],'2-2',line,'The co-ordinates of two points are A(4, −1) and B(7, t). The line l₁: 3x − 4y − 12 = 0 is perpendicular to AB. Find the value of t.')
A('3-b','Q3(b)','10C',[40,58],[5],'2-2',line,'Find, in terms of k, the distance between the point P(10, k) and l₁.',stem=l1)
A('3-c-i','Q3(c)(i),Q3(c)(ii)','5D',[40,58],[5],'2-2',line,'P(10, k) is on a bisector of the angles between the lines l₁ and l₂: 5x + 12y − 20 = 0. (i) Find the possible values of k. (ii) If k > 0, find the distance from P to l₁.',stem=l1)
circles='Two circles s and c touch internally at B, as shown. The equation of the circle s is (x − 1)² + (y + 6)² = 360.'
small='The point K is the centre of circle c. The radius of c is one-third the radius of s. The co-ordinates of B are (7, 12).'
A('4-a','Q4(a)','5B',[41,59],[6],'2-2',circle,'Write down the co-ordinates of the centre of s. Write down the radius of s in the form a√10, where a ∈ ℕ.',stem=circles)
A('4-b-i','Q4(b)(i)','5C',[41,59],[6],'2-2',circle,'Find the co-ordinates of K.',stem=circles+' '+small)
A('4-b-ii','Q4(b)(ii)','10C',[41,59],[6],'2-2',circle,'Find the equation of c.',stem=circles+' '+small+' Part (b)(i): Find the co-ordinates of K.')
A('4-c','Q4(c)','5C',[41,59],[6],'2-2',circle+','+line,'Find the equation of the common tangent at B. Give your answer in the form ax + by + c = 0, where a, b, c ∈ ℤ.',stem=circles+' '+small)
A('5-a','Q5(a)','15D',[42,60],[7],'2-3',ident,'Prove that tan(A + B) = (tan A + tan B)/(1 − tan A tan B).')
A('5-b','Q5(b)','10D',[42,60],[7],'2-3',ident,'Find all the values of x for which sin(3x) = √3/2, 0 ≤ x ≤ 360, x in degrees.')
A('6-a','Q6(a)','5C',[43,60],[8],'2-1',geo,'Construct the centroid of the triangle ABC below. Show all construction lines. (Where measurement is used, show all relevant measurements and calculations clearly.)',extra={'measurementRequired':True})
p.C('6-b','Q6(b)',[{'id':'diagram-given','label':'Diagram / Given','code':'5B'},{'id':'construction','label':'Construction','code':'5B'},{'id':'proof','label':'Proof','code':'10C'}],[44,60],[9],'2-1',geo,
 'Prove that, if three parallel lines cut off equal segments on some transversal line, then they will cut off equal segments on any other transversal line. Complete the sections: Diagram; Given; To Prove; Construction; Proof.')
machine='A flat machine part consists of two circular ends attached to a plate, as shown (diagram not to scale). The sides of the plate, HK and PQ, are tangential to each circle. The larger circle has centre A and radius 4r cm. The smaller circle has centre B and radius r cm. The length of [HK] is 8r cm and |AB| = 20√73 cm.'
q7a='Find r, the radius of the smaller circle. (Hint: Draw BT ∥ KH, T ∈ AH.)'
q7b='Find the area of the quadrilateral ABKH.'
q7c='Find |∠HAP|, in degrees, correct to one decimal place.'
A('7-a','Q7(a)','15C',[45,61],[10],'2-3',trig,q7a,stem=machine)
A('7-b','Q7(b)','15C',[46,61],[10,11],'3-4','area-volume',q7b,stem=machine+' Part (a): '+q7a)
A('7-c-i','Q7(c)(i)','5C',[46,61],[10,11],'2-3',trig,q7c,stem=machine+' Part (a): '+q7a)
A('7-c-ii','Q7(c)(ii)','5D',[46,61],[10,11],'3-4','area-volume,'+trig,'Find the area of the machine part, correct to the nearest cm².',stem=machine+' Part (a): '+q7a+' Part (b): '+q7b+' Part (c)(i): '+q7c)
ball='In basketball, players often have to take free throws. When Michael takes his first free throw in any game, the probability that he is successful is 0·7. For all subsequent free throws in the game, the probability that he is successful is: 0·8 if he has been successful on the previous throw; 0·6 if he has been unsuccessful on the previous throw.'
pn='Let pₙ be the probability that Michael is successful with his nth free throw in the game (and hence (1 − pₙ) is the probability that Michael is unsuccessful with his nth free throw).'
rec='Part (d)(i): Show that pₙ₊₁ = 0·6 + 0·2pₙ.'
an='For all positive integers n, let aₙ = p − pₙ, where p = 0·75 as above.'
georatio='Use the ratio aₙ₊₁/aₙ to show that aₙ is a geometric sequence with common ratio 1/5.'
A('8-a','Q8(a)','10C',[47,62],[12],'1-2',prob,'Find the probability that Michael is successful (S) with all three of his first three free throws in a game.',stem=ball)
A('8-b','Q8(b)','10C',[47,62],[12],'1-2',prob,'Find the probability that Michael is unsuccessful (U) with his first two free throws and successful with the third.',stem=ball)
A('8-c','Q8(c)','15D',[47,62],[12],'1-2',prob,'List all the ways that Michael could be successful with his third free throw in a game and hence find the probability that Michael is successful with his third free throw.',stem=ball)
A('8-d-i','Q8(d)(i)','5C',[48,62],[12,13],'1-2',prob,'Show that pₙ₊₁ = 0·6 + 0·2pₙ.',stem=ball+' '+pn)
A('8-d-ii','Q8(d)(ii)','10B',[48,62],[12,13],'1-2',prob,'Assume that p is Michael’s success rate in the long run; that is, for large values of n, we have pₙ₊₁ ≈ pₙ ≈ p. Using the result from part (d)(i) above, or otherwise, show that p = 0·75.',stem=ball+' '+pn+' '+rec)
A('8-e-i','Q8(e)(i)','5C',[48,62],[12,13],'4-1',seq+','+prob,georatio,stem=ball+' '+pn+' '+rec+' '+an)
A('8-e-ii','Q8(e)(ii)','5C',[49,63],[12,13,14],'4-1',seq+','+prob,'Find the smallest value of n for which p − pₙ < 0·00001.',stem=ball+' '+pn+' '+rec+' '+an+' Part (e)(i): '+georatio)
A('8-f-i','Q8(f)(i),Q8(f)(ii)','5B',[49,63],[12,14],'1-2',prob,'(i) Based on this knowledge, what is your estimate of the probability that Michael will be successful with his next free throw in the game? (ii) Why would it not be appropriate to consider Michael’s subsequent free throws in the game as a sequence of Bernoulli trials?',stem=ball+' You arrive at a game in which Michael is playing. You know that he has already taken many free throws, but you do not know what pattern of success he has had.')
A('9-a','Q9(a)','10C',[50,63],[15],'2-3',trig,'Joan is playing golf. She is 150 m from the centre of a circular green of diameter 30 m. The diagram shows the range of directions in which Joan can hit the ball so that it could land on the green. Find α, the measure of the angle of this range of directions. Give your answer, in degrees, correct to one decimal place.')
A('9-b','Q9(b)','10C',[50,51,63],[15],'2-3',trig,'At the next hole, Joan, at T, attempts to hit the ball in the direction of the hole H. Her shot is off target and the ball lands at A, a distance of 190 metres from T, where |∠ATH| = 18°. |TH| is 385 metres. Find |AH|, the distance from the ball to the hole, correct to the nearest metre.')
golf='At another hole, where the ground is not level, Joan hits the ball from K, as shown. The ball lands at B. The height of the ball, in metres, above the horizontal line OB is given by h = −6t² + 22t + 8, where t is the time in seconds after the ball is struck and h is the height of the ball.'
A('9-c-i','Q9(c)(i)','5B',[52,63],[16],'5-1','functions','Find the height of K above OB.',stem=golf)
A('9-c-ii','Q9(c)(ii)','10C',[52,63],[16],'2-3',trig+',algebra-solving-equations','The horizontal speed of the ball over the straight distance [OB] is a constant 38 m s⁻¹. Find the angle of elevation of K from B, correct to the nearest degree.',stem=golf+' Part (c)(i): Find the height of K above OB.')
tree='At a later hole, Joan’s first shot lands at the point G, on ground that is sloping downwards, as shown. A vertical tree, [CE], 25 metres high, stands between G and the hole. The distance, |GC|, from the ball to the bottom of the tree is also 25 metres. The angle of elevation at G to the top of the tree, E, is θ, where θ = tan⁻¹(1/2). The height of the top of the tree above the horizontal, GD, is h metres and |GD| = d metres.'
A('9-d-i','Q9(d)(i)','5B',[53,63],[17],'2-3',trig,'Write d and |CD| in terms of h.',stem=tree)
A('9-d-ii','Q9(d)(ii)','5D',[53,64],[17],'2-3',trig+',algebra-solving-equations','Hence, or otherwise, find h.',stem=tree+' Part (d)(i): Write d and |CD| in terms of h.')
marks={'1':25,'2':25,'3':25,'4':25,'5':25,'6':25,'7':40,'8':65,'9':45}
p.check(marks,35)
p.review(marks,
 'Independent visual reading of all 20 question PDF pages and combined-scheme PDF pages 35–68. Every printed task checked against model solutions (37–53), the scale table/general notes (54), allocation summary (55) and detailed marking notes (56–64).',
 list(range(35,69)),[54,55],
 ['All nine questions are required, totalling 300 marks. All 35 tasks are retained. The question booklet has 19 numbered pages plus its back cover.',
  'Q1(b)(i)+(ii), Q3(c)(i)+(ii) and Q8(f)(i)+(ii) each share one published scale and are one card. Q6(b) is one proof worth 20 marks, assessed by Diagram/Given 5B, Construction 5B and Proof 10C; preserve all three scales within the one task. The general minor-error deduction is applied only once per printed part.',
  'Paper 2 uses 15C [0,5,12,15], unlike Paper 1. Other bands: 5B [0,2,5], 5C [0,2,4,5], 5D [0,2,3,4,5], 10B [0,5,10], 10C [0,4,8,10], 10D [0,2,5,8,10], 15D [0,4,7,11,15].',
  'All 35 cards are new. Typeset model solutions and detailed credit notes are combined in solution crops revealed only after the student answers. Prose quotes preserve source wording. Where equation objects extract as disconnected glyphs (Q7(c)(i), Q8(e)(i)/(ii), Q9(d)(i)), the quote identifies the scale while the verified crop carries the complete solution and credit notes.',
  'Q6(a) preserves original geometry and measurement access. Q7 retains the machine diagram in every dependent task; Q8 retains conditional probabilities and definitions; Q9 retains each relevant golf diagram. Source references use PDF positions; scheme printed page numbers are two less.'],
 [{'pages':[2,3,10],'wording':'Answer all nine / all six / all three questions','classification':'all-questions-required','reason':'Every question is required and retained.'},
  {'pages':[13,17],'wording':'or otherwise','classification':'method-choice','reason':'Alternative methods of the same task, not a choice of questions.'},
  {'pages':[3,7,8,12,13],'wording':'all possible outcomes / all values / all construction lines / all the ways / all positive integers','classification':'all-items-required','reason':'Required exhaustive work or mathematical domain, not a choose-k pool.'}],
 lambda t: ('all-questions-required','Every printed question is required and retained.') if 'Answer all' in t else ('method-choice','Alternative methods for the same task.') if 'otherwise' in t else ('all-items-required','Required exhaustive work or mathematical domain, not a printed choice pool.'))
p.apply(ROWS,'2015 Higher Level Paper 2',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
