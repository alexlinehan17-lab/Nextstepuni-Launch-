"""2021 Higher review: the 101 original cards reconciled against the SEC sources.

All 52 paper pages and 39 scheme pages were inspected and the independent
census transcribed before any card was touched. 106 base tasks, one card each.
Q13(a)(iii) keeps its two published boundaries (the name at 4, the advantages
at 4+2), and Q14(a) and Q18(a) are carded by printed heading because the scheme
prices each heading on its own (4+2 and 2(2)). 71 original card objects match
a published boundary and tariff and are left byte-identical; they only gain an
Atlas binding and an inspected official source page. 30 originals are corrected
IN PLACE, keeping their IDs: named-crop, named-disorder, named-species,
named-test and named-crop-preservation answers become answer routes instead of
one mixed pool; pools that dropped published points list every point; four
answers truncated mid-sentence regain the scheme's wording; four rows lose a
dash the scheme never printed; stems built from table, axis or sign debris are
replaced by the paper's lead-in and an inspected crop; Q1(b) and Q17(b)(iv)
regain their published splits. Cards are added for the missing Q14(a)
headings, Q15(b)(ii) and Q16(a)(i). Each correction records the original
wording, marks and object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
import re
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024ALP000EV.pdf'
YEAR = 2021
HASHES = {'exampapers':'d60e656eff0863123d5c8152f114bcd323ed0cf81144676becf1f367c2b9d4e3',
          'markingschemes':'6a1ad8c18dcabcd40f63f9b10f28ea23089a29bf4c34cd22ce097c8e988e99a8'}
SELECTIONS = {
    '93c0169ea23ec09c':('exam-selection','Instructions: Section A, seven of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    '588519d631c6a81d':('exam-selection','Instructions: Section B, three of six independent questions. Every question is retained.'),
    '9ac5fdd7ce4a092d':('exam-selection','Repeated Section A instruction: seven independent 10-mark questions, all retained.'),
    'a335f8a2555520a2':('independent-task-selection','Q2 either (a) or (b): both independently marked alternatives are retained.'),
    '3b837fd3a3b243b2':('not-a-selection','Prose in the Q2 article ("one of the most widely recognised weeds"); no response choice.'),
    '53e9fb7555990b75':('independent-task-selection','Q3 either (a) or (b): both alternatives are retained.'),
    '38aed7a703a1c97c':('independent-task-selection','Q6 either (a) or (b): both alternatives are retained.'),
    '528cc8e4bae3e9aa':('not-a-selection','Prose in the Q10 lead-in ("operate one of Ireland\'s sheep dairy farms"); no response choice.'),
    '521052cc84f8b9f4':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    'd248ebc99079542b':('exam-selection','Section B heading: three of six independent 50-mark questions, all retained.'),
    'e5d33bfb49764ae1':('independent-task-selection','Q13: (a) with either (b) or (c). Every part, including both (b) and (c), is retained.'),
    '6777398652c30a1f':('independent-task-selection','Q16: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '7653e96a119afe36':('open','Q17(b)(iv): any two macronutrients that are not on the table. The paper prints no list; the scheme\'s sulfur, calcium, magnesium and nitrogen are a marking menu.'),
}
SUPPLEMENTARY = [
    (9,'In relation to a catch crop or energy crop you have studied','closed','Q5(a)-(c): a student-named catch or energy crop; the scheme answers for kale or stubble turnips, oilseed rape and Miscanthus, kept as answer routes on one card each.'),
    (17,'Briefly describe a named disorder of the ruminant digestive system','closed','Q11(b)(ii): a student-named disorder; the scheme answers for bloat and acidosis, kept as answer routes on one card.'),
    (26,'Compare two different systems of animal production for a chosen livestock enterprise','closed','Q14(a): a chosen enterprise and pair of systems; the scheme answers for liquid v creamery milk, calf to beef v suckler beef and mid-season v early lamb, kept as answer routes on each heading card.'),
    (27,'In relation to two named breeds of pig or horse or poultry','closed','Q14(b)(ii): two breeds of one species; the scheme answers for pigs, poultry and horses, kept as answer routes on one card.'),
    (37,'Describe, with the aid of a labelled diagram, how Joe could carry out this investigation','closed','Q16(b): the scheme answers with a resazurin test or a total bacterial count, kept as answer routes on one card.'),
    (44,'Discuss the effect of each of the following on the productivity of a named crop','closed','Q18(a): a student-named crop; the scheme\'s crop preservation answers are separate grain, potato and grass pools, kept as answer routes on that heading\'s card.'),
    (14,'Outline two advantages of using genomically selected animals in a named animal enterprise','open','Q9(b): no marks for naming the enterprise; the scheme\'s advantages are one pool.'),
    (16,'Describe two advantages of artificial insemination (AI) in cattle or sheep or pigs','open','Q11(a)(iii): no marks for naming the animal; the scheme\'s advantages are one pool.'),
    (10,'by placing a tick','answer-identification','Q6(a)(i): one correct box (mitochondria).'),
    (13,'Calculate which heifers were worth more money to John','answer-identification','Q8(c): one correct conclusion (the Limousine heifers).'),
    (33,'Identify which treatment is the most beneficial organic fertiliser','answer-identification','Q15(b)(i): one correct treatment (FYM high).'),
    (35,'Calculate which farmer (Dan or Joe) earns a higher price for their milk','answer-identification','Q16(a)(i): one correct farmer (Dan).'),
]
TOPIC = 'agricultural-science-higher-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2021-hl-'
RESTORED = []
PAGE4 = 'The scheme\'s own rule (PDF page 4): "the first correct answer encountered is awarded" the first mark, and each later correct answer the next.'

P = lambda *r: [region(*x) for x in r]
Q14_HEAD = (22, .085, .30)
REGIONS = {
    'Q1(a)': (P((3, .155, .515)), P((11, .137, .212))),
    'Q1(b)': (P((3, .155, .41), (3, .52, .565)), P((11, .212, .448))),
    'Q2(a)(i)': (P((4, .065, .44)), P((11, .452, .535))),
    'Q2(a)(ii)': (P((4, .065, .11), (4, .475, .60)), P((11, .535, .665))),
    'Q2(a)(iii)': (P((4, .065, .11), (4, .63, .672)), P((11, .665, .855))),
    'Q2(b)(i)': (P((5, .065, .24)), P((12, .085, .202))),
    'Q2(b)(ii)': (P((5, .065, .135), (5, .305, .335)), P((12, .202, .372))),
    'Q2(b)(iii)': (P((5, .065, .135), (5, .703, .73)), P((12, .372, .455))),
    'Q3(a)(i)': (P((6, .065, .36)), P((12, .462, .527))),
    'Q3(a)(ii)': (P((6, .065, .09), (6, .485, .76)), P((12, .527, .591))),
    'Q3(a)(iii)': (P((6, .065, .09), (6, .51, .70), (6, .765, .81)), P((12, .591, .69))),
    'Q3(b)(i)': (P((7, .065, .40)), P((13, .085, .165))),
    'Q3(b)(ii)': (P((7, .095, .335), (7, .405, .448)), P((13, .165, .257))),
    'Q3(b)(iii)': (P((7, .095, .335), (7, .515, .54)), P((13, .257, .331))),
    'Q3(b)(iv)': (P((7, .095, .335), (7, .608, .652)), P((13, .331, .46))),
    'Q4(a)': (P((8, .065, .455)), P((13, .467, .541))),
    'Q4(b)': (P((8, .065, .425), (8, .52, .548)), P((13, .541, .633))),
    'Q4(c)': (P((8, .065, .425), (8, .675, .72)), P((13, .633, .855))),
    'Q5(a)': (P((9, .065, .197)), P((14, .085, .488))),
    'Q5(b)': (P((9, .065, .165), (9, .39, .442)), P((14, .488, .71))),
    'Q5(c)': (P((9, .065, .165), (9, .55, .572)), P((15, .085, .35))),
    'Q6(a)(i)': (P((10, .065, .215)), P((15, .355, .377))),
    'Q6(a)(ii)': (P((10, .065, .09), (10, .215, .258)), P((15, .377, .499))),
    'Q6(a)(iii)': (P((10, .065, .09), (10, .388, .412)), P((15, .499, .595))),
    'Q6(b)(i)': (P((11, .065, .113)), P((15, .595, .685))),
    'Q6(b)(ii)': (P((11, .065, .09), (11, .215, .255)), P((15, .685, .79))),
    'Q6(b)(iii)': (P((11, .065, .09), (11, .508, .53)), P((15, .79, .87))),
    'Q7(a)': (P((12, .065, .113)), P((16, .085, .132))),
    'Q7(b)': (P((12, .065, .09), (12, .213, .237)), P((16, .132, .265))),
    'Q7(c)': (P((12, .065, .09), (12, .337, .362)), P((16, .265, .49))),
    'Q8(a)': (P((13, .065, .278)), P((16, .496, .539))),
    'Q8(b)': (P((13, .065, .255), (13, .348, .478)), P((16, .539, .624))),
    'Q8(c)': (P((13, .065, .255), (13, .348, .478), (13, .632, .69)), P((16, .624, .75))),
    'Q9(a)': (P((14, .065, .113)), P((17, .085, .146))),
    'Q9(b)': (P((14, .065, .09), (14, .19, .244)), P((17, .146, .323))),
    'Q9(c)': (P((14, .065, .09), (14, .449, .491)), P((17, .323, .422))),
    'Q9(d)': (P((14, .065, .09), (14, .628, .687)), P((17, .422, .585))),
    'Q10(a)': (P((15, .065, .20)), P((17, .592, .678))),
    'Q10(b)': (P((15, .065, .172), (15, .332, .355)), P((17, .678, .773))),
    'Q10(c)': (P((15, .065, .172), (15, .487, .815)), P((17, .773, .835))),
    'Q11(a)(i)': (P((16, .065, .113)), P((18, .085, .202))),
    'Q11(a)(ii)': (P((16, .065, .09), (16, .306, .328)), P((18, .202, .242))),
    'Q11(a)(iii)': (P((16, .065, .09), (16, .37, .422)), P((18, .242, .495))),
    'Q11(b)(i)': (P((17, .065, .113)), P((18, .505, .64))),
    'Q11(b)(ii)': (P((17, .065, .09), (17, .245, .316)), P((19, .085, .465))),
    'Q12(a)': (P((18, .065, .239)), P((19, .473, .512))),
    'Q12(b)': (P((18, .065, .172), (18, .278, .303)), P((19, .512, .552))),
    'Q12(c)': (P((18, .065, .172), (18, .372, .397)), P((19, .552, .592))),
    'Q12(d)': (P((18, .065, .172), (18, .466, .491)), P((19, .592, .825))),
    'Q13(a)(i)': (P((22, .155, .457)), P((20, .137, .179))),
    'Q13(a)(ii)': (P((22, .155, .435), (22, .496, .538)), P((20, .179, .323))),
    'Q13(a)(iii) Name': (P((22, .155, .205), (22, .668, .71)), P((20, .323, .388))),
    'Q13(a)(iii) Advantages': (P((22, .155, .205), (22, .668, .71)), P((20, .388, .532))),
    'Q13(a)(iv)': (P((22, .155, .435), (23, .062, .158)), P((20, .532, .85))),
    'Q13(a)(v)': (P((22, .155, .205), (24, .062, .106)), P((21, .085, .153))),
    'Q13(b)': (P((22, .155, .18), (25, .065, .32)), P((21, .153, .287))),
    'Q13(c)': (P((22, .155, .18), (25, .415, .454)), P((21, .287, .673))),
    'Q14(a) Housing': (P((26, .065, .255)), P(Q14_HEAD, (22, .32, .458), (23, .10, .386), (24, .10, .289))),
    'Q14(a) Nutrition': (P((26, .065, .215), (26, .448, .475)), P(Q14_HEAD, (22, .32, .342), (22, .455, .605), (23, .10, .125), (23, .385, .568), (24, .10, .125), (24, .288, .422))),
    'Q14(a) Production targets': (P((26, .065, .215), (26, .668, .695)), P(Q14_HEAD, (22, .32, .342), (22, .603, .68), (23, .10, .125), (23, .567, .75), (24, .10, .125), (24, .42, .545))),
    'Q14(b)(i)': (P((27, .062, .21)), P((25, .085, .178))),
    'Q14(b)(ii)': (P((27, .338, .435)), P((25, .178, .66))),
    'Q14(b)(iii)': (P((27, .585, .627)), P((26, .085, .49))),
    'Q14(c)(i)': (P((28, .065, .775), (29, .062, .106)), P((26, .49, .84))),
    'Q14(c)(ii)': (P((28, .065, .775), (29, .206, .247)), P((27, .085, .18))),
    'Q14(c)(iii)': (P((28, .065, .775), (29, .347, .372)), P((27, .18, .241))),
    'Q14(c)(iv)': (P((28, .065, .775), (30, .062, .123)), P((27, .241, .63))),
    'Q15(a)(i)': (P((31, .065, .24)), P((28, .085, .149))),
    'Q15(a)(ii)': (P((31, .065, .212), (31, .31, .334)), P((28, .149, .238))),
    'Q15(a)(iii)': (P((31, .065, .212), (31, .464, .506)), P((28, .238, .55))),
    'Q15(a)(iv)': (P((31, .065, .212), (32, .062, .106)), P((28, .55, .752))),
    'Q15(a)(v)': (P((31, .065, .212), (32, .69, .732)), P((28, .752, .835))),
    'Q15(b)(i)': (P((33, .065, .473)), P((29, .085, .139))),
    'Q15(b)(ii)': (P((33, .065, .425), (33, .542, .60)), P((29, .139, .388))),
    'Q15(b)(iii)': (P((33, .065, .425), (34, .065, .123)), P((29, .388, .512))),
    'Q15(b)(iv)': (P((33, .065, .425), (34, .286, .36)), P((29, .512, .66))),
    'Q16(a)(i)': (P((35, .065, .438)), P((30, .085, .27))),
    'Q16(a)(ii)': (P((35, .065, .148), (35, .614, .636)), P((30, .27, .396))),
    'Q16(a)(iii)': (P((35, .065, .148), (36, .065, .335)), P((30, .396, .835))),
    'Q16(b)': (P((37, .065, .123)), P((31, .085, .68))),
    'Q16(c)(i)': (P((38, .065, .32)), P((32, .085, .203))),
    'Q16(c)(ii)': (P((38, .065, .297), (38, .409, .451)), P((32, .203, .285))),
    'Q16(c)(iii)': (P((38, .065, .106), (38, .517, .541)), P((32, .285, .384))),
    'Q16(c)(iv)': (P((38, .065, .106), (38, .663, .702)), P((32, .384, .64))),
    'Q16(d)(i)': (P((39, .065, .30)), P((33, .085, .182))),
    'Q16(d)(ii)': (P((39, .09, .235), (39, .429, .453)), P((33, .182, .243))),
    'Q16(d)(iii)': (P((39, .09, .112), (39, .523, .564)), P((33, .243, .405))),
    'Q16(d)(iv)': (P((39, .09, .112), (39, .748, .79)), P((33, .405, .52))),
    'Q17(a)': (P((40, .065, .17)), P((33, .531, .64))),
    'Q17(b)(i)': (P((40, .30, .725), (41, .065, .41)), P((33, .64, .69))),
    'Q17(b)(ii)': (P((40, .30, .725), (41, .43, .47)), P((33, .69, .875))),
    'Q17(b)(iii)': (P((40, .30, .53), (41, .572, .611)), P((34, .085, .258))),
    'Q17(b)(iv)': (P((40, .30, .725), (42, .065, .106)), P((34, .258, .447))),
    'Q17(b)(v)': (P((40, .30, .53), (42, .299, .321)), P((34, .447, .51))),
    'Q17(b)(vi)': (P((40, .30, .725), (42, .514, .554)), P((34, .51, .609))),
    'Q17(c)': (P((43, .065, .106)), P((34, .609, .832))),
    'Q18(a) Soil quality': (P((44, .065, .235)), P((35, .085, .39))),
    'Q18(a) Crop preservation': (P((44, .065, .165), (44, .343, .38)), P((35, .085, .16), (35, .39, .83))),
    'Q18(b)': (P((44, .502, .562)), P((36, .085, .445))),
    'Q18(c)(i)': (P((45, .24, .596)), P((37, .085, .128))),
    'Q18(c)(ii)': (P((45, .24, .57), (45, .665, .69)), P((37, .128, .206))),
    'Q18(c)(iii)': (P((45, .24, .57), (46, .062, .088)), P((37, .206, .284))),
    'Q18(c)(iv)': (P((45, .24, .57), (46, .219, .26)), P((37, .284, .338))),
    'Q18(c)(v)': (P((45, .24, .57), (46, .33, .389)), P((37, .338, .416))),
    'Q18(c)(vi)': (P((45, .24, .57), (46, .58, .604)), P((37, .416, .459))),
    'Q18(c)(vii)': (P((45, .24, .28), (46, .644, .668)), P((37, .459, .765))),
}
ATLAS = {
    'Q1': 'classification-of-animals-plants', 'Q1(b)': 'classification-of-animals-plants|plant-physiology',
    'Q2(a)': 'crop-production', 'Q2(b)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3(a)': 'beef-cattle|dairy-cattle', 'Q3(b)': 'crop-production|grassland', 'Q3(b)(iv)': 'grassland|dairy-cattle',
    'Q4': 'fertilisers-pollution-environment-cycles', 'Q5': 'energy-crop-catch-crop',
    'Q6(a)': 'soil-science', 'Q6(a)(i)': 'plant-physiology', 'Q6(b)': 'fertilisers-pollution-environment-cycles|soil-science',
    'Q7': 'fertilisers-pollution-environment-cycles', 'Q8': 'beef-cattle', 'Q9': 'genetics', 'Q9(d)': 'animal-diseases|genetics',
    'Q10': 'sheep', 'Q11(a)': 'animal-physiology-reproductive-systems', 'Q11(b)': 'animal-physiology-digestive-system',
    'Q11(b)(ii)': 'animal-physiology-digestive-system|animal-diseases', 'Q12': 'pigs|animal-diseases',
    'Q13(a)': 'grassland', 'Q13(a)(v)': 'grassland|scientific-practices-experiments-investigations',
    'Q13(b)': 'fertilisers-pollution-environment-cycles', 'Q13(c)': 'crop-production|fertilisers-pollution-environment-cycles',
    'Q14(a)': 'dairy-cattle|beef-cattle|sheep', 'Q14(b)(i)': 'beef-cattle|sheep', 'Q14(b)(ii)': 'pigs', 'Q14(b)(iii)': 'beef-cattle',
    'Q14(c)': 'beef-cattle|animal-diseases',
    'Q15(a)': 'grassland|scientific-practices-experiments-investigations', 'Q15(a)(iii)': 'fertilisers-pollution-environment-cycles',
    'Q15(b)': 'grassland|fertilisers-pollution-environment-cycles',
    'Q16(a)': 'dairy-cattle', 'Q16(b)': 'dairy-cattle|scientific-practices-experiments-investigations',
    'Q16(c)': 'dairy-cattle|fertilisers-pollution-environment-cycles', 'Q16(d)': 'innovation-and-biotechnology-in-agriculture|grassland',
    'Q16(d)(iii)': 'grassland|beef-cattle',
    'Q17': 'soil-science', 'Q17(b)(iv)': 'soil-science|plant-physiology', 'Q17(b)(vi)': 'fertilisers-pollution-environment-cycles|soil-science',
    'Q17(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q18(a)': 'crop-production', 'Q18(b)': 'dairy-cattle|fertilisers-pollution-environment-cycles', 'Q18(c)': 'dairy-cattle',
    'Q18(c)(iv)': 'dairy-cattle|animal-physiology-reproductive-systems', 'Q18(c)(vii)': 'dairy-cattle|animal-physiology-reproductive-systems',
}
CROPS = [
    ('kale', 'Kale or stubble turnips',
     ['protection of soil structure against soil erosion (from heavy rain)', 'reduced soil compaction or easier subsequent cultivation as roots which break up the soil',
      'increased soil organic matter (whose main constituent soil organic carbon removes CO2 from the atmosphere)', 'prevents mineral leaching as it uses up nutrients',
      'act as a break crop for weeds, pests and diseases (so less chemicals required)',
      'animals out‐wintered or extends the grazing season ‐ less slurry storage or less housing requirements or less winter feed',
      'high protein ‐ less concentrates needed', 'earthworm activity increased'],
     ['Flea beetle eats holes (in the emerging seedlings, stems of) leaves of plant', 'diamondback moth or white cabbage butterfly caterpillar feeds on the leaves of the crop',
      'aphids suck sap damaging leaves', 'slugs or rabbits eat leaves of crop'],
     ['Germination ‐ cotyledon (seed leaf) emerge from the soil',
      'Vegetative stage: true leaves produced (with uptake of nitrogen to stage where crop is in utilisation stage suitable for grazing in situ)']),
    ('osr', 'Oilseed rape (OSR)',
     ['weed control ‐less herbicides required', 'strong tap root development ‐ reduced soil compaction',
      'improve soil structure which controls drainage and aeration (maintains optimum N mineralisation rates)', 'prevention of nitrogen leaching as it uses up nutrients',
      'prevent soil erosion as root system binds soil', 'can be used as a biofuel reducing diesel requirements reducing the burning of fossil fuels'],
     ['Bird damage over winter, pick at (small tender) leaves', 'flea beetle eat holes in leaves or larvae burrow into the stem'],
     ['Germination and emergence ‐ cotyledon (seed leaf) emergence above ground',
      'Vegetative stage ‐ leaf development and side shoot formation ( occurs once 1st true leaves emerge produces multiple side shoots)']),
    ('miscanthus', 'Miscanthus',
     ['carbon neutral crop or reduces greenhouse gas emissions', 'low fertiliser requirement', 'no serious pest problems so pesticide use is limited', 'increases wildlife biodiversity'],
     ['Larvae (caterpillar) of common rustic moth or ghost moth feed on roots of crop', 'wireworms bite holes in the stems or shoots'],
     ['After establishment: shoots emerge from underground rhizomes in spring', 'Vegetative growth: in summer producing leaf and stem growth (reaching a height of 3m)']),
]
CROP_OPEN = 'The scheme adds "OR valid answer for other named valid crop(s)".'
SYSTEMS = [
    ('dairy', 'Liquid milk v creamery milk', {
        'Housing': ['Housed in loose house or cubicles or slats or straw bedding during dry period and moved to cubicle house once calved',
                    'cubicles cleaned daily and lime put on mats to prevent bacteria (mastitis prevention)', 'well ventilated and draft free sheds',
                    'Cows housed in loose house or slats or cubicles or straw bedding prior to calving and then turned out to grass for grazing'],
        'Nutrition': ['High quality silage (72%+ DMD) (autumn calving) and high levels of concentrates', 'pre calving minerals (lick)',
                      'High levels of good quality silage and concentrates required during peak yield and peak demand period',
                      'Turned out to grass as soon as conditions allow by day with supplementary silage (72%+ DMD) and lower amounts of concentrates required',
                      'Turned out to grass as soon as conditions allow by day', 'Mg included in spring ration to prevent grass tetany',
                      'graze high quality sward in rotational system'],
        'Production targets': ['Higher price paid for quantity of milk', 'higher yielding cows (Holstein Friesian or British Friesian or valid yield)',
                               'Quality of milk essential ‐ higher price paid for %fat and protein of the milk', 'breed with high milk solids (Jersey cross or valid example)'],
    }, 'the liquid-milk column then the creamery-milk column, pre or post calving (pre then post calving for nutrition)'),
    ('beef', 'Calf to beef v suckler beef', {
        'Housing': ['Clean straw bedded', 'well ventilated and draught free', 'penned according to age', 'isolated on arrival', 'calf hut or shelter', 'clean water supply',
                    'out on pasture', 'grouped according to size', 'slats (straw bedding)', 'space in shed 1.2 ‐ 1.5 m2 per head or adequate feeding space',
                    'space in shed 2 ‐ 2.5 m2 per head or adequate feeding space or 4m2 for straw bedding',
                    'Housed with mothers on straw bedding until turnout or creep system'],
        'Nutrition': ['Colostrum', 'milk or milk replacer or bucket fed', 'creep from 7 ‐ 10 days', 'hay (silage or straw) or scratch factor', 'grass (leader follower)',
                      'Silage (72%+ DMD)', 'concentrates (14‐16%) if necessary', 'Grass (rotational grazing)', 'concentrates (14%)', 'milk from mother',
                      'grass or named grazing system'],
        # Nineteen targets: each stage's cell is one option so the menu stays readable.
        'Production targets': ['35 ‐ 40kg at birth / weaning at 90kg / First summer 0.8kg ADG',
                               '220kg at housing / 0.6kg ADG / 320kg at turnout / Second summer 0.8 ‐1.2kg ADG',
                               '550kg at housing / 0.8‐1.2kg ADG / 550 ‐ 650 kg at slaughter',
                               '40‐55kg at birth / First summer 1.2kg ADG / 300kg at weaning',
                               '0.7kg ADG / 400 kg at turnout / Second summer 1‐1.2kg ADG',
                               '550‐600 kg at housing / 1 ‐ 1.2 kg ADG / 650 ‐ 750 kg cattle'],
    }, 'the calf-to-beef column (birth to first winter, first to second winter, second winter to slaughter) then what the suckler-beef column adds'),
    ('lamb', 'Mid-season lamb v early lamb', {
        'Housing': ['Ewes housed 8 weeks prior to lambing in pens according to number of lambs they are carrying', 'housed on clean straw bedding or slats',
                    'triplets are housed close to singles for ease of fostering',
                    'Ewes and lambs are put into single pens for bonding then into hardening off pens prior to letting out to the field',
                    'Ewes and lambs not let out after lambing ‐ housed indoors until slaughter for the Easter market', 'housed in single pens at lambing',
                    'moved to hardening off pens'],
        'Nutrition': ['Ewes are steamed up prior to lambing (0.1kg 7 weeks from lambing to 0.7kg at lambing, split in two feeds)', 'good quality silage (75%+ DMD)',
                      'mineral lick (nutrient bucket)', 'Lambs get colostrum, milk and turnout to grass and creep fed concentrates',
                      'ewe have grass only after a few weeks of concentrate feeding', 'Lambs get colostrum, milk concentrates (high levels) and silage',
                      'ewes on silage and concentrates'],
        'Production targets': ['Ewes BCS 3.5 at mating and 3 at lambing', 'Aim to have 1.8 lambs weaned per ewe', 'finish in 16 weeks at liveweight of 42kg (KO 21kg)',
                               'Aim to have weaning rate of 1.7 lambs per ewe',
                               'target finishing weight 42 kg (KO 21kg) in 12‐ 14 weeks or for higher priced Easter market'],
    }, 'the mid-season-lamb column then the early-lamb column, pre then post lambing'),
]
BREEDS = [
    ('pig', 'Pig', ('Landrace', ['excellent ham', 'high carcase weight', 'good milk production', 'high prolificacy', 'good conformation']),
     ('Large white', ['high growth rate', 'high lean meat %', 'good terminal sires', 'good uniformity of pigs', 'prolific', 'good at converting feed', 'good conformation'])),
    ('poultry', 'Poultry', ('Rhode island red', ['hardy breed', 'produce well on marginal feed', 'lay 200 to 300 eggs per year (prolific)', 'produce large eggs',
                                                 'eggs pale brown colour (market demands)', 'produce medium weight eggs']),
     ('White leghorn', ['lay 280 to 320 eggs per year (very prolific)', 'produce white eggs', 'produce heavy eggs',
                        'can withstand cold conditions (ideal for free range or organic enterprises)'])),
    ('horse', 'Horse', ('Irish sport horse', ['athleticism', 'jumping ability', 'courage', 'intelligence', 'soundness']),
     ('Irish draught horse', ['versatile', 'powerful stride', 'athletic animal', 'excellent conformation quality'])),
]
TBC_SCC = ['Lime on cubicles (to kill bacteria under the cows udder)', 'change liners of clusters in milking parlour regularly (twice a year)', 'cool milk to <4oC as quickly as possible', 'add plate cooler',
           'milk filters (to reduce amount of debris in milk)', 'teat dipping (pre and post milking) (to kill any bacteria present on or in the cow’s teats)',
           'dry cow therapy (teat seals) (to kill any bacteria in udder)(prevent bacteria from entering the udder)',
           'clipping of cows tail (to keep the teats and udder clean)', 'washing and drying udder prior to milking (to remove any excess dirt)',
           '(hot) washing milking parlour or bulk tank (with dump temperature above 50oC) (to kill any bacteria in milk lines (without use of chlorine based sterilising products which can leave trichloromethane ‐ TCM residue)',
           'milk infected cows last to stop transfer of bacteria to other cows (disinfect clusters)',
           'cull persistently infected cows or older cows with high SCC (identified by milk recording) (to prevent disease being passed to other cows)',
           'to identify cows with cell count (clinical or sub‐clinical) ‐ withhold milk from infected cows',
           'clean, dry bedding (straw) in dry cow house (to reduce amount of bacteria cow is exposed to)',
           'dry cow antibiotics (teat seal) (to kill any bacteria present over a period of time) (prevent bacteria from entering the teat)',
           '‘strip’ fore milk to detect any signs of clinical mastitis and treat cow with antibiotics']
RESAZURIN = ['Place equal amounts of one milk sample into a number of sterile containers', 'test samples (average) immediately',
             'leave the other samples to test over time – (e.g. test at 5 hours, 24 hours, 48 hours, 72 hours )', 'Add (1 cm3) of Resazurin to samples',
             'place in water bath at 37oC for 15 minutes', 'record colour of samples',
             'result (State at least two colours and corresponding conclusion from: Fresh – blue – good quality (low TBC) / Blue – deep mauve = good / Deep pink = fair / Light pink = poor / White = poor']
PLATE_COUNT = ['Carry out a serial dilution of one milk sample by adding 1ml of milk into 9ml of sterile water and shake to mix. Then take 1ml from this test tube and add to 9ml of sterile water and shake. Repeat this for 4 more test tubes.',
               'take 1ml of milk from the last test tube and place on a prepared nutrient agar plate under aseptic conditions. Repeat this 3 times for accurate results',
               'spread the milk around the plate using a plate spreader', 'leave one agar plate unopened as a control.', 'place in incubator for 72 hours at 25oC.',
               'remove plate and record number of bacteria colonies on the plate and multiply by 106 to get the number of CFU’s / ml of milk.',
               'repeat steps 2 ‐ 6 from same milk sample (e.g. at 5 hours, 24 hours, 48 hours, 72 hours) to determine the quality of a sample of milk over time',
               'Result: There will be an increase in CFU’s over ‐ time as the number of bacteria in the sample multiply causing a decrease in quality of the milk.']
OTHER_TESTS = ('The scheme adds: "There are other valid tests a student could also do ‐ % protein / % butterfat (Gerber method) / presence of thermoduric bacteria (serial dilution) / '
               'presence of antibiotics (Devlo test) / SCC ‐ Califormia Mastitis Test (CMT) / % Solids in a milk sample (excess water)" and "Points may be presented on a labelled diagram".')
PRESERVATION = [
    ('grain', 'Grain crops (e.g. barley)', ['Crops should have certain moisture content at harvest (e.g. Barley ~ 15%) ‐ otherwise seeds will heat and germinate and spoil ‐ may need drying after harvest or suitable storage (ventilation, cool conditions) for preservation',
                                            'acid treatment (or crimping) to prevent germination of seed for long term storage of feed (throughout the winter) or treated with sprouting inhibitor',
                                            'control of vermin to prevent losses or damage to crop']),
    ('potatoes', 'Potatoes', ['Harvest in dry conditions to prevent rot', 'store in darkness or cool conditions or frost free or well ventilated to prevent spoilage and losses',
                              'vermin free to prevent spoilage and losses', 'sprout inhibitor to prevent losses', 'remove damaged tubers to prevent spoilage']),
    ('grass', 'Grass (silage or hay)', ['Fermentation of grass (lactobacillus bacteria feed off the sugars in the grass) to produce lactic acid which decreases the pH to 4 ‐ fermentation process to preserve the grass (silage) ‐ leads to increased DMD of the silage or palatability',
                                        'dehydration (hay) reduces moisture content below 20% preventing spoilage (or loss)',
                                        'cut in afternoon or double chop or leafy grass for increased sugar or wilting grass to increase sugar or reduces nitrates for DMD or palatability',
                                        'airtight silage pit (or bales) to ensure anaerobic conditions to prevent spoilage (or loss)',
                                        'additive to promote fermentation for high DMD or palatability']),
]
ROLES = ['forms enzymes or assists in formation of plant proteins', 'closely associated with N uptake or efficiency', 'formation of cell walls or cell membranes',
         'helps capture sun’s energy for photosynthesis', 'part of chlorophyll (molecule)', 'helps to activate specific enzyme systems',
         'main component of chlorophyll which traps light in photosynthesis', 'main component of amino acids or protein', 'leafy growth']
FERTILISER_ADVICE = ['Applying FYM provides more DM per ha compared to slurry', 'lower amounts slurry provide more DM than high amounts',
                     'higher amounts of FYM provide more DM than lower amounts until March', 'to ensure high DM in March apply any organic fertiliser in autumn',
                     'high slurry shows limited impact on DM availability in March']
GRAPH = 'agsci-2021-hl-paper-organic-fertiliser-dm-graph'
GRAPH_STEM = ('The following is a graph of the student’s results showing the total available dry matter (DM) over a five month period following the application of the '
              'organic fertiliser in the autumn. Analyse the graph and answer the questions which follow.')


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='higher', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 53)), schemePagesInspected=list(range(1, 40)),
                selectionDirectives=observed, supplementarySelections=supplementary,
                sourceNotes=[dict(questionN='14', questionRef='Q14(a)', note='Scheme PDF pages 22 to 24 price each heading 4+2 and answer it from three stage tables (liquid v creamery milk, calf to beef v suckler beef, mid-season v early lamb) and "Other valid comparisons".'),
                             dict(questionN='15', questionRef='Q15(b)(ii)', note='Scheme PDF page 29 accepts two calculations (from each treatment\'s own November value, or from the November control value for both) and awards marks "based on the answer given by candidate in part (i)".')],
                independentBoundaryReview='106 base tasks, one card each (Q13(a)(iii) keeps its name and advantages boundaries; Q14(a) and Q18(a) are carded by printed heading). 71 original cards match a published boundary and tariff unchanged. 30 are corrected in place (Q1(b), Q3(a)(i), Q3(a)(ii), Q3(a)(iii), Q3(b)(ii), Q3(b)(iii), Q4(c), Q5(a), Q5(b), Q5(c), Q6(b)(ii), Q9(a), Q9(c), Q10(a), Q10(c), Q11(b)(ii), Q14(b)(i), Q14(b)(ii), Q14(c)(ii), Q14(c)(iii), Q15(a)(i), Q15(a)(ii), Q15(b)(i), Q15(b)(iii), Q15(b)(iv), Q16(a)(iii), Q16(b), Q17(b)(i), Q17(b)(iv), Q18(a) Crop preservation); five cards are added for the missing Q14(a) Housing, Nutrition and Production targets, Q15(b)(ii) and Q16(a)(i).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


def atlas_for(ref):
    match = re.match(r'(Q\d+)((?:\([a-z]+\))*)', ref)
    parts = re.findall(r'\([a-z]+\)', match.group(2))
    for n in range(len(parts), -1, -1):
        key = match.group(1) + ''.join(parts[:n])
        if key in ATLAS:
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
        t = dict(questionRef='2021 HL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: str(1001 + len(tasks))}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 52 paper and 39 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2021 HL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'
        if cid in snapshot:
            assert original_hash(card) == snapshot[cid]['originalSha256']
            RESTORED.append(card)

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2021 Higher — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2021 Higher Level examination paper — © State Examinations Commission.',
                    presentationNote='Open the original page for the published wording, photographs, tables and examination context.')

    def record(cid, t, reason):
        old = originals[cid]
        corrections[cid] = dict(originalSha256=original_hash(old), originalQuestionRef=old['questionRef'],
                                originalQuestionText=old['questionText'], originalTotalMarks=old['totalMarks'],
                                originalTariffModel=old['tariffModel'], reason=reason)
        t['originalCard'] = 'corrected-in-place'

    def add(key, ref, topic, concept, question, rows, stem=None, marks=None, tariff=None, selection=None, figure=None, extra_fields=None):
        cid = PREFIX + key
        assert cid not in originals, f'{cid} would replace an original card without a correction record'
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        pp, _ = REGIONS[ref]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='higher',
                    section='A' if int(re.match(r'Q(\d+)', ref).group(1)) <= 12 else 'B', questionRef='2021 HL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + topic],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff or {'kind': 'fixed'}, sourceMaterial=source(ref, pp))
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if extra_fields: card.update(extra_fields)
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None, selection=None):
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2021 HL ' + ref, (cid, card['questionRef'])
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

    def pool(key, ref, options, steps, notation, note, page, scheme_page, wording, problem, open_list=False, changes=None):
        old = originals[PREFIX + key]
        row = menu(options, steps, note)
        if open_list:
            row['openList'] = True
        return fix(key, ref, dict(rows=[row], tariffModel={'kind': 'fixed', 'notation': notation}, **(changes or {})), drop=('notes',),
                   correction=(f'Visually verified paper PDF page {page} and scheme PDF page {scheme_page} ({wording}, "{notation}"). {problem} '
                               f'Same ID, boundary and {old["totalMarks"]} marks; one row lists every published point.'))

    def routes(built):
        """built: [(slug, label, rows)] -> (first route's rows, answerVariants)."""
        variants = [dict(id=slug, label=label, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]) for slug, label, rows in built]
        return variants[0]['rows'], variants

    def reworded(key, row_index, old_text, new_text):
        rows = copy.deepcopy(originals[PREFIX + key]['rows'])
        assert rows[row_index]['verbatim'] == old_text, (key, rows[row_index]['verbatim'])
        rows[row_index]['verbatim'] = new_text
        return rows

    # Section A ---------------------------------------------------------------
    keep('q1a', 'Q1(a)')
    old = originals[PREFIX + 'q1b']
    fix('q1b', 'Q1(b)', dict(
        rows=[point(old['rows'][0]['verbatim'], None, 'The scheme prints "2, 1+1": "Definition of one of annual or biennial for 2 and two marks for the other with a named example". ' + PAGE4),
              point(old['rows'][1]['verbatim'], None),
              dict(point('Some examples: ‐ Barley, Wheat, Oats, Peas, Beans, Maize or other valid example.', None, 'The scheme\'s annual examples; its biennial examples are accepted too.'),
                   kind='alt', accepts=['Some examples: ‐ Potatoes, Ragwort, Sugar beet, Carrots, Kale, Italian Ryegrass or other valid example.'])],
        tariffModel={'kind': 'orderedSplit', 'notation': '2 + 1 + 1'}), drop=('stem', 'notes'),
        correction=('Visually verified paper PDF page 3 ("Using a named example, other than the plants shown at part (a) above, distinguish between annual and biennial lifecycles.") and scheme PDF page 11 '
                    '("Definition of one of annual or biennial for 2 and two marks for the other with a named example", "2 1+1") with its PDF page 4 rule. '
                    'The original pinned the 2 marks to the annual definition, so a biennial definition given first earned 1, and its stem named the three plants that part (a) asks the student to identify. '
                    'Same ID, boundary, figure and 4 marks; the first definition earns 2 and the other definition and the example 1 each.'))
    for k, ref in [('q2ai', 'Q2(a)(i)'), ('q2aii', 'Q2(a)(ii)'), ('q2aiii', 'Q2(a)(iii)'), ('q2bi', 'Q2(b)(i)'), ('q2bii', 'Q2(b)(ii)'), ('q2biii', 'Q2(b)(iii)')]:
        keep(k, ref)
    sign = 'Answer either (a) or (b). (a) The following is an example of a farm safety notice displayed at the entrance to a farm.'
    fix('q3ai', 'Q3(a)(i)', dict(stem=sign),
        correction=('Visually verified paper PDF page 6 ("The following is an example of a farm safety notice displayed at the entrance to a farm. (i) State the meaning of symbols A and B on the sign.") and scheme PDF page 12 (A 2, B 2). '
                    'The original stem was the sign\'s text run together with the next page\'s "Or" ("Farm Safety Notice No unauthorised persons ... THINK SAFETY FIRST! Or"). Same ID, rows, figure, boundary and 4 marks; the stem is the paper\'s lead-in.'))
    fix('q3aii', 'Q3(a)(ii)', dict(stem='Answer either (a) or (b).'),
        correction=('Visually verified paper PDF page 6 ("(ii) State the function of C and D.", photographs C and D) and scheme PDF page 12 (C 2, D 2). '
                    'The original stem was the safety sign\'s text run together with "Or", which has nothing to do with C and D. Same ID, rows, figure, boundary and 4 marks; the stem is the paper\'s instruction.'))
    pool('q3aiii', 'Q3(a)(iii)', ['Castrate male animals on the farm to prevent unwanted breeding (of poor performing animals)', 'bloodless castration or tail docking reduces risk of infection',
                                  'removes requirements for keeping bulls on farm', 'limited market for bull beef'], [2], '2', 'One advantage, 2 marks.',
         6, 12, '"In relation to picture C at part (ii) above, state one advantage of using this piece of equipment to enhance sustainability of the farm", four advantages',
         'The original left out "bloodless castration or tail docking reduces risk of infection" and its stem was the safety sign\'s text run together with "Or".',
         changes=dict(stem='Answer either (a) or (b).'))
    keep('q3bi', 'Q3(b)(i)')
    pool('q3bii', 'Q3(b)(ii)', ['Decreased compaction (due to increased surface area)', 'less damage to soil structure', 'can travel on wet land or better floatation',
                                'reduced risk of tractor turning over on steep hillsides or better stability', 'machine capable of pulling heavier loads'], [2], '2', 'One advantage, 2 marks.',
         7, 13, '"Suggest one advantage of using a tractor fitted with tracks", five advantages', 'The original left out "can travel on wet land or better floatation".')
    pool('q3biii', 'Q3(b)(iii)', ['Reduces water run‐off', 'reduces sediment loss', 'increases soil organic matter (C sink)', 'improved soil structure or reduces compaction',
                                  'fewer number of passes leads to less emissions'], [2], '2', 'One way, 2 marks.',
         7, 13, '"State one way machine A can enhance environmental sustainability", five ways', 'The original left out "improved soil structure or reduces compaction".')
    keep('q3biv', 'Q3(b)(iv)')
    keep('q4a', 'Q4(a)')
    keep('q4b', 'Q4(b)')
    pool('q4c', 'Q4(c)', ['Plant more trees or hedges (around the farmyard) to increase biodiversity or shelterbelts',
                          'sow wild flowers (on bank beside the shed) for pollinators (or biodiversity) or create a wildlife pond',
                          'cover the collecting yard to prevent any run‐off when raining (bales on concrete)', 'cover the open lagoon to avoid it filling up quickly and becoming diluted',
                          'water harvesting to reduce water consumption', 'install bird boxes', 'install bat boxes', 'install insect hotels increase biodiversity',
                          'any energy saving measure that a student has not given as an answer to part (a)', 'pit silage instead of bales to reduce plastic waste'],
         [2, 2], '2(2)', 'Any two ways, 2 marks each (2(2)). The scheme adds "Cannot give the same answer to part (a)".',
         8, 13, '"Apart from your answer to part (a) above, suggest two ways in which the farmer could make the farmyard more environmentally sustainable", ten ways',
         'The original left out the first published way, planting more trees or hedges.')
    crop_labels = [label for _, label, *_ in CROPS]
    crop_stem = 'In relation to a catch crop or energy crop you have studied answer the following questions. Name of chosen crop.'
    rows, built = routes([(slug, label, [menu(a, [2, 2], f'{label}: any two ways, 2 marks each (2(2)). No marks for the name of the crop. {CROP_OPEN}')]) for slug, label, a, _, _ in CROPS])
    fix('q5a', 'Q5(a)', dict(rows=rows, answerVariants=built), drop=('notes',), selection=closed(1, crop_labels),
        correction=('Visually verified paper PDF page 9 ("In relation to a catch crop or energy crop you have studied", "Describe two ways in which the production of your chosen crop contributes to sustainability") and scheme PDF page 14 '
                    '(separate kale or stubble turnip, oilseed rape and Miscanthus pools, "2(2)"). The original rows were two kale points with every oilseed rape and Miscanthus point mixed into their accepted wordings, so points from different crops could be combined. '
                    'Same ID, boundary and 4 marks; each crop the scheme answers for is an answer route the student chooses before reveal, listing every published point, any two at 2 marks.'))
    rows, built = routes([(slug, label, [menu(b, [2], f'{label}: one damage, 2 marks. No marks for naming the pest. {CROP_OPEN}')]) for slug, label, _, b, _ in CROPS])
    fix('q5b', 'Q5(b)', dict(rows=rows, answerVariants=built), drop=('notes',), selection=closed(1, crop_labels),
        correction=('Visually verified paper PDF page 9 ("Describe the damage caused by a named pest to your chosen crop.", a Named pest line) and scheme PDF page 14 '
                    '(separate kale or stubble turnip, OSR and Miscanthus pests, 2). The original row was the kale flea beetle with every other crop\'s pest mixed into its accepted wordings. '
                    'Same ID, boundary and 2 marks; each crop is an answer route the student chooses before reveal, listing every published damage.'))
    rows, built = routes([(slug, label, [point(c[0], 2, f'{label}: the first growth stage, 2 marks. {CROP_OPEN}'), point(c[1], 2, 'The second growth stage, 2 marks.')])
                          for slug, label, _, _, c in CROPS])
    fix('q5c', 'Q5(c)', dict(rows=rows, answerVariants=built), drop=('notes',), selection=closed(1, crop_labels),
        correction=('Visually verified paper PDF page 9 ("Describe the first two growth cycle stages of your chosen crop.") and scheme PDF page 15 (kale or stubble turnip, OSR and Miscanthus stages, "2(2)"). '
                    'The original rows were the kale stages with the oilseed rape and Miscanthus stages mixed into their accepted wordings. '
                    'Same ID, boundary and 4 marks; each crop is an answer route the student chooses before reveal, with its own two published stages at 2 marks each.'))
    for k, ref in [('q6ai', 'Q6(a)(i)'), ('q6aii', 'Q6(a)(ii)'), ('q6aiii', 'Q6(a)(iii)'), ('q6bi', 'Q6(b)(i)')]:
        keep(k, ref)
    fix('q6bii', 'Q6(b)(ii)', dict(rows=reworded('q6bii', 1, 'more recycling of organic matter through crop presence and animal manures',
                                                  'stripping of nutrients or straw removal leads to less organic matter (more recycling of organic matter through crop presence and animal manures)')),
        correction=('Visually verified paper PDF page 11 ("Compare two effects of continuous tillage and permanent grassland on the soil organic matter content.") and scheme PDF page 15 '
                    '("...(increased organic matter) / stripping of nutrients or straw removal leads to less organic matter (more recycling of organic matter through crop presence and animal manures)", "2(2)"). '
                    'The original second point kept only the bracketed grassland half, dropping the tillage effect it compares. Same ID, boundary and 4 marks.'))
    keep('q6biii', 'Q6(b)(iii)')
    for k, ref in [('q7a', 'Q7(a)'), ('q7b', 'Q7(b)'), ('q7c', 'Q7(c)'), ('q8a', 'Q8(a)'), ('q8b', 'Q8(b)'), ('q8c', 'Q8(c)')]:
        keep(k, ref)
    fix('q9a', 'Q9(a)', dict(rows=reworded('q9a', 0, 'Animals or plants selected based on their DNA (or genetic material)',
                                            'Animals or plants selected based on their DNA (or genetic material) examined and compared to reference data.')),
        correction=('Visually verified paper PDF page 14 ("Explain genomic selection.") and scheme PDF page 17 ("Animals or plants selected based on their DNA (or genetic material) examined and compared to reference data.", 2). '
                    'The original answer stopped at "(or genetic material)". Same ID, boundary and 2 marks.'))
    keep('q9b', 'Q9(b)')
    fix('q9c', 'Q9(c)', dict(rows=reworded('q9c', 0, 'Farmer identifies trait (double muscle, udder, sound feet, conformation, good mouth, polled )',
                                            'Farmer identifies trait (double muscle, udder, sound feet, conformation, good mouth, polled ) then the farmer (selectively, deliberately) breeds from these (superior) animals (to achieve superior offspring)')),
        correction=('Visually verified paper PDF page 14 ("Describe how farmers have made genetic improvements in their animal enterprise based on physical traits of their animals.") and scheme PDF page 17 '
                    '("Farmer identifies trait (...) then the farmer (selectively, deliberately) breeds from these (superior) animals (to achieve superior offspring)", 2). '
                    'The original answer stopped after the list of traits, leaving out the breeding step that the question asks for. Same ID, boundary and 2 marks.'))
    keep('q9d', 'Q9(d)')
    fix('q10a', 'Q10(a)', dict(rows=reworded('q10a', 0, 'AP ‐ food produced in microenterprise with unique characteristics',
                                              'AP ‐ food produced in microenterprise with unique characteristics (usually handmade with a distinctive flavour)')),
        correction=('Visually verified paper PDF page 15 ("Distinguish between artisan produce and a niche market.") and scheme PDF page 17 ("AP ‐ food produced in microenterprise with unique characteristics (usually handmade with a distinctive flavour)", 2 + 2). '
                    'The original artisan-produce answer stopped at "unique characteristics". Same ID, boundary and 4 marks.'))
    keep('q10b', 'Q10(b)')
    fix('q10c', 'Q10(c)', dict(
        stem='The Murphy family operate one of Ireland’s sheep dairy farms in Co. Galway. They produce artisan products for a niche market.',
        questionText='Compare the composition of sheep’s milk shown in the pie chart to your knowledge of cow’s milk in relation to the water content.',
        figureKey='agsci-2021-hl-paper-sheep-milk-pie'),
        correction=('Visually verified paper PDF page 15 ("Compare the composition of sheep’s milk shown in the pie chart to your knowledge of cow’s milk in relation to the water content.", the Sheep Milk Composition pie chart) and scheme PDF page 17 (2). '
                    'The original rewrote the question as "given above" and replaced the chart with a description. Same ID, rows, boundary and 2 marks; the question is the paper\'s wording with the chart cropped from the paper.'))
    for k, ref in [('q11ai', 'Q11(a)(i)'), ('q11aii', 'Q11(a)(ii)'), ('q11aiii', 'Q11(a)(iii)'), ('q11bi', 'Q11(b)(i)')]:
        keep(k, ref)
    disorder_open = 'No marks for naming the disorder; points must match the disorder named. The scheme introduces bloat and acidosis with "e.g.".'
    rows, built = routes([
        ('bloat', 'Bloat', [point('Symptoms — Bloat ‐ gas build up in rumen and (left side of the) abdomen becomes distended (swollen)', 2, 'Symptoms, 2 marks. ' + disorder_open),
                            menu(['antacid or antifoaming solution', 'tube inserted through mouth to release gas',
                                  'insert a trocar and canula (into the rumen) or trocar is removed and canula remains to allow gas escape'], [2], 'Treatment: any one, 2 marks.'),
                            menu(['Limit amount of time spent grazing in early spring or provide additional fibre (silage)', 'antifoaming treatment in the water',
                                  'limit grazing on high clover swards'], [2], 'Prevention: any one, 2 marks.')]),
        ('acidosis', 'Acidosis', [point('Symptoms — Acidosis ‐ rumen stops moving leading to loss in appetite due to high levels of lactic acid produced', 2, 'Symptoms, 2 marks. ' + disorder_open),
                                  point('Treatment — Acidosis ‐ dose with bicarbonate (bread soda) solution or magnesium oxide solution to neutralise the pH in the rumen', 2, 'Treatment, 2 marks.'),
                                  menu(['ensure adequate fibre fed especially on high concentrate diets', 'increase concentrate feeding levels gradually'], [2], 'Prevention: any one, 2 marks.')])])
    fix('q11bii', 'Q11(b)(ii)', dict(rows=rows, answerVariants=built), drop=('notes',), selection=closed(1, ['Bloat', 'Acidosis']),
        correction=('Visually verified paper PDF page 17 ("Briefly describe a named disorder of the ruminant digestive system under the following headings.", Named disorder, Symptoms, Treatment and Prevention lines) and scheme PDF page 19 '
                    '("Points must match disorder named", bloat and acidosis answers under each heading, 2 + 2 + 2). The original rows were bloat answers with the acidosis answers as accepted alternatives on each heading, so a bloat symptom could be combined with an acidosis treatment. '
                    'Same ID, boundary and 6 marks; each disorder is an answer route the student chooses before reveal, with its own symptom, treatment and prevention.'))
    for k, ref in [('q12a', 'Q12(a)'), ('q12b', 'Q12(b)'), ('q12c', 'Q12(c)'), ('q12d', 'Q12(d)')]:
        keep(k, ref)
    # Section B ---------------------------------------------------------------
    for k, ref in [('q13ai', 'Q13(a)(i)'), ('q13aii', 'Q13(a)(ii)'), ('q13aiii-name', 'Q13(a)(iii) Name'), ('q13aiii-adv', 'Q13(a)(iii) Advantages'),
                   ('q13aiv', 'Q13(a)(iv)'), ('q13av', 'Q13(a)(v)'), ('q13b', 'Q13(b)'), ('q13c', 'Q13(c)')]:
        keep(k, ref)
    system_labels = [label for _, label, _, _ in SYSTEMS]
    compare = ('Compare two different systems of animal production for a chosen livestock enterprise under the following headings at an identified stage in the animal’s production cycle. ')
    for key, heading, concept in [('q14a-housing', 'Housing', 'comparing-production-systems-housing'), ('q14a-nutrition', 'Nutrition', 'comparing-production-systems-nutrition'),
                                  ('q14a-production-targets', 'Production targets', 'comparing-production-systems-targets')]:
        built = []
        for slug, label, cells, order in SYSTEMS:
            row = menu(cells[heading], [4, 2], f'{label}, {heading.lower()}: the first correct point 4 marks and the next 2 (4+2). {PAGE4} '
                                               f'In order the options are {order}. No marks for naming the systems; answers must match the named stage. '
                                               'The scheme adds "Other valid comparisons".')
            row['openList'] = True
            built.append((slug, label, [row]))
        rows, variants = routes(built)
        add(key, 'Q14(a) ' + heading, '4-3-3', concept, compare + heading + ':', rows, 'The paper prints a table for the name of each production system (1 and 2) and the identified stage of the production cycle.',
            tariff={'kind': 'fixed', 'notation': '4+2'}, selection=closed(1, system_labels), extra_fields={'answerVariants': variants})
    fix('q14bi', 'Q14(b)(i)', {}, drop=('stem',),
        correction=('Visually verified paper PDF page 27 ("(b) (i) Identify each of the following cattle and sheep breeds.", photographs A–D) and scheme PDF page 25 (A Suffolk, B Shorthorn, C Belgian blue, D Texel, "4(1)"). '
                    'The original stem was debris from the next part\'s table ("1. 2. Name of breed"). Same ID, rows, figure, label key, boundary and 4 marks; the stem is removed.'))
    built = []
    for slug, label, (first, first_traits), (second, second_traits) in BREEDS:
        a = menu(first_traits, [2, 1], f'{label}: the scheme\'s first breed is {first}. Two characteristics, 2 for the first and 1 for the second (2+1). No direct marks for naming the breeds.')
        b = menu(second_traits, [2, 1], f'The scheme\'s second breed is {second}. Two characteristics, 2 for the first and 1 for the second (2+1). The scheme adds "Or other valid names and associated valid characteristics".')
        a['openList'] = b['openList'] = True
        built.append((slug, label, [a, b]))
    rows, variants = routes(built)
    fix('q14bii', 'Q14(b)(ii)', dict(rows=rows, answerVariants=variants, tariffModel={'kind': 'fixed', 'notation': '2(2+1)'}), drop=('notes',),
        selection=closed(1, [label for _, label, *_ in BREEDS]),
        correction=('Visually verified paper PDF page 27 ("In relation to two named breeds of pig or horse or poultry that you have studied, compare two characteristics of each breed which make them suitable for intensive production.") '
                    'and scheme PDF page 25 (Landrace and Large white, "OR" Rhode island red and White leghorn, "OR" Irish sport horse and Irish draught horse, each "2(2+1)"). '
                    'The original mixed every species\' characteristics into four positional rows, so a pig characteristic could be combined with a poultry one, and it left out "good terminal sires". '
                    'Same ID, boundary and 6 marks; each species is an answer route the student chooses before reveal, with each breed\'s characteristics at 2+1.'))
    keep('q14biii', 'Q14(b)(iii)')
    keep('q14ci', 'Q14(c)(i)')
    for key, ref, index, old_text, new_text, page in [
            ('q14cii', 'Q14(c)(ii)', 1, 'Conclusion: heifer has extensive lung damage as a result of — pneumonia (viral / bacterial infection) ‐ lung lesions result in reduced performance of the animal',
             'Conclusion: heifer has extensive lung damage as a result of pneumonia (viral / bacterial infection) ‐ lung lesions result in reduced performance of the animal', 27),
            ('q14ciii', 'Q14(c)(iii)', 0, 'There is a lot of liver damage across the age of cattle on the farm — and the lung health is better for the majority of cattle',
             'There is a lot of liver damage across the age of cattle on the farm and the lung health is better for the majority of cattle', 27)]:
        fix(key, ref, dict(rows=reworded(key, index, old_text, new_text)), drop=('notes',),
            correction=(f'Visually verified paper PDF page 29 and scheme PDF page {page} ("{new_text}"). The original inserted a dash the scheme does not print into the middle of the sentence. Same ID, boundary and marks.'))
    keep('q14civ', 'Q14(c)(iv)')
    for key, ref, index, old_text, new_text in [
            ('q15ai', 'Q15(a)(i)', 0, 'Applying organic fertiliser in autumn will increase grass yield — (DM%), earthworm population and spring nutrient availability',
             'Applying organic fertiliser in autumn will increase grass yield (DM%), earthworm population and spring nutrient availability'),
            ('q15aii', 'Q15(a)(ii)', 1, 'Dependent: grass DM% and earthworm population and spring soil — nutrient availability',
             'Dependent: grass DM% and earthworm population and spring soil nutrient availability')]:
        fix(key, ref, dict(rows=reworded(key, index, old_text, new_text)), drop=('notes',),
            correction=(f'Visually verified paper PDF page 31 and scheme PDF page 28 ("{new_text}"). The original inserted a dash the scheme does not print into the middle of the answer. Same ID, boundary and marks.'))
    for k, ref in [('q15aiii', 'Q15(a)(iii)'), ('q15aiv', 'Q15(a)(iv)'), ('q15av', 'Q15(a)(v)')]:
        keep(k, ref)
    graph_problem = 'The original stem was the chart\'s axis labels and legend run together ("800 1000 1200 ... Control treatment calculations") with no chart.'
    fix('q15bi', 'Q15(b)(i)', dict(stem=GRAPH_STEM, figureKey=GRAPH),
        correction=(f'Visually verified paper PDF page 33 (the (b) lead-in, the bar chart and "(i) Identify which treatment is the most beneficial organic fertiliser for a steady supply of herbage over the five month period.") and scheme PDF page 29 ("FYM ‐ High", 3). '
                    f'{graph_problem} Same ID, rows, boundary and 3 marks; the stem is the paper\'s lead-in and the chart is cropped from the paper.'))
    solutions = [('solution-1', 'Solution 1: each treatment\'s own November value', '3700 – 1400 = 2300 kg DM / ha', '3400 – 1000 = 2400 kg DM / ha',
                  'There will be 2300 kg DM in the FYM high treatment compared to the control treatment which gives 2400 kg DM /ha'),
                 ('solution-2', 'Solution 2: the November control value for both', '3700 – 1000 = 2700 kg DM / ha', '3400 – 1000 = 2400 kg DM / ha',
                  'There will be 2700 kg DM in the FYM high treatment compared to the control treatment which gives 2400 kg DM/ha')]
    rows, variants = routes([(slug, label, [point(a, None, 'Most beneficial treatment (FYM high). The scheme prints 3+2: "Marks awarded for correct calculation based on the answer given by candidate in part (i)". ' + PAGE4),
                                            point(b, None, f'Control treatment. The scheme\'s conclusion: "{conclusion}".')])
                             for slug, label, a, b, conclusion in solutions])
    add('q15bii', 'Q15(b)(ii)', '3-2', 'increase-in-herbage-against-control',
        'Calculate the increase in kg DM / ha of herbage over the five month period for the treatment you have identified at part (i) above compared to the increase in the control treatment.',
        rows, GRAPH_STEM, marks=5, tariff={'kind': 'orderedSplit', 'notation': '3+2'}, selection=closed(1, [label for _, label, *_ in solutions]),
        figure=GRAPH, extra_fields={'answerVariants': variants})
    fix('q15biii', 'Q15(b)(iii)', dict(stem=GRAPH_STEM, figureKey=GRAPH),
        correction=(f'Visually verified paper PDF page 34 ("A beef farmer wants to have early spring grass for his spring calving herd to turnout in late February...") with the chart on PDF page 33, and scheme PDF page 29 (4). '
                    f'{graph_problem} Same ID, rows, boundary and 4 marks; the stem is the paper\'s lead-in and the chart is cropped from the paper.'))
    pool('q15biv', 'Q15(b)(iv)', FERTILISER_ADVICE, [2, 2, 2], '3(2)',
         'Any three recommendations, 2 marks each (3(2)). The scheme adds "All statements above must be backed up by relevant evidence from graph".',
         34, 29, '"Your advice should include at least three specific recommendations", five recommendations',
         f'The original listed three of the five recommendations as notation "3 at 2 marks each". {graph_problem}', changes=dict(stem=GRAPH_STEM, figureKey=GRAPH))
    add('q16ai', 'Q16(a)(i)', '4-3-2', 'comparing-milk-payments', 'Calculate which farmer (Dan or Joe) earns a higher price for their milk.',
        [point('Total = 15,558.64', None, 'Dan’s calculation (marks given for totals underlined): 1803 X 5.48 = 9880.44; 2292 X 3.35 = 7678.20; 50,000 x 0.04 = 2000. '
                                          'The scheme prints (4,2,0) for the totals: "*4m for correct totals, deduct 2m if method correct but totals incorrect".', kind='criterion'),
         point('Total = 14,146', None, 'Joe’s calculation: 9316 + 6830 ‐ 2000 =14,146.', kind='criterion'),
         point('Higher Price ‐ Dan', None, 'Higher price: 2 marks.')],
        'Answer both (a) and (b) with either (c) or (d). (a) Two dairy farmers (Dan and Joe) are comparing the amount of money they are getting paid for their milk. Analyse the data in the table and answer the questions which follow.',
        marks=6, tariff={'kind': 'questionTotal', 'notation': '(4, 2, 0) + 2'}, figure='agricultural-science-2021-HL-paper-p35-i1')
    keep('q16aii', 'Q16(a)(ii)')
    pool('q16aiii', 'Q16(a)(iii)', TBC_SCC, [3, 3, 3], '3(3)',
         'Three recommendations, 3 marks each (3(3)). The scheme prints "*At least one point from each of TBC and SCC". In order the first ten options are its reducing-TBC list, two of which (lime on cubicles and teat dipping) it prints in its reducing-SCC list too, given here with the SCC list\'s reasons; the last six are the rest of its reducing-SCC list.',
         36, 30, '"Your plan should include at least three specific recommendations", ten TBC and eight SCC recommendations',
         'The original fixed its third row to teat dipping, so a third recommendation such as clipping the cow\'s tail could not be ticked.')
    resazurin = menu(RESAZURIN, [3, 3, 3, 3], 'Resazurin test: any four steps, 3 marks each (4(3)). ' + OTHER_TESTS)
    plate = menu(PLATE_COUNT, [3, 3, 3, 3], 'Or a total bacterial count: any four steps, 3 marks each (4(3)). ' + OTHER_TESTS)
    resazurin['openList'] = plate['openList'] = True
    rows, variants = routes([('resazurin', 'Resazurin test', [resazurin]), ('total-bacterial-count', 'Total bacterial count', [plate])])
    fix('q16b', 'Q16(b)', dict(rows=rows, answerVariants=variants), drop=('notes',), selection=closed(1, ['Resazurin test', 'Total bacterial count']),
        correction=('Visually verified paper PDF page 37 ("Describe, with the aid of a labelled diagram, how Joe could carry out this investigation in a school laboratory or on his farm.") and scheme PDF page 31 '
                    '(a resazurin method, "OR Joe could do a total bacterial count on the sample", "OR There are other valid tests", "4(3)"). '
                    'The original mixed resazurin and plate-count steps in the same rows and left out the plate spreader, the repeats and the plate-count result. '
                    'Same ID, boundary and 12 marks; each method is an answer route the student chooses before reveal, listing every published step, any four at 3 marks.'))
    for k, ref in [('q16ci', 'Q16(c)(i)'), ('q16cii', 'Q16(c)(ii)'), ('q16ciii', 'Q16(c)(iii)'), ('q16civ', 'Q16(c)(iv)'),
                   ('q16di', 'Q16(d)(i)'), ('q16dii', 'Q16(d)(ii)'), ('q16diii', 'Q16(d)(iii)'), ('q16div', 'Q16(d)(iv)'), ('q17a', 'Q17(a)')]:
        keep(k, ref)
    fix('q17bi', 'Q17(b)(i)', dict(
        stem=('Below is a soil index reference sheet and two sets of soil sample results. Analyse the tables of results and answer the questions that follow. '
              'Field 2 – Permanent pasture (main grazing block): Phosphorus (P) 6.42 mg/l; Potassium (K) 157 mg/l.'),
        figureKey='agsci-2021-hl-paper-reference-soil-index'),
        correction=('Visually verified paper PDF page 41 with the field 2 results on PDF page 40 (P 6.42 mg/l and K 157 mg/l, then "(i) Determine the P and K soil indexes for field 2." above the Reference Soil Index table) and scheme PDF page 33 ("P = 3 K = 4", 3). '
                    'The original stem was field 1\'s table run together ("554115 Field 1 – Permanent pasture ... Test Parameters Result Very Low ...") and the card carried no reference index to read the answer from. '
                    'Same ID, rows, boundary and 3 marks; the stem is the paper\'s lead-in with field 2\'s two results, and the reference index is cropped from the paper.'))
    for k, ref in [('q17bii', 'Q17(b)(ii)'), ('q17biii', 'Q17(b)(iii)')]:
        keep(k, ref)
    fix('q17biv', 'Q17(b)(iv)', dict(
        rows=[menu(['Sulfur', 'Calcium', 'Magnesium', 'Nitrogen'], [1, 1], 'Two other macronutrients named, 1 mark each.'),
              menu(ROLES, [3, 3], 'The role of each nutrient named, 3 marks each (3+3+1+1). In order the scheme gives sulfur two roles, calcium one, magnesium three and nitrogen three; a role must belong to the nutrient you named.')],
        tariffModel={'kind': 'fixed', 'notation': '3+3+1+1'}), drop=('stem', 'notes'),
        correction=('Visually verified paper PDF page 42 ("Some macronutrients do not appear on the table. Identify any two other macronutrients and state their role in plant growth.") and scheme PDF page 34 '
                    '(sulfur, calcium, magnesium and nitrogen with their roles, "3+3+1+1"). The original priced each nutrient and its role together at 4, so a correctly named nutrient with a wrong role earned nothing. '
                    'Same ID, boundary and 8 marks; the names earn 1 each and the roles 3 each. Its stem, which the shipped card already hid, is removed.'))
    for k, ref in [('q17bv', 'Q17(b)(v)'), ('q17bvi', 'Q17(b)(vi)'), ('q17c', 'Q17(c)'), ('q18a-soil-quality', 'Q18(a) Soil quality')]:
        keep(k, ref)
    rows, variants = routes([(slug, label, [dict(menu(items, [2, 2], f'{label}: any two points, 2 marks each (2(2)). The scheme adds "*negative effect on productivity may be accepted as alternative to points above".'), openList=True)])
                             for slug, label, items in PRESERVATION])
    fix('q18a-crop-preservation', 'Q18(a) Crop preservation', dict(rows=rows, answerVariants=variants), drop=('notes',), selection=closed(1, [label for _, label, _ in PRESERVATION]),
        correction=('Visually verified paper PDF page 44 ("Discuss the effect of each of the following on the productivity of a named crop, giving two points for each heading.", a Named Crop line and the Crop preservation heading) and scheme PDF page 35 '
                    '(three crop preservation pools separated by "OR": grain, potatoes and grass, "2(2)"). The original mixed the grain and potato points in the same rows, so points for different crops could be combined. '
                    'Same ID, boundary and 4 marks; each crop is an answer route the student chooses before reveal, listing every published point, any two at 2 marks.'))
    for k, ref in [('q18b', 'Q18(b)'), ('q18ci', 'Q18(c)(i)'), ('q18cii', 'Q18(c)(ii)'), ('q18ciii', 'Q18(c)(iii)'), ('q18civ', 'Q18(c)(iv)'),
                   ('q18cv', 'Q18(c)(v)'), ('q18cvi', 'Q18(c)(vi)'), ('q18cvii', 'Q18(c)(vii)')]:
        keep(k, ref)
    assert len(tasks) == 106 and len(corrections) == 30 and len(originals) == 101 and len(cards) == 35, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2021 Higher card must be reviewed'
    return cards, tasks, corrections
