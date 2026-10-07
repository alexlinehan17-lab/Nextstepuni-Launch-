"""2012 Higher tasks from the complete original paper/scheme review.

The independent source census was transcribed first. Two printed three-of-four
pools expand mechanically; open examples remain coherent answer menus.
"""
from itertools import combinations
from agricultural_science_2010_hl import ROOT, point, menu, region
from agricultural_science_2010_parity import scan
from agricultural_science_2011_hl import variants

FILE = 'LC024ALP000EV.pdf'
HASHES = {'exampapers':'9c36dd32194d49ccb00554ebfe7960cc6be0d95e4c2e3e26c9e60df5164b571d',
          'markingschemes':'eb8f1a690343c38320680ed8425bdf0365e4ea1e4afe240d478026bf8909fdc1'}
SELECTIONS = {
    'f3a498902a4ead71':('exam-selection','Six independent examination questions are selected; every question is retained.'),
    'ce3e4e1d0e60ccd9':('independent-task-selection','Q1 selects six separately priced lettered parts. All are retained, splitting only at published internal awards.'),
    '0edb5bbb1e0254c2':('open','Q3 Option One (b)(ii) selects two factors from the student’s own preceding answer; no finite pool is printed.'),
    'a64eef37127d491b':('independent-task-selection','Q4 selects two independently priced 24-mark methods. All four are retained.'),
    '341e437d57edf3c6':('open','Q6(c) asks for one hormone without a printed finite pool. Scheme examples are coherent answer menus.'),
    '0e1658b6d9ac7f04':('closed','Q7(a) prints four terms and asks for three. All four combinations are retained.'),
    '2400d5f4cae0b778':('required-condition','Q7(b)(ii) crosses two of the new hybrids, both BE. This is a required parent condition, not a finite response selection.'),
    '3514ced833fb6e33':('independent-task-selection','Q8 selects two independently priced parts. All internal tasks and finite comparison routes are retained.'),
    'b8d6b839e57eec1c':('closed','Q8(c) prints four comparison pairs and asks for three. All four complete combinations are retained.'),
    '7f8409467c8fcc41':('independent-task-selection','Q9 selects four independently marked twelve-mark explanations. All five are retained.'),
}
SCIENTIFIC = {
    'q4d':('https://files.givewell.org/files/DWDA%202009/Interventions/ORS/WHO_Oral_rehydration_salts_report_2006.pdf',
        'The historical scheme prints “sodium cobalt nitrate” and a purple potassium result. The sodium cobaltinitrite test produces a yellow-orange precipitate; violet/purple is associated with the potassium flame test. WHO, Oral Rehydration Salts: Production of the new ORS (2006), section 4.3.6.1. The original wording and tariff remain visible.'),
    'q8bii':('https://www.fao.org/4/x7660e/x7660e06.htm',
        'The scheme’s “dry to 20%” refers to moisture content, not dry matter. FAO’s Haymaking chapter describes reducing moisture to 12–20% before storage, depending on the crop and storage conditions.'),
}
SOURCE_NOTES = {
    'q5biii':'The examination paper repeats (ii) beside Earthing-up. The scheme correctly numbers this third practice (iii); this task uses (iii) and retains the original paper crop.',
    'q7bii':'The scheme labels the hybrid intercross offspring F1. Relative to the original Barra × Evita cross, these are the F2 generation. Parents BE × BE and the original genotypes, phenotypes and ten-mark tariff are unchanged.',
    'q8c':'The scheme repeats (ii) beside catch crop and nurse crop. The examination paper correctly labels that pair (iii); the practice routes follow the paper.',
}


def paper_review():
    observed,supplementary=scan(2012,FILE,HASHES,SELECTIONS,[
        (3,'OR 3. Option Two','closed','Both alternative Q3 options are retained at their distinct task addresses.'),
        (3,'a laboratory or field method','open','Setting and method are open; each of the four required outcomes is a separately marked task.'),
        (2,'a named soil texture','open','The student names a texture and explains its three linked effects. No finite named pool is printed.'),
        (4,'one natural method of vegetative reproduction','open','The scheme lists examples; the paper prints no finite choice list.'),
        (4,'a Punnett square or other suitable method','equivalent-presentation','Equivalent representations of the same cross do not create separate practice responses.'),
        (3,'a table or a pie-chart','equivalent-presentation','Equivalent presentations share the same composition and presentation tariff.'),
    ])
    notes=[dict(questionN=key[1],questionRef={'q5biii':'Q5(b)(iii)','q7bii':'Q7(b)(ii)','q8c':'Q8(c)'}[key],note=note) for key,note in SOURCE_NOTES.items()]
    notes += [dict(questionN=key[1],questionRef={'q4d':'Q4(d)','q8bii':'Q8(b)(ii)'}[key],note=note,source=url) for key,(url,note) in SCIENTIFIC.items()]
    return dict(year=2012,level='higher',lang='ev',paperFileid=FILE,hashes=HASHES,
                wholePaperVisualReview='reviewed',schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1,9)),schemePagesInspected=list(range(1,17)),
                selectionDirectives=observed,supplementarySelections=supplementary,sourceNotes=notes,
                independentBoundaryReview='56 base tasks and 62 routes. Shared first-correct scales remain whole. Two printed three-of-four pools expand to four routes each. Milk composition, soil profile and growth-curve drawing retain the published partial bands under manual question-total marking.',
                cropVisualReview='All 56 distinct crop pairs inspected. Clipped scheme continuation, growth-curve axis, neighbouring-line fragments and shared Q4/Q9 tariffs corrected and re-rendered. Both original solution images inspected.',
                runtimeReview='42 integrated production-component cases at 1200px and 390px: source reveal/hide, nonblank crops, full-reader zoom/toggle/return, marking menus, manual question-total grading and solution images; no page errors. Signed-in full-app navigation remains open.',
                remaining=['Irish edition comparison','Full application navigation review','Corpus-wide reconciliation'])


def reviewed_tasks():
    paper_review()
    cards,tasks=[],[]
    def add(key,ref,topic,old,atlas,concept,question,rows,pp,sp,stem=None,marks=None,selection=None,figure=None):
        cid='agsci-2012-hl-'+key
        rows=[dict(row,id=f'r-{i+1}') for i,row in enumerate(rows)]
        card=dict(id=cid,subjectId='agricultural-science',year=2012,level='higher',
                  section='A' if key.startswith('q1') else 'B',questionRef='2012 HL '+ref,
                  topicId='agsci-'+topic,curriculumNodeIds=['agricultural-science-'+t for t in old.split('|')],
                  conceptId=concept,questionText=question,rows=rows,
                  totalMarks=marks if marks is not None else sum(r['marks'] for r in rows),
                  tariffModel={'kind':'questionTotal' if marks is not None else 'fixed'},
                  sourceMaterial=dict(kind='source-text',label='OFFICIAL QUESTION PAGE',title='Agricultural Science 2012 Higher — '+ref,
                      pages=sorted({r['p'] for r in pp}),attribution='SEC Agricultural Science 2012 Higher Level examination paper — © State Examinations Commission.',
                      presentationNote='Open the original page for the published wording and examination context.'))
        if stem: card['stem']=stem
        if figure: card['figureKey']=figure
        task=dict(questionRef=card['questionRef'],paperPage=pp[0]['p'],schemePage=sp[0]['p'],paperRegions=pp,schemeRegions=sp,
                  atlasNumbers={cid:str(1001+len(cards))},cardIds=[cid],marksPerRoute=card['totalMarks'],
                  examTopicIds=['agricultural-science-higher-'+t for t in atlas.split('|')],
                  selection=selection or {'kind':'none','reason':'Required response. Open examples and scheme alternatives remain marking menus, not finite printed routes.'},
                  evidence='All 8 paper and 16 scheme pages visually inspected. Published task boundaries and awards independently transcribed before authoring.')
        note_key='q8c' if key.startswith('q8c-route-') else key
        if note_key in SOURCE_NOTES: task['schemeNote']=SOURCE_NOTES[note_key]
        if key in SCIENTIFIC:
            url,note=SCIENTIFIC[key];task['schemeNote']=note
            task['scientificContext']={'source':url,'checkedAt':'2026-10-07','treatment':'Retain historical wording and tariff with a source-grounded clarification.'}
        if task.get('schemeNote'): rows[0]['contextNote']=(rows[0].get('contextNote','')+' '+task['schemeNote']).strip()
        cards.append(card);tasks.append(task)
        return card

    add('q1ai','Q1(a)(i)','3-2','2-1','classification-of-animals-plants','monocot-dicot-examples',
        'Name one monocot plant and one dicot plant.',[point('Grass/ barley/ correct example',2,'Monocot.'),point('Dock/ dandelion/ correct example.',2,'Dicot.')],
        [region(2,.071,.091)],[region(5,.139,.175)])
    add('q1aii','Q1(a)(ii)','3-2','2-1','classification-of-animals-plants','monocot-dicot-differences',
        'List two differences between monocot plants and dicot plants.',
        [point('Monocot: one cotyledon in seed/ parallel veins in leaves/ vascular bundles scattered in stem/ flower parts in 3s/ fibrous roots/ correct feature.',None,'The published scheme allocates three marks to the monocot side. Compare two matching features across both plant groups.',kind='criterion'),
         point('Dicot: Two cotyledons in seed/ reticulate veins in leaf/ vascular bundles in a circle in stem/ flower parts in 4s or 5s/ tap roots/ correct feature.',None,'Three marks for the dicot side. The paper requests two differences; do not award the full six for only one complete contrast.',kind='criterion')],
        [region(2,.092,.11)],[region(5,.177,.276)],marks=6)
    add('q1b','Q1(b)','4-2','3-1','classification-of-animals-plants','mammalian-characteristics','Give three characteristics of members of the class Mammalia.',
        [menu('Body covered in hair or wool or fur|sweat glands present|mammary glands in female (produce milk)|embryo develops internally|placenta present',[4,3,3])],
        [region(2,.116,.139)],[region(5,.276,.325)])
    add('q1ci','Q1(c)(i)','3-1','2-0','plant-physiology','weed-seed-dispersal-methods','Mention two methods by which weed seeds are dispersed.',
        [menu('Wind|animals|water|self|farming activity',[2,2])],[region(2,.146,.167)],[region(5,.325,.34)])
    add('q1cii','Q1(c)(ii)','3-1','2-0','plant-physiology','weed-seed-dispersal-examples','For each method, name a common weed that uses this method of dispersal.',
        [menu(['Wind: Dandelion/ thistle/ correct example.','Animals: Burdock/ blackberry/ correct example.','Water: Water lily/ alder/ correct example.',
               'Self: Vetch/ furze/ correct example.','Farming activity: Docks in slurry/ correct example.'],[3,3],'One matching weed for each of your two distinct methods. Methods themselves are awarded in part (i).')],
        [region(2,.146,.184)],[region(5,.34,.417)],'Mention two methods by which weed seeds are dispersed, then give one matching weed for each.')
    add('q1d','Q1(d)','4-1','3-0','animal-physiology-digestive-system|animal-physiology-respiratory-system','animal-tissue-locations-and-functions',
        'State the precise location and function of (i) alveolus, (ii) adipose tissue and (iii) abomasum in the body of a farm animal.',
        [menu(['(End of bronchioles) in lungs','gas exchange','Under the dermis(skin)','correct function.','Chamber in ruminant stomach (or named ruminant)','correct function.'],[2,2,2,2,1,1],
              'The six entries follow location/function for alveolus, adipose tissue and abomasum. The scheme leaves the last two functions open; judge adipose storage/insulation and the abomasum’s digestive function appropriately. The first four correct fields earn two marks each, then one each.')],
        [region(2,.191,.259)],[region(5,.416,.477)])
    add('q1e','Q1(e)','4-1','3-0','beef-cattle|animal-physiology-digestive-system','calf-roughage',
        '(i) Suggest a reason for including roughage. (ii) When is roughage introduced? (iii) Name a suitable food that could be used as roughage.',
        [menu(['To develop rumen/ scratch factor.','After 7 days.','Hay/ straw/ haylage'],[4,3,3],'One answer per field; the first correct field earns four marks.')],
        [region(2,.266,.334)],[region(5,.476,.526)],'Roughage must be included in the diet of a calf.')
    tram=['Access for machinery for spraying','fertilising','prevents trampling of crop','prevents attack from crows or pigeons']
    c=add('q1f','Q1(f)','3-3-1','2-3','crop-production','tramlines',
        'Explain the agricultural term tramlines and give two reasons for their use.',
        [menu(['Parallel unsown tracks in a field of cereal.',*tram[:2]],[4,3,3])],[region(2,.341,.364)],[region(5,.526,.593)])
    variants(c,[(f'reasons-{i}',' + '.join(pair),[menu(['Parallel unsown tracks in a field of cereal.',*pair],[4,3,3],
        'Definition and two distinct reasons share the first-correct scale. Choose the two reasons you answered; the reasons are an open marking menu, not new practice identities.')]) for i,pair in enumerate(combinations(tram,2),1)])
    add('q1g','Q1(g)','2-1','1-0','soil-science','limestone-granite-soils','Compare limestone and granite as parent materials in soil formation.',
        [menu('Alkaline (high pH)|better structure|contains calcium|good drainage|best pH for absorption of mineral|intermediate texture|better ion exchange',[3,2],'Limestone: two distinct points.'),
         menu('Acidic soil|more leaching|infertile|could lead to podzol formation|coarse texture|poorer ion exchange',[3,2],'Granite: two distinct points.')],
        [region(2,.371,.394)],[region(5,.592,.669)])
    add('q1h','Q1(h)','4-3-2','3-6','genetics','meiosis-scenarios',
        'Name the type of cell division (i) that produces four daughter cells from one mother cell, (ii) that always produces haploid daughter cells, and (iii) during which crossing over occurs.',
        [menu(['Meiosis (reduction division)','Meiosis (reduction division)','Meiosis (reduction division)'],[4,3,3],
              'The three entries mark the three separate scenarios in order; the same answer is required in each. Apply the first-correct scale across the three fields.')],
        [region(2,.401,.469)],[region(5,.668,.719)])
    add('q1i','Q1(i)','3-1','2-0','plant-physiology','plant-tissue-functions','State the function of (i) xylem, (ii) meristem and (iii) palisade.',
        [menu(['Xylem: Transports water/ minerals/ strengthens plant.','Meristem: Actively divides/ undergoes mitosis/ gives new growth/ gives rise to secondary tissue.',
               'Palisade: Absorbs light/ contains chloroplasts/ carries out photosynthesis.'],[4,3,3],'One function per tissue; alternatives within a tissue earn no extra marks.')],
        [region(2,.476,.544)],[region(5,.718,.794)])
    add('q1ji','Q1(j)(i)','4-3-1','3-3','pigs','sow-litter-and-weaning-targets','Indicate the average litter size and the target number of bonhams weaned per annum for a sow.',
        [point('Average litter size: 11.5 (10-12)',3),point('Target number: 23-29.',3)],[region(2,.552,.587)],[region(5,.794,.827)])
    add('q1jii','Q1(j)(ii)','4-3-1','3-3','pigs','improving-bonham-survival','Suggest two ways by which the number of bonhams weaned per annum could be increased.',
        [menu('Dose|vaccinate|inject with iron|correct housing|correct temperature|use farrowing crate|feed correct concentrate|feed lysine|contact vet|breed(prolific)',[2,2])],
        [region(2,.584,.619)],[region(5,.827,.88)])

    add('q2ai','Q2(a)(i)','2-1','1-0','soil-science','brown-earth-tillage','Suggest two reasons why brown earth soils are suited to tillage.',
        [menu('Deep soil|naturally fertile|well drained|easily worked|suitable pH|aeration',[3,3])],[region(2,.717,.768)],[region(6,.143,.181)])
    add('q2aii','Q2(a)(ii)','2-1','1-0','soil-science','brown-earth-profile','Draw a large labelled diagram of a brown earth soil profile.',
        [point('Diagram: Deep A horizon/ little banding or layers/ gradual lightening of colour from A to B horizon.',None,'Diagram earns 4, 2 or 0 marks; compare the complete profile with the published features.',kind='criterion'),
         point('Labels: Three correct.',None,'Three correct labels at two marks each. Add these to the diagram award for a maximum of ten.',kind='criterion')],
        [region(2,.717,.751),region(2,.767,.785)],[region(6,.18,.247)],marks=10)
    textures=[('sandy','Sandy',['Large pore spaces.','Good drainage/ poor capillarity.','Infertile/ more leaching']),
              ('clay','Clay',['Small pore spaces.','Poor drainage/ waterlogging/ good capillarity.','Naturally fertile/ little leaching']),
              ('loam','Loam',['Some small and some large pores.','Good drainage/ good capillarity.','Fertile/ not as fertile as clay.'])]
    c=add('q2b','Q2(b)','2-2-2','1-3|1-2','soil-science','soil-texture-effects','Explain how a named soil texture influences (i) pore spaces, (ii) water movement and (iii) fertility.',
        [point('Sandy',2),*[point(t,2) for t in textures[0][2]]],[region(2,.792,.86)],[region(6,.246,.575)])
    variants(c,[(key,label,[point(label,2,'Name one texture; keep all three explanations consistent with it.'),*[point(t,2,note) for t,note in zip(rows,['Pore spaces.','Water movement.','Fertility.'])]]) for key,label,rows in textures])
    add('q2c','Q2(c)','2-3','1-6','soil-science|scientific-practices-experiments-investigations','phosphate-deficiency-experiment',
        'Describe a laboratory experiment to show the effect of phosphate deficiency in a plant.',
        [menu('Two flasks|two (suitable) plants|Sacch’s solution|make up solutions|distilled water|one is complete control|one solution minus phosphate|supply oxygen|equal volume of solution in each flask|plant placed in solution|cover flasks with black paper|leave for a number of weeks|in sunlight|compare with control|blue colour on edge of leaves deficient in phosphate or poor root growth',[4]*6)],
        [region(2,.867,.89)],[region(6,.571,.725)])

    add('q3o1a','Q3 Option One (a)','4-1','3-0','dairy-cattle','milk-composition',
        'Using a table or a pie-chart, show the composition of cow’s milk.',
        [point('Table/ pie-chart',None,'Presentation earns 3, 1 or 0 marks.',kind='criterion'),
         point('Composition: Water 87.8%; Butterfat 3.5%; Protein 3.2%; Lactose 4.7%; Minerals(or ash or named mineral) 0.8%',None,
               'Award up to four component names at one mark each and four correct matching percentages at one mark each. Five components are listed as acceptable answers, but only four names and four percentages are paid. Maximum eleven including presentation.',kind='criterion')],
        [region(3,.045,.098)],[region(7,.111,.184)],marks=11)
    factors='Health (disease)|age|stage of lactation|diet|breed|milking interval|morning or evening milk|stage of milking (strippings)'
    add('q3o1bi','Q3 Option One (b)(i)','4-3-1','3-3','dairy-cattle','milk-composition-factors','List four factors that can cause changes in milk composition.',
        [menu(factors,[2]*4,'Four distinct factors; avoid crediting two descriptions of the same milking-interval effect.')],[region(3,.105,.124)],[region(7,.182,.248)])
    add('q3o1bii','Q3 Option One (b)(ii)','4-3-1','3-3','dairy-cattle','explaining-milk-composition',
        'Fully explain any two of the factors referred to above.',
        [menu(['Health: mastitis reduces fat and protein/ lameness reduces food intake and reduce protein and fat.','Age: Butterfat and protein decline with age.',
               'Stage of lactation: Protein and butterfat increase during the lactation.','Diet: High fibre diet increases butterfat/ high protein diet (leafy grass) increase protein.',
               'Breed: Jersey has higher butterfat (than Holstein)/ Jersey has higher protein (than Holstein).','Milking Interval: Cows milk more in the morning and milk has reduced butterfat.'],[4,4],
              'Explain two distinct factors from your own preceding list. Each factor earns at most four marks; the scheme examples do not form a printed closed choice pool.')],
        [region(3,.105,.143)],[region(7,.182,.462)],'First list four factors that can cause changes in milk composition. Choose two of your listed factors to explain; listing marks belong to part (i).',
        selection={'kind':'open','reason':'Selection from student-generated answers; no finite source list.'})
    add('q3o1ci','Q3 Option One (c)(i)','4-3-1','3-3','dairy-cattle','milk-contaminants','List three contaminants of milk.',
        [menu('Antibiotics|bacteria|somatic cells|excess water|sediment (soil particles)',[2]*3)],[region(3,.15,.184)],[region(7,.458,.496)],'Contamination of milk is a problem in milk processing.')
    milk_methods=[('dye','Resazurin or methylene blue','Two sterile test tubes|two milk samples|one is a control|add (10cm3) milk to each test tube|add (1 cm3 of) Resazurin (or methylene blue) to the milk samples|keep at 37°C|for 10 to 15 minutes|blue is best|white is worst|pink or mauve or lilac (better than white, worse than blue)|control stays blue.'),
                  ('agar','Nutrient agar','Two sterile petri dishes|nutrient agar in each|one is a control|inoculate one with milk|using a sterile (inoculating) loop|seal each Petri dish|incubate at 37°C|invert|for 24 hours|compare with control|colonies of bacteria in petri dish with milk|control is clear.')]
    c=add('q3o1cii','Q3 Option One (c)(ii)','4-3-1','3-3','dairy-cattle|scientific-practices-experiments-investigations','milk-hygienic-quality',
        'Describe an experiment to test the hygienic quality of milk.',[menu(milk_methods[0][2],[3]*5)],[region(3,.15,.17),region(3,.184,.199)],[region(7,.494,.743)])
    variants(c,[(key,label,[menu(pool,[3]*5,'Five points from one coherent experimental method. The printed 37°C uses a raised zero in the source text layer.')]) for key,label,pool in milk_methods])
    add('q3o2a','Q3 Option Two (a)','4-3-1','3-3','sheep','ewe-pregnancy-scanning','Discuss the role of scanning in sheep production.',
        [menu('Used to find if ewe is pregnant or barren|single or multiple lambs|determines feeding regime|possible culling',[4]*3)],[region(3,.285,.338)],[region(8,.111,.167)])
    add('q3o2bi','Q3 Option Two (b)(i)','4-3-2','3-6','sheep','terminal-sire',
        'Explain the term terminal sire as it applies in sheep breeding.',
        [menu('Ram used to produce lambs with high growth rates|good quality carcass|for slaughter|and good meat quality|good conformation',[4]*2)],[region(3,.346,.367)],[region(8,.166,.231)])
    add('q3o2bii','Q3 Option Two (b)(ii)','4-3-2','3-6','sheep','terminal-sire-breeds','Suggest two breeds that could be used as terminal sires.',
        [menu('Suffolk|Texel|Charollais|Belclare|any valid breed',[2,2],'Two distinct suitable breeds; a valid unlisted breed earns the same award.')],[region(3,.346,.379)],[region(8,.232,.267)])
    add('q3o2biii','Q3 Option Two (b)(iii)','4-3-2','3-6','sheep','terminal-sire-breed-reasons','Give a reason for each of your choices in part (ii).',
        [menu(['Suffolk: Good carcass quality/ excellent conformation/ fast growth rate.','Texel: Good carcass quality/ lean meat/ good conformation.',
               'Charollais: Good weight gain/ large hind quarters/ fast growth rate/ lean lamb/ less lambing difficulty','Belclare: Excellent carcass quality/ good weight gain.'],[4,4],
              'One valid matching reason for each of your two distinct breeds; several reasons for one breed still earn only four marks. The preceding naming part accepts any valid breed.')],
        [region(3,.346,.398)],[region(8,.276,.43)],'Suggest two breeds that could be used as terminal sires, then justify each choice. Breed-naming marks belong to part (ii).')
    add('q3o2c','Q3 Option Two (c)','4-3-1','3-3','sheep','flushing-steaming-up',
        'Compare flushing with steaming-up as feeding strategies in sheep production.',
        [menu('Ewes placed in low plane of nutrition|followed by a high plane of nutrition|prior to mating|increases ovulation or better conception rates|better attachment of embryos|greater litter size|more regular heats',[4,4],'Flushing: two points.'),
         menu('Increased concentrates|0.25kg to 0.75kg extra per day|in last six weeks of pregnancy|most foetal growth occurs at this time|prevents twin-lamb disease|healthier lambs|more colostrums (milk)|improve condition score or correct figure',[4,4],'Steaming-up: two points.')],
        [region(3,.404,.423)],[region(8,.429,.628)])

    silage_methods=[
        ('leaf-stem','Leaf-to-stem ratio','weigh sample of silage|separate the leaves from the stems|take two dishes|weigh them|put leaves in one and stems in other|weigh|get ratio of leaf to stem|correct conclusion.'),
        ('ph','pH test','squeeze sample of silage|collect liquid|add distilled water|test for pH|record the colour|compare with colour chart|correct conclusion.'),
        ('dm','Dry-matter content','weigh a sample of silage|record|dry sample in an oven|at 100°C|repeat weighing until mass is constant|record final mass|calculate % DM|correct conclusion (16-20% DM).'),
        ('sensory','Physical quality','colour|yellow green (black-brown)|smell|slight or sharp (sweet or sour)|taste|sharp acidic (not sharp acidic)|feel|firm (mushy)|squeeze with two hands|releases a small amount of liquid or none (liquid released with one hand).')]
    c=add('q4a','Q4(a)','3-3-2','2-6','grassland|scientific-practices-experiments-investigations','silage-quality-experiment',
        'Describe a laboratory or field method to assess the quality of grass silage.',[menu(silage_methods[0][2],[4]*6)],
        [region(3,.539,.562),region(3,.57,.592)],[region(9,.066,.336)])
    variants(c,[(key,label,[menu(pool,[4]*6,'Six points from one coherent method; do not combine separate experimental versions. Physical-quality brackets describe poor-quality comparisons.')]) for key,label,pool in silage_methods])
    add('q4b','Q4(b)','3-1','2-0','plant-physiology|scientific-practices-experiments-investigations','plant-cell-slide',
        'Describe a laboratory or field method to prepare a sample of plant cells for examination under a microscope.',
        [menu('Get a clean glass slide|wet it|remove a piece of plant tissue|using a scalpel or blade|place on the slide|correct method of applying|stain with iodine solution|leave for a few minutes|coverslip|drain excess stain',[4]*6)],
        [region(3,.539,.562),region(3,.6,.622)],[region(9,.066,.334),region(9,.331,.402)])
    add('q4c','Q4(c)','3-1','2-0','plant-physiology|scientific-practices-experiments-investigations','carbon-dioxide-photosynthesis',
        'Describe a laboratory or field method to show that carbon dioxide is necessary for photosynthesis.',
        [menu('Get two potted plants of similar size|label them (A and B)|destarch the plants|place a dish of soda lime or sodium hydroxide under plant A|to absorb CO2|place a dish of sodium hydrogencarbonate under plant B|control|to supply CO2|cover both plants with clear plastic bags|leave in light|test a leaf from each plant for starch|result: plant A has no starch (B has starch)',[4]*6)],
        [region(3,.539,.562),region(3,.63,.652)],[region(9,.066,.334),region(9,.397,.517)])
    add('q4d','Q4(d)','2-3','1-6','soil-science|scientific-practices-experiments-investigations','cation-exchange-experiment',
        'Describe a laboratory or field method to demonstrate cation exchange in a soil.',
        [menu('Sample of sieved soil or soil with a high pH or calcium rich or high clay|in filter paper|in a funnel|add (1%) KCl solution or potassium solution|test leachate for calcium|using ammonium oxalate|white ppt. indicates presence of calcium|add distilled water|to wash KCl from soil|test for potassium|by adding sodium cobalt nitrate and a few drops of ethanol|purple indicates presence of potassium|potassium has replaced calcium',[4]*6)],
        [region(3,.539,.562),region(3,.66,.678)],[region(9,.066,.334),region(9,.512,.651)])

    add('q5a','Q5(a)','3-3-1','2-3','crop-production','wheat-barley-cultivation',
        'Give four reasons why the area under wheat cultivation is much less than the area under barley cultivation in Ireland.',
        [menu('grows well in Irish climate|more valuable for animal feed|higher in protein|higher in fibre|straw can be fed to cattle|malting barley is used in brewing (and distilling) industry|price in Ireland is poor|wheat grain not suitable for flour|lack of suitable varieties|more prone to disease|greater fertiliser requirement',[4]*4,
              'The first six entries refer to barley; the remaining five to wheat. Credit at most one climate point. These are the historical 2012 scheme reasons.')],
        [region(4,.06,.098)],[region(10,.126,.247)])
    for roman,label,answer,py,sy in [
        ('i','Sprouting','Speeds up growth/ increases yield/ for early potato production.',(.14,.154),(.245,.28)),
        ('ii','Burning-off the haulms','Makes harvesting easier/ prevents spread of blight to tubers/ to toughen the skin.',(.155,.169),(.279,.313)),
        ('iii','Earthing-up','Prevents ‘greening’ of tubers/ prevents spread of blight to tubers/ weed control/ pest control/ increases yield/ supports stem.',(.17,.184),(.312,.362)),
        ('iv','Using certified seed','Free of disease/ better yield/ true to type/ higher germination/ pest-free.',(.185,.2),(.363,.396)),
    ]:
        add('q5b'+roman,f'Q5(b)({roman})','3-3-1' if roman in ['i','iv'] else '3-3-2','2-3' if roman in ['i','iv'] else '2-4','crop-production','potato-practice-'+roman,
            'Give a reason for the following practice in potato cultivation: '+label+'.',[point(answer,4,'One reason.')],
            [region(4,.121,.139),region(4,*py)],[region(10,*sy)])
    add('q5c','Q5(c)','3-3-3','2-5','crop-production','potato-storage-losses',
        'Outline four reasons for losses occurring in potatoes during storage.',
        [menu('Overheating|sprouting|rotting|frost damage|damage by pests|disease|damaged during harvesting|harvested when wet|poor ventilation',[4]*4)],
        [region(4,.227,.245)],[region(10,.391,.447)])

    growth='Construct the typical growth curve graph for the two-year calf-to-beef production system.'
    add('q6ai','Q6(a)(i)','4-3-1','3-3','beef-cattle','calf-to-beef-growth-curve',growth,
        [point('Labelled axes',None,'Two axes at two marks each: liveweight and age. Consult the official graph.',kind='criterion'),
         point('Growth curve',None,'Curve earns 6, 3 or 0 marks. Add the axis marks for a maximum of ten; use the published curve as the comparison.',kind='criterion')],
        [region(4,.332,.354)],[region(11,.111,.373)],marks=10,figure='agsci-2012-hl-scheme-growth-curve')
    add('q6aii','Q6(a)(ii)','4-3-1','3-3','beef-cattle','winter-weights-compensatory-growth',
        'On your graph show clearly: 1. Target weights at first winter housing and second winter housing. 2. Where compensatory growth begins.',
        [point('First winter housing: 200 kg (190-210 kg)',2,'Show on the graph.'),point('Second winter housing: 460 kg (450-470 kg)',2,'Show on the graph.'),
         point('Compensatory growth (all shown on graph)',2,'Mark where the accelerated spring growth begins after the first winter; compare the official graph.',kind='criterion')],
        [region(4,.332,.429)],[region(11,.111,.444)],growth,figure='agsci-2012-hl-scheme-growth-curve')
    add('q6aiii','Q6(a)(iii)','4-3-1','3-3','beef-cattle','winter-beef-diets',
        'Suggest a suitable diet for the beef cattle in the first and second winter.',
        [point('(Good quality) silage and concentrates',2,'First winter.'),point('(Good quality) silage and concentrates',2,'Second winter.')],
        [region(4,.332,.354),region(4,.437,.46)],[region(11,.442,.494)],'Two-year calf-to-beef production system.')
    add('q6b','Q6(b)','4-3-3','3-5','dairy-cattle|animal-diseases','mastitis-prevention',
        'Suggest a suitable mastitis-prevention programme in a spring-calving dairy herd.',
        [menu('Hygiene in housing|washing udders and teats (before milking)|clean milking machine|service milking machine|hygiene in the dairy|teat dips|treat sores on teats|treat infected cows with antibiotics|insect control|milk separately|cull cows prone to disease|dry cow treatment|do not over-milk or under-milk',[4]*4)],
        [region(4,.482,.505)],[region(11,.506,.626)])
    hormones=[('oxytocin','Oxytocin','Oxytocin|pituitary gland|causes (muscles of) alveoli or milk secreting tissue|to contract|forcing milk into the teat (cisterns)|resulting in milk letdown.'),
              ('prolactin','Prolactin','Prolactin|pituitary gland|stimulates production of milk|in mammary glands|maintains lactation.')]
    c=add('q6c','Q6(c)','4-1','3-0','dairy-cattle','milk-hormones','Outline the role of any one hormone in milk production in a lactating cow.',
        [menu(hormones[0][2],[4]*3)],[region(4,.512,.531)],[region(11,.622,.726)])
    variants(c,[(key,label,[menu(pool,[4]*3,'Three points about the one hormone you selected.')]) for key,label,pool in hormones])

    terms={
        'i':('Sex linkage','Where a gene (for a non-reproductive trait) is carried on the sex (or X) chromosome'),
        'ii':('Continuous variation','Where there is a range of phenotypes between two extremes or controlled by a number of genes (interacting with each other)'),
        'iii':('Genetically modified (GM) crops','Where the genotype of a crop is altered (to produce an improved variety).'),
        'iv':('Binary fission','Division of a cell into two or type of (asexual) reproduction in unicellular organisms or named.'),
    }
    for selected in combinations(terms,3):
        add('q7a-route-'+'-'.join(selected),'Q7(a) — '+', '.join(selected),'4-3-2','3-6','genetics','genetics-terms',
            'Explain three of the following terms: (i) Sex linkage. (ii) Continuous variation. (iii) Genetically modified (GM) crops. (iv) Binary fission.',
            [point(terms[k][1],4,terms[k][0]+'.') for k in selected],[region(4,.617,.7)],[region(12,.111,.266)],
            'Practice choice: '+', '.join(terms[k][0] for k in selected)+'.',selection={'kind':'closed','choose':3,'options':list(terms),'route':list(selected)})
    oats='In cereal trials for oats, pure-breeding Barra (approximately 500 mm straw length) was crossed with pure-breeding Evita (approximately 800 mm). The hybrid had an approximate straw length of 650 mm. Use B for the 500 mm gene and E for the 800 mm gene.'
    add('q7bi','Q7(b)(i)','4-3-2','3-6','genetics','oat-incomplete-dominance',
        'Show how this hybrid result arose.',[point('BB',2,'Pure-breeding Barra parent.'),point('EE',2,'Pure-breeding Evita parent.'),point('BE',2,'Hybrid offspring, explaining the 650 mm result.')],
        [region(4,.722,.816)],[region(12,.264,.295)],oats)
    add('q7bii','Q7(b)(ii)','4-3-2','3-6','genetics','oat-hybrid-intercross',
        'Using a Punnett square or other suitable method, show the genotypes and matching phenotypes resulting from a cross between two of the new hybrids.',
        [point('Parents BE x BE',2),point('Layout of cross',2,'A complete correctly arranged cross; no separate gamete award is printed.',kind='criterion'),
         menu(['BB','BE','EE'],[1]*3,'The three distinct offspring genotypes, correctly derived. The two BE cells represent one genotype award.'),
         menu(['500mm (BB)','650mm (BE)','800mm (EE)'],[1]*3,'Each phenotype must match its genotype; the repeated BE phenotype earns no extra mark.')],
        [region(4,.722,.85)],[region(12,.293,.498)],oats,figure='agsci-2012-hl-scheme-oat-cross')
    methods=[('tuber','Stem tubers','Stem tubers|for food storage (in potatoes)|aerial parts die away in winter|new growth from tubers in spring.'),
             ('rhizome','Rhizomes','Rhizomes|underground stem|grow horizontally|produce adventitious roots|new shoots'),
             ('runner','Runners','Runners|young shoots grow out from the stem|roots develop at points along the stem|new plants grow from these'),
             ('corm','Corms','Corms|swollen underground stems|produce new growth from buds'),
             ('bulb','Bulbs','Bulbs|food stored in swollen leave|side buds produce new growth'),
             ('root-tuber','Root tubers','Root tubers|swollen fibrous roots|store food|new growth from buds at base of old stem.'),
             ('stolon','Stolon','Stolon|overground stem|touches the ground|produces new roots at point of contact|grows new shoot.')]
    c=add('q7c','Q7(c)','3-1','2-0','plant-physiology','natural-vegetative-reproduction','Describe one natural method of vegetative reproduction in plants.',
        [menu(methods[0][2],[4]*3)],[region(4,.858,.88)],[region(12,.494,.729)])
    variants(c,[(key,label,[menu(pool,[4]*3,'Three points describing one coherent method. The scheme examples are not a finite printed response pool.')]) for key,label,pool in methods])
    add('q7d','Q7(d)','4-3-1','3-3','animal-physiology-reproductive-systems','castration-reasons','Identify two reasons why male animals are castrated on farms.',
        [menu('Males are aggressive|danger to the farmer|a lot of fencing required|meat not as marketable|interfere with breeding programme',[4,4])],
        [region(4,.888,.906)],[region(12,.73,.797)])

    add('q8a','Q8(a)','2-3','1-6','fertilisers-pollution-environment-cycles','nitrogen-cycle',
        'Describe, with the aid of a labelled diagram, how the element nitrogen is recycled in nature.',
        [point('Diagram.',None,'A correct labelled nitrogen-cycle diagram.',kind='criterion'),
         point('Nitrogen gas / nitrogen fixation / lightning / in root nodules of clover (legumes) / by rhizobium / nitrogen converted to nitrates / plant protein / animal protein / animal and plant manures provide soil organic matter / undergoes mineralisation (decomposition) to produce ammonium ions / nitrification to nitrites / by nitrosomonas / nitrification to nitrates / by nitrobacter / nitrates provide protein to soil organisms (fungi or bacteria) / nitrates leached from soil / denitrification to nitrogen gas / anaerobic / volatilisation / addition of artificial fertilisers',None,
              'Five distinct correctly linked points at four marks each; add the four-mark diagram award for a maximum of twenty-four. Use the original scheme to record partial credit. Biological nitrogen fixation produces ammonia/ammonium; nitrification subsequently produces nitrite and nitrate. Keep those stages distinct when using the scheme’s abbreviated wording.',kind='criterion')],
        [region(5,.075,.098)],[region(13,.133,.285)],marks=24)
    add('q8bi','Q8(b)(i)','3-3-2','2-6','grassland','hay-in-farming','Defend the statement: “There will always be a role for hay in Irish farming.”',
        [menu('Good dry matter source for livestock|can be fed to cattle, sheep and horses|does not cause pollution|lower cost|no plastic waste|no preservatives needed|develops rumen in calves (scratch factor)|convenience',[4]*3)],
        [region(5,.105,.139)],[region(13,.284,.346)])
    add('q8bii','Q8(b)(ii)','3-3-3','2-5','grassland','hay-conservation','Outline three principal steps in conserving grass as hay.',
        [menu('Close off field 6 weeks before cutting|cut when stemmy (or heading out or correct growth stage)|when a prolonged period of dry weather is expected|(rotary) mower is used to cut grass|(rotary) tedder shakes grass to speed up the drying process|dry to 20%|baler collects the grass and bales it|bales are secured by baling twine|store under cover',[4]*3)],
        [region(5,.14,.158)],[region(13,.345,.437)])
    pairs={
        'i':('Lungworm and ringworm','animal-diseases','Nematode|endoparasite|affects respiratory tract (lungs)|causes hoose|not a zoonosis.','Fungus (fungal disease)|ectoparasite|affects skin and hair on neck and head|zoonosis.'),
        'ii':('Breeding unit and finishing unit','pigs','Pigs weigh less than 32Kg|dry sow house|farrowing house|20°C|farrowing crate|weaner house 24°C|age range birth to 12 weeks|with sow for first 5 weeks until weaned|boar present.','Pigs weigh more than 32 kg|pigs reared for slaughter|22°C|age range 3-6 months|slaughter 82 kg.'),
        'iii':('Catch crop and nurse crop','crop-production','Grown between two main crops|sown after maincrop|fast growing crop (2-3 months)|prevents leaching|prevents soil erosion|high yield|break between grass and cereal|mainly fodder crops|e.g. turnips','Crop with 1 year life cycle|sown with perennial crop|annual crop is harvested leaving the perennial crop|reduces weeds|prevents soil erosion|used to establish perennial crop|e.g. grass sown with spring barley or peas'),
        'iv':('Zoonoses and zoospores','animal-diseases|plant-physiology','Disease(s)|can be transmitted from animal to human|spread by direct contact (insects eating flesh of infected animals, drinking contaminated water)|e.g. anthrax, brucellosis','Asexual reproductive cell|method of propagation in algae (bacteria, fungi)|no cell wall|flagellum for movement|mobile spore|e.g. Phytophthora infestans (potato blight)'),
    }
    for selected in combinations(pairs,3):
        rows=[]
        for k in selected:
            label,_,left,right=pairs[k];a,b=label.split(' and ')
            rows += [menu(left,[2,2],a+': two points.'),menu(right,[2,2],b+': two points.')]
        c=add('q8c-route-'+'-'.join(selected),'Q8(c) — '+', '.join(selected),'4-3-1','3-3|2-4|3-5',
            '|'.join(dict.fromkeys(t for k in selected for t in pairs[k][1].split('|'))),'agricultural-comparisons',
            'Highlight the main differences between the members of three of the following pairs: (i) Lungworm and ringworm. (ii) Breeding unit and finishing unit. (iii) Catch crop and nurse crop. (iv) Zoonoses and zoospores.',
            rows,[region(5,.165,.304)],[region(13,.436,.801)],'Practice choice: '+', '.join(pairs[k][0] for k in selected)+'.',
            selection={'kind':'closed','choose':3,'options':list(pairs),'route':list(selected)})
        c['additionalTopicIds']=['agsci-4-3-3','agsci-3-3-2']
    reasons=[
        ('a','The importance of pollination in plants.','Necessary for (sexual) reproduction of flowering plants|allows for genetic variation|production of seeds|fruits|which are food for animals|part of the food chain|biodiversity-maintains a balance in the ecosystem.','3-1','2-0','plant-physiology',(.436,.458),(.111,.184)),
        ('b','A greater demand for energy by animals kept outdoors over the winter.','Colder outdoors|wetter|animals use energy for heat (respiration)|greater energy demand to maintain critical temperature|animals move around and use energy|thermoregulation (maintain body temperature)','4-1','3-0','animal-physiology-digestive-system',(.466,.488),(.193,.261)),
        ('c','The occurrence of bare patches of ground in a recently sown cereal crop.','Seeding rate is too low|winter kill (frost etc.) may leave bare patches|disease|Rhizoctonia|damping-off|pests eating seed|not using certified seed|poor seedbed preparation|waterlogging.','3-3-1','2-3','crop-production',(.496,.518),(.255,.327)),
        ('d','The benefits arising from shelter-belts on exposed farms.','Protection for animals|protection for plants (crops)|reduce wind damage|increase soil temperature|air temperature|protection for buildings|habitat for wildlife|aesthetic purpose.','3-3-2','2-4','crop-production',(.526,.548),(.326,.391)),
        ('e','The locating of boars in dry sow houses.','Presence of boar stimulates sow’s oestrous cycle|used to detect sows in heat|can detect pheromones|used for double serving.','4-3-1','3-3','pigs',(.556,.574),(.392,.444)),
    ]
    for letter,label,pool,topic,old,atlas,py,sy in reasons:
        add('q9'+letter,f'Q9({letter})',topic,old,atlas,'scientific-explanation-'+letter,
            'Give a scientific explanation for: '+label,[menu(pool,[4]*3,'Three distinct points in a coherent explanation; synonymous descriptions earn only one award.')],
            [region(5,.406,.428),region(5,*py)],[region(14,.111,.195)] if letter=='a' else [region(14,.111,.195),region(14,*sy,.195,.96)])
    assert len(cards)==62
    return cards,tasks
