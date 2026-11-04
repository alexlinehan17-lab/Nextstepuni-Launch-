"""2010 Ordinary tasks: independently read against every paper/scheme page."""
from pathlib import Path
from agricultural_science_2010_hl import point, menu, region
from agricultural_science_2010_parity import scan

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC024GLP000EV.pdf'
HASHES = {
    'exampapers':'4ee8be5bf23d55308b3d08007dad8c0a181c2e7a6cad0e501c4385272fa7e6f0',
    'markingschemes':'42dbd3ca25728ba373226b63a9c1224137705d62fd62a8516faf261a76879ef6',
}
SELECTIONS = {
    '29def7c97b161e02':('exam-selection','Section One chooses six independent questions from seven. Keep every question and its separately marked tasks.'),
    '9e05e2d781e4192b':('open','Q1(b) asks for two particle types without printing a finite response pool.'),
    '096d6a8d92e9ae3a':('answer-identification','Q2 is a correct matching exercise, not permission to choose any machine for any activity. Each numbered activity has its own 4-mark boundary.'),
    '084adf88d05ad6d7':('answer-identification','Q3(a) asks for dairy breeds, not arbitrary pairs. The scheme accepts Friesian, Jersey and Simmental; retain that accepted-answer menu, not incorrect pairs.'),
    '4c69141559e88904':('exam-selection','Section Two chooses three independent questions from six. All six are reviewed.'),
    '08cde5d09c3bc6a3':('independent-task-selection','Q12 chooses two separately priced parts from four. All published internal tasks remain independently practicable; pairs of unrelated exam responses are not new tasks.'),
    '360c0ec99a2f2cf9':('not-selection','Q13(b)(ii): one of the offspring describes the cross, whose F1 offspring all have genotype Ee. It is not a finite answer-route choice.'),
    'd5203138e657084c':('answer-identification','Q13(c)(i): identify the other type of cell division. This is not an optional choice of which type to discuss.'),
}
SOURCE_NOTES = [
    {'questionN':'12','questionRef':'Q12(a)(iii)','paperPage':9,'schemePage':12,
     'note':'For Q12(a)(iii), the English scheme says “Any three points” but prints four awards, 4 + 4 + 4 + 6. The Irish scheme says four points. The printed total is 18; the English wording does not define an unambiguous automatic part-score.'},
    {'questionN':'12','questionRef':'Q12(d)(ii)','paperPage':9,'schemePage':12,
     'note':'For Q12(d)(ii), the English scheme prints 4 + 4 + 4 + 6 (18 marks), making its Q12(d) allocations total 28 despite the paper’s 30 marks. The Irish scheme instead prints 4 + 4 + 6 + 6 (20). This card retains the English scheme’s printed allocation.'},
]


def paper_review():
    observed, supplementary = scan(2010,FILE,HASHES,SELECTIONS,[
        (7,'a root crop or a cereal crop','open','Q9(c) offers open crop categories, not a finite list of named crops. Potato and barley are illustrative scheme routes, not mandatory answer choices.'),
        (7,'under the following headings:','required-headings','All six cultivation headings are required. They split at their own published marks, without expanding combinations.'),
        (10,'match the words from the list below','answer-identification','All six genetic terms must be correctly matched to the passage. Permuting them creates incorrect answers, not permitted examination routes.'),
        (5,'TRUE or FALSE','answer-identification','Ten statements have definite answers. The shared 5(1)+5(3) tariff must remain together; it cannot be assigned to individual letters.'),
    ])
    return {
        'year':2010,'level':'ordinary','lang':'ev','paperFileid':FILE,'hashes':HASHES,
        'wholePaperVisualReview':'reviewed','schemeBoundaryReview':'reviewed',
        'paperPagesInspected':list(range(1,13)),'schemePagesInspected':list(range(1,15)),
        'selectionDirectives':observed,'supplementarySelections':supplementary,'sourceNotes':SOURCE_NOTES,
        'independentBoundaryReview':'All 13 questions read independently against the original scheme. Matching rows with separate activity labels are split; diagram-label sets remain one response. Shared Q5/Q7 tariffs stay together. Q12(a)(iii) has conflicting printed point-count instructions and retains a question-total rubric.',
        'cropVisualReview':'All distinct paper and scheme crops rendered and inspected; source diagrams checked separately. Shared scheme blocks preserve close-set lines and common tariffs.',
        'remaining':['Phone/desktop runtime review','Corpus-wide reconciliation'],
    }


def reviewed_tasks():
    paper_review()
    cards, tasks = [], []

    def add(key, ref, topic, old, atlas, concept, question, rows, pp, sp, stem=None, selection=None, marks=None):
        cid = 'agsci-2010-ol-' + key
        rows = [dict(row,id=f'r-{i+1}') for i,row in enumerate(rows)]
        card = {
            'id':cid,'subjectId':'agricultural-science','year':2010,'level':'ordinary',
            'section':'A' if int(ref.split('(')[0].split(' ')[0][1:]) < 8 else 'B',
            'questionRef':'2010 OL '+ref,'topicId':'agsci-'+topic,
            'curriculumNodeIds':['agricultural-science-'+t for t in old.split('|')],
            'conceptId':concept,'questionText':question,
            'tariffModel':{'kind':'questionTotal' if marks is not None else 'fixed'},
            'totalMarks':marks if marks is not None else sum(r['marks'] for r in rows),'rows':rows,
            'sourceMaterial':{'kind':'source-text','label':'OFFICIAL QUESTION PAGE',
                'title':'Agricultural Science 2010 Ordinary — '+ref,'pages':sorted({r['p'] for r in pp}),
                'attribution':'SEC Agricultural Science 2010 Ordinary Level examination paper — © State Examinations Commission.',
                'presentationNote':'Open the original page for the published diagrams, wording and answer spaces.'},
        }
        if key in {'q1a','q5','q6a','q10ai','q10bi','q13cii'} or key.startswith('q8a'):
            card['sourceMaterial']['kind'] = 'source-illustration'
        if stem: card['stem'] = stem
        cards.append(card)
        task = {
            'questionRef':card['questionRef'],'paperPage':pp[0]['p'],'schemePage':sp[0]['p'],
            'paperRegions':pp,'schemeRegions':sp,'atlasNumbers':{cid:str(1000+len(cards))},
            'selection':selection or {'kind':'none','reason':'Required response; no finite optional pool is printed. Scheme alternatives are accepted answers.'},
            'cardIds':[cid],'marksPerRoute':card['totalMarks'],
            'examTopicIds':['agricultural-science-ordinary-'+t for t in atlas.split('|')],
            'evidence':'Full 12-page paper and 14-page English scheme visually inspected, with all 12 Irish paper and 13 Irish scheme pages compared. Boundaries follow the published tariff; edition discrepancies are recorded explicitly.',
        }
        note = next((n['note'] for n in SOURCE_NOTES if n['questionRef']==ref),None)
        if note: task['schemeNote'] = note
        tasks.append(task)
        return card

    def variants(card, variants):
        card['answerVariants'] = [{'id':key,'label':label,'rows':[dict(r,id=f'r-{i+1}') for i,r in enumerate(rows)]} for key,label,rows in variants]

    add('q1a','Q1(a)','2-2-2','1-3','soil-science','soil-composition',
        'The following chart shows the composition of a soil. Identify A, B, C and D from the information below.',
        [point('Air',1,'A'),point('Organic Matter (humus)',1,'B'),point('Mineral Matter',1,'C'),point('Water',1,'D')],
        [region(2,.274,.729)],[region(5,.115,.163)])
    particles = ['Gravel','Coarse Sand','Fine Sand','Silt','Clay']
    q1b=add('q1b','Q1(b)','2-2-2','1-3','soil-science','soil-mineral-particle-types',
        'Soil includes different types of mineral particles. List any two of these particle types.',
        [menu(particles,[6,6],'Name two distinct particle types. The scheme allows only 3 marks for unspecified “sand”; use the sand marking menu for that response.')],
        [region(2,.736,.851)],[region(5,.176,.216)],selection={'kind':'open','reason':'No finite list of particle types is printed in the question.'})
    variants(q1b,[('specific','Two specific particle types',q1b['rows']),
        ('sand','Answer includes sand',[point('sand',3,'The scheme explicitly accepts “sand” alone for 3 marks.'),
          dict(point('Coarse Sand/ Fine Sand',3,'The remaining 3 marks require a specific coarse/fine type for that same sand answer.'),dependsOn='r-1'),
          menu(particles,[6],'A different specific particle type; do not claim the same sand type twice.')])])
    add('q1c','Q1(c)','2-2-3','1-4','soil-science','beneficial-soil-organisms',
        'Give one example of an organism that is of benefit to soil.',[point('Earthworm, fungus, bacteria or any other relevant organism',4)],
        [region(2,.867,.937)],[region(5,.23,.264)])
    machines = 'A. Elevator digger; B. Combine drill; C. Rotary tedder; D. Subsoiler; E. Round baler; F. Combine harvester.'
    for n,activity,answer,topic,old in [
        (2,'Harvesting barley','F. Combine harvester','3-3-3','2-5'),(3,'Making hay','C. Rotary tedder or round baler','3-3-3','2-5'),
        (4,'Harvesting potatoes','A. Elevator digger','3-3-3','2-5'),(5,'Sowing seed','B. Combine drill','3-3-1','2-3'),
        (6,'Breaking up compacted soil','D. Subsoiler','2-3','1-5'),
    ]:
        add(f'q2-{n}',f'Q2 — activity {n}',topic,old,'soil-science' if n==6 else 'crop-production','machinery-'+activity.lower().replace(' ','-'),
            'Many agricultural activities require the use of farm machinery. Choose a machine from the list below and match it to an activity listed in the table. The first one has been completed as an example.',
            [point(answer,4)],[region(3,.045,.365)],[region(5,.311,.456)],
            f'Practice task: activity {n}, {activity}. {machines} The completed example is making bales of silage: E. Round baler.',
            {'kind':'answer-identification','reason':'One correct activity-machine match. The machine list is a bank of possible answers, not arbitrary permitted routes.'})
    add('q3a','Q3(a)','4-2','3-1','animal-production','dairy-cattle-breeds',
        'Choose two dairy breeds from the following list of cattle breeds: Charolais, Friesian, Simmental, Jersey, Hereford.',
        [menu(['Friesian','Jersey','Simmental'],[1,1],'The scheme explicitly accepts Simmental as well as Friesian and Jersey.')],
        [region(3,.397,.536)],[region(5,.502,.55)],selection={'kind':'answer-identification','reason':'Identify correct dairy breeds; incorrect pairs are not finite practice routes.'})
    add('q3b','Q3(b)','4-3-2','3-4','animal-production','dairy-cow-physical-characteristics',
        'Describe two physical characteristics of a good dairy cow.',
        [menu(['Wedge(triangular) shaped','narrow shoulders(shoulderblades close together','wide hindquarters','long narrow head','long narrow neck','barrel, chest or abdomen is not deep','healthy udder or disease-free or sound feet or high milk yield'],[3,3],
              'Accept one point regarding a “good” cow versus a “bad” cow, e.g. healthy udder or disease-free or sound feet or high milk yield. Only one such general quality may replace a physical conformation point.')],
        [region(3,.542,.647)],[region(5,.541,.639)])
    for key,label,answer in [('lactation','Lactation','production of milk'),('colostrum','Colostrum','first milk produced by cow after calving or milk with higher levels of protein or milk that provides immunity in first 24 hours after calving or milk with a laxative effect')]:
        add('q3c-'+key,'Q3(c) — '+key,'4-1','3-0','animal-physiology|animal-production',key,
            'What do the terms lactation and colostrum mean with regard to dairy cows?', [point(answer,3,label)],
            [region(3,.657,.744)],[region(5,.637,.7)],'Practice term: '+label+'.')
    add('q3d','Q3(d)','4-1','3-0','animal-production','standard-lactation-length',
        'What is the length of the standard lactation in dairy cows?', [point('305 days (or accept range 295-315 days or 42-45 weeks or 10 months)',6)],
        [region(3,.756,.823)],[region(5,.71,.742)])
    for key,name,answer in [('mastitis','Mastitis','Not Notifiable'),('swine-fever','Swine fever','Notifiable'),('brucellosis','Brucellosis','Notifiable'),('liver-fluke','Liverfluke','Not Notifiable'),('tuberculosis','Tuberculosis (TB)','Notifiable')]:
        add('q4-'+key,'Q4 — '+name,'4-3-3','3-5','animal-diseases','notifiable-'+key,
            'Notifiable diseases must, by law, be reported to the authorities. Place a tick (√) in the correct box in each case to indicate if a disease is notifiable or not. The first one has been completed an example.',
            [point(answer,4,'For '+name+' in this 2010 examination scheme.')],
            [region(4,.039,.298)],[region(6,.05,.18)],'Practice disease: '+name+'. Use the classification required by the 2010 paper.')
    q5=add('q5','Q5','3-2','2-1|2-5','classification-of-organisms|crop-production','plant-photograph-identification',
        '(a) Identify the plants in the following photographs. (b) Name the family to which Plant B belongs. (c) Which of the above plants is usually considered to be a weed? (d) Name a by-product of the processing of Plant D.',
        [menu(['A: Clover','B: Oats','C: Thistle','D: (Sugar or fodder) beet or mangold or turnip or swede','Gramineae.','Plant C or Thistle','(Beet) pulp or (Beet) tops or Molasses'],[3]*6+[2],
              'The first four answers match photographs A–D. The last three answer (b), (c), (d), respectively. For (b), accept grass family. For (d), do not accept sugar. First six correct answers earn 3 each; the seventh earns 2. The shared tariff prevents splitting the lettered parts.')],
        [region(4,.301,.94)],[region(6,.223,.363)])
    q5['additionalTopicIds']=['agsci-3-3-3']
    add('q6a','Q6(a)','3-1','2-0','plant-physiology','plant-cell-labels',
        'The following is a diagram of a plant cell. Name the parts labelled A, B and C.',
        [point('Cell Wall',4,'A'),point('Vacuole or (cell)sap',4,'B'),point('Nucleus',4,'C')],
        [region(5,.045,.321)],[region(6,.397,.441)])
    add('q6b','Q6(b)','3-1','2-0','plant-physiology','chlorophyll',
        'What is the name of the green pigment found in chloroplasts?', [point('Chlorophyll',4)],
        [region(5,.319,.371)],[region(6,.437,.463)])
    add('q6c','Q6(c)','3-1','2-0','plant-physiology','chlorophyll-function',
        'What is the function of the green pigment?', [point('Photosynthesis or to make food or to absorb (“trap”) sunlight',4)],
        [region(5,.319,.437)],[region(6,.468,.493)],'The green pigment found in chloroplasts is the pigment referred to in part (b).')
    q7=add('q7','Q7','3-3-2','0-1|2-0|2-1|2-4|3-0|3-4|3-5','crop-production|plant-physiology|animal-physiology|animal-production|animal-diseases|scientific-practices-experiments-investigations','agricultural-true-false',
        'Indicate whether each of the following statements is TRUE or FALSE by circling the correct answer. The first one has been completed as an example.',
        [menu(['(a) False','(b) False','(c)True','(d) True','(e) False','(f) False','(g) False','(h) True','(i) True','(j) True'],[1]*5+[3]*5,
              'Match each answer to its letter on the official page. The scheme explicitly pays 1 mark for each of the first five correct answers, then 3 for each of the next five. These are the original 2010 answers, including (j).')],
        [region(5,.467,.925)],[region(6,.535,.868)],
        '(a) Rooster is a variety of barley. (b) Crop rotation encourages pests. (c) Chickens have a gizzard in their digestive system. (d) Thinning forest trees encourages growth. (e) Iodine is used to test for protein in food. (f) Animal cells have no nucleus. (g) Pigs are ruminant animals. (h) FCR means Feed Conversion Ratio. (i) Cobalt deficiency causes pine in sheep. (j) Blight is a fungal disease.')
    q7['additionalTopicIds']=['agsci-3-1','agsci-3-2','agsci-4-1','agsci-4-3-2','agsci-4-3-3','agsci-1-2']

    grazing='The following diagrams show two grazing systems used in Ireland. Refer to Grazing System A and Grazing System B on the official page.'
    gp=[region(6,.231,.657)]
    add('q8ai','Q8(a)(i)','3-3-2','2-6','grassland','grazing-system-identification','Identify each grazing system.',
        [point('Strip Grazing',3,'A'),point('Paddock Grazing',3,'B')],gp,[region(7,.086,.167)],grazing)
    for key,label,options,sp in [
        ('strip','A: Strip grazing','Land divided into strips with movable electric fence|fence moved to create new strip when cattle have grazed old strip|old strip fenced off and fertilized|movable water supply',[region(7,.173,.235)]),
        ('paddock','B: Paddock grazing','Land divided into paddocks|Cattle moved to a new paddock each day|Old paddock fertilized and regrown before cattle are moved back to it.',[region(7,.239,.303)]),
    ]:
        add('q8aii-'+key,'Q8(a)(ii) — '+key,'3-3-2','2-6','grassland','grazing-method-'+key,
            'Explain how each of the grazing systems works.',[menu(options,[3,3],label)],gp,sp,grazing+' Practice system: '+label+'.')
    for key,system,kind,answer,sp in [
        ('strip-advantage','A','advantage','Fresh grass always available or not as expensive as paddock grazing or back fence prevents damage to grass regrowing / used in block grazing', [region(7,.316,.38)]),
        ('strip-disadvantage','A','disadvantage','High labour or hard to contain stock with temporary electric fencing',[region(7,.376,.401)]),
        ('paddock-advantage','B','advantage','Fresh grass every day or grass is always at the leafy stage or grass can be saved for silage',[region(7,.409,.479)]),
        ('paddock-disadvantage','B','disadvantage','Expensive or need to create roads or time consuming moving animals or lots of labour needed or hard to cut grass for silage in small paddocks with large machines',[region(7,.48,.543)]),
    ]:
        add('q8aiii-'+key,'Q8(a)(iii) — '+key.replace('-',' '),'3-3-2','2-6','grassland',key,
            'State one advantage and one disadvantage of each of the grazing systems named.',[point(answer,3)],gp,sp,
            grazing+f' Practice task: one {kind} of system {system}.')
    add('q8aiv','Q8(a)(iv)','3-3-2','2-6','grassland','other-grazing-system',
        'Name one other system of grazing you have studied.',[point('Set stocking or block grazing or zero grazing or leader-follower or creep grazing or mixed grazing or in-situ',3)],
        gp,[region(7,.543,.593)],grazing+' Name a system other than A or B.')
    add('q8bi','Q8(b)(i)','3-2','2-6','grassland','pasture-plant-species',
        'Name one grass and one other plant species suitable for good quality grazing for livestock.',
        [point('Perennial ryegrass (PRG) or IRG or Timothy or cocksfoot',3,'Grass species'),point('clover or relevant crop',3,'Other plant species')],
        [region(6,.699,.775)],[region(7,.599,.631)])
    add('q8bii','Q8(b)(ii)','3-3-2','2-6','grassland','pasture-plant-suitability',
        'Give a reason for the use of each of the named species.',
        [point('PRG – good productivity/palatability/digestibility/persistence/ aggressive',3,'Reason must match your named grass; PRG is the scheme example.'),
         point('Clover – high protein content/palatable/N-fixation/weed control',3,'Reason must match your named other plant; clover is the scheme example.')],
        [region(6,.699,.779)],[region(7,.631,.692)],'Name one grass species and one other plant suitable for high quality grazing, then give a reason for each.')
    methods=[
        ('undersowing','Undersowing','Undersowing|Grass is sown with nurse crop|Cereal is sown first, then grass seed sown|grow together over summer|cereal is harvested or arable silage|grass is left to grow'),
        ('direct-sowing','Direct sowing','Direct sowing|Plough and harrow to prepare seedbed|Fertilize seedbed|sow seeds using seed drill|roll twice|spring sown leys to be sown before May|Autumn sown leys to be sown before September'),
        ('direct-drilling','Direct drilling','Direct drilling|Seeds drilled into unploughed ground|using seed drill|grass can be grazed tightly|killed with herbicide (prior to drilling of grassland)|add fertilizer to encourage growth|slug pellets.'),
        ('stitching-in','Stitching in','Stitching in|Grassland is not killed|old grass grazed tightly|seeds sown directly into grassland|grass takes over from old pasture|if new seeds do not grow old pasture will continue to grow|slug pellets.'),
        ('slurry-mixed','Slurry seeding — mixed before spreading','Slurry seeding|Old grass grazed tightly|grass seeds and slurry mixed together|spread onto land'),
        ('slurry-after','Slurry seeding — slurry applied after sowing','Slurry seeding|Old grass grazed tightly|grass seed sown|then slurry applied after.'),
    ]
    q8c=add('q8c','Q8(c)','3-3-1','2-3|2-6','grassland','pasture-establishment-method',
        'Describe one method of sowing a field for pasture.',[menu(methods[0][2],[3,3,3],'Three matching points; the method name may count as one point.')],
        [region(6,.783,.823)],[region(8,.048,.348)],selection={'kind':'open','reason':'The question names no finite method pool. The printed scheme methods are alternative marking menus on one practice task; the two slurry sequences stay separate.'})
    variants(q8c,[(k,label,[menu(options,[3,3,3],'Use three points from this method. The name may count as one.')]) for k,label,options in methods])
    for key,label,answer,sp in [('tillering','Tillering','the growth of side shoots (from base of main stem)',[region(8,.38,.417)]),('topping','Topping','cutting the grass at the top to encourage tillering or to remove stemmy growth or to encourage leafy growth or to control weeds',[region(8,.414,.467)])]:
        add('q8d-'+key,'Q8(d) — '+key,'3-1' if key=='tillering' else '3-3-2','2-6','grassland',key,
            'Grazing pasture can be improved by tillering and topping. Explain each of the underlined terms.',[point(answer,3)],
            [region(6,.831,.877)],sp,'Practice term: '+label+'.')

    crop_stem='A farmer has decided to produce a particular crop for the first time. The results of a soil test indicate that the soil has a low pH and is lacking in minerals.'
    add('q9a','Q9(a)','2-3','1-5','soil-science','raising-soil-ph','Suggest one way in which the farmer can raise the pH of the soil.',
        [point('Liming',4)],[region(7,.079,.163)],[region(9,.051,.106)],crop_stem)
    add('q9b','Q9(b)','2-2-1','1-2','soil-science','soil-mineral-elements','List two minerals normally present in the soil.',
        [menu('Nitrogen|Phosphorus|Potassium|Calcium|Magnesium|Sulphur|any other correct element.',[2,4],'Correct chemical symbols are accepted. The scheme prints 2 + 4.')],
        [region(7,.079,.119),region(7,.174,.193)],[region(9,.105,.168)],crop_stem)
    add('q9c','Q9(c)','3-2','2-1','crop-production','root-or-cereal-crop','Give the name of a root crop or a cereal crop that could be sown.',
        [point('Crop named e.g. Potatoes or barley or wheat',2)],[region(7,.079,.119),region(7,.206,.226)],[region(9,.176,.203)],crop_stem,
        {'kind':'open','reason':'Open crop categories. No finite pool of crop names is printed; examples are non-exhaustive.'})
    add('q9d','Q9(d)','2-3','1-6','crop-production|fertilisers-pollution-the-environment','crop-fertiliser',
        'Name a fertilizer suitable for the crop you named in part (c).',[point('Correct Fertilizer e.g. Potato -10:10:20 or 7:6:17',4,'Match your named crop; potato fertilisers are examples, not the only permissible crop response.')],
        [region(7,.079,.119),region(7,.206,.259)],[region(9,.21,.238)],crop_stem+' Name a root crop or cereal crop before choosing its fertiliser.')
    cultivation=[
        ('i','Preparation of seedbed','3-3-1','2-3',6,menu('(Autumn) plough|remove stones|harrow|make drills (ridges)',[2,4]),menu('(Autumn) plough|harrow|roll seedbed',[2,4]),(.309,.337),(.578,.606)),
        ('ii','Seed sowing date','3-3-1','2-3',2,point('Spring sowing (Jan. - April)',2),point('Winter barley :September-October // Spring barley : February - April.',2),(.34,.362),(.609,.635)),
        ('iii','Diseases or pests of the crop','3-3-2','2-4',6,menu('Blight|potato cyst nematode|eelworm|wireworm|slugs|aphids',[2,4]),menu('wireworms|loose smut|powdery mildew|aphids|birds',[2,4]),(.368,.392),(.64,.665)),
        ('iv','A suitable method of disease or pest control (to match part (iii))','3-3-2','2-4',4,point('Spray (fungicide)/spray (insecticide)/crop rotation/certified seed',4),point('crop rotation/spray (fungicide)/spray (insecticide) / certified seed',4),(.399,.424),(.668,.693)),
        ('v','Harvest date','3-3-3','2-5',2,menu('First earlies: May-June|Second earlies : June-July|Maincrop: August-November.',[2]),point('Winter barley :June-July // Spring barley: August-September',2),(.429,.467),(.702,.725)),
        ('vi','Yield','3-3-3','2-5',6,menu('First and second earlies - 7-10 tonnes/Ha.|Maincrop - 30-40 tonnes /Ha.',[6]),point('Winter barley : 7-9 tonnes/Ha // Spring barley : 5-7 tonnes/Ha',6),(.478,.533),(.735,.758)),
    ]
    for numeral,heading,topic,old,marks,potato,barley,pr,br in cultivation:
        for row in [potato,barley]: row['contextNote']='Match the crop you named and its crop type. These are the published potato/barley examples; the paper also permits other appropriate named root or cereal crops.'+(' The control must match the disease or pest named in (iii).' if numeral=='iv' else '')
        c=add('q9e'+numeral,'Q9(e)('+numeral+')',topic,old,'crop-production','crop-'+heading.lower().split(' ')[0],
            'Describe the cultivation of the crop you have named in part (c) under the following headings:',
            [potato],[region(7,.079,.119),region(7,.206,.227),region(7,.272,.43)],
            [region(9,.254,.281),region(9,*pr),region(9,*br)],crop_stem+' Name the root or cereal crop you are describing. Practice heading ('+numeral+'): '+heading+'.',
            {'kind':'required-heading','reason':'One of six required, separately priced cultivation headings. Crop choice is open; scheme examples remain marking variants.'})
        variants(c,[('potato','Potato example',[potato]),('barley','Barley example',[barley])])
        assert c['totalMarks']==marks
    add('q9f','Q9(f)','1-2','0-1|1-4','soil-science|scientific-practices-experiments-investigations','earthworm-population-experiment',
        'Describe an experiment to determine the earthworm population of the field.',
        [menu('Measure area of a field|using trundle wheel|measure 1m² area|clear area of grass/use scissors|pour washing up solution on bare soil|wait for earthworms to come to surface|count earthworms inside measured area|repeat|average|multiply no. earthworms by area of field',[4,4,4,6],
              'Four relevant points forming a coherent method. This English scheme prints 18 marks; the Irish edition prints 20. The original English allocation is retained.')],
        [region(7,.079,.119),region(7,.44,.462)],[region(9,.774,.882)],crop_stem)

    heart=[region(8,.042,.446)]
    add('q10ai','Q10(a)(i)','4-1','3-0','animal-physiology','sheep-heart-labels',
        'Name, in your answer book, the parts labelled A, B, and C.',[point('(Right) atrium',3,'A'),point('(Left) ventricle',3,'B'),point('Septum',3,'C')],heart,[region(10,.05,.107)],'The diagram below shows a sheep’s heart. Use the official diagram.')
    add('q10aii','Q10(a)(ii)','4-1','3-0','animal-physiology','blood-cell-types','List three types of blood cell.',
        [point('White blood cells',3),point('Red blood cells (corpuscles)',3),point('platelets',3)],heart,[region(10,.108,.137)])
    add('q10aiii','Q10(a)(iii)','4-1','3-0','animal-physiology','blood-cell-functions','Give the function of each type of blood cell.',
        [point('Fight infection or needed for immunity',3,'White blood cells'),point('carry oxygen',3,'Red blood cells'),point('blood clotting',3,'Platelets')],heart,[region(10,.137,.166)],'Give a function for each of the three blood-cell types listed in part (ii).')
    add('q10aiv','Q10(a)(iv)','4-3-3','3-5','animal-diseases|animal-production','piglet-anaemia-cause',
        'New-born bonhams often suffer from a blood-related illness called anaemia. What is the cause of anaemia?', [point('Iron deficiency',3)],heart,[region(10,.167,.195)])
    add('q10av','Q10(a)(v)','4-3-3','3-5','animal-diseases|animal-production','piglet-anaemia-prevention',
        'Describe how anaemia in bonhams can be prevented.',[point('Iron injection (in first week of life)',3)],heart,[region(10,.195,.223)])
    repro=[region(8,.449,.925)]
    add('q10bi','Q10(b)(i)','4-1','3-0','animal-physiology','cow-reproductive-system-labels',
        'Name, in your answer book, the parts labelled A, B, and C.',[point('Ovary',3,'A'),point('Vagina',3,'B'),point('Uterus (womb)',3,'C')],repro,[region(10,.225,.282)],'The diagram below shows the reproductive system of the cow. Use the official diagram.')
    add('q10bii','Q10(b)(ii)','4-3-2','3-4','animal-production','flushing-ewes',
        'Sheep farmers often use a technique called ‘flushing’ to improve conception rates. What is meant by flushing?',
        [point('Stock ewes on poor quality pasture and then less heavily on better quality pasture or Improved feeding before mating',3)],repro,[region(10,.287,.326)])
    add('q10biii','Q10(b)(iii)','4-3-2','3-4','animal-production','flushing-advantages','List three advantages of flushing.',
        [menu('More eggs released|greater chance of multiple births|higher conception rates|more regular heat periods|better attachment of embryo|synchronised oestrus',[3,3,3])],repro,[region(10,.334,.389)])
    add('q10biv','Q10(b)(iv)','4-3-2','3-6','animal-production|genetics','artificial-insemination-term',
        'Cattle farmers often use A.I. to improve conception rates. What does A.I. stand for?', [point('Artificial insemination',3)],repro,[region(10,.394,.425)])
    add('q10bv','Q10(b)(v)','4-3-2','3-6','animal-production|genetics','artificial-insemination-advantage',
        'Give one advantage of A.I.',[point('Better choice of sire or cheaper (than keeping a bull on a small farm) or better choice of breed or safety or no need to keep bull or improved genetics or easier to transport or less wastage',3)],repro,[region(10,.431,.49)])
    beef='Irish beef animals are graded at slaughter according to their fatness and conformation.'
    bp=[region(9,.075,.177)]
    add('q11ai','Q11(a)(i)','4-3-1','3-3','animal-production','beef-conformation',
        'Explain the term conformation.',[point('Shape of an animal or distribution of muscle on animal',4)],bp,[region(11,.051,.091)],beef)
    add('q11aii','Q11(a)(ii)','4-3-1','3-3','animal-production','beef-dairy-conformation-comparison',
        'Describe the difference in conformation between beef cattle and dairy cattle.',
        [menu('Beef animals have muscular shoulders and hindquarters|beef animals are rectangular in shape (or “square -shaped”)|Beef animals are wide at shoulders and hindquarters|dairy animals are not muscular (energy goes into milk production)',[4,4],'Two distinct comparison points. Do not count synonymous restatements twice.')],bp,[region(11,.095,.155)],beef)
    add('q11aiii','Q11(a)(iii)','4-3-1','3-3','animal-production','beef-slaughter-age',
        'What is the usual age for the slaughter of beef cattle in Ireland?', [point('2 - 2 ½ years',4,'The age required by this 2010 scheme.')],bp,[region(11,.174,.199)],beef)
    add('q11aiv','Q11(a)(iv)','4-3-1','3-3','animal-production','beef-slaughter-age-reason',
        'Why are beef cattle slaughtered at this age?', [point('After this age fat is put on instead of muscle or Meat quality is better',4,'The scheme also accepts “resources not wasted”.')],bp,[region(11,.21,.266)],beef+' Part (iii) asks for the usual slaughter age; explain that age.')
    sheep='Sheep breeding is an important part of the livestock industry in Ireland.'
    lp=[region(9,.185,.276)]
    add('q11bi','Q11(b)(i)','4-2','3-1','animal-production','lamb-production-breeds','Name two breeds of sheep used for lamb production in Ireland.',
        [menu('Texel|Wicklow Cheviot|BlackfaceMountain|Galway|Suffolk|Border Leicester|any relevant breed',[4,4])],lp,[region(11,.27,.315)],sheep)
    add('q11bii','Q11(b)(ii)','4-3-3','3-5','animal-production','newborn-lamb-weight','What is the average weight of a lamb at birth?',
        [point('3-6 kg',4)],lp,[region(11,.314,.334)],sheep)
    add('q11biii-feeding','Q11(b)(iii) — feeding','4-3-3','3-5','animal-production','newborn-lamb-feeding','Describe the feeding and management of a new-born lamb.',
        [point('Colostrum or Ewe suckles lamb',4)],lp,[region(11,.335,.362)],sheep+' Practice task: feeding.')
    add('q11biii-management','Q11(b)(iii) — management','4-3-3','3-5','animal-production','newborn-lamb-management','Describe the feeding and management of a new-born lamb.',
        [menu('clear mucus|help to suck|kept under Infra-red lamp|stomach tube|glucose injection|warming box|mark lamb|place ewe + lamb in individual pen|iodine|hygiene|(suitable) bedding',[4,4])],
        lp,[region(11,.369,.481)],sheep+' Practice task: management.')
    add('q11ci','Q11(c)(i)','4-3-2','3-4','animal-production','creep-feeding-definition','What does the term creep feeding mean?',
        [point('Only young animal has access to food',4)],[region(9,.283,.348)],[region(11,.509,.537)],'Livestock farmers often use a system called “creep feeding”.')
    add('q11cii','Q11(c)(ii)','4-3-2','3-4','animal-production','creep-feeding-advantages','Give three advantages of creep feeding.',
        [menu('Supplements milk from mother|supplements grass|extends the grazing season|increased weaning rates|increased stocking rates|animals reach genetic potential quicker|suffer less set-back at weaning or adapt quickly|improve lifetime performance even post weaning|balanced diet|Rumen development',[4,4,4])],
        [region(9,.283,.348)],[region(11,.539,.6)])

    survey='A group of students carried out a survey of plants in an old pasture.'
    sap=[region(9,.45,.552)]
    add('q12ai','Q12(a)(i)','3-2','2-1','classification-of-organisms|grassland','pasture-weeds','List two weeds they might find in the pasture.',
        [menu('Thistle|nettle|daisy|dandelion|ragwort',[4,4],'Examples, not an exhaustive list of acceptable pasture weeds.')],sap,[region(12,.049,.108)],survey)
    add('q12aii','Q12(a)(ii)','1-2','0-1','scientific-practices-experiments-investigations','plant-survey-equipment',
        'Name one piece of equipment that could be used in carrying out the survey.',[point('Quadrat or Line Transect',4)],sap,[region(12,.12,.143)],survey)
    add('q12aiii','Q12(a)(iii)','1-2','0-1','scientific-practices-experiments-investigations','plant-population-estimation',
        'Describe how the named piece of equipment may be used in estimating the number of a particular plant in the field.',
        [point('description/throw/random/how random/count or estimate plants/repeat/ average/calculate or scale up',None,SOURCE_NOTES[0]['note'],'criterion')],
        sap,[region(12,.12,.201)],survey+' Name the survey equipment whose use you are describing.',marks=18)
    pigstem='In the pig production industry a sow is moved to a farrowing house to have her litter of bonhams.'
    psp=[region(9,.563,.739)]
    add('q12bi','Q12(b)(i)','4-3-3','3-5','animal-production','farrowing-house-temperature','What is the most suitable temperature for the farrowing house?',
        [point('20°C',4)],psp,[region(12,.227,.251)],pigstem)
    add('q12bii','Q12(b)(ii)','4-3-3','3-5','animal-production','farrowing-crate-reasons','Why is the sow kept in a farrowing crate?',
        [menu('To prevent sow from crushing her bonhams|easier to manage (sow)|easier to feed (sow)',[4,4])],psp,[region(12,.251,.288)],pigstem)
    add('q12biii','Q12(b)(iii)','4-3-1','3-3','animal-production','post-weaning-pig-housing',
        'After the bonhams are weaned the sow and bonhams are moved to different houses. Give the names of the houses for 1. The sow 2. The bonhams.',
        [point('Dry sow house',2,'1. The sow'),point('Weaner house',2,'2. The bonhams')],psp,[region(12,.286,.307)],pigstem)
    add('q12biv','Q12(b)(iv)','4-3-2','3-4','animal-production','gilt-selection','What criteria are used when selecting a gilt for breeding?',
        [menu('Good health or one indication of good health e.g. smooth shiny hair, bright lively eyes|firm body tissues|sound legs and feet|long body|well formed hams|fourteen teats|good constitution|litter size|degree of heritability of characteristics|growth|good FCR',[4,4,6],
              'Three distinct criteria. General health and examples of the same good health count as one criterion.')],psp,[region(12,.307,.385)],pigstem)
    env='Farmers can do many things to improve the environment on their farm.'
    ep=[region(9,.745,.834)]
    add('q12ci','Q12(c)(i)','3-3-2','1-6','fertilisers-pollution-the-environment','hedgerow-benefits','Give three advantages of planting or preserving hedgerows.',
        [menu('Natural amenity|REPS|natural fencing|land boundary|shelter for animals|habitat for animals|sound barrier|Replenish oxygen',[4,4,6])],ep,[region(12,.394,.438)],env)
    add('q12cii','Q12(c)(ii)','2-3','1-6','fertilisers-pollution-the-environment','fertiliser-runoff-prevention',
        'List two ways of reducing the amount of fertilizer that runs off into waterways.',
        [menu('Do not spread in wet weather|use correct fertilizer|use correct amount of fertilizer|do not apply during drought|do not apply during rapid growth|do not apply too close to waterways|do not apply on sloping land|Correct pH',[4,6],
              'These are the printed 2010 scheme criteria. The source includes “do not apply during rapid growth”; it is preserved as examination wording.')],ep,[region(12,.437,.506)],env)
    add('q12ciii','Q12(c)(iii)','4-3-1','1-6','fertilisers-pollution-the-environment','organic-farming-definition','What is meant by organic farming?',
        [point('A system of farming which avoids the use of soluble fertilisers or pesticides or growth regulators or feed additives/ or other chemicals',6,'Definition quoted from the 2010 examination scheme.')],ep,[region(12,.508,.55)],env)
    stages='Germination and establishment are two stages in plant development.'
    dp=[region(9,.84,.916)]
    for key,answer,mark,sp in [('germination','Seed begins to grow (into a new plant )',4,[region(12,.581,.609)]),('establishment','new plant puts down roots or begins to photosynthesise',6,[region(12,.61,.635)])]:
        add('q12di-'+key,'Q12(d)(i) — '+key,'3-1','2-0','plant-physiology',key,
            'Explain each of the underlined terms.',[point(answer,mark)],dp,sp,stages+' Practice term: '+key+'.')
    add('q12dii','Q12(d)(ii)','1-2','0-1|2-0','plant-physiology|scientific-practices-experiments-investigations','germination-conditions-experiment',
        'Outline an experiment to show the conditions necessary for germination.',
        [menu('seeds|on cotton wool|in test tubes|one tube no moisture|how/one tube no O₂|how/one tube unsuitable temp.|how/one tube has all three suitable conditions|period of time|results|conclusion',[4,4,4,6],SOURCE_NOTES[1]['note']+' A suitably labelled diagram may supply the points.')],dp,[region(12,.635,.755)],stages)

    add('q13a','Q13(a)','4-3-2','3-6','genetics','mendelian-genetics-passage',
        'Read the following paragraph about the study of genetics and match the words from the list below with the numbered spaces. Write your answers in your answer book and not on this examination paper.',
        [point(word,3,f'Space {i}') for i,word in enumerate(['dominant','recessive','heterozygous','homozygous','genotype','phenotype'],1)],
        [region(10,.074,.426)],[region(13,.047,.294)],'Use the complete Mendel passage and word list on the official page.')
    pigs='The pig in the photograph shows the dominant characteristic of erect ears. A pure-breeding pig with erect ears (EE) was crossed with a pig with drooping ears (ee).'
    add('q13bi','Q13(b)(i)','4-3-2','3-6','genetics','pure-breeding-pig-cross',
        'Copy the following into your answer book and complete the cross by filling in the spaces to show the possible gametes, genotype and phenotype.',
        [point('E',3,'Gamete of EE parent'),point('e',3,'Gamete of ee parent'),point('Ee',3,'Offspring genotype'),point('Erect ears',3,'Offspring phenotype')],
        [region(10,.45,.807)],[region(13,.315,.393)],pigs)
    add('q13bii','Q13(b)(ii)','4-3-2','3-6','genetics','f1-pig-backcross',
        'One of the offspring of the above cross is then crossed with another pure-breeding pig with erect ears. Copy the following into your answerbook and complete the cross by filling in the spaces to show the possible gametes, genotypes and phenotype.',
        [point('Ee',3,'Genotype of second parent'),point('E',3,'Gamete of the EE parent'),
         menu(['E','e'],[3,3],'Two gametes of the Ee parent'),menu(['EE','Ee'],[3,3],'Two possible offspring genotypes'),point('Erect ears',3,'Offspring phenotype')],
        [region(10,.581,.632),region(11,.04,.306)],[region(13,.392,.458)],pigs+' Use an offspring of EE × ee as the second parent.')
    add('q13ci','Q13(c)(i)','4-3-2','3-6','genetics','cell-division-types',
        'Mitosis is one of the two types of cell division. Name the other type of cell division.',[point('Meiosis',3)],
        [region(11,.35,.389)],[region(13,.49,.519)])
    add('q13cii','Q13(c)(ii)','4-3-2','3-6','genetics','mitosis-metaphase-labels',
        'The diagram shows the metaphase stage of mitosis. Name the parts of the diagram labelled L and M.',
        [point('Spindle (fibre)',3,'L'),point('Chromatid/Chromosome',3,'M')],[region(11,.389,.701)],[region(13,.516,.564)])
    figures = {
        'q6a':('cell',[('A','Cell wall'),('B','Vacuole / cell sap'),('C','Nucleus')]),
        'q10ai':('heart',[('A','Right atrium'),('B','Left ventricle'),('C','Septum')]),
        'q10bi':('reproductive',[('A','Ovary'),('B','Vagina'),('C','Uterus / womb')]),
        'q13cii':('mitosis',[('L','Spindle fibre'),('M','Chromatid / chromosome')]),
    }
    for key,(figure,labels) in figures.items():
        card = next(c for c in cards if c['id']=='agsci-2010-ol-'+key)
        card['figureKey'] = 'agsci-2010-ol-paper-'+figure
        card['labelKey'] = [dict(letter=l,meaning=m,askedInThisQuestion=True) for l,m in labels]
    # Final boundaries after rendering every distinct crop. Closely spaced
    # scheme lines share their complete printed block instead of clipping a
    # neighbouring line or removing the common tariff.
    paper_overrides = {
        'q1a':[region(2,.284,.748)],'q1c':[region(2,.875,.951)],
        'q3a':[region(3,.4,.585)],'q3b':[region(3,.61,.732)],
        'q3c-':[region(3,.741,.84)],'q3d':[region(3,.84,.922)],
        'q2-':[region(3,.05,.38)],'q4-':[region(4,.039,.25)],
        'q5':[region(4,.268,.94)],'q6a':[region(5,.057,.336)],
        'q6b':[region(5,.35,.42)],'q6c':[region(5,.35,.485)],
        'q7':[region(5,.488,.946)],'q8a':[region(6,.233,.678)],
        'q8bi':[region(6,.691,.744)],'q8bii':[region(6,.691,.744)],
        'q8c':[region(6,.756,.793)],'q8d-':[region(6,.805,.87)],
        'q9a':[region(7,.07,.166)],
        'q9b':[region(7,.07,.115),region(7,.184,.215)],
        'q9c':[region(7,.07,.115),region(7,.233,.265)],
        'q9d':[region(7,.07,.115),region(7,.233,.315)],
        'q9e':[region(7,.07,.115),region(7,.233,.265),region(7,.331,.51)],
        'q9f':[region(7,.07,.115),region(7,.52,.552)],
        'q11c':[region(9,.283,.36)],
        'q13bii':[region(10,.574,.604),region(11,.04,.306)],
    }
    scheme_overrides = {
        'q3a':[region(5,.50,.543)],'q3b':[region(5,.543,.634)],
        'q6':[region(6,.397,.499)],
        'q8aii-paddock':[region(7,.241,.311)],
        'q8aiii-strip-advantage':[region(7,.313,.395)],
        'q8aiii-strip-disadvantage':[region(7,.399,.431)],
        'q8aiii-paddock-advantage':[region(7,.436,.516)],
        'q8aiii-paddock-disadvantage':[region(7,.519,.57)],
        'q8aiv':[region(7,.574,.625)],
        'q8bi':[region(7,.685,.72)],'q8bii':[region(7,.722,.787)],
        'q9ei':[region(9,.241,.273),region(9,.276,.307),region(9,.601,.629)],
        'q9eii':[region(9,.241,.273),region(9,.309,.34),region(9,.631,.658)],
        'q9eiii':[region(9,.241,.273),region(9,.343,.374),region(9,.66,.687)],
        'q9eiv':[region(9,.241,.273),region(9,.377,.408),region(9,.69,.717)],
        'q9ev':[region(9,.241,.273),region(9,.411,.472),region(9,.719,.746)],
        'q9evi':[region(9,.241,.273),region(9,.474,.535),region(9,.749,.777)],
        'q11aii':[region(11,.098,.163)],
        'q11b':[region(11,.299,.524)],'q11c':[region(11,.564,.67)],
        'q12b':[region(12,.215,.391)],'q12c':[region(12,.42,.586)],
        'q12d':[region(12,.607,.758)],
        'q13bi':[region(13,.047,.108),region(13,.318,.464)],
        'q13bii':[region(13,.047,.108),region(13,.318,.464)],
        'q13c':[region(13,.047,.108),region(13,.484,.561)],
    }
    for key,start,end in [('q10ai',.11,.138),('q10aii',.14,.167),('q10aiii',.168,.196),
                          ('q10aiv',.198,.225),('q10av',.227,.255),('q10bi',.257,.313),
                          ('q10bii',.315,.36),('q10biii',.362,.429),('q10biv',.43,.457),('q10bv',.459,.526)]:
        scheme_overrides[key]=[region(10,.045,.08),region(10,start,end)]
    for task in tasks:
        key=task['cardIds'][0].removeprefix('agsci-2010-ol-')
        for field,overrides,prefixes in [
            ('paperRegions',paper_overrides,{'q3c-','q2-','q4-','q8a','q8d-','q9e','q11c'}),
            ('schemeRegions',scheme_overrides,{'q6','q11b','q11c','q12b','q12c','q12d','q13c'}),
        ]:
            # Exact keys win over intentionally shared prefix blocks.
            matches=[prefix for prefix in overrides if key==prefix or (prefix in prefixes and key.startswith(prefix))]
            if matches: task[field]=overrides[max(matches,key=len)]
        task['paperPage']=task['paperRegions'][0]['p']
        task['schemePage']=task['schemeRegions'][0]['p']
    return cards,tasks
