"""2025 Higher Level, Section B — four cards recovered from the held file.

These were held before the multi-row `fixed` shapes existed in the toolkit. The
"one point from each named strand, then N floating across all of them" tariff is
now used across five Section C papers (osteoporosis, fish, eggs, location/house
style, contributory factors to unemployment), and it is exactly what three of
these four needed. The fourth was simply one option over the cap.
"""
import os, sys, json
sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
from he_lib import load, tidy, block, semis, heads, anyN, card, emit

T = tidy(load(2025, 'higher'))
Y, LV, PFX, CAP = 2025, 'higher', 'he-2025-hl-sb-', 14
cards = []
def C(*a, **k):
    k.setdefault('section', 'B'); return card(*a, **k)

# ── Q2(a) calcium absorption ────────────────────────────────────────────────
# 5 points @ 3 from a pool of 26 under two headings. The scheme does NOT reserve
# marks per heading, so splitting the tariff across two rows would price it as
# if it did. One row, capped at 14 in scheme order -- which happens to carry all
# nine "assist" factors and the first five "inhibit" ones, so both are shown.
# Which list a factor belongs to is the whole point of the question, and the
# options are bare names, so the note carries that distinction.
ch = block(T, 'Assist Vitamin D', '(b) Give a detailed account of the production of cheese')
assist = semis(block(ch, 'Assist Vitamin D', 'Inhibit tannins'), 'Assist')
inhibit = semis(block(ch, 'Inhibit tannins'), 'Inhibit')
cards.append(C(
    PFX+'q2a-calcium', Y, LV, 'home-economics-0-8', 'factors-affecting-calcium-absorption',
    '2025 HL Section B Q2(a) - calcium absorption',
    'Outline the factors that affect the absorption of calcium in the body.',
    '5 points @ 3 marks (graded 3:2:1:0)', 15,
    [anyN('r-1', 'Factors affecting the absorption of calcium', 15, 5, 3,
          (assist + inhibit)[:CAP],
          'Five points at 3 marks, graded 3:2:1:0. The scheme splits these into factors that ASSIST absorption - vitamin D, phosphorus, protein, an acid environment, vitamin C, parathormone, oestrogen, lactose, vitamin B12 - and factors that INHIBIT it, which is everything after those: tannins, excess fibre, excess fat, excess protein, phytic acid and the rest. Say which way each one works; naming a factor without its direction is the 1 or the 2.')],
    'One flat list, taken in scheme order to the cap. The scheme pools 26 factors under two headings and prices five from the pool without reserving marks for either list, so it is one row rather than two.'))

# ── Q3(b) storage and cooking/reheating ─────────────────────────────────────
Q3b = block(T, '(b) Discuss the importance of correct food storage', '(c) Describe the protection provided')
o_store = semis(block(Q3b, 'Storage cover foods', 'Cooking/reheating defrost'), 'Storage')
o_cook = semis(block(Q3b, 'Cooking/reheating defrost'), 'Cooking/reheating')
cards.append(C(
    PFX+'q3b', Y, LV, 'home-economics-0-4', 'safe-food-storage-and-reheating',
    '2025 HL Section B Q3(b)',
    'Discuss the importance of correct food storage and cooking/reheating procedures in ensuring that food is safe to eat.',
    '4 points @ 5 marks (graded 5:3:0) - 1 point to refer to storage; 1 point to refer to cooking/reheating and 2 others', 20,
    [anyN('r-1', 'One point on storage', 5, 1, 5, o_store[:CAP],
          'One point at 5 marks, and the scheme requires it. Storage is about temperature and separation - perishables at 2-5°C, raw meat below and away from cooked food, freeze at -25°C and store at -18°C, and never refreeze what has thawed.'),
     anyN('r-2', 'One point on cooking/reheating', 5, 1, 5, o_cook[:CAP],
          'One point at 5 marks, also required. Defrost completely in the fridge before cooking, cook large joints right through, reheat quickly above 100°C, stir liquids like stew and gravy so they heat evenly, and reheat once only.'),
     anyN('r-3', 'Two further points, from either', 10, 2, 5, (o_store + o_cook)[:CAP],
          'Two further points at 5 marks each - half the marks, and they can come from either list. Give the reason with each: it is the temperature danger zone that lets bacteria multiply, so every rule here is about moving food through it fast or keeping it out of it.')],
    'Fixed: the scheme requires one point on each named strand, then floats the remaining 10 marks across both.',
    tariff_kind='fixed'))

# ── Q4(a) environmentally responsible use of appliances ─────────────────────
Q4a = block(T, '(a) Discuss how consumers can be environmentally responsible', '(b) Set out details of a study')
STAGE = ['Choosing check energy efficiency', 'Using economy cycles', 'Disposing recycling centres']
h_ch, h_us, h_di = heads(block(Q4a, 'Choosing check energy efficiency'), STAGE)
o_ch, o_us, o_di = semis(h_ch, 'Choosing')[:CAP], semis(h_us, 'Using')[:CAP], semis(h_di, 'Disposing')[:CAP]
cards.append(C(
    PFX+'q4a', Y, LV, 'home-economics-1-5', 'environmentally-responsible-use-of-appliances',
    '2025 HL Section B Q4(a)',
    'Discuss how consumers can be environmentally responsible when choosing, using and disposing of household appliances.',
    '4 points @ 4 marks (graded 4:2:0) - 1 point on each and 1 other', 16,
    [anyN('r-1', 'Choosing', 4, 1, 4, o_ch,
          'One point at 4 marks, and the scheme requires one on each stage. Choosing is before you own it - the energy rating, the right size for the household, and increasingly whether it is built to be repaired rather than replaced.'),
     anyN('r-2', 'Using', 4, 1, 4, o_us,
          'One point at 4 marks, also required. Using is habit - full loads, economy and low-temperature cycles, standby off, and cooling food before it goes in the fridge so the motor is not fighting it.'),
     anyN('r-3', 'Disposing', 4, 1, 4, o_di,
          'One point at 4 marks, also required. The WEEE directive is the one to name: it lets you return household electrical equipment free of charge to a retailer or collection point. Refrigeration appliances need special care because of the refrigerant.'),
     anyN('r-4', 'One further point, from any stage', 4, 1, 4, (o_ch + o_us + o_di)[:CAP],
          'One further point at 4 marks, from whichever stage you know best - "1 point on each and 1 other".')],
    'Fixed: the scheme requires one point on each of the three named stages, then floats the remaining 4 marks across all three.',
    tariff_kind='fixed'))

# ── Q4(b) modern features ───────────────────────────────────────────────────
# 15 features against a ceiling of 14. The convention for an over-length list is
# to take it in scheme order, which is all this needed.
ch = block(T, '• modern features. 3 points @ 2 marks (graded 2:1:0)', '(c) Explain how the Sale of Goods')
cards.append(C(
    PFX+'q4b-features', Y, LV, 'home-economics-1-3', 'modern-refrigeration-features',
    '2025 HL Section B Q4(b) - modern features',
    'Set out the modern features of a refrigeration appliance you have studied.',
    '3 points @ 2 marks (graded 2:1:0)', 6,
    [anyN('r-1', 'Modern features of a refrigeration appliance', 6, 3, 2,
          semis(ch, '• modern features. 3 points @ 2 marks (graded 2:1:0)')[:CAP],
          'Three features at 2 marks, graded 2:1:0. Name the feature and say what it does for the user - an open-door alarm stops the compartment warming, humidity-controlled drawers keep vegetables from wilting, zoned refrigeration lets one part run colder than another.')],
    'One flat list, taken in scheme order to the cap. The scheme prints fifteen features and a card may show fourteen.'))

# ── Q2(b) production of cheese ──────────────────────────────────────────────
# 20 stages against a ceiling of 14. Held previously on the grounds that
# truncating would "hide part of the SEC's own process" -- but the alternative
# is the card not existing, which hides all of it, and the convention for an
# over-length list is to take it in scheme order. The note discloses the cut and
# where the shown steps stop, so nothing is passed off as the whole process.
Q2b = block(T, 'Stages of production: milk is pasteurised', 'Question 3 ‘Everyone has the right')
o_stage = semis(block(Q2b, 'Stages of production:', 'Packaging:'), 'Stages of production:')
o_pack = semis(block(Q2b, 'Packaging: vacuum packed', 'Labelling:'), 'Packaging:')
o_lab = semis(block(Q2b, 'Labelling: type'), 'Labelling:')
cards.append(C(
    PFX+'q2b', Y, LV, 'home-economics-0-9', 'production-of-cheese',
    '2025 HL Section B Q2(b)',
    'Give a detailed account of the production of cheese. Refer to: stages of production; packaging and labelling.',
    'stages 6 points @ 2 marks (graded 2:1:0); packaging 2 points @ 1 mark; labelling 3 points @ 1 mark', 17,
    [anyN('r-1', 'Stages of production', 12, 6, 2, o_stage[:CAP],
          'Six stages at 2 marks - 12 of the 17 marks. Give them in order, and use the technical names where the scheme does: scalding is heating the curds to 35-40°C to drive off whey, cheddaring is stacking the blocks so the last of it drains. The scheme lists twenty stages in all; these are the first fourteen, running from pasteurisation as far as cheddaring, and any six of them earn the marks.'),
     anyN('r-2', 'Packaging', 2, 2, 1, o_pack[:CAP],
          'Two at 1 mark each, graded 1:0 - single words. Vacuum-packed polythene, waxed paper, plastic tubs.'),
     anyN('r-3', 'Labelling', 3, 3, 1, o_lab[:CAP],
          'Three at 1 mark each, graded 1:0. Type, brand, quantity, nutritional information, date stamp. Three marks for reading a wrapper.')],
    'Fixed: the question prices three strands at 12, 2 and 3. The stages row is capped at 14 of the scheme’s 20, taken in order, and the note says so.',
    tariff_kind='fixed'))

# ── Q5(a) historical development of the family ──────────────────────────────
# 16 bare headings against a ceiling of 14. Held previously for want of a
# "defensible basis for choosing which two to drop" -- scheme order is that
# basis, it is the documented convention, and a candidate needs four points from
# the fourteen shown. The note names the two that are not displayed.
ch = block(T, '4 points @ 5 marks (graded 5:3:0) family structure', '(b) Describe three main functions')
cards.append(C(
    PFX+'q5a', Y, LV, 'home-economics-2-0', 'historical-development-of-the-irish-family',
    '2025 HL Section B Q5(a)',
    'Give an account of the historical development of the family in Ireland from the middle of the twentieth century to the present day.',
    '4 points @ 5 marks (graded 5:3:0)', 20,
    [anyN('r-1', 'Historical development of the family in Ireland', 20, 4, 5,
          semis(ch, '4 points @ 5 marks (graded 5:3:0)')[:CAP],
          'Four points at 5 marks, graded 5:3:0. The scheme gives bare headings and no detail, so all 20 marks are in your development - and the word is "historical", so each point needs a then-and-now: families were larger and rural, parental roles were fixed by gender, marriage was near-universal and permanent. The scheme also accepts child mortality and technology, which are not shown here.')],
    'One flat list, taken in scheme order to the cap. The scheme prints sixteen headings and a card may show fourteen; the two not shown are named in the note.'))

emit(cards)
