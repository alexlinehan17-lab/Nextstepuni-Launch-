"""2026 Ordinary tasks from the complete original paper/scheme review.

All 40 paper pages and 24 scheme pages were inspected before authoring; the
independent census in agricultural_science_census.py was transcribed first.
Every printed finite pool expands mechanically: Q1(a), Q5(a), Q14(a)(i) and
Q18(b)(ii) three of four; Q4(a), Q9(b)(i) and Q10(a) two of three; Q4(b) one
of three hazards; Q9(a) three of five safety features. Ticks that identify the
single correct answer are answer identification, not routes.
"""
from itertools import combinations
from agricultural_science_2010_hl import point, menu, region
from agricultural_science_2010_parity import scan
from agricultural_science_2011_hl import variants

FILE = 'LC024GLP000EV.pdf'
YEAR = 2026
HASHES = {'exampapers':'b63e7223ff6e0b724984b51db9b1813f37d19496570b7614694abc85f5702e2f',
          'markingschemes':'5d408c95790f05c59a313f8b2e30ed789d36ddfbbe23da59474d5db79a7e1e8a'}
SELECTIONS = {
    '12643a33f3a32b31':('exam-selection','Section A: ten of twelve independent questions. Every question and both sides of each internal choice are retained.'),
    'e8ef67ddf417a212':('exam-selection','Section B: four of six independent questions. Every question is retained.'),
    '9279a5994cd75306':('exam-selection','Repeated Section A instruction: ten independent 10-mark questions, all retained.'),
    '68cb0434414120e1':('closed','Q1(a) prints machines A–D and asks for any three: all four three-picture routes are retained at 6 marks each.'),
    'e82de7fc3df02343':('independent-task-selection','Q3 either (a) or (b): both alternatives are retained.'),
    'b37292626d759374':('closed','Q4(a) prints hazards A, B and C and asks for any two: all three two-hazard routes are retained at 6 marks each.'),
    'eef9f5121da5b37c':('closed','Q4(b) asks for any one of the three printed hazards: three routes, each with its own scheme measures, at 2 marks.'),
    '31d5f1b76a0150b1':('closed','Q5(a) prints cattle A–D and asks for any three: all four routes are retained at 7 marks each.'),
    'e526e5630e3eef3e':('independent-task-selection','Q8 either (a) or (b): both alternatives are retained.'),
    'e84ceadf8f49b84e':('independent-task-selection','Q9 either (a) or (b): both alternatives are retained.'),
    'b4dda66070736477':('closed','Q9(a) prints five safety features and asks for a reason for any three: all ten routes are retained at 10 marks each.'),
    'd67d299c87eb8406':('closed','Q9(b)(i) prints signs A, B and C and asks for any two: all three routes are retained at 5 marks each.'),
    '548b7645ecdfb3cb':('closed','Q10(a) prints three plants and asks for the lifecycle of any two: all three routes are retained at 6 marks each.'),
    'f08ddcaeb5138cee':('independent-task-selection','Q12 either (a) or (b): both alternatives are retained.'),
    '024b108b32f221f3':('exam-selection','Section B heading: four of six independent 50-mark questions, all retained.'),
    '2c4216f9686097b8':('closed','Q14(a)(i) prints sheep A–D and asks for any three: all four routes are retained at 6 marks each.'),
    '8bc895fb618589af':('independent-task-selection','Q15: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    '1e3a8ee0704d5ce3':('answer-identification','Q15(d)(ii): identify the one method the cows preferred from the graph; one correct answer, not a route.'),
    'b7955337ee8d60ec':('independent-task-selection','Q16: (a) and (b) with either (c) or (d). Every part, including both (c) and (d), is retained.'),
    'c5a0a84851b40d40':('not-a-selection','Prose in the Q16(c) stem ("one of the calves"); no response choice.'),
    '255d6f8999e58e46':('answer-identification','Q18(a)(iv): tick the two correct contributors; the third box is a distractor, not a route.'),
    '1a034decc5bb8379':('closed','Q18(b)(ii) prints udder parts A–D and asks for any three: all four routes are retained at 9 marks each.'),
}
SUPPLEMENTARY = [
    (26,'Identify which machine A or B','answer-identification','Q15(c): the scheme accepts machine A only; B is not an alternative route.'),
    (31,'any of the machines shown','open','Q17(b)(ii): one safety measure for any machine shown; the scheme gives general measures, not per-machine pools.'),
    (22,'under the','required-condition','Q14(b)(ii): Feeding, Housing and Health are required headings, one point each.'),
    (32,'under the following headings','required-condition','Q17(c): every printed heading is required and separately marked.'),
    (27,'State if these calves are more likely','answer-identification','Q16(a)(ii): tick the one correct box (Dairy).'),
]
SOURCE_NOTES = {
    'q11a':'The scheme labels both parts of Question 11 “(b)”. Its first row (4 marks, Monogastric) is the paper’s part (a).',
    'q13aiii':'The scheme heading refers to “your answer in part (i)”; the paper asks for a reason for the answer to part (ii), the best stage for cutting silage.',
}


def paper_review():
    observed, supplementary = scan(YEAR, FILE, HASHES, SELECTIONS, SUPPLEMENTARY)
    refs = {'q11a':('11','Q11(a)'), 'q13aiii':('13','Q13(a)(iii)')}
    notes = [dict(questionN=refs[key][0], questionRef=refs[key][1], note=note) for key, note in SOURCE_NOTES.items()]
    return dict(year=YEAR, level='ordinary', lang='ev', paperFileid=FILE, hashes=HASHES,
                wholePaperVisualReview='reviewed', schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1, 41)), schemePagesInspected=list(range(1, 25)),
                selectionDirectives=observed, supplementarySelections=supplementary, sourceNotes=notes,
                independentBoundaryReview='85 base tasks and 114 routes. Closed pools: Q1(a), Q5(a), Q14(a)(i), Q18(b)(ii) three of four (4 each); Q4(a), Q9(b)(i), Q10(a) two of three (3 each); Q4(b) one of three (3); Q9(a) three of five (10). Pooled first-correct scales stay whole; drawings, graphs and the calculation keep manual totals.',
                cropVisualReview='Every distinct paper/scheme crop pair rendered and inspected, with three paper diagram crops and two scheme solution images.',
                runtimeReview='Integrated production-component cases at 1200px and 390px. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison (deferred)', 'Full application navigation review', 'Corpus-wide reconciliation'])


def reviewed_tasks():
    paper_review()
    cards, tasks = [], []

    def add(key, ref, topic, atlas, concept, question, rows, pp, sp, stem=None, marks=None, selection=None, figure=None, labels=None, extra=()):
        cid = 'agsci-2026-ol-' + key
        rows = [dict(row, id=f'r-{i+1}') for i, row in enumerate(rows)]
        card = dict(id=cid, subjectId='agricultural-science', year=YEAR, level='ordinary',
                    section='A' if int(ref.split('(')[0].split()[0][1:]) <= 12 else 'B',
                    questionRef='2026 OL ' + ref, topicId='agsci-' + topic,
                    curriculumNodeIds=['agsci-' + t for t in (topic, *extra)],
                    conceptId=concept, questionText=question, rows=rows,
                    totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                    tariffModel={'kind': 'questionTotal' if marks is not None else 'fixed'},
                    sourceMaterial=dict(kind='source-text', label='OFFICIAL QUESTION PAGE', title='Agricultural Science 2026 Ordinary — ' + ref,
                        pages=sorted({r['p'] for r in pp}), attribution='SEC Agricultural Science 2026 Ordinary Level examination paper — © State Examinations Commission.',
                        presentationNote='Open the original page for the published wording, photographs, diagrams and examination context.'))
        if extra:
            card['additionalTopicIds'] = ['agsci-' + t for t in extra]
        if stem: card['stem'] = stem
        if figure: card['figureKey'] = figure
        if labels: card['labelKey'] = labels
        task = dict(questionRef=card['questionRef'], paperPage=pp[0]['p'], schemePage=sp[0]['p'], paperRegions=pp, schemeRegions=sp,
                    atlasNumbers={cid: str(1001 + len(cards))}, cardIds=[cid], marksPerRoute=card['totalMarks'],
                    examTopicIds=['agricultural-science-ordinary-' + t for t in atlas.split('|')],
                    selection=selection or {'kind': 'none', 'reason': 'Required response. Open examples and scheme alternatives remain marking menus, not finite printed routes.'},
                    evidence='All 40 paper and 24 scheme pages visually inspected. Published task boundaries and awards independently transcribed before authoring.')
        if key in SOURCE_NOTES:
            task['schemeNote'] = SOURCE_NOTES[key]
            rows[0]['contextNote'] = (rows[0].get('contextNote', '') + ' ' + SOURCE_NOTES[key]).strip()
        cards.append(card); tasks.append(task)
        return card

    def routes(key, ref, topic, atlas, concept, question, pool, k, steps, pp, sp, stem, note, extra=(), figure=None, labels=None, points=False):
        for chosen in combinations(pool, k):
            letters = [c[0] for c in chosen]
            rows = ([point(text, s, label + '.') for (label, text), s in zip(chosen, steps)] if points
                    else [menu([text for _, text in chosen], steps, note)])
            add(f'{key}-route-' + ''.join(l.lower() for l in letters) if all(len(l) == 1 for l in letters) else f'{key}-route-' + '-'.join(letters),
                f'{ref} — ' + ', '.join(letters), topic, atlas, concept, question, rows, pp, sp,
                (stem + ' ' if stem else '') + 'Practice choice: ' + ', '.join(letters) + '.',
                selection={'kind': 'closed', 'choose': k, 'options': [c[0] for c in pool], 'route': letters}, extra=extra, figure=figure,
                labels=[dict(l, askedInThisQuestion=l['letter'] in letters) for l in labels] if labels else None)

    # Section A ---------------------------------------------------------------
    machines = [('A', 'A – combine harvester'), ('B', 'B – plough'), ('C', 'C – drone sprayer'), ('D', 'D - topper')]
    routes('q1a', 'Q1(a)', '3-3-1', 'health-safety|crop-production', 'farm-machinery-identification',
        'Identify any three pieces of equipment commonly found on Irish farms using the words in the list below.',
        machines, 3, [2, 2, 2], [region(3, .148, .705)], [region(12, .132, .252)], None, None, points=True)
    add('q1b', 'Q1(b)', '1-5', 'health-safety', 'drone-sprayer-safety',
        'Outline one safety precaution farmers must take when using the piece of machinery in picture C in part (a) above.',
        [menu(['Be careful wind doesn’t catch it or avoid flying in adverse weather conditions', 'ensure it only flies over target or avoid collisions area or fly (at least 50 metres) away from individuals',
               'ensure it doesn’t come down on someone', 'avoid overhead power lines', 'wear PPE during chemical spraying', 'avoid moving parts', 'avoid spraying where animals are grazing'], [4])],
        [region(3, .148, .815)], [region(12, .252, .403)], 'Picture C in part (a) shows a drone sprayer.')

    q2 = 'Sustainable farming is very important for Irish farmers. Analyse the picture and answer the questions that follow.'
    add('q2a', 'Q2(a)', '2-3', 'fertilisers-pollution-the-environment', 'sustainable-farming-water-quality',
        'Identify how sustainable farming improves water quality, by placing a tick (✓) in the correct box.',
        [point('Reduces soil erosion and run off', 3, 'The scheme ticks this box.')], [region(4, .062, .54)], [region(12, .403, .492)], q2)
    add('q2b', 'Q2(b)', '3-3-2', 'fertilisers-pollution-the-environment|crop-production', 'sustainable-farming-yield',
        'Outline one way sustainable farming can increase the yield of crops.',
        [menu('Improved soil structure|improve soil health|increased nutrient availability|enhanced water retention|break pest and disease cycles or IPM (Integrated Pest Management) controls pests without stunting crop growth|reduce soil erosion|increase pollinators|polyculture maximises space', [3])],
        [region(4, .062, .432), region(4, .54, .665)], [region(12, .492, .611)], q2)
    add('q2c', 'Q2(c)', '3-3-2', 'fertilisers-pollution-the-environment', 'pollinator-habitats', 'Outline two ways farmers can provide habitats for pollinators on their farms.',
        [menu('Plant mixed species|sow cover crops|plant native trees|reduce chemical sprays|field margins|hedgerows|riparian or buffer zones|low intensity mowing|timing of pesticide application|create habitats', [1, 3])],
        [region(4, .062, .432), region(4, .664, .78)], [region(12, .611, .694)], q2, extra=('2-3',))

    q3a = 'The diagram shows photosynthesis in plants. Analyse the diagram and answer the questions that follow.'
    add('q3ai', 'Q3(a)(i)', '3-1', 'plant-physiology', 'photosynthesis-inputs-outputs',
        'Identify one input (requirement) and one output (product) in the process of photosynthesis.',
        [menu(['Carbon dioxide', 'water', 'light'], [2], 'Input.'), menu(['Glucose', 'oxygen'], [2], 'Output.')],
        [region(5, .062, .275)], [region(12, .694, .776)], q3a)
    add('q3aii', 'Q3(a)(ii)', '3-3-2', 'plant-physiology|crop-production', 'photosynthesis-crop-yields',
        'List two ways farmers use their knowledge of photosynthesis to improve crop yields.',
        [menu(['Correct seed rate', 'ensure max light or canopy management or row orientation or aspect or supplemental lighting or plastic mulches', 'efficient water or irrigation',
               'increase CO₂ by using a greenhouse', 'increased soil organic matter', 'increased nutrient availability', 'superior seed selection', 'ventilation control'], [3, 3])],
        [region(5, .062, .285), region(5, .284, .40)], [region(12, .776, .892)], q3a, extra=('3-1',))
    root = 'Study the diagram of the plant root.'
    add('q3bi', 'Q3(b)(i)', '3-1', 'plant-physiology', 'root-hair-location', 'Identify the presence of the root hair by placing an R on its location in the diagram.',
        [point('Correct placement on diagram (anywhere on or around the root hair on the right-hand side of the diagram).', 3, kind='criterion')],
        [region(5, .474, .655)], [region(13, .100, .220)], root, figure='agsci-2026-ol-scheme-root-hair')
    add('q3bii', 'Q3(b)(ii)', '3-1', 'plant-physiology|soil-science', 'root-mineral-uptake', 'State one important mineral that plants take in through their roots.',
        [point('N, P, K, S, Mg, Ca or any valid example', 3, 'Any one valid mineral.')],
        [region(5, .474, .70)], [region(13, .220, .268)], root)
    add('q3biii', 'Q3(b)(iii)', '2-2-2', 'plant-physiology|soil-science', 'nutrient-uptake-barriers',
        'A farmer notices that plants are not growing well, even though the soil looks healthy. Identify two possible reasons why nutrients might not be reaching the plant roots properly by placing ticks (✓) in the correct boxes.',
        [menu(['Soil is too compacted', 'Incorrect pH'], [2, 2], 'The scheme ticks these two boxes.')],
        [region(5, .695, .865)], [region(13, .268, .373)], extra=('3-1',))

    q4 = ('The map below is a hand sketch drawn by an Agricultural Science student on a farm visit. The student identified three potential hazards on the farm and labelled them A, B and C. '
          'Analyse the sketch and answer the questions that follow.')
    hazards = [('A', 'A – slurry gases or falling into tank or beware of animal movement or moving vehicles'),
               ('B', 'B – Moving machinery or items falling off pit or falls from pit (walls)'),
               ('C', 'C – moving machinery or risk of falling objects or disease risk from rodents')]
    hazard_labels = [dict(letter='A', meaning='slurry gases or falling into tank or beware of animal movement or moving vehicles'),
                     dict(letter='B', meaning='Moving machinery or items falling off pit or falls from pit (walls)'),
                     dict(letter='C', meaning='moving machinery or risk of falling objects or disease risk from rodents')]
    routes('q4a', 'Q4(a)', '1-5', 'health-safety', 'farmyard-hazards', 'Identify any two potential safety hazards labelled A, B and C.',
        hazards, 2, [2, 4], [region(6, .062, .605)], [region(13, .373, .492)], q4,
        'Identify the hazard at each of your two chosen letters. The first correct hazard earns 2 marks and the second 4.',
        figure='agsci-2026-ol-paper-farm-hazards', labels=hazard_labels)
    measures = {'A': ['do not enter shed during agitating', 'keep cover on tank', 'beware of animal or machinery movement', 'keep gates closed'],
                'B': ['beware of any moving machinery', 'have side rails on pit', 'do not go under the silage cover'],
                'C': ['be aware of moving machinery or falling objects', 'wash hands after handling feed']}
    for letter, pool in measures.items():
        add('q4b-route-' + letter.lower(), f'Q4(b) — {letter}', '1-5', 'health-safety', 'reducing-farmyard-risk',
            'For any one safety hazard identified in part (a), suggest one measure the farmer could take to reduce the potential risk.',
            [menu(pool, [2], f'One measure for hazard {letter}. The scheme accepts any valid example for each hazard.')],
            [region(6, .062, .545), region(6, .613, .745)], [region(13, .492, .665)], q4 + f' Practice choice: hazard {letter}.',
            selection={'kind': 'closed', 'choose': 1, 'options': list(measures), 'route': [letter]})
    add('q4c', 'Q4(c)', '1-5', 'health-safety|animal-production', 'separating-animals-machinery',
        'Explain why it is important to separate animal movement areas from machinery routes in a farmyard.',
        [menu('Avoid animals escaping|ensure machines don’t run into animals|(human) safety|biosecurity or disease control|farm efficiency or traffic flow', [2])],
        [region(6, .062, .15), region(6, .745, .84)], [region(13, .665, .764)], q4)

    cattle = [('A', 'A – Aberdeen Angus'), ('B', 'B – Friesian or Holstein or Holstein Friesian'), ('C', 'C – Shorthorn'), ('D', 'D – Simmental')]
    routes('q5a', 'Q5(a)', '4-2', 'classification-of-organisms|animal-production', 'cattle-breed-identification',
        'Identify any three cattle breeds found on Irish farms using the list of words below.', cattle, 3, [1, 2, 4],
        [region(7, .062, .64)], [region(13, .764, .883)], None,
        'Identify the three pictured breeds you chose. The scheme prints 1+2+4: the first correct breed earns 1 mark, the second 2 and the third 4.')
    add('q5b', 'Q5(b)', '4-2', 'classification-of-organisms|animal-production', 'roan-colour',
        'Identify which animal A, B, C or D in part (a) above has a roan colour, by placing a tick (✓) in the correct box.',
        [point('C', 3, 'The scheme ticks C.')], [region(7, .062, .83)], [region(14, .082, .163)])

    add('q6', 'Q6', '3-3-2', 'fertilisers-pollution-the-environment', 'organic-farming-statements',
        'In relation to organic farming, indicate if the following are true or false by placing a tick (✓) in the correct box. The first one has been done as an example.',
        [menu(['True', 'False', 'True', 'True', 'False'], [1, 1, 2, 2, 4],
              'In order: (i) The use of synthetic chemical fertilisers is not allowed — True; (ii) Reduces the number of pollinators — False; (iii) Aims to improve soil health — True; '
              '(iv) Crop rotation is a common practice — True; (v) Genetically modified organisms (GMOs) are allowed — False. The scheme prints 1+1+2+2+4 for one to five correct answers.')],
        [region(8, .062, .465)], [region(14, .163, .262)],
        'Organic farming is becoming more popular in Ireland as consumers look for food that is produced in a more natural and environmentally friendly way.', extra=('2-3',))
    add('q7', 'Q7', '4-1', 'animal-production|animal-physiology', 'dairy-breeding-cycle',
        'Complete the breeding cycle of a dairy cow only using the number of days in the following list.',
        [menu(['365', '21', '45', '283'], [2, 2, 3, 3],
              'In order: Calving interval (calving to calving) 365; Oestrus (heat) 21; Mating (in calf) 45; Mating to calving (gestation) 283. The scheme prints 2(2)+2(3).')],
        [region(8, .47, .83)], [region(14, .262, .428)], 'Number of days: 283, 365, 21, 45.', extra=('4-3-2',))

    q8a = 'Healthy soils are full of biological activity. Living organisms play a key role in maintaining soil fertility and supporting plant growth.'
    add('q8ai', 'Q8(a)(i)', '2-2-3', 'soil-science', 'soil-organisms', 'Name two types of living organisms commonly found in soil.',
        [menu('Bacteria|fungi|actinomycetes|algae|earthworms|protozoa|nematodes|arachnids|insects|(burrowing) mammals', [2, 2])],
        [region(9, .062, .235)], [region(14, .428, .494)], q8a)
    add('q8aii', 'Q8(a)(ii)', '2-2-3', 'soil-science', 'soil-organism-benefits', 'Explain two benefits that soil organisms provide for crops or pasture.',
        [menu('Nutrient cycling|nutrient availability or organic matter degradation|improved soil structure|moisture retention|improved aeration or drainage|disease and pest management|nitrogen fixation', [2, 4])],
        [region(9, .088, .128), region(9, .242, .36)], [region(14, .494, .598)], q8a)
    q8b = 'A student carried out an investigation to determine the pH of the soil and used the following equipment: Deionised water, pH meter or pH paper, filter paper, soil sample, glass rod.'
    add('q8bi', 'Q8(b)(i)', '1-2', 'soil-science|scientific-practices-experiments-investigations', 'soil-ph-glass-rod', 'Outline the use of the glass rod in this investigation.',
        [point('To stir the mixture of soil and water', 3)], [region(9, .425, .615)], [region(14, .612, .746)], q8b, extra=('2-2-1',))
    add('q8bii', 'Q8(b)(ii)', '1-2', 'soil-science|scientific-practices-experiments-investigations', 'soil-ph-filter-paper', 'Why did the student use the filter paper?',
        [menu(['To keep the soil in the paper and allow the water to pass through', 'clear water to see colour change'], [3])],
        [region(9, .425, .525), region(9, .62, .71)], [region(14, .746, .812)], q8b, extra=('2-2-1',))
    add('q8biii', 'Q8(b)(iii)', '1-2', 'soil-science|scientific-practices-experiments-investigations', 'soil-ph-measurement', 'Describe how the student used the pH meter or pH paper.',
        [menu(['Wash the probe of the meter with deionised water or remove a strip of pH paper', 'place the pH meter or pH paper into the water', 'read the pH meter or compare colour change to colour chart'], [2, 2])],
        [region(9, .425, .525), region(9, .714, .825)], [region(14, .812, .898)], q8b, extra=('2-2-1',))

    q9 = ('The 2022 Teagasc National Farm Survey states that over 50% of all farming accidents involved livestock, with incidents involving calving cows being the most common. '
          'Entering a pen with a cow and calf can be very dangerous.')
    features = [('Lock cows in a proper calving gate', 'Lock cows in a proper calving gate – to restrain the animal when working with them / after calving cows are very protective of calf'),
                ('Good handling facilities when moving cows to and from calving pens', 'Good handling facilities when moving cows to and from calving pens – they don’t escape / they don’t hurt themselves or keeps them calm / easier to handle or isolate / after calving cows are very protective of calf'),
                ('Have two escape points in a calving pen', 'Have two escape points in a calving pen – ensure you can get out quick as possible / in case one route is blocked / after calving cows are very protective of calf'),
                ('Never turn your back on a freshly calved cow', 'Never turn your back on a freshly calved cow – always observe the cow incase she goes to attack / you can get out of pen / after calving cows are very protective of calf'),
                ('Keep dogs/children away from calving shed', 'Keep dogs / children away form calving shed – dogs and children can aggravate cows / after calving cows are very protective of calf')]
    keys = ['gate', 'handling', 'escape', 'back', 'dogs']
    for chosen in combinations(range(5), 3):
        labels = [features[i][0] for i in chosen]
        add('q9a-route-' + '-'.join(keys[i] for i in chosen), 'Q9(a) — ' + ', '.join(labels), '1-5', 'health-safety|animal-production', 'calving-safety',
            'Some safety features to prevent injury during the calving season are outlined in the table below. Outline one reason for any three safety features.',
            [menu([features[i][1] for i in chosen], [2, 3, 5],
                  'One reason for each of your three features. (Accept after calving cows are very protective of calf once only). The scheme prints 2+3+5.')],
            [region(10, .062, .84)], [region(15, .082, .465)], q9 + ' Practice choice: ' + '; '.join(labels) + '.',
            selection={'kind': 'closed', 'choose': 3, 'options': keys, 'route': [keys[i] for i in chosen]})
    signs = [('A', 'A – Beware of bull'), ('B', 'B – Poisonous or toxic'), ('C', 'C – Beware of machinery')]
    routes('q9bi', 'Q9(b)(i)', '1-5', 'health-safety', 'farm-safety-signs', 'Explain the meaning of any two signs A, B or C to the group of farmers.',
        signs, 2, [2, 3], [region(11, .09, .515)], [region(15, .478, .579)], 'You are on a farm with a group of farmers and you come across the following signs.',
        'Meanings of your two chosen signs. The first correct meaning earns 2 marks and the second 3.')
    add('q9bii', 'Q9(b)(ii)', '1-5', 'health-safety|animal-diseases', 'farm-biosecurity',
        'You also notice a sign saying ‘biosecurity measures in place’ to prevent diseases entering the farm. Outline two biosecurity measures the farmer could put in place on the farm.',
        [menu('Footbath|quarantine sick animals|closed herd|restrict visitors or any valid example', [2, 3])],
        [region(11, .09, .115), region(11, .515, .68)], [region(15, .579, .645)], 'You are on a farm with a group of farmers.')

    lifecycles = [('Barley', 'Barley – annual'), ('White clover', 'White clover – perennial'), ('Potato', 'Potatoes – biennial')]
    for chosen in combinations(range(3), 2):
        labels = [lifecycles[i][0] for i in chosen]
        add('q10a-route-' + '-'.join(labels[j].split()[0].lower() for j in range(2)), 'Q10(a) — ' + ', '.join(labels), '3-2', 'classification-of-organisms', 'plant-lifecycles',
            'Identify the correct lifecycle for any two of the plants below, by placing a tick (✓) in the correct box.',
            [menu([lifecycles[i][1] for i in chosen], [3, 3], 'Tick the lifecycle of each of your two chosen plants, 2(3).')],
            [region(12, .062, .675)], [region(15, .645, .747)], 'Practice choice: ' + ', '.join(labels) + '.',
            selection={'kind': 'closed', 'choose': 2, 'options': [p for p, _ in lifecycles], 'route': labels})
    add('q10b', 'Q10(b)', '3-3-2', 'grassland|crop-production', 'grassland-weed-control', 'Explain how a farmer would control weeds in a grass field.',
        [menu('Fertilising|topping|rotational grazing|reseeding|crop rotation|machine hygiene|certified seed|herbicide or spot spraying|hand rogueing or picking', [2, 2])],
        [region(12, .678, .82)], [region(15, .747, .833)])

    add('q11a', 'Q11(a)', '4-1', 'animal-physiology', 'monogastric-pig',
        'Identify if a pig is a ruminant or a monogastric by placing a tick (✓) in the correct box.',
        [point('Monogastric', 4, 'The scheme ticks Monogastric.')], [region(13, .062, .55)], [region(16, .082, .156)], 'The diagram shows the digestive system of a pig.')
    add('q11b', 'Q11(b)', '4-1', 'animal-physiology', 'pig-digestive-system-labels', 'Label A, B and C on the diagram using the list of words below.',
        [point('Stomach', 2, 'A.'), point('Colon', 2, 'B.'), point('Rectum', 2, 'C.')],
        [region(13, .062, .74)], [region(16, .156, .238)], 'The diagram shows the digestive system of a pig. Words: rectum, stomach, colon.',
        figure='agsci-2026-ol-paper-pig-digestive',
        labels=[dict(letter='A', meaning='Stomach', askedInThisQuestion=True), dict(letter='B', meaning='Colon', askedInThisQuestion=True), dict(letter='C', meaning='Rectum', askedInThisQuestion=True)])

    add('q12ai', 'Q12(a)(i)', '2-2-2', 'soil-science', 'soil-composition-calculation', 'Calculate A the % organic matter in the sample of soil.',
        [point('25 + 25 + 45 = 95', None, 'Addition: 1 mark.', kind='criterion'),
         point('100 – 95 = 5%', None, 'Subtraction: 1 mark. Allow 4 marks for correct answer only.', kind='criterion')],
        [region(14, .062, .42)], [region(16, .238, .345)], 'The chart shows the ideal soil composition for a sample of soil: Mineral 45%, Water 25%, Air 25%, Organic matter A.', marks=4, extra=('1-3',))
    add('q12aii', 'Q12(a)(ii)', '2-2-2', 'soil-science|scientific-practices-experiments-investigations', 'hand-texture-test',
        'An Agricultural Science student wanted to determine the texture of a soil sample they got on a farm walk. Using the hand testing method, explain how the student determined the texture of the soil.',
        [menu('Get sample of dry soil|rub between fingers|note grittiness or description of|add water|try roll into a ball|try to form a thread|try to form thread into a ring|compare to texture flow chart or described result', [2, 2, 2])],
        [region(14, .42, .49)], [region(16, .345, .465)], extra=('1-2',))
    sed = 'A student wanted to determine the texture of two soil samples using the sedimentation method. They set up an investigation using the following method.'
    add('q12bi', 'Q12(b)(i)', '1-2', 'soil-science|scientific-practices-experiments-investigations', 'sedimentation-equipment',
        'Identify the pieces of equipment labelled A and B in the diagram.',
        [point('graduated cylinder', 2, 'A.'), point('funnel', 2, 'B.')], [region(15, .09, .51)], [region(16, .478, .545)], sed,
        figure='agsci-2026-ol-paper-sedimentation',
        labels=[dict(letter='A', meaning='graduated cylinder', askedInThisQuestion=True), dict(letter='B', meaning='funnel', askedInThisQuestion=True)])
    add('q12bii', 'Q12(b)(ii)', '2-2-2', 'soil-science|scientific-practices-experiments-investigations', 'sedimentation-water',
        'Outline one reason why water is mixed with the soil at the beginning of the investigation.',
        [menu(['To form a soil solution', 'to break up or separate the different sized particles'], [3])],
        [region(15, .09, .41), region(15, .511, .555)], [region(16, .545, .627)], sed, extra=('1-2',))
    add('q12biii', 'Q12(b)(iii)', '2-2-2', 'soil-science|scientific-practices-experiments-investigations', 'sedimentation-texture',
        'Explain how the student could determine the texture of each soil sample.',
        [menu(['Allow to settle', 'note the volume of sand, silt and clay in the graduated cylinder (using the graduations on the cylinder)',
               'calculate the % of each compared to the overall volume', 'use the soil textural triangle'], [3])],
        [region(15, .09, .41), region(15, .657, .69)], [region(16, .627, .733)], sed, extra=('1-3',))

    # Section B ---------------------------------------------------------------
    q13 = 'Grass grows in different stages throughout the year. Farmers need to understand these growth stages to manage grazing, silage, and fertiliser properly.'
    add('q13ai', 'Q13(a)(i)', '3-3-2', 'grassland', 'grass-growth-stages',
        'Identify the three stages A, B and C in the growth cycle of a grass plant using the list of words in the table.',
        [point('A – Vegetative', 2), point('B – Elongation', 2), point('C – Reproductive', 2)], [region(18, .148, .672)], [region(17, .135, .234)], q13, extra=('3-1',))
    add('q13aii', 'Q13(a)(ii)', '3-3-3', 'grassland', 'silage-cutting-stage', 'Identify which stage A, B or C is the best stage for cutting grass for silage.',
        [point('A or vegetative', 2)], [region(18, .148, .565), region(18, .672, .72)], [region(17, .234, .299)], q13)
    add('q13aiii', 'Q13(a)(iii)', '3-3-3', 'grassland', 'silage-cutting-reason', 'Outline one reason for your answer in part (ii).',
        [menu(['This is when the digestible sugars are the highest in plant', 'leafy part is more digestible'], [4])],
        [region(18, .672, .70), region(19, .062, .185)], [region(17, .299, .366)], 'Part (ii): identify which stage A, B or C is the best stage for cutting grass for silage.')
    add('q13aiv', 'Q13(a)(iv)', '3-1', 'grassland', 'grass-growth-factors', 'State two factors that affect how grass grows.',
        [menu('Sunlight|water|carbon dioxide (air)|nutrients (Nitrogen is key)|pH level|temperature|oxygen levels|soil compaction|grazing|rest period|sward composition', [4, 4])],
        [region(19, .188, .32)], [region(17, .366, .450)], q13, extra=('3-3-2',))
    add('q13bi', 'Q13(b)(i)', '3-3-3', 'grassland', 'silage-production-order',
        'A farmer wants to produce good quality silage. Place the following steps 1 to 5 in the correct order, to outline the production of good quality silage. Step 1 has been completed for you.',
        [point('2 Mow the grass', 2), point('4 Roll to compact', 2), point('5 Cover the pit', 2), point('3 Wilt for 24 hours', 2)],
        [region(19, .35, .625)], [region(17, .450, .547)], 'Step 1 is Fertilise the field.')
    add('q13bii', 'Q13(b)(ii)', '3-3-3', 'grassland', 'silage-quality-tests',
        'Identify two tests that determine the quality of silage by placing ticks (✓) in the correct two boxes.',
        [menu(['pH', 'Colour'], [3, 3], 'The scheme ticks pH and Colour.')], [region(19, .625, .86)], [region(17, .547, .627)], extra=('1-2',))
    add('q13ci', 'Q13(c)(i)', '1-2', 'grassland|scientific-practices-experiments-investigations', 'dry-matter-procedure',
        'Another test to determine the grass quality is to measure the dry matter (DM). A student carried out this test and took the photographs below of the steps. Complete the table below by placing the photographs (A, B, C and D) in the correct order of how the student carried out this investigation.',
        [point('1st step – C', 2), point('2nd step – D', 2), point('3rd step – A', 2), point('4th step - B', 2)],
        [region(20, .062, .72)], [region(17, .627, .759)], extra=('3-3-2',))
    add('q13cii', 'Q13(c)(ii)', '3-3-2', 'grassland', 'grass-measurement-benefits', 'Outline two benefits of measuring grass on farms.',
        [menu('Data driven approach to management (grazing or winter feed planning)|informed decision making (predicting feed requirements or accurate stocking rates)|cost reduction|best grass utilisation|identify areas for reseeding|environmental benefits', [3, 5])],
        [region(20, .72, .84)], [region(17, .759, .881)])

    q14 = 'Sally and Jess are sheep farmers in Co. Mayo with a mixture of lowland and hill sheep.'
    sheep = [('A', 'A – Texel'), ('B', 'B – Border Leicester'), ('C', 'C – Blackface mountain'), ('D', 'D – Suffolk')]
    routes('q14ai', 'Q14(a)(i)', '4-2', 'animal-production|classification-of-organisms', 'sheep-breed-identification',
        'Identify any three sheep breeds found on their farm using the list below.', sheep, 3, [2, 2, 2],
        [region(21, .062, .70)], [region(18, .082, .184)], q14, None, points=True)
    add('q14aii', 'Q14(a)(ii)', '4-3-1', 'animal-production', 'hill-sheep-breed', 'Identify one breed from part (i) that is most suitable for their hill flock.',
        [point('Blackface mountain or C', 5)], [region(21, .062, .57), region(21, .699, .76)], [region(18, .184, .232)], q14, extra=('4-2',))
    add('q14aiii', 'Q14(a)(iii)', '4-3-2', 'animal-production|genetics', 'terminal-sires',
        'Rams A and D, are classed as terminal sires. Explain the underlined term, by placing a tick (✓) in the correct box.',
        [point('Male animal used to produce offspring destined for meat production', 6, 'The scheme ticks this box.')],
        [region(21, .062, .57), region(21, .763, .87)], [region(18, .232, .344)], q14)
    add('q14bi', 'Q14(b)(i)', '4-3-3', 'animal-production', 'sheep-weaning-timing',
        'Draw an X on the red line on the diagram above to show when weaning occurs.',
        [point('Correct position of X where finishing is indicated.', 6, 'The scheme accepts anywhere in the region shown on its diagram.', kind='criterion')],
        [region(22, .062, .36)], [region(18, .344, .546)], 'The diagram shows the production through the seasons on a sheep farm. Analyse the diagram and answer the questions that follow.',
        figure='agsci-2026-ol-scheme-weaning-region')
    add('q14bii', 'Q14(b)(ii)', '4-3-3', 'animal-production', 'pregnant-ewe-management',
        'Describe how you manage a pregnant ewe from mating to lambing under the headings:',
        [menu('Flushing (low to high plane of nutrition)|maintenance diet|steaming up – gradual increase of concentrates prior to lambing|mineral supplementation', [3], 'Feeding.'),
         menu('good hygiene|dry bedding or slats|adequate lying and feeding space|good ventilation|group penning|house pre or during lambing|shear or dag before housing', [3], 'Housing.'),
         menu('introduce concentrates prior to lambing to prevent twin lamb disease|dipping|vaccination or dosing|control lameness|pre-lambing mineral ration|calcium injection to treat milk fever|monitor BCS', [3], 'Health.')],
        [region(22, .062, .105), region(22, .36, .87)], [region(18, .546, .768)], 'Sally and Jess are sheep farmers. Headings: Feeding, Housing, Health.', extra=('4-1',))
    add('q14ci', 'Q14(c)(i)', '4-3-1', 'animal-production|grassland', 'lowland-grazing-system',
        'Draw a labelled diagram of a named suitable grazing system that would suit their lowland flock.',
        [point('Named grazing system – rotational or paddock or strip / block / creep', None, 'Named system: 3 marks.', kind='criterion'),
         point('Correct diagram', None, 'Diagram = 0, 2 or 4: multiple paddocks for 2 marks; multiple paddocks and indication of direction for 4 marks.', kind='criterion'),
         point('Correct labels', None, 'Labels = 3(1). Maximum ten for name, diagram and labels.', kind='criterion')],
        [region(23, .062, .44)], [region(19, .082, .226)], 'Managing the grazing land for the lowland flock is very different to managing grazing for the hill flock.', marks=10, extra=('3-3-2',))
    add('q14cii', 'Q14(c)(ii)', '4-3-1', 'animal-production|innovation-and-biotechnology-in-agriculture', 'virtual-fencing',
        'Managing the grazing area of the hill flock is very difficult so Jess carried out research on the different ways to manage the sheep. She found new technology called virtual fencing. This technology involves placing a collar on the animal and then you can operate where they can graze from your smart phone. Outline one advantage and one disadvantage of using this technology.',
        [menu('Reduced labour or no physical fencing required|increased grazing flexibility or precision grazing or pasture optimisation|enhanced livestock welfare or tracking|environmental or eco-system protection', [4], 'Advantage.'),
         menu('High upfront costs|reliance on technology (batteries, connectivity)|potential animal welfare concerns (stress from collars/stimuli)|need for ongoing management|legal and liability risks|training period required (to associate audio cue with the boundary)|other animals can enter', [4], 'Disadvantage.')],
        [region(23, .437, .87)], [region(19, .226, .426)])

    q15a = 'The diagram below shows how soils are formed over time.'
    add('q15ai', 'Q15(a)(i)', '2-1', 'soil-science', 'soil-horizons', 'Identify each horizon (a, b, c and d) using the list of words in the table below.',
        [point('Top soil', 2, 'a.'), point('Subsoil', 2, 'b.'), point('Parent rock', 2, 'c.'), point('Bedrock', 2, 'd.')],
        [region(24, .062, .59)], [region(19, .426, .525)], q15a + ' Words: Parent rock, Top soil, Subsoil, Bedrock.')
    add('q15aii', 'Q15(a)(ii)', '2-1', 'soil-science', 'soil-formation', 'Using the diagram, explain how soil is formed.',
        [menu(['Soil forms slowly from the breakdown of rocks (parent material)', 'by weathering (physical, chemical, biological)', 'colonisation by organisms',
               'the accumulation of organic matter from dead plants and animals', 'influenced by climate or topography or time'], [2, 4])],
        [region(24, .062, .405), region(24, .588, .62)], [region(19, .525, .627)], q15a)
    add('q15aiii', 'Q15(a)(iii)', '2-1', 'soil-science', 'topsoil-features', 'Outline one feature of horizon a.',
        [menu('Dark colour|rich in organic matter or higher CEC|crumbly texture or well aggregated structure|lots of micro-organisms or roots|balanced water or air capacity', [6])],
        [region(24, .062, .405), region(24, .768, .80)], [region(19, .627, .710)], q15a, extra=('2-2-2',))
    q15b = ('Springhill Farm is a mixed farm in County Laois. The farm has dairy cows and tillage, with some grassland fields used for silage. Recently, the farmer noticed that: cows are poaching the land in wet weather; '
            'grass growth is poor in some paddocks; soil tests show low organic matter and poor drainage in certain areas. The farmer plans to aerate compacted soils and spread farmyard manure after the second silage cut.')
    add('q15bi', 'Q15(b)(i)', '2-3', 'soil-science', 'poaching-definition', 'Identify the meaning of the underlined term by placing a tick (✓) in the correct box.',
        [point('Damage caused to land by prolonged livestock grazing in wet conditions, which creates compacted, waterlogged soils', 4, 'The scheme ticks this box.')],
        [region(25, .062, .37)], [region(19, .710, .821)], q15b + ' [The term underlined on the paper is: poaching]')
    add('q15bii', 'Q15(b)(ii)', '2-3', 'soil-science', 'case-study-soil-problems', 'From the case study, name two problems the farmer has with the soil.',
        [menu('Poor drainage|low organic matter|poor growth|compacted soil|poached land', [2, 2])],
        [region(25, .062, .23), region(25, .367, .395)], [region(19, .821, .886)], q15b)
    add('q15biii', 'Q15(b)(iii)', '2-2-2', 'soil-science|grassland', 'compaction-grass-growth', 'Explain how compaction can affect grass growth.',
        [menu('Decreased yield|poor root penetration|reduced drainage|reduced aeration|decreased nutrient uptake', [6])],
        [region(25, .062, .23), region(25, .521, .55)], [region(20, .083, .149)], q15b)
    add('q15biv', 'Q15(b)(iv)', '2-3', 'soil-science|animal-production', 'drainage-benefits',
        'Suggest two ways that improving soil drainage can benefit both the soil and the dairy cows.',
        [menu(['Soils: Improved root growth', 'higher biological activity', 'increased nutrient update or higher plant yields', 'increased aeration or temperature or structure', 'reduced compaction',
               'Cows: extended grazing season', 'more grass available', 'reduced lameness rates', 'lower SCC', 'higher grass DMI or increased milk yield', 'reduced fluke or parasite infection'], [4, 6],
              'Two benefits covering both the soil and the cows: the first five options are the scheme’s soil benefits, the rest its cow benefits. The scheme prints 4+6.')],
        [region(25, .062, .23), region(25, .645, .69)], [region(20, .149, .308)], q15b, extra=('4-3-1',))
    add('q15c', 'Q15(c)', '2-3', 'fertilisers-pollution-the-environment|soil-science', 'environmental-slurry-spreading',
        'Sorcha was researching different methods of slurry spreading to see which one would best suit her farm. Identify which machine A or B spreads slurry in a more environmentally friendly way and give a reason for your answer.',
        [point('A', 1, 'Machine A.'),
         menu(['places the slurry on the soil reducing greenhouse gas emissions', 'reducing plant contamination', 'better uptake of nutrients', 'reduced run-off or eutrophication'], [5], 'Reason.')],
        [region(26, .062, .39)], [region(20, .308, .435)])
    q15d = ('Teagasc investigated different methods of slurry spreading. On day 1, they set up the investigation as follows; Field 1 - no slurry. Field 2 - spread using a trailing shoe. Field 3 - spread using a dribble bar. '
            'Field 4 - spread using a splash plate. On day 21, cows were introduced and grazed their preferred field. The graph shows the amount of grass left after grazing in each of the four fields: '
            'no slurry 150, trailing shoe 250, dribble bar 300, splash plate 550 kg DM/ha.')
    add('q15di', 'Q15(d)(i)', '1-2', 'scientific-practices-experiments-investigations|fertilisers-pollution-the-environment', 'slurry-trial-control',
        'Explain why Teagasc included a field with no slurry in the investigation.', [point('Control', 5)], [region(26, .415, .785)], [region(20, .450, .501)], q15d)
    add('q15dii', 'Q15(d)(ii)', '1-3', 'scientific-practices-experiments-investigations|fertilisers-pollution-the-environment', 'slurry-trial-preference',
        'Identify which one of the three methods of slurry spreading did the cows prefer.', [point('Trailing shoe or Field 2', 1)],
        [region(26, .415, .75), region(26, .829, .86)], [region(20, .501, .566)], q15d, extra=('2-3',))

    q16 = 'Aoife was a young beef farmer who purchased 10 three-week-old beef calves to rear to weanling stage.'
    add('q16ai', 'Q16(a)(i)', '4-2', 'animal-production|classification-of-organisms', 'calf-breed-identification',
        'Identify the breeds A and B of calves that she bought using the list below.',
        [point('A – Aberdeen Angus', 2), point('B – Hereford or Hereford x Friesian or black whitehead', 2)], [region(27, .062, .45)], [region(20, .566, .633)], q16)
    add('q16aii', 'Q16(a)(ii)', '4-3-1', 'animal-production', 'calf-origin',
        'State if these calves are more likely to have come from a dairy or beef farm by placing a tick (✓) in the correct box.',
        [point('Dairy', 1, 'The scheme ticks Dairy.')], [region(27, .062, .41), region(27, .45, .525)], [region(20, .633, .685)], q16)
    add('q16aiii', 'Q16(a)(iii)', '4-3-1', 'animal-production', 'calf-ear-tags', 'Outline why each calf has its own ear tag with a unique number.',
        [menu('Identification|traceability|record keeping or genetics|legal requirement', [2])], [region(27, .062, .14), region(27, .50, .59)], [region(20, .685, .752)], q16)
    add('q16aiv', 'Q16(a)(iv)', '4-3-3', 'animal-production', 'buying-calves-directly',
        'Aoife bought the calves directly from two different farmers and not through the mart. Outline two advantages of buying calves directly.',
        [menu('Reduced disease risk or digestive disorders|less stress or calmer temperament|know stock ancestors|trusted source|known vaccination or medical history|more cost effective', [2, 6])],
        [region(27, .062, .14), region(27, .594, .75)], [region(20, .752, .855)], q16)
    add('q16av', 'Q16(a)(v)', '4-3-3', 'animal-production', 'calf-buying-characteristics', 'State two characteristics Aoife would look for in a calf when buying them.',
        [menu('No swollen naval|no discharge from mouth or nose|clean or shiny coat or no scour|alert or healthy eyes or erect ears|feeding well|not breathing heavy|vaccination history|even gait (not lame) or straight back|correct weight|good conformation', [2, 6])],
        [region(27, .062, .14), region(27, .766, .86)], [region(21, .083, .184)], q16)
    q16b = 'Aoife had to sort the calves into two pens when they arrived to ensure they reached maximum performance.'
    add('q16bi', 'Q16(b)(i)', '4-3-3', 'animal-production', 'sorting-calves', 'Advise Aoife on the best way to sort the calves.',
        [menu('By age|by size|group by rearing method|valid grouping|isolate sick calves', [2])], [region(28, .062, .235)], [region(21, .184, .233)], q16b)
    add('q16bii', 'Q16(b)(ii)', '4-3-3', 'animal-production', 'calf-feeding-plan', 'Describe the feeding plan for the calves until weaning.',
        [menu('Milk or milk replacer|concentrates|silage or hay or straw|access to fresh water', [2, 6])], [region(28, .062, .105), region(28, .23, .26)], [region(21, .233, .299)], q16b)
    add('q16biii', 'Q16(b)(iii)', '4-3-3', 'animal-production', 'calf-bedding',
        'Aoife was researching straw bedding and slats as different types of housing for the calves. Outline one advantage of each type of bedding for the calves.',
        [menu(['Straw bedding – increased welfare or more comfortable or less injury', 'warm', 'reduced draft or respiratory disease',
               'Slats – good hygiene', 'reduced workload', 'lower humidity or better air quality', 'space efficiency'], [2, 6],
              'One advantage of straw bedding (first three options) and one of slats (last four). Two advantages of the same bedding earn one award. The scheme prints 2+6.')],
        [region(28, .446, .86)], [region(21, .299, .408)], q16b)
    q16c = 'Aoife noticed one of the calves not coming for their milk. The calf was away from the others, breathing heavily, had a runny nose and was coughing.'
    add('q16ci', 'Q16(c)(i)', '4-3-3', 'animal-diseases|animal-production', 'calf-pneumonia',
        'Identify the disease the calf is likely to be suffering from by placing a tick (✓) in the correct box.', [point('Pneumonia', 3, 'The scheme ticks Pneumonia.')],
        [region(29, .062, .255)], [region(21, .408, .472)], q16c)
    add('q16cii', 'Q16(c)(ii)', '4-3-3', 'animal-diseases|animal-production', 'pneumonia-treatment', 'Briefly describe the treatment for this disease.',
        [menu('Antibiotics|deep straw bedding|eliminate draughts|calf jacket or infra- red lamp|hydration or feeding support', [3])],
        [region(29, .062, .105), region(29, .253, .31)], [region(21, .472, .538)], q16c + ' The disease is pneumonia.')
    add('q16ciii', 'Q16(c)(iii)', '4-3-3', 'animal-diseases|animal-production', 'pneumonia-prevention', 'Outline one way this disease could be prevented.',
        [menu('Ensure good quality colostrum|improved hygiene|good ventilation|avoid temperature fluctuations|draught free|isolate new stock|vaccination|stress or group management|isolate all newly purchased calves', [3])],
        [region(29, .062, .105), region(29, .347, .375)], [region(21, .538, .641)], q16c + ' The disease is pneumonia.')
    add('q16di', 'Q16(d)(i)', '4-3-1', 'animal-production', 'calf-weaning-weight',
        'Identify the target weaning weight for Aoife’s calves by placing a tick (✓) in the correct box.', [point('90 kg', 3, 'The scheme ticks 90 kg.')],
        [region(29, .496, .645)], [region(21, .657, .723)], q16)
    add('q16dii', 'Q16(d)(ii)', '4-3-1', 'animal-production', 'calf-sale-calculation',
        'Aoife brought the calves to the mart and got €5.50 per kg for her 10 calves. Using your weaning weight from part (i), calculate how much money she received for her 10 calves.',
        [point('90 x 5.50 x 10', 2, 'Correct calculation: allow 2 marks for correct calculation with incorrect answer.'),
         point('€4,950', 4, 'Correct answer: allow 4 marks for correct answer without calculation or calculation using the wrong value.')],
        [region(29, .496, .645), region(29, .643, .70)], [region(21, .723, .866)], 'Part (i): the target weaning weight is 90 kg.', extra=('1-3',))

    q17 = ('Read the article and answer the questions that follow. Using technology to reduce our carbon footprint. AgNav is a free online tool developed to calculate the carbon footprint and measure sustainability of farms. '
           'Teagasc climate advisers visited a farm to review AgNav figures and put plans in place to further reduce the farm’s carbon footprint. In 2023, the farmer was using 68% protected urea and 32% CAN fertiliser, '
           'had all perennial ryegrass swards, and housed his stock for 5.5 months of the year. (Adapted from Farmers Journal, 2024)')
    add('q17ai', 'Q17(a)(i)', '2-3', 'fertilisers-pollution-the-environment', 'protected-urea', 'Identify the meaning of the underlined term by placing a tick (✓) in the correct box.',
        [point('Fertiliser that is protected with a urease inhibitor and reduces greenhouse gas emissions and ammonia', 2, 'The scheme ticks this box.')],
        [region(30, .062, .52)], [region(22, .082, .209)], q17 + ' [The term underlined on the paper is: protected urea]')
    add('q17aii', 'Q17(a)(ii)', '2-3', 'fertilisers-pollution-the-environment', 'reducing-carbon-footprint', 'Outline two things farmers could do to further reduce their carbon footprint.',
        [menu('Use LESS slurry spreading or spread more slurry in springtime|organic farming practices|extend the grazing season|less machinery use|plant hedgerows|reduce soil compaction|sow multi-species swards|sow buffer or riparian zones|test soils regularly|improve livestock or breeding efficiency|install renewable energy or any valid example', [3, 5])],
        [region(30, .062, .325), region(30, .514, .54)], [region(22, .209, .343)], q17, extra=('3-3-2',))
    add('q17aiii', 'Q17(a)(iii)', '2-3', 'fertilisers-pollution-the-environment|innovation-and-biotechnology-in-agriculture', 'carbon-footprint-importance',
        'Outline why it is important for farmers to calculate their carbon footprint.',
        [menu('Identify inefficiencies|access to grants or compliance|future proof business or future sustainability|informed decision making (monitoring emissions)|profitability and input savings|protect the local environment', [4])],
        [region(30, .062, .325), region(30, .668, .695)], [region(22, .343, .426)], q17)
    add('q17bi', 'Q17(b)(i)', '3-3-1', 'crop-production', 'seedbed-preparation-order',
        'Complete the table below by placing the following seedbed preparation pictures (A, B, C and D) in correct order for sowing of a crop.',
        [menu(['B', 'C', 'D', 'A'], [2, 2, 4, 4], 'Correct order: B / C / D / A. The scheme prints 2+2+4+4 for one to four correct positions.')],
        [region(31, .062, .56)], [region(22, .426, .491)])
    add('q17bii', 'Q17(b)(ii)', '1-5', 'health-safety|crop-production', 'tillage-machinery-safety',
        'Outline one safety measure taken when working with any of the machines shown in part (i) above.',
        [menu('Be careful when working near PTO|don’t stand at back of machine when moving|turn off machine when handling any part of machine or any valid example', [2])],
        [region(31, .062, .56), region(31, .565, .612)], [region(22, .491, .590)], 'The machines in part (i) are seedbed preparation and sowing machines A, B, C and D.')
    add('q17c', 'Q17(c)', '1-1', 'scientific-practices-experiments-investigations|crop-production', 'drought-germination-investigation',
        'During sowing, the weather was very dry with very little rain. You wanted to investigate if drought conditions had any effect on the germination of the seed. Describe with the aid of a labelled diagram how you would carry out this investigation under the following headings:',
        [point('Drought conditions will reduce the germination rate (as there is very little water)', 3, 'Hypothesis.'),
         point('Amount of rain or water', 3, 'Independent variable.'), point('Germination rate', 3, 'Dependent variable.'),
         menu('Same seed|same amount of seed|same soil type|same seed tray', [3], 'Control variable.'),
         menu('Plant same no of seeds (e.g. 100) in trays with same soil|add a lot of water to one tray and very little water to the other tray|place trays in a well-lit area|leave to germinate|record amount of seeds germinated', [3, 4],
              'Method: two points, 3+4. The scheme prints no separate mark for the labelled diagram.'),
         point('Seeds tray that had little water had reduced germination', 3, 'Result.')],
        [region(32, .062, .85)], [region(22, .590, .906)], extra=('1-2', '3-3-1'))

    q18a = 'Katie and Tom are dairy farmers in Co. Limerick. They want to improve the quality of milk on their farm.'
    add('q18ai', 'Q18(a)(i)', '4-3-2', 'animal-production', 'milk-quality-factors', 'State two factors that affect the quality of milk produced on a dairy farm.',
        [menu('Feed quality|feed type|genetics or breed|stage of lactation|age of cow|hygiene or storage management|disease', [2, 6])], [region(33, .062, .235)], [region(23, .082, .150)], q18a)
    add('q18aii', 'Q18(a)(ii)', '4-3-3', 'animal-production', 'clean-safe-milk', 'Give two practices a farmer should carry out to ensure milk is clean and safe before collection.',
        [menu('Wash and dry udder|check for mastitis or CMT|observe withdrawal period|iodine or spray on teat|clean milking parlour|milk filter or reduced sedimentation|cool the milk adequately|store at correct temperature', [2, 6])],
        [region(33, .242, .39)], [region(23, .150, .267)], q18a)
    add('q18aiii', 'Q18(a)(iii)', '4-3-3', 'animal-production', 'cooling-milk', 'Explain why it is important to cool milk quickly after milking.',
        [menu('To reduce bacteria multiplication or spoilage|maintain quality or prolong shelf life', [4])], [region(33, .414, .44)], [region(23, .267, .333)], q18a)
    add('q18aiv', 'Q18(a)(iv)', '4-3-3', 'animal-production|animal-diseases', 'high-tbc-causes',
        'Identify which two of the following contribute to a high Total Bacterial Count (TBC) in milk, by placing ticks (✓) in the correct boxes.',
        [menu(['Poor Hygiene', 'Udder infection'], [1, 3], 'The scheme ticks these two boxes, 1+3.')], [region(33, .538, .69)], [region(23, .333, .407)], q18a)
    add('q18av', 'Q18(a)(v)', '4-3-3', 'animal-production', 'milk-contamination', 'List two ways that milk can become contaminated.',
        [menu('Dirt or faulty filters or poor hygienic practices|inadequate cooling|iodine or detergent residues or teat disinfectant run-off or dosing products|excess water|sediment|antibiotics|infected cows|spoiled feed or bedding', [2, 6])],
        [region(33, .692, .72)], [region(23, .407, .508)], q18a)
    add('q18bi', 'Q18(b)(i)', '1-4', 'animal-production|scientific-practices-experiments-investigations', 'scc-milk-yield-graph',
        'Draw a trend graph with Somatic Cell Count (SCC) on the X-axis and milk yield on the y-axis.',
        [point('Correct Y-axis – 3m', None, 'Y-axis: 3 marks.', kind='criterion'), point('Correct point – 3(1)m', None, 'Three points at 1 mark each.', kind='criterion'),
         point('Correct line – 3m', None, 'Line: 3 marks. Maximum nine.', kind='criterion')],
        [region(34, .062, .83)], [region(23, .508, .611)],
        'Katie and Tom monitored milk yield and somatic cell count (SCC) over three months to check herd health. April: SCC 180,000 cells/ml, milk yield 1,200 litres/day; May: 240,000, 1,100; June: 300,000, 1,000. (Adapted from Teagasc, 2025)',
        marks=9, extra=('1-3', '4-3-2'))
    udder = [('A', 'A – teat'), ('B', 'B – quarter'), ('C', 'C – median suspensory ligament'), ('D', 'D – connective tissue septum')]
    routes('q18bii', 'Q18(b)(ii)', '4-1', 'animal-physiology|animal-production', 'udder-structure',
        'Identify any three parts labelled A, B, C and D of the udder using the list of words below.', udder, 3, [3, 3, 3],
        [region(35, .062, .655)], [region(23, .611, .731)], 'Words: Quarter, Connective tissue septum, Teat, Median suspensory ligament.', None, points=True,
        figure='agsci-2026-ol-paper-udder',
        labels=[dict(letter='A', meaning='teat'), dict(letter='B', meaning='quarter'), dict(letter='C', meaning='median suspensory ligament'), dict(letter='D', meaning='connective tissue septum')])
    assert len(cards) == 114, len(cards)
    return cards, tasks
