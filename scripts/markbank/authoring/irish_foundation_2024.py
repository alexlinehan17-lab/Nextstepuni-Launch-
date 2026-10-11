#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2024 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
FILE = 'LC001BLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2024-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b', re.I)

def selection_decisions(paper):
    required = 'Required answers; no finite alternative task pool.'
    writing = 'Choose two of 4(a), 4(b), 5(a), 5(b): six pairs, expanded to twelve for the form’s three interview dates.'
    decisions = {
      (2,'Freagair gach ceist.'):required,
      (2,'Freagair gach ceist (1, 2 agus 3).'):required,
      (2,'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).'):writing,
      (2,'Scríobh do chuid freagraí le peann gorm nó le peann dubh. Ní ceadmhach peann luaidhe a úsáid.'):'Pen colour instruction, not an answer route.',
      (3,'Freagair gach ceist. Tá na treoracha don chuid seo ar an dlúthdhiosca.'):required,
      (3,'Cuir tic (\uf0fc) leis an bhfreagra ceart i ngach cás.'):'Correct-answer selection; distractors are not valid task routes.',
      (4,'Cá bhfuil an scoil? (Cuir tic (\uf0fc) sa bhosca ceart.)'):'One correct map position; distractors are not valid task routes.',
      (5,'Nuair a bheidh an Chluastuiscint críochnaithe agat lean ar aghaidh agus freagair na ceisteanna'):required,
      (6,'Freagair gach ceist (1, 2 agus 3).'):required,
      (7,'Ceist 2 Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.'):'Choose two of three passages: AB, AC, BC; each route 50 marks. Each published five-mark answer is also independently practicable.',
      (7,'Léigh an litir atá anseo thíos agus freagair na ceisteanna ar fad atá fúithi.'):required,
      (8,'Léigh an bróisiúr atá anseo thíos agus freagair na ceisteanna ar fad atá faoi. (25 marc)'):required,
      (9,'Léigh an scéal atá anseo thíos agus freagair na ceisteanna ar fad atá faoi.'):required,
      (10,'Ceist 3 Freagair do rogha dhá cheann de (a), (b), (c) anseo thíos.'):'Choose two of three passages: AB, AC, BC; each route 60 marks. Each published six-mark answer is also independently practicable.',
      (10,'Léigh an t‐alt atá anseo thíos agus freagair na ceisteanna ar fad atá faoi. (30 marc)'):required,
      (11,'(b) Léigh an giota seo a leanas agus freagair na ceisteanna ar fad atá faoi. (30 marc)'):required,
      (12,'(c) Léigh na véarsaí seo a leanas agus freagair na ceisteanna ar fad atá fúthu.'):required,
      (13,'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas:'):writing,
      (13,'4 (a), 4 (b), 5 (a) nó 5 (b)'):writing,
      (14,'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).'):writing,
      (15,'Ainmnigh cúig ábhar scoile a rinne tú sa scrúdú sin: …………………………………………………………………..'):'Five school subjects are open answers, not an enumerated task menu.',
      (15,'Luaigh trí chaitheamh aimsire atá agat: ……….......…………………..…………………………………………………..'):'Three hobbies are open answers, not an enumerated task menu.',
      (15,'Cuir tic (\uf0fc) leis an dáta is fearr leat le haghaidh agallaimh:'):'Closed choose-one menu: 25 Meitheamh, 27 Meitheamh, 3 Iúil. Three whole form routes, each retaining one shared language award.',
      (20,'D’fhéadfadh sé go bhfuil téacsanna nó íomhánna sa scrúdpháipéar seo nach é Coimisiún na Scrúduithe Stáit'):'Copyright statement, not a task.',
    }
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == set(decisions), ('Unclassified/stale selection directives', found-set(decisions), set(decisions)-found)
    return [dict(page=page,raw=raw,decision=reason) for (page,raw),reason in decisions.items()]

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2024/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2024/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '7decc354725d34b231f4aa5cbb0daca77bd34ab869552fd7d330b219c8e617f0', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == 'c6f19c2c1e65ef37ca506e484163c89016ecd005444738f132f352122fccbfcb', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2024-fl-{key.lower()}', year=2024, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2024 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2024 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [
      ('1a',3,7,'Cá bhfuil Seán ina chónaí?',None,'Feirm = an tríú pictiúr'),
      ('1b',3,7,'Cén duine is óige sa teaghlach?','Eoghan | Máire | Deirdre','Deirdre'),
      ('2a',3,7,'Cad a reáchtálann Síle agus a teaghlach?',None,'Óstán = an dara pictiúr'),
      ('2b',3,7,'Cá gcaitheann Síle a cuid airgid ar fad?','I siopaí bróg | I siopaí éadaí | I mbialann','I siopaí éadaí'),
      ('3',4,8,'Cá bhfuil an fear ag dul?',None,'Siopa ceoil = an ceathrú pictiúr'),
      ('4',4,8,'Cá bhfuil an scoil? (Cuir tic (✓) sa bhosca ceart.)',None,'An bosca ag an mbun ar dheis (tic nó saighead sa bhosca)'),
      ('5a',4,8,'Cad a bheidh ar siúl ar a naoi a chlog mar chuid den lá spóirt?',None,'Cluiche sacair = an dara pictiúr'),
      ('5b',4,8,'Cé a fhanfaidh sa halla leis an áit a ghlanadh suas?','Na múinteoirí agus na daltaí | Na daltaí ó bhliain a sé | Na daltaí ar fad','Na daltaí ó bhliain a sé'),
      ('6a',5,10,'Cén bheirt is fearr le hAoife?','Pól agus Áine | Aoife agus Seán | Aindí agus Órla','Aindí agus Órla'),
      ('6b',5,10,'Cén sórt duine é Seán, dar le hAoife?','Réalaíoch | Grámhar | Dáiríre','Dáiríre'),
      ('7a',5,10,'Cár chaith Stíofán agus a chairde seachtain an bhliain seo caite?','Sa tSeapáin | Sa Fhrainc | Sa Ghréig','Sa Fhrainc'),
      ('7b',5,10,'Cé mhéad a chosnódh seachtain sa Spáinn, dar le Stíofán?','€350 an duine | €400 an duine | €550 an duine','€400 an duine'),
      ('8a',5,10,'Cé mhéad pointe a bhí idir na foirne ag leath ama?','Dhá phointe | Trí phointe | Ceithre phointe','Ceithre phointe'),
      ('8b',5,10,'Cá mbeidh an fhoireann ag dul ar leathuair tar éis a sé?','Óstán áitiúil | Club óige áitiúil | Halla spóirt áitiúil','Club óige áitiúil'),
    ]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2024/LC001BLP017IV.mp3'
    for n,page,marks,prompt,options,answer in aural:
        comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
        assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (n,prompt)
        for option in (options or '').split(' | '):
            assert comparable(option) in comparable(texts[page-1]), (n,option)
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$',r'(\1)',n)
        add('A-'+n,'1',ref,re.sub(r'^(\d+)([ab]?)$', lambda m: m[1]+'. '+('('+m[2]+') ' if m[2] else ''), n)+prompt+
            ('\n\n'+options.replace(' | ','\n') if options else ''),
            'irish-1-3',['aural'],[page],[3],
            [criterion('answer','Freagra',marks,[answer],True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio',label=ref,
                title='Gaeilge Bonnleibhéal 2024 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))

    signs = [
      'Ceachtanna Gailf\nCuir feabhas ar do chuid scileanna gailf!',
      'Ranganna Gaeilge\nAg tosú Dé Máirt\ni Scoil Naomh Eoin',
      'Dioscó do Dhéagóirí\nGach Satharn i gClub Oíche na Trá',
      'Meicneoir ar fáil\nDeiseoimid do charr anseo inniu!',
      'Traenáil Iománaíochta\nAm lóin gach Máirt agus Déardaoin',
      'Ar Díol\nRíomhaire nua\nPraghas: €400',
      'Ar Iarraidh\nMadra dubh agus bán\nGlaoigh ar 081 321 465',
      'Rabhadh! Bóthar dúnta!\nBóthar faoi uisce\nTéigh ar mhalairt slí',
      'An Faisean is déanaí\nSiopa nua éadaí ar oscailt\nLuan go Satharn',
      'Snámh Urraithe\nAr son Trócaire\nBí ar an trá ar 3.00 p.m.',
    ]
    for i,(sign,answer) in enumerate(zip(signs,'EAJICBDHFG'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[6],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {
      '2A':(7,'letterReading',[
        ('Cén dáta a sheol Colm an litir chuig Gaeilge Bheo?','29 Bealtaine | 7 Meitheamh | 11 Meitheamh','29 Bealtaine'),
        ('Cad is ainm do ghrúpa ceoil Choilm?','Na Buachaillí Dána | The Chieftains | U2','Na Buachaillí Dána'),
        ('Cén lá a chaithfidh an colún a bheith scríofa?','Dé Luain | Dé Céadaoin | Dé hAoine','Dé hAoine'),
        ('Cén sórt ceoil a thaitníonn le Colm?','Rac-cheol | Ceol traidisiúnta | Snagcheol','Rac-cheol'),
        ('Cén t-am ba mhaith le hÁine bualadh le Colm?','A haon a chlog | A trí a chlog | A cúig a chlog','A trí a chlog')]),
      '2B':(8,'brochure',[
        ('Cá bhfuil Gaeltacht na Rinne suite?','I gcathair Chorcaí | I ndeisceart Phort Láirge | I gcathair Phort Láirge','I ndeisceart Phort Láirge'),
        ('Cén fhad atá an Rinn ó bhaile Dhún Garbhán?','Ocht gciliméadar | Deich gciliméadar | Seachtó ciliméadar','Deich gciliméadar'),
        ('Cén duine ón Rinn a bhuaigh Corn Uí Riada trí bliana i ndiaidh a chéile?','Nioclás Tóibín | Cárthach Mac Craith | Labhrás Ó Cadhla','Nioclás Tóibín'),
        ('Cá mbíonn na seisiúin cheoil ar siúl?','Ar an trá | Sa mheánscoil áitiúil | Ar an nglasbhealach','Sa mheánscoil áitiúil'),
        ('Cad is ainm don ghlasbhealach sa cheantar?','Heilbhic | Ros Mhic Thriúin | Rian Glas na nDéise','Rian Glas na nDéise')]),
      '2C':(9,'extract',[
        ('Cá raibh Peadar maidin Déardaoin?','Ar scoil | Sa bhaile | Oifig an phríomhoide','Ar scoil'),
        ('Cén t-am a chuaigh Peadar a chodladh?','A seacht a chlog | A naoi a chlog | Ceathrú tar éis a naoi','A naoi a chlog'),
        ('Cé a dhúisigh Peadar ar maidin?','A dhaid | An príomhoide | An múinteoir','A dhaid'),
        ('Cén rang a bhí ag Peadar ar dtús?','Rang Gaeilge | Rang Fraincise | Rang Béarla','Rang Béarla'),
        ('Cá raibh fón póca Pheadair?','Sa bhaile | Ina phóca | Ina mhála scoile','Ina phóca')]),
      '3A':(10,'news',[
        ('Cén aois a bhí Ciana nuair a bhuaigh sí craobh na liathróide láimhe ag na Cluichí Pobail?','Deich mbliana d’aois | Dhá bhliain déag d’aois | Dhá bhliain is fiche d’aois','Dhá bhliain déag d’aois'),
        ('Cén bhliain a bhuaigh Ciana Craobh Shinsir na hÉireann?','2014 | 2018 | 2023','2023'),
        ('Cén chéim a bhain Ciana amach in Ollscoil Luimnigh?',None,'Céim sa Ghaeilge agus sa Chorpoideachas'),
        ('Cár thosaigh Ciana ag staidéar in 2018?','In Minnesota | I Luimneach | I nGaillimh','In Minnesota'),
        ('Cén chéim a bhain Ciana amach in Ollscoil Minnesota?','Céim sa Ghaeilge | Céim i Síceolaíocht an Spóirt | Céim sa Chorpoideachas','Céim i Síceolaíocht an Spóirt')]),
      '3B':(11,'extract',[
        ('Cá mbíonn Féile na Gealaí ar siúl?','Béal Feirste | Ráth Chairn | Ciarraí','Ráth Chairn'),
        ('Cén bhliain a bhuaigh Féile na Gealaí féile na bliana?','2017 | 2018 | 2023','2018'),
        ('Cad as don ghrúpa ceoil Polka 4?','Ráth Chairn | Albain | Ciarraí','Ciarraí'),
        ('Cá huair a bhí imeachtaí ar siúl do pháistí?',None,'An deireadh seachtaine sin'),
        ('Cén mothúchán a bhraith eagraithe na féile in 2021 agus in 2022?','Áthas | Díomá | Dóchas','Díomá')]),
      '3C':(12,'poem',[
        ('Cá háit ar mhaith leis an spásaire dul?','Ar eitleán | Go dtí an ghealach | Ar long','Go dtí an ghealach'),
        ('Cad a fuair an spásaire óna aintín um Nollaig?','Cóta mór báistí | Dinnéar | Culaith spásaire','Culaith spásaire'),
        ('Cad a bheidh acu nuair a shroichfidh siad an ghealach?',None,'Picnic / Bia'),
        ('Cén eagla atá ar an spásaire?','Go gcaillfidh sé an tae | Go rachaidh sé ar strae | Nach bhfaighidh sé clocha','Go rachaidh sé ar strae'),
        ('Cá háit nach mór dó a bheith roimh a naoi?','Ina leaba | Ar an ngealach | Sa spáslong','Ina leaba')]),
    }
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
            assert comparable(answer) in comparable(scheme[4 if slot[0]=='2' else 5].get_text()), (slot,i,answer)
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
                c['label']=member['questionRef'].replace('2024 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(c['topicId'] for c in members))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2024 FL ','')+'\n'+c['questionText'] for c in members),
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
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Cead isteach?\nCén t-aoi speisialta a bheidh i láthair?\nCad a dhéanfar leis an airgead?',
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
        'Ba mhaith leat a bheith ag obair an samhradh seo mar fhreastalaí i mbialann áitiúil. Líon isteach an Fhoirm Iarratais atá anseo thíos. [Nóta: Is tusa Síle Ní Cheallaigh.]',
        'Bialann na Trá, Cill Airne, Co. Chiarraí\nFoirm Iarratais do Phost mar Fhreastalaí',
        'Ainm: Síle Ní Cheallaigh\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:',
        'Cén scrúdú Teistiméireachta atá déanta agat?',
        'Ainmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:',
        'An bhfuil tú ag obair faoi láthair?',
        'Luaigh trí chaitheamh aimsire atá agat:',
        'An réitíonn tú go maith le daoine eile?',
        'An féidir leat a bheith ag obair ag an deireadh seachtaine?',
        'Cuir tic (✓) leis an dáta is fearr leat le haghaidh agallaimh:\n25 Meitheamh\n27 Meitheamh\n3 Iúil',
        'Scríobh alt gearr (timpeall 40 focal) ag insint cén fáth ar mhaith leat post samhraidh mar fhreastalaí sa bhialann seo.',
        'Síniú: Síle Ní Cheallaigh\nDáta:',
    ])
    forms=[]
    for code,date in [('25-meitheamh','25 Meitheamh'),('27-meitheamh','27 Meitheamh'),('3-iuil','3 Iúil')]:
        forms.append(add('W-4B-'+code,'3','Scríobh · Ceist 4(b) · '+date,
            form_text+'\n\nAn rogha don chárta seo: '+date+'.',
            'irish-9-0',['form'],[15],[11,12],[
                criterion('fields','Na Ceisteanna',19,scheme_guidance(11,11)),
                criterion('paragraph','An tAlt Gearr · Cumarsáid',15,
                    ['Cumarsáid a mharcáil as 15 má tá an t-alt “ad rem”; as 5 mura bhfuil sé “ad rem”.']),
                criterion('length','An tAlt Gearr · Fad',3,
                    ['Timpeall 40 focal. Tábla foilsithe: 35–40 focal: 0; 25–34 focal: −1; 10–24 focal: −2; <10 focal: −3.'],
                    deduct_from='paragraph'),copy.deepcopy(language)],
            ['Is tusa Síle Ní Cheallaigh. Líon gach réimse agus scríobh alt timpeall 40 focal.', 'Dáta agallaimh don rogha seo: '+date+'.'],
            'The 19 field marks, 15 paragraph marks and single 11-mark language award belong to one form. The three printed interview dates are separate valid routes. School subjects and hobbies are open choices.'))

    stories=[]
    for slot,page,end,title in [('5A',16,13,'Cuntas'),('5B',17,15,'Eachtra')]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nChuaigh tú féin agus do theaghlach ar Saoire go Páras na Fraince an bhliain seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin tsaoire sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nSaoire go Páras na Fraince'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ag siopadóireacht le do chara tar éis na scoile.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEachtra a Tharla agus Mé ag Siopadóireacht'
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
            combine('W-'+a+'-'+b+suffix,'Scríobh · '+left['questionRef'].removeprefix('2024 FL Scríobh · ')+' + '+right['questionRef'].removeprefix('2024 FL Scríobh · '),
                [left,right], 'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).')

    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==78 and len({c['id'] for c in cards})==78
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2024,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,25)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writing=90,total=360),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and form fields are compulsory context. One language award covers each whole response.',
            'School subjects and hobbies are open choices; the paper does not enumerate a finite pool.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=dict(url=audio_url,verified='2026-10-07',httpStatus=200,contentType='audio/mpeg',bytes=53345645,
                   browserReadyState=4,durationSeconds=1667.051406,playbackAdvanced=True),
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 6 whole writing routes; 6 paired reading routes; 12 paired writing routes.',
        caveats=['Foundation 2024 only. Other years remain pending.',
                 'The 2024 form length table is 35–40: 0, 25–34: −1, 10–24: −2, <10: −3. Do not substitute the different 2025 table.'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2024 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2024-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2024: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
