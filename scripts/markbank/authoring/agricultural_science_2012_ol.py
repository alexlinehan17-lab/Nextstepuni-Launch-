"""2012 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 12 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 49 base tasks, one card each. Section One questions are one task each: where
the scheme prints one scale across several parts (Q7) the question states the scale (orderedSplit);
otherwise the rows carry the scheme's own marks, and the one-pool scales of Q3, Q5 and Q6 stay on
their menus. Section Two parts are priced on their own. The Q10(c) calf-rearing and heifer-rearing
answers and the Q12(b)(iii) soil-texture methods are answer routes. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': 'ca9b4547982ff4a881b82f3930596bccf39345b57e8367461935a729435c12fb',
          'markingschemes': '1a0dcbbdd3eed489d6adc380071d68897599fc0d272f4e7dccd5ef83b61316dd'}
SELECTIONS = {
    '631dfd57218273ea': ('exam-selection', 'Cover: Section One, six of seven independent 20-mark questions; every question is retained.'),
    '31d9e15392aa6c09': ('exam-selection', 'Cover: Section Two, three of six independent 60-mark questions; every question is retained.'),
    '4681dfa515e653ef': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    '2dbce80433b5780d': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '3aa09a461242bf39': ('open', 'Q10(d): any two hygiene practices from the scheme pool; a marking menu.'),
    '5eb477bf3da288da': ('independent-task-selection', 'Q12: two of four independently priced 30-mark parts; all four are retained.'),
}
SUPPLEMENTARY = [
    (7, 'List four steps to help ensure successful calf rearing', 'closed', 'Q10(c): calf rearing OR replacement heifer rearing, kept as answer routes on one card.'),
    (8, 'Describe an experiment to estimate the percentage clay', 'closed', 'Q12(b)(iii): the scheme gives the sieve, sedimentation and feel methods, kept as answer routes on one card.'),
]
ATLAS = {
    'Q1': 'soil-science|grassland|scientific-practices-experiments-investigations', 'Q2': 'classification-of-organisms|crop-production|soil-science',
    'Q3': 'animal-production|crop-production|soil-science|classification-of-organisms|animal-diseases|scientific-practices-experiments-investigations',
    'Q4': 'crop-production|animal-production', 'Q5': 'animal-physiology', 'Q6': 'plant-physiology', 'Q7': 'animal-production',
    'Q8': 'animal-production', 'Q8(a)(ii)': 'animal-production|animal-diseases',
    'Q9': 'crop-production', 'Q9(c)': 'crop-production|scientific-practices-experiments-investigations',
    'Q10': 'animal-production', 'Q11': 'grassland',
    'Q12(a)': 'animal-production', 'Q12(b)': 'soil-science', 'Q12(b)(iii)': 'soil-science|scientific-practices-experiments-investigations',
    'Q12(c)': 'animal-physiology', 'Q12(d)(i)': 'animal-production', 'Q12(d)(ii)': 'animal-production', 'Q12(d)(iii)': 'crop-production',
    'Q12(d)(iv)': 'crop-production|animal-diseases', 'Q12(d)(v)': 'animal-diseases',
    'Q13': 'genetics',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1': (P((2, 0.307, 0.915)), P((5, 0.128, 0.376))),
    'Q2': (P((3, 0.056, 0.493)), P((5, 0.376, 0.708))),
    'Q3': (P((3, 0.493, 0.909)), P((5, 0.708, 0.915))),  # trimmed above the page footer
    'Q4': (P((4, 0.041, 0.581)), P((6, 0.080, 0.409))),
    'Q5': (P((4, 0.581, 0.900)), P((6, 0.409, 0.597))),
    'Q6': (P((5, 0.041, 0.445)), P((6, 0.597, 0.783))),
    'Q7': (P((5, 0.445, 0.832)), P((6, 0.783, 0.891))),  # trimmed above the page footer
    'Q8(a)(i)': (P((6, 0.235, 0.284)), P((7, 0.113, 0.212))),
    'Q8(a)(ii)': (P((6, 0.235, 0.264), (6, 0.284, 0.310)), P((7, 0.113, 0.162), (7, 0.212, 0.278))),
    'Q8(b)(i)': (P((6, 0.235, 0.264), (6, 0.310, 0.329)), P((7, 0.113, 0.162), (7, 0.278, 0.344))),
    'Q8(b)(ii)': (P((6, 0.235, 0.264), (6, 0.329, 0.355)), P((7, 0.113, 0.162), (7, 0.344, 0.460))),
    'Q8(c)(i)': (P((6, 0.235, 0.264), (6, 0.355, 0.374)), P((7, 0.113, 0.162), (7, 0.460, 0.510))),
    'Q8(c)(ii)': (P((6, 0.235, 0.264), (6, 0.374, 0.460)), P((7, 0.113, 0.162), (7, 0.510, 0.537))),
    'Q9(a)(i)': (P((6, 0.460, 0.509)), P((8, 0.080, 0.145))),
    'Q9(a)(ii)': (P((6, 0.460, 0.490), (6, 0.509, 0.610)), P((8, 0.080, 0.113), (8, 0.145, 0.493))),
    'Q9(b)(i)': (P((6, 0.460, 0.490), (6, 0.610, 0.644)), P((8, 0.080, 0.113), (8, 0.493, 0.559))),
    'Q9(b)(ii)': (P((6, 0.460, 0.490), (6, 0.644, 0.700)), P((8, 0.080, 0.113), (8, 0.559, 0.625))),
    'Q9(c)': (P((6, 0.460, 0.490), (6, 0.700, 0.752)), P((8, 0.080, 0.113), (8, 0.625, 0.685))),
    'Q10(a)(i)': (P((7, 0.041, 0.090)), P((9, 0.079, 0.151))),
    'Q10(a)(ii)': (P((7, 0.041, 0.071), (7, 0.090, 0.131)), P((9, 0.079, 0.128), (9, 0.151, 0.210))),
    'Q10(b)': (P((7, 0.041, 0.071), (7, 0.131, 0.333)), P((9, 0.079, 0.128), (9, 0.210, 0.343))),
    'Q10(c)': (P((7, 0.041, 0.071), (7, 0.333, 0.378)), P((9, 0.079, 0.128), (9, 0.343, 0.558))),
    'Q10(d)': (P((7, 0.041, 0.071), (7, 0.378, 0.484)), P((9, 0.079, 0.128), (9, 0.558, 0.617))),
    'Q11(a)': (P((7, 0.484, 0.544)), P((10, 0.080, 0.194))),
    'Q11(b)(i)': (P((7, 0.484, 0.514), (7, 0.544, 0.593)), P((10, 0.080, 0.129), (10, 0.194, 0.227))),
    'Q11(b)(ii)': (P((7, 0.484, 0.514), (7, 0.544, 0.574), (7, 0.593, 0.619)), P((10, 0.080, 0.129), (10, 0.227, 0.292))),
    'Q11(c)': (P((7, 0.484, 0.514), (7, 0.619, 0.664)), P((10, 0.080, 0.129), (10, 0.292, 0.490))),
    'Q11(d)': (P((7, 0.484, 0.514), (7, 0.664, 0.750)), P((10, 0.080, 0.129), (10, 0.490, 0.584))),  # trimmed above the page footer
    'Q12(a)(i)': (P((8, 0.041, 0.135)), P((11, 0.080, 0.178))),
    'Q12(a)(ii)': (P((8, 0.041, 0.116), (8, 0.135, 0.195)), P((11, 0.080, 0.113), (11, 0.180, 0.222))),  # stops above (iii), which the scheme numbers (ii) again
    'Q12(a)(iii)': (P((8, 0.041, 0.116), (8, 0.192, 0.226)), P((11, 0.080, 0.113), (11, 0.228, 0.302))),  # hand-set: the scheme numbers this part (ii)
    'Q12(b)(i)': (P((8, 0.041, 0.116), (8, 0.251, 0.270)), P((11, 0.080, 0.113), (11, 0.325, 0.391))),
    'Q12(b)(ii)': (P((8, 0.041, 0.116), (8, 0.270, 0.330)), P((11, 0.080, 0.113), (11, 0.391, 0.572))),
    'Q12(b)(iii)': (P((8, 0.041, 0.116), (8, 0.330, 0.371)), P((11, 0.080, 0.113), (11, 0.572, 0.811))),
    'Q12(c)(i)': (P((8, 0.041, 0.116), (8, 0.371, 0.691)), P((11, 0.080, 0.113), (12, 0.080, 0.129))),
    'Q12(c)(ii)': (P((8, 0.041, 0.116), (8, 0.371, 0.672), (8, 0.691, 0.706)), P((11, 0.080, 0.113), (12, 0.129, 0.195))),
    'Q12(c)(iii)': (P((8, 0.041, 0.116), (8, 0.371, 0.672), (8, 0.706, 0.721)), P((11, 0.080, 0.113), (12, 0.195, 0.244))),
    'Q12(c)(iv)': (P((8, 0.041, 0.116), (8, 0.371, 0.672), (8, 0.721, 0.762)), P((11, 0.080, 0.113), (12, 0.244, 0.309))),
    'Q12(d)(i)': (P((8, 0.041, 0.116), (8, 0.762, 0.811)), P((11, 0.080, 0.113), (12, 0.309, 0.343))),
    'Q12(d)(ii)': (P((8, 0.041, 0.116), (8, 0.762, 0.792), (8, 0.811, 0.826)), P((11, 0.080, 0.113), (12, 0.343, 0.408))),
    'Q12(d)(iii)': (P((8, 0.041, 0.116), (8, 0.762, 0.792), (8, 0.826, 0.841)), P((11, 0.080, 0.113), (12, 0.408, 0.441))),
    'Q12(d)(iv)': (P((8, 0.041, 0.116), (8, 0.762, 0.792), (8, 0.841, 0.856)), P((11, 0.080, 0.113), (12, 0.441, 0.490))),
    'Q12(d)(v)': (P((8, 0.041, 0.116), (8, 0.762, 0.792), (8, 0.856, 0.874)), P((11, 0.080, 0.113), (12, 0.490, 0.549))),
    'Q13(a)': (P((9, 0.041, 0.176)), P((13, 0.079, 0.259))),
    'Q13(b)(i)': (P((9, 0.041, 0.071), (9, 0.176, 0.338)), P((13, 0.079, 0.112), (13, 0.259, 0.288))),  # hand-set: the scheme prints the cross lines without (i)-(iii)
    'Q13(b)(ii)': (P((9, 0.041, 0.071), (9, 0.176, 0.305), (9, 0.350, 0.368)), P((13, 0.079, 0.112), (13, 0.290, 0.320))),  # hand-set: the scheme prints the cross lines without (i)-(iii)
    'Q13(b)(iii)': (P((9, 0.041, 0.071), (9, 0.176, 0.305), (9, 0.380, 0.400)), P((13, 0.079, 0.112), (13, 0.323, 0.352))),  # hand-set: the scheme prints the cross lines without (i)-(iii)
    'Q13(c)': (P((9, 0.041, 0.071), (9, 0.424, 0.643)), P((13, 0.079, 0.112), (13, 0.374, 0.521))),
    'Q13(d)': (P((9, 0.041, 0.071), (9, 0.643, 0.698)), P((13, 0.079, 0.112), (13, 0.521, 0.584))),
}
SHARED = 'Shared scale {}: the first correct answers earn the higher award, whichever part they answer, so no part carries a mark of its own.'
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'
FIGURES = {
    'q1': ('agsci-2012-ol-paper-clover-nodules', None),
    'q2': ('agsci-2012-ol-paper-soil-animals', None),
    'q12cii': ('agsci-2012-ol-paper-ruminant-stomach', [('A', 'Rumen or paunch (stomach)', True), ('B', 'Reticulum or honeycomb (stomach)', True), ('C', 'Abomasum or true stomach', True), ('D', 'Omasum (labelled on the paper)', False)]),
    'q12ci': ('agsci-2012-ol-paper-ruminant-stomach', None), 'q12ciii': ('agsci-2012-ol-paper-ruminant-stomach', None), 'q12civ': ('agsci-2012-ol-paper-ruminant-stomach', None),
}


def split(text, note=None, route=None):
    """An unpriced row: the scheme prices the scale, not the row."""
    row = point(text, None, note)
    if route:
        row['route'] = route
    return row


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2012, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 12, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One ------------------------------------------------------------
    figured(add('q1', 'Q1', '2-2-3', 'clover-nodule-bacteria',
                'The diagram shows nodules on the roots of a clover plant. (a) What type of organism do these nodules contain? (b) State one function of the organisms referred to in (i). '
                '(c) In the spaces below, draw and name the piece of equipment normally used in a laboratory to transfer the organisms referred to in (i) onto an agar plate. '
                '(d) Give one reason for using clover in grass seed mixtures.',
                [point('(a) Bacteria/ rhizobium', 4, 'Any one, 4m (5 x 4m across the question).'),
                 point('(b) Decomposition of organic matter (O.M.)/ recycling of nutrients or named nutrient/ silage making/ food manufacturing or named example/ nitrogen fixation', 4, 'Any one, 4m.'),
                 point('(c) Drawing of inoculating loop', 4, '4m. [accept drawing of forceps or “tweezers” if named]', kind='criterion'),
                 point('(c) Name — Inoculating loop', 4, '4m. [accept forceps or “tweezers”]'),
                 point('(d) Nitrogen fixation/ rich in protein/ rich in minerals/ improves productivity of grassland/ weed control/ less N fertiliser required/ saves money/palatable/ digestible/ improved silage if red clover stated', 4, 'Any one, 4m.')],
                tariff={'kind': 'fixed', 'notation': '5 x 4m'}, node='1-4|2-6|0-1'), 'q1')
    figured(add('q2', 'Q2', '3-2', 'soil-animals-table',
                'Complete the table below in relation to the animals shown in the photographs: (a) Name of animal. (b) Phylum to which animal belongs. (c) One characteristic of a member of the phylum. (d) Importance in agriculture.',
                [menu(['Leatherjacket/ cranefly/ daddy-long-legs', 'Earthworm/ Lumbricus.'], [1, 1], '(a) Name of animal: 1m each, Animal 1 (the larva) then Animal 2 (the worm).'),
                 menu(['Arthropoda.', 'Annelida.'], [4, 4], '(b) Phylum to which animal belongs: 4m each, Animal 1 then Animal 2.'),
                 menu(['Jointed limbs/ body divided into two or three parts/ exoskeleton/ metamorphosis', 'Segmented body / cylindrical body or round (in cross –section) / coelomate/ hermaphrodite/ clitellum/ setae'],
                      [4, 4], '(c) One characteristic of a member of this phylum: 4m each, Animal 1 then Animal 2.'),
                 menu(['Crop pest/ eats or kills roots or stems or plants/ decreases yield/ leads to bare patches',
                       'Improves drainage/ improves aeration/ improves soil structure/ mixes soil layers/ creates humus/ increases soil fertility or adds nutrients/ breaks down O.M.'],
                      [1, 1], '(d) Importance in agriculture: 1m each, Animal 1 then Animal 2.')],
                tariff={'kind': 'fixed', 'notation': '2(1m) + 2(4m) + 2(4m) + 2(1m)'}, node='3-1|2-4|1-4'), 'q2')
    statements = [('a', 'Aberdeen Angus cattle are black and white.', 'F'), ('b', 'Sitka spruce is grown in most commercial forests in Ireland.', 'T'), ('c', 'Granite is an igneous rock.', 'T'),
                  ('d', 'Dandelion belongs to the family Gramineae.', 'F'), ('e', 'Soil pH is a measure of the phosphate level in a soil.', 'F'), ('f', 'Liver fluke belongs to the phylum Nematoda.', 'F'),
                  ('g', 'The gestation period in pigs is three months, three weeks and three days.', 'T'), ('h', 'Benedict`s solution is used to test for starch.', 'F'),
                  ('i', 'A line transect is used in ecological studies.', 'T'), ('j', 'Anaemia is a common disease in pigs.', 'T')]
    add('q3', 'Q3', '4-1', 'true-or-false-farm-science',
        'Indicate whether the following statements are true (T) or false (F) by placing a circle around the correct answer in each case, as shown in the example. '
        'Example: The lungs are involved in gas exchange — T. ' + ' '.join(f'({k}) {s}' for k, s, _ in statements),
        [menu([f'({k}) {a}' for k, _, a in statements], [6, 6] + [1] * 8,
              'All ten statements, (8 x 1m) + (2 x 6m). ' + FIRST.format('6, 6, then 1 each') + ' T = true, F = false; the scheme gives each letter with T or F.')],
        tariff={'kind': 'fixed', 'notation': '(8 x 1m) + (2 x 6m)'}, node='3-1|2-3|1-0|2-1|1-2|3-5|0-1')
    add('q4', 'Q4', '2-3', 'reasons-for-farm-tasks',
        'Give one scientific reason why each of the following tasks is carried out on farms. (a) Rolling the seedbed after sowing seed. (b) Male cattle are usually castrated. (c) Housing cattle during the winter. '
        '(d) Sheep are sheared in summer. (e) Trees in a forestry plantation are thinned.',
        [point('(a) Rolling the seedbed — Compacts soil/ covers seed/ improve germination/ prevent birds eating seed/ buries stones /brings up moisture/ improves seed-soil contact/ levels soil', 4, 'Any one for each task, 4m each (5 x 4m).'),
         point('(b) Castrating male cattle — Prevents unwanted breeding/ safer/ less aggressive/ less testosterone/ more easily managed', 4),
         point('(c) Housing cattle in winter — Easier management/ easier feeding/ prevents poaching/ more grass in following spring/ higher stocking rates/ environmental compliance/ reduce death or injury/better FCE/ warmer/ FYM or slurry available', 4),
         point('(d) Shearing sheep in summer — Prevents maggots or blowfly/ increases mobility of sheep/ facilitates mating/ keeps sheep cooler/ sale of wool/ allows more space for housed sheep.', 4),
         point('(e) Thinning forestry trees — Reduces competition/ increases space/ poorer trees removed/ improves the trees that are left or named improvement/ thinned trees used to make (useful) products/ provides access/ source of income.', 4)],
        tariff={'kind': 'fixed', 'notation': '5 x 4m'}, node='2-3|3-4|2-4')
    add('q5', 'Q5', '4-1', 'mammal-body-part-locations',
        'State the precise location of each of the following parts in the body of a mammal. The first one has been completed as an example: Atrium — Heart. (a) Trachea (b) Humerus (c) Ureter (d) Duodenum (e) Cerebellum.',
        [menu(['(a) Trachea: Above lungs/ in the neck/ in the throat.', '(b) Humerus: (Upper) arm/ above elbow/ (upper part of) forelimb', '(c) Ureter: Between kidney and bladder/ beside kidney',
               '(d) Duodenum: Exit from stomach/ beside stomach/ (first part of) small intestine', '(e) Cerebellum: Brain/ head/ skull'], [6, 4, 4, 3, 3],
              'All five, 2(3m) + 2(4m) + 6m. ' + FIRST.format('6, 4, 4, 3, 3'))],
        tariff={'kind': 'fixed', 'notation': '2(3m) + 2(4m) + 6m'}, node='3-0')
    add('q6', 'Q6', '3-1', 'plant-structures-and-descriptions',
        'Match each plant structure from the following list with a description in the table. The first one has been completed as an example. List: root hairs; xylem; phloem; carpels; stomata; stamens. '
        'Example: Phloem — Carries products of photosynthesis. (a) Male parts of flowers. (b) Carries water from the roots. (c) Allow gas exchange in leaves. (d) Absorb water from the soil. (e) Female parts of flowers.',
        [menu(['(a) Stamen: Male part of flowers.', '(b) Xylem: Carries water from roots.', '(c) Stomata: Allows gas exchange in leaves.', '(d) Root hairs: Absorb water from the soil.',
               '(e) Carpel: Female part of flowers.'], [6, 4, 4, 3, 3], 'All five, 2(3m) + 2(4m) + 6m. ' + FIRST.format('6, 4, 4, 3, 3'))],
        tariff={'kind': 'fixed', 'notation': '2(3m) + 2(4m) + 6m'}, node='2-0|2-1')
    add('q7', 'Q7', '4-3-2', 'pig-temperatures-and-weights',
        '(a) Give the recommended temperature for each of the following in relation to pig housing: (i) Creep area. (ii) Weaner house. (iii) Fattener house. '
        '(b) Why do bonhams have their teeth clipped soon after birth? (c) Give the approximate weight at which pigs are finished for slaughter.',
        [split('(a)(i) Creep area — 25 - 30° C', SHARED.format('6m + 2 (4m) + 2 (3m)') + ' Five answers: the three temperatures, (b) and (c).'),
         split('(a)(ii) Weaner house — 22 - 26° C'), split('(a)(iii) Fattener house — 20 - 22° C'),
         split('(b) Teeth clipping — Prevents damage to sow’s teats/ prevents biting other bonhams', 'Any one.'), split('(c) Slaughter weight — 80- 95 kg')],
        marks=20, tariff={'kind': 'orderedSplit', 'notation': '6m + 2 (4m) + 2 (3m)'}, node='3-4|3-3')
    # Question 8 -------------------------------------------------------------
    for key, ref, topic, concept, question, options, steps, note, node in [
            ('q8ai', 'Q8(a)(i)', '4-2', 'common-sheep-breeds', 'Name three common sheep breeds.',
             'Suffolk|Texel|Galway|(Wicklow) Cheviot|Blackface mountain|Border Leicester|Beltex', [5, 2, 2], 'Any three, 5m + 2(2m).', '3-1'),
            ('q8aii', 'Q8(a)(ii)', '4-3-3', 'sheep-parasites', 'Name two parasites of sheep.',
             'Blowfly or maggots or flystrike|mange mites|(stomach) worms|(lung) worms|liver fluke', [4, 2], 'Any two, (4m + 2m).', '3-5'),
            ('q8bi', 'Q8(b)(i)', '4-3-2', 'housing-at-lambing', 'State three advantages of housing sheep at lambing time.',
             'Easier supervision or easier management|prevents poaching|shelter|easier feeding|less predation|earlier grazing|lower rate of lamb mortality|more grass in spring|FYM or slurry available', [5, 2, 2],
             'Any three, 5m + 2(2m).', '3-4'),
            ('q8bii', 'Q8(b)(ii)', '4-3-2', 'mating-time-management', 'Describe four sheep management practices prior to and at mating time.',
             'Ewes on bare pasture|moved to good pasture (one month) before mating|flushing|ewes can be sponged|PMSG|sponge removed|rams introduced|1 ram for 40 - 45 ewes or other suitable ratio|raddle harness on ram(s)|change colour every 14 days|ewes kept on good grazing during mating|mating season lasts six weeks|dagging|shearing',
             [7, 3, 3, 3], 'Any four, 7m + 3(3m).', '3-4'),
            ('q8ci', 'Q8(c)(i)', '4-3-2', 'lamb-diet', 'Describe the diet of the lamb from birth to slaughter.',
             'Colostrum|ewe’s milk|hay|silage|grass|(creep) meal or nuts or rations or Concentrates feeding', [7, 7, 2], 'Any three, 2(7m) + 2m.', '3-4')]:
        add(key, ref, topic, concept, question, [menu(options, steps, note)], node=node)
    add('q8cii', 'Q8(c)(ii)', '4-3-1', 'lamb-slaughter-weight', 'What is the normal weight in kilograms at which lambs are slaughtered?', [point('40-50 kg', 4)], node='3-3')
    # Question 9 -------------------------------------------------------------
    add('q9ai', 'Q9(a)(i)', '3-2', 'potato-varieties', 'Name two common varieties of potato.',
        [menu('Kerrs Pink|Rooster|Home Guard|Golden Wonder|British Queen', [4, 4], 'Any two (2 x 4m).')], node='2-1')
    add('q9aii', 'Q9(a)(ii)', '3-3-1', 'potato-cultivation-headings',
        'Describe the cultivation of potatoes under the following headings: 1. Seed bed preparation. 2. Control of a named disease. 3. Weed control. 4. Harvesting.',
        [menu('Plough|rotavate or harrow|ridger|stone removal', [4], '(1) Seed bed preparation: any one (4m).'),
         menu(['Potato blight: Fungicide/ spray/rotation/ certified seed/ avoid ground keepers', 'Blackleg: Certified seed/ good drainage', 'Scab: Avoid liming/ certified seed/ rotation',
               'Leaf roll: Aphicide/ certified seed/ biological control or detail of', 'Leaf mosaic: Aphicide/ certified seed/ biological control or detail of'], [8],
              '(2) Name of disease (4m) and control measure (4m). [Control measure must match named disease]'),
         menu('Spraying|scuffling|earthing up|rotation|hand-weeding|hoeing|spade|hand pick', [4], '(3) Weed control: any one (4m).'),
         menu('Haulms sprayed|elevator digger|complete harvester|harvested in Sept – Nov. for maincrop', [4],
              '(4) Harvesting: any one (4m). [Accept May-June or June-August as harvest time for first earlies or second earlies respectively]')],
        node='2-3|2-4|2-5')
    add('q9bi', 'Q9(b)(i)', '3-3-1', 'early-potato-areas',
        'First early potatoes are usually grown in coastal areas of the east and south of Ireland. Give two reasons why these areas are suitable for early potato production.',
        [menu('Reduced frost risk in south and east|earlier growth in spring|light soils|free draining|sandy soils|south facing|warmer weather or warmer soil|soil heats up more quickly', [6, 2], 'Any two (6m + 2m).')], node='2-3')
    add('q9bii', 'Q9(b)(ii)', '3-3-2', 'potato-rotation', 'Crop rotation is an important feature of potato cultivation. Give two reasons why crop rotation is important.',
        [menu('Prevents pests|prevents diseases|improves soil structure|prevents nutrient depletion|avoids ground keepers|weed control|prevents plough pan', [6, 2], 'Any two (6m + 2m).')], node='2-4')
    add('q9c', 'Q9(c)', '3-3-3', 'potato-dry-matter', 'Describe an experiment to find the dry matter (DM) content of potatoes.',
        [menu('Weigh dish|cut potatoes|weigh dish and potatoes|weight of potatoes|oven|dry to constant weight|reweigh|loss in weight|calculate % water|calculate % DM', [7, 3, 3, 3], 'Any four, 7m + 3 (3m).')],
        node='2-5|0-1')
    # Question 10 ------------------------------------------------------------
    add('q10ai', 'Q10(a)(i)', '4-2', 'dairy-breeds', 'Give the names of two breeds of cattle commonly used in milk production.',
        [menu('Holstein|Friesian|Jersey|Ayrshire|Shorthorn|Simmental', [3, 3], 'Any two (2 x 3m). [ Note: Simmental in either but not in both]')], node='3-1')
    add('q10aii', 'Q10(a)(ii)', '4-2', 'beef-breeds', 'Give the names of two breeds of cattle commonly used in beef production.',
        [menu('Hereford|Aberdeen Angus|Charolais|Simmental|Limousin', [3, 3], 'Any two (2x 3m). [ Note: Simmental in either but not in both]')], node='3-1')
    add('q10b', 'Q10(b)', '4-3-2', 'dairy-cycle-days',
        'Read the following paragraph on dairy farming and match each capital letter with the correct number of days from the list below. List: 37 days; 21 days; 60 days; 282 days; 4 days; 305 days. '
        'Cows are in heat or ‘bulling’ every __A__ days. The cow is pregnant or ‘in-calf’ for __B__ days. After calving the cow produces a special type of milk called colostrum for about __C__ days. '
        'The cow produces milk for an average of __D__ days in the year. The cow reaches her peak milk yield about __E__ days after calving. The cow should be ‘dried-off’ about __F__ days before the birth of the next calf.',
        [menu(['A 21 days', 'B 282 days', 'C 4 days', 'D 305 days', 'E 37 days', 'F 60 days'], [6, 6, 4, 4, 2, 2], 'All six, 2(6m) + 2(4m) + 2(2m). ' + FIRST.format('6, 6, 4, 4, 2, 2'))],
        node='3-4|3-0')
    rearing = [('calf', 'Calf rearing', 'Remove mucus|iodine on navel|colostrum|good housing or two named examples|hygienic conditions|(whole) milk|milk replacer|meal|hay|silage|disease control|weaning|“let- out” to grass (at 12 weeks)|leader-follower system|parasite control', ''),
               ('heifer', 'Rearing replacement heifer', 'select calf with good dairy characteristics|calf should reach 200 kg at housing|silage|meal|300kg at 15 months/mated|easy calving bull|450 kg at housing second winter|500-525 kg at calving',
                ' [Accept any points from calf rearing above]')]
    rows, variants = routes([(slug, label, [menu(steps, [7, 3, 3, 3], f'{label}: any four, 7m + 3(3m).{extra}')]) for slug, label, steps, extra in rearing])
    add('q10c', 'Q10(c)', '4-3-2', 'calf-or-heifer-rearing', 'Calving is a very important event on the dairy farm. List four steps to help ensure successful calf rearing or successful replacement heifer rearing.', rows,
        selection=closed(1, [label for _, label, *_ in rearing]), node='3-4', extra={'answerVariants': variants})
    add('q10d', 'Q10(d)', '4-3-2', 'milking-hygiene', 'Describe any two ways to ensure good hygiene during milking and milk storage.',
        [menu('Clean housing|clean parlour|wash teats and udders|check for mastitis|fly control|teat dips|change filters|wash bulk tank|plate cooling|bulk tank cooling', [4, 4], 'Any two (2 x 4m).')], node='3-4')
    # Question 11 ------------------------------------------------------------
    add('q11a', 'Q11(a)', '3-3-1', 'seed-mixture-grasses', 'Name two grass species that are commonly used in grass seed mixtures.',
        [menu('PRG|IRG|Cocksfoot|Meadow fescue|Timothy|Meadow foxtail', [3, 3], 'Any two (2 x 3m).')], node='2-6')
    tiller = 'Tillering of young grass plants is important in establishing a good grass sward.'
    add('q11bi', 'Q11(b)(i)', '3-1', 'tillering', 'What is meant by the term tillering?', [point('Tillering: Growth of side-shoot (from base of main stem)', 6)], tiller, node='2-6')
    add('q11bii', 'Q11(b)(ii)', '3-3-2', 'encouraging-tillering', 'Describe two ways by which the farmer can encourage tillering.',
        [menu('Damage to main stem|close grazing|sheep or calves|topping|rolling|(Phosphorus) fertiliser', [4, 4], 'Encouraged by: any two (2 x 4m).')], tiller, node='2-6')
    add('q11c', 'Q11(c)', '3-3-2', 'paddock-and-set-stocking', 'Paddock grazing and set stocking are two grazing systems. With the aid of labelled diagrams, explain both of these systems.',
        [point('Diagrams', 4, 'Diagrams (2m +2m). [Full marks may be awarded for each point labelled in each diagram drawn]', kind='criterion'),
         menu('Land divided|(21) equal sized paddocks|permanent roadway|permanent fencing|water in each|one paddock per day|N fertiliser after grazing|animals return to 1st paddock after 22 days|efficient|expensive', [5, 5],
              'Paddock: any two (2 x 5m).'),
         menu('Access to all land|no divisions|no roadway|not efficient|patchy grazing|cheaper|topping', [5, 5], 'Set stocking: any two (2 x 5m).')],
        node='2-6')
    add('q11d', 'Q11(d)', '3-3-3', 'hay-versus-silage', 'Compare hay and silage under the following headings: (i) Method of preservation. (ii) Digestibility.',
        [split('(i) Hay — Dehydration or drying or removal of water', SHARED.format('7m + 3(3m)') + ' Four answers: hay and silage under each heading. Any one each.'),
         split('(i) Silage — (Controlled) fermentation or anaerobic/ pickling or acid'),
         split('(ii) Hay — Less digestible/ more fibre/ stemmy/ low DMD'), split('(ii) Silage — More digestible/ less fibre/ leafy/ higher DMD')],
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '7m + 3(3m)'}, node='2-6')
    # Question 12 ------------------------------------------------------------
    two = 'Answer any two of the following (a), (b), (c), (d).'
    add('q12ai', 'Q12(a)(i)', '4-3-2', 'weanling-winter-housing', 'Describe three features of good winter housing for weanlings.',
        [menu('Well ventilated|free from draughts|clean water|adequate feed space|slats|straw bed|adequate floor space|slurry holding capacity|adequate (cubic) air capacity|hygiene', [6, 4, 2],
              'Any three (6m + 4m + 2m).')], two, node='3-4')
    add('q12aii', 'Q12(a)(ii)', '4-3-1', 'calf-to-beef-weights',
        'Give the approximate live weight for cattle at the following stages of the two-year ‘calf-to-beef’ system: 1. First winter housing. 2. Slaughter.',
        [menu(['Weight at first winter 200-220 kg', 'Weight at slaughter 600-700 kg'], [6, 2], 'Both (6m + 2m). ' + FIRST.format('6m + 2m'))], two, node='3-3')
    add('q12aiii', 'Q12(a)(iii)', '4-3-1', 'conformation-and-fatness', 'At slaughter the beef carcass is graded for conformation and fatness. Explain each underlined term.',
        [menu('Muscle distribution|on back and hindquarters|graded EUROP|Shape of an animal (around the bones)', [4, 1], 'Conformation: any two (4m + 1m).'),
         menu('Amount of fat on carcass|tail area or hindquarters|graded 1-5', [4, 1], 'Fatness: any two (4m +1m).')], two, node='3-3')
    add('q12bi', 'Q12(b)(i)', '2-2-2', 'texture-and-structure', 'Explain the terms soil texture and soil structure.',
        [point('Soil Texture: Amount or percentage of sand, silt and clay in a soil.', 3), point('Soil structure: (coming together of soil particles to form) aggregates or crumbs or peds.', 3)], two, node='1-3')
    add('q12bii', 'Q12(b)(ii)', '2-2-2', 'soil-texture-types', 'Give two characteristics of each of the following soil texture types: 1. Sandy soil. 2. Loam soil. 3. Clay soil.',
        [menu('Good drainage|good aeration|light|low inherent fertility|warm|early|prone to drought|prone to leaching|easy to till|low CEC', [2, 2], 'Sandy soil: any two (2 x 2m).'),
         menu('Good drainage|good aeration|fertile|light|warm|retains water|not waterlogged|easy to till.', [2, 2], 'Loam soil: any two (2 x 2m).'),
         menu('Poor drainage|poor aeration|heavy|plastic|cold|waterlogged|late|good inherent fertility|difficult to till|retains water.', [2, 2], 'Clay soil: any two (2 x 2m).')], two, node='1-3')
    methods = [('sieve', 'Sieve method', 'Oven dry sample|crush sample|weigh sample|place in sieves|cover|shake|weigh each sieve contents|calculation|soil triangle'),
               ('sedimentation', 'Sedimentation method', 'Add sample to water|stir|add mixture to graduated cylinder|stopper|shake|settle overnight|note layers|record amounts|calculation|soil triangle'),
               ('feel', 'Feel method', 'Handle dry soil|note feel gritty or non-gritty|moisten the soil|note cohesivness|plasticity|grittiness|knead into ball|can it be rolled into threads|can it be bent into threads')]
    rows, variants = routes([(slug, label, [menu(steps, [6, 4, 2], f'{label}: any three (6m + 4m + 2m).')]) for slug, label, steps in methods])
    add('q12biii', 'Q12(b)(iii)', '2-2-2', 'percentage-clay-experiment', 'Describe an experiment to estimate the percentage clay in a soil sample.', rows, two,
        selection=closed(1, [label for _, label, _ in methods]), node='1-3|0-1', extra={'answerVariants': variants})
    stomach = two + ' The diagram below shows the ruminant stomach.'
    figured(add('q12ci', 'Q12(c)(i)', '4-1', 'ruminant', 'Explain the term ruminant.',
                [menu('An animal whose stomach consists of 4 compartments|chews the cud.', [6], 'Any one (6m).')], stomach, node='3-0'), 'q12ci')
    figured(add('q12cii', 'Q12(c)(ii)', '4-1', 'ruminant-stomach-parts', 'Name the parts labelled A, B, C from the diagram. (Part D is already labelled).',
                [menu(['A – Rumen or paunch (stomach)', 'B – Reticulum or honeycomb (stomach)', 'C - Abomasum or true stomach'], [6, 4, 4], 'All three (6m + 4m + 4m). ' + FIRST.format('6m + 4m + 4m'))],
                stomach, node='3-0'), 'q12cii')
    figured(add('q12ciii', 'Q12(c)(iii)', '4-1', 'rumen-function', 'Explain what happens in part A of the stomach.',
                [menu('Breakdown of cellulose|digestion of plant material|protein synthesis.', [6], 'Any one (6m).')], stomach, node='3-0'), 'q12ciii')
    figured(add('q12civ', 'Q12(c)(iv)', '4-1', 'first-chamber-in-young', 'Which chamber of the stomach is used first by calves and lambs?',
                [menu('C|abomasum|true stomach.', [4], 'Any one (4m).')], stomach, node='3-0'), 'q12civ')
    explain = two + ' Give a scientific explanation for each of the following:'
    for key, ref, topic, concept, item, options, node in [
            ('q12di', 'Q12(d)(i)', '4-3-2', 'farrowing-crate', 'The use of a farrowing crate for a sow.', 'Prevents crushing|easy suckling|access to creep area.', '3-4'),
            ('q12dii', 'Q12(d)(ii)', '4-3-2', 'creep-feeding-calves', 'Creep feeding of calves.',
             'Calves access to meal only|increased growth rates|earlier weaning|best grass|parasite control|faster development of rumen|gets used to solid food', '3-4'),
            ('q12diii', 'Q12(d)(iii)', '2-3', 'mixed-shelter-belts', 'Using a mixture of tree species in shelter belts.', 'Attractive|biodiversity|conifers give shelter in winter.', '1-6'),
            ('q12div', 'Q12(d)(iv)', '3-3-2', 'white-patches-on-barley', 'White patches on the leaves of barley plants.',
             'Powdery mildew|fungus|disease|nutrient deficiency|fertiliser scorch|spray damage.', '2-4'),
            ('q12dv', 'Q12(d)(v)', '4-3-3', 'fluke-on-wet-land', 'Higher numbers of fluke in the livers of sheep grazing on wet land.',
             'Mud snail or secondary host lives in wet area|Life cycle stages or named stages need water', '3-5')]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item, [menu(options, [6], 'Any one (6m).')], explain, node=node)
    # Question 13 ------------------------------------------------------------
    add('q13a', 'Q13(a)', '4-1', 'diploid-incomplete-dominance-progeny', 'Explain each of the following terms: (i) Diploid. (ii) Incomplete dominance. (iii) Progeny testing.',
        [split('(i) Diploid — Two sets of chromosomes/ two copies of each chromosome', SHARED.format('8m + 6m+ 2m') + ' Three answers, one for each term (the scheme numbers the third "(iv)"). Any one each.'),
         split('(ii) Incomplete dominance — Two alleles equally dominant/ co-dominance/ phenotype a blend or any detailed example.'),
         split('(iii) Progeny testing — Testing of bull’s offspring compared to other bull’s offspring (under similar feed and housing conditions)')],
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '8m + 6m+ 2m'}, node='3-6')
    peas = ('In pea seeds the allele for round seeds (R) is dominant over the allele for wrinkled seeds (r). A pea plant, homozygous for round seeds (RR), was crossed with a pea plant homozygous for wrinkled seeds (rr). '
            'The offspring (F1) were heterozygous. Copy the following into your answer book and complete the spaces. Genotypes of parents (RR) × (rr).')
    add('q13bi', 'Q13(b)(i)', '4-1', 'pea-gametes', 'Complete: (i) Gametes ( ) × ( )', [point('Gametes (R) x (r)', 8, '(2 x 4m).')], peas, node='3-6')
    add('q13bii', 'Q13(b)(ii)', '4-1', 'pea-f1-genotype', 'Complete: (ii) Genotype of offspring (F1) ( )', [point('F1 genotype (Rr)', 4)], peas, node='3-6')
    add('q13biii', 'Q13(b)(iii)', '4-1', 'pea-f1-phenotype', 'Complete: (iii) Phenotype of offspring (F1) ___', [point('F1 phenotype round', 4)], peas, node='3-6')
    add('q13c', 'Q13(c)', '4-1', 'wrinkled-test-cross',
        'In your answer book show a cross between a wrinkled-seeded plant and an F1 plant from the answer above. Show: (i) Genotypes of parents ( ) × ( ) (ii) Gametes ( ) × ( ) ( ) '
        '(iii) Genotypes of offspring ( ) ( ) (iv) Phenotypes of offspring ___ ___',
        [point('Genotypes of parents (rr) x (Rr)', 4, '(2 x 2m).'), point('Gametes (r) x (R) (r)', 6, '(3 x 2m).'),
         point('F2 genotype (Rr) x (rr)', 2, '(2 x 1m).'), point('F2 phenotypes round wrinkled', 2, '(2 x 1m).')],
        'In pea seeds the allele for round seeds (R) is dominant over the allele for wrinkled seeds (r). A pea plant, homozygous for round seeds (RR), was crossed with a pea plant homozygous for wrinkled seeds (rr). The offspring (F1) were heterozygous.',
        node='3-6')
    add('q13d', 'Q13(d)', '4-1', 'drosophila-in-genetics', 'Fruit flies (Drosophila) are widely used when studying genetics. Give three reasons for this.',
        [menu('Easy to keep|large no of offspring|new generation quickly|few chromosomes|mutations well documented|(larvae) have giant chromosomes|chromosomes easy to identify.', [8, 4, 2],
              'Any three (8m + 4m + 2m).')], node='3-6')
    assert len(p.tasks) == 49, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('49 base tasks, one card each. Section One is one task per question: Q7 prints one scale across its parts (orderedSplit); the other questions carry '
                          'the scheme\'s own row marks or one-pool steps. Section Two parts are priced on their own; Q11(d) and Q13(a) print one scale across their parts. '
                          'Q10(c) calf or heifer rearing and Q12(b)(iii) soil-texture methods are answer routes.')
