#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2025 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
import fitz

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001BLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

def build():
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2025/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2025/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '867f156bd2c3f617c1715ac393c51e1c6f2b1a279db2c0f1438a904cb681f6b5', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '1e1aa8695aa5ee3dbee04b0ae91318bdc719c86a8b609b3600914e3db09af82e', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2025-fl-{key.lower()}', year=2025, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2025 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2025 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [
      ('1a',3,7,'Cad a thiomáineann Seán ar an bhfeirm gach lá?',None,'Tarracóir = an dara pictiúr'),
      ('1b',3,7,'Cén rud a cheannaigh a dhaid do Sheán le déanaí?','Capall | Bó | Cearc','Capall'),
      ('2a',3,7,'Cén seomra a osclaíodh go hoifigiúil inné?',None,'Seomra ríomhairí = an ceathrú pictiúr'),
      ('2b',3,7,'Cathain a bheidh na ranganna ríomhaireachta do phobal an Spidéil ag tosú?','I mí Eanáir | I rith an tsamhraidh | Inniu','I mí Eanáir'),
      ('3',4,8,'Cá bhfuil an bhean ag dul?',None,'Banc = an tríú pictiúr'),
      ('4',4,8,'Cá bhfuil an caifé? (Cuir tic (✓) sa bhosca ceart.)',None,'An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)'),
      ('5a',4,8,'Conas a bheidh an aimsir maidin inniu?',None,'Grianmhar agus geal = an chéad pictiúr'),
      ('5b',4,8,'Cén teocht a bheidh ann tráthnóna amárach?','4 chéim Celsius | 10 gcéim Celsius | 16 chéim Celsius','16 chéim celsius'),
      ('6a',5,10,'Cad a bhí ar siúl ag Liam nuair a bhain timpiste dó?','Bhí sé ag imirt peile. | Bhí sé ag rothaíocht. | Bhí sé ag imirt rugbaí.','Bhí sé ag rothaíocht.'),
      ('6b',5,10,'Cathain a bhí coinne ag Liam leis an dochtúir?','Dé Sathairn seo caite | An mhí seo caite | Coicís ó shin','Coicís ó shin'),
      ('7a',5,10,'Cén marc a bhronn an múinteoir Gaeilge ar scrúdú Aoife le déanaí?','55% | 70% | 80%','55%'),
      ('7b',5,10,'Cé mhéad leathanach a scríobh Aoife mar fhreagra?','Dhá leathanach | Trí leathanach | Ceithre leathanach','Trí leathanach'),
      ('8a',5,10,'Cén costas a bhí ar charr úr Shíle?','€500 | €4,000 | €4,500','€4,500'),
      ('8b',5,10,'Cá huair a bhíonn lá saor ag an mbainisteoir?','Dé hAoine | Dé Sathairn | Dé Domhnaigh','Dé Sathairn'),
    ]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2025/LC001BLP017IV.mp3'
    for n,page,marks,prompt,options,answer in aural:
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$',r'(\1)',n)
        add('A-'+n,'1',ref,re.sub(r'^(\d+)([ab]?)$', lambda m: m[1]+'. '+('('+m[2]+') ' if m[2] else ''), n)+prompt+
            ('\n\n'+options.replace(' | ','\n') if options else ''),
            'irish-1-3',['aural'],[page],[3],
            [criterion('answer','Freagra',marks,[answer],True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio',label=ref,
                title='Gaeilge Bonnleibhéal 2025 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))

    signs = [
      'Comórtas Damhsa\nDuais €100\nAnocht 7.30 p.m.',
      'Bialann Uí Néill\nRogha an Lae\nIspíní agus Sceallóga €5',
      'Páirc an Bhaile\nFáilte roimh mhadraí',
      'Bus na Tuaithe\nDé Luain – Dé Sathairn\n3.00 p.m.',
      'Ciúnas sa Leabharlann\nCosc ar fhóin phóca',
      'Siopa Éadaí\nSladmhargadh\nLacáiste 20% ar gach rud',
      'Crainn Nollag ar Díol\n€20 an crann',
      'An Garáiste Áitiúil\nCarranna ar díol\nBuail isteach!',
      'Dúnta!\nAn scoil dúnta de bharr an tsneachta',
      'Toghchán na Scoile\nCuir do vóta sa bhosca vótála!',
    ]
    for i,(sign,answer) in enumerate(zip(signs,'CDHEIABJFG'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[6],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {
      '2A':(7,'letterReading',[
        ('Cén dáta a tháinig an litir chuig Gaelscoil Uí Riain?','4 Meitheamh | 17 Meitheamh | 21 Meitheamh','4 Meitheamh'),
        ('Cé mhéad bliain a chaith Laoise i nGaelscoil na Trá?','Bliain amháin | Dhá bhliain | Trí bliana','Trí bliana'),
        ('Cén comórtas a bhuaigh Laoise ag an Oireachtas in 2023?','Amhránaíocht | Damhsa | Spórt','Damhsa'),
        ('Cá bhfuil club CLG áitiúil Laoise suite?','Sa Rinn | I nDún Garbhán | I gCill Airne','Sa Rinn'),
        ('Cad iad na laethanta a bheidh Eoghan ar fáil san oifig?','Ó Luan go hAoine | Ó Chéadaoin go hAoine | Ó Luan go Déardaoin','Ó Luan go Déardaoin')]),
      '2B':(8,'brochure',[
        ('Cathain a osclaíodh Ionad Cultúrtha an Phiarsaigh?','1909 | 1916 | 2016','2016'),
        ('Cén ról a bhí ag an bPiarsach in Éirí Amach na Cásca, 1916?','Ar dhuine de na ceannairí | File | Cuairteoir','Ar dhuine de na ceannairí'),
        ('Cad atá idir an t-ionad féin agus teach an Phiarsaigh?','Caifé | Siúlóid álainn | Siopa beag','Siúlóid álainn'),
        ('Cén t-am a bhíonn an t-ionad oscailte ó mhí na Samhna go dtí deireadh mhí na Bealtaine?','Ní bhíonn sé oscailte. | 9.45 a.m. go dtí 4.00 p.m. | 9.45 a.m. go dtí 6.00 p.m.','9.45 a.m go dtí 4.00 p.m.'),
        ('Cén costas atá ann do mhic léinn?','€3 | €4 | €13','€3')]),
      '2C':(9,'extract',[
        ('Cén spórt ab fhearr le Liam?','Peil | Sacar | Iománaíocht','Iománaíocht'),
        ('Ní raibh sé maith go leor le himirt ar ...','fhoireann an chlub. | fhoireann an chontae. | fhoireann na scoile.','fhoireann an chontae'),
        ('Cén laige ba mhó a bhí feicthe ag Séamus in imirt Liam?','Bhí Liam sciliúil. | Bhí Liam aclaí. | Bhí Liam leithleach.','Bhí Liam leithleach.'),
        ('Conas a d’éirigh le foireann Liam sa chluiche an tseachtain dár gcionn?','Níor scóráil siad. | Bhuaigh siad le 10 bpointe. | Níor bhuaigh siad.','Bhuaigh siad le 10 bpointe.'),
        ('Cé a ghlaoigh ar fhón Liam an oíche sin?','Na himreoirí eile | Séamus Ó hAodha | Seán Ó Luasa','Seán Ó Luasa')]),
      '3A':(10,'news',[
        ('Cad is ainm don bhainisteoir nua?','Marc Canham | Heimir Hallgrímsson | Stephen Kenny','Heimir Hallgrímsson'),
        ('Cén post a bhí ag athair Hallgrímsson?','Innealtóir | Fiaclóir | Deisitheoir','Deisitheoir'),
        ('Cén ollscoil ar fhreastail Hallgrímsson uirthi?',None,'Ollscoil Réicivíc'),
        ('Cad a rinne Hallgrímsson nuair a cháiligh sé mar fhiaclóir?','Rinne sé staidéar. | D’oscail sé clinic. | Chláraigh sé ar chúrsa.','D’oscail sé clinic.'),
        ('Cá huair a bhí sé ina chomhbhainisteoir ar fhoireann na hÍoslainne?','Idir 1996 agus 2007 | Idir 2006 agus 2011 | Idir 2013 agus 2016','Idir 2013 agus 2016')]),
      '3B':(11,'extract',[
        ('Cárb as do Diane Ní Chanainn?','Anagaire | Árainn Mhór | Mín Lárach','Mín Lárach'),
        ('Cén post a bhí ag Pádraig Ua Cnáimhsí?','Eagarthóir | Múinteoir | Amhránaí','Múinteoir'),
        ('Cá huair a chuir Cathal Goan an dlúthdhiosca le chéile?','In 2024 | Sna 1950idí | Sna 1990idí','Sna 1990idí'),
        ('Cad a bhíonn ar siúl in Árainn Mhór i mí na Bealtaine gach bliain?',None,'Bíonn Féile Róise Rua ar siúl'),
        ('Cé atá le cloisteáil ar an traic ag seinm an ghiotáir?','Steve Cooney | Proinsias Ó Conluain | Dónal O’Connor','Steve Cooney')]),
      '3C':(12,'poem',[
        ('Cén sórt garsúin é Seán, dar leis an bhfile?','Ar fheabhas | Deas | Bán','Deas'),
        ('Cé a bhuann, dar leis an bhfile?','Seán | An cat | Seoirse','An cat'),
        ('Cathain nach mbeidh an saol go breá?',None,'Ar ball beag / Nuair a rachaidh Seán ar scoil'),
        ('Cá rachaidh Seán?','Ar scoil | Abhaile | Teach a chomharsan','Ar scoil'),
        ('Cá rachaidh an cat?','Ar scoil | Ar fán | Le Seán','Ar fán')]),
    }
    reading_cards = {}
    for slot,(page,exam_topic,rows) in reading.items():
        reading_cards[slot] = []
        for i,(prompt,options,answer) in enumerate(rows,1):
            # Fail on stale question text; normalize only punctuation differences
            # between PDF fonts and the accessible prompt.
            comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
            assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (slot,i,prompt)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],[5 if slot[0]=='2' else 6],
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2025 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(c['topicId'] for c in members))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2025 FL ','')+'\n'+c['questionText'] for c in members),
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

    language=criterion('gaeilge','Cruinneas Gaeilge',11,[
        'Sármhaith 9–11; An-mhaith 7–8; Maith 5–6; Maith go leor 4; Lag 2–3; An-lag 1; Easnamhach 0.',
        'Dul na Gaeilge: struchtúr na Gaeilge agus beachtas gramadaí. Foclóir: cruinneas agus oiriúnacht foclóra. Litriú.',
        'Bronn marc as 11 ar chaighdeán na Gaeilge san iarracht iomlán.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme[p-1].get_text())) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Cead isteach?\nCén t-aoi speisialta a bheidh i láthair?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',10,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1]]),
            criterion('pictiur3','Pictiúr 3',5,[notice_p10.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',5,[notice_p10.split('Pictiúr 4',1)[1].split('N.B.',1)[0]]),copy.deepcopy(language)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared language mark. Apply each −1 past-tense penalty within the affected picture award. Required headings are not choices.')
    form_text = '\n\n'.join([
        'Foirm Iarratais',
        'Ba mhaith leat a bheith ag obair an samhradh seo mar chúntóir i siopa áitiúil. Líon isteach an Fhoirm Iarratais atá anseo thíos. [Nóta: Is tusa Nuala Seoighe]',
        'An Siopa Áitiúil, Cathair na Mart, Co. Mhaigh Eo.\nFoirm Iarratais do Phost mar Chúntóir Siopa',
        'Ainm: Nuala Seoighe\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:',
        'Cén scrúdú Teistiméireachta atá déanta agat?',
        'Ainmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:',
        'An bhfuil post agat faoi láthair?',
        'Luaigh trí chaitheamh aimsire atá agat:',
        'An raibh post agat i siopa riamh cheana?',
        'An mbeidh tú sásta a bheith ag obair ag an deireadh seachtaine?',
        'Cuir tic (✓) leis an dáta is fearr leat le haghaidh agallaimh:\n16 Aibreán\n5 Bealtaine\n10 Meitheamh',
        'Scríobh alt gearr (timpeall 40 focal) ag insint cén fáth ar mhaith leat post páirtaimseartha mar chúntóir sa siopa áitiúil seo.',
        'Síniú: Nuala Seoighe\nDáta:',
    ])
    forms=[]
    for code,date in [('16-aibrean','16 Aibreán'),('5-bealtaine','5 Bealtaine'),('10-meitheamh','10 Meitheamh')]:
        forms.append(add('W-4B-'+code,'3','Scríobh · Ceist 4(b) · '+date,
            form_text+'\n\nAn rogha don chárta seo: '+date+'.',
            'irish-9-0',['form'],[15],[11,12],[
                criterion('fields','Na Ceisteanna',19,scheme_guidance(11,11)),
                criterion('paragraph','An tAlt Gearr · Cumarsáid',15,
                    ['Cumarsáid a mharcáil as 15 má tá an t-alt “ad rem”; as 5 mura bhfuil sé “ad rem”.']),
                criterion('length','An tAlt Gearr · Fad',3,
                    ['Timpeall 40 focal. Tábla foilsithe: 20–40 focal: 0; 1–19 focal: −1. Foilsítear uasteorainn −3 ach ní thugtar tairseacha breise: ná cum rialacha eile.'],
                    deduct_from='paragraph'),copy.deepcopy(language)],
            ['Is tusa Nuala Seoighe. Líon gach réimse agus scríobh alt timpeall 40 focal.', 'Dáta agallaimh don rogha seo: '+date+'.'],
            'The 19 field marks, 15 paragraph marks and single 11-mark language award belong to one form. The three printed interview dates are separate valid routes. School subjects and hobbies are open choices.'))

    stories=[]
    for slot,page,end,title in [('5A',16,13,'Cuntas'),('5B',17,15,'Eachtra')]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nChuaigh tú féin agus do chairde chuig Féile Cheoil an samhradh seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin bhféile cheoil sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nFéile Cheoil'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ar an trá le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEachtra a Tharla agus Mé ar an Trá'
        )
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(13 if slot=='5A' else 14,end+1)),[
                criterion('cumarsaid','Cumas Cumarsáide',34,[paragraph.split('Cruinneas Gaeilge',1)[0] for paragraph in scheme_guidance(13 if slot=='5A' else 14,end)]),
                copy.deepcopy(language),
                criterion('length','Fad',4,['80–90 focal: 0; 60–79: −2; 30–59: −3; <30: −4.'],deduct_from='cumarsaid')],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'References in the scheme are indicative, not a closed selection pool. One shared communication award and one language award cover the whole response. The scheme requires a reference to each of the four pictures plus another detail for 5(b).'))
    writing={'4A':[notice],'4B':forms,'5A':[stories[0]],'5B':[stories[1]]}
    for a,b in itertools.combinations(writing,2):
        for left,right in itertools.product(writing[a],writing[b]):
            suffix='-'+next(c['atlasQuestionId'].removeprefix('W-4B-') for c in [left,right] if c in forms) if a=='4B' or b=='4B' else ''
            combine('W-'+a+'-'+b+suffix,'Scríobh · '+left['questionRef'].removeprefix('2025 FL Scríobh · ')+' + '+right['questionRef'].removeprefix('2025 FL Scríobh · '),
                [left,right], 'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).')

    # Every printed selection directive is classified against the exact source
    # page; content hashes additionally invalidate review after any PDF change.
    decisions={
      2:'Writing choose 2 of 4: six pairs, expanded to twelve after the form date choice.',
      3:'Tick the correct answer: distractors are not valid task routes.',
      4:'Tick the correct map position: distractors are not valid task routes.',
      7:'Reading Q2 choose 2 of A/B/C: three 50-mark routes, plus all fifteen 5-mark practice parts.',
      10:'Reading Q3 choose 2 of A/B/C: three 60-mark routes, plus all fifteen 6-mark practice parts.',
      13:'Repeat of writing choose 2 of 4; no new selection.',
      14:'Repeat of writing choose 2 of 4; required picture headings are not choices.',
      15:'Three interview dates: three form routes. Five subjects and three hobbies are open choices.',
    }
    directive = re.compile(r'Freagair (?:do rogha |dhá)|Cuir tic|Ainmnigh cúig|Luaigh trí',re.I)
    found={i for i,text in enumerate(texts,1) if directive.search(text)}
    assert found==set(decisions), ('Unclassified/stale selection pages',found^set(decisions))
    assert len(cards)==78 and len({c['id'] for c in cards})==78
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2025,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,25)),
        reviewDate='2026-10-07',selectionDecisions=decisions,
        audio=dict(url=audio_url,verified='2026-10-07',httpStatus=200,contentType='audio/mpeg',bytes=56620515),
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 6 whole writing routes; 6 paired reading routes; 12 paired writing routes.',
        caveats=['Foundation 2025 only. Other years remain pending.',
                 'Form length scheme names maximum −3 but its explicit table only prints 0 and −1; no extra word thresholds have been invented.'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2025 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2025-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2025: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
