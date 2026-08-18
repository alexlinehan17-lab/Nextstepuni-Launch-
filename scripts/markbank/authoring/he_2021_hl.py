#!/usr/bin/env python3
"""Home Economics 2021 Higher Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2021, 'higher', 'he-2021-hl-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "The infographic shows two influencing factors on evening meal consumption: Health and Wellbeing (42%) and Responsible Living (27%). (What Ireland Ate Last Night Report 2020, Bord Bia Thinking House)"
hw = semis(block(T, 'Increased knowledge of healthy eating guidelines', '(ii) Responsible living'))
rl = semis(block(T, 'Packaging; food miles; plant based diets', '(b) Identify and describe contemporary trends'))
cards.append(card(
    f'{P}-q1a', Y, L, 'home-economics-0-10', 'health-responsible-living-food-choice',
    '2021 HL Section B Q1(a)',
    'In relation to the infographic above, suggest how (i) health and wellbeing and (ii) responsible living might influence food choices.',
    '4 points @ 5 marks (graded 5:3:1:0); 2 references to health and wellbeing, 2 references to responsible living',
    20,
    [anyN('r-1', 'How health and wellbeing might influence food choices', 10, 2, 5, hw[:14],
          "Two points at 5 marks. The split is fixed at two and two — this half cannot be padded to make up for the other. Health and wellbeing is about the eater: what they are trying to increase or reduce, what they cannot eat, what they are trying to weigh."),
     anyN('r-2', 'How responsible living might influence food choices', 10, 2, 5, rl[:14],
          "Two points at 5 marks. Responsible living is about everything except the eater — food miles, packaging, water footprint, buying local, avoiding waste. Students who know the health half well often lose all 10 here by treating it as more healthy eating.")],
    "The question names two halves and the scheme fixes two references to each, so two rows rather than a pooled four.",
    stem=Q1S, tariff_kind='fixed'))

tr = semis(block(T, 'Nutritiously conscious; take away foods', '(c) Micronutrients are essential'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-1', 'contemporary-irish-eating-trends',
    '2021 HL Section B Q1(b)',
    'Identify and describe contemporary trends in Irish eating patterns.',
    '3 trends @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Identify and describe contemporary trends in Irish eating patterns', 12, 3, 4, tr[:14],
          "Three trends at 4 marks, graded 4:2:0 — identify is 2, describe is 4. \"Contemporary\" is doing work: the scheme includes dashboard dining, food bloggers, intermittent fasting and more home cooking during the pandemic. A trend that has been true for fifty years is not contemporary.")],
    "One flat list, taken in order to the cap.",
    stem=Q1S))

_haem_b = block(T, 'Haem iron found in red meats', 'Non-haem iron in cereals')
_non_b = block(T, 'Non-haem iron in cereals', '• biological functions')
isrc = semis(_haem_b, drop_prefix='Haem iron found in')[:6] + semis(_non_b, drop_prefix='Non-haem iron in')[:7]
ifun = semis(block(T, 'Essential component of haemoglobin', '• effects of deficiency'))
idef = semis(block(T, 'Anaemia; tiredness/ fatigue; irritability', '(d) Identify and explain two factors'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-8', 'iron-account-hl',
    '2021 HL Section B Q1(c)',
    'Give an account of Iron with reference to: sources in the diet; biological functions; effects of deficiency.',
    'sources 3 @ 2 marks (graded 2:0), 1 reference to haem iron, 1 reference to non-haem iron + 1 other; functions 3 @ 2 marks (graded 2:0); deficiencies 3 @ 2 marks (graded 2:0)',
    18,
    [anyN('r-1', 'Sources in the diet', 6, 3, 2, isrc,
          "Three sources at 2 marks, all-or-nothing, and the scheme reserves one for haem and one for non-haem — three red meats cannot score 6. Saying which type a food provides is what makes the reference count."),
     anyN('r-2', 'Biological functions', 6, 3, 2, ifun,
          "Three functions at 2 marks, all-or-nothing. Haemoglobin and carrying oxygen is the core, but they are one function in two halves — pair it with myoglobin or the enzyme systems for genuinely separate points."),
     anyN('r-3', 'Effects of deficiency', 6, 3, 2, idef[:14],
          "Three effects at 2 marks, all-or-nothing. Anaemia is the named condition; the rest are its symptoms, and the scheme accepts them as separate points, so this is the easiest 6 marks in the question.")],
    "18 marks split evenly, 6 + 6 + 6, all all-or-nothing. Nine short points and no partial credit anywhere.",
    stem=Q1S, tariff_kind='fixed'))

assist = tidy(block(T, 'Vitamin C – consuming food high in vitamin C', 'Factors that inhibit iron absorption'))
inhibit = tidy(block(T, 'oxalic acid; phytic acid; fibre intake', '(e) Devise a set of strategies'))
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-0-8', 'iron-absorption-hl',
    '2021 HL Section B Q1(d)',
    'Identify and explain two factors which affect the absorption of iron in the body.',
    '2 factors @ 5 marks (graded 5:4:3:2:1:0)', 10,
    [anyN('r-1', 'Identify and explain two factors which affect the absorption of iron in the body', 10, 2, 5,
          [assist, inhibit],
          "Only two factors, but on a full 5-to-0 ladder — every mark is earned separately, so this is the part of Q1 where chemistry pays. The scheme's explanations are at a level most answers never reach: Vitamin C chemically changes non-haem iron to the more absorbable form, sulphur-containing amino acids convert ferric (Fe3+) to ferrous (Fe2+), tannins bind to iron. Naming a factor is 1 or 2; the mechanism is the rest.")],
    "The scheme's two groups, assisting and inhibiting, kept whole because each carries its own mechanism and the mechanism is where the marks are.",
    stem=Q1S))

pur_b, pln_b = heads(block(T, 'Purchasing: make a shopping list', 'Question 2'), ['Purchasing:', 'Planning:'])
strat = semis(pur_b, drop_prefix='Purchasing:')[:7] + semis(pln_b, drop_prefix='Planning:')[:7]
cards.append(card(
    f'{P}-q1e', Y, L, 'home-economics-0-10', 'irregular-routine-meal-strategies',
    '2021 HL Section B Q1(e)',
    'Devise a set of strategies when purchasing foods and planning meals for families with irregular daily routines.',
    '5 strategies @ 4 marks (graded 4:2:0); 2 references to purchasing, 2 references to planning + 1 other',
    20,
    [anyN('r-1', 'Devise strategies for purchasing foods and planning meals for families with irregular daily routines',
          20, 5, 4, strat,
          "Five strategies at 4 marks, with two reserved for purchasing and two for planning, leaving one free. \"Irregular daily routines\" is the whole point: dishes that reheat well for staggered mealtimes, cooking in bulk and freezing, frozen vegetables for emergencies. A generic meal-planning answer misses what the question is actually about.")],
    "The scheme groups the strategies under purchasing and planning and reserves two marks for each; the options are the individual strategies taken evenly from both so neither is lost to the cap.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "Eggs are a good choice as part of a healthy, balanced diet."
emul = semis(block(T, 'An emulsifier lecithin in egg yolk', 'Culinary application:'))
capp = semis(block(T, 'Culinary application: mayonnaise', '(c) Evaluate the role of food labelling'),
             drop_prefix='Culinary application:')
cards.append(card(
    f'{P}-q2b', Y, L, 'home-economics-0-2', 'eggs-as-emulsifier',
    '2021 HL Section B Q2(b)',
    'Describe how eggs work as an emulsifier in food production. Refer to one culinary application.',
    '5 points @ 3 marks (graded 3:2:0); culinary application 1 @ 3 marks (graded 3:0)', 18,
    [anyN('r-1', 'Describe how eggs work as an emulsifier in food production', 15, 5, 3, emul,
          "Five points at 3 marks. This is one mechanism told in order, and each step is a separate mark: lecithin in the yolk, a hydrophilic head attracted to water, a hydrophobic tail attracted to oil, the two held together, a permanent emulsion formed. Naming lecithin without the two ends of it gets a fraction of what is on offer."),
     anyN('r-2', 'Culinary application', 3, 1, 3, capp,
          "One culinary application, 3 marks, all-or-nothing — a sixth of the question for one word. Mayonnaise is the standard answer and the scheme also accepts creaming fat and sugar in cakes.")],
    "18 marks split 15 + 3. Two rows because the application is priced and graded separately from the mechanism.",
    stem=Q2S, tariff_kind='fixed'))

egglab = semis(block(T, 'Egg packs must have the following information', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-1-2', 'egg-labelling',
    '2021 HL Section B Q2(c)',
    'Evaluate the role of food labelling as a source of consumer information when buying eggs.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Evaluate the role of food labelling as a source of consumer information when buying eggs',
          12, 3, 4, egglab[:14],
          "Three points at 4 marks. Egg labelling has specifics no other food has, and they are the marks worth taking: every individual egg stamped with a traceability code, the week number, the farming method, and the Bord Bia quality assurance symbol for salmonella-free flocks. \"Evaluate\" wants what the information lets a buyer decide.")],
    "One flat list, taken in order to the cap.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "Temperature control is critical to ensuring food safety for all consumers."
sto_b, ck_b = heads(block(T, 'Storage: Refrigerate perishable foods', '(b) Describe the stages in a Hazard Analysis'),
                    ['Storage:', 'Cooking/Reheating:'])
temp = semis(sto_b, drop_prefix='Storage:')[:7] + semis(ck_b, drop_prefix='Cooking/Reheating:')[:7]
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-4', 'temperature-control-food-safety',
    '2021 HL Section B Q3(a)',
    'Discuss the importance of temperature control during the storage and cooking/reheating of food.',
    '4 points @ 4 marks (graded 4:2:0); 2 references to storage, 2 references to cooking/reheating', 16,
    [anyN('r-1', 'Discuss the importance of temperature control during the storage and cooking/reheating of food',
          16, 4, 4, temp,
          "Four points at 4 marks, split two and two between storage and cooking — neither half can carry the other. Every point here is a number and the numbers ARE the marks: 0-5C for perishables, -25C to freeze and -18C to store, 100C to reheat, above 65C to hold, and the danger zone of 6-63C. A point without its temperature is half a point.")],
    "The scheme groups by storage and cooking/reheating with two references reserved for each; the options are the individual points taken evenly from both groups.",
    stem=Q3S))

inf = tidy(block(T, 'Infectious food poisoning - caused by consumption', 'Toxic food poisoning -'))
tox = tidy(block(T, 'Toxic food poisoning - ingesting food', 'Question 4'))
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-4', 'infectious-vs-toxic-food-poisoning',
    '2021 HL Section B Q3(c)',
    'Differentiate between infectious food poisoning and toxic food poisoning.',
    '2 points @ 5 marks (graded 5:3:2:0)', 10,
    [anyN('r-1', 'Differentiate between infectious food poisoning and toxic food poisoning', 10, 2, 5,
          [inf, tox],
          "Two points at 5 marks, and \"differentiate\" means the contrast has to be explicit. Three clean contrasts run through the scheme: endotoxins produced inside the cell against exotoxins produced outside it; easy to destroy against needing 30 minutes' boiling; symptoms after about 12 hours against within 2. Each option carries its own named bacteria, and mixing them up loses the point.")],
    "The two types kept whole, each with its mechanism, timing and examples, because the marks are in the comparison rather than in either description alone.",
    stem=Q3S))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "Efficient home management guides the smooth running of the home."
mg = semis(block(T, 'Needs of the family are met; provision of basic needs', '(b) Using the management framework'))
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-0', 'management-systems-home',
    '2021 HL Section B Q4(a)',
    'Explain how good management systems contribute to a well-run home.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Explain how good management systems contribute to a well-run home', 16, 4, 4, mg[:14],
          "Four points at 4 marks, graded 4:2:0. The list divides into what management achieves (needs met, resources used, quality of life) and what it avoids (conflict, stress, fatigue) — taking from both sides makes four clearly different points. \"Explain how\" means naming the mechanism, not the benefit.")],
    "One flat list, taken in order to the cap.",
    stem=Q4S))

fw = (semis(block(T, 'Inputs – Demands – needs', 'Throughputs – planning'))[:5]
      + semis(block(T, 'Throughputs – planning; organising', 'Outputs – assess'))[:5]
      + semis(block(T, 'Outputs – assess / evaluate', '(c) Evaluate the use of credit'))[:4])
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-0', 'management-framework-holiday',
    '2021 HL Section B Q4(b)',
    'Using the management framework (inputs, throughputs and outputs) outline the strategies to be followed when planning a family holiday to ensure effective management of resources.',
    '6 points @ 3 marks (graded 3:2:1:0); 2 references to inputs, 2 to throughputs, 2 to outputs', 18,
    [anyN('r-1', 'Outline the strategies to be followed when planning a family holiday, using inputs, throughputs and outputs',
          18, 6, 3, fw,
          "Six points at 3 marks, two reserved for each of inputs, throughputs and outputs — a strict two-two-two, so an answer strong on planning and silent on evaluation caps at 12. The framework is the answer: inputs are demands and resources, throughputs are planning, organising and implementing, outputs are the evaluation. Tie each to the holiday — booking accommodation is implementing; asking whether everyone enjoyed it is an output.")],
    "The options are individual points taken evenly across inputs, throughputs and outputs, so the option cap cannot delete a stage the scheme reserves two marks for. The two-per-stage rule is carried in the notation.",
    stem=Q4S))

credit = (semis(block(T, 'Advantages - consumer has the use of travel', 'Disadvantages –'), drop_prefix='Advantages -')[:7]
          + semis(block(T, 'Disadvantages – expensive, high rates of interest', 'Question 5'))[:7])
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-1', 'credit-for-holiday',
    '2021 HL Section B Q4(c)',
    'Evaluate the use of credit as a method of payment for a family holiday.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Evaluate the use of credit as a method of payment for a family holiday', 16, 4, 4, credit,
          "Four points at 4 marks. \"Evaluate\" means both sides — an answer that is only advantages is not an evaluation, however well written. The holiday framing matters: use of travel and accommodation before paying for it, safer than carrying cash abroad, against high interest, surcharges and blowing the holiday budget.")],
    "Individual advantages and disadvantages taken evenly from both sides, since an evaluation needs both and the cap must not silently remove one.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "The modern Irish family is smaller and more diverse than ever before."
defn = tidy(block(T, 'Group of people related to each other by blood', 'Universality @ 5 marks'))
univ = tidy(block(T, 'Family is present in all known societies', '(b) Explain how the family can meet'))
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-0', 'family-definition-universality',
    '2021 HL Section B Q5(a)',
    'Define the term family and explain the concept of the universality of the family.',
    'definition @ 5 marks (graded 5:3:0); universality @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Define the term family', 5, 1, 5, [defn],
          "The definition alone is 5 marks, graded 5:3:0. The scheme gives three usable forms — blood, marriage or adoption; the United Nations wording; and the Irish Constitution's \"natural, primary and fundamental unit group of society\". Quoting one of the named sources is the safest route to 5."),
     anyN('r-2', 'Explain the concept of the universality of the family', 5, 1, 5, [univ],
          "Universality is 5 marks for two clauses: the family exists in all known societies, AND the form it takes differs between them. Giving only the first is the classic 3 — the variation is half the concept.")],
    "10 marks split evenly between definition and concept, so two rows.",
    stem=Q5S, tariff_kind='fixed'))

nd = heads(block(T, 'Physical - family protects', '(c) Discuss the challenges'),
           ['Physical -', 'Emotional -', 'Economic -', 'Social -'])
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-0', 'family-meeting-needs',
    '2021 HL Section B Q5(b)',
    'Explain how the family can meet the physical, emotional, economic and social needs of its members.',
    '4 points @ 6 marks (graded 6:4:2:0)', 24,
    [anyN('r-1', 'Explain how the family can meet the physical, emotional, economic and social needs of its members',
          24, 4, 6, nd,
          "Four points at 6 marks — the biggest part of this question at 24 marks, and all four needs are named, so there is no choosing. Graded 6:4:2:0, which means naming the need is 2 and everything above comes from explaining HOW the family meets it. Economic is the thinnest list in the scheme and the one most often left underwritten.")],
    "The four needs the question names, each carrying the scheme's own explanation.",
    stem=Q5S, answer=4, of_parts=4, per_part=6))

ch = semis(block(T, 'Coping with challenging behaviour in the home', None))
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-0', 'family-special-needs-challenges',
    '2021 HL Section B Q5(c)',
    'Discuss the challenges that may be experienced by the family of a child with special needs.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Discuss the challenges that may be experienced by the family of a child with special needs',
          16, 4, 4, ch[:14],
          "Four challenges at 4 marks, graded 4:2:0. The scheme spreads them across the whole family, not just the child — a parent giving up work, siblings taking on responsibility, less attention for other members, worry about the future. Four challenges all about the child himself covers only part of what the question asks.")],
    "One flat list, taken in order to the cap.",
    stem=Q5S))

emit(cards)
