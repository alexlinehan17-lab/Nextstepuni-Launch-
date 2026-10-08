#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2011 written pages1–16, aural pages1–8 and scheme pages1–20 visually reviewed on 2026-10-07.
Source hashes, selection decisions and task identities travel with the output.
The older Foundation papers remain pending in irish-archive-inventory.json.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001BLP100IV'
AURAL_FILE = 'LC001BLPA00IV'
SCHEME_FILE = 'LC001BLP000EV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2011-authored.json'

def spatial_text(page):
    # The 2011 PDF repeats the last glyph at fragment boundaries. Deduplicate
    # only the same glyph at the same physical origin, never repeated letters.
    rows=[]
    for b in page.get_text('rawdict')['blocks']:
        for line in b.get('lines',[]):
            for span in line['spans']:
                for char in span['chars']:
                    x,y=char['origin'];row=next((r for r in rows if abs(r[0]-y)<0.3),None)
                    if row is None:row=[y,[]];rows.append(row)
                    if not any(c['c']==char['c'] and abs(c['origin'][0]-x)<0.12 for c in row[1]):row[1].append(char)
    lines=[]
    for _,chars in sorted(rows,key=lambda r:r[0]):
        chars.sort(key=lambda c:c['origin'][0]);out='';last=None
        for c in chars:
            if last and c['bbox'][0]-last['bbox'][2]>1.8 and not(out.endswith(' ') or c['c']==' '):out+=' '
            out+=c['c'];last=c
        lines.append(re.sub(r'\s+',' ',out).strip())
    return '\n'.join(lines)

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]|dó/di|Cuir ciorcal|dhá thagairt', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2011-source-review.json'

def scheme_page_text(page):
    # Visually verified Symbol-font bullet and arrow; original PDF unchanged.
    return page.get_text().translate({0xf0b7: "•", 0xf0ae: "→", 0xf0b8: "÷"})

def selection_decisions(papers, spatial=False):
    field='spatialSelectionDecisions' if spatial else 'selectionDecisions'
    decisions = json.loads(SOURCE_REVIEW.read_text())[field]
    expected={(d['paperFileid'],d['page'],d['raw']) for d in decisions}
    found={(name,i,clean(line)) for name,paper in papers.items() for i,page in enumerate(paper,1)
           for line in (spatial_text(page) if spatial else page.get_text()).splitlines() if DIRECTIVE.search(clean(line))}
    assert found==expected, ('Unclassified/stale selection directives',field,found-expected,expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2011/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2011/{SCHEME_FILE}.pdf'
    aural_path = ROOT / f'paper-trail-corpus/exampapers/2011/{AURAL_FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '8cbf542bdf3937dbe1121737d750a11b7e0ba23c5812e11ea27102b2b24a23ca', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '9d661961f601757d5de357b5d53485b16d92ebfa19a01409ea722e0b1c22c37c', 'Scheme changed: repeat visual review'
    assert hashlib.sha256(aural_path.read_bytes()).hexdigest() == '2d4997a9c4399b63edf4ffd152c64700151b6beba165b1b5f5f27cb843ef35c6', 'Aural paper changed: repeat review'
    aural_paper = fitz.open(aural_path)
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(spatial_text(p)) for p in paper]
    aural_texts = [clean(spatial_text(p)) for p in aural_paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2011-fl-{key.lower()}', year=2011, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2011 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=AURAL_FILE if section=='1' else FILE, schemeFileid=SCHEME_FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2011 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag Breandán?', None, 'Leictreoir = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cá háit a bhfuil Breandán ina chónaí faoi láthair?',
  'Droichead Átha | Dún Dealgan | Faoin tuath',
  'Faoin tuath'),
 ('2a', 2, 7, 'Cá bhfuil Deirdre ag obair anois?', None, 'In oifig thaistil = an ceathrú pictiúr'),
 ('2b',
  2,
  7,
  'Cén áit a rachaidh Deirdre an bhliain seo chugainn?',
  'An Eoraip | An tSín | Meiriceá',
  'An tSín'),
 ('3a', 3, 7, 'Cén spórt nach maith le hEoin?', None, 'Galf = an dara pictiúr'),
 ('3b',
  3,
  7,
  'Cé mhéad oíche a bhíonn Eoin ag snámh gach seachtain?',
  'Trí oíche | Cúig oíche | Seacht n-oíche',
  'Trí oíche'),
 ('4', 3, 7, 'Cá bhfuil an bhean ag dul?', None, 'Siopa troscáin = an ceathrú pictiúr'),
 ('5',
  3,
  7,
  'Cá bhfuil an banc suite? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbun ar clé (tic nó saighead)'),
 ('6a',
  4,
  8,
  'Cén sórt aimsire a bheidh ann i Loch Garman Dé Sathairn?',
  None,
  'Grianmhar = an ceathrú pictiúr'),
 ('6b', 4, 8, 'Conas mar a bheidh an aimsir Dé Domhnaigh?', 'Tirim | Gaofar | Te', 'Tirim'),
 ('7a', 4, 8, 'Cad a bheidh ar siúl Dé hAoine i halla na scoile?', None, 'Dráma = an chéad phictiúr'),
 ('7b',
  4,
  8,
  'Cén t-am a thosóidh an dráma?',
  'A cúig a chlog | A seacht a chlog | A hocht a chlog',
  'A hocht a chlog'),
 ('8a', 5, 8, 'Cad a bheidh ar siúl i halla na scoile Dé Sathairn?', None, 'Dioscó = an dara pictiúr'),
 ('8b',
  5,
  8,
  'Cad a bheidh ar díol laistigh den halla?',
  'Guma coganta | Sólaistí agus deochanna | Ticéid',
  'Sólaistí agus deochanna'),
 ('9a', 5, 8, 'Cén spórt a imríonn Katie Taylor?', None, 'Dornálaíocht = an chéad phictiúr'),
 ('9b', 5, 8, 'Cén bhliain a bunaíodh an Club Óige i gCromghlinn?', '1950 | 1961 | 2011', '1961'),
 ('10a', 6, 10, 'Cad a bhí ag Maidhc ar a ghlúin?', 'Bindealán | Clogad | Plástar', 'Bindealán'),
 ('10b',
  6,
  10,
  'Cé a rith amach ar an mbóthar taobh amuigh den siopa?',
  'Siopadóir | Cailín óg | Buachaill óg',
  'Buachaill óg'),
 ('11a', 6, 10, 'Cé mhéad airgid a fuair Bríd óna hAintín?', '€200 | €300 | €500', '€200'),
 ('11b',
  6,
  10,
  'Cad is féidir a fháil go héasca ón gComhar Creidmheasa?',
  'Seic | Iasacht airgid | Iasacht leabhair',
  'Iasacht airgid'),
 ('12a',
  6,
  10,
  'Cén cluiche a d’imir Oisín ar an Domhnach?',
  'Cluiche iománaíochta | Cluiche rugbaí | Cluiche sacair',
  'Cluiche Sacair'),
 ('12b',
  6,
  10,
  'Cé a fuair an cárta dearg ón réiteoir?',
  'An cúl báire | An lántosaí | Oisín',
  'An cúl báire')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2011/LC001BLP017IV.mp3'
    for n,page,marks,prompt,options,answer in aural:
        comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
        assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(aural_texts[page-1])), (n,prompt)
        for option in (options or '').split(' | '):
            assert comparable(option) in comparable(aural_texts[page-1]), (n,option)
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$',r'(\1)',n)
        card = add('A-'+n,'1',ref,re.sub(r'^(\d+)([ab]?)$', lambda m: m[1]+'. '+('('+m[2]+') ' if m[2] else ''), n)+prompt+
            ('\n\n'+options.replace(' | ','\n') if options else ''),
            'irish-1-3',['aural'],[page],[3],
            [criterion('answer','Freagra',marks,[answer],True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio',label=ref,
                title='Gaeilge Bonnleibhéal 2011 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Feighlí Linbh ag teastáil\nIs gá a bheith ceanúil ar pháistí\nFón: Úna 089 22 21 22',
 'Ná Snámh Anseo!\nUisce Contúirteach',
 'Sladmhargadh\nEarraí Leictreonacha\nar leathphraghas',
 'Caith Crios Sábhála\ni gcónaí\nsa charr seo',
 'Seomra Ealaíne\nLuath-oscailt do dhaltaí\nDéardaoin 7.50 a.m.',
 'Club Dreapadóireachta\nTuras speisialta go Mont Blanc\nLúnasa 2011',
 'Tiománaí Leoraí ag teastáil\nCeadúnas glan riachtanach\nFón 0501 89654',
 'Óstán Mhic Dhiarmada\nRátaí Speisialta\nSeomraí ar €57',
 'Amharclann na Mainistreach\n‘An Giall’\n8.p.m. Dé Luain-Dé Sathairn',
 'Siopa na bPeataí\nÉisc órga, coiníní agus éin\n‘Ceannaigh peata do do pháiste’']
    for i,(sign,answer) in enumerate(zip(signs,'EJAHDIFCGB'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[2],[4],
            [criterion('answer','Litir cheart',4,[answer],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (3,
        'letterReading',
        [('Cén dáta ar sheol Sinéad a litir?', '25 Márta | 29 Márta | 19 Aibreán', '25 Márta'),
         ('Cén t-ábhar ina bhfuair Sinéad Grád A san Ardteistiméireacht?',
          'Gnó | Matamaitic | Innealtóireacht',
          'Innealtóireacht'),
         ('Cá bhfuil Sinéad ag staidéar faoi láthair?',
          'Sa mheánscoil | San Institiúid Teicneolaíochta | Le Bord Gáis',
          'San Institiúid Teicneolaíochta'),
         ('Cén obair a theastaíonn ó Shinéad le Bord Gáis an samhradh seo chugainn?',
          'Obair mar innealtóir | Obair theicneolaíochta | Taithí oibre sa Chuntasaíocht',
          'Taithí oibre sa Chuntasaíocht'),
         ('Cad is gá do Shinéad a bhreith léi go dtí an t-agallamh?',
          'An litir seo | A teastas scrúduithe | A teastas breithe',
          'A teastas breithe')]),
 '2B': (4,
        'brochure',
        [('Cén áit a bhfuil an fheirm seo?',
          'Na Blascaodaí | Gaeltacht Chiarraí | Sa chathair',
          'Gaeltacht Chiarraí'),
         ('Cad atá os comhair an tí?', 'Clós feirme | Radhairc áille | Trá ghainmheach', 'Ranganna Céilí'),
         ('Cá bhfuil cúinne na bpeataí?',
          'Ar chúl an tí | In aice na farraige | Os comhair an tí',
          'Ar chúl an tí'),
         ('Cad is féidir a dhéanamh i ngach seomra?',
          'Bricfeasta | Tae nó caife | Seisiún ceoil',
          'Tae nó caife'),
         ('Cé a bhailíonn isteach sa chistin go minic?',
          'Ceoltóirí na háite | Iascairí | Na haíonna',
          'Ceoltóirí na háite')]),
 '2C': (5,
        'news',
        [('Cén aois atá Liam Mac Donnagáin?', '57 | 75 | 83', '75'),
         ('Cé a bhí sa veain a stop lasmuigh?', 'Comharsa | Gadaí | Iníon Liam', 'Gadaí'),
         ('Cá raibh an t-airgead?', 'Sa chistin | Sa seomra folctha | Sa seomra suite', 'Sa chistin'),
         ('Cé a chuir fios ar na Gardaí?', 'Liam | A iníon Áine | A chomharsa Ned', 'A iníon Áine'),
         ('Cén áit ar cúisíodh an gadaí?',
          'Sa teach | I stáisiún na nGardaí | Os comhair na cúirte',
          'Os comhair na cúirte')]),
 '3A': (6,
        'news',
        [('Cá mbíonn Dáithí Ó Sé go minic?',
          'Ar an raidió | Ar an stáitse | Ar an teilifís',
          'Ar an teilifís'),
         ('Cén post a bhí ag Dáithí Ó Sé nuair a bhí sé ina dhéagóir?',
          None,
          'D’oibrigh sé i siopa búistéara'),
         ('Cén bhliain a rinne Dáithí an clár faoi ‘Route 66’?', '1999 | 2006 | 2008', '2006'),
         ('Cén post a bhí ag Dáithí ag Féile Rós Thrá Lí sa bhliain 2010?',
          'Doirseoir | Fáilteoir | Fear an tí',
          'Fear a’tí'),
         ('Cé atá in éad le Dáithí Ó Sé?', 'Mná na hÉireann | Fir na hÉireann | TG4', 'Fir na hÉireann')]),
 '3B': (7,
        'extract',
        [('Cén saghas ceoil atá i gceist sa ghiota seo?',
          'Ceol clasaiceach | Ceol tíre | Ceol traidisiúnta',
          'Ceol traidisiúnta'),
         ('Cá fhad a leanann Scoil Samhraidh Willie Clancy?', 'Bliain | Mí | Seachtain', 'Seachtain'),
         ('Cén uirlis cheoil lenar thit Willie Clancy i ngrá?',
          'An fhidil | An bosca ceoil | An phíb uilleann',
          'An phíb uilleann'),
         ('Cad a rinne Willie sa bhliain 1957?', None, 'D’fhill Willie ar Chontae an Chláir'),
         ('Cé a bhunaigh an Scoil Samhraidh?',
          'Cairde Willie | Seamus Ennis | Willie Clancy',
          'Cairde Willie')]),
 '3C': (8,
        'poem',
        [('Cad a fuair an préachán tráth?', 'Píosa aráin | Píosa cáise | Píosa feola', 'Píosa cáise'),
         ('Cén fáth a raibh ocras ar an sionnach?', None, 'Níor ith sé dada feadh dhá lá'),
         ('Conas a bhí an aimsir an lá sin?',
          'Bhí sé ag cur | Bhí sé go breá | Bhí sé fuar',
          'Bhí sé go breá'),
         ('Cén moladh a thug an sionnach don phréachán?',
          'Fan i do thost | Is binn do ghlór | Tá tú órga',
          'Is binn do ghlór'),
         ('Cén fáth ar oscail an préachán a bhéal?',
          'Chun amhrán a rá | Chun bia a ithe | Chun eitilt in airde',
          'Chun amhrán a rá')])}
    reading_cards = {}
    for slot,(page,exam_topic,rows) in reading.items():
        reading_cards[slot] = []
        for i,(prompt,options,answer) in enumerate(rows,1):
            # Fail on stale question text; normalize only punctuation differences
            # between PDF fonts and the accessible prompt.
            comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
            assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (slot,i,prompt)
            for option in (options or '').split(' | '):
                assert comparable(option) in comparable(texts[page-1]), (slot,i,option)
            for accepted in answer.split(' / '):
                assert comparable(accepted) in comparable(scheme[3 if slot[0]=='2' else 4].get_text()), (slot,i,accepted)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],([4] if slot[0]=='2' else [5,6] if (slot,i) in [('3A',2),('3B',4),('3C',2)] else [5]),
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            if slot=='2B' and i==2:
                card['sourceDiscrepancyNotice']='Nóta foinse: deir an téacs “trá ghainmheach”, ach tá “Ranganna Céilí” sa scéim do 2(b)(2). Féach ar an dá fhoinse.'
                card['criteria'][0]['label']='Freagra · neamhréir fhoilsithe'
                card['criteria'][0]['guidance']=[
                    'SEC answer key: Ranganna Céilí — 5 mharc.',
                    'Published source discrepancy: paper PDF 4 asks what is opposite the house. Its passage says trá ghainmheach and that is one printed option; Ranganna Céilí is absent from the passage and options. Scheme PDF 4 nevertheless prints Ranganna Céilí. Both originals are preserved. The scheme does not explicitly award the passage-supported answer; compare both sources, without treating this key as an uncontested reading or claiming an SEC correction.'
                ]
                card['markingGuideNote']=card['criteria'][0]['guidance'][1]
            if (slot,i) in [('3A',2),('3B',4),('3C',2)]:
                card['criteria'][0]['permittedMarks']=[0,2,4,6]
                details=clean(scheme_page_text(scheme[5]))
                heading={'3A':'Ceist 3 (a) Mír 2','3B':'Ceist 3 (b) Mír 4','3C':'Ceist 3 (c) Mír 2'}
                next_heading={'3A':'Ceist 3 (b) Mír 4','3B':'Ceist 3 (c) Mír 2','3C':None}
                details=details.split(heading[slot],1)[1]
                if next_heading[slot]:details=details.split(next_heading[slot],1)[0]
                card['criteria'][0]['guidance'] += [details,
                    'Start from the accepted 6-mark answer. Extra sentence −2; two extra sentences −4; three extra sentences −6. Enter the final mark for this part only.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2011 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2011 FL ','')+'\n'+c['questionText'] for c in members),
            topics[0],list(dict.fromkeys(t for c in members for t in c['examTopicKeys'])),
            sorted(set(p for c in members for p in c['sourceMaterial']['pages'])),
            sorted(set(p for c in members for p in c['schemePages'])),criteria,
            [r for c in members for r in c['taskRequirements']],
            'This is one permitted printed selection. Each selected response retains its own SEC marking criteria; alternative routes are not added to this tariff.',
            additionalTopicIds=topics[1:], memberCardIds=[c['id'] for c in members])
        return result

    for n in '23':
        for a,b in itertools.combinations('ABC',2):
            combine(f'R-{n}-{a}{b}',f'Léamhthuiscint · Ceist {n}({a.lower()}) + ({b.lower()})',
                reading_cards[n+a]+reading_cards[n+b],
                f'Ceist {n} Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.')

    def language(marks):
        return criterion('gaeilge','Cruinneas Gaeilge',marks,[
            'Dul na Gaeilge: struchtúir na Gaeilge agus cruinneas gramadaí. Foclóir: cruinneas sa stór focal. Litriú: moltar gan an iomarca béime a chur ar an ngné seo ag an leibhéal seo. Ná glac le Béarla.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'Reasonable-accommodation guidance is on scheme PDF 18; no four-point language-conversion table is printed in 2011.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'Gaeilge\s+ATBL 2011\s+\d+', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    n8,n9,n10=scheme_guidance(8,10)
    notice=add('W-4A','3','Scríobh · Ceist 4(a) · Fógra',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis na pictiúir thuas.\n\n'
        'Cén rud? Cén áit?\nCén oíche? Dáta? Am? Cén cead isteach?\nCé a bheidh mar Fhear an Tí?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[10],[8,9,10],[
            criterion('leagan','Leagan Amach',1,[n8.split('Leagan amach:',1)[1]]),
            criterion('pictiur1','Pictiúr 1 · rud 3 + áit 3',6,[n9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2 · oíche 3 + dáta 2 + am 2 + cead 2',9,[n9.split('Pictiúr 2',1)[1],n10.split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3 · Fear an Tí',3,[n10.split('Pictiúr 3',1)[1].split('Pic. 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4 · an t-airgead',3,[n10.split('Pic. 4',1)[1].split('Léiriú na marcanna',1)[0]]),language(8)],
        ['Scríobh fógra bunaithe ar gach pictiúr agus ar na treoracha.'],
        'Whole 30-mark notice: layout 1, pictures 6+9+3+3, shared language 8. Scheme PDF 8 general inappropriate-tense deduction −1 applies to the affected point. Keep the 2011 activity, venue, day, date, time, fee, male-host and children’s-hospital rules; later 40-mark notice tariffs do not apply.')
    i11,i12=scheme_guidance(11,12)
    invitation=add('W-4B','3','Scríobh · Ceist 4(b) · Cuireadh',
        'Féach ar na pictiúir thíos.\n\nIs tusa an duine sna pictiúir seo. Scríobh CUIREADH chuig Úna ag insint di:\n\n'
        '- Cad a bheidh ar siúl. Cén áit. Cén lá. Cén dáta. Cén t-am. Cé mhéad ar thicéad. — Pictiúr 1\n'
        '- Go bhfuil a fhios agat gur maith le hÚna an rugbaí. — Pictiúr 2\n'
        '- Gur mhaith leat go rachadh Úna ann leat. — Pictiúr 3\n'
        '- Cá rachaidh sibh ar an mbealach abhaile. — Pictiúr 4',
        'irish-9-3',['notice','pictures'],[11],[11,12],[
            criterion('beannu','Beannú',2,[i11.split('Beannú oiriúnach A Úna',1)[1].split('Iarracht ar chuireadh:',1)[0]]),
            criterion('cuireadh','Iarracht ar chuireadh',1,[i11.split('Iarracht ar chuireadh:',1)[1].split('Síniú:',1)[0]]),
            criterion('siniu','Síniú',1,[i11.split('Síniú:',1)[1].split('Na Treoracha:',1)[0]]),
            criterion('pictiur1','Pictiúr 1 · sé phointe × 2',12,[i11.split('Na Treoracha:',1)[1],i12.split('Pictiúr 2',1)[0],
                'Published day-rule conflict: the opening sentence lists inné among examples for 2 marks, but the same day block explicitly lists Inné at 0 marks. Both statements are preserved; no SEC resolution is supplied. Compare the original scheme when reviewing an answer using inné.']),
            criterion('pictiur2','Pictiúr 2 · is maith leat an rugbaí',2,[i12.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3 · an cuireadh',2,[i12.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4 · ar an mbealach abhaile',2,[i12.split('Pictiúr 4',1)[1]]),language(8)],
        ['Scríobh chuig Úna faoin gcluiche rugbaí; sé shonra i bpictiúr 1 agus na trí threoir eile.'],
        'Whole 30-mark invitation: greeting 2, invitation 1, signature 1, pictures 12+2+2+2, shared language 8. One required recipient, not a closed pool. Scheme PDF 12 prints contradictory inné examples (2 and 0); compare both original statements.',
        sourceDiscrepancyNotice='Nóta foinse: tá “inné” luaite faoi 2 mharc agus faoi 0 marc sa scéim do lá an chuiridh. Féach ar an scéim bhunaidh.')
    l13,l14,l15=scheme_guidance(13,15)
    letter=add('W-5A','3','Scríobh · Ceist 5(a) · Litir',
        'Féach ar na pictiúir thíos.\n\nTá tusa ag obair sa Gharáiste seo an samhradh seo. Scríobh litir abhaile chuig do chara. Inis dó/di:\n\n'
        '- Faoin nGaráiste agus faoin áit a bhfuil an Garáiste — Pictiúr 1\n'
        '- Faoin obair a dhéanann tú sa Gharáiste. (Trí phointe ag teastáil) — Pictiúr 2\n'
        '- Faoi na daoine a thagann go dtí an Garáiste. (Dhá phointe ag teastáil) — Pictiúr 3\n'
        '- Faoi na rudaí a dhéanann tú nuair a bhíonn am saor agat — Pictiúr 4\n\n'
        'N.B. Bíodh leagan amach cuí ar do litir, i.e. seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[12],[13,14,15],[
            criterion('seoladh','Seoladh',2,[l13.split('Seoladh: 2 mharc',1)[1].split('Dáta:',1)[0]]),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('tus','Tús',1,[l13.split('Tús: 1 marc',1)[1].split('Críoch:',1)[0]]),
            criterion('crioch','Críoch',2,[l13.split('Críoch:',1)[1].split('Na Treoracha:',1)[0]]),
            criterion('pictiur1','Pictiúr 1 · garáiste 2 + áit 2',4,[l13.split('Na Treoracha:',1)[1]]),
            criterion('pictiur2','Pictiúr 2 · trí phointe × 4',12,[l14.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3 · daoine',4,[l14.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0],
                'Published allocation wording differs: scheme PDF 13 says 1× 4 marks for picture 3, but paper PDF 12 and detailed scheme PDF 14 require two references. Keep the published total 4 and the explicit two-reference instruction. No unsupported per-reference tariff is invented.']),
            criterion('pictiur4','Pictiúr 4 · dhá phointe × 2',4,[l14.split('Pictiúr 4',1)[1],l15.split('Léiriú na marcanna',1)[0]]),language(10)],
        ['Scríobh chuig cara faoin ngaráiste agus an áit, trí phointe faoin obair, dhá phointe faoi na daoine, agus na gníomhaíochtaí saor-ama.','Seoladh, dáta, tús agus críoch oiriúnach.'],
        'Whole 40-mark letter: layout 6 (2+1+1+2), pictures 4+12+4+4, shared language 10. Paper and detailed scheme require two references for picture 3 despite overview 1× 4. The worked total labels on PDF 15 say Cum(22)/Cr(8), but its actual totals 30+10 and the opening allocation are consistent. Preserve those printed label errors in the original; this rubric uses 30+10. No later-year length penalty applies.',
        sourceDiscrepancyNotice='Nóta foinse: éilíonn an páipéar agus an treoir mhionsonraithe dhá phointe do phictiúr 3, cé go bhfuil 1× 4 sa tábla. Is é 4 an t-iomlán; tá lipéid 22/8 sa sampla ach iomláin 30/10.',
        additionalTopicIds=['irish-2-8'])
    form_prompt=(
        'Ba mhaith leat post a fháil in Ollstór ‘Tesco’. Fuair tú an Fhoirm Iarratais seo le líonadh.\nLíon isteach an Fhoirm Iarratais anseo thíos.\nNóta: Is tusa Phil de Róiste.\n\n'
        'Ollstór Tesco\nFoirm Iarratais\nAinm: Phil de Róiste\nSeoladh:\nUimhir Theileafóin (Baile):\nFón Póca:\nDáta Breithe:\nAirde:\n'
        'Cén Scrúdú Teistiméireachta atá déanta agat?\nAinmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:\nAr oibrigh tú riamh in Ollstór?\n'
        'An mbeidh tú sásta a bheith ag obair ag an deireadh seachtaine?\nAinmnigh trí chaitheamh aimsire atá agat:\nAn gcaitheann tú tobac?\n'
        'Cuir ciorcal timpeall ar an dáta i mí Lúnasa is fearr leat le haghaidh agallaimh: 15ú / 17ú / 19ú\n\n'
        'Scríobh alt beag (timpeall 40 focal) ag insint dúinn cén fáth ar mhaith leat a bheith ag obair in Ollstór Tesco.\n\nSíniú: Phil de Róiste\nDáta:'
    )
    assert all(f'{day}ú' in texts[12] for day in [15,17,19]) and 'Lúnasa' in texts[12]
    f15=l15.split('Ceist 5 (b) Foirm Iarratais',1)[1]
    f16=scheme_guidance(16,16)[0].split('Ceist 6(a) Cuntas',1)[0]
    fields_guide=[
        'Fields 15: use the printed doubled column. Address 2; home phone 1; mobile 1; birth date 2; height 1; exam 2; five subjects 10; prior store work 1; weekend work 1; three hobbies 6; smoking 1; interview date 1; bottom date 1. Add 30, divide once by 2 and round up once: 21÷2=10½→11.',
        f15.split('An tAlt Beag.',1)[0],
        'Published table conflict: the undoubled hobbies row prints 2, while the doubled row prints 6. The undoubled values therefore sum 14, although both the total 15 and 30÷2 are printed. This rubric follows the explicit doubled 30÷2 method and disclosed 15-mark total, preserving both original columns; no silent correction is made.'
    ]
    forms=[]
    for day in [15,17,19]:
        forms.append(add(f'W-5B-{day}-lunasa','3',f'Scríobh · Ceist 5(b) · {day} Lúnasa',
            form_prompt+f'\n\nAn rogha don chárta seo: {day} Lúnasa.',
            'irish-9-0',['form'],[13],[15,16],[
                criterion('fields','Na Ceisteanna · iomlán slán',15,fields_guide),
                criterion('paragraph','An t-Alt · marc tar éis coigeartú faid',15,[
                    f15.split('An tAlt Beag.',1)[1].split('Cruinneas Gaeilge',1)[0],f16,
                    'Assess the relevant paragraph /15, off-topic /5; reduce only its awarded mark proportionally if short. 20 of 40 words→50% reduction (PDF 15); 32 of 40 words→one-fifth reduction (PDF 16). No fixed reference count or later 8-mark ceiling is printed.'
                ]),language(10)],
            ['Líon gach réimse; cúig ábhar scoile agus trí chaitheamh aimsire.',f'Roghnaigh {day} Lúnasa don agallamh.','Scríobh timpeall 40 focal faoi obair in Ollstór Tesco.'],
            'Whole 40-mark form: fields 15 using doubled 30÷2 rounded once, paragraph 15 after its own length adjustment, shared language 10. Three interview dates expand mechanically. Hobbies and subjects remain open content. Printed undoubled hobby 2 conflicts with doubled 6 and total 15; compare both columns.',
            sourceDiscrepancyNotice='Nóta foinse: tá 2 mharc sa chéad cholún do chaitheamh aimsire agus 6 sa cholún dúbailte. Úsáidtear an modh foilsithe 30÷2 agus iomlán 15; féach ar an dá cholún.'))
    stories=[]
    for slot,page,scheme_page in [('6A',14,16),('6B',15,17)]:
        prompt=(
            'Féach ar an bpictiúr thíos.\n\nBhí tú i láthair ag Cóisir na Nollag sa Chlub Óige.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin gCóisir.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nCÓISIR na NOLLAG sa CHLUB ÓIGE'
            if slot=='6A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú amuigh ag rothaíocht le do chara. Tá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        guide=scheme_guidance(scheme_page,scheme_page)[0]
        if slot=='6A':guide=guide.split('Ceist 6(a) Cuntas',1)[1]
        stories.append(add('W-'+slot,'3',f'Scríobh · Ceist 6({slot[-1].lower()})',
            prompt,'irish-9-4',['pictures','story'],[page],[scheme_page],[
                criterion('cumarsaid','Cumas Cumarsáide · marc tar éis coigeartú faid',37,[guide,
                    'Assess communication /37 against the required five references. Apply the printed proportional short-length reduction to the awarded communication mark only; language /13 is separate. The 2011 scheme does not specify a fixed 5-mark deduction per missing reference, so do not import that later-year rule.']),language(13)],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad; i 6(b), ceann do gach pictiúr agus pointe amháin eile.'],
            'Whole 50-mark story: communication 37 after its proportional short-length reduction plus separate language 13. 2011 requires five references but prints no fixed missing-reference penalty. No later-year worked examples or fixed length table are imported.'))
    # Required Q4,Q5,Q6:2×(one letter+three formdates)× 2 =16 full120-mark selections.
    for first,second,third in itertools.product([notice,invitation],[letter,*forms],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-')+'-'+third['atlasQuestionId'].removeprefix('W-'),
            ' + '.join(c['questionRef'].replace('2011 FL ','') for c in [first,second,third]),
            [first,second,third], 'FREAGAIR GACH CEIST (4, 5 agus 6). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b). Ceist 6: Freagair (a) NÓ (b).')

    papers={FILE+'.pdf':paper,AURAL_FILE+'.pdf':aural_paper}
    decisions=selection_decisions(papers)
    spatial_decisions=selection_decisions(papers,spatial=True)
    assert len(cards)==92 and len({c['id'] for c in cards})==92
    assert sum(c['totalMarks'] for c in cards if c['section']=='1')==180
    outputs={}
    source_review=json.loads(SOURCE_REVIEW.read_text())
    for fileid,doc,paper_file in [(FILE,paper,paper_path),(AURAL_FILE,aural_paper,aural_path)]:
        subset=[c for c in cards if c['paperFileid']==fileid]
        is_aural=fileid==AURAL_FILE
        assert len(subset)==(22 if is_aural else 70)
        review=dict(year=2011,level='foundation',paperFileid=fileid+'.pdf',schemeFileid=SCHEME_FILE+'.pdf',
            paperSha256=hashlib.sha256(paper_file.read_bytes()).hexdigest(),schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
            reviewedPaperPages=list(range(1,len(doc)+1)),reviewedSchemePages=list(range(1,21)),
            reviewDate='2026-10-07',status='reviewed',fullPaperAndApplicableSchemeVisualSweep=True,
            selectionDecisions=[d for d in decisions if d['paperFileid']==fileid+'.pdf'],
            spatialSelectionDecisions=[d for d in spatial_decisions if d['paperFileid']==fileid+'.pdf'],
            atomicPracticeCardIds=[c['id'] for c in subset if 'memberCardIds' not in c],
            pairedRouteCardIds=[c['id'] for c in subset if 'memberCardIds' in c],
            examStructure=dict(listening=180,total=180) if is_aural else dict(matching=40,readingQ2=50,readingQ3=60,writingQ4=30,writingQ5=40,writingQ6=50,writing=120,total=270),
            nonPoolDecisions=source_review['nonPoolDecisions'],openIssues=[],caveats=source_review['sourceFindings'],
            boundaries='22 individually marked listening parts.' if is_aural else '10matching+30reading+8wholewriting routes;6readingpairs and16fullwritingproducts.',
            **({'audio':source_review['audio']} if is_aural else {}))
        outputs['foundation-2011-aural-authored.json' if is_aural else 'foundation-2011-authored.json']=dict(review=review,cards=subset)
    return outputs,scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    outputs={ROOT/'components/MarkBank/cards/irish'/name:json.dumps(value,ensure_ascii=False,indent=2)+'\n' for name,value in data.items()}
    scheme_text='# Gaeilge Bonnleibhéal2011 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page{i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    outputs[ROOT/'examiner-reports/irish/schemes/2011-fl.md']='\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    for path,value in outputs.items():
        if args.check:assert path.exists() and path.read_text()==value, f'Stale Foundation output:{path}'
        else:path.write_text(value)
    print('Irish Foundation2011:22aural +70written task/selection cards; archive remains incomplete.')

if __name__=='__main__':main()
