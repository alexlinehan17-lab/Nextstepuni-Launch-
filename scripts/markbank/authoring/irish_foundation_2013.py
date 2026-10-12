#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2013 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
from irish_choice import withdraw_combinations

ROOT = Path(__file__).resolve().parents[3]
FILE = 'LC001BLP000IV'
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2013-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2013-source-review.json'

def scheme_page_text(page):
    # Visually verified Symbol-font bullet and arrow; original PDF unchanged.
    return page.get_text().translate({0xf0b7: "•", 0xf0ae: "→"})

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2013/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2013/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'fa96169580d48dbd2f59526ca25e1ee5ac0fdd0d7a2721eaa9b7535defa644d6', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '2e757734151f40ae1f01795a95d2ecdd6be661988fd0e00faa0a602c9118c7d9', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2013-fl-{key.lower()}', year=2013, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2013 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2013 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag Niamh?', None, 'Bainisteoir i siopa éadaigh = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cén caitheamh aimsire is fearr le Niamh?',
  'Taisteal | Éadaí a cheannach | Haca a imirt',
  'Haca a imirt'),
 ('2a', 2, 7, 'Cén cúrsa atá á dhéanamh ag Pádraig?', None, 'Innealtóireacht = an dara pictiúr'),
 ('2b',
  2,
  7,
  'Cé chomh minic is a théann Pádraig abhaile go Ciarraí?',
  'Gach deireadh seachtaine | Uair sa mhí | Uair sa bhliain',
  'Uair sa mhí'),
 ('3', 3, 8, 'Cá bhfuil an fear ag dul?', None, 'Ionad Sláinte = an ceathrú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil siopa an táilliúra? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar dheis (tic nó saighead)'),
 ('5a',
  3,
  8,
  'Conas a bheidh an aimsir i bPort Laoise amárach?',
  None,
  'Tirim, grianmhar = an chéad phictiúr'),
 ('5b', 3, 8, 'Cén táille a bheidh ar an mbus?', '€7 | €8 | €10', '€10'),
 ('6a',
  4,
  10,
  'Cá raibh Ciara tráthnóna inné?',
  'Sa rang Mata | San oifig | Ar an bpáirc imeartha',
  'Ar an bpáirc imeartha'),
 ('6b',
  4,
  10,
  'Cé mhéad cárta buí a thug Ciara amach?',
  'Ceann amháin | Dhá cheann | Trí cinn',
  'Dhá cheann'),
 ('7a',
  4,
  10,
  'Conas a bhris Liam a chos?',
  'Ar ghluaisrothar | Ag imirt rugbaí | Thit sé de chrann',
  'Thit sé de chrann'),
 ('7b', 4, 10, 'Cad a bhí sa gharáiste an t-am ar fad?', 'Carr | Dréimire | Otharcharr', 'Dréimire'),
 ('8a',
  4,
  10,
  'Cá raibh Sorcha ar an Satharn?',
  'Ar saoire | San oifig thaistil | In árasán',
  'San oifig thaistil'),
 ('8b',
  4,
  10,
  'Cén margadh a gheobhaidh Maidhc?',
  'Saoire ar €200 | Saoire ar €300 | Saoire ar €400',
  'Saoire ar €300')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2013/LC001BLP017IV.mp3'
    for n,page,marks,prompt,options,answer in aural:
        comparable = lambda s: re.sub(r'[^\w]+','',s.lower())
        assert re.search('.*?'.join(re.escape(comparable(w)) for w in prompt.split()), comparable(texts[page-1])), (n,prompt)
        for option in (options or '').split(' | '):
            assert comparable(option) in comparable(texts[page-1]), (n,option)
        ref = 'Cluastuiscint · Ceist ' + re.sub(r'([ab])$',r'(\1)',n)
        card = add('A-'+n,'1',ref,re.sub(r'^(\d+)([ab]?)$', lambda m: m[1]+'. '+('('+m[2]+') ' if m[2] else ''), n)+prompt+
            ('\n\n'+options.replace(' | ','\n') if options else ''),
            'irish-1-3',['aural'],[page],[4 if n[0] in '78' else 3],
            [criterion('answer','Freagra',marks,[answer],True)],
            ['Éist leis an taifeadadh. Úsáid na pictiúir ar an leathanach nuair is gá.'],
            audioMaterial=dict(kind='source-audio',label=ref,
                title='Gaeilge Bonnleibhéal 2013 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Club Sacair\nTraenáil\nDé Máirt agus Dé hAoine 7 p.m.',
 'Siopa Bearbóra\nAr Oscailt\nó Luan go Satharn 8 a.m.',
 'Cór na Scoile\nCleachtadh 3-5 p.m.\nGach Déardaoin',
 'Bóthar Dúnta romhat\nRás Rothaíochta\nar siúl',
 'Féile Scannán\nBaile Átha Cliath\n7-15 Feabhra, 2014',
 'Ticéad Páirceála\nAr fáil anseo\n€2 san uair',
 'Seó Faisin\nÓstán na Mara\nCead Isteach €10',
 'Árasán ar cíos\nAn dara hurlár\n21 Sráid na Cille',
 'Grianghrafadóir\ndon ócáid speisialta sin\n087-312 432',
 'Rásaí na gCapall\nGaillimh\n22-28 Iúil']
    for i,(sign,answer) in enumerate(zip(signs,'FEBHADJIGC'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[5],
            [criterion('answer','Litir cheart',4,[answer],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cá bhfuil Síle Ní Bhriain ina cónaí?', 'Bré | Cluain Tarbh | Thar lear', 'Cluain Tarbh'),
         ('Cathain a chonaic Síle an fógra sa nuachtán?', 'Inné | Arú inné | Inniu', 'Inné'),
         ('Cá bhfuil an folúntas?',
          'I nuachtán | In oifig dlíodóra | In oifig thaistil',
          'In oifig thaistil'),
         ('Cén grád a fuair Síle sa Stair san Ardteistiméireacht?', 'Grád A | Grád B | Grád C', 'Grád B'),
         ('Cén ceadúnas atá ag Síle?',
          'Ceadúnas píolóta | Ceadúnas teilifíse | Ceadúnas tiomána',
          'Ceadúnas tiomána')]),
 '2B': (7,
        'brochure',
        [('Cén baile mór is gaire don Rinn?', 'Corcaigh | Dún Garbhán | Port Láirge', 'Dún Garbhán'),
         ('Cé mhéad scoláire Gaeilge a thagann go Coláiste na Rinne gach samhradh?',
          '1,000 | 1,500 | 10,000',
          '1,000'),
         ('Cad a théann siar go dtí aimsir an Ghorta sa Rinn?',
          'An coláiste | An teach solais | Reilig an tSléibhe',
          'Reilig an tSléibhe'),
         ('Cad a íosfaidh an cuairteoir sna bialanna sa Rinn?', 'Bia mara | Éanlaith | Leite', 'Bia mara'),
         ('Cén mhí a mbíonn an “Tionól Ceoil” sa Rinn?', 'Feabhra | Iúil | Lúnasa', 'Feabhra')]),
 '2C': (8,
        'news',
        [('Cén mhí in 2012 ar chríochnaigh “Rás Volvo”?', 'Aibreán | Iúil | Deireadh Fómhair', 'Iúil'),
         ('Cé mhéad bád a bhí páirteach i “Rás Volvo”?', '6 | 10 | 20', '6'),
         ('Cén treo ar imigh na báid ag tús an ráis?', 'Soir | Siar | Ó dheas', 'Ó dheas'),
         ('Cén áit a raibh tinte cnámh ar lasadh do na báid?',
          'Ar Árainn | Ar chósta Chonamara | I nGaillimh',
          'Ar chósta Chonamara'),
         ('Cad as don mhairnéalach Damian Foxall?', 'An Spáinn | Éire | Meiriceá Theas', 'Éire')]),
 '3A': (9,
        'news',
        [('Cad a rinne Brendan tar éis dó freastal ar an ollscoil? Thosaigh sé …',
          'Ag déanamh scannán | Ag léamh | Ag múineadh',
          'Ag múineadh'),
         ('Cén bhliain ar éirigh Brendan as a phost mar mhúinteoir?', '1955 | 1982 | 1991', '1991'),
         ('Cén ról a bhí ag Brendan i scannáin Harry Potter?',
          'Gerry Boyle | Mad-Eye Moody | Hamish',
          'Mad-Eye Moody'),
         ('Cá bhfuil Brendan ina chónaí?', None, 'In Éirinn / i mBaile Átha Cliath'),
         ('Cén gléas ceoil a sheinneann Brendan?', 'An fheadóg | An fhidil | An giotár', 'An fhidil')]),
 '3B': (10,
        'extract',
        [('Cén tsiombail oifigiúil atá ag Rialtas na hÉireann?',
          'An ceol | An chláirseach | An tseamróg',
          'An chláirseach'),
         ('Cén fáth ar bunaíodh Comhaltas Ceoltóirí Éireann?',
          None,
          'Chun an ceol traidisiúnta a mhúineadh agus a cheiliúradh'),
         ('Cá raibh Fleá Cheoil na hÉireann an chéad uair a bhí sí ann?',
          'An Cabhán | An Muileann gCearr | Cathair Dhoire',
          'An Muileann gCearr'),
         ('Cad a bhíonn ar siúl sa Scoil Éigse?', 'Ceardlanna | Ceolchoirmeacha | Comórtais', 'Ceardlanna'),
         ('Cá fhad a bheidh an Fhleá Cheoil i gCathair Dhoire?',
          'Ó mhaidin go hoíche | Ar feadh bliana | Ar feadh naoi lá',
          'Ar feadh naoi lá')]),
 '3C': (11,
        'poem',
        [('Cad a thit aréir?', 'Díon an tí | Báisteach | Sneachta', 'Báisteach'),
         ('Cathain a stad an bháisteach?', 'Tráthnóna | Aréir | Ar maidin', 'Ar maidin'),
         ('Cad a bhí i lár an bhaile?', 'Lochán | Sparán | Sruthán', 'Sruthán'),
         ('Cad a chuir an file air féin?', None, 'Buataisí'),
         ('Cad a d’fhág an t-uisce ina dhiaidh?', 'Gáire | Láib | Scáil', 'Láib')])}
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
                assert comparable(accepted) in comparable(scheme[4 if slot[0]=='2' else (6 if slot=='3C' else 5)].get_text()), (slot,i,accepted)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],[5 if slot[0]=='2' else (7 if slot=='3C' else 6)],
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            if slot == '3B' and i == 2:
                card['criteria'][0]['permittedMarks'] = [0,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Chun an ceol traidisiúnta a mhúineadh; Chun an ceol traidisiúnta a cheiliúradh.',
                    '4 mharc: Má fhágtar an focal traidisiúnta ar lár, pionós −2.',
                    '3 mharc: “Ceol traidisiúnta” leis féin.']
            if slot == '3B' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,4,6]
                card['criteria'][0]['guidance'] += ['4 mharc: ó mhaidin go hoíche.']
            if slot == '3C' and i == 4:
                card['criteria'][0]['permittedMarks'] = [0,2,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Chuir mé orm mo bhuataisí / Is shiúil mé amach gan náire (an dá líne).',
                    'Céad trí líne de Véarsa3: pionós −2; Véarsa3 ar fad: pionós −4. Enter the final score for this answer only.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2013 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2013 FL ','')+'\n'+c['questionText'] for c in members),
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
            'Dul na Gaeilge: struchtúr na Gaeilge agus cruinneas gramadaí. Foclóir: cruinneas foclóra. Litriú: cé go mbeadh sé seo san áireamh moltar gan iomarca béime a chur ar an ngné seo ag an leibhéal seo.',
            f'Bronn marc as {marks} ar chaighdeán na Gaeilge san iarracht iomlán.',
            'PDF page16 describes the modified marking scheme and its four-mark language score scaled to10 or13. Do not apply that conversion to the standard rubric.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'Scéim Mharcála\s+\d+\s+ATBL 2013', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    notice_p10 = scheme_guidance(10,10)[0]
    notice_p11 = scheme_guidance(11,11)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'
        'Cén rud a bheidh ar siúl? Cén áit a mbeidh sé?\nCén lá? Dáta? Am? Cead isteach?\nCén t-aoi speisialta?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[9,10,11],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p10.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p10.split('Pictiúr 2',1)[1],
                'Published allocation discrepancy: the date heading is “Dáta? (3 mharc)” and the overview gives picture2 as4+3+3+3=13, but one sentence prints “ar4mharc”. This rubric retains the explicit three-mark date allocation and thirteen-mark picture total; compare both original scheme pages. The conflicting sentence is preserved above.']),
            criterion('pictiur3','Pictiúr 3',4,[notice_p11.split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p11.split('Pictiúr 4',1)[1].split('Cruinneas Gaeilge',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Layout1; required pictures8+13+4+4; one language award10. Preserve the printed1-mark deductions for an indefinite venue, unsuitable day, date without a named month/day, fee, and unintegrated guest name. Published date wording conflicts with the3-mark heading: see picture2 guidance and the original scheme.',
        sourceDiscrepancyNotice='Nóta foinse: tá “4 mharc” in abairt amháin faoin dáta, ach “3 mharc” sa cheannteideal agus sa leithdháileadh iomlán. Féach ar an scéim bhunaidh.')
    letter = add('W-4B','3','Scríobh · Ceist 4(b) · Litir',
        'Féach ar na pictiúir thíos.\n\nTá tú ag obair san ospidéal seo don samhradh. Scríobh litir abhaile chuig do chara ag insint dó / di:\n\n'
        '- Faoin ospidéal (pointe amháin eolais) — Pictiúr 1\n'
        '- Faoin obair a dhéanann tú san ospidéal (trí phointe eolais) — Pictiúr 2\n'
        '- Faoi na daoine a fheiceann tú san ospidéal (dhá phointe eolais) — Pictiúr 3\n'
        '- Faoi na rudaí a dhéanann tú nuair a bhíonn am saor agat (dhá phointe eolais) — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do litir: seoladh, dáta, tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('seoladh','Seoladh',2,['Seoladh = 2 mharc.']),
            criterion('data','Dáta',1,['Glac le figiúirí.']),
            criterion('beannu','Beannú',1,['Beannú = 1 mharc.']),
            criterion('crioch','Críoch / Slán',2,['Críoch / Slán = 2 mharc.']),
            *[criterion(f'pictiur{i}',f'Pictiúr {i}',marks,[
                scheme_guidance(12,12)[0].split(f'Pictiúr {i}',1)[1].split(f'Pictiúr {i+1}' if i<4 else 'Cruinneas Gaeilge',1)[0]
            ]) for i,marks in [(1,3),(2,9),(3,6),(4,6)]],
            language(10)],
        ['Scríobh litir chuig do chara faoi do phost samhraidh san ospidéal.',
         'Luaigh 1/3/2/2 pointe faoi na ceithre phictiúr; seoladh, dáta, tús agus críoch oiriúnach.'],
        'One whole40-mark letter: layout6 (2+1+1+2), picture content24 (3+9+6+6), sharedlanguage10. One friend is an open recipient; dó/dí is flexible pronoun wording, not separate prescribed task prompts. The required1/3/2/2 details have non-exhaustive examples, not finite selection menus. No length penalty is printed.',
        additionalTopicIds=['irish-2-8'])
    stories=[]
    for slot,page,start,end in [('5A',16,13,14),('5B',17,14,15)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú i láthair ag Oíche Speisialta sa Chlub Óige le déanaí.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoi.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nOíche Speisialta sa Chlub Óige'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ag an linn snámha le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        guidance=scheme_guidance(start,end)
        # PDF14 contains the end of5(a) and beginning of5(b); keep only this task.
        if slot=='5A': guidance[-1]=guidance[-1].split('5(b)',1)[0]
        else: guidance[0]=guidance[0].split('5(b)',1)[1]
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(start,end+1)),[
                criterion('cumarsaid','Cumas Cumarsáide · marc tar éis coigeartú faid',37,[
                    'Reduce the communication ceiling by5 for each missing reference. Assess communication against that ceiling, then reduce the awarded communication mark proportionally for insufficient length. Keep the language mark separate.',
                    *guidance,
                    'Published worked examples:60 words, one missing reference → ceiling32, communication27 minus9 =18.45words, two missing references → ceiling27, communication20 minus10 =10. Language is assessed separately /13 (example7). Apply the length adjustment only to this story’s communication score, never to language or the other question.'
                ]),language(13)],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad; i5(b), ceann do gach pictiúr agus ceann amháin eile.'],
            'Communication37 with a5-mark ceiling reduction per missing reference and proportional length adjustment; language13 assessed separately. For5(b), cover all four pictures plus a fifth detail. These references are required content with indicative examples, not a finite task pool.'))
    # Q4 and Q5 are both compulsory, with one of A/B in each: four products.
    for first,second in itertools.product([notice,letter],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2013 FL ','')+' + '+second['questionRef'].replace('2013 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==68 and len({c['id'] for c in cards})==68
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2013,level='foundation',paperFileid=FILE+'.pdf',
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
            'All notice headings and letter points are compulsory. One open friend with dó/dí is flexible pronoun wording, not a finite recipient pool; the letter retains one shared language award.',
            'The required1/3/2/2 letter details and source-retrieval answers are open content, not enumerated task prompts.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 4 whole writing tasks; 6 paired reading routes; 4 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return withdraw_combinations(dict(review=review,cards=cards)),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2013 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2013-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2013: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
