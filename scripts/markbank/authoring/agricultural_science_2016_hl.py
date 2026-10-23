"""2016 Higher: every task authored from the SEC paper and marking scheme (no cards existed).

All 8 paper pages and 12 scheme pages were inspected and the independent census transcribed
before authoring: 62 base tasks, one card each. Under the scheme's convention (PDF page 4) a
scale such as 6 + 3 + 1 pays the first correct answer 6 and each later one the next value, so a
Question 1 part whose scale spans its (i) and (ii) is one task stating the scale (orderedSplit);
a part priced separately at (i) and (ii) is two tasks. The Q3 Option One (b) lowland and hill
comparison is priced once across its four headings, so it is one task with the scale stated.
The Q8(c) choice of three pairs from four is one card whose eight members are parts. Answers
are the scheme's words.
"""
from agricultural_science_legacy import Paper, P, point, menu, closed

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers': '0d0d58001042c543419ee3edc4acb58c9179f901acee5f8573ae9ae4949b12cd',
          'markingschemes': '38b7cf5f6e4504c17f6dd8b6f70dbad197a3c4fe7079e848221750f51eb34502'}
SELECTIONS = {
    'b3044c5c9df9cf82': ('exam-selection', 'Six of nine independent examination questions; every question is retained.'),
    '9644cd1a62d82c59': ('independent-task-selection', 'Q1: six of ten separately priced lettered parts; all ten are retained.'),
    '49c25de9562952d7': ('open', 'Q2(b): any four factors with their effects; the scheme lists eight (a marking menu).'),
    'b2f3bbb6393a5602': ('independent-task-selection', 'Q4: two of four independently priced 24-mark methods; all four are retained.'),
    '0812381668948852': ('open', 'Q5(b): any four factors other than breed; the scheme lists six (a marking menu).'),
    'f041fb5aa02f9e66': ('open', 'Q7(c)(i): any two EBI sub-indices with their factors; the scheme lists seven (a marking menu).'),
    'c47ef3d01563b6f7': ('independent-task-selection', 'Q8: two of three independently priced 24-mark parts; all three are retained.'),
    'b773c9f67647789e': ('closed', 'Q8(c): any three of four printed pairs of terms. One card lists the eight members as parts and counts the best six (three pairs).'),
    '75c1b37a9a05f77d': ('independent-task-selection', 'Q9: four of five independently priced 12-mark explanations; all five are retained.'),
}
SUPPLEMENTARY = [
    (4, 'Option Two', 'closed', 'Both Q3 options are retained at their own task addresses.'),
]
ATLAS = {
    'Q1(a)': 'classification-of-animals-plants|grassland', 'Q1(b)': 'fertilisers-pollution-environment-cycles',
    'Q1(c)': 'classification-of-animals-plants', 'Q1(d)': 'animal-diseases', 'Q1(e)': 'crop-production',
    'Q1(f)': 'animal-physiology-digestive-system|animal-physiology-reproductive-systems', 'Q1(g)': 'soil-science',
    'Q1(h)': 'energy-crop-catch-crop|crop-production', 'Q1(i)': 'plant-physiology', 'Q1(j)': 'pigs|animal-diseases',
    'Q2': 'soil-science', 'Q2(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q3 Option One': 'sheep', 'Q3 Option One (c)': 'grassland',
    'Q3 Option Two': 'beef-cattle', 'Q3 Option Two (b)': 'beef-cattle|grassland', 'Q3 Option Two (c)(iii)': 'beef-cattle|genetics',
    'Q4': 'scientific-practices-experiments-investigations',
    'Q4(a)': 'scientific-practices-experiments-investigations|plant-physiology', 'Q4(b)': 'scientific-practices-experiments-investigations|crop-production',
    'Q4(c)': 'scientific-practices-experiments-investigations|animal-physiology-digestive-system', 'Q4(d)': 'scientific-practices-experiments-investigations|grassland',
    'Q5': 'dairy-cattle', 'Q5(c)': 'dairy-cattle|animal-physiology-reproductive-systems',
    'Q6': 'crop-production', 'Q6(b)': 'crop-production|soil-science',
    'Q7': 'genetics', 'Q7(c)': 'genetics|dairy-cattle',
    'Q8(a)': 'crop-production|classification-of-animals-plants', 'Q8(b)': 'fertilisers-pollution-environment-cycles|crop-production',
    'Q8(c)': 'genetics|plant-physiology|animal-diseases|fertilisers-pollution-environment-cycles',
    'Q9(a)': 'animal-diseases|beef-cattle', 'Q9(b)': 'plant-physiology', 'Q9(c)': 'pigs', 'Q9(d)': 'grassland', 'Q9(e)': 'plant-physiology|crop-production',
}
REGIONS = {
    # Drafted by regions.py.
    'Q1(a)': (P((2, 0.047, 0.129)), P((5, 0.082, 0.186))),
    'Q1(b)(i)': (P((2, 0.047, 0.080), (2, 0.129, 0.150)), P((5, 0.082, 0.119), (5, 0.186, 0.230))),
    'Q1(b)(ii)': (P((2, 0.047, 0.080), (2, 0.150, 0.178)), P((5, 0.082, 0.119), (5, 0.230, 0.291))),
    'Q1(c)': (P((2, 0.047, 0.080), (2, 0.178, 0.211)), P((5, 0.082, 0.119), (5, 0.291, 0.322))),
    'Q1(d)(i)': (P((2, 0.047, 0.080), (2, 0.211, 0.231)), P((5, 0.082, 0.119), (5, 0.322, 0.352))),
    'Q1(d)(ii)': (P((2, 0.047, 0.080), (2, 0.231, 0.260)), P((5, 0.082, 0.119), (5, 0.352, 0.398))),
    'Q1(e)': (P((2, 0.047, 0.080), (2, 0.260, 0.309)), P((5, 0.082, 0.119), (5, 0.398, 0.428))),
    'Q1(f)': (P((2, 0.047, 0.080), (2, 0.309, 0.391)), P((5, 0.082, 0.119), (5, 0.428, 0.489))),
    'Q1(g)': (P((2, 0.047, 0.080), (2, 0.391, 0.440)), P((5, 0.082, 0.119), (5, 0.489, 0.564))),
    'Q1(h)(i)': (P((2, 0.047, 0.080), (2, 0.440, 0.461)), P((5, 0.082, 0.119), (5, 0.564, 0.580))),
    'Q1(h)(ii)': (P((2, 0.047, 0.080), (2, 0.461, 0.489)), P((5, 0.082, 0.119), (5, 0.580, 0.640))),
    'Q1(i)': (P((2, 0.047, 0.080), (2, 0.489, 0.522)), P((5, 0.082, 0.119), (5, 0.640, 0.671))),
    'Q1(j)': (P((2, 0.047, 0.080), (2, 0.522, 0.628)), P((5, 0.082, 0.119), (5, 0.671, 0.809))),
    'Q2(a)': (P((3, 0.047, 0.129)), P((6, 0.082, 0.197))),
    'Q2(b)': (P((3, 0.129, 0.162)), P((6, 0.082, 0.115), (6, 0.197, 0.303))),
    'Q2(c)(i)': (P((3, 0.162, 0.281)), P((6, 0.082, 0.115), (6, 0.303, 0.333))),
    'Q2(c)(ii)': (P((3, 0.162, 0.260), (3, 0.281, 0.297)), P((6, 0.082, 0.115), (6, 0.333, 0.347))),
    'Q2(c)(iii)': (P((3, 0.162, 0.260), (3, 0.297, 0.407)), P((6, 0.082, 0.115), (6, 0.347, 0.492))),
    'Q3 Option One (a)': (P((3, 0.407, 0.489)), P((6, 0.492, 0.591))),
    'Q3 Option One (b)': (P((3, 0.407, 0.440), (3, 0.489, 0.604)), P((6, 0.492, 0.524), (6, 0.591, 0.742))),
    'Q3 Option One (c)': (P((3, 0.407, 0.440), (3, 0.604, 0.735)), P((6, 0.492, 0.524), (6, 0.742, 0.835))),
    'Q3 Option Two (a)': (P((4, 0.047, 0.129)), P((7, 0.082, 0.182))),
    'Q3 Option Two (b)': (P((4, 0.047, 0.080), (4, 0.129, 0.178)), P((7, 0.082, 0.115), (7, 0.182, 0.243))),
    'Q3 Option Two (c)(i)': (P((4, 0.047, 0.080), (4, 0.178, 0.215)), P((7, 0.082, 0.115), (7, 0.243, 0.271))),
    'Q3 Option Two (c)(ii)': (P((4, 0.047, 0.080), (4, 0.178, 0.199), (4, 0.215, 0.247)), P((7, 0.082, 0.115), (7, 0.271, 0.301))),
    'Q3 Option Two (c)(iii)': (P((4, 0.047, 0.080), (4, 0.178, 0.199), (4, 0.247, 0.358)), P((7, 0.082, 0.115), (7, 0.301, 0.431))),
    'Q4(a)': (P((4, 0.358, 0.423)), P((7, 0.431, 0.545))),
    'Q4(b)': (P((4, 0.358, 0.391), (4, 0.423, 0.457)), P((7, 0.431, 0.464), (7, 0.545, 0.621))),
    'Q4(c)': (P((4, 0.358, 0.391), (4, 0.457, 0.489)), P((7, 0.431, 0.464), (7, 0.621, 0.697))),
    'Q4(d)': (P((4, 0.358, 0.391), (4, 0.489, 0.588)), P((7, 0.431, 0.464), (7, 0.697, 0.745))),
    'Q5(a)(i)': (P((4, 0.588, 0.742)), P((8, 0.082, 0.166))),
    'Q5(a)(ii)': (P((4, 0.588, 0.721), (4, 0.742, 0.759)), P((8, 0.082, 0.115), (8, 0.166, 0.211))),
    'Q5(a)(iii)': (P((4, 0.588, 0.721), (4, 0.759, 0.787)), P((8, 0.082, 0.115), (8, 0.211, 0.257))),
    'Q5(b)': (P((4, 0.787, 0.836)), P((8, 0.082, 0.115), (8, 0.257, 0.348))),
    'Q5(c)': (P((4, 0.836, 0.893)), P((8, 0.082, 0.115), (8, 0.348, 0.531))),
    'Q6(a)(i)': (P((5, 0.047, 0.084)), P((8, 0.531, 0.600))),
    'Q6(a)(ii)': (P((5, 0.047, 0.067), (5, 0.084, 0.112)), P((8, 0.531, 0.564), (8, 0.600, 0.706))),
    'Q6(b)': (P((5, 0.112, 0.145)), P((8, 0.531, 0.564), (8, 0.706, 0.766))),
    'Q6(c)(i)': (P((5, 0.145, 0.166)), P((8, 0.531, 0.564), (8, 0.766, 0.811))),
    'Q6(c)(ii)': (P((5, 0.166, 0.227)), P((8, 0.531, 0.564), (8, 0.811, 0.874))),
    'Q7(a)(i)': (P((5, 0.227, 0.264)), P((9, 0.082, 0.162))),
    'Q7(a)(ii)': (P((5, 0.227, 0.248), (5, 0.264, 0.281)), P((9, 0.082, 0.115), (9, 0.162, 0.207))),
    'Q7(a)(iii)': (P((5, 0.227, 0.248), (5, 0.281, 0.297)), P((9, 0.082, 0.115), (9, 0.207, 0.252))),
    'Q7(a)(iv)': (P((5, 0.227, 0.248), (5, 0.297, 0.325)), P((9, 0.082, 0.115), (9, 0.252, 0.302))),
    'Q7(b)(i)': (P((5, 0.325, 0.395)), P((9, 0.082, 0.115), (9, 0.302, 0.317))),
    'Q7(b)(ii)': (P((5, 0.325, 0.379), (5, 0.395, 0.412)), P((9, 0.082, 0.115), (9, 0.317, 0.332))),
    'Q7(b)(iii)': (P((5, 0.325, 0.379), (5, 0.412, 0.428)), P((9, 0.082, 0.115), (9, 0.332, 0.347))),
    'Q7(b)(iv)': (P((5, 0.325, 0.379), (5, 0.428, 0.461)), P((9, 0.082, 0.115), (9, 0.347, 0.377))),
    'Q7(b)(v)': (P((5, 0.325, 0.379), (5, 0.461, 0.489)), P((9, 0.082, 0.115), (9, 0.377, 0.423))),
    'Q7(c)': (P((5, 0.489, 0.578)), P((9, 0.082, 0.115), (9, 0.423, 0.531))),
    'Q8(a)(i)': (P((6, 0.047, 0.148)), P((10, 0.082, 0.150))),
    'Q8(a)(ii)': (P((6, 0.047, 0.101), (6, 0.148, 0.166)), P((10, 0.082, 0.115), (10, 0.150, 0.180))),
    'Q8(a)(iii)': (P((6, 0.047, 0.101), (6, 0.166, 0.182)), P((10, 0.082, 0.115), (10, 0.180, 0.196))),
    'Q8(a)(iv)': (P((6, 0.047, 0.101), (6, 0.182, 0.199)), P((10, 0.082, 0.115), (10, 0.196, 0.226))),
    'Q8(a)(v)': (P((6, 0.047, 0.101), (6, 0.199, 0.227)), P((10, 0.082, 0.115), (10, 0.226, 0.272))),
    'Q8(b)': (P((6, 0.047, 0.080), (6, 0.227, 0.293)), P((10, 0.082, 0.115), (10, 0.272, 0.408))),
    'Q8(c)': (P((6, 0.047, 0.080), (6, 0.293, 0.473)), P((10, 0.082, 0.115), (10, 0.408, 0.741))),
    'Q9(a)': (P((6, 0.473, 0.555)), P((11, 0.082, 0.163))),
    'Q9(b)': (P((6, 0.473, 0.505), (6, 0.555, 0.587)), P((11, 0.082, 0.115), (11, 0.163, 0.210))),
    'Q9(c)': (P((6, 0.473, 0.505), (6, 0.587, 0.621)), P((11, 0.082, 0.115), (11, 0.210, 0.256))),
    'Q9(d)': (P((6, 0.473, 0.505), (6, 0.621, 0.653)), P((11, 0.082, 0.115), (11, 0.256, 0.318))),
    'Q9(e)': (P((6, 0.473, 0.505), (6, 0.653, 0.713)), P((11, 0.082, 0.115), (11, 0.318, 0.367))),
}
FIRST = 'The scheme\'s convention: the first correct answer encountered earns the first value and each later correct answer the next ({}).'


def split(text, note=None):
    """A row of an orderedSplit card: the scheme prices the scale, not the row."""
    return point(text, None, note)


def build():
    p = Paper(2016, 'higher', FILE, HASHES, REGIONS, ATLAS, 8, 12, SELECTIONS, SUPPLEMENTARY,
              section=lambda ref: 'A' if ref.startswith('Q1(') else 'B')
    add = p.add
    six = 'Answer any six of the parts (a) to (j).'
    # Question 1 -------------------------------------------------------------
    add('q1a', 'Q1(a)', '3-2', 'clover-phylum-features',
        '(i) Clover is a member of which plant phylum? (ii) Mention three features of plants belonging to this phylum.',
        [split('(i) Phylum — Spermatophyta or Angiospermae or Leguminosae or Papilionaceae or Fabaceae',
               FIRST.format('(2 × 4m) + (2 × 1m)') + ' Four answers: the phylum and three features.'),
         split('(ii) Features — Flowering plants/ reproduce by seeds/ seeds in a fruit/ roots or stems or leaves/ gametophyte dominant over sporophyte/ nitrogen-fixing/ seed pods/ root nodules/ flower parts in 5s/ high in protein',
               'Any three.')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '(2 × 4m) + (2 × 1m)'})
    add('q1bi', 'Q1(b)(i)', '2-3', 'biological-oxygen-demand', 'Explain the term biological oxygen demand (BOD).',
        [point('The amount of dissolved oxygen needed to break down organic matter in (a litre) water sample or the amount of dissolved oxygen used by (a litre) sample of water at 20° C in darkness for five days', 4)],
        six, node='1-6')
    add('q1bii', 'Q1(b)(ii)', '2-3', 'keeping-bod-low', 'Outline three farming practices that would help maintain a low BOD.',
        [menu('Slurry application at correct time or away from waterways or in suitable weather conditions|use of slurry tanks|collect dairy washings|avoid milk spills|silage effluent tanks|correct fertiliser applications|safe disposal of dead animals or FYM or sheep dip or pesticides',
              [3, 2, 1], 'Any three. ' + FIRST.format('3 + 2 + 1'))], six, node='1-6')
    add('q1c', 'Q1(c)', '3-2', 'rhizopus-diagram', 'Draw a labelled diagram of the fungus Rhizopus (bread mould).',
        [point('Diagram', None, 'Diagram: 4, 2, 0. The scheme prints no model drawing.', kind='criterion'),
         point('Spores/ sporangium/ columella/ sporangiophore/ stolon/ rhizoid/ hyphae', None, 'Labels: any three. ' + FIRST.format('3 + 2 + 1'))],
        six, marks=10, tariff={'kind': 'questionTotal', 'notation': '4, 2, 0 + 3 + 2 + 1'})
    add('q1di', 'Q1(d)(i)', '4-3-3', 'notifiable-diseases', 'What are notifiable diseases?',
        [menu('A disease of national importance|must notify authorities|highly contagious|risk to humans|quarantine|animals slaughtered or depopulated', [2, 2],
              'Any two points, 2 + 2.')], six, node='3-5')
    add('q1dii', 'Q1(d)(ii)', '4-3-3', 'notifiable-disease-examples', 'Give three examples of such diseases.',
        [menu('Scrapie|Aujeszky disease|sheep scab|swine fever|rabies|Newcastle disease|anthrax|brucellosis|foot and mouth|BSE|TB|BVD|bluetongue|avian ‘flu|Johne’s disease|contagious bovine pleural pneumonia',
              [3, 2, 1], 'Any three. ' + FIRST.format('3 + 2 + 1'))], six + ' (i) What are notifiable diseases?', node='3-5')
    add('q1e', 'Q1(e)', '3-3-2', 'scutch-grass-control', 'Why is scutch grass (Agropyrens repens) such a difficult weed to eradicate in a cereal crop?',
        [menu('Rhizomes|cultivation spreads it|same family as cereals|spreads from or to headlands|needs specific weed-killers|not controlled by rotation', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six)
    add('q1f', 'Q1(f)', '4-1', 'villi-nephrons-cervix', 'State the location and function of the following structures in mammals: (i) Villi. (ii) Nephrons. (iii) Cervix.',
        [split('(i) Villi — Small intestine or duodenum or ileum (absorption of nutrients)',
               FIRST.format('(4 × 2m) + (2 × 1m)') + ' Six answers: the location of each structure and its function (in brackets).'),
         split('(ii) Nephrons — Kidney (produce urine/ filter blood/ absorb/ reabsorb/ osmoregulation)'),
         split('(iii) Cervix — Neck of uterus or top of vagina (seals womb/ dilates or role at birth/ allows sperm into uterus/ allows fluids to exit uterus)')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '(4 × 2m) + (2 × 1m)'})
    add('q1g', 'Q1(g)', '2-2-1', 'humus-versus-clay', 'Give three reasons why a high humus content is more beneficial than a high clay content, in a soil.',
        [menu('Humus more fertile (clay less fertile)|holds more water (clay holds less water)|higher CEC (clay has lower CEC)|higher soil temperature (clay lower soil temperature)|increases earthworm activity (no effect on earthworms)|more beneficial for soil structure or more negative charges (less beneficial or fewer negative charges)',
              [6, 3, 1], 'Any three. ' + FIRST.format('6 + 3 + 1'))], six, node='1-2|1-3')
    add('q1hi', 'Q1(h)(i)', '3-3-2', 'catch-crops', 'What are catch crops?', [point('A crop grown between two main crops', 4)], six)
    add('q1hii', 'Q1(h)(ii)', '3-3-2', 'catch-crop-advantages', 'Give three advantages of their use on a mixed farm.',
        [menu('Provides fodder|good crop rotation|break between grass and cereals|prevents nitrogen leaching|early bite in spring|prevents soil erosion or makes use of idle land|high protein content|high yield|fast growing|can be grazed in situ or strip grazed (outwintering)|utilisation of nutrients',
              [3, 2, 1], 'Any three. ' + FIRST.format('3 + 2 + 1'))], six + ' (i) What are catch crops?')
    add('q1i', 'Q1(i)', '3-1', 'respiration-in-germination', 'Explain why respiration is important in the germination of seeds.',
        [menu('Oxygen needed or aerobic respiration|food reserves made soluble or useable|provide energy for digestion|named digestive product|energy for growth', [6, 3, 1],
              'Any three. ' + FIRST.format('6 + 3 + 1'))], six)
    add('q1j', 'Q1(j)', '4-3-3', 'pig-bacterial-diseases', '(i) Name two bacterial diseases of pigs. (ii) Give one symptom of each disease.',
        [split('(i) Bacterial diseases — E. coli scour/ Erysipelas/ leptospirosis/ atrophic rhinitis/ farrowing fever/ mastitis/ navel ill',
               FIRST.format('(2 × 4m) + (2 × 1m)') + ' Four answers: two diseases and one symptom of each. Any two diseases.'),
         split('(ii) Symptom — E. coli: dehydration/ diarrhoea/ weight loss/ loss of condition', 'One symptom for each of your two diseases.'),
         split('(ii) Symptom — Erysipelas: fever/ abortion/ mummification/ red lumps on skin'),
         split('(ii) Symptom — Leptospirosis: low conception rate/ abortion/ stillborn'),
         split('(ii) Symptom — Atrophic rhinitis: sneezing and sniffling/ distorted snout/ low growth rate'),
         split('(ii) Symptom — Farrowing fever: fever/ lack of milk'),
         split('(ii) Symptom — Mastitis: swollen or red udder/ fever/ clotted or reduced milk'),
         split('(ii) Symptom — Navel ill: swollen navel/ stiffness/ fever')],
        six, marks=10, tariff={'kind': 'orderedSplit', 'notation': '(2 × 4m) + (2 × 1m)'}, node='3-5')
    # Question 2 -------------------------------------------------------------
    add('q2a', 'Q2(a)', '2-1', 'podzol-versus-brown-earth', 'Compare a podzol soil with a brown earth soil under the following headings: (i) Drainage. (ii) Fertility. (iii) pH.',
        [split('(i) Drainage — waterlogged or bad (free-draining or good)',
               FIRST.format('(3×4m) + (3×2m)') + ' Podzol (Brown Earth): six answers, the podzol and the brown earth (in brackets) under each heading.'),
         split('(ii) Fertility — leached or poor fertility (fertile)'), split('(iii) pH — acidic (basic or slightly acidic)')],
        marks=18, tariff={'kind': 'orderedSplit', 'notation': '(3×4m) + (3×2m)'})
    add('q2b', 'Q2(b)', '2-2-2', 'soil-structure-factors', 'Identify and explain any four factors that affect the development of a soil structure.',
        [menu('Wetting and drying (breaks up soil or aggregates soil)|freezing and thawing (breaks up soil or aggregates soil)|root activity (small roots bind or large roots crack)|earthworms or soil invertebrates (break up soil or aggregate soil)|tillage (breaks up soil or aggregates soil)|activity of livestock or machinery (compaction)|parent material (limestone for aggregation)|adding lime or organic matter (aggregation)',
              [3] * 4, 'Any four: (4×2m) + (4×1m), each factor 2 and its effect (in brackets) 1. [Cause (and effect) required]')])
    sieve = 'An experiment to determine soil texture by sieving was carried out, and the results were as follows: Sand: 60% Silt: 25% Clay: 15%'
    add('q2ci', 'Q2(c)(i)', '2-2-2', 'soil-texture-by-sieving', 'Describe how this experiment was carried out.',
        [menu('Dry soil sample|crush aggregates|weigh|sieve|with largest mesh on top|weigh amount in each sieve|method of calculation|soil texture triangle', [4] * 3,
              'Any three, 4 marks each (3×4m).')], sieve, node='1-3|0-1')
    add('q2cii', 'Q2(c)(ii)', '2-2-2', 'sandy-loam-enterprise', 'To which type of farm enterprise is this soil best suited?',
        [point('Tillage crops or named tillage crop', 3)], sieve)
    add('q2ciii', 'Q2(c)(iii)', '2-2-2', 'sandy-loam-enterprise-reasons', 'Suggest three reasons for your choice.',
        [menu('Early growth or heats up faster or higher temperature|easily tilled|good drainage|good aeration|not subject to drought|retains nutrients or high in nutrients', [1] * 3,
              'Any three, 1 mark each (3×1m).')], sieve + ' (ii) To which type of farm enterprise is this soil best suited?')
    # Question 3 -------------------------------------------------------------
    add('q3o1a', 'Q3 Option One (a)', '4-3-2', 'lambing-mortality-management', 'Discuss the management practices which contribute to low levels of ewe and lamb mortality at lambing time.',
        [menu('Housing|hygiene specified|avoiding predators|correct feeding programme or steaming up or scanning|supervision or vet|individual pens (bonding)|fostering|prevent chill|colostrum|disease prevention|removing mucus from mouth or nose',
              [6, 6, 4], 'Any three. ' + FIRST.format('6 + 6 + 4'))])
    add('q3o1b', 'Q3 Option One (b)', '4-3-1', 'lowland-versus-hill-sheep',
        'Compare a lowland sheep production system with a hill sheep production system under the following headings: (i) Choice of breed. (ii) Stocking rate. (iii) Management practices. (iv) Lambing percentage.',
        [split('(i) Choice of breed — Named breed/ terminal sires/ crossbred ewes/ meat-producing/ twins (pure-breeding/named breed/single lambs/hardiness)/ poorer mothering ability (better mothering ability)',
               FIRST.format('(4×3m) + (4×1m)') + ' Lowland (Hill): the lowland system and the hill system (in brackets) under each of the four headings.'),
         split('(ii) Stocking rate — 10-15 per ha. or high (2-7 per ha. or low)'),
         split('(iii) Management practices — Housing/ creep feeding/ flushing/ sponging/ grazing system or named, any one (reference to the opposite of each of these points must be stated for hill sheep)',
               '[Breed and mortality not accepted]'),
         split('(iv) Lambing percentage — 120-180% or more twins (70-100% or mostly singles) or correct ratios')],
        marks=16, tariff={'kind': 'orderedSplit', 'notation': '(4×3m) + (4×1m)'})
    add('q3o1c', 'Q3 Option One (c)', '3-3-1', 'grazing-grass-variety-selection', 'Describe the main characteristics to be considered when selecting a grass variety for grazing.',
        [menu('Productivity: yield of grass|Aggressive: competes well|Persistent: keeps growing every year|Digestible: easily digested by the animal or high DMD|Nutritious: provides a well-balanced diet|Palatability: taste or animals are likely to eat it',
              [4] * 4, 'Any four: (4×3m) + (4×1m), each characteristic 3 and its explanation 1.')], node='2-6')
    add('q3o2a', 'Q3 Option Two (a)', '4-3-2', 'housed-weanling-management', 'Describe the management practices necessary to maximise the growth of housed weanlings during their first winter.',
        [menu('Housing time or type|parasite or disease control|1.4 m2 floor space|7 m3 air space|good ventilation|clean water|monitor for illness or poor thrift|group similar size together|feed silage|supplement with meals',
              [6, 6, 4], 'Any three. ' + FIRST.format('6 + 6 + 4'))])
    add('q3o2b', 'Q3 Option Two (b)', '4-3-1', 'beef-grazing-system', 'Describe a suitable grazing system which might be used in a beef enterprise to achieve optimum production.',
        [menu('Rotational grazing system (example strip or paddock)|two points of operation (accept diagram)|leader-follower system|best leafy grass|fewer parasites', [6, 6, 4],
              'Any three. ' + FIRST.format('6 + 6 + 4'))], node='3-3|2-6')
    carcase = 'Beef is classified using the EU beef carcase classification system.'
    add('q3o2ci', 'Q3 Option Two (c)(i)', '4-3-2', 'eu-carcase-classification', 'Outline the main features of this system.',
        [menu('Is a grading system|used in factories|to grade carcases for fat|conformation|1-5 and E-P', [2] * 3, 'Any three, 2 marks each (3×2m).')], carcase)
    add('q3o2cii', 'Q3 Option Two (c)(ii)', '4-3-2', 'carcase-scores',
        'Using this system, indicate a suitable score for a highly productive Continental beef animal and a British crossbred beef animal.',
        [point('Highly productive: E1 or E2 or U1 or U2', 2), point('British crossbred: R4 or R5 or O4 or O5', 2)], carcase)
    add('q3o2ciii', 'Q3 Option Two (c)(iii)', '4-3-2', 'improving-carcase-classification',
        'Describe a suitable strategy which could be used to improve the classification of Irish beef cattle in the future.',
        [menu('Cross breeding|using high quality beef bulls|continental bulls|named breed|slaughter at correct age or at maturity|animal finished on grass', [3, 3],
              'Any two points, 3 marks each (3 + 3m).')], carcase, node='3-4|3-6')
    # Question 4 -------------------------------------------------------------
    lab = 'In the case of any two of the following describe a laboratory or field method:'
    add('q4a', 'Q4(a)', '3-1', 'magnesium-deficiency', 'Describe a laboratory or field method to show the effect of magnesium deficiency on the growth of a plant.',
        [menu('Seeds or seedlings|nutrient tablet (Sach’s) or control or soil containing all nutrients|without Mg or soil deficient in Mg|aerate|tinfoil|correct time|compare growth|(Mg) chlorosis or (Mg) yellowing of leaves|same conditions with one named',
              [4] * 6, 'Any six, 4 marks each (6×4m).')], lab, node='2-0|0-1')
    add('q4b', 'Q4(b)', '3-3-3', 'root-crop-yield', 'Describe a laboratory or field method to estimate the yield of a named root crop.',
        [point('Named crop', 4, '6×4m: the named crop is a compulsory point [*Compulsory point], then any five more.'),
         menu('quadrat 1m2 plot or measured area|place at random|dig crop|wash or remove foliage|weigh|repeat no. of times|average|×10000 for ha. or correct calculation or correct result',
              [4] * 5, 'Any five more, 4 marks each.')], lab, node='2-5|0-1')
    add('q4c', 'Q4(c)', '4-3-2', 'foodstuff-energy-value', 'Describe a laboratory or field method to measure the energy value of an animal foodstuff.',
        [menu('Dry sample of feed|weigh sample|100 g or 100 cm3 or known volume of water in test tube or calorimeter|initial temp.|burn feed under test tube or in calorimeter|reweigh or burn to completion|record new temp.|note temperature change|calculation or ∆H = mc∆t',
              [4] * 6, 'Any six, 4 marks each (6×4m).')], lab, node='3-4|0-1')
    add('q4d', 'Q4(d)', '3-3-2', 'shading-botanical-composition', 'Describe a laboratory or field method to determine the effect of shading on the botanical composition of a pasture.',
        [menu('Quadrat or line transect or belt transect|×10 times or stations|light meter|shaded area|record composition|repeat in unshaded area|record composition|compare|correct conclusion',
              [4] * 6, 'Any six, 4 marks each (6×4m).')], lab, node='2-6|0-1')
    # Question 5 -------------------------------------------------------------
    breeds = 'The average lactation yield and the fat and protein composition of milk for three dairy breeds are shown in the table below:'
    table = 'agsci-2016-hl-paper-milk-table'
    add('q5ai', 'Q5(a)(i)', '4-2', 'dairy-breeds-from-milk', 'Which breeds are represented by A, B, and C?',
        [point('A. Jersey', 2), point('B. Holstein or Holstein cross or Montbéliarde', 2), point('C. Friesian or Friesian cross or Jersey cross or Norwegian Red', 2)], breeds, figure=table)
    add('q5aii', 'Q5(a)(ii)', '4-2', 'dairy-breed-reasons', 'Give a reason for your choice in each case.',
        [point('A: Lower yield/ higher solids', 2), point('B: Higher yield/ lower solids', 2), point('C: Intermediate yield/ intermediate solids', 2)],
        breeds + ' (i) Which breeds are represented by A, B, and C?', figure=table)
    add('q5aiii', 'Q5(a)(iii)', '4-3-2', 'colostrum-fat-protein', 'State the percentage (%) value of fat and protein in colostrum.',
        [point('Fat: 4 - 7%', 2), point('Protein: 14 - 16%', 2)])
    add('q5b', 'Q5(b)', '4-3-2', 'milk-fat-factors', 'List and explain any four of these factors, other than breed.',
        [menu('Age of cow (decreases with age)|stage of lactation (lower during early or higher at end)|stage of milking (increases with milking)|feed (high quality feed or fibre increases)|health (mastitis reduces)|milking interval (lower with long interval)',
              [6] * 4, 'Any four: 4×(5+1m), each factor 5 and its effect (in brackets) 1. [Cause (effect)]')],
        'The fat content of the milk of individual cows can be affected by many factors.')
    add('q5c', 'Q5(c)', '4-3-2', 'heifer-first-calving', 'Discuss how the age and condition of breeding heifers in a dairy herd may influence the date of first calving.',
        [menu('Age: 15 months|280-320 kg at mating|target weight 500-580 kg at calving|24-month calving|Condition: 2.8-3.2 for heat|3.2-3.4 at calving|poor condition causes irregular heat|calving difficulties or should not be put in calf',
              [2] * 4, 'Any four, 2 marks each (4×2m). [*At least one point from each] of age and condition.')])
    # Question 6 -------------------------------------------------------------
    control = 'Weeds, pests and diseases in crops may be controlled by direct and indirect methods.'
    add('q6ai', 'Q6(a)(i)', '3-3-2', 'indirect-control', 'What is meant by indirect control?',
        [point('Any method of control that is effective despite not being targeted at the affected species', 2, '[Accept ‘a method that does not use chemicals’]')], control)
    add('q6aii', 'Q6(a)(ii)', '3-3-2', 'indirect-control-methods', 'Describe three methods of indirect control commonly used in Irish agriculture.',
        [menu('Stubble cleaning (uproots weed seedlings)|crop rotation (interrupts life cycle)|growth encouragement (gives crop growth advantage)|early harvest (less chance of attack on crop)|resistant varieties (less susceptible to attack)|eliminate host plants (interrupts life cycle)|biological control (explained example within definition)|drainage (affects habitat of pest)|liming (affects the life-cycle of liver fluke)',
              [4] * 3, 'Any three: (3×3m) + (3×1m), each method 3 and its effect (in brackets) 1.')], control)
    add('q6b', 'Q6(b)', '3-3-1', 'root-crop-soil-suitability', 'Explain four characteristics that would determine the suitability of a soil for root crops.',
        [menu('texture|pH|organic matter|structure|clay content or CEC|drainage|depth|colour|fertility', [4] * 4,
              'Any four: (4×3m) + (4×1m), each characteristic 3 and its effect 1. [One correct effect required per characteristic].')], node='2-3|1-5')
    add('q6ci', 'Q6(c)(i)', '3-3-2', 'cereal-lodging-causes', 'Give four possible causes of lodging in cereal crops.',
        [menu('Wind|rain|excessive N|tall varieties|disease|pest attack|Ca, P, or K deficiency|weakness of straw|sowing too early or late harvesting', [5, 3, 1, 1],
              'Any four. ' + FIRST.format('5 + 3 + 1 + 1'))])
    add('q6cii', 'Q6(c)(ii)', '3-3-3', 'stored-potato-damage', 'Describe two sources of damage to potato tubers during storage.',
        [menu('Frost (soggy or rot)|water (mould or rot)|sprouting (shrivel)|rodents (eaten)|bruised (rot)|light (greening)|high humidity (mould)|heat (sprouting)', [4, 4],
              'Any two: (2×3m) + (2×1m), each source 3 and its effect (in brackets) 1. [Cause (effect)]')])
    # Question 7 -------------------------------------------------------------
    terms = 'Explain each of the following terms:'
    for key, ref, concept, term, points in [
            ('q7ai', 'Q7(a)(i)', 'f1-hybrids', 'F1 hybrids', 'progeny of two purebred parents|parents are genetically different|progeny are heterozygous|inbred parents'),
            ('q7aii', 'Q7(a)(ii)', 'continuous-variation', 'Continuous variation', 'Characteristic controlled by a number of genes|genes interact|gives a range of phenotypes'),
            ('q7aiii', 'Q7(a)(iii)', 'back-cross', 'Back cross', 'Breeding a cross-breed offspring|with a pure-breeding recessive (plant or animal)|used to identify the genotype of the parent'),
            ('q7aiv', 'Q7(a)(iv)', 'incomplete-dominance', 'Incomplete dominance', 'Neither allele dominant (co-dominant or of equal dominance)|both expressed in phenotype|results in intermediate trait')]:
        add(key, ref, '4-1', concept, f'Explain the term: {term}.', [menu(points, [2, 2], 'Any two points, 2 + 2m.')], terms, node='3-6')
    cattle = ('In cattle, the allele for black coat (B) is dominant to the allele for white coat (b), and the allele for the polled condition (P) is dominant to the allele for horned (p). '
              'A bull, heterozygous for both traits, is mated with a horned, white cow.')
    add('q7bi', 'Q7(b)(i)', '4-1', 'bull-genotype', 'Give the genotype of the bull used in this cross.', [point('BbPp', 4)], cattle, node='3-6')
    add('q7bii', 'Q7(b)(ii)', '4-1', 'cross-genotypes', 'List the possible genotypes resulting from this cross.',
        [point('BbPp', 2, '4×2m.'), point('Bbpp', 2), point('bbPp', 2), point('bbpp', 2)], cattle, node='3-6')
    add('q7biii', 'Q7(b)(iii)', '4-1', 'white-horned-probability', 'What is the probability that a calf from this cross would be white and horned?', [point('25%', 4)], cattle, node='3-6')
    add('q7biv', 'Q7(b)(iv)', '4-1', 'horned-probability', 'What is the probability that a calf from this cross would be horned? Explain your answer.',
        [point('50% chance', 2), point('Half of the offspring have genotype pp or two recessive genes (for horns)', 2)], cattle, node='3-6')
    add('q7bv', 'Q7(b)(v)', '4-1', 'law-of-segregation', 'State Mendel’s Law of Segregation.',
        [point('Law of Segregation: when gametes are formed only one allele from a pair (of alleles) is carried in the gamete', 4)], node='3-6')
    add('q7c', 'Q7(c)', '4-3-2', 'ebi-sub-indices', '(i) List any two sub-indices of the EBI. (ii) Outline the factors that determine each sub-index listed.',
        [menu(['Production index: fat/ protein/ yield of milk', 'Fertility index: calving interval/ survival', 'Calving index: calving difficulties/ mortality/ gestation',
               'Maintenance index: cull cow weight', 'Management index: milking time/ temperament', 'Health index: lameness/ SCC mastitis/ health',
               'Beef index: carcase weight/ conformation/ carcase fat'], [4, 4], 'Any two: 2×(2+2m), each sub-index 2 and its factors 2.')],
        'The Economic Breeding Index (EBI) is widely used in dairying to identify genetically superior animals to improve dairy production in Ireland.', node='3-6|3-4')
    # Question 8 -------------------------------------------------------------
    twoof = 'Answer any two of the parts (a), (b), (c).'
    pests = twoof + ' The leatherjacket and the wireworm are the larval stages of two important crop pests.'
    add('q8ai', 'Q8(a)(i)', '3-3-2', 'leatherjacket-wireworm-adults', 'Name the adult stages of 1. the leatherjacket, 2. the wireworm.',
        [point('1. Cranefly or daddy longlegs', 2), point('2. Clickbeetle', 2)], pests)
    add('q8aii', 'Q8(a)(ii)', '3-3-2', 'leatherjacket-wireworm-damage', 'Describe the damage caused by each of these pests.',
        [point('Leatherjacket: underground stem/ soil level/ roots', 2), point('Wireworm: base of stem/ seeds/ tubers/ roots', 2)], pests)
    add('q8aiii', 'Q8(a)(iii)', '4-2', 'pest-phylum', 'Name the phylum to which they belong.', [point('Arthropoda', 2)], pests, node='3-1')
    add('q8aiv', 'Q8(a)(iv)', '4-2', 'arthropod-features', 'Describe three structural features of members of this phylum.',
        [menu('Jointed limbs|exoskeleton|chitin|triploblastic coelomate|bilateral symmetry|segmented body', [2] * 3, 'Any three, 2 marks each (3×2m).')],
        pests + ' (iii) Name the phylum to which they belong.', node='3-1')
    add('q8av', 'Q8(a)(v)', '3-3-2', 'complete-incomplete-metamorphosis', 'Distinguish fully between complete and incomplete metamorphosis.',
        [point('Complete (incomplete): larva (nymph)', 4, '2×(2+2m): each distinction 2 for complete and 2 for incomplete (in brackets).'),
         point('pupa (no pupa or nymph continues to grow or (nymphal) instars or regular ecdyses)', 4)], twoof, node='2-4|3-1')
    add('q8b', 'Q8(b)', '3-3-2', 'nitrogen-benefits-and-excess',
        'The correct amount of nitrogen fertiliser is of great benefit to crop growth, but excessive nitrogen can have negative effects. Discuss this statement.',
        [menu('Benefits of nitrogen: stimulates growth of leaf and stem|increases tillering|improves establishment|photosynthesis or chlorophyll|protein synthesis|cell division|yield increase|'
              'Negative effects: increased lodging|delayed ripening|increased disease susceptibility|reduced quality potatoes|lowers malting quality|inhibits clover|affects silage preservation|water pollution or eutrophication or leaching|more frost-prone|burning',
              [6] * 4, 'Any four, 6 marks each (4×6m). *[At least one point from each] of benefits and negative effects.')], twoof, node='2-4|1-6')
    members = [('i', 'Cross breeding', 'mating of animals of different breeds|to get the best characteristics of both in the offspring or hybrid vigour or heterosis|F1 seed varieties'),
               ('i', 'Crossing over', 'process in which (homologous) chromosomes exchange genetic material|occurs during meiosis|results in genetic variation or mutation'),
               ('ii', 'Active transport', 'movement of a substance from area of low concentration|to an area of high concentration|requires energy'),
               ('ii', 'Active immunity', 'animal creates antibodies|exposure to antigen or to disease|vaccination'),
               ('iii', 'Transpiration', 'loss of water vapour from leaves|through stomata'),
               ('iii', 'Translocation', 'movement of products of photosynthesis|through phloem|to storage organs or named'),
               ('iv', 'Nitrification', 'conversion of ammonium (ions) or urea|into nitrite and-or nitrate (ions)|by Nitrobacter (spp.) or Nitrosomonas (spp.)'),
               ('iv', 'Denitrification', 'loss of nitrogen from soil|nitrates converted|to nitrogen gas|by Thiobacillus (spp.)')]
    add('q8c', 'Q8(c)', '4-1', 'distinguishing-paired-terms',
        'Distinguish clearly between the members of any three of the following pairs of terms: (i) Crossbreeding and crossing-over. (ii) Active transport and active immunity. (iii) Transpiration and translocation. (iv) Nitrification and denitrification.',
        [menu(pool, [2, 2], f'({k}) {label}: two points, 2 + 2m.' + (' Two points per term for any three pairs.' if i == 0 else ''))
         for i, (k, label, pool) in enumerate(members)],
        twoof, marks=24, tariff={'kind': 'bestNofParts', 'answer': 6, 'ofParts': 8, 'perPart': 4},
        selection=closed(3, ['i', 'ii', 'iii', 'iv']), node='3-6|3-0|2-0|1-6')
    # Question 9 -------------------------------------------------------------
    why = 'Give scientific explanations for any four of the following:'
    for key, ref, topic, concept, item, points, node in [
            ('q9a', 'Q9(a)', '4-3-3', 'liver-fluke-drained-pasture', 'The reduced incidence of liver fluke (Fasciola hepatica) infestation in cattle grazed on well-drained pasture.',
             'Absence of snail|Lymnaea or Galba or mud snail or water snail|secondary host|larval stages need water|named larval stages (miracidium or cercarium)', None),
            ('q9b', 'Q9(b)', '3-1', 'water-through-plant', 'The movement of water from the soil through a plant and into the atmosphere.',
             'Root hairs|root xylem (tissue)|osmosis or diffusion|root pressure|adhesion or cohesion or capillarity|transpiration stream|evaporation|exits stomata', None),
            ('q9c', 'Q9(c)', '4-3-1', 'crossbred-sows', 'The use of cross-breed sows in pig production.',
             'Cross|between two named breeds|best qualities of both or hybrid vigour|good FCR|fast growth rate|good meat quality|good conformation|prolific', '3-3|3-6'),
            ('q9d', 'Q9(d)', '3-3-3', 'silage-acid-additive', 'The use of acid as an additive in silage making.',
             'Sulphuric acid or formic acid or propionic acid or acetic acid|lowers pH|inhibits fermentation|prevents bacterial activity|preservative|used for poor-quality grass or low sugar levels or wet conditions', '2-6'),
            ('q9e', 'Q9(e)', '3-1', 'greenhouse-carbon-dioxide', 'An increase in the yield of crops exposed to higher levels of carbon dioxide in a greenhouse.',
             'CO2 needed for photosynthesis|higher levels of CO2 increase rate of photosynthesis|converted to glucose|glucose converted to starch|more CO2 means more starch', None)]:
        add(key, ref, topic, concept, 'Give a scientific explanation for: ' + item,
            [menu(points, [7, 3, 2], 'Any three points. ' + FIRST.format('7 + 3 + 2'))], why, node=node)
    assert len(p.tasks) == 62, len(p.tasks)
    return p


def reviewed_tasks():
    p = build()
    return p.cards, p.tasks


def paper_review():
    return build().review('62 base tasks, one card each. A scale the scheme prints across a part\'s (i) and (ii) (Q1(a), (f), (j)) or across headings (Q2(a), '
                          'Q3 Option One (b)) is one task with the scale stated; parts priced separately are separate tasks. Q4(b) carries its compulsory named crop; '
                          'Q8(c) is one card for the choice of three pairs from four.')
