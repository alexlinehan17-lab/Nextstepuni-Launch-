#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2021 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2021-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2021-source-review.json'

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2021/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2021/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'e5b0b96924bb9c55ba3cb4a9669e669c37eb4218a5ea810156c05466f9d858bf', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '55f04b3e0511892231e6c948c206b2f5a8ab6239b31031f415e165cf6bf7c5bd', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2021-fl-{key.lower()}', year=2021, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2021 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2021 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén uirlis cheoil a sheinneann Micheál le cór na scoile?', None, 'An giotár = an dara pictiúr'),
 ('1b', 2, 7, 'Cad a chum Micheál don amhrán?', 'An ceol | An físeán | Na liricí', 'Na liricí'),
 ('2a', 2, 7, 'Cá bhfuil Deirdre ag obair faoi láthair?', None, 'I gCaisleán Chill Chainnigh = an ceathrú pictiúr'),
 ('2b', 2, 7, 'Cathain a thug Deirdre cuairt ar Bhrú na Bóinne?', 'I mí an Mheithimh | I mí Iúil | I mí Lúnasa', 'I mí Iúil'),
 ('3', 3, 8, 'Cá bhfuil an fear ag dul?', None, 'An músaem eolaíochta = an chéad phictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil Teach Lóistín na Mara? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)'),
 ('5a',
  3,
  8,
  'Cén sórt aimsire a bheidh ann don chluiche mór iománaíochta i bPáirc an Chrócaigh?',
  None,
  'Ceathanna troma báistí = an tríú pictiúr'),
 ('5b', 3, 8, 'Cén teocht is ísle a bheidh ann oíche amárach?', '5 chéim Celsius | 7 gcéim Celsius | 16 chéim Celsius', '5 chéim Celsius'),
 ('6a', 4, 10, 'Cad a chaill Dónall?', 'Eochair an tí | An fón | A mhála spóirt', 'Eochair an tí'),
 ('6b',
  4,
  10,
  'Cén fáth nach bhfuil fonn ar Nuala an doras a oscailt?',
  'Tá sí préachta leis an bhfuacht | Níl aon chóta aici | Tá sí breá compordach ina leaba',
  'Tá sí breá compordach ina leaba'),
 ('7a',
  4,
  10,
  'Cén chéad rogha a chuir Diarmaid síos ar fhoirm an CAO i mí Eanáir?',
  'Cúrsa Spáinnise | Cúrsa Gnó | Cúrsa Margaíochta',
  'Cúrsa Gnó'),
 ('7b',
  4,
  10,
  'Cad a chuir Síle i láthair ar raidió na scoile nuair a bhí sí san Idirbhliain?',
  'Clár ceoil | Cuntais ar imeachtaí spóirt | Dráma',
  'Clár ceoil'),
 ('8a', 4, 10, 'Cá raibh Cathal agus a dheartháir Dé Sathairn?', 'Ar an trá | Ag féile cheoil | Ag siúl sna sléibhte', 'Ag féile cheoil'),
 ('8b', 4, 10, 'Cad a dhéanann dochar do na héisc sna farraigí?', 'Na cannaí folmha | Na boscaí bruscair | An plaisteach', 'An plaisteach')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2021/LC001BLP017IV.mp3'
    for n,page,marks,prompt,options,answer in aural:
        comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
        assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (n,prompt)
        for option in (options or '').split(' | '):
            assert comparable(option) in comparable(texts[page-1]), (n,option)
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$',r'(\1)',n)
        card = add('A-'+n,'1',ref,re.sub(r'^(\d+)([ab]?)$', lambda m: m[1]+'. '+('('+m[2]+') ' if m[2] else ''), n)+prompt+
            ('\n\n'+options.replace(' | ','\n') if options else ''),
            'irish-1-3',['aural'],[page],[3],
            [criterion('answer','Freagra',marks,[answer],True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio',label=ref,
                title='Gaeilge Bonnleibhéal 2021 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Comórtas Amhránaíochta\nDuaiseanna iontacha do ghuthanna breátha',
 'Fáilte go hInis Mór\nRothair ar cíos anseo\n€10 in aghaidh an lae',
 'Meaisín Bainc\nClúdaigh d’uimhir PIN go cúramach',
 'Club Aclaíochta na Cathrach\nRanganna, Gach Satharn\n9.30 – 11.30',
 'Coiste Glas na Scoile\nSábháil leictreachas\nMúch na soilse i do dhiaidh',
 'An Ciorcal Comhrá ar ceal anocht\nNíl an córas teasa ag obair san fhoirgneamh',
 'Aonad Timpistí agus Éigeandála\nNá páirceáil anseo',
 'Oifig rúnaí na scoile\nBrúigh an cloigín\nFan go nglaofar ort',
 'Seirbhís Pas\nGrianghraf do do phas ar fáil anseo',
 'Ag pacáil málaí\nOllmhargadh SuperValu\nBailiúchán do Focus Ireland']
    for i,(sign,answer) in enumerate(zip(signs,'GEJBIDFCAH'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cathain a d’fhreastail Áine ar an agallamh?', '9 Meán Fómhair | 11 Meán Fómhair | 22 Meán Fómhair', '9 Meán Fómhair'),
         ('Cén spórt a imríonn Áine lena club áitiúil anois?', 'Cispheil | Camógaíocht | Peil na mban', 'Peil na mban'),
         ('Cá raibh Áine ag obair i mí Iúil?', 'Sa chlub reathaíochta | Ar champa spóirt | Sa linn snámha phoiblí', 'Ar champa spóirt'),
         ('Cad a thaispeánfaidh Áine do dhaoine sa halla aclaíochta ar maidin?',
          'Clár aclaíochta | Conas na fearais a úsáid i gceart | Snámh',
          'Conas na fearais a úsáid i gceart'),
         ('Cad atá ar fáil ar shuíomh gréasáin an ionaid?', 'Ríomhphost | An tairiscint | Clár na n-imeachtaí', 'Clár na n-imeachtaí')]),
 '2B': (7,
        'brochure',
        [('Cá bhfuil Contae Loch Garman suite?',
          'Ar Mhór-Roinn na hEorpa | In oirdheisceart na hÉireann | I Meiriceá',
          'In oirdheisceart na hÉireann'),
         ('Conas a thagann cuairteoirí ón bhFrainc go calafort Ros Láir?',
          'Ar na báid farantóireachta | Ar eitleán | Ar bhusanna',
          'Ar na báid farantóireachta'),
         ('Cad a bronnadh ar thrá Churrach Cló?', 'Bruscar | Bratach Ghorm | Cosán siúlóide', 'Bratach Ghorm'),
         ('Cá gcaitheann na géanna fiáine an geimhreadh?',
          'I dTeach Solais Rinn Duáin | Sa Pháirc Náisiúnta Oidhreachta | Ar Shlabaí Loch Garman',
          'Ar Shlabaí Loch Garman'),
         ('Cad a bhíonn ar siúl i mbaile Loch Garman i mí Dheireadh Fómhair gach bliain?',
          'Féile cheoldrámaíochta | Féile scríbhneoireachta | Féile ealaíne',
          'Féile cheoldrámaíochta')]),
 '2C': (8,
        'news',
        [('Cad a bhí taobh istigh den phacáiste?', 'Scríbhinn | Uaireadóir óir | Féar', 'Uaireadóir óir'),
         ('Cad a shocraigh na cailíní a dhéanamh leis an bpacáiste?',
          'É a thabhairt do na Gardaí | É a choimeád | An t-úinéir a aimsiú',
          'An t-úinéir a aimsiú'),
         ('Conas a cuireadh an scéala amach an tráthnóna sin?',
          'Ar an raidió áitiúil | Ar Leathanach Facebook Cháit | Ar Leathanach Facebook Úna',
          'Ar an raidió áitiúil'),
         ('Cathain a tháinig an glaoch isteach ón mbean?', 'An tráthnóna céanna | An lá dár gcionn | Tar éis cúpla lá', 'Tar éis cúpla lá'),
         ('Cad a thug an bhean don bheirt chailíní?', 'Pacáiste | Cárta buíochais | Ríomhaire', 'Cárta buíochais')]),
 '3A': (9,
        'news',
        [('Cén spórt inar bhain Sam Bennett cáil amach?', 'Rámhaíocht | Galf | Rothaíocht', 'Rothaíocht'),
         ('Cén áit ar tógadh Sam Bennett?', 'Sa Bheilg | I gCarraig na Siúire | In Marseille', 'I gCarraig na Siúire'),
         ('Cén comórtas rothaíochta a bhuaigh Sam Bennett dhá bhliain as a chéile?',
          'An Tour de France | Craobh na hÉireann faoi 23 | Rás Tailteann',
          'Craobh na hÉireann faoi 23'),
         ('Cén mí-ádh a bhí ar Sam go luath sa Tour de France sa bhliain 2016?', None, 'Bhris sé méara a lámh de bharr timpiste'),
         ('Cén geansaí a bhuaigh Sam i bPáras in 2020?', 'Geansaí Buí | Geansaí Glas | Geansaí Dearg', 'Geansaí Glas')]),
 '3B': (10,
        'extract',
        [('Cén áit i mBaile Átha Cliath a bhfuil EPIC, Músaem Eisimirice na hÉireann?',
          'Ar Fhaiche an Choláiste | Ar Shráid an Dáma | I gCeantar na nDugaí',
          'I gCeantar na nDugaí'),
         ('Cé mhéad gailearaí atá sa mhúsaem?', '20 | 300 | 500', '20'),
         ('Cén fáth ar fhág na céadta míle duine Éire idir na blianta 1845 agus 1849?',
          'Mar mhisinéirí | De bharr an Ghorta Mhóir | Chun dul ag troid i gcogaí',
          'De bharr an Ghorta Mhóir'),
         ('Cad a úsáidtear chun an cuairteoir a chur i ról lárnach i ngach gailearaí?',
          'Aisteoirí | Na meáin idirghníomhacha | Litreacha',
          'Na meáin idirghníomhacha'),
         ('Cad is gá don chuairteoir a dhéanamh i ngach gailearaí?', None, 'Clárú isteach')]),
 '3C': (11,
        'poem',
        [('Cár thuirling an file sa chéad véarsa?', 'Ar an saol mar atá | Ar an saol mar a bhí | Ar an urlár', 'Ar an saol mar a bhí'),
         ('Cén áit a raibh an t-áiléar?', 'Faoi dhíon an tí | Ar an urlár | I mbosca', 'Faoi dhíon an tí'),
         ('Cad a bhí sáite i mbosca san áiléar le fiche bliain?', 'Cóipleabhair | Leabhar | Grianghraif', 'Grianghraif'),
         ('Cad a bhí san áiléar a briseadh fadó?', 'Bréagán | Dréimire | Peann', 'Bréagán'),
         ('Cad a thit ar an bhfile agus é ag teacht anuas ón áiléar?', None, 'An aois')])}
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
                assert comparable(accepted) in comparable(scheme[4 if slot[0]=='2' else 5].get_text()), (slot,i,accepted)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],[5 if slot[0]=='2' else 6],
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            if slot == '3A' and i == 4:
                card['criteria'][0]['permittedMarks'] = [0,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Bhris sé méara a lámh; Bhí mí-ádh air de bharr timpiste a tharla dó; Timpiste.',
                    '4 mharc: Bhí mí-ádh air de bharr timpiste; Bhris sé a lámh.',
                    '3 mharc: Chríochnaigh sé san áit dheireanach; Bronnadh an Lóchrann Dearg air.']
            if slot == '3B' and i == 5:
                card['criteria'][0]['guidance'] += [
                    'Clárú = 6 mharc. Is gá don chuairteoir clárú isteach i ngach gailearaí = 6 mharc.',
                    'Faigheann gach cuairteoir pas ag dul isteach sa mhúsaem. Is gá don chuairteoir clárú isteach i ngach gailearaí = 6 mharc.']
            if slot == '3C' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,4,6]
                card['criteria'][0]['guidance'] += [
                    'Líne 2 agus Líne 3 as an véarsa deireanach: Iomarcaíocht 6-2 = 4 mharc.',
                    'Líne 3 agus Líne 4 as an véarsa deireanach: Iomarcaíocht 6-2 = 4 mharc.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2021 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2021 FL ','')+'\n'+c['questionText'] for c in members),
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
        'Sármhaith 9–11; An-mhaith 7–8; Maith 5–6; Maith go leor 3–4; Lag 2; An-lag 1; Easnamhach 0.',
        'Dul na Gaeilge: struchtúr na Gaeilge agus beachtas gramadaí. Foclóir: cruinneas agus oiriúnacht foclóra. Litriú.',
        'Bronn marc as 11 ar chaighdeán na Gaeilge san iarracht iomlán.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme[p-1].get_text())) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am?\nCén t-aoi speisialta a bheidh i láthair?\nCad a dhéanfar leis an airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',10,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',5,[notice_p9.split('Pictiúr 3',1)[1]]),
            criterion('pictiur4','Pictiúr 4',5,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),copy.deepcopy(language)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared language mark. Follow the exact 2021 partial-credit and date/name-only rules within the affected picture awards. Required headings are not choices.')
    letter = add('W-4B','3','Scríobh · Ceist 4(b)',
        'Féach ar na pictiúir thíos.\n\nChaith tú féin agus do chairde seachtain i dteach saoire cois farraige.\nScríobh litir chuig do dheartháir / do dheirfiúr i gCeanada ag insint dó / di:\n\n'
        '- Faoin bpóstaer don teach saoire a chonaic sibh (dhá phointe eolais) — Pictiúr 1\n'
        '- Faoin teach saoire agus faoi na háiseanna sa teach (dhá phointe eolais) — Pictiúr 2\n'
        '- Faoi na rudaí a rinne sibh gach lá (dhá rud) — Pictiúr 3\n'
        '- Faoi na rudaí a rinne sibh gach oíche (dhá rud) — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('seoladh','Seoladh',2,['Dhá chuid (1 + 1), as Gaeilge. Glac lena leithéid de “Bóthar Crumlin” nó “Sráid Patrick”. Ná glac le hainm an bhaile i mBéarla.']),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('beannu','Beannú',1,['Ainm ar bith, fiú a chara.']),
            criterion('crioch','Críoch / Slán',2,['Dhá chuid ag teastáil: Slán … agus ainm.']),
            *[criterion(f'pictiur{i}',f'Pictiúr {i} · '+('dhá phointe eolais' if i<3 else 'dhá rud'),7,
                [scheme_guidance(12,12)[0].split(f'Pictiúr {i}',1)[1].split(f'Pictiúr {i+1}',1)[0].split('Cuir tic',1)[0]]) for i in range(1,5)],
            copy.deepcopy(language)],
        ['Scríobh litir chuig do dheartháir nó do dheirfiúr i gCeanada faoin saoire.',
         'Dhá phointe eolais faoi gach ceann de na ceithre phictiúr; leagan amach cuí.'],
        'The letter stays whole: six layout marks, four seven-mark picture awards (4 + 3 for two points), and one shared eleven-mark language award. Two open information points per picture are not a closed printed menu. There is no word-count penalty in the published letter scheme.', additionalTopicIds=['irish-2-8'])
    # Mechanically expand the two printed recipients; all letter criteria stay whole.
    cards.remove(letter)
    for recipient in ['dearthair','deirfiur']:
        route=copy.deepcopy(letter)
        route['id'] += '-'+recipient
        route['atlasQuestionId'] += '-'+recipient
        route['conceptId'] += '-'+recipient
        label='do dheartháir' if recipient == 'dearthair' else 'do dheirfiúr'
        route['questionRef'] += ' · '+label
        route['questionText'] += '\n\nAn rogha don chárta seo: litir chuig '+label+'.'
        cards.append(route)

    stories=[]
    for slot,page,end,title in [('5A',16,14,'Cuntas'),('5B',17,16,'Eachtra')]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí Béárbaiciú sa bhaile agat le do chairde.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin mBéárbaiciú sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nBéárbaiciú sa Bhaile'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo nuair a bhí tú féin agus do chara san ionad siopadóireachta.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEachtra a Tharla'
        )
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(13 if slot=='5A' else 14,end+1)),[
                criterion('cumarsaid','Cumas Cumarsáide',34,[
                    scheme_guidance(13,13)[0].split('Ceist 5 (a)',1)[-1],
                    scheme_guidance(14,14)[0].split('Cruinneas Gaeilge',1)[0],
                ] if slot == '5A' else [
                    scheme_guidance(15,15)[0],
                    scheme_guidance(16,16)[0].split('Cruinneas Gaeilge',1)[0],
                ]),
                copy.deepcopy(language),
                criterion('length','Fad',4,['80–90 focal: 0; 60–79: −2; 30–59: −3; <30: −4.'],deduct_from='cumarsaid')],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'References in the scheme are indicative, not a closed selection pool. One shared communication award and one language award cover the whole response. The communication ceiling is reduced by four per missing reference. For 5(b), cover each of the four pictures plus a fifth detail. Apply the word-count penalty only within communication.'))
    # The 2021 paper selects ONE writing response: no paired writing routes.
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==65 and len({c['id'] for c in cards})==65
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2021,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,25)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writing=45,total=315),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and letter picture instructions are compulsory context. One language award covers each whole response; the two printed letter recipients are separately expanded.',
            'The two information points in each letter picture and source-retrieval answers are content choices, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 5 whole writing routes including two letter recipients; 6 paired reading routes; no paired writing routes.',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2021 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2021-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2021: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
