#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2018 paper pages 1–20 and scheme pages 1–24 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2018-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2018-source-review.json'


def scheme_page_text(page):
    mappings = json.loads(SOURCE_REVIEW.read_text())['schemeGlyphMappings']
    replacements = {}
    for span in page.get_texttrace():
        for code,glyph,origin,_ in span['chars']:
            if code == 0xfffd:
                value = mappings.get(span['font'],{}).get(str(glyph))
                assert value is not None, ('Unreviewed scheme glyph',page.number+1,span['font'],glyph)
                replacements[tuple(round(v,2) for v in origin)] = value
    lines=[]
    for block in page.get_text('rawdict')['blocks']:
        for line in block.get('lines',[]):
            text=''.join(replacements.get(tuple(round(v,2) for v in char['origin']),char['c'])
                for span in line['spans'] for char in span['chars'])
            lines.append(text)
    text='\n'.join(lines).replace('\u00ad','-').replace('\u00a0',' ')
    assert not re.search(r'[\x00-\x08\x0b-\x1f\ufffd]',text), ('Undecoded scheme text',page.number+1)
    return text

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2018/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2018/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == 'fa886ddd37c690d10adb9ebc3b83b5010942994b8c394708c6b58e70c530fe4a', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == 'a57bd47c929114eb30f6dc39b08ce4b874457e355d81ad08536672b2ee9482af', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2018-fl-{key.lower()}', year=2018, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2018 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2018 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 7, 'Cén post atá ag Síle faoi láthair?', None, 'Bainisteoir óstáin = an tríú pictiúr'),
 ('1b',
  2,
  7,
  'Conas a théann Síle go lár na cathrach gach maidin?',
  'Ar an Dart | Sa charr | Ar an mbus',
  'Ar an Dart'),
 ('2a', 2, 7, 'Cad a osclaíodh i Ros Muc an mhí seo caite?', None, 'Siopa caife = an dara pictiúr'),
 ('2b',
  2,
  7,
  'Cén t-am a dhúntar an áit nua seo gach tráthnóna?',
  'A dó dhéag a chlog | Leathuair tar éis a dó | A sé a chlog',
  'A sé a chlog'),
 ('3', 3, 8, 'Cá bhfuil an bhean ag dul?', None, 'Oifig an phoist = an ceathrú pictiúr'),
 ('4',
  3,
  8,
  'Cá bhfuil an t-ionad sláinte? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar chlé (tic nó saighead sa bhosca)'),
 ('5a', 3, 8, 'Conas a bheidh an aimsir maidin amárach?', None, 'Grianmhar, tirim = an tríú pictiúr'),
 ('5b',
  3,
  8,
  'Cá rachaidh na scoláirí ar a dó a chlog?',
  'Chuig an ionad siopadóireachta | Chuig an músaem staire | Chuig an trá',
  'Chuig an músaem staire'),
 ('6a',
  4,
  10,
  'Cad a bheidh ar siúl sa chlub óige Dé hAoine seo chugainn?',
  'Seó tallainne | Cóisir mhór | Ceolchoirm',
  'Cóisir mhór'),
 ('6b',
  4,
  10,
  'Conas a chaithfidh Áine an Satharn ar fad?',
  'Ag siopadóireacht | Ag staidéar | Ag traenáil',
  'Ag staidéar'),
 ('7a',
  4,
  10,
  'Cad a cheap Clár den scrúdú Staire?',
  'Bhí sé éasca go leor | Bhí sé rófhada | Bhí sé an-deacair',
  'Bhí sé éasca go leor'),
 ('7b',
  4,
  10,
  'Cá mbeidh Pól ag dul i mí Lúnasa?',
  'Go dtí an Spáinn | Go hÉirinn | Go dtí an Phortaingéil',
  'Go dtí an Phortaingéil'),
 ('8a',
  4,
  10,
  'Cén fáth nach raibh Eoin ar scoil inné?',
  'Bhí sé ag imirt iománaíochta | Bhí sé ar pháirc na himeartha | Bhí sé san ospidéal',
  'Bhí sé san ospidéal'),
 ('8b',
  4,
  10,
  'Cá bhfanfaidh Eoin nuair a bheidh an lá mór spóirt ar siúl?',
  'Sa seomra staidéir | Sa bhaile | Sna ranganna',
  'Sa seomra staidéir')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2018/LC001BLP017IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2018 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLP017IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Seomra Tíreolaíochta\nLéarscáileanna agus\ncruinneoga ar fáil ann',
 'Ospidéal na hOllscoile\nRannóg Timpistí agus Éigeandála\nCláraigh ag an deasc',
 'Margadh an tSathairn\n10.00 - Meán lae\nTorthaí agus glasraí úra ar díol',
 'Na traenacha ar ceal inniu\nCrainn leagtha ar an iarnród',
 'Dioscó anocht\nÓstán na Carraige\nTaispeáin do chárta aoise',
 'Lig do scíth\nClár nua ceoil ar Raidió Rí-Rá\nGach Déardaoin ar 9 p.m.',
 'Dola-Phlás romhat\nStop ag an bhfuinneog\nÍoc an dola',
 'Corn an Domhain sa sacar\nGach cluiche\nar RTÉ 2',
 'Áras an Uachtaráin\nTurais: 10.15 agus 11.30\nCuir ticéad in áirithe',
 'Ionad Siopadóireachta\nan Bhaile Mhóir\nCeamaraí slándála in úsáid']
    for i,(sign,answer) in enumerate(zip(signs,'CFHAGIJEBD'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer,
                'Glactar le córas eile (uimhir an phictiúir in ionad litir an phictiúir) má tá sé soiléir / intuigthe.'],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cathain a scríobh Cáit an litir seo?', '9 Aibreán | 15 Aibreán | 14 Iúil', '15 Aibreán'),
         ('Cén post a theastaíonn ó Cháit?', 'Rúnaí | Fáilteoir | Treoraí', 'Treoraí'),
         ('Cén grád a fuair Cáit sa Spáinnis san Ardteistiméireacht?',
          'Grád A2 | Grád B1 | Grád C1',
          'Grád B1'),
         ('Cár rugadh agus cár tógadh Cáit?', 'Ciarraí | Corcaigh | Maidrid', 'Ciarraí'),
         ('Cad a fuair Cáit ón ionad turasóireachta i Maidrid?',
          'Céim | Teistiméireacht | Agallamh',
          'Teistiméireacht')]),
 '2B': (7,
        'brochure',
        [('Cá bhfuil Dúlainn?', 'I Meiriceá | In Éirinn | Ar Mhór-Roinn na hEorpa', 'In Éirinn'),
         ('Cathain a bhíonn féile na scríbhneoirí ar siúl i nDúlainn?',
          'I mí Feabhra | I mí an Mheithimh | Ó cheann ceann na bliana',
          'I mí Feabhra'),
         ('Cad atá ann don staraí?', 'Siúlóidí | Machairí gailf | Seanchaisleáin', 'Seanchaisleáin'),
         ('Conas is féidir dul go hOileáin Árann?', 'Ar bhád | Ar bhus | Sa charr', 'Ar bhád'),
         ('Cá bhfuil lóistín compordach le fáil sa cheantar?',
          'Sna siopaí | Sna bialanna | Sna hóstáin',
          'Sna hóstáin')]),
 '2C': (8,
        'news',
        [('Cá bhfuil Úna ina cónaí?', 'Páras | Droichead Átha | Disneyland', 'Droichead Átha'),
         ('Cén áit ar chuir Úna a pas an lá sular imigh sí?',
          'Ina cás | Ar an urlár | Ina mála láimhe',
          'Ina mála láimhe'),
         ('Cén t-am a shroich Úna an t-aerfort?', '7 a.m. | 8.30 a.m. | 11 a.m.', '8.30 a.m.'),
         ('Cén fáth a raibh Úna trí chéile san aerfort?',
          'Ní raibh a pas aici | Ní raibh airgead aici | Ní raibh a cás aici',
          'Ní raibh a pas aici'),
         ('Cá bhfuair Liam an pas ar deireadh?',
          'Sa chistin | Sa seomra suí | I seomra leapa Úna',
          'I seomra leapa Úna')]),
 '3A': (9,
        'news',
        [('Cén tslí bheatha a bhí ag athair Ruth?', 'Dochtúir | Altra | Aisteoir', 'Dochtúir'),
         ('Cár bhog Ruth nuair a bhí sí aon bhliain déag d’aois?',
          'Go dtí an Aetóip | Go Luimneach | Go Londain',
          'Go Londain'),
         ('Cén cúrsa a rinne Ruth i gColáiste na Tríonóide, Baile Átha Cliath?',
          None,
          '(Cúrsa) aisteoireachta'),
         ('Cén pháirt a bhí ag Ruth sa scannán Loving?',
          'Cailín uaigneach | Cailín gorm | Amhránaí',
          'Cailín gorm'),
         ('Cad a dhéanann Ruth nuair a bhíonn am saor aici?',
          'Ag bualadh lena cairde | Ag léamh | Ag taisteal',
          'Ag léamh')]),
 '3B': (10,
        'extract',
        [('Cén amharclann atá i nGaillimh?',
          'Siamsa Tíre | Amharclann na Mainistreach | An Taibhdhearc',
          'An Taibhdhearc'),
         ('Cén fáth ar bunaíodh an Taibhdhearc?', None, 'Chun drámaíocht na Gaeilge a chur chun cinn'),
         ('Cé a scríobh an dráma Diarmuid agus Gráinne?',
          'Mick Lally | Micheál Mac Liammóir | Siobhán McKenna',
          'Micheál Mac Liammóir'),
         ('Cad a bhíonn ar siúl don aos óg ag an Nollaig?',
          'Geamaireacht | Ceoldrámaí | Rince',
          'Geamaireacht'),
         ('Cén mhí ina raibh an Oíche Chultúir ar siúl anuraidh?',
          'Mí na Nollag | Mí Mheán Fómhair | Mí Iúil',
          'Mí Mheán Fómhair')]),
 '3C': (11,
        'poem',
        [('Cá raibh an file ag dul i véarsa 1?', 'Go dtí an club | Abhaile | I gcéin', 'Abhaile'),
         ('Cad a múchadh gan choinne?', 'An ghealach | Na réaltaí | Soilse na sráide', 'Soilse na sráide'),
         ('Cad a tháinig ó íochtar na spéire?', 'Solas faoi luas | Eitleán | Roicéad', 'Solas faoi luas'),
         ('Cad a dúirt an file leis féin i véarsa 3?', None, 'Cad atá ann?'),
         ('Cé atá ag féachaint anuas?', 'Na flaithis | An file | Na spásairí', 'Na spásairí')])}
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
                assert comparable(accepted) in comparable(scheme_page_text(scheme[4 if slot[0]=='2' else 5])), (slot,i,accepted)
            card = add(f'R-{slot}-{i}','2',f'Léamhthuiscint · Ceist {slot[0]}({slot[1].lower()})({i})',
                f'Léigh an téacs ar leathanach {page}.\n\n{i}. '+prompt+
                ('\n\n'+options.replace(' | ','\n') if options else ''),
                'irish-9-2',[exam_topic],[page],[5 if slot[0]=='2' else 6],
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            if slot == '3A' and i == 3:
                card['criteria'][0]['guidance'] += ['6 mharc: Cúrsa aisteoireachta nó aisteoireachta.']
            if slot == '3B' and i == 2:
                card['criteria'][0]['permittedMarks'] = [0,2,4,6]
                card['criteria'][0]['guidance'] += [
                    '4 mharc: Chun drámaíocht a chur chun cinn; Chun Gaeilge a chur chun cinn; Drámaíocht na Gaeilge.',
                    '2 mharc: Drámaíocht; Gaeilge.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2018 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2018 FL ','')+'\n'+c['questionText'] for c in members),
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
        'Cén rud a bheidh ar siúl? Cén áit?\nCén lá? Cén dáta? Cén t-am? Cén táille?\nCén t-aoi speisialta a bheidh i láthair?\nCad a dhéanfar leis an airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p9.split('Pictiúr 1',1)[1].split('Pictiúr 2',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2',1)[1].split('Pictiúr 3',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,['Conor Murray (Pictiúr 3).',notice_p9.split('Pictiúr 3',1)[1],notice_p10.split('Pictiúr 4',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p10.split('Pictiúr 4',1)[1].split('Cuir tic',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Award the published picture submarks and one shared ten-mark language award. Follow the exact 2018 activity/place partial credit, date, fee and guest-name rules within the affected picture awards. Required headings are not choices.')
    form_prompt = (
        'Ba mhaith leat a bheith ag obair an samhradh seo mar chúntóir sa siopa ríomhaireachta áitiúil.\n\n'
        'Líon isteach an Fhoirm Iarratais atá anseo thíos. [Nóta: Is tusa Síofra Ní Cheallaigh.]\n\n'
        'An Siopa Ríomhaireachta, Dún Garbhán, Co. Phort Láirge\nFoirm Iarratais do Phost Samhraidh\n\n'
        'Ainm: Síofra Ní Cheallaigh\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:\n'
        'Cén Scrúdú Teistiméireachta atá déanta agat?\nAinmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:\n'
        'An réitíonn tú go maith le daoine?\nAn mbeidh tú sásta a bheith ag obair ar an Satharn?\n'
        'An bhfuil tú ábalta ríomhphost a sheoladh?\nLuaigh trí chaitheamh aimsire atá agat:\n'
        'Cuir tic (✓) leis an dáta is fearr leat le haghaidh agallaimh: 11 Bealtaine / 14 Bealtaine / 16 Bealtaine\n\n'
        'Scríobh alt gearr (timpeall 40 focal) ag insint cén fáth ar mhaith leat post samhraidh mar chúntóir sa siopa ríomhaireachta seo.\n\n'
        'Síniú: Síofra Ní Cheallaigh\nDáta:'
    )
    for day in [11,14,16]:
        assert f'{day} Bealtaine' in texts[14], 'Interview date changed: repeat selection review'
    fields_guide = [
        'Na Ceisteanna = 15 mharc. Úsáid an colún dúbailte: uimhir theileafóin2; seoladh4; aois2; dáta breithe2; scrúdú2; cúig ábhar10; réiteach le daoine1; obair ar an Satharn1; ríomhphost1; trí chaitheamh aimsire3; dáta agallaimh1; dáta ag bun1. Iomlán30 ÷ 2 = 15.',
        'Round up once after adding the doubled question awards and dividing by two: 21 ÷ 2 = 10½ → 11. Do not round each half-mark field separately.',
        scheme_guidance(11,11)[0].split('Na Ceisteanna',1)[1],
        scheme_guidance(12,12)[0].split('An t-Alt',1)[0],
    ]
    forms=[]
    for day in [11,14,16]:
        forms.append(add(f'W-4B-{day}-bealtaine','3',f'Scríobh · Ceist 4(b) · {day} Bealtaine',
            form_prompt+f'\n\nAn rogha don chárta seo: {day} Bealtaine.',
            'irish-9-0',['form'],[15],[11,12],[
                criterion('fields','Na Ceisteanna · iomlán slán',15,fields_guide),
                criterion('paragraph','An t-Alt · marc tar éis coigeartú faid',15,[
                    scheme_guidance(12,12)[0].split('An t-Alt',1)[1].split('Cruinneas Gaeilge',1)[0],
                    'Mark the relevant paragraph out of15 (off-topic ceiling5), then apply the published proportional short-length reduction to this paragraph award only. Example: 30 of40 words → deduct25% of the awarded paragraph mark. Enter that final paragraph score; keep the form-answer and shared-language scores separate.'
                ]), language(10)],
            ['Líon gach réimse riachtanach; cúig ábhar scoile agus trí chaitheamh aimsire.',
             f'Roghnaigh {day} Bealtaine don agallamh.',
             'Scríobh timpeall 40 focal faoin bpost sa siopa ríomhaireachta.'],
            'One whole40-mark form: questions15 (half marks combined then rounded up once), paragraph15 with its own proportional length adjustment, shared language10 across questions and paragraph. Three printed interview dates are expanded; school subjects and hobbies remain open content choices.'))
    stories=[]
    for slot,page,end in [('5A',16,13),('5B',17,15)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ar thuras rothaíochta faoin tuath le do chairde an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoin turas rothaíochta sin.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nTuras Rothaíochta Faoin Tuath'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nChuaigh tú chuig ceolchoirm le do chara.\nTá tú chun scríobh faoin gceolchoirm sin in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin gceolchoirm (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nCEOLCHOIRM'
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
    # Q4 and Q5 are both compulsory, with one of A/B in each: eight products including the three form dates.
    for first,second in itertools.product([notice,*forms],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2018 FL ','')+' + '+second['questionRef'].replace('2018 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==74 and len({c['id'] for c in cards})==74
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2018,level='foundation',paperFileid=FILE+'.pdf',
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
            'All notice headings and form fields are required. Each whole response keeps one shared language award. The three printed interview dates are mechanically expanded.',
            'Five school subjects, three hobbies, personal details and source-retrieval answers are open content choices, not enumerated task prompts. The scheme accepts at most one social-media hobby; its examples are not a printed task menu.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 6 whole writing routes including three form dates; 6 paired reading routes; 8 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return withdraw_combinations(dict(review=review,cards=cards)),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2018 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2018-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2018: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
