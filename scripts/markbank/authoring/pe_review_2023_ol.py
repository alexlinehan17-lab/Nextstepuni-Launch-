"""Independent visual review: all 36 paper and 44 scheme PDF pages.

Written allocations scheme 5–24; project 25–33; performance 34–40;
remaining pages are notes, blanks and end matter. Q9 and Q12 consist of
four separately marked items; their original IDs follow the first item.
Q10: choose two of three (3 routes). Q16(c): choose two of four (6 routes).
Verified old tariff corrections: Q5 5→8; Q14(a)(i) 4→8; Q16(c) 8→16.
"""

PAPER_PAGE_COUNT=36
SCHEME_PAGE_COUNT=44
ACKNOWLEDGEMENT_PAGE=35
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}
CARD_ID_OVERRIDES={'9a':'pe-2023-ol-q9','12a':'pe-2023-ol-q12'}
PART_REF_OVERRIDES={**{f'9{part}':f'Q9 · row {i}' for i,part in enumerate('abcd',1)},**{f'12{part}':f'Q12 · statement {i}' for i,part in enumerate('abcd',1)}}
ID_CORRECTIONS=[{'id':f'pe-2023-ol-q{q}','part':f'{q}a','reason':'Four independently marked two-mark items replace the former composite. Preserve the existing ID on the first item; add three new IDs. Display row/statement labels because the paper does not print part letters.'} for q in (9,12)]


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


MATCH_OPTIONS='Choose from: state anxiety, trait anxiety, intrinsic motivation, extrinsic motivation.'
TASKS=[
('1a','0-6',[3],[5], 'Name one of the most important health related components of fitness (HRF) for a physical activity of your choice.',
 [fixed('Component',2,'Relevant health-related fitness component for the chosen activity.')]),
('1b','0-9',[3],[5], 'Name and describe a fitness test that can be used to measure this component of fitness.',
 [fixed('Test',2,'Correct test for the component named in 1(a).'),('Description',4,'Full description including correct setup, measurements and procedure: 4; at least two correct steps: 2.',[0,2,4])]),
('2','0-10',[4],[5], 'Describe two strategies that could be used to aid recovery after a training session.',
 repeat('Recovery strategy',2,4,'Detailed description: 4; limited description: 2.',[0,2,4])),
('3','0-14',[4],[6], 'Basketball has zone defence. Figure skating has interpretation of music. Identify one structure/strategy/compositional element from a physical activity of your choice. Explain why it might give a performance advantage if used during competition. You may not use zone defence or interpretation of music in your answer.',
 [fixed('Element named',2,'Relevant structure, strategy or compositional element for the chosen activity.'),('Explanation',6,'Clear and accurate explanation of effectiveness and performance advantage: 6; explanation of effectiveness in competition: 2–3. Do not use either excluded example.',[0,2,3,6])]),
('4','1-12',[5],[6], 'Outline two supports and two barriers to physical activity participation in the community.',
 [fixed(label,2,'Correctly identified support or barrier, as requested.') for label in ('Support 1','Support 2','Barrier 1','Barrier 2')]),
('5','1-10',[5],[7], 'Name a sports supplement and a reason for using it.',
 [fixed('Supplement',3,'Correct supplement named.'),('Reason',5,'Detailed positive effect on sports performance: 5; effect on sports performance: 2.',[0,2,5])]),
('6a','1-2',[6],[7], 'Name two methods of collecting data about physical activity participation.',
 [fixed(f'Method {i}',2,'Correct method of data collection.') for i in (1,2)]),
('6b','1-2',[6],[7], 'What type of information is collected by each of these methods?',
 [fixed(f'Information type {i}',2,'Correct information type for the corresponding method named in 6(a).') for i in (1,2)]),
('7a','0-1',[6],[7], 'Name two characteristics of skilled performance.',
 [fixed(f'Characteristic {i}',2,'Correct characteristic of skilled performance.') for i in (1,2)]),
('7b','0-1',[6],[7], 'Define skill.',
 [fixed('Definition',2,'Learned movement patterns performed effectively and efficiently, acquired through training and practice.')]),
('7c','0-22',[6],[7], 'Identify one method of analysing a skilled performance.',
 [fixed('Analysis method',2,'Relevant method with a brief distinguishing fact or feature.')]),
('8','0-16',[7],[8], 'Organisers of a physical activity event need to take many factors into consideration. Describe two things they should do to ensure the safety of all participants.',
 repeat('Safety measure',2,4,'Clear, accurate description related to organisers ensuring participant safety: 4; correctly named precaution: 2.',[0,2,4])),
('9a','0-11',[7],[8], 'Match this explanation to a psychological factor: “Having a desire to participate in order to achieve positive recognition e.g. to win prizes.” '+MATCH_OPTIONS,
 [fixed('Match',2,'Extrinsic motivation.')]),
('9b','0-11',[7],[8], 'Match this explanation to a psychological factor: “A temporary emotional state that only occurs in certain situations.” '+MATCH_OPTIONS,
 [fixed('Match',2,'State anxiety.')]),
('9c','0-11',[7],[8], 'Match this explanation to a psychological factor: “A general emotional state.” '+MATCH_OPTIONS,
 [fixed('Match',2,'Trait anxiety.')]),
('9d','0-11',[7],[8], 'Match this explanation to a psychological factor: “Having a desire to participate to gain satisfaction from the activity.” '+MATCH_OPTIONS,
 [fixed('Match',2,'Intrinsic motivation.')]),
('10','1-24',[8],[9], 'Explain two of the following terms: sports endorsement; sports merchandising; sports related advertising.',
 repeat('Term',2,4,'Clear and accurate explanation: 4; attempt lacking full clarity: 2–3; example without explanation: 1.')),
('11a','1-22',[9],[9], 'Explain hegemonic masculinity.',
 [('Explanation',4,'Full and correct definition/explanation, with examples if needed: 4; correct terms or basic understanding: 3; lacking clarity: 1–2.')]),
('11b','1-22',[9],[9], 'Explain hegemonic femininity.',
 [('Explanation',4,'Full and correct definition/explanation, with examples if needed: 4; correct terms or basic understanding: 3; lacking clarity: 1–2.')]),
('12a','1-9',[9],[10], 'State whether this statement is true or false: Sport Ireland is responsible for anti-doping in Ireland.',
 [fixed('Answer',2,'True.')]),
('12b','1-8',[9],[10], 'State whether this statement is true or false: The main performance enhancing effect of anabolic steroids is to improve alertness and reduce tiredness.',
 [fixed('Answer',2,'False.')]),
('12c','1-9',[9],[10], 'State whether this statement is true or false: Athletes are allowed 5 whereabouts failures in 12 months.',
 [fixed('Answer',2,'False.')]),
('12d','1-6',[9],[10], 'State whether this statement is true or false: Putting the ball out of play when an opponent is injured is an example of sportsmanship.',
 [fixed('Answer',2,'True.')]),
('13ai','1-24',[10,11,12],[11], 'Define sponsorship.',
 [('Definition',2,'Clear and precise: 2; attempt missing clarity: 1.')]),
('13aii','1-24',[10,11,12],[11], 'Explain two ways that Ellen Keane could benefit from her sponsorship deals.',
 repeat('Benefit',2,3,'Relevant explanation of how Ellen can benefit: 3; attempt at explanation: 1–2.')),
('13bi','1-21',[10,11,13],[12], 'Serena Williams has discussed body image from an athlete’s perspective. Read her quotes in the case study. Explain body image using an example.',
 [('Explanation',4,'Clear and accurate explanation with example: 4; attempted explanation with appropriate example: 2–3; attempt without example, or appropriate example only: 1.')]),
('13bii','1-21',[10,11,13],[12], 'Read Serena Williams’ quotes in the case study. Discuss how female body image can be influenced by their physical activity participation.',
 [('Discussion',8,'Detailed discussion of body image and influences of physical activity supported by evidence: 6–8; accurate discussion with some evidence: 3–5; review without examples or incorrect association: 1–2.')]),
('13c','1-21',[10,11,14],[12], 'Explain how participation levels in certain sports can be affected by the type of clothing that you are required to wear.',
 [('Explanation',6,'Relevant explanation linking participation to sports clothing and a specific scenario: 6; participation explained but reason unclear: 3–4; clothing described without impact on participation: 1–2.',[0,1,2,3,4,6])]),
('13di','0-12',[10,11,15],[13], 'Identify the main energy system for each of these three sports/athletes: Ellen Keane—100m breaststroke; Serena Williams—tennis serve; Grace O’Brien—70-minute camogie match.',
 [fixed('Ellen Keane',2,'Anaerobic.'),fixed('Serena Williams',2,'ATP-PC / anaerobic.'),fixed('Grace O’Brien',2,'Aerobic.')]),
('13dii','0-7',[10,11,15],[13], 'Identify the main performance related fitness (PRF) component for each of these three sports/athletes: Ellen Keane—100m breaststroke; Serena Williams—tennis serve; Grace O’Brien—70-minute camogie match.',
 [fixed('Ellen Keane',2,'Power, coordination or reaction time.'),fixed('Serena Williams',2,'Speed, power or reaction time.'),fixed('Grace O’Brien',2,'Agility, coordination, reaction time or speed.')]),
('13diii','0-7',[10,11,15,16],[13], 'Explain each of the performance related fitness components you have answered in (ii) and give an example of any other sport/physical activity of your choice where this component is important.',
 [(f'Component {i}: explanation',2,'Clear and accurate explanation of the identified component relevant to the activity: 2; correct explanation: 1.') for i in (1,2,3)]+[fixed(f'Component {i}: other activity',2,'Correct matching example from a different physical activity.') for i in (1,2,3)]),
('14ai','0-3',[17],[14], 'Describe an activity that could be used to improve performance in a named skill from a physical activity of your choice. You may use a diagram.',
 [fixed('Skill',2,'Relevant skill.'),fixed('Drill/practice',2,'Suitable drill or practice to improve the skill.'),('Coaching points',4,'At least two relevant coaching/key points: 4; one point: 2.',[0,2,4])]),
('14aii','0-3',[17],[14], 'Explain why the activity that you have described is an effective way to learn the named skill.',
 [('Explanation',8,'Very clear rationale for the previous practice method, explaining why/how it teaches the skill: 7–8; attempts to explain reasons: 4–6; reasons omitted: 1–3.')]),
('14b','0-3',[18],[15], 'Outline two stages of skill learning.',
 repeat('Stage',2,5,'Named stage with clear description: 5; named stage with unclear description: 3–4; name only: 2.',[0,2,3,4,5])),
('14ci','0-2',[18],[15], 'Define Newton’s second law of motion.',
 [fixed('Definition',4,'Full, correct definition of Newton’s second law.')]),
('14cii','0-2',[18],[15], 'Name a skill from a physical activity of your choice and explain a creative application of this skill.',
 [fixed('Skill',2,'Relevant skill from the named activity.'),('Creative application',8,'Correct creative example with clear explanation and reason for use: 8; explained but reason omitted: 5–7; poor explanation: 3–4; no explanation: 2.',[0,2,3,4,5,6,7,8])]),
('15ai','1-26',[19],[16], 'Explain mass participation sports.',
 [('Explanation',4,'Clear and accurate: 4; unclear explanation: 2.',[0,2,4])]),
('15aii','1-1',[19],[16], 'Discuss two economic benefits of physical activity participation.',
 repeat('Economic benefit',2,4,'Considered, balanced review supported by appropriate evidence: 4; economic benefit named without discussion/explanation: 1. Do not accept social, mental or physical benefits.',[0,1,4])),
('15b','0-10',[20],[16], 'Name and explain three different principles of training.',
 [('Principles named',3,'One mark per correct principle.')]+repeat('Explanation',3,3,'Name and explanation match and are clear and accurate: 3; name and attempted explanation: 2.',[0,2,3])),
('15ci','0-10',[21],[17], 'What is periodisation?',
 [('Explanation',4,'Clear and accurate description including cycles/phases: 4; attempted explanation: 2.',[0,2,4])]),
('15cii','0-10',[21],[17], 'Why is periodisation used in sports coaching?',
 [('Purpose',4,'Purpose clearly applied to sports coaching: 4; main purpose identified with limited application: 2.',[0,2,4])]),
('15ciii','0-10',[21],[17], 'Outline two named cycles/phases used in periodisation.',
 repeat('Cycle/phase',2,4,'Correctly named cycle/phase: 2; accurate outline: 2.',[0,2,4])),
('16ai','0-12',[22],[18], 'In a physical activity of your choice, state what nutrients an athlete should eat on the day of an event. Complete all three headings: before the event, during the event, after the event.',
 [fixed(phase,2,'Appropriate nutrient for this phase of the event.') for phase in ('Before','During','After')]),
('16aii','0-12',[22],[18], 'Give a reason for selecting each nutrient: before the event, during the event and after the event.',
 [fixed(phase,4,'Correct reason for the nutrient eaten at this phase, matching 16(a)(i).') for phase in ('Before','During','After')]),
('16b','0-12',[22,23],[18], 'For each of the nutrients named in (a), give an example of a type of food that could be eaten on the day of the event to ensure that the athlete gets the appropriate nutrient. Include before, during and after the event.',
 [fixed(phase,2,'Food named is a major source of the nutrient previously named.') for phase in ('Before','During','After')]),
('16c','0-11',[23],[19], 'Explain two psychological factors from the list below and describe the impact that they can have on performance: confidence, anxiety, motivation, concentration.',
 repeat('Psychological factor',2,8,'Clear and accurate explanation and full description of impact: 8 (4 + 4); one part fully answered: 4; limited attempt to explain or describe: 2.',[0,2,4,8])),
('17a','1-9',[24],[20], 'Explain Therapeutic Use Exemption (TUE).',
 [fixed('Description',2,'Accurate description of a TUE.'),fixed('Grounds',2,'Correct grounds for granting a TUE.')]),
('17bi','1-8',[24],[20], 'Give an example of a Performance Enhancing Drug (PED) in each of the two categories: anabolic agents; stimulants. The table already gives human growth hormone as the example for peptide hormones.',
 [fixed('Anabolic agent',2,'Correct example.'),fixed('Stimulant',2,'Correct example.')]),
('17bii','1-8',[24],[20], 'Explain why an athlete might use a PED.',
 [('Explanation',4,'Clear and accurate explanation including personal, monetary or physical benefits: 4; limited explanation: 2.',[0,2,4])]),
('17biii','1-8',[25],[21], 'Discuss two negative implications of using PEDs.',
 repeat('Negative implication',2,4,'Clear, detailed discussion of an accurate implication with a developed point explaining why it is negative: 4; somewhat detailed discussion: 2.',[0,2,4])),
('17ci','0-15',[26],[21], 'In a physical activity of your choice identify a performer role. Describe two demands on a performer in that role. You may not refer to fitness.',
 [fixed('Performer role',2,'Correct performer role.')]+repeat('Demand',2,4,'Demand relevant to the role accurately described: 4; accurately stated: 2. Do not refer to fitness.',[0,2,4])),
('17cii','0-18',[26],[21], 'In the same physical activity, explain why a coach needs to manage practice/training time effectively.',
 [('Explanation',4,'Clear and accurate reasons relevant to the activity in 17(c)(i): 4; accurate reason: 2.',[0,2,4])]),
('17ciii','0-19',[26],[21], 'Outline two demands of a named official in the same physical activity.',
 [fixed('Official',2,'Correctly named official in the activity from 17(c)(i).'),fixed('Demand 1',2,'Appropriate demand.'),fixed('Demand 2',2,'Appropriate demand.')]),
('18ai','1-25',[27],[22], 'Explain sports marketing.',
 [fixed('Explanation',2,'Accurate explanation of sports marketing.')]),
('18aii','1-25',[27,28],[22], 'Describe the impact that hosting sporting events like the Red Bull Cliff Diving can have on the development of tourism in Ireland.',
 [('Impact',6,'Clear link between hosting and developing Irish tourism, describing positive and/or negative impacts: 6; impacts described without tourism development: 3–4; no link between hosting and tourism: 1–2.',[0,1,2,3,4,6])]),
('18bi','1-2',[29],[23], 'Figure 9 shows the percentage of students who participate in school sport outside of the Physical Education class. Which group of students participate the most in school sport?',
 [fixed('Group',2,'Boys, 70%.')]),
('18bii','1-2',[29],[23], 'Outline two possible reasons why this group participate more in school sport.',
 repeat('Reason',2,3,'Clear and valid outline: 3; reason given: 1. Relate to the group with the highest participation in Figure 9.',[0,1,3])),
('18biii','1-3',[29],[23], 'Suggest ways to increase participation in physical activity for school children.',
 [('Suggestions',8,'Two or more valid and reasonable ways relevant to school children: 6–8; one valid/reasonable way only: 3–5; unclear explanation or not applicable to school children: 1–2.')]),
('18ci','1-21',[30],[24], 'Do these magazine covers highlight how media represents male and female athletes differently? Explain your answer.',
 [('Explanation',6,'Answer with clear and relevant explanation/justification: 6; answer with some explanation: 3–5; answer without explanation: 1.',[0,1,3,4,5,6])]),
('18cii','1-21',[30],[24], 'Discuss how media representation of the body may affect young men’s participation in physical activity/sport.',
 [('Discussion',10,'Clear, accurate discussion connecting media representations and young men’s participation, with positive and negative points and examples: 8–10; examples and attempted explanation of impact on participation: 5–7; participation discussed with limited media connection: 3–4; limited discussion of either media or participation: 1–2.')]),
]

CONTEXT={
 '1b':'Choose an activity and name its important health-related fitness component as requested in 1(a). Use that same component for the test.',
 '6b':'Name two methods of collecting participation data as requested in 6(a). Identify the type of information each of those same methods collects.',
 '14aii':'First describe a practice activity to improve a named skill as requested in 14(a)(i). Explain the effectiveness of that same activity.',
 '16aii':'Choose a physical activity and identify the appropriate nutrients before, during and after its event as requested in 16(a)(i). Give reasons for those same nutrients.',
 '16b':'Use the before/during/after nutrients selected in 16(a). The preceding task and table are included in the source pages.',
 '17cii':'Use the physical activity chosen for the performer role in 17(c)(i).',
 '17ciii':'Use the physical activity chosen for the performer role in 17(c)(i).',
 '18ai':'The paper introduces Red Bull Cliff Diving events on Inis Mór and in Dún Laoghaire. Read the source image on page 27.',
 '18aii':'The article and photograph about the Dún Laoghaire event are on the included original page 27.',
 '18bii':'Read Figure 9 and identify its highest-participation group as requested in 18(b)(i). Explain that group’s higher participation.',
 '18ci':'Refer to both Sports Illustrated covers in Figure 10 on the included original page 30.',
 '18cii':'Figure 10’s magazine covers and the surrounding question context are included on the source page.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete case study about Ellen Keane, Serena Williams and Grace O’Brien on original pages 10–11.'
CONTEXT['13diii']+=' Choose the three fitness components required in 13(d)(ii), then explain those components and give examples from other activities.'

MARKETING=['Sports endorsement','Sports merchandising','Sports related advertising']
PSYCHOLOGY=['Confidence','Anxiety','Motivation','Concentration']
# A printed choice is ONE card (AGENTS.md, 2026-10-12): the printed question
# with its whole pool, the scheme's own grid, and for choose-N the printed
# instruction plus one criterion per chosen item. pe_complete.py emits one card.
CHOICES={
 '10':{'choose':2,'pool':MARKETING,'instruction':'Explain two of the following terms:','slots':['First term you chose','Second term you chose']},
 '16c':{'choose':2,'pool':PSYCHOLOGY,'instruction':'Explain two psychological factors from the list below and describe the impact that they can have on performance.','slots':['First factor you chose','Second factor you chose']},
}
SOURCE_POOLS={
 '10':[(8,'Explain two of the following terms:'),(8,'Sports endorsement'),(8,'Sports merchandising'),(8,'Sports related advertising')],
 '16c':[(23,'Explain two psychological factors from the list below'),(23,'Confidence'),(23,'Anxiety'),(23,'Motivation'),(23,'Concentration')],
}
# Additional Topic Atlas headings, decided 2026-10-11 from the SEC paper,
# scheme and NCCA specification (StudyClix parity audit).
# Q5 asks for a sports supplement and a reason for using it; NCCA LCPE 2.8 Diet and nutrition covers supplements, and the scheme rewards the effect on performance.
ATLAS_TOPIC_ADDITIONS = {'5': ['physical-education-ordinary-2-physical-psychological-demands-of-performance']}

EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any 10'],[2,'any three'],[2,'or'],[3,'any 10'],[3,'one of'],[4,'or'],[7,'choose'],[9,'or'],[10,'or'],[10,'or'],[17,'any three'],[36,'or'],[36,'or']]
SELECTION_REVIEW=[
 {'pages':[2,3,17],'kind':'exam-attempt-rule','reason':'Section choices choose which existing questions to attempt, not combined practice routes.'},
 {'pages':[2,10,36],'kind':'context-or-boilerplate','reason':'Pen colours, case-study descriptions/quotes and copyright text are not choices.'},
 {'pages':[3,4,18,20,21,26],'kind':'open-response','reason':'Fitness component, activity, structure/strategy/compositional element, learning stages, training principles, cycles/phases and roles are chosen from subject knowledge with no finite printed named pool. The two Q3 examples are excluded. Slash terms allow an appropriate kind of response, not a closed named option list.'},
 {'pages':[7,9],'kind':'individually-marked-items','reason':'Q9 has four two-mark matches with one correct answer per row. Q12 has four two-mark true/false statements. Split each item; options are possible answers, not alternative essay routes. Preserve all options on each matching item.'},
 {'pages':[8,23],'kind':'closed-choose-two','reason':'Q10 asks for two of three printed terms (4 + 4) and Q16(c) two of four printed factors (2 x 8). One card each with two slots at the per-item tariff, never one card per pair.'},
 {'pages':[5,15,16,22,23,24],'kind':'required-response-components','reason':'Both supports and barriers, all three athletes, all three event phases, and both unfilled PED categories are required. Q13(d) and Q16(a) split at their printed roman boundaries. Human growth hormone is a supplied example, not an unanswered task or choice.'},
]

# Supplemental raw scan for printed-pool wording without a choose/select verb.
EXPECTED_POOL_SCAN=[[2, 'three of'], [3, 'one of'], [8, 'two of'], [23, 'from the list']]
