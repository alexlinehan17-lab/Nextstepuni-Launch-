"""2023 Higher review: the 81 original cards reconciled against the SEC sources.

All 44 paper pages and 32 scheme pages were inspected and the independent
census transcribed before any card was touched. 85 base tasks, one card each.
57 original card objects match a published task boundary and tariff and are
left byte-identical; they only gain an Atlas binding and an inspected official
source page. 24 originals are corrected IN PLACE, keeping their IDs:
Q2(a) and Q4(a) become one card each that lets any printed item score; Q5(a),
Q9(a)(ii), Q9(b)(i), Q11(a) and Q11(b) list their whole answer pool in one row
instead of a first row that only one scheme point could tick; Q13(c) and Q15(a)
carry every published method as its own route; Q13(d)(ii), Q14(b)(iii),
Q14(c)(i), Q14(c)(ii) and Q15(b)(iii) regain scheme points a five-row cap had
dropped; Q13(a)(i) and Q18(b)(ii) regain the published per-answer awards that
their factor-plus-description pairs made all-or-nothing; Q13(a)(ii) carries
the published drawing criteria; Q1(a)(ii), Q5(c) and Q13(b)(ii) regain answers
cut mid-sentence; Q8(c), Q15(c)(ii) and Q16(a)(ii) replace graph label soup with
the paper's own wording and graph; Q14(b)(iv) names the underlined term the
paper prints. The branch-only Q18(a)(i) card gains its diagram. Cards are added
for the missing Q7(a), Q7(b) and Q18(a)(v). Each correction records the
original wording, marks and object hash plus the SEC page that justifies it.
"""
import copy
import hashlib
import json
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan

FILE = 'LC024ALP000EV.pdf'
YEAR = 2023
HASHES = {'exampapers':'059f553f84ee5e11732cc00a8dedb3163785170a8c1b292ec234326ddeb6c118',
          'markingschemes':'713384aadabd9a6e520dc5288f9047a929a4e43890e928ee7c957113c9d0581a'}
KEPT_ONE_CARD = ' The original one-card form already lets any printed choice score, so it is kept unchanged (item-choice siblings are not separate practice identities).'
SELECTIONS = {
    '009db7e34cafe66f':('exam-selection','Instructions: Section A, ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    '74aedfcd3041d2ba':('exam-selection','Instructions: Section B, four of six independent questions. Every question is retained.'),
    'fcc876794c00fc0d':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    'd488accd90df746b':('independent-task-selection','Q1 either (a) or (b): both independently marked alternatives are retained.'),
    '5980173421c15769':('closed','Q2(a): explain any two of three printed growth stages, 2(3). One card: a single anyN row lists all three stages, claim limit two.'),
    '8f8a1a227248ac71':('closed','Q2(b): identify any two of three weed photographs, 2(2).' + KEPT_ONE_CARD),
    '31a0b95b8b64622b':('open','Q3(a): one source of calcium for either plants or animals; the scheme prints one open pool for each and one 2-mark award.'),
    'ebaf4d19714ab459':('closed','Q4(a): a reason for any three of four printed treatments, 3(2). One card: a single anyN row lists all four treatments, claim limit three.'),
    'ec450d9b7f7a6f17':('independent-task-selection','Q7 either (a) or (b): both alternatives are retained.'),
    '6df18fa968ac3e26':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    '03d94ff3adba0f87':('independent-task-selection','Q10 either (a) or (b): both alternatives are retained.'),
    'e8badd31ecb8c904':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    'cf154a4d33353a8e':('independent-task-selection','Q13: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'e1364468514ac507':('closed','Q13(b)(ii): implications of any two of three printed soil water states, 2+1. One card whose three rows are the published answers, the first correct at 2 and the second at 1.'),
    '9bb0357d5e6415ff':('independent-task-selection','Q16: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '3ae0bc3aadd760ee':('closed','Q17(b)(iii): identify any two of three plant photographs, 2(2).' + KEPT_ONE_CARD),
    '7a167b7d5c18ef90':('closed','Q17(c): grass reproduction either sexually or asexually. The scheme marks the two with different points, so they are mutually exclusive row routes on one card.'),
    'e52b396928582129':('closed','Q18(a)(i): label any three of four lettered udder structures, 3(1). One card: a single anyN row lists all four labels, claim limit three.'),
}
SUPPLEMENTARY = [
    (5,'in any named plant you have studied','open','Q2(a): a student-named plant; the scheme describes each stage without a plant pool.'),
    (6,'Explain one symptom of a named calcium deficiency in cows.','open','Q3(c): a student-named deficiency; the scheme prints milk fever or hypocalcaemia and an open symptom pool ("or valid answer").'),
    (9,'State the name of the disease that can cause lameness in','open','Q6(a): any one of four diseases the scheme accepts; parts (b) and (c) then mark the named disease, kept as mutually exclusive routes on one card each.'),
    (12,'outline one piece of technology that you have studied','open','Q9(a)(iii): a student-chosen technology; the scheme adds "other valid example".'),
    (29,'For a named food crop (other than grass) that you have studied','open','Q15(d): a student-named crop; the scheme notes its points apply to potatoes, barley or other cereal, kale.'),
    (10,'Describe actions these dairy farmers could do to improve their sustainability','open','Q7(b): two student-chosen actions; the scheme table of eight actions is a marking menu.'),
    (16,'Outline ways Tim can achieve this target.','open','Q11(a): student-chosen ways; the scheme pool is a marking menu.'),
    (21,'Identify the soil water content level for each diagram using the words in the box below.','answer-identification','Q13(b)(i): one correct state per diagram from the printed box.'),
    (30,'State with reason if the main source of emissions is above or below the national','answer-identification','Q16(a)(ii): one correct answer (below), not a route.'),
    (38,'Assist Jenny in placing each step in the correct','answer-identification','Q18(a)(v): one correct letter for each numbered step.'),
]
TOPIC = 'agricultural-science-higher-'
SNAPSHOT = ROOT / 'scripts/markbank/authored/agricultural-science-corrected-originals.json'
PREFIX = 'agsci-2023-hl-'
# Original objects written back unchanged after an earlier review rewrote them.
RESTORED = []


def original_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    return dict(year=YEAR, level='higher', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 33)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=[],
                independentBoundaryReview='85 base tasks, one card each. 57 original cards match a published boundary and tariff unchanged; Q2(b) and Q17(b)(iii) already let any printed choice score. 24 are corrected in place (Q1(a)(ii), Q2(a), Q4(a), Q5(a), Q5(c), Q8(c), Q9(a)(ii), Q9(b)(i), Q11(a), Q11(b), Q13(a)(i), Q13(a)(ii), Q13(b)(ii), Q13(c), Q13(d)(ii), Q14(b)(iii), Q14(b)(iv), Q14(c)(i), Q14(c)(ii), Q15(a), Q15(b)(iii), Q15(c)(ii), Q16(a)(ii), Q18(b)(ii)); the branch-only Q18(a)(i) gains its diagram; three cards are added for the missing Q7(a), Q7(b) and Q18(a)(v).',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


# Paper / scheme crop regions for every base task (original cards included).
P = lambda *r: [region(*x) for x in r]
Q1A = (3, .16, .205)
Q1PHOTOS = (3, .16, .355)
Q2 = (5, .065, .11)
Q3 = (6, .065, .135)
Q4 = (7, .065, .135)
Q5 = (8, .065, .135)
Q6 = (9, .065, .135)
Q7 = (10, .065, .122)
Q8 = (11, .065, .152)
Q9A = (12, .065, .395)
Q9B = (13, .090, .152, 0, .575)
Q10B = (15, .065, .348)
Q11 = (16, .065, .335)
Q12 = (17, .065, .34)
Q13 = ((20, .160, .182), (20, .192, .234, 0, .66))
Q13B = (21, .062, .108)
Q14 = (24, .065, .150, 0, .66)
Q14B = (24, .348, .448, 0, .615)
Q14C = (25, .246, .370)
Q15 = (27, .065, .208, 0, .615)
Q15B = (28, .064, .088)
Q15C = (28, .497, .80)
Q16 = (30, .065, .135)
Q16G = (30, .065, .478)
Q16D = (33, .090, .23)
Q17A = (34, .090, .265)
Q17B = (35, .256, .448)
Q18 = (37, .065, .175, 0, .63)
REGIONS = {
    'Q1(a)(i)': (P((3, .16, .455)), P((12, .137, .222))),
    'Q1(a)(ii)': (P(Q1PHOTOS, (3, .462, .502)), P((12, .222, .287))),
    'Q1(a)(iii)': (P(Q1A, (3, .603, .645)), P((12, .287, .37))),
    'Q1(b)(i)': (P((4, .065, .370)), P((12, .388, .471))),
    'Q1(b)(ii)': (P((4, .375, .670)), P((12, .471, .612))),
    'Q2(a)': (P((5, .065, .638)), P((12, .612, .834))),
    'Q2(b)': (P(Q2, (5, .638, .835)), P((12, .834, .885))),
    'Q3(a)': (P((6, .065, .24)), P((13, .085, .193))),
    'Q3(b)': (P(Q3, (6, .310, .335)), P((13, .193, .242))),
    'Q3(c)': (P(Q3, (6, .437, .525)), P((13, .242, .348))),
    'Q4(a)': (P((7, .065, .65)), P((13, .348, .583))),
    'Q4(b)': (P(Q4, (7, .650, .705)), P((13, .583, .81))),
    'Q5(a)': (P((8, .065, .255)), P((14, .085, .318))),
    'Q5(b)': (P(Q5, (8, .422, .485)), P((14, .318, .465))),
    'Q5(c)': (P(Q5, (8, .647, .69)), P((14, .465, .56))),
    'Q6(a)': (P(Q6, (9, .137, .18, 0, .63)), P((14, .56, .618))),
    'Q6(b)': (P(Q6, (9, .253, .296, 0, .63)), P((14, .618, .845))),
    'Q6(c)': (P(Q6, (9, .429, .452)), P((15, .085, .28))),
    'Q6(d)': (P(Q6, (9, .555, .58)), P((15, .28, .395))),
    'Q7(a)': (P((10, .065, .428)), P((15, .395, .555))),
    'Q7(b)': (P(Q7, (10, .452, .87)), P((16, .085, .71))),
    'Q8(a)': (P((11, .065, .39)), P((17, .085, .148))),
    'Q8(b)': (P(Q8, (11, .392, .42)), P((17, .148, .278))),
    'Q8(c)': (P(Q8, (11, .512, .765)), P((17, .278, .39))),
    'Q9(a)(i)': (P((12, .065, .414)), P((17, .39, .436))),
    'Q9(a)(ii)': (P(Q9A, (12, .483, .507)), P((17, .436, .532))),
    'Q9(a)(iii)': (P(Q9A, (12, .690, .733)), P((17, .532, .628))),
    'Q9(b)(i)': (P((13, .065, .205)), P((17, .645, .78))),
    'Q9(b)(ii)': (P(Q9B, (13, .397, .69)), P((18, .085, .338))),
    'Q10(a)(i)': (P((14, .065, .495)), P((18, .338, .421))),
    'Q10(a)(ii)': (P((14, .065, .115), (14, .502, .527)), P((18, .421, .505))),
    'Q10(b)(i)': (P((15, .065, .377)), P((18, .522, .707))),
    'Q10(b)(ii)': (P(Q10B, (15, .572, .596)), P((18, .707, .824))),
    'Q10(b)(iii)': (P((15, .065, .135), (15, .701, .744)), P((18, .824, .905))),
    'Q11(a)': (P((16, .065, .394)), P((19, .085, .238))),
    'Q11(b)': (P(Q11, (16, .587, .612)), P((19, .238, .438))),
    'Q12(a)': (P((17, .065, .365)), P((19, .438, .486))),
    'Q12(b)': (P(Q12, (17, .41, .434)), P((19, .486, .554))),
    'Q12(c)': (P(Q12, (17, .51, .534)), P((19, .554, .618))),
    'Q12(d)': (P((17, .065, .155), (17, .634, .658)), P((19, .618, .75))),
    'Q13(a)(i)': (P((20, .160, .495)), P((20, .155, .591))),
    'Q13(a)(ii)': (P(*Q13, (20, .494, .52)), P((20, .591, .747))),
    'Q13(b)(i)': (P((21, .062, .425)), P((20, .747, .83))),
    'Q13(b)(ii)': (P(Q13B, (21, .425, .745)), P((21, .085, .355))),
    'Q13(c)': (P(*Q13, (22, .062, .125)), P((21, .355, .613))),
    'Q13(d)(i)': (P((23, .065, .49)), P((21, .630, .747))),
    'Q13(d)(ii)': (P((23, .090, .445), (23, .624, .648)), P((21, .747, .845))),
    'Q14(a)': (P((24, .065, .29)), P((22, .085, .237))),
    'Q14(b)(i)': (P(Q14, (24, .348, .49)), P((22, .237, .351))),
    'Q14(b)(ii)': (P(Q14, Q14B, (24, .584, .608)), P((22, .351, .413))),
    'Q14(b)(iii)': (P(Q14, Q14B, (24, .706, .73)), P((22, .413, .493))),
    'Q14(b)(iv)': (P(Q14B, (25, .062, .108, 0, .73)), P((22, .493, .537))),
    'Q14(b)(v)': (P(Q14B, (25, .180, .205, 0, .73)), P((22, .537, .582))),
    'Q14(c)(i)': (P((25, .246, .40)), P((22, .582, .679))),
    'Q14(c)(ii)': (P(Q14C, (26, .064, .088)), P((22, .679, .788))),
    'Q14(c)(iii)': (P(Q14C, (26, .282, .344)), P((22, .788, .85))),
    'Q14(c)(iv)': (P(Q14C, (26, .445, .508)), P((22, .85, .91))),
    'Q15(a)': (P((27, .065, .29)), P((23, .085, .454))),
    'Q15(b)(i)': (P(Q15, (28, .064, .114)), P((23, .454, .503))),
    'Q15(b)(ii)': (P(Q15B, (28, .156, .218)), P((23, .503, .567))),
    'Q15(b)(iii)': (P(Q15B, (28, .321, .364)), P((23, .567, .667))),
    'Q15(c)(i)': (P((28, .497, .831)), P((23, .667, .715))),
    'Q15(c)(ii)': (P(Q15C, (29, .064, .107)), P((23, .715, .835))),
    'Q15(d)': (P(Q15, (29, .301, .75)), P((24, .085, .271))),
    'Q16(a)(i)': (P((30, .065, .501)), P((24, .271, .312))),
    'Q16(a)(ii)': (P(Q16G, (30, .540, .583)), P((24, .312, .408))),
    'Q16(a)(iii)': (P(Q16G, (30, .701, .744)), P((24, .408, .594))),
    'Q16(b)(i)': (P(Q16G, (31, .064, .126)), P((24, .594, .9))),
    'Q16(b)(ii)': (P(Q16, (31, .744, .768)), P((25, .085, .148))),
    'Q16(c)': (P(Q16, (32, .064, .188)), P((25, .148, .258))),
    'Q16(d)(i)': (P(Q16, (33, .090, .272)), P((25, .274, .423))),
    'Q16(d)(ii)': (P(Q16, Q16D, (33, .556, .618)), P((25, .423, .62))),
    'Q17(a)(i)': (P((34, .065, .80)), P((26, .085, .443))),
    'Q17(a)(ii)': (P(Q17A, (35, .064, .107)), P((26, .443, .509))),
    'Q17(b)(i)': (P((35, .256, .47)), P((26, .509, .643))),
    'Q17(b)(ii)': (P(Q17B, (35, .684, .727)), P((26, .643, .759))),
    'Q17(b)(iii)': (P((36, .064, .30)), P((26, .759, .855))),
    'Q17(c)': (P((36, .305, .40)), P((27, .085, .318))),
    'Q18(a)(i)': (P((37, .066, .386)), P((27, .317, .559))),  # the anchor Atlas already publishes as 1001
    'Q18(a)(ii)': (P(Q18, (37, .389, .413)), P((27, .562, .645))),
    'Q18(a)(iii)': (P(Q18, (37, .536, .56)), P((27, .645, .83))),
    'Q18(a)(iv)': (P(Q18, (37, .679, .703)), P((28, .085, .204))),
    'Q18(a)(v)': (P((38, .064, .552)), P((28, .204, .285))),
    'Q18(b)(i)': (P(Q18, (38, .561, .72)), P((28, .285, .444))),
    'Q18(b)(ii)': (P(Q18, (38, .561, .585), (39, .064, .145)), P((28, .444, .845))),
}
# Atlas topics, read from each task's content (SEC-derived, not copied).
ATLAS = {
    'Q1(a)': 'beef-cattle', 'Q1(b)(i)': 'dairy-cattle|sheep', 'Q1(b)(ii)': 'dairy-cattle',
    'Q2(a)': 'crop-production|plant-physiology', 'Q2(b)': 'classification-of-animals-plants|crop-production',
    'Q3(a)': 'soil-science|fertilisers-pollution-environment-cycles', 'Q3(b)': 'soil-science', 'Q3(c)': 'animal-diseases|dairy-cattle',
    'Q4': 'beef-cattle|genetics', 'Q5': 'soil-science|scientific-practices-experiments-investigations',
    'Q5(c)': 'soil-science|fertilisers-pollution-environment-cycles', 'Q6': 'sheep|animal-diseases',
    'Q7(a)': 'dairy-cattle', 'Q7(b)': 'dairy-cattle|fertilisers-pollution-environment-cycles',
    'Q8': 'scientific-practices-experiments-investigations|fertilisers-pollution-environment-cycles',
    'Q9(a)': 'innovation-and-biotechnology-in-agriculture|crop-production', 'Q9(b)': 'beef-cattle|animal-physiology-reproductive-systems',
    'Q10(a)': 'pigs|animal-physiology-digestive-system', 'Q10(b)': 'pigs', 'Q10(b)(iii)': 'pigs|animal-physiology-digestive-system',
    'Q11': 'beef-cattle|animal-physiology-reproductive-systems', 'Q12': 'fertilisers-pollution-environment-cycles|soil-science',
    'Q13': 'soil-science', 'Q13(c)': 'soil-science|scientific-practices-experiments-investigations',
    'Q13(d)': 'soil-science|innovation-and-biotechnology-in-agriculture',
    'Q14': 'crop-production', 'Q14(c)': 'crop-production|scientific-practices-experiments-investigations',
    'Q15(a)': 'soil-science|scientific-practices-experiments-investigations', 'Q15(b)': 'soil-science',
    'Q15(c)': 'soil-science|fertilisers-pollution-environment-cycles', 'Q15(d)': 'crop-production',
    'Q16': 'fertilisers-pollution-environment-cycles', 'Q16(a)': 'fertilisers-pollution-environment-cycles|beef-cattle',
    'Q17': 'grassland', 'Q17(b)(iii)': 'grassland|classification-of-animals-plants', 'Q17(c)': 'grassland|plant-physiology',
    'Q18': 'dairy-cattle', 'Q18(a)': 'dairy-cattle|animal-diseases', 'Q18(a)(i)': 'dairy-cattle',
    'Q18(a)(v)': 'dairy-cattle|scientific-practices-experiments-investigations',
}
# Scheme answer pools, lifted from the marking scheme (PDF pages 12-28).
STAGES = {
    'Germination': "Embryo's cells start to enlarge / seed coat breaks open / root or radicle emerges (first) / (followed by) the shoot or plumule emerges",
    'Stem Elongation': 'Rapid growth of stems / stem lengthens (between the upper nodes)',
    'Flowering': 'Seed head develops or heading out / stem is fibrous and strong enough to support seed head / plants stop growing / produce flowers (buds) for reproduction',
}
TREATMENTS = {
    'Clipped': 'Clipped Improves heat dissipation (from the body when sweating) or prevention of pneumonia/ control of lice',
    'Worm dosed': 'Worm dosed To kill any worms (endoparasites) present in animals',
    'Treated for lice': 'Treated for lice To prevent lice being spread between cattle / prevent irritation',
    'Sorted into pens based on breed and weight': 'Sorted into pens based on breed and weight Animals can be kept under the exact same conditions and comparisons can be made based on breed / reduced amount of competition between animals (as all similar weight)',
}
SAMPLING = ['Soil sampler or soil corer or soil auger', 'W shape', 'take sample every 2 - 4ha', 'taken at random',
            'avoid gateways or troughs or dung or urine patches', 'taken at uniform depth',
            'take separate samples from areas that are different in soil type, previous cropping history, slope, drainage or persistent poor yields',
            'do not sample a field until 3 to 6 months after the last application of P and K and 2 years where lime was applied',
            'take a minimum of 20 soil cores',
            'sample fields at the same time of the year to aid comparisons of soil sample results or avoid sampling under extremes of soil conditions e.g. waterlogged or very dry soils',
            'place the soil sample in a soil box to avoid contamination and write the field number on the soil box']
FARMDROID = ['Less chemical herbicide required', 'fewer fossil fuels burned as solar powered', 'no need to recharge batteries', 'less soil compaction',
             'increased yields as less weeds', 'precision sowing to maximise land usage', 'less labour']
SCANNING = ['Know if the animal is barren or not (or pregnant)', 'know due date for accurate feeding', 'house animals at correct time',
            'pen animals according to number of young they are carrying', 'a lot of barren animals will indicate a problem with fertility of sire',
            'management practices at birth, especially for multiple births (identify due date)']
CALVES = ['Good heat detection', 'good cow or sire fertility', 'grading up or cull poor performing cows', 'good hygiene at calving',
          'enough good quality colostrum at birth', 'highly digestible feed (or concentrate supplementation) (to ensure good milk production or increased liveweight gain)',
          'scanning of cows to accurately know calving date or proper supervision at calving or assist or vet if calving difficulties',
          'iodine on navel at birth', 'vaccination programme']
CALVING_RATE = ['Monitor liveweight (of young heifers) to ensure they are on course to achieve target weights (aim for 60% of mature weight at mating)',
                'correct BCS of 3.0 at mating', 'correct nutrition - good quality leafy grass', 'good heat detection (to increase submission rate)',
                'use AI on cows in first 3 weeks of breeding for replacements or increase EBI of herd or keep early calves for replacements for high EBI',
                'identify non-cycling cows (and get them checked by the vet)', 'ensure healthy cows (received vaccinations)', 'synchronised breeding']
ACTIONS = {
    'Milk recording at least four times a year': 'Identify high yielding cows with good milk solids for breeding or identifying and breeding more profitable and efficient cows which are better for the environment / identify and cull poorer producing cows or cows with high SCC',
    'ASSAP (water)': 'Undertake a water quality assessment to measure and improve the quality of water on the farm',
    'Increasing EBI': 'EBI will help farmers breed a more profitable dairy cow and lower GHG emissions.',
    'Improving soil': 'Use of LESS / sow multispecies swards',
    'Land management': 'Increase grazing season / sow multispecies swards / grassland management to reduce risk of parasites / incorporate clover for N fixation and reduced fertiliser user / soil testing for pH, N, P or K every five years',
    'Farmer training': 'Experience in milk production / qualification from Ag College or Teagasc course',
    'Record keeping or Traceability': 'Keep records of animal remedies / records of animal movements or births and deaths / use of AIM system / tagging / animal passports / compliance with disposal of animals',
    'Animal welfare': 'Sufficient access to clean water and forage / livestock in individual pens to be in sight of other livestock / calving pens hygienic and safe / castration with burdizzo to be before 6 months / manage AI to minimise calving difficulty / appropriate animal handling facilities to minimise stress or injury / lactating cows to be milked daily / quarantine bought in stock to monitor disease',
}
SOIL_FACTORS = {
    'Parent material': 'Parent rock is weathered into smaller particles / granite contains quartz which is weathered into sand particles and acidic in nature / limestone rock is alkaline in nature and increases the pH of soil formed from it / determines physical or chemical characteristics of soil',
    'Climate': 'Temperature – heating and cooling of rock Water – physical or chemical weathering (or any named form) – freeze-thaw or hydrolysis or solution or hydration or determines biological reactions',
    'Topography': 'Slope of landscape / steep slopes the soil is eroded down to valley or thin layer of soil on slopes or deep fertile soil in valley',
    'Organisms': 'Contribute humus when die / (microorganisms) help to decompose organic matter / organic matter increases soil fertility / soils that develop / increase soil fertility or improve soil structure (burrowing, binding, eroding)/ organisms break up rock',
    'Time': 'Young soils (Ireland) have high levels of rock available for weathering / young soils not as deep',
}
LAB = ['Dried soil sample', 'same mass of both soils', 'add to filter paper in funnel', 'add set volume of water to soil',
       'record time taken for water to flow into beakers or record volume for filtrate (for set time)',
       'water would pass through the brown earth sample quicker (as no iron pan)']
FIELD = ['Two open ended tubes', 'set tubes into soil (one in each type)', 'pour equal volume of water into each tube',
         'record time taken for water to drain down through tube', 'result: soil where water drains fastest has best infiltration rate']
MOISTURE = ['Provide water to plants (plant cells contain large amounts of water)', 'seed germination', 'photosynthesis', 'nutrients available',
            'chemical reactions', 'keeps turgor', 'transpiration', 'microbial activity or soil organisms', 'to maintain soil structure or prevent erosion']
CLOVER = ['Increase nitrogen supply to the crop', 'encourage mycorrhizal fungi', 'improve soil function', 'their own root systems can help drainage',
          'improve soil structure', 'prevents weeds']
PLANT_COUNT = ['Place quadrat (0.25m2) on the ground', 'at random', 'count the number of plants (established) in quadrat', 'repeat (at least 10 times)',
               'get average plant count', 'multiply by 80,000 to determine the number of plants in 2 hectares']
COUNT_ADVANTAGES = ['Determine if sowing conditions were optimal or impact of weather conditions', 'if correct seeding rate was used',
                    'correct fertiliser amount used', 'determining germination or establishment rate', 'weed control']
HAND = ['dry soil sample', 'rub between fingers and thumb', 'note grittiness and smoothness',
        'wet sample (and rub between fingers and thumb and note grittiness, smoothness)', 'note plasticity or if sample is sticky',
        'check if it is possible to roll sample into threads or ring or cast', 'valid result']
SEDIMENT = ['add soil sample to water in a beaker and stir', 'pour mixture into graduated cylinder and rinse', 'completely cover the soil with water',
            'stopper or cover the cylinder and shake to mix the soil', 'leave to settle for a few hours or overnight', 'observe layers that have settled',
            'using the graduations on the cylinder record the amount of sand, silt and clay in the soil sample', 'calculate percentage',
            'use soil triangle to find soil texture']
SIEVE = ['dry soil samples', 'crush sample (with pestle and mortar)', 'get mass of soil sample',
         'place sample in sieves with largest sieve on top and smallest on bottom and shake', 'weigh contents of each sieve',
         'calculate percentage of each particle type', 'using soil (texture) triangle classify soil sample']
LIMING = ['Increase in earthworm activity', 'improvement in soil structure (drainage or aeration or flocculation)', 'grass is more palatable to livestock',
          'increased cation exchange capacity', 'improve nutrient availability']
MILK_FACTORS = {
    'Cow health': 'susceptible to irritation or inflammation of the udder if hygiene conditions are poor / sick cows have reduced milk yield and poorer quality milk',
    'Somatic cell counts': 'high somatic cell counts in milk indicate an increased presence of white blood cells—a signal that the cow is fighting an illness / other types of somatic cells can degrade the fat and protein content in milk which adversely affect milk quality',
    'Diet': 'affects the composition of milk / require good digestible feed / ~14% crude protein diet / lack of sufficient nutrients reduces milk quality',
    'Milk handling or storage': 'machine hygiene is very important, or machine is hot washed after milking / install plate cooler to reduce milk temperature as quickly as possible / bulk tank kept below 4oC / no milk washings entering the tank',
    'Milk hygiene': 'any relevant point on hygiene or TBC',
    'Breed or genetics': 'high EBI cow used or named breed with high milk solids',
}
UDDER = {'A': 'Teat', 'B': 'Median suspensory ligament', 'C': 'Connective tissue / fine membrane', 'D': 'Epidermis / hind quarter / outer wall'}
UDDER_ARROWS = {'A': 'Arrow from the lower left to the first teat', 'B': 'Arrow from the upper left to the green band inside the top of the udder',
                'C': 'Arrow from the upper right to the thin pale membrane dividing the inside of the udder', 'D': 'Arrow from the lower right to the orange body of the udder'}
CMT = {'A': 'Take a sample of milk from each quarter onto each well of the paddle', 'B': 'Add equal amounts of CMT solution and rotate in circular motion',
       'C': 'High cell count mixture will thicken to a gel', 'D': 'Pour off excess milk'}
PAGE4 = 'The scheme\'s own rule (PDF page 4): "the first correct answer encountered is awarded" the first mark, and each later correct answer the next.'


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
    RESTORED.clear()
    # Original cards carry no review stamp; cards this review wrote do. The
    # corrected originals come from their frozen snapshot, never the file.
    originals = {cid: card for cid, card in existing.items()
                 if cid.startswith(PREFIX) and (card.get('qa') or {}).get('humanReviewedBy') != 'agent-source-reviewed'}
    snapshot = json.loads(SNAPSHOT.read_text()) if SNAPSHOT.exists() else {}
    for cid, record in snapshot.items():
        if cid.startswith(PREFIX):
            originals[cid] = record['original']
    numbered = []

    def task(cid, ref, base, selection=None):
        pp, sp = REGIONS[base]
        # Q18(a)(i) was published to Atlas as 1001 by an earlier review; the
        # rest of the paper numbers on from 1002.
        number = '1001' if cid == PREFIX + 'q18ai' else str(1002 + len(numbered))
        if cid != PREFIX + 'q18ai':
            numbered.append(cid)
        t = dict(questionRef='2023 HL ' + ref, paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                 atlasNumbers={cid: number}, cardIds=[cid],
                 examTopicIds=[TOPIC + t for t in atlas_for(ref).split('|')],
                 selection=selection or {'kind': 'none', 'reason': 'Required response at a published boundary. Scheme alternatives remain marking menus.'},
                 evidence='All 44 paper and 32 scheme pages visually inspected. Boundary and tariff checked against the independently transcribed census.')
        tasks.append(t)
        return t

    def keep(key, ref, selection=None):
        cid = PREFIX + key
        card = originals[cid]
        assert card['questionRef'] == '2023 HL ' + ref, (cid, card['questionRef'])
        t = task(cid, ref, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'unchanged'
        if cid in snapshot:
            assert original_hash(card) == snapshot[cid]['originalSha256']
            RESTORED.append(card)

    def source(ref, pp):
        return dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2023 Higher — ' + ref,
                    pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2023 Higher Level examination paper — © State Examinations Commission.',
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
                    section='A' if int(ref.split('(')[0][1:]) <= 12 else 'B', questionRef='2023 HL ' + ref,
                    topicId='agsci-' + topic, curriculumNodeIds=['agsci-' + topic],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel=tariff or {'kind': 'fixed'}, sourceMaterial=source(ref, pp))
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        if extra_fields: card.update(extra_fields)
        t = task(cid, ref, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        t['originalCard'] = 'added'
        cards.append(card)
        return card

    def fix(key, ref, changes, drop=(), correction=None, selection=None):
        """Correct an original in place: same ID, ref and boundary; only the named fields change."""
        cid = PREFIX + key
        card = copy.deepcopy(originals[cid])
        assert card['questionRef'] == '2023 HL ' + ref, (cid, card['questionRef'])
        for field in drop:
            card.pop(field, None)
        if 'rows' in changes:
            changes = dict(changes, rows=[dict(row, id=f'r-{i+1}') for i, row in enumerate(changes['rows'])])
        card.update(changes)
        card['curriculumNodeIds'] = [card['topicId']]
        card['sourceMaterial'] = source(ref, REGIONS[ref][0])
        t = task(cid, ref, ref, selection)
        t['marksPerRoute'] = card['totalMarks']
        record(cid, t, correction)
        cards.append(card)
        return card

    def closed(choose, options):
        # Item choice is ONE practice card (coordinator rule, 2026-10-12).
        return {'kind': 'closed', 'choose': choose, 'options': options, 'pooled': True}

    def pool(key, ref, options, steps, notation, note, page, scheme_page, wording, extra=None):
        """A one-row pool card: the whole published pool, any len(steps) of it."""
        old = originals[PREFIX + key]
        row = menu(options, steps, note)
        if extra:
            row.update(extra)
        fix(key, ref, dict(rows=[row], tariffModel={'kind': 'fixed', 'notation': notation}), drop=('notes',),
            correction=(f'Visually verified paper PDF page {page} and scheme PDF page {scheme_page} ({wording}, "{notation}"). '
                        f'The original first row held {old["rows"][0]["verbatim"]!r} alone, so a correct pair drawn from the rest of the pool could not tick it. '
                        f'Same ID, boundary and {old["totalMarks"]} marks; one row lists the whole published pool, any {len(steps)} of it.'))

    # Section A ---------------------------------------------------------------
    for k, ref in [('q1ai', 'Q1(a)(i)')]:
        keep(k, ref)
    fix('q1aii', 'Q1(a)(ii)', dict(rows=[point('Dual-purpose breed is an animal breed that provides at least 2 kinds of resources (e.g. meat, eggs, milk)', 2)]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 3 ("Breed C is a dual-purpose breed. Explain the underlined term.") and scheme PDF page 12 '
                    '("Dual-purpose breed is an animal breed that provides at least 2 kinds of resources (e.g. meat, eggs, milk)", 2). '
                    'The original answer stopped at "provides at least 2", with the rest in a note. Same ID, boundary and 2 marks; the answer is the whole published sentence.'))
    for k, ref in [('q1aiii', 'Q1(a)(iii)'), ('q1bi', 'Q1(b)(i)'), ('q1bii', 'Q1(b)(ii)')]:
        keep(k, ref)
    stages = list(STAGES)
    fix('q2a', 'Q2(a)', dict(
        rows=[menu(list(STAGES.values()), [3, 3], 'Any two of the three printed stages, 3 marks each (2(3)). In order the options describe Germination, Stem Elongation and Flowering.')],
        questionText='Explain what happens at any two of the following stages in any named plant you have studied: Germination, Stem Elongation, Flowering.'),
        drop=('notes',), selection=closed(2, stages),
        correction=('Visually verified paper PDF page 5 ("Explain what happens at any two of the following stages in any named plant you have studied", Germination, Stem Elongation and Flowering) '
                    'and scheme PDF page 12 (one answer per stage, "2(3)"). The original funded Germination and Stem Elongation as rows and left Flowering in a note, so a student who chose it could not score it. '
                    'Same ID: one any-two-of-three card whose anyN row lists all three stages, claim limit two, 6 marks.'))
    keep('q2b', 'Q2(b)', selection=closed(2, ['Chickweed', 'Charlock', "Shepard's Purse"]))
    for k, ref in [('q3a', 'Q3(a)'), ('q3b', 'Q3(b)'), ('q3c', 'Q3(c)')]:
        keep(k, ref)
    fix('q4a', 'Q4(a)', dict(
        rows=[menu(list(TREATMENTS.values()), [2, 2, 2], 'A reason for any three of the four printed treatments, 2 marks each (3(2)).')]),
        drop=('notes',), selection=closed(3, list(TREATMENTS)),
        correction=('Visually verified paper PDF page 7 ("Suggest one reason for any three treatments listed below", four printed treatments) and scheme PDF page 13 (a reason for each of the four, "3(2)"). '
                    'The original funded three treatments as rows and left "Sorted into pens based on breed and weight" in a note. '
                    'Same ID: one any-three-of-four card whose anyN row lists all four treatments with the scheme reasons, claim limit three, 6 marks.'))
    keep('q4b', 'Q4(b)')
    pool('q5a', 'Q5(a)', SAMPLING, [3, 3], '2(3)', 'Any two points from the published pool, 3 marks each. The scheme adds "(marks maybe awarded for points on a diagram)".',
         8, 14, '"Briefly describe how to collect soil samples for soil testing", one pool of eleven sampling points')
    keep('q5b', 'Q5(b)')
    fix('q5c', 'Q5(c)', dict(rows=[point("Soil tests allow you to identify the key nutrients your soil needs more of, so you can make an informed decision on the correct fertiliser in the right quantity for soil's needs.", 2)]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 8 ("With record high fertiliser prices, outline how soil testing can improve the economic sustainability of the farm") and scheme PDF page 14 (one sentence, 2). '
                    'The original answer stopped at "the key nutrients your soil", with the rest in a note. Same ID, boundary and 2 marks; the answer is the whole published sentence.'))
    for k, ref in [('q6a', 'Q6(a)'), ('q6b', 'Q6(b)'), ('q6c', 'Q6(c)'), ('q6d', 'Q6(d)')]:
        keep(k, ref)
    goats = 'Answer either (a) or (b). Liam and Joan are goat dairy farmers in County Sligo.'
    add('q7a', 'Q7(a)', '4-3-2', 'goat-and-cow-dairy-comparison',
        'Complete the table to show how goat dairy farming compares to cow dairy farming. The first one has been done as an example.',
        [point('Lactation length (days) — 305', None, 'The scheme prints 3+3+2+2 for the four cow cells. ' + PAGE4),
         point('Gestation length (days) — 280 - 283', None), point('Oestrus length (hours) — 18 - 24', None),
         point('Breeding programme — (High yielding cows with high milk solids) bred every year (or 365 days)', None)],
        goats, marks=10, tariff={'kind': 'orderedSplit', 'notation': '3+3+2+2'}, figure='agsci-2023-hl-paper-goat-cow-table')
    action_options = list(ACTIONS) + list(ACTIONS.values())
    add('q7b', 'Q7(b)', '4-3-1', 'dairy-sustainability-bonus-actions',
        'Some dairy farmers can receive a sustainability bonus if they are taking actions to improve sustainability on their farm. '
        'Describe actions these dairy farmers could do to improve their sustainability and receive the bonus. '
        'The first one has been done as an example: Use protected urea — Reduces nitrogen loss and greenhouse gases emissions while maintaining the yield when compared with unprotected urea.',
        [menu(action_options, [3, 3, 2, 2],
              'Two actions, each with its description: four answers in all. The scheme prints 3+3+2+2. ' + PAGE4 + ' The first eight options are the scheme\'s actions and the last eight their descriptions, in the same order; a description counts only for an action you gave. The scheme prints three of the actions in full as ASSAP (water) assessment, Increasing EBI of the herd and Improving soil health. The worked example (protected urea) does not score.')],
        goats, tariff={'kind': 'fixed', 'notation': '3+3+2+2'})
    keep('q8a', 'Q8(a)')
    keep('q8b', 'Q8(b)')
    fix('q8c', 'Q8(c)', dict(
        stem='An agricultural science student wanted to see if the amount of nitrates being leached into water from spreading protected urea is less than unprotected urea.',
        questionText='The student tested the leachate using nitrate strips and recorded the results shown below. Analyse the graph and briefly describe the conclusion the student made from his investigation.',
        rows=[dict(point('There is a large amount of nitrate present in the water from the unprotected urea (250mg/l) compared to protected urea (50mg/l)', 3,
                         'One conclusion, 3 marks; the scheme prints the two as alternatives.'),
                   kind='alt', accepts=['farmers should use protected urea as less nitrate is leached when compared to unprotected urea'])]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 11 ("The student tested the leachate using nitrate strips and recorded the results shown below" above the bar chart, then "Analyse the graph and briefly describe the conclusion the student made from his investigation") '
                    'and scheme PDF page 17 (two alternative conclusions, 3). The original stem was the chart\'s axis labels run together and the second published conclusion was missing. '
                    'Same ID, boundary, chart crop and 3 marks; the stem and question are the paper\'s own wording and the row accepts both conclusions.'))
    keep('q9ai', 'Q9(a)(i)')
    pool('q9aii', 'Q9(a)(ii)', FARMDROID, [3, 3], '2(3)', 'Any two benefits from the published pool, 3 marks each.',
         12, 17, '"Explain how the Farmdroid can benefit the environment and the farmer", one pool of seven benefits')
    keep('q9aiii', 'Q9(a)(iii)')
    pool('q9bi', 'Q9(b)(i)', SCANNING, [3, 3], '2(3)', 'Any two benefits from the published pool, 3 marks each.',
         13, 17, '"Briefly describe the benefits of pregnancy scanning in animals", one pool of six benefits')
    keep('q9bii', 'Q9(b)(ii)')
    for k, ref in [('q10ai', 'Q10(a)(i)'), ('q10aii', 'Q10(a)(ii)'), ('q10bi', 'Q10(b)(i)'), ('q10bii', 'Q10(b)(ii)'), ('q10biii', 'Q10(b)(iii)')]:
        keep(k, ref)
    pool('q11a', 'Q11(a)', CALVES, [3, 3], '2(3)', 'Any two ways from the published pool, 3 marks each.',
         16, 19, '"Outline ways Tim can achieve this target", one pool of nine ways')
    pool('q11b', 'Q11(b)', CALVING_RATE, [2, 2], '2(2)', 'Any two ways from the published pool, 2 marks each.',
         16, 19, '"Briefly explain ways Tim can achieve the 6-week calving rate target of 80%", one pool of eight ways')
    for k, ref in [('q12a', 'Q12(a)'), ('q12b', 'Q12(b)'), ('q12c', 'Q12(c)'), ('q12d', 'Q12(d)')]:
        keep(k, ref)
    # Section B ---------------------------------------------------------------
    factor_options = list(SOIL_FACTORS) + list(SOIL_FACTORS.values())
    fix('q13ai', 'Q13(a)(i)', dict(
        rows=[menu(factor_options, [5, 5, 2, 2],
                   'Two factors, each named with its description: four answers in all. The scheme prints 5+5+2+2. ' + PAGE4 + ' The first five options are the scheme\'s factors and the last five their descriptions, in the same order; a description counts only for a factor you named.')],
        tariffModel={'kind': 'fixed', 'notation': '5+5+2+2'}), drop=('notes',),
        correction=('Visually verified paper PDF page 20 ("Describe two factors that are involved in the formation of soil", a Factor and Description table with two rows) and scheme PDF page 20 (five factors with descriptions, "5+5+2+2") with its PDF page 4 rule that "the first correct answer encountered" earns the first mark and each later correct answer the next. '
                    'The original priced each factor-and-description pair at 7 or nothing and told students the description was worth 5 and the name 2, a split the scheme never prints. '
                    'Same ID, boundary and 14 marks; the four answers earn 5, 5, 2 and 2 in the order they are correct.'))
    fix('q13aii', 'Q13(a)(ii)', dict(
        rows=[point('Elements of diagram: O or organic matter / A or topsoil / B or subsoil / C or bedrock or parent material / iron pan (or zone of accumulation) present in B = 6 marks', None,
                    'Drawing, D = 0, 3 or 6: one element missing = 3 marks; two or more elements missing = 0 marks.', kind='criterion'),
              point('Any three labels = 3(2) marks', None, 'Labels, L = 3 x 2.')],
        tariffModel={'kind': 'questionTotal', 'notation': 'D = 0,3,6 + L = 3 x 2'}), drop=('notes',),
        correction=('Visually verified paper PDF page 20 ("Draw a labelled diagram of a podzol soil profile", a blank diagram box) and scheme PDF page 20 (the five elements = 6 marks, one missing = 3, two or more missing = 0, any three labels = 3(2); "D = 0,3,6 L = 3 x 2"). '
                    'The original split the five elements into five unpriced rows under a first-correct tariff, which the session reads as "the first correct answers earn more"; the drawing is banded, not ranked. '
                    'Same ID, boundary and 12 marks; one drawing criterion and one labels criterion judged against the published total.'))
    keep('q13bi', 'Q13(b)(i)')
    fix('q13bii', 'Q13(b)(ii)', dict(
        rows=[point('Field capacity — Plants can remove water from the soil easily or water available to plant or land is usable or land is easily cultivated or conditions are suitable for growth', None,
                    'Any two of the three: the first correct implication earns 2 marks and the second 1 (2+1).'),
              point('Saturation — Excess water (lack of air spaces) can reduce crop growth or waterlogged or easily poached or roots cannot respire, or no earthworms or drainage required to reduce waterlogging', None),
              point('Permanent wilting point — Lack of water so plants can no longer extract water from the soil or irrigation necessary or reduced yield or delayed growing season or wind erosion of soil', None)]),
        drop=('notes',), selection=closed(2, ['Field capacity', 'Saturation', 'Permanent wilting point']),
        correction=('Visually verified paper PDF page 21 ("Briefly describe the implications for a farmer of any two of the following", Field capacity, Saturation, Permanent wilting point) and scheme PDF page 21 (one answer per state, "2+1"). '
                    'The original rows were cut where the marks cell interrupts the extracted text ("or easily" was lost from Saturation and Permanent wilting point began mid-list). '
                    'Same ID, boundary, any-two-of-three tariff and 3 marks; each row is the whole published answer for its state.'))
    lab = dict(menu(LAB, [4, 4, 4], 'Laboratory method: any three points, 4 marks each (3(4)). The scheme stars the timing step: "record time taken for water to flow into beakers or record volume for filtrate (for set time)" is compulsory.'), id='r-1')
    field = dict(menu(FIELD, [4, 4, 4], 'OR FIELD METHOD: any three points, 4 marks each (3(4)). The scheme stars "record time taken for water to drain down through tube" as compulsory.'), id='r-1')
    fix('q13c', 'Q13(c)', dict(
        rows=[lab], answerVariants=[dict(id='laboratory', label='Laboratory method', rows=[lab]), dict(id='field', label='Field method', rows=[field])],
        tariffModel={'kind': 'fixed', 'notation': '3(4)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 22 ("Describe with the aid of a labelled diagram how a farmer would carry out an investigation to compare the drainage (infiltration) rate of a podzol and a brown earth soil sample and outline the expected result") '
                    'and scheme PDF page 21 (a laboratory method of six points "OR FIELD METHOD" of five, "3(4)", with one compulsory point in each). The original listed five of the laboratory points and described the field method only in a note. '
                    'Same ID, boundary and 12 marks; the two methods are official answer routes the student chooses before reveal, each listing every published point, any three at 4 marks.'))
    keep('q13di', 'Q13(d)(i)')
    fix('q13dii', 'Q13(d)(ii)', dict(
        rows=[menu(MOISTURE, [4, 2], 'Two functions: the first correct earns 4 marks and the second 2 (4+2).')],
        tariffModel={'kind': 'fixed', 'notation': '4+2'}), drop=('notes',),
        correction=('Visually verified paper PDF page 23 ("State the functions of soil moisture (water)") and scheme PDF page 21 (nine functions, "4+2"). '
                    'The original showed five of the nine and left chemical reactions, transpiration, microbial activity and soil structure out. '
                    'Same ID, boundary and 6 marks; one row lists all nine, the first correct at 4 and the second at 2.'))
    keep('q14a', 'Q14(a)')
    keep('q14bi', 'Q14(b)(i)')
    keep('q14bii', 'Q14(b)(ii)')
    fix('q14biii', 'Q14(b)(iii)', dict(
        rows=[menu(CLOVER, [5, 1], 'Two advantages: the first correct earns 5 marks and the second 1 (5+1).')],
        tariffModel={'kind': 'fixed', 'notation': '5+1'}), drop=('notes',),
        correction=('Visually verified paper PDF page 24 ("Outline the advantages of sowing clover with the oilseed rape") and scheme PDF page 22 (six advantages, "5+1"). '
                    'The original left "improve soil function" out. Same ID, boundary and 6 marks; one row lists all six, the first correct at 5 and the second at 1.'))
    old_biv = originals[PREFIX + 'q14biv']
    assert old_biv['stem'].endswith("(The underlined term here is 'annual'.)")
    fix('q14biv', 'Q14(b)(iv)', dict(stem=old_biv['stem'].replace("'annual'.)", "'annual plant'.)")),
        correction=('Visually verified paper PDF page 25: the paper underlines "annual plant" in "Berseem clover is an annual plant", and scheme PDF page 22 heads the answer "Explain annual plant." '
                    'The original stem said the underlined term was "annual". Same ID, rows, boundary and 3 marks.'))
    keep('q14bv', 'Q14(b)(v)')
    fix('q14ci', 'Q14(c)(i)', dict(
        rows=[menu(PLANT_COUNT, [4, 4, 4], 'Any three steps, 4 marks each (3(4)).')],
        tariffModel={'kind': 'fixed', 'notation': '3(4)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 25 ("Describe how to carry out a plant count in a 2 hectare field") and scheme PDF page 22 (six steps, "3(4)"). '
                    'The original left "repeat (at least 10 times)" out. Same ID, boundary and 12 marks; one row lists all six steps, any three at 4 marks.'))
    fix('q14cii', 'Q14(c)(ii)', dict(
        rows=[menu(COUNT_ADVANTAGES, [5, 1], 'Two advantages: the first correct earns 5 marks and the second 1 (5+1).')],
        tariffModel={'kind': 'fixed', 'notation': '5+1'}), drop=('notes',),
        correction=('Visually verified paper PDF page 26 ("Briefly explain advantages of carrying out a plant count in a newly sown or reseeded field") and scheme PDF page 22 (five advantages, "5+1"). '
                    'The original left "correct fertiliser amount used" out. Same ID, boundary and 6 marks; one row lists all five, the first correct at 5 and the second at 1.'))
    keep('q14ciii', 'Q14(c)(iii)')
    keep('q14civ', 'Q14(c)(iv)')
    texture = [('hand', 'Hand method', HAND, 'Hand method: any three points, 4 marks each (3(4)).'),
               ('sediment', 'Sediment method', SEDIMENT, 'Or Sediment method: any three points, 4 marks each (3(4)).'),
               ('sieve', 'Sieve method', SIEVE, 'Or Sieve method: any three points, 4 marks each (3(4)).')]
    variants = [dict(id=v, label=label, rows=[dict(menu(options, [4, 4, 4], note), id='r-1')]) for v, label, options, note in texture]
    fix('q15a', 'Q15(a)', dict(
        rows=variants[0]['rows'], answerVariants=variants,
        tariffModel={'kind': 'fixed', 'notation': '3(4)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 27 ("Describe how they carried out this investigation to determine the soil texture") and scheme PDF page 23 (a hand, "Or" sediment and "Or" sieve method, "3(4)"). '
                    'The original listed five hand-method points and described the sediment and sieve methods only in a note. '
                    'Same ID, boundary and 12 marks; the three methods are official answer routes the student chooses before reveal, each listing every published point, any three at 4 marks.'))
    for k, ref in [('q15bi', 'Q15(b)(i)'), ('q15bii', 'Q15(b)(ii)')]:
        keep(k, ref)
    fix('q15biii', 'Q15(b)(iii)', dict(
        rows=[menu(LIMING, [5, 2], 'Two benefits: the first correct earns 5 marks and the second 2 (5+2).')],
        tariffModel={'kind': 'fixed', 'notation': '5+2'}), drop=('notes',),
        correction=('Visually verified paper PDF page 28 ("Farmers can improve the soil quality by liming to adjust the soil pH level. Briefly describe other benefits of liming the soil") and scheme PDF page 23 (five benefits, "5+2"). '
                    'The original left "grass is more palatable to livestock" out. Same ID, boundary and 7 marks; one row lists all five, the first correct at 5 and the second at 2.'))
    keep('q15ci', 'Q15(c)(i)')
    fix('q15cii', 'Q15(c)(ii)', dict(
        stem='A secondary school recently designed and installed a new school garden and polytunnel. Analyse the graph showing the effect soil pH has on nitrous oxide (N20) emissions and answer the questions which follow.',
        questionText='Discuss the relationship between pH and N20 emissions on the graph and its implications for ongoing farming practice.',
        figureKey='agricultural-science-2023-HL-paper-p28-i0',
        rows=[point('The higher the soil pH the lower the N20 emissions', 5, 'The relationship, 5 marks.'),
              point('(Farmers should test their soil pH and) add lime to increase the pH levels to as close to neutral as possible to reduce the N20 emissions which is better for the environment and more sustainable', 3,
                    'The implication for farming practice, 3 marks.')]),
        drop=('notes',),
        correction=('Visually verified paper PDF page 28 and page 29 ("Analyse the graph showing the effect soil pH has on nitrous oxide (N20) emissions", the bar chart, then "Discuss the relationship between pH and N20 emissions on the graph and its implications for ongoing farming practice") '
                    'and scheme PDF page 23 (relationship 5, implication 3). The original stem was the chart\'s axis labels run together, the first answer began with the question\'s own words '
                    '"its implications for ongoing farming practice." and the second stopped before "which is better for the environment and more sustainable". '
                    'Same ID, boundary and 8 marks; the stem is the paper\'s own lead-in, the card shows the inspected chart and each row is the whole published answer.'))
    keep('q15d', 'Q15(d)')
    keep('q16ai', 'Q16(a)(i)')
    fix('q16aii', 'Q16(a)(ii)', dict(
        stem=("Answer both (a) and (b) with either (c) or (d). As part of the governments’ climate action plan targets, agriculture has to reduce its greenhouse gas emissions by 25% by 2030. "
              'Anna and Lucy examined the percentage share of the carbon emissions from their beef enterprise which they received through their Bord Bia farmer feedback report. '
              'The graph highlights where the emissions are coming from on their farm. Analyse the graph and answer the questions which follow.'),
        figureKey='agricultural-science-2023-HL-paper-p30-i0',
        rows=[point('Below', 5, 'State: 5 marks.'),
              dict(point('As the average for the enterprise is over 40%', 1, 'Reason: 1 mark (5+1).'), kind='alt', accepts=['is less for the current and previous assessments'])]),
        correction=('Visually verified paper PDF page 30 (the lead-in, the grouped bar chart, then "State with reason if the main source of emissions is above or below the national average for the enterprise") '
                    'and scheme PDF page 24 ("Below", "As the average for the enterprise is over 40% / is less for the current and previous assessments", 5+1). '
                    'The original stem was the chart\'s legend and axis labels run together, with no chart, and the second published reason was missing. '
                    'Same ID, boundary and 6 marks; the stem is the paper\'s own wording, the card shows the inspected chart and the reason row accepts both reasons.'))
    for k, ref in [('q16aiii', 'Q16(a)(iii)'), ('q16bi', 'Q16(b)(i)'), ('q16bii', 'Q16(b)(ii)'), ('q16c', 'Q16(c)'), ('q16di', 'Q16(d)(i)'), ('q16dii', 'Q16(d)(ii)'),
                   ('q17ai', 'Q17(a)(i)'), ('q17aii', 'Q17(a)(ii)'), ('q17bi', 'Q17(b)(i)'), ('q17bii', 'Q17(b)(ii)')]:
        keep(k, ref)
    keep('q17biii', 'Q17(b)(iii)', selection=closed(2, ['A', 'B', 'C']))
    keep('q17c', 'Q17(c)', selection=closed(1, ['sexually', 'asexually']))
    jenny = ('Jenny and John are farming a 230 cow dairy farm in Co. Cork. They are looking at the overall quality of their milk and in particular '
             'the somatic cell count (SCC) figures from their recent milk report.')
    letters = list(UDDER)
    q18ai = add('q18ai', 'Q18(a)(i)', '4-1', 'udder-structure', 'Label any three parts of the structure of the udder.',
                [menu(list(UDDER.values()), [1, 1, 1], 'Any three of the four labels, 1 mark each (3(1)). Options in letter order: A, B, C, D.')],
                jenny, selection=closed(3, letters), figure='agsci-2023-hl-paper-udder',
                labels=[dict(letter=l, meaning=f'{UDDER_ARROWS[l]} ({UDDER[l]})', askedInThisQuestion=True) for l in letters])
    q18ai['rows'][0]['id'] = 'labels'  # the row id this card has always shipped with
    for k, ref in [('q18aii', 'Q18(a)(ii)'), ('q18aiii', 'Q18(a)(iii)'), ('q18aiv', 'Q18(a)(iv)')]:
        keep(k, ref)
    add('q18av', 'Q18(a)(v)', '4-3-3', 'california-mastitis-test-order',
        'Jenny tested the milk quality from various samples of milk to see which cow had high SCC using the cow side California Mastitis Test (CMT). '
        'The steps involved in carrying out the test are shown in the table. Assist Jenny in placing each step in the correct order by matching the correct letter to the number in the box.',
        [point(f'{n} {l}', 2, f'Step {n}: {l}, "{CMT[l]}".' + (' 2 marks for each step in its correct box (4(2)).' if n == 1 else '')) for n, l in ((1, 'A'), (2, 'D'), (3, 'B'), (4, 'C'))],
        jenny, figure='agsci-2023-hl-paper-cmt-steps',
        labels=[dict(letter=l, meaning=CMT[l], askedInThisQuestion=True) for l in CMT])
    keep('q18bi', 'Q18(b)(i)')
    fix('q18bii', 'Q18(b)(ii)', dict(
        rows=[menu(list(MILK_FACTORS), [3, 3, 3], 'Three factors, 3 marks each (F:3(3)). The scheme adds: "Maximum two matching points (factor + describe) from any one category and third factor from another category".'),
              dict(menu(list(MILK_FACTORS.values()), [3, 3, 3],
                        'A description of each of the same three factors, 3 marks each (D:3(3)). In order the options describe cow health, somatic cell counts, diet, milk handling or storage, milk hygiene and breed or genetics.'),
                   openList=True)],
        tariffModel={'kind': 'fixed', 'notation': 'F:3(3) + D:3(3)'}), drop=('notes',),
        correction=('Visually verified paper PDF page 39 ("Describe the factors you would be looking for in your inspection", a Factors and Description table with three rows) and scheme PDF page 28 (six factor categories with descriptions, "F:3(3) + D:3(3)"). '
                    'The original priced each factor-and-description pair at 6 or nothing, so a correctly named factor with a weak description could not earn its 3. '
                    'Same ID, boundary and 18 marks; three factors at 3 marks each and three matching descriptions at 3 marks each.'))
    assert len(tasks) == 85 and len(cards) == 28 and len(corrections) == 24 and len(originals) == 81, (len(tasks), len(cards), len(corrections), len(originals))
    assert {t['cardIds'][0] for t in tasks} >= set(originals), 'Every original 2023 Higher card must be reviewed'
    assert q18ai['id'] == PREFIX + 'q18ai'
    return cards, tasks, corrections
