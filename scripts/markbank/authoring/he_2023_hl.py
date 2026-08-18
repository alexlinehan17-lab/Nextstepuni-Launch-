#!/usr/bin/env python3
"""Home Economics 2023 Higher Level, Section B."""
import re, sys
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import *

Y, L, P = 2023, 'higher', 'he-2023-hl-sb'
T = load(Y, L)
T = T[[m.start() for m in re.finditer(r'Section B', T)][-1]:]
if 'Section C' in T:
    T = T[:T.index('Section C')]
cards = []

# ── Q1 ─────────────────────────────────────────────────────────────────────
Q1S = "Adequate micronutrient intakes during the teenage years is important for optimum growth and development. The chart gives the dietary sources of iron in a teenager's diet. (National Teen Food Survey II Report 2021, adapted from iuna.net)"
iron = heads(block(T, 'Breakfast cereals 22%', '(b) Identify and describe the factors'),
             ['Breakfast cereals 22%', 'Meat & meat products 20%', 'Bread & rolls 14%',
              'Grains, rice & pasta 10%', 'Vegetables & potatoes 9%', 'Confectionary 11%', 'Other 14%'])
cards.append(card(
    f'{P}-q1a', Y, L, 'home-economics-0-8', 'iron-sources-teenage-diet',
    '2023 HL Section B Q1(a)',
    'Using the information provided in the chart, comment and elaborate on the importance of including different sources of iron in a teenagers’ diet. Refer to four sources in your answer.',
    '4 points @ 5 marks (graded 5:4:3:2:1:0)', 20,
    [anyN('r-1', 'Comment and elaborate on the importance of including different sources of iron in a teenager’s diet',
          20, 4, 5, iron,
          "Four of the seven sources the chart plots, 5 marks each on a full 5-to-0 ladder — depth is paid a mark at a time, so four sources written well beats seven named. Two things run through the scheme's own text and are what \"elaborate\" means here: whether the iron is haem or non-haem, and what helps or blocks its absorption (Vitamin C helps, phytic acid in wholemeal hinders). The teenage angle matters too — menstruating girls and anaemia is the point the scheme returns to.")],
    "Seven sources on the chart, best four taken, each keeping its percentage and its own absorption detail.",
    stem=Q1S))

fe = semis(block(T, 'consuming haem iron and non-haem iron together', '(c) Give an account of Vitamin C'))
cards.append(card(
    f'{P}-q1b', Y, L, 'home-economics-0-8', 'iron-absorption-factors',
    '2023 HL Section B Q1(b)',
    'Identify and describe the factors that affect the absorption of iron in the body.',
    '4 factors @ 5 marks (graded 5:4:3:0)', 20,
    [anyN('r-1', 'Identify and describe the factors that affect the absorption of iron in the body', 20, 4, 5, fe,
          "Four factors at 5 marks on a 5:4:3:0 ladder — no 1 or 2, so any recognisable factor is worth at least 3 and the top two marks come from describing HOW it acts. The list runs both ways: the first three help absorption and the rest hinder it. Saying which direction a factor pulls is most of the description, and it is the half students leave out.")],
    "One flat list in the scheme, evenly priced. The helping and hindering factors are not separated by the scheme, so they are one group.",
    stem=Q1S))

vfun = semis(block(T, 'production of collagen; formation of healthy blood vessels', '• effects of deficiency'))
vdef = semis(block(T, 'collagen production affected', '• properties'))
vprop = semis(block(T, 'crystalline; acidic; sweet/sour taste', '(d) Discuss the guidelines a family'))
cards.append(card(
    f'{P}-q1c', Y, L, 'home-economics-0-8', 'vitamin-c-hl',
    '2023 HL Section B Q1(c)',
    'Give an account of Vitamin C with reference to: biological functions; effects of deficiency; properties.',
    'biological functions 4 points @ 3 marks (graded 3:0); effects of deficiency 2 points @ 2 marks (graded 2:0); properties 2 points @ 2 marks (graded 2:0)',
    20,
    [anyN('r-1', 'Biological functions', 12, 4, 3, vfun,
          "Four functions at 3 marks, all-or-nothing (3:0) — no partial credit anywhere on this part, which is unusual. Twelve of the twenty marks sit here, so this is where the time goes. Note two of the functions are about helping OTHER nutrients in (calcium and iron), which are easy marks students skip past."),
     anyN('r-2', 'Effects of deficiency', 4, 2, 2, vdef,
          "Two effects at 2 marks, all-or-nothing. Only 4 marks — scurvy plus one other and move on."),
     anyN('r-3', 'Properties', 4, 2, 2, vprop,
          "Two properties at 2 marks, all-or-nothing. Properties are how the vitamin behaves — water soluble, destroyed by light, air and alkalis — not what it does in the body. Reusing a function here answers the first bullet twice and scores nothing.")],
    "20 marks split 12 + 4 + 4 across the question's three bullets, and every strand is all-or-nothing. Worth seeing how lopsided it is: the functions are worth three times either of the others.",
    stem=Q1S, tariff_kind='fixed'))

budg = semis(block(T, 'fruit and vegetables in season, cheaper', 'Question 2'))
cards.append(card(
    f'{P}-q1d', Y, L, 'home-economics-1-1', 'shopping-restricted-budget',
    '2023 HL Section B Q1(d)',
    'Discuss the guidelines a family should follow, when doing their weekly shopping on a restricted budget, in order to provide for their nutritional needs.',
    '5 points @ 4 marks each (graded 4:2:0); refer to restricted budget and nutritional needs', 20,
    [anyN('r-1', 'Discuss the guidelines a family should follow when shopping on a restricted budget to provide for their nutritional needs',
          20, 5, 4, budg[:14],
          "Five guidelines at 4 marks, graded 4:2:0. The scheme adds a rubric line that decides the question: refer to restricted budget AND nutritional needs. A guideline that only saves money is half an answer — the 4 comes from tying the saving to the nutrition, which is why \"seasonal fruit and vegetables are cheaper and at their most nutritious\" is the model point.")],
    "The scheme prints more guidelines than a card may show, taken in order to the cap; the row stays openList so any correct guideline scores.",
    stem=Q1S))

# ── Q2 ─────────────────────────────────────────────────────────────────────
Q2S = "'Nutritional experts recommend 2-3 portions of fish each week for a balanced diet.' (www.goodfoodireland.ie)"
fish = heads(block(T, 'Protein (16-18%), HBV', '(b) Give a detailed account of one process'),
             ['Protein (16-18%)', 'Fat (0-18%)', 'Vitamins (1%)', 'Minerals (1%)', 'Water (65-80%)'])
cards.append(card(
    f'{P}-q2a', Y, L, 'home-economics-0-9', 'fish-nutritional-significance',
    '2023 HL Section B Q2(a)',
    'Discuss the nutritional significance of fish in the diet.',
    '5 points @ 4 marks (graded 4:3:2:1:0); nutrient 1, type 1, function/dietary 2', 20,
    [anyN('r-1', 'Discuss the nutritional significance of fish in the diet', 20, 5, 4, fish,
          "Five nutrients at 4 marks, and the scheme spells out how each 4 is built: 1 for the nutrient, 1 for its type, 2 for its function or dietary significance. That is the shape to write in — \"protein, HBV, supplies essential amino acids for growth\" is a full 4, where \"fish contains protein\" is a 1. The percentages are the scheme's own and are worth quoting.")],
    "Five nutrients, all five needed, each kept with its percentage, type and function because the 1+1+2 split is marked across them.",
    stem=Q2S))

fsai = semis(block(T, 'co-ordinates the enforcement of food safety regulation', 'Question 3'))
cards.append(card(
    f'{P}-q2c', Y, L, 'home-economics-0-4', 'fsai-role',
    '2023 HL Section B Q2(c)',
    'Describe the role of the Food Safety Authority of Ireland (FSAI) in the food industry.',
    '2 points @ 6 marks (graded 6:3:0)', 12,
    [anyN('r-1', 'Describe the role of the Food Safety Authority of Ireland (FSAI) in the food industry',
          12, 2, 6, fsai,
          "Two points at 6 marks each, graded 6:3:0 — half or full, nothing else, so a point either gets developed or loses three marks outright. With only two points wanted, take the two that describe themselves: the enforcement powers (improvement notices, closure orders) and the rapid-alert system.")],
    "One flat list; each entry is already a full function, which suits a 6-mark point.",
    stem=Q2S))

# ── Q3 ─────────────────────────────────────────────────────────────────────
Q3S = "'People are becoming more experimental in their culinary choices.' (www.bordbia.ie)"
fc = semis(block(T, 'culture; cost; sensory aspects', '(b) Profile an added value food'))
cards.append(card(
    f'{P}-q3a', Y, L, 'home-economics-0-10', 'family-food-choice-factors',
    '2023 HL Section B Q3(a)',
    'Discuss the factors that affect food choices for families today.',
    '3 points @ 4 marks (graded 4:2:0)', 12,
    [anyN('r-1', 'Discuss the factors that affect food choices for families today', 12, 3, 4, fc[:14],
          "Only three factors at 4 marks, so this is a short part — do not spend Section-B time on it. Graded 4:2:0: named is 2, discussed is 4. The sustainability, origins and ethics cluster is the most current thing on the list and the easiest to develop.")],
    "One flat list, taken in order to the cap.",
    stem=Q3S))

pca = heads(block(T, 'Name: humectants; sorbitol', 'Question 4'),
            ['Name: humectants', 'Name: emulsifiers', 'Name: anti-caking agents', 'Name: setting agent',
             'Name: stabilisers', 'Name: anti-spattering agents', 'Name: anti-foaming agents',
             'Name: firming agents', 'Name: buffers', 'Name: packaging gas'])
cards.append(card(
    f'{P}-q3c', Y, L, 'home-economics-0-11', 'physical-conditioning-agents',
    '2023 HL Section B Q3(c)',
    'Name and describe the role of one physical conditioning agent used in food processing.',
    'name 4 marks; role 2 points @ 4 marks (graded 4:0)', 12,
    [anyN('r-1', 'Name and describe the role of one physical conditioning agent used in food processing',
          12, 1, 12, pca,
          "One agent only, and the 12 marks split 4 for naming it and 4 + 4 for two points on its role — all graded 4:0, so every mark here is all-or-nothing. Each option carries the agent, its named chemicals and the foods it is used in, because the second role mark usually comes from the application. Naming the agent alone is a third of the marks; stopping there throws away eight.")],
    "Ten agents in the scheme, one chosen. Kept as a single 12-mark group because the naming mark and the two role marks are all won inside the one agent picked.",
    stem=Q3S, answer=1, of_parts=10, per_part=12))

# ── Q4 ─────────────────────────────────────────────────────────────────────
Q4S = "'Consumers must be constantly vigilant to protect themselves.' (www.thecai.ie)"
_m = heads(block(T, 'stages in the life cycle of the family arrival of children', '(b) Analyse how different techniques'),
           ['stages in the life cycle', 'employment patterns dual', 'values sustainability'])
# Individual points, taken evenly from each factor so none is truncated away:
# the scheme reserves a mark for each, so all three must stay visible.
mgmt = (semis(_m[0], drop_prefix='stages in the life cycle of the family')[:5]
        + semis(_m[1], drop_prefix='employment patterns')[:5]
        + semis(_m[2], drop_prefix='values')[:4])
cards.append(card(
    f'{P}-q4a', Y, L, 'home-economics-1-0', 'home-management-factors',
    '2023 HL Section B Q4(a)',
    'Discuss how the following factors affect the management of the home: stages in the life cycle of the family; employment patterns; values.',
    '4 points @ 5 marks (graded 5:3:0); one point on each factor plus one other', 20,
    [anyN('r-1', 'Discuss how the life cycle of the family, employment patterns and values affect the management of the home',
          20, 4, 5, mgmt,
          "Four points at 5 marks with a reserved mark on each of the three named factors, plus one free. Values is the thinnest list in the scheme and the one most often skipped — but a mark is held for it, so an answer covering only family stage and employment caps at 15 of 20.")],
    "The options are the individual points, taken evenly across the three factors the question names so that none is squeezed out by the option cap. The reserved mark on each factor is carried in the notation and the contextNote.",
    stem=Q4S))

ret = heads(block(T, 'shop layout size influences', '(c) Describe how the responsibilities of a consumer'),
            ['shop layout', 'in-store stimuli', 'product placement', 'shelf position',
             'pricing multiple buys', 'online shopping suggestions', 'loyalty cards'])
cards.append(card(
    f'{P}-q4b', Y, L, 'home-economics-1-2', 'retailer-techniques',
    '2023 HL Section B Q4(b)',
    'Analyse how different techniques used by retailers influence consumer spending.',
    '4 points @ 5 marks (graded 5:3:0); max of 2 points under each technique', 20,
    [anyN('r-1', 'Analyse how different techniques used by retailers influence consumer spending', 20, 4, 5, ret,
          "Four points at 5 marks, with a cap the scheme states outright: a maximum of 2 points under any one technique. So four points on shelf position cannot score 20 — at least two different techniques are required. \"Analyse\" wants the mechanism: essentials at the back of the store is a 3, and walking a shopper past everything else to reach the milk is the 5.")],
    "Seven techniques in the scheme; the two-per-technique cap is carried in the notation because the card model cannot enforce it.",
    stem=Q4S))

resp = semis(block(T, 'know their rights; educate themselves', 'Question 5'))
cards.append(card(
    f'{P}-q4c', Y, L, 'home-economics-1-2', 'consumer-responsibilities',
    '2023 HL Section B Q4(c)',
    'Describe how the responsibilities of a consumer can assist them in making wise choices.',
    '2 points @ 5 marks (graded 5:3:0)', 10,
    [anyN('r-1', 'Describe how the responsibilities of a consumer can assist them in making wise choices',
          10, 2, 5, resp,
          "Two points at 5 marks. Note the question is about RESPONSIBILITIES, not rights — knowing your rights is itself a responsibility here, but listing the rights is answering a different question. The 5 comes from the second half of the question: how the responsibility leads to a better choice.")],
    "One flat list, evenly priced.",
    stem=Q4S))

# ── Q5 ─────────────────────────────────────────────────────────────────────
Q5S = "The family is an integral social institution in society."
chg = semis(block(T, 'family structure; location; parental roles', '(b) Explain the following sociological terms'))
cards.append(card(
    f'{P}-q5a', Y, L, 'home-economics-2-0', 'family-change-since-1950s',
    '2023 HL Section B Q5(a)',
    'Discuss the changes that have taken place in the family from the middle of the twentieth century to the present day.',
    '5 points @ 4 marks (graded 4:2:0)', 20,
    [anyN('r-1', 'Discuss the changes that have taken place in the family from the middle of the twentieth century to the present day',
          20, 5, 4, chg,
          "Five changes at 4 marks, graded 4:2:0. The scheme gives headings only, so the 2 is nearly automatic and the other 2 comes entirely from tracking the change across the period — each point needs a then and a now. An accurate description of the family today, with no movement in it, scores 10.")],
    "Bare headings in the scheme, kept as printed: the marks come from developing them, not from listing more.",
    stem=Q5S))

soc = heads(block(T, 'universality of the family family is present', '(c) Describe one legal option'),
            ['universality of the family', 'kinship relationships', 'monogamy relationship'])
cards.append(card(
    f'{P}-q5b', Y, L, 'home-economics-2-0', 'sociological-terms',
    '2023 HL Section B Q5(b)',
    'Explain the following sociological terms: universality of the family; kinship; monogamy.',
    '3 points @ 5 marks (graded 5:3:0)', 15,
    [anyN(f'r-{i+1}', name, 5, 1, 5, [soc[i]], note) for i, (name, note) in enumerate([
        ('Universality of the family', "One term, 5 marks, graded 5:3:0. All three are compulsory, so this is three short definitions rather than a choice. The 5 here needs both halves the scheme gives: the family exists in virtually every known society AND the form it takes varies between them."),
        ('Kinship', "One term, 5 marks. The scheme accepts a cluster of near-synonyms — family ties, blood relationships, common ancestry — so give two of them rather than one bare word."),
        ('Monogamy', "One term, 5 marks for a single-clause definition: a relationship with only one partner at a time. The phrase \"at a time\" is doing real work; leaving it out defines something else."),
    ])],
    "Three compulsory terms at 5 marks each, so three rows rather than a pooled choice.",
    stem=Q5S, tariff_kind='fixed'))

legal = heads(block(T, 'deed of separation arrangement agreed', None),
              ['deed of separation', 'judicial separation granted', 'legal nullity partners', 'divorce spouse wishing'])
cards.append(card(
    f'{P}-q5c', Y, L, 'home-economics-2-1', 'marriage-breakdown-legal-options',
    '2023 HL Section B Q5(c)',
    'Describe one legal option available in Ireland to couples when their marriage has broken down.',
    'name 1 point @ 3 marks (graded 3:2:0); description 3 points @ 4 marks (graded 4:2:0)', 15,
    [anyN('r-1', 'Describe one legal option available in Ireland to couples when their marriage has broken down',
          15, 1, 15, legal,
          "ONE option only, worth 15 marks: 3 for naming it and 3 points at 4 for describing it. Describing two options wastes half the answer. Each option carries its own conditions and they are not interchangeable — the two-of-the-previous-three-years living apart belongs to divorce, the one-year and three-year grounds to judicial separation. Those time periods are marking content; a description without them will not reach 4 a point.")],
    "Four options in the scheme, one chosen, each kept whole because its conditions belong to it. The naming mark is carried in the notation.",
    stem=Q5S, answer=1, of_parts=4, per_part=15))

emit(cards)
