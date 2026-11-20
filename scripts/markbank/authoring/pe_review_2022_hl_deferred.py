"""Independent visual sweep of the 2022 DEFERRED Higher paper: all 48 paper and 25 scheme PDF pages.

Written scheme runs PDF 4–23; PDF 24–25 are the blank back cover. The scheme's
section headers misprint the paper's structure (Section A "80 marks", Section C
"120 marks" and "Answer any three"); the paper prints 40 and 80 marks, any five
and any two, and every question total below is the scheme's own per-question
figure. Q12(a)'s header says 2 marks but its allocation is 2 x 2 = 4, which
reconciles Q12 to 8. Q15(a)'s scheme defines "Play" where the paper asks for
Leisure and Recreation. Q16(c)(ii) points to skills "listed in (a)(i)"; they are
listed in (c)(i). Q18(b)'s header reads "aesthetic and/or aesthetic criteria".
Q16(d) and Q18(a) print "one the following groups" (no "of"), so neither scan
sees them; both are printed six-group choices.
"""
from pe_review_2020 import GROUPS

YEAR = 2022
SITTING = 'deferred'

PAPER_PAGE_COUNT = 48
SCHEME_PAGE_COUNT = 25
ACKNOWLEDGEMENT_PAGE = 47
CASE_STUDY_QUESTION = 13
PAGE_ROTATIONS = {}


def fixed(label, maximum, guidance):
    return (label,maximum,guidance,[0,maximum])


def repeated(label, n, maximum, guidance):
    return [(f'{label} {i}',maximum,guidance) for i in range(1,n+1)]


BAND12 = ('Knowledge is accurate and detailed; considers the argument very well with a variety of relevant factors; '
          'independent opinions and judgements are supported by relevant physical activity examples: 9–12. '
          'Knowledge is sometimes accurate with some detail; considers the argument; opinions and judgements may be '
          'supported by relevant physical activity examples: 5–8. Basic knowledge and little understanding; little or no '
          'consideration of the argument; little or no attempt at opinion or judgement: 1–4. No relevant content or an '
          'incorrect response: 0.')

TASKS = [
('1','0-8',[3],[4],
 'Outline how two performance related fitness components and two health related fitness components could benefit Emma when competing in this event.',
 [fixed(f'{kind} related fitness component {i}',2,f'Appropriate {kind.lower()} related fitness component accurately linked to gymnastics beam work.') for kind in ('Performance','Health') for i in (1,2)]),
('2','1-12',[4],[4],
 'Examine the effects of barriers to physical activity participation from the perspective of one of the following groups: women; people with intellectual disabilities; older adults; different ethnic groups; people with physical disabilities; different socio-economic groups.',
 [('Examination',8,'Knowledge is accurate and detailed; considers the argument very well, looking at the negatives/disadvantages with a variety of relevant factors; independent opinions and judgements supported from the perspective of one group: 7–8. Knowledge is sometimes accurate with some detail; provides some negatives/disadvantages; opinions and judgements may be supported from the perspective of one group: 4–6. Basic knowledge and little understanding; little or no reference to negatives/disadvantages from the perspective of one group; little or no attempt at opinion or judgement: 1–3.')]),
('3','0-16',[5],[5],
 'Describe how two injuries commonly associated with a physical activity of your choice could be caused and the first aid treatment for each of them.',
 [fixed(label,2,guidance) for i in (1,2) for label,guidance in
  ((f'Injury {i} and cause','Appropriate injury related to the chosen physical activity named and an appropriate cause described: 2 marks.'),
   (f'First aid for injury {i}','Correct first aid treatment for the named injury described appropriately: 2 marks.'))]),
('4a','0-9',[6],[5],
 'Identify two different tests for cardio respiratory endurance.',
 [('Tests',4,'Two appropriate tests for cardio-respiratory endurance: 2 + 2 marks. Examples: step test, 12 minute/Cooper run, beep test, 1 mile run test.',[0,2,4])]),
('4b','0-9',[6],[5],
 'Explain why one of the tests identified by you in (a) would be included in a fitness test battery for a physical activity of your choice.',
 [('Explanation',4,'Good—clear, accurate justification for including a suitable test of cardio-respiratory endurance for the chosen physical activity: 3–4. Fair—suitable test identified and appropriate justification given: 1–2.')]),
('5a','0-2',[7],[6],
 'Define Newton’s first and second laws of motion.',
 [fixed('First law',2,'Accurate definition of Newton’s first law of motion.'),fixed('Second law',2,'Accurate definition of Newton’s second law of motion.')]),
('5b','0-2',[7],[6],
 'Describe an application of Newton’s first law of motion to a physical activity of your choice.',
 [fixed('Application',4,'Clear, accurate explanation of a good application of the first law of motion to a named physical activity, with a clear example thoroughly and correctly described.')]),
('6','1-15',[8],[6],
 'Describe two ways in which people with a disability could participate in a physical activity of your choice. You must identify a specific disability in your answer.',
 [fixed(f'Way {i}',4,'Name the physical activity and the disability. Accurate adaptation to the named physical activity that would allow a person with the named disability to actively participate in it.') for i in range(1,3)]),
('7a','1-0',[9],[7],
 'Define outdoor and adventure activities.',
 [fixed('Definition',2,'Accurate definition of outdoor and adventure activities.')]),
('7b','1-1',[9],[7],
 'Discuss two social benefits of physical activity participation for older adults.',
 repeated('Social benefit',2,3,'An appropriate social benefit for older adults discussed clearly and accurately, showing knowledge and understanding: 3. A suitable social benefit given with a vague or little attempt at discussion: 1–2.')),
('8a','1-24',[10],[7],
 'Define sponsorship.',
 [fixed('Definition',2,'Clear, accurate definition of sponsorship.')]),
('8b','1-24',[10],[7],
 'Discuss the impact that a sponsorship deal could have on a local sports club.',
 [('Discussion',6,'Name the club/group. Clear, accurate discussion making at least two concrete, accurate points on the impact of a sponsorship deal on a local sports club, relevant to the chosen club/group: 4–6. One point expanded on, relevant to a local sports club: 1–3.')]),
('9a','1-6',[11],[8],
 'Integrity is a principle of ethical practice in sport. Explain integrity in the context of a physical activity of your choice.',
 [fixed('Explanation',4,'Name the physical activity. The scheme prints no band for this part, only an example, in soccer a player will demonstrate integrity by shaking their opponent’s hand and obeying the rules of the game regardless of the performance or result.')]),
('9b','1-6',[11],[8],
 'Discuss the importance of integrity amongst coaches.',
 [('Discussion',4,'Clear and accurate discussion of how/why integrity is important for coaches, generalising and giving clear examples: 3–4. Discussion of the importance of integrity making general points, with or without examples: 1–2. Scheme example: it is important to show leadership as coaches are looked up to and give an example to their players.')]),
('10a','0-12',[12],[9],
 'Discuss the role that sports drinks have when used in physical activity.',
 [('Discussion',4,'Good discussion with general points well made and concrete use of specific examples: 3–4. General discussion that may or may not use specific examples: 1–2.')]),
('10b','1-10',[12],[9],
 'Outline two challenges that athletes can face when using supplements.',
 [('Challenges',4,'Two clear, accurate challenges outlined: 2 + 2 marks.',[0,2,4])]),
('11','1-25',[13],[9],
 'Examine two ways in which the growth of mass participation sporting events could open up business opportunities in the local area.',
 [(f'Way {i}',4,'Clear, accurate general examination with specific examples explaining how/why mass participation events could open up business opportunities in a local area: 4. General examination of the business opportunities that could be opened up by the growth of mass participation events: 2. The answer must link business opportunities and the local area.',[0,2,4]) for i in (1,2)]),
('12a','0-3',[14],[10],
 'Identify two different types of feedback in relation to sporting performance.',
 [('Types',4,'Two types of feedback identified: 2 + 2 marks. Examples: verbal, visual, negative, positive. A misprint in the scheme: the heading for this part says 2 marks, but its allocation is 2 × 2 marks, and only 4 marks makes Question 12 total 8.',[0,2,4])]),
('12b','0-3',[14],[10],
 'Name another type of feedback. In a physical activity of your choice explain how a coach might use this type of feedback to enhance an athlete’s performance.',
 [('Explanation',4,'Name a different type of feedback not used in 12(a), and the physical activity. Clear, accurate explanation of how the feedback is applied in the named activity, linked to enhancing performance and to its use by a coach: 3–4. Vague explanation that may make vague links: 1–2.')]),
('13ai','0-11',[15,16,17],[11],
 'Apart from confidence, name two psychological factors that could impact on Ronaldo’s performance.',
 [('Factors',2,'Two psychological factors that could affect Ronaldo’s performance correctly named, not confidence: 2 × 1 mark. Examples: concentration, anxiety, motivation, or other relevant factors.')]),
('13aii','0-11',[15,16,17],[11],
 'Outline the impact that these two psychological factors could have on performance in a physical activity of your choice.',
 [fixed(f'Factor {i}',2,'Name the physical activity. An appropriate impact that the factor from 13(a)(i) may have on performance in the chosen activity.') for i in range(1,3)]),
('13bi','0-14',[15,16,17],[11],
 'In a physical activity of your choice outline one structure, strategy or compositional element that a performer could use to prevent an opponent gaining the upper hand.',
 [('Outline',4,'Name the physical activity. Clear, descriptive outline of a relevant structure/strategy/compositional element relevant to the activity: 3–4. Outlines a relevant structure/strategy/compositional element relevant to the activity: 1–2.')]),
('13bii','0-15',[15,16,18],[11],
 'Outline two demands of a specific performing role in a physical activity of your choice.',
 [fixed(f'Demand {i}',3,'Name the role and the physical activity; outline the demand.') for i in range(1,3)]),
('13biii','0-10',[15,16,18],[12],
 'Ronaldo’s training reportedly includes pilates, running, rowing and cardio workouts. Outline how training outside the activity can be of benefit to him.',
 [('Outline',4,'Clear outline of how training outside the activity can benefit Ronaldo, using examples: 4. General, sometimes vague outline: 2.',[0,2,4])]),
('13c','1-26',[15,16,19],[12],
 'Many marketing opportunities could arise if Ireland were to host a sporting event which attracted world class athletes. Discuss two positive effects that sports marketing could have on the development of tourism in Ireland.',
 [fixed(f'Positive effect {i}',4,'Clear and appropriate discussion of a positive effect that clearly links sports marketing and its development of tourism.') for i in range(1,3)]),
('13d','1-24',[15,16,20],[12],
 'A young entrepreneur is about to launch an App called “FitTeenagers”. The App aims to increase physical activity participation and physical fitness training amongst teenagers. Compare two different types of sport related advertising that would build awareness around the “FitTeenagers” App.',
 [('Comparison',10,'Clear, accurate and well-developed comparison of two different appropriate types of sport related advertising, with clear examples of how each may help raise awareness of the App: 8–10. Accurate comparison of two appropriate types, which may use examples highlighting the benefit to building awareness of the App: 5–7. Compares two types of advertising but may be somewhat vague on how it raises awareness of the App: 1–4.')]),
('13e','0-1',[15,16,21],[13],
 'Ronaldo has scored in excess of 770 goals and has won FIFA player of the year five times. Examine how economy of movement and creative application of skill can impact on the quality/effectiveness of skill performance.',
 [('Examination',12,'Explain movement economy and creative application of skill, and link both to a skilled performance and its effect, e.g. being energy efficient, having effective technique. '+BAND12.replace('considers the argument very well','considers the argument very well, looking at the positives/advantages,').replace('considers the argument;','considers the argument and gives some positives/advantages;'))]),
('14a','0-2',[22],[14],
 'Figure 8 depicts an athlete’s foot leaving the long jump take-off board. Identify the class of lever, the effort, the load and the fulcrum at work as this action is executed.',
 [fixed('Class of lever',1,'2nd class lever.'),fixed('Effort',1,'Calf (gastrocnemius muscle).'),fixed('Load',1,'Body weight.'),fixed('Fulcrum',1,'Ball of foot.')]),
('14bi','0-16',[22],[14],
 'Identify two reasons why a cool down is used in physical activity.',
 [('Reasons',4,'Two accurate reasons: 2 + 2 marks.',[0,2,4])]),
('14bii','0-16',[23],[14],
 'Outline a warm up structure that a performer could use to ensure that they are suitably prepared for their upcoming event.',
 [('Outline',6,'Accurate and clear outline of an appropriate warm-up structure for use before a competitive performance, using examples: 6. Accurate outline of a suitable warm-up structure, which may be somewhat vague at times, with or without examples: 3. Example: RAMP—raise, activate and mobilise, potentiate/prepare for the activity.',[0,3,6])]),
('14ci','0-19',[24],[15],
 'Identify two ways an official could deal with conflict between participants.',
 [('Ways',4,'Two appropriate approaches a sports official could use when dealing with conflict between participants: 2 + 2 marks.',[0,2,4])]),
('14cii','1-7',[24],[15],
 'Discuss how a code of ethics may influence coaches or club officials’ behaviour in a physical activity of your choice.',
 [('Discussion',10,'Name the physical activity. Clear, accurate and well-developed discussion of how a code of ethics can influence the behaviour of coaches and/or club officials, using clear examples from the chosen activity: 8–10. Clear discussion, with or without examples from the chosen activity: 5–7. Sometimes vague discussion, with links to the chosen activity: 1–4.')]),
('14d','1-6',[25],[15],
 'Examine the impact that sportsmanship and gamesmanship can have on engagement in a physical activity of your choice.',
 [('Examination',12,'Name the physical activity and examine the impact of sportsmanship and gamesmanship on engagement. '+BAND12.replace('considers the argument very well','considers the argument very well, looking at the positives/negatives of their impact on engagement,').replace('considers the argument;','considers the argument and gives some positives/negatives;'))]),
('15a','1-0',[26],[16],
 'Define the following concepts of physical activity: Leisure and Recreation; Physical Education.',
 [fixed('Leisure and Recreation',2,'Clear and accurate definition. A misprint in the scheme: its row for this concept names Play, but the paper asks you to define Leisure and Recreation.'),
  fixed('Physical Education',2,'Clear and accurate definition of Physical Education.')]),
('15b','1-3',[26],[16],
 'Explain two statements that you could include in a physical activity promotion and adherence tip sheet for a target group of your choice.',
 repeated('Statement',2,3,'Statement appropriate for inclusion in a physical activity tip sheet for the chosen target group: 1. Clear and appropriate explanation for including the statement: 2.')),
('15ci','1-3',[27],[16],
 'Identify two ways in which pathways between school and community based physical activity/sport could be improved.',
 [('Ways',4,'Two appropriate ways of improving pathways between school and community based physical activity/sport: 2 + 2 marks.',[0,2,4])]),
('15cii','1-3',[27],[16],
 'Discuss the role that a national policy plays in the promotion of physical activity in the community.',
 [fixed('Policy',2,'Appropriate national policy discussed.'),
  ('Discussion',6,'Clear and comprehensive discussion of the role the national policy plays in promoting physical activity in the community, with examples: 6. Clear discussion of that role, with or without examples: 4. Limited discussion with some vague links between the national policy and physical activity promotion in the community: 2.',[0,2,4,6])]),
('15di','0-1',[28],[17],
 'Practice/training sessions often have improving skill performance as a goal.\nDefine skill.',
 [fixed('Definition',2,'Clear, accurate definition of the concept of skill.')]),
('15dii','0-3',[28],[17],
 'Describe two stages of learning a skill.',
 [fixed(f'Stage {i}',3,'Clear, accurate description of a stage of skill learning, such as cognitive, associative, autonomous; beginner, intermediate, advanced.') for i in range(1,3)]),
('15diii','0-3',[28,29],[17],
 'Identify two principles of effective practice that you could use in the design of a training schedule. Justify your choice of principles.',
 [allocation for i in (1,2) for allocation in
  (fixed(f'Principle {i}',2,'Correct principle of effective practice identified.'),
   fixed(f'Justification {i}',3,'Choice of principle justified by its usefulness in the design of a training schedule.'))]),
('16ai','0-11',[30],[18],
 'Define the psychological factor confidence.',
 [fixed('Definition',2,'Accurate definition of confidence.')]),
('16aii','0-11',[30],[18],
 'Describe one strategy that Mickelson could have used to improve his confidence.',
 [('Description',6,'Clear and accurate description of how a suitable psychological strategy could be used to improve Mickelson’s confidence, using examples: 6. Accurate description of how a suitable psychological strategy could improve his confidence: 4. Somewhat vague description of a strategy that may be used to increase confidence: 2.',[0,2,4,6])]),
('16b','0-12',[31],[18],
 'Discuss three nutritional requirements for a golfer, or another athlete of your choice, when preparing to compete in conditions such as those outlined above. You may not refer to sports drinks.',
 [('Suited to the conditions',3,'A nutritional strategy suitable for the conditions discussed: 3 × 1 mark.'),
  ('Before the competition',3,'A nutritional strategy suitable for use before the competition (in preparing to compete) discussed: 3 × 1 mark.'),
  fixed('Discussion',2,'Clear, accurate discussion provided. Sports drinks are excluded.')]),
('16ci','0-18',[32],[19],
 'List four interpersonal skills desirable in a coach.',
 [('Skills',4,'Four appropriate interpersonal skills desirable in a coach: 4 × 1 mark. Examples: communication, positivity, empathy, leadership.')]),
('16cii','0-18',[32],[19],
 'Outline the value of three of these interpersonal skills to the role of a coach.',
 [fixed(label,maximum,'Clear, accurate outline of the value of an interpersonal skill listed in (c)(i) to the role of a coach. A misprint in the scheme: it says the skills are listed in (a)(i); they are listed in (c)(i).') for label,maximum in (('First skill',3),('Second skill',3),('Third skill',2))]),
('16d','1-18',[33],[19],
 'Examine sports media coverage from the perspective of one the following groups: women; people with intellectual disabilities; older adults; different ethnic groups; people with physical disabilities; different socio-economic groups.',
 [('Examination',12,'Name the group and examine the impact of sports media coverage on it. '+BAND12.replace('considers the argument very well','considers the argument very well, looking at the positives/negatives of sports media coverage for this group,').replace('considers the argument;','considers the argument and gives some positives/negatives;'))]),
('17ai','1-24',[34],[20],
 'Define the terms endorsement and merchandising. Give an example of each.',
 [(term,3,'Clear, accurate definition: 2. Appropriate example: 1.') for term in ('Endorsement','Merchandising')]),
('17aii','1-24',[34],[20],
 'A code of practice should guide the selection of commercial sponsorship for an underage sports club. Outline two criteria suitable for inclusion in such a code of practice.',
 [('Criteria',4,'Two clear, accurate outlines of appropriate criteria: 2 + 2 marks.',[0,2,4])]),
('17bi','1-9',[35],[20],
 'State two Irish anti-doping rules.',
 [('Rules',4,'Two correct Irish anti-doping rules stated: 2 + 2 marks.',[0,2,4])]),
('17bii','1-9',[35],[20],
 'Describe how Sport Ireland enforces its anti-doping rules.',
 [('Description',6,'Accurate description of how Sport Ireland enforces its anti-doping rules. Very good–excellent: 5–6; good: 3–4; fair–poor: 1–2.')]),
('17ci','1-8',[36],[21],
 'Name four substances banned under Irish anti-doping rules.',
 [('Substances',4,'Four banned substances correctly named: 4 × 1 mark.')]),
('17cii','1-8',[36],[21],
 'Identify two implications for the performer of using banned substances.',
 [('Implications',2,'Two appropriate implications identified: 2 × 1 mark.')]),
('17ciii','1-9',[36],[21],
 'Outline one example of when an athlete may be entitled to a Therapeutic Use Exemption (TUE).',
 [('Example',4,'Clear, accurate outline of when an athlete would be entitled to a TUE: 3; medication identified in the outline: 1.',[0,1,3,4])]),
('17d','1-8',[37],[21],
 'Discuss the possible repercussions for an Irish amateur sport if one of their athletes failed a drug test at an Olympic Games.',
 [('Discussion',10,'Excellent discussion: 9–10; very good: 7–8; good: 5–6; fair: 3–4; poor: 1–2.')]),
('18a','1-14',[38],[22],
 'Outline one positive development in physical activity in the last twenty years, from the perspective of one the following groups: women; people with intellectual disabilities; older adults; different ethnic groups; people with physical disabilities; different socio-economic groups. You may not use media in your answer.',
 [fixed('Development',4,'A positive development from the past 20 years for the chosen group, clearly outlined with an example. Media may not be used.')]),
('18b','0-23',[39],[22],
 'Compare the physical activity pictured in Figure 14 to that of Figure 15 in terms of aesthetic and/or artistic criteria.',
 [fixed('Ballet',1,'Clearly highlights ballet as an aesthetic/artistic activity. A misprint in the scheme: its heading reads “aesthetic and/or aesthetic criteria”; the paper asks for aesthetic and/or artistic criteria.'),
  fixed('High jump',1,'Clearly identifies high jump performance as not being judged aesthetically/artistically.'),
  fixed('Criteria',2,'Clearly identifies the inclusion of form, grace, fluidity and body positioning as criteria in aesthetic/artistic activity.'),
  fixed('Difference',2,'Highlights the difference between artistic and aesthetic and other physical activities where the outcome is not reliant on how the performance and performer looks.')]),
('18c','0-10',[40],[22],
 'Explain three principles of training.',
 [fixed(f'Principle {i}',3,'Accurate explanation of a principle of training, such as specificity, reversibility, tedium, progressive overload.') for i in range(1,4)]),
('18di','0-10',[41],[23],
 'Identify three methods of physical fitness training.',
 [('Methods',6,'Three correct methods of physical fitness training: 3 × 2 marks. Examples: plyometric training, HIIT training, weight training, Pilates, interval training.',[0,2,4,6])]),
('18dii','0-10',[41],[23],
 'Explain why two of the methods of physical fitness training identified in (i) are appropriate for training in a physical activity of your choice.',
 [fixed(f'Method {i}',3,'Clear, appropriate explanation of why a training method from (i) is appropriate for the chosen activity.') for i in range(1,3)]),
('18diii','0-12',[42],[23],
 'Name the three energy systems and identify a method of physical fitness training that could be used to train each named system.',
 [(f'Energy system {i}',3,'Energy system correctly identified: 1. Appropriate training method: 2. Energy systems: ATP-PC system/alactic anaerobic system; anaerobic glycolytic system/anaerobic lactic system; aerobic system/oxidative system.') for i in (1,2,3)]),
]

CASE = 'Read the Cristiano Ronaldo case study and Figures 4–7 on paper pages 15–16.'
CONTEXT = {
 '1':'Figure 1 shows Irish gymnast Emma Slevin on the beam at the 2021 Slovenia World Challenge Cup in Artistic Gymnastics. The paper gives the beam as 5 metres long, 10 centimetres wide and raised 125 centimetres from the floor.',
 '3':'The paper notes that all types of sports have a potential for injury, from contact with other players or from overuse or misuse of a body part.',
 '4b':'Question 4(a) asks for two tests for cardio respiratory endurance. Use one of your tests here.',
 '6':'The paper introduces Sports Inclusion Disability Officers (SIDOs), who aim to increase the participation of people with disabilities in sport, fitness and physical activity.',
 **{p:'Figure 2 shows a runner and two walkers passing a Covid-19 “This is 2 metres” sign. The paper notes that the pandemic has increased awareness about the importance of being physically active.' for p in ('7a','7b')},
 '11':'Figure 3 shows the Kerry Cycling logo and riders on the Ring of Kerry Charity Cycling event, which the paper calls Ireland’s largest one day charity cycle event.',
 '12b':'Question 12(a) asks for two types of feedback. Name a different type here.',
 **{p:CASE for p in ('13ai','13bi','13bii','13c','13d','13e')},
 '13aii':CASE+' Question 13(a)(i) asks for two psychological factors other than confidence. Use those two factors here.',
 '13biii':CASE+' The case study says Ronaldo’s fitness regime combines pilates, running, rowing and cardio workouts; Figure 5 shows a gym workout.',
 '14a':'Figure 8 is a close-up of the athlete’s foot on the long jump take-off board.',
 **{p:'The paper describes a fight between the University of Kansas and Kansas State University men’s basketball teams on 19 January 2020; Figure 9 shows the melee.' for p in ('14ci','14cii')},
 **{p:'Question 15(d) opens: “Practice/training sessions often have improving skill performance as a goal.”' for p in ('15dii','15diii')},
 **{p:'Figure 10 shows Phil Mickelson, the oldest winner of a major golf tournament (US PGA, May 2021, aged 50), beside his statement about playing an aggressive style of golf.' for p in ('16ai','16aii')},
 '16b':'The paper describes the 2021 US PGA conditions on the Kiawah Island golf course: temperatures of 25 to 28 degrees Celsius, an average walking distance of 12 kilometres per round, more than five hours to complete a round, and four rounds to win.',
 '16cii':'Question 16(c)(i) asks you to list four interpersonal skills. Use three of your skills here.',
 **{p:'The paper quotes Sean Crowley of the Irish Doping Control Unit on Ireland’s anti-doping system and athletes who dope looking for new ways to beat it.' for p in ('17bi','17bii')},
 '18b':'Figure 14 shows a ballet dancer; Figure 15 shows a high jumper clearing the bar.',
 '18dii':'Question 18(d)(i) asks for three methods of physical fitness training. Use two of your methods here.',
}
# A printed choice is ONE card (AGENTS.md, 2026-10-12): the printed question
# with its whole pool and the scheme's own grid. pe_complete.py emits one card.
# This paper prints the disability groups in the plural, so the pool keeps the
# 2020 group ids in their order with the labels as printed here.
PRINTED = {'physical-disability':'People with physical disabilities','intellectual-disability':'People with intellectual disabilities'}
DEFERRED_GROUPS = [(gid,PRINTED.get(gid,label)) for gid,label in GROUPS]
CHOICES = {part:{'choose':1,'pool':[label for _,label in DEFERRED_GROUPS]} for part in ('2','16d','18a')}
SOURCE_POOLS = {
 '2':[(4,'one of the following groups')]+[(4,label.replace('-','‐')) for _,label in DEFERRED_GROUPS],
 '16d':[(33,'one the following groups')]+[(33,label.replace('-','‐')) for _,label in DEFERRED_GROUPS],
 '18a':[(38,'one the following groups')]+[(38,label.replace('-','‐')) for _,label in DEFERRED_GROUPS],
}
SELECTION_REVIEW = [
 {'parts':['instructions','section-a','section-c'],'decision':'exam-level-selection','reason':'Any five of Q1–12 and any two of Q14–18 are examination selection rules. All twelve short questions, the case study and all five long questions are included with each separately marked part.'},
 {'parts':['2','16d','18a'],'decision':'one-card','options':DEFERRED_GROUPS,'reason':'Each task prints a closed six-group pool; the scheme marks the chosen group with one grid. One card per task. Q16(d) and Q18(a) print “one the following groups” without “of”, so neither raw scan sees them.'},
 {'parts':['4b','13aii','16cii','18dii'],'decision':'candidate-response','reason':'These refer to the candidate’s own preceding answers: one of the two tests from 4(a), the two factors from 13(a)(i), three of the four skills listed in 16(c)(i), two of the three methods from 18(d)(i). There is no fixed printed pool.'},
 {'parts':['4a','12a','12b','13ai','14ci','15diii','16ci','17bi','17ci','18c','18di','18diii'],'decision':'open-knowledge-response','reason':'The paper supplies no closed answer list for fitness tests, feedback types, psychological factors, ways to deal with conflict, principles, interpersonal skills, anti-doping rules, banned substances, training methods or energy systems. Lists in the scheme are answers, not printed question options.'},
 {'parts':['13bi','14cii','18b'],'decision':'flexible-wording','reason':'“Structure, strategy or compositional element”, “coaches or club officials’ behaviour” (the scheme reads coaches and/or club officials) and “aesthetic and/or artistic criteria” are flexible terms marked by one grid, not alternative tasks.'},
 {'parts':['1','3','5a','14a','15a','17ai','18b','18diii'],'decision':'required-headings','reason':'Both performance and both health fitness components, both injuries with their first aid, both laws, all four lever parts, both concepts, both terms with examples, both pictured activities and all three energy-system rows are required; keep them together at each numbered part’s tariff.'},
 {'parts':['3','4b','5b','6','8b','9a','12b','13aii','13bi','13bii','14cii','14d','15b','16b','17d','18dii'],'decision':'open-activity','reason':'Physical activities, clubs, roles, target groups, athletes and sports are unrestricted choices, subject to the printed exclusions carried into each prompt. Q16(b)’s “a golfer, or another athlete of your choice” is one such open choice.'},
 {'parts':['paper-page-2','paper-page-5','paper-page-15','paper-page-16','paper-page-37','copyright'],'decision':'incidental-or','reason':'Blue or black pen, contact or overuse or misuse, “one of the greatest athletes”, “one of the game’s most natural finishers”, “one of his best qualities”, “one of their athletes failed a drug test” and copyright language do not create alternate examination tasks.'},
]

# Q18(d)(iii) names the energy systems (1 mark a row) and pairs each with a
# training method (2 marks a row): it examines NCCA LCPE 2.6 training methods
# as well as 2.8 energy systems.
ATLAS_TOPIC_ADDITIONS = {'18diii': ['physical-education-higher-2-physicalpsychological-demands-of-performance-training-methods-and-fitness-planning']}

EXPECTED_QUESTION_TOTALS = {**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN = [[2,'any five'],[2,'any two'],[2,'or'],[3,'any five'],[4,'one of'],[5,'or'],[5,'or'],[6,'one of'],[15,'one of'],[16,'one of'],[16,'one of'],[17,'or'],[22,'any two'],[24,'or'],[31,'or'],[37,'one of'],[39,'and/or'],[48,'or'],[48,'or']]

# Supplemental raw scan for printed-pool wording without a choose/select verb.
EXPECTED_POOL_SCAN = [[2,'five of'],[2,'two of'],[4,'one of'],[6,'one of'],[15,'one of'],[16,'one of'],[16,'one of'],[32,'three of'],[37,'one of'],[41,'two of']]
