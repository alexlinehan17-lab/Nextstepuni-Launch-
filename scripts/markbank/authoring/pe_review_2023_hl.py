"""Independent visual sweep of all 48 paper and 56 scheme pages.

Written allocations: scheme PDF 4–34. Project 35–43; performance 45–53;
remaining pages are notes/blank/end matter. No finite printed choice pools.
Q8 uses a descending 3+3+2 allocation across three compulsory definitions.
Verified corrections: Q8 2→8, Q17(a)(iii) 3→2, Q18(b) 2→8.
"""
PAPER_PAGE_COUNT=48
SCHEME_PAGE_COUNT=56
ACKNOWLEDGEMENT_PAGE=47
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance):
    return [(f'{label} {i}',maximum,guidance) for i in range(1,n+1)]


TASKS=[
('1a','0-2',[3],[4], 'Name any two planes of human movement.',
 [('Planes',2,'One mark per correctly named plane. Sagittal, frontal, transverse.')]),
('1b','0-2',[3],[4], 'Describe the two planes of human movement, correctly named in (a). Use a sporting example of movement in each plane to support your answer.',
 repeat('Plane',2,3,'Clear, accurate description with correct sporting example: 3; accurate description with correct example: 2; only correct description or only correct example: 1.')),
('2','0-10',[4],[5], 'Explain two different methods of physical fitness training that could be used to help prepare athletes for performance in a physical activity of your choice.',
 repeat('Training method',2,4,'Correct method identified with excellent explanation of its impact on athlete preparation in the named activity: 3–4; correct method with some knowledge of its impact: 1–2.')),
('3a','1-22',[5],[6], 'What is social regulation of the body?',
 [('Description',2,'Clear and accurate description: 2; accurate description: 1.')]),
('3b','1-22',[5],[6], 'Discuss how social regulation of the body impacts on the participation levels of men and women in physical activity.',
 [('Discussion',6,'Detailed, clear and accurate discussion of impacts on both men and women: 5–6; accurate with some detail addressing both: 3–4; little detail, or only one gender with some accuracy/detail: 1–2.')]),
('4a','0-21',[6],[7], 'Identify what you believe are the two most important factors that influence performance in a physical activity of your choice.',
 [('Factors',2,'One mark per factor appropriate to the named activity with a direct impact on performance.')]),
('4b','0-21',[6],[7], 'Discuss why you believe that the factors, correctly named in (a), are the two most important factors that influence performance in your named physical activity.',
 repeat('Factor',2,3,'Clear, accurate discussion showing excellent understanding of why this is one of the two most important factors: 3; evidence of knowledge and understanding of its important impact: 2; vague effort: 1.')),
('5','1-3',[7],[8], 'Outline two ways in which pathways between school and community based physical activity could be strengthened.',
 repeat('Pathway',2,4,'Appropriate pathway clearly and accurately outlined with clear knowledge of how it can be strengthened: 4; good evidence of knowledge: 3; some evidence: 2; appropriate pathway named: 1.')),
('6','1-6',[8],[9], 'Discuss the notion that: “Sportsmanship may lead to enhanced engagement in physical activity, while gamesmanship may contribute to lowering levels of engagement in physical activity.”',
 [('Discussion',8,'Discuss both sportsmanship enhancing engagement and gamesmanship reducing engagement. Excellent, detailed and accurate: 7–8; good, accurate: 5–6; some discussion and somewhat accurate: 3–4; effort with information accurate in parts: 1–2.')]),
('7a','0-2',[9],[10], 'Which of Newton’s laws of motion can be used to calculate the acceleration of a rugby ball which has been kicked?',
 [fixed('Law',2,'Newton’s second law. Accept F = ma or law of acceleration.')]),
('7b','0-2',[9],[10], 'Name and define another one of Newton’s laws of motion.',
 [fixed('Law and definition',2,'Newton’s first law (inertia) or third law (reaction), with an accurate definition. Must differ from 7(a).')]),
('7c','0-2',[9],[10], 'Explain why you would use Newton’s laws of motion when analysing human movement.',
 [('Explanation',4,'Detailed, accurate explanation with clear understanding of forces in sport: 3–4; some detail/accuracy and some understanding: 1–2.')]),
('8','0-17',[10],[11], 'Define each of the following terms as they relate to physical activity: rules, rituals and conventions.',
 [('First definition assessed',3,'Clear and accurate: 3; accurate: 2; little clarity or accuracy: 1. All three terms are compulsory; the scheme awards 3 + 3 + 2 across the definitions.'),('Second definition assessed',3,'Clear and accurate: 3; accurate: 2; little clarity or accuracy: 1.'),('Third definition assessed',2,'Clear and accurate: 2; accurate or limited clarity: 1. This is the reduced third allocation, not an extra answer route.')]),
('9','0-3',[11],[11], 'Describe two principles of effective practice that could have been utilised in the design of Olatunde’s practice schedules.',
 repeat('Practice principle',2,4,'Clear, accurate description of correct principle and use in Olatunde’s schedule: 3–4; accurate description with some clarity about use: 2; correct principle identified with little detail: 1.')),
('10','0-12',[12],[12], 'Describe how any two energy systems used by the human body may contribute to performance in a physical activity of your choice.',
 repeat('Energy system',2,4,'Excellent understanding with detailed, accurate contribution to performance in the named activity: 4; good, accurate understanding: 3; some knowledge: 2; vague description: 1.')),
('11','1-20',[13],[13], 'Having conducted a survey on the physical activity patterns and behaviours of boys and girls in a school, the PE teacher discovered that the boys in the school were far more active than the girls. Discuss two ways in which a school could tackle a gender imbalance in physical activity participation levels.',
 repeat('Way',2,4,'Correct way identified and discussed clearly and accurately, showing how it tackles the gender imbalance: 3–4; correct way discussed with some information on its impact: 1–2.')),
('12a','0-11',[14],[13], 'Outline how the psychological factor concentration can impact the performance levels of an athlete.',
 [('Outline',4,'Clear and accurate outline: 3–4; correct outline: 1–2.')]),
('12b','0-11',[14],[13], 'Describe one strategy that an athlete might use to enhance their concentration for performance.',
 [('Strategy',4,'Clear and accurate description including how the strategy enhances concentration and performance: 3–4; appropriate description: 1–2.')]),
('13a','1-2',[15,16,17],[14], '“Sport” is a concept of physical activity. Explain “sport”.',
 [('Explanation',6,'Excellent, clear, accurate and detailed explanation with correct examples: 5–6; good explanation with some detail and correct examples: 3–4; fair, vague information: 1–2.')]),
('13b','0-3',[15,16,17],[14], 'Discuss the importance of two different types of feedback that a coach could use to enhance athlete performance, in a physical activity of your choice.',
 repeat('Feedback type',2,5,'Appropriate type discussed in excellent, accurate detail with clear impact on performance in the named activity: 5; detailed and accurate discussion showing impact: 3–4; appropriate discussion showing how it helps performance: 1–2.')),
('13c','1-2',[15,16,18],[15], 'Examine the main influences that impact on the participation patterns of young people in physical activity and sport.',
 [('Examination',10,'Accurate and detailed examination of a variety of influences, explaining their impact with excellent understanding: 8–10; accurate with some influences and some detail: 4–7; basic information/limited examination with at least one correct influence: 1–3.')]),
('13d','0-3',[15,16,19],[16], 'Describe the performance of a named skill by athletes at three different stages of skill learning.',
 [('Stages named',3,'One mark per correctly named stage.')]+repeat('Stage description',3,3,'Describe the skill at the correct stage. Excellent, clear, precise detail about patterns/features and understanding: 3; good description and understanding: 2; poor/vague description: 1.')),
('13e','0-2',[15,16,20],[17], 'Examine how economy of movement may impact on the quality/effectiveness of a named skill in a physical activity of your choice.',
 [('Examination',12,'Excellent account of economy of movement and detailed, accurate examination of its effect on quality/effectiveness of the named skill: 9–12; some detail and understanding with some accuracy: 5–8; basic information and limited examination/understanding: 1–4.')]),
('14ai','1-2',[21],[18], '“Outdoor and adventure activities” is a concept of physical activity. Define “outdoor and adventure activities”.',
 [('Definition',2,'Clear, accurate understanding: 2; some understanding/accuracy: 1.')]),
('14aii','1-2',[21],[18], 'Name four “outdoor and adventure activities”, other than water activities.',
 [('Activities',4,'Four correct non-water outdoor/adventure activities: one mark each.')]),
('14bi','0-11',[22],[19], 'Define confidence related to sports performance.',
 [('Definition',2,'Clear and accurate understanding: 2; some understanding/accuracy: 1.')]),
('14bii','0-11',[22],[19], 'Discuss how confidence can impact performance in a physical activity of your choice.',
 [('Discussion',8,'Clear, detailed and accurate discussion of confidence’s impact in a named activity: 7–8; some accuracy/detail and understanding: 4–6; limited effort with some correct information: 1–3.')]),
('14c','1-1',[23],[20], 'Discuss three social benefits of physical activity for teenagers.',
 repeat('Social benefit',3,4,'Correct benefit with accurate, clear and detailed discussion: 4; correct benefit with accurate discussion: 3; correct benefit with some discussion/accuracy: 1–2.')),
('14d','0-10',[24],[20], 'Examine the impact that any two principles of training can have on the performance of an athlete.',
 repeat('Training principle',2,6,'Correct principle with detailed, accurate, clear and precise examination of its impact: 5–6; good examination, mostly clear and accurate: 3–4; some accurate information: 1–2.')),
('15a','0-16',[25],[21], 'Discuss the importance of selecting and maintaining suitable equipment in a physical activity of your choice.',
 [('Discussion',10,'Clear, detailed and accurate discussion of both selection and maintenance of equipment relevant to the named activity: 8–10; some detail/accuracy addressing both: 4–7; basic, limited detail and may neglect either aspect: 1–3.')]),
('15bi','1-10',[26],[22], 'Name two sports nutrition supplements commonly used by athletes.',
 [('Supplements',2,'One mark per accurately named sports nutrition supplement.')]),
('15bii','1-10',[26],[22], 'Explain how one of the supplements named by you in (i) can help optimise athlete performance.',
 [('Explanation',4,'Excellent, detailed, accurate, clear and concise explanation of how the correctly identified supplement optimises performance: 3–4; accurate but vague/undetailed: 1–2.')]),
('15ci','1-8',[27],[23], 'According to Figure 17 the Weightlifting Ireland athlete used the anabolic steroid Nandrolone. Identify two reasons why this athlete might have used an anabolic steroid.',
 [fixed(f'Reason {i}',2,'Correct reason for using an anabolic steroid.') for i in (1,2)]),
('15cii','1-8',[27],[23], 'Identify another category of performance enhancing drug and state one way in which a substance from this category might affect athlete performance.',
 [fixed('Category',2,'Correct category other than anabolic steroids.'),('Effect',2,'Clear and accurate statement of an effect on performance: 2; accurate statement: 1.')]),
('15ciii','1-9',[27,28],[23], 'Figure 17 states that there is no information available on the substance that the Motorsport Ireland athlete was banned for. State two anti-doping rules that this athlete may have violated.',
 [fixed(f'Rule {i}',2,'Correctly stated anti-doping rule that may have been violated.') for i in (1,2)]),
('15di','1-24',[26,29],[24], 'What is sponsorship in sport?',
 [('Explanation',2,'Accurate, clear and concise: 2; some accurate information: 1.')]),
('15dii','1-24',[26,29],[24], 'Examine the positive impact that Leona’s sponsorship deals may have for her.',
 [('Examination',10,'Clear and accurate examination of a range of positive impacts with detailed application to Leona: 7–10; clear/accurate in parts and some impacts examined in some detail: 4–6; basic information with at least one positive impact: 1–3.')]),
('16a','0-9',[30],[25], 'Name and justify the selection of four tests that you would include in a physical fitness test battery for a physical activity of your choice.',
 [('Tests named',4,'Four tests appropriate to the named activity: one mark each.')]+repeat('Justification',4,2,'Detailed and accurate justification of why the test belongs in the activity’s test battery: 2; correct justification: 1.')),
('16b','0-10',[31],[25], 'Describe the FITT formula.',
 [(term,2,'Clear, accurate description of the correctly named variable and its use: 2; accurate information with limited/no detail: 1.') for term in ('Frequency','Intensity','Time','Type')]),
('16c','1-25',[32],[26], 'Discuss two ways that the growth of mass participation sporting events has provided opportunities for business and enterprise in recent years.',
 repeat('Business opportunity',2,4,'Excellent, detailed, clear, relevant and accurate discussion: 3–4; limited discussion with accurate information but little detail: 1–2.')),
('16d','0-23',[33],[27], 'Compare two physical activities of your choice from the perspective of the artistic/aesthetic criteria of performance in the activities. At least one of the physical activities selected must be an artistic/aesthetic activity.',
 [('Comparison',12,'Compare both activities and their similarities/differences using specific aesthetic/artistic criteria; at least one activity must be artistic/aesthetic. Excellent knowledge, clear/detailed/accurate: 10–12; good knowledge with detail: 7–9; knowledge and some accurate detail: 4–6; some knowledge and effort to compare: 1–3.')]),
('17ai','0-10',[34],[28], 'Define periodisation.',
 [('Definition',2,'Accurate, clear and detailed: 2; some accuracy: 1.')]),
('17aii','0-5',[34],[28], 'Identify four components of fitness that are being targeted at some stage during the plan in Figure 19.',
 [('Components',4,'One mark each: power, speed, strength, cardiorespiratory endurance.')]),
('17aiii','0-10',[34],[28], 'State what the athlete is expected to do during “Block 3” of the periodised plan in Figure 19.',
 [('Block 3',2,'All four correct: 2; partial correct response (three or fewer): 1. Fast plyometric exercises; light loaded power; low repetitions for strength; short intervals for conditioning.')]),
('17b','0-12',[35],[29], 'Examine two nutritional considerations that an athlete may implement after performance to enhance recovery. You are not permitted to use hydration or sports drinks.',
 repeat('Nutritional consideration',2,5,'Correctly named consideration with excellent, detailed, accurate examination of how it enhances recovery: 5; good, clear and accurate examination: 3–4; correctly named with an accurate attempt at examination: 1–2. No hydration or sports drinks.')),
('17c','1-25',[36],[29], 'Sports tourism is big business! Discuss how sports marketing can impact on the development of tourism in Ireland.',
 [('Discussion',10,'Excellent, clear and detailed discussion showing understanding of marketing and its potential impact on Irish tourism: 7–10; good, accurate discussion with some detail: 4–6; some discussion with limited information/detail: 1–3.')]),
('17d','1-24',[37],[30], 'Analyse two different forms of sport related advertising in relation to the messages they give to young people.',
 repeat('Advertising form',2,6,'Detailed, accurate and appropriate analysis, clear knowledge, relevant information and justified opinion: 5–6; mostly detailed/accurate with knowledge and clear opinion: 3–4; accurate analysis showing basic knowledge and some relevant information: 1–2.')),
('18ai','0-1',[38],[31], 'Define ability.',
 [('Definition',2,'Accurate, clear and detailed: 2; some accuracy: 1.')]),
('18aii','0-1',[38],[31], 'Are ability and skill the same thing? Justify your response.',
 [('Justification',6,'No, with accurate, detailed justification conveying the difference: 5–6; no, with accurate justification: 3–4; no with little detail or some inaccuracies: 1–2.')]),
('18b','1-6',[39],[32], 'Identify two principles of ethical practice and outline why they are important for sport.',
 [('Principles',2,'One mark per correctly identified principle. Accept respect, integrity, fairness, equity.')]+repeat('Importance',2,3,'Correct principle with clear, accurate and detailed outline of importance: 3; outline with some detail: 2; limited outline: 1.')),
('18ci','1-21',[40],[33], 'Define body image.',
 [('Definition',2,'Accurate, clear and detailed: 2; some accuracy: 1.')]),
('18cii','1-21',[40],[33], '“By showcasing lean bodies of women and sculpted muscular bodies of men the media are helping to promote physical activity participation in young women and men.” Discuss the validity of this statement.',
 [('Discussion',8,'May agree, disagree or partly agree. Excellent, detailed and accurate discussion clarifying judgement: 7–8; good discussion with some detail and accuracy: 4–6; limited/unclear discussion with some relevant information: 1–3.')]),
('18di','1-22',[41],[34], 'Identify two characteristics associated with hegemonic femininity.',
 [('Characteristics',2,'One mark per accurate characteristic.')]),
('18dii','1-22',[41],[34], 'Explain why the characteristics, correctly identified by you in (i), might impact on the participation of girls in sport and physical activity.',
 repeat('Characteristic',2,6,'Clear, accurate and detailed explanation linking the characteristic to participation levels: 5–6; accurate with some detail and mostly correct explanation of impact: 3–4; basic information with little understanding: 1–2.')),
]

CONTEXT={
 '1b':'Name two planes as requested in 1(a), then describe and exemplify those same planes.',
 '4b':'Choose a physical activity and identify its two most important performance factors as requested in 4(a). Discuss those same factors.',
 '5':'Figure 4 reports positive outcomes from a school–community linked intervention. The original study title and authors are on the source page.',
 '7b':'Part 7(a) asks which law calculates acceleration of a kicked rugby ball. Name and define a different law for this part.',
 '9':'Israel Olatunde ran 10.17 seconds in the 100 m at the European Athletics Championships in Munich on 16 August 2022.',
 '15bii':'Name two sports nutrition supplements as requested in 15(b)(i), then explain one of your own choices. The original Kinetica/Leona Maguire context is included.',
 '15cii':'The preceding part concerns an athlete’s use of the anabolic steroid Nandrolone. Use another drug category.',
 '15dii':'Leona Maguire has a Kinetica partnership and deals with Puma, KPMG, Davy, Kingspan, Kastus and the Slieve Russell Golf Club.',
 '18dii':'Identify two characteristics associated with hegemonic femininity as requested in 18(d)(i). Explain the impact of those same characteristics.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the coaching case study on original paper pages 15–16, including the coaching statistics, before answering this part.'

CHOICES={}
SOURCE_POOLS={}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any 10'],[2,'any three'],[2,'or'],[3,'or'],[3,'any two'],[6,'named physical activity'],[9,'one of'],[12,'any two'],[15,'one of'],[15,'or'],[21,'any three'],[24,'any two'],[26,'one of'],[33,'one of'],[35,'or'],[47,'or'],[48,'or'],[48,'or']]
SELECTION_REVIEW=[
 {'pages':[2,21],'kind':'exam-attempt-rule','reason':'Section choices determine which already represented questions a candidate attempts; no compound exam-attempt cards.'},
 {'pages':[2,3,15,47,48],'kind':'context-or-boilerplate','reason':'Pen colours, exercise or other activities, descriptive coaching text, URL and copyright wording are not task routes.'},
 {'pages':[3,9,12,24,39],'kind':'open-knowledge-response','reason':'Planes, another Newton law, energy systems, training principles and ethical principles are requested from subject knowledge. The paper prints no named option pool. The unlabelled body-plane illustration is explanatory, not a labelled selection list. Do not add scheme-only options to the question.'},
 {'pages':[6,26,33,35],'kind':'open-choice-or-own-response','reason':'Physical activities are open; the supplement is chosen from the candidate’s own preceding answer; the artistic activity requirement constrains an open choice; hydration and sports drinks are excluded, not offered as routes.'},
 {'pages':[10,19,31,34],'kind':'required-headings','reason':'All three definitions, all three skill-learning stages, all FITT elements and the requested table observations are compulsory response components. No alternative-route expansion.'},
]

# Supplemental raw scan for printed-pool wording without a choose/select verb.
EXPECTED_POOL_SCAN=[[2, '10 of'], [2, 'three of'], [3, 'any ten'], [9, 'one of'], [10, 'of the following'], [15, 'one of'], [26, 'one of'], [33, 'one of']]

SELECTION_REVIEW.append({'pages':[3],'kind':'exam-attempt-rule','reason':'Any ten is the same Section A attempt rule as any 10 on page 2.'})
