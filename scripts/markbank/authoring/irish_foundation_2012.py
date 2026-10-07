#!/usr/bin/env python3
"""Reviewed Foundation tasks. Counts are assertions, not corpus-completeness proof.

2012 paper pages 1–20 and scheme pages 1–20 visually reviewed on 2026-10-07.
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
OUT = ROOT / 'components/MarkBank/cards/irish/foundation-2012-authored.json'

def clean(text):
    return re.sub(r'\s+', ' ', text).strip()

def criterion(id, label, marks, guidance, exact=False, deduct_from=None):
    return dict(id=id, label=label, kind='deduction' if deduct_from else 'award',
                maxMarks=marks, permittedMarks=[0, marks] if exact else list(range(marks+1)),
                guidanceKind='exact-answer' if exact else 'quality', guidance=guidance,
                **({'deductFrom': deduct_from} if deduct_from else {}))

DIRECTIVE = re.compile(r'rogha|roghna|Freagair|Cuir tic|Ainmnigh|Luaigh|\bchoose\b|\beither\b|\bany\b|one of|\bnó\b|dhá phointe|dhá rud|dheartháir|dheirfiúr|dó / d[ií]', re.I)
SOURCE_REVIEW = ROOT / 'scripts/markbank/authored/irish-foundation-2012-source-review.json'

def scheme_page_text(page):
    # Visually verified Symbol-font bullet and arrow; original PDF unchanged.
    return page.get_text().translate({0xf0b7: "•", 0xf0ae: "→", 0xf0b8: "÷"})

def selection_decisions(paper):
    decisions = json.loads(SOURCE_REVIEW.read_text())['selectionDecisions']
    expected = {(d['page'],d['raw']) for d in decisions}
    found = {(i,clean(line)) for i,page in enumerate(paper,1) for line in page.get_text().splitlines() if DIRECTIVE.search(clean(line))}
    assert found == expected, ('Unclassified/stale selection directives', found-expected, expected-found)
    return decisions

def build():
    import fitz
    paper_path = ROOT / f'paper-trail-corpus/exampapers/2012/{FILE}.pdf'
    scheme_path = ROOT / f'paper-trail-corpus/markingschemes/2012/{FILE}.pdf'
    assert hashlib.sha256(paper_path.read_bytes()).hexdigest() == '14198719b5ef0301924d5d139d77ae34206f300ff5c62c8f4cb24e8b6c4e3f40', 'Paper changed: repeat visual review'
    assert hashlib.sha256(scheme_path.read_bytes()).hexdigest() == '61ce5779e123b1a18df15773ec5fa6876466282ebaaa9878cca03f0ba2c79e03', 'Scheme changed: repeat visual review'
    paper = fitz.open(paper_path)
    scheme = fitz.open(scheme_path)
    texts = [clean(p.get_text()) for p in paper]
    cards = []
    def add(key, section, ref, prompt, topic, exam_topics, pages, scheme_pages, criteria,
            requirements=None, note=None, **extra):
        marks = sum(c['maxMarks'] for c in criteria if c['kind'] == 'award')
        card = dict(id=f'irish-2012-fl-{key.lower()}', year=2012, level='foundation',
            paper=1, section=section, atlasQuestionId=key,
            questionRef=f'2012 FL {ref}', questionText=prompt, totalMarks=marks,
            topicId=topic, examTopicKeys=exam_topics, conceptId=f'irish-foundation-{key.lower()}',
            paperFileid=FILE, schemePage=scheme_pages[0], schemePages=scheme_pages,
            taskRequirements=requirements or [], criteria=criteria,
            markingGuideNote=note or 'Use the answer and tariff published by the SEC for this part.',
            sourceMaterial=dict(kind='source-text', label=ref,
                title=f'Gaeilge Bonnleibhéal 2012 · {ref}', pages=pages,
                attribution='© State Examinations Commission.',
                presentationNote='Original examination pages, including every required picture or passage.'),
            **extra)
        cards.append(card)
        return card

    # Multiple-choice distractors are possible answers to ONE task, not alternative
    # tasks; expanding them would teach knowingly wrong responses as valid routes.
    aural = [('1a', 2, 6, 'Cén cúrsa atá á dhéanamh ag Helen?', None, 'Cúrsa Eolaíochta = an tríú pictiúr'),
 ('1b',
  2,
  6,
  'Cad a bheidh á dhéanamh ag Helen an deireadh seachtaine seo chugainn?',
  'Ag dreapadóireacht | Ag tiomáint | Ag staidéar',
  'Ag staidéar'),
 ('2a', 2, 18, 'Cén post atá ag Diarmaid?', None, 'Múinteoir Corpoideachais = an dara pictiúr'),
 ('2b', 2, 18, 'Cén spórt a imríonn Diarmaid go rialta?', 'Cispheil | Rugbaí | Sacar', 'Rugbaí'),
 ('3', 3, 18, 'Cá bhfuil an bhean ag dul?', None, 'Siopa Rothar = an tríú pictiúr'),
 ('4',
  3,
  6,
  'Cá bhfuil an séipéal? (Cuir tic (✓) sa bhosca ceart.)',
  None,
  'An bosca ag an mbarr ar clé (tic nó saighead)'),
 ('5a',
  3,
  6,
  'Conas mar a bheidh an aimsir don cheolchoirm i bPáirc an Chrócaigh anocht?',
  None,
  'Scamallach = an dara pictiúr'),
 ('5b', 4, 6, 'Conas mar a bheidh an aimsir i rith an lae amárach?', 'Fliuch | Grianmhar | Tirim', 'Fliuch'),
 ('6a',
  4,
  6,
  'Cad a cheap Pól faoin scrúdú Mata?',
  'Bhí sé éasca | Bhí sé deacair | Bhí sé maith go leor',
  'Bhí sé deacair'),
 ('6b',
  4,
  6,
  'Cén áit a mbeidh Pól ag obair sa samhradh?',
  'I siopa faisin | I mbialann | In ollmhargadh',
  'In Ollmhargadh'),
 ('7a',
  4,
  6,
  'Cá háit a raibh Eoin ag an deireadh seachtaine?',
  'I nGaillimh | I Londain | I dTulach Mhór',
  'I nGaillimh'),
 ('7b', 4, 6, 'Cad a bhuaigh máthair Chiara i gcomórtas ar an raidió?', 'Rás | Ticéid | T-léine', 'Ticéid'),
 ('8a',
  4,
  6,
  'Cén comórtas a bheidh ar siúl Dé hAoine seo chugainn?',
  'Comórtas peile | Comórtas scannánaíochta | Comórtas Tráth na gCeist Boird',
  'Comórtas Tráth na gCeist Boird'),
 ('8b', 4, 6, 'Cén táille iontrála atá le híoc ag gach foireann?', '€5 | €20 | €30', '€20')]
    audio_url = 'https://www.examinations.ie/archive/exampapers/2012/LC001BLPO17IV.mp3'
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
                title='Gaeilge Bonnleibhéal 2012 · An Chluastuiscint',playbackUrl=audio_url,
                secFileid='LC001BLPO17IV.mp3',canonicalUrl=audio_url,
                attribution='© State Examinations Commission.',
                presentationNote='Official Foundation Level recording. Answer the question shown using its printed options.'))


    signs = ['Traenáil do Pheileadóirí\nPáirc Uí Néill\nAnocht 7.30 p.m.',
 'Earraí Cistine\nMiasniteoir agus Sorn Cistine\nAr Leathphraghas',
 'Aonad Éigeandála\nOspidéal na hOllscoile\nCláraigh anseo le do thoil',
 'Ceachtanna Tiomána\n€35 san Uair\nTeagascóir cláraithe',
 'Buail isteach sa Siopa Feirme\nGlasraí Úra - Uibheacha\nFeirm De Róiste',
 'Ciúnas!\nScrúdú ar siúl anseo.',
 '“Nead an Dreoilín”\nNaíonra Lán-Ghaelach\nFón: 096-675432',
 'Tá Cosc ar Fhóin Phóca\nSa Scoil Seo.\nGo raibh maith agat.',
 'Spéaclaí de gach saghas\n“Na faisin is déanaí\nar phraghas réasúnta!”',
 'Meicneoir cáilithe ag teastáil\nGaráiste Uí Néill\nLongfort']
    for i,(sign,answer) in enumerate(zip(signs,'JGHDBAEFIC'),1):
        add(f'R-1-{i}','2',f'Léamhthuiscint · Ceist 1({i})',
            'Meaitseáil na pictiúir leis na fógraí/comharthaí agus scríobh síos an litir cheart sa bhosca in aice leis an uimhir cheart atá sa ghreille.\n\n'+f'{i}. {sign}',
            'irish-9-1',['match'],[5],[4],
            [criterion('answer','Litir cheart',4,[answer],True)])

    # Each row: verbatim question, printed alternatives (or none), official answer.
    reading = {'2A': (6,
        'letterReading',
        [('Cén dáta ar fhreastail Úna Nic Thomáis ar agallamh?',
          '27 Aibreán | 3 Bealtaine | 1 Meitheamh',
          '27 Aibreán'),
         ('Céard a fuair Úna ón gCumann Sábháilteachta Uisce?',
          'Ardteistiméireacht | Teastas Athbheochana | Teastas Tarrthála Uisce',
          'Teastas Tarrthála Uisce'),
         ('Cén áit a mbeidh Úna ag obair sa phost seo?',
          'I gCill Airne | Ar an Trá Bhán | I dTrá Lí',
          'Ar an Trá Bhán'),
         ('Cé mhéad lá saor a bheidh ag Úna gach seachtain?', 'Aon lá amháin | Dhá lá | Trí lá', 'Dhá lá'),
         ('Cén post atá ag Síle Ní Néill?',
          'Comhairleoir | Garda Tarrthála | Oifigeach Pearsanra',
          'Oifigeach Pearsanra')]),
 '2B': (7,
        'brochure',
        [('Cad atá in iarthar Chontae Mhaigh Eo?',
          'Abhainn na Sionainne | Cathracha móra | Oileán Acla',
          'Oileán Acla'),
         ('Cén teanga atá á labhairt go coitianta ar Oileán Acla?',
          'Fraincis | Gaeilge | Gearmáinis',
          'Gaeilge'),
         ('Cathain a tógadh an caisleán ar Acaill?',
          'Sa chúigiú haois déag | Le linn an Ghorta | Ceithre scór bliain ó shin',
          'Sa chúigiú haois déag'),
         ('Cad a spreagann na healaíontóirí ar Acaill?', 'An galf | An stair | Na radhairc', 'Na radhairc'),
         ('Cad atá ar gach trá ar Oileán Acla?', 'Aill | Brat gorm | Caisleán', 'Brat gorm')]),
 '2C': (8,
        'news',
        [('Cá raibh Pól Ó Dúill inné?', 'Muine Bheag | Cill Chainnigh | Iarnród Éireann', 'Cill Chainnigh'),
         ('Cad a chonaic Pól ar na ráillí an Satharn sin?', 'Crann | Droichead | Traein', 'Crann'),
         ('Cad a chaith Pól ar an talamh?',
          'Fón póca | Trealamh iascaireachta | Uaireadóir',
          'Trealamh iascaireachta'),
         ('Cá fhad a rith Pól i dtreo Mhuine Bheag?', '200 m | 400 m | 600 m', '400m'),
         ('Cén dath a bhí ar gheansaí Phóil?', 'Dearg | Dubh | Liath', 'Dearg')]),
 '3A': (9,
        'news',
        [('Cén saghas éadaí is breá le hImelda? Éadaí ó na …',
          'Caogaidí | Seascaidí | Seachtóidí',
          'Éadaí ó na caogaidí'),
         ('Cén stíl cheoil is fearr le hImelda?', 'Na Gormacha | “Rockabilly” | Snagcheol', 'Rockabilly'),
         ('Cad a rinne Imelda nuair a bhí sí 16 bliana d’aois?', None, 'Thosaigh sí ag canadh i gclubanna'),
         ('Cé leis a raibh Imelda ar an teilifís sa Bhreatain?',
          'Jay Leno | Jeff Beck | Jools Holland',
          'Jools Holland'),
         ('Cén bhliain ar chuir Imelda a céad albam amach?', '2003 | 2006 | 2010', '2003')]),
 '3B': (10,
        'extract',
        [('Cén áit a bhfuil an tríú staid is mó san Eoraip?',
          'I mBarcelona | I Londain | I mBaile Átha Cliath',
          'I mBaile Átha Cliath'),
         ('Cén spórt a d’imir Frank Dineen?',
          'Iománaíocht | Lúthchleasaíocht | Peil Ghaelach',
          'Lúthchleasaíocht'),
         ('Cén bhliain ar cheannaigh Frank an 14 acra talún?', '1862 | 1901 | 1908', '1908'),
         ('Cén bhaint a bhí ag an Ardeaspag Cróc le Cumann Lúthchleas Gael?',
          'Pátrún | Rúnaí | Uachtarán',
          'Pátrún'),
         ('Cad as a ndearnadh an cnoc ar thaobh na páirce i 1917?', None, 'smionagar')]),
 '3C': (11,
        'poem',
        [('Cén saghas peata í Róise?', 'Páiste | Éan | Cat', 'Cat'),
         ('Cén áit a gcaitheann Róise an oíche?', 'Sa teach | Ar chúl an tí | Sa leaba', 'Ar chúl an tí'),
         ('Cá dtéann Róise gach maidin?', None, 'N’fheadar'),
         ('Cén t-am a fhilleann Róise abhaile?', 'Roimh a trí | Am nóin | Roimh oíche', 'Roimh oíche'),
         ('Cén áit a mbíonn Róise ag sú teasa?',
          'Ar chúl an tí | Os comhair na tine | Sa chlós',
          'Os comhair na tine')])}
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
                'irish-9-2',[exam_topic],[page],([4] if slot[0]=='2' else [5,6] if (slot,i) in [('3A',3),('3B',5),('3C',3)] else [5]),
                [criterion('answer','Freagra',5 if slot[0]=='2' else 6,[answer],True)])
            if slot == '3A' and i == 3:
                card['criteria'][0]['permittedMarks'] = [0,3,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: Thosaigh sí ag canadh i gclubanna (agus gan í ach sé bliana déag d’aois); (ag) canadh i gclubanna; Thosaigh sí i gclubanna.',
                    '4 mharc: Thosaigh sí ag obair i gclubanna; Thosaigh sí ag canadh.',
                    '3 mharc: Ag canadh; Ag obair i gclubanna.',
                    'Iomarcaíocht: an t-eolas i gceart ach dhá abairt ón sliocht scríofa — pionós −2.']
            if slot == '3B' and i == 5:
                card['criteria'][0]['permittedMarks'] = [0,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: (as) Smionagar; Smionagar ó Shráid Sackville; (as) an smionagar a bhí fágtha ar Shráid Sackville (tar éis éirí amach na Cásca i1916). Glac leis an abairt iomlán “Sa bhliain1917 … i1916”.',
                    'Iomarcaíocht: abairt bhreise — pionós −2.']
            if slot == '3C' and i == 3:
                card['criteria'][0]['permittedMarks'] = [0,4,6]
                card['criteria'][0]['guidance'] += [
                    '6 mharc: N’fheadar (in aon chor) (cá dtéann sí); Bailíonn sí léi (de sciuird); líne1+2 as Véarsa2; líne3+4 as Véarsa2.',
                    '4 mharc: líne2+3 le chéile; Véarsa2 iomlán. 0 marc: líne2 leis féin.']
            reading_cards[slot].append(card)

    def combine(key,ref,members,pool_quote):
        criteria=[]
        for member in members:
            prefix=member['atlasQuestionId'].lower()+'-'
            for old in member['criteria']:
                c=copy.deepcopy(old)
                c['id']=prefix+c['id']
                c['label']=member['questionRef'].replace('2012 FL ','')+' · '+c['label']
                if 'deductFrom' in c: c['deductFrom']=prefix+c['deductFrom']
                criteria.append(c)
        topics=list(dict.fromkeys(t for c in members for t in [c['topicId'],*c.get('additionalTopicIds',[])]))
        result=add(key,members[0]['section'],ref,
            pool_quote+'\n\nAn rogha don chárta seo: '+ref+'\n\n'+
            '\n\n'.join(c['questionRef'].replace('2012 FL ','')+'\n'+c['questionText'] for c in members),
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
            'PDF page16 gives reasonable-accommodation guidance excluding spelling and certain grammar for eligible candidates; no four-mark language conversion table is printed in2012.'])
    def scheme_guidance(start,end):
        return [clean(re.sub(r'Gaeilge\s+ATBL 2012\s+\d+', '', scheme_page_text(scheme[p-1]))) for p in range(start,end+1)]
    notice_p8,notice_p9,notice_p10 = scheme_guidance(8,10)
    notice = add('W-4A','3','Scríobh · Ceist 4(a)',
        'Féach ar na pictiúir thíos.\n\nScríobh amach an FÓGRA a bhaineann leis an rud atá i gceist thuas.\n\n'
        'Cén rud a bheidh ar siúl? Cén áit a mbeidh sé?\nCén lá? Dáta? Am? Cead isteach?\nCén t-aoi speisialta?\nCá rachaidh an t-airgead?',
        'irish-9-3',['notice'],[14],[8,9,10],[
            criterion('leagan','Leagan Amach',1,['Iarracht ar fhógra.']),
            criterion('pictiur1','Pictiúr 1',8,[notice_p8.split('Pictiúr 1:',1)[1],notice_p9.split('Pictiúr 2:',1)[0]]),
            criterion('pictiur2','Pictiúr 2',13,[notice_p9.split('Pictiúr 2:',1)[1],notice_p10.split('Pictiúr 3:',1)[0]]),
            criterion('pictiur3','Pictiúr 3',4,[notice_p10.split('Pictiúr 3:',1)[1].split('Pictiúr 4:',1)[0]]),
            criterion('pictiur4','Pictiúr 4',4,[notice_p10.split('Pictiúr 4:',1)[1].split('Cruinneas Gaeilge',1)[0]]),language(10)],
        ['Scríobh fógra bunaithe ar na ceithre phictiúr agus ar na treoracha.'],
        'Layout1; required pictures8+13+4+4; shared language10. Keep the2012 activity4/3, venue4/3/2, day4/3/2, date3/2, fee3/2, Jedward4/3/2 and Barnardos4/3 allowances inside each picture award. No later-year rules are substituted.')
    form_prompt = (
        'Ba mhaith leat a bheith ag obair mar Chúntóir in Ionad Spóirt.\n\n'
        'Líon isteach An Fhoirm Iarratais atá anseo thíos. [Nóta: Is tusa Síle Ní Ruairc.]\n\n'
        'Ionad Spóirt Loch Garman\nFoirm Iarratais do phost mar Chúntóir\n\n'
        'Ainm: Síle Ní Ruairc\nUimhir theileafóin:\nSeoladh:\nAois:\nDáta Breithe:\n'
        'An bhfuil scileanna ríomhaireachta agat?\nCén Scrúdú Teistiméireachta atá déanta agat?\n'
        'Ainmnigh cúig ábhar scoile a rinne tú sa scrúdú sin:\nLuaigh trí spórt is féidir leat a mhúineadh:\n'
        'An ndéanann tú traenáil go rialta?\nAn féidir leat snámh?\nAn mbeidh tú sásta a bheith ag obair gach Satharn?\n'
        'An bhfuil taithí agat ar bheith ag múineadh páistí?\n'
        'Cuir tic (✓) leis an dáta is fearr leat le haghaidh agallaimh: 19 Iúil / 21 Iúil / 24 Iúil\n\n'
        'Scríobh alt beag (timpeall 40 focal) ag insint cén fáth ar mhaith leat a bheith ag obair in Ionad Spóirt.\n\n'
        'Síniú: Síle Ní Ruairc\nDáta:'
    )
    for day in [19,21,24]:
        assert f'{day} Iúil' in texts[14], 'Interview date changed: repeat selection review'
    fields_guide = [
        'Na Ceisteanna =15 mharc. Colún dúbailte: uimhir theileafóin1; seoladh2; aois1; dáta breithe2; ríomhaireacht1; scrúdú1; cúig ábhar10; trí spórt6; traenáil1; snámh1; Satharn1; taithí le páistí1; dáta agallaimh1; dáta ag bun1. Iomlán30 ÷2 =15.',
        'Round up once after adding the doubled question awards and dividing by two:21 ÷2 =10½ →11. Do not round each half-mark field separately.',
        scheme_guidance(11,11)[0].split('An Córas Marcála',1)[1].split('(ii)',1)[0],
        scheme_guidance(12,12)[0].split('An t-Alt:',1)[0],
    ]
    forms=[]
    for day in [19,21,24]:
        forms.append(add(f'W-4B-{day}-iuil','3',f'Scríobh · Ceist 4(b) · {day} Iúil',
            form_prompt+f'\n\nAn rogha don chárta seo: {day} Iúil.',
            'irish-9-0',['form'],[15],[11,12],[
                criterion('fields','Na Ceisteanna · iomlán slán',15,fields_guide),
                criterion('paragraph','An t-Alt · marc tar éis coigeartú faid',15,[
                    scheme_guidance(11,11)[0].split('(ii)',1)[1],
                    scheme_guidance(12,12)[0].split('An t-Alt:',1)[1],
                    'Mark the relevant paragraph out of15 (off-topic ceiling5), then apply the proportional short-length reduction to this paragraph award only.20 of40 words → deduct50% of the awarded paragraph mark. Keep the fields and shared-language awards separate. No fixed number of references is required.'
                ]),language(10)],
            ['Líon gach réimse riachtanach; cúig ábhar scoile agus trí spórt is féidir leat a mhúineadh.',
             f'Roghnaigh {day} Iúil don agallamh.',
             'Scríobh timpeall40 focal faoi bheith ag obair in Ionad Spóirt.'],
            'One whole40-mark form: fields15 (half marks combined then rounded up once), paragraph15 with its own length adjustment, shared language10. Three printed interview dates are expanded; subjects, sports and communicative form answers remain open content.'))
    stories=[]
    for slot,page,start,end in [('5A',16,13,14),('5B',17,14,15)]:
        prompt = (
            'Féach ar an bpictiúr thíos.\n\nBhí tú ag Picnic faoin Tuath leis an gClub Óige an mhí seo caite.\nTá tú chun cuntas (timpeall 90 focal) a scríobh in Iris na Scoile faoi.\n\nScríobh an cuntas sin (timpeall 90 focal) sa spás atá faoin bpictiúr.\n\nPicnic faoin Tuath leis an gClub Óige'
            if slot == '5A' else
            'Féach ar na pictiúir anseo thíos.\n\nTharla an eachtra seo agus tú amuigh ag dioscó le do chara.\nTá tú chun scríobh faoin eachtra seo in Iris na Scoile (timpeall 90 focal).\n\nScríobh faoin eachtra (timpeall 90 focal) sa spás atá faoi na pictiúir.\n\nEACHTRA A THARLA'
        )
        guidance=scheme_guidance(start,end)
        # PDF14 contains the end of5(a) and beginning of5(b); keep only this task.
        if slot=='5A': guidance[-1]=guidance[-1].split('(b) Eachtra',1)[0]
        else: guidance[0]=guidance[0].split('(b) Eachtra',1)[1]
        stories.append(add('W-'+slot,'3','Scríobh · Ceist '+slot[0]+'('+slot[1].lower()+')',
            prompt,'irish-9-4',['pictures','story'],[page],list(range(start,end+1)),[
                criterion('cumarsaid','Cumas Cumarsáide · marc tar éis coigeartú faid',37,[
                    'Reduce the communication ceiling by5 for each missing reference. Assess communication against that ceiling, then reduce the awarded communication mark proportionally for insufficient length. Keep the language mark separate.',
                    *guidance,
                    'Published worked examples:60 words, one missing reference → ceiling32, communication27 minus9 =18.45words, two missing references → ceiling27, communication20 minus10 =10. Language is assessed separately /13 (example7). Apply the length adjustment only to this story’s communication score, never to language or the other question.'
                ]),language(13)],
            ['Scríobh timpeall 90 focal in Iris na Scoile.','Tabhair cúig thagairt ar a laghad; i5(b), ceann do gach pictiúr agus ceann amháin eile.'],
            'Communication37 with a5-mark ceiling reduction per missing reference and proportional length adjustment; language13 assessed separately. For5(b), cover all four pictures plus a fifth detail, ideally two in picture3; the printed allowance accepts another detail elsewhere if the narrative remains continuous. These references are required content with indicative examples, not a finite task pool.'))
    # Q4 and Q5 are both compulsory, with one of A/B in each: eight products, including three form dates.
    for first,second in itertools.product([notice,*forms],stories):
        combine(first['atlasQuestionId']+'-'+second['atlasQuestionId'].removeprefix('W-'),
            first['questionRef'].replace('2012 FL ','')+' + '+second['questionRef'].replace('2012 FL ',''),
            [first,second], 'FREAGAIR GACH CEIST (4 AGUS 5). Ceist 4: Freagair (a) NÓ (b). Ceist 5: Freagair (a) NÓ (b).')
    # Classify exact raw directive lines across all twenty paper pages. Unknown
    # additions on an already-reviewed page and stale keys both fail generation.
    decisions = selection_decisions(paper)
    assert len(cards)==74 and len({c['id'] for c in cards})==74
    assert sum(c['totalMarks'] for c in cards if c['atlasQuestionId'].startswith('A-'))==120
    review=dict(year=2012,level='foundation',paperFileid=FILE+'.pdf',
        paperSha256=hashlib.sha256(paper_path.read_bytes()).hexdigest(),
        schemeSha256=hashlib.sha256(scheme_path.read_bytes()).hexdigest(),
        reviewedPaperPages=list(range(1,21)),reviewedSchemePages=list(range(1,21)),
        reviewDate='2026-10-07',status='reviewed',selectionDecisions=decisions,
        fullPaperAndApplicableSchemeVisualSweep=True,
        atomicPracticeCardIds=[c['id'] for c in cards if 'memberCardIds' not in c],
        pairedRouteCardIds=[c['id'] for c in cards if 'memberCardIds' in c],
        examStructure=dict(listening=120,matching=40,readingQ2=50,readingQ3=60,writingQ4=40,writingQ5=50,writing=90,total=360),
        nonPoolDecisions=[
            'MCQ distractors and map boxes are answers to one task, not independently valid task routes.',
            'All notice headings and form fields are required. The three printed interview dates are mechanically expanded; each whole form keeps its shared language award.',
            'Five school subjects and three sports are open content, not finite enumerated task prompts. Poem conjunctions nó are source content, not answer-selection directives.',
            'The five story references are a communication criterion, with non-exhaustive examples, not a printed choose-five menu.',
            'The modified marking scheme changes assessment for eligible candidates, not the printed task or answer route.',
        ],
        openIssues=[],
        audio=json.loads(SOURCE_REVIEW.read_text())['audio'],
        boundaries='14 listening parts; 10 matching parts; 30 reading parts; 6 whole writing routes including three form dates; 6 paired reading routes; 8 writing products (one Q4 and one Q5).',
        caveats=json.loads(SOURCE_REVIEW.read_text())['sourceFindings'])
    return dict(review=review,cards=cards),scheme

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    data,scheme=build()
    content=json.dumps(data,ensure_ascii=False,indent=2)+'\n'
    scheme_text='# Gaeilge Bonnleibhéal 2012 — SEC marking scheme\n\n'+'\n\n'.join(f'## PDF page {i+1}\n\n'+scheme_page_text(p) for i,p in enumerate(scheme))
    scheme_text = '\n'.join(line.rstrip() for line in scheme_text.splitlines()).rstrip()+'\n'
    outputs={OUT:content,ROOT/'examiner-reports/irish/schemes/2012-fl.md':scheme_text}
    for path,value in outputs.items():
        if args.check:
            assert path.exists() and path.read_text()==value, f'Stale Foundation output: {path}'
        else: path.write_text(value)
    print(f"Irish Foundation 2012: {len(data['cards'])} reviewed task/selection cards; archive remains incomplete.")

if __name__=='__main__': main()
