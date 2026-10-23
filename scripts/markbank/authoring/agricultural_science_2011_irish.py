"""2011 Higher Irish: source comparison and edition-specific task crops.

All eight paper and twelve scheme pages inspected. Coordinates come from the
Irish PDFs, including shared awards and the Irish C/c, F/f genetic cross.
"""
from agricultural_science_2010_parity import scan
from agricultural_science_2010_irish_crops import bind, regions

FILE = 'LC024ALP000IV.pdf'
HASHES = {'exampapers':'4dcb2bc61efb3cc1935b99a960d952d328755b9fcc1326cf234cdb8a7320d70f',
          'markingschemes':'ed9678a1028e2a0cc6ab4dfe47b87c2d4d8f6a163196194e9a2f44d23570e1d8'}
NOTES = [
    dict(questionN='1',questionRef='Q1(b)(ii)',paperPage=2,schemePage=4,
         note='The Irish scheme gives 2.5–3 for the dairy cow’s condition score at calving; the English scheme gives 2.5–3.5. Both give 2–3 at service. The original edition-specific ranges are preserved.'),
    dict(questionN='6',questionRef='Q6(b)',paperPage=4,schemePage=8,
         note='In the Irish scheme, the roman numerals beside Q6(b) do not align with the four question headings. Follow the named headings: soil type, rotation, fertiliser regime and end use, each worth 4 + 2. Under fertiliser regime, the Irish text says high protein for malting barley; the English scheme says low protein. The original Irish wording is shown unchanged.'),
    dict(questionN='7',questionRef='Q7(b)',paperPage=5,schemePage=8,
         note='This Irish edition uses C/c for tassel type and F/f for anther length. Its cross is CcFf × CcFf. The corresponding English edition uses H/h and L/l. The tasks have the same outcomes and tariffs; use the letters in the displayed edition.'),
]


def paper_review():
    cues = {
        'ddb9da0d53cb49db':('independent-task-selection','Q1 selects six of ten lettered parts; all are retained with (b), (g) and (h) split at their fixed roman-part awards.'),
        '1c2016923410dbd5':('independent-task-selection','Q8 selects two independently priced 24-mark parts; all are retained. The internal Q8(c) choice expands separately.'),
        'a041d276a945e12b':('independent-task-selection','Second match inside the same Q8 outer selection, not another choice pool.'),
    }
    extra = [
        (1,'SÉ CHEIST LE FREAGAIRT','exam-selection','Six whole examination questions, not combined practice responses.'),
        (3,'NÓ Rogha a Dó','closed','Both Q3 options are retained with distinct task addresses.'),
        (3,'haon dá cheann díobh seo a leanas','independent-task-selection','Q4 selects two separate 24-mark experiments; all four are available for practice.'),
        (3,'saotharlainne nó páirce','open','Laboratory or field are experiment settings, not a finite printed pool of named methods.'),
        (5,'Mínigh gach aon cheann de na téarmaí','required-headings','All three Q7(a) definitions are required, each worth four marks.'),
        (5,'thrí cinn ar bith de na péirí','closed','Q8(c) selects three of four comparison pairs: one 24-mark card crediting the best six members.'),
        (5,'cheithre cinn ar bith díobh seo a leanas','independent-task-selection','Q9 selects four independent twelve-mark explanations; all five are retained.'),
    ]
    observed,supplementary=scan(2011,FILE,HASHES,cues,extra)
    return dict(year=2011,level='higher',lang='iv',paperFileid=FILE,hashes=HASHES,
                wholePaperVisualReview='reviewed',schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1,9)),schemePagesInspected=list(range(1,13)),
                selectionDirectives=observed,supplementarySelections=supplementary,
                translationParity='All original pages visually inspected. The 67 base tasks (one card each) and all published mark boundaries match the English edition. Source-specific answer ranges, numbering and genetic symbols are retained.',
                sourceNotes=NOTES,
                remaining=['Independent Irish source census','Full application navigation review','Corpus-wide reconciliation'])


def crops():
    paper,scheme={},{}
    for keys,p,top,bottom in [
        ('q1a',2,.09,.127),('q1bi q1bii',2,.135,.172),('q1c',2,.18,.217),
        ('q1d',2,.225,.248),('q1e',2,.255,.278),('q1f',2,.285,.323),
        ('q1gi q1gii',2,.33,.383),('q1hi q1hii',2,.39,.428),
        ('q1i',2,.435,.458),('q1j',2,.465,.518),
        ('q2ai q2aii q2aiii q2aiv',2,.593,.662),('q2bi q2bii',2,.669,.707),('q2c',2,.714,.752),
        ('q3o1a',3,.063,.151),('q3o1b',3,.158,.196),('q3o1ci q3o1cii q3o1ciii',3,.203,.316),
        ('q3o2a',3,.356,.445),('q3o2bi q3o2bii',3,.452,.49),
        ('q3o2ci q3o2cii-advantages q3o2cii-disadvantages',3,.497,.565),
        ('q5ai q5aii q5aiii',4,.047,.101),('q5c',4,.585,.655),
        ('q6a',4,.695,.718),('q6bi q6bii q6biii q6biv',4,.725,.808),('q6c',4,.815,.869),
        ('q7ai q7aii q7aiii',5,.046,.131),
        ('q7b-cross q7bi q7bii q7biii',5,.138,.251),('q7c',5,.258,.327),
        ('q8a',5,.428,.467),('q8bi q8bii q8biii q8biv',5,.474,.557),
    ]:bind(paper,keys,p,top,bottom)
    for key in ['q5bi','q5bii','q5biii']:
        paper[key]=regions(4,.107,.425)+regions(4,.45,.564)
    for key,top,bottom in [('q4a',.654,.677),('q4b',.684,.707),('q4c',.714,.737),('q4d',.744,.782)]:
        paper[key]=regions(3,.623,.647)+regions(3,top,bottom)
    for key,top,bottom in [('q9a',.717,.74),('q9b',.747,.77),('q9c',.777,.8),('q9d',.807,.83),('q9e',.837,.891)]:
        paper[key]=regions(5,.686,.71)+regions(5,top,bottom)
    for keys,p,top,bottom in [
        ('q1a',4,.112,.206),('q1bi q1bii',4,.207,.237),('q1c',4,.238,.313),
        ('q1d',4,.314,.343),('q1e',4,.344,.464),('q1f',4,.465,.51),
        ('q1gi',4,.51,.54),('q1gii',4,.541,.587),('q1hi q1hii',4,.587,.663),
        ('q1i',4,.663,.694),('q1j',4,.694,.787),
        ('q2ai',5,.086,.102),('q2aii',5,.102,.148),('q2aiii',5,.148,.194),('q2aiv',5,.194,.24),
        ('q2bi',5,.239,.3),('q2bii',5,.3,.361),('q2c',5,.361,.439),
        ('q3o1a',6,.084,.224),('q3o1b',6,.223,.3),('q3o1ci',6,.299,.36),
        ('q3o1cii',6,.36,.421),('q3o1ciii',6,.42,.468),('q3o2a',6,.479,.558),
        ('q3o2bi q3o2bii',6,.558,.603),('q3o2ci q3o2cii-advantages q3o2cii-disadvantages',6,.603,.727),
        ('q4a',7,.04,.148),('q4b',7,.148,.284),('q4c',7,.284,.36),('q4d',7,.36,.468),
        ('q5ai',7,.509,.527),('q5aii',7,.526,.558),('q5aiii',7,.557,.618),
        ('q5bi q5bii q5biii',7,.618,.694),('q5c',7,.694,.728),
        ('q6a',8,.084,.148),('q6bi q6bii q6biii q6biv',8,.148,.374),('q6c',8,.374,.422),
        ('q7ai q7aii q7aiii',8,.447,.556),('q7b-cross',8,.556,.677),
        ('q7bi q7bii q7biii',8,.556,.758),('q7c',8,.766,.802),
        ('q8a',9,.084,.182),('q8bi',9,.192,.255),('q8bii',9,.255,.285),
        ('q8biii',9,.285,.331),('q8biv',9,.331,.485),
        ('q9a',10,.097,.178),('q9b',10,.188,.282),('q9c',10,.282,.343),
        ('q9d',10,.342,.434),('q9e',10,.433,.511),
    ]:bind(scheme,keys,p,top,bottom)
    paper['q8c']=regions(5,.564,.662)
    scheme['q8c']=regions(9,.495,.895)
    for key in ['q4b','q4c','q4d']:
        scheme[key].append({'p':7,'r':[.77,.04,.87,.058]})
    for key in ['q9b','q9c','q9d','q9e']:
        scheme[key].append({'p':10,'r':[.75,.097,.86,.115]})
    return paper,scheme


def attach_sources(tasks,review):
    paper,scheme=crops()
    selected=[t for t in tasks if t['cardIds'][0].startswith('agsci-2011-hl-')]
    prefix='agsci-2011-hl-'
    keys={t['cardIds'][0].removeprefix(prefix) for t in selected}
    assert keys==set(paper)==set(scheme) and len(keys)==67, (keys-set(paper),keys-set(scheme))
    for task in selected:
        key=task['cardIds'][0].removeprefix(prefix)
        ref=task['questionRef'].split(' Q',1)[1]
        label=('Ceist '+ref).replace('Option One','Rogha a hAon').replace('Option Two','Rogha a Dó').replace('cross','crosáil').replace('disadvantages','míbhuntáistí').replace('advantages','buntáistí')
        source=dict(lang='iv',paperFileid=FILE,label=label,paperRegions=paper[key],schemeRegions=scheme[key],marksPerRoute=task['marksPerRoute'])
        notes=[n['note'] for n in NOTES if ref.startswith(n['questionRef'].removeprefix('Q'))]
        if task.get('schemeNote'):notes.append(task['schemeNote'])
        if notes:source['schemeNote']='\n\n'.join(notes)
        task['translatedSources']=[source]
    freeze=lambda x:len({tuple((r['p'],tuple(r['r'])) for r in c) for c in x.values()})
    assert (len(keys),freeze(paper),freeze(scheme))==(67,40,53)
    for mapping,pages in [(paper,review['paperPagesInspected']),(scheme,review['schemePagesInspected'])]:
        for crop in mapping.values():
            for r in crop:
                left,top,right,bottom=r['r']
                assert r['p'] in pages and 0<=left<right<=1 and 0<=top<bottom<=1
    review['practiceTaskCropReview']=dict(status='reviewed',taskBindings=len(keys),distinctPaperCropSets=freeze(paper),distinctSchemeCropSets=freeze(scheme),
        evidence='All distinct paper/scheme pairs rendered and visually inspected. Shared tariff columns, heart labels and genetic symbols retained. Final heart and ratio crop corrections re-rendered and inspected.')
