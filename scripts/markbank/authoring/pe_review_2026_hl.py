"""Independent visual sweep: all 44 paper and 42 scheme pages.
Written scheme 4–25, project 26–33, performance 34–40, other pages
introductory/blank/end matter. Two valid Q6 component pairings; two Q16(c)
ethical concepts. The three components in Q17(d) are all compulsory.
"""
from itertools import product
PAPER_PAGE_COUNT=44
SCHEME_PAGE_COUNT=42
ACKNOWLEDGEMENT_PAGE=43
CASE_STUDY_QUESTION=13
PAGE_ROTATIONS={}


def fixed(label,maximum,guidance):
    return (label,maximum,guidance,[0,maximum])


def repeat(label,n,maximum,guidance,scores=None):
    return [(f'{label} {i}',maximum,guidance,*([scores] if scores is not None else [])) for i in range(1,n+1)]


TASKS=[
('1a','0-18',[3],[4],'There are many demands associated with non-playing roles in physical activity and sport. Identify three demands on a coach/choreographer.',
 [('Three demands',4,'Correct demands: first 2, second 1, third 1. One correct: 2; two: 3; three: 4.',[0,2,3,4])]),
('1b','0-17',[3],[4],'Outline the scoring/recording system used in competitions for two physical activities. Two physical activities with the same scoring system may not be used.',
 [fixed(f'System {i}',2,'Accurate outline for the named activity. The two systems must be different.') for i in (1,2)]),
('2a','1-0',[4],[4],'Physical Education is a concept of physical activity. Explain Physical Education in this context.',
 [('Explanation',4,'Clear and accurate explanation contextualised as a concept of physical activity: 3–4; accurate explanation: 1–2.')]),
('2b','1-3',[4],[4,5],'Identify three supports for physical activity participation in schools. You may not use Physical Education.',
 [('Three supports',4,'Correct school supports other than PE: first 2, second 1, third 1. One: 2; two: 3; three: 4.',[0,2,3,4])]),
('3','1-18',[5],[5],'Describe how media coverage can positively impact spectator behaviour.',
 [('Description',8,'Clear, accurate, structured description using one or more well-developed examples: 6–8; accurate description: 3–5; some accurate outline: 1–2.')]),
('4a','0-2',[6],[6],'Identify one class of lever that is involved in the performance of a skill, in a selected physical activity.',
 [fixed('Lever class',2,'Correct class of lever for the selected skill and activity.')]),
('4b','0-2',[6],[6],'Identify the body parts that represent the fulcrum, effort and load for the correctly identified lever in Question 4(a).',
 [fixed(x,2,'Correct body part for the lever correctly named in 4(a).') for x in ('Fulcrum','Effort','Load')]),
('5a','1-9',[7],[6],'Explain what Therapeutic Use Exemptions are and when they are used.',
 [('Explanation',4,'Accurate explanation of TUEs and when used: 4; correctly explains when used: 2.',[0,2,4])]),
('5b','1-9',[7],[7],'Identify two current Irish anti-doping rules.',
 [fixed(f'Rule {i}',2,'Correct Irish anti-doping rule applicable to this 2026 examination. See the published scheme’s rule list.') for i in (1,2)]),
('6','0-10',[8],[8],'Choose one Health Related Fitness component and one Performance Related Fitness component from balance, coordination and flexibility. Outline one activity you could use as a combined approach to training to improve both chosen components. You may use a diagram.',
 [fixed('HRF component',1,'Flexibility.'),fixed('PRF component',1,'Balance or coordination, as selected for the practice route.'),('Combined activity',6,'Clear and accurate outline of one activity training both selected components: 4–6; relevant activity outlined: 1–3.')]),
('7','1-22',[9],[8],'Describe, using examples, two influences that impact on the participation patterns of boys in physical activity and sport.',
 [fixed(f'Influence {i}',1,'Relevant influence identified.') for i in (1,2)]+[fixed(f'Description {i}',3,'Accurate description of why and how this influence affects boys’ participation, with an example.') for i in (1,2)]),
('8a','0-10',[10],[9],'Identify two benefits of warming-up.',
 [fixed(f'Benefit {i}',2,'Appropriate benefit of warming-up.') for i in (1,2)]),
('8b','0-10',[10],[9],'Outline the phases of a warm-up.',
 [('Phases',4,'Clear and accurate outline of a correctly phased warm-up: 3–4; suitable phased warm-up mentioned: 1–2.')]),
('9a','1-3',[11],[9],'State two ways that you could promote physical activity participation.',
 [fixed(f'Way {i}',1,'Appropriate way clearly stated.') for i in (1,2)]),
('9b','1-3',[11],[10],'Identify two tips you would include to help someone adhere to an exercise programme when returning to activity after a long absence. Justify your choices.',
 repeat('Justified tip',2,3,'Appropriate adherence tip for return after a long absence with a relevant justification: 3; less-developed justified tip: 1–2.')),
('10','0-2',[12],[10],'As part of your PE studies you used Newton’s Laws of Motion to analyse skill and technique. Describe how Newton’s First Law of Motion can be applied to two skills that you analysed.',
 repeat('Application',2,4,'Clear and accurate description applied to the named skill: 4; accurate description: 2. The two applications must be different.',[0,2,4])),
('11','1-6',[13],[11],'List two principles of ethical practice and outline the importance of upholding these principles in a sporting context.',
 [fixed(f'Principle {i}',1,'Correct principle of ethical practice.') for i in (1,2)]+[('Importance',6,'Clear, accurate, cohesive outline of the importance of both named principles: 4–6; accurate outline: 1–3.')]),
('12','0-19',[14],[11],'Choose three physical activities. For each, identify one safety regulation that an official must implement and state which official implements it.',
 [('Three regulations and officials',8,'Each correct response names an activity, a relevant safety regulation and the official implementing it. First correct response: 3; second: 3; third: 2. One correct: 3; two: 6; three: 8.',[0,3,6,8])]),
('13ai','1-3',[16,17],[12],'Swim Ireland governs swimming, water polo, diving and artistic swimming in Ireland. Name two other National Governing Bodies for sport in Ireland and the sport that they govern.',
 [fixed(f'NGB and sport {i}',1,'Correct NGB and corresponding sport, other than Swim Ireland/swimming.') for i in (1,2)]),
('13aii','1-4',[16,17],[12],'Outline two ways, identified in the case study, that Swim Ireland supports high performance.',
 [fixed(f'Support {i}',1,'Correct support outlined from the case study.') for i in (1,2)]),
('13b','0-10',[16,17],[13],'Explain periodisation and outline its importance in terms of preparing for the Olympic Games every four years.',
 [('Explanation and importance',10,'Clear and accurate explanation and contextualised importance: 8–10; accurate explanation and importance: 5–7; accurate explanation with limited importance: 1–4.')]),
('13c','0-12',[16,18],[13],'Róisín Ní Riain swam the 100m backstroke and Daniel Wiffen swam the 10km open water swim. These events place different energy demands on the body. Explain how an understanding of the ATP-PC (alactic) and aerobic (oxidative) energy systems can inform preparation for performance.',
 [('Energy systems and preparation',12,'Clear, accurate, cohesive explanation of both systems linked to preparation, with examples: 10–12; accurate linked explanation: 6–9; limited explanation: 3–5; accurate information about the systems: 1–2.')]),
('13d','1-17',[16,19],[14],'Discuss, using two examples, how developments in technology can positively impact on the performer in a selected physical activity. You may not refer to swimming.',
 [('Discussion',12,'Accurate, cohesive, concise discussion, judgement and two clear activity examples: 10–12; accurate discussion with limited cohesion, some judgement and two examples: 7–9; some links with examples: 4–6; limited discussion: 1–3. Swimming is excluded.')]),
('13e','0-12',[16,20],[15],'Discuss, using examples, the nutritional considerations for after performance in a selected physical activity.',
 [('Discussion',12,'Accurate, cohesive, concise discussion with examples, timing, nutrients, functions and judgement: 10–12; accurate discussion with limited cohesion and examples: 7–9; some relevant links: 4–6; limited discussion: 1–3.')]),
('14a','0-1',[21],[16],'Define ability.',
 [('Definition',4,'Clear and accurate definition as it applies to PE: 4; accurate definition: 1–2.',[0,1,2,4])]),
('14b','0-3',[21],[16],'Name and outline the stages of skill learning.',
 [('Stages',9,'All stages accurately named and clearly outlined with examples: 8–9; accurately named and outlined with examples: 5–7; correctly named with some outline: 3–4; at least one stage correctly named: 1–2.')]),
('14c','0-3',[22],[17],'Identify three principles of effective practice that can be used in designing skill practice sessions aimed at improving skill performance. Justify your choices.',
 [fixed(f'Principle {i}',1,'Appropriate principle of effective practice.') for i in range(1,4)]+repeat('Justification',3,4,'Relevant and accurate justification linked to designing practice for skill improvement, with at least one example: 3–4; some justification: 1–2.')),
('14d','0-23',[23],[17],'Compare the performances depicted in Figure 7 and Figure 8 in terms of aesthetic or artistic criteria of performance.',
 [('Comparison',12,'Clear, accurate criteria used to compare both pictured performances with examples: 10–12; appropriate comparison with examples: 7–9; accurate comparison: 4–6; limited reference to criteria: 1–3. Both original performances must be compared.')]),
('15a','1-1',[24],[18],'Identify four benefits of physical activity participation.',
 [fixed(f'Benefit {i}',1,'Appropriate benefit.') for i in range(1,5)]),
('15b','1-20',[24],[18],'Explain hegemonic femininity and hegemonic masculinity.',
 [(x,5,'Clear and accurate explanation with at least one example: 4–5; accurate explanation: 1–3.') for x in ('Hegemonic femininity','Hegemonic masculinity')]),
('15ci','1-21',[25],[18],'Explain body image.',
 [('Explanation',4,'Clear and accurate: 3–4; accurate: 1–2.')]),
('15cii','1-21',[25],[19],'Describe, using two examples, how body image may influence physical activity participation.',
 [('Description',10,'Clear and accurate description with two relevant, accurate examples: 8–10; accurate description with two examples: 5–7; accurate links between body image and participation: 1–4.')]),
('15d','1-3',[26],[19],'Identify two supports for physical activity participation in the community and explain how each support could help enhance participation.',
 [fixed(f'Support {i}',1,'Relevant community support identified.') for i in (1,2)]+repeat('Explanation',2,5,'Clear and accurate explanation of enhanced participation, with examples: 4–5; accurate explanation: 1–3.')),
('16a','1-7',[27],[20],'List four statements that comply with the Principles of Ethical Practice and could be included in a code of ethics for sport.',
 [('Four statements',6,'Appropriate statements complying with ethical practice: first two correct responses 2 each, next two 1 each. One correct: 2; two: 4; three: 5; four: 6.',[0,2,4,5,6])]),
('16b','1-10',[28],[20],'Identify three sports supplements, their function and the performance effect associated with their use. You may not use creatine.',
 [allocation for i in range(1,4) for allocation in [fixed(f'Supplement {i}',1,'Appropriate supplement other than creatine.'),fixed(f'Function {i}',1,'Accurate function of this supplement.'),fixed(f'Performance effect {i}',2,'Correct performance effect of this supplement.')]]),
('16c','1-6',[29],[21],'Describe, using two examples, the impact of either sportsmanship or gamesmanship on engagement in physical activity.',
 [('Description',10,'Clear and accurate description with two relevant, accurate examples of the selected concept: 8–10; accurate description with two examples: 5–7; accurate links to physical activity: 1–4.')]),
('16d','1-8',[30],[21],'Discuss the implications, for the performer, of using performance-enhancing drugs. Use at least two examples.',
 [('Discussion',12,'Accurate, cohesive, concise discussion with examples and judgement: 10–12; accurate discussion with limited cohesion and examples: 7–9; some implications with at least one example: 4–6; limited discussion: 1–3.')]),
('17ai','0-11',[31],[22],'Define the psychological factor confidence.',
 [('Definition',4,'Clear and accurate: 3–4; accurate: 1–2.')]),
('17aii','0-11',[31],[22],'Define the psychological factor motivation.',
 [('Definition',4,'Clear and accurate: 3–4; accurate: 1–2.')]),
('17b','0-11',[32],[22],'Name two psychological strategies that an athlete could use to improve mental preparedness for performance and explain how each strategy could impact performance.',
 [fixed(f'Strategy {i}',1,'Appropriate psychological strategy.') for i in (1,2)]+repeat('Impact',2,4,'Accurate explanation of how the named strategy impacts performance: 3–4; accurate explanation of the strategy: 1–2.')),
('17c','0-10',[33],[23],'Identify two principles of training and explain how effective use of each principle may lead to improved performance.',
 [fixed(f'Principle {i}',1,'Correct training principle.') for i in (1,2)]+repeat('Explanation',2,4,'Clear and accurate explanation of effective use leading to improved performance: 3–4; accurate explanation linking the principle to performance: 1–2.')),
('17d','0-8',[34],[23],'Discuss the extent to which each component of fitness is required in a physical activity of your choice: reaction time; muscular endurance; power.',
 [('Discussion of all three components',12,'Accurate, cohesive, concise discussion of all three correctly explained components, relevance, level of need, examples and judgement: 10–12; accurate discussion with limited cohesion, relevance and examples: 7–9; discussion of the three components’ requirements: 4–6; some links to the activity: 1–3.')]),
('18a','1-1',[35],[24],'Outline two economic benefits of physical activity participation.',
 repeat('Economic benefit',2,3,'Clear and accurate outline: 3; accurate outline: 1–2.')),
('18b','1-3',[36],[24],'Explain two characteristics associated with significant people, such as role models, who promote others’ participation in physical activity.',
 repeat('Characteristic',2,5,'Appropriate characteristic named with clear, concise explanation linking it to promoting others’ participation and at least one example: 3–5; named with accurate explanation: 1–2.')),
('18c','1-21',[37],[25],'It may be commented that gender stereotyping can impact physical activity participation. Describe, using two examples, the role of the media in maintaining gender stereotypes of women in sport.',
 [('Description',12,'Clear and accurate description with two clear, appropriate examples: 10–12; accurate description with two examples: 7–9; accurate description: 4–6; appropriate links between media and women in sport: 1–3.')]),
('18d','1-18',[38],[25],'“Media coverage has a positive impact on mass participation sports events.” Discuss this statement.',
 [('Discussion',12,'Accurate, cohesive, concise discussion considering whether the statement holds, clear links, examples and judgement: 10–12; clear discussion with limited cohesion, examples and consideration of impact: 7–9; relevant discussion with limited cohesion: 4–6; limited discussion: 1–3.')]),
]
CONTEXT={
 '1a':'The original coaching/choreography illustration is included on page 3.',
 '3':'The original sports-commentator photograph is included on page 5.',
 '4b':'Name an activity, skill and correct lever class as requested in 4(a), then identify the three body parts for that same lever.',
 '5a':'The original Sport Ireland anti-doping illustration is included on page 7.',
 '5b':'Answer in the context of the 2026 examination. The original anti-doping illustration is included on page 7.',
 '8a':'The original warm-up photograph is included on page 10.',
 '8b':'The original warm-up photograph is included on page 10.',
 '9a':'The source asks you to draw on the physical activity promotion and adherence tip sheet designed during your PE studies.',
 '9b':'The source asks you to draw on a physical activity promotion and adherence tip sheet, specifically for return after a long absence.',
 '11':'Figure 5 shows the original anti-doping cartoon on page 13.',
 '14d':'Use both original images on page 23: Figure 7 (dance performance) and Figure 8 (synchronised trampoline performance).',
 '16c':'The original sportsmanship photograph and both printed checkboxes are included on page 29.',
 '18a':'The original economic-benefit illustration is included on page 35.',
 '18b':'Figure 11 is a Wimbledon image/headline asking whether Ireland can produce a Wimbledon champion. It is illustrative; your role-model examples remain open.',
 '18c':'Figure 12 shows the original “I’m a girl. Sorry. I like bags.” boxing advertisement on page 37.',
}
for part,*_ in TASKS:
    if part.startswith('13'):
        CONTEXT[part]='Read the complete “Dive into Swimming” case study and photograph on page 16, including Swim Ireland, Olympic/Paralympic swimmers, funding, training and technological developments.'
VARIANTS={
 '6':[('-and-'.join(x.lower() for x in pair),' and '.join(pair)) for pair in product(['Flexibility'],['Balance','Coordination'])],
 '16c':[(x.lower(),x) for x in ['Sportsmanship','Gamesmanship']],
}
VARIANT_REQUIREMENTS={
 '6':'Classify both components in this practice pair and outline one activity that trains both together. Flexibility is the sole HRF option; balance and coordination are the two valid PRF options.',
 '16c':'Use the selected concept and two examples of it, as required by the paper’s either/or checkbox choice.',
}
SOURCE_POOLS={
 '6':[(8,'Choose one Health Related Fitness (HRF) component and one Performance Related Fitness (PRF) component from the following:'),(8,'balance coordination flexibility')],
 '16c':[(29,'either sportsmanship or gamesmanship'),(29,'Sportsmanship'),(29,'Gamesmanship')],
}
EXPECTED_QUESTION_TOTALS={**{n:8 for n in range(1,13)},13:50,**{n:40 for n in range(14,19)}}
EXPECTED_SELECTION_SCAN=[[2,'any three'],[2,'or'],[8,'choose'],[14,'choose'],[21,'any three'],[23,'or'],[29,'either'],[29,'or'],[29,'or'],[44,'or'],[44,'or']]
EXPECTED_POOL_SCAN=[[2,'any ten'],[2,'three of'],[3,'any ten'],[8,'from the following'],[34,'of the following']]
SELECTION_REVIEW=[
 {'pages':[1,2,3,21],'kind':'exam-attempt-rule-or-boilerplate','reason':'Any ten/three section instructions and pen colour wording are not practice combinations. The scheme’s Section C heading says 80 in error; the paper and all five 40-mark allocations establish 120 attempted marks.'},
 {'pages':[8],'kind':'closed-constrained-pair','reason':'One HRF and one PRF from three printed components gives two valid pairs: flexibility with balance or coordination. Do not generate the invalid balance/coordination pair.'},
 {'pages':[3,4,6,7,9,11,12,13,14,17,19,20,22,24,26,27,28,30,32,33,35,36,38],'kind':'open-response','reason':'Activities, demands, supports, levers, rules, principles, supplements, examples and strategies are open knowledge or the candidate’s own answer. The supplement ban and two distinct scoring systems constrain answers without creating finite printed pools.'},
 {'pages':[6,18,21,24,28,34],'kind':'required-components','reason':'All lever parts, both energy systems, all skill stages, both hegemonic concepts, all supplement columns and all three named fitness components are compulsory components, not alternatives.'},
 {'pages':[23],'kind':'flexible-wording-and-required-comparison','reason':'Aesthetic or artistic is flexible terminology, not a closed choice. The candidate must compare both printed performances.'},
 {'pages':[29],'kind':'closed-choose-one','reason':'Explicit either/or instruction and separate checkboxes create two ten-mark practice routes.'},
 {'pages':[44],'kind':'copyright','reason':'Copyright or wording is not a choice directive.'},
]
