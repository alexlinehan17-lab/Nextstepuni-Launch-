#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2017 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2017-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2017-source-review.json'

def scheme_page_text(page):
    # This PDF encodes its printed bullet/arrow as private Symbol-font glyphs.
    return page.get_text().translate({0xf0b7: '•', 0xf0ae: '→'})

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2017/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2017/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'a266b96785cad935dfa6d4a750c2d2c9bf9ebfd1fb3238decb23bf50df26f4e6', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '075e41d3252b6ff8dc85d074791aa79846e0334e633637e6137a52077366447e', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2017-fl-{key.lower()}', year=2017, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2017 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2017 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén obair a dhéanann Muiris faoi láthair?', None, 'Meicneoir = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Cén áit a rachaidh Muiris an bhliain seo chugainn?',
  'An Astráil | Meiriceá | An Afraic',
  'An Afraic'),
 ('2a', 2, 7, 'Cén spórt atá rómhall, dar le Siobhán?', None, 'Galf = an dara pictiúr'),
 ('2b',
  2,
  7,
  'Cá bhfuil Siobhán ag obair?',
  'In oifig na scoile | In óstán | I linn snámha',
  'In oifig na scoile'),
 ('3', 3, 8, 'Cá bhfuil an fear ag dul?', None, 'Siopa crua-earraí = an tríú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil an naíonra? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar dheis (tic nó saighead sa bhosca)'),
 ('5a',
  3,
  8,
  'Conas a bheidh an aimsir do rásaí na gcapall amárach?',
  None,
  'Tirim, scamallach = an dara pictiúr'),
 ('5b',
  3,
  8,
  'Cén teocht is ísle a bheidh ann san oíche amárach?',
  'Cúig chéim Celsius | Naoi gcéim Celsius | Trí chéim déag Celsius',
  'Cúig chéim Celsius'),
 ('6a',
  4,
  10,
  'Cén áit a bhfuil Aoife ina cónaí faoi láthair?',
  'In árasán | I mbungaló | I dteach dhá stór',
  'In árasán'),
 ('6b', 4, 10, 'Conas a rachaidh Aoife ar scoil ón mbungaló?', 'Sa charr | Ag siúl | Ar rothar', 'Ar rothar'),
 ('7a',
  4,
  10,
  'Cá raibh Róise nuair a chuala sí trup uafásach?',
  'Ar scoil | Ag doras an tí | San otharcharr',
  'Ag doras an tí'),
 ('7b',
  4,
  10,
  'Cén damáiste a rinneadh don ghluaisrothar?',
  'Bhí solas amháin briste | Bhí ola ag sileadh as | Bhí sé ina smidiríní',
  'Bhí solas amháin briste'),
 ('8a',
  4,
  10,
  'Cad a bhí ar siúl i halla na scoile aréir?',
  'Cúrsa cócaireachta | Cúrsa ríomhaireachta | Taispeántas gairmeacha',
  'Taispeántas gairmeacha'),
 ('8b',
  4,
  10,
  'Cén áit a ndéanfaidh Pól an cúrsa sna meáin?',
  'I stáisiún teilifíse | Ar an ollscoil | I mbialann',
  'Ar an ollscoil')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2017/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2017 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Club Gaeilge do dhéagóirí\nHalla an Phiarsaigh\nComhrá – Cluichí – Ceol',
 'Láithreán Tógála\nClogad agus Seaicéad Buí\nag teastáil',
 'Raon Reatha\nOscailt Oifigiúil\nDé hAoine, 16 Meitheamh',
 'Páirc an Chrócaigh\nAontroim v An Clár\n10 Lúnasa, 3.30 p.m.',
 'Dáil Éireann\nCosc ar thobac\na chaitheamh anseo',
 'Deireadh Seachtaine thar lear\nLondain – An Róimh – Páras\nRátaí speisialta ar fáil',
 'Oifig an Phríomhoide\nCiúnas\nCruinniú ar siúl',
 'Ceachtanna Giotáir\nGach Céadaoin\nGach eolas ó 083 562771',
 'Ceaintín na Scoile\nCeannaigh Lón Sláintiúil\nPraghas: €3',
 'Banc Buidéal\nDo Phrócaí agus do Bhuidéil\nNá fág bruscar anseo']
    for i,(sign,answer) in enumerate(zip(signs,'EHIBFCJADG'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cathain a sheol Pól an fhoirm iarratais isteach?',
          '20 Aibreán | 24 Aibreán | 15 Meitheamh',
          '20 Aibreán'),
         ('Cén cúrsa atá á dhéanamh ag Pól faoi láthair?',
          'Snámh | Innealtóireacht | Rothaíocht',
          'Innealtóireacht'),
         ('Cén t-am a dhúntar an tIonad i rith an tsamhraidh?',
          '6.30 a.m. | 2.00 p.m. | 10.30 p.m.',
          '10.30 p.m.'),
         ('Conas is féidir le Pól an socrú le haghaidh an agallaimh a chinntiú?',
          'Litir | Glaoch teileafóin | Ríomhphost',
          'Glaoch teileafóin'),
         ('Cén post atá ag Sorcha Ní Neachtain?',
          'Bainisteoir | Rúnaí | Oifigeach Pearsanra',
          'Oifigeach Pearsanra')]),
 '2B': (7,
        'brochure',
        [('Cén áit a bhfuil Árainn Mhór?',
          'Sa chathair | Gar do chósta Dhún na nGall | Ar an mórthír',
          'Gar do chósta Dhún na nGall'),
         ('Conas is féidir le duine dul go dtí an t-oileán?',
          'Ar bhád farantóireachta | I gcarr | Ar eitleán',
          'Ar bhád farantóireachta'),
         ('Cad atá suite ciliméadar ón gcé?',
          'Óstáin | Tithe lóistín | Sráidbhaile saoire',
          'Sráidbhaile saoire'),
         ('Cad a fheicfidh an t-ealaíontóir gach áit ar an oileán?',
          'Rámhaíocht | Radhairc bhreátha | Bádóireacht',
          'Radhairc bhreátha'),
         ('Cén teanga a labhraítear go laethúil ar an oileán?',
          'Gaeilge | Gearmáinis | Fraincis',
          'Gaeilge')]),
 '2C': (8,
        'news',
        [('Cá mbíonn Tomás ag staidéar tar éis na scoile ar an Luan?',
          'Ar scoil | Sa leabharlann phoiblí | Sa bhaile',
          'Sa leabharlann phoiblí'),
         ('Cén lá a fuair Tomás leathlá saoire gan choinne?',
          'Dé Luain | Dé Céadaoin | Déardaoin',
          'Déardaoin'),
         ('Cén obair bhaile a rinne Tomás ar dtús?', 'Matamaitic | Gnó | Stair', 'Matamaitic'),
         ('Cén t-am a dhúisigh Tomás sa leabharlann?',
          'A dó a chlog | A cúig a chlog | A sé a chlog',
          'A sé a chlog'),
         ('Cé a bhí ag gáire faoi Thomás?',
          'An leabharlannaí | An sáirsint | A mháthair',
          'An leabharlannaí')]),
 '3A': (9,
        'news',
        [('Cén tslí bheatha atá ag Miriam O’Callaghan?',
          'Aisteoir | Ceoltóir | Láithreoir teilifíse',
          'Láithreoir teilifíse'),
         ('Cén fáth a raibh Miriam uaigneach agus í ar an ollscoil?', None, 'Ní raibh a lán cairde aici'),
         ('Cén chéim a rinne Miriam?', 'Cúrsaí reatha | Dlí | Polaitíocht', 'Dlí'),
         ('Cén saghas cláir é Prime Time?',
          'Clár raidió | Clár ceoil | Clár cúrsaí reatha',
          'Clár cúrsaí reatha'),
         ('Nuair a bhíonn am saor ag Miriam, téann sí ...',
          'Go bialann Indiach | Go Sasana | Go cumainn éagsúla',
          'Go bialann Indiach')]),
 '3B': (10,
        'extract',
        [('Cén mhí ina mbíonn Lá Fhéile Pádraig?', 'Márta | Bealtaine | Samhain', 'Márta'),
         ('Cén dath a bhíonn ar na héadaí a chaitheann a lán daoine ar Lá Fhéile Pádraig?',
          'Bán | Glas | Liath',
          'Glas'),
         ('Cén áit a mbíonn an pharáid is mó?',
          'San Astráil | I mBaile Átha Cliath | I Nua-Eabhrac',
          'I Nua-Eabhrac'),
         ('Cad a bhíonn ar siúl i bPáirc an Chrócaigh?',
          'Peil agus iománaíocht | Féilte rince | Ceol traidisiúnta',
          'Peil agus iománaíocht'),
         ('Cad a dhéanann daoine nuair a bhíonn Seachtain na Gaeilge ar siúl?',
          None,
          'Iarracht níos mó Gaeilge a labhairt')]),
 '3C': (11,
        'poem',
        [('Cad a bhíonn “Lán de bhrí” sna véarsaí seo?',
          'An geimhreadh | An t-ionad campála | An samhradh',
          'An t-ionad campála'),
         ('Bíonn an ghrian gheal ...', 'Ag spalpadh | Ag gáire | Ag eitilt', 'Ag spalpadh'),
         ('Cé a bhíonn ar saoire?', 'Déagóirí | Naíonáin | Tuismitheoirí', 'Tuismitheoirí'),
         ('Cad a bhíonn ar siúl ar an bhféar?', 'Snámh | Peil | Eitpheil', 'Peil'),
         ('Cathain a bhíonn “Cluichí is scléip” ar siúl?', None, 'Gach lá gan sos')])}
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
            if slot == '2C' and i == 2:
                card['sourceDiscrepancyNotice'] = 'Nóta foinse: ní réitíonn an lá sa téacs leis an lá sa scéim do Cheist 2(c)(2). Féach ar an dá fhoinse.'
                card['criteria'][0]['label'] = 'Freagra · neamhréir fhoilsithe'
                card['criteria'][0]['guidance'] = [
                    'SEC answer key: Déardaoin — 5 mharc.',
                    'Published source discrepancy: the passage on paper page8 says Tomás received the half-day at two on Wednesday (Dé Céadaoin), but scheme page5 prints Déardaoin. Both choices appear in the question. The paper and scheme conflict; the scheme does not explicitly award Dé Céadaoin. Compare both originals when reviewing this answer; do not treat the scheme answer as an uncontested reading of the passage.'
                ]
                card['markingGuideNote'] = card['criteria'][0]['guidance'][1]
            if slot == '3A' and i == 2:
                card['criteria'][0]['permittedMarks'] = [0,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Ní raibh a lán cairde aici san ollscoil.',
                    '4 mharc: Ní raibh cairde aici.',
                    '3 mharc: Ní raibh a lán cairde.']
            if slot == '3B' and i == 5:
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Déanann daoine iarracht níos mó Gaeilge a labhairt nuair a bhíonn Seachtain na Gaeilge ar siúl; Déanann daoine iarracht níos mó Gaeilge a labhairt; Níos mó Gaeilge a labhairt; Bíonn Seachtain na Gaeilge ar siúl. Déanann daoine iarracht níos mó Gaeilge a labhairt (nuair a bhíonn Seachtain na Gaeilge ar siúl).']
            if slot == '3C' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,3,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Gach lá; Cluichí is scléip gach lá gan sos.',
                    '3 mharc: Gan sos.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2017 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2017 FL ','')+'\n'+c['questionText'] for c in members),
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
        return [clean(re.sub(r'\n\s*\d+\s*$', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    notice_p9 = scheme_guidance(9,9)[0]
    notice_p10 = scheme_guidance(10,10)[0]
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'+
        'Cén rud a bheidh ar siúl? Cén áit a mbeidh sé?\nCén lá? Dáta? Am? Cead isteach?\nCén grúpa ceoil a bheidh ag seinm?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,[notice_p9.split('Pictiúr 3',1)[1],notice_p10.split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2017 activity/place partial credit, date, fee and band-name rules within the affected picture awards. Required headings are not choices.')
    reply = add('W-4B','3','Scríobh · Ceist 4(b) · Freagra ar chuireadh',
        'Féach ar na pictiúir thíos.\n\nIs tusa Colm. Fuair tú an cuireadh seo ó Áine. Scríobh FREAGRA ar an gcuireadh seo.\n'
        'I do fhreagra, luaigh na pointí seo:\n\n'
        '- An lá a fuair tú an cuireadh — Pictiúr 1\n'
        '- Go raibh áthas ort nuair a fuair tú an cuireadh — Pictiúr 1\n'
        '- Gur iarr tú cead ar do Mham dul ann — Pictiúr 3\n'
        '- Go mbeidh tú ábalta dul ann — Pictiúr 3\n'
        '- Conas a rachaidh sibh ann — Pictiúr 3\n'
        '- Dhá rud faoin gceolchoirm — Pictiúr 4\n'
        '- An t-am a rachaidh sibh abhaile — Pictiúr 4\n\n'
        'N.B. Bíodh an leagan amach cuí ar do fhreagra: tús agus críoch oiriúnach.',
        'irish-9-3',['letterWriting'],[15],[11,12],[
            criterion('iarracht','Iarracht ar an bhfreagra',1,['Iarracht ar an bhfreagra = 1 mharc.']),
            criterion('beannu','Beannú',1,['Beannú = 1 mharc.']),
            criterion('slan','Slán / Síniú',1,['Slán / Síniú = 1 mharc.']),
            criterion('pictiur1','Pictiúr 1',7,[scheme_guidance(12,12)[0].split('Pictiúr 1',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',9,[scheme_guidance(12,12)[0].split('Pictiúr 3',1)[1].split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',11,[scheme_guidance(12,12)[0].split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),
            language(10)],
        ['Scríobh freagra ar chuireadh Áine mar Colm.',
         'Luaigh gach pointe agus dhá rud faoin gceolchoirm; tús agus críoch oiriúnach.'],
        'The invitation reply stays whole: layout3, picture1=7(4+3), picture3=9(3+3+3), picture4=11(4+4+3), and one shared language10. Picture2 is the invitation source, not another assessed response. The two concert details are open information, not a printed choice menu. No address/date or word-count penalty is specified.',
        additionalTopicIds=['irish-2-8'],taskFormatLabel='Freagra ar chuireadh')
    stories=[]
    for slot,page,end in [('5A',16,13),('5B',17,15)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú i láthair ag Glantachán Earraigh sa Chlub Óige an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin nGlantachán Earraigh sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nGlantachán Earraigh sa Chlub Óige'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú ag an gClub Leadóige le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
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
    # Q4 and Q5 are both compulsory, with one of A/B in each: four products.
    for first,second in itertools.product([notice,reply],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2017 FL ','')+' + '+second['questionRef'].replace('2017 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==68 and len({c['id'] for c in cards})==68
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2017,level='foundation',paperFileid=FILE+'.pdf',
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
            'All notice headings and invitation-reply points are compulsory context. Each whole response retains its own shared language award; Colm and Áine are prescribed roles, not recipient alternatives.',
            'The two concert details in the reply and source-retrieval answers are content choices, not enumerated task prompts.',
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
    scheme_text='# Gaeilge Bonnleibhéal 2017 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2017-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2017: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
