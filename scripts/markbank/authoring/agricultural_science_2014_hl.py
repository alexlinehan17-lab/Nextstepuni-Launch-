"""2014 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 12 scheme pages were inspected and the independent census transcribed
before authoring: 61 base tasks, one card each. Under the scheme's convention (PDF page 4) a
scale such as 6 + 3 + 1 pays the first correct answer 6 and each later one the next value; a
part with one pool keeps the steps on its menu, and parts priced separately at (i), (ii) and (iii)
are separate tasks. The Q6(b) heifer stages carry 2 + 2 + 1 each and are separate tasks. The
milk adulteration tests (Q1(a)) and the named cereal (Q8(b)) are answer routes; the Q8(c) choice
of three pairs from four is one card whose eight members are parts. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': 'c69165b7f74f3a6bd4f5d73343243a1a90ca27c5fa12c9097a0eb11cb8930d85',
          'markingschemes': '555f4e5c9084b028cb3281d987f7c4712f78bc1ce46fb5d83a511351e48d2e09'}
SELECTIONS = {
    '932a8e52a6283663': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '7a31b0578e3b8b2b': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    'de28b762bc658a72': ('open', 'Q3 Option One (a): any two circumstances with their effects; the scheme lists six (a marking menu).'),
    '04d7be763f6c6bb4': ('open', 'Q3 Option Two (b)(iii): any three labels on the candidate\'s own drawing (a marking criterion).'),
    'db259620a3660759': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    'd04f2be67c534ade': ('open', 'Q5(c): any three effects of drought; the scheme lists the pool (a marking menu).'),
    '6185e362cc5625cb': ('open', 'Q6(c)(i): any two secretions with their organs; the scheme lists five (a marking menu).'),
    '9c45287d7055a59a': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    'b0a1853c27659dd3': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    '14b4cf4592c6d202': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (3, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
    (2, 'Describe a method for the detection of adulteration of milk by water', 'closed', 'Q1(a): the scheme gives a freezing-point, a density and a total-solids method, kept as answer routes on one card.'),
    (5, 'Describe in detail the production of a named cereal crop', 'closed', 'Q8(b): the scheme tabulates barley, wheat, oats and maize, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1(a)': 'dairy-cattle|scientific-practices-experiments-investigations', 'Q1(b)': 'animal-physiology-circulatory-system', 'Q1(c)': 'soil-science',
    'Q1(d)': 'animal-diseases', 'Q1(e)': 'classification-of-animals-plants', 'Q1(f)': 'soil-science', 'Q1(g)': 'plant-physiology',
    'Q1(h)': 'fertilisers-pollution-environment-cycles|grassland', 'Q1(i)': 'animal-physiology-digestive-system|scientific-practices-experiments-investigations',
    'Q1(j)': 'classification-of-animals-plants|crop-production',
    'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'grassland', 'Q3 Option Two (a)': 'animal-physiology-digestive-system', 'Q3 Option Two (b)': 'animal-diseases|classification-of-animals-plants',
    'Q3 Option Two (c)': 'animal-diseases|sheep',
    'Q4': 'scientific-practices-experiments-investigations', 'Q4(a)': 'scientific-practices-experiments-investigations|soil-science|crop-production',
    'Q4(b)': 'scientific-practices-experiments-investigations|crop-production', 'Q4(c)': 'scientific-practices-experiments-investigations|dairy-cattle',
    'Q4(d)': 'scientific-practices-experiments-investigations|plant-physiology',
    'Q5(a)': 'plant-physiology|crop-production', 'Q5(b)': 'soil-science|plant-physiology', 'Q5(c)': 'crop-production|plant-physiology', 'Q5(d)': 'soil-science',
    'Q6': 'dairy-cattle', 'Q6(c)': 'animal-physiology-digestive-system',
    'Q7': 'genetics', 'Q7(b)': 'genetics|innovation-and-biotechnology-in-agriculture', 'Q7(d)': 'beef-cattle|pigs|sheep',
    'Q8(a)': 'pigs', 'Q8(b)': 'crop-production', 'Q8(c)': 'soil-science|animal-physiology-reproductive-systems|animal-diseases|crop-production',
    'Q9(a)': 'animal-physiology-digestive-system', 'Q9(b)': 'soil-science', 'Q9(c)': 'fertilisers-pollution-environment-cycles', 'Q9(d)': 'sheep',
    'Q9(e)': 'animal-diseases',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1(a)': (P((2, 0.074, 0.134)), P((5, 0.081, 0.2115))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(b)': (P((2, 0.074, 0.104), (2, 0.134, 0.164)), P((5, 0.081, 0.111), (5, 0.217, 0.272))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(c)': (P((2, 0.074, 0.104), (2, 0.164, 0.194)), P((5, 0.081, 0.111), (5, 0.277, 0.347))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(d)': (P((2, 0.074, 0.104), (2, 0.194, 0.224)), P((5, 0.081, 0.111), (5, 0.352, 0.407))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(e)': (P((2, 0.074, 0.104), (2, 0.224, 0.254)), P((5, 0.081, 0.111), (5, 0.412, 0.46))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(f)': (P((2, 0.074, 0.104), (2, 0.254, 0.284)), P((5, 0.081, 0.111), (5, 0.463, 0.506))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(g)': (P((2, 0.074, 0.104), (2, 0.284, 0.314)), P((5, 0.081, 0.111), (5, 0.51, 0.636))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(h)': (P((2, 0.074, 0.104), (2, 0.314, 0.356)), P((5, 0.081, 0.111), (5, 0.642, 0.69))),  # hand-set: the scheme centres each part label in its cell, so the drafted cut fell mid-answer
    'Q1(i)(i)': (P((2, 0.074, 0.104), (2, 0.358, 0.379, 0, 0.732)), P((5, 0.081, 0.111), (5, 0.690, 0.737))),  # hand-set: the scheme prints this part as one table row; the paper crop stops short of the plant drawing
    'Q1(i)(ii)': (P((2, 0.074, 0.104), (2, 0.358, 0.3945, 0, 0.732)), P((5, 0.081, 0.111), (5, 0.690, 0.737))),  # hand-set: the scheme prints this part as one table row; the paper crop stops short of the plant drawing
    'Q1(j)(i)': (P((2, 0.074, 0.104), (2, 0.408, 0.425, 0, 0.6)), P((5, 0.081, 0.111), (5, 0.740, 0.810))),  # hand-set: the scheme prints this part as one table row; the paper crop stops short of the plant drawing
    'Q1(j)(ii)': (P((2, 0.074, 0.104), (2, 0.408, 0.440, 0, 0.6)), P((5, 0.081, 0.111), (5, 0.740, 0.810))),  # hand-set: the scheme prints this part as one table row; the paper crop stops short of the plant drawing
    'Q1(j)(iii)': (P((2, 0.074, 0.104), (2, 0.408, 0.425, 0, 0.6), (2, 0.440, 0.455, 0, 0.6)), P((5, 0.081, 0.111), (5, 0.740, 0.810))),  # hand-set: the scheme prints this part as one table row; the paper crop stops short of the plant drawing
    'Q2(a)(i)': (P((2, 0.633, 0.650)), P((6, 0.077, 0.098), (6, 0.094, 0.1105))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q2(a)(ii)': (P((2, 0.633, 0.6495, 0, 0.18), (2, 0.6495, 0.6645)), P((6, 0.077, 0.098), (6, 0.1105, 0.1415))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q2(a)(iii)': (P((2, 0.633, 0.6495, 0, 0.18), (2, 0.6645, 0.680)), P((6, 0.077, 0.098), (6, 0.1415, 0.174))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q2(b)(i)': (P((2, 0.691, 0.711)), P((6, 0.077, 0.098), (6, 0.183, 0.204))),
    'Q2(b)(ii)': (P((2, 0.711, 0.736)), P((6, 0.077, 0.098), (6, 0.204, 0.273))),
    'Q2(c)': (P((2, 0.736, 0.789)), P((6, 0.077, 0.098), (6, 0.273, 0.472))),
    'Q3 Option One (a)': (P((3, 0.074, 0.163)), P((6, 0.472, 0.598))),
    'Q3 Option One (b)(i)': (P((3, 0.074, 0.103), (3, 0.163, 0.238)), P((6, 0.472, 0.502), (6, 0.598, 0.619))),
    'Q3 Option One (b)(ii)': (P((3, 0.074, 0.103), (3, 0.163, 0.208), (3, 0.238, 0.283)), P((6, 0.472, 0.502), (6, 0.619, 0.719))),
    'Q3 Option One (c)': (P((3, 0.074, 0.103), (3, 0.283, 0.374)), P((6, 0.472, 0.502), (6, 0.719, 0.804))),
    'Q3 Option Two (a)(i)': (P((3, 0.419, 0.483)), P((7, 0.081, 0.132))),
    'Q3 Option Two (a)(ii)': (P((3, 0.419, 0.450), (3, 0.483, 0.525)), P((7, 0.081, 0.111), (7, 0.132, 0.167))),
    'Q3 Option Two (b)(i)': (P((3, 0.419, 0.450), (3, 0.525, 0.559)), P((7, 0.081, 0.111), (7, 0.167, 0.188))),
    'Q3 Option Two (b)(ii)': (P((3, 0.419, 0.450), (3, 0.525, 0.544), (3, 0.559, 0.574)), P((7, 0.081, 0.111), (7, 0.188, 0.219))),
    'Q3 Option Two (b)(iii)': (P((3, 0.419, 0.450), (3, 0.525, 0.544), (3, 0.574, 0.613)), P((7, 0.081, 0.111), (7, 0.219, 0.263))),
    'Q3 Option Two (c)': (P((3, 0.419, 0.450), (3, 0.613, 0.719)), P((7, 0.081, 0.111), (7, 0.263, 0.424))),
    'Q4(a)': (P((3, 0.719, 0.779)), P((7, 0.424, 0.515))),
    'Q4(b)': (P((3, 0.719, 0.749), (3, 0.779, 0.809)), P((7, 0.515, 0.644))),  # the Q4 head shares its line with (a)'s answer; left out
    'Q4(c)': (P((3, 0.719, 0.749), (3, 0.809, 0.839)), P((7, 0.644, 0.729))),  # the Q4 head shares its line with (a)'s answer; left out
    'Q4(d)': (P((3, 0.719, 0.749), (3, 0.839, 0.875)), P((7, 0.729, 0.800))),  # stops above the page footer; the Q4 head shares its line with (a)'s answer
    'Q5(a)': (P((4, 0.075, 0.106)), P((8, 0.081, 0.141))),  # stops above (b)(i), which the draft ran into
    'Q5(b)(i)': (P((4, 0.107, 0.137), (4, 0.137, 0.154)), P((8, 0.143, 0.1775))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q5(b)(ii)': (P((4, 0.107, 0.137), (4, 0.154, 0.169)), P((8, 0.1775, 0.2065))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q5(b)(iii)': (P((4, 0.107, 0.137), (4, 0.169, 0.186)), P((8, 0.2065, 0.240))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q5(c)': (P((4, 0.196, 0.226)), P((8, 0.257, 0.338))),  # the Q5 head shares its line with (a)'s answer; left out
    'Q5(d)(i)': (P((4, 0.226, 0.368)), P((8, 0.336, 0.353))),  # the Q5 head shares its line with (a)'s answer; left out
    'Q5(d)(ii)': (P((4, 0.226, 0.349), (4, 0.368, 0.499)), P((8, 0.336, 0.352, 0, 0.10), (8, 0.353, 0.375))),  # with the (d) label; stops above Q6
    'Q6(a)': (P((4, 0.499, 0.545)), P((8, 0.438, 0.512))),  # stops above the (b) table head
    'Q6(b)(i)': (P((4, 0.545, 0.608)), P((8, 0.438, 0.460), (8, 0.514, 0.583))),  # with the table head; the drafted cut took only half of it
    'Q6(b)(ii)': (P((4, 0.545, 0.589), (4, 0.608, 0.624)), P((8, 0.438, 0.460), (8, 0.514, 0.5525), (8, 0.583, 0.651))),  # with the table head; the drafted cut took only half of it
    'Q6(b)(iii)': (P((4, 0.545, 0.589), (4, 0.624, 0.639)), P((8, 0.438, 0.460), (8, 0.514, 0.5525), (8, 0.651, 0.703))),  # with the table head; the drafted cut took only half of it
    'Q6(b)(iv)': (P((4, 0.545, 0.589), (4, 0.639, 0.664)), P((8, 0.438, 0.460), (8, 0.514, 0.5525), (8, 0.703, 0.758))),  # with the table head; the drafted cut took only half of it
    'Q6(c)(i)': (P((4, 0.664, 0.699)), P((8, 0.438, 0.468), (8, 0.758, 0.809))),
    'Q6(c)(ii)': (P((4, 0.699, 0.747)), P((8, 0.438, 0.468), (8, 0.809, 0.843))),
    'Q7(a)(i)': (P((5, 0.062, 0.0795), (5, 0.092, 0.109)), P((9, 0.158, 0.1745))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q7(a)(ii)': (P((5, 0.062, 0.0795), (5, 0.109, 0.125)), P((9, 0.1745, 0.223))),  # hand-set: the scheme table prints these subparts without separate part heads
    'Q7(b)': (P((5, 0.135, 0.226)), P((9, 0.262, 0.385))),
    'Q7(c)(i)': (P((5, 0.226, 0.331)), P((9, 0.385, 0.415))),
    'Q7(c)(ii)': (P((5, 0.226, 0.300), (5, 0.331, 0.421)), P((9, 0.415, 0.551))),
    'Q7(d)': (P((5, 0.421, 0.526)), P((9, 0.551, 0.591))),
    'Q8(a)': (P((5, 0.526, 0.586)), P((10, 0.106, 0.212))),  # stops above the (b) table head
    'Q8(b)': (P((5, 0.526, 0.556), (5, 0.586, 0.721)), P((10, 0.106, 0.124, 0, 0.12), (10, 0.216, 0.523))),  # with its table head; the Q8 head shares a line with (a)'s answer
    'Q8(c)': (P((5, 0.526, 0.556), (5, 0.721, 0.838)), P((10, 0.106, 0.124, 0, 0.12), (10, 0.523, 0.879))),  # stops above the page footer; the Q8 head shares a line with (a)'s answer
    'Q9(a)': (P((6, 0.046, 0.106)), P((11, 0.126, 0.194))),
    'Q9(b)': (P((6, 0.046, 0.075), (6, 0.106, 0.135)), P((11, 0.194, 0.246))),
    'Q9(c)': (P((6, 0.046, 0.075), (6, 0.135, 0.166)), P((11, 0.246, 0.313))),
    'Q9(d)': (P((6, 0.046, 0.075), (6, 0.166, 0.196)), P((11, 0.313, 0.381))),
    'Q9(e)': (P((6, 0.046, 0.075), (6, 0.196, 0.251)), P((11, 0.381, 0.442))),
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'
OAT = 'agsci-2014-hl-paper-oat-plant'
TABLE = 'agsci-2014-hl-paper-soil-water-table'


def split(text, note=None, route=None, kind='point'):
    """An unpriced row: the scheme prices the scale or the question, not the row."""
    row = point(text, None, note, kind)
    if route:
        row['route'] = route
    return row


def build():
    p = Paper(2014, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 12, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    six = 'Answer any six of the parts (a) – (j).'
    # Question 1 -------------------------------------------------------------
    tests = [('freezing-point', 'Freezing point', 'find freezing point of sample (melting point)|compare with freezing point of milk|if freezing point is higher, milk is adulterated|above -0.5oC'),
             ('density', 'Density', 'find density of sample|correct method|compare with density of milk|less than milk|<1.03'),
             ('total-solids', 'Total solids', 'find % solids (or water)|method|compare with pure milk|<10%')]
    rows, variants = routes([(slug, label, [menu(steps, [6, 3, 1], f'{label}: any three points. ' + FIRST.format('6 + 3 + 1'))]) for slug, label, steps in tests])
    add('q1a', 'Q1(a)', '4-3-2', 'milk-adulteration-test', 'Describe a method for the detection of adulteration of milk by water.', rows, six,
        selection=closed(1, [label for _, label, _ in tests]), node='3-4|0-1', extra={'answerVariants': variants})
    for key, ref, topic, concept, question, options, node in [
            ('q1b', 'Q1(b)', '4-1', 'lymphatic-system-functions', 'Give three functions of the lymphatic system in mammals.',
             'Antibody production|absorbs lipids|white blood cell or lymphocyte production|collects extracellular fluid|transport of materials (e.g. hormones, white blood cells, extracellular fluid, lipids)|bacteria filtered out at nodes', '3-0'),
            ('q1c', 'Q1(c)', '2-3', 'aspect-and-soil-temperature', 'Explain how the aspect of a field may affect the temperature of a soil in early spring.',
             'Soil temperature increases sooner in south-facing field or later in north-facing field|more exposure to sun in south-facing area or less exposure in north-facing area|soil dries faster in south facing|more exposed to prevailing wind in south facing', '1-5'),
            ('q1d', 'Q1(d)', '4-3-3', 'notifiable-diseases', 'Name three notifiable diseases of farm animals in Ireland.',
             'Scrapie|Aujeszky’s disease|sheep scab|swine fever|rabies|Newcastle disease|anthrax|brucellosis|foot and mouth|BSE|TB|avian ‘flu|blue tongue|Johne’s disease|BVD', '3-5'),
            ('q1e', 'Q1(e)', '3-2', 'angiosperm-features', 'Give three features of angiosperms.',
             'Flowers|seeds|fruit|endosperm present|female organs smaller|smaller pollen grains', '2-1'),
            ('q1f', 'Q1(f)', '2-2-1', 'lime-in-cation-exchange', 'Fully outline the role of lime in cation exchange.',
             'Calcium ions (or magnesium ions)|soil solution|swap places with or replace H+ or K+ or Al3+|on the surface of colloids (humus or clay)|colloids negative', '1-2')]:
        add(key, ref, topic, concept, question, [menu(options, [6, 3, 1], 'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node=node)
    add('q1g', 'Q1(g)', '3-1', 'wind-versus-insect-pollination', 'Compare the structure of wind-pollinated and insect-pollinated flowers.',
        [menu('nectaries absent (nectaries present)|inconspicuous petals (conspicuous petals)|large amount of pollen produced (less pollen)|small pollen grains (large pollen grains)|smooth pollen grains (spiky pollen grains)|anthers hang outside flower (anthers inside flower)|stigma outside flower (stigma inside flower)|*feathery stigma (*sticky stigma)',
              [4, 4, 1, 1], 'Wind (Insect): any four. ' + FIRST.format('4 + 4 + 1 + 1') + ' *must state both for full marks. '
              '[Accept ‘reproductive organs outside flower (inside flower)’ for one point only] Marks may be awarded for correctly labelled diagrams.')], six, node='2-0')
    add('q1h', 'Q1(h)', '2-3', 'autumn-nitrogen', 'Give a full explanation why it is not recommended to spread nitrogen fertiliser on grassland in late autumn.',
        [menu('Poor growth|leaching|denitrification|pollution|wasteful|nitrates directive|lower temperature inhibits bacteria', [4, 4, 1, 1], 'Any four. ' + FIRST.format('4 + 4 + 1 + 1'))],
        six, node='1-6|2-6')
    add('q1ii', 'Q1(i)(i)', '4-1', 'protein-elements', 'List the four chemical elements always present in protein.',
        [menu('Carbon|hydrogen|oxygen|nitrogen', [2] * 4, 'All four, 2 marks each (4×2m). [accept symbols]')], six, node='3-0')
    add('q1iii', 'Q1(i)(ii)', '4-1', 'protein-reagent', 'Name the reagent used to test for the presence of protein in a food.',
        [point('Biuret / sodium hydroxide and copper sulphate', 2)], six, node='3-0|0-1')
    add('q1ji', 'Q1(j)(i)', '3-2', 'identify-oat-plant', 'Identify the plant shown in the diagram.', [point('(i) Oats', 4)], six, figure=OAT, node='2-1')
    add('q1jii', 'Q1(j)(ii)', '3-2', 'oat-family', 'To which family does this plant belong?', [point('(ii) Gramineae', 4)], six + ' (i) Identify the plant shown in the diagram.',
        figure=OAT, node='2-1')
    card = add('q1jiii', 'Q1(j)(iii)', '3-2', 'oat-parts', 'Name the parts labelled A and B.', [point('A: spikelet', 1), point('B: petiole / stalk / panicle', 1)],
               six + ' (i) Identify the plant shown in the diagram.', figure=OAT, node='2-1')
    card['labelKey'] = [dict(letter='A', meaning='Spikelet', askedInThisQuestion=True), dict(letter='B', meaning='Petiole or stalk or panicle', askedInThisQuestion=True)]
    # Question 2 -------------------------------------------------------------
    add('q2ai', 'Q2(a)(i)', '2-1', 'metamorphic-rock-factors', 'What are the two main factors involved in the formation of metamorphic rocks?',
        [menu(['Heat', 'pressure'], [2, 2], '2m + 2m: heat and pressure.')], node='1-0')
    add('q2aii', 'Q2(a)(ii)', '2-1', 'metamorphic-rocks-and-parents', 'Name two metamorphic rocks and in each case state which rock type it develops from.',
        [menu('Marble from limestone|slate (or schist) from shale|quartzite from sandstone|gneiss from granite|greenstone from basalt', [4, 4],
              'Any two: 2×(2+2)m, the metamorphic rock 2 and its parent rock 2.')], node='1-0')
    add('q2aiii', 'Q2(a)(iii)', '2-1', 'parent-material-influence', 'Explain one way in which parent material influences the type of soil that eventually develops.',
        [menu('(pH) acidic or alkaline|coarse or fine (texture)|minerals the same as rock|soil structure|temperature', [2, 2], '2m + 2m: one way, explained.')], node='1-0')
    add('q2bi', 'Q2(b)(i)', '2-2-3', 'adding-organic-matter', 'Give two methods by which organic matter may be added to a soil.',
        [menu('Dung|slurry|seaweed|ploughing-in material|earthworms|bacteria|compost', [2, 2], 'Any two, 2m + 2m.')], node='1-4')
    add('q2bii', 'Q2(b)(ii)', '2-2-3', 'organic-matter-in-tillage', 'Outline the importance of maintaining a satisfactory level of organic matter in a tillage soil.',
        [menu('Structure and aggregation|erosion prevention|nutrient reservoir|humus source|ion exchange|water reservoir|improves aeration|dark colour - soil warms up faster|increases earthworms|improves drainage|lowers pH|cross compliance',
              [4] * 4, 'Any four, 4 marks each (4×4m).')], node='1-4|1-5')
    add('q2c', 'Q2(c)', '2-2-2', 'inorganic-matter-in-soil', 'Describe a laboratory method to determine the amount of inorganic material in a sample of soil.',
        [point('*Soil must be dry at start', 2, '*2×2m for the two essential points, then any four more, 2 marks each (4×2m). [*essential points]'),
         point('*remaining mass = inorganic matter', 2),
         menu('find mass of soil sample|burn or roast|over Bunsen|in crucible|to constant mass|cool|loss of mass = organic matter|calculation of inorganic matter', [2] * 4, 'Any four more, 2 marks each.')],
        node='1-3|0-1')
    # Question 3 -------------------------------------------------------------
    add('q3o1a', 'Q3 Option One (a)', '3-3-3', 'fodder-crisis-circumstances',
        'During 2013 many farmers in Ireland experienced a fodder crisis. Describe any two circumstances, and their effects, that could contribute to a widespread shortage of fodder.',
        [menu('low temperatures : poor grass growth rates|long winter (cold or wet spring) : shorter growing season|high level of rainfall : difficult conditions for hay or silage making or poaching of land|poor planning : insufficient fodder|poaching : land unsuitable for grass growth or trampled grass|drought : poor grass growth',
              [8, 8], 'Any two: 2×(4+4)m, each circumstance 4 and its effect 4 (Circumstance : effect).')], node='2-6')
    hay = 'In 2013 a larger number of farmers than in recent years returned to haymaking as a method of conserving grass.'
    add('q3o1bi', 'Q3 Option One (b)(i)', '3-3-3', 'return-to-haymaking', 'Give the main reason for the return to haymaking.', [point('Suitable weather / suitable drying conditions', 4)], hay, node='2-6')
    add('q3o1bii', 'Q3 Option One (b)(ii)', '3-3-3', 'haymaking-steps-and-reasons', 'Describe the main steps in conserving grass as hay and give a scientific reason behind each step.',
        [menu('cut correct stage, not too heavy : easier to dry|cut when weather forecast is dry : need 3 -7 days dry and sunny with breeze (dehydration)|ted frequently : to dry evenly|dry : prevents spoilage or preserve|bale : makes handling and storage easier|leave in field after baling : prevents heating (respiration) in storage|store under cover : to keep it dry',
              [6, 6], 'Any two: 2 × (2 step + 4 reason) m (Step : reason).')], hay, node='2-6')
    add('q3o1c', 'Q3 Option One (c)', '3-3-3', 'high-quality-silage-practices', 'Outline four grassland management practices used to achieve high-quality silage.',
        [menu('High quality ryegrass species or clover|fertilizer|top before closing|close for six weeks minimum|cut at leafy stage or heading out stage (high DMD)|reseed old meadows (leys) frequently|weed control|frequent soil tests|possible liming|drainage if needed on certain soils|paddock-strip-block-zero-grazing systems – one named [accept rotational]',
              [4] * 4, 'Any four, 4 marks each (4×4 m).')], node='2-6')
    liver = 'The liver is often referred to as a storage organ.'
    add('q3o2ai', 'Q3 Option Two (a)(i)', '4-1', 'liver-stores', 'Name two substances that are stored in the liver of a farm animal.',
        [menu('Glycogen|vitamins A / D / B12|iron|copper|potassium', [2, 2], 'Any two, 2+2m.')], liver, node='3-0')
    add('q3o2aii', 'Q3 Option Two (a)(ii)', '4-1', 'other-storage-locations',
        'Name two other locations in the animal body where metabolically useful substances are stored and indicate the substance stored in each case.',
        [menu('skin or adipose tissue : fat|skeleton : calcium|muscle : glycogen|gall bladder : bile', [6, 6], 'Any two: 2×(3+3)m, the location 3 and its substance 3 (Location : substance).')],
        liver, node='3-0')
    fluke = 'Liver fluke (Fasciola hepatica) is an endoparasite that occurs in the liver of some farm animals.'
    add('q3o2bi', 'Q3 Option Two (b)(i)', '4-2', 'fluke-phylum', 'To what phylum does F. hepatica belong?', [point('Platyhelminthes', 2)], fluke, node='3-1')
    add('q3o2bii', 'Q3 Option Two (b)(ii)', '4-2', 'flatworm-characteristics', 'Give two characteristics of members of this phylum.',
        [menu('Flat|triploblastic|acoelomate|bilateral symmetry|hermaphrodite|single gut opening', [3, 3], 'Any two, 3 marks each (2x3m).')], fluke, node='3-1')
    add('q3o2biii', 'Q3 Option Two (b)(iii)', '4-2', 'adult-fluke-diagram', 'Draw a diagram of an adult fluke, labelling any three structures.',
        [point('Diagram', None, 'Diagram: 5, 3, 0m. The scheme prints no model drawing.', kind='criterion'),
         point('Labels', None, 'Labels: any three, 1 mark each (3×1). The scheme does not list the structures.', kind='criterion')],
        fluke, marks=8, tariff={'kind': 'questionTotal', 'notation': '5, 3, 0m + 3×1'}, node='3-1|3-5')
    add('q3o2c', 'Q3 Option Two (c)', '4-3-3', 'liver-fluke-life-cycle', 'Describe in detail, with the aid of a labelled diagram, the life cycle of the liver fluke.',
        [point('Diagram', None, 'Diagram 4, 2, 0.', kind='criterion'),
         point('Adult attached to bile duct / of primary host (cow or sheep) / fertilised eggs / in faeces / miracidium / into mudsnail / secondary host / sporocysts / redia / cercaria / cysts on grass (metacercaria) / eaten by primary host',
               None, 'Any six points, 2 marks each (6×2m). [N.B. No diagram => max 6x2m]')],
        marks=16, tariff={'kind': 'questionTotal', 'notation': '6×2m + Diagram 4,2,0'}, node='3-5')
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following, describe a laboratory or field method:'
    for key, ref, topic, concept, aim, steps, node in [
            ('q4a', 'Q4(a)', '2-2-1', 'liming-and-oat-growth', 'To assess the effect of liming on the growth of oats.',
             'Prepared growth media (or field areas) at same pH|leave one unlimed (as a control)|apply lime at different rates to the others|record pH|have same growth conditions for all|same seeding rate of oats|same variety|growth of oat plants recorded at intervals or compare final yields|results stated (must be correctly related to pH)', '1-2|0-1'),
            ('q4b', 'Q4(b)', '3-3-1', 'sprouting-and-potato-yield', 'To investigate the effect of sprouting on the yield of early potatoes.',
             'Named early variety|select groups of tubers that have not been sprouted (control)|select groups of tubers that have been sprouted|same day planting|cultivated under same conditions (e.g. fertilizers, blight sprays, earthing up, weed control)|allow to grow for stated period of time (not less than two months)|same day harvest dig|weigh the amount of potatoes in each plot area|results stated', '2-3|0-1'),
            ('q4c', 'Q4(c)', '4-3-2', 'butterfat-test', 'To determine the butterfat content of a sample of fresh milk.',
             'Milk sample in water bath at 20 °C|butyrometer (Gerber test)|add 10 cm3 of sulphuric acid|add milk sample|add 1cm3 of amyl alcohol|stopper|centrifuge|heat to 65 °C in water bath|adjust with stopper to butterfat line at zero|read % fat or result 3-5% fat', '3-4|0-1'),
            ('q4d', 'Q4(d)', '3-1', 'germinating-seeds-release-energy', 'To show that germinating seeds release energy.',
             'Two thermos flasks|named seeds|thermometers|flasks and seeds disinfected|boil half as a control|invert flasks|record initial temperatures|record the temperatures daily|result stated', '2-0|0-1')]:
        add(key, ref, topic, concept, 'Describe a laboratory or field method ' + aim[0].lower() + aim[1:],
            [menu(steps, [4] * 6, 'Any six, 4 marks each (6×4m).')], lab, node=node)
    # Question 5 -------------------------------------------------------------
    add('q5a', 'Q5(a)', '3-1', 'tap-root-food-reserve', 'Describe in detail how a named plant builds up a reserve of food in a tap root system.',
        [point('Named plant (with tap root)', 2),
         menu('Photosynthesis|sugars|the green part of plant|translocation|phloem|stored as sugar or starch in the root', [4] * 4,
              'Any four, 4 marks each (4x4m). [maximum of 2 points for correct chemical equation for photosynthesis]')], node='2-0')
    terms = 'Explain each of the following terms as used in the context of plant growth in the soil:'
    for key, ref, concept, term, answer in [
            ('q5bi', 'Q5(b)(i)', 'field-capacity', 'field capacity', 'Field capacity: amount of water held in the soil after gravitational (excess) water has drained away'),
            ('q5bii', 'Q5(b)(ii)', 'permanent-wilting-point', 'permanent wilting point', 'Permanent wilting point: when all the capillary water is used or plant is unable to extract any more water from the soil (and dies)'),
            ('q5biii', 'Q5(b)(iii)', 'available-water', 'available water', 'Available water: The portion of water held in soil that may be absorbed by plants / field capacity minus permanent wilting point ((i) minus (ii))')]:
        add(key, ref, '2-2-2', concept, f'Explain the term as used in the context of plant growth in the soil: {term}.', [point(answer, 4)], terms, node='1-3')
    add('q5c', 'Q5(c)', '3-1', 'drought-effects', 'Explain any three effects of drought on the development of crop plants.',
        [menu('Poor development|low yield|available water problem|drought stress|osmosis problem|mineral uptake problem|poor leaf development|reduced transpiration|less photosynthesis|root yield decrease|leaf yield decrease with consequent effect on taproot|lack of turgidity (plant wilts)',
              [4] * 3, 'Any three, 4 marks each (3×4m).')], node='2-0|2-4')
    water = 'The following table shows the water content of three soil samples.'
    add('q5di', 'Q5(d)(i)', '2-2-2', 'least-likely-to-wilt', 'In which soil, A, B or C, would plants be less likely to wilt in a drought?', [point('(i) B', 2)], water, figure=TABLE, node='1-3')
    add('q5dii', 'Q5(d)(ii)', '2-2-2', 'least-likely-to-wilt-reason', 'Explain your answer.', [point('(ii) most available water', 4)],
        water + ' (i) In which soil, A, B or C, would plants be less likely to wilt in a drought?', figure=TABLE, node='1-3')
    # Question 6 -------------------------------------------------------------
    add('q6a', 'Q6(a)', '4-3-2', 'replacement-heifer-features', 'Describe four visible features a dairy farmer would look for when selecting a replacement heifer for a dairy herd.',
        [menu('Good feet|healthy udder|four teats|good conformation|healthy (disease free)|good condition (BCS 3.25)|suitable breed|shiny coat|alert', [3] * 4, 'Any four, 3 marks each (4×3m).')], node='3-4')
    heifer = 'Describe the target weights, nutrition and housing of a replacement heifer in a spring-calving dairy herd at each of the following stages:'
    for key, ref, concept, stage, weight, nutrition, housing in [
            ('q6bi', 'Q6(b)(i)', 'heifer-newborn-stage', 'Newborn calf stage', '35-45 kg', 'Colostrum / whole milk / milk replacer / concentrates / hay', 'In pens / on straw'),
            ('q6bii', 'Q6(b)(ii)', 'heifer-weanling-stage', 'Weanling stage', '55-280 kg', 'Hay / silage / grass / concentrates', 'Out on grass (to 1st November) On straw or slats (November - March)'),
            ('q6biii', 'Q6(b)(iii)', 'heifer-yearling-stage', 'Yearling stage', '280-300 kg', 'Silage ad lib / meals / early grazing', 'Housed on slats or straw or cubicles / out on grass'),
            ('q6biv', 'Q6(b)(iv)', 'heifer-mating-stage', 'Mating stage', '290-340 kg', 'Grass', 'Out on grass')]:
        add(key, ref, '4-3-2', concept, f'Describe the target weight, nutrition and housing of a replacement heifer in a spring-calving dairy herd at the {stage[0].lower() + stage[1:]}.',
            [split(f'Target weight — {weight}', '4×(2+2+1): each stage 2 + 2 + 1 across its target weight, nutrition and housing.'),
             split(f'Nutrition — {nutrition}'), split(f'Housing — {housing}')],
            heifer, marks=5, tariff={'kind': 'orderedSplit', 'notation': '2+2+1'}, node='3-4')
    add('q6ci', 'Q6(c)(i)', '4-1', 'digestive-secretions', 'Name any two substances secreted into an animal’s digestive system and in each case name the organ that secretes it.',
        [menu('bile : liver or gall bladder|amylase or saliva : salivary gland|pancreatic juice or named enzyme : pancreas|succus entericus or named enzyme : small intestine|gastric juice or named component : stomach',
              [4, 4], 'Any two: 2×(2+2)m, the secretion 2 and its organ 2 (Secretion : organ).')], node='3-0')
    add('q6cii', 'Q6(c)(ii)', '4-1', 'fowl-digestive-system', 'Draw a diagram of the digestive system of a fowl and label four parts not found in mammals.',
        [point('Diagram', None, 'Diagram: 4,2,0. The scheme prints no model drawing.', kind='criterion'),
         point('Avian system labels: beak / crop / proventiculus / gizzard / cloaca', None, 'Any four labels, 1 mark each (4×1m).')],
        marks=8, tariff={'kind': 'questionTotal', 'notation': '4,2,0 + 4×1m'}, node='3-0')
    # Question 7 -------------------------------------------------------------
    dna = 'The DNA molecule carries genetic information.'
    add('q7ai', 'Q7(a)(i)', '4-1', 'dna-structures', 'In which structures is DNA found in animal cell nuclei?', [point('(i) Chromosomes', 2)], dna, node='3-6')
    add('q7aii', 'Q7(a)(ii)', '4-1', 'sex-determination', 'Explain how particular types of these structures determine the sex of individual animals.',
        [point('Parents — XX Female', 2, 'Parents 2+2, gametes 2+2, F1 2m.'), point('Parents — XY Male', 2), point('Gametes — X', 2), point('Gametes — X, Y', 2), point('F1 — XX XY', 2)],
        dna + ' (i) In which structures is DNA found in animal cell nuclei?', node='3-6')
    add('q7b', 'Q7(b)', '4-1', 'cloned-gm-mutations',
        'Scientists in Scotland, where Dolly the sheep was cloned, recently announced a development in a project to produce animals resistant to infection. They have created a genetically modified pig using a new technique. '
        'The bonham (piglet), born in August 2012 and named Pig 26, was genetically engineered using DNA mutations. Explain the underlined terms: cloned, genetically modified, mutations.',
        [point('Cloned: exact copy of the cell or organism / genetically identical organisms', 4, '3×4m.'),
         point('Genetically modified: altering the genetic make-up of an organism / placing a gene from one species into another', 4),
         point('Mutations: changes in the DNA sequence or structure of a gene / gain or loss of part of or a whole chromosome', 4)], node='3-6')
    maize = ('In maize, the traits pigmy size (n) and crinkly leaf (r) are recessive to the traits normal size (N) and regular leaf (R). '
             'A maize plant, heterozygous for size and leaf shape, is self pollinated and 160 seeds are subsequently collected and germinated.')
    add('q7ci', 'Q7(c)(i)', '4-1', 'maize-parent-genotype', 'Write the genotype of the parent using the above notation.', [point('Parents genotype: NnRr (× NnRr)', 4)], maize, node='3-6')
    add('q7cii', 'Q7(c)(ii)', '4-1', 'maize-offspring-counts',
        'How many new plants would you expect to show: 1. crinkly leaves 2. regular leaves 3. normal size and regular leaves 4. pigmy size and regular leaves?',
        [point('1. Crinkly leaves 40', 4, '4×4m. [Accept correct fraction, decimal or percentage for half marks in each case]'), point('2. Regular leaves 120', 4),
         point('3. Normal size and regular leaves 90', 4), point('4. Pigmy size and regular leaves 30', 4)], maize, node='3-6')
    add('q7d', 'Q7(d)', '4-3-3', 'castration-reasons', 'Give two reasons why male animals are castrated on farms.',
        [menu('Health & safety|to stop inbreeding on farms (keep best animals for mating only)|strong taste on meat (boar-taint )|small market for bull beef|unwanted mating|less fencing', [2, 2],
              'Any two, 2 marks each (2×2m).')], node='3-5')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of the parts (a), (b), (c).'
    add('q8a', 'Q8(a)', '4-3-2', 'bonham-management', 'Describe the management of bonhams (piglets) from birth to weaning.',
        [menu('Sow in farrowing house at 20°C|in farrowing crate|suckling sow|colostrum|treat the navel with iodine(solution)|creep feeding|creep ration 21% protein (or lysine)|water available|iron injection|temperature 30°C creep area|infra-red lamp|castration or ear notching|cutting teeth|tail clipping|weaning at four to six weeks (at 9 kg)',
              [6, 6, 6, 2, 2, 2], 'Any six: 3×6m+3×2m, the first three correct earn 6 each and the next three 2 each.')], twoof, node='3-4')
    barley = {'soil': 'pH 6-6.5 / deep, fertile, medium to light or sandy loam / brown earth or grey brown podzolic', 'prep': 'Plough / depth 12-20cm / harrow / rotavate / produce fine seed bed',
              'sow': 'Winter barley: Sept. – Oct. or Spring barley: Feb. - Apr. / Rate 140-220 kg per ha or correct seeding rate per m2 / tramlines / combine drill / post-sowing rolling',
              'fert': '10:10:20 or 18:6:12 (NPK)', 'harvest': 'Combine harvester / July - September'}
    cereals = [('barley', 'Barley', barley['soil'], barley['sow'], barley['harvest'], '3-4 tonne per ha', ''),
               ('wheat', 'Wheat', 'pH 5-7', barley['sow'], 'Jly-Sp', '3-4 t per ha', ' (as for barley)'),
               ('oats', 'Oats', 'pH 5.5', barley['sow'], 'Jly-Sp', '4-4.5 t per ha', ' (as for barley)'),
               ('maize', 'Maize', 'pH 6.6-7.0', '20-30 kg / Mar. - May / precision seeder', 'Sept-Oct', 'No straw', '')]
    built = []
    for slug, name, soil, sow, harvest, straw, same in cereals:
        first = slug == 'barley'
        built.append((slug, name, [
            split(f'Name of crop — {name}', 'Name 3m, then 5×(3+1)m across (i)-(v) and Yield 1m for (vi). The wheat, oats and maize columns print "as for barley" where they share its answer.'),
            split(f'(i) Soil suitability — {soil}' if first else f'(i) Soil suitability (otherwise as for barley) — {soil}'),
            split(f'(ii) Preparation of the seed bed{"" if first else " (as for barley)"} — {barley["prep"]}'),
            split(f'(iii) Sowing the seed{same} — {sow}'),
            split(f'(iv) Use of fertiliser{"" if first else " (as for barley)"} — {barley["fert"]}'),
            split(f'(v) Harvesting — {harvest}'),
            split(f'(vi) Straw yield — {straw}')]))
    rows, variants = routes(built)
    add('q8b', 'Q8(b)', '3-3-1', 'named-cereal-production',
        'Describe in detail the production of a named cereal crop under each of the following headings: (i) Soil suitability (ii) Preparation of the seed bed (iii) Sowing the seed (iv) Use of fertiliser (v) Harvesting (vi) Straw yield.',
        rows, twoof, marks=24, tariff={'kind': 'questionTotal', 'notation': 'Name 3m + 5×(3+1)m + Yield 1m'},
        selection=closed(1, [name for _, name, *_ in cereals]), node='2-3|2-4|2-5', extra={'answerVariants': variants})
    members = [('i', 'Glaciation', 'alteration of any part of the earth’s surface|by passage of a glacier|chiefly by glacial erosion or deposition|slow movement downwards by gravity|glacial drift|glacial till'),
               ('i', 'Gleisation', 'soil forming process|high water table or impermeable nature of soil|poor drainage and aeration|waterlogging|anaerobic conditions|low bacterial activity|low level of decomposition|reduction of iron|giving grey-blue colour in subsoil or with red mottling after reoxidation process|high rainfall|peat accumulation on top'),
               ('ii', 'Epidermis', 'outermost layer of cells|tissue in an organism|protection|protects against water loss|skin'),
               ('ii', 'Epididymis', 'location testes or scrotum|long convoluted tube|part of spermatic cord|sperm stored or sperm mature|leads into the vas deferens'),
               ('iii', 'Antibodies', 'proteins|produced by body|response to antigen or infection|colostrums|immunoglobins|resistance to diseases|made by white blood cells'),
               ('iii', 'Antibiotics', 'produced by micro-organisms|kill other organisms|stop growth of other organisms|e.g. penicillin, streptomycin etc.|control bacterial or fungal diseases|no effect on viruses'),
               ('iv', 'Earthing up', 'piling up soil around the base of a plant crop (e.g. potatoes)|prevents greening|prevents formation of solanine or alkaloids|prevents blight infection|improves yield|controls weeds|pest control|frost protection|supports the stems'),
               ('iv', 'Steaming up', '(process farmers use towards) end of gestation period|gradual increase in feeding of meals during last six-eight weeks|prevents twin lamb disease in sheep enterprise|increases milk yield|improves body condition score or build up energy reserve')]
    add('q8c', 'Q8(c)', '2-1', 'distinguishing-paired-terms',
        'Highlight the main differences between the members of any three of the following pairs of terms: (i) Glaciation and Gleisation. (ii) Epidermis and Epididymis. (iii) Antibodies and Antibiotics. (iv) Earthing up and Steaming up.',
        [menu(pool, [3, 1], f'({k}) {label}: two points, 3 + 1.' + (' 3×2x(3+1)m: each term 3 + 1, for any three pairs.' if i == 0 else ''))
         for i, (k, label, pool) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='1-0|3-0|3-5|2-4')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following:'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '4-1', 'weaned-animal-bulky-food', 'The ability of a young farm animal to digest bulky foods after weaning.',
             'Ruminant|rumen developed|lack of bacterial activity in rumen before|cellulose or hay or straw present (scratch factor)|concentrates (and water)|takes up to 3 weeks|increasing numbers of microbes stimulate growth and development of rumen', '3-0'),
            ('q9b', 'Q9(b)', '2-3', 'subsoiling-podzol', 'Sub-soiling of a podzolic soil.',
             'Break iron pan or hard pan|recover some nutrients|improve drainage|improve aeration|to prevent peat formation|to loosen soil or help root penetration', '1-5'),
            ('q9c', 'Q9(c)', '2-3', 'shelter-belts', 'The use of shelter belts on farms.',
             'Reduce wind speed|higher temperatures for crop growth or earlier growth or higher yield|better FCR for farm animals|protection for animals from extreme conditions or prevents hypothermia|biodiversity or habitat|reduces heat loss from buildings or protect them from damage|aesthetic', '1-6'),
            ('q9d', 'Q9(d)', '4-3-2', 'flushing-ewes', 'The flushing of lowland ewes prior to mating.',
             'Improves condition prior to mating|more eggs at ovulation|more twins|fewer barren ewes|fewer repeat ewes|increased conception rates|better implantation to the uterine lining|more regular oestrus cycles', '3-4'),
            ('q9e', 'Q9(e)', '4-3-3', 'redwater-in-bought-in-animal', 'The presence of a red colour in the urine of a bought-in animal after six weeks grazing on the farm.',
             'Red water fever|Babesia|spread by tick|red blood cells burst|haemoglobin released in urine (or blood in urine)|incubation period in animal is 10 – 20 days therefore infected on farm|effect of eating kale (for one point only)', '3-5')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item,
            [menu(points, [10, 1, 1], 'Any three points. ' + FIRST.format('10+1+1m'))], why, node=node)
    assert len(p.tasks) == 61, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('61 base tasks, one card each. One-pool parts keep their steps (6 + 3 + 1, 4 + 4 + 1 + 1, 10 + 1 + 1, 3×6m + 3×2m); parts priced separately '
                          '(Q1(i), Q1(j), Q5(d)) and the four Q6(b) heifer stages (2 + 2 + 1 each) are separate tasks. Q1(a) adulteration tests and Q8(b) cereals are answer routes; '
                          'Q8(c) is one card for the choice of three pairs from four.')
