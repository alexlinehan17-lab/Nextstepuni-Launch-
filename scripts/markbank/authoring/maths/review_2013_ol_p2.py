"""2013 Ordinary Project Maths Phase 2 Paper 2, independently reviewed against both original booklets."""
import os,sys
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R={'1-a': ['Partial Credit — States one or two players throw more heads than tails.',
         'Partial Credit — Gives an indication that 109 > 100 or 238 > 200.'],
 '1-b': ['Low Partial Credit — Finds the correct total number of heads or throws.',
         'Low Partial Credit — Calculates the correct probability for one player.',
         'High Partial Credit — Finds the total number of heads and throws.',
         'High Partial Credit — Calculates the probability using the totals but one element of the fraction incorrect.',
         'High Partial Credit — Calculates the correct probability for each of the three players individually.'],
 '1-c': ['Low Partial Credit — Writes the correct probability for three heads or two tails.',
         'Low Partial Credit — Calculates the correct probability for three heads and two tails using a fair coin.',
         'High Partial Credit — Calculates the correct probability for three heads and two tails but with an incorrect or '
         'omitted statement.',
         'High Partial Credit — Fully correct answer using a fair coin.'],
 '2-a-i': ['Low Partial Credit — Relevant work in one section e.g. states two green sectors or gives GGG as a possible outcome.',
           'High Partial Credit — One section correct.',
           'High Partial Credit — Substantially correct work in both sections.'],
 '2-b': ['Note — Accept answers consistent with candidate’s answers listed in (a)(ii).',
         'Low Partial Credit — One correct or consistent outcome written.',
         'High Partial Credit — One correct outcome for each category.',
         'High Partial Credit — At least five outcomes in total from a(ii).'],
 '2-c': ['Low Partial Credit — A correct response without an explanation of some merit.',
         'Low Partial Credit — An incorrect response but some merit in the explanation.',
         'High Partial Credit — A correct response with one aspect of the explanation correct.',
         'High Partial Credit — An incorrect response with a correct explanation.'],
 '3-a': ['Low Partial Credit — Writes y = mx + c and stops.',
         'Low Partial Credit — Writes a relevant slope formula and stops.',
         'Low Partial Credit — Some correct work at transposing terms.',
         'Low Partial Credit — Finds one or two points on l.',
         'High Partial Credit — Equation of the line written in the form y = mx + c but slope not identified.',
         'High Partial Credit — Finds the slope of l using two points, one of which is incorrect.',
         'Note — A correct answer without work shown, award full credit.'],
 '3-b': ['Low Partial Credit — Identifies correct relevant formula, e.g. writes y − y₁ = m(x − x₁) and stops.',
         'Low Partial Credit — Writes correct or consistent slope for k.',
         'Low Partial Credit — Some correct work with (7, 0).',
         'High Partial Credit — Substitution into the line equation with one error.',
         'Note — A correct answer without work shown, award full credit.'],
 '3-c': ['Low Partial Credit — Relevant work towards equating coefficients in both equations.',
         'Low Partial Credit — Relevant work towards substituting for one variable using the other equation.',
         'Low Partial Credit — One line correctly graphed.',
         'High Partial Credit — One correct or consistent co-ordinate found.',
         'High Partial Credit — One or two algebraic errors leading to an incorrect point of intersection.',
         'High Partial Credit — A correct structure to the solution with up to two errors.',
         'High Partial Credit — A correct answer, obtained graphically.'],
 '4-a': ['Low Partial Credit — Writes a correct distance formula or formula for the equation of the circle.',
         'High Partial Credit — Calculates the distance O to A.',
         'High Partial Credit — Substitutes into correct circle formula with one error.',
         'High Partial Credit — Calculates r² incorrectly.',
         'Note — A correct answer without work shown, award full credit.'],
 '4-b': ['Low Partial Credit — Writes a correct midpoint formula or formula for the equation of the circle.',
         'Low Partial Credit — Writes the midpoint or radius correctly.',
         'Mid Partial Credit — Writes the midpoint and radius correctly.',
         'Mid Partial Credit — Substitutes the centre or radius into the equation.',
         'High Partial Credit — Substitutes the centre and radius into the equation.',
         'High Partial Credit — Substitutes into correct circle formula with one error.',
         'High Partial Credit — Calculates r² incorrectly.'],
 '4-c': ['Low Partial Credit — Identifies that y = 0.',
         'Low Partial Credit — Some relevant substitution into the equation.',
         'Low Partial Credit — Correct answer without work shown.',
         'High Partial Credit — Substantially correct work at solving for x, e.g. works incorrectly with (x − 4)² = 16.',
         'High Partial Credit — Correct answer without the co-ordinates of P identified.',
         'Note — A correct answer with a correct geometrical explanation, award full credit.'],
 '5-a': ['Low Partial Credit — A rectangle or a circle drawn.',
         'Low Partial Credit — The length of the circle calculated.',
         'High Partial Credit — A correct sketch drawn without dimensions.',
         'High Partial Credit — A partially complete sketch drawn with some dimensions given.'],
 '5-b': ['Low Partial Credit — Correct formula for the volume of a cylinder written and stops.',
         'Low Partial Credit — An incorrect relevant formula and some correct substitution.',
         'High Partial Credit — Formula substituted correctly without calculation or with incorrect calculation.',
         'High Partial Credit — Some incorrect substitution into formula with correct calculation.',
         'High Partial Credit — Correct answer not expressed in terms of π.',
         'Note — A correct answer without work shown, award full credit.'],
 '5-c': ['Low Partial Credit — Writes correct formula for the volume or surface area of a sphere.',
         'Low Partial Credit — Equates volume of cylinder with surface area of sphere.',
         'Mid Partial Credit — Equates volume of cylinder with volume of sphere.',
         'Mid Partial Credit — Equates volume of cylinder with surface area of sphere and correctly calculates r.',
         'High Partial Credit — Calculates the radius of the sphere.',
         'High Partial Credit — Calculates correctly an incorrect surface area.',
         'High Partial Credit — Calculates the correct surface area with an incorrect radius.',
         'High Partial Credit — Correct answer not expressed in terms of π.'],
 '6a-a': ['Low Partial Credit — Point B or C correctly marked on the given line.',
          'Low Partial Credit — One arc drawn for a point not on the line.',
          'Low Partial Credit — Freehand triangle drawn with dimensions.',
          'High Partial Credit — Point B found and one arc for C drawn.',
          'High Partial Credit — Correct triangle drawn but construction lines not shown.',
          'High Partial Credit — Points B and C constructed but sides not drawn.',
          'High Partial Credit — Triangle constructed correctly but measurements not exact.'],
 '6a-b': ['Low Partial Credit — Freehand image drawn.',
          'Low Partial Credit — Relevant work at constructing the image of C.',
          'High Partial Credit — Correct triangle drawn but construction lines not shown.'],
 '6a-c': ['Partial Credit — Some correct element in the candidate’s justification or an incomplete justification.'],
 '6b': ['Low Partial Credit — Relevant work with the angle sum in one triangle.',
        'Low Partial Credit — Correct identification of vertically opposite angles being equal.',
        'Mid Partial Credit — Similar work with two relevant triangles.',
        'High Partial Credit — A correct answer other than one step omitted or incorrect.'],
 '7-a': ['Low Partial Credit — A correct element of the plot entered.',
         'Low Partial Credit — Key given without entering any elements.',
         'Mid Partial Credit — One side of the plot correct without the key.',
         'Mid Partial Credit — Ten elements on each side correct, without the key.',
         'Mid Partial Credit — Ten elements in total correct, with the correct key.',
         'High Partial Credit — A correct plot without the key.',
         'High Partial Credit — A plot with five or less elements incorrect with the correct key.',
         'High Partial Credit — Correct plot and key but data not ordered.'],
 '7-b': ['Partial Credit — A correct but incomplete difference given.'],
 '7-c': ['Low Partial Credit — Describes the median or interquartile range.',
         'Low Partial Credit — Relevant work towards finding the median or the interquartile range.',
         'Low Partial Credit — Writes the range of the marriage rate.',
         'High Partial Credit — One correct answer.',
         'High Partial Credit — Substantially correct work in each part.',
         'High Partial Credit — Correct answers using the data for the birth rate or the death rate.'],
 '7-d-i': ['Low Partial Credit — Writes the formula for the mean.',
           'Low Partial Credit — Finds the value of n or adds some of the elements.',
           'High Partial Credit — Correct substitution into the formula without calculation.',
           'High Partial Credit — Incorrect substitution into the formula with calculation.',
           'Note — A correct answer without work shown, award full credit.',
           'Note — Accept 78 in this context.'],
 '7-d-ii': ['Low Partial Credit — Finds one correct boundary.',
            'High Partial Credit — Finds both correct boundaries without elements listed.',
            'High Partial Credit — Finds one correct boundary with the correct elements.'],
 '7-e': ['Low Partial Credit — Identifies 165 as the birth rate or recognises the rate is per 10 000.',
         'High Partial Credit — Correct fraction without calculation.',
         'High Partial Credit — Fraction with one element incorrect, correctly calculated.'],
 '7-f': ['Low Partial Credit — Identifies 61 as the death rate.',
         'Low Partial Credit — Carries forward the answer from (e).',
         'High Partial Credit — Correct fraction without calculation.',
         'High Partial Credit — Fraction with one element incorrect, correctly calculated.'],
 '7-g': ['Partial Credit — A plausible reason with some relevant reference to the data.'],
 '7-h': ['Low Partial Credit — One correct ratio found.',
         'Low Partial Credit — A prediction with some merit.',
         'Low Partial Credit — Two correct ratios based on years rather than events.',
         'High Partial Credit — Two correct ratios found and a prediction or a reason.',
         'High Partial Credit — One correct ratio with some merit in the prediction and reason.',
         'High Partial Credit — A prediction with a reason, both having merit.'],
 '7-i': ['Partial Credit — Relationship described as negative correlation.',
         'Partial Credit — Relevant reason about the population change.'],
 '8-a-i': ['Partial Credit — Six equal sectors identified or notes the angle at the centre is 360°.',
           'Note — A correct answer without work shown, award full credit.'],
 '8-a-ii': ['Low Partial Credit — Writes a correct relevant formula.',
            'Low Partial Credit — One or two correct substitutions into formula.',
            'High Partial Credit — Correct or consistent substitution into formula.',
            'High Partial Credit — Incorrect answer from an incorrect calculator mode.',
            'Note — A correct answer without work shown, award full credit.'],
 '8-a-iii': ['Low Partial Credit — Writes a correct formula for area of sector.',
             'Low Partial Credit — Some correct substitution into a correct relevant formula.',
             'High Partial Credit — Correct area of sector.',
             'High Partial Credit — Fraction written with one error, calculated.'],
 '8-a-iv': ['Low Partial Credit — Formula for the cosine rule written.',
            'Low Partial Credit — Some correct substitution.',
            'High Partial Credit — A fully correct substitution, without complete and correct calculation.',
            'High Partial Credit — Substantially correct work in substitution and calculation.'],
 '8-a-v': ['Partial Credit — Work of merit such as reference to two sides equal.'],
 '8-b-i': ['Low Partial Credit — Writes the correct formula.',
           'High Partial Credit — Correct substitution into formula without complete and correct calculation.',
           'High Partial Credit — Incorrect substitution with correct calculation.',
           'High Partial Credit — An answer of 189 km with work.',
           'Note — A correct answer without work shown, award full credit.'],
 '8-b-ii': ['Partial Credit — One correct line drawn.'],
 '8-b-iii': ['Partial Credit — Relevant work such as |∠FDC| indicated correctly.'],
 '8-b-iv': ['Low Partial Credit — Calculates or gives one correct distance.',
            'High Partial Credit — Calculates the total distance.',
            'High Partial Credit — Sets up correct fraction to calculate time without complete and correct calculation.',
            'High Partial Credit — Sets up incorrect fraction to calculate time with correct calculation.'],
 '8-c-i': ['Low Partial Credit — Draws a line from K to X or notes additional relevant work on the diagram.',
           'Low Partial Credit — Correct trigonometric ratio set up.',
           'Low Partial Credit — Correct application of theorem of Pythagoras written.',
           'High Partial Credit — A fully correct substitution, without complete and correct calculation.',
           'High Partial Credit — One error in substitution with fully correct calculation.'],
 '8-c-ii': ['Low Partial Credit — Indicates the required point on the diagram.',
            'Low Partial Credit — Correct trigonometric ratio set up or similar work of merit.',
            'High Partial Credit — A fully correct substitution, without complete and correct calculation.',
            'High Partial Credit — One error in substitution with fully correct calculation.']}
STAR={'5-a','5-b','5-c','7-d-i','8-a-ii','8-a-iv','8-b-i','8-b-iv','8-c-i','8-c-ii'}
for s in STAR:R[s].append(L(FCM,'Penalise one mark for incorrect or omitted '+('roundoff' if s in {'7-d-i','8-b-i'} else 'units')+', provided full marks otherwise.'))
ROWS={'maths-2013-ol-p2-q'+k:v for k,v in R.items()}
if len(sys.argv)>1:quotes(ROWS,sys.argv[1]);raise SystemExit
SC={'5B':[0,3,5],'5C':[0,3,4,5],'10C':[0,4,7,10],'10D':[0,2,5,8,10],'15D':[0,4,7,11,15],'25D':[0,6,12,19,25]}
p=Paper(2013,'ol','p2',SC,'LC003GLP200EV.pdf','LC003GLP000EV.pdf',reviewed_at='2026-10-29',full_credit_minus_one=False)
def A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=None,extra=None):
 e=extra or {}
 if s in STAR:e['fullCreditMinusOne']=True
 p.A(s,ref,scale,scheme,pages,topic,atlas,prompt,stem=stem,extra=e)
coin='Katie tossed a coin 200 times and threw 109 heads. Joe tossed the same coin 400 times and threw 238 heads. Lucy tossed the same coin 500 times and threw 291 heads. Katie, Joe and Lucy now think the coin may be biased.'
A('1-a','Q1(a)','5B',[37, 56],[3],'1-3','probability','Give a reason why they think that the coin may be biased.',coin)
A('1-b','Q1(b)','10C',[37, 56],[3],'1-3','probability','Lucy uses all the above data and calculates that the best estimate of the probability of throwing a head with this coin is 0·58. Show how Lucy might have calculated this probability.',coin)
A('1-c','Q1(c)','10C',[37, 56],[3],'1-3','probability','Joe agrees with Lucy’s estimate of 0·58 as the probability of throwing a head with this coin. He claims that the probability of throwing 3 successive heads with this coin is less than the probability of throwing 2 successive tails. Calculate the probability of each event and state whether Joe’s claim is true or not.',coin)
spinner='An unbiased circular spinner has a movable pointer and five equal sectors, two coloured green and three coloured red.'
A('2-a-i','Q2(a)(i),Q2(a)(ii)','10C',[38, 57],[4],'1-3','probability','(i) Find the probability that the pointer stops on green for one spin of the spinner. (ii) List all the possible outcomes of 3 successive spins of the spinner.',spinner)
A('2-b','Q2(b)','10C',[39, 57],[4,5],'1-3','probability','A game consists of spinning the spinner 3 times. Each time the spinner stops on green the player wins €1; otherwise the player wins nothing. For example, if the outcome of one game is “green, red, green” the player wins €2. Complete the table of required outcomes for winnings of €0, €1, €2 and €3.',spinner+' Part (a)(ii): list all possible outcomes of three successive spins.')
A('2-c','Q2(c)','5C',[39, 57],[4,5],'1-3','probability','Is one spin of the spinner above an example of a Bernoulli trial? Explain what a Bernoulli trial is.',spinner)
line='l is the line 3x + 2y + 18 = 0.'
A('3-a','Q3(a)','10C',[40, 58],[6],'2-2','co-ordinate-geometry-of-the-line','Find the slope of l.',line)
A('3-b','Q3(b)','10C',[40, 58],[6],'2-2','co-ordinate-geometry-of-the-line','The line k is perpendicular to l and cuts the x-axis at the point (7, 0). Find the equation of k.',line)
A('3-c','Q3(c)','5C',[40, 58],[6],'2-2','co-ordinate-geometry-of-the-line','Find the co-ordinates of the point of intersection of the lines l and k.',line+' The line k is perpendicular to l and cuts the x-axis at (7, 0).')
circle='The point A has co-ordinates (8, 6) and O is the origin. The diagram shows circles c₁ and c₂. c₁ has centre (0, 0) and radius |OA|; c₂ has a diameter of [OA].'
A('4-a','Q4(a)','5C',[41, 59],[7],'2-3','co-ordinate-geometry-the-circle','Find the equation of c₁.',circle)
A('4-b','Q4(b)','10D',[41, 59],[7],'2-3','co-ordinate-geometry-the-circle','Find the equation of c₂.',circle)
A('4-c','Q4(c)','10C',[41, 59],[7],'2-3','co-ordinate-geometry-the-circle','The circle c₂ cuts the x-axis at the point P. Find the co-ordinates of P.',circle)
cylinder='A solid cylinder has a radius of 10 mm and a height of 45 mm.'
A('5-a','Q5(a)','5C',[42, 60],[8],'3-4','area-volume','Draw a sketch of the net of the surface of the cylinder and write its dimensions on the sketch.',cylinder)
A('5-b','Q5(b)','10C',[43, 60],[8,9],'3-4','area-volume','Calculate the volume of the cylinder. Give your answer in terms of π.',cylinder)
A('5-c','Q5(c)','10D',[43, 60],[8,9],'3-4','area-volume','A sphere has the same volume as the cylinder. Find the surface area of the sphere. Give your answer in terms of π.',cylinder)
construction='Construct the triangle ABC such that |AB| = 8 cm, |BC| = |AC| = 5 cm. The point A is given to you.'
A('6a-a','Q6A(a)','10C',[44, 61],[10],'2-1','geometry-proofs-and-constructions',construction,extra={'measurementRequired':True})
A('6a-b','Q6A(b)','10C',[44, 61],[10],'2-1','geometry-proofs-and-constructions','On the same diagram, construct the image of the triangle ABC under the axial symmetry in AB.','Part (a): '+construction,{'measurementRequired':True})
A('6a-c','Q6A(c)','5B',[44, 61],[10],'2-1','geometry-proofs-and-constructions','Justify the statement “AC′BC is a parallelogram” where C′ is the image of C under the axial symmetry in AB.','Part (a): '+construction+' Part (b): construct the reflected triangle in AB.')
A('6b','Q6B','25D',[45, 61],[11],'2-1','geometry-proofs-and-constructions','Prove that |∠ABQ| + |∠BCR| + |∠CAP| = 90°.','In the acute-angled triangle ABC, AP ⟂ BC, BQ ⟂ AC and CR ⟂ AB. The original diagram is supplied.')
data='The table shows the rates of births, marriages and deaths in Ireland from 1990 to 2010, per 10 000 of the estimated population. Rows (year: births, marriages, deaths): '+ '; '.join(f'{y}: {b}, {m}, {d}' for y,b,m,d in [(1990,151,51,90),(1991,150,49,89),(1992,144,47,87),(1993,138,47,90),(1994,135,46,86),(1995,135,43,90),(1996,140,45,87),(1997,144,43,86),(1998,146,45,85),(1999,144,50,87),(2000,145,51,83),(2001,150,50,79),(2002,155,52,76),(2003,155,51,73),(2004,153,52,71),(2005,148,52,68),(2006,154,52,67),(2007,163,52,64),(2008,168,50,63),(2009,167,48,63),(2010,165,46,61)])+'.'
A('7-a','Q7(a)','15D',[47, 62],[12,13],'1-6','statistics','Complete the back to back stem and leaf plot to show the marriage rate and death rate in Ireland during the period covered by the table.',data)
A('7-b','Q7(b)','5B',[47, 62],[12,13],'1-6','statistics','State one difference that can be observed between the distributions of the marriage rate and the death rate in your plot.',data+' Part (a): complete the back to back stem and leaf plot.')
A('7-c','Q7(c)','10C',[47, 62],[12,13],'1-6','statistics','Find the median and interquartile range of the yearly marriage rates in Ireland from 1990 to 2010.',data)
A('7-d-i','Q7(d)(i)','10C',[47, 62],[12,13],'1-6','statistics','Find the mean of the death rate in Ireland from 1990 to 2010. Give your answer correct to one decimal place.',data)
A('7-d-ii','Q7(d)(ii)','5C',[48, 63],[12,13,14],'1-6','statistics','The standard deviation of the death rates in the table is 10·3. List all of the death rates that are within 1 standard deviation of the mean.',data+' Part (d)(i): find the mean death rate correct to one decimal place.')
A('7-e','Q7(e)','5C',[48, 63],[12,14],'1-6','statistics','In 2010, the number of children born in Ireland was 75 174. Use this number to estimate the total population of Ireland in 2010.',data)
A('7-f','Q7(f)','5C',[48, 63],[12,14],'1-6','statistics','Use your answer to (e) to estimate the number of people who died in Ireland in 2010.',data+' Part (e): use 75 174 births in 2010 to estimate the total population.')
A('7-g','Q7(g)','5B',[48, 63],[12,14],'1-6','statistics','“More children were born in Ireland in 1990 than in 2000.” Give a reason, based on the data, why this statement is not necessarily true.',data)
A('7-h','Q7(h)','10C',[49, 63],[12,15],'1-6','statistics','Find the ratio, Birth rate : Death rate, for the two years 1990 and 2010. Based on your answers for the two years, what would you predict about the population of Ireland in future years? Give a reason for your answer.',data)
A('7-i','Q7(i)','5B',[49, 63],[15],'1-6','statistics','The birth rate and death rate over the 21 years are plotted against each other in the scatter plot below. The correlation coefficient between the two sets of data is −0·85. Describe the relationship between the two sets of data and suggest a reason why this might be the case.','Birth and death rates are per 10 000 of the estimated population in Ireland, 1990–2010. The original scatter plot is supplied.')
sea='A search is begun for a buoy that has become detached from its mooring at sea. The area to be searched is a circle of radius 30 km from the last known position, K, of the buoy. The search area is divided into six equal sectors indicated by A, B, C, D, E and F in the original diagram.'
A('8-a-i','Q8(a)(i)','5B',[50, 64],[16],'2-1','geometry','Find |∠BKA|.',sea+' Fishing boats search the triangular area KAB.')
A('8-a-ii','Q8(a)(ii)','10C',[50, 64],[16],'2-4','trigonometry','Find the area of the triangle KAB.',sea+' Fishing boats search the triangular area KAB.')
A('8-a-iii','Q8(a)(iii)','10C',[51, 64],[16,17],'3-4','area-volume','Write the area of the triangle KAB as a percentage of the area of the sector KAB.',sea)
A('8-a-iv','Q8(a)(iv)','10C',[51, 64],[16,17],'2-4','trigonometry','Use the cosine rule to find the length of [AB].',sea)
A('8-a-v','Q8(a)(v)','5B',[51, 64],[16,17],'2-1','geometry','What does your answer to (iv) above show about the triangle KAB?',sea+' Part (a)(iv): use the cosine rule to find |AB|.')
A('8-b-i','Q8(b)(i)','5C',[52, 65],[16,18],'3-4','area-volume','A helicopter took part in the search. The helicopter flew from the point F around the perimeter of the search area. What distance did the helicopter fly, correct to the nearest km?',sea)
flight='The helicopter then flew in a straight line from F to D and from D on to C, also in a straight line.'
A('8-b-ii','Q8(b)(ii)','5B',[52, 65],[16,18],'2-1','geometry',flight+' Draw the path of the helicopter on the diagram.',sea)
A('8-b-iii','Q8(b)(iii)','5B',[52, 65],[16,18],'2-1','geometry-proofs-and-constructions','A theorem on your course can be used to find |∠FDC|. Write down |∠FDC| and state the theorem.',sea+' '+flight)
A('8-b-iv','Q8(b)(iv)','10C',[52, 65],[16,18],'2-4','trigonometry','The helicopter flew at a speed of 80 km/h. How long did it take to fly from F to D and on to C?',sea+' '+flight)
boat='A lifeboat taking part in the search sailed, in a straight line, from K until it reached a point X, the midpoint of [ED].'
A('8-c-i','Q8(c)(i)','5C',[53, 66],[16,19],'2-4','trigonometry','Calculate |KX|.',sea+' '+boat)
A('8-c-ii','Q8(c)(ii)','5C',[53, 66],[16,18,19],'2-4','trigonometry','The buoy was located at the point where the path KX, of the lifeboat, crossed the path FD of the helicopter. How far was the buoy from X?',sea+' '+flight+' '+boat)
marks={str(q):25 for q in range(1,6)}|{'6A':25,'6B':25,'7':75,'8':75}
p.check(marks,40)
p.review(marks,'Independent visual inspection of all 20 original question pages and scheme PDF pages 35–68, including every model, scale, allocation and detailed credit note. Forty marking units include both Q6 alternatives; Q2(a)(i)+(ii) share one 10C scale.',list(range(35,69)),[54,55],
 ['325 offered marks, 300 candidate marks; both Q6 routes retained. The unlettered Q6B proof is one 25D task with all five bands.',
  'Q2(a)(i)+(ii) is one shared 10C task; its list of all eight outcomes is required, not an answer-choice pool. Q2(b) requires every category, not a finite selection.',
  'Paper 2 uses 5B 0,3,5; 5C 0,3,4,5; 10C 0,4,7,10; 10D 0,2,5,8,10; 15D 0,4,7,11,15; 25D 0,6,12,19,25.',
  'Phase 2-specific credit conditions for Q3, Q4 and Q5 retained, including line-equation, radius-squared and exact-pi criteria.',
  'Only ten starred tasks allow Full Credit minus one. Q7(d)(i) explicitly accepts 78. Q7(c) preserves both accepted interquartile ranges.',
  'Original construction baseline, proof diagram, full 21-year table, stem-and-leaf plot, scatter plot and search diagrams accompany all dependent tasks. Prior answers are not supplied in question context.'],
 [{'pages':[2,10,11],'wording':'either Question 6A or Question 6B; Answer either 6A or 6B; OR','classification':'numbered-alternatives','reason':'Both complete routes retained at 25 marks each.'},{'pages':[4,5],'wording':'List all the possible outcomes; Complete the following table','classification':'all-required-outcomes','reason':'Every spinner outcome and winnings category is required, no finite answer selection.'},{'pages':[13],'wording':'State one difference','classification':'open-response','reason':'No finite pool of possible differences is supplied.'}],
 lambda t:('numbered-alternatives','Both Q6A and Q6B retained.') if '6A' in t or '6B' in t or t.strip()=='OR' else ('all-required','All printed tasks retained.') if 'Answer all' in t or 'Answer both' in t else None)
SCHEME_ROW_FIGURES = {'maths-2013-ol-p2-q1-a': 'maths-2013-OL-scheme-project-p035-i0', 'maths-2013-ol-p2-q1-b': 'maths-2013-OL-scheme-p037-i1', 'maths-2013-ol-p2-q1-c': 'maths-2013-OL-scheme-project-p035-i2', 'maths-2013-ol-p2-q2-a-i': 'maths-2013-OL-scheme-p038-i0', 'maths-2013-ol-p2-q2-b': 'maths-2013-OL-scheme-project-p037-i0', 'maths-2013-ol-p2-q2-c': 'maths-2013-OL-scheme-p039-i1', 'maths-2013-ol-p2-q3-a': 'maths-2013-OL-scheme-project-p038-i0', 'maths-2013-ol-p2-q3-b': 'maths-2013-OL-scheme-project-p038-i1', 'maths-2013-ol-p2-q3-c': 'maths-2013-OL-scheme-p040-i2', 'maths-2013-ol-p2-q4-a': 'maths-2013-OL-scheme-project-p039-i0', 'maths-2013-ol-p2-q4-b': 'maths-2013-OL-scheme-p041-i1', 'maths-2013-ol-p2-q4-c': 'maths-2013-OL-scheme-p041-i2', 'maths-2013-ol-p2-q5-a': 'maths-2013-OL-scheme-project-p040-i0', 'maths-2013-ol-p2-q5-b': 'maths-2013-OL-scheme-p043-i0', 'maths-2013-ol-p2-q5-c': 'maths-2013-OL-scheme-project-p041-i1', 'maths-2013-ol-p2-q6a-a': 'maths-2013-OL-scheme-project-p042-i0', 'maths-2013-ol-p2-q6a-b': 'maths-2013-OL-scheme-project-p042-i1', 'maths-2013-ol-p2-q6a-c': 'maths-2013-OL-scheme-project-p042-i2', 'maths-2013-ol-p2-q6b': 'maths-2013-OL-scheme-p045-i0', 'maths-2013-ol-p2-q7-a': 'maths-2013-OL-scheme-project-p045-i0', 'maths-2013-ol-p2-q7-b': 'maths-2013-OL-scheme-project-p045-i1', 'maths-2013-ol-p2-q7-c': 'maths-2013-OL-scheme-p047-i2', 'maths-2013-ol-p2-q7-d-i': 'maths-2013-OL-scheme-project-p045-i3', 'maths-2013-ol-p2-q7-d-ii': 'maths-2013-OL-scheme-project-p046-i0', 'maths-2013-ol-p2-q7-e': 'maths-2013-OL-scheme-project-p046-i1', 'maths-2013-ol-p2-q7-f': 'maths-2013-OL-scheme-p048-i2', 'maths-2013-ol-p2-q7-g': 'maths-2013-OL-scheme-project-p046-i3', 'maths-2013-ol-p2-q7-h': 'maths-2013-OL-scheme-p049-i0', 'maths-2013-ol-p2-q7-i': 'maths-2013-OL-scheme-project-p047-i1', 'maths-2013-ol-p2-q8-a-i': 'maths-2013-OL-scheme-project-p048-i0', 'maths-2013-ol-p2-q8-a-ii': 'maths-2013-OL-scheme-project-p048-i1', 'maths-2013-ol-p2-q8-a-iii': 'maths-2013-OL-scheme-p051-i0', 'maths-2013-ol-p2-q8-a-iv': 'maths-2013-OL-scheme-project-p049-i1', 'maths-2013-ol-p2-q8-a-v': 'maths-2013-OL-scheme-p051-i2', 'maths-2013-ol-p2-q8-b-i': 'maths-2013-OL-scheme-project-p050-i0', 'maths-2013-ol-p2-q8-b-ii': 'maths-2013-OL-scheme-project-p050-i1', 'maths-2013-ol-p2-q8-b-iii': 'maths-2013-OL-scheme-project-p050-i2', 'maths-2013-ol-p2-q8-b-iv': 'maths-2013-OL-scheme-p052-i3', 'maths-2013-ol-p2-q8-c-i': 'maths-2013-OL-scheme-project-p051-i0', 'maths-2013-ol-p2-q8-c-ii': 'maths-2013-OL-scheme-project-p051-i1'}
p.apply(ROWS,'2013 Ordinary Project Maths Phase 2 Paper 2',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
