#!/usr/bin/env python3
"""Home Economics 2022 Higher Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2022, 'higher', 'he-2022-hl-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "'Health-related habits developed during teenage years tend to persist into adulthood' (iuna.net). The chart shows the factors that make it difficult for teenagers to eat a healthy diet, from the National Teens Food Survey II. (adapted from iuna.net)"
fac = heads(block(T, 'Likes/dislikes influence of the senses', '(b) Give a detailed account of the dietary measures'),
            ['Likes/dislikes influence', 'Convenience availability', 'Availability foods in season',
             'Cost money available', 'Advertising product placement', 'Other culture'])
cards.append(card(
    f'{P}-q1a', Y, L, 'home-economics-0-1', 'teenage-healthy-eating-barriers',
    '2022 HL Section B Q1(a)',
    'Using the information provided in the chart, comment and elaborate on the factors that make it difficult for teenagers to eat a healthy diet.',
    '4 points @ 5 marks (graded 5:4:3:2:1:0)', 20,
    [anyN('r-1', 'Comment and elaborate on the factors that make it difficult for teenagers to eat a healthy diet',
          20, 4, 5, fac,
          "Four factors at 5 marks on a full 5-to-0 ladder — depth is paid a mark at a time, so four written well beats six named. Convenience and availability overlap heavily and a marker will not pay twice for the same idea; taking one of those plus likes/dislikes, cost and advertising gives four clearly separate factors. \"Elaborate\" means naming the mechanism, not the factor: adapted taste buds, product placement, eating on the go.")],
    "Six factors in the scheme, best four taken.",
    stem=Q1S))

diet = semis(block(T, 'Use of food pyramid to ensure balance', '(c) An adequate intake of Vitamin D'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-10', 'teenage-dietary-measures',
    '2022 HL Section B Q1(b)',
    'Give a detailed account of the dietary measures to follow when planning and preparing meals for teenagers.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Give a detailed account of the dietary measures to follow when planning and preparing meals for teenagers',
          20, 4, 5, diet[:14],
          "Four measures at 5 marks, graded 5:3:0 — named is 3, detailed is 5. What makes a measure teenage-specific is the growth spurt and the activity level: iron for menstruating girls, calcium and Vitamin D for bone growth, energy requirements peaking when growth and activity coincide. A generic healthy-eating answer that would suit any age stays at 3 a point.")],
    "The scheme prints one long list covering both planning and preparation, taken in order to the cap.",
    stem=Q1S))

vfun = semis(block(T, 'Absorption of calcium; absorption of phosphorous', 'Effects of deficiency'))
vdef = semis(block(T, 'Rickets in children; osteomalacia', 'Properties'))
vprop = semis(block(T, 'White crystalline solid; fat soluble', '(d) Discuss how the health status'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-8', 'vitamin-d',
    '2022 HL Section B Q1(c)',
    'Give an account of Vitamin D with reference to: biological functions; effects of deficiency; properties.',
    'biological functions 4 points @ 2 marks (graded 2:0); effects of deficiency 3 points @ 2 marks (graded 2:0); properties 3 points @ 2 marks (graded 2:0)',
    20,
    [anyN('r-1', 'Biological functions', 8, 4, 2, vfun,
          "Four functions at 2 marks, all-or-nothing. Every function on this list is about calcium and phosphorus — absorbing them, using them for bone and teeth, balancing them between blood and skeleton. That is the whole of Vitamin D's job and the four points are four angles on it."),
     anyN('r-2', 'Effects of deficiency', 6, 3, 2, vdef,
          "Three effects at 2 marks, all-or-nothing. Rickets in children and osteomalacia in adults is the pair the examiner looks for, and naming who gets which is what makes them two separate points rather than one."),
     anyN('r-3', 'Properties', 6, 3, 2, vprop,
          "Three properties at 2 marks, all-or-nothing. Vitamin D is the stable one — unaffected by heat, oxygen, acids and alkalis — which is the opposite of Vitamin C and is exactly why examiners set them against each other.")],
    "20 marks split 8 + 6 + 6, every strand all-or-nothing. Ten short points; there is no partial credit anywhere, so precision beats length.",
    stem=Q1S, tariff_kind='fixed'))

hs = semis(block(T, 'Special dietary requirements; restricted diets', 'Question 2'))
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-0-1', 'health-status-food-choice',
    '2022 HL Section B Q1(d)',
    'Discuss how the health status of an individual can influence their choice when purchasing foods.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Discuss how the health status of an individual can influence their choice when purchasing foods',
          20, 5, 4, hs,
          "Five points at 4 marks, graded 4:2:0. The list is almost all named conditions, so the 2 is easy — the second 2 comes from saying what the person actually does differently in the shop: reads labels for gluten, checks for lactose, avoids high-salt foods. A list of five conditions with no purchasing behaviour attached scores 10 of 20.")],
    "One flat list, evenly priced.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "Vegan diets are increasing in popularity; however, these diets require careful planning."
veg = heads(block(T, 'Protein include a combination of wholegrains', '(b) Set out details of an alternative protein food'),
            ['Protein include', 'Calcium use fortified', 'Iron include plant', 'Vitamin D include fortified', 'Vitamin B12 include'])
cards.append(card(
    f'{P}-q2a', Y, L, 'home-economics-0-5', 'vegan-diet-deficiencies',
    '2022 HL Section B Q2(a)',
    'Identify three nutrients that could be deficient in a vegan diet and outline a strategy to prevent the deficiency of each nutrient.',
    '3 points @ 6 marks (graded 6:4:2:0); (name nutrient 2 marks (graded 2:0), strategy 1 point @ 4 marks (graded 4:2:0)) x3',
    18,
    [anyN('r-1', 'Identify three nutrients that could be deficient in a vegan diet and outline a strategy to prevent each deficiency',
          18, 3, 6, veg,
          "Three nutrients at 6 marks, and each 6 splits 2 for naming the nutrient and 4 for the strategy. Each option carries its own strategy because they are marked as a pair — a fortified-foods answer attached to the wrong nutrient does not earn the 4. Naming three nutrients and stopping scores 6 of 18.")],
    "Five nutrients in the scheme, best three taken, each kept with its own strategy.",
    stem=Q2S))

alt = heads(block(T, 'Textured Vegetable Protein soya beans are cleaned', '(c) Indicate how European Union'),
            ['Textured Vegetable Protein', 'Mycoprotein fungi', 'Tofu soya milk', 'Soya milk soya beans',
             'Soya yoghurt non-dairy', 'Tempeh soya beans', 'Miso soya beans'])
cards.append(card(
    f'{P}-q2b', Y, L, 'home-economics-0-5', 'alternative-protein-food',
    '2022 HL Section B Q2(b)',
    'Set out details of an alternative protein food you have studied. Refer to: name; stages in manufacture.',
    'name 2 marks (graded 2:0); stages in manufacture 6 points @ 3 marks (graded 3:2:0)', 20,
    [anyN('r-1', 'Name an alternative protein food and set out its stages of manufacture', 20, 1, 20, alt,
          "ONE alternative protein food, worth 20 marks: 2 for naming it and 6 stages at 3. Pick one and stay in it — the scheme prices seven separate processes and stages cannot be mixed between them. Each is an ordered sequence and every one of them ends the same way, packaged and labelled, which are two of the six stages and the two most often left off.")],
    "Seven foods in the scheme, one chosen; each kept whole because its stages belong to it. The naming mark is carried in the notation.",
    stem=Q2S, answer=1, of_parts=7, per_part=20))

eu = semis(block(T, 'Additives are tested; provide a list of approved additives', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-0-11', 'eu-additive-legislation',
    '2022 HL Section B Q2(c)',
    'Indicate how European Union (EU) legislation in relation to food additives protects the consumer.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Indicate how EU legislation in relation to food additives protects the consumer', 12, 3, 4, eu,
          "Three points at 4 marks, graded 4:2:0. The E number is the point to lead with — approved additives carry one, it must appear on the label, and flavourings are the exception. The rest of the list is about limits: smallest effective quantity, cannot disguise faults, cannot mislead.")],
    "One flat list, evenly priced.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "Micro-organisms and enzymes have a role to play in food spoilage and food production."
enz = heads(block(T, 'Over-ripening enzymes ripen food', '(b) Name and give details of one type of mould'),
            ['Over-ripening enzymes', 'Enzymic browning when', 'Enzymic deterioration enzymes'])
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-4', 'enzymes-food-spoilage',
    '2022 HL Section B Q3(a)',
    'Discuss the role of enzymes in relation to food spoilage.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN('r-1', 'Discuss the role of enzymes in relation to food spoilage', 15, 3, 5, enz,
          "Three points at 5 marks, and the scheme gives exactly three — so all three are needed and there is no choosing. Each one names an enzyme mechanism: over-ripening, enzymic browning by oxidase, and deterioration that continues even at freezer temperatures. Naming the process is 3; naming oxidase and the oxidation reaction is the 5.")],
    "Three mechanisms, all three required, each kept with its own explanation.",
    stem=Q3S))

cond = heads(block(T, 'Food saprophytic, feeding on bread', '(c) Assess the uses of micro-organisms'),
             ['Food saprophytic', 'Oxygen Aerobic', 'Temperature Most are mesophilic',
              'Moisture require moisture', 'pH level moulds', 'Time 24 to 48 hours'])
cards.append(card(
    f'{P}-q3b-conditions', Y, L, 'home-economics-0-4', 'mould-growth-conditions',
    '2022 HL Section B Q3(b) — conditions for growth',
    'Name and give details of one type of mould. Refer to: conditions necessary for growth.',
    'conditions necessary for growth 4 points @ 3 marks (graded 3:2:1:0)', 12,
    [anyN('r-1', 'Conditions necessary for growth', 12, 4, 3, cond,
          "Four conditions at 3 marks on a 3:2:1:0 ladder, so partial knowledge is paid for at every step. The six conditions are the standard set for any micro-organism — food, oxygen, temperature, moisture, pH, time — and the marks are in the specifics: mesophilic, slowed below 15C, destroyed above 75C, pH 4 to 6, 24 to 48 hours. A condition named without its number sits at 1.")],
    "Q3(b) is 23 marks: 2 for the name, 9 for characteristics and 12 for conditions. This card carries the conditions strand, which is the largest and is the same for any mould chosen. The name-and-characteristics strand is a four-row table the extraction interleaves and is held separately.",
    stem=Q3S))

mo = semis(block(T, 'Yeast produces CO2, raising agent in bread', 'Question 4'))
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-11', 'micro-organisms-food-production',
    '2022 HL Section B Q3(c)',
    'Assess the uses of micro-organisms in food production.',
    '3 points @ 4 marks (graded 4:3:2:1:0)', 12,
    [anyN('r-1', 'Assess the uses of micro-organisms in food production', 12, 3, 4, mo,
          "Three points at 4 marks on a full 4-to-0 ladder. Each entry in the scheme is a complete answer in itself — the organism, what it does, and the food it does it in — and writing all three parts is what reaches 4. \"Yeast\" alone is a 1; \"yeast produces CO2 which raises bread\" is a 4.")],
    "One flat list; each option is already organism, action and food, which is the shape of a full 4.",
    stem=Q3S))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "'Homeownership is good for individuals, families and communities.' (Housing for All, 2021)"
soc = semis(block(T, 'Purchase cost; location; amenities', '(b) Discuss the conditions that lending institutions'))
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-3-3', 'socio-economic-housing-factors',
    '2022 HL Section B Q4(a)',
    'Analyse the socio-economic factors that determine housing choices for potential buyers.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Analyse the socio-economic factors that determine housing choices for potential buyers',
          16, 4, 4, soc[:14],
          "Four factors at 4 marks, graded 4:2:0. The word is \"socio-economic\", so the strongest answers pair a money factor with a household one — purchase cost against size of household, BER rating against running costs. \"Analyse\" wants the trade-off: what a buyer gives up to get it.")],
    "One flat list, taken in order to the cap.",
    stem=Q4S))

mort = semis(block(T, 'Term of the loan older applicants', '(c) Explain how consumers are protected'))
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-1', 'mortgage-conditions',
    '2022 HL Section B Q4(b)',
    'Discuss the conditions that lending institutions require for potential buyers in order to qualify for a mortgage.',
    '4 points @ 6 marks (graded 6:4:2:0)', 24,
    [anyN('r-1', 'Discuss the conditions that lending institutions require for potential buyers in order to qualify for a mortgage',
          24, 4, 6, mort,
          "Four conditions at 6 marks — the highest per-point value in this Section B, so each one needs real development. The numbers are the marking content: up to three and a half times gross salary, 10% deposit for first-time buyers. A condition named without its figure will not reach 6, and the ladder drops straight to 4.")],
    "One flat list, evenly priced; the scheme's own figures are kept inside the options.",
    stem=Q4S))

sog = semis(block(T, 'Act confers a legally binding contract', 'Question 5'))
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-2', 'sale-of-goods-services-electrician',
    '2022 HL Section B Q4(c)',
    'Explain how consumers are protected by the Sale of Goods and Supply of Services Act (1980) when availing of the services of an electrician in the home.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Explain how consumers are protected by the Sale of Goods and Supply of Services Act (1980) when availing of the services of an electrician',
          10, 2, 5, sog,
          "Two points at 5 marks. The question is about SERVICES, not goods — so the points that answer it are the ones about the tradesperson: registered and skilled, appropriately insured, due care and diligence, a cert on completion. Quoting the merchantable-quality rules for goods answers a different question.")],
    "One flat list, evenly priced.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "Marriage and families are recognised social structures."
leg = heads(block(T, 'Over 18: both partners must be over 18', '(b) Analyse how socio-economic factors'),
            ['Over 18:', 'Mental capacity:', 'Notification:', 'Registered venue:',
             'Free to marry:', 'Voluntary basis:', 'Wedding registration:', 'Not closely related:'])
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-1', 'legal-obligations-marriage',
    '2022 HL Section B Q5(a)',
    'Describe the legal obligations for marriage in Ireland.',
    '4 points @ 4 marks (graded 4:2:0)', 16,
    [anyN('r-1', 'Describe the legal obligations for marriage in Ireland', 16, 4, 4, leg,
          "Four obligations at 4 marks, graded 4:2:0. Every one is a rule with a condition attached, and the condition is the second 2 — three months' notice, over 18, a registered venue, free to marry. Naming the obligation without its detail is half marks, and the notice period is the specific most often forgotten.")],
    "Eight obligations in the scheme, best four taken, each kept with its own condition.",
    stem=Q5S))

older = semis(block(T, 'Changing family structures; less defined roles', '(c) State why it is important to make a will'))
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-3', 'changing-roles-older-people',
    '2022 HL Section B Q5(b)',
    'Analyse how socio-economic factors have affected the changing roles of older family members in contemporary society.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Analyse how socio-economic factors have affected the changing roles of older family members',
          20, 5, 4, older[:14],
          "Five points at 4 marks, graded 4:2:0. The word is \"changing\", so every point needs a before and after: grandparents are now more actively involved in childcare BECAUSE both parents work and childcare is expensive. The economic drivers — cost of living, childcare cost, extended lifespan, longer dependency of children — are what make this an analysis rather than a description.")],
    "One flat list, taken in order to the cap.",
    stem=Q5S))

why = semis(block(T, 'Why peace of mind; wishes will be carried out', 'Procedure may employ a solicitor'))
proc = semis(block(T, 'Procedure may employ a solicitor', None), drop_prefix='Procedure')
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-3', 'making-a-will-hl',
    '2022 HL Section B Q5(c)',
    'State why it is important to make a will and outline the procedure involved in making a will.',
    'why 2 points @ 2 marks (graded 2:0); procedure 5 points @ 2 marks (graded 2:1:0)', 14,
    [anyN('r-1', 'Why it is important to make a will', 4, 2, 2, why,
          "Two reasons at 2 marks, all-or-nothing — only 4 of the 14 marks, so state them and move on. The question says \"state\", and that is exactly what it pays for."),
     anyN('r-2', 'The procedure involved in making a will', 10, 5, 2, proc,
          "Five procedural steps at 2 marks, graded 2:1:0 — 10 of the 14 marks are here, so the procedure is the question. It is an ordered process ending with the formal requirements that make a will valid: signed in the presence of two witnesses, lodged somewhere safe. Those two are the steps most often missed and the ones that carry legal weight.")],
    "14 marks split 4 + 14-4, with the procedure carrying more than twice the reasons. Two rows because the strands are graded differently: the reasons are all-or-nothing and the steps are not.",
    stem=Q5S, tariff_kind='fixed'))

emit(cards)
