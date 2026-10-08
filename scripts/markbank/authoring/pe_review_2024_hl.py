"""Independent visual review of all 44 paper and 48 scheme pages.
Written scheme 4–28; Irish bonus 29; project 30–38; performance 39–45;
46–48 blank/end matter. No finite printed response pools.
Corrected old tariffs: Q4 4→8, Q7 4→8, Q13(c)(iii) 1→5,
Q15(a)(ii) 2→6, Q15(b) 4→8, Q17(c) 6→12.
"""
PAPER_PAGE_COUNT=44
SCHEME_PAGE_COUNT=48
ACKNOWLEDGEMENT_PAGE=43
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


TASKS=[
('1a','0-22',[3],[4], 'Identify an appropriate method to analyse each of the following aspects of performance: psychological preparedness; choreography. You must use a different method of analysis for each aspect of performance.',
 [fixed('Psychological preparedness',2,'Appropriate method, such as a SCAT questionnaire or Sports Motivation Scale.'),fixed('Choreography',2,'Appropriate different method, such as video analysis, coach feedback or a checklist.')]),
('1b','0-23',[3],[4], 'Explain the term “aesthetic and/or artistic criteria of performance” related to physical activities.',
 [('Explanation',4,'Clear, accurate and detailed explanation: 4; some detail and accuracy: 2.',[0,2,4])]),
('2a','1-2',[4],[5], 'Define the concept of physical activity, leisure and recreation.',
 [('Definition',2,'Accurate definition of leisure and recreation: 2; somewhat accurate: 1.')]),
('2b','1-12',[4],[5], 'Discuss two barriers to physical activity participation in the community.',
 repeat('Barrier',2,3,'Detailed and accurate discussion: 3; brief discussion: 2; appropriate barrier named: 1.')),
('3a','0-11',[5],[6], 'Discuss how motivation can impact an athlete’s practice.',
 [('Discussion',4,'Detailed and accurate discussion of motivation and practice: 4; some detail and accuracy: 2. Address practice, not only performance.',[0,2,4])]),
('3b','0-11',[5],[6], 'Name a strategy that athletes could use to enhance their motivation. Explain how this strategy enhances motivation.',
 [fixed('Strategy',2,'Appropriate strategy named.'),('Explanation',2,'Accurate explanation of how the strategy enhances motivation: 2; some accuracy: 1.')]),
('4','1-17',[6],[7], 'According to a Capgemini survey of 10,000 people in nine countries, nearly 70 percent of fans say new technologies have enhanced their viewing experience. Discuss two advancements in technology that have impacted spectator experience in a named physical activity of your choice.',
 repeat('Advancement',2,4,'Detailed and accurate discussion of the advancement and its impact on spectator experience: 4; some detail and accuracy: 2.',[0,2,4])),
('5a','0-1',[7],[8], 'Define skill.',
 [('Definition',2,'Accurate definition: 2; somewhat accurate: 1.')]),
('5b','0-1',[7],[8], 'Identify two characteristics of skilled performance.',
 [('Characteristics',2,'One mark per correctly identified characteristic.')]),
('5c','0-1',[7],[8], 'Explain the term creative application of skill.',
 [('Explanation',4,'Accurate and detailed explanation: 4; some accuracy and detail: 2.',[0,2,4])]),
('6','1-9',[8],[9], 'A function of Sport Ireland Anti-Doping is the elimination of doping in Irish sport. State four current Irish anti-doping rules.',
 [fixed(f'Rule {i}',2,'Correctly stated rule. Apply the rules examined in the 2024 paper and published scheme.') for i in range(1,5)]),
('7','0-10',[8],[9], 'Explain two methods of physical fitness training used to develop performance for a named physical activity of your choice.',
 repeat('Training method',2,4,'Detailed, accurate explanation of the method and its use to develop performance: 4; some detail and accuracy: 2.',[0,2,4])),
('8a','0-16',[9],[10], 'Identify two injuries that commonly occur in a named physical activity of your choice and identify the potential causes of both injuries.',
 [fixed(label,1,'Appropriate injury or matching potential cause for the named activity.') for label in ('Injury 1','Cause 1','Injury 2','Cause 2')]),
('8b','0-16',[9],[10], 'Describe the first aid treatment for one of the injuries identified by you in Question 8(a).',
 [('Treatment',4,'Detailed and accurate description of first aid for the selected injury: 4; some detail and accuracy: 2.',[0,2,4])]),
('9a','1-24',[10],[11], 'Define endorsements related to sport.',
 [('Definition',2,'Accurate definition: 2; somewhat accurate: 1.')]),
('9b','1-24',[10],[11], 'Identify two advantages of sponsorship for the National Governing Bodies of sport.',
 [('Advantages',2,'One mark per appropriate advantage for an NGB.')]),
('9c','1-24',[10],[11], 'Describe two disadvantages of sponsorship for athletes.',
 repeat('Disadvantage',2,2,'Accurate description of a disadvantage for athletes: 2; some accuracy: 1.')),
('10','1-3',[11],[12], 'Figures 5 and 6 give details of the World Health Organisation’s guidelines for physical activity for children and adolescents aged 5–17. Discuss two different approaches to physical activity promotion.',
 repeat('Approach',2,4,'Detailed and accurate discussion of an appropriately identified promotion approach: 4; some detail and accuracy: 2.',[0,2,4])),
('11a','0-19',[12],[12], 'The development of personal fitness is important for officials. Why?',
 [('Reason',2,'Accurate reason: 2; some degree of accuracy: 1.')]),
('11b','0-19',[12],[12], 'Identify two strategies that an official can use to manage conflict between participants.',
 [('Strategies',2,'One mark per appropriate strategy, such as clarifying the situation, applying rules, addressing players assertively or speaking to captains.')]),
('11c','0-19',[12],[13], 'Describe appropriate attire and appropriate equipment needed by an official in a named physical activity of your choice.',
 [(label,2,'Detailed and accurate description relevant to the official and activity: 2; some detail and accuracy: 1.') for label in ('Attire','Equipment')]),
('12a','0-12',[13],[13], 'Name three energy systems used by the human body.',
 [('Energy systems',3,'One mark each: ATP-PC/phosphagen/anaerobic alactacid; anaerobic glycolytic/lactic acid; aerobic/oxidative.')]),
('12b','0-12',[13],[13], 'Discuss the role of one named energy system for performance in a named physical activity of your choice.',
 [('Discussion',5,'Accurate, detailed and clear understanding of the system’s contribution to performance: 5; some accuracy and understanding: 3; little understanding and lacking detail: 1.',[0,1,3,5])]),
('13ai','0-2',[14,15],[14], 'Discuss the difference between vectors and scalars in sport.',
 [('Discussion',4,'Accurate, detailed difference: 4; some accuracy: 2. Vectors have magnitude and direction; scalars have magnitude only.',[0,2,4])]),
('13aii','0-2',[14,15],[14], 'Identify two sport related scalar quantities mentioned in the case study.',
 [('Scalar quantities',2,'One mark per correct scalar from the case: 400 m, 50.13 seconds, 8.13 m/s. The published scheme also accepts 49.20 seconds.')]),
('13b','0-16',[14,16],[14], 'Examine two approaches to safe practice that organisers of an event, such as the Olympic Games, may implement.',
 repeat('Safe practice approach',2,5,'Detailed and accurate examination: 4–5; mostly accurate with some detail: 2–3; little detail or accuracy: 1.')),
('13ci','0-10',[14,17],[15], 'Define periodisation.',
 [('Definition',2,'Accurate: 2; somewhat accurate: 1.')]),
('13cii','0-2',[14,17],[15], 'What time did Adeleke run in the 400m NCAA championship final race in Texas in 2023?',
 [('Time calculation',3,'49.2 seconds: 3; 49.2 without units or correct calculation 400 ÷ 8.13: 2; correct unit (seconds) only: 1.')]),
('13ciii','0-10',[14,17],[15], 'Suggest one reason why Adeleke ran a faster time in the NCAA championship final than in the 400m World Championship final last year. Justify your reason with reference to the case study.',
 [('Reason and justification',5,'Correct reason appropriately justified from the case study: 5; correct reason with attempted justification but some inaccurate detail: 3; correct reason or limited justification: 1. Example: fatigue following a long season.',[0,1,3,5])]),
('13d','1-17',[14,18],[16], 'Analyse the role of technology in the evaluation of sporting performance.',
 [('Analysis',12,'Detailed and accurate: 10–12; mostly accurate: 7–9; some detail and accuracy: 4–6; little accurate information: 1–3.')]),
('13e','1-25',[14,19],[16], 'Mass participation events like the Olympic Games provide great opportunities for business and enterprise. Analyse this statement.',
 [('Analysis',12,'Detailed and accurate: 12; mostly accurate: 9; some detail and accuracy: 6; little accurate information: 3.',[0,3,6,9,12])]),
('14a','1-18',[20],[17], 'Identify four characteristics from a named physical activity of your choice that give it media and/or spectator appeal.',
 [fixed(f'Characteristic {i}',2,'Correct characteristic relevant to the activity and its media or spectator appeal.') for i in range(1,5)]),
('14b','0-3',[21],[17], 'Explain three practice methods that can be used to develop skills in a named physical activity of your choice.',
 repeat('Practice method',3,4,'Accurate and detailed explanation of skill development in the named activity: 3–4; somewhat accurate and detailed: 1–2.')),
('14c','0-2',[22],[18], 'Using sporting examples, examine the differences between second class levers and third class levers.',
 [('Comparison',8,'Excellent detail and accuracy with appropriate sporting examples: 7–8; accurate with sporting examples: 5–6; some detail and accuracy: 3–4; little accuracy: 1–2. Second class has load in the middle; third class has effort in the middle.')]),
('14d','1-18',[23],[18], 'As part of your studies in Leaving Certificate Physical Education you investigated the media coverage of elite performance in sport. Explain your findings.',
 [('Findings',12,'Detailed, accurate investigation displaying excellent knowledge: 12; mostly accurate with good knowledge: 9; some detail and accuracy: 6; little accurate information: 3.',[0,3,6,9,12])]),
('15ai','1-4',[24],[19], 'Suggest one way a National Governing Body of a sport might use the funding they receive from Sport Ireland to support athletes who compete at an international level.',
 [fixed('Suggestion',2,'Appropriate use of Sport Ireland funding for international athletes.')]),
('15aii','1-3',[24],[19], 'Discuss how a named National Governing Body of sport supports the development of sport at a local level.',
 [fixed('NGB',2,'Appropriate National Governing Body named.'),('Discussion',4,'Good discussion with correct examples: 4; fair discussion of local development: 2.',[0,2,4])]),
('15b','0-10',[25],[20], 'Explain two recovery strategies that athletes use after exercise to support adaptations of the body.',
 repeat('Recovery strategy',2,4,'Detailed, accurate explanation linking the strategy to positive adaptations: 3–4; some accuracy: 1–2.')),
('15c','0-9',[26],[20], 'Design a performance-related fitness test battery for a named physical activity of your choice. Complete three rows, giving the performance-related fitness component being tested, the name of a fitness test, and a justification for including that test in each row.',
 [fixed(f'Component {i}',1,'Performance-related fitness component appropriate to the activity.') for i in range(1,4)]+[fixed(f'Test {i}',1,'Correct fitness test matching the component.') for i in range(1,4)]+repeat('Justification',3,2,'Accurate reason why the component is being tested, relevant to the named activity: 2; somewhat accurate: 1.')),
('15d','1-4',[27],[21], 'Analyse the provision and support for excellence in performance in a named physical activity of your choice.',
 [('Analysis',12,'Excellent detail and accuracy: 12; good detail and accuracy: 9; some correct aspects and detail: 6; little analysis or accurate detail: 3.',[0,3,6,9,12])]),
('16ai','1-8',[28],[22], 'Make two statements about doping in cycling over recent years based on information presented in Figure 12.',
 [('Statements',2,'One mark per accurate graph-based statement. Examples: peak in 2007/2008; lowest in 2020; increase since 2020; decline over the 20-year period.')]),
('16aii','1-7',[28],[22], 'What is a code of ethics for sport?',
 [('Definition',2,'Accurate definition with appropriate examples: 2; some accuracy: 1.')]),
('16aiii','1-6',[28],[22], 'Explain the importance of equity in a named physical activity of your choice.',
 [('Importance',4,'Detailed and accurate explanation: 4; some accuracy: 2.',[0,2,4])]),
('16b','1-10',[28,29],[23], 'Discuss the challenges for performers who use sports supplements.',
 [('Discussion',8,'Detailed and accurate discussion: 7–8; good discussion with some detail and accuracy: 4–6; vague discussion: 1–3.')]),
('16c','1-9',[28,30],[23], 'Analyse the implications for the sport where anti-doping rules violations have been committed by its athletes.',
 [('Analysis',12,'Excellent detail and accuracy: 12; good detail and accuracy: 9; some correct aspects and detail: 6; little analysis and few accurate details: 3.',[0,3,6,9,12])]),
('16d','0-12',[31],[24], 'As part of your studies in Leaving Certificate Physical Education you designed a dietary plan for an athlete in a named physical activity of your choice. Outline three aspects of the dietary plan and provide a rationale for the inclusion of each aspect.',
 repeat('Aspect and rationale',3,4,'Appropriate aspect with detailed rationale relevant to the performer: 3–4; some accuracy in the rationale: 1–2.')),
('17a','1-1',[32],[25], 'Discuss the personal benefits of physical activity for health and wellbeing for people at two different life stages.',
 repeat('Life stage',2,4,'Detailed and accurate discussion of personal health and wellbeing benefits at the named life stage: 3–4; some accuracy: 1–2.')),
('17b','1-3',[33],[25], 'Describe two characteristics of people who positively impact and support the physical activity participation of others.',
 repeat('Characteristic',2,4,'Detailed and accurate description of an appropriate characteristic: 3–4; some accuracy: 1–2.')),
('17c','1-24',[34],[26], 'Write three statements that you would include in a code of practice for the selection of commercial sponsorship for a youth sports team. Justify why you would include each statement in this code of practice.',
 [fixed(f'Statement {i}',2,'Accurate statement for the youth team’s sponsorship code.') for i in range(1,4)]+[fixed(f'Justification {i}',2,'Appropriate justification for the corresponding statement.') for i in range(1,4)]),
('17di','1-3',[35],[26], 'Name a national policy that promotes physical activity engagement.',
 [fixed('National policy',2,'Appropriate national policy named.')]),
('17dii','1-3',[35],[26], 'Analyse how the policy named by you in Question 17(d)(i) promotes physical activity engagement.',
 [('Analysis',10,'Detailed, accurate analysis of how the policy promotes engagement in Ireland: 8–10; some detail and accuracy: 4–7; lacking detail and accuracy: 1–3.')]),
('18a','0-6',[36],[27], 'Define five components of health-related fitness.',
 [fixed(label,2,'Accurate definition of the correctly named health-related fitness component.') for label in ('Muscular strength','Muscular endurance','Body composition','Cardiorespiratory endurance','Flexibility')]),
('18bi','0-11',[36],[27], 'Define anxiety related to performance in physical activity.',
 [('Definition',2,'Accurate definition: 2; somewhat accurate: 1.')]),
('18bii','0-11',[36],[27], 'Discuss how anxiety may impact on an athlete’s performance in physical activity.',
 [('Discussion',4,'Detailed and accurate discussion: 3–4; some accuracy: 1–2.')]),
('18c','0-24',[37],[28], 'As part of your studies in Leaving Certificate Physical Education you designed a personal action plan to support a positive psychological disposition for performance. Outline three aspects of the action plan and provide a rationale for the inclusion of each aspect.',
 repeat('Aspect and rationale',3,4,'Appropriate aspect with detailed rationale for supporting psychological disposition: 3–4; some accuracy in the rationale: 1–2.')),
('18d','1-25',[38],[28], 'Analyse the involvement of a named business in sport.',
 [('Analysis',12,'Excellent detail and accuracy: 12; good detail and accuracy: 9; some correct aspects and detail: 6; little analysis and few accurate details: 3.',[0,3,6,9,12])]),
]
CONTEXT={
 '1a':'Figure 1 shows Cork gymnast Meg Ryan performing a floor exercise routine.',
 '8b':'First identify an injury and its potential cause in a named activity, as requested in 8(a). Describe treatment for that same injury.',
 '11a':'The source quotes a 2020 study concluding that rugby union refereeing is more physically demanding at higher competitive levels, particularly high-intensity efforts.',
 '15ai':'Read Figure 11, the Sport Ireland investment table for 2018–2023, on the original source page.',
 '15aii':'Figure 11’s NGB investment table is included as context; your named NGB is not restricted to that table.',
 '16ai':'Read the complete cycling anti-doping graph, including its axes, years and values, on original page 28.',
 '17dii':'Name a national physical activity policy as requested in 17(d)(i), then analyse that same policy.',
 '18d':'The Adidas and O’Neills photographs are examples on the original page; name a business of your choice.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete Paris 2024 Olympics and Rhasidat Adeleke case study, with its images and numerical data, on original page 14.'
VARIANTS={}
VARIANT_REQUIREMENTS={}
SOURCE_POOLS={}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any three'],[2,'or'],[3,'and/or'],[6,'named physical activity'],[8,'named physical activity'],[9,'named physical activity'],[9,'one of'],[12,'named physical activity'],[13,'named physical activity'],[20,'any three'],[20,'named physical activity'],[20,'and/or'],[21,'named physical activity'],[26,'named physical activity'],[27,'named physical activity'],[28,'named physical activity'],[31,'named physical activity'],[44,'or'],[44,'or']]
EXPECTED_POOL_SCAN=[[2,'any ten'],[2,'three of'],[3,'any ten'],[3,'of the following'],[9,'one of']]
SELECTION_REVIEW=[
 {'pages':[2,3,20],'kind':'exam-attempt-rule','reason':'Any ten short questions and any three long questions choose already represented tasks; no combined exam-attempt cards.'},
 {'pages':[2,44],'kind':'boilerplate','reason':'Pen colours and copyright wording are not task routes.'},
 {'pages':[3,20],'kind':'flexible-wording','reason':'Aesthetic and/or artistic and media and/or spectator allow a flexible response, not a fixed choice of named routes.'},
 {'pages':[3,22,26,34,36],'kind':'required-components','reason':'Both analysis headings, both lever classes in a comparison, all three test-battery rows, all three statements with justifications and all five HRF definitions are required.'},
 {'pages':[6,8,9,12,13,21,24,27,28,31,32,35,38],'kind':'open-choice-or-own-response','reason':'Activities, injuries, energy systems, NGBs, life stages, policies and businesses are open knowledge or the candidate’s own preceding answers. The investment table, life-stage photos and business photos are context, not finite printed selection pools.'},
 {'pages':[15],'kind':'source-extraction','reason':'Two scalar quantities are identified from case-study data. These are possible factual answers, not alternative essay routes or a printed named option pool.'},
]
