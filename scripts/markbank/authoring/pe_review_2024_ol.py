"""Independent visual sweep: all 36 paper and 40 scheme pages.
Written scheme 4–22, Irish bonus 23, project 24–32, performance 33–39,
remaining pages introductory/end matter. Q18(b)(i) chooses two of three:
three mechanically generated routes. Q6(a) is one four-mark MCQ.
"""
from itertools import combinations
PAPER_PAGE_COUNT=36
SCHEME_PAGE_COUNT=40
ACKNOWLEDGEMENT_PAGE=35
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


TASKS=[
('1','1-17',[3],[4], 'In a named physical activity of your choice, outline two ways technology has impacted on coaches.',
 repeat('Impact',2,4,'Clear and accurate outline of impact on coaches in a named activity: 4; limited outline: 2.',[0,2,4])),
('2','0-11',[4],[4], 'Outline two ways motivation can have a positive impact on practice.',
 repeat('Positive impact',2,4,'Clear and accurate outline of positive impact on practice: 4; limited outline: 2.',[0,2,4])),
('3','1-24',[4],[5], 'Outline two impacts of merchandising on a named physical activity of your choice.',
 repeat('Impact',2,4,'Clear and accurate outline of merchandising’s impact on the named activity: 4; limited outline: 2.',[0,2,4])),
('4a','1-8',[5],[5], 'Identify two different categories of performance-enhancing drugs.',
 [fixed(f'Category {i}',2,'Correctly identified performance-enhancing drug category.') for i in (1,2)]),
('4b','1-8',[5],[5], 'Describe how one of the performance-enhancing drug categories identified by you in Question 4(a) can affect performance.',
 [('Description',4,'Clear and accurate description of effect on performance: 4; vaguely accurate: 2.',[0,2,4])]),
('5','1-1',[6],[6], 'Outline two social benefits of physical activity.',
 repeat('Social benefit',2,4,'Clear and accurate outline: 4; limited outline: 2. Examples include friendships and a sense of belonging.',[0,2,4])),
('6a','0-10',[6],[6], 'Choose the statement that correctly describes periodisation: (i) It is interval training for 6 months. (ii) It is the division of a training plan into phases. (iii) It is performance analysis that provides coaches with data.',
 [fixed('Correct statement',4,'(ii) It is the division of a training plan into phases.')]),
('6b','0-10',[6],[6], 'Describe a method of physical fitness training that develops power.',
 [('Training method',4,'Clear and accurate description of training that develops muscular power: 4; vaguely accurate: 2. For example, plyometrics.',[0,2,4])]),
('7a','0-14',[7],[7], 'In a named physical activity of your choice, identify two weaknesses that an opposition team could have.',
 [fixed(f'Weakness {i}',2,'Correct weakness relevant to the opposition team and named activity.') for i in (1,2)]),
('7b','0-14',[7],[7], 'Suggest a strategy you could use to exploit one of the weaknesses identified by you in Question 7(a).',
 [('Strategy',4,'Clear and accurate strategy to exploit the selected weakness: 4; vague strategy: 2.',[0,2,4])]),
('8','1-18',[8],[7], 'Outline two characteristics of a named physical activity that could give it media or spectator appeal.',
 repeat('Characteristic',2,4,'Clear and accurate characteristic giving media or spectator appeal: 4; vaguely accurate: 2.',[0,2,4])),
('9a','0-21',[8],[8], 'List two factors that influence personal performance in a named physical activity of your choice.',
 [fixed(f'Factor {i}',2,'Appropriate factor influencing personal performance in the named activity.') for i in (1,2)]),
('9b','0-21',[8],[8], 'Describe one of the factors listed by you in Question 9(a).',
 [('Description',4,'Clear and accurate description of a factor influencing personal performance: 4; somewhat clear and accurate: 2.',[0,2,4])]),
('10','1-8',[9],[8], 'Outline two implications of using performance-enhancing drugs for the performer.',
 repeat('Implication',2,4,'Clear and accurate outline: 3–4; somewhat clear and accurate: 1–2.')),
('11','0-1',[9],[9], 'Outline two characteristics of a skilled performance.',
 repeat('Characteristic',2,4,'Clear and accurate characteristic of skilled performance: 3–4; somewhat clear and accurate: 1–2.')),
('12','1-25',[10],[9], 'Describe how mass participation events provide opportunities for business.',
 [('Description',8,'Excellent description: 8; very good: 6; good: 4; fair: 2.',[0,2,4,6,8])]),
('13ai','1-1',[12,13],[10], 'Identify two reasons why the Cork Masters Swimming Club was set up.',
 [fixed(f'Reason {i}',2,'Correct reason from the case study, such as leisure, health and fitness, or increasing numbers wanting to swim.') for i in (1,2)]),
('13aii','1-1',[12,13],[10], 'Explain one of the reasons identified by you in Question 13(a)(i).',
 [('Explanation',4,'Clear and accurate explanation: 3–4; somewhat clear and accurate: 1–2.')]),
('13bi','1-3',[12,13,14],[10], 'With reference to the case study, identify three characteristics that Susan and Martin displayed to promote others’ participation in physical activity.',
 [fixed(label,2,'Correct characteristic identified from the case study.') for label in ('Enthusiastic','Organised','Determined')]),
('13bii','1-3',[12,13,14],[10], 'Describe one of the characteristics correctly identified by you in Question 13(b)(i).',
 [('Description',4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')]),
('13ci','0-6',[12,13,14],[11], 'Explain why endurance would be important in long distance open water swimming.',
 [('Explanation',4,'Clear and accurate explanation: 3–4; somewhat clear and accurate: 1–2.')]),
('13cii','0-10',[12,13,14],[11], 'Identify two strategies a marathon swimmer could use to support recovery following long-distance swimming training.',
 [fixed(f'Strategy {i}',2,'Correct recovery strategy relevant to the swimmer.') for i in (1,2)]),
('13ciii','0-10',[12,13,14,15],[11], 'Describe one of the strategies identified by you in Question 13(c)(ii).',
 [('Description',4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')]),
('13di','1-21',[12,13,15],[12], 'During the Olympic women’s springboard diving final there was a lot of media focus on diver Tom Daley knitting. Identify two ways the media may play a role in maintaining gender stereotypes of men and women in sport.',
 [fixed(f'Way {i}',2,'Appropriate way: for example, sensationalising differences, focusing on body type, editing images or limiting coverage.') for i in (1,2)]),
('13dii','1-21',[12,13,15],[12], 'Discuss one of the ways the media maintains gender stereotypes identified by you in Question 13(d)(i).',
 [('Discussion',6,'Clear and accurate discussion: 4–6; somewhat clear and accurate: 1–3.')]),
('13ei','0-11',[12,13,16],[12], 'What strategy does Tom Daley use to help him prepare mentally for competition?',
 [fixed('Strategy',2,'Knitting / selective attention.')]),
('13eii','0-11',[12,13,16],[12], 'Describe two different strategies to improve mental preparedness before practice or performance in a named physical activity of your choice.',
 repeat('Strategy',2,4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')),
('14ai','1-24',[17],[13], 'Define sponsorship.',
 [('Definition',4,'Accurate: 4; somewhat accurate: 2.',[0,2,4])]),
('14aii','1-24',[17,18],[13], 'Outline two advantages and two disadvantages of sponsorship for performers.',
 [fixed(label,2,'Appropriate advantage or disadvantage of sponsorship for performers outlined.') for label in ('Advantage 1','Advantage 2','Disadvantage 1','Disadvantage 2')]),
('14bi','1-25',[17,18],[13], 'Discuss the involvement of a named business in sport.',
 [('Discussion',6,'Clear and accurate discussion: 4–6; somewhat clear and accurate: 1–3.')]),
('14bii','1-24',[17,19],[13], 'Describe two impacts sponsorship could have on a named National Governing Body (NGB).',
 repeat('Impact',2,4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')),
('14ci','0-12',[19],[14], 'Lionel Messi the soccer player has been sponsored by the sports drink Gatorade. Identify two advantages and two disadvantages of sports drinks.',
 [fixed(label,2,'Appropriate advantage or disadvantage of sports drinks identified.') for label in ('Advantage 1','Advantage 2','Disadvantage 1','Disadvantage 2')]),
('14cii','0-12',[20],[14], 'Figure 12 is a graph of how the body uses energy. Identify the line colour/letter that represents the aerobic system.',
 [fixed('Line',2,'Green / line C.')]),
('14ciii','0-12',[20],[14], 'In a named physical activity of your choice, explain why that activity uses the aerobic system.',
 [('Explanation',4,'Clear and accurate explanation: 4; somewhat clear and accurate: 2.',[0,2,4])]),
('15ai','1-18',[21],[15], 'List two positive and two negative impacts the media has on spectators.',
 [fixed(label,2,'Appropriate impact of media on spectators identified.') for label in ('Positive 1','Positive 2','Negative 1','Negative 2')]),
('15aii','1-18',[21],[15], 'Describe one positive and one negative impact the media has on spectators listed by you in Question 15(a)(i).',
 [(label,4,'Clear and accurate description: 4; somewhat clear and accurate: 2.',[0,2,4]) for label in ('Positive impact','Negative impact')]),
('15b','0-18',[22],[15], 'During a camogie match the coach yells “Lily get into space”. Lily looks up into the space in the sky. The coach shakes their head in disbelief. Describe two desirable interpersonal skills of a coach or choreographer.',
 repeat('Interpersonal skill',2,4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')),
('15ci','1-17',[22],[15], 'Describe one advantage and one disadvantage of a newly developed technology for officials in a named physical activity of your choice.',
 [(label,4,'Clear and accurate description relevant to officials and the named activity/technology: 3–4; somewhat clear and accurate: 1–2.') for label in ('Advantage','Disadvantage')]),
('15cii','1-17',[23],[16], 'Explain how technology can benefit performers.',
 [('Explanation',8,'Excellent: 8; very good: 6; good: 4; fair: 2.',[0,2,4,6,8])]),
('16ai','0-16',[24],[17], 'Define safe practice in physical activity.',
 [fixed('Definition',2,'Correct definition of safe practice.')]),
('16aii','0-16',[24],[17], 'Give two examples of safe practice in physical activity.',
 [fixed(f'Example {i}',2,'Correct example of safe practice.') for i in (1,2)]),
('16aiii','1-1',[24],[17], 'Describe two economic benefits of physical activity.',
 repeat('Economic benefit',2,4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')),
('16bi','0-16',[25],[17], 'In a named physical activity of your choice, identify two common injuries and explain how they could be treated.',
 [fixed(f'Injury {i}',2,'Common injury appropriate to the named activity.') for i in (1,2)]+repeat('Treatment',2,3,'Very good explanation of treatment for the corresponding injury: 3; good: 2; fair: 1.')),
('16bii','0-10',[26],[17], 'Identify two symptoms of overtraining.',
 [fixed(f'Symptom {i}',2,'Correct symptom of overtraining.') for i in (1,2)]),
('16biii','0-10',[26],[18], 'Describe one symptom of overtraining identified by you in Question 16(b)(ii).',
 [('Description',4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')]),
('16c','0-10',[26],[18], 'In a named physical activity of your choice, describe two benefits of flexibility training.',
 repeat('Benefit',2,4,'Clear and accurate description of a flexibility-training benefit: 3–4; somewhat clear and accurate: 1–2.')),
('17ai','1-6',[27],[19], 'Describe two principles of ethical practice.',
 repeat('Principle',2,4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2. Accept integrity, respect, fairness and equity.')),
('17aii','1-6',[27,28],[19], 'Discuss the difference between sportsmanship and gamesmanship.',
 [('Discussion',8,'Excellent discussion of both concepts and their difference: 8; very good: 6; good: 4; fair: 2.',[0,2,4,6,8])]),
('17bi','0-2',[28],[19], 'Label the load, effort and fulcrum on the diagram of a lower leg and foot.',
 [fixed('Effort',2,'Upper-right box at the calf muscle.'),fixed('Load',2,'Lower-right box at the ankle.'),fixed('Fulcrum',2,'Left-hand box at the toes/ball of the foot.')]),
('17bii','0-2',[28],[19], 'Identify the class of lever shown in the diagram.',
 [fixed('Class of lever',2,'Second class lever.')]),
('17ci','0-21',[29],[20], 'Explain performance analysis.',
 [('Explanation',4,'Clear and accurate: 4; somewhat clear and accurate: 2.',[0,2,4])]),
('17cii','0-21',[29],[20], 'In a named physical activity of your choice, describe two benefits of performance analysis for the performer.',
 repeat('Benefit',2,4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')),
('17ciii','0-22',[30],[20], 'Outline two ways that you can compare your performance to that of a model performer in a named physical activity of your choice.',
 repeat('Comparison method',2,2,'Clear and accurate outline: 2; somewhat clear and accurate: 1.')),
('18ai','0-17',[31],[21], 'Outline three rules and regulations of a named physical activity of your choice.',
 [fixed(f'Rule/regulation {i}',2,'Appropriate rule or regulation outlined for the named activity.') for i in range(1,4)]),
('18aii','0-17',[31],[21], 'Describe the appropriate scoring or recording system of a named physical activity of your choice.',
 [('Description',4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')]),
('18bi','0-19',[32],[21], 'Describe the demands of officiating under two of the following headings: personal fitness; psychological readiness; personal attire.',
 repeat('Demand',2,4,'Clear and accurate description of the selected officiating demand: 3–4; somewhat clear and accurate: 1–2.')),
('18bii','0-19',[32],[21], 'Identify two strategies used by officials when managing conflict.',
 [fixed(f'Strategy {i}',2,'Correct strategy for managing conflict between the official and participants.') for i in (1,2)]),
('18biii','0-19',[32,33],[21], 'Describe one of the strategies identified by you in Question 18(b)(ii).',
 [('Description',4,'Clear and accurate description: 3–4; somewhat clear and accurate: 1–2.')]),
('18ci','0-12',[33],[22], 'In a named physical activity of your choice, describe one nutritional requirement before the activity and one nutritional requirement after the activity.',
 [(phase,4,'Clear and accurate description of a requirement at this phase: 4; somewhat clear and accurate: 2.',[0,2,4]) for phase in ('Before','After')]),
('18cii','1-10',[33],[22], 'Name one dietary supplement and outline two advantages of using that supplement.',
 [fixed('Supplement',2,'Appropriate dietary supplement named.')]+repeat('Advantage',2,2,'Clear and accurate outline: 2; somewhat clear and accurate: 1.')),
]
CONTEXT={
 '4b':'Identify a performance-enhancing drug category as requested in 4(a), then describe the effect of that same category.',
 '7b':'Choose a physical activity and identify an opposition weakness as requested in 7(a), then suggest how to exploit that same weakness.',
 '9b':'Name an activity and identify a factor affecting personal performance as requested in 9(a), then describe that same factor.',
 '11':'The source quotes Carol Dweck on learning skills and techniques and practising them regularly.',
 '14ai':'Read the original Rhasidat Adeleke/Allianz sponsorship text and photograph on page 17.',
 '14aii':'The original Adeleke/Allianz sponsorship context is included on page 17.',
 '14bi':'The Allianz example is included as context; the question permits any named business.',
 '14bii':'The original sponsorship context on page 17 is included; name an NGB of your choice.',
 '14cii':'Use the complete original energy-system graph and colour/letter key on page 20.',
 '15aii':'Identify positive and negative media impacts on spectators as requested in 15(a)(i). Describe one of each from your own list.',
 '15cii':'Figure 14 shows athletes with running blades. The source describes the customised socket, knee joint and carbon-fibre blade.',
 '16biii':'Identify symptoms of overtraining as requested in 16(b)(ii), then describe one of your own choices.',
 '17ai':'Figure 16 shows Maggie Duba helping fallen runner Sarah Storey to finish a race.',
 '17aii':'The sportsmanship example and images from Figure 16 are included on page 27.',
 '17ciii':'Figure 17 shows a gymnast performing an aerial cartwheel on the beam at the Olympic Games.',
 '18biii':'Identify conflict-management strategies as requested in 18(b)(ii), then describe one of those same strategies. The preceding question and illustration are included.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete “On the water” case study on pages 12–13, including Cork Masters Swimming Club, marathon swimming and Tom Daley.'
for part,dependency in {'13aii':'Choose one reason identified in 13(a)(i).','13bii':'Choose one characteristic identified in 13(b)(i).','13ciii':'Choose one recovery strategy identified in 13(c)(ii); that preceding task is included on page 14.','13dii':'Choose one way identified in 13(d)(i).'}.items():
    CONTEXT[part]+=' '+dependency
HEADINGS=['Personal fitness','Psychological readiness','Personal attire']
VARIANTS={'18bi':[('-and-'.join(s.lower().replace(' ','-') for s in pair),' and '.join(pair)) for pair in combinations(HEADINGS,2)]}
VARIANT_REQUIREMENTS={'18bi':'Describe both demands in this practice pair. The original paper asks for any two of three printed headings; each pair carries eight marks.'}
SOURCE_POOLS={'18bi':[(32,'Describe the demands of officiating under two of the following headings:'),(32,'Personal fitness'),(32,'Psychological readiness'),(32,'Personal attire')]}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any three'],[2,'or'],[3,'named physical activity'],[4,'named physical activity'],[5,'one of'],[7,'named physical activity'],[7,'one of'],[8,'named physical activity'],[8,'or'],[8,'named physical activity'],[8,'one of'],[13,'one of'],[14,'one of'],[15,'one of'],[15,'one of'],[16,'or'],[16,'named physical activity'],[17,'any three'],[20,'named physical activity'],[22,'or'],[22,'named physical activity'],[25,'named physical activity'],[26,'named physical activity'],[29,'named physical activity'],[30,'named physical activity'],[31,'named physical activity'],[31,'or'],[31,'named physical activity'],[33,'one of'],[33,'named physical activity'],[36,'or'],[36,'or']]
EXPECTED_POOL_SCAN=[[2,'any ten'],[2,'three of'],[3,'any ten'],[5,'one of'],[7,'one of'],[8,'one of'],[12,'three of'],[13,'one of'],[14,'one of'],[15,'one of'],[15,'one of'],[32,'two of'],[33,'one of']]
SELECTION_REVIEW=[
 {'pages':[1,2,3,17],'kind':'exam-attempt-rule-or-boilerplate','reason':'Historical paper format and any ten/three section instructions are not combined practice routes. Pen colours are boilerplate.'},
 {'pages':[3,4,5,7,8,13,14,15,16,19,20,21,22,25,26,29,30,31,33],'kind':'open-response-or-own-answer','reason':'Activities, PED categories, weaknesses, factors, reasons, characteristics, recovery methods, media impacts, symptoms, rules and strategies are open knowledge or chosen from the candidate’s preceding answer. Case-study facts are source extraction, not a printed essay-option pool.'},
 {'pages':[6],'kind':'single-answer-mcq','reason':'Periodisation has one correct statement among three distractor options. This is one four-mark task, not three alternative practice routes.'},
 {'pages':[8,16,22,31],'kind':'flexible-wording','reason':'Media or spectator, practice or performance, coach or choreographer, and scoring or recording describe permissible contexts; no fixed finite route selection is required.'},
 {'pages':[18,19,21,22,28,33],'kind':'required-components','reason':'Positive and negative responses, advantages and disadvantages, all three lever labels, and both nutritional phases are compulsory headings. Keep each printed task intact at its scheme boundary.'},
 {'pages':[32],'kind':'closed-choose-two','reason':'Q18(b)(i) explicitly chooses two of the three named officiating demands. Generate C(3,2)=3 eight-mark routes.'},
 {'pages':[36],'kind':'copyright','reason':'Copyright or wording is not a choice directive.'},
]

SELECTION_REVIEW.append({'pages':[12],'kind':'source-description','reason':'All three of these swimmers is factual case-study text, not a selection directive.'})
