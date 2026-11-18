"""Independent visual review of all 2024 deferred Ordinary Paper 2 tasks."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from solution_lib import Paper
PREFIX='maths-2024-ol-p2-deferred'
p=Paper(year=2024,level='ordinary',paper_key='p2',sitting='deferred',
 paper_file='LC003GLP200EV-deferred.pdf',scheme_file='LC003GLP000EV-deferred.pdf',prefix=PREFIX,ref='2024 OL Paper 2 — Deferred',
 scales={'5A':[0,5],'5B':[0,2,5],'5C':[0,2,3,5],'10B':[0,4,10],'10C':[0,4,5,10],'10D':[0,3,5,7,10],'15D':[0,4,6,8,15]},
 reviewed_at='2026-10-31',general_notes=[2,22,23],scheme_pages=[1,2]+list(range(21,41)),
 printed_marks={**{str(q):30 for q in range(1,7)},**{str(q):50 for q in range(7,11)}},
 review_method='Independent visual sweep of all 32 paper pages and scheme pages 1–2 and 21–40; every published mark boundary reconciled, including shared allocations, choices and source errors. All question and solution crops inspected before publication.',
 source_notes=[
 'All ten questions retained: 50 tasks and 380 offered marks. Exam-level choice does not remove practice questions.',
 'Paper 2 uses 10C (0,4,5,10) and 15D (0,4,6,8,15); do not copy the different Paper 1 bands.',
 'Q1(a)(iii) requires the complete parallelogram, but the scheme supplies only R and a preceding point plot. An attributed NextStepUni drawing supplies OPQR.',
 'Q4(b)(i): p is A\\B, not the B\\A printed in one partial-credit example; the worked p=16 and q=29 are correct.',
 'Q6(b) has only (i) and (ii) on the paper; the summary label (ii)(iii) is erroneous. The proof is a single 10D task.',
 'Q7(a)(ii): detailed notes mislabel 5B, but give (0,4,10), and the summary confirms 10B. Use 10B and preserve the original note.',
 'Q7(a)(i) and (iv): the scheme PDF table clips the graph at the right edge. Recover its embedded SEC image unchanged, preserving every point and all axis labels; add attributed explanatory captions.',
 'Q7(a)(iv): the circled outlier is at about 19 degrees Celsius and €147. The source describes its distance from the trend; a possible contextual explanation is supplied separately as an illustration, not a known fact.',
 'Q7(c)(iii): 0.23 ± 0.056 gives (0.174,0.286), not the printed (0.175,0.287). The latter follows from unrounded 74/320 ± 1/sqrt(320). Both exclude 0.30. The attributed worked example states the hypotheses and uses the rounded answers requested by the paper.',
 'Q9(c)(i): 5C gives numeric awards 0,2,3,5 but lists Low, Mid and High partial descriptors. Preserve the published awards and flag the unallocated Mid descriptor instead of inventing a mark.',
 'Q9(c)(ii): any two of four ordered solutions form one card. All four solutions are retained in the scheme; no pair-combination expansion.',
 'Q9(c)(iii): the median of P is (7+11)/2=9, which belongs to P complement. The scheme also refers to the median of P complement; this is not an additional required task.',
 'Q10(a)(iii): the earlier angle is from (ii), not the printed (iv). The shown working uses the right-triangle ratio AD=80 sin(66 degrees).',
 'Q10(b): the published solution takes the acute angle 42.5 degrees. The sine equation alone also allows 137.5 degrees; the sketch indicates the acute configuration but is explicitly not to scale.',
 ],out_name='2024-ordinary-p2-deferred.json',atlas_prefix='mathematics-ordinary-',section_of=lambda q:'A' if q<=6 else 'B')
def A(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem=None):
 p.add(suffix,parts,scale,scheme,pages,topic,atlas,prompt,quotes,stem,dict(figureKey=f'{PREFIX}-q{suffix}-solution',questionFigureKey=f'{PREFIX}-q{suffix}-question'))
line='A line k has equation 2x + y − 4 = 0, where x, y ∈ ℝ. It intersects the y-axis at Q, where x = 0, and the x-axis at P(2, 0).'
A('1-a-i','Q1(a)(i)','10C',[24],[4],'2-2','co-ordinate-geometry-of-the-line','Use the equation to find the co-ordinates of point Q.',['Some correct transposition.'],line)
A('1-a-ii','Q1(a)(ii)','5C',[24],[4],'2-2','co-ordinate-geometry-of-the-line','Plot and label the points P and Q on the co-ordinate diagram below. Hence, draw the line k.',['coordinates swapped.','Label/s missing'],line)
A('1-a-iii','Q1(a)(iii)','5C',[24],[4,5],'2-2','co-ordinate-geometry-of-the-line,geometry','O is the point (0,0). R is the point that makes OPQR a parallelogram. Draw the parallelogram OPQR on the diagram and write down the co-ordinates of the point R.',['Pilot Diagram','Correct coordinates based on an'],line)
A('1-b','Q1(b)','10C',[25],[5],'2-2','co-ordinate-geometry-of-the-line,area-volume','Find the area of the triangle with vertices A(2,0), B(2,4) and C(−3,3).',['Base or height identified.','Formula fully substituted.'])
normal='The finishing times for a cross country race were normally distributed with mean 13 minutes and standard deviation 1.5 minutes. Use the empirical rule and the diagram.'
A('2-a-i','Q2(a)(i)','10C',[26],[6],'1-7','statistics','Use the mean and standard deviation to fill in the missing numbers along the horizontal axis.',['One correct entry.','Two correct entries.'],normal)
A('2-a-ii','Q2(a)(ii)','5B',[26],[6],'1-7','statistics','What percentage of the runners who finished the race had a finishing time between 11.5 and 14.5 minutes?',['68%','empirical rule'],normal)
A('2-a-iii','Q2(a)(iii)','5B',[26],[6],'1-7','statistics','120 runners finished the race. Find the number of runners who finished the race in less than 10 minutes.',['Multiplies 120 by some probability.'],normal)
sprint='In a sprint final there are 8 finalists and 8 lanes. Each finalist is put in a different lane.'
A('2-b-i','Q2(b)(i)','5C',[26],[7],'1-1','counting','Find the number of possible ways the finalists could be arranged at the start line of the race.',['All terms listed but not multiplied.'],sprint)
A('2-b-ii','Q2(b)(ii)','5B',[26],[7],'1-1','counting','Find the number of possible ways that the top three places can be filled if only one person can finish first, one person can finish second, and one person can finish third.',['Terms listed but not multiplied.'],sprint)
circle='A circle c has centre (3,−1) and radius 2.'
A('3-a-i','Q3(a)(i)','10C',[27],[8],'2-2','co-ordinate-geometry-the-circle','Write down the equation of c.',['Equation with just one error.'],circle)
A('3-a-ii-iii','Q3(a)(ii),Q3(a)(iii)','10C',[27],[8],'2-4','co-ordinate-geometry-the-circle,geometry','The circle c and O(0,0) are shown. (ii) Circle s is the image of c by central symmetry through O. Work out the centre and radius of s and fill them into the table. (iii) Hence, construct s on the co-ordinate diagram.',['Centre or radius found.','Either (ii) or (iii) correct.'],circle)
A('3-b','Q3(b)','10C',[27],[9],'2-2','co-ordinate-geometry-the-circle,co-ordinate-geometry-of-the-line','Find the slope of [AB], and hence work out the slope of the tangent line l.',['Finds the slope of the radius.'],'Circle k has centre A(4,−2). B(7,2) is on the circle and is the point of contact for tangent l, as shown.')
A('4-a-i-ii','Q4(a)(i),Q4(a)(ii)','10D',[28],[10],'1-6','statistics','(i) Draw a histogram to represent the data. (ii) What is the greatest number of students that could have spent less than 15 hours on their phone in the last week?',['Three correct bars','Correct histogram'],'Aoife surveyed 80 students. Phone hours in the last week: 0–10, 10–20, 20–30, 30–40, 40–50; frequencies 12, 14, 26, 12, 16. Intervals include the lower bound but exclude the upper bound.')
venn='Aoife surveyed 80 students: 21 have neither social media account A nor B, and 43 have B. In the Venn diagram, p is A only and q is both A and B.'
A('4-b-i-ii','Q4(b)(i),Q4(b)(ii)','15D',[28],[11],'3-1','number-systems','(i) Work out p, the number who have A only. (ii) 30 students have an account on A or B only. Hence, or otherwise, find q, the number who have both.',['Work of merit in (i) AND (ii)','(i) OR (ii) correct'],venn)
A('4-b-iii','Q4(b)(iii)','5B',[28],[11],'1-2','probability','A student is chosen at random. What is the probability that the student has neither an account on A nor B?',['Either numerator or denominator'],venn)
chocolate='A chocolatier uses large rectangular blocks of chocolate. One block has dimensions 70 cm, 36 cm and 1.8 cm, as shown.'
A('5-a-i','Q5(a)(i)','5C',[29],[12],'3-4','area-volume','Show that the volume of the rectangular block of chocolate is 4536 cm³.',['Formula with some substitution.','Formula fully substituted.'],chocolate)
A('5-a-ii','Q5(a)(ii)','5B',[29],[12],'3-3','number-systems,area-volume','The weight of the block is 5 kg. Find the weight, in grams, of 1 cm³ of chocolate, correct to 1 decimal place.',['Converts 5 kg to grams.'],chocolate)
A('5-b-i-ii','Q5(b)(i),Q5(b)(ii)','10D',[29],[13],'3-4','area-volume','The chocolatier makes chocolate spheres of radius 1.6 cm. (i) Find the volume of one sphere, correct to 1 decimal place. (ii) Work out the number of complete spheres that can be made from the block of volume 4536 cm³.',['One part correct','Work of merit in both parts'])
A('5-b-iii','Q5(b)(iii)','10C',[29],[13],'3-4','area-volume','Edible paint covers the total surface area of a chocolate sphere of radius 1.6 cm. Work out its surface area, correct to 1 decimal place.',['Formula fully substituted.'])
A('6-a','Q6(a)','10C',[30],[14],'2-1','geometry-proofs-and-constructions','Construct the triangle ABC, where |BC| = 11 cm, |AB| = 7 cm and |AC| = 9 cm. [BC] is given.',['Correct triangle without arcs.','Pilot Diagram'])
similar='In the triangle XYZ shown, [UV] is parallel to [YZ]. |XU| = 4, |UY| = 7 and |VZ| = 8.4.'
A('6-b-i','Q6(b)(i)','10C',[30],[15],'2-1','geometry','Find |XV|, the distance from X to V.',['some relevant ratio stated.'],similar)
A('6-b-ii','Q6(b)(ii)','10D',[30],[15],'2-1','geometry-proofs-and-constructions','Show that triangles XYZ and XUV are similar. Give a reason for each statement you make.',['One equal pair of angles','Two equal pairs of angles','Reasons ignored'],similar)
scatter='Liam and Ava sell ice cream. Ava records daily temperature (°C) and daily ice cream sales (€) for 14 days. The scatterplot shows 12 days.'
A('7-a-i','Q7(a)(i)','10B',[31],[16],'1-7','statistics','Data for Day 1 and Day 2 are not plotted. Plot and label these points on the scatterplot: Day 1, 23°C and €500; Day 2, 17°C and €400.',['One point plotted correctly'],scatter)
A('7-a-ii','Q7(a)(ii)','10B',[31],[16,17],'1-7','statistics','Describe the relationship between daily temperature and daily ice cream sales.',['In general, as temperatures increase,','the daily ice cream sales increase.'],scatter)
A('7-a-iii','Q7(a)(iii)','5A',[31],[16,17],'1-7','statistics','Estimate which correlation coefficient best describes the relationship. Tick one box only: 0.2 / −0.8 / 0.8 / −0.2.',['Estimate of correlation coefficient:'],scatter)
A('7-a-iv','Q7(a)(iv)','5C',[31],[16,17],'1-7','statistics','Circle the outlier on the scatter graph and give a possible reason for this outlier.',['Circle outlier.','trend of the data.'],scatter)
sales='Daily ice cream sales (€) for Monday to Sunday are 618, 530, 446, 500, 400, 369 and 147.'
A('7-b-i','Q7(b)(i)','5C',[32],[18],'1-7','statistics','Work out the mean and standard deviation for these 7 days. Give your answer in euro, correct to 2 decimal places where necessary.',['Either mean or standard deviation'],sales)
A('7-b-ii','Q7(b)(ii)','5B',[32],[18],'1-7','statistics','What would happen to the standard deviation if Sunday’s value, 147, was omitted? Tick one box only: Increase / Decrease / Stay the same. Give a reason without calculating the new standard deviation.',['The data would be closer together','Mentions some measure of spread.'],sales)
vanilla='An ice cream company surveyed 320 randomly selected customers in 2024. 74 said vanilla was their favourite flavour.'
A('7-c-i-ii','Q7(c)(i),Q7(c)(ii)','5C',[32],[19],'1-7','statistics','(i) Work out the percentage who said vanilla was their favourite, to the nearest percent. (ii) Show that the margin of error for a population proportion is 5.6%, correct to 1 decimal place.',['a fraction of 320.','Either (i) or (ii) correct.'],vanilla)
A('7-c-iii','Q7(c)(iii)','5C',[32],[19],'1-7','statistics','In 2020 vanilla was the favourite flavour of 30% of customers. Use your answers to (c)(i) and (c)(ii) to test the claim that this percentage has changed since 2020, at the 5% level of significance. Show relevant calculations, state your conclusion and give a reason.',['Conclusion from correct work not in','context.'],vanilla)
pool='A swimming pool is a prism. Its side wall is rectangle ABCF joined to triangle CDE, with C on BD and E on CF. AB = 20 m, EF = 8 m, AF = 0.75 m and CD = 1.25 m, as shown.'
A('8-a-i','Q8(a)(i)','5B',[33],[20],'3-4','area-volume','Find |BD|, the total depth of the water at the deeper end of the pool.',['down one of the relevant measurements'],pool)
A('8-a-ii','Q8(a)(ii)','10C',[33],[20],'3-4','area-volume','Show that the area of the vertical side wall of the pool is 22.5 m².',['One relevant area calculated.','Both formulas substituted correctly.'],pool)
A('8-a-iii','Q8(a)(iii)','10C',[33],[21],'3-4','area-volume','The pool is 10 m wide and its vertical side-wall area is 22.5 m². Use the answer to (a)(ii) to find the volume of water in litres (1 m³ = 1000 litres).',['Volume correct','Convert to litres:'])
A('8-b-i-ii','Q8(b)(i),Q8(b)(ii)','10D',[34],[21],'3-4','area-volume','The floor of the swimming pool is to be tiled. (i) Each square tile has side 45 cm. Find its area in m². (ii) The floor area is 201 m². Work out the minimum number of tiles needed if 10% wastage is expected.',['One area correct','Both areas correct.'])
pump='A pump is a cylinder on top of another cylinder, as shown. The top cylinder has radius 22 cm and height 11 cm.'
A('8-c-i','Q8(c)(i)','5C',[34],[22],'3-4','area-volume','Show that the volume of the top cylinder is 5324π cm³.',['Formula fully substituted.'],pump)
A('8-c-ii','Q8(c)(ii)','10D',[34],[22],'3-4','area-volume','The bottom cylinder has three times the volume of the top cylinder and height 50 cm. Find its radius, correct to 1 decimal place.',['Finds the volume of the bottom cylinder.'],pump)
darts='Susan plays “Hit the bull”: she throws 3 darts at the bullseye. The probability of a hit with a single dart is 0.2, independently of previous throws.'
A('9-a-i','Q9(a)(i)','5C',[35],[23],'1-2','probability','Find the probability Susan does not hit the bullseye on a single throw.',['mention of 1.'],darts)
A('9-a-ii','Q9(a)(ii)','5C',[35],[23],'1-2','probability','Find the probability Susan hits the bullseye with her first dart and does not hit the bullseye with the other two darts.',['two relevant probabilities.'],darts)
A('9-a-iii','Q9(a)(iii)','10C',[35],[23],'1-3','probability','Susan gets 50 for each hit. The table gives scores 150, 100, 50, 0 with probabilities 0.008, 0.096, 0.384, 0.512. Work out her expected score for throwing 3 darts.',['correct but not evaluated.'],darts)
A('9-b-i','Q9(b)(i)','5B',[35],[24],'2-1','geometry','A circular dartboard is divided into 20 equal sectors as shown. Show that the measure of the angle of each sector is 18°.',['number of degrees in a full angle'])
A('9-b-ii','Q9(b)(ii)','10D',[36],[24],'3-4','area-volume','Two sectors have angle 18° and radii 99 mm and 107 mm. Work out the shaded area, the part of the larger sector not in the smaller sector, correct to the nearest mm².',['One error and finishes correctly'])
prime='U is the integers 1 to 20 on the dartboard. P is the set of prime numbers on the dartboard: P = {2, 3, 5, 7, 11, 13, 17, 19}.'
A('9-c-i','Q9(c)(i)','5C',[36],[25],'3-1','number-systems','List the elements of P′, the set of integers on the dartboard that are not prime.',['12 items required.','3 correct.','6 correct.','9 correct.'],prime)
A('9-c-ii','Q9(c)(ii)','5C',[36],[25],'3-1','number-systems','There are four solutions to the equation a + b = 20, where a, b ∈ P. List two solutions.',['Any two of:','One solution found'],prime)
A('9-c-iii','Q9(c)(iii)','5C',[36],[25],'1-7','statistics,number-systems','M is the median of P. Is M ∈ P or M ∈ P′? Tick one box only and use calculations to support your answer.',['Correct answer and one correct'],prime)
campus='The diagram (not to scale) shows a university campus ABCD. C, D and E are main doors; DC, DE and EC are pathways. DE = 80 m, EC = 41 m, EB = 9 m and angle DEC = 37°. A and B are right angles.'
A('10-a-i','Q10(a)(i)','10D',[37],[26],'2-3','trigonometry','Use triangle CEB and the Theorem of Pythagoras to work out |BC|, the distance from B to C.',['theorem of Pythagoras.','Correct answer without supporting work.'],campus)
A('10-a-ii','Q10(a)(ii)','5C',[37],[26],'2-3','trigonometry','Use triangle CEB to show that angle CEB = 77°, correct to the nearest degree.',['Demonstrates some understanding of sin,'],campus)
A('10-a-iii','Q10(a)(iii)','10D',[37],[26,27],'2-3','trigonometry','Use angle CEB = 77° to work out |AD|, the distance from A to D, correct to the nearest metre.',['Note: Accept candidates answer from part (ii).'],campus)
A('10-a-iv','Q10(a)(iv)','5C',[38],[26,27],'2-3','trigonometry,area-volume','Calculate the area of triangle CDE, correct to the nearest m².',['Area formula fully substituted.'],campus)
A('10-a-v','Q10(a)(v)','10C',[38],[26,27],'2-3','trigonometry','Use the cosine rule to work out |DC|, the distance from D to C, correct to 1 decimal place.',['Cosine formula fully substituted.'],campus)
A('10-b','Q10(b)','10C',[38],[28],'2-3','trigonometry','A university has a triangular flag as shown (not to scale). Use the sine rule to find angle θ, correct to 1 decimal place.',['Correct formula fully substituted.','Incorrect rounding'])
assert len(p.cards)==50
selection_review=[
 {'pages':[3,4,16],'wording':'any five / any three questions','classification':'exam-level-selection','reason':'Every offered question retained for practice.'},
 {'pages':[11],'wording':'or otherwise','classification':'method-choice','reason':'Alternative methods solve the same required task.'},
 {'pages':[17,18,25],'wording':'Tick one box only','classification':'answer-selection','reason':'All printed alternatives and required reasons stay together at the published allocation.'},
 {'pages':[25],'wording':'There are four solutions / List two solutions','classification':'answer-selection','reason':'One task selecting any two ordered solutions; original instruction and all four scheme solutions retained, without combination expansion.'},
]
def classify(c):
 t=c['context'].lower()
 if 'questions' in t and 'any' in t:return ('exam-level-selection','Exam choice; every offered question retained.')
 if 'or otherwise' in t:return ('method-choice','Alternative methods for one required task.')
 if 'one of these tiles' in t:return ('required-reference','Identical square tiles; one tile area is required, not a selectable question pool.')
 if 'solutions' in t:return ('answer-selection','Any two ordered solutions form one response, with all four scheme solutions retained.')
 if 'box' in t or 'tick' in t:return ('answer-selection','One card retains every printed choice and the required reasoning.')
 return None
if __name__=='__main__':p.write(selection_review,classify)
