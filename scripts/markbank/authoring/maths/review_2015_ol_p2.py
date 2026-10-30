"""2015 Ordinary Paper 2: 37 published scale units, 300 marks, all new."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from review_lib import *

R = {
 '1-a':[L(PC,'Any work of merit e.g. Mention of 10 or 6, use of !.'),L(FC,'Accept correct answers without work.')],
 '1-b-i':[L(NOTE,'Accept correct or consistent work from (a).'),L(LPC,'Any work of merit e.g. Works with value from (a) reduced to exclude zero.'),L(HPC,'Any one correct answer.'),L(FC,'Accept correct answers without work.')],
 '1-c':[L(PC,'Any work of merit.'),L(FC,'Correct answer without work.')],
 '2-a-i':[L(LPC,'Writes a correct relevant formula e.g. [Slope or equation of line].'),L(LPC,'Identifies slope and stops.')],
 '2-b':[L(PC,'Writes equation of line formula.')],
 '2-c':[L(LPC,'Correctly identifies any one pair of corresponding sides.'),L(LPC,'States SSS, SAS, RHS, ASA.'),L(HPC,'Fails to finish.'),L(HPC,'Any 2 elements identified.'),L(HPC,'Diagram marked with 3 elements identified.'),L(FC,'Accept correct explanation on basis of diagram information.')],
 '3-a':[L(LPC,'Attempt to scale an axis.'),L(MPC,'Any two of the four components Centre, Radius, Scale or Drawing correct.'),L(HPC,'Any three of the four components Centre, Radius, Scale or Drawing correct.')],
 '3-b':[L(PC,'Any correct or consistent substitution.'),L(PC,'Radius = 5 (relevant work).'),L(PC,'No conclusion.')],
 '3-c':[L(PC,'Identifies a correct relevant formula'),L(PC,'Any correct substitution and stops.'),L(PC,'Radius calculated.'),L(PC,'Fully correct or consistent substitution without calculation.'),L(PC,'Correct calculation with one incorrect substitution.')],
 '4-a':[L(LPC,'Any correct relevant work or statement for x, y, or z.'),L(LPC,'One correct value without reason.'),L(MPC,'One correct value and reason.'),L(MPC,'Two correct values without reasons.'),L(MPC,'Two correct with one reason.'),L(HPC,'Two correct values, both with reasons.'),L(HPC,'All correct values with one reason.'),L(NOTE,'Answers may be on the diagram.')],
 '4-b-i':[L(LPC,'Any correct relevant work on the area of triangle in either part.'),L(HPC,'One correct area.'),L(FC,'Accept correct answer without work.')],
 '5-a-i':[L(LPC,'Writes Sine Rule.'),L(HPC,'A correct answer without work.')],
 '5-a-ii':[L(NOTE,'Accept consistent answer from previous work.'),L(LPC,'Writes the correct formula for the area of a triangle.'),L(LPC,'Any correct or consistent substitution into formula.'),L(HPC,'Calculates area of the triangle with one incorrect substitution.'),L(HPC,'A correct or consistent answer without work.')],
 '5-b':[L(LPC,'Writes Cosine Rule correctly.'),L(MPC,'An almost correct formula substitution and stops.'),L(HPC,'A correct or consistent answer without work.')],
 '6-a-i':[L(LPC,'Plots some points to illustrate a scatter graph but shows no understanding of correlation in any of the cases.'),L(LPC,'Plots one correlation with less than ten points.'),L(MPC,'Plots one correct type of correlation.'),L(MPC,'Plots two types of correlation only with less than ten points.'),L(HPC,'Plots two correct types of correlation.'),L(HPC,'Plots three types of correlation some with less than ten points.')],
 '6-b-i':[L(HPC,'One correct solution.'),L(HPC,'Substantive work in both parts.')],
 '7-a-i':[L(LPC,'An attempt to draw any construction ray e.g. [Join B to Q].'),L(HPC,'Two construction rays drawn.'),L(HPC,'Construction rays drawn but centre not identified correctly.')],
 '7-a-ii':[L(NOTE,'Accept tolerance of 5 mm'),L(NOTE,'Accept correct or consistent work from previous section.'),L(LPC,'One measurement correct.'),L(HPC,'Two measurements correct.'),L(HPC,'Error in scale factor.')],
 '7-b':[L(PC,'Correct answer without work.')],
 '7-c-i':[L(NOTE,'Accept correct or consistent from previous work.'),L(ZC,'Correct answer without work.')],
 '8-a-i':[L(FC,'Accept a correct answer without work. (6 m).')],
 '8-a-ii':[L(NOTE,'Accept correct /consistent answer from (a)(i).'),L(PC,'Any work of merit e.g. writes the correct formula, identifies correct/consistent radius.'),L(FC,'Accept a correct/consistent answer without work.')],
 '8-b-i':[L(NOTE,'Accept correct /consistent answer from (a)(i).'),L(LPC,'Any work of merit e.g. writes the correct formula, identifies correct/consistent radius.'),L(HPC,'Correct formula with correct/consistent substitution and stops.'),L(FC,'Accept a correct/consistent answer without work.')],
 '8-b-ii':[L(NOTE,'Accept correct /consistent answer from (b)(i).'),L(FC,'Accept a correct/consistent answer without work.')],
 '8-b-iii':[L(NOTE,'Accept correct/consistent answer from (b)(ii).'),L(LPC,'Any correct relevant work e.g. Writes answer from (b) (ii), sets up division.'),L(HPC,'Finishes with only one error…e.g. incorrect number of tins.'),L(HPC,'Sets up correct cost multiplication and stops.')],
 '8-c-i':[L(PC,'Writes correct formula.'),L(PC,'Correct formula with correct/consistent substitution and stops.'),L(FC,'Accept a correct/consistent answer without work.')],
 '8-c-ii':[L(NOTE,'Accept correct/ consistent answer from (a)(ii) and (c)(i).'),L(LPC,'Any correct or relevant work e.g. writes answers from (a)(ii) or (c)(i).'),L(LPC,'Work towards setting up relevant equation with or without substitution.'),L(MPC,'Calculates the volume of the cylinder (523).'),L(MPC,'Finishes with two errors… e.g. one incorrect volume and a transposition error.'),L(HPC,'Finishes with only one error… e.g. index error, transposition error.')],
 '9-a':[L(LPC,'Tick in Numerical Continuous with no explanation.'),L(HPC,'A tick and an incomplete explanation for Numerical Continuous.'),L(FC,'A tick and a correct explanation for Numerical Continuous.'),L(FC,'A tick and a correct explanation for Numerical Discrete.')],
 '9-b-i':[L(LPC,'Work of merit.'),L(FC,'Correct answer without work.')],
 '9-b-ii':[L(LPC,'One end of range identified correctly.'),L(HPC,'Both ends of range identified correctly.'),L(FC,'Correct answer without work.')],
 '9-b-iii':[L(PC,'Presents an incomplete explanation e.g. “Half are tall”.'),L(FC,'Indicates “middle” of the sample.')],
 '9-c-i':[L(LPC,'One/two correct percentage.'),L(LPC,'Attempt to find % e.g. Writes 100.'),L(HPC,'Any three correct percentages.'),L(HPC,'Decimal format used.')],
 '9-c-ii':[L(PC,'Any work of merit e.g. One correct block.')],
 '9-c-iii':[L(PC,'Indicates correct answer only.'),L(PC,'Incomplete explanation.')],
 '9-c-iv':[L(PC,'Indicates correct answer.'),L(PC,'Indicates correct answer and an incomplete explanation.')],
 '9-d-i':[L(LPC,'Writes a correct formula and stops.')],
 '9-d-ii':[L(PC,'An incomplete interpretation e.g. Says different values/Subtracts values, with no interpretation.')],
}
ROWS={'maths-2015-ol-p2-q'+k:v for k,v in R.items()}
if len(sys.argv)>1: quotes(ROWS,sys.argv[1]); raise SystemExit
p=Paper(2015,'ol','p2',{'5A':[0,5],'5B':[0,3,5],'5C':[0,3,4,5],'5D':[0,2,3,4,5],'10B':[0,4,10],'10C':[0,4,9,10],'10D':[0,2,5,8,10],'15C':[0,4,11,15],'15D':[0,4,7,11,15],'20C':[0,10,17,20],'20D':[0,5,10,15,20]},'LC003GLP200EV.pdf','LC003GLP000EV.pdf',reviewed_at='2026-10-29')
A=p.A
bank='A bank issues a unique six-digit password to each of its online customers. The password may contain any of the numbers 0 to 9 in any position and numbers may be repeated. For example, 071737 is a valid password.'
A('1-a','Q1(a)','10B',[31,47],[3],'1-1','counting','How many different passwords are possible?',stem=bank)
A('1-b-i','Q1(b)(i),Q1(b)(ii)','10C',[31,47],[3],'1-1','counting,probability','(i) How many different passwords do not contain any zero? (ii) One password is selected at random from all the possible passwords. What is the probability that this password contains at least one zero?',stem=bank)
A('1-c','Q1(c)','5B',[31,47],[3],'1-1','counting','John is issued with one such password from the bank. Each time John wants to access his account online, the bank’s website requires him to input three of his password digits into the boxes provided. For example, he may be asked for the 2nd, 4th and 5th digits, as shown below. In how many different ways can the bank select the three required boxes?',stem=bank)
line='The line p makes equal intercepts on the axes at A and at B, as shown.'
q2a='(i) Write down the slope of p. (ii) The point (1, 5) is on p. Find the equation of p. Write your answer in the form ax + by + c = 0, where a, b, and c ∈ ℤ.'
q2b='The line q is perpendicular to p and contains the point O(0, 0). Find the equation of q.'
A('2-a-i','Q2(a)(i),Q2(a)(ii)','10C',[32,48],[4],'2-2','co-ordinate-geometry-of-the-line',q2a,stem=line)
A('2-b','Q2(b)','10B',[32,48],[4],'2-2','co-ordinate-geometry-of-the-line',q2b,stem=line)
A('2-c','Q2(c)','5C',[32,48],[4],'2-1','geometry-proofs-and-constructions','The lines p and q intersect at the point C. Explain why the triangles OCA and OBC are congruent.',stem=line+' The line q is perpendicular to p and contains the point O(0, 0).')
A('3-a','Q3(a)','10D',[33,49],[5],'2-3','co-ordinate-geometry-the-circle','Draw the circle c: x² + y² = 25. Show your scale on both axes.')
A('3-b','Q3(b)','10B',[33,49],[5],'2-3','co-ordinate-geometry-the-circle','Verify, using algebra, that A(−4, 3) is on c.',stem='The circle c has equation x² + y² = 25.')
A('3-c','Q3(c)','5B',[33,49],[5],'2-3','co-ordinate-geometry-the-circle','Find the equation of the circle with centre (−4, 3) that passes through the point (3, 4).')
A('4-a','Q4(a)','20D',[34,50],[6],'2-1','geometry','The diagram shows a parallelogram, with one side produced. Use the data on the diagram to find the value of x, of y, and of z. Give a reason for your answer in each case.')
A('4-b-i','Q4(b)(i),Q4(b)(ii)','5C',[34,50],[6],'2-1','geometry,area-volume','(i) Find the area of the triangle ABD. (ii) E is the midpoint of [CD]. Find the area of the triangle BCE.',stem='The area of the parallelogram ABCD is 480 m².')
tri='The diagram shows the triangles BCD and ABD, with some measurements given.'
A('5-a-i','Q5(a)(i)','15D',[35,51],[7],'2-4','trigonometry','Find |BC|, correct to two decimal places.',stem=tri)
A('5-a-ii','Q5(a)(ii)','5C',[35,51],[7],'2-4','trigonometry','Find the area of the triangle BCD, correct to two decimal places.',stem=tri)
A('5-b','Q5(b)','5D',[35,51],[7],'2-4','trigonometry','Find |AB|, correct to two decimal places.',stem=tri)
A('6-a-i','Q6(a)(i),Q6(a)(ii),Q6(a)(iii)','20D',[36,52],[8],'1-7','statistics','Mark ten or more points on each of the scatter graphs below to show an example of the type of correlation named under each graph: (i) Strong positive correlation; (ii) Strong negative correlation; (iii) No correlation.')
A('6-b-i','Q6(b)(i),Q6(b)(ii)','5C',[37,52],[9],'1-7','statistics','(i) If YouGov sampled 1000 people, find the margin of error. Write your answer as a percentage, correct to one decimal place. (ii) Create a 95% confidence interval for the level of support for the ‘No’ campaign in the population.',stem='A few days before the Scottish Independence Referendum in September 2014 a YouGov poll estimated the support for the ‘No’ campaign to be 54%.')
logo='The diagram below shows the right-angled triangle ABC, which is used in the logo for a company called Deane Construction Limited (DCL). The triangle PQR is the image of ABC under an enlargement.'
q7ai='Construct the centre of enlargement and label it O.'
q7aii='(ii) Measure, in centimetres, |OB| and |OQ|. (iii) Use your measurements to find the scale factor of the enlargement, correct to one decimal place.'
A('7-a-i','Q7(a)(i)','15C',[38,39,53],[10,11],'2-1','geometry',q7ai,stem=logo,extra={'measurementRequired':True})
A('7-a-ii','Q7(a)(ii),Q7(a)(iii)','10C',[38,39,53],[10,11],'2-1','geometry',q7aii,stem=logo+' Part (a)(i): '+q7ai,extra={'measurementRequired':True})
A('7-b','Q7(b)','5B',[39,53],[10,11],'2-1','geometry,area-volume','The area of the triangle ABC is 7·5 cm². Use the scale factor to find the area of the image triangle PQR under the enlargement.',stem=logo+' Part (a)(i): '+q7ai+' Part (a): '+q7aii,extra={'measurementRequired':True})
A('7-c-i','Q7(c)(i),Q7(c)(ii),Q7(c)(iii)','5D',[39,53],[10,11],'2-1','geometry,trigonometry','(i) Given that |AB| = 5 cm, use the scale factor to find |PQ|. (ii) Given that |QR| = 8·7 cm, use the scale factor to find |BC|. (iii) Hence, show that |∠ABC| = |∠PQR|.',stem=logo+' Part (a)(i): '+q7ai+' Part (a): '+q7aii,extra={'measurementRequired':True})
tank='A company has a spherical storage tank. The diameter of the tank is 12 m.'
paint='The company paints the outside curved surface of the spherical tank.'
q8bii='The curved surface is painted with a special paint. One litre of paint will cover 3·5 m². Find how many litres of paint are used, correct to the nearest litre.'
A('8-a-i','Q8(a)(i)','5A',[40,54],[12],'3-4','area-volume','Write down the radius of the tank.',stem=tank)
A('8-a-ii','Q8(a)(ii)','10B',[40,54],[12],'3-4','area-volume','Find the volume of the tank, correct to the nearest m³.',stem=tank)
A('8-b-i','Q8(b)(i)','5C',[40,54],[12],'3-4','area-volume','Find the curved surface area of the tank, correct to one decimal place.',stem=tank+' '+paint)
A('8-b-ii','Q8(b)(ii)','5A',[40,54],[12],'3-4','area-volume',q8bii,stem=tank+' '+paint)
A('8-b-iii','Q8(b)(iii)','5C',[40,54],[12],'3-4','area-volume','The paint is sold in 25 litre tins. Each tin costs €180. Find the total cost of the paint.',stem=tank+' '+paint+' '+q8bii)
other='At another site the company has a differently-shaped tank with the same volume. This tank has hemispherical ends and a cylindrical mid-section of length h m, as shown. The radius of each hemispherical end is 4·5 m.'
A('8-c-i','Q8(c)(i)','5B',[41,55],[13],'3-4','area-volume','Find the volume of one hemispherical end, correct to the nearest m³.',stem=other)
A('8-c-ii','Q8(c)(ii)','10D',[41,55],[12,13],'3-4','area-volume','Find the length, h, of the cylindrical section, correct to one decimal place.',stem=tank+' '+other)
heights='The heights of a random sample of 1000 students were collected and recorded.'
girls='The sample of 1000 students was made up of 500 boys and 500 girls. The data from the 500 girls was used to create the information shown in Table 1.'
table='Table 1 (Girls). Height (cm): 145–150, 150–155, 155–160, 160–165, 165–170, 170–175, 175–180, 180–185. Number of girls: 15, 48, 80, 112, 125, 81, 29, 10.'
table2='Table 2 (Girls, %). Height (cm): 145–150, 150–155, 155–160, 160–165, 165–170, 170–175, 175–180, 180–185. Percentage of girls: _, _, _, 22·4, 25, _, _, _.'
A('9-a','Q9(a)','5C',[42,56],[14],'1-5','statistics','Tick one box from the table below to indicate how you would categorise the type of data collected. Explain your choice. Options: Categorical Nominal; Categorical Ordinal; Numerical Discrete; Numerical Continuous.',stem=heights)
A('9-b-i','Q9(b)(i)','20C',[42,56],[14],'1-6','statistics','Use the information in Table 1 to estimate the mean height of the girls, using mid-interval values.',stem=heights+' '+girls+' '+table)
A('9-b-ii','Q9(b)(ii)','5C',[42,56],[14],'1-6','statistics','What is the largest possible value for the range of the heights of the girls in this sample?',stem=heights+' '+girls+' '+table)
A('9-b-iii','Q9(b)(iii)','5B',[42,56],[14],'1-6','statistics','The median height of the girls in the sample is 164·5 cm. Explain what this means in the context of the heights of the 500 girls.',stem=heights+' '+girls)
q9ci='Use the data in Table 1 to complete Table 2 by finding the percentage of girls in each of the height categories.'
q9cii='Use the data in Table 2 to draw a histogram showing the percentage of girls in each height category.'
A('9-c-i','Q9(c)(i)','5C',[43,57],[14,15],'1-6','statistics',q9ci,stem=heights+' '+girls+' '+table+' '+table2)
A('9-c-ii','Q9(c)(ii)','10B',[43,57],[14,15],'1-6','statistics',q9cii,stem=heights+' '+girls+' '+table+' '+table2+' Part (c)(i): '+q9ci)
A('9-c-iii','Q9(c)(iii)','5B',[43,57],[14,15],'1-6','statistics','A histogram showing the percentage of boys in each height category is given above. John examines both histograms and comments that “There are roughly twice as many boys as girls in the 175 to 180 cm category”. Do the histograms support his claim? Explain your answer.',stem=heights+' '+girls+' '+table+' '+table2+' Part (c)(i): '+q9ci+' Part (c)(ii): '+q9cii)
A('9-c-iv','Q9(c)(iv)','5B',[43,44,57],[14,15,16],'1-6','statistics','Mary examines both histograms and comments that “I see that there are more tall girls than tall boys”. Do the two histograms support her claim? Explain your answer.',stem=heights+' '+girls+' '+table+' '+table2+' Part (c)(i): '+q9ci+' Part (c)(ii): '+q9cii)
A('9-d-i','Q9(d)(i)','5C',[44,57],[14,16],'1-7','statistics','The mean height of the boys in the sample is 166·7 cm and the standard deviation of their height is 8·9 cm. Assuming that boys’ heights are normally distributed, use the Empirical Rule to find an interval that will contain the heights of approximately 95% of all boys.',stem=heights+' '+girls)
A('9-d-ii','Q9(d)(ii)','5B',[44,57],[14,16],'1-7','statistics','The standard deviation of the heights of the girls in the sample is 7·7 cm while the standard deviation of the heights of the boys is 8·9 cm. Interpret this difference in the context of the data.',stem=heights+' '+girls)
marks={'1':25,'2':25,'3':25,'4':25,'5':25,'6':25,'7':35,'8':45,'9':70}
p.check(marks,37)
p.review(marks,'Independent visual inspection of all 20 question PDF pages and scheme PDF pages 29–60, including all model solutions, the scale table, allocation summary and detailed credit notes. Published mark boundaries independently reconciled with all 300 marks.',list(range(29,61)),[45,46],
 ['All nine questions are compulsory. Every published scale boundary is retained in 37 cards, totalling 300 marks.',
  'Shared scales: Q1(b)(i)+(ii), Q2(a)(i)+(ii), Q4(b)(i)+(ii), Q6(a)(i)+(ii)+(iii), Q6(b)(i)+(ii), Q7(a)(ii)+(iii), Q7(c)(i)+(ii)+(iii). Q7(a)(i) remains its separately marked construction.',
  'Paper 2 has different ladders from Paper 1: 10B 0,4,10; 10C 0,4,9,10; 10D 0,2,5,8,10; 15C 0,4,11,15; 15D 0,4,7,11,15; 20C 0,10,17,20; 20D 0,5,10,15,20. General Full Credit minus one is retained.',
  'Q9(c)(i)–(iv) are confirmed in the PDF text layer, individual question crops, allocation summary and detailed notes. The Q9(d)(i) notes heading omits an opening parenthesis; its unambiguous scale remains 5C.',
  'Q7 retains the original enlargement diagram and measurement access. Dependent tasks carry the original construction/scale-factor prompts, not inserted answers. Q9 dependent statistics cards retain the data tables and original boys histogram.',
  'The Q4(a) model has a printed 100° typo in its calculation for y; the diagram gives 110° and the correct calculation is 180°−(110°+30°)=40°. Q4(b)(ii) prints half the parallelogram area equal to 120 m²; the correct fraction is one quarter. Q8(b)(iii) rounds 129/25 inconsistently: 5·16 from rounded litres or about 5·17 from unrounded litres, both requiring six tins costing €1080. Original images are preserved with separately labelled clarifications.',
  'Model equations and full credit notes are carried as typeset source images after reveal; text quotes only intact prose. Source references use PDF positions; scheme printed page numbers are two less.'],
 [{'pages':[2,3,10],'wording':'Answer all nine / six / three questions','classification':'all-questions-required','reason':'All tasks are retained.'},
  {'pages':[3],'wording':'select the three required boxes','classification':'counting-problem','reason':'The selection is the mathematical problem, not a choice of examination tasks.'},
  {'pages':[14],'wording':'Tick one box','classification':'single-response-classification','reason':'One data-classification answer, with explanation; not alternative questions.'}],
 lambda t:('all-questions-required','Every published scale unit from all nine questions is retained.') if 'Answer all' in t else None)
SCHEME_ROW_FIGURES = {'maths-2015-ol-p2-q1-a': 'maths-2015-OL-scheme-p031-i0', 'maths-2015-ol-p2-q1-b-i': 'maths-2015-OL-scheme-p031-i1', 'maths-2015-ol-p2-q1-c': 'maths-2015-OL-scheme-p031-i2', 'maths-2015-ol-p2-q2-a-i': 'maths-2015-OL-scheme-p032-i0', 'maths-2015-ol-p2-q2-b': 'maths-2015-OL-scheme-p032-i1', 'maths-2015-ol-p2-q2-c': 'maths-2015-OL-scheme-p032-i2', 'maths-2015-ol-p2-q3-a': 'maths-2015-OL-scheme-p033-i0', 'maths-2015-ol-p2-q3-b': 'maths-2015-OL-scheme-p033-i1', 'maths-2015-ol-p2-q3-c': 'maths-2015-OL-scheme-p033-i2', 'maths-2015-ol-p2-q4-a': 'maths-2015-OL-scheme-p034-i0', 'maths-2015-ol-p2-q4-b-i': 'maths-2015-OL-scheme-p034-i1', 'maths-2015-ol-p2-q5-a-i': 'maths-2015-OL-scheme-p035-i0', 'maths-2015-ol-p2-q5-a-ii': 'maths-2015-OL-scheme-p035-i1', 'maths-2015-ol-p2-q5-b': 'maths-2015-OL-scheme-p035-i2', 'maths-2015-ol-p2-q6-a-i': 'maths-2015-OL-scheme-p036-i0', 'maths-2015-ol-p2-q6-b-i': 'maths-2015-OL-scheme-p037-i0', 'maths-2015-ol-p2-q7-a-i': 'maths-2015-OL-scheme-p039-i0', 'maths-2015-ol-p2-q7-a-ii': 'maths-2015-OL-scheme-p039-i1', 'maths-2015-ol-p2-q7-b': 'maths-2015-OL-scheme-p039-i2', 'maths-2015-ol-p2-q7-c-i': 'maths-2015-OL-scheme-p039-i3', 'maths-2015-ol-p2-q8-a-i': 'maths-2015-OL-scheme-p040-i0', 'maths-2015-ol-p2-q8-a-ii': 'maths-2015-OL-scheme-p040-i1', 'maths-2015-ol-p2-q8-b-i': 'maths-2015-OL-scheme-p040-i2', 'maths-2015-ol-p2-q8-b-ii': 'maths-2015-OL-scheme-p040-i3', 'maths-2015-ol-p2-q8-b-iii': 'maths-2015-OL-scheme-p040-i4', 'maths-2015-ol-p2-q8-c-i': 'maths-2015-OL-scheme-p041-i0', 'maths-2015-ol-p2-q8-c-ii': 'maths-2015-OL-scheme-p041-i1', 'maths-2015-ol-p2-q9-a': 'maths-2015-OL-scheme-p042-i0', 'maths-2015-ol-p2-q9-b-i': 'maths-2015-OL-scheme-p042-i1', 'maths-2015-ol-p2-q9-b-ii': 'maths-2015-OL-scheme-p042-i2', 'maths-2015-ol-p2-q9-b-iii': 'maths-2015-OL-scheme-p042-i3', 'maths-2015-ol-p2-q9-c-i': 'maths-2015-OL-scheme-p043-i0', 'maths-2015-ol-p2-q9-c-ii': 'maths-2015-OL-scheme-p043-i1', 'maths-2015-ol-p2-q9-c-iii': 'maths-2015-OL-scheme-p043-i2', 'maths-2015-ol-p2-q9-c-iv': 'maths-2015-OL-scheme-p044-i0', 'maths-2015-ol-p2-q9-d-i': 'maths-2015-OL-scheme-p044-i1', 'maths-2015-ol-p2-q9-d-ii': 'maths-2015-OL-scheme-p044-i2'}
p.apply(ROWS,'2015 Ordinary Level Paper 2',expect_added=[c['id'] for c in p.cards],card_overrides={k:{'figureKey':v} for k,v in SCHEME_ROW_FIGURES.items()},question_figures=True)
