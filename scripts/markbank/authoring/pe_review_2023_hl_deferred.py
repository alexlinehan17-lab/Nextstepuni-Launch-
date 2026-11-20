"""Independent visual sweep of all 44 paper and 28 scheme pages (2023 deferred sitting).

Written allocations: scheme PDF 4–26; 1–3 cover/notes, 27–28 blank/end matter.
The deferred scheme carries no project or performance pages. No finite printed
choice pools. Single-value scheme rows are all-or-nothing, as June encodes them.
Scheme misprints, each recorded in its task's guidance: Q4's lowest band 1–4
overlaps 4–6; Q6(b) says "frontal plane" against its own sagittal/frontal (a);
Q6(c)(ii) row says 2 marks, column 3 (1 + 3 = the 4 printed for (c));
Q13(b)(ii) grid labelled (iii); Q13(c) restates "boys and girls" though the
paper asks about boys only; Q16(a) grid labelled (a)(i); Q16(d)(i) row says
"method" for a type of feedback; Q17(b) prints 2 x 3(1+2) where its rows give
1 + 3 per system, which is what reaches the printed 8.
"""
YEAR=2023
SITTING='deferred'
PAPER_PAGE_COUNT=44
SCHEME_PAGE_COUNT=28
ACKNOWLEDGEMENT_PAGE=43
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


TASKS=[
('1a','1-6',[3],[4], 'Define gamesmanship.',
 [fixed('Definition',2,'Accurate definition of gamesmanship provided.')]),
('1b','1-6',[3],[4], 'Describe how gamesmanship could influence engagement in a physical activity of our choice.',
 [('Description',6,'Clear and accurate description of how gamesmanship can affect participation, with well-defined links to the chosen activity; may use examples: 5–6; accurate description of at least one influence gamesmanship can have on participation, with some link to the chosen activity: 3–4; one accurate description provided: 1–2.')]),
('2a','0-19',[4],[4], 'Identify two strategies that could be used by an official to manage conflict between participants.',
 [('Strategies',2,'One mark per accurately identified strategy used to manage conflict (2 × 1 mark).')]),
('2b','0-19',[4],[4], 'Outline two areas of safe practice that should be considered by an official in a physical activity of your choice.',
 repeat('Area of safe practice',2,3,'Clear outline of an area of safe practice that should be considered in the chosen activity: 3; area of safe practice identified: 1.',[0,1,3])),
('3a','1-2',[5],[5], 'Name four different methods of collecting data about physical activity participation.',
 [('Methods',2,'Any four appropriate methods of collecting information on physical activity participation: 2; one to three appropriate methods: 1.')]),
('3b','1-2',[5],[5], 'For three methods of collecting data about physical activity participation, correctly named in (a), outline what information they provide about physical activity participation.',
 [fixed(f'Method {i}',2,'Appropriate information the method provides about physical activity participation.') for i in (1,2,3)]),
('4','0-12',[6],[6], 'Discuss the role that sports drinks play in the performance of a marathon runner or another endurance athlete of your choice.',
 [('Discussion',8,'Accurate and detailed knowledge, with independent opinions and judgements supported by links to the demands of a marathon runner/other endurance athlete: 7–8; some accurate and detailed knowledge, briefly identifying advantages and drawbacks of consuming sports drinks, linked to the demands of an endurance athlete: 4–6; some accurate information on the use of sports drinks in endurance sports, not always linked to the athlete: 1–4. A misprint in the scheme: the lowest band is printed as 1–4, which overlaps the 4–6 band.')]),
('5a','0-9',[7],[7], 'What component of fitness does the vertical jump test measure?',
 [fixed('Component',2,'Performance related fitness component: power.')]),
('5b','0-7',[7],[7], 'State if the component of fitness, correctly named in (a), is a health related or performance related component of fitness.',
 [fixed('Classification',2,'Performance related component of fitness.')]),
('5c','0-7',[7],[7], 'Define the component of fitness correctly named in (a).',
 [fixed('Definition',2,'Accurate definition of power.')]),
('5d','0-9',[7],[7], 'Name another component of fitness and a test that is used to measure performance in it.',
 [fixed('Component',1,'Correct component of fitness, not power.'),fixed('Test',1,'Appropriate test for the named component.')]),
('6a','0-2',[8],[8], 'Name the plane and axis through which a performer moves when completing a forward somersault.',
 [fixed('Plane',1,'Sagittal.'),fixed('Axis',1,'Frontal.')]),
('6b','0-2',[8],[8], 'Provide one sporting example, other than a forward somersault, that moves through the same plane and axis.',
 [fixed('Example',2,'Any other correct movement in the same plane and axis. A misprint in the scheme: this row says the movement travels through the “frontal plane”, but the scheme’s own answer to 6(a) is the sagittal plane and the frontal axis, and the question asks for that same plane and axis.')]),
('6ci','0-2',[8],[8], 'What class of lever is found at the ankle joint?',
 [fixed('Lever class',1,'2nd class lever.')]),
('6cii','0-2',[8],[8], 'Give a sporting example of another named class of lever.',
 [fixed('Lever and sporting example',3,'A named class of lever other than 2nd class, with a sporting example. A misprint in the scheme: the row reads “Lever and sporting example – 2 marks”, but the marks column gives 3, and 6(c)’s printed 4 marks are reached only by 1 for (i) plus 3 for (ii). The scheme prints no split of the 3 marks.')]),
('7','1-22',[9],[8], 'Explain the term ‘social regulation of the body’ and how it might impact on participation in physical activity.',
 [('Explanation',8,'Accurate explanation of how social regulation of the body might impact on the participation of men and women in physical activity and sport: 6–8; accurate discussion of its impact on both men and women, some understanding of social regulation of the body, both sides may not be addressed in equal detail, links made to physical activity and sport: 3–5; little or no understanding of social regulation of the body, fails to consider both sides, limited or no links to physical activities: 1–2.')]),
('8a','1-25',[10],[9], 'What is sports marketing?',
 [fixed('Statement',2,'Any accurate statement of what sports marketing is.')]),
('8b','1-25',[10],[9], 'Discuss two ways that sports marketing could help develop tourism in Ireland.',
 repeat('Way',2,3,'Relevant and appropriate discussion of how sports marketing links to developing tourism in Ireland (it must be sports marketing): 3; accurate discussion: 1.',[0,1,3])),
('9','0-23',[11],[9], 'Compare the two physical activities diving and basketball in terms of aesthetic/artistic criteria.',
 [fixed('Diving',3,'Explanation of the role of artistic/aesthetic criteria of performance in diving.'),fixed('Basketball',3,'Explanation of the role of artistic/aesthetic criteria of performance in basketball.'),fixed('Comparison',2,'Comparison of the two activities in terms of the role of artistic/aesthetic criteria of performance.')]),
('10','1-24',[12],[10], 'Discuss two different types of messages that sports related advertising may give to young people.',
 repeat('Message',2,4,'Clear and accurate discussion of sports related advertising that explores the link between the form of advertising and the message given to young people: 4; limited but accurate discussion, with a limited link between the form of advertising and the message: 2.',[0,2,4])),
('11','0-10',[13],[10], 'Outline two periodisation phases/cycles you might use when planning for training in a physical activity of your choice.',
 repeat('Phase/cycle',2,4,'Clear and applicable, includes examples, an accurate reflection of the use of periodisation in the chosen activity: 4; some understanding of periodisation and how it applies to the chosen activity: 2.',[0,2,4])),
('12','1-6',[14],[11], 'Explain the importance of maintaining two principles of ethical practice in a physical activity of your choice.',
 repeat('Principle',2,4,'Accurate and detailed explanation of the principle with practical examples: 4; limited explanation, practical examples inaccurate or not provided: 2. Accept integrity, fairness, equity, respect.',[0,2,4])),
('13ai','1-24',[15,16,17],[12], 'The Lionesses are sponsored by Nike, Hello Fresh and Visa.\nDefine sponsorship.',
 [fixed('Definition',2,'Any accurate definition of sponsorship.')]),
('13aii','1-24',[15,16,17],[12], 'Describe two disadvantages that sponsorship can have for a physical activity of your choice.',
 [fixed(f'Disadvantage {i}',3,'Accurate description of a disadvantage of sponsorship on the chosen physical activity.') for i in (1,2)]),
('13bi','1-3',[15,16,18],[13], 'Outline two characteristics of a role model, or another significant person, who might encourage physical activity participation.',
 [fixed(f'Characteristic {i}',3,'Accurate outline of a characteristic of an appropriate person who might encourage participation; must be a significant person.') for i in (1,2)]),
('13bii','1-3',[15,16,18,19],[13], 'Role models can only do so much. Discuss two other supports to physical activity participation that may exist in the community. You may not refer to the support provided by role models/significant people in your answer.',
 [fixed(f'Support {i}',3,'Clear and accurate discussion of a support to participation that may exist in the community; must not refer to people. A misprint in the scheme: its grid labels this part (iii); it is 13(b)(ii).') for i in (1,2)]),
('13c','1-22',[15,16,20],[13], 'Discuss two influences on the participation patterns of boys in physical activity/sport.',
 repeat('Influence',2,4,'Clear and applicable discussion that refers clearly to participation patterns, links influences clearly and includes examples: 4; limited discussion of participation patterns, poor/limited links with influences, may not include examples: 2. A misprint in the scheme: it restates the question as “boys and girls” and its 4-mark band asks for examples for both boys and girls, but the paper asks only about boys.',[0,2,4])),
('13d','1-22',[15,16,21],[14], 'Explain why the characteristics associated with hegemonic femininity might impact on female participation in soccer, or another physical activity of your choice.',
 [('Explanation',10,'Accurately explains hegemonic femininity, identifies two or more of its characteristics, clear links between accurate characteristics and participation impacts, good use of examples in the chosen activity: 8–10; accurately explains hegemonic femininity, identifies at least one characteristic, limited links between characteristics and impact on participation, may use examples: 5–7; explains hegemonic femininity with a poor/limited explanation of how it may affect participation rates: 1–4.')]),
('13e','1-21',[15,16,22],[15], 'Examine how media representations of the body may impact on both young men’s and young women’s participation in physical activity and sport.',
 [('Examination',12,'At least two clear examples of how media representations of the body could impact participation; looks at both young men’s and young women’s participation; clear, accurate links to participation rates in both groups; clear examples; each point linked to participation; positives and negatives highlighted; judgement provided and justified: 10–12. At least two examples, both groups, clear links, examples, some points linked to participation: 7–9. Some examples, both groups, some relevant examples and some links to participation: 4–6. One example, looking at either men’s or women’s participation: 1–3.')]),
('14ai','1-9',[23],[16], 'World Athletics said Kipsang, a bronze medallist at the 2012 Olympics, had four whereabouts failures between April 2018 and May 2019. Three such failures within 12 months leads to an automatic ban.\nOther than whereabouts failures name three Irish anti-doping rule violations.',
 [fixed(f'Violation {i}',2,'Accurate Irish anti-doping rule violation. The question excludes whereabouts failures.') for i in (1,2,3)]),
('14aii','1-8',[23],[16], 'Outline one implication for the athlete and one implication for the activity of using Performance Enhancing Drugs (PEDs).',
 [fixed('Implication for athlete',3,'One valid implication for the athlete clearly outlined.'),fixed('Implication for activity',3,'One valid implication for the activity clearly outlined.')]),
('14b','1-10',[24],[16], 'Name two dietary supplements and explain how an athlete could use both of these dietary supplements to optimise their performance.',
 [('Supplements named',2,'One mark per named supplement (2 × (1 + 3)).')]+[fixed(f'Explanation {i}',3,'Explanation of how the supplement can be used to optimise performance.') for i in (1,2)]),
('14c','0-10',[25],[17], 'Apply the FITT formula to two health related components of fitness.',
 repeat('Component',2,4,'One mark each for frequency, intensity, time and type, each explained in terms of the chosen component of fitness (2 × 4 × 1 mark).')),
('14d','0-10',[26],[17], 'When planning to improve performance and avoid injuries it is important to take into consideration the principles of training. Name three principles of training and outline one specific example of how each of these principles can be used to train for improvement in performance in a physical activity of your choice. You may not use recovery in your answer.',
 [('Principles',3,'One mark per correct principle of training (3 × (1 + 3)). Recovery is not accepted.')]+[fixed(f'Example {i}',3,'Clearly outlined example of how the principle of training can be used to train for improvement in performance.') for i in (1,2,3)]),
('15a','1-2',[27],[18], 'Explain the following concepts of physical activity:\nMass participation sports\nLeisure and Recreation\nSport',
 [fixed(concept,2,f'Accurate definition of {concept.lower()}.') for concept in ('Mass participation sports','Leisure and Recreation','Sport')]),
('15b','1-25',[28],[18], 'State two reasons why mass participation sporting events have experienced growth in recent years and explain the opportunities that this growth may have provided for businesses.',
 [('Reasons',2,'State 1st reason: 1 mark; state 2nd reason: 1 mark.'),('Explanation of opportunities',8,'Clear and applicable explanation that refers clearly to the opportunities the growth has provided for businesses and includes examples: 6–8; limited explanation, poor/limited links to the opportunities for businesses, may not include examples: 1–5.')]),
('15c','1-24',[29],[19], 'Discuss the impacts that both endorsement and merchandising can have on sports performers.',
 [(concept,6,'Explains the concept clearly and accurately, explores how it can impact on sports performers, gives positive and negative impacts, a justified opinion and examples: 4–6; explains the concept accurately and looks at the impact on sports performers, opinion may not be provided and may not include examples: 1–3.') for concept in ('Endorsement','Merchandising')]),
('15d','1-25',[30],[19], 'Examine the impacts that involvement with a named business may have on a sport of your choice.',
 [('Examination',12,'Detailed impacts that involvement with the named business has had on the named sport, positive and negative impacts, and a justified opinion: 10–12; detailed impacts with positive and negative impacts: 7–9; detailed impacts, opinion may not be provided, only positive or negative impacts, not both: 4–6; brief discussion around the business and the sport/event: 1–3.')]),
('16a','0-11',[31],[20], 'Goal setting can be used as a strategy to improve an athlete’s motivation. Name and explain two other strategies that a coach could use to improve an athlete’s motivation.',
 [('Strategies named',2,'One mark per accurate strategy for improving motivation (2 × (1 + 3)). The question excludes goal setting. A misprint in the scheme: its grid labels this part (a)(i); the paper’s 16(a) has no sub-parts.')]+[fixed(f'Explanation {i}',3,'Accurate explanation of the named strategy.') for i in (1,2)]),
('16b','0-18',[32],[20], 'Explain how a coach/choreographer might guide a performers effective use of ongoing reflection about their performance. Use two examples from a physical activity of your choice to support your answer.',
 [('Examples',2,'One mark per example of how the coach/choreographer might guide reflection (2 × (1 + 3)).')]+[fixed(f'Explanation {i}',3,'Explanation of how the coach/choreographer may use the example to guide the performer’s ongoing reflection about performance.') for i in (1,2)]),
('16ci','0-22',[33],[20], 'A coach might use video analysis to assist them in identifying weaknesses in opponents.\nIdentify four other methods of analysing performance.',
 [('Methods',4,'One mark per correct analysis method identified (4 × 1 mark). The question excludes video analysis.')]),
('16cii','0-22',[33],[20], 'Give an example of what aspect of performance two of the methods, correctly identified in (i), could be used to analyse. Justify your answer.',
 [('Examples',2,'One mark per accurate example of an aspect of performance the method could analyse (2 × (1 + 3)).')]+[fixed(f'Justification {i}',3,'Valid justification.') for i in (1,2)]),
('16di','0-3',[34],[21], 'As well as using methods of analysis and choosing strategies, a coach should be able to provide the appropriate feedback to their athletes. Identify four different types of feedback that a coach could use.',
 [('Types of feedback',4,'One mark per valid type of feedback identified (4 × 1 mark). A misprint in the scheme: the row reads “Valid method identified”; the question asks for types of feedback.')]),
('16dii','0-3',[34],[21], 'Discuss the importance of two of these types of feedback, correctly named in (i), for a physical activity of your choice.',
 repeat('Feedback type',2,4,'Clear discussion that links back to the physical activity, covers the importance of the feedback to the activity and looks at pros and cons: 3–4; limited discussion: 1–2.')),
('17ai','0-11',[35],[22], 'Mageean explains how having confidence in her ability helped her bounce back after injury.\nDefine confidence.',
 [fixed('Definition',2,'Accurate definition of confidence.')]),
('17aii','0-11',[35],[22], 'Discuss how confidence can impact on practice/training in a physical activity of your choice.',
 [('Discussion',8,'Clear and accurate discussion of how confidence in one’s ability leads to better decision making and so better performance; positives and negatives; how feedback from coaches can help confidence; reflective practice; intrinsic and extrinsic motivation to practice/training; how self-confidence and resilience can help athletes improve; includes examples: 7–8. Brief discussion of how confidence leads to better decision making and performance, positives and negatives, coach feedback, an example: 4–6. Limited discussion of how confidence leads to better decision making and performance, coach feedback, may not include examples: 1–3.')]),
('17b','0-12',[36],[23], 'Performance in middle distance running is dependant on more than one energy system. Name and explain two energy systems.',
 [('Energy systems named',2,'One mark per correctly named energy system. ATP-PC/alactic anaerobic/phosphagen; lactic acid/anaerobic glycolysis; aerobic/oxidative.')]+[fixed(f'Explanation {i}',3,'Accurate explanation of the energy system. A misprint in the scheme: the grid’s heading gives two marks for each explanation, but its rows give three, and only three for each explanation reaches the total printed for 17(b).') for i in (1,2)]),
('17c','0-12',[37],[23], 'Explain how an athlete could plan their recovery based on the energy systems used during performance. At least two energy systems must be referred to in your answer. You may not use nutrition in your answer.',
 repeat('Energy system',2,5,'Two energy systems referred to, linking fuel and time to recovery. Accurate explanation of how planning can aid recovery: 5; explains recovery with limited links to energy systems: 3. Nutrition is excluded by the question.',[0,3,5])),
('17d','0-12',[38],[24], 'Examine how an understanding of the energy systems can inform nutritional preparation for performance. Refer to before during and after performance nutrition in your answer.',
 [('Examination',12,'Must refer to before, during and after performance nutrition. Explains clearly how understanding the energy system can inform nutritional preparation, clearly links energy system to fuel and nutrition, refers to before, during and after, includes examples, explores the impact on performance and gives a justified opinion: 10–12; some accuracy, some links to fuel and nutrition, refers to before, during and after, includes examples: 7–9; basic knowledge, refers to two of before, during and after, reference to fuel only: 4–6; little understanding, refers to one of before, during and after: 1–3.')]),
('18a','0-7',[39],[25], 'Define four named performance related components of fitness.',
 [('Components named',4,'One mark per correctly named performance related fitness component (4 × (1 + 2)).')]+[fixed(f'Definition {i}',2,'Accurate definition of the component.') for i in (1,2,3,4)]),
('18b','0-9',[39],[25], 'Complete the table below in relation to the four performance related components of fitness correctly named in (a).\nComponent of performance related fitness\nFitness test\nTraining method for enhancing performance',
 [(f'Component {i}',2,'Appropriate fitness test for the component: 1 mark; suitable training method for the component: 1 mark.') for i in (1,2,3,4)]),
('18ci','0-2',[40],[25], 'Newtons laws of motion can aid understanding of skill performance.\nDefine Newton’s 1st and 2nd laws of motion.',
 [fixed('Newton’s 1st law',2,'Accurate definition of Newton’s 1st law of motion.'),fixed('Newton’s 2nd law',2,'Accurate definition of Newton’s 2nd law of motion.')]),
('18cii','0-2',[40],[25], 'Apply Newton’s 1st and 2nd laws of motion to the performance of a sports skill of your choice.',
 [fixed('Newton’s 1st law applied',3,'Accurate application of Newton’s 1st law of motion to the performance of the chosen skill.'),fixed('Newton’s 2nd law applied',3,'Accurate application of Newton’s 2nd law of motion to the performance of the chosen skill.')]),
('18d','0-1',[41],[26], 'Discuss the impact that creative application of skill can have on the effectiveness of performance in a physical activity of your choice.',
 [('Discussion',10,'Clear and applicable discussion linking the creative application of skill to effectiveness of performance with examples from the chosen activity, justified opinions, pros and cons, links back to the activity: 8–10; clear discussion with links, may use examples, links back to the activity, pros and cons not looked at: 5–7; brief discussion linking back to the activity, pros and cons not looked at: 1–4.')]),
]

CASE='Read the case study “From being banned to breaking barriers - how much has changed in 100 years” on pages 15–16, with Figure 9 (the Lionesses celebrating), Figure 10 (the Euro 2022 final attendance board) and Figure 11 (match action), before answering this part.'
FIG12=' Figure 12 on page 18 shows a young girl being inspired by the Lionesses’ victory.'
KIPSANG='Question 14(a) opens with a World Athletics report on page 23: Kipsang, a 2012 Olympic bronze medallist, had four whereabouts failures between April 2018 and May 2019.'
MAGEEAN='Figure 14 on page 35 shows Ciara Mageean celebrating her 2022 European 1500m silver medal, beside her quote on coming back from injury and mental resilience.'
CONTEXT={
 '1b':'Define gamesmanship as requested in 1(a). This part asks how gamesmanship could influence engagement in a physical activity you choose.',
 '2a':'Figure 1 on page 4 is a photograph of a referee among players during a soccer match.',
 '2b':'Figure 1 on page 4 is a photograph of a referee among players during a soccer match.',
 '3b':'Name four methods of collecting data about physical activity participation as requested in 3(a). Outline the information provided by three of those same methods.',
 '4':'Figure 2 on page 6 shows marathon runners taking drinks from volunteers along the course.',
 '5a':'Figure 3 on page 7 shows an athlete performing the vertical jump test against a wall-mounted measure.',
 '5b':'Part 5(a) asks what component of fitness the vertical jump test (Figure 3, page 7) measures. Classify that same component.',
 '5c':'Part 5(a) asks what component of fitness the vertical jump test (Figure 3, page 7) measures. Define that same component.',
 '5d':'Part 5(a) asks what component of fitness the vertical jump test (Figure 3, page 7) measures. Name a different component here.',
 '6a':'Figure 4 on page 8 is a drawing of a performer completing a forward somersault, from take-off to landing.',
 '6b':'Figure 4 on page 8 is a drawing of a forward somersault. Part 6(a) asks for its plane and axis; give a different movement in that same plane and axis.',
 '6cii':'Part 6(c)(i) asks what class of lever is found at the ankle joint. Use a different class of lever for this part.',
 '9':'Figure 5 on page 11 shows two synchronised divers in mid-dive; Figure 6 shows a basketball player in mid-air at the basket in front of a crowd.',
 '10':'Figure 7 on page 12 is the Irish Life Dublin Marathon 2022 logo; Figure 8 is a Coca-Cola bottle with Tokyo 2020 Olympic branding.',
 '13ai':CASE,
 '13aii':'Question 13(a) states that the Lionesses are sponsored by Nike, Hello Fresh and Visa. '+CASE,
 '13bi':CASE+FIG12,
 '13bii':'Part 13(b)(i) asks for characteristics of a role model, or another significant person, who might encourage participation. '+CASE+FIG12,
 '13c':CASE,
 '13d':CASE,
 '13e':CASE,
 '14ai':'The World Athletics report printed in the box on page 23 concerns whereabouts failures.',
 '14aii':KIPSANG,
 '14b':'Figure 13 on page 24 is a photograph of assorted supplement tablets and capsules.',
 '16cii':'Identify four methods of analysing performance other than video analysis as requested in 16(c)(i). Give examples for two of those same methods.',
 '16dii':'Identify four types of feedback as requested in 16(d)(i). Discuss two of those same types.',
 '17ai':MAGEEAN,
 '17aii':MAGEEAN+' Question 17(a) notes that confidence in her ability helped her bounce back after injury.',
 '17b':MAGEEAN,
 '18b':'Define four named performance related components of fitness as requested in 18(a). Complete one table row, with a fitness test and a training method, for each of those same components.',
 '18cii':'Define Newton’s 1st and 2nd laws of motion as requested in 18(c)(i), then apply both to a sports skill you choose.',
}

CHOICES={}
SOURCE_POOLS={}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any 10'],[2,'any three'],[2,'or'],[3,'any 10'],[6,'or'],[7,'or'],[15,'or'],[18,'or'],[21,'or'],[23,'any three'],[44,'or'],[44,'or']]
SELECTION_REVIEW=[
 {'pages':[2,3,23],'kind':'exam-attempt-rule','reason':'Any 10 of the 12 Section A questions and any three of the five Section C questions are examination attempt rules. Every question and every separately priced part is represented; no compound exam-attempt cards.'},
 {'pages':[2,15,44],'kind':'context-or-boilerplate','reason':'Blue or black pen, “men’s or women’s” in the case-study text (the record attendance for any Euro fixture), and copyright wording are not task routes.'},
 {'pages':[6,18,21],'kind':'open-choice-or-own-response','reason':'A marathon runner or another endurance athlete, a role model or another significant person, and soccer or another physical activity are open candidate choices, not finite printed pools.'},
 {'pages':[7],'kind':'answer-selection','reason':'Health related or performance related is the response to 5(b), not an alternative question route.'},
]

# Supplemental raw scan for printed-pool wording without a choose/select verb.
EXPECTED_POOL_SCAN=[[2,'10 of'],[2,'three of'],[33,'two of'],[34,'two of']]

SELECTION_REVIEW.append({'pages':[2],'kind':'exam-attempt-rule','reason':'“10 of” and “three of” on page 2 are the same Section A and Section C attempt rules.'})
SELECTION_REVIEW.append({'pages':[5,33,34],'kind':'own-response-selection','reason':'3(b) takes three of the candidate’s own four methods from 3(a); 16(c)(ii) takes two of the candidate’s own methods from 16(c)(i); 16(d)(ii) takes two of the candidate’s own types of feedback from 16(d)(i). No printed pool; no alternative-route expansion.'})
SELECTION_REVIEW.append({'pages':[27,39,40],'kind':'required-headings','reason':'All three concepts in 15(a), every row and column of the 18(b) table, and both of Newton’s 1st and 2nd laws in 18(c) are compulsory response components.'})

# Additional Topic Atlas headings, decided from the SEC paper, scheme and NCCA
# specification. Q16(d) asks for four types of feedback and the importance of
# two of them; NCCA LCPE 2.7 Psychological preparation lists "different types
# of feedback" (same decision as June 2020 HL Q4 and June 2025 HL Q2).
# Q18(b) gives half its marks to a training method for each component; that
# is Designing a fitness plan (2.6), filed beside the fitness-test topic.
ATLAS_TOPIC_ADDITIONS={
 '16di':['physical-education-higher-2-psychological-demands-of-performance'],
 '16dii':['physical-education-higher-2-psychological-demands-of-performance'],
 '18b':['physical-education-higher-2-physicalpsychological-demands-of-performance-training-methods-and-fitness-planning'],
}
