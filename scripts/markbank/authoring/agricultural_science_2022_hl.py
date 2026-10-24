"""2022 Higher review: the 96 original cards reconciled against the SEC sources.

All 44 paper pages and 35 scheme pages were inspected and the independent
census transcribed before any card was touched. 101 base tasks, one card each
(Q1(b)(iii) and (iv), the tick and its justification, stay one task). 89
original card objects match a published task boundary and tariff and are left
byte-identical; they only gain an Atlas binding and an inspected official
source page. Seven originals are corrected IN PLACE, keeping their IDs:
Q16(c)(i) regains its published 11 marks (named system 2, drawing 6/3/0,
labels 3(1)) where the card priced the name alone at 3; Q2(b) lists every
characteristic in the scheme's two-page table; Q10(b), Q10(c) and Q15(a)(i)
carry each crop or animal the scheme answers for as its own answer route;
Q17(a)(i) carries its banded drawing criteria; Q17(b)(ii) regains the end of a
truncated definition. Cards are added for the missing Q9(a)(i), Q13(a)(iv),
Q13(b)(iii), Q14(c)(ii) and Q18(b)(ii). Each correction records the original
wording, marks and object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024ALP000EV.pdf'
YEAR = 2022
HASHES = {'exampapers':'690cca40b2798863c397126cac71dc076d4fd3d6cb38395fee63c57625dc8f7f',
          'markingschemes':'9e868b6c11ecf6bf71da03b8ced52b3be4aa80bbacb205b5fd418b555abd1a40'}
KEPT_ONE_CARD = ' The original one-card form already lets any printed choice score, so it is kept unchanged (item-choice siblings are not separate practice identities).'
SELECTIONS = {
    'b2cb14d3a9c56565':('exam-selection','Instructions: Section A, seven of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'dd29dfd56ce26f9b':('exam-selection','Instructions: Section B, three of six independent questions. Every question is retained.'),
    'e934ac6fd6827f33':('exam-selection','Repeated Section A instruction: seven independent 10-mark questions, all retained.'),
    '7163b93debada842':('independent-task-selection','Q1 either (a) or (b): both independently marked alternatives are retained.'),
    'ecc57706a12a1182':('closed','Q2(a): identify any four of six photographed breeds A–F, 4(1).' + KEPT_ONE_CARD),
    '40bc0418d913b508':('not-a-selection','"to select a female replacement animal" in the Q2(b) stem is the farmer\'s task, not a response choice.'),
    '394cec5f2f0e9a36':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    '8755fac1ea415f47':('not-a-selection','Prose in the Q9(b) article ("one of the biggest challenges"); no response choice.'),
    '393f1b1bde32d98d':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    'b6077383f474cd46':('independent-task-selection','Q12 either (a) or (b): both alternatives are retained.'),
    '2907202d35ecc76e':('exam-selection','Section B heading: three of six independent 50-mark questions, all retained.'),
    '1bd4570cfafa77cc':('closed','Q13(a)(iii): identify any two of three photographed plants A, B and C, 2(1).' + KEPT_ONE_CARD),
    '0b8805db948e5e79':('independent-task-selection','Q14: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '33e063a1cca92586':('not-a-selection','Prose in Q14(a)(v) ("one of her freshly calved cows"); no response choice.'),
    '2edd172b7c28c2ba':('independent-task-selection','Q17: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '9c490ba4828a71cd':('not-a-selection','"why scientists select the plants" in Q17(b)(i) is breeding vocabulary, not a response choice.'),
}
SUPPLEMENTARY = [
    (5,'A farmer was looking to select a female replacement animal','open','Q2(b): a student-named enterprise; the scheme\'s two-page characteristics table is a marking menu.'),
    (14,'In relation to a named catch or energy crop you have studied','closed','Q10(b) and Q10(c): a student-named crop; the scheme answers for kale, Miscanthus and oilseed rape, kept as answer routes on one card each.'),
    (27,'Describe how this is carried out for a named','closed','Q15(a)(i): a student-named animal; the scheme answers for ewes, heifers or cows (three protocols) and sows, kept as answer routes on one card.'),
    (31,'Describe using a labelled diagram a named grazing system','open','Q16(c)(i): any named grazing system; the scheme lists paddock, block, strip and spokes of a wheel and excludes zero grazing.'),
    (38,'a named livestock or tillage enterprise','closed','Q18(a)(ii): livestock or tillage enterprise; the scheme marks the two with different points, kept as mutually exclusive row routes on one card.'),
    (4,'by placing a tick','answer-identification','Q1(b)(iii): one correct box (spring, overcast and misty).'),
    (14,'Identify the type of lifecycle which best describes your chosen crop','answer-identification','Q10(a): the lifecycle of the crop named.'),
    (35,'State with reason which variety would suit the diet','answer-identification','Q17(c)(i): one correct variety (Bazooka) with a reason.'),
]
TOPIC = 'agricultural-science-higher-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2022-hl-'
RESTORED = []

P = lambda *r: [region(*x) for x in r]
REGIONS = {
    'Q1(a)(i)': (P((3, .158, .35)), P((12, .137, .217))),
    'Q1(a)(ii)': (P((3, .158, .226), (3, .35, .374)), P((12, .217, .452))),
    'Q1(a)(iii)': (P((3, .158, .226), (3, .474, .498)), P((12, .452, .615))),
    'Q1(b)(i)': (P((4, .065, .115)), P((12, .615, .782))),
    'Q1(b)(ii)': (P((4, .305, .33)), P((12, .782, .843))),
    'Q1(b)(iii)–(iv)': (P((4, .459, .645)), P((12, .843, .9), (13, .085, .217))),
    'Q2(a)': (P((5, .065, .56)), P((13, .217, .348))),
    'Q2(b)': (P((5, .56, .662)), P((13, .348, .431), (14, .1, .87), (15, .1, .445))),
    'Q3(a)': (P((6, .065, .15)), P((16, .085, .253))),
    'Q3(b)': (P((6, .065, .13), (6, .52, .545)), P((16, .253, .302))),
    'Q3(c)': (P((6, .065, .13), (6, .644, .702)), P((16, .302, .435))),
    'Q4(a)': (P((7, .065, .315)), P((16, .435, .484))),
    'Q4(b)': (P((7, .065, .27), (7, .384, .408)), P((16, .484, .619))),
    'Q4(c)': (P((7, .065, .27), (7, .478, .52)), P((16, .619, .9), (17, .07, .32))),
    'Q5(a)': (P((8, .065, .155)), P((17, .32, .436))),
    'Q5(b)(i)': (P((8, .065, .13), (8, .286, .566)), P((17, .436, .485))),
    'Q5(b)(ii)': (P((8, .065, .13), (8, .286, .54), (8, .606, .63)), P((17, .485, .76))),
    'Q6(a)': (P((9, .065, .172)), P((18, .085, .271))),
    'Q6(b)': (P((9, .453, .495)), P((18, .271, .389))),
    'Q6(c)': (P((9, .625, .735)), P((18, .389, .522))),
    'Q7(a)': (P((10, .065, .643)), P((18, .522, .605))),
    'Q7(b)': (P((10, .065, .19), (10, .478, .667)), P((18, .605, .688))),
    'Q7(c)': (P((10, .065, .19), (10, .756, .78)), P((18, .688, .775))),
    'Q8(a)(i)': (P((11, .065, .47)), P((19, .085, .226))),
    'Q8(a)(ii)': (P((11, .065, .35), (11, .47, .585)), P((19, .226, .401))),
    'Q8(b)': (P((11, .065, .35), (11, .592, .632)), P((19, .401, .645))),
    'Q9(a)(i)': (P((12, .065, .115)), P((20, .085, .21))),
    'Q9(a)(ii)': (P((12, .065, .115), (12, .645, .67)), P((20, .21, .362))),
    'Q9(b)(i)': (P((13, .065, .38)), P((20, .362, .481))),
    'Q9(b)(ii)': (P((13, .09, .335), (13, .561, .6)), P((20, .481, .651))),
    'Q9(b)(iii)': (P((13, .09, .335), (13, .729, .786)), P((20, .651, .72))),
    'Q10(a)': (P((14, .065, .29)), P((21, .085, .151))),
    'Q10(b)': (P((14, .065, .14), (14, .305, .33)), P((21, .151, .602))),
    'Q10(c)': (P((14, .065, .14), (14, .58, .605)), P((21, .602, .885))),
    'Q11(a)(i)': (P((15, .065, .2)), P((22, .085, .131))),
    'Q11(a)(ii)': (P((15, .09, .2), (15, .203, .228)), P((22, .131, .231))),
    'Q11(a)(iii)': (P((15, .324, .348)), P((22, .231, .294))),
    'Q11(b)(i)': (P((15, .466, .545, 0, .64)), P((22, .294, .339))),
    'Q11(b)(ii)': (P((15, .466, .521, 0, .64), (15, .605, .645, 0, .64)), P((22, .339, .383))),
    'Q11(b)(iii)': (P((15, .466, .521, 0, .64), (15, .682, .706)), P((22, .383, .463))),
    'Q11(b)(iv)': (P((15, .466, .521, 0, .64), (15, .8, .824)), P((22, .463, .545))),
    'Q12(a)(i)': (P((16, .065, .352)), P((23, .085, .147))),
    'Q12(a)(ii)': (P((16, .065, .33), (16, .454, .476)), P((23, .147, .263))),
    'Q12(a)(iii)': (P((16, .065, .33), (16, .642, .68)), P((23, .263, .45))),
    'Q12(b)(i)': (P((17, .065, .297)), P((23, .45, .529))),
    'Q12(b)(ii)': (P((17, .065, .27), (17, .367, .39)), P((23, .529, .609))),
    'Q12(b)(iii)': (P((17, .065, .27), (17, .491, .515)), P((23, .609, .688))),
    'Q12(b)(iv)': (P((17, .065, .27), (17, .646, .67)), P((23, .688, .77))),
    'Q13(a)(i)': (P((20, .158, .268)), P((24, .14, .273))),
    'Q13(a)(ii)': (P((20, .185, .24), (20, .397, .59)), P((24, .273, .352))),
    'Q13(a)(iii)': (P((20, .185, .24), (20, .59, .835)), P((24, .352, .432))),
    'Q13(a)(iv)': (P((20, .59, .835), (21, .065, .11)), P((24, .432, .548))),
    'Q13(b)(i)': (P((21, .237, .29)), P((24, .548, .662))),
    'Q13(b)(ii)': (P((21, .237, .262), (21, .566, .64)), P((24, .662, .89))),
    'Q13(b)(iii)': (P((21, .237, .262), (22, .065, .135)), P((25, .085, .279))),
    'Q13(b)(iv)': (P((21, .237, .262), (22, .376, .42)), P((25, .279, .43))),
    'Q14(a)(i)': (P((23, .065, .09), (23, .095, .135, 0, .6)), P((25, .43, .547))),
    'Q14(a)(ii)': (P((23, .44, .465)), P((25, .547, .63))),
    'Q14(a)(iii)': (P((23, .567, .61)), P((25, .63, .695))),
    'Q14(a)(iv)': (P((23, .713, .737)), P((25, .695, .778))),
    'Q14(a)(v)': (P((24, .065, .30)), P((25, .778, .915))),
    'Q14(b)(i)': (P((24, .397, .635)), P((26, .085, .178))),
    'Q14(b)(ii)': (P((24, .397, .595), (24, .728, .752)), P((26, .178, .313))),
    'Q14(c)(i)': (P((25, .065, .335)), P((26, .313, .431))),
    'Q14(c)(ii)': (P((25, .065, .09), (25, .535, .897)), P((26, .431, .69))),
    'Q14(d)(i)': (P((26, .09, .36)), P((26, .69, .755))),
    'Q14(d)(ii)': (P((26, .09, .31), (26, .465, .51)), P((26, .755, .855))),
    'Q14(d)(iii)': (P((26, .09, .15), (26, .61, .635)), P((27, .085, .234))),
    'Q15(a)(i)': (P((27, .065, .165)), P((27, .234, .697))),
    'Q15(a)(ii)': (P((27, .363, .405)), P((27, .697, .792))),
    'Q15(a)(iii)': (P((27, .509, .59)), P((27, .792, .905))),
    'Q15(b)(i)': (P((28, .065, .475)), P((28, .085, .17))),
    'Q15(b)(ii)': (P((28, .065, .42), (28, .6, .625)), P((28, .17, .231))),
    'Q15(b)(iii)': (P((28, .065, .42), (28, .724, .79)), P((28, .231, .316))),
    'Q15(b)(iv)': (P((28, .065, .42), (29, .065, .09)), P((28, .316, .43))),
    'Q15(c)(i)': (P((29, .283, .47)), P((28, .43, .492))),
    'Q15(c)(ii)': (P((29, .283, .325), (29, .572, .615)), P((28, .492, .673))),
    'Q16(a)(i)': (P((30, .065, .40)), P((28, .673, .792))),
    'Q16(a)(ii)': (P((30, .065, .31), (30, .406, .43)), P((28, .792, .865))),
    'Q16(a)(iii)': (P((30, .065, .31), (30, .529, .553)), P((29, .085, .149))),
    'Q16(b)(i)': (P((30, .645, .812)), P((29, .149, .199))),
    'Q16(b)(ii)': (P((30, .645, .79), (31, .065, .11)), P((29, .199, .28))),
    'Q16(b)(iii)': (P((31, .241, .29)), P((29, .28, .433))),
    'Q16(c)(i)': (P((31, .387, .465)), P((29, .433, .619))),
    'Q16(c)(ii)': (P((32, .065, .11)), P((29, .619, .845))),
    'Q17(a)(i)': (P((33, .065, .14)), P((30, .085, .208))),
    'Q17(a)(ii)': (P((33, .09, .115), (33, .588, .63)), P((30, .208, .338))),
    'Q17(a)(iii)': (P((34, .065, .335)), P((30, .338, .522))),
    'Q17(a)(iv)': (P((34, .065, .335), (34, .395, .42)), P((30, .522, .566))),
    'Q17(b)(i)': (P((34, .491, .75)), P((30, .566, .628))),
    'Q17(b)(ii)': (P((34, .491, .55), (35, .065, .11)), P((30, .628, .708))),
    'Q17(c)(i)': (P((35, .288, .475)), P((30, .708, .774))),
    'Q17(c)(ii)': (P((35, .288, .355), (35, .576, .62)), P((30, .774, .89))),
    'Q17(d)(i)': (P((36, .065, .33)), P((31, .085, .2))),
    'Q17(d)(ii)': (P((36, .065, .30), (36, .522, .565)), P((31, .2, .363))),
    'Q18(a)(i)': (P((37, .065, .48)), P((31, .363, .655))),
    'Q18(a)(ii)': (P((38, .065, .16)), P((31, .655, .9), (32, .085, .145))),
    'Q18(b)(i)': (P((38, .329, .785)), P((32, .145, .228))),
    'Q18(b)(ii)': (P((38, .329, .75), (39, .065, .12)), P((32, .228, .76))),
    'Q18(c)(i)': (P((40, .065, .43)), P((33, .085, .222))),
    'Q18(c)(ii)': (P((40, .065, .39), (40, .571, .615)), P((33, .222, .33))),
}
ATLAS = {
    'Q1(a)': 'soil-science', 'Q1(b)': 'fertilisers-pollution-environment-cycles|soil-science',
    'Q2(a)': 'classification-of-animals-plants', 'Q2(b)': 'genetics|animal-physiology-reproductive-systems',
    'Q3': 'crop-production|scientific-practices-experiments-investigations', 'Q4': 'animal-diseases', 'Q5': 'pigs',
    'Q6': 'fertilisers-pollution-environment-cycles', 'Q6(c)': 'genetics', 'Q7': 'beef-cattle',
    'Q8(a)(i)': 'crop-production|fertilisers-pollution-environment-cycles', 'Q8(a)(ii)': 'animal-diseases',
    'Q8(b)': 'fertilisers-pollution-environment-cycles', 'Q9(a)': 'animal-physiology-digestive-system|dairy-cattle',
    'Q9(b)': 'animal-physiology-digestive-system|innovation-and-biotechnology-in-agriculture', 'Q10': 'energy-crop-catch-crop',
    'Q11': 'plant-physiology|soil-science', 'Q12': 'grassland', 'Q13(a)': 'grassland',
    'Q13(a)(iii)': 'grassland|classification-of-animals-plants', 'Q13(a)(iv)': 'grassland|plant-physiology',
    'Q13(b)': 'grassland|scientific-practices-experiments-investigations', 'Q14': 'dairy-cattle',
    'Q14(d)': 'sheep|animal-diseases', 'Q15(a)': 'animal-physiology-reproductive-systems|genetics',
    'Q15(b)': 'dairy-cattle|innovation-and-biotechnology-in-agriculture', 'Q15(c)': 'innovation-and-biotechnology-in-agriculture',
    'Q16': 'grassland|scientific-practices-experiments-investigations', 'Q16(b)': 'grassland|dairy-cattle',
    'Q16(c)(i)': 'grassland', 'Q16(c)(ii)': 'scientific-practices-experiments-investigations|soil-science',
    'Q17(a)': 'soil-science', 'Q17(a)(iii)': 'soil-science|scientific-practices-experiments-investigations',
    'Q17(b)': 'genetics|crop-production', 'Q17(c)': 'genetics|crop-production', 'Q17(d)': 'genetics|innovation-and-biotechnology-in-agriculture',
    'Q18(a)(i)': 'animal-diseases', 'Q18(a)(ii)': 'fertilisers-pollution-environment-cycles', 'Q18(b)': 'crop-production',
    'Q18(c)': 'beef-cattle|dairy-cattle',
}
# Scheme pools, lifted from the marking scheme (PDF pages 12-33).
CHARACTERISTICS = [
    ('Good body conformation', 'Triangle shape (dairy) or block shape (beef) or smooth shoulders and straight backs (sheep) or long body with thick well‐muscled hams (to allow for weight of boar at breeding) (pigs) / moderate frame size to reduce amount of feed required to maintain body condition and fertility (increase sustainability of farm) / good pelvic width to reduce incidence of dystocia (difficult calving – dairy or beef)) / long body or not too heavily muscled (pigs) / mature vulva (pigs)'),
    ('Temperament', 'Docile (quiet temperament) for easy management / identified at birth (with tags) as lambing without difficulty or up suckling quickly'),
    ('Good health', 'No signs of discharge or thriving / longevity to improve sustainability of enterprise / not a twin to a male calf (freemartin) as her reproductive tract may not have developed / good mouth – not over or undershot / tail docked properly (not too long or short) reduce incidence of flystrike or frost damage to vulva (ewe) / not too much muscle – cause difficult farrowing (gilt)'),
    ('Age and weight', 'For increased fertility ‐ 60% of mature weight at mating or 300 ‐350 kg (dairy) or 370 ‐ 420kg (beef) at mating at 15 months of age to ensure she has reached puberty or will reach max body size when older (cows don’t reach mature weight until they are 5 years old)(dairy) or liveweight of 45kg (sheep) or 130 – 150 kg at 240 days for breeding(pigs) / time of year heifer was born – need to be 2 years at the start of the calving season (early born heifers) (as heifers should calve at the start of the calving season to ensure compact calving herds) / ewe lamb is at least 10 – 12 months of age for first breeding or at least 7 – 8 months of age to ensure puberty has been reached (pigs)'),
    ('Good udder', 'Not pendulous to ensure less mastitis or less udder injury or greater longevity or young can suckle easily or easy of cluster attachment (dairy) / 4 well placed teats to ensure clusters attach or fit correctly / 4 (cows) or 2 (sheep) or 12 (pigs) well placed teats to allow for ease of suckling / free of pin (underdeveloped) nipples or free of inverted nipples (as they take up space and) do not allow milk to flow / presence of good milk vein (dairy)'),
    ('Good feet', 'No sign of lameness or foot rot (sheep only) as can reduce milk yield or animal won’t thrive / strong straight legs with large even sized claws to avoid lameness (pigs only) / walk straight'),
    ('Milk production', 'Records of parents to determine her milking potential or daughters of high yielding cows (dairy) / daughters of low producing Friesian cows (or quarter bred Friesian) X good conformation beef bull to ensure good milk supply (not too much milk) for good growth rate of the calf (beef) / beef traits (conformation) and good growth potential from sire or Simmental breed can be used to maintain milk yield or good fertility to ensure a calf per cow per year / daughter of good mother or good mothering ability (good heritability) (sheep or pigs) / daughter of ewe with high milk yield (good heritability)'),
    ('Genetics, dairy heifer', 'Daughters of top cows in herd and sired by bulls with strong maternal traits (genomically selected) / genotyped where parentage is verified and reduce risk of future inbreeding / high EBI – improved profitability or lower GHG emissions / genomically selected – the DNA of the heifer has been analysed and milk performance predicted'),
    ('Genetics, beef heifer', 'Genotyped where parentage is verified and reduce risk of future inbreeding / good beef merit (high EBI) to profitability and reduce GHG emissions / cross bred for hybrid vigour (best characteristics of both breeds) or pure bred heifer bred from a maternal bull (genotype) / daughters of top performing cows in herd (produce good quality calf with high weight gain from birth to weaning, fertile cows & have a tight calving interval, docile and easy calving)'),
    ('Genetics, ewe', 'Not a daughter of a ewe prone to prolapse / high genetic merit – perform well / was a twin or triplet for increased fertility / bred from 5 star ram'),
    ('Genetics, gilt', 'Cross bred gilt to allow for hybrid vigour (criss‐cross breeding) / daughter of good producing sow'),
]
PLANTING = {
    'Kale': ['sown into a cultivated(plough and harrow) seedbed', 'direct drilled or seed drill or one pass system or broadcast (require higher seed rate) or seeds should be sown into a fine (firm) seedbed',
             'maximum depth of 10mm (to ensure uniform germination)', 'seeding rate of 4‐5kg/ha or 70 plants per m2', 'rolled well after sowing to ensure good soil:seed contact'],
    'Miscanthus': ['Grassland site spray with total herbicide for controlling perennial weeds',
                   'ploughed from January 15th to control perennial weeds or allow frost activity to break down the soil further or help prevent ‘ley’ pests such as the larvae of two moths (the common rustic moth or the ghost moth) attacking the newly established plants',
                   '(later in the spring from March to April) the site should be rotovated or power harrowed (immediately prior to planting to improve establishment by aiding good root development, good soil root contact or improved soil aeration)',
                   'a planting rate of 16,000 rhizomes per ha or an emergence of 10‐15,000 plants per ha', 'rhizomes need to be planted at a depth of 5‐10 cm (in March or April)',
                   'sown using automatic planting machine'],
    'Oilseed rape (OSR)': ['preparing the seedbed min‐till or cultivate (plough and harrow) or one‐pass or strip‐till cultivation or in shallow stubble ploughing to remove residual compaction',
                           'sown at a seed rate of between 3.0‐4.0kg/ha (higher seed rates can be used to allow for winter losses or excellent emergence)', 'sown using a seed drill',
                           '25 cm spacing or depth of 20 mm', 'rolled to improve soil‐seed contact'],
}
ADVANTAGES = {
    'Kale': ['high digestibility', 'long utilisation period or use of idle land', 'fodder crop', 'can use used to extend grazing season',
             'out‐winter animals (less housing or slurry storage requirement)', 'high protein', 'fast growing crop'],
    'Miscanthus': ['renewable source of energy', 'perennial crop', 'carbon neutral fuel', 'reduction in GHG (carbon sinks)',
                   'low input crop (fertilisers or herbicides or pesticides)', 'increased biodiversity'],
    'Oilseed rape (OSR)': ['Green manure crop (due to its developed root system to reaches the minerals located in the lower soil layers)', 'crop can be used for human consumption',
                           'retains moisture well', 'saturates fields with oxygen', 'provides a take‐all break', 'leaves high levels of residual nitrogen for subsequent crops',
                           'helps control annual or perennial grass weeds', 'spreads the harvest workload (normally be cut before winter wheat)'],
}
SYNCHRONISATION = [
    ('ewes', 'Ewes', ['Flush ewes on good quality pasture or tupping dose', 'place progesterone sponge in vagina of ewe', 'leave for 10 – 12 days',
                      'remove (in morning) and inject PMSG', 'inseminate (let rams out) 1‐2 days later', 'ram ratio 1:10 or ram effect']),
    ('heifers-pg-heats', 'Heifers or cows: prostaglandin after natural heats', ['Allow heifers to mate to natural heats for 7 days',
                      'observe heats, then if not in heat give prostaglandin (PG) injection', 'repeat PG injection 11 days later if not in heat', 'observe heat and AI with AM:PM rule']),
    ('heifers-pg-two-shots', 'Heifers or cows: two prostaglandin shots', ['Give heifers first shot of PG 13 days before start of breeding season', 'another shot 11 days later',
                      'bull introduced 2 days prior to start of breeding season or AI 72‐96 hours later']),
    ('heifers-p4', 'Heifers or cows: progesterone (P4) device', ['Progesterone (P4) based device (PRID or CEDAR) is placed in vagina of animal for 6 – 10 days',
                      'PG injection is given day prior to removal', 'gonadotrophin (GnRH) injection', 'AI (mating) 48 hours after removal of device']),
    ('sows', 'Sows', ['P4 is given to sows for 14 – 18 days prior to insemination', 'GnRH day prior to service (AI)',
                      'located beside to boar (releases phermones) to bring sow into heat', 'double service (to increase litter size)']),
]
SEED_CHARACTERISTICS = ['Min. 85% of the plants had germination', 'Reduced weeds', 'plants were all similar height', 'plants were all the same colour',
                        'plants all had same stem or root structure or leaf', 'true variety', 'Less than 85% germinated', 'increased number of weeds present',
                        'plants varied in height', 'plants varied in colour', 'plants varied in stem or root or leaf', 'mix of other varieties']
WEED_ADVICE = ['Cultural control has to be the most important part of the IMS, and use of herbicides is less important',
               'Increase use of pre‐emergent herbicides and decrease the use of post‐emergent herbicides',
               'increase in plant numbers for increased competition with weeds so less chemical sprays required',
               'increased competition for space or light or nutrients so less chemical sprays required or some cover crops– release chemicals that suppress weeds (allelopathic) (e.g. wheat, kale, cabbage)',
               'hand pulling of weeds (prior to flowering) to reduce the chemical requirement',
               'breaks lifecycle of weeds or weeds don’t get a chance to establish in an area',
               'crop is deliberately destroyed by burning due to high incidence of weeds or disease',
               'remove all weeds from farmyard to prevent seeds being spread on fields through FYM or slurry',
               'ensure that all machinery is free from plants or seeds when moving fields to prevent cross contamination']


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='higher', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 36)),
                selectionDirectives=observed, supplementarySelections=supplementary,
                sourceNotes=[dict(questionN='2', questionRef='Q2(b)', note='Scheme PDF pages 14 and 15 carry the Q2(b) characteristics table as an image with no text layer; the marking points are read from the rendered page.')],
                independentBoundaryReview='101 base tasks, one card each (Q1(b)(iii) and its justification (iv) stay one task). 89 original cards match a published boundary and tariff unchanged; Q2(a) and Q13(a)(iii) already let any printed choice score. Seven are corrected in place (Q2(b), Q10(b), Q10(c), Q15(a)(i), Q16(c)(i), Q17(a)(i), Q17(b)(ii)); five cards are added for the missing Q9(a)(i), Q13(a)(iv), Q13(b)(iii), Q14(c)(ii) and Q18(b)(ii).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


def atlas_for(ref):
    base = ref.split(' — ')[0].split('–')[0]
    for key in (base, base.split(')(')[0] + ')' if ')(' in base else None, base.split('(')[0]):
        if key and key in ATLAS:
            return ATLAS[key]
    raise KeyError(ref)


def reviewed_tasks(existing):
    """existing: {id: card} from the authored file (originals are read, never rewritten unless corrected)."""
    paper_review()
    cards, tasks, corrections = [], [], {}
    RESTORED.clear()
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith(PREFIX) and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith(PREFIX):
            originals[cid] = record['original']

    def task(cid, ref, selection=None):
        pp, sp = REGIONS[ref]
        t = dict(questionRef='2022 HL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 44 paper and 35 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2022 HL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'
        if cid in snapshot:
            assert original_hash(card) == snapshot[cid]['originalSha256']
            RESTORED.append(card)

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2022 Higher — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2022 Higher Level examination paper — © State Examinations Commission.',
                    presentationNote='Open the original page for the published wording, photographs, tables and examination context.')

    def record(cid, t, reason):
        old = originals[cid]
        corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                originalTariffModel=old['tariffModel'], reason=reason)
        t['originalCard'] = 'corrected-in-place'

    def add(key, ref, topic, concept, question, rows, stem=None, marks=None, tariff=None, selection=None, figure=None, labels=None, extra_fields=None):
        cid = PREFIX + key
        assert cid not in originals, f'{cid} would replace an original card without a correction record'
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[ref]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='higher',
                    section='A' if int(ref.split('(')[0][1:]) <= 12 else 'B', questionRef='2022 HL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + topic],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff or {'kind': 'fixed'}, sourceMaterial=source(ref, pp))
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        if extra_fields: card.update(extra_fields)
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None, selection=None):
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2022 HL ' + ref, (cid, card['questionRef'])
        for field in drop:
            card.pop(field, None)
        if 'rows' in changes:
            changes = dict(changes, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(changes['rows'])])
        card.update(changes)
        card['curriculumNodeIds'] = [card['topicId']]
        card['sourceMaterial'] = source(ref, REGIONS[ref][0])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        record(cid, t, correction)
        cards.append(card)
        return card

    def closed(choose, options):
        return {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}

    def variants(pools, steps, notation_note):
        built = [dict(id=slug, label=label, rows=[dict(menu(options, steps, f'{label}: {notation_note}'), id='r-1')]) for slug, label, options in pools]
        return built[0]['rows'], built

    # Section A ---------------------------------------------------------------
    for k, ref in [('q1ai', 'Q1(a)(i)'), ('q1aii', 'Q1(a)(ii)'), ('q1aiii', 'Q1(a)(iii)'), ('q1bi', 'Q1(b)(i)'), ('q1bii', 'Q1(b)(ii)'),
                   ('q1biii-iv', 'Q1(b)(iii)–(iv)')]:
        keep(k, ref)
    keep('q2a', 'Q2(a)', selection=closed(4, ['A', 'B', 'C', 'D', 'E', 'F']))
    fix('q2b', 'Q2(b)', dict(
        rows=[menu([d for _, d in CHARACTERISTICS], [3, 3],
                   'Two characteristics for the enterprise you named, 3 marks each (2(3)). In order the options are the scheme\'s '
                   + ', '.join(name.lower() for name, _ in CHARACTERISTICS) + '.')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 5 ("A farmer was looking to select a female replacement animal for breeding for his chosen animal enterprise. Describe characteristics he would be looking for", a Named animal enterprise line) '
                    'and scheme PDF pages 13 to 15 ("Details on next page", 2(3), then a table of characteristics for a dairy heifer, beef heifer, ewe or gilt). '
                    'The original quoted ten scattered points; age and weight, the good udder, the good feet and most of each characteristic\'s description were missing. '
                    'Same ID, boundary and 6 marks; one row lists every characteristic in the scheme\'s own words, any two at 3 marks.'))
    for k, ref in [('q3a', 'Q3(a)'), ('q3b', 'Q3(b)'), ('q3c', 'Q3(c)'), ('q4a', 'Q4(a)'), ('q4b', 'Q4(b)'), ('q4c', 'Q4(c)'),
                   ('q5a', 'Q5(a)'), ('q5bi', 'Q5(b)(i)'), ('q5bii', 'Q5(b)(ii)'), ('q6a', 'Q6(a)'), ('q6b', 'Q6(b)'), ('q6c', 'Q6(c)'),
                   ('q7a', 'Q7(a)'), ('q7b', 'Q7(b)'), ('q7c', 'Q7(c)'), ('q8ai', 'Q8(a)(i)'), ('q8aii', 'Q8(a)(ii)'), ('q8b', 'Q8(b)')]:
        keep(k, ref)
    add('q9ai', 'Q9(a)(i)', '4-1', 'drawing-a-calfs-stomach', 'Draw a labelled diagram of a calf’s stomach in its first week of life.',
        [point('Candidates diagram must clearly show all four chambers, the abomasum being the largest stomach in comparison to others, especially the rumen or oesophageal groove directing the milk straight to the abomasum', None,
               'Drawing, D = 3, 2, 0.', kind='criterion'),
         point('Any three labels', None, 'Labels, L = 3(1): any three correct labels, 1 mark each.')],
        'Answer either (a) or (b).', marks=6, tariff={'kind': 'questionTotal', 'notation': 'D = 3, 2, 0 + L = 3(1)'})
    for k, ref in [('q9aii', 'Q9(a)(ii)'), ('q9bi', 'Q9(b)(i)'), ('q9bii', 'Q9(b)(ii)'), ('q9biii', 'Q9(b)(iii)'), ('q10a', 'Q10(a)')]:
        keep(k, ref)
    crops = list(PLANTING)
    slugs = {'Kale': 'kale', 'Miscanthus': 'miscanthus', 'Oilseed rape (OSR)': 'osr'}
    rows, built = variants([(slugs[c], c, PLANTING[c]) for c in crops], [2, 2], 'any two planting points, 2 marks each (2(2)).')
    fix('q10b', 'Q10(b)', dict(rows=rows, answerVariants=built), drop=('notes',), selection=closed(1, crops),
        correction=('Visually verified paper PDF page 14 ("In relation to a named catch or energy crop you have studied", "(b) Describe the method of planting of your choosen crop.") and scheme PDF page 21 (separate kale, Miscanthus and OSR pools, "2(2)"). '
                    'The original rows were two kale points with every Miscanthus and OSR point mixed into their accepted wordings, so points from different crops could be combined. '
                    'Same ID, boundary and 4 marks; each crop the scheme answers for is an answer route the student chooses before reveal, listing every published point, any two at 2 marks.'))
    rows, built = variants([(slugs[c], c, ADVANTAGES[c]) for c in crops], [2, 2], 'any two advantages, 2 marks each (2(2)).')
    fix('q10c', 'Q10(c)', dict(rows=rows, answerVariants=built), drop=('notes',), selection=closed(1, crops),
        correction=('Visually verified paper PDF page 14 ("(c) Outline advantages of sowing your chosen crop.") and scheme PDF page 21 (separate kale, Miscanthus and OSR pools, "2(2)"). '
                    'The original rows were two kale points with every Miscanthus and OSR advantage mixed into their accepted wordings. '
                    'Same ID, boundary and 4 marks; each crop is an answer route the student chooses before reveal, listing every published advantage, any two at 2 marks.'))
    for k, ref in [('q11ai', 'Q11(a)(i)'), ('q11aii', 'Q11(a)(ii)'), ('q11aiii', 'Q11(a)(iii)'), ('q11bi', 'Q11(b)(i)'), ('q11bii', 'Q11(b)(ii)'),
                   ('q11biii', 'Q11(b)(iii)'), ('q11biv', 'Q11(b)(iv)'), ('q12ai', 'Q12(a)(i)'), ('q12aii', 'Q12(a)(ii)'), ('q12aiii', 'Q12(a)(iii)'),
                   ('q12bi', 'Q12(b)(i)'), ('q12bii', 'Q12(b)(ii)'), ('q12biii', 'Q12(b)(iii)'), ('q12biv', 'Q12(b)(iv)')]:
        keep(k, ref)
    # Section B ---------------------------------------------------------------
    for k, ref in [('q13ai', 'Q13(a)(i)'), ('q13aii', 'Q13(a)(ii)')]:
        keep(k, ref)
    keep('q13aiii', 'Q13(a)(iii)', selection=closed(2, ['A', 'B', 'C']))
    sward = originals[PREFIX + 'q13aiii']
    add('q13aiv', 'Q13(a)(iv)', '3-1', 'reproductive-stage-of-sward-plants',
        'Identify the growth cycle stage of the plants in part (iii) and describe briefly what happens at this stage.',
        [point('Reproductive stage', 3, 'Stage: 3 marks.'),
         dict(point('Seed head develops or heading out or flowering', 3, 'Description: 3 marks; any one of the scheme\'s descriptions.'), kind='alt',
              accepts=['stem is strong enough to hold plant upright', 'wind pollination occurs in A or insect pollination occurs in B'])],
        'Maintaining a constant supply of high quality leafy grass can be easily achieved by managing and measuring the amount of grass on the farm. '
        'In part (iii) a farmer identified different plants in the sward while measuring the grass: A Italian ryegrass, B chicory and C cocksfoot.',
        figure=sward['figureKey'], labels=copy.deepcopy(sward['labelKey']))
    keep('q13bi', 'Q13(b)(i)')
    keep('q13bii', 'Q13(b)(ii)')
    add('q13biii', 'Q13(b)(iii)', '3-3-1', 'certified-versus-uncertified-seed-crop',
        'Gerry was able to compare the plant uniformity of both batches of seed (certified and uncertified). Describe the characteristics Gerry would have observed to determine which batch was certified and which was uncertified.',
        [menu(SEED_CHARACTERISTICS, [4, 4], 'Two characteristics, 4 marks each (2(4)). The first six options are the scheme\'s certified-seed column and the last six its uncertified-seed column; a characteristic and its opposite are the same characteristic.')],
        'Gerry wants to reseed his grassland pastures. He ordered two batches of seeds, certified and uncertified, which arrived unlabelled, and carried out a research trial in a small section of his field to distinguish between them.')
    keep('q13biv', 'Q13(b)(iv)')
    for k, ref in [('q14ai', 'Q14(a)(i)'), ('q14aii', 'Q14(a)(ii)'), ('q14aiii', 'Q14(a)(iii)'), ('q14aiv', 'Q14(a)(iv)'), ('q14av', 'Q14(a)(v)'),
                   ('q14bi', 'Q14(b)(i)'), ('q14bii', 'Q14(b)(ii)'), ('q14ci', 'Q14(c)(i)')]:
        keep(k, ref)
    add('q14cii', 'Q14(c)(ii)', '4-3-3', 'natural-airflow-in-a-calf-shed',
        'A farmer let off a smoke bomb in his calf shed to check the ventilation. Complete the diagram using arrows to show the natural airflow he should expect through the shed.',
        [point('Correct indication of arrows coming in at side', None, 'The scheme prints 4 + 1 for the arrows; its drawn answer shows after you reveal.'),
         point('going out through roof', None)],
        'Answer both (a) and (b) with either (c) or (d). Part (c): analyse the picture of calf housing and answer the questions which follow.',
        marks=5, tariff={'kind': 'orderedSplit', 'notation': '4 + 1'}, figure='agsci-2022-hl-scheme-calf-shed-airflow',
        extra_fields={'questionFigureKey': 'agsci-2022-hl-paper-calf-shed-airflow'})
    for k, ref in [('q14di', 'Q14(d)(i)'), ('q14dii', 'Q14(d)(ii)'), ('q14diii', 'Q14(d)(iii)')]:
        keep(k, ref)
    rows, built = variants(SYNCHRONISATION, [3, 3], 'any two steps, 3 marks each (2(3)).')
    fix('q15ai', 'Q15(a)(i)', dict(rows=rows, answerVariants=built, tariffModel={'kind': 'fixed', 'notation': '2(3)'},
                                  stem='Animals maybe synchronised at breeding. The paper asks you to name the animal first.'),
        drop=('notes',), selection=closed(1, [label for _, label, _ in SYNCHRONISATION]),
        correction=('Visually verified paper PDF page 27 ("Animals maybe synchronised at breeding. Describe how this is carried out for a named animal you have studied.", a Named animal line) and scheme PDF page 27 '
                    '(protocols for ewes, heifers or cows by prostaglandin after natural heats, "Or" by two prostaglandin shots, by a progesterone (P4) device, and for sows; "2(3)"). '
                    'The original mixed ten steps from different animals in one group, so steps from different protocols could be combined, and left out the rest of each protocol. '
                    'Same ID, boundary and 6 marks; each protocol is an answer route the student chooses before reveal, listing every published step, any two at 3 marks.'))
    for k, ref in [('q15aii', 'Q15(a)(ii)'), ('q15aiii', 'Q15(a)(iii)'), ('q15bi', 'Q15(b)(i)'), ('q15bii', 'Q15(b)(ii)'), ('q15biii', 'Q15(b)(iii)'),
                   ('q15biv', 'Q15(b)(iv)'), ('q15ci', 'Q15(c)(i)'), ('q15cii', 'Q15(c)(ii)'), ('q16ai', 'Q16(a)(i)'), ('q16aii', 'Q16(a)(ii)'),
                   ('q16aiii', 'Q16(a)(iii)'), ('q16bi', 'Q16(b)(i)'), ('q16bii', 'Q16(b)(ii)'), ('q16biii', 'Q16(b)(iii)')]:
        keep(k, ref)
    fix('q16ci', 'Q16(c)(i)', dict(
        stem='An investigation looking at milk production from grass and white clover systems over the course of a year was carried out by Teagasc researchers in Moorepark.',
        rows=[point('Named grazing system – Paddock (rotational) / block / strip grazing / spokes of a wheel', None, 'Named system: 2 marks. The scheme adds "(Zero grazing is not accepted)".'),
              point('For 6 marks: diagram must show fencing, water supply, indication of animal movement', None,
                    'Drawing, D - 6, 3, 0: "For 3 marks: diagram has one of the elements above missing".', kind='criterion'),
              point('Marks awarded for any 3 labelled parts', None, 'Labels, L - 3(1).')],
        tariffModel={'kind': 'questionTotal', 'notation': '2 + D - 6, 3, 0 + L - 3(1)'}, totalMarks=11), drop=('notes',),
        correction=('Visually verified paper PDF page 31 ("Describe using a labelled diagram a named grazing system that could have been used to manage the swards in the trial in part (a).", a Named grazing system line and a labelled diagram box) '
                    'and scheme PDF page 29 (named system 2; "D - 6, 3, 0 L - 3(1)"), which is the 11 marks Question 16 needs to total 50 (15 + 12 + 11 + 12). '
                    'The original priced the named system alone at 3 and left the drawing and its labels out. Same ID and boundary; the card now carries the published 11 marks as a name, a banded drawing and labels.'))
    keep('q16cii', 'Q16(c)(ii)')
    fix('q17ai', 'Q17(a)(i)', dict(
        rows=[point('Diagram: A number of layers, presence of organic matter, earthworms, creating channels or mixing layers (indication of activity)', None,
                    'Drawing, D - 6, 3, 0 (showing layers).', kind='criterion'),
              point('Layer of organic matter (leaf litter) on top or decomposed organic matter / layer of chalk or layer of compost or layer of sand or layer of gravel / earthworms /create channels / mixing layers / wormery or soil profile', None,
                    'Labels - 3(1): any three of these labels, 1 mark each.')],
        tariffModel={'kind': 'questionTotal', 'notation': 'D - 6, 3, 0 + Labels - 3(1)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 33 ("Describe using a labelled diagram the activity of earthworms in a soil.", a labelled diagram box) and scheme PDF page 30 ("D - 6, 3, 0 (showing layers)", "Labels - 3(1)"). '
                    'The original priced the drawing as one 6-mark row, so a drawing missing an element could not earn the published 3, and its answer stopped at "earthworms". '
                    'Same ID, boundary and 9 marks; the drawing criterion and the labels are judged against the published total.'))
    for k, ref in [('q17aii', 'Q17(a)(ii)'), ('q17aiii', 'Q17(a)(iii)'), ('q17aiv', 'Q17(a)(iv)'), ('q17bi', 'Q17(b)(i)')]:
        keep(k, ref)
    old = originals[PREFIX + 'q17bii']
    fix('q17bii', 'Q17(b)(ii)', dict(rows=[old['rows'][0],
        point('Hybrid vigour ‐ a cross‐bred individual to shows qualities superior to those of both parents', 3)]),
        correction=('Visually verified paper PDF page 35 ("Scientists genotype the plants and cross two high yielding plants to achieve good hybrid vigour. Explain the underlined terms.") and scheme PDF page 30 (genotype 3, hybrid vigour 3). '
                    'The original hybrid vigour answer stopped at "qualities superior", leaving out "to those of both parents". Same ID, boundary and 6 marks.'))
    for k, ref in [('q17ci', 'Q17(c)(i)'), ('q17cii', 'Q17(c)(ii)'), ('q17di', 'Q17(d)(i)'), ('q17dii', 'Q17(d)(ii)'), ('q18ai', 'Q18(a)(i)')]:
        keep(k, ref)
    keep('q18aii', 'Q18(a)(ii)', selection=closed(1, ['Animal enterprise', 'Tillage enterprise']))
    keep('q18bi', 'Q18(b)(i)')
    weeds = originals[PREFIX + 'q18bi']
    add('q18bii', 'Q18(b)(ii)', '3-3-2', 'integrated-weed-management-advice',
        'You have been asked to address a group of tillage farmers. Using the ‘Integrated Management System’ for controlling weeds (outlined on previous page), provide advice to them on the future of weed control on their farms.',
        [menu(WEED_ADVICE, [4, 4, 4], 'Three pieces of advice, 4 marks each (3(4)). The scheme answers each heading of the diagram: integrated management, use of herbicides, '
              'increased seed rates and competitive crops (one answer for both), cover crops, rogueing, crop rotation and whole cropping (one answer for both), crop destruction, on-farm hygiene and machinery hygiene, in that order.')],
        'The diagram below shows an ‘Integrated Management System’ for controlling weeds. Analyse the diagram and answer the questions which follow.',
        figure=weeds['figureKey'])
    for k, ref in [('q18ci', 'Q18(c)(i)'), ('q18cii', 'Q18(c)(ii)')]:
        keep(k, ref)
    assert len(tasks) == 101 and len(corrections) == 7 and len(originals) == 96 and len(cards) == 12, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2022 Higher card must be reviewed'
    return cards, tasks, corrections
