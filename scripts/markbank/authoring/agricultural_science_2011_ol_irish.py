"""2011 Ordinary Irish: complete source comparison and task-specific crops.

All twelve paper and sixteen scheme pages inspected. The 81 task boundaries,
pooled Section One scales and genetic asterisks match the English edition.
Coordinates and source wording are taken from the Irish PDFs independently.
"""
from agricultural_science_2010_parity import scan
from agricultural_science_2010_irish_crops import bind, regions
from agricultural_science_2011_ol import SCIENTIFIC

FILE = 'LC024GLP000IV.pdf'
HASHES = {'exampapers':'0d32fbdb30e5d13ca15b792d48f6cfd9744869bc0d26099188548ebc77e51377',
          'markingschemes':'79f95dcf8bcf49c50251496711d020ebcfd4c40bfba83720089e27f28258a837'}
NOTES = [dict(questionN={'q7c':'7','q9di':'9','q10biii':'10'}[key],
              questionRef={'q7c':'Q7(c)','q9di':'Q9(d)(i)','q10biii':'Q10(b)(iii)'}[key],
              note=note,source=url) for key,(url,note) in SCIENTIFIC.items()]


def paper_review():
    observed,supplementary=scan(2011,FILE,HASHES,{
        'e4905f4e8326b2f8':('exam-selection','Section One selects six separately priced questions; all seven are retained.'),
        'b8652464d31bdfdf':('exam-selection','Section Two selects three separately priced questions; all six are retained.'),
        'a7b0bf09d83d2b21':('independent-task-selection','Q12 selects two separately priced 30-mark parts. Retain all thirteen published internal tasks, not pairings of unrelated responses.'),
    },[
        (1,'Ní mór sé cheist a fhreagairt.','exam-selection','Cover repeats Section One selection.'),
        (1,'Ní mór trí cheist a fhreagairt.','exam-selection','Cover repeats Section Two selection.'),
        (7,'meaitseáil na focail ón liosta','answer-identification','Q10(a) requires six matches in a single dependent paragraph. Word permutations are not optional answer routes.'),
        (7,'thrí bhealach ar bith','open','Q10(c) asks for three weathering processes without a finite printed pool.'),
        (8,'gránach nó barr fréimhe','open','Q11(c) permits open crop categories. Barley and potatoes are scheme examples, not a printed closed pool.'),
        (8,'faoi na ceannteidil seo a leanas','required-headings','Q11(c) requires all headings. Date and method split at their separately printed awards.'),
        (8,'feithide ainmnithe','open','Q11(b) permits a suitable insect; complete and incomplete metamorphosis are scheme menus.'),
        (8,'einsíme díleáiche ainmnithe','open','Q12(a) permits an appropriate digestive enzyme and matching experiment.'),
        (8,'comhpháirt ainmnithe amháin','open','Q12(c)(ii) permits a suitable milk component and matching investigation.'),
    ])
    return dict(year=2011,level='ordinary',lang='iv',paperFileid=FILE,hashes=HASHES,
                wholePaperVisualReview='reviewed',schemeBoundaryReview='reviewed',
                paperPagesInspected=list(range(1,13)),schemePagesInspected=list(range(1,17)),
                selectionDirectives=observed,supplementarySelections=supplementary,
                translationParity='All original pages visually inspected. All 81 task boundaries, marks, open choices, diagrams, pooled first-correct scales and genetic asterisks match the English tasks. Original Irish answer examples and wording are retained in the displayed source.',
                sourceNotes=NOTES,
                remaining=['Full application navigation review','Corpus-wide reconciliation'])


def crops():
    paper,scheme={},{}
    for keys,p,top,bottom in [
        ('q1',2,.28,.908),('q2',3,.042,.626),('q3',3,.65,.946),('q4',4,.042,.466),
        ('q5-bullock q5-gilt q5-draft-ewe q5-broiler q5-suckler-calf',4,.51,.796),
        ('q6a q6b q6c q6d',5,.042,.587),
        ('q7a',5,.643,.706),('q7b',5,.726,.814),('q7c',5,.838,.865),
        ('q8ai q8aii q8aiii q8aiv q8av',6,.2,.35),
        ('q8bi q8bii q8biii q8biv q8bv',6,.365,.51),
        ('q9ai q9aii',6,.554,.613),('q9b-ley q9b-establishment q9b-heading-out',6,.624,.696),
        ('q9ci q9cii',6,.706,.825),('q9di q9dii q9diii',6,.837,.907),
        ('q10a',7,.042,.277),('q10bi q10bii q10biii',7,.294,.382),('q10c',7,.39,.443),
        ('q10d-a q10d-b q10d-c',7,.452,.955),
        ('q11ai q11aii q11aiii',8,.075,.159),('q11b',8,.171,.197),
        ('q11ci q11cii-date q11cii-method q11ciii q11civ q11cv-method q11cv-time q11cvi',8,.204,.323),
        ('q12a-system q12a-enzyme',8,.45,.506),
        ('q12bi q12bii q12biii q12biv q12bv',8,.517,.62),
        ('q12ci q12cii q12ciii',8,.632,.734),('q12di q12dii q12diii',8,.744,.85),
        ('q13ai q13aii q13aiii',9,.041,.097),('q13b-f1',9,.104,.327),
        ('q13di q13dii q13diii q13div',9,.579,.911),
    ]:bind(paper,keys,p,top,bottom)
    paper['q13b-f2']=regions(9,.104,.211)+regions(9,.352,.457)
    for key in ['q13ci','q13cii','q13ciii']:
        paper[key]=regions(9,.104,.211)+regions(9,.467,.571)
    for keys,p,top,bottom in [
        ('q1',5,.2,.396),('q2',5,.463,.725),('q3',6,.084,.329),('q4',6,.38,.747),
        ('q5-bullock q5-gilt q5-draft-ewe q5-broiler q5-suckler-calf',7,.084,.301),
        ('q6a',7,.38,.417),('q6b',7,.425,.497),('q6c',7,.507,.527),('q6d',7,.535,.614),
        ('q7a',7,.685,.734),('q7b',7,.744,.782),('q7c',7,.792,.816),
        ('q8ai',8,.171,.224),('q8aii',8,.234,.287),('q8aiii',8,.297,.359),
        ('q8aiv',8,.359,.413),('q8av',8,.422,.495),
        ('q8bi',8,.534,.585),('q8bii',8,.598,.65),('q8biii',8,.662,.714),
        ('q8biv',8,.725,.776),('q8bv',8,.788,.826),
        ('q9ai',9,.141,.178),('q9aii',9,.188,.225),('q9b-ley',9,.293,.345),
        ('q9b-establishment',9,.356,.407),('q9b-heading-out',9,.419,.471),
        ('q9ci q9cii',9,.504,.574),
        ('q9di',9,.652,.705),('q9dii',9,.716,.737),('q9diii',9,.745,.782),
        ('q10a',10,.11,.247),('q10c',10,.72,.815),
        ('q10d-a q10d-b q10d-c',10,.835,.91),
        ('q11ai q11aii',11,.11,.197),('q11aiii',11,.202,.253),
        ('q11b',11,.263,.447),
        ('q12a-system',13,.114,.133),('q12a-enzyme',13,.145,.222),
        ('q12bi',13,.231,.271),('q12bii',13,.28,.314),('q12biii',13,.326,.387),
        ('q12biv',13,.398,.431),('q12bv',13,.442,.522),
        ('q12ci',13,.535,.583),('q12cii',13,.594,.643),('q12ciii',13,.655,.734),
        ('q12di',13,.745,.778),('q12dii',13,.79,.838),('q12diii',13,.853,.872),
        ('q13ai',14,.114,.15),('q13aii',14,.157,.21),('q13aiii',14,.218,.251),
        ('q13b-f1',14,.279,.372),('q13b-f2',14,.382,.506),
        ('q13ci q13cii q13ciii',14,.533,.662),('q13di q13dii q13diii q13div',14,.686,.779),
    ]:bind(scheme,keys,p,top,bottom)
    for key,top,bottom in [('q10bi',.326,.393),('q10bii',.389,.554),('q10biii',.546,.696)]:
        scheme[key]=regions(10,.249,.336)+regions(10,top,bottom)
    for key,br,pr in [
        ('q11ci',(.506,.539),(.162,.221)),
        ('q11cii-date',(.548,.62),(.248,.315)),
        ('q11cii-method',(.548,.62),(.248,.315)),
        ('q11ciii',(.628,.696),(.337,.379)),
        ('q11civ',(.704,.755),(.4,.434)),
        ('q11cv-method',(.759,.847),(.458,.575)),
        ('q11cv-time',(.759,.847),(.458,.575)),
        ('q11cvi',(.854,.889),(.585,.616)),
    ]:
        scheme[key]=regions(11,.462,.496)+regions(11,*br)+regions(12,.131,.147)+regions(12,*pr)
    return paper,scheme


def attach_sources(tasks,review):
    paper,scheme=crops()
    prefix='agsci-2011-ol-'
    selected=[t for t in tasks if t['cardIds'][0].startswith(prefix)]
    keys={t['cardIds'][0].removeprefix(prefix) for t in selected}
    assert keys==set(paper)==set(scheme) and len(keys)==81,(keys-set(paper),keys-set(scheme))
    suffixes={'bullock':'Bullán','gilt':'Céis','draft ewe':'Caora dhealaithe','broiler':'Sicín grísce','suckler calf':'Lao diúil',
              'ley':'bán','establishment':'bunú','heading out':'ag teacht i gcraobh',
              'digestive system':'córas díleá','enzyme experiment':'turgnamh einsíme',
              'soil A':'ithir A','soil B':'ithir B','soil C':'ithir C',' — date':' — dáta',' — method':' — modh',' — time':' — am'}
    for task in selected:
        key=task['cardIds'][0].removeprefix(prefix)
        ref=task['questionRef'].split(' Q',1)[1]
        label='Ceist '+ref
        for english,irish in suffixes.items():label=label.replace(english,irish)
        source=dict(lang='iv',paperFileid=FILE,label=label,paperRegions=paper[key],schemeRegions=scheme[key],marksPerRoute=task['marksPerRoute'])
        if key in SCIENTIFIC:source['schemeNote']=SCIENTIFIC[key][1]
        task['translatedSources']=[source]
    freeze=lambda m:len({tuple((r['p'],tuple(r['r'])) for r in c) for c in m.values()})
    for mapping,pages in [(paper,review['paperPagesInspected']),(scheme,review['schemePagesInspected'])]:
        for crop in mapping.values():
            for r in crop:
                left,top,right,bottom=r['r']
                assert r['p'] in pages and 0<=left<right<=1 and 0<=top<bottom<=1
    review['practiceTaskCropReview']=dict(status='reviewed',taskBindings=len(keys),distinctPaperCropSets=freeze(paper),distinctSchemeCropSets=freeze(scheme),evidence='All 66 distinct paper/scheme pairs rendered and visually inspected. Missing blight wording, cropped answer lines and adjacent tariff fragments corrected; all changed crop pairs re-rendered and inspected. Original diagrams, full genetic stems and crop-name headings retained.')
