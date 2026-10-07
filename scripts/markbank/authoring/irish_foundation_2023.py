#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2023 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2023-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2023-source-review.json'

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2023/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2023/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '63e6c61769a22b1420822ff37a379ea8d9ccc7fc3b73fa42d34fae175528aaac', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '329234acc3dd24894a9ed50c1ab163a9265e4cc11b6c3894c7fb6aacda7f7338', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2023-fl-{key.lower()}', year=2023, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2023 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2023 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [
      ('1a',3,7,'Cén post atá ag athair Chiara?',None,'Tógálaí = an chéad phictiúr'),
      ('1b',3,7,'Cén rud a bhfuil an-spéis ag Ciara ann?','Ainmhithe | Obair thógála | Dul chuig Coláiste na Tríonóide','Ainmhithe'),
      ('2a',3,7,'Cárbh as do Shéamus ó dhúchas?',None,'Co. Phort Láirge = an ceathrú pictiúr'),
      ('2b',3,7,'Cén duine a bhíonn ag cócaireacht?','Séamus | Anna | Billy','Billy'),
      ('3',4,8,'Cá bhfuil an fear ag dul?',None,'Staid pheile = an tríú pictiúr'),
      ('4',4,8,'Cá bhfuil an mheánscoil? (Cuir tic (✓) sa bhosca ceart.)',None,'An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)'),
      ('5a',4,8,'Cad a bheidh ar siúl?',None,'Cluiche sacair = an chéad phictiúr'),
      ('5b',4,8,'Cén teocht is ísle a bheidh ann amárach?','23° Celsius | 29° Celsius | 31° Celsius','23 céim Celsius nó 29 céim Celsius'),
      ('6a',5,10,'Cén fáth nach bhfuil a Daid sásta le Laoise?','Tá a pictiúr ar Instagram. | Tá fáinne ina srón aici. | Fuair sí fáinne cluaise eile.','Fuair sí fáinne cluaise eile nó Tá fáinne ina srón aici'),
      ('6b',5,10,'Cé mhéad a chosnóidh an turas scoile?','€40 | €750 | €1,000','€750'),
      ('7a',5,10,'Cá háit a raibh Máire ar saoire?','Ar Inis Mór | I Ros an Mhíl | I gCathair na Gaillimhe','Ar Inis Mór'),
      ('7b',5,10,'Conas a thaistil Máire ar ais go Cathair na Gaillimhe?','Ar an eitleán | Ar an mbád | Ar an rothar','Ar an mbád'),
      ('8a',5,10,'Cá háit a raibh Rian ag an gCáisc?','I mBaile Átha Cliath | In Birmingham Shasana | I mBeirlín sa Ghearmáin','I mBeirlín sa Ghearmáin'),
      ('8b',5,10,'Cad a cheannaigh Rian dá chailín?','Bráisléad | Geansaí | Cúpla t-léine','Bráisléad'),
    ]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2023/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2023 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))

    signs = [
      'Club Gailf\nFáilte roimh dhéagóirí\nCláraigh anois',
      'Ranganna Damhsa\nGach Déardaoin\n€50 ar théarma sé seachtaine',
      'Seachain an Madra\nFan amach',
      'Carr ar díol\nDath dubh, bliain 2018\nGlaoigh ar 01 548 9321',
      'Ceachtanna gluaisrothair\nAr fáil\nEolas: ceachtannagluaisrothair.ie',
      'Saotharlann Eolaíochta\nCosc ar bhia agus ar dheoch',
      'Bóthar dúnta\nMalairt slí romhat\nLean na comharthaí',
      'Radharceolaí\nTástáil súl ar €15.00 an duine\nSpéaclaí dearthóra ar fáil',
      'Club peile\nBuachaillí agus cailíní\nTraenáil gach Satharn',
      'Ceolchoirm\nChun cabhrú le teifigh ón Úcráin\nDé Sathairn i Halla an Phobail',
    ]
    for i,(sign,answer) in enumerate(zip(signs,'IDBGHJFCEA'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[6],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {
      '2A':(7,'letterReading',[
        ('Cá háit a bhfuil An Bia Blasta suite?','Thar lear | Inse Chór, Baile Átha Cliath | Dún Búinne, Co. na Mí','Dún Búinne, Co. na Mí'),
        ('Cén t-ábhar ina bhfuair Seán grád H1?','San Eacnamaíocht Bhaile | Sa Mhatamaitic | San Ealaín','San Eacnamaíocht Bhaile'),
        ('Cá raibh Seán ag obair an samhradh seo caite?','Sa chaifé An Cupán Tae | Ag cuntar an deilí san ollmhargadh | Sa bhialann An Bia Blasta','Ag cuntar an deilí san ollmhargadh'),
        ('Cén scil chócaireachta ar leith atá ag Seán?','Dinnéar a réiteach | Milseoga deasa a chruthú | Cístí a bhácáil','Milseoga deasa a chruthú'),
        ('Cathain a bheidh Seán sásta freastal ar agallamh?','12 Bealtaine 2023 | An mhí seo chugainn | Am ar bith','Am ar bith')]),
      '2B':(8,'brochure',[
        ('Cad faoi atá an scéal sa scannán An Cailín Ciúin?','Faoin samhradh | Faoi Chontae Phort Láirge | Faoi chailín óg','Faoi chailín óg'),
        ('Cén pháirt atá ag Catherine Clinch sa scannán?','Eibhlín | Cáit | Seán','Cáit'),
        ('Cá háit ar taispeánadh An Cailín Ciúin i dtosach?','In Hollywood | I mBeirlín na Gearmáine | Sa Rinn, Co. Phort Láirge','I mBeirlín na Gearmáine'),
        ('Cé mhéad gradam IFTA a bronnadh ar An Cailín Ciúin?','3 | 8 | 9','8'),
        ('Cad a bhí ar siúl in Hollywood an t-earrach seo caite?','Oíche na ngradam Oscar | Oíche na ngradam IFTA | An Cailín Ciúin','Oíche na ngradam Oscar')]),
      '2C':(9,'news',[
        ('Cén t-am a thosaigh an stoirm mhór ag séideadh?','Ar a naoi a chlog ar maidin | Ar a deich a chlog ar maidin | Ag meán lae','Ar a deich a chlog ar maidin'),
        ('Cén fáth nár ghlaoigh na múinteoirí ar na seirbhísí slándála?','Bhí siad scanraithe. | Bhí siad ar foscadh. | Ní raibh na fóin ag obair.','Ní raibh na fóin ag obair'),
        ('Cá háit ar thiomáin an feirmeoir ag lorg cabhrach?','Go dtí stáisiún na nGardaí. | Go dtí an t-ionad pobail. | Go dtí an stáisiún dóiteáin.','Go dtí stáisiún na nGardaí'),
        ('Cé a chinntigh go raibh gach duine ceart go leor?','Na múinteoirí | Na Gardaí | Dochtúir agus altra','Dochtúir agus altra'),
        ('Cén fáth a raibh na tuismitheoirí buíoch?','Bhí dochtúir ann. | Bhí a bpáistí slán sábháilte. | Bhí stoirm mhór ann.','Bhí a bpáistí slán sábháilte.')]),
      '3A':(10,'news',[
        ('Cén bhliain a rugadh Gearóid Hegarty?','1994 | 2015 | 2018','1994'),
        ('Cén spórt inar bhuaigh Gearóid ceithre bhonn uile-Éireann?','Rugbaí | Iomáint | Peil Ghaelach','Iomáint'),
        ('Cá háit ar fhreastail Gearóid ar an ollscoil?','I nGaillimh | I gCorcaigh | I Luimneach','I Luimneach'),
        ('Cé mhéad gradam All-Star atá bainte amach ag Gearóid?','2 | 3 | 4','3'),
        ('Luaigh tréith amháin atá i nGearóid Hegarty.',None,'Sciliúil / láidir / tapa / cabhrach / cairdiúil')]),
      '3B':(11,'extract',[
        ('Cén post atá ag Eimear le TG4 anois?','Iriseoir ceoil | Príomhláithreoir nuachta | Iriseoir spóirt','Príomhláithreoir Nuachta'),
        ('Cá háit ar fhreastail Eimear ar an meánscoil?','Sa Spidéal | Sa Ghaillimh | Ar oileáin Árann','Sa Spidéal'),
        ('Cad iad na hábhair atá ag Eimear ina céim ollscoile?','Ceol agus drámaíocht | Gaeilge agus Gearmáinis | Spórt','Gaeilge agus Gearmáinis'),
        ('Cén bhliain a raibh an chéad díospóireacht toghcháin as Gaeilge ar TG4?','2000 | 2006 | 2011','2011'),
        ('Cén rud a bhfuil an-spéis ag Eimear ann?',None,'Taisteal / Thar lear / Meiriceá (Theas) / Eoraip / Áise / Saoire / (oileán) Árann')]),
      '3C':(12,'poem',[
        ('Cá háit a raibh Daideo ina shuí?','Sa scoil | Sa chistin | Taobh amuigh','Sa Chistin'),
        ('Cad atá imithe ar strae, dar le Daideo?','An raidió | An ceannaire | An domhan','An domhan'),
        ('Cé a bhí ag ullmhú bhéile an tráthnóna?','Daideo | Mamó | An ceannaire','Mamó'),
        ('Cén áit a raibh an saol ina chíor thuathail?','Taobh amuigh | Sa chistin | Sa scoil','Taobh amuigh'),
        ('Cé leis a raibh an snag breac ag argóint?',None,'Le spideog')]),
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
            for accepted in answer.split(' / '):
                assert comparable(accepted) in comparable(scheme[4 if slot[0]=='2' else 5].get_text()), (slot,i,accepted)
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
                c['label']=member['questionRef'].replace('2023 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2023 FL ','')+'\n'+c['questionText'] for c in members),
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
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',5,[notice_p9.split('Pictiúr 3',1)[1]]),
            criterion('pictiur4','Pictiúr 4',5,[notice_p10.split('Pictiúr 4',1)[1].split('N.B.',1)[0]]),copy.deepcopy(language)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared language mark. Apply each −1 past-tense penalty within the affected picture award. Required headings are not choices.')
    letter = add('W-4B','3','Scríobh · Ceist 4(b)',
        'Féach ar na pictiúir thíos.\n\nBhí post páirtaimseartha agat in óstán.\nScríobh litir chuig do chara ag insint dó/di:\n\n'
        '- Faoin óstán a raibh tú ag obair ann (dhá phointe eolais) — Pictiúr 1\n'
        '- Faoi na daoine a bhíonn san óstán (dhá phointe eolais) — Pictiúr 2\n'
        '- Faoin obair a rinne tú san óstán (dhá phointe eolais) — Pictiúr 3\n'
        '- Faoi na rudaí a rinne tú nuair a bhíodh lá saor agat (dhá phointe eolais) — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('seoladh','Seoladh',2,['Dhá chuid (1 + 1), as Gaeilge. Glac lena leithéid de “Bóthar Crumlin” nó “Sráid Patrick”. Ná glac le hainm an bhaile i mBéarla.']),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('beannu','Beannú',1,['Ainm ar bith, fiú a chara.']),
            criterion('crioch','Críoch / Slán',2,['Dhá chuid ag teastáil: Slán … agus ainm.']),
            *[criterion(f'pictiur{i}',f'Pictiúr {i} · dhá phointe eolais',7,
                [scheme_guidance(12,12)[0].split(f'Pictiúr {i}',1)[1].split(f'Pictiúr {i+1}',1)[0].split('Cuir tic',1)[0]]) for i in range(1,5)],
            copy.deepcopy(language)],
        ['Scríobh litir chuig do chara faoi do phost san óstán.',
         'Dhá phointe eolais faoi gach ceann de na ceithre phictiúr; leagan amach cuí.'],
        'The letter stays whole: six layout marks, four seven-mark picture awards (4 + 3 for two points), and one shared eleven-mark language award. Two open information points per picture are not a closed printed menu. There is no word-count penalty in the published letter scheme.', additionalTopicIds=['irish-2-8'])

    stories=[]
    for slot,page,end,title in [('5A',16,13,'Cuntas'),('5B',17,15,'Eachtra')]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ar Saoire in Ionad Campála an samhradh seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin tsaoire sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nSaoire in Ionad Campála'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nChuaigh tú chuig cluiche i bPáirc an Chrócaigh le do chara.\nTá tú chun scríobh faoi seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin gcluiche i bPáirc an Chrócaigh (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nCluiche i bPáirc an Chrócaigh'
        )
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(13 if slot=='5A' else 14,end+1)),[
                criterion('cumarsaid','Cumas Cumarsáide',34,[paragraph.split('Cruinneas Gaeilge',1)[0] for paragraph in scheme_guidance(13 if slot=='5A' else 14,end)]),
                copy.deepcopy(language),
                criterion('length','Fad',4,['80–90 focal: 0; 60–79: −2; 30–59: −3; <30: −4.'],deduct_from='cumarsaid')],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'References in the scheme are indicative, not a closed selection pool. One shared communication award and one language award cover the whole response. The scheme requires a reference to each of the four pictures plus another detail for 5(b).'))
    writing={'4A':[notice],'4B':[letter],'5A':[stories[0]],'5B':[stories[1]]}
    for a,b in itertools.combinations(writing,2):
        for left,right in itertools.product(writing[a],writing[b]):
            combine('W-'+a+'-'+b,'Scríobh · '+left['questionRef'].removeprefix('2023 FL Scríobh · ')+' + '+right['questionRef'].removeprefix('2023 FL Scríobh · '),
                [left,right], 'Freagair dhá cheist ar bith as na ceithre cinn seo a leanas: 4 (a), 4 (b), 5 (a) nó 5 (b).')

    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==70 and len({c['id'] for c in cards})==70
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2023,level='foundation',paperFileid=FILE+'.pdf',
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
            'All notice headings and letter picture instructions are compulsory context. One language award covers each whole response.',
            'The two information points in each letter picture and the retrieved trait in Q3A(5) are content answers, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 4 whole writing responses; 6 paired reading routes; 6 paired writing routes.',
        caveats=['Foundation 2023 only. Other years remain pending.',
                 'The SEC accepts two alternatives for aural Q5(b) and Q6(a); each remains one task.',
                 'The letter has no published word-count penalty; keep all four picture instructions and one shared language award.',
                 'Preserve the Tagairt NR/-12 headings beside the explicit 34,30,26,22,18,14 communication caps. Do not invent an extra automatic deduction from the abbreviated heading.'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2023 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2023-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2023: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
