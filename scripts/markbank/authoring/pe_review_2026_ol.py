"""Independent visual sweep: all 32 paper and 38 scheme pages.
Written scheme 4–22; project 23–30; performance 31–36; other pages
introductory/blank/end matter. Fixed matching and true/false rows are separate
tasks at their printed allocations. Q8 has three routes; Q13(c)(i) has two.
"""
PAPER_PAGE_COUNT=32
SCHEME_PAGE_COUNT=38
ACKNOWLEDGEMENT_PAGE=31
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


PART_REF_OVERRIDES={}
TASKS=[]
for i,(timeframe,answer) in enumerate([('Two months','Mesocycle'),('A full year','Macrocycle'),('Two weeks','Microcycle')],1):
    part='1a' if i==1 else f'1a-row-{i}'
    PART_REF_OVERRIDES[part]=f'Q1(a) · row {i}'
    TASKS.append((part,'0-10',[3],[4],f'Match the timeframe “{timeframe}” to a periodisation cycle: Macrocycle; Mesocycle; Microcycle.',[fixed('Cycle',1,answer+'.')]))
TASKS += [
('1b','0-10',[3],[4],'Why do coaches use periodisation?',
 [('Reason',5,'Clear description of accurate practical reasons: 5; accurate reasons: 3; some reference to a correct reason: 1.',[0,1,3,5])]),
('2','0-19',[4],[4],'Outline two safety checks an official should make before a competition, in a physical activity of your choice.',
 repeat('Safety check',2,4,'Relevant safety check correctly outlined: 4; identified only: 2.',[0,2,4])),
('3','1-18',[4],[5],'Identify three characteristics of a physical activity that could make it appealing to spectators.',
 [(f'Characteristic {i}',maximum,f'Accurate characteristic of the named activity: {maximum}; a reason why people watch sport: 1. Award full-credit responses in descending order (3, 3, 2).',[0,1,maximum]) for i,maximum in enumerate([3,3,2],1)]),
]
for i,(statement,answer) in enumerate([
 ('An athlete is allowed to sell performance-enhancing drugs.','False'),
 ('Three whereabouts failures within a 12-month period can lead to a suspension.','True'),
 ('An athlete must provide a sample when requested by a Doping Control Officer.','True'),
 ('Athletes are allowed to cover up for another athlete if they know they are using performance-enhancing drugs.','False'),
],1):
    part='4' if i==1 else f'4-statement-{i}'
    PART_REF_OVERRIDES[part]=f'Q4 · statement {i}'
    TASKS.append((part,'1-9',[5],[5],f'Is this statement about Irish anti-doping rules true or false? {statement}',[fixed('Correct answer',2,answer+' (2026 examination).')]))
TASKS += [
('5a','0-11',[5],[6],'Outline how the psychological factor confidence can affect sports performance.',
 [('Outline',6,'Clear and accurate outline of effects on performance: 4–6; relevant outline: 1–3.')]),
('5b','0-11',[5],[6],'Identify one strategy that could be used to improve confidence.',
 [fixed('Strategy',2,'Relevant strategy to improve confidence.')]),
('6','1-22',[6],[6],'Identify three examples of gender stereotyping in sport.',
 [('Three examples',8,'Correct examples: first 3, second 3, third 2. One correct: 3; two: 6; three: 8.',[0,3,6,8])]),
]
METHODS='Anxiety test; Video analysis; Balance test; Sit-and-reach test; Food diary; 12-minute run.'
for i,(area,answer,topic) in enumerate([
 ('Performance-related component of fitness','Balance test','0-9'),
 ('Psychological preparedness','Anxiety test','0-22'),
 ('Skill and technique','Video analysis','0-22'),
 ('Nutrition','Food diary','0-12'),
],1):
    part='7' if i==1 else f'7-row-{i}'
    PART_REF_OVERRIDES[part]=f'Q7 · row {i}'
    TASKS.append((part,topic,[6],[7],f'Identify the appropriate analysis method or test for this performance area: {area}.\n\nMethods/tests: {METHODS}',[fixed('Method/test',2,answer+'.')]))
TASKS += [
('8','0-3',[7],[7],'Explain how one type of practice from this list could be used to improve a skill of your choice: Massed Practice; Part Practice; Variable Practice.',
 [('Explanation',8,'Clear and accurate explanation of the selected method linked to improving a named skill: 6–8; accurate linked explanation: 4–5; appropriate method explanation: 1–3.')]),
('9','1-17',[7],[8],'Outline how one technological development has positively impacted a physical activity of your choice.',
 [fixed('Development',2,'Appropriate technological development.'),('Positive impact',6,'Clear and accurate outline of its positive impact on the named activity: 4–6; correct outline: 1–3.')]),
('10a','0-7',[8],[8],'Define reaction time.',
 [('Definition',4,'Clear and accurate: 4; accurate: 2.',[0,2,4])]),
('10b','0-8',[8],[8],'Identify two examples of where reaction time is needed during performance in one physical activity.',
 [fixed(f'Example {i}',2,'Correct example. Both examples must come from the same named activity.') for i in (1,2)]),
('11','0-18',[8],[9],'Outline two ways a coach could manage time effectively during a training session.',
 repeat('Time management',2,4,'Clear and accurate suggestion relevant to training: 3–4; relevant suggestion outlined: 1–2.')),
('12','1-1',[9],[9],'Describe two benefits of physical activity for teenagers.',
 repeat('Benefit',2,4,'Clear and accurate description of a benefit relevant to teenagers: 3–4; benefit with little or no detail: 1–2.')),
('13a','1-8',[10,11],[10],'Kamila Valieva tested positive for trimetazidine. Name two other performance-enhancing drugs and state how they affect performance.',
 [fixed(f'PED {i}',2,'Correct PED other than trimetazidine.') for i in (1,2)]+repeat('Effect',2,3,'Correctly states effect on performance: 3; vague statement: 1.',[0,1,3])),
('13bi','1-9',[10,11],[10],'Outline two consequences for an athlete when anti-doping rules are broken. At least one consequence must be from the case study.',
 [('Two consequences',5,'Two appropriate consequences clearly outlined: 5 (3+2); one: 3. Include a case-study consequence: a ban from competing or being stripped of a medal.',[0,3,5])]),
('13bii','1-9',[10,11],[10],'Outline two consequences for the physical activity when anti-doping rules are broken.',
 [('Two consequences',5,'Two accurate consequences for the physical activity: 5 (3+2); one: 3.',[0,3,5])]),
('13ci','1-6',[10,12],[11],'Explain one of the following ethical principles with reference to the case study: fairness; integrity.',
 [('Explanation',8,'Clear and accurate explanation of the chosen principle linked to the case: 7–8; accurate explanation and/or case reference: 4–6; appropriate explanation: 1–3.')]),
('13cii','1-7',[10,12],[11],'Identify three statements that you would include in a code of ethics for sport.',
 [(f'Statement {i}',maximum,f'Relevant statement suitable for a code of ethics: {maximum}; appropriate but less-developed answer: 1. Apply full-credit responses in descending order (4, 3, 2).',[0,1,maximum]) for i,maximum in enumerate([4,3,2],1)]),
('13di','0-23',[10,13],[11],'Identify two artistic/aesthetic criteria of performance in a physical activity of your choice. You may not refer to use of space.',
 [('Two criteria',5,'Clearly identified criteria other than use of space: first 4, second 1. One correct: 4; two: 5.',[0,4,5])]),
('13dii','0-23',[10,13],[12],'Compare the two performances depicted in Figure 4a and Figure 4b in terms of artistic or aesthetic criteria of performance.',
 [('Comparison',8,'Clear and accurate comparison using examples from both images: 7–8; criteria related to both images: 4–6; criteria related to one image: 1–3.')]),
('14ai','0-10',[14],[13],'Identify one symptom of overtraining.',
 [fixed('Symptom',2,'Correct symptom of overtraining.')]),
('14aii','0-10',[14],[13],'Outline one strategy to avoid overtraining.',
 [('Strategy',4,'Clear and accurate outline: 4; appropriate outline: 2.',[0,2,4])]),
('14b','0-10',[14],[13],'Outline how you could use weight training and circuit training to improve performance in a component of fitness of your choice.',
 [(x,4,'Clear and accurate outline of using this method for the chosen component: 3–4; appropriate outline: 1–2.') for x in ('Weight training','Circuit training')]),
('14ci','0-9',[15],[14],'From Alan’s test results, identify which component of fitness he scored above average on.',
 [fixed('Component',1,'Coordination (37, compared with an average of 25–29).')]),
]
for i,(component,answer,topic) in enumerate([('Coordination','PRF','0-7'),('Muscular endurance','HRF','0-6')],1):
    part='14cii' if i==1 else '14cii-row-2'
    PART_REF_OVERRIDES[part]=f'Q14(c)(ii) · row {i}'
    TASKS.append((part,topic,[15],[14],f'Is {component.lower()} a Health-Related Fitness (HRF) or Performance-Related Fitness (PRF) component?',[fixed('Classification',1,answer+'.')]))
TASKS += [
('14ciii','0-8',[15],[14],'Identify three fitness components required by an athlete in a physical activity of your choice. You may not use coordination or muscular endurance.',
 [fixed(f'Component {i}',2,'Correct component relevant to the named activity; coordination and muscular endurance are excluded.') for i in range(1,4)]),
('14civ','0-5',[15],[14],'Identify whether the three components you chose in Question 14(c)(iii) are health-related fitness (HRF) or performance-related fitness (PRF) components.',
 [fixed(f'Classification {i}',1,'Correct classification of the corresponding component named in 14(c)(iii).') for i in range(1,4)]),
('14cv','0-9',[15],[14],'State a fitness test for each of the three components you chose in Question 14(c)(iii).',
 [fixed(f'Fitness test {i}',2,'Correct test for the corresponding component chosen in 14(c)(iii).') for i in range(1,4)]),
('14cvi','0-9',[15,16],[14],'Describe how to carry out one of the fitness tests identified by you in Question 14(c)(v). You may use a diagram.',
 [('Test protocol',8,'Clear and accurate description of the protocol for the previously named test: 8; accurate description: 4–7; appropriate description: 1–3.')]),
]
for i,(description,answer) in enumerate([
 ('Large number of people participating in an event at the same time.','Mass-participation sports'),
 ('Activities that focus on fun and enjoyment.','Play'),
 ('Activities that have an element of risk and take place outdoors.','Outdoor and adventure'),
],1):
    part='15ai' if i==1 else f'15ai-row-{i}'
    PART_REF_OVERRIDES[part]=f'Q15(a)(i) · row {i}'
    TASKS.append((part,'1-0',[17],[15],f'Match the description to its concept of physical activity and name one example of an activity for that concept.\n\nDescription: {description}\n\nConcepts: mass-participation sports; play; outdoor and adventure.',[fixed('Concept',2,answer+'.'),fixed('Example',2,'Appropriate physical activity for this concept.')]))
TASKS += [
('15aii','1-0',[17],[15],'Physical Education is a concept of physical activity. Explain Physical Education.',
 [('Explanation',4,'Accurately explains PE as a concept of physical activity: 3–4; appropriate explanation: 1–2.')]),
('15b','1-3',[18],[16],'Outline three characteristics of significant people, like role models, who promote participation in physical activity amongst young people.',
 repeat('Characteristic',3,4,'Correctly identified and outlined with a clear link to promoting activity: 4; some link: 2–3; appropriate characteristic outlined: 1.')),
('15c','1-3',[19],[16],'Describe how a National Governing Body can help promote physical activity at local and national levels.',
 [fixed('NGB',2,'Correct National Governing Body named.')]+[(x,5,'Clear and accurate description of how the named NGB promotes activity at this level: 5; relevant description, possibly with examples: 2–4; appropriate description: 1.') for x in ('Local','National')]),
('16ai','0-1',[20],[17],'Identify two characteristics of skilled performance.',
 [fixed(f'Characteristic {i}',2,'Correct characteristic, such as accuracy, anticipation, consistency or kinaesthetic awareness.') for i in (1,2)]),
('16aii','0-1',[20],[17],'Describe two ways that creative application of a skill can be beneficial to performance.',
 repeat('Creative application',2,4,'Accurate description: 4; appropriate description: 2. The scheme expects applications from two different activities. Its printed 8-mark maximum is two 4-mark responses; the bracketed extra 2×2 is a typographical inconsistency.',[0,2,4])),
('16b','0-3',[21],[17],'Describe three stages of skill learning.',
 [fixed(f'Stage {i}',2,'Correct stage named (cognitive, associative, autonomous).') for i in range(1,4)]+repeat('Description',3,4,'Clear and accurate description of the corresponding correctly named stage: 3–4; accurate description: 1–2.')),
('16ci','0-2',[22],[18],'What class of lever is depicted in Figure 6?',
 [fixed('Lever class',2,'Second class lever.')]),
('16cii','0-2',[22],[18],'Name one example of a sporting action that uses the class of lever depicted in Figure 6.',
 [fixed('Sporting action',2,'Appropriate sporting action using a second class lever.')]),
('16ciii','0-2',[22],[18],'Name two other classes of lever, different from Figure 6, and an example of where each is used in sport.',
 [fixed('First class lever',2,'First class lever named.'),fixed('Third class lever',2,'Third class lever named.'),fixed('First class example',1,'Accurate sporting example.'),fixed('Third class example',1,'Accurate sporting example.')]),
('17a','0-12',[23],[19],'Identify two food or drink choices that would be good to consume after exercise and give a reason for each choice.',
 [fixed(f'Food/drink {i}',2,'Appropriate choice for after exercise.') for i in (1,2)]+repeat('Reason',2,4,'Accurate reason linked to nutrient content and function: 4; appropriate reason: 1–2.',[0,1,2,4])),
('17bi','1-10',[24],[19],'Protein can be used as a supplement. Name two other food supplements and give a reason for taking them.',
 [fixed(f'Supplement {i}',2,'Correct supplement other than protein.') for i in (1,2)]+repeat('Reason',2,3,'Correct reason: 3; appropriate reason: 1.',[0,1,3])),
('17bii','1-10',[24],[19],'Outline two challenges to taking sports supplements.',
 repeat('Challenge',2,3,'Accurate outline of a relevant challenge: 3; appropriate information: 1–2.')),
('17ci','0-11',[25],[20],'Identify two reasons an elite pole vaulter’s concentration could be decreased.',
 [fixed(f'Reason {i}',2,'Appropriate reason affecting concentration in this context.') for i in (1,2)]),
('17cii','0-11',[25],[20],'Explain a strategy an athlete, such as the elite pole vaulter, could use to maintain concentration during a long competition.',
 [fixed('Strategy',2,'Correct concentration strategy named.'),('Explanation',6,'Clear, accurate and detailed explanation: 6; accurate explanation: 3–5; appropriate explanation: 1–2.')]),
('18ai','1-21',[26],[21],'Define body image.',
 [('Definition',4,'Clear and accurate: 4; appropriate: 2.',[0,2,4])]),
('18aii','1-21',[26],[21],'Outline how body image can influence participation in physical activity. Use two examples.',
 repeat('Example and influence',2,3,'Clear and accurate outline of influence using a relevant example: 3; appropriate outline: 1–2.')),
('18b','1-21',[26,27],[21],'Describe two ways media representation of the body may impact on young people’s participation in physical activity.',
 repeat('Way',2,6,'Clear and accurate description with an appropriate example: 4–6; appropriate description: 1–3. The two ways must be different.')),
('18ci','1-26',[28],[22],'Outline two benefits of mass-participation sports events, like Parkrun.',
 repeat('Benefit',2,3,'Appropriate outline of benefit: 3; relevant benefit: 1–2.')),
('18cii','1-18',[28],[22],'Describe how media coverage is used positively in mass-participation sports events. Use two examples.',
 repeat('Positive use',2,6,'Clear and accurate description with a relevant example: 4–6; appropriate description with example: 1–3. The two examples must be different.')),
]
CONTEXT={
 '14ci':'Alan is a 16-year-old Gaelic football player. Coordination: 37, average 25–29. Muscular endurance: 12, average 15–20. Read the original results table on page 15.',
 '14cii':'Use the original fitness table on page 15. Classify the coordination row.',
 '14cii-row-2':'Use the original fitness table on page 15. Classify the muscular endurance row.',
 '14civ':'Name an activity and three required components as requested in 14(c)(iii), excluding coordination and muscular endurance. Classify those same three components.',
 '14cv':'Name an activity and three required components as requested in 14(c)(iii), excluding coordination and muscular endurance. Give a test for each of those same components.',
 '14cvi':'Choose your own fitness component other than coordination or muscular endurance and name its test as requested in 14(c)(iii)–(v). Describe that same test. The original preceding table is included on page 15.',
 '15b':'Ireland won seven medals at the Paris Olympics 2024. The original photograph of the medal winners, presented as role models, is included on page 18.',
 '15c':'The source states that extra funding is being provided to NGBs after Irish athletes’ 2024 Olympic success. Name any suitable NGB and cover both local and national promotion.',
 '16ci':'Use the original wheelbarrow diagram with effort, load and fulcrum labelled on page 22.',
 '16cii':'Use the lever class represented by the original wheelbarrow diagram on page 22.',
 '16ciii':'The original wheelbarrow diagram and preceding lever questions are included on page 22. Name two classes other than the one depicted.',
 '17a':'The original healthy-plate illustration in Figure 7 is included on page 23.',
 '17ci':'Elite pole vault competitions can last two to three hours in a busy athletics arena, while an athlete may jump only four times in a three-hour competition.',
 '17cii':'Elite pole vault competitions can last two to three hours in a busy athletics arena, while an athlete may jump only four times in a three-hour competition.',
 '18ai':'Figure 8 and the complete Ilona Maher passage are included on page 26: she defended her body type against negative online comments and encouraged people to notice the variety of Olympic athletes’ bodies.',
 '18aii':'Figure 8 and the complete Ilona Maher passage are included on page 26, including negative online comments and her response about different Olympic athletes’ body types.',
 '18b':'The complete Ilona Maher passage and photograph from the preceding page are included.',
 '18ci':'The source describes Parkrun as a 5km mass-participation run held on Saturday mornings in many locations, welcoming everyone.',
 '18cii':'The original Parkrun context and preceding benefits question are included on page 28.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete “Figure Skating” case study, skating pattern, photograph and headline on page 10 about Kamila Valieva and the consequences of her positive doping test.'
CONTEXT['13di']+=' Figure 1 illustrates use of space, which this task excludes.'
CONTEXT['13dii']+=' Compare both Figure 4a (figure skater) and Figure 4b (artistic swimming team) on page 13.'
VARIANTS={
 '8':[(x.lower().replace(' ','-'),x) for x in ['Massed Practice','Part Practice','Variable Practice']],
 '13ci':[(x.lower(),x) for x in ['Fairness','Integrity']],
}
VARIANT_REQUIREMENTS={
 '8':'Use the selected printed practice method and apply it to a skill of your choice.',
 '13ci':'Explain the selected printed ethical principle with reference to the complete figure-skating case study.',
}
SOURCE_POOLS={
 '8':[(7,'one type of practice, from the list below'),(7,'Massed Practice'),(7,'Part Practice'),(7,'Variable Practice')],
 '13ci':[(12,'one of the following ethical principles'),(12,'fairness integrity')],
}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any three'],[2,'or'],[3,'choose'],[5,'or'],[6,'or'],[6,'or'],[6,'choose'],[10,'or'],[12,'one of'],[13,'or'],[14,'any three'],[15,'or'],[15,'or'],[15,'or'],[15,'or'],[15,'or'],[16,'one of'],[17,'choose'],[23,'or'],[32,'or'],[32,'or']]
EXPECTED_POOL_SCAN=[[2,'any ten'],[2,'three of'],[3,'any ten'],[7,'from the list'],[12,'one of'],[15,'two of'],[16,'one of'],[17,'of the following']]
SELECTION_REVIEW=[
 {'pages':[1,2,3,14],'kind':'exam-attempt-rule-or-boilerplate','reason':'Section-level any ten/three and pen colour instructions are not task alternatives.'},
 {'pages':[3,5,6,15,17],'kind':'fixed-answer-matching-or-classification','reason':'Periodisation matches, anti-doping true/false, analysis-method matches, fixed HRF/PRF classifications and concept matches have correct answers, not freely selectable alternatives. Fixed printed rows split at their scheme tariffs; concept matches keep the associated example with each row.'},
 {'pages':[7,12],'kind':'closed-choose-one','reason':'Q8 has three explicitly listed practice methods; Q13(c)(i) has two named ethical principles. Generate all three and both routes respectively.'},
 {'pages':[10,13,15,23],'kind':'descriptive-or-flexible-wording','reason':'Patterns or figures, artistic or aesthetic, food or drink and two of his fitness results are descriptive/flexible wording. The original performance comparison requires both images.'},
 {'pages':[4,5,8,9,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28],'kind':'open-response-or-required-components','reason':'Own activities, symptoms, methods, components, tests, examples, characteristics and benefits are open knowledge. Weight/circuit training, local/national levels, all skill stages and both other lever classes are required components. Follow-up tests use the candidate’s own chosen components, not a finite printed pool.'},
 {'pages':[32],'kind':'copyright','reason':'Copyright or wording is not a choice directive.'},
]
ID_CORRECTIONS=[
 {'id':'pe-2026-ol-q1a','reason':'Retained on the first independently scored one-mark periodisation match; remaining rows have new IDs.'},
 {'id':'pe-2026-ol-q7','reason':'Retained on the first independently scored two-mark analysis match; remaining rows have new IDs and their own canonical topics.'},
]
