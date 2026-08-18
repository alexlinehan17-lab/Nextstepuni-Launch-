#!/usr/bin/env python3
"""Home Economics 2024 Higher Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2024, 'higher', 'he-2024-hl-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "The Eurobarometer survey 2022 and 2019 questioned consumers on factors that affect their decisions when purchasing foods. (adapted from www.efsa.europa.eu)"
f = heads(block(T, 'Cost increased since 2019', '(b) Give a detailed account of carbohydrates'),
          ['Cost increased', 'Food safety slight', 'Origin of food decrease',
           'Impact on environment huge', 'Nutrient content no change'])
cards.append(card(
    f'{P}-q1a', Y, L, 'home-economics-1-2', 'consumer-food-purchase-factors',
    '2024 HL Section B Q1(a)',
    'Using the information provided in the chart, comment and elaborate on four factors that affect consumer decisions when purchasing food.',
    '4 factors @ 5 marks each (graded 5:4:3:2:1:0)', 20,
    [anyN('r-1', 'Comment and elaborate on four factors that affect consumer decisions when purchasing food',
          20, 4, 5, f,
          "Four of the five factors the chart plots, 5 marks each on a full 5:4:3:2:1:0 ladder — depth is paid for a mark at a time, so this rewards saying more about fewer things. Each option opens with the chart's own movement since 2019 (cost up, environment sharply up, origin down, nutrient content flat), and quoting that direction is the cheapest mark on the question. \"Comment and elaborate\" then wants the why behind the movement.")],
    "Five factors on the chart, best four taken. Each option keeps its 2019 trend because the question says \"using the information provided in the chart\" — an answer that never touches the data is answering a different question.",
    stem=Q1S))

mono = semis(block(T, 'chemical formula of glucose', '• formation of disaccharides'))
di = semis(block(T, 'chemical formula C12H22O11', 'H₂O'))
bio = semis(block(T, 'heat; energy; spares protein', '(c) Describe three properties of sugar'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-6', 'carbohydrate-structure-functions',
    '2024 HL Section B Q1(b)',
    'Give a detailed account of carbohydrates and refer to: basic structure of a monosaccharide; formation of disaccharides; biological functions.',
    'monosaccharide structure 1 point @ 8 marks (graded 8:7:6:5:4:3:2:1:0); disaccharide formation 4 points @ 2 marks (graded 2:1:0); biological functions 3 points @ 2 marks (graded 2:1:0)',
    22,
    [anyN('r-1', 'Basic structure of a monosaccharide', 8, 1, 8, mono,
          "One point worth 8 marks, on a ladder that runs the whole way from 8 to 0 — the single most valuable marking point in Section B, and it is worth writing everything you know. The formula, the ring, the single sugar unit and a named example are four separate things the marker can climb; a labelled diagram earns here too."),
     anyN('r-2', 'Formation of disaccharides', 8, 4, 2, di,
          "Four points at 2 marks. The condensation reaction is the point students most often half-make: two monosaccharides joining is 1, and the water molecule eliminated is what earns the second. The formula C12H22O11 is a free 2 marks."),
     anyN('r-3', 'Biological functions', 6, 3, 2, bio,
          "Three functions at 2 marks. Half this list is fibre rather than sugar — bowel movements, cholesterol, satiety — and fibre functions count, which is what makes this the easiest of the three strands to fill.")],
    "22 marks split 8 + 8 + 6 across the question's own three bullets. The 8-mark single point is unusual and is why the strands are separate rows rather than a pooled list.",
    stem=Q1S, tariff_kind='fixed'))

props = heads(block(T, 'solubility sugars are white crystalline', '(d) Devise a set of strategies'),
              ['solubility ', 'sweetness ', 'assists aeration ', 'Maillard reaction ',
               'caramelisation ', 'crystallisation ', 'hydrolysis and inversion '])
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-2', 'properties-of-sugar',
    '2024 HL Section B Q1(c)',
    'Describe three properties of sugar and give one culinary example of each property.',
    '3 properties @ 6 marks (graded 6:5:4:3:2:1:0); [name 2 marks (graded 2:0), description 2 marks (graded 2:1:0), culinary application 2 marks (graded 2:1:0)] x3',
    18,
    [anyN('r-1', 'Describe three properties of sugar and give one culinary example of each property',
          18, 3, 6, props,
          "Three properties at 6 marks, and each 6 splits three ways: 2 for naming the property, 2 for describing it, 2 for a culinary application. That last 2 is the one most often dropped — a perfect description of caramelisation with no crème brûlée against it scores 4 of 6. Each option below carries its own culinary application for that reason; an example borrowed from another property does not pay.")],
    "Seven properties in the scheme, best three taken, each kept with its own culinary-application line because the scheme pairs them and marks them together.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "'A foetus is dependent on its mother for nutrition; so pregnant women must eat healthily and safely.' (www.bordbia.ie)"
guide = semis(block(T, 'use of food pyramid for nutritional balance', '(b) Give an account of Folic Acid'))
cards.append(card(
    f'{P}-q2a', Y, L, 'home-economics-0-1', 'pregnancy-dietary-guidelines',
    '2024 HL Section B Q2(a)',
    'Discuss the dietary guidelines to follow when planning and preparing meals for a woman during pregnancy.',
    '5 dietary guidelines @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Discuss the dietary guidelines to follow when planning and preparing meals for a woman during pregnancy',
          20, 5, 4, guide[:14],
          "Five guidelines at 4 marks, graded 4:2:0 — named is 2, discussed is 4, nothing between. The scheme's list runs in two directions, include and avoid, and both count: the avoid side (pâté, soft ripened cheese, unpasteurised dairy, shellfish, undercooked meat) is about listeria and is the half students forget. A nutrient named without saying what it does for the pregnancy stays at 2.")],
    "The scheme prints far more than the 14 a card may show, so the list is taken in scheme order to the cap; the row stays openList, so any correct guideline still scores.",
    stem=Q2S))

fsrc = semis(block(T, 'wheat germ; wheat bran', '• biological functions'))
ffun = semis(block(T, 'red blood cell formation', '• properties.'))
fprop = semis(block(T, 'water soluble/insoluble in alcohol', '(c) Evaluate food labelling'))
cards.append(card(
    f'{P}-q2b', Y, L, 'home-economics-0-8', 'folic-acid',
    '2024 HL Section B Q2(b)',
    'Give an account of Folic Acid/Folate under each of the following headings: sources; biological functions; properties.',
    'sources 3 @ 2 marks (graded 2:0); biological functions 3 @ 2 marks (graded 2:1:0); properties 3 @ 2 marks (graded 2:0)',
    18,
    [anyN('r-1', 'Sources', 6, 3, 2, fsrc[:14],
          "Three sources at 2 marks, all-or-nothing (2:0). Nothing to describe — a correct food scores, a wrong one does not. Fortified cereals and supplements are on the list and are the two most often forgotten."),
     anyN('r-2', 'Biological functions', 6, 3, 2, ffun,
          "Three functions at 2 marks, and this one is graded 2:1:0 rather than 2:0 — the only strand of the three where a half-made point earns something. Neural tube defects is the function to lead with in a pregnancy question."),
     anyN('r-3', 'Properties', 6, 3, 2, fprop,
          "Three properties at 2 marks, all-or-nothing again. Properties are physical and chemical behaviour — solubility, heat stability, what destroys it — not what it does in the body. Mixing functions in here answers the previous bullet twice.")],
    "Three headings priced identically at 6 marks each. Worth showing the grading differences: two strands are all-or-nothing and the middle one is not.",
    stem=Q2S, tariff_kind='fixed'))

lab = semis(block(T, 'name of food; list of ingredients', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-1-2', 'food-labelling-dietary-requirements',
    '2024 HL Section B Q2(c)',
    'Evaluate food labelling as a source of consumer information when purchasing foods for individuals with specific dietary requirements.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Evaluate food labelling as a source of consumer information', 12, 3, 4, lab[:14],
          "Three points at 4 marks, graded 4:2:0. The question says \"for individuals with specific dietary requirements\", so the allergen points do the most work — declared allergens, printed in bold — followed by the quantity declarations someone on a restricted diet actually reads. Listing label contents earns 2; saying what that content lets a particular consumer decide earns 4.")],
    "The scheme prints one flat list of label contents, taken in order to the cap.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "'Artisan producers have altered Irish food culture to enrich our culinary heritage.' (Irish Examiner Jan. 2023)"
chg = semis(block(T, 'increased consumption of convenience foods', '(b) Outline the stages involved in the manufacture of yogurt'))
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-1', 'irish-eating-patterns',
    '2024 HL Section B Q3(a)',
    'Discuss the changes that have evolved in Irish food and eating patterns in recent years.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Discuss the changes that have evolved in Irish food and eating patterns in recent years',
          20, 5, 4, chg[:14],
          "Five changes at 4 marks, graded 4:2:0. The list is deliberately two-sided — convenience foods, salt, sugar and low fibre on one hand; wider choice, more nutritional knowledge and a focus on gut and mental health on the other — and an answer that runs only the decline story is telling half of it. Naming a change is 2; saying what drove it or what it costs is 4.")],
    "One flat list, taken in scheme order to the cap.",
    stem=Q3S))

yog = semis(block(T, 'milk is homogenised', '(c) Describe the protection provided to the consumer by the Food Hygiene'))
cards.append(card(
    f'{P}-q3b', Y, L, 'home-economics-0-9', 'yogurt-manufacture',
    '2024 HL Section B Q3(b)',
    'Outline the stages involved in the manufacture of yogurt. In your answer refer to production, packaging and labelling.',
    '10 points @ 2 marks (graded 2:1:0)', 20,
    [anyN('r-1', 'Outline the stages involved in the manufacture of yogurt', 20, 10, 2, yog,
          "Ten points at 2 marks — the highest point-count in Section B, and the one question where breadth beats depth outright. It is a sequence, and the temperatures are marking content: pasteurised at 80-90C, cooled to 37C for the culture, incubated 6-8 hours, cooled to 5C. A stage named without its temperature sits at 1. Packaging and labelling are named in the question and are the last two stages, so an account that stops at the finished yogurt leaves 4 marks behind.")],
    "One ordered process. Kept as a single group because every stage is priced the same and the order is what carries the meaning.",
    stem=Q3S))

fhr = semis(block(T, 'prohibits sale of food that is diseased', 'Question 4'))
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-4', 'food-hygiene-regulations',
    '2024 HL Section B Q3(c)',
    'Describe the protection provided to the consumer by the Food Hygiene Regulations 1950-1989.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Describe the protection provided to the consumer by the Food Hygiene Regulations 1950-1989',
          10, 2, 5, fhr,
          "Only two points, at 5 marks each, so both must be developed — this is not a list. Graded 5:3:0: naming a provision is 3 and describing what it means in a food premises is 5. The enforcement point (closure orders, unfit food seized and destroyed) is the strongest one to take, because it describes itself.")],
    "One flat list; each entry is already a full provision, which suits a 5-mark point.",
    stem=Q3S))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "'Helpful, knowledgeable staff are the driving force behind in-store shopping being popular amongst Irish consumers.' (www.pwc.ie)"
shop = semis(block(T, 'payment options; store loyalty cards', '(b) Name and evaluate two different methods of payment'))
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-2', 'consumer-shopping-patterns',
    '2024 HL Section B Q4(a)',
    'Analyse the changes in consumer shopping patterns over the last decade.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Analyse the changes in consumer shopping patterns over the last decade', 20, 5, 4, shop[:14],
          "Five changes at 4 marks, graded 4:2:0. \"Analyse\" is the difference between the 2 and the 4: self-service checkouts is a 2, and what they changed for the consumer and the retailer is the 4. The list splits into how people pay, how they shop, and what they value — spreading five points across all three reads better than five variations on technology.")],
    "One flat list, taken in scheme order to the cap.",
    stem=Q4S))

cpa = semis(block(T, 'false or misleading claims about goods', 'Question 5'))
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-2', 'consumer-protection-act-2007',
    '2024 HL Section B Q4(c)',
    'Describe the protection provided to the consumer by the Consumer Protection Act 2007.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Describe the protection provided to the consumer by the Consumer Protection Act 2007',
          12, 3, 4, cpa,
          "Three points at 4 marks, graded 4:2:0. The scheme's list is narrow and all of one shape — false or misleading claims about goods, services, price, previous price, recommended retail price — so the three points come from naming which claim, and the 4 comes from an example of what that misleading claim looks like in a shop.")],
    "One flat list. Short by design: this Act is examined on misleading claims rather than on redress, which belongs to the Sale of Goods Act.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "'The family is a dynamic, fluid, resilient and ever changing fundamental institution of society.' (Kristy Hawthorn)"
needs = heads(block(T, 'food parents to provide children', '(b) Analyse the impact of social'),
              ['food parents', 'clothing parents', 'shelter\nchildren' if 'shelter\nchildren' in T else 'shelter',
               'love affection', 'security and trust', 'praise and encouragement', 'protection from physical'])
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-0', 'family-child-needs',
    '2024 HL Section B Q5(a)',
    'Discuss the role of the family in meeting the physical and psychological needs of young children so that they will become well-adjusted adults in society.',
    '4 points @ 5 marks (graded 5:3:1:0); 1 point relating to physical, 1 point relating to psychological & 2 other points',
    20,
    [anyN('r-1', 'Discuss the role of the family in meeting the physical and psychological needs of young children',
          20, 4, 5, needs,
          "Four points at 5 marks on a 5:3:1:0 ladder, and the distribution is fixed: at least one physical need, at least one psychological, then two of either. Four points on food and clothing cannot score 20 because a psychological mark is reserved. The question ends \"so that they will become well-adjusted adults\", and that clause is what lifts a 3 to a 5 — say what the need does for the adult the child becomes.")],
    "Physical needs (food, clothing, shelter) and psychological needs (love, security and trust, praise, protection) as the scheme groups them, with the reservation carried in the notation.",
    stem=Q5S))

soc, eco, tech = heads(block(T, 'social decline in extended family', '(c) Describe two supports available'),
                       ['social decline', 'economic increased cost', 'technological automated'])
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-0', 'changes-family-structures',
    '2024 HL Section B Q5(b)',
    'Analyse the impact of social, economic and technological changes on contemporary family structures.',
    '3 points @ 6 marks (graded 6:4:2:0); 1 point relating to social, economic & technological changes',
    18,
    [anyN('r-1', 'Analyse the impact of social, economic and technological changes on contemporary family structures',
          18, 3, 6, [soc, eco, tech],
          "Three points at 6 marks, one from each of the three named strands — the distribution here is total, not partial: there is no free point, so an answer missing any one strand caps at 12. Graded 6:4:2:0, and \"analyse the impact\" is the whole ladder: the change itself is the 2, and what it did to family structure is the 6.")],
    "The question names the three strands and the scheme reserves a mark for each, so the strands are the options.",
    stem=Q5S, answer=3, of_parts=3, per_part=6))

sup = semis(block(T, 'family; neighbours; sheltered housing', None))
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-3', 'supports-older-family-members',
    '2024 HL Section B Q5(c)',
    'Describe two supports available to older family members and state how these supports help them to maintain their independence.',
    '2 points @ 6 marks (graded 6:4:2:0)', 12,
    [anyN('r-1', 'Describe two supports available to older family members and state how these supports help them to maintain their independence',
          12, 2, 6, sup,
          "Two supports at 6 marks each — a short answer where both points must be developed twice over, because the question asks for the support AND how it maintains independence. Naming Meals on Wheels is the 2; describing it is the 4; saying that it lets someone stay in their own home is the 6. The named services (Meals on Wheels, Age Action, public health nurses, Home Support Services) are worth more than the generic ones.")],
    "One flat list of supports; the independence half of the question is not a separate scheme list, so it lives in the contextNote as the thing the second half of each 6 pays for.",
    stem=Q5S))

emit(cards)
