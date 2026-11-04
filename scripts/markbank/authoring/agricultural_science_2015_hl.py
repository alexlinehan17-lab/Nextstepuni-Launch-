"""2015 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 58 base tasks, one card each. Under the scheme's convention (PDF page 4) a
scale such as 6 + 3 + 1 pays the first correct answer 6 and each later one the next value, so a
Question 1 part whose scale spans its (i) and (ii) (Q1(h), (j)) is one task stating the scale
(orderedSplit); a part with one pool keeps the steps on its menu. Numbered items inside a part
(Q2(b)(i), Q7(a)(ii), Q8(b)(iii)) stay on that part's card. The three Q3 Option Two (a) headings
carry 2 + 2 each and are separate tasks. Q8(c) is one card whose eight members are parts.
Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': 'd9f65036e827e5b6de193ee0c5a0d825b16ef7e83d3a1698684f82aa6a95304c',
          'markingschemes': '59811aee15e026a6bb6013e29d71fc851e71809ae7dc2ef0e96e79fd35cfe5c7'}
SELECTIONS = {
    '4eb13c9ec23f67ff': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '654cd1a5abdc7c4a': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    '6ee76567de52aa5e': ('open', 'Q1(d): any three factors in gley formation; the scheme lists five (a marking menu).'),
    'df3cc27d93a0b330': ('open', 'Q1(f): any two characteristics of each plant; the scheme lists the fern and pine pools (marking menus).'),
    '8c34adfa0aeaceba': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    '3564518691c7a4ee': ('open', 'Q6(c)(ii): any three environmental factors with their effect; the scheme lists seven (a marking menu).'),
    '95b935cc82833748': ('not-a-selection', '"one of four phenotypes" describes the cross in Q7(b), not a choice.'),
    'e24c8951d91bdc55': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    '8b2202fea71013a9': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    '6894d3316651582d': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (3, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
]
ATLAS = {
    'Q1(a)': 'crop-production', 'Q1(b)': 'classification-of-animals-plants', 'Q1(c)': 'fertilisers-pollution-environment-cycles|crop-production',
    'Q1(d)': 'soil-science', 'Q1(e)': 'classification-of-animals-plants|grassland', 'Q1(f)': 'classification-of-animals-plants',
    'Q1(g)': 'pigs', 'Q1(h)': 'fertilisers-pollution-environment-cycles', 'Q1(i)': 'animal-physiology-circulatory-system', 'Q1(j)': 'soil-science|crop-production',
    'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'crop-production', 'Q3 Option One (b)': 'crop-production|animal-diseases', 'Q3 Option One (c)(i)': 'crop-production|animal-diseases',
    'Q3 Option Two': 'dairy-cattle', 'Q3 Option Two (c)(ii)': 'beef-cattle',
    'Q4': 'scientific-practices-experiments-investigations', 'Q4(a)': 'scientific-practices-experiments-investigations|grassland',
    'Q4(b)': 'scientific-practices-experiments-investigations|grassland', 'Q4(c)': 'scientific-practices-experiments-investigations|crop-production',
    'Q4(d)': 'scientific-practices-experiments-investigations|animal-diseases',
    'Q5': 'sheep', 'Q5(b)': 'sheep|animal-physiology-reproductive-systems', 'Q5(a)': 'sheep|animal-physiology-reproductive-systems',
    'Q6': 'crop-production', 'Q6(a)': 'crop-production|fertilisers-pollution-environment-cycles', 'Q6(c)': 'plant-physiology',
    'Q7': 'genetics', 'Q7(c)': 'genetics|dairy-cattle',
    'Q8(a)': 'fertilisers-pollution-environment-cycles', 'Q8(b)': 'grassland', 'Q8(c)': 'grassland|animal-physiology-circulatory-system|soil-science|crop-production',
    'Q9(a)': 'grassland', 'Q9(b)': 'grassland|fertilisers-pollution-environment-cycles', 'Q9(c)': 'fertilisers-pollution-environment-cycles',
    'Q9(d)': 'dairy-cattle', 'Q9(e)': 'beef-cattle',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1(a)': (P((2, 0.052, 0.112)), P((5, 0.080, 0.180))),
    'Q1(b)': (P((2, 0.052, 0.083), (2, 0.112, 0.217)), P((5, 0.080, 0.114), (5, 0.180, 0.213))),
    'Q1(c)': (P((2, 0.052, 0.083), (2, 0.217, 0.248)), P((5, 0.080, 0.114), (5, 0.213, 0.280))),
    'Q1(d)': (P((2, 0.052, 0.083), (2, 0.248, 0.278)), P((5, 0.080, 0.114), (5, 0.280, 0.346))),
    'Q1(e)': (P((2, 0.052, 0.083), (2, 0.278, 0.308)), P((5, 0.080, 0.114), (5, 0.346, 0.395))),
    'Q1(f)': (P((2, 0.052, 0.083), (2, 0.308, 0.368)), P((5, 0.080, 0.114), (5, 0.395, 0.461))),
    'Q1(g)': (P((2, 0.052, 0.083), (2, 0.368, 0.398)), P((5, 0.080, 0.114), (5, 0.461, 0.527))),
    'Q1(h)': (P((2, 0.052, 0.083), (2, 0.398, 0.443)), P((5, 0.080, 0.114), (5, 0.527, 0.594))),
    'Q1(i)': (P((2, 0.052, 0.083), (2, 0.443, 0.473)), P((5, 0.080, 0.114), (5, 0.594, 0.660))),
    'Q1(j)': (P((2, 0.052, 0.083), (2, 0.473, 0.593)), P((5, 0.080, 0.114), (5, 0.660, 0.735))),
    'Q2(a)(i)': (P((2, 0.593, 0.612)), P((6, 0.097, 0.185))),
    'Q2(a)(ii)': (P((2, 0.612, 0.627)), P((6, 0.097, 0.130), (6, 0.185, 0.251))),
    'Q2(a)(iii)': (P((2, 0.627, 0.653)), P((6, 0.097, 0.130), (6, 0.251, 0.278))),
    'Q2(b)(i)': (P((2, 0.653, 0.687)), P((6, 0.097, 0.130), (6, 0.278, 0.382))),
    'Q2(b)(ii)': (P((2, 0.687, 0.713)), P((6, 0.097, 0.130), (6, 0.382, 0.426))),
    'Q2(c)': (P((2, 0.713, 0.766)), P((6, 0.097, 0.130), (6, 0.426, 0.518))),
    'Q3 Option One (a)(i)': (P((3, 0.046, 0.095)), P((7, 0.097, 0.184))),
    'Q3 Option One (a)(ii)': (P((3, 0.046, 0.075), (3, 0.095, 0.135)), P((7, 0.097, 0.130), (7, 0.184, 0.252))),
    'Q3 Option One (b)(i)': (P((3, 0.046, 0.075), (3, 0.135, 0.185)), P((7, 0.097, 0.130), (7, 0.252, 0.300))),
    'Q3 Option One (b)(ii)': (P((3, 0.046, 0.075), (3, 0.135, 0.166), (3, 0.185, 0.200)), P((7, 0.097, 0.130), (7, 0.300, 0.349))),
    'Q3 Option One (b)(iii)': (P((3, 0.046, 0.075), (3, 0.135, 0.166), (3, 0.200, 0.226)), P((7, 0.097, 0.130), (7, 0.349, 0.410))),
    'Q3 Option One (c)(i)': (P((3, 0.046, 0.075), (3, 0.226, 0.289)), P((7, 0.097, 0.130), (7, 0.410, 0.4625), (7, 0.4625, 0.4815, 0, 0.775), (7, 0.4815, 0.531))),  # (c)(ii)'s 3+3+2m cell sits on this row; left out
    'Q3 Option One (c)(ii)': (P((3, 0.046, 0.075), (3, 0.289, 0.361)), P((7, 0.097, 0.130), (7, 0.4625, 0.4815, 0.775, 0.89), (7, 0.531, 0.584))),  # the scheme's 'Q 3 Option 2' head is not read as a boundary
    'Q3 Option Two (a)(i)': (P((3, 0.420, 0.442), (3, 0.452, 0.4845)), P((8, 0.098, 0.121), (8, 0.131, 0.1838))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q3 Option Two (a)(ii)': (P((3, 0.420, 0.442), (3, 0.452, 0.4695), (3, 0.4845, 0.4995)), P((8, 0.098, 0.121), (8, 0.131, 0.152, 0.787, 0.888), (8, 0.1838, 0.2165))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q3 Option Two (a)(iii)': (P((3, 0.420, 0.442), (3, 0.452, 0.4695), (3, 0.4995, 0.5145)), P((8, 0.098, 0.121), (8, 0.131, 0.152, 0.787, 0.888), (8, 0.2165, 0.268))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q3 Option Two (b)(i)': (P((3, 0.420, 0.442), (3, 0.527, 0.5745)), P((8, 0.098, 0.121), (8, 0.279, 0.3485))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q3 Option Two (b)(ii)': (P((3, 0.420, 0.442), (3, 0.527, 0.5595), (3, 0.5745, 0.5895)), P((8, 0.098, 0.121), (8, 0.3485, 0.416))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q3 Option Two (c)(i)': (P((3, 0.420, 0.442), (3, 0.602, 0.6195)), P((8, 0.098, 0.121), (8, 0.427, 0.4475))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q3 Option Two (c)(ii)': (P((3, 0.420, 0.442), (3, 0.6195, 0.651)), P((8, 0.098, 0.121), (8, 0.4475, 0.515))),  # hand-set: the scheme heads this option 'Q 3 Option 2'
    'Q4(a)': (P((3, 0.721, 0.781)), P((8, 0.558, 0.657))),
    'Q4(b)': (P((3, 0.721, 0.751), (3, 0.781, 0.812)), P((8, 0.558, 0.591), (8, 0.657, 0.724))),
    'Q4(c)': (P((3, 0.721, 0.751), (3, 0.812, 0.841)), P((8, 0.558, 0.591), (8, 0.724, 0.823))),
    'Q4(d)': (P((3, 0.721, 0.751), (3, 0.841, 0.883)), P((8, 0.558, 0.591), (8, 0.823, 0.882))),  # trimmed above the page footer
    'Q5(a)(i)': (P((4, 0.046, 0.065)), P((9, 0.097, 0.153))),
    'Q5(a)(ii)': (P((4, 0.065, 0.080)), P((9, 0.097, 0.118), (9, 0.153, 0.169))),
    'Q5(a)(iii)': (P((4, 0.080, 0.106)), P((9, 0.097, 0.118), (9, 0.169, 0.229))),
    'Q5(b)': (P((4, 0.106, 0.135)), P((9, 0.097, 0.118), (9, 0.229, 0.279))),
    'Q5(c)': (P((4, 0.135, 0.181)), P((9, 0.097, 0.118), (9, 0.279, 0.344))),
    'Q5(d)': (P((4, 0.181, 0.301)), P((9, 0.097, 0.118), (9, 0.344, 0.460))),
    'Q6(a)': (P((4, 0.301, 0.346)), P((9, 0.460, 0.625))),
    'Q6(b)': (P((4, 0.346, 0.391)), P((9, 0.460, 0.480), (9, 0.625, 0.724))),
    'Q6(c)(i)': (P((4, 0.391, 0.410)), P((9, 0.460, 0.480), (9, 0.724, 0.761))),
    'Q6(c)(ii)': (P((4, 0.410, 0.526)), P((9, 0.460, 0.480), (9, 0.761, 0.865))),
    'Q7(a)(i)': (P((4, 0.526, 0.545)), P((10, 0.129, 0.202))),
    'Q7(a)(ii)': (P((4, 0.545, 0.616)), P((10, 0.129, 0.163), (10, 0.202, 0.360))),
    'Q7(b)': (P((4, 0.616, 0.736)), P((10, 0.129, 0.163), (10, 0.360, 0.459))),
    'Q7(c)': (P((4, 0.736, 0.834)), P((10, 0.129, 0.163), (10, 0.459, 0.617))),
    'Q8(a)': (P((5, 0.030, 0.107)), P((11, 0.080, 0.293))),
    'Q8(b)(i)': (P((5, 0.030, 0.062), (5, 0.107, 0.126)), P((11, 0.080, 0.100), (11, 0.293, 0.359))),
    'Q8(b)(ii)': (P((5, 0.030, 0.062), (5, 0.126, 0.141)), P((11, 0.080, 0.100), (11, 0.359, 0.4335), (11, 0.4335, 0.449, 0, 0.775))),  # (iii)'s 2+2m cell sits on this last row; left out
    'Q8(b)(iii)': (P((5, 0.030, 0.062), (5, 0.141, 0.196)), P((11, 0.080, 0.100), (11, 0.4335, 0.449, 0.775, 0.89), (11, 0.449, 0.609))),  # with its 2+2m cell from the row above
    'Q8(c)': (P((5, 0.030, 0.062), (5, 0.196, 0.346)), P((11, 0.080, 0.100), (11, 0.609, 0.890))),
    'Q9(a)': (P((5, 0.346, 0.406)), P((12, 0.080, 0.213))),
    'Q9(b)': (P((5, 0.346, 0.376), (5, 0.406, 0.436)), P((12, 0.080, 0.114), (12, 0.213, 0.279))),
    'Q9(c)': (P((5, 0.346, 0.376), (5, 0.436, 0.466)), P((12, 0.080, 0.114), (12, 0.279, 0.345))),
    'Q9(d)': (P((5, 0.346, 0.376), (5, 0.466, 0.496)), P((12, 0.080, 0.114), (12, 0.345, 0.444))),
    'Q9(e)': (P((5, 0.346, 0.376), (5, 0.496, 0.552)), P((12, 0.080, 0.114), (12, 0.444, 0.523))),
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'


def split(text, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def build():
    p = Paper(2015, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    six = 'Answer any six of the parts (a) – (j).'
    # Question 1 -------------------------------------------------------------
    add('q1a', 'Q1(a)', '3-3-2', 'thinning-forest-trees', 'Give three reasons for the practice of thinning forest trees.',
        [menu('Disease|damaged trees|harvesting thinnings (income)|reduce competition|provides access|have uniform crop at clear felling or an example in each case', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='2-4')
    add('q1b', 'Q1(b)', '4-2', 'phyla-of-farm-organisms', 'State to which phylum each of the following belongs: (i) Earthworm. (ii) Greenbottle fly. (iii) Liver fluke. (iv) Sheep. (v) Babesia.',
        [point('(i) Earthworm — Annelida', 2, '5 × 2m, in the scheme\'s order.'), point('(ii) Greenbottle fly — Arthropoda', 2), point('(iii) Liver fluke — Platyhelminthes', 2),
         point('(iv) Sheep — Chordata', 2), point('(v) Babesia — Protozoa', 2)], six, node='3-1|2-1')
    add('q1c', 'Q1(c)', '3-3-2', 'pesticide-controls', 'Explain why it is necessary to have strict controls in the application of pesticides to farm crops.',
        [menu('Pollution or damage to wildlife|toxicity|accumulation in food chain (biomagnification)|crop residues|health risk to operator|affects pollination', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='2-4|1-6')
    add('q1d', 'Q1(d)', '2-1', 'gley-soil-formation', 'Mention any three factors that contribute to the formation of a gley soil.',
        [menu('High rainfall|waterlogging or poor drainage or high water table or impermeable subsoil|anaerobic conditions|oxidation or reduction of iron|formed in lowland or gently sloping hillsides', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='1-0')
    add('q1e', 'Q1(e)', '3-2', 'gramineae-characteristics', 'List three characteristics that are typical of the family Gramineae.',
        [menu('Monocot or named monocot feature|tillers|nodes|ligule|spikelet|green flower parts|wind pollinated or correct flower feature', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='2-1|2-6')
    add('q1f', 'Q1(f)', '3-2', 'fern-and-pine-structure', 'List any two structural characteristics of each of the following: (i) a fern plant. (ii) a pine tree.',
        [menu('Flowerless|rhizome (underground stem)|frond|pinnae|pinnules|rachis|sorus|sporangia|young fronds crozier-shaped', [3, 2], 'Fern: any two, 3 + 2 (2×(3+2)m).'),
         menu('Woody|shallow root system|cones|needles|naked seeds', [3, 2], 'Pine: any two, 3 + 2.')], six, node='2-1')
    add('q1g', 'Q1(g)', '4-3-2', 'pig-critical-temperature', 'Explain the importance of critical temperature in the context of a pig rearing enterprise.',
        [menu('Environmental temperature at which pigs can maintain body temperature|without weight loss|correct temperature for specified house|if temp too low they eat too much feed|maintains good FCR', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='3-4')
    add('q1h', 'Q1(h)', '2-3', 'interdependence', '(i) Explain the term interdependence as used in ecology. (ii) Give two examples of interdependence in agriculture.',
        [split('(i) Interdependence — organisms depending on each other', FIRST.format('6 + 3 + 1') + ' Three answers: the term and two examples.'),
         split('(ii) Examples — Any two correct examples explaining role of both organisms in each relationship', 'Two examples, each explaining the role of both organisms.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '6+3+1m'}, node='1-6')
    add('q1i', 'Q1(i)', '4-1', 'blood-functions', 'Give three functions of blood in the animal body.',
        [menu('food or named food|waste products|hormones|oxygen|carbon dioxide|heat|Immunity or fighting infection|clotting', [6, 3, 1],
              'Any three, with a maximum of two transport points (food to heat). ' + FIRST.format('6 + 3 + 1'))], six, node='3-0')
    add('q1j', 'Q1(j)', '2-3', 'field-aspect', '(i) Explain what is meant by the aspect of a field. (ii) Outline how aspect affects crop growth.',
        [split('(i) Aspect — Direction in which a field is facing', FIRST.format('6 + 3 + 1') + ' Three answers: the term and two effects.'),
         split('(ii) Effect on crop growth — South facing fields get more sun or heat up faster or crops get more light (for photosynthesis)/ higher yields/ longer season/ earlier germination/ earlier sowing',
               '[Opposite valid points for north-facing]')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '6+3+1m'}, node='1-5|2-3')
    # Question 2 -------------------------------------------------------------
    add('q2ai', 'Q2(a)(i)', '2-1', 'podzol-formation', 'Describe the conditions which contribute to the formation of a podzol soil.',
        [menu('High rainfall or low evaporation|acid leaching or leaching of iron or of aluminium or iron pan formed|low pH|cool temperatures|acidic parent materials|hilly mountainous areas', [2] * 3,
              'Any three, 2 marks each (3×2m).')], node='1-0')
    add('q2aii', 'Q2(a)(ii)', '2-2-2', 'texture-and-soil-temperature', 'Explain how soil temperature is influenced by soil texture.',
        [menu(['Sandy soil has more air (or less water)/ is warmer', 'Clay soil has less air (or more water)/ is cold', 'Loam has the optimal air or water content/ for suitable temperature'], [4, 4],
              'Any two soils: 2(2+2), the cause 2 and its effect 2. [Cause and effect required]')], node='1-3')
    add('q2aiii', 'Q2(a)(iii)', '2-2-2', 'other-soil-temperature-factor', 'Name one other characteristic of a soil that could affect its temperature.',
        [point('Soil colour or organic matter content or soil structure or soil pH', 2)], 'Explain how soil temperature is influenced by soil texture.', node='1-3')
    add('q2bi', 'Q2(b)(i)', '2-2-1', 'cations-colloids-and-cec',
        '1. Explain the difference between a cation and a colloid. 2. Explain the terms cation exchange and cation exchange capacity (CEC).',
        [point('Cation: positively charged particle (or positively charged ion)', 2, '1. 2 + 2m: the cation 2 and the colloid 2.'),
         point('Colloid: small negatively charged particle of clay or humus', 2),
         point('Cation exchange: swapping of positive ions on the surface of colloid particles or correct example (e.g. H+ exchanged with Ca2+)', 4, '2. 4 + 4m: each term 4.'),
         point('Cation exchange capacity (CEC): ability of a soil to carry out cation exchange', 4)], node='1-2')
    add('q2bii', 'Q2(b)(ii)', '2-2-1', 'raising-cec', 'How may the CEC of a soil be increased?',
        [point('Adding humus or organic matter or FYM or compost or slurry or seaweed or green manure or liming', 2)], node='1-2')
    add('q2c', 'Q2(c)', '2-2-1', 'cation-exchange-experiment', 'Describe an experiment to investigate cation exchange in a soil.',
        [menu('Sieved soil sample|high pH soil or clay-rich soil or calcium-rich soil|wash with (1%) potassium (chloride) solution|through a filter|test filtrate for Ca2+|ammonium oxalate reagent|white ppt. indicates calcium|potassium has replaced calcium',
              [3] * 6, 'Any six, 3 marks each (6×3m), or valid details from alternative method.')], node='1-2|0-1')
    # Question 3 -------------------------------------------------------------
    add('q3o1ai', 'Q3 Option One (a)(i)', '3-3-1', 'sprouting-seed-potatoes', 'Outline the advantages of sprouting seed potatoes.',
        [menu('Start growing immediately or earlier emergence|increased yield or longer growing season|earlier harvest|essential for early varieties|removal of diseased tubers', [4, 4],
              'Any two, 4 marks each (2×4m).')], node='2-3')
    add('q3o1aii', 'Q3 Option One (a)(ii)', '3-2', 'seed-potatoes-not-true-seeds', 'Seed potatoes are not true seeds. Discuss the validity of this statement.',
        [point('State or imply that the statement is true', 2),
         menu('Potatoes are tubers or modified stems|asexual reproduction|true seeds form within flowers|as a result of sexual reproduction|seeds are found in fruit', [2] * 3,
              'Any three, 2 marks each (3×2m). [At least one point to refer to potatoes and one to refer to seeds]')], node='2-1|2-3')
    blight = 'Give an account of the potato blight fungus (Phytophthora infestans) under the following headings:'
    add('q3o1bi', 'Q3 Option One (b)(i)', '3-3-2', 'potato-blight-lifecycle', 'Give an account of the potato blight fungus (Phytophthora infestans) under the heading: Lifecycle.',
        [menu('Spores airborne|germinate in humid conditions|haustoria absorb food (from cells)|sporangiophores grow out of the stomata|break off|produce zoospores (in water)|onto soil|infect tubers', [2] * 4,
              'Any four, 2 marks each (4×2m).')], blight, node='2-4')
    add('q3o1bii', 'Q3 Option One (b)(ii)', '3-3-2', 'potato-blight-symptoms', 'Give an account of the potato blight fungus (Phytophthora infestans) under the heading: Disease symptoms.',
        [menu('Leaf (or stem) has black spots|whitish mould (beard)|necrosis|tuber has brown-purple skin|shrunken areas|rusty brown colour inside|turns black', [2, 2], 'Any two, 2 + 2m.')], blight, node='2-4')
    add('q3o1biii', 'Q3 Option One (b)(iii)', '3-3-2', 'potato-blight-control', 'Give an account of the potato blight fungus (Phytophthora infestans) under the heading: Prevention and control measures.',
        [menu('Spray fungicide|plant resistant varieties|remove all tubers at harvesting|rotation|use certified seed|burn off haulms|earthing up|destroy volunteer plants in dumps or remove diseased plants', [2, 2],
              'Any two, 2 + 2m.')], blight, node='2-4')
    add('q3o1ci', 'Q3 Option One (c)(i)', '3-3-2', 'other-potato-diseases',
        'It is important to use certified seed potatoes in commercial growing because they are disease-free. Give two possible diseases of potato crops, other than blight, and the causative agent in each case.',
        [menu(['Disease: Leaf roll/ leaf mosaic/ virus X or virus Y Cause: Viruses', 'Disease: Blackleg or soft rot/ common scab Cause: Bacteria',
               'Disease: Silver scurf/ rust/ blotch/ dry rot/ gangrene/ powdery scab/ warts Cause: Fungus'], [4, 4],
              'Two diseases: 2×(2+2)m, each disease 2 and its cause 2.')], node='2-4')
    add('q3o1cii', 'Q3 Option One (c)(ii)', '3-3-1', 'donegal-seed-potatoes',
        'Explain why some regions of Ireland, e.g. Co. Donegal, are considered to be particularly suitable for the production of seed potatoes.',
        [menu('Low numbers of aphids|aphids transmit viruses|high wind speed|cooler temperature|Donegal isolated from main potato growing areas', [3, 3, 2],
              'Any three. ' + FIRST.format('3 + 3 + 2'))], node='2-3|2-4')
    calving = 'Discuss in detail the following points in relation to a dairy enterprise:'
    for key, ref, concept, heading, options, node in [
            ('q3o2ai', 'Q3 Option Two (a)(i)', 'calving-management', 'Management of calving',
             'Isolate or supervise|assist if required|cut umbilical cord|dip navel in iodine|dry calf|remove mucus|irritate nose if not breathing|stimulate circulation', '3-5'),
            ('q3o2aii', 'Q3 Option Two (a)(ii)', 'newborn-calf-environment', 'Environmental conditions in the first three days after birth',
             'indoors|clean disinfected area|warm|draught free or good ventilation|separate pens|dry bedding', '3-4'),
            ('q3o2aiii', 'Q3 Option Two (a)(iii)', 'newborn-calf-feeding', 'Feeding principles in the first three days after birth',
             'colostrum|from mother or other valid method|10% of body weight or 3-5 litres of colostrum|12 hours|whole milk or milk replacer', '3-4')]:
        add(key, ref, '4-3-2', concept, f'Discuss in detail the following point in relation to a dairy enterprise: {heading}.',
            [menu(options, [2, 2], 'Any two points, 2 + 2 (3×(2+2)m across the three headings).')], calving, node=node)
    rearing = 'Discuss in detail the rearing of dairy calves, from age three days to first housing, under the following headings:'
    add('q3o2bi', 'Q3 Option Two (b)(i)', '4-3-2', 'calf-rearing-management', 'Discuss in detail the rearing of dairy calves, from age three days to first housing, under the heading: Management.',
        [menu('disease prevention or example|weaning at 6-8 weeks or when rumen develops|moved to grass|dosing for parasites|early tagging|BVD sample|dehorning|castrate and relevant remark|delousing at housing|group penning|change bedding',
              [2] * 5, 'Any five, 2 marks each (5×2m).')], rearing, node='3-4')
    add('q3o2bii', 'Q3 Option Two (b)(ii)', '4-3-2', 'calf-rearing-feeding', 'Discuss in detail the rearing of dairy calves, from age three days to first housing, under the heading: Feeding principles required for optimum growth.',
        [menu('introduction to milk|feed milk replacer|hay or scratch factor at 7 days|feed concentrates indoors|grass at 8 weeks|feed meals after going on grass|leader-follower system|shortage of grass =>feed meals|fresh water supply (on grass and indoors)',
              [2] * 5, 'Any five, 2 marks each (5×2m).')], rearing, node='3-4')
    add('q3o2ci', 'Q3 Option Two (c)(i)', '4-3-1', 'calf-weight-at-housing', 'What is the expected liveweight of dairy calves at first housing?', [point('170 – 220 kg', 4)], node='3-3')
    add('q3o2cii', 'Q3 Option Two (c)(ii)', '4-3-1', 'slaughter-at-two-years', 'Explain why most beef animals are slaughtered at two years of age.',
        [menu('Target weight reached|fat laid down instead of muscle after 2 years|better meat quality|older cattle carcasses grade poorly or better kill-out percentage|frees up grass|better stocking rate|FCR disimproves with age or with fat deposition',
              [4] * 3, 'Any three, 4 marks each (3×4m).')], node='3-3')
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following describe a laboratory or field method:'
    for key, ref, topic, concept, aim, steps, note, node in [
            ('q4a', 'Q4(a)', '3-3-3', 'grass-mineral-ash', 'To determine the percentage mineral ash in a sample of freshly cut grass.',
             'Start with dry grass|weigh crucible|weigh crucible plus grass sample|calculate mass of sample|(gently) burn the sample|method of burning|to a constant mass|mineral ash left|result calculation', '', '2-6|0-1'),
            ('q4b', 'Q4(b)', '3-3-2', 'overgrazing-botanical-composition', 'To assess the effects of overgrazing on the botanical composition of a pasture sward.',
             '2 areas of equal size|quadrat|random|record plants present|control is area grazed normally|other area grazed bare|record plants present in both|repeat above|compare both samples for plants present', '', '2-6|0-1'),
            ('q4c', 'Q4(c)', '3-3-1', 'variety-yield-trial', 'To examine the effect on yield of growing different varieties of a named crop.',
             'Name crop|minimum 2 varieties|planting|same conditions|same sowing rate|same soil type|same area|same sowing date|same fertiliser treatment|same light levels|same weed or pest or disease control|same growing period|same harvesting date|same harvesting method|compare yields|method of measuring yield',
             ' The scheme credits any 3 of the "same ..." controls.', '2-3|0-1'),
            ('q4d', 'Q4(d)', '4-3-3', 'microbes-in-foodstuff', 'To show the presence of micro-organisms in an animal foodstuff.',
             'Agar plates|sterile|control not opened|inoculate one plate|with foodstuff|how (e.g. inoculating loop)|one aseptic technique|incubate|upside down|time for growth|colonies of bacteria|furry growth of fungi|control clear', '', '3-5|0-1')]:
        add(key, ref, topic, concept, 'Describe a laboratory or field method ' + aim[0].lower() + aim[1:],
            [menu(steps, [4] * 6, 'Any six, 4 marks each (6×4m).' + note)], lab, node=node)
    # Question 5 -------------------------------------------------------------
    add('q5ai', 'Q5(a)(i)', '4-1', 'polyoestrous', 'Sheep are polyoestrous. What does the term polyoestrous mean?',
        [point('Having several oestrous cycles in one year (or breeding season) or to come in heat more than once during a breeding season', 4)], node='3-0')
    add('q5aii', 'Q5(a)(ii)', '4-1', 'sheep-oestrous-cycle-length', 'What is the length of the oestrous cycle in sheep?', [point('15-19 days inclusive', 4)], node='3-0')
    add('q5aiii', 'Q5(a)(iii)', '4-1', 'day-length-and-breeding', 'Explain the connection between day length and the breeding season in sheep.',
        [menu('Shorter days = less light|short day breeders or autumn or named autumn month|pineal gland|hormone or melatonin|stimulate ovulation|photo-oestrous|resumption of cycling', [1] * 4,
              'Any four, 1 mark each (4×1m).')], node='3-0')
    add('q5b', 'Q5(b)', '4-1', 'ewe-reproductive-system', 'Draw a large labelled diagram of the reproductive system of a ewe and label four parts.',
        [point('Diagram: Must have ovaries and oviducts and uterus and vagina', None, 'Diagram: 4, 2, 0m.', kind='criterion'),
         point('ovaries/ oviduct/ uterus/ endometrium/ vagina/ cervix/ vulva', None, 'Labels: any four, 2 marks each (4×2m).')],
        marks=12, tariff={'kind': 'questionTotal', 'notation': '4, 2, 0 + 4×2m'}, node='3-0')
    add('q5c', 'Q5(c)', '4-3-2', 'breeding-out-of-season', 'Describe the key steps involved in ‘breeding out of season’ to produce lambs for the early spring market.',
        [menu('Insert sponges (in ewes’ vaginas)|progesterone (soaked)|leave for 12-16 days|remove sponges|ewes injected with PMSG|mated 1-2 days later|ram to ewe ratio 1:10', [4] * 3,
              'Any three, 4 marks each (3×4m).')], node='3-4')
    add('q5d', 'Q5(d)', '4-3-2', 'culling-ewes', 'Outline four reasons for culling ewes.',
        [menu('Udders damaged|barren|prolapsed vagina|broken mouth or teeth damaged|poor condition score|lambing problems|poor mothers|bad feet|age|poor prolificacy (single lambs)|disease or injury', [3] * 4,
              'Any four, 3 marks each (4×3m).')], node='3-4')
    # Question 6 -------------------------------------------------------------
    add('q6a', 'Q6(a)', '3-3-2', 'fertiliser-rate-factors', 'List and explain four factors a farmer should take into consideration when deciding how much fertiliser to apply to a crop.',
        [menu('Soil type or sandy or clay or loam [low fertility in sand, high fertility in clay]|previous crop [some remove more than others]|crop being sown [some crops need more]|result of a soil test [high or low]|pH of soil [affects nutrient availability]|number of years since under grass cover [improves fertility]|time of year [affects amount of fertiliser applied]|environmental scheme [limits fertiliser use]|stage of growth [variable requirements]',
              [4] * 4, 'Any four: 4×(2+2)m, each factor 2 and its effect (in square brackets) 2. [Cause and effect required]')], node='2-4|1-6')
    add('q6b', 'Q6(b)', '3-3-2', 'crop-yield-factors', 'Other than fertilisers, list and explain four additional factors that would influence the yield of a crop at harvest.',
        [menu('Variety sown|certified seed|climate too wet or too cold or too dry|disease|pests|competition from weeds|sunshine levels (aspect) [affect photosynthesis]|time of sowing|delay in harvesting|length of growing season|sprouting|named soil type',
              [4] * 4, 'Any four: 4×(2+2)m, each factor 2 and its effect 2. [Cause and effect required]')], node='2-4')
    add('q6ci', 'Q6(c)(i)', '3-1', 'transpiration', 'What is meant by the term transpiration?',
        [menu(['Transpiration: the water evaporating from the leaf of a plant', 'through the stomata'], [2, 2], '2 + 2m.')], node='2-0')
    add('q6cii', 'Q6(c)(ii)', '3-1', 'transpiration-factors', 'Describe how any three environmental factors affect the rate of transpiration in a plant.',
        [menu('Light intensity [more light, more transpiration]|(relative) humidity [dry air, more transpiration]|air movement [faster wind, more transpiration]|temperature [hotter, more transpiration]|soil water level [dry soil, less transpiration]|very fast wind [stomata close or less transpiration]|CO2 concentration [stomata close or less transpiration]',
              [4] * 3, 'Any three: 3×(2+2)m, each factor 2 and its effect (in square brackets) 2. [Cause and effect required]')], node='2-0')
    # Question 7 -------------------------------------------------------------
    add('q7ai', 'Q7(a)(i)', '4-1', 'law-of-independent-assortment', 'State the Law of Independent Assortment.',
        [point('When gametes are formed each member of a pair of alleles may be inherited with any one of another pair', 4)], node='3-6')
    add('q7aii', 'Q7(a)(ii)', '4-1', 'sex-linkage-clone-polyploid', 'Explain the following terms: 1. Sex linkage. 2. Clone. 3. Polyploid.',
        [point('1. Gene located on sex chromosomes (or on X or on Y chromosomes) or gene found on the X chromosome but has no copy on the Y chromosome', 4, '3×4m.'),
         point('2. (A group of) cells or organisms that are genetically identical to each other (or have the same DNA) or organism reproduced from a single cell of a donor organism or (a group of) organisms produced by asexual reproduction', 4),
         point('3. More than two copies of each chromosome (in a cell)/ 3N or 4N or similar notation', 4)], node='3-6')
    add('q7b', 'Q7(b)', '4-1', 'red-straight-coat-cross',
        '(i) State the genotypes of the bull and cow using the above notation. (ii) State the four possible calf phenotypes. (iii) Which of the possible phenotypes indicate that independent assortment has taken place?',
        [menu(['Bull: RrSs', 'Cow: rrss'], [2, 2], '(i) Genotypes: 2 each. 8×2m across the eight answers.'),
         menu(['Red straight', 'red curly', 'black straight', 'black curly'], [2] * 4, '(ii) The four phenotypes: 2 each.'),
         menu(['Red curly', 'black straight'], [2, 2], '(iii) Phenotypes showing independent assortment: 2 each.')],
        'In cattle, the allele for red coat (R) is dominant to the allele for black coat (r) and the allele for straight coat (S) is dominant to the allele for curly coat (s). '
        'If a bull with a red straight coat is mated with a cow with a black curly coat, the resulting calf has an equal chance of showing one of four phenotypes.', node='3-6')
    add('q7c', 'Q7(c)', '4-3-2', 'sexed-semen-advantages',
        'Discuss the advantages of using sexed semen rather than conventional semen to those dairy farmers planning to increase milk production.',
        [point('More heifer calves (or fewer unwanted bull calves)', 4, 'Sexed semen: this point 4, then any three more (3×4m).'),
         menu('Less calving difficulty [females calves smaller]|Herd improvement or more replacements for top milkers or higher milk yield|Males are less valuable|Fewer cows required for breeding or more diverted to beef|Faster rate of herd expansion',
              [4] * 3, 'Any three, 4 marks each.')],
        'The abolition of milk quotas will give many dairy farmers scope to increase milk production for the first time in more than thirty years.', node='3-6|3-4')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of the parts (a), (b), (c).'
    add('q8a', 'Q8(a)', '2-3', 'nitrogen-cycle', 'Describe with the aid of a diagram the processes involved in the nitrogen cycle.',
        [point('Diagram', None, 'Diag. 4, 0m.', kind='criterion'),
         point('Nitrogen gas to useable compounds or to nitrates/ nitrogen fixation/ plant protein to animal protein/ excretion releasing nitrogenous compounds/ urea to ammonia(um)/ death and decomposition/ dead organic matter to ammonia(um)/ ammonium to nitrite/ nitrite to nitrate/ nitrification/ nitrates to plant protein/ nitrogen compounds to nitrogen gas/ denitrification/ role of lightning',
               None, 'Any ten points, 2 marks each (10×2m), including these and the terms below.'),
         point('Any 2 of the following terms correctly placed on diagram: Rhizobium/ Azotobacter/ Nitrosomonas/ Nitrobacter', None)],
        twoof, marks=24, tariff={'kind': 'questionTotal', 'notation': 'Diag. 4,0m + 10×2m'}, node='1-6')
    add('q8bi', 'Q8(b)(i)', '3-3-2', 'grassland-management-practices', 'Outline the principal practices required for good grassland management.',
        [menu('Sowing|seed mixture used|reseeding|weed control|establishment method|fertility or soil pH - liming|grazing methods|recovery time (3 weeks for grazing or 6 weeks for silage)|planning for hay or silage or grass herbage requirements|stocking rate|topping (promotes tillering)',
              [3] * 4, 'Any four, 3 marks each (4×3m).')], twoof, node='2-6')
    add('q8bii', 'Q8(b)(ii)', '3-3-2', 'mixed-grazing-benefits', 'Give two benefits of mixed grazing.',
        [menu('Sheep grazing close to ground or to base of grass increases tillering (denser sward)|more DM|sheep eat around cattle dung pats or fewer tufts of grass formed or cattle more selective grazers than sheep or more grass utilised|more recycling of nutrients (different dung + urine composition)|fewer parasite problems (in each type of animal)|more productivity (10-15%)|sheep eat ragwort',
              [3, 3], 'Any two, 3 marks each (2×3m).')], twoof, node='2-6')
    add('q8biii', 'Q8(b)(iii)', '4-3-1', 'livestock-units', '1. What is meant by the term livestock units? 2. Give two examples to show your understanding of the term livestock units.',
        [menu(['Measurement of livestock grazing', 'equivalent to food consumed by a mature (550 kg) liveweight cow'], [2, 2], 'Livestock unit (LU) definition: 2 + 2m.'),
         menu('2 year old cattle = 1.0 LU|1-2 year old cattle = 0.6 LU|Less than a year old = 0.4 LU|Sheep = each ewe or ram = 0.2 LU|Sheep 1 > year = 0.16LU|Sheep < 1 year = 0.1LU|Horse = 1-1.5 LU', [1, 1],
              'Examples: any two, 1 mark each (2×1m).')], twoof, node='3-3|2-6')
    members = [('i', 'Topdressing', 'fertilizer (in any form)|added to the surface (of the soil or to the growing crop)'),
               ('i', 'Topping', 'mowing grass to a height of 5-7 cm|encourages tillering|removes old grass|aids weed control|adds organic matter'),
               ('ii', 'Hepatic vein', 'brings blood away from the liver|to inferior vena cava or to heart'),
               ('ii', 'Hepatic portal vein', 'carries blood rich in nutrients|from the small intestine|to the liver'),
               ('iii', 'Raised bog', 'formed in lakes or hollows or river valleys|accumulation of organic matter closes the lake over (rises above surface level)|very deep|more agricultural value'),
               ('iii', 'Blanket bog', 'high rainfall|high humidity|mountains|west coast|covers landscape|shallow'),
               ('iv', 'Tilling', 'the process involved in preparing a seed-bed|involves ploughing|harrowing or rotavating|sowing|rolling (single pass or minimum tillage system explained)'),
               ('iv', 'Tillering', 'The ability of plants belonging to family Gramineae|to produce side shoots|from buds|at the base of the plant')]
    add('q8c', 'Q8(c)', '3-3-2', 'distinguishing-paired-terms',
        'Distinguish between the members of any three of the following pairs of terms: (i) Top dressing and topping. (ii) Hepatic vein and hepatic portal vein. (iii) Raised bog and blanket bog. (iv) Tilling and tillering.',
        [menu(pool, [2, 2], f'({k}) {label}: two points, 2 + 2.' + (' 3×(4+4)m: each term 4, split into 2 + 2, for any three pairs.' if i == 0 else ''))
         for i, (k, label, pool) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='2-6|3-0|1-0|2-3')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following:'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '3-3-3', 'rancid-silage', 'The formation of rancid silage.',
             'Fermentation by clostridia|of carbohydrates|into butyric acid|wet harvesting encourages clostridia or dilutes sugar concentration|not enough lactic acid to lower pH or pH too high to prevent clostridial activity|not wilted|no additive used|low carbohydrate levels|lack of anaerobic conditions|contamination from soil or slurry or FYM', '2-6'),
            ('q9b', 'Q9(b)', '3-3-2', 'slurry-before-silage', 'Spreading slurry at least seven weeks before cutting grass for silage.',
             'Allow light in for photosynthetic activity|avoid caking on grass|allow time to act|allow time to decompose|provides nutrients for growth|avoid contamination of silage|grass needs 6 weeks to grow', '2-6|1-6'),
            ('q9c', 'Q9(c)', '2-3', 'hedgerow-retention', 'Retention and conservation of hedgerows on a farm.',
             'Protection for flora or fauna or food chain|promote diversity|shelter for crops or animals or buildings or warmer soil|noise reduction or aesthetic|REPS or environmental scheme|wildlife habitat or corridor|boundaries', '1-6'),
            ('q9d', 'Q9(d)', '4-3-2', 'dairy-milk-testing', 'The testing of milk by dairies.',
             'Test for bacteria to show hygiene (TBC)|test for white blood cells to show mastitis levels (SCC)|antibiotic test to show presence or not (Delvo test)|water test to show dilution|sediment test to show particle contamination|thermoduric test counts number of thermo resistant bacteria|test for % milk solids', '3-4'),
            ('q9e', 'Q9(e)', '4-3-3', 'burdizzo-castration', 'Using a burdizzo in beef rearing enterprises.',
             'Castration of male animals (bulls)|prevents unwanted breeding|crushes spermatic cord|cuts off blood supply to the testes|safety (easier to manage animals)|produces steers or bullocks for beef (small market for bull beef or tainted meat)|less risk of infection', '3-5')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item,
            [menu(points, [7, 3, 2], 'Any three points. ' + FIRST.format('7 + 3 + 2'))], why, node=node)
    assert len(p.tasks) == 58, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('58 base tasks, one card each. A scale the scheme prints across a part\'s (i) and (ii) (Q1(h), (j)) is one task with the scale stated; '
                          'parts priced separately are separate tasks, and numbered items inside a part stay on its card. The three Q3 Option Two (a) headings carry 2 + 2 each; '
                          'Q8(c) is one card for the choice of three pairs from four.')
