"""2013 Ordinary: every task authored from the SEC paper and marking scheme (no cards existed).

All 12 paper pages and 16 scheme pages were inspected and the independent census transcribed
before authoring: 62 base tasks, one card each. Section One questions are one task each, their
rows carrying the scheme's own marks (5 x 4m, 5 x (2m + 2m), 10 x 2m and the per-part values of
Q3 and Q6). Section Two parts are priced on their own. The Q12(d) cross is one task because its
genotype and phenotype marks are tied line to line. The Q13(b)(iii) species (PRG, IRG or clover)
are answer routes. Answers are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed, routes

FILE = 'LC024GLP000EV.pdf'
HASHES = {'exampapers': '4681992b7ebd6dc0340ad28122b85dd60f0caf6642481bb1a0f9a123b257d249',
          'markingschemes': '35f8630e40044a6434575a758b2e2c26550dedc5dc57020583113b833ab16c79'}
SELECTIONS = {
    '16d8f869c593305a': ('exam-selection', 'Section One: six of seven independent 20-mark questions; every question is retained.'),
    'bab91ba584e07509': ('open', 'Q6(b): any two reasons for culling cows from the scheme pool; a marking menu.'),
    '25e48480df75745e': ('exam-selection', 'Section Two: three of six independent 60-mark questions; every question is retained.'),
    '31b6c84d76847961': ('open', 'Q11(a)(ii): any three benefits of earthworms from the scheme pool; a marking menu.'),
    '6109958a9fd4bb14': ('open', 'Q11(b)(i): any three soil-forming factors from the scheme\'s five; a marking menu.'),
    '2e4f1117c27adc08': ('independent-task-selection', 'Q13: two of four independently priced 30-mark parts; all four are retained.'),
    '2f14927affc1b079': ('open', 'Q13(b)(ii): any two grass seed species from the scheme pool; a marking menu.'),
    '9ed086aac0f737b4': ('closed', 'Q13(b)(iii): one of the species named in (ii); the scheme gives features for PRG, IRG and clover, kept as answer routes on one card.'),
    '47a35a7b93299b1e': ('closed', 'Q13(b)(iii): the same choice of one species, kept as answer routes on one card.'),
    'e7baebbfc96e76ca': ('open', 'Q13(d)(i): any three labels on the candidate\'s own drawing (a marking criterion).'),
}
SUPPLEMENTARY = []
ATLAS = {
    'Q1': 'animal-diseases', 'Q2': 'crop-production|grassland', 'Q3': 'crop-production|animal-diseases',
    'Q4': 'crop-production|animal-production|soil-science|fertilisers-pollution-the-environment|animal-physiology|plant-physiology|classification-of-organisms',
    'Q5': 'animal-production|health-safety', 'Q6': 'animal-production', 'Q7': 'grassland|animal-production|health-safety|animal-diseases',
    'Q8': 'crop-production', 'Q8(d)': 'crop-production|scientific-practices-experiments-investigations',
    'Q9': 'animal-production', 'Q10': 'animal-production',
    'Q11(a)': 'soil-science|classification-of-organisms', 'Q11(a)(iii)': 'soil-science|scientific-practices-experiments-investigations',
    'Q11(b)': 'soil-science', 'Q11(c)': 'soil-science', 'Q11(d)': 'soil-science|fertilisers-pollution-the-environment',
    'Q12(a)': 'genetics|animal-production', 'Q12(b)': 'plant-physiology|genetics', 'Q12(c)': 'genetics', 'Q12(d)': 'genetics',
    'Q13(a)': 'crop-production', 'Q13(b)': 'grassland|classification-of-organisms', 'Q13(c)': 'animal-production|animal-diseases',
    'Q13(d)': 'animal-physiology|animal-diseases',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1': (P((2, 0.293, 0.710)), P((5, 0.124, 0.312))),
    'Q2': (P((3, 0.041, 0.953)), P((5, 0.312, 0.627))),  # trimmed above the page footer
    'Q3': (P((4, 0.041, 0.461)), P((5, 0.627, 0.817))),
    'Q4': (P((4, 0.461, 0.887)), P((6, 0.080, 0.277))),
    'Q5': (P((5, 0.041, 0.609)), P((6, 0.277, 0.441))),  # trimmed above the page footer
    'Q6': (P((6, 0.041, 0.638)), P((6, 0.441, 0.605))),
    'Q7': (P((7, 0.041, 0.855)), P((6, 0.605, 0.861))),  # trimmed above the page footer
    'Q8(a)(i)': (P((8, 0.214, 0.263)), P((7, 0.119, 0.184))),
    'Q8(a)(ii)': (P((8, 0.214, 0.244), (8, 0.263, 0.289)), P((7, 0.119, 0.151), (7, 0.184, 0.217))),
    'Q8(b)(i)': (P((8, 0.214, 0.244), (8, 0.289, 0.323)), P((7, 0.119, 0.151), (7, 0.217, 0.266))),
    'Q8(b)(ii)': (P((8, 0.214, 0.244), (8, 0.289, 0.308), (8, 0.323, 0.338)), P((7, 0.119, 0.151), (7, 0.266, 0.331))),
    'Q8(b)(iii)': (P((8, 0.214, 0.244), (8, 0.289, 0.308), (8, 0.338, 0.354)), P((7, 0.119, 0.151), (7, 0.331, 0.365))),
    'Q8(b)(iv)': (P((8, 0.214, 0.244), (8, 0.289, 0.308), (8, 0.354, 0.379)), P((7, 0.119, 0.151), (7, 0.365, 0.431))),
    'Q8(c)': (P((8, 0.214, 0.244), (8, 0.379, 0.424)), P((7, 0.119, 0.151), (7, 0.431, 0.480))),
    'Q8(d)': (P((8, 0.214, 0.244), (8, 0.424, 0.559)), P((7, 0.119, 0.151), (7, 0.480, 0.573))),
    'Q9(a)(i)': (P((8, 0.559, 0.609)), P((8, 0.080, 0.145))),
    'Q9(a)(ii)': (P((8, 0.559, 0.590), (8, 0.609, 0.635)), P((8, 0.080, 0.113), (8, 0.145, 0.228))),
    'Q9(b)': (P((8, 0.559, 0.590), (8, 0.635, 0.680)), P((8, 0.080, 0.113), (8, 0.228, 0.310))),
    'Q9(c)(i)': (P((8, 0.559, 0.590), (8, 0.680, 0.714)), P((8, 0.080, 0.113), (8, 0.310, 0.410))),
    'Q9(c)(ii)': (P((8, 0.559, 0.590), (8, 0.680, 0.699), (8, 0.714, 0.740)), P((8, 0.080, 0.113), (8, 0.310, 0.333), (8, 0.410, 0.492))),
    'Q9(d)(i)': (P((8, 0.559, 0.590), (8, 0.740, 0.774)), P((8, 0.080, 0.113), (8, 0.492, 0.525))),
    'Q9(d)(ii)': (P((8, 0.559, 0.590), (8, 0.740, 0.759), (8, 0.774, 0.789)), P((8, 0.080, 0.113), (8, 0.525, 0.558))),
    'Q9(d)(iii)': (P((8, 0.559, 0.590), (8, 0.740, 0.759), (8, 0.789, 0.804)), P((8, 0.080, 0.113), (8, 0.558, 0.607))),
    'Q9(d)(iv)': (P((8, 0.559, 0.590), (8, 0.740, 0.759), (8, 0.804, 0.826)), P((8, 0.080, 0.113), (8, 0.607, 0.633))),
    'Q10(a)(i)': (P((9, 0.041, 0.105)), P((9, 0.080, 0.162))),
    'Q10(a)(ii)': (P((9, 0.041, 0.090), (9, 0.105, 0.131)), P((9, 0.080, 0.103), (9, 0.162, 0.359))),
    'Q10(b)(i)': (P((9, 0.041, 0.071), (9, 0.131, 0.180)), P((9, 0.080, 0.103), (9, 0.359, 0.392))),
    'Q10(b)(ii)': (P((9, 0.041, 0.071), (9, 0.131, 0.165), (9, 0.180, 0.195)), P((9, 0.080, 0.103), (9, 0.392, 0.425))),
    'Q10(b)(iii)': (P((9, 0.041, 0.071), (9, 0.131, 0.165), (9, 0.195, 0.221)), P((9, 0.080, 0.103), (9, 0.425, 0.474))),
    'Q10(c)': (P((9, 0.041, 0.071), (9, 0.221, 0.251)), P((9, 0.080, 0.103), (9, 0.474, 0.572))),
    'Q10(d)': (P((9, 0.041, 0.071), (9, 0.251, 0.401)), P((9, 0.080, 0.103), (9, 0.572, 0.748))),
    'Q11(a)(i)': (P((9, 0.401, 0.598)), P((10, 0.080, 0.147))),  # the whole (a) block: its parts sit beside the photograph
    'Q11(a)(ii)': (P((9, 0.401, 0.598)), P((10, 0.080, 0.103), (10, 0.147, 0.213))),  # the whole (a) block: its parts sit beside the photograph
    'Q11(a)(iii)': (P((9, 0.401, 0.598)), P((10, 0.080, 0.103), (10, 0.213, 0.311))),  # the whole (a) block: its parts sit beside the photograph
    'Q11(b)(i)': (P((9, 0.401, 0.431), (9, 0.596, 0.615)), P((10, 0.080, 0.103), (10, 0.311, 0.361))),
    'Q11(b)(ii)': (P((9, 0.401, 0.431), (9, 0.615, 0.657)), P((10, 0.080, 0.103), (10, 0.361, 0.460))),
    'Q11(c)(i)': (P((9, 0.401, 0.431), (9, 0.657, 0.706)), P((10, 0.080, 0.103), (10, 0.460, 0.493))),
    'Q11(c)(ii)': (P((9, 0.401, 0.431), (9, 0.657, 0.691), (9, 0.706, 0.732)), P((10, 0.080, 0.103), (10, 0.493, 0.559))),
    'Q11(d)': (P((9, 0.401, 0.431), (9, 0.732, 0.787)), P((10, 0.080, 0.103), (10, 0.559, 0.634))),  # trimmed above the page footer
    'Q12(a)(i)': (P((10, 0.041, 0.135)), P((11, 0.080, 0.163))),
    'Q12(a)(ii)': (P((10, 0.041, 0.116), (10, 0.135, 0.176)), P((11, 0.080, 0.113), (11, 0.163, 0.244))),
    'Q12(b)(i)': (P((10, 0.041, 0.071), (10, 0.176, 0.420)), P((11, 0.080, 0.113), (11, 0.244, 0.343))),
    'Q12(b)(ii)': (P((10, 0.041, 0.071), (10, 0.176, 0.401), (10, 0.420, 0.435)), P((11, 0.080, 0.113), (11, 0.343, 0.375))),
    'Q12(b)(iii)': (P((10, 0.041, 0.071), (10, 0.176, 0.401), (10, 0.435, 0.461)), P((11, 0.080, 0.113), (11, 0.375, 0.425))),
    'Q12(c)(i)': (P((10, 0.041, 0.071), (10, 0.461, 0.611)), P((11, 0.080, 0.113), (11, 0.425, 0.474))),
    'Q12(c)(ii)': (P((10, 0.041, 0.071), (10, 0.461, 0.581), (10, 0.611, 0.641)), P((11, 0.080, 0.113), (11, 0.474, 0.507))),
    'Q12(c)(iii)': (P((10, 0.041, 0.071), (10, 0.461, 0.581), (10, 0.641, 0.672)), P((11, 0.080, 0.113), (11, 0.507, 0.539))),
    'Q12(d)': (P((10, 0.041, 0.071), (10, 0.672, 0.887)), P((11, 0.080, 0.113), (11, 0.539, 0.681))),
    'Q13(a)(i)': (P((11, 0.041, 0.120)), P((12, 0.080, 0.146))),
    'Q13(a)(ii)': (P((11, 0.041, 0.101), (11, 0.120, 0.135)), P((12, 0.080, 0.113), (12, 0.146, 0.195))),
    'Q13(a)(iii)': (P((11, 0.041, 0.101), (11, 0.135, 0.150)), P((12, 0.080, 0.113), (12, 0.195, 0.293))),
    'Q13(a)(iv)': (P((11, 0.041, 0.101), (11, 0.150, 0.191)), P((12, 0.080, 0.113), (12, 0.293, 0.392))),
    'Q13(b)(i)': (P((11, 0.041, 0.101), (11, 0.191, 0.476)), P((12, 0.080, 0.113), (12, 0.392, 0.490))),
    'Q13(b)(ii)': (P((11, 0.041, 0.101), (11, 0.476, 0.496)), P((12, 0.080, 0.113), (12, 0.490, 0.523))),
    'Q13(b)(iii)': (P((11, 0.041, 0.101), (11, 0.496, 0.552)), P((12, 0.080, 0.113), (12, 0.523, 0.730))),
    'Q13(c)(i)': (P((11, 0.041, 0.101), (11, 0.552, 0.586)), P((12, 0.080, 0.113), (13, 0.080, 0.261))),
    'Q13(c)(ii)': (P((11, 0.041, 0.101), (11, 0.586, 0.615)), P((12, 0.080, 0.113), (13, 0.261, 0.310))),
    'Q13(c)(iii)': (P((11, 0.041, 0.101), (11, 0.615, 0.657)), P((12, 0.080, 0.113), (13, 0.310, 0.392))),
    'Q13(d)(i)': (P((11, 0.041, 0.101), (11, 0.657, 0.675)), P((12, 0.080, 0.113), (13, 0.392, 0.476))),
    'Q13(d)(ii)': (P((11, 0.041, 0.101), (11, 0.675, 0.706)), P((12, 0.080, 0.113), (13, 0.476, 0.525))),
    'Q13(d)(iii)': (P((11, 0.041, 0.101), (11, 0.706, 0.721)), P((12, 0.080, 0.113), (13, 0.525, 0.591))),
    'Q13(d)(iv)': (P((11, 0.041, 0.101), (11, 0.721, 0.742)), P((12, 0.080, 0.113), (13, 0.591, 0.621))),
}
FIGURES = {
    'q2': ('agsci-2013-ol-paper-farm-machinery', [('A', 'Hay tedder', True), ('B', 'Combine harvester', True), ('C', 'Subsoiler', True), ('D', 'Disc harrow', True), ('E', 'Roller', True)]),
    'q12bi': ('agsci-2013-ol-paper-plant-cell', [('A', 'Cytoplasm', True), ('B', 'Nucleus', True), ('C', 'Chloroplast', True), ('D', 'Vacuole', True), ('E', 'Cell Wall', True)]),
    'q12bii': ('agsci-2013-ol-paper-plant-cell', None), 'q12biii': ('agsci-2013-ol-paper-plant-cell', None),
    'q13bi': ('agsci-2013-ol-paper-grass-species', [('A', 'Perennial ryegrass', True), ('B', 'Meadow foxtail', True), ('C', 'Italian ryegrass', True), ('D', 'Cocksfoot', True)]),
}


def figured(card, key):
    figure, labels = FIGURES[key]
    card['figureKey'] = figure
    if labels:
        card['labelKey'] = [dict(letter=l, meaning=m, askedInThisQuestion=a) for l, m, a in labels]
    return card


def build():
    p = Paper(2013, 'ordinary', FILE, HASHES, REGIONS, ATLAS, 12, 16, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if int(ref.split('(')[0].split(' ')[0][1:]) <= 7 else 'B')
    add = p.add
    # Section One ------------------------------------------------------------
    add('q1', 'Q1', '4-3-3', 'animal-disease-causes',
        'A list of common animal diseases is given below. Place these in Column A to match the cause of each disease in Column B. The first one is completed as an example. '
        'List: Red Water Fever; Mastitis; Milk Fever; Sheep Scab; Joint-ill Disease; Twin-lamb Disease. Example: Milk Fever — Deficiency of calcium. '
        'Column B: Caused by mange mite; Bacterial disease of udder; Caused by protozoan Babesia; Ewes lacking nutrition; Bacteria enter the navel.',
        [menu(['Sheep scab: Caused by mange mite', 'Mastitis: Bacterial disease of udder', 'Red water fever: Caused by protozoan Babesia',
               'Twin-lamb disease: Ewes lacking nutrition', 'Joint-ill disease: Bacteria enter the navel'], [4] * 5, 'One disease for each cause, 4 marks each (5 x 4m).')],
        tariff={'kind': 'fixed', 'notation': '5 x 4m'}, node='3-5')
    machines = [('Roller', 'E', 'Breaking large clods/ smoothing or levelling soil surface/ compacting soil/ burying seeds/ burying stones/ improving seed-soil contact/ rolling silage ground/ rolling grass/ encouraging tillering'),
                ('Disc harrow', 'D', 'Preparation of seedbed/ breakdown of soil/ cultivation of soil'),
                ('Combine harvester', 'B', 'Harvesting (cereal) crops/ separating grain from straw'),
                ('Subsoiler', 'C', 'Shatters soil/ loosens soil/ alleviates soil compaction/ breaks up soil pan/ improves drainage'),
                ('Hay tedder', 'A', 'Shakes grass (or hay)/ separates grass/ turns hay/ gathers hay into rows (for baling)/ (helps) to dry hay')]
    figured(add('q2', 'Q2', '3-3-1', 'farm-machinery-letters-uses',
                'All the machinery shown in the photographs below is used on farms. (a) Match the letters over the photographs with the names of the machines in the table. '
                '(b) Give the main use of each piece of machinery in the table: Roller; Disc harrow; Combine harvester; Subsoiler; Hay tedder.',
                [menu([f'{name}: {letter}' for name, letter, _ in machines], [2] * 5, '5 x (2m + 2m): (a) the letter 2 for each machine.'),
                 menu([f'{name}: {use}' for name, _, use in machines], [2] * 5, '(b) The main use on farm 2 for each machine.')],
                tariff={'kind': 'fixed', 'notation': '5 x (2m + 2m)'}, node='2-3|2-5|2-6'), 'q2')
    add('q3', 'Q3', '3-3-2', 'potato-varieties-and-pests',
        '(a) Name one variety of maincrop potatoes. (b) In Ireland, seed potatoes are mainly grown in Co. Donegal. Give a reason for this. '
        '(c) State two methods of prevention or control of potato blight. (d) Name one common insect pest of potatoes.',
        [point('(a) Maincrop variety — Kerr Pink/ Rooster/ Golden Wonder/ Record/ Cara/ Maris Piper', 4),
         point('(b) Seed potatoes in Donegal — Free from aphids/ reduced spread of diseases', 4),
         menu('Spraying|fungicide or named fungicide|earthing up|resistant varieties|burn off haulms|certified seed|avoid groundkeepers|isolate potato dumps|rotation|remove infected plants', [4, 4],
              '(c) Blight prevention or control: any two, 2 x 4m.'),
         point('(d) Insect pest — Wireworms/ aphids/ leatherjackets', 4)],
        tariff={'kind': 'fixed', 'notation': '4 + 4 + 2 x 4m + 4'}, node='2-1|2-4')
    statements = [('a', 'Powdery mildew is a disease of cereals.', 'T'), ('b', 'Scottish Blackface is a mountain sheep breed.', 'T'), ('c', 'Tillering means cultivating the soil.', 'F'),
                  ('d', 'Thistle belongs to the family Compositae (Asteraceae).', 'T'), ('e', 'Urea is a fertilizer high in potassium.', 'F'), ('f', 'Hay has a high moisture content.', 'F'),
                  ('g', 'Cattle have a monogastric stomach.', 'F'), ('h', 'Most food chains begin with a green plant.', 'T'), ('i', 'Holstein is a common beef breed.', 'F'),
                  ('j', 'Positive phototropism is the growth response of a plant towards light.', 'T')]
    add('q4', 'Q4', '4-1', 'true-or-false-farm-science',
        'Indicate whether the following statements are true (T) or false (F) by placing a circle around the correct answer in each case. An example is shown. '
        'Example: Limestone is a sedimentary rock — T. ' + ' '.join(f'({k}) {s}' for k, s, _ in statements),
        [menu([f'({k}) {a}' for k, _, a in statements], [2] * 10, 'All ten statements, 2 marks each (10 x 2m). T = true, F = false; the scheme gives each letter with T or F.')],
        tariff={'kind': 'fixed', 'notation': '10 x 2m'}, node='2-4|3-1|2-6|2-1|1-6|3-0|2-0')
    add('q5', 'Q5', '4-3-3', 'farm-equipment-uses',
        'The following pieces of equipment are used regularly in agriculture. Give a use for each piece of equipment in the space provided. (a) Burdizzo (b) Fostering crate (c) Infra-red lamp (d) Bulk tank (e) Calving jack.',
        [point('(a) Burdizzo — Castration (of male animals)/ crushes spermatic cord/ cuts off blood supply to the testes/ prevents unwanted breeding', 4, 'One use for each, 4 marks each (5 x 4m).'),
         point('(b) Fostering crate — Adoption or fostering of lambs', 4),
         point('(c) Infra-red lamp — Warms animal / heating of chilled animals/ prevention of water freezing in farm buildings', 4),
         point('(d) Bulk tank — Storage of milk for collection/ cooling of milk/ prevents growth of bacteria/ prevents souring of milk', 4),
         point('(e) Calving jack — Assists calving process/ for difficult births', 4)],
        tariff={'kind': 'fixed', 'notation': '5 x 4m'}, node='3-5|3-4')
    add('q6', 'Q6', '4-2', 'friesian-and-culling',
        '(a) (i) The Friesian cow is described as a dual-purpose breed. Explain the term dual-purpose in this context. (ii) What is the expected milk yield in litres per lactation for a high yielding Holstein-Friesian cow? '
        '(iii) At what age might a cow be expected to reach her maximum milk yield? (b) Cows may have to be removed or culled from the herd for a number of reasons. Outline any two reasons for culling cows.',
        [point('(a)(i) Dual-purpose — Produces both milk and beef', 4), point('(a)(ii) Milk yield — 6000 litres – 12,000 litres', 4), point('(a)(iii) Age of maximum yield — 7 – 8 years', 4),
         menu('Age|disease|infertility|lameness|high cell count|grading up|calving difficulties|low milk yield|poor milk quality|breeding policy|hard to get in calf|bad temperament', [4, 4],
              '(b) Reasons for culling: any two, 2 x 4m.')],
        tariff={'kind': 'fixed', 'notation': '3 x 4m + 2 x 4m'}, node='3-1|3-4')
    add('q7', 'Q7', '2-3', 'reasons-for-farm-tasks',
        'Give a scientific reason why each of the following tasks is carried out on farms: (a) Silage pits are rolled. (b) Sheep are walked through a foot-bath. (c) Milking cows are fed dairy rations. '
        '(d) Hay is introduced to the diet of a calf about one week after birth. (e) Slurry is agitated from outside slatted houses.',
        [point('(a) Rolling silage pits — Excludes air/ provides anaerobic conditions/ allows fermentation/ encourages lactic acid bacteria/ reduces pit size', 4, 'One reason for each task, 4 marks each (5 x 4m).'),
         point('(b) Foot-bath — Prevents foot rot/ prevents foot scald/ reduces lameness/ kills bacteria/ prevents infection in feet', 4),
         point('(c) Dairy rations — Provides minerals or named mineral/ prevents grass tetany/ prevents milk fever/ ensures cow reaches peak yield/ increases milk yield/ supplements silage or grass/ increases BCS/ better quality colostrum/ stronger calf/ increases milk protein', 4),
         point('(d) Hay for calves — Faster development of rumen/ scratch factor/ introduces bacteria into rumen', 4),
         point('(e) Agitating slurry outside — Prevents risk of harm or death/ build- up of poisonous gases or named gas indoors/ legal requirement', 4)],
        tariff={'kind': 'fixed', 'notation': '5 x 4m'}, node='2-6|3-5|3-4|1-6')
    # Question 8 -------------------------------------------------------------
    add('q8ai', 'Q8(a)(i)', '3-2', 'other-cereals', 'Barley is a cereal crop. Name two other cereal crops grown in Ireland.',
        [menu('Wheat|Oats|Maize', [3, 3], 'Any two, 2 x 3m.')], node='2-1')
    add('q8aii', 'Q8(a)(ii)', '3-3-3', 'barley-uses', 'Give two uses of barley.',
        [menu('Animal feed|concentrates|malting or brewing or distilling|straw', [3, 3], 'Any two, 2 x 3m.')], 'Barley is a cereal crop.', node='2-5')
    barley = 'Describe the cultivation of barley under the following headings:'
    for key, ref, topic, concept, heading, options, note, node in [
            ('q8bi', 'Q8(b)(i)', '3-3-1', 'barley-soil-suitability', 'Soil suitability', '(Sandy) loam|good drainage|good aeration|brown earth or grey-brown podzolic|pH 6.5 – 7.0|fertile', 'Any one, 4m.', '2-3'),
            ('q8bii', 'Q8(b)(ii)', '3-3-1', 'barley-sowing', 'Sowing', 'Spring barley: February – April|Winter barley: September – November|corn drill|combine drill|seed sown 3-5cm deep|seeding rate 200kg per ha.|lines 18cm apart', 'Any one, 4m.', '2-3'),
            ('q8biii', 'Q8(b)(iii)', '3-3-2', 'barley-weed-control', 'Weed control', 'Spraying|herbicide|rotation|pulling|certified seed|stubble cleaning', 'Any one, 4m.', '2-4'),
            ('q8biv', 'Q8(b)(iv)', '3-3-3', 'barley-harvesting', 'Harvesting', 'Combine harvester|one sign of ripeness|harvest date - Spring barley: August – October|Winter barley: July - August',
             'Any one, 4m. [Harvest date must match sowing date in part (ii)]', '2-5')]:
        add(key, ref, topic, concept, f'Describe the cultivation of barley under the heading: {heading}.', [menu(options, [4], note)], barley, node=node)
    add('q8c', 'Q8(c)', '3-3-1', 'certified-seed-features', 'Certified seed should be sown when cultivating barley. List three features of certified seed.',
        [menu('True to type|(minimum) purity|high germination rate|free from wild oats|seed treated|higher yields', [4] * 3, 'Any three, 3 x 4m.')], node='2-3')
    add('q8d', 'Q8(d)', '3-1', 'barley-germination-percentage', 'Describe a laboratory or field experiment to estimate the percentage (%) germination of a barley seed sample.',
        [menu('Seeds|count|soak (for 24 hours)|seed tray or suitable container|cotton wool or suitable growing medium|warm place|regular watering|leave for suitable time|count sprouted seeds|repeat for average|control|calculate % germination',
              [4] * 5, 'Any five, 5 x 4m. [Award maximum of 16 marks if candidate omits (reference to) calculation of germination]')], node='2-0|0-1')
    # Question 9 -------------------------------------------------------------
    add('q9ai', 'Q9(a)(i)', '4-2', 'commercial-pig-breeds', 'Name two breeds of pig used in commercial pig production in Ireland.',
        [menu('Landrace|Large White|Duroc', [3, 3], 'Any two, 2 x 3m.')], node='3-1')
    add('q9aii', 'Q9(a)(ii)', '4-2', 'pig-breed-features', 'Describe one feature of each named breed.',
        [menu(['Landrace: Good conformation/ long body/ large hams/ small shoulders/ droopy ears', 'Large white: Prolific/ fast growth/ good meat quality/ good FCR/ good mothering ability/ erect ears'],
              [4, 4], 'One feature of each of your two breeds, 4m each.')], 'Name two breeds of pig used in commercial pig production in Ireland.', node='3-1')
    add('q9b', 'Q9(b)', '4-3-3', 'newborn-bonham-practices', 'List two managerial practices carried out on bonhams (piglets) during the first week after birth.',
        [menu('Teeth clipping|tail docking|iron injection|navel dip|ear notching|infrared lamp|water supply|colostrum or ensure piglet sucks the sow|introduce creep feed|maintain good hygiene', [4, 4],
              'Any two, 2 x 4m.')], node='3-5')
    houses = 'Describe the management of pigs in the following pig production houses:'
    add('q9ci', 'Q9(c)(i)', '4-3-2', 'dry-sow-house', 'Describe the management of pigs in the dry sow house.',
        [menu('Temp 20°C|sows fed on (sow) ration or concentrates or meals|thin sows fed extra ration|oestrus detection|mated or served|second day of oestrus|double served|vaccinated|washed|deloused|disinfected|moved to farrowing house one week before farrowing date|(fresh) water supply|maintain good hygiene',
              [3] * 3, 'Dry sow house: any three, 3 x 3m.')], houses, node='3-4')
    add('q9cii', 'Q9(c)(ii)', '4-3-2', 'fattener-house', 'Describe the management of pigs in the fattener house.',
        [menu('grouped by size|fattener ration|fed ad lib|15% protein|lysine|temp. 22°C|restrict feeding in final two weeks|disease control|good hygiene|target weight at slaughter of 80 – 82 kg|slaughter before 6 months',
              [3] * 3, 'Fattener house: any three, 3 x 3m.')], houses, node='3-4')
    terms = 'Explain the following terms in relation to pig production:'
    for key, ref, concept, term, answer, note in [
            ('q9di', 'Q9(d)(i)', 'food-conversion-ratio', 'Food conversion ratio (FCR)', 'FCR: Amount of feed needed or eaten to produce (1 kg) LWG', None),
            ('q9dii', 'Q9(d)(ii)', 'gilt', 'Gilt', 'Gilt : (Young) female pig that has not yet farrowed', None),
            ('q9diii', 'Q9(d)(iii)', 'farrowing-crate', 'Farrowing crate', 'Farrowing crate: Holds sow during farrowing/ prevents sow lying on bonhams/ allows easy suckling', None),
            ('q9div', 'Q9(d)(iv)', 'delousing', 'Delousing', 'Delousing: Treatment to prevent lice infection', '[Accept to prevent (external) parasites]')]:
        add(key, ref, '4-3-2', concept, f'Explain the term in relation to pig production: {term}.', [point(answer, 5, note)], terms, node='3-4')
    # Question 10 ------------------------------------------------------------
    breeds = 'British breeds and continental breeds are commonly used in beef production in Ireland.'
    add('q10ai', 'Q10(a)(i)', '4-2', 'british-and-continental-breeds', 'Give one example of each type of breed.',
        [menu('Hereford|Aberdeen Angus', [4], 'British: any one, 4m.'), menu('Charolais|Limousin|Simmental|Belgian Blue', [4], 'Continental: any one, 4m.')], breeds, node='3-1')
    add('q10aii', 'Q10(a)(ii)', '4-3-1', 'breed-type-pros-and-cons', 'Explain one advantage and one disadvantage of each type of breed.',
        [menu('Smaller|hardier|ease of calving|beef suited to Irish market|less feeding', [3], 'British advantage: any one, 3m.'),
         menu('Early maturing|slow growth rates|fatter (carcasses)', [3], 'British disadvantage: any one, 3m.'),
         menu('Leaner|heavier|faster growth|late maturing|suited to export|better conformation', [3], 'Continental advantage: any one, 3m.'),
         menu('Less hardy|difficult calving|too heavy|high feeding level', [3], 'Continental disadvantage: any one, 3m.')], breeds, node='3-3')
    weights = 'Two-year calf-to-beef is a common beef production system. Give the target weights for beef cattle in this system at the following stages:'
    for key, ref, concept, stage, answer in [
            ('q10bi', 'Q10(b)(i)', 'first-winter-weight', 'Start of first winter housing', '(i) Start of first winter: 200 - 230 kg'),
            ('q10bii', 'Q10(b)(ii)', 'second-winter-weight', 'Start of second winter housing', '(ii) Start of second winter housing: 470 - 490 kg'),
            ('q10biii', 'Q10(b)(iii)', 'slaughter-weight', 'Slaughter', '(iii) Slaughter: 550-750 kg')]:
        add(key, ref, '4-3-1', concept, f'Give the target weight for beef cattle in the two-year calf-to-beef system at: {stage}.', [point(answer, 4)], weights, node='3-3')
    add('q10c', 'Q10(c)', '4-3-2', 'weanling-housing', 'Describe the housing of weanlings during their first winter.',
        [menu('Housed in October-November|slats or straw bedding or cubicles|adequate floor space|good ventilation|no draughts|dry|warm|(fresh) water supply|adequate trough space|good hygiene or cleanliness|sufficient slurry holding capacity|ease of access|dosing|treatment for lice|silage or hay|concentrates or meals',
              [4] * 4, 'Any four, 4 x 4m.')], node='3-4')
    add('q10d', 'Q10(d)', '4-3-1', 'store-period-compensatory-growth', 'Store period and compensatory growth are important terms in beef production. Explain each term.',
        [menu('Moderate feeding level in winter|frame grows|little extra muscle produced|decrease in rate of weight gain|target LWG of 0.2 – 0.5 kg', [3, 3], 'Store period: any two, 2 x 3m.'),
         menu('Higher level of growth|during following summer at grass|after Period of restricted feeding during winter|higher LWG than that of animal fed well over winter|average LWG of 0.8-1.2 kg', [3, 3],
              'Compensatory growth: any two, 2 x 3m. [Award 6m in each case if a graph is drawn, and where the terms “store period” and “compensatory growth” are labelled , and where the axes are labelled]')],
        node='3-3')
    # Question 11 ------------------------------------------------------------
    worms = 'Earthworms belong to the phylum Annelida and play a very important role in the soil.'
    add('q11ai', 'Q11(a)(i)', '4-2', 'annelida-features', 'Give two characteristic features of the phylum Annelida.',
        [menu('Segmented body|triploblastic|coelomate|setae|bilateral symmetr|nephridia|hermaphrodite', [2, 2], 'Any two, 2 x 2m. [Accept clitellum]')], worms, node='3-1')
    add('q11aii', 'Q11(a)(ii)', '2-2-3', 'earthworm-benefits', 'Describe any three benefits earthworms bring to the soil.',
        [menu('Improve drainage|improve aeration|mix soil (layers)|decompose organic matter|create humus|deepen topsoil|excretory products add nutrients to soil|dead earthworms improve organic matter content of soil|improve soil structure',
              [3] * 3, 'Any three, 3 x 3m.')], worms, node='1-4')
    add('q11aiii', 'Q11(a)(iii)', '2-2-3', 'earthworm-population', 'Describe an investigation to estimate the earthworm population in a pasture.',
        [menu('Mark out area|quadrat|random|how random|remove vegetation|apply potassium permanganate solution or washing up liquid solution|wait for suitable time|count earthworms inside quadrat|multiply no. earthworms by 10,000|repeat|calculate average number of earthworms',
              [3] * 5, 'Any five, 5 x 3m.')], worms, node='1-4|0-1')
    add('q11bi', 'Q11(b)(i)', '2-1', 'soil-formation-factors', 'Describe any three factors involved in soil formation.',
        [menu('Parent material|climate|living organisms|topography or slope|time', [3] * 3, 'Any three, 3 x 3m. [Accept (description of) named example in each case above]')], node='1-0')
    add('q11bii', 'Q11(b)(ii)', '2-1', 'podzol-features', 'Describe two features of a podzol soil.',
        [menu('Deep O horizon|pale or leached (A2) horizon or layer|rusty coloured or dark (B2) horizon or layer|iron pan|poor drainage or wet|acid parent material|peat on top|high rainfall', [4, 4],
              'Any two, 2 x 4m. [Award 8m if diagram drawn with any two of the above included as labels]')], node='1-0')
    lime = 'Regular liming of soil is a very important practice. Explain the importance of liming in relation to the following:'
    add('q11ci', 'Q11(c)(i)', '2-2-1', 'liming-and-ph', 'Explain the importance of liming in relation to soil pH.', [menu('Raises soil pH|reduces soil acidity', [3], 'Any one, 3m.')], lime, node='1-2')
    add('q11cii', 'Q11(c)(ii)', '2-2-1', 'liming-and-flocculation', 'Explain the importance of liming in relation to flocculation.',
        [menu('Causes soil particles to clump together|improves structure|improves aeration|improves drainage|provides calcium ions (or Ca2+)', [2, 2], 'Any two, 2 x 2m.')], lime, node='1-2|1-3')
    add('q11d', 'Q11(d)', '2-3', 'fym-benefits', 'Describe two benefits of adding farm yard manure (FYM) to the soil.',
        [menu('Increases organic matter content|increases humus content|provides soil nutrients or named soil nutrient or increases soil fertility|increases earthworm population in soil|improves soil structure|improves soil aeration|cheap (source of organic matter)|handy way of disposal',
              [4, 4], 'Any two, 2 x 4m.')], node='1-6|1-4')
    # Question 12 ------------------------------------------------------------
    progeny = 'Progeny testing of bulls is a common practice in dairying and beef production systems in Ireland.'
    add('q12ai', 'Q12(a)(i)', '4-3-1', 'progeny-testing', 'Explain the term progeny testing.',
        [menu('Recording of the characteristics or named characteristic of the offspring of a bull|comparing performance to other bulls|kept in same conditions', [3, 3], 'Any two, 2 x 3m.')], progeny, node='3-6')
    add('q12aii', 'Q12(a)(ii)', '4-3-1', 'progeny-test-usefulness', 'Comment on the usefulness of progeny test information to the modern animal-production farmer.',
        [menu('Increased performance|increased growth rates|increased milk yields|increased prolificy in pigs or sheep|select best breeding stock|other EBI related factors e.g. health', [3, 3], 'Any two, 2 x 3m.')],
        progeny, node='3-6')
    cell = 'The diagram shows the main parts of a plant cell. The cell membrane is already labelled.'
    figured(add('q12bi', 'Q12(b)(i)', '3-1', 'plant-cell-parts', 'Identify parts A, B, C, D and E.',
                [menu(['A Cytoplasm', 'B Nucleus', 'C Chloroplast', 'D Vacuole', 'E Cell Wall'], [2] * 5, 'All five, 5 x 2m.')], cell, node='2-0'), 'q12bi')
    figured(add('q12bii', 'Q12(b)(ii)', '4-1', 'chromosome-location', 'In which part are the chromosomes found?', [point('Nucleus / B', 3)], cell, node='3-6'), 'q12bii')
    figured(add('q12biii', 'Q12(b)(iii)', '4-1', 'chromosome-function', 'What is the function of chromosomes?', [point('Contain the genes/ contains hereditary information', 3)], cell, node='3-6'), 'q12biii')
    maize = ('In maize the allele for green plants (G) is dominant over the allele for albino plants (g). A maize plant homozygous for green colour (GG) was crossed with a maize plant homozygous for albino colour (gg). '
             'The F1 individuals were heterozygous. Copy the following into your answer book and complete the spaces (genotypes in brackets, phenotypes on lines). Genotypes of original parents (GG) × (gg).')
    add('q12ci', 'Q12(c)(i)', '4-1', 'maize-gametes', 'Complete: (i) Possible gametes ( ) × ( )', [point('(i) Gametes: (G) (g)', 8, '2 x 4m.')], maize, node='3-6')
    add('q12cii', 'Q12(c)(ii)', '4-1', 'maize-f1-genotype', 'Complete: (ii) F1 genotype ( )', [point('(ii) Genotype F1: (Gg)', 4)], maize, node='3-6')
    add('q12ciii', 'Q12(c)(iii)', '4-1', 'maize-f1-phenotype', 'Complete: (iii) F1 phenotype ___', [point('(iii) Phenotype F1: Green', 4)], maize, node='3-6')
    add('q12d', 'Q12(d)', '4-1', 'maize-test-cross',
        'In your answer book show a cross between an albino plant and an F1 plant from the above cross. In your cross show: (i) Genotypes of parents ( ) × ( ) (ii) Possible gametes ( ) × ( ) ( ) '
        '(iii) Genotypes of offspring ( ) ( ) (iv) Phenotypes of offspring ___ ___',
        [point('(i) Genotypes: (gg) x (Gg)', 4, '2 x 2m.'), point('(ii) Gametes: (g) x (G) (g)', 6, '3 x 2m.'),
         point('(iii) Genotype of offspring: (Gg) (gg)', 4, '2 x 2m.'), point('(iv) Phenotypes of offspring: Green Albino', 2, '2 x 1m.')],
        'In maize the allele for green plants (G) is dominant over the allele for albino plants (g). A maize plant homozygous for green colour (GG) was crossed with a maize plant homozygous for albino colour (gg). The F1 individuals were heterozygous.',
        node='3-6')
    # Question 13 ------------------------------------------------------------
    two = 'Answer any two of the parts (a), (b), (c), (d).'
    add('q13ai', 'Q13(a)(i)', '3-2', 'irish-conifers', 'Name two species of coniferous trees grown in Irish forests.',
        [menu('(Sitka) spruce|(Lodgepole) pine|(Japanese) larch|fir', [4, 4], 'Any two, 2 x 4m.')], two, node='2-1')
    add('q13aii', 'Q13(a)(ii)', '3-3-1', 'tree-planting', 'Describe the main features of tree planting in a commercial forest.',
        [menu('Select healthy plants|fence off land|drain land|create mounds|2m x 2m spacing|each tree has 4 m²|2500 trees per ha.', [3, 3], 'Any two, 2 x 3m.')], two, node='2-3')
    add('q13aiii', 'Q13(a)(iii)', '3-3-2', 'forest-weed-control', 'Explain why weeds must be controlled around trees and how this is carried out.',
        [menu('Reduces competition|improves growth of trees|weeds smother young trees', [4], 'Why? Any one, 4m.'), menu('Spraying|herbicides|cutting|trampling', [4], 'How? Any one, 4m.')], two, node='2-4')
    add('q13aiv', 'Q13(a)(iv)', '3-3-2', 'forest-thinning', 'Give the reasons why trees are thinned in commercial forests.',
        [menu('Removes poorer trees|increased space|less competition|remaining trees grow better|useful products from thinnings or source of income|improves access|thinnings can be used to create “roadway”', [4, 4],
              'Any two, 2 x 4m.')], two, node='2-4')
    figured(add('q13bi', 'Q13(b)(i)', '3-2', 'grass-species-photographs',
                'Identify the four species of grass shown in the photographs (A, B, C, D) from the following list: Cocksfoot; Italian ryegrass; Meadow foxtail; Perennial ryegrass.',
                [menu(['A: Perennial ryegrass', 'B: Meadow foxtail', 'C: Italian ryegrass', 'D: Cocksfoot'], [4] * 4, 'All four, 4 x 4m.')], two, node='2-1|2-6'), 'q13bi')
    add('q13bii', 'Q13(b)(ii)', '3-3-1', 'grazing-seed-species', 'List any two species that are commonly used in grass seed mixtures for grazing pastures.',
        [menu('Perennial ryegrass or PRG|Italian ryegrass or IRG|(red or white) clover', [3, 3], 'Any two, 2 x 3m.')], two, node='2-6')
    species = [('prg', 'PRG', 'Persistent|high productivity or high yield|palatable|tillers vigorously|digestible|aggressive'),
               ('irg', 'IRG', 'High productivity or high yield|palatable|digestible|large amounts of herbage|long growing season|early bite for cows'),
               ('clover', 'Clover', 'Palatable|digestible|fixes nitrogen|protein source|good ground cover|rich in minerals')]
    rows, variants = routes([(slug, label, [menu(points, [4, 4], f'{label}: any two features, 2 x 4m.')]) for slug, label, points in species])
    add('q13biii', 'Q13(b)(iii)', '3-3-1', 'grazing-species-features', 'Choose one of the species referred to in part (ii) and give two features that make it suitable for grazing.', rows,
        two + ' (ii) List any two species that are commonly used in grass seed mixtures for grazing pastures.',
        selection=closed(1, [label for _, label, _ in species]), node='2-6', extra={'answerVariants': variants})
    add('q13ci', 'Q13(c)(i)', '4-3-2', 'flushing-and-sponging', 'Flushing and sponging of ewes are common practices in sheep production. Explain the terms flushing and sponging as used here.',
        [menu('Ewes on bare pasture|high stocking rate|placed on very good pasture 3-4 weeks before mating|kept on good pasture for 3 weeks after mating|reduced stocking rate|increased number of eggs released|more twins|higher conception rates|more regular heat periods|fewer barren ewes|safer implantation of embryo(s)',
              [3] * 3, 'Flushing: any three, 3 x 3m.'),
         menu('Sponge containing hormone or named hormone|ewe’s vagina|removed after 12-14 days|PMSG injection|ewes come into heat at same time|compact lambing|early lamb production|easier management on mixed farm|reduced labour costs|reduced ram:ewe ratio or 1 ram:10 ewes',
              [3] * 3, 'Sponging: any three, 3 x 3m.')], two, node='3-4')
    maggots = two + ' Maggots are a common parasite of sheep.'
    add('q13cii', 'Q13(c)(ii)', '4-3-3', 'maggot-insect', 'Maggots are the larvae of which insect?', [point('Blow fly or green bottle or blue bottle', 3)], maggots, node='3-5')
    add('q13ciii', 'Q13(c)(iii)', '4-3-3', 'maggot-control', 'Describe three common methods of maggot prevention or control in sheep management.',
        [menu('Dipping|pour-on|spray (insecticides)|tail docking|dagging or clipping wool|shearing|dosing (to prevent diarrhoea)', [3] * 3, 'Any three, 3 x 3m.')], maggots, node='3-5')
    add('q13di', 'Q13(d)(i)', '4-1', 'breathing-system-diagram', 'Draw a diagram of the breathing system of a mammal. Label any three parts.',
        [point('Diagram', None, 'Diagram 6m, 3m, 0m. [Award full marks if diagram shows trachea, bronchus, lung and bronchiole.] [Award three marks for diagram if any one of the above structures is not shown]', kind='criterion'),
         point('Any three labels', None, 'Labels: any three, 3 x 3m. The scheme does not list the labels.', kind='criterion')],
        two, marks=15, tariff={'kind': 'questionTotal', 'notation': '6m, 3m, 0m + 3 x 3m'}, node='3-0')
    add('q13dii', 'Q13(d)(ii)', '4-3-3', 'preventing-viral-pneumonia', 'Viral pneumonia is a common illness during calf housing. How can viral pneumonia be prevented?',
        [menu('Good ventilation|vaccination|house only when dry|isolate bought-in stock|good hygiene|avoid stress|colostrum|avoid draughts', [3], 'Any one, 3m.')], two, node='3-5')
    add('q13diii', 'Q13(d)(iii)', '4-3-3', 'lungworm-life-cycle', 'Describe briefly the life cycle of lungworms.',
        [menu('Adult worm in lungs|eggs coughed up|swallowed|pass out with dung|larvae on grass|picked up by grazing animals|larvae burrow through intestine|enter lungs|larvae mature in lungs', [3] * 3,
              'Any three, 3 x 3m.')], two, node='3-5')
    add('q13div', 'Q13(d)(iv)', '4-3-3', 'lungworm-control', 'Outline one method of control of lungworms in cattle.', [point('Dosing/ leader- follower system/ vaccination', 3)], two, node='3-5')
    assert len(p.tasks) == 62, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('62 base tasks, one card each. Section One is one task per question with the scheme\'s own row marks. Section Two parts are priced on their own; '
                          'the Q12(d) cross is one task because its marks are tied line to line. Q13(b)(iii) species are answer routes.')
