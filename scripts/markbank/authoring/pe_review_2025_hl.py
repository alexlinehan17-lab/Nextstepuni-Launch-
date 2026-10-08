"""Independent visual sweep: all 44 paper and 56 scheme pages.
Written scheme 4–34; project 36–44; performance 46–54; remainder
introductory/blank/end matter. Seven closed pools, including C(6,2)=15
barrier comparisons. Q17(c) is descending 4+3+3; Q17(d) is 12+2=14.
Scheme page 20's Section C heading mistakenly says 80 and omits Q17;
the paper specifies 120, and all five forty-mark questions are represented.
Old tariffs verified: Q12(b) 4→2, Q13(c)(iii) 4→2, Q17(a) 6→8.
"""
from itertools import combinations
PAPER_PAGE_COUNT=44
SCHEME_PAGE_COUNT=56
ACKNOWLEDGEMENT_PAGE=43
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


TASKS=[
('1','1-3',[3],[4], 'Describe two ways in which pathways between school based sport and community based sport can be strengthened.',
 repeat('Pathway',2,4,'Accurate description of an appropriate way to strengthen school–community pathways: 4; some accuracy: 2.',[0,2,4])),
('2','0-3',[4],[4], 'Outline four types of feedback that can be beneficial to athlete performance.',
 repeat('Feedback type',4,2,'Appropriate outline of a named type and its benefit to performance: 2; correct type only: 1.')),
('3a','1-22',[5],[5], 'Explain gender stereotyping in sport.',
 [('Explanation',4,'Accurate: 4; some accuracy: 2.',[0,2,4])]),
('3b','1-21',[5],[5], 'What role can the media play in relation to gender stereotyping in sport?',
 [('Description',4,'Detailed and accurate description of the media’s role: 4; some detail and accuracy: 2.',[0,2,4])]),
('4a','0-24',[6],[6], 'Define the following types of goals related to physical activity: short term goal; performance goal.',
 [(label,2,'Accurate definition: 2; somewhat accurate: 1.') for label in ('Short term goal','Performance goal')]),
('4b','0-24',[6],[6], 'Write a short term performance goal.',
 [('Goal',4,'Accurate, measurable short-term performance goal: 4; missing one element: 3; missing two elements: 2; a goal that is not relevant: 1.')]),
('5','1-8',[6],[7], 'Describe two categories of performance-enhancing drugs. You are not permitted to use anabolic steroids as one of your answers.',
 repeat('Category',2,4,'Detailed and accurate description of an allowed category: 4; accurate example: 2. Anabolic steroids are excluded.',[0,2,4])),
('6a','0-3',[7],[8], 'The principles of effective practice are important in the design of skill practice sessions. Outline two principles of effective practice.',
 repeat('Practice principle',2,2,'Accurate detail on a correctly named principle: 2; some accuracy or correctly identified principle only: 1.')),
('6b','0-3',[7],[8], 'How would you use one of the principles outlined by you in Question 6(a) to develop skill in a practice session?',
 [('Application',4,'Detailed and accurate description of skill development using the principle: 4; some detail and accuracy: 2.',[0,2,4])]),
('7a','1-15',[8],[9], 'Explain adapted physical activity.',
 [('Explanation',2,'Detailed and accurate: 2; some detail and accuracy: 1.')]),
('7b','1-15',[8],[9], 'Outline two ways that a school or community can provide for adapted physical activity. Choose which context you are answering in: school or community.',
 repeat('Provision',2,3,'Accurate outline relevant to the selected context: 3; some accuracy: 2; appropriate way identified: 1.')),
('8a','0-22',[9],[10], 'As part of your studies in Leaving Certificate Physical Education you compared your personal performance to that of a more skilled/model performer. Describe how you conducted this analysis.',
 [('Analysis method',4,'Detailed and accurate description of how the comparison was conducted: 4; some detail and accuracy: 2.',[0,2,4])]),
('8b','0-23',[9],[10], 'Outline two aesthetic/artistic criteria of performance in a named physical activity of your choice.',
 repeat('Criterion',2,2,'Accurate outline relevant to the named activity: 2; some accuracy: 1.')),
('9a','1-26',[10],[11], 'Define the concept of physical activity, mass-participation sports.',
 [fixed('Definition',2,'Accurate definition of mass-participation sports.')]),
('9b','1-2',[10],[11], 'Identify two outdoor and adventure activities.',
 [('Activities',2,'One mark per appropriate outdoor/adventure activity.')]),
('9c','1-2',[10],[11], 'Explain the concept of physical activity, physical education.',
 [('Explanation',4,'Detailed and accurate: 4; somewhat accurate: 2.',[0,2,4])]),
('10a','0-12',[11],[12], 'Outline two benefits of sports drinks for performers.',
 repeat('Benefit',2,2,'Detailed and accurate outline: 2; some accuracy: 1.')),
('10b','1-10',[11],[12], 'Name a sports supplement used by athletes and justify why athletes might use this supplement.',
 [fixed('Supplement',2,'Appropriate sports supplement named.'),('Justification',2,'Detailed and accurate: 2; some detail and accuracy: 1.')]),
('11','0-14',[12],[13], 'Explain two structures or two strategies that can help an athlete or team succeed. Support your answer with physical activity examples. Choose which context you are answering in: structures or strategies.',
 repeat('Example and explanation',2,4,'Detailed and accurate explanation of the chosen structure/strategy in a physical activity and how it helps success: 4; accurate explanation: 2.',[0,2,4])),
('12a','1-9',[13],[14], 'Identify three ways in which Irish anti-doping rules are enforced.',
 repeat('Enforcement method',3,2,'Accurate identification: 1–2 marks, as allocated in the published scheme.')),
('12b','1-9',[13],[14], 'Under what circumstance can an athlete compete with banned substances in their system?',
 [fixed('Circumstance',2,'Appropriate circumstance, such as an approved Therapeutic Use Exemption (TUE).')]),
('13ai','1-2',[14,15,16],[15], 'Identify and define two concepts of physical activity named in the case study.',
 [fixed('Concepts identified',3,'Correct concepts from the case study identified, including play and sport. The scheme allocates 3 marks to identification.'),('Definitions',3,'Detailed and accurate definitions of the concepts: 1–3. The published six-mark allocation is 3 for identification plus 3 for definitions.')]),
('13aii','1-1',[14,15,16],[15], 'Discuss the personal and social benefits, mentioned in the case study, for children engaging in throwing activities.',
 [('Discussion',6,'Detailed and accurate discussion of personal and social benefits: 5–6; some detail and accuracy: 3–4; limited discussion: 1–2.')]),
('13b','0-2',[14,15,17],[16], 'Name a skill that uses a 3rd class lever from a named physical activity of your choice. Justify why this skill is an example of a 3rd class lever.',
 [('Skill and justification',6,'Relevant third-class-lever skill and justification showing understanding of why it is a third-class lever: 1–6. Explain the arrangement of fulcrum, effort and load.')]),
('13ci','0-3',[14,15,18],[17], 'Based on the description of javelin in the case study, name a skill practice method that is appropriate for developing the skill of a javelin thrower.',
 [fixed('Practice method',2,'Appropriate skill practice method for the described javelin technique.')]),
('13cii','0-3',[14,15,18],[17], 'Explain how you would apply the practice method named by you in Question 13(c)(i) to improve the skill of a javelin thrower.',
 [('Application',6,'Accurate application of the named practice method to improve the javelin skill: 4–6; some detail and accuracy: 1–3.')]),
('13ciii','0-2',[14,15,18],[17], 'Hammer throwers mainly move in which plane of movement?',
 [fixed('Plane',2,'Transverse plane.')]),
('13di','0-7',[14,15,19],[18], 'Use Figure 9 to suggest which component of fitness might be developed by throwing light implements in training. Justify why this component of fitness might be developed by throwing light implements.',
 [fixed('Component',3,'Correct component identified using Figure 9, such as speed.'),('Justification',3,'Accurate justification linking the lighter implement to the chosen component: 1–3.')]),
('13dii','0-6',[14,15,19],[18], 'Use Figure 9 to suggest which component of fitness might be developed by throwing heavy implements in training. Justify why this component of fitness might be developed by throwing heavy implements.',
 [fixed('Component',3,'Correct component identified using Figure 9, such as strength.'),('Justification',3,'Accurate justification linking the heavier implement to the chosen component: 1–3.')]),
('13ei','1-8',[14,15,20],[19], 'Suggest two effects that anabolic steroids can have on athlete performance.',
 [fixed(f'Effect {i}',2,'Appropriate effect on athlete performance.') for i in (1,2)]),
('13eii','1-6',[14,15,20],[19], 'Explain how DP Manu did not adhere to the principles of ethical practice when he took methyltestosterone. You must refer to at least two principles of ethical practice in your answer.',
 [('Explanation',6,'Detailed and accurate explanation referring to two appropriate principles: 5–6; some detail and accuracy referring to one appropriate principle: 3–4; little detail or accuracy: 1–2.')]),
('14ai','0-6',[21],[20], 'Define all three components of health-related fitness: cardiorespiratory endurance; body composition; flexibility.',
 [fixed(label,2,'Clear and accurate definition.') for label in ('Cardiorespiratory endurance','Body composition','Flexibility')]),
('14aii','0-10',[21],[20], 'Apply the FITT formula to one of the following components of health-related fitness: cardiorespiratory endurance; body composition; flexibility.',
 [fixed(label,1,'Correct application to the selected component of health-related fitness.') for label in ('Frequency','Intensity','Time','Type')]),
('14bi','1-12',[22],[21], 'Define one of the following terms: discrimination; stereotyping; inclusiveness; prejudice.',
 [('Definition',2,'Clear and accurate definition of the selected term: 2; somewhat accurate: 1.')]),
('14bii','1-6',[22],[21], 'Explain the concept of sportsmanship related to its influence on engagement in physical activity and sport.',
 [('Explanation',6,'Detailed and accurate explanation of sportsmanship and its influence on engagement: 5–6; some detail and accuracy: 3–4; little detail and accuracy: 1–2.')]),
('14c','1-14',[23],[22], 'Discuss two developments in physical activity and sport, since 2005, for one of these groups: women; older adults; people with physical disability; people with intellectual disability; different ethnic groups; different socio-economic groups.',
 repeat('Development',2,5,'Very good detail and accuracy about developments for the selected group in the twenty years to the 2025 exam: 5; some detail and accuracy: 3–4; little detail and accuracy: 1–2.')),
('14d','1-17',[24],[22], 'Examine how advances in technology have impacted performers. Support your answer with physical activity examples.',
 [('Examination',12,'Excellent detail and accuracy with at least three physical activity examples: 10–12; good detail and accuracy with at least two examples: 7–9; some detail and accuracy with at least one example: 4–6; little detail or accuracy: 1–3.')]),
('15ai','0-22',[25],[23], 'Identify two methods that can be used to analyse the skill and technique of an athlete and identify two tests that can be used to analyse the performance-related fitness of an athlete.',
 [fixed(label,1,'Correct method or test for the requested analysis heading.') for label in ('Skill/technique method 1','Skill/technique method 2','Performance fitness test 1','Performance fitness test 2')]),
('15aii','1-7',[25],[23], 'Explain how a code of ethics may apply to one of the following: participant; parent; spectator; coach; club official.',
 [('Explanation',4,'Detailed and accurate explanation for the selected group: 3–4; some accuracy: 1–2.')]),
('15b','0-10',[26],[24], 'Name two principles of training and explain how each of these principles can be used by a coach when designing training programmes. Support your answer with physical activity examples.',
 [('Principles named',2,'One mark per correctly named training principle.')]+repeat('Explanation',2,4,'Detailed and accurate explanation with relevant physical activity examples: 3–4; some detail and accuracy: 1–2.')),
('15c','0-18',[27],[24], 'Discuss personal and technical qualities needed for successful sports coaching.',
 [(label,5,'Very good detail and accuracy: 5; good detail and accuracy: 3–4; some detail and accuracy: 1–2.') for label in ('Personal qualities','Technical qualities')]),
('15d','1-17',[28],[25], 'Examine how developments in technology have impacted coaches or choreographers. Support your answer with physical activity examples.',
 [('Examination',12,'Excellent detail and accuracy with at least two physical activity examples: 10–12; good detail and accuracy with at least two examples: 7–9; some detail and accuracy with at least one example: 4–6; little detail or accuracy: 1–3.')]),
('16ai','1-2',[29],[26], 'People are encouraged to collect data to monitor their physical activity levels. Identify three methods of collecting data on physical activity participation.',
 [('Methods',3,'One mark per appropriate method.')]),
('16aii','1-1',[29],[26], 'Discuss the economic benefits of physical activity participation.',
 [('Discussion',6,'Detailed and accurate discussion of more than one economic benefit: 5–6; some detail and accuracy on more than one benefit: 3–4; little detail: 1–2. The scheme relates the benefits to adults’ health and wellbeing.')]),
('16bi','0-1',[30],[27], 'Define ability.',
 [fixed('Definition',2,'Accurate definition.')]),
('16bii','0-3',[30],[27], 'Outline three stages of learning a new skill.',
 [('Stages named',3,'One mark per correctly named stage: cognitive, associative, autonomous.')]+repeat('Stage outline',3,2,'Accurate outline: 2; some accuracy: 1.')),
('16c','0-10',[31],[28], 'Identify two approaches to training outside of a named physical activity that an athlete could use. Discuss how each approach might help improve performance.',
 [('Approaches identified',2,'One mark per appropriate approach outside the named activity.')]+repeat('Discussion',2,3,'Detailed and accurate discussion of how the approach improves performance: 3; some detail and accuracy: 1–2.')),
('16d','1-18',[32],[28], 'Provide an analysis of how spectator behaviour has been impacted by media coverage.',
 [('Analysis',12,'Very good detail and accuracy: 10–12; good detail and accuracy: 7–9; some detail and accuracy: 4–6; little detail or accuracy: 1–3.')]),
('17a','0-7',[33],[29], 'Identify two performance-related components of fitness that are important in a named physical activity of your choice. Justify why these components are important in the named activity.',
 [('Components',2,'One mark per appropriate performance-related component.')]+repeat('Justification',2,3,'Clear and accurate justification for the named activity: 3; good justification: 2; limited justification, including a health-related component: 1.')),
('17bi','0-11',[34],[30], 'Discuss how a named psychological strategy helps athletes develop their concentration for sports performance.',
 [('Discussion',4,'Detailed and accurate discussion: 3–4; some detail: 1–2.')]),
('17bii','0-21',[34],[30], 'Explain why athletes would conduct a performance analysis.',
 [('Explanation',4,'Detailed and accurate explanation: 3–4; some detail: 1–2.')]),
('17c','1-3',[35],[31], 'Describe three supports to physical activity participation in schools.',
 [('First support assessed',4,'Detailed and accurate: 3–4; some detail and accuracy: 1–2. The scheme uses a descending 4 + 3 + 3 allocation.'),('Second support assessed',3,'Detailed and accurate: 3; some detail and accuracy: 1–2. This allocation is capped at three.'),('Third support assessed',3,'Detailed and accurate: 3; some detail and accuracy: 1–2. This allocation is capped at three.')]),
('17d','1-15',[36],[31], 'Examine ways in which participants in adapted physical activities can be provided with opportunities to achieve excellence.',
 [('Examination',12,'Excellent detail: 10–12; good detail and accuracy: 7–9; some detail and accuracy: 4–6; little detail or accuracy: 1–3.'),fixed('Adapted activity example',2,'Appropriate example of adapted physical activity. These two marks are additional to the twelve-mark examination, giving fourteen overall.')]),
('18ai','1-6',[37],[32], 'Define gamesmanship related to physical activity and sport.',
 [('Definition',2,'Accurate definition: 2; some accuracy: 1.')]),
('18aii','1-6',[37],[32], 'Give two examples of gamesmanship. You cannot use faking injury.',
 [('Examples',2,'One mark per accurate example. Do not accept faking injury, which the paper explicitly excludes.')]),
('18aiii','0-16',[37],[32], 'Outline three safety regulations in a named physical activity of your choice.',
 repeat('Safety regulation',3,2,'Correct outline appropriate to the named activity: 2; some link to physical activity: 1.')),
('18bi','0-10',[38],[33], 'Define overtraining.',
 [('Definition',2,'Accurate definition: 2; some accuracy: 1.')]),
('18bii','0-10',[38],[33], 'Explain two ways that a training schedule can be designed to prevent athletes overtraining.',
 repeat('Prevention method',2,3,'Detailed and accurate explanation: 3; some accuracy and detail: 2; limited explanation: 1.')),
('18c','1-8',[39],[34], 'Explain the possible implications for a performer who is using performance-enhancing drugs.',
 [('Explanation',10,'Excellent detail and accuracy: 8–10; good detail and accuracy: 4–7; some detail and accuracy: 1–3.')]),
('18d','1-12',[40],[34], 'Compare the barriers to physical activity participation for two of the following groups: women; older adults; people with physical disability; people with intellectual disability; different ethnic groups; different socio-economic groups.',
 [('Comparison',12,'Very good detail and accuracy comparing barriers for both selected groups: 10–12; good detail and accuracy: 7–9; some detail and accuracy: 4–6; limited detail: 1–3.')]),
]
CONTEXT={
 '2':'Figure 1 shows rugby coach Niamh Briggs in conversation with player Stacey Flood.',
 '6b':'Choose one of the practice principles you outlined in 6(a). Explain how that same principle develops skill.',
 '7a':'Read the original CSPPA 2022 finding and Sport Ireland Activities for All initiative in Figures 2–3.',
 '7b':'The CSPPA finding and Activities for All initiative are included on the original page.',
 '8a':'Figure 4 shows the 2021 RTÉ Sportsperson of the Year nominees. These illustrate model performers; your analysis is not restricted to that list.',
 '15ai':'Figures 13–14 show Eamon Ryan and Ciara Mageean with Jerry Kiernan; the methods and tests are open choices.',
 '17c':'The original page includes the Active School Flag illustration.',
 '18ai':'Figure 17 describes the Bloodgate incident, in which a player used a capsule to appear to bleed from the mouth.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete throwing case study on pages 14–15, including the movement diagrams, javelin description and weekly training table in Figure 9.'
CONTEXT['13cii']+=' Use the same practice method you named in 13(c)(i).'
GROUPS=['Women','Older adults','People with physical disability','People with intellectual disability','Different ethnic groups','Different socio-economic groups']
FITNESS=['Cardiorespiratory endurance','Body composition','Flexibility']
TERMS=['Discrimination','Stereotyping','Inclusiveness','Prejudice']
ROLES=['Participant','Parent','Spectator','Coach','Club official']
def slug(label):
    return label.lower().replace(' ','-')
def singles(options):
    return [(slug(option),option) for option in options]
VARIANTS={
 '7b':singles(['School','Community']),
 '11':singles(['Structures','Strategies']),
 '14aii':singles(FITNESS),
 '14bi':singles(TERMS),
 '14c':singles(GROUPS),
 '15aii':singles(ROLES),
 '18d':[('-and-'.join(map(slug,pair)),' and '.join(pair)) for pair in combinations(GROUPS,2)],
}
VARIANT_REQUIREMENTS={
 '7b':'Outline two ways to provide adapted activity in this selected context. The original paper requires one context; this route carries six marks.',
 '11':'Explain two examples in this selected category, with physical activity examples. The original paper requires one category; this route carries eight marks.',
 '14aii':'Apply all four FITT elements to this selected fitness component. Each of the three printed alternatives carries four marks.',
 '14bi':'Define this selected term. Each of the four printed alternatives carries two marks.',
 '14c':'Discuss two developments since 2005 for this selected group. Each of the six alternatives carries ten marks.',
 '15aii':'Explain the application of a code of ethics to this selected role. Each of the five alternatives carries four marks.',
 '18d':'Compare barriers for both groups in this practice pair. The original paper requires two of six groups; each of the fifteen pairs carries twelve marks.',
}
SOURCE_POOLS={
 '7b':[(8,'Tick the box to indicate which context you are answering in - school or community.')],
 '11':[(12,'Tick the box to indicate which context you are answering in - structures or strategies.')],
 '14aii':[(21,'Apply the FITT formula to one the following components of health-related fitness:')]+[(21,label) for label in FITNESS],
 '14bi':[(22,'Define one of the following terms:')]+[(22,label) for label in TERMS],
 '14c':[(23,'since 2005, for one of the following groups:')]+[(23,label) for label in GROUPS],
 '15aii':[(25,'Explain how a code of ethics may apply to one of the following:')]+[(25,label) for label in ROLES],
 '18d':[(40,'Compare the barriers to physical activity participation for two of the following groups:')]+[(40,label) for label in GROUPS],
}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any three'],[2,'or'],[6,'one of'],[7,'one of'],[8,'or'],[8,'or'],[9,'named physical activity'],[12,'or'],[12,'or'],[12,'or'],[14,'or'],[14,'or'],[14,'or'],[17,'named physical activity'],[21,'any three'],[22,'one of'],[23,'one of'],[25,'one of'],[28,'or'],[31,'named physical activity'],[33,'named physical activity'],[33,'named physical activity'],[37,'named physical activity'],[43,'choose'],[44,'or'],[44,'or']]
EXPECTED_POOL_SCAN=[[2,'any ten'],[2,'three of'],[3,'any ten'],[6,'one of'],[7,'one of'],[22,'one of'],[23,'one of'],[25,'one of'],[40,'two of']]
SELECTION_REVIEW=[
 {'pages':[2,3,21],'kind':'exam-attempt-rule','reason':'Any ten/three chooses already represented questions, not combinations of examination attempts.'},
 {'pages':[2,43,44],'kind':'boilerplate-and-attribution','reason':'Pen colours, an RTÉ URL containing choose, and copyright text are not task choices.'},
 {'pages':[6,7,9,17,20,26,28,31,33,37],'kind':'open-response-and-exclusions','reason':'Practice/training principles, named activities, performance components and ethics principles have no finite printed option pool. Anabolic steroids and faking injury are excluded. Aesthetic/artistic and coach/choreographer are flexible wording. The athlete nominees illustrate model performers, not a required selection pool.'},
 {'pages':[8,12],'kind':'closed-binary-context','reason':'Q7(b) and Q11 explicitly require a checkbox selection of one of two named contexts. Generate both routes for each, preserving two responses within each selected context.'},
 {'pages':[14,15,16],'kind':'case-study-context','reason':'Movement categories, illustrated skills and throwing disciplines provide source context. Q13(a)(i) extracts two concepts from the source; it does not offer a finite list of alternative essay routes.'},
 {'pages':[6,21,25,27,30,35],'kind':'required-headings','reason':'Both goals, all three HRF definitions, both analysis methods and tests, both coaching-quality headings, all three learning stages and all three school supports are compulsory response components.'},
 {'pages':[21,22,23,25,40],'kind':'closed-printed-pools','reason':'Q14(a)(ii) chooses one of three FITT components (paper omits the word of); Q14(b)(i) one of four terms; Q14(c) one of six groups; Q15(a)(ii) one of five roles; Q18(d) two of six groups. Generate every route and pair.'},
]
