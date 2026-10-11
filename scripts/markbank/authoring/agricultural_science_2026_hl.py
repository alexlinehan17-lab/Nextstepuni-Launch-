"""2026 Higher tasks from the complete original paper/scheme review.

All 44 paper pages and 33 scheme pages were inspected before authoring; the
independent census in agricultural_science_census.py was transcribed first.
Three printed finite pools expand mechanically (Q2(b) three of four headings,
Q7 four of six benefits, Q10(a) two of three plants) and two printed either/or
choices become one route each (Q14(c)(i) method A or B, Q18(c)(iii) plants or
animals). Open examples stay coherent answer menus.
"""
from itertools import combinations
from agricultural_science_2010_hl import point, menu, region
from agricultural_science_2010_parity import scan
from agricultural_science_2011_hl import variants

FILE = 'LC024ALP000EV.pdf'
YEAR = 2026
HASHES = {'exampapers':'900dc33c639e740c3e50079caa34400ff62ada89418cc677142eec53335fd990',
          'markingschemes':'efc3a2aa5656657aaec9364c23caf927f47078ecd622976e97b10628f8ecf6a6'}
SELECTIONS = {
    'babe7659cb22db72':('exam-selection','Section A: ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'e8c019ae0b41ecb7':('exam-selection','Section B: four of six independent questions. Every question is retained.'),
    '7432b25456cb2ca8':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    '9707f8e403d3e354':('independent-task-selection','Q2 either (a) or (b): both independently marked alternatives are retained at their own addresses.'),
    'dede8045c702dde8':('closed','Q2(b) prints four headings and asks for any three: all four three-heading routes are retained at 10 marks each.'),
    '1dbe2dc4871a9fc0':('independent-task-selection','Q3 either (a) or (b): both alternatives are retained.'),
    '814a14887d2c6953':('not-a-selection','Prose in the Q5 stem ("one of the most costly"); no response choice.'),
    'cf26516051e681aa':('independent-task-selection','Q6 either (a) or (b): both alternatives are retained.'),
    '6dac7ebdeb2a6e5c':('closed','Q7 prints six benefits and asks for any four: all fifteen four-benefit routes are retained at 10 marks each.'),
    '00f8ddba32153c18':('closed','Q10(a) prints plants A, B and C and asks for any two: all three two-plant routes are retained at 5 marks each.'),
    '66628fc3651b1157':('independent-task-selection','Q11 either (a) or (b): both alternatives are retained.'),
    'f726bead2abb20bc':('not-a-selection','Q12(a) uses "select" for breeding selection of traits; the two traits are open, not a printed pool.'),
    '246c040a8fc33fc0':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    'd2c81f14fad6809d':('independent-task-selection','Q14: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '4a520afd30e05775':('independent-task-selection','Q16: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
}
SUPPLEMENTARY = [
    (26,'Identify method A or B','closed','Q14(c)(i): a printed choice between photographs A and B. Both routes are retained, each with its own name and method menu.'),
    (39,'plants or animals','closed','Q18(c)(iii): a printed choice between plants and animals. Both routes are retained with their own scheme menus.'),
    (8,'Name one other mineral','open','Q4(c): any suitable mineral; the scheme examples are matching name/reason menus, not a printed pool.'),
    (31,'Describe three stages of grass growth','open','Q16(a)(i): the stages are student-generated; the scheme lists four described stages as a marking menu.'),
    (36,'profitability and/or environmental footprint','open','Q17(a)(v): flexible and/or wording; one combined menu, not fanned out.'),
    (16,'two features of good animal housing','open','Q11(a)(i): two features chosen by the student from an open field; no printed pool.'),
    (37,'identify whether the following statements are true or false','answer-identification','Q17(b)(ii): each statement has one correct answer; every statement is required.'),
    (21,'Identify the meaning of a nutrient','answer-identification','Q13(a)(i): tick the one correct definition; the other boxes are distractors, not routes.'),
]
SOURCE_NOTES = {
    'q11bi':'The scheme heading asks for “the straw bedded floor space and feed space”, but the examination paper asks only for the straw bedded floor space. The published answer and its 2+2 marks concern floor space alone (4 x 40 = 160 m2).',
    'q17aiv':'The scheme’s descriptors print 3 marks each for scale, plotted data and line, but its mark column prints 4+4+3 = 11, which is the allocation needed for Question 17 to total 50. The card keeps the 11-mark manual total.',
}


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    refs = {'q11bi':('11','Q11(b)(i)'), 'q17aiv':('17','Q17(a)(iv)')}
    notes = [dict(questionN=refs[key][0], questionRef=refs[key][1], note=note) for key, note in SOURCE_NOTES.items()]
    return dict(year=YEAR, level='higher', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 45)), schemePagesInspected=list(range(1, 34)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=notes,
                independentBoundaryReview='91 base tasks and 112 routes. Q2(b) three-of-four (4 routes), Q7 four-of-six (15), Q10(a) two-of-three (3), Q14(c)(i) A or B (2) and Q18(c)(iii) plants or animals (2). First-correct scales stay whole; drawings, the graph and the two-field fertility comparison keep manual question-total marking.',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected; the scheme reproductive-system solution image inspected.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


def reviewed_tasks():
    paper_review()
    cards, tasks = [], []

    def add(key, ref, topic, atlas, concept, question, rows, pp, sp, stem=None, marks=None, selection=None, figure=None, extra=()):
        cid = 'agsci-2026-hl-' + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='higher',
                    section='A' if int(ref.split('(')[0].split()[0][1:]) <= 12 else 'B',
                    questionRef='2026 HL ' + ref, topicId='agsci-' + topic,
                    curriculumNodeIds=['agsci-' + t for t in (topic, *extra)],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel={'kind': 'questionTotal' if marks is not None else 'fixed'},
                    sourceMaterial=dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2026 Higher — ' + ref,
                        pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2026 Higher Level examination paper — © State Examinations Commission.',
                        presentationNote='Open the original page for the published wording, photographs, tables and examination context.'))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        task = dict(questionRef=card['questionRef'], paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                    atlasNumbers={cid: str(1001 + len(cards))}, cardIds=[cid], marksPerRoute=card['totalMarks'],
                    examTopicIds=['agricultural-science-higher-' + t for t in atlas.split('|')],
                    selection=selection or {'kind': 'none', 'reason': 'Required response. Open examples and scheme alternatives remain marking menus, not finite printed routes.'},
                    evidence='All 44 paper and 33 scheme pages visually inspected. Published task boundaries and awards independently transcribed before authoring.')
        if key in SOURCE_NOTES:
            task['schemeNote'] = SOURCE_NOTES[key]
            rows[0]['contextNote'] = (rows[0].get('contextNote', '') + ' ' + SOURCE_NOTES[key]).strip()
        cards.append(card); tasks.append(task)
        return card

    # Section A ---------------------------------------------------------------
    q1 = 'Irish weather conditions can prove a challenge to crop production, resulting in shorter working windows and the need to use large machines. Analyse the photograph and answer the questions that follow.'
    ways = [('tracks', '(wider) Tracks', 'Reduced Soil Compaction or weight spread over a larger surface area or reduced poaching'),
            ('fuel', 'Lower fuel consumption / GPS', 'Less energy (fuel) to pull heavy equipment or reducing carbon emissions or fewer passes'),
            ('movement', 'Smoother, more even movement', 'Causes less disturbance to soil organisms or reduces erosion risk')]
    c = add('q1a', 'Q1(a)', '2-3', 'crop-production', 'environmentally-friendly-machinery',
        'Briefly explain with reason one way the machine above is environmentally friendly.',
        [menu([ways[0][1], ways[0][2]], [5, 3])], [region(3, .155, .522), region(3, .53, .62)], [region(12, .118, .326)], q1, extra=('3-3-1',))
    variants(c, [(k, way, [menu([way, reason], [5, 3], 'Way and matching reason. The first correct field earns 5 marks and the second 3.')]) for k, way, reason in ways])
    add('q1b', 'Q1(b)', '3-3-1', 'crop-production', 'large-machinery-drawbacks', 'Identify one negative for using this large machine.',
        [menu('High maintenance or costs or emissions|safety issues or described|limited manoeuvrability|will not fit on all farms or roads', [2])],
        [region(3, .155, .522), region(3, .72, .745)], [region(12, .326, .409)], q1)

    add('q2ai', 'Q2(a)(i)', '3-1', 'plant-physiology', 'photosynthesis-structures', 'Outline the role of two named plant structures in photosynthesis.',
        [menu(['Leaf', 'Absorbing light / take in CO2 / combine them with water to make glucose', 'Chloroplasts/ palisade layer', 'Contain chlorophyll which is used to trap light',
               '(Spongy) Mesophyll', '(Layer of leaf cells) allows diffusion', 'Stomata', '(Pores) that absorb CO2 or release O2 or gas exchange',
               'Root', 'Absorb water (from soil)', 'Vascular bundle or xylem or phloem', '(Xylem) which transport water or (phloem) which transports food'], [3, 3, 1, 1],
              'Two named structures, each with its matching role. The scheme prints 2(3)+2(1): the first two correct fields earn 3 marks each and the next two 1 each.')],
        [region(4, .065, .195)], [region(12, .409, .713)], 'Photosynthesis is fundamental to agriculture.')
    add('q2aii', 'Q2(a)(ii)', '3-1', 'plant-physiology', 'photosynthesis-carbon-cycle', 'Briefly describe one role photosynthesis contributes to the carbon cycle.',
        [menu(['Plants absorb CO2 from the atmosphere which they use to combine with water to make glucose, (using energy)',
               'Carbon Sequestration – capture atmospheric carbon into plant tissues and soils to help regulate climate change'], [2], 'One role.')],
        [region(4, .065, .112), region(4, .47, .596)], [region(12, .713, .852)], 'Photosynthesis is fundamental to agriculture.', extra=('2-2-3',))
    headings = {
        'fertilising': ('Fertilising the crop', 'Provides nutrients (e.g. N, P, K) to enhance leaf growth/area or provides N for chlorophyll production or correct mineral function related to photosynthesis'),
        'light': ('Optimising light capture', 'Sow crops in rows / correct spacing to maximise sunlight / avoid shading /aspect described / time of sowing to maximise daylength (growth days) / relevant genetic selection for enhanced light capture'),
        'genetic': ('Genetic improvement of crops', '(Breeding) genetically selecting crops for traits (like faster growth or larger surface area or higher chlorophyll content, or drought resistance) leads to increased photosynthesis or crop yields'),
        'grassland': ('Grassland management', 'Management of grazing system (stocking rate or reseeding or topping or rotation) to increase leaf growth / increase sugar content for silage or grazing.'),
    }
    for chosen in combinations(headings, 3):
        labels = [headings[k][0] for k in chosen]
        add('q2b-route-' + '-'.join(chosen), 'Q2(b) — ' + ', '.join(labels), '3-1', 'plant-physiology|crop-production', 'photosynthesis-crop-production',
            'Discuss how the knowledge of photosynthesis is used to enhance crop production on Irish farms. In your answer, refer to any three of the following:',
            [menu([headings[k][1] for k in chosen], [5, 3, 2],
                  'One point under each of your three headings, in order: ' + '; '.join(labels) + '. Alternatives within one heading earn one award. The first correct heading earns 5 marks, the second 3 and the third 2.')],
            [region(5, .065, .295)], [region(13, .066, .467)], 'Practice choice: ' + ', '.join(labels) + '.',
            selection={'kind': 'closed', 'choose': 3, 'options': list(headings), 'route': list(chosen)}, extra=('3-3-2',))

    q3a = ('Teagasc have confirmed the first reported case of a field population of Italian ryegrass which has proven resistant to the chemical herbicide glyphosate. '
           'Italian ryegrass is already a major challenge on some Irish tillage farms, with some populations resistant to selective herbicides used in crops. (Adapted from Teagasc, 2025)')
    add('q3ai', 'Q3(a)(i)', '3-3-2', 'crop-production', 'herbicide-resistance', 'Explain the underlined term.',
        [point('The ability of an organism to remain unaffected by any factor (herbicide)', 2)],
        [region(6, .065, .31)], [region(13, .467, .533)], q3a + ' [The term underlined on the paper is: resistant]')
    add('q3aii', 'Q3(a)(ii)', '3-3-2', 'crop-production', 'italian-ryegrass-challenge', 'Outline why Italian ryegrass would be a challenge on Irish tillage farms.',
        [menu('High seed production|herbicide resistance|similar growth habits to cereals|seeds stay in soil for long periods|long germination periods|competition for resources|crop contamination', [2])],
        [region(6, .065, .245), region(6, .437, .462)], [region(13, .533, .616)], q3a)
    add('q3aiii', 'Q3(a)(iii)', '3-3-2', 'crop-production', 'non-chemical-weed-control', 'Describe two ways farmers could control weeds on tillage farms without the use of herbicides.',
        [menu(['Mechanical or cultural control such as ploughing or harrowing or rogueing to disrupt growth cycle of weeds', 'crop rotation involving sowing a variety of crops breaks lifecycle of weeds',
               'later sowing date allow weeds to germinate then cultivate lightly', 'competitive seed varieties are fast establishing varieties which shade out weeds',
               'higher seed rates more competition for light or nutrients or space', 'min-till or direct drilling as to not disturb weed seed reservoir or machine hygiene to prevent transfer of weed seed',
               'described biological control', 'certified seed with reference to high germination rate or high purity or free from wild oats'], [5, 1])],
        [region(6, .065, .245), region(6, .561, .603)], [region(13, .616, .875)], q3a)
    q3b = ('Sarah has identified wild oats as a weed in her ripe barley field as shown in the photograph below. She carried out an assessment close to harvest using a scorecard to determine the extent of the problem. '
           'Analyse the information and answer the questions that follow.')
    add('q3bi', 'Q3(b)(i)', '3-3-2', 'crop-production', 'weed-score-card',
        'Using the weed score card above, determine the weed score (1 - 3) in Sarah’s field shown in the photograph below and justify your answer.',
        [point('Weed score – 2', 2, 'Score.'), point('Justification – there are few patches of wild oats present, but they are sparse', 2, 'Justification.')],
        [region(7, .065, .685)], [region(14, .083, .182)], q3b, extra=('1-3',))
    add('q3bii', 'Q3(b)(ii)', '3-3-2', 'crop-production', 'wild-oat-control', 'Advise suitable weed control measures Sarah could implement on her farm.',
        [menu('Certified seed|hand rogueing|mechanical control|delayed sowing|competitive crops|good machine hygiene|crop rotation|min-till or direct drilling|stubble cleaning|creation of sterile seedbed', [5, 1])],
        [region(7, .09, .31), region(7, .72, .745)], [region(14, .182, .301)], q3b)

    q4 = ('As the calving season progresses on dairy farms, the risk of milk fever and metabolic issues increases. This is because later-calving cows tend to be older and are at high risk of being too high in body condition due to longer days dry. '
          'Attention to detail on feeding dry cow minerals may also have slipped, as the farm is now very busy with calves, milking and grassland management. (Adapted from Farmers Journal, 2025)')
    add('q4a', 'Q4(a)', '4-3-3', 'animal-diseases|dairy-cattle', 'milk-fever', 'Explain the underlined term.',
        [point('Metabolic disorder caused by low blood calcium levels', 2)], [region(8, .065, .297)], [region(14, .301, .349)],
        q4 + ' [The term underlined on the paper is: milk fever]')
    add('q4b', 'Q4(b)', '4-3-3', 'animal-diseases|dairy-cattle', 'milk-fever-signs', 'Describe one clinical sign or symptom of milk fever in cows.',
        [menu(['Staggering - cow has difficulty walking, may collapse', 'loss of appetite - reduced feed intake', 'cold ears or low body temperature - poor circulation due to muscle failure',
               'lying down and unable to rise - paralysis caused by nerve malfunction', 'reduced rumen activity - leads to poor digestion'], [2])],
        [region(8, .065, .276), region(8, .425, .45)], [region(14, .349, .485)], q4)
    minerals = [('magnesium', 'Magnesium', "Essential for the cow's ability to absorb and metabolise calcium or prevent grass tetany or milk fever"),
                ('phosphorus', 'Phosphorus', 'Supports bone development or energy or metabolism or appetite'),
                ('selenium', 'Selenium', 'Boosts immunity or reduces retained placenta risk or improve fertility')]
    c = add('q4c', 'Q4(c)', '4-3-3', 'animal-diseases|dairy-cattle', 'dry-cow-minerals',
        'The mineral content of a dry cow diet is designed to be low in calcium, in order to allow the cow mobilise her own calcium reserves. Name one other mineral added to the diet of dry cows and give a reason for its inclusion in the diet.',
        [menu(list(minerals[0][1:]), [5, 1])], [region(8, .065, .276), region(8, .58, .717)], [region(14, .485, .681)], q4)
    variants(c, [(k, name, [menu([name, reason], [5, 1], 'Named mineral and matching reason. The first correct field earns 5 marks and the second 1.')]) for k, name, reason in minerals])

    q5 = ('Lameness is one of the most costly and challenging issues in dairy farming, costing on average €8,750 per annum for a 100-cow herd in 2024. Artificial intelligence (AI) powered smart technology has emerged '
          'which uses camera and vision technology to assess and monitor cows’ movement and can detect early signs of lameness.')
    add('q5a', 'Q5(a)', '4-3-3', 'animal-diseases|dairy-cattle', 'lameness-causes', 'Outline two causes of lameness in dairy cows.',
        [menu(['Sole ulcers pressure on sole of foot or standing on concrete or poor cubicle comfort or foreign object or extensive walking to paddocks', 'laminitis – feeding high concentrate or high energy diets (weaken hoof structure)',
               'sudden change in diet (rumen acidosis)', 'foot rot or bacterial infection (standing in wet or dirty conditions)', 'overgrown hooves or uneven weight bearing or digital dermatitis in hoof'], [3, 1])],
        [region(9, .065, .592)], [region(15, .066, .218)], q5)
    add('q5b', 'Q5(b)', '4-3-3', 'animal-diseases|dairy-cattle', 'lameness-prevention', 'Outline one-way lameness can be prevented.',
        [menu('Regular hoof trimming|foot baths|good hygiene|comfortable cow accommodation or roadways|balanced nutrition|minimise walking distance', [3])],
        [region(9, .065, .178), region(9, .625, .65)], [region(15, .218, .301)], q5)
    add('q5c', 'Q5(c)', '4-3-3', 'animal-diseases|dairy-cattle', 'lameness-costs', 'Explain why lameness is costly on dairy farms.',
        [menu('Decreased production (reduced milk yield or poor live weight gain)|reduced fertility (poor heat detection or increased calving intervals)|increased culling rates|high treatment or labour costs (higher AI or veterinary costs)', [3])],
        [region(9, .065, .178), region(9, .742, .766)], [region(15, .301, .401)], q5, extra=('4-3-1',))

    q6a = ('A relatively new challenge on Irish farms is the blood sucking Barber’s Pole worm. It is very efficient at reproducing, with faecal egg counts in excess of 5,000 eggs per gram, in a short period of time. '
           'Symptoms in animals are very like those of liver fluke. The picture shows the lifecycle of the worm. Analyse the picture and answer the questions that follow.')
    add('q6ai', 'Q6(a)(i)', '4-3-3', 'animal-diseases|sheep', 'faecal-egg-count', 'Explain the underlined term.',
        [point('Quantitative measure of how many worm eggs in sheep or cattle is passing in each gram of its manure', 2)],
        [region(10, .065, .558)], [region(15, .401, .467)], q6a + ' [The term underlined on the paper is: faecal egg counts]')
    add('q6aii', 'Q6(a)(ii)', '4-3-3', 'animal-diseases|sheep', 'endoparasite-ectoparasite',
        'Identify whether the parasite is an endoparasite or ectoparasite by placing a tick (✓) in the correct box.',
        [point('Endoparasite', 4, 'The scheme ticks Endoparasite.')], [region(10, .09, .525), region(10, .626, .72)], [region(15, .467, .516)], q6a)
    add('q6aiii', 'Q6(a)(iii)', '4-3-3', 'animal-diseases|sheep', 'barbers-pole-worm-control',
        'Apart from chemical control, outline two ways a farmer could control or prevent this worm spreading.',
        [menu(['Rotational Grazing - prevents lambs grazing heavily contaminated paddocks where larvae build up', 'mixed grazing - graze sheep after cattle or horses as do not host barber pole worm',
               'clean pasture - use silage ground or reseeded paddocks', 'quarantine of bought-in animals or maintain closed herd - prevents introducing resistant worm strains',
               'breeding for resistance', 'select breeding stock that show natural resistance (good body condition, low FEC)', 'nutrition or health management - provide adequate protein and minerals',
               'healthy sheep are better able to withstand infection', 'sow or graze multispecies sward'], [3, 1])],
        [region(10, .09, .525), region(10, .728, .771)], [region(15, .516, .759)], q6a)
    q6b = ('The Barber’s pole worm is normally found in warm climates. Incidence from the Regional Veterinary Lab (RVL) have shown it in Ireland with the highest number of cases in the southeast and midlands. '
           'Analyse the graph and answer the questions that follow.')
    add('q6bi', 'Q6(b)(i)', '4-3-3', 'animal-diseases|sheep', 'parasite-incidence-trend', 'Identify the trend in incidence of the worm on Irish farms.',
        [point('The incidence of barber pole in increasing rapidly in recent years', 4)], [region(11, .065, .516)], [region(16, .083, .131)], q6b, extra=('1-3',))
    add('q6bii', 'Q6(b)(ii)', '4-3-3', 'animal-diseases|sheep', 'parasite-incidence-reason', 'Outline one reason for the trend identified in part (i) above.',
        [point('As Ireland’s climate is getting milder, the incidence of barber pole worm in increasing', 2)],
        [region(11, .09, .495), region(11, .581, .605)], [region(16, .131, .197)], q6b, extra=('1-3',))
    add('q6biii', 'Q6(b)(iii)', '4-3-3', 'animal-diseases|sheep', 'anthelmintic-resistance',
        'Anthelmintic resistance is becoming an issue in its control. Outline two practices a farmer could follow to reduce the risk of anthelmintic resistance developing.',
        [menu('Weigh animals to ensure accurate weight for accurate dosage rates|only treat animals that require treatment (selective treatment)|use different groups of worm doses|isolate bought in animals|carryout out faecal egg count|good grassland management', [3, 1])],
        [region(11, .09, .19), region(11, .69, .752)], [region(16, .197, .333)], q6b)

    benefits = {
        'pests': ('Protection from pests and diseases', 'Diverse farming systems encourage beneficial organisms / natural predators control pests, (reducing the need for pesticides) / healthy soils suppress plant diseases or improving crop survival or improving yield.'),
        'carbon': ('Carbon storage', 'It reduces the amount of carbon dioxide in the atmosphere, (helping to slow climate change) / (Carbon-rich) soils have better structure or water-holding capacity or higher fertility or allows stronger root growth or higher yields.'),
        'losses': ('Reduced environmental losses', 'Healthy soil biome prevents nitrate leaching or phosphorus runoff (into rivers and lakes, improving water quality) / more nutrients stay in the field, meaning less fertiliser is wasted.'),
        'resilience': ('Improve plant resilience', 'Healthy soil biome (and diverse systems) help plants cope with stress / crops becomes more resistant to drought or disease or extreme weather / more reliable yields, even in difficult seasons.'),
        'food': ('Food quality', 'Improved access to soil nutrients improves crop quality / increases protein or vitamin or mineral content of food crops / produces healthier feed for livestock or higher quality produce for consumers.'),
        'nutrients': ('Nutrient provision', 'Soil organisms release nutrients naturally through decomposition / provides crops with a steady supply of nitrogen or phosphorus or trace elements / reduces reliance on chemical fertilisers, lowering costs.'),
    }
    for chosen in combinations(benefits, 4):
        labels = [benefits[k][0] for k in chosen]
        add('q7-route-' + '-'.join(chosen), 'Q7 — ' + ', '.join(labels), '2-2-3', 'soil-science', 'soil-biological-health-benefits',
            'Outline how any four benefits can improve agricultural productivity and/or ecosystem health.',
            [menu([benefits[k][1] for k in chosen], [5, 3, 1, 1],
                  'One outline for each of your four benefits, in order: ' + '; '.join(labels) + '. Alternatives within one benefit earn one award. The scheme prints 5+3+2(1).')],
            [region(12, .065, .505)], [region(16, .333, .870)],
            'Good soil biology is essential for agricultural productivity and ecosystem health. Improving soil’s biological health is a very important aspect of all farming. Practice choice: ' + ', '.join(labels) + '.',
            selection={'kind': 'closed', 'choose': 4, 'options': list(benefits), 'route': list(chosen)})

    q8 = 'A farmer is considering introducing a new beef breed (Breed A) to cross with their dairy cows (Breed B) towards the end of the breeding season to improve beef efficiency on their farm.'
    add('q8a', 'Q8(a)', '4-2', 'beef-cattle|dairy-cattle', 'beef-dairy-breed-identification', 'Identify breed A and B.',
        [menu(['A – Limousin', 'B – (Holstein) Friesian'], [4, 1], 'Breeds pictured A and B. The first correct identification earns 4 marks and the second 1.')],
        [region(13, .065, .375)], [region(17, .066, .130)], q8)
    add('q8b', 'Q8(b)', '4-2', 'beef-cattle|dairy-cattle', 'beef-dairy-breed-traits', 'Compare the production traits of breed A and B under the following headings:',
        [point('Higher liveweight gain / low milk yield', None, 'Growth / milk yield: Limousin (A).', kind='criterion'),
         point('Lower liveweight gain / higher milk yield', None, 'Growth / milk yield: Holstein Friesian (B).', kind='criterion'),
         point('Lively / excitable', None, 'Temperament: Limousin (A).', kind='criterion'),
         point('Quiet / easy to handle', None, 'Temperament: Holstein Friesian (B). The scheme prints 4+1 for the two headings: the first correctly compared heading earns 4 marks and the second 1. Award a heading only when both breeds are compared.', kind='criterion')],
        [region(13, .065, .375), region(13, .41, .82)], [region(17, .130, .275)], q8, marks=5, extra=('4-3-1',))

    q9 = 'A student set up an investigation to compare the drainage rate of 50 g of three different soil samples, sand, clay and loam.'
    add('q9a', 'Q9(a)', '1-2', 'soil-science|scientific-practices-experiments-investigations', 'fair-test-drainage', 'State why this investigation is a fair test.',
        [menu('Used equal amounts of samples|same set up used for all or described', [3])], [region(14, .065, .455)], [region(17, .275, .340)], q9, extra=('2-2-2',))
    add('q9b', 'Q9(b)', '2-2-2', 'soil-science|scientific-practices-experiments-investigations', 'soil-drainage-prediction',
        'Predict the result the student would observe from this investigation.',
        [point('Water drains fastest in the sand / slowest in clay / loam between the two', 3)], [region(14, .065, .43), region(14, .546, .57)], [region(17, .340, .406)], q9, extra=('1-2',))
    add('q9c', 'Q9(c)', '2-2-2', 'soil-science|crop-production', 'soil-type-for-crops',
        'Using your predicted result from part (b), identify with reason which soil type would be most suitable for a crop production enterprise.',
        [point('Soil type = loam', 2), menu('good drainage|retains water|won’t wash out nutrients|air spaces for root development or easily worked|warms easily', [2], 'One reason for choosing loam.')],
        [region(14, .065, .43), region(14, .546, .57), region(14, .663, .767)], [region(17, .406, .545)], q9)

    plants = {'A': 'A – Ragwort', 'B': 'B – Nettle', 'C': 'C – Dandelion'}
    for chosen in combinations(plants, 2):
        add('q10a-route-' + ''.join(chosen).lower(), 'Q10(a) — ' + ', '.join(chosen), '3-2', 'classification-of-animals-plants', 'weed-identification',
            'Identify any two of the plants A, B, and C.',
            [menu([plants[k] for k in chosen], [3, 2], 'Identify the two plants you chose. The first correct identification earns 3 marks and the second 2.')],
            [region(15, .065, .387)], [region(17, .545, .628)],
            'During a farm walk, a farmer was asked to identify the three plants A, B and C found in the field. Practice choice: plants ' + ' and '.join(chosen) + '.',
            selection={'kind': 'closed', 'choose': 2, 'options': list(plants), 'route': list(chosen)})
    add('q10b', 'Q10(b)', '3-3-1', 'crop-production', 'uncertified-seed-risks',
        'The farmer accidentally bought uncertified seed containing a high percentage of weed seeds. Explain two risks this poses to productivity and sustainability on his farm.',
        [menu(['(Increase in weed populations) competition – reduced yield or income', 'seeds can remain viable in soil for many years', 'long term weed control very difficult or expensive',
               'use of chemical or cultivation needed to control weeds or pests (reducing biodiversity)', 'damaged soil structure', 'increased risk of disease',
               'lower percentage germination or any negative effect of not using certified seed'], [3, 2])],
        [region(15, .065, .115), region(15, .387, .43)], [region(17, .628, .785)], extra=('3-3-2',))

    q11a = 'A farmer is building new winter housing for beef cattle.'
    add('q11ai', 'Q11(a)(i)', '4-3-3', 'beef-cattle', 'housing-health-welfare',
        'Outline with reason two features of good animal housing that promote animal health and welfare.',
        [menu(['Good Ventilation: Removes moisture or dust or harmful gases such as ammonia / reduces (respiratory) disease or improves overall air quality',
               'Clean, dry bedding: Comfortable lying areas prevent pressure sores or mastitis / dry conditions reduce the growth of bacteria or parasites',
               'Adequate space or stocking density or light: Prevents overcrowding or reduces stress or aggression or disease / allows animals to express normal behaviour (such as lying, feeding and social interaction)',
               'Non-slip flooring: Prevents injuries or lameness', 'Proper drainage or hygiene: Reduces build-up of slurry or pathogens / lowers the risk of diseases such as foot rot or digital dermatitis',
               'Easy access to feed or water: Prevents bullying or uneven feed intake / ensures animals maintain good body condition or healthy',
               'Comfortable temperature or draft free or shelter: Protects animals from cold stress or heat stress / maintains immunity or productivity',
               'Isolation unit: Prevent transmission of disease', 'Enrichment materials: Correctly described'], [3, 3],
              'Each award needs a feature with its matching reason, as paired in the scheme table.')],
        [region(16, .065, .193)], [region(18, .066, .709)], q11a)
    add('q11aii', 'Q11(a)(ii)', '4-3-3', 'beef-cattle', 'poor-housing-effects', 'Explain how poor housing design can negatively affect the following:',
        [menu(['Poor ventilation leads to a build-up of ammonia or moisture, increasing the risk of (respiratory) diseases / (Sick animals eat less and convert feed poorly) resulting in reduced growth rates or lower milk yield',
               'Overcrowding causes competition for feed or lying space. This leads to uneven feed intake or aggression or bullying, which can reduce fertility or milk production or weight gain or injury',
               'Slippery or uneven floors increase the incidence of lameness or injury. (Lame animals spend less time feeding and more time lying down), reducing output or increasing veterinary costs',
               'Damp, dirty conditions promote microbial growth or increasing cases of mastitis or foot rot or other infections, which further lower productivity'], [2], 'Animal performance.'),
         menu(['Inadequate handling facilities make it difficult to restrain or treat animals safely / frightened or stressed animals are unpredictable, increasing the risk of injury',
               'Poor lighting or narrow passageways make it harder to move around buildings / increasing the chance of accidents',
               'Slippery floors and poor drainage expose farmers to falls / while poorly positioned gates or barriers can lead to serious accidents (when working with large livestock)',
               'Poor Ventilation inhalation of harmful gases or pathogens'], [2], 'Farmer safety.')],
        [region(16, .09, .113), region(16, .473, .72)], [region(19, .066, .612)], q11a, extra=('1-5',))
    q11b = 'Calculate the straw bedded floor space required for 40 finishing bulls, if the recommended space per head allowances are: Straw bed: 4.0 m2; Slatted house: 2.5 m².'
    add('q11bi', 'Q11(b)(i)', '4-3-3', 'beef-cattle', 'floor-space-calculation', q11b,
        [point('4 x 40', 2, 'Correct method.'), point('160 (m2)', 2, 'Correct answer. 160 without the calculation earns all 4 marks; no units are required.')],
        [region(17, .065, .2)], [region(19, .629, .753)], extra=('1-3',))
    add('q11bii', 'Q11(b)(ii)', '4-3-3', 'beef-cattle', 'finishing-bull-housing',
        'The cattle shed was 170 m2 divided into two pens. Based on your answer in part (i), describe how the farmer would manage the housing of his finishing bulls to ensure they reach their target slaughter weight.',
        [point('Bulls would have to be split between the two pens (according to weight or size)', 3)],
        [region(17, .09, .165), region(17, .315, .375)], [region(19, .753, .855)], 'Part (i): ' + q11b)
    add('q11biii', 'Q11(b)(iii)', '4-3-3', 'beef-cattle|pigs', 'repurposing-pig-housing',
        'Due to financial constraints, the farmer is considering converting an old slatted pig house shown in the pictures, for beef cattle housing. Evaluate one potential problem with repurposing housing designed for pigs to accommodate cattle.',
        [menu(['Floor and structural strength - slats are not designed to support heavier animals',
               'Space allowance and layout – overcrowding or bullying or reduced feed intake or narrow pens or low headroom or low gates or narrow passageways or poor access',
               'Ventilation systems insufficient air flow', 'Handling and safety facilities Cattle require strong or larger barriers or gates or handling facilities',
               'Slurry storage not designed for the much larger volumes produced by cattle'], [3])],
        [region(17, .512, .79)], [region(20, .066, .314)])

    q12 = 'Alice is a sheep and beef farmer. She is planning to expand into pig production and wants high performance for her pig herd. Using knowledge of sheep and beef production, answer the questions that follow.'
    add('q12a', 'Q12(a)', '4-3-2', 'pigs|genetics', 'pig-breeding-traits', 'Suggest two desirable traits the farmer might select when breeding pigs.',
        [menu('Prolificacy (large litter size)|good mothering ability|fast growth rate|efficient food conversion ratio (low FCR)|good carcass quality|disease resistance|good feet|good genetics|good conformation', [3, 3])],
        [region(18, .065, .36)], [region(20, .314, .430)], q12)
    add('q12b', 'Q12(b)', '4-3-2', 'pigs|genetics', 'hybrid-vigour-pigs', 'Explain how hybrid vigour could improve the performance in a pig herd.',
        [menu('Increased litter size|fast growth rate|low FCR|good carcass quality|disease resistance|good feet|good genetics', [2])],
        [region(18, .065, .157), region(18, .489, .514)], [region(20, .430, .513)], q12)
    add('q12c', 'Q12(c)', '4-3-2', 'pigs|genetics', 'pedigree-breeding-risk', 'Outline one genetic risk of relying heavily on pedigree breeding in animals.',
        [menu('Greater risk of Inbreeding|harmful recessive genes or described disease (BRD) are more likely to be expressed|possible reduction in overall performance (offspring show reduced fertility or slower growth)|poorer disease resistance|increase in inherited defects', [2])],
        [region(18, .065, .157), region(18, .673, .698)], [region(20, .513, .635)], q12)

    # Section B ---------------------------------------------------------------
    q13 = ('Dermot and Pauline are mixed tillage and sheep farmers in Co. Galway. They are planning on reseeding 10% of their 70-hectare farm and are preparing a nutrient management plan (NMP) before reseeding the grassland field.')
    add('q13ai', 'Q13(a)(i)', '2-3', 'soil-science|fertilisers-pollution-environment-cycles', 'nutrient-management-plan',
        'Identify the meaning of a nutrient management plan by placing a tick (✓) in the correct box.',
        [point('Blueprint for managing nutrient inputs and applications across the farm', 6, 'The scheme ticks this box.')],
        [region(21, .155, .415)], [region(21, .118, .240)], q13)
    add('q13aii', 'Q13(a)(ii)', '2-2-1', 'soil-science|grassland', 'phosphorus-potassium-establishment',
        'Explain how each of the following soil properties affects grass establishment:',
        [menu('Essential for root development|low P – weak root or slow seedling establishment|helps young grass plants develop (and compete with weeds)|energy production (ATP) or cell division', [1], 'Phosphorus (P).'),
         menu('Essential for plant (stem) strength or stress tolerance|improves resistance to drought or stomata function or disease or poaching|low K levels are slow to establish or more easily damaged|maximise N uptake|translocation of nutrients/protein or enzyme synthesis', [1], 'Potassium (K).')],
        [region(21, .155, .275), region(21, .418, .645)], [region(21, .240, .418)], q13, extra=('3-3-1',))
    add('q13bi', 'Q13(b)(i)', '2-2-2', 'soil-science', 'flocculation',
        'Explain flocculation and outline why it is important for soil structure.',
        [menu(['Process by which fine soil particles (especially clay) bind together to form larger aggregates (peds)', 'Improves soil porosity or aeration', 'better drainage or preventing waterlogging',
               'increases root penetration or allows plants to access nutrients and moisture', 'reduces compaction or surface crusting or erosion, (making soils easier to cultivate)', 'promotes microbial activity'], [3, 1],
              'One explanation and one importance point. The first correct field earns 3 marks and the second 1.')],
        [region(21, .155, .275), region(21, .646, .762)], [region(21, .418, .600)], q13)
    add('q13bii', 'Q13(b)(ii)', '2-2-1', 'soil-science', 'ph-calcium-flocculation', 'Describe how soil pH and calcium influence flocculation in soils.',
        [menu(['Maintaining a suitable soil pH (pH 6-8) ensures sufficient calcium is available', 'sufficient calcium cations attract negative clay particles allowing flocculation to occur',
               'high soil pH (6-8) and calcium increases flocculation or low soil pH (<6) and calcium decreases flocculation'], [2])],
        [region(22, .065, .09)], [region(21, .600, .718)], extra=('2-2-2',))
    add('q13biii', 'Q13(b)(iii)', '1-2', 'soil-science|scientific-practices-experiments-investigations', 'flocculation-investigation',
        'Describe with the aid of a labelled diagram an investigation to show flocculation in a sample of soil.',
        [point('add named reagent to each test tube (Lime or Calcium Chloride or Aluminium Chloride or Sodium Chloride or Hydrochloric Acid)', 5,
               'Compulsory point (*): name the reagent. The scheme prints 3(5)+1 for four points and no separate diagram award.'),
         menu('Add 5g (or specified amount) of soil to each test tube|water as a control|add equal volume of deionised water to each test tube|stopper and shake|leave to stand or set period of time|record which suspensions settles faster', [5, 5, 1],
              'Three further points from one coherent investigation: two at 5 marks and one at 1.')],
        [region(22, .249, .292)], [region(21, .718, .874)], extra=('2-2-2',))
    q13c = ('Pauline carried out a soil test in two areas planned for grassland reseeding and she compared her data with the reference soil index shown in the tables below. Analyse the results and answer the questions that follow.')
    add('q13ci', 'Q13(c)(i)', '2-2-1', 'soil-science|fertilisers-pollution-environment-cycles', 'soil-fertility-comparison', 'Compare the fertility status of Field A and Field B.',
        [point('Field B has good fertility due to Optimum pH, or adequate P or adequate K or higher Organic Matter', None, 'Field B.', kind='criterion'),
         point('Field A has poor fertility due to Acidic soil or very low P or low K or lower Organic Matter.', None,
               'Field A. The scheme: at least 2 factors compared correctly for full marks (12); 1 factor mentioned correctly for 6 marks. Its table compares pH, P index, K index and organic matter for each field.', kind='criterion')],
        [region(23, .065, .43)], [region(22, .066, .629)], q13c, marks=12, extra=('1-3',))
    add('q13cii', 'Q13(c)(ii)', '2-3', 'soil-science|fertilisers-pollution-environment-cycles', 'field-fertility-management',
        'Recommend appropriate management for each field to improve or maintain fertility.',
        [menu(['Field A: (corrective action) Addition of Lime or P or K or organic matter necessary (qualified)', 'Field B: Lime or fertiliser or OM not necessary (qualified)'], [6, 2],
              'One qualified recommendation for each field; the scheme requires at least 2 factors compared correctly for full marks.')],
        [region(23, .065, .40), region(23, .62, .77)], [region(22, .629, .789)], q13c)

    q14 = ('Beef farmers Dylan and Margaret are aiming to improve the sustainability and profitability of their suckler-to-beef enterprise. Based on a visit from their local Teasgasc advisor they were advised to: '
           'Improve soil fertility and drainage; Establish a perennial ryegrass–clover sward for finishing cattle; Increase daily live weight gain (DLG) while reducing chemical nitrogen inputs; '
           'Ensure animal health, welfare, and safe farm practices. Using this advice answer the questions that follow.')
    add('q14ai', 'Q14(a)(i)', '3-3-1', 'grassland|fertilisers-pollution-environment-cycles', 'clover-nitrogen-fixation',
        'Identify why clover is included in the sward for the finishing cattle, by placing a tick (✓) in the correct box.',
        [point('Clover fixes atmospheric nitrogen and makes it available to the soil', 5, 'The scheme ticks this box.')],
        [region(24, .065, .432)], [region(23, .066, .166)], q14, extra=('2-2-3',))
    add('q14aii', 'Q14(a)(ii)', '2-2-1', 'grassland|soil-science', 'ph-clover-establishment',
        'Explain why maintaining soil pH is critical for clover establishment and grass growth.',
        [menu(['If soil is too acidic (< 5.8), nutrients become unavailable (for plant growth) or pH 6-8 is required for clover establishment or grass growth', 'calcium or magnesium deficiency (reduces rhizobia survival)',
               'in low pH soils manganese (Mn) and aluminium (Al) toxicity can have a major effect on white clover development.', 'formation of nodules for N fixation is reduced below soil pH 5.8',
               '(symbiotic) bacteria (Rhizobium or nitrogen fixing) are pH sensitive'], [1])],
        [region(24, .065, .285), region(24, .437, .462)], [region(23, .166, .335)], q14)
    add('q14aiii', 'Q14(a)(iii)', '1-5', 'beef-cattle', 'farm-safety-practices', 'Outline two ways Dylan and Margaret can ensure safe practices on the farm.',
        [menu('Identify hazards and risks and remove them|lock away chemicals|proper signage|use of protective guards (PTO)|have an escape route when dealing with animals|barrier between cow during calving|beware of bull|keep gates closed|safe practices when using chemicals|any valid safety practice', [6, 6])],
        [region(24, .065, .285), region(24, .592, .616)], [region(23, .335, .454)], q14)
    add('q14bi', 'Q14(b)(i)', '4-1', 'grassland|animal-physiology-digestive-system|beef-cattle', 'clover-ruminant-liveweight-gain',
        'Using your knowledge of ruminant digestion, explain how clover can increase live weight gain in the beef finishing cattle.',
        [menu('Improves the nutritional value of the diet or rumen efficiency|higher level of protein than grass|(palatable) increasing feed intake|(digestibility) improving feed conversion efficiency', [5])],
        [region(24, .09, .285), region(25, .065, .106)], [region(23, .454, .553)], q14, extra=('4-3-1',))
    add('q14bii', 'Q14(b)(ii)', '4-3-3', 'beef-cattle|animal-diseases', 'clover-bloat-risk',
        'Outline with reason one risk of grazing high-clover swards for beef cattle.',
        [menu(['Risk: Bloat', 'Clover is very rapidly digested in the rumen or very high in Nitrogen or protein and (produces a stable foam that traps gas)',
               'prevents normal eructation (belching), causing the rumen to swell', 'if not treated quickly, bloat can restrict breathing and may lead to death'], [4, 1],
              'Risk and one matching reason. The first correct field earns 4 marks and the second 1.')],
        [region(24, .09, .285), region(25, .226, .336)], [region(23, .553, .696)], q14)
    add('q14biii', 'Q14(b)(iii)', '3-3-2', 'grassland', 'maintaining-clover',
        'Outline two management practices to maintain clover in a grass–clover sward under grazing conditions.',
        [menu(['Maintain correct soil pH (around 6.3–6.5)', 'ensure adequate P and K levels', 'controlled nitrogen use (as this favours grass growth and suppresses clover)',
               'rotational grazing – (use a tight grazing system) to prevent shading', 'avoid overgrazing in wet conditions or prevent poaching which damages clover',
               'reseeding or oversown into existing swards (when plant numbers decline)', 'balanced stocking rate - grazed evenly and not out-competed by grass', 'clover friendly weed management plan'], [6, 2])],
        [region(24, .09, .285), region(25, .37, .411)], [region(23, .696, .844), region(24, .066, .109)], q14)
    add('q14biv', 'Q14(b)(iv)', '3-3-1', 'grassland', 'clover-inclusion-rate',
        'Identify the average recommended clover inclusion rate in grassland swards by placing a tick (✓) in the correct box.',
        [point('20%', 2, 'The scheme ticks 20%.')], [region(25, .602, .755)], [region(24, .109, .195)], q14)
    sowing = {
        'A': ('Direct drilling', 'Method: A = Direct drilling / stitching in / slit sowing',
              ['Land grazed or cut tightly', 'The machine opens a small groove in the grass sward', 'Clover seed is dropped into the slot at the correct depth (5-10mm)',
               'The slot then closes, leaving the seed in direct contact with the soil or rolled']),
        'B': ('Broadcasting', 'Method B = Broadcast',
              ['Land grazed or cut tightly', 'Seed is spread using a fertiliser spreader or by hand',
               'The field is then lightly grazed or rolled so that animals’ hooves or machinery help press the seed into the soil']),
    }
    for letter, (label, name, steps) in sowing.items():
        add('q14ci-route-' + letter.lower(), f'Q14(c)(i) — {letter}', '3-3-1', 'grassland', 'clover-oversowing-method',
            'Identify method A or B and explain to a group of farmers how clover seeds can be sown using this method.',
            [point(name, 3, 'Named method.'),
             menu(steps, [3, 3], '* If the name and method match they get full marks, if the name and method don’t match they get awarded the marks for the name')],
            [region(26, .065, .41)], [region(24, .195, .542)],
            f'Clover seeds can be over-sown into established swards in a number of ways as shown in the photographs A and B below. Practice choice: method {letter} ({label}).',
            selection={'kind': 'closed', 'choose': 1, 'options': list(sowing), 'route': [letter]})
    add('q14cii', 'Q14(c)(ii)', '3-3-1', 'grassland', 'oversowing-grazing-height',
        'Identify the ideal post-grazing height of the sward at time of over-sowing by placing a tick (✓) in the correct box.',
        [point('≤ 4cm', 3, 'The scheme ticks ≤ 4cm.')], [region(26, .065, .106), region(26, .73, .875)], [region(24, .542, .647)])
    add('q14d', 'Q14(d)', '1-2', 'scientific-practices-experiments-investigations|grassland', 'root-nodule-bacteria',
        'Describe with the aid of a labelled diagram, how a student could carry out an investigation to isolate and grow bacteria from the root nodules of a clover plant.',
        [menu(['Sterilise equipment or wash roots in (Milton) solution or stay close to Bunsen burner (sterile environment)', 'rinse roots with water', 'remove nodules with scalpel or crush root nodules',
               'swab some of the root nodules onto agar plate', 'in a zig zag', 'incubate upside down', '25°C', '> 48 hours (2-7days)',
               'record no. of colonies present or correctly identify colonies or no growth on control', 'incubate unopened plate as a control'], [3, 3, 3, 3],
              'Four points from one coherent investigation; *only one point accepted related to sterile. The scheme prints 4(3) and no separate diagram award.')],
        [region(27, .065, .205)], [region(24, .665, .879)], extra=('2-2-3',))

    q15a = ('Read the article and answer the questions that follow. Artificial Intelligence (AI) tools are revolutionising farming. The 2025 innovation award winner at the National Ploughing Championships is a technology which utilises AI '
            'to give real-time information on cow scanning. This AI-powered reproductive intelligence allows for smarter scanning and AI-enhanced reproductive status of animals in seconds. '
            'Scan readout: ID = 453; Days calved = 125 days; Days served = 36 days; Lactation = 3.2 years; AI Age = 36.2 days. (Adapted from Agriland and RTÉ, 2025)')
    add('q15ai', 'Q15(a)(i)', '4-3-2', 'dairy-cattle|innovation-and-biotechnology-in-agriculture', 'scan-days-in-calf', 'Identify how long the cow ID number 453 is in calf.',
        [point('36 days', 5)], [region(28, .065, .542)], [region(25, .066, .114)], q15a, extra=('1-3',))
    add('q15aii', 'Q15(a)(ii)', '4-3-2', 'dairy-cattle|innovation-and-biotechnology-in-agriculture', 'scan-lactation-number', 'Identify the lactation number of the cow.',
        [point('3 or 3.2', 5)], [region(28, .09, .51), region(28, .582, .606)], [region(25, .114, .163)], q15a, extra=('1-3',))
    add('q15aiii', 'Q15(a)(iii)', '4-3-2', 'dairy-cattle|innovation-and-biotechnology-in-agriculture', 'scan-ai-accuracy', 'Comment on the accuracy of the AI age of this foetus.',
        [menu(['Very accurate', 'AI accuracy is 36.2 days which is in line with the actual days served', 'AI provides precise reading using bank of comparison values'], [4, 1],
              'Judgement and one supporting reason. The first correct field earns 4 marks and the second 1.')],
        [region(28, .09, .51), region(28, .645, .67)], [region(25, .163, .254)], q15a, extra=('1-3',))
    add('q15aiv', 'Q15(a)(iv)', '4-3-2', 'dairy-cattle|animal-physiology-reproductive-systems', 'twin-pregnancy-importance', 'Outline the importance of identifying twin pregnancies in cows.',
        [menu(['require extra nutrition to maintain correct BCS or support the increased foetal demand', 'to provide extra supervision at calving (higher risk of calving difficulties)',
               'cows can be put on a special pre-calving diet and monitored closely (greater risk of metabolic disorders)',
               'adjust feeding levels or reduce stress to lower the risk of losing calves (higher incidence of abortion and premature calving)',
               'more likely to produce freemartin heifers (sterile female calves when born with a bull twin)'], [5])],
        [region(28, .09, .51), region(28, .766, .79)], [region(25, .254, .407)], q15a)
    add('q15av', 'Q15(a)(v)', '4-3-2', 'dairy-cattle|animal-physiology-reproductive-systems', 'reproductive-status-dry-cow',
        'Explain how an accurate reproductive status can improve dry cow management for next calving and breeding season.',
        [menu(['Knowing the expected calving date ensures cows are dried off at the correct time (60 days)', 'give udder enough time to regenerate, leading to higher milk yield in the following lactation',
               'feed cows at appropriate stage of pregnancy - prevent metabolic disorders or ensure available colostrum (such as milk fever or ketosis or retained placenta or maintain BCS)',
               'identifies barren cows – culled (to shorten calving interval)',
               'easier management at calving - moved to calving pens and monitored closely or reducing calving difficulties or improving calf survival'], [2])],
        [region(28, .09, .51), region(29, .065, .106)], [region(25, .407, .593)], q15a)
    add('q15bi', 'Q15(b)(i)', '4-1', 'animal-physiology-reproductive-systems', 'cow-reproductive-system-diagram', 'Draw a labelled diagram of a cow’s reproductive system.',
        [point('Diagram', None, 'Diagram earns 0, 3 or 6 marks; compare with the official scheme diagram.', kind='criterion'),
         point('Labels', None, 'Four correct labels at one mark each, as 4(1). Add to the diagram award for a maximum of ten.', kind='criterion')],
        [region(29, .266, .32)], [region(25, .593, .774)], marks=10, figure='agsci-2026-hl-scheme-cow-reproductive-system')
    add('q15bii', 'Q15(b)(ii)', '4-1', 'dairy-cattle|animal-physiology-reproductive-systems', 'calving-interval-targets',
        'In order to ensure maximum profitability is achieved targets need to be met. Using the diagram below, identify X, Y and Z days in the passage.',
        [menu(['X = 365 days', 'Y = 275 days', 'Z = 45 or 90 days'], [5, 5, 1], 'The first two correct values earn 5 marks each and the third 1.')],
        [region(30, .065, .598)], [region(25, .774, .880)], extra=('4-3-2',))
    add('q15biii', 'Q15(b)(iii)', '4-3-2', 'dairy-cattle', 'drying-off-date',
        'Based on an expected calving date of the 1st February, state what date a dairy cow should be dried off.',
        [point('1st to 3rd Dec', 2)], [region(30, .603, .648)], [region(26, .066, .130)])
    add('q15biv', 'Q15(b)(iv)', '4-3-2', 'dairy-cattle|animal-physiology-reproductive-systems', 'heat-detection-importance',
        'Briefly explain the importance of heat detection in the reproductive cycle of dairy cows.',
        [menu(['Limited opportunity to put in calf', 'if missed has to wait 21 days to serve',
               'optimising calving intervals – (target 365-day calving interval or maximising lifetime milk or calf production)', 'maintain compact calving',
               'identifying "silent" heats (high-producing cows often show less intense heat signs)'], [5])],
        [region(30, .69, .715)], [region(26, .130, .264)])

    q16 = 'Silage is a key winter feed for dairy cows in Ireland. High-quality silage depends on grass variety, growth stage at cutting, and proper storage.'
    add('q16ai', 'Q16(a)(i)', '3-1', 'grassland', 'grass-growth-stages', 'Describe three stages of grass growth and identify the ideal growth stage for cutting.',
        [menu(['Germination Stage: The radicle and plumule emerge / emergence of cotyledons',
               'Leafy / Vegetative Stage: Grass is young with mainly leaf material (and little or no stem) / grass tillers / high in digestibility or energy or protein/ production of 3 leaves',
               'Stem Elongation Stage: The stem begins to grow upwards (and the grass becomes less leafy) / fibre content increases /digestibility starts to fall',
               'Reproductive / Heading / Flowering /inflorescence Stage: The seed head emerges / wind pollination occurs/ high fibre / low digestibility',
               'Ideal Stage for Cutting: The best time to cut silage is during the leafy (vegetative) stage'], [4, 4, 1, 1],
              'Three described stages and the ideal cutting stage. The scheme prints 2(4)+2(1): the first two correct fields earn 4 marks each and the next two 1 each.')],
        [region(31, .065, .158)], [region(26, .264, .619)], q16, extra=('3-3-3',))
    add('q16aii', 'Q16(a)(ii)', '3-2', 'grassland|classification-of-animals-plants', 'multispecies-sward-plants',
        'Identify plants A, B and C that farmers could sow in a multi-species sward.',
        [menu(['A – Plantain', 'B – Chicory', 'C – Timothy'], [5, 3, 1], 'The first correct identification earns 5 marks, the second 3 and the third 1.')],
        [region(31, .623, .845)], [region(26, .619, .703)], q16)
    add('q16aiii', 'Q16(a)(iii)', '3-3-1', 'grassland', 'chicory-purpose', 'Outline one purpose of including plant B from part (ii) in a multi-species sward.',
        [menu('(Deep or tap root leads to) drought tolerance or increased nutrient absorption|improve soil structure|very digestible or palatable (increased production or liveweight gain)|is a (natural) anthelmintic or reduce internal parasites or reduce usage of anthelmintic', [2],
              'Plant B is chicory in the scheme for part (ii).')],
        [region(31, .623, .845), region(32, .065, .09)], [region(26, .703, .821)], q16)
    add('q16aiv', 'Q16(a)(iv)', '3-3-1', 'grassland', 'polyculture-sward',
        'Identify whether a multi-species sward is a monoculture or polyculture sward by placing a tick (✓) in the correct box',
        [point('Polyculture', 3, 'The scheme ticks Polyculture.')], [region(32, .188, .29)], [region(26, .821, .883)], q16)
    c = add('q16av', 'Q16(a)(v)', '3-3-2', 'grassland', 'spring-grazing-before-silage',
        'State with reason if farmers should graze grass in spring to 4cm prior to closing grass for silage.',
        [menu(['No', 'Yield reduction - grazing too tightly (e.g., to 4cm) removes a large portion of the active leaf area required for photosynthesis'], [3, 3])],
        [region(32, .295, .336)], [region(27, .066, .325)], q16)
    variants(c, [
        ('no', 'No', [menu(['No', 'Yield reduction - grazing too tightly (e.g., to 4cm) removes a large portion of the active leaf area required for photosynthesis',
                            'slow recovery - the growth of the grass is severely hindered by hard grazing or plant needs adequate energy reserves to initiate strong regrowth',
                            'increased contamination risk - hard grazing can expose the base of the plant and potentially disturb the soil surface'], [3, 3],
                           'The position and one matching reason, 2(3). The scheme credits either position when the reason matches it.')]),
        ('yes', 'Yes', [menu(['Yes', 'To remove dead (winter damaged) vegetation', 'increase light penetration', 'increased tillering', 'promotes rapid leafy (uniform) growth'], [3, 3],
                             'The position and one matching reason, 2(3). The scheme credits either position when the reason matches it.')]),
    ])
    q16b = 'Soil fertility affects the quality of silage. Analyse the graph and answer the questions that follow.'
    add('q16bi', 'Q16(b)(i)', '2-3', 'grassland|soil-science', 'soil-fertility-silage-yield', 'Outline how the fertility of the soil affects the yield and quality of silage.',
        [point('The better the soil fertility, the higher the yield and quality of silage', 3)], [region(32, .436, .835), region(33, .065, .09)], [region(27, .325, .374)], q16b, extra=('1-3',))
    add('q16bii', 'Q16(b)(ii)', '1-3', 'grassland|soil-science', 'silage-target-dates',
        'If the target yield is 5 tonnes Dry Matter (DM) per ha, identify at what date each soil type will reach this target.',
        [point('26th May', 4, 'Good soil fertility.'), point('16th June', 4, 'Poor soil fertility.')],
        [region(32, .436, .835), region(33, .219, .34)], [region(27, .374, .446)], q16b, extra=('2-3',))
    add('q16biii', 'Q16(b)(iii)', '1-3', 'grassland|soil-science', 'silage-fertility-conclusion', 'Outline the conclusion you make based on the results in part (ii).',
        [menu('Good quality soil can produce 5 ton DM per ha (3 weeks or 20 days) earlier than poor quality soil|good quality soil will produce higher DMD silage (72% vs 62%)', [3])],
        [region(32, .436, .835), region(33, .219, .26), region(33, .344, .368)], [region(27, .446, .530)], q16b, extra=('2-3',))
    spoil = [('wet', 'Grass too wet', 'Cut grass in dry weather / wilt'),
             ('aerobic', 'Aerobic conditions present', 'Roll continuously during filling to remove air / high density bale / cover pit immediately after filling or secure plastic or repair damage plastic / fill and seal the pit as quickly as possible'),
             ('contamination', 'Contamination', 'Prevent soil or slurry or N entering / close field for adequate length of time (6 weeks)'),
             ('sugars', 'Insufficient sugars in grass', 'Cut leafy grass at the correct growth stage or time of day / use a silage additive (e.g. molasses or sulphuric acid or inoculant) / precision chop or conditioner mower')]
    c = add('q16c', 'Q16(c)', '3-3-3', 'grassland', 'silage-spoilage', 'Outline one reason why silage might spoil and how it can be prevented.',
        [menu(list(spoil[0][1:]), [3, 3])], [region(33, .468, .52)], [region(27, .530, .810)])
    variants(c, [(k, reason, [menu([reason, prevention], [3, 3], 'Reason and matching prevention, 2(3).')]) for k, reason, prevention in spoil])
    add('q16d', 'Q16(d)', '3-3-3', 'grassland|sheep', 'baled-silage-advantages', 'State two advantages of bailed silage on a sheep farm.',
        [menu('Flexibility and scalability (easy transport or handling or saleability)|better quality and nutrition|reduced spoilage or waste|lower risk at harvesting|easier manage different fields at harvest|efficient storage and handling|cost-effective', [3, 3])],
        [region(33, .635, .66)], [region(28, .083, .184)])

    q17 = ('In a standard suckling to beef system Teagasc over the years has set the target of producing a 400 kg steer carcase at two years of age. The table below shows the performance targets that need to be reached throughout the lifetime of a spring born suckled steer to achieve this. '
           'Birth: target live weight X. Weaning / housing (1st Winter): 8 months (240 days), 315 kg. Spring turnout (2nd Summer): 12 months (365 days), 380 kg. Housing (2nd Winter): 19 months (570 days), 580 kg. '
           'Slaughter: 24 months (730 days), 780 kg. ADG: 1st Summer = 1.1 kg; 1st Winter = 0.5 kg; 2nd Summer = ?; 2nd Winter = 1.1 kg. (Adapted from Teagasc, 2022)')
    add('q17ai', 'Q17(a)(i)', '4-3-1', 'beef-cattle', 'calf-birth-weight', 'State the target live weight X in the table above.',
        [point('40 – 50kg', 5)], [region(34, .065, .48)], [region(28, .184, .233)], q17)
    add('q17aii', 'Q17(a)(ii)', '4-3-1', 'beef-cattle', 'average-daily-gain-calculation', 'Calculate the ADG for the animal during its 2nd Summer.',
        [point('580-380 = 200', 2, 'Weight gained (kg).'), point('570-365 = 205', 2, 'Days.'),
         point('200 / 205 = 0.975 (0.97-0.98)', 2, 'Answer. The correct answer without the calculation earns all 6 marks.')],
        [region(34, .065, .447), region(34, .521, .546)], [region(28, .233, .379)], q17, extra=('1-3',))
    add('q17aiii', 'Q17(a)(iii)', '4-3-1', 'beef-cattle', 'adg-stage-differences', 'Explain why there is a difference in ADG during the different stages.',
        [menu('Maintenance diet in 1st winter|compensatory growth in 2nd summer|production or finishing diet in 2nd Winter', [1, 1])],
        [region(34, .065, .447), region(34, .69, .714)], [region(28, .379, .446)], q17)
    add('q17aiv', 'Q17(a)(iv)', '1-4', 'beef-cattle', 'liveweight-trend-graph',
        'Using the data in the table, plot a graph showing the trend in target live weight over the lifecycle of the animal.',
        [point('correct scale', None, 'Scale.', kind='criterion'), point('correct data plotted (5 plotted points)', None, 'Plotted points.', kind='criterion'),
         point('line correctly drawn', None, 'Line. The mark column prints 4+4+3 for these three criteria, a maximum of eleven.', kind='criterion')],
        [region(34, .065, .447), region(35, .065, .735)], [region(28, .446, .548)], q17, marks=11, extra=('4-3-1',))
    add('q17av', 'Q17(a)(v)', '4-3-1', 'beef-cattle|fertilisers-pollution-environment-cycles', 'missed-performance-targets',
        'Outline the consequences for the profitability and/or environmental footprint of the beef production system, if performance targets are not achieved.',
        [menu(['Cattle that fail to reach target daily live-weight gain (DLWG) take longer to reach slaughter weight', 'increases the length of the finishing period - meaning more feed or bedding or labour or housing required',
               'reduced animals that can be finished each year', 'inefficient use of inputs (feed, fertiliser and veterinary costs)',
               'Underperforming cattle produce emissions for longer periods because they are on the farm for more time', 'increased greenhouse gas emissions (per kilogram of beef produced)',
               'extra feed production or fertiliser use also increase the risk of nutrient losses to water or higher energy use'], [5, 1],
              'Profitability and/or environmental consequences; the first correct point earns 5 marks and the second 1.')],
        [region(36, .065, .106)], [region(28, .548, .845)], q17)
    q17b = 'Ireland is internationally recognised for producing high-quality food from grass-based systems. Over 90% of Irish beef and dairy products come from animals raised on pasture.'
    add('q17bi', 'Q17(b)(i)', '3-3-2', 'grassland|beef-cattle', 'irish-grass-based-farming', 'Explain how Ireland’s climate and agricultural practices support grass-based farming.',
        [menu('Ireland has a mild, temperate climate with few extremes of heat or cold|regular rainfall ensures consistent grass growth throughout most of the year|long grazing season (up to 300 days in many areas)|farmers use rotational grazing to maintain high-quality leafy grass|soil testing or liming optimise pH and nutrient availability|use of high-yielding grass or clover varieties improves pasture output|grass-based systems reduce reliance on imported feeds or fertilisers', [5, 1])],
        [region(36, .297, .363)], [region(29, .066, .252)], extra=('4-3-1',))
    add('q17bii', 'Q17(b)(ii)', '4-3-1', 'beef-cattle', 'grass-fed-beef-statements',
        'In relation to grass-fed beef identify whether the following statements are true or false by placing a tick (✓) in the correct box. The first one has been done as an example.',
        [menu(['False', 'False', 'True', 'False'], [3, 3, 1, 1],
              'In order: a High in fat — False; b Lower in omega-3 fatty acids — False; c Higher levels of CLA (Conjugated Linoleic Acid) — True; d Lower in beta-carotene — False. The scheme prints 2(3)+2(1): the first two correct answers earn 3 marks each and the next two 1 each.')],
        [region(37, .065, .336)], [region(29, .252, .334)], q17b)
    add('q17biii', 'Q17(b)(iii)', '4-3-1', 'beef-cattle|dairy-cattle', 'traceability-origin-labelling',
        'Outline two reasons why food traceability and origin labelling are important to consumers of Irish meat and dairy.',
        [menu('Food safety - tracked from farm to fork|consumer confidence – ensures trust in product|allows consumers to choose food that is produced in Ireland|associated with high animal welfare or environmental standards|supports local farmers|ensures consumers know the true origin of their food.', [5, 1])],
        [region(36, .297, .338), region(37, .353, .395)], [region(29, .334, .469)], q17b)

    q18 = 'Plant and animal breeding play a vital role in improving the productivity, sustainability, and profitability of Irish agriculture.'
    add('q18a', 'Q18(a)', '4-3-2', 'genetics', 'progeny-performance-testing', 'Compare progeny testing and performance testing.',
        [point('Comparison of the performance of an organism’s offspring with another organism’s offspring (kept under the same conditions)', 2, 'Progeny testing.'),
         point('Comparison of an organism’s traits or performance with another organism kept under the same conditions', 2, 'Performance testing.')],
        [region(38, .065, .19)], [region(29, .469, .604)], q18)
    add('q18bi', 'Q18(b)(i)', '4-3-2', 'genetics|dairy-cattle', 'selective-breeding-benefits',
        'A dairy farmer selects cows with high milk yield and good fertility. Explain how selective breeding and genetic improvement benefit the herd over several generations.',
        [menu('(Increased production) - average milk yield or milk solids of the herd increases|increased fertility or shorter calving intervals or more calves per cow lifetime|cows become more efficient|improved health or longevity', [5, 2])],
        [region(38, .065, .135), region(38, .415, .474)], [region(29, .604, .721)], q18)
    add('q18bii', 'Q18(b)(ii)', '4-3-2', 'genetics', 'breeding-recording-systems',
        'Describe how a recording system (e.g. Irish Cattle Breeding Federation (ICBF) for cattle and Department of Agriculture, Food and Marine (DAFM) for variety lists for plants) helps farmers make genetic decisions.',
        [menu('(Informed genetic decisions) - provides farmers with reliable information on the genetic performance of breeding stock or plant varieties|farmers can select animals or plants with proven genetic merit|higher productivity|better fertility|improved health or disease resistance|greater profitability', [5, 2])],
        [region(38, .065, .135), region(38, .661, .72)], [region(29, .721, .860)], q18, extra=('3-3-1',))
    add('q18biii', 'Q18(b)(iii)', '4-3-2', 'genetics', 'animal-plant-breeding-traits', 'State genetic traits of importance in:',
        [menu(['milk yield', 'fertility', 'calving difficulty', 'carcass traits', 'health data', 'any valid genetic trait',
               'Yield', 'disease resistance', 'straw strength', 'quality traits (digestibility, etc)', 'any valid genetic trait'], [5, 2],
              'One trait under each heading: the first six options are for Animal breeding and the last five for Plant breeding. The first correct heading earns 5 marks and the second 2.')],
        [region(39, .065, .226)], [region(30, .066, .205)], q18, extra=('3-3-1',))
    q18c = 'The table below shows two varieties of wheat. Wheat A: disease resistance High, yield 8.1 t/ha, maturity 115 days. Wheat B: disease resistance Moderate, yield 8.9 t/ha, maturity 124 days. Analyse the data and answer the questions that follow.'
    add('q18ci', 'Q18(c)(i)', '3-3-1', 'genetics|crop-production', 'wheat-variety-choice', 'Which variety would you recommend for an early-harvest system with low chemical input?',
        [point('Wheat A', 5)], [region(39, .229, .403)], [region(30, .205, .270)], q18c, extra=('1-3',))
    add('q18cii', 'Q18(c)(ii)', '3-3-1', 'genetics|crop-production', 'wheat-variety-justification', 'Justify your choice in part (i) above, with two reasons.',
        [menu('Matures (9 days) earlier than Wheat B|it has higher disease resistance (so reduced chemical requirement)', [4, 4])],
        [region(39, .229, .356), region(39, .473, .497)], [region(30, .270, .336)], q18c + ' Part (i) recommends a variety for an early-harvest system with low chemical input.', extra=('1-3',))
    domains = {
        'plants': ('In plants', '3-3-1', ['Select for traits such as disease resistant',
                    'tolerance to acidic soils or waterlogging or drought or low fertility (e.g. certain grass or cereal varieties have deeper or stronger root systems that allow them to access nutrients and moisture from poor or dry soils)']),
        'animals': ('In livestock', '4-3-2', ['select animals that are better adapted to specific soil and grazing conditions. (e.g. hardy)',
                     'Native cattle or sheep breeds cope better on wet, heavy soils and are less prone to lameness',
                     'animals with efficient feed conversion or strong immune systems perform better on land with lower grass quality']),
    }
    for key, (label, topic, pool) in domains.items():
        add('q18ciii-route-' + key, f'Q18(c)(iii) — {key}', topic, 'genetics|soil-science', 'genetic-traits-soil-conditions',
            'Explain how genetic traits in plants or animals can help farmers respond to soil conditions.',
            [menu(pool, [3], label + '.')], [region(39, .627, .67)], [region(30, .336, .585)],
            f'Practice choice: {key}.', selection={'kind': 'closed', 'choose': 1, 'options': list(domains), 'route': [key]}, extra=('2-3',))
    q18d = ('‘Genocells’ is a new emerging technology available for genotyped dairy herds. Bulk milk samples were tested with an accuracy of 90 – 98% for Somatic Cell Count (SCC). '
            'Together with milk recording, this allows for better management of SCC throughout the lactation period. (Adapted from Teagasc, 2025)')
    add('q18di', 'Q18(d)(i)', '4-3-2', 'genetics|innovation-and-biotechnology-in-agriculture', 'genotyped-definition', 'Explain the underlined term.',
        [point('Genetic make-up of an organism determined', 2)], [region(40, .065, .245)], [region(30, .585, .633)], q18d + ' [The term underlined on the paper is: genotyped]')
    add('q18dii', 'Q18(d)(ii)', '4-3-3', 'dairy-cattle|animal-diseases', 'somatic-cell-count-management',
        'Explain how the better management of SCC throughout the lactation period can benefit farmers.',
        [menu('Ensuring low SCC reduces the incidence of mastitis|(healthy udders) produce better quality milk or higher milk yields|fewer discarded milk days due to antibiotic treatments|milk with a low SCC attracts bonus payments from processors or avoids penalties|less need to cull (reducing replacement costs and improving genetic progress in the herd)|enhances animal welfare|reduces veterinary or labour costs', [5, 2])],
        [region(40, .065, .215), region(40, .348, .391)], [region(30, .633, .807)], q18d)
    assert len(cards) == 112, len(cards)
    return cards, tasks
