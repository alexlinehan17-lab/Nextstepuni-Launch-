"""2014 Higher Paper 2: all 41 tasks, including both 6A/6B alternatives (325 offered marks)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *
R = {
 '1-a-i':[(LPC,'Identifies Cosine Rule formula'),(MPC,'All values correctly inserted'),(HPC,'Substantially correct work with one non-arithmetic error')],
 '1-a-ii':[(LPC,'Relevant area formula'),(HPC,'Values correctly inserted')],
 '1-b':[(LPC,'Some understanding of circumcentre'),(HPC,'Clearly identifies two congruent triangles but does not make reference to the remaining triangle')],
 '2-a':[(LPC,'Relevant compound angle formula'),(HPC,'Expansion correct but not tidied')],
 '2-b':[(LPC,'Correct formula for finding either arc'),(MPC,'One or both arcs expressed correctly'),(HPC,'Substantially correct work with one non-arithmetic error')],
 '3-a':[(LPC,'Reference to €3 and €5'),(HPC,'Listing with not more than five omitted')],
 '3-b':[(LPC,'One partially accurate statement'),(HPC,'Correct answer but inaccurate / only partially correct supporting evidence')],
 '3-c':[(LPC,'Establishes probability of stopping on €4 sector once'),(HPC,'Indices incorrect')],
 '4-a-i':[(LPC,'Range understood'),(HPC,'Correct range'),(HPC,'Correct number of periods')],
 '4-b-i':[(LPC,'At least three further entries in table correct'),(HPC,'Table correct')],
 '4-c-i':[(NOTE,'Scale 5C (0, 2, 3, 5)')],
 '5-a':[(LPC,'Relevant area of triangle formula'),(HPC,'Substantially correct work with one error')],
 '5-b':[(LPC,'Effort at finding one slope'),(LPC,'Effort at finding equation of RS'),(HPC,'Relevant conclusion not stated or implied')],
 '5-c':[(LPC,'Effort at finding intercept on one or both axes'),(HPC,'Either c or m found')],
 '6a-a':[('Diagram / Given, '+PC,'Effort at Diagram or Given'),('Construction, '+PC,'Construction attempted'),('Construction, '+PC,'Construction not explained or explanation incomplete'),('Proof, '+LPC,'More than one critical step omitted but still some substantial work of merit'),('Proof, '+HPC,'Proof completed with one critical step omitted')],
 '6a-b':[(PC,'Effort at drawing arc from B')],
 '6b-a':[(LPC,'Triangles named'),(HPC,'Two pairs of angles identified with justification but triangles not named')],
 '6b-b':[(LPC,'Relevant triangles identified'),(LPC,'Partly correct ratio'),(HPC,'Correct ratio established but fails to complete')],
 '6b-c':[(LPC,'Effort at establishing ratio'),(HPC,'Ratio established and values entered')],
 '7-a':[(PC,'One correct category only')],
 '7-b':[(LPC,'Effort at listing numbers in order of magnitude'),(LPC,'Some indication of understanding of the term ‘median’'),(LPC,'Some indication of understanding of interquartile range'),(HPC,'Median correct or interquartile range correct only')],
 '7-c-i':[(PC,'One or two correct (no work shown)'),(PC,'All incorrect but sum to 100%'),(PC,'Correct numerator or denominator chosen for one category- work shown')],
 '7-c-ii':[(PC,'One or two correct (no work shown)'),(PC,'All incorrect but sum to 100%'),(PC,'Correct total population - shown'),(PC,'Correct numerator or denominator chosen for one category- work shown')],
 '7-c-iii':[(NOTE,'Answer here depends on candidate’s answers in previous sections'),(PC,'One reason only'),(PC,'Reasons contradictory')],
 '7-d-i':[(PC,'Incomplete or contradictory statement')],
 '7-d-ii':[(PC,'Stating none, one or both without explanation')],
 '7-d-iii':[(LPC,'Effort at finding % increase between 2012 and 2013'),(HPC,'Total number predicted at work in 2014'),(HPC,'Percentage increase calculated'),(NOTE,'Candidates not required to round to any particular number of places of decimals')],
 '8-a-i':[(LPC,'One element entered correctly'),(LPC,'One column correct'),(LPC,'Some indication that values lie between 0 and 1'),(HPC,'Two columns correct')],
 '8-a-ii':[(LPC,'One correct value chosen'),(LPC,'Addition of values indicated'),(LPC,'Configured correctly but no values entered'),(LPC,'Answer outside range'),(HPC,'Correct values chosen but operator incorrect')],
 '8-a-iii':[(LPC,'One or both correct value(s) chosen only'),(LPC,'Configured correctly but values not entered'),(LPC,'Answer outside range'),(HPC,'Correct values chosen but incorrect operator leading to an answer within range')],
 '8-a-iv':[(PC,'Reason incorrect or incomplete')],
 '8-b-i':[(LPC,'One relevant step e.g. null hypothesis stated only'),(LPC,'Some work towards margin of error'),(MPC,'Margin of error or observed proportion'),(MPC,'Margin of error and observed proportion found but fails to continue'),(HPC,'Failure to state null hypothesis correctly'),(HPC,'Failure to contextualise answer (e.g. Stops at reject Null Hypothesis)')],
 '8-b-ii':[(PC,'Recognises interval where result must lie'),(PC,'Some relevant work')],
 '9-a-i':[(LPC,'Effort at relating one or more coefficients of given equation to general equation of circle'),(LPC,'Effort at completing square(s)'),(HPC,'Either radius or centre correct'),(HPC,'Substantive work with one critical error')],
 '9-a-ii':[(LPC,'Length of line segment formula')],
 '9-a-iii':[(LPC,'Slope DE'),(LPC,'Equation DE and stops'),(LPC,'Formula for slope and /or equation of DE'),(LPC,'Perpendicular distance formula'),(HPC,'Values inserted into perpendicular distance formula'),(HPC,'No conclusion stated or implied')],
 '9-a-iv':[(LPC,'Effort to find midpoint of DE'),(LPC,'Centre found from scaled drawing'),(HPC,'Centre of j found and inserted into equation of circle i.e radius omitted')],
 '9-a-v':[(LPC,'Effort to find F'),(HPC,'F found')],
 '9-b-i':[(PC,'Circle containing A and B but lacking in accuracy')],
 '9-b-ii':[(LPC,'Pythagoras stated or implied'),(LPC,'Effort at finding area of s or t or u'),(HPC,'Correct expression for area of any circle')],
 '9-b-iii':[(LPC,'Statement using result from (b)(ii)'),(LPC,'Recognising half area of u can be expressed in terms of three components'),(HPC,'Correct expression for two of the relevant areas')],
}
ROWS={'maths-2014-hl-p2-q'+k:[L(a,b) for a,b in v] for k,v in R.items()}
if len(sys.argv)>1: quotes(ROWS,sys.argv[1]);raise SystemExit
p=Paper(2014,'hl','p2',{'5B':[0,2,5],'5C':[0,2,3,5],'10B':[0,5,10],'10C':[0,3,7,10],'10D':[0,2,5,8,10],'15C':[0,5,10,15],'15D':[0,4,7,11,15]},'LC003ALP230EV.pdf','LC003ALP000EV.pdf',reviewed_at='2026-10-29')
A=p.A
trig='trigonometry-triangles'; ident='trigonometry-functions-identities'; geo='geometry-constructions-proofs'; prob='probability'; stat='statistics-descriptive-statistics'; infer='statistics-inferential-statistics'; line='co-ordinate-geometry-of-the-line'; circle='co-ordinate-geometry-of-the-circle'
field='The lengths of the sides of a flat triangular field ACB are |AB| = 120 m, |BC| = 134 m and |AC| = 150 m.'
A('1-a-i','Q1(a)(i)','15D',[43,65],[3],'2-3',trig,'Find |∠CBA|. Give your answer, in degrees, correct to two decimal places.',stem=field)
A('1-a-ii','Q1(a)(ii)','5C',[43,65],[3],'2-3',trig,'Find the area of the triangle ACB correct to the nearest whole number.',stem=field)
A('1-b','Q1(b)','5C',[44,65],[3],'2-1',geo,'A vertical mast, [DE], is fixed at the circumcentre, D, of the triangle. The mast is held in place by three taut cables [EA], [EB] and [EC]. Explain why the three cables are equal in length.',stem=field)
A('2-a','Q2(a)','15C',[45,66],[4],'2-3',ident,'Prove that cos 2A = cos² A − sin² A.')
A('2-b','Q2(b)','10D',[45,66],[4],'2-3',ident,'The diagram shows part of the circular end of a running track with three running lanes shown. The centre of each of the circular boundaries of the lanes is at O. Kate runs in the middle of lane 1, from A to B as shown. Helen runs in the middle of lane 2, from C to D as shown. Helen runs 3 m further than Kate. |∠AOB| = |∠COD| = θ radians. If each lane is 1·2 m wide, find θ.')
games='Two different games of chance, shown below, can be played at a charity fundraiser. In each game, the player spins an arrow on a wheel and wins the amount shown on the sector that the arrow stops in. Each game is fair in that the arrow is just as likely to stop in one sector as in any other sector on that wheel. Game A has sectors €5, €0, €6, €3, €0. Game B has sectors €2, €5, €0, €3, €1, €4.'
A('3-a','Q3(a)','10C',[46,67],[5],'1-2',prob,'John played Game A four times and tells us that he has won a total of €8. In how many different ways could he have done this?',stem=games)
A('3-b','Q3(b)','5C',[46,67],[5],'1-2',prob,'To spin either arrow once, the player pays €3. Which game of chance would you expect to be more successful in raising funds for the charity? Give a reason for your answer.',stem=games)
A('3-c','Q3(c)','10C',[46,67],[5],'1-2',prob,'Mary plays Game B six times. Find the probability that the arrow stops in the €4 sector exactly twice.',stem=games)
voltage='The graph below shows the voltage, V, in an electric circuit as a function of time, t. The voltage is given by the formula V = 311 sin(100πt), where V is in volts and t is in seconds.'
q4b='(i) The table below gives the voltage, correct to the nearest whole number, at equally spaced intervals from t₁ to t₁₂ over one complete period (as shown by the dashed lines on the diagram). Use the entries given in the table and the properties of the function to complete the table. (ii) Using a calculator, or otherwise, calculate the standard deviation, σ, of the twelve values of V in the table, correct to the nearest whole number.'
A('4-a-i','Q4(a)(i),Q4(a)(ii)','10C',[47,68],[6],'2-3',ident,'(i) Write down the range of the function. (ii) How many complete periods are there in one second?',stem=voltage)
A('4-b-i','Q4(b)(i),Q4(b)(ii)','10C',[47,48,68],[6,7],'1-6',stat+','+ident,q4b,stem=voltage)
A('4-c-i','Q4(c)(i),Q4(c)(ii)','5C',[48,68],[6,7],'2-3',ident+','+stat,'(i) The standard deviation, σ, of closely spaced values of any function of the form V = a sin(bt), over 1 full period, is given by kσ = Vmax, where k is a constant that does not depend on a or b, and Vmax is the maximum value of the function. Use the function V = 311 sin(100πt) to find an approximate value for k correct to three decimal places. (ii) Using your answer in part (c)(i), or otherwise, find the value of b required so that the function V = a sin(bt) has 60 complete periods in one second and the approximate value of a so that it has a standard deviation of 110 volts.',stem=voltage+' Part (b): '+q4b)
rs='The line RS cuts the x-axis at the point R and the y-axis at the point S(0, 10), as shown. The area of the triangle ROS, where O is the origin, is 125/3.'
A('5-a','Q5(a)','10C',[49,69],[8],'2-2',line,'Find the co-ordinates of R.',stem=rs)
A('5-b','Q5(b)','10C',[49,69],[8],'2-2',line,'Show that the point E(−5, 4) is on the line RS.',stem=rs)
A('5-c','Q5(c)','5C',[49,69],[8],'2-2',line,'A second line y = mx + c, where m and c are positive constants, passes through the point E and again makes a triangle of area 125/3 with the axes. Find the value of m and the value of c.',stem=rs+' The point E is (−5, 4).')
p.C('6a-a','Q6A(a)',[{'id':'diagram-given','label':'Diagram / Given','code':'5B'},{'id':'construction','label':'Construction','code':'5B'},{'id':'proof','label':'Proof','code':'10C'}],[50,70],[9],'2-1',geo,'Prove that, if two triangles ABC and A′B′C′ are similar, then their sides are proportional, in order: |AB|/|A′B′| = |BC|/|B′C′| = |CA|/|C′A′|. Complete the sections: Diagram; Given; To Prove; Construction; Proof.')
A('6a-b','Q6A(b)','5B',[51,70],[10],'2-1',geo,'Given the line segment [BC], construct, without using a protractor or set square, a point A such that |∠ABC| = 60°. Show your construction lines.')
chords='[AB] and [CD] are chords of a circle that intersect externally at E, as shown.'
A('6b-a','Q6B(a)','10C',[52,70],[11],'2-1',geo,'Name two similar triangles in the diagram above and give reasons for your answer.',stem=chords)
A('6b-b','Q6B(b)','10C',[52,70],[11],'2-1',geo,'Prove that |EA|·|EB| = |EC|·|ED|.',stem=chords)
A('6b-c','Q6B(c)','5C',[52,70],[11],'2-1',geo,'Given that |EB| = 6·25, |ED| = 5·94 and |CB| = 10, find |AD|.',stem=chords)
labour='Table 1 below gives details of the number of males (M) and females (F) aged 15 years and over at work, unemployed, or not in the labour force for each year in the period 2004 to 2013. The figures are in thousands.'
q7ci='The percentages of persons aged 15 years and over at work, unemployed, or not in the labour force for the year 2006 are given below. Complete the table for the year 2011. Give your answers correct to one decimal place.'
q7cii='A census in 2006 showed that there were 864 449 persons in the population aged under 15 years of age. The corresponding number in the 2011 census was 979 590. Assuming that none of these persons are in the labour force, complete the table below to give the percentages of the total population at work, unemployed, or not in the labour force for the year 2011.'
A('7-a','Q7(a)','10B',[53,71],[12],'1-4',stat,'Suggest two categories of people, aged 15 years and over, who might not be in the labour force.',stem=labour)
A('7-b','Q7(b)','5C',[53,71],[12],'1-6',stat,'Find the median and the interquartile range of the total persons at work over the period.',stem=labour)
A('7-c-i','Q7(c)(i)','5B',[54,71],[12,13],'1-6',stat,q7ci,stem=labour)
A('7-c-ii','Q7(c)(ii)','5B',[54,71],[12,13],'1-6',stat,q7cii,stem=labour)
A('7-c-iii','Q7(c)(iii)','5B',[54,71],[12,13],'1-6',stat,'A commentator states that “The changes reflected in the data from 2006 to 2011 make it more difficult to balance the Government’s income and expenditure.” Do you agree with this statement? Give two reasons for your answer based on your calculations above.',stem=labour+' Part (c)(i): '+q7ci+' Part (c)(ii): '+q7cii)
charts='Liam and Niamh are analysing the number of males and the number of females at work over the period 2004 to 2013. Liam draws the following chart, using data from Table 1. Niamh uses the same data and calculates the number of females at work as a percentage of the total number of persons at work and then draws the following chart.'
q7di='Having examined both charts, a commentator states “females were affected just as much as males by the downturn in employment.” Do you agree or disagree with this statement? Give a reason for your conclusion.'
A('7-d-i','Q7(d)(i)','5B',[55,56,71],[12,14,15],'1-5',stat,q7di,stem=labour+' '+charts)
A('7-d-ii','Q7(d)(ii)','5B',[55,56,72],[12,14,15],'1-5',stat,'Which, if any, of the two charts did you find most useful in reaching your conclusion above? Give a reason for your answer.',stem=labour+' '+charts+' Part (d)(i): '+q7di)
A('7-d-iii','Q7(d)(iii)','5C',[56,72],[12,15],'1-6',stat,'Use the data in Table 1, for the years 2012 and 2013 only, to predict the percentage of persons, aged 15 years and over, who will be at work in 2014.',stem=labour)
blood='Blood tests are sometimes used to indicate if a person has a particular disease. Sometimes such tests give an incorrect result, either indicating the person has the disease when they do not (called a false positive) or indicating that they do not have the disease when they do (called a false negative). It is estimated that 0·3% of a large population have a particular disease. A test developed to detect the disease gives a false positive in 4% of tests and a false negative in 1% of tests. A person picked at random is tested for the disease.'
q8aii='Hence, or otherwise, calculate the probability that a person selected at random from the population tests positive for the disease.'
q8aiii='A person tests positive for the disease. What is the probability that the person actually has the disease? Give your answer correct to three significant figures.'
A('8-a-i','Q8(a)(i)','10C',[57,73],[16],'1-2',prob,'Write the probability associated with each branch of the tree diagram in the blank boxes provided.',stem=blood)
A('8-a-ii','Q8(a)(ii)','5C',[57,73],[16],'1-2',prob,q8aii,stem=blood)
A('8-a-iii','Q8(a)(iii)','5C',[57,73],[16],'1-2',prob,q8aiii,stem=blood)
A('8-a-iv','Q8(a)(iv)','5B',[58,73],[16,17],'1-2',prob,'The health authority is considering using a test on the general population with a view to treatment of the disease. Based on your results, do you think that the above test would be an effective way to do this? Give a reason for your answer.',stem=blood+' Part (a)(ii): '+q8aii+' Part (a)(iii): '+q8aiii)
drug='A generic drug used to treat a particular condition has a success rate of 51%. A company is developing two new drugs, A and B, to treat the condition. They carried out clinical trials on two groups of 500 patients suffering from the condition. The results showed that Drug A was successful in the case of 296 patients. The company claims that Drug A is more successful in treating the condition than the generic drug.'
q8bi='Use a hypothesis test at the 5% level of significance to decide whether there is sufficient evidence to justify the company’s claim. State the null hypothesis and state your conclusion clearly.'
A('8-b-i','Q8(b)(i)','15D',[58,73],[17],'1-7',infer,q8bi,stem=drug)
A('8-b-ii','Q8(b)(ii)','5B',[59,74],[17],'1-7',infer,'The null hypothesis was accepted for Drug B. Estimate the greatest number of patients in that trial who could have been successfully treated with Drug B.',stem=drug+' Part (b)(i): '+q8bi)
clock='The diagram shows a circular clock face, with the hands not shown. The square part of the clock face is glass so that the mechanism is visible. Two circular cogs, h and k, which touch externally are shown. The point C is the centre of the clock face. The point D is the centre of the larger cog, h, and the point E is the centre of the smaller cog, k.'
q9ai='In suitable co-ordinates, the equation of the circle h is x² + y² + 4x + 6y − 19 = 0. Find the radius of h, and the co-ordinates of its centre, D.'
q9aii='The point E has co-ordinates (3, 2). Find the radius of the circle k.'
q9aiii='Show that the distance from C(−2, 2) to the line DE is half the length of [DE].'
A('9-a-i','Q9(a)(i)','15C',[60,75],[18],'2-2',circle,q9ai,stem=clock)
A('9-a-ii','Q9(a)(ii)','10C',[60,75],[18],'2-2',circle,q9aii,stem=clock+' Part (a)(i): '+q9ai)
A('9-a-iii','Q9(a)(iii)','10C',[60,75],[18],'2-2',line,q9aiii,stem=clock+' Part (a)(i): '+q9ai+' Part (a)(ii): '+q9aii)
A('9-a-iv','Q9(a)(iv)','5C',[61,75],[18,19],'2-2',circle,'The translation which maps the midpoint of [DE] to the point C maps the circle k to the circle j. Find the equation of the circle j.',stem=clock+' Part (a)(i): '+q9ai+' Part (a)(ii): '+q9aii+' Part (a)(iii): '+q9aiii)
A('9-a-v','Q9(a)(v)','5C',[61,76],[18,19],'2-2',circle,'The glass square is of side length l. Find the smallest whole number l such that the two cogs, h and k, are fully visible through the glass.',stem=clock+' Part (a)(i): '+q9ai+' Part (a)(ii): '+q9aii+' Part (a)(iii): '+q9aiii)
tri='The triangle ABC is right-angled at C. The circle s has diameter [AC] and the circle t has diameter [CB].'
q9bii='Prove that in any right-angled triangle ABC, the area of the circle u equals the sum of the areas of the circles s and t.'
A('9-b-i','Q9(b)(i)','5B',[61,76],[20],'2-1',geo,'Draw the circle u which has diameter [AB].',stem=tri)
A('9-b-ii','Q9(b)(ii)','5C',[62,76],[20],'2-1',geo,q9bii,stem=tri+' The circle u has diameter [AB].')
A('9-b-iii','Q9(b)(iii)','5C',[62,76],[20,21],'2-1',geo,'The diagram shows the right-angled triangle ABC and arcs of the circles s, t and u. Each of the shaded areas in the diagram is called a lune, a crescent-shaped area bounded by arcs of the circles. Prove that the sum of the areas of the two shaded lunes is equal to the area of the triangle ABC.',stem=tri+' The circle u has diameter [AB]. Part (b)(ii): '+q9bii)
marks={'1':25,'2':25,'3':25,'4':25,'5':25,'6A':25,'6B':25,'7':45,'8':45,'9':60}
p.check(marks,41)
p.review(marks,'Independent visual review of all 24 original paper pages and scheme PDF pages 41–80. All models, detailed notes and allocation/scale tables read. Both Q6 alternatives retained; 41 marking boundaries, 325 offered marks, 300 candidate marks.',list(range(41,81)),[63,64],
 ['All tasks in Questions 1–5 and 7–9 are required. Candidates choose Q6A or Q6B; both complete alternatives are represented, each worth 25 marks.',
 'Q4(a)(i)+(ii), (b)(i)+(ii), (c)(i)+(ii) each share a single scale. Q6A(a) is one complete proof with component scales Diagram/Given 5B, Construction 5B, Proof 10C.',
 'Source discrepancy: summary PDF page 64 prints Q9(a)(i) 10C and (iv) 10C; the detailed question-specific notes on PDF page 75 explicitly print 15C (0,5,10,15) and 5C (0,2,3,5). Cards use those detailed scales; either allocation totals 60. Original source preserved and the discrepancy is disclosed after reveal.',
 'The Q7(d)(i) model prints Male unemployment declined where the chart concerns employment. A separately labelled clarification corrects this wording after reveal; the original source remains intact.',
 'All diagrams, probability tree, voltage table/graph, labour-force table, comparison charts, constructions and preceding dependencies accompany the relevant tasks. Earlier answers are not supplied in questions.',
 'Paper 2 ladders differ from Paper 1. Full credit minus one follows the general notes on PDF page 63. Model working and all credit notes are shown as original typeset source images.',
 'All question and scheme references are PDF positions. Scheme printed page numbers are two less. The paper is the sole indexed 2014 Project Maths edition, LC003ALP230EV.'],
 [{'pages':[2,9,11],'wording':'either Question 6A or Question 6B / Answer either 6A or 6B','classification':'finite-alternatives-expanded','reason':'Both alternatives are included, with two cards for Q6A and three for Q6B, each alternative retaining its 25-mark tariff.'},
 {'pages':[3,12],'wording':'Answer all six / three questions','classification':'all-questions-required','reason':'All tasks retained, including the alternative sixth question.'},
 {'pages':[5,16],'wording':'either arrow / either indicating','classification':'scenario-description','reason':'Describes the games or test errors; no finite pool of exam tasks.'},
 {'pages':[7,16],'wording':'or otherwise','classification':'alternative-method','reason':'Alternative methods for one marked task.'}],
 lambda t: ('finite-alternatives-expanded','Both Q6A and Q6B are fully carded.') if '6A' in t else ('all-questions-required','Every required task retained.') if 'Answer all' in t else ('alternative-method','Alternative method within one task.') if 'or otherwise' in t else ('scenario-description','Describes the scenario, not a choice of exam tasks.') if 'either arrow' in t or 'either indicating' in t else None)
SCHEME_ROW_FIGURES = {'maths-2014-hl-p2-q1-a-i': 'maths-2014-HL-scheme-p043-i0', 'maths-2014-hl-p2-q1-a-ii': 'maths-2014-HL-scheme-p043-i1', 'maths-2014-hl-p2-q1-b': 'maths-2014-HL-scheme-p044-i0', 'maths-2014-hl-p2-q2-a': 'maths-2014-HL-scheme-p045-i0', 'maths-2014-hl-p2-q2-b': 'maths-2014-HL-scheme-p045-i1', 'maths-2014-hl-p2-q3-a': 'maths-2014-HL-scheme-p046-i0', 'maths-2014-hl-p2-q3-b': 'maths-2014-HL-scheme-p046-i1', 'maths-2014-hl-p2-q3-c': 'maths-2014-HL-scheme-p046-i2', 'maths-2014-hl-p2-q4-a-i': 'maths-2014-HL-scheme-p047-i0', 'maths-2014-hl-p2-q4-b-i': 'maths-2014-HL-scheme-p048-i0', 'maths-2014-hl-p2-q4-c-i': 'maths-2014-HL-scheme-p048-i1', 'maths-2014-hl-p2-q5-a': 'maths-2014-HL-scheme-p049-i0', 'maths-2014-hl-p2-q5-b': 'maths-2014-HL-scheme-p049-i1', 'maths-2014-hl-p2-q5-c': 'maths-2014-HL-scheme-p049-i2', 'maths-2014-hl-p2-q6a-a': 'maths-2014-HL-scheme-p050-i0', 'maths-2014-hl-p2-q6a-b': 'maths-2014-HL-scheme-p051-i0', 'maths-2014-hl-p2-q6b-a': 'maths-2014-HL-scheme-p052-i0', 'maths-2014-hl-p2-q6b-b': 'maths-2014-HL-scheme-p052-i1', 'maths-2014-hl-p2-q6b-c': 'maths-2014-HL-scheme-p052-i2', 'maths-2014-hl-p2-q7-a': 'maths-2014-HL-scheme-p053-i0', 'maths-2014-hl-p2-q7-b': 'maths-2014-HL-scheme-p053-i1', 'maths-2014-hl-p2-q7-c-i': 'maths-2014-HL-scheme-p054-i0', 'maths-2014-hl-p2-q7-c-ii': 'maths-2014-HL-scheme-p054-i1', 'maths-2014-hl-p2-q7-c-iii': 'maths-2014-HL-scheme-p054-i2', 'maths-2014-hl-p2-q7-d-i': 'maths-2014-HL-scheme-p056-i0', 'maths-2014-hl-p2-q7-d-ii': 'maths-2014-HL-scheme-p056-i1', 'maths-2014-hl-p2-q7-d-iii': 'maths-2014-HL-scheme-p056-i2', 'maths-2014-hl-p2-q8-a-i': 'maths-2014-HL-scheme-p057-i0', 'maths-2014-hl-p2-q8-a-ii': 'maths-2014-HL-scheme-p057-i1', 'maths-2014-hl-p2-q8-a-iii': 'maths-2014-HL-scheme-p057-i2', 'maths-2014-hl-p2-q8-a-iv': 'maths-2014-HL-scheme-p057-i3', 'maths-2014-hl-p2-q8-b-i': 'maths-2014-HL-scheme-p058-i0', 'maths-2014-hl-p2-q8-b-ii': 'maths-2014-HL-scheme-p059-i0', 'maths-2014-hl-p2-q9-a-i': 'maths-2014-HL-scheme-p060-i0', 'maths-2014-hl-p2-q9-a-ii': 'maths-2014-HL-scheme-p060-i1', 'maths-2014-hl-p2-q9-a-iii': 'maths-2014-HL-scheme-p060-i2', 'maths-2014-hl-p2-q9-a-iv': 'maths-2014-HL-scheme-p061-i0', 'maths-2014-hl-p2-q9-a-v': 'maths-2014-HL-scheme-p061-i1', 'maths-2014-hl-p2-q9-b-i': 'maths-2014-HL-scheme-p061-i2', 'maths-2014-hl-p2-q9-b-ii': 'maths-2014-HL-scheme-p062-i0', 'maths-2014-hl-p2-q9-b-iii': 'maths-2014-HL-scheme-p062-i1'}
p.apply(ROWS,'2014 Higher Level Paper 2 (Project Maths)',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
