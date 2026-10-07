#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2019 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2019-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2019-source-review.json'

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2019/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2019/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '9dee183d256f38953d14021ace3e6ef399ac90f67ad32ea27b58f8ccecbb81d3', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == 'c95192c5d9379c44ddc109ae3737f178ef5464bb1650b1357e3da1aef78f5d4e', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2019-fl-{key.lower()}', year=2019, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2019 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2019 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cá bhfuair Seán a chéad phost?', None, 'Ag obair ar fheirm = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cén rud is fearr le Seán faoin obair san ionad garraíodóireachta?',
  'Tá an pá go maith | Bíonn sé amuigh faoin aer gach lá | Bíonn sé gnóthach gach lá',
  'Bíonn sé amuigh faoin aer gach lá'),
 ('2a', 2, 7, 'Cá bhfuil Deirdre ag obair?', None, 'Altra in ospidéal = an dara pictiúr'),
 ('2b',
  2,
  7,
  'Cathain a chuaigh Deirdre go dtí an Iodáil ag sciáil?',
  'An deireadh seachtaine seo caite | I mí na Bealtaine | Tar éis na Nollag',
  'Tar éis na Nollag'),
 ('3', 3, 8, 'Cá bhfuil an fear ag dul?', None, 'Siopa leabhar = an ceathrú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil an siopa troscáin? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)'),
 ('5a',
  3,
  8,
  'Conas a bheidh an aimsir oíche Dé Sathairn?',
  None,
  'Titim throm sneachta = an ceathrú pictiúr'),
 ('5b',
  3,
  8,
  'Cad a bheidh ar oscailt maidin Dé Domhnaigh?',
  'Na haerfoirt | Gach stáisiún traenach | Gach stáisiún bus',
  'Na haerfoirt'),
 ('6a',
  4,
  10,
  'Cén mhí a raibh Eilís ag tabhairt aire dá deirfiúr óg?',
  'Mí an Mheithimh | Mí Iúil | Mí Lúnasa',
  'Mí an Mheithimh'),
 ('6b',
  4,
  10,
  'Cén áit i mBaile Átha Cliath a raibh an cheolchoirm ar siúl?',
  'I nDún Droma | I bPáirc Mharlaí | I Mullach Íde',
  'I bPáirc Mharlaí'),
 ('7a',
  4,
  10,
  'Cá mbeidh Nóra ag dul tráthnóna amárach?',
  'Chuig bainis | Ag siopadóireacht | Chuig scannán',
  'Ag siopadóireacht'),
 ('7b',
  4,
  10,
  'Cén rud nach bhfuil ag Nóra?',
  'Ríomhaire glúine | Cód poist | Cárta creidmheasa',
  'Cárta creidmheasa'),
 ('8a',
  4,
  10,
  'Cad a bheidh ar siúl oíche Dé Sathairn?',
  'Tráth na gCeist Boird | Seó faisin | Dráma',
  'Tráth na gCeist Boird'),
 ('8b', 4, 10, 'Cén táille a bheidh le híoc ag gach foireann?', '€2 | €5 | €20', '€20')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2019/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2019 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Ceachtanna tiomána ar fáil\n€40 an ceacht\nGlaoigh ar 086 261873',
 'Spórtlann an Bhaile\nRanganna aclaíochta\nGach Máirt: 8 p.m. - 9 p.m.',
 'An tIonad Athchúrsála\nÚsáid na boscaí cearta',
 'An Luas\nAmchlár speisialta\ndo thréimhse na Nollag',
 'Rialacha na Scoile\nCoimeád an fón póca\nsa taisceadán',
 'Ciorcal Comhrá\nCuir feabhas ar do chuid Gaeilge\nGach Aoine - 7.30 p.m.',
 'Maratón na cathrach ar siúl\nBóthar dúnta',
 'Oíche Shamhna\nComórtas bréigéide\nDuaiseanna le buachan',
 'Siopa an bhláthadóra\nBláthanna do gach ócáid',
 'Ionad fiaclóireachta\nDéan coinne ag an deasc fáilte']
    for i,(sign,answer) in enumerate(zip(signs,'HDBFCAIJEG'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cén dáta a chuaigh Róisín faoi agallamh in oifigí RTÉ Raidió na Gaeltachta?',
          '30 Bealtaine | 4 Meitheamh | 2 Iúil',
          '30 Bealtaine'),
         ('Cad a mhúineann Róisín do pháistí bunscoile?',
          'An bosca ceoil | An fhidil | An fheadóg stáin',
          'An fheadóg stáin'),
         ('Cén post atá á thairiscint ag RTÉ Raidió na Gaeltachta do Róisín?',
          'Teicneoir fuaime | Láithreoir | Stiúrthóir ceoil',
          'Láithreoir'),
         ('Cá bhfuil an stiúideo ina ndéanfar an clár a thaifeadadh?',
          'Baile na nGall | Casla | Lios Póil',
          'Baile na nGall'),
         ('Cén lá a chraolfar an clár ar RTÉ Raidió na Gaeltachta?',
          'Déardaoin | Gach Aoine | Gach Domhnach',
          'Gach Domhnach')]),
 '2B': (7,
        'brochure',
        [('Cén contae ina bhfuil Gaeltacht Ghaoth Dobhair?',
          'Co. Chiarraí | Co. Dhún na nGall | Co. na Gaillimhe',
          'Co. Dhún na nGall'),
         ('Cén grúpa daoine a labhraíonn an Ghaeilge gach lá?',
          'Muintir na háite | Foghlaimeoirí fásta | Scoláirí dara leibhéal',
          'Muintir na háite'),
         ('Cad is féidir leis an dreapadóir a dhéanamh?',
          'An Earagail a dhreapadh | Imeachtaí uisce | Galf a imirt',
          'An Earagail a dhreapadh'),
         ('Cá bhfuil na gairdíní áille?',
          'In Ionad na gCuairteoirí | Sna taispeántais | Timpeall ar an gcaisleán',
          'Timpeall ar an gcaisleán'),
         ('Cá mbíonn drámaí ar stáitse?',
          'Sna bialanna | San amharclann áitiúil | Sna tithe tábhairne',
          'San amharclann áitiúil')]),
 '2C': (8,
        'news',
        [('Cén obair bhaile a rinne Orlaith maidin Dé Máirt?',
          'Bitheolaíocht | Matamaitic | Béarla',
          'Matamaitic'),
         ('Cén t-am a thosaigh na ranganna?', '7 a.m. | 8.15 a.m. | 9 a.m.', '9 a.m.'),
         ('Cad a fuair Orlaith ó rúnaí na scoile?', 'Iasacht airgid | Obair bhaile | Lón', 'Iasacht airgid'),
         ('Cá raibh an bosca bruscair?', 'Sa charr | San ollmhargadh | Ar an gcosán', 'Ar an gcosán'),
         ('Thug Orlaith an nóta cúig euro …',
          'Don bhean | Don seanfhear | Do rúnaí na scoile',
          'Don bhean')]),
 '3A': (9,
        'news',
        [('Cén spórt a imríonn Jonathan Sexton?', 'Rugbaí | Dornálaíocht | Rámhaíocht', 'Rugbaí'),
         ('Cathain a d’fhill Jonathan Sexton ar fhoireann Chúige Laighean?', '2006 | 2009 | 2015', '2015'),
         ('Cad é an bua is mó atá ag Jonathan?',
          'Tá sé tapa | Tá sé ábalta scóráil le ciceanna pionóis | Tá sé cliste',
          'Tá sé ábalta scóráil le ciceanna pionóis'),
         ('Cén mhí a raibh an bua stairiúil ag foireann na hÉireann ar fhoireann na Nua-Shéalainne?',
          'Mí an Mhárta | Mí na Bealtaine | Mí na Samhna',
          'Mí na Samhna'),
         ('Cad ba bhreá le Jonathan a bhuachan i mbliana?', None, 'Corn an Domhain sa rugbaí')]),
 '3B': (10,
        'extract',
        [('Cá bhfuil Gaeltacht Ráth Chairn suite?',
          'Contae Phort Láirge | Contae na Mí | Contae Chiarraí',
          'Contae na Mí'),
         ('Cad a tharla sa bhliain 1935?', None, 'Tháinig daoine ó Chonamara chun cónaithe i Ráth Chairn'),
         ('Cá gcuirtear na drámaí ar stáitse?',
          'Sa leabharlann | Sa teach tábhairne | I halla an phobail',
          'I halla an phobail'),
         ('Cén mhí a mbíonn Féile na Gealaí ar siúl?',
          'Mí an Mhárta | Mí an Mheithimh | Mí na Samhna',
          'Mí an Mheithimh'),
         ('Conas is féidir ticéad a cheannach don fhéile?',
          'Ar líne | I Ráth Chairn | Ar an raidió',
          'Ar líne')]),
 '3C': (11,
        'poem',
        [('Cad atá ina sheasamh sa pháirc ar chúl an ghairdín?', 'Capall | Préachán | Crann', 'Crann'),
         ('Cad atá faoi bhun an chrainn?', 'Nead | Fréamhacha | Géaga', 'Fréamhacha'),
         ('Cad a bhíonn ag fás ar an gcrann san earrach?',
          'Bachlóga | Duilleoga glasa | Cnónna donna',
          'Bachlóga'),
         ('Cathain a thiteann na cnónna donna?', 'Sa samhradh | San fhómhar | Sa gheimhreadh', 'San fhómhar'),
         ('Cá fhad atá an crann seo ann?', None, 'Ní fios cá fhad atá sé ann')])}
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
            if slot == '3A' and i == 5:
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Corn an Domhain; Corn an Domhain sa rugbaí le foireann na hÉireann; Corn an Domhain le foireann na hÉireann.']
            if slot == '3B' and i == 2:
                card['criteria'][0]['permittedMarks'] = [0,2,4,6]
                card['criteria'][0]['guidance'] += [
                    '4 mharc: Tháinig daoine chun cónaithe i Ráth Chairn.',
                    '2 mharc: Tháinig daoine ó Chonamara chun cónaithe; Tháinig daoine ó Chonamara.']
            if slot == '3C' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Leathchéad bliain ar a laghad; Líne 1, Líne 2 agus Líne 3 as Véarsa 3 le chéile.',
                    '4 mharc: Leathchéad bliain / Caoga bliain; An véarsa iomlán (iomarcaíocht 6 - 2).',
                    '3 mharc: Bhí sé ann nuair a bhí mise óg.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2019 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2019 FL ','')+'\n'+c['questionText'] for c in members),
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
            'Dul na Gaeilge: struchtúr na Gaeilge agus beachtas gramadaí. Foclóir: cruinneas agus oiriúnacht foclóra. Litriú.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'The band table on PDF page16 belongs only to the modified marking scheme. Do not apply it as the standard language rubric.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme[p-1].get_text())) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Cead isteach?\nCén t-aoi speisialta a bheidh i láthair?\nCad a dhéanfar leis an airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,['Sinéad Aherne (Pictiúr 3).',notice_p9.split('Pictiúr 3',1)[1],notice_p10.split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2019 activity/place partial credit, date, fee and guest-name rules within the affected picture awards. Required headings are not choices.')
    letter = add('W-4B','3','Scríobh · Ceist 4(b)',
        'Féach ar na pictiúir thíos.\n\nBhí tú ag cluiche mór i bPáirc an Chrócaigh le déanaí. Scríobh litir chuig do dheartháir / do dheirfiúr i Londain ag insint dó / di:\n\n'
        '- Faoin bpóstaer a chonaic tú (dhá phointe eolais) — Pictiúr 1\n'
        '- Faoin turas go dtí an cluiche (dhá phointe eolais) — Pictiúr 2\n'
        '- Faoin gcluiche (dhá phointe eolais) — Pictiúr 3\n'
        '- Faoi na rudaí a rinne tú nuair a bhí an cluiche thart (dhá phointe eolais) — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('seoladh','Seoladh',2,['Dhá chuid (1 + 1), as Gaeilge. Glac le Bóthar Crumlin / Sráid Patrick. Ná glac le hainm an bhaile i mBéarla.']),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('beannu','Beannú',1,['Ainm ar bith nó a dheartháir, a dheirfiúr, a chara.']),
            criterion('crioch','Críoch / Slán',2,['Dhá chuid ag teastáil: Slán agus ainm.']),
            *[criterion(f'pictiur{i}',f'Pictiúr {i} · dhá phointe eolais',6,
                [scheme_guidance(12,12)[0].split(f'Pictiúr {i}',1)[1].split(f'Pictiúr {i+1}',1)[0].split('Cruinneas Gaeilge',1)[0]]) for i in range(1,5)],
            language(10)],
        ['Scríobh litir chuig do dheartháir nó do dheirfiúr i Londain faoin gcluiche mór.',
         'Dhá phointe eolais faoi gach ceann de na ceithre phictiúr; leagan amach cuí.'],
        'The letter stays whole: layout6, four picture awards of6(3+3), and shared language10. Expand brother/sister recipients. Each picture requires two open details; no closed detail menu or word-count penalty is printed.',additionalTopicIds=['irish-2-8'])
    cards.remove(letter)
    letters=[]
    for recipient in ['dearthair','deirfiur']:
        route=copy.deepcopy(letter)
        route['id']+='-'+recipient
        route['atlasQuestionId']+='-'+recipient
        route['conceptId']+='-'+recipient
        label='do dheartháir' if recipient=='dearthair' else 'do dheirfiúr'
        route['questionRef']+=' · '+label
        route['questionText']+='\n\nAn rogha don chárta seo: litir chuig '+label+'.'
        cards.append(route)
        letters.append(route)
    stories=[]
    for slot,page,end in [('5A',16,13),('5B',17,15)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ag Céilí Mór i halla na scoile an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin gCéilí Mór sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nCéilí Mór'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ar do bhealach chun na scoile le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        # The scheme reduces the awarded whole-response mark proportionally for
        # insufficient length. One final score keeps that adjustment confined to
        # this story in paired routes, while preserving both 37/13 rubric parts.
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(13 if slot=='5A' else 14,end+1)),[
                criterion('freagra','Freagra iomlán · Cumarsáid 37 + Gaeilge 13',50,[
                    'Cumas Cumarsáide = 37 marc; Cruinneas Gaeilge = 13 mharc. Mark both parts, then enter the final whole-response mark after any published proportional length adjustment.',
                    *scheme_guidance(13 if slot=='5A' else 14,end),
                    *language(13)['guidance'],
                    'If too short, subtract the appropriate percentage of the awarded mark: the SEC example is 45 words → mark the attempt, then deduct 50% of the awarded mark. Apply this only to this story. No later-year fixed length table is printed.'
                ])],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad don ócáid sna pictiúir.'],
            'First assess communication /37 and language /13. Reduce the communication ceiling by five per missing reference; for 5(b), cover each of the four pictures plus a fifth detail. The final story score includes the scheme’s proportional short-length reduction (45 words: halve the awarded mark). Enter that final mark out of 50. References are indicative, not a closed pool.'))
    # Q4 and Q5 are both compulsory, with one of A/B in each: six products including the two letter recipients.
    for first,second in itertools.product([notice,*letters],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2019 FL ','')+' + '+second['questionRef'].replace('2019 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==71 and len({c['id'] for c in cards})==71
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2019,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,25)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writingQ4=40,writingQ5=50,writing=90,total=360),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and letter picture points are required. Each whole response keeps one language award. The printed brother/sister recipient alternatives are mechanically expanded.',
            'The two information points per letter picture and source-retrieval answers are content choices, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 5 whole writing routes including both letter recipients; 6 paired reading routes; 6 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2019 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+p.get_text() for i,p in enumerate(scheme))
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2019-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2019: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
