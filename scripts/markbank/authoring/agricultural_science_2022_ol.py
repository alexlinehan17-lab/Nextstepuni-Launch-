"""2022 Ordinary review: the 95 original cards reconciled against the SEC sources.

All 40 paper pages and 28 scheme pages were inspected and the independent
census transcribed before any card was touched. 98 base tasks, one card each
(Q2(b)(ii) and Q13(b)(i) were reviewed in an earlier batch and keep their
cards and Atlas numbers). Of the 95 original cards, 71 match a published task
boundary and tariff and are left byte-identical. 19 are corrected IN PLACE,
keeping their IDs. Q4(b)'s true/false table is one task under one 5(2) tariff:
the table card keeps its ID and gains the printed statements, and the five
per-statement cards that duplicated its marks are withdrawn as progress
aliases of it. Six cards are added for the missing Q10(a), Q12(a), Q15(a)(ii),
Q16(a)(ii), Q17(b)(i) and Q17(b)(iii). Each correction records the original
wording, marks and object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024GLP000EV.pdf'
YEAR = 2022
HASHES = {'exampapers':'93a3be61e0ec5891f6ac6a2660fc1a98732fc9ff21a4b3c1e50681db1fe14194',
          'markingschemes':'cb6dac4e3b45f824dfd75bf82443d62dc807fdbbf1e5406713be32e51c22e916'}
SELECTIONS = {
    '1643a3a7f339597c':('exam-selection','Instructions: Section A, seven of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    '529e66c12bf6d0b5':('exam-selection','Instructions: Section B, three of six independent questions. Every question is retained.'),
    'b72f88947965ee17':('exam-selection','Repeated Section A instruction: seven independent 10-mark questions, all retained.'),
    'b0a438903888f617':('independent-task-selection','Q2 either (a) or (b): both independently marked alternatives are retained.'),
    'eb88a1f66c501918':('closed','Q2(a)(i): identify any three of four photographed breeds A–D, 3(2). One card: a single anyN row lists all four, claim limit three.'),
    '16084acebeb0d8b8':('closed','Q2(b)(ii): breed E or F with reasons. One card listing both breeds\' reasons, 3+1 (reviewed in an earlier batch).'),
    '20929faf270032a3':('closed','The same Q2(b)(ii) breed choice ("either breed E or F"); no further route.'),
    '1adc59f55f6c6627':('not-a-selection','"which breed to choose" restates the Q2(b)(ii) choice already classified.'),
    '84767f7c44326e67':('not-a-selection','Prose in Q2(b)(iii) ("Jessica choose to have Suffolk cross ewes"); no response choice.'),
    '6affab5ae0701f14':('independent-task-selection','Q4 either (a) or (b): both alternatives are retained.'),
    'bcb6c41c4243d787':('independent-task-selection','Q7 either (a) or (b): both alternatives are retained.'),
    'e5148990f01416b6':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    '061023251f2a5302':('closed','Q12(a): describe any three of five printed soil-forming factors, 2+1+1. One card: a single anyN row lists all five, claim limit three.'),
    'ff0abf761cb97823':('exam-selection','Section B heading: three of six independent 50-mark questions, all retained.'),
    'ba31c532a1141c6c':('independent-task-selection','Q13: (a) with either (b) or (c). Every part, including both (b) and (c), is retained.'),
    '0d2805546cf3a368':('independent-task-selection','Q16: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'cb5e470cd8abdabb':('open','Q18(c)(iii): any two concerns from the scheme\'s pool; a marking menu, not a printed item choice.'),
}
SUPPLEMENTARY = [
    (10,'A farmer discovers his crop is deficient in the nutrient named in (ii) above','closed','Q7(a)(iii): the nutrient named in (ii); the scheme answers for nitrogen, phosphorus, potassium, sulphur, calcium and magnesium, kept as answer routes on one card.'),
    (26,'Draw a labelled diagram of one named method of grazing','open','Q15(a)(ii): any named grazing system; the scheme lists paddock, block, strip, spokes of a wheel and leader-follower and excludes zero grazing.'),
    (7,'Indicate if the following statements are true or false','answer-identification','Q4(b): one correct box per statement.'),
    (11,'Identify the bacteria in the root nodules of clover','answer-identification','Q8(d): one correct box (Rhizobium).'),
    (12,'Identify the average slaughter weight of lambs','answer-identification','Q9(c): one correct box (42 kg).'),
    (15,'State if this breed is a continental or','answer-identification','Q11(b)(i): one correct box (continental).'),
    (30,'Identify the ideal moisture content of hay','answer-identification','Q16(b)(iii): one correct box (18%).'),
]
TOPIC = 'agricultural-science-ordinary-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2022-ol-'
RESTORED = []
WITHDRAWN = {}
# Atlas numbers an earlier batch published for this paper (Q2(b)(ii) 1001, Q13(b)(i) 1003).
RESERVED = {'1001', '1003'}
PAGE4 = 'The scheme\'s own rule (PDF page 4): "the first correct answer encountered is awarded" the first mark, and each later correct answer the next.'

P = lambda *r: [region(*x) for x in r]
REGIONS = {
    'Q1(a)': (P((3, .16, .725)), P((12, .137, .246))),
    'Q1(b)': (P((3, .16, .41), (3, .72, .745)), P((12, .246, .35))),
    'Q2(a)(i)': (P((4, .065, .70)), P((12, .35, .45))),
    'Q2(a)(ii)': (P((4, .065, .365), (4, .715, .76)), P((12, .45, .552))),
    'Q2(b)(i)': (P((5, .09, .36)), P((12, .556, .623))),
    'Q2(b)(iii)': (P((5, .09, .13), (5, .619, .66)), P((12, .736, .894))),
    'Q3(a)': (P((6, .065, .205)), P((13, .085, .327))),
    'Q3(b)': (P((6, .065, .13), (6, .518, .665)), P((13, .327, .418))),
    'Q4(a)(i)': (P((7, .065, .18)), P((13, .418, .463))),
    'Q4(a)(ii)': (P((7, .09, .15), (7, .236, .26)), P((13, .463, .747))),
    'Q4(a)(iii)': (P((7, .09, .15), (7, .376, .40)), P((13, .747, .872))),
    'Q4(b)': (P((7, .495, .79)), P((14, .085, .226))),
    'Q5(a)': (P((8, .065, .12)), P((14, .226, .351))),
    'Q5(b)': (P((8, .305, .49)), P((14, .351, .511))),
    'Q6(a)': (P((9, .065, .30)), P((14, .511, .594))),
    'Q6(b)': (P((9, .065, .27), (9, .40, .425)), P((14, .594, .666))),
    'Q6(c)': (P((9, .065, .15), (9, .493, .517)), P((14, .666, .781))),
    'Q7(a)(i)': (P((10, .065, .20)), P((15, .12, .173))),
    'Q7(a)(ii)': (P((10, .09, .165), (10, .256, .28)), P((15, .173, .255))),
    'Q7(a)(iii)': (P((10, .09, .165), (10, .256, .355)), P((15, .255, .869))),
    'Q7(b)(i)': (P((10, .533, .70)), P((16, .085, .204))),
    'Q7(b)(ii)': (P((10, .533, .745)), P((16, .204, .357))),
    'Q8(a)': (P((11, .065, .372)), P((16, .357, .429))),
    'Q8(b)': (P((11, .065, .15), (11, .442, .466)), P((16, .429, .512))),
    'Q8(c)': (P((11, .065, .15), (11, .566, .606)), P((16, .512, .577))),
    'Q8(d)': (P((11, .065, .15), (11, .738, .879)), P((16, .577, .628))),
    'Q9(a)': (P((12, .065, .437)), P((16, .628, .769))),
    'Q9(b)': (P((12, .065, .395), (12, .567, .592)), P((16, .769, .817))),
    'Q9(c)': (P((12, .629, .77)), P((16, .817, .865))),
    'Q9(d)': (P((12, .771, .795)), P((16, .865, .908))),
    'Q10(a)': (P((13, .065, .188)), P((17, .085, .544))),
    'Q10(b)': (P((13, .378, .515)), P((17, .544, .644))),
    'Q10(c)': (P((13, .065, .13), (13, .644, .686)), P((17, .644, .803))),
    'Q11(a)(i)': (P((14, .065, .172)), P((18, .085, .134))),
    'Q11(a)(ii)': (P((14, .09, .15), (14, .243, .266, 0, .64)), P((18, .134, .178))),
    'Q11(a)(iii)': (P((14, .09, .15), (14, .337, .36)), P((18, .178, .24))),
    'Q11(a)(iv)': (P((14, .09, .15), (14, .461, .505)), P((18, .24, .285))),
    'Q11(a)(v)': (P((14, .09, .15), (14, .603, .645)), P((18, .285, .37))),
    'Q11(b)(i)': (P((15, .09, .25)), P((18, .378, .43))),
    'Q11(b)(ii)': (P((15, .09, .25), (15, .25, .295)), P((18, .43, .475))),
    'Q11(b)(iii)': (P((15, .39, .455)), P((18, .475, .59))),
    'Q11(b)(iv)': (P((15, .684, .725)), P((18, .59, .652))),
    'Q12(a)': (P((16, .065, .65)), P((19, .085, .636))),
    'Q12(b)': (P((16, .065, .13), (16, .656, .86)), P((19, .636, .81))),
    'Q13(a)(i)': (P((19, .158, .29)), P((20, .137, .221))),
    'Q13(a)(ii)': (P((19, .158, .24), (19, .334, .66)), P((20, .221, .322))),
    'Q13(a)(iii)': (P((19, .158, .24), (19, .66, .726)), P((20, .322, .417))),
    'Q13(a)(iv)': (P((19, .158, .24), (20, .065, .12)), P((20, .417, .586))),
    'Q13(a)(v)': (P((19, .158, .24), (21, .065, .09)), P((20, .586, .685))),
    'Q13(a)(vi)': (P((19, .158, .24), (19, .334, .59), (21, .213, .255)), P((20, .685, .788))),
    'Q13(b)(ii)': (P((22, .065, .09), (22, .128, .404)), P((21, .148, .201))),
    'Q13(b)(iii)': (P((22, .065, .09), (22, .128, .378), (22, .444, .468)), P((21, .196, .258))),
    'Q13(c)(i)': (P((22, .532, .556)), P((21, .262, .401))),
    'Q13(c)(ii)': (P((22, .724, .765)), P((21, .396, .525))),
    'Q14(a)': (P((23, .065, .167)), P((21, .52, .625))),
    'Q14(b)(i)': (P((23, .358, .407)), P((21, .62, .743))),
    'Q14(b)(ii)': (P((23, .358, .382), (23, .537, .70)), P((21, .738, .856))),
    'Q14(c)(i)': (P((24, .065, .12)), P((22, .085, .255))),
    'Q14(c)(ii)': (P((24, .358, .383)), P((22, .25, .41))),
    'Q14(c)(iii)': (P((24, .573, .598)), P((22, .405, .489))),
    'Q14(c)(iv)': (P((25, .065, .836)), P((22, .484, .857))),
    'Q15(a)(i)': (P((26, .065, .243)), P((23, .085, .189))),
    'Q15(a)(ii)': (P((26, .373, .47)), P((23, .184, .426))),
    'Q15(b)(i)': (P((27, .065, .395)), P((23, .421, .474))),
    'Q15(b)(ii)': (P((27, .065, .37), (27, .434, .48)), P((23, .469, .588))),
    'Q15(b)(iii)': (P((27, .065, .37), (27, .693, .758)), P((23, .583, .654))),
    'Q15(b)(iv)': (P((27, .065, .37), (28, .065, .09)), P((23, .649, .768))),
    'Q15(b)(v)': (P((27, .065, .37), (28, .28, .305)), P((23, .767, .82))),
    'Q15(b)(vi)': (P((28, .344, .37)), P((23, .815, .883))),
    'Q16(a)(i)': (P((29, .065, .408)), P((24, .085, .195))),
    'Q16(a)(ii)': (P((29, .065, .38), (29, .533, .557)), P((24, .19, .259))),
    'Q16(a)(iii)': (P((29, .065, .38), (29, .557, .58)), P((24, .254, .36))),
    'Q16(a)(iv)': (P((29, .712, .755)), P((24, .355, .408))),
    'Q16(b)(i)': (P((30, .065, .13)), P((24, .403, .456))),
    'Q16(b)(ii)': (P((30, .065, .105), (30, .231, .255)), P((24, .451, .556))),
    'Q16(b)(iii)': (P((30, .065, .105), (30, .635, .81)), P((24, .551, .603))),
    'Q16(c)(i)': (P((31, .065, .278)), P((24, .598, .669))),
    'Q16(c)(ii)': (P((31, .065, .25), (31, .355, .38)), P((24, .664, .745))),
    'Q16(d)(i)': (P((31, .523, .745)), P((24, .745, .814))),
    'Q16(d)(ii)': (P((31, .523, .745), (31, .748, .772)), P((24, .809, .862))),
    'Q17(a)(i)': (P((32, .065, .337)), P((25, .085, .203))),
    'Q17(a)(ii)': (P((32, .09, .316), (32, .468, .492)), P((25, .198, .282))),
    'Q17(a)(iii)': (P((32, .09, .316), (32, .676, .70)), P((25, .277, .361))),
    'Q17(b)(i)': (P((33, .065, .386)), P((25, .356, .481))),
    'Q17(b)(ii)': (P((33, .065, .36), (33, .494, .518)), P((25, .476, .585))),
    'Q17(b)(iii)': (P((33, .065, .36), (33, .629, .69)), P((25, .58, .731))),
    'Q17(b)(iv)': (P((33, .065, .165), (34, .065, .105)), P((25, .726, .81))),
    'Q17(c)': (P((34, .237, .426)), P((25, .805, .887))),
    'Q18(a)(i)': (P((35, .065, .315)), P((26, .085, .151))),
    'Q18(a)(ii)': (P((35, .065, .276), (35, .419, .443)), P((26, .146, .193))),
    'Q18(a)(iii)': (P((35, .065, .276), (35, .483, .507)), P((26, .191, .24))),
    'Q18(b)(i)': (P((35, .547, .595)), P((26, .235, .354))),
    'Q18(b)(ii)': (P((35, .547, .571), (36, .065, .09)), P((26, .349, .417))),
    'Q18(c)(i)': (P((36, .189, .49)), P((26, .412, .482))),
    'Q18(c)(ii)': (P((36, .189, .231), (36, .496, .535)), P((26, .477, .596))),
    'Q18(c)(iii)': (P((36, .189, .231), (36, .668, .692)), P((26, .591, .69))),
}
ATLAS = {
    'Q1(a)': 'health-safety|fertilisers-pollution-the-environment', 'Q1(b)': 'health-safety',
    'Q2(a)(i)': 'classification-of-organisms|animal-production', 'Q2(a)(ii)': 'animal-production|genetics', 'Q2(b)': 'animal-production|genetics',
    'Q3': 'soil-science|scientific-practices-experiments-investigations', 'Q3(b)': 'soil-science',
    'Q4(a)': 'fertilisers-pollution-the-environment', 'Q4(b)': 'animal-physiology|animal-production', 'Q5': 'animal-production',
    'Q6': 'health-safety|crop-production', 'Q6(a)': 'crop-production', 'Q7(a)': 'plant-physiology', 'Q7(a)(iii)': 'plant-physiology|soil-science',
    'Q7(b)': 'plant-physiology', 'Q8': 'scientific-practices-experiments-investigations|plant-physiology', 'Q9': 'animal-production',
    'Q10(a)': 'grassland|animal-production', 'Q10(b)': 'scientific-practices-experiments-investigations|grassland',
    'Q10(c)': 'scientific-practices-experiments-investigations|grassland', 'Q11(a)': 'animal-diseases', 'Q11(b)': 'animal-production',
    'Q12': 'soil-science', 'Q13(a)': 'soil-science|scientific-practices-experiments-investigations', 'Q13(b)': 'soil-science', 'Q13(c)': 'soil-science',
    'Q14': 'animal-production', 'Q14(a)': 'animal-production|health-safety', 'Q15(a)': 'grassland|animal-production', 'Q15(b)': 'animal-production',
    'Q16(a)': 'grassland|scientific-practices-experiments-investigations', 'Q16(b)': 'grassland',
    'Q16(c)': 'classification-of-organisms|crop-production', 'Q16(d)': 'classification-of-organisms|crop-production',
    'Q17(a)': 'innovation-and-biotechnology-in-agriculture', 'Q17(b)': 'fertilisers-pollution-the-environment|animal-production',
    'Q17(c)': 'fertilisers-pollution-the-environment', 'Q18(a)': 'grassland|scientific-practices-experiments-investigations',
    'Q18(b)': 'grassland|crop-production', 'Q18(c)': 'genetics|innovation-and-biotechnology-in-agriculture',
}
BREEDS = {'A': ('Simmental', 'a heavy red-brown bull with a white face, white belly and white socks'),
          'B': ('Landrace', 'a long pale pink pig with large forward-drooping ears and a curled tail'),
          'C': ('Blackface mountain or Swaledale', 'a white-fleeced ewe with a black-and-white face and curled horns, a lamb beside her'),
          'D': ('Jersey', 'a small fawn cow with a dark muzzle and a large udder')}
INDICATOR = ['Add soil sample to beaker and add distilled or deionised water', 'stir or mix well', 'add filter paper to funnel (in retort stand)',
             'pour the mixture into the funnel', 'collect the filtrate (filtered soil solution)', 'add pH paper or universal', 'note colour change',
             'compare colour to colour chart (to determine the pH)']
METER = ['Add soil sample to beaker and add distilled or deionised water', 'stir or mix well', 'turn on pH meter and calibrate using buffer solutions',
         'clean probe by inserting into distilled water (pH 7)', 'ensure pH reading correctly – pH 7', 'place probe into (stirred) solution', 'record reading',
         'clean probe into distilled or deionised water after reading']
STATEMENTS = [('i', 'The length of the oestrus cycle in cows is 17 days', 'False'), ('ii', 'Gestation length in cattle is 283 days', 'True'),
              ('iii', 'pH of the rumen is 7', 'True'), ('iv', 'Ideal Body Condition Score (BCS) for a cow at calving is 4.5', 'False'),
              ('v', 'The number of compartments in the ruminant stomach is 3', 'False')]
NUTRIENTS = [
    ('nitrogen', 'Nitrogen', 'Spindly yellow plants or yellow leaves / leaves may have pink tints / stunted growth/ necrosis (death) of older leaves',
     'Spread chemical nitrogen (Urea or protected urea or CAN or named chemical compound e.g. 18‐6‐12) / spread slurry / spread FYM'),
    ('phosphorus', 'Phosphorus', 'Reduced shoot growth / leaves turn dark or dull or blue‐green or pale in severe deficiency / reddish or reddish‐violet, or violet colour develops / lack of fruit or flowers/ wilting / delayed maturity',
     'Spread chemical phosphorus (named chemical compound e.g. 10‐10‐20 / spread FYM / spread slurry)'),
    ('potassium', 'Potassium', 'Chlorosis (yellowing) at the leaf margins / reduced yield or slow growth / scorching of leaves / poorly developed root system / weak stalks',
     'Spread chemical potassium (potash) (named chemical compound e.g. 10‐10‐20 / spread FYM / spread slurry'),
    ('sulphur', 'Sulphur', 'Plants are small and spindly / with short and slender stalks / stunted growth (prevent plants from utilising nitrogen) / maturity in cereals is delayed / nodulation in legumes may be poor or nitrogen‐fixation reduced / fruits often do not mature fully and remain light‐green in colour / chlorosis of leaves',
     'Spread chemical sulphur (with fertiliser) / spreading slurry / spreading FYM'),
    ('calcium', 'Calcium', 'Symptoms first appear on younger leaves and tissues / growth is inhibited / plants have a bushy appearance / youngest leaves are usually small or misshapen / brown chlorotic spots developing along the margins which spread to eventually unite in the centre of the leaves',
     'Adding lime (to soil in autumn) / apply a calcium supplement'),
    ('magnesium', 'Magnesium', 'Chlorosis (yellowing of the leaves) or interveinal chlorosis (yellowing of the leaf with the veins remaining green) / reduced growth',
     'Adding lime / apply a magnesium supplement'),
]
ADAPTATIONS = ['Flat (large surface area for max absorption of light)', 'thin (for diffusion of gases)', 'waxy cuticle (prevent water loss)',
               'palisade layer (tightly packed together with large number of chloroplasts for max light absorption)',
               'spongy mesophyll (many air spaces for rapid diffusion of gases)',
               'vascular tissue (xylem or phloem) ‐ (transport of water or removal of sugars for storage)', 'stomata (gas exchange)',
               'guard cells (open and close stomata)']
SILAGE_TESTS = [
    'Good quality – squeeze silage juice into a jar and place pH probe in or pH paper – pH 4 Poor quality ‐ squeeze silage juice into a jar and place pH probe in or pH paper – pH >5',
    'Good quality – firm and fibres do not wear easily Poor quality – soft or wet or slimy',
    'Good quality – green or yellow in colour Poor quality – darker or brown colour',
    'Good quality ‐ sweet perfume or sharp vinegary smell (which indicates excellent preservation) Poor quality ‐ putrid or rancid smell',
    'Good quality ‐ separate the leaves from the stems / if you roughly calculate the leaf‐to‐stem ratio to be 70:30, then you could say that the silage has a DMD of roughly 70‐72% or a satisfactory DMD Poor quality ‐ separate the leaves from the stems / if the ratio of leaf‐to‐stem is 60:40, then DMD of silage is roughly 60‐62% or unsatisfactory',
    'Good quality ‐ squeeze the silage and note any moisture. Very little or no water released indicates high DM Poor quality – squeeze the silage and note any moisture. Water released indicates low DM.',
]
PIT_SAMPLING = ['Samples taken at random or 10 ‐ 12 samples or in a W shape', 'samples not taken near the edges of the pit or from the open face of the pit',
                'samples should not be taken if spoiled', 'use corer to take the sample or dig through about 20cm from pit face', 'mix all samples in bucket',
                'put in zip lock bag and remove as much air as possible', 'sampling bales from same batch (min 5)',
                'safety ‐ be aware of silage falling from overhead at the pit face or any one valid safety point']
FACTORS = {
    'Parent material': 'Soil is formed by weathering of rock / mineral composition / texture or correct example of texture (coarse texture of granitic rocks leads to a coarse loamy soil texture) / pH of the soil is derived from the parent rock',
    'Topography': 'Erosion will occur in steep slopes / thin layer of soil on hillsides / deep fertile soils in valleys / soils in valleys retain water (easy cultivation)',
    'Time': 'Over time, vegetation and climate act on parent material and topography / development determines a soil\'s age / the degree of aging depends on the intensity of the other four soil‐ forming factors',
    'Climate': 'Temperature – heat and cooling of rocks (causing them to break) / low temperature leads to low water evaporation so more water for chemical weathering / precipitation – water contributes to physical or chemical weathering (freezing or solution or hydrolysis or hydration)',
    'Organisms': 'Provide humus when plant and animals die / microorganisms decompose organic matter (OM contributes to fertility and structure) / roots bind soil together / grasses contain alkaline compounds which reduce acidity in soil / acidic soils developed under forests / earthworms improve drainage or aeration or assist in soil formation',
}
MORTALITY_WAYS = ['Spread lime on pen', 'Add iodine to navel or adequate hygiene in sheds', 'Ensure the lambs get colostrum', 'Ewes in good condition',
                  'Adequate supervision', 'Fostering multiple births higher than 2 lambs', 'Equipment in one place', 'Contact the vet or experienced person',
                  'Infra‐red lamp or heat box or glucose injection or lambing indoors']
MORTALITY_REASONS = ['Reduce risk of infection', 'Prevent navel or joint ill or infection', 'Provide immunity or antibodies', 'Less risk of difficult lambing',
                     'Assist ewes in trouble lambing', 'Ewes only have 2 teats and can only rear 2 lambs', 'Have all equipment ready in case of difficult birth',
                     'Have number ready to call in an emergency', 'Prevent hypothermia or chill or predation']
HAY_STEPS = ['Fertilise grass (min 6 weeks prior)', 'cut at correct stage (vegetative or inflorescence stage)', 'cut using a mower', 'cut in June or July',
             'tedder grass', 'row the grass using a rower', 'until completely dehydrated', 'bale', 'move to storage shed']
TECH_ADVANTAGES = ['Better use of chemicals', 'harvesting crops', 'sowing fertiliser (accurately) or saving fuel or saving fertiliser', 'reducing labour or time',
                   'more accurate data', 'increased animal yields', 'increased crop yield', 'better animal welfare', 'less leaching',
                   'tracking or monitoring animals or identification of disease or illness']
ROBOT_REASONS = ['Reduced labour or easier to use', 'increased milk yield as cows milked more often', 'quicker detection of mastitis or of milk quality',
                 'more consistency', 'better overall herd management']
TECH_DISADVANTAGES = ['Lack of practical knowledge', 'increased maintenance cost', 'technical difficulties',
                      'overuse of machinery can cause environmental damage', 'expensive to install', 'reduced employment']
TRAITS = ['Heading date', 'total yield', 'ground cover', 'spring growth', 'autumn growth', 'dry matter digestibility (DMD)']
SEEDBED = ['Spray with total herbicide', 'plough (10 days after spraying)', 'spread lime and fertiliser or apply slurry after seeding',
           '(power) harrowed (to produce fine firm seedbed)', 'roll prior to sowing',
           'broadcast seed or sow seed close to surface or seed sown into old grassland or seed barrow', 'rolled again to achieve good soil to seed contact']


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='ordinary', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 41)), schemePagesInspected=list(range(1, 29)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=[],
                independentBoundaryReview='98 base tasks, one card each (Q2(b)(ii) and Q13(b)(i) reviewed in an earlier batch). Of the 95 original cards, 71 match a published boundary and tariff unchanged; 19 are corrected in place (Q1(a), Q2(a)(i), Q2(a)(ii), Q3(a), Q3(b), Q4(b), Q5(a), Q7(a)(iii), Q7(b)(ii), Q9(c), Q10(c), Q11(a)(iii), Q14(c)(iv), Q16(b)(ii), Q17(a)(i), Q17(a)(ii), Q17(a)(iii), Q18(a)(i), Q18(b)(i)); the five per-statement Q4(b) cards are withdrawn as aliases of the Q4(b) table card; six cards are added for the missing Q10(a), Q12(a), Q15(a)(ii), Q16(a)(ii), Q17(b)(i) and Q17(b)(iii).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


def atlas_for(ref):
    base = ref.split(' — ')[0]
    for key in (base, base.split(')(')[0] + ')' if ')(' in base else None, base.split('(')[0]):
        if key and key in ATLAS:
            return ATLAS[key]
    raise KeyError(ref)


def reviewed_tasks(existing):
    """existing: {id: card} from the authored file (originals are read, never rewritten unless corrected)."""
    paper_review()
    cards, tasks, corrections = [], [], {}
    RESTORED.clear(); WITHDRAWN.clear()
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith(PREFIX) and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith(PREFIX):
            originals[cid] = record['original']
    numbers = (str(n) for n in range(1001, 1200) if str(n) not in RESERVED)

    def task(cid, ref, selection=None):
        pp, sp = REGIONS[ref]
        t = dict(questionRef='2022 OL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: next(numbers)}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 40 paper and 28 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2022 OL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2022 Ordinary — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2022 Ordinary Level examination paper — © State Examinations Commission.',
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
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='ordinary',
                    section='A' if int(ref.split('(')[0][1:]) <= 12 else 'B', questionRef='2022 OL ' + ref,
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
        assert card['questionRef'] == '2022 OL ' + ref, (cid, card['questionRef'])
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

    def pool(key, ref, options, steps, notation, note, page, scheme_page, wording, problem, open_list=False):
        old = originals[PREFIX + key]
        row = menu(options, steps, note)
        if open_list:
            row['openList'] = True
        return fix(key, ref, dict(rows=[row], tariffModel={'kind': 'fixed', 'notation': notation}), drop=('notes',),
                   correction=(f'Visually verified paper PDF page {page} and scheme PDF page {scheme_page} ({wording}, "{notation}"). {problem} '
                               f'Same ID, boundary and {old["totalMarks"]} marks; one row lists every published point.'))

    # Section A ---------------------------------------------------------------
    fix('q1a', 'Q1(a)', dict(rows=[
        point('A = (fertiliser) spreader', 2), dict(point('Function = spread (shake or broadcast) fertiliser', 2), kind='alt', accepts=['spreading grass seed']),
        point('B = Slurry spreader or slurry tanker or trailing shoe or injector', 2), point('Function = spreading slurry or effluent', 2)],
        tariffModel={'kind': 'fixed', 'notation': '2, 2, 2, 2'}), drop=('notes',),
        correction=('Visually verified paper PDF page 3 ("Identify and state the function of machine A and B", A:/Function:/B:/Function: lines) and scheme PDF page 12 (2, 2, 2, 2 against A, its function, B and its function). '
                    'The original priced machine A and its function as one 4-mark row, so naming A without its function scored nothing. Same ID, boundary and 8 marks; four rows at 2 marks each.'))
    keep('q1b', 'Q1(b)')
    letters = list(BREEDS)
    fix('q2ai', 'Q2(a)(i)', dict(
        stem='Answer either (a) or (b).',
        questionText='The photographs below show breeds of animals found on Irish farms. Identify any three of the following breeds using the list below: Jersey, Blackface mountain, Landrace, Simmental.',
        rows=[menu([f'{l} = {BREEDS[l][0]}' for l in letters], [2, 2, 2], 'Any three of the four photographs, 2 marks each (3(2)).')],
        labelKey=[dict(letter=l, meaning=f'{BREEDS[l][1]} ({BREEDS[l][0]})', askedInThisQuestion=True) for l in letters]),
        drop=('notes',), selection=closed(3, letters),
        correction=('Visually verified paper PDF page 4 ("Identify any three of the following breeds using the list below", word list and photographs A–D) and scheme PDF page 12 (A Simmental, B Landrace, C Blackface mountain or Swaledale, D Jersey, "3(2)"). '
                    'The original stem was the word list run together, the label key decoded only A–C and D sat as an accepted answer on each row. '
                    'Same ID: one any-three-of-four card whose anyN row lists all four breeds, claim limit three, with every photograph decoded.'))
    fix('q2aii', 'Q2(a)(ii)', dict(stem='Answer either (a) or (b). The photographs below show breeds of animals found on Irish farms.'),
        correction=('Visually verified paper PDF page 4 ("Describe two traits which make animal A shown in part (i) above suitable for selection as a sire") and scheme PDF page 12 (3+1). '
                    'The original stem was the word list run together ("Jersey Blackface mountain Landrace Simmental Or"). Same ID, rows, figure, boundary and 4 marks; the stem is the paper\'s lead-in.'))
    keep('q2bi', 'Q2(b)(i)')
    keep('q2biii', 'Q2(b)(iii)')
    ind = dict(menu(INDICATOR, [2, 2, 2], 'Indicator method: any three steps, 2 marks each (3(2)).'), id='r-1')
    met = dict(menu(METER, [2, 2, 2], 'Or pH meter method: any three steps, 2 marks each (3(2)).'), id='r-1')
    fix('q3a', 'Q3(a)', dict(rows=[ind], answerVariants=[dict(id='indicator', label='pH paper or universal indicator', rows=[ind]),
                                                         dict(id='meter', label='pH meter', rows=[met])]),
        drop=('notes',), selection=closed(1, ['pH paper or universal indicator', 'pH meter']),
        correction=('Visually verified paper PDF page 6 ("Briefly describe how the student carried out this investigation") and scheme PDF page 13 (an indicator method "Or" a pH meter method, "3(2)"). '
                    'The original mixed the steps of both methods in one pool, so steps from the two methods could be combined. '
                    'Same ID, boundary and 6 marks; each method is an answer route the student chooses before reveal, listing every published step, any three at 2 marks.'))
    fix('q3b', 'Q3(b)', dict(
        stem='A student carried out an investigation in the school laboratory to determine the pH of a soil sample.',
        questionText='The result of the investigation is shown in the table below: soil sample, pH 5.2. Suggest one implication this has for growing crops on the land and one way the student could alter the pH of the soil.',
        rows=[dict(point('Implication: low nutrient availability or nutrient deficiencies in the crop', None, 'Implication and alteration: the scheme prints 3+1. ' + PAGE4),
                   kind='alt', accepts=['reduced crop yield', 'decreased growth rate of crop', 'affect earthworm activity']),
              point('Alter pH: adding lime to the land', None)],
        tariffModel={'kind': 'orderedSplit', 'notation': '3+1'}),
        correction=('Visually verified paper PDF page 6 (the table, soil sample pH 5.2, then the Implication: and Alter pH: lines) and scheme PDF page 13 ("Implication: low nutrient availability or nutrient deficiencies in the crop / reduced crop yield / decreased growth rate of crop / affect earthworm activity Alter pH: adding lime to the land", 3+1) with its PDF page 4 rule. '
                    'The original stem was the table run together ("pH Soil sample 5.2"), three of the four published implications were missing, and the 3 marks were pinned to the implication. '
                    'Same ID, boundary and 4 marks; every implication is accepted and the 3+1 follows the order of correct answers.'))
    for k, ref in [('q4ai', 'Q4(a)(i)'), ('q4aii', 'Q4(a)(ii)'), ('q4aiii', 'Q4(a)(iii)')]:
        keep(k, ref)
    fix('q4b', 'Q4(b)', dict(
        stem='Answer either (a) or (b).',
        questionText='Indicate if the following statements are true or false by place a tick (✓) in the correct box. The first one has been done as an example: Duration of heat in cattle is 48 hours — False. '
                     + ' '.join(f'({n}) {s}.' for n, s, _ in STATEMENTS),
        rows=[point(f'({n}) {s} — {a}', 2, '2 marks for each statement (5(2)).' if n == 'i' else None) for n, s, a in STATEMENTS],
        tariffModel={'kind': 'fixed', 'notation': '5(2)'}),
        correction=('Visually verified paper PDF page 7 (a true/false table of five statements (i)–(v) under one instruction, the example given) and scheme PDF page 14 ("False True True False False", "5(2)"). '
                    'The original rows were bare "True"/"False" with no statement anywhere on the card, and the five statements were also carded separately, so the same 10 marks shipped twice. '
                    'Same ID, boundary and 10 marks; the card prints every statement and the per-statement cards are withdrawn as progress aliases of it.'))
    for n, _, _ in STATEMENTS:
        cid = PREFIX + 'q4b' + n
        assert originals[cid]['questionRef'] == f'2022 OL Q4(b)({n})'
        RESTORED.append(originals[cid])
        WITHDRAWN[cid] = PREFIX + 'q4b'
    old5 = originals[PREFIX + 'q5a']
    fix('q5a', 'Q5(a)', dict(rows=[old5['rows'][0],
        point('Production diet – extra amount of feed required and used for production of some kind (1kg of LWG or 1 litre of milk or 1 kg of wool or produce calf or lamb)', 1)]),
        correction=('Visually verified paper PDF page 8 ("Farm animals are fed diets for maintenance and production. Explain the underlined terms.") and scheme PDF page 14 (1 + 1). '
                    'The original production answer stopped at "required and used for". Same ID, boundary and 2 marks; the row is the whole published answer.'))
    keep('q5b', 'Q5(b)')
    for k, ref in [('q6a', 'Q6(a)'), ('q6b', 'Q6(b)'), ('q6c', 'Q6(c)'), ('q7ai', 'Q7(a)(i)'), ('q7aii', 'Q7(a)(ii)')]:
        keep(k, ref)
    variants = [dict(id=slug, label=label, rows=[dict(point(f'Symptom — {sym}', 2, f'{label}: one symptom 2 marks and one treatment 2 marks.'), kind='alt', id='r-1'),
                                                  dict(point(f'Treatment — {treat}', 2), kind='alt', id='r-2')])
                for slug, label, sym, treat in NUTRIENTS]
    fix('q7aiii', 'Q7(a)(iii)', dict(
        stem='Answer either (a) or (b). A student plants some seeds to investigate germination. In part (ii) you named one nutrient absorbed through the root.',
        rows=variants[0]['rows'], answerVariants=variants), drop=('notes',), selection=closed(1, [label for _, label, _, _ in NUTRIENTS]),
        correction=('Visually verified paper PDF page 10 ("A farmer discovers his crop is deficient in the nutrient named in (ii) above. Describe (1) a symptom and (2) the treatment for this deficiency.") and scheme PDF page 15 (a table of symptoms and treatments for nitrogen, phosphorus, potassium, sulphur, calcium and magnesium; "Symptom - 2 Treatment - 2"). '
                    'The original told the student their nutrient was nitrogen and showed only the nitrogen answers. '
                    'Same ID, boundary and 4 marks; each nutrient is an answer route the student chooses before reveal, with its published symptom and treatment.'))
    keep('q7bi', 'Q7(b)(i)')
    pool('q7bii', 'Q7(b)(ii)', ADAPTATIONS, [3, 1], '3+1', 'Two adaptations: the first correct earns 3 marks and the second 1 (3+1).',
         10, 16, '"Describe two ways a leaf is adapted to carry out photosynthesis", eight adaptations',
         'The original stem was the diagram labels run together ("Gas B Gas A Water") and its two rows were pick-lists with no options, with 3 and 1 marks pinned to "flat" and "thin"; the stem is now the paper\'s lead-in.')
    cards[-1]['stem'] = 'Answer either (a) or (b). Photosynthesis is the method by which green plants make their own food using chlorophyll.'
    for k, ref in [('q8a', 'Q8(a)'), ('q8b', 'Q8(b)'), ('q8c', 'Q8(c)'), ('q8d', 'Q8(d)'), ('q9a', 'Q9(a)'), ('q9b', 'Q9(b)')]:
        keep(k, ref)
    fix('q9c', 'Q9(c)', dict(questionText='Identify the average slaughter weight of lambs by placing a tick (✓) in the box below. Slaughter Weight (kg): 30, 50, 42.'),
        correction=('Visually verified paper PDF page 12 ("Identify the average slaughter weight of lambs by placing a tick (✓) in the box below.", a three-row table 30, 50, 42) and scheme PDF page 16 ("42*(kg)", 3). '
                    'The original rewrote the question as "by choosing the correct value from the following three options". Same ID, row, boundary and 3 marks; the question is the paper\'s own wording.'))
    keep('q9d', 'Q9(d)')
    add('q10a', 'Q10(a)', '3-3-3', 'testing-silage-at-the-pit-face', 'Describe two tests a farmer could do to assess the quality of the silage at the pit face.',
        [menu(SILAGE_TESTS, [2, 1], 'Two tests, each with good and poor quality described. The scheme prints 2+1: the first correct test earns 2 marks and the second 1. In order the options are the scheme\'s pH, texture, colour, smell, DMD and DM tests.')],
        'Beef, sheep and dairy farmers require high quality silage for winter feed.')
    keep('q10b', 'Q10(b)')
    pool('q10c', 'Q10(c)', PIT_SAMPLING, [2, 1], '2+1', 'Two precautions: the first correct earns 2 marks and the second 1 (2+1).',
         13, 17, '"State two precautions the student should take when obtaining samples of silage from the pit face", eight precautions',
         'The original left out the first published precaution ("Samples taken at random or 10 - 12 samples or in a W shape") and its two rows were pick-lists with no options.')
    for k, ref in [('q11ai', 'Q11(a)(i)'), ('q11aii', 'Q11(a)(ii)')]:
        keep(k, ref)
    old11 = originals[PREFIX + 'q11aiii']
    fix('q11aiii', 'Q11(a)(iii)', dict(rows=[dict(old11['rows'][0], verbatim='Rotational grazing or leader follower grazing or good grazing management')]),
        correction=('Visually verified paper PDF page 14 ("Briefly explain one way Seán could prevent this disease on his farm") and scheme PDF page 18 ("Rotational grazing or leader follower grazing or good grazing management / vaccinate young calves", 2). '
                    'The original answer stopped at "good grazing". Same ID, boundary and 2 marks; the row is the whole published answer.'))
    for k, ref in [('q11aiv', 'Q11(a)(iv)'), ('q11av', 'Q11(a)(v)'), ('q11bi', 'Q11(b)(i)'), ('q11bii', 'Q11(b)(ii)'), ('q11biii', 'Q11(b)(iii)'), ('q11biv', 'Q11(b)(iv)')]:
        keep(k, ref)
    add('q12a', 'Q12(a)', '2-1', 'soil-forming-factors', 'Describe how any three of the following factors are involved in soil formation: Parent material, Topography, Time, Climate, Organisms.',
        [menu(list(FACTORS.values()), [2, 1, 1], 'Any three of the five factors. The scheme prints 2+1+1: the first correct description earns 2 marks and the next two 1 each. In order the options describe parent material, topography, time, climate and organisms.')],
        'Soil formation is a process that takes thousands of years and is influenced by many factors.', selection=closed(3, list(FACTORS)))
    keep('q12b', 'Q12(b)')
    # Section B ---------------------------------------------------------------
    for k, ref in [('q13ai', 'Q13(a)(i)'), ('q13aii', 'Q13(a)(ii)'), ('q13aiii', 'Q13(a)(iii)'), ('q13aiv', 'Q13(a)(iv)'), ('q13av', 'Q13(a)(v)'),
                   ('q13avi', 'Q13(a)(vi)'), ('q13bii', 'Q13(b)(ii)'), ('q13biii', 'Q13(b)(iii)'), ('q13ci', 'Q13(c)(i)'), ('q13cii', 'Q13(c)(ii)'),
                   ('q14a', 'Q14(a)'), ('q14bi', 'Q14(b)(i)'), ('q14bii', 'Q14(b)(ii)'), ('q14ci', 'Q14(c)(i)'), ('q14cii', 'Q14(c)(ii)'), ('q14ciii', 'Q14(c)(iii)')]:
        keep(k, ref)
    fix('q14civ', 'Q14(c)(iv)', dict(
        rows=[menu(MORTALITY_WAYS, [2, 2, 2], 'Three ways to minimise mortality, 2 marks each.'),
              menu(MORTALITY_REASONS, [2, 2, 1], 'The reason for each of the same three ways: 2, 2 and 1 marks (2(2+2) 1(2+1)). The reasons are listed in the same order as the ways.')],
        tariffModel={'kind': 'fixed', 'notation': '2(2+2) 1(2+1)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 25 ("Complete the table below to outline three ways to minimise mortality and give a reason for each action", the first row given) and scheme PDF page 22 (nine ways with reasons, "2(2+2) 1(2+1)"). '
                    'The original showed five of the nine published ways and priced each way-and-reason pair together. Same ID, boundary and 11 marks; every published way and reason is listed, three ways at 2 marks and their reasons at 2, 2 and 1.'))
    keep('q15ai', 'Q15(a)(i)')
    add('q15aii', 'Q15(a)(ii)', '3-3-2', 'drawing-a-named-grazing-system',
        'Good grassland management during springtime will ensure excellent milk production from grazed grass for the remainder of the year. Draw a labelled diagram of one named method of grazing employed by the dairy farmer.',
        [point('Named grazing system ‐ Paddock (rotational) / block / strip grazing / spokes of a wheel / leader‐follower', None, 'Named system: 4 marks. The scheme adds "(Zero grazing is not accepted)".'),
         point('For 6 marks: diagram must show any three of the following; fencing, water supply, indication of animal movement, roadway, indication of grazing or previously grazed', None,
               'Drawing, D - 0, 3, 6: "For 3 marks: diagram has two of the items listed above."', kind='criterion'),
         point('Labels 3(3) ‐ any 3 valid labels', None, 'Labels, L - 3(3).')],
        'When it comes to dairy and dairy by‐products consumers are increasingly looking for natural, sustainable, high‐quality products. Grass fed means that for an average of 220 days a year the diet of the animal is composed of a minimum of 90% grass.',
        marks=19, tariff={'kind': 'questionTotal', 'notation': '4 + D - 0,3,6 + L - 3(3)'})
    for k, ref in [('q15bi', 'Q15(b)(i)'), ('q15bii', 'Q15(b)(ii)'), ('q15biii', 'Q15(b)(iii)'), ('q15biv', 'Q15(b)(iv)'), ('q15bv', 'Q15(b)(v)'), ('q15bvi', 'Q15(b)(vi)'),
                   ('q16ai', 'Q16(a)(i)')]:
        keep(k, ref)
    graph = 'agsci-2022-ol-paper-grass-growth-curve'
    add('q16aii', 'Q16(a)(ii)', '3-3-2', 'excess-grass-on-the-growth-curve', 'Shade onto the graph above the portion which represents the excess grass in summer months.',
        [point('Shaded area between continous blue line and orange dash line', 2, 'The excess is where grass growth (the solid line) runs above feed demand (the dashed line) in the summer months.')],
        'Answer (a) and (b) with either (c) or (d). The graph shows the growth of grass in kg/ha for the months February to November 2021.', figure=graph)
    for k, ref in [('q16aiii', 'Q16(a)(iii)'), ('q16aiv', 'Q16(a)(iv)'), ('q16bi', 'Q16(b)(i)')]:
        keep(k, ref)
    pool('q16bii', 'Q16(b)(ii)', HAY_STEPS, [4, 4, 4, 3], '3(4)+3', 'Four steps: the first three correct earn 4 marks each and the fourth 3 (3(4)+3).',
         30, 24, '"Describe four steps involved in the production of hay", nine steps',
         'The original grouped the nine steps into five rows, so two steps in the same row (for example cutting with a mower and cutting in June or July) could not both be ticked.')
    for k, ref in [('q16biii', 'Q16(b)(iii)'), ('q16ci', 'Q16(c)(i)'), ('q16cii', 'Q16(c)(ii)'), ('q16di', 'Q16(d)(i)'), ('q16dii', 'Q16(d)(ii)')]:
        keep(k, ref)
    pool('q17ai', 'Q17(a)(i)', TECH_ADVANTAGES, [4, 2], '4+2', 'Two advantages: the first correct earns 4 marks and the second 2 (4+2). The scheme adds "other valid answer".',
         32, 25, '"Outline two advantages of technology in agriculture", ten advantages and "other valid answer"',
         'The original grouped the ten advantages into five rows, so two advantages in the same row (for example increased animal and crop yields) could not both be ticked.', open_list=True)
    pool('q17aii', 'Q17(a)(ii)', ROBOT_REASONS, [4, 2], '4+2', 'Two reasons: the first correct earns 4 marks and the second 2 (4+2). The scheme adds "other valid answer".',
         32, 25, '"Briefly describe two reasons for the increased installation of robotic milking machines", five reasons and "other valid answer"',
         'The original reworded one reason as "Milked more often — increased milk yield"; the scheme prints "increased milk yield as cows milked more often".', open_list=True)
    pool('q17aiii', 'Q17(a)(iii)', TECH_DISADVANTAGES, [4, 2], '4+2', 'Two disadvantages: the first correct earns 4 marks and the second 2 (4+2). The scheme adds "other valid answer".',
         32, 25, '"Outline two potential disadvantages of using technology on Irish farms", six disadvantages and "other valid answer"',
         'The original put "technical difficulties" inside the first row, so it could not be ticked alongside lack of practical knowledge.', open_list=True)
    john = ('John’s farm is Bord Bia Quality Assured. He aims to make his farm more sustainable. He is part of the Beef Emergency Aid Measure (BEAM) and is required to reduce '
            'his bovine nitrogen livestock figures by 5%. Analyse the data and answer the questions which follow.')
    table = 'agricultural-science-2022-OL-paper-p33-art'
    add('q17bi', 'Q17(b)(i)', '1-3', 'bovine-nitrogen-for-young-cattle', 'Calculate the total bovine nitrogen (figure A) for John’s 1 – 2 year-old cattle for 2020-21.',
        [point('40 X 57', 4, 'The working: number of livestock times nitrogen produced per year.'),
         point('= 2280 (kg)', 4, 'The scheme adds: (If a candidate gives 2280 (kg) without showing any calculations they may be awarded 8m).')],
        john, figure=table)
    keep('q17bii', 'Q17(b)(ii)')
    add('q17biii', 'Q17(b)(iii)', '1-3', 'checking-a-bovine-nitrogen-target',
        'The bovine nitrogen reference figure for the previous year 2019-20 is 6992kg on John’s farm. State if John achieved his target of 5% bovine nitrogen reduction in 2020-21. Show your calculation in the box below.',
        [point('6992 x 5% = 349.6 (kg)', 2), point('6992 ‐ 349.6 = 6642.4 (kg)', 2,
               'The scheme adds that this can be rounded to 6643 (kg) or left as it is, and (If a candidate gives 6642.4 (kg) or 6643 (kg) without showing any calculations they may be awarded 4m).'),
         point('Yes – John reached his target as he only produced 6442 (kg)', 2, 'The scheme prints 6442 here; its own answer to part (ii) is 6448 kg, which is also below 6642.4 kg.')],
        john, figure=table)
    for k, ref in [('q17biv', 'Q17(b)(iv)'), ('q17c', 'Q17(c)')]:
        keep(k, ref)
    pool('q18ai', 'Q18(a)(i)', TRAITS, [4, 4, 4], '3(4)', 'Any three traits, 4 marks each (3(4)).',
         35, 26, '"List three physical traits assessed by the DAFM when recommending grass seed varieties", six traits',
         'The original put "autumn growth" inside the spring growth row, so the two could not both be ticked.')
    for k, ref in [('q18aii', 'Q18(a)(ii)'), ('q18aiii', 'Q18(a)(iii)')]:
        keep(k, ref)
    pool('q18bi', 'Q18(b)(i)', SEEDBED, [2, 2, 2], '3(2)', 'Any three steps, 2 marks each (3(2)).',
         35, 26, '"Describe how Harry should prepare his seedbed", seven steps',
         'The original put "roll prior to sowing" inside the harrowing row and "rolled again" inside the broadcasting row, so neither could be ticked alongside its host step.')
    for k, ref in [('q18bii', 'Q18(b)(ii)'), ('q18ci', 'Q18(c)(i)'), ('q18cii', 'Q18(c)(ii)')]:
        keep(k, ref)
    keep('q18ciii', 'Q18(c)(iii)')
    assert len(tasks) == 96 and len(corrections) == 19 and len(originals) == 95 and len(cards) == 25 and len(WITHDRAWN) == 5, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} | set(WITHDRAWN) >= set(originals), 'Every original 2022 Ordinary card must be reviewed or withdrawn as an alias'
    return cards, tasks, corrections
