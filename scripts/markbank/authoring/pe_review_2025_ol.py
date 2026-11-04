"""Independent visual sweep: all 36 paper pages and 52 scheme pages.
Written scheme 4–28; project 30–40; performance 42–50; other pages
introductory/blank/end matter. Eight independently scored cloze blanks retain
the whole passage. Descending 3+3+2 answers remain a single eight-mark task.
Q15(c)'s six-group pool carries into both (i) and (ii).
"""
PAPER_PAGE_COUNT=36
SCHEME_PAGE_COUNT=52
ACKNOWLEDGEMENT_PAGE=35
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


def descending(label,guidance):
    return [(label,8,guidance+' Three correct responses: 8; two: 6; one: 3.',[0,3,6,8])]


TASKS=[]
PART_REF_OVERRIDES={}
CONTEXT={}
for i,(statement,answer) in enumerate([
    ('Carbohydrates are the body’s main source of energy.','True'),
    ('All fats are bad for your health.','False'),
    ('Protein is only important for building muscle.','False'),
    ('You should only drink water during exercise.','False'),
],1):
    part='1' if i==1 else f'1-statement-{i}'
    PART_REF_OVERRIDES[part]=f'Q1 · statement {i}'
    TASKS.append((part,'0-12',[3],[4],f'Is this statement true or false? {statement}',[fixed('Correct answer',2,answer+'.')]))
TASKS += [
('2a','0-10',[3],[4],'Outline why a cool-down is performed after physical activity.',
 [('Reason',4,'Clear and accurate reason: 4; somewhat clear and accurate: 2.',[0,2,4])]),
('2b','0-10',[3],[4],'Name two different activities suitable for a cool-down.',
 [fixed(f'Activity {i}',2,'Appropriate activity for a cool-down.') for i in (1,2)]),
('3','1-1',[4],[5],'Describe two benefits of physical activity for children.',
 repeat('Benefit',2,4,'Clear and accurate description: 4; somewhat clear and accurate: 2.',[0,2,4])),
('4','1-18',[4],[5],'During the Paris Olympics, RTÉ Sport showed coverage of different physical activities. Identify three characteristics that give a physical activity media or spectator appeal.',
 descending('Three characteristics','The scheme awards 3+3+2 for correct characteristics.')),
]
TERMS='Anti-Doping Rule Violation; Performance-enhancing drug; Therapeutic Use Exemption; Code of ethics.'
for i,(explanation,answer,topic) in enumerate([
 ('An athlete being allowed to take a drug that is not normally allowed in their sport because they suffer from a particular medical condition.','Therapeutic Use Exemption','1-9'),
 ('A substance that is used without permission specifically to improve sports performance.','Performance-enhancing drug','1-8'),
 ('A set of rules about appropriate behaviour.','Code of ethics','1-7'),
 ('Use or attempted use by an athlete of a prohibited substance or a prohibited method.','Anti-Doping Rule Violation','1-9'),
],1):
    part='5' if i==1 else f'5-row-{i}'
    PART_REF_OVERRIDES[part]=f'Q5 · row {i}'
    TASKS.append((part,topic,[5],[6],f'Match this explanation to the correct term: {explanation}\n\nTerms: {TERMS}',[fixed('Correct term',2,answer+'.')]))
for i,(statement,answer) in enumerate([
 ('The total distance of a marathon is 42 kilometres.','Scalar'),
 ('A basketball player ran 5 metres per second towards the basket.','Vector'),
 ('A tennis player served the ball with maximum force over the net.','Vector'),
 ('A hurling match lasts 70 minutes.','Scalar'),
],1):
    part='6' if i==1 else f'6-statement-{i}'
    PART_REF_OVERRIDES[part]=f'Q6 · statement {i}'
    TASKS.append((part,'0-2',[5],[6],f'Does this statement describe a vector or a scalar? {statement}',[fixed('Correct classification',2,answer+'.')]))
TASKS += [
('7a','1-11',[6],[7],'Is the statement about South American and European soccer players an example of discrimination, prejudice, stereotyping or inclusion?',
 [fixed('Classification',2,'Stereotyping or prejudice.')]),
('7b','1-11',[6],[7],'Explain your classification of the statement in Question 7(a).',
 [('Explanation',6,'Clear and accurate explanation: 6; accurate: 4; vaguely accurate: 2.',[0,2,4,6])]),
('8a','1-0',[6],[8],'White water rafting is an example of outdoor and adventure activities. Name one other physical activity that is an outdoor and adventure activity.',
 [fixed('Activity',2,'Appropriate outdoor/adventure activity other than white water rafting.')]),
('8b','1-0',[6],[8],'Outdoor and adventure activities is a concept of physical activity. Explain outdoor and adventure activities.',
 [('Explanation',4,'Clear and accurate explanation: 3–4; vaguely accurate: 1–2.')]),
('8c','1-0',[6],[8],'Name a different concept of physical activity, other than outdoor and adventure activities.',
 [('Concept',2,'A different correct concept: 1–2.')]),
('9a','1-6',[7],[9],'Explain sportsmanship.',
 [('Explanation',4,'Clear and accurate explanation: 3–4; vaguely accurate: 1–2.')]),
('9b','1-6',[7],[9],'Outline an example of sportsmanship in a named physical activity of your choice.',
 [('Example',4,'Accurate example: 4; vaguely accurate: 2.',[0,2,4])]),
('10','0-3',[7],[9],'Match the three unanswered explanations to the correct skill practice method.\n\nMethods: Distributed; Fixed; Variable; Massed.\n\nGiven example: Practising tackles in rugby, without a break → Massed.\n\n1. Run a sprint, rest, receive feedback, repeat.\n2. Serve in volleyball, repeatedly, environment remains the same.\n3. Small sided game, allowing athlete to adapt technique in a changing situation.',
 descending('Three matches','1 Distributed; 2 Fixed; 3 Variable. The given Massed example earns no additional marks.')),
('11','0-19',[8],[10],'A basketball referee uses hand signals to communicate to the teams. Outline three other effective communication skills.',
 descending('Three skills','Three appropriate communication skills other than hand signals.')),
('12','1-17',[9],[10],'Figure 3 shows a coach using a stop watch to help run the session. Name and explain two different types of technology and how a coach might use them in training.',
 [fixed(f'Technology {i}',2,'Appropriate technology named.') for i in (1,2)]+[fixed(f'Use {i}',2,'Correct explanation of how a coach might use the corresponding technology in training.') for i in (1,2)]),
('13ai','0-7',[10,11],[11],'From the case study, identify three performance-related components of fitness.',
 [fixed(x,2,'Correct performance-related component identified from the case study.') for x in ('Speed','Power','Coordination')]),
('13aii','0-9',[10,11],[11],'Name and describe a fitness test for any one of the performance-related components of fitness identified by you in Question 13(a)(i). You may draw a diagram if you wish.',
 [fixed('Fitness test',2,'Appropriate test for the selected performance-related component.'),('Description',4,'Accurate description with setup, measurement and procedures: 4; vaguely accurate: 2.',[0,2,4])]),
('13bi','0-2',[10,12],[12],'Name the plane and axis that a hammer thrower moves in when they rotate in the circle.',
 [fixed('Plane',2,'Transverse.'),fixed('Axis',2,'Vertical / longitudinal.')]),
('13bii','0-2',[10,12],[12],'In a named physical activity of your choice, identify a sporting movement that occurs through a different plane and axis of movement from Question 13(b)(i). Explain why the movement is in that plane and axis.',
 [fixed('Movement',2,'Appropriate sporting movement in a different plane and axis from transverse/vertical.'),('Explanation',4,'Accurate explanation in the named activity: 3–4; some relevant explanation: 1–2.')]),
('13c','0-3',[10,12],[12],'Using three examples from the case study, identify what stage of skill learning Nicola Tuthill is at in the sport of hammer throw.',
 [fixed('Stage',2,'Autonomous stage.')]+[fixed(f'Case-study example {i}',2,'Appropriate evidence from the case study supporting this stage of skill learning.') for i in range(1,4)]),
('13di','1-3',[10,13],[13],'From the case study, name the National Governing Body that governs the hammer throw.',
 [fixed('NGB',2,'Athletics Ireland.')]),
('13dii','1-3',[10,13],[13],'Suggest three ways that a National Governing Body can promote physical activity at a local level.',
 descending('Three ways','Appropriate ways for an NGB to promote local physical activity.')),
('13ei','1-13',[10,14],[14],'The nearest hammer throwing cage was far away. From the case study, identify one way this barrier was addressed by Nicola and her family.',
 [fixed('Barrier addressed',2,'Her father built a hammer throwing cage at home on the family farm.')]),
('13eii','1-12',[10,14],[14],'From the case study, describe three supports that have helped Nicola become involved in athletics and achieve her current titles and records in the hammer throw event.',
 descending('Three supports','Appropriate supports described from the case study: family, neighbour/coaches, college/academy or foundation support.')),
('14ai','0-6',[15],[15],'Define flexibility.',
 [('Definition',4,'Accurate: 4; somewhat accurate: 2.',[0,2,4])]),
('14aii','0-8',[15],[15],'Why is flexibility important for a tennis player?',
 [('Importance',4,'Clear and accurate explanation specific to tennis: 4; vaguely accurate: 2.',[0,2,4])]),
('14bi','0-12',[16],[16],'Name two nutrients. Give an example of the type of food that will provide each nutrient.',
 [fixed(f'Nutrient {i}',2,'Correct nutrient.') for i in (1,2)]+[fixed(f'Food source {i}',2,'Correct food source for the corresponding nutrient.') for i in (1,2)]),
('14bii','0-12',[16],[16],'Give a reason why an athlete would eat one of the nutrients named by you in Question 14(b)(i).',
 [('Reason',4,'Accurate reason for the chosen nutrient: 4; vaguely accurate: 2.',[0,2,4])]),
('14biii','0-12',[16],[16],'List two side effects of dehydration.',
 repeat('Side effect',2,2,'Appropriate side effect: 1–2.')),
('14ci','1-15',[17],[17],'How can equipment be adapted for an athlete with a disability, in a named physical activity of your choice? You cannot use racquet size.',
 [('Adaptation',4,'Clear and accurate adaptation: 4; somewhat clear and accurate: 2. Racquet size is excluded.',[0,2,4])]),
('14cii','1-15',[17],[17],'Identify two other adaptations that can be made to a physical activity so that people with a disability can participate.',
 [fixed(f'Adaptation {i}',2,'Appropriate additional adaptation, different from the equipment adaptation in 14(c)(i).') for i in (1,2)]),
('14d','0-19',[18],[18],'Describe two roles of an official. Support your answer with examples from physical activities.',
 repeat('Role',2,4,'Clear and accurate description with examples: 4; vaguely accurate: 2.',[0,2,4])),
('15a','0-17',[19],[19],'List three rules of a named physical activity of your choice.',
 [fixed(f'Rule {i}',3,'Correct rule of the named activity.') for i in range(1,4)]),
('15bi','0-3',[19],[19],'What type of feedback is Rhys McClenaghan talking about in the statement?',
 [fixed('Feedback',2,'Intrinsic feedback.')]),
('15bii','0-3',[19],[19],'Explain this feedback type and how it can help an athlete prepare for performance.',
 [('Explanation',4,'Accurate explanation of intrinsic feedback and how it supports preparation: 4; somewhat accurate: 2.',[0,2,4])]),
('15biii','0-11',[19,20],[19],'Describe two psychological factors that can affect an athlete’s performance.',
 repeat('Factor',2,4,'Factor described: 3–4; some relevant information: 1–2.')),
('15biv','0-11',[19,20],[20],'Explain two ways an athlete can mentally prepare for performance.',
 repeat('Preparation',2,4,'Accurate explanation: 4; somewhat accurate: 2.',[0,2,4])),
('15ci','1-14',[21],[20],'On the timeline below, identify three major developments that have occurred in the last 20 years for one of the following groups:\n• Women\n• Older Adults\n• People with physical disability\n• People with intellectual disability\n• Different ethnic groups\n• Different socio-economic groups',
 [fixed('Three developments',1,'Three major developments for the selected group. The published allocation is one mark in total for this timeline task.')]),
('15cii','1-14',[21,22],[20],'Describe one of the developments you identified in Question 15(c)(i) and outline the impact it has had for the group you have chosen.',
 [('Development and impact',8,'Development described with impact: 6–8; development described with vague impact: 3–5; development identified without impact: 1–2.')]),
('16ai','1-2',[23],[21],'Suggest two methods that might have been used to collect the data shown in Figure 9.',
 [fixed(f'Method {i}',2,'Appropriate method to collect the school participation data.') for i in (1,2)]),
('16aii','1-2',[23],[21],'Give a possible reason why 64% of students play Gaelic games but only 2% go swimming.',
 [fixed('Reason',4,'A clear, accurate possible reason based on school/location context. The scheme prints 4 marks; its second description has no numeric partial score.')]),
('16aiii','1-2',[23,24],[21],'Discuss why there is a change in the participation levels of year groups (Result 3 in Figure 9).',
 [('Discussion',8,'Clear and detailed discussion of the first-to-sixth-year change and reasons: 6–8; some discussion: 3–5; limited discussion: 1–2.')]),
('16aiv','1-3',[23,24],[22],'Describe two ways a school can help increase participation levels in physical activity.',
 repeat('Way',2,4,'Clear and accurate description: 4; somewhat clear and accurate: 2.',[0,2,4])),
('16bi','0-14',[25],[22],'Explain, using an example, what a strategy is, in a named physical activity of your choice.',
 [('Strategy',4,'Clear and accurate explanation with an example: 4; vaguely accurate: 2.',[0,2,4])]),
('16bii','0-14',[25],[22],'Outline why you might have to make a change to your strategy in Question 16(b)(i) and suggest a possible change to that strategy.',
 [('Change',4,'Clear and accurate reason and suggested change: 4; vaguely accurate: 2.',[0,2,4])]),
('16c','0-1',[26],[23],'“Taylor has great natural ability” – overheard on the sideline of an U10 match. Can someone succeed with just ability? Explain your answer.',
 [('Explanation',8,'Clear and accurate explanation: 6–8; accurate explanation: 3–5; limited explanation: 1–2.')]),
('17ai','0-22',[27],[24],'Identify an appropriate method to analyse each aspect of performance: health-related fitness; psychological preparedness.',
 [fixed('Health-related fitness',2,'Appropriate analysis method.'),fixed('Psychological preparedness',2,'Appropriate analysis method.')]),
('17aii','0-22',[27],[24],'Explain how you would analyse your performance using one of the methods identified by you in Question 17(a)(i).',
 [('Method',4,'Clear and accurate explanation of the selected method: 4; somewhat clear and accurate: 2. The paper refers to 17(a)(i); the scheme’s 17(b)(i) reference is a typo.',[0,2,4])]),
('17aiii','0-22',[27],[24],'Outline two reasons why it can be helpful to compare your performance to that of a more skilled performer.',
 repeat('Reason',2,3,'Reason outlined: 3; limited information: 1–2.')),
('17bi','1-22',[28],[25],'Give an example of a gender stereotype in sport.',
 [fixed('Example',2,'Appropriate gender stereotype in sport.')]),
('17bii','1-21',[28],[25],'Outline how the media can contribute to gender stereotypes of men and women in sport.',
 [('Contribution',6,'Outline of media contribution: 4–6; limited information: 1–3.')]),
('17biii','1-18',[28,29],[25],'RTÉ shows Gaelic games for free. GAAGO is pay-per-view TV. Describe one advantage and one disadvantage of media coverage like those named above, in a named physical activity of your choice.',
 [(x,4,'Appropriate advantage/disadvantage described: 4; named with no description: 2.',[0,2,4]) for x in ('Advantage','Disadvantage')]),
('17ci','0-2',[30],[26],'Explain Newton’s Third Law of Motion, using a named physical activity of your choice.',
 [('Law and application',6,'Correct explanation and application: 6; some application: 4; correct definition only: 2.',[0,2,4,6])]),
('17cii','0-2',[30],[26],'Name and explain another one of Newton’s Laws of Motion, other than the Third Law.',
 [fixed('Law',2,'First or Second Law, correctly named.'),fixed('Explanation',2,'Accurate explanation of the named law.')]),
]
CLOZE='''Fill in the blanks using the words in the box. Each word can only be used once. The words “race” and “resources” have already been supplied.

Word box: Inclusivity; female; Discrimination; race (given); equality; welcomed; prejudiced; barriers; disability; resources (given).

[1] __________ in sport refers to the unfair or [2] __________ treatment of individuals or groups based on characteristics such as race, gender, ethnicity, sexual orientation or [3] __________. In Ireland, discrimination has been evident in various forms across different sports. One example involves gender discrimination in Gaelic games, where [4] __________ athletes in the Ladies’ Gaelic Football Association (LGFA) and Camogie Association have faced unequal funding and resources compared to their male counterparts. Another example is the experience of Travellers, an ethnic minority in Ireland, who have encountered [5] __________ to participation in mainstream sports due to social prejudice. These examples highlight ongoing challenges in ensuring [6] __________ in Irish sport. [7] __________ in sport refers to creating an environment where people of all backgrounds, abilities and identities can participate and feel [8] __________.'''
for i,answer in enumerate(['Discrimination','prejudiced','disability','female','barriers','equality','Inclusivity','welcomed'],1):
    part='18ai' if i==1 else f'18ai-blank-{i}'
    PART_REF_OVERRIDES[part]=f'Q18(a)(i) · blank {i}'
    CONTEXT[part]=CLOZE
    TASKS.append((part,'1-11',[31],[27],f'Complete blank {i} in the passage using the printed word box.',[fixed(f'Blank {i}',2,answer+'.')]))
TASKS += [
('18aii','1-6',[31],[27],'Identify three principles of ethical practice in sport.',
 [fixed(f'Principle {i}',2,'Correct principle of ethical practice.') for i in range(1,4)]),
('18b','1-17',[32],[28],'In any named physical activities of your choice, describe two changes in technology that have allowed for improved performances.',
 repeat('Technology change',2,4,'Described change supporting improved performance: 3–4; technology named: 1–2.')),
('18ci','0-16',[32],[28],'Marta ran a 10km race wearing new runners. She ended up with blisters and a knee injury. Explain the importance of selecting suitable attire in a named physical activity of your choice. You cannot use running.',
 [('Importance',6,'Clear and accurate explanation: 4–6; some explanation: 1–3. Running is excluded.')]),
('18cii','0-16',[32],[28],'Give an example of how you would maintain a sporting facility and why this is important.',
 [fixed('Maintenance',2,'Appropriate example of facility maintenance.'),fixed('Importance',2,'Correct reason why this maintenance is important.')]),
]
CONTEXT.update({
 '7a':'South American soccer players are seen as passionate, skilful and flair-oriented but sometimes lack discipline. European players are tactical, team-oriented and more disciplined.',
 '7b':'South American soccer players are seen as passionate, skilful and flair-oriented but sometimes lack discipline. European players are tactical, team-oriented and more disciplined. Classify the statement using the choices in 7(a), then explain that same classification.',
 '12':'The original stopwatch/coaching photograph is included on page 9.',
 '14aii':'The original tennis photograph is included on page 15.',
 '14bii':'First name a nutrient as requested in 14(b)(i), then explain why an athlete would eat that same nutrient.',
 '14ci':'Figure 7 shows different tennis racquet sizes. Each racquet has a different advantage and is selected based on ability. Your adaptation must not use racquet size.',
 '14cii':'Figure 7 and the preceding equipment task are included. Give two additional adaptations, different from your response to 14(c)(i).',
 '15bi':'Read Rhys McClenaghan’s complete quotation on page 19 about being physically ready but mentally unhappy before the 2023 World Championships in Antwerp.',
 '15bii':'Read the complete Rhys McClenaghan quotation and preceding feedback question on page 19. Explain the type of feedback identified there.',
 '15biii':'The complete Rhys McClenaghan quotation about psychological preparation is included on page 19.',
 '15biv':'The complete Rhys McClenaghan quotation about psychological preparation is included on page 19.',
 '15ci':'Use the original 2005–2025 answer timeline. Figure 8 provides an illustrative LGBTQI+ Olympic timeline, not an additional selectable group.',
 '15cii':'Question 15(c)(i): On the timeline below, identify three major developments that have occurred in the last 20 years for one of the following groups: Women; Older Adults; People with physical disability; People with intellectual disability; Different ethnic groups; Different socio-economic groups.',
 '16ai':'Figure 9 shows all three results of a physical activity participation investigation in a rural Irish secondary school. Use the original charts and data on page 23.',
 '16aii':'Read the original Figure 9 data from a rural Irish secondary school on page 23.',
 '16aiii':'Use Result 3 in the original Figure 9 on page 23, including year groups and participation levels.',
 '16aiv':'The original school investigation data is included on page 23.',
 '16bi':'In 2017 a mixed 4×400m relay was introduced to athletics championships. Teams had two men and two women and could initially choose their running order. This is an example; you may use any named activity.',
 '16bii':'Identify a strategy in your own named activity as requested in 16(b)(i), then explain a reason for changing that same strategy and suggest a change. The relay example is included.',
 '17aii':'Choose one analysis method from your own response to 17(a)(i), then explain how you would use it.',
 '17bi':'The original 2013 and 2023 Sunday Game panel photographs are included on page 28.',
 '17bii':'The original 2013 and 2023 Sunday Game panel photographs are included on page 28.',
 '17biii':'Read the Sunday Game context and panel images on page 28 and the free/pay-per-view comparison on page 29.',
 '17ci':'Figure 12 and the complete original question are included on page 30.',
})
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete Nicola Tuthill case study and photographs on page 10, including her hammer-throw achievements, technique, family and coaching support.'
CONTEXT['13aii']+=' Choose a performance-related component from your own answer to 13(a)(i), then name and describe a test for that same component.'
CONTEXT['13bii']+=' Use a different plane and axis from the hammer rotation in 13(b)(i).'
GROUPS=['Women','Older adults','People with physical disability','People with intellectual disability','Different ethnic groups','Different socio-economic groups']
# A printed choice is ONE card (AGENTS.md, 2026-10-12): the printed question
# with its whole pool, the scheme's own grid, and for choose-N the printed
# instruction plus one criterion per chosen item. pe_complete.py emits one card.
CHOICES={part:{'choose':1,'pool':GROUPS,'stemPrinted':part=='15cii'} for part in ('15ci','15cii')}
SOURCE_POOLS={part:[(21,'for one of the following groups:'),(21,'Women'),(21,'Older Adults'),(21,'People with physical disability'),(21,'People with intellectual disability'),(21,'Different ethnic groups'),(21,'Different socio-economic groups')] for part in CHOICES}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any three'],[2,'or'],[3,'or'],[4,'or'],[5,'choose'],[5,'or'],[5,'or'],[5,'or'],[6,'or'],[7,'named physical activity'],[7,'choose'],[10,'or'],[11,'any one'],[12,'named physical activity'],[15,'any three'],[16,'one of'],[17,'named physical activity'],[19,'named physical activity'],[21,'one of'],[22,'one of'],[25,'choose'],[25,'named physical activity'],[27,'one of'],[29,'named physical activity'],[30,'named physical activity'],[30,'one of'],[31,'or'],[31,'or'],[31,'or'],[32,'named physical activity'],[35,'choose'],[36,'or'],[36,'or']]
EXPECTED_POOL_SCAN=[[2,'any ten'],[2,'three of'],[3,'any ten'],[3,'of the following'],[11,'one of'],[16,'one of'],[21,'one of'],[22,'one of'],[27,'one of'],[30,'one of']]
SELECTION_REVIEW=[
 {'pages':[1,2,3,15],'kind':'exam-attempt-rule-or-boilerplate','reason':'Any ten/three section rules and pen colours are not practice combinations.'},
 {'pages':[3,5,6,7,31],'kind':'single-correct-answer-or-matching','reason':'True/false, vector/scalar, vocabulary matches, classification and cloze blanks have correct answers, not freely selectable essay routes. Split equally and independently marked rows/blanks; retain Q10 as one descending 3+3+2 matching task.'},
 {'pages':[4,10,25,31],'kind':'flexible-or-source-wording','reason':'Media or spectator, three or four hammer rotations, historical relay order choices, and or within the cloze passage are descriptive/flexible wording.'},
 {'pages':[7,11,12,16,17,19,22,25,27,29,30,32],'kind':'open-response-or-own-answer','reason':'Named activities, own fitness component/nutrient/development/analysis method and a different Newton law are open knowledge or selections from the candidate’s own answer, not a printed option pool.'},
 {'pages':[21,22],'kind':'closed-pool-with-inherited-choice','reason':'15(c)(i) asks about one of six printed groups and 15(c)(ii) continues with the group chosen; each scheme grid is the same for every group, so each part is one card. The LGBTQI+ timeline is an illustration, not a seventh option.'},
 {'pages':[16,18,27,29],'kind':'required-components','reason':'Both nutrients and food sources, both official roles, health-related fitness and psychological preparedness, and advantage/disadvantage are compulsory components.'},
 {'pages':[35,36],'kind':'acknowledgements-and-copyright','reason':'Choose in a credited website URL and copyright or are not selection directives.'},
]
ID_CORRECTIONS=[
 {'id':'pe-2025-ol-q1','reason':'Retained on the first independently scored two-mark true/false statement; the other three statements have new IDs.'},
 {'id':'pe-2025-ol-q5','reason':'Retained on the first independently scored two-mark vocabulary match; the other three rows have new IDs.'},
 {'id':'pe-2025-ol-q18ai','reason':'Retained on blank 1 (two marks); seven other independently scored blanks have new IDs and all retain the complete passage.'},
]
